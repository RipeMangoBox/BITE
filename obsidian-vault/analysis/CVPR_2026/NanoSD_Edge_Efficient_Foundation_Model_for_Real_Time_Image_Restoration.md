---
title: "NanoSD: Edge Efficient Foundation Model for Real Time Image Restoration"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/NanoSD_Edge_Efficient_Foundation_Model_for_Real_Time_Image_Restoration.pdf
project_link: null
code_link: null
aliases:
- NanoSD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过硬件感知的网络手术将 U‑Net 分解为形状保持的块变体，结合逐块特征匹配蒸馏与多目标贝叶斯优化，在保持 SD 1.5 生成先验的前提下搜索出最优的块组合。
primary_logic: 逐块独立蒸馏使得 32,768 种组合的大规模搜索成为可能，而从 Pareto 前沿选出的架构能在生成保真度、设备延迟和参数量之间实现最优折中，从而将扩散模型压缩至移动端实时可运行的规模；同时证明参数减少与硬件效率并不线性相关。
claims:
- NanoSD Model 2 在 Qualcomm NPU 上实现 27 ms 延迟、315 M 参数、taFID 10 的平衡最优。
- NanoSD 在延迟‑taFID 和参数‑taFID Pareto 前沿上显著优于 Segmind TinySD 和手工设计基线。
- 重新引入 E4‑‑Mid‑‑D4 块使参数从 309 M 增至 565 M，延迟仅从 41 ms 升至 46 ms，而生成质量几乎无变化，证明移除深层块是合理的。
- Nano‑OSEDiff 在 DIV‑2K Val 上以更低 MACs 取得 PSNR 24.29，超越 Edge‑SD‑SR、PocketSR 等轻量方案。
---

# NanoSD: Edge Efficient Foundation Model for Real Time Image Restoration

> [!tip] 核心洞察
> 逐块独立蒸馏使得 32,768 种组合的大规模搜索成为可能，而从 Pareto 前沿选出的架构能在生成保真度、设备延迟和参数量之间实现最优折中，从而将扩散模型压缩至移动端实时可运行的规模；同时证明参数减少与硬件效率并不线性相关。

| 字段 | 内容 |
|------|------|
| 中文题名 | NanoSD：面向实时图像恢复的边缘高效基础模型 |
| 英文题名 | NanoSD: Edge Efficient Foundation Model for Real Time Image Restoration |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.09823) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | NanoSD |
| Dataset | DIV-2K Val, DRealSR, CelebA‑Test, RealBlur‑J |

> [!tip] 效果简介
> - DIV-2K Val (super‑resolution) 上，PSNR↑ 24.29 (Nano‑OSEDiff) vs 24.10 (Edge‑SD‑SR) (+0.19)。
> - DRealSR (real‑world super‑resolution) 上，PSNR↑ 29.01 (Nano‑OSEDiff) vs 27.92 (OSEDiff) (+1.09)。
> - CelebA‑Test (face restoration) 上，MACs (G) ↓ 479 (Nano‑OSDFace) vs 2465 (OSDFace) (-1986 (≈5.1× reduction))。

## 概要

将 Stable Diffusion 等大型扩散模型部署到边缘 NPU 面临一个根本矛盾：全量 U‑Net 和 VAE 的计算开销极高，而 FLOPs 或参数量这类传统指标并不能真实反映实际设备延迟；现有的轻量化方法往往破坏潜空间结构，导致生成先验丧失，难以泛化到超分辨率、人脸修复、去模糊等多种恢复任务。

NanoSD 的核心思路是通过**硬件感知的网络手术**将 SD 1.5 的 U‑Net 分解为逐阶段、形状保持的块变体，再结合**逐块特征匹配蒸馏**与**多目标贝叶斯优化**，在保持 SD 1.5 生成先验的前提下，从 32,768 种候选架构中搜索出在生成保真度、设备延迟和参数量之间实现最优折中的 Pareto 前沿架构。这一流程使得扩散模型首次被压缩至移动端实时可运行的规模，同时揭示了参数减少与硬件效率之间并非线性相关。

在方法定位上，NanoSD 并非针对单一任务的轻量模型，而是一个**可插拔的边缘高效扩散骨干**：它可直接替换 OSEDiff、S3Diff、Diff‑Plugin、OSDFace、DiffBIR、Marigold 等框架中的原始扩散模型，以极低的计算代价保留甚至提升原有恢复性能。实验表明，NanoSD 在 Qualcomm NPU 上实现 12–27 ms 延迟、130–315 M 参数的 Pareto 最优族，其中 Model 2 以 27 ms 延迟、315 M 参数、taFID 10 取得最佳平衡。在下游任务中，Nano‑OSEDiff 在 DIV‑2K Val 上以更低 MACs 取得 PSNR 24.29，超越 Edge‑SD‑SR 等轻量方案；Nano‑OSDFace 将 OSDFace 的 MACs 降低约 5.1 倍（2465 G → 479 G），同时在真实人脸数据集上保持竞争力；Nano‑Diff‑Plugin 在 RealBlur‑J 上 FID 降低 29.76，MACs 减少 9.4 倍。与 SD 1.5 教师的 LPIPS 为 0.57、嵌入余弦相似度 0.84，远优于直接回归的 U‑Net 基线（LPIPS 1.92，相似度 0.41），证明生成先验得到良好保留。消融研究进一步确认，移除深层低分辨率块（E4–Mid–D4）使参数从 565 M 降至 309 M，延迟仅从 46 ms 降至 41 ms，生成质量几乎无变化，验证了深层块对边缘效率贡献甚微。跨平台测试在 Apple A17 Pro Neural Engine 上复现了与 Qualcomm NPU 高度一致的相对延迟排序，表明搜索产生的架构具有跨加速器鲁棒性。

