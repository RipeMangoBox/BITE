---
title: "Stable Virtual Camera: Generative View Synthesis with Diffusion Models"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/Stable_Virtual_Camera_Generative_View_Synthesis_with_Diffusion_Models.pdf
aliases:
- SSVC
- SVCGVSDM
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过在训练阶段联合采样小视角和大视角变化（小步幅）的视图序列，使模型同时学习局部连续性和大范围生成能力；在推理时采用灵活的两遍程序化采样策略（首遍生成锚点帧，第二遍根据任务类型使用最近邻或插值分块生成目标帧），并通过记忆库保证长轨迹的3D一致性，从而无需任何3D表示蒸馏即可直接输出时空一致的新视图。
primary_logic: 避免在网络中引入显式3D表示，使模型能够充分继承预训练2D扩散模型的强大先验，并结合灵活的输入-目标视图条件化（Plücker嵌入、CLIP特征）和分块采样策略，实现一个通用模型同时解决集合式NVS和轨迹式NVS，支持稀疏到半稠密的任意视图数量。
claims:
- SEVA在所有基准上综合性能最优，在CAT3D自身设置下PSNR提升+1.5 dB
- 在小视角集NVS任务中，SEVA在多数划分上取得最先进结果，例如LLFF数据集上P=3时PSNR提高+6.0 dB
- 在大视角集NVS任务中，SEVA在Mip360数据集上P=3时PSNR超过CAT3D 0.6 dB
- 采用interp两遍采样相比one-pass或gt+nearest可显著减少时序闪烁，确保平滑渲染
---

# Stable Virtual Camera: Generative View Synthesis with Diffusion Models

