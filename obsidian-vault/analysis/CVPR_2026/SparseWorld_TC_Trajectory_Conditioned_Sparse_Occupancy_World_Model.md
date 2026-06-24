---
title: "SparseWorld-TC: Trajectory-Conditioned Sparse Occupancy World Model"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SparseWorld_TC_Trajectory_Conditioned_Sparse_Occupancy_World_Model.pdf
project_link: null
code_link: "https://github.com/MrPicklesGG/SparseWorld"
aliases:
- ST
- SparseWorld-TC
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 轨迹条件信号与稀疏锚点注意力融合机制，将未来轨迹作为时空嵌入直接注入Transformer，引导场景按照给定轨迹演化。
primary_logic: 纯注意力Transformer架构利用稀疏3D锚点（随机点集）直接从多视图图像特征中端到端学习未来场景占用，无需离散token或BEV投影，并通过轨迹嵌入实现灵活的条件预测。
claims:
- 在Occ3D-nuScenes基准上，SparseWorld-TC-Large以相机输入获得平均语义mIoU 26.42%（几何IoU 49.21%），比先前最佳相机方法COME分别提高18.7%和11.7%。
- 在长达8秒的长期预测中，SparseWorld-TC-Large以相机输入获得平均语义mIoU 22.33%和几何IoU 45.35%，远超使用地面真值占用的DOME和COME，表明模型在长时预测中性能衰减极小。
- Occ3D-nuScenes (1-3s) 上 Semantic mIoU Avg.（%） = 26.42
- Occ3D-nuScenes (1-3s) 上 Geometric IoU Avg.（%） = 49.21
---

# SparseWorld-TC: Trajectory-Conditioned Sparse Occupancy World Model

> [!tip] 核心洞察
> 纯注意力Transformer架构利用稀疏3D锚点（随机点集）直接从多视图图像特征中端到端学习未来场景占用，无需离散token或BEV投影，并通过轨迹嵌入实现灵活的条件预测。

