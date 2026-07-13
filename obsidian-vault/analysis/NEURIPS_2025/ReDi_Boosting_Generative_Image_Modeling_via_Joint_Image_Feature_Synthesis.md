---
title: "ReDi: Boosting Generative Image Modeling via Joint Image-Feature Synthesis"
type: paper
paper_level: A
venue: NeurIPS
year: 2025
pdf_ref: paperPDFs/arxiv_2025/ReDi_Boosting_Generative_Image_Modeling_via_Joint_Image_Feature_Synthesis.pdf
project_link: https://representationdiffusion.github.io/
code_link: null
aliases:
- RRD
- ReDi
tags:
- NEURIPS_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将高维语义特征（DINOv2）与VAE潜变量在同一扩散过程中进行联合建模，强制模型显式学习两者的联合分布。
primary_logic: 通过联合建模图像和语义表示，扩散模型能够直接整合互补的低级细节和高级语义，从而在不增加复杂蒸馏目标的情况下简化训练，并解锁了一种新的推理策略——表示引导（Representation Guidance），利用学习到的语义理解迭代精炼生成图像，进一步提升质量。
claims:
- ReDi联合建模VAE潜变量和DINOv2语义特征，显著提升图像合成性能并加速收敛。
- 在DiT和SiT上，ReDi相较于基线大幅降低FID，例如DiT-XL/2在400K步即超越基线7M步的性能。
- 表示引导（Representation Guidance）在推理时利用语义预测，将DiT-XL/2的FID从8.7降至5.9。
- ImageNet 256x256 (无 CFG) 上 FID↓ = 7.5 (SiT-XL/2 w/ ReDi 400K)
---

# ReDi: Boosting Generative Image Modeling via Joint Image-Feature Synthesis

