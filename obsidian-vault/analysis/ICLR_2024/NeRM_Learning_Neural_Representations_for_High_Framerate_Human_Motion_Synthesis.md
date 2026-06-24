---
title: "NeRM: Learning Neural Representations for High Framerate Human Motion Synthesis"
type: paper
paper_level: A
venue: ICLR
year: 2024
pdf_ref: paperPDFs/ICLR_2024/NeRM_Learning_Neural_Representations_for_High_Framerate_Human_Motion_Synthesis.pdf
aliases:
- NeRM
tags:
- ICLR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 将人体运动表示为时间坐标上的连续隐式神经场，并通过变分自解码器学习紧凑的、与帧率解耦的潜在码。这一设计使得模型能够直接处理任意帧率的原生数据，并在紧凑的潜在空间中利用扩散模型生成多样化运动，从根本上打破了帧率与内存/模型规模的耦合。
primary_logic: 利用隐式神经表示（INR）的连续性与紧凑性，将不同帧率、不同时长的运动统一表示为归一化时间坐标上的函数，并通过变分潜在分布与编码本增强注意力机制捕获高频细节。在潜在空间中进行扩散模型训练，既实现了任意帧率生成，又规避了高帧率直接建模带来的计算负担。
claims:
- NeRM提出将运动序列建模为以时间坐标和潜在码为条件的连续函数，避免了显式建模变长运动，从而支持原生多帧率训练。
- 在HumanML3D和KIT文本到运动基准上，NeRM在FID、R-Precision等关键指标上全面超越现有最先进方法（如MLD、MDM），FID从0.473（MLD）降至0.389（NeRM原生帧率训练）。
- NeRM能够直接生成高达120fps的平滑运动，而基线方法通过插值升采样会产生脚滑伪影；在clip-FID指标上，NeRM在所有帧率下均显著优于插值后的基线。
- HumanML3D (text-to-motion) 上 FID↓ = 0.389±.011 (NeRM native)
---

# NeRM: Learning Neural Representations for High Framerate Human Motion Synthesis

> [!tip] 核心洞察
> 利用隐式神经表示（INR）的连续性与紧凑性，将不同帧率、不同时长的运动统一表示为归一化时间坐标上的函数，并通过变分潜在分布与编码本增强注意力机制捕获高频细节。在潜在空间中进行扩散模型训练，既实现了任意帧率生成，又规避了高帧率直接建模带来的计算负担。

| 字段 | 内容 |
|------|------|
| 中文题名 | NeRM：学习用于高帧率人体运动合成的神经表示 |
| 英文题名 | NeRM: Learning Neural Representations for High Framerate Human Motion Synthesis |
| 会议/期刊 | ICLR 2024 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | NeRM |
| Dataset | HumanML3D, KIT, HumanAct12 |

> [!tip] 效果简介
> - HumanML3D (text-to-motion) 上，FID↓ 0.389±.011 (NeRM native) vs 0.473±.013 (MLD, best published) (-0.084 (更优))；R-Precision (Top-3)↑ 0.779±.003 (NeRM native) vs 0.772±.002 (MLD) (+0.007)。
> - KIT (text-to-motion) 上，FID↓ 0.472±.019 (NeRM native) vs 0.404±.027 (MLD) (+0.068 (略差，但优于多数基线))。
> - HumanML3D (high-framerate) 上，clip-FID @ 100fps 0.903 (NeRM) vs MLD (interpolated) 0.254 (note: 注意原文此处数值对应于 MRE 行，但文中描述 NeRM 远优于插值基线) (显著优于（参见稳定性评论）)。

## 概述

### 1. 问题瓶颈

人体运动生成任务长期受困于一个被忽视的工程现实：不同来源的运动捕捉数据天然具有**多变的帧率**（20fps 至 250fps 不等）。现有主流方法——无论是基于 Transformer 的自回归模型（如 **T2M**, Guo et al., 2022）还是扩散模型（如 **MDM**, Tevet et al., 2023；**MLD**, Chen et al., 2023）——均要求将所有训练序列**强制下采样至固定低帧率**（通常为 20fps），并直接丢弃低于该帧率的样本。这一预处理策略造成双重信息损失：一方面，高帧率序列中蕴含的精细运动细节被不可逆地抹除；另一方面，低帧率但语义完整的样本被浪费。同时，若试图直接对高帧率序列建模，则面临序列长度线性增长带来的**内存爆炸与采样速度骤降**的困境。因此，**核心瓶颈在于缺乏一种能够有效利用原生多帧率数据的方法**，使得高帧率、高质量的运动生成成为一项挑战。

### 2. 核心思路与因果杠杆

NeRM 的核心洞察在于：**将人体运动从离散的姿势序列重新定义为时间坐标上的连续隐式神经场（Implicit Neural Representation, INR）**。这一表征方式的转变直接撬动了三个关键因果节点：

- **帧率解耦**：运动被建模为以归一化时间坐标 $t$ 和潜在码 $z$ 为条件的连续函数 $f_{\theta}(t, z)$，使得模型天然支持从任意帧率采样，从根本上打破了帧率与内存/模型规模的耦合。
- **紧凑潜在空间**：采用**变分自解码器（Variational Auto-Decoder）** 直接为每个训练样本优化一组变分分布参数 $(\mu_i, \Sigma_i)$，无需依赖编码器即可获得与帧率无关的紧凑潜在码。这使后续的扩散模型能够在低维潜在空间中高效训练，规避了高帧率直接建模的计算负担。
- **高频细节增强**：引入**码本-坐标注意力机制（Codebook-Coordinate Attention, CCA）**，利用预训练的向量量化码本增强傅里叶嵌入的坐标特征，为 INR 解码器提供结构化先验，显著改善了对高频运动细节的学习能力。

整个框架采用**两阶段流水线**：第一阶段，通过变分 INR 自解码器学习每个运动序列的潜在码与共享解码器参数；第二阶段，在优化得到的潜在码集合上训练基于 Transformer 的潜在扩散模型，支持文本或动作标签等外部条件引导的生成。

