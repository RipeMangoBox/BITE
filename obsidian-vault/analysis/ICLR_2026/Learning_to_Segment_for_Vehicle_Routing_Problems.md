---
title: "Learning to Segment for Vehicle Routing Problems"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Learning_to_Segment_for_Vehicle_Routing_Problems.pdf
openreview_forum_id: pN261iTKvr
aliases:
- LSLFSTAF
- LSVRP
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/probabilistic_methods
core_operator: "通过学习识别哪些边缘不稳定，将稳定段聚合成超节点以减小问题规模，从而将搜索集中在不稳定部分，显著加速迭代求解。"
primary_logic: "首次将稳定性感知引入迭代求解器的搜索过程，通过端到端学习预测不稳定边缘，并利用 FSTA 框架将稳定段聚合为超节点，实现了加速的同时保持解的质量。"
claims:
- "在迭代求解过程中，大多数边缘保持不变，说明了冗余计算的存在。"
- "L2Seg-SYN 在学习指导下识别不稳定边缘，其加速效果远优于随机选择不稳定边缘的 FSTA 方法。"
- "L2Seg 可将不同的迭代求解器加速 2 倍至 7 倍，证明了其广泛的适用性。"
- "CVRP2k (large-capacity) 上 Obj↓ (LNS backbone) = 43.42"
---

# Learning to Segment for Vehicle Routing Problems

> [!tip] 核心洞察
> 首次将稳定性感知引入迭代求解器的搜索过程，通过端到端学习预测不稳定边缘，并利用 FSTA 框架将稳定段聚合为超节点，实现了加速的同时保持解的质量。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 学习分割车辆路径问题 |
| 英文题名 | Learning to Segment for Vehicle Routing Problems |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=pN261iTKvr) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/probabilistic_methods |
| Method | Learning to Segment (L2Seg) with First-Segment-Then-Aggregate (FSTA) |
| Dataset | CVRP2k (large-capacity), CVRP5k (large-capacity), CVRP5k (small-capacity), VRPTW5k |

> [!tip] 效果简介
> - CVRP2k (large-capacity) 上，Obj↓ (LNS backbone) 为 43.42，对比 44.92，变化 -1.50 (3.34% gain)。
> - CVRP5k (large-capacity) 上，Obj↓ (LNS backbone) 为 63.94，对比 64.69，变化 -0.75 (1.16% gain)。
> - CVRP5k (small-capacity) 上，Gap vs HGS (%) 为 -3.55%，对比 0% (HGS)，变化 低于 HGS 3.55%。

## 概述

大规模车辆路径问题（VRP）的迭代求解过程中存在一个被忽视的关键瓶颈：**绝大多数解分量在搜索迭代间保持稳定，导致大量冗余计算**。实证分析显示，在使用经典求解器 LKH-3 对 100 个 CVRP 实例进行迭代搜索时，大部分边在连续迭代中保持不变（Figure 1），这意味着求解器反复在已经收敛的区域浪费计算资源，严重制约了可扩展性。

针对这一瓶颈，本文提出 **Learning to Segment (L2Seg)** 框架，核心思路是**学习识别解中不稳定的边**，进而通过 **First-Segment-Then-Aggregate (FSTA)** 分解策略将稳定段聚合为超节点，大幅缩小问题规模，使骨干求解器仅需在缩小的子问题上集中搜索。这一“稳定性感知”的设计首次将端到端学习引入迭代求解器的搜索过程，实现了加速与解质量的兼顾。

L2Seg 提供三种解码器变体：**L2Seg-NAR**（非自回归，一次性全局预测）、**L2Seg-AR**（自回归，逐步建模局部依赖）以及 **L2Seg-SYN**（协同推理，结合 NAR 的全局识别与 AR 的局部精化）。FSTA 框架则通过识别不稳定边、提取稳定段、聚合超节点等步骤，将原始问题转化为规模显著缩小的子问题，供骨干求解器高效重优化。

在实验验证中，L2Seg 展现出三个决定性优势：

1. **广泛适用性**：可将 LKH-3、LNS、L2D 等不同类型的迭代求解器加速 **2 倍至 7 倍**（Figure 5），在 CVRP2k 上 LNS 骨干的目标值从 44.92 降至 43.42（3.34% 增益），在 CVRP5k 上从 64.69 降至 63.94（1.16% 增益）（Table 1）。
2. **学习信号的有效性**：L2Seg-SYN 显著优于随机选择不稳定边的 Random FSTA 方法（Table 3），证明模型学到了问题结构中的稳定性模式，而非简单依赖分解框架本身。
3. **跨求解器泛化**：训练标签在不同求解器（HGS 与 LKH-3）之间具有 78.3% 的相似度（Table 5），表明稳定性主要由实例结构决定，而非特定求解器行为，这为模型的零样本泛化能力提供了基础。

