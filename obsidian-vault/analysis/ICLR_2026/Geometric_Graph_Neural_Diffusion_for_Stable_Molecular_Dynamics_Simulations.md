---
title: "Geometric Graph Neural Diffusion for Stable Molecular Dynamics Simulations"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Geometric_Graph_Neural_Diffusion_for_Stable_Molecular_Dynamics_Simulations.pdf
openreview_forum_id: T8VcTykTf1
aliases:
- GGNDG
- GGNDSMDS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/chemistry_and_drug_discovery
core_operator: "引入几何图上的扩散过程，通过等变梯度算子和张量值注意力扩散度算子进行全连通图的信息传播。这一机制能够在分子构象变化时保持不变性，从而缓解误差积累并确保模拟稳定性。"
primary_logic: "将扩散偏微分方程推广到几何图中，利用等变梯度算子将节点特征差映射为边特征，再用基于Clebsch‑Gordan系数、球谐函数和径向函数的张量值注意力矩阵调控信息传播速率。连续时间演化使节点表示能够捕获任意原子对之间的全对信息流，对局部截止半径等几何拓扑变化不敏感，同时保持SE(3)‑等变性，从而大幅减小分布外误差。"
claims:
- "VisNet在300 K训练，在600 K和1200 K的稳定性从100 ps骤降至25.358和0.004 ps；而+GGND将600 K和1200 K的稳定性提升至100 ps。"
- "GGND将MACE在1200 K的稳定性从1.965 ps提升至29.218 ps，能量MAE从0.507 eV降低至0.137 eV。"
- "在SAMD23半导体系统的OOD测试中，GGND在SiN和HfO上均达到接近100 ps的稳定性（99.892和97.928），而大多数对比模型稳定性显著下降。"
- "3BPA 上 Energy MAE (eV) = 0.022"
---

# Geometric Graph Neural Diffusion for Stable Molecular Dynamics Simulations

