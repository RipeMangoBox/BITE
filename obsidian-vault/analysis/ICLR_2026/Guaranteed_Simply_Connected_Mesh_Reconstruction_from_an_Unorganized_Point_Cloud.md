---
title: Guaranteed Simply Connected Mesh Reconstruction from an Unorganized Point Cloud
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Guaranteed_Simply_Connected_Mesh_Reconstruction_from_an_Unorganized_Point_Cloud_5f2be3ee1ede.pdf
project_link: null
code_link: "https://github.com/NVIDIA/cutlass"
aliases:
- HBSCMR
- GSCMRFUPC
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 通过 Helmholtz-Hodge 分解 (HHD) 从缠绕数场提取谐波分量 γ，并在线性系统中消除该分量，强制平凡的第一上同调群 H¹，从而移除所有非边界 2-循环，保证表面封闭且单连通。
primary_logic: 将基于缠绕数场的拓扑控制从二维曲线推广到三维曲面，利用 HHD 将拓扑约束转化为可求解的线性代数问题，并结合谱初始化与交替鲁棒优化，以代数方式保证生成封闭、单连通的网格表面。
claims:
- 在 CrossSDF 薄结构基准上，本文方法的连通分量数 (CC) 显著低于所有基线，例如 Alveolis 对齐上的 CC=1（理想单连通），而 CrossSDF 产生多个连通分量。
- 与最先进的 CrossSDF 相比，Chamfer 距离减少 15.8%，Hausdorff 距离减少 9.62%。
- 消融实验表明，去除谱初始化、鲁棒优化（L0 范数）或交替优化任一组件，都会导致重建失败或拓扑错误。
- CrossSDF medical benchmark (Alveolis aligned) 上 Chamfer Distance (CD×100) = 0.41
---

# Guaranteed Simply Connected Mesh Reconstruction from an Unorganized Point Cloud

> [!tip] 核心洞察
> 将基于缠绕数场的拓扑控制从二维曲线推广到三维曲面，利用 HHD 将拓扑约束转化为可求解的线性代数问题，并结合谱初始化与交替鲁棒优化，以代数方式保证生成封闭、单连通的网格表面。

