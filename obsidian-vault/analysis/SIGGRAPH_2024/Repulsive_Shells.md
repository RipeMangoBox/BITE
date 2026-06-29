---
title: Repulsive Shells
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/Repulsive_Shells.pdf
project_link: null
code_link: null
aliases:
- RS
tags:
- SIGGRAPH_2024
- topic/benchmarks_datasets_evaluation
core_operator: 通过在原有黎曼度量中融入排斥势能的变化率（即图流形/graph manifold 构造），而非直接惩罚势能本身，从而避免轨迹中部的过度形变，并将碰撞规避编码为度量的一阶属性。
primary_logic: 将排斥势能作为形状空间上的附加维度，构建图流形(graph manifold)并以其度量定义路径能量，使碰撞避免自然地嵌入黎曼结构中；配合自适应切点能量(adaptive TPE)数值求积，既能在粗网格上可靠防止相交，又能收敛到有意义的连续极限能量。
claims:
- 图流形构造通过在度量中加入排斥势能的变化率，避免直接惩罚势能导致的轨迹中部爆炸，并将碰撞规避编码为度量的一阶属性。
- 自适应切点能量求积能够可靠地在粗网格上防止自相交，并随空间细化收敛到有意义的连续能量，而固定中点求积方案无法捕捉关键奇点，导致相交。
- 排斥壳空间上的测地线插值和指数映射能够主动（而非被动反应）避免碰撞，产生自然的全局形变，且无需骨骼绑定或数据集训练。
- 长程切点能量在形状空间任务中优于局部 IPC 障碍方法，提供更好的全局引导且计算成本在多数场景中相当或更低。
---

# Repulsive Shells

> [!tip] 核心洞察
> 将排斥势能作为形状空间上的附加维度，构建图流形(graph manifold)并以其度量定义路径能量，使碰撞避免自然地嵌入黎曼结构中；配合自适应切点能量(adaptive TPE)数值求积，既能在粗网格上可靠防止相交，又能收敛到有意义的连续极限能量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 排斥壳空间：面向碰撞感知几何处理的形状空间框架 |
| 英文题名 | Repulsive Shells |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://www.cs.cmu.edu/~kmcrane/Projects/RepulsiveShells/index.html) |
| Topic | #topic/benchmarks_datasets_evaluation |
| Method | Repulsive Shells |
| Dataset | Hand interleaving interpolation, Camel through needle, Interpolation comparison, Energy evaluation timing |

> [!tip] 效果简介
> - Hand interleaving interpolation (Figure 11) 上，intersection-free natural motion Repulsive Shells (adaptive TPE) vs Elastic shells (无自相交，手指/手腕自然弯曲以规避碰撞)。
> - Camel through needle (Figure 14) 上，collision-free compression Repulsive Shells vs Elastic shells (主动折叠以适应狭窄管道，避免穿透)。
> - Interpolation comparison (Figure 15) 上，motion quality and collision avoidance Repulsive Shells vs Skeletal rig / elastic shells (全局运动计划改变，主动规避碰撞而非仅处理接触瞬间)。

## 概要

现有形状空间将曲面视为浸入，允许自相交，导致插值、外推、平均等几何操作产生非物理的交叠。若直接在路径能量上累加排斥势能，则会引起轨迹中部不自然的“爆炸”式扩张。本文提出**排斥壳空间**（Repulsive Shells）框架，核心思路是将排斥势能作为形状空间上的附加维度，构造**图流形**（graph manifold），以其黎曼度量定义路径能量，使碰撞避免自然地内嵌于度量的一阶属性中，而非直接惩罚势能本身。配合**自适应切点能量**（adaptive TPE）数值求积方案，利用BVH与快速多极方法在无限剖分上懒惰求积，既能在粗网格上可靠防止自相交，又能收敛到有意义的连续极限能量。

实验表明，排斥壳空间上的测地线插值和指数映射能够**主动规避碰撞**，产生自然的全局形变（如双手穿插时手指自然弯曲、骆驼主动折叠穿过狭窄管道），无需骨骼绑定或数据集训练。与局部IPC障碍方法相比，TPE提供更好的长程引导且计算成本在多数场景中相当或更低。该方法在形状插值、外推、加权平均、等距嵌入及无相交打包等任务上均展现出优于传统弹性壳空间和直接惩罚方案的结果。

