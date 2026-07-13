---
title: "SRA 2: Variational Autoencoder Self-Representation Alignment  for Efficient Diffusion Training"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SRA_2_Variational_Autoencoder_Self_Representation_Alignment_for_Efficient_Diffusion_Training.pdf
project_link: null
code_link: null
aliases:
- S2
- S2VASRAEDT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 利用预训练VAE特征的重建特性和内置视觉先验，作为扩散变换器训练中的对齐目标，从而提供丰富的纹理、结构和语义引导。
primary_logic: 预训练VAE在潜在扩散模型的第一阶段已经提取，其特征天然包含图像重构所需的细节和结构信息，可被直接复用为训练引导信号，无需引入额外模型或增大计算开销。
claims:
- SD-VAE特征相比SiT潜在表示在视觉概念描述上显著更优，包含更清晰的细节、结构完整性和语义连贯性。
- SRA 2仅需4%额外GFLOPs且零额外引导特征提取成本。
- 在ImageNet 256×256上，SRA 2在生成质量和训练收敛速度上超越vanilla SiT，并匹配或超越依赖外部模型的方法。
- ImageNet 256×256 (no CFG, SiT-B/2) 上 FID = 28.89
---

# SRA 2: Variational Autoencoder Self-Representation Alignment  for Efficient Diffusion Training

> [!tip] 核心洞察
> 预训练VAE在潜在扩散模型的第一阶段已经提取，其特征天然包含图像重构所需的细节和结构信息，可被直接复用为训练引导信号，无需引入额外模型或增大计算开销。

| 字段 | 内容 |
|------|------|
| 中文题名 | SRA 2：变分自编码器自表征对齐以实现高效扩散训练 |
| 英文题名 | SRA 2: Variational Autoencoder Self-Representation Alignment  for Efficient Diffusion Training |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.17830) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SRA 2 |
| Dataset | ImageNet 256×256, MS-COCO T2I |

> [!tip] 效果简介
> - ImageNet 256×256 (no CFG, SiT-B/2) 上，FID 28.89 vs 33.02 (vanilla SiT-B/2) (-4.13)。
> - ImageNet 256×256 (with CFG, SiT-XL/2) 上，FID 1.52 (800 epochs) vs SOTA with external dependencies (e.g., REPA) (matches or surpasses)。
> - MS-COCO T2I 上，FID↓ / PickScore↑ 4.67 / 20.92 vs vanilla SiT (not explicitly reported) (improved generation performance)。

## 概要

扩散变换器（如 SiT、DiT）在图像生成中展现出强大能力，但其训练过程缺乏内置的视觉先验引导，导致收敛缓慢。现有加速方法试图通过引入外部表征编码器（如 REPA 依赖 DINOv2）或维护双模型自对齐（如 SRA 依赖教师扩散模型）来弥补这一缺陷，但这些方案均引入了额外的计算开销与外部依赖，限制了方法的普适性和效率。

本文提出 **SRA 2**（VAE Self-Representation Alignment），一种轻量级的内在引导框架。其核心洞察在于：潜在扩散模型第一阶段使用的预训练 VAE 已经提取了图像重建所需的丰富特征——包含纹理细节、结构模式与基本语义信息——这些特征天然可被直接复用为扩散变换器训练中的对齐目标，无需引入任何额外模型。SRA 2 仅通过一个轻量投影 MLP 将扩散变换器中间层特征映射至 VAE 特征空间，并以 Smooth L1 损失进行对齐，从而为去噪训练提供有效的视觉先验引导。

**方法定位**：SRA 2 属于训练范式层面的改进，在 SiT 骨干网络（Ma et al., ECCV 2024）的基础上，将引导信号来源从“外部编码器”（如 REPA, Yu et al., ICLR 2025）或“双模型教师”（如 SRA, Jiang et al., arXiv 2025）迁移至“预提取的 VAE 内置特征”，在保持引导有效性的同时消除了外部依赖。

