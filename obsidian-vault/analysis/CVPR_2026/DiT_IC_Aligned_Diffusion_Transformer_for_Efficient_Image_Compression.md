---
title: "DiT-IC: Aligned Diffusion Transformer for Efficient Image Compression"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DiT_IC_Aligned_Diffusion_Transformer_for_Efficient_Image_Compression.pdf
project_link: "https://njuvision.github.io/DiT-IC/"
code_link: null
aliases:
- DiT-IC
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将扩散操作下移至32×下采样的深层潜在空间，并采用扩散Transformer（DiT）替代U‑Net，结合三个对齐机制（方差引导重建流、自蒸馏对齐、潜在条件引导）将多步扩散蒸馏为单步重建。
primary_logic: 预训练的文本到图像扩散Transformer经过适当的对齐训练后，可在深层压缩潜在空间中实现高效的单步重建，同时保持出色的感知质量。
claims:
- DiT‑IC在Kodak、CLIC、DIV2K三个数据集上达到BD‑rate LPIPS −83.65%、DISTS −87.88%，延迟仅0.15秒（1024×1024）。
- 用户研究中DiT‑IC获得56.8%的最高偏好分数，远超第二名的27.5%（StableCodec）。
- 在16GB笔记本GPU上可重建2048×2048图像，采用1024×1024分块解码时峰值内存低于7GB。
- 消融实验显示方差引导重建流、自蒸馏对齐和潜在条件引导均对重建质量和效率有显著贡献。
---

# DiT-IC: Aligned Diffusion Transformer for Efficient Image Compression

