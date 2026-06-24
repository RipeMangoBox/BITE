---
title: "Light3R-SfM: Towards Feed-forward Structure-from-Motion"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/Light3R_SfM_Towards_Feed_forward_Structure_from_Motion.pdf
aliases:
- LS
- Light3R-SfM
tags:
- CVPR_2025
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "用可学习的潜在全局注意力模块（latent global alignment）替代传统的显式全局优化，并结合检索分数引导的最短路径树（SPT）构建稀疏场景图。"
primary_logic: "在图像编码与解码之间插入一个可扩展的注意力层，在特征空间进行多视图信息共享，使成对点图解码能够间接获得全局一致性；同时通过 SPT 限制解码边数并减少累积漂移，实现纯前馈式的高效全局对齐。"
claims:
- "在 Tanks&Temples 全序列上，Light3R-SfM 完成重建仅需 63.4 秒，而 MASt3R-SfM 需要 2723.1 秒（速度提升约 43 倍）。"
- "在 25 视角 Tanks&Temples 场景，Light3R-SfM 的相对旋转精度 RRA@5 达到 50.9%，远超 Spann3R 的 19.6%。"
- "消融实验表明，加入潜在对齐模块使 RRA@5 提升 6.95%，ATE 降低 15.78%。"
- "使用最短路径树（SPT）替代最小生成树（MST）后，RRA@5 相对提升 15.26%，RTA@5 提升 25.61%。"
---

# Light3R-SfM: Towards Feed-forward Structure-from-Motion

> [!tip] 核心洞察
> 在图像编码与解码之间插入一个可扩展的注意力层，在特征空间进行多视图信息共享，使成对点图解码能够间接获得全局一致性；同时通过 SPT 限制解码边数并减少累积漂移，实现纯前馈式的高效全局对齐。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Light3R-SfM: 迈向前馈式运动恢复结构 |
| 英文题名 | Light3R-SfM: Towards Feed-forward Structure-from-Motion |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2501.14914) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Light3R-SfM |
| Dataset | Tanks&Temples (25 views), Tanks&Temples (full sequence) |

> [!tip] 效果简介
> - Tanks&Temples (25 views) 上，RRA@5↑ 为 50.9，对比 MASt3R-SfM 68.0，变化 -17.1。
> - Tanks&Temples (25 views) 上，Time(s)↓ 为 4.4，对比 MASt3R-SfM 283.2，变化 278.8 s 更快。
> - Tanks&Temples (full sequence) 上，RRA@5↑ 为 52.0，对比 Spann3R (unordered) 20.3，变化 +31.7。

## 概述

**问题瓶颈**：传统运动恢复结构（Structure-from-Motion, SfM）方法——无论是经典的增量式（COLMAP）或全局式（GLOMAP），还是基于点图回归的优化式方法（MASt3R-SfM）——其核心瓶颈在于依赖昂贵的特征匹配与全局迭代优化（如 Bundle Adjustment），导致计算耗时极长、内存开销巨大，难以高效扩展至大规模图像集。另一方面，前馈式方法 Spann3R 虽然避免了全局优化，但其基于记忆库的在线/离线对齐机制存在时序漂移，且难以处理无序图像。

**核心思路**：Light3R-SfM 提出了一条纯前馈式 SfM 管线，其核心因果开关是在图像编码器与成对解码器之间插入一个可学习的**潜在全局注意力模块**（latent global alignment），在特征空间实现多视图信息共享，从而替代传统的显式全局优化。同时，通过**检索分数引导的最短路径树**（Shortest Path Tree, SPT）构建稀疏场景图，仅对 N-1 条边进行解码，在限制解码边数、减少累积漂移的同时，实现高效的全局对齐。这一设计使得成对点图解码能够间接获得全局一致性，无需任何迭代优化步骤。

**方法定位**：在方法谱系上，Light3R-SfM 属于前馈式 SfM（Feed-forward SfM），与基于优化的 MASt3R-SfM 和基于记忆库的 Spann3R 形成对比。其关键改变包括：
- **全局对齐方式**：从迭代优化（BA 或 pairwise 联合优化）转变为可学习的潜在注意力机制；
- **场景图构建**：从全连接图或最小生成树（MST）转变为基于编码器相似度的最短路径树（SPT），使树结构更扁平以减少漂移；
- **点图融合**：从对所有图像对解码后的大尺度全局优化，转变为仅对 SPT 边解码、通过广度优先遍历与加权 Procrustes 对齐逐步累积成全局点图。

**主要结果**：
- **速度飞跃**：在 Tanks&Temples 全序列上，Light3R-SfM 完成重建仅需 63.4 秒，而 MASt3R-SfM 需要 2723.1 秒，速度提升约 43 倍（Table 1）。
- **精度对比**：在 25 视角 Tanks&Temples 场景中，Light3R-SfM 的相对旋转精度 RRA@5 达到 50.9%，远超前馈基线 Spann3R 的 19.6%，但落后于优化式方法 MASt3R-SfM 的 68.0%（Table 1）。在 Waymo 驾驶场景中，Light3R-SfM 的 RRA@5 达到 78.3%，反超 MASt3R-SfM 的 75.7%（Table 4）。
- **消融验证**：潜在对齐模块使 RRA@5 提升 6.95%，ATE 降低 15.78%；SPT 相比 MST 使 RRA@5 相对提升 15.26%，RTA@5 提升 25.61%（Table 5）。