**核心结果**：
- 在 ImageNet 256×256 无 CFG 条件下，SiT-B/2 + SRA 2 的 FID 从 vanilla SiT 的 33.02 降至 **28.89**，降低 4.13。
- 在 SiT-XL/2 800 轮训练后，FID 达到 **1.52**，匹配或超越依赖外部模型的方法。
- 额外计算开销仅为 **4% GFLOPs**，且引导特征提取成本为零（直接复用离线预提取的 VAE 特征）。
- 方法可泛化至文本到图像任务，在 MS-COCO 上取得 FID **4.67**、PickScore **20.92** 的改进结果。

扩散变换器（Diffusion Transformers, DiTs）已成为生成式建模的主流架构，在图像、视频等任务中取得了显著成功。其训练过程通常分为两个阶段：第一阶段，使用变分自编码器（VAE）将图像压缩至低维潜在空间；第二阶段，在潜在空间中训练扩散变换器以学习去噪过程。然而，扩散变换器的训练缺乏内置的视觉先验引导，导致收敛速度缓慢——模型需要大量迭代才能逐步习得图像的语义结构与纹理细节。

为加速这一收敛过程，近期工作提出了表征对齐策略。**REPA**（Yu et al., ICLR 2025）通过引入外部预训练编码器（如DINOv2）作为表征引导，将扩散模型的中间特征与外部特征对齐，从而注入语义先验。然而，该方法依赖外部模型，引入了额外的参数和计算开销。**SRA**（Jiang et al., arXiv 2025）则采用双模型自对齐策略，利用教师扩散模型提供引导，避免了外部编码器的依赖，但仍需维护双模型架构，增加了训练复杂度。这两种范式分别代表了“外部依赖”和“双模型自对齐”两条路线，但都未能同时实现轻量化与无外部依赖。

本文的核心动机源于一个关键观察：预训练VAE的特征天然包含丰富的视觉先验。如Figure 2所示，通过PCA可视化对比，SD-VAE编码器提取的特征在描绘视觉概念方面显著优于SiT的潜在表征——VAE特征保持了更清晰的细节、更完整的结构完整性和更强的语义连贯性，而SiT的潜在特征则相对模糊、缺乏结构信息。这一现象具有直观的解释：VAE在第一阶段训练中被优化以精确重建图像，其编码器必须捕获足够的纹理、结构和语义信息才能实现高质量重建。更重要的是，在标准的两阶段训练流程中，VAE特征已被离线预提取用于第二阶段的扩散模型训练——这些特征可以直接被复用为内置引导信号，无需任何额外的前向计算成本。

基于上述动机，本文提出SRA 2（VAE Self-Representation Alignment），一种轻量级的内在引导框架。SRA 2的核心思想是：将扩散变换器的中间潜在特征与预提取的VAE特征对齐，利用VAE内置的视觉先验为扩散训练提供丰富的纹理、结构和语义引导。该方法通过一个轻量投影MLP实现特征空间变换，并以Smooth L1损失监督对齐过程，在仅增加4% GFLOPs且零额外引导特征提取成本的前提下，显著加速训练收敛并提升生成质量。

## 核心方法与创新机理

SRA 2 的核心创新在于**将预训练 VAE 的编码特征复用作扩散变换器训练的内在对齐信号**，从而在不引入外部模型依赖的前提下，显著加速训练收敛并提升生成质量。其关键创新点可归纳为以下三个维度。

### 1. 从“外部表征”到“内置视觉先验”的范式转换

现有加速训练方法普遍依赖外部表征编码器或双模型架构来提供训练引导，例如 **REPA**（Yu et al., ICLR 2025）需要引入额外的 DINOv2 等预训练编码器作为对齐目标，而 **SRA**（Jiang et al., arXiv 2025）则需要维护一个教师扩散模型进行双模型自对齐。这些方法虽然有效，但引入了显著的外部参数量和计算开销。

