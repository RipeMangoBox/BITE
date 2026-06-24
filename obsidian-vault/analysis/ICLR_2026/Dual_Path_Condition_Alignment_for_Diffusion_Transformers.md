---
title: "Dual-Path Condition Alignment for Diffusion Transformers"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Dual_Path_Condition_Alignment_for_Diffusion_Transformers.pdf
openreview_forum_id: ALpn1nQj5R
aliases:
- DPCAD
- DPCADT
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "通过对同一干净图像进行多次独立加噪，并利用解耦扩散Transformer提取不同噪声路径的低频条件特征，强制这些特征彼此对齐，从而在没有外部监督的情况下为模型提供一致的语义引导。"
primary_logic: "同一真实图像的不同噪声版本所携带的低频语义信息在理想情况下应该是不变的。通过对齐这些内部条件，可以替代外部视觉编码器，实现无监督的高效表示引导，显著加速训练并提升生成质量。"
claims:
- "DUPA independently noises an image multiple times and processes these noisy latents through decoupled diffusion transformer, then aligns the derived conditions—low-frequency seman..."
- "DUPA aligns conditions from different noisy latents of the same image without requiring any external visual encoder."
- "ImageNet 256×256 上 FID↓ (with CFG) = 1.46"
- "ImageNet 256×256 上 FID↓ (without CFG) = 5.92"
---

# Dual-Path Condition Alignment for Diffusion Transformers

