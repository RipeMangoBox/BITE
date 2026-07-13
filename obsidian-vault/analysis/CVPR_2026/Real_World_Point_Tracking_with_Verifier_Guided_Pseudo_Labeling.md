---
title: Real-World Point Tracking with Verifier-Guided Pseudo-Labeling
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Real_World_Point_Tracking_with_Verifier_Guided_Pseudo_Labeling.pdf
project_link: null
code_link: null
aliases:
- VGPL
- RWPTVGPL
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入一个可学习的验证器（verifier），在每帧动态评估多个教师跟踪器输出的可靠性，并根据该评分自适应选择伪标签，从而把模型差异性转化为适应优势。
primary_logic: 通过仅在合成数据上训练验证器来识别时空一致性线索，它可以跨域地评估跟踪预测的可靠性，进而将多个互补的跟踪器组合成高质量、逐帧优选的伪标签，实现数据高效且稳健的真实世界微调。
claims:
- Oracle测试揭示出相比于任意单个教师或随机选择，逐帧最优选择存在巨大提升空间，说明需要自适应选择机制。
- 验证器集成在四个真实世界基准上一致优于所有单个教师模型和随机教师基线，验证了其有效利用互补性。
- 在 EgoPoints 上，验证器引导的自训练将 δ_avg^x 从 61.7（纯合成基线）提升至 67.3，取得了最多 5.6 个点的增益。
- 消融实验表明，无论使用哪组教师模型，验证器选择均优于随机选择，且推广到不同数据集和场景。
---

# Real-World Point Tracking with Verifier-Guided Pseudo-Labeling

> [!tip] 核心洞察
> 通过仅在合成数据上训练验证器来识别时空一致性线索，它可以跨域地评估跟踪预测的可靠性，进而将多个互补的跟踪器组合成高质量、逐帧优选的伪标签，实现数据高效且稳健的真实世界微调。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于验证器引导伪标注的真实世界点跟踪 |
| 英文题名 | Real-World Point Tracking with Verifier-Guided Pseudo-Labeling |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.12217) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Verifier-Guided Pseudo-Labeling（验证器引导伪标注） |
| Dataset | EgoPoints, RoboTAP, TAP-Vid Kinetics, TAP-Vid DAVIS |

> [!tip] 效果简介
> - EgoPoints 上，δ_avg^x 67.3 vs 61.7 (Track-On2 合成预训练) (+5.6)。
> - RoboTAP 上，AJ 70.9 vs 68.1 (Track-On2 合成预训练) (+2.8)。
> - TAP-Vid Kinetics 上，AJ 57.8 vs 55.3 (Track-On2 合成预训练) (+2.5)。

## 概要

点跟踪旨在给定视频首帧的查询点后，预测该点在后续所有帧中的二维轨迹坐标与可见性状态。现有方法在合成数据上预训练后，直接迁移到真实世界视频时性能显著下降，核心瓶颈在于：**在未标注的真实视频上，单个预训练跟踪器产生的伪标签在帧间可靠性波动极大**（Figure 2(b)），简单的随机选择或固定融合策略会放大噪声和漂移，导致自训练适应质量差。

本文提出 **Verifier-Guided Pseudo-Labeling（验证器引导伪标注）**，核心思想是引入一个可学习的验证器，在每帧动态评估多个预训练教师跟踪器输出的可靠性，并根据评分自适应选择最优预测作为伪标签。验证器完全在合成数据上训练，通过识别时空一致性线索来跨域评估跟踪预测的质量，从而将多个互补跟踪器的差异性转化为适应优势。

主要结论如下：

- **Oracle 测试揭示巨大提升空间**：在 EgoPoints、RoboTAP、TAP-Vid Kinetics 和 DAVIS 四个真实世界基准上，逐帧最优选择（oracle）远超任意单个教师模型和随机选择基线（Figure 2(a)），说明需要自适应选择机制。

- **验证器集成一致优于所有教师**：在推理时，验证器集成在四个基准上均超过最强单个教师和随机教师基线（Figure 4），验证了其有效利用模型互补性的能力。

- **自训练适应带来显著增益**：以 Track-On2 为基座模型，验证器引导的自训练在 EgoPoints 上将 δ_avg^x 从 61.7 提升至 67.3（+5.6），在 RoboTAP 上将 AJ 从 68.1 提升至 70.9（+2.8），在 Kinetics 和 DAVIS 上分别提升 +2.5 和 +1.1（Table 1）。

- **方法数据效率高**：仅使用 TAO 数据集（约 2.9K 视频）即可取得大部分适应增益，额外增加 OVIS 和 VSPW 带来的边际提升有限（Table 6）。

在方法谱系上，本工作属于真实世界点跟踪的自训练微调范式。与 **BootsTAPIR**（大规模自蒸馏）和 **BootsTAPNext**（状态空间替代方案）等现有真实世界微调基线不同，本文不依赖单一教师模型，而是通过验证器动态组合多个现成跟踪器（Track-On2、BootsTAPIR、BootsTAPNext、Anthro-LocoTrack、AllTracker、CoTracker3 Window）的预测，形成更高质量的伪标签监督。



