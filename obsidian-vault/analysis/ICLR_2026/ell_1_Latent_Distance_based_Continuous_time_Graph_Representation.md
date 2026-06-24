---
title: "$\\ell_1$ Latent Distance based Continuous-time Graph Representation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ell_1_Latent_Distance_based_Continuous_time_Graph_Representation.pdf
aliases:
- 1C
- E1LDBCTGR
- "ℓ1LD-CTGR"
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "将潜在距离从平方ℓ2距离替换为ℓ1距离，从而获得一个真正的度量空间，并使风险函数的积分成为闭式分段指数积分。"
primary_logic: "ℓ1距离满足三角不等式，可作为有效的潜在度量；其对应的风险函数积分具有闭式分段指数形式，适合超低维嵌入；通过使用次梯度（下降方向）替代梯度，可以处理ℓ1范数的不可微性。"
claims:
- "平方ℓ2距离违反三角不等式，不是有效的潜在度量。"
- "ℓ1距离风险函数的积分是闭式分段指数积分。"
- "ℓ1LD-CTGR在网络补全（out-of-sample）任务中，在大多数数据集上优于其他方法。"
- "ℓ1LD-CTGR在未来连接预测（across-sample）任务中，在大多数情况下优于其他竞争者。"
---

# $\ell_1$ Latent Distance based Continuous-time Graph Representation

> [!tip] 核心洞察
> ℓ1距离满足三角不等式，可作为有效的潜在度量；其对应的风险函数积分具有闭式分段指数形式，适合超低维嵌入；通过使用次梯度（下降方向）替代梯度，可以处理ℓ1范数的不可微性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于ℓ1潜在距离的连续时间图表示 |
| 英文题名 | $\ell_1$ Latent Distance based Continuous-time Graph Representation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=pW1Kg9CYyw) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | ℓ1LD-CTGR |
| Dataset | Synthetic-α, HyperText, Infectious |

> [!tip] 效果简介
> - Synthetic-α 上，ROC 为 0.793±0.038，对比 GRASSP: 0.577±0.028，变化 +0.216。
> - Synthetic-α 上，PR 为 0.708±0.039，对比 GRASSP: 0.509±0.029，变化 +0.199。
> - HyperText 上，ROC 为 0.694±0.011，对比 GRASSP: 0.607±0.006，变化 +0.087。

## 概述

连续时间图表示学习旨在将节点嵌入随时间演化的潜在空间，并通过点过程建模边的生成。现有工作（如GRASSP）使用平方ℓ2距离作为潜在度量，但该度量违反三角不等式，导致其在社交、接触和协作网络上的性能下降。此外，平方ℓ2距离对应的风险函数积分虽为闭式高斯积分，但ℓ2距离（无平方）的积分无闭式解，需数值近似，带来高计算复杂度和近似误差。

本文提出基于ℓ1潜在距离的连续时间图表示方法（ℓ1LD-CTGR），核心创新在于将潜在距离从平方ℓ2距离替换为ℓ1距离。这一替换带来三重优势：ℓ1距离满足三角不等式，构成有效的潜在度量空间；其风险函数的积分具有闭式分段指数形式，避免了数值近似；通过使用次梯度（下降方向）替代梯度，可处理ℓ1范数的不可微性。方法采用分段线性轨迹建模节点运动，并针对D=2的超低维嵌入实现了张量并行化积分计算。

实验在多个真实和合成数据集上进行，包括网络补全（out-of-sample）、未来连接预测（across-sample）和网络重构（in-sample）三个任务。主要结果表明：在网络补全任务中，ℓ1LD-CTGR在除两种情形外的所有数据集上优于其他方法；在未来连接预测任务中，在大多数情况下优于其他竞争者；在重构任务中，在Synthetic-α、HyperText和Reddit等数据集上表现突出。消融实验显示方法对bin数量和嵌入维度的微小变化具有鲁棒性，且运行时间与GRASSP处于同一量级。

## 背景与动机

连续时间图表示学习旨在将动态图中节点间的时序交互编码到低维潜在空间中。现有方法GRASSP采用平方ℓ2距离（squared ℓ2 distance）定义节点间风险函数，并利用高斯积分获得似然的闭式解。然而，平方ℓ2距离不满足三角不等式，因此不是一个有效的度量（valid metric）。这一缺陷导致潜在空间中节点相对位置失真，在社交、接触和协作网络等实际场景中显著损害表示质量。此外，若直接使用ℓ2距离（无平方）以维持度量性质，其风险函数的积分不存在闭式解，必须依赖数值近似，这既增加计算开销又引入近似误差。现有连续时间图嵌入方法（如CTDNE、HTNE、PIVEM）以及静态/时序基线（Node2Vec、TCL、GraphMixer、DyGFormer）均未从根本上解决潜在距离的度量有效性问题。

