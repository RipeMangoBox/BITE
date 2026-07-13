---
title: "$S^3$-Slicer: A General Slicing Framework for Multi-Axis 3D Printing"
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/S_3_Slicer_A_General_Slicing_Framework_for_Multi_Axis_3D_Printing.pdf
project_link: "https://mewangcl.github.io/publication.html"
code_link: "https://dl.acm.org/doi/10.1145/3197517.3201342"
aliases:
- INFBMAPP
- S3SGSFMA3P
tags:
- SIGGRAPH_ASIA_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 采用可微分的 SIREN 隐式场同时表示层与刀路，将碰撞避免和刀路几何约束直接构建为可优化的损失函数，实现层与刀路的联合优化。
primary_logic: 隐式神经场及其空间导数的连续可微性允许在任意点直接评估碰撞状态与几何属性（法向、曲率等），从而在统一框架内将制造约束（碰撞、支撑自由、方向对齐）与刀路几何控制（间距、曲率）进行协同优化。
claims:
- "与 Neural Slicer 相比，所提方法在保持无支撑性能的同时彻底消除了碰撞，而 Neural Slicer 仅靠增加曲率损失权重无法避免碰撞。"
- 在 Fork 模型上，加入碰撞损失（L_cl）后工具与零件间的碰撞被消除，同时保持了高质量的方向对齐，直方图证实对齐度与无碰撞版本相当。
- 在 T-Bracket 的连续碳纤维加强中，所提方法用比 High-Density Toolpath 方法少 18.5% 的碳纤维，实现了高 33.9% 的刚度和相当的断裂力。
- T-Bracket model (continuous carbon fiber reinforcement) 上 stiffness (k) = 33.9% higher than HD baseline
---

# $S^3$-Slicer: A General Slicing Framework for Multi-Axis 3D Printing

> [!tip] 核心洞察
> 隐式神经场及其空间导数的连续可微性允许在任意点直接评估碰撞状态与几何属性（法向、曲率等），从而在统一框架内将制造约束（碰撞、支撑自由、方向对齐）与刀路几何控制（间距、曲率）进行协同优化。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于隐式神经场的多轴制造工艺规划：碰撞避免与刀路几何的直接控制 |
| 英文题名 | $S^3$-Slicer: A General Slicing Framework for Multi-Axis 3D Printing |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://mewangcl.github.io/publication.html) · [paper](http://arxiv.org/abs/2505.03779) · [Code](https://dl.acm.org/doi/10.1145/3197517.3201342) · [Project](https://doi.org/10.1145/3550454.3555516) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Implicit Neural Field-Based Multi-Axis Process Planning |
| Dataset | T-Bracket model, Fertility model, Fork model |

> [!tip] 效果简介
> - T-Bracket model (continuous carbon fiber reinforcement) 上，stiffness (k) 33.9% higher than HD baseline vs High-Density Toolpath method (+33.9%)。
> - Fertility model (support-free printing) 上，collision elimination all collisions removed, support-free maintained vs Neural Slicer (curvature-controlled) (from severe collisions to collision-free)。
> - Fork model (direction alignment) 上，direction alignment quality & collision status collision eliminated, alignment distribution comparable vs without collision loss (collisions removed without degrading alignment)。

## 概要

现有的多轴制造工艺规划方法——无论是基于变形场的曲线层切片（如 S³-Slicer）还是基于隐式神经场的切片（如 Neural Slicer）——仅通过局部曲率控制间接处理碰撞，无法检测全局工具-零件干涉，且刀路几何在优化过程中不可控，导致制造可行性与机械性能受限。

本文提出一种基于隐式神经场的统一可微框架，采用 SIREN 网络同时表示层标量场与路径标量场，将碰撞避免和刀路几何约束直接构建为可优化的损失函数，实现层与刀路的联合优化。核心机理在于：隐式场及其空间导数的连续可微性，允许在任意点直接评估碰撞状态与几何属性（法向、曲率、路径间距等），从而在统一框架内协同优化制造约束与刀路品质。

实验表明，该方法在 Fertility 模型上彻底消除了 Neural Slicer 无法避免的碰撞，同时保持无支撑性能；在 Fork 模型上，碰撞损失消除了工具-零件干涉而未损害方向对齐质量；在 T-Bracket 的连续碳纤维增强中，以比 High-Density Toolpath 方法少 18.5% 的碳纤维用量，实现了高 33.9% 的刚度。该方法定位为将碰撞避免从后处理或间接控制提升为场优化原语，并将刀路几何纳入可微规划回路。

