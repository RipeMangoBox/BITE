---
title: "MoLingo: Motion-Language Alignment for Text-to-Human Motion Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MoLingo_Motion_Language_Alignment_for_Text_to_Human_Motion_Generation.pdf
project_link: https://hynann.github.io/molingo/MoLingo.html
aliases:
- MoLingo
tags:
- CVPR_2026
- topic/text_to_motion
- topic/motion_language_alignment
- topic/semantic_latent_space
- topic/cross_attention
- topic/text_to_motion/general
core_operator: "通过帧级文本标签的余弦相似度损失实现语义对齐的潜在空间；使用多 token 交叉注意力替代单 token 条件化，显著增强文本条件化强度。"
primary_logic: "语义对齐使潜在空间更具扩散友好性，而多 token 交叉注意力提供了更强的文本条件化；两者结合大幅提升了动作真实感和文本-动作对齐性能。"
claims:
- "多 token 交叉注意力 (CrossAttn) 相比单 token 调制 (AdaLN) 显著提高 R-Precision 和 CLIP-Score，同时降低 FID。"
- "语义对齐自动编码器 (SAE) 在文本-动作对齐指标上一致优于普通 AE 和 VAE。"
- "MoLingo 在多个评估协议 (MARDM-67, TMR-263, MS-272) 上均达到最先进的 FID 和 R-Precision。"
- "在用户研究中，MoLingo 相比 DisCoRD、MoMask、MotionStreamer 分别获得 83.75%、77.70%、84.70% 的偏好率。"
---

# MoLingo: Motion-Language Alignment for Text-to-Human Motion Generation