**局限性**：在严格误差阈值下的精度仍明显落后于基于优化的最优方法；动态物体场景可能导致全局置信度下降；检索图构建失败时可能造成场景断裂；训练图规模受显存限制（N=8），限制了高阶多视图约束的学习。

## 背景与动机

### 运动恢复结构（SfM）的核心任务与现实瓶颈

运动恢复结构（Structure-from-Motion, SfM）旨在从一组无序的二维图像中同时恢复相机位姿与场景的三维结构。这是一项基础且经典的计算机视觉任务，在自动驾驶、机器人导航、增强现实、文化遗产数字化等领域具有广泛的应用需求。

传统 SfM 管道（如 COLMAP、GLOMAP）遵循一套成熟的增量式或全局式流程：特征提取与匹配 → 几何验证 → 初始重建 → 捆绑调整（Bundle Adjustment, BA）。这一范式的**核心瓶颈**在于其对显式特征匹配与迭代全局优化的深度依赖。特征匹配的计算复杂度随图像数量呈二次增长，而捆绑调整作为非线性最小二乘问题，每次迭代都需要求解大规模稀疏线性系统，导致**速度慢、内存开销大**，难以高效扩展到包含数百甚至上千张图像的大规模场景。

### 从优化式到前馈式的范式转换

近年来，基于学习的点图回归方法为 SfM 提供了一条新的技术路径。DUSt3R 和 MASt3R 等工作表明，可以通过 Transformer 架构直接从图像对中回归密集的三维点图，从而隐式地绕过显式特征匹配。然而，这些方法仍然需要将成对预测通过**穷举的全局优化**（如多视图联合优化 + BA）进行后处理，以实现全局一致的相机位姿估计。例如，MASt3R-SfM 在 Tanks&Temples 数据集上完成一个 200 视角场景的重建需要约 27 分钟（Table 1），速度瓶颈依然突出。

Spann3R 首次尝试构建**纯前馈式**的 SfM 管道，通过引入显式记忆库（memory bank）替代全局优化，在图像序列上实现了在线式（online）重建。但这一方案存在两个关键缺陷：

1. **时序漂移**：在在线模式下，误差沿序列累积，导致长序列末端的重建质量显著退化。
2. **无序图像处理能力弱**：当输入为无序图像集时，Spann3R 的离线模式性能急剧下降——在 Tanks&Temples 全序列上，其相对旋转精度 RRA@5 仅为 20.3%，远低于优化式方法（Table 2）。

### 本文动机：前馈式全局对齐的可能性

上述现状揭示了一个核心矛盾：**优化式方法精度高但速度极慢，前馈式方法速度快但缺乏有效的全局一致性机制**。这一矛盾的根源在于，现有的前馈式方法（如 Spann3R）试图通过序列化记忆传递来近似全局信息，但记忆的有限容量和单向传播特性使其无法真正实现多视图间的信息共享与约束满足。

Light3R-SfM 的核心动机正是回答一个关键问题：**能否在纯前馈框架内实现可扩展的全局对齐，从而同时获得优化式方法的精度和前馈式方法的速度？** 具体而言，本文试图解决两个技术挑战：

- **如何在不依赖迭代优化的前提下，实现多视图间的全局信息共享？** 传统方法通过 BA 显式地最小化重投影误差来满足全局几何约束，而前馈式方法缺乏等效的机制。
- **如何构建一个稀疏但信息充分的场景图来引导前馈式重建？** 全连接图计算成本过高，而简单的链式或树形结构（如 Spann3R 的在线序列）又容易引入累积误差。

本文的解决方案——潜在全局注意力模块（latent global alignment）与检索分数引导的最短路径树（SPT）——正是围绕这两个核心挑战展开设计。通过在特征空间而非几何空间完成多视图信息交换，以及通过扁平化的树结构减少累积漂移，Light3R-SfM 试图证明：**前馈式 SfM 可以在保持极高速度的同时，达到接近优化式方法的全局一致性**。

## 核心创新

Light3R-SfM 的核心创新在于将传统 SfM 中依赖显式迭代优化的全局对齐，替换为一种纯前馈式的、可学习的潜在全局注意力机制，并结合检索分数引导的最短路径树（SPT）构建稀疏场景图，从而在保持竞争性精度的同时实现数量级的速度提升。

### 从显式优化到可学习潜在全局对齐

传统优化式 SfM（如 MASt3R-SfM）依赖对所有图像对解码点图后进行大规模全局优化（如 Bundle Adjustment），计算开销随图像数量急剧增长。Light3R-SfM 的关键洞察是：**在图像编码器与成对点图解码器之间，插入一个基于注意力机制的可扩展潜在全局对齐模块（Latent Global Alignment），使多视图信息在特征空间完成共享，从而让成对解码器能间接获得全局一致性，完全消除显式全局优化。**

