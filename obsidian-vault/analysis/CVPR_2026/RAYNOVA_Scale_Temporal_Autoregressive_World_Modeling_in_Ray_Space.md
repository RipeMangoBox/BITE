---
title: "RAYNOVA: Scale-Temporal Autoregressive World Modeling in Ray Space"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/RAYNOVA_Scale_Temporal_Autoregressive_World_Modeling_in_Ray_Space.pdf
project_link: "https://raynova-ai.github.io/"
code_link: null
aliases:
- RAYNOVA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过基于相对Plücker-ray位置的各向同性时空表示，消除对特定相机拓扑和运动模式的结构性依赖，并统一尺度与时间的双因果自回归过程，实现以最小归纳偏置维持物理合理性。
primary_logic: 核心洞察在于利用相机光线空间中的相对位置编码构造一个几何无关的连续4D表示，使模型能够在统一的全局注意力中进行跨视角、跨帧的尺度-时序自回归，从而在无显式3D先验的情况下获得高时空一致性和强泛化性。
claims:
- 提出双因果自回归框架，同时遵循尺度和时间的拓扑顺序进行生成。
- 构造基于相对Plücker-ray位置编码的各向同性时空表示，用于统一的4D推理。
- 相对光线编码在消融实验中显著优于绝对编码，且全局注意力远超解耦时空设计。
- 零样本下可泛化至未见的Waymo相机配置，新视角合成性能大幅领先基线。
---

# RAYNOVA: Scale-Temporal Autoregressive World Modeling in Ray Space

> [!tip] 核心洞察
> 核心洞察在于利用相机光线空间中的相对位置编码构造一个几何无关的连续4D表示，使模型能够在统一的全局注意力中进行跨视角、跨帧的尺度-时序自回归，从而在无显式3D先验的情况下获得高时空一致性和强泛化性。

