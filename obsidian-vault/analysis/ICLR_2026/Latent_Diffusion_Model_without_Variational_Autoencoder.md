---
title: "Latent Diffusion Model without Variational Autoencoder"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Latent_Diffusion_Model_without_Variational_Autoencoder.pdf
project_link: https://howlin-wang.github.io/svg
code_link: https://github.com/shiml20/SVG
aliases:
- LDMWVA
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "利用自监督视觉基础模型（DINOv3）的强判别性特征构造潜在空间，并加入轻量残差编码器补充细粒度感知细节，同时在训练时对齐残差特征分布以保持语义结构，从而在无需VAE的情况下实现高效扩散训练和多任务特征复用。"
primary_logic: "具有良好语义分离性的潜在空间可大幅简化扩散模型的优化难度，使得模型在更少训练轮次和采样步数下达到更高质量；同时，这种空间继承了自监督特征的感知理解能力，为构建任务通用的视觉表示提供了可行路径。"
claims:
- "VAE潜在空间语义高度混合，DINOv3特征空间类间分离清晰。"
- "在语义分散的空间中，平均速度方向在类内一致、类间分离，简化优化并减少所需采样步数。"
- "SVG在80个训练epoch、25步采样下即达到gFID 3.54（w/ CFG），显著优于传统VAE扩散模型，且训练收敛更快。"
- "去除残差编码器的分布对齐导致生成FID从6.12升至9.03，验证了分布对齐对维持语义结构的关键作用。"
---

# Latent Diffusion Model without Variational Autoencoder

> [!tip] 核心洞察
> 具有良好语义分离性的潜在空间可大幅简化扩散模型的优化难度，使得模型在更少训练轮次和采样步数下达到更高质量；同时，这种空间继承了自监督特征的感知理解能力，为构建任务通用的视觉表示提供了可行路径。

| 字段 | 内容 |
|------|------|
| 中文题名 | 无需变分自编码器的潜在扩散模型 |
| 英文题名 | Latent Diffusion Model without Variational Autoencoder |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://arxiv.org/abs/2510.15301) · [Project](https://howlin-wang.github.io/svg) · [Code](https://github.com/shiml20/SVG) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | SVG |
| Dataset | ImageNet 256×256 |

> [!tip] 效果简介
> - ImageNet 256×256 上，gFID (w/ CFG, 25 steps) 3.54 (SVG-XL, 80 epochs) vs 22.58 (SiT-XL†, SD-VAE, 25 steps) (-19.04)；gFID (w/o CFG, 25 steps) 6.57 (SVG-XL, 80 epochs) vs 22.58 (SiT-XL†, SD-VAE, 25 steps) (-16.01)。
> - ImageNet 256×256 (few-step, 5 steps) 上，FID-50K w/o CFG 12.26 (SVG-XL) vs 69.38 (SiT-XL, SD-VAE) (-57.12)。
> - ImageNet 256×256 (few-step, 10 steps) 上，FID-50K w/o CFG 9.39 (SVG-XL) vs 32.81 (SiT-XL, SD-VAE) (-23.42)。

## 概要

扩散模型已成为视觉生成的主流范式，但现有方法普遍依赖变分自编码器（VAE）将图像压缩至低维潜在空间以降低计算成本。这一设计存在根本性瓶颈：**VAE潜在空间存在严重的语义纠缠，缺乏清晰的判别结构**，导致扩散模型训练效率低下、推理步数多，且难以作为统一视觉特征空间服务于多种任务。

针对上述问题，本文提出**SVG（Semantic Vision Generation）**——一种无需VAE的潜在扩散模型。其核心洞察在于：**具有良好语义分离性的潜在空间可大幅简化扩散模型的优化难度**，使模型在更少训练轮次和采样步数下达到更高质量；同时，该空间继承了自监督特征的感知理解能力，为构建任务通用的视觉表示提供了可行路径。

在方法定位上，SVG区别于三类现有方案：一是传统的VAE潜在扩散模型（如**DiT-XL**（Peebles & Xie, 2022）、**SiT-XL**（Ma et al., 2024）），它们依赖VAE压缩但受限于语义纠缠；二是扩散模型特征对齐方法（如**REPA-XL**（Yu et al., 2025）），仅在扩散模型中间层对齐视觉基础模型特征，未改变潜在空间本身；三是VAE与扩散模型联合对齐方法（如**SiT-XL with VA-VAE**（Yao et al., 2025）），虽对齐了VAE潜在特征，但仍保留VAE框架。SVG则直接利用自监督视觉基础模型（DINOv3）的强判别性特征构造潜在空间，并加入轻量残差编码器补充细粒度感知细节，在无需VAE的情况下实现高效扩散训练和多任务特征复用。