在方法谱系中，L2Seg 定位于**学习引导的迭代求解加速**，区别于端到端构造方法（如 AM、POMO）和完全手工设计的分解策略（如 LNS 的邻域破坏）。其神经网络推理开销始终低于总迭代时间的 10%（Table 15），在计算效率上具备实用价值。当前验证集中于 CVRP 和 VRPTW，扩展到更广泛的 VRP 变体及与 HGS 等闭箱求解器的集成仍是开放问题。

## 背景与动机

车辆路径问题（Vehicle Routing Problem, VRP）是组合优化领域的核心问题之一，在物流配送、共享出行等场景中具有广泛的应用价值。随着问题规模的增长，精确求解器因指数级的时间复杂度而难以在可接受的时间内获得最优解，迭代启发式求解器成为大规模 VRP 的主要求解手段。然而，当前迭代求解器面临一个关键瓶颈：**在迭代搜索过程中，大部分解结构保持稳定，导致大量冗余计算，严重限制了求解器的可扩展性和效率**。

这一现象在 **Figure 1** 中得到了实证支持：在使用 **LKH-3**（Helsgaun, 2017）对 100 个 CVRP 实例进行迭代搜索时，每一轮迭代中仅有少量边被重新优化，绝大多数边保持不变。这意味着求解器在每一轮迭代中重复计算了大量已收敛的路径片段，造成了计算资源的浪费。这一冗余计算问题在大规模实例（如 CVRP2k、CVRP5k）上尤为突出，因为随着节点数增加，稳定段的规模也随之扩大，但求解器仍需对整个解空间进行全局搜索。

现有方法在应对这一问题时存在明显缺口。传统的分解策略——如 **LNS**（Shaw, 1998）基于预定义邻域选择相邻子路径进行破坏与修复——依赖手工设计的启发式规则，无法自适应地识别哪些解片段真正需要重新优化。近年来兴起的神经组合优化方法，如 **L2D**（Li et al., 2021）通过学习将子问题委派给不同求解器，虽然在一定程度上提升了求解效率，但并未从根本上解决迭代搜索中的冗余计算问题。当前最优的经典启发式求解器 **HGS**（Vidal, 2022）虽然解质量出色，但其设计并不接受初始解输入，难以与分解-聚合框架直接集成。

本文的核心动机源于一个关键洞察：**如果能够提前识别解中哪些边不稳定、哪些边保持稳定，就可以将稳定段聚合成超节点以缩小问题规模，从而将搜索资源集中到真正需要优化的不稳定部分**。这一思路将稳定性感知首次引入迭代求解器的搜索过程，有望在不牺牲解质量的前提下实现显著的加速效果。为此，本文提出 **Learning to Segment（L2Seg）** 框架，通过端到端学习预测不稳定边，并结合 **First-Segment-Then-Aggregate（FSTA）** 分解框架，将稳定段聚合为超节点，使骨干求解器仅需在简化后的子问题上进行搜索，从而在保证解质量的同时实现 2 至 7 倍的加速。

## 核心创新

### 创新动机：迭代搜索中的冗余计算

在大规模车辆路径问题（VRP）的迭代求解过程中，一个关键但长期被忽视的现象是：**大部分解结构在搜索过程中保持稳定**。Figure 1 的实证分析显示，使用 **LKH-3**（Helsgaun, 2017）对 100 个 CVRP 实例进行迭代搜索时，仅有少量边缘被重新优化，绝大多数边缘保持不变。这意味着传统迭代求解器将大量计算资源浪费在重复处理已经收敛的稳定区域上，形成了严重的**冗余计算瓶颈**。

### 核心因果机制：稳定性感知的搜索聚焦

L2Seg 的核心创新在于**首次将稳定性感知引入迭代求解器的搜索过程**。其因果逻辑链为：

1. **识别不稳定区域**：通过端到端学习，预测当前解中哪些边缘（edges）可能在后续搜索中被修改；
2. **稳定段聚合**：利用 FSTA（First-Segment-Then-Aggregate）框架，将连续稳定边缘连接的节点段聚合成超节点（hypernodes），大幅缩小问题规模；
3. **搜索聚焦**：骨干求解器仅在由不稳定边缘构成的子问题上运行，将计算资源集中投入最有改进潜力的区域。

这一机制实现了**加速与解质量的兼顾**：稳定段的解结构被完整保留，而搜索能力被精准投放到需要优化的局部。

### 关键方法创新：L2Seg 与 FSTA 的协同设计

#### Changed Slot 1：不稳定边缘识别策略

| 维度 | Baseline | L2Seg |
|------|----------|-------|
| 识别方式 | 随机选择（Random FSTA）或无分解的传统求解器 | 深度学习模型（NAR/AR/SYN）预测 |
| 证据 | — | Table 3：L2Seg-SYN 显著优于 Random FSTA |