> [!tip] 核心洞察
> 语义对齐使潜在空间更具扩散友好性，而多 token 交叉注意力提供了更强的文本条件化；两者结合大幅提升了动作真实感和文本-动作对齐性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | MoLingo：面向文本到人体运动生成的运动-语言对齐 |
| 英文题名 | MoLingo: Motion-Language Alignment for Text-to-Human Motion Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.13840); [Project](https://hynann.github.io/molingo/MoLingo.html) |
| Topic | #topic/text_to_motion #topic/motion_language_alignment #topic/semantic_latent_space #topic/cross_attention #topic/text_to_motion/general |
| Method | Semantically aligned autoencoder, multi-token cross-attention, masked autoregressive rectified flow |
| Dataset | HumanML3D, BABEL, MARDM-67 evaluator, TMR-263 evaluator, MS-272 evaluator |

> [!tip] 效果简介
> - MARDM-67 上，FID 为 0.049 (VAE) / 0.064 (SAE)，对比 0.053 (DisCoRD) / 0.058 (ACMDM-XL-PS2)，变化 -0.004 (vs DisCoRD)。
> - MARDM-67 上，R-Precision Top-1 为 0.542 (SAE)，对比 0.522 (ACMDM-XL-PS2)，变化 +0.020。
> - TMR-263 上，FID 为 0.014，对比 0.022 (MoMask)，变化 -0.008。

## 概述

**核心问题**：现有文本到人体运动生成方法在连续潜在空间中缺乏语义对齐，且普遍采用单 token 条件化（如 AdaLN 调制），导致生成的运动难以精确遵循文本指令，在真实感和语义一致性上存在瓶颈。

**核心方案**：MoLingo 提出两个关键改进——(1) **语义对齐自动编码器 (SAE)**，利用 BABEL 数据集的帧级文本标签，通过余弦相似度损失将运动潜在与文本语义在潜在空间中对齐，使潜在空间更具扩散友好性；(2) **多 token 交叉注意力 (CrossAttn)** 替代传统单 token 调制，配合 T5-Large 文本编码器，显著增强文本条件化强度。在此基础上，采用掩码自回归 Transformer 与整流流 (Rectified Flow) MLP 在连续潜在空间中进行去噪生成。

**方法定位**：MoLingo 属于连续潜在空间的自回归流模型，区别于 VQ 离散潜在方法（如 **MoMask**、**DisCoRD**）和单 token 条件化的连续潜在方法（如 **MARDM**、**MotionStreamer**、**ACMDM**）。其语义对齐策略在自动编码器训练阶段引入显式的跨模态监督，是区别于普通 AE/VAE 的关键设计。

**主要结果**：在 MARDM-67 评估协议上，MoLingo (SAE) 取得 FID 0.064、R-Precision Top-1 0.542，MoLingo (VAE) 取得 FID 0.049；在 TMR-263 上 FID 低至 0.014；在 MS-272 上 FID 为 3.444（对比 MotionStreamer 的 11.979）。用户研究中，MoLingo 相较 DisCoRD、MoMask、MotionStreamer 分别获得 83.75%、77.70%、84.70% 的偏好率。消融实验证实多 token 交叉注意力和语义对齐各自带来显著且一致的性能增益。

## 背景与动机

### 问题背景

文本到人体运动生成的目标是根据自然语言描述合成逼真的 3D 人体动作序列。这一任务在动画制作、游戏开发、虚拟现实和人机交互等领域具有广泛应用。近年来，扩散模型和自回归模型在运动生成领域取得了显著进展，但现有方法仍面临两个核心瓶颈：

1. **连续潜在空间缺乏语义对齐**：当前主流的运动生成方法通常将运动序列编码到连续潜在空间中进行建模，但该潜在空间的构造仅依赖重建损失，缺乏显式的语义监督。这导致语义相似的运动在潜在空间中可能相距甚远，使潜在空间对生成模型不够“友好”，增加了扩散或自回归建模的难度。

2. **单 token 条件化表达能力不足**：现有方法普遍将文本提示压缩为单一全局向量（如 CLIP 嵌入），再通过 AdaLN 等调制机制注入生成过程。这种单 token 条件化方式丢失了文本中的细粒度语义信息，导致生成的运动难以精确遵循文本指令中的细节描述。

### 现有方法缺口

表 1 总结了当前主流方法在文本条件化和潜在空间设计上的典型方案：

- **MARDM** 采用连续潜在自回归扩散框架，使用 CLIP 文本编码器的单 token 输出通过 AdaLN 调制生成过程，潜在空间由普通 VAE 构建。
- **MotionStreamer** 采用连续潜在自回归流模型，同样依赖单 token 条件化，且潜在空间缺乏语义监督。
- **DisCoRD** 和 **MoMask** 转向 VQ 离散潜在空间，通过码本离散化间接缓解了连续空间的对齐问题，但离散化本身引入了信息损失和训练复杂度。
- **ACMDM** 在连续潜在空间中引入自回归扩散，但文本条件化机制和潜在空间设计与 MARDM 类似，未能根本解决语义对齐问题。

这些方法的共同缺陷在于：**文本条件化过于粗糙**（单 token 调制），且**潜在空间构造缺乏文本语义引导**。这导致生成的运动在真实感（FID）和文本-动作对齐（R-Precision、CLIP-Score）两个维度上难以同时达到最优。

### 本文动机

针对上述瓶颈，MoLingo 从两个关键维度对现有框架进行系统性改进：

1. **语义对齐的潜在空间**：提出语义对齐自动编码器（SAE），利用 BABEL 数据集提供的帧级文本标签，通过余弦相似度损失显式地将运动潜在与其对应语义类 token 对齐。这使得语义相似的运动帧在潜在空间中自然聚集，为后续生成模型提供更“扩散友好”的潜在表示。

2. **多 token 交叉注意力条件化**：将文本编码器从 CLIP 升级为 T5-Large，并通过文本适配器将文本提示编码为多 token 嵌入序列。在生成过程中，使用交叉注意力（CrossAttn）替代单 token 的 AdaLN 调制，使模型能够细粒度地关注文本中的不同语义单元，显著增强文本条件化强度。

这两项改进的因果关系清晰：语义对齐降低了潜在空间的结构复杂度，使生成模型更容易学习；多 token 交叉注意力则提供了更强的条件信号，使生成的运动更精确地遵循文本指令。两者协同作用，在运动真实感和文本-动作对齐两个维度上均实现了显著提升。

## 核心创新

MoLingo 的核心创新围绕两个相互协同的**关键因果旋钮**展开：**语义对齐的连续潜在空间**与**多 token 交叉注意力条件化机制**。这两个设计分别解决了现有文本到动作生成方法在潜在空间语义表达能力和文本条件化强度上的瓶颈，共同驱动了运动真实感和文本-动作对齐性能的显著提升。

### 创新一：语义对齐自动编码器 (SAE)

现有方法通常采用普通 AE 或 VAE 对运动序列进行压缩编码，其潜在空间缺乏显式的语义结构，导致语义相似的文本难以映射到相邻的潜在区域，增加了扩散模型的建模难度。MoLingo 的 SAE 通过引入**帧级文本标签的余弦相似度损失**，将语义监督直接注入潜在空间训练中（Figure 2）。

具体而言，SAE 利用 BABEL 数据集提供的帧级文本标注，为每个运动潜在 $m_i$ 构建对应的类 token $\kappa_i$，并通过语义损失拉近二者的余弦距离：

$$\mathcal{L}_{\mathrm{sem}} = \frac{1}{|\mathcal{T}|}\sum_{i\in\mathcal{I}}\left(1 - \frac{\boldsymbol{m}_i \cdot \boldsymbol{\kappa}_i}{\Vert\boldsymbol{m}_i\Vert \Vert\kappa_i\Vert}\right)$$

其中 $\mathcal{I}$ 为过滤了相邻重复类 token 的索引集，这种过滤策略作为软语义正则器，有效避免了过度对齐。SAE 的最终训练目标融合了重建损失、语义损失和 KL 散度：

$$\mathcal{L}_{\mathrm{SAE}} = \mathcal{L}_{\mathrm{recon}} + \lambda_{\mathrm{sem}}\mathcal{L}_{\mathrm{sem}} + \lambda_{\mathrm{KL}}\mathcal{L}_{\mathrm{KL}}$$

消融实验（Table 3）证实，余弦相似度损失配合较小权重 ($\lambda_{\mathrm{sem}}=0.001$) 及 KL 正则化，在 R-Precision 和 CLIP-Score 上达到最佳性能，显著优于 InfoNCE 等替代方案。

**证据强度**：Table 2 显示，SAE 在所有文本-动作对齐指标上一致优于普通 AE 和 VAE，R-Precision Top-1 达到 0.542，CLIP-Score 达到 0.686，同时保持具有竞争力的 FID (0.064)。该结论在 MARDM-67、TMR-263、MS-272 三个独立评估协议下均得到验证（Table 1, 7, 8）。

### 创新二：多 token 交叉注意力条件化

现有连续潜在方法（如 **MARDM**）普遍采用单 token 调制 (AdaLN)，将文本嵌入压缩为单一向量进行条件化，表达能力严重受限。MoLingo 改用**多 token 交叉注意力 (CrossAttn)** 机制，使生成模型能够细粒度地关注文本序列中的不同语义单元。

该机制与 T5-Large 文本编码器及可训练的文本适配器配合使用：冻结的 T5-Large 将文本提示编码为嵌入序列，随后通过可配置层数的 Transformer 文本适配器进一步增强跨模态交互能力，最终通过交叉注意力注入自回归 Transformer 的条件向量生成过程（Figure 3）。

**证据强度**：Table 2 的消融实验直接对比了 CrossAttn (T5+SAE) 与 AdaLN (CLIP) 的性能差异。CrossAttn 在所有指标上均显著优于 AdaLN，尤其在 R-Precision 和 CLIP-Score 上提升明显。值得注意的是，即使不引入 SAE，仅将条件化机制从 AdaLN 切换为 CrossAttn (T5+VAE)，FID 即可从 0.053 降至 0.049，验证了多 token 条件化本身的独立增益。

### 协同效应与架构定位

两项创新的协同效应体现在：语义对齐使潜在空间更具扩散友好性，降低了生成模型的学习难度；而多 token 交叉注意力提供了更强的文本条件化信号，使模型能更精确地遵循文本指令。两者结合使 MoLingo 在 MARDM-67 评估器上达到 FID 0.064 (SAE) / 0.049 (VAE)，R-Precision Top-1 0.542，显著超越 **DisCoRD**、**ACMDM**、**MoMask** 等代表性基线（Table 1）。

在方法谱系上，MoLingo 属于**连续潜在空间的自回归流模型**，其生成过程通过链式法则分解联合分布：

$$p(m_1,\ldots,m_l) = \prod_{i=1}^l p(m_i \mid c, m_1, \ldots, m_{i-1})$$

条件向量 $z_i$ 由掩码自回归 Transformer 预测，随后通过整流流 MLP 对潜在进行迭代去噪。这一设计既保留了连续潜在空间的高保真重建能力，又通过自回归机制捕获了运动序列的时序依赖。

**需要人工验证的点**：SAE 的语义对齐训练仅利用了 BABEL 与 HumanML3D 的交集部分，帧级文本监督的覆盖范围受限。这一限制对更广泛动作类别上语义对齐效果的具体影响程度，在现有消融实验中未做定量评估，需结合更大规模标注数据集进一步验证。

## 整体框架

MoLingo 的整体框架由两大核心组件构成：**语义对齐运动自动编码器** 与 **掩码自回归整流流生成器**。前者将原始运动序列压缩为连续潜在表示，并通过帧级文本监督实现语义对齐；后者以文本提示为条件，自回归地预测条件向量，再通过整流流在潜在空间中迭代去噪，最终解码为运动帧。图 2 与图 3 分别展示了这两个组件的数据流与模块关系。

**输入与输出流**：给定文本提示 $c$，系统首先通过冻结的 T5-Large 编码器将其映射为文本嵌入序列，再经可训练的文本适配器（Transformer 编码器块）进一步处理，以增强跨模态交互能力。同时，运动序列 $\mathbf{m}_{1:N} \in \mathbb{R}^{N \times D}$ 经 1D 卷积编码器压缩为潜在序列 $m_{1:l} \in \mathbb{R}^{l \times d}$，其中 $l = N/h$，$h$ 为时序下采样率。生成阶段，掩码自回归 Transformer 以文本嵌入和已生成的潜在为条件，逐 token 预测条件向量 $z_i$；整流流 MLP 则依据 $z_i$ 和时间步 $t$ 对噪声潜在进行去噪。最终，去噪后的潜在序列由 1D 卷积解码器重建为运动帧。

**模块间关系**：语义对齐自动编码器（SAE）与生成器是解耦训练的——先独立训练 SAE 获得语义对齐的潜在空间，再固定编码器/解码器，仅训练生成器。SAE 内部引入了一条并行的文本编码分支：利用 BABEL 数据集的帧级文本标签，通过可学习的类 token 将文本语义注入潜在空间，以余弦相似度损失 $\mathcal{L}_{\mathrm{sem}}$ 拉近运动潜在 $m_i$ 与对应类 token $\kappa_i$ 的距离（公式见 Eq.(1)）。同时，SAE 的总损失 $\mathcal{L}_{\mathrm{SAE}}$ 还包含重建损失 $\mathcal{L}_{\mathrm{recon}}$（特征、关节位置、关节速度的加权和）与 KL 散度项 $\mathcal{L}_{\mathrm{KL}}$（公式见 Eq.(5)）。

**生成器的关键设计**：生成器采用链式法则将联合分布分解为条件概率的乘积 $p(m_1,\ldots,m_l) = \prod_{i=1}^l p(m_i \mid c, m_1, \ldots, m_{i-1})$（Eq.(6)），实现自回归生成。训练时随机掩码部分潜在 token 并替换为可学习 token，推理时从全掩码状态初始化，逐 token 去噪。整流流损失（Eq.(7)）训练 MLP 学习从噪声到干净潜在的速度场。此外，模型采用无分类器引导（CFG），训练时以 10% 概率将文本提示替换为空提示，推理时 CFG 尺度设为 6.0。

**两种变体**：MoLingo 提供 VAE 变体（无显式语义监督）与 SAE 变体（引入帧级语义对齐）。SAE 变体在文本-动作对齐指标上更优，而 VAE 变体在 FID 上略占优势——这一权衡在消融实验（Table 2）中得到系统分析。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2512_13840/figures/002_Figure_2.jpg]]
*Figure 2: Semantically aligned autoencoder architecture. The model comprises an encoder–decoder autoencoder for motion sequences and a parallel text-encoding branch that maps frame-level text labels into class tokens. A cosine-similarity loss $\mathcal { L } _ { \mathrm { s e m } }$ is applied to align the motion latents with their corresponding class tokens