实验结果表明，SVG在ImageNet 256×256类条件生成任务上展现出显著优势：**SVG-XL仅需80个训练epoch、25步采样即达到gFID 3.54（w/ CFG）**，远优于同等条件下的SiT-XL（gFID 22.58）；在少步采样场景下，5步FID-50K仅为12.26，而SiT-XL高达69.38。此外，SVG特征在下游感知任务（ImageNet分类、ADE20K分割、NYUv2深度估计）上保持与DINO相比拟的性能，验证了其作为统一视觉特征空间的潜力。

### 潜在扩散模型的成功与隐忧

潜在扩散模型（Latent Diffusion Models, LDMs）已成为高分辨率视觉生成的主流范式。其核心策略是将扩散过程从高维像素空间迁移至低维潜在空间，从而大幅降低计算开销。这一范式的成功高度依赖于变分自编码器（VAE）提供的压缩表示。然而，**传统VAE潜在空间存在严重的语义纠缠**：特征在空间中高度混合，缺乏清晰的判别结构。这一瓶颈直接导致扩散模型训练效率低下——模型需要大量迭代才能理清混乱的语义关系，且推理时需要较多采样步数才能生成高质量图像。

更深层的问题在于，VAE潜在空间仅服务于“压缩-重建”目标，**难以作为统一的视觉特征空间支撑多种任务**。生成模型学到的表示与识别、分割等感知任务所需的结构化语义存在根本性鸿沟，使得生成模型与视觉理解模型长期处于割裂状态。

### 现有改进路线的局限

为弥合这一鸿沟，近期工作尝试将扩散模型的特征与视觉基础模型（Visual Foundation Models, VFMs）对齐。这些努力可归纳为两条技术路线：

- **扩散模型内部特征对齐**：在扩散模型训练过程中，将其中间层特征与VFM特征对齐（如**REPA**，Yu et al., 2025）。该方法虽能增强生成特征的语义性，但扩散模型仍需在语义混杂的VAE潜在空间上运行，未能从根本上解决瓶颈。
- **VAE与扩散模型联合对齐**：将VAE潜在特征和扩散模型中间特征同时向VFM特征对齐（如**VA-VAE**配合SiT，Yao et al., 2025）。这一方案部分改善了VAE空间的语义结构，但VAE自身的重建约束限制了其语义判别能力的上限。

上述方法的共同局限在于：**它们始终保留VAE作为潜在空间的构造基础**，仅通过外部对齐来“弥补”语义缺陷，而非直接从源头构建具有判别性的特征空间。

### 核心动机：从语义结构出发重构生成空间

本文的核心洞察是：**具有良好语义分离性的潜在空间可大幅简化扩散模型的优化难度**。当特征空间中不同语义类别的样本自然分离时，扩散模型的概率流方向在类内趋于一致、在类间彼此远离（见Figure 4b的Toy Example）。这种结构化特性使得模型能以更少的训练轮次和采样步数达到更高质量。

基于此，本文提出一个根本性转变：**放弃VAE，直接利用自监督视觉基础模型的强判别性特征构造潜在空间**。具体而言，SVG以冻结的DINOv3编码器为核心，其深层特征天然具有清晰的类间分离（Figure 4a的t-SNE可视化证实，DINOv3空间的语义结构远优于SD-VAE和VA-VAE）。同时，为弥补DINO特征在细粒度感知细节（颜色、高频纹理等）上的不足，引入轻量残差编码器进行补充，并通过分布对齐机制保持语义结构不被破坏。

这一设计使得SVG空间同时继承了自监督特征的感知理解能力与重建所需的细节保真度，**为构建任务通用的视觉表示提供了可行路径**——扩散模型可直接在此空间上高效训练，且该空间可复用于分类、分割、深度估计等下游任务。

## 核心方法与创新机理

SVG 的核心创新在于**彻底摒弃了传统潜在扩散模型中依赖变分自编码器（VAE）进行压缩的范式**，转而构建一个基于自监督视觉基础模型（VFM）的、具有清晰语义判别结构的统一特征空间，并直接在该空间上训练扩散模型。这一转变并非简单的编码器替换，而是对潜在空间语义属性的根本性重塑，其关键创新体现在以下三个紧密耦合的层面。

### 1. 从“感知压缩”到“语义结构化”的范式转换

传统 LDM 的瓶颈在于 VAE 潜在空间存在严重的语义纠缠（Figure 4a 的 t-SNE 可视化清晰显示 SD-VAE 等潜在空间中不同类别样本高度混合）。这种缺乏判别结构的空间迫使扩散模型在训练时需额外学习解耦语义，导致优化困难、收敛缓慢且需要大量采样步数。SVG 的核心洞察是：**一个具有良好语义分离性的潜在空间可以大幅简化扩散模型的优化难度**。为此，SVG 直接利用冻结的 DINOv3 编码器提取具有强语义判别性的特征作为潜在空间的基础。DINOv3 特征空间中类间分离清晰、类内紧凑（Figure 4a），这种结构使得扩散模型中的平均速度方向在类内一致、类间分离（Figure 4b），从而显著降低了生成模型的训练难度，使得少步数采样成为可能。

