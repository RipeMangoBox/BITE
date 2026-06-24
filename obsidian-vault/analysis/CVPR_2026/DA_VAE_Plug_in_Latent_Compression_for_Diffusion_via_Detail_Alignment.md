---
title: "DA-VAE: Plug-in Latent Compression for Diffusion via Detail Alignment"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DA_VAE_Plug_in_Latent_Compression_for_Diffusion_via_Detail_Alignment.pdf
project_link: "https://caixin98.github.io/davae"
code_link: null
aliases:
- DVDAV
- DA-VAE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
core_operator: 结构化潜在空间设计（固定基础通道 + 额外细节通道）并通过细节对齐损失（Detail Alignment Loss）强制细节潜在与基础潜在共享结构，是实现高效微调的关键控制变量。
primary_logic: 利用预训练扩散模型已具备的结构化低维潜在空间，通过显式扩展通道维度并引入对齐约束，可在不破坏原有潜在结构的前提下提升压缩率，从而以极低的微调成本实现高分辨率生成。
claims:
- 细节对齐损失使细节潜在z_d的t-SNE可视化呈现清晰的类别可分性（Figure 3），表明其继承了基础潜在的结构信息。
- 消融实验显示，移除对齐损失后FID-10k从9.27退化至16.37（Table 5），零初始化对训练稳定性至关重要（无零初始化FID-10k升至29.73）。
- 在ImageNet 512×512上，本文方法在仅微调25个epoch的情况下FID-50k（w/ CFG）达到1.68，显著优于从零训练的LightningDiT-XL（3.12）（Table 1）。
- 在SD3.5 Medium上，方法实现1024×1024生成吞吐量提升4倍（1.03 vs 0.25 img/s）且CLIP Score更高（31.91 vs 29.74）（Table 3）。
---

# DA-VAE: Plug-in Latent Compression for Diffusion via Detail Alignment

