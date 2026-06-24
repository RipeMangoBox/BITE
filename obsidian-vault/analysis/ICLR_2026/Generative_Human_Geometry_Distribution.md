---
title: "Generative Human Geometry Distribution"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Generative_Human_Geometry_Distribution.pdf
openreview_forum_id: YsQM7sQl0j
aliases:
- GHGDH
- GHGD
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "将几何分布编码为2D特征图替代网络参数存储，并将流匹配的源分布从高斯分布替换为更接近目标的人体SMPL模板分布，配合训练对构造与分布归一化。"
primary_logic: "通过将人体几何分布压缩到结构化2D特征图并利用SMPL模板作为概率流的起点，大幅降低了流匹配学习难度，使模型能够高效扩展到数据集规模，同时实现高保真、姿态感知的几何生成。"
claims:
- "我们使用2D特征图而非网络权重来编码几何分布，这提供了泛化的表示方式。"
- "我们采用SMPL模板分布替代高斯分布并改进流速度场，显著提升训练效率。"
- "我们的方法在THuman2数据集上对比gDNA，几何质量（FID）从42.90降至16.16，相对提升57%。"
- "通过构造近邻训练对并添加扰动，结合分布归一化，模型收敛速度与质量均优于未优化版本。"
---

# Generative Human Geometry Distribution

> [!tip] 核心洞察
> 通过将人体几何分布压缩到结构化2D特征图并利用SMPL模板作为概率流的起点，大幅降低了流匹配学习难度，使模型能够高效扩展到数据集规模，同时实现高保真、姿态感知的几何生成。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 生成式人体几何分布 |
| 英文题名 | Generative Human Geometry Distribution |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=YsQM7sQl0j) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Generative Human Geometry Distribution (HGD) |
| Dataset | THuman2 (pose-conditioned generation), THuman2 (dataset-scale reconstruction), 4DDress (novel pose generation) |

> [!tip] 效果简介
> - THuman2 (pose-conditioned generation) 上，FID (normal maps, lower is better) 为 16.16 (raw geometry)，对比 gDNA: 42.90 (raw geometry)，变化 减少26.74 (相对提升57%)。
> - THuman2 (dataset-scale reconstruction) 上，Chamfer Distance (lower is better) 为 0.0032，对比 Zhang et al. (geometry distributions): 0.0101，变化 减少0.0069。
> - 4DDress (novel pose generation) 上，User study: Quality (1-5) 为 4.04，对比 gDNA: 2.54，变化 +1.50。

## 概述

人体几何生成的核心瓶颈在于：现有几何分布方法将单个几何体的信息直接编码在流网络参数中，导致无法高效扩展到大规模数据集；同时，从高斯分布到多样化人体形状的流匹配训练效率低下，难以捕获宽松衣物的细粒度细节与姿态关联。

本文提出 **Generative Human Geometry Distribution (HGD)**，通过两个关键设计解决上述问题：

1. **2D特征图编码**：将几何分布压缩为结构化的2D特征图（$\mathbb{R}^{8 \times 24 \times 24}$），替代网络权重作为分布载体，提供泛化的表示方式。
2. **SMPL模板先验**：将流匹配的源分布从高斯分布替换为更接近目标的SMPL模板分布，配合最近邻训练对构造与分布归一化，大幅降低流匹配学习难度。

方法采用两阶段训练范式：首先通过自动解码器将目标几何体压缩为特征图，再在潜空间上训练扩散流模型实现姿态条件的随机生成与新姿态生成。

在THuman2数据集上，HGD将原始几何FID从gDNA的42.90降至16.16，相对提升57%；数据集规模重建的Chamfer距离从0.0101降至0.0032。在4DDress新姿态生成任务上，用户评分的质量（4.04 vs. 2.54）与物理合理性（4.36 vs. 2.66）均显著优于现有方法。

## 背景与动机

高保真三维人体生成是计算机视觉与图形学领域的核心问题，其目标是从姿态、身份等条件信号中合成具有丰富几何细节的数字化人体。该任务面临双重挑战：一方面需要捕获衣物褶皱、发型纹理等细粒度几何特征，另一方面必须保证生成结果在任意姿态下的物理合理性。