SRA 2 的关键洞察在于：潜在扩散模型第一阶段使用的 VAE 编码器已经提取了图像的结构、纹理和语义信息，这些特征天然具备重建所需的丰富视觉先验。如 Figure 2 所示，SD-VAE 特征在描绘视觉概念方面显著优于 SiT 的潜在表示，包含更清晰的细节、完整的结构信息和更强的语义连贯性。更重要的是，这些 VAE 特征在第二阶段扩散训练中通常已被离线预提取，因此 SRA 2 可以直接复用它们作为对齐目标，**实现零额外引导特征提取成本**。

### 2. 轻量级对齐机制：仅需 4% 额外计算量

SRA 2 的对齐机制极为精简。它仅在 SiT 骨干网络的某一中间层后插入一个轻量投影 MLP，将扩散变换器的中间特征映射到 VAE 特征空间，然后通过 Smooth L1 损失最小化两者之间的差异。整体训练目标为去噪损失与对齐损失的加权组合：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\phi} + \lambda \cdot \mathcal{L}_{\mathrm{align}}$$

这一设计带来的计算开销极低——仅增加 4% 的 GFLOPs，且无需任何外部引导模型的前向传播。如 Table 5 所示，与 REPA 和 SRA 相比，SRA 2 的外部前向参数量（EFP）为零，训练速度和延迟均接近 vanilla SiT 基线。

### 3. 与基线方法的核心差异

| 维度 | Vanilla SiT (Ma et al., ECCV 2024) | REPA (Yu et al., ICLR 2025) | SRA (Jiang et al., arXiv 2025) | **SRA 2 (本方法)** |
|------|-------------------------------------|------------------------------|--------------------------------|---------------------|
| **训练引导方式** | 仅去噪损失（速度预测损失） | 外部编码器特征对齐 | 双模型教师-学生自对齐 | VAE 特征对齐（轻量投影层 + Smooth L1 损失） |
| **外部依赖** | 无（但收敛慢） | 需外部预训练编码器（如 DINOv2） | 需维护教师扩散模型 | **无外部依赖**，复用预提取的 VAE 特征 |
| **额外计算开销** | 0% | 显著（外部编码器前向 + MLP） | 显著（双模型维护 + MLP） | **仅 4% GFLOPs**，零引导特征提取成本 |

这种设计使 SRA 2 在保持方法简洁性的同时，实现了对依赖外部模型方法的性能匹配甚至超越。在 ImageNet 256×256 上，SiT-B/2 + SRA 2 的 FID 达到 28.89，相比 vanilla SiT 的 33.02 降低了 4.13；在 SiT-XL/2 上，800 epoch 训练的 FID 达到 1.52，匹配或超越了 REPA 等依赖外部模型的方法。

SRA 2 的整体训练框架建立在**可扩展插值变换器（SiT）**（Ma et al., ECCV 2024）的核心架构之上，通过引入一个轻量级的**VAE特征对齐组件**，在不依赖外部编码器或双模型维护的前提下，为扩散变换器训练提供内置视觉先验引导。

### 核心设计动机

扩散变换器训练面临的核心瓶颈在于：模型缺乏内置的视觉先验引导，导致收敛缓慢。现有的加速方法中，**REPA**（Yu et al., ICLR 2025）依赖外部表征编码器，**SRA**（Jiang et al., arXiv 2025）需要维护双模型结构，二者均引入了额外的计算开销和外部依赖。SRA 2 的关键洞察在于：预训练VAE在潜在扩散模型的第一阶段已经提取，其特征天然包含图像重构所需的纹理细节、结构模式和基本语义信息（如 Figure 2 所示），可直接被复用为训练引导信号，无需引入额外模型或增大计算开销。

### Pipeline 模块与数据流

SRA 2 的训练流程包含以下核心模块，其数据流为：

