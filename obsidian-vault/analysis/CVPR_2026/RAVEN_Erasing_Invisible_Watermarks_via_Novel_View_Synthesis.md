---
title: "RAVEN: Erasing Invisible Watermarks via Novel View Synthesis"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/RAVEN_Erasing_Invisible_Watermarks_via_Novel_View_Synthesis.pdf
project_link: null
code_link: null
aliases:
- RAVEN
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 在扩散潜空间中施加受控的视点变换（模拟相机平移），通过新视角合成扰动水印的空间对齐，同时保持语义内容。
primary_logic: 将水印去除重新定义为新视角合成问题：生成同一场景的感知一致替代视图，在保持视觉保真度的同时，天然地与嵌入的水印信号统计解相关。
claims:
- 我们通过将水印去除重新定义为新视角合成问题，暴露了不可见水印的一个根本漏洞。
- 关键洞察是：生成同一语义内容的感知一致替代“视图”会产生一个新图像实例，在保持视觉保真度的同时，统计上与嵌入的水印信号解相关。
- RAVEN 通过三阶段实现：部分扩散逆序、潜空间视点调制，以及视图引导的对应注意力，在无盒设定下达到最优去除效果。
- MS-COCO 上 TPR@1%FPR（TreeRing 语义水印） = 0.020
---

# RAVEN: Erasing Invisible Watermarks via Novel View Synthesis

> [!tip] 核心洞察
> 将水印去除重新定义为新视角合成问题：生成同一场景的感知一致替代视图，在保持视觉保真度的同时，天然地与嵌入的水印信号统计解相关。

| 字段 | 内容 |
|------|------|
| 中文题名 | RAVEN: 通过新视角合成擦除不可见水印 |
| 英文题名 | RAVEN: Erasing Invisible Watermarks via Novel View Synthesis |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.08832) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | RAVEN |
| Dataset | MS-COCO, DiffusionDB |

> [!tip] 效果简介
> - MS-COCO 上，TPR@1%FPR（TreeRing 语义水印） 0.020 vs 0.032（UnMarker） (-0.012)；Bit Accuracy（VINE 位流水印） 0.533 vs 0.573（UnMarker） (-0.040（更接近理想值 0.5）)。
> - DiffusionDB 上，TPR@1%FPR（语义水印平均） 0.029 vs 0.081（UnMarker） (-0.052)。

## 概要

RAVEN 揭示了一个不可见水印的根本性漏洞：**将水印去除重新定义为新视角合成问题**。其核心洞察在于——生成同一语义内容的感知一致替代“视图”，会在保持视觉保真度的同时，统计上与嵌入的水印信号解相关。

**问题瓶颈**：现有水印去除方法难以兼顾感知保真度与水印抑制。像素空间和频域攻击对语义水印效果有限，而基于扩散模型的纯化方法需要大幅注入噪声，破坏结构一致性。

**方法定位**：RAVEN 是一种零样本、无盒的扩散框架，通过三阶段流水线实现水印去除：
1. **部分扩散逆序**——在潜空间中注入受控噪声（强度 $s=0.15$），保留语义结构；
2. **潜空间视点调制**——通过全局相机平移函数在潜空间引入空间扰动，模拟视点变化；
3. **视图引导的对应注意力**——在去噪过程中耦合变换潜变量与参考潜变量，维持跨视结构、纹理和身份一致性。

**主要结果**：在涵盖 15 种水印方案和 14 种基线攻击的广泛评估中，RAVEN 在 MS-COCO 上将 TreeRing 语义水印的 TPR@1%FPR 降至 0.020（UnMarker 为 0.032），VINE 位流水印的 Bit Accuracy 降至 0.533（更接近理想随机值 0.5），同时在 DiffusionDB 上语义水印平均 TPR@1%FPR 降至 0.029（UnMarker 为 0.081），且保持优越的感知质量。

### 不可见水印的攻防困境