现有方法可大致归为三类。基于隐式函数的方法（如 **gDNA** (Xu et al., CVPR 2022)、**ENARF** (Noguchi et al., CVPR 2022)）通过神经网络建模连续占据场或符号距离场，能够表达连续表面，但对宽松衣物和复杂拓扑的支持有限。基于显式表示的方法（如 **EVA3D** (Hong et al., CVPR 2022)）利用三平面或体素网格生成几何，细节保真度受限于网格分辨率。基于点云或高斯泼溅的方法（如 **E3Gen** (Zhang et al., ACM Multimedia 2024)）虽能高效渲染，但在几何一致性和随机采样多样性上存在不足。**Table 1** 系统对比了各类方法在宽松衣物、可扩展性和细节表现三个维度的差异，揭示了当前技术的结构性短板。

### 瓶颈分析：几何分布学习的效率困境

上述方法的根本瓶颈并非表示能力不足，而是**几何分布建模的效率问题**。具体而言：

1. **参数化存储的扩展性障碍**：现有几何分布方法（如基于流匹配的框架）将单个几何体的分布信息直接编码到流网络的权重参数中。当数据集规模从数十个样本扩展到数百甚至数千个身份时，每个几何体都需要独立维护一组网络参数，存储开销和优化难度呈线性增长，难以规模化部署。

2. **流匹配的源-目标分布鸿沟**：传统流匹配方法以多元高斯分布 $\mathcal{N}(0,1)$ 作为源分布，目标是复杂的人体几何表面分布。这两种分布在拓扑结构和几何形态上差异巨大，导致流速度场的学习极为困难——模型需要“凭空”将无结构的噪声映射为具有人体拓扑约束的精细几何，训练收敛缓慢且容易产生伪影。

3. **姿态-几何耦合的弱建模**：现有方法通常将姿态条件（如SMPL顶点或3D关键点）直接拼接到网络输入，缺乏对姿态如何系统性影响衣物形变的显式建模。这导致在夸张姿态或宽松服饰场景下，生成结果出现穿模、孔洞或细节丢失等问题。

### 本文动机与核心思路

针对上述瓶颈，本文提出**生成式人体几何分布（Generative Human Geometry Distribution, HGD）**方法，其核心洞察在于：**通过将几何分布压缩到结构化2D特征图并利用SMPL模板作为概率流的起点，可以大幅降低流匹配的学习难度**。

具体而言，HGD从两个维度重构了几何分布学习范式：

- **表示层面**：将几何分布编码为维度为 $\mathbb{R}^{8\times24\times24}$ 的压缩2D特征图 $z_{\mathcal{T}|\mathcal{S}}$，而非网络权重。这种泛化的表示方式使模型能够高效扩展到大规模数据集，同时保留了条件生成所需的身份与几何信息。

- **分布层面**：将流匹配的源分布从高斯分布替换为SMPL模板表面分布 $\Phi_{\mathcal{S}}$，并通过最近邻配对与零中心化归一化构造训练对。由于SMPL模板在拓扑上与目标人体几何高度相似，流速度场只需学习从模板到具体几何的“残差位移”，学习难度显著降低。

基于上述设计，HGD采用两阶段训练范式：第一阶段通过自动解码器（auto-decoder）将目标几何压缩为特征图；第二阶段在特征图潜空间上训练扩散流模型，实现姿态条件的随机生成和新姿态生成（**Figure 2**）。实验表明，该方法在THuman2数据集上将原始几何的FID从42.90降至16.16，相对提升57%（**Table 4**），并在4DDress数据集的新姿态生成任务中显著优于现有方法（**Table 5**）。

## 核心创新

本文提出的 **Generative Human Geometry Distribution (HGD)** 方法，针对现有几何分布方法的两大瓶颈——**网络参数存储无法规模化**与**高斯分布流匹配训练低效**——进行了系统性重构，核心创新体现在三个相互耦合的层面。

### 1. 几何分布的压缩编码：从网络权重到2D特征图

现有方法（如 Zhang et al., 2025）将单个几何体的分布信息直接编码在流网络权重中，每新增一个几何体就需要独立的网络参数，无法扩展到大规模数据集。HGD 将这一范式彻底翻转：**将几何分布压缩为结构化的 2D 特征图** $z_{\mathcal{T}|\mathcal{S}} \in \mathbb{R}^{8 \times 24 \times 24}$，而非网络权重。

具体而言，HGD 采用**自动解码器（auto-decoder）** 框架：每个目标几何体 $\mathcal{T}$ 被压缩为一个低维特征图，解码器 $\mathrm{Dec}_\phi$ 将该特征图与 SMPL 顶点图拼接后上采样，获得逐点的条件潜变量。这一设计使几何分布从“网络参数”变为“数据”，为后续在潜空间训练生成模型奠定了基础。