> [!tip] 核心洞察
> 通过联合建模图像和语义表示，扩散模型能够直接整合互补的低级细节和高级语义，从而在不增加复杂蒸馏目标的情况下简化训练，并解锁了一种新的推理策略——表示引导（Representation Guidance），利用学习到的语义理解迭代精炼生成图像，进一步提升质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | ReDi：通过联合图像-特征合成提升生成式图像建模 |
| 英文题名 | ReDi: Boosting Generative Image Modeling via Joint Image-Feature Synthesis |
| 会议/期刊 | NeurIPS 2025 (Spotlight) |
| Links | [paper](https://arxiv.org/abs/2504.16064) · [Project](https://representationdiffusion.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ReDi (Representation Diffusion) |
| Dataset | ImageNet 256x256 |

> [!tip] 效果简介
> - ImageNet 256x256 (无 CFG) 上，FID↓ 7.5 (SiT-XL/2 w/ ReDi 400K) vs 17.2 (SiT-XL/2 400K) (-9.7)；FID↓ 8.7 (DiT-XL/2 w/ ReDi 400K) vs 19.5 (DiT-XL/2 400K) (-10.8)。
> - ImageNet 256x256 (有 CFG) 上，FID↓ 1.72 (ReDi 350 epochs) vs 2.06 (SiT-XL/2 1400 epochs) (-0.34)。
> - ImageNet 256x256 (无 CFG, 无条件生成) 上，FID↓ 22.6 (DiT-XL/2 w/ ReDi + RG) vs 43.5 (DiT-XL/2) (-20.9)。

## 概要

### 问题与瓶颈

潜在扩散模型（LDM）在训练过程中面临一个内在张力：需要同时保持精确的低级像素重建和开发具有语义意义的表示。现有方法如 **REPA**（Yu et al., 2025）试图通过蒸馏外部视觉表示（如 DINOv2）来改善语义质量，但引入了额外的复杂损失目标，未能从根本上解决这一矛盾。

### 核心方法

**ReDi（Representation Diffusion）** 提出了一种简洁而有效的方案：将高维语义特征（DINOv2）与 VAE 潜变量在同一扩散过程中进行**联合建模**。具体而言，ReDi 对两种模态施加共享噪声调度，构建联合扩散过程，强制模型显式学习图像细节与语义表示的联合分布。训练目标为联合去噪损失，同时最小化图像潜变量和语义特征的噪声预测误差：

$$ \mathcal{L}_{joint} = \mathbb{E}_{\mathbf{x}_0,\mathbf{z}_0,t} \Big[ \|\epsilon_{\theta}^x(\mathbf{x}_t,\mathbf{z}_t,t) - \epsilon_x\|^2 + \lambda_z \|\epsilon_{\theta}^z(\mathbf{x}_t,\mathbf{z}_t,t) - \epsilon_z\|^2 \Big] $$

此外，ReDi 解锁了一种新的推理策略——**表示引导（Representation Guidance）**，利用模型自身对语义特征的条件预测迭代精炼生成图像，进一步提升质量。

### 方法谱系与知识库定位

ReDi 位于生成式图像建模与表示学习的交叉点，与以下基线方法形成对比与互补：

| 方法 | 核心机制 | 与 ReDi 的关系 |
|------|----------|---------------|
| **DiT**（Peebles & Xie, 2023） | 扩散变换器，仅建模 VAE 潜变量 | ReDi 的基础架构，在其上扩展为联合建模 |
| **SiT**（Ma et al., 2024） | 随机插值模型，仅建模 VAE 潜变量 | ReDi 的另一种基础架构，同样可扩展 |
| **REPA**（Yu et al., 2025） | 通过蒸馏 DINOv2 特征进行表示对齐 | 正交互补：ReDi 联合建模，REPA 蒸馏对齐；两者结合可进一步降低 FID |

ReDi 的关键创新在于**将语义特征从“外部蒸馏目标”提升为“内部联合建模对象”**，从而在不增加复杂损失目标的情况下简化训练，并自然衍生出表示引导推理策略。

### 主要结果速览

在 ImageNet 256×256 基准上，ReDi 展现出显著的性能提升与训练加速：

- **无分类器引导（CFG）**：DiT-XL/2 w/ ReDi 在 400K 步即达到 FID **8.7**，超越基线 DiT-XL/2 在 7M 步的性能（FID 9.6）；SiT-XL/2 w/ ReDi 在 400K 步 FID 降至 **7.5**（基线 17.2）。
- **训练加速**：ReDi 将 DiT-XL/2 和 SiT-XL/2 的收敛速度提升约 **×23**，且比 REPA 快约 **×6**。
- **表示引导**：在 DiT-XL/2 上，表示引导将 FID 从 8.7 进一步降至 **5.9**。
- **有 CFG 场景**：ReDi 在 350 epoch 达到 FID **1.72**，优于 SiT-XL/2 在 1400 epoch 的 2.06。
- **与 REPA 互补**：结合两者训练 SiT-XL/2，400K 步 FID 降至 **5.3**，1M 步达 **3.5**。

> **注意**：以上结果来自 verified_analysis 中的实验证据（Table 1、Table 2、Table 4、Table 5），置信度 0.95-0.98。论文发表年份与会议信息未在元数据中提供，需手动核实。

生成式图像建模的核心目标是从噪声中合成高质量、高保真度的图像。当前主流框架——潜在扩散模型（Latent Diffusion Models, LDMs）——将图像压缩至低维VAE潜空间进行扩散过程，在计算效率与生成质量之间取得了平衡。然而，这一范式面临一个深层瓶颈：**模型在训练过程中必须同时维持精确的低级像素重建与开发具有语义意义的内部表示，这两种需求之间存在内在张力**。具体而言，扩散模型的目标函数（如噪声预测损失）天然倾向于像素级保真度，但高质量的图像合成同时要求模型理解对象的语义结构、部件关系与全局上下文——这些高级语义信息并非显式存在于VAE潜变量之中。

近年来，研究者尝试通过引入外部视觉表示来弥补这一缺口。代表性工作如**REPA**（Yu et al., 2025）提出表示对齐方法，在扩散模型训练过程中额外蒸馏预训练视觉编码器（如DINOv2）的特征，以提升生成图像的语义质量。然而，这类方法存在两个关键局限：其一，它们需要设计额外的复杂损失目标，增加了训练的超参数负担与工程复杂度；其二，蒸馏本质上是一种单向的知识注入——模型被动接收外部表示，而非主动学习图像与语义之间的联合生成规律，因此无法充分释放两种模态协同建模的潜力。

从更宏观的视角审视，扩散模型天然具备学习数据分布的能力，而预训练视觉编码器（如DINOv2）能够提取富含语义信息的特征表示。**能否将这两种能力统一在同一个扩散框架内，让模型直接学习图像潜变量与语义特征的联合分布？** 这一思路若得以实现，将从根本上消解前述张力：模型不再需要在“重建质量”与“语义理解”之间做出权衡，而是通过联合建模将两者内化为同一生成过程的两个互补侧面。

本文提出的**ReDi（Representation Diffusion）**正是沿着这一思路展开。其核心动机可概括为三个递进层次：

1. **简化训练**：摒弃额外的蒸馏损失，通过在同一扩散过程中联合建模VAE潜变量与DINOv2语义特征，让模型以统一目标学习两者的联合分布，从而降低训练复杂度并加速收敛。
2. **性能提升**：联合建模使模型能够直接整合互补的低级细节与高级语义信息，预期在相同训练预算下显著提升生成质量（以FID衡量）。
3. **解锁新能力**：一旦模型学会了语义特征的条件分布，便可在推理时引入一种全新的引导策略——**表示引导（Representation Guidance）**——利用模型自身的语义理解来迭代精炼生成图像，进一步提升质量，而无需依赖外部分类器或额外模型。

初步实验证据有力地支撑了这一动机的合理性：在ImageNet 256×256基准上，ReDi使DiT-XL/2在仅40万训练步数下即达到FID 8.7，超越了基线模型700万步的性能（FID 9.6），实现了约**23倍**的训练加速（Figure 2）。这表明，联合建模图像与语义特征不仅理论上自洽，而且在实践中带来了实质性的效率与质量增益。

## 核心方法与创新机理

ReDi 的核心创新在于将生成式图像建模与表示学习统一到同一个扩散过程中，从根本上改变了扩散变换器（DiT/SiT）的建模范式。与现有方法相比，其关键突破体现在以下四个维度。

### 1. 从“仅建模图像”到“联合建模图像-语义”

传统扩散变换器（**DiT**, Peebles & Xie, 2023；**SiT**, Ma et al., 2024）仅对 VAE 潜变量 $\mathbf{x}$ 进行去噪训练，模型缺乏对高层语义结构的显式认知。REPA（Yu et al., 2025）通过蒸馏 DINOv2 特征来改善语义质量，但引入了一个额外的、与生成目标解耦的对齐损失。

ReDi 的范式转变在于：**将 VAE 潜变量 $\mathbf{x}$ 和 DINOv2 语义特征 $\mathbf{z}$ 作为同一扩散过程的联合变量进行建模**。前向过程对两者施加共享的噪声调度：

$$\mathbf{x}_t = \sqrt{\bar{\alpha}_t} \mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon_x, \quad \mathbf{z}_t = \sqrt{\bar{\alpha}_t} \mathbf{z}_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon_z$$

训练目标从单一噪声预测扩展为联合损失：

$$\mathcal{L}_{joint} = \mathbb{E}_{\mathbf{x}_0,\mathbf{z}_0,t} \Big[ \|\epsilon_{\theta}^x(\mathbf{x}_t,\mathbf{z}_t,t) - \epsilon_x\|^2 + \lambda_z \|\epsilon_{\theta}^z(\mathbf{x}_t,\mathbf{z}_t,t) - \epsilon_z\|^2 \Big]$$

这一设计使模型显式学习两种模态的联合分布 $p(\mathbf{x}, \mathbf{z})$，而非依赖外部蒸馏信号。其因果机制在于：语义特征的预测任务迫使 Transformer 内部形成对图像结构的深层理解，这种理解通过共享的注意力层反向惠及图像潜变量的去噪过程。

### 2. 令牌融合策略：模态交互的两种路径

为实现 VAE 潜变量与语义特征的联合处理，ReDi 提出了两种令牌融合方案（Figure 4）：

- **合并令牌（Merged Tokens, MR）**：将两种模态的线性嵌入进行通道级求和，保持序列长度不变：
  $$\mathbf{h}_t = \mathbf{x}_t \mathbf{W}_{emb}^x + \mathbf{z}_t \mathbf{W}_{emb}^z \in \mathbb{R}^{L \times C_d}$$
  这种早期融合策略计算效率更高，但模态间的信息混合可能引入干扰。

- **分离令牌（Separate Tokens, SP）**：将两种令牌沿序列维度拼接，形成 $2L$ 长度的序列输入 Transformer。该方案保留了模态独立性，生成质量略优（FID 24.7 vs 25.7），但计算开销更大。

两种策略的核心差异在于交互粒度：MR 在嵌入层面强制融合，SP 则依赖自注意力机制自行发现跨模态关联。

### 3. PCA 降维：解决通道容量失衡的关键设计

DINOv2 的原始特征维度（768 维）远大于 VAE 潜变量维度（4 维），直接联合建模会导致 Transformer 的容量被语义特征主导。ReDi 通过主成分分析（PCA）将语义特征降至 $C_z'$ 维（默认 $C_z' = 8$），在保留必要语义信息的同时平衡两种模态的通道占比。

消融实验（Figure 7）揭示了一个反直觉现象：**增加 PCA 分量数超过 8 反而导致 FID 上升**。这表明过多的语义维度会引入冗余信息，干扰图像潜变量的去噪学习，而非提供额外帮助。这一发现暗示存在一个最优的语义压缩率，其本质是在“语义丰富度”与“通道容量平衡”之间的权衡。

### 4. 表示引导：利用语义理解迭代精炼生成

ReDi 的联合建模解锁了一种新的推理策略——**表示引导（Representation Guidance, RG）**。其核心思想是：利用模型自身对语义特征 $\mathbf{z}$ 的条件预测能力，在采样过程中引导图像潜变量向更高语义似然的方向移动：

$$\hat{\epsilon}_{\theta}(\mathbf{x}_t, \mathbf{z}_t, t) = \epsilon_{\theta}(\mathbf{x}_t, t) + w_r \left( \epsilon_{\theta}(\mathbf{x}_t, \mathbf{z}_t, t) - \epsilon_{\theta}(\mathbf{x}_t, t) \right)$$

其中 $w_r$ 为引导强度。该方法与传统的无分类器引导（CFG）在机制上有本质区别：CFG 利用类别标签的条件分布进行引导，而 RG 利用的是**连续语义表示的条件分布**，能够提供更细粒度的结构约束。实验表明，RG 将 DiT-XL/2 的 FID 从 8.7 降至 5.9（Table 4），且与 CFG 正交——两者可叠加使用以获得进一步增益。

### 创新总结

| 维度 | 基线方法（DiT/SiT） | REPA | ReDi |
|------|---------------------|------|------|
| 训练目标 | 仅 VAE 潜变量去噪 | VAE 去噪 + 表示对齐蒸馏 | 联合 VAE + 语义特征去噪 |
| 输入模态 | 单一 VAE 潜变量 | 单一 VAE 潜变量 | VAE 潜变量 + PCA 降维语义特征 |
| 语义利用方式 | 无 | 外部蒸馏（额外损失） | 内部联合建模（统一损失） |
| 推理策略 | CFG | CFG | CFG + 表示引导（RG） |

ReDi 的深层洞察在于：**生成与理解不应是分离的两个阶段，而应是同一过程的两种输出**。通过让扩散模型同时预测图像和语义，低层细节重建与高层语义理解之间的内在张力被转化为互补关系，从而在不增加复杂损失目标的前提下显著提升生成质量和训练效率。

ReDi（**Re**presentation **Di**ffusion）的核心思想是将图像生成与语义表示学习统一在一个扩散框架中，通过联合建模VAE潜变量与DINOv2语义特征的共享概率分布，消除了传统潜在扩散模型（LDM）在低级重建与高级语义之间的内在张力。

### 整体流程

ReDi的pipeline由五个核心模块串联构成，形成从图像到生成结果的完整闭环：

1. **语义特征提取与降维**：给定输入图像，首先通过预训练的SD-VAE编码器提取图像潜变量 $\mathbf{x}_0$，同时利用冻结的DINOv2编码器提取块级视觉表示。为缓解两种模态的通道容量不平衡，对DINOv2特征应用主成分分析（PCA），将其从768维压缩至默认8维，得到紧凑的语义表示 $\mathbf{z}_0$。

2. **联合前向扩散**：对 $\mathbf{x}_0$ 和 $\mathbf{z}_0$ 施加共享的噪声调度，构建统一的扩散前向过程：
   $$\mathbf{x}_t = \sqrt{\bar{\alpha}_t} \mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon_x, \quad \mathbf{z}_t = \sqrt{\bar{\alpha}_t} \mathbf{z}_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon_z$$
   两种模态在相同的时间步 $t$ 被同步加噪，迫使模型学习两者的联合分布 $q(\mathbf{x}_t, \mathbf{z}_t|\mathbf{x}_{t-1}, \mathbf{z}_{t-1})$。

3. **令牌融合与Transformer处理**：将加噪后的两种模态分别通过线性嵌入层投影至统一维度 $C_d$，随后采用**合并令牌**（Merged Tokens）策略进行通道级求和融合：
   $$\mathbf{h}_t = \mathbf{x}_t \mathbf{W}_{emb}^x + \mathbf{z}_t \mathbf{W}_{emb}^z \in \mathbb{R}^{L \times C_d}$$
   融合后的令牌序列保持长度 $L$ 不变，送入DiT或SiT架构的Transformer骨干进行处理。该策略相比分离令牌（Separate Tokens）串联方案计算效率更高，性能仅略低（FID 25.7 vs. 24.7）。

4. **联合去噪预测**：Transformer输出经两个模态专属的线性预测头，分别解码为图像潜变量的噪声预测 $\epsilon_{\theta}^x$ 和语义特征的噪声预测 $\epsilon_{\theta}^z$。训练目标为两者的加权联合损失：
   $$\mathcal{L}_{joint} = \mathbb{E}_{\mathbf{x}_0,\mathbf{z}_0,t} \Big[ \|\epsilon_{\theta}^x(\mathbf{x}_t,\mathbf{z}_t,t) - \epsilon_x\|^2 + \lambda_z \|\epsilon_{\theta}^z(\mathbf{x}_t,\mathbf{z}_t,t) - \epsilon_z\|^2 \Big]$$
   默认平衡权重 $\lambda_z = 1$，使模型同时学习精确的低级重建和语义一致的表示生成。

5. **表示引导（Representation Guidance）**：在推理时，利用模型自身对语义特征的条件预测能力，通过引导强度 $w_r$ 调整去噪过程：
   $$\hat{\epsilon}_{\theta}(\mathbf{x}_t, \mathbf{z}_t, t) = \epsilon_{\theta}(\mathbf{x}_t, t) + w_r \left( \epsilon_{\theta}(\mathbf{x}_t, \mathbf{z}_t, t) - \epsilon_{\theta}(\mathbf{x}_t, t) \right)$$
   该机制无需额外模型或复杂蒸馏目标，直接利用联合建模学到的语义理解迭代精炼生成图像。

### 与现有方法的关系

ReDi的设计逻辑与表示对齐方法**REPA**（Yu et al., 2025）形成互补：REPA通过额外的蒸馏损失将生成过程中的中间表示对齐到DINOv2特征空间，而ReDi将语义特征直接作为扩散过程的联合建模对象。两者可叠加使用，在SiT-XL/2上结合训练400K步即达到FID 5.3，1M步进一步降至3.5，验证了联合建模与表示对齐的协同效应。

### 关键设计决策

- **PCA降维至8维**：实验表明PCA分量数为8时获得最佳生成质量，增大分量数反而导致性能下降。这一反直觉现象是本文的开放问题之一，可能与高维语义特征对生成任务的干扰有关。
- **仅对VAE潜变量应用CFG**：消融实验显示，仅对图像潜变量施加无分类器引导（FID 2.39）优于同时对两种模态施加CFG（FID 2.86），表明语义特征的条件引导更适合通过表示引导机制实现，而非简单的联合CFG。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2504_16064/figures/001_Figure_1.jpg]]
*Figure 1: ReDi: Our generative image modeling framework bridges the gap between generative modeling and representation learning by leveraging a diffusion model that jointly captures low-level image details (via VAE latents) and high-level semantic features (via DINOv2). Trained to generate coherent image–feature pairs from pure noise, this unified latent-semantic dual-space diffusion approach significantly boosts both generative quality and training convergence speed*