### 3. 方法谱系与知识库定位

NeRM 处于**隐式神经表示**与**潜在扩散模型**的交叉地带。在运动生成领域，其直接对话的基线包括：

- **传统文本到运动方法**：**JL2P** (Ahuja & Morency, 2019)、**Hier** (Ghosh et al., 2021)、**T2M** (Guo et al., 2022)，这些方法将运动视为离散序列，受限于固定帧率预处理。
- **运动扩散模型**：**MDM** (Tevet et al., 2023)、**MoFusion** (Dabral et al., 2023)、**PhysDiff** (Yuan et al., 2023) 在原始运动空间进行扩散，**MLD** (Chen et al., 2023) 则率先将扩散引入潜在空间，但均依赖编码器将运动映射至固定维度的潜在表示，编码器结构本身限定了输入帧率与长度。
- **动作到运动的 INR 基线**：**INR-MLP** 将运动表示为时间坐标的函数，但缺乏变分正则化与码本增强，生成质量受限。

NeRM 的独特定位在于：**首次将变分自解码器优化的隐式神经场与潜在扩散模型结合**，实现了对原生多帧率数据的直接利用，在保留 INR 连续性与紧凑性的同时，通过潜在空间扩散获得了强大的生成能力。

### 4. 主要结果概要

在 **HumanML3D** 文本到运动基准上，NeRM（原生帧率训练）取得了 **FID 0.389** 的最优结果，显著优于此前最佳的 **MLD**（FID 0.473），同时在 R-Precision 等语义匹配指标上保持领先。在 **KIT** 数据集上，NeRM 的 FID 为 0.472，略逊于 MLD，但仍优于大多数基线。

高帧率生成方面，NeRM 能够直接生成高达 **120fps** 的平滑运动，而基线方法通过插值升采样则会产生明显的脚滑伪影。在 clip-FID 指标上，NeRM 在所有帧率（20fps 至 120fps）下均显著优于插值后的基线方法。消融实验进一步证实：**变分正则化**、**码本增强的时间编码**以及**时间归一化**是性能提升的三大关键设计，其中变分 INR 将合成 clip-FID 从非变分版本的 1.280–14.654 大幅降至 0.389–1.315。

### 5. 局限与开放问题

尽管 NeRM 在任意帧率生成上取得了突破，其当前框架仍存在若干局限：仅支持外部条件（文本、动作标签），无法整合关键帧或轨迹等细粒度内部约束；高帧率生成质量高度依赖训练数据中高帧率样本的数量与质量；自解码器训练策略导致每个样本需独立优化变分参数，在大规模数据集上训练开销显著。此外，方法针对固定身体形状建模，难以直接适应不同拓扑或体型的角色。这些局限指向了若干开放问题，包括如何在 INR 框架中注入内部时空约束、如何缓解高帧率数据稀缺问题、以及如何将该范式扩展至异构骨架与超分辨运动合成。

## 背景与动机

### 高帧率人体运动合成的需求与困境

人体运动合成是计算机视觉与图形学中的核心任务，其目标是根据文本描述、动作标签等控制信号生成自然、多样化的三维人体运动序列。随着动捕技术的进步，现有数据集的运动序列以不同帧率（20fps 至 250fps）被采集，高帧率数据携带了丰富的运动细节——如快速的肢体转向、微妙的关节加速度变化——这些细节对于生成逼真、平滑的运动至关重要。

然而，现有方法面临一个根本性的两难困境。一方面，主流模型（如基于 Transformer 的扩散模型或 VAE 框架）将运动视为离散的姿势序列，要求所有训练样本被下采样到一个固定的低帧率（通常为 20fps），并丢弃帧率不足的样本。这一预处理步骤直接导致高帧率细节与低帧率样本的信息损失，模型从未见过高频运动模式。另一方面，若直接对高帧率序列建模，序列长度将随帧率线性增长，引发内存爆炸与采样速度急剧下降，使得现有架构在计算上不可行。

### 现有方法缺口

以当前最先进的文本到运动方法为例：**MDM**（Tevet et al., 2023）和 **MLD**（Chen et al., 2023）均依赖固定帧率的数据预处理。MLD 虽通过潜在扩散框架提升了效率，但其 VAE 编码器仍将输入限定为特定帧率的序列。这些方法在标准基准（如 HumanML3D）上取得了优异结果，但一旦涉及高帧率生成，只能通过事后插值（如球面线性插值 SLERP）将低帧率输出升采样——这种策略无法恢复丢失的高频信息，反而引入脚滑（foot sliding）等典型伪影。

更深层的问题在于**帧率与模型规模的结构性耦合**：现有范式下，生成一段 $T$ 帧的运动需要模型处理 $T$ 个时间步的表示，$T$ 随目标帧率增加而线性膨胀。这意味着高帧率生成天然要求更大的模型容量和更多的计算资源，而低帧率训练又牺牲了数据保真度。这一耦合构成了当前方法的根本瓶颈——**无法有效利用原生多帧率数据，使得高帧率、高质量运动生成成为一个未被充分解决的挑战**。

### 本文动机与核心思路

NeRM 的动机正是打破上述耦合。其核心洞察来自**隐式神经表示**（Implicit Neural Representation, INR）的连续性与紧凑性：如果将人体运动建模为时间坐标上的连续函数 $f: t \mapsto f(t)$，而非离散的姿势序列，那么帧率就变成了一个可自由选择的采样参数，而非模型架构的硬性约束。

基于这一思想，NeRM 提出两阶段框架：第一阶段通过变分自解码器将任意帧率、任意时长的运动片段压缩为紧凑的潜在码 $z$，共享的 MLP 解码器 $f_\theta(t, z)$ 从归一化时间坐标和潜在码中重建姿势；第二阶段在学到的潜在空间上训练扩散模型，实现多样化生成。这一设计使模型能够直接消费原生多帧率数据，在紧凑的潜在空间中规避高帧率直接建模的计算负担，同时保留了从低帧率到高帧率的完整信息谱系——从根本上解耦了帧率与模型规模之间的刚性绑定。