传统 FSTA 框架若采用随机策略选择不稳定边缘，无法有效定位真正需要优化的区域。L2Seg 通过三个模型变体实现学习驱动的边缘预测：

- **L2Seg-NAR**（非自回归）：一次性全局预测每个节点的不稳定概率，速度快但精度有限；
- **L2Seg-AR**（自回归）：逐步建模局部依赖关系，通过交替执行删除和插入阶段来预测不稳定边缘序列，精度高但计算开销较大；
- **L2Seg-SYN**（协同推理）：结合 NAR 的全局识别能力和 AR 的局部细化能力，采用四步协同流程——子问题分解、NAR 全局检测不稳定节点、K-means 聚类定位不稳定区域、AR 从初始节点出发局部细化边缘预测（Figure 2）。

Table 4 的分析表明，L2Seg-SYN 在 CVRP2k 上实现了**召回率（Recall）与真负率（TNR）的最佳平衡**，这是其性能优于单独使用 NAR 或 AR 的关键原因。

#### Changed Slot 2：分解范围和方法

| 维度 | Baseline | L2Seg |
|------|----------|-------|
| 分解方式 | 基于预定义邻域的手工分解（如 LNS 选择相邻子路径） | 基于学习信号的全局边缘级 FSTA 分解 |
| 证据 | — | Section 2 & Appendix C.1 |

传统分解方法（如 **LNS**（Shaw, 1998）的邻域选择）依赖手工设计的规则，无法感知解的全局稳定性结构。L2Seg 的 FSTA 框架实现了**全局边缘级分解**：不稳定边缘可以同时破坏多个子路径中的连接，而稳定段被聚合成超节点保留。这种分解方式不受路径边界限制，能够更精准地捕获跨路径的优化机会。

### 方法谱系与知识库定位

L2Seg 在神经组合优化（NCO）领域的方法谱系中占据独特位置：

- **相对于经典求解器**（**LKH-3**, Helsgaun 2017; **HGS**, Vidal 2022）：L2Seg 并非替代而是**加速**这些求解器，通过 FSTA 框架将问题规模缩小后调用它们作为骨干求解器，实现了 2× 至 7× 的加速（Figure 5）；
- **相对于学习引导的混合求解器**（**L2D**, Li et al., 2021）：L2D 通过学习将子问题委托给不同求解器，而 L2Seg 聚焦于**识别解的稳定结构以缩小搜索空间**，两者互补且 L2Seg 可与 L2D 集成（Table 1 中 L2Seg-SYN-L2D 的组合验证了这一点）；
- **相对于 NCO 中的 AR/NAR 模型**：L2Seg 首次在 NCO 领域实现了 AR 与 NAR 模型的协同推理（L2Seg-SYN），为联合决策问题提供了新的范式。

### 理论支撑

FSTA 框架的适用性得到了形式化研究和理论证明（Section 1），覆盖了多种 VRP 变体，确保了方法的理论基础不仅限于经验验证。

### 创新边界与局限

需要指出的是，L2Seg 目前仅在 CVRP 和 VRPTW 上进行了验证，扩展到其他 VRP 变体（如 VRPB、VRPPD）以及更广泛的组合优化问题仍有待探索。此外，L2Seg 尚未与 **HGS**（Vidal, 2022）等不接受初始解输入的顶级求解器集成，限制了其在某些场景下的直接应用。训练数据生成依赖于预定义的骨干求解器，可能引入求解器特异性偏差，但 Table 5 显示 HGS 和 LKH-3 的标签相似度达 78.3%，表明**稳定性主要由问题实例的内在结构决定**，偏差有限。

## 整体框架

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_pN261iTKvr/figures/002_Figure_2.jpg]]
*Figure 2: The overview of our FSTA decomposition framework (top) and the three proposed L2Seg models (bottom). L2Seg-SYN employs a four-step synergized approach: (1) problem decomposition into subproblems, (2) unstable nodes detection globally via NAR decoding, (3) clustering of NARpredicted nodes to localize unstable regions and select initial target nodes, and (4) refining unstable edge predictions locally via AR decoding starting from these identified initial target nodes*

L2Seg 的核心 pipeline 由两个紧密耦合的阶段构成：**学习驱动的稳定性预测**与**结构感知的问题简化**。整个框架以“先分割、后聚合”（First-Segment-Then-Aggregate, FSTA）为理论基础，将迭代求解过程中不必要的冗余计算转化为可学习的边缘稳定性识别任务。

### FSTA 分解框架

FSTA 是 L2Seg 的上层框架，其设计动机源于一个关键观察：在大规模 VRP 的迭代搜索中，大部分解片段保持稳定，仅有少量边缘被反复重优化（Figure 1 显示 LKH-3 在 100 个 CVRP 实例上仅重优化了极少比例的边缘）。FSTA 通过以下步骤将这一观察转化为计算收益：

