---
title: "Latent Fourier Transform"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Latent_Fourier_Transform.pdf
project_link: null
code_link: null
openreview_forum_id: ogMxCjdCCq
aliases:
- LFTL
- LFT
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "在潜在序列的傅里叶域进行随机频率掩膜训练，迫使编码器将不同时间尺度的音乐特征分离到不同的潜频率bin中，使得推理时通过频谱掩膜即可调节条件。"
primary_logic: "将扩散自编码器与潜在空间傅里叶变换相结合，引入频率掩膜训练策略，实现了音乐模式按时间尺度的正交分离，提供了一条直观的连续频率轴用于条件生成、混合与频谱解释。"
claims:
- "LATENTFT combines a diffusion autoencoder with a latent-space Fourier transform to separate musical patterns by timescale."
- "Training involves randomly masking latents in the Fourier domain, and the decoder reconstructs the audio from the frequency-masked latent sequence."
- "Removing frequency masking during training substantially degrades audio quality (FAD 5.341 vs 0.349 in conditional generation) and adherence."
- "Using locally correlated scores to mask frequency bins, forming contiguous regions, is key to performance; removing correlation increases FAD to 2.744."
---

# Latent Fourier Transform

> [!tip] 核心洞察
> 将扩散自编码器与潜在空间傅里叶变换相结合，引入频率掩膜训练策略，实现了音乐模式按时间尺度的正交分离，提供了一条直观的连续频率轴用于条件生成、混合与频谱解释。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 潜在傅里叶变换 |
| 英文题名 | Latent Fourier Transform |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=ogMxCjdCCq) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Latent Fourier Transform (LATENTFT) |
| Dataset | MTG-Jamendo Conditional Generation, MTG-Jamendo Blending, GTZAN Conditional Generation |

> [!tip] 效果简介
> - MTG-Jamendo Conditional Generation 上，FAD (↓) 为 0.337 (LATENTFT-UNet)，对比 1.124 (ILVR)，变化 -0.787。
> - MTG-Jamendo Conditional Generation 上，Loudness Correlation (↑) 为 0.834 (LATENTFT-UNet)，对比 0.551 (ILVR)，变化 +0.283。
> - MTG-Jamendo Blending 上，FAD (↓) 为 1.357 (LATENTFT-UNet)，对比 2.696 (ILVR)，变化 -1.339。

## 概要

音乐生成模型（扩散模型、自回归模型、掩码语言模型）通常以粗到细的方式运作，不同噪声级别或量化层级天然耦合了时间尺度信息。这使得用户无法选择性地提取参考音频中特定时间尺度的音乐模式（如节奏、和弦进行、音色纹理）进行条件生成——这是现有方法的真实瓶颈。

**LATENTFT** 提出了一种根本不同的解决方案：在潜在序列的傅里叶域进行随机频率掩膜训练，迫使编码器将不同时间尺度的音乐特征分离到不同的潜频率 bin 中。其核心洞察在于将扩散自编码器与潜在空间傅里叶变换相结合，通过频率掩膜训练策略实现音乐模式按时间尺度的正交分离，为用户提供了一条直观的连续频率轴，用于条件生成、混合与频谱解释。

在方法定位上，LATENTFT 区别于基于离散声学 token 的掩码模型（如 Vampnet, Garcia et al., 2023）、基于梯度引导的扩散条件控制（Levy et al., 2023）以及仅在信号域进行低频替换的 ILVR（Choi et al., 2021）。它通过学习得到的潜在向量序列替代原始波形或 Mel 频谱作为表示域，对潜在序列应用 DFT/IDFT 进行频率操作，并采用基于对数坐标的相关频率 bin 随机阈值掩膜策略（RBF 核平滑），形成连续掩膜区域以控制任务难度。

实验表明，LATENTFT 在 MTG-Jamendo 条件生成任务上取得了 FAD 0.337（ILVR 为 1.124），响度相关性 0.834（ILVR 为 0.551）；在混合任务上 FAD 为 1.357（ILVR 为 2.696）。消融实验进一步验证了频率掩膜、bin 间相关性和对数频率轴缩放的关键作用——移除频率掩膜使 FAD 从 0.349 飙升至 5.341，取消相关性使 FAD 增至 2.744。听力研究也表明 LATENTFT 在音频质量和条件遵循度上获得了最多的头对头胜出。

该方法的主要局限在于推理需要多步扩散反推，无法实时交互；当前仅在短时片段（5.9 秒）上验证；潜在频谱的可解释性仅覆盖 genre、tempo、pitch 等有限属性。未来的开放问题包括能否支持流式频率控制、沿语义轴进一步解耦，以及扩展到更长音乐段落或其他时序模态。