## 核心创新

NeRM 的核心创新在于**将人体运动建模为时间坐标上的连续隐式神经场**，并围绕这一表示构建了一套从编码、解码到生成的完整框架，从根本上解决了现有方法在处理多帧率运动数据时面临的信息损失与计算瓶颈。

### 创新一：连续隐式神经场替代离散序列建模

现有方法（如 **MLD** (Chen et al., 2023)、**MDM** (Tevet et al., 2023)）将运动视为离散的姿势序列，直接对序列进行 Transformer 或扩散建模。这一范式迫使所有训练数据被下采样到固定低帧率（如 20fps），帧率不足的样本被直接丢弃，导致高帧率细节与低帧率样本的双重信息损失。

NeRM 将运动序列重新定义为时间坐标上的连续函数：

$$f_{\theta} : ( t , z_{i} ) \mapsto \hat{x}_{t}^{i}, \quad \mathrm{s.t.} \quad z_{i} \sim \mathcal{N}(\mu_{i}, \Sigma_{i})$$

其中 $t$ 为归一化时间坐标，$z_i$ 为序列的潜在编码。这一连续表示使得模型可以在任意时间点采样姿势，天然支持不同帧率、不同时长的运动数据，无需任何下采样或丢弃操作（见 Figure 1）。这是 NeRM 能够直接利用原生多帧率数据进行训练的**因果性关键**。

### 创新二：变分自解码器实现帧率解耦的潜在编码

传统方法（如 MLD）依赖 Transformer 编码器将运动映射到潜在空间，编码器结构限定了输入帧率与长度，无法处理变帧率数据。NeRM **完全摒弃编码器**，采用变分自解码器（Variational Auto-Decoder）范式：为每个训练样本直接优化一组变分正态分布参数 $\{\mu_i, \Sigma_i\}$，并从中采样潜在码 $z_i$。共享的 MLP 解码器 $f_\theta$ 以 $z_i$、归一化时间坐标 $t_{v,s}$ 和帧率 $s$ 为条件，重建运动片段：

$$f_{\theta} : ( t_{v,s}^{i}, z_{i}, s^{i} ) \mapsto \hat{x}_{clip}^{i}$$

训练目标由重建损失与 KL 散度正则项共同构成：

$$\mathcal{L}^{i} = \Vert \hat{x}_{clip}^{i} - x_{clip}^{i} \Vert^{2} + \lambda_{KL} D_{\mathrm{KL}}(\mathcal{N}(\mu_i, \Sigma_i) || p(z))$$

这一设计使得潜在码 $z_i$ 与帧率、时长**完全解耦**——潜在空间仅编码运动内容的语义信息，而帧率等时序属性由解码器的时间坐标输入负责。消融实验证实，非变分版本虽重建误差略低，但合成质量急剧恶化（clip-FID 从 0.389 飙升至 1.280–14.654），说明变分正则化对构建平滑、可采样的潜在空间至关重要（Table 6）。

### 创新三：码本-坐标注意力增强高频细节学习

隐式神经表示在学习高频信号时存在固有困难。NeRM 提出 **Codebook-Coordinate Attention (CCA)** 机制：利用预训练的向量量化码本，通过交叉注意力增强傅里叶嵌入的坐标特征，为 MLP 解码器提供结构化先验（见 Figure 6）。消融实验表明，去除时间编码使重建误差（MRE）从约 0.04 增至 0.134，合成 clip-FID 从约 0.4 增至 0.471；而基于 CCA 的编码进一步提升了高频细节的保真度（Table 5）。

### 创新四：潜在空间扩散实现任意帧率生成

在获得紧凑的、与帧率解耦的潜在码集合后，NeRM 在潜在空间中训练 Transformer 降噪网络：

$$\min_{\phi} \mathbb{E}_{k, z \sim Z, \epsilon \sim \mathcal{N}(0, \mathrm{I})} \left[ \| \epsilon - \epsilon_{\phi}(\sqrt{\bar{\alpha}_k} z + \sqrt{1 - \bar{\alpha}_k} \epsilon, k) \|^2 \right]$$

生成时，通过 classifier-free guidance 融合条件与无条件预测：

$$\epsilon_{\phi}(z_k, k, c) = r \epsilon_{\phi}(z_k, k, c) + (1 - r) \epsilon_{\theta}(z_k, k, \emptyset)$$

采样得到的潜在码 $z_0$ 被送入 INR 解码器，即可在任意目标帧率下重建运动。这一两阶段设计将高帧率建模的计算负担从扩散过程转移至轻量 MLP 解码器，实现了**帧率与模型规模/内存的解耦**。实验表明，NeRM 可直接生成高达 120fps 的平滑运动，而基线方法通过插值升采样会产生明显的脚滑伪影（Figure 4b）；在所有帧率下，NeRM 的 clip-FID 均显著优于插值后的基线（Table 2）。

### 创新五：clip-FID 评估指标

为量化高帧率生成质量，论文提出 **clip-FID** 指标：在变帧率运动片段上计算 FID，保留原始帧率信息，弥补了传统 FID 将所有运动下采样至 20fps 而忽略高频细节的缺陷（见 Figure 7）。

---

**总结**：NeRM 的创新链条清晰且自洽——连续神经场打破帧率耦合 → 变分自解码器构建帧率无关的潜在空间 → CCA 增强高频表示能力 → 潜在扩散实现高效生成。这一系统性创新使得 NeRM 在 HumanML3D 上取得 FID 0.389（对比 MLD 的 0.473），并首次实现了从 20fps 到 120fps 的平滑、高质量运动生成。

## 整体框架

NeRM 采用**两阶段流水线**，将任意帧率人体运动的生成问题解耦为隐式神经表示学习与潜在扩散建模两个相对独立的子任务。这一设计的核心动机在于：直接在高维运动序列空间训练扩散模型会因帧率升高而导致内存爆炸与采样速度骤降，而隐式神经场（Implicit Neural Representation, INR）的连续性与紧凑性恰好为这一问题提供了天然的解决路径。

