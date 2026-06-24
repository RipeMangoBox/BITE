---
title: "MASt3R-SfM: a Fully-Integrated Solution for Unconstrained Structure-from-Motion"
type: paper
paper_level: A
venue: 3DV
year: 2025
pdf_ref: paperPDFs/3DV_2025/MASt3R_SfM_a_Fully_Integrated_Solution_for_Unconstrained_Structure_from_Motion.pdf
aliases:
- MS
- MASt3R-SfM
tags:
- 3DV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "利用MASt3R作为冻结的3D视觉基础模型，同时输出局部3D重建和密集像素匹配，并复用其编码器进行高效的图像检索（ASMK），将匹配复杂度从O(N²)降至O(N)。通过两阶段梯度下降（基于稀疏匹配的3D粗对齐 + 基于2D重投影的细化）实现无需RANSAC的全局优化。"
primary_logic: "通过复用MASt3R分词编码器以近乎零开销进行检索并构建稀疏场景图，保证了整个SfM管道的线性复杂度；同时粗到细的全局优化（3D点到3D点损失 + 2D重投影损失）无需昂贵的RANSAC且能处理纯旋转。"
claims:
- "在T&T数据集上，从25视图到全视图，MASt3R-SfM的ATE始终低于所有竞争对手（如25视图ATE=0.03360，COLMAP=0.03840；全视图ATE=0.01060，Ace-Zero=0.01520），且注册率保持100%。"
- "在CO3Dv2上，随着输入视图数量减少，MASt3R-SfM的相对旋转和相对平移精度（RRA、RTA）几乎恒定，而其他方法急剧下降。"
- "在T&T-200子集上，检索式场景图（Keyframes+kNN）的ATE为0.01243，仅略逊于全图（0.01256），但所需边数从O(N²)减少到O(N)，带来10倍加速。"
- "在ETH3D上，MASt3R-SfM的平均RRA@5=81.2，RTA@5=79.7，大幅超越COLMAP、VGGSfM、FlowMap等所有对比方法。"
---

# MASt3R-SfM: a Fully-Integrated Solution for Unconstrained Structure-from-Motion