### 扩散模型在图像恢复中的兴起与边缘部署困境

扩散模型已成为图像恢复领域的主流范式。以 **Stable Diffusion 1.5（SD 1.5）** 为代表的潜在扩散模型通过在压缩潜空间中进行迭代去噪，展现出强大的生成先验，能够有效处理超分辨率、去模糊、去噪、人脸修复等多种低层视觉任务。然而，这类模型的推理过程依赖于庞大的 U‑Net 去噪器和变分自编码器（VAE），其全量参数规模高达约 860 M，在边缘设备上的计算开销极为高昂，难以满足实时性要求。

### 现有轻量化方法的局限性

针对扩散模型的边缘部署，已有若干轻量化尝试，但普遍存在以下瓶颈：

1. **FLOPs 与硬件延迟的脱节**：现有压缩方法多以 FLOPs 或参数量作为优化目标，但这些指标并不能真实反映在移动端 NPU 上的实际延迟。实验表明，参数减少与硬件效率之间并非线性相关——某些参数更少的架构在设备上的运行速度反而更慢。

2. **潜空间结构的破坏**：直接对 U‑Net 进行剪枝或通道缩减等粗粒度压缩，容易破坏 SD 1.5 教师模型所学习到的潜空间结构，导致生成质量严重退化，且压缩后的模型难以泛化到多种恢复任务。

3. **搜索空间与蒸馏策略的失配**：现有方法（如 **Segmind TinySD**）通常采用手工设计或单一维度的压缩策略，无法系统性地探索架构效率与生成保真度之间的最优权衡，最终落在 Pareto 前沿的次优区域。

### 核心动机与解决思路

针对上述问题，本文的核心动机是：**在保持 SD 1.5 生成先验的前提下，通过硬件感知的网络手术与多目标优化，将扩散模型压缩至移动端实时可运行的规模，同时保持对多种恢复任务的泛化能力。**

具体而言，本文提出 **NanoSD** 框架，其关键思路包括：

- **硬件感知的 U‑Net 分解**：将 SD 1.5 的 U‑Net 按阶段（Encoder‑1 至 Decoder‑3）分解为形状保持的块变体（如 R、RA、RAR、RRA 等），并在目标 NPU 上实测每个变体的延迟，构建与硬件特性对齐的搜索空间。同时，移除深层低分辨率阶段（Encoder‑4、Middle、Decoder‑4），以在不损失生成质量的前提下大幅降低参数量。

- **逐块特征匹配蒸馏**：提出特征逐块生成蒸馏（Feature‑wise Generative Distillation, FwGD），对每个候选块独立地匹配其教师块的输出分布，使得大规模架构搜索无需全模型重训练即可完成。

- **多目标贝叶斯优化**：以教师对齐的 FID（taFID）、设备延迟和参数量为优化目标，利用期望超体积改进（EHVI）准则搜索 Pareto 最优的块组合，从而在生成保真度与边缘效率之间取得最优折中。

通过上述设计，NanoSD 能够在 Qualcomm NPU 上实现低至 27 ms 的推理延迟，同时将参数规模压缩至 315 M，并在超分辨率、人脸修复、去模糊等多种任务上展现出与全量模型相当甚至更优的性能。

## 核心方法与创新机理

NanoSD 的核心创新在于将 Stable Diffusion 1.5 的全量扩散模型压缩至边缘 NPU 实时可运行的规模，同时完整保留其生成先验。这一目标通过三个紧密耦合的技术环节实现：**硬件感知的网络手术**、**逐块特征匹配蒸馏**以及**多目标贝叶斯优化搜索**。

### 瓶颈与因果调节变量

Stable Diffusion 1.5 在边缘部署面临的根本瓶颈并非单纯的参数量或 FLOPs 过大，而是其 U‑Net 和 VAE 的深层低分辨率模块（Encoder‑4、Middle、Decoder‑4）在边缘 NPU 上产生了不成比例的计算开销与内存占用，且 FLOPs 与实际延迟之间存在显著的非线性偏差。现有轻量化方法（如直接剪枝或手工设计窄化网络）往往破坏潜空间结构，导致在多种恢复任务上的泛化能力急剧下降。

NanoSD 的因果调节变量是：**通过硬件感知的网络手术将 U‑Net 分解为形状保持的块变体，结合逐块特征匹配蒸馏与多目标贝叶斯优化，在保持 SD 1.5 生成先验的前提下搜索出最优的块组合**。这一设计使得参数减少与硬件效率之间的非线性关系被显式建模并纳入优化目标。

### 关键 changed slots

与基线 SD 1.5 U‑Net 相比，NanoSD 在以下四个维度上进行了结构性改变：

1. **移除深层低分辨率阶段**：从设计空间中彻底移除 Encoder‑4、Middle 和 Decoder‑4 三个阶段（Section 3.1）。消融实验（Figure 10, Section 11.1）表明，重新引入这些模块使参数量从 309 M 增至 565 M，但延迟仅从 41 ms 升至 46 ms，且生成质量几乎无变化——这证明深层低分辨率块对边缘效率贡献甚微，其移除是合理的。

