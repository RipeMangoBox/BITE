---
title: "The Affine Heat Method"
type: paper
paper_level: A
venue: SGP
year: 2025
pdf_ref: paperPDFs/SGP_2025/The_Affine_Heat_Method.pdf
code_link: null
project_link: https://www.yousufsoliman.com/projects/the-affine-heat-method.html
aliases:
- AHMAAA
- AHM
tags:
- SGP_2025
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "在连接拉普拉斯算子中引入齐次坐标，构造包含平移的仿射连接，使得短时热扩散能够直接同时编码从源点出发的测地线方向与距离。"
primary_logic: "利用齐次坐标将旋转和平移统一表示为线性变换，定义在平凡丛上的仿射连接 ∇ = d - (0 id; 0 0)，其平行截面沿最测地线的演化恰为对数映射，从而可通过求解单一仿射热扩散方程直接获得对数映射，避免分离计算与数值微分。"
claims:
- "在连接拉普拉斯算子中引入齐次坐标后，短时热流可直接同时给出从源点出发的测地线方向与距离。"
- "局部变体通过仿射扩散得到的径向场长度等于测地距离（即梯度平方距离的一半），无需数值微分。"
- "自适应变体通过适应源点的仿射连接，可直接计算出对数映射本身，参数化精度更高。"
- "仿射热方法在平直域上可精确恢复恒等参数化（至浮点精度）。"
---

# The Affine Heat Method

