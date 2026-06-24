---
title: A General Two-stage Initialization for Sag-free Deformable Simulations
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/A_General_Two_stage_Initialization_for_Sag_free_Deformable_Simulations.pdf
project_link: "https://graphics.cs.utah.edu/research/projects/sag-free-simulations/"
code_link: null
aliases:
- TSI
- GTSISFDS
tags:
- SIGGRAPH_2022
- topic/other_unclear
core_operator: 将初始化过程解耦为全局线性静力平衡阶段和局部材料非线性处理阶段：全局阶段通过线性最小二乘求解满足接触与摩擦约束的内力；局部阶段针对每个单元独立求解其静止状态参数，从而避免全局非线性优化。
primary_logic: 全局阶段仅需内力方向已知或力子空间由线性约束描述即可保持线性，与材料非线性无关；通过多边形摩擦锥近似将摩擦接触转化为线性约束，使整个全局优化保持线性；局部阶段可并行处理大量小型非线性问题，极大降低计算成本。
claims:
- 在多种仿真系统（质点弹簧、FEM、MPM、PBD）上实现了无下垂初始化，并在复杂场景（接触、自接触、摩擦）中保持形状，显著优于naive初始化。
- 与Twigg and Kačić-Alesić (2011)相比，初始化速度提升480倍；与Ly et al. (2018)相比，类似复杂度模型的初始化时间从50分钟降至0.5秒。
- 消融实验验证了正确接触处理（vs. 无接触/固定位置约束）和摩擦锥近似对静态平衡的必要性。
- 张量平移（tension shifting）对于布料在风力扰动下恢复形状至关重要；缺少它则布料迅速失稳。
---

# A General Two-stage Initialization for Sag-free Deformable Simulations

> [!tip] 核心洞察
> 全局阶段仅需内力方向已知或力子空间由线性约束描述即可保持线性，与材料非线性无关；通过多边形摩擦锥近似将摩擦接触转化为线性约束，使整个全局优化保持线性；局部阶段可并行处理大量小型非线性问题，极大降低计算成本。

| 字段 | 内容 |
|------|------|
| 中文题名 | 一种通用的两阶段无下垂变形仿真初始化方法 |
| 英文题名 | A General Two-stage Initialization for Sag-free Deformable Simulations |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://graphics.cs.utah.edu/research/projects/sag-free-simulations/) · [Project](https://graphics.cs.utah.edu/research/projects/sag-free-simulations/") |
| Topic | #topic/other_unclear |
| Method | Two-Stage Initialization |
| Dataset | Mass-spring tetrahedral mesh, Cloth hat simulation, FEM plant |

> [!tip] 效果简介
> - Mass-spring tetrahedral mesh (Fig. 17) 上，初始化的速度提升倍数 比 Twigg and Kačić-Alesić (2011) 快 480× vs Twigg and Kačić-Alesić (2011) (480× 加速)。
> - Cloth hat simulation (Fig. 12) 上，初始化耗时 约 0.5 秒 vs Ly et al. (2018) 报告的约 50 分钟 (快约 6000×)。
> - FEM plant (Fig. 9) 上，平均体积压缩比 (det(F)) 平均 0.999，标准差 0.038（Corotated Linear Elasticity） vs 无（纯性质指标）。

## 概要

在变形体仿真中，若直接将给定的初始形状当作静止形状启动模拟，重力会使物体产生明显的下垂（sagging），破坏艺术设计的初始姿态。现有抗下垂方法大多依赖全局非线性优化，计算代价高昂，且难以处理摩擦接触、局限于特定仿真系统或材料模型。

本文提出一种**通用的两阶段初始化方法**，将问题解耦为：**全局阶段**——通过线性最小二乘求解包含接触与摩擦约束的静力平衡，确定各元素应产生的目标内力；**局部阶段**——针对每个元素独立求解其静止状态参数，处理材料非线性。核心洞察在于：全局阶段仅需内力方向已知即可保持线性，与材料非线性无关；通过多边形摩擦锥近似将摩擦转化为线性约束，使整个全局优化维持线性；局部阶段可并行处理大量小型非线性问题，极大降低计算开销。