随着生成式人工智能的爆发，不可见水印已成为区分AI生成内容与真实内容的核心技术手段。主流水印方案可分为两类：**像素空间水印**（如DwtDct、SSL）在图像像素域嵌入信号，而**语义水印**（如TreeRing、ROBIN）在生成过程中将水印编码至图像的语义结构，后者对传统攻击表现出更强的鲁棒性。

然而，水印的鲁棒性与可去除性之间存在根本张力。现有水印去除方法陷入了一个关键瓶颈：**难以同时兼顾感知保真度与水印抑制**。像素空间攻击（如JPEG压缩、高斯模糊）和频域攻击（如VAE-C）对语义水印效果有限；而基于扩散模型的纯化方法（如**Regen**，Zhao et al., NeurIPS 2024）虽然能更有效地抑制水印，却需要大幅注入噪声，导致结构一致性严重受损——这正是当前方法的核心矛盾。

### 现有方法的三个缺口

从方法特性来看，现有水印去除基线在三个维度上存在明显短板（参见Table 1）：

1. **有效性不足**：对抗优化方法（如**UnMarker**）和可控再生方法（如**CtrlGen+**, Liu et al., arXiv 2024）对语义水印的抑制能力有限，难以将检测率降至随机猜测水平。
2. **质量退化严重**：扩散纯化方法为达到水印抑制效果，必须施加高强度噪声注入，导致输出图像出现模糊、伪影和结构失真。
3. **效率与通用性受限**：部分方法需要逐图像优化或额外训练，无法在零样本设定下快速部署。

### 核心动机：将水印去除重新定义为新视角合成

本文的核心洞察是：**生成同一语义内容的感知一致替代“视图”，会产生一个在保持视觉保真度的同时、统计上与嵌入水印信号解相关的全新图像实例**。这一洞察揭示了不可见水印的一个根本漏洞——水印信号依赖于图像的空间对齐，而通过受控的视点变换，可以在不破坏语义内容的前提下打破这种对齐。

基于此，RAVEN将水印去除重新概念化为**新视角合成问题**：在扩散模型的潜空间中施加受控的相机平移变换，模拟物理世界的视点变化，从而天然地将输出图像与原始水印信号统计解相关。这一范式转换使得水印抑制与感知保真度不再相互冲突，而是统一于同一生成过程之中。

### 无盒威胁模型下的攻击要求

RAVEN遵循严格的无盒威胁模型：攻击者无法访问水印检测器、水印密钥或任何特权信息，不使用附加数据或训练，仅在单张水印图像上操作。这一设定对攻击方法提出了极高要求——必须在没有任何先验的条件下，实现跨水印方案、跨数据集的鲁棒去除效果。

## 核心方法与创新机理

RAVEN 的核心创新在于将水印去除问题**重新定义为新视角合成（Novel View Synthesis）问题**，而非沿用传统的像素空间扰动、频域攻击或扩散纯化范式。这一视角转换带来了根本性的方法差异：现有方法要么在像素/频域直接破坏水印信号（对语义水印效果有限），要么通过高噪声注入进行扩散纯化（严重损害结构一致性）。RAVEN 则利用受控的视点变换，在保持语义内容的同时，天然地与嵌入的水印信号统计解相关。

具体而言，RAVEN 在以下四个关键维度上相对于基线方法做出了实质性改变：

### 1. 扩散逆序强度：从完全逆序到部分逆序

传统扩散纯化方法（如 **Regen**，Zhao et al., NeurIPS 2024）通常执行完全逆序或注入大量噪声，导致生成图像与原始图像产生显著偏差。RAVEN 采用**部分逆序**策略，仅在扩散过程的中间时间步 $\tau = \lfloor s \cdot T \rfloor$ 处注入受控噪声（默认强度 $s = 0.15$），在保留足够语义结构的同时，为后续视点调制留出操作空间。

### 2. 潜空间操作：从标准去噪到视点调制

