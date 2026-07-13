---
title: "Multinex: Lightweight Low-light Image Enhancement via Multi-prior Retinex"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Multinex_Lightweight_Low_light_Image_Enhancement_via_Multi_prior_Retinex.pdf
project_link: "https://albrateanu.github.io/multinex"
code_link: null
aliases:
- Multinex
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入由Retinex理论指导的加性增强增量（enhancement delta）公式，并利用解析导出的多视角亮度先验栈（illumination guidance stack）与反射率先验栈（reflectance guidance stack）作为网络输入，实现亮度与颜色的解耦学习与校正。
primary_logic: 增强的核心不应是重建整张图像，而是添加一个结构化的校正场。通过将Retinex分解视为结构先验而非重建目标，并结合互补的亮度与色度解析先验，轻量级神经网络即可有效学习曝光与色彩的调整。
claims:
- 在LOLv1数据集上，Multinex（45K参数）以23.19dB PSNR超越同参数量级轻量模型LYT-Net（22.38dB），且参数更少。
- 在无参考数据集MEF/LIME/DICM/NPE上，Multinex取得了最低的NIQE均值3.64，优于所有对比方法。
- 消融实验证实，同时使用亮度与反射率双先验（vs. 仅用一种或仅用RGB）在LOL-v1上显著提升PSNR至23.19dB。
- 在低光照目标检测任务ExDark上，Multinex-Nano仅凭0.7K参数取得了最高的mAP50（84.6%）。
---

# Multinex: Lightweight Low-light Image Enhancement via Multi-prior Retinex

> [!tip] 核心洞察
> 增强的核心不应是重建整张图像，而是添加一个结构化的校正场。通过将Retinex分解视为结构先验而非重建目标，并结合互补的亮度与色度解析先验，轻量级神经网络即可有效学习曝光与色彩的调整。