2. **形状保持的块变体替换**：对于保留的六个阶段（编码器 E1–E3，解码器 D1–D3），将标准的注意力‑残差序列（如 R‑A‑R‑A）替换为经过硬件感知手术派生的形状保持变体（R、RA、RAR、RRA 等）。这些变体在保持张量形状不变的前提下，提供了 3–8× 的延迟下降（Table 7），为搜索空间注入了丰富的硬件多样性。

3. **轻量化 VAE 蒸馏**：将 SD 1.5 VAE 中随深度逐级扩宽的 ResNet 块（64→128→256→512 通道）替换为固定 64 通道的 Tiny ResNet 块（Table 9），通过特征匹配损失进行蒸馏，在保持重建质量的同时大幅降低编解码开销。

4. **U‑Net 整体规模压缩**：从全量 SD 1.5 U‑Net 的约 860 M 参数压缩至 Pareto 最优变体的 130 M–315 M 参数范围（Table 1），在生成保真度、设备延迟和参数量之间实现了多维度的最优折中。

### 核心洞察：逐块独立蒸馏使大规模搜索成为可能

NanoSD 的关键洞察在于：**逐块独立蒸馏使得 32,768 种组合的大规模架构搜索成为可能**。传统的架构搜索需要对每个候选网络进行完整训练，计算成本不可承受。NanoSD 通过特征逐块生成蒸馏（FwGD），以 L2 损失对齐每个候选块与其教师块的输出分布：

$$\mathcal{L}_{\mathrm{distill}}^{(i,j)} = \|O_S - O_T\|_2^2$$

其中 $O_T = \mathcal{B}_i(F)$ 为教师块输出，$O_S = \mathcal{B}_{i,j}(F)$ 为学生块输出。这一策略将搜索的计算复杂度从“完整模型训练”降为“单块蒸馏”，使 32,768 种架构的评估成为可行。随后，多目标贝叶斯优化以 Expected Hypervolume Improvement（EHVI）为采集函数，在 taFID（与教师分布的距离）和实际设备延迟/参数量之间搜索 Pareto 前沿：

$$\operatorname*{min}_{\mathbf{z}} \left( f_{\mathrm{FID}}(\mathbf{z}), \ f_{\mathrm{latency}}(\mathbf{z}) \right)$$

从 Pareto 前沿选出的架构（如 Model 2：315 M 参数、27 ms 延迟、taFID 10）在生成保真度与硬件效率之间达到了最优平衡，同时证明参数减少与硬件效率之间并非线性相关——这一发现对边缘部署具有重要的工程指导意义。

NanoSD 的核心目标是将 Stable Diffusion 1.5 的生成先验压缩至边缘 NPU 可实时运行的规模，并保持对多种图像恢复任务的泛化能力。其 pipeline 由五个关键模块串联而成，形成“分解—蒸馏—搜索—压缩—对齐”的闭环。

### 硬件感知的 U‑Net 分解

首先对 SD 1.5 的全量 U‑Net 进行结构手术。原 U‑Net 包含四个编码器阶段（E1–E4）、一个中间块（Mid）和四个解码器阶段（D4–D1）。分析表明，深层低分辨率阶段（E4、Mid、D4）对生成质量的贡献极小，却占用大量参数和内存带宽，因此**直接从设计空间中移除**这三个阶段，仅保留 E1–E3 和 D3–D1 六个阶段（Figure 2a, 2b）。

对保留的每个阶段，从原始块结构（如 R‑A‑R‑A，其中 R 为残差块、A 为注意力块）出发，派生出多个**形状保持的块变体**（R、RA、RAR、RRA 等）。这些变体保持输入/输出张量形状不变，但在内部计算结构上产生显著差异，从而在硬件延迟和参数量上形成多样性。所有变体均在目标 Qualcomm NPU 上进行逐块延迟实测，构成硬件感知的搜索空间，共包含 $4 \times 4 \times 4 \times 8 \times 8 \times 8 = 32,768$ 种候选 U‑Net 架构。

### 逐块生成蒸馏

为评估每种候选架构的生成保真度，NanoSD 采用**逐块特征匹配生成蒸馏**。对每个阶段的每个候选块 $\mathcal{B}_{i,j}$，独立地将其与对应的 SD 1.5 教师块 $\mathcal{B}_i$ 对齐：

$$O_T = \mathcal{B}_i(F), \quad O_S = \mathcal{B}_{i,j}(F)$$
$$\mathcal{L}_{\mathrm{distill}}^{(i,j)} = \|O_S - O_T\|_2^2$$

这一策略的核心优势在于：**每个块的蒸馏完全独立**，无需训练完整模型即可评估任意块组合的保真度。这为后续的 $32,768$ 种架构的大规模搜索提供了可行性基础。

### 组合式架构评估

任意一个完整的 U‑Net 架构由一个离散决策向量 $\mathbf{z} = [z_1, z_2, z_3, z_4, z_5, z_6]$ 编码，每个元素从对应阶段的候选块中选择一个。将该向量指定的六个蒸馏块按 SD 1.5 的跳连结构组装，即得到一个结构合法的学生 U‑Net。每个组装模型在以下三个目标上评估：

- **taFID（Teacher‑aligned FID）**：学生生成分布与 SD 1.5 教师分布之间的 Fréchet Inception Distance，衡量生成先验的保留程度：
  $$f_{\mathrm{FID}}(\mathbf{z}) = \mathrm{FID}\Big(\hat{X}(\mathbf{z}), X_{\mathrm{SD1.5}}\Big)$$
