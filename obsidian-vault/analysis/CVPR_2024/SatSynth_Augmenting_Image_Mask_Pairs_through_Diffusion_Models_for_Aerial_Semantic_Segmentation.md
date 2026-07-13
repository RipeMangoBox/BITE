---
title: "SatSynth: Augmenting Image-Mask Pairs through Diffusion Models for Aerial Semantic Segmentation"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/SatSynth_Augmenting_Image_Mask_Pairs_through_Diffusion_Models_for_Aerial_Semantic_Segmentation.pdf
project_link: null
code_link: null
aliases:
- SatSynth
tags:
- CVPR_2024
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "通过扩散模型学习图像与语义标签的联合分布 p(x,y)，直接合成成对的（图像，掩码）训练样本，作为数据扩充手段。"
primary_logic: "将离散标签编码到比特空间（binary embedding），使扩散模型能同时生成图像与对应掩码；并采用两阶段生成（低分辨率扩散 + 条件超分辨率）解耦语义连贯性与细节恢复，从而在有限标注下显著提升分割性能。"
claims:
- "合成图像在 FID、sFID、IS 上均优于 SemGAN 和 DDPM，且生成的标签分布匹配原始数据。"
- "将合成数据加入训练后，在所有基准上一致提升分割指标，例如 PSPNet 在 iSAID 上 mIoU 提升 7.59%。"
- "二进制编码 + 噪声预测（bin+ε）是获得最优下游分割的必要设计。"
- "合成数据能缓解类别不平衡，稀有类别的提升幅度与类别频率呈负相关（Pearson r=-0.47）。"
---

# SatSynth: Augmenting Image-Mask Pairs through Diffusion Models for Aerial Semantic Segmentation