基线方法在潜空间中仅执行标准去噪，缺乏空间变换能力。RAVEN 引入**潜空间视点调制**，通过全局相机平移函数 $\mathcal{C}_{\theta}(i,j) = (i + \Delta_x, j + \Delta_y)$ 对潜变量施加空间扰动，模拟视点变化。这一设计的关键洞察在于：水印信号通常依赖于精确的空间对齐，而视点平移会破坏这种对齐关系，从而实现水印抑制。

### 3. 注意力机制：从自注意力到视图引导的对应注意力

标准扩散 UNet 中的自注意力无法维持跨视点的结构一致性。RAVEN 提出**视图引导的对应注意力**，将变换后的潜变量（作为查询）与参考潜变量（作为键/值）进行交叉注意力计算：

$$\text{ViewAttn}(Q,K,V) = \text{softmax}\left(\frac{(W_Q \tilde{z}_t)(W_K z_t^{\text{ref}})^\top}{\sqrt{d}}\right) W_V z_t^{\text{ref}}$$

这一机制在去噪过程中持续将生成视图与原始视图进行结构对齐，确保纹理、细节和身份信息的一致性。消融实验表明，去除该模块会导致严重的结构失真。

### 4. 后处理：从无后处理到 CIELAB 颜色与对比度迁移

基线方法通常不包含专门的后处理步骤。RAVEN 在 CIELAB 空间中进行颜色与对比度迁移，保留输出图像的亮度通道，采用原始水印图像的色度信息，并匹配亮度通道的均值和标准差，有效修复视点变换可能引入的残余色偏，稳定提升 FID 指标。

这些 changed slots 共同构成了 RAVEN 的方法论优势：在无盒威胁模型下（不访问检测器、水印密钥或任何特权信息），仅通过单张水印图像即可实现最优的水印抑制效果，同时保持感知质量。

RAVEN 将水印去除重新定义为**新视角合成问题**：给定一张被嵌入不可见水印的图像，生成同一语义内容的感知一致替代“视图”，在保持视觉保真度的同时，使输出图像在统计上与嵌入的水印信号解相关。这一核心洞察暴露了不可见水印的一个根本漏洞——无需访问水印编码器、检测器或任何特权信息，仅利用公开可用的预训练扩散模型，即可实现高效的水印抑制。

### 威胁模型与优化目标

攻击者处于严格的**无盒设定**下：无法访问水印编码器 $\mathcal{U}_\zeta$、检测器 $\mathcal{V}_\eta$、水印密钥 $\kappa$，不能查询检测器，也没有干净-水印配对图像的监督信号。唯一可用的资源是公开的 image-to-image 扩散模型。

在此约束下，水印去除需同时满足三个目标：
- **检测规避（P1）**：使攻击图像 $\tilde{x}$ 提取的密钥与真实密钥的距离超过检测阈值 $\phi$，即 $d(\mathcal{V}_\eta(\tilde{x}), \kappa) > \phi$；
- **语义保持（P2）**：保留原始图像的语义内容；
- **视觉自然度（P3）**：输出图像应具备逼真的视觉质量。

### 三阶段流水线

RAVEN 通过三个阶段实现上述目标，整体流程如 Figure 1 所示：

**阶段一：部分扩散逆序（Partial Diffusion Inversion）**
将水印图像 $x_w$ 编码为潜变量 $z$，在时间步 $\tau = \lfloor s \cdot T \rfloor$（$s=0.15$）添加受控噪声，得到含噪潜变量：
$$z_{\tau} = \sqrt{\bar{\alpha}_{\tau}} z + \sqrt{1-\bar{\alpha}_{\tau}} \epsilon, \quad \epsilon \sim \mathcal{N}(0, I)$$
与完全逆序或高噪声注入的扩散纯化方法不同，部分逆序仅扰动中间层表示，在保留语义结构的同时为后续视点变换留出操作空间。