- **设备延迟** $f_{\mathrm{latency}}(\mathbf{z})$：在目标 NPU 上的实测推理延迟（8‑bit 权重、16‑bit 激活）。
- **参数量** $f_{\mathrm{param}}(\mathbf{z})$。

### 多目标贝叶斯优化搜索

在离散的组合空间中，NanoSD 采用**多目标贝叶斯优化**，以 Expected Hypervolume Improvement 为采集函数，同时优化 taFID 与延迟、taFID 与参数量两组目标：

$$\operatorname*{min}_{\mathbf{z}} \left( f_{\mathrm{FID}}(\mathbf{z}), \ f_{\mathrm{latency}}(\mathbf{z}) \right)$$
$$\operatorname*{min}_{\mathbf{z}} \left( f_{\mathrm{FID}}(\mathbf{z}), \ f_{\mathrm{param}}(\mathbf{z}) \right)$$

搜索产生两条 Pareto 前沿（Figure 2e, 2f），从中选出 7 个 Pareto 最优架构构成 NanoSD 家族（Table 1），覆盖从极致低延迟（Model 5，12 ms）到极小参数（Model 7，130 M）的不同工作点。其中 **Model 2**（315 M 参数，27 ms 延迟，taFID 10）在生成保真度与效率之间取得最佳平衡，被选为后续所有下游实验的骨干模型。

### VAE 蒸馏与端到端扩散对齐

在 U‑Net 架构确定后，进一步对 VAE 进行压缩。学生 VAE 采用固定的 64 通道 Tiny ResNet 块替代原 SD 1.5 VAE 中逐级扩宽的结构（64→128→256→512 通道），通过均值/标准差匹配损失进行蒸馏：

$$\mathcal{L}_{\mathrm{latent}} = \|\mu_t(x) - \mu_s(x)\|_2^2 + \|\sigma_t(x) - \sigma_s(x)\|_2^2$$

最后，为纠正逐块蒸馏带来的累积误差，对整个 NanoSD 管线（学生 VAE + 选定 U‑Net）进行端到端扩散对齐微调，使用标准去噪目标匹配教师 U‑Net 的噪声预测：

$$\mathcal{L}_{\mathrm{align}} = \|U_s(\alpha z_s + \sigma_t \epsilon, t, c) - U_t(\alpha z_t + \sigma_t \epsilon, t, c)\|_2^2$$

### 推理部署策略

在边缘设备上进行高分辨率图像恢复时，NanoSD 采用**分块推理**策略（Figure 9）。输入图像被分割为 $128 \times 128$ 的瓦片（25% 重叠），各瓦片独立通过 NanoSD 处理后拼接为最终输出。这一策略在保持感知一致性的同时，满足了移动端 NPU 的内存与实时性约束。

![[assets/figures/papers/paper_list_l903_https_arxiv_org_abs_2601_09823/figures/015_Figure_9.jpg]]
*Figure 9: NanoSD employs a tiled inference strategy to enable high-resolution image restoration on edge computing platforms. The processing pipeline begins by partitioning a 1000×750 input image into 128×128 overlapping tiles (25% overlap), generating 88 total tiles. Each tile undergoes independent processing through the NanoSD model before being reassembled into a final 4K resolution output. This tile-based approach achieves two critical objectives: (1) maintaining perceptual consistency across the reconstructed image, and (2) meeting the computational constraints of mobile processors for real-time operation. The method effectively balances restoration quality with the practical requirements of edge...*

整个 pipeline 的输入是低质图像（或文本提示），经学生 VAE 编码为潜变量，由搜索得到的高效 U‑Net 在潜空间进行去噪/恢复，最后经学生 VAE 解码输出恢复图像。各模块之间的关系是严格串行的：U‑Net 架构搜索依赖于 VAE 提供的潜空间，VAE 蒸馏在 U‑Net 冻结后进行，端到端对齐则统一校正两者的协同误差。

NanoSD 的核心设计围绕一个硬件感知的架构搜索与蒸馏流水线展开，其关键模块包括：U‑Net 形状保持分解、逐块生成式蒸馏、多目标贝叶斯优化，以及后续的 VAE 蒸馏与端到端扩散对齐。

### U‑Net 形状保持分解

NanoSD 从 Stable Diffusion 1.5 的全量 U‑Net 出发，首先移除 Encoder‑4、Middle、Decoder‑4 三个深层低分辨率阶段（Section 3.1），理由在于这些块虽然贡献大量参数，但在低空间分辨率下操作，对边缘 NPU 的实际延迟影响甚微（消融实验证实，重新引入 E4‑‑Mid‑‑D4 使参数从 309 M 增至 565 M，延迟仅从 41 ms 升至 46 ms，生成质量几乎无变化；Figure 10）。保留的六个阶段（E1–E3 编码器、D3–D1 解码器）各自被分解为若干形状保持的块变体，例如 R、RA、RAR、RRA 等注意力‑残差序列组合。这些变体保持输入/输出张量形状不变，从而可独立替换对应位置的教师块，构成包含 32,768（即 $4 \times 4 \times 4 \times 8 \times 8 \times 8$）种候选架构的离散搜索空间，并在目标 NPU 上进行逐块延迟与参数量测量（Table 7），确保搜索空间直接反映真实硬件特性。

### 逐块生成式蒸馏（FwGD）