1. **不稳定边缘识别**：给定当前解 $R$，识别其中可能被重优化的不稳定边缘集合。
2. **稳定段聚合**：将稳定边缘连接的节点段聚合成超节点（hypernodes），大幅缩减问题规模。
3. **聚焦重优化**：在简化后的问题上调用骨干求解器，将搜索资源集中投入不稳定区域。
4. **解的重构**：将简化问题的优化结果映射回原始问题的完整解。

这一框架的核心因果杠杆在于：**通过精确识别不稳定边缘，将求解器的搜索空间从全局压缩到局部关键区域**，从而在不牺牲解质量的前提下实现显著加速。

### L2Seg 学习框架

L2Seg 作为 FSTA 的“感知模块”，负责从数据中学习预测不稳定边缘。其架构采用编码器-解码器范式，提供三种互补的预测变体：

**编码器** 将节点特征与边特征融合为统一的嵌入表示。编码器由 Transformer 层和图神经网络层组成，通过注意力机制整合图级和路径级特征，并利用路径掩码阻止不同子路径节点间的无效计算。

**三种解码器变体** 分别对应不同的预测策略：

- **L2Seg-NAR（非自回归）**：一次性全局预测每个节点的不稳定概率 $\mathbf{p}^{\mathrm{NAR}} = \mathrm{MLP}_{\mathrm{NAR}}(\mathbf{H}^{\mathrm{GNN}})$，将与不稳定节点相连的所有边标记为不稳定。优点是速度快，适合快速全局扫描。
- **L2Seg-AR（自回归）**：逐步建模不稳定边缘的局部依赖关系，交替执行删除（识别不稳定边）和插入（引入桥接伪边）两个阶段。删除阶段使用浅层解码器（1层MHA），插入阶段使用更深解码器（4层MHA），以精细捕捉局部搜索行为中的序列模式。
- **L2Seg-SYN（协同推理）**：结合 NAR 的全局召回能力与 AR 的局部精确性，通过四步流程实现互补协同：(1) 将问题分解为子问题；(2) 通过 NAR 解码全局检测不稳定节点；(3) 对 NAR 预测的不稳定节点进行聚类，定位不稳定区域并选择初始目标节点；(4) 从这些初始节点出发，通过 AR 解码局部细化不稳定边缘预测。

### 训练与推理流程

训练阶段采用模仿学习范式：以迭代求解器（如 LKH-3 或 HGS）作为前瞻启发式，通过比较重优化前后的解差异生成不稳定边缘的真实标签。NAR 模型使用加权二元交叉熵损失 $\mathcal{L}_{\mathrm{NAR}}$（正样本权重 $w_{\mathrm{pos}} > 1$），AR 模型使用加权交叉熵损失 $\mathcal{L}_{\mathrm{AR}}$（插入阶段权重 $w_{\mathrm{insert}} >$ 删除阶段权重 $w_{\mathrm{delete}}$），以平衡数据集中不稳定边缘的稀疏性。

推理阶段，L2Seg-SYN 的神经网络开销始终低于总迭代时间的 10%（Table 15），证明其扩展效率可控。预测结果直接输入 FSTA 框架，驱动问题简化与聚焦求解，最终实现对 LKH-3、LNS、L2D 等骨干求解器 2 至 7 倍的加速（Figure 5）。

## 核心模块与公式推导

### 编码器：融合图级与路径级特征

L2Seg 的编码器负责将 VRP 实例的节点和边特征转化为富含结构信息的嵌入向量。输入特征包括节点坐标、需求量和边距离等，经过线性投影后，编码器使用 $L_{\text{TFM}}$ 层带掩码的 Transformer 进行处理。掩码机制的关键作用在于阻止不同子路径（route）之间节点的注意力计算，确保路径内部的拓扑关系被优先建模，同时避免跨路径的噪声干扰。编码器输出节点嵌入 $\mathbf{H}^{\text{GNN}}$，作为后续解码器的共享表示。

### NAR 解码器：一次性全局不稳定节点预测

非自回归（NAR）解码器采用全局并行预测策略，直接输出每个节点的不稳定概率：

$$\mathbf{p}^{\mathrm{NAR}} = \mathrm{MLP}_{\mathrm{NAR}}(\mathbf{H}^{\mathrm{GNN}})$$

其中 $\mathbf{p}^{\mathrm{NAR}} \in [0,1]^{|V|}$ 表示每个节点属于不稳定节点的概率，$\mathrm{MLP}_{\mathrm{NAR}}$ 是一个轻量级的多层感知机。NAR 解码器将节点级预测转化为边级判断：若某节点被预测为不稳定，则其所有关联边均被标记为不稳定边。这种设计的优势在于推理速度快，但代价是可能过度预测不稳定区域。