**阶段二：潜空间视点调制（Latent Viewpoint Modulation）**
在潜空间施加受控的几何变换，模拟相机视点变化。论文采用简洁高效的全局相机平移：
$$\mathcal{C}_{\theta}(i,j) = (i + \Delta_x, j + \Delta_y)$$
通过空间变形函数对含噪潜变量进行重采样：
$$\tilde{z}_{\tau}[i,j] = z_{\tau}[\mathcal{C}_{\theta}(i,j)]$$
这一操作扰动了水印信号的空间对齐，使其在后续去噪重建中难以保留，同时不破坏图像的语义布局。

**阶段三：视图引导的对应注意力（View-Guided Correspondence Attention）**
在去噪过程中，将变换后的潜变量 $\tilde{z}_t$ 与参考潜变量 $z_t^{\mathrm{ref}}$ 进行交叉注意力耦合：
$$\mathrm{ViewAttn}(Q,K,V) = \mathrm{softmax}\left(\frac{(W_Q\tilde{z}_t)(W_K z_t^{\mathrm{ref}})^\top}{\sqrt{d}}\right) W_V z_t^{\mathrm{ref}}$$
其中查询来自变换视图，键和值来自参考视图。该机制在维持跨视结构、纹理和身份一致性的同时，允许视点变换带来的局部变化，避免了标准自注意力下可能出现的严重结构失真。

**后处理：颜色与对比度迁移**
在 CIELAB 空间进行颜色迁移，保留输出图像的亮度通道，采用原始水印图像的色度：
$$x_c = \mathcal{F}_{\mathrm{RGB}}(L_{\mathrm{opt}}, a_w, b_w)$$
并通过亮度统计量匹配进行对比度对齐：
$$L_{\mathrm{final}} = \frac{\sigma_w}{\sigma_c}(L_c - \mu_c) + \mu_w$$
此后处理步骤稳定提升 FID，修复去噪过程中引入的残余色偏。

### 输入输出流

- **输入**：单张水印图像 $x_w$（无需原始文本提示，使用空文本提示重建）。
- **处理**：VAE 编码 → 部分逆序加噪 → 潜空间视点平移 → 视图引导注意力去噪 → VAE 解码 → CIELAB 颜色/对比度迁移。
- **输出**：感知上与原始图像一致、但水印信号被有效抑制的干净图像 $\tilde{x}$。

### 与基线方法的关键差异

Table 1 从有效性、质量和效率三个维度对比了 RAVEN 与现有方法。**VAE-C** 等像素空间攻击对语义水印效果有限且引入过度模糊；**Regen**（Zhao et al., NeurIPS 2024）和 **CtrlGen+**（Liu et al., arXiv 2024）等扩散纯化方法需要大幅注入噪声，破坏结构一致性；**UnMarker** 等对抗优化方法依赖检测器梯度，在无盒设定下受限。RAVEN 通过潜空间视点变换和对应注意力机制，在无盒约束下同时实现了最优的水印抑制和感知保真度。

![[assets/figures/papers/paper_list_l2039_https_arxiv_org_abs_2601_08832/figures/001_Table_1.jpg]]
*Table 1: Comparison of watermark removal methods across three dimensions: (i) Effectiveness, i.e., how strongly the attack suppresses both pixel-level and semantic watermarks; (ii) Quality, preservation of semantic content and visual naturalness; and (iii) Efficiency, compute budget in training and per-image processing. Regen [47] is efficient but limited to weak watermarks; Ctrl-Gen+ [25] requires multi-node training (8 GPUs); IRA [29] performs slow per-image optimization (≈ 40 min./image) and require access to model parameter to be effective; and UnMarker [21] degrades visual fidelity. Our method achieves superior performance across all dimensions*

RAVEN 将水印去除重新定义为新视角合成问题，其核心洞察在于：生成同一语义内容的感知一致替代“视图”会产生一个新图像实例，在保持视觉保真度的同时，统计上与嵌入的水印信号解相关。该方法在严格的无盒威胁模型下运行——攻击者不访问水印编码器、检测器、密钥或任何特权信息，仅使用公开可用的图像到图像扩散模型。

整个框架由四个关键模块串联构成。

---

### 模块一：部分扩散逆序（Partial Diffusion Inversion）

