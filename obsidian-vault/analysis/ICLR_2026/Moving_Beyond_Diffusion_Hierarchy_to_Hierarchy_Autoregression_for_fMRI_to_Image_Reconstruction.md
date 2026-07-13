---
title: "Moving Beyond Diffusion: Hierarchy-to-Hierarchy Autoregression for fMRI-to-Image Reconstruction"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Moving_Beyond_Diffusion_Hierarchy_to_Hierarchy_Autoregression_for_fMRI_to_Image_Reconstruction.pdf
project_link: null
code_link: https://github.com/XuZhang2/MindHier
openreview_forum_id: AT7hCh6HB7
aliases:
- MBDHHAFIR
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "采用层次化fMRI编码器提取多尺度特征，结合层次到层次对齐和尺度感知的粗到细神经引导，将全局语义注入低分辨率生成阶段，细节特征注入高分辨率阶段。"
primary_logic: "通过将fMRI信号解耦为层次化嵌入，并与CLIP视觉编码器的层级对齐，再利用尺度自回归模型的逐尺度生成特性，实现符合人类感知“先森林后树木”的粗到细重建过程。"
claims:
- "层次化全监督相比单层特征在Subject 1上CLIP分数大幅提升（97.2% vs 95.1%），且所有指标均改善。"
- "粗到细引导策略优于倒置的细到粗策略，CLIP 97.2% vs 96.1%，SwAV 0.321 vs 0.330，验证尺度感知注入的必要性。"
- "在NSD测试集上，MindHier（无辅助特征）取得了最高CLIP分数96.4%和最低SwAV距离0.329，同时推理仅需2.64秒，比MindEye2快约4.67倍。"
- "NSD (1,000 shared test images) 上 CLIP两方向识别准确率 (%) = 96.4"
---

# Moving Beyond Diffusion: Hierarchy-to-Hierarchy Autoregression for fMRI-to-Image Reconstruction