为使每个候选块在独立替换后仍能保持生成先验，NanoSD 引入逐块特征匹配蒸馏。对于第 $i$ 阶段的教师块 $\mathcal{B}_i$ 及其学生变体 $\mathcal{B}_{i,j}$，给定输入特征 $F$，教师与学生输出分别为：

$$O_T = \mathcal{B}_i(F), \quad O_S = \mathcal{B}_{i,j}(F)$$

蒸馏损失采用 L2 特征匹配形式：

$$\mathcal{L}_{\mathrm{distill}}^{(i,j)} = \|O_S - O_T\|_2^2$$

这一逐块对齐策略使得每个学生块能够独立逼近其教师块的输出分布，从而在无需完整模型重训练的前提下，为后续组合式搜索提供 3–8× 延迟下降的多样化候选块（Table 7），同时保持与教师分布的一致性。

### 多目标贝叶斯优化

完整 U‑Net 架构由一个离散决策向量 $\mathbf{z} = [z_1, z_2, z_3, z_4, z_5, z_6]$ 编码，其中每个元素从对应阶段的候选块中选择一个。搜索目标同时考虑生成保真度、设备延迟和参数量。保真度通过教师对齐的 FID 衡量：

$$f_{\mathrm{FID}}(\mathbf{z}) = \mathrm{FID}\Big(\hat{X}(\mathbf{z}), X_{\mathrm{SD1.5}}\Big)$$

其中 $\hat{X}(\mathbf{z})$ 为架构 $\mathbf{z}$ 的生成分布，$X_{\mathrm{SD1.5}}$ 为 SD 1.5 教师的生成分布。由此形成两类双目标优化问题：

$$\min_{\mathbf{z}} \left( f_{\mathrm{FID}}(\mathbf{z}), \ f_{\mathrm{param}}(\mathbf{z}) \right)$$

$$\min_{\mathbf{z}} \left( f_{\mathrm{FID}}(\mathbf{z}), \ f_{\mathrm{latency}}(\mathbf{z}) \right)$$

搜索采用贝叶斯优化，通过最大化期望超体积改进（Expected Hypervolume Improvement, EHVI）在离散空间中选择候选点，最终产出延迟‑taFID 和参数‑taFID 两条 Pareto 前沿（Fig. 2e, 2f）。从 Pareto 前沿中选出的七种架构构成 NanoSD 家族，其中 Model 2 在 27 ms 延迟、315 M 参数下取得 taFID 10 的最优平衡，被选为下游任务的默认骨干（Table 1）。

### VAE 蒸馏与端到端扩散对齐

在 U‑Net 搜索完成后，NanoSD 对 VAE 编码器/解码器进行蒸馏。学生 VAE 采用固定 64 通道的 Tiny ResNet 块替代教师 VAE 的宽化残差块（Table 9），蒸馏损失匹配教师与学生编码器输出的均值 $\mu$ 和标准差 $\sigma$：

![[assets/figures/papers/paper_list_l903_https_arxiv_org_abs_2601_09823/figures/018_Table_9.jpg]]
*Table 9: Architectural comparison of the Teacher VAE (SD 1.5) and the proposed Student VAE. Both models are shown using a unified notation with identical spatial dimensions. Only architectural differences are listed. ResNetBlockTiny refers to a lightweight residual block that preserves the Conv–Norm–Activation–Conv pattern of a standard ResNet block but replaces the full*

$$\mathcal{L}_{\mathrm{latent}} = \|\mu_t(x) - \mu_s(x)\|_2^2 + \|\sigma_t(x) - \sigma_s(x)\|_2^2$$

最后，为纠正逐块蒸馏带来的累积误差，对组装后的完整 NanoSD 流水线进行端到端扩散对齐微调。给定潜变量缩放因子 $\alpha = 0.18215$（即 $\tilde{z}_t = \alpha z_t$），对齐损失匹配学生与教师 U‑Net 的噪声预测：

$$\mathcal{L}_{\mathrm{align}} = \|U_s(\alpha z_s + \sigma_t \epsilon, t, c) - U_t(\alpha z_t + \sigma_t \epsilon, t, c)\|_2^2$$

这一端到端微调步骤有效修复了逐块蒸馏引入的分布偏移，使 NanoSD 在 LPIPS 和嵌入余弦相似度上显著优于未对齐的 U‑Net 基线（LPIPS 0.57 vs. 1.92，相似度 0.84 vs. 0.41；Table 6）。

## 实验与关键发现

### 硬件感知搜索与 Pareto 最优架构

NanoSD 的核心实验逻辑建立在“硬件感知网络手术 + 逐块蒸馏 + 多目标贝叶斯优化”三条因果链上。首先，将 SD 1.5 U‑Net 的 Encoder‑4、Middle、Decoder‑4 阶段从搜索空间中移除（Section 3.1），这一决策的合理性由消融实验直接支撑：重新引入 E4‑‑Mid‑‑D4 块使参数量从 309 M 增至 565 M，而延迟仅从 41 ms 升至 46 ms，生成质量几乎无变化（Figure 10, Section 11.1）。这表明深层低分辨率块对边缘效率贡献甚微，验证了搜索空间剪枝的有效性。

![[assets/figures/papers/paper_list_l903_https_arxiv_org_abs_2601_09823/figures/021_Figure_10.jpg]]
*Figure 10: Ablation demonstrating the effect of reintroducing the*

