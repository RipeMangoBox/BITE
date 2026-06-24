---
title: Adaptive Rigidification of Elastic Solids
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Adaptive_Rigidification_of_Elastic_Solids.pdf
project_link: null
code_link: "http://github.com/alecjacobson/gptoolbox"
aliases:
- ARES
tags:
- SIGGRAPH_2022
- topic/other_unclear
core_operator: 基于单元应变率Frobenius范数的双阈值机制（刚化阈值τ_R与弹性化阈值τ_E），驱动元素在刚体与弹性状态之间动态切换，并利用广度优先搜索构建无铰链的连通刚体组件。
primary_logic: 通过有限差分计算单元应变率来识别非形变区域并刚化，在需要弹性化时使用单次共轭梯度迭代的快速求解器近似估计应变以激活弹性区域，从而在无需预建层次结构的前提下实现运行时弹性-刚体模型的自适应混合仿真，同时利用接触力热身和近似接触处理保持仿真稳定。
claims:
- 轮胎仿真（橡胶胎面+钢制轮毂）中每步平均加速10倍，总仿真时间缩短为原来的1/5。
- 森林砍伐场景中自适应刚化比全弹性有限元仿真快10倍。
- 悬臂梁实验中，弹性化阈值τ_E=1e-5时顶点最大误差仅约0.1%，同时实现1.7倍加速。
- 方法适用于非均匀材料和多类超弹性本构模型；钢制轮毂与橡胶轮胎的混合场景验证了材料相关的自适应刚化行为。
---

# Adaptive Rigidification of Elastic Solids

> [!tip] 核心洞察
> 通过有限差分计算单元应变率来识别非形变区域并刚化，在需要弹性化时使用单次共轭梯度迭代的快速求解器近似估计应变以激活弹性区域，从而在无需预建层次结构的前提下实现运行时弹性-刚体模型的自适应混合仿真，同时利用接触力热身和近似接触处理保持仿真稳定。

| 字段 | 内容 |
|------|------|
| 中文题名 | 弹性固体的自适应刚化 |
| 英文题名 | Adaptive Rigidification of Elastic Solids |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://www.alexandremercieraubin.com/Work/papers/AdaptiveRigidification/) · [Code](http://github.com/alecjacobson/gptoolbox) |
| Topic | #topic/other_unclear |
| Method | Adaptive Rigidification of Elastic Solids |
| Dataset | Tire, Blob, Wheel, Forest |

> [!tip] 效果简介
> - Tire (rubber tread & steel hub) 上，Mean per-step speedup 10× vs 1× (+9×)。
> - Blob 上，Total Speedup 2.09 vs 1.0 (+1.09)。
> - Wheel (rolling) 上，Total Speedup 11.49 vs 1.0 (+10.49)。

## 概要

传统物理仿真要求用户在运行前将物体预先指定为刚体或可变形体，无法根据运行时受力情况自适应调整，导致对实际上不发生形变的区域仍进行昂贵的有限元计算，造成性能浪费。本文提出**自适应刚化**方法，通过监测单元应变率的 Frobenius 范数，以双阈值机制（刚化阈值 $\tau_R$ 与弹性化阈值 $\tau_E$）驱动元素在刚体与弹性状态之间动态切换，并利用广度优先搜索构建无铰链的连通刚体组件，从而在无需预建层次结构的前提下实现弹性-刚体模型的运行时自适应混合仿真。

在橡胶轮胎与钢制轮毂混合场景中，方法实现每步平均 **10 倍**加速，总仿真时间缩短为原来的 1/5；森林砍伐场景中比全弹性有限元仿真快 **10 倍**；悬臂梁实验中顶点最大误差仅约 0.1% 时仍可获得 1.7 倍加速。方法适用于非均匀材料和多类超弹性本构模型，为弹性体仿真中的计算资源自适应分配提供了有效方案。

## 核心方法与创新机理

### 问题背景与根本瓶颈

物理仿真中，弹性体的有限元计算是性能的主要瓶颈。传统方法（如 **Baraff & Witkin, SIGGRAPH 1998** 的半隐式向后欧拉格式）要求用户在仿真运行前就将物体预先指定为刚体或可变形体，无法根据运行时受力情况自适应调整。这导致对实际上不发生形变的区域仍然进行昂贵的有限元计算——每一时间步都需要组装并求解完整的弹性系统 $A \Delta \dot{\pmb x} = \pmb b$，造成大量计算资源浪费。

