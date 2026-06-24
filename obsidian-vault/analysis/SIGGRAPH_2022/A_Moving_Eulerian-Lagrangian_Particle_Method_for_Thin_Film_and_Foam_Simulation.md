---
title: A Moving Eulerian-Lagrangian Particle Method for Thin Film and Foam Simulation
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/A_Moving_Eulerian_Lagrangian_Particle_Method_for_Thin_Film_and_Foam_Simulation.pdf
project_link: "https://yitongdeng.github.io/MELP_Project/"
code_link: null
aliases:
- MELPMMM
- MELPMTFFS
tags:
- SIGGRAPH_2022
- topic/other_unclear
core_operator: 引入双层粒子体系（稀疏欧拉粒子负责界面几何离散与PDE投影求解，稠密拉格朗日粒子负责物质与动量平流），并将欧拉粒子运动限制为仅法向平流加切向重分布，从根本上解耦了几何演化与流动物理。
primary_logic: 拉格朗日粒子可大量部署以捕捉丰富流动细节，而欧拉粒子通过法向追踪和扩散式重分布始终维持均匀空间离散，使PDE求解稳定高效；对于泡沫，将每个液膜视为独立MELP区域，通过表面张力共享机制实现非流形交界处的力学耦合，无需显式处理奇异交接线，从而在动态演变中自然恢复Plateau定律。
claims:
- 双层粒子设计使动态表面上始终维持均匀离散，即使在高湍流下欧拉粒子也不聚集；而单层方法在相同CFL下出现粒子堆积和厚度方差发散。
- MELP支持更大时间步长，平衡态收敛时间从单层方法的3.91秒降至0.35秒，加速10倍以上。
- Multi-MELP无需显式对接，仅通过表面张力共享即可自发形成符合Plateau定律的泡沫交接：双气泡交界二面角误差≤2%，三叉交界线角度误差≤5%。
- MELP通过欧拉粒子间接求解压力，使其能以约7,000个欧拉粒子驱动约700,000个拉格朗日粒子，实现约60倍的物质分辨率提升。
---

# A Moving Eulerian-Lagrangian Particle Method for Thin Film and Foam Simulation

> [!tip] 核心洞察
> 拉格朗日粒子可大量部署以捕捉丰富流动细节，而欧拉粒子通过法向追踪和扩散式重分布始终维持均匀空间离散，使PDE求解稳定高效；对于泡沫，将每个液膜视为独立MELP区域，通过表面张力共享机制实现非流形交界处的力学耦合，无需显式处理奇异交接线，从而在动态演变中自然恢复Plateau定律。

| 字段 | 内容 |
|------|------|
| 中文题名 | 一种用于薄膜和泡沫模拟的移动欧拉-拉格朗日粒子方法 |
| 英文题名 | A Moving Eulerian-Lagrangian Particle Method for Thin Film and Foam Simulation |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://yitongdeng.github.io/MELP_Project.github.io/) · [Project](https://yitongdeng.github.io/MELP_Project/) |
| Topic | #topic/other_unclear |
| Method | Moving Eulerian-Lagrangian Particles (MELP) and multi-MELP |
| Dataset | Equilibrium thickness convergence, Plateau border dihedral angle validation, Partition surface curvature validation, Flow resolution |

> [!tip] 效果简介
> - Equilibrium thickness convergence (vs. Wang et al. 2021) 上，Time to equilibrium (s) 0.35 vs 3.91 (-91% (10× faster))。
> - Plateau border dihedral angle validation (double-bubble) 上，Dihedral angle error (%) ≤2.93% (max, pair 1–2) vs N/A (theoretical 120°) (≤2.93% deviation)。
> - Partition surface curvature validation (R2=0.02) 上，Curvature error (%) 3.41% vs N/A (analytical value) (3.41% deviation)。

## 概要

针对薄膜流体模拟中界面追踪与流动物理耦合在同一粒子集上导致的稳定性与分辨率矛盾，以及泡沫多区域非流形交接拓扑演化的难题，本文提出**移动欧拉‑拉格朗日粒子方法（MELP）**。其核心思路是引入双层粒子体系：稀疏的欧拉粒子仅沿法向平流并通过扩散式移位维持均匀空间离散，负责界面几何表示与压力投影求解；稠密的拉格朗日粒子随全速度平流，承载物质与动量输运，从而将几何演化与流动物理从根本上解耦。在此基础上，**multi‑MELP**将每个液膜视为独立MELP区域，通过表面张力共享机制实现非流形交界处的力学耦合，无需显式处理奇异交接线。