> [!tip] 核心洞察
> 通过复用MASt3R分词编码器以近乎零开销进行检索并构建稀疏场景图，保证了整个SfM管道的线性复杂度；同时粗到细的全局优化（3D点到3D点损失 + 2D重投影损失）无需昂贵的RANSAC且能处理纯旋转。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MASt3R-SfM：面向无约束运动恢复结构的全集成解决方案 |
| 英文题名 | MASt3R-SfM: a Fully-Integrated Solution for Unconstrained Structure-from-Motion |
| 会议/期刊 | 3DV 2025 |
| Links | [paper](https://arxiv.org/abs/2409.19152); [GitHub](https://github.com/naver/mast3r) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MASt3R-SfM |
| Dataset | Tanks&Temples (25 views subset), Tanks&Temples (full set), MIP-360, CO3Dv2 (10 random frames) |

> [!tip] 效果简介
> - Tanks&Temples (25 views subset) 上，ATE ↓ 为 0.03360，对比 0.03840 (COLMAP)，变化 相对降低12.5%。
> - Tanks&Temples (full set) 上，ATE ↓ 为 0.01060，对比 0.01520 (ACE-Zero)，变化 相对降低30.3%。
> - MIP-360 上，ATE ↓ 为 0.00079，对比 0.00089 (FlowMap)，变化 相对降低11.2%。

## 概述

运动恢复结构（Structure-from-Motion, SfM）旨在从无序图像集合中同时恢复相机姿态与三维场景结构。传统SfM流水线（如 **COLMAP**, Schönberger et al., CVPR 2016）依赖关键点提取、特征匹配、RANSAC外点剔除与增量式光束平差（Bundle Adjustment, BA）的级联模块，在图像重叠不足、视图稀少或纯旋转（无平移运动）等无约束条件下极易崩溃，且计算复杂度随图像数量呈超线性增长，可扩展性受限。

近期基于学习的稠密方法，如 **DUSt3R**，虽大幅简化了流程，但其全局对齐采用所有图像对穷举的二次方复杂度，精度有限且难以处理大规模场景。**MASt3R-SfM** 针对上述瓶颈提出了一套全集成、训练自由的SfM解决方案，核心思想可概括为三点：

1. **复用冻结的MASt3R编码器实现高效检索**：将MASt3R的分词编码器特征通过ASMK（Aggregated Selective Match Kernels）聚合，以近乎零额外开销进行图像检索，构建稀疏场景图，将匹配复杂度从 $O(N^2)$ 降至 $O(N)$。
2. **两阶段梯度下降替代RANSAC**：粗对齐阶段在3D空间最小化稀疏匹配点的欧氏距离，细化阶段基于2D重投影误差联合优化相机位姿、尺度与深度，全程无需昂贵的RANSAC。
3. **纯旋转场景的稳定处理**：通过冻结规范深度图并禁用锚点深度优化，使方法在无平移运动时仍能稳定工作，填补了传统SfM的关键空白。

实验表明，MASt3R-SfM在多个基准上实现了最优性能：在Tanks&Temples全视图集上ATE为0.01060，较 **ACE-Zero**（Brachmann et al., ECCV 2024）相对降低30.3%；在CO3Dv2上，即使视图数量大幅减少，相对旋转与平移精度几乎恒定；在ETH3D上平均RRA@5达81.2、RTA@5达79.7，大幅超越 **COLMAP**、**VGGSfM**（Wang et al., CVPR 2024）、**FlowMap**（Smith et al., ECCV 2024）等所有对比方法。消融实验证实，检索式稀疏场景图在保持精度的同时带来约10倍加速，而相机再参数化与运动学链设计对姿态精度有决定性贡献。

**方法定位**：MASt3R-SfM属于基于学习的稠密SfM方法，但区别于端到端可微分SfM（如VGGSfM）或场景坐标回归方法（如ACE-Zero），它完全训练自由，仅依赖冻结的MASt3R预训练模型，兼具传统几何优化的可解释性与深度学习的前端鲁棒性。

## 背景与动机

运动恢复结构（Structure-from-Motion, SfM）旨在从无序图像集合中同时恢复相机姿态和场景三维结构，是三维视觉与具身智能的基础模块。然而，传统SfM流水线面临一个根本性瓶颈：其依赖的模块级联架构——关键点提取、特征匹配、几何验证、增量式光束平差——在图像重叠不足、视图极度稀疏或相机仅发生纯旋转时极易崩溃，且计算复杂度随图像数量急剧膨胀，可扩展性受限。

这一瓶颈的因果根源在于传统流水线对各模块的脆弱依赖。关键点检测器在低纹理或重复纹理区域失效；RANSAC需要足够的正确匹配才能估计几何关系；增量式重建一旦在早期阶段引入错误便难以恢复。近期方法尝试从不同角度突破这些限制：**COLMAP**（Schönberger et al., CVPR 2016）作为经典增量SfM代表，精度高但速度慢且对初始条件敏感；**VGGSfM**（Wang et al., CVPR 2024）引入端到端可微分框架，但在极稀疏视图下性能急剧下降；**FlowMap**（Smith et al., ECCV 2024）和**ACE-Zero**（Brachmann et al., ECCV 2024）分别通过梯度下降与测试时训练改进流程，但仍未根本解决计算复杂度和纯旋转失效问题。

一个关键的范式转变来自DUSt3R——它用单一的视觉Transformer直接回归成对图像的点图，大幅简化了匹配与重建流程。然而，DUSt3R的全局对齐策略存在两个致命缺陷：其一，对所有图像对穷举计算，复杂度为$O(N^2)$，无法处理大规模场景；其二，全局对齐精度不足，在困难条件下表现脆弱。这暴露了当前方法的核心矛盾：**如何在不牺牲精度的前提下，将SfM的计算复杂度从二次方降至线性，并使其在纯旋转等极端条件下仍能稳定工作？**

MASt3R-SfM正是在这一矛盾中找到了因果操纵点。其核心洞察是：MASt3R作为冻结的3D视觉基础模型，不仅能输出局部重建和密集匹配，其编码器产生的分词特征还可以被“劫持”用于近乎零开销的图像检索。通过复用同一编码器构建稀疏场景图，匹配复杂度从$O(N^2)$降至$O(N)$；同时，粗到细的两阶段梯度下降优化——先在3D空间对齐稀疏匹配点，再通过2D重投影误差细化——无需昂贵的RANSAC即可实现全局一致的相机姿态估计。整个流水线完全训练自由，仅需一个现成的MASt3R检查点。

这一设计的决定性优势在多项实验中得到了验证：在CO3Dv2数据集上，当输入视图数量从数十帧降至数帧时，MASt3R-SfM的相对旋转精度（RRA）和相对平移精度（RTA）几乎保持恒定，而其他方法急剧下降（Figure 1）；在Tanks&Temples全视图集上，其ATE达到0.01060，相对ACE-Zero降低30.3%（Table 1）；在ETH3D上，平均RRA@5=81.2、RTA@5=79.7，大幅超越所有对比方法（Table 3）。更重要的是，该方法在传统SfM完全失效的纯旋转场景下仍能输出有效重建，填补了领域内长期存在的空白。

## 核心创新

MASt3R-SfM 的核心创新并非提出新的学习范式，而是**将冻结的 MASt3R 3D 视觉基础模型重新编排为一个完整的、无需训练的 SfM 流水线**，并通过四项关键设计（changed slots）从根本上突破了传统 SfM 在无约束条件下的瓶颈。

### 创新一：编码器复用与线性复杂度的场景图构建

传统 SfM 依赖独立的检索器（如 NetVLAD）进行图像匹配对选择，而 DUSt3R 等端到端方法则采用全对穷举，匹配复杂度为 $O(N^2)$，严重限制可扩展性。MASt3R-SfM 的关键洞察是：**MASt3R 的冻结编码器本身已产生富含几何信息的局部特征（token features），可被直接“劫持”用于图像检索，几乎零额外计算开销**。

具体而言，方法将编码器输出的分词特征通过 ASMK（Aggregated Selective Match Kernels）聚合为全局描述子，无需任何训练或微调。基于这些描述子，采用最远点采样（FPS）选取 $N_a$ 个关键帧构建稠密连接的骨干图，其余图像仅连接到最近的 $k$ 个非关键帧和最近的关键帧。由此，场景图的边数从 $O(N^2)$ 降至 $O(N)$，在 T&T-200 子集上实现了约 10 倍加速，而 ATE 仅从 0.01256 轻微升高至 0.01243（Table 4）。这一设计使 MASt3R-SfM 成为首个具有准线性复杂度的全集成 SfM 方法。

### 创新二：稀疏匹配驱动的两阶段全局优化替代 RANSAC

DUSt3R 的全局对齐对所有密集点图施加刚性相似变换，计算代价高且缺乏显式对应约束。MASt3R-SfM 转而利用 MASt3R 解码器同时输出的**快速最近邻稀疏匹配**（FastNN），将优化变量大幅缩减，并采用两阶段梯度下降替代传统的 RANSAC+BA 级联：

1. **粗对齐（3D 损失）**：固定规范深度和内参，仅对置信度加权的稀疏匹配点最小化 3D 欧氏距离（式 3），在全局坐标系中快速对齐所有局部点云。该阶段使用 Adam 优化器，$\lambda_1=1.5$，300 次迭代。
2. **细化（2D 重投影损失）**：在粗对齐基础上，构建锚点网格（间距 $\delta$）形成伪轨迹，联合优化相机位姿、尺度、锚点深度和共享焦距，最小化所有稀疏对应的鲁棒 2D 重投影误差（式 4）。该阶段本质上是一种**可微分的类 BA 过程**，$\lambda_2=0.5$，300 次迭代。

消融实验（Table 5）表明：仅粗对齐（类似 DUSt3R 全局对齐）ATE 为 0.01504，加入细化后降至 0.01243；若细化时不优化深度，ATE 为 0.01315，仍优于仅粗对齐。这证明了两阶段优化中，粗对齐提供了可靠的初始位姿，而 2D 重投影细化则显著提升了精度。

### 创新三：规范相机再参数化与运动学链解耦

传统位姿参数化中，旋转与平移高度耦合，导致梯度下降优化困难。MASt3R-SfM 引入两项关键再参数化（Table 11）：

- **规范相机变换**：将相机旋转中心沿 Z 轴平移到中值深度平面（式 8），有效解除旋转与平移的相互干扰。该变换使 ATE 从 0.01445 降至 0.01243，RTA@5 从 56.0 跃升至 70.9。
- **运动学链传播**：通过基于匹配数目的层次聚类构建树形连接结构，将绝对姿态转化为相对姿态参数（式 9），沿树逐层传播。相比星型树（ATE 0.02013），平衡的运动学链（ATE 0.01243）显著减少了参数优化中的不一致性。

### 创新四：纯旋转场景的显式处理

传统 SfM 在缺少平移运动时因三角测量失效而崩溃。MASt3R-SfM 通过**冻结规范深度图并禁用锚点深度优化**，使方法在纯旋转场景下也能稳定工作。在 InLoc 数据集的 20 个纯旋转场景上，MASt3R-SfM 实现了 100% 的相对旋转精度（RRA@5），而 COLMAP、VGGSfM 等所有对比方法完全失效（Table 8）。这一能力将 SfM 的适用范围从需要充分平移运动的场景拓展到了完全无约束的图像集合。

### 创新总结

上述四项 changed slots 形成了完整的因果链条：编码器复用使流水线可扩展至大规模场景（$O(N)$ 复杂度）；稀疏匹配与两阶段优化消除了对 RANSAC 的依赖，同时保持了全局一致性；再参数化与运动学链解决了位姿优化中的耦合问题；纯旋转处理策略则填补了传统 SfM 的关键能力空白。整个流水线完全训练自由，仅依赖一个现成的 MASt3R 检查点，却能在 T&T、CO3Dv2、ETH3D 等多个基准上以显著优势超越 COLMAP、VGGSfM、FlowMap、ACE-Zero 等强基线。

## 整体框架

![[assets/figures/papers/paper_list_l9_MASt3R_SfM_a_Fully_Integrated_Solution_for_Unconstrained_Structure_from/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed MASt3R-SfM method. Given an unconstrained image collections, possibly small (1 image) or large (> 1000 images), we start by computing a sparse scene graph using efficient image retrieval techniques given a frozen MASt3R’s per-image features. We then compute local 3D reconstruction and matches for each edge using again a frozen MASt3R’s decoder. Global optimization proceeds with gradient descent of a matching loss in 3D space, followed by refinement in terms of 2D reprojection error*

MASt3R-SfM 是一个面向无约束图像集合的全集成运动恢复结构（SfM）流水线，整个流程完全免训练，仅依赖一个冻结的 MASt3R 预训练模型。其核心设计思路是将传统 SfM 中相互解耦的模块——图像检索、匹配、位姿估计、三角测量与光束法平差——统一为四个紧密衔接的阶段，如图 Figure 2 所示。

### 流水线四阶段

**阶段一：稀疏场景图构建。** 给定一组无约束输入图像（可从单张到上千张），系统首先利用 MASt3R 的冻结编码器提取每张图像的 token 级特征，并采用 ASMK（Aggregated Selective Match Kernels）聚合方法进行免训练的高效图像检索。通过最远点采样（FPS）选取固定数量 $N_a$ 的关键帧（keyframes），将其全连接构成核心图，再将每张非关键帧图像连接到最近的关键帧及 $k$ 个最近邻非关键帧。这一策略将匹配边数从 $O(N^2)$ 降至 $O(N)$，使整个流水线具备准线性复杂度。

**阶段二：局部重建与匹配。** 对场景图 $\mathcal{G} = (\mathcal{V}, \mathcal{E})$ 中的每条边 $(n, m) \in \mathcal{E}$，调用 MASt3R 的冻结解码器，同时输出成对的规范点图（canonical pointmaps）和快速最近邻稀疏匹配（FastNN）。每个像素的规范 3D 坐标由所有相连边估计的置信度加权平均聚合得到：

$$\tilde{X}_{i,j}^n = \frac{\sum_{e \in \mathcal{E}^n} C_{i,j}^{n,e} X_{i,j}^{n,e}}{\sum_{e \in \mathcal{E}^n} C_{i,j}^{n,e}}$$

随后通过 Weiszfeld 算法从规范点图恢复焦距，并构建严格满足针孔投影模型的约束点图 $\chi^n$。这一阶段为后续优化提供了冻结的局部 3D 几何和稀疏对应关系。

**阶段三：粗对齐（3D 损失）。** 固定规范深度和内参，仅优化每张图像的相似变换参数（尺度 $\sigma_n$ 与刚体姿态 $P_n$），通过最小化所有稀疏匹配点在全局坐标系下的 3D 欧氏距离来对齐所有点云：

$$\sigma^*, P^* = \underset{\sigma, P}{\arg\min} \sum_{c \in \mathcal{M}^{n,m} \atop (n,m) \in \mathcal{E}} q_c \left\| \chi_c^n - \chi_c^m \right\|^{\lambda_1}$$

该阶段使用 Adam 优化器，迭代约 300 次，为后续细化提供良好的初始位姿。

**阶段四：细化（2D 重投影损失）。** 在粗对齐基础上，引入锚点网格（anchor grid）将密集像素深度变量压缩为稀疏锚点深度，形成伪轨迹。联合优化相机内参 $K_n$、位姿 $P_n$、尺度 $\sigma_n$ 及锚点深度 $Z$，最小化类光束法平差的 2D 重投影误差：

$$\mathcal{L}_2 = \sum_{c \in \mathcal{M}^{n,m} \atop (n,m) \in \mathcal{E}} q_c \left[ \rho( y_c^n - \pi_n( \chi_c^m ) ) + \rho( y_c^m - \pi_m( \chi_c^n ) ) \right]$$

其中 $\rho$ 为鲁棒范数。此阶段通过运动学链（kinematic chain）将绝对姿态转化为相对姿态参数，并采用规范相机变换将旋转中心平移到中值深度平面，有效解除旋转与平移的参数耦合。

### 关键设计决策

整个流水线有三个关键设计使 MASt3R-SfM 区别于现有方法：

1. **编码器复用**：图像检索与局部重建共享同一个冻结编码器，几乎零额外计算开销，避免了独立检索器（如 NetVLAD）的冗余。
2. **两阶段梯度下降**：粗对齐提供全局一致的初始解，细化则通过 2D 重投影损失精调，整个过程无需 RANSAC 等随机采样机制。
3. **纯旋转处理**：在检测到无平移运动的场景时，冻结规范深度图并禁用锚点深度优化，使方法在传统 SfM 完全失效的纯旋转条件下仍能稳定工作。

消融实验证实了各阶段的必要性：仅粗对齐（类似 DUSt3R 全局对齐）的 ATE 为 0.01504，加入细化后降至 0.01243；细化若从随机初始化出发则无法收敛，说明粗对齐提供的初始解对非凸的类 BA 优化至关重要（Table 5）。

## 核心模块与公式推导

MASt3R-SfM 的核心架构由四个顺序模块构成：场景图构建、局部重建与匹配、粗对齐（3D损失）、细化（2D重投影损失）。其关键创新在于将 MASt3R 冻结编码器复用为图像检索器，从而将匹配复杂度从 $O(N^2)$ 降至 $O(N)$，并通过两阶段梯度下降实现无需 RANSAC 的全局优化。

### 场景图构建

给定无约束图像集合，系统首先利用 MASt3R 的冻结编码器提取每张图像的分词（token）特征，再通过 ASMK（Aggregated Selective Match Kernels）方法进行训练自由的图像检索。基于检索相似度，采用最远点采样（FPS）选出 $N_a$ 张关键图像构成核心节点集并全连接，其余图像仅与其最近的关键图像及 $k$ 个最近邻非关键图像相连。该策略构建的稀疏场景图 $\mathcal{G} = (\mathcal{V}, \mathcal{E})$ 边数为 $O(N)$，相比全连接图带来约 10 倍加速，而精度仅轻微下降（ATE 从 0.01256 升至 0.01243，Table 4）。

### 局部重建与匹配

对场景图的每条边 $(n,m) \in \mathcal{E}$，运行 MASt3R 解码器获得成对的规范点图 $X^{n,e}, X^{m,e}$ 及其置信度 $C^{n,e}$，以及通过 FastNN 提取的稀疏像素对应集合 $\mathcal{M}^{n,m}$。每个图像的规范点图由所有相连边估计的置信度加权平均聚合：

$$\tilde{X}_{i,j}^n = \frac{\sum_{e \in \mathcal{E}^n} C_{i,j}^{n,e} X_{i,j}^{n,e}}{\sum_{e \in \mathcal{E}^n} C_{i,j}^{n,e}}$$

其中 $\mathcal{E}^n$ 为与图像 $n$ 相连的所有边。聚合后的规范点图通过逆投影显式约束为针孔相机模型，定义约束点图 $\chi^n$ 作为内参 $K_n$ 和深度图 $Z^n$ 的函数。焦距 $f$ 则通过 Weiszfeld 算法从规范点图恢复（假设中心主点和方形像素）：

$$f^* = \underset{f}{\arg\min} \sum_{i,j} \left\| \left(i - \frac{W}{2}, j - \frac{H}{2}\right) - f \left( \frac{\tilde{X}_{i,j,1}^n}{\tilde{X}_{i,j,3}^n}, \frac{\tilde{X}_{i,j,2}^n}{\tilde{X}_{i,j,3}^n} \right) \right\|$$

### 粗对齐（3D损失）

粗对齐阶段固定规范深度 $Z^n$ 和内参 $K_n$，仅优化相机位姿 $P_n$ 和尺度 $\sigma_n$。损失函数最小化所有稀疏对应点在全局坐标系中的3D欧氏距离：

$$\sigma^*, P^* = \underset{\sigma, P}{\arg\min} \sum_{c \in \mathcal{M}^{n,m} \atop (n,m) \in \mathcal{E}} q_c \left\| \chi_c^n - \chi_c^m \right\|^{\lambda_1}$$

其中 $q_c$ 为匹配置信度，$\lambda_1 = 1.5$ 为鲁棒范数参数。该阶段使用 Adam 优化器迭代 $\nu_1 = 300$ 次，学习率 0.07。消融实验表明，仅粗对齐（类似 DUSt3R 全局对齐）的 ATE 为 0.01504，远逊于加入细化后的 0.01243（Table 5），说明粗对齐仅提供初始解，需后续细化提升精度。

### 细化（2D重投影损失）

细化阶段联合优化相机位姿、尺度、深度和共享焦距。为降低变量维度，在图像平面上定义间距为 $\delta$ 的规则锚点网格：

$$\dot{y}_{u,\nu} = \left( u\delta + \frac{\delta}{2}, \nu\delta + \frac{\delta}{2} \right)$$

将每个像素的深度变量绑定到最近锚点，形成伪轨迹。损失函数最小化所有稀疏对应的2D重投影误差，采用鲁棒范数 $\rho$：

$$\mathcal{L}_2 = \sum_{c \in \mathcal{M}^{n,m} \atop (n,m) \in \mathcal{E}} q_c \left[ \rho( y_c^n - \pi_n( \chi_c^m ) ) + \rho( y_c^m - \pi_m( \chi_c^n ) ) \right]$$

其中 $\pi_n(\cdot)$ 为相机 $n$ 的投影函数。该阶段使用 Adam 优化器迭代 $\nu_2 = 300$ 次，学习率 0.014，$\lambda_2 = 0.5$。细化本质上是一个可微分类 BA（Bundle Adjustment），但无需显式的三角测量步骤。

### 相机再参数化与运动学链

为解除旋转与平移的耦合，系统引入规范相机变换，将旋转中心沿 Z 轴平移到中值深度平面：

$$\tilde{T}_n = \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & \tilde{m}_n^z \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

同时通过运动学链将绝对姿态转化为相对姿态参数，按树形层次传播：

$$\forall (n \ m) \in \mathcal{D}, P_m = P_{n \ m} P_n$$

消融实验证实，相机再参数化使 RTA@5 从 56.0 跃升至 70.9，ATE 从 0.01445 降至 0.01243（Table 11）；而基于匹配数目的层次聚类构建的运动学链（ATE 0.01243）显著优于星型树（ATE 0.02013），表明平衡的连接树能有效避免相关参数优化中的不一致。

### 纯旋转处理

在纯旋转场景下，系统冻结规范深度图并禁用锚点深度优化，使方法在无平移运动时也能稳定工作。该策略在 InLoc 数据集上实现了 100% 的相对旋转精度（Table 8），而传统 SfM 方法（COLMAP、VGGSfM）在此条件下完全失效。

## 实验与分析

### 主实验结果

**Tanks&Temples 数据集。** MASt3R-SfM 在不同视图数量下均保持最高的注册率（100%），而 COLMAP、VGGSfM、FlowMap 等基线在视图减少时注册率急剧下降。从 25 视图到全视图，MASt3R-SfM 的 ATE 始终低于所有竞争对手：25 视图下 ATE=0.03360（COLMAP=0.03840），全视图下 ATE=0.01060（ACE-Zero=0.01520），相对降低 30.3%。值得注意的是，ATE 计算对所有方法均仅基于已注册相机，而 MASt3R-SfM 始终注册全部视图，这意味着其误差计算包含了所有相机——在公平性上实际处于不利地位，但仍全面领先（Table 1 左）。

![[assets/figures/papers/paper_list_l9_MASt3R_SfM_a_Fully_Integrated_Solution_for_Unconstrained_Structure_from/figures/004_Table_1.jpg]]
*Table 1: Results on Tanks&Temples in terms of ATE and overall registration rate (Reg.). For easier readability, we color-code ATE results as a linear gradient between worst and best ATE for a given dataset or split; and Reg results with linear gradient between 0% and 100%. Left: impact of the number of input views, regularly sampled from the full set. ‘N/A’ indicates that at least one scene did not converge. Right: ATE↓ on different datasets with the arbitrary splits defined in FlowMap [50]*

在 FlowMap 定义的任意分割上，MASt3R-SfM 在 MIP-360 上取得 ATE=0.00079，优于 FlowMap（0.00089）；在 LLFF 上 ATE=0.00098，与 FlowMap（0.00097）持平；在 T&T 和 CO3Dv2 分割上分别取得 0.00215 和 0.00538。需注意 FlowMap 可能在其自身训练分割上进行了训练，而 MASt3R-SfM 完全训练自由（Table 1 右）。

**CO3Dv2 与 RealEstate10K 多视图姿态回归。** 在 10 帧随机采样设置下，MASt3R-SfM 在 CO3Dv2 上取得 mAA(30)=88.0，显著优于 VGGSfM（80.2）和 RelPose++（82.8）；在 RealEstate10K 上取得 86.8，同样领先。当视图数量从 10 降至 5 和 3 时，MASt3R-SfM 的相对旋转精度（RRA）和相对平移精度（RTA）几乎保持恒定，而其他方法急剧下降——这验证了该方法对稀疏输入的高度鲁棒性（Table 2, Table 9, Figure 1 上）。

![[assets/figures/papers/paper_list_l9_MASt3R_SfM_a_Fully_Integrated_Solution_for_Unconstrained_Structure_from/figures/001_Figure_1.jpg]]
*Figure 1: Top: Relative rotation (RRA) and translation (RTA) accuracies on the CO3Dv2 dataset when varying the number of input views with random subsampling (the more views, the larger they overlap). In contrast to our competitors, MASt3R-SfM offers nearly constant performance on the full range, even for very few views. Bottom: MASt3R-SfM also works without motion, i.e. in purely rotational settings. We show here a reconstruction from 6 views sharing the same optical center*

![[assets/figures/papers/paper_list_l9_MASt3R_SfM_a_Fully_Integrated_Solution_for_Unconstrained_Structure_from/figures/005_Table_2.jpg]]
*Table 2: Multi-view pose regression on CO3Dv2 [39] and RealEstate10K [70] with 10 random frames. Parenthesis () denote methods that do not report results on the 10 views set, we report their best for comparison (8 views). We distinguish between (a) multi-view and (b) pairwise methods*

**ETH3D 数据集。** 在逐场景评估中，MASt3R-SfM 平均 RRA@5=81.2、RTA@5=79.7，大幅超越所有对比方法：VGGSfM（64.6/57.2）、FlowMap（56.5/50.1）、COLMAP（39.2/35.4）。在 13 个场景中的 12 个上取得最优或次优结果，唯一例外是“courtyard”场景中 DF-SfM 略优（Table 3）。

![[assets/figures/papers/paper_list_l9_MASt3R_SfM_a_Fully_Integrated_Solution_for_Unconstrained_Structure_from/figures/006_Table_3.jpg]]
*Table 3: Detailed per-scene translation and rotation accuracies (↑) on ETH-3D. For clarity, we color-code results with a linear gradient between the worst and best result for a given scene*

### 消融实验

所有消融实验在 T&T-200 子集上进行。

**场景图构建策略。** 检索式稀疏场景图（Keyframes+kNN）的 ATE=0.01243，与全连接图（0.01256）几乎持平，但边数从 O(N²) 降至 O(N)，带来约 10 倍加速。仅使用 kNN 短程连接（ATE=0.01440）或仅使用关键帧长程连接（ATE=0.01722）均显著劣于二者结合，表明短程与长程连接互补，对鲁棒重建至关重要（Table 4, Table 5）。

![[assets/figures/papers/paper_list_l9_MASt3R_SfM_a_Fully_Integrated_Solution_for_Unconstrained_Structure_from/figures/007_Table_4.jpg]]
*Table 4: Ablation of scene graph construction on Tanks&Temples (200 view subset). See text for details*

![[assets/figures/papers/paper_list_l9_MASt3R_SfM_a_Fully_Integrated_Solution_for_Unconstrained_Structure_from/figures/009_Table_5.jpg]]
*Table 5: Ablations on Tanks&Temples (200 view subset). See text for details*

**优化阶段贡献。** 仅进行粗对齐（类似 DUSt3R 全局对齐但使用稀疏匹配和更少优化变量）得到 ATE=0.01504；加入细化后降至 0.01243，RTA@5 从 56.0 跃升至 70.9。若细化时不优化锚点深度（仅使用冻结的规范深度图），ATE 为 0.01315，仍优于仅粗对齐，但弱于完整细化——说明联合优化深度能进一步提升精度（Table 5）。

**内参策略。** 共享单焦距优于每相机独立内参（ATE 0.01243 vs 0.01329），表明联合优化多相机的共同焦距能提高全局一致性（Table 5）。

**相机再参数化与运动学链。** 将相机旋转中心平移到中值深度平面（规范相机变换）大幅提升姿态精度：ATE 从 0.01445 降至 0.01243，RTA@5 从 56.0 升至 70.9。运动学链结构方面，基于匹配数目的层次聚类构建的平衡树性能最优（ATE=0.01243），而星型树仅 0.02013——平衡的连接树能有效避免相关参数优化中的不一致传播（Table 11, Appendix F）。

**检索特征聚合方式。** MASt3R 编码器分词特征经 ASMK 聚合后，在视觉定位任务上表现最优；若改用平均池化+白化+余弦相似度的全局特征，或先学习投影器再 ASMK，定位精度均有所下降（Table 7）。

![[assets/figures/papers/paper_list_l9_MASt3R_SfM_a_Fully_Integrated_Solution_for_Unconstrained_Structure_from/figures/011_Table_7.jpg]]
*Table 7: Comparison of retrieval based on MASt3R features. We compare the visual localization accuracy using top-20 retrieved images with ASMK (top row), a global feature representation obtained by averaging pooling the local features, whitening using a cosine similarity (middle row), and ASMK when first learning a projector on top of the MASt3R features (bottom row)*

**超参数敏感性。** 关键图像数 N_a 和最近邻数 k 在合理范围内（N_a≥15, k≥5）对最终精度影响较小，方法对此不敏感（Figure 7）。粗对齐迭代次数约 250 次后收敛，细化在此基础上持续改善（Figure 4）。

![[assets/figures/papers/paper_list_l9_MASt3R_SfM_a_Fully_Integrated_Solution_for_Unconstrained_Structure_from/figures/010_Figure_4.jpg]]
*Figure 4: Pose accuracy (↑) on T&T-200 w.r.t. the number of iterations of the coarse and refinement stages (resp. ??1 and ??2)*

![[assets/figures/papers/paper_list_l9_MASt3R_SfM_a_Fully_Integrated_Solution_for_Unconstrained_Structure_from/figures/015_Figure_7.jpg]]
*Figure 7: Pose accuracy (↑) on T&T-200 w.r.t. the number of key images N _ { a } and number of nearest neighbors ??*

### 图像检索评估

复用 MASt3R 冻结编码器+ASMK 的检索方案（top-20）在 Aachen 昼夜定位和 InLoc 室内定位任务上，与专用检索器 FIRe 性能相当，并在 InLoc 上设定了新的定位精度最优。这验证了“劫持”编码器进行检索的有效性——几乎零额外计算开销即获得了有竞争力的检索质量（Table 6）。

![[assets/figures/papers/paper_list_l9_MASt3R_SfM_a_Fully_Integrated_Solution_for_Unconstrained_Structure_from/figures/008_Table_6.jpg]]
*Table 6: Comparison of retrieval based on MASt3R features using ASMK with the state-of-the-art FIRe method when localizing with MASt3R (bottom rows), as well as with other state-of-the-art visual localization methods (top rows)*

### 纯旋转场景

在 InLoc 数据集 20 个纯旋转场景上，传统 SfM 方法（COLMAP、VGGSfM）完全失效，而 MASt3R-SfM 通过冻结规范深度图并禁用锚点深度优化（MASt3R-SfM†），实现了 100% 的相对旋转精度（RRA@5）。这验证了方法对无平移运动这一极端条件的独特处理能力（Table 8, Figure 1 下）。

![[assets/figures/papers/paper_list_l9_MASt3R_SfM_a_Fully_Integrated_Solution_for_Unconstrained_Structure_from/figures/014_Table_8.jpg]]
*Table 8: Pure Rotation Case. RRA@5 (↑) on 20 randomly chosen scenes from the InLoc dataset. MASt3R-SfM† denotes our approach with disabled depth optimization for better optimization stability*

### 失败模式分析

所有手动审查的失败案例根因均为**重复或相似纹理导致的错误匹配（outliers）**。在室内纯旋转场景（如 InLoc 的 DUC1/007）中尤为突出：相似外观区域间的错误对应破坏了全局对齐。当前方法假设针孔相机模型且无镜头畸变，未考虑动态场景或非朗伯面等更具挑战性的条件。此外，方法严重依赖 MASt3R 预训练模型的质量与泛化性，在极端低纹理或跨域场景下性能可能下降（Figure 6, Section 6）。

## 方法谱系与知识库定位

### 与基线方法的关系

MASt3R-SfM 的核心定位是**全集成、无训练的SfM流水线**，其方法谱系可沿两条主线追溯：传统SfM的模块化解耦路线，以及基于学习的端到端重建路线。

**相对于传统增量SfM（COLMAP）**：COLMAP（Schönberger et al., CVPR 2016）依赖关键点提取、特征匹配、RANSAC外点剔除、增量式BA的级联模块，在图像重叠不足、视图稀少或纯旋转时极易失败，且随着图像数量增加，匹配和BA的计算开销急剧增长。MASt3R-SfM 以MASt3R的冻结解码器替代了整个前端（关键点+匹配+RANSAC），用两阶段梯度下降替代增量BA，从根本上消除了模块间的误差累积和RANSAC的随机性。在T&T 25视图子集上，ATE从COLMAP的0.03840降至0.03360（降低12.5%）；在全视图上差距进一步拉大。更重要的是，COLMAP在困难场景下会丢弃无法注册的相机，而MASt3R-SfM始终保持100%注册率，且ATE计算包含所有相机——这对MASt3R-SfM实际上是不利的比较条件。

**相对于端到端可微分SfM（VGGSfM）**：VGGSfM（Wang et al., CVPR 2024）将SfM重新表述为可微分优化问题，但仍需要训练。在CO3Dv2的10帧随机采样实验中，MASt3R-SfM的mAA(30)达到88.0，而VGGSfM为80.2（提升9.7个百分点）；在ETH3D上，平均RRA@5/RTA@5为81.2/79.7，远超VGGSfM的64.6/57.2。关键差异在于：VGGSfM依赖学习到的匹配器和优化器，而MASt3R-SfM利用MASt3R作为冻结的3D基础模型，管道完全训练自由。

**相对于基于梯度下降的SfM（FlowMap）**：FlowMap（Smith et al., ECCV 2024）同样采用梯度下降进行全局优化，但通过深度网络再参数化来约束优化空间。在FlowMap的任意分割实验中，MASt3R-SfM在MIP-360上ATE为0.00079（FlowMap为0.00089），在LLFF上为0.00098（FlowMap为0.00105），达到可比或更优水平。值得注意的是，FlowMap可能在其自身训练分割上进行了训练，而MASt3R-SfM完全无训练，这一公平性差异使得MASt3R-SfM的优势更具说服力。

**相对于场景坐标回归方法（ACE-Zero）**：ACE-Zero（Brachmann et al., ECCV 2024）通过测试时训练场景坐标回归器来重建，在T&T全视图上ATE为0.01520。MASt3R-SfM的ATE为0.01060，相对降低30.3%。ACE-Zero需要为每个场景单独训练，而MASt3R-SfM的前向推理无需任何场景级训练。

**相对于免检测器匹配SfM（DF-SfM）**：DF-SfM（He et al., CVPR 2024）消除了显式关键点检测，但仍依赖匹配和RANSAC。MASt3R-SfM更进一步，将匹配隐式地嵌入到MASt3R的点图回归中，并通过FastNN直接输出稀疏对应，完全绕过了独立的匹配和几何验证步骤。

**相对于DUSt3R**：DUSt3R是MASt3R的直接前身，也是MASt3R-SfM最直接的比较对象。DUSt3R的全局对齐对所有密集点施加相似变换约束，复杂度为O(N²)，且未针对纯旋转优化。MASt3R-SfM在此基础上做了三个关键改进：（1）复用编码器进行ASMK检索，将匹配复杂度降至O(N)；（2）用稀疏匹配替代密集点进行粗对齐，减少优化变量；（3）引入基于2D重投影的细化阶段和规范相机再参数化，显著提升精度。消融实验表明，仅粗对齐（类似DUSt3R全局对齐）的ATE为0.01504，加入细化后降至0.01243。

**相对于DROID-SLAM**：DROID-SLAM（Teed et al., NeurIPS 2021）基于稠密光流的深度优化，在FlowMap分割的部分数据集上略优于MASt3R-SfM。但DROID-SLAM本质上是SLAM系统，需要时序连续的输入，而MASt3R-SfM面向完全无约束的图像集合，输入无需任何时序信息。

### 适用边界与局限

**已知失败模式**：所有手动审查的失败案例均源于重复或相似纹理导致的错误匹配（outliers）。在InLoc数据集的纯旋转场景中尤为明显（如DUC1/007场景），相似外观的不同区域被错误关联，导致优化陷入局部极小。Figure 6展示了三个典型错误匹配对，并标注了真实相机的方位角和仰角以佐证。

**模型假设限制**：当前方法严格假设针孔相机模型且无镜头畸变。对于鱼眼、全景等非针孔相机，或存在显著畸变的图像，管道无法直接适用。此外，方法未考虑动态场景或非朗伯面，这些条件下的MASt3R点图质量可能下降，进而影响整个管道。

**预训练模型依赖性**：尽管管道整体无训练，但其性能严重依赖于MASt3R预训练模型的质量与泛化性。在极端低纹理（如医学影像）或与预训练域差异显著的场景中，点图估计和匹配质量可能下降。这一依赖性是所有基于冻结基础模型的方法共有的局限。

**纯旋转场景的深度优化不稳定**：在纯旋转场景下，深度参数的过度自由会导致优化不稳定。当前解决方案是冻结规范深度图并禁用锚点深度优化（MASt3R-SfM†），这虽然保证了稳定性（InLoc上RRA@5达到100%），但牺牲了可能的深度改善。Table 8显示，未禁用深度优化的版本在纯旋转场景下性能显著下降。

**大规模极限**：虽然检索式场景图将边数从O(N²)降至O(N)，但ASMK检索模块的码本规模和检索效率在超大规模（>10万图）下的表现尚未验证。此外，最远点采样（FPS）和kNN连接的选择策略是否在极端规模下仍能保持场景图的连通性和覆盖度，仍需进一步研究。

### 开放问题

1. **非针孔相机扩展**：如何将管道扩展至鱼眼、全景等非针孔相机模型，并自动处理镜头畸变？这需要MASt3R本身支持非针孔几何，或在管道中引入畸变参数化。

2. **外点匹配的语义抑制**：重复纹理导致的外点匹配是主要失败根源。能否引入语义或几何先验（如全局上下文一致性、共面性约束）来进一步抑制错误匹配？例如，利用MASt3R的密集特征进行局部几何一致性检验。

3. **纯旋转下的深度正则化**：当前冻结深度的策略虽然有效但过于刚性。是否存在更好的正则化方法（如深度平滑先验、单目深度先验），在保持稳定性的同时允许有益的深度调整？

4. **动态场景处理**：该框架能否自然地纳入多帧时空信息以处理动态场景？可能的方向包括在场景图构建阶段引入运动掩码，或在优化阶段对动态区域施加额外的鲁棒损失。

5. **极大规模验证**：MASt3R-SfM声称的线性复杂度在实际大规模重建（>10万图）中是否仍然成立？检索模块的码本规模如何影响效率与精度？FPS采样策略是否需要在极大规模下引入层次化或分块机制？

6. **与NeRF/3DGS的协同**：MASt3R-SfM输出的稀疏重建和精确相机姿态能否作为NeRF或3D Gaussian Splatting的理想初始化？这种协同可能进一步提升稠密重建和新视角合成的质量。

## 原文 PDF

![[paperPDFs/3DV_2025/MASt3R_SfM_a_Fully_Integrated_Solution_for_Unconstrained_Structure_from_Motion.pdf]]