ReDi 的核心架构由五个紧密协作的模块构成，其本质是将图像潜变量和语义特征纳入统一的扩散框架中进行联合建模。以下按流程顺序阐述各模块的设计逻辑与关键公式。

### 语义特征提取与降维

给定输入图像，首先通过预训练的 SD VAE 编码器提取图像潜变量 $\mathbf{x}_0 \in \mathbb{R}^{L \times C_x}$，同时通过冻结的 DINOv2 编码器提取块级语义特征 $\mathbf{z}_0 \in \mathbb{R}^{L \times C_z}$（默认 $C_z = 768$）。由于语义特征通道数远大于潜变量通道数（$C_x = 4$），直接联合建模会导致严重的通道不平衡问题。为此，ReDi 对 DINOv2 特征应用 PCA 降维，将维度从 $C_z$ 压缩至 $C_z'$（默认 $C_z' = 8$），在保留必要语义信息的同时简化预测任务。消融实验表明，PCA 分量数为 8 时获得最佳生成质量，继续增大分量数反而导致性能下降——这一反直觉现象的深层原因仍是一个开放问题。

### 联合前向扩散

降维后的语义特征 $\mathbf{z}_0$ 与 VAE 潜变量 $\mathbf{x}_0$ 共享同一噪声调度，构成联合前向扩散过程。对于时间步 $t$，两种模态分别独立地施加高斯噪声：