### 点跟踪任务与域间鸿沟

点跟踪（Point Tracking）的目标是：给定视频 $\mathcal{V}$ 中某一帧 $t_0$ 的查询点 $\mathbf{q}_{t_0}$，模型 $\Phi$ 需预测该点在后续所有帧中的二维轨迹坐标 $\hat{\mathbf{p}}_t$ 及可见性 $\hat{v}_t$：

$$\{ ( \hat{\mathbf{p}}_t, \hat{v}_t ) \}_{t=t_0+1}^T = \Phi(\mathcal{V}, \mathbf{q}_{t_0})$$

这一任务在视频编辑、3D 重建、机器人操作等应用中具有基础性地位。近年来，基于合成数据训练的稀疏点跟踪模型（如 **Track-On2**、**LocoTrack**、**CoTracker3** 等）在标准基准上取得了显著进展。然而，这些模型面临一个核心瓶颈：**合成数据与真实世界视频之间存在显著的域间鸿沟**——合成场景中的运动模式、遮挡分布、光照变化和纹理复杂度与真实视频差异明显，导致模型在真实场景下的跟踪精度和鲁棒性大幅下降。

### 现有自训练方法的局限

为弥合这一鸿沟，研究者尝试通过自训练（self-training）在未标注的真实视频上微调模型：先用预训练跟踪器生成伪标签，再用这些伪标签监督模型在真实数据上的学习。然而，这一范式存在一个被忽视的关键问题：**单个预训练跟踪器产生的伪标签在帧间的可靠性波动极大**。如 Figure 2(b) 所示，同一教师模型在不同帧上的像素误差可以剧烈振荡，尤其在遮挡帧附近，预测质量急剧恶化。简单的随机选择教师模型（random teacher selection）或固定融合策略无法感知这种帧级质量波动，会不加区分地将噪声和漂移注入训练信号，导致自训练适应质量差甚至模型退化。

### 教师模型间的互补性与未利用空间

现实中有多个架构各异、互补性强的预训练跟踪器可用（如基于逐点匹配的 **TAPIR**、基于区域的 **LocoTrack**、联合多点建模的 **CoTracker3** 等）。一个自然的问题是：能否通过组合多个教师模型的输出来获得更高质量的伪标签？

Figure 2(a) 通过 Oracle 测试揭示了这一方向的巨大潜力：若在每一帧都“先知”地选择最准确的教师预测（Oracle），其性能远超任意单个教师模型，也远超随机选择基线。**Oracle 与单个教师/随机选择之间的巨大差距表明，逐帧自适应选择机制存在可观的提升空间**。然而，在真实无标注场景下，我们无法获知哪个教师的预测更准确，因此需要一个可学习的机制来评估各候选轨迹的帧级可靠性。

### 核心动机与本文思路

上述观察共同指向一个清晰的动机：

- **瓶颈**：在未标注真实视频上，单一教师伪标签的帧间质量波动破坏了自训练的稳定性；随机或固定融合策略放大了噪声和漂移。
- **机遇**：多个互补教师模型的存在，以及 Oracle 测试揭示的巨大提升空间，说明若能动态评估帧级可靠性并自适应选择伪标签，可将模型差异性转化为适应优势。
- **挑战**：如何在没有真实标注的情况下，训练出一个能够跨域评估跟踪预测可靠性的元模型？

本文的核心思路是引入一个**可学习的验证器（verifier）**——一个轻量级元模型，在每帧动态评估多个教师跟踪器输出的可靠性，并根据评分自适应选择最优候选作为伪标签。验证器完全在合成数据上训练，通过构造带有真实误差特征的扰动候选轨迹和对比学习目标，使其学会识别时空一致性线索，从而**跨域地**评估真实视频上的跟踪预测质量。这一设计将伪标签生成从“随机盲选”转变为“逐帧优选”，为后续的真实世界微调提供更干净、更稳定的监督信号。



## 核心方法与创新机理

本工作的核心创新在于提出 **验证器引导伪标注（Verifier-Guided Pseudo-Labeling）** 框架，将真实世界点跟踪的自训练适应问题重新表述为一个**逐帧可靠性评估与自适应选择**问题。与现有方法的关键差异体现在以下维度。

### 问题瓶颈的重新定位

在未标注的真实视频上，现有自训练方法通常从一组预训练教师模型中随机选择一个，用其预测作为伪标签。然而，如 Figure 2(a) 所示，单个教师模型的性能在不同帧之间波动剧烈，且始终远低于一个能够逐帧选择最优教师预测的 Oracle 上界。这一“Oracle 差距”揭示了核心瓶颈：**教师模型的帧间可靠性高度不一致，简单的随机选择或固定融合会放大噪声和漂移**，导致自训练适应质量差。