## 核心方法与创新机理

### 1. 问题瓶颈与核心洞察

现有的多轴制造工艺规划方法面临两个根本性瓶颈。其一，碰撞避免仅通过间接手段实现——**S³-Slicer**（Zhang et al., ACM TOG 2022）依赖变形场的局部曲率限制，**Neural Slicer**（Liu et al., ACM TOG 2024）通过四元数变形和曲率损失间接约束，两者均无法在优化过程中显式检测和消除工具与零件间的全局碰撞。其二，刀路几何（路径间距、测地曲率、方向对齐）与层生成过程解耦，通常作为后处理步骤完成，导致层与刀路无法协同优化，制造的可行性与力学性能受限。

本文的核心洞察在于：**隐式神经场及其空间导数的连续可微性，允许在任意空间点直接评估碰撞状态与几何属性**。通过将层与刀路统一表示为可微的 SIREN 隐式场，碰撞避免和刀路几何控制可以从间接约束转化为直接可优化的损失函数，在一个统一的梯度下降框架内实现层与刀路的联合优化。

### 2. 统一隐式表征框架

方法的核心是引入两个定义在零件域 $\Omega$ 上的标量场（图 2）：

- **层场** $f_l(\mathbf{x}): \Omega \to \mathbb{R}$，其水平集 $l_l(c) = \{ \mathbf{x} \mid f_l(\mathbf{x}) = c \}$ 定义打印/铣削层。
- **路径场** $f_p(\mathbf{x}): \Omega \to \mathbb{R}$，其与层场水平面的交线 $l_l(c) \cap l_p(c)$ 定义刀路曲线。

两个场均采用 **SIREN**（Sinusoidal Representation Network）架构实现——即带有正弦激活函数的多层感知机（MLP），因其在表示高频细节和计算精确空间导数方面的优异性能。网络结构如图 3(a) 所示：输入为空间坐标 $\mathbf{x}$，经过若干全连接层（每层后接正弦激活），输出标量场值 $f(\mathbf{x})$。通过自动微分，可同时获得一阶梯度 $\nabla f$ 和二阶 Hessian 矩阵 $\mathbf{H}_f$，这是后续所有几何计算和损失构建的基础。

### 3. 关键几何量的可微计算

从两个标量场出发，所有制造相关的几何属性均可通过场导数解析表达：

- **层表面单位法向**（Eq. 2）：
  $$\mathbf{n}_{f_l}(\mathbf{x}) = \frac{\nabla f_l(\mathbf{x})}{\|\nabla f_l(\mathbf{x})\|}$$
  该法向直接决定多轴打印/铣削时的工具朝向。

- **刀路切向量**（Eq. 3）：
  $$\mathbf{t} = \frac{\mathbf{n}_{f_l} \times \mathbf{n}_{f_p}}{\|\mathbf{n}_{f_l} \times \mathbf{n}_{f_p}\|}$$
  刀路方向由层法向与路径法向的叉积给出，保证刀路始终位于层曲面内。

- **投影梯度**（Eq. 4）：
  $$\nabla_l f_p = \nabla f_p - (\nabla f_p \cdot \mathbf{n}_{f_l}) \mathbf{n}_{f_l}$$
  路径场梯度在层曲面上的投影，其范数 $\|\nabla_l f_p\|$ 度量相邻刀路间距，方向则指示刀路法向。

- **层平均曲率**（Eq. 5）与**高斯曲率**（Eq. 6）：通过 Hessian 矩阵 $\mathbf{H}_{f_l}$ 计算，用于控制层曲面的平滑度。

- **刀路测地曲率**（Eq. 7）：
  $$\kappa_{\text{geo}}(\mathbf{x}) = \left\| \frac{d\mathbf{t}}{ds} - \left(\frac{d\mathbf{t}}{ds} \cdot \mathbf{n}_{f_l}\right) \mathbf{n}_{f_l} \right\|$$
  衡量刀路在层曲面内的弯曲程度，直接影响纤维增强中的力学连续性和打印过程中的工具加速度。

这些几何量的可微性是整个框架的数学基础——它们将制造约束转化为关于网络参数的可微损失函数，使梯度下降优化成为可能。

### 4. 核心创新模块：三个 Changed Slots

#### 4.1 碰撞避免机制：从间接约束到直接可微损失

**改变前**：S³-Slicer 和 Neural Slicer 通过限制层曲率间接降低碰撞风险，但无法检测或保证消除碰撞。Neural Slicer 即使增大曲率损失权重，仍产生严重碰撞（图 14、15）。