> [!tip] 核心洞察
> 通过将fMRI信号解耦为层次化嵌入，并与CLIP视觉编码器的层级对齐，再利用尺度自回归模型的逐尺度生成特性，实现符合人类感知“先森林后树木”的粗到细重建过程。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 超越扩散：面向fMRI图像重建的层次到层次自回归 |
| 英文题名 | Moving Beyond Diffusion: Hierarchy-to-Hierarchy Autoregression for fMRI-to-Image Reconstruction |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=AT7hCh6HB7) · [GitHub](https://github.com/XuZhang2/MindHier) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | MindHier |
| Dataset | NSD (1, 000 shared test images), NSD, THINGS-fMRI test set |

> [!tip] 效果简介
> - NSD (1,000 shared test images) 上，CLIP两方向识别准确率 (%) 为 96.4，对比 93.0 (MindEye2)，变化 +3.4。
> - NSD 上，SwAV距离 (越低越好) 为 0.329，对比 0.344 (MindEye2)，变化 -0.015。
> - NSD 上，推理时间 (秒/图) 为 2.64，对比 12.14 (MindEye2)，变化 -78%。

## 概要

### 问题背景与核心瓶颈

从功能性磁共振成像（fMRI）信号重建人类视觉感知的图像，是连接神经科学与计算机视觉的关键任务。现有主流方法——尤其是基于扩散模型的重建管线——依赖一个单一、静态的神经嵌入（通常映射到CLIP空间）作为固定引导条件，贯穿整个生成过程。这种设计存在根本性失配：fMRI信号本身蕴含从全局语义到局部细节的层次化信息，而图像生成本质上是一个“先森林后树木”的粗到细过程。固定引导无法利用这一层次结构，导致重建在语义保真度和细节还原之间难以兼顾。

### 核心方法：MindHier

本文提出**MindHier**，一个“层次到层次自回归”框架，从三个层面系统性地解决上述瓶颈：

1. **层次化fMRI编码器（HFE）**：将fMRI信号编码为多尺度特征序列 $\{\mathbf{e}_1, ..., \mathbf{e}_M\}$，逐层提取从局部细节到全局语义的信息。
2. **层次到层次对齐**：通过级联MSE损失（结构对齐）与SoftCLIP损失（语义对齐），将HFE各层输出与CLIP视觉编码器的对应层特征建立逐层对应关系。
3. **尺度感知的粗到细神经引导**：在尺度自回归模型（VAR）的逐尺度生成过程中，根据当前尺度 $k$ 选择对应的fMRI特征 $\mathbf{s}_k$ 作为条件——粗尺度（低分辨率）注入高层语义，细尺度（高分辨率）注入低层细节，实现符合人类感知逻辑的重建。

### 方法定位

MindHier属于**fMRI到图像重建**任务，在方法谱系中处于扩散式重建的替代方案位置。与基于扩散的SOTA方法（如**MindEye2**，Scotti et al., ICML 2024）相比，MindHier的核心变革在于：

- **生成范式**：从扩散模型转向尺度自回归模型（VAR），以“下一尺度预测”替代迭代去噪。
- **引导机制**：从单一固定嵌入转向层次化、尺度感知的动态注入。
- **对齐策略**：从终端特征对齐转向层次到层次的逐层对齐。

### 核心结论

在NSD测试集上，MindHier取得了**CLIP两方向识别准确率96.4%**和**SwAV距离0.329**的最优高层语义指标，同时推理仅需**2.64秒/图**，比MindEye2快约4.67倍。消融实验证实：层次化全监督、粗到细引导策略以及均衡的CLIP层映射是性能提升的关键驱动因素。此外，单样本生成（N=1）即可获得CLIP 95.0%的强确定性结果，验证了模型无需多次采样即可稳定重建。在THINGS-fMRI跨数据集测试中，MindHier同样显著优于BrainFlora（CLIP 73.1% vs 57.6%），展现出一定的泛化能力。

### 主要局限

尽管高层语义指标领先，MindHier仍存在若干固有限制：无法重建可读文字和特定标识；面部特征模糊，缺乏身份识别精度；精细计数和材质属性容易出错；跨受试者少样本微调时性能大幅下降。这些问题为后续研究指明了方向。

从功能磁共振成像（fMRI）信号中重建人类视觉体验，是连接神经科学与计算机视觉的核心挑战。fMRI通过非侵入方式记录血氧水平依赖（BOLD）信号，反映大脑对视觉刺激的响应模式。然而，fMRI信号具有低信噪比、低空间分辨率和高个体差异性等特点，使得从这些信号中恢复出具有语义保真度和视觉细节的图像成为极具难度的逆向问题。

近年来，深度生成模型的引入显著推动了fMRI-to-image重建领域的发展。主流方法将这一任务建模为条件生成问题：先将fMRI信号编码为神经嵌入，再以此作为条件引导生成模型重建图像。**MindEye1**（Scotti et al., NeurIPS 2023）和**MindEye2**（Scotti et al., ICML 2024）是该范式的代表性工作，它们将fMRI信号映射为单一的CLIP空间向量，然后通过扩散模型（如Stable Diffusion）进行图像生成。**BrainDiffuser**（Sci. Rep. 2023）和**MindBridge**（Wang et al., CVPR 2024）也遵循类似的扩散引导框架。

然而，这一范式存在一个根本性的瓶颈：**使用单一的、静态的神经嵌入作为固定引导**。扩散模型的去噪过程从纯噪声开始，逐步注入细节，这一生成过程天然具有从全局语义到局部细节的阶段性特征。但现有方法在整个生成过程中仅使用同一个固定特征向量，无法利用fMRI信号中蕴含的层次化信息。人类视觉系统本身也是从“先森林后树木”的方式组织感知——先把握场景的全局语义，再逐步关注局部细节。现有方法将fMRI信号压缩为单一向量，抹平了这种层次性，导致神经引导与生成阶段的需求之间产生结构性错配。

此外，扩散模型的迭代去噪机制带来了高昂的推理成本。MindEye2生成单张图像约需12.14秒，限制了该技术在实际应用中的可部署性。

针对上述缺口，MindHier提出一个核心洞察：**将fMRI信号解耦为层次化嵌入，与CLIP视觉编码器的层级结构对齐，再利用尺度自回归模型逐尺度生成的特性，实现符合人类感知的粗到细重建过程**。这一思路从三个层面突破现有范式：第一，设计层次化fMRI编码器，从脑信号中显式提取多尺度特征；第二，通过层次到层次对齐，将编码器各层输出与CLIP视觉编码器的对应层建立结构-语义双重监督；第三，在尺度自回归生成中，按尺度感知方式注入层次化特征——粗尺度阶段接收高层语义嵌入以建立全局布局（“森林”），细尺度阶段接收低层细节嵌入以逐步细化纹理（“树木”），如图1所示。

这一设计不仅实现了语义保真度与视觉细节的更好平衡，还因尺度自回归模型的高效推理特性（单次前向即可完成生成），将推理速度提升约4.67倍，为fMRI-to-image重建的实用化提供了新的可能性。

## 核心方法与创新机理

MindHier的核心创新在于**将fMRI信号解耦为层次化神经嵌入，并以尺度感知的方式注入自回归生成过程**，从而替代了现有扩散方法中“单一、静态嵌入固定引导”的范式。这一转变直接针对了当前fMRI-to-image重建的根本瓶颈：扩散模型使用的固定CLIP嵌入无法利用fMRI信号的层次信息，且与图像重建从全局语义到局部细节的阶段需求不对齐。

### 关键创新点

**1. 层次化fMRI编码器（Hierarchical fMRI Encoder）**

传统方法（如MindEye2, Scotti et al., ICML 2024）将fMRI信号映射为单个CLIP空间向量，丢失了大脑信号中从局部细节到全局语义的多尺度信息。MindHier设计了由M个级联Transformer块组成的统一编码器，输出层次化特征序列 $\{\mathbf{e}_1, ..., \mathbf{e}_M\}$，其中浅层块捕获局部细节，深层块提取全局语义。这一设计使得fMRI信号的自然层次结构得以保留和利用。

**2. 层次到层次对齐（Hierarchy-to-Hierarchy Alignment）**

不同于基线方法仅对齐终端特征与CLIP嵌入，MindHier采用双重监督策略实现层次到层次的对应：
- **结构对齐**：通过级联MSE损失 $\mathcal{L}_{\mathrm{MSE}} = \sum_{m=1}^{M} \| \ell_{2}(\mathbf{e}_{m}) - \ell_{2}(\mathbf{v}_{g_{m}}) \|_{2}^{2}$，将HFE各层输出与CLIP视觉编码器对应层特征对齐，确保从浅层到深层的结构一致性。
- **语义对齐**：通过SoftCLIP对比损失，将终端fMRI嵌入 $\mathbf{e}_M$ 同时与视觉嵌入和文本嵌入对齐，强化高层语义保真度。

**3. 尺度感知的粗到细神经引导（Scale-Aware Coarse-to-Fine Neural Guidance）**

这是MindHier最具区分度的创新。基于尺度自回归模型（VAR）的“下一尺度预测”范式，MindHier在生成过程中根据当前尺度 $k$ 选择对应的fMRI特征 $\mathbf{s}_k$ 作为条件：粗尺度（低分辨率）接收高层语义嵌入，建立“森林”般的全局布局；细尺度（高分辨率）接收低层细节嵌入，逐步精炼“树木”般的局部纹理。这一策略通过选择性注意力掩码实现，使得信息流严格遵循“先全局后局部”的顺序。

消融实验（Table 4）强有力地验证了这一设计的必要性：将引导策略倒置为“细到粗”时，CLIP识别准确率从97.2%降至96.1%，SwAV距离从0.321升至0.330，证明粗到细的信息流顺序对高保真重建至关重要。

**4. 生成范式的根本转变**

MindHier用尺度自回归模型替代了扩散模型，带来了两个关键优势：
- **推理效率大幅提升**：单张图像推理仅需2.64秒，比MindEye2快约4.67倍（Table 1）。这是因为层次化编码器一次前向即可生成所有特征，且自回归模型将主要计算集中在低分辨率尺度。
- **生成确定性增强**：单样本生成（N=1）即可获得CLIP 95.0%的强结果（Table S5），避免了扩散模型多次采样的随机性和计算开销。

### 方法谱系与知识库定位

MindHier处于fMRI-to-image重建、层次化表示学习和自回归生成模型的交叉点。相对于现有工作：

- **对比扩散式方法**（MindEye1/2, BrainDiffuser）：MindHier摒弃了固定嵌入引导和迭代去噪范式，转而利用层次化嵌入与尺度自回归的天然契合，实现了更高效、更符合感知过程的粗到细重建。
- **对比桥接对齐方法**（MindBridge, Wang et al., CVPR 2024）：MindHier不仅关注语义对齐，还通过层次到层次的结构对齐捕获了从纹理到语义的全谱信息。
- **生成模型选择**：基于VAR的尺度自回归为fMRI引导提供了离散的控制点，使得层次化特征的注入具有明确的尺度对应关系，这是扩散模型难以实现的。

综上，MindHier的核心创新并非单一技术的堆叠，而是通过“层次化编码-层次化对齐-尺度感知引导”三位一体的设计，系统性地解决了fMRI信号层次信息利用不足的问题，实现了从“森林”到“树木”的粗到细重建。

*Figure 2: Overview of the two-stage training pipeline of MindHier. (a) Stage 1: Hierarchy-to-Hierarchy Alignment. A hierarchical fMRI encoder (composed of M cascaded blocks) is trained to map fMRI signals to a feature hierarchy in CLIP space. This mapping is learned by aligning the encoder’s outputs with corresponding intermediate features from a frozen CLIP vision encoder using a cascaded MSE loss (LMSE (Eq. 1)). To ensure high-level semantic coherence, the terminal fMRI feature is further aligned within CLIP’s shared embedding space via a SoftCLIP loss ( ${ \mathcal { L } } _ { \mathrm { S o f t C L I P } }$ (Eq. 2)). (b) Stage 2: Scale-Aware Coarse-to-Fine Neural Guidance. A scale-wise autoregressiv...

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_AT7hCh6HB7/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of fMRI-to-image reconstruction pipelines. (a) Prior diffusion-based methods utilize a fixed neural feature to guide the reconstruction. (b) In contrast, MindHier employs scaleaware guidance, leveraging hierarchical neural features to first establish a low-resolution overview (“Forest”) before progressively refining local details (“Trees”) at higher resolutions*

MindHier 提出了一种从 fMRI 信号到自然图像的“层次到层次”重建范式，其核心 pipeline 由三个紧密耦合的模块构成：**层次化 fMRI 编码器（Hierarchical fMRI Encoder, HFE）**、**层次到层次对齐（Hierarchy-to-Hierarchy Alignment）** 和 **尺度感知的粗到细神经引导（Scale-Aware Coarse-to-Fine Neural Guidance）**。整个训练流程分为两个阶段，如图 2 所示。

**阶段一：层次到层次对齐。** HFE 由 $M$ 个级联的 Transformer 块组成，以 fMRI 信号为输入，依次输出层次化特征序列 $\{\mathbf{e}_1, \mathbf{e}_2, \ldots, \mathbf{e}_M\}$，其中浅层块捕获局部细节信息，深层块编码全局语义信息。为赋予这些特征以视觉可解释性，MindHier 将 HFE 各层输出与 CLIP 视觉编码器（ViT-L/14）的对应层特征进行对齐。对齐通过双重目标实现：

- **结构对齐**：采用级联 MSE 损失 $\mathcal{L}_{\mathrm{MSE}} = \sum_{m=1}^{M} \| \ell_{2}(\mathbf{e}_{m}) - \ell_{2}(\mathbf{v}_{g_{m}}) \|_{2}^{2}$，将 HFE 第 $m$ 块输出与 CLIP 视觉编码器第 $g_m$ 层特征在 L2 归一化后最小化距离（§3.2, Eq. 1）。
- **语义对齐**：采用 SoftCLIP 损失，将 HFE 的终端特征 $\mathbf{e}_M$ 与对应图像的视觉嵌入及文本嵌入进行对比学习，温度参数 $\tau = 0.005$（§3.2, Eq. 2）。

这一阶段的核心作用是将 fMRI 信号解耦为与 CLIP 层级对应的多尺度神经嵌入，使浅层特征承载纹理、边缘等低层视觉信息，深层特征承载类别、场景等高层语义信息，为后续生成提供层次化引导基础。

**阶段二：尺度感知的粗到细神经引导。** 生成模型采用尺度自回归模型（VAR），基于“下一尺度预测”范式，将图像生成分解为 $K$ 个尺度从低分辨率到高分辨率的逐步预测过程。连续特征经 VQ 量化后得到离散 token 图 $r_k$，其似然分解为 $p(R|E) = \prod_{k=1}^{K} p(r_k | r_{<k}, \mathbf{s}_k)$（§3.3, Eq. 5）。

关键创新在于条件信号 $\mathbf{s}_k$ 的设计：对于尺度 $k$，MindHier 从 HFE 的层次化特征中选择对应层特征 $\mathbf{s}_k = \mathbf{e}_{h_k}$ 作为引导，其中 $h_k = M - \lfloor M(k-1)/K \rfloor$。这意味着粗尺度（低分辨率）生成阶段接收来自 HFE 深层的高层语义嵌入，用于建立全局布局和语义结构（“先森林”）；细尺度（高分辨率）生成阶段接收来自 HFE 浅层的低层细节嵌入，用于逐步丰富纹理和局部细节（“后树木”）。该尺度感知的引导通过选择性注意力掩码实现（Fig. 2(b)），确保每个生成阶段仅关注与其分辨率相匹配的神经特征。

最终，各尺度生成的 token 图经 VQ 解码器码本 $Z$ 查找后求和得到连续特征图 $\hat{f} = \sum_{k=1}^{K} \text{lookup}(Z, \hat{r}_k)$，再由解码器 $D$ 生成最终图像 $\hat{I}$。

**输入输出流总结：** 输入为单次 fMRI 响应信号，经 HFE 单次前向传播产生 $M$ 层层次化特征；这些特征在阶段一与 CLIP 视觉编码器对齐后，在阶段二按尺度感知策略注入 VAR 生成器，最终输出 $512 \times 512$ 的重建图像。整个推理仅需 2.64 秒（Table 1），相比扩散式 SOTA 方法 MindEye2 加速约 4.67 倍。

MindHier 的核心架构由三个紧密耦合的模块构成，分别解决 fMRI 信号的层次化解码、跨模态特征对齐以及尺度感知的条件生成。以下逐一展开其设计逻辑与关键公式。

### 层次化 fMRI 编码器 (HFE)

传统扩散方法将 fMRI 信号映射为单一的 CLIP 空间向量，丢弃了脑信号中从局部细节到全局语义的层次信息。HFE 的设计直指这一瓶颈：它由 $M$ 个级联的 Transformer 块堆叠而成，每个块的输出 $\mathbf{e}_1, \dots, \mathbf{e}_M$ 不仅是中间步骤，其本身就是层次化表征——浅层块捕获局部纹理和边缘信息，深层块聚合为全局语义概念（§3.1, Fig. 2(a)）。这种“解耦而非压缩”的策略，为后续的尺度感知引导提供了信息基础。

### 层次到层次对齐

仅有层次化输出不足以使 fMRI 特征与视觉表征对齐，还需要建立层级间的对应关系。该模块通过双重损失函数，将 HFE 各层的输出与 CLIP 视觉编码器（ViT-L/14）的指定层特征进行对齐（§3.2, Fig. 2(a)）。

**结构对齐损失（Cascaded MSE Loss）：**

$$\mathcal{L}_{\mathrm{MSE}} = \sum_{m=1}^{M} \| \ell_{2}(\mathbf{e}_{m}) - \ell_{2}(\mathbf{v}_{g_{m}}) \|_{2}^{2}$$

其中 $\mathbf{e}_m$ 为 HFE 第 $m$ 个 Transformer 块的输出，$\mathbf{v}_{g_m}$ 为 CLIP 视觉编码器第 $g_m$ 层的特征图，$\ell_2(\cdot)$ 表示 L2 归一化。该损失逐层强制 fMRI 嵌入与视觉特征在结构上对齐，确保浅层 fMRI 特征对应 CLIP 的低层视觉特征（纹理、边缘），深层对应高层语义特征（类别、场景）。

**语义对齐损失（SoftCLIP Loss）：**

$$\mathcal{L}_{\mathrm{SoftCLIP}} = -\frac{1}{B} \sum_{i=1}^{B} \left( \log \frac{\exp(\mathbf{e}_{i} \cdot \mathbf{v}_{i} / \tau)}{\sum_{j} \exp(\mathbf{e}_{i} \cdot \mathbf{v}_{j} / \tau)} + \log \frac{\exp(\mathbf{e}_{i} \cdot \mathbf{t}_{i} / \tau)}{\sum_{j} \exp(\mathbf{e}_{i} \cdot \mathbf{t}_{j} / \tau)} \right)$$

该损失将 HFE 的终端输出 $\mathbf{e}_M$（最抽象的语义表征）同时与视觉嵌入 $\mathbf{v}$ 和文本嵌入 $\mathbf{t}$ 进行对比对齐，温度参数 $\tau = 0.005$。双重监督（视觉+文本）使 fMRI 嵌入在 CLIP 联合空间中占据更稳健的语义位置，缓解了单一模态对齐的歧义性。

总训练目标为上述损失的加权和，通过层次化对应关系实现从 CLIP 到 fMRI 编码器的有原则信息流动。

### 尺度感知的粗到细神经引导

生成阶段采用尺度自回归模型（VAR），其“下一尺度预测”范式天然提供了离散的控制点，使得层次化 fMRI 特征可按尺度注入（§3.3, Fig. 2(b)）。

**量化与自回归分解：** 连续特征图 $\mathbf{f}_k$ 首先被量化为离散 token 图 $\mathbf{r}_k$：

$$r_{k}^{(i,j)} = \mathop{\mathrm{argmin}}_{n \in \{1,\dots,N\}} \| f_{k}^{(i,j)} - \mathrm{lookup}(Z,n) \|_{2}$$

其中 $N=4096$ 为码本大小。随后，多尺度 token 图的联合似然按尺度自回归分解：

$$p(r_1, \dots, r_K) = \prod_{k=1}^{K} p(r_k \mid r_1, \dots, r_{k-1})$$

**条件注入：** 引入层次化 fMRI 条件 $E = \{\mathbf{e}_1, \dots, \mathbf{e}_M\}$ 后，条件似然变为：

$$p(R|E) = \prod_{k=1}^{K} p(r_k \mid r_{<k}, \mathbf{s}_k)$$

其中 $\mathbf{s}_k$ 为尺度特定的引导特征，通过索引映射 $h_k = M - \lfloor M(k-1)/K \rfloor$（$M \leq K$）从层次化特征中选取。粗尺度（$k$ 小）使用深层语义特征（$\mathbf{s}_k$ 对应大 $h_k$），细尺度（$k$ 大）使用浅层细节特征（$\mathbf{s}_k$ 对应小 $h_k$），实现“先森林后树木”的生成顺序。该策略通过选择性注意力掩码实现，确保各尺度仅关注其对应的 fMRI 特征（Fig. 2(b)）。

最终图像通过将各尺度的量化向量求和后送入解码器 $\mathcal{D}$ 获得：$\hat{I} = \mathcal{D}\left(\sum_{k=1}^{K} \mathrm{lookup}(Z, \hat{r}_k)\right)$。

---

**关键公式汇总：** 上述五个公式构成了 MindHier 的理论骨架——Eq. (1) 和 Eq. (2) 定义了对齐训练的目标，Eq. (3)–(5) 定义了尺度感知的条件生成过程。消融实验证实，层次化全监督（Eq. 1 + Eq. 2 作用于所有块）相比仅监督终端层，CLIP 准确率从 95.1% 跃升至 97.2%（Table 2）；粗到细引导策略（Eq. 5 中 $\mathbf{s}_k$ 按 $h_k$ 递减选取）相比倒置的细到粗策略，CLIP 提升 1.1 个百分点，SwAV 距离降低 0.009（Table 4），验证了公式设计的有效性。

## 实验与关键发现

### 主实验：NSD测试集性能对比

MindHier在NSD新测试集（1,000张共享测试图像）上与现有fMRI-to-image方法进行了全面对比，结果见 **Table 1**。MindHier在不使用任何辅助低层特征（†标记）的前提下，取得了最高的高层语义指标：CLIP双向识别准确率达到96.4%，SwAV距离降至0.329，InceptionV3准确率95.9%。相比之下，基于扩散的SOTA方法MindEye2（Scotti et al., ICML 2024）的CLIP为93.0%，SwAV为0.344。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_AT7hCh6HB7/figures/003_Table_1.jpg]]
*Table 1: Quantitative performance comparison on the new NSD test set (Allen et al., 2022). The best and second best results are highlighted in bold and underlined respectively. The Wall-clock inference time for one image is reported. †: an auxiliary low-level feature is used*