本文的动机在于：**能否在保持闭式可积性的前提下，用真正满足三角不等式的距离替代平方ℓ2距离，从而构建一个理论上更合理的潜在度量空间？** 核心洞察是：ℓ1距离（Manhattan距离）天然满足三角不等式，且其风险函数积分具有闭式分段指数形式（Theorem 1），避免了数值近似的需求。基于此，本文提出ℓ1LD-CTGR（ℓ1 Latent Distance based Continuous-Time Graph Representation），将潜在距离从平方ℓ2距离替换为ℓ1距离，并引入次梯度（下降方向）处理ℓ1范数的不可微性。这一替换的因果机制是：通过使用有效度量，节点在潜在空间中的相对位置不再受三角不等式违反带来的系统性偏差，从而更忠实地反映真实交互模式；同时，闭式分段指数积分使得超低维嵌入（D=2）下的计算可张量化并行（Theorem 2），保持与GRASSP相同的实际运行时间量级。

## 核心创新

ℓ1LD-CTGR 的核心创新在于用一个单一但根本性的因果旋钮——将潜在距离度量从平方ℓ2距离替换为ℓ1距离——同时解决了 GRASSP 基线中两个耦合的瓶颈：度量空间的合法性和计算的可处理性。

**瓶颈与因果旋钮。** GRASSP 使用的平方ℓ2距离（$\|\mathbf{r}_i(t) - \mathbf{r}_j(t)\|_2^2$）违反了三角不等式（原文 Eq. 8），因此不是一个有效的潜在度量。这导致潜在空间中节点相对位置失真，在社交、接触和协作网络上性能下降。同时，平方ℓ2距离（无平方）的风险函数积分虽为闭式高斯积分，但ℓ2距离（无平方）的积分无闭式解，需要数值近似（H=1000 个样本点），带来高计算复杂度和近似误差。ℓ1LD-CTGR 将距离度量替换为ℓ1距离（$\|\mathbf{r}_i(t) - \mathbf{r}_j(t)\|_1$），该度量满足三角不等式，是有效的潜在度量空间距离。这一替换使风险函数积分从需要数值近似的非闭式形式变为闭式分段指数积分（Theorem 1），同时通过使用次梯度（下降方向）替代梯度（Theorem 3）处理了ℓ1范数的不可微性。

**三个 changed slots 及其证据强度。**

1.  **潜在距离度量**：从平方ℓ2距离（$\|\cdot\|_2^2$）变为ℓ1距离（$\|\cdot\|_1$）。证据 anchor 为风险函数定义式 `λ_ij(s,t) := exp(β(s) + s ||r_i(t) - r_j(t)||_1)`。证据强度 1.0。

2.  **风险函数积分形式**：从高斯积分（闭式，基于误差函数）变为闭式分段指数积分。Theorem 1 明确指出该积分是闭式分段指数形式。证据强度 1.0。

3.  **梯度/优化方法**：从标准梯度下降（平方ℓ2距离可微）变为使用下降方向（次梯度）。原文明确说明 `we find a descent direction to replace the gradient`。证据强度 1.0。

**核心洞察与机制。** ℓ1距离满足三角不等式，可作为有效的潜在度量；其对应的风险函数积分具有闭式分段指数形式，适合超低维嵌入（D=2）；通过使用次梯度替代梯度，可以处理ℓ1范数的不可微性。这三个 changed slots 共同构成了一个自洽的解决方案：替换度量解决了度量空间合法性问题，闭式积分解决了计算效率问题，次梯度优化解决了优化可行性问题。

**实验证据强度。** 在主要结果中，ℓ1LD-CTGR 在网络补全（out-of-sample）任务中，在除两个情况外的所有情况下优于其他方法（Table 1，置信度 0.95）；在未来连接预测（across-sample）任务中，在大多数情况下优于其他竞争者（Table 2，置信度 0.95）。具体性能提升包括：在 Synthetic-α 数据集上，ROC 从 0.577±0.028（GRASSP）提升至 0.793±0.038，提升 +0.216（Table A5，置信度 0.9）；在 Infectious 数据集上，ROC 从 0.738±0.018 提升至 0.861±0.021，提升 +0.123（Table A5，置信度 0.9）。消融实验表明，ℓ1LD-CTGR 对 bin 数量和嵌入维度的微小变化具有鲁棒性（置信度 0.95），且与 GRASSP 具有相同的实际运行时间量级（置信度 1.0）。

**需要手动验证的点。** 论文未明确讨论方法的局限性，实验仅在超低维嵌入（D=2）下进行，更高维度的性能未充分验证。此外，仅使用 AUC-ROC 和 AUC-PR 作为评估指标，缺乏其他指标（如 NDCG、MAP）的对比。这些点需要手动验证。

## 整体框架

ℓ1LD-CTGR的整体pipeline延续了连续时间图表示（CTGR）的通用范式，其核心是将潜在空间中节点之间的**距离度量**从平方ℓ2距离替换为ℓ1距离，从而在保持计算效率的同时解决了平方ℓ2距离违反三角不等式导致的潜在空间几何失真问题。