该方法适用于质点弹簧、FEM、MPM、PBD/XPBD 等多种仿真系统，在复杂接触、自接触和摩擦场景下均能实现无下垂初始化。实验表明，与 Twigg and Kačić-Alesić (2011) 相比初始化速度提升 **480 倍**；与 Ly et al. (2018) 相比，类似复杂度模型的初始化时间从约 50 分钟降至 **0.5 秒**。消融实验验证了正确接触处理、摩擦锥近似和张量平移对静态平衡与形状保持的关键作用。

## 核心方法与创新机理

### 问题瓶颈与核心洞察

传统变形仿真初始化将给定的初始形状直接视为静止形状（rest shape），当重力等外力作用于仿真对象时，对象在仿真启动瞬间即发生下垂（sagging），无法保持初始形状。现有抗下垂方法（如 **Twigg & Kačić-Alesić**, SCA 2011；**Ly et al.**, ACM Trans. Graph. 2018）依赖于求解全局非线性优化问题，不仅计算代价高昂（数十分钟至数小时），而且大多无法处理摩擦接触，且局限于特定的仿真系统和材料模型。

本文的核心洞察在于：**全局静力平衡阶段仅需知道内力的方向或力子空间由线性约束描述即可保持线性，与材料本身的非线性无关**。通过将摩擦接触转化为多边形摩擦锥近似下的线性约束，整个全局优化可保持为线性最小二乘问题；而材料的非线性则被完全移入局部阶段，每个单元独立求解小规模非线性问题，可高度并行化。这一解耦策略从根本上避免了全局非线性优化，使得初始化速度提升数个数量级。

### 两阶段初始化框架

方法将初始化过程解耦为两个顺序执行的阶段：

**全局阶段（Global Stage）**：在给定的初始形状下，构建并求解一个线性静力平衡系统，确定每个元素（弹簧、四面体、MPM粒子等）为维持初始形状所需产生的目标内力。该阶段同时处理接触法向力和摩擦力，将其作为未知量纳入线性系统。

**局部阶段（Local Stage）**：针对每个元素，根据全局阶段输出的目标力，独立求解其静止状态参数（弹簧张力、FEM变形梯度、MPM Cauchy应力对应的变形梯度、PBD/XPBD约束函数值等）。由于各元素相互独立，该阶段可完全并行化。

### 关键 Changed Slots 与因果链路

#### Slot 1：初始化范式——从全局非线性优化到线性-非线性解耦

**基线**：将初始形状视为静止形状（naive initialization），或求解全局非线性优化问题（Twigg & Kačić-Alesić 2011; Ly et al. 2018）。

**本文方案**：全局线性最小二乘求解静力平衡 + 局部并行求解单元静止状态。这一改变的因果链路如下：

1. **全局阶段**构建线性系统 $\mathbf{A} \mathbf{f} = - \mathbf{f}^{\mathrm{ext}}$，其中 $\mathbf{A}$ 为 $(3n + n_f) \times 3m$ 的稀疏矩阵，由静力平衡方程和内力约束方程组成。静力平衡要求作用在每个质量 $j$ 上的内力之和等于负的外力：
   $$\forall j , \quad \sum_{i} \mathbf{f}_{ij} = - \mathbf{f}_{j}^{\mathrm{ext}}$$
   对于非点质量物体，还需满足力矩平衡：
   $$\forall j , \quad \sum_{i} \left( \mathbf{r}_{ij} \times \mathbf{f}_{ij} \right) = - \pmb{\tau}_{j}^{\mathrm{ext}}$$

2. 每个元素 $i$ 产生的内力必须满足牛顿第三定律（净力为零）和角动量守恒（净力矩为零）：
   $$\forall i , \quad \sum_{j} \mathbf{f}_{ij} = \mathbf{0}$$
   $$\forall i , \quad \sum_{j} \left( ( \mathbf{x}_j - \mathbf{p} ) \times \mathbf{f}_{ij} \right) = 0$$

