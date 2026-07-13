---
title: "Complet4R: Geometric Complete 4D Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Complet4R_Geometric_Complete_4D_Reconstruction.pdf
project_link: null
code_link: null
aliases:
- Complet4R
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 通过引入聚合令牌（aggregation tokens）和全局Transformer架构，模型能够将其他帧的几何信息直接融合到目标时间戳，从而实现对遮挡区域的补全和时空一致的4D重建。
primary_logic: 将4D重建重新定义为一个基于全局聚合的补全任务：对于每一帧，利用所有其他帧的观测来补全被遮挡的几何区域，从而隐式地实现跨时间的一致性，无需显式的运动估计或逐对跟踪。
claims:
- 在4D完整重建基准上，Complet4R相比基线在Accuracy上获得约50%相对提升，Completion指标（Mean）实现数量级改进（2.67→0.26）。
- 消融实验验证了Focal-Weighted Point Loss、Endpoint聚合表示以及Concatenate聚合令牌三个设计选择的必要性，每个变体均使性能下降。
- 定性结果（Figure 4）表明，Complet4R能够成功补全在当前帧被遮挡但在其他帧可见的几何区域，而St4RTrack等基线仅能给出不完整的重建。
- SAIL-VOS 3D-test (4D Complete Reconstruction) 上 Accuracy Mean = 0.50
---

# Complet4R: Geometric Complete 4D Reconstruction

> [!tip] 核心洞察
> 将4D重建重新定义为一个基于全局聚合的补全任务：对于每一帧，利用所有其他帧的观测来补全被遮挡的几何区域，从而隐式地实现跨时间的一致性，无需显式的运动估计或逐对跟踪。

| 字段 | 内容 |
|------|------|
| 中文题名 | Complet4R：几何完整4D重建 |
| 英文题名 | Complet4R: Geometric Complete 4D Reconstruction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.27300) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | Complet4R |
| Dataset | SAIL-VOS 3D-test, Point Odyssey, Dynamic Replica |

> [!tip] 效果简介
> - SAIL-VOS 3D-test (4D Complete Reconstruction) 上，Accuracy Mean 0.50 vs 0.92 (St4RTrack-seq) (降低0.42（相对提升约45%）)；Completion Mean 0.26 vs 2.67 (St4RTrack-pairs) (降低2.41（数量级改进）)。
> - Point Odyssey (3D Point Tracking) 上，APD↑ 80.17 vs 68.72 (St4RTrack) (+11.45)；EPE↓ 16.07 vs 29.70 (St4RTrack) (-13.63)。
> - Dynamic Replica (3D Point Tracking) 上，APD↑ 80.65 vs 68.13 (St4RTrack) (+12.52)。

## 概要

从视频序列重建动态场景的完整三维几何是计算机视觉中的一项基本挑战。现有方法通常采用逐帧或逐对的局部推理策略，无法有效聚合整个时间序列的全局几何信息，导致被遮挡区域的重建不完整且缺乏时空一致性。Complet4R 将这一任务重新定义为**几何完整4D重建**（Geometric Complete 4D Reconstruction）——一个统一的补全与重建框架：对于每一帧，模型利用所有其他帧的观测来补全被遮挡的几何区域，从而隐式地实现跨时间的一致性，无需显式的运动估计或逐对跟踪。

Complet4R 的核心设计是一个基于解码器（decoder-only）的全局 Transformer 架构，通过引入专门的**聚合令牌**（aggregation tokens），使模型能够识别目标时间戳并将其他帧的几何信息直接融合到该时刻，输出包含遮挡区域的完整三维点图。该方法以静态重建模型 VGGT（Wang et al., CVPR 2025）为初始化基础，在其上新增聚合头（Aggregation head），并设计了 Focal-Weighted Point Loss 以加大对高误差区域的监督力度。

在 SAIL-VOS 3D-test 基准的 4D 完整重建任务上，Complet4R 相比基线 St4RTrack（Sucar et al., ICCV 2025）在 Accuracy Mean 上获得约 45% 相对提升（0.92 → 0.50），Completion Mean 实现数量级改进（2.67 → 0.26）。在 Point Odyssey 和 Dynamic Replica 的 3D 点跟踪任务上，APD 指标分别提升 11.45 和 12.52 个百分点。定性结果表明，Complet4R 能够成功补全在当前帧被遮挡但在其他帧可见的几何区域，而基线方法仅能给出不完整的重建。

### 从静态重建到动态世界的鸿沟

近年来，基于前馈神经网络的三维重建取得了显著进展。以 **VGGT**（Wang et al., CVPR 2025）为代表的方法能够从单张或少量图像中直接预测几何上一致的三维点图和相机参数，在静态场景上展现出令人瞩目的能力。然而，这些方法的核心假设——场景是静止的——使其在面对真实世界中无处不在的动态场景时，暴露出根本性的局限。

现实世界的视觉数据大多是动态的：视频序列中包含了运动的人物、移动的物体、变化的遮挡关系。当场景随时间演化时，任何单一帧都只能捕捉到部分可见的几何信息。被前景物体遮挡的区域、因视角变化而暂时不可见的结构，在逐帧独立重建的范式下，要么被留为空洞，要么被不可靠地猜测填充。这就引出了一个关键问题：**如何从视频序列中获得几何完整的四维重建？**

