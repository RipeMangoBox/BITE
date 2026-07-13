---
title: "ReHub: Linear Complexity Graph Transformers with Adaptive Hub-Spoke Reassignment"
type: paper
paper_level: A
venue: TMLR
year: 2025
pdf_ref: paperPDFs/TMLR_2025/ReHub_Linear_Complexity_Graph_Transformers_with_Adaptive_Hub_Spoke_Reassignment.pdf
project_link: https://tomerborreda.github.io/rehub/
code_link: null
aliases:
- ReHub
tags:
- TMLR_2025
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "spoke-to-hub连接矩阵E及其自适应重分配机制——通过将每个spoke连接的hub数量限制为小常数k，并在每层动态重分配hub连接，实现线性复杂度的同时保持高hub利用率。"
primary_logic: "图Transformer的计算复杂度主要由spoke-hub注意力驱动；因此无需减少总hub数量，只需限制每个spoke连接的小常数k个hub，并通过基于hub-hub相似度的自适应重分配来有效利用所有hub，从而在保持O(n)复杂度的前提下达到与全连接版本相当的性能。"
claims:
- "ReHub通过将每个spoke连接的hub数量限制为小常数k=3，并令总hub数N_h=O(√N_s)，实现了线性复杂度。"
- "稀疏版本的ReHub（每spoke仅连接k个hub）性能与全连接版本（ReHub-FC）相当，验证了重分配机制的有效性。"
- "自适应重分配基于hub-hub相似度分数，无需昂贵的node-hub计算，从而维持线性复杂度。"
- "Peptides-func 上 AP ↑ = 0.6685 ± 0.0074"
---

# ReHub: Linear Complexity Graph Transformers with Adaptive Hub-Spoke Reassignment

