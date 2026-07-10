---
title: A Contact Proxy Splitting Method for Lagrangian Solid-fluid Coupling
type: paper
paper_level: A
venue: SIGGRAPH
year: 2023
pdf_ref: paperPDFs/SIGGRAPH_2023/A_Contact_Proxy_Splitting_Method_for_Lagrangian_Solid_fluid_Coupling.pdf
project_link: null
code_link: null
aliases:
- FMPGVA
- CPSMLSFC
tags:
- SIGGRAPH_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 利用标准粒子-网格传输操作（P2G与G2P）对变形梯度的体积部分——雅可比 J 进行体积平均，以计算假设变形梯度 F̄，从而放宽过强的不可压缩约束。
primary_logic: 将面向有限元法的假设变形梯度（F̄）方法与MPM固有的粒子-网格迁移机制相结合，通过投影法对 J 进行体积平均，无需引入额外的低阶基函数或修改现有基函数，即可在标准显式MPM框架内高效消除体积锁定，且与基函数类型和材料模型无关。
claims:
- 在 Cook 膜问题中，标准 MPM 产生严重的非物理应力振荡且无法通过网格细化消除，而 F̄ MPM 在两种基函数（GIMP 和 B-splines）下均消除了振荡。
- 在条形基础（Prandtl 承载力）问题中，F̄ MPM 的归一化荷载-位移曲线趋近解析解 5.14，而标准 MPM 预测值显著偏高（过刚）。
- 在溃坝流问题中，F̄ MPM 的结果与更复杂的三场混合 MPM 公式一致，且采用 GIMP 与 B-splines 时质心演化几乎完全重合，而标准 MPM 则表现出明显差异。
- "在三维滑坡模拟中，F̄ MPM 成功再现了实际滑坡的渐进破坏并给出约 29 m 的滑移距离；标准 MPM 则严重低估滑移（GIMP: 0.0055 m, B-splines: 19.07 m）甚至无法激发破坏。"
---

# A Contact Proxy Splitting Method for Lagrangian Solid-fluid Coupling

> [!tip] 核心洞察
> 将面向有限元法的假设变形梯度（F̄）方法与MPM固有的粒子-网格迁移机制相结合，通过投影法对 J 进行体积平均，无需引入额外的低阶基函数或修改现有基函数，即可在标准显式MPM框架内高效消除体积锁定，且与基函数类型和材料模型无关。