3. 由于未知力 $\mathbf{f}$ 的数量通常多于约束方程，系统是欠定的。本文通过正则化最小二乘求解最小内应力解：
   $$\operatorname*{min}_{\mathbf{f}} { \left\| \mathbf{A} \mathbf{f} + \mathbf{f}^{\mathrm{ext}} \right\| _{2}^{2} } + \rho \left\| \mathbf{f} \right\| _{2}^{2}$$
   对应法方程为对称正定系统，可用共轭梯度法高效求解：
   $$\left( \mathbf{A}^{T} \mathbf{A} + \rho \mathbf{I} \right) \mathbf{f} = - \mathbf{A}^{T} \mathbf{f}^{\mathrm{ext}}$$

4. **局部阶段**在已知当前形状 $\mathbf{x}$ 和目标力 $\mathbf{H}_i$ 的情况下，求解单元 $i$ 的静止配置 $\mathbf{q}_i$：
   $$\mathbf{q}_{i} = \mathbf{G}_{i}^{-1} ( \mathbf{H}_{i} ) \Big|_{\mathbf{x}}$$
   该逆映射 $\mathbf{G}_{i}^{-1}$ 的具体形式取决于仿真系统和材料模型。

**因果效果**：全局阶段始终为线性，与材料非线性无关；局部阶段各单元独立求解，可完全并行化。这一解耦使得初始化速度提升 480× 至 6000×（见实验部分）。

#### Slot 2：接触处理——从忽略/固定位置约束到法向力作为未知量

**基线**：忽略接触或将接触简化为固定位置约束。

**本文方案**：将法向接触力作为未知量纳入全局线性系统。在接触点 $j$ 处，法向接触力表示为：
   $$\mathbf{f}_{j}^{\mathbf{n}} = c_j \mathbf{n}_j$$
其中 $c_j \geq 0$ 为非负标量系数，$\mathbf{n}_j$ 为接触面法向。该约束作为边界条件加入全局线性系统，使用 Bounded Conjugate Gradient（BCCG）方法求解，确保 $c_j \geq 0$。

**因果效果**：正确的接触处理使对象在撤去支撑后仍能保持初始形状（Figure 3d），而忽略接触（Figure 3b）或使用固定位置约束（Figure 3c）均导致不正确的初始化和滑动。在自接触场景（如果冻立方体堆积，Figure 4）中，正确接触处理使对象利用自接触维持形状，而 naive 初始化出现明显下垂。

#### Slot 3：摩擦处理——从无法处理到多边形摩擦锥线性近似

**基线**：未处理摩擦或需要非线性锥约束。

**本文方案**：使用 $K=8$ 个离散方向的多边形保守近似摩擦锥。接触点 $j$ 的摩擦力表示为：
   $$\mathbf{f}_{j}^{\mu} = \sum_{k=0}^{K-1} c_{j}^{k} \mathbf{u}_{j}^{k}$$
其中 $\mathbf{u}_{j}^{k}$ 为第 $k$ 个离散摩擦方向，$c_{j}^{k} \geq 0$ 为非负系数。该近似将摩擦融入线性系统，仅需施加非负系数约束。

**因果效果**：在依靠摩擦力维持初始形状的场景（如软桥，Figure 5）中，正确摩擦处理使桥能够楔入两侧悬崖并保持稳定，而固定位置约束导致仿真开始时桥即滑落。在薄页靠摩擦立起（Figure 10）和帽子靠摩擦放置在球上（Figure 12）等场景中，摩擦处理同样至关重要。

### 模块顺序与训练/推理路径

完整的初始化流程如下：

1. **输入**：给定的初始形状 $\mathbf{x}$、外部力 $\mathbf{f}^{\mathrm{ext}}$（如重力）、接触和摩擦配置。

2. **接触检测**：在初始形状上检测所有接触点和自接触点，计算法向 $\mathbf{n}_j$ 和摩擦方向 $\mathbf{u}_j^k$。