$$\mathbf{x}_t = \sqrt{\bar{\alpha}_t} \mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon_x, \quad \mathbf{z}_t = \sqrt{\bar{\alpha}_t} \mathbf{z}_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon_z$$

其中 $\epsilon_x, \epsilon_z \sim \mathcal{N}(0, \mathbf{I})$ 为独立的噪声样本，$\bar{\alpha}_t$ 为标准 DDPM 噪声调度系数。这一设计的核心洞察在于：通过强制模型在去噪过程中同时恢复两种模态，扩散模型被迫学习图像细节与语义结构的联合分布，从而在生成过程中内化高级语义理解。

### 令牌融合与 Transformer 处理

获得含噪的 $\mathbf{x}_t$ 和 $\mathbf{z}_t$ 后，需要将其融合为统一的令牌序列送入 DiT/SiT 架构。ReDi 探索了两种融合策略：

**合并令牌（Merged Tokens, MR）**：将两种模态的线性嵌入在通道维度上直接相加，保持序列长度 $L$ 不变：

$$\mathbf{h}_t = \mathbf{x}_t \mathbf{W}_{emb}^x + \mathbf{z}_t \mathbf{W}_{emb}^z \in \mathbb{R}^{L \times C_d}$$

其中 $\mathbf{W}_{emb}^x \in \mathbb{R}^{C_x \times C_d}$、$\mathbf{W}_{emb}^z \in \mathbb{R}^{C_z' \times C_d}$ 为可学习的嵌入矩阵，$C_d$ 为 Transformer 的隐藏维度。

**分离令牌（Separate Tokens, SP）**：将两种模态的嵌入沿序列维度拼接，形成长度为 $2L$ 的序列：

$$\mathbf{h}_t = \text{concat}\left(\mathbf{x}_t \mathbf{W}_{emb}^x, \mathbf{z}_t \mathbf{W}_{emb}^z\right) \in \mathbb{R}^{2L \times C_d}$$

消融实验显示，分离令牌策略略优于合并令牌（FID 24.7 vs 25.7），但合并令牌的计算效率更高，因为序列长度减半。融合后的令牌序列与时间步嵌入一同送入标准 DiT/SiT Transformer 块进行处理。

### 联合去噪预测

Transformer 的输出 $\mathbf{o}_t$ 通过两个独立的线性预测头分别解码为图像潜变量和语义特征的噪声预测：

$$\mathcal{L}_{joint} = \mathbb{E}_{\mathbf{x}_0,\mathbf{z}_0,t} \Big[ \|\epsilon_{\theta}^x(\mathbf{x}_t,\mathbf{z}_t,t) - \epsilon_x\|^2 + \lambda_z \|\epsilon_{\theta}^z(\mathbf{x}_t,\mathbf{z}_t,t) - \epsilon_z\|^2 \Big]$$

其中 $\epsilon_{\theta}^x$ 和 $\epsilon_{\theta}^z$ 分别为图像和语义特征的噪声预测头，$\lambda_z$ 为语义损失平衡权重（默认设为 1）。对于 SiT 框架，损失函数替换为对应的速度预测损失，但联合建模的结构保持一致。

### 表示引导（Representation Guidance）

ReDi 在推理时引入了一种新颖的引导策略，利用模型自身对语义特征的条件预测来精炼生成过程。其核心思想是修改采样时的后验分布，使生成样本偏向具有更高语义条件似然的区域：

$$\hat{p}_{\theta}(\mathbf{x}_t, \mathbf{z}_t) \propto p_{\theta}(\mathbf{x}_t) \, p(\mathbf{z}_t|\mathbf{x}_t)^{w_r}$$

在噪声预测范式下，这等价于对去噪预测进行线性插值：

$$\hat{\epsilon}_{\theta}(\mathbf{x}_t, \mathbf{z}_t, t) = \epsilon_{\theta}(\mathbf{x}_t, t) + w_r \left( \epsilon_{\theta}(\mathbf{x}_t, \mathbf{z}_t, t) - \epsilon_{\theta}(\mathbf{x}_t, t) \right)$$

其中 $w_r$ 为引导强度。当 $w_r = 0$ 时退化为无条件生成；$w_r = 1$ 时等价于标准条件生成；$w_r > 1$ 时增强语义条件的影响。实验表明，$w_r = 1.1$ 时 DiT-XL/2 的 FID 从 8.7 降至 5.9，验证了表示引导的有效性。值得注意的是，表示引导在无条件生成场景中尤为关键：DiT-XL/2 的无条件 FID 从 43.5 降至 22.6，降幅达 20.9。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2504_16064/figures/002_Figure_2.jpg]]
*Figure 2: Accelerated Training. Generative performance curves on Imagenet 2 5 6 $\times$ 2 5 6 without Classifier-Free Guidance. Left: Our ReDi accelerates convergence of DiT-XL/2 and SiT-XL/2 by approximately ×23. Right: ReDi converges ×6 faster than REPA. When applied on top of REPA delivers a ×11 speed-up*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2504_16064/figures/010_Figure_6.jpg]]
*Figure 6: VAE-only vs. VAE & DINOv2 CFG. FID scores for SiT-XL with ReDi (trained for 400K steps) as a function of Classifier-Free Guidance weight w, comparing two configurations: (1) applying CFG only to VAE latents (VAE-only CFG) versus (2) applying CFG to both VAE and DINOv2 representations (VAE & DINOv2 CFG). # Principal Components Figure 7: Effect of number of principal components. FID of DiT-B/2 w/ ReDi with different number of DINOv2 Principal Components. The vanilla DiT-B/2 is illustrated with gray. No Classifier-Free Guidance is used*