NAR 模型的训练损失为加权二元交叉熵：

$$\mathcal{L}_{\mathrm{NAR}} = -\sum_{y_{x_k} \in y^{ij}} \left[ w_{\mathrm{pos}}\, y_{x_k} \log(p_k^{\mathrm{NAR}}) + (1-y_{x_k}) \log(1-p_k^{\mathrm{NAR}}) \right]$$

其中 $y_{x_k} \in \{0,1\}$ 是节点 $x_k$ 的不稳定性标签，$w_{\mathrm{pos}} > 1$ 是对正样本（不稳定节点）的加权系数。由于不稳定节点在数据中占比较低，加权机制能有效缓解类别不平衡问题，迫使模型更关注少数类样本的召回。

### AR 解码器：逐步建模局部依赖关系

自回归（AR）解码器以序列化方式逐步预测不稳定边，其核心设计是交替执行**删除阶段**和**插入阶段**。删除阶段识别当前解中应被移除的边，插入阶段则引入伪边以桥接至下一个待删除的不稳定边，从而建模不稳定边之间的局部依赖结构。

在每一步解码中，AR 解码器通过注意力机制计算节点选择得分：

$$u_i = \begin{cases} (W_q \mathbf{h}^{\mathrm{c}})^T W_k \mathbf{h}_i^{(L^{\mathrm{MHA}})} / \sqrt{d_h}, & \text{if } i > 3 \\ -\infty, & \text{otherwise} \end{cases}$$

其中 $\mathbf{h}^{\mathrm{c}}$ 是上下文嵌入，$\mathbf{h}_i^{(L^{\mathrm{MHA}})}$ 是第 $i$ 个节点经过 $L^{\mathrm{MHA}}$ 层多头注意力后的表示，$d_h$ 是注意力头维度。$i \leq 3$ 的位置被掩码为 $-\infty$，用于屏蔽编码器中的特殊嵌入位置（如起点、终点标记），确保解码器仅从有效节点中选择。

AR 解码器在删除阶段使用浅层结构（$L_{\text{delete}}^{\mathrm{MHA}} = 1$），在插入阶段使用更深的结构（$L_{\text{insert}}^{\mathrm{MHA}} = 4$）。这种非对称设计反映了两个阶段的认知差异：删除操作相对直接，而插入操作需要更复杂的推理以找到合适的桥接边。解码器的初始隐藏状态由所有节点嵌入的平均值初始化：

$$\mathbf{h}_0^{\mathrm{hidden}} = \frac{1}{|V|} \sum_{i=0}^{|V|} \mathbf{h}_i^{\mathrm{GNN}}$$

序列终止由一个可学习的终止嵌入 $\mathbf{h}^{\mathrm{end}}$ 控制：

$$\mathbf{h}^{\mathrm{end}} = \alpha \mathbf{h}_{\pi_0}^{\mathrm{GNN}} + (1-\alpha) \frac{1}{|V|} \sum_{i=0}^{|V|} \mathbf{h}_i^{\mathrm{GNN}}$$

其中 $\alpha$ 是可学习参数，$\mathbf{h}_{\pi_0}^{\mathrm{GNN}}$ 是序列起始节点的嵌入。该设计使终止信号既能感知局部上下文，又能参考全局信息。

AR 模型的训练损失为加权交叉熵，分别对删除和插入阶段赋予不同权重：

$$\mathcal{L}_{\mathrm{AR}} = -\sum_{x_{\pi_{2k}} \in y_K} w_{\mathrm{insert}} \log(p_{\pi_{2k}}^{\mathrm{AR}}) - \sum_{x_{\pi_{2k+1}} \in y_K} w_{\mathrm{delete}} \log(p_{\pi_{2k+1}}^{\mathrm{AR}})$$

其中 $w_{\mathrm{insert}} > w_{\mathrm{delete}}$，对插入阶段的预测赋予更高权重。这一设计源于插入操作对最终解质量影响更大——错误的插入可能导致子路径断裂，而错误的删除相对容易被后续搜索修正。

### L2Seg-SYN 协同推理

L2Seg-SYN 将 NAR 的全局感知能力与 AR 的局部精炼能力相结合，形成四步协同推理流程：首先将问题分解为子问题，然后通过 NAR 解码器全局检测不稳定节点，接着对 NAR 预测的不稳定节点进行 K-means 聚类以定位不稳定区域并选择初始目标节点，最后以这些初始节点为起点进行 AR 解码，局部精炼不稳定边预测。这种协同设计使 L2Seg-SYN 在召回率和真负率（TNR）之间取得了最佳平衡——NAR 提供较高的召回率，AR 提供较高的 TNR，二者互补实现了最优的加速与解质量权衡。

## 实验与分析