具体而言，该模块将每幅图像的密集特征 tokens 池化为一个全局 token，然后通过全局 token 间的自注意力（Self-Attention）实现跨图像信息交换，再通过交叉注意力（Cross-Attention）将更新后的全局信息传播回各图像的密集 tokens。这种因式分解的注意力设计将计算复杂度从全连接注意力的 $O(N^2)$ 降至可控范围，使得模型能够高效处理无序图像集。

消融实验证实了这一设计的决定性作用：**加入潜在对齐模块后，RRA@5 提升 6.95%，ATE 降低 15.78%**（Table 5）。更直观的证据来自 Figure 4：经过潜在全局对齐的条件化后，解码器甚至能够为朝向相反的相机预测出合理的点图，表明该模块确实学习到了整个场景的全局表征。

### 从最小生成树到最短路径树

传统方法通常采用全连接图或最小生成树（MST）构建场景图。MST 虽然将边数降至 $N-1$，但树结构可能过深，导致逐边累积漂移严重。Light3R-SfM 提出**基于检索分数引导的最短路径树（SPT）**：利用编码器池化后的图像嵌入计算成对余弦相似度作为边权重，然后构建使根节点到所有节点的路径代价之和最小的有根树。

SPT 的关键优势在于：通过最小化路径代价，树结构更扁平，有效减少了广度优先遍历累积时的漂移累积。消融实验表明，**使用 SPT 替代 MST 后，RRA@5 相对提升 15.26%，RTA@5 提升 25.61%**（Table 5）。同时，SPT 保持边数为 $N-1$，解码和累积的计算开销与图像数量呈线性关系。

### 纯前馈式全局累积

在全局重建阶段，Light3R-SfM 仅对 SPT 的 $N-1$ 条边进行成对点图解码，然后以根节点为基准，按广度优先顺序通过加权 Procrustes 对齐将各局部点图逐步注册到全局坐标系。整个过程为**纯前馈式**，无需任何迭代优化或 Bundle Adjustment。

这一设计带来的速度优势是决定性的：在 Tanks&Temples 全序列上，Light3R-SfM 完成重建仅需 **63.4 秒**，而 MASt3R-SfM 需要 **2723.1 秒**（速度提升约 43 倍）；在 200 视图场景中，Light3R-SfM 仅需约 33 秒，MASt3R-SfM 则需约 27 分钟（>49 倍加速）（Table 1, Figure 1）。

### 创新边界与局限

需要指出的是，这种纯前馈式设计在精度上仍存在妥协：在严格误差阈值下，Light3R-SfM 的精度明显落后于基于优化的最优方法（如 MASt3R-SfM 和 GLOMAP）。例如在 Tanks&Temples 25 视图设定下，Light3R-SfM 的 RRA@5 为 50.9%，而 MASt3R-SfM 达到 68.0%（Table 1）。这表明潜在对齐虽然能捕获全局约束，但尚不能完全替代显式几何优化的精度。此外，当检索图构建失败时，SPT 可能导致场景断裂成多个不一致的子重建，这是该方法的一个结构性脆弱点。

## 整体框架

Light3R-SfM 的目标是将一组**无序图像**（无需时间戳或顺序先验）作为输入，直接输出每幅图像对应的相机外参 $P \in \mathbb{R}^{4\times4}$、内参 $K_i \in \mathbb{R}^{3\times3}$ 以及图像分辨率的稠密 3D 点图 $X \in \mathbb{R}^{H\times W\times3}$。整个流程是**纯前馈式**的，不包含任何迭代优化或捆集调整（BA）步骤。

### 核心瓶颈与设计动机

传统 SfM 管线（如 COLMAP、GLOMAP）依赖昂贵的特征匹配与全局优化，导致速度慢、内存开销大，难以扩展到大规模图像集。基于 DUSt3R/MASt3R 的优化式方法虽然利用学习到的点图回归提升了鲁棒性，但仍需对所有图像对进行穷举解码和全局联合优化，其计算复杂度随图像数量呈平方级增长。另一条前馈式路线 Spann3R 通过记忆库实现隐式对齐，但存在**时序漂移**问题，且难以有效处理无序图像。

Light3R-SfM 的核心设计动机即在于：**用可学习的潜在全局注意力模块替代显式全局优化**，在特征空间完成多视图信息共享，同时通过**检索分数引导的最短路径树（SPT）** 构建稀疏场景图，将解码边数从 $O(N^2)$ 压缩到 $N-1$，从而在保持全局一致性的同时实现大幅加速。

### 五阶段流水线

如图 2 所示，Light3R-SfM 的流水线由以下五个模块串联构成：

1.  **图像编码器 (Encoder)**  
    将每幅输入图像 $\mathbb{Z}_i$ 编码为密集特征 tokens $F_i^{(0)} \in \mathbb{R}^{\lfloor H/p \rfloor \times \lfloor W/p \rfloor \times d}$，同时通过空间平均池化得到全局 token $g_i^{(0)}$，用于后续的场景图构建和潜在对齐。