> [!tip] 核心洞察
> 图Transformer的计算复杂度主要由spoke-hub注意力驱动；因此无需减少总hub数量，只需限制每个spoke连接的小常数k个hub，并通过基于hub-hub相似度的自适应重分配来有效利用所有hub，从而在保持O(n)复杂度的前提下达到与全连接版本相当的性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ReHub：具有自适应枢纽-辐条重分配的线性复杂度图Transformer |
| 英文题名 | ReHub: Linear Complexity Graph Transformers with Adaptive Hub-Spoke Reassignment |
| 会议/期刊 | TMLR 2025 |
| Links | [paper](https://arxiv.org/abs/2412.01519) · [Project](https://tomerborreda.github.io/rehub/) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | ReHub |
| Dataset | Peptides-func, Peptides-struct, PCQM-Contact, PascalVOC-SP |

> [!tip] 效果简介
> - Peptides-func 上，AP ↑ 为 0.6685 ± 0.0074，对比 Neural Atoms 0.6591 ± 0.0050，变化 +0.0094。
> - Peptides-struct 上，MAE ↓ 为 0.2488 ± 0.0017，对比 Neural Atoms 0.2553 ± 0.0005，变化 −0.0065。
> - PCQM-Contact 上，MRR ↑ 为 0.3534 ± 0.0014，对比 Neural Atoms 0.3262 ± 0.0010，变化 +0.0272。

## 概要

图Transformer通过全局注意力机制有效捕获图中远距离节点间的依赖关系，但其密集注意力的二次复杂度 $O(N^2)$ 严重制约了在大规模图上的可扩展性。现有工作通过引入少量虚拟节点（hub）来聚合全局信息，但若为提升性能而增加hub数量，复杂度会迅速恶化——例如，Neural Atoms（Li et al., 2024）在hub数增至 $O(\sqrt{N})$ 时复杂度已达 $O(N^{3/2})$，形成了性能与效率之间的尖锐权衡。

ReHub 针对这一瓶颈提出了一种**自适应枢纽-辐条重分配**（adaptive hub-spoke reassignment）架构。其核心洞察在于：图Transformer的计算复杂度主要由辐条-枢纽（spoke-hub）注意力驱动，因此**无需减少总hub数量，只需将每个spoke连接的hub数量限制为一个小常数 $k$**（如 $k=3$），同时令总hub数 $N_h = O(\sqrt{N_s})$，即可将整体复杂度降至 $O(N)$。为弥补稀疏连接带来的信息损失，ReHub 在每一层基于hub-hub相似度分数动态重分配spoke所连接的hub，以极低的计算开销实现所有hub的高效利用。

实验表明，稀疏版 ReHub 在长程图基准（LRGB）的多个数据集上不仅显著优于 Neural Atoms——Peptides-func AP 提升 0.0094、PCQM-Contact MRR 提升 0.0272——而且性能与全连接版本（ReHub-FC）相当，验证了重分配机制的有效性。在大图内存测试中，ReHub 的内存消耗随节点数线性增长，并在 Coauthor Physics 与 OGBN-Arxiv 上以显著更低的内存开销取得了与 Exphormer（Shirzad et al., 2023）可比甚至更优的精度。

**方法定位**：ReHub 属于基于虚拟节点的线性图Transformer家族，其方法谱系与知识库定位将在下一节详述。

图Transformer通过在图上执行全局自注意力，能够有效捕获节点间的长程依赖关系，在分子性质预测、图像分割等任务中展现出超越传统消息传递神经网络（MPNN）的性能。然而，标准Transformer中的密集自注意力机制具有$O(N^2)$的时间与空间复杂度，其中$N$为图中节点数。这一二次复杂度瓶颈使得图Transformer难以扩展至大规模图——当图包含数万乃至数十万节点时，内存消耗与计算开销将变得不可承受。

为缓解上述问题，研究者提出了多种稀疏化注意力策略。其中一类重要方法是引入虚拟节点（virtual nodes）作为信息中转站：图中所有真实节点（spoke）与少量虚拟节点（hub）进行信息交互，再由hub之间进行全自注意力，从而间接实现全局信息融合。这一范式的代表工作包括**Neural Atoms**（Li et al., 2024），它将图节点通过聚类分配到固定数量的虚拟原子（atoms）上，在长程图基准（LRGB）上取得了领先性能。

然而，现有基于虚拟节点的方法面临一个根本性的**性能-效率权衡困境**：若将hub数量设为固定小常数，则模型表达能力受限；若增加hub数量以提升性能，则计算复杂度将急剧上升。以Neural Atoms为例，其计算复杂度为$O(N^{3/2})$——当图规模增大时，这一超线性增长依然会构成可扩展性障碍。具体而言，Neural Atoms的性能依赖于每个spoke连接所有hub（全连接模式），若将hub数量从常数提升至$O(\sqrt{N})$以增强表达能力，则spoke-hub交互的复杂度将变为$O(N \cdot \sqrt{N}) = O(N^{3/2})$，失去了线性复杂度的优势。

这一困境的核心在于：**图Transformer的计算复杂度主要由spoke-hub注意力驱动**。因此，根本的解决思路并非减少hub总数，而是限制每个spoke所连接的hub数量。ReHub正是在这一洞察下提出的——通过将每个spoke连接的hub数量限制为小常数$k$（如$k=3$），并令总hub数$N_h = O(\sqrt{N_s})$，即可将整体复杂度从$O(N^{3/2})$降至$O(N)$。但稀疏连接带来的新挑战是：如何保证所有hub被充分且均衡地利用，以避免信息瓶颈？

ReHub的回答是引入**自适应hub重分配机制**：在每一层根据hub之间的特征相似度与注意力分数，动态地为每个spoke重新分配其连接的$k$个hub。这一设计使得稀疏连接版本（ReHub）的性能能够与全连接版本（ReHub-FC）相媲美，从而在保持线性复杂度的同时，突破了此前方法中性能与效率的固有权衡。

## 核心方法与创新机理

ReHub 的核心创新在于**将图 Transformer 的复杂度控制从“减少 hub 总数”转向“限制每 spoke 的连接数 + 动态重分配”**，从而打破此前基于虚拟节点方法中性能与效率的权衡困境。

### 创新动机：打破性能-效率权衡

图 Transformer 中密集自注意力导致 $O(N_s^2)$ 的二次复杂度，使其难以扩展到大规模图。引入虚拟节点（hub）作为全局信息中转站是自然的降复杂度思路，但此前的方法面临一个根本性困境：若 hub 数量过少，全局信息瓶颈严重，性能受限；若增加 hub 数量以提升性能，复杂度又会迅速攀升。以 **Neural Atoms**（Li et al., 2024）为代表的方法，当将 hub 数量提升至 $O(\sqrt{N_s})$ 以获得更好性能时，其复杂度增至 $O(N_s^{3/2})$，未能真正实现线性扩展。

ReHub 的洞察在于：**复杂度瓶颈并非来自 hub 总数，而是来自 spoke-hub 间密集连接的注意力计算**。因此，无需减少 hub 总数——只需限制每个 spoke 在每层连接的 hub 数量为小常数 $k$，同时通过动态重分配机制确保所有 hub 被有效利用。

### 关键机制：自适应 Hub-Spoke 重分配

ReHub 的核心技术杠杆是**自适应 hub 重分配机制**（Hub (Re)Assignment），该机制在每一层为每个 spoke 重新选择其连接的 $k$ 个 hub。具体而言：

1. **稀疏连接约束**：定义二进制分配矩阵 $E \in \{0,1\}^{N_s \times N_h}$，约束每个 spoke 恰好连接 $k$ 个 hub（$E \mathbf{1}_{N_h} = k \cdot \mathbf{1}_{N_s}$），其中 $k$ 为小常数（默认 $k=3$）。这使得 spoke-hub 交叉注意力的复杂度从 $O(N_s N_h)$ 降至 $O(N_s k)$。

2. **基于 Hub-Hub 相似度的重分配**：每层重分配时，首先为每个 spoke 保留上一轮注意力分数最高的 1 个 hub，然后以该 hub 为中心，选择与其特征最相似的 $k-1$ 个 hub 作为该 spoke 的新连接。这一设计**避免了昂贵的 spoke-hub 全局相似度计算**，仅依赖 hub 间的距离度量，维持线性复杂度。

3. **Hub 全自注意力**：由于 hub 数量被设定为 $N_h = r\sqrt{N_s}$（$r=1$），hub 间的全自注意力复杂度为 $O(N_h^2) = O(N_s)$，同样保持在线性范围内。

### 与 Baseline 的核心差异（Changed Slots）

| 设计维度 | Neural Atoms 等 Baseline | ReHub |
|---------|------------------------|-------|
| **Spoke-Hub 连接方式** | 全连接（所有 spoke 连接所有 hub） | 稀疏连接，每 spoke 仅连 $k=3$ 个 hub |
| **Hub 重分配** | 各层间静态连接 | 每层基于 hub-hub 相似度与注意力分数动态重分配 |
| **Hub 数量规模** | 固定常数或与 $N_s$ 线性相关 | $N_h = r\sqrt{N_s}$，$r=1$，保证整体线性复杂度 |

### 创新有效性验证

消融实验直接验证了重分配机制的核心作用：关闭重分配（即静态连接）导致 PascalVOC-SP 上 F1 从 0.3860 降至 0.3775（Table 5）。更关键的是，**稀疏版本的 ReHub 性能与全连接版本（ReHub-FC）相当**，证明重分配机制使得仅连接 $k$ 个 hub 的稀疏配置能够达到与连接全部 hub 相当的信息聚合能力——这正是该方法突破性能-效率权衡的直接证据。

此外，hub 利用率分析（Figure 3）显示，在 $k=3$、$r=1$ 的默认配置下，各层 hub 利用率峰值集中在 90%-100%，表明重分配机制有效避免了 hub 闲置，确保了所有 hub 的充分参与。

ReHub 的整体架构遵循“局部消息传递—稀疏全局注意力—动态连接重分配”的交替范式，将图节点（spoke）与少量虚拟节点（hub）组织成二分交互结构，在保持线性复杂度的前提下实现长程信息传播。

### 架构总览

如图 Figure 1 所示，ReHub 的每一层由五个有序步骤构成：

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2412_01519/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of ReHub architecture. (1) Overview of the different steps in the architecture. A is the input (spoke) graph’s adjacency matrix; spoke features s ; hub features h ; hub assignment E ; and Γ contains attention scores from the Hubs-Spokes attention. (2) Hubs initialization. Spokes are first clustered, then each cluster is aggregated to compute hub features. Finally, each spoke is assigned more hubs. (3) Hub (Re)Assignment. Each spoke selects the k hubs closest to its most similar hub as its new assignment. (4) Illustration of connectivity between spokes and hubs. Information pass between spokes with an MPNN; while the interaction between hubs and spokes is performed via attention...*

1. **Spokes→Spokes 局部更新**：在原始图的 1‑环邻域内执行标准消息传递（MPNN），更新 spoke 表征。
2. **Spokes→Hubs 稀疏交叉注意力**：利用当前层的分配矩阵 $E_{sh}^{\ell}$，将 spoke 信息聚合至 hub。
3. **Hubs→Hubs 全自注意力**：在少量 hub（$N_h = O(\sqrt{N_s})$）之间执行全自注意力，捕获全局上下文。
4. **Hubs→Spokes 稀疏交叉注意力**：通过转置分配矩阵 $E_{hs}^{\ell}$ 将全局信息回传至 spoke。
5. **Hub (Re)Assignment**：基于 hub‑hub 相似度与注意力分数，为每个 spoke 重新分配下一层的 $k$ 个 hub 连接。

### 输入输出流

- **输入**：原始图邻接矩阵 $\mathbf{A}$、spoke 特征 $\mathbf{s}$。
- **初始化阶段**（Figure 1‑2）：使用 METIS 将图划分为 $N_h = r\sqrt{N_s}$ 个簇（$r=1$ 为默认设置），对每个簇内 spoke 特征进行聚合（如均值）得到 hub 初始特征 $\mathbf{h}_{i_h}^0$，并为每个 spoke 分配初始的 $k$ 个 hub 连接。
- **逐层传播**：spoke 特征 $\mathbf{s}^{\ell}$ 与 hub 特征 $\mathbf{h}^{\ell}$ 在五个步骤中交替更新，分配矩阵 $\mathbf{E}^{\ell}$ 控制 spoke‑hub 间的稀疏连接模式。
- **输出**：最终层的 spoke 表征 $\mathbf{s}^{L}$ 用于下游任务（节点分类、图分类或回归）。

### 模块关系与设计逻辑

五个步骤形成闭合的信息循环：MPNN 负责局部结构编码，spoke‑hub 交叉注意力实现从局部到全局的信息汇聚，hub 自注意力完成全局信息融合，hub‑spoke 交叉注意力将全局上下文广播回每个节点。这一循环的关键在于**分配矩阵 $\mathbf{E}$ 的稀疏性与动态性**——每层仅允许每个 spoke 连接 $k$ 个 hub（$k=3$ 为典型值），使得 spoke‑hub 交互复杂度降至 $O(N_s k)$；同时 hub 数量被约束在 $O(\sqrt{N_s})$，保证 hub 自注意力复杂度 $O(N_h^2) = O(N_s)$ 线性可控。

重分配模块（Algorithm 1）是连接各层的自适应开关：它基于 hub‑hub 相似度分数，为每个 spoke 保留最相似的 1 个 hub，并从该 hub 的最近邻中选取其余 $k-1$ 个 hub 作为新连接。这一设计避免了昂贵的 node‑hub 全局相似度计算，维持了整体线性复杂度，同时使所有 hub 在多层传播中获得高利用率（Figure 3 验证了 90%–100% 的 hub 被实际使用），从而使得稀疏版本 ReHub 的性能与全连接版本 ReHub‑FC 相当。

### 复杂度保证

ReHub 的线性复杂度依赖于两个关键约束的协同：
- **hub 数量**：$N_h = O(\sqrt{N_s})$，控制 hub 自注意力的二次项；
- **每 spoke 连接数**：$k$ 为小常数（如 $k=3$），控制交叉注意力的稀疏度。

在此约束下，单层总复杂度为 $O(N_s k + N_h^2 + N_s) = O(N_s)$，内存消耗随节点数线性增长，这在大规模随机正则图实验（Figure 2）中得到了实证验证——ReHub 的峰值内存显著低于 Exphormer 和 Neural Atoms 等基线方法。

### 枢纽-辐条二分图建模

ReHub将图Transformer重新建模为一个二分图架构：原始图节点称为**辐条（spokes）**，数量为 $N_s$；引入的虚拟节点称为**枢纽（hubs）**，数量为 $N_h$。二者之间的连接由二进制分配矩阵 $E \in \{0,1\}^{N_s \times N_h}$ 定义，满足约束：

$$E_{i_s, i_h} = \begin{cases} 1 & \text{if spoke } i_s \text{ is connected to hub } i_h \\ 0 & \text{otherwise} \end{cases} \quad \text{s.t.} \quad E \mathbf{1}_{N_h} = k \cdot \mathbf{1}_{N_s}$$

该约束保证**每个辐条恰好连接 $k$ 个枢纽**，其中 $k$ 为小常数（默认 $k=3$）。枢纽数量按 $N_h = r\sqrt{N_s}$ 设定，$r=1$ 在绝大多数基准上使用。这一设计是ReHub实现线性复杂度的核心：当 $N_h = O(\sqrt{N_s})$ 且 $k$ 为常数时，辐条-枢纽交叉注意力的复杂度为 $O(N_s k)$，枢纽间全自注意力的复杂度为 $O(N_h^2) = O(N_s)$，整体保持线性。

### 二分图稀疏注意力算子

ReHub定义了一个统一的稀疏注意力算子，在源图节点 $K$ 与目标图节点 $Q$ 之间执行注意力计算，仅通过连接矩阵 $E$ 指定的边进行：

$$O, \Gamma = \text{Attention}(K, Q, E)$$

其中 $O$ 为目标节点的更新特征，$\Gamma$ 为可选返回的稀疏注意力分数矩阵（用于后续重分配）。该算子内部仅对 $E$ 中非零位置计算注意力乘法，从而将计算量从全连接的 $O(N_s N_h)$ 压缩至 $O(N_s k)$。

### 长程辐条更新层的五步流水线

每层 $\ell$ 的长程信息传递由五个步骤组成（对应Figure 1），形成“局部→全局→局部”的信息流：

**步骤1：辐条-辐条局部消息传递。** 在原始图的1-环邻域内执行标准MPNN，捕获局部结构信息：

$$\pmb{s}^{\ell+\frac{1}{2}} = \mathtt{MPNN}(\pmb{s}^{\ell})$$

该步骤的计算复杂度为 $O(N_s)$，与图边数线性相关。

**步骤2：辐条→枢纽稀疏交叉注意力。** 利用当前层的分配矩阵 $E_{sh}^{\ell}$，将更新后的辐条特征聚合到枢纽：

$$\mathbf{h}^{\ell+\frac{1}{2}} = \text{Attention}(\mathbf{s}^{\ell+\frac{1}{2}}, \mathbf{h}^{\ell}, E_{sh}^{\ell})$$

此处注意力仅在每个辐条与其连接的 $k$ 个枢纽之间计算，复杂度为 $O(N_s k)$。

**步骤3：枢纽-枢纽全自注意力。** 在少量枢纽之间执行全自注意力，融合全局信息：

$$\mathbf{h}^{\ell+1} = \text{Attention}(\mathbf{h}^{\ell+\frac{1}{2}}, \mathbf{h}^{\ell+\frac{1}{2}}, \mathbf{E}_{full})$$

由于 $N_h = O(\sqrt{N_s})$，该步骤复杂度为 $O(N_h^2) = O(N_s)$，不破坏整体线性性。

**步骤4：枢纽→辐条稀疏交叉注意力。** 利用转置后的分配矩阵 $E_{hs}^{\ell} = (E_{sh}^{\ell})^T$，将全局信息回传至辐条：

$$\mathbf{s}^{\ell+1}, \Gamma^{\ell+1} = \text{Attention}(\mathbf{h}^{\ell+1}, \mathbf{s}^{\ell+\frac{1}{2}}, E_{hs}^{\ell})$$

同时返回注意力分数 $\Gamma^{\ell+1}$，供后续重分配使用。

**步骤5：枢纽（重）分配。** 基于枢纽-枢纽相似度与上一步的注意力分数，为每个辐条动态更新其连接的 $k$ 个枢纽（详见下文）。

### 枢纽初始化：聚类与特征聚合

初始枢纽特征的构建直接影响模型性能。ReHub采用基于图聚类的初始化策略（Equation 3）：首先使用METIS将图 $A$ 及其辐条特征 $\mathbf{s}$ 划分至 $N_h$ 个簇 $\{\mathcal{C}_{i_h}\}_{i_h=1}^{N_h}$，然后对每个簇内辐条特征进行聚合：

$$\mathbf{h}_{i_h}^0 = \text{Aggregate-Feat}(\{\mathbf{s}_{i_s}^0\}_{i_s \in \mathcal{C}_{i_h}})$$

聚合函数通常为均值池化（Cluster Mean），消融实验（Table 4/Table 14）表明该策略显著优于可学习参数初始化——后者甚至导致性能低于纯GNN基线。在聚合前可选择性加入辐条编码器（Spokes Encoder，一个前馈层），进一步提升初始化质量。

### 自适应枢纽重分配机制

重分配是ReHub区别于Neural Atoms等静态虚拟节点方法的关键模块。其核心思想是：**无需减少总枢纽数量，只需限制每辐条连接的小常数 $k$ 个枢纽，并通过每层动态重分配来高效利用所有枢纽**。

重分配过程（Algorithm 1）分为两步：
1. **保留最相关枢纽**：对每个辐条，根据上一步枢纽→辐条注意力分数 $\Gamma^{\ell+1}$ 保留与其最相似的1个枢纽。
2. **替换其余枢纽**：对剩余的 $k-1$ 个连接位置，基于枢纽-枢纽相似度分数，选择与保留枢纽最接近的 $k-1$ 个枢纽进行替换。

该设计的关键在于**基于枢纽-枢纽相似度而非辐条-枢纽相似度进行重分配**，从而避免了昂贵的辐条-枢纽全局计算，维持线性复杂度。消融实验（Table 5）证实：关闭重分配（静态连接）导致PascalVOC-SP上F1从0.3860降至0.3775；基于注意力分数的重分配优于无重分配和随机策略。

### 枢纽利用率与负载均衡

为量化重分配机制对枢纽利用的促进效果，论文引入Bhattacharyya系数衡量辐条-枢纽连接分布 $P$ 与均匀分布 $Q$ 的相似度：

$$\operatorname{BC}(P, Q) = \sum_{x \in \mathcal{X}} \sqrt{P(x) Q(x)}$$

Figure 3和Figure 5的直方图分析表明，在 $r=1, k=3$ 的默认配置下，各层枢纽利用率峰值集中在90%-100%，且Bhattacharyya分布接近均匀——验证了重分配机制有效避免了枢纽闲置，使得稀疏连接版本（ReHub）性能与全连接版本（ReHub-FC）相当。

## 实验与关键发现

### 核心实验设计逻辑

ReHub 的实验体系围绕三个递进目标构建：**长程建模能力验证**（LRGB 基准）、**线性复杂度实证**（大规模图内存/时间测量）和**组件贡献归因**（消融实验）。实验设计的关键决策是始终将稀疏版本 ReHub 与全连接版本 ReHub-FC 并排展示——这直接检验核心主张：自适应重分配能否使稀疏连接达到密集连接的同等性能。

实验公平性得到系统保障：所有结果基于 5 个随机种子报告均值±标准差；外部基线结果直接采用原论文汇报值，未重新训练；大图内存实验中所有模型采用相近的隐藏维度与层数，并额外纳入 $N_h = \sqrt{N_s}$ 的 Neural Atoms 变体以消除 hub 数量差异的干扰；所有实验在单块 NVIDIA L40 GPU（48GB）上运行，峰值内存通过 `torch.cuda.max_memory_allocated` 测量。

### 主结果：LRGB 基准性能

ReHub 在长程图基准（LRGB）上展现出系统性的性能优势，尤其是相对于其直接对标方法 Neural Atoms。核心结果如下：

**分子图任务上的优势**。在 Peptides-func（多标签分类）上，ReHub 以 GatedGCN 为 MPNN backbone 取得 AP $0.6685 \pm 0.0074$，较 Neural Atoms 的 $0.6591 \pm 0.0050$ 提升 $+0.0094$；在 Peptides-struct（回归）上取得 MAE $0.2488 \pm 0.0017$，较 Neural Atoms 的 $0.2553 \pm 0.0005$ 降低 $0.0065$；在 PCQM-Contact（接触预测）上取得 MRR $0.3534 \pm 0.0014$，较 Neural Atoms 的 $0.3262 \pm 0.0010$ 大幅提升 $+0.0272$（Table 2）。这三个数据集的共同趋势是 ReHub 在需要长程信息传递的任务上优势更明显，PCQM-Contact 的 8.3% 相对提升尤为突出。

**稀疏与密集版本的性能等价**。一个关键发现是稀疏 ReHub 与全连接 ReHub-FC 的性能差异极小：Peptides-func 上 AP 分别为 $0.6685$ 和 $0.6713$（差 $0.0028$），Peptides-struct 上 MAE 分别为 $0.2488$ 和 $0.2502$（差 $0.0014$）（Table 1）。这直接验证了重分配机制的有效性——将每 spoke 的 hub 连接数限制为 $k=3$ 并未造成信息瓶颈，因为动态重分配确保了所有 hub 的高效利用。

**非分子图任务上的表现**。在 PascalVOC-SP（超像素图节点分类）上，ReHub 取得 F1 $0.3860 \pm 0.0172$，略低于 Exphormer 的 $0.3975 \pm 0.0037$（差 $-0.0115$）。这一差距的可能原因需要进一步分析：Exphormer 使用 expander 图边提供额外的全局连接，而 ReHub 完全依赖 hub 中介，在图的异质性较高时可能存在信息路由效率的差异。但需注意 ReHub 在此任务上仍优于 GraphGPS 和 Transformer+LapPE 等基线。

### MPNN 模块化验证

Table 1 展示了 ReHub 的一个重要工程特性：**与底层 MPNN 的解耦性**。在 GINE、GatedGCN、GCN 三种 backbone 上，ReHub 均一致优于 Neural Atoms。以 Peptides-func 为例，ReHub 在 GINE 上取得 AP $0.6387$（Neural Atoms: $0.6351$），在 GCN 上取得 AP $0.6362$（Neural Atoms: $0.6267$）。这表明 ReHub 的长程信息传递机制独立于局部消息传递的具体实现，具有即插即用的模块化优势。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2412_01519/figures/002_Table_1.jpg]]
*Table 1: MPNN modularity. Test performance on datasets from the long-range graph benchmarks (LRGB) (Dwivedi et al., 2022) compared on various GNN types to Neural Atoms (Li et al., 2024). ReHub-FC has each spoke fully connected to all hubs. Best results are colored: first, second*