**改变后**：本文在层场优化阶段直接集成可微碰撞损失。核心原理如图 6 所示：对于层 $f_l(\mathbf{x}) = c$ 上的每个采样点 $\mathbf{x}$，在工具几何体上采样一组点 $\{\mathbf{y}\} \in T_{\mathbf{x}}$。碰撞判定基于层场值的比较——若工具点 $\mathbf{y}$ 的层场值 $f_l(\mathbf{y})$ 小于当前层值 $c$（即 $\mathbf{y}$ 位于已打印区域内），则判定为碰撞。

对于**增材制造**，碰撞损失（Eq. 13）为：
$$\mathcal{L}_{\text{cla}} = \frac{1}{|\{\Omega\}| |\{T\}|} \sum_{\mathbf{x}\in\{\Omega\}} \sum_{\mathbf{y}\in\{T_{\mathbf{x}}\}} \left(10\,\text{ReLU}( f_l(\mathbf{x}) - f_l(\mathbf{y}) + \delta ) \cdot \tilde{\Omega}_{\text{part}}(\mathbf{y}) \right)^2$$

其中 $\tilde{\Omega}_{\text{part}}$ 为零件 SDF 的平滑指示函数，$\delta$ 为安全容差。ReLU 激活确保仅在碰撞发生时产生惩罚。

对于**减材制造（铣削）**，碰撞损失（Eq. 15）改为：
$$\mathcal{L}_{\text{clm}} = \frac{1}{|\{\Omega\}| |\{T\}|} \sum_{\mathbf{x}\in\{\Omega\}} \sum_{\mathbf{y}\in\{T_{\mathbf{x}}\}} \left(10\,\text{ReLU}( -\text{sdf}_{\text{model}}(\mathbf{y}) + \delta ) \right)^2$$

该损失惩罚工具点侵入目标零件内部的情形。工具几何被近似为圆柱/圆锥组合体以加速采样（图 11），碰撞损失通过 SDF 模型网络（独立训练的 SIREN 网络拟合零件符号距离场）高效评估。

**因果链路**：碰撞损失直接作用于层场网络参数，通过梯度下降调整层曲面形状，将工具从碰撞区域“推开”，同时保持其他功能性损失（如无支撑、方向对齐）的优化目标。

#### 4.2 刀路几何控制：层与刀路的联合优化

**改变前**：High-Density Toolpath 方法（Zhang et al., Composites Part B 2025）在固定层上通过后处理生成刀路，方向对齐通过离线优化实现，刀路间距和曲率不可直接控制。

**改变后**：本文通过路径场 $f_p$ 与层场 $f_l$ 的联合优化，将刀路几何需求直接构建为可微损失：

- **方向对齐损失**（Eqs. 17–20）：使刀路切向 $\mathbf{t}$ 与期望方向 $\mathbf{d}$（如最大主应力方向）对齐。非归一化形式（Eq. 20）：
  $$\mathcal{L}_{\text{df1}} = \frac{10}{|\Omega_d|} \sum_{\mathbf{x}\in\Omega_d} \| (\mathbf{n}_{f_l} \times \nabla f_p) \times \mathbf{d} \|^2$$
  实验表明非归一化损失比归一化版本（Eq. 16）更好地处理奇异点，收敛到更优的刀路布局（图 27）。

- **路径间距损失**（Eq. 28）：
  $$\mathcal{L}_{\text{pds}} = \frac{1}{|\{\Omega\}|} \sum_{\mathbf{x}\in\{\Omega\}} \left( 1 - \| \nabla_l f_p \| \right)^2$$
  推动投影梯度范数趋近于 1，实现均匀的刀路间距。

- **路径曲率损失**：基于测地曲率 $\kappa_{\text{geo}}$ 构建，但仅当投影梯度范数大于阈值时计算（曲率过滤），否则在奇异点附近优化发散（图 25）。

**因果链路**：方向对齐损失调整 $\nabla f_p$ 的方向，间距损失调整其范数，曲率损失平滑刀路轨迹。这些损失同时反向传播至 $f_l$ 和 $f_p$ 的网络参数，实现层与刀路的协同优化——层形状为刀路提供几何载体，刀路需求反过来影响层的演化。

#### 4.3 层间距离控制：从固定梯度到自适应导数平滑

**改变前**：传统方法直接固定 $\|\nabla f_l\| = 1$ 或使用拉普拉斯平滑，强制均匀层距，限制了层在复杂几何处的自适应能力。

