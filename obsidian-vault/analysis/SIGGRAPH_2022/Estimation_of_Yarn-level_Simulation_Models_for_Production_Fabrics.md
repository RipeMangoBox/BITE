---
title: Estimation of Yarn-level Simulation Models for Production Fabrics
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Estimation_of_Yarn_level_Simulation_Models_for_Production_Fabrics.pdf
project_link: "http://mslab.es/projects/YarnLevelFabrics"
code_link: null
aliases:
- TSYLPETSI
- EYLSMPF
tags:
- SIGGRAPH_2022
- topic/benchmarks_datasets_evaluation
core_operator: 通过引入中间薄壳模型，将样片级非均匀变形物理测试数据转化为均匀应力‑应变目标，并利用周期边界条件纱线级仿真进行匹配；在此框架内对纱线模型进行最小但关键的扩展（两阶段拉伸刚度、独立弯曲刚度、双半径接触），使模型能够定量重现真实织物的非线性、各向异性力学响应。
primary_logic: 两步估计策略：先用扩展的各向异性 Neo‑Hookean 增强薄壳模型拟合真实测试数据并生成均匀变形目标，再利用扩展的纱线模型（两阶段拉伸、双半径接触）对这些均匀目标进行参数优化，实现了对真实机织物拉伸力学行为的首次定量纱线级复现。
claims:
- 薄壳面内模型在 33 种织物上的平均拉伸力误差为 17.59% ± 8.33%，平均正交压缩误差为 16.84% ± 8.11%，表明中介模型足够准确。
- 纱线级模型在舒适拉伸范围内有 24/33 织物的应力误差低于 10%（不包含弯曲误差训练），验证了两步拟合流程的整体有效性。
- 去除休息形状估计后拉伸误差急剧增大（Figure 17），证明该步骤对纱线级优化至关重要。
- 移除两阶段纱线拉伸模型导致整体拉伸误差大幅上升（Figure 16），证实了该扩展的必要性。
---

# Estimation of Yarn-level Simulation Models for Production Fabrics