> [!tip] 核心洞察
> 将离散标签编码到比特空间（binary embedding），使扩散模型能同时生成图像与对应掩码；并采用两阶段生成（低分辨率扩散 + 条件超分辨率）解耦语义连贯性与细节恢复，从而在有限标注下显著提升分割性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SatSynth：通过扩散模型增强图像-掩码对用于航空语义分割 |
| 英文题名 | SatSynth: Augmenting Image-Mask Pairs through Diffusion Models for Aerial Semantic Segmentation |
| 会议/期刊 | CVPR 2024 |
| Links | [paper](https://arxiv.org/abs/2403.16605) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | SatSynth |
| Dataset | iSAID, OpenEarthMap, iSAID (256×256, object-centric) |

> [!tip] 效果简介
> - iSAID 上，FID (lower is better) 为 8.66，对比 10.21 (SemGAN)，变化 -1.55。
> - iSAID 上，mIoU (segmentation, FPN) 为 52.13，对比 41.25 (SegDiff)，变化 +10.88。
> - OpenEarthMap 上，mIoU (segmentation, FPN) 为 62.24，对比 51.23 (SegDiff)，变化 +11.01。

## 概要

遥感语义分割的性能高度依赖大规模逐像素标注数据，而人工标注成本高昂，导致高质量标注样本稀缺。传统数据增强手段（如翻转、旋转、缩放）难以模拟卫星图像中丰富多变的场景与尺度分布，成为制约分割模型泛化能力的关键瓶颈。

针对这一问题，**SatSynth** 提出了一种基于扩散模型的数据增强范式：直接学习图像与语义标签的联合分布 $p(\mathbf{x}, \mathbf{y})$，并从中采样生成成对的（图像，掩码）合成样本，用于扩充下游分割模型的训练集。方法的核心洞察在于将离散类别标签编码到比特空间（binary embedding），使扩散模型能够同时生成视觉上合理的遥感图像与空间对齐的语义掩码；同时采用两阶段生成策略——先以低分辨率扩散模型保证语义连贯性，再以条件超分辨率扩散模型恢复细节——解耦了语义一致性与高保真度之间的矛盾。

在 iSAID、LoveDA 和 OpenEarthMap 三个卫星分割基准上的实验表明：
- 合成图像在 FID、sFID、IS 等视觉质量指标上均优于 **SemGAN** 和 **DDPM**（vanilla），且生成的标签分布与原始数据高度一致（Table 1a, Fig. 2(c)）。
- 将合成数据加入训练后，所有主流分割骨干网络（FPN、SegFormer、PSPNet、PFSegNet、FarSeg）均获得一致的性能提升，例如 PSPNet 在 iSAID 上的 mIoU 从 48.95 提升至 56.54（+7.59%）（Table 2）。
- 二进制编码与噪声预测（bin+ε）的组合是获得最优下游分割性能的必要设计（Table 3）。
- 合成数据能够有效缓解类别不平衡问题，稀有类别的提升幅度与类别频率呈负相关（Pearson r = -0.47）（Fig. 7）。

该方法在方法谱系上定位于**生成式数据增强**，区别于仅生成图像（如 DDPM）或分别生成图像与掩码（如 SemGAN）的路线，亦不同于基于判别式扩散模型直接预测分割掩码的方案（如 **SegDiff**, Amit et al., CVPR 2021）。与 Cutout、CutMix、Copy-Paste 等经典增强策略相比，SatSynth 带来的分割精度提升更为显著（Table 5）。当前方案的主要局限在于高分辨率生成（>256×256）仍面临训练不稳定和计算开销大的挑战，且尚未在变化检测等更广泛的地球观测任务上验证其通用性。

遥感图像的语义分割是地球观测领域的核心任务之一，广泛应用于城市规划、灾害评估、环境监测等场景。然而，高精度的语义分割模型通常依赖于大规模、高质量的逐像素标注数据。对于卫星和航空图像而言，获取此类标注的成本极高——不仅需要领域专家的参与，还面临地理空间覆盖范围广、地物类别多样、成像条件多变等挑战。这一标注瓶颈直接导致可用训练数据稀缺，严重制约了分割模型的泛化能力和实际部署效果。

传统的数据增强策略，如随机翻转、旋转、缩放、颜色抖动等，虽然能在一定程度上缓解过拟合，但其本质是对现有样本的几何或光度变换，无法引入真正新颖的场景组合、地物布局和尺度变化。对于卫星图像中复杂多样的城市场景、农田纹理、水域边界等，这类浅层变换所能提供的多样性极为有限。因此，如何在有限标注的前提下，生成具有足够多样性和真实性的新训练样本，成为提升遥感分割性能的关键突破口。

生成模型，特别是扩散模型（Diffusion Models）的快速发展，为上述问题提供了新的可能性。扩散模型通过逐步去噪学习数据分布，在图像生成质量上已展现出超越生成对抗网络（GAN）的优势。然而，将扩散模型直接应用于遥感数据增强面临两个核心挑战：

**挑战一：如何同时生成图像与对应的语义掩码？** 现有方法或仅生成图像（如普通 DDPM），无法提供下游分割训练所需的标签；或分别生成图像与掩码（如 **SemGAN**），难以保证二者之间的语义一致性。判别式扩散分割方法（如 **SegDiff**，Amit et al., CVPR 2021）虽能生成掩码，但其本质是条件于输入图像的分割预测，而非从联合分布中采样全新的训练对。

**挑战二：如何在有限计算资源下生成高分辨率、语义连贯的卫星图像？** 直接在高分辨率（如 256×256 或更高）上训练扩散模型面临训练不稳定、计算开销巨大、生成质量下降等问题。卫星图像中地物的精细结构和多尺度特征对分辨率尤为敏感，低质量生成将直接损害下游分割性能。

针对上述瓶颈，本文提出 **SatSynth**——一种基于扩散模型的联合数据增强框架，其核心动机在于：**通过学习图像与语义标签的联合分布 $p(\mathbf{x}, \mathbf{y})$，直接从分布中采样全新的（图像，掩码）训练对，作为数据扩充手段注入下游分割训练**。该方法的关键洞察是将离散语义标签编码到比特空间（binary embedding），使得扩散模型能够将图像与掩码视为统一的连续信号进行联合建模；同时采用两阶段生成策略（低分辨率扩散 + 条件超分辨率），解耦语义布局的全局一致性与细节纹理的局部恢复，从而在有限标注和计算预算下显著提升分割性能。

## 核心方法与创新机理

SatSynth 的核心创新在于将遥感语义分割的数据稀缺问题重新建模为一个**联合分布学习**问题：通过扩散模型直接学习图像与语义标签的联合分布 $p(\mathbf{x}, \mathbf{y})$，而非仅生成图像或分别生成图像与掩码。这一范式转换通过三个关键设计实现，形成了与现有方法的显著差异。

### 创新一：标签的二进制空间编码

传统方法对语义标签的处理存在根本局限：**DDPM**（Ho et al., NeurIPS 2020）仅对图像建模，无法生成对应的掩码；**SegDiff**（Amit et al., CVPR 2021）采用判别式扩散直接预测分割掩码，而非联合生成；**SemGAN** 则分别处理图像与掩码的生成。SatSynth 的核心洞察在于：离散标签与连续图像之间存在模态鸿沟，直接拼接 one-hot 编码会导致扩散模型的连续去噪过程与离散标签空间不兼容。

解决方案是将 $K$ 类离散标签通过二进制编码映射到比特空间：

$$\operatorname{bin} : \{0,\dots,K-1\} \to \{0,1\}^{\lceil \log_2 K \rceil}$$

这一设计的因果机制在于：二进制编码将离散决策转化为多个独立的二值连续预测问题，使扩散模型的高斯噪声假设在比特空间上仍然成立。消融实验（Table 3）证实了这一设计的必要性——二进制编码联合噪声预测（bin+ε）在所有配置中取得最优下游分割性能，显著优于 one-hot 编码方案。

### 创新二：图像-掩码联合生成

SatSynth 将语义分割的数据增强从“图像变换”升级为“联合分布采样”。具体而言，扩散模型 $\mathcal{G}$ 的输入输出空间从 $\mathbb{R}^{H \times W \times 3}$ 扩展为 $\mathbb{R}^{H \times W \times (3 + \lceil \log_2 K \rceil)}$，在单次扩散过程中同时生成 RGB 图像与二进制编码的语义掩码。这一设计使得合成样本 $( \mathbf{x}', \mathbf{y}' ) \sim p(\mathbf{x}, \mathbf{y})$ 天然保持图像与标签之间的语义一致性，避免了 SemGAN 等分离式生成方法中可能出现的图像-掩码不对齐问题。

生成质量验证（Table 1a）表明，SatSynth 在 iSAID 上的 FID 达到 8.66，优于 SemGAN 的 10.21；在 LoveDA 和 OpenEarthMap 上也一致取得更优的 FID/sFID/IS 指标。标签分布分析（Fig. 2c）进一步证实生成掩码的类别分布与原始数据高度匹配。

### 创新三：两阶段高分辨率生成策略

直接在高分辨率（≥256×256）上训练扩散模型面临训练不稳定和生成伪影问题。SatSynth 通过解耦语义合成与细节恢复来解决这一瓶颈：先训练 128×128 的生成器 $\mathcal{G}$ 确保语义连贯性，再训练条件超分辨率网络 $\mathcal{G}_{\text{SR}}$：

$$\mathcal{G}_{\text{SR}} : \mathbb{R}^{L} \times \mathbb{R}^{H \times W \times C} \to \mathbb{R}^{2H \times 2W \times C}$$

该网络以低分辨率图像-掩码对为条件，通过条件去噪扩散实现两倍上采样。消融实验（Table 4）证实，这一两阶段方案在分割精度上显著优于直接训练 DDPM-256，且避免了高分辨率训练的不稳定性。

### 创新四：合成数据驱动的分割增强范式

与 Cutout、CutMix、Copy-Paste 等传统数据增强方法不同，SatSynth 生成的合成样本是全新的场景实例，而非对现有样本的局部修改。通过重采样比率 $R$ 控制合成数据与真实数据的混合比例，实验（Fig. 5）表明增加 $R$ 持续提升分割性能，在 iSAID 上 $R=3$ 达到最优。值得注意的是，合成数据对稀有类别的提升幅度与类别频率呈负相关（Pearson $r=-0.47$，Fig. 7），表明该方法能有效缓解类别不平衡问题——这是传统增强方法难以实现的。

综合而言，SatSynth 的创新链条为：**二进制编码解决模态对齐 → 联合扩散实现一致生成 → 两阶段策略突破分辨率瓶颈 → 合成扩充提升分割鲁棒性**。在 iSAID 上，PSPNet 的 mIoU 从 48.95% 提升至 56.54%（+7.59%），验证了这一技术路线的有效性。


SatSynth 的整体 pipeline 围绕一个核心目标展开：从有限标注的遥感数据集中学习图像与语义标签的联合分布 $p(\mathbf{x}, \mathbf{y})$，并以此生成成对的合成样本用于下游分割模型的数据扩充。整个框架由四个关键模块串联而成，形成“编码—生成—超分—训练”的闭环流程，如 Figure 2 所示。

**模块一：标签二进制编码器（Binary Encoder）**
在将标签送入扩散模型之前，SatSynth 先将离散的语义掩码 $\mathbf{y}_i \in \{0,\dots,K-1\}^{H\times W}$ 通过映射 $\operatorname{bin} : \{0,\dots,K-1\} \to \{0,1\}^{\lceil\log_2 K\rceil}$ 编码为二进制向量（Eq. 4）。这一步的核心动机在于：one-hot 编码的高维稀疏性会使扩散模型难以同时学习图像与标签的联合流形，而紧凑的比特空间表示将标签通道数从 $K$ 压缩至 $\lceil\log_2 K\rceil$，使标签与 RGB 图像在通道维度上形成自然拼接，从而让扩散模型将联合生成问题统一为“图像生成”问题处理。

**模块二：低分辨率联合扩散生成器 $G$**
生成器 $G$ 采用标准 DDPM 架构（Ho et al., NeurIPS 2020），在前向过程中按方差调度 $\beta_t$ 逐步向拼接后的 $(\mathbf{x}_i, \operatorname{bin}(\mathbf{y}_i))$ 注入高斯噪声（Eq. 1），在反向过程中学习去噪映射 $\mathcal{G} : \mathbb{R}^L \to \mathbb{R}^{H\times W\times C}$（Eq. 2）。训练完成后，$G$ 从随机噪声 $z \sim \mathcal{N}(0, \mathbf{I})$ 出发，经迭代去噪直接输出 $128\times128$ 的低分辨率图像-掩码对 $(\hat{\mathbf{x}}_i', \hat{\mathbf{y}}_i')$。随后通过阈值化与逆二进制变换 $\operatorname{bin}^{-1}$ 将连续值掩码解码回离散类别标签，得到最终合成对 $(\mathbf{x}_i', \mathbf{y}_i')$。

**模块三：条件超分辨率生成器 $G_{SR}$**
直接在高分辨率（256×256）上训练 DDPM 存在训练不稳定和伪影问题（Table 4, Figure 10）。SatSynth 的解耦策略是：将 $G$ 的输出作为条件，训练一个条件去噪扩散模型 $\mathcal{G}_{SR} : \mathbb{R}^L \times \mathbb{R}^{H\times W\times C} \to \mathbb{R}^{2H\times 2W\times C}$（Eq. 5），以低分辨率对为引导，从噪声中重建出 256×256 的高分辨率合成样本。这种两阶段设计将语义连贯性（由 $G$ 保证）与细节恢复（由 $G_{SR}$ 负责）解耦，使得整体生成过程更稳定且下游分割精度更高。

**模块四：数据扩充与分割模型训练**
生成的高质量合成数据集 $\mathcal{D}' = \{(\mathbf{x}_i', \mathbf{y}_i')\}$ 与原始标注数据集 $\mathcal{D}$ 合并为 $\mathcal{D} \cup \mathcal{D}'$。通过重采样比率 $R$ 控制每个原始样本对应的合成样本数量，在保持真实-合成数据比例可控的前提下训练下游分割骨干网络（默认采用 FPN with ResNet-50，同时验证了 SegFormer、PSPNet、PFSegNet、FarSeg 等多种架构的兼容性）。

**输入输出流总结**：原始图像-掩码对 → 二进制编码 → 拼接为 $[0,1]^{H\times W\times(3+\lceil\log_2 K\rceil)}$ 的张量 → $G$ 生成 128×128 合成对 → 阈值解码 → $G_{SR}$ 上采样至 256×256 → 合并入训练集 → 分割模型训练。这一流程将“标注稀缺”的瓶颈转化为“生成模型学习联合分布”的可控问题，其有效性在 iSAID、LoveDA、OpenEarthMap 三个基准上得到一致验证（Table 1, Table 2）。

SatSynth 的核心目标是从标注数据集中学习图像与语义标签的联合分布 $p(\mathbf{x}, \mathbf{y})$，并从中采样新的训练样本对 $(\mathbf{x}', \mathbf{y}')$ 用于数据扩充。该方法由四个关键模块串联构成。

### 1. 二进制标签编码器 (Binary Encoder/Decoder)

遥感语义标签是离散的类别索引 $\mathbf{y}_i \in \{0, \dots, K-1\}^{H \times W}$，而扩散模型天然处理连续信号。直接使用 one-hot 编码会导致通道数随类别数线性增长，且类别间的有序性假设不成立。SatSynth 的解决方案是将离散标签映射到紧凑的比特空间：

$$
\operatorname{bin} : \{0, \dots, K-1\} \to \{0, 1\}^{\lceil \log_2 K \rceil}
$$

该映射将每个像素的 $K$ 类标签编码为长度为 $\lceil \log_2 K \rceil$ 的二进制向量。例如，对于 $K=16$ 类，仅需 4 个比特通道，远小于 one-hot 的 16 通道。在生成过程的末端，通过阈值化将去噪后的连续值二值化，再经逆映射 $\operatorname{bin}^{-1}$ 恢复为离散类别标签。消融实验 (Table 3) 证实，二进制编码 (bin) 在下游分割性能上显著优于 one-hot 编码，且与噪声预测 ($\epsilon$-prediction) 结合时达到最优。

### 2. 联合生成扩散模型 G (DDPM Backbone)

生成器 $\mathcal{G}$ 的核心是一个标准的去噪扩散概率模型 (DDPM)，其前向加噪过程定义为：

$$
\mathbf{x}_t := \sqrt{1 - \beta_t} \mathbf{x}_{t-1} + \sqrt{\beta_t} \epsilon, \quad \epsilon \sim \mathcal{N}(0, \mathbf{I})
$$

其中 $\beta_t$ 为噪声方差调度。与传统仅建模图像分布 $p(\mathbf{x})$ 的扩散模型不同，SatSynth 将 RGB 图像与二进制编码标签沿通道维度拼接，形成联合数据实例 $(\mathbf{x}_i, \operatorname{bin}(\mathbf{y}_i)) \in [0,1]^{H \times W \times (3 + \lceil \log_2 K \rceil)}$。生成器 $\mathcal{G}$ 学习从随机噪声 $\mathbf{z} \in \mathbb{R}^L$ 到该联合空间的映射：

$$
\mathcal{G} : \mathbb{R}^L \to \mathbb{R}^{H \times W \times C}
$$

其中 $C = 3 + \lceil \log_2 K \rceil$。一次扩散逆过程同时输出图像和对应的语义掩码，实现了对 $p(\mathbf{x}, \mathbf{y})$ 的直接建模。这一设计使得生成的图像与掩码在语义上天然对齐，无需后处理配对。

### 3. 条件超分辨率生成器 G_SR

直接在高分辨率（如 $256 \times 256$）上训练 DDPM 存在训练不稳定和伪影问题 (Table 4, Fig. 10)。SatSynth 采用两阶段解耦策略：先由 $\mathcal{G}$ 生成 $128 \times 128$ 的低分辨率对，再通过条件超分辨率网络 $\mathcal{G}_{\text{SR}}$ 将其上采样至 $256 \times 256$：

$$
\mathcal{G}_{\text{SR}} : \mathbb{R}^L \times \mathbb{R}^{H \times W \times C} \to \mathbb{R}^{2H \times 2W \times C}
$$

$\mathcal{G}_{\text{SR}}$ 是一个以低分辨率图像-掩码对为条件的去噪扩散模型，输入包括随机噪声和低分辨率对，输出为两倍分辨率的合成对。这种级联设计将语义连贯性的学习交给 $\mathcal{G}$，将细节恢复交给 $\mathcal{G}_{\text{SR}}$，有效规避了高分辨率 DDPM 的不稳定训练行为。

### 4. 数据扩充与分割训练

给定原始标注数据集 $\mathcal{D} := \{(\mathbf{x}_i, \mathbf{y}_i) \mid \mathbf{x}_i \in \mathbb{R}^{H \times W \times 3}, \mathbf{y}_i \in \{0,\dots,K-1\}^{H \times W}, 1 \leq i \leq N\}$，SatSynth 通过 $\mathcal{G}$ 和 $\mathcal{G}_{\text{SR}}$ 采样合成数据集 $\mathcal{D}'$，并将两者合并为 $\mathcal{D} \cup \mathcal{D}'$。通过重采样比率 $R$ 控制合成样本相对于真实样本的数量，在扩充后的数据集上训练标准分割骨干网络（默认为 FPN with ResNet-50）。实验表明，增加 $R$ 可持续提升分割性能，iSAID 上最优 $R=3$ (Fig. 5)。

### 证据强度说明

- **二进制编码 + 噪声预测的最优性**：Table 3 消融实验提供了直接对比，bin+$\epsilon$ 组合在 IoU 和 F1 上均优于其他变体，置信度高。
- **两阶段超分辨率的必要性**：Table 4 和 Fig. 10 分别从定量和定性角度证实 DDPM-256 的训练不稳定和伪影问题，所提方案的下游分割精度更高，置信度高。
- **联合生成的有效性**：Table 1a 中 SatSynth 在 FID/sFID/IS 上均优于 SemGAN 和 DDPM，Table 1b 中分割精度显著超越 SegDiff，构成强证据链。

## 实验与关键发现

### 核心实验设置

SatSynth 在三个主流卫星语义分割基准上进行了系统性评估：**iSAID**（15 类，高分辨率目标级标注）、**LoveDA**（7 类，城乡土地覆盖）和 **OpenEarthMap**（8 类，全球城市语义）。实验分为两个层次：生成模型自身的视觉质量评估，以及合成数据对下游分割任务的增益验证。生成模型统一在 128×128 分辨率上训练，分割评估则覆盖 128×128 和 256×256（通过超分辨率模块 G_SR 上采样）两种尺度。下游分割默认使用 FPN + ResNet-50 骨干网络，并在多个主流架构（SegFormer、PSPNet、PFSegNet、FarSeg）上重复实验以验证鲁棒性。

### 生成质量：FID/sFID/IS 全面领先

Table 1(a) 报告了生成图像在三个基准上的 FID、sFID 和 IS 指标。SatSynth 在所有数据集上均优于基于 GAN 的 **SemGAN** 和仅对图像建模的 **DDPM**（vanilla）。以 iSAID 为例，SatSynth 的 FID 降至 8.66，相比 SemGAN（10.21）降低 1.55，sFID 和 IS 同样保持优势。值得注意的是，vanilla DDPM 虽然能生成视觉上合理的图像，但无法产生对应的语义掩码，因此在分割任务中无法直接使用；而 SatSynth 通过联合建模 p(x,y) 同时输出成对的图像与掩码，在保证图像质量的同时实现了标签一致性（Fig. 2(c) 验证了生成标签的类别分布与原始数据高度吻合）。

### 分割增益：跨基准、跨骨干的稳定提升

Table 1(b) 和 Table 2 展示了合成数据带来的下游分割增益。在 128×128 分辨率下，SatSynth 在 iSAID 上达到 52.13 mIoU，相较 **SegDiff**（Amit et al., CVPR 2021）的 41.25 提升了 10.88 个百分点；在 OpenEarthMap 上同样以 62.24 mIoU 领先 SegDiff 的 51.23（+11.01）。Table 2 进一步在 256×256 目标级分割上验证：将合成数据 D′ 与原始数据 D 合并后，五个不同分割骨干网络一致获得提升，其中 PSPNet 的 mIoU 从 48.95 跃升至 56.54（+7.59%），PFSegNet 从 60.93 提升至 63.71。Fig. 5 通过控制重采样比率 R（每个真实样本对应的合成样本数）揭示了合成数据量的影响：mIoU 随 R 增加持续上升，在 iSAID 上 R=3 时达到最优，此后趋于饱和，表明合成数据存在边际效益递减但未出现性能下降。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2403_16605/figures/006_Figure_5.jpg]]
*Figure 5: Analysis of synthetic data. We assess the impact of generated samples $\mathcal { D } \cup \mathcal { D } ^ { \prime }$ on the mIoU segmentation score for iSAID [61], LoveDA [60], and OpenEarthMap [64], with a spatial size of 1 2 8 $\times$ 1 2 8 . Different resampling ratios are applied, defined as sampling R $\in \{$ 0 , $\ldots$ , 5 $\}$ synthetic pairs per original instance, i . e . , | $\mathcal { D } ^ { \prime }$ | = R $\cdot | \mathcal { D }$ | pairs in total. In each case, error bars are provided which denote the standard error (SE). We separately plot the accuracies without synthetic samples R = 0 (gray dashed lines) for ease of comparison

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2403_16605/figures/007_Table_2.jpg]]
*Table 2: Object-centric segmentation. We demonstrate that integrating our generated training pairs $\mathcal { D } \cup \mathcal { D } ^ { \prime }$ improves the performance over the original data D on the iSAID [61] benchmark. To this end, we consider the recent state-of-the-art approaches PFSegNet [34] and FarSeg [73] that specialize on satellite segmentation, as well as three generic segmentation models [31, 65, 71]. In each setting, we utilize super-resolution pairs with a spatial size of 2 5 6 $\times$ 2 5 6 as defined in Sec. 4.4