**输入与输出流：** 输入为连续时间图 $\mathcal{G}$，包含节点集 $\mathcal{V}$ 和带时间戳的边事件 $\mathcal{E}_{ij}$（节点 $i$ 和 $j$ 之间在时间 $e_k$ 发生的交互）。输出为每个节点 $i$ 随时间演化的潜在轨迹 $\mathbf{r}_i(t) \in \mathbb{R}^\mathcal{D}$，以及一个可学习的基线强度参数 $\beta(s)$。

**核心模块与数据流：**

1.  **节点轨迹建模（分段线性近似）：** 将时间轴划分为 $B$ 个等长的bins（每个bin长度 $\Delta_B$），每个节点 $i$ 的轨迹由初始位置 $\mathbf{x}_i^{(0)}$ 和每个bin内的速度向量 $\boldsymbol{\sigma}_i^{(b)}$ 参数化。轨迹 $\mathbf{r}_i(t)$ 由公式 $\mathbf{r}_i(t) = \mathbf{x}_i^{(0)} + \Delta_B \sum_{b=1}^{\lfloor t/\Delta_B \rfloor} \boldsymbol{\sigma}_i^{(b)} + \mathrm{mod}(t, \Delta_B) \boldsymbol{\sigma}_i^{(\lfloor t/\Delta_B \rfloor+1)}$ 给出。该模块为整个框架提供了连续时间上的节点位置表示。

2.  **ℓ1距离风险函数定义：** 对于节点对 $(i,j)$，在源节点 $s$ 和时间 $t$ 条件下的风险函数定义为 $\lambda_{ij}(s,t) := \exp(\beta(s) + s \|\mathbf{r}_i(t) - \mathbf{r}_j(t)\|_1)$。这里 $s \in \{1, -1\}$ 表示边事件或非边事件。与GRASSP中使用平方ℓ2距离不同，ℓ1距离满足三角不等式，是一个有效的潜在度量空间。

3.  **闭式积分计算（Theorem 1）：** 计算对数似然函数中的关键项 $\int_{e_l}^{e_u} \lambda_{ij}(s,t) \mathrm{d}t$。由于节点轨迹是分段线性的，节点对之间的ℓ1距离 $\|\mathbf{r}_i(t) - \mathbf{r}_j(t)\|_1$ 在每个bin内是多个绝对值线性函数的和。该积分可以分解为基于“零点”排序的分段指数积分，具有闭式解（Theorem 1公式）。这避免了平方ℓ2距离无平方版本（ℓ2 Distance baseline）需要数值近似的缺点。

4.  **张量并行积分（Theorem 2）：** 针对超低维嵌入（$\mathcal{D}=2$）这一实际设置，进一步将积分计算张量化。Theorem 2指出，对于所有节点对 $(i,j)$ 和所有bins $k$，积分 $[\int_{e_k}^{e_{k+1}} \lambda_{ij}(s,t) \mathrm{d}t]_{i,j,k}$ 可以表示为 $\exp(\beta(s)) \odot (\mathcal{Z}_1 + \mathcal{Z}_2 + \mathcal{Z}_3)$ 的形式，其中 $\mathcal{Z}_1, \mathcal{Z}_2, \mathcal{Z}_3$ 是基于节点位置和速度参数构造的张量。该模块使得积分计算可以高效地在GPU上进行并行化。

5.  **次梯度优化（Theorem 3）：** 由于ℓ1范数在零点处不可微，标准梯度下降无法直接应用。Theorem 3提供了一个下降方向（次梯度）来替代梯度。具体地，对于风险函数关于节点位置 $\mathbf{r}_i$ 的导数，使用 $\partial \lambda_{ij}(\mathbf{r}_i) := \exp(\beta(s) + s \|\mathbf{r}_i(t) - \mathbf{r}_j(t)\|_1) \cdot s \cdot \mathrm{sign}(\mathbf{r}_i(t) - \mathbf{r}_j(t))$ 作为上升方向。这使得主流的学习架构（如Adam优化器）能够处理ℓ1范数的不可微性，并学习图参数。

**模块间关系：** 轨迹建模模块为风险函数模块提供 $\mathbf{r}_i(t)$；风险函数模块的输出 $\lambda_{ij}(s,t)$ 进入积分计算模块；积分计算模块的输出（闭式积分或张量并行积分）直接用于计算对数似然；对数似然的梯度通过次梯度优化模块反向传播，更新轨迹参数和基线强度 $\beta(s)$。整个pipeline是一个端到端的可微系统。

## 核心模块与公式推导

本文的核心贡献在于将连续时间图表示（CTGR）框架中的潜在距离从平方ℓ2距离替换为ℓ1距离，从而在理论上解决了平方ℓ2距离违反三角不等式、不是有效潜在度量的问题。这一替换带来了三个关键模块的连锁变化：风险函数定义、积分计算闭式形式、以及优化方法。

