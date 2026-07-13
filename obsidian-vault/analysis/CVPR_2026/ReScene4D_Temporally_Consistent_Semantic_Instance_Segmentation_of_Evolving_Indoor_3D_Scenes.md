---
title: "ReScene4D: Temporally Consistent Semantic Instance Segmentation of Evolving Indoor 3D Scenes"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ReScene4D_Temporally_Consistent_Semantic_Instance_Segmentation_of_Evolving_Indoor_3D_Scenes.pdf
project_link: "https://www.easteine.com/rescene4d/"
code_link: null
aliases:
- ReScene4D
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 跨时间观测的信息共享机制——通过时空对比损失、时空掩码和时空序列化，使实例查询能够自适应地融合语义与几何先验，从而实现时间一致的实例分割。
primary_logic: 尽管场景在稀疏观测间发生了未观察到的变化，通过灵活共享不同时间阶段的信息，可以同时提升单阶段实例分割质量和跨阶段身份一致性，而无需依赖密集时序采样或严格的几何对齐假设。
claims:
- ReScene4D 在多个时间观测之间始终保持一致的身份分配，即使对象移动或改变。
- 在3RScan数据集上，ReScene4D（Concerto骨干）达到34.8 t-mAP，远超 Mask4Former（17.0）和 Mask3D+geo（20.7）。
- 在相同骨干下，时空对比损失与时空序列化的组合带来了最显著的时序一致性增益。
- 3RScan 上 t-mAP = 34.8 (ReScene4D (C))
---

# ReScene4D: Temporally Consistent Semantic Instance Segmentation of Evolving Indoor 3D Scenes

> [!tip] 核心洞察
> 尽管场景在稀疏观测间发生了未观察到的变化，通过灵活共享不同时间阶段的信息，可以同时提升单阶段实例分割质量和跨阶段身份一致性，而无需依赖密集时序采样或严格的几何对齐假设。

