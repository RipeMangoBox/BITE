---
title: A Clebsch Method for Free-surface Vortical Flow Simulation
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/A_Clebsch_Method_for_Free_surface_Vortical_Flow_Simulation.pdf
project_link: "https://shiyingxiong.github.io/proj/Clebsch/Clebsch"
code_link: null
aliases:
- FSCS
- CMFSVFS
tags:
- SIGGRAPH_2022
- topic/other_unclear
core_operator: 波函数校正方案（用于平滑局部相位偏差）和基于快速行进法的波函数外推算法（用于在窄带内保持速度与波函数的一致性）。
primary_logic: 通过优化驱动的波函数校正和基于速度场的外推，确保自由表面附近波函数与速度的一致性，使Clebsch方法能够模拟具有复杂涡旋-界面相互作用的自由表面流动，同时保留丰富的涡旋细节。
claims:
- 与基于速度的求解器相比，自由表面Clebsch求解器能更好地保持气泡环的涡旋结构（Fig. 2）。
- 波函数校正消除了界面合并后的非物理动能尖峰（Fig. 12(c)）。
- 快速行进外推避免了常数外推导致的界面运动过度阻尼（Fig. 14）。
- 与Yang et al. 2021的Clebsch规范流体相比，本方法在沉没涡旋模拟中保留了更多的表面细节（Fig. 15）。
---

# A Clebsch Method for Free-surface Vortical Flow Simulation

> [!tip] 核心洞察
> 通过优化驱动的波函数校正和基于速度场的外推，确保自由表面附近波函数与速度的一致性，使Clebsch方法能够模拟具有复杂涡旋-界面相互作用的自由表面流动，同时保留丰富的涡旋细节。

| 字段 | 内容 |
|------|------|
| 中文题名 | 一种用于自由表面涡流模拟的Clebsch方法 |
| 英文题名 | A Clebsch Method for Free-surface Vortical Flow Simulation |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://shiyingxiong.github.io/proj/Clebsch/Clebsch) · [Project](https://shiyingxiong.github.io/proj/Clebsch/Clebsch") |
| Topic | #topic/other_unclear |
| Method | Free-Surface Clebsch Solver |
| Dataset | Bubble ring evolution, Paddling propulsion with waves, Single hole sink vortex, Multiple parallel surface vortices |

> [!tip] 效果简介
> - Bubble ring evolution 上，涡旋结构保持 保持清晰涡旋细丝，气泡环交互复杂 vs 涡旋细丝快速耗散，交互模糊 (显著改善)。
> - Paddling propulsion with waves 上，尾涡形成与保持 形成明显的马蹄涡和尾涡 vs 涡旋结构模糊 (显著改善)。
> - Single hole sink vortex 上，表面细节丰富度 保留清晰螺旋状表面变形 vs 表面平滑，细节丢失 (明显更多细节)。

## 概要

本文针对自由表面涡流模拟中，Clebsch波函数表示在动态界面附近出现的数值不稳定性问题，提出了一种**自由表面Clebsch求解器**。核心瓶颈在于：当不同拓扑区域的流体合并时，波函数的全局相位差异导致局部速度场产生非物理奇异性，破坏涡旋结构的保持。为此，本文引入了两项关键机制：**波函数校正方案**，通过局部优化消除界面附近的相位不一致；以及基于**快速行进法的波函数外推算法**，在窄带内保持速度与波函数的一致性。实验表明，该方法在气泡环演化、划水推进尾涡、沉没涡表面细节等多个场景下，相比传统基于速度的求解器显著改善了涡旋结构的保持能力，并优于Yang et al. 2021的Clebsch规范流体方法。该方法定位于Eulerian自由表面流体模拟与Clebsch涡旋表示框架的交叉点，为复杂涡旋-界面交互现象的模拟提供了新的数值方案。

## 核心方法与创新机理

### 问题背景与核心瓶颈

自由表面涡流模拟是计算机图形学中的长期挑战。传统基于速度的Eulerian求解器在平流过程中会引入显著的数值耗散，导致涡旋细丝结构快速衰减，无法保持丰富的涡旋细节。Clebsch方法通过波函数表示速度场，理论上能够精确保持涡旋拓扑结构，但在自由表面附近存在根本性的数值不稳定问题。