在此基础上，对保留的六个阶段（E1–E3, D3–D1）构造形状保持的块变体（R, RA, RAR, RRA 等），在 Qualcomm SM8750 NPU 上进行逐块延迟剖析。Table 7 报告了 30 个替代块的延迟测量结果，多个硬件感知变体相比原始 SD 1.5 块实现了 3–8× 的延迟下降，为搜索空间提供了丰富的硬件多样性。

随后，通过特征逐块生成蒸馏（FwGD）独立训练每个候选块，使其输出与教师块对齐（损失函数 $\mathcal{L}_{\mathrm{distill}}^{(i,j)} = \|O_S - O_T\|_2^2$），从而使得 32,768 种组合的大规模搜索无需全模型重训练。多目标贝叶斯优化以 Expected Hypervolume Improvement（EHVI）为采集函数，在 taFID‑延迟和 taFID‑参数量两个双目标空间上搜索。

搜索结果如 Table 1 所示，产生了七个 Pareto 最优架构（NanoSD Model 1–7），覆盖了从极致低延迟到极致小参数的不同工作点：
- **Model 5**：延迟最低，仅 12 ms，适合对实时性要求最苛刻的场景；
- **Model 7**：参数量最少，仅 130 M，适合严格的内存受限场景；
- **Model 2**：延迟 27 ms、参数 315 M、taFID 10，在三个维度上取得最佳平衡，被选为下游所有实验的默认骨干（NanoSD‑Prime）。

![[assets/figures/papers/paper_list_l903_https_arxiv_org_abs_2601_09823/figures/003_Table_1.jpg]]
*Table 1: Comparison of TinySD (Segmind), hand-tuned baseline, and NanoSD variants. Latency is measured on a Qualcomm NPU using 8-bit weights and 16-bit activations. taFID denotes the teacher-aligned FID metric used during the search. The seven NanoSD models correspond to all Pareto-optimal architectures obtained from the latency–taFID and parameter–taFID objectives. For each model, we list the selected block variants across the retained stages of the SD 1.5 U–Net (E1–E3 for encoders and D3–D1 for decoders). Model 5 achieves the lowest latency, Model 7 achieves the fewest parameters, and Model 2 provides the best overall balance of accuracy and efficiency and is used as NanoSD in all downstream exper...*

Figure 2e 和 Figure 2f 的 Pareto 前沿图直观展示了 NanoSD 系列架构相对于 Segmind TinySD 和手工设计基线的显著优势——后者均远离前沿面，证明系统化的硬件感知搜索远优于启发式压缩。

### 跨平台鲁棒性验证

一个关键问题是：针对 Qualcomm NPU 优化的架构是否具有跨加速器泛化能力？Table 8 给出了肯定答案。将 NanoSD Pareto 集中的所有 U‑Net 候选模型直接部署到 Apple A17 Pro Neural Engine 上测试，其相对延迟排序与 Qualcomm NPU 上的趋势高度一致。这一结果揭示了两个深层事实：（1）硬件感知搜索产生的架构具有跨加速器鲁棒性；（2）FLOPs 或参数量为中心的压缩策略无法可靠预测真实边缘性能，进一步验证了以实测延迟为优化目标的必要性。

![[assets/figures/papers/paper_list_l903_https_arxiv_org_abs_2601_09823/figures/017_Table_8.jpg]]
*Table 8: Cross-platform latency analysis of NanoSD family on the Apple A17 Pro Neural Engine (iOS). We evaluate all U–Net candidates from the NanoSD Pareto set—originally optimized using Qualcomm SM8750 latency data—on the Apple ANE without modification. The relative latency ordering and efficiency trends mirror those observed on SM8750, confirming that the proposed hardware-aware search produces architectures that generalize across accelerators. This consistency demonstrates the hardware-agnostic nature of our method and highlights the limitations of FLOP- or parameter-centric compression for predicting real-world edge performance*

### 生成先验保留的定量证据

NanoSD 的核心价值主张是“在极致压缩的同时保留 SD 1.5 的生成先验”，Table 6 提供了关键定量证据。以 LPIPS 感知距离和 CLIP 嵌入余弦相似度衡量与 SD 1.5 教师分布的接近程度：
- NanoSD 与 SD 1.5 的 LPIPS 为 0.57，嵌入余弦相似度为 0.84；
- 相比之下，回归式 U‑Net 基线的 LPIPS 高达 1.92，相似度仅 0.41。

这一差距表明，NanoSD 的逐块生成蒸馏策略有效保留了潜空间的结构化先验，而非简单地拟合像素级映射。Figure 8 的潜空间插值实验提供了定性佐证：在随机种子之间，NanoSD 与 SD 1.5 均展现出平滑的生成过渡，确认了流形结构的保持。

### 超分辨率任务上的效率与精度权衡

将 NanoSD 作为骨干集成到单步扩散超分辨率框架 OSEDiff 和 S3Diff 中，在 DIV‑2K Val 上进行了系统比较（Table 10）。Nano‑OSEDiff 以更低的 MACs 取得 PSNR 24.29，超越 Edge‑SD‑SR（PSNR 24.10）等轻量方案。Nano‑S3Diff 在 NIQE 和 MUSIQ 等感知指标上取得最优，FID 位列第二。

![[assets/figures/papers/paper_list_l903_https_arxiv_org_abs_2601_09823/figures/019_Table_10.jpg]]
*Table 10: Quantitative comparison of different methods on DIV-2K Val [1]to dataset. The best, second-best and third-best results are highlighted in red, blue, and green colors, respectively*