| 字段 | 内容 |
|------|------|
| 中文题名 | 轨迹条件稀疏占用世界模型 |
| 英文题名 | SparseWorld-TC: Trajectory-Conditioned Sparse Occupancy World Model |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.22039) · [Code](https://github.com/MrPicklesGG/SparseWorld) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SparseWorld-TC |
| Dataset | Occ3D-nuScenes, Occ3D-nuScenes（长期 1-8s） |

> [!tip] 效果简介
> - Occ3D-nuScenes (1-3s) 上，Semantic mIoU Avg.（%） 26.42 vs 22.26（COME） (+4.16（+18.7%）)；Geometric IoU Avg.（%） 49.21 vs 44.07（COME） (+5.14（+11.7%）)。
> - Occ3D-nuScenes（长期 1-8s） 上，Semantic mIoU Avg.（%） 22.33 vs 19.07（COME, Occ GT） (+3.26（+17.1%）)；Geometric IoU Avg.（%） 45.35 vs 29.96（COME, Occ GT） (+15.39（+51.4%）)。

## 概述

4D占用预测（4D occupancy forecasting）旨在从历史传感器观测中推断未来三维场景的几何与语义演变，是自动驾驶世界模型的核心能力之一。现有方法普遍依赖**VAE离散token化**或**BEV几何先验**来压缩占用表示，再通过自回归或扩散模型生成未来帧。这种设计虽然简化了时序建模，但限制了表示容量和时空特征交互，导致**长程预测性能衰减严重**——尤其是在纯相机输入条件下，几何与语义精度随预测时长增加急剧下降。

**SparseWorld-TC** 针对上述瓶颈提出了一个根本性的架构转变：完全摒弃离散token和BEV投影，转而采用**稀疏锚点表示**与**纯注意力Transformer**的端到端范式。其核心思想是将场景占用建模为一组可学习的3D锚点（随机点集+特征向量），通过帧级交叉注意力和时间自注意力直接从多视图图像特征中演化未来占用，并将**未来轨迹作为显式时空嵌入**注入网络，引导场景沿给定轨迹条件演化。这一设计形成了“轨迹条件信号→稀疏锚点注意力融合→端到端占用预测”的因果链路。

在**Occ3D-nuScenes基准**上，SparseWorld-TC-Large以纯相机输入取得平均语义mIoU **26.42%**、几何IoU **49.21%**，分别比先前最佳相机方法COME提升18.7%和11.7%。更关键的是，在长达**8秒的长期预测**中，该方法仍保持mIoU 22.33%和IoU 45.35%，几何IoU较使用地面真值占用的COME高出51.4%，表明其**长程预测性能衰减极小**。消融实验进一步证实，轨迹条件嵌入和随机集成训练策略是长程鲁棒性的关键因素。

从方法谱系看，SparseWorld-TC属于**稀疏查询+注意力融合**的占用世界模型分支，与基于VAE token的OccWorld（Zheng et al., ECCV 2024）、基于BEV的COME等形成鲜明对比。其稀疏锚点机制与3D视觉中的可变形注意力、点云学习中的集合预测方法存在概念关联，但通过将轨迹条件显式注入时空注意力，开辟了条件世界建模的新路径。

## 背景与动机

### 4D占用预测：从静态重建到世界模型

自动驾驶系统对环境的理解正从单帧3D占用感知向**4D占用预测**（4D occupancy forecasting）延伸——不仅重建当前场景的几何与语义，还需预测未来数秒内场景如何演化。这一能力构成了**世界模型**（world model）的核心，使自车能够预判动态障碍物轨迹、静态基础设施变化，从而支撑下游的运动规划与决策。

现有工作大致分为两类。一类以**OccWorld**（Zheng et al., ECCV 2024）为代表，将3D占用压缩为离散VAE token，再通过自回归Transformer预测未来token序列。另一类如**COME**、**RenderWorld**、**OccLLaMA**等方法，依赖BEV（Bird's-Eye-View）投影或扩散生成范式，在密集网格上建模时空关系。尽管这些方法推动了4D占用预测的进展，但它们共享两个结构性瓶颈：

1. **表示容量受限**：离散VAE token化将连续3D几何压缩为有限码本，不可避免地引入量化误差，尤其对细粒度几何（如行人、路障）的表达能力不足。BEV投影则将3D信息坍缩到2D平面，损失了高度维度的精细结构。
2. **时空交互薄弱**：基于BEV的时空建模通常将历史BEV特征拼接或做简单时序融合，难以捕捉跨帧的长程依赖。自回归生成范式则面临误差累积问题，导致预测步长增加时性能急剧衰减。

### 核心瓶颈：长程预测的性能衰减

上述方法在短时预测（1–3秒）上尚可维持合理精度，但一旦扩展到长程预测（如6–8秒），性能下降显著。以Occ3D-nuScenes基准为例，使用地面真值占用作为输入的**COME**在1–3秒平均几何IoU为44.07%，但在1–8秒长期预测中骤降至29.96%，衰减幅度超过30%。这一现象的根本原因在于：**现有架构缺乏有效机制将未来自车运动信息显式注入场景演化过程**，模型只能从历史观测中隐式推断未来，随着时间跨度增加，不确定性迅速放大。

### 本文动机：稀疏表示 + 轨迹条件 + 全注意力架构

针对上述瓶颈，**SparseWorld-TC** 提出三条核心设计原则：

- **稀疏锚点表示**：摒弃离散token和密集BEV网格，将场景占用建模为一组可学习的3D锚点（anchor），每个锚点由一组3D查询点及其关联特征向量构成。这种稀疏表示天然适配3D场景的非均匀信息密度，且避免了量化误差。
- **轨迹条件注入**：将未来自车轨迹作为显式时空嵌入，直接注入Transformer的注意力层，引导场景按照给定轨迹演化。这使模型从“盲预测”转变为“条件预测”，显著降低了长程预测的不确定性。
- **纯注意力前馈架构**：采用帧级交叉注意力与时间自注意力堆叠的Transformer，直接从多视图图像特征中端到端学习时空关系，无需BEV投影或自回归生成，从而缓解误差累积。

在Occ3D-nuScenes基准上，SparseWorld-TC-Large以相机输入获得1–3秒平均语义mIoU 26.42%（几何IoU 49.21%），比先前最佳相机方法COME分别提升18.7%和11.7%；在1–8秒长期预测中，语义mIoU 22.33%和几何IoU 45.35%的成绩远超使用地面真值占用的COME（分别提升17.1%和51.4%），证明该架构在长程预测中的性能衰减极小。

## 核心创新

SparseWorld-TC 的核心创新在于用**纯注意力 Transformer + 稀疏锚点**彻底重构了 4D 占用世界模型的表示与交互范式，并引入**轨迹条件机制**实现可控的未来场景演化。

### 1. 稀疏锚点表示：摆脱离散 token 与 BEV 投影

现有方法（如 **OccWorld**，Zheng et al., ECCV 2024）普遍依赖 VAE 离散 token 化或密集 BEV 网格来表示场景占用，这限制了表示容量，并在长程预测中引入累积误差。SparseWorld-TC 提出了一种全新的稀疏占用表示：

- 将场景占用建模为 $N$ 个**锚点**的集合 $\mathcal{M} = \{ A_i \}_{i=1}^N$，每个锚点 $A_i$ 由一组 3D 查询点 $P_i$ 和一个关联的特征向量 $\mathbf{f}_i$ 构成（Equation 1）。
- 这些 3D 点初始为随机采样，通过可变形注意力从多视图图像特征中提取传感器证据，再由两个 MLP 解码头预测每个点的偏移量和语义类别，从而将随机点“去噪”为一致的占用场（Figure 2）。

**因果机制**：稀疏锚点直接以端到端方式从原始图像特征中学习，无需离散 codebook 的量化损失，也无需 BEV 投影带来的几何先验约束，从根本上提升了表示灵活性和信息保真度。

### 2. 纯注意力 Transformer 架构：全连接时空交互

传统方法采用基于 BEV 的时空建模或自回归/扩散生成，时空特征交互受限。SparseWorld-TC 采用**前馈纯注意力 Transformer**（Figure 3），包含两个关键注意力模块：

- **帧级交叉注意力**：每个未来帧的占用嵌入通过交叉注意力查询过去帧的传感器嵌入，实现跨模态信息融合。
- **时间自注意力**：在所有未来帧之间应用自注意力，直接捕捉长时间跨度的时空依赖。

消融实验证实了这一设计的必要性：移除时间注意力使语义 mIoU 从 25.60 降至 25.07，移除可变形注意力进一步降至 23.89（Table 3），证明全注意力架构对时空特征交互至关重要。

### 3. 轨迹条件注入：从隐式到显式的场景演化控制

这是 SparseWorld-TC 最具区分度的创新点。现有方法对场景演化缺乏显式控制，而 SparseWorld-TC 将未来自车轨迹 $\tau = \{ \mathbf{x}_t \}_{t=1}^T$ 作为**条件信号**直接注入世界模型。

- 轨迹通过时空嵌入模块融合位置和时间信息，形成轨迹特征向量。
- 该嵌入在帧级注意力阶段与占用特征融合，引导场景按照给定轨迹方向演化。

**决定性证据**：消融实验（Table 3）显示，使用真实轨迹条件后，平均语义 mIoU 从 15.44%（无轨迹）跃升至 25.60%，几何 IoU 从 32.19% 提升至 49.02%。Figure 6 进一步展示了同一场景在不同轨迹条件（直行、左转、右转）下产生符合预期的差异化预测，验证了条件控制的灵活性与一致性。

### 4. 随机集成训练策略：提升长程泛化

传统方法通常以固定未来帧数进行监督，模型对长程预测的泛化能力不足。SparseWorld-TC 提出**随机集成训练**：训练时从 $\{2, \dots, T\}$ 中随机选择目标序列长度 $L$ 进行监督。

这一策略使模型在长期预测（1-8s）中 mIoU 提升 2.0 个百分点（20.36 vs 22.33），IoU 提升 2.1 个百分点（Table 4），有效缓解了长程预测中的性能衰减。

### 创新总结

| 变更槽位 | Baseline 值 | SparseWorld-TC 值 | 因果作用 |
|---------|------------|-------------------|---------|
| 占用表示 | 离散 VAE token / 密集 BEV 网格 | 稀疏锚点（可学习 3D 点 + 特征向量） | 消除量化损失与几何先验约束，提升表示容量 |
| 特征交互架构 | 基于 BEV 的时空建模 / 自回归生成 | 全注意力前馈 Transformer（帧级 + 时间注意力） | 实现全连接时空交互，捕捉长程依赖 |
| 条件注入方式 | 无 / 隐式条件 | 显式轨迹时空嵌入融合 | 实现可控的场景演化预测 |
| 训练策略 | 固定未来帧监督 | 随机集成训练（随机选择预测长度） | 提升长程预测泛化能力 |

这四项创新协同作用，使 SparseWorld-TC 在 Occ3D-nuScenes 基准上以相机输入取得语义 mIoU 26.42%（超越此前最佳方法 COME 18.7%）和几何 IoU 49.21%（超越 11.7%），并在长达 8 秒的长期预测中保持显著领先优势。

## 整体框架

SparseWorld‑TC 将 4D 占用预测建模为一个**轨迹条件的稀疏世界模型**，其核心设计是抛弃现有方法中普遍使用的 VAE 离散 token 化和 BEV 几何投影，转而采用**纯注意力 Transformer 架构**，以一组稀疏 3D 锚点作为占用表示，直接从多视图图像特征中端到端地学习未来场景的时空演化。

### 输入与输出流

模型的输入由三部分组成：

1. **历史传感器观测** $\mathbf{S}_{-T':0}$：过去 $T'$ 帧的多视图相机图像，经图像主干（ResNet‑50 或 DINOv3‑Base）提取多尺度特征。
2. **初始占用先验** $\mathcal{M}_{1:T}$：$T$ 帧未来时刻的初始占用锚点集合，每个锚点由一组随机采样的 3D 点 $P_i$ 和对应的可学习特征向量 $\mathbf{f}_i$ 组成。
3. **未来自车轨迹** $\tau = \{\mathbf{x}_t\}_{t=1}^T$：$T$ 个离散时刻的自车位姿状态，作为条件信号注入模型。

输出为未来 $T$ 帧的占用预测序列 $\mathcal{O}_{1:T}$，每帧包含每个锚点的 3D 点偏移量和语义类别 logits，经过解码形成稠密的语义占用场。

### 核心模块与数据流

整个 pipeline 可以概括为“**嵌入 → 融合 → 解码**”三个阶段，对应图 Figure 3 所示的架构：

![[assets/figures/papers/paper_list_l2041_https_arxiv_org_abs_2511_22039/figures/003_Figure_3.jpg]]
*Figure 3: We embed the sensor observations, occupancy priors, and trajectories into feature vectors. These embeddings pass through stacked frame-level attention and temporal attention blocks that iteratively fuse cross-modal and cross-time information into occupancy features. Those occupancy features finally decode random points into meaningful occupancy predictions*

**1. 多源嵌入**

- **传感器嵌入**：以每个锚点的 3D 中心 $\mathbf{c}_i$ 为查询点，通过可变形注意力操作从多视图图像特征图上采样空间特征，得到传感器特征 $\mathbf{f}_i'$。
- **占用嵌入**：直接使用锚点的可学习特征向量 $\mathbf{f}_i$ 作为占用先验嵌入。
- **轨迹时空嵌入**：将轨迹点的空间坐标与时间索引分别编码，通过可学习的仿射变换融合为统一的时空特征向量，作为条件信号注入后续注意力模块。

**2. 堆叠式注意力融合**

嵌入后的三类特征进入由**帧级注意力**和**时间注意力**交替堆叠构成的 Transformer 模块：

- **帧级注意力**：对每一帧 $t$，当前占用嵌入通过交叉注意力与过去帧的传感器嵌入交互，同时融合该帧对应的轨迹时空嵌入，实现“传感器证据 + 轨迹引导 → 当前帧占用特征”的信息聚合。
- **时间注意力**：在所有未来帧的占用特征之间执行自注意力，捕捉跨帧的长程时空依赖，确保预测序列的时间一致性。

这种“帧内跨模态融合 + 帧间时序推理”的设计，使得模型能够根据给定的轨迹条件，灵活地引导场景沿特定方向演化。

**3. 解码头**

融合后的占用特征通过两个并行的 MLP 解码头，分别预测每个锚点内各 3D 点的**空间偏移量**和**语义类别 logits**。偏移量将随机初始化的采样点“去噪”为与真实场景表面对齐的占用点云，语义 logits 则赋予每个点语义标签，最终形成完整的 4D 语义占用预测。

### 训练策略

训练时采用**随机集成策略**：设最大预测时长为 $T$，每次迭代随机选择一个目标序列长度 $L \in \{2, \dots, T\}$，仅对前 $L$ 帧的预测结果进行监督。这使得单一模型能够灵活适应不同长度的预测需求，并在长程预测中显著提升性能（消融实验表明，该策略使长期平均 mIoU 从 20.36% 提升至 22.33%）。

损失函数由两部分组成：

$$\mathcal{L} = \mathcal{L}_{CD} + \mathcal{L}_{focal}$$

其中 $\mathcal{L}_{CD}$ 为预测点云与真值点云之间的双向 L1 倒角距离损失，$\mathcal{L}_{focal}$ 为逐点的焦点分类损失，分别监督几何重建精度和语义预测质量。

### 与先前方法的关键差异

| 设计维度 | 先前方法（OccWorld, COME 等） | SparseWorld‑TC |
|---------|------------------------------|----------------|
| 占用表示 | 离散 VAE token 或密集 BEV 网格 | 稀疏锚点：可学习 3D 点集 + 特征向量 |
| 特征交互 | 基于 BEV 的时空建模或自回归/扩散生成 | 前馈式纯注意力 Transformer（帧级 + 时间注意力） |
| 条件注入 | 无显式条件或隐式条件 | 轨迹时空嵌入显式注入帧级注意力 |
| 训练策略 | 固定未来帧长度监督 | 随机集成训练，支持灵活预测时长 |

这种设计使得 SparseWorld‑TC 在避免 VAE 信息瓶颈和 BEV 几何约束的同时，通过轨迹条件实现了对场景演化的精确控制，并在 Occ3D‑nuScenes 的 1–3 秒和 1–8 秒预测任务上均大幅超越先前最佳方法。

## 核心模块与公式推导

SparseWorld-TC 将未来占用预测建模为一个**纯注意力前馈 Transformer**，其核心由三个关键模块串联而成：稀疏锚点占用表示、轨迹时空嵌入、以及帧级-时间双重注意力融合。

### 3.1 稀疏锚点占用表示

模型摒弃了传统方法中依赖 VAE 离散 token 或密集 BEV 网格的表示方式，转而采用**稀疏锚点（anchors）** 来描述场景占用。单帧占用表示定义为：

$$
\mathcal{M} = \{ A_i \}_{i=1}^N, \quad A_i = (P_i, \mathbf{f}_i)
$$

其中，每个锚点 $A_i$ 由一组 3D 查询点集 $P_i$ 和一个关联的特征向量 $\mathbf{f}_i$ 构成。$N$ 为锚点总数。这种稀疏表示从一组随机初始化的 3D 点出发，通过后续的注意力机制从多视图图像特征中端到端地学习其几何偏移与语义标签，无需任何离散化或 BEV 投影步骤。

### 3.2 轨迹时空嵌入

轨迹条件信号是引导场景沿指定路径演化的关键“因果旋钮”。轨迹 $\tau$ 定义为一段离散的自车状态序列：

$$
\tau = \{ \mathbf{x}_t \}_{t=1}^T
$$

其中 $\mathbf{x}_t$ 包含位置和朝向信息，$T$ 为预测时长。为将轨迹信息有效注入 Transformer，模型设计了**时空嵌入（spatiotemporal embedding）** 模块，通过可学习的仿射变换将位置嵌入与时间嵌入融合为统一的轨迹特征向量。该嵌入随后被送入帧级注意力模块，与占用特征进行交叉注意力交互，实现轨迹条件对场景演化的显式引导。

### 3.3 帧级注意力与时间注意力

世界模型 $\mathcal{F}$ 的整体功能可形式化为：

$$
\mathcal{O}_{1:T} = \mathcal{F} \left( \mathcal{M}_{1:T}, \mathbf{S}_{-T':0}, \tau \right)
$$

即根据初始占用先验 $\mathcal{M}_{1:T}$、历史传感器特征 $\mathbf{S}_{-T':0}$ 和轨迹 $\tau$，预测未来 $T$ 帧的占用序列 $\mathcal{O}_{1:T}$。

架构内部通过两类注意力实现跨模态与跨时间的特征融合（参见 Figure 3）：

- **帧级注意力（Frame-level Attention）**：对每一未来帧 $t$，占用嵌入通过交叉注意力查询历史传感器嵌入，同时融合轨迹时空嵌入，完成单帧内的多模态信息聚合。
- **时间注意力（Temporal Attention）**：在所有未来帧之间施加自注意力，捕捉长程时空依赖，确保预测序列的时间一致性。

消融实验证实，移除时间注意力使语义 mIoU 从 25.60 降至 25.07，移除可变形注意力（传感器嵌入的关键操作）则进一步降至 23.89，表明两类注意力均为性能的关键支撑。

### 3.4 解码头与损失函数

每个锚点的占用特征最终通过两个 MLP 解码头分别预测：
- **点偏移量**：将初始随机点去噪至物体表面；
- **语义类别 logits**：赋予每个点语义标签。

训练监督采用**倒角距离损失（Chamfer Distance Loss）** 与**焦点分类损失（Focal Loss）** 的联合优化：

$$
\mathcal{L}_{CD} = \frac{1}{|\mathbb{P}|} \sum_{\mathbf{p}\in\mathbb{P}} D(\mathbf{p},\mathbb{P}_g) + \frac{1}{|\mathbb{P}_g|} \sum_{\mathbf{p}_g\in\mathbb{P}_g} D(\mathbf{p}_g,\mathbb{P})
$$

$$
\mathcal{L} = \mathcal{L}_{CD} + \mathcal{L}_{focal}
$$

其中 $\mathbb{P}$ 为预测点云，$\mathbb{P}_g$ 为目标点云（从真值占用体素中心提取），$D(\cdot,\cdot)$ 采用 L1 距离。倒角距离双向度量确保预测点分布与目标点云在几何上紧密对齐，焦点损失则缓解类别不平衡问题。

### 补充图表

![[assets/figures/papers/paper_list_l2041_https_arxiv_org_abs_2511_22039/figures/002_Figure_2.jpg]]
*Figure 2: Occupancy is modeled as a collection of anchors formed by a bundle of 3D points paired with an occupancy embedding. The embedding is decoded by two MLPs to yield per point offsets and semantic class logits, which denoise sampled points to a consistent occupancy field*

## 实验与分析

### 核心结果：Occ3D-nuScenes 基准

SparseWorld-TC 在 Occ3D-nuScenes 基准上进行了 4D 占用预测评估，覆盖 1s、2s、3s 的短时预测和 1-8s 的长期预测。Table 1 给出了短时预测（1-3s）的主要结果，Table 2 给出了长期预测（1-8s）的结果。

![[assets/figures/papers/paper_list_l2041_https_arxiv_org_abs_2511_22039/figures/005_Table_1.jpg]]
*Table 1: 4D occupancy forecasting performance on Occ3D-nuScenes [38]. Input denotes the modality of input apart from the ego trajectory. Avg. denotes average performance of that in 1s, 2s, and 3s*

![[assets/figures/papers/paper_list_l2041_https_arxiv_org_abs_2511_22039/figures/006_Table_2.jpg]]
*Table 2: Long-term 4D occupancy forecasting performance*

**短时预测（1-3s）**：SparseWorld-TC-Large 以纯相机输入取得平均语义 mIoU 26.42%、几何 IoU 49.21%，相较先前最优相机方法 **COME** 分别提升 18.7%（26.42 vs. 22.26）和 11.7%（49.21 vs. 44.07）。更大的 SparseWorld-TC-Large*（DINOv3-Base 骨干）进一步将 mIoU 推至 29.89%、IoU 推至 53.52%，在所有相机方法中全面领先。值得注意的是，SparseWorld-TC 系列在仅使用相机输入的条件下，已大幅超越使用地面真值占用的 **DOME**（mIoU 21.38%）和 **COME**（mIoU 22.26%），表明稀疏锚点表示与全注意力架构的强表示能力。

**长期预测（1-8s）**：在长达 8 秒的预测中，SparseWorld-TC-Large 取得平均语义 mIoU 22.33%、几何 IoU 45.35%，相较使用地面真值占用的 COME 分别提升 17.1%（22.33 vs. 19.07）和 51.4%（45.35 vs. 29.96）。这一结果表明，SparseWorld-TC 在长时预测中的性能衰减远小于基线方法，验证了时间注意力机制对长程时空依赖的有效建模能力。

### 消融研究

消融实验围绕四个关键设计展开：轨迹条件、训练策略、注意力模块、嵌入模块。

**轨迹条件的影响（Table 3）**：移除轨迹条件后，平均 mIoU 从 25.60% 骤降至 15.44%，IoU 从 49.02% 降至 32.19%，降幅分别达 39.7% 和 34.3%。使用预测轨迹（而非真实轨迹）时，mIoU 为 24.83%、IoU 为 47.36%，与真实轨迹条件差距较小，表明模型对轨迹预测误差具有一定鲁棒性。这一结果确证了轨迹条件信号是引导场景演化的核心因果旋钮。

**训练策略的影响（Table 4）**：随机集成训练（random ensemble）在长期预测中显著优于固定帧训练：mIoU 从 20.36% 提升至 22.33%（+2.0 pp），IoU 从 43.26% 提升至 45.35%（+2.1 pp）。随机选择未来帧长度进行监督增强了模型对可变预测时长的泛化能力。

**注意力模块的影响（Table 7）**：移除时间注意力使 mIoU 从 25.60% 降至 25.07%，IoU 从 49.02% 降至 47.53%；移除可变形注意力使 mIoU 降至 23.89%，IoU 降至 46.55%。可变形注意力的移除导致更大降幅，说明从多视图图像特征中高效采样 3D 锚点特征是模型性能的关键支撑。

**嵌入模块的影响（Table 6）**：消融传感器嵌入、占用先验嵌入或轨迹时空嵌入均导致性能下降，验证了三者协同融合的必要性。

### 失败模式与局限性

Figure 10 展示了典型失败案例：
- **严重遮挡**：当目标（如车辆、护栏）被严重遮挡时，模型难以准确恢复其占用和语义。
- **远未来小物体出现**：在 6 秒后的预测中，远处突然出现的小物体（如行人）容易被遗漏或预测错误。

这些失败模式揭示了稀疏锚点表示在极稀疏观测下的固有挑战：当图像证据不足以支撑 3D 点的语义去噪时，模型倾向于保守预测或产生空洞。

### 关键图表结论

- **Figure 4**：3 秒预测内的定性结果显示，模型能有效捕捉动态（移动车辆）和静态（建筑物、道路）场景变化。
- **Figure 5**：长期预测可视化表明，即使到 8 秒，场景结构仍保持较高一致性，动态物体的运动趋势合理。
- **Figure 6**：条件预测可视化展示了同一初始场景在不同轨迹条件（直行、左转、右转）下的差异化演化，直观验证了轨迹条件机制的有效性。
- **Table 9**：小物体性能改进表显示，SparseWorld-TC 在行人、自行车等小类别上的 mIoU 显著优于基线，归因于稀疏锚点对细粒度几何的灵活建模能力。
- **Table 8**：GPU 内存与推理速度对比显示，SparseWorld-TC 在保持高精度的同时具有竞争力的效率，Large* 模型在精度-速度权衡上表现最优。

![[assets/figures/papers/paper_list_l2041_https_arxiv_org_abs_2511_22039/figures/010_Figure_6.jpg]]
*Figure 6: Forecasting with conditioned trajectories*

![[assets/figures/papers/paper_list_l2041_https_arxiv_org_abs_2511_22039/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative results of our proposed SparseWorld-TC are presented here. Our method effectively captures both dynamic and static changes in the surrounding environment over a 3-second forecasting horizon*

![[assets/figures/papers/paper_list_l2041_https_arxiv_org_abs_2511_22039/figures/009_Figure_5.jpg]]
*Figure 5: Long-term 4D occupancy world model forecasting*

![[assets/figures/papers/paper_list_l2041_https_arxiv_org_abs_2511_22039/figures/015_Table_9.jpg]]
*Table 9: Performance Improvement for Small Objects*

### 补充图表

![[assets/figures/papers/paper_list_l2041_https_arxiv_org_abs_2511_22039/figures/007_Table_3.jpg]]
*Table 3: Ablation study on trajectory. Avg. denotes average performance of mIoU or IoU in 1s, 2s, and 3s*

![[assets/figures/papers/paper_list_l2041_https_arxiv_org_abs_2511_22039/figures/008_Table_4.jpg]]
*Table 4: Ablation study on training strategies. Avg. denotes average performance of mIoU or IoU in 1-8s*

![[assets/figures/papers/paper_list_l2041_https_arxiv_org_abs_2511_22039/figures/011_Table_7.jpg]]
*Table 7: Ablation on Removing Temporal and Deformable Attention. Avg. denotes average of mIoU or IoU in 1s, 2s, and 3s*

![[assets/figures/papers/paper_list_l2041_https_arxiv_org_abs_2511_22039/figures/014_Table_6.jpg]]
*Table 6: Ablation study on embedding modules. Avg. denotes average performance of mIoU or IoU in 1s, 2s, and 3s*

## 方法谱系与知识库定位

### 与现有工作的关系

SparseWorld-TC 的核心设计直接回应了当前 4D 占用预测方法的两个瓶颈：**离散 token 化对表示容量的限制**，以及 **BEV 几何先验对时空特征交互的约束**。理解其谱系位置，需要从这两个维度展开。

**对 VAE/离散 token 范式的替代。** 以 **OccWorld**（Zheng et al., ECCV 2024）为代表的基线将 3D 占用体素压缩为离散 token 序列，再通过自回归 Transformer 预测未来 token。这种设计受限于 VAE codebook 的有限容量，难以保留细粒度几何细节。SparseWorld-TC 完全抛弃了离散 token 化，转而采用**稀疏锚点表示**——将场景占用建模为一组可学习的 3D 点集与特征向量的集合（$\mathcal{M} = \{ A_i \}_{i=1}^N, A_i = (P_i, \mathbf{f}_i)$）。这一表示从多视图图像特征中端到端学习，无需中间压缩，保留了连续的几何表达能力。

**对 BEV 投影范式的替代。** 现有方法（如 COME、I2-World、RenderWorld 等）普遍依赖 BEV 特征图作为统一的时空表示空间，通过自回归或扩散模型在 BEV 平面上生成未来占用。BEV 的固定网格分辨率限制了空间精度，且 2D 平面上的时序建模难以捕捉复杂的三维动态。SparseWorld-TC 采用**全注意力前馈 Transformer 架构**（Figure 3），通过帧级交叉注意力和跨帧时间注意力直接在 3D 锚点特征空间中融合多模态信息，绕过了 BEV 投影的几何近似损失。

**条件预测范式的引入。** 与现有工作将未来轨迹作为隐式输入或完全忽略条件信号不同，SparseWorld-TC 引入了**显式轨迹时空嵌入**机制。轨迹信息 $\tau = \{ \mathbf{x}_t \}_{t=1}^T$ 通过可学习的仿射变换融合位置编码与时间编码，直接注入占用特征，使模型能够根据给定的自车轨迹灵活地引导场景演化。消融实验（Table 3）表明，使用真实轨迹条件后，平均语义 mIoU 从 15.44% 跃升至 25.60%，几何 IoU 从 32.19% 提升至 49.02%，验证了轨迹条件信号的因果作用。

**训练策略的改进。** 传统方法通常固定未来帧长度进行监督训练，导致模型在长期预测中泛化能力不足。SparseWorld-TC 提出**随机集成训练策略**：在训练时随机选择目标序列长度 $L \in \{2, \dots, T\}$，使模型学习适应不同的预测时域。Table 4 的消融显示，该策略在长期预测（1-8s）中带来 mIoU 2.0 个百分点的提升（20.36 vs 22.33），IoU 提升 2.1 个百分点。

### 适用边界与局限

SparseWorld-TC 的适用边界由其设计选择决定，在以下场景中表现出局限性：

**严重遮挡场景。** 模型的稀疏锚点表示依赖多视图图像特征的可变形注意力采样。当目标区域被严重遮挡时，投影到该区域的图像特征质量下降，导致占用预测错误。Figure 10（左）展示了车辆和护栏在严重遮挡下的预测失败案例。

**远未来小物体的出现。** 在长时预测中（6 秒以上），场景中可能出现当前帧完全不可见的小物体（如远处行人、小型障碍物）。由于模型仅从历史传感器特征和轨迹条件推断未来，缺乏对"新出现物体"的先验建模能力，这些物体的预测质量显著下降（Figure 10 右）。

**360° 自监督扩展尚未完成。** 论文展示了利用前向相机进行高斯喷溅重建的扩展能力（Figure 7），以及验证集上的未来传感器观测预测（Figure 8），但尚未实现全 360° 视图的自监督训练。这意味着当前模型的稀疏占用表示尚未在环视传感器数据上得到全面验证。

**对轨迹条件的依赖。** 当使用预测轨迹（而非真实轨迹）作为条件时，性能从 mIoU 25.60% 降至 23.50%（Table 3），表明模型对轨迹条件的质量敏感。在实际部署中，轨迹预测模块的误差会传播到占用预测中。

### 开放问题与后续方向

论文明确指出了两个开放问题，为后续工作提供了方向：

1. **向 3D 高斯表示的扩展。** 如何将 SparseWorld-TC 的稀疏占用表示扩展到 3D 高斯溅射（3D Gaussian Splatting）表示，实现逼真的传感器数据渲染？这一方向将世界模型从几何占用预测提升到可微渲染层面，有望支持闭环的视觉规划与自监督学习。

2. **世界模型与运动规划的融合。** 如何利用学习到的未来世界模型直接辅助运动规划与决策？当前框架仅输出未来占用预测，尚未与下游规划模块形成端到端的联合优化。将世界模型嵌入规划循环，是通往自动驾驶世界模型的关键一步。

从知识库定位的角度，SparseWorld-TC 处于**稀疏表示学习**与**世界模型**的交叉点。它在方法上借鉴了 3D 视觉中的可变形注意力机制和点云处理中的倒角距离损失（$\mathcal{L}_{CD}$），在架构上呼应了 Transformer 在序列建模中的优势，在理念上延续了世界模型对"学习预测未来"的追求。其核心贡献在于证明了：**在 4D 占用预测中，稀疏锚点 + 纯注意力 + 轨迹条件的设计组合，可以在不依赖离散 token 和 BEV 投影的前提下，实现显著的性能提升和长时预测稳定性**。

## 原文 PDF

![[paperPDFs/CVPR_2026/SparseWorld_TC_Trajectory_Conditioned_Sparse_Occupancy_World_Model.pdf]]