**核心瓶颈**在于波函数与速度场之间的相位不一致性。Clebsch表示中，速度场通过波函数的空间梯度与内积构造：$\pmb{u} = \hbar \langle \pmb{\nabla} \Psi, \mathrm{i} \Psi \rangle_{\mathbb{R}}$。当自由表面动态演化导致不同拓扑区域的流体合并时，各区域波函数的全局相位可能不同。由于速度场对波函数的全局相位不敏感（$\pmb{\nabla}(e^{\mathrm{i}\theta}\Psi) = e^{\mathrm{i}\theta}\pmb{\nabla}\Psi$），但相位差异会在界面附近产生非物理的速度奇异性，破坏涡旋结构的保持。

### 方法框架与模块顺序

Free-Surface Clebsch Solver在每个时间步内执行四个核心模块，形成完整的模拟管线：

1. **Advection（平流）**：使用二阶半拉格朗日方法同时平流速度和波函数，并混合Clebsch速度与对流速度
2. **Wave-Function Correction（波函数校正）**：局部优化波函数以消除界面附近因拓扑变化引起的速度奇异性
3. **Projection（投影）**：求解泊松方程强制无散条件，同步更新速度和波函数
4. **Wave-Function Extrapolation（波函数外推）**：在level-set窄带内基于外推速度场重建波函数

这四个模块形成闭环：平流提供候选场，校正消除相位不一致，投影确保物理约束，外推维持界面附近的一致性表示。

### 关键公式与物理模型

自由表面Clebsch求解器的数学基础建立在波函数的两个约束条件上：

**归一化条件**（Eq. 1）：
$$\| \Psi \|^2 = \langle \Psi, \Psi \rangle_{\mathbb{R}} = 1$$

**无散约束**（Eq. 2）：
$$\langle \mathrm{i} \Psi, \Delta \Psi \rangle_{\mathbb{R}} = 0$$

速度场从波函数重建（Eq. 3）：
$$\pmb{u} = \hbar \langle \pmb{\nabla} \Psi, \mathrm{i} \Psi \rangle_{\mathbb{R}}$$

波函数的随体导数演化方程（Eq. 5）：
$$\frac{\mathrm{D} \Psi}{\mathrm{D} t} = \frac{-\mathrm{i}}{\hbar} \left( q - \frac{|\pmb{u}|^2}{2} \right) \Psi$$

在平流步中，忽略压力项$q$，波函数按（Eq. 6）对流：
$$\frac{\mathrm{D} \Psi}{\mathrm{D} t} = \frac{\mathrm{i} |\pmb{u}|^2}{2\hbar} \Psi \quad \text{with} \quad \| \Psi \| = 1$$

平流后的Clebsch速度$\pmb{u}^{\Psi}$与对流速度$\pmb{u}^{\star}$通过混合系数$\beta$融合（Eq. 8）：
$$\pmb{u}^{\sharp} = \beta \pmb{u}^{\Psi} + (1 - \beta) \pmb{u}^{\star}$$

投影步求解泊松方程（Eq. 9）：
$$\Delta t \nabla^2 q = \nabla \cdot \pmb{u}^{\sharp}$$

速度和波函数同步更新（Eq. 11）：
$$\begin{cases} u^{\flat} = u^{\sharp} - \Delta t \nabla q, \\ \Psi^{\flat} = \Psi^{\sharp} \exp\left( -\frac{\mathrm{i} q \Delta t}{\hbar} \right) \end{cases}$$

### Changed Slot 1：波函数校正算法

**基线缺陷**：传统Clebsch方法在平流和投影后无校正步骤。当自由表面合并导致不同拓扑区域连接时，各区域波函数的全局相位差异造成界面附近速度场出现非物理奇异性。

**提出方案**：基于优化的波函数校正算法（Algorithm 4），在投影前对波函数进行局部优化。核心思想是最小化波函数与邻近面速度重建波函数的差异。

定义从相邻网格面速度重建的波函数（Eq. 14）：
$$\Phi_{vw} = \Psi_w \exp\left( \frac{\mathrm{i} u_{vw}^{\sharp} \Delta x}{\hbar} \right)$$

优化目标函数（Eq. 16）：
$$\Psi^{\sharp} = \underset{\Psi \in \{ \psi \mid \| \psi \| = 1 \}}{\arg\min} \sum_{vw \in \mathcal{E}} \big\| \Psi_v - \Phi_{vw} \big\|^2$$