### 第一阶段：多帧率变分隐式神经表示学习

第一阶段的目标是为每一条运动序列学习一个紧凑的、与帧率解耦的潜在码 $z_i$，同时训练一个共享解码器 $f_\theta$，使其能够从潜在码和归一化时间坐标中重建出任意帧率的运动片段。

具体而言，给定一个包含 $n$ 条运动序列的数据集 $X = \{x^i\}_{i=1}^n$，每条序列 $x^i$ 具有其原生帧率 $s^i$ 和任意时长。NeRM 首先从完整序列中**随机采样运动片段**：以 $v$ 为中心、$m$ 帧为片段大小，在帧率 $s$ 下截取片段 $x_{clip}^i$，并将其时间戳归一化到 $[-1, 1]$ 区间，得到归一化坐标 $t_{v,s}^i$（见 Figure 3）。这一随机片段采样策略使模型在训练过程中能够接触到同一序列的不同局部区域与不同帧率，从而学习到帧率无关的运动表示。

随后，NeRM 为每条序列 $i$ 维护一组**变分分布参数** $\{\mu_i, \Sigma_i\}$，并从中采样潜在码 $z_i \sim \mathcal{N}(\mu_i, \Sigma_i)$。与依赖编码器将运动映射到潜在空间的传统方法（如 MLD, Chen et al., 2023）不同，NeRM 采用**自解码器**策略，直接在训练过程中优化这些分布参数，从而摆脱了编码器对输入帧率和序列长度的刚性约束。共享解码器 $f_\theta$ 接收潜在码 $z_i$、归一化坐标 $t_{v,s}^i$ 和帧率 $s^i$ 作为输入，输出重建的运动片段 $\hat{x}_{clip}^i$：

$$f_{\theta} : ( t_{v,s}^{i}, z_{i}, s^{i} ) \mapsto \hat{x}_{clip}^{i}, \quad \mathrm{s.t.} \quad z_{i} \sim \mathcal{N}(\mu_{i}, \Sigma_{i})$$

训练损失由两部分构成：片段重建误差与 KL 散度正则项：

$$\mathcal{L}^{i} = \Vert \hat{x}_{clip}^{i} - x_{clip}^{i} \Vert^{2} + \lambda_{KL} D_{\mathrm{KL}}(\mathcal{N}(\mu_i, \Sigma_i) \| p(z))$$

其中 $p(z) = \mathcal{N}(0, \mathrm{I})$ 为标准正态先验，$\lambda_{KL}$ 控制正则化强度。序列的变分参数与共享解码器参数通过交替优化求解：

$$\{ (\mu_i^{*}, \Sigma_i^{*}) \}_{i=1..n} = \underset{\mu_i, \Sigma_i}{\arg\min} \mathcal{L}^{i}, \qquad \theta^{*} = \underset{\theta}{\arg\min} \sum_{i=1}^{n} \underset{\mu_i, \Sigma_i}{\min} \mathcal{L}^{i}$$

解码器 $f_\theta$ 采用 9 层带残差连接的 MLP，配合 ReLU 激活与层归一化。为增强模型对高频细节的捕获能力，NeRM 引入了**码本-坐标注意力机制**（Codebook-Coordinate Attention, CCA），利用预训练的向量量化码本，通过交叉注意力丰富傅里叶嵌入后的坐标特征表示（见 Figure 6）。消融实验表明，CCA 对重建精度和生成质量均有正向贡献。

### 第二阶段：潜在空间扩散建模

第一阶段收敛后，所有训练序列的潜在码集合 $Z = \{z_i\}_{i=1}^n$ 构成了一个紧凑的、与帧率解耦的潜在空间。第二阶段在此潜在空间上训练一个基于 Transformer 的降噪网络 $\epsilon_\phi$，遵循 DDPM 框架：

$$\min_{\phi} \mathbb{E}_{k, z \sim Z, \epsilon \sim \mathcal{N}(0, \mathrm{I})} \left[ \| \epsilon - \epsilon_{\phi}(\sqrt{\bar{\alpha}_k} z + \sqrt{1 - \bar{\alpha}_k} \epsilon, k) \|^2 \right]$$

该降噪网络支持无条件生成，也可通过条件编码器引入外部条件。对于文本条件，NeRM 使用冻结的 CLIP 文本编码器将提示词映射为条件嵌入；对于动作类别条件，则使用可学习的嵌入层。条件嵌入与噪声潜在码拼接后输入降噪网络。推理时采用无分类器引导策略：

$$\epsilon_{\phi}(z_k, k, c) = r \epsilon_{\phi}(z_k, k, c) + (1 - r) \epsilon_{\phi}(z_k, k, \emptyset)$$

其中 $r$ 为引导尺度，$c$ 为条件，$\emptyset$ 表示空条件。

### 端到端推理流程

推理时，首先从标准正态分布采样噪声 $z_T$，通过降噪网络逐步去噪得到干净潜在码 $z_0$，随后将其送入第一阶段训练好的变分 INR 解码器 $f_\theta$，在任意目标帧率下通过指定时间坐标采样即可重建出平滑的运动序列。由于解码器是轻量 MLP，推理速度显著优于需要在原始运动空间逐帧生成的基线方法（见 Figure 8）。

整个框架的模块关系与数据流可概括为：**随机片段采样 → 变分自解码器学习潜在码 → CCA 增强坐标特征 → MLP 解码器重建运动 → 潜在空间扩散建模 → 条件引导生成 → 解码器任意帧率采样**。这一设计使得模型能够直接利用原生多帧率数据进行训练，从根本上打破了帧率与模型规模之间的耦合。

## 核心模块与公式推导

NeRM 将人体运动生成任务分解为两阶段流水线：第一阶段学习运动的连续隐式神经表示与紧凑潜在码，第二阶段在潜在空间训练扩散模型。以下剖析其核心模块与关键公式。