## 核心模块与公式推导

MoLingo 的整体框架由两个关键组件构成：**(1) 语义对齐运动自动编码器 (SAE)**，负责将运动序列映射到语义对齐的连续潜在空间；**(2) 基于掩码自回归整流流的生成模型**，在该潜在空间中进行条件生成。

### 语义对齐自动编码器 (SAE)

SAE 的核心创新在于将帧级文本语义显式注入潜在空间的学习过程。给定运动序列 $\mathbf{m}_{1:N}$，编码器通过 1D 卷积将其压缩为潜在序列 $m_{1:l} \in \mathbb{R}^{l \times d}$，其中 $l = N / h$，$h$ 为时间下采样因子。并行地，文本编码分支利用 BABEL 数据集提供的帧级文本标签，将每个运动帧对应的文本标签映射为类 token $\kappa_i$。

语义对齐的核心是余弦相似度损失，其定义为：

$$\mathcal{L}_{\mathrm{sem}} = \frac{1}{|\mathcal{T}|}\sum_{i\in\mathcal{I}}\left(1 - \frac{\boldsymbol{m}_i \cdot \boldsymbol{\kappa}_i}{\Vert\boldsymbol{m}_i\Vert \Vert\kappa_i\Vert}\right)$$

其中 $\mathcal{I}$ 是经过相邻重复类 token 过滤后的索引集。过滤机制通过计算相邻类 token 的相似度 $\Delta_i = \langle \kappa_i, \kappa_{i+1} \rangle$，并丢弃 $\Delta_i$ 超过阈值 $\tau$ 的 token 对，作为软语义正则器，避免对静态动作的过度约束（Table 6 验证了该过滤对 FID 和检索分数的一致改善）。