1. **VAE特征提取（离线预提取）**：对于输入图像 $\pmb{x} \in \mathbb{R}^{3 \times 256 \times 256}$，使用预训练的SD-VAE编码器提取潜在特征 $\pmb{f}_{\mathrm{VAE}} \in \mathbb{R}^{C \times H \times W}$（形状为 $4 \times 32 \times 32$）。这些特征在第二阶段扩散模型训练时通常已离线预提取，因此可被直接复用为对齐目标，**零额外引导特征提取成本**。

2. **SiT骨干网络（在线训练）**：图像经VAE编码后得到潜在表示 $\pmb{z}$，加入噪声后形成插值状态 $\pmb{y}_t = a_t \pmb{z} + b_t \pmb{\epsilon}$。SiT网络接收 $\pmb{y}_t$ 和时间步 $t$，预测速度场 $\pmb{v}_\phi(\pmb{y}_t, t)$，并通过去噪损失 $\mathcal{L}_\phi$ 进行优化：
   $$\mathcal{L}_\phi = \mathbb{E}_{t, z, \epsilon} \left[ \left\| v_\phi(y_t, t) - (\dot{a}_t z + \dot{b}_t \epsilon) \right\|^2 \right] dt$$

3. **轻量投影MLP（在线计算）**：在SiT的指定中间层（B架构为第2层，L/XL架构为第8层），将扩散潜在特征通过一个投影层进行非线性和维度变换，映射到VAE特征空间。消融实验表明，5层MLP达到最佳效果，2层MLP性能次优。

4. **特征对齐损失（Smooth L1）**：计算投影后SiT特征与VAE特征之间的逐元素Smooth L1损失，以最小化特征空间差异：
   $$\mathcal{L}_{\mathrm{align}} = \mathbb{E}_{z, \epsilon, t} \left[ \sum_{i=1}^{N} \begin{cases} \frac{1}{2\beta} (\Delta \pmb{f}_i)^2 & \text{if } |\Delta \pmb{f}_i| \leq \beta \\ |\Delta \pmb{f}_i| - \frac{\beta}{2} & \text{otherwise} \end{cases} \right]$$
   其中 $\Delta \pmb{f}_i$ 为投影特征与VAE特征在第 $i$ 个元素上的差异，$\beta$ 控制平滑过渡阈值。

5. **总训练目标**：去噪损失与对齐损失的加权组合：
   $$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_\phi + \lambda \cdot \mathcal{L}_{\mathrm{align}}$$
   消融实验表明，对齐损失权重 $\lambda = 1.0$ 在主要评估指标上达到最佳，全时间步范围 $t \in [0, 1]$ 优于部分时间步范围。

### 与现有范式的结构对比

Figure 3 清晰展示了四种训练范式的差异：

![[assets/figures/papers/paper_list_l935_https_arxiv_org_abs_2601_17830/figures/003_Figure_3.jpg]]
*Figure 3: Comparison of typical SiT training paradigms. (a) Vanilla SiT Training: Images are encoded by a VAE, added with noise, and processed by the diffusion model for denoising. (b) SiT Training with External Representation Alignment (e.g., REPA [47]): SiT training augmented with an external representative encoder and an MLP for alignment. (c) SiT Training with Dual-model Self-Alignment (e.g., SRA [20]): SiT training leveraging a dual-model setup with an MLP for self-alignment, guided by a teacher diffusion model. (d) SiT Training with VAE Representation Alignment (ours): SiT utilizes VAE features as representation guidance and an MLP for alignment, efficiently combining VAE’s semantic richness wi...*

- **(a) Vanilla SiT**：仅依靠去噪损失训练，无额外引导信号。
- **(b) 外部表征对齐（REPA）**：引入外部表征编码器和MLP进行特征对齐，增加外部模型依赖。
- **(c) 双模型自对齐（SRA）**：利用教师扩散模型进行自对齐，需维护双模型结构。
- **(d) VAE表征对齐（SRA 2，本文）**：直接复用VAE特征作为表征引导，仅需一个轻量MLP，**仅增加4%额外GFLOPs**，无外部编码器或双模型开销。