消融实验（Table 3）证实，自动解码器在表面距离指标上显著优于基于自编码器的 **VecSet**（Zhang et al., SIGGRAPH 2023）和 FeatureMap 变体，验证了压缩编码的有效性。

### 2. 流匹配源分布重构：从高斯分布到SMPL模板分布

传统流匹配以多元高斯分布 $\mathcal{N}(0,1)$ 为源分布，需要学习从噪声到复杂人体几何的全局变换，训练效率极低。HGD 的第二个关键创新是**将源分布替换为 SMPL 模板表面分布 $\Phi_S$**——一个与目标人体几何拓扑一致、空间邻近的分布。

这一替换大幅降低了流匹配的学习难度：网络只需学习从 SMPL 模板到目标几何的位移场 $\Delta\mathbf{x} = \mathbf{x}_1 - \mathbf{x}_0'$，而非从噪声重建整个几何体。为进一步增强训练稳定性，HGD 引入了三项配套设计：

- **最近邻训练对构造**：对每个目标几何点 $\mathbf{x}_1$，在 SMPL 模板上寻找最近点 $\mathbf{x}_0'$ 形成训练对，并添加高斯扰动 $\mathcal{N}(0,\sigma)$ 以增强样本多样性。
- **分布归一化**：将源分布和目标分布均减去 $\mathbf{x}_0'$，使源分布变为零中心高斯 $\mathcal{N}(0,1)$，消除空间位置偏差对训练的影响；同时将 $\mathbf{x}_0'$ 重新注入网络作为条件信号，缩放隐藏特征。
- **稀疏采样策略**：在构造训练对时对 SMPL 点进行稀疏采样，避免宽松衣物区域因密集匹配导致的孔洞伪影（Fig. 6 第一行 vs 第二行）。

Table 2 的数据集规模消融实验表明，完整分布公式（含配对构造与归一化）的 Chamfer 距离为 0.0032，显著优于无配对变体（0.0101）和无归一化变体，验证了每项设计的必要性。

### 3. 两阶段生成框架：压缩-生成解耦

HGD 将几何生成拆解为两个阶段：（1）**自动解码器压缩阶段**，将每个几何体编码为特征图；（2）**潜空间流生成阶段**，在特征图空间训练扩散流模型，实现姿态条件随机生成和新姿态生成。

这种解耦设计使生成模型不再直接操作高维点云，而是在紧凑的潜空间（$8 \times 24 \times 24$）中学习分布，显著降低了计算开销。姿态条件通过将 SMPL 顶点位置渲染为 UV 图并以残差连接注入 UNet 实现，新姿态生成任务则额外引入冻结的 DINO-ViT 图像编码器提取身份特征。

### 创新耦合逻辑

三项创新形成因果闭环：**SMPL 源分布**降低了流匹配的学习难度，使**自动解码器压缩**成为可能；**2D 特征图编码**将分布信息从网络参数中解耦，使**两阶段生成框架**能够规模化；而**分布归一化与训练对构造**则为这一耦合提供了训练稳定性保障。三者共同实现了从“单几何体网络参数”到“数据集规模潜空间生成”的范式跃迁。

## 整体框架

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_YsQM7sQl0j/figures/020_Figure_14.jpg]]
*Figure 14: This figure shows the results of our method after full training, using the same identities and poses as in Fig. 7*

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_YsQM7sQl0j/figures/005_Figure_4.jpg]]
*Figure 4: Overview of our method. (a) We encode a geometry into a feature map, which is decompressed with a SMPL vertex map. The decompressed feature serves as a condition for our denoising network. (b) The human generation task is formulated as the conditional generation of feature maps, guided by the SMPL vertex map, optionally incorporating additional conditioning inputs*

HGD 采用**两阶段生成范式**，将人体几何分布的学习分解为压缩编码与潜在空间生成两个子问题。图 4 给出了完整的架构概览。

**第一阶段：几何分布压缩。** 给定一个目标人体几何体 $\mathcal{T}$ 及其对应的 SMPL 模板 $\mathcal{S}$，系统通过自动解码器（auto-decoder）将 $\mathcal{T}$ 相对于 $\mathcal{S}$ 的几何偏移信息压缩为一个紧凑的 2D 特征图 $\mathbf{z}_{\mathcal{T}|\mathcal{S}} \in \mathbb{R}^{8 \times 24 \times 24}$。该特征图并非直接存储点云坐标，而是编码了目标几何体在 SMPL 模板各顶点邻域内的条件分布信息。解码时，SMPL 顶点位置被渲染为 UV 图，与特征图拼接后经 UNet 风格的上采样网络 $\mathrm{Dec}_\phi$ 处理，为每个 SMPL 采样点 $\mathbf{x}_0'$ 输出一个条件潜变量 $\mathrm{Dec}_\phi(\mathbf{z}_{\mathcal{T}|\mathcal{S}})(\mathbf{x}_0')$。