### 关键消融：二进制编码与噪声预测的必要性

Table 3 针对两个核心设计选择进行了消融实验——标签编码方式（one-hot vs. binary）和扩散模型的预测目标（x₀ 预测 vs. ε 噪声预测）。结果表明：

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2403_16605/figures/009_Table_3.jpg]]
*Table 3: Ablation study. We investigate how two central design choices for the joint data generation, outlined in Sec. 4.3, relate to the downstream segmentation performance on iSAID. Specifically, we compare two variants of the network G, predicting the noise component ϵ or the initial sample x0, and we contrast the binary label embedding with standard one-hot encoding. These results confirm that both components are crucial (lower row, bin+ϵ) for obtaining optimal results*

- **二进制编码（bin）** 在所有配置下均优于 one-hot 编码，验证了将离散标签压缩至 ⌈log₂K⌉ 位二进制空间对联合生成的有效性；
- **噪声预测（ε-prediction）** 优于直接预测 x₀，这与标准 DDPM 的实践一致；
- **bin + ε 的组合** 达到最优分割性能（iSAID: 52.13 IoU, 66.13 F1），证明两者是互补而非冗余的设计。

Table 4 消融了超分辨率策略。直接在高分辨率（256×256）上训练 DDPM（DDPM-256）存在训练不稳定和伪影问题，导致下游分割性能低于 SatSynth 的两阶段方案（G + G_SR）。Fig. 10 的定性对比进一步显示，DDPM-256 生成的图像存在明显的结构扭曲，而 G_SR 能在保持语义连贯性的前提下恢复细节。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2403_16605/figures/011_Table_4.jpg]]
*Table 4: Super-resolution. We compare our super-resolution approach to directly generating synthetic samples with DDPM, analogous to our approach in Sec. 4.3. We find that DDPM exhibits unstable training behaviour for resolutions H = W ≥ 256 which results in a suboptimal downstream segmentation performance on iSAID. The obtained joint samples display notable artifacts, particularly in terms of the saturation and contrast of the generated images, refer to Fig. 10 for a qualitative comparison*