| 字段 | 内容 |
|------|------|
| 中文题名 | ReScene4D：演变中室内3D场景的时间一致语义实例分割 |
| 英文题名 | ReScene4D: Temporally Consistent Semantic Instance Segmentation of Evolving Indoor 3D Scenes |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Steiner_ReScene4D_Temporally_Consistent_Semantic_Instance_Segmentation_of_Evolving_Indoor_3D_CVPR_2026_paper.html) · [Project](https://www.easteine.com/rescene4d/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ReScene4D |
| Dataset | 3RScan |

> [!tip] 效果简介
> - 3RScan 上，t-mAP 34.8 (ReScene4D (C)) vs 20.7 (Mask3D+geo) (+14.1)；mAP Stage 2 48.3 (ReScene4D (C)) vs 21.9 (Mask3D+geo) (+26.4)。

## 概要

**问题背景**：理解室内场景随时间的演变是具身智能与环境建模的核心需求。现有3D语义实例分割方法独立处理每一帧扫描，缺乏时序推理能力，必须依赖额外的后处理匹配步骤来关联跨时间的实例身份；而4D LiDAR全景分割方法则假设密集的时间采样，难以应对室内场景中常见的稀疏观测与大幅度未观察变化。这一瓶颈导致现有方法无法在稀疏时间观测下保持实例身份的时间一致性。

**核心洞察与因果机制**：ReScene4D 的核心发现是，尽管场景在稀疏观测之间发生了未观察到的变化，通过灵活共享不同时间阶段的信息，可以同时提升单阶段实例分割质量和跨阶段身份一致性，而无需依赖密集时序采样或严格的几何对齐假设。这一因果杠杆通过三个协同的时间信息共享机制实现——时空对比损失、时空掩码和时空序列化——使实例查询能够自适应地融合语义与几何先验，从而实现时间一致的实例分割。

**方法定位**：ReScene4D 将 Mask3D（Schult et al., ICRA 2023）的掩码Transformer架构从3D语义实例分割适配到4D语义实例分割任务。关键改造包括：将独立3D点云替换为统一注册的时空4D点云表示，引入跨时间阶段共享的时空实例查询，以及设计4D Fourier位置编码。在此框架之上，时空对比损失在超级点特征上施加监督对比学习以促进时间一致的特征表示；时空掩码通过逻辑或池化实现跨阶段的掩码注意力引导；时空序列化在解码器中对时空点云混合使用空间与时间序列化模式。与 Mask4Former（Yilmaz et al., ICRA 2024）等4D全景分割方法的适配不同，ReScene4D 专为稀疏时序观测设计，不假设密集采样。

**主要结果**：在3RScan数据集上，ReScene4D（Concerto骨干）达到34.8 t-mAP，远超 Mask4Former（17.0）和 Mask3D+geo（20.7），提升幅度达+14.1（Table 1）。分阶段评估中，Stage 2的mAP从21.9提升至48.3（+26.4，Table 2）。消融实验表明，时空对比损失与时空序列化的组合带来了最显著的时序一致性增益（Table 3），而混合空间与时间序列化模式（3D & 4D）达到t-mAP 32.9，优于仅空间（28.4）或仅时间（32.0）模式（Table 4a）。定性结果（Figure 1）进一步验证，ReScene4D 在多个时间观测之间始终保持一致的身份分配，即使对象移动或改变，而基线方法无法准确分配静态和变化对象的实例身份。

**局限与开放问题**：当前进展受限于3RScan数据集多样性和标注质量，缺乏大规模、高度动态的室内4D数据集。时间信息共享的增益在现有数据规模下趋于饱和，可能需要在更丰富的时序变化场景中验证其上限。此外，ST-mask和ST-serialization单独使用会降低刚性变化性能但组合使用时却能互补的机制尚不明确，值得进一步探究。

### 问题背景：从静态场景理解到动态场景演变

3D 语义实例分割（3D Semantic Instance Segmentation, 3DSIS）旨在从单帧点云中同时识别物体类别并区分个体实例。近年来，基于 Transformer 的查询式方法（如 **Mask3D**，Schult et al., ICRA 2023）在这一任务上取得了显著进展。然而，现实世界的室内场景并非静态快照——家具被移动、物品被增减、房间布局随时间演变。理解这些变化对于机器人长期环境交互、AR/VR 场景更新和数字孪生维护至关重要。

这就要求将 3DSIS 扩展到时间维度，即 **4D 语义实例分割（4D Semantic Instance Segmentation, 4DSIS）**：给定一个场景在不同时间点的多次稀疏观测，联合输出跨所有时间阶段的语义实例掩码，并保持实例身份的时间一致性。

### 现有方法缺口：时序推理的缺失与假设的局限

现有方法在面对这一任务时存在两类根本性不足：

**第一类：3DSIS + 后匹配。** 最直接的思路是对每个时间阶段的点云独立运行 3DSIS，再通过后处理步骤匹配跨阶段的实例身份。典型方案包括：
- **语义匹配**（Mask3D+sem）：按语义类别分组，利用实例特征相似度进行匈牙利匹配。
- **几何匹配**（Mask3D+geo）：基于最近邻几何对应关系传递实例标签。

这类方法的核心问题是 **分割与关联的解耦**——实例分割质量直接影响匹配精度，且匹配过程依赖手工设计的相似度度量，缺乏端到端的时序一致性学习。当物体发生大幅度移动或形变时，几何对应和特征相似度假设均可能失效。

**第二类：4D 全景分割方法的直接迁移。** 来自自动驾驶领域的 4D LiDAR 全景分割方法（如 **Mask4D**，Marcuzzi et al., IEEE RA-L 2023；**Mask4Former**，Yilmaz et al., ICRA 2024）假设密集的时序采样，依赖相邻帧间的几何连续性和小幅度运动。当直接应用于室内场景的稀疏时间观测（如相隔数小时或数天的两次扫描）时，这些方法面临根本性挑战：
- 两次观测之间可能发生了大量 **未观察到的变化**（unobserved changes）——物体被移动、替换或移除，几何对齐假设不再成立。
- 室内场景缺乏自动驾驶场景中的密集时序先验，无法依赖逐帧传播维持身份一致性。

实验证据直接印证了这一缺口：在 3RScan 数据集上，Mask4D 仅取得 **1.3 t-mAP**（Table 1），几乎无法工作；Mask4Former 也仅达到 17.0 t-mAP，远低于具备时序一致性设计的 ReScene4D。

### 核心瓶颈与本文动机

上述分析揭示了一个共同瓶颈：**现有方法无法在稀疏时间观测下保持实例身份的时间一致性**。3DSIS 方法缺乏时序推理能力，需要额外匹配步骤来弥补；4D LiDAR 方法则依赖密集时序采样和几何连续性假设，难以应对室内场景长间隔、大幅度的变化。

本文的核心动机在于：**能否设计一个统一的时空框架，使实例查询能够自适应地融合不同时间阶段的语义与几何信息，从而在稀疏观测条件下同时提升单阶段分割质量和跨阶段身份一致性？**

这一动机催生了 ReScene4D 的核心设计理念——通过跨时间观测的信息共享机制（时空对比损失、时空掩码、时空序列化），让模型在无需密集时序采样或严格几何对齐假设的前提下，学习时间一致的实例表示。

## 核心方法与创新机理

ReScene4D 的核心创新不在于提出全新的分割架构，而在于**将3D语义实例分割范式系统性地改造为时间一致的4D语义实例分割框架**，并通过三个关键改造点（changed slots）解决了现有方法在稀疏时序观测下实例身份漂移的根本瓶颈。

### 从3D到4D的范式改造

现有方法处理时序场景时存在两条路径，但均存在结构性缺陷：**Mask3D+sem/geo**（Schult et al., ICRA 2023）将每个时间步作为独立的3D语义实例分割任务，再通过语义或几何匹配进行后关联，缺乏端到端的时序推理能力；**Mask4Former**（Yilmaz et al., ICRA 2024）和**Mask4D**（Marcuzzi et al., IEEE RA-L 2023）虽面向4D全景分割，但依赖密集时序采样，难以应对室内场景中长间隔、大幅度的物体变化。ReScene4D 的改造体现在以下四个维度：

**1. 输入表示：从独立3D点云到统一时空4D点云**

ReScene4D 将时间序列中的多个3D扫描表示为统一注册的时空4D点云 $\mathcal{P} \in \mathbb{R}^{N \times 4}$，显式保留时间坐标作为第四维（Section 3.2）。这一改造使得骨干网络能够在一个统一的坐标框架下处理所有时间步的点，为后续的跨时间信息共享提供了结构基础。

**2. 查询机制：从单阶段实例查询到跨时间共享的时空实例查询**

传统3D实例分割的查询（query）仅负责单个扫描内的实例分组。ReScene4D 将查询扩展为**时空实例查询**，每个查询负责跨所有时间阶段预测同一个实例的掩码和语义类别。这意味着模型必须学习将不同时间步中属于同一实例的点关联到同一个查询下，从根本上避免了后匹配步骤中的身份歧义。

**3. 位置编码：从3D Fourier特征到4D Fourier特征**

为适应4D点云的输入，ReScene4D 将位置编码从 $(x, y, z)$ 三维 Fourier 特征扩展为 $(x, y, z, t)$ 四维 Fourier 特征（Section 3.2）。时间维度的编码使得模型能够区分空间位置相同但时间不同的点，这是处理物体移动场景的关键。

**4. 时间信息共享：对比损失 + 时空掩码 + 时空序列化**

这是 ReScene4D 最核心的创新模块，由三个互补机制构成（Section 3.3, Figure 2）：

- **跨时间监督对比损失**：在超级点（superpoint）特征上施加监督 InfoNCE 对比损失，以整个时间序列的实例标注定义正负样本对。具体而言，二元关系矩阵 $R_{GT}(i, j) = 1$ 当且仅当点 $i$ 和 $j$ 在整个序列中属于同一实例。这使得模型在特征空间中拉近同一实例跨时间的表示，推远不同实例的表示，从而隐式学习时间不变性。

- **时空掩码**：通过逻辑或池化将跨阶段的掩码注意力进行融合，使解码器在优化查询时能够同时关注来自不同时间步的证据。

- **时空序列化**：在解码器中随机混合空间序列化（3D）和时间序列化（4D）模式，迫使查询在迭代优化过程中交替利用空间上下文和时间上下文，避免对单一模式的过拟合。

### 创新的因果逻辑

这些改造点并非孤立存在，而是围绕一个核心因果机制设计：**通过灵活共享不同时间阶段的信息，使实例查询能够自适应地融合语义与几何先验，从而同时提升单阶段分割质量和跨阶段身份一致性**。消融实验（Table 3）证实了这一设计的协同效应：单独使用对比损失或时空序列化均能带来增益，但三者组合时达到最优的 t-mAP 34.8，表明各模块之间存在互补关系——对比损失提供特征层面的时间一致性约束，时空掩码提供注意力层面的跨时间引导，时空序列化提供解码器层面的信息混合路径。

ReScene4D 的整体 pipeline 围绕一个核心设计展开：将时间上稀疏的 3D 扫描序列建模为统一的时空 4D 点云，并通过跨时间阶段的信息共享机制，使实例查询能够自适应地融合语义与几何先验，从而在单阶段分割质量和跨阶段身份一致性两个维度上同时取得提升。

### 输入与输出

输入为一个时间有序的 3D 扫描序列 $\mathcal{P} = \{P^{(1)}, ..., P^{(T)}\}$，各阶段点云已预先配准到统一坐标系。输出为跨整个序列的 $K$ 个实例掩码 $\bar{\mathcal{M}} = \{m^1, ..., m^K\}$，每个掩码定义了一个实例在所有时间阶段中的点集归属。

### 三大核心模块

如 Figure 2 所示，ReScene4D 的架构由以下模块串联构成：

![[assets/figures/papers/paper_list_l41_https_openaccess_thecvf_com_content_CVPR2026_html_Steiner_ReScene4D_Temp/figures/002_Figure_2.jpg]]
*Figure 2: Overview of ReScene4D Architecture. Given a temporal sequence of T 3D observations, hierarchical features for each temporal stage, preserving temporal distinction are extracted using a backbone encoder . A transformer-based query decoder iteratively refines spatio-temporal (ST) instance queries by jointly sampling across temporal hierarchical features . Given ST superpoint features and ST queries, the mask module predicts joint binary masks and semantic classes consistent across the sequence. Adaptations for 4DSIS are denoted in purple. Our temporal information sharing modules ⃝1 , ⃝2 , ⃝3 facilitate cross-temporal consistency and shared learning via cross-time contrastive loss, ST mask poo...*

1. **时空骨干编码器（Backbone Encoder）**：接收统一注册的时空 4D 点云 $\mathcal{P} \in \mathbb{R}^{N \times 4}$（其中 $N = \sum_{t=1}^{T} N_t$，第四维为时间坐标），提取各时间阶段的分层特征。编码器保持冻结状态，其序列化模式与原始预训练保持一致，以避免域偏移。

2. **查询解码器（Query Decoder）**：基于 Transformer 的迭代优化模块，通过掩码交叉注意力在时空分层特征上联合采样，逐步精化时空实例查询。关键改造在于引入 4D Fourier 位置编码（x, y, z, t）替代原有的 3D Fourier 特征，使查询具备时间维度的感知能力。

3. **掩码模块（Mask Module）**：以时空超级点特征和精化后的时空查询为输入，预测跨所有时间阶段的联合二值掩码和语义类别。通过将预测/真值实例定义为所有阶段点集的并集——$pr_i(c) = \bigcup_{t=1}^{T} p_i(c,t)$ 和 $gt_i(c) = \bigcup_{t=1}^{T} g_i(c,t)$——实现时间上统一的实例表示。

### 时间信息共享机制

上述模块之间通过三个紫色标注的时间信息共享组件（Figure 2 中 ⃝1⃝2⃝3）实现跨阶段一致性，这是 ReScene4D 区别于单阶段 3DSIS 方法的核心差异：

- **跨时间对比损失（Contrastive Loss）**：在超级点特征上施加监督 InfoNCE 对比损失 $\mathcal{L}_{\mathrm{cont}}$，以整个时间序列的实例标注定义正样本对（$R_{GT}(i,j)=1$ 当且仅当点 i 和 j 属于同一实例），强制同一实例在不同时间阶段的特征表示相互靠近，不同实例的特征相互远离。

- **时空掩码池化（ST Masking）**：通过逻辑或池化将不同阶段的掩码注意力引导信号融合，使查询能够跨阶段共享实例定位信息。

- **时空解码器序列化（ST Decoder Serialization）**：在解码器的每个层级，随机混合原始空间序列化模式与跨整个序列的时空序列化模式，使查询在迭代过程中交替感知空间局部结构和时间全局关联。

### 问题形式化

ReScene4D 将 4D 语义实例分割（4DSIS）定义如下：给定同一场景在时间上稀疏采样的 $T$ 个 3D 扫描序列 $\mathcal { P } = \{ P ^ { ( 1 ) } , . . . , P ^ { ( T ) } \}$，目标是预测跨整个序列的 $K$ 个实例掩码 $\bar { \mathcal { M } } = \{ m ^ { 1 } , . . . , m ^ { K } \}$，使得同一实例在不同时间阶段的身份保持一致。所有时间阶段的总点数定义为：

$$N = \sum _ { t = 1 } ^ { T } N _ { t }$$

### 时空 4D 点云表示

方法的核心输入改造是将时间上独立的 3D 扫描统一注册为一个时空 4D 点云（Section 3.2）：

$$\mathcal { P } \in \mathbb { R } ^ { N \times { 4 } }$$

这一表示将空间坐标 $(x, y, z)$ 与时间坐标 $t$ 拼接，使骨干网络能够在一个统一的张量中感知点的时空位置。相应地，位置编码从 3D Fourier 特征扩展为 4D Fourier 特征，以编码时间维度信息。

### 骨干编码器与查询解码器

ReScene4D 沿用 Mask3D（Schult et al., ICRA 2023）的掩码 Transformer 架构（Section 3.1），并针对 4DSIS 进行适配。骨干编码器对 4D 点云提取分层特征，保留各时间阶段的时序区分性。Transformer 查询解码器通过掩码交叉注意力迭代优化时空实例查询，这些查询在跨时间阶段的特征层级上联合采样，从而实现时间共享的实例表示。

### 时间信息共享三大模块

为实现跨时间观测的信息共享，ReScene4D 引入三个关键模块（Section 3.3, Figure 2）：

**时空对比损失** 在超级点特征上施加监督对比学习。首先定义二值关系矩阵来标识跨时间阶段的同一实例点对：

$$R _ { G T } ( i , j ) = { \left\{ \begin{array} { l l } { 1 , } & { { \mathrm { i f ~ } } i , j { \mathrm { ~ b e l o n g ~ t o ~ t h e ~ s a m e ~ i n s t a n c e } } , } \\ { 0 , } & { { \mathrm { o t h e r w i s e } } , } \end{array} \right. }$$

基于此，对有多个正样本的超级点特征计算监督 InfoNCE 对比损失：

$$\mathcal { L } _ { \mathrm { c o n t } } = - \frac { 1 } { | S ^ { + } | } \sum _ { i \in S ^ { + } } \log \frac { \sum _ { j \in P ( i ) } \exp ( L _ { i j } ) } { \sum _ { k } \exp ( L _ { i k } ) }$$

该损失强制同一实例的超级点特征在嵌入空间中聚集，不同实例的特征相互推开，从而在特征层面建立时间一致性。

**时空掩码** 通过逻辑或池化将查询在各时间阶段的掩码预测融合为联合掩码，引导解码器的掩码注意力跨阶段共享实例信息（Figure 2）。

**时空解码器序列化** 在解码器的每个层级中，随机混合原始空间序列化模式和跨整个序列的时空序列化模式。同时，对于冻结的预训练编码器保持序列化模式固定，以确保输入分布与骨干预训练一致，避免域偏移（Section 3.3）。

此外，为抑制跨时间的重复预测，未匹配预测的 no-object 语义损失权重被提高至 $\lambda _ { n o o b j } = 0.2$，高于单阶段设置（Section 3.2）。

### 时间一致性评估度量

为联合评估分割质量和时间身份一致性，ReScene4D 定义了时序 IoU（t-IoU）。预测实例和真值实例分别定义为所有时间阶段点集的并集：

$$p r _ { i } ( c ) = \bigcup _ { t = 1 } ^ { T } p _ { i } ( c , t ) \quad { \mathrm { a n d } } \quad g t _ { i } ( c ) = \bigcup _ { t = 1 } ^ { T } g _ { i } ( c , t )$$

正检测的条件是所有阶段的最小 IoU 必须超过阈值 $\tau$：

$${ \mathrm { t } } \mathrm { I o U } ( p _ { i } ( c ) , g _ { i } ( c ) ) : = \operatorname* { m i n } _ { t \in [ 1 , T ] } \{ \mathrm { I o U } ( p _ { i } ( c , t ) , g _ { i } ( c , t ) ) \} > \tau$$

这一度量确保实例在所有观测时刻的分割质量都达到要求，而非仅在平均意义上表现良好（Figure 3 通过案例展示了 t-IoU 与标准 IoU 的差异）。

![[assets/figures/papers/paper_list_l41_https_openaccess_thecvf_com_content_CVPR2026_html_Steiner_ReScene4D_Temp/figures/003_Figure_3.jpg]]
*Figure 3: Toy Examples for Temporal Metrics. Right: summary table showing IoU and t-IoU scores for four cases*

## 实验与关键发现

### 4DSIS 主结果：时间一致性的量化飞跃

Table 1 报告了在 3RScan 数据集上 4DSIS 的核心指标 t-mAP 与标准 mAP。ReScene4D 在所有骨干配置下均大幅超越基线，其中最强配置 **ReScene4D (Concerto)** 达到 **34.8 t-mAP**，相较最强基线 **Mask3D+geo**（20.7）提升 **+14.1 点**，相较 **Mask4Former**（17.0）提升 +17.8 点。值得注意的是，专为 4D LiDAR 全景分割设计的 **Mask4D** 仅获 1.3 t-mAP，验证了密集时序假设在稀疏室内观测下的根本失效。

![[assets/figures/papers/paper_list_l41_https_openaccess_thecvf_com_content_CVPR2026_html_Steiner_ReScene4D_Temp/figures/004_Table_1.jpg]]
*Table 1: 4DSIS Scores on the 3RScan dataset [37]. We report both the t-mAP and standard mAP scores with different IoU thresholds averaged over 18 classes*

这一差距的因果根源在于基线方法缺乏跨时间的信息共享机制：Mask3D+geo 和 Mask3D+sem 依赖独立 3D 分割后的几何或语义匹配，匹配错误在稀疏观测间被放大；Mask4Former 虽引入时序建模，但其 4D 全景分割设计无法适应室内场景长间隔、大幅度的实例变化。ReScene4D 通过统一的时空实例查询，在分割与身份分配两个维度上实现了端到端的联合优化。

Table 2 的分阶段 3DSIS mAP 进一步揭示了时间一致性对单阶段分割质量的反哺效应。在 Stage 2 上，ReScene4D (Concerto) 达到 **48.3 mAP**，远超 Mask3D+geo 的 21.9（+26.4），表明跨时间的信息共享不仅维持了身份一致性，还显著提升了个体阶段的分割精度。这一反哺效应的机制在于：时空对比损失迫使同一实例在不同阶段的特征表示趋于一致，从而在解码器迭代中增强了查询对目标实例的判别力。

![[assets/figures/papers/paper_list_l41_https_openaccess_thecvf_com_content_CVPR2026_html_Steiner_ReScene4D_Temp/figures/005_Table_2.jpg]]
*Table 2: Per-stage 3DSIS mAP on 3RScan [37]. Joint 4D predictions are evaluated independently at each 3D temporal stage*

### 时间信息共享策略的消融分析

Table 3 系统拆解了三种时间信息共享策略的贡献。基线（无任何时间共享）t-mAP 为 28.2。单独引入对比损失（Lcontr）将 t-mAP 提升至 31.0（+2.8），且在刚性变化子集上 t-mREC 从 44.9 跃升至 48.4（+3.5），表明对比学习对几何对齐但身份不同的实例区分最为有效。然而，单独引入 ST-mask 或 ST-serialization 时，刚性变化性能反而下降，暴露了这些模块在缺乏对比约束时可能引入跨时间的特征混淆。

![[assets/figures/papers/paper_list_l41_https_openaccess_thecvf_com_content_CVPR2026_html_Steiner_ReScene4D_Temp/figures/008_Table_3.jpg]]
*Table 3: Ablation of temporal information sharing strategies in 4DSIS. Rows show combinations of contrastive loss (Lcontr), spatio-temporal serialization (ST-serial), and spatiotemporal masking (ST-mask), with t-mAP and temporal recall (tmREC) reported for ambiguous, rigid, and non-rigid instances. Best overall t-mAP is in green , baseline in blue , and gray denotes combinations that do not exceed individual method performance*

三者组合（Lcontr + ST-serial + ST-mask）达到 **32.9 t-mAP**，超越任何单一或双组合配置。这种互补效应暗示了一个非线性交互机制：对比损失提供了跨时间的语义锚点，ST-mask 通过逻辑或池化扩展了查询的时空感受野，而 ST-serialization 在解码器中混合空间与时间序列化模式，三者协同才使查询能够自适应地平衡几何与语义先验。

Table 4a 进一步消融序列化模式。混合空间与时间序列化（3D & 4D）达到 t-mAP 32.9，优于仅空间序列化（28.4）和仅时间序列化（32.0）。仅时间序列化虽能捕获跨阶段依赖，但丢失了空间局部性；仅空间序列化则无法建立时间对应。混合模式在每层解码器中随机打乱空间与时间序列化，使查询同时保有空间精细度和时间全局性。

Table 4b 验证了跨时间正负对比对的关键作用。在 4DSIS 训练中引入跨时间对比对，将 mAP 从 43.2 提升至 47.3（+4.1），而仅使用 3D 对比损失（无跨时间对）仅提升至 43.6。这直接证明了时间维度上的对比信号是时间一致性的核心驱动力，而非单纯的空间特征增强。

### 失败模式与局限性

尽管整体性能显著领先，消融实验揭示了若干值得关注的失败模式：

1. **刚性变化的性能权衡**：ST-mask 和 ST-serialization 单独使用时，刚性变化子集的 t-mREC 下降（Table 3），说明这些模块在缺乏语义对比约束时，可能将几何相似但身份不同的刚性实例误认为同一实例。组合使用时该问题被对比损失缓解，但刚性变化的 t-mREC（50.1）仍低于非刚性变化（56.1），暗示几何相似性仍是身份混淆的主要来源。

2. **时间信号增益的饱和趋势**：Table 3 中从双组合到三组合的增益（32.0 → 32.9）已明显小于从单策略到双策略的增益，这可能受限于 3RScan 数据集中有限的时间变化多样性。在更丰富的动态场景中，这些策略的潜力可能尚未完全释放。

3. **骨干依赖性**：公平比较中，ReScene4D (Minkowski) 的 t-mAP（28.2 基线）与 Mask3D+geo（20.7）的差距虽仍显著，但弱骨干下 Mask3D 的匹配策略表现相对更好。这说明 ReScene4D 的增益部分依赖于强预训练骨干的特征质量——在缺少合适预训练模型的场景下，方法的迁移性仍需验证。

### 时间度量设计的合理性验证

Figure 3 通过四个典型案例说明了 t-IoU 度量相较于标准 IoU 的必要性。当实例在不同阶段发生移动、变形或部分遮挡时，标准 IoU 可能因某一阶段的高重叠而给出虚高评分，而 t-IoU 取所有阶段的最小 IoU，强制要求跨时间的一致性覆盖。这一设计使 t-mAP 成为同时衡量分割质量与身份一致性的严格指标——Table 1 中所有方法的 t-mAP 均显著低于标准 mAP，印证了时间一致性是当前方法的普遍短板，而 ReScene4D 正是在这一短板上建立了最大优势。

![[assets/figures/papers/paper_list_l41_https_openaccess_thecvf_com_content_CVPR2026_html_Steiner_ReScene4D_Temp/figures/007_Table_4.jpg]]
*Table 4: Temporal Information Sharing Ablations. a) We study how different serialization patterns affect performance using the Concerto backbone: ⃝1 Spatial Only (3D) ⃝2 Temporal only (4D) where all serialization patterns traverse the 4D point cloud ⃝3 , Spatio-temporal (3D & 4D) where we randomly shuffle temporal and spatial patterns. b) We evaluate the impact of using positive and negative temporal pairs across temporal stages in contrastive loss. Training and inference on either 3DSIS or 4DSIS. For 4D, mAP is averaged across stages for direct comparison*