### 关键设计选择

- **对齐深度**：在SiT的浅层（B架构第2层）或中层（L/XL架构第8层）进行对齐效果最佳，这与浅层特征更易捕捉结构信息、深层特征更抽象的特性一致。
- **损失函数**：Smooth L1损失在所有对齐损失中取得最佳整体性能，因其对异常值具有更好的鲁棒性。
- **时间步范围**：全范围 $[0, 1]$ 优于部分范围，表明在不同噪声水平下均需要视觉先验引导。

> **注意**：关于对齐层和时步选择策略在不同扩散架构（如DiT）中是否需要调整，以及VAE特征对齐与外部表征对齐结合时的最佳整合方式，目前仍为开放问题。

SRA 2 在 SiT 扩散变换器训练框架之上引入一个轻量级的特征对齐组件，其核心由三个模块构成：VAE 特征复用、投影 MLP 与对齐损失、以及联合训练目标。整体架构如 Figure 3(d) 所示。

### VAE 特征复用

预训练的 SD-VAE 编码器在第一阶段已从原始图像中提取出潜在特征 $\\pmb{f}_{\\mathrm{VAE}} \\in \\mathbb{R}^{C \\times H \\times W}$（对于 3×256×256 输入图像，特征形状为 4×32×32）。这些特征天然保留了纹理细节、结构模式与基本语义信息（见 Figure 2），且在第二阶段扩散训练中通常已被离线预提取。SRA 2 直接复用这些预提取的 VAE 特征作为对齐目标，**无需引入额外编码器或维护双模型**，引导特征提取成本为零。

![[assets/figures/papers/paper_list_l935_https_arxiv_org_abs_2601_17830/figures/002_Figure_2.jpg]]
*Figure 2: We empirically visualize the feature information richness of SD-VAE [36] and SiT-XL/2 [29] via PCA [1]. Top: VAE features, extracted from original images by an SD-VAE encoder. Bottom: Latent features of SiT-XL/2 across different block layers and noise levels. We observe that SD-VAE features are significantly superior in delineating visual concepts compared to SiT’s latent representations, maintaining clearer details, structural integrity, and stronger semantic coherence. This motivates our use of VAE features for representation alignment*

### 投影 MLP 与对齐损失

在 SiT 的某一中间层（对齐深度），扩散潜在特征首先通过一个**轻量投影 MLP** 进行非线性与维度变换，将其映射到 VAE 特征空间。随后，计算投影后特征与目标 VAE 特征之间的逐元素差异，并采用 **Smooth L1 损失** 作为对齐目标：

$$
\mathcal{L}_{\mathrm{align}} = \mathbb{E}_{z,\epsilon,t}\left[ \sum_{i=1}^{N} 
\begin{cases} 
\frac{1}{2\beta}(\Delta \pmb{f}_i)^2 & \text{if } |\Delta \pmb{f}_i| \leq \beta \\
|\Delta \pmb{f}_i| - \frac{\beta}{2} & \text{otherwise}
\end{cases} 
\right]
$$

其中 $\Delta \pmb{f}_i$ 为投影 SiT 特征与 VAE 特征在第 $i$ 个元素上的差值，$\beta$ 为控制 L1 与 L2 过渡的阈值参数。消融实验表明，Smooth L1 损失在所有候选对齐损失中取得最佳整体性能（Table 1）。

### 联合训练目标

SRA 2 的总体训练目标为 SiT 原始速度预测损失与对齐损失的加权组合：

$$
\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\phi} + \lambda \cdot \mathcal{L}_{\mathrm{align}}
$$