音乐生成模型的核心挑战之一，是如何让用户以直观、可控的方式指定生成条件。现有主流方法——扩散模型、自回归模型、掩码语言模型——在条件生成上存在一个共同的瓶颈：它们以“粗到细”（coarse-to-fine）的方式运作，不同噪声级别或量化层级天然地耦合了时间尺度信息。这意味着，用户无法选择性地提取参考音频中特定时间尺度的模式（如仅保留节奏骨架而替换音色细节，或仅保留和弦进行而改变旋律走向）。

具体而言，现有条件生成范式存在以下缺口：

- **基于离散声学token的模型**（如Vampnet，Garcia et al., 2023）通过RVQ层进行粗到细控制，但不同量化层级对时间尺度的分离是隐式且耦合的——实验证据表明，在中层或细粒度RVQ层级上进行条件生成会导致音频质量急剧退化（Figure 13, Section B.5）。
- **基于梯度引导的扩散模型**（如Levy et al., 2023）使用可微目标函数引导反向扩散过程，但引导信号作用于全局，无法按时间尺度解耦。
- **ILVR**（Choi et al., 2021）在扩散反推过程中替换低频分量以保留大尺度结构，但其操作域是原始信号空间，频率分离能力受限于信号本身的频谱特性。
- **传统交叉合成**（Smith, 2011）在波形频谱上直接进行交叉混合，缺乏学习表征的灵活性。
- 对预训练音频编码器（DAC、RAVE）的潜在序列进行频域后处理，虽能引入频率维度，但编码器并未为频率解耦而优化，分离效果有限。

上述方法的共同缺陷在于：**它们缺乏一条显式、连续且可学习的频率轴来按时间尺度正交化音乐特征**。这导致三个关键能力缺失——（1）无法从参考音频中精确提取指定时间尺度的模式进行条件生成；（2）无法将两段音频在不同时间尺度上进行可控混合；（3）无法对潜在表征的频谱进行解释性分析，以理解不同音乐属性（genre、tempo、pitch等）在时间尺度上的分布。

本文的核心动机正是填补这一缺口：**能否设计一种方法，使得潜在空间中的频率轴成为时间尺度的直观代理，从而让用户通过简单的频谱掩膜即可实现对音乐模式的选择性提取与生成控制？** 这一动机直接催生了LATENTFT——将扩散自编码器与潜在空间傅里叶变换相结合，并引入频率掩膜训练策略，迫使编码器将不同时间尺度的音乐特征分离到不同的潜频率bin中。

## 核心方法与创新机理

LATENTFT 的核心创新在于将**扩散自编码器**与**潜在空间傅里叶变换**相结合，并通过**频率掩膜训练策略**，实现了音乐模式按时间尺度的正交分离。这一设计直接回应了现有方法的瓶颈：扩散模型、自回归模型、掩码语言模型等以粗到细方式运作，不同噪声级别或量化层级耦合了时间尺度信息，用户无法选择性提取参考音频中特定时间尺度的模式进行条件生成。

### 关键 changed slots

与基线方法相比，LATENTFT 在以下三个维度上做出了根本性改变：

| 维度 | 基线做法 | LATENTFT 做法 | 证据锚点 |
|------|----------|---------------|----------|
| **表示域** | 在原始音频波形或 Mel 频谱上操作（如 ILVR、Spectrogram 基线） | 通过学习得到的潜在向量序列 $z = \mathrm{Enc}_\phi(x_0)$ 作为操作对象 | Eq.2, Section 3.3 |
| **频率操作** | 无潜在频率操作，或直接在信号域进行掩膜/替换 | 对潜在序列应用 DFT 得到潜频谱 $Z = \mathrm{DFT}(z)$，在潜频谱上进行频率掩膜后再 IDFT 回时域 | Alg.1, Fig.2, Eq.3 |
| **训练掩膜策略** | 无掩膜，或随机屏蔽时间/频率块 | 基于对数坐标的相关频率 bin 随机阈值掩膜，通过 RBF 核 $K_{i,j} = c_i \exp\left(-\frac{|a_i - a_j|^p}{2\sigma^p}\right)$ 引入局部相关性，形成连续掩膜区域 | Section 3.4, Eq.4 |

### 创新机制：频率掩膜训练如何驱动解耦

LATENTFT 的核心因果机制可概括为：**在潜在序列的傅里叶域进行随机频率掩膜训练，迫使编码器将不同时间尺度的音乐特征分离到不同的潜频率 bin 中**。

具体而言，训练时随机掩膜部分潜频率分量，解码器（扩散模型）被迫仅从剩余频率分量中重建完整音频。这一信息瓶颈迫使编码器学习将语义模式沿频率轴正交排列——低频 bin 编码大尺度结构（如 genre、和弦进行），高频 bin 编码细粒度模式（如 tempo、pitch）。推理时，用户通过指定频谱掩膜即可沿这条连续的频率轴选择性提取所需时间尺度的特征，实现条件生成、混合与频谱解释。

