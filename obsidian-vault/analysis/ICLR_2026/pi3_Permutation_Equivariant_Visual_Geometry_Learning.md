---
title: "$\\pi^3$: Permutation-Equivariant Visual Geometry Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/pi3_Permutation_Equivariant_Visual_Geometry_Learning.pdf
project_link: null
code_link: https://github.com/yyfz/Pi3
aliases:
- P3
- P3PEVGL
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "移除所有与顺序相关的组件（如帧索引位置编码、用于标记参考视图的可学习token），并采用完全置换等变的Transformer架构（交替进行视图间和全局自注意力），使模型对输入顺序不敏感。"
primary_logic: "通过预测定义在各自相机坐标系下的仿射不变相机姿态和尺度不变局部点图，并利用相对监督（相对姿态、相对点图对齐）进行训练，可以完全消除对全局参考坐标系的需求，同时保持模型对输入顺序的鲁棒性。"
claims:
- "π³在Sintel数据集上的相机姿态估计ATE从VGGT的0.167降至0.074。"
- "π³在Sintel数据集上的视频深度估计绝对相对误差从VGGT的0.299降至0.233。"
- "π³在DTU和ETH3D上的点云估计标准差接近零（DTU上Acc. std. mean为0.003，ETH3D上为0.000），远优于现有方法。"
- "π³在RealEstate10K上以30°阈值评估的AUC达到85.90，优于VGGT的77.62。"
---

# $\pi^3$: Permutation-Equivariant Visual Geometry Learning