其中 $\mathcal{L}_{\phi}$ 为 SiT 的去噪损失（速度预测的均方误差），$\lambda$ 为对齐损失权重。消融实验确定 $\lambda=1.0$ 在主要评估指标上达到最优（Table 1）。该设计仅增加约 4% 的额外 GFLOPs，且对齐损失仅在训练时计算，推理阶段无额外开销。

## 实验与关键发现

### 核心实验设置

SRA 2 的评估建立在 **SiT**（Ma et al., ECCV 2024）扩散变换器框架之上，覆盖类条件图像生成（ImageNet 256×256）和文本到图像生成（MS-COCO T2I）两类任务。对齐策略遵循消融实验确定的最优配置：在 B、L、XL 架构中分别将对齐应用于第 2、8、8 层，采用全时间步范围 $t \in [0, 1]$，对齐损失权重 $\lambda = 1.0$，投影 MLP 为 5 层结构，损失函数采用平滑 L1 损失。所有实验均复用预提取的 SD-VAE 特征，零额外引导特征提取成本。

### 主实验结果

**类条件生成质量。** 在 ImageNet 256×256 无分类器引导（no CFG）设置下，SiT-B/2 基线 FID 为 33.02，SRA 2 在最优对齐深度（层 2）下将 FID 降至 28.89，绝对降低 4.13，验证了 VAE 特征对齐对生成质量的显著提升（Table 1）。在带 CFG 的更大规模设置中，SiT-XL/2 + SRA 2 训练 800 epoch 后达到 FID 1.52，匹配或超越依赖外部模型的 **REPA**（Yu et al., ICLR 2025）等方法（Table 3）。

**训练收敛加速。** 跨训练迭代的 FID 对比（Table 2）表明，SRA 2 在相同训练步数下持续优于 vanilla SiT 和 vanilla REPA。Figure 4 的可视化进一步证实，SRA 2 在相同训练步数下生成图像具有更高的结构保真度、更精细的细节和更强的语义连贯性，收敛速度明显加快。

**文本到图像泛化。** 在 MS-COCO T2I 任务上，SRA 2 取得 FID 4.67 和 PickScore 20.92（Table 4），相比 vanilla SiT 实现生成性能的稳定提升，表明该方法对多模态条件生成任务具有良好的泛化能力。

### 消融实验分析

Table 1 系统消融了五个关键设计维度（均在 ImageNet 256×256 no CFG、SiT-B/2 400K 迭代下评估）：

![[assets/figures/papers/paper_list_l935_https_arxiv_org_abs_2601_17830/figures/004_Table_1.jpg]]
*Table 1: Ablation studies on ImageNet 256×256 without classifier-free guidance (CFG), which employs SiT-B/2 architectures trained for 400K iterations (with a batch size of 256). ↓ and ↑ indicate whether lower or higher values are better, respectively*

- **对齐深度：** 在 SiT-B/2 的 12 个变换器层中，层 2 取得最佳 FID 28.89，层 3 取得最佳 sFID 6.07。过浅或过深的对齐均导致性能退化，表明中间浅层特征与 VAE 表征的对齐最为关键。
- **时间步范围：** 全范围 $[0, 1]$ 优于任何部分范围，说明在高噪声和低噪声阶段同时进行表征对齐对训练均有增益。
- **损失函数：** 平滑 L1 损失在 FID、sFID、IS 和 Precision/Recall 等主要指标上取得最佳整体性能，优于 MSE 损失和余弦相似度损失。
- **损失权重：** $\lambda = 1.0$ 在主要评估指标上达到最佳平衡，过高或过低的权重均会损害生成质量。
- **投影 MLP 深度：** 5 层 MLP 达到最佳效果，2 层 MLP 次优，验证了适度的非线性变换能力对于弥合 SiT 潜在空间与 VAE 特征空间之间的差异是必要的。

### 计算开销分析