**目的**：将水印图像编码为潜变量，并在中间时间步注入受控噪声，在保留语义结构的同时为后续视点变换创造操作空间。

**公式**：

$$z_{\tau} = \sqrt{\bar{\alpha}_{\tau}} z + \sqrt{1 - \bar{\alpha}_{\tau}} \epsilon, \quad \epsilon \sim \mathcal{N}(0, I)$$

**变量含义**：
- $z$：从水印图像经 VAE 编码得到的初始潜变量
- $\bar{\alpha}_{\tau}$：扩散调度在时间步 $\tau$ 的累积信号保留系数，$\tau = \lfloor s \cdot T \rfloor$，其中 $s$ 为逆序强度（默认 $s = 0.15$）
- $\epsilon$：标准高斯噪声

**设计逻辑**：完全逆序（$s = 1.0$）会过度破坏结构信息，而完全不注入噪声（$s = 0$）则无法为视点变换提供足够的扰动空间。部分逆序在两者之间取得平衡——消融实验表明，增大 $s$ 会增强水印抑制但降低视觉质量，过低则可能保留水印。

---

### 模块二：潜空间视点调制（Latent Viewpoint Modulation）

**目的**：在扩散潜空间中施加受控的几何变换，模拟相机视点变化，从而扰动水印信号的空间对齐。

**公式**：

$$\tilde{z}_{\tau}[i, j] = z_{\tau}[\mathcal{C}_{\theta}(i, j)]$$

其中空间变形函数采用最简洁有效的全局相机平移：

$$\mathcal{C}_{\theta}(i, j) = (i + \Delta_x, \; j + \Delta_y)$$

**变量含义**：
- $\tilde{z}_{\tau}$：经视点调制后的潜变量
- $\mathcal{C}_{\theta}$：以 $\theta$ 为参数的空间变形函数
- $\Delta_x, \Delta_y$：水平和垂直方向的平移量

**因果机制**：不可见水印（尤其是语义水印）依赖像素或频域特征的精确空间对齐来实现可靠检测。通过引入全局平移，水印信号的空间分布被系统性扰动，使其与检测器期望的模式失配。同时，由于变换发生在潜空间而非像素空间，语义内容得以保留。

---

### 模块三：视图引导的对应注意力（View-Guided Correspondence Attention）

**目的**：在去噪过程中，将变换后的潜变量与参考潜变量进行交叉注意力，维持跨视图的结构、纹理和身份一致性。

**公式**：

$$\mathrm{ViewAttn}(Q, K, V) = \mathrm{softmax}\left(\frac{(W_Q \tilde{z}_t)(W_K z_t^{\mathrm{ref}})^\top}{\sqrt{d}}\right) W_V z_t^{\mathrm{ref}}$$

**变量含义**：
- $\tilde{z}_t$：当前去噪时间步 $t$ 的变换潜变量（作为查询 $Q$）
- $z_t^{\mathrm{ref}}$：参考潜变量（作为键 $K$ 和值 $V$），由原始水印图像经相同逆序过程生成
- $W_Q, W_K, W_V$：可学习的投影矩阵
- $d$：缩放因子，为键向量的维度

**设计逻辑**：标准的 UNet 自注意力仅在同一潜变量内部建立长程依赖，无法保证变换后视图与原始视图的一致性。视图引导的交叉注意力通过将变换潜变量的查询与参考潜变量的键/值关联，使模型在去噪时能够“参考”原始视图的细节信息。消融实验证实，去除该模块会导致严重的结构失真，而加入后可保持细粒度细节、纹理和结构一致性。

---

### 模块四：颜色与对比度迁移（Color and Contrast Transfer）

**目的**：在 CIELAB 空间进行颜色和对比度迁移，修复扩散重建过程中引入的残余色偏，提升感知质量。

**颜色迁移公式**：

$$x_c = \mathcal{F}_{\mathrm{RGB}}(L_{\mathrm{opt}}, a_w, b_w)$$

**对比度匹配公式**：