在低层结构指标上，MindHier的SSIM达到0.461±0.0023，在无辅助特征的方法中同样最优。值得注意的是，MindHier的推理时间仅为2.64秒/图，比MindEye2的12.14秒快约4.67倍。这一效率优势源于两个设计：层次化fMRI编码器在单次前向传播中生成全部神经特征；尺度自回归模型将主要计算量集中在低分辨率阶段，高分辨率阶段的token数相对较少。

在跨数据集泛化方面，**Table S9**显示MindHier在THINGS-fMRI测试集上取得CLIP 73.1%，相比BrainFlora的57.6%提升了15.5个百分点，验证了层次化引导策略在不同fMRI数据集上的迁移能力。

### 消融实验

#### 层次化特征编码器设计

**Table 2**对比了三种fMRI编码器设计对Subject 1数据的影响。单层特征（Single Feature）仅使用最终输出作为固定引导，CLIP为95.1%，Alex(5)为96.6%。引入层次化特征但仅对终端层监督（Hierarchical Feature + final supervision）时，CLIP提升至96.0%，Alex(5)提升至98.0%。当采用完整的级联监督（Hierarchical Feature + full cascaded supervision，即对每个Transformer块均施加MSE+SoftCLIP损失）时，性能全面跃升：CLIP达到97.2%，Alex(5)达到99.3%。这一消融直接证明了层次化全监督是性能提升的关键——仅有多层结构而不逐层对齐是不够的，必须让每个中间层都显式学习对应尺度的视觉特征。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_AT7hCh6HB7/figures/007_Table_2.jpg]]
*Table 2: Comparison of different fMRI encoder designs using fMRI data from Subject 1*

