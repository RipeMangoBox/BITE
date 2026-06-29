---
title: "Scintilla: Simulating Combustible Vegetation for Wildfires"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/Scintilla_Simulating_Combustible_Vegetation_for_Wildfires.pdf
project_link: null
code_link: null
aliases:
- Scintilla
tags:
- SIGGRAPH_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 燃料湿度、边界燃料层（草、细燃料、腐殖质）的分布与燃烧速率直接控制火蔓延和火行为。
primary_logic: 提出统一多域表述，将3D植物模块、2D地表燃料图和3D大气网格耦合，通过基于活力模型的燃料湿度、边界燃料层和飞火扩散模型，实现地表火、树冠火等多种野火类型的真实模拟。
claims:
- 模拟火线与可控燃烧实验的火线形状和进展高度一致。
- 模拟火线蔓延速率与Rothermel冠层燃料模型吻合良好。
- 飞火模型产生新火点，导致火线更线性且出现点状火。
- Rothermel冠层燃料模型 上 火线蔓延速率 = 模拟结果与Rothermel曲线吻合
---

# Scintilla: Simulating Combustible Vegetation for Wildfires

> [!tip] 核心洞察
> 提出统一多域表述，将3D植物模块、2D地表燃料图和3D大气网格耦合，通过基于活力模型的燃料湿度、边界燃料层和飞火扩散模型，实现地表火、树冠火等多种野火类型的真实模拟。

| 字段 | 内容 |
|------|------|
| 中文题名 | Scintilla: 模拟可燃植被的野火仿真 |
| 英文题名 | Scintilla: Simulating Combustible Vegetation for Wildfires |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://wp.faculty.wmi.amu.edu.pl/Scintilla.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Scintilla |
| Dataset | Rothermel冠层燃料模型 |

> [!tip] 效果简介
> - Rothermel冠层燃料模型 上，火线蔓延速率 模拟结果与Rothermel曲线吻合 vs Rothermel模型预测值 (定性吻合，小风速下略低)。
> - 可控燃烧实验 (Vanella et al. 2021) 上，火线轮廓相似性 火线形状与实验数据高度一致，进展精确 vs Vanella et al. 仿真结果 (teal contour) (更接近真实火线形状)。
> - 森林管理场景（自有设置） 上，火灾强度与蔓延 移除中间树木和灌木降低火灾强度与蔓延 vs 未处理场景 (强度与蔓延显著降低)。

## 概要

现有野火模拟方法未能协同考虑多种地表燃料类型（草、细燃料、腐殖质）及其湿度分布对火势蔓延的影响，导致模拟真实性受限。本文提出**Scintilla**，一种统一多域表述的野火仿真框架，将3D植物模块、2D地表燃料图和3D大气网格耦合，通过基于活力模型的燃料湿度计算、边界燃料层（草、细燃料、腐殖质）以及飞火扩散模型，实现从地表火到树冠火等多种野火类型的真实模拟。实验表明，模拟火线形状与可控燃烧实验高度一致，火线蔓延速率与Rothermel冠层燃料模型吻合良好；飞火模型可产生新火点，导致更线性的火线及点状火。方法定位上，Scintilla在**Hädrich et al.**（ACM Trans. Graph. 2021）的精细植被模拟基础上，新增了燃料湿度模型、边界燃料层和飞火模型三个关键模块，并将数值对流方案从半拉格朗日方法升级为无条件稳定的MacCormack格式。

## 核心方法与创新机理

### 问题瓶颈与核心思路

现有野火模拟方法（如 **Hädrich et al.**, ACM Trans. Graph. 2021）虽然能够生成精细的3D植被几何，但未能协同考虑多种地表燃料类型（草、细燃料、腐殖质）及其湿度分布对火势蔓延的影响。这导致模拟无法真实再现从地表火到树冠火的完整火行为谱系。Scintilla 的核心洞察在于：**燃料湿度、边界燃料层的分布与燃烧速率直接控制火蔓延和火行为**，因此必须建立一个统一的多域表述，将3D植物模块、2D地表燃料图和3D大气网格耦合在一起，并通过基于活力的燃料湿度模型、边界燃料层和飞火扩散模型，实现多种野火类型的真实模拟。

### 整体框架与模块顺序

Scintilla 的模拟管线包含六个顺序耦合的模块，其因果关系链为：**输入初始化 → 边界燃料层计算 → 燃料湿度分配 → 耦合燃烧与传热 → 飞火粒子模拟 → 流体动力学与烟扩散**。下面逐一展开各模块的设计机理与关键公式。