| 字段 | 内容 |
|------|------|
| 中文题名 | RAYNOVA：光线空间中的尺度-时序自回归世界建模 |
| 英文题名 | RAYNOVA: Scale-Temporal Autoregressive World Modeling in Ray Space |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.20685) · [Project](https://raynova-ai.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | RAYNOVA |
| Dataset | nuScenes, nuScenes object condition, nuScenes map condition, nuScenes novel view synthesis |

> [!tip] 效果简介
> - nuScenes (multi-view video generation) 上，FID↓ / FVD↓ / Throughput↑ 10.5 / 91 / 1.96 vs 17.0 / 139 / 0.67 (Panacea) (-38% / -35% / +193%)。
> - nuScenes object condition (camera-only, StreamPETR) 上，NDS↑ 41.9 (89% of oracle) vs 32.1 (68% of oracle, Panacea) (+30%)。
> - nuScenes map condition (multisensor, BEVFusion) 上，mIoU↑ 49.9 (79% of oracle) vs 47.0 (75% of oracle, MagicDrive) (+6%)。

## 概要

当前世界模型普遍将空间与时间相关性解耦处理，依赖固定相机配置、相邻视角或显式3D表示等强归纳偏置，限制了模型对新型传感器布局、灵活相机运动及开放世界环境的泛化能力。RAYNOVA 针对这一瓶颈，提出一种基于光线空间的双因果自回归框架，以最小归纳偏置实现物理合理的高时空一致性生成。

核心思路是：利用相机光线空间中的相对Plücker-ray位置编码构造几何无关的各向同性4D表示，使模型在统一的全局注意力中同时进行跨视角、跨帧的尺度-时序自回归，从而在无显式3D先验的情况下获得强泛化性。具体而言，RAYNOVA 将多视角视频生成建模为“先尺度后时间”的双因果过程——每一帧的每一尺度以所有视角的历史前缀为条件，并通过7D相对旋转位置嵌入消除对绝对相机坐标的依赖。训练上，引入循环训练策略与随机位错误注入，缩小训练-推理分布差异，支持长时域视频生成。

在 nuScenes 多视角视频生成基准上，RAYNOVA 取得 FID 10.5、FVD 91、吞吐量 1.96 的全面领先，相较 Panacea 分别提升 38%、35% 和 193%。在 3D 目标条件保真度上，下游检测器 NDS 达 41.9（oracle 的 89%），大幅超越基线。新视角合成任务中，相机平移 1m 时 FID 较 OmniRe 降低 55%。消融实验证实：相对光线编码显著优于绝对编码，统一全局注意力大幅超越解耦时空设计，尺度因果性与循环训练对视频质量提升均起关键作用。此外，RAYNOVA 在零样本条件下可泛化至未见过的 Waymo 相机配置，展现出作为通用世界基础模型的潜力。

当前方法主要局限于驾驶场景训练数据，在非驾驶环境及闭环仿真等下游应用中的泛化性尚待验证。



世界模型旨在构建对物理环境的内部表征，以支持预测、规划和决策。近年来，随着自回归视觉生成技术的快速发展，利用大规模视频数据学习世界模型已成为一条极具前景的技术路径。然而，当前的世界模型普遍面临一个核心瓶颈：**空间与时间相关性被解耦处理**，模型通常依赖固定相机配置、相邻视角或显式3D表示（如BEV、体积渲染）等强归纳偏置来维持时空一致性。这种设计虽然在一定程度上简化了建模难度，却严重限制了模型对新型传感器布局、灵活相机运动及开放世界环境的泛化能力。

具体而言，现有方法存在以下结构性缺口：

1. **相机拓扑依赖**：多数模型假设固定的相机外参和数量，难以适应不同的传感器配置。当相机布局发生变化时，模型往往需要重新训练或进行繁琐的标定适配。

2. **时空解耦建模**：主流方案将空间注意力与时间注意力分离处理，虽降低了计算复杂度，却牺牲了跨视角、跨帧的全局一致性，导致长时域视频生成中出现时序抖动和视角间不一致。

3. **显式3D先验的局限**：基于BEV或NeRF的表示虽能提供几何约束，但在稀疏视角、大范围运动或复杂遮挡场景下，其重建质量会显著下降，且计算开销随分辨率增长而急剧增加。

针对上述问题，RAYNOVA 提出了一种**光线空间中的尺度-时序自回归世界建模**范式。其核心动机在于：通过消除对特定相机拓扑和运动模式的结构性依赖，以最小归纳偏置实现物理上合理的世界建模。具体而言，RAYNOVA 利用相机光线空间中的相对位置编码，构造一个几何无关的连续4D表示，使模型能够在统一的全局注意力中进行跨视角、跨帧的尺度-时序自回归，从而在无显式3D先验的情况下获得高时空一致性和强泛化性。这一设计使得模型可以零样本泛化至未见过的相机配置，并在新视角合成、条件视频生成等任务上显著超越现有基线。



## 核心方法与创新机理

RAYNOVA 的核心创新在于通过**光线空间中的相对位置编码**和**尺度-时序双因果自回归框架**，从根本上消除了现有世界模型对固定相机拓扑和显式3D表示的强归纳偏置依赖，实现了以最小结构先验维持高时空一致性的开放世界建模能力。

### 关键创新点

**1. 双因果自回归生成范式**

现有世界模型普遍采用分离的空间/时间自注意力或显式3D BEV/体积表示来处理时空建模，而 RAYNOVA 提出了一种统一的**双因果自回归框架**，同时遵循尺度（scale-wise）和时间（temporal）的拓扑顺序进行生成。如 Figure 3 所示，模型首先在同一帧内按从粗到细的尺度顺序生成多视角图像的 token 图，然后沿时间轴逐帧推进。这种设计将多视角视频的联合分布分解为：

$$p \left( { X } _ { 1 : K } ^ { 1 : V , 1 : T } \right) = \prod _ { t = 1 } ^ { T } \prod _ { k = 1 } ^ { K } p \left( X _ { k } ^ { 1 : V , t } | X _ { 1 : k - 1 } ^ { 1 : V , 1 : t } \right)$$

即每一帧的每一尺度以所有视角的历史前缀为条件，实现了跨视角、跨帧的联合建模。消融实验（Table 7）表明，仅使用前缀尺度作为条件效果最佳（FID 17.2），而使用全部历史尺度会严重损害动力学建模（FID 60.4），仅使用同尺度则时间一致性不足（FID 20.7）。

**2. 各向同性时空表示：相对 Plücker-ray 位置编码**

传统方法依赖绝对 Plücker-ray 嵌入或固定相机配置的偏置来编码空间信息，这限制了模型对新型传感器布局的泛化能力。RAYNOVA 构造了基于**相对 Plücker-ray 位置编码**的各向同性时空表示，将每条相机光线表示为带时间戳的7D向量：

$$\mathbf { p } _ { k } ^ { v , t } = ( \mathbf { m } _ { k } ^ { v , t } \in \mathbb { R } ^ { 3 } , \mathbf { d } _ { k } ^ { v , t } \in \mathbb { R } ^ { 3 } , t )$$

其中 $\mathbf{m}$ 为光线原点与方向的叉积，$\mathbf{d}$ 为单位方向向量。通过在全局自注意力中引入相对旋转位置编码，注意力分数转化为仅依赖 token 间相对位置的表达：

$$a _ { i , j } = \mathbf { q } _ { k _ { i } } ^ { v _ { i } , t _ { i } } ^ { T } \mathbf { R } _ { \Delta } ^ { i , j } \mathbf { k } _ { k _ { j } } ^ { v _ { j } , t _ { j } }$$

其中 $\mathbf{R}_\Delta$ 为块对角旋转矩阵，分别对光线原点、方向和时间维度使用不同频带的 RoPE。Table 6 的消融实验证实，相对光线编码显著优于绝对编码（FID: 17.2 vs 18.7, FVD: 124 vs 214），且远超无时空模块的基线（FID: 18.7, FVD: 214）。

**3. 统一全局注意力机制**

与解耦时空注意力的设计不同，RAYNOVA 采用**统一的全局自注意力**，使每个视觉 token 能够同时关注所有视角和帧的前缀 token。Table 8 的消融结果显示，统一全局注意力大幅超越解耦时空设计（FID: 10.5 vs 15.6, FVD: 91 vs 140），验证了以最小归纳偏置实现时空一致性的有效性。这一机制与相对光线位置编码的配合，使模型在零样本条件下即可泛化至未见过的 Waymo 相机配置（Figure 6），新视角合成性能大幅领先基于显式3D表示的基线（Table 5，1m平移下 FID 14.11 vs OmniRe 31.48）。

**4. 循环训练策略**

针对自回归模型训练与推理分布不一致的问题，RAYNOVA 提出了**循环训练策略**，结合隐状态缓存与随机位错误注入。由于全局自注意力是唯一跨帧操作的模块（Sec. 3.4），训练时仅缓存该模块的 KV 隐状态，并在前向传播中注入随机位错误以模拟推理时的累积误差。Table 9 表明，注入随机位错误可将 FID 从 19.8 降至 17.2，FVD 从 142 降至 124；循环训练阶段进一步将 FVD 从约100降至91，对提升长时域视频的时间连贯性尤为关键。

### 创新点总结

| 创新维度 | 基线方法 | RAYNOVA 方案 | 关键证据 |
|---------|---------|-------------|---------|
| 时空一致性机制 | 分离的空间/时间自注意力或显式3D表示 | 基于相对光线位置编码的统一全局自注意力 | Table 8: FID 10.5 vs 15.6 |
| 位置嵌入 | 绝对 Plücker-ray 嵌入或固定相机偏置 | 7D 相对旋转位置嵌入，消除绝对坐标依赖 | Table 6: FID 17.2 vs 18.7 |
| 训练范式 | 仅对短片段 teacher-forcing | 循环训练 + KV 缓存 + 随机位错误注入 | Table 9: FID 17.2 vs 19.8 |
| 自回归顺序 | 单尺度 next-token 或独立图像/视频生成 | 双因果顺序：先尺度后时间，联合建模 | Table 7: 前缀尺度 FID 17.2 vs 全部尺度 60.4 |

这些创新共同构成了 RAYNOVA 在 nuScenes 多视角视频生成任务上以 FID 10.5、FVD 91、吞吐量 1.96 images/s 全面领先现有基线（如 Panacea 的 FID 17.0、FVD 139、吞吐量 0.67）的技术基础，并在仅使用公开数据训练的条件下展现了显著的数据效率和泛化优势。



RAYNOVA 的整体框架围绕“双因果自回归”范式构建，旨在以最小归纳偏置实现多视角视频的统一生成。其核心设计原则是：**在相机光线空间中构造各向同性的时空表示，并通过统一的全局注意力同时建模跨视角、跨帧的尺度-时序依赖关系**。

### 输入与输出流

模型的输入由三部分构成：
1. **多视角图像序列**：来自任意相机配置的 $V$ 个视角、$T$ 个时间步的 RGB 图像。
2. **相机光线参数**：每张图像中每个 token 对应的 7D 扩展 Plücker 射线 $\mathbf{p}_k^{v,t} = (\mathbf{m}_k^{v,t} \in \mathbb{R}^3, \mathbf{d}_k^{v,t} \in \mathbb{R}^3, t)$，其中 $\mathbf{m}$ 为原点-方向叉积，$\mathbf{d}$ 为单位方向，$t$ 为时间戳。
3. **条件信号**（可选）：文本描述、3D 目标边界框、HD 地图等控制信息。

输出为按双因果顺序生成的多尺度 token 图序列，经解码器还原为多视角视频帧。

### 模块组成与数据流

RAYNOVA 的每个 Transformer 块内部按固定顺序串联三个注意力模块，形成清晰的数据流：

```
视觉 token → 图像内自注意力 → 全局自注意力 → 图像内交叉注意力 → 下一层
```

#### 1. 多尺度图像分词器
每张输入图像首先被独立量化为 $K$ 个尺度的 token 图 $X_1, X_2, \ldots, X_K$，形成层次化表示。这一“下一尺度预测”的设计使得模型能够从粗到细逐步生成图像内容，其单图似然分解为：
$$p(X_1, X_2, \ldots, X_K) = \prod_{k=1}^{K} p(X_k \mid X_1, X_2, \ldots, X_{k-1})$$

#### 2. 图像内自注意力模块
该模块独立作用于每张图像的 token，确保单帧视觉真实感。其关键优势在于可以复用预训练的图像生成模型权重，降低训练成本并提升收敛速度。

#### 3. 全局自注意力模块
这是实现时空一致性的核心模块。它采用掩码自注意力机制，使每个视觉 token 能够关注来自**所有视角、所有历史帧**中处于尺度-时序前缀位置的全部 token。该模块集成了基于相对 Plücker-ray 位置的旋转位置编码，将注意力分数转化为仅依赖 token 间相对几何关系的表达：
$$a_{i,j} = \left(\mathbf{R}_{k_i}^{v_i, t_i} \mathbf{q}_{k_i}^{v_i, t_i}\right)^T \left(\mathbf{R}_{k_j}^{v_j, t_j} \mathbf{k}_{k_j}^{v_j, t_j}\right) = \mathbf{q}_{k_i}^{v_i, t_i^T} \mathbf{R}_{\Delta}^{i,j} \mathbf{k}_{k_j}^{v_j, t_j}$$

其中 $\mathbf{R}$ 为块对角旋转矩阵，分别对射线原点 $\mathbf{m}$、方向 $\mathbf{d}$ 和时间 $t$ 应用不同频带的 RoPE：
$$\mathbf{R} = \begin{bmatrix} \mathbf{R_m} & 0 & 0 \\ 0 & \mathbf{R_d} & 0 \\ 0 & 0 & \mathrm{RoPE}_{\frac{d}{4}}(t) \end{bmatrix}$$

这种设计消除了对绝对相机坐标或固定拓扑的依赖，使模型天然具备跨相机配置的泛化能力。

#### 4. 图像内交叉注意力模块
该模块负责将外部控制信号（文本、3D 框、地图）对齐到视觉 token。它使用轴向 2D RoPE 增强条件的空间局部性，确保生成内容忠实于给定的条件约束。

### 双因果自回归顺序

模型的生成过程严格遵循两层因果拓扑顺序（参见 Figure 3）：

1. **尺度因果性**：同一帧内的所有视角图像联合建模，先预测粗尺度 token，再以前缀尺度为条件预测细尺度 token。多视角联合分布为：
   $$p(X_1^{1:V}, \ldots, X_K^{1:V}) = \prod_{k=1}^{K} p(X_k^{1:V} \mid X_1^{1:V}, \ldots, X_{k-1}^{1:V})$$

2. **时序因果性**：在尺度因果的基础上，当前帧的所有尺度以前序所有帧的完整尺度前缀为条件。完整的双因果生成过程为：
   $$p\left({X}_{1:K}^{1:V, 1:T}\right) = \prod_{t=1}^{T} \prod_{k=1}^{K} p\left(X_k^{1:V, t} \mid X_{1:k-1}^{1:V, 1:t}\right)$$

### 循环训练策略

为缩小训练（teacher-forcing 短片段）与推理（自回归长序列生成）之间的分布差异，RAYNOVA 引入循环训练范式：

- 逐帧进行前向/反向传播，同时缓存全局自注意力模块的隐状态（KV cache），因为这是唯一跨帧操作的模块。
- 在训练过程中向缓存的隐状态注入随机位错误，模拟推理时可能出现的误差累积，迫使模型学习鲁棒的生成策略。

这一策略在消融实验中证明对长时域视频的时间连贯性至关重要，将 FVD 从约 100 进一步降至 91。

### 框架设计的核心优势

整体框架通过三个关键设计实现了对现有方法的超越：
- **几何无关性**：相对光线位置编码消除了对特定相机拓扑的结构性依赖，使模型在零样本条件下即可泛化至未见过的 Waymo 相机配置（Table 5, Figure 6）。
- **统一时空建模**：全局自注意力同时处理空间和时间维度，消融实验表明其性能大幅超越解耦时空注意力设计（FID: 10.5 vs 15.6, FVD: 91 vs 140, Table 8）。
- **高效推理**：自回归架构结合 KV 缓存机制，推理吞吐量达 1.96 images/s，远超扩散模型基线（Table 1）。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2602_20685/figures/002_Figure_2.jpg]]
*Figure 2: Overview of RAYNOVA Framework. RAYNOVA is composed of dual-casual (scale and time) blocks. The local scale attention and local cross attention works on each image indepedently, while the global causal attention works across multi-view and multiframe images enhanced with a unified ray-level relative position embedding for better spatio-temporal consistency*



