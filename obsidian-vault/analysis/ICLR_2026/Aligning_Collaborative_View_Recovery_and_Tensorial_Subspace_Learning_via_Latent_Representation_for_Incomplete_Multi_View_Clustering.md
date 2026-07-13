---
title: "Aligning Collaborative View Recovery and Tensorial Subspace Learning via Latent Representation for Incomplete Multi-View Clustering"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Aligning_Collaborative_View_Recovery_and_Tensorial_Subspace_Learning_via_Latent_Representation_for_Incomplete_Multi_View_Clustering.pdf
project_link: null
code_link: https://github.com/caoyu110/ARSL-IMVC
aliases:
- AI
- ACVRTSLLRIMV
- ARSL-IMVC
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "ARSL-IMVC用共享潜在表示同时驱动协作视图恢复和张量子空间学习。"
primary_logic: "潜在表示先重建缺失视图并保持视图多样性，再学习共享与视图特定子空间构建谱聚类亲和矩阵。"
claims:
- "共享潜在表示把视图恢复和子空间表示学习从顺序流程变为显式协作。"
- "HSIC正则化鼓励视图特定估计器捕获互补信息。"
- "低秩张量子空间约束提升不完整多视图聚类在BBCSport、HW等数据集上的表现。"
---

# Aligning Collaborative View Recovery and Tensorial Subspace Learning via Latent Representation for Incomplete Multi-View Clustering

> [!tip] 核心洞察
> 共享潜在表示不仅用于视图重建，还直接参与子空间学习，使得视图恢复和子空间表示学习在互补性和一致性探索上能够相互促进，从而提升聚类性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 通过潜在表示对齐协作视图恢复和张量子空间学习的不完整多视图聚类 |
| 英文题名 | Aligning Collaborative View Recovery and Tensorial Subspace Learning via Latent Representation for Incomplete Multi-View Clustering |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=a5aRjldX9l) · [GitHub](https://github.com/caoyu110/ARSL-IMVC) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | ARSL-IMVC |
| Dataset | BBCSport, HW |

> [!tip] 效果简介
> - BBCSport 上，ACC 为 96.51，对比 91.91，变化 +4.60。
> - BBCSport 上，NMI 为 89.77，对比 N/A，变化 N/A。
> - BBCSport 上，Purity 为 96.51，对比 N/A，变化 N/A。

## 概要

本文提出了一种名为 **ARSL-IMVC**（Aligning Collaborative View Recovery and Tensorial Subspace Learning via Latent Representation for Incomplete Multi-View Clustering）的新方法，用于解决不完整多视图聚类（Incomplete Multi-View Clustering, IMVC）问题。核心思想是通过引入一个共享的潜在表示 H 作为桥梁，将协作视图恢复（Collaborative View Recovery, CVR）和张量子空间学习（Tensorial Subspace Learning, TSL）统一到一个框架中，使得视图恢复和子空间表示学习能够相互促进，从而更充分地利用多视图间的互补性和一致性。实验结果表明，ARSL-IMVC 在多个基准数据集上显著优于现有方法。

多视图聚类（Multi-View Clustering, MVC）旨在利用来自不同视角或来源的数据进行无监督聚类。然而，在实际应用中，数据往往存在视图缺失问题，即某些样本在某些视图上不可用，这被称为不完整多视图聚类（IMVC）。

现有基于插补的 IMVC 方法通常将视图恢复和子空间表示学习作为两个独立或顺序执行的步骤，缺乏显式对齐和协作交互。具体来说，现有方法存在以下瓶颈：

- **视图恢复与子空间学习脱节**：视图恢复过程未考虑后续子空间学习的结构需求，而子空间学习也未利用恢复过程中的中间信息。
- **互补性与一致性探索不足**：无法同时充分利用多视图间的互补性（多样性）和一致性（共享结构）。

本文的核心动机是：**通过共享潜在表示 H 作为桥梁，将协作视图恢复和张量子空间学习显式对齐，使得两者在互补性和一致性探索上能够相互促进，从而提升聚类性能。**

## 核心方法与创新机理

ARSL-IMVC 的核心创新体现在以下三个关键设计变更：

| 变更维度 | 现有方法（Baseline） | 本文方法（Proposed） | 证据来源 |
|---------|-------------------|-------------------|---------|
| 视图恢复与子空间学习的交互方式 | 弱耦合或顺序执行，缺乏显式对齐 | 通过共享潜在表示 H 实现显式对齐和协作交互 | "leveraging the latent representation as a bridge in a unified framework, the ARSL-IMVC seamlessly aligns the complementarity and consistency exploration across view recovery and subspace representation learning" |
| 视图恢复中的多样性建模 | 通常仅考虑一致性或简单正则化 | 引入 HSIC 正则化项，显式鼓励视图特定估计器之间的多样性 | "HSIC(E_1^v, E_1^w) = Tr(K_v \tilde{H} K_w \tilde{H}) / (n-1)^2" |
| 子空间表示的结构建模 | 通常仅考虑视图共享或视图特定表示之一 | 同时学习视图共享子空间 Z 和视图特定子空间 Z^v，并堆叠成低秩张量以捕获高阶相关性 | "Z = Φ(Z^1, Z^2, ..., Z^V, Z)" |

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_a5aRjldX9l_Alignin/figures/001_Figure_1.jpg]]
*Figure 1: The overall framework of proposed ARSL-IMVC method, which mainly consists of CVR and TSL modules and aligns them in cross-view consistency and complementarity exploration by a latent representation.*