2.  **潜在全局对齐模块 (Latent Global Alignment)**  
    这是整个方法的关键创新。该模块在图像编码与解码之间插入 $L$ 层可扩展的注意力操作：首先在所有图像的全局 token $\{g_i\}$ 之间执行**自注意力**，实现跨视图信息交换；然后通过**交叉注意力**将更新后的全局信息传播回各图像的密集 tokens。这一机制使得后续的成对点图解码能够间接获得全局场景先验，从而在无需显式全局优化的前提下实现多视图一致性。

3.  **场景图构建 (Scene Graph Construction)**  
    基于池化后的图像嵌入计算成对余弦相似度 $S_{ij} = \langle \|\bar{F}_i\|_2, \|\bar{F}_j\|_2 \rangle$，并运行**最短路径树（SPT）** 算法，得到包含恰好 $N-1$ 条边的稀疏场景图 $E_{\text{SPT}}$。相比传统的最小生成树（MST），SPT 使树结构更扁平，有效减少了累积漂移。

4.  **成对点图解码器 (Pairwise Decoder)**  
    仅对场景图中的每条边 $(i,j) \in E_{\text{SPT}}$，利用经过潜在对齐的图像 tokens 解码出成对点图 $(X^{i,i}, X^{j,i})$ 及逐点置信度图 $(C^{i,i}, C^{j,i})$。由于解码边数被限制为 $N-1$，该步骤的计算开销得到严格控制。

5.  **全局累积 (Global Accumulation)**  
    以 SPT 的根节点为全局基准，按广度优先顺序遍历场景图，通过**对数置信度加权的闭式 Procrustes 对齐**将各局部点图逐步注册到全局坐标系，最终生成每幅图像的全局点图 $X^i$ 及全局置信度 $C^i$。整个过程无需任何迭代优化。

### 输入输出与数据流

-   **输入**：一组无序 RGB 图像 $\{\mathbb{Z}_i\}_{i=1}^N$。
-   **输出**：每幅图像的相机外参 $P_i$、内参 $K_i$、稠密 3D 点图 $X^i$ 及置信度图 $C^i$。
-   **数据流**：图像 → 编码器 → 密集 tokens + 全局 tokens → 潜在全局对齐 → 对齐后的密集 tokens → SPT 边选择 → 成对解码器 → 局部点图 → 全局累积 → 全局点图与相机参数。

### 训练监督

训练时采用两项损失的加权组合：
$$\mathcal{L} = \mathcal{L}_{\text{pair}} + \lambda \mathcal{L}_{\text{global}}$$

其中 $\mathcal{L}_{\text{pair}}$ 在所有 SPT 边上监督成对点图重建（损失定义在第一幅相机的坐标系下），$\mathcal{L}_{\text{global}}$ 则将预测的全局点云与真值通过 Procrustes 对齐后计算逐点置信度加权的 L1 损失。实验表明 $\lambda=0.1$ 取得最优平衡。

> **注意**：由于显存限制，训练时的图规模设定为 $N=8$，这限制了高阶多视图约束的学习，高分辨率模型可能无法使用更大的训练图。该局限性对实际部署的影响需进一步评估。

### 补充图表

![[assets/figures/papers/paper_list_l47_https_arxiv_org_abs_2501_14914/figures/002_Figure_2.jpg]]
*Figure 2: Light3R-SfM Pipeline. Given an unordered set of images, we first encode them to obtain image tokens from which we average pool global features for constructing a shortest path tree. We next feed image tokens into our attention-based latent global alignment to enable global context sharing. Afterwards, for each edge in the SPT, we decode pairwise pointmaps using the implicitly aligned feature tokens. Finally, we use global accumulation to obtain globally aligned pointmaps per image*

## 核心模块与公式推导

Light3R-SfM 的核心架构由五个模块串联构成，其设计目标是用纯前馈计算替代传统 SfM 中的显式全局优化。整个流程从无序图像集合出发，输出每幅图像的相机外参、内参以及密集 3D 点图。

### 图像编码器

给定一组无序图像 $\{\mathbb{Z}_i\}_{i=1}^N$，每幅图像首先通过一个 ViT 编码器转换为密集特征 tokens：

$$F_i^{(0)} = \mathtt{Enc}(\mathbb{Z}_i), \quad F_i^{(0)} \in \mathbb{R}^{\lfloor H/p \rfloor \times \lfloor W/p \rfloor \times d}$$

其中 $p$ 为 patch 大小，$d$ 为特征维度。编码器同时将密集 tokens 沿空间维度平均池化，得到每幅图像的全局 token $g_i^{(0)}$，用于后续的全局信息交换和场景图构建。

### 潜在全局对齐模块

这是替代传统全局优化的关键组件。该模块通过一个可扩展的分解注意力机制，在所有图像间共享多视图信息。具体而言，它由 $L$ 层交替的自注意力和交叉注意力构成：

$$\{g_i^{(l+1)}\}_{i=1}^N = \mathtt{Self}(\{g_i^{(l)}\}_{i=1}^N)$$

$$F_i^{(l+1)} = \mathtt{Cross}(F_i^{(l)}, \{g_i^{(l+1)}\}_{i=1}^N)$$

自注意力层在所有图像的全局 token 之间进行信息交换，使每个全局 token 感知整个场景的上下文；交叉注意力层则将更新后的全局信息传播回各图像的密集 tokens。这种分解设计将原本 $O(N^2 \cdot (HW/p^2)^2)$ 的全对全注意力复杂度降低到可处理水平，同时使后续的成对解码器能够间接获得全局一致性。