消融实验提供了决定性证据：
- **移除频率掩膜**（w/o Freq. Masking）导致条件生成 FAD 从 0.349 升至 5.341，且各项 adherence 指标严重下降（Table 9），证明频率掩膜是训练信号的核心来源。
- **取消频率 bin 相关性**（w/o Correlation）使 FAD 增至 2.744（Table 9），表明连续掩膜区域（而非散点状随机掩膜）对于控制任务难度和促进泛化至关重要。
- **移除对数频率轴缩放**（w/o Log. Scale）降低音频质量（FAD 1.196）并削弱条件遵循能力（Table 9），说明对数尺度更符合音乐感知的倍频程特性。
- **消除编码器**直接在波形上掩膜（w/o Encoder）导致 adherence 急剧下降（Table 10），证明学习到的潜在表示对条件遵循是必要的。

### 与基线方法的本质区别

- **vs. ILVR**（Choi et al., 2021）：ILVR 在扩散反推过程中替换低频分量以保留大尺度结构，操作发生在信号域且仅支持低频保留。LATENTFT 在学习的潜在频率域操作，支持任意频段的选择性提取，且通过训练而非手工规则实现解耦。
- **vs. Masked Token Model / Vampnet**（Garcia et al., 2023）：基于 RVQ 层的粗到细控制将时间尺度与量化层级耦合，无法提供连续的频率轴。LATENTFT 的潜频谱提供了直观的连续频率轴，且生成质量在调节细粒度特征时不会退化（Fig.13）。
- **vs. Guidance**（Levy et al., 2023）：基于梯度的引导需要可微目标函数，无法直接实现“提取特定时间尺度模式”的条件控制。
- **vs. DAC/RAVE 潜在操作**：对预训练编码器的潜在序列进行频域后处理，但编码器未经过频率掩膜训练，潜频率 bin 未与时间尺度语义对齐，条件控制效果有限。

综上，LATENTFT 的创新不在于引入全新的模块类型，而在于**将 DFT 的频率分解能力与扩散自编码器的表示学习能力通过掩膜训练策略有机耦合**，创造出一条可解释、可操控的连续频率轴，使音乐生成中的时间尺度控制从隐式、耦合变为显式、正交。

LATENTFT 的核心 pipeline 由五个模块串联构成：**编码器 → 潜在傅里叶变换（DFT）→ 频率掩膜 → 逆傅里叶变换（IDFT）→ 解码器（扩散模型）**。整个流程在训练和推理阶段共享相同的前向通路，但掩膜策略和下游目标不同。

### 训练流程

给定输入音频 $\mathbf{x}_0 \in \mathbb{R}^{C \times T}$（Mel 频谱），编码器首先将其映射为潜在向量序列 $\mathbf{z} = \mathrm{Enc}_\phi(\mathbf{x}_0)$，其中 $\mathbf{z} \in \mathbb{R}^{C' \times T'}$，$T'$ 为潜在帧数，帧率 $f_r$ 由编码器下采样率决定。