**改变后**：本文采用基于导数平滑的自适应控制（Eq. 26）：
$$\mathcal{L}_{\text{lds}} = \frac{1}{|\Omega|} \sum_{\mathbf{x}\in\Omega} \sum_{k\in x,y,z} \frac{1}{\|\nabla f_l\|} \left( \frac{d(\|\nabla f_l\|)}{dk} \right)^2$$

该损失惩罚梯度范数的空间变化率，而非强制其等于常数。这允许 $\|\nabla f_l\|$ 在零件不同区域自适应变化：在曲率大的区域允许更密的层分布，在平坦区域保持均匀层距。有效频率常数 $c=0.1$ 在层场平滑度与局部适应能力之间取得最佳平衡（图 24）：$c$ 过低导致区域耦合和非均匀层距，过高则引入过多奇异性。

### 5. 完整优化流水线

图 3(b) 和图 5 展示了完整的优化流水线。总损失函数由三类损失加权组合：

$$\mathcal{L}_{\text{total}} = \sum \lambda_R \mathcal{L}_R + \sum \lambda_F \mathcal{L}_F + \sum \lambda_C \mathcal{L}_C$$

- **正则化损失** $\mathcal{L}_R$：包括层曲率损失、路径曲率损失、层距平滑损失、路径间距损失，控制几何品质。
- **功能损失** $\mathcal{L}_F$：包括方向对齐损失、无支撑损失（Eq. 30，要求层法向与零件表面法向满足自支撑角度限制）、支撑生成损失。
- **碰撞损失** $\mathcal{L}_C$：增材碰撞损失 $\mathcal{L}_{\text{cla}}$ 或减材碰撞损失 $\mathcal{L}_{\text{clm}}$。

优化流程如下：

1. **初始化**：训练 SDF 模型网络拟合零件符号距离场（用于碰撞检测）。层场 $f_l$ 初始化为沿某个方向线性增长的场，路径场 $f_p$ 初始化为正交方向的线性场。
2. **采样**：在零件域 $\Omega$ 内采样空间点，在工具几何上采样碰撞检测点。
3. **前向计算**：将采样点输入 SIREN 网络，获得场值、一阶梯度和二阶 Hessian。
4. **损失计算**：根据当前应用（无支撑打印、铣削、纤维增强）选择对应的损失组合（权重配置见表 1），计算总损失。
5. **反向传播**：通过自动微分计算损失对网络参数的梯度，更新 $f_l$ 和 $f_p$ 的网络权重。
6. **迭代**：重复步骤 2–5，直至收敛。部分损失权重在优化过程中逐渐增大（表 1 中箭头标记），以稳定训练。
7. **后处理**：从收敛的场中提取水平集，生成层曲面和刀路曲线，用于实际制造。

对于复杂模型，还引入**摆放优化模块**（Eq. 41），优化零件在打印平台上的位置和方向，以改善可制造性（如减少悬垂区域）。

### 6. 关键公式变量含义速查

| 符号 | 含义 | 来源 |
|------|------|------|
| $f_l, f_p$ | 层场、路径场 | SIREN 网络输出 |
| $\nabla f_l, \nabla f_p$ | 场梯度 | 自动微分一阶导 |
| $\mathbf{H}_{f_l}$ | 层场 Hessian | 自动微分二阶导 |
| $\mathbf{n}_{f_l}$ | 层表面单位法向 | Eq. 2 |
| $\mathbf{t}$ | 刀路单位切向量 | Eq. 3 |
| $\nabla_l f_p$ | 路径场投影梯度 | Eq. 4 |
| $K_M, K_G$ | 层平均曲率、高斯曲率 | Eqs. 5–6 |
| $\kappa_{\text{geo}}$ | 刀路测地曲率 | Eq. 7 |
| $\tilde{\Omega}_{\text{part}}$ | 零件 SDF 平滑指示函数 | SDF 模型网络 |
| $\mathbf{d}$ | 期望刀路方向 | 应力分析或用户指定 |
| $\delta$ | 碰撞安全容差 | 用户设定 |

### 7. 训练与推理路径

**训练阶段**：SDF 模型网络独立预训练（使用零件表面采样点），层场和路径场网络联合训练。所有网络均为轻量 MLP（约 5–8 层，每层 256 神经元），在 NVIDIA RTX 3070 上优化。标准优化周期时间见表 2：典型模型（如 Fertility，最大包围盒尺寸约 150 mm）的优化时间约 30–60 分钟。