### 场景图构建

为减少需要解码的图像对数量并抑制累积漂移，Light3R-SfM 在解码前先构建一个稀疏场景图。首先利用池化后的图像嵌入计算成对余弦相似度：

$$S_{ij} = \langle \|\bar{F}_i\|_2, \|\bar{F}_j\|_2 \rangle$$

然后以相似度分数作为边权重，构建**最短路径树**。与最小生成树不同，SPT 以检索分数最高的图像为根节点，最小化从根到每个节点的路径代价，从而使树结构更扁平，有效减少长链带来的累积漂移。SPT 的边数保持为 $N-1$，大幅降低了后续解码的计算量。

### 成对点图解码器

仅对场景图中的每条边 $(i,j) \in E_{\mathrm{SPT}}$ 运行解码器：

$$(X^{i,i}, X^{j,i}), (C^{i,i}, C^{j,i}) = \mathtt{Dec}(F_i, F_j)$$

解码器输出两个点图 $X^{i,i}, X^{j,i}$ 及对应的逐点置信度图 $C^{i,i}, C^{j,i}$。上标 $X^{j,i}$ 表示以图像 $i$ 的相机坐标系为参考系预测图像 $j$ 的点图。由于解码前图像 tokens 已经过潜在全局对齐，解码器能够利用隐含的全局信息，即使对视角差异极大的图像对也能产生合理的点图预测。

### 全局累积

以 SPT 根节点为全局坐标系基准，按广度优先顺序遍历场景图。对于每条边，通过加权 Procrustes 对齐将局部点图注册到全局坐标系：

$$P_k = \mathtt{Procrustes}(X^k, X^{k,k}, \log C^k)$$

其中 $X^k$ 为已注册到全局坐标系的点图，$X^{k,k}$ 为局部点图，$\log C^k$ 作为逐点权重。求得刚性变换 $P_k$ 后，将新节点的局部点图变换到全局坐标系：

$$X^{l,l} = P_k^{-1} X^{k,l}$$

这一过程无需任何迭代优化，通过闭式 Procrustes 求解和广度优先遍历即可逐步累积成全局一致的 3D 重建。

### 训练监督

训练损失由两部分加权组成：

$$\mathcal{L} = \mathcal{L}_{\mathrm{pair}} + \lambda \mathcal{L}_{\mathrm{global}}$$

**成对损失**在所有 SPT 边上监督局部点图重建质量：

$$\mathcal{L}_{\mathrm{pair}} = \sum_{(i,j)\in E_{\mathrm{SPT}}} \big(\mathcal{L}_{\mathrm{conf}}(P_i \bar{X}^i, X^{i,i}, C^{i,i}, \mathcal{D}^i) + \mathcal{L}_{\mathrm{conf}}(P_i \bar{X}^j, X^{j,i}, C^{j,i}, \mathcal{D}^j)\big)$$

其中 $\mathcal{L}_{\mathrm{conf}}$ 为置信度加权的 L1 损失：

$$\mathcal{L}_{\mathrm{conf}}(\bar{X}, X, C, \mathcal{D}) := \sum_{p\in\mathcal{D}} C_p \|X_p - \bar{X}_p\| - \alpha C_p$$

正则项 $-\alpha C_p$ 防止置信度退化为 0。

**全局损失**先将所有预测点图通过 Procrustes 对齐到真值坐标系，再计算重建误差：

$$P_{\mathrm{align}} = \mathtt{Procrustes}(\bar{\mathbf{X}}, \mathbf{X})$$

$$\mathcal{L}_{\mathrm{global}} = \sum_{i} \mathcal{L}_{\mathrm{conf}}(\bar{X}^i, P_{\mathrm{align}} X^i, C^i, \mathcal{D}^i)$$

消融实验表明，全局监督权重 $\lambda=0.1$ 取得最优平衡，加入全局损失后 RRA@5 提升 6.95%，ATE 降低 15.78%。

## 实验与分析

### 核心实验结果

Light3R-SfM 在多个基准上验证了其核心主张：以前馈式架构实现与优化式方法可比的位姿精度，同时获得数量级的速度提升。

**Tanks&Temples 多视图位姿估计。** Table 1 系统比较了 Light3R-SfM 与优化式方法（MASt3R-SfM、GLOMAP、COLMAP）及前馈式方法（Spann3R、DUSt3R+全局对齐）在不同视图子集（25/50/100/200 视图及全序列）上的性能。关键发现如下：