在真实世界超分辨率数据集 DRealSR 上（Table 11），Nano‑OSEDiff 的 PSNR 达到 29.01，相比原始 OSEDiff（27.92）提升 1.09 dB。这一反直觉的提升可能源于蒸馏过程中的隐式正则化效应，但原文未给出因果解释，需要手动验证。

### 人脸恢复与多任务泛化

在人脸恢复任务上（Table 3），Nano‑OSDFace 以 479 G MACs 取得与 OSDFace（2465 G MACs）可比的恢复质量，计算量减少约 5.1×。在多个底层视觉任务（去雪、去雾、去模糊、去雨）上（Table 4），Nano‑Diff‑Plugin 在 RealBlur‑J 上以 17120 G MACs 取得 FID 52.41，而原始 Diff‑Plugin 需要 160640 G MACs 且 FID 为 82.17——效率提升 9.4× 的同时质量大幅领先。

在单目深度估计任务上（Table 5），Nano‑Marigold 在 NYUv2 上的 AbsRel 为 7.2，相比 Marigold 的 6.9 略有退化，但模型尺寸缩小约 90%。这一结果表明，生成先验的压缩在密集预测任务上存在一定的保真度损失，属于可预期的权衡。

### 关键消融与失败模式

**深层块移除的合理性**已在 Figure 10 中验证。需要注意，该消融在预微调（pre‑finetuning）阶段进行，微调后可能进一步缩小质量差距，但原文未提供微调后的对比数据，这一点需要手动验证。

**端到端对齐的必要性**：逐块蒸馏后，组装的全模型存在累积误差。NanoSD 通过标准扩散去噪目标进行端到端微调（损失函数 $\mathcal{L}_{\mathrm{align}} = \|U_s(\alpha z_s + \sigma_t \epsilon, t, c) - U_t(\alpha z_t + \sigma_t \epsilon, t, c)\|_2^2$）来纠正这一误差。原文未提供该步骤的消融实验，其贡献量无法从现有证据中量化。

**VAE 蒸馏的影响**：Student VAE 采用固定 64 通道的 Tiny ResNet 块替换教师 VAE 的渐进式扩宽结构（Table 9），通过均值和方差的特征匹配损失进行蒸馏。VAE 压缩对整体效率的贡献未在消融中单独量化，需要手动验证。

### 实验公平性说明

所有延迟测量均在 Qualcomm SM8750 NPU 上使用 8‑bit 权重和 16‑bit 激活进行，反映真实边缘部署条件。taFID 是相对保真度指标，衡量与 SD 1.5 教师分布的距离，而非绝对图像质量，因此不能直接与其他方法的 FID 对比。不同基线的推理步数可能不同（如 DiffBIR 使用 50 步，OSEDiff 仅需 1 步），报告的计算量按原始配置给出。

## 定位与知识库关联

### 1. 与教师模型和轻量化基线的关系

NanoSD 的核心定位是 **Stable Diffusion 1.5 (SD 1.5)** 的边缘高效替代品，而非从头训练的扩散模型。其技术路线与现有轻量化扩散方案存在本质差异：

- **相对于 SD 1.5**：NanoSD 并非简单的剪枝或量化版本，而是通过“硬件感知的网络手术”将 SD 1.5 的 U‑Net 分解为形状保持的块变体，再经由逐块特征匹配蒸馏（FwGD）和多目标贝叶斯优化重建出 Pareto 最优架构。这一策略在保留 SD 1.5 生成先验的同时，将参数量从约 860 M 压缩至 130 M–315 M（Table 1）。定量证据表明，NanoSD 与 SD 1.5 的 LPIPS 为 0.57，CLIP 嵌入余弦相似度为 0.84，远优于回归式 U‑Net 基线（LPIPS 1.92，相似度 0.41），证明生成先验得到良好保留（Table 6）。

- **相对于 Segmind TinySD**：TinySD 是现有的轻量扩散基线，但在延迟–taFID 和参数–taFID 的 Pareto 前沿上均显著劣于 NanoSD 系列（Fig. 2e, Fig. 2f）。这表明单纯缩减模型规模而不考虑硬件特性无法实现真正的边缘高效。

- **相对于手工设计基线**：论文中的 hand‑tuned baseline 同样远离 Pareto 前沿（Fig. 2e, Fig. 2f），说明人工调参难以在生成保真度、延迟和参数量三者之间找到最优折中。

### 2. 与下游任务框架的集成关系

NanoSD 作为边缘基础模型，其价值在于可无缝嵌入多种已有的图像恢复框架，替代其中的 SD 1.5 U‑Net 主干。论文验证了以下集成路径：

- **超分辨率**：与 **OSEDiff**（单步潜空间扩散超分框架）和 **S3Diff**（退化感知单步超分框架）集成，形成 Nano‑OSEDiff 和 Nano‑S3Diff。在 DIV‑2K Val 上，Nano‑OSEDiff 以更低 MACs 取得 PSNR 24.29，超越 **Edge‑SD‑SR**（24.10）和 **PocketSR** 等轻量方案（Table 10）；在真实世界数据集 DRealSR 上，Nano‑OSEDiff 的 PSNR 达到 29.01，比原始 OSEDiff（27.92）提升 1.09 dB（Table 11）。

- **人脸恢复**：与 **OSDFace**（单步人脸恢复 SOTA）集成形成 Nano‑OSDFace，在 CelebA‑Test 上将 MACs 从 2465 G 降至 479 G（约 5.1× 缩减），同时保持竞争性的恢复质量（Table 3）。在真实数据集 Wider‑Test、LFW‑Test、WebPhoto‑Test 上的结果见 Table 12。