### 现有方法的瓶颈：局部推理与全局信息的缺失

针对动态场景，已有的探索主要沿着两条路径展开：**3D点跟踪**和**逐对/逐帧重建**。

3D点跟踪方法，如 **SpaTracker**（Xiao et al., CVPR 2024）和 **MonST3R**（Zhang et al., arXiv 2024），专注于追踪稀疏关键点在时空中的三维轨迹。它们能够刻画运动，但天然地放弃了稠密几何重建的目标，更无法处理被遮挡后重新出现的区域——因为跟踪本质上依赖于可见性，一旦点被遮挡，轨迹便可能中断或漂移。

逐帧或逐对重建方法，如 **St4RTrack**（Sucar et al., ICCV 2025），试图将静态重建模型扩展到视频输入，但它们在推理时仍然以局部窗口或成对帧为单位进行运算。这意味着，**每一帧的几何预测仅基于其自身或邻近帧的信息，无法有效聚合整个时间序列的全局几何上下文**。当目标帧中的某个区域被遮挡时，即使该区域在其他帧中清晰可见，这些方法也缺乏一个机制将远距离帧的观测信息“搬运”到目标时间戳。结果是，重建结果在遮挡区域不完整，且跨帧的几何一致性难以保证。

这种局部推理的局限性，构成了当前动态场景重建领域真正的瓶颈。

### 核心动机：将4D重建重新定义为全局聚合补全任务

Complet4R的出发点正是对这一瓶颈的突破。其核心洞察在于：**4D重建不应被视为逐帧重建的简单拼接，而应被重新定义为一个基于全局聚合的补全任务**。

具体而言，对于序列中的每一帧，模型应当能够“注视”所有其他帧的观测，将那些在当前帧被遮挡、但在其他帧可见的几何区域，直接聚合到目标时间戳的三维表示中。这并非显式地估计运动场或建立逐对对应关系，而是通过一个全局推理架构，隐式地实现跨时间的几何信息融合——从而在每一个时间戳，都输出一个包含完整几何（包括被遮挡区域）的三维点图。

这种视角的转换带来了两个关键优势：其一，**遮挡区域的补全变得自然且可解释**——被遮挡的结构只要在序列中某处可见，就能被聚合回来；其二，**时空一致性被隐式地保证**——因为所有帧的几何都来源于同一个全局上下文的聚合，而非独立预测后再进行后处理对齐。

### 技术挑战：如何实现全局时序聚合

将上述动机转化为可运行的模型，面临着一个核心的技术挑战：**如何设计一个架构，使其能够高效地在所有帧之间交换几何信息，并将信息精确地导向目标时间戳？**

这需要解决几个子问题：
1. **聚合目标的指定**：模型需要明确知道当前正在为哪一帧进行聚合，以便将其他帧的信息对齐到该帧的坐标系。
2. **跨帧信息流动**：需要一个机制，让每一帧的特征能够“看到”所有其他帧的特征，并在全局范围内进行信息融合。
3. **几何输出的对齐**：聚合后的几何表示必须与目标帧的相机姿态和场景状态保持一致，而非简单地混合不同时刻的观测。

Complet4R通过引入**聚合令牌**和**全局Transformer架构**来应对这些挑战，将4D重建从局部推理的局限中解放出来，迈向全局一致的几何完整重建。

## 核心方法与创新机理

Complet4R 的核心创新在于将“几何完整4D重建”重新定义为一个**全局聚合驱动的补全任务**，而非传统的逐帧或成对重建。其关键设计是让模型从整个视频序列中为每一帧聚合所有其他帧的几何信息，从而直接输出包含被遮挡区域的完整三维几何，无需显式的运动估计或帧间跟踪。这一思想通过以下四个关键槽位的改变得以实现：

### 任务定义：从局部重建到全局补全

现有方法（如 **VGGT** (Wang et al., CVPR 2025)）将任务视为静态三维重建，每个时间步独立预测可见点图；**St4RTrack** (Sucar et al., ICCV 2025) 等动态方法也仅进行成对对应或序列跟踪，不主动补全被遮挡的几何区域。Complet4R 将任务重新定义为：给定一段包含 $N$ 帧的视频序列 $\mathbf{I}_i \in \mathbb{R}^{3 \times H \times W}$，对于任意目标时间戳 $a$，预测每个输入帧 $i$ 在时刻 $a$ 的完整三维点图 $\mathbf{P}_i^a$，以及相机参数 $\mathbf{g}_i$ 和深度图 $\mathbf{D}_i$。这一统一映射可形式化为：

$$f \left( ( {\bf { I } } _ { i } ) _ { i = 0 } ^ { N - 1 } , a \right) = ( {\bf { P } } _ { i } ^ { a } , {\bf { g } } _ { i } , {\bf { D } } _ { i } ) _ { i = 0 } ^ { N - 1 }$$