3. **全局阶段**：
   - 构建线性系统 $\mathbf{A} \mathbf{f} = - \mathbf{f}^{\mathrm{ext}}$，包含静力平衡方程、内力约束、接触法向力约束和摩擦锥近似约束。
   - 使用 BCCG 求解正则化最小二乘问题，得到每个元素的目标力 $\mathbf{H}_i$。
   - 对于 MPM，全局阶段直接求解 Cauchy 应力 $\pmb{\sigma}_i$ 而非单个力 $\mathbf{f}_{ij}$。

4. **局部阶段**（并行执行）：
   - 对于质量-弹簧系统：从目标力直接计算弹簧张力 $T_i$。
   - 对于 FEM：通过优化求解变形梯度 $\mathbf{D}_m$：
     $$\operatorname*{min}_{\mathbf{D}_{m}} \left\| \mathbf{H} + w \left( \mathbf{D}_{m} \right) \mathbf{P} \left( \mathbf{D}_{m} \right) \mathbf{D}_{m}^{-T} \right\| _{2}^{2}$$
   - 对于 MPM：通过优化求解变形梯度 $\mathbf{F}_i$：
     $$\operatorname*{min}_{\mathbf{F}_{i}} \left\| \pmb{\sigma}_{i} - \frac{1}{\operatorname{det}(\mathbf{F}_{i})} \mathbf{P} ( \mathbf{F}_{i} ) \mathbf{F}_{i}^{T} \right\| _{2}^{2}$$
   - 对于 PBD/XPBD：通过静力平衡形式 $\sum_{i} \mathbf{g}_{ij} ( \mathbf{x} ) C_{i} ( \mathbf{x} ) = - \mathbf{f}_{j}^{\mathrm{ext}}$ 求解约束函数值。

5. **输出**：更新后的静止状态参数（弹簧张力、变形梯度、约束函数值等），用于启动后续仿真。

**关键因果链路**：全局阶段的线性性依赖于内力子空间可由线性约束描述这一事实——无论材料非线性如何，只要力的方向已知或力子空间是线性的，静力平衡方程就保持线性。材料的非线性完全被隔离在局部阶段的逆映射 $\mathbf{G}_i^{-1}$ 中，每个单元独立求解，互不干扰。

### 关键公式与变量含义

- $\mathbf{f}_{ij}$：元素 $i$ 作用在质量 $j$ 上的内力向量
- $\mathbf{f}_{j}^{\mathrm{ext}}$：作用在质量 $j$ 上的外力（如重力）
- $\mathbf{r}_{ij}$：质量 $j$ 相对于元素 $i$ 参考点的位置向量
- $\pmb{\tau}_{j}^{\mathrm{ext}}$：作用在质量 $j$ 上的外部力矩
- $\mathbf{A}$：合并静力平衡和内力约束的稀疏矩阵，维度 $(3n + n_f) \times 3m$
- $\rho$：正则化系数，用于趋向最小内应力解
- $c_j, c_j^k$：接触法向力和摩擦力的非负系数
- $\mathbf{D}_m$：FEM 四面体单元的变形梯度
- $\mathbf{P}$：第一 Piola-Kirchhoff 应力张量
- $\pmb{\sigma}_i$：MPM 粒子的 Cauchy 应力
- $\mathbf{F}_i$：MPM 粒子的变形梯度

### 特殊机制：张量平移（Tension Shifting）

对于布料等薄膜材料，局部阶段计算的弹簧张力可能为负（压缩），导致布料在微小扰动下失稳。本文引入张量平移技术：将计算出的张力整体向上平移一个常数值，使所有张力非负，从而赋予布料足够的刚度以抵抗扰动。消融实验（Figure 13）表明，缺少张量平移时布料在微风中迅速坍塌，而有平移时即使受到大扰动也能恢复初始形状。

![[assets/figures/papers/paper_list_l16_https_graphics_cs_utah_edu_research_projects_sag_free_simulations/figures/010_Figure_9.jpg]]
*Figure 9: A plant model simulated using FEM with different materials: (top) Neo-Hookean, (middle) Corotated Linear Elasticity, and (bottom) Saint Venant-Kirchhoff, deforming with an external wind force, producing visually similar motion, all initialized using our method. The visualization on the right shows how the tetrahedra in the initial shape are compressed (cyan color) or stretched (red color) after initializing with the Corotated Linear Elasticity material. The average compression ratio is 0.999 and the standard deviation is 0.038. The other two materials produce similar visualizations*