### 2. 轻量残差编码器与分布对齐机制

仅使用 DINOv3 特征虽能获得强语义性，但会丢失细粒度感知细节（如颜色、高频纹理），导致重建质量严重下降。SVG 的解决方案是引入一个**轻量级残差编码器**（Residual Encoder，基于 ViT 构建）来捕获 DINO 特征缺失的感知信息，并将其输出沿通道维与 DINO 特征拼接形成完整的 SVG 特征（Figure 3）。

然而，简单的拼接会破坏 DINO 特征原有的语义结构。SVG 的关键设计在于**残差特征分布对齐**：通过批次统计将残差特征归一化到与 DINO 特征相同的分布，公式为：

$$\hat{F}_R = \frac{F_R - \mu(F_R)}{\sigma(F_R)} \cdot \sigma(F_D) + \mu(F_D)$$

该操作使得残差信息在补充感知细节的同时，不会扰乱 DINO 特征空间固有的语义判别结构。消融实验（Table 4）强有力地验证了这一设计的必要性：移除分布对齐后，生成 gFID 从 6.12 急剧恶化至 9.03，证明了维持语义结构对扩散模型训练的关键作用。

### 3. 高维语义空间上的高效扩散训练

SVG 将扩散模型直接部署在由 DINO 特征和残差特征拼接而成的高维语义空间上（如 $16\times16\times384$），而非传统 VAE 的低维压缩空间（如 $16\times16\times4$）。在这一空间中，SVG 采用流匹配（Flow Matching）目标训练扩散模型，并应用 QK-Norm 和逐通道归一化来稳定训练过程。得益于潜在空间的语义结构化特性，SVG 在极少的训练轮次和采样步数下即可达到卓越的生成质量：SVG-XL 仅需 **80 个训练 epoch、25 步采样**即可达到 gFID 3.54（w/ CFG），而传统 VAE 扩散模型（如 SiT-XL with SD-VAE）在相同步数下 gFID 高达 22.58（Table 1）。在更极端的 5 步采样设置下，SVG-XL 的 FID 为 12.26，而 SiT-XL 为 69.38（Table 2a），差距达 57.12。这充分验证了语义结构化空间对扩散模型优化难度的根本性降低。

### 关键改动槽位总结

| 改动槽位 | 基线方案 | SVG 方案 | 证据锚点 |
|---------|---------|---------|---------|
| 潜在空间编码器 | 标准 VAE 编码器（如 SD-VAE） | 冻结 DINOv3 + 轻量残差编码器 | Section 3.3, Figure 3 |
| 残差特征整合 | 无（仅 VAE 特征） | 通道拼接 + 批次统计分布对齐（公式 6） | Equation (6), Table 4 |
| 扩散模型训练目标 | 噪声/速度预测（DiT, SiT） | 在 SVG 高维语义空间上使用流匹配 + QK-Norm | Section 3.3 |
| 特征空间维度 | 低维 VAE 潜在空间（如 16×16×4） | 高维语义空间（如 16×16×384） | Table 1 note |

### 统一特征空间的延伸价值

SVG 的另一重要创新在于其构建的特征空间**继承了自监督特征的感知理解能力**，具备作为任务通用视觉表示的潜力。实验表明，SVG 特征在 ImageNet 分类、ADE20K 分割和 NYUv2 深度估计等下游任务上保持了与 DINO 相比拟的性能（Table 4），并支持零样本类别条件编辑（Figure 6）和潜在空间插值（Figure 7）等应用。这使得 SVG 不仅是一个生成模型，更是一个向统一视觉特征空间迈进的框架。

SVG 的整体框架围绕一个核心设计展开：**用自监督视觉基础模型（DINOv3）的强语义判别性特征空间，替代传统 VAE 的潜在空间，作为扩散模型的生成空间**。这一设计解决了 VAE 潜在空间中语义高度纠缠、缺乏清晰判别结构的瓶颈问题。

### Pipeline 总览

SVG 的 pipeline 由两大阶段串联而成：

1. **SVG 自编码器（SVG Autoencoder）**：将输入图像映射到一个兼具语义判别性和细粒度感知细节的 SVG 特征空间，并能从该空间解码回像素空间。
2. **SVG 扩散模型（SVG Diffusion）**：直接在 SVG 特征空间上训练流匹配（Flow Matching）扩散模型，实现高效生成。

### 模块关系与数据流

如图 Figure 3 所示，SVG 自编码器由以下模块构成，数据流严格按序传递：

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2510_15301/figures/003_Figure_3.jpg]]
*Figure 3: Architecture of the proposed SVG Autoencoder. The model augments the DINO encoder with a Residual Encoder to achieve high-quality reconstruction and preserve transferability*

