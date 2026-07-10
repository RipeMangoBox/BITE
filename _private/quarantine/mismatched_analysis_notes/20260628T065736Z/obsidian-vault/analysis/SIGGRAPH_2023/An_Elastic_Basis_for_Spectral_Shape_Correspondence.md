---
title: An Elastic Basis for Spectral Shape Correspondence
type: paper
paper_level: A
venue: SIGGRAPH
year: 2023
pdf_ref: paperPDFs/SIGGRAPH_2023/An_Elastic_Basis_for_Spectral_Shape_Correspondence.pdf
project_link: null
code_link: "https://gitlab.com/numod/goast"
aliases:
- RSSSGMTPE
- EBSSC
tags:
- SIGGRAPH_2023
- topic/representation_self_supervised_transfer
core_operator: 通过构建图形流形（graph manifold），将排斥势（切线点能量）作为额外的坐标维度嵌入形状空间，并修改黎曼度量，使得度量梯度惩罚排斥势的改变，从而引导路径倾向于保持恒定排斥势，自然避免碰撞。
primary_logic: 简单地在路径能量中加入排斥惩罚（如 Coulomb 势）会导致不合理的“爆炸”式变形（Figure 3）；而将排斥势提升为图形流形的一部分后，度量本身即鼓励路径保持安全的分离状态，测地线会在尽可能保持原始弹性变形的同时主动调整全局姿态以避免接触（Figure 15）。
claims:
- 直接最小化含排斥惩罚的路径能量会导致表面不必要的膨胀和变形（Figure 3, Section 2.2）
- 图形流形构造（Equation 5, Section 2.3）将排斥势纳入度量，使得测地线自然保持无碰撞
- 排斥壳空间中的测地线在插值手部网格时产生了无自相交且自然的弯曲变形，即使没有骨架（Figure 11）
- 与纯惩罚路径能量相比，图形流形方法保持了合理的形状（例如点集平移，Figure 7）
---

# An Elastic Basis for Spectral Shape Correspondence

> [!tip] 核心洞察
> 简单地在路径能量中加入排斥惩罚（如 Coulomb 势）会导致不合理的“爆炸”式变形（Figure 3）；而将排斥势提升为图形流形的一部分后，度量本身即鼓励路径保持安全的分离状态，测地线会在尽可能保持原始弹性变形的同时主动调整全局姿态以避免接触（Figure 15）。