这意味着，即使某一区域在当前帧被遮挡，只要它在其他帧可见，模型就能将其几何信息聚合到目标时间戳，实现“所见即所得”之外的完整重建。这一任务定义的转变是整个方法的核心瓶颈突破点：它使得模型能够隐式地利用跨帧的观测互补性来解决遮挡问题，而不依赖显式的运动场或光流。

### 时序聚合机制：聚合令牌与全局注意力

这是实现全局补全的核心技术手段。Complet4R 引入了**聚合令牌（Aggregation Tokens）**，分为两类：目标帧专用令牌和共享的其他帧令牌。这些令牌被拼接（Concatenate）到每帧的视觉令牌中，通过 decoder-only Transformer 的全局自注意力机制，使模型能够识别聚合目标时间戳，并引导所有帧的几何信息向目标帧流动。

与 VGGT 的逐帧独立推理不同，Complet4R 的全局注意力在帧级注意和全局注意两个阶段进行：帧级注意在每帧内部交换信息，全局注意则在所有帧之间进行跨帧交互。这一设计使得模型能够直接“看到”整个序列的几何上下文，从而在目标时间戳处输出完整的聚合点图。消融实验（Table 3）证实，聚合令牌采用拼接方式优于加法方式，在 Accuracy 和 Completion 指标上均更优。

### 预测头：新增聚合头

Complet4R 在 VGGT 已有的相机头（Camera Head）和深度头（Depth Head）基础上，新增了**聚合头（Aggregation Head）**。该头以各帧经过全局注意力更新后的特征为输入，预测各帧三维场景表示在目标时间戳下的位置。与仅预测当前帧可见几何的点头不同，聚合头输出的点图 $\mathbf{P}_i^a$ 融合了来自所有帧的信息，因此能够包含在当前帧被遮挡、但在其他帧可见的几何区域。聚合头与聚合令牌协同工作，共同构成了“跨帧聚合→目标帧输出”的完整信息通路。

### 点损失函数：Focal-Weighted Point Loss

为了强化模型对高误差区域的关注，Complet4R 提出了 **Focal-Weighted Point Loss**。其核心思想是根据预测误差的大小动态调整损失权重：

$$\mathbf { w } _ { i } ^ { a } = | \beta \mathbf { e } _ { i } ^ { a } | ^ { \gamma } , \qquad \mathbf { e } _ { i } ^ { a } = \hat { \mathbf { P } } _ { i } ^ { a } - \mathbf { P } _ { i } ^ { a }$$

其中 $\mathbf{e}_i^a$ 为预测点图与真值之间的对齐误差，$\beta$ 和 $\gamma$ 为超参数。误差越大的区域，权重越高，使得训练聚焦于对齐困难的部分——这恰好对应遮挡区域和动态区域，即完整重建任务中最关键的挑战所在。该权重与高斯不确定性加权相结合，构成完整的点损失函数：

$$\mathcal { L } _ { \mathrm { p o i n t } } = \displaystyle \sum _ { i = 1 } ^ { N } \Big ( \| \hat { \boldsymbol { \Sigma } } _ { i , a } ^ { P } \odot { \mathbf { w } } _ { i } ^ { a } \odot ( \hat { \mathbf { P } } _ { i } ^ { a } - { \mathbf { P } } _ { i } ^ { a } ) \| + \| \hat { \boldsymbol { \Sigma } } _ { i , a } ^ { P } \odot ( \nabla \hat { \mathbf { P } } _ { i } ^ { a } - \nabla { \mathbf { P } } _ { i } ^ { a } ) \| - \alpha \log \hat { \boldsymbol { \Sigma } } _ { i , a } ^ { P } \Big )$$

消融实验（Table 3）表明，Focal-Weighted Point Loss 在各项指标上全面优于仅加大动态点权重的 Dynamic-weighted Point Loss，验证了这一设计的必要性。同时，聚合表示采用直接预测目标时间戳的绝对坐标（Endpoint）优于预测相对偏移量（Offset），进一步证实了全局聚合框架下直接补全策略的有效性。

### 方法谱系与知识库定位

Complet4R 处于**视频驱动的稠密几何重建**与**时空补全**的交汇点。其视觉令牌化模块采用 **DINOv2** 作为冻结的特征提取器，Transformer 骨架继承自 **VGGT** (Wang et al., CVPR 2025) 的 decoder-only 架构并冻结其预训练权重，在此基础上新增聚合令牌、聚合头和 Focal-Weighted Point Loss。训练数据从 VGGT 的静态场景数据集（如 ScanNet）转向动态场景数据集 **Point Odyssey、Dynamic Replica、SAIL-VOS 3D**，以提供完整的动态三维轨迹和相机参数真值。

在4D完整重建任务上，Complet4R 显著超越 **St4RTrack**（序列模式和成对模式），在 SAIL-VOS 3D-test 上 Accuracy Mean 从 0.92 降至 0.50（相对提升约45%），Completion Mean 从 2.67 降至 0.26（数量级改进）。在3D点跟踪任务上，Complet4R 同样优于 **St4RTrack、MonST3R** (Zhang et al., arXiv 2024) 和 **SpaTracker** (Xiao et al., CVPR 2024)，在 Point Odyssey 上 APD 达到 80.17（+11.45），EPE 降至 16.07（-13.63）。