## 核心方法与创新机理

### 问题本质：为什么形状空间需要“排斥”？

现有基于物理的形状空间（如弹性壳度量空间）将曲面视为浸入（immersions），其黎曼度量仅编码弹性形变代价，天然允许自相交。当执行插值、外推、平均等几何任务时，生成的轨迹可能产生非物理的交叠——例如手指穿透手掌、衣物穿过自身。一个直觉方案是直接在路径能量上累加排斥势能作为惩罚项：

$$\widetilde{\mathcal{E}}^\Phi(\mathbf{x}) := \int_0^1 g_{\mathbf{x}(t)}(\dot{\mathbf{x}}(t), \dot{\mathbf{x}}(t)) \mathrm{d}t + \beta \int_0^1 \Phi(\mathbf{x}(t)) \mathrm{d}t$$

但这一方案存在根本缺陷：优化器会通过让轨迹中部的曲面“爆炸”式扩张来降低总势能，而非保持形状平移以规避碰撞。图 3 和图 7 分别展示了曲面和点云场景下的这种失败行为——固定端点间，表面无端膨胀以减小排斥能量，产生完全违背物理直觉的形变。

**核心瓶颈**在于：直接惩罚势能值本身，将碰撞规避编码为路径能量的零阶量，导致优化器找到的“捷径”是整体改变形状尺度而非局部调整姿态。

### 核心创新：图流形构造——将碰撞规避编码为度量的一阶属性

本文的核心洞察是：**不应惩罚排斥势能的值，而应惩罚排斥势能的变化率**。具体而言，将排斥势能 $\Phi$ 作为形状空间上的附加维度，构造图流形（graph manifold），并以该流形的度量定义路径能量。这样，碰撞规避被编码为黎曼度量的一阶属性，而非路径能量的零阶惩罚项。

**图流形度量**定义为：

$$g_{\mathbf{x}}^{\Phi}(u,v) := g_{\mathbf{x}}(u,v) + \beta \, \mathrm{d}_{\mathbf{x}}\Phi(u) \, \mathrm{d}_{\mathbf{x}}\Phi(v)$$

其中：
- $g_{\mathbf{x}}$ 是原始形状空间上的弹性壳度量（膜能量+弯曲能量）；
- $\mathrm{d}_{\mathbf{x}}\Phi(u)$ 是排斥势能沿切向量 $u$ 的方向导数；
- $\beta > 0$ 是排斥强度参数，控制弹性形变与排斥力之间的平衡。

这一构造的因果机制如下：
1. **距离下界保证**：图流形上的黎曼距离满足 $\mathrm{dist}_{\Phi}(x, y) \geq |\Phi(y) - \Phi(x)|$。这意味着，若某配置 $\mathbf{y}^*$ 具有无穷大的排斥势能（即自相交状态），则从任何有限势能配置 $\mathbf{x}$ 到 $\mathbf{y}^*$ 需要无穷大的距离——排斥壳空间中的测地线永远不会触及自相交状态。
2. **一阶惩罚避免爆炸**：度量仅惩罚势能的*变化*，而非势能绝对值。当曲面平移以规避碰撞时，势能变化率在接近接触区增大，但度量不会驱使曲面整体膨胀（因为膨胀本身也改变势能，产生额外代价）。图 6 用点云示例对比了直接最小化路径长度（产生碰撞）与图流形测地线（自然规避碰撞且保持尽可能直的轨迹）。
3. **主动规避而非被动响应**：图流形上的测地线最小化的是整个轨迹的累积形变代价（弹性+排斥变化），因此会*提前*调整姿态以规避碰撞，而非像前向动力学模拟那样仅在接触瞬间产生响应（图 4）。

### 关键 Changed Slot 1：黎曼度量替换

| 组件 | 基准方案 | 本文方案 |
|------|----------|----------|
| 形状空间度量 | $g$（弹性壳度量） | $g^{\Phi}$（图流形度量） |

这一替换是框架的理论核心。图 8 通过两个排斥点的形状空间可视化，直观对比了局部惩罚方案与图流形方案的差异：图流形将排斥势能作为附加维度“图化”到原空间上，使可行域（无相交配置）的边界位于无穷远处。

### 关键 Changed Slot 2：排斥势能离散化