### 因果调节变量：可学习的验证器

针对上述瓶颈，本文引入了一个**可学习的验证器（verifier）**作为因果调节变量。验证器是一个元模型，不直接预测轨迹，而是在每帧动态评估多个教师跟踪器输出的可靠性，并根据该评分自适应选择伪标签。其核心机制在于：

- **跨域可靠性评估**：验证器完全在合成数据上训练，通过构造带有漂移、跳跃、遮挡和重现等真实错误模式的扰动候选轨迹，学习识别时空一致性线索。这使得验证器能够跨域地评估跟踪预测的可靠性，无需真实标注。
- **模型互补性利用**：验证器将多个互补的教师跟踪器组合成高质量、逐帧优选的伪标签，把模型差异性转化为适应优势，而非被其拖累。

### Changed Slots 对比

| 维度 | 基线方法 | 本文方法 |
|------|----------|----------|
| **伪标签生成策略** | 从一组预训练教师模型中随机选择一个，用其预测作为伪标签 | 使用验证器在每帧评估所有教师候选轨迹的可靠性，并动态选择得分最高的预测作为伪标签 |

这一替换看似简单，但其效果依赖于验证器架构的精心设计。验证器通过**局部特征提取**（使用冻结的 CoTracker3 CNN 编码器提取查询点和候选位置周围的视觉特征，并通过可变形注意力聚合上下文）和**候选 Transformer**（对查询特征与候选特征进行局部交叉注意力和时间自注意力，融合时空信息）来生成逐帧可靠性评分，最终通过温度缩放的余弦相似度转化为可靠性分布：

$$\hat{\mathbf{s}}_t = \mathrm{Softmax}(\mathbf{f}_t^q \cdot \mathbf{f}_t / \tau)$$

训练时，验证器以候选点与真实点之间的欧氏距离构造软标签分布作为监督信号：

$$\mathbf{s}_t = \mathrm{Softmax}( - \| \mathbf{C}_t - \mathbf{p}_t \| / \tau_s )$$

### 证据强度

这一创新的有效性得到了多层次验证：
- **Oracle 分析**（Figure 2(a)）直接量化了逐帧自适应选择的上界提升空间，为验证器的必要性提供了动机支撑（置信度 0.95）。
- **推理时集成实验**（Figure 4）表明，验证器集成在四个真实世界基准上一致优于所有单个教师模型和随机教师基线（置信度 0.95）。
- **自训练适应实验**（Table 1）显示，验证器引导的伪标注将 Track-On2 在 EgoPoints 上的 δ_avg^x 从 61.7 提升至 67.3，增益达 5.6 个点（置信度 0.95）。
- **消融实验**（Table 2）证实，无论使用哪组教师模型，验证器选择均优于随机选择，且推广到不同数据集和场景（置信度 0.95）。

### 局限性

需要指出的是，验证器的性能上限受限于所使用的教师跟踪器质量——若所有教师对某个特定运动模式或场景均表现不佳，验证器仍可能选出次优轨迹。此外，该方法在微调时需保留多个教师模型用于生成伪标签，增加了训练阶段的存储和计算开销。



本文提出了一种**验证器引导的伪标注**（Verifier-Guided Pseudo-Labeling）框架，旨在将合成数据上预训练的点跟踪模型高效地适应到真实世界视频。该框架的核心思想是：通过一个可学习的元模型——验证器（verifier），在每一帧动态评估多个预训练教师跟踪器的预测可靠性，并自适应地选择最优轨迹作为伪标签，从而将模型间的互补性转化为自训练的监督优势。

### 问题建模

给定一段 $T$ 帧的 RGB 视频 $\mathcal{V}$ 和查询帧 $t_0$ 上的查询点 $\mathbf{q}_{t_0}$，点跟踪任务的目标是预测该点在后续帧中的二维坐标 $\hat{\mathbf{p}}_t$ 和可见性 $\hat{v}_t$：

$$\{ (\hat{\mathbf{p}}_t, \hat{v}_t) \}_{t=t_0+1}^T = \Phi(\mathcal{V}, \mathbf{q}_{t_0})$$

从数据视角，系统面临两个域：**合成域** $\mathcal{D}_{\text{syn}}$（有真实标注）和**真实域** $\mathcal{D}_{\text{real}}$（无标注）。挑战在于，在 $\mathcal{D}_{\text{real}}$ 上直接自训练时，单个教师跟踪器的伪标签质量在帧间波动剧烈，简单的随机选择或固定融合会放大噪声和漂移。

### 动机：Oracle 分析

Figure 2(a) 的 Oracle 测试揭示了这一瓶颈的本质：在四个真实世界数据集上，逐帧选择最准确教师预测的 Oracle 与任一单个教师模型或随机选择基线之间存在巨大性能鸿沟。这一差距表明，**逐帧自适应选择机制存在显著的提升空间**。Figure 2(b) 进一步展示，不同教师的逐帧像素误差随时间剧烈波动，遮挡帧（灰色区域）的误差尤其突出——这直接驱动了验证器的设计。