Table 5 对比了 REPA、**SRA**（Jiang et al., arXiv 2025）和 SRA 2 的训练计算开销。SRA 2 的外部前向参数（EFP）为零——因为 VAE 特征离线预提取，无需在训练循环中运行任何外部编码器或教师模型。相比之下，REPA 需额外加载 DINOv2 等外部编码器，SRA 需维护双模型教师网络。SRA 2 仅增加 4% 的 GFLOPs，且训练速度每批次仅略微下降，在计算效率与生成质量之间取得了最优权衡。

![[assets/figures/papers/paper_list_l935_https_arxiv_org_abs_2601_17830/figures/007_Table_5.jpg]]
*Table 5: Training computational computational cost comparison. This table compares REPA, SRA, and SRA 2 on ImageNet 256×256, detailing external forward parameters (EFP, formatted as external model parameters + MLP head parameters), training speed per batch (size 256) (TS), GFLOPs, and forward latency. Values in red parentheses indicate changes relative to the SiT-XL/2 baseline. These results were tested on H100 GPUs*

### 失败模式与局限性

当前实验未报告明确的失败模式，但存在以下需手动验证的点：在极高分辨率或极端域外场景下，预训练 VAE 特征的信息丰富度是否仍足以提供有效引导，尚缺乏实验证据。此外，SRA 2 在视频生成、3D 生成等缺乏成熟预训练 VAE 的领域是否有效，仍为开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l935_https_arxiv_org_abs_2601_17830/figures/006_Table_2.jpg]]
*Table 2: FID comparison across training iterations for accelerated alignment methods. All experiments are conducted on ImageNet (256×256) with a batch size of 256 and without CFG*

![[assets/figures/papers/paper_list_l935_https_arxiv_org_abs_2601_17830/figures/008_Table_4.jpg]]
*Table 4: Generalization to T2I Tasks. We find that SRA 2 also generalizes to T2I tasks, yielding improved generation performance*

## 定位与知识库关联

### 1. 问题定位：扩散变换器训练中的先验缺失与收敛瓶颈

扩散变换器（Diffusion Transformers, DiTs）已成为高分辨率视觉生成的主流架构，但其训练过程存在一个根本性瓶颈：模型缺乏内置的视觉先验引导，导致收敛缓慢。标准训练范式仅依赖去噪损失（在SiT框架中为速度预测损失），迫使模型从噪声中隐式学习视觉表征，这一过程需要大量训练迭代才能形成稳定的特征空间。

现有加速方法试图通过引入表征对齐信号来解决此问题，但均存在结构性缺陷：

- **外部表征对齐**：以 **REPA**（Yu et al., ICLR 2025）为代表，在训练中引入额外的预训练编码器（如DINOv2）提取图像表征，通过MLP投影层与扩散模型中间特征对齐。此方法虽能加速收敛，但引入了外部模型依赖，增加了前向传播的参数量和特征提取成本。

- **双模型自对齐**：以 **SRA**（Jiang et al., arXiv 2025）为代表，通过维护一个教师扩散模型来提供对齐目标。该方法避免了外部编码器，但需要同时维护两个扩散模型，导致训练开销翻倍。

- **VAE优化路径**：**VAVAE**（Yao et al., arXiv 2025）等尝试优化VAE本身以提升生成质量，但未直接解决扩散变换器训练的收敛效率问题。

- **掩码建模路径**：**MaskDiT**（Zheng et al., arXiv 2023）和 **SD-DiT**（Zhu et al., CVPR 2024）通过掩码建模策略引入自监督信号，但训练范式与标准扩散训练存在较大差异，通用性受限。

### 2. 核心洞察：预训练VAE特征作为“免费”视觉先验

SRA 2的关键洞察在于识别了一个常被忽视的事实：在潜在扩散模型的标准两阶段训练流程中，第一阶段预训练的VAE编码器已经提取了图像特征，这些特征天然包含丰富的纹理细节、结构模式和语义信息——这正是VAE重建任务所强制保留的内容。Figure 2的PCA可视化实证了这一观察：SD-VAE特征在描绘视觉概念方面显著优于SiT的潜在表征，保持了更清晰的细节、结构完整性和更强的语义连贯性。