| 模块 | 角色 | 输入 → 输出 |
|------|------|-------------|
| **Frozen DINOv3 Encoder** | 提取具有强语义判别性的基础特征 | 原始图像 → DINO 语义特征 $F_D$ |
| **Residual Encoder** | 轻量级 ViT，捕获 DINO 特征缺失的细粒度感知细节（如颜色、高频纹理） | 原始图像 → 残差特征 $F_R$ |
| **Feature Concatenation & Alignment** | 将残差特征与 DINO 特征沿通道维拼接，并通过批次统计对齐（公式 6）维持语义结构 | $F_D, F_R$ → 对齐后的 SVG 特征 |
| **SVG Decoder** | 将 SVG 特征解码回像素空间，训练时使用重建损失 | SVG 特征 → 重建图像 |

其中，**分布对齐（Alignment）** 是关键的因果调节旋钮。消融实验表明，移除该对齐（即直接拼接）会导致生成 gFID 从 6.12 恶化到 9.03（Table 4），验证了其维持语义结构、保障扩散训练有效性的核心作用。

### 扩散模型训练

SVG 扩散模型在 SVG 特征空间上训练，采用流匹配目标（公式 5）：

$$\mathcal{L}_{\mathrm{FM}} = \mathbb{E}_{\mathbf{x}_0 \sim p_0(\mathbf{x}), \epsilon \sim p_1(\mathbf{x})} [\lambda(t) \lVert \mathbf{v}_{\theta}(\mathbf{x}_t, t) - \mathbf{v}_t \rVert]$$

训练设置严格遵循 SiT（Ma et al., 2024），但将嵌入层修改以适配 SVG 的高维特征空间（如 $16\times16\times384$）。同时应用 QK-Norm 和逐通道归一化以稳定训练。

### 核心洞察

该框架的根本优势在于：**语义分离性良好的潜在空间大幅简化了扩散模型的优化难度**。在语义分散的空间中，平均速度方向在类内一致、类间分离（Figure 4b），使得模型在更少训练轮次（80 epochs）和采样步数（25 steps）下即可达到高质量生成——SVG-XL 在 25 步、80 epoch 下即达到 gFID 3.54（w/ CFG），显著优于传统 VAE 扩散模型（Table 1）。同时，该空间继承了 DINOv3 的感知理解能力，为构建任务通用的视觉表示提供了可行路径。

### 1. 扩散与流匹配基础

SVG的生成模型建立在连续时间扩散与流匹配框架之上。给定数据分布 $p_0(\mathbf{x})$ 与噪声分布 $p_1(\mathbf{x})$，前向扩散过程通过信噪比调度 $\alpha_t$、$\sigma_t$ 将数据逐渐加噪：

$$\mathbf{x}_t = \alpha_t \mathbf{x}_0 + \sigma_t \epsilon, \quad t \in [0,1], \quad \epsilon \sim \mathcal{N}(0,\mathbf{I}) \tag{1}$$

其中 $t=0$ 对应干净数据，$t=1$ 对应纯噪声。去噪扩散模型（DDPM）的训练目标为预测添加的噪声：

$$\mathcal{L}_{\mathrm{DDPM}} = \mathbb{E}_{\mathbf{x}_0 \sim p_0(\mathbf{x}), \epsilon \sim p_1(\mathbf{x})} [\lambda(t) ||\epsilon_{\theta}(\mathbf{x}_t, t) - \epsilon_t||] \tag{2}$$

SVG实际采用流匹配（Flow Matching）范式，将前向过程定义为数据与噪声的线性插值：

$$\mathbf{x}_t = (1-t)\mathbf{x}_0 + t\epsilon, \quad t \in [0,1], \quad \epsilon \sim \mathcal{N}(0,\mathbf{I}) \tag{3}$$

对应的目标速度场为：

$$\mathbf{v}_t \triangleq \frac{\mathrm{d}\mathbf{x}_t}{\mathrm{d}t} = \epsilon - \mathbf{x}_0 \tag{4}$$

流匹配的训练损失直接回归该速度场：

$$\mathcal{L}_{\mathrm{FM}} = \mathbb{E}_{\mathbf{x}_0 \sim p_0(\mathbf{x}), \epsilon \sim p_1(\mathbf{x})} [\lambda(t) \lVert \mathbf{v}_{\theta}(\mathbf{x}_t, t) - \mathbf{v}_t \rVert] \tag{5}$$

在SVG中，上述公式中的 $\mathbf{x}_0$ 并非原始像素，而是经过SVG编码器提取的高维语义特征。扩散模型训练遵循SiT（Ma et al., 2024）的设置，应用QK-Norm并在逐通道对SVG特征空间进行归一化以稳定训练。

### 2. SVG自编码器核心模块

SVG自编码器由三个核心组件构成（Figure 3），共同构建具有强语义判别性的潜在空间。