## 实验与关键发现

### 核心结果：无分类器引导下的性能与收敛加速

ReDi在ImageNet 256×256无条件类引导（w/o CFG）设置下展现出显著且一致的性能增益。表1汇总了DiT和SiT系列模型在400K训练步时的FID指标。

**Table 1** 的核心结论显示，ReDi使DiT-XL/2在400K步即达到FID 8.7，不仅大幅优于同步骤基线DiT-XL/2的19.5（Δ=-10.8），甚至超越了基线模型训练7M步的FID 9.6。在SiT架构上，SiT-XL/2 w/ ReDi在400K步取得FID 7.5，相比基线SiT-XL/2的17.2降低9.7。当训练延长至4M步时，SiT-XL/2 w/ ReDi的FID进一步降至3.3。

收敛加速效应在**Figure 2**中更为直观：左侧曲线表明ReDi将DiT-XL/2和SiT-XL/2的收敛速度提升约**23倍**；右侧曲线显示ReDi的收敛速度比REPA快约**6倍**。当ReDi与REPA叠加使用时（Table 5），二者互补性得到验证——SiT-XL/2在400K步FID降至5.3，1M步达3.5，实现了约**11倍**的综合加速。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2504_16064/figures/007_Table_5.jpg]]
*Table 5: ReDi with REPA. FID scores on ImageNet 256×256 w/o CFG*