**推理阶段**：训练完成后，网络可在任意空间点快速查询场值和导数，无需重新优化。层和刀路通过 Marching Cubes 或等高线追踪从水平集提取。

![[assets/figures/papers/paper_list_l7_https_mewangcl_github_io_publication_html/figures/004_Figure_4.jpg]]
*Figure 4: Illustration of the geometric meaning of spatial derivatives of scalar fields and their derived quantities*

![[assets/figures/papers/paper_list_l7_https_mewangcl_github_io_publication_html/figures/003_Figure_3.jpg]]
*Figure 3: Pipeline of the algorithm for neural field-based process planning: (a) illustrates the structure of the neural network used for all field representations in our work. Each unit*

![[assets/figures/papers/paper_list_l7_https_mewangcl_github_io_publication_html/figures/005_Figure_5.jpg]]
*Figure 5: Illustration of the total loss function framework used across different applications. Individual loss components are categorized as: (i) regularization losses*

## 实验与关键发现

### 一、实验设置概览

所有实验在统一软硬件环境下完成：NVIDIA RTX 3070 GPU、Intel i9-14900K CPU、64 GB RAM，基于 PyTorch 实现。测试模型覆盖无支撑增材制造（Fertility、4C）、方向对齐纤维增强（Fork、T-Bracket）及减材铣削（Cup）三类典型多轴制造场景。各模型的最大包围盒尺寸、采样点数及优化时间统计于 Table 2，优化时间从数十分钟到数小时不等。不同应用场景的损失权重配置在 Table 1 中给出，部分权重在优化过程中采用渐进增大策略（以 → 表示）。

对比基线方法均按原始论文实现或设置运行：**S³-Slicer**（Zhang et al., ACM Trans. Graph. 2022）代表基于变形场的曲线层切片方法，**Neural Slicer**（Liu et al., ACM Trans. Graph. 2024）代表隐式神经场切片方法，**High-Density Toolpath**（Zhang et al., Composites Part B 2025）代表高密度纤维路径生成方法。

### 二、碰撞避免：从间接曲率控制到直接可微损失

碰撞避免是本文框架的核心差异化能力。传统方法（S³-Slicer、Neural Slicer）仅通过曲率正则化间接约束层几何，无法显式检测或消除工具-零件干涉。

**Fertility 模型（Fig. 14）** 提供了决定性对比证据。Neural Slicer 在 Quaternion Harmonic 权重 0.01 下生成的层虽达到与本文方法相当的无支撑性能，但在多处位置（Fig. 14(a2) 标注区域）工具与已打印零件发生严重碰撞。增大曲率损失权重无法消除这些碰撞——因为曲率控制与碰撞状态之间不存在因果关联。相比之下，本文方法通过直接可微碰撞损失 $\mathcal{L}_{\mathrm{cla}}$（Eq. 13）在层场优化阶段显式惩罚工具采样点侵入已打印区域，成功消除了所有碰撞（Fig. 14(b)），同时保持了无支撑性能。

**4C 模型（Fig. 16）** 进一步验证了这一能力。该模型在平面打印中需要支撑的区域以红色标注。S³-Slicer 的结果（Fig. 16(a)）存在多处工具-零件碰撞。本文方法在加入碰撞损失（SCF 完整公式）后，消除了所有碰撞并保持了无支撑层朝向（Fig. 16(c)）。值得注意的是，移除碰撞损失后（Fig. 16(b)），碰撞问题重新出现，直接证实了碰撞损失模块的因果作用。

**Fork 模型（Fig. 18）** 揭示了碰撞避免与方向对齐之间的协同关系。该模型需要刀路方向与最大主应力方向对齐以增强力学性能。在未加入碰撞损失时（Fig. 18(d1)），优化后的刀路虽对齐良好但存在工具-零件干涉。加入 $\mathcal{L}_{\mathrm{cla}}$ 后（Fig. 18(d2)），碰撞被消除，而方向对齐质量几乎不受影响——Fig. 18(c) 的直方图显示，有无碰撞损失下的方向偏差分布高度一致。这表明碰撞损失与方向对齐损失在优化空间中可解耦，不会因避碰而牺牲功能性能。

### 三、刀路几何控制与力学性能验证

T-Bracket 模型的连续碳纤维增强实验（Fig. 19, Fig. 20）是本文最具说服力的物理验证。该模型在特定加载条件下，最大主应力方向由有限元分析确定（Fig. 19(b)）。本文方法通过方向对齐损失 $\mathcal{L}_{\mathrm{df1}}$（Eq. 20）使刀路切向与应力方向对齐，同时通过路径间距损失 $\mathcal{L}_{\mathrm{pds}}$（Eq. 28）和路径曲率损失控制刀路几何品质。