**第二阶段：潜在特征图生成。** 在第一阶段获得所有训练样本的特征图 $\{\mathbf{z}_{\mathcal{T}|\mathcal{S}}\}$ 后，系统在特征图空间上训练一个扩散流模型。该生成模型以 SMPL 顶点 UV 图为条件，并可选择性地融合来自 DINO-ViT 编码的正面法向图特征作为身份条件，从而实现两类生成任务：（1）给定姿态的随机人体生成；（2）给定身份图像的新姿态生成。

**流匹配的源分布改进。** 区别于先前工作从高斯分布 $\mathcal{N}(0,1)$ 出发的做法，HGD 将流匹配的源分布替换为 SMPL 模板表面分布 $\Phi_\mathcal{S}$，并通过最近邻配对与扰动策略构造训练对 $(\mathbf{x}_0', \mathbf{x}_1)$。在此基础上，系统对源和目标分布同时进行零中心化归一化——减去 $\mathbf{x}_0'$ 后源分布退化为标准高斯，目标变为位移场 $\Delta\mathbf{x} = \mathbf{x}_1 - \mathbf{x}_0'$，而 $\mathbf{x}_0'$ 本身作为条件信号重新注入去噪网络。这一设计大幅降低了流匹配的学习难度，使得模型能够高效扩展到数据集规模训练。

**端到端推理流程。** 推理时，第二阶段生成的特征图送入第一阶段的解码器与去噪网络，直接在 SMPL 模板表面采样点上回归几何位移，输出高保真的人体点云。整个过程无需渲染增强即可获得高质量的原始几何输出。

## 核心模块与公式推导

### 几何分布建模的核心瓶颈与解决路径

现有几何分布方法（如Zhang et al., 2025）将单个几何体的信息直接编码到流网络权重中，导致两个根本性缺陷：一是无法高效扩展到大规模数据集，每个几何体需独立维护一组网络参数；二是从高斯分布到多形状的流匹配训练效率低下，难以捕获细粒度衣物细节与姿态的关联。HGD通过两个关键设计打破这一瓶颈：**将几何分布压缩为2D特征图**替代网络参数存储，以及**将流匹配的源分布从高斯分布替换为更接近目标的SMPL模板分布**。

### 流匹配基础

HGD建立在条件流匹配（Conditional Flow Matching）框架之上。给定源分布 $\mathbf{p}$ 和目标分布 $\mathbf{q}$，流匹配的核心目标是学习一个速度场 $u_\theta$，使得从 $\mathbf{p}$ 采样的点 $\mathbf{x}_0$ 沿该速度场演化后逼近 $\mathbf{q}$ 的采样点 $\mathbf{x}_1$。基础训练目标为：

$$\arg \min_\theta \mathbb{E}_{\mathbf{x}_0 \sim \mathbf{p}, \mathbf{x}_1 \sim \mathbf{q}, t \in [0,1]} \| u_\theta(\mathbf{x}_t, t) - (\mathbf{x}_1 - \mathbf{x}_0) \|$$

其中 $\mathbf{x}_t = (1-t)\mathbf{x}_0 + t\mathbf{x}_1$ 为线性插值路径。该公式定义在Sec 3，是后续所有模块推导的数学基础。

### 模块一：SMPL模板分布替代高斯分布

直接使用高斯分布作为源分布的朴素做法，要求流网络学习从无结构噪声到复杂人体几何的完整映射，训练难度极大。HGD的核心创新是将源分布替换为SMPL模板表面分布 $\Phi_S$，使流匹配的起点本身已具备人体拓扑结构。朴素目标函数为：

$$\arg \min_\theta \mathbb{E}_{\mathbf{x}_0 \sim \Phi_S, \mathbf{x}_1 \sim \Phi_T} \| u_\theta(\mathbf{x}_t, t) - (\mathbf{x}_1 - \mathbf{x}_0) \|$$

然而，SMPL模板点与目标几何点之间缺乏自然对应关系。HGD通过**最近邻配对**构建训练对：对于每个目标点 $\mathbf{x}_1$，在SMPL点集中寻找最近点 $\mathbf{x}_0'$：

$$\mathbf{x}_0' = \arg \min_{\mathbf{x}_0 \in \{\mathbf{x}_0\}_S} \|\mathbf{x}_1 - \mathbf{x}_0\|_2$$

为进一步增强样本多样性，在 $\mathbf{x}_0'$ 上添加高斯扰动 $\mathbf{n} \sim \mathcal{N}(0, \sigma)$，使源分布变为 $\mathcal{N}(\mathbf{x}_0', \sigma)$。