### 与经典增强方法的对比

Table 5 将 SatSynth 与 Cutout、CutMix、Copy-Paste 等经典数据增强方法进行了公平对比（均使用 R=1 的合成样本量）。SatSynth 在所有基准上均取得更优的分割精度，证明通过扩散模型生成全新的、语义一致的训练样本，比在已有样本上进行空间变换或区域混合更能提升模型的泛化能力。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2403_16605/figures/012_Table_5.jpg]]
*Table 5: Quantitative comparison of augmentation methods. We compare our method to the recent augmentation techniques Cutout [18], CutMix [68], and Copy-Paste [22]. Across all experiments, we generate additional training pairs with a resampling ratio of R = 1. The experimental setup is equivalent to the results on iSAID reported in Fig. 5 of the main paper*

### 类别不平衡的缓解

Fig. 7 分析了合成数据对各类别的差异化影响。以 PSPNet 在 iSAID 上的逐类 IoU 提升为纵轴，类别在训练集中的相对频率为横轴，两者呈显著负相关（Pearson r = -0.47）。这意味着稀有类别（如“游泳池”、“直升机”）从合成数据中获得的绝对提升远大于高频类别（如“道路”、“建筑”）。Table 6 的逐类得分进一步证实了这一趋势：合成数据通过生成更多稀有类别的样本，隐式缓解了类别不平衡问题，这是传统几何增强难以实现的。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2403_16605/figures/013_Table_6.jpg]]
*Table 6: Per-class segmentation scores on iSAID 256 × 256. We provide a detailed analysis of the per-class segmentation scores on iSAID. Specifically, we report mean IoU scores for approaches tailored for high-resolution satellite imagery [34, 73] and the generalpurpose segmentation models SegFormer [65], FPN [31], and PSPNet [71]. Each model is trained on the combined dataset of original and generated samples $\mathcal { D } \cup \mathcal { D } ^ { \prime }$ . , and compared against models trained solely on the original data D. For a majority of classes, the synthesized data yields marked improvements in performance. We abbreviate the 16 semantic classes with the following acronyms: background (BG),...