| 字段 | 内容 |
|------|------|
| 中文题名 | Multinex：基于多先验Retinex的轻量级低光照图像增强 |
| 英文题名 | Multinex: Lightweight Low-light Image Enhancement via Multi-prior Retinex |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.10359) · [Project](https://albrateanu.github.io/multinex) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Multinex |
| Dataset | LOLv1, LOLv2-real, LOLv2-syn, Model Size |

> [!tip] 效果简介
> - LOLv1 上，PSNR ↑ 23.19 vs 22.38 (LYT-Net) (+0.81 dB)。
> - LOLv2-real 上，PSNR ↑ 23.04 vs 21.83 (LYT-Net) (+1.21 dB)。
> - LOLv2-syn 上，PSNR ↑ 25.04 vs 23.78 (LYT-Net) (+1.26 dB)。

## 概要

低光照图像增强（LLIE）面临一个根本性瓶颈：在常用的RGB或YUV等色彩空间中，亮度（illumination）与颜色（chrominance）信息高度耦合，导致曝光修正与色调恢复相互干扰，限制了增强质量与模型效率。现有方法或直接以Retinex分解为目标重建整张图像，或将增强建模为曲线映射，均未充分解耦这两个相互冲突的子任务。

**Multinex** 提出了一种范式转换：**增强的核心不应是重建整张图像，而是添加一个结构化的校正场**。该方法将Retinex分解视为结构先验而非重建目标，引入**加性增强增量（enhancement delta）公式** $\hat{\mathbf{I}} = \mathbf{I} + \pmb{\Delta}_L \odot \pmb{\Delta}_R$，将增强分解为亮度校正 $\pmb{\Delta}_L$ 与反射率校正 $\pmb{\Delta}_R$ 的逐元素乘积。在此基础上，Multinex利用解析导出的**多视角亮度先验栈**（4个互补亮度特征图）与**反射率先验栈**（5个色度/色调特征图）作为网络输入，通过双分支轻量融合网络实现亮度与颜色的解耦学习。

**核心结论**：Multinex以仅**45K参数**（0.0446M）的极致轻量规模，在LOLv1数据集上达到**23.19dB PSNR**，超越同参数量级最强基线LYT-Net（22.38dB），同时在无参考数据集（MEF/LIME/DICM/NPE）上取得最低NIQE均值**3.64**，并在低光照目标检测任务ExDark上以0.7K参数的Nano变体获得最高**mAP50 84.6%**。消融实验证实，同时使用亮度与反射率双先验是性能的关键支撑，而加性增量公式显著优于直接RGB输入或单一先验方案。

**方法定位**：Multinex属于**解析先验驱动的轻量级Retinex增强**路线，区别于以重建为目标的经典Retinex方法（如RetinexNet）和基于曲线映射的轻量方法（如ZeroDCE）。其核心贡献在于将经典色彩理论与Retinex结构先验注入网络输入层，使极简网络即可学习有效的曝光与色彩调整，而非依赖复杂的网络架构设计。

低光照图像增强（Low-Light Image Enhancement, LLIE）是计算机视觉中的基础任务，其目标是在恢复曝光不足区域的可见性的同时，保持色彩的自然性与结构的完整性。该任务在自动驾驶、夜间监控、移动摄影等场景中具有广泛的应用需求。然而，现有方法在**亮度与颜色的解耦**这一核心瓶颈上仍面临显著挑战。

### 亮度-颜色耦合：LLIE的根本瓶颈

在常见的色彩空间（如RGB、YUV）中，亮度（illumination）与色度（chrominance）信息天然耦合。这一耦合导致增强过程中的两个核心矛盾：

1. **曝光修正与色调恢复相互干扰**：提升暗区亮度时，容易引入色彩偏移或饱和度失真；而试图校正颜色时，又可能破坏亮度的自然过渡。
2. **模型效率与增强质量的权衡**：大型模型（如**GLARE**，59.48M参数）可通过复杂网络隐式学习解耦，但计算代价高昂；轻量级方法（如**LYT-Net**，45K参数）因表示能力有限，难以在紧凑架构内同时处理好亮度与色彩两个维度。

### 现有方法的范式局限

当前LLIE方法的主流范式可归纳为两类，均未从根本上解决亮度-颜色耦合问题：

- **基于Retinex分解的重建范式**：如**RetinexNet**、**PairLIE**（330K参数）、**RetinexFormer**（1.53M参数）等方法，遵循 $I = L \odot R$ 的分解公式，以**重建整张图像**为目标。这类方法将增强任务转化为光照图（L）与反射图（R）的估计问题，但分解过程本身是欠定的，且网络需要同时学习分解与重建，增加了优化难度。
- **端到端映射范式**：如**ZeroDCE**（79K参数）通过曲线映射直接预测增强图像，**CIDNet**（1.88M参数）在可学习色彩空间中操作，**LYT-Net**在YUV空间中利用Transformer进行增强。这些方法绕过了显式分解，但缺乏对亮度与颜色各自物理特性的结构化先验引导，导致校正过程缺乏可解释性。

上述方法的共同缺陷在于：**增强的核心被错误地定位为“重建”，而非“校正”**。重建整张图像要求网络学习完整的图像分布，这对轻量级模型而言负担过重；而实际需求是学习一个结构化的**校正场**，仅对输入图像中曝光不足和色彩失真的区域进行调整。

### 本文动机：从重建到校正的范式转换

Multinex的核心动机源于以下洞察：**Retinex理论不应作为重建目标，而应作为结构先验**。具体而言：

- 将Retinex分解视为一种**引导信号**而非输出目标，利用其提供的亮度与反射率分离特性，构造多视角的解析先验栈（guidance stack）。
- 将增强范式从“重建整张图像”转变为“添加一个结构化的增强增量（enhancement delta）”，使网络仅需学习**需要校正的部分**，大幅降低学习负担。
- 通过**亮度先验栈**（4个互补的亮度特征图）与**反射率先验栈**（5个光照无关的色度特征图）的显式构造，在输入端实现亮度与颜色的解耦，使后续的双分支轻量网络可以各自独立地学习曝光校正与色彩校正。

这一范式转换使得在**仅45K参数**的极端轻量级架构下，实现超越同参数量级方法（如LYT-Net）的增强质量成为可能，同时保持了出色的泛化能力与下游任务兼容性。

## 核心方法与创新机理

Multinex 的核心创新并非提出更深的网络或更复杂的注意力机制，而是从**低光照增强的范式层面**重新定义了问题与输入表示，使得极轻量网络也能实现亮度与颜色的解耦校正。

### 从重建到校正：加性增强增量范式

传统 Retinex 方法将增强视为图像分解与重建问题，即从输入图像 $I$ 估计光照图 $L$ 和反射图 $R$，再通过 $I = L \odot R$ 重建增强结果。这一范式的根本缺陷在于：**亮度与颜色在分解过程中高度耦合**，任何一方的估计误差都会通过乘积传播到最终输出，导致曝光修正与色调恢复相互干扰。

Multinex 的破局思路是将 Retinex 分解从“重建目标”降级为“结构先验”，转而学习一个**加性增强增量（Enhancement Delta）**：

$$\hat{\mathbf{I}} = \mathbf{I} + \pmb{\Delta}_L \odot \pmb{\Delta}_R$$

其中 $\pmb{\Delta}_L$ 是单通道亮度校正场，$\pmb{\Delta}_R$ 是三通道反射率校正场。这一公式的因果机制在于：网络不再需要“凭空”重建整张图像，而只需预测一个结构化的校正残差。亮度与颜色的调整通过乘积显式分解为两个独立分量，从数学形式上实现了**亮度-颜色解耦**——这是后续所有设计选择得以生效的前提。

### 从单一色彩空间到多视角解析先验栈

现有轻量级方法通常将原始 RGB 或单一色彩空间（如 YUV、HVI）作为网络输入，但单一色彩空间的表示能力有限，难以同时提供充分的曝光线索与色调信息。Multinex 的第二个关键创新是**用解析导出的多视角先验栈替代原始图像作为网络输入**，将亮度与颜色的解耦从公式层面延伸到特征层面。

**亮度引导栈** $\mathcal{S}_{\mathcal{L}}(\mathbf{I})$ 包含 4 个互补的亮度特征图：

$$\mathcal{S}_{\mathcal{L}}(\mathbf{I}) = [\mathbf{Y}_{\mathrm{Rec.709}}, \mathbf{Y}_{\mathrm{vmax}}, \mathbf{Y}_{\mathrm{lightness}}, \mathbf{Y}_{\mathrm{L_2}}]$$

这四种亮度定义分别从标准光度、通道最大值、感知明度和欧氏范数角度刻画场景的曝光与对比度结构，形成对光照条件的多视角观测。

**反射率引导栈** $\mathcal{S}_{\mathcal{R}}(\mathbf{I})$ 包含 5 个光照无关的色度特征图：

$$S_{\mathcal{R}}(\mathbf{I}) = [\mathbf{C}_b, \mathbf{C}_r, \mathbf{r}, \mathbf{g}, \mathbf{S}]$$

其中 $\mathbf{C}_b, \mathbf{C}_r$ 为蓝、红色差分量，$\mathbf{r}, \mathbf{g}$ 为红、绿通道的归一化比例，$\mathbf{S}$ 为饱和度。这些特征图的设计目标是**剥离亮度信息，仅保留光照无关的色彩结构**，使反射率网络 $f_{\mathcal{R}}$ 能够专注于色调校正而不受曝光变化的干扰。

消融实验为这一设计提供了决定性证据：在 LOLv1 上，仅使用亮度先验或仅使用反射率先验时 PSNR 最高为 22.74dB，而**同时使用双先验栈将 PSNR 提升至 23.19dB**（Table 4a）。此外，完整的亮度栈（4 图）优于任意部分组合（Table 7），完整的反射率栈（5 图）同样优于任意子集（Table 8），证实了多视角互补信息的必要性。

### 双分支轻量融合网络与分量注意力

Multinex 使用两个结构相同但参数独立的轻量融合网络 $f_{\mathcal{L}}$ 和 $f_{\mathcal{R}}$ 分别处理亮度栈与反射率栈：

$$f(\mathcal{S}) = \mathrm{Conv}_{1 \times 1} \circ \mathrm{FB}^T \left( \mathrm{CWA}(\mathcal{S}) \odot \bar{\mathcal{S}} \right)$$

其核心构建块包括：

- **融合块（Fusion Block, FB）**：通过 MSEF → 深度可分离卷积 → ReLU → MSEF 的级联实现高效特征细化，保持极低参数量。
- **分量注意力（Component-wise Attention, CWA）**：为引导栈的各个分量产生独立的软注意力掩码，选择性加权不同先验的贡献。消融实验表明，将 CWA 放置在投影层与 FB 之间（“Between”位置）可获得最佳 PSNR 23.19dB，优于提前或延后放置（Table 9）。

综上，Multinex 的创新链条可概括为：**范式转换（加性增量）→ 表示重构（多视角先验栈）→ 结构适配（双分支融合网络）**。这三个 changed slots 层层递进，共同实现了在仅 45K 参数下超越同量级最强基线 LYT-Net 的性能（LOLv1: 23.19dB vs. 22.38dB，Table 1），并验证了“增强的核心是添加结构化校正场，而非重建整张图像”这一核心洞察。

Multinex 的整体流程围绕一个核心洞察展开：低光照增强不应以重建整张图像为目标，而应学习一个结构化的**加性增强增量（enhancement delta）**。这一增量由 Retinex 理论指导，通过亮度校正与颜色校正的解耦组合，实现轻量而高效的曝光与色调调整。

### 增强增量的分解

给定低光照输入图像 $\mathbf{I} \in \mathbb{R}^{H \times W \times 3}$，增强图像 $\hat{\mathbf{I}}$ 的生成公式为：

$$\hat{\mathbf{I}} = \mathbf{I} + \pmb{\Delta}_L \odot \pmb{\Delta}_R$$

其中，$\pmb{\Delta}_L \in \mathbb{R}^{H \times W \times 1}$ 是单通道亮度校正场，$\pmb{\Delta}_R \in \mathbb{R}^{H \times W \times 3}$ 是三通道反射率（颜色）校正场。两者逐元素相乘后，以加性残差的形式叠加到原始输入上（见 Eq. 1）。

这一设计的关键在于：它将传统 Retinex 分解 $I = L \odot R$ 从“重建目标”转化为“结构先验”——网络不再需要预测完整的光照图和反射图，而只需估计两个校正场，从而显著降低了学习难度。

### 多视角先验栈与双分支网络

为了进一步解耦亮度与颜色的学习，Multinex 不从原始 RGB 直接预测校正场，而是分别为两个网络分支构建**解析先验栈（guidance stacks）**：

- **亮度引导栈** $\mathcal{S}_{\mathcal{L}}(\mathbf{I})$：由 4 个互补的亮度特征图拼接而成，包括 Rec.709 亮度、最大值亮度、感知亮度和 L2 范数亮度（Eq. 4）。这些图从不同角度刻画场景的曝光与对比度结构。
- **反射率引导栈** $\mathcal{S}_{\mathcal{R}}(\mathbf{I})$：由 5 个色度/色调特征图拼接而成，包括蓝、红色差分量 $\mathbf{C}_b, \mathbf{C}_r$，红、绿归一化比例 $\mathbf{r}, \mathbf{g}$，以及饱和度 $\mathbf{S}$（Eq. 9）。这些图捕获了光照无关的色彩结构。

基于上述先验栈，Multinex 采用**双分支轻量融合网络**（Fig. 2）：

![[assets/figures/papers/paper_list_l901_https_arxiv_org_abs_2604_10359/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of Multinex Architecture. Fusion modules*

- **亮度网络** $f_{\mathcal{L}}$：以 $\mathcal{S}_{\mathcal{L}}(\mathbf{I})$ 为输入，输出单通道亮度校正 $\pmb{\Delta}_L$。
- **反射率网络** $f_{\mathcal{R}}$：以 $\mathcal{S}_{\mathcal{R}}(\mathbf{I})$ 为输入，输出三通道反射率校正 $\pmb{\Delta}_R$。

两个网络采用**相同的架构但独立的权重**，确保亮度与颜色的学习过程完全解耦，同时保持模型结构的简洁性。

### 融合模块的内部结构

每个分支网络的核心是**融合模块（Fusion Module）**，其内部由以下组件级联构成（Eq. 18）：

1. **分量注意力（Component-wise Attention, CWA）**：对输入先验栈的各分量产生独立软注意力掩码，选择性加权不同先验特征（Eq. 16）。
2. **融合块（Fusion Block, FB）**：通过 MSEF（多尺度增强融合）操作、深度可分离卷积（DSConv）和 ReLU 激活的组合，逐层细化特征表达（Eq. 15）。多个 FB 串行堆叠（共 $T$ 个）。
3. **最终投影**：经 $1 \times 1$ 卷积将融合后的特征映射到目标输出通道数（亮度网络为 1，反射率网络为 3）。

### 端到端流程

完整的前向传播可概括为：

1. 对输入图像 $\mathbf{I}$ 分别计算亮度引导栈 $\mathcal{S}_{\mathcal{L}}$ 和反射率引导栈 $\mathcal{S}_{\mathcal{R}}$。
2. 将 $\mathcal{S}_{\mathcal{L}}$ 送入亮度网络 $f_{\mathcal{L}}$，生成 $\pmb{\Delta}_L$。
3. 将 $\mathcal{S}_{\mathcal{R}}$ 送入反射率网络 $f_{\mathcal{R}}$，生成 $\pmb{\Delta}_R$。
4. 通过加性增强增量公式 $\hat{\mathbf{I}} = \mathbf{I} + \pmb{\Delta}_L \odot \pmb{\Delta}_R$ 合成最终增强图像。

整个框架仅包含约 45K 可学习参数，却能在 LOLv1 上达到 23.19 dB PSNR，超越同参数量级的轻量方法 LYT-Net（22.38 dB），验证了“解析先验 + 加性校正”这一设计范式的有效性。

![[assets/figures/papers/paper_list_l901_https_arxiv_org_abs_2604_10359/figures/015_Figure_11.jpg]]
*Figure 11: MSEF module architecture*

### 3.1 增强范式：从重建到校正

Multinex的核心洞察在于**增强的本质不应是重建整张图像，而是添加一个结构化的校正场**。传统Retinex方法将增强建模为 $\\hat{\\mathbf{I}} = \\mathbf{L} \\odot \\mathbf{R}$，以乘法分解为目标重建输出图像。Multinex则提出**加性增强增量（Enhancement Delta）**公式：

$$\hat{\mathbf{I}} = \mathbf{I} + \pmb{\Delta}_L \odot \pmb{\Delta}_R$$

其中 $\\hat{\\mathbf{I}}$ 为增强后图像，$\\mathbf{I}$ 为输入低光照图像，$\\pmb{\\Delta}_L$ 为单通道亮度校正场，$\\pmb{\\Delta}_R$ 为三通道反射率（颜色）校正场。这一范式转变将Retinex分解视为**结构先验而非重建目标**，使网络只需学习曝光与色彩的调整量，显著降低了学习难度。

逐通道展开形式为：

$$\hat{\mathbf{I}}_i = \mathbf{I}_i + f_{\mathcal{L}}(\mathbf{I}, \theta_{\mathcal{L}}) \odot f_{\mathcal{R}_i}(\mathbf{I}, \theta_{\mathcal{R}})$$

其中 $i \\in \\{R, G, B\\}$，$f_{\\mathcal{L}}$ 输出共享的亮度校正，$f_{\\mathcal{R}_i}$ 输出各通道独立的色度校正。这一因式分解直接对应了Retinex理论中亮度与反射率的解耦结构。

### 3.2 多视角先验栈：亮度与颜色的解耦输入

为彻底解耦亮度与颜色信息，Multinex构建了两个互补的解析先验栈作为网络输入，替代原始RGB。

**亮度引导栈（Luminance Guidance Stack）** $\\mathcal{S}_{\\mathcal{L}}(\\mathbf{I})$ 包含4个特征图：

$$\mathcal{S}_{\mathcal{L}}(\mathbf{I}) = [\mathbf{Y}_{\mathrm{Rec.709}}, \mathbf{Y}_{\mathrm{vmax}}, \mathbf{Y}_{\mathrm{lightness}}, \mathbf{Y}_{\mathrm{L_2}}]$$

- $\\mathbf{Y}_{\\mathrm{Rec.709}}$：标准Rec.709亮度（加权RGB和）
- $\\mathbf{Y}_{\\mathrm{vmax}}$：逐像素RGB最大值
- $\\mathbf{Y}_{\\mathrm{lightness}}$：CIELAB感知亮度
- $\\mathbf{Y}_{\\mathrm{L_2}}$：RGB通道L2范数

四种亮度定义从不同角度捕获曝光与对比度线索，形成互补的亮度表征。

**反射率引导栈（Reflectance Guidance Stack）** $\\mathcal{S}_{\\mathcal{R}}(\\mathbf{I})$ 包含5个特征图：

$$S_{\mathcal{R}}(\mathbf{I}) = \\left[ \\mathbf{C}_b, \\mathbf{C}_r, \\mathbf{r}, \\mathbf{g}, \\mathbf{S} \\right]$$

- $\\mathbf{C}_b, \\mathbf{C}_r$：YCbCr空间中的蓝、红色差分量
- $\\mathbf{r}, \\mathbf{g}$：归一化红、绿比例（$r = R/(R+G+B)$，$g = G/(R+G+B)$）
- $\\mathbf{S}$：HSV空间饱和度

这些色度/色调特征图具有光照无关性，捕获了场景固有的色彩结构。

引入先验栈后的完整增强公式为：

$$\hat{\mathbf{I}}_i = \mathbf{I}_i + f_{\mathcal{L}}(S_{\mathcal{L}}(\mathbf{I}), \theta_{\mathcal{L}}) \odot f_{\mathcal{R}_i}(S_{\mathcal{R}}(\mathbf{I}), \theta_{\mathcal{R}})$$

### 3.3 双分支融合网络

亮度校正网络 $f_{\\mathcal{L}}$ 和反射率校正网络 $f_{\\mathcal{R}}$ 采用**相同架构但参数独立**，均为轻量级融合模块：

$$f(\\mathcal{S}) = \\mathrm{Conv}_{1 \\times 1} \\circ \\mathrm{FB}^T \\left( \\mathrm{CWA}(\\mathcal{S}) \\odot \\bar{\\mathcal{S}} \\right)$$

其中 $f_{\\mathcal{L}}: \\mathbb{R}^{H \\times W \\times 4} \\to \\mathbb{R}^{H \\times W \\times 1}$，$f_{\\mathcal{R}}: \\mathbb{R}^{H \\times W \\times 5} \\to \\mathbb{R}^{H \\times W \\times 3}$。$\\bar{\\mathcal{S}}$ 为输入先验栈经投影后的特征，$T$ 为融合块（FB）的串联数量。

### 3.4 融合块与分量注意力

**融合块（Fusion Block, FB）** 通过微操作序列细化特征：

$$\bar{\mathbf{X}} = \\mathrm{MSEF} \\circ \\sigma_{\\mathrm{ReLU}} \\circ \\mathrm{DSConv} \\circ \\mathrm{MSEF}(\\mathbf{X})$$

其中MSEF为多尺度特征提取操作，DSConv为深度可分离卷积，$\\sigma_{\\mathrm{ReLU}}$ 为ReLU激活。该设计在保持轻量的同时实现了有效的特征融合。

**分量注意力（Component-wise Attention, CWA）** 为各先验分量生成独立的软注意力掩码：

$$\mathbf{A} = \\sigma \\circ \\mathrm{Conv}_{1 \\times 1} \\circ \\mathrm{DWConv}(\\mathbf{X})$$

其中DWConv为深度可分离卷积，$\\mathrm{Conv}_{1 \\times 1}$ 为逐点卷积，$\\sigma$ 为Sigmoid激活。CWA使网络能够自适应地选择性加权不同先验分量，消融实验证实将CWA放置在投影层与FB之间（“Between”位置）可获得最佳PSNR 23.19（Table 9）。

## 实验与关键发现

### 核心定量结果

Multinex 在参考数据集（LOLv1、LOLv2-real、LOLv2-syn）和无参考数据集（MEF、LIME、DICM、NPE）上均展现出显著的性能与效率优势。**Table 1** 汇总了 LOL 基准上的全参考指标对比。在轻量级组（参数 < 1M）中，Multinex 仅以 **0.0446M 参数**（45K）和 2.50 GFLOPs 在 LOLv1 上取得 **23.19 dB PSNR** 和 **0.843 SSIM**，超越同参数量级最强基线 **LYT-Net**（0.0449M，22.38 dB）0.81 dB。在 LOLv2-real 和 LOLv2-syn 上，优势进一步扩大至 +1.21 dB 和 +1.26 dB。值得注意的是，Multinex 甚至超越了参数量大 40 倍的 **CIDNet**（1.88M，22.51 dB）和 **RetinexFormer**（1.53M，23.07 dB）。

![[assets/figures/papers/paper_list_l901_https_arxiv_org_abs_2604_10359/figures/003_Table_1.jpg]]
*Table 1: Results on LOLv1 [42], and LOLv2 [46] datasets (real and synthetic) across four model groups of parameter scales. Best performance in each group is highlighted in bold*

无参考评估（**Table 2**）进一步验证了 Multinex 的感知质量优势。在 MEF、LIME、DICM、NPE 四个数据集上，Multinex 取得最低的 **NIQE 均值 3.64**，优于所有对比方法，且未使用 GT-Mean 后处理——这直接反映了模型真实的亮度与颜色校正能力，而非人为膨胀指标。

![[assets/figures/papers/paper_list_l901_https_arxiv_org_abs_2604_10359/figures/005_Table_2.jpg]]
*Table 2: No-reference results on MEF, LIME, DICM, and NPE using NIQE [29] and BRISQUE [28]. Lower is better*

在下游任务方面，**Table 3** 展示了低光照目标检测（ExDark）的结果。Multinex-Nano 变体仅凭 **0.7K 参数** 取得最高的 **mAP50 84.6%**，证明增强增量公式在极低参数预算下仍能为高层视觉任务提供有效的前端预处理。

![[assets/figures/papers/paper_list_l901_https_arxiv_org_abs_2604_10359/figures/006_Table_3.jpg]]
*Table 3: Low-light object detection on ExDark [22]: per-class AP% and overall mAP50% , with LLIE model parameter count (P). Best results are in bold, second best are underlined*

### 消融实验：设计选择的因果验证

消融实验系统验证了 Multinex 三个核心设计维度的因果贡献。

**先验组合的因果分析。** **Table 4 (a)** 对比了不同输入表示的性能。仅使用 RGB 输入时 PSNR 为 22.74 dB；单独使用亮度先验或反射率先验分别提升至 22.86 dB 和 22.95 dB；同时使用双先验栈达到 **23.19 dB**，证实亮度-颜色解耦是性能提升的关键瓶颈。**Figure 4** 的定性结果直观展示了仅用单一先验时颜色偏差和亮度不均的失效模式。

**引导栈内部组件的贡献。** **Table 7** 和 **Table 8** 分别消融了亮度栈和反射率栈的特征图。亮度栈的四个特征图（Rec.709 亮度、vmax、lightness、L₂ 范数）具有互补性：移除任一特征图均导致 PSNR 下降，完整四图组合取得最优 23.19 dB，而最佳三图组合仅 22.74 dB。**Table 5** 的重要性排序显示，Rec.709 亮度贡献最大，L₂ 范数亮度提供独特的对比度线索。反射率栈的五个特征图（Cb、Cr、r、g、S）同样呈现互补效应，完整组合优于任何部分组合。

**网络组件的架构选择。** **Table 9** 消融了分量注意力（CWA）的放置位置。将 CWA 放置在投影层与融合块（FB）之间（"Between"）取得最佳 PSNR 23.19 dB，优于提前放置（"Before"，22.92 dB）或延后放置（"After"，22.88 dB）。这表明注意力机制在特征投影后、融合细化前介入，能最有效地选择性加权各先验分量。

**损失函数的联合效应。** **Table 6** 验证了多损失联合训练的必要性。单独使用 MSE 损失仅 22.83 dB；同时使用 MSE + MS-SSIM + Perceptual Loss 达到最高的 23.19 dB，兼顾像素精度、结构一致性与感知质量。

### 失败模式与局限性

尽管 Multinex 在轻量级设定下表现优异，其极低的参数预算（45K）带来了固有的能力边界。在极端低光或过曝场景下，模型可能产生光失真、噪声放大和色彩损失（见原文 Fig. 21）。细节重建能力有限，在复杂纹理场景下不如大型模型（如 **GLARE**，59.48M）。此外，当前工作未探讨对光谱失真、镜头眩光或混合光源场景的处理能力，这些构成了实际部署中的潜在失效模式。

### 公平性说明

所有对比均在相同的模型参数量级分组内进行（轻量级 < 1M、微型 < 0.01M 等），确保架构效率比较的公平性。无参考数据集结果未使用 GT-Mean 后处理，反映模型真实的亮度/颜色校正能力。

![[assets/figures/papers/paper_list_l901_https_arxiv_org_abs_2604_10359/figures/007_Table_4.jpg]]
*Table 4: Results of ablation studies (a), (b) and (c) validating design elements of Multinex*

## 定位与知识库关联

### 一、方法谱系：从Retinex重建到加性校正

Multinex的方法论定位源于对低光照增强领域两条主流路线的批判性整合：**基于物理先验的Retinex分解**与**端到端的学习增强**。

**与经典Retinex方法的关系。** 早期工作如**RetinexNet**将Retinex理论（I = L ⊙ R）直接嵌入深度学习框架，通过预测光照图L和反射图R来重建增强图像。这一范式面临两个根本性约束：（1）亮度与颜色在RGB等常用色彩空间中的**耦合**导致曝光修正与色调恢复相互干扰；（2）以**重建**为目标的优化使得网络必须学习完整的图像生成，而非仅关注所需的校正量。Multinex的关键突破在于**将Retinex分解从重建目标降级为结构先验**——不再要求网络输出L和R，而是利用Retinex理论指导一个**加性增强增量**（enhancement delta）的设计：

$$\hat{\mathbf{I}} = \mathbf{I} + \pmb{\Delta}_L \odot \pmb{\Delta}_R$$

这一范式转换使得网络只需学习“需要改变什么”，而非“图像应该是什么”，从而大幅降低了对模型容量的需求。

**与轻量级增强方法的对比。** 在轻量级方法谱系中，**ZeroDCE**（79K参数）通过曲线映射实现增强，但缺乏对颜色校正的显式建模；**PairLIE**（330K参数）虽采用Retinex框架，但仍以分解-重建为范式。**LYT-Net**（45K参数）是轻量级最强基线，通过在YUV空间中引入高效Transformer实现亮度-色度分离处理。Multinex（44.6K参数）以更少的参数量超越了LYT-Net（LOLv1上PSNR +0.81dB），其核心差异在于：LYT-Net依赖单一色彩空间（YUV）的隐式解耦，而Multinex通过**多视角解析先验栈**实现了显式、互补的亮度与色度线索聚合。

**与中/大型模型的定位差异。** 相较于**CIDNet**（1.88M，基于可学习色彩空间）、**RetinexFormer**（1.53M，CNN+Transformer混合架构）和**GLARE**（59.48M），Multinex并不追求通过增大模型容量来逼近重建精度上限，而是探索**在极端参数压缩下（<0.05M）通过结构化先验注入实现有效增强**的边界。这一设计哲学使其在参数量低两个数量级的情况下，仍在无参考数据集上取得了最低的NIQE均值（3.64），并在下游检测任务（ExDark）上以仅0.7K参数的Nano变体达到最高的mAP50（84.6%）。

### 二、知识库定位：先验驱动轻量增强的新范式

Multinex在低光照增强知识库中的核心贡献是提出并验证了**“解析先验栈 + 轻量融合网络”**这一设计范式。其知识增量体现在三个层面：

**（1）多视角亮度与色度先验的系统化构建。** 不同于依赖单一色彩空间转换的现有方法，Multinex从经典色彩理论中导出了两个互补的解析先验栈：亮度引导栈S_L（Rec.709亮度、最大值亮度、感知亮度、L2范数亮度）和反射率引导栈S_R（Cb、Cr色差分量、r/g归一化比例、饱和度）。消融实验（Table 4a）证实，同时使用双先验栈（PSNR 23.19）显著优于仅用单一先验或直接RGB输入（PSNR 22.74），验证了**亮度-色度解耦先验的协同增益**。

**（2）加性校正场的有效性证明。** 增强增量公式Δ_L ⊙ Δ_R将校正建模为亮度场与色度场的逐元素乘积，而非独立的图像生成。这一设计使得网络输出维度极低（亮度网络输出单通道，色度网络输出三通道），从根本上控制了参数增长。消融实验（Table 4b/c）进一步表明，该公式对先验栈的选择具有鲁棒性，但对网络组件的设计（如分量注意力CWA的放置位置）存在敏感性。

**（3）极端压缩下的性能边界探索。** Multinex-Nano（0.7K参数）在检测任务上的表现揭示了**先验驱动方法在微型模型上的潜力**——当网络容量不足以学习复杂表示时，解析先验可以提供有效的归纳偏置。这一发现为资源受限场景（如移动端实时增强、嵌入式视觉前端）提供了新的设计思路。

### 三、适用边界与局限

尽管Multinex在轻量级设定下表现优异，其方法边界和局限值得明确：

**已知局限。** 论文自身报告的失败模式包括：（1）在**极端低光或过曝场景**下可能产生光失真、噪声放大和色彩损失（见Fig. 21）；（2）由于参数量的根本性限制（45K），**细节重建能力**在纹理丰富或高频区域不如大型模型（如GLARE）；（3）当前设计未针对**光谱失真、镜头眩光或混合光源**场景进行验证。

**适用边界推断。** 基于方法设计可推断以下边界：（1）先验栈的解析计算依赖标准RGB输入，对非标准光谱响应（如多光谱、红外增强）的泛化能力未经验证；（2）加性校正公式假设增强可通过线性叠加实现，对于需要非线性色调映射或高光剪切恢复的场景可能不足；（3）双分支融合网络的结构对称性假设亮度与色度校正具有相似的融合复杂度，在色偏严重而亮度适中的退化场景下可能存在冗余。

### 四、开放问题

从Multinex的设计逻辑出发，以下问题值得后续工作关注：

1. **先验栈的扩展性。** 当前亮度与色度先验栈均基于经典色彩理论手工设计，能否通过学习或搜索自动发现更优的先验组合？先验栈的通道数与网络容量的最优配比如何确定？

2. **加性残差范式的推广。** 增强增量公式能否扩展到HDR恢复（需要处理剪切高光）、去雾（透射率图与增强增量的关系）或水下增强（光谱衰减的非均匀性）等任务？

3. **极端场景的鲁棒性增强。** 在保持低参数量的约束下，如何引入自适应机制（如场景难度感知的注意力调制）来缓解极端低光/过曝场景下的性能退化？

4. **与其他视觉任务的联合优化。** Multinex在ExDark上的检测结果表明其增强输出对下游任务友好，但当前训练仅使用增强损失。将检测/分割等高层任务的反馈纳入增强网络的训练，是否能在保持轻量级的同时进一步提升任务导向的增强质量？

## 原文 PDF

![[paperPDFs/CVPR_2026/Multinex_Lightweight_Low_light_Image_Enhancement_via_Multi_prior_Retinex.pdf]]
