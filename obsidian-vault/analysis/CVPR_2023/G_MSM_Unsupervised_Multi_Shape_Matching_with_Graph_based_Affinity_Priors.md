---
title: "G-MSM: Unsupervised Multi-Shape Matching with Graph-based Affinity Priors"
type: paper
paper_level: A
venue: CVPR
year: 2023
pdf_ref: paperPDFs/CVPR_2023/G_MSM_Unsupervised_Multi_Shape_Matching_with_Graph_based_Affinity_Priors.pdf
code_link: https://github.com/marvin-eisenberger/gmsm-matching
project_link: https://github.com/marvin-eisenberger/gmsm-matching
aliases:
- GM
- G-MSM
tags:
- CVPR_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "在形状集合上构建一个以自监督匹配能量为边权的完全亲和图 G；通过沿图中的最短路径传播并组合成对对应关系，得到拓扑感知的多形状匹配；训练时，引入循环一致性损失，强制多形状匹配与成对注册之间的一致性，从而将全集的形状流形结构作为隐式先验注入模型。"
primary_logic: "核心洞见：将形状集合建模为亲和图，并利用高置信度路径上的匹配组合来传播几何信息，使模型能够从整个集合的冗余中学习到更鲁棒的对应关系，而无需任何外部监督。"
claims:
- "我们引入了边加权无向形状图 G，用于逼近形状数据流形，并通过最短路径组合匹配实现多形状匹配。"
- "在近等距、拓扑噪声和跨类匹配等多个基准上取得了最优性能。"
- "移除图多匹配模块 III 会导致性能显著下降，表明该模块对性能至关重要。"
- "在 SHREC'Iso 和 TOPKIDS 上，对应误差分别降低 19% 和 73%。"
---

# G-MSM: Unsupervised Multi-Shape Matching with Graph-based Affinity Priors