ARSL-IMVC 的整体框架如 Figure 1 所示，主要由两个核心模块组成：

**Figure 1: The overall framework of proposed ARSL-IMVC method, which mainly consists of CVR and TSL modules and aligns them in cross-view consistency and complementarity exploration by a latent representation.**

1. **协作视图恢复（CVR）模块**：从共享潜在表示 H 和视图特定估计器 E_1^v 重建完整视图，并通过 HSIC 正则化保持视图间的多样性。
2. **张量子空间学习（TSL）模块**：对潜在表示和恢复视图施加自表示约束，学习共享子空间 Z 和视图特定子空间 Z^v，并堆叠成低秩张量以捕获高阶相关性。

两个模块通过共享潜在表示 H 实现对齐和协作交互。

### 5.1 协作视图恢复（CVR）

CVR 模块的核心假设是：每个不完整视图 X^v 可以通过一个共享的潜在表示 H 和一个视图特定的估计器 E_1^v 来重建：

**视图重建公式** (Eq.1):
\[
P^v H + E_1^v
\]

其中 P^v 是投影矩阵，H 是共享潜在表示，E_1^v 是视图特定估计器。

为了鼓励视图特定估计器之间的多样性（从而捕获互补信息），引入 HSIC（Hilbert-Schmidt Independence Criterion）正则化：

**HSIC 经验估计** (Eq.2):
\[
\mathrm{HSIC}(E_1^v, E_1^w) = \mathrm{Tr}(K_v \tilde{H} K_w \tilde{H}) / (n-1)^2
\]

其中 K_v, K_w 为核矩阵，H̃ 为中心化矩阵。

CVR 的优化目标为 (Eq.3)：
\[
\min_{H,P^v,E_1^v} \sum_{w=1; w\neq v}^V \mathrm{HSIC}(E_1^v, E_1^w) \quad \mathrm{s.t.} \ X^v W^v = (P^v H + E_1^v) W^v, \ (P^v)^T P^v = I
\]

### 5.2 张量子空间学习（TSL）

TSL 模块对共享潜在表示 H 和恢复视图施加自表示约束：

**自表示约束** (Eq.4):
\[
H = H Z + E_H, \quad P^v H + E_1^v = (P^v H + E_1^v) Z^v + E_2^v
\]

其中 Z 为共享子空间，Z^v 为视图特定子空间，E_H, E_2^v 为噪声项。

然后将所有子空间表示堆叠成张量并施加低秩约束：

**TSL 优化目标** (Eq.5):
\[
\min \|\mathcal{Z}\|_{\mathfrak{P}} + \lambda_1 (\|E_H\|_{2,1} + \sum_{v=1}^V \|E_2^v\|_{2,1}) \quad \mathrm{s.t.} \ H = H Z + E_H, \ P^v H + E_1^v = (P^v H + E_1^v) Z^v + E_2^v, \ \mathcal{Z} = \Phi(Z^1, Z^2, \cdots, Z^V, Z)
\]

### 5.3 统一目标函数

将 CVR 和 TSL 统一到单一框架中：