| 字段 | 内容 |
|------|------|
| 中文题名 | 规避显式物质点法中的体积锁定：一种简单、高效且通用的方法 |
| 英文题名 | A Contact Proxy Splitting Method for Lagrangian Solid-fluid Coupling |
| 会议/期刊 | SIGGRAPH 2023 |
| Links | [paper](https://www.math.ucla.edu/multiples/publication/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | F̄-MPM with Particle-Grid Volume-Averaging |
| Dataset | Cook's membrane, Strip footing on incompressible elastoplastic solid, Dam break, 3D landslide |

> [!tip] 效果简介
> - Cook's membrane (Neo-Hookean, ν=0.499) 上，应力场中非物理震荡消除与尖端位移收敛 F̄ MPM 消除了应力震荡，尖端位移收敛至非线性 B̄ MPM 参考解 vs 标准 MPM 存在严重应力震荡且不随网格细化改善 (定性上从强震荡变为光滑应力场；尖端位移：标准 MPM 过刚，F̄ MPM 与 B̄ 参考解一致)。
> - Strip footing on incompressible elastoplastic solid (Prandtl 承载力) 上，归一化承载力 (q/κ) F̄ MPM (GIMP/B-splines) 趋近分析解 5.14 vs 标准 MPM 预测值远高于 5.14（过刚） (F̄ 结果准确逼近 5.14，标准 MPM 误差显著)。
> - Dam break (近不可压缩流体) 上，流体质心在流向的时间演化及压力场合理性 F̄ MPM 在两种基函数下质心演化几乎一致，压力场与三场混合 MPM 参考结果相似 vs 标准 MPM 在不同基函数下质心演化差异大，压力场存在锁定迹象 (F̄ 方法消除了基函数依赖性，接近复杂基准解)。

## 概要

显式物质点法（MPM）在模拟近不可压缩材料时，因每个背景网格单元内使用大量积分点，引入了过强的不可压缩约束，导致体积锁定——表现为非物理的过刚行为和应力/应变场的严重振荡。本文提出一种简单、高效且通用的解决方案：将面向有限元法的假设变形梯度（F̄）方法与 MPM 固有的粒子-网格迁移机制相结合。核心操作是利用标准 P2G/G2P 传输操作对变形梯度的体积部分（雅可比 J）进行体积加权平均，得到假设变形梯度 F̄，以此替代原始变形梯度进行应力更新，从而放宽过强的不可压缩约束。该方法无需引入额外基函数或修改现有基函数，仅修改应力更新步骤，与基函数类型和材料模型无关。

在 Cook 膜、条形基础（Prandtl 承载力）、溃坝流和三维滑坡四个基准算例中，F̄ MPM 均有效消除了体积锁定：应力振荡消失，荷载-位移曲线趋近解析解，质心演化与更复杂的三场混合 MPM 公式一致，并成功再现真实滑坡的渐进破坏。方法定位为显式 MPM 框架内的一种轻量级锁定缓解技术，可直接嵌入现有代码，无需额外参数。

## 核心方法与创新机理

### 问题背景与体积锁定的根源

显式物质点法（MPM）在模拟近不可压缩材料时面临一个根本性困难：体积锁定（volumetric locking）。其物理根源在于，当泊松比 ν → 0.5 时，材料几乎不可压缩，每个物质点（积分点）都独立承载着“体积不变”的约束。在标准 MPM 框架中，一个背景网格单元内通常包含多个物质点，导致该单元内被施加了过多的不可压缩约束，远超出物理系统实际的约束数量。这种约束冗余使得系统呈现出非物理的过刚行为，表现为应力场和应变场中出现严重的空间振荡，且这种振荡无法通过简单的网格细化来消除。

这一问题在面向有限元法（FEM）的文献中已有成熟解决方案——假设变形梯度（F̄）方法。其核心思想是将变形梯度 $F$ 分解为体积部分（由雅可比 $J = \det(F)$ 表征）和偏斜部分，然后对体积部分进行某种形式的“放松”处理，以降低过强的不可压缩约束。然而，将 F̄ 方法直接移植到 MPM 中面临一个关键障碍：FEM 中的 F̄ 方法依赖单元内的平均操作，而 MPM 的物质点与背景网格之间不存在固定的单元归属关系。

### 核心创新：基于粒子-网格迁移的体积平均算子

本工作的核心洞察在于，MPM 框架中天然存在的粒子-网格（P2G）与网格-粒子（G2P）传输操作，恰好可以充当体积平均的载体，无需引入任何额外的低阶基函数或修改现有基函数。这一洞察将 F̄ 方法从“基于单元平均”的范式转换为“基于粒子支持域平均”的范式，使其与 MPM 的计算结构无缝融合。

具体而言，方法的核心是定义了一个投影算子 $\Pi(\cdot)$，用于对雅可比 $J$ 进行两步体积加权平均：

**第一步（P2G 投影）：** 将每个物质点的雅可比 $J_p$ 与其体积 $V_p$ 加权后映射到背景网格节点，计算节点上的体积平均雅可比：

$$\bar{J}_i = \frac{\sum_p w_{ip} J_p V_p}{V_i}, \quad V_i := \sum_p w_{ip} V_p$$

其中 $w_{ip}$ 是物质点 $p$ 在网格节点 $i$ 处的基函数值。这一步的本质是将局部（粒子尺度）的体积变化信息汇聚到节点，利用基函数的紧支性实现空间平滑。

**第二步（G2P 投影）：** 将节点上的平均雅可比映射回物质点，得到粒子上的体积平均雅可比：

$$\bar{J}_p = \sum_i w_{ip} \bar{J}_i$$

两步合起来定义了投影算子 $\Pi(J_p) := \bar{J}_p$。这一算子具有明确的物理含义：$\bar{J}_p$ 代表了以物质点 $p$ 为中心、以其基函数支持域为范围的体积变化加权平均值，而非该点处的局部精确值。

### 假设变形梯度的构造与应力更新

获得 $\bar{J}_p$ 后，假设变形梯度 $\bar{F}_p$ 通过局部缩放构造：

$$\bar{\pmb{F}}_p = \left( \frac{\bar{J}_p}{J_p} \right)^{1/\mathrm{dim}} \pmb{F}_p$$

其中 $\mathrm{dim}$ 是空间维度。这一运算将原始变形梯度 $F_p$ 的体积部分（由 $J_p$ 控制）替换为平滑后的体积部分（由 $\bar{J}_p$ 控制），而保持偏斜部分不变。当材料接近不可压缩时，$J_p \approx 1$ 的局部约束被 $\bar{J}_p \approx 1$ 的“平均约束”所取代，从而有效减少了独立约束的数量，消除了体积锁定。

在实际显式时间积分中，为避免隐式求导带来的复杂性和计算开销，方法采用增量形式。定义相对变形梯度 $\Delta F_p = F_p^{n+1} \cdot (F_p^n)^{-1}$ 及其雅可比 $\Delta J_p = \det(\Delta F_p)$，则增量形式的相对假设变形梯度为：

$$\Delta\bar{\pmb{F}}_p = \left( \frac{\Pi(\bar{J}_p^n \Delta J_p)}{\bar{J}_p^n \Delta J_p} \right)^{1/\mathrm{dim}} \Delta\pmb{F}_p$$

这一公式的关键在于，投影算子 $\Pi(\cdot)$ 作用于“试探雅可比” $\bar{J}_p^n \Delta J_p$，而分子分母中均使用 $\bar{J}_p^n$（上一时间步已知量），从而完全避免了需要计算 $\Pi(\cdot)$ 的导数。最终，粒子应力通过 $\Delta\bar{F}_p$ 更新，而非原始的 $\Delta F_p$。

### 修改的模块与计算流程

所提方法对标准显式 MPM 框架的修改极为克制，仅涉及一个模块中的一个步骤。完整的计算流程如下：

1. **P2G 传输（不变）：** 将物质点的质量和动量映射至背景网格节点，使用标准基函数 $w_{ip}$。
2. **网格更新（不变）：** 在背景网格上求解动量方程，更新节点速度，施加边界条件。
3. **G2P 传输（速度部分不变）：** 将节点速度映射回物质点，更新物质点位置和速度。
4. **应力更新（修改）：** 在更新物质点应力时，不再直接使用原始变形梯度 $F_p^{n+1}$，而是：
   - 计算增量变形梯度 $\Delta F_p$ 及其雅可比 $\Delta J_p$；
   - 通过 P2G/G2P 两步投影计算 $\Pi(\bar{J}_p^n \Delta J_p)$；
   - 构造增量相对假设变形梯度 $\Delta\bar{F}_p$；
   - 使用 $\Delta\bar{F}_p$ 更新应力。

**Changed Slot 1：应力更新中使用的变形梯度。** 基线方法直接使用 $F_p^{n+1}$ 或 $\Delta F_p$ 驱动本构模型；所提方法使用体积平均后的 $\bar{F}_p^{n+1}$（通过 $\Delta\bar{F}_p$ 增量构造），从源头上减少了过约束。

**Changed Slot 2：雅可比的计算与使用方式。** 基线方法中，$J_p = \det(F_p)$ 直接参与应力计算（如体积响应部分）；所提方法中，$J_p$ 仅作为中间量，实际驱动应力的是经过投影算子平滑后的 $\bar{J}_p$。投影算子 $\Pi(\cdot)$ 的引入是方法的核心，它利用了 MPM 现有的 P2G/G2P 通信模式，未增加新的数据结构或计算阶段。

### 方法的关键性质

**与基函数和材料模型无关：** 体积平均算子 $\Pi(\cdot)$ 仅使用标准基函数 $w_{ip}$ 作为权重，不依赖基函数的具体形式（GIMP、B-splines 等均适用），也不对本构模型做任何假设（超弹性、弹塑性、黏塑性等均可直接使用）。

**无需额外参数：** 方法不引入任何人工阻尼系数或约束参数。FLIP/PIC 混合比、时间步长准则等与标准 MPM 保持一致。

**计算开销极小：** 额外的计算仅包括两次基函数加权的求和操作（P2G 和 G2P 各一次）以及少量标量运算，相比完整的应力更新步骤几乎可以忽略。

**边界条件与接触处理不变：** 由于修改仅限于应力更新阶段，网格上的动量求解和节点速度计算完全不受影响，因此现有的边界条件施加方式和接触算法无需任何调整。

### 与现有 MPM 锁定缓解方法的区别

与 Coombs 等人（CMAME 2018）提出的 F̄ MPM 方法相比，本方法的核心区别在于平均操作的作用域：Coombs 方法在背景网格单元内进行平均，需要引入额外的“低阶”基函数来构造单元内的平均场；而本方法在基函数支持域内进行平均，直接复用标准基函数，无需定义新的函数空间。与 Bisht 等人（Computers and Geotechnics 2021）的非线性 B̄ 方法相比，B̄ 方法直接修改应变-位移矩阵，而本方法在变形梯度层面操作，数学上更为简洁，且与 MPM 的更新拉格朗日描述自然兼容。

## 实验与关键发现

本文通过四组覆盖固体力学与流体力学的基准算例，系统验证了所提 F̄ MPM 方法在消除体积锁定方面的有效性、通用性及与基函数类型的无关性。所有实验均在统一的显式 MPM 框架（Taichi）下进行，标准 MPM 与 F̄ MPM 的唯一差异仅在于应力更新时是否使用体积平均的假设变形梯度，其余 P2G、网格更新、G2P 速度更新及粒子位置更新完全一致，确保了对比的公平性。

### 4.1 Cook 膜问题：应力振荡消除与位移收敛

Cook 膜是验证近不可压缩材料锁定行为的经典基准。采用 Neo-Hookean 本构，泊松比 ν = 0.499，分别使用 GIMP 和二次 B-splines 两种基函数进行模拟。

**核心发现**：标准 MPM 在两种基函数下均产生严重的非物理应力振荡，且该振荡不随网格细化而改善——这是体积锁定的典型特征。相比之下，F̄ MPM 在 GIMP 和 B-splines 下均消除了应力振荡，获得了光滑的应力场（Figure 3, Figure 4）。尖端竖向位移的收敛性分析（Figure 6）进一步表明：标准 MPM 预测的尖端位移显著偏小（过刚），而 F̄ MPM 的结果与 Bisht et al. 的非线性 B̄ GIMP 参考解一致，且随物质点数量增加稳定收敛。Figure 5 中 F̄ GIMP 解与非线性 B̄ GIMP 参考解在 5,776 个物质点下的应力场高度吻合，验证了所提方法在精度上与更复杂的 B̄ 方法相当。

**基函数依赖性消除**：标准 MPM 中，B-splines 的锁定程度轻于 GIMP——这是因为 B-splines 具有更大的支撑域，天然提供了更多的体积平均效应。F̄ MPM 则通过显式的体积平均操作消除了这种基函数依赖性，使两种基函数下的解趋于一致。

### 4.2 条形基础问题：承载力预测精度

该问题模拟不可压缩弹塑性固体上的 Prandtl 承载力问题，解析归一化承载力为 q/κ = 5.14。采用 GIMP 和 B-splines 两种基函数，对比标准 MPM 与 F̄ MPM 的归一化荷载-位移曲线。

**定量结果**（Figure 8）：F̄ MPM 在两种基函数下的归一化承载力均趋近解析解 5.14；标准 MPM 的预测值则显著偏高，表现出典型的体积锁定过刚行为。Figure 9 展示了 F̄ MPM 接触压力解的网格收敛性，表明方法在承载力预测上具有良好的数值收敛特性。Figure 10 的应力场对比进一步确认：标准 MPM 的应力场存在锁定导致的异常应力集中，而 F̄ MPM 的应力场合理且光滑。

### 4.3 溃坝流问题：流体力学验证与基函数无关性

溃坝流模拟近不可压缩流体的大变形自由表面流动，是验证方法在流体力学中锁定缓解能力的严格测试。采用弱可压缩 Neo-Hookean 模型，对比标准 MPM、F̄ MPM 以及 Mast et al. 的三场混合 MPM 参考解。

**流动形态与压力场**（Figure 12）：F̄ MPM 的流动快照与三场混合 MPM 参考结果高度一致，压力场分布合理；标准 MPM 的压力场则存在锁定迹象，流动形态与参考解存在明显偏差。

**质心演化的基函数无关性**（Figure 13）：标准 MPM 在 GIMP 和 B-splines 下的流体质心演化曲线存在显著差异，再次证实了基函数类型对锁定程度的强影响。F̄ MPM 在两种基函数下的质心演化几乎完全重合，且与三场混合 MPM 参考解一致。这一结果强有力地证明了所提方法在流体大变形问题中同样能有效消除体积锁定，且使结果摆脱了对基函数选择的敏感依赖。

### 4.4 三维滑坡问题：真实灾害模拟能力

三维滑坡模拟采用弹性-塑性不排水粘土模型（Tresca 屈服准则），验证方法在真实岩土工程问题中的表现。该问题的关键指标是滑移距离（run-out distance），反映滑坡的渐进破坏过程。

**定量对比**（Figure 17）：
- **F̄ GIMP**：滑移距离 29.96 m
- **F̄ B-splines**：滑移距离 29.29 m
- **Standard GIMP**：滑移距离 0.0055 m（几乎无滑动）
- **Standard B-splines**：滑移距离 19.07 m

标准 GIMP 严重过刚，几乎无法激发破坏，严重低估了滑坡风险；标准 B-splines 虽有一定滑移，但仍显著偏低。F̄ MPM 在两种基函数下均成功再现了渐进破坏过程，滑移距离约 29 m，且两种基函数的结果高度一致。Figure 15 和 Figure 16 的等效塑性应变与平均正应力快照直观展示了 F̄ MPM 对破坏区演化与应力分布的合理捕捉能力。

### 关键消融与适用边界

**基函数通用性消融**：四组实验一致表明，F̄ MPM 在 GIMP 和二次 B-splines 两种截然不同的基函数下均能有效缓解锁定，而标准 MPM 的表现高度依赖基函数类型。这验证了体积平均操作独立于基函数选择的通用性。

**参数无关性**：所提方法仅修改应力更新步骤，不引入任何额外参数（如人工阻尼或约束），FLIP/PIC 混合比 η = 0.85 在所有实验中保持与标准 MPM 相同，表明锁定缓解效果完全来自体积平均机制本身。

**方法边界与局限**：
1. **显式框架限制**：该方法基于显式时间积分设计，直接推广至隐式 MPM 较为困难，因为计算 F̄ 的导数值复杂且开销大。
2. **残余微弱振荡**：在 Cook 膜等算例中，F̄ MPM 解仍存在微弱应力振荡，但已证实与体积锁定无关，可能源于 MPM 固有的跨单元积分误差。
3. **验证范围**：当前仅在标准显式 MPM 格式（更新拉格朗日描述）下验证，尚未在总拉格朗日 MPM 或其他高阶 MPM 变体上测试。
4. **多物理场与接触**：方法在孔隙介质大变形-渗流耦合问题中的适用性，以及体积平均操作对接触压力计算精度的潜在影响，仍有待进一步研究。

![[assets/figures/papers/paper_list_l15_https_www_math_ucla_edu_multiples_publication/figures/005_Figure_5.jpg]]
*Figure 5: Cook’s membrane: comparison of our F¯ GIMP solution with the nonlinear B¯ GIMP solution in Bisht et al. [19]. Both solutions are produced with 5,776 material points*

![[assets/figures/papers/paper_list_l15_https_www_math_ucla_edu_multiples_publication/figures/027_Figure_17.jpg]]
*Figure 17: 3D landslides: comparison of run-out distances in the standard and F¯ MPM simulations*

![[assets/figures/papers/paper_list_l15_https_www_math_ucla_edu_multiples_publication/figures/003_Figure_3.jpg]]
*Figure 3: Cook’s membrane: mean normal stress fields in the standard and F¯ MPM solutions, obtained with GIMP basis functions*

![[assets/figures/papers/paper_list_l15_https_www_math_ucla_edu_multiples_publication/figures/004_Figure_4.jpg]]
*Figure 4: Cook’s membrane: mean normal stress fields in the standard and F¯ MPM solutions, obtained with B-splines basis functions*

![[assets/figures/papers/paper_list_l15_https_www_math_ucla_edu_multiples_publication/figures/006_Figure_6.jpg]]
*Figure 6: Cook’s membrane: tip vertical displacements from our standard and*

![[assets/figures/papers/paper_list_l15_https_www_math_ucla_edu_multiples_publication/figures/008_Figure_8.jpg]]
*Figure 8: Strip footing: normalized load–displacement curves from the standard and F¯ MPM solutions, obtained with GIMP and B-splines basis functions*

## 定位与知识库关联

本文的核心贡献在于为显式物质点法（MPM）的体积锁定问题提供了一个**极简的插拔式解决方案**：它不引入新的自由度、不修改背景网格上的基函数、不增加额外的背景网格，也不改变标准MPM时间步循环中除应力更新外的任何环节。这一设计使其在知识库中的定位非常清晰——它是一个**作用于“变形梯度→应力”这一计算槽（slot）的锁定缓解算子**，而非一个重新设计的MPM变体。

### 相对已有方法的本质差异与改变的 slot

在MPM中缓解体积锁定的已有路线大致有三条：（1）采用高阶基函数（如B-splines）以增加单元内可用的积分约束自由度；（2）引入多场混合公式（如位移-压力-雅可比三场格式），增加独立的压力场或雅可比场；（3）将有限元法中的假设变形梯度（F̄）或B̄方法移植到MPM，通过在背景网格单元内对变形梯度的体积部分进行平均来放松约束。

本文属于第三条路线，但与现有F̄-MPM工作存在**slot层面的根本差异**。以 **Coombs et al.**（CMAME 2018）的F̄-MPM为代表，其体积平均操作是在**背景网格单元**上进行的，这要求为每个单元定义额外的低阶基函数来构造单元内的平均雅可比场，从而改变了MPM的离散化结构——相当于在“网格离散化”这一slot中插入了新的成分。**Bisht et al.**（Computers and Geotechnics 2021）的非线性B̄-MPM同样需要构造单元级的平均变形梯度，涉及对标准基函数空间的修改。

本文的方法则完全避开了对基函数空间的任何改动。它将体积平均操作**从“单元”迁移到了“粒子-网格传输”这一MPM固有的slot中**：利用粒子到网格（P2G）的投影将粒子雅可比 $J_p$ 进行体积加权平均得到节点上的 $\bar{J}_i$，再通过网格到粒子（G2P）的映射将节点平均雅可比传回粒子得到 $\bar{J}_p$，最终以 $\bar{J}_p$ 与 $J_p$ 的比值缩放变形梯度构成 $\bar{\pmb{F}}_p$。这一操作的数学本质是一个投影算子 $\Pi(J_p)$，其实现完全复用了标准MPM中已有的 $w_{ip}$ 权重和P2G/G2P数据通路，不引入任何新的离散化对象。

因此，相对于已有F̄/B̄-MPM方法，本文改变的 slot 是：**将体积平均的载体从“单元级低阶基函数”替换为“标准粒子-网格传输算子”**。这一替换的后果是，方法不再与特定的基函数类型耦合——同一套代码在GIMP和二次B-splines上均直接生效，无需针对基函数调整平均策略。同时，它也不依赖材料模型的具体形式，因为修改只发生在变形梯度的体积部分缩放上，本构关系本身未被触及。

相对于**Mast et al.**（JCP 2012）的三场混合MPM，本文方法的差异更为本质：三场格式在“状态变量”slot中增加了独立的压力场和雅可比场，需要求解额外的耦合方程系统；而本文方法仅在“变形梯度后处理”slot中插入一个显式的体积平均步骤，不增加系统自由度，保持了显式MPM的计算简单性。在溃坝流问题中，本文F̄-MPM的结果与三场混合MPM参考解一致（Figure 12），但计算成本显著更低。

### 知识库挂载点与适用边界

本文方法最直接的知识库挂载点是**显式MPM框架下的“应力更新”模块**。具体而言，它挂载在标准MPM时间步循环中G2P阶段的变形梯度更新之后、本构关系调用之前（Algorithm 1）。这一挂载位置意味着：

- **适用条件**：方法适用于采用更新拉格朗日描述的显式时间积分MPM，其中变形梯度以增量方式更新（$\pmb{F}_p^{n+1} = \Delta\pmb{F}_p \cdot \pmb{F}_p^n$）。对于总拉格朗日MPM或其他非增量格式，需要重新推导体积平均的插入方式，论文未对此进行验证。
- **材料适用范围**：任何通过变形梯度驱动本构关系的材料模型均可直接受益，包括超弹性、弹塑性和近不可压缩流体。论文在Neo-Hookean超弹性、von Mises弹塑性和弱可压缩牛顿流体上均给出了验证。
- **基函数无关性**：方法对背景网格基函数的选择无特殊要求，已在GIMP（线性精度）和二次B-splines上验证，理论上可推广至其他满足单位分解性质的基函数族。
- **不适用场景**：论文明确指出，该方法基于显式时间积分设计，直接推广至隐式MPM较为困难，因为计算 $\bar{\pmb{F}}$ 的导数值（用于隐式切线刚度矩阵）复杂且开销大。此外，在多物理场耦合（如孔隙介质中的渗流-变形耦合）和涉及复杂接触约束的场景中，体积平均操作是否会对接触压力精度产生额外影响，尚属开放问题。

### 后续启发

本文的方法论贡献在于揭示了一个更一般的洞察：**MPM中粒子-网格传输操作本身即构成一个天然的多尺度投影算子**，可被用于构造各类“放松约束”的均匀化操作，而无需回到单元级的构造。这一思路可启发以下方向：

1. **其他锁定现象的缓解**：类似的思想能否用于剪切锁定或薄膜锁定的缓解？这需要将体积平均推广为更一般的变形模式投影，但P2G/G2P通路本身是通用的。
2. **多物理场扩展**：在孔隙介质大变形问题中，孔隙压力场同样面临锁定风险，能否利用相同的粒子-网格投影机制对压力场进行类似的均匀化处理？
3. **自适应体积平均尺度**：当前的体积平均尺度由基函数支撑域自动决定。是否存在最优的FLIP/PIC混合系数与背景网格尺寸配合方案，可在进一步降低数值阻尼的同时保持锁定缓解效果？

需要指出的是，论文在Cook膜问题中观察到F̄-MPM解仍存在微弱的应力振荡，但已证实与体积锁定无关。这一残余振荡的来源及其消除方法，以及该方法在三维复杂接触-大变形耦合问题中的鲁棒性，仍需后续工作验证。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2023/A_Contact_Proxy_Splitting_Method_for_Lagrangian_Solid_fluid_Coupling.pdf]]