> [!tip] 核心洞察
> 核心洞见：将形状集合建模为亲和图，并利用高置信度路径上的匹配组合来传播几何信息，使模型能够从整个集合的冗余中学习到更鲁棒的对应关系，而无需任何外部监督。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | G-MSM: 基于图亲和先验的无监督多形状匹配 |
| 英文题名 | G-MSM: Unsupervised Multi-Shape Matching with Graph-based Affinity Priors |
| 会议/期刊 | CVPR 2023 |
| Links | [paper](https://arxiv.org/abs/2212.02910) · [GitHub](https://github.com/marvin-eisenberger/gmsm-matching) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | G-MSM |
| Dataset | SHREC'Iso, TOPKIDS, SMAL (跨类泛化) |

> [!tip] 效果简介
> - SHREC'Iso 上，平均测地误差 为 5.2，对比 6.2 (SyNoRiM)，变化 -1.0 (约 16%)。
> - TOPKIDS 上，平均测地误差 为 7.9，对比 13.7 (DS)，变化 -5.8 (约 42%)。
> - SMAL (跨类泛化) 上，平均测地误差 为 2.6，对比 5.7 (SyNoRiM)，变化 -3.1 (约 54%)。

## 概要

**问题瓶颈**：现有的无监督深度形状匹配方法将形状集合视为无序样本，独立处理每对形状，未能充分利用形状间的几何相似性和冗余信息。这一设计在拓扑噪声、非等距变形及跨类匹配等挑战性场景下表现不稳定。

**核心方法**：G-MSM 提出在形状集合上构建一个以自监督匹配能量为边权的完全亲和图 $G$。通过沿图中的最短路径传播并组合成对对应关系，得到拓扑感知的多形状匹配。训练时，引入循环一致性损失，强制多形状匹配与成对注册之间的一致性，从而将全集的形状流形结构作为隐式先验注入模型。

**方法定位**：G-MSM 属于无监督多形状匹配方法，其核心创新在于将形状集合建模为亲和图，并利用高置信度路径上的匹配组合来传播几何信息，使模型能够从整个集合的冗余中学习到更鲁棒的对应关系，而无需任何外部监督。与独立成对匹配基线（如 UFM、SURFM、DS）和需要后处理的现有多形状匹配方法（如 CZO、SyNoRiM）相比，G-MSM 以端到端、完全无监督的方式实现了循环一致的多形状对应。

**主要结果**：在近等距、拓扑噪声和跨类匹配等多个基准上取得了最优性能。具体而言，在 SHREC'Iso 和 TOPKIDS 上，对应误差分别降低 19% 和 73%；在 SMAL 跨类泛化任务上，平均测地误差较 SyNoRiM 降低约 54%。消融实验证实，移除图多匹配模块会导致性能显著下降，验证了该模块的关键作用。

**局限性**：方法假设输入形状具有近似一致的朝向；完全亲和图的存储和查询成本随训练集大小平方增长（$O(N^2)$）；在极端非刚性变形或部分重叠匹配上的泛化性尚未充分验证。

### 问题背景

三维形状匹配是计算机视觉与图形学中的基础问题，其目标是在两个或多个几何形状之间建立有意义的逐点对应关系。该问题在纹理迁移、三维重建、形状插值与统计形状分析等任务中扮演关键角色。形式化地，给定两个形状 $\boldsymbol{\mathcal{X}}^{(i)} = (\mathbf{V}^{(i)}, \mathbf{T}^{(i)})$ 和 $\boldsymbol{\mathcal{X}}^{(j)} = (\mathbf{V}^{(j)}, \mathbf{T}^{(j)})$，形状匹配的目标是寻找一个稀疏的分配矩阵 $\mathbf{\bar{I}}^{(i,j)} \in \{0,1\}^{\bar{m} \times n}$，使得对应点之间的几何结构尽可能保持一致。

近年来，基于函数映射（functional maps）的深度学习方法在成对形状匹配上取得了显著进展。这类方法通过可微分层将特征提取与对应求解联合优化，在近等距人体形状等标准基准上表现出色。然而，当面对拓扑噪声（如自接触导致的网格合并）、非等距变形或跨类匹配等挑战性场景时，现有方法的鲁棒性仍显不足。

### 现有方法缺口

当前的无监督深度形状匹配方法存在一个根本性的结构缺陷：**它们将形状集合视为无序的独立样本，仅对随机采样的形状对进行孤立的成对匹配训练**。这种“成对独立”范式忽略了形状集合中蕴含的丰富几何冗余与全局结构信息。

具体而言，现有方法面临以下瓶颈：

1. **信息利用不充分**：一个形状集合中的多个形状往往共享相似的几何结构（如同一人体的不同姿态），这些冗余信息天然地构成了一种隐式的监督信号。独立的成对匹配无法利用这种跨形状的几何一致性。

2. **缺乏全局约束**：成对匹配仅最小化单对形状之间的特征距离，缺乏多形状之间的循环一致性约束。当 $N$ 个形状之间存在 $N(N-1)/2$ 个成对匹配时，这些匹配之间应当满足组合一致性，但现有无监督方法并未显式地利用这一性质。

3. **挑战场景下表现不稳定**：在拓扑噪声和非等距变形场景下，单对形状之间的特征信号可能高度模糊，导致匹配误差急剧上升。缺乏来自形状集合全局结构的引导，模型难以在这些困难场景中做出可靠判断。

### 本文动机

本文的核心动机源于一个关键观察：**形状集合本身构成了一个隐含的几何流形，形状之间的相似性关系可以被建模为一个图结构**。如果能够有效地捕捉并利用这一图结构，就可以将形状集合的全局几何先验注入到匹配过程中，从而引导模型学习更鲁棒的对应关系。

基于这一洞见，G-MSM 提出了一种全新的无监督多形状匹配框架。其核心思想是：

- **构建亲和图**：在训练形状集合上定义一个边加权的无向形状图 $\mathcal{G}$，其中边权由成对匹配能量决定，用于逼近底层的数据流形结构。
- **沿图传播匹配**：通过沿亲和图中的最短路径组合成对匹配，得到拓扑感知的多形状对应。
- **循环一致性训练**：引入循环一致性损失，强制多形状对应与成对注册之间的一致性，从而以自监督的方式将形状流形的全局结构注入模型训练。

这种方法无需任何外部监督标注，完全依赖形状集合内部的几何冗余来提升匹配质量。在近等距匹配、拓扑噪声匹配和跨类泛化等多个具有挑战性的设定下，G-MSM 均展现出相对于现有方法的显著性能提升。

## 核心方法与创新机理

G-MSM 的核心创新在于将无序的形状集合显式建模为**边加权无向亲和图**（shape graph），并利用该图的全局结构作为隐式先验来驱动无监督多形状匹配。与现有方法将形状视为独立样本、仅进行成对匹配不同，G-MSM 通过两个紧密耦合的“changed slots”实现了范式转变：

### 创新一：基于亲和图的多形状图匹配

现有无监督方法（如 **UFM**、**SURFM**、**DS** 等）仅对随机采样的形状对进行独立的成对匹配，完全忽略了形状集合中蕴含的几何冗余和流形结构。G-MSM 的核心突破在于：

1. **构建亲和图**：在训练形状集合 $\mathcal{S}$ 上定义一个完全图 $\mathcal{G} := (\mathcal{S}, w)$，其边权 $w(\boldsymbol{\mathcal{X}}^{(i)}, \boldsymbol{\mathcal{X}}^{(j)})$ 由双向匹配能量的最小值确定（公式 5），即：
   $$w(\boldsymbol{\mathcal{X}}^{(i)},\boldsymbol{\mathcal{X}}^{(j)}):=\min\{E_{\mathrm{match}}(\mathbf{V}^{(i,j)},\mathbf{V}^{(j)};\boldsymbol{\Pi}^{(i,j)}),E_{\mathrm{match}}(\mathbf{V}^{(j,i)},\mathbf{V}^{(i)};\boldsymbol{\Pi}^{(j,i)})\}$$
   这一设计使得边权能够以完全无监督的方式反映形状间的几何亲和度——匹配能量越低，亲和分值越高。

2. **最短路径传播匹配**：对于任意形状对 $(i, j)$，通过 Dijkstra 算法在亲和图中计算最短路径 $(i, s_1, \dots, s_{M-1}, j)$，然后沿该路径组合成对匹配以产生多形状对应：
   $$\boldsymbol{\Pi}_{\mathrm{mult}}^{(i,j)} := \boldsymbol{\Pi}^{(i,s_1)} \circ \boldsymbol{\Pi}^{(s_1,s_2)} \circ \cdots \circ \boldsymbol{\Pi}^{(s_{M-1},j)}$$
   这一机制的本质在于：当直接匹配质量较低时（例如因拓扑噪声或大变形），模型可以绕道通过高置信度的中间形状来传播几何信息，从而获得更鲁棒的对应关系。

### 创新二：循环一致性训练损失

仅有图结构本身不足以将全局信息注入模型训练。G-MSM 进一步引入了**循环一致性损失** $\ell_{\mathrm{cyc}}^{(i,j)}$（公式 7），惩罚成对变形注册与多形状对应之间的不一致：
$$\ell_{\mathrm{cyc}}^{(i,j)} := E_{\mathrm{match}}(\mathbf{V}^{(i,j)},\mathbf{V}^{(j)};\boldsymbol{\Pi}_{\mathrm{mult}}^{(i,j)})$$

最终的端到端训练目标联合优化成对匹配损失和循环一致性损失（公式 8）：
$$\ell := \mathbb{E}_{\mathcal{X}^{(i)},\mathcal{X}^{(j)}\sim\mathcal{S}}\biggl[\ell_{\mathrm{match}}^{(i,j)}+\lambda_{\mathrm{cyc}}\ell_{\mathrm{cyc}}^{(i,j)}\biggr]$$

这一设计的深层逻辑在于：成对匹配模块（DeepShells）输出的对应矩阵 $\boldsymbol{\Pi}^{(i,j)}$ 和变形顶点 $\mathbf{V}^{(i,j)}$ 仅依赖局部特征，而多形状对应 $\boldsymbol{\Pi}_{\mathrm{mult}}^{(i,j)}$ 则编码了沿图路径的全局几何一致性。通过强制两者一致，模型被迫学习能够支持全局循环一致性的特征表示，从而将整个形状流形的结构作为隐式先验注入特征提取器。

### 创新机制的有效性证据

消融实验提供了强有力的因果证据：**移除图多匹配模块 III（即仅使用成对匹配损失训练）在多个基准上导致性能显著下降**（Table 1 中 Ours vs Ours w/o III）。例如，在 SCAPE 上误差从 1.8 升至 3.3，在拓扑噪声基准 SHREC'Iso 和 TOPKIDS 上同样出现大幅退化。这表明图多匹配模块并非简单的增量改进，而是模型在挑战性场景下取得鲁棒性能的**必要条件**。

值得注意的是，这一图先验机制具有架构无关性：Table 3 显示，即使替换特征提取器或匹配层，加入模块 III 仍能一致提升所有架构变体的性能，进一步验证了其作为通用几何先验注入机制的有效性。

G-MSM 的整体流水线由三个核心模块串联构成，以形状集合 $\mathcal{S}=\{\boldsymbol{\mathcal{X}}^{(1)},\dots,\boldsymbol{\mathcal{X}}^{(N)}\}$ 为输入，在完全无监督的条件下输出多形状对应关系。流水线概览见 Figure 2。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2212_02910/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline overview. For a collection of shapes $\mathcal { S } = \{ \mathcal { X } ^ { ( 1 ) }$ , . . . , $\mathcal { X } ^ { ( N ) } \}$ , I. feature embeddings are extracted with DiffusionNet [56] and II. pairwise correspondences $\boldsymbol { \Pi } ^ { ( i , j ) }$ are predicted via an iterative, differentiable matching layer [20]. III. The pairwise matches are utilized to construct a shape graph $\mathcal { G } = \left( \boldsymbol { \mathcal { S } } , \boldsymbol { w } \right$) with affinity edge weights $\mathcal { \chi } \big ( \mathcal { X } ^ { ( i ) } , \mathcal { X } ^ { ( j ) } \big ) \geq$ 0 . During training, we minimize the pairwise matching loss $\ell _ { \mathrm { m a t c h } } ^ { (...$

**模块 I — 特征提取器**  
采用 **DiffusionNet** 作为特征骨干网络，将每个输入形状 $\boldsymbol{\mathcal{X}}^{(i)}=(\mathbf{V}^{(i)},\mathbf{T}^{(i)})$ 映射为 $l$ 维的逐顶点特征嵌入：
$$\boldsymbol{\Phi}_{\mathrm{feat}}:\boldsymbol{\mathcal{X}}^{(i)}\mapsto\mathbf{F}^{(i)}\in\mathbb{R}^{m\times l}$$
该模块为后续匹配提供统一的几何描述基底。

**模块 II — 成对匹配**  
基于可微分最优传输的 **DeepShells** 多尺度匹配方案，对任意形状对 $(\boldsymbol{\mathcal{X}}^{(i)},\boldsymbol{\mathcal{X}}^{(j)})$ 输出三项结果：
$$\Phi_{\mathrm{match}}:(\mathbf{F}^{(i)},\mathbf{F}^{(j)})\mapsto(\boldsymbol{\Pi}^{(i,j)},\mathbf{V}^{(i,j)},\ell_{\mathrm{match}}^{(i,j)})$$
其中 $\boldsymbol{\Pi}^{(i,j)}$ 为稀疏对应矩阵，$\mathbf{V}^{(i,j)}$ 为经匹配变形后的顶点坐标，$\ell_{\mathrm{match}}^{(i,j)}$ 为匹配损失。匹配能量定义为基于对应矩阵加权的特征距离：
$$E_{\mathrm{match}}(\mathbf{F},\mathbf{G};\tilde{\Pi}):=\sum_{i'=1}^{m}\sum_{j'=1}^{n}\tilde{\Pi}_{i',j'}\|\mathbf{F}_{i'}-\mathbf{G}_{j'}\|_{2}^{2}$$

**模块 III — 基于图的多形状匹配**  
这是 G-MSM 区别于现有无监督成对匹配方法的核心创新。在训练形状集合 $\mathcal{S}$ 上构建一个边加权无向完全图 $\mathcal{G}:=(\mathcal{S},w)$，其中亲和边权由双向匹配能量的最小值确定：
$$w(\boldsymbol{\mathcal{X}}^{(i)},\boldsymbol{\mathcal{X}}^{(j)}):=\min\{E_{\mathrm{match}}(\mathbf{V}^{(i,j)},\mathbf{V}^{(j)};\boldsymbol{\Pi}^{(i,j)}),E_{\mathrm{match}}(\mathbf{V}^{(j,i)},\mathbf{V}^{(i)};\boldsymbol{\Pi}^{(j,i)})\}$$
该边权直接反映形状对之间的几何亲和度——匹配能量越低，形状越相似。基于此图，通过 Dijkstra 算法计算任意形状对之间的最短路径，并沿路径组合成对匹配以获得多形状对应：
$$\boldsymbol{\Pi}_{\mathrm{mult}}^{(i,j)}:=\boldsymbol{\Pi}^{(i,s_{1})}\circ\boldsymbol{\Pi}^{(s_{1},s_{2})}\circ\cdots\circ\boldsymbol{\Pi}^{(s_{M-1},j)}$$
训练时，引入循环一致性损失 $\ell_{\mathrm{cyc}}^{(i,j)}$ 惩罚多形状对应与成对注册之间的不一致：
$$\ell_{\mathrm{cyc}}^{(i,j)}:=E_{\mathrm{match}}(\mathbf{V}^{(i,j)},\mathbf{V}^{(j)};\boldsymbol{\Pi}_{\mathrm{mult}}^{(i,j)})$$
最终端到端训练目标为成对匹配损失与循环一致性损失的联合优化：
$$\ell:=\mathbb{E}_{\boldsymbol{\mathcal{X}}^{(i)},\boldsymbol{\mathcal{X}}^{(j)}\sim\mathcal{S}}\biggl[\ell_{\mathrm{match}}^{(i,j)}+\lambda_{\mathrm{cyc}}\ell_{\mathrm{cyc}}^{(i,j)}\biggr]$$

**数据流与训练机制**  
整个网络端到端训练。形状图 $\mathcal{G}$ 在训练过程中定期更新（每隔固定 epoch 数），以反映模型不断改进的成对匹配质量。这一设计使得图结构本身成为可演化的隐式先验——随着训练推进，亲和边权逐渐精准刻画形状流形的几何结构，进而通过最短路径传播将集合层面的冗余信息注入每个成对匹配的梯度信号中。值得注意的是，循环一致性损失仅在训练阶段发挥作用；测试时，多形状匹配的改善依赖于训练过程中习得的图结构先验。消融实验（Table 1 中 Ours vs Ours w/o III）证实，移除模块 III 在多个基准上导致性能显著下降，验证了该模块在整个流水线中的关键地位。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2212_02910/figures/001_Figure_1.jpg]]
*Figure 1: For a given collection of 3D meshes $\{ \mathcal { X } ^ { ( i ) }$ | 1 $\leq$ i $\leq$ N $\}$ , (i) our method constructs, in a fully unsupervised manner, a shape graph G which approximates the underlying shape data manifold. (ii) Its edge weights (affinity scores) are derived from a putative pairwise correspondence loss signal. (iii) During training, we enforce cycle-consistency by propagating maps along shortest paths in the graph G. As shown for the sample pair above ( $\mathcal { X } ^ { ( 1 ) } , \hat { \mathcal { X } } ^ { ( 2 ) }$ ) , the resulting multi-matching $\mathbf { I I } ^ { ( 1 , 3 ) } \circ \mathbf { \hat { I } } ^ { ( \hat { 3 } , 2 ) }$ is significantly more accurate than the pairw...

G-MSM 的整体流水线由三个可微分模块串联构成，端到端联合训练。以下按数据流顺序逐一展开。

### 模块 I：特征提取器（Feature Extractor）

输入形状 $\boldsymbol{\mathcal{X}}^{(i)} = (\mathbf{V}^{(i)}, \mathbf{T}^{(i)})$ 由顶点集 $\mathbf{V}^{(i)}$ 和三角面片集 $\mathbf{T}^{(i)}$ 定义。特征提取器将每个形状映射为逐顶点的 $l$ 维嵌入：

$$
\boldsymbol{\Phi}_{\mathrm{feat}}:\boldsymbol{\mathcal{X}}^{(i)}\mapsto\mathbf{F}^{(i)}\in\mathbb{R}^{m\times l}
\tag{1}
$$

其中 $m$ 为顶点数。该模块直接采用现成的 **DiffusionNet** 作为特征骨干（Section 3.2），无需从头设计几何特征描述子。

### 模块 II：成对匹配（Pairwise Matching）

给定一对形状的特征嵌入 $\mathbf{F} \in \mathbb{R}^{m \times l}$ 和 $\mathbf{G} \in \mathbb{R}^{n \times l}$，首先定义基于最优传输的匹配能量：

$$
E_{\mathrm{match}}(\mathbf{F},\mathbf{G};\tilde{\Pi}):=\sum_{i'=1}^{m}\sum_{j'=1}^{n}\tilde{\Pi}_{i',j'}\|\mathbf{F}_{i'}-\mathbf{G}_{j'}\|_{2}^{2}
\tag{2}
$$

其中 $\tilde{\Pi}$ 为软分配矩阵。基于此能量，成对匹配函数 $\Phi_{\mathrm{match}}$ 输出三项：

$$
\Phi_{\mathrm{match}}:(\mathbf{F}^{(i)},\mathbf{F}^{(j)})\mapsto(\boldsymbol{\Pi}^{(i,j)},\mathbf{V}^{(i,j)},\ell_{\mathrm{match}}^{(i,j)})
\tag{3}
$$

- $\boldsymbol{\Pi}^{(i,j)}$：稀疏对应矩阵；
- $\mathbf{V}^{(i,j)}$：经匹配变形后的顶点坐标（用于后续循环一致性约束）；
- $\ell_{\mathrm{match}}^{(i,j)}$：成对匹配损失，直接来自最优传输能量。

该模块采用 **DeepShells** 的多尺度可微分匹配方案（Section 3.2），使整个匹配过程保持端到端可导。

### 模块 III：基于图的多形状匹配（Graph-based Multi-Matching）

这是 G-MSM 的核心创新。在形状集合 $\mathcal{S}$ 上构建一个边加权无向完全图：

$$
\mathcal{G}:=(\mathcal{S},w),\quad w:\mathcal{S}\times\mathcal{S}\to[0,\infty]
\tag{4}
$$

边权 $w$ 定义为双向匹配能量的最小值，即亲和分值（affinity score）：

$$
w(\boldsymbol{\mathcal{X}}^{(i)},\boldsymbol{\mathcal{X}}^{(j)}):=\min\{E_{\mathrm{match}}(\mathbf{V}^{(i,j)},\mathbf{V}^{(j)};\boldsymbol{\Pi}^{(i,j)}),\;E_{\mathrm{match}}(\mathbf{V}^{(j,i)},\mathbf{V}^{(i)};\boldsymbol{\Pi}^{(j,i)})\}
\tag{5}
$$

该分值完全由模块 II 的自监督匹配损失驱动，无需任何外部标注。亲和分值越低，表明两形状的几何相似性越高。

对于任意形状对 $(\mathcal{X}^{(i)}, \mathcal{X}^{(j)})$，在 $\mathcal{G}$ 上通过 Dijkstra 算法计算最短路径：

$$
(i,s_{1},\dots,s_{M-1},j):=\mathrm{Dijkstra}(\mathcal{X}^{(i)},\mathcal{X}^{(j)};\mathcal{G})
\tag{6a}
$$

沿该路径逐段组合成对对应矩阵，得到多形状对应：

$$
\boldsymbol{\Pi}_{\mathrm{mult}}^{(i,j)}:=\boldsymbol{\Pi}^{(i,s_{1})}\circ\boldsymbol{\Pi}^{(s_{1},s_{2})}\circ\cdots\circ\boldsymbol{\Pi}^{(s_{M-1},j)}
\tag{6b}
$$

这一组合操作使得信息能够沿高置信度路径在形状间传播，将整个集合的流形结构隐式注入模型。

### 训练损失函数

训练时，除了最小化成对匹配损失 $\ell_{\mathrm{match}}^{(i,j)}$，还引入循环一致性损失，惩罚成对注册与多形状对应之间的不一致：

$$
\ell_{\mathrm{cyc}}^{(i,j)}:=E_{\mathrm{match}}(\mathbf{V}^{(i,j)},\mathbf{V}^{(j)};\boldsymbol{\Pi}_{\mathrm{mult}}^{(i,j)})
\tag{7}
$$

总训练目标为两者的加权期望：

$$
\ell:=\mathbb{E}_{\mathcal{X}^{(i)},\mathcal{X}^{(j)}\sim\mathcal{S}}\biggl[\ell_{\mathrm{match}}^{(i,j)}+\lambda_{\mathrm{cyc}}\ell_{\mathrm{cyc}}^{(i,j)}\biggr]
\tag{8}
$$

其中 $\lambda_{\mathrm{cyc}}$ 为平衡系数。训练过程中，形状图 $\mathcal{G}$ 会定期根据最新的成对匹配结果更新边权，使图结构随模型能力提升而逐步精化（Section 3.3）。

### 关键设计要点

| 设计要素 | 具体选择 | 依据 |
|---------|---------|------|
| 特征骨干 | DiffusionNet | 现成架构，无需定制 |
| 成对匹配层 | DeepShells 多尺度方案 | 可微分最优传输 |
| 图拓扑 | 完全图（默认），可选 MST/TSP/星形图 | Table 2 消融表明 MST 可接近完全图精度 |
| 路径搜索 | Dijkstra 最短路径 | 保证亲和分值最优 |
| 图更新策略 | 每固定 epoch 数重新计算边权 | 适应模型进化 |

消融实验（Table 1）表明，移除模块 III（即仅保留 $\ell_{\mathrm{match}}$ 训练）会导致性能显著下降——例如在 SCAPE 上误差从 1.8 升至 3.3——证实了图多匹配模块对整体性能的关键作用。

## 实验与关键发现

### 核心实验设置与公平性

所有评估均遵循标准的 Princeton benchmark protocol，采用测地误差度量。G-MSM 完全无监督，无需任何对应标注或测试后处理；作为对照，部分基线方法（如 CZO、UDM、SyNoRiM）可能需要额外的后处理或微调步骤。对比结果均使用原作者提供的公开数据或标准协议，确保比较的公平性。在跨类匹配泛化实验中，所有模型均在 SHREC'20 上训练，直接在其他未见数据集上测试，未进行任何领域自适应。

### 近等距匹配主结果

**Table 1** 汇总了在四个近等距人体形状基准（FAUST、SCAPE、SURREAL、SHREC'19）以及两个泛化设置（FAUST→SCAPE 和 SCAPE→FAUST）上的定量对比。G-MSM 在所有设置下均取得最优性能：FAUST 上平均测地误差为 1.5，SCAPE 上为 1.8，显著优于所有成对匹配基线（UFM、SURFM、WFM、DiffNet、DS、NM）和多形状匹配基线（CZO、UDM、SyNoRiM）。移除图多匹配模块 III（即 Ours w/o III）后，SCAPE 上的误差从 1.8 上升至 3.3，FAUST 上从 1.5 上升至 1.7，表明模块 III 对最优性能至关重要。

### 拓扑噪声下的匹配

**Figure 3** 展示了在拓扑噪声基准 SHREC'Iso 和 TOPKIDS 上的累计误差曲线及平均误差表。G-MSM（红色曲线）在两个基准上均显著优于所有基线。具体而言，SHREC'Iso 上平均测地误差为 5.2，相比 SyNoRiM（6.2）降低约 16%；TOPKIDS 上平均测地误差为 7.9，相比 DS（13.7）降低约 42%。**Figure 4** 的定性对比进一步印证：在 SHREC'Iso 的真实扫描手部模型上（手指自接触导致的拓扑合并），G-MSM 与 DS、CZO 均能产生较合理的对应，但 DS 和 CZO 在食指与中指前端存在明显错误。

### 跨类匹配泛化

**Figure 5**（左表）报告了跨类匹配的定量对比。在 SHREC'20 上训练后直接泛化至 SMAL 测试集时，G-MSM 的平均测地误差为 2.6，相比 SyNoRiM（5.7）降低约 54%，展现了强大的跨类泛化能力。**Figure 5**（右）通过 2D MDS 可视化 TOSCA 上的形状图节点嵌入：由于学习到的边权表达了亲和分值，几何相似的形状倾向于聚类在一起，直观验证了形状图先验的有效性。

### 消融实验

#### 图拓扑消融

**Table 2** 对比了不同图拓扑 G 的性能。在 SHREC'Iso 和 TOPKIDS 上，稀疏图拓扑（如最小生成树 MST、旅行商路径 TSP、星形图）可获得与完全图接近的匹配精度，同时大幅降低计算和存储开销。完全移除模块 III（w/o III）导致两个基准上误差显著上升，再次确认该模块的关键作用。值得注意的是，即使测试时无法构建图，训练时使用图结构仍然能够提升模型性能（Table 2 底部一行），表明图先验在训练阶段已有效注入特征学习。

#### 网络架构消融

**Table 3** 对比了替换特征提取器 I 或匹配模块 II 的影响。无论使用何种现成架构组合，加入图多匹配模块 III 均能一致提升性能，证明模块 III 的增益与具体网络架构选择无关，具有通用性。

### 计算成本分析

**Table 4** 报告了不同训练集大小下的经验训练成本。完全亲合图的存储和查询成本随训练集大小平方增长（O(N²)），扩展至大规模形状集合时计算开销较高。**Table 5** 对比了测试时全图与 MST 图的查询时间和存储成本：稀疏图可显著降低开销，但可能损失部分精度，需根据实际场景权衡。

### 失败模式与局限性

1. **朝向假设**：方法假设输入形状具有近似一致的朝向（弱监督设定），可能不适用于任意旋转的扫描数据。
2. **大规模扩展性**：完全亲合图的 O(N²) 存储和查询成本限制了其在大规模形状集合上的直接应用；稀疏图可缓解但精度有所折损。
3. **领域泛化**：实验主要聚焦于人体和动物形状，对极端非刚性变形或部分重叠匹配的泛化性尚未充分验证。
4. **图可靠性依赖**：循环一致性损失仅在训练时发挥作用；当测试形状与训练分布差异较大时，图边的亲合分值可能不准确，影响多形状匹配质量。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2212_02910/figures/003_Table_1.jpg]]
*Table 1: Nearly isometric matching. A quantitative comparison on four nearly-isometric human shape benchmarks, FAUST [5], SCAPE [1], SURREAL [60] and SHREC’19 [40]. Following prior work [15, 55, 56], we additionally show generalization results when training on FAUST and testing on SCAPE (F on S), and vice versa. We consider both standard, pairwise baselines [19,20,23,50,55,56] and multi-matching approaches [10, 25, 27]*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2212_02910/figures/010_Table_2.jpg]]
*Table 2: Graph topology comparison. We compare the quantitative performance of our model for different graph topologies G. Specifically, we revisit the experiment from Figure 3 and report the mean geodesic error on SHREC’Iso [16] and TOPKIDS [32]. The standard ‘full’ graph is compared to three sparse topologies ‘MST’, ‘TSP’, ‘star’ graph, as well as the ‘w/o III’ variant of our pipeline*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2212_02910/figures/014_Table_4.jpg]]
*Table 4: Empirical training cost. We quantify the computation cost of our pipeline for different training set sizes. For a given number of shapes N = ∣S∣, one epoch consists of #pairs $\mathbf { \bar { \Psi } } = N ^ { 2 } \in \hat { \{ 1 0 ^ { 2 } , . . . , 1 0 0 ^ { 2 } \} }$ optimization steps that each match a pair of shapes ${ \mathcal { X } } ^ { ( i ) } , { \mathcal { X } } ^ { ( j ) } \in$ S