> [!tip] 核心洞察
> 利用预训练扩散模型已具备的结构化低维潜在空间，通过显式扩展通道维度并引入对齐约束，可在不破坏原有潜在结构的前提下提升压缩率，从而以极低的微调成本实现高分辨率生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | DA-VAE：面向扩散模型的即插式潜空间压缩与细节对齐 |
| 英文题名 | DA-VAE: Plug-in Latent Compression for Diffusion via Detail Alignment |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.22125) · [Project](https://caixin98.github.io/davae) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/representation_self_supervised_transfer |
| Method | DA-VAE (Detail-Aligned VAE) |
| Dataset | ImageNet 512×512 class-conditional generation, MJHQ-30K (1024×1024) text-to-image, ImageNet 512×512 reconstruction |

> [!tip] 效果简介
> - ImageNet 512×512 class-conditional generation 上，FID-50k (w/ CFG) 1.68 vs 3.12 (LightningDiT-XL fine-tune with VA-VAE) (-1.44)。
> - MJHQ-30K (1024×1024) text-to-image 上，FID↓ 10.91 vs 10.31 (SD3.5-medium original 64×64 tokens) (+0.60 (with 4× speedup))；CLIP Score↑ 31.91 vs 29.74 (SD3.5-medium original) (+2.17)；Throughput (img/s, A100) 1.03 vs 0.25 (SD3.5-medium original) (+0.78 (4.12×))。
> - ImageNet 512×512 reconstruction 上，rFID↓ 0.47 vs 0.50 (VA-VAE) (-0.03)。

## 概述

扩散模型已成为视觉生成的主流范式，但其高分辨率生成的推理成本极高——以 **SD3.5 Medium**（Stability AI, 2024）为例，生成一张1024×1024图像需处理64×64个Token，吞吐量仅0.25 img/s（A100）。根本瓶颈在于：预训练扩散模型依赖标准VAE的固定压缩率，若直接提升VAE空间压缩率以减少Token数量，将导致潜在空间丧失语义结构，迫使扩散模型从零训练，代价巨大且浪费已有先验知识。因此，如何在降低Token数的同时保留预训练模型的生成能力，是亟待解决的核心问题。

**DA-VAE (Detail-Aligned VAE)** 针对上述瓶颈提出了一种即插即用的潜空间压缩方案。其核心思路是：将潜在空间显式结构化为“基础潜在 $\mathbf{z}$ + 细节潜在 $\mathbf{z}_d$”的通道拼接形式，其中前C通道直接继承预训练VAE的编码结果，后D通道编码高分辨率下新增的细节信息；通过**细节对齐损失**（Detail Alignment Loss）强制 $\mathbf{z}_d$ 的投影与 $\mathbf{z}$ 保持一致，使扩展后的潜在空间共享原有结构化属性，从而仅需对扩散Transformer进行轻量微调即可适配。该方法将压缩率提升与预训练先验保留解耦，控制变量在于结构化潜在空间设计与对齐约束的协同。

在**ImageNet 512×512**类别条件生成任务上，DA-VAE在仅微调25个epoch的条件下，FID-50k（w/ CFG）达到**1.68**，显著优于从零训练的**LightningDiT-XL**（3.12，Yao et al., 2024）和微调方案**DC-Gen-DiT-XL**（Chen et al., 2024）。在文本到图像生成任务上，基于SD3.5 Medium的DA-VAE将1024×1024生成的吞吐量提升**4倍**（1.03 vs 0.25 img/s），同时CLIP Score从29.74提升至**31.91**，MJHQ-30K FID仅微增至10.91（原10.31）。在2048×2048分辨率下，加速比更达**6.04倍**，适配仅需5 H100天。

消融实验揭示了方法的关键支撑：移除对齐损失后FID-10k从9.27恶化至**16.37**；零初始化对训练稳定性至关重要，移除后FID-10k升至**29.73**（完全失效）；温暖启动损失调度带来小幅增益。频率域分析证实细节潜在携带显著高频能量，与基础潜在互补而非冗余。

方法谱系上，DA-VAE区别于两类路线：一是从零训练的高压缩VAE（如**DC-AE**，Chen et al., 2024），虽压缩率高但丢失预训练先验；二是表示对齐VAE（如**VA-VAE**，Yao et al., 2024），虽保留结构但未针对扩散模型微调优化。DA-VAE在两者间取得折中：以结构化潜在空间继承预训练结构，以对齐损失约束细节通道，以零初始化和温暖启动调度保证微调稳定性，最终实现“高压缩率+低微调成本+高质量生成”的三元统一。

当前方法存在若干局限：对齐损失采用简单L2投影，可能非最优；仅在SD3.5 Medium上验证了LoRA微调，未在更大模型（如FLUX）上进行全微调测试；微调依赖合成数据集，可能影响生成图像的真实感；2048×2048分辨率的定量评估有限。这些为后续研究留下了明确空间。

## 背景与动机

### 扩散模型高分辨率生成的Token瓶颈

现代扩散模型（如Stable Diffusion 3.5、FLUX）依赖变分自编码器（VAE）将图像压缩至低维潜在空间，再通过DiT（Diffusion Transformer）进行生成建模。然而，当生成分辨率从512×512提升至1024×1024或更高时，潜在Token数量呈平方级增长——以SD3.5为例，其标准8倍下采样VAE在1024×1024分辨率下产生64×64个Token，导致Transformer的计算开销急剧膨胀。这一瓶颈直接制约了高分辨率生成的吞吐量：SD3.5 Medium在A100上生成1024×1024图像仅能达到0.25 img/s。

### 提升VAE压缩率的困境

直观的解决方案是提升VAE的下采样倍率（如从8倍增至16倍或32倍），从而减少Token数量。然而，这一策略面临两个关键障碍：

1. **高维潜在空间缺乏语义结构**：高压缩率VAE（如DC-AE，f32c32）产生的潜在空间往往不具备良好的语义组织性，扩散模型难以在其中学习有意义的分布。从零训练一个适配高压缩VAE的扩散模型（如LightningDiT-XL）不仅训练成本高昂，且生成质量（FID-50k 3.12）仍劣于标准Token预算下的预训练模型。

2. **预训练先验知识流失**：直接替换VAE意味着必须丢弃预训练扩散模型的权重，无法利用其已学到的丰富视觉先验。这对于文本到图像生成尤为致命，因为大规模预训练模型（如SD3.5）的语义理解能力是在海量图文数据上积累的。

### 现有方法的局限

当前应对高分辨率生成的主流策略可分为两类：

- **级联超分辨率**：先用扩散模型生成512×512图像，再通过独立的超分辨率网络（如SeedVR2、FMBoost）上采样至目标分辨率。这一方案虽能复用预训练模型，但级联架构割裂了全局语义与局部细节的联合建模，容易产生计数错误、结构失真等问题。

- **高压缩VAE + 从零训练**：如DC-Gen（Chen et al., 2024）和LightningDiT（Yao et al., 2024）采用更高压缩比的VAE，但需要从零训练或大规模微调扩散骨干网络，训练成本与质量之间难以兼顾。

### 核心动机与研究问题

本文的核心洞察在于：**预训练扩散模型已具备结构良好的低维潜在空间，若能以兼容的方式扩展该空间而非替换它，便可在保留预训练先验的同时提升压缩率**。具体而言，本文试图回答以下问题：

> 能否设计一种“即插式”的潜在压缩方案，使预训练扩散模型仅需轻量微调即可在高压缩率下生成高分辨率图像，同时保持甚至提升生成质量？

这一动机驱动了DA-VAE（Detail-Aligned VAE）的提出：通过结构化潜在空间设计（基础通道 + 细节通道）与细节对齐损失，在不破坏原有潜在结构的前提下实现Token压缩，从而以极低的微调成本（如SD3.5仅需5 H100天）获得4倍以上的生成加速。

## 核心创新

DA-VAE 的核心创新在于**结构化潜在空间设计 + 细节对齐机制 + 零初始化微调策略**的组合，使其能够以极低的训练成本（SD3.5 Medium 仅需 5 H100-days）将预训练扩散模型提升至高分辨率生成，同时保持甚至提升图像质量。

### 创新一：结构化潜在空间——基础与细节的显式分离

现有高压缩率 VAE（如 **DC-AE**，Chen et al., 2024）直接将图像编码为单一的高维潜在表示，导致潜在空间缺乏语义结构，扩散模型训练困难且需要从头训练。DA-VAE 提出了一种**显式的潜在布局**：

$$
\mathbf{z}_{\mathbf{hr}} = [\mathbf{z}, \mathbf{z}_d] \in \mathbb{R}^{(C+D)\times \frac{H}{f} \times \frac{W}{f}}
$$

其中：
- $\mathbf{z} = E(I)$：由**冻结的预训练 VAE 编码器** $E$ 从基础分辨率图像 $I$ 编码得到的基础潜在（$C$ 通道），保留了预训练模型已学到的语义结构；
- $\mathbf{z}_d = E_d(I_{hr})$：由**新增细节编码器** $E_d$ 从高分辨率图像 $I_{hr}$ 编码得到的细节潜在（$D$ 通道），编码高频细节信息。

这一设计的核心洞察在于：**基础潜在 $\mathbf{z}$ 作为"锚点"，为扩展的潜在空间提供了稳定的结构骨架**，使新增的细节通道不必从头学习全局语义，只需专注于编码互补的高频信息。频率分析（Figure S5）证实了细节潜在携带显著的高频能量，验证了其互补性而非冗余复制。

### 创新二：细节对齐损失——强制结构继承

仅靠重建损失训练细节编码器，会导致 $\mathbf{z}_d$ 与 $\mathbf{z}$ 的语义空间脱节。DA-VAE 引入**细节对齐损失**（Detail Alignment Loss）：

$$
\mathcal{L}_{\mathrm{align}} = \big\| \mathrm{Proj}(\mathbf{z}_d) - \mathbf{z} \big\|^2
$$

其中 $\mathrm{Proj}(\cdot)$ 是一个**无参投影算子**，通过通道分组均值将 $D$ 通道的细节潜在映射到 $C$ 通道：

$$
\mathrm{Proj}(\mathbf{z}_d)[i, h, w] = \frac{1}{r}\sum_{j=1}^{r} \mathbf{z}_d[ir+j, h, w], \quad r = D/C
$$

这一约束的因果效应在 Figure 3 中得到清晰验证：加入对齐损失后，$\mathbf{z}_d$ 的 t-SNE 可视化呈现**清晰的类别可分性**，表明细节潜在继承了基础潜在的语义结构；而无对齐时，细节特征退化为噪声残差。消融实验（Table 5）进一步量化了这一机制的重要性——移除对齐损失后，FID-10k 从 9.27 恶化至 16.37。

### 创新三：零初始化与温暖启动——保护预训练先验

将 DA-VAE 的结构化潜在接入预训练扩散 Transformer（如 DiT）时，面临一个关键挑战：新增细节通道的 Patch 嵌入层 $P'$ 和输出层 $O'$ 若随机初始化，会在训练初期破坏预训练模型的生成能力。DA-VAE 提出**零初始化**策略（Figure 2 右）：

> 保持基础潜在 $\mathbf{z}$ 路径的预训练权重不变，将 $P'$ 和 $O'$ 的权重初始化为零。

这使得训练开始时，细节通道的输出为零，模型完全等价于原始预训练扩散模型，从"良好起点"开始优化。Figure 4 的训练曲线对比显示，零初始化相比随机初始化收敛更快且更稳定；消融实验（Table 5）表明，移除零初始化后 FID-10k 飙升至 29.73，模型完全失效。

为进一步平滑训练，DA-VAE 引入**温暖启动损失调度**：

$$
w(n) = \begin{cases} \frac{1-\cos(\pi n / N_{\mathrm{warm}})}{2}, & n < N_{\mathrm{warm}} \\ 1, & n \ge N_{\mathrm{warm}} \end{cases}
$$

扩散损失中细节通道的预测误差通过 $w(n)$ 逐步增加权重，使训练早期梯度由基础潜在主导，确保与预训练主干的稳定对齐。该调度进一步将 FID-10k 从 9.27 提升至 9.80（Table 5），虽提升幅度较小，但对训练稳定性有辅助作用。

### 方法谱系与知识库定位

DA-VAE 处于**潜空间压缩 VAE + 扩散模型微调**的交叉点。与以下工作的关键区别：

| 方法 | 潜在空间设计 | 训练范式 | 核心局限 |
|------|------------|---------|---------|
| **SD-VAE** | 单一 8× 下采样潜在 | 预训练 | 高分辨率时 Token 数过多 |
| **DC-AE** (Chen et al., 2024) | 高压缩率单通道组 | 从头训练扩散模型 | 潜在空间缺乏语义结构，训练成本高 |
| **VA-VAE** (Yao et al., 2024) | 表示对齐的潜在空间 | 微调 | 未显式分离基础与细节通道 |
| **DA-VAE** (本文) | 结构化基础-细节分离 + 对齐约束 | 轻量微调（冻结基础路径） | 对齐机制可能非最优（L2 投影） |

DA-VAE 的独特贡献在于**将"保护预训练先验"作为第一性原理**：通过冻结基础编码器、零初始化新增参数、温暖启动调度三个机制，确保预训练扩散模型的核心能力在微调过程中不被破坏，从而以极低的计算成本（5 H100-days vs 从头训练的数百 GPU-days）实现高分辨率生成。

## 整体框架

DA-VAE 的整体设计围绕一个核心思想展开：**在不增加视觉 Token 数量的前提下，通过结构化潜在空间扩展来承载高分辨率图像的细节信息**。整个 pipeline 分为两个协同工作的阶段——结构化 VAE 训练和扩散 Transformer 微调，二者共享统一的潜在布局。

### 结构化潜在空间设计

DA-VAE 的潜在表示采用显式的双通道组拼接结构。给定一张高分辨率图像 $I_{hr}$，首先将其下采样至基础分辨率得到 $I$，然后通过两条编码路径分别提取：

- **基础潜在** $\mathbf{z} = E(I) \in \mathbb{R}^{C \times \frac{H}{f} \times \frac{W}{f}}$：由预训练 VAE 编码器 $E$（权重冻结）从低分辨率图像中提取，保留了原始 VAE 空间的全部语义结构。
- **细节潜在** $\mathbf{z}_d = E_d(I_{hr}) \in \mathbb{R}^{D \times \frac{H}{f} \times \frac{W}{f}}$：由新增的细节编码器 $E_d$ 从高分辨率原图中提取，承载基础分辨率无法捕获的高频纹理与细节。

两者沿通道维度拼接，构成结构化潜在表示：

$$\mathbf{z}_{\mathbf{hr}} = [\mathbf{z}, \mathbf{z}_d] \in \mathbb{R}^{(C+D)\times \frac{H}{f} \times \frac{W}{f}}$$

这一设计的巧妙之处在于：**空间分辨率保持不变（均为 $\frac{H}{f} \times \frac{W}{f}$），仅通过增加通道数来提升信息容量**，从而在不增加 Token 数量的前提下实现更高的压缩率。

### 细节对齐机制

直接让 $E_d$ 自由学习细节通道会导致 $\mathbf{z}_d$ 缺乏有意义的语义结构，使后续扩散模型训练困难。DA-VAE 引入了一个轻量级的**细节对齐损失**来解决这一问题：

$$\mathcal{L}_{\mathrm{align}} = \big\| \mathrm{Proj}(\mathbf{z}_d) - \mathbf{z} \big\|^2$$

其中 $\mathrm{Proj}(\cdot)$ 是一个无参数的通道分组均值投影算子，将 $D$ 通道的细节潜在映射到 $C$ 通道：

$$\mathrm{Proj}(\mathbf{z}_d)[i, h, w] = \frac{1}{r}\sum_{j=1}^{r} \mathbf{z}_d[ir+j, h, w], \quad r=D/C$$

该约束强制细节潜在的整体统计结构与基础潜在对齐，使得 $\mathbf{z}_d$ 继承了基础空间的语义组织方式（见图 3 的 t-SNE 可视化验证），同时仍保留编码高频细节的自由度。

### VAE 训练阶段

DA-VAE 的 VAE 部分训练仅涉及 $E_d$ 和解码器 $D$（$E$ 保持冻结），总损失为重建损失与对齐损失的加权和：

$$\mathcal{L} = \mathcal{L}_{\mathrm{rec}} + \lambda_{\mathrm{align}}\mathcal{L}_{\mathrm{align}}$$

其中 $\mathcal{L}_{\mathrm{rec}}$ 包含 LPIPS、L1、对抗损失和 KL 散度的标准组合。训练完成后，DA-VAE 能够以更少的 Token 数量（更高的空间压缩率）重建高分辨率图像，同时保持细节潜在与基础潜在的结构一致性。

### 扩散 Transformer 微调阶段

将预训练扩散模型适配到扩展后的结构化潜在空间时，DA-VAE 采用三项关键设计以确保训练稳定性和微调效率：

1. **零初始化**：对于新增细节通道对应的 Patch 嵌入层 $P'$ 和输出层 $O'$，权重初始化为零。这使得训练开始时细节通道的贡献为零，模型完全保留预训练扩散模型在基础分辨率上的生成能力（见图 2 右侧和图 4）。

2. **基础通道路径保持**：基础潜在 $\mathbf{z}$ 的 Patch 嵌入和输出层权重直接复用预训练参数，不做任何修改。

3. **温暖启动损失调度**：对细节通道的扩散预测损失施加余弦退火调度权重 $w(n)$，在训练早期逐步从 0 升至 1：

$$w(n) = \begin{cases} \frac{1-\cos(\pi n / N_{\mathrm{warm}})}{2}, & n < N_{\mathrm{warm}} \\ 1, & n \ge N_{\mathrm{warm}} \end{cases}$$

这使得扩散损失中细节通道的梯度贡献渐进增加：

$$\mathcal{L}_{\mathrm{DiT}}(n) = \frac{1}{|B|+w(n)|R|} \big( \|\hat{\mathbf{u}} - \mathbf{u}\|_2^2 + w(n) \|\hat{\mathbf{u}}_d - \mathbf{u}_d\|_2^2 \big)$$

### 输入输出流总结

整个 pipeline 的端到端流程如下：

- **输入**：高分辨率图像 $I_{hr}$（训练时）或随机噪声（推理时）
- **编码**：$E$ 从下采样图像提取 $\mathbf{z}$，$E_d$ 从原图提取 $\mathbf{z}_d$，拼接为 $\mathbf{z}_{\mathbf{hr}}$
- **扩散去噪**：DiT 在结构化潜在空间上进行去噪，预测噪声 $\hat{\mathbf{u}}$ 和 $\hat{\mathbf{u}}_d$
- **解码**：$D$ 从去噪后的结构化潜在重构高分辨率图像
- **输出**：与输入分辨率一致的高质量图像，但 Token 数量仅为原始 VAE 方案的 $1/4$（当空间压缩率翻倍时）

这种设计使得 DA-VAE 能够以**即插即用**的方式提升任意预训练扩散模型的分辨率上限：只需训练轻量的 $E_d$ 和微调 DiT 的新增通道参数（甚至可采用 LoRA 进一步降低开销，如 SD3.5 Medium 实验仅需 5 H100-天），即可在保持或超越原模型生成质量的同时获得数倍的推理加速。

### 补充图表

![[assets/figures/papers/paper_list_l852_https_arxiv_org_abs_2603_22125/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our method. Left: Illustration of our Detail-Aligned VAE (DA-VAE), which encodes a high-resolution image using the same number of visual tokens as the base image. Right: Zero initialization of the linear layer for detail latent. At the beginning of training, the model keep pretrained diffusion model capability of generating images at the base resolution*

![[assets/figures/papers/paper_list_l852_https_arxiv_org_abs_2603_22125/figures/001_Figure_1.jpg]]
*Figure 1: We propose Detail-Aligned VAE (DA-VAE), a VAE model that increases the compression rate of a pretrained VAE, while requiring only light-weight finetuning of the original diffusion backbone while preserving image quality. Image results are from a finetuned SD3.5 Medium. DA-VAE accelerates the original SD3.5 Medium model by 6.04 times for 2048 × 2048 image generation*

## 核心模块与公式推导

### 结构化潜在空间设计

DA-VAE 的核心创新在于构建了一个**结构化潜在空间**（structured latent space），将高分辨率图像的潜在表示沿通道维度显式拆分为两个互补部分：

$$
\mathbf{z}_{\mathbf{hr}} = [\mathbf{z}, \mathbf{z}_d] \in \mathbb{R}^{(C+D)\times \frac{H}{f} \times \frac{W}{f}} \tag{1}
$$

其中：

- **基础潜在** $\mathbf{z} = E(I) \in \mathbb{R}^{C \times \frac{H}{f} \times \frac{W}{f}}$：由预训练 VAE 的固定编码器 $E$ 从低分辨率图像 $I$ 编码得到，保留了原预训练模型已学到的语义结构化信息。
- **细节潜在** $\mathbf{z}_d = E_d(I_{hr}) \in \mathbb{R}^{D \times \frac{H}{f} \times \frac{W}{f}}$：由新增的细节编码器 $E_d$ 从高分辨率图像 $I_{hr}$ 编码得到，负责捕获高分辨率下额外涌现的细节信息。

这一设计的因果逻辑链为：**固定基础通道 → 保持预训练先验 → 扩展细节通道 → 提升压缩率**。通过将空间压缩率从 $f$ 提升至 $f'$（$f' > f$），同时增加通道数以补偿信息损失，DA-VAE 在保持相同视觉 Token 数量的前提下实现了更高的压缩率。

### 细节对齐损失

仅扩展通道维度会导致细节潜在 $\mathbf{z}_d$ 缺乏与基础潜在 $\mathbf{z}$ 一致的结构化语义，使扩散模型难以学习其分布。DA-VAE 引入**细节对齐损失**（Detail Alignment Loss）来解决这一瓶颈：

$$
\mathcal{L}_{\mathrm{align}} = \big\| \mathrm{Proj}(\mathbf{z}_d) - \mathbf{z} \big\|^2 \tag{3}
$$

投影算子 $\mathrm{Proj}$ 将 $D$ 通道的细节潜在映射到 $C$ 通道，通过通道分组均值实现无参映射：

$$
\mathrm{Proj}(\mathbf{z}_d)[i, h, w] = \frac{1}{r}\sum_{j=1}^{r} \mathbf{z}_d[ir+j, h, w], \quad r=D/C \tag{4}
$$

**核心机制**：该损失通过强制细节潜在在投影后与基础潜在一致，使 $\mathbf{z}_d$ 继承 $\mathbf{z}$ 的结构化语义属性。消融实验证实了这一设计的决定性作用——移除对齐损失后，FID-10k 从 9.27 退化至 16.37（Table 5），且 $\mathbf{z}_d$ 的 t-SNE 可视化失去类别可分性（Figure 3）。

### VAE 训练总损失

DA-VAE 的 VAE 部分训练损失为重建损失与对齐损失的加权组合：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{rec}} + \lambda_{\mathrm{align}}\mathcal{L}_{\mathrm{align}} \tag{6}
$$

其中重建损失 $\mathcal{L}_{\mathrm{rec}}$ 采用标准 VAE 的多项损失加权：

$$
\mathcal{L}_{\mathrm{rec}} = \lambda_{\mathrm{L}}\mathrm{LPIPS} + \lambda_{1}L_1 + \lambda_{\mathrm{adv}}\mathcal{L}_{\mathrm{adv}} + \lambda_{\mathrm{KL}}\mathcal{L}_{\mathrm{KL}}
$$

对齐损失权重 $\lambda_{\mathrm{align}}$ 控制重建-生成权衡：增大 $\lambda_{\mathrm{align}}$ 略微降低重建质量（rFID 上升、PSNR 下降），但显著提升生成质量（gFID 下降）。实验确定 $\lambda_{\mathrm{align}}=0.5$ 为最优折衷点（Table 4）。

### 扩散模型微调中的零初始化

在将结构化潜在接入预训练扩散 Transformer（DiT）时，DA-VAE 对新增细节通道的 Patch 嵌入层 $P'$ 和输出层 $O'$ 采用**零初始化**策略：

- 保持基础通道的 Patch 嵌入 $P$ 和输出层 $O$ 的预训练权重不变
- 将 $P'$ 和 $O'$ 的权重初始化为零，使其在训练初期输出为零

这一设计的因果机制为：**训练开始时，模型完全等价于原始预训练扩散模型**，仅对基础潜在 $\mathbf{z}$ 进行去噪，确保训练起点的稳定性。随着训练推进，细节通道的梯度逐渐激活，模型平滑地学习建模 $\mathbf{z}_d$ 的分布。Figure 4 的对比显示，零初始化相比随机初始化收敛更快、更稳定；移除零初始化后 FID-10k 恶化至 29.73，模型完全失效（Table 5）。

### 温暖启动损失调度

为进一步稳定训练，DA-VAE 对细节通道的扩散损失采用**余弦退火温暖启动调度**：

$$
w(n) = \begin{cases} \frac{1-\cos(\pi n / N_{\mathrm{warm}})}{2}, & n < N_{\mathrm{warm}} \\ 1, & n \ge N_{\mathrm{warm}} \end{cases} \tag{12}
$$

带调度的扩散损失为：

$$
\mathcal{L}_{\mathrm{DiT}}(n) = \frac{1}{|B|+w(n)|R|} \left( \|\hat{\mathbf{u}} - \mathbf{u}\|_2^2 + w(n) \|\hat{\mathbf{u}}_d - \mathbf{u}_d\|_2^2 \right) \tag{13}
$$

其中 $\hat{\mathbf{u}}$ 和 $\hat{\mathbf{u}}_d$ 分别为基础通道和细节通道的预测速度场，$\mathbf{u}$ 和 $\mathbf{u}_d$ 为对应的真实速度场，$|B|$ 和 $|R|$ 分别为基础通道和细节通道的 Token 数量。

**调度机制**：在训练初期（$n \ll N_{\mathrm{warm}}$），$w(n) \approx 0$，梯度主要由基础通道主导，模型保持与预训练骨干的对齐；随着训练推进，$w(n)$ 逐渐升至 1，模型逐步被迫学习细节通道 $\mathbf{z}_d$ 的分布。消融实验显示，温暖启动调度对生成质量有正向贡献（FID-10k 从 9.27 升至 9.80），但提升幅度相对对齐损失和零初始化较小（Table 5）。

### 补充图表

![[assets/figures/papers/paper_list_l852_https_arxiv_org_abs_2603_22125/figures/003_Figure_3.jpg]]
*Figure 3: Effect of the proposed latent alignment loss on the learned detail feature*

## 实验与分析

### 核心实验设计

DA-VAE的实验评估围绕两个核心维度展开：**压缩率提升带来的效率增益**与**生成质量的保持**。实验覆盖类条件生成（ImageNet 512×512）和文本到图像生成（MJHQ-30K 1024×1024/2048×2048）两大场景，重点验证以下因果链条：结构化潜在空间设计 → 细节对齐约束 → 零初始化微调 → 高压缩率下的质量保持。

实验的关键对照逻辑是：在相同Token预算（16×16）下，将DA-VAE的微调方案与从头训练的高压缩VAE方案进行对比，同时与原始预训练模型的高分辨率生成（64×64 Token）进行效率对比。

### 类条件生成：ImageNet 512×512

**Table 1** 给出了ImageNet 512×512类条件生成的核心结果。在仅微调25个epoch的条件下，DA-VAE + LightningDiT-XL取得FID-50k（w/ CFG）**1.68**，显著优于从零训练的LightningDiT-XL（3.12）和基于DC-AE的DC-Gen-DiT-XL（2.04）。值得注意的是，本文方法的训练成本远低于从头训练基线——仅需25 epoch微调，而DiT-XL从零训练需4000 epoch。

在无CFG设置下，DA-VAE的FID-50k为**4.84**，Inception Score达到**314.3**，同样优于所有对比方法。这一结果表明，结构化潜在空间设计使得预训练扩散模型的知识得以有效迁移，而非简单的高压缩率自编码器重建。

**Table 2** 进一步揭示了重建质量与生成质量之间的权衡关系。DA-VAE的rFID为0.47，略优于VA-VAE（0.50），但生成FID-10k（9.27）显著优于所有对比自编码器。这验证了核心洞察：细节对齐损失虽然轻微牺牲重建指标，但通过强制细节潜在继承基础潜在的结构信息，大幅提升了扩散模型的生成质量。

### 文本到图像生成：效率与质量

**Table 3** 展示了在SD3.5 Medium上的文本到图像生成结果，这是验证方法实用性的关键实验。在MJHQ-30K 1024×1024分辨率下，DA-VAE实现吞吐量**1.03 img/s**（A100），相比原始SD3.5 Medium的0.25 img/s提升约**4.12倍**。同时，CLIP Score从29.74提升至**31.91**，GenEval从0.62提升至0.64，表明压缩不仅未损害语义对齐，反而有所改善。

FID指标上，DA-VAE的10.91略高于原始SD3.5的10.31，但考虑到4倍吞吐量提升，这一微小退化是可接受的。与超分辨率后处理基线（**Table S.2**）的对比进一步表明，DA-VAE的联合建模优于级联方法：在相同512px SD3.5-M骨干下，DA-VAE的FID（10.91）显著低于SeedVR2（11.62）和FMBoost（11.65），且吞吐量匹配512px基线。

在2048×2048分辨率下（**Figure 1**），DA-VAE实现**6.04倍**加速，且定性结果（**Figure 7**）显示细节保真度明显优于SD3.5的上采样方案。整个SD3.5-M适配仅需**5 H100-days**，计算成本极低。

### 消融实验：因果机制的验证

消融实验是本文证据链的核心，直接验证了三个关键设计选择的因果作用。

**对齐损失权重（Table 4）**：λ_align从0增至1.0时，重建rFID从0.43升至0.54，但生成FID-10k从16.37降至9.27再升至10.40。λ_align=0.5时取得最佳权衡，验证了细节对齐对生成质量的关键作用。无对齐时FID-10k恶化至16.37，表明细节潜在若无结构约束，扩散模型难以有效建模。

**核心组件消融（Table 5）**：完整模型FID-10k为9.27。移除对齐损失后升至16.37（退化76.6%）；移除零初始化后飙升至**29.73**（完全失效）；移除温暖启动调度后升至9.80（小幅退化）。这一结果清晰地确立了因果层级：零初始化是训练稳定性的必要条件（无此则模型崩溃），对齐损失是生成质量的主要驱动因素，温暖启动调度提供额外收益。

**零初始化的训练动力学（Figure 4）**：零初始化使模型从预训练能力完好的起点出发，收敛更快且更稳定；随机初始化则导致早期训练混乱，最终性能显著恶化。

**细节潜在的互补性验证（Figure S2, Figure S5）**：解码器对细节潜在高度敏感——随机化/置零细节潜在导致重建rFID升至8.25/2.93（原0.47）。频率分析（**Figure S5**）显示细节潜在携带显著高频能量，证实其编码的是互补的细粒度信息，而非基础潜在的简单复制。

**对齐损失的可视化证据（Figure 3）**：t-SNE可视化显示，有对齐时细节潜在z_d呈现清晰的类别可分性，表明其继承了基础潜在的结构信息；无对齐时则退化为噪声残差。这一可视化直接支撑了“结构化潜在空间”的核心主张。

### 局限性与失败模式

尽管DA-VAE在效率和质量的权衡上表现出色，仍存在若干值得关注的局限：

1. **对齐机制的次优性**：当前L2投影对齐损失可能并非最优方案，存在更有效的结构化约束（如对比学习或互信息最大化）的探索空间。λ_align=0.5的最优值可能依赖于具体任务和模型规模。

2. **大规模模型验证缺失**：仅在SD3.5 Medium上采用LoRA微调，未验证在更大规模模型（如FLUX）上全微调的效果。FLUX等更大模型可能呈现不同的适配特性。

3. **合成数据偏差**：微调使用由基础模型生成的合成数据集，可能导致生成图像的真实感不如原生高分辨率模型。这在Table 3的FID轻微退化中有所体现。

4. **高分辨率定量评估不足**：2048×2048分辨率下的评估主要依赖定性展示（Figure 7），缺乏大规模定量指标。

5. **模态泛化未验证**：方法仅在图像生成任务上验证，未扩展到视频扩散模型或3D生成任务。

### 方法谱系与知识库定位

DA-VAE定位于**预训练扩散模型的高效压缩适配**这一研究脉络，与以下工作形成直接对照：

- **VA-VAE**（Yao et al., 2024）：同样追求表示对齐，但DA-VAE通过显式的结构化潜在空间设计和通道扩展机制，实现了更高的压缩率和更优的生成质量。
- **DC-AE**（Chen et al., 2024）：高压缩率自编码器，但需要从头训练扩散模型，而DA-VAE仅需轻量微调，保留了预训练先验。
- **SD-VAE**：标准8倍下采样VAE，DA-VAE在其基础上通过通道扩展和对齐约束实现压缩率翻倍。
- **LightningDiT-XL**（Yao et al., 2024）：基于VA-VAE的扩散模型，DA-VAE在相同Token预算下以微调方式超越其从头训练的性能。

DA-VAE的核心贡献在于揭示了**结构化潜在空间 + 对齐约束 + 零初始化微调**这一组合策略的有效性，为预训练扩散模型的高效高分辨率适配提供了新的范式。该方法的知识库定位可概括为：通过显式的潜在空间结构设计，将压缩率提升问题转化为通道扩展与对齐问题，从而以极低的微调成本实现预训练模型能力的迁移。

### 补充图表

![[assets/figures/papers/paper_list_l852_https_arxiv_org_abs_2603_22125/figures/005_Table_1.jpg]]
*Table 1: ImageNet 512 × 512 comparison in training regime, efficiency, and performance. Training Regime: Scratch trains the generator from random initialization for the target setting; Fine-tune starts from a pretrained generator (or a closely-related pretrained checkpoint) and adapts it to the target setting (e.g., resolution/tokenizer/architecture change). † indicates numbers are directly copied from the corresponding papers; ∗ follows the original paper’s from-scratch setting*

![[assets/figures/papers/paper_list_l852_https_arxiv_org_abs_2603_22125/figures/007_Table_2.jpg]]
*Table 2: Performance comparison of different autoencoders. All generation models were trained from scratch*

![[assets/figures/papers/paper_list_l852_https_arxiv_org_abs_2603_22125/figures/009_Table_3.jpg]]
*Table 3: Comparison of our method with SOTA approaches in efficiency and performance. FID and CLIP Score are reported on MJHQ-30K (1024×1024). Throughput is measured on a single A100 GPU (BF16, batch size 10). Data sources: the first five baselines (PixArt-Σ, Hunyuan-DiT, SANA-1.5, FLUX-dev, and SD3-medium) are copied from [44] under the same evaluation protocol*

![[assets/figures/papers/paper_list_l852_https_arxiv_org_abs_2603_22125/figures/010_Table_4.jpg]]
*Table 4: Ablation on alignment-loss weight. Increasing λalign slightly degrades reconstruction (higher rFID / LPIPS, lower PSNR / SSIM) but improves generation quality (lower gFID), with the best trade-off at a moderate weight*

![[assets/figures/papers/paper_list_l852_https_arxiv_org_abs_2603_22125/figures/011_Table_5.jpg]]
*Table 5: Ablation on three components. Our full model enables all three (✓); each ablation disables exactly one component (✗)*

![[assets/figures/papers/paper_list_l852_https_arxiv_org_abs_2603_22125/figures/012_Table_S.1.jpg]]
*Table S.1: Training and sampling hyperparameters for lightningDiT-XL and SD3.5-M*

![[assets/figures/papers/paper_list_l852_https_arxiv_org_abs_2603_22125/figures/014_Table.jpg]]
*Table: (a) Reconstruction metrics on the ImageNet validation set*

![[assets/figures/papers/paper_list_l852_https_arxiv_org_abs_2603_22125/figures/015_Figure_S.2.jpg]]
*Figure S.2: Ablation on detail channels in the DA-VAE decoder on ImageNet. (a) Reconstruction metrics for different decoder variants. (b) Visual examples showing that randomizing or zeroing the detail latent either destroys the image or removes fine-grained details such as faces and text. Please zoom in for best view*

![[assets/figures/papers/paper_list_l852_https_arxiv_org_abs_2603_22125/figures/019_Figure_S.5.jpg]]
*Figure S.5: Radial power spectrum of the base latent z and detail latent*

## 方法谱系与知识库定位

### 1. 核心问题与现有方法格局

扩散模型在高分辨率生成中的核心瓶颈在于Token数量随分辨率平方增长：以 **SD3.5 Medium**（Stability AI, 2024）为例，生成1024×1024图像需64×64个Token，导致推理吞吐量仅0.25 img/s（A100）。现有解决方案可归纳为三条技术路线：

- **高压缩率VAE + 从头训练**：如 **DC-AE**（Chen et al., 2024）将下采样率提升至f32，但高维潜在空间缺乏语义结构，迫使扩散模型从头训练，丧失了预训练先验。
- **表示对齐VAE + 微调**：如 **VA-VAE**（Yao et al., 2024）通过表示对齐约束提升压缩率，但仍需对扩散骨干进行较大幅度的微调，且生成质量与从头训练的 **LightningDiT-XL**（Yao et al., 2024）相比优势有限。
- **超分辨率后处理**：如 **SeedVR2**、**FMBoost** 等，在基础分辨率生成后级联超分模型。这种方式将生成与超分解耦，导致全局结构错误无法修正（如计数错误），且吞吐量受限于两级流水线。

DA-VAE的方法定位在于：**在保留预训练扩散骨干先验的前提下，通过结构化潜在空间设计实现Token压缩**，从而以极低的微调成本（SD3.5 Medium仅需5 H100-days）获得高分辨率生成能力。

### 2. 与基线方法的关键差异

#### 2.1 潜在空间结构设计

标准VAE（如 **SD-VAE**）使用单一通道组的潜在表示，缺乏对基础信息与细节信息的显式分离。**DC-AE**（Chen et al., 2024）虽提升了压缩率，但其潜在空间是“扁平”的——所有通道地位相同，扩散模型需从头学习其中的语义结构。**VA-VAE**（Yao et al., 2024）引入了表示对齐的概念，但未将潜在空间显式分割为基础通道与细节通道。

DA-VAE的核心创新在于**结构化潜在空间** $[\mathbf{z}, \mathbf{z}_d]$：
- 前 $C$ 通道 $\mathbf{z}$ 直接继承预训练VAE的基础潜在，保持与原有扩散模型的兼容性；
- 额外 $D$ 通道 $\mathbf{z}_d$ 编码高分辨率细节，通过**细节对齐损失** $\mathcal{L}_{\mathrm{align}} = \|\mathrm{Proj}(\mathbf{z}_d) - \mathbf{z}\|^2$ 强制其与基础潜在共享语义结构。

这一设计的因果效应在Figure 3中得到验证：加入对齐损失后，$\mathbf{z}_d$ 的t-SNE可视化呈现清晰的类别可分性，表明其继承了基础潜在的结构信息；而无对齐时细节特征退化为噪声残差。

#### 2.2 扩散模型适配策略

现有方法在适配扩散骨干时通常采用全参数微调或随机初始化新增参数。DA-VAE引入了两个关键设计：

- **零初始化**（Figure 2右）：对新增细节通道的Patch嵌入层 $P'$ 和输出层 $O'$ 进行零初始化，使得训练初期模型完全等价于预训练扩散模型，仅在基础通道上运行。消融实验（Table 5）显示，移除零初始化导致FID-10k从9.27恶化至29.73，模型完全失效。Figure 4进一步表明，零初始化使训练收敛速度显著快于随机初始化。

- **温暖启动损失调度**：细节通道的扩散损失通过余弦退火调度 $w(n)$ 逐步引入，早期训练步骤中 $w(n) \approx 0$，梯度由基础通道主导。这一设计确保扩散模型在稳定学习基础分布后，再逐步建模细节通道。消融显示该设计将FID-10k从9.27提升至9.80，贡献虽小于对齐损失和零初始化，但进一步稳定了训练。

#### 2.3 与超分辨率路线的本质区别

Table S2的对比揭示了DA-VAE与超分辨率后处理的根本差异：在计数任务中，512px基础生成已出现计数错误，超分方法无法修正；而DA-VAE通过联合建模基础与细节通道，在生成过程中即可纠正全局语义错误。此外，DA-VAE的吞吐量（1.03 img/s @ 1024×1024）与512px基线（1.05 img/s）持平，避免了级联流水线的开销。

### 3. 适用边界与局限

#### 3.1 已验证的适用场景

- **类别条件生成**（ImageNet 512×512）：在16×16 Token预算下，FID-50k（w/ CFG）达1.68，显著优于从头训练的LightningDiT-XL（3.12），验证了方法在中等分辨率条件生成中的有效性。
- **文本到图像生成**（1024×1024, 2048×2048）：在SD3.5 Medium上实现4倍吞吐量提升（1.03 vs 0.25 img/s），CLIP Score从29.74提升至31.91，FID仅轻微退化（10.91 vs 10.31）。
- **即插即用性**：方法仅需微调扩散骨干的Patch嵌入层和输出层（SD3.5 Medium上采用LoRA），无需修改VAE解码器或扩散Transformer主体。

#### 3.2 已知局限

1. **对齐损失的最优性**：当前采用的L2投影对齐 $\|\mathrm{Proj}(\mathbf{z}_d) - \mathbf{z}\|^2$ 可能并非最优结构化约束。是否存在对比学习、互信息最大化等更强的对齐机制，仍是开放问题。

2. **大规模模型验证不足**：仅在SD3.5 Medium（~2.5B参数）上采用LoRA微调，未在更大规模模型（如 **FLUX-dev**，Black Forest Labs, 2024）上进行全微调验证。方法在大模型上的扩展性和收益尚不明确。

3. **训练数据偏差**：微调使用合成数据集（由基础模型生成），可能导致生成图像的真实感不如原生SD3.5。这在Table 3的FID轻微退化中有所体现。

4. **极高分辨率评估缺失**：2048×2048分辨率下的定量评估有限，主要依赖定性展示（Figure 7）。6.04倍加速的声明（Figure 1）需要更多定量指标支撑。

5. **模态泛化性未知**：方法未在视频扩散模型、3D生成等任务上验证。结构化潜在空间设计是否适用于时序或空间一致的潜在表示，需要进一步探索。

### 4. 开放问题

1. **最优对齐机制**：L2投影的替代方案（如对比对齐、最优传输、信息瓶颈）能否在保持重建质量的同时进一步提升生成质量？

2. **温暖启动调度的敏感性**：$N_{\mathrm{warm}}$ 超参数对最终性能的影响程度如何？是否存在自适应调度策略？

3. **多尺度扩展**：能否堆叠多层细节通道（如 $[\mathbf{z}, \mathbf{z}_{d1}, \mathbf{z}_{d2}]$）实现多级压缩率，以支持从512到4096的连续分辨率缩放？

4. **与其他压缩范式的结合**：结构化潜在空间能否与Token剪枝、KV-cache压缩等推理加速技术协同，实现更大的吞吐量提升？

5. **无条件生成与下游任务**：方法在无条件生成、图像编辑、可控生成等任务中的表现如何？结构化潜在是否影响可编辑性？

### 5. 知识库定位

DA-VAE处于**扩散模型高效推理**与**表示学习**的交叉点，与以下工作脉络直接相关：

- **高压缩率自编码器**：DC-AE（Chen et al., 2024）、VA-VAE（Yao et al., 2024）等探索了提升VAE压缩率的路径，但未解决潜在空间结构化问题。
- **扩散模型微调范式**：LoRA、Adapter等参数高效微调方法关注模型适配，DA-VAE则从潜在空间设计角度降低了适配难度。
- **表示对齐学习**：对比学习、知识蒸馏中的表示对齐思想被DA-VAE以轻量投影对齐的形式引入潜在空间设计。

方法的本质贡献在于**通过潜在空间的显式结构化，将“提升压缩率”与“保留预训练先验”这两个冲突目标解耦**，为扩散模型的高效高分辨率生成提供了新的设计范式。

## 原文 PDF

![[paperPDFs/CVPR_2026/DA_VAE_Plug_in_Latent_Compression_for_Diffusion_via_Detail_Alignment.pdf]]