### 1. 问题背景：平方ℓ2距离的缺陷

在GRASSP框架中，节点对(i,j)在时间t的风险函数（hazard function）定义为：
$$\lambda_{ij}(s,t) := \exp(\beta(s) + s \|\mathbf{r}_i(t) - \mathbf{r}_j(t)\|_2^2)$$

其中$\mathbf{r}_i(t)$是节点i在时间t的潜在位置向量，$\beta(s)$是基强度函数，参数$s \in \{-1, 1\}$控制事件类型（边出现或消失）。平方ℓ2距离$\|\cdot\|_2^2$违反三角不等式，因此不是有效的度量空间距离——这意味着潜在空间中节点之间的相对位置关系可能失真，尤其是在社交、接触和协作网络等具有非欧几何特性的数据上。

对于平方ℓ2距离，风险函数的积分具有闭式高斯积分形式：
$$\int_{e_l}^{e_u} \exp(\beta(s) + s \|\mathbf{r}_i(t) - \mathbf{r}_j(t)\|_2^2) \mathrm{d}t = \frac{\sqrt{\pi}}{2\|\Delta\mathbf{v}_{ij}\|_2} \exp(\beta(s) + s\|\Delta\mathbf{x}_{ij}\|_2^2 - s\rho_{ij}^2) \cdot E_{ij}(s, \tau(e_l), \tau(e_u))$$

其中$\Delta\mathbf{x}_{ij}$和$\Delta\mathbf{v}_{ij}$分别表示节点轨迹分段线性近似中的位置差和速度差，$\rho_{ij}$和$E_{ij}$是误差函数相关项。虽然这是闭式解，但高斯误差函数的计算仍然带来一定的复杂度。

### 2. 核心模块一：ℓ1距离风险函数

本文提出的ℓ1距离风险函数定义为：
$$\lambda_{ij}(s,t) := \exp(\beta(s) + s \|\mathbf{r}_i(t) - \mathbf{r}_j(t)\|_1)$$

其中$\|\cdot\|_1$是ℓ1范数（曼哈顿距离），满足三角不等式，因此是有效的潜在度量。节点轨迹采用与GRASSP相同的分段线性模型：
$$\mathbf{r}_i(t) = \mathbf{x}_i^{(0)} + \Delta_B \sum_{b=1}^{\lfloor t/\Delta_B \rfloor} \boldsymbol{\sigma}_i^{(b)} + \mathrm{mod}(t, \Delta_B) \boldsymbol{\sigma}_i^{(\lfloor t/\Delta_B \rfloor+1)}$$

其中$\Delta_B$是时间bin的宽度，$\boldsymbol{\sigma}_i^{(b)}$是节点i在第b个bin内的速度向量。该模型将连续时间运动离散化为B个线性段。

### 3. 核心模块二：闭式分段指数积分（Theorem 1）

ℓ1距离风险函数的积分具有闭式分段指数形式，这是本文的核心理论贡献。对于时间区间$[e_l, e_u]$，积分可写为：
$$\int_{e_l}^{e_u} \lambda_{ij}(s,t) \mathrm{d}t = \exp(\beta(s)) \int_0^{e_u-e_l} \exp\left(s \sum_{d=1}^{\mathcal{D}} |\Delta x_{ij,d} + \Delta v_{ij,d} t|\right) \mathrm{d}t$$

其中$\Delta x_{ij,d}$和$\Delta v_{ij,d}$分别是第d维的位置差和速度差。关键在于，每个绝对值函数$|\Delta x_{ij,d} + \Delta v_{ij,d} t|$的零点将时间区间分割成若干子区间，在每个子区间内所有绝对值函数都是线性的（符号不变）。因此，被积函数在每个子区间内是指数函数，积分具有闭式形式。

**Theorem 1** 的完整形式为：
$$\int_{e_l}^{e_u} \lambda_{ij}(s,t) \mathrm{d}t = \begin{cases} \exp(\beta(s)) \mathcal{T}_{ij,0,e_u-e_l} & \text{if } z_{ij,(\underline{c})} > e_u-e_l \text{ or } z_{ij,(\overline{c})} < 0; \\ \exp(\beta(s)) (\mathcal{T}_{ij,0,(\underline{c})} + \sum_{c=\underline{c}}^{\overline{c}-1} \mathcal{T}_{ij,(c),(c+1)} + \mathcal{T}_{ij,(\overline{c}),e_u-e_l}) & \text{else} \end{cases}$$

其中$z_{ij,(c)}$是排序后的零点位置，$\underline{c}$和$\overline{c}$分别是落在区间$[0, e_u-e_l]$内的最小和最大零点索引，$\mathcal{T}_{ij,(c),(c+1)}$是子区间上的闭式积分值。当速度非零时，子区间积分为：
$$\mathcal{T}_{ij,(c),(c+1)} = \frac{\exp(s X_{ij,(c)})}{s V_{ij,(c)}} \left(\exp(s V_{ij,(c)} z_{ij,(c+1)}) - \exp(s V_{ij,(c)} z_{ij,(c)})\right)$$