### 整体 Pipeline

框架由三个核心阶段组成，如 Figure 1 所示：

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2603_12217/figures/001_Figure_1.jpg]]
*Figure 1: Verifier-guided real-world adaptation. (Left) Given a query point in a real-world video, multiple off-the-shelf trackers produce alternative trajectory hypotheses. Verifier evaluates these per-frame predictions and selects the most reliable ones, forming a refined pseudo-label trajectory. (Right) Unlike na¨ıve self-training, which randomly selects a teacher model for pseudo-label generation, the verifier adaptively combines predictions from multiple teachers, providing cleaner supervision for the student tracker during real-world fine-tuning*

1. **候选轨迹生成**：给定真实视频中的查询点，$M=6$ 个预训练的现成跟踪器（Track-On2、BootsTAPIR、BootsTAPNext、Anthro-LocoTrack、AllTracker、CoTracker3 Window）分别产生候选轨迹假设，构成候选张量 $\mathbf{C}$。

2. **验证器评分与伪标签选择**：验证器 $\Phi_{\text{ver}}$ 接收视频 $\mathcal{V}$、查询点 $\mathbf{q}_{t_0}$ 和候选轨迹 $\mathbf{C}$，输出逐帧的可靠性评分：

   $$\hat{\mathcal{S}} = \Phi_{\text{ver}}(\mathcal{V}, \mathbf{q}_{t_0}, \mathbf{C})$$

   对于每一帧，选择可靠性分数最高的候选作为伪标签；可见性则通过教师预测的多数投票估计。

3. **真实世界微调**：在合成数据 $\mathcal{D}_{\text{syn}}$（带真实标注）和真实数据 $\mathcal{D}_{\text{real}}$（带验证器生成的伪标签）的混合数据上微调基座模型 Track-On2，并采用**逐步增大真实样本损失权重**的调度策略，最终得到适应后的模型 Track-On-R。

### 验证器架构

验证器的内部结构如 Figure 3 所示，包含四个关键模块：

- **局部特征提取**：使用冻结的 CoTracker3 CNN 编码器提取逐帧密集特征图 $\mathbf{F}_t \in \mathbb{R}^{H' \times W' \times D}$，并在查询点和候选位置周围通过可变形注意力聚合局部上下文，生成紧凑的描述符。

- **候选 Transformer**：对查询特征 $\mathbf{f}^q$ 与候选特征 $\mathbf{f}_t$ 进行局部交叉注意力和时间自注意力，融合时空信息以产生更可靠的嵌入。

- **可靠性评分头**：通过温度缩放的余弦相似度将解码后的查询和候选特征转化为逐帧可靠性分布：

  $$\hat{\mathbf{s}}_t = \mathrm{Softmax}(\mathbf{f}_t^q \cdot \mathbf{f}_t / \tau), \quad \hat{\mathbf{s}}_t \in \mathbb{R}^M$$

- **训练目标**：验证器完全在合成数据上训练，使用对比目标。训练时根据候选点与真实点 $\mathbf{p}_t$ 的欧氏距离构造软标签分布：

  $$\mathbf{s}_t = \mathrm{Softmax}(-\|\mathbf{C}_t - \mathbf{p}_t\| / \tau_s)$$

  通过故意扰动候选轨迹来模拟真实误差模式（漂移、跳变、遮挡、重现），验证器学会了识别时空一致性线索，从而具备跨域评估跟踪预测可靠性的能力。

### 关键设计选择

与朴素自训练（随机选择一个教师模型生成伪标签）相比，本框架的差异化在于：验证器不是简单地固定选择或平均融合教师输出，而是**逐帧动态评估并切换**，从而将教师间的互补性转化为更干净、更可靠的监督信号。消融实验证实，无论使用哪组教师子集，验证器选择均一致优于随机选择（Table 2），且显著超越几何中位数、一致性选择、卡尔曼恒速选择等非学习集成方法（Table 5）。



### 问题形式化

点跟踪任务定义如下：给定一段 T 帧的 RGB 视频 $\mathcal{V}$ 和第 $t_0$ 帧上的查询点 $\mathbf{q}_{t_0}$，模型 $\Phi$ 需要预测该点在后续所有帧中的二维轨迹坐标与可见性：

$$\{ ( \hat{\mathbf{p}}_t, \hat{v}_t ) \}_{t=t_0+1}^T = \Phi(\mathcal{V}, \mathbf{q}_{t_0})$$

其中 $\hat{\mathbf{p}}_t \in \mathbb{R}^2$ 为第 $t$ 帧的预测坐标，$\hat{v}_t \in \{0, 1\}$ 为可见性标志（Equation 1, Section 3）。