### 3.1 多尺度图像分词与下一尺度预测

RAYNOVA 将每张图像独立量化为多尺度 token 图，构建层次化表示。对于单张图像，其多尺度 token 图集合 $\{X_1, X_2, \ldots, X_K\}$ 的联合分布被分解为尺度自回归形式：

$$p ( X _ { 1 } , X _ { 2 } , \ldots , X _ { K } ) = \prod _ { k = 1 } ^ { K } p ( X _ { k } | X _ { 1 } , X _ { 2 } , \ldots , X _ { k - 1 } )$$

其中 $X_k$ 表示第 $k$ 个尺度的 token 图，$K$ 为总尺度数。每一尺度的生成以前缀所有更小尺度的 token 图为条件，形成“下一尺度预测”范式（Sec. 3.1, Eq. 1）。

### 3.2 双因果自回归框架

RAYNOVA 的核心创新在于同时遵循**尺度因果性**与**时间因果性**。对于同一帧内的 $V$ 个视角，多视角图像被联合建模，因为它们共同描述特定时刻的统一 3D 空间：

$$p ( X _ { 1 } ^ { 1 : V } , \ldots , X _ { K } ^ { 1 : V } ) = \prod _ { k = 1 } ^ { K } p ( X _ { k } ^ { 1 : V } | X _ { 1 } ^ { 1 : V } , \ldots , X _ { k - 1 } ^ { 1 : V } )$$