### 核心瓶颈与动机验证

在大规模车辆路径问题（VRP）的迭代求解过程中，一个被长期忽视的关键现象是解的**稳定性**：Figure 1 显示，在使用 LKH-3（Helsgaun, 2017）对 100 个 CVRP 实例进行迭代搜索时，绝大多数边在迭代间保持不变，只有少量边被重新优化。这一实证发现揭示了迭代求解器中普遍存在的**冗余计算**——求解器在每一轮迭代中对大量已经稳定的解片段进行重复搜索，严重限制了求解器在大规模实例上的可扩展性和效率。

L2Seg 的核心洞察正是将这种稳定性感知引入迭代求解器的搜索过程：通过端到端学习预测哪些边不稳定，将稳定段聚合成超节点以缩小问题规模，从而将搜索资源集中到不稳定的局部区域。

### 主要实验结果

#### 大规模 CVRP 上的加速与质量提升

Table 1 报告了 L2Seg 三种变体（L2Seg-NAR、L2Seg-AR、L2Seg-SYN）在大容量 CVRP 实例上加速三个骨干求解器（LKH-3、LNS、L2D）的性能。在 CVRP2k 上，L2Seg-SYN 对 LNS 骨干求解器实现了 **3.34% 的目标值增益**（Obj 43.42 vs. 44.92），对 LKH-3 实现了 2.92% 的增益；在 CVRP5k 上，L2Seg-SYN 对 LNS 实现 1.16% 增益（Obj 63.94 vs. 64.69），对 LKH-3 实现 1.87% 增益。值得注意的是，L2Seg-SYN 在所有骨干求解器和问题规模上均一致优于单独的 NAR 和 AR 变体，验证了协同推理的有效性。

Figure 5 的搜索曲线进一步揭示了加速效果的时间维度：L2Seg 在不同骨干求解器上实现了 **2 倍至 7 倍的加速**，即在相同时间预算内，L2Seg 增强的求解器能够达到传统求解器需要数倍时间才能获得的解质量。

#### 基准数据集上的竞争力

Table 2 将 L2Seg-SYN-L2D 与当前最优经典启发式求解器 HGS（Vidal, 2022）在标准 CVRP 和 VRPTW 基准上进行对比。在小容量 CVRP5k 上，L2Seg-SYN-L2D 相对于 HGS 的 gap 为 **-3.55%**；在 VRPTW5k 上，gap 为 **-3.14%**。这表明 L2Seg 不仅在加速方面有效，而且在绝对解质量上也具有竞争力，尽管其骨干求解器本身并非当前最优。


![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_pN261iTKvr/figures/008_Table_2.jpg]]
*Table 2: Performance comparisons of our L2Seg-SYN-L2D against baselines on benchmark CVRP and VRPTW instances. The gap % (lower the better) is w.r.t. the performance of HGS*

### 消融研究

#### 学习预测 vs. 随机选择

Table 3 的关键消融对比了 L2Seg-SYN 与 Random FSTA（随机选择不稳定边缘的 FSTA 方法）在加速 LNS 求解器上的表现。结果显示，L2Seg-SYN 在所有 CVRP 实例上显著优于 Random FSTA，证明了**学习预测不稳定边缘**是加速效果的核心来源，而非 FSTA 分解框架本身的简单效果。


![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_pN261iTKvr/figures/009_Table_3.jpg]]
*Table 3: Performance of L2Seg-SYN v.s. Random FSTA to accelerate LNS on CVRP instances*

#### NAR 与 AR 的协同机制

Table 4 从预测分析角度解释了 L2Seg-SYN 优于单独变体的原因。在 CVRP2k 上，L2Seg-NAR 具有较高的召回率（Recall）但真负率（TNR）较低，倾向于过度预测不稳定边；L2Seg-AR 具有较高的 TNR 但召回率不足，倾向于遗漏不稳定区域。L2Seg-SYN 结合了 NAR 的全局识别能力（高召回率）和 AR 的局部细化能力（高 TNR），在召回率和 TNR 之间取得了最佳平衡，最终实现了最优的目标值（Obj 43.42）。Figure 6 和 Figure 12 从概念和案例层面可视化了这一协同行为。


![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_pN261iTKvr/figures/026_Figure_12.jpg]]
*Figure 12: Prediction comparison of L2Seg-SYN, L2Seg-NAR, and L2Seg-AR on two adjacent routes from a small-capacity CVRP1k solution. Red dashed lines indicate predicted unstable edges. L2Seg-SYN provides the most reasonable predictions, while L2Seg-NAR over-predicts unstable edges and L2Seg-AR fails to identify unstable regions*

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_pN261iTKvr/figures/011_Table_4.jpg]]
*Table 4: Model prediction analysis of L2Seg-LNS on CVRP2k*

#### 训练标签的求解器特异性