#### 模块一：植被、地形、土壤水、大气初始化

系统输入包括数字高程模型（DEM）、土壤水分布图、基于多尺度植物图（multi-scale plant graphs）的植被表示、大气数据结构以及土壤图。植被采用 **Makowski et al. 2019** 提出的基于活力的层次化离散图表示，每株植物由模块（module）和枝段（branch segment）组成，模块是燃烧模拟的基本单元。这一模块化表示使得植物几何可以复用，同时支持局部环境适应。

#### 模块二：边界燃料层计算（草、细燃料、腐殖质）

这是 Scintilla 相对于先前工作的第一个关键创新槽位（changed slot）。传统方法仅模拟3D树木和灌木，忽略了地表可燃物对火行为的关键影响。Scintilla 引入**边界燃料层（boundary fuel layer）**，用2D空间地图分别表示草、细燃料和腐殖质三层。

**草生物量**由温度、光照和土壤水的正态分布共同决定，公式为：

$$B_{g}(x,y) = \frac{N_{T}(T_{a}) \cdot N_{L}(L) \cdot N_{P}(q_{w})}{N_{T}(T_{A}) \cdot N_{L}(L_{A}) \cdot N_{P}(P_{A})} \cdot \varpi_{g}$$

其中 $N_T$、$N_L$、$N_P$ 分别为温度、光照、土壤水的正态分布函数，分母为理想条件下的归一化值，$\varpi_g$ 为单位面积理想草生物量。该公式的因果含义是：草只在温度适宜、光照充足、土壤水分适当的区域生长，灌木遮蔽区域草生物量自然降低。

**细燃料**则通过高斯核将3D植物模块的生物量映射到2D地面：

$$G_{f}(M, x, y) = \frac{\varpi_{f}}{2\pi\sigma_{f}^{2}} e^{-\frac{(x-x_{M})^{2}+(y-y_{M})^{2}}{2\sigma_{f}^{2}}} \cdot M_{M} \cdot \varphi_{f}$$

其中 $M_M$ 为模块 $M$ 的生物量，$\varphi_f$ 为物种特定的细燃料转化系数，$\sigma_f$ 控制空间扩散范围。这一映射的因果逻辑是：树木和灌木的枯枝落叶在地表积累形成细燃料，其空间分布与上方植被的位置和生物量直接相关。腐殖质层则基于细燃料的长期累积和分解过程计算。

Fig. 5 展示了三层边界燃料的典型空间分布：草避开灌木区域，而细燃料和腐殖质则集中在灌木周围。

![[assets/figures/papers/paper_list_l34_https_wp_faculty_wmi_amu_edu_pl_Scintilla_html/figures/005_Figure_5.jpg]]
*Figure 5: An example arrangement of duff (a), grass (b), and fine fuel (c), generated using our boundary fuel model. Grass is avoiding the regions where shrubs are located (dark spots), whereas duff and fine fuel are found more readily around the locations of shrubs*

#### 模块三：燃料湿度计算（环境适应、光通量、活力、蒸腾）

这是第二个关键创新槽位。先前方法对燃料湿度采用简单假设或无模型，Scintilla 提出了一个基于植物生理过程的**四步湿度计算模型**：

1. **环境适应计算**：根据海拔、温度等气候因子计算每株植物的气候适应参数，高海拔寒冷区域的植物适应度较低（Fig. 3b 中浅红色表示）。
2. **局部光照近似**：计算每个模块接收的光通量，考虑上层枝叶的遮蔽效应。
3. **活力分布**：将植物的整体活力沿枝图分配到每个模块，活力高的模块具有更强的水分获取能力。
4. **时变湿度**：基于蒸腾作用计算模块湿度的动态变化。

模块初始湿度由活力 $V_{\mathcal{M}}$、物种水分系数 $\psi$、模块质量 $M_{\mathcal{M}}$ 和最小湿度 $W_{min}$ 决定：

$$W_{\mathcal{M}}(V_{\mathcal{M}}, M_{\mathcal{M}}) = \log(1 + e^{V_{\mathcal{M}}}) \cdot \psi \cdot M_{\mathcal{M}} + W_{min} \cdot \frac{1}{1 + e^{-V_{\mathcal{M}}}}$$

