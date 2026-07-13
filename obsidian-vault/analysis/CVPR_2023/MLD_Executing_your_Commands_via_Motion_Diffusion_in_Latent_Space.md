---
title: "MLD: Executing your Commands via Motion Diffusion in Latent Space"
type: paper
paper_level: A
venue: CVPR
year: 2023
pdf_ref: paperPDFs/CVPR_2023/MLD_Executing_your_Commands_via_Motion_Diffusion_in_Latent_Space.pdf
project_link: null
code_link: https://github.com/chenfengye/motion-latent-diffusion
aliases:
- MLBDM
- MLD
tags:
- CVPR_2023
- topic/motion_animation
- topic/motion_animation/human_motion_generation
core_operator: "控制隐空间的表示能力和维度（通过VAE的架构和隐变量形状），以及条件嵌入与隐码的融合方式，是影响生成质量和效率的关键调节变量。"
primary_logic: "先训练一个强大的运动VAE，将运动压缩到低维、高信息密度的隐空间，然后在该隐空间上执行扩散过程来建立条件到运动的映射，从而大幅降低计算量并提升生成质量。"
claims:
- "在HumanML3D数据集上，MLD的FID达到0.473，显著优于之前最优的扩散模型MDM（0.544）和MotionDiffuse（0.630）。"
- "MLD的推理速度比在原始运动序列上扩散的MDM快两个数量级（AITS对比，Figure 6）。"
- "消融实验证明，使用VAE隐空间（而非普通自动编码器）和长跳跃连接对生成质量至关重要。"
- "HumanML3D 上 FID = 0.473"
---

# MLD: Executing your Commands via Motion Diffusion in Latent Space