其中$X_{ij,(c)}$和$V_{ij,(c)}$是在该子区间内所有维度上合并后的线性系数（符号确定后，绝对值展开为线性函数）。当速度为零时，积分退化为简单的指数函数乘以区间长度。

**变量含义**：
- $\mathcal{D}$：潜在空间维度
- $\Delta x_{ij,d} = x_{i,d}^{(0)} - x_{j,d}^{(0)}$：节点i和j在第d维的初始位置差
- $\Delta v_{ij,d} = v_{i,d} - v_{j,d}$：节点i和j在第d维的速度差
- $z_{ij,(c)}$：第c个排序后的零点，即满足$\Delta x_{ij,d} + \Delta v_{ij,d} t = 0$的时间点
- $X_{ij,(c)}$和$V_{ij,(c)}$：在零点$z_{ij,(c)}$和$z_{ij,(c+1)}$之间的区间内，所有维度绝对值展开后的总常数项和总线性系数

### 4. 核心模块三：张量并行积分（Theorem 2）

针对超低维嵌入（$\mathcal{D}=2$），本文进一步提出了张量并行化的积分计算方法。当$\mathcal{D}=2$时，积分形式为：
$$\int_{e_k}^{e_{k+1}} \lambda_{ij}(s,t) \mathrm{d}t = \exp(\beta(s)) \int_0^{\Delta e_k} \exp(s(|\Delta x_{ij,1} + \Delta v_{ij,1} t| + |\Delta x_{ij,2} + \Delta v_{ij,2} t|)) \mathrm{d}t$$

其中$\Delta e_k = e_{k+1} - e_k$。Theorem 2表明，所有节点对(i,j)和所有时间bin k的积分可以表示为：
$$[\int_{e_k}^{e_{k+1}} \lambda_{ij}(s,t) \mathrm{d}t]_{i,j,k} = \exp(\beta(s)) \odot (\mathcal{Z}_1 + \mathcal{Z}_2 + \mathcal{Z}_3)$$

其中$\mathcal{Z}_1, \mathcal{Z}_2, \mathcal{Z}_3$是三个张量，分别对应零点划分后不同区域（两个绝对值函数符号组合的四种情况）的积分贡献，$\odot$表示逐元素乘法。这种方法避免了逐对逐区间的循环计算，使得在GPU上可以高效并行处理所有节点对。

### 5. 核心模块四：次梯度优化（Theorem 3）

ℓ1范数在零点处不可微，因此标准梯度下降无法直接应用。本文使用次梯度（subgradient）来定义下降方向。对于ℓ1距离风险函数，关于节点i位置$\mathbf{r}_i$的上升方向定义为：
$$\partial \lambda_{ij}(\mathbf{r}_i) := \exp(\beta(s) + s \|\mathbf{r}_i(t) - \mathbf{r}_j(t)\|_1) \cdot s \cdot \mathrm{sign}(\mathbf{r}_i(t) - \mathbf{r}_j(t))$$

其中$\mathrm{sign}(\cdot)$是逐元素的符号函数，在零点处取集合$[-1, 1]$中的任意值。Theorem 3进一步指出，当节点i和j在某维度上的坐标相等时（即$r_{i,d} = r_{j,d}$），该维度的次梯度方向需要特殊处理：令$C := \{d \in \mathcal{D}: r_{i,d} = r_{j,d}\}$为坐标相等的维度索引集，在这些维度上，下降方向的选择会影响收敛性，但任意选择符号函数值（如0或±1）仍然保证下降方向的有效性。

### 6. 整体对数似然与优化目标

综合上述模块，整个图$\mathcal{G}$在超参数$\Omega$下的对数似然为：
$$\log p(\mathcal{G} | \Omega) = \sum_{(i,j) \in \mathcal{V}^2} \sum_{k=1}^{|\mathcal{E}_{ij}|} \left( \log \lambda_{ij}(s_k, e_k) - \int_{e_{k-1}}^{e_k} \lambda_{ij}(s_k, \tau) \mathrm{d}\tau \right)$$

其中$\mathcal{V}$是节点集合，$\mathcal{E}_{ij}$是节点对(i,j)的事件序列（边出现或消失），$e_k$是第k个事件的时间戳，$s_k \in \{-1, 1\}$是事件类型。第一项$\log \lambda_{ij}(s_k, e_k)$使用ℓ1距离风险函数直接计算，第二项积分使用Theorem 1的闭式分段指数积分计算。优化时，使用Theorem 3的次梯度方向替代梯度，通过标准的随机梯度下降或Adam等优化器更新节点轨迹参数（初始位置和速度向量）。

### 7. 关键公式汇总