### 模块二：分布归一化

最近邻配对策略在数据集层面存在空间不平衡问题：不同区域的SMPL点被选为最近邻的频率差异显著，导致流网络对高频区域过拟合、低频区域欠拟合。HGD引入**分布归一化**解决此问题：将源分布和目标分布同时减去 $\mathbf{x}_0'$，使源分布退化为零中心高斯 $\mathcal{N}(0,1)$，目标变为位移场 $\Delta\mathbf{x} = \mathbf{x}_1 - \mathbf{x}_0'$。此时 $\mathbf{x}_0'$ 不再作为采样源，而是作为条件信号重新注入网络，用于缩放隐藏层特征。归一化后的完整流匹配目标为：

$$\arg \min_\theta \mathbb{E}_{\mathbf{n} \sim \mathcal{N}(0,1), (\mathbf{x}_0', \mathbf{x}_1) \in \{(\mathbf{x}_0', \mathbf{x}_1)\}_{\mathcal{T}}} \| u_\theta(\mathbf{x}_t, t | \mathbf{x}_0') - (\Delta\mathbf{x} - \mathbf{n}) \|$$

其中 $\mathbf{x}_t = (1-t)\mathbf{n} + t\Delta\mathbf{x}$。该公式（Eq.(4)，Sec 4.2）是HGD分布建模的核心数学表达。

### 模块三：自动解码器与2D特征图编码

为将几何分布从网络权重中解耦，HGD引入自动解码器（auto-decoder）架构。每个目标几何体 $\mathcal{T}$ 被压缩为一个紧凑的2D特征图 $\mathbf{z}_{\mathcal{T}|\mathcal{S}} \in \mathbb{R}^{8 \times 24 \times 24}$，而非网络权重。解码器 $\mathrm{Dec}_\phi$ 是一个UNet风格网络，接收SMPL顶点位置渲染的UV图作为输入，通过上采样与 $\mathbf{z}_{\mathcal{T}|\mathcal{S}}$ 拼接，在UV坐标上输出逐点条件潜变量 $\mathrm{Dec}_\phi(\mathbf{z}_{\mathcal{T}|\mathcal{S}})(\mathbf{x}_0')$。该潜变量作为去噪网络的附加条件信号，与 $\mathbf{x}_0'$ 一起引导流生成。

完整的联合训练目标将特征图优化、解码器参数优化和去噪网络优化统一在一个损失函数中：

$$\arg \min_{\theta, \phi, \{\mathbf{z}_{\mathcal{T}|\mathcal{S}}\}} \mathbb{E}_{(\mathcal{S},\mathcal{T})\in\mathcal{D}} \mathbb{E}_{\mathbf{n}, (\mathbf{x}_0', \mathbf{x}_1)} \| u_\theta(\mathbf{x}_t, t | \mathbf{x}_0', \mathrm{Dec}_\phi(\mathbf{z}_{\mathcal{T}|\mathcal{S}})(\mathbf{x}_0')) - (\Delta\mathbf{x} - \mathbf{n}) \|$$

该公式（Eq.(6)，Sec 4.3）是HGD完整训练目标的数学表达，涵盖了自动解码器潜变量、解码器和去噪网络的端到端联合优化。

### 模块四：潜在流生成模型

完成自动解码器训练后，每个几何体拥有对应的特征图 $\mathbf{z}_{\mathcal{T}|\mathcal{S}}$。第二阶段在特征图空间上训练扩散/流模型，实现姿态条件的随机生成和新姿态生成。对于姿态条件注入，HGD将SMPL顶点位置渲染为UV图并以残差连接方式注入UNet架构，相比直接拼接3D关键点或SMPL顶点的方式，姿态引导更高效。对于新姿态生成任务，额外引入冻结的DINO-ViT模型提取正面法向图特征作为身份条件。

### 关键公式汇总

| 公式 | 含义 | 锚点 |
|------|------|------|
| $\arg \min_\theta \mathbb{E}_{\mathbf{x}_0 \sim \mathbf{p}, \mathbf{x}_1 \sim \mathbf{q}, t} \| u_\theta(\mathbf{x}_t, t) - (\mathbf{x}_1 - \mathbf{x}_0) \|$ | 基础流匹配损失，$\mathbf{x}_t = (1-t)\mathbf{x}_0 + t\mathbf{x}_1$ | Eq.(1), Sec 3 |
| $\arg \min_\theta \mathbb{E}_{\mathbf{n}, (\mathbf{x}_0', \mathbf{x}_1)} \| u_\theta(\mathbf{x}_t, t \| \mathbf{x}_0') - (\Delta\mathbf{x} - \mathbf{n}) \|$ | 归一化流匹配目标，源分布为零中心高斯，目标为位移场，$\mathbf{x}_0'$ 作为条件 | Eq.(4), Sec 4.2 |
| $\arg \min_{\theta, \phi, \{\mathbf{z}_{\mathcal{T}\|\mathcal{S}}\}} \mathbb{E}_{(\mathcal{S},\mathcal{T})\in\mathcal{D}} \mathbb{E}_{\mathbf{n}, (\mathbf{x}_0', \mathbf{x}_1)} \| u_\theta(\mathbf{x}_t, t \| \mathbf{x}_0', \mathrm{Dec}_\phi(\mathbf{z}_{\mathcal{T}\|\mathcal{S}})(\mathbf{x}_0')) - (\Delta\mathbf{x} - \mathbf{n}) \|$ | 完整训练目标，联合优化自动解码器潜变量、解码器参数和去噪网络 | Eq.(6), Sec 4.3 |

### 训练策略：两阶段范式

HGD采用两阶段训练范式（Sec 4.1, Sec 4.4）：第一阶段通过自动解码器将每个几何体压缩为2D特征图，同时训练解码器和去噪网络完成重建；第二阶段冻结自动解码器，在特征图空间上训练潜在扩散/流模型，实现从随机噪声或身份条件到特征图的生成，再经解码器还原为几何体。这一设计将几何分布学习解耦为“压缩-生成”两步，使模型能够高效扩展到数据集规模。

## 实验与分析

### 主结果：姿态条件随机生成

本节评估模型在给定姿态下随机生成人体几何的能力。所有方法均在THuman2数据集上训练，评估时从每个身份渲染50个视角的法向图，共生成25,000张图像计算FID。为避免渲染增强带来的不公平优势，核心指标基于原始几何输出（raw geometry）计算。

**Table 4** 汇总了各方法的FID对比。HGD在原始几何FID上达到 **16.16**，相比当前最优的隐式函数方法 **gDNA**（Xu et al., CVPR 2022）的42.90，**绝对降低26.74，相对提升57%**。在渲染后FID指标上，HGD同样以16.16优于gDNA的17.41（相对提升约7%），表明几何质量的提升直接转化为视觉质量的改善。其他对比方法中，**E3Gen**（Zhang et al., ACM Multimedia 2024）的原始几何FID为25.24，**GetAvatar**（Zhang et al., ICCV 2023）为26.64，HGD分别领先36%和39%。


![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_YsQM7sQl0j/figures/011_Table_4.jpg]]
*Table 4: Comparison of FID scores. The * results are adopted from E3Gen (Zhang et al., 2024d). For some methods, the results are rendered directly from their raw geometries, so the numbers in both rows are identical*

定性结果见 **Figure 8**。E3Gen在宽松衣物区域合成出不自然的形状，法向颜色不一致；GetAvatar生成的布料褶皱呈现不自然的方向性纹理；gDNA的法向图褶皱随机且不符合物理规律。相比之下，HGD生成的法向图纹理清晰、方向合理，几何细节更接近真实扫描。

### 主结果：新姿态生成

新姿态生成任务评估模型在给定身份条件下生成未见姿态的能力。在4DDress数据集上进行用户研究，25名参与者对2个身份×8个姿态的结果进行盲评（1-5分制）。

**Table 5** 显示，HGD在生成质量上获得 **4.04** 分，物理合理性获得 **4.36** 分，分别比gDNA的2.54和2.66高出 **+1.50** 和 **+1.70**。这表明HGD的姿态感知特征图能有效捕获身份相关的衣物细节，并在新姿态下保持物理一致性。


![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_YsQM7sQl0j/figures/013_Table_5.jpg]]
*Table 5: User study on quality and physical plausibility*

**Figure 9** 展示了挑战性案例，包括夸张姿态、裙装和宽松服饰。HGD在这些场景下仍能生成合理的褶皱和变形，但论文指出极端姿态下点云稀疏性可能导致局部细节缺失——这是通过泊松表面重建验证过的边界情况，仍属潜在局限。

### 消融实验：几何分布公式

论文系统消融了三个关键设计选择：训练对构造、源分布选择和分布归一化。

**Table 2** 报告了不同分布公式的Chamfer距离。在数据集规模训练中，完整HGD（含配对+归一化）达到 **0.0032**，显著优于无配对变体（w/o Pairs）的0.0101和无分布归一化变体（w/o DistNorm）的0.0056。值得注意的是，无归一化变体在单几何体拟合实验中可达到最低Chamfer距离（见 **Figure 5**），但在多姿态数据集中性能退化——论文将此归因于该变体过度拟合单一几何而缺乏跨姿态泛化能力。HGD的归一化策略在单几何精度与数据集泛化之间取得了最佳平衡。


![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_YsQM7sQl0j/figures/010_Table_2.jpg]]
*Table 2: Chamfer distance of different distribution formulations*

**Figure 7** 可视化了训练至第30,000次迭代时各公式的生成结果。无配对变体产生大量噪声和缺失区域，无归一化变体虽有改善但仍存在局部伪影，完整HGD最接近真实几何。


![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_YsQM7sQl0j/figures/007_Figure_7.jpg]]
*Figure 7: Visualization results of different geometry distribution formulations at the 30, 000th training iteration. GT represents the ground-truth result*

**Figure 6** 对比了训练对构造策略。直接在密集SMPL网格上搜索最近点（第二行）会在宽松衣物区域产生孔洞伪影；HGD采用的稀疏采样SMPL点并利用KNN构造训练对（第一行）有效避免了这一问题，因为稀疏采样允许更大的位移容差，使流匹配更容易学习宽松衣物的变形。

### 消融实验：网络架构

**Table 3** 对比了不同编码器设计的表面距离。基于自编码器的 **VecSet**（Zhang et al., SIGGRAPH 2023）和FeatureMap变体在重建精度上均不及HGD的自动解码器（auto-decoder）。FeatureMap相比VecSet有所改善，但自动解码器通过联合优化潜变量和网络参数，实现了最优的压缩-重建平衡。


![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_YsQM7sQl0j/figures/009_Table_3.jpg]]
*Table 3: Surface distance comparison between various designs*

### 失败模式与局限

论文明确指出的局限包括：

1. **非均匀采样**：目标几何体表面存在点密度不均匀问题，稀疏区域可能导致局部细节缺失。
2. **服装泛化受限**：模型无法生成训练数据中完全未出现的新服装款式，生成多样性受限于数据集覆盖范围。
3. **UV接缝伪影**：UV参数化引入的接缝在生成结果中可见，当前未针对真实服装分片进行优化。
4. **极端姿态下的稀疏性**：面对夸张姿态和宽松衣物时，点云覆盖不足可能导致局部几何退化（尽管泊松重建在边界情况下表现出一定鲁棒性）。

这些局限指向了论文提出的开放问题：如何实现目标表面的均匀采样、如何扩展至训练数据之外的服装风格、以及如何消除UV贴图接缝伪影。

### 补充图表

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_YsQM7sQl0j/figures/022_Figure.jpg]]

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_YsQM7sQl0j/figures/025_Figure.jpg]]

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_YsQM7sQl0j/figures/003_Table_1.jpg]]
*Table 1: Comparison of 3D human representation methods*