Complet4R 是一个基于解码器架构的全局 Transformer 框架，将几何完整 4D 重建形式化为统一的跨帧聚合补全任务。其核心设计理念是：对于任意目标时间戳，利用所有其他帧的观测信息，直接聚合出包含遮挡区域的完整三维几何表示，从而隐式实现时空一致性，无需显式的运动估计或逐对跟踪。

### 任务定义与输入输出

模型接收一段时序连续的 RGB 视频序列作为输入，并指定一个目标聚合时间戳 $a$。统一映射函数定义为：

$$f \left( ( {\bf { I } } _ { i } ) _ { i = 0 } ^ { N - 1 } , a \right) = ( {\bf { P } } _ { i } ^ { a } , {\bf { g } } _ { i } , {\bf { D } } _ { i } ) _ { i = 0 } ^ { N - 1 }$$

其中 $\mathbf{I}_i \in \mathbb{R}^{3 \times H \times W}$ 为第 $i$ 帧的 RGB 图像，$\mathbf{P}_i^a$ 表示在第 $i$ 帧视角下对齐至目标时间戳 $a$ 的聚合三维点图，$\mathbf{g}_i$ 为相机参数（内参与外参），$\mathbf{D}_i$ 为深度图。通过交替指定聚合目标时间戳 $a$，模型即可为每一帧输出完整的几何表示，构成时空一致的 4D 重建结果。

### 核心瓶颈与设计动机

现有方法通常采用逐帧或逐对的局部推理，无法有效聚合整个时间序列的全局几何信息，导致遮挡区域重建不完整且缺乏时空一致性。Complet4R 的关键洞察在于：将 4D 重建重新定义为全局聚合补全任务——对于每一帧，利用所有其他帧的观测来补全被遮挡的几何区域，从而隐式实现跨时间的一致性。

### Pipeline 模块关系

整体架构由以下核心模块串联构成（参见 Figure 3）：

1. **视觉令牌化**：采用 DINOv2 将每帧图像分割为 patch 并嵌入为视觉令牌序列。
2. **聚合令牌设计**：引入两类特殊的聚合令牌——目标帧专用令牌与非目标帧共享令牌，通过拼接方式注入令牌序列，使模型明确识别聚合目标时间戳并引导时序信息流动。
3. **相机与配准令牌**：继承自 VGGT（Wang et al., CVPR 2025）的设计，编码相机参数，并将各帧特征对齐到以首帧为参考的统一坐标系。
4. **全局 Transformer 处理**：解码器架构的 Transformer 在帧级注意和全局注意阶段通过自注意力机制交换时序信息，逐步将所有帧的特征向目标时间戳对齐。
5. **多任务预测头**：
   - **相机头**：从相机令牌直接预测相机参数。
   - **深度头**：从 patch 令牌预测每帧的深度图。
   - **聚合头**：新增的核心模块，输入各帧特征，预测对齐至目标时间戳的三维点图，输出完整的聚合点图 $\mathbf{P}_i^a$。

### 训练损失

训练总损失由三项加权组成：

$$\mathcal { L } = \lambda \mathcal { L } _ { \mathrm { p o i n t } } + \mathcal { L } _ { \mathrm { c a m e r a } } + \mathcal { L } _ { \mathrm { d e p t h } }$$

其中点损失 $\mathcal{L}_{\mathrm{point}}$ 采用新提出的 Focal-Weighted Point Loss，基于预测误差 $\mathbf{e}_i^a = \hat{\mathbf{P}}_i^a - \mathbf{P}_i^a$ 动态计算权重 $\mathbf{w}_i^a = |\beta \mathbf{e}_i^a|^\gamma$，加大高误差区域的监督力度，同时结合不确定性加权与梯度平滑约束。训练数据来自 Point Odyssey、Dynamic Replica 和 SAIL-VOS 3D 等动态场景数据集，提供完整的三维轨迹和相机参数真值。

### 关键设计选择

与基线方法相比，Complet4R 在以下关键维度进行了根本性改变：

- **任务定义**：从静态三维重建（每帧独立预测可见点图）转变为几何完整 4D 重建（跨帧聚合，补全遮挡区域）。
- **时序聚合机制**：从无跨帧聚合或仅成对对应，转变为通过聚合令牌和全局自注意力实现全帧时序聚合。
- **预测头**：在 VGGT 原有的 Point head 基础上新增 Aggregation head，专门负责跨帧几何对齐。
- **点损失函数**：从标准高斯不确定性加权 L2 损失升级为 Focal-Weighted Point Loss，聚焦于困难样本的优化。

### 问题形式化与统一映射

Complet4R将几何完整4D重建定义为一个统一的映射函数。给定一段包含 $N$ 帧的时间连续RGB图像序列 $\mathbf{I}_i \in \mathbb{R}^{3 \times H \times W}$（$i = 0, \dots, N-1$）以及目标聚合时间戳 $a$，模型输出三项结果：聚合至时间戳 $a$ 的三维点图 $\mathbf{P}_i^a$、相机参数 $\mathbf{g}_i$ 和深度图 $\mathbf{D}_i$。该映射可形式化为：