该公式使用 softplus 函数 $\log(1+e^{V})$ 和 sigmoid 函数 $1/(1+e^{-V})$ 实现活力到湿度的平滑映射：活力越高，湿度越接近 $\psi \cdot M_{\mathcal{M}}$ 主导的线性增长；活力越低，湿度趋近于 $W_{min}$。模拟过程中，模块湿度因蒸腾作用而变化：

$$\frac{dW_M}{dt} = \kappa_w^m(T_M) \cdot A$$

其中 $\kappa_w^m$ 为温度相关的蒸发函数，$A$ 为模块表面积。这一湿度模型是连接植被生理状态与火行为的核心因果节点：湿度高的模块更难点燃，从而在模拟中自然形成防火屏障。

#### 模块四：耦合燃烧与传热

燃烧过程在多域框架中统一求解。有机材料在高温下分解为焦炭、水蒸气和可燃气体，反应速率 $k$ 取决于温度 $T_{\mathcal{M}}$、湿度 $\mathcal{W}_{\mathcal{M}}$ 和风速 $u$：

$$k(T_{\mathcal{M}}, \mathcal{W}_{\mathcal{M}}, u) = \eta(u) \cdot S_{T_{0},T_{1}}(T_{\mathcal{M}}) \cdot S_{W_{0},W_{1}}(\mathcal{W}_{\mathcal{M}})$$

其中 $\eta(u)$ 为风速修正因子，$S_{T_0,T_1}$ 和 $S_{W_0,W_1}$ 分别为温度和湿度的平滑阶跃函数，定义了点燃和熄灭的阈值区间。模块质量变化率由反应速率和表面积 $A$ 决定：

$$\frac{\mathrm{d}M}{\mathrm{d}t} + k(T_{M}, W_{\mathcal{M}}, u) c A = 0$$

其中 $c$ 为燃料类型系数。该方程描述了燃烧过程中模块质量的指数衰减，湿度通过 $k$ 中的 $S_{W_0,W_1}$ 项直接调控衰减速率。

传热在3D植物模块、2D边界燃料层和3D大气网格之间通过辐射、对流和传导耦合求解。边界燃料层的燃烧释放热量加热大气网格，大气网格中的热空气又通过对流加热植物模块，形成正反馈循环。

#### 模块五：飞火粒子模拟

这是第三个关键创新槽位。飞火（ember/firebrand）是野火跨越防火带、产生新火点的主要机制，先前图形学方法均未建模。Scintilla 的飞火模型包含三个物理过程：

**产生**：飞火粒子产生速率与燃料质量损失率成正比：

$$\frac{\mathrm{d}N_{e}}{\mathrm{d}t} = c_{e} \frac{\mathrm{d}M}{\mathrm{d}t}$$

**输运**：飞火粒子受风场和热羽流驱动，采用拉格朗日粒子追踪。Fig. 6 展示了不同风速下飞火轨迹的差异：低风速时轨迹更随机（热羽流主导），高风速时飞火被携带更远距离。

**点火**：飞火能否引燃新燃料取决于其半径是否超过临界值 $r_{cr}$：

$$r_{cr} = \delta_{cr} \sqrt{ \frac{K_{gg}}{\rho_{g} A_{g} \Delta H_{g}} \frac{R T_{e}^{2}}{E} \exp\left(\frac{E}{R T_{e}}\right) }$$

该公式基于热爆炸理论（thermal explosion theory），其中 $K_{gg}$ 为燃料导热系数，$\rho_g$ 为燃料密度，$A_g$ 为指前因子，$\Delta H_g$ 为燃烧热，$E$ 为活化能，$T_e$ 为飞火温度。飞火半径大于 $r_{cr}$ 时，其热释放速率超过散热速率，可引发自持燃烧。

#### 模块六：流体动力学与烟扩散（MacCormack对流）

这是第四个创新槽位。先前方法使用半拉格朗日（semi-Lagrangian）方案求解对流，存在数值耗散导致动能损失。Scintilla 改用**无条件稳定的 MacCormack 格式**配合二阶 RK-2 回追，显著减少数值耗散。实验表明，MacCormack 方案的平均动能比半拉格朗日方案高 19.35%，这对飞火输运和火羽流模拟尤为关键（Fig. 19 展示了改进前后的流线对比）。

### 模块间因果关系总结

整个管线的因果链可概括为：**边界燃料层的空间分布（模块二）和燃料湿度（模块三）共同决定燃烧的起始位置和速率（模块四）；燃烧释放的热量驱动大气对流（模块六），同时产生飞火（模块五）；飞火在风场（模块六）作用下输运并引发新火点，反馈回燃烧模块；湿度因蒸腾（模块三）动态降低，进一步加速燃烧，形成正反馈直至燃料耗尽**。这一闭环使得 Scintilla 能够自发涌现出地表火向树冠火的转变、飞火跳跃、火线指状延伸等复杂火行为。