| 组件 | 基准方案 | 本文方案 |
|------|----------|----------|
| TPE 求积 | 中点求积（Yu et al. 2021a） | 自适应切点能量 + 快速多极方法 + 懒惰无限剖分 |

切点能量（Tangent-Point Energy, TPE）定义为：

$$\Phi(\mathbf{x}) := \int_{\Sigma}\int_{\Sigma} \frac{|\langle \mathbf{n}(x), x-y \rangle|^\alpha}{|x-y|^{2\alpha}} \, \mathrm{d}x \, \mathrm{d}y$$

该能量对封闭曲面有严格的排斥性：当曲面自相交时能量趋于无穷大。但直接使用中点求积离散化存在致命缺陷——当两个三角形接近平行且距离极小时，中点求积无法捕捉核函数的奇异性，导致粗网格上出现自相交（图 12）。

本文的自适应求积方案通过以下机制解决该问题：
1. **BVH 加速的近接触检测**：利用包围体层次结构快速识别彼此接近的三角形对。
2. **懒惰无限剖分**：对接近接触的三角形对进行递归剖分，直到子三角形满足精度准则，而非预先固定剖分深度。
3. **快速多极方法（FMM）**：对远场相互作用采用零阶多极近似：

$$\Phi(U_1,U_2) = \mathrm{area}(U_1)\mathrm{area}(U_2) \frac{|\langle \overline{\mathbf{n}}(U_1), c(U_1)-c(U_2) \rangle|^\alpha}{|c(U_1)-c(U_2)|^{2\alpha}}$$

多极接受准则（MAC）为：

$$\max\{ \mathrm{diam}(U_1), \mathrm{diam}(U_2) \} \le \theta \, \mathrm{dist}(\mathrm{conv}(U_1), \mathrm{conv}(U_2))$$

其中 $\theta=1/4$ 时相对误差约 0.1%，且远场相互作用仅占总计算时间的约 5%（图 16）。

该方案是首个同时满足两个条件的 TPE 离散化：（i）在粗网格上可靠防止碰撞；（ii）在空间细化下收敛到有意义的连续极限能量（图 17）。

### 方法流水线与模块因果关系

整个框架包含六个核心模块，按执行逻辑组织如下：

**模块 1：图流形构造**
- 输入：原始形状空间 $\mathcal{M}$（配备弹性壳度量 $g$）、排斥势能 $\Phi$
- 操作：按 $g^{\Phi}$ 定义构造图流形 $\mathcal{M}^{\Phi}$
- 输出：碰撞感知的形状空间，其中自相交状态位于无穷远距离处

**模块 2：自适应切点能量求积**
- 输入：曲面三角剖分、当前配置 $\mathbf{x}$
- 操作：BVH 遍历检测近接触三角形对 → 懒惰递归剖分近接触对 → FMM 处理远场相互作用
- 输出：$\Phi(\mathbf{x})$ 及其梯度、Hessian 的精确近似
- 因果链接：该模块为模块 1 的度量提供 $\mathrm{d}\Phi$ 信息，为模块 3 的优化提供能量与导数

**模块 3：离散测地线路径能量最小化**
- 输入：$n+1$ 个时间采样点的初始配置序列 $\mathbf{x}^0, \ldots, \mathbf{x}^n$
- 目标函数：离散路径能量

$$\widehat{\mathcal{E}}(\mathbf{x}) := n \sum_{k=1}^n \mathrm{dist}_{\Phi}^2(\mathbf{x}^{k-1}, \mathbf{x}^k)$$

其中平方距离近似为：

$$D_{\Phi}^2(\mathbf{x}, \mathbf{y}) := |\mathbf{x} - \mathbf{y}|^2 + (\Phi(\mathbf{x}) - \Phi(\mathbf{y}))^2$$

- 优化方法：信赖域牛顿法，采用 Gauss-Newton Hessian 近似和分块对角预条件子
- 关键性质：$D_{\Phi}^2$ 的 Hessian 在 $\mathbf{y}=\mathbf{x}$ 处恰好等于图流形度量 $g^{\Phi}$，保证离散能量与连续路径能量的一阶一致性
- 因果链接：该模块利用模块 2 提供的 $\Phi$ 值计算 $D_{\Phi}^2$，利用模块 1 的度量结构保证优化方向正确