### 大规模图内存效率

Figure 2 的峰值内存-图规模曲线是验证线性复杂度的直接证据。在节点数从数千扩展至约 70 万的随机正则图上，ReHub 的内存消耗呈线性增长，且绝对值显著低于 Exphormer 和 Neural Atoms。Table 3 进一步在真实大规模图上验证：在 Coauthor Physics（约 34,493 节点）上，ReHub 以约 1.5 GB 峰值内存取得与 Exphormer 相当的准确率；在 OGBN-Arxiv（约 169,343 节点）上，ReHub 的内存消耗约为 Exphormer 的 1/3，同时保持可比的分类精度。这直接证明了“限制每 spoke 连接 $k$ 个 hub”策略在工程上的可扩展性优势。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2412_01519/figures/005_Table_3.jpg]]
*Table 3: Coauthor Physics (Shchur et al., 2018) and OGBN-Arxiv (Hu et al., 2020) test results show ReHub achieves comparable accuracy to Exphormer with significant reduction in memory consumption*

### 消融实验：组件贡献归因

消融实验在 PascalVOC-SP（Table 4, Table 5）和 Peptides-func（Table 14）上进行，系统分离了各设计要素的独立贡献。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2412_01519/figures/006_Table_4.jpg]]
*Table 4: Ablation study of long-range spoke update layer components. We measure the effect of various components of ReHub on top of a GatedGCN MPNN, using the PascalVOC-SP dataset. The number of hubs used per graph (#Hubs): for 22 it is a static amount and for $\sqrt { N _ { s } }$ it is dynamic per graph size. Initial hubs (Hubs Init) can be set as learned parameters or initialized from the assigned spokes as described in 3.3 where we can add a feedforward layer on the spokes (Spokes Enc) before aggregation. Reassignment is as described in 3.4. We use k = 3 for all runs*

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2412_01519/figures/007_Table_5.jpg]]
*Table 5: Ablation study of spoke-hub assignment strategies. We analyze the impact of various strategies for hub clustering, initial hub assignment, and hub reassignment on ReHub’s performance using the PascalVOC-SP dataset. Accordingly, the results are grouped into three categories, with ReHub’s performance reported at the bottom. The clustering methods include random, balanced random, and METIS. For hub assignment and reassignment, we evaluate random, balanced random, feature similarity-based assignment, and no reassignment. Reassignment based on Attention Scores is as described in Section 3.4. We use k = 3 for all runs. Our findings show that neither of the random strategies improve the results an...*