> [!tip] 核心洞察
> 同一真实图像的不同噪声版本所携带的低频语义信息在理想情况下应该是不变的。通过对齐这些内部条件，可以替代外部视觉编码器，实现无监督的高效表示引导，显著加速训练并提升生成质量。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 扩散Transformer的双路径条件对齐 |
| 英文题名 | Dual-Path Condition Alignment for Diffusion Transformers |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ALpn1nQj5R); [GitHub](https://github.com/PCH-gg/DUPA); [Project](https://openi.pcl.ac.cn/OpenAIDriving/DUPA) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | DUal-Path condition Alignment (DUPA) |
| Dataset | ImageNet 256×256 |

> [!tip] 效果简介
> - ImageNet 256×256 上，FID↓ (with CFG) 为 1.46，对比 2.90 (DDT-XL/2, 400 epochs)，变化 -1.44。
> - ImageNet 256×256 上，FID↓ (without CFG) 为 5.92，对比 8.57 (DDT-XL/2, 400 epochs)，变化 -2.65。
> - ImageNet 256×256 上，IS↑ (with CFG) 为 296.2，对比 229.8 (DDT-XL/2, 400 epochs)，变化 +66.4。

## 概述

扩散Transformer在训练过程中面临一个关键瓶颈：早期层缺乏准确的低频语义引导，导致收敛缓慢且生成质量受限。现有方法（如REPA）虽能借助外部视觉编码器（如DINOv2）提供高质量表示引导，但存在分布偏移和高计算成本的问题。

本文提出**DUal-Path condition Alignment (DUPA)**，一种无需外部视觉编码器的自对齐框架。其核心洞察是：同一真实图像的不同噪声版本所携带的低频语义信息在理想情况下应保持不变。基于此，DUPA对同一干净图像进行多次独立加噪，利用解耦扩散Transformer（DDT）提取不同噪声路径的低频条件特征，并通过最大化这些特征间的余弦相似度来实现内部语义对齐，从而替代外部编码器的监督角色。

DUPA在ImageNet 256×256上取得了显著效果：仅需400个训练epoch，FID即达到1.46（with CFG），不仅优于所有不依赖外部监督的方法，且收敛速度比同类方法快约3倍以上。与基线DDT-XL/2相比，DUPA在无CFG条件下FID从8.57降至5.92，IS从229.8提升至296.2，同时实现了约5倍训练加速和10倍推理加速。消融实验表明，双路径采样与条件对齐的联合引入是性能提升的关键，且独立重采样噪声ε比仅重采样时间戳t对条件对齐更为关键。

## 背景与动机

扩散Transformer（Diffusion Transformer, DiT）已成为视觉生成领域的主流架构，但其训练过程面临一个关键瓶颈：**早期层缺乏准确的低频语义引导，导致收敛缓慢且生成质量受限**。这一问题在无辅助任务的标准训练范式下尤为突出——模型仅依赖速度场预测损失（Equation 3），缺乏对高层语义结构的显式监督信号。

为缓解这一问题，现有方法主要沿两条路径展开。**有监督表示对齐**的代表性工作REPA引入外部视觉编码器（如DINOv2），将扩散Transformer中间层的表示与预训练编码器的输出对齐，从而为生成模型提供高质量的语义引导。然而，这一策略存在两个根本性缺陷：（1）**分布偏移**——外部编码器通常在大规模自然图像上预训练，其表示空间与扩散模型在噪声隐变量上学习到的特征分布存在系统性差异；（2）**高计算成本**——加载并运行一个大型视觉编码器显著增加了训练时的显存占用和计算开销。

**无辅助任务**的基线方法（如SiT、DDT）则完全放弃表示引导，仅依赖去噪目标进行端到端训练。DDT通过解耦扩散Transformer架构将条件编码与速度场预测分离，为后续改进提供了结构基础，但其训练仍缺乏对条件特征质量的直接监督，导致收敛速度远慢于REPA等方法。

上述格局揭示了一个核心张力：**有监督方法效果好但成本高、假设强；无监督方法轻量但收敛慢、质量受限**。本文的核心动机在于打破这一僵局——能否在不引入任何外部视觉编码器的情况下，为扩散Transformer提供同样有效的表示引导？

关键洞察在于：**同一真实图像的不同噪声版本所携带的低频语义信息在理想情况下应该是不变的**。若对一张干净图像进行多次独立加噪，得到的多个噪声隐变量虽然在高频细节上各不相同，但其底层语义结构（如物体类别、空间布局）应当保持一致。因此，从这些不同噪声路径中提取的条件特征应当彼此对齐。基于这一观察，本文提出DUPA（DUal-Path condition Alignment），通过对齐内部条件替代外部编码器，实现无监督的高效表示引导，显著加速训练并提升生成质量。

## 核心创新

### 问题瓶颈：扩散Transformer训练缺乏低频语义引导

扩散Transformer在训练过程中面临一个根本性瓶颈：早期层缺乏准确的低频语义引导，导致模型收敛缓慢且生成质量受限。现有解决方案中，REPA等方法通过引入外部视觉编码器（如DINOv2）提供高质量的表示监督，但这一策略存在两个关键缺陷：一是外部编码器与生成模型之间存在**分布偏移**，二是大规模预训练编码器带来了**高昂的计算与数据成本**。因此，核心问题转化为：**能否在不依赖任何外部视觉编码器的前提下，为扩散Transformer提供有效的表示引导？**

### 核心洞察：同一图像的不同噪声版本共享不变的低频语义

DUPA的关键洞察源于一个简单而深刻的观察：对同一张干净图像进行多次独立加噪，所得到的噪声隐变量虽然在像素层面差异显著，但它们携带的**低频语义信息（如类别、结构）在理想情况下应当是不变的**。这一洞察直接指向一种自对齐策略——如果模型能够从同一图像的不同噪声路径中提取条件特征，并强制这些特征彼此对齐，就能在不引入外部监督的条件下，为模型提供一致的语义引导信号。

### 方法创新：三个关键changed slots

相对于基线方法，DUPA在三个关键维度上进行了创新性改造：

**1. 噪声采样策略：从单路径到双路径**

基线方法（DDT、SiT）对每张图像仅执行单次加噪（K=1），DUPA则将每张图像独立加噪两次（K=2），构造双路径。这一选择的依据是：多次独立噪声采样能够暴露同一底层语义在不同噪声扰动下的表示差异，从而为条件对齐提供必要的对比信号。实验表明，独立重采样噪声ε比仅重采样时间戳t更能提升性能（FID 12.4 vs 13.2，Table 2），证实了噪声多样性对条件对齐的关键作用。

**2. 表示引导方式：从外部编码器到内部自对齐**

REPA依赖外部视觉编码器提供目标表示，而DUPA通过一个可训练的投影器 $z_\phi$ 将不同噪声路径的条件特征映射到对齐空间，最大化它们之间的余弦相似度：

$$\mathcal{L}_{\mathrm{DUPA}}(\theta, \phi) := - \mathbb{E}_{\mathbf{x}_*, \{\epsilon_k, t_k\}_{k=1}^K} \left[ \frac{2}{K(K-1)} \sum_{1 \leq i < j \leq K} \frac{1}{N} \sum_{n=1}^N \sin(z_\phi(\mathbf{z}_{t_i}^{[n]}), z_\phi(\mathbf{z}_{t_j}^{[n]})) \right]$$

这一设计的精妙之处在于：对齐目标完全来自模型内部，无需任何外部表示作为锚点。投影器 $z_\phi$ 的初始化需避免零权重和零偏置，以防止模型走捷径学习到平凡解。

**3. 训练损失函数：去噪与对齐的联合优化**

DUPA的总损失由速度场预测损失和条件对齐损失加权组合而成：

$$\mathcal{L} := \mathcal{L}_{\mathrm{velocity}} + \lambda \mathcal{L}_{\mathrm{DUPA}}$$

其中 $\lambda$ 控制去噪与对齐之间的权衡。这一联合优化框架使得模型在学会去噪的同时，逐步构建跨噪声路径的语义一致性表示。

### 架构实现：解耦扩散Transformer中的条件提取与对齐

DUPA的pipeline由四个核心模块构成（图2）：**Condition Encoder**从噪声隐变量中提取低频语义条件特征 $\mathbf{z}_{t_k}$；**Velocity Decoder**基于条件特征预测速度场 $\mathbf{v}_{t_k}$；**Projector** $z_\phi$ 将条件特征映射到对齐空间；**Dual-Path Sampling**对同一干净图像两次独立加噪。条件对齐在第8层进行时性能最优（FID 11.2，Table 2），表明中层表示在语义一致性和去噪能力之间达到了最佳平衡。

### 创新效果：无外部监督下的显著加速与质量提升

DUPA以无外部视觉编码器的设定，在ImageNet 256×256上取得了FID 1.46（with CFG）和FID 5.92（without CFG）的优异性能，不仅超越了所有不使用外部监督的方法，甚至与依赖大规模预训练编码器的REPA性能相当。更重要的是，DUPA仅需约400个训练epoch即可达到REPA约800个epoch的性能水平，实现了**约5倍训练加速和10倍推理加速**（Figure 3b），同时完全消除了对外部视觉编码器和额外图像数据的依赖。

## 整体框架

![[assets/figures/papers/iclr26_0011_ALpn1nQj5R_Dual-Path_Condition_Alignment_for_Diffusion_Tran/figures/004_Figure_2.jpg]]
*Figure 2: Comparison between REPA and DUPA. REPA needs an external visual encoder to generate effective representations, whereas DUPA can get effective representations through internal alignment*

DUPA（DUal-Path condition Alignment）是一种无需外部视觉编码器的自对齐框架，其核心思路是：对同一张干净图像进行多次独立加噪，通过解耦扩散Transformer提取不同噪声路径的低频条件特征，并强制这些特征彼此对齐，从而为模型提供一致的语义引导。

**Pipeline 总览。** 整个训练流程由四个关键模块串联构成：

1. **双路径采样（Dual-Path Sampling）**：对同一干净图像 $\mathbf{x}_*$ 独立采样两组噪声 $\epsilon_1, \epsilon_2$ 和时间戳 $t_1, t_2$，生成两个噪声隐变量 $\mathbf{x}_{t_1}, \mathbf{x}_{t_2}$。论文设定 $K=2$，在性能和计算开销之间取得平衡（Figure 3a）。
2. **条件编码器（Condition Encoder）**：从每个噪声隐变量中提取低频语义条件特征 $\mathbf{z}_{t_k} = \text{Encoder}(\mathbf{x}_{t_k}, t_k, y)$，其中 $y$ 为类别条件。
3. **速度解码器（Velocity Decoder）**：基于条件特征预测速度场 $\mathbf{v}_{t_k} = \text{Decoder}(\mathbf{x}_{t_k}, t_k, \mathbf{z}_{t_k})$，用于去噪过程。
4. **投影器与对齐损失（Projector & Alignment Loss）**：通过可训练的 MLP 投影器 $z_\phi$ 将两条路径的条件特征映射到对齐空间，最大化其间的余弦相似度：

$$\mathcal{L}_{\mathrm{DUPA}}(\theta, \phi) := - \mathbb{E}_{\mathbf{x}_*, \{\epsilon_k, t_k\}_{k=1}^K} \left[ \frac{2}{K(K-1)} \sum_{1 \leq i < j \leq K} \frac{1}{N} \sum_{n=1}^N \sin(z_\phi(\mathbf{z}_{t_i}^{[n]}), z_\phi(\mathbf{z}_{t_j}^{[n]})) \right]$$

**联合训练目标。** 最终损失函数将速度场预测损失与条件对齐损失相结合：

$$\mathcal{L} := \mathcal{L}_{\mathrm{velocity}} + \lambda \mathcal{L}_{\mathrm{DUPA}}$$

其中 $\lambda$ 控制去噪与对齐之间的权衡。速度场损失为标准 MSE：

$$\mathcal{L}_{\mathrm{velocity}}(\theta) = \mathbb{E}_{\mathbf{x}_*, \epsilon, t} \left[ || \mathbf{v}_\theta(\mathbf{x}_t, t) - \dot{\alpha}_t \mathbf{x}_* - \dot{\sigma}_t \epsilon ||^2 \right]$$

**与 REPA 的关键差异。** Figure 2 清晰展示了两种范式：REPA 依赖外部视觉编码器（如 DINOv2）提供表示监督，存在分布偏移和高计算成本问题；DUPA 则完全通过内部分支对齐实现表示引导，无需任何外部预训练模型或额外图像数据。

**因果机制。** 同一真实图像的不同噪声版本所携带的低频语义信息在理想情况下应保持不变——这是 DUPA 有效性的核心假设。通过对齐这些内部条件，模型在早期层即可获得稳定的语义引导，从而显著加速收敛并提升生成质量。消融实验（Table 4）证实：在 DDT-L/2 基线上，单独添加双路径采样将 FID 从 14.9 降至 12.5，进一步添加条件对齐损失将 FID 降至 11.1，IS 提升至 104.8，验证了两个模块的增量贡献。

## 核心模块与公式推导

### 3.1 预备知识：流匹配与速度场

DUPA建立在连续时间流匹配框架之上。给定干净图像 $\mathbf{x}_*$ 和噪声 $\epsilon$，噪声隐变量通过插值构造：

$$\mathbf{x}_t = \alpha_t \mathbf{x}_* + \sigma_t \epsilon$$

其中 $\alpha_t$ 和 $\sigma_t$ 为时间依赖的噪声调度系数。该过程对应的速度场定义为条件期望的线性组合：

$$\mathbf{v}(\mathbf{x}, t) = \dot{\alpha}_t \mathbb{E}[\mathbf{x}_* | \mathbf{x}_t = \mathbf{x}] + \dot{\sigma}_t \mathbb{E}[\epsilon | \mathbf{x}_t = \mathbf{x}] \tag{2}$$

训练目标是使模型 $\mathbf{v}_\theta$ 预测的速度场逼近真实速度场，采用均方误差损失：

$$\mathcal{L}_{\mathrm{velocity}}(\theta) = \mathbb{E}_{\mathbf{x}_*, \epsilon, t} \left[ \| \mathbf{v}_\theta(\mathbf{x}_t, t) - \dot{\alpha}_t \mathbf{x}_* - \dot{\sigma}_t \epsilon \|^2 \right] \tag{3}$$

在采样阶段，可通过逆向SDE从噪声逐步恢复图像：

$$d \mathbf{x}_t = \mathbf{v}(\mathbf{x}_t, t) dt - \frac{1}{2} w_t \mathbf{s}(\mathbf{x}_t, t) dt + \sqrt{w_t} d \bar{\mathbf{w}}_t \tag{1}$$

### 3.2 解耦扩散Transformer架构

DUPA采用解耦扩散Transformer作为基础架构。该架构将条件编码器与速度解码器分离：条件编码器从噪声隐变量中提取低频语义条件特征 $\mathbf{z}_{t_k}$，速度解码器则基于该条件特征预测速度场：

$$\mathbf{z}_{t_k} = \mathrm{Encoder}(\mathbf{x}_{t_k}, t_k, y) \tag{4}$$

$$\mathbf{v}_{t_k} = \mathrm{Decoder}(\mathbf{x}_{t_k}, t_k, \mathbf{z}_{t_k})$$

其中 $y$ 为类别条件。这种解耦设计使得条件特征 $\mathbf{z}_{t_k}$ 成为可显式操作的中间表示，为后续的双路径对齐提供了操作对象。

### 3.3 双路径采样策略

DUPA的核心创新在于对同一干净图像进行多次独立加噪，构造多路径噪声隐变量。具体而言，对于每张图像 $\mathbf{x}_*$，独立采样 $K$ 组噪声 $\epsilon_k$ 和时间戳 $t_k$，生成 $K$ 个不同的噪声版本：

$$\{ \mathbf{x}_{t_k} = \alpha_{t_k} \mathbf{x}_* + \sigma_{t_k} \epsilon_k \}_{k=1}^K$$

基于性能与计算成本的权衡，DUPA设定 $K=2$。选择 $K=2$ 而非更大值的原因在于：更大的 $K$ 虽然理论上能提供更多样化的条件特征，但会显著增加训练时间和显存占用，而性能增益边际递减。

### 3.4 条件对齐损失

双路径采样的理论动机在于：同一真实图像的不同噪声版本所携带的低频语义信息在理想情况下应保持一致。因此，DUPA通过对齐不同路径的条件特征来提供无监督的表示引导。

具体做法是，将两条路径的条件特征 $\mathbf{z}_{t_1}$ 和 $\mathbf{z}_{t_2}$ 通过可训练的MLP投影器 $z_\phi$ 映射到对齐空间，然后最大化它们之间的余弦相似度。对齐损失定义为：

$$\mathcal{L}_{\mathrm{DUPA}}(\theta, \phi) := - \mathbb{E}_{\mathbf{x}_*, \{\epsilon_k, t_k\}_{k=1}^K} \left[ \frac{2}{K(K-1)} \sum_{1 \leq i < j \leq K} \frac{1}{N} \sum_{n=1}^N \sin(z_\phi(\mathbf{z}_{t_i}^{[n]}), z_\phi(\mathbf{z}_{t_j}^{[n]})) \right] \tag{6}$$

其中 $N$ 为条件特征中的token数量，$\sin(\cdot, \cdot)$ 表示余弦相似度。当 $K=2$ 时，该损失简化为两条路径条件特征之间余弦相似度的负期望。

### 3.5 联合训练目标

最终训练损失为速度场预测损失与条件对齐损失的加权组合：

$$\mathcal{L} := \mathcal{L}_{\mathrm{velocity}} + \lambda \mathcal{L}_{\mathrm{DUPA}} \tag{8}$$

其中 $\lambda$ 为控制去噪任务与表示对齐任务之间权衡的超参数。该联合目标使模型在保持去噪能力的同时，通过内部条件对齐获得有效的语义引导，从而替代了REPA等对外部视觉编码器的依赖。

**关键实现细节**：投影器 $z_\phi$ 的初始化至关重要——必须避免将权重和偏置同时设为零，否则会导致捷径学习，使对齐损失迅速归零而无法提供有效的表示引导。

## 实验与分析

### 核心瓶颈验证

扩散Transformer训练的核心瓶颈在于早期层缺乏准确的低频语义引导，导致收敛缓慢且生成质量受限。REPA等方法通过引入外部视觉编码器（如DINOv2）提供高质量表示引导，但存在两个根本性问题：一是外部编码器与生成模型的**分布偏移**，二是额外编码器的**高计算成本**。

DUPA的核心洞察在于：同一真实图像的不同噪声版本所携带的低频语义信息在理想情况下应该是**不变的**。通过对齐这些内部条件，可以替代外部视觉编码器，实现无监督的高效表示引导。Figure 2 对比了两种范式：REPA依赖外部编码器生成表示，而DUPA通过内部分支对齐实现表示引导。

### 系统级性能对比

Table 1 展示了ImageNet 256×256上的系统级性能对比。DUPA-XL/2在400个训练epoch下取得：


![[assets/figures/papers/iclr26_0011_ALpn1nQj5R_Dual-Path_Condition_Alignment_for_Diffusion_Tran/figures/005_Table_1.jpg]]
*Table 1: System-Level Performance on ImageNet 2 5 6 $\times$ 2 5 6 . Our results are bolded to indicate that DUPA performs better than methods without external supervision of large visual encoders, while highlighted to indicate that DUPA performs the best among all methods. ↓ indicates a lower value is better and ↑ indicates a higher value is better*

- **FID 1.46**（with CFG），相比DDT-XL/2的2.90降低了1.44，且优于所有不依赖外部监督的方法
- **FID 5.92**（without CFG），相比DDT-XL/2的8.57降低了2.65
- **IS 296.2**（with CFG），相比DDT-XL/2的229.8提升了66.4

Figure 1 的散点图进一步揭示：DUPA以约400 epoch达到REPA约800 epoch的性能水平，意味着**≥3倍的收敛加速**。图中圆圈半径表示模型规模，REPA外围的灰色环代表其依赖的辅助视觉编码器——DUPA在完全不需要该编码器的情况下实现了可比的性能。


![[assets/figures/papers/iclr26_0011_ALpn1nQj5R_Dual-Path_Condition_Alignment_for_Diffusion_Tran/figures/003_Figure_1.jpg]]
*Figure 1: Unsupervised representation alignment can efficiently train diffusion transformer as REPA does. By aligning the representations of different noised images, DUPA achieves FID performance comparable to that of REPA with only 400 training epochs, which means ≥ 3× faster convergence than current state-of-the-art methods that do not rely on supervision from an external visual encoder. The radius of the circles in the right figure denotes model size while the gray ring surrounding REPA represents the auxiliary visual encoder*

### 组件分析与消融

Table 2 的组件分析（基于DUPA-L/2，400K迭代）揭示了几个关键设计选择：


![[assets/figures/papers/iclr26_0011_ALpn1nQj5R_Dual-Path_Condition_Alignment_for_Diffusion_Tran/figures/006_Table_2.jpg]]
*Table 2: Component-wise analysis. All models are DUPA-L/2 trained for 400K iterations with different settings. “Resampling” column indicates whether to independently resample timestamp t or noise ϵ*

1. **重采样策略**：独立重采样噪声ε比仅重采样时间戳t更能提升性能（FID 12.4 vs 13.2），表明噪声的多样性对条件对齐更关键。因为不同的ε导致不同的去噪路径，产生更多样化的条件表示，为对齐提供更丰富的学习信号。

2. **对齐深度**：在第8层进行条件对齐时性能最优（FID 11.2）。过浅的层（如第2层）特征尚未充分语义化，过深的层（如第18层）则可能过度拟合去噪任务细节，均不利于低频语义对齐。

3. **相似度函数**：余弦相似度作为对齐目标优于NT-Xent损失，验证了直接最大化特征方向一致性比对比学习框架更适合该任务。

Table 4 的增量消融清晰展示了各组件的贡献链：

![[assets/figures/papers/iclr26_0011_ALpn1nQj5R_Dual-Path_Condition_Alignment_for_Diffusion_Tran/figures/008_Table_4.jpg]]
*Table 4: Ablation study of proposed improvements*

- DDT-L/2基线：FID 14.9，IS 87.8
- +双路径采样：FID降至12.5，IS升至96.6
- +条件对齐损失：FID进一步降至11.1，IS升至104.8

双路径采样是条件对齐的前提——没有独立的噪声路径，对齐操作无法进行。两者协同作用，共同驱动性能提升。

### 模型规模扩展性

Table 3 展示了不同模型规模（B/2、L/2、XL/2）下SiT、DDT与DUPA的性能对比（400K训练步）。DUPA在所有规模上一致优于SiT和DDT，且性能增益随模型规模扩大而增加：DUPA-XL/2取得FID 8.71、sFID 4.65、IS 114.6。这表明条件对齐机制具有良好的可扩展性，更大的模型能更有效地利用内部语义引导。

### 训练效率与推理加速

Figure 3 的计算成本分析揭示了DUPA的效率优势：


![[assets/figures/papers/iclr26_0011_ALpn1nQj5R_Dual-Path_Condition_Alignment_for_Diffusion_Tran/figures/012_Figure_3.jpg]]
*Figure 3: (a) “BS” indicates batch size, “K” indicates noising times, “TS” indicates (b) Image sampling is performed on training speed (sec/step) and “Mem.” indicates memory usage of a single DUPA-XL/2 and DDT-XL/2 trained for GPU (GB). 400K iterations. Figure 3: Time and computational cost analysis. (a) Time and computational costs comparison. (b)Training efficiency and inference speed comparison*

- **训练效率**（Figure 3b）：与DDT相比，DUPA实现了约**5倍训练加速**——在相同训练迭代下，DUPA的生成质量远超DDT
- **推理速度**（Figure 3b）：约**10倍推理加速**，因为更好的低频语义引导使模型在更少的去噪步骤中即可生成高质量图像
- **K值选择**（Figure 3a）：K=2在训练速度与显存开销之间取得最优平衡，进一步增加K值带来的性能增益递减而计算成本线性增长

### 表示质量分析

Figure 4 的判别性语义分析从两个维度验证了DUPA学到的表示质量：

- **线性探测准确率**（Figure 4a）：DUPA-XL/2的峰值准确率达69%，而SiT-XL/2仅为53.5%，证明条件对齐显著提升了特征的语义判别性
- **CKNNA分数**（Figure 4b）：DUPA-XL/2的CKNNA分数始终超过0.4，SiT-XL/2则低于0.2，表明DUPA的特征在最近邻检索任务中具有更强的语义一致性

Figure 5 展示了训练过程中条件对齐余弦相似度的变化曲线，从初始的噪声状态逐步收敛到高相似度，直观呈现了模型从不一致到语义一致的学习过程。

### 无分类器引导强度分析

Table 6 展示了DUPA-XL/2在2M迭代时不同CFG scale w的性能变化。w=1.60时取得最佳FID 1.46；更高的scale虽持续提升IS（从274.6到309.5），但会损害召回率并导致FID反弹。这一现象表明过强的引导会牺牲生成多样性——DUPA采用interval guidance策略，仅在[0, 0.7]区间应用CFG，专注于高频细节生成阶段。

### 局限性与待验证方向

DUPA目前仅在类别条件图像生成（ImageNet 256×256）上进行了系统验证，尚未扩展到文本到图像、视频生成等更复杂的多模态任务。双路径对齐机制是否可推广至非DDT架构的其他扩散模型（如标准DiT），以及条件对齐深度和最优K值在不同规模模型和任务下的自适应选择策略，仍是待探索的开放问题。

## 方法谱系与知识库定位

### 与基线方法的关系

DUPA 的方法论定位处于**无外部监督的表示引导**这一新兴分支，其设计直接回应了 REPA（Yu et al., 2024）的核心瓶颈：REPA 通过外部视觉编码器（如 DINOv2）为扩散 Transformer 提供表示监督，虽能显著加速收敛并提升生成质量，但引入了两个不可忽视的成本——**分布偏移风险**（外部编码器训练数据与生成任务数据分布不一致）和**高昂的计算开销**（需额外加载并运行大规模预训练编码器）。DUPA 的核心创新在于将这一“外部引导”范式转化为“内部自对齐”范式，从而在保持表示引导有效性的同时消除对外部模型的依赖。

具体而言，DUPA 建立在**解耦扩散 Transformer（DDT）**架构之上。DDT 本身是一种无外部监督的基线架构，其将扩散 Transformer 分解为条件编码器（Condition Encoder）和速度解码器（Velocity Decoder），前者负责从噪声隐变量中提取低频语义条件特征 $\mathbf{z}_t$，后者基于该条件预测速度场。DUPA 在 DDT 的基础上进行了两项关键改造：

1. **双路径采样策略**：将 DDT 的单次加噪（$K=1$）改为对同一干净图像独立加噪两次（$K=2$），构造两条噪声路径。这一设计的因果逻辑在于：同一真实图像的不同噪声版本所携带的低频语义信息在理想情况下应是不变的，因此从两条路径提取的条件特征应彼此一致。

2. **条件对齐损失**：在 DDT 的速度场预测损失 $\mathcal{L}_{\mathrm{velocity}}$ 基础上，引入条件对齐损失 $\mathcal{L}_{\mathrm{DUPA}}$，通过可训练的投影器 $z_\phi$ 将两条路径的条件特征映射到对齐空间，最大化其余弦相似度。形式上，总损失为：
   $$\mathcal{L} := \mathcal{L}_{\mathrm{velocity}} + \lambda \mathcal{L}_{\mathrm{DUPA}}$$

与 SiT 和 DiT 等标准扩散 Transformer 基线相比，DUPA 的差异化优势在于：这些基线方法在训练过程中缺乏任何形式的表示引导，导致早期层难以获得准确的低频语义引导，收敛缓慢。DUPA 通过内部条件对齐弥补了这一缺陷，同时避免了 REPA 的外部依赖。

### 适用边界

目前 DUPA 的系统性验证仅限于**类别条件图像生成**任务，具体配置为 ImageNet 256×256 分辨率下的类条件生成。其训练设置使用 8×A100 GPU、batch size 256、Adam 优化器（学习率 0.0001），推理阶段采用 classifier-free guidance，引导区间为 $[0, 0.7]$（仅作用于高频细节生成阶段），最优引导强度 $w=1.60$ 时取得 FID 1.46。

DUPA 的架构设计（双路径采样 + 条件对齐）在原理上不依赖于特定的网络结构或条件类型，但其在以下场景的有效性尚待验证：

- **文本到图像生成**等开放域条件任务，其中条件语义的复杂度和多样性远超类别标签；
- **视频生成**等时序生成任务，其中时间维度的语义一致性可能对条件对齐机制提出新的要求；
- **非 DDT 架构**的标准 DiT 或其他扩散 Transformer 变体，双路径对齐机制是否可平滑迁移仍属开放问题。

### 局限与开放问题

**已确认的局限**：DUPA 目前仅在类别条件图像生成上完成了系统验证，尚未扩展到文本到图像、视频生成等更复杂的多模态任务。这一局限意味着其在更广泛生成场景中的泛化性需要进一步测试。

**开放问题**：

1. **跨任务泛化**：DUPA 在文本到图像等开放域条件生成任务中的表现及进一步优化方向。文本条件的语义稀疏性和组合性可能对“同一图像的不同噪声版本共享低频语义”这一核心假设构成挑战。

2. **架构可迁移性**：双路径对齐机制是否可推广至非 DDT 架构的其他扩散模型（如标准 DiT）。DDT 的解耦设计为条件提取提供了天然接口，而标准 DiT 中条件与去噪过程的耦合方式可能需要重新设计对齐策略。

3. **自适应对齐策略**：条件对齐的最优深度（当前为第 8 层）和最优路径数 $K$（当前为 2）在不同规模模型和不同任务下的自适应选择策略。消融实验表明，对齐深度和 $K$ 值对性能有显著影响，但当前选择主要基于经验调参，缺乏理论指导或自动化机制。

4. **对齐机制的理论理解**：训练过程中条件对齐余弦相似度的变化曲线（Figure 5）展示了从噪声到语义一致性的转变过程，但这一现象背后的动力学机制及其与生成质量提升的因果关联尚未被充分阐释。

5. **与外部监督方法的公平比较**：DUPA 完全无需外部视觉编码器及外部图像数据，与依赖大规模预训练编码器（如 DINOv2）的 REPA 等方法在资源约束上不平等。在相近计算预算下 DUPA 以更少的资源达到了极具竞争力的性能，但若允许 REPA 使用同等计算资源进行更长时间的训练，性能差距是否会缩小尚不明确。

## 原文 PDF

![[paperPDFs/ICLR_2026/Dual_Path_Condition_Alignment_for_Diffusion_Transformers.pdf]]