**模块 4：时空分层优化**
- 时间升采样：在粗时间轨迹的相邻配置间插入新配置，以当前解为初始化继续优化
- 空间升采样：通过最接近点投影将粗网格解传递到细网格
- 因果链接：图 30 表明粗时间预览高度预测最终结果，使分层策略高效可行——先在少数时间步上获得近似解，再逐步细化

**模块 5：指数映射外推**
- 输入：初始配置 $\mathbf{x}^0$、初始速度方向（由 $\mathbf{x}^0 \to \mathbf{x}^1$ 定义）
- 方法：沿图流形测地线以恒定速度前进，逐步求解非线性方程：

$$(\mathbf{x}^{k-1} - 2\mathbf{x}^k + \mathbf{x}^{k+1}) + (\Phi(\mathbf{x}^{k-1}) - 2\Phi(\mathbf{x}^k) + \Phi(\mathbf{x}^{k+1})) \mathsf{d}_{\mathbf{x}^k}\Phi = 0$$

- 输出：一系列自然外推的配置，逐渐接近但不触及自相交状态（图 28：叶子卷曲）

**模块 6：Karcher 均值加权平均**
- 输入：多个目标配置及权重
- 方法：变分求解流形上的 Fréchet 均值，最小化到各目标配置的图流形距离平方和
- 输出：无相交的加权平均形状
- 因果链接：图 1 右侧展示了三个姿态的测地线重心插值结果

### 排斥势能的选择与边界条件

本文主要采用切点能量（$\alpha=2$）作为排斥势能，其对封闭曲面有严格排斥性理论保证。对于带边界曲面，虽然缺乏严格证明，但实践中表现良好。切点能量会引入非局部弯曲正则化效应——它在惩罚接近接触的同时也惩罚高曲率，这可能抑制尖锐褶皱的形成（图 25 中增加膜刚度可产生皱褶以逼近等距嵌入，验证了度量保持能力）。

排斥强度参数 $\beta$ 需手动调节：过小导致碰撞规避不足，过大则过度约束形变。图 31 展示了不同弯曲刚度下同一障碍场景的行为差异，揭示了弹性力与排斥力之间的相互作用对最优轨迹的影响。

### 与 IPC 障碍方法的本质区别

增量势接触（IPC）方法使用对数障碍函数防止碰撞，依赖连续碰撞检测（CCD）作为安全保障。当将 IPC 障碍直接用作 $\Phi$ 时，框架难以找到平滑测地线——轨迹出现突然“跳跃”（图 20），即使在良好初始化下也无法完成光滑的曲面外翻。根本原因在于 IPC 障碍是局部、短程的排斥力，缺乏 TPE 的长程全局引导能力。图 18 进一步表明：无 CCD 时 IPC 惩罚可导致大范围自相交，而自适应 TPE 在同等条件下仍能防止碰撞。

![[assets/figures/papers/paper_list_l32_https_www_cs_cmu_edu_kmcrane_Projects_RepulsiveShells_index_html/figures/029_Figure_20.jpg]]
*Figure 20: When using the IPC barrier as potential energy in our framework, we struggle to find geodesics without sudden “jumps” (more obvious in supplementary video), even with good initialization (top left). Here using the IPC barrier energy for repulsion fails to yield a smooth surface eversion, even after extensive parameter tuning (bottom three rows). A TPE-based formulation easily finds smooth trajectories without jumps (top right)*

![[assets/figures/papers/paper_list_l32_https_www_cs_cmu_edu_kmcrane_Projects_RepulsiveShells_index_html/figures/031_Figure_23.jpg]]
*Figure 23: We can use our framework to faithfully visualize abstract metrics. Here we isometrically embed a large piece of the hyperbolic plane*

## 实验与关键发现

### 一、核心实验：碰撞规避与全局形变质量

排斥壳空间的核心价值在于将碰撞规避从“被动响应”转变为“主动规划”。Figure 11 的双手手指穿插插值实验最直观地验证了这一点：在仅给定起始和终止姿态（均为无自相交配置）的条件下，排斥壳测地线自动产生手指和手腕的自然弯曲，以规避穿插过程中的近接触碰撞，整个过程无需任何骨骼绑定或数据集训练。相比之下，传统弹性壳测地线在相同输入下出现严重的自相交。Figure 14 的“骆驼穿针”实验进一步展示了这种主动规避能力——球面壳在通过狭窄圆柱管时主动折叠自身，而非像前向动力学模拟那样仅在碰撞发生后才产生形变响应（Figure 4）。