| 公式 | 表达式 | 含义 |
|------|--------|------|
| 平方ℓ2风险函数 | $\lambda_{ij}(s,t) = \exp(\beta(s) + s \|\mathbf{r}_i(t) - \mathbf{r}_j(t)\|_2^2)$ | GRASSP基线，违反三角不等式 |
| ℓ1风险函数 | $\lambda_{ij}(s,t) = \exp(\beta(s) + s \|\mathbf{r}_i(t) - \mathbf{r}_j(t)\|_1)$ | 本文提出，有效度量 |
| 分段线性轨迹 | $\mathbf{r}_i(t) = \mathbf{x}_i^{(0)} + \Delta_B \sum_{b=1}^{\lfloor t/\Delta_B \rfloor} \boldsymbol{\sigma}_i^{(b)} + \mathrm{mod}(t, \Delta_B) \boldsymbol{\sigma}_i^{(\lfloor t/\Delta_B \rfloor+1)}$ | 节点连续时间运动模型 |
| ℓ1积分（Theorem 1） | 分段指数闭式积分 | 见上节完整形式 |
| 张量并行积分（Theorem 2） | $[\int_{e_k}^{e_{k+1}} \lambda_{ij}(s,t) \mathrm{d}t]_{i,j,k} = \exp(\beta(s)) \odot (\mathcal{Z}_1 + \mathcal{Z}_2 + \mathcal{Z}_3)$ | $\mathcal{D}=2$时的并行化 |
| 次梯度方向（Theorem 3） | $\partial \lambda_{ij}(\mathbf{r}_i) = \exp(\beta(s) + s \|\mathbf{r}_i - \mathbf{r}_j\|_1) \cdot s \cdot \mathrm{sign}(\mathbf{r}_i - \mathbf{r}_j)$ | 处理ℓ1不可微性 |
| 对数似然 | $\log p(\mathcal{G} | \Omega) = \sum_{(i,j)} \sum_k (\log \lambda_{ij}(s_k, e_k) - \int_{e_{k-1}}^{e_k} \lambda_{ij}(s_k, \tau) \mathrm{d}\tau)$ | 整体优化目标 |

## 实验与分析

### 主要结果

ℓ1LD-CTGR 在三个任务（网络重构、网络补全、未来连接预测）上进行了评估，并与 GRASSP、ℓ2 Distance 版本以及六种静态/动态图基线方法进行了对比。实验覆盖了 Synthetic-α、HyperText、Infectious、Contact、Reddit、Facebook 和 NeurIPS 等多样化的数据集。

**网络补全（out-of-sample）**：如 Table 1 所示，ℓ1LD-CTGR 在所有数据集上几乎全面领先。在 Synthetic-α 上，ℓ1LD-CTGR 的 ROC 达到 0.793±0.038，而 GRASSP 仅为 0.577±0.028（提升 +0.216）；PR 也从 0.509±0.029 提升至 0.708±0.039。在 HyperText 上，ℓ1LD-CTGR 的 ROC 为 0.694±0.011，GRASSP 为 0.607±0.006；Infectious 上为 0.861±0.021 对比 0.738±0.018；Reddit 上为 0.801±0.009 对比 0.707±0.011。论文指出 ℓ1LD-CTGR 在所有测试情形中仅有两个数据集未取得最优结果，但整体优势显著。

![[assets/figures/papers/iclr26_0001_pW1Kg9CYyw_ell_1_Latent_Distance_based_Continuous-time_Grap/figures/001_Table_1.jpg]]
*Table 1: Performance of different methods for network completion (out-of-sample) across diverse data sets (mean±STD)*

**未来连接预测（across-sample）**：Table 2 的结果显示 ℓ1LD-CTGR 在大多数情况下优于所有竞争者，包括在具有挑战性的 Facebook 和 NeurIPS 真实数据集上。该任务要求模型基于历史数据预测未来未见的时间段内的连接，更能体现连续时间建模的优势。

![[assets/figures/papers/iclr26_0001_pW1Kg9CYyw_ell_1_Latent_Distance_based_Continuous-time_Grap/figures/002_Table_2.jpg]]
*Table 2: Performance of different methods for network prediction (across-sample) across diverse data sets (mean±STD)*

**网络重构（in-sample）**：Table A5 的结果表明 ℓ1LD-CTGR 在重构任务上也具有竞争力，特别是在 Synthetic-α、HyperText 和 Reddit 上表现突出。

### 消融与鲁棒性分析

**距离度量的消融**：论文直接对比了 ℓ1 距离、平方 ℓ2 距离（GRASSP）和普通 ℓ2 距离（无平方，需数值积分）三种变体。结果一致表明 ℓ1LD-CTGR 在大多数情况下取得最佳性能，而 ℓ2 Distance 版本（需数值近似积分）通常显著劣于 ℓ1LD-CTGR 和 GRASSP。这验证了 ℓ1 距离作为有效度量、且其闭式分段指数积分带来的计算优势。