| 字段 | 内容 |
|------|------|
| 中文题名 | 从无组织点云中保证单连通的网格重建 |
| 英文题名 | Guaranteed Simply Connected Mesh Reconstruction from an Unorganized Point Cloud |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=jjEnTBsffi) · [paper](https://arxiv.org/abs/2501.11871) · [Code](https://github.com/NVIDIA/cutlass) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | HHD-based simply-connected mesh reconstruction |
| Dataset | CrossSDF medical benchmark, Synthetic Stanford Bunny with outliers |

> [!tip] 效果简介
> - CrossSDF medical benchmark (Alveolis aligned) 上，Chamfer Distance (CD×100) 0.41 vs CrossSDF (higher) (-15.8%)；Connected Components (CC) 1 vs CrossSDF (multiple) (significantly better)。
> - Synthetic Stanford Bunny with outliers 上，Robustness (visual quality) 完整且无洞 vs Screened PSR / SALD (显著更优)。

## 概要

从无组织点云中重建封闭且拓扑正确的曲面是计算机图形学与医学影像分析中的基础问题。现有表面重建方法，无论是经典的隐式方法（如 Screened Poisson Surface Reconstruction）还是基于神经隐式场的最新方法（如 **CrossSDF** (Walker et al., CVPR 2025)、**OReX** (Sawdayee et al., CVPR 2023)），普遍缺乏对输出曲面拓扑的显式控制——它们无法保证重建结果同胚于球体（即单连通），从而在医学器官建模、血管重建等对拓扑正确性要求严苛的应用中产生虚假的连通分量和多余的手柄（handles）。

本文提出一种基于 Helmholtz-Hodge 分解（HHD）的单连通网格重建方法，核心贡献在于将拓扑控制从二维曲线推广到三维曲面：通过在缠绕数场（winding number field）的框架中引入 HHD，提取并消除谐波分量 γ，从而强制平凡的第一上同调群 H¹，以代数方式保证输出曲面封闭且单连通。该方法将拓扑约束转化为可求解的线性代数问题，无需依赖启发式后处理或对训练数据的隐式拓扑先验。

方法流水线包含两个关键阶段：初始化阶段通过八叉树引导的增强 Delaunay 三角剖分构建基础四面体网格，并利用谱方法初始化三角形方向；交替优化阶段则迭代地在“HHD 分解与校正表面计算”和“方向重定向”之间循环，以逐步剔除异常三角形。校正表面的优化采用 L₀ 范数目标函数，通过迭代加权最小二乘（IRLS）实现，相比传统 L₁ 范数或线性规划具有更强的稀疏性和抗异常值能力。

在 CrossSDF 薄结构医学基准上的实验表明，本文方法在 Alveolis 对齐数据上实现了连通分量数 CC=1（即理想单连通），而基线方法 CrossSDF 产生多个连通分量；与 CrossSDF 相比，Chamfer 距离降低 15.8%，Hausdorff 距离降低 9.62%。消融实验进一步验证了谱初始化、鲁棒优化（L₀ 范数）和交替优化三个组件对最终拓扑正确性均不可或缺。

**局限性**方面，当前方法仅保证单连通重建，无法处理更高亏格的拓扑（如环面）；此外，方法依赖全局三角剖分构建，对大规模点云存在计算瓶颈，且初始化阶段在点云极度稀疏或非均匀时可能不准确。未来方向包括通过选择性保留部分谐波分量以支持任意亏格拓扑，以及将该表征与生成模型结合以学习具有可控拓扑的 3D 形状先验。

### 从点云到曲面：隐式重建的拓扑盲区

从无组织点云重建三维曲面是计算机图形学与几何处理的核心问题，在医学影像、逆向工程和数字孪生等领域有广泛应用。现有方法——无论是经典的 **Screened Poisson Surface Reconstruction**，还是基于神经隐式场的 **SALD** (Atzmon & Lipman, ICLR 2021)、**OReX** (Sawdayee et al., CVPR 2023) 和 **CrossSDF** (Walker et al., CVPR 2025)——在几何精度上取得了显著进展，但它们共享一个根本性缺陷：**缺乏拓扑控制**。这些方法无法保证输出曲面的拓扑类型，重建结果可能包含孔洞、非流形边或多余的环柄（handles），导致曲面在拓扑上不可靠。

这一问题在医学应用中尤为突出。以肺血管重建为例（Figure 1），输入为 CT 扫描的截面点云，理想输出应为单连通曲面（同胚于球体）。然而，CrossSDF 的重建结果包含 6 个连通分量和大量虚假环柄，无法直接用于血流模拟、手术规划等下游任务。

### 瓶颈：拓扑约束从何而来？

问题的本质在于，现有方法将曲面重建视为纯粹的几何拟合问题——最小化点云到曲面的距离——而忽略了曲面的拓扑结构。要从根本上解决这一问题，需要回答一个更深刻的数学问题：**如何在重建过程中强制曲面的拓扑类型？**

二维曲线重建已经给出了部分答案。通过缠绕数场（winding number field）的拓扑分析，可以保证重建曲线是简单闭合的。但三维曲面重建面临更复杂的挑战：曲面的拓扑由第一上同调群 $H^1$ 刻画，强制 $H^1$ 平凡（即单连通）等价于消除所有非边界的 2-循环（2-cycles），这需要处理离散微分形式在三维四面体网格上的全局约束。

### 核心思路：将拓扑约束转化为代数问题

本文的核心洞察是将上述拓扑约束转化为可求解的线性代数问题。具体而言，利用 **Helmholtz-Hodge 分解 (HHD)** 从缠绕数场中提取谐波分量 $\gamma$，该分量编码了曲面的拓扑信息。通过在线性系统中消除 $\gamma$，可以强制 $H^1$ 平凡，从而以代数方式保证输出曲面封闭且单连通。

这一思路将拓扑控制从二维曲线推广到三维曲面，并结合谱初始化与交替鲁棒优化，形成一个完整的重建流水线。其关键优势在于：**拓扑保证是严格的数学结论，而非经验性的启发式约束**。

## 核心方法与创新机理

本文的核心创新在于将**拓扑控制**从启发式后处理提升为重建算法的一等公民，通过代数化方法**保证**输出网格为单连通（同胚于球体）。其关键在于识别并操控了缠绕数场的**谐波分量 γ**——该分量编码了表面的非平凡拓扑特征（如洞、手柄），并通过线性系统将其强制消去，从而移除所有非边界的 2-循环。

具体而言，方法在以下四个维度上实现了突破性改进：

### 1. 谐波分量的代数化消除（核心机制）

传统方法（如 Screened Poisson Surface Reconstruction）无法保证输出的拓扑正确性，因为它们缺乏对一阶上同调群 $H^1$ 的控制。本文的因果杠杆在于：将离散 1-形式 $\omega$ 进行 **Helmholtz-Hodge 分解**：

$$\omega = d_0 \alpha + \delta_2 \beta + \gamma$$

其中 $\gamma$ 为谐波分量，其维度等于曲面亏格数的两倍。通过在线性系统中显式约束 $\gamma = 0$，方法强制 $H^1$ 平凡，从而从代数层面保证重建曲面封闭且单连通。这一机制将拓扑控制转化为可求解的线性代数问题，而非依赖几何启发式。

### 2. 谱初始化的方向估计

三角形方向的初始化质量直接影响谐波分量的消除效果。基线方法通常采用随机或法线启发式初始化，容易引入虚假的拓扑特征。本文提出**谱方法**：将谐波分量表示为方向向量的线性函数 $\gamma = A\mathbf{x}$，并通过求解 $A^T A$ 的最小特征值对应的特征向量来优化 $\mathbf{x}$，使得 $\gamma$ 的范数最小化。这一初始化策略为后续优化提供了拓扑上更合理的起点。

### 3. L0 范数鲁棒优化

校正表面 $\Lambda$ 的优化目标直接影响对异常值的容忍度。Feng et al. (2023) 使用 L1 范数或线性规划，对大面积异常三角形的惩罚不足。本文改用 **L0 范数**：

$$\min_{\sigma_T} \sum_{f\in \mathcal{F}} \operatorname{Area}(f) |\Lambda_f|^0$$

并通过迭代加权最小二乘 (IRLS) 实现，利用二面角拉普拉斯算子（边权重定义见 Figure 6）作为正则化项。L0 范数直接惩罚非零面的数量，在稀疏性假设下更有效地剔除异常三角形，同时保留几何细节。

### 4. 交替优化策略

单次重建无法有效处理初始方向估计中的系统性偏差。本文提出**交替优化**：迭代地在“基于当前方向重建校正表面”和“利用重建结果更新三角形方向”之间切换。每次迭代中，不符合当前重建的三角形被重新定向或剔除，逐步收敛到一致的方向场。消融实验（Figure 5）证实，去除交替优化后，单次优化无法有效剔除所有异常值，导致重建质量显著下降。

### 5. 增强的三角剖分构建

基础三角剖分的质量影响后续所有计算。传统方法仅使用 3D Delaunay 三角剖分，在点云稀疏区域可能产生狭长四面体，导致数值不稳定。本文通过**八叉树引导的辅助点插入**：在包围盒的稀疏网格中心插入额外点后再进行 Delaunay 剖分，有效改善了四面体质量，为 HHD 分解和线性系统求解提供了更稳定的离散域。

| 改进维度 | 基线做法 | 本文方法 | 作用机制 |
|---------|---------|---------|---------|
| 拓扑控制 | 无保证 | HHD 消去 γ | 代数化保证单连通 |
| 方向初始化 | 随机/法线启发式 | 谱特征向量优化 | 最小化初始谐波分量 |
| 优化目标 | L1 范数 | L0 范数 (IRLS) | 稀疏性促进异常值剔除 |
| 优化策略 | 单次重建 | 交替迭代 | 逐步收敛至一致方向场 |
| 剖分构建 | 纯 Delaunay | 八叉树增强 Delaunay | 改善四面体质量 |

本文提出一种从无组织点云中重建**保证单连通**的封闭网格表面的方法。整个流水线分为两大阶段：**初始化阶段**和**交替优化阶段**，如 Figure 2 所示。

![[assets/figures/papers/paper_list_l73_https_openreview_net_forum_id_jjEnTBsffi/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our approach. (a) Input unoriented point cloud. (b) The initialization stage computes a base triangulation (left) and an initial orientation of the boundary faces*

### 输入与输出

- **输入**：无方向的无组织点云，可能包含噪声和异常值。
- **输出**：一个封闭的、单连通的三角网格表面（同胚于二维球面），即拓扑上无洞、无手柄。

### 初始化阶段

初始化阶段完成两项准备工作：

1. **基础三角剖分构建**：将输入点云与稀疏网格的单元中心进行增强，然后执行 3D Delaunay 三角剖分，得到包围点云的四面体网格。这一增强步骤避免了狭长四面体的产生，为后续计算提供高质量的体网格基础。
2. **三角形初始方向估计**：通过谱方法初始化边界面的方向。具体而言，将谐波分量 $\gamma$ 表示为方向向量 $\mathbf{x}$ 的线性函数 $\gamma = A\mathbf{x}$，并通过最小化 $\|A\mathbf{x}\|^2 / \|\mathbf{x}\|^2$ 的 Rayleigh 商求得最优方向，其解为 $A^T A$ 的最小特征值对应的特征向量。这一步骤为后续 HHD 分解提供合理的初始 1-形式 $\omega$。

### 交替优化阶段

该阶段是方法的核心，迭代执行以下两个步骤直至收敛：

1. **核心模块（HHD 分解与校正表面）**：以当前的方向化三角形集合为输入，执行 Helmholtz-Hodge 分解，将离散 1-形式 $\omega$ 分解为精确分量 $d_0\alpha$、共精确分量 $\delta_2\beta$ 和谐波分量 $\gamma$：
   $$\omega = d_0 \alpha + \delta_2 \beta + \gamma$$
   谐波分量 $\gamma$ 编码了当前方向配置中的拓扑障碍。核心模块通过求解一个线性系统来消除 $\gamma$，强制平凡的第一上同调群 $H^1$，从而移除所有非边界 2-循环。具体做法是构建一个**校正 2-链** $\Lambda$，通过 L0 范数优化（以迭代加权最小二乘实现）来稀疏地修正表面，输出一个单连通的体网格，其边界逼近输入三角形。

2. **方向更新**：根据当前重建的表面，重新选择和定向输入三角形，剔除异常值，为下一轮核心模块提供更新后的方向化三角形集合。

### 最终曲面提取

在交替优化收敛后，求解跳变谐波场并四舍五入得到整数 3-链 $W$，最终重建曲面 $S$ 定义为该 3-链的边界：
$$S = \partial W$$
这一代数构造保证了输出曲面封闭且同调平凡（即单连通）。

### 关键设计决策

- **拓扑控制机制**：区别于现有方法仅追求几何精度，本框架通过 HHD 将拓扑约束（单连通性）转化为可求解的线性代数问题，以代数方式保证拓扑正确性。
- **鲁棒性保障**：L0 范数优化和交替迭代策略共同作用，使方法对噪声和异常值具有较强鲁棒性。消融实验表明，移除任一组件均会导致重建失败或拓扑错误。
- **无需法线信息**：与部分基线方法（如 Screened Poisson Surface Reconstruction）不同，本方法仅需点云位置信息，不依赖输入法线。

### 核心模块：基于 HHD 的校正表面重建

本文方法的核心模块是一个鲁棒的拓扑控制单元：输入为一组带方向的三角形（位于 3D 三角剖分中），输出一个单连通的体积网格，其边界逼近输入三角形。该模块将 **Feng et al. (2023)** 的缠绕数场方法从二维曲线推广到三维曲面，核心机制是通过 **Helmholtz-Hodge 分解 (HHD)** 提取并消除谐波分量，从而强制平凡的第一上同调群 $H^1$，代数化地保证输出表面封闭且同胚于球面。

具体而言，模块首先在输入的有向三角形集合上定义一个离散 1-形式 $\omega$，对其进行 HHD 分解：

$$\omega = d_0 \alpha + \delta_2 \beta + \gamma$$

其中 $d_0 \alpha$ 为精确分量，$\delta_2 \beta$ 为共精确分量，$\gamma$ 为**谐波分量**——它编码了与拓扑缺陷（如非平凡循环、手柄）相关的信息。若 $\gamma = 0$，则 $\omega$ 是某个 0-形式的外微分，对应的缠绕数场无跳变，重建表面必为单连通。因此，核心问题转化为：寻找一个校正 2-链 $\Lambda$，使得修正后的 1-形式 $\omega' = \omega + \delta_2 \Lambda$ 的谐波分量消失。

### 缠绕数场的降维表示

为高效求解校正链，模块采用降维坐标表示。对每个四面体 $T$ 和顶点 $v$，缠绕数场 $u$ 被分解为：

$$u_v^T = (u_0)_v + c_v^T$$

其中 $(u_0)_v$ 是在参考四面体 $T_{\text{ref}}$ 上的基场值，$c_v^T$ 编码了从 $T_{\text{ref}}$ 到 $T$ 沿面相邻四面体路径累积的**跳变信息**。跨相邻四面体 $T_1, T_2$ 的势差与顶点无关：

$$u_v^{T_1} - u_v^{T_2} = c_v^{T_1} - c_v^{T_2}$$

这一性质将跳变约束简化为标量变量，大幅降低了优化问题的维度。

### 校正链的稀疏优化

谐波分量 $\gamma$ 提取后，需寻找校正 2-链 $\Lambda$（定义在三角剖分的面上），使得其补微分 $\delta_2 \Lambda$ 抵消 $\gamma$。对于任意边 $(i,j)$，一致性约束为：

$$(D \sigma)_{ij} = \gamma_{ij}$$

其中 $D$ 为 Darboux 梯度算子，$\sigma$ 为每个四面体上的势函数。校正表面 $\Lambda$ 的优化目标采用 **$L^0$ 范数**以促进稀疏性，从而鲁棒地剔除异常三角形：

$$\min_{\sigma_T} \sum_{f \in \mathcal{F}} \operatorname{Area}(f) \, |\Lambda_f|^0$$

该优化通过**迭代加权最小二乘 (IRLS)** 实现，在每次迭代中根据当前残差更新权重，逐步压制离群面的影响。相比传统 $L^1$ 范数或线性规划方法，$L^0$ 范数能更有效地产生稀疏解，使校正表面仅包含必要的拓扑修正面片。

### 最终曲面提取

求解得到势函数 $\sigma$ 后，构建跳变谐波场并四舍五入得到整数 3-链 $W$，最终重建曲面定义为其边界：

$$S = \hat{o}_3 W$$

由于 $W$ 的构造保证了其边界无 2-循环（即 $H^1$ 平凡），$S$ 必然是封闭且单连通的网格表面。这一代数化保证是本文方法区别于所有现有隐式重建方法的核心优势。

### 谱初始化与方向编码

在进入核心模块之前，需要为输入三角形赋予初始方向。本文通过**谱方法**优化方向向量 $\mathbf{x}$，使得由方向编码的谐波分量 $\gamma = A \mathbf{x}$ 最小化。具体地，求解 $A^T A$ 的最小特征值对应的特征向量作为初始方向 $\mathbf{x}^\star$，其中 1-形式 $\omega$ 由方向向量经稀疏矩阵 $B$ 编码：$\omega = B \mathbf{x}$。这一初始化步骤为后续交替优化提供了拓扑上接近正确的起点。

### 交替优化策略

整个重建流程采用**交替优化**：初始化后，核心模块输出当前重建曲面，随后根据该曲面更新有向三角形集合（剔除与当前曲面不一致的面），再重新运行核心模块。这一迭代过程逐步去除异常值，使重建收敛到几何精确且拓扑正确的表面。消融实验表明，去除交替优化、谱初始化或 $L^0$ 鲁棒优化中任一组件，均会导致重建失败或拓扑退化（详见 Figure 5）。

![[assets/figures/papers/paper_list_l73_https_openreview_net_forum_id_jjEnTBsffi/figures/008_Figure_6.jpg]]
*Figure 6: Edge weight*

## 实验与关键发现

### 实验设置与评估基准

我们在 **CrossSDF** 医学基准 (Walker et al., CVPR 2025) 的六个挑战性薄结构模型上进行了评估。这些模型从 CT 截面重建而来，包含肺泡 (Alveolis)、冠状动脉 (Coronaries) 等解剖结构。对于 Coronaries 数据集，其由三个解剖上分离的管状段组成，我们使用单链接聚类进行预分割后分别处理——这一预处理步骤可能对比较的公平性产生影响，因为基线方法直接处理整个点云。所有方法使用相同的输入点云和相同的评估指标，基线参数均采用其推荐设置。

评估指标包括 **Chamfer Distance (CD×100)**、**Hausdorff Distance (HD×100)** 和 **连通分量数 (CC)**。CC 是衡量拓扑质量的核心指标——理想单连通表面的 CC=1。基线方法包括 **CrossSDF** (Walker et al., CVPR 2025)、**OReX** (Sawdayee et al., CVPR 2023)、**Screened Poisson Surface Reconstruction** 和 **SALD** (Atzmon & Lipman, ICLR 2021)。

### 主要定量结果

Table 1 展示了在薄结构数据集上的定量对比。在 Alveolis aligned 数据集上，本文方法取得了 **CD 0.41, HD 11.8, CC 1** 的结果。与最先进的 CrossSDF 相比，**Chamfer 距离降低 15.8%，Hausdorff 距离降低 9.62%**。更重要的是，本文方法是唯一在 Alveolis 对齐数据上实现 CC=1 的方法，而 CrossSDF 产生了多个连通分量——这直接验证了核心声明：**方法能够保证生成单连通的封闭表面**。

![[assets/figures/papers/paper_list_l73_https_openreview_net_forum_id_jjEnTBsffi/figures/004_Table_1.jpg]]
*Table 1: Quantitative results on thin structures across different methods and metrics. The table compares the Chamfer Distance(CD)×100, Hausdorff Distance(HD)×100, and number of Connected Components(CC), under both aligned and non-aligned versions of each structure. Note on the Coronaries dataset: because our core algorithm is designed to reconstruct a single simply connected component, we leveraged prior knowledge to pre-segment the Coronaries point cloud into three anatomical components. Each component is reconstructed independently, and the results were aggregated*

在 Coronaries aligned 数据集上，本文方法取得了 CD 0.26, HD 4.6, CC 3。CC=3 反映了该解剖结构本身由三个分离的管状段组成，经过单链接聚类预分割后分别重建，因此每个子结构均为单连通，整体结果与解剖学事实一致。

### 鲁棒性分析

Figure 4 展示了在不同噪声和异常值水平下合成斯坦福兔子的重建对比。在增加异常值数量的情况下，Screened PSR 和 SALD 的重建表面出现明显孔洞和断裂，而本文方法保持了**完整且无洞的封闭表面**。这一鲁棒性来源于两个关键设计：(1) L0 范数优化通过迭代加权最小二乘 (IRLS) 实现稀疏性，有效抑制异常三角形的贡献；(2) 交替优化循环逐步剔除异常值，而非单次优化。

![[assets/figures/papers/paper_list_l73_https_openreview_net_forum_id_jjEnTBsffi/figures/006_Figure_4.jpg]]
*Figure 4: Reconstruction of a synthetic shape at various noise. Top row: Screened PSR; Middle row: SALD; Bottom row: Ours. Each column corresponds to a different number of outliers*

### 消融实验

Figure 5 的消融实验系统性地验证了三个核心组件的必要性：

- **去除谱初始化 (Figure 5c)**：不使用谱方法估计初始三角形方向，导致重建拓扑退化，无法形成单连通表面。这证明了通过最小化谐波分量 γ（即求解 $A^T A$ 的最小特征向量）进行方向初始化的关键作用。
- **去除鲁棒优化 (Figure 5d)**：将 L0 范数替换为 L1 范数或线性规划后，重建表面受到伪影和多余手柄的影响，光滑性显著下降。这验证了 L0 范数在促进稀疏性和抗异常值方面的优势。
- **去除交替优化 (Figure 5e)**：仅执行单次核心模块，无法有效剔除所有异常三角形，导致重建质量下降。这表明迭代地应用核心模块与方向重定向是收敛到高质量单连通表面的必要条件。

### 失败模式与局限性

尽管本文方法在几何精度和拓扑保证方面表现优异，仍存在以下限制：

1. **拓扑灵活性不足**：当前方法强制 $H^1=0$（平凡第一上同调群），仅能保证单连通重建，无法处理更高亏格的拓扑结构（如环面）。这限制了其在需要保留非平凡拓扑特征的应用中的适用性。
2. **计算可扩展性**：方法依赖于构建全局 3D Delaunay 三角剖分，对于数百万点的大规模点云可能面临计算瓶颈。虽然我们实现了高性能 GPU 求解器（融合共轭梯度法和几何多重网格预条件子为单个持久化 GPU 核函数），但三角剖分构建本身仍是性能瓶颈。
3. **初始化敏感性**：谱初始化阶段的方向估计在输入点云非常稀疏或高度非均匀时可能不准确，影响后续重建质量。这一问题在点云密度剧烈变化的区域尤为突出。
4. **局部最优问题**：交替优化可能陷入局部最优，且迭代次数需手动设定，缺乏自动收敛判据。

### 开放问题

- **任意亏格扩展**：如何选择性地保留部分谐波分量 γ，使框架能够处理任意亏格拓扑，同时保持可控的拓扑复杂度？
- **生成模型集成**：如何将该拓扑可控表征与生成模型结合，学习具有指定拓扑特征的 3D 形状先验分布？

![[assets/figures/papers/paper_list_l73_https_openreview_net_forum_id_jjEnTBsffi/figures/001_Figure_1.jpg]]
*Figure 1: Visual comparison of pulmonary vascular reconstruction. The top row displays the full rendered results, while the bottom row presents corresponding zoomed-in views. From left to right: (a) the input CT scan; (b) the reconstruction of Walker et al. (2025) with 6 connected components and numerous spurious handles; (c) our simply connected reconstruction; and (d) the simply connected ground truth*

![[assets/figures/papers/paper_list_l73_https_openreview_net_forum_id_jjEnTBsffi/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative comparisons between our approach and baseline approaches*

## 定位与知识库关联

### 1. 与现有工作的关系

本方法的核心思想源于 Feng et al.（2023）提出的缠绕数场（winding number field）表面重建框架。该框架将表面重建转化为在三维三角剖分上求解一个整数 3-链的边界问题，通过优化缠绕数场的跳变来逼近输入点云。本文在此基础上做出了三个关键推进：

**从二维到三维的拓扑控制推广。** Feng et al. 的原框架在二维曲线重建中利用 Hodge-Helmholtz 分解（HHD）约束拓扑，但未将其推广至三维。本文首次将这一机制完整迁移到三维曲面重建中：通过 HHD 从缠绕数场对应的离散 1-形式 $\omega$ 中提取谐波分量 $\gamma$，并在线性系统中强制 $\gamma = 0$，从而消除所有非边界 2-循环，保证输出曲面同胚于二维球面（单连通）。这是目前唯一能从代数上保证三维重建拓扑正确性的方法。

**鲁棒优化与交替策略。** Feng et al. 使用 L1 范数或线性规划进行表面校正，而本文改用 L0 范数优化（通过迭代加权最小二乘 IRLS 实现），显著提升了对异常值和噪声的鲁棒性。此外，本文引入交替优化循环——迭代地在当前重建基础上重新定向输入三角形并再次求解校正表面——使得单次优化无法剔除的顽固异常值在多次迭代中被逐步排除。

**初始化与网格构建改进。** 与直接使用 3D Delaunay 三角剖分不同，本文通过八叉树引导插入额外点来避免狭长四面体，提升了数值稳定性。同时，谱初始化方法通过最小化谐波分量 $\gamma = A\mathbf{x}$ 来估计三角形初始方向，替代了随机或启发式初始化，为后续优化提供了更可靠的起点。

### 2. 与基线方法的对比定位

| 方法 | 技术路线 | 拓扑保证 | 鲁棒性策略 | 适用场景 |
|------|---------|---------|-----------|---------|
| **Screened Poisson Surface Reconstruction** | 隐式曲面（泊松方程） | 无 | 筛选参数 | 一般点云，需法线 |
| **SALD** (Atzmon & Lipman, ICLR 2021) | 无符号学习导数 | 无 | 网络隐式正则化 | 无定向点云 |
| **OReX** (Sawdayee et al., CVPR 2023) | 神经场从截面重建 | 无 | 神经隐式先验 | 平面截面输入 |
| **CrossSDF** (Walker et al., CVPR 2025) | 神经隐式场 + 截面 | 无 | SDF 平滑先验 | 薄结构截面重建 |
| **本文方法** | 缠绕数场 + HHD 拓扑约束 | **单连通保证** | L0 范数 + 交替优化 | 无定向点云，需拓扑可靠性 |

**与 CrossSDF 的对比。** CrossSDF 是当前薄结构重建的最先进方法，但其输出常包含多个连通分量和虚假手柄。在 Alveolis aligned 数据集上，本文方法连通分量数 CC=1（理想单连通），而 CrossSDF 产生多个连通分量；同时 Chamfer 距离降低 15.8%，Hausdorff 距离降低 9.62%（Table 1）。这表明拓扑约束不仅没有损害几何精度，反而通过排除虚假结构提升了整体质量。

**与隐式方法的对比。** Screened Poisson 和 SALD 等隐式方法依赖法线信息或网络先验，在噪声和异常值下容易产生孔洞或虚假连接。Figure 4 的合成数据实验显示，本文方法在不同噪声水平下均能保持完整且无洞的重建，而基线方法在异常值增多时出现明显退化。

### 3. 适用边界

**输入要求。** 方法适用于无组织、无定向的三维点云，不需要法线信息。输入点云应来自一个近似单连通的物体表面（如医学器官、血管、封闭物体），且点密度不宜过于稀疏或高度非均匀，否则初始化阶段的方向估计可能不准确。

**拓扑限制。** 当前方法仅能保证输出单连通曲面（同胚于二维球面），无法处理更高亏格的拓扑结构（如环面、多孔物体）。这是方法最根本的适用边界——它牺牲了拓扑灵活性以换取确定性保证。

**计算规模。** 方法依赖全局三维三角剖分和稀疏线性系统求解，对于包含数百万点的大规模点云可能面临计算瓶颈。虽然作者实现了 GPU 加速的共轭梯度-多重网格融合求解器，但八叉树引导的额外点插入和全局剖分本身仍具有超线性复杂度。

### 4. 局限性与开放问题

**已知局限：**

1. **亏格限制。** 方法强制谐波分量 $\gamma = 0$，等价于消除所有非平凡的第一上同调群 $H^1$ 元素，这直接排除了环面等亏格 $g \geq 1$ 的拓扑。对于需要保留特定拓扑特征的应用（如带孔机械零件），该方法不适用。

2. **初始化敏感性。** 谱初始化通过最小化 $\|A\mathbf{x}\|^2 / \|\mathbf{x}\|^2$ 来估计三角形方向，其最优解是 $A^\top A$ 的最小特征向量。当输入点云极度稀疏或采样严重不均匀时，该特征向量可能无法正确反映真实表面的内外方向，导致后续交替优化陷入局部最优。

3. **局部最优风险。** 交替优化虽然有效，但本质上是一个非凸迭代过程，迭代次数需手动设定，且不保证收敛到全局最优解。

4. **部件分割需求。** 在 Coronaries 数据集上，本文方法需要将点云预先分割为三个解剖部件分别处理，而基线方法可直接处理整体点云。这在一定程度上削弱了方法在该数据集上的可比性。

**开放问题：**

1. **选择性拓扑控制。** 如何扩展框架以支持任意亏格拓扑？一个自然的方向是选择性保留部分谐波分量 $\gamma$，而非强制其完全为零。这需要在 HHD 框架中引入拓扑先验或用户交互，以指定哪些手柄应被保留。

2. **与生成模型结合。** 该表征将拓扑约束编码为线性代数条件，具有可微性潜力。如何将其嵌入生成模型（如扩散模型或神经场），以学习具有可控拓扑的三维形状先验分布，是一个值得探索的方向。

3. **大规模扩展。** 如何通过自适应剖分或局部拓扑约束避免全局三角剖分的计算瓶颈，使方法适用于更大规模的真实扫描数据，仍需进一步研究。

## 原文 PDF

![[paperPDFs/ICLR_2026/Guaranteed_Simply_Connected_Mesh_Reconstruction_from_an_Unorganized_Point_Cloud_5f2be3ee1ede.pdf]]