**冻结DINOv3编码器（Frozen DINOv3 Encoder）**：直接复用预训练的DINOv3模型作为特征提取骨干，提供具有清晰类间分离和类内紧凑性的基础语义特征。该编码器在整个训练过程中保持冻结，确保语义结构不被生成任务破坏。

**残差编码器（Residual Encoder）**：一个轻量级Vision Transformer，专门捕获DINO特征中缺失的细粒度感知细节（如颜色、纹理、高频信息）。其输出与DINO特征沿通道维度拼接，形成完整的SVG特征表示。Figure 5的消融可视化表明，缺少残差编码器时重建图像会丢失大量视觉细节。

**残差特征分布对齐（Feature Alignment）**：直接将残差特征与DINO特征拼接会引入分布不匹配，破坏语义结构并损害扩散模型训练。SVG通过批次统计归一化将残差特征对齐到DINO特征的分布：

$$\hat{F}_R = \frac{F_R - \mu(F_R)}{\sigma(F_R)} \cdot \sigma(F_D) + \mu(F_D) \tag{6}$$

其中 $F_D$ 为DINO特征，$F_R$ 为残差编码器输出，$\mu(\cdot)$ 和 $\sigma(\cdot)$ 分别表示沿特征维度的均值和标准差。该操作确保拼接后的特征空间保持DINO原有的语义判别结构。消融实验（Table 4）表明，移除该对齐步骤会导致生成gFID从6.12恶化至9.03，验证了分布对齐对维持语义结构的关键作用。

**SVG解码器（SVG Decoder）**：将拼接对齐后的SVG特征解码回像素空间，训练时使用重建损失进行监督。

### 3. 潜在空间插值

为评估SVG特征空间的连续性与语义平滑性，论文引入了两种噪声向量插值方式。给定两个随机采样的噪声向量 $\pmb{x}_T^{0}$ 和 $\pmb{x}_T^{1}$，线性插值（lerp）定义为：

$$\pmb{x}_T^{\lambda} = (1 - \lambda) \pmb{x}_T^{0} + \lambda \pmb{x}_T^{1}, \qquad \lambda \in [0, 1] \tag{7}$$

球面线性插值（slerp）保持噪声向量的范数分布：

$$\pmb{x}_T^{\lambda} = \frac{\sin((1 - \lambda)\theta)}{\sin\theta} \pmb{x}_T^{0} + \frac{\sin(\lambda\theta)}{\sin\theta} \pmb{x}_T^{1}, \qquad \lambda \in [0, 1] \tag{8}$$

其中 $\theta$ 为两向量夹角：

$$\theta = \operatorname{arccos}\left(\frac{(\pmb{x}_T^{0})^{\top} \pmb{x}_T^{1}}{\|\pmb{x}_T^{0}\| \|\pmb{x}_T^{1}\|}\right) \tag{9}$$

这些插值操作用于验证SVG潜在空间的语义连续性——在语义分散良好的空间中，插值生成的图像应呈现平滑的语义过渡，而非突变或语义混合。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2510_15301/figures/001_Figure_1.jpg]]
*Figure 1: Core contribution of SVG. (a) Vanilla VAE-based LDM: the diffusion model is trained on the pretrained VAE latent space. (b) Diff. Model Feature Alignment: intermediate features of the diffusion model are aligned to Visual Foundation Model (VFM) features. (c) VAE and Diff. Model Feature Alignment: both VAE latent features and diffusion model intermediate features are aligned to VFM features. (d) Our method: the diffusion model is trained directly in the SVG space derived from self-supervised representations (DINOv3). (e-f) Comparisons of inference and training efficiency*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2510_15301/figures/005_Figure_5.jpg]]
*Figure 5: Visualization of SVG reconstruction. Incorporating the Residual Encoder enables SVG to better preserve visual information, such as color and high-frequency details*

## 实验与关键发现

### 核心瓶颈与因果机制

传统VAE潜在空间存在严重的语义纠缠，缺乏清晰的判别结构。t-SNE可视化（Figure 4a）明确显示，标准VAE（如SD-VAE）的潜在空间中不同类别的特征高度混合，而DINOv3特征空间则呈现出清晰的类间分离和紧凑的类内聚集。这种语义分散性直接影响了扩散模型的优化难度：在语义纠缠的空间中，平均速度方向在不同类别间重叠、方向模糊；而在语义分离的空间中，平均速度方向在类内一致、类间分离（Figure 4b）。这一因果机制解释了为何SVG能够在更少的训练轮次和采样步数下达到更高质量——语义结构化的潜在空间大幅简化了扩散模型需要学习的映射关系。

### 系统级性能对比