- **速度优势显著。** 在全序列上，Light3R-SfM 完成重建仅需 63.4 秒，而 MASt3R-SfM 需要 2723.1 秒（约 43 倍加速），GLOMAP 需要 1977.7 秒（约 31 倍加速）。在 200 视图子集上，Light3R-SfM 耗时 33.4 秒，MASt3R-SfM 耗时约 27 分钟（>49 倍加速），与 Figure 1 的速度-精度散点图一致。
- **精度保持竞争力。** 在 25 视图设定下，Light3R-SfM 的 RRA@5 为 50.9%，虽低于 MASt3R-SfM 的 68.0%，但远超 Spann3R 的 19.6%。在全序列上，RRA@5 达到 52.0%，ATE 仅 0.011，注册率 100%。
- **与 Spann3R 的详细对比。** Table 2 显示，Light3R-SfM 在 25 视图、50 视图和全序列三个设定下，RRA@5 分别领先 Spann3R（无序模式）31.3、29.3 和 31.7 个百分点。Spann3R 的时序漂移问题在长序列中尤为突出，而 Light3R-SfM 通过潜在全局对齐和最短路径树有效抑制了累积误差。

![[assets/figures/papers/paper_list_l47_https_arxiv_org_abs_2501_14914/figures/003_Table_2.jpg]]
*Table 2: Detailed comparison to Spann3R. We compare on Tanks&Temples using the 25 and 50 image subsets as well as the full sequences*

**CO3Dv2 宽基线位姿估计。** Table 3 评估了在随机采样的宽基线场景下的性能。Light3R-SfM 在不同输入图像数下均保持较高的注册率和位姿精度，验证了方法对无序、宽基线图像的鲁棒性。

**Waymo 驾驶场景。** Table 4 显示，Light3R-SfM 的 RRA@5 达到 78.3%，超过 MASt3R-SfM 的 75.7%，同时耗时仅 8.5 秒（MASt3R-SfM 为 1662.0 秒）。Figure 3 的定性对比进一步揭示：MASt3R-SfM 未能真实重建 90° 转弯，而 Spann3R 的预测在数十帧后明显退化，Light3R-SfM 则保持了全局一致的轨迹。

### 消融实验

Table 5 的消融研究揭示了各设计选择的因果贡献：

![[assets/figures/papers/paper_list_l47_https_arxiv_org_abs_2501_14914/figures/007_Table_5.jpg]]
*Table 5: Model ablation. We study the impact of backbone initialization, global supervision, latent alignment as well as different ways for graph construction on pose estimation performance*

**潜在全局对齐模块。** 加入潜在对齐模块后，RRA@5 提升 6.95%，ATE 降低 15.78%。这一结果直接验证了核心因果旋钮的有效性——在特征空间实现多视图信息共享能显著改善成对点图解码的全局一致性，无需任何显式优化。Table 8 进一步表明，潜在对齐层数 L=1 已足够，增加层数未带来额外增益。

**最短路径树 vs. 最小生成树。** 使用 SPT 替代 MST 后，RRA@5 相对提升 15.26%，RTA@5 提升 25.61%。SPT 通过最小化到根节点的路径代价，使树结构更扁平，从而减少广度优先累积过程中的漂移。注意 SPT 和 MST 的边数均为 N-1，解码开销相同，性能提升纯粹来自图拓扑的改进。

**全局监督损失。** 全局损失权重 λ=0.1 取得最优平衡（Table 9）。过大的 λ 会过度约束中间表示，损害成对解码的灵活性；过小则弱化全局一致性信号。

**骨干网络初始化。** 使用 MASt3R 预训练权重初始化编码器/解码器是必要的。Table 10 显示，从头训练导致所有指标大幅下降，表明成对点图回归能力是方法的基础，潜在对齐模块在此之上提供增量式的全局一致性。

**训练图规模。** Table 11 显示，训练时图规模 N=8 已能学到有效的多视图约束。由于显存限制，更大规模的训练图在当前硬件下不可行，这构成了一个已知局限。

### 点图置信度分析

Table 6 分析了学习到的置信度图的过滤效果。Light3R-SfM 的置信度图能有效识别异常点，虽然导致更多帧被拒绝，但保留帧的位姿精度更高。Figure 6 展示了动态物体场景中置信度图的定性表现：模型对动态区域自动分配低置信度，验证了逐点置信度学习机制的有效性。

![[assets/figures/papers/paper_list_l47_https_arxiv_org_abs_2501_14914/figures/010_Table_6.jpg]]
*Table 6: Pointmap confidence analysis on Tanks&Temples [21]. Our learned confidence maps effectively filter outlier points, leading to increased rejected frames yet overall more accurate poses*

### 运行时间分解

Table 7 在 Courthouse 场景（1106 张图像）上分解了各模块的运行时间。潜在全局对齐和 SPT 构建的开销极低，主要耗时集中在编码和解码阶段。整体运行时间与图像数呈近似线性增长，验证了方法的可扩展性。

![[assets/figures/papers/paper_list_l47_https_arxiv_org_abs_2501_14914/figures/008_Table_7.jpg]]
*Table 7: Runtime Analysis. We evaluate Light3R-SfM on the Courthouse scene with 1106 images using a NVIDIA V100-32GB*

### 失败模式与局限性

Figure 11 展示了 Tanks&Temples 上的典型失败案例。主要失败模式包括：

1. **严格阈值下的精度差距。** 尽管在宽松指标（RRA@5、RTA@5）上接近优化式方法，但在更严格的误差阈值下（如 RRA@1），Light3R-SfM 仍明显落后于 MASt3R-SfM 和 GLOMAP。Figure 5 的位姿误差 CDF 曲线直观展示了这一差距。