将尺度因果性扩展至时间维度，得到完整的双因果生成过程——每一帧的每一尺度以所有视角的历史前缀为条件：

$$p \left( { X } _ { 1 : K } ^ { 1 : V , 1 : T } \right) = \prod _ { t = 1 } ^ { T } \prod _ { k = 1 } ^ { K } p \left( X _ { k } ^ { 1 : V , t } | X _ { 1 : k - 1 } ^ { 1 : V , 1 : t } \right)$$

其中 $T$ 为总帧数，上标 $v$ 和 $t$ 分别标识视角与时间步。该分解确保生成过程严格遵循“先尺度后时间”的拓扑顺序，如图 3 所示（Sec. 3.2, Eq. 4）。

### 3.3 相对 Plücker-Ray 位置编码

为实现几何无关的各向同性时空表示，RAYNOVA 在相机光线空间中构造相对位置编码。每个 token 对应一条扩展的 7D Plücker 射线：

$$\mathbf { p } _ { k } ^ { v , t } = ( \mathbf { m } _ { k } ^ { v , t } \in \mathbb { R } ^ { 3 } , \mathbf { d } _ { k } ^ { v , t } \in \mathbb { R } ^ { 3 } , t )$$

其中 $\mathbf{m} = \mathbf{o} \times \mathbf{d}$ 为射线原点与方向的叉积，$\mathbf{d}$ 为单位方向向量，$t$ 为时间戳（Sec. 3.3, Eq. 5）。