## 定位与知识库关联

### 1. 问题定位：从成对匹配到多形状匹配

G-MSM 瞄准的核心瓶颈在于：现有无监督深度形状匹配方法（如 **UFM**、**SURFM**、**WFM**）将形状集合视为无序样本，独立处理每对形状，未能利用形状间的几何相似性和冗余信息。这导致在拓扑噪声、非等距变形及跨类匹配等挑战性场景下表现不稳定。相比之下，传统公理化多形状匹配方法（如 **CZO**）虽然追求循环一致性，但依赖手工特征和后处理，缺乏端到端学习能力；而学习型多形状匹配方法（如 **UDM**、**SyNoRiM**）则通过规范嵌入间接实现一致性，未显式建模形状间的成对亲和关系。

G-MSM 的独特定位在于：**首次在无监督深度学习框架中，将形状集合显式建模为亲和图，并利用图上的最短路径传播来组合成对匹配，从而将全集的形状流形结构作为隐式先验注入模型训练**。这一思路将多形状匹配从“独立成对匹配 + 后处理循环一致”的范式，转变为“图结构引导的联合学习”范式。

### 2. 技术谱系与关键差异

#### 2.1 特征提取与成对匹配的继承与改造

G-MSM 的流水线前两个模块直接继承自现有工作：
- **特征提取器**采用 **DiffNet**（DiffusionNet），该架构通过扩散过程在非欧几里德域上学习点特征，是目前无监督形状匹配的主流 backbone。
- **成对匹配模块**基于 **DS (DeepShells)** 的多尺度可微分最优传输方案，输出对应矩阵 $\boldsymbol{\Pi}^{(i,j)}$、变形顶点 $\mathbf{V}^{(i,j)}$ 和匹配损失 $\ell_{\mathrm{match}}^{(i,j)}$。