实验表明，MELP在平衡态收敛速度上较单层粒子方法**Wang et al. 2021**加速约10倍（0.35 s vs 3.91 s），且能以约7,000个欧拉粒子驱动约700,000个拉格朗日粒子，实现约60倍的物质分辨率提升；multi‑MELP可自发恢复Plateau定律，双气泡交界二面角误差≤2.93%，三叉交界线角度误差≤5%。该方法为动态表面上PDE求解提供了一种稳定、高效的无网格粒子框架，并展示了向多区域泡沫模拟的自然扩展能力。

## 核心方法与创新机理

### 问题瓶颈

薄膜与泡沫的粒子模拟长期受困于一个根本矛盾：单层粒子方法（如 **Thin-Film SPH**，Wang et al., TOG 2021）将界面几何追踪与流动物理求解耦合在同一粒子集上。粒子必须同时携带几何信息（位置、厚度、曲率）和物理量（速度、压力、浓度），而物理流动会驱动粒子运动，导致粒子分布随变形而剧烈不均匀——在高曲率或强拉伸区域粒子稀疏、数值精度崩溃，在压缩区域粒子堆积、时间步长被迫缩小。这使得单层方法无法同时实现高分辨率流动细节与稳定的大变形薄膜追踪。泡沫模拟中，多个液膜在非流形交接线处相遇，其拓扑演变和力学耦合的复杂性进一步超出了单层粒子方法的能力边界。

### 核心洞察：双层解耦

MELP的核心创新在于引入**双层粒子体系**，从根本上解耦几何演化与流动物理：

- **稀疏欧拉粒子（E particles）**：仅负责界面几何离散与PDE投影求解。E粒子数量少（通常数千个），但通过特殊运动策略始终维持均匀空间分布，为压力投影提供稳定、良条件的计算模板。
- **稠密拉格朗日粒子（L particles）**：负责物质与动量平流。L粒子可大量部署（可达数十万），以全速度自由流动，捕捉丰富的流动细节。

这一解耦的关键在于**欧拉粒子的运动限制**：E粒子仅沿法向平流（跟随薄膜变形），而在切向通过扩散式粒子移位（particle shifting）自由重分布，持续维持均匀离散。拉格朗日粒子则以完整速度平流，并将物理量通过APIC（Affine Particle-In-Cell）机制在两层之间传递。这种设计使得压力求解的数值稳定性与流动分辨率的丰富性不再相互制约。

### 方法框架总览

MELP单步仿真包含六个顺序模块（参见Figure 5），形成闭环：

1. **L2E Transfer**：将L粒子的质量、体积、表面活性剂浓度和动量保守地转移到E粒子。
2. **Geometry Computation**：在E粒子上计算面积、厚度、平均曲率和度量张量。
3. **Dynamics Computation**：在均匀E粒子上用IISPH求解法向和切向动力学。
4. **E2L Transfer**：将更新后的E粒子速度和APIC仿射量插值回L粒子。
5. **E Advance**：E粒子法向移动+切向扩散重分布。
6. **L Advance**：L粒子以全速度平流并投影回E定义的表面。

### 关键Changed Slot 1：粒子结构 — 从单层到双层

**Baseline**（Wang et al. 2021）：单一粒子集同时承担几何追踪与物理量携带，粒子数量与分布直接受流动影响。

**MELP**：双层粒子集（稀疏E + 稠密L），各自承担不同职责。E粒子数量由几何分辨率需求决定，L粒子数量由流动细节需求决定，两者可独立配置。典型配置中，约7,000个E粒子可驱动约700,000个L粒子，实现约60倍的物质分辨率提升（Table 4）。

**因果机制**：E粒子的均匀分布保证了压力泊松方程求解的数值条件，而L粒子的密集采样保证了平流精度和流动细节。两者通过APIC传递动量，避免了单层方法中粒子分布恶化→压力求解失稳→粒子进一步聚集的恶性循环。

### 关键Changed Slot 2：欧拉粒子平流策略 — 法向约束+切向重分布

**Baseline**：粒子以全速度场平流，随物质流动自然聚集或稀疏。

**MELP**：E粒子仅以法向材料速度移动（跟随表面的几何变形），切向运动完全由扩散式粒子移位驱动，目标是最小化粒子分布的不均匀性。具体而言，E粒子的切向位移由邻近粒子密度梯度决定，通过迭代将粒子推向低密度区域，直至分布均匀。