### 有分类器引导下的SOTA对比

在启用CFG的设置下，ReDi同样具备竞争力。**Table 2** 显示，ReDi以SiT-XL/2为基座、仅训练350 epochs即取得FID 1.72，优于SiT-XL/2训练1400 epochs的2.06。这表明联合建模策略在有限训练预算下即可逼近或超越长时训练的基线。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2504_16064/figures/006_Table_2.jpg]]
*Table 2: Comparison with State-of-the-art. Quantitative evaluation on ImageNet 256 × 256 with Classifier-Free Guidance. Both REPA and ReDi (ours) employ SiT-XL/2 as the base model*

### 无条件生成与表示引导

ReDi在无条件生成任务上同样表现突出。**Table 3** 显示，DiT-XL/2 w/ ReDi在400K步的无条件FID为22.6（启用表示引导RG），而基线DiT-XL/2为43.5，降幅高达20.9。这验证了联合建模赋予模型的语义理解能力即使在没有类别条件时也能有效指导生成。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2504_16064/figures/008_Table_3.jpg]]
*Table 3: Unconditional Generation FID Performance. Results on ImageNet 256 × 256. For comparison, we include conditional generation results (shown in gray). Models at 400K steps. RG denotes using Representation Guidance. Table 4: FID with Representation Guidance. FID scores on ImageNet 256 × 256. RG denotes Representation Guidance. Models at 400K steps*