## 方法谱系与知识库定位

### 1. 核心瓶颈与设计动机

现有3D人体生成方法面临一个根本性矛盾：**几何分布方法**（如 **gDNA**，Xu et al., CVPR 2022）将单个几何体的信息编码在流网络参数中，导致存储开销随数据集规模线性增长，无法高效扩展到大规模多身份训练；而**隐式场方法**（如 **ENARF**，Noguchi et al., CVPR 2022；**GNARF**，Bergman et al., ECCV 2022）虽然可扩展，却难以捕获宽松衣物的细粒度几何细节与姿态依赖变形。基于高斯泼溅的 **E3Gen**（Zhang et al., ACM Multimedia 2024）和基于GAN的 **EVA3D**（Hong et al., CVPR 2022）同样在几何保真度上存在妥协。

本文 **HGD** 的因果调控点在于两个关键设计：**将几何分布从网络参数迁移到结构化2D特征图**，以及**将流匹配的源分布从无信息的高斯分布替换为更接近目标的SMPL模板分布**。前者解决了可扩展性问题，后者大幅降低了概率流的学习难度——模型不再需要从纯噪声出发学习复杂的衣物-姿态耦合，而是从已知的人体模板表面出发，仅需学习位移场。

### 2. 与基线工作的关系

**HGD** 直接建立在几何分布方法（Zhang et al., 2025）的流匹配框架之上，但对其三个核心组件进行了根本性改造：