> [!tip] 核心洞察
> 避免在网络中引入显式3D表示，使模型能够充分继承预训练2D扩散模型的强大先验，并结合灵活的输入-目标视图条件化（Plücker嵌入、CLIP特征）和分块采样策略，实现一个通用模型同时解决集合式NVS和轨迹式NVS，支持稀疏到半稠密的任意视图数量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 稳定虚拟相机：基于扩散模型的生成式视角合成 |
| 英文题名 | Stable Virtual Camera: Generative View Synthesis with Diffusion Models |
| 会议/期刊 | ICCV 2025 |
| Links | [paper](https://arxiv.org/abs/2503.14489) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | SEVA (STABLE VIRTUAL CAMERA) |
| Dataset | LLFF, Mip-NeRF 360, DL3DV |

> [!tip] 效果简介
> - 综合 (CAT3D 设置) 上，PSNR SEVA vs CAT3D (+1.5 dB)。
> - LLFF (小视角集合 NVS, P=3) 上，PSNR SEVA (提升显著) vs 先前方法 (+6.0 dB)。
> - Mip-NeRF 360 (大视角集合 NVS, P=3) 上，PSNR SEVA vs CAT3D (+0.6 dB)。

## 概述

### 问题瓶颈

新视角合成（NVS）旨在从稀疏输入图像生成任意相机姿态下的新视图。现有基于扩散模型的方法面临一个根本性矛盾：**大视角变化下的强生成能力**与**时序平滑的视图插值**难以在单一模型中兼得。具体而言，以 **CAT3D**、**ReconFusion** 为代表的方法虽然生成质量较高，但通常需要额外的3D表示（如NeRF）进行蒸馏来融合不一致的采样结果，导致流程复杂且灵活性受限——仅支持固定数量的输入/目标视图，无法处理任意稀疏到半稠密的视图配置。

### 核心方法

**SEVA（Stable Virtual Camera）** 提出了一条截然不同的路径：**避免在网络中引入任何显式3D表示**，使模型能够充分继承预训练2D扩散模型（Stable Diffusion 2.1）的强先验。其关键调控手段包括：

- **联合训练策略**：在训练阶段同时采样小视角和大视角变化的视图序列，使模型同步学习局部连续性和大范围生成能力。
- **两遍程序化采样**：推理时首遍生成锚点帧，第二遍根据任务类型（集合式或轨迹式NVS）采用最近邻或插值分块策略生成目标帧，支持任意数量的输入和目标视图。
- **记忆库机制**：通过空间最近邻查找维持长轨迹的3D一致性，无需任何3D蒸馏。

这一设计使SEVA成为一个**通用生成式渲染器**，同时覆盖集合式NVS（无序目标视图）和轨迹式NVS（有序视频序列），支持从单视图到半稠密视图的灵活输入。

### 主要结果

SEVA在涵盖10个公开数据集的综合基准上表现出一致的性能优势：

- 在CAT3D自身设置下，PSNR提升 **+1.5 dB**。
- 在小视角集合NVS任务中，LLFF数据集上P=3时PSNR提高 **+6.0 dB**。
- 在大视角集合NVS任务中，Mip-NeRF 360数据集上P=3时PSNR超过CAT3D **+0.6 dB**。
- 在轨迹NVS任务中，采用插值两遍采样可显著减少时序闪烁，确保平滑渲染。

### 方法定位

SEVA属于**基于扩散模型的生成式NVS**，与现有方法的关键区别在于：无需NeRF蒸馏、无需显式3D表示、训练数据同时覆盖物体级和场景级数据、支持灵活的输入条件化和强生成能力。在方法谱系中，它介于纯回归式方法（如 **MVSplat**、**DepthSplat**）和需要3D蒸馏的扩散方法（如 **CAT3D**、**ReconFusion**）之间，以纯2D扩散先验实现了3D一致的视图生成。

## 背景与动机

### 视角合成任务的演化与瓶颈

新视角合成（Novel View Synthesis, NVS）旨在从一组稀疏的输入图像及其对应的相机参数中，生成任意目标视角下的真实感图像。近年来，该领域沿着两条技术路线快速演进：**回归式方法**将NVS建模为确定性映射 $f_{\theta}(\mathbf{I}^{\mathrm{inp}}, \pi^{\mathrm{inp}}, \pi^{\mathrm{tgt}})$，直接从输入推断目标视图；**扩散式方法**则将其视为条件分布 $p_{\theta}(\mathbf{I}^{\mathrm{tgt}} \mid \mathbf{I}^{\mathrm{inp}}, \pi^{\mathrm{inp}}, \pi^{\mathrm{tgt}})$ 的迭代采样过程，借助预训练2D扩散模型的强先验实现更逼真的生成。

然而，现有基于扩散模型的NVS方法面临一个核心瓶颈：**难以在单个模型中同时处理大视角变化下的生成能力和时序平滑的插值过渡**。具体而言，当目标视角与输入视角之间差异较大时（即大视角变化NVS），模型需要具备强生成能力来填补未观测区域；而当目标视角沿连续相机轨迹排列时（即轨迹NVS），又要求相邻帧之间保持时序一致性，避免闪烁和跳变。现有工作通常在这两个维度上顾此失彼——例如，**ReconFusion**和**CAT3D**等基于扩散的图像NVS模型虽然生成质量较高，但依赖NeRF蒸馏来融合不一致的采样结果，流程复杂且灵活性受限（仅支持固定数量的输入/目标视图）；**ViewCrafter**和**MotionCtrl**等基于扩散的视频模型虽然在时序平滑度上表现较好，但在大视角变化场景下的生成能力不足。

### 3D表示依赖带来的灵活性缺失

更深层的问题在于，当前主流方法普遍在网络中引入显式的3D表示（如NeRF、3D Gaussian Splatting）来保证多视图一致性。这种设计虽然在一定程度上缓解了不同采样结果之间的不一致性，但带来了两个关键缺陷：

1. **流程复杂性**：需要额外的蒸馏步骤将扩散模型的采样结果融合为3D表示，再从中渲染新视图，导致端到端流程冗长且调优困难。
2. **灵活性受限**：3D表示的引入使得模型难以充分继承预训练2D扩散模型的强大先验，同时限制了模型对任意数量输入/目标视图的支持能力。如Table 1所示，现有方法在输入条件灵活性、生成能力和插值平滑度三个维度上难以兼得——回归式方法（如**MVSplat**、**DepthSplat**）通常速度快但生成质量有限，扩散式方法（如**CAT3D**、**4DiM**）生成质量高但缺乏时序平滑能力或受限于固定视图数量。

### 本文动机与核心思路

针对上述瓶颈，**SEVA（Stable Virtual Camera）** 提出了一条根本性的技术路径：**避免在网络中引入显式3D表示，使模型能够充分继承预训练2D扩散模型的强大先验，同时通过训练策略和推理采样策略的创新，实现一个通用模型同时解决集合式NVS和轨迹式NVS**。

这一动机源于一个关键洞察：预训练的2D扩散模型（如Stable Diffusion 2.1）已经蕴含了丰富的场景先验和生成能力，显式3D表示的引入反而会削弱这种先验的利用效率。SEVA的核心思路是：

- **训练阶段**：联合采样小视角和大视角变化的视图序列，使模型同时学习局部连续性和大范围生成能力，从而在单一模型中统一两种能力。
- **推理阶段**：采用灵活的两遍程序化采样策略——首遍生成锚点帧，第二遍根据任务类型使用最近邻（集合NVS）或插值分块（轨迹NVS）生成目标帧，并通过记忆库保证长轨迹的3D一致性，从而无需任何3D表示蒸馏即可直接输出时空一致的新视图。

这一设计使得SEVA在综合性能上显著超越现有方法，在CAT3D自身设置下PSNR提升+1.5 dB，在小视角集NVS的LLFF数据集上（P=3）PSNR提高+6.0 dB，在大视角集NVS的Mip360数据集上（P=3）PSNR超过CAT3D 0.6 dB。更重要的是，SEVA首次在单一模型中实现了从单视图到半稠密视图、从无序目标集合到有序视频轨迹的灵活覆盖，为生成式视角合成提供了统一的解决方案。

## 核心创新

SEVA 的核心创新在于**避免在网络内部引入显式 3D 表示**，转而通过一套精心设计的训练与推理策略，使单个通用模型同时具备大视角变化下的强生成能力与时序平滑的插值能力。这与现有主流方法形成根本性差异——**ReconFusion** 和 **CAT3D** 等基于扩散的 NVS 模型依赖 NeRF 蒸馏来融合不一致的采样结果，导致流程复杂且灵活性受限（仅支持固定数量的输入/目标视图）；而 SEVA 直接继承预训练 2D 扩散模型（SD 2.1）的强大先验，无需任何 3D 表示蒸馏即可输出时空一致的新视图。

### 关键创新点

**1. 联合训练策略：同时覆盖小视角与大视角变化**

现有方法通常以固定的大或小视点变化进行训练，难以在单一模型中兼顾局部连续性与大范围生成能力。SEVA 在训练阶段联合采样小视角变化和大视角变化（小降采样步长）的视图序列，使模型同时学习局部平滑过渡与大跨度新视图生成。这一训练策略的因果作用在于：模型在去噪过程中被迫建立从细微到剧烈的视角变化映射，从而在推理时能够灵活应对从稀疏到半稠密的任意输入视图数量（见 Sec. 3.1）。

**2. 两遍程序化采样策略：解耦锚点生成与目标帧生成**

推理时，SEVA 采用灵活的两遍程序化采样策略，这是其区别于单遍固定序列长度采样的核心机制：

- **首遍（锚点生成）**：从输入视图出发，生成一组均匀分布的锚点帧，建立场景的全局结构。
- **第二遍（目标帧生成）**：根据任务类型动态选择分块策略：
  - **集合式 NVS**（无序目标视图）：采用最近邻分块（nearest chunking），将每个目标帧分配到与其相机位姿最近的锚点帧所在块中，公式为：
    $$\mathrm{nearest}: \{ \mathbf{I}_{i}^{\mathrm{acr}} \} \cup \{ \mathbf{I}_{j}^{\mathrm{tgt}} \mid \mathrm{NN}( \mathbf{I}_{j}^{\mathrm{tgt}}, \mathbf{I}^{\mathrm{acr}} ) = \mathbf{I}_{i}^{\mathrm{acr}} \}$$
  - **轨迹式 NVS**（有序视频序列）：采用插值分块（interp chunking），将目标帧作为锚点帧之间的时序片段生成，公式为：
    $$\mathrm{interp}: \{ \mathbf{I}_{i}^{\mathrm{acr}}, \mathbf{I}_{i\cdot\Delta+1}^{\mathrm{tgt}}, \cdots, \mathbf{I}_{(i+1)\cdot\Delta-1}^{\mathrm{tgt}}, \mathbf{I}_{i+1}^{\mathrm{acr}} \}$$

消融实验（Fig. 7, Table 6）证实：interp 程序化采样相比 one-pass 或 gt+nearest 策略可显著减少时序闪烁，确保平滑渲染。

**3. 记忆库机制：保障长轨迹的 3D 一致性**

当目标视图数量远超训练上下文窗口长度 $T$ 时，锚点帧本身也会被分块到不同的前向传播中，导致锚点间不一致。SEVA 引入记忆库（memory bank），维护已生成锚点帧及其相机位姿，并通过**空间最近邻查找**（而非时间最近邻）检索相关锚点进行自回归生成。消融实验（Fig. 8）表明，空间最近邻查找显著改善了长程循环轨迹的视图一致性，减少了不同循环中重复位置处出现的伪影。

**4. 无需显式 3D 表示的架构设计**

SEVA 的网络架构基于预训练 SD 2.1 的自编码器与潜在去噪 U-Net，通过以下模块实现多视图生成，而无需引入 NeRF 或 3DGS 等显式 3D 表示：

- **3D 自注意力块**：将 2D 自注意力膨胀为 3D，实现跨视图交互。
- **1D 视图轴自注意力**：增强视图间信息聚合。
- **可选的 3D 卷积时序通路**：当帧有序时提升时序平滑度。
- **Plücker 嵌入相机条件化**：通过拼接和自适应层归一化注入相机姿态。
- **CLIP 图像嵌入注入**：提供高层语义信息。

这种设计使模型能够充分继承预训练 2D 扩散模型的强大先验，同时避免 3D 表示蒸馏带来的流程复杂性和灵活性损失。

### 创新点的因果链条

上述创新点构成一条完整的因果链：**联合训练策略**赋予模型同时处理小视角和大视角变化的能力 → **两遍程序化采样**将这一能力解耦为结构锚定与细节填充两个阶段 → **记忆库机制**确保在超长序列生成中锚点间的一致性 → **无 3D 表示的架构**使整个过程无需额外的 3D 蒸馏步骤。这一链条最终使 SEVA 成为一个通用模型，能够同时解决集合式 NVS 和轨迹式 NVS，支持从稀疏到半稠密的任意视图数量，并在 CAT3D 自身设置下实现 +1.5 dB PSNR 的综合性能提升。

## 整体框架

SEVA 的整体设计遵循一个核心原则：**不在网络内部引入显式三维表示**，从而最大程度继承预训练 2D 扩散模型的强大先验。如图 4 所示，系统以 Stable Diffusion 2.1 的自编码器与潜在去噪 U‑Net 为骨架，将 2D 自注意力膨胀为 **3D 自注意力**，并额外插入 **1D 视图轴自注意力** 以实现跨视图信息交互。当输入帧具有明确时序关系时，可进一步在每个残差块后通过跳跃连接引入 **3D 卷积时序通路**，将模型驯化为视频模型（总参数量约 1.5B）。相机姿态通过 **Plücker 嵌入** 以拼接和自适应层归一化的方式注入，同时利用 **CLIP 图像嵌入** 提供高层语义条件。

训练阶段，模型以固定序列长度 $T = M + N$ 的 “M‑in N‑out” 多视图扩散范式进行学习，其中 $M$ 和 $N$ 分别为单次前向中的输入帧数与目标帧数。关键的设计选择在于 **视图采样策略**：训练时联合覆盖小视角变化和大视角变化，并采用较小的降采样步长，使模型同时习得局部连续性和大范围生成能力。

推理阶段，SEVA 被重构为一个灵活的 “P‑in Q‑out” 生成式渲染器，其中 $P$ 和 $Q$ 无需等于训练时的 $M$ 和 $N$。当 $P + Q \le T$ 时，通过重复首张输入图像将前向过程填充至恰好 $T$ 帧，以避免改变上下文窗口长度带来的分布偏移。当目标视图数量 $Q$ 远超 $T$ 时，系统采用 **两遍程序化采样** 策略：首遍生成锚点帧，第二遍根据任务类型（集合式或轨迹式）使用最近邻或插值分块策略生成目标帧。对于极长轨迹，系统维护一个 **记忆库**，存储已生成的锚点帧及其相机姿态，并通过空间最近邻查找实现自回归式锚点生成，从而在多个前向过程之间维持长程三维一致性。

整个 pipeline 的输入为任意数量的源视图及其对应相机参数，输出为时空一致的新视图序列，无需任何 NeRF 或 3DGS 蒸馏后处理即可直接使用。

### 补充图表

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2503_14489/figures/005_Figure_4.jpg]]
*Figure 4: Method. SEVA is trained with fixed sequence length as a “M-in N-out” multi-view diffusion model with standard architecture. It conditions on CLIP embeddings, VAE latents of the input views, and their corresponding camera poses. During sampling, SEVA can be cast as a generative “P -in Q-out” renderer that works with variable sequence length, where P and Q need not be equal to M and N. To enhance temporal and 3D consistency across generated views, especially when generating along a trajectory, we present procedural two-pass sampling as a general strategy*