G-MSM 的核心创新不在于替换这些组件，而在于**在其上叠加图多匹配模块 III**，使得原本独立的成对匹配输出被组织成全局一致的图结构。

#### 2.2 图多匹配模块：核心创新点

与所有 baseline 的关键差异体现在两个“changed slots”上：

| 设计维度 | Baseline 做法 | G-MSM 做法 |
|---------|-------------|-----------|
| **多形状匹配机制** | 仅使用随机对采样进行独立的成对匹配，不考虑形状间全局结构（UFM、SURFM、WFM、DS、NM） | 构建完全亲和图 $\mathcal{G}=(\mathcal{S},w)$，边权 $w(\mathcal{X}^{(i)},\mathcal{X}^{(j)})$ 由双向匹配能量的最小值定义（式 5）；通过 Dijkstra 最短路径传播并组合成对匹配，产生循环一致的多形状对应 $\boldsymbol{\Pi}_{\mathrm{mult}}^{(i,j)}$（式 6） |
| **训练损失** | 仅最小化成对匹配损失 $\ell_{\mathrm{match}}$ | 添加循环一致性损失 $\ell_{\mathrm{cyc}}$，惩罚多形状对应与成对变形注册之间的不一致，联合优化 $\ell = \ell_{\mathrm{match}} + \lambda_{\mathrm{cyc}}\ell_{\mathrm{cyc}}$（式 7-8） |