**Hub 初始化的关键作用**（Table 4）。使用可学习参数初始化 hub（Neural Atoms 方式）导致 F1 降至约 $0.372$，甚至低于纯 GatedGCN MPNN 基线；而基于 METIS 聚类与 spoke 特征聚合的初始化（Cluster Mean）将 F1 提升至约 $0.384$。这揭示了 hub 初始质量对模型收敛的强影响：随机初始化的 hub 无法提供有意义的全局信息聚合锚点，而聚类初始化使 hub 天然成为局部区域的语义代表。

**重分配机制的不可或缺性**（Table 5）。关闭重分配（静态连接）导致 F1 从 $0.3860$ 降至 $0.3775$，降幅约 $0.0085$。基于注意力分数的重分配优于无重分配，而基于特征相似度的初始分配又显著优于随机分配和均衡随机分配——后两种策略甚至损害性能。这一消融链条确立了因果方向：特征相似度提供有意义的初始连接 → 注意力分数驱动的重分配在每层优化连接 → 最终性能接近全连接版本。

**动态 Hub 数量的贡献**（Table 4, Table 14）。使用动态 hub 数量 $\sqrt{N_s}$（按图尺寸自适应）配合簇均值初始化、spoke 编码器及重分配，在 Peptides-func 上取得 AP $0.6683$，优于静态 22 个 hub 的配置。这表明图规模自适应是性能提升的独立贡献因子。