**超参数鲁棒性**：Table A3 显示，在 Contact 数据集上改变 bin 数量（B=5, 10, 20, 50, 100）时，ℓ1LD-CTGR 的性能波动很小，表明模型对节点轨迹分段粒度的微小变化具有鲁棒性。Table A4 进一步考察了嵌入维度的影响：当维度从 2 增加到 4、8 时，ℓ1LD-CTGR 的性能保持稳定，而 GRASSP 和 ℓ2 Distance 版本在某些维度下出现退化。这表明 ℓ1 度量的优势不仅限于超低维（D=2）场景。

![[assets/figures/papers/iclr26_0001_pW1Kg9CYyw_ell_1_Latent_Distance_based_Continuous-time_Grap/figures/006_Table_5.jpg]]
*Table 5: Table A3: Performance of $\ell _ { 1 } \mathrm { L D }$ . -CTGR with respect to different bin numbers on Contact (mean of 10 repetitions)

![[assets/figures/papers/iclr26_0001_pW1Kg9CYyw_ell_1_Latent_Distance_based_Continuous-time_Grap/figures/007_Table_6.jpg]]
*Table 6: Table A4: Performance of ℓ1LD-CTGR, GRASSP, and the $\ell _ { 2 }$ distance version (H = 1000) with respect to different dimensionalities on Contact and Infectious (mean of 10 repetitions)*

**计算效率**：Table A1 和 Table A2 报告了运行时间。关键结论是：在超低维 D=2 下，ℓ1LD-CTGR 与 GRASSP 具有相同的实际运行时间量级（例如在 Contact 上分别为 0.024±0.002 秒/epoch 和 0.023±0.003 秒/epoch）。这反驳了 ℓ1 距离引入分段计算会导致显著开销的担忧。在高维（D=4, 8）下，ℓ1LD-CTGR 的运行时间增加，但仍在可接受范围内。

![[assets/figures/papers/iclr26_0001_pW1Kg9CYyw_ell_1_Latent_Distance_based_Continuous-time_Grap/figures/004_Table_3.jpg]]
*Table 3: Table A1: Average runtime (in seconds) per epoch of GRASSP, $\ell _ { 1 } \mathrm { L D - C T G R }$ . and the $\ell _ { 2 }$ distance version ( H = 1 0 0 0 ) with ultra-low-dimensionality $\mathcal { D }$ = 2 on different data sets ( $\mathrm { m e a n } \pm \mathrm { S T D }$ ) . The training criterion of GRASSP is followed, which is a three-stage 300-epoch procedure. Results are conducted on a device with an Intel(R) Xeon(R) Gold 6330 CPU, 1 TB RAM, and eight NVIDIA A100 GPUs. Both GRASSP and $\ell _ { 1 } \mathrm { L D - C T G R }$ have the same order of actual runtime

![[assets/figures/papers/iclr26_0001_pW1Kg9CYyw_ell_1_Latent_Distance_based_Continuous-time_Grap/figures/005_Table_4.jpg]]
*Table 4: Table A2: Average runtime (in seconds) per epoch of GRASSP and $\ell _ { 1 } \mathrm { L D }$ . -CTGR with higher dimensionalities on different data sets (mean ± STD)

### 失败模式与局限

论文未明确讨论方法的失败模式。从结果中可以推断出以下潜在局限：
- **超低维依赖**：张量并行积分（Theorem 2）专门针对 D=2 设计，这是实现高效计算的核心。虽然 Table A4 显示了维度扩展的可行性，但更高维度下的计算复杂度会显著增加，且论文未提供 D>2 时的并行化通用方案。
- **评估指标单一**：仅使用 AUC-ROC 和 AUC-PR，缺乏 NDCG、MAP 等排序指标或负对数似然等概率校准指标的对比，限制了对其生成质量的全面评估。
- **数据集规模有限**：实验数据集（如 Infectious、HyperText）规模较小，最大的是 Reddit（约 1 万节点、数万时间步）。在百万级节点或极长时间序列上的可扩展性尚未验证。
- **ℓ1 距离的边界行为**：当节点轨迹在某个维度上完全重合时（Theorem 3 中的集合 C），次梯度退化为集合 [-1,1] 中的任意值，可能导致优化不稳定性。论文虽提供了理论处理，但未在实验中专门分析这种退化情形的影响。

### 关键图表结论

- **Table 1 & Table 2**：核心证据，证明 ℓ1 距离替代平方 ℓ2 距离在连续时间图表示中的有效性，特别是在外推任务（补全和预测）上的显著提升。
- **Table A1**：消除计算效率疑虑，证明 ℓ1LD-CTGR 与 GRASSP 在运行时上等价。
- **Figure A1**：直观展示了 ℓ1 距离风险函数的分段指数形态，与 Theorem 1 的闭式积分公式对应。
- **Figure A2**：潜在空间可视化显示，ℓ1 距离产生的节点轨迹在几何上更合理，节点之间的相对位置关系更符合三角不等式约束。

## 方法谱系与知识库定位

### 与基线方法的谱系关系