数据层面，训练涉及两个域：有标注的合成数据 $\mathcal{D}_{\mathrm{syn}}$ 和无标注的真实数据 $\mathcal{D}_{\mathrm{real}}$。合成数据提供真值轨迹用于监督训练，真实数据则通过验证器生成伪标签实现自训练适应（Section 3）。

### 验证器整体框架

验证器 $\Phi_{\mathrm{ver}}$ 是一个元模型（metamodel），其核心功能是：接收视频、查询点和 $M$ 个预训练教师跟踪器产生的候选轨迹张量 $\mathbf{C}$，输出每帧各候选的可靠性评分：

$$\hat{\mathcal{S}} = \Phi_{\mathrm{ver}}(\mathcal{V}, \mathbf{q}_{t_0}, \mathbf{C})$$

其中 $\hat{\mathcal{S}} = \{\hat{\mathbf{s}}_t\}_{t=t_0+1}^T$，$\hat{\mathbf{s}}_t \in \mathbb{R}^M$ 为第 $t$ 帧上 $M$ 个候选的可靠性分布（Equation 2, Section 4）。

候选轨迹由 $M=6$ 个预训练教师跟踪器产生，包括 **Track-On2**、**BootsTAPIR**、**BootsTAPNext**、**Anthro-LocoTrack**、**AllTracker** 和 **CoTracker3**（窗口变体）。验证器通过比较预测位置周围的视觉特征与初始查询点的特征，跨教师、跨时间地推理出每帧的可靠性评分，而非直接预测轨迹（Section 4.1）。

### 局部特征提取模块

验证器首先使用冻结的 CoTracker3 CNN 编码器 $\phi_{\mathrm{enc}}$ 对所有帧提取下采样特征图：

$$\mathbf{F}_t = \phi_{\mathrm{enc}}(\mathbf{I}_t), \quad \mathbf{F}_t \in \mathbb{R}^{H' \times W' \times D}$$

其中 $H' \times W'$ 为下采样后的空间分辨率，$D$ 为特征通道数（Equation 3, Section 4.2）。

在查询帧 $t_0$ 上，通过双线性采样获取查询点的参考嵌入：

$$\mathbf{q}_{\mathrm{sample}} = \mathrm{sample}(\mathbf{F}_{t_0}, \mathbf{q}_{t_0}) \in \mathbb{R}^D$$

该嵌入作为后续跨帧匹配的锚点（Equation 4, Section 4.2）。

对于每个候选轨迹，模块在候选位置 $\mathbf{C}_t$ 周围应用可变形注意力 $\phi_{\mathrm{def}}$ 聚合局部上下文，产生候选描述符 $\mathbf{h}_t$。同时，将位移嵌入 $\eta(\cdot)$ 与身份嵌入拼接，通过投影层 $\phi_{\mathrm{proj}}$ 得到最终的查询特征 $\mathbf{f}_t^q$ 和候选特征 $\mathbf{f}_t$（Figure 5, Section 4.2）。

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2603_12217/figures/008_Figure_5.jpg]]
*Figure 5: Localized Feature Extraction. Given frame-wise features of the query frame*

### 候选 Transformer 与可靠性评分

候选 Transformer 由多层堆叠构成，每层包含三个子模块：局部交叉注意力（localized cross-attention）、时间自注意力（temporal self-attention）和前馈网络。交叉注意力仅在查询特征与对应候选特征之间进行（受限范围），时间自注意力则沿时间维度建模帧间依赖，从而融合时空一致性信息（Section 4.3, Figure 3 右）。

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2603_12217/figures/003_Figure_3.jpg]]
*Figure 3: Verifier overview. Given query points at frame*

最终，验证器通过温度缩放的余弦相似度将查询特征与候选特征转化为逐帧的可靠性分布：

$$\hat{\mathbf{s}}_t = \mathrm{Softmax}(\mathbf{f}_t^q \cdot \mathbf{f}_t / \tau), \quad \hat{\mathbf{s}}_t \in \mathbb{R}^M$$

其中 $\tau$ 为温度参数，$\hat{\mathbf{s}}_t^{(m)}$ 表示第 $m$ 个候选在第 $t$ 帧的可靠性分数（Equation 9, Section 4.3）。

### 训练目标与伪标签构造

验证器完全在合成数据上训练。给定真值轨迹 $\mathbf{p}_t$，训练时根据候选点与真值之间的欧氏距离构造软标签分布：

$$\mathbf{s}_t = \mathrm{Softmax}( - \| \mathbf{C}_t - \mathbf{p}_t \| / \tau_s ), \quad \mathbf{s}_t \in \mathbb{R}^M$$

其中 $\tau_s$ 为距离温度参数。该软标签引导验证器学习将高分分配给空间上更接近真值的候选（Equation 10, Section 4.4）。训练使用交叉熵损失，使预测分布 $\hat{\mathbf{s}}_t$ 逼近目标分布 $\mathbf{s}_t$。