SAE 的总损失函数为：

$$\mathcal{L}_{\mathrm{SAE}} = \mathcal{L}_{\mathrm{recon}} + \lambda_{\mathrm{sem}}\mathcal{L}_{\mathrm{sem}} + \lambda_{\mathrm{KL}}\mathcal{L}_{\mathrm{KL}}$$

其中重建损失 $\mathcal{L}_{\mathrm{recon}}$ 由三项加权组成：

$$\mathcal{L}_{\mathrm{recon}} = \mathcal{L}_{\mathrm{feat}} + \lambda_{\mathrm{joint}}\mathcal{L}_{\mathrm{joint}} + \lambda_{\mathrm{vel}}\mathcal{L}_{\mathrm{vel}}$$

- **特征损失**：$\mathcal{L}_{\mathrm{feat}} = \|\mathbf{m} - \mathcal{D}(m)\|_2^2$，约束原始运动表示与解码运动表示之间的 L2 距离。
- **关节位置损失**：$\mathcal{L}_{\mathrm{joint}} = \|\mathcal{T}(\mathbf{m}) - \mathcal{T}(\mathcal{D}(m))\|_2^2$，约束原始与重建关节位置的一致性，$\mathcal{T}$ 为运动表示到关节位置的转换函数。
- **速度损失**：$\mathcal{L}_{\mathrm{vel}} = \frac{1}{N-1}\sum_{n=1}^{N-1}\left\|\left(\mathcal{T}(\mathbf{m})_{n+1} - \mathcal{T}(\mathbf{m})_n\right) - \left(\mathcal{T}(\mathcal{D}(m))_{n+1} - \mathcal{T}(\mathcal{D}(m))_n\right)\right\|_2^2$，确保重建运动的动态一致性。