表示引导（Representation Guidance）的消融实验（**Table 4**）进一步量化其贡献：DiT-XL/2 w/ ReDi在无RG时FID为8.7，当引导强度$w_r=1.1$时FID降至5.9。这表明推理阶段利用模型自身的语义条件分布进行迭代精炼是提升质量的有效杠杆。

### 关键消融与设计选择

**CFG策略选择**：**Figure 6** 的消融表明，仅对VAE潜变量施加CFG（FID 2.39）优于同时对VAE和DINOv2特征施加CFG（FID 2.86）。这说明语义模态的引导信号与图像模态的引导信号之间存在冗余或干扰，单独引导图像侧更为有效。

**PCA分量数**：**Figure 7** 揭示了一个非单调现象——PCA分量数从1增至8时FID持续改善，但超过8后性能反而下降。8维PCA表示在压缩效率与语义保真度之间达到最优平衡；更高维度的表示可能引入噪声或加剧通道不平衡，损害联合学习。

**令牌融合策略**：**Table 6** 对比了分离令牌（SP）与合并令牌（MR）两种方案。SP策略FID为24.7，略优于MR的25.7，但MR在计算效率上更具优势（详见附录B的吞吐量测量）。这一权衡为实际部署提供了灵活选择空间。

### 失败模式与局限性

1. **表示多样性受限**：当前仅验证了DINOv2作为语义表示的单一来源，未探索融合多个异构视觉表示（如不同自监督模型）的潜力。
2. **PCA降维的天花板**：PCA分量数超过8后性能下降的深层原因尚未完全阐明，更复杂的压缩技术（如可训练自编码器）可能突破这一瓶颈。
3. **滥用风险**：生成模型性能的显著提升可能被滥用于虚假信息传播，需关注负向社会影响。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2504_16064/figures/005_Table_1.jpg]]
*Table 1: FID Comparisons. FID scores on ImageNet 256×256 without Classifier-Free Guidance for DiT and SiT models of various sizes with REPA and ReDi (ours)*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2504_16064/figures/011_Table_6.jpg]]
*Table 6: Performance of Modality Combination Strategies. FID scores on ImageNet 256 × 256 without CFG for DiT-B/2 with ReDi using Separate Tokens (SP) and Merged Tokens (MR). See Appendix B for details on throughput measurements*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2504_16064/figures/012_Table_7.jpg]]
*Table 7: Model configuration details. The configurations are the same for both DiT and SiT models*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2504_16064/figures/013_Table_8.jpg]]
*Table 8: Optimization details. The optimization hyperparameters for both DiT and SiT models*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2504_16064/figures/014_Table_9.jpg]]
*Table 9: Detailed evaluation for SiT-XL/2 w/ ReDi. All results are reported without classifier-free guidance*

## 定位与知识库关联

### 1. 与基线方法的关系

ReDi 的核心贡献在于将扩散模型的建模对象从单一的 VAE 潜变量空间扩展为**图像潜变量与语义特征的联合空间**，这一设计使其与现有方法形成明确的继承与超越关系。

**与 DiT / SiT 的关系（继承与扩展）**。ReDi 直接建立在扩散变换器（**DiT**，Peebles & Xie, 2023）和随机插值模型（**SiT**，Ma et al., 2024）的基础架构之上。两者的基线范式仅对 VAE 潜变量 $\mathbf{x}_t$ 进行噪声或速度预测，训练目标为 $\mathcal{L}_{simple} = \mathbb{E}_{\mathbf{x}_0, \epsilon, t} \| \epsilon_{\theta}(\mathbf{x}_t, t) - \epsilon \|^2$。ReDi 将这一范式扩展为联合建模：在相同噪声调度下同时对 VAE 潜变量 $\mathbf{x}_t$ 和 PCA 降维后的 DINOv2 语义特征 $\mathbf{z}_t$ 施加扩散过程，并将训练损失替换为联合损失 $\mathcal{L}_{joint}$（Eq. 6），其中语义特征的损失项由平衡权重 $\lambda_z$ 控制（默认 $\lambda_z = 1$）。这一扩展保持了原始架构的兼容性——Transformer 主干网络无需结构性修改，仅需在输入端增加语义令牌的嵌入与融合模块，并在输出端增加语义特征的预测头。

**与 REPA 的关系（互补而非替代）**。**REPA**（Yu et al., 2025）代表了另一条改进生成质量的路线——表示对齐（Representation Alignment），其核心是通过额外的蒸馏损失强制模型内部表示逼近预训练视觉编码器（如 DINOv2）的特征。ReDi 与 REPA 在机制上存在根本差异：REPA 将语义特征作为**外部监督信号**施加蒸馏约束，而 ReDi 将语义特征作为**联合生成目标**纳入扩散过程本身。这一差异带来了两方面的后果：（1）ReDi 无需设计复杂的蒸馏损失函数，训练目标更为简洁；（2）ReDi 在训练过程中显式学习了图像与语义的联合分布 $p(\mathbf{x}, \mathbf{z})$，从而解锁了表示引导（Representation Guidance）等新的推理策略。实验证据表明两者具有互补性：将 ReDi 与 REPA 结合训练 SiT-XL/2，在 400K 步时 FID 降至 5.3，1M 步时进一步降至 3.5（Table 5），显著优于任一方法单独使用的效果。