$$f \left( ( {\bf { I } } _ { i } ) _ { i = 0 } ^ { N - 1 } , a \right) = ( {\bf { P } } _ { i } ^ { a } , {\bf { g } } _ { i } , {\bf { D } } _ { i } ) _ { i = 0 } ^ { N - 1 }$$

这一形式化的核心在于：对于任意目标时间戳 $a$，模型从所有 $N$ 帧中聚合几何信息，为每一帧 $i$ 输出对齐到 $a$ 时刻坐标系的三维点图 $\mathbf{P}_i^a$。当 $a$ 遍历所有时间戳时，即获得时空一致的完整4D几何表示。

### 架构核心模块

Complet4R基于decoder-only Transformer架构，在冻结的**VGGT**（Wang et al., CVPR 2025）基础之上新增时序聚合能力。其关键模块如下：

**视觉令牌化**：每帧输入图像被分割为 $K$ 个patch，通过冻结的DINOv2编码器嵌入为视觉令牌序列，作为Transformer的基础输入单元。

**聚合令牌设计**：这是实现跨帧信息聚合的核心机制。系统引入两类特殊的聚合令牌——目标帧专用令牌与共享其他帧令牌。目标帧令牌标识当前聚合的目标时间戳，共享令牌则引导非目标帧的几何信息向目标帧流动。两类令牌通过**拼接**方式附加到各帧的视觉令牌序列中，使全局自注意力机制能够显式感知聚合方向。消融实验证实，拼接方式在Accuracy和Completion上均优于加法融合方式。

**相机令牌与配准令牌**：继承自VGGT的设计。相机令牌编码每帧的相机参数（内参与外参），配准令牌则将各帧特征逐步对齐到以首帧为参考的统一世界坐标系。这一对齐过程在Transformer的交替注意力阶段中隐式完成。

**全局Transformer注意力**：模型采用交替的帧级注意力和全局注意力阶段。在帧级阶段，各帧内部令牌进行自注意力；在全局阶段，所有帧的所有令牌（视觉令牌、聚合令牌、相机令牌、配准令牌）共同参与自注意力计算。通过多层迭代，其他帧的几何信息被逐步聚合到目标时间戳的表示中。

**预测头**：模型包含三个并行的预测头：
- **相机头**：从相机令牌直接回归相机参数。
- **深度头**：从patch令牌预测每帧的稠密深度图。
- **聚合头**：这是Complet4R的核心新增模块。它接收各帧经过全局Transformer处理后的特征，预测对应目标时间戳 $a$ 的三维点图 $\mathbf{P}_i^a$。聚合头直接输出端点坐标（Endpoint表示），而非预测相对偏移量——消融实验表明Endpoint表示在Completion指标上显著优于Offset表示。

### 关键公式与损失函数

训练总损失由点损失、相机损失和深度损失的加权和构成：

$$\mathcal { L } = \lambda \mathcal { L } _ { \mathrm { p o i n t } } + \mathcal { L } _ { \mathrm { c a m e r a } } + \mathcal { L } _ { \mathrm { d e p t h } }$$

其中 $\lambda$ 为点损失的权重系数。

**Focal-Weighted Point Loss** 是本文的核心损失设计。其动机在于：聚合点图中不同区域的预测难度差异显著，遮挡区域和动态区域的对齐误差通常远大于静态可见区域。为让训练聚焦于高误差区域，引入基于预测误差的Focal权重：

$$\mathbf { w } _ { i } ^ { a } = | \beta \mathbf { e } _ { i } ^ { a } | ^ { \gamma } , \qquad \mathbf { e } _ { i } ^ { a } = \hat { \mathbf { P } } _ { i } ^ { a } - \mathbf { P } _ { i } ^ { a }$$

其中 $\hat{\mathbf{P}}_i^a$ 为预测点图，$\mathbf{P}_i^a$ 为真值，$\mathbf{e}_i^a$ 为逐点误差向量。超参数 $\beta$ 控制缩放尺度，$\gamma$ 控制权重对误差的敏感度（$\gamma > 0$ 时高误差区域获得更大权重）。该权重与标准高斯不确定性加权结合，形成完整的点损失：

$$\mathcal { L } _ { \mathrm { p o i n t } } = \displaystyle \sum _ { i = 1 } ^ { N } \Big ( \| \hat { \boldsymbol { \Sigma } } _ { i , a } ^ { P } \odot { \mathbf { w } } _ { i } ^ { a } \odot ( \hat { \mathbf { P } } _ { i } ^ { a } - { \mathbf { P } } _ { i } ^ { a } ) \| + \| \hat { \boldsymbol { \Sigma } } _ { i , a } ^ { P } \odot ( \nabla \hat { \mathbf { P } } _ { i } ^ { a } - \nabla { \mathbf { P } } _ { i } ^ { a } ) \| - \alpha \log \hat { \boldsymbol { \Sigma } } _ { i , a } ^ { P } \Big )$$