在真实世界微调阶段，对每个查询点，选择验证器评分最高的候选轨迹作为伪标签。可见性通过多数投票（majority voting）估计：若多数教师认为该点可见，则标记为可见。最终在 $\mathcal{D}_{\mathrm{syn}}$ 和 $\mathcal{D}_{\mathrm{real}}$ 的混合数据上微调 Track-On2 基座模型，逐步增大真实样本的损失权重，得到适应后的模型 Track-On-R（Section 4.5）。

### 候选扰动构造

为训练验证器识别典型跟踪失败模式，合成数据上的候选轨迹通过故意扰动真值生成：包括随机漂移（模拟累积误差）、跳跃（模拟错误匹配）、遮挡丢失（模拟可见性误判）和重现身偏移（模拟遮挡后位置偏差）。这些扰动使验证器学会从视觉特征中辨别时空不一致性，从而在未见过的真实视频上泛化（Section 1, Section 4.4）。



## 实验与关键发现

### 核心瓶颈与动机验证

在真实世界视频上进行点跟踪自训练的核心瓶颈在于：单一下游预训练跟踪器产生的伪标签在帧间可靠性波动极大（Figure 2(b) 中可见各教师模型的逐帧像素误差曲线剧烈起伏），简单的随机选择或固定融合策略会放大噪声和漂移，导致适应质量差。Figure 2(a) 的 Oracle 实验直接量化了这一瓶颈——在四个真实世界数据集上，逐帧选择最准确教师预测的 Oracle 性能显著高于任何单个教师模型以及随机选择基线，二者之间存在巨大差距。这一发现表明，**自适应、逐帧的伪标签选择机制**存在可观的提升空间，直接促成了验证器（verifier）的设计动机。

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2603_12217/figures/002_Figure_2.jpg]]
*Figure 2: Teacher inconsistency and oracle performance. (a) Across 4 real-world datasets, six off-the-shelf teacher models (shown on the legend) are compared against an oracle that, at each frame, selects the most accurate teacher prediction. Individual teachers (colored circles) cluster below the oracle (diamonds), while the black horizontal line marks the performance of random teacher selection. The large gap between the oracle and both individual models and random selection highlights the substantial headroom available for adaptive, per-frame selection. (b) Example from TAP-Vid Kinetics [11]: Teacher predictions whose pixel errors fluctuate across time. The upper plot shows per-frame pixel error c...*

### 主实验结果

Table 1 汇总了在四个真实世界基准上的主实验结果。我们以合成数据预训练的 **Track-On2** 作为基座模型，通过验证器引导伪标注进行真实世界微调后得到 **Track-On-R**，在所有基准上均实现了显著提升：

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2603_12217/figures/005_Table_1.jpg]]
*Table 1: Quantitative results on real-world datasets. Comparison with prior work on EgoPoints, RoboTAP, TAP-Vid Kinetics, and TAP-Vid DAVIS in terms of*

- **EgoPoints**：$\delta_{\text{avg}}^x$ 从 61.7 提升至 67.3（+5.6），OA 达到 90.2，在所有方法中取得最优。
- **RoboTAP**：AJ 从 68.1 提升至 70.9（+2.8），OA 达到 94.0，同样领先于包括 BootsTAPIR 等大规模自蒸馏方法在内的先前工作。
- **TAP-Vid Kinetics**：AJ 从 55.3 提升至 57.8（+2.5），OA 达到 90.5。
- **TAP-Vid DAVIS**：AJ 从 67.0 提升至 68.1（+1.1），OA 达到 92.5。

值得注意的是，Track-On-R 在合成基准 Dynamic Replica 和 PointOdyssey 上也保持了与纯合成基线相当的性能（Table 4），表明真实世界微调并未牺牲模型在合成域上的泛化能力。

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2603_12217/figures/010_Table_4.jpg]]
*Table 4: Quantitative results on synthetic benchmarks. We compare the synthetic baseline Track-On2 with our real-world fine-tuned variant (Track-On-R) on Dynamic Replica (DR) and PointOdyssey*

### 推理时集成的有效性

Figure 4 展示了验证器作为推理时集成方法的性能。在不进行任何微调的情况下，仅通过验证器在推理时动态选择教师预测，其性能即**一致优于随机教师基线和最强单个教师模型**。这证明了验证器能够有效利用不同跟踪器的互补性——不同模型在不同帧、不同运动模式下的可靠性各异，验证器学会了识别这些差异并做出最优选择。

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2603_12217/figures/004_Figure_4.jpg]]
*Figure 4: Verifier as inference time ensemble. Comparison of the verifier ensemble against individual teacher models and the randomteacher baseline on real-world datasets. All teacher results are reproduced using their official checkpoints. The verifier consistently achieves the best performance across datasets, demonstrating its ability to exploit the complementary strengths of different models*

### 消融实验

**教师组合的影响（Table 2）**：无论使用哪组教师模型子集，验证器选择（Ver.）均一致优于随机选择（Rand.），表明验证器的选择能力具有鲁棒性，不依赖于特定的教师组合。

