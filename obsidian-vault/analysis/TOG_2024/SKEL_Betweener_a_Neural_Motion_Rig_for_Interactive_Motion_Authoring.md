---
title: "SKEL-Betweener: a Neural Motion Rig for Interactive Motion Authoring"
type: paper
paper_level: A
venue: TOG
year: 2024
pdf_ref: paperPDFs/TOG_2024/SKEL_Betweener_a_Neural_Motion_Rig_for_Interactive_Motion_Authoring.pdf
aliases:
- SB
- SKEL-Betweener
tags:
- TOG_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: SKEL-Betweener
primary_logic: SKEL-Betweener
claims:
- SKEL-Betweener
---

# SKEL-Betweener: a Neural Motion Rig for Interactive Motion Authoring

> [!tip] 核心洞察
> SKEL-Betweener

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SKEL-Betweener: a Neural Motion Rig for Interactive Motion Authoring |
| 英文题名 | SKEL-Betweener: a Neural Motion Rig for Interactive Motion Authoring |
| 会议/期刊 | TOG 2024 |
| Links | [paper](https://doi.org/10.1145/3687941) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method |  |
| Dataset | |

## 概述

三维角色动画的制作长期面临一个核心矛盾：传统关键帧动画虽然能提供精确的控制，但需要动画师手动指定大量的中间姿态，制作一段包含跑动和跳跃的序列往往需要耗费数小时；而数据驱动的运动生成方法虽然高效，却难以让艺术家在生成过程中进行直观的局部干预。**SKEL-Betweener** 提出了一套神经运动绑定（Neural Motion Rig）框架，试图弥合这一鸿沟——仅需给定起始和结束两个姿态，即可生成完整的运动序列，并允许用户通过任意稀疏的中间约束（关节位置或朝向）来精细控制生成结果。

该方法的核心洞察在于将运动生成重新定义为一种“神经中间帧插值”问题，但与以往需要密集上下文帧的中间帧生成模型（如 **TwoStage**，Qin et al. 2022）不同，SKEL-Betweener 支持极稀疏的约束模式：用户可以在时间轴的任意位置、对任意关节施加约束，模型会自动补全其余部分。在 Lafan1 数据集的分布外约束条件下，SKEL-Betweener 的全局位置 L2 距离（L2P）达到 **0.032**，显著优于 TwoStage 基线。

在交互层面，SKEL-Betweener 引入了**神经运动曲线（Neural Motion Curves）** 的概念——将生成的运动表示为可编辑的关节级曲线，能够直接集成到 Blender、Maya 等主流动画软件的标准曲线编辑器中。用户研究显示，与传统的关键帧工具（LIK）相比，无论是新手用户还是专业作者，使用 SKEL-Betweener 都能以更少的操作时间和更少的关键帧数量，更准确地重现参考动画。

技术实现上，模型采用骨骼图网络架构，由关节编码器、骨骼 Transformer（18 层）和关节解码器三部分组成，通过模拟运动编辑过程生成配对数据来训练运动保持版本，从而在保持生成质量的同时支持实时交互式编辑。

## 背景与动机

三维角色动画的制作长期面临效率瓶颈。传统关键帧动画流程要求动画师在时间轴上密集地定义角色姿态，一段包含奔跑与跳跃的序列往往需要耗费约一小时的手工调整，而使用 SKEL-Betweener 仅需数分钟即可完成。这种效率鸿沟源于现有工具的输入模式限制：动画师必须提供密集的上下文帧与结束帧，系统才能生成中间过渡，这本质上是一个“补间”（inbetweening）问题，而非真正的运动创作。

现有补间模型的根本局限在于其约束模式过于僵化。以 **TwoStage**（Qin et al., 2022）为代表的方法要求提供稠密的时间上下文和固定的结束帧，输入约束在时间轴上呈现连续块状分布。这种设计使得模型无法处理稀疏、任意分布的中间约束——动画师无法在运动序列的任意时间点对特定关节施加位置或朝向控制。当约束条件偏离训练分布时，TwoStage 生成的全局位置 L2 距离（L2P）显著升高，表明其泛化能力受限于固定的输入范式。

本文的核心动机在于将运动生成从“补间”范式升级为“运动装配”（motion rigging）范式。SKEL-Betweener 仅需首尾两个姿态即可生成完整运动序列，同时支持在任意中间时刻添加任意关节的稀疏约束。这种灵活的输入模式使得动画师可以像操作骨骼绑定控制器一样，通过直觉式的关节级位置与朝向控制来塑造运动——作者将其抽象为“神经运动曲线”（Neural Motion Curves）。为实现这一目标，方法需要解决两个关键挑战：一是在稀疏约束下保持运动学合理性，二是使模型能够理解并响应分布外（out-of-distribution）的约束组合。

## 核心创新

SKEL‑Betweener 的核心创新在于将运动生成问题从“稠密上下文补全”重新定义为**稀疏约束下的运动插值**，并围绕这一范式构建了三个紧密耦合的组件：稀疏约束接口、神经运动曲线（Neural Motion Curves, NMCs）以及运动保持训练策略。

### 1. 稀疏约束驱动的运动生成范式

传统运动补间模型（如 **TwoStage**, Qin et al. 2022）要求提供稠密的上下文帧和固定的结束帧（Fig. 2a），输入模式僵硬且不直观。SKEL‑Betweener 打破了这一限制：用户只需提供**起始与结束两帧姿态**，以及**任意位置、任意关节、任意时间步的可选中间约束**（Fig. 2c）。模型通过线性插值与球面插值将稀疏控制点初始化为稠密运动张量（位置 $\text{pos} \in \mathbb{R}^{T \times J \times 3}$，朝向 $\text{rot} \in \mathbb{R}^{T \times J \times 6}$），再由骨骼图网络（18 层 Skeletal Transformer）在稀疏约束的引导下生成完整运动序列。

这一范式转变的关键收益在于**交互自由度的大幅提升**：用户无需预先规划完整的约束时间线，可以在任意时刻对任意关节施加位置或朝向约束，模型自动完成全局协调。

### 2. 神经运动曲线（NMCs）作为交互中介

稀疏约束在数学上是离散的时空点，但艺术家需要连续、可编辑的曲线来理解与微调运动。SKEL‑Betweener 将模型输出的运动轨迹直接可视化为**神经运动曲线**——这些曲线既是生成结果的直观呈现，也是交互编辑的句柄。NMCs 同时嵌入 3D 视口（空间轨迹）和曲线编辑器（1D 时序曲线，如旋转分量），与 Blender/Maya 等传统动画工具的工作流无缝衔接（Fig. 7）。

NMCs 的引入解决了深度生成模型在动画管线中的“黑箱”问题：艺术家不再面对不可解释的隐空间，而是通过熟悉的曲线编辑范式来引导和控制生成过程。

### 3. 运动保持训练策略

直接训练的 SKEL‑Betweener 在满足新约束时会不可避免地改变原始运动的高频细节，导致“编辑后运动与原始运动差异过大”的问题。论文的核心洞察是：**重建损失与约束满足损失在基础运动与目标运动差异显著时是相互对抗的**。为解决这一问题，论文提出了一种自监督运动编辑数据生成流程（Fig. 5）：利用预训练的 SKEL‑Betweener，从数据集中采样运动并随机施加两组不相交的约束（一组用于生成编辑后运动，另一组作为测试约束），构造“原始运动—编辑后运动”的配对数据。在此基础上训练**运动保持版本 SKEL‑Betweener\***，其损失函数为：

$$\mathcal{L}_{ME} = \mathcal{L}_{SB} + \lambda_{BM} \mathcal{L}_{BM}$$

其中 $\mathcal{L}_{SB}$ 是标准骨骼重建损失，$\mathcal{L}_{BM}$ 是基础运动保持损失，$\lambda_{BM}$ 控制两者的相对权重。

这一训练策略的效果在 Table 2 中得到验证：SKEL‑Betweener\* 在仅使用 15% 约束时即可达到 L2P = 0.015 的重建精度，而未使用运动保持的版本需要 15%–20% 的额外约束才能达到可比精度。更重要的是，运动保持版本在满足新约束的同时，能够保留原始运动的高频细节，这是单纯增加约束数量无法实现的。

### 4. 与 TwoStage 的关键差异总结

| 维度 | TwoStage (Qin et al. 2022) | SKEL‑Betweener |
|------|---------------------------|----------------|
| 输入模式 | 稠密上下文 + 固定结束帧 | 仅起止帧 + 任意稀疏中间约束 |
| 交互方式 | 预设约束时间线 | 任意时刻任意关节的即时约束 |
| 运动编辑 | 不支持 | 支持，且保持原始运动细节 |
| 用户界面 | 无 | 3D NMCs + 1D 曲线编辑器 |
| 推理速度 | 未报告 | 27 ms/frame（RTX3090），支持 24 FPS 实时播放 |

在 Lafan1 数据集的 OOD 约束测试中（Table 1），SKEL‑Betweener 的 L2P 误差为 0.032，显著低于 TwoStage，验证了稀疏约束范式在分布外泛化上的优势。

## 整体框架

![[assets/figures/papers/paper_list_l3_https_doi_org_10_1145_3687941/figures/003_Figure_3.jpg]]
*Figure 3: Our SKEL-Betweener architecture consists of a Joint Encoder that encodes joint ID, position encoding (PE) and transform for each joint independently. The input motion is then transformed with # = 18 Skeletal Transformer Layers that consist of a Multi-Head A!ention block using a!ention graph and a feed forward network. Finally, the output of the last transformer layer is decoded by the Joint Decoder to give dense positions, orientations and contacts*

SKEL‑Betweener 的 pipeline 围绕“从稀疏约束到稠密运动”这一核心流程构建。系统接收一组稀疏的时空控制点——即用户指定的若干关节在特定时刻的位置和朝向——作为输入，输出一段完整的、时序稠密的骨骼运动序列。

**输入预处理**：稀疏控制点首先通过线性插值（位置）和球面线性插值（朝向）被扩展为稠密的初始运动张量，包括位置张量 $\text{pos} \in \mathbb{R}^{T \times J \times 3}$ 和朝向张量 $\text{rot} \in \mathbb{R}^{T \times J \times 6}$。同时，为每一帧的足部关节生成接触标签：已知帧设为 0 或 1，未知帧统一设为 0.5，其余关节始终为 0，得到 $\text{contact} \in \mathbb{R}^{T \times J \times 1}$。这些稠密初始值与接触标签共同构成后续网络的输入。

**三大模块**：模型由三个顺序连接的模块组成（参见 Fig. 3）：

1. **Joint Encoder（关节编码器）**：对每个关节独立编码。将关节索引经线性嵌入得到 $J_{emb} \in \mathbb{R}^{1 \times J \times h'}$，时间帧经正弦位置编码得到 $T_{emb} \in \mathbb{R}^{T \times 1 \times h'}$，并与约束掩码等拼接形成节点嵌入 $\text{Node}_{emb} \in \mathbb{R}^{T \times J \times h}$。同时，输入的稠密运动张量经线性变换后与节点嵌入相加，作为后续 Transformer 的输入。

2. **Skeletal Transformer（骨骼 Transformer）**：由 18 层图 Transformer 层堆叠而成，在骨骼拓扑图上执行消息传递。每一层在时间维度上使用局部注意力机制，在空间维度上沿骨骼邻接关系聚合信息，逐步细化每一帧每一关节的隐表示。

3. **Joint Decoder（关节解码器）**：通过一个前馈网络从 Transformer 输出中同时解码出全局位置、全局朝向和接触标签。全局朝向随后按骨骼层级关系转换为局部朝向，以保持骨骼长度一致性。全局位置仅用于训练阶段的额外监督，推理时被丢弃，以避免因帧间骨长不一致导致的蒙皮网格伪影。

**推理流程**：推理时，用户只需提供首尾两帧姿态以及可选的任意中间约束点，系统先插值生成稠密初始运动，再经编码器‑Transformer‑解码器前向传播，输出满足约束的完整运动序列。模型在 RTX 3090 上的执行时间约为 27 ms，足以支持 Blender 中 24 FPS 的实时预览。

**运动编辑扩展**：在基础框架之上，SKEL‑Betweener 引入了一个运动保持版本（SKEL‑Betweener*）。该版本以一段已有的“基础运动”作为初始化（而非插值），并在损失函数中增加基础运动保持项 $\mathcal{L}_{BM}$，使模型在满足新约束的同时尽可能保留原始运动的高频细节。这一扩展使得 pipeline 可同时用于运动编辑任务，而不仅仅是两帧间的插值生成。

## 核心模块与公式推导

### 3.1 稀疏控制插值初始化

SKEL-Betweener 的推理起点是对用户提供的稀疏约束进行插值，生成稠密的初始运动序列。具体而言，对位置采用线性插值，对朝向采用球面插值，得到稠密的初始位置张量 $pos \in \mathbb{R}^{T \times J \times 3}$ 和朝向张量 $rot \in \mathbb{R}^{T \times J \times 6}$。

对于足部关节的接触标签，未知帧设为 0.5，其余关节始终设为 0，形成接触张量 $contact \in \mathbb{R}^{T \times J \times 1}$。

### 3.2 关节编码器

关节编码器对每个关节独立编码，将关节身份、时间位置和约束掩码融合为节点嵌入。关节嵌入通过独热编码的线性映射得到：

$$J_{emb} = W_{emb} \cdot 1_A([1, 2, \ldots, J]) \quad (\in \mathbb{R}^{1 \times J \times h'})$$

时间嵌入采用正弦位置编码：

$$T_{emb} = PE([1, 2, \ldots, T]) \quad (\in \mathbb{R}^{T \times 1 \times h'})$$

最终节点嵌入由关节嵌入、时间嵌入和约束掩码拼接而成：

$$Node_{emb} = [J_{emb}, T_{emb}, mask_*] \quad (\in \mathbb{R}^{T \times J \times h})$$

### 3.3 骨骼Transformer

骨骼Transformer 采用图神经网络架构，包含 18 层图 Transformer 层。每一层由多头注意力机制和图结构信息组成，在骨骼拓扑图上进行消息传递。该架构沿用了 Agrawal 等人（2023）的设计思路，并基于 Dwivedi 和 Bresson（2021）的图 Transformer 实现。

### 3.4 关节解码器

关节解码器通过前馈网络从骨骼Transformer的输出中提取三类信息：全局位置、全局朝向和接触标签。其中，全局朝向随后根据骨骼层级结构转换为局部朝向。全局位置仅用于训练阶段的额外监督，在推理时被丢弃——因为跨帧的骨骼长度可能不一致，直接使用会导致蒙皮网格产生伪影。

### 3.5 损失函数

**重建损失** 由位置损失和旋转损失两部分构成。位置损失采用全局位置的 L2 距离：

$$\mathcal{L}_{pos} = \left\| \widehat{pos_g} - pos_g \right\|_2$$

旋转损失同时约束局部朝向和全局朝向，使用测地线距离度量：

$$\mathcal{L}_{rot} = Geo(rot_l, \widehat{rot_l}) + Geo(rot_g, \widehat{rot_g})$$

其中测地线损失定义为旋转矩阵间的大圆弧角度：

$$Geo(R, \hat{R}) = \operatorname{arccos} \left[ \left( tr \left( \hat{R}^T R \right) - 1 \right) / 2 \right]$$

**运动编辑损失** 在重建损失基础上引入基础运动保持项，完整形式为：

$$\mathcal{L}_{ME} = \mathcal{L}_{SB} + \lambda_{BM} \cdot \mathcal{L}_{BM}$$

其中 $\mathcal{L}_{SB}$ 为 SKEL-Betweener 的基础损失，$\mathcal{L}_{BM}$ 为基础运动保持损失，$\lambda_{BM}$ 控制二者的相对权重。当基础运动与目标输出差异显著时，重建损失与基础运动保持损失呈对抗关系，需通过权重调节平衡约束满足与运动保真度。

## 实验与分析

### 主结果：稀疏约束下的运动生成

SKEL-Betweener 在稀疏、非均匀分布的关键帧约束下展现出显著优于 **TwoStage** 的泛化能力。Table 1 报告了三个数据集上的定量对比：在 Lafan1 的 OOD 约束条件下，SKEL-Betweener 的全局位置 L2 距离（L2P）为 **0.032**，远低于 TwoStage；在 AMASS 和 DanceDB 上，L2P 分别为 0.060 和 0.388。旋转误差（GeoR）方面，SKEL-Betweener 在 AMASS（0.045）和 DanceDB（0.044）的约束帧上也取得了更低的地测距离。定性结果（Fig. 4）进一步表明，TwoStage 在面对分布外约束时会产生不自然的扭曲或滑步，而 SKEL-Betweener 输出的运动曲线更平滑、更具物理合理性。

![[assets/figures/papers/paper_list_l3_https_doi_org_10_1145_3687941/figures/006_Table_1.jpg]]
*Table 1: #antitative analysis of SKEL-Betweener (Ours) and TwoStage models on Lafan1, AMASS and DanceDB datasets. L2P measures the L ^ { 2 } distance between the global positions and GeoR measures the geodesic distance between the global rotations*

### 消融实验：约束密度与基础运动保持

Table 2 揭示了约束密度对重建质量的影响。当不提供任何中间约束（0% 约束比）时，SKEL-Betweener 的 L2P 高达 0.302；将约束比提升至 15% 时，L2P 骤降至 0.015，与使用真值初始化的 SKEL-Betweener*（L2P = 0.015）持平。这表明模型仅需约 **15%–20% 的额外约束**即可实现接近真值的重建精度，大幅降低了用户的手动关键帧负担。

![[assets/figures/papers/paper_list_l3_https_doi_org_10_1145_3687941/figures/007_Table_2.jpg]]
*Table 2: Comparing motion reconstruction between our SKEL-Betweener model with di$erent ratios of constraints, and our SKEL-Betweener* model initialized with ground truth and no additional constraint*

基础运动保持损失（ $ \mathcal{L}_{BM} $ ）的作用在运动编辑任务中尤为关键。当基础运动与目标输出差异较大时，纯重建损失与基础运动保持损失形成对抗关系。随机选择基础运动片段的变体在重建和约束满足上均表现挣扎，验证了从同一运动序列中采样基础运动进行训练的必要性。

### 用户研究：Neural Motion Rig 的交互效率

Table 3 和 Fig. 6 展示了 3D 视口中 Neural Motion Rig（NMR）的实际可用性。在短跑和行走两个场景中，新手用户使用 NMR 平均仅需 **13.42** 和 **11.66** 个关键帧，显著少于传统逆向运动学（LIK）方法的 23.28 和 20.16 个关键帧。Fig. 6 的时间-误差曲线显示，NMR 的 L2P 误差始终低于 LIK 和 Mixamo Rig，且收敛速度更快。专业动画师的反馈同样偏好 NMR 的插值质量，认为其生成的中间帧更符合运动学规律。

![[assets/figures/papers/paper_list_l3_https_doi_org_10_1145_3687941/figures/010_Figure_6.jpg]]
*Figure 6: (a) Sprinting Scene (b) Walking Scene Fig. 6. User performance against the reference animation over time. For both scenes, the novice users and the authors are able to recreate the reference animation more accurately using NMR compared to LIK. Similarly, the professional artists are also faster using NMR compared to the Mixamo Rig*

![[assets/figures/papers/paper_list_l3_https_doi_org_10_1145_3687941/figures/008_Table_3.jpg]]
*Table 3: Average time taken, number of keyframes added, and final error to reference animation for novice users. Across the two scenes, the users need fewer keyframes and get closer using NMR compared to LIK*

### 推理效率与实时交互

模型在单块 RTX 3090 GPU 上的推理时间为 **27 ms**，支持 Blender 中以 24 FPS 的速率实时预览。这一延迟水平使得 Neural Motion Curves 可以作为交互式手柄直接嵌入 3D 视口和曲线编辑器，用户在拖动约束时能即时获得运动更新。

### 已知局限与失败模式

- **感受野限制**：由于采用局部注意力架构，模型的感受野仅随层数线性增长，在处理超长运动序列时可能无法捕捉远距离依赖。
- **约束精确性**：当前模型在约束帧上存在微小偏移，无法实现完全无损的约束满足，这在需要精确匹配的编辑场景中可能引入累积误差。
- **视觉混乱**：当 Neural Motion Curves 超过四条时，3D 视口中的控制手柄会显著遮挡场景，影响操作精度。
- **用户预期偏差**：添加新约束而不移动其位置时，模型仍可能改变整体运动，与“仅添加关键帧不应改变已有曲线”的用户直觉相悖。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_doi_org_10_1145_3687941/figures/002_Figure_2.jpg]]
*Figure 2: (c) Sparse Motion Editing Fig. 2. Input pa!erns of constraints (blue) for joints (vertical axis) over time (horizontal axis). In previous inbetweening models such as [Qin et al. 2022], a dense context and an end frame must be provided, as shown in (a). In addition partial or full constrained frames may be given. In contrast, our method (SKEL-Betweener) shown in (b) only requires two frames, and enables individual joint level controls. Lastly, we unlock motion editing via a motion-preservation bias, which is illustrated with so" blue in (c)*

## 方法谱系与知识库定位

### 与基线方法的关系

SKEL-Betweener 的核心对比基线是 **TwoStage**（Qin et al., 2022），该方法采用两阶段策略：先预测关节轨迹，再通过逆向运动学（IK）求解关节旋转。这一范式在运动内插（motion inbetweening）任务中具有代表性，但存在两个结构性瓶颈：

1. **约束模式僵化**：TwoStage 要求提供密集的上下文帧和明确的结束帧（Fig. 2a），无法处理稀疏、任意分布的中间约束。SKEL-Betweener 则仅需起始和结束两帧姿态，并可接受任意数量的中间约束（pink spheres），约束模式从“密集上下文+结束帧”变为“两端帧+稀疏中间点”（Fig. 2b-c）。
2. **IK 后处理引入误差**：TwoStage 将位置预测与旋转解耦，IK 求解步骤可能产生与原始运动动力学不一致的关节旋转。SKEL-Betweener 通过端到端的骨骼图网络同时预测全局位置和局部旋转，避免了这一解耦误差。

定量对比（Table 1）显示，在 Lafan1 数据集的分布外（OOD）约束条件下，SKEL-Betweener 的 L2P 达到 0.032，显著低于 TwoStage；在 AMASS 和 DanceDB 上同样保持优势（L2P 分别为 0.060 和 0.388，GeoR 分别为 0.045 和 0.044）。定性对比（Fig. 4）进一步表明，SKEL-Betweener 生成的神经运动曲线在关节级控制精度上优于 TwoStage。

### 方法架构定位

在骨骼运动生成的方法谱系中，SKEL-Betweener 处于**基于图神经网络的条件运动生成**分支。其架构由三部分构成（Fig. 3）：

- **关节编码器**：对关节 ID 进行线性嵌入，结合正弦位置编码和时间掩码，形成节点嵌入。
- **骨骼变换器**：采用 18 层图变换器层（graph transformer layers），参考了 Agrawal et al., 2023 的图网络设计和 Dwivedi & Bresson, 2021 的图变换器架构。
- **关节解码器**：通过前馈网络输出全局位置、全局旋转和接触标签，再将全局旋转按骨骼层级转换为局部旋转。

该架构的关键设计选择包括：
- **稀疏控制初始化**：使用线性和球面插值将稀疏约束初始化为密集运动序列（pos ∈ R^{T×J×3}, rot ∈ R^{T×J×6}），为网络提供合理的初始猜测。
- **接触标签处理**：对足部关节的未知帧设置接触标签为 0.5，其余关节始终为 0，形成 contact ∈ R^{T×J×1} 的辅助信号。
- **全局位置的双重角色**：训练时使用全局位置作为额外监督信号，但推理时丢弃，以避免骨骼长度不一致导致的蒙皮网格伪影。

### 运动编辑扩展

SKEL-Betweener 还衍生出一个运动保持版本（SKEL-Betweener*），用于运动编辑场景。其训练策略是：利用预训练的 SKEL-Betweener 模拟运动编辑过程，生成配对数据（Fig. 5），再通过组合损失函数训练运动保持模型：

$$\mathcal{L}_{ME} = \mathcal{L}_{SB} + \lambda_{BM} \mathcal{L}_{BM}$$

其中 $\mathcal{L}_{SB}$ 是基础重建损失，$\mathcal{L}_{BM}$ 是基础运动保持损失，$\lambda_{BM}$ 控制两者权重。当基础运动与目标输出差异较大时，重建损失与保持损失呈对抗关系，这是该方法的一个内在张力。

### 适用边界与局限

1. **感受野线性增长**：由于采用局部注意力架构，模型的感受野仅随时间线性增长。这意味着对于极长运动序列，远距离依赖关系的建模能力受限。
2. **约束数量与视觉杂乱**：超过四条神经运动曲线（NMC）时，3D 视口开始出现视觉杂乱，影响交互体验。
3. **非破坏性工作流**：约束满足存在一定偏移量，尚无法实现完全精确的非破坏性编辑。
4. **约束选择歧义**：当静止关节的约束在时间上重叠时，用户难以精确选择目标约束；添加约束而不移动时，预测结果的变化可能与用户预期不符。
5. **实时扩展性**：当前模型执行时间为 27 ms（RTX3090），支持 24 FPS 回放，但扩展到更长序列的实时控制仍需优化。

### 开放问题

- 如何为中间约束引入“影响范围”参数，使用户能控制约束的时间作用域？
- 如何改进 UI 设计，帮助用户识别每个控制球对应的精确时间步？
- 如何在保持实时性的前提下扩展模型以处理更长运动序列？
- 如何降低约束满足的偏移量，实现非破坏性编辑工作流？

## 原文 PDF

![[paperPDFs/TOG_2024/SKEL_Betweener_a_Neural_Motion_Rig_for_Interactive_Motion_Authoring.pdf]]