该损失函数包含三项：第一项为Focal加权的位置误差，第二项为梯度一致性约束（保证预测点图的局部平滑性），第三项为不确定性正则化项（防止预测方差 $\hat{\boldsymbol{\Sigma}}_{i,a}^P$ 退化为零）。消融实验表明，Focal-Weighted Point Loss在各项指标上全面优于仅按动态/静态区域加权的Dynamic-weighted Point Loss。

### 训练数据与序列处理

训练数据来自三个动态场景数据集：Point Odyssey、Dynamic Replica和SAIL-VOS 3D，这些数据集提供完整的三维轨迹真值和相机参数。对于SAIL-VOS 3D中的长视频序列，模型通过检测深度突变（对应故事性视频中的镜头切换）将其分割为时间一致的短片段进行训练。

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2603_27300/figures/003_Figure_3.jpg]]
*Figure 3: Architecture Overview. By concatenating special aggregation tokens, Complet4R identifies the specific timestamp for aggregation. The Aggregation head then outputs the positions of 3D points from other views at this timestamp, aggregating 3D point maps across frames to form a complete geometric representation*

## 实验与关键发现

### 4D完整重建：主实验结果

Complet4R在SAIL-VOS 3D-test基准上的4D完整重建结果如Table 1所示。该任务评估模型从视频序列中为指定时间戳重建完整三维几何的能力，指标包括Accuracy（Acc.）、Completion（Complet.）与Normal Consistency（N.C.），均报告全部点上的Mean和Median。

与基线方法相比，Complet4R在所有指标上均取得显著领先。在Accuracy Mean上，Complet4R达到0.50，而**St4RTrack-seq**（Sucar et al., ICCV 2025）为0.92，相对提升约45%；在Completion Mean上，Complet4R为0.26，而**St4RTrack-pairs**（Sucar et al., ICCV 2025）为2.67，实现了数量级的改进（降低2.41）。这一巨大差距揭示了核心瓶颈所在：逐帧或逐对推理的基线方法无法有效聚合跨时间戳的几何信息，导致遮挡区域的Completion误差极高；而Complet4R通过全局聚合机制，将其他帧的观测直接融合到目标时间戳，从根本上解决了遮挡补全问题。

定性结果（Figure 4）进一步验证了这一结论。在红色椭圆标注的遮挡区域，Complet4R成功重建了完整的几何结构，而St4RTrack等基线仅能给出不完整或几何不一致的输出。这表明聚合令牌与全局Transformer的设计确实使模型能够从整个序列中“借用”被遮挡区域的几何信息。

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2603_27300/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative Results for 4D Complete Reconstruction. The first column shows the video inputs, with red boxes indicating the target aggregation timestamp for each sequence (Agg.: aggregation). The subsequent columns present the outputs of different models. Our method successfully reconstructs the complete geometry at the target timestamp highlighted by the red ellipses, whereas other methods produce incomplete or geometrically inconsistent reconstructions*

### 3D点跟踪：跨任务泛化能力

尽管Complet4R的设计目标是4D完整重建，其输出的聚合点图天然支持3D点跟踪任务。在Point Odyssey和Dynamic Replica两个数据集上（Table 2），Complet4R在APD↑和EPE↓两项指标上均显著超越现有方法。以Point Odyssey为例，Complet4R的APD达到80.17，EPE降至16.07，相比**St4RTrack**（APD 68.72, EPE 29.70）分别提升11.45和降低13.63。在Dynamic Replica上表现类似（APD 80.65 vs 68.13, EPE 15.99 vs 29.61）。

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2603_27300/figures/005_Table_2.jpg]]
*Table 2: World Coordinate 3D Point Tracking on Dynamic Points. We report both APD and EPE for four datasets: PO (Point Odyssey), DR (Dynamic Replica), ADT (Aria Digital Twin), and PStudio (Panoptic Studio). Best results are bold*

值得关注的是，这一优势并非来自专门的跟踪设计，而是聚合机制的自然副产品：当模型为每一帧聚合所有其他帧的几何信息时，同一三维点在不同时间戳下的位置已经隐式对齐，从而天然具备时空一致的跟踪能力。此外，在Aria Digital Twin和Panoptic Studio数据集上，Complet4R同样保持领先，表明其对不同场景类型具有较好的泛化性。

### 消融实验：关键设计选择验证

Table 3的消融实验系统验证了三个核心设计选择的有效性，所有实验均在SAIL-VOS 3D-test上进行。

**Focal-Weighted Point Loss vs. Dynamic-weighted Loss。** 变体（1）将Focal权重替换为仅加大动态点权重的Dynamic-weighted Point Loss。结果显示，Focal-Weighted版本在Accuracy和Completion上均更优。原因在于Focal权重基于预测误差的高次幂动态调整（$|\beta \mathbf{e}_i^a|^\gamma$），能够自适应地聚焦于对齐困难的区域，而非简单地按静态/动态类别分配固定权重。当场景中静态区域也存在较大重建误差时，Focal机制能更精细地分配监督信号。

