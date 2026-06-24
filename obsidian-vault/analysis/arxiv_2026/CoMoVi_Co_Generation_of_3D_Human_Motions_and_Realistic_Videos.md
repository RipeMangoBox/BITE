---
title: "CoMoVi: Co-Generation of 3D Human Motions and Realistic Videos"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/CoMoVi_Co_Generation_of_3D_Human_Motions_and_Realistic_Videos.pdf
aliases:
- CoMoVi
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 将3D运动编码为融合法向与语义的2D表示，桥接模态差异；并采用双分支扩散模型，通过特征交互使运动生成与视频生成相互引导，实现同步生成与性能提升。
primary_logic: 3D人体运动与2D视频生成本质上相互耦合：运动提供结构一致性先验，视频预训练模型提供泛化能力。通过有效的2D运动表示对齐两模态，可在单一扩散去噪循环中协同生成，使二者相互增强。
claims:
- CoMoVi在CoMoVi-Dataset上运动生成FID达到0.349，显著优于Go-to-Zero-7B（1.641）等SoTA T2M方法。
- 在视频生成VBench评估中，CoMoVi在所有指标上均优于I2V基线，且无需外部运动参考。
- 消融实验表明，去除2D运动表示（w/o motion）使运动FID从0.349骤升至0.758，视频主体一致性下降，验证同步运动生成的关键作用。
- 双分支全拷贝架构（Ours）在FID和SC上均显著优于VideoJAM联合潜空间和VACE分布式副本策略，证明特征交互设计的有效性。
---

# CoMoVi: Co-Generation of 3D Human Motions and Realistic Videos

> [!tip] 核心洞察
> 3D人体运动与2D视频生成本质上相互耦合：运动提供结构一致性先验，视频预训练模型提供泛化能力。通过有效的2D运动表示对齐两模态，可在单一扩散去噪循环中协同生成，使二者相互增强。