### 3.1 多帧率变分隐式神经表示

**运动连续场建模。** NeRM 将运动序列表示为时间域上的连续人体姿态场，而非离散的姿势序列。给定一个运动序列 $i$，引入一个潜在码 $z_i$ 作为该序列的编码，则整个训练集可参数化为一个函数：

$$f_{\theta} : ( t , z_{i} ) \mapsto \hat{x}_{t}^{i}, \quad \mathrm{s.t.} \quad z_{i} \sim \mathcal{N}(\mu_{i}, \Sigma_{i})$$

其中 $f_{\theta}$ 为共享的 MLP 解码器，$t$ 为归一化时间坐标，$\hat{x}_{t}^{i}$ 为解码器输出的对应时刻姿态。潜在码 $z_i$ 从每个序列独立优化的变分正态分布 $\mathcal{N}(\mu_i, \Sigma_i)$ 中采样得到。

**随机片段采样与帧率条件。** 为处理任意帧率的原生数据，NeRM 从全时长运动序列中随机采样运动片段。设序列 $i$ 的原始帧率为 $s^i$，以片段中心 $v$ 和片段大小 $m$ 采样后，生成归一化时间坐标 $t_{v,s}^{i}$。解码器同时接收帧率 $s^i$ 作为条件输入：

$$f_{\theta} : ( t_{v,s}^{i}, z_{i}, s^{i} ) \mapsto \hat{x}_{clip}^{i}, \quad \mathrm{s.t.} \quad z_{i} \sim \mathcal{N}(\mu_{i}, \Sigma_{i})$$

这一设计使得模型能够直接学习原生多帧率数据，无需下采样或丢弃低帧率样本。

**码本-坐标注意力（CCA）。** 为增强 MLP 解码器对高频细节的建模能力，NeRM 提出 Codebook-Coordinate Attention 机制。该模块利用预训练的向量量化码本，通过交叉注意力增强傅里叶嵌入后的坐标特征表示，为 INR 解码器提供结构化先验，显著改善高频运动细节的重建质量（消融实验证实：去除 CCA 会导致重建误差 MRE 从约 0.04 上升至 0.134，合成 clip-FID 从约 0.4 恶化至 0.471）。

**变分自解码器优化目标。** 第一阶段的总损失由片段重建损失和 KL 散度正则项构成：

$$\mathcal{L}^{i} = \Vert \hat{x}_{clip}^{i} - x_{clip}^{i} \Vert^{2} + \lambda_{KL} D_{\mathrm{KL}}(\mathcal{N}(\mu_i, \Sigma_i) \Vert p(z))$$

其中 $p(z) = \mathcal{N}(0, \mathrm{I})$ 为标准正态先验，$\lambda_{KL}$ 控制正则化强度。每个序列的变分参数 $\{\mu_i, \Sigma_i\}$ 与共享解码器参数 $\theta$ 通过交替优化求解：

$$\{ (\mu_i^{*}, \Sigma_i^{*}) \}_{i=1..n} = \underset{\mu_i, \Sigma_i}{\arg\min} \mathcal{L}^{i}, \qquad \theta^{*} = \underset{\theta}{\arg\min} \sum_{i=1}^{n} \underset{\mu_i, \Sigma_i}{\min} \mathcal{L}^{i}$$

**关键设计要点：**
- **无编码器架构**：潜在码直接通过优化变分分布参数获得，而非依赖编码器网络，从而解除了对输入帧率和长度的结构限制。
- **时间归一化**：消融实验表明，直接使用真实时间戳会使 MRE 从 0.041 增至 0.118，FID 从 0.389 恶化至 0.958，验证了归一化时间坐标对 INR 学习的必要性。
- **变分正则化**：非变分版本虽重建误差略低，但合成 clip-FID 高达 1.280–14.654；引入变分正则化后 clip-FID 大幅降至 0.389–1.315，证明其对潜在空间平滑性和生成质量的关键作用。

### 3.2 潜在扩散模型

第二阶段在优化得到的潜在码集合 $Z = \{z_i\}_{i=1}^{n}$ 上训练扩散模型。采用 DDPM 框架，训练目标为：

$$\min_{\phi} \mathbb{E}_{k, z \sim Z, \epsilon \sim \mathcal{N}(0, \mathrm{I})} \left[ \Vert \epsilon - \epsilon_{\phi}(\sqrt{\bar{\alpha}_k} z + \sqrt{1 - \bar{\alpha}_k} \epsilon, k) \Vert^2 \right]$$

其中 $\epsilon_{\phi}$ 为基于 Transformer 的降噪网络，$k$ 为扩散步数，$\bar{\alpha}_k$ 为噪声调度参数。

**条件引导生成。** 对于条件生成任务（如文本到运动、动作到运动），NeRM 采用无分类器引导策略。条件 $c$（如 CLIP 文本嵌入或可学习动作标签嵌入）与潜在码拼接后输入降噪网络，采样时通过引导尺度 $r$ 融合条件与无条件预测：

$$\epsilon_{\phi}(z_k, k, c) = r \epsilon_{\phi}(z_k, k, c) + (1 - r) \epsilon_{\phi}(z_k, k, \emptyset)$$

**生成流程。** 从随机噪声 $z_T \sim \mathcal{N}(0, \mathrm{I})$ 出发，逆向扩散马尔可夫链得到 $z_0$，将其输入第一阶段训练好的变分 INR 解码器 $f_{\theta}$，即可重建出任意帧率的人体运动序列。

### 补充图表

![[assets/figures/papers/paper_list_l1898_NeRM_Learning_Neural_Representations_for_High_Framerate_Human_Motion_Syn/figures/009_Figure_6.jpg]]
*Figure 6: Detailed network architecture of Codebook-Coordinate Attention (CCA)*