全局自注意力的分数通过相对旋转位置编码计算，仅依赖 token 间的相对位置：

$$a _ { i , j } = \left( \mathbf { R } _ { k _ { i } } ^ { v _ { i } , t _ { i } } \mathbf { q } _ { k _ { i } } ^ { v _ { i } , t _ { i } } \right) ^ { T } \left( \mathbf { R } _ { k _ { j } } ^ { v _ { j } , t _ { j } } \mathbf { k } _ { k _ { j } } ^ { v _ { j } , t _ { j } } \right) = \mathbf { q } _ { k _ { i } } ^ { v _ { i } , t _ { i } } ^ { T } \mathbf { R } _ { \Delta } ^ { i , j } \mathbf { k } _ { k _ { j } } ^ { v _ { j } , t _ { j } }$$

其中 $\mathbf{R}_{\Delta}^{i,j}$ 为相对旋转矩阵，将绝对位置编码转换为仅依赖相对位置的表达，消除对特定相机拓扑的依赖（Sec. 3.3, Eq. 6）。

射线不同分量（原点 $\mathbf{m}$、方向 $\mathbf{d}$、时间 $t$）的旋转矩阵被组合为块对角阵，各维度使用不同频带的 RoPE：

$$\mathbf { R } = \left[ \begin{array} { c c c } { \mathbf { R _ { m } } } & { 0 } & { 0 } \\ { 0 } & { \mathbf { R _ { d } } } & { 0 } \\ { 0 } & { 0 } & { \mathrm { R o P E } _ { \frac { d } { 4 } } ( t ) } \end{array} \right]$$

其中 $\mathbf{R_m}$ 和 $\mathbf{R_d}$ 分别为 3×3 块对角矩阵，内部沿对角线放置不同频带的 2D RoPE 矩阵（Sec. 3.3, Eq. 7）。消融实验证实，该相对编码显著优于绝对编码（FID: 17.2 vs 18.7, FVD: 124 vs 214），且全局注意力大幅超越解耦时空设计（FID: 10.5 vs 15.6, FVD: 91 vs 140），验证了各向同性表示的核心作用（Table 6, Table 8）。