### 失败模式与局限性

尽管 SatSynth 在多个维度上表现出色，实验中也暴露了若干局限：

1. **高分辨率生成瓶颈**：直接训练 256×256 的 DDPM 存在训练不稳定和伪影问题（Table 4, Fig. 10），两阶段超分辨率方案虽有所缓解，但仍将分辨率上限限制在 256×256，更高分辨率（如 512×512）的扩展尚未验证。
2. **计算开销**：扩散模型的训练和采样本身计算密集，加上超分辨率模块的两阶段流水线，整体训练成本显著高于传统增强方法。
3. **任务泛化未验证**：评估仅聚焦于语义分割任务，合成数据在变化检测、实例分割等其他地球观测任务上的有效性仍是开放问题。
4. **分布偏移风险**：Fig. 2(c) 显示生成标签的分布匹配原始数据，但在更复杂的实际场景中，生成数据与真实数据之间的潜在分布偏移可能引入偏差，这一点尚未进行系统性分析。

## 定位与知识库关联

### 1. 卫星图像数据增强的方法谱系

SatSynth 处于**卫星图像语义分割的数据增强**这一交叉领域，其核心贡献在于将扩散模型的生成能力从“仅生成图像”拓展到“联合生成图像-掩码对”，从而直接为下游分割模型提供成对的合成标注数据。理解其定位需要从以下三个维度展开：