- **通用图像恢复**：与 **Diff‑Plugin**（任务自适应插件，支持去雪、去雾、去模糊、去雨等）集成形成 Nano‑Diff‑Plugin。在 RealBlur‑J 去模糊任务上，FID 从 82.17 降至 52.41，MACs 从 160640 G 降至 17120 G（约 9.4× 缩减）（Table 4）。定性对比见 Figure 6、Figure 14、Figure 15。

- **单目深度估计**：与 **Marigold** 集成形成 Nano‑Marigold，在 NYUv2 上 AbsRel 从 6.9 微升至 7.2（轻微退化），但模型体积缩减约 90%（Table 5）。零样本跨数据集泛化结果见 Table 5 和 Figure 7。

- **文本到图像生成**：NanoSD 本身可作为独立的边缘文本到图像生成器使用（Figure 3），其潜空间插值实验（Figure 8）显示与 SD 1.5 一致的平滑流形结构。

### 3. 适用边界

NanoSD 的设计和验证范围界定了以下适用条件：

- **硬件平台**：主要针对 Qualcomm SM8750 NPU（Samsung S25 Ultra）优化，使用 8‑bit 权重和 16‑bit 激活。跨平台验证（Apple A17 Pro Neural Engine, Table 8）显示 Pareto 架构的相对延迟排序高度一致，表明搜索产生的架构具有跨加速器鲁棒性。但论文未提供其他 NPU/DSP/GPU 平台的系统性基准，在其他硬件上的绝对性能需要手动验证。

- **任务范围**：已验证的任务包括超分辨率、人脸恢复、去模糊、去雪、去雾、去雨、深度估计和文本到图像生成。对于未测试的恢复任务（如去噪、去摩尔纹、老照片修复等），NanoSD 的理论适用性依赖于相应下游框架（如 Diff‑Plugin 类插件）的存在，但缺乏直接实验证据。

- **推理步数**：NanoSD 本身不改变扩散模型的采样步数。下游任务中，OSEDiff 和 S3Diff 采用单步推理，DiffBIR 使用 50 步。论文报告的计算量按各方法的原始配置给出，跨步数的效率对比需注意这一差异。

- **高分辨率推理**：论文提出了分块推理策略（Figure 9），将 1000×750 输入分割为 128×128 重叠块（25% 重叠），独立处理后拼接为 4K 输出。该策略在边缘设备上平衡了感知一致性和计算约束，但其拼接伪影和块边界效应未进行定量消融。

### 4. 关键消融发现与设计合理性

- **深层低分辨率块的移除**：论文将 Encoder‑4、Middle、Decoder‑4 阶段从设计空间中移除。消融实验（Figure 10, Section 11.1）表明，重新引入 E4‑‑Mid‑‑D4 块使参数量从 309 M 增至 565 M，延迟仅从 41 ms 升至 46 ms，而生成质量几乎无变化。这证明深层低分辨率块对边缘效率贡献甚微，移除是合理的。

- **硬件感知蒸馏的有效性**：30 个替代 U‑Net 块的延迟剖析（Table 7）显示，硬件感知变体相比原始 SD 1.5 块可实现 3–8× 的延迟下降，为搜索空间提供了丰富的硬件多样性。这验证了“参数减少与硬件效率并不线性相关”的核心洞察。

- **端到端扩散对齐的必要性**：逐块蒸馏后，论文通过标准扩散去噪目标对整个 NanoSD 管线进行微调，以纠正累积的蒸馏误差（Section 9.6）。这一步骤对于恢复生成质量至关重要，但论文未提供跳过此步骤的定量对比。

### 5. 局限与开放问题

论文未明确列出局限性章节，但基于实验设计和结果可识别以下边界：

- **教师模型锁定**：NanoSD 完全依赖 SD 1.5 作为教师，无法直接受益于 SDXL、SD 3 等更新、更强的扩散模型的生成先验。将该方法迁移至其他教师模型需要重新执行整个搜索–蒸馏–优化流程。

- **taFID 指标的局限性**：搜索过程中使用的 teacher‑aligned FID 衡量的是与 SD 1.5 分布的距离，而非绝对图像质量。这意味着 Pareto 前沿上的“最优”是相对于 SD 1.5 的保真度最优，不一定对应人类感知或下游任务指标的最优。

- **VAE 压缩的独立性与联合优化**：VAE 蒸馏（Table 9）在 U‑Net 搜索完成后独立进行，未与 U‑Net 架构搜索联合优化。这种解耦策略简化了搜索，但可能错失 U‑Net 与 VAE 之间的协同压缩机会。

- **实时性的定义**：论文声称“实时推理”（低至 12–27 ms），但这一延迟仅测量 U‑Net 前向过程，不包括 VAE 编解码、文本编码器、采样循环等完整管线的端到端耗时。实际应用中的“实时”感知需要手动验证完整管线延迟。

- **开放问题**：
  - 该方法能否推广至 DiT（Diffusion Transformer）架构的轻量化？
  - 在多任务联合训练场景下，NanoSD 的生成先验是否会因任务特定微调而退化？
  - 搜索空间中的块变体设计是否可自动化（如通过神经架构搜索生成形状保持变体），而非依赖手工枚举？

## 原文 PDF

![[paperPDFs/CVPR_2026/NanoSD_Edge_Efficient_Foundation_Model_for_Real_Time_Image_Restoration.pdf]]