#### CLIP层映射策略

**Table 3**探索了fMRI编码器各层输出与CLIP ViT-L/14视觉编码器层的映射关系。三种映射策略分别为：晚期映射 $g_m = 16 + 2m$（对应层{18,20,22,24}）、早期映射 $g_m = 6m$（对应层{6,12,18,24}）和平衡映射 $g_m = 8 + 4m$（对应层{12,16,20,24}）。平衡映射在高层语义（CLIP 97.2%）和低层相似性（Alex(5) 99.3%）之间取得了最佳折中。晚期映射偏向高层语义导致低层细节丢失，早期映射则因过早引入细粒度特征而干扰了全局语义的建立。这表明fMRI编码器的层次结构需要与CLIP的层次结构保持适当的对应节奏——既不能太浅也不能太深。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_AT7hCh6HB7/figures/008_Table_3.jpg]]
*Table 3: Comparison of different CLIP layer mapping mechanisms using fMRI data from Subject 1*

#### 尺度感知引导策略

**Table 4**直接验证了“先森林后树木”信息流顺序的必要性。MindHier的粗到细（Coarse-to-Fine）策略将高层语义注入低分辨率生成阶段，细节特征注入高分辨率阶段。与之对比的倒置策略（Fine-to-Coarse）将细节特征先注入低分辨率阶段。结果显示，粗到细策略在CLIP上领先1.1个百分点（97.2% vs 96.1%），SwAV距离降低0.009（0.321 vs 0.330）。这一差异的因果机制在于：低分辨率阶段（如8×8 token map）的生成能力有限，若此时注入细节特征，模型无法有效利用这些信息，反而会干扰全局布局的建立；而正确的粗到细流让模型先确定场景语义和布局，再逐步填充纹理细节，符合人类视觉感知的层级特性。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_AT7hCh6HB7/figures/009_Table_4.jpg]]
*Table 4: Ablation study on the scale-aware neural guidance. The proposed coarse-to-fine strategy is compared against an inverted variant on Subject 1*