**微调数据配比（Table 3）**：我们比较了三种配置：仅使用真实数据（Real）、真实与合成数据混合（Mix）、以及混合数据配合逐步增大真实损失权重的调度策略（Mix + Schedule）。Mix + Schedule 在所有基准上取得了最佳整体性能，纯真实训练虽然在定位精度上略优，但遮挡精度有所下降，说明合成数据在微调过程中仍然起到重要的正则化作用。

**与非学习集成方法的对比（Table 5）**：我们将验证器与几何中位数、一致性选择、卡尔曼恒速预测等固定启发式集成策略进行了对比。验证器在所有数据集上均大幅优于这些非学习方法，尤其是在挑战性最大的 EgoPoints 上优势最为显著，表明学习到的自适应选择机制远非简单启发式规则所能替代。

**真实数据规模的影响（Table 6）**：仅使用 TAO 数据集（约 2.9K 视频）即可取得大部分适应增益，进一步增加 OVIS 和 VSPW 数据（总计约 4.9K 视频）带来的提升边际有限。这说明该方法具有较高的数据效率，在少量真实视频上即可实现有效的域适应。

### 失败模式与局限性

尽管验证器引导的自训练策略在多数场景下表现出色，其性能上限仍受限于所使用的教师跟踪器质量。当所有教师对某一特定运动模式（如极度快速旋转或严重运动模糊）均表现不佳时，验证器可能选出次优轨迹，因为它只能从已有候选中择优，而无法“创造”更好的预测。此外，伪标签的质量高度依赖验证器的跨域泛化能力——验证器完全在合成数据上训练，若真实视频的视觉特性（如光照、纹理分布）与合成训练数据差异过大，可靠性评分的准确性可能下降。

### 关键图表结论速览

| 图表 | 核心结论 |
|------|----------|
| Figure 2(a) | Oracle 与单个教师/随机选择之间存在巨大差距，验证了自适应逐帧选择的必要性 |
| Figure 4 | 验证器推理时集成一致优于所有单个教师和随机基线，证明互补性利用有效 |
| Table 1 | Track-On-R 在四个真实世界基准上全面超越合成基线和先前方法 |
| Table 2 | 验证器选择在不同教师子集上均优于随机选择，鲁棒性强 |
| Table 3 | Mix + Schedule 策略在定位精度与遮挡鲁棒性之间取得最佳平衡 |
| Table 5 | 学习到的验证器大幅优于所有非学习启发式集成方法 |
| Table 6 | 仅 2.9K 真实视频即可实现大部分适应增益，数据效率高 |

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2603_12217/figures/006_Table_2.jpg]]
*Table 2: Effect of teacher composition on verifier performance. We report*

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2603_12217/figures/007_Table_3.jpg]]
*Table 3: Synthetic vs. real data during fine-tuning. We compare three configurations: Real (only*

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2603_12217/figures/011_Table_5.jpg]]
*Table 5: Non-learning ensemble baselines vs. verifier. Comparison of fixed ensemble heuristics and the learned verifier on four benchmarks measured by*

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2603_12217/figures/009_Table_6.jpg]]
*Table 6: Effect of the*

### 补充图表

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2603_12217/figures/012_Figure_6.jpg]]
*Figure 6: Verifier selection behavior across videos. Each row corresponds to a different video from TAP-Vid Kinetics. Frames are uniformly sampled among visible ones, and a 50 × 50 crop centered at the ground-truth point is shown. Colored dots indicate predictions from teacher trackers, the star marks the ground-truth location, and the legend lists the verifier reliability scores, with the selected candidate highlighted in bold. The verifier adaptively switches between trackers across frames, assigning higher scores to spatially accurate predictions while suppressing unreliable ones*



## 定位与知识库关联

### 1. 问题定位：点跟踪的自训练瓶颈

点跟踪（Point Tracking）任务要求在给定视频 $\mathcal{V}$ 和查询点 $\mathbf{q}_{t_0}$ 的条件下，预测该点在后续所有帧中的二维轨迹和可见性：

$$\{ ( \hat{\mathbf{p}}_t, \hat{v}_t ) \}_{t=t_0+1}^T = \Phi(\mathcal{V}, \mathbf{q}_{t_0})$$

现有方法主要沿两条路径发展：**合成数据预训练**和**真实世界微调**。前者以 **Track-On2**、**CoTracker3** (Karaev et al., 2024) 等为代表，在合成数据上训练出强泛化能力的基座模型；后者如 **BootsTAPIR** (Doersch et al., 2024) 和 **BootsTAPNext**，通过自蒸馏或自训练将模型适配到真实场景。然而，真实世界微调的核心瓶颈在于：**在未标注的真实视频上，单个预训练跟踪器产生的伪标签在帧间可靠性波动极大**——从 Figure 2(b) 可见，同一教师模型在不同帧的像素误差剧烈振荡，遮挡帧（灰色区域）尤其明显。简单的随机选择教师或固定融合策略会放大噪声和漂移，导致自训练适应质量差。