Table 1呈现了ImageNet 256×256上的系统级性能对比。SVG-XL在仅80个训练epoch、25步采样下即达到gFID 3.54（w/ CFG）和gFID 6.57（w/o CFG），显著优于基于标准VAE的扩散模型。作为对比，同样使用流匹配目标的**SiT-XL**（Ma et al., 2024）配合SD-VAE在25步采样下的gFID为22.58（w/o CFG），SVG将其降低了16.01。即使与训练更充分的模型相比——如**SiT-XL**配合SD-VAE在250步采样下达到gFID 5.10（w/ CFG）——SVG-XL仅用25步就实现了3.54的更优结果。当训练扩展至500 epochs时，SVG-XL进一步达到gFID 2.10（w/ CFG），在生成质量上展现出持续的提升潜力。

值得注意的是，SVG的训练收敛速度显著快于传统方案。Table 1中80 epochs的SVG-XL已超越多数需要更长训练的基线模型，包括**DiT-XL**（Peebles & Xie, 2022）和**REPA-XL**（Yu et al., 2025）等特征对齐方法。与同样尝试对齐VFM特征的**SiT-XL with VA-VAE**（Yao et al., 2025）相比，SVG在无需完整VAE编解码器的情况下取得了更优的性能。

### 少步采样与模型缩放

Table 2进一步验证了SVG在少步采样场景下的显著优势。在5步极低采样步数下，SVG-XL达到FID-50K 12.26（w/o CFG），而SiT-XL配合SD-VAE仅为69.38，差距达57.12。在10步采样下，SVG-XL的9.39同样大幅优于SiT-XL的32.81。这一结果表明，语义结构化的潜在空间不仅加速了训练收敛，也使得扩散模型在推理时能够以更少的去噪步数达到高质量生成。

在模型缩放维度（Table 2b），SVG在不同模型容量（B、L、XL）下均一致优于对应的SiT配置，且仅需25步采样即可超越SiT在250步下的性能。这证明SVG框架的收益具有跨模型规模的泛化性，并非仅适用于特定参数规模。

### 编码器选择与消融分析

Table 3比较了不同视觉基础模型作为编码器的表现。DINOv3在语义理解（线性探针Top-1准确率）和重建质量之间取得了最佳平衡，优于SigLIP2和MAE。这一选择对SVG框架至关重要：过强的语义压缩（如MAE）会损失重建所需的细粒度信息，而语义判别性不足的特征空间则无法提供扩散模型所需的优化简化。

Table 4的消融实验揭示了SVG各组件的关键作用。移除残差编码器的分布对齐（naively concatenated）导致生成gFID从6.12恶化至9.03，验证了公式（6）中批次统计对齐对维持语义结构的重要性。仅使用DINOv3特征而不引入残差编码器时，重建rFID显著恶化，生成gFID大幅上升，说明DINO特征虽具有强语义判别性，但缺失了重建所需的感知细节（如颜色、高频纹理，见Figure 5）。

Table 6进一步考察了DINOv3不同深度的特征层。使用浅层特征（如layer 4）会导致生成质量急剧下降（gFID 73.45），而深层特征（layer 11）则表现优异。这表明高层语义信息对扩散模型的生成过程至关重要，浅层特征虽保留更多细节但缺乏足够的语义结构来引导生成。

### 下游任务迁移能力

Table 4同时报告了SVG特征在多个下游视觉任务上的迁移性能。在ImageNet分类、ADE20K语义分割和NYUv2深度估计任务上，SVG特征保持了与原始DINOv3相比拟的性能水平。这一结果验证了SVG的核心主张：该特征空间不仅服务于生成任务，还继承了自监督特征的感知理解能力，具备作为任务通用视觉表示空间的潜力。

### 失败模式与局限性

尽管SVG在类条件生成上表现优异，但存在若干值得关注的限制。Figure 13显示，分类器自由引导（CFG）在SVG框架中的有效性低于传统VAE扩散模型，CFG对生成质量的提升幅度有限，这可能需要探索更适合语义结构化空间的引导策略。论文主要评估了类条件生成场景，对于文本到图像等更复杂的多模态条件生成的验证尚不充分。此外，SVG特征维度较高（如16×16×384），Table 7的推理效率数据显示其编码器参数量和推理延迟均高于标准VAE tokenizer，在实际部署中可能引入额外的计算开销。

### 关键图表结论汇总