**Hub 利用率实证**（Figure 3）。在 PascalVOC-SP 验证集上，不同 hub 比率 $r$ 和连接数 $k$ 配置下，各层 hub 利用率直方图显示峰值集中在 90%-100% 区间，几乎所有 hub 在各层均被有效利用。这从机制层面解释了为何 $k=3$ 的稀疏连接不损失性能：重分配确保了 hub 负载均衡，避免了“死 hub”导致的信息容量浪费。

### 超参数敏感度分析

Figure 4 展示了 hub 比率 $r$ 和每 spoke 连接数 $k$ 对性能的影响。在 PascalVOC-SP 上，$r \in [0.5, 2]$ 范围内性能稳定，$r \ge 3$ 后略有下降；Peptides-func 上 $r=1$ 附近最优。$k=3$ 与 $k=5$ 的性能差异不显著，表明 $k=3$ 已提供足够的信息带宽。这一发现支持了 $k$ 作为小常数的设计选择具有实用鲁棒性。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2412_01519/figures/018_Figure_4.jpg]]
*Figure 4: Results for various hubs ratio and k, which is the number of hubs each spoke is connected to. We shown this on PascalVOC-SP (Left) and Peptides-func (Right) datasets with k = [ 3 , 5 ] and r = [0.5, 1, 2, 3, 4, 5]*

