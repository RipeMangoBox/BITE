---
title: "HVG-3D: Bridging Real and Simulation Domains for 3D-Conditional Hand-Object Interaction Video Synthesis"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/HVG_3D_Bridging_Real_and_Simulation_Domains_for_3D_Conditional_Hand_Object_Interaction_Video_Synthesis.pdf
project_link: "https://hvg3d.github.io"
code_link: null
aliases:
- H3
- HVG-3D
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入显式三维条件信号（3D点云序列和跟踪序列），通过3D ControlNet将几何与运动线索直接注入扩散模型，将控制维度从2D提升到3D。
primary_logic: 利用3D ControlNet编码几何与运动线索，配合混合训练管道融合真实与仿真数据，实现三维条件驱动的高保真、物理一致的手物交互视频生成。
claims:
- HVG-3D在全帧和手物掩码区域均取得最佳的FVD分数，显著优于现有基线。
- 消融实验表明，去除3D点云条件后PSNR从24.15降至18.44，证明3D条件对交互质量的因果作用。
- 混合训练管道使得模型可接受来自仿真器或真实视频的3D条件，实现了真实与仿真域的桥接。
- TASTE-Rob (Single Hand subset) 上 FVD (Full Frame) = 13.8
---

# HVG-3D: Bridging Real and Simulation Domains for 3D-Conditional Hand-Object Interaction Video Synthesis

