---
title: MEGA Masked Generative Autoencoder for Human Mesh Recovery
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/MEGA_Masked_Generative_Autoencoder_for_Human_Mesh_Recovery.pdf
aliases:
- MMGAHMR
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: MEGA 的随机迭代生成策略（基于余弦掩码调度和 Gumbel-max 采样的逐步 token 预测）允许在保持精度的同时产生多样化的预测。
primary_logic: 将人体网格离散化为 token 序列，并采用掩码生成式自编码器进行自监督预训练和条件生成，能够同时实现高精度的确定性预测和可控的随机多样化预测。
claims:
- MEGA 在确定性模式下的 3DPW 和 EMDB 上全面超越先前的最佳方法（包括 VQ-HPS 等）。
- 自监督预训练带来显著提升：丢弃预训练导致 3DPW PVE 增加 2.5 mm，EMDB PVE 增加 6.0 mm。
- 在随机多输出模式下，MEGA 的单次预测已优于概率基线，并且随着样本数量增加性能持续提升。
- 随机模式的平均预测随着 Q 增大收敛到确定性预测，表明确定性模式是对多次采样的良好估计。
---

# MEGA Masked Generative Autoencoder for Human Mesh Recovery

> [!tip] 核心洞察
> 将人体网格离散化为 token 序列，并采用掩码生成式自编码器进行自监督预训练和条件生成，能够同时实现高精度的确定性预测和可控的随机多样化预测。

