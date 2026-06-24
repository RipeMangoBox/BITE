---
title: "CoD: A Diffusion Foundation Model for Image Compression"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CoD_A_Diffusion_Foundation_Model_for_Image_Compression.pdf
project_link: null
code_link: "https://github.com/microsoft/GenCodec/tree/main/CoD"
aliases:
- CoD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将压缩条件从文本替换为端到端可学习的本机图像令牌（通过量化瓶颈），并在极低比特率下进行统一训练，使扩散模型同时习得压缩先验和生成先验，从而实现跨码率的高效压缩与合成。
primary_logic: 通过训练一个面向压缩的扩散基础模型 CoD，利用量化图像令牌作为条件，结合修正流（rectified flow）与统一训练策略（在 t=0 时联合优化失真和感知），可以在极低比特率下实现端到端的压缩-生成联合优化，在保真度和感知质量上超越现有文本条件和潜在扩散方案。
claims:
- CoD 替换 Stable Diffusion 后，在零样本压缩框架 DiffC 上实现 SOTA，尤其在 0.0039 bpp 超低比特率下显著提升重建质量。
- 像素空间 CoD 达到与 VTM 可比的 PSNR（BD-Rate −2.1%），同时在 FID/DISTS 上大幅优于 GAN 基感知编解码器（MS-ILLM, HiFiC 等）。
- 统一训练（unified training）消除了仅用修正流损失导致的颜色偏移，并赋予了通过采样步数控制失真-感知权衡的能力（一步推理可提升 3.4 dB PSNR）。
- CoD 训练成本极低，仅需约 20 A100 GPU 天（约为 Stable Diffusion v1.5 的 0.3%），且全部使用开源数据集，易于复现。
---

# CoD: A Diffusion Foundation Model for Image Compression

> [!tip] 核心洞察
> 通过训练一个面向压缩的扩散基础模型 CoD，利用量化图像令牌作为条件，结合修正流（rectified flow）与统一训练策略（在 t=0 时联合优化失真和感知），可以在极低比特率下实现端到端的压缩-生成联合优化，在保真度和感知质量上超越现有文本条件和潜在扩散方案。