## 定位与知识库关联

### 任务定义与问题定位

ReScene4D 解决的是一个此前未被明确形式化的任务：**时间稀疏的4D语义实例分割（4DSIS）**。其输入为同一场景在不同时间阶段采集的 T 个独立 3D 扫描序列 $\mathcal{P} = \{P^{(1)}, ..., P^{(T)}\}$，输出为跨整个序列的 K 个时间一致实例掩码 $\bar{\mathcal{M}} = \{m^1, ..., m^K\}$。与 4D LiDAR 全景分割假设密集时序采样不同，4DSIS 面向室内场景中长间隔、大幅度的场景变化，观测之间的大部分变化是未被观察到的——这构成了方法设计的核心约束。

### 与现有方法的关系

#### 3D 语义实例分割 + 后匹配范式

最直接的基线是将单帧 3D 语义实例分割（3DSIS）方法独立应用于每个时间阶段，再通过后处理匹配跨阶段实例身份。**Mask3D+sem**（Schult et al., ICRA 2023）和 **Mask3D+geo**（Schult et al., ICRA 2023）分别采用语义特征匹配和几何最近邻匹配来关联跨时间实例。这类方法存在根本性缺陷：匹配步骤与分割步骤解耦，无法在分割过程中利用时间上下文；当实例发生大幅度移动或形变时，几何匹配失效，语义匹配也因缺乏跨时间特征对齐而不可靠。实验表明，Mask3D+geo 在 3RScan 上的 t-mAP 仅为 20.7（Table 1），远低于 ReScene4D 的 34.8。