Table 5 分析了不同求解器（HGS 和 LKH-3）生成的训练标签之间的相似度，结果为 **78.3%**。这一较高的相似度表明，解的稳定性主要由**问题实例的内在结构**决定，而非特定求解器的搜索行为。这一发现降低了 L2Seg 对特定骨干求解器的过拟合风险，也为跨求解器的迁移训练提供了依据。


![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_pN261iTKvr/figures/013_Table_5.jpg]]
*Table 5: Label similarity across different solvers*

#### 超参数敏感性

Figure 11 分析了两个关键超参数：K-means 聚类数 `nKMEANS` 和平衡因子 `η`。结果表明 `nKMEANS=3` 和 `η=0.6` 是最佳配置，偏离这些值会导致性能下降，但总体变化幅度可控，说明方法对超参数具有一定的鲁棒性。


![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_pN261iTKvr/figures/022_Figure_11.jpg]]
*Figure 11: Analysis of key hyperparameters: (a) number of clusters nMEANS, and (b) balancing factor η*

### 泛化性与计算开销

#### 零样本泛化

Table 12 验证了 L2Seg 在分布外实例上的泛化能力。在聚类分布 CVRP 和异构需求 CVRP 上，L2Seg 在零样本设置下（即未在这些分布上训练）对 LNS 骨干求解器实现了 **1.23% 至 3.10%** 的增益，证明了学习到的稳定性模式具有一定的分布迁移能力。

#### 计算开销

Table 15 详细分析了 L2Seg 的神经网络推理开销。在所有问题规模下，L2Seg-SYN 的推理时间始终**低于总迭代时间的 10%**。这一可控的开销确保了加速效果并非来自不公平的额外计算预算，而是真正来自搜索效率的提升。

### 局限性

尽管 L2Seg 在 CVRP 和 VRPTW 上展现了显著的加速效果，仍存在以下局限：（1）当前验证范围仅限于 CVRP 和 VRPTW，扩展到其他 VRP 变体（如 VRPB、VRPPD）以及更广泛的组合优化问题仍有待探索；（2）L2Seg 尚未与 HGS 等不接受初始解输入的顶级求解器集成，限制了其直接应用范围；（3）神经网络推理开销虽可控（<10%），但在极短时间限制下可能影响性价比；（4）训练数据生成依赖于预定义的骨干求解器，可能引入求解器特异性偏差，但 Table 5 的标签相似度分析表明这种偏差有限。

### 补充图表

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_pN261iTKvr/figures/015_Figure.jpg]]
*Figure: (a) Random instance 1 at step 1*

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_pN261iTKvr/figures/016_Figure_9.jpg]]
*Figure 9: Illustration of our FSTA applied to one CVRP instance. Each FSTA step corresponds to the descriptions in Appendix B.1.4. Red dashed lines: unstable edges; blue dashed lines: re-optimized edges. Note that the subproblem (d) contains substantially fewer nodes than the original instance (a)*

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_pN261iTKvr/figures/007_Table.jpg]]

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_pN261iTKvr/figures/014_Table.jpg]]

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_pN261iTKvr/figures/017_Table_7.jpg]]
*Table 7: Implementation specifications of FSTA hypernode aggregation for CVRP, VRPTW, VRPB variants. Refer to Equation 3 for the definitions of $\bar { \bar { s } } _ { j } , \bar { t } _ { j } ^ { l }$ and $\bar { \bar { t } } _ { j } ^ { r }$


## 方法谱系与知识库定位

### 1. 与迭代启发式求解器的关系

L2Seg 的核心定位是**迭代启发式求解器的通用加速器**，而非独立的端到端求解器。它通过 FSTA（First-Segment-Then-Aggregate）框架将稳定解段聚合为超节点，从而缩小问题规模，使骨干求解器仅需在显著缩小的不稳定子问题上进行搜索。

该方法与以下骨干求解器进行了集成验证：

- **LKH-3**（Helsgaun, 2017）：经典的基于 k-opt 交换的迭代启发式求解器。L2Seg-SYN-LKH-3 在 CVRP2k 上实现 2.92% 的增益，在 CVRP5k 上实现 1.87% 的增益（Table 1）。

- **LNS**（Shaw, 1998）：基于分解的大邻域搜索求解器。L2Seg-SYN-LNS 在 CVRP2k 上实现 3.34% 的增益，在 CVRP5k 上实现 1.16% 的增益（Table 1）。值得注意的是，LNS 本身已采用分解策略（选择相邻子路径进行破坏-重建），而 L2Seg 的 FSTA 分解在粒度上与之有本质区别——FSTA 是基于学习信号的全局边缘级分解，可同时破坏所有子路径中的不稳定边缘，而非局限于预定义的邻域结构。