- **Figure 4**：DINOv3特征空间类间分离清晰、类内聚集紧凑，而VAE潜在空间语义高度混合；语义分散的空间中平均速度方向在类间分离，简化优化并减少所需采样步数。
- **Table 1**：SVG-XL在80 epochs、25步下gFID 3.54（w/ CFG），显著优于传统VAE扩散模型，训练收敛更快。
- **Table 2**：SVG在5步和10步极低采样下大幅领先SiT-XL（差距达57.12和23.42），且在不同模型容量下一致优于基线。
- **Table 4**：移除残差编码器的分布对齐使gFID从6.12升至9.03；仅用DINO特征导致重建和生成质量均显著下降；SVG特征在下游分类、分割、深度估计任务上保持DINO的强迁移能力。
- **Table 6**：DINOv3浅层特征（layer 4）导致生成质量崩溃（gFID 73.45），深层语义信息对生成至关重要。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2510_15301/figures/007_Table_2.jpg]]
*Table 2: Comparison of few-Step generation and model scaling. Both (a) and (b) report FID-50K results after 80 training epochs. (a) SVG achieves substantially better performance than SiT under few-step sampling. (b) SVG consistently outperforms SiT across different capacities with fewer sampling steps. SD and VA denote SD-VAE and VA-VAE, respectively. (a) Few-step generation*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2510_15301/figures/009_Table_4.jpg]]
*Table 4: Ablation study on the effectiveness of SVG encoder components. Reconstruction performance is reported after 40 epochs of training, while generative metrics are evaluated after 500K training iterations using classifier-free guidance. For visual downstream tasks, we report fine-tuning results on ImageNet-1K, ADE20K, and NYUv2*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2510_15301/figures/004_Figure_4.jpg]]
*Figure 4: (a) The t-SNE visualization of different visual (b) Toy example illustrating the impact of semantic dispersion feature spaces. in the feature space on diffusion model training. Figure 4: Visualization of feature space. (a) Feature visualization with t-SNE for 100 ImageNet classes (100 random samples per class, top row) and 20 classes (100 random samples per class, bottom row). Features are extracted using DINOv3 (Simeoni et al. ´ , 2025), VA-VAE (Yao et al., 2025), SD-VAE (Rombach et al., 2021), and MAR-VAE (Li et al., 2024), with each class shown in a distinct color, and model names annotated with their linear-probe Top-1 accuracy on ImageNet-1K (Deng et al., 2009). (b) Each subfigure show...*

## 定位与知识库关联

### 1. 问题定位与核心瓶颈

传统潜在扩散模型（Latent Diffusion Models, LDMs）的生成能力高度依赖预训练的变分自编码器（VAE）提供的潜在空间，然而该空间存在一个根本性问题：**语义高度纠缠，缺乏清晰的判别结构**。如 Figure 4a 的 t-SNE 可视化所示，SD-VAE 与 MAR-VAE 的潜在特征在不同类别间严重混合，而 DINOv3 的自监督特征则呈现出显著的类间分离与类内紧凑性。这种语义纠缠直接导致扩散模型的优化目标复杂化——在语义混合的空间中，平均速度场方向在类内不一致、类间不分离（Figure 4b），迫使模型需要更多训练迭代和采样步数来逼近复杂的概率流。

SVG 的核心洞察在于：**具有良好语义分离性的潜在空间可大幅简化扩散模型的优化难度**，使得模型在更少训练轮次和采样步数下达到更高质量；同时，这种空间继承了自监督特征的感知理解能力，为构建任务通用的视觉表示提供了可行路径。

### 2. 现有方法谱系与 SVG 的定位

当前主流方法可归纳为三条技术路线，SVG 在其中开辟了第四条路径：

| 路线 | 代表工作 | 核心策略 | 潜在空间性质 |
|------|---------|---------|-------------|
| **VAE-based LDM** | **DiT-XL** (Peebles & Xie, 2022)、**SiT-XL** (Ma et al., 2024) | 在预训练 VAE 的压缩空间上训练扩散/流匹配模型 | 感知压缩，语义混合 |
| **扩散模型特征对齐** | **REPA-XL** (Yu et al., 2025) | 将扩散模型中间层特征与视觉基础模型（VFM）对齐 | 训练中注入语义信号，但空间本身仍为 VAE 潜在空间 |
| **VAE + 扩散模型联合对齐** | **SiT-XL with VA-VAE** (Yao et al., 2025) | 同时将 VAE 潜在特征和扩散中间特征对齐到 VFM | VAE 空间被微调，但编码器-解码器架构不变 |
| **无 VAE 的语义原生空间** | **SVG**（本工作） | 直接在自监督 VFM 特征空间上训练扩散模型，无需 VAE | 语义判别性强，可复用为通用视觉特征 |

此外，还有两条非扩散的生成路线作为参照：**LlamaGen**（Sun et al., 2024）采用自回归生成范式，**MaskDiT-XL**（Zheng et al., 2024）采用掩码扩散范式。它们均依赖 VAE 进行图像 token 化，因此同样受限于 VAE 潜在空间的语义纠缠问题。

SVG 的独特之处在于**彻底移除 VAE**，转而利用冻结的 DINOv3 编码器提取具有强语义判别性的基础特征，并通过轻量残差编码器补充细粒度感知细节。这一设计改变了四个关键技术槽位：