#### 4D 全景分割方法的直接适配

**Mask4Former**（Yilmaz et al., ICRA 2024）和 **Mask4D**（Marcuzzi et al., IEEE RA-L 2023）是为室外自动驾驶场景的 4D LiDAR 全景分割设计的。这些方法依赖密集时序采样（通常 10Hz 以上）来建立帧间对应关系，假设相邻帧之间场景变化微小。当直接应用于室内 4DSIS 时，长间隔导致的稀疏观测使帧间对应假设不再成立。Mask4D 在 3RScan 上仅获得 1.3 t-mAP（Table 1），几乎完全失效，表明密集时序假设在此任务上不适用。

#### 关键差异：从“匹配”到“共享”

ReScene4D 的核心范式转变在于：**不再试图在独立预测之间建立匹配，而是通过跨时间的信息共享使模型直接输出时间一致的实例查询**。这一转变通过三个机制实现：

1. **输入表示**：将 T 个独立 3D 点云统一注册为时空 4D 点云 $\mathcal{P} \in \mathbb{R}^{N \times 4}$（含 x, y, z, t 坐标），使模型在单一表示中访问所有时间阶段的信息。
2. **查询机制**：实例查询跨时间阶段共享，查询解码器通过掩码交叉注意力同时从所有时间阶段的层次化特征中采样。
3. **位置编码**：将 3D Fourier 特征扩展为 4D Fourier 特征，显式编码时间维度。