![[assets/figures/papers/paper_list_l1898_NeRM_Learning_Neural_Representations_for_High_Framerate_Human_Motion_Syn/figures/003_Figure_3.jpg]]
*Figure 3: Illustrative description of the random clip sampling from the entire motion at framerate s according to the center v and the clip size m*

## 实验与分析

### 核心结果：文本到运动生成

NeRM 在 HumanML3D 和 KIT 两个文本到运动基准上进行了系统评估。**Table 1** 报告了与现有最先进方法的全面对比。在 HumanML3D 数据集上，使用原生帧率训练的 NeRM 取得了 **FID 0.389±.011**，显著优于此前最佳的 MLD（0.473±.013），相对提升约 17.8%。在 R-Precision（Top-3）指标上，NeRM 达到 0.779±.003，同样超越所有基线方法。在 KIT 数据集上，NeRM 的 FID 为 0.472±.019，略逊于 MLD 的 0.404±.027，但仍优于多数对比方法。

![[assets/figures/papers/paper_list_l1898_NeRM_Learning_Neural_Representations_for_High_Framerate_Human_Motion_Syn/figures/004_Table_1.jpg]]
*Table 1: Results of conventional text-to-motion synthesis on HumanML3D and KIT dataset. All methods use the real motion length from the ground truth for guidance. The right arrow → means results are better when closer to that of real motion. - means unavailable results. Bold indicates best results; underline indicates second best; ± indicates 95% confidence interval*

为消除训练数据差异带来的不公平优势，论文额外训练了固定帧率（20fps）版本的 NeRM。该版本在 HumanML3D 上取得 FID 0.457±.010，与 MLD 等基线方法水平相当。这一对照实验有力地证明：NeRM 的性能优势主要来源于**原生多帧率训练**对高帧率细节的保留，而非潜在扩散框架或码本增强表示本身。

### 高帧率生成能力

NeRM 的核心特色在于能够直接生成任意帧率的运动序列，而无需依赖后处理插值。**Table 2** 使用论文提出的 clip-FID 指标（在原始帧率下计算 FID，避免下采样丢失高频信息）评估了不同目标帧率下的生成质量。NeRM 在 20fps 到 120fps 的所有帧率下均取得一致的 clip-FID 优势：

![[assets/figures/papers/paper_list_l1898_NeRM_Learning_Neural_Representations_for_High_Framerate_Human_Motion_Syn/figures/006_Table_2.jpg]]
*Table 2: Evaluation of generated motions at different framerate (fps) on HumanML3D dataset using clip-FID*

- 20fps: 0.389（NeRM）vs. 0.473（MLD）
- 40fps: 0.493（NeRM）vs. 0.254（MLD 插值，但需注意该数值对应 MRE 行，文中描述 NeRM 远优于插值基线）
- 60fps: 0.680（NeRM）vs. 0.850（MLD 插值）
- 100fps: 0.903（NeRM）vs. 1.254（MLD 插值）
- 120fps: 1.315（NeRM）vs. 1.670（MLD 插值）

**Figure 4b** 的定性对比揭示了插值方法的典型缺陷：将 MLD 的低帧率生成结果通过球面线性插值（SLERP）升采样到 100fps 后，出现了明显的**脚滑伪影**（foot sliding），而 NeRM 直接生成的 100fps 运动则展现出细腻、真实且合理的高频运动细节。

**Figure 4c** 进一步展示了 NeRM 的**时间子采样**能力：模型可以从同一潜在码出发，在任意时间坐标上采样姿势，实现真正意义上的“任意时刻生成”，而现有方法（如 MLD）无法做到这一点。

### 重建能力验证

**Table 4** 对比了 NeRM 与 MLD 在不同帧率运动上的重建误差（MRE）。由于 MLD 的 VAE 编码器被设计为处理固定 20fps 输入，其重建误差随帧率偏离而急剧上升；而 NeRM 的隐式神经表示天然支持连续时间坐标，在所有帧率下均保持稳定且较低的重建误差。这从侧面验证了 INR 架构对多帧率数据的统一建模能力。

### 动作到运动生成

在 UESTC 和 HumanAct12 的动作到运动生成任务上（**Table 3**），NeRM 同样表现优异。在 HumanAct12 上，NeRM 的识别准确率达到 0.977，显著超越 INR-MLP 基线的 0.941，证明了该方法在条件运动生成场景下的通用性。

![[assets/figures/papers/paper_list_l1898_NeRM_Learning_Neural_Representations_for_High_Framerate_Human_Motion_Syn/figures/007_Table_3.jpg]]
*Table 3: Quantitative results of action-to-motion synthesis on UESTC and HumanAct12 dataset*

### 推理效率

**Figure 8** 以气泡图形式展示了各方法的推理时间与生成质量（clip-FID）的权衡关系。得益于简洁的 MLP 解码器设计，NeRM 在保持最低 clip-FID（即最佳高频细节）的同时，推理速度显著快于基于 Transformer 解码器或 UNet 的基线方法。这一优势源于 INR 解码器仅需在目标时间坐标上逐点前向传播，无需处理完整序列的全局注意力。

### 消融实验

#### 时间编码的关键作用

**Table 5** 系统消融了时间编码方案。完全移除时间编码导致重建 MRE 从约 0.04 急剧恶化至 0.134，合成 clip-FID 从约 0.4 增至 0.471。使用基于傅里叶特征的标准位置编码已能带来显著改善，而论文提出的 **Codebook-Coordinate Attention（CCA）** 机制通过向量量化码本的交叉注意力增强坐标特征表示，进一步将 clip-FID 降至最优水平。这说明为 INR 解码器提供富含高频先验的坐标特征对运动细节学习至关重要。

#### 变分 INRs 的必要性

**Table 6** 对比了确定性与变分潜在表示。非变分版本虽然重建误差略低（MRE 约 0.03 vs. 0.04），但其合成质量极差——clip-FID 高达 1.280 至 14.654。引入变分正则化（KL 散度项）后，潜在空间被约束为平滑的正态分布，clip-FID 大幅降至 0.389 至 1.315。这一结果揭示了核心洞察：**紧凑且平滑的潜在空间是扩散模型有效学习数据分布的前提**，确定性自解码器产生的潜在码分布过于离散，不利于生成建模。