## 核心模块与公式推导

SEVA 的核心架构建立在预训练 Stable Diffusion 2.1 的自编码器与潜在去噪 U-Net 之上，通过三个关键改造将其转化为一个通用的“M-in N-out”多视图扩散模型。

### 基础生成范式

SEVA 采用扩散式新视角合成范式，将目标视图的生成建模为条件分布：

$$p_{\theta}\left(\mathbf{I}^{\mathrm{tgt}} \mid \mathbf{I}^{\mathrm{inp}}, \pi^{\mathrm{inp}}, \pi^{\mathrm{tgt}}\right)$$

其中 $\mathbf{I}^{\mathrm{inp}}$ 为输入视图集合，$\pi^{\mathrm{inp}}$ 和 $\pi^{\mathrm{tgt}}$ 分别为输入与目标视图对应的相机参数。模型从该条件分布中迭代去噪采样，生成目标视图 $\mathbf{I}^{\mathrm{tgt}}$。与之对比，传统的回归式方法将 NVS 建模为确定性映射 $f_{\theta}\left(\mathbf{I}^{\mathrm{inp}}, \pi^{\mathrm{inp}}, \pi^{\mathrm{tgt}}\right)$，缺乏对未观测区域的不确定性建模能力。

### 训练上下文窗口

SEVA 以固定序列长度进行训练，单次前向传播处理的帧总数定义为：