#### 单样本生成稳定性

**Table S5**显示MindHier在单次采样（N=1）时即可达到CLIP 95.0%，推理仅需0.92秒。这与扩散模型需要多次采样（通常N=16或更多）才能稳定输出的特性形成鲜明对比。尺度自回归模型的确定性生成机制避免了扩散模型中的随机采样方差，使得单次生成即可获得高质量结果，进一步放大了推理效率优势。

### 失败模式与局限性

尽管MindHier在高层语义指标上表现优异，但在以下场景存在系统性失败：

1. **文字与标识重建**：无法重建可读的文字和特定标识（如商标、路牌），这些元素被生成为通用纹理。这与CLIP空间中对文字语义编码能力有限相关。
2. **面部特征模糊**：人脸重建缺乏身份识别所需的精度，面部特征趋于平均化。这是fMRI信号空间分辨率限制与生成模型对精细人脸结构建模不足的共同结果。
3. **精细计数与材质失准**：对物体数量的判断容易出错，高密度纹理信息（如建筑外立面材质）在重建中丢失。这反映了层次化特征在极细粒度信息上的表达瓶颈。
4. **跨受试者泛化**：**Table S3**显示，当仅使用1小时新受试者数据进行微调时，性能大幅下降，表明模型对新受试者的适应仍需要大量标注fMRI数据，少样本泛化能力有限。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_AT7hCh6HB7/figures/010_Table_5.jpg]]
*Table 5: Table S1: Quantitative results of each subject*