**ARSL-IMVC 最终目标** (Eq.6):
\[
\min_{\Upsilon} \|\mathcal{Z}\|_{\mathfrak{S}} + \lambda_1 (\|E_H\|_{2,1} + \sum_{v=1}^V \|E_2^v\|_{2,1}) + \lambda_2 \sum_{w=1; w\neq v}^V \mathrm{HSIC}(E_1^v, E_1^w) \quad \mathrm{s.t.} \ X^v W^v = (P^v H + E_1^v) W^v, \ P^v H + E_1^v = (P^v H + E_1^v) Z^v + E_2^v, \ H = H Z + E_H, \ (P^v)^T P^v = I, \ \mathcal{Z} = \Phi(Z^1, Z^2, \cdots, Z^V, Z)
\]

### 5.4 ADMM 优化

采用交替方向乘子法（ADMM）进行优化，引入辅助变量和拉格朗日乘子：

**增广拉格朗日函数** (Eq.7):
\[
\mathcal{L}(\Upsilon, X_c^v, \mathcal{I}; Y_1^v, Y_2^v, Y_3^v, Y_4, \mathcal{V}, \mu) = \|\mathcal{I}\|_{\Theta} + \lambda_1 (\|E_H\|_{2,1} + \sum_{v=1}^V \|E_2^v\|_{2,1}) + \lambda_2 \sum_{w=1; v\neq w}^V \mathrm{HSIC}(E_1^v, E_1^w) + \sum_{v=1}^V \phi(Y_1^v, X_c^v - P^v H - E_1^v) + \sum_{v=1}^V \phi(Y_2^v, X^v W^v - X_c^v W^v) + \sum_{v=1}^V \phi(Y_3^v, X_c^v - X_c^v Z^v - E_2^v) + \phi(Y_4, H - H Z - E_H) + \phi(\mathcal{V}, \mathcal{Z} - \mathcal{I})
\]

关键更新步骤包括：
- **P^v 更新**：通过 SVD 求解
- **H 更新**：求解 Sylvester 方程
- **E_1^v 更新**：涉及 HSIC 项的闭式解
- **E_2^v 更新**：通过 ℓ2,1 阈值算子逐列更新 (Eq.20):
  \[
  E_2^v(:,j) = \left(1 - \frac{\lambda_1}{\mu \|L^v(:,j)\|_2}\right)^+ L^v(:,j)
  \]

### 5.5 亲和矩阵构建

优化完成后，从共享子空间 Z 和视图特定子空间 Z^v 构建用于谱聚类的亲和矩阵：

**亲和矩阵 S 构建**:
\[
\mathbf{S} = ( |\mathbf{Z}| + |\mathbf{Z}^T| + \sum_{v=1}^V |Z^v| + \sum_{v=1}^V |(Z^v)^T| ) / (V+1)
\]

## 实验与关键发现

### 6.1 主要实验结果

**Table 2: Clustering results of all methods on the BBCSport, HW, and BDGP datasets.**

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_a5aRjldX9l_Alignin/figures/003_Table_2.jpg]]
*Table 2: Clustering results of all methods on the BBCSport, HW, and BDGP datasets.*

在缺失率 0.1 时，ARSL-IMVC 在三个数据集上均取得最佳结果：

| 数据集 | 指标 | ARSL-IMVC | 次优方法 | 提升幅度 |
|-------|------|-----------|---------|---------|
| BBCSport | ACC | 96.51 | 91.91 | +4.60% |
| BBCSport | NMI | 89.77 | - | - |
| BBCSport | Purity | 96.51 | - | - |
| HW | ACC | 96.90 | 88.59 | +8.31% |
| HW | NMI | 92.77 | - | - |
| HW | Purity | 96.90 | - | - |
| BDGP | ACC | 56.07 | 50.66 | +5.41% |
| BDGP | NMI | 35.22 | - | - |
| BDGP | Purity | 56.07 | - | - |

**Table 4: Clustering results of some methods on HDigit datasets with the missing rate of 0.1.**

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_a5aRjldX9l_Alignin/figures/010_Table_4.jpg]]
*Table 4: Clustering results of some methods on HDigit datasets with the missing rate of 0.1.*

在大规模数据集 HDigit 上，ARSL-IMVC 同样表现优异：

| 指标 | ARSL-IMVC | 次优方法 (HCLS-IMSC) | 提升幅度 |
|------|-----------|---------------------|---------|
| ACC | 99.00 | 98.30 | +0.70% |
| NMI | 96.97 | 95.27 | +1.70% |
| Purity | 99.00 | - | - |

