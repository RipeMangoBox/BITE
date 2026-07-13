---
title: Diffusion-Based sRGB Real Noise Generation via Prompt-Driven Noise Representation Learning
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Diffusion_Based_sRGB_Real_Noise_Generation_via_Prompt_Driven_Noise_Representation_Learning.pdf
project_link: null
code_link: "https://github.com/JK-the-Ko/PNG"
aliases:
- DBSRNGPDNRL
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/benchmarks_datasets_evaluation
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 从输入噪声图像中提取的隐式提示特征（Prompt Features）取代显式元数据，驱动生成式模型合成符合目标噪声分布的图像。
primary_logic: 通过可学习的全局和局部提示组件（Global/Local Prompt Block），自动编码器能从噪声图像中提取高维提示特征，分别捕捉 ISO 等全局统计量和空间相关性等局部模式，进而条件化一致性模型生成逼真的信号依赖噪声，彻底摆脱训练与推理阶段对元数据的依赖。
claims:
- 在 SIDD 验证集上，PNG 在所有设备类型上均优于对比方法，平均 KLD 和 AKLD 较 NAFlow 分别降低 0.0111 和 0.0143。
- 使用生成数据集训练的去噪网络在仅合成和合成-真实混合设置下均取得最优平均性能，且与仅用真实数据训练的模型性能几乎一致。
- SIDD validation (subset) 上 KLD = 0.0194
- SIDD-Benchmark 上 PSNR = 37.55
---

# Diffusion-Based sRGB Real Noise Generation via Prompt-Driven Noise Representation Learning