![[assets/figures/papers/paper_list_l34_https_wp_faculty_wmi_amu_edu_pl_Scintilla_html/figures/001_Figure_1.jpg]]
*Figure 1: A temporal progression of a wildfire generated with our framework. Modeling different types of fuel and vegetation with detailed geometry enables simulating complex wildfire behavior ranging from harmless surface fires to raging crown fires*

![[assets/figures/papers/paper_list_l34_https_wp_faculty_wmi_amu_edu_pl_Scintilla_html/figures/002_Figure_2.jpg]]
*Figure 2: An overview of our method. A user specifies the initialization of vegetation, soil and atmosphere models as inputs. We then initialize the boundary fuel model. Wildfires are simulated by representing the fuel, water and other wildfire related quantities using a multi-domain approach, which includes 3D modules for representing plants, 2D maps for representing the soil and the forest floor, and a 3D grid for representing the atmosphere*

![[assets/figures/papers/paper_list_l34_https_wp_faculty_wmi_amu_edu_pl_Scintilla_html/figures/006_Figure_6.jpg]]
*Figure 6: 100 Firebrand trajectories depicted as blue lines for various vertical wind profiles of varying speeds ranging from 0, 20, 40, 60, 100, and 150 km/h. The trajectories are more random with lower velocities compared to high wind velocities, but at higher wind speeds the embers are carried a longer distance. The range of how far the embers travel is given in meters (m)*

## 实验与关键发现

Scintilla 的实验验证围绕三个核心维度展开：与经典物理模型的定量吻合、与真实可控燃烧实验的形态对比，以及通过消融实验揭示各新增模块（飞火、燃料湿度、边界燃料层）对火行为的因果调控作用。

### 与 Rothermel 冠层燃料模型的速率对比

论文将模拟火线蔓延速率与 **Rothermel 冠层燃料模型**（Bishop 2007 配置）进行对比。在四种不同风速条件下，Scintilla 模拟的火线蔓延速率与 Rothermel 模型预测曲线定性吻合良好（Fig. 8 左）。在低风速区间，模拟值略低于模型预测值，这可能是由于数值扩散或边界燃料层的简化所致，但整体趋势一致，验证了耦合燃烧模型在冠层火场景中的物理合理性。该实验使用 Fig. 9 所示的森林斑块场景，火线从左侧向右推进，蔓延速率近似恒定，为数据点提取提供了稳定条件。

![[assets/figures/papers/paper_list_l34_https_wp_faculty_wmi_amu_edu_pl_Scintilla_html/figures/008_Figure_8.jpg]]
*Figure 8: Left: A comparison of the rate of fire spread of the fireline using Rothermel’s model configured for crown fuel [Bishop 2007] (solid line) and our simulation results for four experiments with varying wind speeds. Our simulation results correspond well to Rothermel’s model. Right: A comparison of the maximum extent of firelines in our simulation (solid line) to measurements of the controlled burn experiment shown in Fig. 13 at three different time points (blue dots). Our simulation captures accurately the linear progression of the fireline*

### 与可控燃烧实验的火线形态验证

更具说服力的验证来自与 **Vanella et al. (2021)** 可控燃烧实验的对比。Fig. 13 并排展示了真实燃烧照片、Vanella et al. 的仿真结果（青色轮廓）以及 Scintilla 的模拟结果。Scintilla 不仅捕捉到了火线推进的主要特征，而且在三个时间点的火线轮廓与真实火线的形状和进展高度一致（Fig. 21）。定量对比显示，Scintilla 的火线轮廓（红色）在形状和线性推进方面均优于 Vanella et al. 的仿真结果（青色轮廓），更贴近实验测量点（圆点、方块、三角标记）。这一结果直接支撑了核心主张：边界燃料层和燃料湿度模型的引入显著提升了火线形态的模拟保真度。

### 飞火模型的定量消融

飞火（ember）模型的消融实验揭示了其对燃烧动力学的非线性影响。Fig. 20 展示了有无飞火模型下生物质损失随时间的演化曲线。无飞火模型时，生物质损失曲线呈平滑的山丘状；加入飞火模型后，曲线形态变得更为复杂，反映了飞火引发的新火点对燃烧进程的非线性贡献。有趣的是，在干燥场景下（红色曲线），有无飞火模型的差异减小——这表明当整体燃料湿度较低时，火蔓延主要由主火线驱动，飞火的增量效应被削弱。