## 定位与知识库关联

### 从扩散到自回归：范式转换的动因

fMRI-to-image重建领域长期由扩散模型主导，其核心范式是将fMRI信号映射为单一的CLIP空间嵌入，作为固定条件注入扩散过程。代表性工作包括**MindEye1**（Scotti et al., NeurIPS 2023）、**MindEye2**（Scotti et al., ICML 2024）和**BrainDiffuser**（Sci. Rep. 2023）。这一范式的根本瓶颈在于：**单一的、静态的神经嵌入无法利用fMRI信号的层次信息**——大脑视觉通路本身是层级化组织的，从初级视觉皮层提取局部边缘和纹理，到高级视觉区域编码语义类别和场景概念。用固定嵌入引导整个生成过程，相当于用同一把钥匙开所有门，与图像重建“先森林后树木”的阶段性需求形成结构性错配。

MindHier的方法学贡献在于将这一范式从“固定引导+扩散”切换为“层次引导+尺度自回归”。具体而言，它用**层次化fMRI编码器（HFE）**替代了单一嵌入映射，用**尺度自回归模型（VAR）**替代了扩散模型，并通过**层次到层次对齐**和**粗到细神经引导**两个机制将二者耦合。这一转换并非简单的生成器替换——它触及了问题的因果关节：将fMRI信号的层级结构显式地暴露给生成过程，使全局语义注入低分辨率阶段，细节特征注入高分辨率阶段，从而对齐了人类感知“先把握整体再分辨细节”的认知逻辑。