> [!tip] 核心洞察
> 将扩散偏微分方程推广到几何图中，利用等变梯度算子将节点特征差映射为边特征，再用基于Clebsch‑Gordan系数、球谐函数和径向函数的张量值注意力矩阵调控信息传播速率。连续时间演化使节点表示能够捕获任意原子对之间的全对信息流，对局部截止半径等几何拓扑变化不敏感，同时保持SE(3)‑等变性，从而大幅减小分布外误差。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 几何图神经网络扩散用于稳定分子动力学模拟 |
| 英文题名 | Geometric Graph Neural Diffusion for Stable Molecular Dynamics Simulations |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=T8VcTykTf1) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/chemistry_and_drug_discovery |
| Method | Geometric Graph Neural Diffusion (GGND) |
| Dataset | 3BPA, SiN (Test, SAMD23), HfO (Test |

> [!tip] 效果简介
> - 3BPA 上，Energy MAE (eV) 为 0.022，对比 1.405，变化 1.405 → 0.022。
> - 3BPA 上，Stability (ps) 为 29.218，对比 1.965，变化 1.965 → 29.218。
> - SiN (Test, SAMD23) 上，Stability (ps) 为 100，对比 100 (Equiformer V2) / 较低 ，变化 多数对比模型远低于100；GGND与Equiformer V2并列满分。

## 概述

现有几何图神经网络（Geo‑GNN）在分子动力学（MD）模拟中面临一个根本瓶颈：训练数据仅覆盖有限温度下的分子构象，当模拟遇到高温等分布外构象时，即使微小的力预测误差也会累积导致非物理的化学键形成，使长期模拟迅速崩溃。图 1 的初步分析揭示了这一问题的根源——几何拓扑偏移：3BPA 分子在 600 K 和 1200 K 下的邻接矩阵分布与训练集（300 K）存在显著差异，而 VisNet 和 SEGNO 等主流等变模型在此偏移下的稳定性从 100 ps 骤降至数十甚至近乎零 ps。

针对这一瓶颈，本文提出**几何图神经网络扩散（Geometric Graph Neural Diffusion, GGND）**，其核心思路是将扩散偏微分方程推广到几何图上，通过等变梯度算子和张量值注意力扩散度算子在全连通图上进行信息传播。这一机制使模型能够捕获任意原子对之间的全局依赖关系，对截止半径等局部几何拓扑变化不敏感，同时保持 SE(3)‑等变性，从而大幅缓解分布外误差。

GGND 定位为**即插即用模块**，可无缝集成到现有局部等变消息传递框架（如 NequIP、MACE、VisNet）中。实验结果表明：

- 在 3BPA 数据集上，GGND 将 VisNet 在 600 K 和 1200 K 的稳定性从 25.358 ps 和 0.004 ps 均提升至 100 ps，能量 MAE 从 1.405 eV 降至 0.022 eV；将 MACE 在 1200 K 的稳定性从 1.965 ps 提升至 29.218 ps。
- 在 SAMD23 半导体系统的分布外测试中，GGND 在 SiN 和 HfO 上均达到接近 100 ps 的稳定性，力 MAE 相比 Neural P3M 等 SOTA 模型降低约 40%。
- 消融实验证实，完整的全连通扩散与等变扩散度算子是性能提升的关键，去掉任一组件的变体在高温外推任务上均明显退化。

GGND 引入约 26.5% 的训练时间增加和 15.6% 的 MD 模拟时间增加，但鉴于其在稳定性和精度上的巨大提升，这一开销在实践中是可接受的。当前方法的主要局限在于全连通图扩散的平方级复杂度，使其难以直接扩展至包含数百万原子的蛋白质等大生物分子系统。

## 背景与动机

分子动力学（MD）模拟是理解分子系统物理化学性质的核心工具，其精度高度依赖于势能面描述的准确性。近年来，几何图神经网络（Geo‑GNN）在拟合高精度量子力学数据方面取得了显著进展，使得机器学习力场（MLFF）能够以较低的计算成本逼近第一性原理精度。然而，现有 Geo‑GNN 模型的训练数据通常仅覆盖有限温度下的分子构象，当模拟遇到分布外（OOD）构象时，即使微小的力预测误差也会在长期 MD 轨迹中逐步累积，最终导致非物理的化学键形成，破坏模拟的稳定性。

### 几何拓扑偏移：外推失败的根本瓶颈

问题的核心在于**几何拓扑偏移**（Geometric Topological Shift）。现有 Geo‑GNN 通常依赖预定义的截止半径构建局部几何图，通过邻域内的等变消息传递提取原子环境特征。这种局部建模策略在训练数据覆盖的构象空间内表现良好，但缺乏对几何拓扑变化的外推能力。

Figure 1 以柔性药物分子 3BPA 为例揭示了这一问题的严重性。在 300 K 下训练的 VisNet 和 SEGNO 模型，当测试温度升至 600 K 和 1200 K 时，性能急剧退化：

- **VisNet**：稳定性从 300 K 的 100 ps 骤降至 600 K 的 25.358 ps 和 1200 K 的 0.004 ps；力预测 MAE 从 0.0065 eV/Å 飙升至 0.9971 eV/Å（600 K）和 1.4043 eV/Å（1200 K）。
- **SEGNO**：稳定性从 300 K 的 99.812 ps 降至 600 K 的 59.892 ps 和 1200 K 的 0.009 ps；力预测 MAE 从 0.3592 eV/Å 升至 0.8925 eV/Å（600 K）和 1.2375 eV/Å（1200 K）。

Figure 1(a)-(b) 的邻接矩阵分布差异进一步表明，高温构象与训练构象之间的几何拓扑偏移是系统性的——原子间距离分布发生显著变化，导致基于固定截止半径的局部图结构不再可靠。Figure 2 的因果图形式化地刻画了这一偏移机制：环境变量 $E$（温度、压力等）和建模方法 $M$（预定义截止半径 $C$）共同作为图拓扑结构的隐式原因，当测试环境 $E_{\text{te}} \neq E_{\text{tr}}$ 时，模型面临不可观测的图结构变化，局部消息传递无法适应这种分布外偏移。

### 现有方法的局限与本文动机

现有 Geo‑GNN 的改进方向主要集中在更丰富的等变表示（如 MACE、Equiformer V2）或更高阶的局部交互（如 Allegro、QuinNet），但这些方法本质上仍受限于局部邻域的信息传播范式。当构象变化导致原子对跨越截止半径边界时，局部图拓扑发生突变，模型缺乏机制来捕获这种全局性的结构重排。

本文的核心动机在于：**能否设计一种保持 SE(3)-等变性的全局信息传播机制，使模型对几何拓扑偏移不敏感，从而在分布外构象上维持稳定的力预测？** 为此，GGND 将扩散偏微分方程推广到几何图上，通过全连通图上的等变梯度算子和张量值注意力扩散度算子，实现任意原子对之间的连续时间信息流。这一设计使节点表示不再依赖预定义的邻接结构，从根本上缓解了几何拓扑偏移带来的误差累积问题。

## 核心创新

GGND 的核心创新在于将**几何图上的连续时间扩散过程**引入等变图神经网络，从根本上改变了消息传递的拓扑范围和机制，从而缓解了现有 Geo‑GNN 在分子动力学模拟中因**几何拓扑偏移**导致的稳定性崩溃问题。

### 从局部消息传递到全连通图扩散

现有等变消息传递模型（如 NequIP、MACE、VisNet）均依赖预定义截止半径构建局部几何图，消息仅在邻域内传播。当模拟温度升高或化学环境变化时，分子构象进入训练分布之外，局部邻域结构发生显著偏移，导致力预测误差迅速积累并引发非物理的化学键断裂或形成。

GGND 做出了三个关键的 **changed slots**：

| 设计维度 | 基线方法 | GGND |
|---------|---------|------|
| 图拓扑 | 预定义截止半径下的局部几何图 | 全连通图（所有原子对参与信息传播） |
| 消息传递范式 | 局部邻域内的等变消息传递 | 基于连续时间扩散 PDE 的全局信息传播 |
| 注意力机制 | 无全局注意力或仅局部注意力 | 张量值等变注意力矩阵 $\mathbf{S}(t)$，包含 Clebsch‑Gordan 系数、球谐函数和径向基函数 |

### 等变扩散算子的因果机制

GGND 的扩散过程由两个核心算子驱动，共同构成对几何拓扑偏移不敏感的全局特征提取机制：

1. **等变梯度算子**（Equation 2）：将节点特征差映射为高阶张量边特征，保持 SE(3)‑等变性：
   $$(\nabla \mathbf{z})_{ij, k l_3 m_3} = \sum_{\tilde{k}} W_{k\tilde{k} l_2} ( \mathbf{z}_{j, \tilde{k} l_2 m_2} - \mathbf{z}_{i, \tilde{k} l_2 m_2} )$$

2. **张量值等变扩散度算子**（Equation 3）：基于球谐函数、径向基函数和 Clebsch‑Gordan 系数的注意力矩阵，调控全局信息流动的速率：
   $$\mathbf{S}(t)[i,j]_{k l_3 m_3} = \sum_{l_1, l_2, m_1, m_2} C_{l_1 m_1, l_2 m_2}^{l_3 m_3} R_{k l_1 l_2 l_3}(\|\mathbf{x}_{ji}\|) Y_{m_1}^{l_1}(\hat{\mathbf{x}}_{ji}) \phi(\mathbf{z}_i(t), \mathbf{z}_j(t))_{l_2 m_2}$$

这两个算子结合在全连通图上，使得节点特征的连续时间演化能够捕获**任意原子对之间的全对信息流**。其核心因果机制在于：当分子构象变化导致局部截止半径内的邻域结构剧烈改变时，全连通扩散路径不受影响，模型表示对邻接矩阵的变化保持低敏感性（Theorem 3.1 给出了表示变化对 $\|\Delta\tilde{\mathbf{A}}\|_2$ 的多项式阶上界保证）。

### 扩散 PDE 的连续时间演化

GGND 将扩散过程建模为几何图上的偏微分方程（Equation 1）：
$$\frac{\partial \mathbf{Z}(t)}{\partial t} = \mathrm{div}\left[ \mathbf{S}(\mathbf{Z}(t), \mathbf{X}, t) \odot \nabla \mathbf{Z}(t) \right]$$

当扩散度矩阵 $\mathbf{S}(t)$ 满足右随机性时，该方程可等价写为连续时间随机游走形式（Equation 4）：
$$\frac{\partial \mathbf{Z}(t)}{\partial t} = (\mathbf{S}(\mathbf{Z}(t), \mathbf{X}, t) - \mathbf{I})\mathbf{Z}(t)$$

这种连续时间演化使得信息传播不再受离散消息传递层数的限制，能够在任意深度上自适应地融合全局结构信息。更重要的是，扩散过程对几何拓扑变化具有天然的不变性——这正是 GGND 能够大幅减小分布外误差的根本原因。

### 插件式架构设计

GGND 并非重新设计整个模型，而是作为**插件模块**与现有局部等变消息传递网络无缝集成。整体架构（Figure 3）包含两个互补组件：(i) 局部等变消息传递网络提取局部原子环境特征；(ii) GGND 模块在全连通图上进行等变扩散，生成对几何拓扑偏移不敏感的全局特征。两者特征融合后输入输出头进行能量和力的预测。这种设计使得 GGND 可以即插即用地增强 MACE、NequIP、SEGNO、VisNet 等主流 backbone 的外推能力，同时保持域内精度不退化。

### 关键证据

消融实验（Table 3）直接验证了上述创新机制的必要性：去掉全连通扩散或等变扩散度算子的变体（GGND† 和 GGND‡）在高温外推任务上的稳定性和准确性均明显下降，而完整 GGND 在 600 K 达到 100 ps 的满分稳定性，在 1200 K 仍保持 29.218 ps。这证实了**完整的等变扩散过程**——而非单纯的全连通图或注意力机制——是缓解几何拓扑偏移的核心因果开关。

## 整体框架

![[assets/figures/papers/iclr26_0012_T8VcTykTf1_Geometric_Graph_Neural_Diffusion_for_Stable_Mole/figures/007_Figure_3.jpg]]
*Figure 3: The Illustration of Geometric Graph Neural Diffusion: (a) Our method serves as a plug-in module that integrates with local equivariant message passing. (b) The GGND uses equivariant diffusion operators (gradient and diffusivity) on a fully connected graph to capture domaininvariant geometric topological features. (c) The local message passing and the equivariant diffusion operators are combined to address geometric topological shifts, enabling generalizable energy and force predictions for stable molecular dynamics simulations*

GGND 采用**双通道并行**的架构设计，将局部等变消息传递网络与几何图神经扩散模块结合为一个即插即用的整体框架（Figure 3）。其核心思路是：局部通道负责提取原子邻域内的精细几何特征，而全局扩散通道则在全连通图上传播信息，捕获对几何拓扑偏移不敏感的全局表示。

### 输入与预处理

给定一个分子构象，输入包括原子坐标 $\mathbf{X} \in \mathbb{R}^{N \times 3}$ 和初始节点特征 $\mathbf{H}$（如原子类型嵌入）。传统 Geo‑GNN 在此处根据预设截止半径 $r_c$ 构建局部几何图 $\mathcal{G}_{\text{local}}$，仅保留距离小于 $r_c$ 的原子对之间的边。**GGND 的关键不同在于**：在扩散通道中，图拓扑被扩展为**全连通图**，所有 $N(N-1)/2$ 个原子对均参与信息传播（Section 3.1 明确假设 "full connectivity in the graph"）。这一设计直接绕过了截止半径带来的几何拓扑偏移问题——当分子构象随温度变化导致原子间距跨越 $r_c$ 阈值时，局部图的边集发生突变，而全连通图始终保持不变。

### 双通道模块

框架包含两个并行模块，其输出在末端融合（Figure 3(a)）：

1.  **局部等变消息传递网络（Local EGNN Backbone）**  
    该模块可以是任意现有的等变消息传递模型（如 NequIP、MACE、VisNet 等），在局部几何图上通过球谐函数和等变卷积提取原子邻域的几何特征。其输出为局部节点表示 $\mathbf{Z}_{\text{local}}$。

2.  **几何图神经扩散模块（GGND Module）**  
    这是本文的核心创新。GGND 在全连通图上运行一个**连续时间扩散偏微分方程**：
    $$\frac{\partial \mathbf{Z}(t)}{\partial t} = \mathrm{div}\left[ \mathbf{S}(\mathbf{Z}(t), \mathbf{X}, t) \odot \nabla \mathbf{Z}(t) \right]$$
    其中 $\nabla$ 是**等变梯度算子**，将节点特征差映射为高阶张量边特征；$\mathbf{S}(t)$ 是**张量值等变扩散度矩阵**，由 Clebsch‑Gordan 系数、球谐函数 $Y_{m_1}^{l_1}(\hat{\mathbf{x}}_{ji})$ 和径向基函数 $R_{k l_1 l_2 l_3}(\|\mathbf{x}_{ji}\|)$ 共同构成，本质上是一个全局等变注意力机制，调控每对原子之间的信息传播速率。该扩散过程从初始嵌入 $\mathbf{Z}(0)$ 开始演化至终端时间 $T$，产出全局扩散特征 $\mathbf{Z}_{\text{diff}}$。

### 输出融合与预测

局部特征 $\mathbf{Z}_{\text{local}}$ 与全局扩散特征 $\mathbf{Z}_{\text{diff}}$ 通过组合操作（Figure 3(c) 所示）融合为最终节点表示，随后输入预测头输出能量和原子力。由于扩散通道已在全连通图上捕获了任意原子对之间的全对信息流，融合后的表示对局部截止半径的变化不敏感，同时保持了 SE(3)‑等变性。

### 关键设计决策与因果机制

从因果角度看（Figure 2），传统方法中环境 $E$（温度、压力）和建模方法 $M$（预设截止半径 $C$）共同导致几何拓扑偏移，进而破坏外推稳定性。GGND 通过以下设计打破这一因果链：

-   **全连通图**消除了 $C$ 作为拓扑变化的源头；
-   **等变扩散度算子 $\mathbf{S}(t)$** 利用张量值注意力在所有原子对之间自适应地分配信息流权重，使得模型能够平滑地适应构象变化，而非在截止边界处发生突变；
-   **连续时间演化**使得节点表示能够整合全局上下文，理论分析（Theorem 3.1）表明，该扩散过程可将表示变化 $\|\mathbf{Z}(T;\mathbf{A}')-\mathbf{Z}(T;\mathbf{A})\|_2$ 控制在对邻接矩阵变化 $\|\Delta\tilde{\mathbf{A}}\|_2$ 的任意多项式阶范围内，从而将外推误差中的表示变化项压缩至极低水平。

### 即插即用特性

GGND 作为一个独立模块，可以与 NequIP、MACE、SEGNO、VisNet 等多种局部等变消息传递框架无缝集成。实验表明（Table 1），在 3BPA 数据集上，将 GGND 附加到 VisNet 后，600 K 下的能量 MAE 从 1.405 eV 降至 0.022 eV；附加到 MACE 后，1200 K 下的稳定性从 1.965 ps 提升至 29.218 ps。在 SAMD23 半导体系统的 OOD 测试中（Table 2），GGND 在 SiN 和 HfO 上分别达到 99.892 ps 和 97.928 ps 的稳定性，显著优于多数对比模型。

> **注意**：GGND 的全连通扩散带来了约 26.5% 的训练时间增加和约 15% 的 GPU 内存增长（Table 5），复杂度为 $O(N^2)$，目前主要适用于中小规模系统（如 3BPA 和 SAMD23 中最多 510 个原子）。向百万原子级蛋白质系统的扩展需要稀疏近似或分层扩散机制，这一点原文将其列为未来工作方向。

## 核心模块与公式推导

GGND 的核心由两个互补组件构成：**局部等变消息传递网络（EGNN backbone）** 和 **几何图神经扩散模块（GGND module）**。前者负责提取局部原子环境特征，后者在全连通图上进行等变扩散，生成对几何拓扑偏移不敏感的全局特征。两者通过特征融合机制结合，使 GGND 能够作为即插即用模块集成到现有局部等变消息传递框架中（Figure 3）。

### 几何图扩散偏微分方程

GGND 的扩散过程由连续时间偏微分方程（PDE）描述：

$$\frac{\partial \mathbf{Z}(t)}{\partial t} = \mathrm{div}\left[ \mathbf{S}(\mathbf{Z}(t), \mathbf{X}, t) \odot \nabla \mathbf{Z}(t) \right] \tag{1}$$

其中 $\mathbf{Z}(t) \in \mathbb{R}^{N \times d}$ 为 $N$ 个节点的等变特征在时间 $t$ 的状态，$\nabla$ 为等变梯度算子，$\mathbf{S}(t)$ 为张量值扩散度矩阵，$\odot$ 表示张量缩并运算。该方程在全连通图上演化节点特征，使任意原子对之间的信息得以传播，从而对局部截止半径等几何拓扑变化不敏感。

### 等变梯度算子

等变梯度算子将节点特征差映射为高阶张量边特征，保持 SE(3)-等变性：

$$(\nabla \mathbf{z})_{ij, k l_3 m_3} = \sum_{\tilde{k}} W_{k\tilde{k} l_2} ( \mathbf{z}_{j, \tilde{k} l_2 m_2} - \mathbf{z}_{i, \tilde{k} l_2 m_2} ) \tag{2}$$

其中 $W_{k\tilde{k} l_2}$ 为可学习的线性变换权重，$l_2, m_2$ 为球谐函数的阶数和度数指标，$k, \tilde{k}$ 为通道索引。该算子将标量节点特征差推广到任意阶张量空间，为后续扩散提供等变边特征。

### 等变扩散度算子（张量值注意力）

扩散度矩阵 $\mathbf{S}(t)$ 通过基于 Clebsch–Gordan 系数、球谐函数和径向基函数的张量值注意力机制构建：

$$\mathbf{S}(t)[i,j]_{k l_3 m_3} = \sum_{l_1, l_2, m_1, m_2} C_{l_1 m_1, l_2 m_2}^{l_3 m_3} R_{k l_1 l_2 l_3}(\|\mathbf{x}_{ji}\|) Y_{m_1}^{l_1}(\hat{\mathbf{x}}_{ji}) \phi(\mathbf{z}_i(t), \mathbf{z}_j(t))_{l_2 m_2} \tag{3}$$

其中 $C_{l_1 m_1, l_2 m_2}^{l_3 m_3}$ 为 Clebsch–Gordan 系数，负责张量积的角动量耦合；$R_{k l_1 l_2 l_3}(\|\mathbf{x}_{ji}\|)$ 为可学习的径向基函数，编码原子间距离信息；$Y_{m_1}^{l_1}(\hat{\mathbf{x}}_{ji})$ 为球谐函数，编码方向信息；$\phi(\mathbf{z}_i(t), \mathbf{z}_j(t))_{l_2 m_2}$ 为节点特征交互函数。该注意力矩阵确保全局信息流动的等变性，同时调控不同原子对之间的信息传播速率。

### 线性化扩散动力学

当扩散度矩阵 $\mathbf{S}(t)$ 满足行随机性（row-stochastic）时，扩散方程可重写为连续时间随机游走形式：

$$\frac{\partial \mathbf{Z}(t)}{\partial t} = (\mathbf{S}(\mathbf{Z}(t), \mathbf{X}, t) - \mathbf{I})\mathbf{Z}(t) \tag{4}$$

该形式显式表明节点特征通过全对注意力权重进行全局混合，使模型能够学习域不变特征，同时保持 SE(3)-等变性。这一性质是 GGND 缓解几何拓扑偏移、提升外推稳定性的理论根基。

### 外推间隙分解

为从理论上理解 GGND 的外推能力，分布外误差可分解为三项：

$$| \mathcal{L}(\Gamma_{\theta}; E_{\mathrm{te}}, M_{\mathrm{tr}}) - \mathcal{L}_{\mathrm{tr}}(\Gamma_{\theta}; E_{\mathrm{tr}}, M_{\mathrm{tr}}) | \le \mathcal{D}_{\mathrm{in}} + O(\mathbb{E}\|\mathbf{Z}(T;\mathbf{A}')-\mathbf{Z}(T;\mathbf{A})\|_2) + O(\mathbb{E}\|\mathbf{Y}'-\mathbf{Y}\|_2) \tag{8}$$

其中 $\mathcal{D}_{\mathrm{in}}$ 为域内泛化误差（由 Rademacher 复杂度和训练集规模控制），第二项为模型表示对邻接矩阵变化 $\Delta\mathbf{A}$ 的敏感性，第三项为标签随环境变化产生的偏移。GGND 的核心优势在于：通过全连通图扩散，使表示变化项 $\mathbb{E}\|\mathbf{Z}(T;\mathbf{A}')-\mathbf{Z}(T;\mathbf{A})\|_2$ 对 $\|\Delta\mathbf{A}\|_2$ 的依赖降至任意多项式阶，从而大幅压缩外推间隙。此结论由 Theorem 3.1 形式化保证（若 $f$ 和 $h$ 为单射，则扩散模型将表示变化降至 $O(\psi(\|\Delta\mathbf{A}\|_2))$，其中 $\psi$ 为任意多项式函数）。

> **注意**：Theorem 3.1 的完整表述和证明细节需查阅原文 Section 3.2，此处仅给出其结论性描述以支撑外推间隙分解的逻辑链条。

## 实验与分析

### 核心瓶颈与评估框架

现有几何图神经网络（Geo‑GNN）的根本瓶颈在于训练数据只能覆盖有限分子构象。当模拟遇到分布外（OOD）构象时，即使微小的力预测误差也会通过动力学积分逐步累积，最终导致非物理的化学键形成，破坏长期 MD 模拟的稳定性。Figure 1 通过 3BPA 数据集直观展示了这一现象：Figure 1(a)–(b) 表明，600 K 和 1200 K 测试构象的邻接矩阵分布与 300 K 训练集存在显著偏移；Figure 1(c) 的定量结果显示，VisNet 在 300 K 训练后，稳定性从 100 ps 骤降至 600 K 的 25.358 ps 和 1200 K 的 0.004 ps，力预测 MAE 从 0.0065 eV/Å 飙升至 1.4043 eV/Å。这种退化源于模型缺乏对几何拓扑偏移的外推能力。

![[assets/figures/papers/iclr26_0012_T8VcTykTf1_Geometric_Graph_Neural_Diffusion_for_Stable_Mole/figures/005_Figure_1.jpg]]
*Figure 1: Geometric Topological Shift Analysis of the 3BPA Dataset and Extrapolation Performance Across Conformational Domains in the 3BPA Dataset: (a) Distribution of adjacency matrix of 3BPA in training data (300 K); (b) distributional difference of Adjacency matrix of 3BPA in testing set (k=300 K, 600 K, and 1200 K) and training set (300 K); (c) extrapolation performance evaluation across conformational domains in the 3BPA Dataset*

GGND 的核心机制是在全连通图上引入等变扩散过程，通过张量值注意力扩散度算子实现全局信息传播。这一扩散过程对局部截止半径等几何拓扑变化不敏感，同时保持 SE(3)‑等变性，从而从根本上缓解误差积累。评估采用两个关键稳定性指标：对于分子系统，定义 $\max_{i,j \in \mathcal{B}} | \|\mathbf{x}_i(T) - \mathbf{x}_j(T)\| - b_{ij} | > \Delta$ 为不稳定判据；对于周期性系统，采用径向分布函数偏差 $\int_0^\infty \| \langle \mathrm{RDF}(r) \rangle - \langle \mathrm{R\hat{D}F}_t(r) \rangle_{t=T}^{T+\tau} \| dr > \Delta$ 进行检测。

### 3BPA 分子系统主结果

Table 1 展示了 GGND 作为插件模块与四种基线模型（MACE、NequIP、SEGNO、VisNet）结合后在 3BPA 数据集上的表现。核心发现如下：

![[assets/figures/papers/iclr26_0012_T8VcTykTf1_Geometric_Graph_Neural_Diffusion_for_Stable_Mole/figures/008_Table_1.jpg]]
*Table 1: Accuracy and Stability on the 3BPA Dataset. MAE for energy (E, eV), force (F, eV/A), ˚ and stability (S, ps) of three baseline models and our proposed model (+GGND), trained on configurations of the flexible drug-like molecule 3BPA at 300 K and evaluated on 300 K, 600 K, 1200 K, and varied dihedral angles. Best results are in bold; tied results are underlined*

**能量预测精度大幅提升。** 在 600 K 条件下，VisNet+GGND 将能量 MAE 从 1.405 eV 降至 0.022 eV，降幅达 98.4%；MACE+GGND 在 1200 K 将能量 MAE 从 0.507 eV 降至 0.137 eV，降幅为 73.0%。这一改进在 OOD 温度下尤为显著，表明扩散机制有效捕获了高温构象中的全对相互作用。

**力预测误差系统性降低。** 所有基线模型在集成 GGND 后，力 MAE 在 600 K 和 1200 K 均显著下降。例如，NequIP+GGND 在 1200 K 将力 MAE 从 0.912 eV/Å 降至 0.265 eV/Å。力预测的准确性直接决定了 MD 模拟中原子轨迹的物理合理性。

**模拟稳定性实现数量级提升。** 这是最具决定性的证据。MACE 在 1200 K 的稳定性仅为 1.965 ps，而 MACE+GGND 提升至 29.218 ps，提升约 14.9 倍。VisNet 在 600 K 的稳定性从 25.358 ps 恢复至 100 ps（满分），在 1200 K 从 0.004 ps 提升至 8.500 ps。值得注意的是，在分布内（300 K）条件下，GGND 未造成精度损失，所有模型均保持满分稳定性。

### SAMD23 半导体系统 OOD 泛化

Table 2 展示了在更大规模半导体系统（SiN 和 HfO，最多 510 个原子）上的 OOD 测试结果。GGND 在 SiN OOD 和 HfO OOD 上分别达到 99.892 ps 和 97.928 ps 的稳定性，与 Equiformer V2 并列满分水平，而大多数对比模型（包括 Allegro、QuinNet、Neural P3M 等 SOTA 方法）的稳定性显著下降。在力预测精度方面，GGND 在 HfO Test 上达到 0.179 eV/Å 的力 MAE，比 Neural P3M（0.300 eV/Å）和 QuinNet（0.296 eV/Å）降低约 40%。这些结果表明，全连通扩散机制在处理包含多种元素和复杂键合环境的半导体系统时，同样展现出对几何拓扑偏移的强鲁棒性。

![[assets/figures/papers/iclr26_0012_T8VcTykTf1_Geometric_Graph_Neural_Diffusion_for_Stable_Mole/figures/009_Table_2.jpg]]
*Table 2: Accuracy and Stability on the 3BPA Dataset. MAE for energy per atom (E/A, eV), force (F, eV/A), and stability (S, ps) obtained by SOTA models and our proposed model (GGND), trained ˚ on SiN and HfO semiconductor molecular system. Best results are in bold*

### 消融实验与失效模式

Table 3 的消融实验验证了 GGND 各组件的必要性。消融变体 GGND†（去除全连通扩散）和 GGND‡（去除等变扩散度算子）在高温外推任务上的稳定性和准确性均明显下降。在 1200 K 条件下，完整 GGND 的稳定性为 8.500 ps，而 GGND† 和 GGND‡ 分别降至 0.004 ps 和 0.005 ps，与基线 VisNet 水平相当。这证实了完整扩散过程——包括全连通图拓扑和张量值注意力机制——对缓解几何拓扑偏移至关重要。

![[assets/figures/papers/iclr26_0012_T8VcTykTf1_Geometric_Graph_Neural_Diffusion_for_Stable_Mole/figures/010_Table_3.jpg]]
*Table 3: Ablation Analysis on the 3BPA Dataset. MAE for energy (E, eV), force (F, eV/A), and ˚ stability (S, ps) of baseline model, GGND, and two variants of GGND. Best results are in bold; tied results are underlined*

Figure 4 的 MD 轨迹可视化进一步揭示了失效模式。在 100 ps NVE 模拟中，GGND 的最大键长偏差仅偶尔略微超过阈值（约 30 ps 处出现瞬时波动后恢复），而 MACE 约 13 ps 后即出现持续不稳定性，VisNet 几乎立即崩溃。附录中的 Figure 6（NVE）和 Figure 7（NVT）在 1200 K 条件下进一步验证了这一模式，表明 GGND 在不同系综下均能维持物理合理的键长分布。

![[assets/figures/papers/iclr26_0012_T8VcTykTf1_Geometric_Graph_Neural_Diffusion_for_Stable_Mole/figures/004_Figure_4.jpg]]

### 计算开销分析

Table 5 量化了 GGND 的计算开销。以 VisNet 为基线，集成 GGND 后训练时间增加 26.54%（6.822 h → 8.633 h），100 ps MD 模拟时间增加 15.57%（1.958 h → 2.282 h），GPU 显存占用增加约 15%（20.457 GB → 23.484 GB）。考虑到 GGND 在能量/力预测精度和稳定性方面的数量级提升，这一额外开销在实践中是可接受的。全连通图扩散导致的平方级复杂度是主要瓶颈，当前方法主要适用于中小规模系统（如 3BPA 的 27 原子和 SAMD23 的最多 510 原子），未来需通过稀疏近似或分层扩散机制扩展至更大规模生物分子系统。

## 方法谱系与知识库定位

### 与现有等变消息传递框架的关系

GGND 并非一个独立的力场预测模型，而是作为一个**即插即用的插件模块**，可无缝集成到现有的局部等变消息传递（local equivariant message‑passing）框架中（参见 Figure 3(a)）。论文选取了四种代表性基线模型进行集成验证：

- **NequIP** 和 **MACE**：基于局部邻域内等变消息传递的经典骨干网络，在域内（300 K）表现优异，但面对高温构象外推时稳定性急剧下降。例如，MACE 在 1200 K 的稳定性仅为 1.965 ps（Table 1）。
- **SEGNO**：在局部等变消息传递基础上引入了二阶运动偏置（second‑order motion bias），旨在提升动力学一致性，但在几何拓扑偏移下仍出现显著性能退化（Figure 1(c)）。
- **VisNet**：当前最优的局部等变消息传递基线，在 300 K 达到满分稳定性（100 ps），但在 600 K 和 1200 K 分别骤降至 25.358 ps 和 0.004 ps（Figure 1(c)）。

GGND 的核心干预在于**将消息传递范式从局部邻域扩展为基于连续时间扩散 PDE 的全局信息传播**（Equation (1)）。这一转变的关键在于两个算子：

1. **等变梯度算子**（Equation (2)）：将节点特征差映射为高阶张量边特征，保持 SE(3)‑等变性。
2. **张量值等变扩散度算子**（Equation (3)）：基于 Clebsch‑Gordan 系数、球谐函数和径向基函数构建的注意力矩阵，调控全连通图上的信息传播速率。

这种设计使得 GGND 能够捕获任意原子对之间的全对信息流（all‑pair information flow），对局部截止半径等几何拓扑变化不敏感，从而大幅减小分布外误差。**消融实验**（Table 3）证实，去掉全连通扩散或等变扩散度算子的变体（GGND† 和 GGND‡）在高温外推任务上的稳定性和准确性均明显下降，表明完整的扩散过程对缓解几何拓扑偏移至关重要。

### 适用边界与计算代价

GGND 的适用边界受限于其**全连通图扩散机制**的计算复杂度。当前实验覆盖的系统规模为：

- **3BPA**：27 个原子的柔性类药物分子，训练 1,000 个 epoch 约需 4 小时（Table 4）。
- **SAMD23**：SiN（16–510 个原子）和 HfO 半导体系统，批量大小为 1，训练 200 个 epoch 约需 30 小时（Table 4）。

计算开销分析（Table 5）显示，在 VisNet 上集成 GGND 后：
- 训练时间增加约 **26.54%**（6.822 h → 8.633 h）
- 100 ps MD 模拟时间增加约 **15.57%**（1.958 h → 2.282 h）
- GPU 显存占用增加约 **15%**（20.457 GB → 23.517 GB）

这些额外开销在能源/力预测精度和稳定性方面的巨大提升面前是可接受的，但全连通图扩散的 $O(N^2)$ 复杂度使其**难以直接扩展至数百万原子规模的蛋白质等大生物分子系统**。这是当前方法的一个明确局限。

### 局限性与开放问题

**主要局限**：

GGND 的全对扩散机制虽然有效缓解了几何拓扑偏移，但其平方级别的计算复杂度限制了向大规模系统的直接扩展。论文明确指出，当前方法主要面向中小规模分子系统，对蛋白质等大生物分子系统的适用性需要进一步研究。

**开放问题**：

1. **大规模系统的稀疏近似**：如何将全对扩散机制高效近似处理，使其能应用于包含数十万至上百万原子的大规模生物系统，而不会导致不可接受的计算和内存开销？可能的路径包括稀疏注意力近似或分层扩散机制。

2. **时间离散化的精度‑效率权衡**：GGND 的连续时间扩散是否可以通过更精细的时间离散化（如自适应步长）进一步平衡精度与效率？当前实现采用固定离散化方案，但不同系统可能需要不同的时间分辨率。

3. **复合环境偏移下的性能边界**：在多种环境偏移（如温度、压力、化学组成等复合偏移）同时存在的情况下，GGND 的外推性能边界是否依然符合理论保证？Theorem 3.1 建立了表示变化对邻接矩阵变化的任意阶多项式控制，但其在复合偏移场景下的实证验证尚不充分。

4. **与长程相互作用模型的对比**：GGND 通过扩散过程隐式捕获长程相互作用，但与显式建模长程静电相互作用的 Neural P3M 等方法相比，在周期性系统中的适用性和精度边界尚需进一步对比研究。在 SAMD23 的 HfO 测试中，GGND 的力 MAE（0.179 eV/Å）虽优于 Neural P3M（0.300 eV/Å），但这一优势是否在更大规模系统中保持仍需验证。

## 原文 PDF

![[paperPDFs/ICLR_2026/Geometric_Graph_Neural_Diffusion_for_Stable_Molecular_Dynamics_Simulations.pdf]]