Figure 15 的消融对比揭示了排斥度量的深层作用：骨架驱动插值（skeletal rig）仅在接触瞬间处理局部碰撞，而排斥壳测地线改变了整个运动计划（motion plan），产生全局姿态的差异以主动规避相交。这说明排斥势能通过图流形度量编码后，影响的不是局部修补，而是轨迹的全局几何结构。

![[assets/figures/papers/paper_list_l32_https_www_cs_cmu_edu_kmcrane_Projects_RepulsiveShells_index_html/figures/023_Figure_15.jpg]]
*Figure 15: Interpolation between far-left and far-right poses, using a skeletal rig (top), a geodesic in the space of elastic shells (center), and a geodesic in our repulsive shell space (bottom). Notice that the repulsive metric does not merely resolve local intersections near moments of contact—rather, it alters the overall motion plan, yielding different global poses that proactively avoid intersection*

### 二、自适应切点能量的决定性作用

自适应切点能量（adaptive TPE）求积方案是方法可行性的关键工程支柱。Figure 12 的消融实验表明：在粗网格上，固定中点求积（midpoint quadrature）的 TPE 无法阻止自相交，即使网格加密也未能解决；而自适应方案在相同粗网格上即可可靠防止相交。Figure 17 进一步量化了自适应方案在 0 维（点接触）、1 维（线接触）和 2 维（面接触）近接触场景下的计算成本与精度——能量随空间细化收敛到有意义的连续极限，而固定求积方案无法捕捉奇点附近的能量贡献。

在计算效率方面，Figure 16 的计时对比显示：在多数实验场景中，自适应 TPE 的求值速度快于 IPC 障碍能量，且远场相互作用（通过快速多极方法处理）仅占总计算时间的约 5%。多极展开参数 θ = 1/4 时，相对误差约 0.1%，精度与效率取得良好平衡。

### 三、与 IPC 障碍方法的系统对比

IPC（Incremental Potential Contact）作为当前主流的碰撞处理方法，在排斥壳框架中作为替代势能时暴露出根本性局限。Figure 20 的关键消融显示：使用 IPC 障碍作为排斥势能 Φ，即使有良好的初始化，也无法找到光滑的曲面外翻（eversion）轨迹——轨迹出现突然的“跳跃”（supplementary video 中更明显），且经大量参数调优后仍失败。而基于 TPE 的排斥壳方法轻松找到平滑、无跳跃的外翻轨迹。

Figure 18 揭示了 IPC 的另一脆弱点：IPC 依赖连续碰撞检测（CCD）作为安全网，因为其对数障碍仅提供微弱的排斥力；在无 CCD 的情况下，IPC 惩罚会导致大范围自相交。自适应 TPE 在相同条件下仍能有效防止碰撞，无需昂贵的 CCD 检查。

然而，TPE 并非在所有方面都优于 IPC。Figure 21 的章鱼装箱实验表明，长程排斥势能产生的打包结果与纯碰撞驱动的打包（inset，使用参考 IDP 代码）有质的区别：前者产生良好分离的全局排列并保留局部几何特征，后者仅防止穿透但可能无法得到良好的全局布局。这说明两种方法适用于不同的设计目标。

![[assets/figures/papers/paper_list_l32_https_www_cs_cmu_edu_kmcrane_Projects_RepulsiveShells_index_html/figures/030_Figure_21.jpg]]
*Figure 21: Progressively packing an octopus (top left) into a small box (bottom right) with a long-range repulsive potential yields a well-separated packing that nicely preserves local geometric features. The result is qualitatively different from a collision-based packing (inset, using reference IDP code), which prevents interpenetration but may not yield a nice global arrangement*

### 四、应用场景验证

**形状外推**（Figure 27、28、32）：排斥壳指数映射能够从简单姿态出发，通过外推产生更复杂的无相交配置。Figure 27 展示了两根圆柱的缠绕外推——无排斥项时圆柱会相互穿透并分离，排斥壳则产生紧密缠绕。Figure 32 展示了从易于建模的分离手指姿态出发，外推得到手指紧密贴合的无相交姿态，验证了该方法在建模辅助中的实用价值。