Fig. 14 的可视化对比进一步展示了飞火与燃料湿度的交互效应：(g-i) 中飞火模型在火线前方产生新的点状火（spot fire），导致火线更加线性；(j-l) 中叠加从左向右的风场后，飞火被输运至更远处，新火点出现在火线前方更远位置。燃料湿度分布与飞火模拟的交互产生了复杂的火线形状。

### 燃料湿度调控火灾类型

通过调节边界燃料层和植物模块的整体燃料湿度，Scintilla 能够模拟从地表火到树冠火的连续谱系。Fig. 16 展示了五种不同湿度配置下的火灾动力学，Table 1 给出了对应的参数配置。在低湿度条件下，火灾迅速转变为活跃的树冠火（c-e）；在高湿度条件下，火势保持为地表火或被动树冠火（a-b）。这一结果表明燃料湿度是控制火灾类型转换的关键因果旋钮，验证了基于活力的湿度计算模型的有效性。

![[assets/figures/papers/paper_list_l34_https_wp_faculty_wmi_amu_edu_pl_Scintilla_html/figures/017_Table_1.jpg]]
*Table 1: Overview of the different parameter value configurations of simulations presented in Fig. 16. For each scene, the spatial dimensions are*

### 森林管理场景的定性验证

Fig. 11 展示了不同人为干预场景下的火行为变化：(a) 未处理的密集林地中，丰富的垂直燃料（不同高度的树木）导致高强度、快速蔓延的火灾；(b) 移除中等大小树木后，火强度和蔓延速度显著降低；(c) 进一步清除灌木后，垂直燃料稀缺，火灾主要表现为低强度的地表火。这一实验虽为定性展示，但直观地验证了边界燃料层与 3D 植物模块耦合模型对燃料结构变化的敏感性。

### 数值方案改进的定量收益

将半拉格朗日对流方案替换为无条件稳定的 **MacCormack 格式** 并配合二阶 RK-2 回追后，模拟的平均动能提升了 **19.35%**（Sec 6.1）。Fig. 19 的并排对比显示，新数值方案下流线更加丰富，树冠周围的湍流结构更精细，表明数值扩散的减少使得火致对流得到了更准确的解析。这一改进对于飞火输运和烟扩散的模拟尤为关键，因为飞火轨迹对风场细节高度敏感（Fig. 6, Fig. 7）。

### 性能特征与适用边界

Table 2 报告了不同场景的性能数据。最大场景包含约 20 万棵植物、近 100 万个模块，模拟时间步长为 45 秒，可在交互速率下运行。然而，论文明确指出**内存限制**是当前方法的主要瓶颈，难以模拟更大地理范围。此外，土壤模型采用简化处理，未能精细模拟地火（ground fire）行为；飞火对植被的点火使用了稳态抽象，可能在高湍流条件下引入误差；火旋风等火致天气现象未被包含。这些限制界定了 Scintilla 的适用边界：适用于中尺度（数百米至数公里）的森林-草地交界野火模拟，在极端天气条件或需要精细土壤火模拟的场景中需谨慎对待。

## 定位与知识库关联

Scintilla 的核心定位是**在 Hädrich et al. (ACM Trans. Graph. 2021) 的模块化植被野火框架上，补全了三个关键缺失的物理槽位**，从而使模拟从“仅能表现树冠火”扩展到“地表火—树冠火—飞火”的完整野火类型谱系。Hädrich et al. 的方法已具备精细的 3D 植物模块表示和基本的大气耦合，但存在一个根本瓶颈：**缺乏对地表燃料层（草、细燃料、腐殖质）的显式建模，以及驱动火行为差异的燃料湿度空间分布机制**。这导致其模拟无法区分地表火与树冠火，也无法解释为何同一场景中某些区域燃烧而相邻区域幸存。

Scintilla 改变的三个决定性 slot 如下：

1. **燃料湿度模型**（从“无/简单假设”到“基于活力的四步计算”）：Hädrich et al. 未对植物模块的湿度进行空间差异化建模。Scintilla 引入了环境适应→光通量→活力分配→蒸腾驱动的时变湿度管线（Sec 5.3），使得同一场景中不同位置的同种植物可因微气候差异而具有不同可燃性。这一 slot 是**从“均匀可燃假设”到“生态驱动的异质可燃性”的范式转换**，直接决定了火线形状的复杂性和火灾类型的分化（Fig. 14, Fig. 16）。