### 2. 核心方法差异：从随机选择到验证器引导

本工作提出的 **Verifier-Guided Pseudo-Labeling** 与现有自训练范式的根本差异在于伪标签生成策略（changed_slot）：

| 维度 | 基线策略 | 本方法策略 |
|------|----------|------------|
| 教师模型使用 | 从预训练教师集合中随机选择一个，用其全部预测作为伪标签 | 使用可学习验证器在每帧动态评估所有教师候选轨迹的可靠性，逐帧选择得分最高的预测 |
| 模型差异性利用 | 差异性被视为噪声源，通过随机化规避 | 差异性被视为互补信号源，通过验证器转化为适应优势 |
| 训练信号 | 仅在合成数据上训练跟踪器 | 验证器在合成数据上训练（学习时空一致性线索），跟踪器在合成+真实混合数据上微调 |

验证器的核心公式为：

$$\hat{\mathbf{s}}_t = \mathrm{Softmax}(\mathbf{f}_t^q \cdot \mathbf{f}_t / \tau)$$

其中 $\mathbf{f}_t^q$ 和 $\mathbf{f}_t$ 分别是通过 Candidate Transformer 解码后的查询特征和候选特征，$\tau$ 为温度参数。训练时，目标分布由候选点与真实点之间的欧氏距离构造：

$$\mathbf{s}_t = \mathrm{Softmax}( - \| \mathbf{C}_t - \mathbf{p}_t \| / \tau_s )$$

### 3. 与相关工作的关系

**与 BootsTAPIR / BootsTAPNext 的关系**：这些方法属于真实世界微调基线，通过大规模自蒸馏利用未标注视频。但它们依赖单一教师模型或固定融合策略生成伪标签，无法像本方法那样逐帧自适应地利用多个教师的互补性。Table 1 显示，Track-On-R 在四个真实基准上全面超越 BootsTAPIR 和 BootsTAPNext。

**与 CoTracker3 的关系**：CoTracker3 是联合多点跟踪的 Transformer 模型，本方法将其冻结的 CNN 编码器用作局部特征提取骨干（$\phi_{\mathrm{enc}}$），并选取其窗口变体作为六位教师之一。这是一种模块级复用而非方法级继承。

**与 LocoTrack / TAPIR 的关系**：这些是早期的逐点或基于区域的跟踪方法，在本工作中作为教师模型集合的组成部分，用于提供互补的轨迹假设。

### 4. 适用边界与局限

验证器引导伪标注的有效性受以下边界条件约束：

1. **教师质量上限**：验证器的性能天花板由教师集合的整体能力决定。若所有教师对特定运动模式（如极端快速旋转、严重运动模糊）均表现不佳，验证器仍可能选出次优轨迹。这是方法的内在局限，而非工程问题。

2. **跨域泛化依赖**：验证器完全在合成数据上训练，其可靠性评分的准确性取决于合成数据中构造的扰动（漂移、跳跃、遮挡、重现）能否覆盖真实场景的误差模式。如果真实视频的视觉特性与合成训练数据差异过大，评分可能不够准确。

3. **训练阶段的计算开销**：微调时需要保留多个教师模型用于生成伪标签，增加了存储和计算负担。这与 BootsTAPIR 等单教师自蒸馏方法相比是一个实际的部署成本。

4. **数据效率的边际递减**：Table 6 显示，仅使用 TAO 数据集（约 2.9K 视频）即可取得大部分适应增益，额外增加 OVIS 和 VSPW 带来的提升有限。这表明方法的真实数据需求存在饱和点。

### 5. 开放问题

1. **教师集合的扩展性**：能否将验证器与更强的基础模型（如基于大规模预训练的动态跟踪器）结合，以突破当前教师质量设定的上限？验证器架构本身支持任意数量的候选输入，但评分质量对教师能力的依赖性尚未被系统性研究。

2. **半监督扩展**：验证器的训练目前完全依赖合成扰动的构造方式。是否可以通过引入少量真实标注来改进评分模型的跨域鲁棒性？这涉及到主动学习或弱监督学习的交叉方向。

3. **任务泛化性**：该框架的核心思想——学习一个元模型来评估多源预测的逐帧可靠性——是否能够扩展到其他需要时序质量评估的视频理解任务，如光流估计、视频物体分割或多目标跟踪？这需要验证时空一致性线索在不同任务中的可迁移性。

4. **合成训练策略的改进**：当前验证器训练中的候选扰动是人工设计的。是否可以通过对抗生成或基于扩散模型的方式构造更逼真的伪误差，从而提升验证器在真实场景中的判别能力？



## 原文 PDF

![[paperPDFs/CVPR_2026/Real_World_Point_Tracking_with_Verifier_Guided_Pseudo_Labeling.pdf]]