### 3.4 模型架构与注意力模块

每个 Transformer 块依次包含三个注意力模块（Fig. 2）：

- **图像内自注意力**：独立处理每张图像，确保单帧视觉真实性，并复用预训练权重。
- **全局自注意力**：在所有视角和帧之间进行统一注意力计算，集成相对光线位置编码，实现时空一致性。训练时采用掩码自注意力，使每个 token 仅关注其在尺度和时间拓扑顺序中的前缀。
- **图像内交叉注意力**：对齐文本描述、3D 目标边界框和 HD 地图等控制信号，使用轴向 2D RoPE 增强条件局部性。

### 3.5 循环训练策略

为缩小训练与推理的分布差异，RAYNOVA 采用循环训练范式（Alg. 1）。由于全局自注意力是唯一跨帧操作的模块，训练时缓存其隐状态（KV cache），逐帧进行前向/反向传播。同时注入随机位错误以模拟推理时的累积误差。消融实验表明，该策略将 FVD 从约 100 降至 91，对提升长时域视频的时间连贯性尤为关键（Table 9, Sec. 4.4）。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2602_20685/figures/003_Figure_3.jpg]]
*Figure 3: Dual-Causality for Multi-View Video Generation. Green arrows represent the causal dependency, while the darkness indicates the topological order of autoregression (from light to dark)*



## 实验与关键发现

### 4.1 多视角视频生成主结果

RAYNOVA 在 nuScenes 验证集上与现有世界模型进行了全面对比，评估指标包括 FID、FVD 和生成吞吐量。如表 1 所示，RAYNOVA 在 384×672 分辨率下取得 **FID 10.5、FVD 91、吞吐量 1.96 images/s** 的优异表现。相比最强扩散基线 **Panacea**（FID 17.0, FVD 139, 0.67 images/s），FID 相对降低 38%，FVD 降低 35%，推理速度提升近 3 倍。值得注意的是，部分对比基线使用了大量内部私有数据进行训练，而 RAYNOVA 仅基于公开的 nuScenes 和 nuPlan 数据集训练，却在所有指标上取得全面领先，充分体现了方法的数据效率和有效性。

### 4.2 条件保真度评估

为验证生成视频对控制信号的还原能力，论文使用预训练感知模型对生成结果进行下游评估。如表 2 所示，在 3D 目标检测条件（仅相机输入的 StreamPETR）下，RAYNOVA 取得 **NDS 41.9**，达到真实数据 oracle 分数的 89%，而 Panacea 仅达到 68%（NDS 32.1），相对提升 30%。在 HD 地图条件（多传感器 BEVFusion）下，RAYNOVA 的 mIoU 达到 **49.9**（oracle 的 79%），优于 MagicDrive 的 47.0（oracle 的 75%），提升 6%。这些结果表明双因果自回归框架能有效保留精细的空间条件信息。

### 4.3 新视角合成泛化

RAYNOVA 的几何无关光线空间表示使其天然具备新视角合成能力。如表 5 所示，在相机平移 1m 的设置下，RAYNOVA 取得 **FID 14.11、FVD 117.20**，相比专门的新视角合成方法 **OmniRe**（FID 31.48, FVD 152.01）分别降低 55% 和 23%。更重要的是，RAYNOVA 在零样本条件下可泛化至未见过的 Waymo 相机配置（图 6），生成的多视角视频保持高度时空一致性，这验证了相对 Plücker-ray 位置编码消除绝对相机拓扑依赖的核心设计优势。

### 4.4 消融实验

#### 相对光线位置编码

表 6 的消融实验揭示了位置编码设计的决定性作用。**相对 Plücker-ray 位置编码**（FID 17.2, FVD 124）显著优于绝对编码（FID 18.7, FVD 214），FVD 下降 42%。移除整个时空模块后性能进一步恶化（FID 18.7, FVD 214），证实了统一 4D 表示对时空一致性的关键贡献。

#### 尺度因果性策略

表 7 和图 4 展示了不同尺度条件策略的对比。**仅使用前缀尺度**（prefix scales only）取得最优 FID 17.2 和 FVD 124；使用全部历史尺度（all scales）导致 FID 急剧恶化至 60.4，说明过多历史信息会干扰动力学建模；仅使用同尺度（same scale）的 FID 为 20.7，时间一致性不足。

#### 全局 vs 解耦时空注意力

表 8 对比了统一全局注意力与解耦时空设计。**统一全局注意力**（FID 10.5, FVD 91）大幅超越解耦方案（FID 15.6, FVD 140），FVD 下降 35%。这验证了跨视角、跨帧的联合注意力对维持 4D 一致性的必要性。