随后，对 $\mathbf{z}$ 沿时间轴应用 DFT，得到复值潜频谱 $\mathbf{Z} = \mathrm{DFT}(\mathbf{z}) \in \mathbb{C}^{C' \times K}$，其中第 $k$ 个频率 bin 对应的潜在频率为 $f_k = k f_r / T'$ Hz。为提高频谱粒度，在 DFT 前对 $\mathbf{z}$ 末端补零，将时间长度扩展 $L$ 倍，使频率 bin 数增至 $\hat{F} = \lfloor L T' / 2 \rfloor + 1$。

训练时，系统在潜频谱上施加随机频率掩膜 $\mathbf{M} \in \{0,1\}^{\hat{F}}$。掩膜并非独立采样每个 bin，而是先为每个 bin 采样一个分数，再通过 RBF 核矩阵在**对数频率轴**上引入局部相关性，形成连续掩膜区域（Figure 8）。这一设计使模型必须从部分频率成分重建完整音频，迫使编码器将不同时间尺度的音乐特征分离到不同的潜频率 bin 中。

掩膜后的频谱经 IDFT 恢复为时域潜在序列 $\mathbf{z}^{\text{masked}}$，送入解码器。解码器以扩散模型形式工作：从正向扩散过程中采样噪声版本 $\mathbf{x}_\tau$ 和扩散时间 $\tau$，以 $\mathbf{z}^{\text{masked}}$ 为条件，估计干净输入 $\hat{\mathbf{x}}_0 = \mathrm{Dec}_\theta(\mathbf{z}^{\text{masked}}, \mathbf{x}_\tau, \tau)$。训练目标是最小化重建损失。

### 推理流程

推理时，频率掩膜 $\mathbf{M}$ 由用户指定，用于选择性提取参考音频中特定频率区间的模式。系统对参考音频执行相同的编码→DFT→掩膜→IDFT 流程，得到条件潜在序列 $\mathbf{z}^{\text{masked}}$。随后，解码器以 $\mathbf{z}^{\text{masked}}$ 为条件，从纯噪声出发执行多步扩散反推（Algorithm 2），生成与参考音频在指定时间尺度上一致、但在其他尺度上变化的变体。

混合任务（Algorithm 3）则对两段参考音频分别执行上述流程，得到两个频率掩膜后的潜在序列，将它们相加后送入解码器，实现跨时间尺度的特征融合。

### 关键设计决策

| 设计要素 | 作用 | 消融证据 |
|---------|------|---------|
| **频率掩膜训练** | 迫使编码器按时间尺度正交化特征 | 移除后条件生成 FAD 从 0.349 升至 5.341（Table 9） |
| **频率 bin 相关性** | 形成连续掩膜区域，避免琐碎解 | 取消相关性后 FAD 升至 2.744（Table 9） |
| **对数频率轴缩放** | 匹配音乐感知的倍频程特性 | 移除后 FAD 升至 1.196，adherence 下降（Table 9） |
| **编码器** | 将音频映射到可学习的表示域 | 消除编码器直接掩膜波形时 adherence 急剧下降（Table 10） |

> **注意**：上述消融数据均来自 Table 9 和 Table 10，其中 Mel-Cepstral Distortion（Timbre）指标已被除以 100 以便显示。

LATENTFT 的核心架构由五个模块串联构成：**编码器**、**潜在傅里叶变换（DFT）**、**频率掩膜**、**逆傅里叶变换（IDFT）** 和 **扩散解码器**。训练时，系统通过随机掩膜潜频谱迫使编码器将不同时间尺度的音乐模式分离到不同的潜频率 bin 中；推理时，用户通过指定频谱掩膜来选择性地提取参考音频中特定时间尺度的特征。

### 编码器

编码器将输入音频映射为潜在向量序列。输入 $x_0 \in \mathbb{R}^{C \times T}$ 可以是 Mel 频谱或原始波形，输出 $z \in \mathbb{R}^{C' \times T'}$：

$$z = \mathrm{Enc}_\phi(x_0)$$

其中 $T'$ 为潜在时间步数，$C'$ 为潜在通道数。论文训练了三种编码器变体：MLP 编码器、1D U-Net 编码器和基于 DAC（Descript Audio Codec）的波形编码器，以验证方法在不同表示域上的通用性。

### 潜在傅里叶变换

对潜在序列 $z$ 沿时间轴进行离散傅里叶变换，得到潜频谱 $Z \in \mathbb{C}^{C' \times K}$：

$$Z = \mathrm{DFT}(z)$$

第 $k$ 个频率 bin 对应的潜频率为 $f_k = k f_r / T' \ \mathrm{Hz}$，其中 $f_r$ 为潜帧率。这一变换将时域潜在表示分解为不同时间尺度的正弦分量，为后续的频率选择性操作提供了数学基础。DFT 和 IDFT 的标准定义如下：

$$X[k] = x \cdot w_k$$

$$x = \frac{1}{N} \sum_{k=0}^{N-1} X[k] w_k$$

其中 $w_k$ 为第 $k$ 个复正弦基向量。对于实值信号，可进一步表示为实正弦级数：

$$x[n] = \sum_{k=0}^{\lfloor N/2 \rfloor} A_k \cos(2\pi \frac{k}{N} n + \phi_k)$$

幅值 $A_k$ 和相位 $\phi_k$ 由 DFT 系数导出。论文通过 Figure 1 展示了这一分解过程。

### 频率掩膜策略

为提高频谱粒度，编码器输出 $z$ 在 DFT 前进行末端零填充，将时间长度扩展 $L$ 倍，使频率 bin 数增至 $\hat{F} = \lfloor L T' / 2 \rfloor + 1$。

训练时，掩膜 $M \in \{0,1\}^{\hat{F}}$ 随机生成。关键设计在于引入频率 bin 间的**局部相关性**，避免产生散点状孤立掩膜。具体地，首先为每个频率 bin 独立采样一个得分 $s_i \sim \mathcal{U}(0,1)$，然后通过径向基函数（RBF）核矩阵 $K \in \mathbb{R}^{\hat{F} \times \hat{F}}$ 进行平滑：

$$K_{i,j} = c_i \exp\left(-\frac{|a_i - a_j|^p}{2\sigma^p}\right)$$

其中 $a_i = \log(f_i + \epsilon)$ 为对数频率轴映射，$c_i$ 为行归一化系数（使每行 $\ell_2$ 范数为 1），$p$ 控制距离度量形式，$\sigma$ 控制相关性带宽。平滑后的得分 $\tilde{s} = K s$ 经阈值化得到二值掩膜。这一设计使得掩膜区域在频率轴上形成连续块（Figure 8），而非散点状噪声（Figure 7），对任务难度控制和泛化能力至关重要。

推理时，用户可直接指定 $M$，选择感兴趣频率区间的潜频率分量。

### 逆傅里叶变换与解码器

掩膜后的潜频谱经 IDFT 恢复为时域潜在序列 $z^{\text{masked}}$，作为解码器的条件输入。解码器采用扩散模型框架：训练时，对输入 $x_0$ 施加前向扩散过程得到噪声版本 $x_\tau$（$\tau \sim p(\tau)$ 为采样的扩散时间步），解码器以 $z^{\text{masked}}$、$x_\tau$ 和 $\tau$ 为条件，预测干净输入：

$$\hat{x}_0 \gets \mathrm{Dec}_\theta(z^{\text{masked}}, x_\tau, \tau)$$

推理时，解码器通过多步反向扩散生成音频。条件生成（Algorithm 2）使用单个参考音频的掩膜潜序列引导去噪过程；混合任务（Algorithm 3）则通过将两个参考音频的掩膜潜序列相加后送入解码器，实现不同时间尺度特征的融合。

### 模块间因果机制

整个流水线的核心因果链条可概括为：**频率掩膜训练 → 编码器被迫按时间尺度分离特征 → 潜频谱获得可解释的频率轴 → 推理时通过频谱掩膜实现选择性条件控制**。消融实验（Table 9）验证了这一链条的每个环节：移除频率掩膜使 FAD 从 0.349 升至 5.341；取消频率 bin 相关性使 FAD 增至 2.744；移除对数频率缩放使 FAD 升至 1.196 并削弱条件遵循能力；移除编码器则导致条件遵循指标急剧下降。

## 实验与关键发现

### 实验设置概览

作者在三个数据集上对 LATENTFT 进行了系统评估：**MTG-Jamendo**（超 55,000 首歌曲的大规模音乐集合，作为主实验平台）、**GTZAN**（多流派音乐数据集）和 **Maestro**（钢琴录音数据集）。模型训练了三个变体，分别采用不同的编码器架构：

- **LATENTFT-UNet**：基于 1D U-Net 的编码器，在 Mel 频谱上操作
- **LATENTFT-MLP**：轻量级 MLP 编码器，同样在 Mel 频谱上操作
- **LATENTFT-DAC**：使用预训练 DAC（Descript Audio Codec）作为前端，直接在原始音频波形上编码

所有变体共享相同的扩散解码器，训练时采用频率掩膜策略。推理时，解码器通过多步扩散反推过程生成音频（Alg. 2），最终由 BigVGAN 声码器将 Mel 频谱转换为波形。

基线方法覆盖了多种技术路线：基于离散 token 的 **Masked Token Model（Vampnet）**（Garcia et al., 2023）、基于梯度的扩散引导 **Guidance**（Levy et al., 2023）、在扩散反推中替换低频分量的 **ILVR**（Choi et al., 2021）、传统信号处理的 **Cross Synthesis**（Smith, 2011），以及对预训练编码器潜在序列进行频域后处理的 **DAC**（Kumar et al., 2023）和 **RAVE**。

---

### 主实验结果

**Table 1** 汇总了 MTG-Jamendo 测试集上条件生成与混合任务的核心指标。评价维度分为两类：**adherence（条件遵循度）**——包括响度相关性（Loudness Correlation）、节奏余弦相似度（Rhythmic Cosine Similarity）、音色失真（Mel-Cepstral Distortion，表中除以 100）、和声距离（Harmonic Distance）；以及**音频质量**——FAD（Fréchet Audio Distance，越低越好）。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_ogMxCjdCCq/figures/003_Table_1.jpg]]
*Table 1: Results on Conditional Generation and Blending on the MTG-Jamendo Test set. Mel-Cepstral Distortion (Timbre) is divided by 100. Compared to baselines, LATENTFT variants achieve superior adherence and audio quality. The Masked Token Model and Cross Synthesis baselines do not offer frequency-based controls, so we do not compute adherence. Cross Synthesis also only applies to the blending task*