本工作的核心洞察是：**通过监测单元应变率来动态识别非形变区域并将其刚化，同时利用低成本的近似求解器在需要时激活弹性区域**，从而在无需预建层次结构的前提下实现运行时弹性-刚体模型的自适应混合仿真。

### 核心控制机制：双阈值驱动的状态切换

方法的“因果旋钮”在于基于单元应变率 Frobenius 范数的双阈值机制：

- **刚化阈值 $\tau_R$**：当某单元的应变率平方 Frobenius 范数 $\|\dot{E}\|_F^2$ 连续若干帧低于 $\tau_R$ 时，该单元成为刚体候选。
- **弹性化阈值 $\tau_E$**：当已刚化的单元通过近似求解估计出的应变率超过 $\tau_E$ 时，该单元被重新激活为弹性。

这两个阈值形成了状态切换的迟滞回路——$\tau_E$ 通常设置为 $\tau_R$ 的 1~2 个数量级以上，防止刚化与弹性化之间的高频振荡。这种非对称设计是关键：刚化条件相对宽松（只需应变率足够低），而弹性化条件更为保守（需要足够强的变形信号），从而在精度与性能之间取得可控的权衡。

### Changed Slots：相对于全弹性 FEM 的三个核心替换

**Slot 1：单元仿真模型——从“始终弹性”到“动态刚弹切换”**

基线方法中，每个四面体单元始终参与弹性求解。本方法将每个单元的状态动态标记为弹性或刚性：弹性单元贡献刚度矩阵 $K_{\mathsf{A}}$ 和节点力 $\pmb f_{\mathsf{A}}$，而刚性单元仅贡献刚体运动自由度（质心速度 $\pmb v$ 和角速度 $\pmb \omega$），其内部弹性力被完全省略。这一替换直接减少了系统求解规模。

**Slot 2：应变率监测——从“无”到“有限差分应变率计算”**

基线方法不追踪单元的形变历史。本方法引入基于 Green 应变的有限差分应变率：

$$\dot{E}_k = \frac{E_k - E_{k-1}}{h}$$

其中 $E_k$ 为当前帧的单元 Green 应变，$h$ 为时间步长。这一近似有意忽略了旋转分量——作者明确指出，解析应变率 $\dot{E} = \frac{1}{2}(\dot{F}^T F + F^T \dot{F})$ 对纯旋转运动也会产生非零值，而有限差分形式能更好地区分刚体旋转与真实形变。

**Slot 3：系统求解——从“全 FEM 线性系统”到“混合弹性-刚体约化系统”**

全弹性 FEM 每步求解完整的 $A \Delta \dot{\pmb x} = \pmb b$。本方法将系统约化为仅含弹性自由度（active DOFs）和刚体广义自由度的混合系统：

$$A_{\mathsf{A}} \Delta \dot{\boldsymbol{x}}_{\mathsf{A}} = h \left( D_{\mathsf{A}} \dot{\boldsymbol{x}}_{\mathsf{A}} + f_{\mathsf{A}} + h K_{\mathsf{A}} \dot{\boldsymbol{x}}_{\mathsf{A}} + f_{\mathcal{A}\mathrm{ext}} \right)$$

其中 $A_{\mathsf{A}} = M_{\mathsf{A}} - h D_{\mathsf{A}} - h^2 K_{\mathsf{A}}$，下标 $\mathsf{A}$ 表示仅涉及弹性单元对应的活跃自由度。弹性力与刚度矩阵的组装也仅遍历弹性单元子集 $\mathcal{E}$：

$$f_{\mathsf{A}} = G^{T} B_{\mathcal{E}}^{T} P_{\mathcal{E}}, \quad K_{\mathsf{A}} = G^{T} B_{\mathcal{E}}^{T} C_{\mathcal{E}} B_{\mathcal{E}} G$$

其中 $G$ 为从活跃自由度到全自由度的映射矩阵。该系统通过 LDLT 分解直接求解，避免了迭代求解器的不确定性。

### 管线模块顺序与因果链路

Algorithm 1 定义了主循环的完整流程，各模块之间存在严格的因果依赖：