#### 循环训练与位错误注入

表 9 显示，在训练中**注入随机位错误**（random bit error injection）可将 FID 从 19.8 降至 17.2，FVD 从 142 降至 124，有效缩小了训练-推理分布差距。循环训练阶段进一步将长视频生成的 FVD 从约 100 降至 91，对提升长时域时间连贯性尤为关键。

#### 模型规模

图 5 显示，将模型从 130M 扩展至 2B 参数可带来显著的视觉质量提升，验证了该框架的扩展潜力。

### 4.5 局限性

当前实验存在以下局限：训练数据局限于驾驶场景，在非驾驶环境（机器人、无人机等）中的泛化性能尚未验证；评估主要聚焦于多视角视频生成质量与条件保真度，尚未探索闭环仿真等更广泛的世界模型应用。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2602_20685/figures/004_Table_1.jpg]]
*Table 1: Multi-view Video Generation Performance*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2602_20685/figures/005_Table_2.jpg]]
*Table 2: Fidelity to Object Condition*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2602_20685/figures/007_Table_5.jpg]]
*Table 5: Novel View Synthesis Performance with Camera Shifts*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2602_20685/figures/008_Table_6.jpg]]
*Table 6: Ablation Study on Camera Ray*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2602_20685/figures/010_Table_7.jpg]]
*Table 7: Ablation Study on Scale Causality and Model Size*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2602_20685/figures/012_Table_8.jpg]]
*Table 8: Ablation Study on Spatio-Temporal Module*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2602_20685/figures/013_Table_9.jpg]]
*Table 9: Ablation Study on Random Errors in Training*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2602_20685/figures/009_Figure_4.jpg]]
*Figure 4: Ablation Study on Scale Causality. Conditioning on all scales in history hurts the modeling of dynamics, while condition-130M Model 2B Model ing only on same scale is insufficient for temporal coherence*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2602_20685/figures/011_Figure_5.jpg]]
*Figure 5: Ablation Study on Model Size. Large scale model can bring significantly better visual quality*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2602_20685/figures/014_Figure_6.jpg]]
*Figure 6: Zero-Shot to Unseen Waymo Open Dataset Camera Configuration*



## 定位与知识库关联

### 1. 方法演进脉络与关键差异

RAYNOVA 的出现，源于对当前世界模型在时空建模中“强归纳偏置”与“泛化瓶颈”的根本性反思。现有主流方法普遍将空间与时间相关性解耦处理，依赖固定相机配置、相邻视角或显式 3D 表示（如 BEV、体积渲染）来维持一致性。这种设计虽然简化了优化，却严重限制了模型对新型传感器布局、灵活相机运动及开放世界环境的泛化能力。

RAYNOVA 的核心突破在于**以最小归纳偏置实现物理合理性**。其技术路径可概括为三个递进层次：

1.  **从解耦到统一**：摒弃分离的空间/时间自注意力或显式 3D 中间表示，转而采用基于相对 Plücker-ray 位置编码的统一全局自注意力。该模块使每个视觉 token 能同时关注所有视角和帧的历史前缀，在单一注意力机制内完成 4D 时空推理（Table 8 消融实验证实，统一全局注意力相较解耦时空注意力，FID 从 15.6 降至 10.5，FVD 从 140 降至 91）。
2.  **从绝对到相对**：位置嵌入从依赖固定相机拓扑的绝对 Plücker-ray 编码，进化为 7D 相对旋转位置嵌入（RoPE）。该编码作用于相机光线空间，使模型对相机的外参变化完全等变，从而消除了对特定传感器布局的结构性依赖（Table 6 消融显示，相对编码相较绝对编码，FID 从 18.7 改善至 17.2，FVD 从 214 大幅降至 124）。
3.  **从单序到双序**：自回归顺序从单尺度 next-token 或独立图像/视频生成，扩展为“先尺度、后时间”的双因果过程。每一帧的每一尺度以所有视角的历史前缀为条件，联合建模多视角多帧分布（Table 7 消融表明，仅使用前缀尺度效果最佳；使用全部尺度会严重损害动力学建模，FID 高达 60.4；仅使用同尺度则时间一致性不足，FID 为 20.7）。

此外，RAYNOVA 引入了**循环训练策略**（结合隐状态缓存与随机位错误注入），以缩小 teacher-forcing 训练与自回归推理之间的分布差异。Table 9 的消融证实，注入随机位错误可将 FID 从 19.8 降至 17.2，FVD 从 142 降至 124；循环训练阶段进一步将 FVD 从约 100 降至 91，对长时域视频的时间连贯性尤为关键。

### 2. 与相关工作的关系图谱