### 失败模式与局限性

尽管 ReHub 在多数任务上表现优异，实验中仍暴露出几个值得关注的局限：

1. **非分子图任务上的相对劣势**：在 PascalVOC-SP 上弱于 Exphormer（$-0.0115$ F1），可能与 ReHub 完全依赖 hub 中介而缺乏直接的长程边有关。Exphormer 的 expander 图边提供了额外的全局连接通路，这在异质性高的图上可能更具优势。

2. **重分配的启发式本质**：Table 5 显示基于特征相似度的分配优于随机，但仍低于全连接版本的性能上界（ReHub-FC），表明基于 hub-hub 相似度的间接重分配并非信息路由的最优解，存在进一步优化的空间。

3. **大图验证范围有限**：虽然随机正则图扩展至约 70 万节点，但真实图验证仅限于 OGBN-Arxiv（约 17 万节点）和 Coauthor Physics（约 3.5 万节点）等中等规模数据集，尚未在亿级节点图或极度稀疏/密集图上测试。

4. **Hub 数量的手动设定**：$r \approx 1$ 在多数数据集上表现良好，但在特定规模或结构图上可能需要调整 $r$ 和 $k$，缺乏自动自适应机制。Figure 4 显示 $r$ 的最优值在不同数据集间存在差异。