### 2. 适用边界与关键设计约束

**视觉表示的选择与降维约束**。当前 ReDi 的实现仅验证了 DINOv2 作为语义特征来源的有效性。DINOv2 特征具有高维度（768 维）和强语义表达能力，但直接将其纳入联合扩散过程会因通道数远大于 VAE 潜变量（4 通道）而造成严重的容量不平衡。ReDi 采用 PCA 将 DINOv2 特征降至 $C_z'$ 维（默认 $C_z' = 8$）来解决此问题。消融实验揭示了一个关键约束：**PCA 分量数并非越多越好**——当 $C_z'$ 从 8 增加至更高维度时，生成质量反而下降（Figure 7）。这一反直觉现象的可能解释是，过高的语义特征维度会挤占模型有限的建模容量，干扰对图像细节的学习。该发现暗示了更优降维策略（如训练自编码器进行非线性压缩）的研究空间。

**令牌融合策略的效率-性能权衡**。ReDi 探索了两种令牌融合方式（Figure 4）：合并令牌（Merged Tokens, MR）通过通道级求和 $\mathbf{h}_t = \mathbf{x}_t \mathbf{W}_{emb}^x + \mathbf{z}_t \mathbf{W}_{emb}^z$ 实现早期融合，保持序列长度 $L$ 不变；分离令牌（Separate Tokens, SP）则将两种模态的令牌沿序列维度级联，使序列长度翻倍至 $2L$。实验表明 SP 策略在生成质量上略优（FID 24.7 vs. 25.7），但 MR 策略具有更高的计算效率（Table 6）。这一权衡意味着在实际部署中需根据计算预算选择融合方式。

**表示引导的适用范围**。表示引导（Representation Guidance）在推理时通过调整条件分布 $p_{\theta}(\mathbf{x}_t, \mathbf{z}_t) \propto p_{\theta}(\mathbf{x}_t) p(\mathbf{z}_t|\mathbf{x}_t)^{w_r}$ 来提升生成质量（Eq. 13），在无条件生成场景下效果尤为显著——DiT-XL/2 w/ ReDi 的 FID 从 43.5 降至 22.6（Table 3）。然而，该策略的效果依赖于模型对联合分布的学习质量，且引导强度 $w_r$ 需要仔细调节（最优值约为 1.1，Table 4）。此外，Figure 6 的消融表明，在 CFG 场景下仅对 VAE 潜变量施加引导（FID 2.39）优于同时对两种模态施加引导（FID 2.86），提示多模态引导策略的设计需要更精细的理论分析。

### 3. 局限性与开放问题

**已识别的局限性**：

1. **单一视觉表示的验证**。当前工作仅验证了 DINOv2 一种视觉表示的有效性，尚未探索融合多个不同属性的预训练表示（如 CLIP、MAE、DINO 等）能否带来进一步的增益。不同自监督模型捕获的语义属性存在差异，多表示融合可能是一个有前景的方向。

2. **PCA 降维的次优性**。PCA 作为线性降维方法，可能无法充分保留 DINOv2 特征的表达能力。更复杂的压缩技术（如训练专用的自动编码器或使用可学习的投影层）可能进一步提升性能，尤其是当需要保留更细粒度的语义信息时。

3. **潜在的社会风险**。生成模型性能的提升可能加剧虚假信息传播、深度伪造等滥用风险。论文未讨论针对此类风险的具体缓解措施。

**值得关注的开放问题**：

1. **PCA 分量数的反直觉效应**。为何增加 PCA 分量数超过 8 反而导致生成质量下降？是否存在一个理论上的最优信息瓶颈，使得语义特征的维度恰好平衡了"提供足够语义引导"与"避免挤占图像建模容量"两个目标？

2. **表示引导的理论理解**。表示引导与现有的引导方法（如 CLIP 引导、分类器引导）在数学形式上有何本质区别？其提升生成质量的机制是源于更好的语义对齐，还是源于对采样动力学的正则化效应？

3. **多模态扩展的可能性**。联合建模方案能否扩展到其他模态？例如，将文本嵌入、深度图或分割掩码与图像潜变量在同一扩散过程中联合建模，有望实现更通用的多模态生成框架。这一扩展需要解决不同模态间的维度匹配、噪声调度协调等问题。

4. **与自回归生成范式的联系**。ReDi 通过联合建模图像与语义特征，实际上在扩散框架内隐式地建立了一种"图像-语义"的双向生成能力。这一能力与自回归视觉生成模型中"next-token prediction"所学习的表示之间存在何种理论联系，值得深入探讨。

## 原文 PDF

![[paperPDFs/arxiv_2025/ReDi_Boosting_Generative_Image_Modeling_via_Joint_Image_Feature_Synthesis.pdf]]