**Endpoint vs. Offset聚合表示。** 变体（2）将聚合头的输出从绝对坐标（Endpoint）改为相对偏移量（Offset）。结果表明Endpoint表示在Completion指标上明显更优。直接预测目标时间戳的绝对三维坐标使模型能够利用全局坐标系中的几何先验，而偏移量预测则需要额外学习帧间变换关系，增加了优化难度。

**Concatenate vs. Add聚合令牌融合。** 变体（3）将聚合令牌与图像令牌的融合方式从拼接（Concatenate）改为加法（Add）。拼接方式在Accuracy和Completion上均表现更好。这是因为拼接保留了聚合令牌的独立通道，使模型能够显式地识别目标时间戳身份，而加法方式将聚合令牌信息与图像特征混合，削弱了时间戳标识的区分度。

### 失败模式与局限性

尽管Complet4R在主要基准上取得了显著提升，但仍存在若干值得关注的局限。

**计算复杂度与长序列扩展。** 由于采用全局自注意力机制，模型的运行时内存和计算量随帧数非线性增长。Table 7报告了不同序列长度下的推理时间与GPU内存消耗，表明当前设计难以直接应用于数百帧以上的长视频序列。这是全局Transformer架构的固有瓶颈，也是未来工作的重要方向——例如引入FlashAttention或稀疏注意力机制来降低计算开销。

**永久性遮挡区域无法补全。** Complet4R的核心假设是场景中所有区域至少在某帧中可被观测到。对于从未在任何帧中出现的永久性遮挡区域（如物体内部或被持续遮挡的背景），模型无法凭空生成几何信息。这是聚合范式的理论边界，而非工程缺陷。

**真实场景泛化待验证。** 训练数据主要来自Point Odyssey、Dynamic Replica和SAIL-VOS 3D等合成或受控动态场景。对于真实世界中复杂光照、剧烈运动或新物体突然出现等情况，模型的泛化能力尚未经过充分验证。这一局限在当前实验设置中未被直接评估，需要后续工作在真实视频基准上进行测试。

**动态拓扑变化建模。** 当场景中出现新物体或物体完全离开视野时，聚合令牌是否仍能保持时空一致性是一个开放问题。现有框架假设场景几何在时间维度上是连续可追踪的，尚未显式建模拓扑变化。

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2603_27300/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative Results for 3D Dynamic Point Tracking. The first column shows the input images; the second and third columns display the tracking trajectories produced by our method at successive time steps. The smooth trajectories demonstrate strong spatiotemporal geometric consistency*

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2603_27300/figures/014_Figure_6.jpg]]
*Figure 6: More Qualitative Results for 4D Complete Reconstruction. The first column shows the video inputs, with red boxes indicating the target aggregation timestamp for each sequence (Agg.: aggregation). The subsequent columns present the outputs of different models. Our method successfully reconstructs the complete geometry at the target timestamp highlighted by the red ellipses, whereas other methods produce incomplete or geometrically inconsistent reconstructions*

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2603_27300/figures/016_Figure_7.jpg]]
*Figure 7: Comparison with DreamScene4D. The left shows the video inputs, while the right presents the reconstruction results: (a) from DreamScene4D, and (b) from our method. Our approach demonstrates higher reconstruction quality*

## 定位与知识库关联

### 任务定义的范式转换

Complet4R 的核心贡献在于将4D动态场景重建从一个**逐帧/逐对局部推理问题**重新定义为**全局聚合补全问题**。传统方法，如 **St4RTrack** (Sucar et al., ICCV 2025) 和 **MonST3R** (Zhang et al., arXiv 2024)，通常以成对对应或滑动窗口的方式处理时序信息，这导致它们在面对遮挡区域时只能给出不完整的几何输出——被遮挡的部分在当前帧中不可见，而模型缺乏从其他帧“借用”几何信息的机制。Complet4R 通过引入聚合令牌和全局Transformer架构，使模型能够将所有帧的观测显式地融合到目标时间戳，从而在概念层面实现了从“局部重建”到“全局补全”的范式跃迁。

这一范式转换的直接后果是：模型不再需要显式的运动估计、光流或逐对对应关系。聚合过程本身隐式地编码了跨时间的几何一致性，使得遮挡区域的补全成为全局上下文推理的自然产物，而非后处理步骤。

### 与基线方法的关系网络

#### 直接基线与架构继承

Complet4R 在架构层面直接继承自 **VGGT** (Wang et al., CVPR 2025)，后者是一个面向静态场景的decoder-only Transformer重建框架。具体继承关系体现在：

- **视觉令牌化**：沿用DINOv2作为图像编码器，将每帧分割为patch并嵌入为视觉令牌。
- **相机令牌与配准令牌**：继承了VGGT的相机参数编码方案，以及将各帧特征对齐到统一坐标系（以首帧为参考）的配准机制。
- **深度头与相机头**：直接复用VGGT的预测头设计，用于输出每帧的深度图和相机参数。