$$L_{\mathrm{final}} = \frac{\sigma_w}{\sigma_c}(L_c - \mu_c) + \mu_w$$

**变量含义**：
- $L_{\mathrm{opt}}$：RAVEN 输出图像的亮度通道
- $a_w, b_w$：原始水印图像的色度通道
- $L_c$：颜色迁移后中间结果的亮度通道
- $\mu_w, \sigma_w$：原始水印图像亮度通道的均值和标准差
- $\mu_c, \sigma_c$：中间结果亮度通道的均值和标准差

**设计逻辑**：颜色迁移保留输出图像的亮度信息，同时采用原始水印图像的色度，恢复色彩一致性。对比度匹配进一步对齐亮度统计量，使输出图像在感知上更接近原始水印图像。消融实验表明，该后处理步骤稳定提升 FID 指标。

## 实验与关键发现

### 主实验结果

RAVEN 在 MS-COCO 数据集上针对 **15 种水印方案** 和 **14 种基线攻击** 进行了全面评估。Table 2 报告了核心量化结果，分为两类水印的验证性能：

![[assets/figures/papers/paper_list_l2039_https_arxiv_org_abs_2601_08832/figures/003_Table_2.jpg]]
*Table 2: Verification performance of different watermarking methods under various attacks. TPR@1%FPR is reported for in-generation semantic watermarking methods (TreeRing to ROBIN), where lower values indicate better attack performance. Bit Accuracy is reported for post-hoc bitstream-based methods (DwtDct to VINE), where values near 0.5 indicate successful watermark randomization. RAVEN achieves the lowest detection rates across both categories, demonstrating superior removal efficacy while maintaining visual quality*

**语义水印（TPR@1%FPR，越低越好）**：在 TreeRing 水印上，RAVEN 将 TPR@1%FPR 压至 **0.020**，显著优于最强基线 UnMarker 的 0.032，降幅达 37.5%。在 DiffusionDB 数据集上（Table 6），RAVEN 对语义水印的平均 TPR@1%FPR 仅为 **0.029**，而 UnMarker 为 0.081，降幅达 64.2%。这一结果表明，RAVEN 通过潜空间视点变换，有效破坏了语义水印在生成过程中的空间对齐结构。

**位流水印（Bit Accuracy，越接近 0.5 越好）**：在 VINE 水印上，RAVEN 的 Bit Accuracy 为 **0.533**，比 UnMarker 的 0.573 更接近理想随机值 0.5，表明水印比特被更彻底地随机化。

Table 3 报告了图像质量指标。RAVEN 在 FID 和 CLIP-Text Score 上均保持竞争力，证明其在强力水印抑制的同时，未牺牲感知保真度。Figure 2 的定性对比显示，基线方法（如 Regen、CtrlGen+）常出现模糊、伪影或色彩偏移，而 RAVEN 保持了细节纹理和自然光影。

![[assets/figures/papers/paper_list_l2039_https_arxiv_org_abs_2601_08832/figures/006_Figure_2.jpg]]
*Figure 2: Qualitative comparison of watermark removal methods. The top row shows full images, while the bottom row displays zoomed-in regions (red boxes) for detailed inspection. VAE-C [7] introduces excessive blurring that degrades fine details. Regen [47] produces visible artifacts due to high noise injection required for watermark removal. Rinse exhibits unnatural color shifts and loss of photorealism, a consequence of performing multiple regeneration passes. UnMarker [25] leaves noisy residual artifacts that compromise visual quality. CtrlGen+ [25] produces overly stylized outputs that deviate from natural appearance. In contrast, RAVEN preserves finegrained details, natural textures, and photore...*

### 消融实验

**扩散逆序强度 s**：Figure 3 和 Table 4 揭示了 s 参数的核心权衡。增大 s（如从 0.10 到 0.25）会增强水印抑制效果，但 FID 随之上升，视觉质量下降；过低的 s（如 0.05）则可能保留水印残余。RAVEN 选择 s=0.15 作为最优平衡点，在有效去水印的同时保持结构完整性。