ℓ1LD-CTGR 直接继承自 GRASSP 的连续时间图表示框架，其核心创新在于将潜在距离度量从平方 ℓ2 距离替换为 ℓ1 距离。这一替换并非简单的范数选择，而是针对一个已被证实的理论瓶颈：平方 ℓ2 距离违反三角不等式（见 Eq. 8），因此不是潜在度量空间中的有效距离。GRASSP 依赖的平方 ℓ2 距离在社交、接触和协作网络上导致潜在空间中节点相对位置失真，表现为性能下降。ℓ1LD-CTGR 通过使用满足三角不等式的 ℓ1 距离，将风险函数重新定义为 `λ_ij(s,t) := exp(β(s) + s ||r_i(t) - r_j(t)||_1)`，从而获得一个真正的度量空间。

这一改变产生了三个级联的因果效应：
1. **积分形式的质变**：平方 ℓ2 距离的风险函数积分是高斯积分（基于误差函数），而 ℓ1 距离的积分变为闭式分段指数积分（Theorem 1）。这一变化不仅提供了精确解，还避免了数值近似带来的计算复杂度和误差。
2. **优化方法的调整**：平方 ℓ2 距离可微，可使用标准梯度下降；ℓ1 范数在零点不可微，因此论文使用次梯度定义的下降方向（Theorem 3）替代梯度，使主流学习架构仍可训练参数。
3. **张量并行化的可能性**：在超低维嵌入 D=2 时，ℓ1 距离的积分可分解为张量并行化计算（Theorem 2），这与 GRASSP 的高斯积分形成对比——后者在 D=2 时虽也有闭式解，但形式不同。

实验证据表明，这一替换带来了显著性能提升：在 Synthetic-α 数据集上，ℓ1LD-CTGR 的 ROC 比 GRASSP 高 0.216（0.793 vs 0.577），PR 高 0.199；在 Infectious 上 ROC 提升 0.123；在 HyperText 和 Reddit 上分别提升 0.087 和 0.094（Table A5）。更重要的是，ℓ1LD-CTGR 与 GRASSP 具有相同的实际运行时间量级（Table A1），说明计算效率并未因积分形式变化而受损。论文还对比了使用 ℓ2 距离（无平方）的数值积分版本，该版本因需要数值近似而普遍表现更差，进一步凸显了 ℓ1 距离闭式解的优势。

### 适用边界与条件

ℓ1LD-CTGR 的适用性受以下条件约束：
- **超低维嵌入假设**：论文的理论推导和实验主要集中在 D=2 的嵌入维度。Theorem 2 的张量并行化专门针对 D=2 设计。消融实验（Table A4）表明 ℓ1LD-CTGR 对维度变化具有鲁棒性，但更高维度的性能未充分验证。
- **分段线性轨迹假设**：节点运动建模为分段线性（B 个 bins），这一近似假设的有效性依赖于 bin 数量的选择。消融实验显示对 bin 数量的微小变化具有鲁棒性（Table A3），但极端情况（bin 过少或过多）的影响未探讨。
- **数据特性**：在 Facebook 和 NeurIPS 等挑战性真实数据集上，ℓ1LD-CTGR 仍优于其他方法（Table 2），但性能提升幅度因数据集而异。在部分网络补全任务中，ℓ1LD-CTGR 并非在所有情况下都最优（"all but two situations"），表明存在某些数据特性使其优势不明显。

### 局限与开放问题

论文未明确讨论方法的局限性，但基于实验设计和理论分析可识别以下关键局限：

1. **评估指标的单一性**：仅使用 AUC-ROC 和 AUC-PR，缺乏 NDCG、MAP 等排序指标或计算效率指标的对比，限制了对其综合性能的评判。
2. **维度扩展性未验证**：虽然消融实验涉及不同维度，但主要实验在 D=2 下进行。Theorem 2 的张量并行化仅适用于 D=2，更高维度时积分计算的复杂度可能显著增加。
3. **大规模图的可扩展性**：实验使用的数据集规模有限（最大为 Reddit），在更大规模图上的计算效率未验证。分段线性轨迹的 bin 数量与时间跨度相关，可能成为大规模图的瓶颈。

开放问题包括：
- 探索其他类型的有效度量（如 ℓ∞ 或混合度量）以进一步提高潜在空间的几何多样性。
- 设计更高效的算法来处理更高维度的嵌入，突破 D=2 的限制。
- 将 ℓ1LD-CTGR 扩展到更大规模的图数据，评估其在工业级应用中的可行性。

**需要人工验证的点**：论文声称 ℓ1LD-CTGR 在大多数情况下优于其他方法，但未明确说明在哪些数据集或任务上表现不佳。这一结论的边界条件需要从原始实验数据（Table 1 和 Table 2）中进一步核实。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/ell_1_Latent_Distance_based_Continuous_time_Graph_Representation.pdf

![[paperPDFs/ICLR_2026/ell_1_Latent_Distance_based_Continuous_time_Graph_Representation.pdf]]