#### 条件生成任务

在条件生成任务中，LATENTFT 的两个 Mel 频谱变体在所有 adherence 指标上均显著优于所有基线：

| 方法 | FAD (↓) | 响度相关 (↑) | 节奏相似 (↑) | 音色失真 (↓) | 和声距离 (↓) |
|------|---------|-------------|-------------|-------------|-------------|
| LATENTFT-UNet | **0.337** | **0.834** | **0.966** | 0.391 | 0.079 |
| LATENTFT-MLP | 0.349 | 0.815 | 0.963 | 0.376 | 0.079 |
| ILVR | 1.124 | 0.551 | 0.922 | 0.517 | 0.094 |
| Guidance | 4.723 | 0.607 | 0.850 | 0.803 | 0.147 |
| DAC | 3.960 | 0.525 | 0.848 | 1.010 | 0.163 |

LATENTFT-UNet 的 FAD（0.337）比最佳基线 ILVR（1.124）降低了 **0.787**，响度相关性从 0.551 提升至 0.834（+0.283）。这表明频率掩膜训练策略使模型能够更精准地从参考音频中提取指定时间尺度的模式，同时保持生成音频的高保真度。

值得注意的是，Masked Token Model 和 Cross Synthesis 不提供频率控制能力，因此在条件生成任务中未计算 adherence 指标。