| 字段 | 内容 |
|------|------|
| 中文题名 | MEGA：面向人体网格恢复的掩码生成式自编码器 |
| 英文题名 | MEGA Masked Generative Autoencoder for Human Mesh Recovery |
| 会议/期刊 | CVPR 2025 |
| Links | [Project](https://gfiche.github.io/research-pages/mega/) · [paper](https://arxiv.org/abs/2405.18839) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MEGA |
| Dataset | 3DPW, EMDB |

> [!tip] 效果简介
> - 3DPW 上，PVE (mm) 81.6 (MEGA HRNet-w48) vs 84.8 (VQ-HPS HRNet-w48) (-3.2)；MPJPE (mm) 68.5 vs 71.1 (-2.6)；PA-MPJPE (mm) 44.1 vs 45.2 (-1.1)。
> - EMDB 上，PVE (mm) 107.9 vs 112.9 (-5.0)；MPJPE (mm) 90.5 vs 99.9 (-9.4)；PA-MPJPE (mm) 58.7 vs 65.2 (-6.5)。
> - 3DPW (stochastic, best of 25 samples) 上，MPJPE (mm) 73.9 (MEGA ResNet-50) vs 84.0 (ProHMR) (-10.1)。

## 概述

从单张图像恢复三维人体网格是一个病态问题，其根本瓶颈在于**深度歧义**：同一二维观测可对应多种合理的三维姿态，而现有方法往往在预测多样性与精度之间难以兼得。MEGA（Masked Generative Autoencoder）针对这一矛盾提出了一种基于掩码生成建模的解决方案，其核心思路是将人体网格离散化为 token 序列，并采用编码器-解码器 Transformer 架构进行掩码预测，从而在单一框架内同时支持高精度的确定性预测与可控的随机多样化预测。

MEGA 的关键设计包括三个层面。在**表示层**，通过冻结的 Mesh-VQ-VAE 将规范空间下的人体网格编码为 54 个离散 token，将连续几何生成转化为分类问题。在**训练层**，首先在大规模动作捕捉数据上进行自监督预训练——模型仅从部分可见的 token 重建完整网格序列，无需任何图像条件；随后在图像-网格对上以随机掩码条件生成的方式进行监督微调。在**推理层**，确定性模式一次前向传播预测全部 token，随机模式则从全掩码序列出发，通过迭代采样逐步生成 token，采样过程中的噪声温度随步数衰减以控制多样性。

实验证据表明上述设计带来了显著增益。在确定性模式下，MEGA 在 3DPW 和 EMDB 两个主流野外基准上全面超越此前最优方法：以 HRNet-w48 为骨干，3DPW 上的 PVE 达到 81.6 mm（对比 VQ-HPS 的 84.8 mm），EMDB 上的 MPJPE 达到 90.5 mm（对比 VQ-HPS 的 99.9 mm）。消融实验进一步揭示，**自监督预训练是性能提升的关键驱动因素**——移除预训练后，3DPW PVE 增加 2.5 mm，EMDB PVE 增加 6.0 mm。在随机多输出模式下，MEGA 的单次预测已优于概率基线 ProHMR，且随着采样数增加性能持续提升：在 25 次采样下，MPJPE 从 86.2 mm 降至 73.9 mm，相对 ProHMR 的改进幅度超过 10%。此外，随机模式的平均预测随采样数增大收敛至确定性预测，表明确定性模式是对多次采样的良好估计。

在方法谱系中，MEGA 相对于现有工作完成了若干关键转变：将训练范式从纯监督回归/分类拓展为“自监督预训练 + 掩码条件生成”；将推理模式从单次确定性输出拓展为确定性/随机双模式；将输入表示从图像到姿态参数的直接映射转变为图像到离散 token 序列的条件生成；并将预训练数据的利用从仅限于 2D 特征提取器拓展到直接在三维网格 token 上进行掩码重建。这些转变使 MEGA 在精度-多样性权衡上取得了新的最优平衡点。

需要指出的是，MEGA 对极端姿态的泛化仍存在局限——当输入姿态与训练分布差异较大时，模型会产生高多样性但误差较大的预测（Fig. 9），这提示了不确定性估计在实际部署中的重要性。此外，模型不重建面部细节，在一定程度上限制了其在需要面部信息的应用中的适用性。

## 背景与动机

从单张 RGB 图像恢复三维人体网格（Human Mesh Recovery, HMR）是计算机视觉中的基础任务，在动作捕捉、虚拟现实、人机交互等领域有广泛应用。然而，该任务本质上是一个病态问题：二维图像中蕴含的深度信息不足，导致同一张图像可能对应多个在二维投影上看似合理、但在三维空间中差异显著的人体姿态（Figure 1）。这种深度歧义构成了单图像 HMR 的核心瓶颈。

现有方法大致分为两类。一类是确定性单输出方法，如 **FastMETRO**、**PARE**、**CLIFF**、**HMR2.0** 等，它们直接从图像回归到单一的三维网格或 SMPL 参数，追求预测精度，但无法表达预测的不确定性，在面对遮挡或歧义场景时缺乏鲁棒性。另一类是概率多输出方法，如基于正态化流的 **ProHMR**、基于扩散模型的 **Diff-HMR**、以及基于评分假设的 **ScoreHypo** 等，它们试图通过生成多个候选姿态来覆盖歧义空间。然而，这些方法往往面临精度与多样性之间的权衡：增加多样性通常以牺牲单个预测的准确性为代价，导致即便采样多个输出，其最佳预测的精度仍不及确定性方法。

**VQ-HPS** 是近期一项与 MEGA 最相关的工作，它首次将人体网格离散化为 token 序列，并将 HMR 形式化为分类任务——预测每个 token 的类别索引。这一范式避免了直接回归连续姿态参数时的不稳定问题，但 VQ-HPS 仍然是一个单输出方法，且其训练仅依赖图像-网格对，未能充分利用大规模无图像标注的动作捕捉数据。

MEGA 的提出正是为了解决上述困境：**能否在保持高精度确定性预测的同时，赋予模型可控的随机生成能力，从而在单一框架内同时应对精度需求和深度歧义？** 这一动机催生了三个关键设计方向：（1）将人体网格完全离散化为 token 序列，使 HMR 转化为生成式建模问题；（2）引入自监督掩码预训练，在不依赖图像的情况下从动作捕捉数据中学习人体网格的先验分布；（3）设计统一的掩码条件生成框架，在推理时既能单次前向传播完成确定性预测，又能通过迭代采样产生多样化输出。

## 核心创新

MEGA 的核心创新在于将人体网格恢复（HMR）重新定义为一种**掩码生成式建模**问题，并通过三个关键的技术转变，突破了现有方法在精度与多样性之间的固有矛盾。

### 1. 范式转移：从回归/分类到掩码生成
传统 HMR 方法（如 **HMR2.0**、**CLIFF**、**PARE** 等参数化方法，以及 **FastMETRO**、**Virtual Marker** 等非参数化方法）将任务视为从图像到姿态参数或 3D 顶点的直接映射，采用全监督回归范式。与 MEGA 最相关的 **VQ-HPS** 虽引入了离散 token 表示，但仍采用分类式训练。MEGA 的突破在于采用**掩码生成式自编码器**框架：训练时随机掩码部分网格 token，要求模型从可见 token 和图像条件中预测被掩码的部分。这一范式转变使模型能够学习人体网格 token 之间的内在依赖关系，而非简单的输入-输出映射。

### 2. 训练策略创新：自监督预训练 + 条件微调
MEGA 引入了一个此前在 HMR 领域未被充分利用的训练策略——**在无图像条件下进行大规模自监督预训练**。具体而言：
- **预训练阶段**：仅使用动作捕捉数据（无需配对图像），在人体网格 token 上执行掩码重建任务。掩码比例 $M = \lfloor N \cos(\frac{\pi \tau}{2}) \rfloor$（$\tau \in [0,1)$ 均匀采样），采用余弦调度以控制训练难度。
- **微调阶段**：在图像-网格对数据上进行条件掩码生成训练，图像特征作为条件信息。

消融实验（Table 1）提供了强有力证据：丢弃自监督预训练导致 3DPW 上 PVE 增加 2.5 mm，EMDB 上增加 6.0 mm，验证了无图像预训练对模型学习人体网格先验知识的关键作用。

### 3. 推理模式创新：统一确定性与随机生成
MEGA 在同一框架下支持两种推理模式，这是现有方法无法实现的：
- **确定性模式**：单次前向传播，解码器输入全掩码序列，仅依赖图像条件预测所有 token（取 argmax），实现高精度单输出预测。
- **随机模式**：从全掩码序列开始，迭代采样 token。第 $t$ 步前已预测的 token 数量为 $n_t = \lfloor N \times (1 - \cos(\frac{\pi t}{2T})) \rfloor$，配合温度调度 $A \times (1 - \frac{t}{T})$ 控制随机性。这种渐进式生成策略允许模型在保持合理性的同时产生多样化输出。

Table 3 和 Table 4 的证据表明，随机模式的单次预测（Q=1）已优于概率基线（如 **ProHMR**），且随着采样数增加性能持续提升；同时，随机模式的平均预测收敛到确定性预测，证明确定性模式是对多次采样的良好估计。

### 4. 输入表示创新：端到端的离散 Token 化
MEGA 依赖冻结的 **Mesh-VQ-VAE** 将规范空间人体网格编码为 $N=54$ 个离散 token（码本大小 $S=512$，隐维度 $L=9$），将连续几何重建问题转化为离散序列生成问题。这一表示选择使得掩码生成式建模（类似 NLP 中的 BERT）能够直接应用于 3D 网格，同时保持解码器可微性。

### 创新总结

| 创新维度 | 基线方法 | MEGA 方案 | 证据强度 |
|---------|---------|----------|---------|
| 训练范式 | 全监督回归/分类 | 自监督预训练 + 掩码条件生成 | 强（消融实验 PVE 差异 2.5-6.0 mm） |
| 推理模式 | 单次确定性预测 | 确定性/随机双模式统一 | 强（Table 1/3/4 全面验证） |
| 输入表示 | 图像到参数/顶点的直接映射 | 图像到离散 token 序列生成 | 强（架构依赖 Mesh-VQ-VAE 编码） |
| 预训练数据利用 | 通常不使用或仅 2D 预训练 | 直接在网格 token 上自监督预训练 | 强（Table 1 消融证实关键作用） |

这些创新共同构成了 MEGA 的核心贡献：通过掩码生成式建模统一了精度与多样性，在确定性模式下达到 SOTA 精度（3DPW PVE 81.6 mm，EMDB PVE 107.9 mm），在随机模式下提供可控的多样化预测。

## 整体框架

MEGA 是一个基于编码器-解码器 Transformer 架构的掩码生成式自编码器，其核心思想是将人体网格恢复转化为离散 token 序列的条件生成问题。整体 pipeline 由三个关键阶段串联而成：**网格 token 化 → 条件生成 → 网格解码**。

### 输入输出流

给定单张 RGB 图像，MEGA 首先通过冻结的图像特征提取器（HRNet 或 ViT）提取空间特征图，作为后续生成过程的条件信息。与此同时，人体网格被离散化为固定长度的 token 序列——这一过程由预训练且冻结的 Mesh-VQ-VAE 完成：规范姿态下的人体网格被编码为 $N=54$ 个离散 token 索引，每个 token 来自大小为 $S=512$ 的码本，隐空间维度 $L=9$。

在推理阶段，MEGA 支持两种互补的工作模式：

- **确定性模式**：解码器接收 $N$ 个全掩码 token 和图像嵌入，在单次前向传播中通过 argmax 直接预测全部 token 序列，编码器在此模式下不被使用。
- **随机模式**：从全掩码序列出发，按余弦调度 $n_t = \lfloor N \times (1 - \cos(\frac{\pi t}{2T})) \rfloor$ 逐步确定已预测 token 数量，结合 Gumbel-max 采样和噪声温度调度 $A \times (1 - \frac{t}{T})$ 迭代生成 token 序列，实现可控的多样化预测。

最终，预测的 token 序列被送入 Mesh-VQ-VAE 解码器，重构出完整的人体网格；同时，平均图像特征经过一个两层 MLP 预测全局 6D 旋转和透视相机参数，将规范网格变换到相机空间。

### 模块关系与训练流程

MEGA 的训练分为两个阶段，共享同一 Transformer 架构（12 层编码器 + 4 层解码器）：

1. **自监督预训练阶段**：仅使用动作捕捉数据（无配对图像），对网格 token 序列进行掩码重建。掩码数量 $M$ 按余弦调度 $M = \lfloor N \cos(\frac{\pi \tau}{2}) \rfloor$（$\tau \sim \mathcal{U}[0,1)$）随机确定，模型需从部分可见 token 预测被掩码的 token。此阶段使 MEGA 学习到人体网格的先验分布，是后续监督训练性能提升的关键——消融实验表明，丢弃预训练会导致 3DPW 上 PVE 增加 2.5 mm，EMDB 上增加 6.0 mm。

2. **监督 HMR 训练阶段**：在预训练权重基础上，模型以图像嵌入为条件，对随机掩码的网格 token 进行预测。训练仅使用交叉熵损失监督被掩码位置的 token 预测，掩码调度与预训练阶段保持一致。

值得注意的是，Mesh-VQ-VAE 在整个流程中保持冻结，仅作为 token 编解码的确定性桥梁，MEGA 本身不直接操作连续网格顶点，而是完全在离散 token 空间中进行生成建模。这种设计将生成任务从高维连续空间压缩到低维离散空间，既降低了学习难度，也为自监督预训练和随机采样提供了天然的概率框架。

### 补充图表

![[assets/figures/papers/paper_list_l19_MEGA_Masked_Generative_Autoencoder_for_Human_Mesh_Recovery_motion20v2/figures/001_Figure_1.jpg]]
*Figure 1: Human mesh recovery from a single image is an ill-posed problem due to depth ambiguity. Probabilistic approaches have aimed to address this by generating multiple predictions, but diversity often sacrifices accuracy. Introducing MEGA, our HMR model based on masked generative modeling achieves state-of-the-art performance on in-the-wild benchmarks in single- and multi-output settings. Given a single image, MEGA can make predictions that all look accurate given the 2D cues but correspond to diverse 3D interpretations*

![[assets/figures/papers/paper_list_l19_MEGA_Masked_Generative_Autoencoder_for_Human_Mesh_Recovery_motion20v2/figures/002_Figure_2.jpg]]
*Figure 2: MEGA is a masked generative model based on an encoder-decoder Transformer architecture. During the self-supervised pretraining stage, MEGA is trained to predict human mesh tokens from partially visible inputs using motion capture data without paired image data. During the supervised training stage for HMR, the model is trained to predict randomly masked human mesh tokens conditioned on image embeddings. For both training stages, only the cross-entropy loss is used on the predicted mesh tokens. At test time, in stochastic inference mode, we start from a fully masked sequence of tokens and iteratively sample human mesh tokens conditioned on input image embeddings. In deterministic inference m...*

## 核心模块与公式推导

MEGA 的核心架构围绕“离散 token 序列的条件生成”展开，由三个关键模块串联构成：**Mesh-VQ-VAE** 提供网格的离散 token 表示，**图像特征提取器** 提供条件信息，**编码器-解码器 Transformer** 执行掩码生成建模。以下逐一解析其设计逻辑与关键公式。

---

### 3.1 Mesh-VQ-VAE：规范网格的离散化

MEGA 不直接回归 3D 顶点坐标，而是利用预训练且冻结的 Mesh-VQ-VAE 将人体网格转换为离散 token 序列。其工作流程为：

1. **编码**：输入规范姿态下的人体网格，经编码器得到 $N = 54$ 个 latent 向量，每个维度 $L = 9$。
2. **量化**：将每个 latent 向量映射到大小为 $S = 512$ 的 codebook 中最近邻的索引，形成 54 个离散 token 索引。
3. **解码**：从 token 索引序列通过 codebook 查表恢复 latent 向量，经解码器重构出规范网格。

这一离散化是 MEGA 将 HMR 转化为序列生成问题的关键前提——模型只需预测 54 个 token 索引，而非直接输出高维顶点。

---

### 3.2 编码器-解码器 Transformer 架构

MEGA 的主体是一个编码器-解码器 Transformer（Figure 2），包含以下子模块：

| 模块 | 规格 | 功能 |
|------|------|------|
| **图像特征提取器** | HRNet-w48 或 ViT-H | 从输入 RGB 图像提取 $W \times H \times C$ 空间特征图，作为条件信息 |
| **MEGA Encoder** | 12 层 Transformer | 处理可见的网格 token 嵌入，产生编码表示 |
| **MEGA Decoder** | 4 层 Transformer | 结合编码 token 嵌入、掩码 token 和图像嵌入（通过 cross-attention），预测所有 token 的概率分布 |
| **旋转/相机预测头** | 2 层 MLP | 将平均图像特征线性映射为全局 6D 旋转和透视相机参数 |

**关键设计**：图像特征通过 cross-attention 注入 decoder，而非在 encoder 中融合。在确定性推理模式下，encoder 完全不被使用——decoder 直接接收 $N$ 个全掩码 token 和图像嵌入，单次前向传播完成全部 token 预测。

---

### 3.3 掩码调度：余弦掩码率

MEGA 的训练（包括自监督预训练和监督微调）均采用**可变掩码率**策略，而非固定比例。其核心公式为：

$$M = \lfloor N \cos(\frac{\pi \tau}{2}) \rfloor$$

其中：
- $M$：当前训练步被掩码的 token 数量
- $N = 54$：token 序列总长度
- $\tau \sim \mathcal{U}[0, 1)$：从均匀分布随机采样

该余弦调度使得掩码率在 $[0, N]$ 范围内平滑变化，模型在训练中见过从“几乎全可见”到“几乎全掩码”的各种情况。消融实验（Table 1）证实：线性掩码调度（$M = \lfloor N \tau \rfloor$）在 3DPW 上 PVE 升至 86.5 mm（vs 余弦的 81.6 mm），验证了余弦调度的优越性。

**自监督预训练**阶段仅使用动作捕捉数据（无图像），MEGA 学习从部分可见 token 重建完整网格 token 序列，损失函数仅为预测 token 上的交叉熵。

---

### 3.4 双模式推理公式

MEGA 支持两种推理模式，其差异体现在 token 预测策略上：

**确定性模式**：单次前向传播，对所有 $N$ 个位置取 argmax 得到 token 索引，一步完成预测。无需迭代，速度最快。

**随机模式**：从全掩码序列开始，分 $T$ 步迭代生成。第 $t$ 步之前已预测的 token 总数由下式控制：

$$n_t = \lfloor N \times (1 - \cos(\frac{\pi t}{2T})) \rfloor$$

每一步根据当前预测分布进行 Gumbel-max 采样，采样温度随步数递减：

$$A \times (1 - \frac{t}{T})$$

其中 $A$ 为初始温度（HMR 任务中 $A$ 取较小值以平衡多样性与精度）。无条件随机网格生成时，温度调度采用六次方 $(A \times (1 - t/T))^6$，以在生成初期保留更大随机性。

**收敛性**：Table 4 显示，随着采样数 $Q$ 从 1 增至 100，随机模式的平均预测与确定性预测的距离从 14.78 mm 降至 7.61 mm，表明确定性输出是多次采样的良好估计。

---

### 3.5 损失函数

整个训练流程（自监督预训练 + 监督 HMR 训练）仅使用**交叉熵损失**作用于被预测的网格 token 上，外加旋转和相机参数的监督损失。这种简洁的损失设计得益于将连续网格重建问题完全委托给冻结的 Mesh-VQ-VAE，MEGA 只需专注 token 分类。

### 补充图表

![[assets/figures/papers/paper_list_l19_MEGA_Masked_Generative_Autoencoder_for_Human_Mesh_Recovery_motion20v2/figures/003_Figure_3.jpg]]
*Figure 3: Prediction process iterations. We visualize the predictions for intermediate steps in stochastic mode. All masked tokens are replaced by the first token of the codebook, corresponding to index 0*

![[assets/figures/papers/paper_list_l19_MEGA_Masked_Generative_Autoencoder_for_Human_Mesh_Recovery_motion20v2/figures/010_Figure_6.jpg]]
*Figure 6: Random mesh generations. We use MEGA pre-trained in a self-supervised fashion to generate random human meshes*

## 实验与分析

### 确定性模式下的主结果

MEGA 在确定性推理模式下（单次前向传播，取所有 token 预测分布的 argmax）于 3DPW 和 EMDB 两个主流 in-the-wild 基准上全面超越现有方法。与最相关的离散 token 基线 **VQ-HPS** 相比，MEGA 使用相同 HRNet-w48 骨干时，在 3DPW 上的 PVE 降低 3.2 mm（81.6 vs 84.8），MPJPE 降低 2.6 mm（68.5 vs 71.1）；在更具挑战性的 EMDB 上优势更为显著，PVE 降低 5.0 mm（107.9 vs 112.9），MPJPE 降低 9.4 mm（90.5 vs 99.9）。当骨干网络升级为 ViT-H 时，MEGA 在 3DPW 上的 PA-MPJPE 进一步降至 41.0 mm，PVE 降至 80.0 mm，验证了该方法对更强特征提取器的兼容性。详见 **Table 1**。

![[assets/figures/papers/paper_list_l19_MEGA_Masked_Generative_Autoencoder_for_Human_Mesh_Recovery_motion20v2/figures/004_Table_1.jpg]]
*Table 1: Evaluation in deterministic mode. We evaluate MEGA on the 3DPW and EMDB datasets and compare it to the SOTA methods using metrics defined in Sec. 4.1 given in mm. † stands for additionally using 2D training data, and ∓ for additionally using 2D data and BEDLAM [7]. Methods in italic below the row ”MEGA” indicate the results of the ablation study*

值得注意的是，MEGA 在 3DPW-OCC 遮挡数据集上也表现出较强的鲁棒性（**Table 2**），表明掩码生成框架天然具备处理部分观测的能力，即使训练阶段并未针对遮挡做专门设计。

![[assets/figures/papers/paper_list_l19_MEGA_Masked_Generative_Autoencoder_for_Human_Mesh_Recovery_motion20v2/figures/005_Table_2.jpg]]
*Table 2: Evaluation on 3DPW-OCC. We evaluate MEGA on an occlusion dataset and compare it to SOTA HMR methods designed to handle occlusions using standard metrics (see Sec. 4.1) in mm. Methods in the top part use a ResNet-50 backbone, while others use HRNet*

### 消融实验：预训练与掩码策略

**Table 1** 下半部分的消融实验揭示了三个关键设计选择的影响：

1. **自监督预训练至关重要**：丢弃预训练（w/o pre-training + full mask）导致 3DPW PVE 从 81.6 mm 升至 84.1 mm（+2.5 mm），EMDB PVE 从 107.9 mm 升至 113.9 mm（+6.0 mm）。EMDB 上的退化幅度更大，说明预训练在分布外场景下的收益尤为突出。预训练仅使用动作捕捉数据，无需配对图像，通过重建部分可见的网格 token 使模型习得人体形态的先验。

2. **余弦掩码调度优于线性掩码**：将余弦调度 $M = \lfloor N \cos(\frac{\pi \tau}{2}) \rfloor$ 替换为线性调度 $M = \lfloor N \tau \rfloor$ 后，3DPW PVE 从 81.6 mm 升至 86.5 mm（+4.9 mm）。余弦调度在低掩码率区域采样更频繁，使模型更多地在“少量 token 可见”的困难条件下训练，从而提升了推理时从全掩码状态恢复的能力。

3. **监督训练阶段保持与预训练一致的掩码策略更优**：在 HMR 监督训练中使用 100% 掩码（full mask）虽然逻辑上与确定性推理模式（全掩码输入）对齐，但 3DPW PVE 轻微升至 81.8 mm，EMDB 表现更差。这表明保持余弦调度的可变掩码率，使训练与预训练分布一致，有助于保留预训练学到的先验。

### 随机模式下的多输出评估

**Table 3** 展示了随机模式在 3DPW 上的多输出 HMR 评估。MEGA 的单次随机预测（Q=1）已在 MPJPE（86.2 mm）上优于所有概率基线，包括 **ProHMR**（97.0 mm）、**Diff-HMR**（89.2 mm）和 **3D Multibodies**（89.3 mm）。随着采样数量 Q 增加，性能持续提升：Q=25 时 MPJPE 降至 73.9 mm，相对 ProHMR 的最佳 25 样本结果（84.0 mm）提升 12.0%。在 PA-MPJPE 上，MEGA 从 Q=1 的 54.7 mm 降至 Q=25 的 47.6 mm。

这一结果说明 MEGA 的迭代生成策略（基于余弦进度 $n_t = \lfloor N \times (1 - \cos(\frac{\pi t}{2T})) \rfloor$ 和 Gumbel-max 采样）能有效探索合理的 3D 解释空间，且单次采样质量已具竞争力。**Figure 4** 的定性样本进一步展示了在遮挡输入下，MEGA 能生成多个视觉上合理且 3D 结构各异的人体姿态。

![[assets/figures/papers/paper_list_l19_MEGA_Masked_Generative_Autoencoder_for_Human_Mesh_Recovery_motion20v2/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative samples. Given a single image with occlusions, MEGA makes diverse plausible predictions*

### 随机模式向确定性模式的收敛

**Table 4** 定量分析了随机模式平均预测与确定性预测的距离。当 Q=1 时，平均网格与确定性预测的 PVE 距离为 14.78 mm；随着 Q 增大，距离单调递减，Q=100 时降至 7.61 mm。预测的标准差也从 Q=1 的 9.65 mm 收敛到 Q=100 的 7.34 mm。**Figure 5** 的误差分布可视化进一步佐证：随着采样数增加，平均误差和最小误差的分布均逐渐向确定性误差靠拢。

这表明 MEGA 的确定性模式本质上是对多次随机采样的良好估计——在单次前向传播中取 argmax 即可逼近大量采样的期望输出，为实际部署提供了高效的选择。

### 失败模式与不确定性

**Figure 9** 展示了 MEGA 的典型失败案例：对于训练数据分布中罕见的极端姿态，模型预测出现较大误差，同时随机模式产生高度多样化的输出。这种高多样性可被解释为模型对自身预测的高不确定性——一个有用的自诊断信号。**Figure 8** 通过顶点位置标准差的可视化进一步支持这一观察：困难样本上网格的四肢末端呈现红色（高标准差），而躯干等稳定区域呈蓝色（低标准差）。

此外，尽管 MEGA 采用非参数 token 表示，重构的网格在极端样本上偶尔仍不符合人体形态学约束。模型不重建面部细节也限制了其在需要面部信息的应用场景中的使用。

### 补充图表

![[assets/figures/papers/paper_list_l19_MEGA_Masked_Generative_Autoencoder_for_Human_Mesh_Recovery_motion20v2/figures/006_Table_3.jpg]]
*Table 3: Evaluation in stochastic mode. We compare MEGA to the SOTA probabilistic methods on the multi-output HMR task using standard metrics (see Sec. 4.1) given in mm and the relative improvement (Imp) in %. ‡ uses an HRNet backbone; all other methods use a ResNet-50 backbone*

![[assets/figures/papers/paper_list_l19_MEGA_Masked_Generative_Autoencoder_for_Human_Mesh_Recovery_motion20v2/figures/008_Table_4.jpg]]
*Table 4: Comparison between deterministic and stochastic generation modes. In stochastic mode, we evaluate the mean mesh obtained with different sample sizes on 10% of the 3DPW [84] dataset, and we provide its distance to the deterministic prediction (Dist. to det.). We also report the standard deviation of the predictions. All metrics are in mm*

![[assets/figures/papers/paper_list_l19_MEGA_Masked_Generative_Autoencoder_for_Human_Mesh_Recovery_motion20v2/figures/012_Figure_8.jpg]]
*Figure 8: Visualization of the predictions diversity. We visualize the standard deviation of the 3D location of each vertex. Bluish regions in the mesh indicate low standard deviation, while reddish areas signify higher standard deviation*

![[assets/figures/papers/paper_list_l19_MEGA_Masked_Generative_Autoencoder_for_Human_Mesh_Recovery_motion20v2/figures/013_Figure_9.jpg]]
*Figure 9: Failure cases. In failure cases, it is worth noting that our model predicts very diverse results, which can be interpreted as high uncertainty*

![[assets/figures/papers/paper_list_l19_MEGA_Masked_Generative_Autoencoder_for_Human_Mesh_Recovery_motion20v2/figures/009_Figure_5.jpg]]
*Figure 5: Error distribution. We visualize the distribution of the MPJPE in mm on the 3DPW dataset*

## 方法谱系与知识库定位

### 1. 任务定位与核心瓶颈

MEGA 聚焦于单图像人体网格恢复（HMR）中的根本性挑战：深度歧义导致的不适定性。单张 RGB 图像缺乏显式深度信息，使得同一二维投影可以对应多个不同的三维人体姿态，而现有方法难以在预测多样性与精度之间取得平衡——确定性方法只输出单一解，概率方法虽能产生多样化解却常以精度为代价（Figure 1）。

MEGA 的核心洞察在于将人体网格离散化为 token 序列，并采用掩码生成式自编码器框架进行自监督预训练和条件生成，从而同时实现高精度的确定性预测与可控的随机多样化预测。这一设计使 MEGA 在单输出和多输出两种模式下均达到最优性能。

### 2. 与现有方法的谱系关系

#### 2.1 单输出确定性 HMR 方法

传统的单输出 HMR 方法可大致分为参数化和非参数化两类。参数化方法直接回归 SMPL 模型参数（如 **PARE**、**CLIFF**、**HMR2.0**），非参数化方法则直接预测三维顶点位置（如 **FastMETRO**、**Virtual Marker**）。这些方法均采用单次前向传播产生确定性预测，无法建模深度歧义带来的多模态性。

**VQ-HPS** 和 **TokenHMR** 是与 MEGA 最相关的确定性方法，它们同样引入了离散 token 表示。VQ-HPS 将人体网格 token 的分类视为纯分类任务，TokenHMR 则使用姿态 token 进行回归。MEGA 在此基础上做了关键范式转换：将分类/回归任务重新定义为条件生成任务，并引入自监督预训练阶段。这一转变带来的性能提升在 Table 1 中得到验证——MEGA HRNet-w48 在 3DPW 上 PVE 为 81.6 mm，较 VQ-HPS 的 84.8 mm 降低 3.2 mm；在更具挑战性的 EMDB 上，MPJPE 从 99.9 mm 降至 90.5 mm，降幅达 9.4 mm。

#### 2.2 多输出概率 HMR 方法

在概率建模方面，先前工作主要基于两类框架：基于正态化流的方法（**ProHMR**、**3D Multibodies**）和基于扩散/评分模型的方法（**Diff-HMR**、**ScoreHypo**）。这些方法从图像条件中采样潜在变量，再解码为人体网格，本质上是在连续空间中进行采样。

MEGA 在随机模式下采用完全不同的生成策略：基于余弦掩码调度的迭代 token 预测。每一步根据当前已预测的 token 和图像条件，通过 Gumbel-max 采样逐步填充剩余的掩码 token。这一离散迭代生成过程天然适合建模人体姿态的组合结构。Table 3 显示，MEGA ResNet-50 的单次预测（Q=1）MPJPE 已达 86.2 mm，优于 ProHMR 的 97.0 mm；当采样 25 次取最优时，MPJPE 进一步降至 73.9 mm，而 ProHMR 仅为 84.0 mm，相对提升 10.1 mm。

#### 2.3 自监督预训练范式的差异

MEGA 的方法论创新中最具区分度的是其自监督预训练策略。与仅在 ImageNet 等二维任务上预训练特征提取器的常见做法不同，MEGA 直接在人体网格 token 上进行掩码重建预训练，无需任何配对图像数据。这一设计充分利用了大规模动作捕捉数据集，使模型在接触图像条件之前就学会人体网格的内在结构和运动先验。

消融实验（Table 1）有力地证明了这一策略的价值：丢弃预训练后，3DPW PVE 从 81.6 mm 增至 84.1 mm（+2.5 mm），EMDB PVE 从 107.9 mm 增至 113.9 mm（+6.0 mm），表明预训练在分布外场景下的增益更为显著。

### 3. 方法谱系中的关键变化槽位

| 变化槽位 | 基线方法取值 | MEGA 取值 | 证据锚点 |
|---------|------------|----------|---------|
| 训练范式 | 全监督回归或分类（仅图像-网格对） | 自监督预训练（动作捕捉）+ 掩码条件生成训练 | Section 3.3, Table 1 |
| 推理模式 | 单次前向传播确定预测 | 支持确定性单次预测和随机迭代采样多预测 | Section 3.4 |
| 输入表示 | 图像到姿态参数或 3D 顶点的直接映射 | 图像到离散网格 token 序列的生成，需通过 Mesh-VQ-VAE 编解码 | Section 3.1 |
| 预训练数据利用 | 通常不使用或仅在特征提取器上预训练（2D 任务） | 直接在人体网格 token 上进行自监督掩码重建预训练，无需图像 | Section 3.3, Table 1 ablation |

### 4. 适用边界与局限性

尽管 MEGA 在多个基准上表现优异，其适用边界仍有明确限制：

1. **极端姿态泛化不足**：对于与训练数据分布差异较大的极端姿态，模型预测容易出现较大误差，并呈现高度不确定性。Figure 9 的失败案例分析表明，此时模型会产生非常多样化的预测，可被解释为高不确定性信号，但预测质量本身下降明显。

2. **网格形态保真度限制**：虽然采用非参数 token 表示避免了对 SMPL 参数空间的依赖，但重构出的网格偶尔仍可能不符合人体形态，尤其在困难样本上。这一限制源于 Mesh-VQ-VAE 的离散化编码能力边界。

3. **面部细节缺失**：模型不重建面部细节，一定程度限制了在需要面部信息的应用中使用。

4. **数据依赖性**：自监督预训练阶段依赖大规模动作捕捉数据，在动作捕捉数据稀缺的领域（如特殊运动类型）可能无法充分发挥优势。

### 5. 开放问题

1. **极端姿态泛化**：如何进一步将对极端姿态的泛化能力融入训练（例如增加相应数据或改进模型架构）？

2. **时序扩展**：能否将 MEGA 扩展到视频输入，通过时间维度的掩码建模来提高序列预测的一致性和准确性？

3. **多模态条件生成**：MEGA 的生成框架是否适用于文本或其它模态条件（如文本描述、多人交互 token）？

4. **生成策略进化**：离散扩散模型等新技术能否替代当前的迭代采样，进一步提升生成质量和速度？

5. **不确定性驱动的自适应选择**：如何根据不确定性（如顶点方差，Figure 8）自动选择最佳预测，以在实际应用中平衡精度和多样性？

6. **端到端训练**：当前 Mesh-VQ-VAE 是冻结的，端到端微调整个 pipeline 是否能进一步提升重构质量？

## 原文 PDF

![[paperPDFs/CVPR_2025/MEGA_Masked_Generative_Autoencoder_for_Human_Mesh_Recovery.pdf]]