![[assets/figures/papers/paper_list_l16_https_graphics_cs_utah_edu_research_projects_sag_free_simulations/figures/013_Figure_14.jpg]]
*Figure 14: Inverse elastic shape design: (a) the given initial shape, used for initializing our method with gravity, (b) the generated rest shape after simulation without gravity, (c) the final shape after initializing using the generated rest shape and simulating with gravity, and (d) all models. Notice that the initial and the final shapes closely match. Simulated using FEM with corotated linear elasticity material*

## 实验与关键发现

本文在两阶段初始化框架下，针对质量-弹簧、FEM、MPM、PBD/XPBD 等多种仿真系统进行了系统性验证，覆盖了接触、摩擦、自接触、风力扰动等复杂场景。以下从主结果、消融实验、性能对比和适用边界四个维度梳理关键发现。

### 一、主结果：无下垂初始化与形状保持

**核心定性结果**：在所有测试场景中，本文方法均能实现无下垂初始化，使物体在重力作用下保持给定的初始形状，而 naive 初始化（直接将初始形状视为静止形状）则出现明显的塌陷或下垂。Figure 1 以 FEM 八爪鱼模型为典型示例：naive 初始化导致触手下垂，而本文方法在接触圆环前始终保持初始形状。这一优势在果冻立方体堆积（Figure 4，自接触场景）、倾斜果冻堆夹在刚性障碍间（Figure 6）、卡车干草堆（Figure 7）等场景中均得到一致验证。

**FEM 材料模型通用性**：Figure 9 展示了同一植物模型在 Neo-Hookean、Corotated Linear Elasticity 和 Saint Venant-Kirchhoff 三种材料下的初始化效果。三者均实现无下垂，且在外力扰动下产生视觉相似的变形。以 Corotated Linear Elasticity 为例，初始化后四面体的平均体积压缩比 det(F) 为 0.999，标准差仅 0.038，表明初始形状几乎未被压缩。Figure 8 的直方图进一步量化了八爪鱼模型的体积压缩分布，验证了方法对多种超弹性材料的适应性。

**MPM 与 PBD 系统验证**：Figure 16 展示了 MPM 可变形兔子与近不可压缩水流体耦合的场景：naive 初始化导致兔子耳朵下垂和体积损失，本文方法完全避免。Figure 15 的 XPBD 头发仿真同样证实了方法在基于位置的动力学框架中的有效性。

### 二、性能对比：数量级加速

**与 Twigg and Kačić-Alesić (SCA 2011) 对比**：在质量-弹簧四面体网格场景（Figure 17）中，本文方法初始化速度比前者快约 **480 倍**。前者采用全局非线性优化求解静力平衡，而本文的全局阶段仅为线性最小二乘，局部阶段高度并行，这是加速的根本原因。

**与 Ly et al. (ACM Trans. Graph. 2018) 对比**：在布料帽子靠摩擦放置在球体上的场景（Figure 12）中，Ly et al. 的方法对类似复杂度模型需约 **50 分钟**完成初始化（含摩擦接触的弹性壳逆设计），本文方法仅需约 **0.5 秒**，加速约 **6000 倍**。需注意该比较基于相似形状和复杂度的模型，但并非严格同模型同硬件，故应视为数量级层面的优势，而非精确倍数。

**Table 1** 汇总了各示例的初始化时间，全局阶段和局部阶段分别计时，总时间从数毫秒到数秒不等，验证了方法在多种仿真规模和系统中的高效性。

### 三、消融实验：关键设计决策的因果验证

消融实验系统性地验证了接触处理、摩擦处理和张力平移三个关键设计对无下垂初始化的必要性。