**因果机制**：法向约束使得E粒子始终附着在物理表面上，不会因切向流动而漂移；切向重分布则消除了拉伸/压缩导致的粒子聚集/稀疏，维持了PDE求解的数值稳定性。Figure 4验证了这一机制：在稳态螺旋流中，E粒子（红点）始终保持均匀分布，而L粒子（蓝圈）随流自由移动。

### 关键Changed Slot 3：压力求解方式 — IISPH on E + APIC to L

**Baseline**：在单层粒子上直接使用SPH求解压力，粒子分布的不均匀性直接影响求解精度和稳定性。

**MELP**：压力投影在均匀分布的E粒子上使用隐式不可压缩SPH（IISPH）求解。法向动力学方程为：

$$\frac{D \mathbf{u}_E^{\perp}}{D t} = \frac{\hat{p}_{\mathrm{in}} - \hat{p}_{\mathrm{out}}}{\rho \eta_E} \mathbf{n}_E + \frac{2 (\sigma_0 - \bar{R} T \Gamma) H_E}{\rho \eta_E} \mathbf{n}_E + \frac{\hat{f}_{\mathrm{ext}}^{\perp}}{\rho}$$

其中第一项为气‑液压力差（封闭气泡的$\hat{p}_{\mathrm{in}}$由理想气体定律计算），第二项为杨‑拉普拉斯表面张力（含表面活性剂修正），第三项为外部体力。切向动力学由表面活性剂梯度驱动的隐式方程描述，同样在E粒子上用松弛雅可比迭代求解。

求解完成后，更新后的E粒子速度和APIC仿射量通过E2L Transfer插值回L粒子，使密集的L粒子继承压力投影的动量修正。

**因果机制**：均匀E粒子网格使得IISPH的压力泊松方程条件数良好，允许更大的时间步长和更快的收敛。Table 4显示，MELP在平衡态收敛时间从单层方法的3.91秒降至0.35秒，加速超过10倍。

### 多区域泡沫耦合：multi-MELP

对于泡沫模拟，每个液膜区域独立运行MELP，通过三个机制实现区域间耦合：

1. **接触检测与碰撞处理**：检测不同区域E粒子间的穿透，施加非穿透力和速度阻尼。
2. **表面张力共享**：在交界处对称化计算表面张力和气压，使得交界粒子所受净力自动满足Plateau定律的力学平衡条件。某粒子的净力为：

$$f_{\mathrm{net}} = f_{\mathrm{st},L_K} + f_{\mathrm{air},L_K} + \sum_{(S,\gamma_{P,S})} \left( f_{\mathrm{st},L_S} + f_{\mathrm{air},L_S} \right) + f_{\mathrm{st},\mathrm{atm}}$$

其中包含自身区域的表面张力与气压、所有耦合区域的共享力以及外部大气表面张力。这一机制使得泡沫交界无需显式处理奇异交接线，在动态演变中自然恢复Plateau定律（双气泡交界二面角误差≤2.93%，Table 2）。

3. **概率性物质转移**：基于运动方向和表面活性剂浓度比，在区域间迁移L粒子，实现物质交换。

### 关键公式体系

薄膜动力学模型基于不可压缩无粘欧拉方程，分离为法向和切向分量（Equation 3），并引入表面活性剂浓度$\Gamma$和膜厚$\eta$的演化方程，构成完整的薄膜动力学系统（Equation 5）。L2E转移使用分区归一化的SPH核函数保证守恒性：

$$q_E = \sum_{L \in \mathcal{N}^{\mathcal{L}}(E)} \hat{W}(E, L) \cdot q_L$$

表面活性剂浓度的隐式求解方程（Equation 14）包含对流、扩散和源项，通过IISPH框架和雅可比迭代在E粒子上求解。

![[assets/figures/papers/paper_list_l28_https_yitongdeng_github_io_MELP_Project_github_io/figures/002_Figure_2.jpg]]
*Figure 2: An illustration of our one-sided geometric model. Left: a thin film lamella with thickness and local frames. Right: a triple-junction represented by three lamellae without directly modeling the singularity at ??*

![[assets/figures/papers/paper_list_l28_https_yitongdeng_github_io_MELP_Project_github_io/figures/006_Figure_5.jpg]]
*Figure 5: The computation workflow of a single simulation step in our proposed MELP framework*

![[assets/figures/papers/paper_list_l28_https_yitongdeng_github_io_MELP_Project_github_io/figures/011_Figure_10.jpg]]
*Figure 10: Left: illustration of the force*