**与 High-Density Toolpath 方法的定量对比（Fig. 20(d)）** 显示：本文方法在碳纤维用量减少 **18.5%** 的条件下，实现了刚度提升 **33.9%**，断裂力也略高于基线。这一反直觉结果——更少材料、更高性能——源于刀路方向与应力场的精确对齐以及刀路连续性的改善。High-Density Toolpath 方法的方向对齐依赖后处理修正，缺乏对刀路几何的直接优化控制，导致纤维路径偏离理想应力方向，材料效率降低。

Fig. 20(a-c) 的刀路可视化进一步揭示了差异：本文方法生成的刀路在几何突变处（如拐角、加强筋根部）保持了连续且平滑的过渡，而基线方法在这些区域出现路径断裂或急剧转向，削弱了纤维的连续承载能力。

### 四、关键消融实验

**（1）有效频率常数 c 的选择（Fig. 24）**

SIREN 网络的有效频率缩放因子 c 是控制层场行为的关键超参数。实验对比了 c 从 0.01 到 1.0 的表现：c = 0.1 在场平滑度与局部适应能力之间取得最佳平衡。c 过低（0.01）时，场过于平滑，导致空间上远距离区域耦合，产生非均匀层距；c 过高（≥ 0.5）时，场引入过多局部振荡和奇异性，层表面出现不连续或自交。该消融直接指导了 Table 1 中不同模型的 c 值选取策略。

**（2）路径曲率损失过滤（Fig. 25）**

路径曲率损失在奇异点（如层表面曲率极大处）附近会产生梯度爆炸，导致优化发散。本文提出仅当投影梯度范数 $\|\nabla_l f_p\|$ 大于阈值时才计算曲率损失的过滤策略。Fig. 25 显示，不过滤时优化在迭代后期发散，损失曲线剧烈振荡；加入过滤后优化稳定收敛。这一机制是方法稳定性的必要条件。

**（3）方向对齐损失的形式选择（Fig. 27）**

对比了归一化方向对齐损失（Eq. 16）与非归一化版本（Eqs. 17-19）在 Fork 模型上的表现。非归一化损失在奇异点附近具有更好的梯度行为，使优化收敛到更优的刀路布局——刀路方向与目标应力场的偏差更小，且路径分布更均匀。该消融验证了损失函数设计中对梯度特性的考量。

**（4）层曲率损失权重的影响（Fig. 26）**

增大层曲率损失权重会显著减慢层场的收敛速度。过高权重甚至引起优化不稳定性，表现为层表面的局部波动。这一发现指导了实际应用中曲率损失权重的设置原则：仅施加足够维持制造可行性的最小权重，避免过度约束限制层的自适应变形能力。

### 五、减材制造（铣削）场景验证

Cup 模型的五轴粗铣规划实验（Fig. 22）验证了框架在减材制造中的泛化能力。传统平面高度场策略（Fig. 22(b1)）在杯壁区域导致严重的工具-零件碰撞（Fig. 22(b2)）。本文方法通过铣削碰撞损失 $\mathcal{L}_{\mathrm{clm}}$（Eq. 15）——惩罚工具采样点侵入目标零件 SDF 内部——在优化过程中自动调整层几何，消除了所有碰撞（Fig. 22(c)），同时保持了材料去除效率。该实验表明，碰撞损失模块的框架设计（Eq. 12-15）可统一处理增材与减材两种制造范式，只需切换碰撞检测的符号逻辑。

### 六、失败模式与适用边界

**（1）薄壁特征碰撞漏检（Fig. 30）**

碰撞检测基于工具表面采样点，当零件特征尺寸小于采样间距时，工具可能穿透薄壁而不触发碰撞损失。Fig. 30 展示了一个薄壁模型的漏检案例。文中提出可通过扰动采样（在采样点邻域内随机偏移）降低漏检风险，但未给出系统性的采样密度准则。

**（2）工具几何近似误差**

当前工具被近似为轴向对称的圆柱/圆锥组合体，对末端形状复杂的工具（如带倒角、阶梯或非对称切削刃的刀具）可能产生不准确的碰撞评估。这一近似在粗加工场景下可接受，但在精加工或复杂刀具路径规划中可能引入误差。

**（3）SIREN 初始化和超参数敏感性**

SIREN 网络对初始化方案和频率参数敏感。若 c 值选择不当，可能导致场函数局部振荡或收敛缓慢。当前依赖人工试凑（Table 1 中的经验配置），缺乏自适应参数选择准则。