这一设计使得模型在训练时能够利用整个集合的冗余信息：即使某对形状的直接匹配不可靠（如拓扑噪声导致自接触区域错误），通过高置信度路径上的匹配组合仍可获得更准确的对应关系。

#### 2.3 与多形状匹配方法的对比

- **CZO（公理化多形状匹配）**：通过函数映射的逐步细化实现循环一致性，但依赖预定义的特征描述子和手工后处理，无法端到端学习。G-MSM 则将循环一致性作为可微分损失融入训练，使得特征提取器能够自适应地学习有利于多形状匹配的表示。
- **UDM / SyNoRiM（学习规范嵌入）**：通过将形状映射到规范空间间接实现多形状匹配，但未显式建模成对亲和关系。G-MSM 的图结构显式编码了形状间的相似度，在跨类匹配等场景下具有更好的可解释性和鲁棒性（Figure 5 右侧的 MDS 可视化表明，学习到的图嵌入自然地按几何相似性聚类）。

### 3. 适用边界与局限

#### 3.1 已验证的适用场景

- **近等距匹配**：在 FAUST、SCAPE、SURREAL、SHREC'19 四个基准上取得最优性能（Table 1），且跨数据集泛化（F on S、S on F）表现稳定。
- **拓扑噪声匹配**：在 SHREC'Iso 和 TOPKIDS 上，对应误差分别降低 19% 和 73%（Figure 3），对自接触导致的拓扑合并具有显著鲁棒性。
- **跨类匹配**：在 SMAL 动物模型上，平均测地误差从 SyNoRiM 的 5.7 降至 2.6（约 54% 提升，Figure 5），表明图先验对非等距变形同样有效。