> [!tip] 核心洞察
> 利用齐次坐标将旋转和平移统一表示为线性变换，定义在平凡丛上的仿射连接 ∇ = d - (0 id; 0 0)，其平行截面沿最测地线的演化恰为对数映射，从而可通过求解单一仿射热扩散方程直接获得对数映射，避免分离计算与数值微分。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 仿射热方法 |
| 英文题名 | The Affine Heat Method |
| 会议/期刊 | SGP 2025 |
| Links | [paper](https://www.yousufsoliman.com/projects/download/AffineHeatMethod.pdf) · [Project](https://www.yousufsoliman.com/projects/the-affine-heat-method.html) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Affine Heat Method (AHM, 局部变体 AHM_ℓ 与自适应变体 AHM_a) |
| Dataset | 多个三维模型 (Fig. 2), S^2 球面序列网格, 网格数据集 (Fig. 22), 复杂网格 (Fig. 20) |

> [!tip] 效果简介
> - 多个三维模型 (Fig. 2) 上，度量畸变 D 为 显著更低的畸变，且在源点保持等距，对比 VHM_log, SEM, DEM，变化 全域畸变更小。
> - S^2 球面序列网格 上，对数映射 L^2 误差 为 线性收敛速率 O(h)，变化 O(h)。
> - 网格数据集 (Fig. 22) 上，单次求解耗时 为 AHM_ℓ 比 VHM_log 慢 27%；AHM_a 慢 70%，对比 VHM_log，变化 +27% / +70%。

## 概要

### 问题背景

在计算机图形学与几何处理中，曲面上的对数映射（logarithmic map）将曲面点映射到切空间，同时编码测地线方向和距离，是纹理映射、曲面参数化、形状分析等任务的基础工具。然而，从测地距离中提取方向信息需要数值微分，这不仅降低了正则性，还在源点附近和切割轨迹处引入显著畸变。

现有的基于热扩散的对数映射方法存在两个核心瓶颈：

1. **分离计算导致的精度损失**：**VHM_log**（Sharp et al., ACM Trans. Graph. 2019）通过向量热扩散近似平行传输，但需要分别计算角度分量和距离分量，或依赖不精确的数值微分来构建参数化；**SEM**（Herholz and Alexa, Comp. Graph. Forum 2019）则通过分离的角度扩散来平滑指数映射。这种分离策略在源点附近和切割轨迹处产生较大畸变。
2. **缺乏对平移的直接编码**：传统方法使用的 Levi-Civita 连接仅包含旋转信息，无法在连接拉普拉斯算子中直接编码切空间之间的平移关系，导致短时热扩散无法同时给出方向与距离。

### 核心方法

本文提出的**仿射热方法**（Affine Heat Method, AHM）通过一个关键的因果调节变量解决了上述问题：**在连接拉普拉斯算子中引入齐次坐标，构造包含平移的仿射连接**。

核心洞察在于：利用齐次坐标将欧几里得运动（旋转+平移）统一表示为线性变换，在平凡丛上定义仿射连接 $\overline{\nabla} := d - \begin{pmatrix} 0 & \mathrm{id} \\ 0 & 0 \end{pmatrix}$。该连接的平行截面沿最测地线的演化恰为对数映射，因此可通过求解单一的仿射热扩散方程直接获得对数映射，从根本上避免了分离计算与数值微分。

方法提供两种变体：
- **局部变体（AHM_ℓ）**：结合 Levi-Civita 连接与重言1-形式构造连接 $\nabla^{\ell}$，通过一次仿射热扩散得到径向场，再投影到向量热方法延拓的测地线框架上，提取对数映射。
- **自适应变体（AHM_a）**：通过适应源点的测地线框架定义连接 $\overline{\nabla}^{\Phi}$，直接计算出对数映射本身，参数化精度更高，但每次更改源点需重新分解算例。

### 主要结果

仿射热方法在多个维度上展现出显著优势：

- **度量畸变**（Figure 2）：在两个变体上均比 VHM_log、SEM 和 **DEM**（Schmidt et al., ACM Trans. Graph. 2006）产生显著更低的度量畸变 $\mathcal{D}$，且在源点保持等距。
- **平直域精确性**（Lemma 3）：在平面域上可精确恢复恒等参数化至浮点精度，而 VHM_log 在源点附近存在大量畸变（Figure 6）。
- **收敛性**（Figure 24）：在 $S^2$ 球面上对解析解呈现线性收敛速率 $O(h)$。
- **测地距离精度**（Figure 20）：在源点邻域内的测地距离估计比前馈热方法（**Heat Method** [Crane et al., 2013]、**Signed Heat Method** [Fischer et al., 2024]）更精确。
- **鲁棒性**（Figure 23）：对低质量网格的鲁棒性优于 VHM_log 和 SEM，结合内在 Delaunay 三角剖分可确保高质量参数化不受输入网格质量影响（Figure 14）。
- **计算开销**（Figure 22）：AHM_ℓ 比 VHM_log 慢约 27%，但支持预分解以加速重复求解；AHM_a 慢约 70%，每次更改源点需重新分解。

### 方法定位

仿射热方法属于基于热扩散的几何处理方法的谱系，是对向量热方法（VHM）的直接推广。其核心创新在于将连接从仅含旋转的 Levi-Civita 连接扩展为包含平移的仿射连接，从而将原本需要多步分离计算的对数映射任务统一为单次扩散求解。该方法在概念上与离散指数映射（DEM）和平滑指数映射（SEM）等显式追踪方法形成对比——后者依赖沿网格边或面的逐步传播，容易累积误差。

### 对数映射：测地距离与方向的统一编码

在计算机图形学与几何处理中，曲面上的测地距离是一个基础量，广泛应用于纹理映射、曲面参数化、形状分析等任务。然而，仅从标量距离场中提取方向信息需要进行数值微分，这不仅降低了正则性，还会在源点附近和切割轨迹（cut locus）处引入显著的精度损失。对数映射（logarithmic map）将测地距离与方向统一编码为以源点为中心的局部参数化，从而避免了上述问题。

具体而言，给定曲面 $M$ 上的一点 $p$，对数映射 $\log_p: M \to T_pM$ 将曲面上任意点 $q$ 映射到切空间中的一个向量，该向量的**方向**等于从 $p$ 到 $q$ 的最短测地线的初始方向，**长度**等于测地距离 $d(p,q)$。这一映射在源点的单射半径（injectivity radius）内是良定义的微分同胚，为下游任务提供了等距于切空间的局部坐标。

### 现有方法的瓶颈

目前计算离散对数映射的方法主要面临以下困境：

**基于显式追踪的方法**（如 **DEM**，Schmidt et al., ACM Trans. Graph. 2006）通过沿网格边展开径向测地线来构建参数化，但法向偏差的累积会导致严重的度量畸变，尤其在复杂几何上表现不稳定。

**基于热扩散的方法**试图利用短时热核的渐近性质来规避显式追踪。其中，**向量热方法**（**VHM_log**，Sharp et al., ACM Trans. Graph. 2019）通过向量扩散近似切向量的平行传输，进而构造对数映射。然而，该方法存在两个根本性缺陷：

1. **源点附近的畸变**：由于向量热方法仅编码旋转分量，需要额外通过数值微分或分离计算来恢复平移信息（即测地距离），导致源点邻域内精度大幅下降。在平面域上，VHM_log 甚至无法恢复恒等参数化（Figure 6）。
2. **分离计算的脆弱性**：**平滑指数映射**（**SEM**，Herholz and Alexa, Comp. Graph. Forum 2019）通过分离角度扩散来构建参数化，但同样在源点附近和平面域上产生显著畸变（Figure 26）。

这些方法的共同瓶颈在于：**它们将旋转与平移分量割裂处理，无法在单一扩散过程中同时编码测地线的方向与距离**。

### 核心洞察：仿射连接中的平移编码

本文的核心洞察源于对欧几里得运动群 $SE(n)$ 齐次坐标表示的重新审视。一个刚体运动 $g = (A, b)$（其中 $A \in SO(n)$ 为旋转，$b \in \mathbb{R}^n$ 为平移）在齐次坐标下可统一表示为线性变换：

$$g = \begin{pmatrix} A & b \\ 0 & 1 \end{pmatrix}$$

这一观察启发我们：**若能在连接拉普拉斯算子中引入齐次坐标来编码切空间标架间的平移，则短时热扩散可直接同时给出从源点出发的测地线方向与距离**。

具体而言，我们在平凡丛 $\mathbb{R}^{n+1} \to \mathbb{R}^n$ 上定义仿射连接：

$$\overline{\nabla} := d - \begin{pmatrix} 0 & \mathrm{id} \\ 0 & 0 \end{pmatrix}$$

该连接将无穷小平移编码为连接1-形式，使得沿最测地线的平行截面恰好演化为对数映射本身。这一构造的数学保证来自 Lemma 1：若 $(Y, \lambda)$ 满足 $Y_p = 0$、$\lambda_p = 1$，且沿所有通过 $p$ 的测地线是 $\nabla^\ell$-平行的，则 $Y = d_p(\gamma) \gamma' / |\gamma'|$ 且 $\lambda \equiv 1$。这意味着**径向场的长度精确等于测地距离，无需任何数值微分**。

### 本文的动机与贡献

基于上述洞察，本文提出**仿射热方法**（Affine Heat Method, AHM），通过求解单一仿射热扩散方程直接获得对数映射，从根本上避免分离计算与数值微分。方法包含两个互补变体：

- **局部变体（AHM_ℓ）**：在切丛与平凡线丛的直和上定义连接 $\nabla^\ell$，通过一次仿射扩散得到径向场，再借助向量热方法延拓的测地线框架提取对数映射。
- **自适应变体（AHM_a）**：在适应于源点的测地线框架下定义连接 $\overline{\nabla}^{\Phi}$，通过两次扩散直接输出 $\mathbb{R}^2$ 坐标，在切割轨迹附近提供更平滑的角度坐标。

在平面域上，AHM 可精确恢复恒等参数化至浮点精度（Lemma 3），这一性质是现有热扩散方法所不具备的。

## 核心方法与创新机理

### 瓶颈与突破：从纯旋转连接到仿射连接

现有的基于热扩散的对数映射方法存在一个共同的深层瓶颈：它们依赖的微分算子仅编码了切空间之间的**旋转**分量，而平移分量要么被忽略，要么通过分离的数值微分或角度扩散来事后补全。这导致了两个典型失败模式：

1. **源点附近畸变严重**：**VHM_log**（Sharp et al., ACM Trans. Graph. 2019）在源点邻域内产生大量度量畸变，即使在平直域上也无法恢复恒等参数化（Figure 6）。
2. **切割轨迹处不连续**：**SEM**（Herholz and Alexa, Comp. Graph. Forum 2019）将角度分量与距离分量分离计算，在测地线碰撞区域难以保持角度坐标的平滑性。

本工作的核心创新在于**将平移显式编码为连接的一部分**，从而通过单一的热扩散方程同时解出测地线的方向与距离。具体而言，通过在连接拉普拉斯算子中引入**齐次坐标**（homogeneous coordinate），将原本仅包含旋转的 Levi-Civita 连接扩展为包含平移的**仿射连接**。短时热流在该仿射连接下的演化，其平行截面沿最测地线的行为恰好对应了对数映射的构造。

### Changed Slot：连接构造的根本性改变

| 维度 | 基线方法 | 仿射热方法 |
|------|----------|------------|
| **连接类型** | 仅包含旋转的 Levi-Civita 连接（或分离角度扩散） | 包含旋转和平移的仿射连接，引入齐次坐标 |
| **平移编码** | 不编码；通过数值微分或分离计算补全 | 显式编码在连接的矩阵值1-形式中 |
| **核心方程** | 向量热扩散 | 仿射热扩散：$(M + \tau L) [\mathsf{y}; \lambda] = \delta_p$ |

#### 仿射连接的数学构造

基础仿射连接定义在平凡丛 $\mathbb{R}^{n+1} \to \mathbb{R}^n$ 上：

$$\overline{\nabla} := d - \begin{pmatrix} 0 & \mathrm{id} \\ 0 & 0 \end{pmatrix}$$

该连接将无穷小平移编码为矩阵值1-形式中的非对角块 $\mathrm{id}$。其平行截面沿曲线的演化满足线性增长，恰好对应了从源点出发的测地线参数化。

在局部变体 **AHM_ℓ** 中，该连接被提升到 $TM \oplus \mathbb{R}$ 上，与 Levi-Civita 连接耦合：

$$\nabla^{\ell} = \begin{pmatrix} \nabla & 0 \\ d & 0 \end{pmatrix} - \begin{pmatrix} 0 & \mathrm{id} \\ 0 & 0 \end{pmatrix}$$

该构造的平行传输条件 $\nabla^{\ell}_{\gamma'} (Y, \lambda) = 0$ 直接蕴含：沿测地线 $\gamma$，$Y = d_p(\gamma) \cdot \gamma' / |\gamma'|$ 且 $\lambda \equiv 1$（Lemma 1）。这意味着**径向场 $Y$ 的长度恰好等于测地距离**，无需任何数值微分。

在自适应变体 **AHM_a** 中，连接进一步适应于源点的测地线框架：

$$\overline{\nabla}^{\Phi} := d - \begin{pmatrix} 0 & \Phi \\ \Phi \circ \mathrm{id} & 0 \end{pmatrix}$$

其中 $\Phi: TM \to \mathbb{R}^n$ 是通过平行传输构建的测地线框架识别映射。该变体直接计算出对数映射本身，通过齐次坐标归一化 $\Phi_{\nu} := \mathbf{x}_{\nu} / \lambda_{\nu}$ 获得最终参数化。

### 关键性质：平直域上的精确恢复

仿射热方法在平直域上可精确恢复恒等参数化，达到浮点精度（Lemma 3）。这一性质源自仿射连接的构造与欧几里得运动的齐次坐标表示之间的内在一致性：在 $\mathbb{R}^n$ 上，标量扩散的解满足 $\tilde{\mathbf{x}}_i = 0$，经平移后得到 $\mathbf{x}_i = z_i$ 对所有顶点成立。相比之下，VHM_log 在平直域上仍会产生显著的源点邻域畸变（Figure 6），这直接印证了缺少平移编码是现有方法精度不足的因果机制。

### 方法谱系与知识库定位

仿射热方法处于热方法（Heat Method）与连接拉普拉斯算子（Connection Laplacian）两条技术路线的交汇点：

- **热方法谱系**：继承自 **HM**（Crane et al., ACM Trans. Graph. 2013）的短时热扩散范式，但将标量扩散推广为仿射扩散，从而同时获得方向与距离信息。
- **向量热方法谱系**：直接回应 **VHM_log**（Sharp et al., ACM Trans. Graph. 2019）的局限——VHM_log 仅用向量扩散近似平行传输，再通过数值微分提取距离；AHM 通过在连接中编码平移，将两步合并为一步，消除了数值微分引入的误差。
- **指数映射方法谱系**：相对于 **DEM**（Schmidt et al., ACM Trans. Graph. 2006）的显式径向追踪和 **SEM**（Herholz and Alexa, Comp. Graph. Forum 2019）的分离角度扩散，AHM 提供了统一的 PDE 框架，在切割轨迹附近保持角度坐标的平滑性。

仿射热方法（Affine Heat Method, AHM）从一个核心洞察出发：在齐次坐标下，欧几里得运动（旋转+平移）可统一表示为线性变换。将这一思想注入连接拉普拉斯算子的构造中，使得短时热扩散能够**直接同时编码从源点出发的测地线方向与距离**，从而绕过了现有方法（如 VHM_log、SEM）中分离计算角度分量或不精确数值微分带来的精度损失。

论文提出了两个互补的变体，共享同一个底层原理但采用不同的连接构造策略：

| 变体 | 核心机制 | 输出 | 关键差异 |
|------|----------|------|----------|
| **局部变体 AHM_ℓ** | 在 $TM \oplus \mathbb{R}$ 上定义连接 $\nabla^{\ell}$，结合 Levi-Civita 连接与重言 1-形式 | 径向场 $(Y, \lambda)$，其中 $|Y|$ 等于测地距离 | 需要额外计算测地线框架以提取对数映射 |
| **自适应变体 AHM_a** | 在平凡丛上定义适应于源点的仿射连接 $\overline{\nabla}^{\Phi}$ | 直接输出二维参数化坐标 | 每次更改源点需重新分解算例 |

### 通用 Pipeline

两种变体共享一个统一的二阶段或三阶段流程，其信息流可概括为：

```
源点 p → [仿射连接拉普拉斯构建] → [短时热扩散求解] → [对数映射提取] → 参数化 Φ: M → ℝ²
```

#### 阶段一：离散仿射连接拉普拉斯算子构建

在给定的三角网格（或内在 Delaunay 三角剖分）上，组装带齐次坐标的仿射连接拉普拉斯矩阵。核心操作为：

- **局部变体**：在每条边 $ij$ 上定义离散仿射平行传输 $r_{ij}^{\nabla^{\ell}}(X_i) = r_{ij}^{\nabla} X_i + e_{ji}$，其中 $r_{ij}^{\nabla}$ 是 Levi-Civita 连接的旋转分量（由边向量比给出），$e_{ji}$ 是边向量提供的平移分量（Equation 9）。该传输作用于 $(n+1)$ 维向量——前 $n$ 维为切向量，末维为齐次坐标。
- **自适应变体**：构建适应于源点 $p$ 的测地线框架 $\Phi: TM \to \mathbb{R}^n$（通过向量热方法延拓正交标架），并在平凡丛上定义连接 $\overline{\nabla}^{\Phi} = d - (0\ \Phi\ \Phi \circ \mathrm{id};\ 0\ 0)$（Equation 14），使得平行截面沿最短测地线的演化恰为对数映射本身。

#### 阶段二：仿射热扩散求解

以源点 $p$ 处的 Dirac delta 为右端项，用单步反向欧拉法求解短时仿射热方程（时间步长 $\tau = h^2$，$h$ 为平均边长）：

$$(\mathsf{M} + \tau \mathsf{L}^{\nabla}) \binom{\mathsf{Y}}{\lambda} = \binom{0}{1} \delta_p$$

其中 $\mathsf{M}$ 为质量矩阵，$\mathsf{L}^{\nabla}$ 为仿射连接拉普拉斯矩阵。此步的输出是一个全局定义的场：

- **AHM_ℓ**：输出径向向量场 $Y$ 和齐次坐标场 $\lambda$。由 Lemma 1 保证，当 $(Y, \lambda)$ 沿所有通过 $p$ 的测地线 $\nabla^{\ell}$-平行且满足 $Y_p = 0, \lambda_p = 1$ 时，$Y$ 的长度精确等于测地距离，即 $Y = d_p(\gamma) \cdot \gamma' / |\gamma'|$ 且 $\lambda \equiv 1$。
- **AHM_a**：输出三维齐次坐标场 $(\mathbf{x}, \lambda)$，其中 $\mathbf{x} \in \mathbb{R}^2$ 直接编码了二维参数化信息。

#### 阶段三（仅 AHM_ℓ）：测地线框架计算

局部变体得到的径向场 $Y$ 位于各点的切空间 $T_q M$ 中，需要将其投影到一个全局一致的坐标系下才能获得对数映射。为此，通过向量热方法（VHM）从源点 $p$ 延拓其正交标架 $\{E_i(p)\}$ 至整个曲面，构建测地线框架。该框架为每个点 $q$ 提供了 $T_q M$ 与 $\mathbb{R}^n$ 之间的等距识别（Figure 10 右）。

#### 对数映射提取

- **AHM_ℓ**：将径向场投影到测地线框架，得到最终参数化：$\mathbf{x}(q) = (\langle E_i(q), Y_q \rangle)_{i=1}^n$（Equation 7/12）。
- **AHM_a**：直接通过齐次坐标归一化获得：$\Phi_{\nu} = \mathbf{x}_{\nu} / \lambda_{\nu}$（Equation 16）。

### 关键理论保证

框架的数学基础建立在两个核心事实上：

1. **平直域精确恢复**：Lemma 3 证明，在欧几里得域上，仿射热扩散的解经齐次坐标归一化后可精确恢复恒等参数化（至浮点精度），而 VHM_log 在源点附近存在显著畸变（Figure 6）。
2. **线性收敛**：在 $S^2$ 球面序列网格上，方法展现出 $O(h)$ 的线性收敛速率（Figure 24）。

### 计算特性与适用场景

| 特性 | AHM_ℓ | AHM_a |
|------|-------|-------|
| 矩阵分解复用 | 支持预分解，重复求解加速 | 每次更改源点需重新分解 |
| 切割轨迹附近行为 | 角度坐标可能出现不连续 | 提供更平滑的角度坐标（Figure 12） |
| 计算开销 | 比 VHM_log 慢约 27% | 比 VHM_log 慢约 70%（Figure 22） |
| 网格质量鲁棒性 | 强（配合内在 Delaunay） | 强（配合内在 Delaunay） |

两种变体在注入半径内产生几乎不可区分的参数化结果（Figure 8），且均对低质量网格具有优于 VHM_log 和 SEM 的鲁棒性（Figure 23）。实际应用中可根据场景选择：需要频繁更换源点时优先 AHM_ℓ（利用预分解加速），追求切割轨迹附近平滑性时优先 AHM_a。

![[assets/figures/papers/paper_list_l34_https_www_yousufsoliman_com_projects_download_AffineHeatMethod_pdf/figures/002_Figure_2.jpg]]
*Figure 2: Metric Distortion. Compared with prior methods V H M _ { l o g } \ : l S S C I 9 \ : l , , SEM [HA19], and DEM [SGW06] (bottom row), both variants of our affine heat method produce parameterizations with dramatically less metric distortion (D) (Eqn. 18). We remark that our parameterizations are isometric at the source, just as the logarithmic map is in the smooth setting*

### 核心思想：从向量热到仿射热

向量热方法（**VHM_log**, Sharp et al., TOG 2019）的核心在于：沿最短测地线的平行传输可通过短时向量热扩散来近似。具体而言，给定源点 $p$ 处的切向量 $\mathbf{X}_p$，求解连接拉普拉斯热方程 $(M + \tau L^\nabla) \mathbf{X} = \delta_p \mathbf{X}_p$ 并归一化解，即可得到 $\mathbf{X}_p$ 沿所有从 $p$ 出发的测地线的平行传输场。

然而，VHM_log 在构造对数映射时存在根本性缺陷：它需要先通过向量扩散获得径向方向场，再通过数值微分测地距离来缩放该方向场——这种分离计算在源点附近和切割轨迹处引入显著畸变。**仿射热方法 (AHM)** 的核心洞察是：若在连接中同时编码旋转和平移，则单次短时热扩散即可直接给出对数映射的完整信息。

### 关键公式体系

#### 1. 齐次坐标与欧几里得运动

仿射热方法的数学基础在于利用齐次坐标将旋转和平移统一表示为线性变换。$\mathrm{SE}(n)$ 中的元素可写为 $(n+1) \times (n+1)$ 矩阵：

$$g = \begin{pmatrix} A & b \\ 0 & 1 \end{pmatrix}$$

其中 $A \in \mathrm{SO}(n)$ 为旋转矩阵，$b \in \mathbb{R}^n$ 为平移向量。这一表示使得仿射连接可在平凡丛 $\mathbb{R}^{n+1} \to \mathbb{R}^n$ 上自然定义。

#### 2. 基础仿射连接

在平凡丛 $\mathbb{R}^{n+1} \to M$ 上，定义连接：

$$\overline{\nabla} := d - \begin{pmatrix} 0 & \mathrm{id} \\ 0 & 0 \end{pmatrix}$$

**变量含义**：该连接编码了沿微分方向的无穷小平移。具体而言，对于从 $p$ 出发的测地线 $\gamma$ 和 $\overline{\nabla}$-平行截面 $(Y, \lambda)$，有 $\nabla_{\gamma'} Y = \lambda \gamma'$ 且 $d_{\gamma'} \lambda = 0$。这意味着若初始条件为 $Y_p = 0$ 且 $\lambda_p = 1$，则沿测地线 $Y$ 线性增长，其长度恰等于测地距离——这正是对数映射的径向分量。

#### 3. 局部变体连接 (AHM_ℓ)

为在曲面上实际计算，AHM_ℓ 在 $TM \oplus \mathbb{R}$ 上构造连接，结合 Levi-Civita 连接 $\nabla$ 与重言 1-形式：

$$\nabla^{\ell} = \begin{pmatrix} \nabla & 0 \\ d & 0 \end{pmatrix} - \begin{pmatrix} 0 & \mathrm{id} \\ 0 & 0 \end{pmatrix}$$

**变量含义**：第一项 $\begin{pmatrix} \nabla & 0 \\ d & 0 \end{pmatrix}$ 提供切向量的旋转平行传输和标量分量的平凡外微分；第二项 $- \begin{pmatrix} 0 & \mathrm{id} \\ 0 & 0 \end{pmatrix}$ 引入平移耦合，使得平行截面沿测地线的切向分量线性增长。

**Lemma 1**（理论保证）：若 $(Y, \lambda)$ 满足 $Y_p = 0$、$\lambda_p = 1$，且沿所有通过 $p$ 的测地线 $\nabla^{\ell}$-平行，则 $Y = d_p(\gamma) \cdot \gamma' / |\gamma'|$ 且 $\lambda \equiv 1$。这意味着 $Y$ 的长度精确等于测地距离，无需任何数值微分。

#### 4. 离散仿射平行传输

在离散曲面网格上，边 $ij$ 上的 $\nabla^{\ell}$-平行传输为：

$$r_{ij}^{\nabla^{\ell}}(X_i) = r_{ij}^{\nabla} X_i + e_{ji}$$

**变量含义**：$r_{ij}^{\nabla}$ 为 Levi-Civita 连接的离散平行传输（由边向量比值 $r_{ij}^{\nabla} := -e_{ji}/e_{ij}$ 给出），$e_{ji}$ 为从顶点 $j$ 指向 $i$ 的边向量。该公式将旋转和平移统一编码：切向量部分经历标准旋转平行传输，齐次分量通过边向量累加实现平移。

#### 5. 仿射热扩散方程

采用单步反向欧拉法离散短时热方程：

$$(\mathsf{M} + \tau \mathsf{L}^{\nabla^{\ell}}) \binom{\mathsf{Y}}{\lambda} = \binom{0}{1} \delta_p$$

**变量含义**：$\mathsf{M}$ 为质量矩阵，$\mathsf{L}^{\nabla^{\ell}}$ 为基于上述离散平行传输构造的连接拉普拉斯矩阵，$\tau$ 为扩散时间步长（通常取 $\tau = h^2$，$h$ 为平均边长），$\delta_p$ 为源点 $p$ 处的 Dirac delta。右端源项仅在 $p$ 点非零，其切向分量为零、标量分量为 1——这恰好对应 Lemma 1 的初始条件。

#### 6. 对数映射提取

**AHM_ℓ**：求解上述方程得到径向场 $Y$ 后，需将其投影到从源点 $p$ 出发的全局一致切空间坐标系。通过向量热方法延拓 $p$ 处的正交标架 $\{E_i\}$ 得到测地线框架，对数映射由下式给出：

$$\mathbf{x}(q) = \big(\langle E_i(q), Y_q \rangle\big)_{i=1}^{n}$$

**AHM_a**（自适应变体）：直接构造适应于源点 $p$ 的仿射连接 $\overline{\nabla}^{\Phi}$，求解扩散后通过齐次坐标归一化得到对数映射：

$$\Phi_{\nu} := \mathbf{x}_{\nu} / \lambda_{\nu}$$

**变量含义**：$\mathbf{x}_{\nu}$ 和 $\lambda_{\nu}$ 分别为扩散解在顶点 $\nu$ 的切向分量和标量分量。除以 $\lambda$ 的操作本质上是将仿射扩散得到的“齐次坐标”投影回 $\mathbb{R}^n$，直接获得二维参数化。

### 计算管线模块

| 模块 | AHM_ℓ | AHM_a |
|------|-------|-------|
| **连接拉普拉斯构建** | 基于 $\nabla^{\ell}$ 的离散平行传输 $r_{ij}^{\nabla} X_i + e_{ji}$ | 基于适应源点的 $\overline{\nabla}^{\Phi}$（Equation 14） |
| **热扩散求解** | 单次反向欧拉求解 $(\mathsf{M} + \tau \mathsf{L}^{\nabla^{\ell}})$ | 同左，但矩阵依赖源点 |
| **测地线框架** | 需通过向量热方法延拓源点正交标架 | 不需要（连接本身已适应源点） |
| **对数映射提取** | 径向场投影到框架坐标 | 齐次坐标归一化 $\mathbf{x}/\lambda$ |

### 理论性质

**Lemma 3**（平直域精确性）：在欧几里得域上，AHM 可精确恢复恒等参数化（至浮点精度）。标量扩散的解为 $\tilde{\mathbf{x}}_i = 0$，平移后得到 $\mathbf{x}_i = z_i$（对所有顶点成立）。这解释了为何 AHM 在平直域上远优于 VHM_log（Figure 6）：VHM_log 在源点附近产生大量畸变，而 AHM 几乎完全复现 ground truth。

**边界行为**：由于热核的短时渐近展开不受边界强烈影响，AHM 在边界处自然实现正确的测地距离行为（Figure 4），与 Signed Heat Method（FC24）一致。

## 实验与关键发现

### 核心性能对比：度量畸变

仿射热方法（AHM）的核心优势在于其生成的对数映射具有显著更低的度量畸变。在多个三维模型上的对比实验（Figure 2）表明，AHM 的局部变体（AHM_ℓ）和自适应变体（AHM_a）在度量畸变指标 $\mathcal{D} = \max(1/\sigma_1, \sigma_2)$ 上均大幅优于先前方法，包括 **VHM_log**（Sharp et al., ACM Trans. Graph. 2019）、**SEM**（Herholz and Alexa, Comp. Graph. Forum 2019）和 **DEM**（Schmidt et al., ACM Trans. Graph. 2006）。特别值得注意的是，AHM 在源点处严格保持等距（$\mathcal{D}=1$），这与光滑情形下对数映射的理论性质一致——而 VHM_log 等方法在源点附近存在较大畸变。

在平直域上的对照实验（Figure 6）进一步揭示了方法间的本质差异：VHM_log 在源点附近产生大量畸变，而 AHM 的两个变体均可精确恢复恒等参数化（至浮点精度）。这一结果由 Lemma 3 从理论上保证——在欧几里得情形下，标量扩散的解给出零径向场，经平移后即得精确的对数映射坐标。

![[assets/figures/papers/paper_list_l34_https_www_yousufsoliman_com_projects_download_AffineHeatMethod_pdf/figures/009_Figure_6.jpg]]
*Figure 6: A Flat Comparison. Computing logarithmic maps using the vector heat method approach introduced in [SSC19] results in a large amount of distortion near the source point (bottom row); both versions our affine heat method result in much more accurate parameterizations, in the Euclidean case reproducing the ground truth (top row)*

### 测地距离精度

AHM 在源点邻域内的测地距离估计精度显著优于前馈热方法。Figure 20 的对比显示，在源点周围高亮区域内，AHM 的距离近似误差明显低于原始热方法 **HM**（Crane et al., 2013）和带符号热方法 **SHM**（Fayolle and Cazals, 2024）。这一优势源于 AHM 通过单一仿射扩散方程同时编码了方向与距离信息，避免了 HM/SHM 中通过数值微分从距离场提取方向分量所引入的精度损失。

### 收敛性分析

在 $S^2$ 球面序列网格上的收敛性实验（Figure 24）验证了方法的理论性质：AHM 的对数映射误差在 $L^2$ 和 $L^\infty$ 范数下均呈现线性收敛速率 $O(h)$，其中 $h$ 为网格平均边长。这一收敛行为与短时热核渐近展开的理论预期一致。

### 时间步长鲁棒性

Figure 13 展示了 AHM 对扩散时间步长 $\tau$ 的鲁棒性。与 VHM_log 相比，AHM 在跨越数个数量级的时间步长范围内均能提供准确的对数映射估计。VHM_log 在极短或极长扩散时间下性能显著退化，而 AHM 的仿射连接构造使其对 $\tau$ 的选择不敏感——论文中采用简单的启发式 $\tau = h^2$ 即可获得稳定结果。

![[assets/figures/papers/paper_list_l34_https_www_yousufsoliman_com_projects_download_AffineHeatMethod_pdf/figures/018_Figure_13.jpg]]
*Figure 13: Very Short and Long Time Diffusion. Compared to the method from [SSC19] (top), our affine heat method (bottom) provides accurate estimates of the log map across orders of magnitude of the time step used to estimate the heat kernels*

### 切割轨迹附近的平滑性

尽管曲面对数映射仅在源点的单射半径内有良好定义，AHM 在切割轨迹附近仍能产生全局连续的极坐标参数化。Figure 12 展示了即使在单射半径极小的源点处，AHM 也能提供平滑的角度坐标，且自适应变体 AHM_a 在切割轨迹附近的平滑性优于局部变体 AHM_ℓ。这一性质使 AHM 在实际应用中具有更强的实用性——许多下游任务需要全局连续的参数化，而非仅在单射半径内的严格对数映射。

### 网格质量鲁棒性

Figure 23 的鲁棒性实验表明，AHM 对低质量网格的容忍度显著优于 VHM_log 和 SEM。所有方法均基于内在 Delaunay 三角剖分构建扩散算子，但 AHM 的仿射连接构造在粗剖分几何体上仍能产生更准确的参数化。此外，Figure 14 证实使用内在 Delaunay 三角剖分可确保高质量参数化不受输入网格质量影响——这一特性对处理来自扫描或建模管线的非理想网格至关重要。

### 消融实验：局部变体 vs 自适应变体

两个变体在精度与效率间存在明确的权衡：

- **精度**：在单射半径内，AHM_ℓ 与 AHM_a 的参数化几乎不可区分（Figure 8）。但在切割轨迹附近，AHM_a 提供更平滑的角度坐标（Figure 12）。
- **计算效率**：单次求解耗时方面，AHM_ℓ 比 VHM_log 慢约 27%，AHM_a 则慢约 70%（Figure 22）。然而，AHM_ℓ 支持预分解加速：其完整矩阵分解可在多次求解中复用，显著降低重复求解的开销（Figure 22 底部）。相比之下，AHM_a 每次更改源点都需要重新计算连接拉普拉斯算子的符号分解（Figure 22 红色部分），限制了其在需要频繁更换源点的场景中的适用性。

### 径向向量场的各向同性

在各向异性网格上，AHM_ℓ 通过仿射扩散近似的径向向量场在归一化后，比 VHM_log 通过向量扩散得到的结果具有明显更好的各向同性（Figure 21）。这一性质对于依赖径向场方向信息的应用（如纹理映射、曲面参数化）尤为重要。

### 应用验证

AHM 的有效性在多个应用中得到了验证：

- **贴花放置**（Figure 17）：利用对数映射可轻松将几何图案放置到曲面上。
- **UV 平面化**（Figure 18）：即使在复杂曲面上，AHM 也能提供低畸变参数化；对于无法无缝参数化的曲面，用户可指定一组源点计算 Voronoi 区域上的极坐标。
- **笔触对齐参数化**（Figure 19）：沿曲线扩散指定的参数化可计算对齐的曲面参数化，UV 空间中到曲线的距离提供了到曲线测地距离的估计。
- **点云与多边形网格**（Figure 15, Figure 16）：方法自然泛化到点云和四边形网格等非标准离散几何表示。

![[assets/figures/papers/paper_list_l34_https_www_yousufsoliman_com_projects_download_AffineHeatMethod_pdf/figures/023_Figure_19.jpg]]
*Figure 19: Stroke-Aligned Parameterizations. Diffusing a parameterization specified along a curve provides a straightforward method for computing aligned surface parameterizations. Measuring the distance to the curve in UV space provides an estimate of the geodesic distance to the curve*

### 失败模式与局限性

尽管 AHM 表现优异，仍存在以下已知局限：

1. **自适应变体的计算开销**：AHM_a 对每个源点需要重新计算连接拉普拉斯算子的符号分解，在大规模网格或需要频繁更换源点的场景中构成瓶颈。
2. **仅支持度量定义的最短测地线**：方法只能沿由度量定义的最短测地线计算平行传输，无法泛化到任意仿射连接对应的对数映射。
3. **高维扩展未验证**：当前工作主要聚焦于二维曲面，三维及更高维的应用仍待探索。
4. **时间步长选择的极端情况**：虽然 $\tau = h^2$ 的启发式在大多数情况下有效，但在极端几何（如极细长三角形）下可能影响精度。

### 公平性说明

所有对比实验均采用相同的内在 Delaunay 三角剖分和相同的扩散时间步长 $\tau = h^2$（$h$ 为平均边长），确保了比较的公平性。VHM_log 和 SEM 也采用了内在 Delaunay 三角剖分以提升其基线性能。

## 定位与知识库关联

### 问题瓶颈与现有方法

曲面上从源点出发的对数映射（logarithmic map）同时编码了测地线方向与距离，是几何处理中的核心算子。现有基于热扩散的方法在构建该映射时面临两个关键瓶颈：

1. **源点附近的畸变**：**VHM_log**（Sharp et al., ACM Trans. Graph. 2019）通过向量热扩散近似平行传输，再经数值微分提取对数映射。由于短时向量扩散在源点邻域内对平移分量不敏感，该方法在源点附近产生显著畸变（见 Figure 6 平面域对比）。**SEM**（Herholz and Alexa, Comp. Graph. Forum 2019）将角度分量与距离分量分离计算，通过平滑指数映射避免显式平行传输，但分离策略引入了额外的近似误差。

2. **切割轨迹处的不连续性**：对数映射仅在单射半径内有严格定义，而**DEM**（Schmidt et al., ACM Trans. Graph. 2006）等基于显式径向追踪的方法在切割轨迹附近因法向偏差累积而产生扭曲参数化（Figure 25）。

### 核心因果机制

本文的关键洞察在于：**在连接拉普拉斯算子中引入齐次坐标，将旋转与平移统一表示为仿射连接**，使得短时热扩散能够直接同时编码测地线方向与距离。具体而言：

- 在平凡丛 $\mathbb{R}^{n+1} \to \mathbb{R}^n$ 上定义仿射连接 $\overline{\nabla} := d - \begin{pmatrix} 0 & \mathrm{id} \\ 0 & 0 \end{pmatrix}$，其平行截面沿测地线的演化恰为对数映射的线性增长（Equation 6）。
- 局部变体 **AHM_ℓ** 在 $TM \oplus \mathbb{R}$ 上构造连接 $\nabla^{\ell} = \begin{pmatrix} \nabla & 0 \\ d & 0 \end{pmatrix} - \begin{pmatrix} 0 & \mathrm{id} \\ 0 & 0 \end{pmatrix}$，结合 Levi-Civita 连接与重言 1-形式，通过单次仿射热扩散 $(M + \tau L^{\nabla^{\ell}}) \binom{Y}{\lambda} = \binom{0}{1} \delta_p$ 直接获得径向场 $Y$，其长度等于测地距离（Lemma 1），无需数值微分。
- 自适应变体 **AHM_a** 通过适应源点的测地线框架构造仿射连接 $\overline{\nabla}^{\Phi}$，可直接计算出对数映射本身（Equation 14-16）。

### 方法谱系定位

| 方法 | 核心机制 | 平移编码方式 | 源点畸变 | 切割轨迹鲁棒性 |
|------|---------|-------------|---------|--------------|
| **DEM** (Schmidt et al., 2006) | 显式径向追踪 | 逐步累加 | 累积误差 | 法向偏差累积 |
| **SEM** (Herholz & Alexa, 2019) | 分离角度扩散 | 距离与角度分离 | 分离近似误差 | 中等 |
| **VHM_log** (Sharp et al., 2019) | 向量热扩散 + 数值微分 | 仅旋转（Levi-Civita） | 显著畸变 | 依赖微分精度 |
| **AHM_ℓ** (本文) | 仿射热扩散 + 框架投影 | 旋转 + 平移（齐次坐标） | 等距保持 | 连续近似 |
| **AHM_a** (本文) | 自适应仿射热扩散 | 旋转 + 平移（适应框架） | 等距保持 | 更平滑的角度坐标 |

### 适用边界与局限

1. **计算开销**：AHM_a 对每个源点需重新计算连接拉普拉斯算子的符号分解，耗时比 VHM_log 多约 70%（Figure 22）。AHM_ℓ 支持预分解以加速重复求解，但需额外计算全局测地线框架。

2. **连接泛化能力**：本方法只能沿由度量定义的最短测地线计算平行传输，无法泛化到任意仿射连接的对数映射（Section 7）。

3. **维度限制**：当前工作聚焦于二维曲面，三维及更高维的应用仍待探索。

4. **扩散时间步长**：$\tau = h^2$（$h$ 为平均边长）的选择在极端几何下可能影响精度，尽管实验表明该方法在跨数量级时间步长下均保持鲁棒（Figure 13）。

### 开放问题

1. 是否可以将自适应变体重写为固定通用算子的形式，从而避免每次更改源点时重复分解矩阵？
2. 局部变体与自适应变体能否统一为某个非线性 PDE 的不动点迭代框架？
3. 能否将仿射热方法推广到计算任意仿射连接（非仅度量定义的最短测地线）对应的对数映射？
4. 如何开发直观的控制器，使得测地线概念可超出共形等价度量进行修改？
5. 如何自动确定用于分片 UV 平面化的源点最优配置？

## 原文 PDF

![[paperPDFs/SGP_2025/The_Affine_Heat_Method.pdf]]