| 字段 | 内容 |
|------|------|
| 中文题名 | 用于谱形状对应的弹性基础 |
| 英文题名 | An Elastic Basis for Spectral Shape Correspondence |
| 会议/期刊 | SIGGRAPH 2023 |
| Links | [paper](https://josuasassen.com/#publications) · [Code](https://gitlab.com/numod/goast) |
| Topic | #topic/representation_self_supervised_transfer |
| Method | Repulsive Shell Shape Space (Graph Manifold with Tangent-Point Energy) |
| Dataset | Hand interleaving interpolation, Armadillo roll / obstacle avoidance, Various mesh sequences, Nonrigid packing |

> [!tip] 效果简介
> - Hand interleaving interpolation 上，Qualitative (no self-intersection) Ours (repulsive shells): natural bending without intersection vs Elastic shells without repulsion: severe intersections (Intersection-free vs. intersecting)。
> - Armadillo roll / obstacle avoidance 上，Qualitative (deformation behavior) Proactive folding to avoid obstacle vs Forward simulation or no repulsion: no proactive avoidance (Proactive deformation emerges)。
> - Various mesh sequences (Fig 11,15,20,14) 上，Energy evaluation time (ms) Adaptive TPE (ours) vs IPC barrier energy (7–10× faster (Fig 16))。

## 概要

在黎曼形状空间中进行几何操作（插值、外推、平均）时，弹性壳等现有空间无法自动避免自相交，导致非物理的穿刺或需要昂贵的碰撞检测与解决。本文提出**排斥壳形状空间**：通过将排斥势（切线点能量）作为额外坐标维度嵌入形状空间，构造**图形流形**，并修改黎曼度量，使度量梯度惩罚排斥势的改变，从而引导测地线自然保持无碰撞。核心洞察是：简单地在路径能量中加排斥惩罚会导致表面不合理的“爆炸”式膨胀；而将排斥势纳入度量后，路径在尽可能保持弹性变形的同时主动调整姿态以避免接触。

实验表明，该方法在手部网格插值中产生无自相交的自然弯曲变形，无需骨架；在障碍物规避、非刚体打包、双曲面等距嵌入等任务中均能产生主动避碰行为。自适应多极子加速使切线点能量评估比 IPC 屏障能量快 7–10 倍。方法不提供离散情况下的严格无相交保证，对初始化敏感，且未实现自适应重网格化。

## 核心方法与创新机理

### 问题背景与唯一瓶颈

在几何处理与计算机图形学中，形状空间（shape space）为插值、外推、平均等操作提供了统一的黎曼框架。以**弹性壳空间**（Heeren et al., 2014）为代表的现有方法，通过定义膜能量与弯曲能量的组合构建黎曼度量，能够在形状之间产生自然的弹性变形轨迹。然而，这些方法存在一个根本性缺陷：**度量本身不包含任何排斥机制，导致测地线路径可以自由穿越自相交区域**。在手指交错、肢体折叠等紧密接触场景中，直接最小化弹性路径能量会产生严重的非物理穿刺（Figure 11, Figure 15 中间行）。

一个直观的补救思路是在路径能量中直接加入排斥势的积分惩罚项，例如 Coulomb 势或 IPC 障碍函数。但论文通过理论分析与实验揭示了这一策略的灾难性失败模式：**简单惩罚总排斥势会导致表面在路径中间“爆炸”式膨胀**，因为系统发现通过整体放大形状来降低排斥势比保持合理变形更“便宜”（Figure 3, Figure 7）。这表明排斥约束不能作为外部惩罚项施加，而必须内化到形状空间的几何结构中。

![[assets/figures/papers/paper_list_l19_https_josuasassen_com_publications/figures/002_Figure_3.jpg]]
*Figure 3: Simply penalizing the total repulsive potential over a time-varying trajectory yields undesirable deformation: between the fixed start/end configurations, the surface “explodes” away from itself to reduce potential*

### 核心创新：图形流形（Graph Manifold）构造

论文的核心创新是将排斥势从外部惩罚提升为形状空间的内在几何维度。具体而言，给定原始形状空间 $\mathcal{M}$ 及其黎曼度量 $g_{\mathbf{x}}$，选择一个排斥势函数 $\Phi: \mathcal{M} \to \overline{\mathbb{R}}$，构造**图形流形**：

$$\mathcal{M}^{\Phi} := \{ (\mathbf{x}, \Phi(\mathbf{x})) \mid \mathbf{x} \in \mathcal{M} \} \subset \mathcal{M} \times \overline{\mathbb{R}}$$

这一构造将排斥势作为额外的坐标维度嵌入，使得 $\mathcal{M}^{\Phi}$ 成为比原空间高一维的子流形。关键在于，图形流形上的自然黎曼度量在原始坐标上的诱导度量为：

$$g_{\mathbf{x}}^{\Phi}(u,v) := g_{\mathbf{x}}(u,v) + \beta \, \mathrm{d}_{\mathbf{x}}\Phi(u) \, \mathrm{d}_{\mathbf{x}}\Phi(v) \quad \text{(Equation 5)}$$

其中 $\beta > 0$ 控制排斥强度，$\mathrm{d}_{\mathbf{x}}\Phi(u)$ 是 $\Phi$ 沿切向量 $u$ 的方向导数。

**因果机制**：该度量的第二项惩罚排斥势的改变。当路径试图穿越自相交区域时，$\Phi$ 会急剧增大（因为切线点能量在自相交处趋于无穷），导致 $\mathrm{d}_{\mathbf{x}}\Phi(\dot{\mathbf{x}})$ 很大，从而路径能量急剧上升。因此，测地线会主动调整全局姿态以避免 $\Phi$ 的显著增加——这并非简单的局部碰撞响应，而是**度量梯度本身引导路径倾向于保持恒定排斥势**。Figure 15 清晰地展示了这一效应：在手指交错插值中，排斥壳空间的测地线不仅避免了局部接触，还改变了整体运动规划，使手腕自然弯曲以主动避让，而无需任何骨架驱动。

### 三个关键 Changed Slots

**Slot 1：黎曼度量——从纯弹性到弹性-排斥耦合**

| 维度 | 基线（弹性壳空间） | 本文方法 |
|------|-------------------|---------|
| 度量定义 | $g_{\mathbf{x}}(u,v)$（仅膜能量+弯曲能量） | $g_{\mathbf{x}}^{\Phi}(u,v) = g_{\mathbf{x}}(u,v) + \beta \, \mathrm{d}_{\mathbf{x}}\Phi(u) \mathrm{d}_{\mathbf{x}}\Phi(v)$ |
| 排斥建模 | 无 | 通过度量梯度内化 |
| 路径行为 | 可穿越自相交区域 | 主动避免 $\Phi$ 的显著变化 |

**Slot 2：路径能量——从路径积分惩罚到图形流形测地线**

基线方法若需排斥，只能在路径能量中加惩罚项 $\int \Phi(\mathbf{x}(t)) dt$，导致“爆炸”失效。本文的路径能量形式不变（$\int g_{\mathbf{x}}^{\Phi}(\dot{\mathbf{x}}, \dot{\mathbf{x}}) dt$），但度量本身已包含排斥信息。离散化后，路径能量近似为：

$$\widehat{\mathcal{E}}(\mathbf{x}) := n \sum_{k=1}^{n} D_{\Phi}^{2}(\mathbf{x}^{k-1}, \mathbf{x}^{k}) \quad \text{(Equation 6)}$$

其中近似平方距离为：

$$D_{\Phi}^{2}(\mathbf{x}, \mathbf{y}) := |\mathbf{x} - \mathbf{y}|^{2} + (\Phi(\mathbf{x}) - \Phi(\mathbf{y}))^{2} \quad \text{(Equation 7)}$$

对于弹性壳空间，第一项替换为弹性膜能量 $\widehat{\mathcal{W}}(\mathbf{x}, \mathbf{y})$（Equation 17）。这一离散化使得优化问题可直接用信赖域方法求解。

**Slot 3：排斥势评估——从全对求积到自适应多极子加速**

切线点能量（Tangent-Point Energy, TPE）的连续形式为：

$$\Phi(\mathbf{x}) := \int_{\Sigma} \int_{\Sigma} \frac{|\langle \mathbf{n}(x), x-y \rangle|^{\alpha}}{|x-y|^{2\alpha}} \mathrm{d}x \mathrm{d}y \quad \text{(Equation 13)}$$

该能量的关键性质是：**当且仅当表面无自相交时有限**，使其成为理想的排斥势。然而，直接离散化需要 $O(N^2)$ 的三角形对求积，计算代价过高。本文设计了**自适应求积+快速多极子方法（FMM）** 的混合策略：远场三角形对使用多极子近似，近场则根据 MAC 准则（Multipole Acceptance Criterion）自适应细分求积（Figure 13）。这一方案将复杂度降至 $O(n \log n)$，且相对误差约 0.1%（Section 5.3.1），比 Barnes-Hut 方法快 7–10 倍（Figure 16）。

### 方法模块与因果链路

完整流程包含以下模块，按执行顺序形成因果链：

1. **弹性壳能量计算**（Section 3.1）：计算膜能量与弯曲能量，构成基线度量 $g_{\mathbf{x}}$ 的基础。膜能量惩罚面内拉伸，弯曲能量惩罚法向变化，共同定义了“自然弹性变形”的先验。

2. **切线点能量计算**（Section 3.2, Section 5）：基于自适应 FMM 评估 $\Phi(\mathbf{x})$ 及其梯度 $\nabla \Phi$。这是排斥信息的唯一来源，其梯度通过 Equation 5 耦合进度量。

3. **图形流形路径能量组装**（Section 2.4, Section 4.2）：将弹性距离与排斥势差组合为 $D_{\Phi}^{2}$，构建离散路径能量 $\widehat{\mathcal{E}}$。这一模块是弹性先验与排斥约束的**唯一耦合点**——排斥不改变弹性行为本身，而是通过修改距离概念来引导路径选择。

4. **信赖域优化**（Section 6.1）：使用 Steihaug 共轭梯度法最小化 $\widehat{\mathcal{E}}$，求解插值测地线。初始化采用分段常数路径（端点+中间配置），通过逐步增加时间步数实现由粗到精的优化（Figure 30）。

5. **指数映射外推**（Section 6.2）：基于最优性条件逐步求解 $\mathbf{x}^{k+1}$，实现从初始运动方向的外推。该模块使得用户只需指定初始变形趋势，系统自动生成符合排斥度量的后续形变（Figure 27, Figure 28）。

6. **时空上采样**（Section 6.4）：对粗粒度轨迹和网格进行细化，提升视觉质量。

**因果链路总结**：TPE 评估提供排斥梯度 → 图形流形度量将排斥梯度与弹性度量耦合 → 路径能量最小化在弹性变形与排斥避让之间自动权衡 → 信赖域优化/指数映射生成无自相交轨迹。整个链路中，**排斥势仅通过度量梯度影响路径选择，不直接施加力或约束**，这是区别于传统惩罚方法的关键。

### 排斥势选择的消融证据

论文对比了两种候选排斥势在图形流形框架中的表现：

- **IPC 障碍函数**（Li et al., 2020）：作为 $\Phi$ 时，测地线出现突然“跳跃”（Figure 20 左），即使经过大量参数调整也难以获得平滑轨迹。原因在于 IPC 的对数障碍仅在极近距离产生显著梯度，缺乏中远距离的引导信息。

![[assets/figures/papers/paper_list_l19_https_josuasassen_com_publications/figures/029_Figure_20.jpg]]
*Figure 20: When using the IPC barrier as potential energy in our framework, we struggle to find geodesics without sudden “jumps” (more obvious in supplementary video), even with good initialization (top le ). Here using the IPC barrier energy for repulsion fails to yield a smooth surface eversion, even a er extensive parameter tuning (bo om three rows). A TPE-based formulation easily finds smooth trajectories without jumps (top right)*

- **切线点能量（TPE）**：提供从近到远的多尺度排斥梯度，使得测地线平滑且主动避让（Figure 20 右）。Figure 18 进一步表明，TPE 在无连续碰撞检测（CCD）的情况下仍能有效防止自相交，而 IPC 则会出现大面积穿透。

这一消融验证了 TPE 作为排斥势的优越性：其全局性、多尺度特性与图形流形的度量梯度机制高度契合。

### 边界条件与实现注意事项

- **自适应求积的必要性**：Figure 12 显示，若不加自适应细分，紧密接触区域的三角形对仅用中点求积会产生自相交。自适应策略（Figure 13）通过模拟无限层次细分解决了这一问题。

- **初始化敏感性**：优化对初始路径敏感，极端场景需多次调整参数（$\beta$、时间步数）逐步逼近。Figure 30 展示了分层优化策略可生成快速预览。

- **无严格离散保证**：论文明确指出不提供离散情况下的无相交理论保证，紧密接触时可能仍需精细调参。

- **边界曲面限制**：TPE 理论仅对无边界曲面保证有限性，带边界曲面在实践中表现良好但存在病态特例。

![[assets/figures/papers/paper_list_l19_https_josuasassen_com_publications/figures/031_Figure_23.jpg]]
*Figure 23: We can use our framework to faithfully visualize abstract metrics. Here we isometrically embed a large piece of the hyperbolic plane*

## 实验与关键发现

### 核心定性结果：无自相交的自然变形

论文的核心实验主张是：排斥壳空间中的测地线能够在**无骨架信息**的条件下，自动产生无自相交且保持局部几何特征的变形序列。最具代表性的例子是**手部网格的交错插值**（Figure 11）：给定两个手指交错姿态作为端点，排斥壳测地线产生了手指和手腕的自然弯曲以避开碰撞，而纯弹性壳空间中的测地线则出现严重穿透。这种“主动避碰”行为并非来自外部碰撞检测，而是由度量本身的结构诱导——测地线在尽可能保持弹性变形的同时，调整全局姿态以维持排斥势的恒定。

另一个展示方法独特性的例子是**球壳穿过窄管**（Figure 4）：排斥壳测地线在接近障碍物时**预先折叠**以通过狭窄通道，这与前向动力学模拟中“碰撞后才响应”的行为形成本质区别。类似地，**骆驼穿过针眼**（Figure 14）展示了极端压缩场景下，方法能将网格逐步压缩为柱状并通过极小开口，同时保持无相交。

在**衣物翻面**（Figure 26）任务中，排斥壳测地线自动产生了手指被拉入手套时的复杂反转动作，无需任何骨架或手动引导。**双兔装箱**（Figure 22）和**章鱼装箱**（Figure 21）展示了排斥势在非刚性打包中的全局组织能力：与仅防止穿透的碰撞方法（IDP）相比，排斥壳方法产生的打包结果具有更好的空间分布和特征保持。

### 关键消融实验

**1. 路径能量中直接惩罚排斥势的失败（Figure 3, Figure 7）**

这是论文最重要的消融：如果简单地在路径能量中加入排斥势的积分惩罚（类似在目标函数中加一个 Coulomb 势项），表面会在中间帧“爆炸”以降低总排斥能（Figure 3）。对于点集平移任务，直接惩罚导致点云膨胀而非平移（Figure 7）。这验证了将排斥势**嵌入度量**（而非作为外部惩罚）的必要性——图形流形构造（Equation 5）通过惩罚排斥势的**改变**而非绝对值来引导路径，从而避免了这种非物理行为。

**2. 自适应求积的必要性（Figure 12）**

如果不使用自适应求积（仅用三角形中点近似切线点能量），在接近接触时表面仍可能出现自相交（Figure 12）。自适应细分策略（Figure 13）对近接触三角形对进行层次化细分，是保证数值可靠性的关键模块。

**3. IPC 屏障作为排斥势的局限性（Figure 18, Figure 20）**

将 IPC 对数屏障能量替换切线点能量（TPE）作为图形流形中的 Φ 会导致两个问题：
- **无连续碰撞检测时的大面积穿透**（Figure 18）：IPC 的排斥力较弱，在没有 CCD 作为安全保障时无法有效防止自相交，而 TPE 在同样条件下仍能保持无碰撞。
- **轨迹中的突然跳变**（Figure 20）：在表面翻转任务中，IPC 势产生的测地线出现不连续的“跳跃”，即使经过大量参数调整也无法获得平滑轨迹；而 TPE 公式化则轻松找到平滑无跳变的解。

**4. 与体积流方法的比较（Figure 19）**

基于无散体积流的方法在近接触形状上因空间分辨率不足而失效，而排斥壳方法在相同场景下能产生无相交的插值。

**5. 排斥势对全局运动规划的影响（Figure 15）**

与骨架驱动动画和纯弹性壳测地线的对比表明，排斥度量**不仅解决局部近接触穿透，更改变了整体运动规划**：排斥壳测地线产生了完全不同的全局姿态序列，主动避免碰撞而非仅在接触时刻进行局部修正。

### 性能与计算效率

**切线点能量 vs. IPC 屏障**（Figure 16）：在四个典型测地线序列（手部交错、Figure 15、Figure 20 初始化、骆驼穿针）上，自适应 TPE 的能量评估时间比 IPC 屏障能量快 **7–10 倍**。值得注意的是，TPE 的评估成本与局部弹性能量相差不大（Figure 33），这使得全局排斥势在计算上是可行的。

**自适应多极子方案**（Section 5.3.1）：与 Barnes-Hut 方法（Yu et al., 2021a）相比，快速多极子方法（FMM）配合 MAC 准则实现了约 0.1% 相对误差下的 7–10 倍加速。远场相互作用通过多极子展开高效近似，计算成本由少量近场交互主导。

**层次化优化**（Figure 30）：尽管全时空优化涉及全对能量，分层方案（从分段常数初始化开始，逐步增加时间步数）能够提供快速预览，使方法在实际使用中可控。

### 失败模式与适用边界

**1. 离散情况下的无相交保证缺失**：论文明确承认不提供离散情况下的严格无相交保证。在多维紧密接触场景中，可能需要精细调整参数才能获得无穿透结果。

**2. 带边界曲面的理论局限**：切线点能量理论上仅对**无边界曲面**保证有限性（即当且仅当曲面无自相交时能量有限）。带边界曲面在实践中表现良好，但存在病态特例，方法对此缺乏理论保障。

**3. 初始化敏感性**：数值优化对初始化敏感。极端变形或紧密接触场景需要**逐步调整参数**（如逐步增加排斥强度 β），计算可能耗时数小时。例如，Figure 20 中 IPC 势的失败部分归因于初始化策略的困难。

**4. 无自适应重网格化**：方法未实现自适应重网格化，在大剪切滑动变形时可能产生几何失真。三角形质量下降会影响弹性壳能量和切线点能量的数值精度。

**5. 排斥势对锐利特征的抑制**：切线点能量的全局排斥特性已知会抑制锐利弯曲和褶皱的形成。这在需要保持尖锐几何特征的场景中可能是不利因素。

**6. 排斥壳 vs. 纯弹性壳的定性边界**（Figure 31）：弯曲刚度与排斥力之间的相互作用显著影响最优轨迹。较强的弯曲刚度（Figure 31 top）与较弱的刚度（bottom）产生不同的变形行为，表明方法的行为受弹性参数与排斥参数耦合的影响，需要针对具体场景进行调节。

**7. 双曲平面等距嵌入的消融**（Figure 24）：去除排斥项后，等距嵌入产生大面积自相交（left）；加入长程排斥力不仅消除相交，还促进了全局对称性（center, right）。但最终嵌入的等距性仍需通过共形展平进行验证（bottom right），表明排斥势的引入可能对等距性产生间接影响。

## 定位与知识库关联

本文的核心贡献在于**将碰撞避免从路径能量的外挂惩罚项提升为形状空间度规的内建几何结构**。这一改变对应知识库中一个明确的 slot 替换：

**改变的 slot：形状空间的黎曼度规**

- **Baseline 值**：弹性壳空间（Elastic Shell Shape Space, Heeren et al., 2014）使用纯弹性度规 $g_{\mathbf{x}}(u,v)$ 度量形状变化成本。该度规仅编码膜应变和弯曲应变，对自相交无感知。
- **Proposed 值**：通过图形流形（graph manifold）构造，将排斥势 $\Phi$ 的微分信息嵌入度规：$g_{\mathbf{x}}^{\Phi}(u,v) := g_{\mathbf{x}}(u,v) + \beta \, \mathrm{d}_{\mathbf{x}}\Phi(u) \, \mathrm{d}_{\mathbf{x}}\Phi(v)$（Equation 5）。度规梯度直接惩罚排斥势的改变量，而非势的绝对值。

这一 slot 替换的**因果机制**在于：传统方法若在路径能量中加性惩罚总排斥势 $\int \Phi(\mathbf{x}(t)) dt$，会导致表面为降低势能而整体“爆炸”式膨胀（Figure 3, Figure 7）；而图形流形将排斥势作为额外维度嵌入形状空间后，度规本身即引导测地线保持恒定排斥势，从而在尽可能保留原始弹性变形的同时主动调整全局姿态以避免接触（Figure 15）。

**与知识库中已有工作的关系定位：**

1. **弹性壳形状空间（Heeren et al., 2014）**：本文直接继承其弹性壳能量作为基础度规 $g_{\mathbf{x}}$（膜应变 + 弯曲项），但该基线无法处理自相交。本文的贡献是在不改变弹性先验的前提下，通过度规增广引入排斥行为。

2. **IPC 障碍函数（Li et al., 2020）**：IPC 提供对数碰撞障碍，依赖连续碰撞检测（CCD）作为安全网。本文将其作为可选的 $\Phi$ 进行对比实验，发现 IPC 障碍函数在图形流形框架中会导致轨迹出现突然“跳跃”（Figure 20），且无 CCD 时仍产生大量自相交（Figure 18）。这表明**排斥势的光滑性对图形流形方法至关重要**——切线点能量（TPE）的全局光滑性使其天然适配度规嵌入。

3. **静态切线点能量计算（Yu et al., 2021a）**：本文在 TPE 的数值计算上进行了关键改进，用自适应多极子方法（FMM）替代 Barnes-Hut 近似，实现 7–10× 加速（Figure 16），相对误差约 0.1%。这一高效计算使得 TPE 在时空优化中的反复评估成为可能。

**知识库挂载点：**

- **几何处理与形状空间**：本文可挂载在“弹性形状空间”节点下，作为其“碰撞感知扩展”。它提供了一种通用框架——任何具有光滑排斥势的形状空间均可通过图形流形构造获得无碰撞测地线。
- **物理模拟与碰撞处理**：与 IPC 等基于局部障碍函数的接触方法形成互补。本文的全局排斥势适合离线形状插值与规划，而 IPC 更适合动态仿真中的精确接触解决。
- **数值优化**：本文的信任区域优化 + Steihaug CG 求解器、分层初始化策略（Figure 30）可挂载为“大规模时空优化”的参考实现。

**适用边界与限制：**

1. **无严格无相交保证**：论文明确承认在离散情况下不提供无碰撞的严格证明，这是一个需要后续工作填补的理论缺口。
2. **边界曲面的病态特例**：切线点能量理论上仅对无边界曲面保证有限性，带边界曲面在实践中表现良好但存在理论风险。
3. **计算成本与初始化敏感**：极端变形或紧密接触场景需要逐步调整参数，可能耗时数小时；未实现自适应重网格化，大剪切滑动时可能产生几何失真。
4. **排斥势抑制锐利特征**：TPE 的全局排斥特性可能抑制尖锐弯曲和褶皱的形成，这是该势函数的已知缺陷。

**后续启发：**

- 若能在离散设置下建立严格的无相交保证，该方法可成为几何处理中碰撞避免的标准工具。
- 图形流形框架具有通用性——任何光滑排斥势（如静电势、Wasserstein 距离等）均可嵌入，为不同应用定制排斥行为。
- 结合降阶模型或参数化表示可大幅降低计算成本，有望将方法从离线场景推向交互式应用。
- 无碰撞上采样问题在当前框架下尚未解决，是直接可操作的后续方向。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2023/An_Elastic_Basis_for_Spectral_Shape_Correspondence.pdf]]