$$T = |\mathbf{I}^{\mathrm{inp}}| + |\mathbf{I}^{\mathrm{tgt}}| = M + N$$

其中 $M$ 为输入视图数量，$N$ 为目标视图数量。训练时 $T$ 保持固定（例如 $T=8$），但推理阶段通过两遍程序化采样策略可突破此限制，支持任意数量的输入与目标视图。

### 3D 自注意力与视图轴注意力

为在无显式 3D 表示的前提下实现跨视图信息交互，SEVA 对 U-Net 的每个低分辨率残差块进行了两项关键改造：

1. **3D 自注意力膨胀**：将原始的 2D 自注意力膨胀为 3D 自注意力，使不同视图的潜在特征能够在空间维度上联合交互。这是将 2D 扩散模型转化为多视图生成模型的核心操作。

2. **1D 视图轴自注意力**：在 3D 自注意力的基础上，额外引入沿视图轴的 1D 自注意力层，专门增强视图间的信息聚合能力，提升生成视图的 3D 一致性。

### 可选时序通路

当目标视图构成有序轨迹时，SEVA 可在每个残差块后通过跳跃连接引入 3D 卷积，将基础模型转化为视频模型变体。该变体总参数量约 1.5B，专门提升时序平滑度，在轨迹 NVS 任务中表现出显著的时序质量增益（见 Table 6 中 temp. 变体的 TSED 和 MS 指标）。