**因果机制**：该优化问题通过迭代更新求解（Eq. 17），每次迭代保证能量函数递减（Theorem 5.2）。校正后的波函数消除了相位不一致性，使速度场在界面合并处保持连续。验证实验（Fig. 11）表明，算法能在约20次迭代内将随机初始波函数重建为准确的Taylor-Green速度场，证明了校正算法的收敛性和有效性。

**与下游模块的因果关系**：校正后的波函数$\Psi^{\sharp}$输入投影步，确保投影求解的泊松方程右侧$\nabla \cdot \pmb{u}^{\sharp}$不受相位奇异性污染，从而保证整个求解管线的稳定性。

### Changed Slot 2：波函数外推算法

**基线缺陷**：自由表面模拟中，level-set窄带外的波函数需要外推。常数外推导致窄带内速度为零，界面运动过度阻尼，无法保持自然行为。

**提出方案**：基于快速行进法的波函数外推算法（Algorithm 5）。首先将速度场外推到窄带内，然后利用外推速度场重建波函数。

算法流程：
1. 识别窄带内的待外推网格单元集合$\mathcal{V}_I$
2. 按level-set值$\phi^{(j+1)}$降序排列，存入有序集合$O$
3. 基于已外推的速度场$u_{vw}^{\sharp}$，使用反追踪公式（Eq. 14）重建波函数

**因果机制**：快速行进法确保波函数从界面内侧向外侧逐步构建，每一步利用相邻已知网格的速度信息反推波函数值。这保证了窄带内速度场与波函数的一致性，避免了常数外推造成的速度偏差。

**与上游模块的因果关系**：外推模块依赖投影步输出的速度场$u^{\flat}$作为外推基础，确保外推后的波函数与物理速度场一致。外推结果作为下一时间步平流的初始条件，形成闭环。

### 核心创新机理的深层逻辑

两个changed slots共同解决同一个根本问题：**自由表面附近的波函数-速度一致性**。校正算法处理的是界面合并时的相位跳变（空间上的不连续性），外推算法处理的是窄带区域的波函数定义（空间上的缺失性）。两者在管线中的位置体现了因果顺序：校正在前（消除已有奇异性），外推在后（扩展一致性表示）。

参数$\hbar$和$\beta$在方法中扮演关键角色。$\hbar$控制波函数到速度的映射尺度，数值实验表明Clebsch流的涡旋结构趋向于相似尺度，猜测与$\hbar$有关。$\beta$平衡Clebsch速度与对流速度的混合比例，影响数值稳定性和涡旋保持能力。这两个参数的数学含义尚未完全理解，是论文指出的开放问题之一。

### 方法边界条件

当前方法存在明确的局限性：未考虑多相流（难以定义波函数跨界面的跳跃条件），尚未正确定义粘性项（理论困难），参数$\hbar$和$\beta$缺乏严格的数学基础。这些限制源于Clebsch表示本身的数学结构，而非实现细节，构成了方法的理论边界。

## 实验与关键发现

### 主结果：涡旋结构保持能力的定量与定性验证

本文的核心实验围绕一个关键命题展开：**自由表面Clebsch求解器能否在动态界面条件下保持传统速度求解器无法保留的涡旋结构？** 实验设计以气泡环演化（Fig. 2）作为核心基准，该场景包含气泡环的移动、变形、连接和分裂等复杂拓扑变化。与基于速度的求解器相比，自由表面Clebsch求解器在相同网格分辨率和CFL条件下（Table 1），显著保持了涡旋细丝的清晰度。速度求解器中涡旋细丝快速耗散，气泡环之间的交互模糊；而Clebsch求解器则完整保留了涡旋结构的几何特征，使得气泡环的再连接和分裂过程清晰可辨。这一差异的因果机制在于：Clebsch表示将涡旋信息编码在波函数的相位中，而波函数随体导数的演化方程（Eq. 5）天然保持了涡旋的拉格朗日不变性。