### 与基线方法的关键差异

**神经引导方式**是最根本的差异点。扩散方法（MindEye2等）使用固定的CLIP嵌入全程引导去噪过程，而MindHier根据生成尺度动态选择引导特征：粗尺度（低分辨率）接收高层语义嵌入（对应CLIP ViT-L/14的第24层），细尺度（高分辨率）接收低层细节嵌入（对应第12层）。这一设计由尺度-特征映射函数 $h_k = M - \lfloor M(k-1)/K \rfloor$ 显式定义，并在Transformer的交叉注意力中通过选择性掩码实现。

**训练对齐策略**的差异同样关键。扩散方法通常仅对齐终端特征与CLIP嵌入，而MindHier的层次到层次对齐引入了双重监督：级联MSE损失（$\mathcal{L}_{\mathrm{MSE}} = \sum_{m=1}^{M} \| \ell_{2}(\mathbf{e}_{m}) - \ell_{2}(\mathbf{v}_{g_{m}}) \|_{2}^{2}$）强制HFE各层输出与CLIP视觉编码器对应层特征的结构对齐；SoftCLIP损失则将终端fMRI嵌入与视觉和文本嵌入进行对比对齐。这种“结构+语义”的双重约束使得fMRI特征的层级结构在训练中得以保留。

**推理效率**是范式转换的直接红利。扩散模型需要多步迭代去噪（MindEye2约12.14秒/图），而尺度自回归模型将大部分计算集中在低分辨率阶段，单次前向传播即可生成完整图像（2.64秒/图），加速约4.67倍。单样本生成（N=1）即可获得CLIP 95.0%的强确定性结果（Table S5），无需多次采样，进一步凸显了自回归范式在效率上的优势。