![[assets/figures/papers/paper_list_l28_https_yitongdeng_github_io_MELP_Project_github_io/figures/024_Figure_21.jpg]]
*Figure 21: Interaction among bubbles of different sizes, showcasing our system’s ability to restore the equilibrium states*

## 实验与关键发现

### 平衡态收敛验证

MELP在薄膜平衡态收敛测试中表现出数量级优势。在相同初始条件和物理参数下，与单层粒子方法**Thin-Film SPH**（Wang et al., ACM Trans. Graph. 2021）进行对比：MELP在0.35秒内收敛到平衡厚度，而单层方法需要3.91秒，加速约10倍（Table 4, Figure 14右）。更关键的是，单层方法在CFL=0.033时厚度方差持续发散，无法收敛；而MELP的双层粒子设计使方差稳定下降并收敛（Figure 14左）。Figure 16进一步展示：在重力驱动的牛顿干涉条纹场景中，MELP始终收敛，单层方法在相同参数下发散，仅当降低物理参数（减小表面张力和重力）时才能收敛——这直接证明了双层结构是稳定性的因果瓶颈。

### 泡沫Plateau定律验证

Multi-MELP无需显式建模奇异交接线，仅通过表面张力共享机制即可自发恢复Plateau定律。Table 2给出了定量验证：双气泡交界处各分隔面之间的二面角与理论值120°的最大偏差仅为2.93%（pair 1–2）；三气泡三叉交界线处，三个分隔面之间的角度误差均不超过5%（最大4.75%）；四气泡交界处六片分隔面形成四条交界线，其交角与理论值109.47°的偏差亦在可接受范围。Figure 11和Figure 12分别从可视化和不同半径比的双气泡形态上佐证了这一结果。不同半径比下，较小气泡向较大气泡内凸出的程度符合物理预期（Figure 12），而分隔面曲率与解析值的偏差仅为3.41%（Table 3, Figure 13左上）。

### 流动分辨率与计算效率

MELP的核心架构优势在于解耦了几何离散与物质平流。欧拉粒子仅需约7,000个即可维持均匀空间离散并稳定求解压力投影，而拉格朗日粒子可部署约700,000个以捕捉丰富流动细节，实现了约60倍的物质分辨率提升（Table 4, Section 6.2）。相比之下，单层方法仅能使用约40,000个粒子。Figure 15的对比清晰展示了这一差异：MELP模拟的薄膜表面流动细节（涡旋、条纹）远丰富于单层方法。在计算耗时方面，MELP每帧约1.42秒（平衡场景），单层方法约0.48秒，但考虑到17.5倍的粒子数差距和稳定性收益，这一开销是可接受的。

### 消融实验：双层设计的决定性作用

最关键的消融证据来自Figure 14：移除双层设计（即使用单层粒子方法）直接导致厚度方差随模拟时间发散，薄膜无法收敛到平衡态。这验证了分析中的因果链条——单层粒子将界面追踪与流动物理耦合在同一粒子集上，粒子在大变形下堆积或稀疏，破坏了PDE求解的离散质量；而MELP通过欧拉粒子的仅法向平流加切向重分布策略，始终维持均匀离散，从根本上解决了这一瓶颈。

### 泡沫动态演变的复杂场景

MELP在多个复杂泡沫场景中验证了其能力：13个气泡融合并在底部热源驱动下形成表面“气旋”（Figure 9）；300个气泡落入容器形成泡沫山（Figure 18）；四个气泡从不稳定平衡重组到稳定结构并最终瓦解（Figure 20）；不同尺寸气泡间的相互作用及平衡态恢复（Figure 21）。这些场景展示了multi-MELP在动态拓扑演变中的鲁棒性，无需手动干预交接关系。

### 方法局限与适用边界

尽管MELP在薄膜与泡沫模拟中表现优异，仍存在明确局限：
- **显式力耦合限制**：多区域交界处的力计算采用显式方案，缺乏完全隐式积分，在极端刚度下可能限制时间步长。
- **物理精度边界**：分隔面及多连接处的流动力学未引入交界曲率等更精确的物理效应；理想气体方程与薄膜流体方程的耦合不满足动量守恒。
- **耦合范围受限**：当前框架不支持薄膜与固体的耦合（如固‑液边界、碰撞），限制了其在固‑液‑气三相场景中的应用。
- **硬件差异提示**：与Wang et al. 2021的性能对比中，MELP使用AMD ThreadRipper 3990X / Intel i9-9980XE（Table 5），而基线方法的硬件平台未完全统一，绝对耗时需谨慎解读，但相对趋势可靠。