| 字段 | 内容 |
|------|------|
| 中文题名 | CoMoVi: 三维人体运动与真实感视频的协同生成 |
| 英文题名 | CoMoVi: Co-Generation of 3D Human Motions and Realistic Videos |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2601.10632v2) · [Project](https://igl-hkust.github.io/CoMoVi/) · [arXiv](https://arxiv.org/abs/2510.20888) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | CoMoVi |
| Dataset | CoMoVi-Dataset, Motion-X++, VBench |

> [!tip] 效果简介
> - CoMoVi-Dataset (运动生成) 上，FID 0.349 vs 1.641 (Go-to-Zero-7B) (-1.292)。
> - Motion-X++ (运动生成，泛化) 上，FID 16.728 vs 19.365 (MoMask) (-2.637)。
> - VBench (视频生成) 上，Subject Consistency 0.955 vs 0.948 (Wan2.2-I2V-5B) (+0.007)。

## 概述

**问题瓶颈**：3D人体运动生成长期受限于高质量标注数据的匮乏，导致模型泛化能力薄弱；与此同时，视频生成模型缺乏对人体结构的显式约束，容易产生肢体扭曲、动作不合理的视频内容。现有的级联式方案（先生成运动再驱动视频，或反之）将两者割裂，无法利用运动与视频之间的内在耦合关系，导致上游误差向下游累积，且错失了相互增强的机会。

**核心洞察**：3D人体运动与2D视频生成本质上是相互耦合的——运动为视频提供结构一致性的强先验，而视频预训练模型则蕴含丰富的视觉泛化能力。关键在于设计一种有效的2D运动表示来桥接模态差异，使得运动与视频可以在统一的扩散去噪循环中协同生成、彼此增强。

**方法定位**：**CoMoVi** 提出了一种双分支扩散协同生成框架。它将3D人体运动编码为融合法向与身体部件语义的单一2D RGB表示，从而对齐2D视频的像素空间；并基于预训练视频扩散模型扩展为双分支架构，通过零线性特征交互层实现运动与视频潜在特征的相互注入，在同一个去噪过程中同步输出3D运动和真实感视频。该框架将传统的“运动→视频”或“视频→运动”级联范式升级为**同步协同生成范式**，使两个模态互为约束、共同优化。

**主要结果**：
- **运动生成**：在CoMoVi-Dataset上，CoMoVi的运动FID达到**0.349**，显著优于Go-to-Zero-7B（1.641）等SOTA文本驱动运动生成方法（Table 2）。
- **视频生成**：在VBench评估中，CoMoVi在所有指标上均优于I2V基线，且无需外部运动参考即可生成结构一致的人体视频（Table 3）。
- **消融验证**：移除2D运动表示后，运动FID从0.349骤升至0.758，视频主体一致性显著下降，证实同步运动生成对视频质量的关键支撑作用（Table 4）。

**局限与展望**：当前框架仅支持单人原地运动生成，推理速度较慢（约15分钟生成5秒视频），且3D运动伪标签可能引入标注误差。未来工作将探索多人交互场景、推理加速以及更敏感的人体运动质量评估指标。

## 背景与动机

### 3D人体运动与视频生成的耦合困境

生成逼真且可控的3D人体运动与视频是计算机视觉与图形学领域的核心挑战，在虚拟数字人、影视制作、游戏开发等应用中具有广泛需求。然而，当前研究在两个关键维度上存在显著瓶颈：

**运动生成的数据与泛化瓶颈。** 3D人体运动生成（Text-to-Motion, T2M）模型的性能高度依赖大规模、高质量的三维标注数据。现有数据集如HumanML3D、KIT-ML等规模有限，且多为实验室环境采集，难以覆盖开放世界中多样化的运动模式。这导致当前SoTA T2M方法（如**MDM** (Tevet et al., arXiv 2022)、**MotionGPT** (Jiang et al., NeurIPS 2023)、**MoMask** (Guo et al., CVPR 2024)）在域外文本描述上的泛化能力不足，生成的3D运动序列常出现物理不合理或语义不匹配的问题。

**视频生成的结构一致性缺陷。** 另一方面，基于扩散模型的图像到视频（I2V）生成方法（如**CogVideoX1.5-I2V-5B** (Yang et al., arXiv 2024)、**Wan2.2-I2V-5B** (Wan et al., arXiv 2025)）虽能生成高保真视频，但缺乏对人体运动的结构化约束，容易产生肢体变形、关节错位、运动闪烁等不合理现象。现有方案通常依赖外部运动参考信号或后处理动捕算法（如CameraHMR）来修正，但这种级联范式存在根本性缺陷：上游错误会向下游累积，且两模态无法相互增强。

### 级联范式的结构性缺陷

如Figure 2所示，现有运动-视频协同生成的主流范式可分为三类：
1. **运动→视频级联**：先生成3D运动，再以其驱动视频生成。该方法将运动作为刚性条件，视频生成无法反哺运动质量。
2. **视频→运动级联**：先生成视频，再通过动捕算法提取3D运动。该方法将运动估计完全置于生成循环之外，无法利用生成过程中的中间表征。
3. **无交互并行**：两模态独立生成，缺乏任何耦合机制。

这三类范式的共同缺陷在于**未能利用运动与视频之间的内在耦合关系**：3D运动为视频提供结构一致性先验（骨骼长度、关节角度、时序连续性），而视频预训练模型蕴含丰富的视觉世界知识，可为运动生成提供泛化能力。将二者割裂，意味着放弃了相互增强的可能性。

### 核心科学问题

本文的核心洞察在于：**3D人体运动与2D视频生成本质上相互耦合**。关键挑战在于如何桥接三维运动与二维视频之间的模态鸿沟，使二者能在统一的生成框架中协同工作。具体而言，需要回答以下问题：

- **模态对齐**：如何将3D运动信息有效编码为与2D视频兼容的表示形式，使预训练视频扩散模型能够理解并利用运动结构？
- **协同机制**：如何设计生成架构，使运动与视频在去噪过程中相互引导，而非单向依赖？
- **联合优化**：如何通过损失函数设计，强化2D潜在表示与3D运动参数之间的对齐，确保协同生成的一致性？

CoMoVi正是针对上述问题提出的协同生成框架，其核心思路是通过**融合法向与语义的2D运动表示**桥接模态差异，并采用**双分支扩散模型**实现特征交互，使运动生成与视频生成在单一去噪循环中同步进行、相互增强。

## 核心创新

CoMoVi 的核心创新在于将 3D 人体运动生成与 2D 视频生成从传统的“级联式”或“无交互”范式，重构为**单一扩散去噪循环内的同步协同生成**。这一范式转变由三个紧密耦合的 changed slot 支撑。

### 范式转变：从级联到协同

现有方法通常采用“先运动后视频”或“先视频后运动”的级联流程，例如 **Go-to-Zero-7B + Champ** 组合（T2M 生成运动，再驱动视频生成），或 **Wan + CameraHMR**（先生成视频，再通过外部动捕模型提取运动）。这类范式存在两个根本缺陷：一是上游模块的错误会向下游累积且无法修正；二是运动与视频模态之间的耦合关系被完全忽略，无法相互增强。

CoMoVi 提出**双分支扩散协同生成范式**（Fig. 2）：在 Wan2.2-I2V-5B 预训练视频扩散模型的基础上，扩展出并行的 2D 运动图分支与 RGB 视频分支，两者在去噪过程中通过特征交互实现相互引导。这一设计的核心洞察是：**3D 运动为视频提供人体结构一致性先验，而视频预训练模型则为运动生成提供强大的泛化能力**——二者本质上是互补的。

### 关键创新点一：融合法向与语义的 2D 运动表示

桥接 3D 运动与 2D 视频模态的核心挑战在于找到一种有效的中间表示。已有方法或使用分离的法向图、语义图，或仅用 2D 骨骼关键点，均无法同时传递 3D 几何信息与身体部件语义。

CoMoVi 提出将 SMPL 网格渲染为**单一 RGB 图像**，其颜色编码同时携带两类信息（Fig. 4）：
- **法向信息**：利用顶点法向的 x、y 分量编码到 G、B 通道，而 z 分量的符号（表征表面朝向）编码到 R 通道的低位；
- **身体部件语义**：将 SMPL 的 24 个身体部件索引编码到 R 通道的高位，形成可区分的颜色区域。

具体地，对于顶点 $i$ 的法向 $v n$，其 z 分量由 $v n_{z} = \pm \sqrt{1 - v n_{x}^{2} - v n_{y}^{2}}$ 恢复，符号通过红色通道赋值公式确定：
$$\operatorname{Red}(\mathbf{v e}_{i}) = \begin{cases} \operatorname{RedList}[\mathrm{r}] & \mathrm{if}\ \mathrm{sign}(v n_{z}) \geq 0 \\ \operatorname{RedList}[\mathrm{r}+1] & \mathrm{if}\ \mathrm{sign}(v n_{z}) < 0 \end{cases}$$

这种融合表示使预训练视频扩散模型能够直接处理 3D 运动信息，同时保留了像素空间中的几何与语义结构。消融实验（Table 4）证实：仅使用法向或仅使用语义表示均导致运动 FID 和视频主体一致性显著下降，融合表示在所有指标上达到最优。

### 关键创新点二：双分支特征交互与 3D-2D 交叉注意力

CoMoVi 的双分支架构并非简单的并行处理，而是通过 **Zero-Linear 特征交互层**实现运动与视频潜在特征的相互注入：
$$\begin{array}{rl} & \boldsymbol{x}_{t}^{\mathrm{fused}} = \boldsymbol{x}_{t}^{\mathrm{motion}} + \mathrm{ZeroLinear}_{i}(\boldsymbol{x}_{t}^{\mathrm{video}}) \\ & \boldsymbol{x}_{t}^{\mathrm{video}} = \boldsymbol{x}_{t}^{\mathrm{video}} + \mathrm{ZeroLinear}_{i+1}(\boldsymbol{x}_{t}^{\mathrm{motion}}) \end{array}$$

其中 Zero-Linear 层初始化为零，确保训练初期不破坏预训练权重，随后逐步学习跨模态的特征融合。这一设计与 **VideoJAM** 的联合潜空间和 **VACE** 的分布式副本策略形成对比：消融实验（Table 4, Architecture）表明，CoMoVi 的全拷贝双分支架构在运动 FID 和视频主体一致性（SC）上均显著优于这两种替代方案，验证了特征交互设计的有效性。

在此基础上，**3D-2D 交叉注意力模块**直接从融合特征中估计 3D 运动序列，避免了对外部视频动捕模型（如 CameraHMR）的依赖：
$$\pmb q = \mathrm{CrossAttention}(\pmb q^{\prime}, \pmb x_{t}^{\mathrm{fused}})$$
其中运动查询 $\pmb q^{\prime}$ 按每 4 帧重组后与融合视频特征进行交叉注意力，输出 3D 人体运动参数。这一设计将 3D 运动估计集成于去噪循环内部，使运动生成与视频生成共享同一表征空间。

### 关键创新点三：SMPL 损失强化的 2D-3D 对齐

为强化 2D 潜在表示与 3D 结构之间的对齐，CoMoVi 引入 SMPL 损失直接监督 3D 运动预测：
$$\mathcal{L}^{\mathrm{smpl}} = \frac{1}{F-1} \sum_{i=1}^{F-1} \left\| \pmb{m}_{i} - \mathrm{GT}(\pmb{m}_{i}) \right\|_{2}^{2}$$

总损失函数为 $\mathcal{L}^{\mathrm{total}} = \mathcal{L}^{\mathrm{motion}} + \mathcal{L}^{\mathrm{video}} + \mathcal{L}^{\mathrm{smpl}}$，其中运动与视频损失均采用流匹配目标 $\mathcal{L} = \mathbb{E}_{\pmb{x}_{0}, \epsilon, t, \pmb{p}} \left[ \| \mathcal{D}(\pmb{x}_{t}, t, \pmb{p}) - \pmb{v}_{t} \|_{2}^{2} \right]$。消融实验（Table 4）显示，移除 $\mathcal{L}^{\mathrm{smpl}}$ 后视频主体一致性 SC 从 0.955 降至 0.951，验证了 3D 正则化对 2D 视频质量的反馈增强作用。

### 创新效果验证

上述三个 changed slot 的协同作用在实验中得到了充分验证：
- 移除 2D 运动表示（w/o motion）使运动 FID 从 **0.349 骤升至 0.758**，视频 SC 从 0.955 降至 0.937（Table 4），证明同步运动生成是视频质量的关键支撑；
- CoMoVi 在自建数据集上运动 FID 达到 **0.349**，显著优于 Go-to-Zero-7B 的 1.641（Table 2）；
- 在 VBench 视频评估中，CoMoVi 在所有指标上均优于 I2V 基线（Table 3），且无需任何外部运动参考。

## 整体框架

CoMoVi 的目标是从一张起始人物图像 $s_0$ 和一段运动文本描述 $\delta_p$ 出发，同步协同生成 3D 人体运动序列 $\{\mathbf{m}_i \in \mathbb{R}^{J \times 3}\}_{i=0}^{F}$ 和 RGB 视频序列 $\{\mathbf{s}_i \in \mathbb{R}^{H \times W \times 3}\}_{i=0}^{F}$。其整体 pipeline（Fig. 3）由两大核心模块串联而成：**2D 人体运动表示编码器**与**双分支视频扩散模型**。

![[assets/figures/papers/paper_list_l47_https_arxiv_org_abs_2601_10632v2/figures/003_Figure_3.jpg]]
*Figure 3: Pipeline overview of CoMoVi. Our method consists of an effective 2D human motion representation (Sec. 3.2) to encode 3D motion information in pixel space, and a dual-branch diffusion model extended from Wan2.2-I2V-5B to coordinate 2D motion and RGB video sequence denoising process with 3D-2D cross-attention modules to concurrently generate 3D human motion (Sec. 3.3)*

![[assets/figures/papers/paper_list_l47_https_arxiv_org_abs_2601_10632v2/figures/016_Figure_3.jpg]]
*Figure 3: Prompt instruction for Qwen2.5-VL [103] to analyze the first frame of video*

**2D 人体运动表示编码器**负责桥接 3D 运动与 2D 视频之间的模态鸿沟。它将初始 3D SMPL 网格 $m_0$ 渲染为一幅融合顶点法向与身体部件语义的单一 RGB 图像 $k_0$（Sec. 3.2）。该表示在像素空间中同时编码了 3D 几何信息（法向）和结构语义（身体部件），使预训练的 2D 视频扩散模型能够直接“理解”运动结构，而无需额外的投影适配。

**双分支扩散模型**以预训练的 Wan2.2-I2V-5B 为基础扩展而来（Sec. 3.3）。它包含两条并行的去噪分支：一条处理 2D 运动表示序列，另一条处理 RGB 视频序列。在每个扩散块之间，**零线性特征交互层**（Zero-Linear Feature Interaction Layers）负责将运动分支与视频分支的潜在特征相互注入：

$$
\begin{array}{rl} & \boldsymbol{x}_{t}^{\mathrm{fused}} = \boldsymbol{x}_{t}^{\mathrm{motion}} + \mathrm{ZeroLinear}_{i}(\boldsymbol{x}_{t}^{\mathrm{video}}) \\ & \boldsymbol{x}_{t}^{\mathrm{video}} = \boldsymbol{x}_{t}^{\mathrm{video}} + \mathrm{ZeroLinear}_{i+1}(\boldsymbol{x}_{t}^{\mathrm{motion}}) \end{array}
$$

这一设计使运动生成与视频生成在单一去噪循环中相互引导、彼此增强，而非简单的级联或后处理。

**3D-2D 交叉注意力模块**（3D-2D Cross-Attention Module）嵌入在去噪过程中，将重排后的运动查询 $\mathbf{q}'$ 与融合特征 $\mathbf{x}_t^{\mathrm{fused}}$ 进行交叉注意力：

$$
\pmb q = \mathrm { C r o s s A t t e n t i o n } ( \pmb q ^ { \prime } , \pmb x _ { t } ^ { \mathrm { f u s e d } } )
$$

该模块直接从融合特征中估计 3D 人体运动序列，省去了传统级联范式中依赖外部视频动捕算法（如 CameraHMR）的后处理步骤。

**训练目标**由三部分损失联合驱动：

$$
\mathcal { L } ^ { \mathrm { t o t a l } } = \mathcal { L } ^ { \mathrm { m o t i o n } } + \mathcal { L } ^ { \mathrm { v i d e o } } + \mathcal { L } ^ { \mathrm { s m p l } }
$$

其中 $\mathcal{L}^{\mathrm{motion}}$ 和 $\mathcal{L}^{\mathrm{video}}$ 均为流匹配损失（Flow Matching Loss），$\mathcal{L}^{\mathrm{smpl}}$ 监督预测的 SMPL 参数与真值之间的均方误差，强化 2D 潜在表示与 3D 结构之间的对齐。消融实验表明，引入 $\mathcal{L}^{\mathrm{smpl}}$ 可将视频主体一致性（SC）从 0.951 提升至 0.955（Table 4）。

**输入输出流总结**：起始图像 $s_0$ 与文本描述 $\delta_p$ 作为条件输入双分支扩散模型；2D 运动表示编码器将初始 SMPL 网格 $m_0$ 渲染为 $k_0$ 并送入运动分支；两条分支在去噪过程中通过零线性层持续交互；3D-2D 交叉注意力模块从融合特征中解码出 3D 运动序列；最终同步输出 RGB 视频帧和对应的 3D 人体运动。

### 补充图表

![[assets/figures/papers/paper_list_l47_https_arxiv_org_abs_2601_10632v2/figures/002_Figure_2.jpg]]
*Figure 2: Different paradigms of motion video co-generation*

## 核心模块与公式推导

### 2D人体运动表示：法向-语义融合编码

CoMoVi的核心设计之一是将3D运动信息压缩为一种与2D视频在像素空间对齐的表示，从而桥接模态差异。该表示以SMPL网格为输入，通过两个关键步骤构建：

1. **顶点法向恢复**：给定SMPL网格的顶点法向分量 $v n_x$ 和 $v n_y$（可直接从网格几何计算），其z分量可由下式恢复，但符号未定：

   $$v n_{z} = \pm \sqrt{1 - v n_{x}^{2} - v n_{y}^{2}} \tag{1}$$

2. **红色通道双重编码**：法向z分量的符号（指示表面朝向）与身体部件语义被联合编码至RGB图像的红色通道。具体而言，对于每个顶点 $\mathbf{v e}_{i}$ 所属的身体部件 $r$，红色通道的赋值规则为：

   $$\operatorname{Red}(\mathbf{v e}_{i}) = \begin{cases} \operatorname{RedList}[\mathrm{r}] & \mathrm{if}\ \mathrm{sign}(v n_{z}) \geq 0 \\ \operatorname{RedList}[\mathrm{r}+1] & \mathrm{if}\ \mathrm{sign}(v n_{z}) < 0 \end{cases} \tag{2}$$

   其中 $\operatorname{RedList}$ 为预定义的颜色列表。该设计使得单一RGB图像同时承载了3D几何信息（法向朝向）与语义信息（身体部件），为后续扩散模型提供了结构化的2D运动表示。消融实验证实，仅使用法向或仅使用语义表示均导致运动生成FID和视频主体一致性下降，验证了融合表示的必要性。

### 双分支扩散与零线性特征交互

CoMoVi在预训练视频扩散模型 **Wan2.2-I2V-5B**（Wan et al., arXiv 2025）的基础上扩展为双分支架构，同时对2D运动表示序列和RGB视频序列进行去噪。两分支之间的耦合通过**零线性特征交互层**实现，其核心操作为：

$$\begin{array}{rl} & \boldsymbol{x}_{t}^{\mathrm{fused}} = \boldsymbol{x}_{t}^{\mathrm{motion}} + \mathrm{ZeroLinear}_{i}(\boldsymbol{x}_{t}^{\mathrm{video}}) \\ & \boldsymbol{x}_{t}^{\mathrm{video}} = \boldsymbol{x}_{t}^{\mathrm{video}} + \mathrm{ZeroLinear}_{i+1}(\boldsymbol{x}_{t}^{\mathrm{motion}}) \end{array} \tag{3}$$

其中 $\boldsymbol{x}_{t}^{\mathrm{motion}}$ 和 $\boldsymbol{x}_{t}^{\mathrm{video}}$ 分别为运动分支和视频分支在去噪时间步 $t$ 的潜在特征。$\mathrm{ZeroLinear}$ 层初始化为零，在训练中逐步学习跨模态特征注入的权重，使运动生成与视频生成在单一去噪循环中相互引导、彼此增强。消融实验表明，该全拷贝架构在FID和主体一致性上均显著优于VideoJAM的联合潜空间策略和VACE的分布式副本策略。

### 3D-2D交叉注意力与运动估计

为从融合特征中直接估计3D人体运动序列，CoMoVi设计了3D-2D交叉注意力模块。首先将运动查询 $\pmb q$ 按每4帧重组为 $\pmb q'$，随后与融合特征 $\pmb x_{t}^{\mathrm{fused}}$ 进行交叉注意力：

$$\pmb q = \mathrm{CrossAttention}(\pmb q', \pmb x_{t}^{\mathrm{fused}}) \tag{5}$$

该模块集成于去噪循环内部，使得3D运动估计直接受益于视频预训练模型的泛化能力，无需依赖外部视频动捕算法（如CameraHMR）进行后处理，避免了级联范式中的误差累积。

### 损失函数设计

训练总损失由三部分构成：

$$\mathcal{L}^{\mathrm{total}} = \mathcal{L}^{\mathrm{motion}} + \mathcal{L}^{\mathrm{video}} + \mathcal{L}^{\mathrm{smpl}} \tag{6}$$

其中 $\mathcal{L}^{\mathrm{motion}}$ 和 $\mathcal{L}^{\mathrm{video}}$ 均采用流匹配目标函数，以速度场 $\pmb v_t$ 为回归目标：

$$\mathcal{L} = \mathbb{E}_{\pmb{x}_{0}, \epsilon, t, \pmb{p}} \left[ \| \mathcal{D}(\pmb{x}_{t}, t, \pmb{p}) - \pmb{v}_{t} \|_{2}^{2} \right] \tag{7}$$

$\mathcal{L}^{\mathrm{smpl}}$ 为SMPL参数回归损失，通过均方误差监督预测运动序列与真实值之间的对齐：

$$\mathcal{L}^{\mathrm{smpl}} = \frac{1}{F - 1} \sum_{i = 1}^{F - 1} \| \pmb{m}_{i} - \mathrm{GT}(\pmb{m}_{i}) \|_{2}^{2} \tag{8}$$

该损失项强化了2D潜在表示与3D结构之间的对应关系。消融实验显示，移除 $\mathcal{L}^{\mathrm{smpl}}$ 后视频主体一致性从0.955降至0.951，证实了3D正则化对视频生成质量的促进作用。

### 补充图表

![[assets/figures/papers/paper_list_l47_https_arxiv_org_abs_2601_10632v2/figures/004_Figure.jpg]]

![[assets/figures/papers/paper_list_l47_https_arxiv_org_abs_2601_10632v2/figures/005_Figure_5.jpg]]
*Figure 5: We observe that significant appearance shifts occur when directly applying pretrained VDM on our 2D motion representation*

## 实验与分析

### 核心实验设计

CoMoVi 在自建的 **CoMoVi-Dataset** 上训练与评估，该数据集包含 2,946 个真实世界视频及对应的 3D 人体运动伪标签（由 CameraHMR 估计并经平滑处理）。评估分为两条主线：**3D 人体运动生成** 和 **RGB 视频生成**，二者共享同一输入——一张起始人物图像和一段运动文本描述。运动生成对比 SoTA 文本-运动（T2M）方法；视频生成对比开源图像-视频（I2V）模型及级联式 T2M+运动驱动视频生成基线。

### 3D 人体运动生成：主结果

在 CoMoVi-Dataset 上，CoMoVi 的运动生成 **FID 达到 0.349**，大幅领先所有对比方法。最接近的基线 **Go-to-Zero-7B** 的 FID 为 1.641，CoMoVi 相对降低了 **1.292**（Table 2）。其他 T2M 方法如 **MoMask**（Guo et al., CVPR 2024）和 **MotionGPT**（Jiang et al., NeurIPS 2023）的 FID 分别为 1.250 和 3.137，差距显著。定性结果（Fig. 6）显示，CoMoVi 生成的运动在时序连贯性、物理合理性上明显优于基线，尤其在复杂动作（如“从坐姿起身并伸展身体”）上，级联基线 Wan2.2-I2V-5B+CameraHMR 常出现抖动和不自然姿态。

![[assets/figures/papers/paper_list_l47_https_arxiv_org_abs_2601_10632v2/figures/008_Table_2.jpg]]
*Table 2: Quantitative evaluation of 3D human motion generation. “*”: Motion-X++ [47] is in the training set of Go-to-Zero [18]*

![[assets/figures/papers/paper_list_l47_https_arxiv_org_abs_2601_10632v2/figures/007_Figure_6.jpg]]
*Figure 6: Qualitataive comparison of 3D human motion generation with SoTA T2M models [18, 21, 33, 83]. Wan2.2-I2V-5B+CameraHMR [65, 84] is a simple yet meaningful baseline composed a video generation model followed by a video motion capture model. We present motion keywords in text prompts for simplicity*

为验证泛化能力，在 **Motion-X++** 数据集上进行跨域评估。CoMoVi 的 FID 为 **16.728**，优于 MoMask 的 19.365，但需注意 Go-to-Zero 系列模型在 Motion-X++ 上存在训练集重叠问题（Table 2 标注 `*`），其数值比较的公平性存疑。

### 视频生成：主结果

视频质量通过 **VBench** 基准评估，涵盖主体一致性（SC）、背景一致性（BC）、运动平滑度（MS）、美学质量（AQ）和图像质量（IQ）。CoMoVi 在所有五项指标上均优于 I2V 基线（Table 3）：

- **主体一致性 SC**：CoMoVi 达到 **0.955**，优于 **Wan2.2-I2V-5B**（0.948）和 **CogVideoX1.5-I2V-5B**（0.947）。
- **运动平滑度 MS**：CoMoVi 为 **0.993**，与 Wan2.2-I2V-5B（0.988）相比略有提升。
- **背景一致性 BC** 和 **图像质量 IQ** 同样取得最优。

值得注意的是，CoMoVi **无需外部参考视频或预提取的运动信号**，而级联基线 Go-to-Zero-7B+Champ 需要先独立生成运动再驱动视频生成，其 SC 仅为 0.949。这验证了同步协同生成在保持人物外观一致性上的优势。

**但需谨慎解读**：VBench 指标差异普遍在 ±0.05 以内，现有视频评估体系对人体运动质量与结构一致性的区分度有限，定量增益未能完全反映视觉上的结构保真度提升。

### 消融实验：关键设计验证

Table 4 系统消融了 2D 运动表示形式和模型架构的贡献，结论如下：

![[assets/figures/papers/paper_list_l47_https_arxiv_org_abs_2601_10632v2/figures/013_Table_4.jpg]]
*Table 4: Quantitative ablation of representations and architectures*

#### 2D 运动表示的核心作用

- **移除 2D 运动表示（w/o motion）** 导致运动 FID 从 0.349 骤升至 **0.758**，视频 SC 从 0.955 降至 **0.937**。这证明同步运动生成对维持视频中人体结构一致性不可或缺——纯 I2V 模型缺乏结构化运动先验，难以生成合理的人体动作。
- **仅使用法向图（Normal）** 或 **仅使用语义图（Semantic）** 均导致性能下降：单独法向的 FID 为 0.438，单独语义的 FID 为 0.409，而融合表示（Ours）的 0.349 为最优。这验证了同时编码 3D 几何信息（法向）与身体部件语义信息的必要性。

#### 双分支架构设计

- 对比 **VideoJAM** 的联合潜空间策略（将运动与视频在潜空间直接相加）和 **VACE** 的分布式副本策略（仅复制部分参数），CoMoVi 的**双分支全拷贝架构（Ours）**在 FID（0.349 vs. 0.437 vs. 0.447）和 SC（0.955 vs. 0.943 vs. 0.942）上均显著领先。这表明通过零线性特征交互层（Eq. 3）进行显式、双向的特征注入，比简单的潜空间混合或参数共享更能有效耦合两模态。
- 定性比较（Fig. 9）中，VideoJAM 和 VACE 变体在“起身伸展”场景下出现手臂穿透身体、姿态不自然等问题，而 CoMoVi 保持了连贯的 3D 结构。

![[assets/figures/papers/paper_list_l47_https_arxiv_org_abs_2601_10632v2/figures/012_Figure_9.jpg]]
*Figure 9: Qualitative results of different motion representations and model architectures. The input motion keyword is: “transition from seated state to get up and stretch body"*

#### 3D 正则化损失

- 移除 SMPL 损失（$\\mathcal{L}^{\\mathrm{smpl}}$）使视频 SC 从 0.955 降至 **0.951**，运动 FID 从 0.349 升至 **0.377**。该损失通过显式监督 3D 运动预测，强化了 2D 潜在表示与 3D 结构之间的对齐，对视频中主体一致性有直接贡献。

### 失败模式与局限性

1. **复杂动作的末端效应器漂移**：在快速旋转或大幅度肢体摆动场景中，生成的 3D 运动偶尔出现手部、足部位置不准确，表现为“滑步”或手部穿透。这源于 2D 运动表示对深度信息的间接编码存在歧义，且 SMPL 损失仅约束整体参数，缺乏对末端关节的精细监督。
2. **外观漂移**：长时间生成（>5 秒）时，人物服装纹理可能逐渐模糊或色彩偏移。这与扩散模型的误差累积有关，当前框架未引入显式的时间一致性约束。
3. **单人、原地运动限制**：框架仅支持单人、无全局位移的运动生成，无法处理多人交互或人-物交互。这是 2D 表示和当前训练数据范围的根本性约束。
4. **推理速度瓶颈**：生成 5 秒视频约需 15 分钟，远不能满足实时应用。双分支扩散架构的推理计算量约为单分支的 2 倍，且 3D-2D 交叉注意力模块增加了额外开销。

### 重要图表结论速览

- **Table 2**：CoMoVi 在 CoMoVi-Dataset 上运动 FID 0.349，较 Go-to-Zero-7B 降低 78.7%；在 Motion-X++ 上 FID 16.728，泛化能力优于 MoMask。
- **Table 3**：VBench 全指标最优，SC 0.955，无需外部运动参考。
- **Table 4**：去除 2D 运动表示使 FID 退化 117%；融合法向+语义表示优于任一单独表示；双分支全拷贝架构优于联合潜空间和分布式副本策略；$\\mathcal{L}^{\\mathrm{smpl}}$ 贡献 SC +0.004。
- **Fig. 6, 8**：定性结果中，CoMoVi 的运动和视频在结构一致性与时序连贯性上明显优于级联范式和纯 I2V 基线。
- **Fig. 9**：消融可视化清晰展示不同表示和架构对“起身伸展”动作的质量影响。

### 补充图表

![[assets/figures/papers/paper_list_l47_https_arxiv_org_abs_2601_10632v2/figures/011_Figure_8.jpg]]
*Figure 8: Qualitataive comparison of human video generation with SoTA open-souce I2V models [84, 107], and a baseline composed of SoTA T2M [18] and motion-driven video generation model [118]*

![[assets/figures/papers/paper_list_l47_https_arxiv_org_abs_2601_10632v2/figures/006_Table_1.jpg]]
*Table 1: Comparison of CoMoVi-Dataset with existing datasets. “*": We only count real-world data*

![[assets/figures/papers/paper_list_l47_https_arxiv_org_abs_2601_10632v2/figures/017_Figure_4.jpg]]
*Figure 4: Prompt instruction for Gemini2.5-Pro to caption human motion in videos*

## 方法谱系与知识库定位

### 任务定位与范式变革

CoMoVi 针对的是**三维人体运动与真实感视频的协同生成**这一新兴任务。传统上，3D人体运动生成（Text-to-Motion, T2M）与人体视频生成（Image-to-Video, I2V）是两个独立发展的领域，前者受限于高质量标注数据的匮乏导致泛化能力弱，后者则因缺乏结构化约束而常产生不合理的人体动作。CoMoVi 的核心变革在于将两者从**级联式或无交互的分离范式**统一为**单一扩散去噪循环内的同步协同生成范式**（Fig. 2），使运动生成与视频生成能够相互引导、彼此增强。

### 在运动生成谱系中的定位

在 T2M 任务上，CoMoVi 与以下代表性基线形成对比：

- **MDM**（Tevet et al., arXiv 2022）：基于扩散模型的运动生成先驱，但仅处理纯运动模态。
- **MotionGPT**（Jiang et al., NeurIPS 2023）：将运动视为语言进行建模，探索了运动与文本的统一表示。
- **MoMask**（Guo et al., CVPR 2024）：采用掩码建模的运动生成方法，在运动质量上达到当时最优。
- **Go-to-Zero-3B / Go-to-Zero-7B**：大规模运动生成模型，代表了参数扩展路线的 SoTA。

CoMoVi 与上述方法的根本区别在于：**它不将运动生成视为孤立任务，而是通过与视频生成的耦合来获取额外的结构化监督**。在 CoMoVi-Dataset 上，CoMoVi 的运动 FID 达到 0.349，显著优于 Go-to-Zero-7B 的 1.641（Table 2）。这一优势来源于视频预训练模型提供的泛化能力——视频扩散模型在海量数据上习得的先验，通过双分支特征交互反哺给运动生成分支。

### 在视频生成谱系中的定位

在人体视频生成任务上，CoMoVi 与以下基线形成对比：

- **Wan2.2-I2V-5B**（Wan et al., arXiv 2025）与 **CogVideoX1.5-I2V-5B**（Yang et al., arXiv 2024）：开源 I2V 模型，缺乏显式的运动结构约束。
- **Wan+CameraHMR**（Patel & Black, 3DV 2025）：视频生成后接外部视频动捕的级联方案，视频生成与运动估计完全解耦。
- **Go-to-Zero-7B+Champ**：T2M 模型与运动驱动视频生成模型的级联组合，上游运动误差会向下游传播。

CoMoVi 的关键不同在于：**视频生成过程本身受到同步生成的 3D 运动的结构一致性先验约束**，无需外部运动参考。在 VBench 评估中，CoMoVi 在所有指标上均优于 I2V 基线（Table 3），尤其在主体一致性（Subject Consistency）上达到 0.955。然而需注意，VBench 指标差异在 ±0.05 量级，对运动质量与人体结构一致性的区分度有限，这一评价体系本身有待完善。

### 技术路线对比：关键设计选择

CoMoVi 的三个关键设计槽位及其与替代方案的对比如下：

| 设计维度 | 基线做法 | CoMoVi 方案 | 证据锚点 |
|---------|---------|------------|---------|
| **运动-视频交互范式** | 级联式（运动→视频 或 视频→运动）或无交互 | 双分支扩散同步协同生成，通过零线性特征交互相互增强 | Fig.2; Eq.(3) |
| **2D运动表示形式** | 分离的法向图、语义图或2D骨骼关键点 | 融合法向与身体部件语义的单一RGB表示 | Sec.3.2; Fig.4 |
| **3D运动估计方式** | 借助外部视频动捕算法后处理 | 集成于去噪循环中的3D-2D交叉注意力模块 | Sec.3.3 Eq.(5) |

**消融实验验证了每个设计选择的必要性**（Table 4）：
- **移除2D运动表示（w/o motion）**：运动 FID 从 0.349 骤升至 0.758，视频主体一致性从 0.955 降至 0.937，证明同步运动生成对视频质量的关键支撑作用。
- **仅使用法向或语义表示**：均导致性能下降，融合表示在所有指标上最优，验证了 3D 几何与语义信息互补的必要性。
- **双分支全拷贝架构 vs. VideoJAM 联合潜空间 / VACE 分布式副本**：CoMoVi 的全拷贝策略在 FID 和 SC 上均显著优于替代架构，证明特征交互设计的有效性。
- **引入 3D 正则化损失 $\mathcal{L}^{\mathrm{smpl}}$**：将视频主体一致性从 0.951 提升至 0.955，验证了 2D-3D 对齐监督的价值。

### 适用边界与局限

CoMoVi 当前存在以下明确局限：

1. **场景受限**：仅支持单人、原地运动生成，尚未扩展至多人交互或人-物交互场景。
2. **推理效率**：推理速度较慢（约 15 分钟生成 5 秒视频），难以满足实时应用需求。
3. **标注噪声**：3D 运动伪标签由 CameraHMR 估计并经平滑后处理，可能引入系统性标注误差。
4. **评价体系不足**：VBench 等现有视频评估指标对人体运动质量的区分度有限，指标提升幅度小（±0.05），未能充分反映人体结构一致性与运动质量的实质改善。

### 开放问题与未来方向

1. **场景扩展**：如何将框架扩展至可变长度、无限长度运动及多人交互场景？
2. **推理加速**：能否利用蒸馏技术加速推理，降低对计算资源的需求？
3. **评价指标**：能否设计专门针对人体运动质量与一致性的更敏感评估指标？
4. **模态泛化**：该协同生成思想能否推广到深度、光流等其他模态的联合建模？

### 知识库定位总结

CoMoVi 在知识库中的核心贡献在于：**首次证明了 3D 人体运动与 2D 视频可以在单一扩散去噪循环中相互增强**。其方法论桥梁——融合法向与语义的 2D 运动表示——有效对齐了两模态的特征空间，使视频预训练模型的泛化能力得以反哺运动生成，同时运动的结构一致性先验约束了视频生成。这一协同生成范式为后续的多模态人体生成研究提供了新的技术路线。

## 原文 PDF

![[paperPDFs/arxiv_2026/CoMoVi_Co_Generation_of_3D_Human_Motions_and_Realistic_Videos.pdf]]