**（4）计算成本与采样分辨率**

优化时间随采样点数量线性增长。Table 2 显示，复杂模型（如 T-Bracket）的优化时间可达数小时。高分辨率采样虽提升碰撞检测精度和刀路品质，但显著增加计算开销。当前框架未针对实时或交互式应用优化。

**（5）工具朝向的简化假设**

当前方法按层法向确定工具朝向，未将工具逆运动学纳入优化变量。对于多自由度机械臂，这意味着可利用的运动空间未被充分开发——在某些构型下，偏离层法向的工具朝向可能同时满足碰撞避免和可达性要求，但当前框架无法探索这些解。

![[assets/figures/papers/paper_list_l7_https_mewangcl_github_io_publication_html/figures/020_Figure_14.jpg]]
*Figure 14: This figure presents a comparison of the Fertility model layers generated using Neural Slicer [3] with the Quaternion Harmonic weight of 0.01 (a) as indirect curvature control. We select a result exhibiting support-free performance comparable to ours (b). However, as shown in (a), the generated layers lead to severe collisions and intersections with the tool. Moreover, as illustrated in the two zoom-views (a(i) & a(ii)), such collisions cannot be resolved through post-processing because no valid configuration without collision could be obtained when using these layers. The black dashed-line on the histogram (b) shows the desired support-free threshold of 135◦, which shows that although the...*

![[assets/figures/papers/paper_list_l7_https_mewangcl_github_io_publication_html/figures/021_Figure_15.jpg]]
*Figure 15: This figure presents an additional comparison with the results of Neural Slicer. To mitigate collisions, we increased the Harmonic (curvature) Loss weight term in their formulation to reduce curvature. Subfigures (a1) and (a2) show the outcomes for weight values of 1.0 and 50.0, respectively, where collisions with the tool remain present. As shown in (b), this adjustment also causes a substantial deterioration of the support-free properties, while still failing to eliminate all collisions. This is because the collision region is already relatively flat locally, making curvature a poor indicator for such cases. In contrast, our result (a3) and (b) successfully avoids such collisions while ma...*

![[assets/figures/papers/paper_list_l7_https_mewangcl_github_io_publication_html/figures/022_Figure_16.jpg]]
*Figure 16: Results and comparisons for the 4C model (d), which we attempt to print without support. The red region in (d) indicates the area that would require support in a planar print. (a) shows the result obtained using the*

## 定位与知识库关联

本文提出的基于隐式神经场的多轴制造工艺规划框架，其核心定位在于**将碰撞避免和刀路几何控制从间接的后处理环节提升为可微优化的直接目标**，从而改变了现有曲线层切片方法中“碰撞仅靠局部曲率间接约束”这一根本性设计。

### 相对已有方法的本质差异

与两类代表性基线方法相比，本文改变的关键 slot 如下：

**相对于 S^3-Slicer（Zhang et al., ACM Trans. Graph. 2022）和 Neural Slicer（Liu et al., ACM Trans. Graph. 2024）**：这两类方法均采用“间接碰撞控制”策略——S^3-Slicer 通过变形场和曲率限制隐式地避免层间干涉，Neural Slicer 则依赖四元数变形和曲率损失权重来间接影响碰撞。本文的**碰撞避免机制** slot 从“间接曲率控制或后处理修正”变为“直接可微碰撞损失，在层场优化中显式避免工具-零件干涉”。这一改变的因果机理在于：SIREN 隐式场及其空间导数的连续可微性，使得在任意采样点处可以直接评估工具与已打印零件/目标模型之间的空间关系（通过比较层场值或查询 SDF），并将碰撞状态构建为可微损失函数（式 12–15），从而在梯度下降过程中主动推开会产生干涉的层几何。实验证据（Fig. 14, Fig. 15）表明，Neural Slicer 即使增大曲率损失权重也无法消除 Fertility 模型上的严重碰撞，而本文方法在保持无支撑性能的同时彻底消除了碰撞。