2. **边界燃料层**（从“无”到“2D 多类型地表燃料图”）：这是 Scintilla 与 Hädrich et al. 最显著的结构性差异。Scintilla 增加了三个 2D 地图——草、细燃料、腐殖质——作为燃烧耦合的新域（Fig. 2 中的 Boundary Fuel Layer）。草的生物量由温度、光照、土壤水的正态分布函数决定（Eq. 6），细燃料由 3D 模块质量经高斯核投影得到（Eq. 7）。这一 slot 使得模拟能够表现草地火蔓延、林缘火线推进、以及地表燃料对树冠火触发的控制。

3. **飞火/余烬模型**（从“无”到“产生—输运—点火物理模型”）：Hädrich et al. 无法模拟火线前方的点状火。Scintilla 增加了飞火粒子管线（Sec 5.7），其产生率与燃料质量损失率成正比（$\frac{\mathrm{d}N_{e}}{\mathrm{d}t} = c_{e} \frac{\mathrm{d}M}{\mathrm{d}t}$），输运受风场和湍流影响，点火由临界半径判据决定（Eq. 25）。这一 slot 使模拟火线形状从平滑弧线变为带有突前火点的复杂形态（Fig. 14 g-l）。

此外，Scintilla 还将数值对流方案从半拉格朗日方法替换为无条件稳定的 MacCormack 格式及二阶 RK-2 回追，使平均动能提高 19.35%（Sec 6.1），但这属于工程改进而非概念性 slot 变化。

**与 Vanella et al. (2021) 的关系**：Vanella et al. 是 Scintilla 用于可控燃烧验证的对比方法（Fig. 13, Fig. 21）。Scintilla 的火线轮廓比 Vanella et al. 更接近真实实验数据（Fig. 21 中红色轮廓 vs. 蓝绿色轮廓），但这是定性视觉比较，缺乏定量指标。

**知识库挂载点**：Scintilla 应挂载在**基于物理的野火模拟**节点下，与以下工作形成知识关联：
- **Hädrich et al. (ACM Trans. Graph. 2021)**：提供模块化植被表示和基础燃烧框架，Scintilla 是其直接扩展。
- **Rothermel 模型 (1972) 及其冠层燃料配置 (Bishop 2007)**：Scintilla 的火线蔓延速率验证基准（Fig. 8 左），表明其模拟在宏观行为上与经典经验模型一致。
- **Makowski et al. (2019) 的活力驱动植物生长模型**：Scintilla 的湿度计算管线借用了其活力分配框架，但将其从生长驱动改为可燃性驱动。

**适用边界与局限**：
- **内存限制**：Scintilla 的大规模场景（约 200K 植物、近 1000K 模块）已接近内存上限（Table 2），无法模拟更大地理范围（如整个流域），这限制了其在区域级野火风险评估中的直接应用。
- **土壤模型简化**：边界燃料层中的腐殖质仅为 2D 生物量分布，未模拟地下有机层的燃烧（地火），因此无法表现泥炭火等深层持续燃烧现象。
- **无火致天气**：框架不包含火旋风、火积云等火—大气强耦合现象，这在高强度树冠火场景中可能低估火行为复杂性。
- **飞火点火抽象**：飞火对植被的点火使用了稳态临界半径判据（Eq. 25），未考虑燃料床的瞬态加热过程，可能在极端干燥条件下高估点火概率。

**后续工作启发**：
1. **多尺度耦合**：将 Scintilla 的精细模块化表示与粗粒度的景观尺度模型（如 FARSITE）耦合，在关键区域使用高分辨率模拟，其他区域使用经验蔓延模型，可缓解内存限制。
2. **数据同化**：Scintilla 的湿度计算管线（环境适应→活力→湿度）为集成遥感植被指数（如 NDVI、Live Fuel Moisture）提供了天然接口，可用于真实场景的初始化。
3. **火致天气扩展**：在现有大气网格上增加涡度输运方程，可模拟火旋风等局部现象，提升高能场景的物理保真度。
4. **不确定性量化**：Scintilla 的多个参数（如 $\varpi_g$、$\sigma_f$、$\delta_{cr}$）缺乏系统敏感性分析，后续可通过参数扫描确定对火线形状和蔓延速率影响最大的控制变量。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/Scintilla_Simulating_Combustible_Vegetation_for_Wildfires.pdf]]