### 相机条件化

相机姿态通过 Plücker 嵌入注入网络：将 Plücker 坐标与潜在特征拼接后通过自适应层归一化（Adaptive Layer Normalization）进行调制。同时，输入视图的 CLIP 图像嵌入被注入以提供高层语义信息，帮助模型理解场景内容。

### 程序化采样中的分块策略

推理阶段的两遍采样依赖于两种分块策略，将目标视图分配到训练窗口大小 $T$ 的块中进行生成：

- **最近邻分块**（集合 NVS）：

$$\mathrm{nearest}: \{ \mathbf{I}_{i}^{\mathrm{acr}} \} \cup \{ \mathbf{I}_{j}^{\mathrm{tgt}} \mid \mathrm{NN}( \mathbf{I}_{j}^{\mathrm{tgt}}, \mathbf{I}^{\mathrm{acr}} ) = \mathbf{I}_{i}^{\mathrm{acr}} \}$$

通过计算目标帧与锚点帧的相机姿态最近邻，将每个目标帧分配到与其空间位置最接近的锚点帧所在块中。

- **插值分块**（轨迹 NVS）：

$$\mathrm{interp}: \{ \mathbf{I}_{i}^{\mathrm{acr}}, \mathbf{I}_{i\cdot\Delta+1}^{\mathrm{tgt}}, \cdots, \mathbf{I}_{(i+1)\cdot\Delta-1}^{\mathrm{tgt}}, \mathbf{I}_{i+1}^{\mathrm{acr}} \}$$

将目标帧作为相邻锚点帧之间的插值片段进行生成，其中 $\Delta$ 为锚点采样步长。该策略确保相邻帧在同一个前向传播中生成，从而保证时序平滑性。

### 记忆库机制

当目标视图数量 $Q \gg T$ 时，首遍生成的锚点帧本身也会被分块到不同的前向传播中，导致锚点间不一致。SEVA 维护一个记忆库，存储已生成的锚点视图及其相机姿态，后续锚点通过检索其空间最近邻进行自回归生成，从而维持长程 3D 一致性。

### 填充策略

当实际帧数 $P+Q < T$ 时，SEVA 通过重复第一个输入视图将前向传播填充至恰好 $T$ 帧，而非动态改变上下文窗口长度。消融实验（Fig. 14）表明，这种填充策略有效避免了改变 $T$ 带来的注意力分布偏移伪影。

## 实验与分析

### 核心实验设置

SEVA在涵盖物体级和场景级的10个公开数据集上进行了系统评估（Table 7），根据输入视图与目标视图之间的视点差异，将新视角合成（NVS）任务划分为**小视角集合NVS**和**大视角集合NVS**，并额外引入**轨迹NVS**以评估时序平滑度。模型基于Stable Diffusion 2.1骨架，以固定上下文窗口长度 $T = M + N$ 训练（$M$ 个输入帧，$N$ 个目标帧），训练图像分辨率为 $576 \times 576$。推理时采用两遍程序化采样，支持任意 $P$ 个输入视图和 $Q$ 个目标视图的灵活生成，并利用记忆库维持长程3D一致性。

### 集合NVS主结果