**Step 1: Find Contacts（碰撞检测）**  
检测当前帧的碰撞对并构建接触约束 Jacobian 矩阵 $J_c$。这是后续接触力求解的前提。

**Step 2: WarmStart（接触力热身）**  
利用上一帧的接触力解 $\lambda$ 对当前帧进行初始化。这一步骤利用了时间相干性，显著加速接触力求解的收敛。

**Step 3: QuickSolve（快速近似求解）**  
这是弹性化决策的关键前驱模块。使用单次共轭梯度迭代（配合基于固定 Laplacian 的不完全 Cholesky 预条件子）近似求解全系统速度变化 $\Delta \dot{\boldsymbol{x}}_{\mathrm{approx}}$，进而估计每个刚化单元的近似应变率 $\dot{E}_{\mathrm{approx}}$。该近似求解的成本远低于完整弹性求解，但提供了足够准确的应变率上界估计，用于判断哪些刚化单元需要被重新激活。

**Step 4: Compute Strain Rates（计算实际应变率）**  
对弹性单元计算基于有限差分的实际应变率 $\dot{E}_k$。这是刚化决策的输入信号。

**Step 5: BFS to Identify Rigid Components（广度优先搜索构建刚体组件）**  
这是方法中防止物理失真的关键几何约束。将满足刚化条件的候选单元通过广度优先搜索聚合成连通刚体组件，但**禁止共享顶点的组件合并**——如图 2 所示，若红色三角形与已属于刚体 A 的顶点相邻，则不能并入刚体 B，否则 A 与 B 将共享该顶点并形成铰链，需要额外的铰链约束才能保证正确运动。这一设计保证了每个刚体组件内部无相对运动自由度。

**Step 6: Compute Rigid Properties（计算刚体属性）**  
对每个新形成的刚体组件计算质心 $\boldsymbol{p}$、质量矩阵 $M_{\mathsf{R}}$ 等刚体动力学参数。刚体顶点速度到广义速度的映射为：

$$\dot{x}_{i} = \begin{bmatrix} I & -(R r_{i})^{\times} \end{bmatrix} \begin{bmatrix} \pmb v \\ \pmb \omega \end{bmatrix}$$

其中 $r_i$ 为顶点相对于质心的位置向量。

**Step 7: LDLT Solve（混合系统求解）**  
求解约化系统 $A_{\mathsf{A}} \Delta \dot{\boldsymbol{x}}_{\mathsf{A}} = \pmb b_{\mathsf{A}}$ 获得弹性自由度的速度增量，同时更新刚体的广义速度 $\Delta \phi$。弹性与刚体之间的耦合通过共享顶点处的力传递自然处理。

**Step 8: Contact Solve（接触力求解）**  
使用投影高斯-赛德尔迭代求解接触力脉冲 $\lambda$，更新方程为：

$$\lambda_i^+ \gets \frac{\lambda_i H_{ii} - b + J_{ci} \Delta \dot{\pmb x}_c}{H_{ii} + \gamma}$$

其中 $b = J_c(\dot{\pmb x} + \Delta \dot{\pmb x}) + k_b \Phi$ 为 Baumgarte 稳定化约束，$\gamma$ 为柔顺系数，$k_b$ 为 Baumgarte 反馈系数。这一柔顺接触模型允许微小穿透，换取数值稳定性。

**Step 9: Update Velocities and Positions（状态更新）**  
将求解得到的速度增量应用于弹性和刚体自由度，更新位置和速度状态，进入下一时间步。

### 因果链路总结

整个管线的因果链可概括为：**QuickSolve 近似应变率 → 弹性化决策 → BFS 组件构建 → 混合系统求解 → 接触力求解 → 实际应变率计算 → 刚化决策（下一帧）**。QuickSolve 与 LDLT Solve 的分工是关键设计：前者以低成本提供弹性化所需的应变率估计，后者以精确求解保证弹性区域的物理准确性。双阈值机制在这两个求解器之间建立了非对称的迟滞回路，使得系统能够在刚体效率与弹性精度之间平滑过渡。

### 方法边界与限制