**等距嵌入**（Figure 23-25）：排斥壳框架可忠实可视化抽象度量。Figure 23 展示了双曲平面的大片等距嵌入，排斥项避免了自相交（Figure 24 左：无排斥项时出现大范围相交），同时长程排斥力促进了全局对称性（Figure 24 中、右）。Figure 25 的环面平坦度量近等距嵌入中，增加膜刚度可产生皱褶，逼近真实等距嵌入，验证了框架的度量保持能力。

**衣物翻面**（Figure 26）：排斥壳测地线实现了衣物从反面到正面的自然外翻，手指被拉入手套时指尖反转等复杂无相交形变自然涌现，无需专门设计。

### 五、失败模式与适用边界

1. **离散无相交保证的缺失**：尽管自适应 TPE 在实践中可靠，但论文明确指出离散情况下未提供严格的无相交保证。粗网格上可能残留小相交，空间升采样后在紧密接触区域可能出现局部穿透。这是该方法的理论边界，需要人工验证。

2. **排斥强度参数 β 的手动调节**：β 需手动平衡弹性形变与排斥力（Figure 31 展示了不同弯曲刚度下同一障碍场景的行为差异），缺乏自动选择机制。

3. **切点能量的非局部弯曲正则化**：TPE 可能抑制尖锐褶皱的形成，这在需要精细折痕的应用中构成限制。

4. **带边界曲面的理论保证缺失**：切点能量仅对无边界的封闭曲面有严格排斥性证明，带边界曲面在实践中表现良好但缺乏理论保证。

5. **初始化依赖**：复杂场景仍需人工提供中间姿态（尽管简单初始化方案已足够应对多数情况），且当前框架要求输入网格具有固定拓扑连接关系。

6. **高维近接触场景的优化性能**：在极近距离接触的高维场景中，当前的弹性 Hessian 预条件子可能性能不足。

![[assets/figures/papers/paper_list_l32_https_www_cs_cmu_edu_kmcrane_Projects_RepulsiveShells_index_html/figures/026_Figure_19.jpg]]
*Figure 19: Methods based on injectively deforming the space around an object can struggle with shapes in near-contact due to insufficient spatial resolution. Here we compare shape interpolation via our method (top) versus a method based on divergence-free volumetric flows (bottom)*

![[assets/figures/papers/paper_list_l32_https_www_cs_cmu_edu_kmcrane_Projects_RepulsiveShells_index_html/figures/002_Figure_3.jpg]]
*Figure 3: Simply penalizing the total repulsive potential over a time-varying trajectory yields undesirable deformation: between the fixed start/end configurations, the surface “explodes” away from itself to reduce potential*

## 定位与知识库关联

**Repulsive Shells** 的核心定位是将碰撞避免从“后处理约束”或“路径能量惩罚项”提升为形状空间黎曼度量的一阶属性。在知识库中，它占据**基于物理度量的形状空间**与**无相交几何处理**两条主线的交汇点，并改变了现有形状空间框架中“度量定义”这个关键槽位。

### 相对于现有工作的槽位改变

现有弹性形状空间（如 **Heeren et al., 2012, 2014** 的弹性壳度量框架）将曲面视为浸入（immersions），其黎曼度量 $g$ 仅编码弹性形变的代价，允许轨迹中出现自相交。Repulsive Shells 将该槽位从 $g$ 替换为图流形度量 $g^{\Phi}$：

$$g_{\mathbf{x}}^{\Phi}(u,v) := g_{\mathbf{x}}(u,v) + \beta \, \mathrm{d}_{\mathbf{x}}\Phi(u) \, \mathrm{d}_{\mathbf{x}}\Phi(v)$$

这一替换的因果效应是：排斥势能的变化率（而非势能本身）被编码为度量的一阶量，从而在测地线插值、指数映射外推、Karcher 均值等所有基于路径能量优化的任务中，碰撞避免自动生效。这与直接惩罚路径总势能的方案（“penalty-augmented path energy”）有本质区别——后者将排斥作为目标函数的加性项，导致轨迹中部出现不自然的“爆炸”式扩张（Figure 3, Figure 7），而图流形构造通过将排斥信息嵌入度量，使爆炸效应被抑制。

### 与 IPC 障碍方法的关系