**小视角集合NVS**（Table 2）：SEVA在绝大多数划分上取得最优PSNR。在LLFF数据集上，$P=3$ 时PSNR提升高达 **+6.0 dB**，展现了在小视点变化下强大的重建保真度。在T&T数据集上半稠密视图区域，SEVA与最先进方法的差距仅为1.7 dB，考虑到SEVA未针对半稠密输入专门设计，该结果具有竞争力。在OO3D上，$P=3$ 时SEVA达到30.30 PSNR。

**大视角集合NVS**（Table 3）：SEVA在Mip-NeRF 360数据集上 $P=3$ 时PSNR达到17.82，超过此前最优方法**CAT3D** **+0.6 dB**。在CAT3D自身设置下的综合对比中，SEVA以 **+1.5 dB PSNR** 的显著优势一致超越先前工作。这一结果表明，SEVA无需任何3D表示蒸馏即可有效处理大视点变化下的生成任务。

**定性对比**（Figure 6）：与开源方法ViewCrafter、DepthSplat以及闭源方法LVSM、Long-LRM、4DiM、CAT3D相比，SEVA在集合NVS和轨迹NVS任务上均生成了更逼真且一致的新视图，尤其在多视图输入条件下，目标视图与输入视图的视觉连续性明显更优。

### 轨迹NVS与时序质量

在轨迹NVS任务上（Table 5），SEVA在RE10K、WRGBD、DL3DV三个数据集上进行了评估。当启用可选的3D卷积时序通路时，模型在DL3DV上达到PSNR 15.78、TSED 109.0、运动平滑度（MS）95.77（Table 6）。时序通路的引入显著提升了视频生成的平滑度，但基础模型本身已具备相当的时序一致性。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2503_14489/figures/011_Table_5.jpg]]
*Table 5: PSNR↑ on trajectory NVS. temp. denotes optional temporal pathway. RE, WR, and DL denotes RE10K, WRGBD, and DL3DV, respectively. For the V [9] split, P = 1 with unit length swept; for the O split, P = 3. Underlined numbers are run by us using the officially released code*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2503_14489/figures/013_Table_6.jpg]]
*Table 6: 3D consistency (TSED↓ and PSNR↑) and temporal quality (MS↑) on trajectory NVS. SEVA uses interp procedural sampling by default. temp. denotes the optional temporal pathway. MS denotes motion smoothness from VBench [52]. Results are reported on our split of DL3DV with P = 3*

**采样策略消融**（Figure 7）：对比三种采样策略——单遍（one-pass）、真值+最近邻（gt+nearest）和插值（interp）——垂直切片显示，one-pass和gt+nearest在相邻视点间产生明显闪烁伪影，而interp策略确保了时序平滑渲染。这是SEVA实现流畅相机轨迹的核心机制。

**记忆库查找策略**（Figure 8）：在TELEPHONE-BOOTH场景上循环三圈的长程轨迹测试中，使用空间最近邻查找的记忆库相比时间最近邻查找，显著改善了回访位置的视图一致性，减少了跨圈累积的伪影。这验证了空间感知的记忆库对长程3D一致性的关键作用。

### 关键消融与设计选择

**上下文窗口零样本扩展**（Figure 9）：在半稠密视图区域，零样本扩展上下文窗口长度 $T$ 可提升PSNR和图像质量。然而，在稀疏视图下扩展 $T$ 仍存在性能下降，表明训练时固定 $T$ 与推理时动态 $T$ 之间的注意力分布偏移尚未完全消除。

**填充策略**（Figure 14）：当 $P+Q < T$ 时，通过重复第一个输入视图进行填充（padding）相比改变 $T$ 能有效避免分布偏移伪影，这是工程实现中的重要细节。

**CFG尺度**（Figure 11）：无分类器引导（CFG）尺度在2到5之间产生高质量结果。单视图条件化通常需要更高的CFG尺度（如5-8）以应对更大的生成不确定性，而多视图条件化在较低CFG下即可获得稳定输出。

**生成多样性**（Figure 12）：通过改变随机种子，SEVA能够在未观测区域生成多样化的合理预测，体现了扩散模型的固有优势。

### 失败模式与局限性

1. **长轨迹远端饱和**：当目标视图与输入视图无内容重叠时，生成结果逐渐饱和，远端视图质量下降。
2. **单视图尺度歧义**：在RealEstate10K等数据集上，单视图输入存在尺度歧义，需手动扫描相机归一化的单位长度以获取最佳结果。
3. **训练分辨率限制**：模型仅在 $576 \times 576$ 正方形图像上训练，虽可零样本泛化到不同纵横比和分辨率（Figure 10），但在极端分辨率下可能出现退化。
4. **上下文窗口固定**：训练时固定的 $T$ 导致零样本扩展时存在注意力分布偏移，动态 $T$ 训练是否是解决方案仍是一个开放问题。
5. **预训练先验继承**：模型依赖SD 2.1的预训练先验，可能继承其数据偏见。