- **L2D**（Li et al., 2021）：学习引导的混合求解器（Learning to Delegate）。L2Seg-SYN-L2D 在标准 CVRP5k 上相对于 HGS 的 Gap 为 -3.55%，在 VRPTW5k 上为 -3.14%（Table 2）。

### 2. 与端到端神经求解器的关系

L2Seg 与端到端构造式或改进式神经求解器（如 AM、POMO、N2S 等）属于不同的技术路线。端到端方法试图直接从问题实例映射到完整解，而 L2Seg 采用**学习增强搜索**的范式：神经网络负责识别解的稳定性结构，搜索仍由成熟的迭代启发式求解器完成。这种分工使得 L2Seg 能够继承骨干求解器的理论保证和工程优化，同时利用学习信号消除冗余计算。

### 3. 方法谱系中的关键创新

| 维度 | 传统迭代求解器 | 现有学习增强方法 | L2Seg (本文) |
|------|---------------|-----------------|-------------|
| 分解策略 | 手工预定义（如 LNS 的相邻子路径） | 基于策略网络的破坏选择 | 学习驱动的全局边缘级 FSTA 分解 |
| 稳定性利用 | 无显式建模 | 无 | 端到端学习预测不稳定边缘 |
| 解码范式 | N/A | 单一 AR 或 NAR | AR-NAR 协同（SYN） |
| 骨干求解器兼容性 | N/A | 通常绑定特定求解器 | 通用加速器，已验证 LKH-3/LNS/L2D |

FSTA 框架本身在理论上被证明适用于多种 VRP 变体（论文声称进行了形式化研究和理论证明），但在实验中仅验证了 CVRP 和 VRPTW。L2Seg 开创性地将 AR 和 NAR 模型的协同引入神经组合优化领域——NAR 提供快速的全局不稳定节点检测（高召回率），AR 提供精确的局部边缘细化（高 TNR），两者互补（Table 4 证实了这种互补性）。

### 4. 适用边界与局限

**已验证的适用范围：**
- CVRP（大容量均匀分布、小容量标准基准、聚类分布、异构需求）
- VRPTW（带时间窗的车辆路径问题）
- 问题规模：1k 至 5k 节点

**已知局限：**

1. **求解器兼容性受限**：L2Seg 目前仅与接受初始解输入的迭代求解器集成。对于 **HGS**（Vidal, 2022）这类不接受外部初始解的当前最优求解器，尚无法直接应用。这限制了 L2Seg 在顶级求解器上的直接加速能力。

2. **VRP 变体覆盖有限**：论文明确指出，扩展到其他 VRP 变体（如 VRPB、VRPPD）以及更广泛的组合优化问题仍有待探索。尽管 FSTA 框架在理论上具有通用性，但 L2Seg 的神经网络组件（编码器、解码器）是针对路径问题的图结构设计的，直接迁移需要架构调整。

3. **推理开销的性价比边界**：神经网络推理开销始终低于总迭代时间的 10%（Table 15），但在极短时间限制下（如秒级求解），这个固定开销可能稀释加速收益。搜索曲线（Figure 5）显示，加速效果在迭代早期尤为显著，但随求解趋近收敛，边际增益递减。

4. **训练数据的求解器特异性**：训练标签依赖于预定义的前向骨干求解器（通过模仿学习），理论上可能引入求解器特异性偏差。但标签相似度分析（Table 5）显示，HGS 和 LKH-3 的标签相似度为 78.3%，表明稳定性主要由问题实例的内在结构决定，偏差有限。

### 5. 开放问题

1. **FSTA 与精确方法的结合**：FSTA 分解能否与 Branch-and-Cut 等精确方法集成，在保持可证明最优性的同时加速求解？这需要处理超节点聚合后子问题的最优性条件传递问题。

2. **动态与在线场景的扩展**：L2Seg 目前针对静态 VRP 设计。在动态 VRP 或在线设置中，解的稳定性模式可能随时间演化，能否实时适应不断变化的路线需求是一个开放挑战。

3. **训练效率的优化**：当前训练需要为每个问题规模和分布生成大量模仿学习数据。能否通过迁移学习或预训练模型降低训练成本，使得 L2Seg 更容易扩展到万级节点实例？

4. **AR-NAR 协同的泛化**：L2Seg 中 AR 和 NAR 的协同思想（全局快速扫描 + 局部精确细化）能否推广到神经组合优化中的其他联合决策问题，如同时决策节点选择和路径构造？

5. **多模态特征融合**：当前 L2Seg 主要基于图结构特征和路径特征进行稳定性预测。能否将节点和边的多模态特征（如时间窗紧度、需求分布密度）纳入预测模型，进一步提高不稳定边缘的识别精度？

## 原文 PDF

![[paperPDFs/ICLR_2026/Learning_to_Segment_for_Vehicle_Routing_Problems.pdf]]