### 关键图表结论速览

- **Table 1**：ReHub 在三种 MPNN backbone 上一致优于 Neural Atoms，稀疏版本与全连接版本性能等价。
- **Table 2**：在 LRGB 五个数据集上，ReHub 在分子图任务上取得领先，非分子图任务上略低于 Exphormer 但优于多数基线。
- **Figure 2**：峰值内存随节点数线性增长，绝对值显著低于 Exphormer 和 Neural Atoms，实证线性复杂度。
- **Table 4**：Hub 聚类初始化是性能的关键前提，可学习参数初始化严重损害性能。
- **Table 5**：基于特征相似度的分配 + 注意力分数重分配是当前最优策略，随机策略损害性能。
- **Figure 3**：重分配机制确保各层 hub 利用率接近 90%-100%，解释了稀疏连接的效率。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2412_01519/figures/003_Table_2.jpg]]
*Table 2: Test performance on datasets from the long-range graph benchmarks (LRGB) (Dwivedi et al., 2022) compared to baselines. For Neural Atoms we show only available results. ReHub-FC has each spoke fully connected to all hubs. Best results are colored: first, second*

### 补充图表

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2412_01519/figures/019_Figure_5.jpg]]
*Figure 5: Percentage of graphs with a Bhattacharyya Percentage below a given threshold for the validation split of the PascalVOC-SP dataset. Results are shown for varying k and hubs ratio r. Left: k = 3 with r $\in \{$ 1 , 4 $\}$ . Right: k = 5 with r $\in \{$ 1 , 4 $\}$

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2412_01519/figures/009_Table_6.jpg]]
*Table 6: Statistics of the five dataset proposed in the long-range graph benchmark. Source: LRGB (Dwivedi et al., 2022)*

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2412_01519/figures/010_Table_7.jpg]]
*Table 7: Dataset statistics of LRGB, OGBN-Arxiv and Coauthor Physics. Source: Exphormer (Shirzad et al., 2023)*

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2412_01519/figures/012_Table_9.jpg]]
*Table 9: Model-specific hyperparameters for PCQM-Contact, and the number of model parameters*

## 定位与知识库关联

### 核心基线：Neural Atoms 及其性能-效率权衡

ReHub 最直接的方法前身是 **Neural Atoms**（Li et al., 2024）。两者共享“虚拟节点作为全局信息瓶颈”的架构范式：在原始图节点（spoke）之间引入一组可学习的虚拟节点（hub），通过 spoke-hub 交叉注意力实现长程信息传递。然而，Neural Atoms 面临一个根本性的性能-效率权衡困境：

- Neural Atoms 若将 hub 数量设为常数，虽能保持线性复杂度，但全局信息容量受限，性能不足；
- 若按 spoke 数量的比例增加 hub（如 $N_h \propto N_s$），则 spoke-hub 全连接注意力的复杂度攀升至 $O(N_s \cdot N_h) = O(N_s^{3/2})$，在大图上不可接受。