$\mathcal{L}_{\mathrm{KL}}$ 为标准 VAE 的 KL 散度正则项，约束潜在分布接近先验。消融实验（Table 3）表明，采用余弦相似度损失、配合小权重 $\lambda_{\mathrm{sem}}=0.001$ 及 KL 正则化，在 R-Precision 和 CLIP-Score 上达到最佳性能，显著优于 InfoNCE 等其他配置。

### 掩码自回归整流流生成

生成模型采用自回归方式对潜在序列进行条件建模，利用链式法则分解联合分布：

$$p(m_1,\ldots,m_l) = \prod_{i=1}^l p(m_i \mid c, m_1, \ldots, m_{i-1})$$

**文本条件化**：输入文本提示 $c$ 首先通过冻结的 T5-Large 编码器获得嵌入序列，再经过 $l_{ad}$ 层 Transformer 编码器构成的文本适配器进行跨模态增强。消融实验（Table 5）显示 6 层适配器获得最佳的 FID 与 R-Precision 权衡。随后，掩码自回归 Transformer 解码器以自注意力处理已生成的潜在序列，并通过交叉注意力（CrossAttn）与多 token 文本嵌入交互，输出条件向量 $z_i$。

**整流流去噪**：条件向量 $z_i$ 引导 MLP 网络 $v_\theta$ 在连续潜在空间中执行整流流去噪，其训练损失为：

$$\mathcal{L}(z_i, m_i) = \mathbb{E}_{m_i, \epsilon, t}\left[\|v_\theta(m_i^t, t, z_i) - \dot{\alpha}_t m_i - \dot{\sigma}_t \epsilon\|^2\right]$$

其中 $m_i^t = \alpha_t m_i + \sigma_t \epsilon$ 为加噪后的潜在，$\epsilon \sim \mathcal{N}(0, I)$，$t$ 为时间步。该损失训练网络学习从噪声到干净潜在的速度场。训练时采用随机掩码策略，将部分潜在替换为可学习 token；推理时从全掩码状态初始化，逐步去噪生成完整潜在序列，最终由运动解码器恢复为运动帧。

**关键设计对比**：Table 2 的消融实验验证了两个核心设计选择的有效性——多 token 交叉注意力（CrossAttn）相比单 token AdaLN 调制在所有指标上均有显著提升，尤其 R-Precision Top-1 从 0.528 提升至 0.542；SAE 相比普通 AE/VAE 在文本-动作对齐指标上持续改善，验证了语义对齐潜在空间的扩散友好性。

## 实验与分析

### 核心瓶颈与因果机制

现有文本到动作生成方法面临两个关键瓶颈：**(1)** 连续潜在空间缺乏显式的语义对齐，导致生成的动作难以精确遵循文本指令；**(2)** 单 token 条件化（如 DiT 风格的 AdaLN 调制）表达能力不足，无法充分捕捉复杂文本提示的细粒度语义。MoLingo 通过两个因果调节变量解决上述问题：**语义对齐自动编码器（SAE）** 利用 BABEL 数据集的帧级文本标签，通过余弦相似度损失将运动潜在与对应语义 token 拉近，使潜在空间更具扩散友好性；**多 token 交叉注意力（CrossAttn）** 替代单 token 调制，显著增强文本条件化强度。两者协同作用下，模型在运动真实感和文本-动作对齐两个维度上均取得大幅提升。

### 主实验结果

**MARDM-67 评估协议**（Table 1）是文本到动作生成领域最广泛使用的基准之一。MoLingo 的 SAE 变体在 FID 上达到 0.064，R-Precision Top-1 达到 0.542，CLIP-Score 达到 0.686，三项指标均取得最优。VAE 变体则取得最佳 FID 0.049，略优于 DisCoRD（FID 0.053）和 ACMDM-XL-PS2（FID 0.058）。这表明语义对齐在提升文本-动作对齐的同时，VAE 变体在保真度上具有微弱优势——两者构成互补。

**TMR-263 评估协议**（Table 8）上，MoLingo 的 FID 低至 0.014，显著优于 MoMask（FID 0.022）等 VQ 离散潜在方法，同时在 R-Precision 和 MultiModality 上均达到最优。这说明连续潜在空间配合整流流去噪在运动多样性上同样具有竞争力。

**MS-272 评估协议**（Table 7）上，MoLingo 的 FID 为 3.444，相比 MotionStreamer 的 11.979 降低了 8.535，幅度极为显著。该评估使用 MotionStreamer 原生的 272D 运动表示和官方评估器，确保了比较的公平性。值得注意的是，MoLingo 通过将第一层 1D 卷积的 padding 模式改为复制初始帧，稳定了训练并改善了重建质量（Table 9），这一细节调整对 272D 表示下的性能提升起到了关键作用。