![[assets/figures/papers/paper_list_l28_https_yitongdeng_github_io_MELP_Project_github_io/figures/017_Figure_14.jpg]]
*Figure 14: Comparison with Wang et al. [2021]. Left: test of convergence to equilibrium thickness. Right: comparison of computational cost*

![[assets/figures/papers/paper_list_l28_https_yitongdeng_github_io_MELP_Project_github_io/figures/012_Table_2.jpg]]
*Table 2: Numerical results to validate multi-MELP’s adherence to Plateau’s laws. The pairs are labeled corresponding to Figure 11*

## 定位与知识库关联

MELP 的核心定位在于**将薄膜流体模拟的粒子表示从单层结构改为双层协作结构**，这是其相对于既有方法的本质 slot 变更。在 **Thin-Film SPH**（Wang et al., ACM Trans. Graph. 2021）等前代工作中，单层粒子集同时承担界面几何追踪与流动物理量携带的双重职责。这种耦合导致一个根本性矛盾：要捕捉丰富的流动细节需要大量粒子，但粒子随物质全速度平流必然导致分布不均匀，进而使 PDE 投影求解的数值模板退化，表现为厚度方差发散和无法收敛到平衡态（Figure 14 左图）。MELP 将这一耦合拆解为两个独立但协作的粒子集——稀疏欧拉粒子（E）负责界面几何离散与压力投影，稠密拉格朗日粒子（L）负责物质与动量平流——从根本上解耦了几何演化与流动物理。

**知识库挂载点**：MELP 在知识图谱中的主要附着点有三处。其一，**无网格薄壳/薄膜流体模拟**分支，直接继承自 Thin-Film SPH 的单侧几何模型与 IISPH 压力求解框架，但将求解模板从随流粒子迁移到均匀分布的欧拉粒子上，解决了该分支长期存在的粒子聚集与数值退化问题。其二，**PIC/FLIP 混合粒子-网格方法**的思想迁移——MELP 的 L2E/E2L 转移机制本质上是将 APIC（Affine Particle-In-Cell）从固定网格背景移植到移动的无网格表面上，用欧拉粒子替代网格节点作为投影模板。这一跨分支嫁接使得 MELP 同时获得无网格方法的拓扑灵活性与网格类方法的数值稳定性。其三，**多材料/多区域界面追踪**领域，multi-MELP 通过表面张力共享机制处理泡沫交界，与显式重建交界线的方法（如网格类泡沫模拟中的交界追踪）形成对照——multi-MELP 选择不显式建模奇异交界线，而是让各液膜区域独立运行 MELP 并通过力耦合自发恢复 Plateau 定律。

**适用边界**：MELP 的设计假设薄膜始终可用单侧基曲面加厚度场描述，这意味着它天然适用于液膜、气泡壁等余一维主导的几何结构。论文明确指出的限制包括：（1）多区域交界处采用显式力计算，缺乏完全隐式积分，在极端刚度条件下可能限制时间步长；（2）理想气体方程与薄膜流体方程的耦合不满足动量守恒；（3）当前框架不支持薄膜与固体的耦合（固-液边界、碰撞）。此外，欧拉粒子的法向平流加切向重分布策略在薄膜发生拓扑变化（如破裂、融合）时需要额外处理，论文中通过 multi-MELP 的区域间物质转移部分解决了融合问题，但薄膜自交、撕裂等更复杂的拓扑事件仍需进一步机制。

**后续启发**：MELP 的双层解耦思路对更广泛的移动表面 PDE 求解具有方法论价值。论文提出的开放问题直接指向两个扩展方向：一是将框架从余一维（薄膜）推广到余二维（细丝/液丝结构），实现薄膜与液丝的统一耦合；二是将水平集等隐式几何表示融入 MELP 以增强对拓扑变化的处理能力。从知识库演进角度看，MELP 证明了“用稀疏均匀粒子做投影求解、用稠密随流粒子做物质输运”这一范式在无网格表面动力学中的有效性，这为其他需要在动态几何上求解 PDE 的物理模拟问题（如生物膜力学、燃烧前沿传播）提供了可参考的架构模板。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/A_Moving_Eulerian_Lagrangian_Particle_Method_for_Thin_Film_and_Foam_Simulation.pdf]]