#### 混合任务

在混合任务中，LATENTFT-UNet 同样取得了最佳综合表现：FAD 为 **1.357**，而 ILVR 为 2.696（降低 1.339）。Cross Synthesis 在混合任务中表现尚可（FAD 1.968），但 LATENTFT 在 adherence 上仍有明显优势。LATENTFT-DAC 变体在混合任务中 FAD 达到 0.854，音频质量甚至优于 UNet 变体，但其条件遵循能力较弱——这暗示直接在波形域编码可能引入更多高频细节，但牺牲了对指定频段的精确控制。

#### 跨数据集泛化

**Table 11**（GTZAN）和 **Table 12**（Maestro）验证了方法的跨数据集泛化能力。在 GTZAN 上，LATENTFT-MLP 的条件生成 FAD 为 0.844，显著优于 ILVR 的 1.873（降低 1.029）。即使在仅包含钢琴录音的 Maestro 数据集上，LATENTFT 仍保持了对基线的优势，证明频率掩膜策略学到的解耦表示不依赖于特定音乐风格或配器。

#### 主观听力研究

**Figure 3** 展示了成对比较听力研究的结果。在音频质量和条件遵循度两个维度上，LATENTFT 均获得了最多的 head-to-head 胜场。然而，作者也报告了评分者间一致性较低的问题（Fleiss's Kappa 约 0.07–0.09），说明音乐混合质量的主观评价存在较大个体差异——这是该领域评估的固有挑战。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_ogMxCjdCCq/figures/004_Figure_3.jpg]]
*Figure 3: Listening study Figure 4: Isolating frequencies from an electronic music clip. We with pairwise comparisons. show three audio spectrograms. The second spectrogram smooths the We achieve the most head-to- reference spectrogram, and the third accentuates patterns occurring at head wins on both criteria. 8 Hz while removing lower-frequency patterns, like the bass*

---

### 消融实验

消融实验（**Table 9** 和 **Table 10**）系统拆解了 LATENTFT 各核心组件的作用，揭示了几个关键因果机制。

#### 频率掩膜的核心地位

移除训练中的频率掩膜（w/o Frequency Masking）是最致命的消融：条件生成 FAD 从 0.349 飙升至 **5.341**，所有 adherence 指标严重恶化。这一结果直接证明了频率掩膜训练是迫使编码器将不同时间尺度的音乐特征分离到不同潜频 bin 中的关键机制——没有掩膜，模型退化为一个普通的扩散自编码器，无法在推理时通过频谱掩膜调节条件。

#### 频率 bin 相关性的必要性

取消频率 bin 间的局部相关性（w/o Correlation）——即使用独立的随机掩膜而非 RBF 核平滑的连续掩膜区域——使 FAD 增至 **2.744**。**Figure 7** 和 **Figure 8** 直观对比了两种掩膜策略：无相关性时掩膜呈散点状、无规律；有局部相关性时掩膜形成连续区域。连续掩膜区域对模型构成了更强的信息瓶颈，迫使编码器学习更鲁棒的时间尺度分离，同时避免模型利用孤立频率 bin 的泄漏信息“作弊”。

#### 对数频率轴缩放

移除对数频率轴缩放（w/o Log. Scale）使 FAD 升至 1.196，且条件遵循能力下降。对数缩放使得低频区域（对应大尺度音乐结构，如段落、和弦进行）获得更细粒度的频率分辨率，高频区域（对应细节纹理）获得较粗的分辨率——这与人类对音乐时间结构的感知特性一致。

#### 编码器的角色

消除编码器直接在波形 Mel 频谱上掩膜（w/o Encoder）的实验揭示了编码器的双重作用：在条件生成任务中，adherence 急剧下降，说明编码器对条件遵循是**必要的**；但在混合任务中，音频质量反而略微提升（FAD 0.854）。**Figure 9** 和 **Figure 10** 的频谱图示例直观展示了这一现象：编码器消融的生成结果虽然音频质量可接受，但几乎不遵循指定的频率条件。这表明编码器学到的潜在表示是频率选择性条件控制的关键载体，而原始 Mel 频谱的频域掩膜无法提供同等程度的语义解耦。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_ogMxCjdCCq/figures/018_Figure_9.jpg]]
*Figure 9: A conditional generation example, where we take 0.68–2.70 Hz from the latent spectrum of the reference (top left). LATENTFT generates a variation capturing the rhythmic pattern near 2 Hz. The frequency-masking, correlation, and log-scaling ablations also have a pattern near 2 Hz, but the audio quality is much worse. The encoder ablation does not follow the conditioning*

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_ogMxCjdCCq/figures/019_Figure_10.jpg]]
*Figure 10: A blending example, where we take 0–0.68 Hz from the first reference, and 10.78–43 Hz from the second reference. LATENTFT generates a variation that contains characteristics from both examples. For instance, the rapid rhythmic patterns of Reference 2 are retained, as well as the horizontal line from Reference 1. The correlation and log-scaling ablations retain some of these characteristics, while the encoder and frequency masking ablations ignore the references*