1. **潜在空间编码器**：从标准 VAE 编码器（如 SD-VAE）替换为冻结 DINOv3 + 轻量残差编码器（Section 3.3, Figure 3）。
2. **残差特征整合**：从无残差分支到沿通道维拼接 DINO 特征与残差特征，并通过批次统计对齐（公式 6）以维持语义结构。
3. **扩散模型训练目标**：在 SVG 高维语义空间上使用流匹配目标（公式 5）训练，结合 QK-Norm 和逐通道归一化以稳定训练（Section 3.3）。
4. **特征空间维度**：从低维 VAE 潜在空间（如 $16 \times 16 \times 4$）跃升至高维 SVG 特征空间（如 $16 \times 16 \times 384$，DINOv3-ViT-S/16+），显著增加了信息容量。

### 3. 关键设计决策的因果机制

#### 3.1 为什么语义分离性对扩散模型至关重要

Figure 4b 的 toy example 揭示了因果机制：在语义分散的空间中，平均速度场方向在同类样本间一致、异类样本间分离，扩散模型只需学习简单的概率流即可实现高质量生成。相反，在语义纠缠的空间中，速度方向重叠且模糊，模型必须拟合高度复杂的流形。这解释了为何 SVG 在仅 80 个训练 epoch、25 步采样下即可达到 gFID 3.54（w/ CFG），而基于 SD-VAE 的 SiT-XL 在相同步数下仅为 22.58（Table 1）。

#### 3.2 残差编码器的双重作用

残差编码器并非简单的细节补充模块。其核心设计——**分布对齐**（公式 6）——将残差特征的批次统计量归一化到与 DINO 特征相同的分布，从而在拼接后保持整体特征空间的语义结构。消融实验（Table 4）表明，移除对齐操作（naively concatenated）导致生成 gFID 从 6.12 恶化至 9.03，验证了分布对齐对维持语义结构的关键作用。仅使用 DINOv3 特征而不用残差编码器时，重建 rFID 显著变差，生成 gFID 同步上升，说明残差分支在保留感知细节（如颜色、高频纹理，见 Figure 5）的同时，不影响语义空间的判别性。

#### 3.3 编码器选择的边界条件

Table 3 的编码器比较揭示了 SVG 设计的适用边界：DINOv3 在语义理解（线性探测 Top-1 准确率）和重建质量之间取得了最佳平衡，优于 SigLIP2 和 MAE。Table 6 进一步表明，使用 DINOv3 的浅层特征（如 layer 4）会导致生成质量急剧下降（gFID 73.45），说明深层语义信息对生成任务至关重要。这意味着 SVG 框架的有效性依赖于所选 VFM 的深层特征同时具备强语义判别性和足够的空间分辨率。

### 4. 适用边界与局限性

尽管 SVG 在类条件图像生成上展示了显著优势，其当前版本存在明确的适用边界：

1. **分类器自由引导（CFG）效率不足**：CFG 在 SVG 框架中的有效性低于传统 VAE 扩散模型（见 Figure 13），需要探索更适配语义原生空间的引导策略。

2. **特征维度开销**：SVG 特征空间维度（如 $16 \times 16 \times 384$）远高于 VAE 潜在空间（如 $16 \times 16 \times 4$），可能引入额外的计算和存储开销。压缩特征维度或优化残差编码器是未来方向。

3. **任务覆盖范围有限**：当前验证集中于 ImageNet 类条件生成、分类、语义分割和深度估计（Table 4），在更大规模数据集（如 LAION）、更高分辨率、文本到图像/视频生成、以及目标检测/实例分割等任务上的潜力尚未验证。

4. **对特定自监督模型的依赖**：SVG 的性能与 DINOv3 深度绑定，能否在不依赖特定 VFM 的情况下训练端到端的联合编码器，同时优化生成和感知，仍是一个开放问题。

### 5. 开放问题

1. SVG 特征空间在更广泛的下游感知任务（如目标检测、实例分割）上的性能能否持续超越专门的预训练模型？
2. 如何有效降低 SVG 特征的维度，同时保持其语义判别性和重建质量，以进一步提升效率？
3. 该框架能否无缝集成到现有的视频生成或多模态大模型中，作为统一的视觉编码器？
4. 在不依赖特定自监督模型（DINOv3）的情况下，能否训练一个端到端的联合编码器，同时优化生成和感知？
5. SVG 特征空间的语义结构在多大程度上可被显式操控（如通过潜在空间编辑），以实现更精细的可控生成？

### 6. 知识库定位总结

SVG 在扩散模型知识库中的定位是：**首个彻底移除 VAE、直接在自监督语义原生空间上训练扩散模型的工作**。它不同于仅对扩散中间特征进行对齐的 REPA，也不同于同时对齐 VAE 和扩散特征的 VA-VAE，而是从根本上重构了潜在空间的来源。其核心贡献在于证明了语义分离性对扩散模型训练效率的因果性影响，并提供了可同时服务于生成和感知任务的统一特征空间蓝图。当前局限性主要集中在 CFG 效率、特征维度和任务覆盖范围，这为后续工作指明了改进方向。

## 原文 PDF

![[paperPDFs/ICLR_2026/Latent_Diffusion_Model_without_Variational_Autoencoder.pdf]]