**接触处理的必要性**：Figure 3 以右端固定、左端靠在刚性物体上的薄弹性梁为对象，对比了四种初始化策略：(a) naive 初始化——撤去支撑后形状与初始状态差异显著；(b) 本文方法但无接触处理——无法维持初始形状；(c) 将接触视为固定位置约束——撤去支撑后形状不正确，且初始状态已出现异常滑动；(d) 本文完整方法——正确保持初始形状，撤去支撑后正常变形。该消融直接证明：真实接触力作为未知量纳入全局线性系统（含 cⱼ ≥ 0 约束）是保持静力平衡的必要条件，固定位置约束无法替代。

**摩擦处理的必要性**：Figure 5 的软桥场景提供了决定性证据。软桥依靠摩擦力楔入两悬崖之间维持初始形状。使用固定位置约束（无摩擦处理）的初始化导致仿真一开始软桥即滑落；本文方法正确求解摩擦力，使桥在木桶滚过前稳定保持。Figure 10 的薄页靠摩擦立起场景进一步印证：naive 初始化瞬间倒塌，本文方法通过静摩擦力维持初始姿态。这些结果表明，多边形摩擦锥近似（K=8）虽然引入一定保守性，但足以在复杂接触场景中实现物理正确的静力平衡。

**张力平移（tension shifting）对布料稳定性的关键作用**：Figure 13 的布料场景消融显示，无张力平移时，即便初始形状得以保持，轻微风力扰动即导致布料迅速坍塌；有张力平移时，布料在经受大扰动后仍能恢复初始形状。该消融揭示了局部阶段中张力平移对于布料类结构在动态扰动下维持稳定的因果机制：无平移时局部阶段求得的张力过低，使布料缺乏恢复力。

**局部硬化（local stiffening）的自动增强**：Figure 12 的帽子场景中，本文方法自动加强了折叠和接触区域的刚度，使帽子在摩擦支撑下保持形状；naive 初始化虽未滑落，但形状明显塌陷。该效果源于局部阶段根据目标力自动调整静止状态参数，无需手动指定加强区域。

### 四、适用边界与失败模式

**仿真系统表示限制**：方法要求仿真系统可抽象为“元素-质量”表示，且内力函数可从目标力反向计算静止状态参数。对于不满足此条件的表示形式（如某些非结构化粒子系统），方法无法直接适用。但论文已覆盖质量-弹簧、FEM、MPM、PBD/XPBD 等主流范式，覆盖面较广。

**力函数可逆性要求**：局部阶段依赖力函数的逆映射 Gᵢ⁻¹。尽管大多数常用力函数（线性弹簧、超弹性 FEM、MPM 超弹性粒子、PBD 约束函数等）满足可逆性或可通过小规模优化求解，但理论上存在不可逆情形。论文未给出此类情形的失效示例，该边界需手动验证。

**塑性不兼容**：现有塑性模型会覆盖初始化计算的变形梯度，因此当前方法与塑性模拟不兼容。这是方法的一个明确限制，论文在 limitations 中直接指出。

**摩擦锥近似的保守性**：多边形摩擦锥近似（K=8）将摩擦融入线性系统，但可能因离散方向有限而引入保守性，即求解的摩擦力可能略小于真实库仑摩擦锥内的最优值。论文未给出不同 K 值对精度影响的定量消融，该点需要进一步验证。

**非显式静止形状输出**：方法不直接输出显式的静止形状网格，而是输出每个元素的静止状态参数（如变形梯度、弹簧张力等）。对于需要显式静止形状的下游应用（如 3D 打印），需通过零重力仿真间接估计（Figure 14 展示了该逆设计流程，初始形状与最终形状高度匹配）。这一间接路径虽可行，但增加了额外步骤。

![[assets/figures/papers/paper_list_l16_https_graphics_cs_utah_edu_research_projects_sag_free_simulations/figures/016_Table_1.jpg]]
*Table 1: Computation times of our method*

![[assets/figures/papers/paper_list_l16_https_graphics_cs_utah_edu_research_projects_sag_free_simulations/figures/008_Figure_8.jpg]]
*Figure 8: Visualization and histogram of volume compression ratios (measured by det(F?? )) of the tetrahedra in the octopus models shown in Figure 1, initialized using our method*