### 适用边界与局限

**无法重建可读文字和特定标识**。商标、路牌、文字等符号化信息被生成为通用纹理，这源于CLIP视觉编码器本身对细粒度符号表征的固有限制——层次化对齐无法弥补预训练视觉骨干的语义盲区。

**面部特征模糊，身份无法准确恢复**。尽管粗到细策略在全局语义上表现优异（CLIP 96.4%），但人脸的身份识别精度仍然不足。这暗示高层语义引导（如“这是一张人脸”）与低层细节引导（如“这张脸的具体特征”）之间的信息梯度可能不够陡峭，或者CLIP的层级特征本身缺乏身份判别所需的细粒度信息。

**精细计数和材料属性容易出错**。高密度纹理（如建筑外立面材质）在重建中丢失，物体数量统计不可靠。这一问题与尺度自回归模型的离散token化机制有关——VQ量化（N=4096）可能在高分辨率尺度上引入信息瓶颈，导致纹理细节被平滑为统计模式。

**跨数据集泛化有限**。在THINGS-fMRI测试集上，尽管高层语义指标大幅领先（CLIP 73.1% vs BrainFlora 57.6%），低层指标仍较低（PixCorr 0.109），表明模型对不同fMRI采集协议和数据分布的适应能力不足。

**跨受试者少样本泛化脆弱**。仅使用1小时新受试者数据进行微调时性能大幅下降（Table S3），说明层次化fMRI编码器对个体脑区功能拓扑的差异敏感，需要大量标注数据才能完成受试者间的迁移。

### 开放问题

1. **纹理逼真度与面部保真度的提升路径**：能否在不显著增加计算开销的前提下，引入显式的纹理重建模块或身份感知损失？尺度自回归的离散token化是否可以在高分辨率尺度上增加码本容量以缓解信息瓶颈？

2. **计数与材质的显式建模**：是否可以通过引入显式计数模块或材质感知损失来缓解对物体数量和材质的系统性失准？这可能需要突破CLIP视觉特征的信息上限，引入额外的视觉监督信号。

3. **层次化引导策略的跨模态扩展**：该策略的核心思想——将条件信号的层级结构与生成过程的尺度结构对齐——是否可推广至文本到图像生成、视频预测或其他脑区信号（如EEG、MEG）的重建任务？

4. **更高分辨率的计算挑战**：尺度自回归模型在>512×512分辨率下的伪影控制和计算负载如何解决？随着尺度数K增加，token序列长度呈指数增长，选择性注意力掩码的效率优势可能被稀释。

5. **跨受试者少样本泛化机制**：如何设计受试者无关的fMRI表征学习策略，以降低对新受试者的数据依赖？这可能需要在HFE中引入脑区对齐模块或元学习框架。

## 原文 PDF

![[paperPDFs/ICLR_2026/Moving_Beyond_Diffusion_Hierarchy_to_Hierarchy_Autoregression_for_fMRI_to_Image_Reconstruction.pdf]]