> [!tip] 核心洞察
> 通过可学习的全局和局部提示组件（Global/Local Prompt Block），自动编码器能从噪声图像中提取高维提示特征，分别捕捉 ISO 等全局统计量和空间相关性等局部模式，进而条件化一致性模型生成逼真的信号依赖噪声，彻底摆脱训练与推理阶段对元数据的依赖。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于提示驱动的噪声表示学习的 sRGB 真实噪声扩散生成 |
| 英文题名 | Diffusion-Based sRGB Real Noise Generation via Prompt-Driven Noise Representation Learning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.04870) · [Code](https://github.com/JK-the-Ko/PNG) |
| Topic | #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/benchmarks_datasets_evaluation #topic/generative_models_diffusion/diffusion_image_video |
| Method | PNG |
| Dataset | SIDD validation, SIDD-Benchmark, PolyU, Nam, SIDD Val, SIDD+ (avg) — 100% synthetic |

> [!tip] 效果简介
> - SIDD validation (subset) 上，KLD 0.0194 vs 0.0305 (NAFlow) (-36.4%)。
> - SIDD-Benchmark 上，PSNR 37.55 vs 37.22 (NAFlow) (+0.33 dB)。
> - PolyU, Nam, SIDD Val, SIDD+ (avg) — 100% synthetic 上，PSNR 37.47 vs 37.06 (NAFlow) (+0.41 dB)。

## 概要

真实图像去噪的核心瓶颈在于**高质量配对训练数据的稀缺**——真实噪声-清洁图像对的采集成本极高，且噪声分布随传感器型号、ISO 感光度等相机元数据剧烈变化。现有 sRGB 真实噪声合成方法（如 **C2N**、**Flow-sRGB**、**NeCA-W**、**NAFlow**）普遍依赖显式相机元数据（设备型号、ISO 等）来条件化生成模型，当元数据缺失或跨设备不一致时，泛化能力严重受限。

本文提出 **PNG（Prompt-Driven Noise Generation）**，一种**无元数据依赖**的 sRGB 真实噪声生成框架。其核心洞察是：从输入噪声图像中学习到的**隐式提示特征（Prompt Features）**可以取代显式元数据，驱动生成模型合成符合目标噪声分布的图像。具体而言，PNG 通过一个 Prompt Autoencoder（PAE）从噪声图像中提取高维提示特征——其中**全局提示块（GPB）**捕捉 ISO 等全局统计量，**局部提示块（LPB）**捕捉空间相关性等局部模式——进而条件化基于一致性模型（CM）的 Prompt DiT（P-DiT）在紧凑潜空间中生成逼真的信号依赖噪声，彻底摆脱训练与推理阶段对元数据的依赖。

**主要结果**：在 SIDD 验证集上，PNG 的合成噪声质量显著优于所有对比方法，平均 KLD 和 AKLD 较 NAFlow 分别降低 0.0111 和 0.0143。使用 PNG 生成数据集训练的去噪网络（DnCNN）在 SIDD-Benchmark 上达到 37.55 dB PSNR，优于 NAFlow 的 37.22 dB，且与仅用真实数据训练的模型性能几乎一致。在跨数据集泛化实验中，PNG 在纯合成（100%）和合成-真实混合（50%）设置下均取得最优平均性能。



真实世界图像去噪是计算摄影中的核心任务。在 sRGB 域，真实噪声呈现出复杂的信号依赖特性——噪声强度随像素亮度变化，且不同相机传感器和图像信号处理（ISP）管线会引入截然不同的噪声模式。然而，获取大规模、高质量的配对真实噪声-清洁图像数据集成本极高，这促使研究者转向噪声合成范式：先建模真实噪声分布，再生成成对的合成噪声-清洁图像以训练去噪网络。

现有 sRGB 真实噪声合成方法可大致分为两类。一类基于物理模型，通过模拟光子散粒噪声和读出噪声等传感器噪声源来合成噪声，但这类方法难以精确复现 ISP 管线引入的非线性变换。另一类基于数据驱动的生成模型，如 **C2N** 和 **Flow-sRGB** 利用条件生成对抗网络或归一化流学习噪声分布，**NeCA-W** 和 **NAFlow** 则进一步采用扩散模型提升合成质量。然而，这些方法的共同瓶颈在于：**它们依赖显式相机元数据（如 ISO 感光度、设备型号）作为条件输入**（Figure 1a）。当元数据缺失、不准确或跨设备不一致时，模型的泛化能力严重受限，无法在真实应用场景中灵活部署。

这一瓶颈的根源在于真实噪声的分布高度依赖于拍摄参数和传感器特性。ISO 值决定了噪声的整体强度，而传感器的空间相关性和 ISP 的降噪处理则塑造了噪声的局部结构。显式元数据试图用离散标签捕捉这些连续、高维的噪声特性，本质上是一种信息瓶颈——不同设备在相同 ISO 下可能产生截然不同的噪声模式，而同一设备在不同场景下的噪声也远非单一参数所能描述。

本文的核心动机正是**彻底摆脱对显式元数据的依赖**。我们提出一个根本性问题：能否直接从噪声图像本身提取出足够丰富的特征，用以条件化生成模型，使其合成出符合目标噪声分布的图像？这一思路将噪声生成从“元数据驱动”转变为“数据驱动”——让模型从噪声图像中自主学习那些传统方法需要人工标注的噪声属性。这种范式转变不仅消除了训练和推理阶段对元数据的硬性依赖，还使模型能够捕捉到元数据无法编码的细粒度噪声特征，从而在跨设备、跨数据集的泛化场景中展现出更强的适应性。



## 核心方法与创新机理

### 问题瓶颈：元数据依赖导致真实噪声合成的泛化困境

现有 sRGB 真实噪声合成方法（如 **C2N**、**Flow-sRGB**、**NeCA-W**、**NAFlow**）在生成噪声时普遍依赖显式相机元数据——典型的是 ISO 感光度与设备型号。这一设计存在两个根本性缺陷：

1. **元数据缺失或不可靠时的失效**：当输入噪声图像的 EXIF 信息丢失、被篡改，或来自训练阶段未见过的设备时，模型缺乏可用的条件信号，噪声生成质量急剧退化。
2. **跨设备泛化受限**：不同相机型号的传感器特性、ISP 流水线差异巨大，基于离散设备 ID 或 ISO 值的条件化方式难以捕捉连续、细粒度的噪声分布差异，导致合成噪声与真实噪声之间存在不可忽略的分布偏移。

同时，获取大规模、多设备、覆盖多样光照条件的配对真实噪声-清洁图像成本极高，进一步加剧了数据驱动方法对元数据的过度依赖。

### 核心洞察：以隐式提示特征替代显式元数据

本文的核心创新在于**将噪声条件信息从“显式元数据”替换为“从噪声图像自身学习到的隐式提示特征”**。具体而言，PNG 框架提出：

- **噪声图像本身已经蕴含了生成该噪声所需的全部统计信息**——ISO 级别体现在噪声强度的全局统计量中，传感器读出噪声的行/列相关性体现在局部空间模式中，ISP 引入的非线性映射体现在通道间的协方差结构中。
- 通过设计可学习的**全局提示块（Global Prompt Block, GPB）**和**局部提示块（Local Prompt Block, LPB）**，自动编码器能够从输入噪声图像中自适应地提取高维提示特征（Prompt Features），分别捕获全局噪声统计量（如 ISO 增益）和局部空间相关性（如行噪声、列噪声模式）。
- 这些提示特征随后作为条件信号注入到基于一致性模型（Consistency Model, CM）的扩散 Transformer（**Prompt DiT, P-DiT**）中，驱动其在潜空间中生成与目标噪声分布一致的潜变量，最终经解码器重建为具有信号依赖特性的真实噪声图像。

这一设计使得 PNG **在训练和推理阶段均彻底摆脱了对相机元数据的依赖**，从根本上解决了元数据缺失场景下的泛化难题。

### Changed Slot：噪声条件信息的范式转换

在方法谱系中，PNG 的核心 changed slot 可精确描述为：

| 模块 | 基线方法（Baseline） | PNG 方法（Proposed） |
|------|---------------------|---------------------|
| **噪声条件信息** | 显式相机元数据（ISO、设备型号等） | 从噪声图像中学习到的隐式提示特征（全局 + 局部） |

这一 changed slot 的因果作用链路如下：

1. **Prompt Encoder** 接收真实噪声图像 $n_{\text{Real}}$，通过 GPB 和 LPB 分别提取全局提示特征 $\mathbf{F}_{\text{Global}}$ 和局部提示特征 $\mathbf{F}_{\text{Local}}$，同时将噪声图像压缩为紧凑潜变量 $\mathbf{z}$。
2. **P-DiT** 以洁净图像 $I_{\text{Clean}}$ 和提示特征为联合条件，在潜空间中基于一致性训练损失 $\mathcal{L}_{\text{CT}}$ 学习噪声潜变量的分布，生成符合目标噪声特性的潜变量 $\hat{\mathbf{z}}$。
3. **Decoder** 以 $I_{\text{Clean}}$ 为条件，将 $\hat{\mathbf{z}}$ 解码为具有信号依赖特性的合成噪声图像 $\hat{n}_{\text{Real}}$。

### 关键支撑证据

- **噪声生成质量**：在 SIDD 验证集上，PNG 的 KLD 为 0.0194，较最强基线 NAFlow（0.0305）降低 36.4%（Table 1）。在所有设备类型上，PNG 的平均 KLD 和 AKLD 分别较 NAFlow 降低 0.0111 和 0.0143。
- **下游去噪性能**：使用 PNG 合成数据训练的 DnCNN 在 SIDD-Benchmark 上取得 37.55 dB PSNR，超越 NAFlow（37.22 dB）0.33 dB（Table 2）。在 100% 合成数据设置下，PNG 在四个基准上的平均 PSNR 达 37.47 dB，较 NAFlow（37.06 dB）提升 0.41 dB（Table 3）。
- **消融验证**：联合使用 GPB 和 LPB 可获得最佳噪声生成质量（KLD 0.0261），仅使用单一提示块会导致性能显著下降（Table 7），证实了全局与局部提示特征的互补性。

### 局限与开放问题

尽管 PNG 在元数据无关的噪声生成上取得了显著进展，仍存在以下局限：

1. **PAE 训练仍依赖配对数据**：提示自动编码器的训练需要成对的噪声-清洁图像，尚无法在完全无配对场景下学习。
2. **跨传感器迁移能力未充分验证**：提示特征在跨传感器、跨 ISP 流程下的泛化能力尚未系统评估，能否直接迁移到训练阶段未见过的相机型号仍需进一步研究。
3. **推理速度**：在高分辨率（1024×1024）下推理速度约 5 fps，虽优于 NAFlow，但仍不及非扩散方法 NeCA-W。

开放问题包括：能否进一步减少对配对数据的依赖（如仅利用非配对噪声图像和任意洁净图像训练）；提示特征能否支撑盲去噪任务（无需显式输入噪声图像）；以及框架在 RAW 域或视频帧上的适用性。



PNG 框架的核心设计动机在于彻底消除真实噪声生成对显式相机元数据（如 ISO、设备型号）的依赖。如图 2 所示，整个系统由两个串行训练的关键模块构成：**Prompt Autoencoder（PAE）** 和 **Prompt DiT（P-DiT）**，二者在紧凑的潜空间中协同工作。

### 训练流程

训练分为两个阶段，分别对应图 2(a) 中的上下两条通路。

**第一阶段：PAE 训练。** 输入为真实噪声图像 $n_{\text{Real}}$ 及其对应的清洁图像 $I_{\text{Clean}}$。Prompt Encoder $E$ 接收 $n_{\text{Real}}$，通过内部的 Global Prompt Block（GPB）和 Local Prompt Block（LPB）提取输入特定的高维提示特征（Prompt Features），同时将噪声图像编码为紧凑的潜变量 $z$。Decoder $D$ 则以 $I_{\text{Clean}}$ 为条件，从 $z$ 重建出具有信号依赖特性的噪声图像。PAE 的训练目标是使重建的噪声图像逼近原始输入，同时约束潜变量分布接近标准高斯，为后续的扩散生成提供良好的潜空间结构。

**第二阶段：P-DiT 训练。** 固定已训练好的 PAE，在潜空间中训练基于一致性模型（Consistency Model, CM）的扩散 Transformer。P-DiT 接收三个条件输入：从 PAE 编码得到的潜变量 $z$、对应的清洁图像 $I_{\text{Clean}}$、以及由 Prompt Encoder 提取的提示特征。其训练目标是通过一致性训练损失 $\mathcal{L}_{\text{CT}}$ 学习潜变量的条件分布，使得模型能够从随机噪声出发，在少量采样步内生成符合目标噪声分布的潜变量。

### 推理流程

如图 2(b) 所示，推理阶段完全无需显式元数据。给定一张目标噪声图像 $n_{\text{Real}}$ 和一张任意清洁图像 $I_{\text{Clean}}$，Prompt Encoder 从 $n_{\text{Real}}$ 中提取提示特征。P-DiT 以该提示特征和 $I_{\text{Clean}}$ 为条件，从随机初始化的潜变量出发，通过一致性模型的多步去噪过程生成潜变量 $z$。最终，Decoder $D$ 将 $z$ 与 $I_{\text{Clean}}$ 结合，重建出具有与输入噪声图像相似统计特性的合成噪声图像。

### 关键设计要点

- **元数据自由：** 提示特征完全从输入噪声图像中学习，捕捉了 ISO 等级、空间相关性等传感器特异性统计量，使得训练和推理均不依赖显式元数据。
- **两阶段解耦：** PAE 负责噪声表示学习与压缩，P-DiT 负责条件生成，二者解耦训练，降低了整体优化难度。
- **一致性模型加速：** P-DiT 采用 CM 目标（式 (4)）进行训练，在推理时仅需少量采样步即可生成高质量潜变量。补充材料中 Table S1 显示，PNG 在 1024×1024 分辨率下的推理速度约为 5 fps，优于 NAFlow 但不及 NeCA-W。
- **提示特征的双重注入：** P-DiT 中提示特征同时注入时间步嵌入和注意力层（Prompt Attention），消融实验（Table S2）证实这种双重注入策略显著优于仅对时间步嵌入进行条件化。

![[assets/figures/papers/paper_list_l2305_https_arxiv_org_abs_2603_04870/figures/014_Table_S.1.jpg]]
*Table S.1: Inference speed comparison between NeCA-W, NAFlow, and PNG*

### 补充图表

![[assets/figures/papers/paper_list_l2305_https_arxiv_org_abs_2603_04870/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed method. (a) Training pipeline. (b) Inference pipeline*



PNG 框架由两个核心模块构成：**Prompt Autoencoder (PAE)** 和 **Prompt DiT (P-DiT)**，二者分两阶段顺序训练。第一阶段，PAE 学习将真实噪声图像编码为紧凑的潜变量，同时通过提示块提取输入噪声的特性；第二阶段，P-DiT 在潜空间中基于一致性模型（CM）学习潜变量的分布，以洁净图像和提示特征为条件生成符合目标噪声分布的潜变量，再经 PAE 的解码器重建为噪声图像。

### 3.1 一致性模型基础

P-DiT 的训练建立在一致性模型（Consistency Model, CM）之上。给定前向扩散过程的重参数化形式：

$$
\mathbf{x}_t = \alpha_t \mathbf{x}_0 + \sigma_t \boldsymbol{\epsilon}, \quad \boldsymbol{\epsilon} \sim \mathcal{N}(0, \mathbf{I}), \quad t \in \{0, 1, \dots, T\}
$$

其中 $\mathbf{x}_0$ 为干净数据，$\mathbf{x}_t$ 为第 $t$ 步的噪声样本，$\alpha_t$ 和 $\sigma_t$ 为噪声调度参数。一致性函数 $f_\theta$ 的目标是直接从任意噪声级别的 $\mathbf{x}_t$ 近似原始数据 $\mathbf{x}_0$：

$$
f_\theta(\mathbf{x}_t, \sigma_t) = \mathbf{x}_t + \int_{\sigma_t}^{\sigma_0} \frac{d\mathbf{x}_u}{du} du \approx \mathbf{x}_0
$$

训练通过最小化相邻噪声级别上学生网络与教师网络（指数移动平均副本 $\theta^-$）输出之间的距离来实现，损失函数为：

$$
\mathcal{L}_{\mathrm{CT}} = \mathbb{E}\left[ \lambda(\sigma_t) d\left( f_{\theta}(\mathbf{x}_{t+1}, \sigma_{t+1}), \mathrm{sg}\big( f_{\theta^{-}}(\mathbf{x}_t, \sigma_t) \big) \right) \right]
$$

其中 $\mathrm{sg}(\cdot)$ 表示停止梯度，$d(\cdot, \cdot)$ 为距离度量，$\lambda(\sigma_t)$ 为权重函数。PNG 在紧凑的潜空间中运行 CM，从而获得显著的计算效率优势。

### 3.2 Prompt Autoencoder (PAE)

PAE 由 Prompt Encoder $E$ 和 Decoder $D$ 组成。给定真实噪声图像 $\mathbf{n}_{\mathrm{Real}}$，Encoder 将其映射为潜变量 $\mathbf{z}$，同时通过两个关键模块——**Global Prompt Block (GPB)** 和 **Local Prompt Block (LPB)**——提取高维提示特征，分别捕捉输入噪声的全局统计量（如 ISO 级别）和局部空间相关性。

#### 3.2.1 Global Prompt Block (GPB)

GPB 通过计算输入特征图的通道均值和标准差来捕捉全局噪声统计量。对于第 $\ell$ 层的输入特征 $\mathbf{F}_{\mathrm{In}}^{\ell} \in \mathbb{R}^{C \times H \times W}$，全局提示系数 $\mathbf{w}_{\mathrm{Global}}^{\ell}$ 由通道统计量经 $1\times1$ 卷积和 Softmax 生成：

$$
\mathbf{w}_{\mathrm{Global}}^{\ell} = \mathrm{Softmax}\Bigg(\mathrm{Conv}_{1\times1}\Big[\mu(\mathbf{F}_{\mathrm{In}}^{\ell}), \boldsymbol{\Sigma}(\mathbf{F}_{\mathrm{In}}^{\ell})\Big]\Bigg)
$$

其中 $\mu(\cdot)$ 和 $\boldsymbol{\Sigma}(\cdot)$ 分别表示通道均值和标准差。随后，这些系数对可学习的全局提示组件 $\mathbf{P}_{\mathrm{Global}}^{\ell}$ 进行逐元素调制，再经 $3\times3$ 卷积精炼为全局提示特征：

$$
\mathbf{F}_{\mathrm{Global}}^{\ell} = \mathrm{Conv}_{3\times3}\bigg(\mathbf{w}_{\mathrm{Global}}^{\ell} \odot \mathbf{P}_{\mathrm{Global}}^{\ell}\bigg)
$$

#### 3.2.2 Local Prompt Block (LPB)

LPB 负责捕捉噪声的空间相关模式。首先从输入特征 $\mathbf{F}^{\rho}$ 计算噪声局部相关图，再沿行和列方向分别进行平均池化，拼接后经轻量组合块 CoMB 处理，通过 Softmax 得到局部提示系数 $\mathbf{w}_{\mathrm{Local}}$：

$$
\mathbf{w}_{\mathrm{Local}} = \mathrm{Softmax}\bigg(\mathrm{CoMB}\big(\big[\mathrm{Avg}_{\mathrm{row}}(\mathbf{F}^{\rho}), \mathrm{Avg}_{\mathrm{col}}(\mathbf{F}^{\rho})\big]\big)\bigg)
$$

最终局部提示特征由系数调制可学习局部组件 $\mathbf{P}_{\mathrm{Local}}$ 后经 $3\times3$ 卷积生成：

$$
\mathbf{F}_{\mathrm{Local}} = \mathrm{Conv}_{3\times3}\bigg(\mathbf{w}_{\mathrm{Local}} \odot \mathbf{P}_{\mathrm{Local}}\bigg)
$$

GPB 和 LPB 提取的提示特征被拼接后作为条件注入 P-DiT 的生成过程。Decoder $D$ 则以洁净图像 $\mathbf{I}_{\mathrm{Clean}}$ 为条件，将潜变量 $\mathbf{z}$ 重建为具有信号依赖特性的噪声图像。

### 3.3 Prompt DiT (P-DiT)

P-DiT 是基于 DiT（Diffusion Transformer）架构的一致性模型，在潜空间中根据提示特征和洁净图像条件生成符合目标噪声分布的潜变量。P-DiT 在训练时接收 PAE 编码的潜变量作为 $\mathbf{x}_0$，通过前向扩散加噪后，以 CM 损失 $\mathcal{L}_{\mathrm{CT}}$ 进行优化。提示特征通过两种途径注入 P-DiT：**时间步嵌入的条件化**和**注意力层的 Prompt Attention 机制**。消融实验表明，同时在时间步嵌入和注意力层进行条件注入能显著降低 KLD 和 AKLD，是取得最优噪声生成质量的关键设计选择（Table S2）。增加 P-DiT 的 Transformer 块数 $B$ 可持续提升生成质量，$B=8$ 时 KLD 从 $B=4$ 的 0.0350 降至 0.0261（Table S4）。



## 实验与关键发现

### 合成噪声质量评估

PNG 在 SIDD 验证集子集上的噪声生成质量显著优于现有方法。如 Table 1 所示，PNG 在所有设备类型上均取得最优 KLD 和 AKLD，平均 KLD 为 0.0194，较 NAFlow 的 0.0305 降低 36.4%；平均 AKLD 为 0.1108，较 NAFlow 的 0.1251 降低 0.0143。这一优势源于提示特征对噪声统计量的精确捕捉——GPB 提取的全局统计量（如 ISO 相关的通道均值和标准差）与 LPB 建模的空间相关性共同构成了对真实噪声分布的高保真表示。

![[assets/figures/papers/paper_list_l2305_https_arxiv_org_abs_2603_04870/figures/004_Table_1.jpg]]
*Table 1: Quantitative results for synthetic noise on a subset of the SIDD validation set, in which the ISO values exist in the training set. The results are computed with KLD↓ and AKLD↓. The best and second-best results are highlighted in bold and underline, respectively*

Figure 4 的可视化对比进一步印证了定量结果：C2N 和 NeCA-W 生成的噪声在平坦区域呈现明显的人工痕迹，NAFlow 虽有所改善但仍与真实噪声存在偏差，而 PNG 生成的噪声在信号依赖特性、空间纹理和强度分布上均与真实噪声高度一致。

![[assets/figures/papers/paper_list_l2305_https_arxiv_org_abs_2603_04870/figures/007_Figure_4.jpg]]
*Figure 4: Visualization of synthetic noisy images on the SIDD validation set. From left to right: C2N, NeCA-W, NAFlow, Ours (PNG), and real noisy images*

### 去噪性能验证

**SIDD-Benchmark 评估。** 使用各方法生成的合成数据集训练 DnCNN 去噪网络，在 SIDD-Benchmark 上评估（Table 2）。PNG 以 37.55 dB PSNR 和 0.937 SSIM 取得最优性能，较 NAFlow（37.22 dB / 0.935）提升 0.33 dB，且与使用真实配对数据训练的模型（37.59 dB / 0.938）性能几乎一致。这验证了 PNG 生成的合成噪声在分布层面与真实噪声高度对齐，能够有效替代真实配对数据进行去噪网络训练。

**跨数据集泛化。** Table 3 报告了在 PolyU、Nam、SIDD Val 和 SIDD+ 四个基准上的跨数据集去噪性能。在 100% 合成数据设置下，PNG 以平均 37.47 dB PSNR 超越 NAFlow（37.06 dB）0.41 dB；在 50% 合成-50% 真实混合设置下，PNG 平均 PSNR 达 37.65 dB，进一步缩小了与纯真实数据训练的差距。值得注意的是，PNG 在 PolyU（40.14 dB）和 Nam（40.83 dB）等外部数据集上的表现同样领先，表明提示特征捕捉的噪声特性具备跨数据集迁移能力。

**外部数据集噪声质量。** Table 4 显示，所有方法均仅使用 SIDD 训练集训练，但在 PolyU、Nam 和 MAI2021 三个外部数据集上评估噪声生成质量时，PNG 的 KLD 和 AKLD 均取得最优。这直接证明了无元数据提示特征相较于显式相机参数（如 ISO、设备型号）在跨设备泛化上的根本优势——当目标设备的元数据分布与训练集不一致时，基于元数据条件化的方法（如 NAFlow）会出现性能退化，而 PNG 的隐式提示特征无需依赖此类先验信息。

### 消融实验

**提示块设计。** Table 7 表明，联合使用 GPB 和 LPB 可获得最佳噪声生成质量（KLD 0.0261, AKLD 0.1108）。仅使用 GPB 时 KLD 升至 0.0291，仅使用 LPB 时 AKLD 升至 0.1129，验证了两类提示特征在捕捉全局统计量和局部空间模式上的互补性。Table S3 进一步证实，在 PAE 重建任务中，双提示块组合同样取得最优重建质量。

**P-DiT 条件注入策略。** Table S2 探索了提示特征在 P-DiT 中的注入位置。结果表明，同时对时间步嵌入和注意力层进行条件注入（Prompt Attention）比仅对时间步嵌入条件化能显著降低 KLD 和 AKLD，说明在扩散 Transformer 的多层级结构中充分注入提示信息对于学习准确的潜变量分布至关重要。

**P-DiT 容量。** Table S4 显示，增加 P-DiT 的 Transformer 块数（B）能持续提升噪声生成质量：B=4 时 KLD 为 0.0350，B=8 时降至 0.0261。这提示在计算资源允许的情况下，增大生成模型容量是进一步提升噪声保真度的可行方向。

### 推理效率

Table S1 比较了各方法的推理速度。在高分辨率（1024×1024）下，PNG 约 5 fps，虽不及 NeCA-W 但显著优于 NAFlow。PNG 的效率优势来自两方面：一是 PAE 将噪声压缩至紧凑潜空间（32×32），二是 P-DiT 基于一致性模型仅需少量采样步即可生成高质量潜变量。

### 局限与失败模式

尽管 PNG 在多项指标上表现优异，仍存在以下局限：第一，PAE 训练仍需成对的噪声-清洁图像，无法完全在无配对数据场景下直接学习，这限制了其在数据获取极度困难场景下的适用性；第二，所有实验均局限于 sRGB 域，未验证提示特征在 RAW 域或视频帧上的有效性，跨域迁移能力尚不明确；第三，在高分辨率场景下推理速度仍不及轻量级方法（如 NeCA-W），对于实时应用存在性能瓶颈。以上局限需要在实际部署中结合具体需求进行手动验证。

### 补充图表

![[assets/figures/papers/paper_list_l2305_https_arxiv_org_abs_2603_04870/figures/005_Table_2.jpg]]
*Table 2: Denoising performance of DnCNN on SIDD-Benchmark in terms of PSNR↑ and SSIM↑. All methods are trained with synthetic noisy-clean pairs. Note that Real indicates denoising results by training using real noisy-clean pairs. The best and secondbest results are highlighted in bold and underline*

![[assets/figures/papers/paper_list_l2305_https_arxiv_org_abs_2603_04870/figures/008_Table_3.jpg]]
*Table 3: Quantitative comparison of DnCNN denoising performance on the PolyU, Nam, SIDD validation, and SIDD+ benchmarks. The percentage (%) denotes the mixing ratio between the two training subsets. The best and second-best results are highlighted in bold and underline*

![[assets/figures/papers/paper_list_l2305_https_arxiv_org_abs_2603_04870/figures/011_Table_7.jpg]]
*Table 7: Effect of GPB and LPB on SIDD validation noise generation. The best results are shown in bold*

![[assets/figures/papers/paper_list_l2305_https_arxiv_org_abs_2603_04870/figures/016_Table_S.2.jpg]]
*Table S.2: Effect of conditioning features on different components in P-DiT. The best results are shown in bold*

![[assets/figures/papers/paper_list_l2305_https_arxiv_org_abs_2603_04870/figures/015_Table_S.4.jpg]]
*Table S.4: KLD score depending on different number of blocks B*

![[assets/figures/papers/paper_list_l2305_https_arxiv_org_abs_2603_04870/figures/009_Table_4.jpg]]
*Table 4: Quantitative results of synthetic noise on the PolyU, Nam, and MAI2021. All methods are trained with SIDD training set. The results are computed with KLD↓ and AKLD↓. The best results are shown in bold*

![[assets/figures/papers/paper_list_l2305_https_arxiv_org_abs_2603_04870/figures/017_Table_S.3.jpg]]
*Table S.3: Effect of GPB and LPB on SIDD validation noisy image reconstruction. The best results are shown in bold*

![[assets/figures/papers/paper_list_l2305_https_arxiv_org_abs_2603_04870/figures/018_Figure_S.2.jpg]]
*Figure S.2: Overview of unpaired noise generation process*



## 定位与知识库关联

### 与基线方法的关系

PNG 的核心贡献在于将 sRGB 真实噪声生成的**条件信息**从显式相机元数据替换为从噪声图像中学习到的隐式提示特征，从而彻底摆脱训练与推理阶段对元数据的依赖。这一设计直接回应了现有方法的根本瓶颈：当 ISO、设备型号等元数据缺失或跨设备不一致时，生成模型的泛化能力严重受限。

在对比方法中，**C2N** 和 **Flow-sRGB** 属于典型的元数据依赖型方法，需要显式输入设备型号和 ISO 等信息来条件化噪声生成过程。**NeCA-W** 和 **NAFlow** 作为强基线，虽然引入了更先进的生成架构（如流模型），但仍未摆脱对元数据的依赖。PNG 在 SIDD 验证集上的噪声质量评估（Table 1）显示，其平均 KLD 为 0.0194，较 NAFlow 的 0.0305 降低了 36.4%，且在所有设备类型上均取得最优。

从方法论谱系来看，PNG 可被定位为“元数据自由的噪声生成”范式的开创性工作。其两阶段训练框架——先训练 Prompt Autoencoder (PAE) 学习紧凑潜空间，再训练 Prompt DiT (P-DiT) 在潜空间中基于一致性模型（CM）进行条件生成——继承了 LDM（Latent Diffusion Models）的潜空间压缩思想，但将条件机制从文本/类别嵌入替换为从输入噪声中提取的提示特征。P-DiT 采用 DiT（Diffusion Transformer）架构，并创新性地在时间步嵌入和注意力层同时注入提示特征条件（Prompt Attention），消融实验证实这一设计对降低 KLD 和 AKLD 至关重要（Table S2）。

### 适用边界

PNG 的适用边界由以下要素共同划定：

1. **数据域限制**：当前框架仅针对 sRGB 域的真实噪声建模，未验证其在 RAW 域或视频帧上的有效性。RAW 域的噪声特性（如泊松-高斯混合分布）与 sRGB 域经过 ISP 处理后的噪声存在本质差异，直接迁移需要重新设计提示特征提取模块。

2. **训练数据依赖**：尽管 PNG 在推理阶段完全摆脱元数据依赖，但 PAE 的训练仍需成对的噪声-清洁图像。论文在补充材料中探索了非配对设置（Figure S2, Table S6-S7），但性能仍不及配对训练，说明完全无监督的噪声表示学习仍是开放问题。

3. **分辨率-速度权衡**：在高分辨率（1024×1024）下推理速度约为 5 fps，虽优于 NAFlow（约 2 fps），但仍不及 NeCA-W（约 15 fps）（Table S1）。这一差距源于 P-DiT 的 Transformer 架构在潜空间中的计算开销。

4. **设备泛化**：提示特征从 SIDD 训练集中学习传感器特定的噪声统计量，当面对训练集中未出现的相机型号或 ISP 流程时，泛化能力需要进一步验证。Table 4 在 PolyU、Nam、MAI2021 等外部数据集上的噪声质量评估显示 PNG 仍优于基线，但这些数据集的设备类型与 SIDD 存在重叠，未见完全未知设备的测试。

### 局限与开放问题

**已知局限**：

- **配对数据瓶颈**：PAE 训练仍需成对的噪声-清洁图像，这在高噪声场景或动态场景下收集成本高昂。论文的非配对实验（Table S6-S7）表明，仅在非配对设置下训练的 PNG 在 KLD 上从 0.0194 退化至 0.0285†，说明配对监督信号对 PAE 学习紧凑且有判别力的噪声表示至关重要。

- **域迁移未验证**：当前所有实验均在 sRGB 自然图像上完成，提示特征在 RAW 域、医学图像、遥感图像等不同噪声分布下的迁移能力未知。

- **生成多样性未量化**：论文主要使用 KLD 和 AKLD 评估噪声分布匹配度，但未评估生成噪声的多样性和模式覆盖能力，这对下游去噪网络的鲁棒性训练可能产生影响。

**开放问题**：

1. **能否进一步减少对配对数据的依赖？** 一个可能的方向是利用自监督或对比学习框架，仅从非配对噪声图像和任意洁净图像中学习噪声表示，或通过跨数据集的提示特征对齐实现零样本噪声生成。

2. **提示特征的跨传感器迁移能力如何？** 当前提示特征在 SIDD 训练集上学习，能否通过元学习或域自适应方法泛化到未见过的相机型号和 ISP 流程，是实现“一次训练、任意部署”的关键。

3. **框架能否扩展到盲去噪任务？** 目前 PNG 需要显式输入噪声图像以提取提示特征。在盲去噪场景中，仅有单张噪声图像可用，如何从该图像自身提取有效的提示特征并用于条件生成，是一个具有实际价值的研究方向。

4. **潜空间的可解释性**：全局提示块（GPB）和局部提示块（LPB）分别捕捉 ISO 等全局统计量和空间相关性等局部模式，但这些高维提示特征的具体语义含义尚未被深入分析，理解其与物理噪声参数的对应关系可能指导更高效的架构设计。



## 原文 PDF

![[paperPDFs/CVPR_2026/Diffusion_Based_sRGB_Real_Noise_Generation_via_Prompt_Driven_Noise_Representation_Learning.pdf]]