> [!tip] 核心洞察
> 预训练的文本到图像扩散Transformer经过适当的对齐训练后，可在深层压缩潜在空间中实现高效的单步重建，同时保持出色的感知质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | DiT-IC：面向高效图像压缩的对齐扩散Transformer |
| 英文题名 | DiT-IC: Aligned Diffusion Transformer for Efficient Image Compression |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.13162) · [Project](https://njuvision.github.io/DiT-IC/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | DiT-IC |
| Dataset | Kodak + CLIC2020 + DIV2K（平均）, 1024×1024 解码延迟, 2048×2048 扩散部分延迟 |

> [!tip] 效果简介
> - Kodak + CLIC2020 + DIV2K（平均） 上，BD‑rate LPIPS (↓) −83.65% vs −79.19% (StableCodec) (优于 4.46个百分点)；BD‑rate DISTS (↓) −87.88% vs −83.95% (StableCodec) (优于 3.93个百分点)。
> - 1024×1024 解码延迟 上，Latency (s) 0.15 s vs 0.34 s (StableCodec) (降低 55.9%)。
> - 2048×2048 扩散部分延迟 上，Latency (s) 0.12 s vs 0.8 s (StableCodec) (降低 85%)。

## 概述

图像压缩领域长期面临一个核心矛盾：基于均方误差（MSE）优化的传统编码器（如 **ELIC**，He et al., CVPR 2022）能够实现高保真度，但重建结果缺乏高频细节和感知真实感；而扩散模型虽能生成丰富纹理，却因多步迭代去噪导致计算开销巨大，难以满足实际应用的低延迟需求。现有扩散图像编码器普遍采用 U‑Net 架构，在 8× 下采样的浅层潜在空间中执行多步扩散，这从根本上限制了效率提升的空间。

**DiT‑IC** 的核心洞察在于：预训练的文本到图像扩散 Transformer（DiT）经过适当的对齐训练后，可以在 32× 下采样的深层压缩潜在空间中实现高效的单步重建，同时保持出色的感知质量。这一洞察转化为三个关键的技术突破：

1. **方差引导重建流**：将编码器预测的潜在方差映射为逐像素伪时间步，实现空间自适应的单步去噪，将多步扩散折叠为一次线性变换。
2. **自蒸馏对齐**：以冻结编码器的输出作为内部参考，通过余弦相似度损失将多步扩散过程蒸馏为单步前向传播。
3. **潜在条件引导**：将压缩潜在特征投影到文本嵌入空间，替代文本条件进行语义引导，实现推理阶段完全无文本依赖。

在方法谱系上，DiT‑IC 属于**单步扩散图像压缩**范式，与 **StableCodec**（Zhang et al., ICCV 2025）、**OSCAR**（Guo et al., NeurIPS 2025）、**ResULIC**（Ke et al., ICML 2025）等方法同处一个技术路线，但通过将扩散操作下移至深层潜在空间并引入扩散 Transformer，从根本上改变了效率与质量的权衡边界。

实验结果表明，DiT‑IC 在 Kodak、CLIC2020 和 DIV2K 三个标准数据集上取得 BD‑rate LPIPS −83.65%、DISTS −87.88%，较当前最优方法 StableCodec 分别提升 4.46 和 3.93 个百分点。在 1024×1024 分辨率下，解码延迟仅 0.15 秒，比 StableCodec 降低 55.9%；在 2048×2048 分辨率下，扩散部分延迟从 0.8 秒降至 0.12 秒，降幅达 85%。用户研究中，DiT‑IC 获得 56.8% 的最高偏好分数，远超第二名的 27.5%。此外，该方法在 16GB 笔记本 GPU 上可重建 2048×2048 图像，分块解码时峰值内存低于 7GB，展现出优异的实际部署潜力。

值得注意的是，DiT‑IC 在极低码率（<0.01 bpp）下可能面临潜在条件语义信息不足的问题，且训练数据规模有限（约 150K 图像），在长尾内容覆盖上仍需进一步验证。对抗训练在提升感知真实感的同时也引入了失真–感知权衡，以轻微牺牲 PSNR 为代价。这些局限性为后续研究指明了方向。

## 背景与动机

图像压缩是数字媒体传输与存储的基础技术。传统基于均方误差（MSE）优化的编码器（如 **ELIC**，He et al., CVPR 2022）在高压缩率下虽能保持信号保真度，却不可避免地丢失高频纹理细节，导致重建图像出现模糊和过度平滑。扩散模型的出现为感知导向的图像压缩开辟了新路径：通过在解码端引入生成式先验，扩散编码器能够合成逼真的纹理，显著提升视觉质量。

然而，现有扩散图像压缩方法面临一个核心瓶颈：**它们几乎全部基于 U‑Net 架构，迫使扩散过程在较浅的潜在空间（通常仅 8× 下采样）中运行**。U‑Net 的层级下采样设计使得潜在特征图的空间分辨率仍然较高，导致去噪网络的计算量和内存消耗巨大。这带来了两个直接后果：

1. **推理效率低下**：多步扩散采样（4~50 步）叠加高分辨率特征图，使得解码延迟居高不下。例如 **StableCodec**（Zhang et al., ICCV 2025）在 1024×1024 分辨率下的解码延迟为 0.34 秒，而扩展到 2048×2048 时扩散部分延迟高达 0.8 秒。
2. **可扩展性受限**：高内存占用使得现有方法难以在消费级 GPU 上处理超高分辨率图像，限制了实际部署场景。

更深层的矛盾在于：**压缩编码天然适合在深层潜在空间（如 32× 下采样）中进行，因为更紧凑的表示能大幅降低存储和计算开销；但 U‑Net 架构却天然不适合在如此低分辨率的特征图上运行扩散过程**。这一架构性错配构成了“效率-质量”权衡的关键堵点。

与此同时，扩散 Transformer（DiT）在文本到图像生成领域展现出强大的可扩展性和表达能力。与 U‑Net 不同，DiT 在整个去噪过程中保持恒定的空间分辨率，使其天然兼容深层压缩潜在输入。然而，将预训练的文本条件 DiT 直接用于图像压缩面临三重挑战：

- **多步到单步的蒸馏**：生成任务依赖迭代去噪，而压缩解码需要单步重建以匹配实时性要求；
- **文本条件到潜在条件的转换**：压缩解码时无法提供文本提示，必须从压缩表示本身提取引导信号；
- **预训练先验的保持与适配**：全量微调成本高昂且易破坏预训练知识，需要更轻量的适配策略。

本文提出 **DiT‑IC**，核心动机是：**将扩散操作下移至 32× 下采样的深层潜在空间，采用 DiT 替代 U‑Net，并通过三个对齐机制将多步扩散蒸馏为单步重建**。这一设计从根本上解耦了扩散架构与潜在空间深度之间的绑定，使得模型既能享受深层压缩的效率优势，又能保留扩散模型的生成能力。

## 核心创新

DiT-IC 的核心创新在于将扩散图像压缩从传统的 U-Net 架构彻底迁移至**深层潜在空间中的扩散 Transformer（DiT）**，并通过三个关键对齐机制将多步扩散过程蒸馏为高效的单步重建。这一设计同时解决了现有扩散压缩方法在计算效率、内存开销和重建质量三个维度上的瓶颈。

### 瓶颈洞察：U-Net 的架构性限制

现有扩散图像编码器（如 **StableCodec**（Zhang et al., ICCV 2025）、**OSCAR**（Guo et al., NeurIPS 2025）等）普遍基于 U-Net 架构。U-Net 的层级下采样特性迫使扩散过程在较浅的潜在空间（通常仅 8× 下采样）中运行，导致两个根本性问题（Figure 2）：

1. **计算与内存开销巨大**：浅层潜在空间的特征图分辨率较高，多步去噪过程需反复处理大量 token，严重制约解码速度和可扩展性。
2. **无法利用深层潜在空间的高效性**：深层潜在空间（如 32× 下采样）具有更紧凑的表示，但 U-Net 的渐进式分辨率变化与之天然不兼容。

### 关键变更槽位（Changed Slots）

DiT-IC 相对于现有扩散压缩方法的系统性创新可归纳为以下五个关键维度：

| 变更维度 | 现有方法（Baseline） | DiT-IC 方案 | 核心收益 |
|---------|-------------------|------------|---------|
| **扩散网络架构** | U-Net（如 StableCodec） | Diffusion Transformer（基于 SANA） | 支持深层潜在空间，恒定分辨率处理 |
| **潜在空间下采样率** | 8×（典型 U-Net 扩散） | 32× | 大幅降低计算量，提升效率 |
| **推理步数** | 多步（4~50 步） | 单步（1 步） | 解码延迟降低 55.9%~85% |
| **条件类型** | 文本提示（text prompt） | 潜在条件（latent-conditioned projection） | 推理时无需文本输入，语义一致性更强 |
| **训练策略** | 全量微调或部分微调 | LoRA 适配 + 两阶段隐式码率剪枝 | 保护预训练先验，稳定训练，参数高效 |

### 三大对齐机制：从多步扩散到单步重建

DiT-IC 的核心技术贡献在于设计了三个互补的对齐机制，将预训练的文本到图像 DiT 改造为高效的压缩重建模型（Figure 3）：

**1. 方差引导重建流（Variance-Guided Reconstruction Flow）**

传统扩散从纯高斯噪声出发，而压缩重建的起点是包含结构化噪声的量化潜在表示 $\tilde{\mathbf{y}}$。DiT-IC 利用编码器预测的方差 $\pmb{\sigma}$ 作为逐像素的不确定性估计，通过单调映射函数将其转化为伪时间步场 $t = \mathcal{F}(\mathrm{proj}_\theta(\pmb{\sigma})) \in \mathbb{R}^{H \times W}$（Eq. 2）。这使得单步重建 $\hat{\mathbf{y}} = \tilde{\mathbf{y}} - \mathbf{v}_\theta(\tilde{\mathbf{y}}, t)$（Eq. 3）能够自适应地调节每个空间位置的去噪强度——高方差区域施加更强的重建，低方差区域保持编码保真度（Figure 4）。消融实验证实，去除该机制会导致细节恢复能力显著下降（Figure 5）。

**2. 自蒸馏对齐（Self-Distillation Alignment）**

单步重建的潜在表示 $\hat{\mathbf{y}}$ 需要与冻结编码器输出的原始潜在 $\mathbf{y}_0$ 保持一致。DiT-IC 提出自蒸馏对齐策略，通过最大化两者之间的余弦相似度来约束重建过程：$\mathcal{L}_{\mathrm{distil}} = \mathbb{E}_{x\sim p_{\mathrm{data}}} \left[ 1 - m - \frac{\langle \hat{\mathbf{y}}, \mathbf{y}_0 \rangle}{|\hat{\mathbf{y}}|_2 |\mathbf{y}_0|_2} \right]$（Eq. 4），其中 $m$ 为边际参数。该机制以编码器自身作为内部参考，无需外部监督信号，稳定了单步蒸馏训练（Figure 6）。消融实验表明，去除自蒸馏对齐后模型难以收敛到最优（Figure 7）。

**3. 潜在条件引导（Latent-Conditioned Guidance）**

预训练 DiT 依赖文本嵌入作为条件输入，但压缩场景下文本标注不可得。DiT-IC 引入潜在条件投影器 $\mathrm{Proj}_\psi$，将重建潜在特征映射到文本嵌入空间：$c_{\mathrm{lat}} = \mathrm{Proj}_\psi(\hat{y})$（Eq. 5），并通过 CLIP 风格的对比共对齐损失 $\mathcal{L}_{\mathrm{cond}}$（Eq. 6）使其与对应文本嵌入对齐。训练后，推理阶段完全使用潜在条件替代文本条件，实现文本无关的语义引导（Figure 8）。消融实验显示，该机制显著提升了语义一致性和感知质量（Figure 9）。

### 训练策略创新：LoRA 适配与两阶段码率剪枝

为高效适配大规模预训练 DiT（如 SANA），DiT-IC 采用 **LoRA** 低秩适配而非全量微调，在扩散 Transformer 和 VAE 解码器中分别插入秩为 64 和 32 的适配器。消融实验表明，该配置在适应能力与训练稳定性之间达到最优平衡，全量微调反而导致性能略微下降（Table 2）。

训练采用**两阶段隐式码率剪枝（IBP）**策略：第一阶段以较小的码率惩罚系数 $\lambda_{\mathrm{base}}$ 宽松约束率失真（Eq. 7），保护特征丰富度；第二阶段加大码率惩罚并引入对抗损失 $\mathcal{L}_{\mathrm{adv}}$（Eq. 8），增强感知质量。失真损失联合 MSE、LPIPS 和 DISTS 三项指标（Eq. 10），对齐损失由自蒸馏对齐和条件对比对齐加权组成（Eq. 11）。

## 整体框架

DiT‑IC 的整体流程围绕“深层潜在空间中的单步扩散重建”这一核心思想展开，其 pipeline 可划分为编码压缩、熵建模、条件化单步去噪、解码重建四个阶段，如 Figure 3 所示。

![[assets/figures/papers/paper_list_l859_https_arxiv_org_abs_2603_13162/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the proposed DiT-IC framework. Following StableCodec [64], we adopt ELIC [16] as our auxiliary encoder*

### 编码压缩阶段

输入图像首先经过冻结的 **SANA‑VAE 编码器** 映射到 32× 下采样的深层潜在空间，同时输出均值 μ 与方差 σ。均值 μ 作为压缩潜在表示送入后续熵编码，方差 σ 则被保留为不确定性估计，用于指导后续的自适应重建强度。辅助编码器采用 **ELIC** (He et al., CVPR 2022) 架构，负责生成超先验信息以辅助熵模型。

### 熵建模与量化

潜在表示经过量化后，由 **Hyperprior + 自回归上下文模型** 估计其概率分布，从而计算编码比特数。与 StableCodec 不同，DiT‑IC 将原上下文模型中的重型组件替换为轻量级 **DepthConvBlock**，在保持建模能力的同时降低计算开销 (Figure 12)。量化后的潜在表示 $\tilde{\mathbf{y}}$ 作为扩散重建的起点。

### 方差引导的单步去噪

这是 DiT‑IC 区别于现有扩散编码器的关键环节。传统扩散方法从高斯噪声出发进行多步迭代去噪，而 DiT‑IC 的起点是已包含结构化压缩信息的量化潜在 $\tilde{\mathbf{y}}$。系统将编码器预测的方差 σ 通过投影网络映射为逐像素的伪时间步 $t = \mathcal{F}(\mathrm{proj}_\theta(\sigma)) \in \mathbb{R}^{H \times W}$，实现空间自适应的去噪强度控制 (Figure 4)。随后，**扩散 Transformer (DiT)** 在 32× 潜在空间中执行单步去噪：

$$\hat{\mathbf{y}} = \tilde{\mathbf{y}} - \mathbf{v}_\theta(\tilde{\mathbf{y}}, t)$$

这一操作将多步概率流 ODE 折叠为一次线性变换，从根本上消除了迭代去噪的延迟瓶颈。

### 条件注入机制

DiT 的条件输入由两部分构成：**潜在条件引导投影器** 将去噪后的潜在特征 $\hat{y}$ 投影到文本嵌入空间，生成 $c_{\mathrm{lat}} = \mathrm{Proj}_\psi(\hat{y})$，并通过对比共对齐损失与预训练的文本嵌入对齐 (Figure 8)。这一设计使得模型在推理时完全摆脱对文本提示的依赖，实现文本无关的条件化重建。同时，伪时间步 $t$ 作为逐像素的条件信号注入 DiT 的每一层，指导局部去噪强度。

### 解码重建

去噪后的潜在表示 $\hat{\mathbf{y}}$ 送入 **SANA‑VAE 解码器** 重建为最终图像。解码器通过 LoRA 适配器进行部分微调，以在保持预训练先验的同时适应压缩重建的特定需求。整个 pipeline 采用两阶段隐式码率剪枝策略训练：第一阶段以宽松的码率约束保护特征丰富度，第二阶段加大码率惩罚并引入对抗损失以增强感知质量。

### 与 U‑Net 路线的架构差异

Figure 2 对比了 DiT‑IC 与传统 U‑Net 扩散编码器的根本区别：U‑Net 依赖层级下采样-上采样结构，迫使扩散过程在较浅的潜在空间（通常 8× 下采样）中运行，导致计算量和内存消耗巨大；而 DiT 在整个去噪过程中保持恒定的空间分辨率，天然适配 32× 下采样的深层压缩潜在输入，显著降低了扩散阶段的计算复杂度。

![[assets/figures/papers/paper_list_l859_https_arxiv_org_abs_2603_13162/figures/002_Figure_2.jpg]]
*Figure 2: Architectural comparison. The left panel illustrates the overall diffusion-based image compression framework. U-Netbased diffusers perform multi-stage downsampling, while DiTs maintain a constant spatial resolution throughout the denoising process, making them naturally compatible with deeply compressed latent inputs*

## 核心模块与公式推导

### 3.1 概率流ODE与方差引导重建流

DiT-IC将扩散过程下移至32×下采样的深层潜在空间，并基于连续概率流ODE构建重建流。基础模型采用如下形式：

$$
\frac{d\mathbf{y}_t}{dt} = \mathbf{v}_\theta(\mathbf{y}_t, t), \quad \mathbf{y}_T \sim \mathcal{N}(0, I)
$$

其中 $\mathbf{v}_\theta$ 为学习到的向量场，将高斯噪声 $\mathbf{y}_T$ 逐步迁至数据分布。与传统扩散从纯噪声出发不同，压缩重建的起点是包含结构化噪声的量化潜在表示 $\tilde{\mathbf{y}}$。编码器同时输出均值 $\mu$ 和方差 $\sigma$，后者度量了逐像素的量化不确定性。

**方差引导伪时间步映射**将这一不确定性转化为空间自适应的去噪强度：

$$
t = \mathcal{F}(\mathrm{proj}_\theta(\pmb{\sigma})) \in \mathbb{R}^{H \times W}
$$

其中 $\mathrm{proj}_\theta$ 为可学习的投影层（含sigmoid激活），$\mathcal{F}$ 为单调映射函数，将投影后的方差值映射为伪时间步 $t$。高方差区域对应较大 $t$（更强去噪），低方差区域对应较小 $t$（更弱去噪），实现空间自适应的重建控制。

**单步重建**将多步去噪折叠为一次线性变换：

$$
\hat{\mathbf{y}} = \tilde{\mathbf{y}} - \mathbf{v}_\theta(\tilde{\mathbf{y}}, t)
$$

通过自适应时间步字段 $t$，DiT-IC在单次前向传播中完成重建，避免了迭代采样的计算开销。

### 3.2 自蒸馏对齐

为将多步扩散知识蒸馏为单步重建，DiT-IC提出**自蒸馏余弦对齐损失**，以冻结编码器的输出 $\mathbf{y}_0$ 作为内部监督信号：

$$
\mathcal{L}_{\mathrm{distil}} = \mathbb{E}_{{x}\sim p_{\mathrm{data}}} \left[ 1 - m - \frac{\langle \hat{\mathbf{y}}, \mathbf{y}_0 \rangle}{|\hat{\mathbf{y}}|_2 |\mathbf{y}_0|_2} \right]
$$

其中 $\hat{\mathbf{y}}$ 为去噪后的潜在表示，$\mathbf{y}_0$ 为冻结编码器的原始输出，$m$ 为边际超参数（设为0.1）。该损失通过最大化余弦相似度，使单步重建的潜在表示与多步扩散的潜在表示在方向上保持一致，同时联合优化扩散Transformer和解码器。消融实验（Figure 7）证实，去除该对齐后模型难以达到最优重建一致性。

### 3.3 潜在条件引导

预训练DiT依赖文本嵌入 $c_{\text{text}}$ 作为条件，但压缩场景下文本不可得。DiT-IC提出**潜在条件投影**，将压缩潜在特征映射到文本嵌入空间：

$$
c_{\mathrm{lat}} = {\mathrm{Proj}}_\psi(\hat{y})
$$

其中 ${\mathrm{Proj}}_\psi$ 为可学习的投影网络。为保证语义一致性，引入**对比共对齐损失**（CLIP风格）：

$$
\mathcal{L}_{\mathrm{cond}} = - \mathbb{E}_{(x_i, t_i)} \left[ \log \frac{\exp( c_{\mathrm{lat},i}, c_{\mathrm{text},i} / \tau)}{\sum_j \exp( c_{\mathrm{lat},i}, c_{\mathrm{text},j} / \tau)} \right]
$$

该损失使投影潜在嵌入与对应文本嵌入在对比空间中拉近，与其他文本嵌入推远，确保潜在条件携带充分的语义信息。训练时使用VLM生成的图像描述作为文本监督（Figure 13），推理时完全丢弃文本分支，仅使用潜在条件引导。消融实验（Figure 9）表明，潜在条件引导在语义一致性和感知质量上均优于纯文本条件。

### 3.4 两阶段隐式码率剪枝

DiT-IC采用两阶段训练策略，通过逐步收紧码率约束实现宽码率范围的单一模型覆盖。

**第一阶段**（宽松约束，保护特征丰富度）：

$$
\mathrm{Stage\ 1: min}\ \lambda_{\mathrm{base}} \mathcal{R} + \mathcal{D} + \mathcal{L}_{\mathrm{align}}
$$

**第二阶段**（加大码率惩罚，引入对抗损失）：

$$
\mathrm{Stage\ 2: min}\ \lambda_{\mathrm{target}} \mathcal{R} + \mathcal{D} + \mathcal{L}_{\mathrm{align}} + \lambda_{\mathrm{adv}} \mathcal{L}_{\mathrm{adv}}
$$

其中各损失项定义为：

**率损失**（由主潜在和超先验的负对数似然构成）：

$$
\mathcal{R}(\hat{y}, \hat{z}) = -\log_2 p_{\hat{\mathbf{y}}}(\hat{\mathbf{y}}\mid\hat{\mathbf{z}}) - \log_2 p_{\hat{\mathbf{z}}}(\hat{\mathbf{z}})
$$

**失真损失**（联合MSE、LPIPS和DISTS）：

$$
\mathcal{D}(x, \hat{x}) = \lambda_1 MSE + \lambda_2 LPIPS + \lambda_3 DISTS
$$

**总对齐损失**：

$$
\mathcal{L}_{\mathrm{align}}(c, \hat{y}_0) = \lambda_4 \mathcal{L}_{\mathrm{distil}} + \lambda_5 \mathcal{L}_{\mathrm{cond}}
$$

消融实验（Table 2）显示：去除 $\mathcal{L}_{\mathrm{adv}}$ 导致PSNR BD-rate下降37.10%；DISTS项的引入在低码率下显著提升了与人类感知的相关性。LoRA适配采用VAE秩32、DiT秩64的配置，在适应能力与训练稳定性间达到最优平衡。

### 补充图表

![[assets/figures/papers/paper_list_l859_https_arxiv_org_abs_2603_13162/figures/005_Figure_4.jpg]]
*Figure 4: Variance-Guided Flow Matching. Unlike standard diffusion that starts from Gaussian noise, compression reconstruction begins from a quantized latent*

![[assets/figures/papers/paper_list_l859_https_arxiv_org_abs_2603_13162/figures/006_Figure_6.jpg]]
*Figure 6: Self-Distillation Alignment. DiT-IC distills the multistep diffusion process into a single forward pass by aligning its denoised latent with the frozen encoder representation, while jointly optimizing the diffusion transformer and decoder*

![[assets/figures/papers/paper_list_l859_https_arxiv_org_abs_2603_13162/figures/007_Figure_8.jpg]]
*Figure 8: Latent-Conditioned Guidance. We replace text-based guidance in DiT with a latent-conditioned projection derived from the compressed representation by aligning projected latent and text embeddings, enabling text-free conditioning at inference*

## 实验与分析

### 主结果：BD‑rate与延迟的全面领先

DiT‑IC在三个标准基准（Kodak、CLIC2020、DIV2K）上以PerCo为零点参考计算BD‑rate，取得平均LPIPS −83.65%、DISTS −87.88%的成绩，分别优于当前最优单步扩散方法**StableCodec**（Zhang et al., ICCV 2025）4.46和3.93个百分点（Table 1）。在解码延迟方面，DiT‑IC处理1024×1024图像仅需0.15秒（单张A100 GPU），比StableCodec的0.34秒降低55.9%。当分辨率提升至2048×2048时，扩散部分延迟从StableCodec的0.8秒降至0.12秒，降幅达85%（Table 3），充分体现了深层潜在空间（32×下采样）与DiT架构结合带来的效率增益。

![[assets/figures/papers/paper_list_l859_https_arxiv_org_abs_2603_13162/figures/012_Table_1.jpg]]
*Table 1: Comprehensive comparison with state-of-the-art methods in terms of BD-rate (↓) [4]. “Diff. Reso.” and “Code Reso.” denote the latent resolutions used in the diffusion and coding stages, respectively, where f indicates the spatial downsampling factor relative to the pixel domain, and d denotes the number of channels. Latency is measured as the per-image decoding time (for 1024 × 1024 resolution) on a single A100 GPU; ♣ marks FP16 inference and ♠ marks FP32. “DiT-IC (baseline)” represents the variant without the proposed alignment strategies. The best results are highlighted in red, and the second-best in blue*

![[assets/figures/papers/paper_list_l859_https_arxiv_org_abs_2603_13162/figures/014_Table_3.jpg]]
*Table 3: Runtime latency (s) comparison in FP32 precision*

感知质量方面，在相近码率（约0.03–0.04 bpp）下，DiT‑IC在FID、NIQE、CLIPIQA、MUSIQ等多项指标上全面超越StableCodec（Table 4）。用户研究进一步验证了这一优势：DiT‑IC获得56.8%的最高偏好分数，而StableCodec仅27.5%，其余方法（ResULIC、OSCAR、PerCo）均低于10%。

### 消融实验：三对齐机制与训练策略的因果验证

消融实验系统性地验证了各个设计选择的贡献（Table 2, Figures 5/7/9）。

![[assets/figures/papers/paper_list_l859_https_arxiv_org_abs_2603_13162/figures/013_Table_2.jpg]]
*Table 2: Ablation study results measured by BD-rate ↓ [4]*

**方差引导重建流**（Figure 5）的移除导致模型退化为均匀去噪强度，细节恢复能力显著下降——纹理区域出现模糊或伪影，表明逐像素自适应伪时间步映射是单步重建质量的关键保障。

**自蒸馏对齐**（Figure 7）的消融使训练难以收敛至最优，重建潜在与编码器表示之间的余弦相似度波动增大，最终感知指标恶化。该机制通过内部参考信号替代外部监督，稳定了多步扩散到单步的蒸馏过程。

**潜在条件引导**（Figure 9）替换文本条件后，语义一致性和感知质量均有提升。去除该模块而直接使用文本嵌入时，模型在文本无关推理场景下出现语义漂移，尤其在包含文字、数字的场景中错误率增加（参见Figure 10中StableCodec和OSCAR的窗户格数、数字错误）。

**损失函数与训练策略**（Table 2）的消融揭示了几个关键因果链：
- 移除对抗损失 $\mathcal{L}_{adv}$ 导致PSNR BD‑rate下降37.10%，说明对抗训练虽以轻微客观指标为代价，但对感知真实感至关重要。
- 从零训练DiT（无预训练权重）使LPIPS恶化22.00%、DISTS恶化32.45%，验证了预训练文本到图像DiT作为先验的不可替代性。
- LoRA秩的选择存在最优平衡点：VAE秩32/DiT秩64表现最佳，全量微调反而略降性能，表明轻量适配在有限数据下具有正则化效果。

### 失败模式与局限

尽管整体性能优异，DiT‑IC在以下场景存在退化风险：

1. **极低码率（<0.01 bpp）**：潜在条件携带的语义信息不足，重建可能出现内容缺失或语义错误。论文指出可借助文本先验增强，但当前框架未集成该能力。
2. **长尾内容与特定领域**：训练数据约150K图像，覆盖范围有限，在罕见场景下泛化性待验证。
3. **失真‑感知权衡**：对抗训练提升感知真实感的同时，PSNR等客观指标有所牺牲（Table 2中 $\mathcal{L}_{adv}$ 消融），在需要精确保真度的应用场景下需谨慎使用。
4. **编码器冻结的刚性**：自蒸馏对齐依赖冻结的编码器表示，未来若需更新编码器，整个对齐流程需重新训练。

### 关键图表结论速览

- **Figure 10**：可视化对比直观展示了DiT‑IC在语义保真度与感知质量之间的优势平衡——ELIC丢失高频细节，StableCodec和OSCAR产生语义不一致（错误数字、窗户格数），DiT‑IC则保持内容准确且纹理自然。
- **Figure 11/14**：率失真感知曲线显示DiT‑IC在LPIPS和DISTS两个感知轴上均形成对StableCodec、OSCAR、PerCo等方法的全面包络，尤其在低码率段优势扩大。
- **Table 3**：延迟分解表明DiT‑IC的效率优势随分辨率提升而放大，1024²扩散仅0.055秒（StableCodec 0.11秒），2048²降至0.12秒（StableCodec 0.8秒），验证了DiT恒定分辨率去噪的计算可扩展性。
- **Figure 15**：FID和语义精度指标上DiT‑IC同样领先，佐证了潜在条件引导对语义一致性的提升效果。

![[assets/figures/papers/paper_list_l859_https_arxiv_org_abs_2603_13162/figures/010_Figure_10.jpg]]
*Figure 10: Visualization comparison. MSE-optimized ELIC [16] suffers from high-frequency detail loss, whereas diffusion-based codecs such as StableCodec [64] and OSCAR [15] produce inconsistent semantic content, e.g., incorrect numbers or window panes. In contrast, DiT-IC achieves a more favorable balance between perceptual quality and semantic consistency*

> **公平性备注**：BD‑rate以PerCo（多步扩散、性能较低）为零点参考，可能放大相对改善幅度；延迟测量均在单张A100上执行，不同实现的并行优化程度可能影响对比公平性；用户研究的参与者数量和筛选标准未明确，偏好分数的统计显著性有待独立验证。

### 补充图表

![[assets/figures/papers/paper_list_l859_https_arxiv_org_abs_2603_13162/figures/004_Figure_5.jpg]]
*Figure 5: Ablation study of variance-guided reconstruction flow*

![[assets/figures/papers/paper_list_l859_https_arxiv_org_abs_2603_13162/figures/008_Figure_7.jpg]]
*Figure 7: Ablation of self-distillation alignment*

![[assets/figures/papers/paper_list_l859_https_arxiv_org_abs_2603_13162/figures/009_Figure_9.jpg]]
*Figure 9: Ablation of latent-conditioned guidance*

## 方法谱系与知识库定位

### 1. 技术路线定位：从VAE编码到扩散解码的范式迁移

DiT-IC 处于**神经图像压缩**与**扩散生成模型**的交叉地带。传统神经图像压缩以变分自编码器（VAE）范式为主导，代表性工作如 **ELIC**（He et al., CVPR 2022）通过精心设计的熵模型和变换网络在率失真性能上取得突破，但其MSE优化的重建往往丢失高频纹理细节。近年来，扩散模型被引入图像压缩以提升感知质量，形成了两条主要技术路线：

- **扩散后处理路线**：以 **CorrDiff**（Ma et al., ICML 2024）为代表，在传统编解码器之后附加扩散模型作为后处理增强器，不改变编码流程本身。
- **扩散原生编码路线**：将扩散模型直接嵌入压缩管线，如 **PerCo**（Careil et al., ICLR 2024）、**DiffEIC**（Li et al., TCSVT 2024）采用多步扩散进行重建，以及 **StableCodec**（Zhang et al., ICCV 2025）、**OSCAR**（Guo et al., NeurIPS 2025）、**ResULIC**（Ke et al., ICML 2025）探索单步扩散编码。

DiT-IC 继承自 StableCodec 的“VAE编码 + 扩散解码”框架，但对其核心瓶颈进行了根本性改造：**将扩散操作从U-Net的浅层潜在空间（8×下采样）迁移至Diffusion Transformer的深层潜在空间（32×下采样）**，并通过三个对齐机制将多步扩散蒸馏为单步重建。这一迁移并非简单的架构替换，而是触及了现有扩散压缩方法的结构性限制——U-Net的层级下采样迫使扩散在较浅的潜在空间中运行，导致计算量和内存消耗巨大，且无法利用深层潜在空间的高效性。

### 2. 与关键基线的方法论差异

#### 2.1 与 StableCodec 的核心差异

StableCodec 是DiT-IC最直接的对比对象，两者共享“ELIC编码器 + 扩散解码器”的整体框架。DiT-IC 在以下四个维度实现了结构性改进：

| 维度 | StableCodec | DiT-IC |
|------|-------------|--------|
| 扩散架构 | U-Net | Diffusion Transformer（基于SANA） |
| 潜在空间下采样率 | 8× | 32× |
| 推理步数 | 单步（U-Net内） | 单步（DiT内，但潜在空间更深） |
| 条件机制 | 文本提示 | 潜在条件引导（文本无关） |
| 训练策略 | 全量微调 | LoRA适配 + 两阶段隐式码率剪枝 |

**架构迁移的因果机制**：U-Net的层级下采样结构天然适合浅层潜在空间，但将其应用于32×下采样的深层潜在空间时，需要额外的上采样层来匹配扩散分辨率，引入冗余计算。DiT（Diffusion Transformer）在整个去噪过程中保持恒定空间分辨率，与深层压缩潜在输入天然兼容——这是DiT-IC能够将扩散下移至32×潜在空间并显著降低延迟的结构性原因。

**条件机制的创新**：StableCodec等现有方法依赖文本提示作为扩散条件，需要额外的语义标注或VLM生成流程。DiT-IC提出**潜在条件引导**（Latent-Conditioned Guidance），将压缩潜在特征投影到文本嵌入空间，通过对比共对齐损失（Eq. 6）与文本嵌入对齐，实现推理时的文本无关条件注入。这一设计不仅消除了对文本标注的依赖，更在语义一致性和感知质量上取得提升（Figure 9消融实验证实）。

#### 2.2 与其他扩散压缩方法的边界

- **PerCo / DiffEIC（多步扩散）**：这些方法在像素空间或浅层潜在空间执行多步（4~50步）去噪，计算开销大。DiT-IC通过方差引导重建流将去噪折叠为单步，同时利用32×深层潜在空间降低每步的计算量，在效率上形成代际差距（Table 3：2048²分辨率下扩散延迟仅0.12s，相比StableCodec的0.8s降低85%）。

- **OSCAR（可变码率单步扩散）**：OSCAR聚焦于可变码率控制，但仍在U-Net框架内运行。DiT-IC的DiT架构和深层潜在空间策略在效率上具有独立优势，且两阶段隐式码率剪枝策略同样支持宽码率范围训练。

- **CorrDiff（后处理增强）**：后处理路线不改变编码器行为，本质上是对已有压缩结果的“美化”。DiT-IC的扩散模块直接参与重建，在率失真优化框架内联合训练，理论上能实现更优的码率-感知质量权衡。

#### 2.3 与VAE路线的定位

**ELIC** 和 **GLC**（Qi et al., TCSVT 2025）代表VAE路线的性能上限。DiT-IC在PSNR等保真度指标上可能不及MSE优化的VAE方法（Table 2消融显示引入对抗损失后PSNR BD-rate下降37.10%），但在LPIPS、DISTS等感知指标上实现显著超越（平均BD-rate −83.65% LPIPS、−87.88% DISTS）。这一“失真-感知权衡”是扩散压缩方法的固有特征，DiT-IC通过联合优化MSE、LPIPS、DISTS和对抗损失在两者间寻求平衡。

### 3. 适用边界与局限

#### 3.1 码率适用范围

DiT-IC在两阶段训练中覆盖了较宽码率范围，但其设计假设潜在表示携带足够的语义信息。在**极低码率（<0.01 bpp）**下，32×下采样的潜在空间可能缺乏足够的语义信息支撑高质量重建，论文也指出此时需借助文本先验增强。这一边界在Figure 11的率失真曲线中有所体现——极低码率段的性能差距可能收窄。

#### 3.2 训练数据依赖性

训练数据约150K高分辨率图像（CLIC 2020 Professional、MLIC-Train-100K、LSDIR），规模相对有限。对于长尾内容或特定领域（如医学影像、遥感图像），预训练DiT的生成先验可能不匹配，导致重建质量下降。LoRA适配虽然高效，但也限制了模型容量——Table 2显示全量微调在部分指标上略优于LoRA，暗示在更大规模数据和更复杂分布下，全量微调可能获得更好性能。

#### 3.3 分辨率可扩展性

论文验证了最高4096²分辨率下的可扩展性，采用1024×1024分块解码时峰值内存低于7GB（16GB笔记本GPU可运行）。但**8K/16K等极端分辨率**下的延迟和内存表现尚未验证，分块策略可能引入边界伪影。

#### 3.4 编码器冻结的代价

自蒸馏对齐依赖于冻结的SANA-VAE编码器输出作为对齐目标。这一设计简化了训练，但也意味着：若未来需要更新编码器（如适配新数据类型），整个对齐流程需要重新训练。这限制了方法在持续学习或域适应场景中的灵活性。

### 4. 开放问题

1. **极低码率下的语义增强**：如何在极低码率下有效融合文本先验或其他辅助信息，弥补深层潜在空间的语义不足？当前潜在条件引导在中等码率表现优异，但极端条件下的鲁棒性有待验证。

2. **端到端联合优化**：是否存在统一的训练策略，能够同时更新编码器、对齐模块和解码器，而非冻结编码器？这需要解决联合训练中的稳定性问题，但可能释放更大的性能潜力。

3. **视频压缩扩展**：深层潜在空间是否有助于时序一致性建模？将DiT-IC的框架扩展到视频压缩，需要处理运动估计、时序条件注入等新挑战。

4. **架构效率的进一步优化**：DiT虽然在深层潜在空间中高效，但其自注意力机制在极高分辨率下仍存在二次复杂度。是否存在更高效的注意力机制或替代架构（如线性注意力、状态空间模型），进一步降低深层潜在空间扩散的计算和内存开销？

5. **失真-感知权衡的量化与控制**：对抗训练引入的失真-感知权衡目前通过损失权重间接控制。如何量化这一权衡，并设计可控的机制（如感知约束下的保真度最大化），使重建同时满足不同应用场景的需求？

6. **用户偏好分数的统计显著性**：论文报告的用户研究中DiT-IC获得56.8%的最高偏好分数，但未明确说明参与者数量及筛选标准。该结果的统计显著性和生态效度需要独立验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/DiT_IC_Aligned_Diffusion_Transformer_for_Efficient_Image_Compression.pdf]]