这种设计使模型在分割过程中自然地保持身份一致性，而非事后修补。

### 适用边界与局限

#### 数据依赖

当前进展受限于 3RScan 数据集的规模和多样性。该数据集虽然提供了同一场景的多次扫描，但变化类型和幅度有限，缺乏大规模、高度动态的室内 4D 标注数据。时间信息共享模块的增益在现有数据规模下趋于饱和——消融实验（Table 3）显示，单独使用对比损失在刚性变化上提升显著（t-mREC 48.4 vs 基线 44.9），但组合所有模块后的总体 t-mAP 提升幅度暗示数据多样性可能是当前瓶颈。

#### 骨干网络依赖

ReScene4D 的性能与预训练 3D 骨干网络强相关。使用 Minkowski 骨干的 ReScene4D (M) 与使用 Concerto 预训练骨干的 ReScene4D (C) 之间存在显著性能差距（Table 1）。在缺少合适预训练模型的传感器配置或场景类型下，方法的迁移性未知。公平性比较中，Mask3D 的匹配策略在弱骨干上暂时表现更好，但 ReScene4D 的联合时空框架在更强骨干上整体最优——这表明方法增益部分依赖于骨干网络的特征质量。

#### 时间序列长度

当前评估默认使用 T=2 的时间阶段。t-mAP 随 T 增加而下降的趋势已被观察到（Section 5），但方法在更长时间序列（T >> 2）上的扩展性未经验证。时空对比损失的正负对数量随 T 二次增长，时空掩码的联合预测空间也线性扩展，计算开销可能成为瓶颈。