#### 移除 DFT 的影响

**Figure 12** 展示了同时移除训练和推理中 DFT 掩膜的结果：模型退化为直接基于完整潜在序列 z 的条件重建，生成的音频几乎与参考音频完全一致，丧失了生成变体的能力。这验证了 DFT 域的掩膜是引入可控变异的必要操作。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_ogMxCjdCCq/figures/023_Figure_12.jpg]]
*Figure 12: Mel-spectrograms where we remove the DFT during both training and inference. During inference, we condition the diffusion process on the full latent sequence z derived from a reference (left). This reconstructs the input without creating a variation (right)*

---

### 潜在频谱的可解释性

**Figure 5** 和 **Figure 11** 通过“保留曲线”（preservation curves）揭示了潜在频谱中不同频率 bin 与音乐语义属性的对应关系：

- **流派（genre）**：主要集中在 0 Hz 附近的极低频段，说明流派是全局性、大尺度的音乐特征
- **和弦进行（chord changes）**：同样位于低频段，与音乐结构的大尺度时间模式一致
- **速度（tempo）和音高（pitch）**：关联于较高的潜在频率，对应更细粒度的时间模式

**Figure 4** 展示了频率隔离的可视化示例：从一个电子音乐片段中，低频段（如 0–0.68 Hz）对应平滑的频谱包络和低频节奏，而 8 Hz 附近的频段则捕捉了更快速的节奏模式。这种按时间尺度的正交分离是 LATENTFT 方法的核心优势——与 Vampnet 等基于 RVQ 层的粗到细控制（**Figure 13**）相比，LATENTFT 在调节细粒度特征时仍能保持生成质量，而 Vampnet 在深层 RVQ 层的条件生成质量明显下降。

---

### 失败模式与局限性

1. **实时性不足**：推理需要多步扩散反推，无法实现实时交互，限制了现场音乐制作等应用场景。
2. **主观评价一致性低**：听力研究的 Fleiss's Kappa 仅 0.07–0.09，说明音乐混合质量的主观标准高度分散，量化评估体系有待完善。
3. **短时片段限制**：当前模型仅在 5.9 秒的短片段上训练和评估，扩展到长时生成可能面临跨段一致性问题——长音乐段落中不同时间尺度的模式可能跨越多个片段边界。
4. **语义解耦不完整**：潜在频谱的可解释性仅针对 genre、tempo、pitch、chord 等有限属性进行了验证，尚未覆盖所有语义轴（如音色、配器密度、情感表达等）。
5. **声码器依赖**：基于 Mel 频谱的解码依赖外部 BigVGAN 声码器，可能引入额外质量损失；端到端波形生成实验尚未展示，LATENTFT-DAC 变体的条件遵循能力不足也暗示了波形域编码的挑战。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_ogMxCjdCCq/figures/006_Table_2.jpg]]
*Table 2: MLP Encoder Architecture*

## 定位与知识库关联

### 核心瓶颈：现有方法的粗到细耦合与不可选择性

LATENTFT 针对的瓶颈是：现有音乐生成模型（扩散模型、自回归模型、掩码语言模型）在不同噪声级别或量化层级上耦合了时间尺度信息，用户无法**选择性**地提取参考音频中特定时间尺度的模式进行条件生成。具体而言：

- **Masked Token Model**（如 Vampnet，Garcia et al., 2023）基于离散声学 token，通过 RVQ 层进行粗到细控制，但不同量化层耦合了多个时间尺度，无法独立操控某一尺度。
- **Guidance**（基于梯度的扩散引导，Levy et al., 2023）使用可微目标函数引导扩散过程，但条件信号通过梯度注入，缺乏显式的频率解耦机制。
- **ILVR**（Iterative Latent Variable Refinement，Choi et al., 2021）在扩散反推过程中替换低频分量以保留大尺度结构，但仅在信号域操作，且无法灵活选择频率区间。
- **Cross Synthesis**（Smith, 2011）是传统信号处理技术，直接在波形频谱上进行交叉合成，缺乏学习到的语义表示。
- **DAC**（Kumar et al., 2023）和 **RAVE** 等方法对预训练编解码器的潜在序列进行后处理，但未在训练中引入频率掩膜，因此潜在空间未按时间尺度正交化。
- **Spectrogram** 基线直接在 Mel 频谱上应用频率掩膜，但 Mel 频带对应的是声学频率而非音乐时间尺度，无法实现语义级的尺度分离。