**用户研究**（Section 4.3）进一步验证了上述量化结果：在成对比较中，MoLingo 相比 DisCoRD、MoMask、MotionStreamer 分别获得 83.75%、77.70%、84.70% 的偏好率，表明人类评估者一致认为 MoLingo 生成的动作更自然且更符合文本描述。

### 消融实验分析

**条件化机制与自动编码器类型**（Table 2）是最核心的消融。以 T5 为文本编码器时，CrossAttn 相比 AdaLN 在 FID 上从 0.058 降至 0.049（VAE）和 0.064（SAE），R-Precision Top-1 从 0.515 提升至 0.528（VAE）和 0.542（SAE），CLIP-Score 从 0.660 提升至 0.672（VAE）和 0.686（SAE）。多 token 交叉注意力在所有指标上一致优于单 token 调制，且提升幅度在文本-动作对齐指标上尤为显著。同时，SAE 相比 AE 和 VAE 在 R-Precision 和 CLIP-Score 上持续提升，验证了语义对齐对文本条件化的增强作用。

**SAE 配置消融**（Table 3）揭示了三项关键设计选择的影响：**(1)** 余弦相似度损失优于 InfoNCE 损失，在 R-Precision Top-1 上提升约 0.01；**(2)** KL 散度正则化对维持生成多样性至关重要，移除后 FID 显著恶化；**(3)** 语义损失权重 λ_sem=0.001 取得最佳平衡，过大权重会损害重建质量。最优配置（余弦相似度 + KL + λ_sem=0.001）在 R-Precision Top-1 达到 0.542，CLIP-Score 达到 0.686，同时 FID 保持在 0.064。

**文本适配器深度**（Table 5）的消融表明，6 层 Transformer 编码器块作为文本适配器取得了最佳的 FID 与 R-Precision 权衡。无适配器时性能明显下降，而 9 层适配器并未带来额外收益，说明适度的跨模态交互处理已足够。

**重复类 token 过滤**（Table 6）作为软语义正则器，过滤相邻相似度超过阈值 τ 的重复类 token 后，FID 和检索分数均得到一致改善。这一机制避免了过强的语义对齐导致潜在空间坍缩。

**潜在维度与时序下采样**（Figure 5）的分析显示，4× 时序压缩（即一个潜在向量对应 4 帧运动）在多数配置下与 2× 压缩性能相当甚至更优，表明更大的时序感受野有利于单个潜在向量捕获更完整的运动语义。

### 定性分析与失败模式

**Figure 4** 的定性对比展示了 MoLingo 相比 MARDM、ACMDM 和 MotionStreamer 的优势：MoLingo 生成的动作更自然且准确遵循文本指令，而其他方法要么无法捕捉细粒度语义，要么出现动作坍缩。**Figure 6** 进一步将 MoLingo 与 RL 跟踪控制器结合，展示了其在足部-地面交互上的改进——MoLingo 生成的运动具有一致的真实接触行为，而 MotionStreamer 频繁出现平衡伪影。

**已知局限**：语义对齐训练仅利用了 BABEL 与 HumanML3D 的交集部分，帧级文本监督的覆盖范围受限，可能影响在更广泛动作类别上的语义对齐效果。当前方法尚未扩展到包含手部细节的全身运动生成。评估指标（FID、R-Precision 等）虽被广泛使用，但可能无法完全捕捉人类对运动质量和语义一致性的感知，用户研究虽部分弥补了这一不足，但规模有限。

### 公平性说明