**相对于 High-Density Toolpath 方法（Zhang et al., Composites Part B 2025）**：该方法的**刀路几何控制** slot 为“离线后处理生成，层与路径解耦”，即方向对齐通过后处理实现，路径间距和曲率无法在层生成阶段被联合优化。本文将其变为“通过可微损失实现层与刀路的联合优化，直接控制测地曲率、路径间距等几何属性”。具体而言，路径场 $f_p$ 与层场 $f_l$ 共享同一 SIREN 网络架构，刀路由两者的水平集交线定义（式 3–4），路径间距均匀性损失（式 28）、测地曲率损失（式 7）和方向对齐损失（式 17–20）均作为可微项直接作用于场优化。在 T-Bracket 的连续碳纤维增强实验中（Fig. 20），本文方法用比 HD 方法少 18.5% 的碳纤维实现了高 33.9% 的刚度，这一性能增益根源于刀路方向与主应力方向的精确对齐以及路径连续性的保障——这些恰是后处理解耦方案难以同时达成的。

此外，**层间距离控制** slot 也从“直接固定梯度范数或使用拉普拉斯平滑”变为“基于导数平滑的自适应控制”。传统方法强制 $\|\nabla f_l\| = 1$ 以保证等距层厚，但本文通过层距平滑损失（式 26）仅惩罚梯度范数的空间变化，允许场增长速率在空间上自适应调整（Fig. 7），从而在复杂几何上获得更均匀的实际层厚分布。

### 知识库挂载点

本文在知识库中的挂载点可从以下维度定位：

1. **隐式神经表示用于制造**：继承自 SIREN（Sitzmann et al., NeurIPS 2020）的周期性激活网络在表示连续场及其高阶导数方面的优势，本文将其拓展到多轴制造的层-路径联合表征。这一挂载点连接了神经隐式表示与计算制造两个领域。

2. **可微工艺规划**：本文属于将制造约束（碰撞、支撑自由、方向对齐）嵌入可微优化管线的研究脉络。与现有工作（如 Neural Slicer 将无支撑约束纳入场优化）相比，本文的关键增量在于将碰撞检测和刀路几何控制也纳入同一可微框架，实现了三个功能维度（碰撞避免、支撑自由、路径几何）的协同优化。

3. **曲线层切片与多轴增材制造**：在曲线层切片方法的演进中，本文代表了从“几何驱动的变形”到“物理约束驱动的可微优化”的范式转换。碰撞损失（式 13, 15）的引入使得层几何不再仅由局部曲率决定，而是全局地响应工具-零件空间关系。

### 适用边界

本文方法的适用边界由以下因素界定：

- **工具几何假设**：碰撞检测基于工具表面采样点，且工具被近似为轴向对称的圆柱/圆锥组合体。对于末端形状复杂的工具（如带侧刃的异形铣刀），碰撞评估可能不准确。此外，小尺寸或薄壁特征可能因采样不足而漏检碰撞（Fig. 30），需引入扰动采样作为补救措施。
- **场表征能力**：SIREN 网络对初始化和频率参数 $c$ 敏感。消融实验（Fig. 24）表明 $c=0.1$ 在平滑度与局部适应性之间取得平衡，但该参数目前依赖人工试凑，缺乏针对一般模型几何的自适应选择准则。
- **计算成本**：优化时间随采样点数量线性增长，高分辨率采样下可达数小时（Table 2），尚未针对实时交互式应用优化。
- **运动学简化**：工具朝向当前仅按层法向确定，未将逆运动学作为优化变量。这意味着对于多自由度机械臂，完整的无碰撞可达空间尚未被充分开发。

### 后续工作启发

本文为后续研究开辟了若干方向：

1. **全链路可微设计-制造优化**：由于层场、路径场和碰撞损失均为可微，该框架理论上可与拓扑优化、纤维取向优化等上游设计任务无缝耦合，实现从设计到制造的端到端梯度驱动优化。这是本文最具潜力的知识库延伸方向。

2. **支撑-层联合优化**：当前支撑生成（式 31–33）与层优化共享框架但未深度耦合。将支撑结构也表示为可微隐式场，并与层场协同优化，可进一步减少支撑材料用量。

3. **通用工具运动模型**：将工具取向作为独立优化变量（而非仅从层法向派生），并引入逆运动学约束，可充分利用多轴机床或机械臂的灵活性，同时避免当前因朝向固定而可能产生的“过保守”层变形。

4. **自适应超参数策略**：系统地表征频率缩放因子、采样密度和模型几何之间的相互作用，建立自适应参数选择准则，将降低该方法在实际工业部署中的调参门槛。

**证据强度说明**：本文的核心对比结论（碰撞消除、刚度提升）有物理实验和数值实验双重支撑，置信度较高。但关于“与拓扑优化无缝耦合”的潜力目前仅为框架层面的推演，尚未有实验验证，属于开放问题而非既定结论。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/S_3_Slicer_A_General_Slicing_Framework_for_Multi_Axis_3D_Printing.pdf]]