| 字段 | 内容 |
|------|------|
| 中文题名 | CoD：面向压缩的扩散基础模型 |
| 英文题名 | CoD: A Diffusion Foundation Model for Image Compression |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.18706) · [Code](https://github.com/microsoft/GenCodec/tree/main/CoD) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | CoD |
| Dataset | Kodak, CLIC2020 |

> [!tip] 效果简介
> - Kodak (512×512) 上，BD-Rate (PSNR) -2.1% (以 VTM 为锚点) vs VTM (PSNR 相当或略优于 VTM)。
> - Kodak (256×256) 上，FID / 重建质量 CoD 49M 参数显著优于 MS-ILLM 181M vs MS-ILLM (GAN-based) (更少的参数实现更好的 FID 和纹理细节)。
> - CLIC2020 (512×512) 上，PSNR, DISTS, FID 像素空间 CoD 在所有比特率上优于 HiFiC, MS-ILLM, CDC, TACO vs HiFiC, MS-ILLM, CDC, TACO (PSNR 更高（可达 ~47 dB@4 bpp），DISTS/FID 更低)。

## 概述

图像压缩长期面临一对根本矛盾：在极低比特率下，传统编解码器（如 VVC/H.266 的参考软件 VTM）能保持高 PSNR，但重建结果模糊、缺乏纹理细节；而基于生成对抗网络（GAN）的感知编解码器（如 HiFiC、MS-ILLM）虽能合成逼真纹理，却往往引入伪影且 PSNR 偏低。近年来，文本到图像的扩散模型（如 Stable Diffusion）被尝试用作压缩解码器，利用其强大的生成先验在超低码率下重建语义合理的图像。然而，这一范式存在**关键瓶颈**：文本条件由冻结的字幕器（如 BLIP-2）生成，无法携带精细的空间与纹理信息，且离散的文本词汇阻断了编码器与解码器的端到端联合优化；同时，潜在扩散模型受限于 VAE 的重建质量上限，难以在宽比特率范围内同时实现高 PSNR 和高感知质量。

本文提出 **CoD（Compression-oriented Diffusion）**，首个面向压缩的扩散基础模型。其核心思想是**将压缩条件从文本替换为端到端可学习的本机图像令牌**：通过一个量化瓶颈将图像压缩为极低比特率的离散令牌，再用这些令牌作为条件驱动扩散模型解码重建。这一设计使编码器、瓶颈和解码器能够联合优化，让扩散模型同时习得压缩先验和生成先验。在此基础上，CoD 采用**修正流（rectified flow）与统一训练策略**：在训练时随机选取部分样本在时间步 t=0 进行一步重建监督，将失真项直接融入扩散损失，从而消除纯流匹配训练导致的颜色偏移，并赋予通过调节采样步数控制失真-感知权衡的能力。

**核心结论与主要结果：**

- **零样本压缩框架的即插即用提升**：将 CoD 替换 Stable Diffusion 后，在零样本扩散压缩方法 DiffC 上实现 SOTA 性能，尤其在 0.0039 bpp 的超低比特率下重建质量显著提升（Figure 5, Figure 6）。
- **像素空间性能**：像素空间 CoD 在 Kodak 数据集上取得与 VTM 可比的 PSNR（BD-Rate 为 −2.1%，以 VTM 为锚点），同时在 FID 和 DISTS 指标上大幅优于 GAN 基感知编解码器（Figure 8）。在 4 bpp 下可达到约 47 dB 的近无损 PSNR。
- **失真-感知权衡控制**：统一训练使 CoD 具备零样本的失真-感知权衡调节能力：将采样步数从 25 步降至 1 步可提升 3.4 dB PSNR（Figure 5 左），无需重新训练。
- **极高训练效率**：CoD 仅需约 20 A100 GPU 天完成训练（约为 Stable Diffusion v1.5 的 0.3%），且全部使用 ImageNet、OpenImages、SA-1B 等开源数据集，易于复现。

**方法定位**：CoD 不同于固定的编解码器，而是一个面向压缩的**基础模型**。它可服务于多种下游扩散压缩框架（如 DiffC、DDCM、单步蒸馏等），在像素空间和潜在空间均可部署。在方法谱系中，CoD 填补了传统编解码器（高 PSNR 但低感知质量）与 GAN 基感知编解码器（高感知质量但 PSNR 不足）之间的空白，同时克服了文本条件扩散压缩方法的端到端优化障碍。

## 背景与动机

### 图像压缩的经典范式与扩散模型的介入

传统图像压缩遵循“编码—解码”的确定性映射：给定图像 $x$，编码器 $\Theta$ 将其压缩为紧凑表示 $y$，解码器 $\Phi$ 再从 $y$ 重建 $\hat{x}$：

$$y = \operatorname{Encode}(x, \Theta), \quad \hat{x} = \operatorname{Decode}(y, \Phi)$$

这一范式在 VVC/H.266（以 **VTM** 为参考实现）等标准中已达到极高的率失真效率。然而，极低比特率下（如 <0.01 bpp），传统编解码器受限于信息瓶颈，重建图像往往丢失纹理细节，呈现模糊或块效应。

近年来，扩散模型（diffusion models）凭借强大的生成先验，在图像合成上展现出惊人的纹理生成能力。研究者自然想到将扩散模型引入压缩：用扩散模型的生成先验来“脑补”被量化丢弃的高频信息，从而在极低码率下实现感知质量跃升。这一思路催生了以 **Stable Diffusion** 为基础模型的扩散压缩方法，如零样本方法 **DiffC**、**DDCM**，以及微调式方法 **PerCo**、**OSCAR** 等。

### 现有扩散压缩方案的双重瓶颈

尽管前景诱人，现有扩散压缩方法面临两个根本性瓶颈：

**瓶颈一：文本条件的信息带宽不足。** Stable Diffusion 等文本到图像扩散模型使用自然语言描述（通常由 BLIP-2 等字幕器生成）作为条件信号。然而，文本词汇是离散且粗粒度的，无法携带精确的空间布局、纹理细节和局部结构信息。这导致两个后果：其一，编码器无法将精细的图像信息有效注入解码器；其二，字幕器是冻结的，编码器与解码器无法端到端联合优化，压缩效率大打折扣。实验表明，在零样本压缩框架 DiffC 中，文本条件甚至对压缩性能产生负面影响（Figure 5 右）。

**瓶颈二：潜在扩散的 VAE 重建上限。** 基于 Stable Diffusion 的潜在空间编解码器将图像编码到 SD-VAE 的潜在空间，再对潜在变量进行量化和扩散解码。这一设计天然受限于 VAE 的重建质量上限——即使比特率无限增大，PSNR 也无法突破约 26 dB（0.6 bpp 时）。这意味着潜在扩散方案无法覆盖从极低到近无损的宽比特率范围，也无法同时实现高 PSNR 和高感知质量。

### 本工作的核心动机

上述瓶颈的根源在于：**现有扩散模型是为“文本到图像生成”设计的，而非为“图像压缩”设计的**。压缩任务需要的是：条件信号能承载精细的图像信息，编码器与解码器能端到端联合优化，且模型能在统一框架下覆盖从极低比特率到近无损的全码率范围。

CoD（Compression-oriented Diffusion）正是为解决这一根本性错配而提出。其核心思路是：**从零开始训练一个面向压缩的扩散基础模型**，用可学习的本机图像令牌（native image tokens）替代文本条件，通过量化瓶颈实现极低比特率，并在修正流（rectified flow）框架下统一优化压缩失真与扩散感知损失。这一设计使 CoD 既能作为独立编解码器工作，又能作为基础模型替换 Stable Diffusion，赋能下游扩散压缩方法。

## 核心创新

CoD 的核心创新在于**将扩散模型的生成条件从文本替换为端到端可学习的本机图像令牌**，并配套设计了**统一训练策略**，从而将压缩任务从“文本条件的零样本适配”升级为“压缩-生成的联合优化”。这一范式转换通过四个关键“changed slots”实现，从根本上解决了现有文本到图像扩散模型在压缩场景中的结构性缺陷。

### 条件信息：从文本描述到量化图像令牌

现有扩散压缩方法（如 **DiffC**、**DDCM**）直接复用预训练的文本到图像扩散模型（如 **Stable Diffusion**），依赖 BLIP-2 等字幕器生成的文本描述作为条件信号。这一方案存在两个致命瓶颈：

1. **信息瓶颈**：自然语言本质上是离散且高度抽象的，无法携带精细的空间结构、纹理细节和局部语义信息。字幕器将图像压缩为一句或一段文本的过程，造成了不可逆的信息损失。
2. **优化断裂**：字幕器与扩散模型分别预训练，彼此冻结，无法进行端到端的联合优化。编码器（字幕器）的压缩目标与解码器（扩散模型）的重建目标完全脱节。

CoD 将条件信息替换为**本机图像令牌**：通过一个可训练的量化图像编码器（Condition Encoder）将输入图像 $x$ 压缩为紧凑的潜在表示，再经由信息瓶颈（16-way 矢量量化）离散化为极低比特率的码流（最低仅 0.0039 bpp），最后通过条件解码器恢复为条件表示 $c$。这一设计使得条件信号本身成为压缩过程的一部分，编码器和解码器可以针对压缩目标进行端到端联合优化，从根本上消除了文本条件的信息瓶颈和优化断裂问题。

### 训练范式：从分别预训练到端到端联合优化

传统扩散压缩方法采用“预训练扩散模型 + 冻结条件网络”的分离式训练：扩散模型的生成能力来自大规模文本-图像数据的预训练，压缩任务仅通过调整采样策略或添加轻量级条件注入来实现零样本适配。这种范式下，扩散模型的生成先验与压缩任务之间存在根本性的错配——模型从未学习过“从压缩码流重建图像”这一任务。

CoD 采用**完全端到端的联合训练**：编码器、瓶颈、条件解码器和扩散模型从零开始同步训练，统一优化压缩失真与扩散感知损失。训练数据从文本-图像对（如 LAION-5B）转变为纯图像数据集（ImageNet-21K、OpenImages、SA-1B），实现完全自监督。这一转变的关键意义在于：扩散模型在训练过程中同时习得了**压缩先验**（如何从极低比特率码流中提取有效信息）和**生成先验**（如何生成逼真的图像细节），两者在统一的训练目标下相互增强，而非彼此割裂。

### 扩散损失与训练策略：修正流 + 统一训练

CoD 在扩散损失层面的创新体现在两个层面：

**修正流替代传统扩散损失**。传统扩散模型使用 DDPM/DDIM 的噪声预测损失或 flow matching 损失，这些损失在 $t=0$ 时缺乏对一步重建的直接监督。CoD 采用修正流损失 $\mathcal{L}_{\mathrm{RF}} = \mathrm{MSE}(v_t, v_t^{\mathrm{pred}})$，其中在 $t=0$ 时，修正流损失等价于一步重建的 MSE 失真：

$$\mathcal{L}_{\mathrm{RF}}|_{t=0} = \mathrm{MSE}(v_0, v_0^{\mathrm{pred}}) = \mathrm{MSE}(x, \hat{x}_0)$$

这一等价关系为将失真项融入扩散训练提供了数学基础。

**统一训练策略**。基于上述等价关系，CoD 提出了统一训练方案：训练时随机选取 $\alpha\%$ 的样本在 $t \in [0,1]$ 上训练（覆盖完整扩散过程），其余样本强制在 $t=0$ 训练（等价于一步重建的失真优化）。这一策略的核心效果是：

- 消除了仅用修正流损失导致的颜色偏移问题；
- 赋予模型通过采样步数控制失真-感知权衡的能力：多步采样（25 步）获得最佳感知质量，单步推理可提升约 3.4 dB PSNR；
- 使扩散模型在极低比特率下同时习得压缩先验和生成先验。

最终训练目标整合了修正流损失、表示对齐损失、码本承诺损失和辅助损失：

$$\mathcal{L} = \mathcal{L}_{\mathrm{RF}} + \lambda \cdot \mathcal{L}_{\mathrm{REPA}} + \beta \cdot \mathcal{L}_{\mathrm{C}} + \gamma \cdot \mathcal{L}_{\mathrm{aux}}$$

其中 $\lambda=0.5$，$\beta=0.25$，$\gamma=1.0$。

### 训练数据：从文本-图像对到纯图像数据集

CoD 完全摆脱了对文本标注的依赖，仅使用纯图像数据集进行自监督训练。这一改变的深层意义在于：

- **数据获取成本大幅降低**：无需昂贵的图像-文本配对数据，可使用更大规模、更多样化的图像数据集；
- **避免文本域偏差**：文本到图像模型受限于训练文本的分布，可能在某些视觉概念上存在盲区；纯图像训练使模型直接学习视觉世界的统计规律；
- **训练效率显著提升**：CoD 仅需约 20 A100 GPU 天（约为 Stable Diffusion v1.5 的 0.3%），全部使用开源数据集，易于复现。

### 创新总结

CoD 的四项关键改动形成了一个完整的创新闭环：**本机图像令牌**解决了条件信息瓶颈，**端到端联合训练**实现了压缩与生成的协同优化，**修正流 + 统一训练**提供了数学上优雅的失真-感知联合优化框架，**纯图像自监督训练**大幅降低了数据和计算门槛。这些创新共同使 CoD 在极低比特率下实现了超越现有文本条件和潜在扩散方案的保真度与感知质量，同时保持了极低的训练成本。

## 整体框架

CoD 的整体框架围绕一个核心设计展开：**用端到端可学习的本机图像令牌替代文本条件**，将压缩编码与扩散生成统一为一个可联合优化的基础模型。如图 1 所示，传统文本-图像扩散模型用于压缩时，条件信息来自冻结的字幕器（如 BLIP-2），文本词汇无法携带精细的空间和纹理信息，且编码器与解码器被割裂，无法进行端到端优化。CoD 则从零开始训练，直接学习将图像压缩为紧凑的离散令牌，并以这些令牌作为扩散解码器的唯一条件，实现压缩与生成的协同优化。

### 模块组成与数据流

CoD 的 pipeline 由四个核心模块串联构成（图 2），形成一条从像素到码流再到重建像素的完整通路：

1. **条件编码器（Condition Encoder）**：接收原始图像 $x$，通过残差块和注意力层将其压缩为紧凑的潜在表示，输出分辨率为输入的 1/32。该模块的作用是将高维像素空间信息高效地浓缩为低维特征。

2. **熵瓶颈（Entropy Bottleneck）**：对编码器输出的连续表示进行矢量量化，将其离散化为极低比特率的码流。具体而言，采用码本大小 $N = 2^4 = 16$ 的矢量量化，对应每 $(32 \times 32)$ 像素块仅需 4 bits，即 **0.0039 bpp** 的超低比特率。这一瓶颈是 CoD 实现跨码率压缩的关键——通过在极低比特率下进行统一训练，迫使扩散模型同时习得强压缩先验和强生成先验。

3. **条件解码器（Condition Decoder）**：从量化令牌 $y$ 恢复出中间压缩条件 $c$，输出分辨率为原始图像的 1/16。该条件 $c$ 将作为扩散模型的引导信号，替代传统方案中的文本嵌入。

4. **扩散模型（Diffusion Model）**：采用 **DiT 骨干 + DDT 头**的解耦架构。DiT 骨干在 1/16 分辨率上执行去噪，将条件 $c$ 与加噪输入沿通道拼接；DDT 头负责将去噪结果上采样至全分辨率，生成最终重建图像 $\hat{x}$。

### 像素空间与潜在空间的双轨设计

CoD 同时支持像素空间和潜在空间两种工作模式，以覆盖不同的比特率范围和应用场景：

- **像素空间 CoD**：直接在原始像素上建模扩散过程，不受任何预训练 VAE 的重建质量限制。这使得像素空间 CoD 能够在宽比特率范围内（从 0.0039 bpp 到 4 bpp 以上）持续提升重建质量，在 4 bpp 时可达到约 47 dB 的近无损 PSNR。
- **潜在空间 CoD**：在 Stable Diffusion 的 VAE 潜在空间中操作，利用 VAE 的压缩优势在极低比特率下（<0.02 bpp）取得最佳的感知质量。但其 PSNR 和比特率范围受限于 SD-VAE 的重建上限（约 26 dB @ 0.6 bpp），这是所有基于该 VAE 的方法的共同约束。

### 训练范式：修正流 + 统一训练

CoD 采用**修正流（Rectified Flow）**作为扩散训练框架，预测速度场 $v_t$ 并以 $\mathcal{L}_{\mathrm{RF}} = \mathrm{MSE}(v_t, v_t^{\mathrm{pred}})$ 作为基础损失。其关键创新在于**统一训练策略**：在训练时随机选取 $\alpha\%$ 的样本使用 $t \in [0, 1]$ 的标准修正流训练，其余 $(1-\alpha)\%$ 的样本强制在 $t=0$ 处训练。由于在 $t=0$ 时修正流损失等价于一步重建的 MSE 失真（$\mathcal{L}_{\mathrm{RF}}|_{t=0} = \mathrm{MSE}(x, \hat{x}_0)$），该策略将压缩失真项无缝融入扩散训练，实现了**一步失真与多步感知的联合优化**。

最终训练目标为四项损失的加权和：

$$\mathcal{L} = \mathcal{L}_{\mathrm{RF}} + \lambda \cdot \mathcal{L}_{\mathrm{REPA}} + \beta \cdot \mathcal{L}_{\mathrm{C}} + \gamma \cdot \mathcal{L}_{\mathrm{aux}}$$

其中 $\lambda=0.5$、$\beta=0.25$、$\gamma=1.0$，$\mathcal{L}_{\mathrm{REPA}}$ 为表示对齐损失，$\mathcal{L}_{\mathrm{C}}$ 为码本承诺损失，$\mathcal{L}_{\mathrm{aux}}$ 为辅助监督损失。

### 与现有范式的本质差异

| 维度 | 文本-图像扩散压缩（Stable Diffusion） | CoD |
|------|--------------------------------------|-----|
| 条件信息 | 文本描述（BLIP-2 生成） | 可学习图像令牌（量化瓶颈） |
| 训练范式 | 分别预训练，条件网络冻结 | 端到端联合训练编码器-瓶颈-解码器 |
| 扩散损失 | 标准 DDPM/DDIM 噪声预测 | 修正流 + t=0 失真联合优化 |
| 训练数据 | 文本-图像对（LAION-5B） | 纯图像数据集（ImageNet-21K, OpenImages, SA-1B） |
| 训练成本 | ~6,250 A100 GPU 天 | ~20 A100 GPU 天（约 0.3%） |

这一框架设计使 CoD 成为一个通用的压缩基础模型，可被下游扩散编解码器（如 DiffC、DDCM）直接替换 Stable Diffusion 使用，在零样本设置下即可获得显著性能提升，尤其是在超低比特率场景中。

### 补充图表

![[assets/figures/papers/paper_list_l847_https_arxiv_org_abs_2511_18706/figures/001_Figure_1.jpg]]
*Figure 1: Overview of Compression-oriented Diffusion (CoD) foundation models, which are trained from scratch to jointly optimize compression and generation. Rather than a fixed codec, CoD serves as a foundational model for downstream diffusion-based codecs such as DiffC [43], substantially enhancing their performance by replacing Stable Diffusion*

![[assets/figures/papers/paper_list_l847_https_arxiv_org_abs_2511_18706/figures/002_Figure_2.jpg]]
*Figure 2: Framework overview of CoD in pixel and latent spaces. CoD consists of a condition encoder, an entropy bottleneck, a condition decoder and a diffusion model which is decoupled to DiT backbone and DDT head [49]. CoD is trained with rectified flow [33], where*

## 核心模块与公式推导

### 条件编码与瓶颈模块

CoD 将压缩条件从文本替换为端到端可学习的本机图像令牌。整个条件链路包含三个紧密耦合的模块：

**Condition Encoder（条件编码器）** 接收原始图像 $x$，通过残差块和注意力层将其压缩为紧凑的潜在表示，输出分辨率为输入的 1/32。该编码器与扩散解码器联合训练，使得压缩表示能够携带精细的空间和纹理信息，而非依赖离散的文本词汇。

**Entropy Bottleneck（熵瓶颈）** 采用矢量量化（Vector Quantization）将连续表示离散化为极低比特率码流。具体地，使用大小为 $N = 2^4 = 16$ 的码本，每个空间位置分配 4 bits，对应比特率为 $4 / (32 \times 32) = 0.0039$ bpp。这一极低比特率设计使得扩散模型在训练中被迫习得强生成先验，从而在解码端实现高质量的语义重建。

**Condition Decoder（条件解码器）** 从量化令牌 $y$ 恢复条件表示 $c$，输出分辨率为原始图像的 1/16。该条件表示随后被注入扩散模型，作为去噪过程的引导信号。

### 扩散模型架构

扩散模型采用解耦设计，分为 **DiT Backbone** 和 **DDT Head** 两部分。DiT 骨干在 1/16 分辨率上执行去噪，条件 $c$ 与加噪输入在通道维度拼接后送入网络；DDT 头负责将去噪结果上采样至全分辨率。这种解耦设计使得模型能够高效处理高分辨率图像，同时保持生成质量。

### 修正流与统一训练

CoD 采用修正流（Rectified Flow）作为扩散训练框架。修正流定义了从纯噪声到干净图像的确定性线性过渡：

$$x_t = t \cdot x + (1 - t) \cdot \varepsilon$$

其中 $\varepsilon \sim \mathcal{N}(0, I)$ 为标准高斯噪声。对应的常微分方程为 $\mathrm{d} x_t = v_t \mathrm{d} t$，速度场 $v_t = x - \varepsilon$。模型预测速度场 $v_t^{\mathrm{pred}}$，训练损失为预测速度与真实速度之间的均方误差：

$$\mathcal{L}_{\mathrm{RF}} = \mathrm{MSE}(v_t, v_t^{\mathrm{pred}})$$

**统一训练（Unified Training）的核心洞察**在于 $t = 0$ 时的修正流损失等价于一步重建的 MSE 失真：

$$\mathcal{L}_{\mathrm{RF}} \big|_{t=0} = \mathrm{MSE}(v_0, v_0^{\mathrm{pred}}) = \mathrm{MSE}(x, \hat{x}_0)$$

基于此，CoD 在训练中随机选取 $\alpha\%$ 的样本使用 $t \in [0,1]$ 的标准修正流训练，其余 $1-\alpha\%$ 的样本强制在 $t=0$ 训练，从而将失真项无缝融入扩散训练。这一策略消除了仅用修正流损失导致的颜色偏移问题，并赋予模型通过调整采样步数控制失真-感知权衡的能力——一步推理即可获得 3.4 dB 的 PSNR 提升。

### 整体训练目标

最终训练损失由四项加权求和构成：

$$\mathcal{L} = \mathcal{L}_{\mathrm{RF}} + \lambda \cdot \mathcal{L}_{\mathrm{REPA}} + \beta \cdot \mathcal{L}_{\mathrm{C}} + \gamma \cdot \mathcal{L}_{\mathrm{aux}}$$

其中 $\lambda = 0.5$，$\beta = 0.25$，$\gamma = 1.0$。$\mathcal{L}_{\mathrm{REPA}}$ 为表示对齐损失（Representation Alignment），$\mathcal{L}_{\mathrm{C}}$ 为码本承诺损失（Codebook Commitment Loss），$\mathcal{L}_{\mathrm{aux}}$ 为辅助损失。辅助损失在统一后训练阶段可进一步提升 FID 指标，与统一训练结合后达到全局最优性能。

## 实验与分析

### 主要结果

CoD 在两个核心维度上接受了系统评估：像素空间编解码器的率失真性能，以及潜在空间扩散压缩框架中的表现。实验覆盖 Kodak、CLIC2020 等标准测试集，比特率范围从 0.0039 bpp 的极低码率延伸至 4 bpp 的近无损区域。

**像素空间性能。** 在 Kodak 512×512 上，像素空间 CoD 以 VTM（H.266/VVC 参考软件）为锚点取得了 BD-Rate −2.1% 的结果，意味着在同等 PSNR 下节省了约 2.1% 的码率。在 CLIC2020 测试集上，CoD 在所有比特率下均优于 GAN 基感知编解码器 **HiFiC**、**MS-ILLM**、**CDC** 和 **TACO**，在 PSNR、DISTS 和 FID 三个指标上同时领先。尤其在 4 bpp 附近，CoD 的 PSNR 可达约 47 dB，接近无损重建水平。需要指出的是，HiFiC、MS-ILLM、CDC 和 TACO 均针对 LPIPS 进行了显式优化，而 CoD 未做此类优化，因此在 LPIPS 的某些比特率点上可能不占优——但在 PSNR、DISTS、FID 上的一致性优势表明其重建质量更均衡。

**潜在空间性能。** 潜在空间 CoD 在低比特率（<0.02 bpp）下展现出 SOTA 性能（Figure 9）。当替换 Stable Diffusion 作为 DiffC 的基础模型后，CoD 在超低码率（0.0039 bpp）下显著提升重建质量，LPIPS 明显优于基于文本条件的 Stable Diffusion 方案（DiffC、DDCM、PerCo）。但潜在空间 CoD 的 PSNR 上限受限于 SD-VAE 的重建质量（约 26 dB@0.6 bpp），这是所有基于 SD-VAE 的方法共有的约束，而非 CoD 特有缺陷。

**缩放定律。** 在 Kodak 256×256 上，CoD 仅用 49M 参数（0.016 bpp）即显著优于 181M 参数的 GAN 基方法 MS-ILLM（0.021 bpp），表明扩散先验在参数效率上的优势（Figure 4）。

**失真-感知权衡控制。** 统一训练赋予 CoD 通过采样步数控制失真-感知权衡的零样本能力：在 0.0039 bpp 下，从 25 步减少到 1 步推理可提升 3.4 dB PSNR（16.2 dB → 19.6 dB），同时保持可接受的感知质量（Figure 5 左）。

**训练效率。** CoD 的全部训练仅需约 20 A100 GPU 天（464 A100 GPU 小时），约为 Stable Diffusion v1.5 训练成本的 0.3%，且完全基于 ImageNet-21K、OpenImages、SA-1B 等开源数据集（Table 3）。

### 消融实验

**统一训练与辅助损失。** Table 5 系统消融了统一训练（unified training）和辅助损失（auxiliary loss）的贡献。仅使用修正流损失（flow matching）时，PSNR 仅为 9.83 dB；引入统一训练（在 t=0 时强制一步重建监督）后，PSNR 跃升至 15.83 dB，同时 LPIPS 和 FID 均显著改善。辅助损失单独使用可进一步提升 FID，但 PSNR 偏低；将辅助损失与统一训练结合（统一后训练，unified post-training）达到全局最优，在 PSNR、LPIPS、FID 三个指标上实现最佳平衡。对统一后训练中权重因子 ω_α 的敏感性分析（Figure 18）表明，ω_α=3 可获得额外收益，暗示进一步调优该超参数仍有提升空间。

**Prediction 目标的选择。** Table 2 比较了 V-prediction 和 X-prediction 两种扩散预测目标。X-prediction 在基础模型感知指标上明显优于 V-prediction（PSNR +1.08 dB，LPIPS −0.018），但当应用于下游零样本压缩框架 DiffC 时，由于 X-prediction 的似然估计不稳定，重建结果保留了轻微噪声，导致 FID 恶化（Figure 17）。这表明 prediction 目标的选择需要针对下游任务进行适配。

### 失败模式与局限性

1. **LPIPS 指标劣势。** 像素空间 CoD 未针对 LPIPS 进行显式优化，在以 LPIPS 为主要指标的对比中可能不如专门优化该指标的 GAN 方法（HiFiC、MS-ILLM 等）。这是训练目标的选择差异，而非模型能力的固有缺陷。

2. **潜在空间的 PSNR 上限。** 潜在空间 CoD 的 PSNR 和比特率范围受 SD-VAE 重建质量约束（≤~26 dB），无法像像素空间版本那样覆盖宽比特率范围并达到高 PSNR。

3. **X-prediction 的下游不稳定性。** X-prediction 虽在基础模型上表现更好，但在 DiffC 零样本压缩中因似然估计不准确导致噪声残留和 FID 恶化，说明基础模型的 prediction 目标与下游量化压缩框架之间存在兼容性问题。

4. **高分辨率扩展。** CoD 未在 2K 及以上分辨率上进行训练，扩展到更高分辨率需要更大的计算资源。

5. **推理速度。** 多步采样过程无法满足实时编码要求（Table 4 给出了与 Stable Diffusion 的复杂度对比），单步蒸馏虽可提速但仍有优化空间。

![[assets/figures/papers/paper_list_l847_https_arxiv_org_abs_2511_18706/figures/020_Table_4.jpg]]
*Table 4: Complexity comparison with Stable Diffusion. Average speed (ms) is measured for*

### 关键图表结论

- **Figure 8（像素空间编解码器率失真曲线）**：CoD 在 PSNR、DISTS、FID 上全面超越 HiFiC、MS-ILLM、CDC、TACO，验证了扩散先验在像素空间压缩中的优势。
- **Figure 9（潜在空间编解码器率失真曲线）**：潜在空间 CoD 在低比特率下达到 SOTA，证明了图像令牌条件替代文本条件的有效性。
- **Table 5（统一训练消融）**：统一训练是 PSNR 提升的关键驱动力（+6.0 dB），辅助损失进一步改善感知质量，二者结合达到全局最优。
- **Table 2（X-prediction 消融）**：X-prediction 提升基础模型感知性能但损害下游零样本压缩的 FID，揭示了 prediction 目标选择的任务依赖性。
- **Table 6（用户研究与语义评分）**：在约 0.004 bpp 的极低码率下，CoD 在用户偏好和语义相似度上均优于对比方法，验证了其在实际感知场景中的优势。

![[assets/figures/papers/paper_list_l847_https_arxiv_org_abs_2511_18706/figures/008_Figure_8.jpg]]
*Figure 8: Comparison with pixel-space codecs. Note: HiFiC, MS-ILLM, CDC, and TACO are optimized using LPIPS, whereas CoD is not. So pixel-space CoD may not achieve the best LPIPS at certain bitrates, despite outperforming in PSNR, DISTS and FID*

![[assets/figures/papers/paper_list_l847_https_arxiv_org_abs_2511_18706/figures/009_Figure_9.jpg]]
*Figure 9: Comparison with latent-space codecs. Latent-space CoD demonstrates state-of-the-art performance towards low bitrates*

![[assets/figures/papers/paper_list_l847_https_arxiv_org_abs_2511_18706/figures/022_Table_5.jpg]]
*Table 5: Ablation study on unified training and auxiliary loss on Kodak at*

![[assets/figures/papers/paper_list_l847_https_arxiv_org_abs_2511_18706/figures/019_Table_2.jpg]]
*Table 2: Ablation study for X -prediction on Kodak at 512 × 512*

![[assets/figures/papers/paper_list_l847_https_arxiv_org_abs_2511_18706/figures/024_Table_6.jpg]]
*Table 6: Additional evaluation metrics including user study and semantic scores around 0.004 bpp on Kodak*

### 补充图表

![[assets/figures/papers/paper_list_l847_https_arxiv_org_abs_2511_18706/figures/005_Figure_5.jpg]]
*Figure 5: Comparison of CoD and Stable Diffusion on Kodak at 512 × 512 resolution. (left) Pixel-space CoD enables zero-shot distortionperception controlling by adjusting the sampling steps. CoD is at 0.0039 bpp and PerCo is at 0.0036 bpp. (right) Text conditions harms performance of zero-shot algorithm DiffC on Stable Diffusion, while CoD condition boosts LPIPS at low-bitrate. In addition, pixel-space CoD is not limited by the SD-VAE thus demonstrating wider bitrates, higher PSNR and higher potential in perceptual quality*

![[assets/figures/papers/paper_list_l847_https_arxiv_org_abs_2511_18706/figures/004_Figure_4.jpg]]
*Figure 4: Scaling law analysis on Kodak at 256 × 256. All CoD models are at 0.016 bpp while MS-ILLM is at 0.021 bpp*

![[assets/figures/papers/paper_list_l847_https_arxiv_org_abs_2511_18706/figures/006_Figure_6.jpg]]
*Figure 6: Visual comparison between Stable-Diffusion-based codecs and latent-space CoD under ultra-low bitrates*

![[assets/figures/papers/paper_list_l847_https_arxiv_org_abs_2511_18706/figures/018_Figure_17.jpg]]
*Figure 17: Evaluating V-and X -prediction pixel-space CoD using DiffC on Kodak at 512 × 512*

## 方法谱系与知识库定位

### 1. 与现有扩散压缩方法的代际差异

CoD 的核心定位是**面向压缩的扩散基础模型**，而非一个固定的编解码器。这一设计哲学使其与现有扩散压缩方法形成根本性的代际差异。

**文本条件扩散压缩的瓶颈。** 以 Stable Diffusion 为基础模型的零样本压缩方法（如 **DiffC**、**DDCM**）和微调方法（如 **PerCo**）均依赖文本描述作为条件信号。文本条件存在两个结构性缺陷：(1) 离散的文本词汇无法携带精细的空间位置和纹理信息，导致重建中高频细节丢失；(2) 文本编码器（如 BLIP-2）在压缩流程中保持冻结，阻断了编码器与解码器之间的端到端联合优化。实验证据表明，在 Stable Diffusion 上使用文本条件甚至会损害 DiffC 的压缩性能（Figure 5 右），而 CoD 将条件替换为**可学习的本机图像令牌**后，在极低比特率下显著提升了 LPIPS 指标。

**潜在扩散的 PSNR 天花板。** 基于 SD-VAE 的潜在空间编解码器（包括 PerCo、OSCAR 以及 CoD 自身的潜在空间版本）均受制于 VAE 的重建质量上限——PSNR 无法超过约 26 dB（0.6 bpp 时），且比特率范围被限制在 VAE 潜在空间的容量内。CoD 的像素空间版本通过直接在原始像素上建模，突破了这一约束：在 4 bpp 下可达到约 47 dB 的 PSNR，同时保持优于 GAN 基方法的感知质量。

**与 GAN 基感知编解码器的对比。** **HiFiC**、**MS-ILLM**、**CDC** 和 **TACO** 等方法以 LPIPS 为主要优化目标，在感知相似性指标上表现强劲。CoD 未针对 LPIPS 进行显式优化，因此在某些比特率下的 LPIPS 可能不占优，但在 PSNR、DISTS 和 FID 上表现一致更优（Figure 8）。值得注意的是，CoD（49M 参数）在 Kodak 256×256 上的重建质量显著优于 MS-ILLM（181M 参数），展现出更高的参数效率（Figure 4）。

**与单步扩散方法的对比。** **OSCAR** 等单步扩散编解码器追求推理效率，但通常以牺牲感知质量为代价。CoD 的统一训练策略使其天然支持通过采样步数控制失真-感知权衡：在 25 步时达到最佳感知质量，减少至单步推理可获得 3.4 dB 的 PSNR 提升（Figure 5 左），这种零样本的权衡控制能力是现有方法所不具备的。

### 2. 与传统编解码器（VTM）的关系

在像素空间，CoD 与 **VTM**（H.266/VVC 测试模型）的 BD-Rate 为 −2.1%（以 VTM 为锚点），表明两者的 PSNR-码率性能基本相当。然而，CoD 在感知质量上大幅领先：VTM 作为传统混合编码框架，其优化目标为像素级失真最小化，在低比特率下会产生模糊和块效应；CoD 通过扩散生成先验，能在极低比特率（如 0.0039 bpp）下重建出语义合理且纹理丰富的图像。这一结果意味着扩散基础模型有望在保持与传统编码器可比的保真度的同时，提供显著更优的感知体验。

### 3. 适用边界与局限

**分辨率扩展受限。** CoD 当前的训练和评估主要集中在 512×512 分辨率。扩展到 2K/4K 等高分辨率输入需要更大的计算资源和更高效的注意力机制，这是扩散模型在像素空间面临的结构性挑战。

**实时编码不可行。** 与所有扩散编解码器一样，CoD 的多步采样过程无法满足实时编码需求。虽然单步蒸馏可以大幅提速，但感知质量会有所下降，且蒸馏后的模型仍无法达到传统编解码器的编码延迟水平。

**潜在空间的 PSNR 天花板。** 潜在空间 CoD 虽然训练和推理效率更高，但其 PSNR 上限（约 26 dB）和比特率范围受 SD-VAE 的固有限制，无法通过 CoD 自身的改进来突破。

**LPIPS 非优化目标。** 像素空间 CoD 未针对 LPIPS 进行显式优化，在以 LPIPS 为主要评价指标的对比中可能不如专门针对该指标优化的 GAN 方法（如 HiFiC、MS-ILLM）。

**Prediction 目标的下游兼容性。** X-prediction 基础模型在感知指标上优于 V-prediction（PSNR +1.08 dB，LPIPS −0.018），但应用于下游 DiffC 时因似然估计不稳定导致 FID 恶化（Table 2），表明 prediction 类型需要针对下游任务进行适配性选择。

### 4. 开放问题

1. **高分辨率扩展。** 如何将 CoD 的压缩-生成范式扩展到 2K/4K 分辨率而不导致计算成本急剧增加？可能的路径包括分层编码、稀疏注意力或潜在-像素混合架构。

2. **实时扩散编码。** 通过知识蒸馏、一致性模型或更高效的采样策略能否实现真正的实时像素空间扩散编码？单步蒸馏已展示初步可行性，但感知质量差距仍需弥合。

3. **跨模态与跨任务迁移。** CoD 的压缩-生成联合训练范式是否可以直接应用于视频压缩、三维场景压缩或其他模态的压缩任务？这需要验证图像令牌条件机制在时序或多模态数据上的泛化能力。

4. **缩放定律的边界。** 在更大规模的训练数据（目前约 22M 图像，远小于 Stable Diffusion 的数十亿级数据）和更大模型下，CoD 的性能能否继续遵循缩放定律？训练数据质量和多样性的提升可能带来多大增益？

5. **Prediction 目标的统一设计。** 如何设计更好的 prediction 目标（如 V-prediction 与 X-prediction 的混合策略），以同时优化基础模型的感知性能和下游量化压缩框架的似然估计稳定性？

## 原文 PDF

![[paperPDFs/CVPR_2026/CoD_A_Diffusion_Foundation_Model_for_Image_Compression.pdf]]