![[assets/figures/papers/paper_list_l47_https_arxiv_org_abs_2501_14914/figures/011_Figure_5.jpg]]
*Figure 5: CDF of pose errors on 100-view Tanks&Temples scenes*

2. **动态物体干扰。** 包含大量动态物体的场景会导致全局置信度整体下降，影响重建质量。Figure 6 显示模型能检测动态区域，但无法完全消除其对位姿估计的负面影响。

3. **检索图失效导致的场景断裂。** 当基于编码器相似度的检索图构建失败时（如重复纹理、对称结构），SPT 可能将本应连接的子场景分离，导致全局重建断裂成多个不一致的部分。这一问题源于方法完全依赖前馈相似度，缺乏回环检测或重排名机制。

4. **训练图规模限制。** 由于显存约束，训练时图规模限制为 N=8，限制了高阶多视图约束的学习。这可能是严格阈值下精度不足的部分原因。

### 定性分析

Figure 4 展示了潜在全局对齐的隐式场景理解能力：即使对于朝向相反的相机对，解码器也能预测出合理的点图，表明潜在对齐模块确实学到了场景的全局表示。Figure 8 和 Figure 9 分别展示了 Tanks&Temples 和 ETH3D 场景的重建定性结果，Figure 10 提供了 Waymo 场景的更多对比。

![[assets/figures/papers/paper_list_l47_https_arxiv_org_abs_2501_14914/figures/018_Figure_8.jpg]]
*Figure 8: Qualitative examples of reconstruction of Tanks & Temples scenes. Figure 9. Qualitative examples of reconstruction of ETH3D scenes*

### 补充图表

![[assets/figures/papers/paper_list_l47_https_arxiv_org_abs_2501_14914/figures/005_Table_3.jpg]]
*Table 3: Wide-baseline, multi-view camera pose estimation on CO3Dv2 [32]. We vary the number of input images by randomly sampling from the original sequence*

![[assets/figures/papers/paper_list_l47_https_arxiv_org_abs_2501_14914/figures/021_Table_12.jpg]]
*Table 12: Per-scene reconstruction runtimes on Tanks&Temples. All runtimes are reported in seconds*

![[assets/figures/papers/paper_list_l47_https_arxiv_org_abs_2501_14914/figures/004_Table_1.jpg]]
*Table 1: Multi-view pose estimation on Tanks&Temples [21]. We adopt the benchmark by [12] and consider 25/50/100/200 view subsets and using the full sequence. We report relative pose accuracy RRA@5 and RTA@5, absolute translation error (ATE) and registration rate (Reg.). For clarity, we color-code results with a linear gradient between the worst and best result for a given scene. ‘-’ results indicate that all scenes did not converge or that we did not obtain runtime measurements. We specify the type of alignment used by each methods, ‘OPT’ stands for optimizationbased and ‘FFD’ stands for feedforward-based*

![[assets/figures/papers/paper_list_l47_https_arxiv_org_abs_2501_14914/figures/014_Table_9.jpg]]
*Table 9: Impact of weight of global supervision λ*

![[assets/figures/papers/paper_list_l47_https_arxiv_org_abs_2501_14914/figures/015_Table_10.jpg]]
*Table 10: Impact of backbone initialization*

## 方法谱系与知识库定位

### 1. 方法谱系：从优化式 SfM 到前馈式 SfM

Light3R-SfM 处于“前馈式运动恢复结构（Feed-forward SfM）”这一新兴范式与经典优化式 SfM 的交汇点上。其方法谱系可沿两条轴线梳理：

**轴线一：优化式 SfM → 学习式点图回归 → 前馈式 SfM**

- **经典优化式 SfM**：以 **COLMAP** 为代表的增量式方法，以及 **GLOMAP** 为代表的全局式方法，依赖显式的特征提取、匹配、几何验证和迭代式 Bundle Adjustment（BA）。这类方法精度高，但计算开销随图像数量急剧增长，难以扩展到大规模无序图像集。
- **学习式成对点图回归**：**DUSt3R** 首次将成对图像的点图回归引入 SfM 流程，用可学习的解码器替代传统几何匹配。然而，DUSt3R 仍需要穷举式的成对全局对齐与联合优化，本质上并未摆脱优化式后处理的依赖。**MASt3R-SfM** 在此基础上进一步引入特征匹配先验，但整体流程依然以“成对回归 + 全局优化”为核心，在 Tanks&Temples 全序列上耗时达 2723.1 秒（Table 1）。
- **前馈式 SfM**：**Spann3R** 率先尝试用显式记忆库（memory bank）替代 DUSt3R 的全局对齐，实现纯前馈式推理。但其设计面向在线/时序图像，面对无序图像时存在严重的时序漂移问题——在 Tanks&Temples 25 视图设定下，Spann3R 的 RRA@5 仅 19.6%，远低于同场景下 Light3R-SfM 的 50.9%（Table 1）。Light3R-SfM 在此基础上，用**可学习的潜在全局注意力模块**替代显式记忆库，从根本上解决了无序图像的多视图信息共享问题。

**轴线二：场景图构建策略的演化**