RAYNOVA 在驾驶场景世界模型的知识库中，占据了一个独特的位置：它既是自回归视觉生成范式的继承者，又是对扩散模型主导格局的有力挑战者。

**与扩散模型基线的对比**：
在 nuScenes 多视角视频生成基准上，RAYNOVA 以 FID 10.5、FVD 91 的表现全面超越扩散模型基线，包括 **DriveDreamer**、**Panacea**（FID 17.0, FVD 139）、**DrivingDiffusion** 和 **MagicDrive** 等。更关键的是，RAYNOVA 的生成吞吐量达到 1.96 images/s，较 Panacea 的 0.67 images/s 提升近 193%，展现出显著的实际部署优势。值得注意的是，RAYNOVA 仅使用公开的 nuScenes 和 nuPlan 数据训练，而部分基线使用了大量内部数据，这进一步凸显了其数据效率。

**在新视角合成任务上的泛化优势**：
当相机发生平移（1m/2m/4m）时，RAYNOVA 的零样本性能大幅领先显式 3D 表示方法。在 1m 平移设定下，RAYNOVA 的 FID 为 14.11，FVD 为 117.20，相较 **OmniRe**（FID 31.48, FVD 152.01）和 **StreetGaussian** 等基于 Gaussian Splatting 的方法有显著提升。这验证了相对光线编码在消除相机拓扑依赖方面的核心价值。

**条件保真度与下游任务**：
在 3D 目标检测条件（StreamPETR）下，RAYNOVA 生成的视频达到 NDS 41.9（oracle 的 89%），显著优于 Panacea 的 32.1（oracle 的 68%）；在 HD 地图条件（BEVFusion）下，mIoU 达到 49.9（oracle 的 79%），超越 MagicDrive 的 47.0。在运动规划任务中，RAYNOVA 生成的视频能提供有效的运动线索，进一步验证了其物理一致性。

**零样本跨数据集泛化**：
RAYNOVA 在未见过的 Waymo Open Dataset 相机配置上，无需任何微调即可生成高质量多视角视频（Figure 6），而依赖固定相机偏置的方法（如 **BEVWorld**、**X-Drive**）则难以实现此类泛化。这直接证明了各向同性时空表示的设计有效性。

### 3. 适用边界与局限

尽管 RAYNOVA 在驾驶场景中展现了强大的能力，其当前版本仍存在明确的适用边界：

1.  **领域局限**：训练数据完全局限于驾驶场景（nuScenes + nuPlan），模型在非驾驶环境（如室内机器人、无人机航拍、通用操作场景）中的泛化性能尚未验证。相对光线编码的几何无关性理论上支持跨领域迁移，但缺乏实证。
2.  **应用深度不足**：评估主要聚焦于多视角视频生成和新视角合成，尚未探索闭环仿真、交互式驾驶决策、具身智能等更广泛的世界模型下游应用。生成视频的物理一致性虽在运动规划任务中得到初步验证，但能否支撑强化学习等闭环训练仍是开放问题。
3.  **尺度-质量权衡**：模型规模从 130M 扩展至 2B 可带来显著视觉质量提升（Figure 5），但训练数据规模与多样性对性能的边际增益关系尚需量化。在数据受限的领域，小模型的性能天花板可能较低。
4.  **长时域稳定性**：循环训练策略有效缓解了分布漂移，但超长序列（如数分钟以上）生成的误差累积问题未得到系统性分析。隐状态缓存的记忆容量与遗忘机制有待深入研究。

### 4. 开放问题与未来方向

RAYNOVA 开辟了若干值得探索的方向：

1.  **跨领域泛化验证**：模型在非驾驶环境中的零样本/少样本泛化能力是检验其“通用世界模型”主张的关键试金石。在机器人操作、无人机巡检等场景中的表现亟待评估。
2.  **闭环仿真与决策**：将 RAYNOVA 作为神经仿真器嵌入强化学习或模型预测控制回路，评估其生成的视觉动态能否支撑有效的策略学习，是验证其物理合理性的终极标准。
3.  **数据规模化律**：在更大规模、更多样化的视频数据上训练 RAYNOVA，量化数据规模与生成质量、泛化能力之间的缩放关系，对于理解该方法的潜力上限至关重要。
4.  **记忆与遗忘机制**：为隐状态缓存引入更复杂的记忆管理策略（如选择性遗忘、动态容量分配），以支持更长时域的视频生成和更稳定的闭环仿真。
5.  **多模态条件融合**：当前模型已支持文本、3D 框、HD 地图等条件，未来可探索动作指令、自然语言导航等更丰富的控制信号，以拓展其在具身智能和人机交互中的应用。



## 原文 PDF

![[paperPDFs/CVPR_2026/RAYNOVA_Scale_Temporal_Autoregressive_World_Modeling_in_Ray_Space.pdf]]