更重要的是，由于这些VAE特征在第二阶段训练扩散模型时已经离线预提取，因此可以被直接复用为对齐目标，**零额外引导特征提取成本**。这一设计将“外部依赖”转化为“内部资源复用”，从根本上解决了REPA和SRA各自的核心缺陷。

### 3. 方法谱系中的定位

SRA 2在扩散变换器训练加速方法谱系中占据了一个独特位置：

| 维度 | Vanilla SiT | REPA | SRA | **SRA 2** |
|------|-------------|------|-----|-----------|
| 对齐信号来源 | 无 | 外部编码器 | 教师扩散模型 | 预训练VAE特征 |
| 外部依赖 | 无 | 有（DINOv2等） | 有（双模型） | 无 |
| 额外计算开销 | 基准 | 编码器前向+投影 | 教师模型前向+投影 | 仅投影MLP（4% GFLOPs） |
| 视觉先验质量 | 隐式学习 | 外部模型决定 | 扩散模型自身 | VAE重建特性保证 |

SRA 2的方法论贡献在于**将VAE从单纯的潜空间压缩工具重新定位为视觉先验的提供者**。这一视角转换使得对齐信号天然具备以下优势：
- **重建保真度**：VAE特征为重建目标而优化，包含像素级细节信息；
- **语义完整性**：VAE编码过程保留了类别级别的语义结构；
- **零成本获取**：特征已在标准训练流程中预提取，无需额外计算。

### 4. 适用边界与局限

基于现有证据，SRA 2的适用边界可归纳如下：

**已验证的适用范围**：
- 架构：SiT系列（B、L、XL规模），基于Scalable Interpolant Transformers框架；
- 任务：类别条件图像生成（ImageNet 256×256）和文本到图像生成（MS-COCO T2I）；
- 训练设置：支持无分类器引导（CFG）和带CFG的训练范式。

**潜在局限与开放问题**：

1. **跨架构泛化性未验证**：SRA 2在SiT上验证有效，但对其他扩散变换器架构（如标准DiT、U-ViT等）的适用性尚未报告。不同架构的中间特征空间结构可能影响对齐层深度的最优选择。

2. **VAE依赖性**：方法的核心前提是存在预训练的VAE编码器。在视频生成、3D生成等缺乏成熟预训练VAE的领域，SRA 2的直接迁移存在障碍。这是一个需要手动验证的开放问题。

3. **对齐层选择策略**：实验显示B、L、XL架构的最优对齐层分别为2、8、8层，但这一选择背后的理论依据尚不明确，可能依赖于具体架构的特征演化特性。

4. **与外部对齐的组合上限**：Figure 4显示SRA 2可与REPA叠加使用（REPA+SRA 2），但两者结合的最佳整合方式及性能上限尚未被系统探索。这暗示VAE特征对齐与外部表征对齐可能存在互补性，但需进一步研究确认。

5. **大规模扩展行为**：当前实验规模上限为SiT-XL/2（800 epochs），在更大规模模型和更长训练周期下的行为尚未报告。

### 5. 知识库贡献总结

SRA 2为扩散模型训练加速领域贡献了一个**零外部依赖、低计算开销**的解决方案。其核心方法论——复用预训练VAE特征作为内置视觉先验——填补了“完全无引导”与“外部模型引导”之间的空白。该方法在ImageNet 256×256上实现了FID 28.89（SiT-B/2, 无CFG），较基线降低4.13；在更大规模SiT-XL/2上达到FID 1.52（800 epochs, 带CFG），匹配或超越依赖外部模型的方法，同时仅增加4%的GFLOPs开销。

## 原文 PDF

![[paperPDFs/CVPR_2026/SRA_2_Variational_Autoencoder_Self_Representation_Alignment_for_Efficient_Diffusion_Training.pdf]]