关键差异在于 Complet4R 新增了两个核心组件：**聚合令牌**（Aggregation Tokens）和**聚合头**（Aggregation Head）。聚合令牌分为目标帧专用令牌和非目标帧共享令牌两类，通过拼接方式融入图像令牌序列，使模型在全局自注意力阶段能够识别聚合目标时间戳并引导时序信息流动。聚合头则从各帧特征预测对齐到目标时间戳的三维点图，输出完整的聚合点图——这是VGGT所不具备的跨帧补全能力。

#### 与动态场景方法的对比

在动态场景重建领域，Complet4R 与以下方法构成直接对比关系：

- **St4RTrack** (Sucar et al., ICCV 2025)：作为4D完整重建和3D点跟踪的主要基线，St4RTrack 提供序列模式（seq）和成对模式（pairs）两种变体。在SAIL-VOS 3D-test基准上，Complet4R 的Accuracy Mean达到0.50，相比St4RTrack-seq的0.92降低约45%（该指标越低越好）；Completion Mean更是从St4RTrack-pairs的2.67降至0.26，实现了数量级改进。定性结果（Figure 4）直观展示了这一差距：St4RTrack输出中，被遮挡区域呈现空洞或不一致几何，而Complet4R成功补全了这些区域。

- **MonST3R** (Zhang et al., arXiv 2024)：同为动态场景重建方法，但在3D点跟踪任务上，Complet4R在Point Odyssey数据集上APD达到80.17（MonST3R未直接出现在Table 2的主对比中，但作为领域代表性工作被引用）。

- **SpaTracker** (Xiao et al., CVPR 2024) 和 **SpatialTrackerV2**：这两类方法仅支持稀疏点跟踪，不预测遮挡区域且缺乏稠密重建能力。作者明确指出将它们纳入4D完整重建对比并不公平，因此仅在3D点跟踪评估中作为基线出现。

#### 与静态重建方法的边界

Complet4R 与静态场景重建方法（如VGGT、DUSt3R等）的根本区别在于训练数据和任务目标：静态方法假设场景几何不变，而Complet4R专门针对动态场景设计，训练数据来自Point Odyssey、Dynamic Replica和SAIL-VOS 3D等动态数据集。这些数据集提供完整的三维轨迹和相机参数，使模型能够学习跨时间的几何聚合。

### 适用边界与局限

#### 计算复杂度的非线性增长

Complet4R 采用全局自注意力机制，所有帧的令牌在Transformer中进行全连接交互。这带来了一个根本性的效率瓶颈：**运行时内存和计算量随帧数非线性增长**。Table 7的系统效率数据显示，随着序列长度增加，推理时间和GPU内存消耗快速攀升。这使得方法难以直接应用于数百帧以上的长视频序列，限制了其在需要实时处理或超长时序场景中的部署。

#### 训练数据分布的局限

当前训练数据主要来自合成或受控动态场景（Point Odyssey为合成数据，Dynamic Replica为室内受控场景，SAIL-VOS 3D为叙事性视频片段）。对于真实世界中复杂光照、剧烈运动模糊、新物体突然出现或消失等情况，模型的泛化能力尚未经过充分验证。这是一个需要人工核实的具体风险点——论文未提供在完全野外（in-the-wild）视频上的系统评估。

#### 永久性遮挡的不可补全性

Complet4R 的核心假设是：场景中所有区域至少在某帧中被观测到。对于从未在任何帧中出现的永久性遮挡区域（如物体内部、始终被遮挡的背面），模型无法进行补全。这是聚合机制的固有上限，而非模型设计的缺陷——任何基于可见观测的方法都面临这一限制。

#### 动态拓扑变化的处理

当场景中出现新物体或物体离开视野时，聚合令牌是否仍能保持时空一致性是一个开放问题。论文未专门讨论动态拓扑变化下的模型行为，这一点需要人工验证。

### 开放问题与未来方向

1. **线性复杂度替代方案**：如何将推理复杂度从非线性降至近似线性，以支持超长视频的实时4D重建？可能的路径包括引入FlashAttention、稀疏注意力机制或基于记忆的状态空间模型。

2. **Focal-Weighted Loss的自适应调参**：Focal-Weighted Point Loss中的超参数 $\beta$ 和 $\gamma$ 对不同动态程度的场景需要如何自适应调整？当前采用固定值，但场景的运动幅度和遮挡程度差异显著，自适应机制可能进一步提升性能。

3. **动态拓扑建模**：当场景中出现新物体或物体离开视野时，聚合令牌的机制是否仍然有效？可能需要引入显式的物体出现/消失检测模块，或设计支持动态令牌数量的架构变体。

4. **与生成式方法的融合**：Figure 7将Complet4R与**DreamScene4D**进行了定性对比，展示了更高的重建质量。但DreamScene4D代表了一类基于生成先验的4D重建方法，Complet4R的纯几何聚合思路是否能与生成式先验互补，是一个值得探索的方向。

5. **多模态扩展**：当前方法仅依赖RGB输入，未来可考虑融合深度传感器、IMU等多模态信号，以增强在纹理缺失或光照极端场景下的鲁棒性。

## 原文 PDF

![[paperPDFs/CVPR_2026/Complet4R_Geometric_Complete_4D_Reconstruction.pdf]]