#### 3.2 明确局限

1. **朝向假设**：方法假设输入形状具有近似一致的朝向（弱监督设定），可能不适用于任意旋转的扫描数据。这一假设继承自底层成对匹配模块 DeepShells 的设计。
2. **计算扩展性**：完全亲和图的存储和查询成本随训练集大小平方增长（$\mathcal{O}(N^2)$）。Table 4 和 Table 5 的经验评估表明，当训练形状数量从 10 增至 100 时，每 epoch 的优化步数从 $10^2$ 增至 $100^2$，内存和查询时间显著上升。稀疏图拓扑（如 MST）可缓解此问题（Table 2），但可能损失部分精度。
3. **领域泛化未充分验证**：实验主要聚焦于人体和动物形状，对极端非刚性变形（如衣物大幅摆动）或部分重叠匹配的泛化性尚未充分验证。
4. **测试时图依赖**：循环一致性损失仅在训练时发挥作用。测试时多形状匹配的改善依赖于图结构的可靠性，当测试形状与训练分布差异较大时，图边的亲和分值可能不准确。不过 Table 2 的消融实验表明，即使在测试时无法构建图，训练时使用图结构仍能提升模型性能，说明图先验已被内化到特征提取器中。

### 4. 开放问题

1. **部分形状匹配扩展**：当前框架假设输入为完整形状，如何将图多匹配机制扩展到部分视图匹配（如通过可学习的部分函数映射）是一个自然的研究方向。
2. **理论保证**：实验表明沿最短路径组合匹配优于直接成对匹配，但能否为多形状匹配提供理论保证（如证明其严格优于独立成对匹配的误差上界）仍是开放问题。
3. **在线/流式场景**：在在线或流式场景下，如何高效地维护和更新形状图（而非定期全量重建）是实际部署的关键挑战。
4. **自适应图拓扑学习**：当前图拓扑依赖预定义的启发式（全连接或 MST），能否自动学习最优的图拓扑（如通过可微分的边剪枝或图神经网络）是一个值得探索的方向。Table 2 中 MST 在 TOPKIDS 上性能与全图接近（7.9 vs 7.9），暗示稀疏拓扑已具备竞争力，但最优稀疏结构可能因数据集而异。

### 5. 知识库定位总结

G-MSM 处于**无监督深度学习**与**多形状匹配**的交叉点，其核心贡献在于将图结构先验引入端到端学习框架。与现有工作的关系可概括为：
- **继承**：DiffusionNet（特征提取）和 DeepShells（成对匹配）作为基础组件。
- **超越**：通过图多匹配模块和循环一致性损失，将独立成对匹配提升为拓扑感知的多形状联合学习，在拓扑噪声和跨类匹配等挑战性场景下取得显著提升。
- **启发**：图先验的思想可推广至其他需要利用集合冗余的无监督学习任务，稀疏图拓扑的探索也为大规模应用提供了可行路径。

## 原文 PDF

![[paperPDFs/CVPR_2023/G_MSM_Unsupervised_Multi_Shape_Matching_with_Graph_based_Affinity_Priors.pdf]]