### 开放问题

1. **模块互补性机制**：消融实验（Table 3）揭示了一个值得深入研究的现象——ST-mask 和 ST-serialization 单独使用时会降低刚性变化的性能，但组合使用时却能互补提升。这种非线性的交互机制尚未被充分解释，可能涉及特征空间中时间信号与空间信号的竞争与协同。

2. **时间信号增益的饱和**：当前三个时间信息共享模块的组合已接近性能平台期。这种饱和是数据集的局限性导致（变化类型不够丰富），还是存在更根本的信息论上限？在更丰富的时序变化数据上，增益是否能继续扩展？

3. **长序列扩展**：如何将方法有效扩展到 T >> 2 并保持计算可控？可能的路径包括：层次化时间聚合、基于关键帧的稀疏时间采样、或引入时间注意力机制的稀疏化。

4. **极端变化的鲁棒性**：对于外观剧烈变化（如重新装修）或完全不可见的类别变化（如新增家具类型），当前的时空信息共享策略是否仍然鲁棒？对比损失依赖于语义特征的一致性，当实例外观发生根本改变时，正样本对的特征相似性可能不再成立。

5. **与 4D 基础模型的融合**：当前方法将 3D 骨干网络“升维”使用，未来是否可以直接利用 4D 预训练模型（如时空点云自监督学习）来提供更强的时间先验？这可能是突破当前性能瓶颈的方向之一。

## 原文 PDF

![[paperPDFs/CVPR_2026/ReScene4D_Temporally_Consistent_Semantic_Instance_Segmentation_of_Evolving_Indoor_3D_Scenes.pdf]]