**（1）传统数据增强的局限与生成式增强的兴起**

传统卫星图像增强方法主要包括几何变换（翻转、旋转、缩放）和像素级操作（颜色抖动、噪声注入）。这些方法虽然简单高效，但存在根本局限：它们无法模拟卫星图像中多样的场景组合、尺度变化和类别共现模式。更高级的增强策略如 Cutout、CutMix 和 Copy-Paste 通过区域级操作引入了更强的正则化，但仍局限于对已有样本的局部重组，无法创造全新的场景布局。

SatSynth 的定位是**生成式数据增强**（generative data augmentation），即通过学习训练集的联合分布 $p(\mathbf{x}, \mathbf{y})$ 来合成全新的（图像，掩码）对。这一思路将数据增强从“变换已有样本”提升为“采样新样本”，从根本上扩展了训练数据的多样性空间。Table 5 的实验直接验证了这一优势：在 iSAID 数据集上，SatSynth 的 mIoU 提升幅度显著超过 Cutout、CutMix 和 Copy-Paste。

**（2）与 GAN 基线和判别式扩散模型的对比**

在生成式数据增强的谱系中，SatSynth 的直接比较对象包括两类方法：

- **SemGAN**：基于 GAN 的图像-掩码联合生成方法。GAN 的优势在于单步生成速度快，但其训练不稳定性在卫星图像这种具有复杂空间结构和长尾类别分布的数据上尤为突出。从 Table 1a 的结果看，SatSynth 在 FID 上全面优于 SemGAN（iSAID: 8.66 vs 10.21; LoveDA: 13.87 vs 15.79; OpenEarthMap: 12.09 vs 15.96），表明扩散模型在生成质量和多样性上具有显著优势。