| 设计维度 | 基线方法（几何分布） | HGD 改进 | 改进动机 |
|---------|-------------------|---------|---------|
| **几何分布存储** | 网络权重为每个几何体存储独立参数 | 压缩2D特征图 $z_{T\|S} \in \mathbb{R}^{8\times 24\times 24}$ | 泛化表示，支持数据集规模训练 |
| **流匹配源分布** | 多元高斯 $\mathcal{N}(0,1)$ | SMPL模板表面分布 $\Phi_S$ + 最近邻配对扰动 + 零中心化归一化 | 降低学习难度，加速收敛 |
| **训练范式** | 端到端学习条件分布 | 两阶段：自动解码器压缩 → 潜空间扩散流生成 | 解耦表示学习与生成建模 |

与 **gDNA** 相比，HGD 在THuman2数据集上实现了几何质量（FID）从42.90到16.16的显著提升（相对提升57%），这主要归因于HGD直接合成高保真几何点云，而非依赖隐式场的等值面提取。与 **E3Gen** 相比，HGD避免了高斯泼溅在宽松衣物区域产生的不自然形状和法向颜色不一致问题（Fig. 8）。与 **GetAvatar**（Zhang et al., ICCV 2023）相比，HGD生成的衣物褶皱具有更自然的方向性模式，而非随机、不真实的纹理。