当前实现存在几个明确的方法边界：(1) 刚体属性仅在组件成员变化时重新计算，未实现增量更新，刚体分裂时的高效处理尚为未来工作；(2) 仅合并相邻单元形成刚体，未考虑合并相互接触但不相邻的单元以进一步减少自由度；(3) 当前实现依赖线性四面体单元和线性形函数，扩展到六面体或高阶形函数需进一步研究；(4) QuickSolve 的应变率近似总是高估真实值，导致弹性化阈值必须保守设置，可能延迟弹性区域的激活。

![[assets/figures/papers/paper_list_l4_https_www_alexandremercieraubin_com_Work_papers_AdaptiveRigidification_repair/figures/001_Figure_1.jpg]]
*Figure 1: Our algorithm can identify and adaptively rigidify undeforming portions of simulated elastic objects in order to improve performance without sacrificing visual fidelity. Per-step computation time for this tire simulation, with rubber tread and steel hub, shows a mean performance improvement of 10×, resulting in a 5× reduction in total simulation time*

## 实验与关键发现

本文的核心实验逻辑围绕一个中心问题展开：**自适应刚化能否在保持视觉保真度的前提下，显著降低弹性体仿真的计算开销？** 实验设计从性能加速比、精度-效率权衡、参数敏感性以及接触求解独立性四个维度，系统验证了方法的有效性。

### 主要性能结果

**Table 1** 汇总了五个典型场景下的总加速比。所有对比均以标准半隐式向后欧拉全弹性有限元仿真为基线，使用相同的时间步长、阻尼参数和材料参数。

| 场景 | 总加速比 | 刚化阈值 τ_R | 弹性化阈值 τ_E | 单元数 |
|------|----------|-------------|---------------|--------|
| Blob（弹性体自由落体） | 2.09× | 1e-6 | 1e-4 | 3,072 |
| Wheel（滚轮下落） | 11.49× | 1e-6 | 1e-4 | 4,096 |
| Forest（森林砍伐） | 8.29× | 1e-6 | 1e-4 | 38,912 |
| Octopus（章鱼碰撞） | 4.30× | 1e-6 | 1e-4 | 4,096 |
| Pachinko（弹珠台） | 3.38× | 1e-6 | 1e-4 | 3,072 |

最具代表性的案例是 **轮胎仿真**（橡胶胎面 + 钢制轮毂，**Figure 1**），每步平均加速 **10×**，总仿真时间缩短为原来的 **1/5**。这一场景的关键在于：钢制轮毂区域几乎不发生形变，方法自动将其刚化，仅对橡胶胎面部分维持弹性求解。这直接验证了核心瓶颈的突破——传统方法对非形变区域仍进行昂贵的有限元计算，而自适应刚化将计算资源集中在真正发生形变的区域。

**Forest 场景**（8.29× 加速）进一步凸显了方法的规模化优势。该场景包含 38,912 个四面体单元，模拟多棵树木被依次砍伐的过程。在任意时刻，仅被砍伐的树木需要弹性求解，其余静止树木自动刚化。**Figure 3** 的逐帧加速比曲线显示，Forest 场景的加速比随时间推移持续攀升，因为越来越多的树木进入静止状态并被刚化。

### 精度-效率权衡

自适应刚化的核心控制参数是**弹性化阈值 τ_E**，它决定了方法在多大程度上“保守地”恢复弹性区域。**Figure 5** 的悬臂梁实验给出了精确的权衡曲线：当 τ_E = 1e-5 时，顶点最大误差仅为悬臂长度的约 **0.1%**，同时实现 **1.7×** 加速。随着 τ_E 增大，加速比提升但误差也随之增加。这一结果确立了方法的实用边界：用户可根据应用对精度的容忍度，通过调节 τ_E 在精度与效率之间灵活取舍。

![[assets/figures/papers/paper_list_l4_https_www_alexandremercieraubin_com_Work_papers_AdaptiveRigidification_repair/figures/008_Figure_5.jpg]]
*Figure 5: Cantilever max vertex error (measured relative to cantilever length), and inverse speedup factor (lower is better), for a varying range of elastification thresholds and*

**Figure 7** 的滚轮下落实验从另一角度验证了精度保持：不同弹性化阈值下的滚轮下落时间与全弹性仿真几乎一致，表明刚化并未改变系统的宏观动力学行为。

### 参数敏感性分析

**Figure 4** 系统探索了四个关键参数对刚化行为的影响：