- **全连接图**：DUSt3R 的 naive 方案是对所有图像对进行解码，计算量为 $O(N^2)$，内存开销巨大。
- **最小生成树（MST）**：后续工作（包括 Spann3R）采用 MST 将边数压缩至 $N-1$，但 MST 倾向于形成深度较大的链式结构，加剧累积漂移。
- **最短路径树（SPT）**：Light3R-SfM 提出的 SPT 同样保持 $N-1$ 条边，但通过最小化从根节点到各叶子节点的路径代价，使树结构更扁平，显著减少累积漂移。消融实验（Table 5）表明，SPT 相较 MST 使 RRA@5 相对提升 15.26%，RTA@5 提升 25.61%。

### 2. 与基线方法的关键差异

| 方法 | 全局对齐方式 | 场景图 | 推理范式 | 无序图像处理 |
|------|-------------|--------|---------|-------------|
| **MASt3R-SfM** | 迭代全局优化 + BA | 全连接 | 优化式 | 支持，但计算量极大 |
| **Spann3R** | 显式记忆库（在线/离线） | MST | 前馈式 | 存在严重时序漂移 |
| **Light3R-SfM** | 潜在全局注意力（可学习） | SPT | 前馈式 | 原生支持，全局一致 |

核心差异在于**全局信息共享的机制**：MASt3R-SfM 通过显式的成对点图联合优化实现全局一致性，Spann3R 通过记忆库隐式传递时序信息，而 Light3R-SfM 在图像编码与解码之间插入一个可扩展的注意力层——全局 token 间的自注意力实现多视图信息交换，再通过交叉注意力将全局上下文传播回各图像的密集 token。这意味着成对解码器在运行时已经“看到”了全局场景信息，从而无需后处理优化即可获得全局一致的点图。

### 3. 适用边界与局限

**适用场景**：
- 大规模无序图像集的快速重建（数百至上千张图像），如 Tanks&Temples 的 Courthouse 场景（1106 张图像）可在 63.4 秒内完成（Table 1）。
- 宽基线场景（如 CO3Dv2），Light3R-SfM 在 10 视图设定下 RRA@5 达 57.4，与 MASt3R-SfM 的 60.3 接近（Table 3）。
- 自动驾驶场景（如 Waymo），Light3R-SfM 在 RRA@5 上以 78.3 超越 MASt3R-SfM 的 75.7（Table 4）。

**已知局限**：
1. **严格阈值下的精度差距**：在 RRA@5 等紧阈值指标上，Light3R-SfM 仍明显落后于 MASt3R-SfM 和 GLOMAP。例如在 Tanks&Temples 25 视图设定下，Light3R-SfM 的 RRA@5 为 50.9，而 MASt3R-SfM 为 68.0（Table 1）。这表明纯前馈式回归在精细几何精度上尚无法完全替代迭代优化。
2. **动态物体敏感**：模型在包含大量动态物体的场景中，全局置信度会明显下降，影响重建质量（Figure 6）。
3. **检索失败导致场景断裂**：SPT 构建依赖于编码器嵌入的余弦相似度。当检索分数不可靠时，可能导致全局场景断裂成多个不一致的子重建（Figure 11 展示了此类失败案例）。
4. **训练图规模受限**：由于显存约束，训练时的图规模仅为 $N=8$（Table 11），限制了高阶多视图约束的学习。这可能是模型在紧阈值下精度不足的深层原因之一。

### 4. 开放问题与后续方向

从论文分析和实验证据出发，以下问题值得关注：

1. **极大规模扩展**：当前模型在 1106 张图像上已验证可行性（Table 7），但如何扩展到数万张图像的场景（如城市级重建）仍是一个开放问题。潜在注意力的计算复杂度与 $N$ 呈线性关系（通过全局 token 分解），但编码器和解码器的内存占用仍可能成为瓶颈。

2. **前馈 + 轻量优化的混合范式**：论文的核心洞察是“在特征空间完成全局对齐，避免显式优化”。但精度差距提示，是否可以在纯前馈回归的基础上叠加一个小型轻量优化模块（如仅对关键帧进行局部 BA），在保持高速的同时大幅提升紧阈值下的精度？这是一个自然且有实际价值的延伸方向。

3. **检索鲁棒性增强**：当前 SPT 构建完全依赖编码器嵌入的余弦相似度。当检索失败导致场景断裂时，是否可以通过引入回环检测、重排名策略或几何一致性验证来提升鲁棒性？这是一个工程上重要但论文未深入探讨的问题。

4. **动态场景建模**：模型对动态物体的处理能力有限。是否可以通过在训练数据中增加含动态物体的场景，或引入运动分割模块，使模型具备更强的动态场景适应性？

5. **与后续工作的潜在关联**：Light3R-SfM 提出的“潜在注意力 + SPT”框架为前馈式 SfM 提供了一个可扩展的基础架构。后续工作可以在此基础上探索：更高效的注意力变体（如线性注意力）、多尺度全局 token、以及与其他 3D 表示（如 3D Gaussian Splatting）的直接结合。

## 原文 PDF

![[paperPDFs/CVPR_2025/Light3R_SfM_Towards_Feed_forward_Structure_from_Motion.pdf]]