### 3. 方法适用边界

**HGD** 在以下场景表现出明显优势：

- **姿态条件随机生成**：给定任意SMPL姿态，生成多样化的高保真人体几何（Table 4, FID=16.16）。
- **新姿态生成**：对已知身份生成未见姿态的几何，用户研究显示质量（4.04/5）和物理合理性（4.36/5）均显著优于gDNA（Table 5）。
- **宽松衣物与裙子**：通过稀疏SMPL点采样策略（Fig. 6），避免了密集近邻搜索在宽松区域产生的孔洞伪影。

但方法存在明确的适用边界：

- **非均匀点采样**：目标几何表面存在局部点密度稀疏问题，在极端姿态和宽松服饰区域可能导致细节缺失。
- **服装泛化受限**：无法生成训练数据中完全未出现的新服装款式，生成多样性受限于数据集覆盖范围。
- **UV接缝伪影**：UV参数化引入的接缝伪影未针对真实服装分片进行优化，可能影响纹理连续性。

### 4. 消融实验揭示的关键机制

消融实验（Table 2, Table 3, Fig. 6, Fig. 7）揭示了几个关键因果机制：

1. **训练对构造策略**：稀疏采样SMPL点并利用KNN构造训练对，可避免在宽松衣物区域出现孔洞伪影（Fig. 6）。直接对密集SMPL网格进行最近邻搜索会导致法向图中的明显孔洞。

2. **分布归一化的必要性**：所提出的归一化公式（SMPL源分布+扰动+归一化）在数据集规模训练中，Chamfer距离（0.0032）显著低于无配对变体（w/o Pairs）和无分布归一化变体（w/o DistNorm）（Table 2）。Fig. 7的可视化显示，未归一化版本在30,000次迭代时仍存在明显的几何失真。

3. **自动解码器 vs 自编码器**：自动解码器在重建精度上优于基于自编码器的 **VecSet**（Zhang et al., SIGGRAPH 2023）和FeatureMap变体（Table 3），表面距离分别为0.0012 vs 更高值。

4. **单几何体 vs 数据集规模的权衡**：在单几何体拟合实验中，添加扰动的方法（w/o DistNorm）可达到最低Chamfer距离，但在多姿态数据集中性能退化（Table 2, Single vs. Dataset行）。本文归一化方法在二者间取得最佳平衡。

### 5. 开放问题与未来方向

论文明确指出的开放问题包括：

- **均匀采样**：如何实现目标几何表面的均匀采样，避免局部点密度稀疏导致的细节缺失？
- **服装泛化**：能否扩展至训练数据之外的服装风格生成，突破数据覆盖范围的限制？
- **UV接缝消除**：如何消除UV贴图接缝伪影，使分割与真实服装分片对齐？
- **极端姿态鲁棒性**：在极端姿态和宽松服饰区域，如何进一步保证点云的均匀覆盖和细节保真度？

这些问题的解决将推动几何分布方法从“数据集内插值”向“真正泛化生成”的跨越。

## 原文 PDF

![[paperPDFs/ICLR_2026/Generative_Human_Geometry_Distribution.pdf]]