![[assets/figures/papers/paper_list_l16_https_graphics_cs_utah_edu_research_projects_sag_free_simulations/figures/001_Figure_1.jpg]]
*Figure 1: An example deformable object simulation prepared using (top-row) naive initialization that treats the given initial shape as the rest shape, which leads to sagging with gravity, and (bottom-row) our initialization that preserves the given initial shape by treating it as the intended shape in static equilibrium under gravity. The two initialization methods produce qualitatively similar animations, while ours maintains the initial shape prior to collisions with the torus. Simulations are generated using FEM with corotated linear elasticity material [Sifakis and Barbic 2012]*

![[assets/figures/papers/paper_list_l16_https_graphics_cs_utah_edu_research_projects_sag_free_simulations/figures/003_Figure_3.jpg]]
*Figure 3: A thin elastic beam that is fixed on the right side and resting on contact on a rigid object on the left side, simulated using FEM with corotated linear elasticity material. The bottom row shows the final simulated shape after the rigid object is removed. The simulations are initialized using (a) naive initialization, (b) ours without contact handling, (c) ours by treating contacts as position constraints, and (d) ours with proper contact handling. Notice that proper contact handling is important for both maintaining the initial shape and allowing deformation when the contact is removed*

## 定位与知识库关联

本文的核心贡献在于改变了变形仿真初始化中 **“静止形状—初始形状”关系的求解范式**（slot: 初始化范式）。传统方法将用户给定的初始形状直接视为静止形状（naive initialization），或通过全局非线性优化在给定初始形状下反向求解静止形状（Twigg & Kačić-Alesić, SCA 2011; Ly et al., ACM Trans. Graph. 2018）。本文提出的两阶段初始化将这一过程解耦为**全局线性静力平衡求解**和**局部材料非线性处理**，从而将初始化从一个昂贵的、系统特定的全局非线性问题，转化为一个通用的、可高效求解的线性-非线性混合框架。

### 相对已有方法的本质差异

与 **Twigg & Kačić-Alesić (SCA 2011)** 的力基静态平衡方法相比，本文改变的关键 slot 在于**求解策略的线性化程度和接触处理能力**。Twigg 方法在全局范围内直接包含材料非线性，导致必须求解一个大规模非线性优化问题；本文通过将材料非线性完全移入局部阶段，使全局阶段退化为一个稀疏线性最小二乘问题（公式5-8），从而在类似复杂度的质量-弹簧模型上实现了 **480倍的初始化加速**（Figure 17）。更为关键的是，Twigg 方法无法处理摩擦接触，而本文通过多边形摩擦锥近似（K=8，公式11）将摩擦接触转化为线性约束，首次在保持全局阶段线性的前提下实现了对接触和摩擦的正确处理。

与 **Ly et al. (ACM Trans. Graph. 2018)** 的弹性壳逆设计方法相比，本文改变的核心 slot 在于**通用性和计算效率**。Ly 的方法采用两步非线性优化，虽然支持摩擦接触，但仅限于超弹性壳模型，且对于类似复杂度的帽子模型需要约 **50 分钟**的初始化时间；本文方法将同一任务压缩至约 **0.5 秒**，加速约 6000 倍（Figure 12），同时将适用范围扩展至质点弹簧、FEM（多种材料模型）、MPM、PBD/XPBD 等几乎所有主流仿真范式。这一通用性的根源在于本文仅要求仿真系统可抽象为“元素-质量”表示，且内力函数可从目标力反向计算静止状态参数（公式13）。

### 知识库挂载点

本文在变形仿真知识库中的挂载位置是**初始化预处理模块**，与以下知识节点形成紧密关联：

1. **静力平衡求解**：本文的全局阶段（Section 3.3）将静力平衡条件（公式1-2）与内力约束（公式3-4）合并为线性系统 $\mathbf{A} \mathbf{f} = -\mathbf{f}^{\mathrm{ext}}$，并通过正则化最小二乘 $\min_{\mathbf{f}} \|\mathbf{A} \mathbf{f} + \mathbf{f}^{\mathrm{ext}}\|_2^2 + \rho \|\mathbf{f}\|_2^2$ 求解最小内应力解。这一形式与**约束动力学中的力基求解**和**静力学逆问题**文献直接对接。