> [!tip] 核心洞察
> 利用3D ControlNet编码几何与运动线索，配合混合训练管道融合真实与仿真数据，实现三维条件驱动的高保真、物理一致的手物交互视频生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | HVG-3D：连接真实与仿真域的三维条件手物交互视频生成 |
| 英文题名 | HVG-3D: Bridging Real and Simulation Domains for 3D-Conditional Hand-Object Interaction Video Synthesis |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.03305) · [Project](https://hvg3d.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | HVG-3D |
| Dataset | TASTE-Rob |

> [!tip] 效果简介
> - TASTE-Rob (Single Hand subset) 上，FVD (Full Frame) 13.8；FID (Full Frame) 58.2；CLIP Score (Full Frame) 0.96。

## 概要

手物交互（Hand-Object Interaction, HOI）视频生成是具身智能与视觉内容合成的关键交叉问题。现有方法普遍依赖二维控制信号（如点轨迹、光流、边界框等），缺乏对三维空间几何与运动线索的直接建模能力，导致生成视频中手物交互不真实、几何变形频繁，且难以利用合成三维数据降低采集成本。**HVG-3D** 针对这一瓶颈，提出将控制维度从二维提升至三维：引入显式的三维点云序列与三维跟踪序列作为条件信号，通过一个可训练的三维 ControlNet 将几何与运动线索注入冻结的图像到视频扩散骨干网络，实现三维条件驱动的高保真、物理一致的手物交互视频生成。

该方法的核心洞察在于：三维点云与跟踪序列提供了紧凑且信息丰富的几何-运动表征，使扩散模型能够作为“神经渲染器”直接推理手物交互的空间关系，而非仅依赖二维外观线索。配合混合训练管道——从真实第一人称视频中自动提取三维条件，并与仿真数据联合训练——HVG-3D 桥接了真实域与仿真域，使模型既可接受来自仿真器的精确三维输入，也可接受从真实视频重建的近似三维输入。

在 TASTE-Rob 数据集的单手子集上，HVG-3D 在全帧与手物掩码区域均取得最优的 FVD 分数，显著优于 CogVideoX、Wan 2.2、Kling 等通用视频生成基线。消融实验进一步验证了三维条件的关键因果作用：去除三维点云条件后，PSNR 从 24.15 骤降至 18.44；去除掩码加权扩散损失后，PSNR 降至 22.09。这些结果表明，显式三维条件与交互区域聚焦训练是提升手物交互生成质量的决定性因素。

目前该方法仍限于固定 49 帧的生成，长序列合成能力与跨场景泛化性有待进一步验证，且尚未与机器人操作策略形成闭环集成。

手物交互（Hand-Object Interaction, HOI）视频生成是计算机视觉与机器人领域的关键技术，其核心目标是根据给定的控制信号合成真实且时序连贯的交互视频。这项技术对于机器人操作策略学习、增强现实以及人类行为模拟等下游任务具有重要价值。然而，当前该领域面临一个核心瓶颈：**现有方法普遍依赖2D控制信号，缺乏空间表达能力，难以充分利用合成3D数据，导致手物交互不真实、几何变形频繁，且数据收集成本高昂**。

具体而言，当前主流的手物交互视频生成方法——包括通用视频生成模型如 **CogVideoX**、**Wan 2.2**、**Kling**，以及专用交互生成方法如 **DaS**、**InterDyn**——均采用2D控制信号作为条件输入，例如点轨迹、光流、边界框或分割掩码。这些2D信号虽然易于从真实视频中提取，但存在根本性的维度缺陷：它们无法完整表达三维空间中手与物体的几何结构与运动关系。这导致生成结果中频繁出现手部穿透物体、物体形状畸变、交互动作不符合物理约束等问题。此外，2D条件信号的提取精度受限于视角遮挡和深度缺失，使得模型难以从合成仿真数据中获益，而仿真数据恰恰是缓解真实数据稀缺和高标注成本的关键途径。

这一瓶颈的因果根源在于**控制信号维度与交互本质维度之间的不匹配**。手物交互本质上是三维空间中的物理过程，涉及手部姿态、物体几何和相对运动的精确协调。2D控制信号将这一三维过程投影到图像平面，不可避免地丢失了深度信息和遮挡关系，使得扩散模型在生成过程中缺乏对三维几何的显式推理能力。因此，尽管现有方法在通用视频生成任务上取得了显著进展，但在手物交互这一特定场景下，其空间保真度和时序一致性仍然远远不足。

针对上述问题，**HVG-3D** 提出了一个根本性的思路转变：**将控制信号的维度从2D提升到3D**。该工作的核心洞察是，通过引入显式的三维条件信号——具体为3D点云序列和3D跟踪序列——并设计专门的3D ControlNet将这些几何与运动线索直接注入扩散模型，可以使模型具备显式的三维空间推理能力。这一设计不仅能够从根本上改善交互生成的几何准确性，更重要的是，它架起了一座连接真实域与仿真域的桥梁：模型可以接受来自真实视频提取的3D条件，也可以接受来自仿真器的合成3D条件，从而实现了数据来源的统一和互补。这种桥接能力使得HVG-3D能够充分利用仿真数据中精确、廉价的3D标注，同时保持对真实场景的泛化能力，为解决手物交互视频生成中的数据稀缺和几何变形难题提供了新的范式。

## 核心方法与创新机理

HVG-3D 的核心创新在于将手物交互视频生成的控制维度从二维提升到三维，通过显式的几何与运动条件信号驱动扩散模型，从根本上解决了现有方法中交互不真实和几何变形的问题。

### 从 2D 到 3D 的条件维度跃迁

现有手物交互视频生成方法普遍依赖二维控制信号，如点轨迹、光流、边界框或掩码，这些信号缺乏空间表达能力，难以精确约束手与物体的三维几何关系。HVG-3D 的关键突破在于直接引入三维条件信号——**3D 点云序列** $P \in \mathbb{R}^{T \times N \times 3}$ 和**3D 跟踪序列** $\tau = \{ T_{t} \}_{t=1}^{T}$，将控制维度从 2D 提升到 3D。这一改变使得扩散模型能够显式地推理手物交互的空间结构，而非仅依赖二维投影的模糊线索。

### 3D ControlNet：几何与运动线索的编码与注入

为实现三维条件信号的有效利用，HVG-3D 引入了一个**3D ControlNet**模块。该模块通过复制基础扩散模型（CogVideoX-5B-I2V）的 DiT 块构建，专门负责处理 3D 条件信号。具体而言，3D 点云序列首先经过 3D 点云编码器（3DShape2VecSet）编码为潜在特征，随后与 3D 跟踪序列一同输入 3D ControlNet，经零初始化卷积层注入冻结的扩散骨干网络。这种设计既保留了预训练模型的时空建模能力，又赋予其显式的三维推理能力。

### 掩码加权扩散损失：聚焦交互区域

标准扩散损失对全帧像素均等对待，但在手物交互场景中，背景区域往往占据大量像素却对交互质量贡献甚微。HVG-3D 提出**掩码加权的扩散损失**：

$$L = \sum_{i=1}^{n} \mathbb{E}_{\varepsilon} \left( \left| \left( Z_{gt} - Z_{\varepsilon} \right) \odot \left( 1 + M^{i} \right) \right|^{2} \right)$$

其中 $M^{i}$ 为手物交互区域的二值掩码。该损失函数通过 $(1 + M^{i})$ 的加权机制，在训练时强制模型优先关注手物交互区域的重建精度，抑制背景干扰。消融实验证实，去除该损失后 PSNR 从 24.15 降至 22.09（Table 3），验证了其对交互质量的关键作用。

### 混合训练管道：桥接真实与仿真域

HVG-3D 的另一重要创新在于其**混合训练数据构建管道**。该管道能够从真实视频中利用 YOLOv8、SAMURAI、VGGT 和 SpatialTracker 等工具自动提取 2D/3D 线索，构建配对的输入图像、3D 跟踪视频和 3D 点云序列；同时也能直接接受来自仿真器或现成 3D 数据集的合成条件。这一设计使得模型在训练和推理阶段均可灵活接受来自真实域或仿真域的 3D 条件，实现了两域之间的桥接，大幅降低了数据收集成本并拓展了应用场景。

### 与基线的关键差异总结

| 变化维度 | 基线方法 | HVG-3D |
|---------|---------|--------|
| 条件类型 | 2D 控制信号（点轨迹、光流、边界框等） | 3D 点云序列 + 3D 跟踪序列 |
| 条件注入方式 | 无专用 3D 控制模块 | 复制 DiT 块的 3D ControlNet，经零初始化卷积注入 |
| 损失函数 | 标准扩散损失 | 掩码加权扩散损失，强调手物交互区域 |

这些创新点的因果作用在消融实验中得到了明确验证：去除 3D 点云条件后 PSNR 从 24.15 骤降至 18.44，去除 3D 跟踪视频后降至 22.76（Table 3），证明三维几何与运动线索是生成高质量手物交互视频的核心驱动力。

HVG-3D 是一个统一的**三维条件手物交互视频合成框架**，其核心设计在于将控制维度从传统的2D信号提升到显式3D几何与运动表示，从而桥接真实域与仿真域的数据鸿沟。整个框架由两大组件构成：(i) 一个3D感知的扩散生成架构，(ii) 一个混合数据构建管道，用于从真实视频和仿真数据中提取并构建输入图像与3D条件信号（Figure 2）。

![[assets/figures/papers/paper_list_l2521_https_arxiv_org_abs_2604_03305/figures/002_Figure_2.jpg]]
*Figure 2: Architecture of HVG-3D. The left panel illustrates the hybrid training and inference pipeline, where egocentric driving videos, simulator outputs, and 3D HOI datasets are processed by grounded segmentation, key bounding-box extraction and a point-cloud scanner to construct paired input images, 3D tracking videos, and 3D point cloud sequences. The right panel depicts the 3D-aware HOI video generation diffusion architecture, in which the 3D point cloud and tracking signals are encoded by a trainable 3D ControlNet and injected into a frozen image-to-video diffusion backbone via zero-initialized layers, enabling the synthesis of temporally coherent videos that respect the underlying 3D hand–obj...*

### 输入输出规范

框架接受三类输入：

- **输入图像** $I_{0} \in \mathbb{R}^{H \times W \times 3}$：单张真实RGB图像，作为视频合成的外观条件锚点。
- **3D点云序列** $P \in \mathbb{R}^{T \times N \times 3}$：$T$帧的手物几何点云，提供显式的三维结构条件。
- **3D跟踪序列** $\tau = \{ T_{t} \}_{t=1}^{T}$（可选）：提供逐帧的运动线索，增强时序一致性。

输出为与输入图像外观一致、且严格遵循3D条件约束的高保真手物交互视频 $V \in \mathbb{R}^{T \times H \times W \times 3}$。

### 生成架构

生成骨干网络采用冻结的**CogVideoX-5B-I2V**图像到视频扩散模型，以充分利用其预训练的时空建模能力。在此之上，引入一个**3D ControlNet**——通过复制DiT（Diffusion Transformer）块构建的可训练分支，专门处理3D条件信号：

1. **3D点云编码**：使用**3DShape2VecSet**编码器将3D点云序列 $P$ 压缩为潜在特征表示。
2. **条件注入**：编码后的3D几何与运动特征通过**零初始化卷积层**注入冻结的扩散骨干网络，确保训练初期不破坏预训练权重，逐步学习3D条件到视频生成的映射。

这一设计使得扩散模型能够作为“神经渲染器”，在3D几何与运动线索的显式引导下进行视频合成，从根本上解决了2D控制信号（如点轨迹、光流）空间表达能力不足的瓶颈。

### 混合训练管道

为了桥接真实与仿真域，框架构建了一个**混合训练数据管道**（Figure 2左半部分）：

- **真实视频路径**：从第一人称驾驶视频出发，依次通过**YOLOv8**进行目标检测、**SAMURAI**进行精细分割、**VGGT**估计深度与相机位姿、**SpatialTracker**提取3D轨迹，最终将2D视频转化为配对的输入图像与3D条件信号。
- **仿真数据路径**：直接从仿真器或现有3D手物交互数据集中获取3D点云序列与跟踪信号，无需复杂的2D到3D提升过程。
- **融合训练**：两条路径的数据共同送入生成架构，使模型既能在真实场景下泛化，又能充分利用仿真数据的精确3D标注。

### 训练目标

训练采用**掩码加权扩散损失**，公式为：

$$L = \sum_{i=1}^{n} \mathbb{E}_{\varepsilon} \left( \left| \left( Z_{gt} - Z_{\varepsilon} \right) \odot \left( 1 + M^{i} \right) \right|^{2} \right)$$

其中 $Z_{gt}$ 为真实视频的潜在表示，$Z_{\varepsilon}$ 为去噪预测，$M^{i}$ 为手物交互区域的二值掩码。通过 $(1 + M^{i})$ 的加权机制，损失函数对手物区域施加更高的重建精度要求，同时抑制背景区域的干扰，引导模型聚焦于交互过程的学习。

训练使用**AdamW**优化器，学习率 $1 \times 10^{-4}$，在8张H20 GPU上训练20个epoch。

### 3.1 问题形式化与条件信号

HVG-3D 将手物交互视频生成形式化为三维条件驱动的图像到视频（I2V）扩散任务。给定单张真实图像 $I_{0} \in \mathbb{R}^{H \times W \times 3}$ 作为外观条件，模型需合成一段 $T$ 帧的视频序列 $V_{gt} \in \mathbb{R}^{T \times H \times W \times 3}$。区别于现有方法依赖 2D 控制信号（点轨迹、光流、边界框等），HVG-3D 引入两类显式三维条件：

- **3D 点云序列** $P \in \mathbb{R}^{T \times N \times 3}$：$T$ 帧的手物几何点云，每帧包含 $N$ 个三维点，提供空间结构约束。
- **3D 跟踪序列** $\tau = \{ T_{t} \}_{t=1}^{T}$：可选的三维运动线索，编码手物关键点的时空轨迹。

这两类信号共同构成三维几何与运动先验，使扩散模型能够显式推理手物交互的空间关系，而非仅依赖 2D 像素级统计。

### 3.2 3D ControlNet 条件注入架构

HVG-3D 以 **CogVideoX-5B-I2V** 作为冻结的图像到视频扩散骨干网络，在其上附加一个可训练的 3D ControlNet 以注入三维条件信号。该 ControlNet 的设计要点如下：

1. **结构复制**：3D ControlNet 复制了 CogVideoX 骨干中 DiT（Diffusion Transformer）块的网络结构，确保条件特征与骨干特征在维度上对齐。
2. **3D 点云编码**：引入 **3DShape2VecSet** 作为点云编码器，将原始 3D 点云序列 $P$ 映射为潜在特征表示，再送入 3D ControlNet 进行处理。
3. **零初始化注入**：ControlNet 的输出通过零初始化卷积层逐层注入冻结骨干网络的对应 DiT 块。零初始化确保训练初期条件分支的输出为零，模型从无条件生成平稳起步，逐步学习利用 3D 几何与运动线索。
4. **双条件融合**：3D 点云序列和 3D 跟踪序列经编码后共同输入 ControlNet，使模型同时感知空间结构与运动趋势。

这一设计的核心优势在于：冻结骨干保留了 CogVideoX 强大的时空先验，而可训练的 3D ControlNet 仅需学习如何将三维几何信息“翻译”为骨干可理解的调制信号，训练效率高且不易破坏预训练质量。

### 3.3 掩码加权扩散损失

手物交互视频中，交互区域（手部与物体）的几何精度远重要于背景区域。标准扩散损失对所有像素一视同仁，导致模型在背景上浪费容量，而交互区域的重建精度不足。为此，HVG-3D 采用掩码加权的扩散损失：

$$L = \sum_{i=1}^{n} \mathbb{E}_{\varepsilon} \left( \left| \left( Z_{gt} - Z_{\varepsilon} \right) \odot \left( 1 + M^{i} \right) \right|^{2} \right)$$

其中各变量含义如下：

- $Z_{gt}$：真实视频帧的潜在表示。
- $Z_{\varepsilon}$：扩散模型预测的去噪潜在表示。
- $M^{i}$：第 $i$ 帧的手物交互区域二值掩码（手部与物体像素为 1，背景为 0）。
- $\odot$：逐元素乘法。
- $n$：视频帧数。

该损失通过 $(1 + M^{i})$ 因子对交互区域施加 2 倍权重，迫使模型将优化重点放在手物几何的重建精度上。消融实验（Table 3）证实，去除掩码加权损失后 PSNR 从 24.15 降至 22.09，验证了该设计对交互质量的因果作用。

### 3.4 混合训练管道

为桥接真实域与仿真域，HVG-3D 构建了混合训练数据管道（Fig. 2 左半部分），从三类数据源提取统一的 3D 条件信号：

1. **真实自拍视频**：利用 **YOLOv8** 进行手物接地分割，**SAMURAI** 提取精细掩码，**VGGT** 重建三维几何，**SpatialTracker** 估计 3D 跟踪轨迹。
2. **仿真器输出**：直接从物理仿真环境获取精确的 3D 点云和跟踪序列。
3. **现有 3D HOI 数据集**：复用已标注的三维手物交互数据。

所有数据源经统一预处理后，生成配对的 $I_{0}$、$P$ 和 $\tau$，送入 3D ControlNet 增强的扩散骨干进行端到端训练。训练采用 AdamW 优化器，学习率 $1 \times 10^{-4}$，在 8 块 H20 GPU 上训练 20 个 epoch。这一管道使模型在推理时既可接受仿真器提供的精确 3D 条件，也可接受从真实视频估计的带噪 3D 条件，实现了域间桥接。

## 实验与关键发现

### 主实验结果

HVG-3D 在 TASTE-Rob 数据集的 Single Hand 子集上与多个主流视频生成基线进行了定量对比，包括通用模型 **CogVideoX**、**Wan 2.2**、**Kling**，以及手物交互专用方法 **DaS** 和 **InterDyn**。所有方法在相同的 100 个随机选取视频上评估，采用统一的图像质量和时空相似性指标，确保公平性。

**全帧评估**（Table 1）显示，HVG-3D 在视频生成的核心指标上取得最优性能。FVD 降至 13.8，FID 降至 58.2，CLIP Score 达到 0.96，GMSD-T 为 0.40。FVD 的大幅领先表明生成视频在时序连贯性上显著优于基线；FID 的改善则反映了整体视觉质量的提升。

**手物掩码区域评估**（Table 2）聚焦于交互核心区域，HVG-3D 的优势更为突出。手物掩码区域的 FVD 为 88.5，C-FID 为 13.1。这一结果表明，3D 条件信号对交互区域的几何保真度和运动准确性具有关键作用，而纯 2D 条件方法在该区域容易出现几何变形和运动不真实的问题。

**定性对比**（Figure 3）进一步印证了定量结论。通用视频生成模型在手物交互场景中频繁出现手部几何变形、物体漂移和交互动作不准确等问题，而 HVG-3D 生成的视频保持了手部和物体的几何完整性，交互动作高度准确且视觉质量优越。

### FVD 指标对比

Figure 4 以可视化方式呈现了各方法在全帧和手物掩码区域的 FVD 分布。HVG-3D 在两个设置下均取得最佳 FVD 分数，且与其他方法的差距显著。FVD 作为衡量生成视频与真实视频时序分布差异的指标，其大幅领先直接证明了 3D 条件对时序一致性的因果贡献。

![[assets/figures/papers/paper_list_l2521_https_arxiv_org_abs_2604_03305/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative comparison between HVG-3D and baselines on FVD. Our method achieves the best FVD scores in both the full-frame setting and the hand–object masked region*

### 消融实验

为验证各组件的因果作用，Table 3 报告了三项关键消融实验的 PSNR 结果：

![[assets/figures/papers/paper_list_l2521_https_arxiv_org_abs_2604_03305/figures/007_Table_3.jpg]]
*Table 3: Ablation Studies on 3D point cloud, 3D tracking video and mask diffusion loss. The experimental results demonstrate that these techniques enhance the quality of hand–object interaction video generation, improve the accuracy of the synthesized interaction process, and accelerate convergence during training*

- **去除 3D 点云条件**：PSNR 从完整模型的 24.15 骤降至 18.44，降幅达 23.6%。这是所有消融中性能退化最严重的一项，直接证明了 3D 点云提供的几何结构信息对手物交互质量的不可替代性。
- **去除 3D 跟踪视频**：PSNR 降至 22.76，表明运动线索对时序一致性有辅助作用，但影响程度小于点云条件。
- **去除掩码扩散损失**：PSNR 降至 22.09，说明在训练中强调手物交互区域有助于模型聚焦于关键区域的生成精度，抑制背景干扰对损失函数的稀释效应。

消融实验的结论与论文的核心因果论断一致：3D 点云条件是决定交互质量的主导因素，3D 跟踪信号和掩码损失提供增量改进，三者协同作用实现了最优性能。

### 失败模式与局限性

根据论文明确指出的局限性和实验观察，当前方法存在以下已知边界：

1. **固定帧长限制**：模型仅支持生成 49 帧的视频序列，对于需要更长时序上下文的交互场景（如完整操作过程）无法直接应用。
2. **场景泛化性未验证**：训练和评估均局限于 TASTE-Rob 数据集的特定场景子集（office、dining、bedroom、kitchen、dressing table），对未见场景、新物体类别和不同光照条件的泛化能力有待检验。该结论需要读者在自身应用场景中手动验证。
3. **3D 条件质量依赖**：混合训练管道依赖 VGGT 和 SpatialTracker 等工具从真实视频中提取 3D 线索，这些工具的估计误差对生成质量的影响边界尚未量化分析。在实际部署中，低质量 3D 条件可能导致交互精度下降，但目前缺少系统的鲁棒性实验。
4. **闭环应用缺失**：尚未实现与机器人操作策略的闭环集成，生成视频在实际机器人任务中的效用有待验证。

![[assets/figures/papers/paper_list_l2521_https_arxiv_org_abs_2604_03305/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison between HVG-3D and baselines on Full Frame evaluation metrics. Most video generation metrics demonstrate that HVG-3D achieves superior performance*

![[assets/figures/papers/paper_list_l2521_https_arxiv_org_abs_2604_03305/figures/004_Table_2.jpg]]
*Table 2: Quantitative comparison between HVG-3D and baselines on Hand Object Masked Region evaluation metrics. All video generation metrics consistently indicate that HVG-3D delivers superior performance*

![[assets/figures/papers/paper_list_l2521_https_arxiv_org_abs_2604_03305/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative comparison of video generation performance. HVG-3D is capable of generating videos with highly accurate motions and superior visual quality, while further ensuring that both the hand and the object remain free from geometric deformation. A level of performance that current state-of-the-art general-purpose video generation models are unable to achieve*

## 定位与知识库关联

### 与现有基线的对比定位

HVG-3D 的核心差异在于将手物交互视频生成的控制维度从 2D 提升到 3D。现有方法普遍依赖二维控制信号——点轨迹、光流、边界框或掩码——这些信号缺乏空间表达力，难以捕捉手物交互中复杂的遮挡与几何关系。HVG-3D 通过引入显式的三维条件信号（3D 点云序列 $P \in \mathbb{R}^{T \times N \times 3}$ 与 3D 跟踪序列 $\tau = \{ T_{t} \}_{t=1}^{T}$），使扩散模型能够直接推理三维几何与运动，从而从根本上改变了条件注入的语义层级。

在具体基线对比中：

- **通用视频生成模型**（**CogVideoX**、**Wan 2.2**、**Kling**）：这些模型具备强大的图像到视频生成能力，但缺乏专用的手物交互空间推理机制。定性结果（Figure 3）表明，它们在生成手物交互视频时频繁出现几何变形和交互不真实的问题，而 HVG-3D 通过 3D ControlNet 注入几何线索，使手和物体均保持几何完整性。

- **专用手物交互方法**（**DaS**、**InterDyn**）：这些方法针对交互场景设计，但仍停留在 2D 条件层面。HVG-3D 在 TASTE-Rob 数据集上取得了显著更优的 FVD（全帧 13.8，掩码区域 88.5）和 FID（全帧 58.2），证明 3D 条件带来的空间推理能力提升是 2D 方法难以弥合的。

### 方法谱系中的关键创新锚点

HVG-3D 的方法设计可定位为三个关键创新锚点：

1. **3D ControlNet 条件注入**：不同于标准 ControlNet 处理 2D 条件（如边缘图、深度图），HVG-3D 复制了 CogVideoX-5B-I2V 的 DiT 块构建 3D ControlNet，通过零初始化卷积将 3D 点云编码器（3DShape2VecSet）输出的几何特征注入冻结的扩散骨干网络。这一设计使模型可以接受来自不同源的 3D 条件，而无需修改骨干网络。

2. **掩码加权扩散损失**：训练目标 $L = \sum_{i=1}^{n} \mathbb{E}_{\varepsilon} \left( \left| \left( Z_{gt} - Z_{\varepsilon} \right) \odot \left( 1 + M^{i} \right) \right|^{2} \right)$ 通过手物掩码 $M^{i}$ 强调交互区域的重建精度，抑制背景干扰。消融实验（Table 3）表明，去除该损失后 PSNR 从 24.15 降至 22.09，验证了其对交互质量的因果作用。

3. **混合训练管道**：通过 YOLOv8 进行接地分割、SAMURAI 提取关键边界框、VGGT 与 SpatialTracker 估计 3D 点云和跟踪序列，使模型可同时利用真实视频和仿真数据训练。这一管道桥接了真实域与仿真域，使得 HVG-3D 既能从真实视频中学习外观分布，又能利用仿真数据获得精确的 3D 标注。

### 适用边界与局限

尽管 HVG-3D 在 TASTE-Rob 数据集上展示了优异性能，其适用边界存在以下约束：

- **帧长度固定**：目前仅支持 49 帧的视频生成，长序列合成能力未经验证。对于需要长时间交互建模的场景（如完整操作流程），模型需要架构扩展。
- **场景泛化性有限**：训练和评估均基于 TASTE-Rob 的特定场景子集（办公室、餐厅、卧室、厨房、梳妆台），对其他手物交互场景（如工业操作、户外活动）的泛化性能有待检验。
- **3D 条件精度依赖**：3D 条件信号的重建依赖 VGGT 和 SpatialTracker 等估计器的精度，这些模块的误差传播对生成质量的影响边界尚未量化分析。
- **闭环集成缺失**：目前 HVG-3D 作为独立的视频生成器运行，尚未与机器人操作策略形成闭环。将生成模型直接服务于下游操作任务（如策略训练的数据增强），需要进一步的系统集成工作。

### 开放问题

1. **场景与序列扩展**：如何将 3D 条件视频生成扩展到更多样化的交互场景和更长的视频序列？这可能需要引入层次化的 3D 表示或渐进式生成策略。

2. **闭环机器人集成**：如何将 HVG-3D 与机器人操作策略形成闭环，使生成的视频直接服务于策略学习或仿真到现实的迁移？这涉及生成质量与策略性能之间的因果关系验证。

3. **3D 条件的鲁棒性边界**：3D 点云和跟踪序列的估计误差在何种精度范围内不会显著损害生成质量？这需要系统性的扰动实验来确定条件信号的容错边界。

4. **多模态条件融合**：当前方法将 3D 点云和跟踪序列作为独立条件注入，是否存在更有效的多模态 3D 表示（如神经辐射场、3D 高斯泼溅）能进一步提升生成质量？

## 原文 PDF

![[paperPDFs/CVPR_2026/HVG_3D_Bridging_Real_and_Simulation_Domains_for_3D_Conditional_Hand_Object_Interaction_Video_Synthesis.pdf]]