> [!tip] 核心洞察
> 先训练一个强大的运动VAE，将运动压缩到低维、高信息密度的隐空间，然后在该隐空间上执行扩散过程来建立条件到运动的映射，从而大幅降低计算量并提升生成质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | MLD：在隐空间中执行指令——基于运动隐扩散模型 |
| 英文题名 | MLD: Executing your Commands via Motion Diffusion in Latent Space |
| 会议/期刊 | CVPR 2023 |
| Links | [paper](https://arxiv.org/abs/2212.04048) · [GitHub](https://github.com/chenfengye/motion-latent-diffusion) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation |
| Method | Motion Latent-based Diffusion (MLD) |
| Dataset | HumanML3D, KIT |

> [!tip] 效果简介
> - HumanML3D 上，FID 为 0.473，对比 0.544 (MDM)，变化 -0.071。
> - HumanML3D 上，MM Dist 为 3.196，对比 5.566 (MDM)，变化 -2.370。
> - HumanML3D 上，R Precision Top 3 为 0.772，对比 0.611 (MDM)，变化 +0.161。

## 概要

**问题瓶颈**：原始人体运动序列包含显著的时间冗余与噪声，直接在高维原始数据上进行扩散建模导致计算开销巨大且易产生伪影。同时，自然语言与运动序列之间存在巨大的模态分布鸿沟，难以学习跨模态的概率映射。

**核心洞察**：将运动数据压缩至低维、高信息密度的隐空间，再在该隐空间上执行扩散过程，从而将“条件→运动”的映射问题转化为“条件→隐码”的映射问题，大幅降低计算量并提升生成质量。

**方法定位**：本文提出 **Motion Latent-based Diffusion (MLD)**，属于“隐空间扩散生成”范式。其方法谱系可概括为：

- **上游表示学习**：构建带长跳跃连接的Transformer运动VAE，将原始运动序列编码为紧凑隐变量 $z$（Sec. 3.1）。
- **下游条件扩散**：在冻结的运动隐空间上训练Transformer去噪器 $\epsilon_\theta$，条件（文本/动作标签）经编码后与隐码拼接注入（Sec. 3.2–3.3）。
- **与基线差异**：区别于 **MDM** 在原始运动序列上直接扩散、**MotionDiffuse** 在原始空间做条件扩散、**TEMOS** 使用VAE但以KL对齐方式注入条件，MLD的关键变化是将扩散目标空间从原始运动序列迁移至运动VAE的隐空间，并采用拼接式条件注入与长跳跃连接架构。

**主要结果**：在HumanML3D文本-运动生成基准上，MLD的FID达到 **0.473**，显著优于此前最优扩散模型MDM（0.544）和MotionDiffuse（0.630）；MM Dist降至 **3.196**（MDM为5.566）；R Precision Top-3提升至 **0.772**（MDM为0.611）。在KIT数据集上FID达到 **0.404**（MDM为0.497）。推理速度方面，MLD比MDM快约两个数量级（Figure 6）。消融实验证实，VAE隐空间（对比普通自动编码器）和长跳跃连接是生成质量的关键保障。

### 问题背景：文本驱动的三维人体运动生成

文本到运动生成（Text-to-Motion Generation）旨在根据自然语言描述合成逼真的三维人体运动序列。该任务在游戏开发、影视制作、虚拟人交互和机器人学习等场景中具有广泛的应用前景。与图像或语音生成不同，人体运动数据具有高维时序结构，每一帧通常由若干关节的三维旋转或位置参数表示，且不同动作之间存在复杂的运动学约束和时序依赖。因此，如何从离散、抽象的语言描述映射到连续、高维的运动序列，是该领域的核心挑战。

### 现有方法缺口：扩散模型在原始运动空间上的效率瓶颈

近年来，扩散模型（Diffusion Models）在图像和视频生成领域取得了显著成功，并开始被引入运动生成任务。代表性工作如 **MDM** 和 **MotionDiffuse** 直接在原始运动序列上执行扩散过程，即逐步向运动数据添加噪声并学习逆向去噪。然而，这一范式面临两个根本性困难：

1. **计算开销巨大**：原始运动序列通常具有较高的时间维度（例如每秒30帧，持续数秒），直接在原始空间进行多步扩散意味着每一轮去噪都需要处理完整的高维张量。这导致训练和推理耗时极长，限制了模型的实用化部署。
2. **原始运动空间的冗余与噪声**：人体运动数据天然存在时间冗余——相邻帧之间变化微小，且数据采集过程中常引入标记噪声。扩散模型若直接在此类冗余、嘈杂的空间上建模，不仅浪费计算资源，还容易产生不自然的抖动或伪影，损害生成质量。

此外，文本条件与运动序列之间的跨模态分布差异巨大。文本是离散、稀疏的语义符号，而运动是连续、稠密的时序信号。直接在高维运动空间学习条件概率映射 $p(x \mid c)$ 难度极大，往往需要大量训练数据和精心设计的条件注入机制。

### 本文动机：将扩散过程迁移到低维运动隐空间

受图像领域隐扩散模型（Latent Diffusion Models）的启发，本文提出一个核心洞察：**先学习一个强大的运动变分自编码器（VAE），将运动序列压缩到低维、高信息密度的隐空间，然后在该隐空间上执行扩散过程**。这一思路旨在从根源上解决上述两个瓶颈：

- **降低计算维度**：隐空间的维度远小于原始运动序列，扩散过程在低维空间进行，可大幅减少每步去噪的计算量，从而显著加速训练和推理。
- **提升表征质量**：VAE通过重构和KL正则化训练，能够自动滤除原始运动中的冗余和噪声，提取出紧致且富有语义的隐表征。在此“干净”的隐空间上建模条件分布，有助于生成更平滑、更符合文本语义的运动。

基于这一动机，本文提出了 **Motion Latent-based Diffusion (MLD)** 模型。MLD采用两阶段训练范式：第一阶段训练运动VAE以获取高质量的运动隐空间；第二阶段在该隐空间上训练条件扩散模型，实现从文本或动作标签到运动隐码的映射，最终通过解码器一次前向即可重建出运动序列。这一设计将扩散模型的强大生成能力与隐空间的高效表征能力有机结合，为高质量、高效率的条件运动生成提供了新的技术路径。

## 核心方法与创新机理

MLD 的核心创新在于将扩散模型的生成目标从**原始运动序列空间**迁移至**运动隐空间**，并通过一系列架构与训练策略的配套改进，实现了生成质量与推理效率的双重突破。以下从三个关键维度展开分析。

### 1. 扩散目标空间的迁移：从原始运动到隐空间

传统扩散式文本-运动生成方法（如 MDM、MotionDiffuse）直接在原始运动特征序列上执行前向加噪与反向去噪过程。然而，原始运动数据存在显著的时间冗余与噪声，导致扩散模型计算开销巨大，且容易在生成结果中引入伪影。

MLD 的核心洞察在于：**先训练一个强大的运动变分自编码器（VAE），将高维运动序列压缩至低维、高信息密度的隐空间，再在该隐空间上执行扩散过程**。这一设计将扩散模型的目标从原始运动序列 $x^{1:L}$ 转变为隐变量 $z = \mathcal{E}(x^{1:L})$，从根本上缩小了扩散模型的搜索空间。论文明确指出：“we perform the diffusion process on a representative and low-dimensional motion latent space”（Sec. 3.2）。

这一迁移带来的直接收益是推理速度的量级提升：在 HumanML3D 测试集上，MLD 的推理速度比在原始运动序列上扩散的 MDM 快两个数量级（Figure 6, Sec. 6）。同时，隐空间的紧凑性使得扩散模型能够以更少的去噪步数达到收敛，进一步放大了效率优势。

### 2. 运动 VAE 的架构增强：长跳跃连接与 KL 正则化

运动 VAE 是 MLD 隐空间质量的基础保障。MLD 在 ACTOR 的 Transformer 架构基础上引入了两项关键改进：

**长跳跃连接（Long Skip Connections）**：在 VAE 的编码器 $\mathcal{E}$ 和解码器 $\mathcal{D}$ 的 Transformer 层之间添加长跳跃连接，以缓解深层网络中的梯度消失问题，并促进信息在不同抽象层次间的流动。消融实验表明，这一设计显著加快了扩散模型的收敛速度并提升了生成质量（Figure 9, Table 6）。

**KL 正则化的必要性**：VAE 的 KL 散度损失对于隐空间的结构化至关重要。消融实验（Table 8）对比了使用完整 VAE（含 KL 损失）与使用普通自动编码器（不含 KL 损失）的生成效果：后者在 HumanML3D 上的 FID 从 0.473 急剧恶化至 5.033，充分证明了 KL 正则化对于隐空间连续性和生成质量的决定性作用。

### 3. 条件注入与采样策略：拼接式融合与无分类器引导

在条件注入方式上，MLD 采用**拼接（Concatenation）**策略，将条件嵌入 $\tau_\theta(c)$ 与隐码 $z$ 在特征维度上拼接后输入 Transformer 去噪器 $\epsilon_\theta$。实验表明，这一方式在文本-运动生成任务上优于交叉注意力机制（Table 5）。

此外，MLD 引入了**无分类器引导（Classifier-Free Guidance）**机制，通过调节引导强度 $s$ 来平衡生成多样性与质量：

$$\epsilon_\theta^s(z_t, t, c) = s \epsilon_\theta(z_t, t, c) + (1-s) \epsilon_\theta(z_t, t, \emptyset)$$

这一公式允许模型在条件生成与无条件生成之间插值，为不同应用场景提供了灵活的采样控制。

### 小结

MLD 的创新并非单一技术点的突破，而是**隐空间扩散范式 + VAE 架构增强 + 条件融合策略**的系统性协同：隐空间迁移解决了效率瓶颈，长跳跃连接与 KL 正则化保障了隐空间质量，拼接式条件注入与无分类器引导则提升了条件控制的精度。这一组合使得 MLD 在 HumanML3D 数据集上以 FID 0.473 显著优于此前最优的扩散模型 MDM（0.544）和 MotionDiffuse（0.630），同时实现了两个数量级的推理加速。

MLD 的核心设计遵循 **“先压缩，再生成”** 的两阶段范式，将运动生成问题从高维的原始运动序列空间迁移到低维、高信息密度的隐空间（latent space）中求解。其整体 pipeline 由四个功能模块串联而成，形成一个从条件输入到运动序列输出的端到端生成流程（Figure 2, Figure 12）。


### 模块关系与数据流

1. **运动 VAE（Motion VAE）**：作为 pipeline 的“压缩-重建”底座，由 **运动编码器 ℰ** 和 **运动解码器 𝒟** 构成。ℰ 将原始运动序列 $x^{1:L}$ 映射为紧凑的隐变量 $z = \mathcal{E}(x^{1:L})$；𝒟 则负责从 $z$ 重建运动 $\hat{x}^{1:L} = \mathcal{D}(z)$。该 VAE 在第一阶段独立训练，仅使用 MSE 重建损失与 KL 正则化损失，旨在学到一个兼具表征力与平滑性的运动隐空间（Sec. 3.1）。编码器与解码器均采用带长跳跃连接（long skip connections）的 Transformer 架构，以增强信息流动与训练稳定性。

2. **条件编码器 τ_θ**：接收外部条件输入 $c$（如文本描述或动作类别标签），将其编码为与隐变量维度对齐的条件嵌入 $\tau_\theta(c)$。对于文本条件，默认采用 CLIP 文本编码器以获得更强的语义对齐能力（Table 7 消融实验证实其优于 BERT）。

3. **隐空间去噪器 ε_θ**：这是扩散过程的核心执行单元，在运动隐空间而非原始数据空间上进行去噪。条件嵌入 $\tau_\theta(c)$ 与噪声隐码 $z_t$ 通过**拼接（concatenation）** 的方式融合后，送入基于 Transformer 的去噪器 $\epsilon_\theta$ 中，预测所添加的噪声 $\epsilon$（Sec. 3.3, Table 5 消融表明拼接优于交叉注意力）。去噪器同样配备了长跳跃连接以加速收敛（Figure 9, Table 6）。

4. **两阶段训练与推理流**：训练时，先固定已训好的运动 VAE，仅优化条件扩散模型，损失函数为条件隐扩散损失：
   $$L_{MLD} := \mathbb{E}_{\epsilon, t, c} \left[ \|\epsilon - \epsilon_\theta(z_t, t, \tau_\theta(c))\|_2^2 \right]$$
   推理时，$\epsilon_\theta$ 从随机噪声 $z_T$ 出发，经 $T$ 步迭代去噪得到预测的干净隐码 $\hat{z}_0$，再由解码器 𝒟 单次前向解码为最终的运动序列。为平衡生成质量与多样性，推理阶段引入无分类器引导（classifier-free guidance）：
   $$\epsilon_\theta^s(z_t, t, c) = s \epsilon_\theta(z_t, t, c) + (1-s) \epsilon_\theta(z_t, t, \emptyset)$$

### 关键设计决策

这一架构的核心洞察在于：**将扩散过程的“战场”从原始运动序列转移到 VAE 隐空间**。这直接回应了本领域的瓶颈——原始运动数据存在大量时间冗余与噪声，直接在其上进行扩散建模（如 MDM、MotionDiffuse）不仅计算开销巨大，且易产生伪影。通过 VAE 将运动压缩至极低维度（默认隐变量形状为 $1 \times 256$），MLD 使扩散模型的输入规模缩小了两个数量级，从而在推理速度上比 MDM 快约两个数量级（Figure 6, Table 10），同时实现了更优的生成质量（HumanML3D 上 FID 0.473 vs MDM 0.544, Table 1）。

消融实验进一步揭示了两个关键的因果调节变量：**VAE 的 KL 正则化**（使用普通自编码器而非 VAE 会导致 FID 从 0.473 急剧恶化至 5.033, Table 8）和**隐空间的紧凑性**（较小的 $1 \times 256$ 隐空间在文本生成任务上优于较大的 $7 \times 256$ 隐空间，Table 5），表明在有限数据条件下，强正则化的紧凑表征对扩散建模更为有效。

MLD 的整体架构由四个核心模块构成，按两阶段训练范式组织：第一阶段训练运动 VAE 以获得紧凑的隐空间，第二阶段在该隐空间上训练条件扩散模型。以下逐一阐述各模块的设计逻辑与关键公式。

### 运动编码器 ℰ 与解码器 𝒟

运动 VAE 采用基于 Transformer 的编码器-解码器架构（继承自 ACTOR），并引入**长跳跃连接（long skip connection）**以增强信息流动。给定原始运动序列 $x^{1:L}$，编码器 ℰ 将其映射为隐变量 $z$：

$$z = \mathcal{E}(x^{1:L})$$

解码器 𝒟 则从隐变量重建运动序列：

$$\hat{x}^{1:L} = \mathcal{D}(z) = \bar{\mathcal{D}}(\mathcal{E}(x^{1:L}))$$

VAE 的训练仅使用两项损失：**均方误差（MSE）重建损失**与 **KL 散度正则化损失**。KL 正则化在此处扮演关键角色——消融实验（Table 8）表明，若去除 KL 项退化为普通自动编码器，FID 将从 0.473 急剧恶化至 5.033，证明 VAE 的概率先验对隐空间质量至关重要。

### 隐空间去噪器 ε_θ

这是 MLD 的核心创新所在：**将扩散过程从原始运动空间迁移至运动 VAE 的低维隐空间**。隐空间上的前向扩散过程定义为标准的马尔可夫噪声注入：

$$q(z_t | z_{t-1}) = \mathcal{N}(\sqrt{\alpha_t} z_{t-1}, (1-\alpha_t) I)$$

其中 $\alpha_t$ 为噪声调度参数，控制每一步的信噪比。去噪器 ε_θ 是一个 Transformer 网络，其任务是预测添加的噪声 ε，而非直接预测干净隐码 $z_0$。消融实验（Table 9）证实预测噪声 ε 优于预测 $z_0$（FID: 0.473 vs 0.513）。

无条件生成场景下的简单扩散损失为：

$$L_{\text{MLD}} := \mathbb{E}_{\epsilon, t} \left[ \|\epsilon - \epsilon_\theta(z_t, t)\|_2^2 \right]$$

### 条件编码器 τ_θ 与条件注入

条件编码器 τ_θ 负责将文本（使用 CLIP 编码器）或动作标签映射为条件嵌入 $\tau_\theta(c) \in \mathbb{R}^{1 \times 256}$。条件嵌入与隐码 $z$ 通过**拼接（concatenation）**方式注入 Transformer 去噪器，而非交叉注意力。消融实验（Table 5）表明拼接方式在文本-运动生成任务上更有效。

条件扩散损失在无条件损失基础上引入条件变量 $c$：

$$L_{\text{MLD}} := \mathbb{E}_{\epsilon, t, c} \left[ \|\epsilon - \epsilon_\theta(z_t, t, \tau_\theta(c))\|_2^2 \right]$$

### 无分类器引导采样

推理阶段采用无分类器引导（classifier-free guidance）以平衡生成质量与多样性。引导后的噪声预测为条件预测与无条件预测的线性插值：

$$\epsilon_\theta^s(z_t, t, c) = s \epsilon_\theta(z_t, t, c) + (1-s) \epsilon_\theta(z_t, t, \emptyset)$$

其中 $s$ 为引导尺度（$s > 1$ 增强条件一致性），$\emptyset$ 表示空条件。推理流程为：ε_θ 经过 $T$ 步迭代去噪预测 $\hat{z}_0$，再由解码器 𝒟 单次前向解码为最终运动序列。

## 实验与关键发现

### 核心实验设置

MLD在两阶段训练框架下评估：第一阶段在**HumanML3D**和**KIT**上训练运动VAE（数据集详细统计见[[../../references/T2M_Common_Datasets#HumanML3D|HumanML3D]]和[[../../references/T2M_Common_Datasets#KIT-ML|KIT-ML]]）；第二阶段在冻结的隐空间上训练条件扩散模型。所有方法使用相同的评估协议和特征提取器（来自[16]），推理时间对比在同一**Tesla V100** GPU上进行，排除了模型和数据加载时间以公平比较。对于未开源模型（如TEMOS），作者使用其默认设置重新训练以统一评估指标。

### 文本到运动生成：主结果

在**HumanML3D**数据集上（Table 1），MLD在所有核心指标上均取得最优：

![[assets/figures/papers/paper_list_l10_MLD_Executing_your_Commands_via_Motion_Diffusion_in_Latent_Space/figures/004_Table_1.jpg]]
*Table 1: Comparison of text-conditional motion synthesis on HumanML3D [17] dataset. These metrics are evaluated by the motion encoder from [16]. Empty MModality indicates the non-diverse generation methods. We employ real motion as a reference and sort all methods by descending FIDs. The right arrow → means the closer to real motion the better. Bold and underline indicate the best and the second best result*

| 方法 | FID↓ | R Precision Top-3↑ | MM Dist↓ | Diversity→ | MModality↑ |
|------|------|---------------------|----------|------------|------------|
| Real | 0.002 | 0.797 | 2.974 | 9.503 | - |
| **MLD** | **0.473** | **0.772** | **3.196** | 9.724 | 2.413 |
| MDM | 0.544 | 0.611 | 5.566 | 9.559 | 2.799 |
| MotionDiffuse | 0.630 | 0.739 | 3.113 | 9.410 | 1.553 |
| T2M | 1.087 | 0.740 | 3.340 | 9.188 | 2.090 |
| TEMOS | 3.717 | 0.703 | 3.732 | 8.973 | 0.368 |

MLD的FID达到**0.473**，显著优于此前最优的扩散模型MDM（0.544）和MotionDiffuse（0.630），且与真实运动分布（0.002）的差距大幅缩小。在语义匹配上，R Precision Top-3达到**0.772**，接近真实运动的0.797，而MDM仅为0.611；MM Dist降至**3.196**，远低于MDM的5.566，表明生成运动与文本描述的对齐度显著提升。Diversity指标（9.724）接近真实运动（9.503），MModality（2.413）表明MLD在保持多样性的同时避免模式坍塌。

在**KIT**数据集上（Table 2），MLD同样表现最优：FID为**0.404**，显著优于MDM的0.497和MotionDiffuse的1.954；R Precision Top-3为**0.734**，MM Dist为**2.759**，均优于所有对比方法。

![[assets/figures/papers/paper_list_l10_MLD_Executing_your_Commands_via_Motion_Diffusion_in_Latent_Space/figures/005_Table_2.jpg]]
*Table 2: We involve KIT [48] dataset and evaluate the SOTA methods on the text-to-motion task. (cf. Tab. 1 for metrics details)*

### 动作到运动生成

在**UESTC**和**HumanAct12**的动作条件生成任务上（Table 3），MLD同样展现竞争力：


- **UESTC**：准确率ACC达到**0.954**，Diversity为33.52，FID_train为0.230
- **HumanAct12**：准确率ACC达到**0.964**，Diversity为6.831，FID_train为0.053

MLD在动作识别准确率和生成多样性之间取得了良好平衡，证明了隐空间扩散框架在条件运动生成任务上的通用性。

### 效率分析：推理速度

MLD的核心优势之一是推理效率。**Figure 6**和**Table 10**展示了各方法的平均推理时间（AITS）对比：

- MLD的推理速度比直接在原始运动序列上扩散的**MDM快两个数量级**（约100倍加速）
- 这归因于扩散过程在低维隐空间（如1×256）而非高维原始运动空间（如N×263）上执行
- 较小的隐空间形状（1×256 vs 7×256）进一步降低了计算量，且FID几乎不受影响

### 消融实验：关键设计选择

**1. VAE隐空间 vs 自动编码器隐空间（Table 8）**

这是最关键的消融。移除KL正则化（即使用普通自动编码器而非VAE）后，FID从**0.473急剧恶化至5.033**，R Precision Top-3从0.772降至0.614。这表明VAE的KL正则化迫使隐空间更加规整和连续，对后续扩散建模至关重要——规整的隐空间使扩散过程更容易学习从噪声到有效运动码的映射。

**2. 长跳跃连接（Figure 9, Table 5, Table 6）**

在扩散去噪器中加入长跳跃连接显著加快收敛速度（Figure 9）并提高生成质量。在文本到运动任务中（Table 5），有跳跃连接的MLD-1 FID为**0.473**，而无跳跃连接版本FID为0.577。无条件生成实验（Table 6）同样验证了这一结论。跳跃连接有助于梯度流动，使深层Transformer去噪器更有效地学习隐空间上的去噪映射。

![[assets/figures/papers/paper_list_l10_MLD_Executing_your_Commands_via_Motion_Diffusion_in_Latent_Space/figures/016_Figure_9.jpg]]
*Figure 9: The evaluation on long skip connection on diffusion training stage. Two sub-figures are under the same training process and evaluated on the test set of HumanML3D. Training steps indicate the epoch number*

![[assets/figures/papers/paper_list_l10_MLD_Executing_your_Commands_via_Motion_Diffusion_in_Latent_Space/figures/011_Table_5.jpg]]
*Table 5: Evaluation of text-based motion synthesis on HumanML3D [17]: we use metrics in Tab. 1 and provides real reference, the evaluation on latent z (cf. V in Tab. 4), cross-attention or concatenation with conditions τθ, with (w/) or without (w/o) skip connection, θ with different number of transformer layers*

![[assets/figures/papers/paper_list_l10_MLD_Executing_your_Commands_via_Motion_Diffusion_in_Latent_Space/figures/012_Table_6.jpg]]
*Table 6: Evaluation of unconditional motion generation. From left to right, we evaluate the denoiser $\epsilon _ { \theta }$ with (w/) or without (w/o) skip connection and the latent z $\left$( c f . $\mathcal { V } \right$. in Tab. 4)

**3. 隐空间形状（Table 5）**

较小且紧凑的隐空间形状**1×256**（MLD-1）在文本生成任务上优于更大的**7×256**（MLD-7）：FID 0.473 vs 0.514，R Precision Top-3 0.772 vs 0.755。在有限数据（HumanML3D仅约15k序列）下，紧凑表示降低了学习难度，避免了过拟合和维度灾难。

**4. 去噪目标：预测噪声 vs 预测干净隐码（Table 9）**

预测噪声ε比直接预测干净隐码z₀性能更好：FID **0.473 vs 0.513**，R Precision Top-3 **0.772 vs 0.760**。这与标准扩散模型实践一致——预测噪声是更稳定的训练目标。

**5. 文本编码器选择（Table 7）**

使用**CLIP**文本编码器比BERT在条件匹配指标上更好：CLIP的R Precision Top-3为0.772，MM Dist为3.196；BERT的R Precision Top-3为0.761，MM Dist为3.327。CLIP的视觉-语言联合预训练使其文本嵌入与运动语义更对齐。

**6. 条件注入方式（Table 5）**

将条件嵌入与隐码**拼接**（concatenation）优于交叉注意力（cross-attention）：FID 0.473 vs 0.514。拼接方式更直接地将条件信息注入去噪过程，在隐空间维度较低时尤为有效。

**7. 分类器自由引导（Table 11）**

引导尺度s和dropout概率p对生成质量有显著影响。适当的引导（s>1）可在多样性和质量间取得平衡，但过强的引导会降低多样性。

### 定性分析

**Figure 3**展示了MLD与MDM、MotionDiffuse、T2M、TEMOS在相同文本提示下的可视化对比。MLD生成的运动更准确地匹配描述语义，而其他方法出现动作降级或语义不匹配问题。**Figure 10**通过t-SNE可视化展示了隐码在逆向扩散过程中的演化轨迹：从初始随机噪声（t=49）逐步收敛到按动作类别聚集的结构化分布（t=0），直观验证了隐空间扩散的有效性。

### 失败模式与局限性

1. **有限长度生成**：MLD目前只能生成固定长度的运动序列，难以建模无限延续的非停止运动（如持续行走）。
2. **数据依赖性**：模型泛化能力受限于训练数据规模，HumanML3D仅约15k序列，可能无法覆盖所有可能的人类运动模式。
3. **文本理解瓶颈**：依赖CLIP文本编码器对特定短语的区分能力，复杂或歧义描述仍可能导致语义不匹配。
4. **细粒度动作缺失**：未考虑面部表情、手部细节等精细动作的生成，生成的全身运动缺乏末端执行器的精细控制。

### 用户研究

**Figure 11**的用户偏好研究表明，MLD在所有对比方法中均获得超过50%的偏好率：对MDM约65%，对MotionDiffuse约70%，对T2M约75%，对TEMOS超过85%。这从人类感知角度验证了MLD生成质量的优越性。




![[assets/figures/papers/paper_list_l10_MLD_Executing_your_Commands_via_Motion_Diffusion_in_Latent_Space/figures/018_Table_9.jpg]]
*Table 9: Comparison of text-to-motion. ( c f . Tab. 1 for details.)*

## 定位与知识库关联

### 1. 方法演进脉络与关键基线

MLD 的提出建立在两条技术路线的交汇点上：**运动生成中的变分自编码器（VAE）范式**与**扩散概率模型在连续数据上的应用**。

在 VAE 路线中，**ACTOR**（Petrovich et al., 2021）率先将 Transformer-based VAE 引入动作条件运动生成，但其隐空间缺乏正则化，生成多样性受限。**TEMOS**（Petrovich et al., 2022）进一步引入文本-运动联合 VAE，通过 KL 对齐实现跨模态映射，但生成质量受限于 VAE 固有的模糊重建问题。MLD 继承了 ACTOR 的 Transformer 编码器-解码器架构，但通过引入**长跳跃连接**和**KL 正则化**，将 VAE 的角色从“直接生成器”转变为“隐空间提供者”，这是方法定位上的关键分野。

在扩散路线中，**MDM**（Tevet et al., 2023）和**MotionDiffuse**（Zhang et al., 2023）均直接在原始运动序列上执行扩散过程。MDM 采用 Transformer-based 去噪器预测原始运动信号，MotionDiffuse 则引入文本引导的细粒度控制。这两种方法的共同瓶颈在于：原始运动序列维度高（通常为 $L \times D$，其中 $L$ 为帧数，$D$ 为关节特征维度），且存在大量时间冗余，导致扩散采样需数百步迭代，推理成本极高。MLD 将扩散过程从原始运动空间**迁移至 VAE 隐空间**，这是相对于上述扩散方法的根本性改变——扩散目标从“运动序列”变为“隐码 $z$”，维度从 $L \times D$ 压缩至 $1 \times 256$（默认配置），使推理速度提升约两个数量级（Figure 6 对比 AITS）。

### 2. 技术栈定位与模块继承关系

MLD 的技术栈可拆解为三个可独立分析的模块，各自有清晰的继承或改进谱系：

| 模块 | 继承/参考来源 | MLD 的改进 | 证据锚点 |
|------|-------------|-----------|---------|
| 运动 VAE 架构 | ACTOR 的 Transformer 编解码器 | 引入长跳跃连接，加速收敛并提升重建质量 | Table 4, Figure 9 |
| 隐空间扩散 | 通用隐扩散模型（Latent Diffusion）范式 | 首次将其应用于运动生成领域，扩散目标为 VAE 隐码 $z$ | Sec. 3.2 |
| 条件注入方式 | TEMOS 的跨模态 KL 对齐 | 改为条件嵌入与隐码拼接后输入 Transformer 去噪器 | Sec. 4.2, Table 5 |

值得注意的是，MLD 的**条件编码器**采用 CLIP 文本编码器（而非 TEMOS 使用的 BERT），消融实验（Table 7）证实 CLIP 在条件匹配指标（R Precision、MM Dist）上显著优于 BERT，这暗示视觉-语言预训练模型对运动语义的捕捉优于纯文本模型。

### 3. 适用边界与失效模式

根据论文提供的实验证据与局限性声明，MLD 的适用边界可归纳如下：

**已验证的有效范围：**
- **文本条件运动生成**：在 HumanML3D 和 KIT（数据集统计见[[../../references/T2M_Common_Datasets|T2M Common Datasets]]）上均取得 SOTA FID（0.473 和 0.404），表明对中规模文本-运动对数据有效。
- **动作标签条件生成**：在 UESTC（40 类动作）和 HumanAct12（12 类动作）上取得最高准确率（0.954 和 0.964），表明对离散类别条件有效。
- **无条件生成**：在 AMASS 子集上 FID 优于 ACTOR（Figure 5），但该结论仅在小规模测试上验证。

**已知失效模式与局限：**
1. **有限长度生成**：MLD 只能生成固定长度的运动序列，无法建模无限延续的非停止运动（如“持续行走”）。这是 VAE 固定维度隐空间的结构性限制。
2. **数据饥渴与泛化瓶颈**：HumanML3D 仅含约 15k 序列，模型对训练分布外文本（如复杂组合动作、罕见动词）的泛化能力未经验证。Table 1 中 MLD 的 MModality（3.016）虽优于多数方法，但仍低于 Real（2.794），提示多样性存在上限。
3. **细粒度动作缺失**：模型未建模面部表情、手部姿态等细节，生成的运动仅包含全身关节轨迹。
4. **文本编码器依赖性**：依赖 CLIP 对特定短语的区分能力，歧义或长文本描述可能导致语义不匹配（Figure 3 定性对比中，其他方法出现“downgraded motions or improper semantics”，MLD 虽表现更好，但该问题未彻底解决）。

### 4. 开放问题与后续工作方向

论文明确提出的开放问题包括：

- **跨形态扩展**：能否将隐扩散框架迁移至非人体运动（如动物运动）或细粒度动作（人脸、手部）？这需要重新训练领域特定的 VAE，但隐扩散的架构本身具有通用性。
- **无限运动生成**：如何突破固定长度限制，实现时间一致的非停止运动？可能的路径包括引入自回归隐空间预测或循环 VAE 架构。
- **弱监督/无监督扩展**：如何利用大规模无标注运动数据（如 AMASS 原始 MoCap）提升隐空间质量？当前 VAE 训练仅需运动重建，理论上可接入无标注数据，但条件生成部分仍需配对数据。
- **多模态条件融合**：能否将文本、动作标签、音乐、语音等多模态条件统一注入同一隐扩散框架？当前条件编码器 $\tau_\theta$ 的设计（拼接注入）为多模态扩展提供了接口。

### 5. 在知识库中的定位

MLD 的核心贡献在于**证明了“先压缩再扩散”的两阶段范式在运动生成领域的有效性**。它属于隐扩散模型（Latent Diffusion Models）在结构化序列数据上的成功迁移案例，与图像领域的 Stable Diffusion（Rombach et al., 2022）共享方法论哲学，但针对运动数据的时间冗余特性做了定制化设计（长跳跃连接、紧凑隐空间形状 $1 \times 256$）。

从实验证据强度看，MLD 的 SOTA 声明有较高可信度：FID 提升幅度（-0.071 vs MDM）在相同评估协议下验证，推理速度优势（两个数量级）在相同硬件上测试，消融实验完整覆盖了 VAE vs 自编码器（Table 8）、跳跃连接（Figure 9）、预测目标（Table 9）、条件编码器选择（Table 7）等关键设计选择。但需注意，所有实验均基于 HumanML3D/KIT 等中小规模数据集，在大规模运动数据（如完整 AMASS）上的扩展性尚未验证。

## 原文 PDF

![[paperPDFs/CVPR_2023/MLD_Executing_your_Commands_via_Motion_Diffusion_in_Latent_Space.pdf]]