1. **阻尼（Figure 4b）**：更高阻尼加速了振荡衰减，使区域更快满足刚化条件，从而带来更高的加速比。这揭示了方法的物理直觉——阻尼耗散越强，非形变状态越早出现。

2. **网格分辨率（Figure 4c）**：不同分辨率下的刚化模式高度相似，但粗糙网格刚化更快。原因在于粗糙网格的数值阻尼和分辨率相关的刚度差异。这一发现表明方法对网格分辨率具有较好的鲁棒性。

3. **杨氏模量（Figure 4d）**：较低刚度导致更长、更大振幅的振荡周期，延迟刚化；较高刚度使物体更快趋于静止并刚化。这与物理直觉一致——刚度越大的材料在受力后恢复静止的速度越快。

4. **弹性化阈值（Figure 4a）**：刚化阈值 τ_R 决定何时创建刚体，但弹性化阈值 τ_E 才是决定哪些区域保持刚性的关键因素。较低的 τ_E 提供更忠实于全弹性行为的仿真，但计算代价更大。

### 接触求解独立性验证

一个潜在的公平性问题是：加速是否来自接触求解器的更换而非自适应刚化本身？**Table 1** 提供了不包含接触求解时间的加速比（标记为 NC），结果表明移除接触求解时间后加速比依然显著，排除了接触求解器夸大效益的可能性。方法使用的接触处理（Baumgarte 稳定化 + 投影高斯-赛德尔迭代）与刚化框架解耦，加速根源于弹性自由度的大幅削减。

![[assets/figures/papers/paper_list_l4_https_www_alexandremercieraubin_com_Work_papers_AdaptiveRigidification_repair/figures/004_Table_1.jpg]]
*Table 1: Speedup for different examples, and the parameters used: rigidification and elastification thresholds*

### 失败模式与适用边界

方法存在以下明确边界：

1. **刚体分裂效率**：当构成刚体的单元需要重新弹性化时，目前仅在刚体成员发生变化时重新计算刚体属性，未实现增量更新。刚体分裂为多个独立刚体的高效处理尚为未来工作。

2. **刚体合并范围**：方法仅合并相邻单元形成刚体，未考虑合并相互接触的单元。在密集接触场景（如大量物体堆叠）中，进一步减少自由度的潜力未被挖掘。

3. **单元类型限制**：当前实现依赖线性四面体单元和线性形函数，扩展到六面体或高阶形函数需要重新推导应变率度量和刚化判据。

4. **快速求解的保守性**：快速求解提供的应变率近似总是高估实际应变率，实践中需将 τ_E 设为 τ_R 的 1~2 个数量级以上。这意味着即使某些区域实际应变率已很小，也可能因近似高估而保持弹性，限制了极端加速比的实现。

5. **高度动态场景的退化**：当整个物体持续发生剧烈形变时（如流体状流动），几乎没有区域满足刚化条件，方法退化为全弹性仿真，无法提供加速。**Figure 8** 的落球实验定性展示了这一现象：更高的落球高度弹性化了更大区域。

![[assets/figures/papers/paper_list_l4_https_www_alexandremercieraubin_com_Work_papers_AdaptiveRigidification_repair/figures/005_Figure_3.jpg]]
*Figure 3: Per-frame speedup factors for blob, wheel, forest, octopus, and pachinko. Using conservative elastification and rigidification thresholds, we can obtain very accurate simulations in reduced computation time. Adaptive rigidification works for collision, rotation, frictional contact, and proves a large benefit in big scenes with local deformations, such as forest, where it is possible to elastify individual trees as needed. The green line in each plot shows mean speedup*

![[assets/figures/papers/paper_list_l4_https_www_alexandremercieraubin_com_Work_papers_AdaptiveRigidification_repair/figures/006_Figure_4.jpg]]
*Figure 4: (a) The rigidification threshold decides when rigid bodies are created, but it is the elastification threshold which is critical for deciding what regions will stay rigid. Lower values provide simulations that more faithfully reproduce the fully elastic behaviour, but at greater cost. (b) Rigidification takes place faster when there is higher damping in the simulation scenario, leading to greater speedups. (c) We observe very similar rigidification patters independent of the resolution of the mesh, while very coarse meshes rigidify more quickly because of resolution dependent stiffness and numerical damping. (d) Lower stiffness leads to larger and longer lived oscillations, while the dampin...*