- **SegDiff**（Amit et al., CVPR 2021）：基于判别式扩散模型的图像-掩码生成方法，其核心是直接预测分割掩码。SatSynth 与之的关键区别在于**生成范式**：SegDiff 是判别式的（从图像到掩码），而 SatSynth 是生成式的（从噪声到图像-掩码联合样本）。这一差异导致 SegDiff 生成的掩码质量受限于输入图像的质量，而 SatSynth 可以自由采样全新的场景。Table 1b 的分割精度对比（iSAID mIoU: 52.13 vs 41.25）证实了联合生成范式在数据扩充场景下的优势。

**（3）与通用扩散模型（DDPM）的关系**

SatSynth 直接建立在 **DDPM**（Ho et al., NeurIPS 2020）的框架之上，但其核心创新在于将 DDPM 从单模态图像生成扩展为多模态联合生成。普通 DDPM 仅对图像 $\mathbf{x} \sim p(\mathbf{x})$ 建模，生成的图像没有对应的语义掩码，无法直接用于分割训练。SatSynth 通过**二进制标签编码**（将离散标签映射到比特空间）和**通道拼接**（将 RGB 图像与二进制掩码在通道维度拼接），使 DDPM 能够同时学习并采样 $p(\mathbf{x}, \mathbf{y})$。这一设计是方法的核心技术贡献，Table 3 的消融实验证实二进制编码 + 噪声预测（bin+ε）是获得最优下游分割的必要组合。

### 2. 核心技术设计的因果机制

SatSynth 的性能优势源于以下三个相互关联的设计选择，每个选择都对应一个明确的因果机制：

**（1）二进制编码（bit-space embedding）→ 解耦类别间的生成冲突**

将 K 类离散标签映射为 $\lceil \log_2 K \rceil$ 位的二进制向量，而非 one-hot 编码，是 SatSynth 最关键的微观设计。其因果机制在于：one-hot 编码在通道维度上引入了类别间的互斥约束（每个像素只有一个通道为 1），这使得扩散模型在去噪过程中需要同时满足“类别互斥”和“图像-掩码一致性”两个约束，增加了优化难度。二进制编码则允许每个比特通道独立去噪，将复杂的多类预测问题分解为多个独立的二分类问题，降低了生成任务的难度。Table 3 显示，仅将 one-hot 替换为二进制编码，mIoU 就有显著提升。

**（2）噪声预测（ε-prediction）→ 更稳定的联合分布学习**