所有实验均报告 20 次独立运行的均值及 95% 置信区间。在 MS-272 比较中，MoLingo 使用与 MotionStreamer 相同的 272D 数据训练，并采用其官方评估器。基线方法的数值来自原论文或使用相同数据重新运行得到的官方结果，确保了比较的公平性。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2512_13840/figures/001_Figure_1.jpg]]
*Figure 1: Left: Given text prompts, MoLingo generates realistic and text-aligned motions, ranging from daily movements like sweeping to more challenging movements like dancing. Right: MoLingo significantly outperforms previous works in both FID and R-Precision scores. The difference can best be seen in motion, hence we urge the reader to view the supplementary video*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2512_13840/figures/008_Figure_5.jpg]]
*Figure 5: Effect of latent dimension and temporal downsampling. We vary the latent dimension (16–128) under two temporal compression settings: (4×) and (2×). Overall, the 4× setting gives comparable or better performance than 2×, showing that is beneficial that a single latent encodes 4 frame, even 2× preserves more fine-grained temporal information*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2512_13840/figures/004_Table_1.jpg]]
*Table 1: Quantitative results on the MARDM-67 evaluator. We compare our method with a broad set of motion generation approaches, from early models [6, 53] to recent ones [19, 40], covering pose-frame diffusion [53], single-vector latent diffusion [6, 9], VQ-based next-token prediction [7, 18, 19, 44, 45, 65], and continuous-valued auto-regressive models [39, 40]. We report the mean results over 20 independent runs, and the ± values indicate the 95% confidence interval. Our method achieves state-of-the-art FID, R-Precision, and CLIP-Score. Green cells highlight the best scores, and yellow cells the second best*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2512_13840/figures/005_Table_2.jpg]]
*Table 2: Ablation studies. We analyze: (1) different text-conditioning mechanisms, and (2) the effect of using a semantically aligned latent space. AdaLN denotes single-text-token conditioning with DiT-style modulation; note that the first row corresponds to MARDM [39]. CrossAttn denotes multi-token cross-attention conditioning. We conduct all experiments using the MARDM-67 evaluator with 4× downsampling and latent dimensions of 16. We adopt adapter depth 6 for T5+CrossAttn setting*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2512_13840/figures/007_Table_3.jpg]]
*Table 3: Performance under different SAE configurations. We ablate three design choices for SAE: (1) the semantic regularization loss (cosine similarity vs. InfoNCE), (2) whether KL divergence is applied jointly, and (3) the weight of ${ \mathcal { L } } _ { \mathrm { { s e m } } }$ . . The configuration with cosine similarity, KL divergence, and a relatively small weight (0.001) gives the best SAE design, significantly improving text–motion alignment (R-Precision and CLIP-score) while maintaining FID comparable to SOTA models

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2512_13840/figures/010_Table_4.jpg]]
*Table 4: Notation Table. The main notation used in our paper*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2512_13840/figures/011_Table_5.jpg]]
*Table 5: Effect of text adapter depth. We compare models without a text adapter and with text adapters of different depths (3, 6, and 9 layers). Using a 6-layer adapter (ours) gives the best overall tradeoff, improving FID and R-Precision across all others. We conduct all experiments on MARDM-67 [39] evaluator using a VAE with a downsampling 4× and latent dimension 16*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2512_13840/figures/012_Table_6.jpg]]
*Table 6: Effect of repetitive class token filtering. We ablate generative performance with and without repetitive class token filtering during SAE training. Filtering consistently improves FID and retrieval scores, indicating that it acts as a soft semantic regularizer, encouraging coherence without forcing adjacent motion latents to collapse to the same text label*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2512_13840/figures/014_Table_7.jpg]]
*Table 7: Quantitative comparison with MotionStreamer. MotionStreamer proposed a TMR-style [42] feature extractor used as an evaluator in their own 272D representation. To ensure a fair comparison, we train our model on the 272D HumanML3D data and evaluate using their evaluator. rFID denotes reconstruction FID, and MPJPE is measured in millimeters. Our replicated padding design improves reconstruction realism in terms of rFID while preserving comparable MPJPE. For generation, our method achieves significant improvements over MotionStreamer across all metrics. We run the experiment 20 runs and ± indicates 95% confidence interval. We apply 4× downsampling and latent dimension 16 with a well-trained SAE*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2512_13840/figures/015_Table_8.jpg]]
*Table 8: Quantitative results on the TMR-263 evaluator. We compare our method with a broad set of motion generation approaches, from early models [6, 53] to recent ones [7, 76], covering pose-frame diffusion [53], single-vector latent diffusion [6, 9], VQ-based next-token prediction [7, 18, 19, 44, 45, 65], and continuous-valued auto-regressive models [76]. We report the mean results over 20 independent runs, and the ± values indicate the 95% confidence interval. We do not compare with MARDM [39] and ACMDM [40] here because of the motion representation inconsistency. Our method achieves state-of-the-art FID, R-Precision, and MultiModality. Green cells highlight the best scores, and yellow cells the...*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2512_13840/figures/016_Table_9.jpg]]
*Table 9: Detail architecture of our autoencoders. Different from [62], we set the padding mode of the first 1D convolutional layer to replicate the initial frames, which stabilizes training and improves reconstruction*

## 方法谱系与知识库定位

### 连续潜在空间生成范式的演进与分化

MoLingo 的核心技术路线属于**连续潜在空间的自回归生成**范式，但其设计选择与同路线方法存在显著差异，同时在关键模块上吸收了离散潜在方法的优势。

**与同路线方法的对比：** 在连续潜在自回归扩散路线中，**MARDM** 采用单 token 的 AdaLN 调制作为文本条件化机制，并使用普通 AE 进行运动压缩。MoLingo 通过消融实验直接证明了这一设计的局限性：将 AdaLN 替换为多 token 交叉注意力后，FID 从 0.053 降至 0.049，R-Precision Top-1 从 0.522 提升至 0.528（Table 2）。**ACMDM** 同样属于连续潜在扩散路线，但在 MARDM-67 评估协议下，其最优变体 ACMDM-XL-PS2 的 FID 为 0.058，R-Precision Top-1 为 0.522，均弱于 MoLingo 的 0.049/0.528（VAE 变体）和 0.064/0.542（SAE 变体）（Table 1）。**MotionStreamer** 采用连续潜在自回归流模型，在 MS-272 评估协议上 FID 高达 11.979，而 MoLingo 仅 3.444，差距超过 8.5 个 FID 点（Table 7），且在用户研究中 MoLingo 获得了 84.70% 的偏好率（Section 4.3）。