2. **摩擦接触的线性化处理**：多边形摩擦锥近似（公式11）将 Coulomb 摩擦锥保守近似为 K 个离散方向的非负组合，使全局阶段保持线性。这一技术可追溯到**基于优化的接触力学**中线性互补问题（LCP）的处理策略，但本文的创新在于将其嵌入到一个与材料模型无关的初始化框架中。

3. **材料模型的反向映射**：局部阶段（公式13）要求从目标力 $\mathbf{H}_i$ 反解静止状态参数 $\mathbf{q}_i = \mathbf{G}_i^{-1}(\mathbf{H}_i)|_{\mathbf{x}}$。对于 FEM，这表现为求解变形梯度 $\mathbf{D}_m$ 使力矩阵匹配（公式21）；对于 MPM，表现为求解 Cauchy 应力对应的变形梯度 $\mathbf{F}_i$（公式28）；对于 PBD/XPBD，表现为通过几何级数闭合形式直接计算拉格朗日乘子（公式39）。这一反向映射机制与**基于物理的逆问题**和**参数估计**文献形成知识关联。

4. **仿真系统的通用抽象**：本文要求仿真系统满足“元素-质量”抽象（Section 3.1），即每个元素 $i$ 产生作用于质量 $j$ 的力 $\mathbf{f}_{ij}$，且满足牛顿第三定律（公式3）和角动量守恒（公式4）。这一抽象覆盖了**基于力的仿真范式**的主流分支，使其成为连接不同仿真系统的通用初始化层。

### 适用边界与限制

本文方法的适用边界由以下条件界定：

- **表示形式限制**：仅适用于可抽象为元素-质量的仿真系统，不能直接应用于无质量概念或非力基的表示（如纯几何方法）。
- **内力函数的可逆性**：要求内力函数能够从目标力反向计算静止状态参数。虽然大多数常用力函数满足此条件，但理论上存在不可逆情形（如某些退化或病态材料模型），此时局部阶段将无法求解。
- **力子空间的线性性**：全局阶段保持线性的前提是力子空间可由线性约束描述。如果内力方向依赖于未知的材料参数，则全局阶段将退化为非线性优化，失去本文的核心优势。
- **塑性不兼容**：现有塑性模型会在仿真过程中覆盖初始化计算的变形梯度，因此当前方法与塑性模拟不直接兼容。
- **显式静止形状的缺失**：方法不显式输出静止形状，对于需要显式静止形状的应用（如 3D 打印）不够直接，但可通过在零重力环境下仿真估计静止形状（Figure 14）。
- **摩擦锥近似的保守性**：多边形近似（K=8）引入一定保守性，所有约束要求非负系数，可能限制某些极端摩擦行为。

### 后续研究启发

本文为后续研究开辟了若干方向：

1. **塑性兼容的初始化**：在 MPM 等支持塑性的仿真系统中，如何将初始化计算的变形梯度与后续塑性变形统一，使塑性变形继承初始静止配置，是一个直接但非平凡的扩展方向。

2. **不可逆内力函数的处理**：对于无法直接求逆的内力函数，可探索基于采样的局部阶段求解策略，或利用机器学习从大量初始形状-仿真参数对中学习局部初始化映射，进一步加速并扩展适用范围。

3. **自适应摩擦锥近似**：研究多边形摩擦锥边数 K 对精度和计算开销的 trade-off，以及是否可采用自适应或更紧致的近似（如椭圆锥近似），在保持线性性的同时减少保守性。

4. **跨系统知识迁移**：本文的通用抽象为不同仿真系统间的初始化知识迁移提供了基础。例如，在 FEM 中计算的静止状态参数是否可指导 MPM 的初始化，或反之，是一个值得探索的问题。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/A_General_Two_stage_Initialization_for_Sag_free_Deformable_Simulations.pdf]]