**视图引导的对应注意力**：Figure 4 的消融表明，移除该注意力模块会导致严重的结构失真——输出图像出现错位、撕裂和纹理混乱。加入视图引导注意力后，RAVEN 能够精确保持跨视点的细节、纹理和身份一致性。这一机制的核心在于，通过交叉注意力将变换后的潜变量（查询）与参考潜变量（键/值）耦合，确保去噪重建不偏离原始语义结构。

**颜色与对比度迁移后处理**：Figure 5 显示，CIELAB 空间的颜色和对比度迁移稳定改善了 FID。该后处理保留输出图像的亮度通道，同时从原始水印图像借用色度信息，有效修复了扩散重建中常见的残余色偏，提升了色彩一致性。

### 模型泛化性

Table 5 验证了 RAVEN 的模型无关性。在不同 Stable Diffusion Image-to-Image 骨干网络（包括不同版本和微调变体）上，RAVEN 均实现了一致的水印抑制效果，无需针对特定模型调优。这表明视点变换攻击利用的是扩散模型的通用重建机制，而非特定架构的漏洞。

![[assets/figures/papers/paper_list_l2039_https_arxiv_org_abs_2601_08832/figures/008_Table_5.jpg]]
*Table 5: Model-agnostic watermark removal. RAVEN achieves consistent watermark suppression across different Stable Diffusion Image-to-Image backbones, demonstrating generalizability without model-specific tuning*

### 失败模式与局限性

尽管 RAVEN 在整体上表现优异，仍存在以下局限：

1. **空间偏移**：由于采用全局相机平移进行视点调制，输出图像与原始水印图像存在轻微的空间偏移。这在需要精确像素对齐的下游任务中可能构成问题。
2. **扩散模型依赖**：RAVEN 依赖公开可用的预训练图像到图像扩散模型。若防御方限制或禁用此类模型的访问，攻击效力将受到直接影响。
3. **空文本提示限制**：在严格无盒设定下，无法获取原始文本提示，RAVEN 使用空文本提示进行重建，可能限制与原始语义的完全对齐。
4. **计算开销**：单张图像处理约需 6 秒（A100 GPU），尚不适合实时大规模部署场景。

### 公平性说明

所有实验严格遵循无盒威胁模型：攻击者不访问水印编码器、检测器、密钥或任何特权信息，不使用附加训练数据，仅在单张水印图像上操作。实验覆盖 15 种水印方案（涵盖语义水印和位流水印两大类）和 14 种基线攻击，在 MS-COCO、DiffusionDB 等多个数据集上评估，结果具有广泛代表性。

![[assets/figures/papers/paper_list_l2039_https_arxiv_org_abs_2601_08832/figures/009_Figure_5.jpg]]
*Figure 5: Effect of color and contrast transfer. FID comparison across four watermarking methods before and after applying color and contrast transfer in CIELAB space. The post-processing step consistently improves FID*

![[assets/figures/papers/paper_list_l2039_https_arxiv_org_abs_2601_08832/figures/013_Figure_6.jpg]]
*Figure 6: Qualitative comparison of watermark removal methods. VAE-B [7] introduces excessive blurring that degrades fine details. Regen [47] produces visible artifacts due to high noise injection required for watermark removal. Rinse exhibits unnatural color shifts and loss of photorealism, a consequence of performing multiple regeneration passes. UnMarker [25] leaves noisy residual artifacts that compromise visual quality. CtrlGen+ [25] produces overly stylized outputs that deviate from natural appearance. In contrast, RAVEN preserves fine-grained details, natural textures, and photorealistic appearance. Note that the images for UnMarker [25] and RAVEN differ slightly from other methods due to crop...*

## 定位与知识库关联

### 与基线方法的关系