### 与3DGS渲染的对比

SEVA生成的样本与3DGS渲染结果在感知上极为接近（Figure 13），差异极小。在3DGS渲染的定量评估中（Table 4），SEVA同样展现了竞争力，表明扩散模型生成的视图在视觉真实感上已逼近传统重建方法。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2503_14489/figures/009_Table_3.jpg]]
*Table 3: PSNR↑ on large-viewpoint set NVS. For all results with P = 1, we sweep the*

### 补充图表

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2503_14489/figures/012_Figure_7.jpg]]
*Figure 7: Temporal quality. Vertical slices of a rendered novel camera path on the BONSAI scene from Mip-NeRF360 [42] illustrate the temporal quality across adjacent viewpoints. One-pass or gt + nearest procedural sampling results in notable flickering, whereas interp procedural sampling ensures temporally smooth rendering*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2503_14489/figures/010_Figure_6.jpg]]
*Figure 6: SOTA comparison on set NVS (top) and trajectory NVS (bottom) across varying numbers of input views. We compare with open-source approaches—ViewCrafter [9] (VC) and DepthSplat [45] (DS)—as well as proprietary ones including LVSM [11], Long-LRM [18] (LLRM), 4DiM [12], and CAT3D [8]. When the input comprises multiple views, we arrange them so that the view closest to the target is placed at the top of each set*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2503_14489/figures/008_Table_2.jpg]]
*Table 2: PSNR↑ on small-viewpoint set NVS. P denotes the number of input views. For all results with*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2503_14489/figures/014_Figure_9.jpg]]
*Figure 9: Generation quality on the number of input views. PSNR↑ (top) and Image Quality↑ (bottom) on set NVS. Results are reported on our split of T&T. Extending T to more input views in a zero-shot manner produces more consistent samples in the semi-dense-view regime. Dense 3DGS denotes results of [3] with full views*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2503_14489/figures/018_Figure_11.jpg]]
*Figure 11: Generation uncertainty on CFG. The CFG scale should be increased as generation uncertainty rises. For singleview conditioning (top), a higher CFG scale is typically required, whereas few-view conditioning (bottom) benefits from a lower scale*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2503_14489/figures/024_Figure_14.jpg]]
*Figure 14: Padding. Padding the last elements within one forward reduces artifacts compared to changing T*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2503_14489/figures/003_Figure_2.jpg]]
*Figure 2: Diverse camera control. SEVA generates photorealistic novel views following diverse camera trajectories. This includes orbit, spiral, zoom out, dolly zooms, and any user-specified trajectories. Please visit our website for more visual results*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2503_14489/figures/015_Figure_8.jpg]]
*Figure 8: Long-range 3D consistency. We visualize samples following a camera path looping three times around the TELEPHONE-BOOTH scene. Lookup using spatial neighbors from the memory bank (ours) notably improves view consistency and reduces artifacts in recurring locations across different loops, compared to lookup using temporal neighbors (baseline)*

## 方法谱系与知识库定位

### 1. 核心定位：生成式NVS的范式转移

SEVA 代表了一种从“重建-渲染”范式向“纯生成式”范式转移的趋势。传统方法（如 ZipNeRF、MVSplat、DepthSplat）依赖显式3D表示（NeRF、3DGS）或多视图几何约束，通过回归模型确定性地映射输入视图到目标视图。这类方法的优势在于几何保真度高，但生成能力受限于输入视图覆盖的区域，且在稀疏输入下易产生模糊或空洞。

扩散式NVS方法（如 CAT3D、ReconFusion、4DiM）引入了2D扩散先验以增强生成能力，但多数仍需后续的NeRF蒸馏来融合不一致的采样结果，导致流程复杂且灵活性受限——通常仅支持固定数量的输入/目标视图。SEVA 的关键突破在于：**完全避免在网络内引入显式3D表示**，使模型能够充分继承预训练2D扩散模型（SD 2.1）的强大先验，同时通过训练和采样策略的创新，直接输出时空一致的多视图，无需任何后处理蒸馏。

### 2. 与现有工作的关系图谱

| 维度 | 代表性工作 | 与SEVA的关系 |
|------|-----------|-------------|
| **回归式稀疏视图NVS** | MVSplat, DepthSplat | SEVA在稀疏输入下生成能力更强，但几何精度可能不及专用回归模型 |
| **扩散式图像NVS + NeRF蒸馏** | CAT3D, ReconFusion | SEVA直接输出一致多视图，省去蒸馏步骤，流程更简洁 |
| **扩散式视频NVS** | ViewCrafter, MotionCtrl, SV3D | SEVA同时支持集合式和轨迹式NVS，通用性更强 |
| **单视图NVS** | ZeroNVS | SEVA在单视图设置下需要CFG调整和相机归一化扫描，存在尺度歧义 |
| **大型回归式重建** | Long-LRM, LVSM | SEVA在生成多样性和大视角变化下表现更优，但半稠密输入下可能不及专用模型 |
| **稠密视图重建** | ZipNeRF | SEVA无需稠密输入即可生成合理新视图，但重建精度有上限 |