**与离散潜在方法的对比：** 尽管 MoLingo 采用连续潜在空间，其在文本条件化强度和多 token 交互设计上与 VQ 离散潜在方法形成呼应。**MoMask** 使用 VQ 掩码预测，在 TMR-263 评估器上 FID 为 0.022，而 MoLingo 达到 0.014（Table 8），表明连续潜在配合强条件化机制可以超越离散量化的保真度上限。**DisCoRD** 作为 VQ 离散潜在扩散模型，在 MARDM-67 上 FID 为 0.053，MoLingo 以 0.049 取得领先（Table 1），用户偏好率亦达到 83.75%。

**方法差异的关键因果节点：** MoLingo 相对于上述基线的核心改进可归结为两个因果变量：（1）**语义对齐潜在空间**——通过 BABEL 帧级文本标签的余弦相似度损失，使潜在空间具有语义结构化特性，这使 SAE 变体在所有文本-动作对齐指标上一致优于普通 AE 和 VAE（Table 2）；（2）**多 token 交叉注意力**——相比单 token 调制，交叉注意力允许模型在生成每个潜在时动态关注文本的不同部分，显著增强了文本条件化的表达能力。两者的组合效应在 Table 2 中清晰呈现：T5 + CrossAttn + SAE 配置在 R-Precision Top-1（0.542）和 CLIP-Score（0.686）上达到最优，而 T5 + CrossAttn + VAE 则在 FID（0.049）上最优。

### 适用边界与局限

**语义对齐的数据依赖性：** SAE 的语义损失仅应用于 BABEL 与 HumanML3D 的交集部分，这意味着帧级文本监督的覆盖范围受限于 BABEL 的标注规模。对于 BABEL 未覆盖的动作类别，语义对齐效果缺乏直接监督，模型在这些动作上的文本-动作对齐可能退化至普通 AE 水平。这一局限在 Table 2 中表现为 SAE 的 FID（0.064）略高于 VAE（0.049），暗示语义约束在提升对齐的同时对重建保真度有轻微负面影响。

**评估指标的感知局限性：** 尽管 MoLingo 在 FID、R-Precision、CLIP-Score 等自动指标上全面领先，但论文明确指出这些指标可能无法完全捕捉人类对运动质量和语义一致性的感知（limitations）。用户研究提供了补充证据（MoLingo 在三个基线对比中均获得超过 77% 的偏好率），但用户研究的规模和多样性未在可验证材料中详细说明，该结论的泛化性需谨慎对待。

**运动表示的覆盖范围：** 当前 MoLingo 框架尚未扩展到包含详细手部动作的全身运动生成。手部交互的建模仍是开放挑战（limitations），这意味着该方法目前适用于身体躯干和四肢的运动生成，但在需要精细手部姿态的场景（如手语、乐器演奏）中存在能力边界。

**数据分布依赖性：** 生成的运动依赖训练数据的分布，可能无法泛化到极具创意或罕见的文本描述。这一点在定性比较（Figure 4）中得到间接印证——对于舞蹈等复杂动作，MoLingo 虽优于基线，但生成质量与真实采集数据之间仍存在可感知的差距。

### 开放问题与未来方向

1. **语义对齐的规模化扩展：** 如何将语义对齐策略扩展到更大、更多样化的文本-动作数据集，而不依赖 BABEL 的帧级标注？可能的路径包括利用视觉-语言模型的弱监督或自监督语义对齐。

2. **文本编码器的进一步强化：** 多 token 交叉注意力能否与更强大的文本编码器（如更大规模的 T5 变体或视觉-语言模型）结合，以进一步提升文本-动作对齐的上限？当前使用的 T5-Large 是冻结的，微调或替换编码器可能带来额外增益。

3. **全身运动生成的扩展：** 将 MoLingo 框架扩展到包含手指细节的全身运动生成，同时保持实时性，需要在运动表示、潜在压缩率和解码器架构上进行系统性探索。

4. **语义潜在空间的下游复用：** 语义对齐的潜在空间是否能够直接用于运动编辑、跨模态检索或运动风格迁移等下游任务？这一方向可能拓展 MoLingo 框架的应用范围，超越纯粹的生成任务。

5. **自回归生成顺序的优化：** 当前的自回归生成顺序是固定的（从第一个潜在到最后一个），是否存在更优的生成顺序（如从关键帧向外扩散，或基于文本引导的动态排序），以进一步提高运动质量和长序列一致性？

## 原文 PDF

![[paperPDFs/CVPR_2026/MoLingo_Motion_Language_Alignment_for_Text_to_Human_Motion_Generation.pdf]]