RAVEN 在三个关键维度上重新定义了水印去除攻击的设计范式（见 Table 1）。现有基线可归纳为三类：**像素/频域攻击**（VAE-C、亮度调整、JPEG 压缩等）对语义水印几乎无效；**对抗优化方法**（如 UnMarker）需要迭代优化，计算开销大且易产生感知伪影；**扩散纯化方法**（如 **Regen** (Zhao et al., NeurIPS 2024)、**CtrlGen+** (Liu et al., arXiv 2024)）通过大量注入噪声来破坏水印，但代价是结构一致性的显著退化。

RAVEN 的核心区分点在于**将水印去除重新定义为新视角合成问题**，而非传统的噪声注入或对抗扰动。这一视角转换带来了三个方法层面的根本差异：

1. **部分扩散逆序（强度 s=0.15）**：相比 Regen 等方法的完全逆序或高噪声策略，RAVEN 仅在中间时间步 τ 添加受控噪声，保留语义结构的同时为后续视点变换留出操作空间。
2. **潜空间视点调制**：通过全局相机平移函数 $\mathcal{C}_{\theta}(i,j) = (i+\Delta_x, j+\Delta_y)$ 在潜空间引入空间扰动，这是现有所有基线方法均不具备的能力。该操作模拟了物理世界中的视点变化，使水印信号在统计上与输出图像解相关。
3. **视图引导的对应注意力**：在去噪过程中，将变换后的潜变量（Query）与参考潜变量（Key/Value）进行交叉注意力，维持跨视点的结构、纹理和身份一致性。这是对标准 UNet 自注意力的关键替换，解决了单纯空间变换导致的结构失真问题。

实验证据表明（Table 2），RAVEN 在 MS-COCO 数据集上对 TreeRing 语义水印的 TPR@1%FPR 降至 0.020，优于最强基线 UnMarker 的 0.032；对 VINE 位流水印的 Bit Accuracy 降至 0.533，更接近理想随机值 0.5（UnMarker 为 0.573）。在 DiffusionDB 数据集上（Table 6），RAVEN 的平均 TPR@1%FPR 为 0.029，相比 UnMarker 的 0.081 降低了 0.052。

### 适用边界与局限

RAVEN 的适用性受以下条件约束：

- **依赖公开扩散模型**：攻击需要访问预训练的 Stable Diffusion Image-to-Image 模型。若防御方禁用或限制该模型的访问，攻击效力将直接受影响。Table 5 表明 RAVEN 在不同 SD 骨干网络上具有一定泛化性，但本质上仍绑定于扩散模型生态。
- **空间偏移的固有代价**：由于采用视点平移，输出图像与原始图像存在轻微的空间偏移。论文已明确指出这一限制，这是新视角合成范式无法完全消除的副作用。
- **无盒约束下的语义对齐**：在无法获取原始文本提示的无盒设定下，RAVEN 使用空文本提示进行重建，可能限制与原始语义的完全对齐。这是所有无盒扩散攻击的共性瓶颈。
- **计算效率**：单张图像处理约需 6 秒（A100 GPU），虽优于迭代优化方法，但尚不适合实时大规模部署场景。

### 开放问题

RAVEN 揭示的“视点变换可解耦水印信号与语义内容”这一洞察，为未来研究打开了若干方向：

1. **跨模态泛化**：新视角合成攻击能否推广至视频水印？视频帧间的时间连续性可能为防御提供额外约束，也可能为攻击提供更丰富的变换空间。
2. **防御方的自适应策略**：若水印方案引入视点不变特征或几何鲁棒编码，RAVEN 的有效性将如何变化？这本质上是一场“变换-不变性”的军备竞赛。
3. **更丰富的几何变换空间**：当前仅采用全局平移，能否结合缩放、旋转、透视变换等更精细的几何操作，在进一步增强水印抑制的同时不损害感知质量？
4. **检测方升级的影响**：若检测方采用自适应阈值或更强大的语义水印方案（如基于对抗训练的鲁棒水印），基于视点解相关的攻击策略是否需要根本性调整？

## 原文 PDF

![[paperPDFs/CVPR_2026/RAVEN_Erasing_Invisible_Watermarks_via_Novel_View_Synthesis.pdf]]