### 3. 方法创新的因果机制

SEVA 的核心创新可归结为三个相互耦合的因果旋钮：

**旋钮一：联合训练小/大视角变化。** 现有方法通常以固定的大或小视点变化进行训练，导致模型要么擅长局部插值但缺乏大范围生成能力，要么反之。SEVA 在训练阶段精心设计视图选择策略，同时覆盖小步幅和大步幅的视图序列，使模型在单一训练过程中同时学习局部连续性和大范围生成能力。这一设计是SEVA能够同时胜任小视角集合NVS和大视角集合NVS的根本原因。

**旋钮二：两遍程序化采样策略。** 推理时，SEVA 采用灵活的“锚点生成+目标帧填充”两遍策略：首遍生成空间均匀分布的锚点帧，第二遍根据任务类型使用最近邻（集合NVS）或插值分块（轨迹NVS）生成目标帧。这一策略的关键优势在于：(1) 支持任意数量的输入/目标视图，突破了训练时固定窗口长度 $T = M + N$ 的限制；(2) 插值分块策略显著减少时序闪烁，确保平滑渲染（Fig. 7 垂直切片对比验证）。

**旋钮三：记忆库机制。** 当目标视图数量远超训练窗口 $T$ 时，锚点帧本身也需要分块生成，导致跨块不一致。SEVA 维护一个记忆库，存储已生成的锚点帧及其相机姿态，并通过空间最近邻查找（而非时间最近邻）进行自回归生成。这一设计显著改善了长程循环轨迹的视图一致性（Fig. 8 电话亭场景三圈循环对比验证）。

### 4. 适用边界与能力边界

**强项场景：**
- 稀疏到半稠密输入（1-9个输入视图）下的新视图生成
- 大视角变化下的合理内容预测（Mip360上P=3时PSNR超越CAT3D +0.6 dB）
- 长相机轨迹的平滑视频渲染（interp采样策略确保时序一致性）
- 多样化相机控制（轨道、螺旋、变焦、滑轨变焦等，Fig. 2）
- 零样本分辨率/纵横比泛化（Fig. 10，肖像和风景模式均可处理）

**弱项与限制：**
- **长轨迹远端饱和：** 当目标视图与输入视图无内容重叠时，生成结果逐渐饱和，影响远端视图质量（论文明确指出的限制）。
- **单视图尺度歧义：** 在RealEstate10K等数据集上，单视图输入时存在尺度歧义，需要手动扫描相机归一化参数（实验中通过单位长度扫描缓解，但非根本解决）。
- **训练分辨率固定：** 仅支持正方形图像训练（576×576），虽可零样本泛化到其他分辨率，但可能存在退化。
- **上下文窗口分布偏移：** 训练时使用固定 $T$，推理时零样本扩展 $T$ 可能导致注意力分布偏移（通过重复第一输入视图的填充策略缓解，Fig. 14）。
- **半稠密输入非最优：** 在半稠密视图区域（如T&T数据集），SEVA落后专用回归方法约1.7 dB PSNR，因其未针对此类输入进行专门设计。

### 5. 开放问题与未来方向

1. **远端饱和问题的根本解决：** 如何在长轨迹NVS中维持远端视图的生成质量？可能需要引入层次化生成策略或条件化机制的改进。

2. **动态上下文窗口训练：** 训练时动态改变 $T$ 能否完全消除零样本扩展时的注意力分布偏移？这是提升模型灵活性的关键方向。

3. **稀疏视图下的半稠密扩展：** 如何在保持稀疏输入灵活性的同时，提升半稠密视图区域的生成精度？可能需要混合回归-生成策略。

4. **多数据集规模化训练：** 论文未探索SEVA在更大规模、更多样化数据集上的扩展性，这是验证方法通用性的重要方向。

5. **动态场景与4D视图合成：** SEVA 当前仅处理静态场景，能否扩展到时变内容（动态场景、4D NVS）是自然的延伸方向。

6. **预训练模型偏见的继承：** SEVA 依赖SD 2.1先验，可能继承其数据偏见和生成伪影，如何缓解这一问题值得进一步研究。

## 原文 PDF

![[paperPDFs/ICCV_2025/Stable_Virtual_Camera_Generative_View_Synthesis_with_Diffusion_Models.pdf]]