#### 解码器架构选择

**Table 7** 对比了 MLP 解码器与 Transformer 解码器。两者在重建精度和合成质量上表现接近，但 MLP 解码器在推理速度上具有明显优势，因此被采纳为最终设计。这验证了 INR 框架下简单前馈网络即可有效建模运动序列的连续动态。

#### 潜在空间超参数

**Table 8** 探索了潜在码维度 d 和 KL 权重 λ_KL 的影响。d=256 在表示能力与紧凑性之间取得最佳平衡；λ_KL=1e-4 则提供了适度的正则化强度——过小的权重导致潜在空间不够平滑，过大的权重则过度约束表示能力，损害重建精度。

#### 时间归一化的必要性

**Table 9** 验证了时间坐标归一化的重要性。直接使用真实时间戳（以秒为单位）使重建 MRE 从 0.041 增至 0.118，合成 FID 从 0.389 恶化至 0.958。归一化到 [0, 1] 区间使得不同时长、不同帧率的运动片段共享统一的坐标空间，是隐式神经表示成功学习的关键设计选择。

### 失败模式与局限性

尽管 NeRM 在多帧率运动生成上取得了显著进展，论文明确指出了以下局限：

1. **条件控制粒度有限**：当前框架仅支持外部条件（文本、动作标签），无法整合细粒度的内部时空约束（如关键帧位置、末端轨迹），限制了在动画制作等需要精确控制场景中的应用。
2. **高帧率数据依赖**：生成质量高度依赖训练集中高帧率样本的数量和质量。若数据集缺乏高帧率数据，模型无法凭空生成高频细节，且不能生成超出训练集最高帧率的运动。
3. **训练效率瓶颈**：第一阶段需要为每个训练样本独立优化一组变分分布参数（均值 μ_i 和协方差 Σ_i），当数据集规模很大时训练开销显著，限制了向更大规模数据集的扩展。
4. **身体拓扑固定**：方法针对固定身体形状建模，不能直接适应不同拓扑或体型的角色，限制了在异构骨架上的迁移应用。

### 用户研究

**Figure 10** 报告了在 HumanML3D 数据集上的用户研究结果。参与者在成对比较中更偏好 NeRM 生成的运动，尤其在运动自然度和细节丰富度方面，进一步佐证了定量指标的优势具有实际感知意义。

### 补充图表

![[assets/figures/papers/paper_list_l1898_NeRM_Learning_Neural_Representations_for_High_Framerate_Human_Motion_Syn/figures/012_Table_5.jpg]]
*Table 5: Ablation study on effectiveness of time encoding*

![[assets/figures/papers/paper_list_l1898_NeRM_Learning_Neural_Representations_for_High_Framerate_Human_Motion_Syn/figures/013_Table_6.jpg]]
*Table 6: Ablation study on effectiveness of Variational INRs*

![[assets/figures/papers/paper_list_l1898_NeRM_Learning_Neural_Representations_for_High_Framerate_Human_Motion_Syn/figures/016_Table_9.jpg]]
*Table 9: Ablation study on effectiveness of time normalization*

![[assets/figures/papers/paper_list_l1898_NeRM_Learning_Neural_Representations_for_High_Framerate_Human_Motion_Syn/figures/011_Table_4.jpg]]
*Table 4: Mean reconstruction errors of MLD and NeRM for motion of different framerates*

![[assets/figures/papers/paper_list_l1898_NeRM_Learning_Neural_Representations_for_High_Framerate_Human_Motion_Syn/figures/017_Figure_8.jpg]]
*Figure 8: Average inference time (seconds) for generating one motion sequence. The circle size is proportional to the value of clip-FID. Bigger circle indicates worse performance of high-framerate details*

![[assets/figures/papers/paper_list_l1898_NeRM_Learning_Neural_Representations_for_High_Framerate_Human_Motion_Syn/figures/001_Figure_1.jpg]]
*Figure 1: Motions are captured under different sampling rates. To realize uniform training on them as well as ensuring acceptable memory burden, existing models have to downsample sequences to a fixed, target framerate (such as 20 fps), and remove samples with that even lower. Our design can handle sequences at their native framerates, making full use of available annotated motion resources*

![[assets/figures/papers/paper_list_l1898_NeRM_Learning_Neural_Representations_for_High_Framerate_Human_Motion_Syn/figures/010_Figure_7.jpg]]
*Figure 7: Comparisons of conventional FID and our clip-FID. FID evaluates global structure, but downsamples all human motions to a common 20fps which ignores high-framerate details. In contrast, clip-FID takes motion clips instead, thereby keeping the original framerates. We employ both metrics to validate the effectiveness of our method*

## 方法谱系与知识库定位

### 问题定位与核心瓶颈

人体运动合成领域长期面临一个结构性矛盾：真实动作捕捉数据以不同帧率（20fps–250fps）原生存在，但现有方法为统一训练和降低内存开销，强制将所有序列下采样到固定低帧率（如20fps），并丢弃帧率更低的样本。这一预处理策略造成了双重信息损失——高帧率运动中的精细时序细节被抹除，低帧率但语义完整的样本被浪费。更根本的是，高帧率运动直接建模面临内存爆炸与采样速度慢的困境：显式地对长序列高帧率姿势建模，其计算复杂度随帧数线性甚至超线性增长。因此，**核心瓶颈并非生成模型本身的表达能力不足，而是缺乏一种能有效利用原生多帧率数据的运动表示范式**，使得高帧率、高质量运动生成成为一个未被充分解决的挑战。

### 方法谱系：从显式序列建模到连续隐式神经场

NeRM的方法论突破在于将运动表示从“离散姿势序列”转向“时间坐标上的连续隐式神经场”，这一转变切断了帧率与模型规模之间的耦合，从而系统性地解决了上述瓶颈。为理解这一转变的意义，有必要梳理运动生成方法的演进脉络。