> [!tip] 核心洞察
> 通过预测定义在各自相机坐标系下的仿射不变相机姿态和尺度不变局部点图，并利用相对监督（相对姿态、相对点图对齐）进行训练，可以完全消除对全局参考坐标系的需求，同时保持模型对输入顺序的鲁棒性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | π³：置换等变视觉几何学习 |
| 英文题名 | $\pi^3$: Permutation-Equivariant Visual Geometry Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=DTQIjngDta) · [GitHub](https://github.com/yyfz/Pi3) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | $\pi^3$ |
| Dataset | RealEstate10K, Sintel, ETH3D |

> [!tip] 效果简介
> - RealEstate10K 上，AUC@30° 为 85.90，对比 77.62 (VGGT)，变化 +8.28。
> - Sintel 上，ATE↓ 为 0.074，对比 0.167 (VGGT)，变化 -0.093。
> - Sintel 上，Abs Rel↓ (视频深度) 为 0.233，对比 0.299 (VGGT)，变化 -0.066。

## 概要

本文提出 $\pi^3$，一个完全置换等变的前馈式视觉几何学习框架，旨在解决现有方法（如 VGGT、DUSt3R）因依赖固定参考视图坐标系而引入的归纳偏置问题。核心瓶颈在于：当参考视图选择不佳时，模型的重建质量会显著下降。$\pi^3$ 的因果干预是**彻底移除所有与顺序相关的组件**——包括帧索引位置编码和用于标记参考视图的可学习 token——并采用交替视图间与全局自注意力的 Transformer 架构，使模型对输入顺序完全不敏感。

方法的核心洞察在于：通过预测定义在各自相机坐标系下的**仿射不变相机姿态**和**尺度不变局部点图**，并利用**相对监督**（相对姿态与相对点图对齐）进行训练，可以完全消除对全局参考坐标系的需求。模型使用 DINOv2 骨干网络嵌入每个视图，经过 36 层交替注意力模块（少于 VGGT 的 48 层）后，由独立的解码器生成相机姿态、局部点图和置信度图。

主要实验结果验证了该设计的有效性：
- 在 RealEstate10K 上，$\pi^3$ 的相机姿态估计 AUC@30° 达到 **85.90**，显著优于 VGGT 的 77.62。
- 在 Sintel 数据集上，ATE 从 VGGT 的 0.167 降至 **0.074**；视频深度估计的绝对相对误差从 0.299 降至 **0.233**。
- 在 DTU 和 ETH3D 上的点云估计标准差接近零（分别为 0.003 和 0.000），验证了其对输入顺序的鲁棒性。
- 推理速度达到 **57.4 FPS**（KITTI 上单卡 A800），优于 VGGT 的 43.2 FPS。

消融实验（Table 7）表明，移除参考视图依赖（即置换等变性）是性能提升的关键因素，尺度不变局部点图和仿射不变相机姿态的监督方式也均有显著贡献。需要注意的是，主要实验中的 $\pi^3$ 使用了 VGGT 的预训练权重进行初始化，但从零开始训练的公平比较（Table 8）同样证明了 $\pi^3$ 架构本身的优越性。



视觉几何学习（从多张图像估计相机姿态和3D结构）的核心瓶颈在于：现有前馈式方法普遍依赖一个固定的参考视图，将其相机坐标系作为全局坐标系，从而引入了不必要的归纳偏置。这种设计导致模型对参考视图的选择高度敏感——当参考视图选择不佳（如视角极端或纹理匮乏）时，重建质量会显著下降。

以DUSt3R、VGGT为代表的当前SOTA方法，其共性缺陷在于：通过拼接特殊token（Type A）或添加可学习嵌入（Type B）来标记参考视图，迫使模型学习一个以该视图为基准的绝对坐标系。这一机制包含两个关键问题：
1. **顺序敏感性**：输入视图的排列顺序直接影响输出，模型无法对输入顺序保持鲁棒。
2. **参考帧依赖**：全局坐标系的质量完全取决于参考视图的选择，错误选择会导致级联误差。

现有方法试图通过DINO-based参考帧选择（如CUT3R）来缓解这一问题，但无法从根本上消除。如图2所示，即使采用智能选择策略，现有方法在不同参考帧下的性能仍表现出显著的不一致性。

本文的动机是：**能否设计一种完全消除参考视图依赖的架构，使模型对输入顺序天然不敏感？** 核心思路是移除所有与顺序相关的组件（帧索引位置编码、可学习参考视图token），采用完全置换等变的Transformer架构（交替进行视图间和全局自注意力），并预测定义在各自相机坐标系下的仿射不变相机姿态和尺度不变局部点图，通过相对监督进行训练。

这一设计的关键因果机制在于：通过将监督信号从绝对坐标系下的损失改为相对姿态和相对点图对齐的损失，模型不再需要学习一个全局参考系，从而实现了对输入顺序的完全鲁棒性。消融实验（Table 7）证实，移除参考视图依赖是性能提升的最关键因素——完整模型在7-Scenes-dense上的Acc. Mean为0.019，而使用参考视图的变体为0.024和0.022。



## 核心方法与创新机理

π³ 的核心创新在于彻底消除了前馈式视觉几何学习中根深蒂固的参考视图依赖。现有方法（如 DUSt3R、VGGT）强制将某一视图的相机坐标系作为全局坐标系，这一设计引入了不必要的归纳偏置，导致模型对参考视图的选择高度敏感——当参考视图不佳时重建质量显著下降。π³ 通过一个简单但根本性的因果旋钮解决了这个问题：移除所有与顺序相关的组件（帧索引位置编码、用于标记参考视图的可学习 token），并采用完全置换等变的 Transformer 架构。

**架构设计。** π³ 使用 DINOv2 骨干网络将每个视图嵌入为 patch token 序列，然后通过交替的视图间和全局自注意力模块进行处理（与 VGGT 类似，但仅使用 36 层，而 VGGT 为 48 层）。关键区别在于：π³ 不指定任何视图为参考——它预测每个视图自身相机坐标系下的**尺度不变局部点图**和**仿射不变相机姿态**。解码器（相机姿态、局部点图、置信度图）共享架构但不共享权重。

**训练信号的重构。** 由于没有全局坐标系，π³ 无法使用绝对姿态监督。其解决方案是使用**相对监督**：对所有视图对计算相对姿态，并最小化预测相对旋转（测地线距离）和平移（Huber 损失）与真实值之间的差异。点图损失同样巧妙：先求解一个全局最优尺度因子 $s^*$（通过最小化深度加权的 L1 距离），再计算对齐后的点云重建损失。此外还引入了法向量损失（最小化预测与真实法向量的夹角）和置信度损失（基于 L1 重建误差阈值的二值交叉熵）。

**决定性证据。** 消融研究（Table 7）明确验证了参考视图消除是性能提升的关键：完整模型在 7-Scenes-dense 上的 Acc. Mean 为 0.019，而使用参考视图的变体为 0.022–0.024。置换等变性带来的鲁棒性在 Table 6 中得到量化证明——π³ 在 DTU 和 ETH3D 上的点云估计标准差接近零（DTU 上 Acc. std. mean 为 0.003，ETH3D 上为 0.000），远优于任何现有方法。在主要基准上，π³ 在 Sintel 数据集上将相机姿态估计 ATE 从 VGGT 的 0.167 降至 0.074，在 RealEstate10K 上以 30°阈值评估的 AUC 从 77.62 提升至 85.90。视频深度估计的绝对相对误差也从 0.299 降至 0.233。



π³ 的架构核心在于彻底移除传统前馈式视觉几何学习中对参考视图的依赖，从而实现输入序列的完全置换等变性。其整体 pipeline 由三个模块串联而成：骨干网络、交替注意力模块和解码器。

**输入与嵌入**：给定 $N$ 张无序图像 $\mathcal{S} = \{I_1, \ldots, I_N\}$，pipeline 首先使用一个 DINOv2 骨干网络将每张视图嵌入为 patch token 序列。与 VGGT、DUSt3R 等基线方法的关键区别在于，π³ 在此阶段**完全移除了所有顺序相关组件**，包括帧索引位置编码和用于标记参考视图的可学习 token。这使得模型对输入图像的排列顺序天然不敏感。

**核心处理模块**：嵌入后的 token 序列被送入一系列交替的视图间自注意力（view-wise self-attention）和全局自注意力（global self-attention）层。该模块的设计与 VGGT 类似，但层数更少（π³ 使用 36 层，VGGT 使用 48 层）。视图间注意力允许同一张图像内的 patch 进行信息交换，而全局注意力则允许不同视图之间的 patch 进行交互。这种交替设计是实现置换等变性的关键——由于没有特殊的参考视图 token，所有视图在注意力计算中地位平等。

**输出与解码**：经过交替注意力模块处理后，token 被送入三个独立的解码器（共享架构但不共享权重），分别预测：
1. **仿射不变相机姿态** $\hat{\mathbf{T}}_i$：每个视图在其自身相机坐标系下的绝对姿态，但训练时仅通过视图间的相对姿态 $(\hat{\mathbf{T}}_{ij} = \hat{\mathbf{T}}_i^{-1} \hat{\mathbf{T}}_j)$ 进行监督，从而消除全局参考坐标系的需求。
2. **尺度不变局部点图** $\hat{\mathbf{X}}_i$：定义在各自相机坐标系下的像素对齐 3D 点图，具有未知的全局尺度。训练时通过求解最优尺度因子 $s^*$ 对齐预测点图和真实点图，并使用深度加权的 L1 损失进行监督。
3. **置信度图** $\hat{\mathbf{C}}_i$：每个像素点的置信度，用于指示重建质量。

**损失函数**：总损失 $\mathcal{L}$ 由四项组成：点云重建损失 $\mathcal{L}_{\mathrm{points}}$、法向量损失 $\mathcal{L}_{\mathrm{normal}}$、置信度损失 $\mathcal{L}_{\mathrm{conf}}$ 和相机损失 $\mathcal{L}_{\mathrm{cam}}$。其中相机损失对所有有序视图对计算旋转测地线距离和平移 Huber 损失。这种相对监督方式使得模型无需任何全局对齐步骤即可从输出中恢复场景的几何结构。



### 置换等变架构

π³ 的核心创新在于构建了一个完全置换等变的映射函数。设输入图像序列为 $\mathcal{S} = (I_1, \ldots, I_N)$，网络输出为：

$$\phi(\mathcal{S}) = ((\mathbf{T}_1, \ldots, \mathbf{T}_N), (\mathbf{X}_1, \ldots, \mathbf{X}_N), (\mathbf{C}_1, \ldots, \mathbf{C}_N))$$

其中 $\mathbf{T}_i$ 为第 $i$ 个视图的仿射不变相机姿态，$\mathbf{X}_i$ 为尺度不变的局部点图，$\mathbf{C}_i$ 为置信度图。该映射满足置换等变性质：

$$\phi(P_\pi(\mathcal{S})) = P_\pi(\phi(\mathcal{S}))$$

即对输入序列施加任意置换 $P_\pi$，输出序列的各分量按相同置换重新排列。这一性质的实现关键在于：**移除了所有顺序相关组件**——包括帧索引位置编码和用于标记参考视图的可学习 token，并采用交替的视图间自注意力与全局自注意力的 Transformer 架构（与 VGGT 类似，但仅使用 36 层交替注意力层，而 VGGT 使用 48 层）。编码器与交替注意力模块的结构与 VGGT 相同。

### 尺度不变局部几何

π³ 为每个视图预测定义在其自身相机坐标系下的局部点图 $\hat{\mathbf{X}}_i \in \mathbb{R}^{H \times W \times 3}$，而非全局坐标系下的点云。由于预测点图与真实点图 $\mathbf{x}_{i,j}$ 之间存在未知的全局尺度因子，训练时通过优化求解最优尺度因子：

$$s^* = \arg\min_s \sum_{i=1}^N \sum_{j=1}^{H \times W} \frac{1}{z_{i,j}} \| s \hat{\mathbf{x}}_{i,j} - \mathbf{x}_{i,j} \|_1$$

其中 $z_{i,j}$ 为真实深度，用于加权。基于最优尺度因子，点云重建损失定义为深度加权的 L1 损失：

$$\mathcal{L}_{\mathrm{points}} = \frac{1}{3 N H W} \sum_{i=1}^N \sum_{j=1}^{H \times W} \frac{1}{z_{i,j}} \| s^* \hat{\mathbf{x}}_{i,j} - \mathbf{x}_{i,j} \|_1$$

此外，法向量损失通过最小化预测法向量 $\hat{\mathbf{n}}_{i,j}$ 与真实法向量 $\mathbf{n}_{i,j}$ 之间的夹角来约束局部几何：

$$\mathcal{L}_{\mathrm{normal}} = \frac{1}{N H W} \sum_{i=1}^N \sum_{j=1}^{H \times W} \operatorname{arccos}\left( \hat{\mathbf{n}}_{i,j} \cdot \mathbf{n}_{i,j} \right)$$

### 仿射不变相机姿态

由于不存在全局参考坐标系，π³ 无法直接监督绝对相机姿态。解决方案是**对所有有序视图对进行相对姿态监督**。从预测的绝对姿态 $\hat{\mathbf{T}}_i$（表示为 $4 \times 4$ 变换矩阵）计算视图 $j$ 到视图 $i$ 的相对姿态：

$$\hat{\mathbf{T}}_{i j} = \hat{\mathbf{T}}_i^{-1} \hat{\mathbf{T}}_j$$

旋转的预测采用 9D 表示（Levinson et al., 2020），随后通过 SVD 正交化转换为 $3 \times 3$ 旋转矩阵。相机损失定义为所有有序视图对上的旋转损失和平移损失的加权和：

$$\mathcal{L}_{\mathrm{cam}} = \frac{1}{N(N-1)} \sum_{i \neq j} \left( \mathcal{L}_{\mathrm{rot}}(i,j) + \lambda_{\mathrm{trans}} \mathcal{L}_{\mathrm{trans}}(i,j) \right)$$

其中旋转损失使用测地线距离（角度）：

$$\mathcal{L}_{\mathrm{rot}}(i,j) = \operatorname{arccos}\left( \frac{\mathrm{Tr}((\mathbf{R}_{ij})^\top \hat{\mathbf{R}}_{ij}) - 1}{2} \right)$$

平移损失使用 Huber 损失 $\mathcal{H}_\delta$ 比较尺度校正后的预测平移与真实平移：

$$\mathcal{L}_{\mathrm{trans}}(i,j) = \mathcal{H}_\delta \big( s^* \hat{\mathbf{t}}_{i j} - \mathbf{t}_{i j} \big)$$

### 总损失函数

模型以多任务学习方式联合优化：

$$\mathcal{L} = \mathcal{L}_{\mathrm{points}} + \lambda_{\mathrm{normal}} \mathcal{L}_{\mathrm{normal}} + \lambda_{\mathrm{conf}} \mathcal{L}_{\mathrm{conf}} + \lambda_{\mathrm{cam}} \mathcal{L}_{\mathrm{cam}}$$

其中各损失权重为：$\lambda_{\mathrm{normal}} = 1.0$，$\lambda_{\mathrm{conf}} = 0.05$，$\lambda_{\mathrm{cam}} = 0.1$，平移损失权重 $\lambda_{\mathrm{trans}} = 100.0$。置信度损失 $\mathcal{L}_{\mathrm{conf}}$ 为二元交叉熵损失，其真实标签依据 L1 重建误差是否低于阈值 $\epsilon$ 来设定。解码器部分——相机姿态、局部点图和置信度图的解码器——共享相同的架构但不共享权重。训练采用初始学习率 $5 \times 10^{-5}$ 和 OneCycleLR 余弦退火调度器，每个训练阶段运行 80 个 epoch，每个 epoch 包含 800 次迭代。



## 实验与关键发现

### 主要结果：相机姿态与几何重建

π³在多个基准上全面超越了现有前馈式方法。在**相机姿态估计**任务中（Table 1），π³在RealEstate10K上以30°阈值评估的AUC达到85.90，显著优于VGGT的77.62；在Sintel数据集上的ATE从VGGT的0.167降至0.074，误差降低超过55%。这一提升的核心机制在于：π³通过消除参考视图依赖，避免了因参考视图选择不佳导致的姿态估计偏差。

![[assets/figures/papers/iclr26_0001_DTQIjngDta_pi3_Permutation-Equivariant_Visual_Geometry_Lear/figures/006_Table_1.jpg]]
*Table 1: Camera pose estimation. RRA, RTA, AUC are evaluated with threshold of 30 degrees*

在**点图估计**任务中（Table 2、Table 3），π³在ETH3D上的Acc. Mean为0.194，优于VGGT的0.287；在NRGBD-sparse上Acc. Mean为0.026，优于VGGT的0.058。对于**视频深度估计**（Table 4），π³在Sintel上的绝对相对误差从VGGT的0.299降至0.233，同时推理速度达到57.4 FPS（KITTI上评估），比VGGT的43.2 FPS快33%。速度提升部分源于更浅的网络（36层交替注意力层 vs VGGT的48层）。

![[assets/figures/papers/iclr26_0001_DTQIjngDta_pi3_Permutation-Equivariant_Visual_Geometry_Lear/figures/007_Table_2.jpg]]
*Table 2: Point map estimation on 7-Scenes and NRGBD*

![[assets/figures/papers/iclr26_0001_DTQIjngDta_pi3_Permutation-Equivariant_Visual_Geometry_Lear/figures/008_Table_3.jpg]]
*Table 3: Point map estimation on DTU and ETH3D*

![[assets/figures/papers/iclr26_0001_DTQIjngDta_pi3_Permutation-Equivariant_Visual_Geometry_Lear/figures/009_Table_4.jpg]]
*Table 4: Video depth estimation on Sintel, Bonn and KITTI. FPS is evaluated on KITTI using one A800 GPU*

在**单目深度估计**中（Table 5），π³在Sintel、Bonn、KITTI、NYU-v2四个数据集上均达到多帧前馈式重建方法中的最佳性能，尽管其设计初衷并非针对单目任务。

![[assets/figures/papers/iclr26_0001_DTQIjngDta_pi3_Permutation-Equivariant_Visual_Geometry_Lear/figures/011_Table_5.jpg]]
*Table 5: Monocular depth estimation*

### 置换等变性的鲁棒性验证

π³的核心创新——置换等变性——在**点云估计的标准差**实验中得到直接验证（Table 6）。在DTU和ETH3D上，π³的标准差接近零（DTU上Acc. std. mean为0.003，ETH3D上为0.000），比现有方法低数个数量级。这表明当输入视图顺序改变时，π³的输出几乎完全一致，而依赖参考视图的方法（如VGGT）则表现出显著波动。

![[assets/figures/papers/iclr26_0001_DTQIjngDta_pi3_Permutation-Equivariant_Visual_Geometry_Lear/figures/012_Table_6.jpg]]
*Table 6: Standard deviation of point cloud estimation*

Figure 2进一步定性展示了这一鲁棒性：当参考视图变化时，VGGT等方法的重建质量出现明显不一致，而π³始终保持稳定。这种鲁棒性的因果机制在于：π³完全移除了帧索引位置编码和参考视图token，使模型对输入顺序不敏感，从而消除了参考视图选择这一人为引入的方差源。

### 消融研究

消融实验（Table 7）量化了各组件的贡献。在7-Scenes-dense上，完整模型的Acc. Mean为0.019，而引入参考视图的变体（Model 1: 0.024, Model 2: 0.022）性能明显下降，证实了消除参考视图依赖是性能提升的关键。尺度不变局部点图（归一化）和仿射不变相机姿态（相对监督）也均有显著贡献。需要注意的是，消融实验中的基线模型已经包含了置换等变架构，因此这些组件的效果是叠加在等变性之上的。

### 公平性分析与从零训练对比

主要实验中的π³使用了VGGT的预训练权重进行初始化，这可能带来一定优势。为排除这一因素，Table 8展示了从零开始训练的结果。在ETH3D和NRGBD上，π³显著优于VGGT基线，说明π³架构本身的优越性是性能提升的根本原因，而非预训练权重的继承。

### 姿态分布分析

Figure 4和Figure 6分析了预测相机姿态的几何性质。π³预测的姿态分布呈现出清晰的低维结构，而VGGT的姿态分布则较为分散。这表明π³学习到的表示具有更强的几何一致性，其内在原因可能是：相对监督迫使模型学习视图间的几何关系，而非记忆特定参考系下的绝对姿态。

### 失败模式与局限

根据论文的明确讨论，π³存在以下限制：1）无法处理透明物体，因为模型没有显式考虑复杂的光传输现象；2）与基于扩散的方法相比，重建的几何细节精细度不足；3）点云生成使用简单的MLP加像素重排上采样机制，在高不确定性区域可能引入明显的网格状伪影。这些失败模式的根源在于模型架构的设计选择——为了保持置换等变性和前馈效率，牺牲了对复杂物理现象和精细细节的建模能力。



## 定位与知识库关联

**与基线方法的关系：从参考视图依赖到置换等变**

π³ 的核心贡献在于诊断并消除了前馈式视觉几何重建方法中一个长期存在的归纳偏置——对固定参考视图的依赖。现有方法如 DUSt3R、Fast3R、FLARE、CUT3R 以及当前最先进的 VGGT，均隐式或显式地将一个输入视图的相机坐标系作为全局坐标系。这种设计通过特殊 token（Type A）或可学习嵌入（Type B）来标记参考视图，导致模型对输入顺序高度敏感：当参考视图选择不佳时（如视角极端、遮挡严重），重建质量会显著下降（Figure 2）。

π³ 的因果性改动是**移除所有与顺序相关的组件**，包括帧索引位置编码和参考视图token，并采用完全置换等变的Transformer架构（交替进行视图间和全局自注意力）。这一改动迫使模型放弃依赖一个固定的“锚点”坐标系，转而学习更本质的几何关系——即视图间的相对姿态和局部几何。具体地，π³ 预测定义在各自相机坐标系下的**仿射不变相机姿态**和**尺度不变局部点图**，并通过相对监督（相对姿态损失、相对点图对齐）进行训练。这种设计使得模型对输入顺序完全鲁棒：在DTU和ETH3D上的点云估计标准差接近零（DTU上Acc. std. mean为0.003，ETH3D上为0.000），远优于现有方法（Table 6）。

**适用边界与性能增益**

π³ 在多个基准上取得了显著提升，其增益主要源于对参考视图依赖的消除：

- **相机姿态估计**：在RealEstate10K上AUC@30°从VGGT的77.62提升至85.90；在Sintel上ATE从0.167降至0.074（Table 1）。
- **点图重建**：在NRGBD-sparse上Acc. Mean从VGGT的0.058降至0.026；在ETH3D上从0.287降至0.194（Table 2, 3）。
- **视频深度估计**：在Sintel上Abs Rel从0.299降至0.233；推理速度达57.4 FPS，优于VGGT的43.2 FPS（Table 4）。
- **鲁棒性**：消融实验（Table 7）表明，移除参考视图依赖是性能提升的关键：完整模型在7-Scenes-dense上的Acc. Mean为0.019，而使用参考视图的变体为0.024–0.022。

**局限与开放问题**

π³ 在架构设计上仍有明确边界：

1. **透明物体处理**：模型未显式考虑复杂光传输现象，无法处理透明物体。
2. **几何细节精细度**：与基于扩散的方法相比，重建的几何细节精细度不足。这与前馈式方法的固有特性相关——单次前向传播难以捕捉高频细节。
3. **网格状伪影**：点云生成使用简单的MLP加像素重排上采样机制，在高不确定性区域可能引入明显的网格状伪影。

**开放问题**包括：如何扩展模型以处理透明物体？如何提高几何细节的精细度以匹配基于扩散的方法？如何减轻上采样MLP引入的网格状伪影？模型如何处理视图间存在极端尺度变化的情况？置信度图阈值epsilon对重建质量的具体影响是什么？模型在超出测试基准的非常大的无序图像集上表现如何？

**知识库定位**

π³ 属于前馈式多视图几何重建方法谱系，其核心贡献在于将置换等变性引入该领域。与VGGT相比，π³ 的编码器和交替注意力模块架构相同，但层数更少（36层 vs. 48层），且解码器不共享权重。在从零开始的公平比较中（Table 8），π³ 在ETH3D和NRGBD上显著优于VGGT，表明其架构优势独立于预训练初始化。π³ 的姿态分布呈现出清晰的低维结构（Figure 4, 6），而VGGT的分布则较为分散，这进一步验证了消除参考视图依赖后模型学习到的几何表示更加本质和紧凑。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/pi3_Permutation_Equivariant_Visual_Geometry_Learning.pdf

![[paperPDFs/ICLR_2026/pi3_Permutation_Equivariant_Visual_Geometry_Learning.pdf]]