![[assets/figures/papers/paper_list_l4_https_www_alexandremercieraubin_com_Work_papers_AdaptiveRigidification_repair/figures/007_Figure_7.jpg]]
*Figure 7: Rolling wheels with different elastification thresholds ???? fall at approximately the same time matching the fully elastic simulation. Lower thresholds lead to more accurate simulations. Here, adaptive simulations share a common rigidification threshold*

## 定位与知识库关联

本文的核心贡献在于改变了物理仿真中一个长期固定的“槽位”：**每个仿真元素（单元）的力学模型在运行时是静态预设的，而非动态可切换的**。在标准有限元仿真管线（如 **Baraff & Witkin, SIGGRAPH 1998** 的半隐式向后欧拉方法）中，所有单元始终被视为可变形弹性体，每一时间步都需要组装并求解完整的刚度矩阵系统。本文提出的自适应刚化方法将该槽位替换为：**基于运行时应变率监测的双阈值机制，使每个单元可在刚体与弹性体状态之间动态切换**。

这一改变的因果链条清晰：传统方法对“实际上不发生形变的区域”仍然执行昂贵的有限元计算（组装刚度矩阵、求解线性系统），造成了根本性的性能瓶颈。本文通过有限差分计算单元应变率的 Frobenius 范数，当该范数在连续若干帧内低于刚化阈值 $\tau_R$ 时，将对应单元标记为刚体候选，并通过广度优先搜索（BFS）将其合并为无铰链的连通刚体组件。弹性化方向则通过一次共轭梯度迭代的“快速求解”近似估计应变率，当估计值超过弹性化阈值 $\tau_E$ 时激活对应区域。这使得仿真系统从“全弹性求解”退化为“仅对活跃弹性自由度求解”的混合系统（Equation 11），自由度数大幅降低。

**相对已有工作的本质差异**：先前存在两类相关思路，但均未触及上述槽位。第一类是预计算的分层模型（如将物体预先划分为刚体区域和弹性区域），这要求用户在仿真前手动指定或离线分析，无法应对运行时受力情况变化导致的形变区域转移。第二类是基于模态分析或降阶模型的方法，它们虽然减少了自由度，但仍需预计算基底，且难以处理大变形和拓扑变化。本文的方法**不需要任何预计算或预建层次结构**，完全基于运行时状态自适应决策，这是其与已有工作的分水岭。

**知识库挂载点**：本工作可挂载到物理仿真知识库的以下节点：
- **混合刚-弹性体仿真**：作为运行时自适应混合仿真的代表性方法，与预定义刚体区域的方法（如动画中的刚体绑定）形成对照。
- **自适应仿真优化**：作为基于“非形变检测”的自适应降阶策略，与基于几何误差估计的网格自适应细分方法属于不同的自适应维度。
- **接触力学与碰撞处理**：方法中接触求解的“热身启动”和近似接触处理策略，可与更广泛的约束求解器优化文献关联。

**适用边界**：方法当前实现依赖线性四面体单元和线性形函数，论文明确指出扩展到六面体网格或高阶形函数尚需进一步研究。此外，刚体属性的计算仅在构成刚体的元素集合发生变化时才重新执行，未实现增量更新，这意味着在刚体频繁分裂的场景下效率会下降。快速求解提供的应变率近似总是高估真实值，因此实践中 $\tau_E$ 需设置为 $\tau_R$ 的 1~2 个数量级以上，这带来了保守性——部分本可弹性化的区域可能被延迟激活。方法仅合并相邻单元形成刚体，未考虑将相互接触但不相邻的单元合并以进一步减少自由度。

**后续启发**：本文打开了若干有价值的后续方向。其一，如何高效处理刚体组件的分裂（一个刚体因受力分裂为多个独立刚体）是直接的工程挑战。其二，将刚化逻辑从基于单元应变率推广到基于顶点运动监测，可能使方法适用于无网格或基于粒子的仿真框架。其三，将相互接触的多个物体合并为单个刚体以降低碰撞检测和接触求解开销，是一个有实际应用价值的扩展方向。其四，本文的双阈值机制本质上是一种“迟滞”策略（hysteresis），这为其他需要稳定性与响应性权衡的自适应系统提供了可借鉴的设计模式。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Adaptive_Rigidification_of_Elastic_Solids.pdf]]