> [!tip] 核心洞察
> 两步估计策略：先用扩展的各向异性 Neo‑Hookean 增强薄壳模型拟合真实测试数据并生成均匀变形目标，再利用扩展的纱线模型（两阶段拉伸、双半径接触）对这些均匀目标进行参数优化，实现了对真实机织物拉伸力学行为的首次定量纱线级复现。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向生产织物的纱线级仿真模型估计 |
| 英文题名 | Estimation of Yarn-level Simulation Models for Production Fabrics |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](http://mslab.es/projects/YarnLevelFabrics/) · [Project](http://mslab.es/projects/YarnLevelFabrics) |
| Topic | #topic/benchmarks_datasets_evaluation |
| Method | Two-step yarn-level parameter estimation via thin-shell intermediation |
| Dataset | Fabric dataset |

> [!tip] 效果简介
> - Fabric dataset (33 knitted swatches) 上，Stretch force relative error (thin‑shell in‑plane model) 17.59% ± 8.33%；Orthogonal compression relative error (thin‑shell in‑plane model) 16.84% ± 8.11%；Bending aspect ratio relative error (thin‑shell bending model) 5.61% ± 2.21%。

## 概要

真实生产织物的纱线级仿真面临双重瓶颈：纱线变形行为超出标准 Kirchhoff 杆模型的表达能力，且包含数万纱线的全样片仿真计算代价过高，使直接在仿真内环优化纱线参数不可行。本文提出一种两步估计策略——先以扩展的各向异性 Neo-Hookean 增强薄壳模型作为中介，拟合样片级非均匀拉伸与弯曲测试数据并生成均匀应力‑应变目标；再在周期边界条件下的纱线级仿真中，利用扩展的纱线模型（两阶段拉伸刚度、独立弯曲刚度、双半径接触）对这些目标进行参数优化。在 33 种针织物上，薄壳面内模型平均拉伸力误差为 17.59%，弯曲误差为 5.61%；纱线级模型在舒适拉伸范围内有 24/33 织物的应力误差低于 10%。消融实验证实，两阶段拉伸模型、休息形状估计及 Neo-Hookean 面积保持项对精度至关重要。该方法首次实现了对真实机织物拉伸力学行为的定量纱线级复现，但其几何初始化依赖手工注册，且尚未在全尺寸自由边仿真中验证。

## 核心方法与创新机理

### 问题瓶颈与整体策略

本文面临的核心瓶颈是双重困境：一方面，真实世界纱线（尤其是包芯纱等复合纱线）的力学行为极为复杂，表现出非线性、多阶段刚度转变和各向异性，远超标准 Kirchhoff 杆模型的表达能力；另一方面，包含数万根纱线的全织物样片级仿真计算代价极高，使得直接在纱线级参数上进行“仿真内环优化”（simulation-in-the-loop optimization）不可行。更棘手的是，物理拉伸测试中样片变形往往呈现空间非均匀性（如偏斜拉伸时的剪切集中和夹持端附近的弯曲，见图 2），这与纱线级周期仿真所依赖的均匀变形假设相矛盾。

针对这一瓶颈，作者提出**两步估计策略**：引入一个**中间薄壳模型**（intermediate thin-shell model）作为“翻译器”，将样片级非均匀物理测试数据转化为均匀应力–应变目标曲线，再在周期边界条件下对纱线级模型进行参数优化，使其匹配这些均匀目标。在此框架内，作者对薄壳模型和纱线模型分别进行了**最小但关键的扩展**，使整个管线能够定量重现真实机织物的非线性、各向异性力学响应。

### 管线模块顺序与因果关系

整个参数估计管线由五个顺序模块构成，模块间存在严格的因果依赖：

1. **数据采集与纱线几何初始化**（Section 4）：输入为编织指令（通过 STOLL M1plus 获取拓扑）、高分辨率照片（4912 × 3684 像素，1.8 μm/像素）和样片级物理测试数据；输出为手工注册的三维纱线曲线和拓扑结构。该模块为后续所有仿真提供几何基础。

2. **薄壳模型拟合**（Section 5）：在样片级有限元仿真框架内，通过仿真内环优化拟合物理测试的拉伸力–伸长量和正交压缩数据，估计薄壳面内参数（各向异性刚度矩阵和 Neo-Hookean 系数）和弯曲参数。该模块的输出是已标定的薄壳模型。

3. **均匀目标数据生成**（Section 5.1，式 3）：利用已标定的薄壳模型，在均匀变形假设下求解给定拉伸量和方向时的正交压缩量（使面内应变能最小化），生成完整的应力–应变曲线作为纱线级模型的优化目标。这一步将非均匀物理数据“翻译”为均匀目标，是连接薄壳模型与纱线级优化的关键桥梁。

4. **周期纱线级仿真与休息形状估计**（Section 7.1–7.2）：在周期边界条件下仿真纱线重复单元，计算宏观应力。同时通过交替进行平衡求解与休息形状重置，找到无应力且接近初始手工几何的纱线构型。休息形状估计是纱线级参数优化的必要前置步骤——消融实验（图 17）表明，跳过该步骤将导致拉伸误差急剧增大。

5. **纱线机械参数优化**（Section 7.3）：采用全局粒子群优化（PSO）加局部 COBYLA 精炼的两阶段策略，将纱线模型参数（两阶段拉伸刚度 $k_{s1}$、$k_{s2}$、转变应变 $\bar{\varepsilon}_s$、弯曲刚度 $k_b$、外接触半径 $R_1$ 和接触刚度 $k_{c1}$）拟合至薄壳均匀目标。消融实验（图 11）证实，仅使用局部非线性求解器会陷入局部最小值，而粒子群全局优化能有效避免。

### 关键创新：四个 Changed Slots

#### Slot 1：薄壳面内能量——从各向异性 StVK 到 Neo-Hookean 增强

基线模型为各向异性 Saint Venant-Kirchhoff（StVK）模型，其面内应变能密度仅包含二次形变项。该模型在拟合真实织物时存在严重缺陷：仿真中会出现不现实的 100% 压缩反转（图 5 右）。为解决此问题，作者引入 Neo-Hookean 面积保持项，将面内应变能扩展为：

$$\Psi_{\mathrm{inplane}} = \frac{1}{2} \varepsilon^T \begin{pmatrix} k_{xx} & k_{xy} & 0 \\ k_{xy} & k_{yy} & 0 \\ 0 & 0 & k_{ss} \end{pmatrix} \varepsilon + k_{n1}(J-1)^2 + k_{n2} \log^2 J$$

其中 $\varepsilon$ 为 Green-Lagrange 应变向量，$J$ 为面内变形梯度的行列式（面积变化率）。新增的 Neo-Hookean 项 $k_{n1}(J-1)^2 + k_{n2} \log^2 J$ 在面积趋近于零时产生无穷大势垒，有效阻止反转，同时不影响正常的应力–应变行为（图 5 左）。这一扩展是薄壳模型能够稳定拟合真实测试数据的前提。

#### Slot 2：纱线拉伸模型——从单相刚度到两阶段分段线性

基线模型假设纱线具有单一线性拉伸刚度，无法描述包芯纱等复合纱线的双相力学行为。显微照片（图 9）揭示了这一行为的物理来源：弹性单丝（氨纶）在低拉伸下提供柔软响应，而多丝刚性纱（涤纶）在高拉伸下承担主要载荷。为建模这一行为，作者将纱线段拉伸能量 $W_s$ 设计为三个线性区间的分段二次函数：

$$W_s = \begin{cases} \frac{1}{2} \bar{L} k_{s2} \varepsilon_s^2 & \varepsilon_s \leq 0 \\ \frac{1}{2} \bar{L} k_{s1} \varepsilon_s^2 & 0 \leq \varepsilon_s \leq \bar{\varepsilon}_s \\ \frac{1}{2} \bar{L} \left( k_{s2} (\varepsilon_s - \bar{\varepsilon}_s)^2 + 2 k_{s1} \bar{\varepsilon}_s \varepsilon_s - k_{s1} \bar{\varepsilon}_s^2 \right) & \varepsilon_s \geq \bar{\varepsilon}_s \end{cases}$$

其中 $\bar{L}$ 为纱线段休息长度，$\varepsilon_s$ 为拉伸应变，$k_{s1}$ 为低拉伸刚度，$k_{s2}$ 为高拉伸刚度（同时也用于压缩区间），$\bar{\varepsilon}_s$ 为刚度转变的临界应变。消融实验（图 16）表明，移除两阶段模型（即回退到单相刚度）会导致整体拉伸误差大幅上升，证实了该扩展的必要性。

#### Slot 3：纱线弯曲与接触模型的独立化与双半径扩展

标准 Kirchhoff 杆模型中弯曲刚度与拉伸刚度耦合（由截面几何决定），作者将其**解耦**，使弯曲刚度 $k_b$ 成为独立参数：

$$W_b = \frac{1}{2} \frac{2}{\bar{L}_a + \bar{L}_b} k_b \| \kappa - \bar{\kappa} \|^2$$

其中 $\kappa$ 为顶点处离散曲率，$\bar{\kappa}$ 为休息曲率。这一解耦允许弯曲行为独立于拉伸行为进行标定，对匹配真实织物的各向异性弯曲响应至关重要。

纱线–纱线接触模型同样进行了关键扩展：从单一半径势垒升级为**双半径两相接触**。接触能量定义为两个屏障势垒的组合：

$$W_c = k_{ci} \bar{L}_a \bar{L}_b \int_0^1 \int_0^1 f\left( \min\left( \frac{D}{2R_i}, 1 \right)^2 \right) da db$$

其中外半径 $R_1$ 对应柔软的初始接触响应（纱线表面绒毛和蓬松结构），内半径 $R_2$ 对应刚性核心的硬接触。通过调节两个势垒的刚度 $k_{c1}$ 和 $k_{c2}$，模型能够再现真实纱线从柔软接触到刚性压实的非线性接触响应。

### 训练/推理路径

**训练阶段**包含两个层次的仿真内环优化：

- **薄壳层**：以式 (2) 为目标函数，最小化仿真与物理测试的拉伸力误差和正交压缩误差，优化变量为面内刚度矩阵元素和 Neo-Hookean 系数。弯曲参数通过式 (5) 独立优化，匹配弯曲测试的梨形环纵横比。

- **纱线层**：以式 (11) 为目标函数，最小化周期纱线仿真与薄壳均匀目标之间的加权拉伸应力误差和压缩误差平方和。优化采用 PSO 全局搜索 + COBYLA 局部精炼的两阶段策略，有效避免局部最小值陷阱。

**推理阶段**：给定已标定的纱线级参数，在周期边界条件下直接运行纱线仿真即可预测织物在任意均匀变形下的宏观力学响应。作者明确指出，全尺寸非周期性仿真（含自由边和摩擦）尚未验证，因为缺少可靠的边界摩擦等建模元素。

![[assets/figures/papers/paper_list_l39_http_mslab_es_projects_YarnLevelFabrics/figures/001_Figure_1.jpg]]
*Figure 1: The figure shows our pipeline to fit yarn-level mechanical parameters to real-world knits, applied to a double knit pique fabric (DKP). (1) We take as input the fabric composition, knit schematics, high-resolution photographs, and swatch-level physical tests. (2) We fit a thin-shell model to the non-uniform physical data, and we use it to generate target uniform data. (3) Then, we fit the yarn-level model to the uniform data, leveraging periodic simulations to reduce the computational cost. (4) The images show the yarn model for DKP, under uniform stretch on the weft, bias, and warp directions*

![[assets/figures/papers/paper_list_l39_http_mslab_es_projects_YarnLevelFabrics/figures/005_Figure_5.jpg]]
*Figure 5: Our thin-shell formulation augments the anisotropic StVK model with a Neo-Hookean area-preservation term [Smith et al. 2018]. This term does not affect the stress-stretch behavior (left), but it eliminates inversion problems (right). Both models, with and without the Neo-Hookean term, are fitted to a double-knit interlock fabric (DKIN1). Without the Neo-Hookean term, the fitted model is stable but suffers inversion (i.e., it reaches 100% compression)*

![[assets/figures/papers/paper_list_l39_http_mslab_es_projects_YarnLevelFabrics/figures/009_Figure_9.jpg]]
*Figure 9: High-res photographs of a plated double-knit interlock fabric (DKIN8) at 20% warp stretch (left) and 150% weft stretch (right). A multi-filament stiff yarn, polyester, provides texture and stiff response under high forces. A single-filament flexible yarn, spandex (partially highlighted), provides flexible response under low forces. The flexible yarn is stretched during knitting, and then it compresses the stiff yarn as it retracts and relaxes into the stitch structure*

![[assets/figures/papers/paper_list_l39_http_mslab_es_projects_YarnLevelFabrics/figures/014_Figure_11.jpg]]
*Figure 11: The performance of our system with a local non-linear solver (purple) compared to a particle swarm optimization (blue), on an all-needle fabric (A2). Without the swarm optimization, the fitting gets stuck in a local minimum, causing the stretching error to blow up. The black bar denotes the transition from the “comfort” to the “power” range of stretches*

## 实验与关键发现

### 中介薄壳模型的拟合精度

薄壳面内模型在 33 种织物的样片级物理测试上取得了整体准确的拟合。拉伸力相对误差平均为 17.59% ± 8.33%，正交压缩相对误差平均为 16.84% ± 8.11%（Figure 6 后文本，Figure 13 汇总）。弯曲模型的拟合精度更高，弯曲梨形环高宽比的相对误差仅为 5.61% ± 2.21%（Section 5.2）。这些结果表明，各向异性 StVK + Neo‑Hookean 面积保持项的薄壳面内模型，以及各向异性离散壳弯曲模型，能够有效捕捉真实机织物在样片级非均匀变形下的力学行为。

消融实验揭示了 Neo‑Hookean 面积保持项的关键作用：移除该项后，虽然拟合的应力‑拉伸曲线无明显变化，但仿真中会出现不现实的 100% 压缩反转（Figure 5）。这证实了面积保持项在维持数值稳定性方面的必要性，而非仅仅影响拟合精度。

### 纱线级模型的整体拟合能力

在舒适拉伸范围内（不包含弯曲误差训练），纱线级模型在 33 种织物中有 24 种的拉伸应力误差低于 10%（Figure 15，Section 8）。整体拉伸应力误差为 10.40% ± 5.27%，压缩误差为 16.28% ± 11.58%（Table 1 “No bending” 列）。考虑到真实世界织物的高度非线性和各向异性，这一结果验证了两步估计策略——薄壳中介生成均匀目标 + 周期纱线仿真参数优化——的有效性。

![[assets/figures/papers/paper_list_l39_http_mslab_es_projects_YarnLevelFabrics/figures/016_Figure_15.jpg]]
*Figure 15: Overall ability of our yarn-level solver to reproduce the corresponding real-world behaviors of materials in our database. The ??-axis is error percentage, and the ??-axis lists specific types of fabric in our database. The error is relative to the maximum ground-truth datum in the comfort stretch per pattern (see Section 7.3.1)*

Figure 14 展示了所有 33 种织物上估计的纱线级参数值分布，包括两阶段拉伸刚度 $k_{s1}$、$k_{s2}$、过渡应变 $\bar{\varepsilon}_s$、独立弯曲刚度 $k_b$、外接触半径 $R_1$ 及对应刚度 $k_{c1}$。参数在不同织物类型间展现出显著差异，表明模型能够适应从单面平纹到双面衬纬等多种编织结构。

### 关键消融实验

**两阶段纱线拉伸模型**（Figure 16）：将两阶段拉伸模型替换为单一线性刚度后，整体拉伸误差大幅上升，压缩误差也随之增加。这证实了包芯纱的双相力学行为——柔性纱线在低拉伸下提供柔软响应，刚性纱线在高拉伸下提供强力支撑——是真实织物非线性响应的核心来源（Figure 9 显微照片直观展示了这一机制）。

**休息形状估计**（Figure 17）：移除休息形状优化步骤后，拉伸误差急剧增大，压缩误差也显著升高。这是因为手工注册的初始纱线几何并非无应力状态；直接在该几何上优化力学参数会导致系统性的应力偏差。交替进行平衡求解与休息形状重置，是找到接近初始几何的无应力构型的必要步骤。

**全局优化策略**（Figure 11）：仅使用局部非线性求解器（COBYLA）会使优化陷入局部最小值，导致拉伸误差爆炸。结合粒子群全局优化（PSO）能够有效避免该问题，在舒适拉伸范围内将误差控制在较低水平。Figure 11 中黑色竖线标记了从“舒适”到“强力”拉伸范围的过渡。

**弯曲误差项的加入**（Table 1, Figure 18）：在纱线级目标函数中加入弯曲误差项后，弯曲拟合显著改善，但拉伸误差恶化。Table 1 显示，“No bending”列的整体拉伸应力误差为 10.40%，“Bending”列升至更高水平；而弯曲误差则从较高值大幅下降。这表明在当前模型框架下，拉伸精度与弯曲精度之间存在明显的权衡关系，难以同时优化。

### 失败模式与适用边界

**卷曲织物的弯曲建模困难**：单面平纹（single jersey）织物在拉伸测试中表现出强烈的面外卷曲倾向（Figure 7），这不仅影响弯曲测试的准确测量，也使薄壳弯曲模型的拟合精度受限。当前的弯曲能量密度 $\Psi_{\mathrm{bending}} = k_\theta \kappa^2$ 不支持自然卷曲的休息状态。

**未建模的滞后与卸载行为**：物理测试仅记录加载曲线，未考虑织物的滞后（hysteresis）现象。这意味着拟合的模型参数仅适用于单调加载场景，无法准确预测卸载路径和循环加载行为。

**全尺寸非周期性仿真的验证缺失**：纱线级参数估计仅在周期边界条件下进行验证。由于缺少可靠的自由边处理和纱线间摩擦模型，尚未在全尺寸、含自由边的仿真中与原始样片级物理测试进行直接对比。这限制了模型在真实服装仿真等非周期性场景中的直接适用性。

**几何初始化的主观偏差**：手工注册纱线几何每个织物需 1–10 小时，可能引入人为偏差。Figure 10 展示了手工几何与优化后休息形状的对比，两者差异的大小直接影响后续参数优化的收敛质量。

**多层与复杂编织的未覆盖**：当前方法针对单层纬编织物设计，多层织物、三维编织以及经编结构等更复杂的织物类型仍需进一步研究。这些结构中的纱线遮蔽和复杂接触将显著增加几何初始化和力学建模的难度。

![[assets/figures/papers/paper_list_l39_http_mslab_es_projects_YarnLevelFabrics/figures/019_Figure_16.jpg]]
*Figure 16: The performance of our optimization with and without our biphasic yarn-stretching model, on an all-needle fabric (A2). Omitting the more complex yarn model massively increases the overall stretching error and adds to the compression error (purple line)*

## 定位与知识库关联

本文解决的核心问题是：**真实生产织物的纱线级力学参数估计**，其本质瓶颈在于真实纱线的复杂非线性变形行为（包芯纱的双相拉伸、纱线间多级接触）超出标准 Kirchhoff 杆模型的表达能力，且包含数万纱线的全织物样片级仿真计算代价极高，使得直接在纱线级参数上进行仿真内环优化不可行。

### 相对已有工作的本质差异与改变的 slot

在图形学织物仿真领域，已有纱线级模型（如 Kaldor et al. 2008, 2010; Cirio et al. 2014, 2016, 2017）普遍采用标准 Kirchhoff 杆模型，其**拉伸刚度与弯曲刚度耦合**（弯曲刚度由拉伸刚度与截面几何推导），且拉伸响应为**单一线弹性**、纱线接触为**单一半径势垒**。这些模型在定性动画中表现良好，但**从未在定量力学层面与真实织物测试数据进行系统对比验证**。

本文改变的关键 slot 包括：

1. **薄壳面内模型**：从各向异性 StVK（无面积保持）→ 各向异性 StVK + Neo-Hookean 面积保持项。该 slot 的改变直接解决了纯 StVK 模型在仿真中出现不现实 100% 压缩反转的问题（Figure 5），使中介模型能够稳定生成均匀变形目标数据。

2. **纱线拉伸模型**：从单一线性刚度 → 三段分段线性刚度（压缩区、低拉伸区 $k_{s1}$、高拉伸区 $k_{s2}$，以 $\bar{\varepsilon}_s$ 为分界）。该 slot 的改变源于对包芯纱微观结构的观察（Figure 9）：柔性氨纶丝提供低力下的弹性响应，刚性涤纶多丝提供高力下的刚度支撑。消融实验（Figure 16）证实，移除该两阶段模型导致整体拉伸误差大幅上升。

3. **纱线弯曲刚度**：从与拉伸刚度耦合（Kirchhoff 杆推导）→ 独立各向同性弯曲刚度 $k_b$。该 slot 的解耦使得弯曲行为可以独立拟合，避免拉伸参数估计误差传导至弯曲响应。

4. **纱线接触模型**：从单一半径势垒 → 双半径两相接触（软大半径势垒 $R_1$ + 硬小半径势垒 $R_2$）。该 slot 的改变使模型能够区分纱线表面绒毛的柔软接触与纱线芯部的刚性接触。

### 知识库挂载点

本文在织物仿真知识库中的挂载点位于**多尺度织物建模**与**参数估计**的交叉节点：

- **向上挂载**：连接“薄壳中介模型”节点。本文借鉴了 Miguel et al. (2012, 2013) 的样片级薄壳参数拟合框架，但将其扩展为**各向异性 + 面积保持**的形式，并赋予其新的角色——作为从非均匀物理测试数据到均匀纱线级仿真目标的“翻译器”。这一中介策略与 Sperl et al. (2020) 的均质化方法形成互补：后者通过周期边界纱线仿真直接计算宏观应力，本文则反向利用该均质化框架进行参数优化。

- **向下挂载**：连接“纱线级本构模型”节点。本文在标准 Kirchhoff 杆模型（Kaldor et al. 2008; Bergou et al. 2008）基础上进行了**最小但关键的扩展**（两阶段拉伸、独立弯曲、双半径接触），这些扩展的物理依据来自对真实包芯纱微观结构的观察（Figure 9），而非纯粹的经验拟合。

- **横向关联**：与“数据驱动的材质参数估计”节点（如 Wang et al. 2011 的薄壳参数估计、Miguel et al. 2012 的布料参数拟合）关联，但本文首次将此类方法推进到**纱线级别**，且面向**生产级针织物**的多样性（33 种织物，涵盖全针、双面衬纬、单面平纹、Links 等多种组织结构）。

### 适用边界与限制

1. **仅适用于周期性针织物**：方法假设织物样片可近似为周期性重复图案，因此不适用于随机纤维排列的非织造布或具有大尺度结构变化的织物。

2. **仅使用加载曲线**：物理测试仅记录加载曲线，未建模卸载及滞后（hysteresis）现象，因此估计的参数仅适用于单调加载场景，不适用于循环加载或塑性变形。

3. **几何初始化依赖人工**：手工注册纱线几何每个织物需 1–10 小时，可能引入人为偏差，且不适用于多层、三维编织或经编等高度遮蔽结构。

4. **未在全尺寸非周期性仿真中验证**：纱线级参数估计仅在周期边界条件下进行，未在包含自由边的全尺寸仿真中与物理测试直接对比，因为缺少可靠的边界摩擦等建模元素。

5. **弯曲与拉伸精度的权衡**：在纱线级目标函数中加入弯曲误差项虽能大幅改善弯曲拟合，但使拉伸误差变差（Table 1, Figure 18），表明当前模型在两个力学维度间存在固有张力。

### 后续工作启发

本文的“两步中介估计”策略为后续研究提供了可泛化的方法论框架：**当目标模型的仿真代价过高而无法直接进行仿真内环优化时，可引入一个计算代价低的中介模型，在物理测试数据与目标模型之间建立映射**。这一策略可推广至其他层级的多尺度材质建模问题（如纤维级→纱线级、纱线级→织物级）。

开放问题包括：(1) 如何设计对跨越多个数量级的弯曲刚度更鲁棒的误差度量；(2) 能否直接利用单纱拉伸等纱线级测试数据约束参数，减少对样片级中介模型的依赖；(3) 如何将方法扩展至多层、三维编织及经编结构。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Estimation_of_Yarn_level_Simulation_Models_for_Production_Fabrics.pdf]]