扩散模型的训练目标可以选择预测噪声 ε 或预测原始数据 $\mathbf{x}_0$。SatSynth 选择 ε-prediction 的因果逻辑是：在联合生成图像和二进制掩码时，两者的数值范围（图像像素值 ∈ [0,1]，二进制掩码 ∈ {0,1}）和统计特性差异很大。直接预测 $\mathbf{x}_0$ 需要模型同时恢复两种不同模态的精确值，而预测噪声 ε 只需要学习去噪方向，对模态差异更鲁棒。Table 3 的 bin+ε 组合达到最优性能，验证了这一设计。

**（3）两阶段超分辨率（G + G_SR）→ 解耦语义连贯性与细节恢复**

直接在高分辨率（≥256×256）上训练 DDPM 存在训练不稳定和生成伪影的问题（Table 4, Figure 10）。SatSynth 的两阶段方案——先训练 128×128 的生成器 G，再训练条件超分辨率网络 G_SR 上采样至 256×256——将生成任务分解为两个子问题：G 负责保证语义布局的全局连贯性，G_SR 负责恢复高频细节。这种解耦使得每个子网络的任务更简单，训练更稳定。Table 4 的对比证实，两阶段方案的下游分割精度优于直接高分辨率 DDPM。

### 3. 适用边界与局限

基于论文中的实验设置和讨论，SatSynth 的适用边界和局限可从以下维度理解：

**（1）分辨率边界**

当前方案支持的最高生成分辨率为 256×256（通过两阶段超分辨率）。对于需要更高分辨率的应用场景（如 512×512 或更高），论文明确指出存在两个障碍：一是直接训练高分辨率 DDPM 的不稳定性（Figure 10 展示了明显的伪影），二是超分辨率网络的级联扩展尚未验证。这是一个**工程可扩展性**问题，而非理论限制——原则上可以通过增加超分辨率级联层数或采用更先进的高分辨率扩散架构（如级联扩散模型）来解决，但需要额外的工程验证。

**（2）任务边界**

论文的实验验证集中在**语义分割**任务上，包括三个卫星图像基准（iSAID、LoveDA、OpenEarthMap）。对于其他地球观测任务，如变化检测、实例分割、云去除等，SatSynth 的适用性尚未验证。从方法原理看，联合生成范式可以自然地扩展到任何需要成对图像-标注数据的任务，但不同任务对生成质量的要求不同（如变化检测需要时序一致性，实例分割需要区分个体实例），这些场景下的有效性需要进一步实验确认。

**（3）类别分布偏移**

SatSynth 通过学习训练集的联合分布来生成新样本，这意味着生成数据的类别分布会反映训练集的分布特征。Figure 7 的分析显示，合成数据对稀有类别的提升幅度更大（Pearson r=-0.47），这在一定程度上缓解了类别不平衡问题。但这也意味着，如果训练集中某些类别极度稀缺（如仅有个位数样本），扩散模型可能无法学习到这些类别的有效表示，生成的掩码质量会下降。这是一种**数据驱动的固有局限**，而非方法缺陷。

**（4）计算成本**

扩散模型的训练和采样本身计算密集，SatSynth 的两阶段方案（G + G_SR）进一步增加了计算开销。论文未提供具体的训练时间和推理延迟数据，但这是实际部署中需要考虑的重要因素。对于资源受限的场景，可能需要权衡合成数据的质量增益与计算成本。

### 4. 开放问题与未来方向

基于论文的讨论和方法的内在特性，以下开放问题值得关注：

**（1）高分辨率扩展的工程路径**

如何将合成数据扩充推广到 >256×256 分辨率？可能的路径包括：采用更高效的扩散架构（如潜在扩散模型 LDM）、增加超分辨率级联层数、或探索隐式神经表示等替代生成范式。这些方向的核心挑战在于保持语义掩码在高分辨率下的空间精度。

**（2）可控生成与定向增强**

当前 SatSynth 生成的样本是“无条件”的（从随机噪声采样），无法针对特定类别或场景进行定向增强。一个自然的扩展是引入控制信号（如文本提示、类别标签、场景图），使生成过程可以聚焦于提升特定类别或场景的表现。这对于处理极度不平衡的数据集尤为重要。

**（3）生成数据与真实数据的分布偏移**

合成数据与真实数据之间不可避免地存在分布偏移。Figure 2(c) 显示生成的标签分布与原始数据匹配良好，但这仅在统计层面成立。在更细粒度的特征层面（如纹理、光照、几何形变），生成数据可能与真实数据存在系统性偏差。这种偏差是否会在更复杂的实际场景中引入模型偏见，是一个需要深入研究的开放问题。

**（4）与其他学习范式的结合**

SatSynth 目前与全监督分割模型结合使用。将其与自监督预训练、半监督学习或域自适应方法结合，可能产生协同效应。例如，利用合成数据预训练分割模型，再在真实数据上微调；或利用合成数据作为源域，进行域自适应分割。这些组合的效益尚未被探索。

**（5）多模态扩展**

卫星数据通常包含多光谱波段（超出 RGB），而 SatSynth 目前仅处理 RGB 图像。将联合生成框架扩展到多光谱数据，需要考虑不同波段间的物理约束和统计特性，这是一个具有实际价值但技术上具有挑战性的方向。

## 原文 PDF

![[paperPDFs/CVPR_2024/SatSynth_Augmenting_Image_Mask_Pairs_through_Diffusion_Models_for_Aerial_Semantic_Segmentation.pdf]]