![[assets/figures/papers/paper_list_l4_https_shiyingxiong_github_io_proj_Clebsch_Clebsch/figures/015_Table_1.jpg]]
*Table 1: Details of the Simulation Examples. (a) reconnecting bubble rings, (b) vortex in a sink with one hole, (c) vortex in a sink with two holes, (d) horseshoe vortex, (e) paddling, (f) a bunny in waves, (g) multiple parallel surface vortex, (h) a boat in waves, (i) a lighthouse in waves, (j) reconnecting bubble rings, (j) leapfrogging bubble rings, and (k) fishtail wiggling. (d) was performed on a server with a 36-core CPU and an Nvidia RTX 2080 Ti GPU. (b) and (g) were performed on a server with a 64-core CPU and a Quadro RTX 8000 GPU. (c) was performed on a server with a 40-core CPU and an Nvidia Tesla V100 GPU. (a), (e), (j), and (k) were performed on personal computer with a 32-core CPU and...*

![[assets/figures/papers/paper_list_l4_https_shiyingxiong_github_io_proj_Clebsch_Clebsch/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of bubble ring evolution simulated with the free-surface Clebsch solver (top) and a velocity-based solver (bottom), which shows two bubble rings moving, deforming, connecting, and splitting, from left to right are frames 1, 120, 320, 400 of the two simulations*

在更复杂的自由表面场景中，该方法同样展现出优势。**划水推进模拟**（Fig. 5）在稀疏网格上对比了两种求解器的表现：Clebsch求解器形成了清晰的马蹄涡和尾涡结构，而速度求解器仅产生模糊的涡旋痕迹。这一结果验证了波函数表示对涡旋生成和输运过程的保真度。**单孔沉没涡模拟**（Fig. 15）进一步与Yang et al.（2021）的Clebsch规范流体方法进行了直接对比：自由表面Clebsch求解器保留了清晰的螺旋状表面变形，而Clebsch规范方法产生的表面更为平滑，细节丢失明显。该差异源于本文方法在界面附近对波函数与速度场一致性的主动维护。

![[assets/figures/papers/paper_list_l4_https_shiyingxiong_github_io_proj_Clebsch_Clebsch/figures/005_Figure_5.jpg]]
*Figure 5: Comparison of results simulated with the free-surface Clebsch solver (top) and that simulated with a velocity-based solver (bottom). This figure shows a paddling simulated on a sparse grid where the right end of the simulation domain attaches a wave generator outputs moderate waves. The figures from left to right are frames 50, 100, 150, and 200, respectively*

方法还展示了处理多涡交互的能力。**平行表面涡旋交互**（Fig. 7）成功模拟了双涡和三涡在自由表面的合并与演化过程，这是传统速度求解器难以处理的场景，因为多个涡旋的叠加会导致数值耗散加剧。

![[assets/figures/papers/paper_list_l4_https_shiyingxiong_github_io_proj_Clebsch_Clebsch/figures/007_Figure_7.jpg]]
*Figure 7: Interactions of two (top) and three (bottom) parallel vortices on freesurface. The top figures from left to right are frame 200, 300 and 400 of the dual-vortex simulation. The bottom figures from left to right are frame 500, 600, and 700 of the tri-vortex simulation, respectively*

### 消融实验：波函数校正与外推的因果作用

消融实验系统性地验证了两个核心模块的因果贡献。

**波函数校正的消融**（Fig. 12, Fig. 13）以二维溃坝算例为测试平台。当去除波函数校正步骤时，界面合并后动能出现非物理尖峰（Fig. 12(c)中虚线圈出区域）。因果分析揭示：当两个拓扑分离的流体区域合并时，各自波函数的全局相位差异导致界面附近波函数方向相反（Fig. 13(b)），进而在速度场中产生局部奇异性。波函数校正算法（Algorithm 4）通过最小化相邻网格面波函数重建差异（Eq. 16），在约20次迭代内即可消除相位不一致性。Taylor-Green涡的收敛性测试（Fig. 11）定量验证了该算法的有效性：从随机初始波函数出发，算法能快速收敛到准确的速度场重建。

**波函数外推的消融**（Fig. 14）对比了三种策略：无外推、常数外推和基于快速行进的外推。无外推导致窄带内波函数未定义，界面运动异常；常数外推使窄带内速度趋于零，造成界面运动过度阻尼（如二维液滴下落算例中，液滴无法自然变形）；而快速行进外推（Algorithm 5）利用外推速度场反追踪重建波函数（Eq. 14），保持了窄带内速度与波函数的一致性，使得界面运动行为自然。这一结果揭示了自由表面Clebsch方法的一个关键边界条件：**波函数在界面附近必须与速度场保持相位一致性，否则外推误差会通过投影步骤传播到整个流场**。

### 实验细节与计算成本

Table 1汇总了各算例的分辨率、CFL数和每帧平均计算时间。分辨率范围从二维算例到三维高分辨率的 $256 \times 512 \times 256$ 网格（气泡环蛙跳算例，Fig. 9）。计算平台涵盖从6核CPU配RTX 2070的个人计算机到64核CPU配Quadro RTX 8000的工作站，表明方法在不同硬件配置下均具可行性。每帧平均时间取决于算例复杂度和CFL数，具体数值需查阅原文表格。

### 失败模式与适用边界

尽管方法在涡旋保持方面表现突出，但存在明确的适用边界：

1. **多相流限制**：当前算法未考虑多相流，因为难以定义波函数跨界面的跳跃条件。这意味着方法仅适用于单一液体与气体（或真空）的两相自由表面流，无法处理液-液界面或多相混合场景。

2. **粘性缺失**：由于理论困难，尚未为正确定义Clebsch方法的粘性项。因此方法本质上是无粘的，适用于高雷诺数流动，但在需要粘性耗散精确建模的场景（如小尺度涡旋的最终耗散阶段）可能存在偏差。

3. **参数ℏ的物理含义不明**：数值实验表明Clebsch流的涡旋结构趋向于相似尺度，猜测与ℏ有关，但缺乏严格的理论解释。这限制了参数选择的系统性指导。

4. **波函数校正的局部性假设**：校正算法假设相位不一致性仅发生在界面附近的局部区域。当大范围流体合并且相位差异显著时，算法的收敛性和有效性需要进一步验证。

### 证据强度评估

- **高置信度证据**（confidence ≥ 0.9）：气泡环涡旋保持（Fig. 2）、波函数校正消除动能尖峰（Fig. 12(c)）、快速行进外推避免过度阻尼（Fig. 14）、与Yang et al. 2021的对比（Fig. 15）均有清晰的视觉对比和定量指标支持。
- **中等置信度证据**（confidence 0.8–0.85）：多涡交互能力（Fig. 7）和波函数校正收敛性（Fig. 11）虽有展示，但缺乏与更多基准方法的系统对比。
- **需手动验证的点**：参数ℏ对涡旋尺度的控制机制、方法在极端拓扑变化（如大规模飞溅）下的鲁棒性，原文未提供充分实验证据。

![[assets/figures/papers/paper_list_l4_https_shiyingxiong_github_io_proj_Clebsch_Clebsch/figures/012_Figure_12.jpg]]
*Figure 12: Comparison of the wave-function distribution of a two-dimensional dam breaking (a), (b) without, and (d), (e) with wave-function correction. (a), (d) and (b), (e) are the two adjacent frames before and after the interface merge, respectively. (see the supplemented video for more details). We convert the first component of the two-component wave function to a vector in two-dimensional Euclidean space and plot it as an arrow line. Red points in (d) and (e) highlight the grid cells involved in the correction algorithm. (c) and (f ) are the evolution of kinetic energy with and without wave-function correction, respectively. The dotted circle in (c) denotes a non-physical increment of kinetic en...*

![[assets/figures/papers/paper_list_l4_https_shiyingxiong_github_io_proj_Clebsch_Clebsch/figures/008_Figure_8.jpg]]
*Figure 8: The distribution of the velocity field of two topologically disconnected fluids close to each other. The wave functions in the two domains enclosed by the red lines have (a) the same global phase, (b) different global phases without wave function correction, and (d) different global phases with wave function correction. The arrow line in the wave function schematic denotes the first component of the two-component wave function. In (c), we show the relationship between the relative error of wave function transformed velocity and global phase difference*

## 定位与知识库关联

本文提出了一种面向自由表面涡流模拟的Clebsch方法，其核心定位在于**将Clebsch表示从纯欧拉域扩展到含动态界面的自由表面流**，解决了此前Clebsch方法在界面附近因波函数-速度场不一致导致的数值不稳定性问题。

### 相对已有方法的核心差异

传统基于速度的Eulerian自由表面求解器直接以速度场为基本变量，在平流和投影过程中涡旋结构会因数值耗散而快速衰减。本文方法将基本变量替换为波函数 $\Psi$，通过映射 $\pmb{u} = \hbar \langle \pmb{\nabla} \Psi, \mathrm{i} \Psi \rangle_{\mathbb{R}}$ 重建速度场，利用Clebsch表示的拉格朗日不变量性质保持涡旋拓扑。与**Clebsch gauge fluid**（Yang et al., ACM Trans. Graph. 2021）相比，后者面向表面张力主导的自由表面流，采用Clebsch规范势而非波函数表示，在沉没涡模拟中表面细节丰富度明显不足（Fig. 15），而本文方法能保留清晰的螺旋状表面变形。

**改变的关键slot**有两个：

1. **波函数后处理slot**：传统Clebsch方法在平流和投影后无校正步骤。当不同拓扑区域的流体合并时，波函数的全局相位差异导致局部速度场出现非物理奇异性（Fig. 8(b)）。本文引入基于优化的波函数校正算法（Algorithm 4），以邻近面速度重建的波函数 $\Phi_{vw}$ 为目标，最小化 $\sum_{vw \in \mathcal{E}} \| \Psi_v - \Phi_{vw} \|^2$，在保持归一化约束下迭代消除相位不一致。该slot直接决定了界面合并后动能演化的物理合理性（Fig. 12(c)）。

2. **波函数外推slot**：传统方法采用常数外推，导致level-set窄带内速度场被强制置零，界面运动过度阻尼。本文改用基于快速行进法的波函数外推（Algorithm 5），利用已外推的速度场通过反追踪公式 $\Phi_{vw} = \Psi_w \exp(\mathrm{i} u_{vw}^{\sharp} \Delta x / \hbar)$ 重建波函数，确保窄带内速度与波函数的一致性（Fig. 14）。

### 知识库挂载点

本工作可挂载到以下知识节点：

- **Clebsch表示理论**：将速度场编码为波函数的几何相位梯度，继承了量子力学中Madelung变换的思想。该表示天然保持涡旋线的拉格朗日不变性，是区别于传统欧拉方法的核心理论支柱。
- **自由表面流体求解器**：以level-set方法为界面追踪框架，结合ghost fluid方法处理界面两侧的压力跳跃条件，属于Eulerian自由表面模拟的标准技术栈。本文在该框架中嵌入了波函数表示层。
- **波函数校正优化**：校正算法本质上是一个定义在网格面上的局部优化问题，与图上的相位同步问题有数学关联，其收敛性由定理5.2保证。
- **快速行进法外推**：将速度场外推的标准技术适配到波函数外推，通过有序集合 $O$ 按level-set值降序处理，保证外推从已知区域向未知区域单向传播。

### 适用边界

- **适用场景**：涡旋-自由表面强耦合的流动，如气泡环重连、马蹄涡演化、划水尾涡、沉没涡等需要保持涡旋拓扑细节的场景。
- **不适用场景**：（1）多相流，因难以定义波函数跨界面的跳跃条件；（2）含显著粘性效应的流动，因尚未正确定义Clebsch方法的粘性项；（3）参数 $\hbar$ 和 $\beta$ 的物理含义尚未完全理解，涡旋尺度与 $\hbar$ 的关系仅为经验性猜测，缺乏理论指导下的最优选择。

### 后续研究启发

1. **可压缩流与磁流体动力学扩展**：Clebsch表示的拉格朗日性质在可压缩流和MHD中具有理论潜力，但需解决波函数在激波等不连续处的行为定义问题。
2. **双向流固耦合**：将Clebsch表示扩展到含刚体动力学的场景，需要处理固体边界对波函数相位的约束条件。
3. **粒子-Clebsch混合方法**：利用Clebsch映射的拉格朗日性质，与基于粒子的流体模拟方法（如SPH、FLIP）结合，有望在保持涡旋细节的同时处理大变形自由表面。
4. **参数 $\hbar$ 的理论研究**：数值实验表明Clebsch流的涡旋结构趋向于相似尺度，该尺度与 $\hbar$ 相关。建立 $\hbar$ 与涡旋尺度的定量关系可为参数选择提供理论依据。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/A_Clebsch_Method_for_Free_surface_Vortical_Flow_Simulation.pdf]]