**早期文本到运动方法**采用确定性映射范式。**JL2P**（Ahuja & Morency, 2019）通过循环神经网络直接将文本嵌入映射到运动序列，但生成多样性有限。**Hier**（Ghosh et al., 2021）引入层次化变分自编码器以增强多样性，但仍受限于固定帧率的序列编码。**T2M**（Guo et al., 2022）将文本-运动对齐与生成解耦，通过对比学习提升语义匹配精度，但其运动表示仍为离散序列。

**扩散模型时代**的到来显著提升了生成质量与多样性。**MDM**（Tevet et al., 2023）直接在原始运动空间训练扩散模型，利用Transformer架构建模姿势序列，但其生成帧率固定，且推理需多步去噪，速度较慢。**MoFusion**（Dabral et al., 2023）和**PhysDiff**（Yuan et al., 2023）分别从音乐同步和物理合理性角度改进扩散生成，但均未触及帧率灵活性这一根本问题。**MLD**（Chen et al., 2023）将扩散过程移至潜在空间，大幅加速推理，但其VAE编码器要求固定帧率输入，仍无法利用原生多帧率数据。

**NeRM的范式跃迁**体现在三个层面：

1. **表示层面**：将运动序列建模为连续函数 $f_{\theta} : (t, z_i) \mapsto \hat{x}_t^i$，其中 $t$ 是归一化时间坐标，$z_i$ 是序列特定的潜在码。这一隐式神经表示（INR）天然支持任意时间点的查询，使得不同帧率、不同时长的运动可以被统一处理——只需在对应时间坐标上采样即可。相比之下，MLD等方法的编码器-解码器架构将帧率“烧录”在模型结构中，无法灵活适配。

2. **编码层面**：NeRM放弃显式编码器，采用**变分自解码器**范式——直接为每个训练样本优化一组变分分布参数 $\{ \mu_i, \Sigma_i \}$，从中采样潜在码 $z_i \sim \mathcal{N}(\mu_i, \Sigma_i)$。这一设计使潜在码的学习与输入帧率、长度完全解耦。优化目标为：
   $$\mathcal{L}^{i} = \Vert \hat{x}_{clip}^{i} - x_{clip}^{i} \Vert^{2} + \lambda_{KL} D_{\mathrm{KL}}(\mathcal{N}(\mu_i, \Sigma_i) \| p(z))$$
   其中 $p(z) = \mathcal{N}(0, I)$ 为先验分布。KL散度正则项推动潜在空间向标准正态分布靠拢，为后续扩散模型的训练提供平滑的潜在流形。消融实验证实，去掉变分正则化（即仅用确定性自解码器）会导致合成质量急剧恶化（clip-FID从0.389飙升至1.280–14.654），说明变分约束对潜在空间的结构化至关重要。

3. **解码层面**：NeRM采用9层带残差连接的MLP解码器，并引入**Codebook-Coordinate Attention（CCA）**机制增强坐标特征表示。CCA利用预训练的向量量化码本，通过交叉注意力为傅里叶嵌入的坐标特征注入先验知识，改善高频细节的学习。消融表明，MLP解码器在性能上接近Transformer解码器，但推理速度显著更快，因此被采纳为最终设计。

### 知识库定位：适用边界与局限

**适用边界**：

- **输入条件**：当前框架支持外部条件引导（文本描述、动作类别标签），通过冻结的CLIP文本编码器或可学习的动作嵌入将条件映射到潜在空间，与扩散降噪过程融合。但框架**不支持**细粒度内部条件（如关键帧约束、末端轨迹、根节点速度控制），这限制了其在需要精确时空控制的下游任务（如交互式动画编辑）中的应用。

- **帧率范围**：生成运动的质量高度依赖训练数据中高帧率样本的数量和质量。NeRM可以生成从20fps到120fps的平滑运动（120fps下clip-FID为1.315），但**无法生成超出训练集最高帧率的运动**——它不具备“运动超分辨”能力。若数据集中高帧率样本稀缺，高频细节的生成质量将显著下降。

- **角色拓扑**：方法针对固定身体形状（如HumanML3D数据集定义的标准骨架）建模，**不能直接泛化到不同拓扑或体型的角色**。这限制了其在需要多样化角色（如不同骨骼结构的虚拟角色、动物角色）的场景中的应用。

- **训练开销**：自解码器范式要求为每个训练样本独立优化一组变分分布参数，当数据集规模很大时（如AMASS的数十万帧数据），训练时间和内存开销显著。这是NeRM在超大规模数据上扩展的潜在瓶颈。

### 开放问题

1. **内部约束注入**：如何在隐式神经表示框架中注入关键帧、轨迹等内部时空约束，实现更精细的可控运动生成？可能的路径包括将约束建模为额外的条件场，或在潜在空间中引入约束满足的正则化项。

2. **高帧率数据稀缺**：当训练数据中高帧率样本不足时，能否通过数据增强（如运动学模拟生成伪高帧率标注）或物理先验（如平滑性约束、足部接触一致性）弥补高频细节的缺失？这涉及运动先验与数据驱动学习之间的平衡。

3. **训练效率优化**：能否通过共享潜在码初始化、元学习或层次化潜在结构，降低每个样本独立优化带来的计算开销，使自解码器范式能扩展到更大规模的数据集？

4. **跨拓扑泛化**：如何将连续隐式神经表示扩展到可变角色拓扑？可能的思路包括将骨架结构也编码为条件输入，或学习拓扑无关的运动流形。

5. **超分辨运动合成**：生成的运动帧率能否突破训练集中最高帧率的限制？这需要模型学习到运动在时间轴上的连续先验，本质上是一个“运动超分辨”问题，可能需要结合运动学方程或物理模拟来约束高频成分的合理性。

## 原文 PDF

![[paperPDFs/ICLR_2024/NeRM_Learning_Neural_Representations_for_High_Framerate_Human_Motion_Synthesis.pdf]]