### 6.2 消融实验

**Table 3: The experimental results of ARSL-IMVC and its ablation variant with the 0.1 missing ratio.**

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_a5aRjldX9l_Alignin/figures/005_Table_3.jpg]]
*Table 3: The experimental results of ARSL-IMVC and its ablation variant with the 0.1 missing ratio.*

消融实验比较了 ARSL-IMVC 与去掉对齐机制的变体 ARSL-IMVC-1：

| 数据集 | ARSL-IMVC (ACC) | ARSL-IMVC-1 (ACC) | 提升幅度 |
|-------|----------------|-------------------|---------|
| BBCSport | 96.51 | 84.03 | +12.48% |
| HW | 96.90 | 70.15 | +26.75% |
| Yale | 86.06 | 76.55 | +9.51% |
| NGs | 96.20 | 89.96 | +6.24% |
| 100leaves | 89.24 | 78.61 | +10.63% |

这些结果充分证明了共享潜在表示对齐机制的有效性。

### 6.3 稳定性分析

**Figure 2: Clustering results on Yale, NGs, 100leaves and Scene-15 with different missing rates.**

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_a5aRjldX9l_Alignin/figures/004_Figure_2.jpg]]
*Figure 2: + BSV+ConCact +DAIMC→UEAF IMSC-AGL *HCLS-CGL +HCP-IMSC→BWIC-TIMCRMoGLOurS Figure 2: Clustering results on Yale, NGs, 100leaves and Scene-15 with different missing rates.*

ARSL-IMVC 在缺失率增加时，性能下降幅度小于其他方法，表现出更高的稳定性。

### 6.4 收敛性分析

**Figure 5: The convergence curves on Yale, BBCSport and NGs datasets with the missing rate of 0.1.**

优化算法能够在有限迭代次数内达到局部最小值，具有良好的收敛性。

### 6.5 实验公平性说明

- 所有实验均在相同缺失率设置下进行，缺失模式为随机缺失。
- 比较方法均使用作者提供的原始代码或公开实现，并采用推荐参数设置。
- ARSL-IMVC 在多个数据集和不同缺失率下均取得最佳或次优结果，表明其泛化能力。

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_a5aRjldX9l_Alignin/figures/002_Table_1.jpg]]
*Table 1: Main notations and descriptions in this study.*

## 定位与知识库关联

ARSL-IMVC 属于**基于插补的不完整多视图聚类**方法谱系，其核心贡献在于通过共享潜在表示实现了视图恢复和子空间学习的显式对齐与协作交互。

与现有方法的关键区别：
- **DAIMC**：基于对齐的插补-free 方法，未考虑视图恢复与子空间学习的交互。
- **UEAF**：基于统一嵌入对齐的插补-based 方法，但未显式建模多样性。
- **BWIC-TIMC**：基于张量学习的 IMVC 方法，但未将视图恢复纳入统一框架。
- **HCP-IMSC**：基于高阶相关性的方法，但未考虑视图特定子空间。

ARSL-IMVC 的创新在于同时解决了三个关键问题：
1. **视图恢复与子空间学习的对齐**：通过共享潜在表示 H 实现。
2. **视图间多样性的显式建模**：通过 HSIC 正则化实现。
3. **共享与特定子空间的高阶相关性捕获**：通过张量低秩约束实现。

**局限性**：
- 论文未明确讨论 ARSL-IMVC 在极高缺失率（如 >0.8）下的性能表现。
- 优化过程涉及多个超参数（λ1, λ2, μ, ρ），其选择可能对结果敏感。
- 方法基于线性重建假设，可能无法有效处理高度非线性的多视图数据。
- 计算复杂度未进行理论分析。

**开放问题**：
- ARSL-IMVC 是否可以扩展到深度网络框架以处理更复杂的数据？
- HSIC 正则化项的计算复杂度较高，是否存在更高效的多样性正则化方法？
- 如何自动确定潜在表示 H 的维度 k？
- 方法在非随机缺失模式下的表现如何？

## 原文 PDF

![[paperPDFs/ICLR_2026/Aligning_Collaborative_View_Recovery_and_Tensorial_Subspace_Learning_via_Latent_Representation_for_Incomplete_Multi_View_Clustering.pdf]]