这些方法的共同局限在于：条件机制与时间尺度耦合，用户无法沿一条连续的频率轴自由选择“保留哪些时间尺度的音乐模式”。

### 核心洞察：潜在傅里叶域的频率掩膜训练

LATENTFT 的核心洞察是：**将扩散自编码器与潜在空间傅里叶变换相结合，引入频率掩膜训练策略，迫使编码器将不同时间尺度的音乐特征分离到不同的潜频率 bin 中**。这一设计提供了一条直观的连续频率轴，用于条件生成、混合与频谱解释。

方法的关键因果旋钮在于训练阶段的随机频率掩膜：编码器将输入音频映射为潜在向量序列 $z = \mathrm{Enc}_\phi(x_0)$（式 2），对该序列沿时间轴进行 DFT 得到潜频谱 $Z = \mathrm{DFT}(z)$（式 3），然后随机掩膜部分频率 bin，再由解码器从掩膜后的潜在序列重建音频。这一训练范式迫使编码器学习将不同时间尺度的音乐模式分配到不同的潜频率 bin 中——因为解码器必须仅从保留的频率成分中恢复完整音频，任何跨频率的信息泄漏都会导致重建失败。

推理时，用户通过指定频谱掩膜 $M$ 即可选择性地保留参考音频中特定潜频率的模式，其余频率由扩散模型的生成先验补全。这一机制实现了**按时间尺度的正交分离**，且频率轴是连续可调的（通过零填充实现频谱插值，提高频谱粒度）。

### 与基线方法的本质差异：表示域与操作域的迁移

LATENTFT 相对于基线方法的关键变化体现在三个维度：

| 维度 | 基线方法 | LATENTFT |
|------|---------|----------|
| **表示域** | 原始音频波形或 Mel 频谱 | 学习到的潜在向量序列（编码器输出） |
| **频率操作** | 无潜在频率操作，或直接在信号域掩膜 | 对潜在序列应用 DFT，在潜频谱上进行频率掩膜，再 IDFT 回时域 |
| **训练掩膜策略** | 无掩膜，或随机屏蔽时间/频率块 | 基于对数坐标的相关频率 bin 随机阈值掩膜（RBF 核平滑，式 4） |

其中，**表示域的迁移**是根本性的：直接在波形或 Mel 频谱上掩膜（Spectrogram 基线）无法实现语义级的尺度分离，因为声学频率与音乐时间尺度之间不存在简单映射。编码器将音频映射到学习到的潜在空间后，DFT 分解的“频率”对应的是潜在序列的变化速率，而非声学频率，这使得潜频率 bin 可以承载节奏、和弦变化、音高等语义属性。

**频率掩膜策略**同样关键：消融实验表明，移除频率掩膜（w/o Freq. Masking）导致条件生成 FAD 从 0.349 升至 5.341，且各项 adherence 指标严重下降（Table 9）。取消频率 bin 相关性（w/o Correlation）使 FAD 增至 2.744，表明基于 RBF 核的连续掩膜区域（而非散点状随机掩膜）对于控制任务难度和促进泛化至关重要。

### 适用边界与局限

1. **推理延迟**：推理过程需要多步扩散反推，无法实时交互，可能限制现场音乐制作应用。
2. **主观评价一致性低**：听力研究的评分者间一致性较低（Fleiss's Kappa 约 0.07–0.09），表明音乐混合质量的评价高度主观，定量指标与人类偏好之间的对应关系仍需进一步验证。
3. **短时片段限制**：当前实现仅在 5.9 秒的音乐片段上训练和评估，扩展到长时生成时可能面临跨段一致性问题。
4. **可解释性覆盖有限**：潜在频谱的可解释性仅针对 genre、tempo、pitch、chord 等有限属性进行了验证，尚未覆盖所有语义轴（如音色、表现力等）。
5. **声码器依赖**：基于 Mel 频谱的解码依赖外部声码器（BigVGAN），可能引入额外质量损失；端到端波形生成实验尚未展示。

### 开放问题

1. **实时交互**：能否通过蒸馏或单步生成方法支持实时或流式频率控制？
2. **语义解耦深化**：潜在频谱能否进一步沿语义轴解耦（如音高、节奏、音色），实现更精细的独立编辑？
3. **长时生成扩展**：方法能否扩展到更长音乐段落，或应用于视频、语音等其他时序模态？
4. **自适应掩膜策略**：是否可能引入自适应或可学习的频率掩膜策略，以进一步减少信息泄漏并提高鲁棒性？
5. **混合相干性保证**：如何量化并保证混合时不同段的相干性，避免不自然的拼接？

## 原文 PDF

![[paperPDFs/ICLR_2026/Latent_Fourier_Transform.pdf]]