ReHub 的突破在于打破了这一权衡：**不减少 hub 总数，而是限制每个 spoke 连接的 hub 数量**。通过将 $N_h$ 设为 $O(\sqrt{N_s})$ 并将每 spoke 的连接数 $k$ 约束为小常数（如 $k=3$），ReHub 在理论上将整体复杂度压至 $O(N_s k + N_h^2) = O(N_s)$。这一设计使得 ReHub 能够在不牺牲 hub 容量的前提下实现线性复杂度，从而在长程图基准（LRGB）上以稀疏版本达到与全连接版本（ReHub-FC）相当的性能（Table 1, Table 2）。

### 与其他图 Transformer 的关系

ReHub 在方法谱系中定位于**稀疏注意力图 Transformer** 与**虚拟节点架构**的交汇处：

- **Exphormer**（Shirzad et al., 2023）通过 expander 图边和虚拟节点实现稀疏全局注意力，其虚拟节点与所有图节点全连接。ReHub 与其区别在于：Exphormer 的虚拟节点连接是静态的，而 ReHub 的核心创新在于**层间自适应的 hub 重分配机制**。在 Coauthor Physics 和 OGBN-Arxiv 大图实验中（Table 3），ReHub 以显著更低的内存消耗取得了与 Exphormer 相当的准确率，验证了动态重分配在效率上的优势。

- **GraphGPS**（Rampášek et al., 2022）和 **SAN+LapPE**（Kreuzer et al., 2021）等经典图 Transformer 依赖全对全注意力或基于位置编码的稀疏注意力，其复杂度仍为超线性。ReHub 与它们的本质区别在于将全局信息聚合委托给远少于节点数的 hub 集合，而非直接在所有节点对之间建模。

- 在模块化设计上，ReHub 继承了 Neural Atoms 的“MPNN backbone + 长程更新层”框架，可灵活替换 MPNN 类型（GatedGCN、GCN、GINE 等），使其成为**即插即用的长程增强模块**，而非独立的端到端架构。

### 适用边界

ReHub 的设计假设决定了其适用范围：

1. **图规模**：当前验证覆盖节点数从 LRGB 的小分子图（数十节点）到 Coauthor Physics 的中等规模图（约 3 万节点）及随机正则图（约 70 万节点）。在极大稀疏图或极度稠密图上，METIS 聚类的质量以及 $N_h = \sqrt{N_s}$ 的设定是否仍然合理，尚待验证。

2. **图结构类型**：hub 初始化依赖 METIS 图划分和簇内特征聚合，这对具有清晰社区结构的图效果良好；在缺乏局部聚簇结构的随机图或高度同质图上，聚类可能退化为任意划分，削弱 hub 初始表征的语义质量。

3. **特征模态**：当前实现仅利用图拓扑和节点特征进行聚类与重分配，未显式利用边特征或几何位置信息（如 3D 坐标、拉普拉斯位置编码）。这限制了其在分子构象预测等需要精确几何建模的任务上的直接适用性。

### 关键局限

1. **重分配策略的次优性**：hub 重分配基于 hub-hub 相似度启发式，未直接建模 spoke-hub 细粒度交互。这意味着重分配可能不是信息路由的最优解——spoke 可能被分配至与其信息需求不完全匹配的 hub。消融实验（Table 5）表明，基于注意力分数的重分配优于特征相似度重分配，但两者均为固定准则，缺乏端到端可学习性。

2. **hub 数量的手动设定**：$r=1$（即 $N_h = \sqrt{N_s}$）在多数基准上表现良好，但超参数敏感度分析（Figure 4）显示，不同数据集对 $r$ 和 $k$ 的最优组合存在差异。当前缺乏根据图全局属性（如直径、聚类系数）自动确定 $r$ 的自适应机制。

3. **大规模验证不足**：大图实验仅覆盖至约 70 万节点，尚未在亿级节点图或流式图场景下测试。在极高动态性场景中，每层的 METIS 重聚类和 hub 重分配的计算开销可能成为新瓶颈。

### 开放问题

1. **可学习重分配**：能否将 hub 重分配改造为可微组件，端到端地根据下游任务优化分配策略？例如，通过 Gumbel-Softmax 松弛 $E$ 矩阵的离散约束，使重分配参与梯度反传。

2. **位置编码融合**：如何将拉普拉斯位置编码或随机游走结构编码有机融入 spoke-hub 注意力与重分配过程，以提升在几何图或异质图上的性能？

3. **与 expander 图的结合**：ReHub 的 hub 重分配思想是否可以与 Exphormer 的 expander 图边结合，实现层间动态重连 expander 邻居，从而在保持线性复杂度的同时增强全局连通性？

4. **动态图扩展**：在高动态图或流式图设置中，如何高效地在线更新 hub 特征与连接分配，避免每步重新聚类？

5. **自适应 hub 比率**：是否能基于图的全局结构属性（如谱半径、社区模块度）学习一个轻量预测器，为每张图自动确定最优的 $r$ 和 $k$？

## 原文 PDF

![[paperPDFs/TMLR_2025/ReHub_Linear_Complexity_Graph_Transformers_with_Adaptive_Hub_Spoke_Reassignment.pdf]]