**Incremental Potential Contact (IPC)**（Li et al., 2020）是当前无相交模拟的代表性方法，使用对数障碍函数和连续碰撞检测（CCD）保障无穿透。Repulsive Shells 在排斥势能的选择上与 IPC 形成互补而非替代关系：

- **长程引导 vs 局部障碍**：IPC 障碍仅在接近接触时产生显著力，缺乏全局运动规划能力；切点能量（TPE）提供长程排斥，使形状在远离接触时就主动调整姿态（Figure 4, Figure 20）。实验表明，将 IPC 障碍直接作为图流形的势能 $\Phi$ 时，外翻轨迹出现跳跃，无法获得平滑结果（Figure 20），而 TPE 则稳定完成。
- **计算成本**：在多数测试场景中，自适应 TPE 求值的速度与 IPC 障碍相当甚至更快（Figure 16），远场相互作用仅占总成本的约 5%。
- **理论保证的差异**：IPC 在离散设置下通过 CCD 提供严格的相交避免；Repulsive Shells 在离散情况下未给出严格保证，粗网格可残留小相交，空间升采样后可能出现局部穿透。这是该方法的一个明确边界。

### 知识库挂载点

1. **形状空间理论**：该方法直接继承 Heeren 等人的弹性壳形状空间框架（包括膜能量 $\widehat{\mathcal{W}}_{\mathrm{membrane}}$ 和弯曲能量 $\widehat{\mathcal{W}}_{\mathrm{bending}}$ 的定义），在其上附加图流形构造。知识库中后续工作若需在形状空间中引入其他约束（如不可压缩性、等距嵌入），可参考此“度量增强”模式。

2. **排斥势能离散化**：该方法改进了 **Yu et al. (2021a)** 的中点求积 TPE 方案，提出了自适应切点能量求积——利用 BVH 和快速多极方法在无限剖分上懒惰求积，精确捕获近接触奇点。这一改进使 TPE 在粗网格上可靠防止自相交（Figure 12），并随空间细化收敛到有意义的连续能量（Figure 17）。固定中点求积方案无法捕捉关键奇点，即使加密网格也未能阻止相交。该自适应方案可作为知识库中其他需要精确奇异积分评估的方法的参考。

3. **几何处理任务**：该方法将碰撞避免统一应用于插值、外推、平均等任务，与基于骨骼绑定（skeletal rig）的方法形成对比——后者仅处理局部关节运动，无法产生全局运动计划的改变（Figure 15）。与基于体流形的微分同胚变形方法（divergence-free volumetric flow）相比，Repulsive Shells 不受空间分辨率限制，在近接触形状处理上表现更好（Figure 19）。

### 适用边界

- **拓扑约束**：要求输入网格具有固定连接关系，不适用于拓扑变化的任务。
- **边界曲面的理论保证缺失**：切点能量仅对无边界的封闭曲面有严格排斥性证明，带边界曲面在实践中表现良好但缺乏理论保证（Figure 29 展示了切割球面的外翻，边界固定为黄色曲线）。
- **参数敏感性**：排斥强度参数 $\beta$ 需手动调节以平衡弹性形变与排斥力；弯曲刚度与排斥力的相互作用会影响最优轨迹（Figure 31）。
- **非局部正则化的副作用**：切点能量引入非局部弯曲正则化，可能抑制尖锐褶皱的形成——在需要褶皱的场景（如环面平坦度量的等距嵌入，Figure 25）中，需增加膜刚度来逼近。

### 后续启发与开放问题

该方法为知识库打开了若干后续方向：(1) 能否建立离散版本的自适应 TPE 的严格无相交保证，弥合与 IPC 在理论保证上的差距；(2) 如何将最新的 IPC 连续扩展（Li et al., 2023）或其他势能（如 Möbius 能量）集成到图流形框架中，以改进长程排斥行为；(3) 在保持相交避免的前提下实现自动空间重网格化，以处理大剪切变形；(4) 结合降阶模型（如骨骼绑定、隐空间参数）加速高维轨迹优化——当前的分层时空优化（Figure 30）已展示粗预览高度预测最终结果，为进一步加速提供了基础；(5) 如何更自然地融入刚体运动，避免当前手动惩罚平移和旋转的对齐问题。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/Repulsive_Shells.pdf]]