---
title: Primal-dual Non-smooth Friction for Rigid Body Animation
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/Primal_dual_Non_smooth_Friction_for_Rigid_Body_Animation.pdf
project_link: null
code_link: null
aliases:
- PD
- PDNSFRBA
tags:
- SIGGRAPH_2024
- topic/graphics_animation_interaction
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: Primal-dual
primary_logic: Primal-dual
claims:
- Primal-dual
---

# Primal-dual Non-smooth Friction for Rigid Body Animation

> [!tip] 核心洞察
> Primal-dual

| 字段 | 内容 |
|------|------|
| 中文题名 | Primal-dual Non-smooth Friction for Rigid Body Animation |
| 英文题名 | Primal-dual Non-smooth Friction for Rigid Body Animation |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://visualcomputing.ist.ac.at/publications/2024/PDNSF/) |
| Topic | #topic/graphics_animation_interaction #topic/vision_multimodal_applications/image_and_video_generation |
| Method |  |
| Dataset |  |

> [!tip] 效果简介
> 结果与证据沿用下文“实验与关键发现”中的现有记录；本轮不新增或外推论文事实。

## 概要

本文针对刚体动画中非光滑库仑摩擦约束求解困难的问题，提出一种基于原始-对偶内点法的摩擦求解框架。核心思路是将高度约束的非光滑接触问题通过**对数障碍函数**转化为无约束光滑问题，并构建原始-对偶形式，使其可通过牛顿迭代高效求解。该方法将法向接触力与切向摩擦力分离为两个独立障碍项，在保持计算效率的同时实现了模块化结构。

实验表明，该方法在多种复杂场景（如链甲网、螺纹螺栓、砖块城堡倒塌）中均能稳定收敛，无穿透和视觉伪影，且收敛速度在理论和实践上均优于传统高斯-赛德尔方法。与基于非光滑牛顿法的Siconos求解器相比，本方法在保持相当视觉质量的前提下，每时间步计算时间从20–30秒降至约2秒，加速一个数量级。此外，方法计算复杂度与刚体自由度数相关，而非接触数量，因此在密集接触场景（如大量颗粒堆积）中具有显著优势。

## 核心方法与创新机理

### 问题背景与核心瓶颈

刚体仿真的接触力学求解长期面临一个根本性矛盾：Coulomb摩擦定律是非光滑（non-smooth）且高度非线性的，传统方法要么将其光滑化近似而丧失物理精度，要么采用LCP/NCP互补形式但求解器收敛困难、对大规模场景扩展性差。现有增量势能（Incremental Potential, IP）类方法在弹性体接触中取得突破，但其摩擦处理仍依赖光滑近似；而基于非光滑动力学的刚体仿真（如Bullet、MuJoCo）则在复杂约束（非凸几何、大质量比、互锁结构）下频繁失稳。

本文的核心瓶颈突破在于：**将刚体摩擦接触这一高度约束的非光滑问题，通过对数障碍函数（logarithmic barrier）转化为无约束光滑问题，并建立原始-对偶（primal-dual）内点框架，使Newton迭代能够高效、精确地求解每一时间步的接触力与速度。**

### 方法框架总览

整个求解器由以下模块按因果链串联构成：

1. **离散动力学建模** → 2. **接触约束的min-max表述** → 3. **对数障碍松弛与原始-对偶转化** → 4. **Newton-KKT线性化与求解** → 5. **实现层面的稳定化与加速策略**

每个模块的输出直接成为下一模块的输入，形成端到端的单步求解路径。

### 核心机制一：接触问题的min-max表述

系统动力学从隐式Euler离散出发，运动方程为：

$$\mathbf{M} \frac{d\mathbf{v}}{dt} = \mathbf{f}_{\mathrm{ext}} - \nabla U(\mathbf{q}) + \mathbf{H}^{\top} \mathbf{r}$$

其中 $\mathbf{H}$ 为接触Jacobian矩阵，$\mathbf{r}$ 为接触力向量（包含法向分量 $\mathbf{r}_N$ 和切向分量 $\mathbf{r}_T$）。Coulomb摩擦的互补条件为：

$$\begin{cases} \mathbf{u}_{N,i}=0 \text{ 且 } \mathbf{r}_{N,i}\geq 0 & \text{(非穿透)} \\ \text{或 } \mathbf{u}_{N,i}>0 \text{ 且 } \mathbf{r}_{N,i}=0 & \text{(脱离)} \end{cases}$$

$$\|\mathbf{r}_{T,i}\| \leq \mu \mathbf{r}_{N,i}, \quad \mathbf{u}_{T,i} \text{ 与 } \mathbf{r}_{T,i} \text{ 满足最大耗散原理}$$

这一约束系统的关键洞察是：**可以将动力学表述为关于速度 $\mathbf{v}$ 的极小化和关于接触力 $\mathbf{r}$ 的极大化的鞍点问题**：

$$\min_{\mathbf{v}} \max_{\mathbf{r}} \frac{1}{2}(\mathbf{v} - \tilde{\mathbf{v}})^\top \mathbf{M} (\mathbf{v} - \tilde{\mathbf{v}}) + \tilde{U}(\mathbf{v}) - \mathbf{v}^\top \mathbf{H}^\top \mathbf{r} \quad \text{s.t.} \quad -\mathbf{r}_N \leq 0, \; c(\mathbf{r}_T, \mathbf{s}) \leq 0$$

其中 $c(\mathbf{r}_T, \mathbf{s}) = \|\mathbf{r}_T\| - \mu \mathbf{s}$ 为摩擦锥约束，$\mathbf{s}$ 是滞后迭代（lagged iteration）中对法向力 $\mathbf{r}_N$ 的近似值。这一滞后策略借鉴了Macklin et al. (2020)的框架，但将其推广至非光滑摩擦场景，是连接前一步已知量与当前步未知量的关键工程近似。

### 核心机制二：对数障碍松弛与原始-对偶转化

上述min-max问题的核心困难在于不等式约束 $-\mathbf{r}_N \leq 0$ 和 $c(\mathbf{r}_T, \mathbf{s}) \leq 0$。本文的核心创新是**引入对数障碍函数将这些硬约束转化为目标函数的惩罚项**，得到无约束问题：

$$\min_{\mathbf{v}} \max_{\mathbf{r}} \frac{1}{2}(\mathbf{v} - \tilde{\mathbf{v}})^\top \mathbf{M} (\mathbf{v} - \tilde{\mathbf{v}}) + \tilde{U}(\mathbf{v}) - \mathbf{v}^\top \mathbf{H}^\top \mathbf{r} + \kappa \sum_i \ln(\mathbf{r}_{N,i}) + \kappa \sum_i \ln(\mu \mathbf{s}_i - \|\mathbf{r}_{T,i}\|)$$

这里 $\kappa > 0$ 为障碍参数。当 $\kappa \to 0$ 时，障碍问题的解收敛到原约束问题的精确解。**法向和切向约束被分离为两个独立的对数障碍项**，这一分离使得求解器具有高度模块化——接触模型（法向部分）理论上可替换，而摩擦求解器保持相同结构。

进一步，引入对偶变量 $\lambda_i = -\kappa / b_i(\mathbf{r})$，其中 $b_i(\mathbf{r})$ 为对应的障碍函数（法向为 $\mathbf{r}_{N,i}$，切向为 $\mu\mathbf{s}_i - \|\mathbf{r}_{T,i}\|$），将问题转化为原始-对偶形式。一阶最优性条件（KKT系统）为：

$$\mathbf{M}(\mathbf{v} - \tilde{\mathbf{v}}) + \nabla \tilde{U}(\mathbf{v}) - \mathbf{H}^\top \mathbf{r} = 0$$

$$-\mathbf{H}\mathbf{v} + \kappa \sum_i \frac{1}{\mathbf{b}_i(\mathbf{r})} \nabla \mathbf{b}_i(\mathbf{r}) = 0$$

$$\lambda_i \mathbf{b}_i(\mathbf{r}) + \kappa = 0$$

这一组方程将原始变量 $(\mathbf{v}, \mathbf{r})$ 与对偶变量 $\lambda$ 耦合，为Newton迭代提供了完整的可微系统。

### 核心机制三：Newton-KKT求解与障碍参数更新

对上述KKT系统进行线性化，得到关于增量 $(\Delta\mathbf{v}, \Delta\mathbf{r}, \Delta\lambda)$ 的对称不定线性系统。本文采用**原始-对偶内点法的标准路径跟踪策略**：每次Newton迭代求解线性化系统后，沿搜索方向进行线搜索（linesearch）以保证约束满足，然后更新障碍参数 $\kappa$。

障碍参数的更新规则是方法收敛性的关键控制旋钮：**将 $\kappa$ 缩放为代理对偶间隙（surrogate duality gap）的一个比例**：

$$\kappa \leftarrow -k \frac{\lambda^\top \bar{\mathbf{b}}}{2m}, \quad k \in (0,1)$$

其中 $m$ 为接触约束总数，实践中取 $k = 0.1$。这一自适应策略使障碍参数随优化进程自动衰减，在保证数值稳定的同时驱动解向精确约束满足收敛。

### 实现层面的关键工程策略（Changed Slots）

上述理论框架在实现中引入了三个关键的“changed slots”，即相对于标准内点法的定制化改进：

**Slot 1：Baumgarte稳定化（法向约束修正）**

将法向部分的KKT条件替换为：

$$- (\mathbf{H}\mathbf{v})_N - \gamma \mathbf{r}_N - \sum_i \lambda_i \nabla_{\mathbf{r}_N} \mathbf{b}_i(\mathbf{r}) = \frac{e}{\delta t}\varphi$$

其中 $\varphi$ 为穿透深度，$\gamma$ 为柔度参数，$e$ 为误差缩减速率。这一修正使求解器能够处理初始穿透并抑制数值漂移，在Figure 1的大规模颗粒堆积场景中至关重要，但在多数其他示例中并非必需——说明方法本身的数值稳定性已相当鲁棒。

**Slot 2：Coulomb锥正则化**

为避免摩擦锥顶点处梯度不连续导致的收敛困难，将切向力扩展一维：

$$\mathbf{r}_{T,i}' = [\mathbf{r}_{T,i}, \epsilon_p]^\intercal$$

$$c_i'(\mathbf{r}_{T,i}) = \|\mathbf{r}_{T,i}'\| - \mu \mathbf{r}_{N,i} - \epsilon_p - \epsilon_s$$

其中 $\epsilon_p$ 和 $\epsilon_s$ 为小正则化参数。这一处理将锥顶点“圆化”，使Newton迭代在摩擦锥边界附近具有光滑梯度，是保证求解器在滑动-黏着转换区收敛的关键。

**Slot 3：摩擦权重缩放与搜索方向投影**

在接近滑动状态时，切向方程的刚度矩阵条件数恶化。引入自适应摩擦权重：

$$w_i = \left( \hat{\mathbf{u}}_{T,i}^\top \mathbf{H} \mathbf{M}^{-1} \mathbf{H}^\top \hat{\mathbf{u}}_{T,i} \right) \frac{\mu \mathbf{r}_{N,i}}{\|\mathbf{u}_{T,i}\|}$$

对式(5c)进行重缩放。此外，在每次Newton步后进行**过滤搜索方向投影**：

$$\Delta \bar{\mathbf{r}}' = \underset{\mathbf{d}_{\bar{\mathbf{r}}}}{\mathrm{argmin}} \left\| \mathbf{d}_{\bar{\mathbf{r}}} - \Delta \bar{\mathbf{r}} \right\|^2 \quad \mathrm{s.t.} \ \mathbf{b}(\bar{\mathbf{r}}^n + \mathbf{d}_{\bar{\mathbf{r}}}) > 0$$

确保更新后的接触力严格满足对数障碍的定义域（$\mathbf{r}_N > 0$，$\|\mathbf{r}_T\| < \mu\mathbf{s}$），之后再进行回溯线搜索。这一双层保障机制是求解器在实际大规模场景中不崩溃的工程基石。

### 推理路径总结

单时间步的完整推理路径为：

1. **滞后更新**：用上一迭代步的法向力 $\mathbf{s}$ 近似当前摩擦锥约束中的 $\mathbf{r}_N$
2. **构建KKT系统**：基于当前 $(\mathbf{v}, \mathbf{r}, \lambda)$ 和障碍参数 $\kappa$ 组装线性化矩阵
3. **求解Newton方向**：求解对称不定系统得 $(\Delta\mathbf{v}, \Delta\mathbf{r}, \Delta\lambda)$
4. **方向投影**：将 $\Delta\mathbf{r}$ 投影到约束可行域内部
5. **线搜索**：沿投影方向回溯，保证障碍函数正值且目标函数充分下降
6. **障碍参数更新**：根据代理对偶间隙缩放 $\kappa$
7. **收敛检查**：当KKT残差低于阈值（通常 $10^{-4}$）或达到最大迭代数（通常50）时终止

整个流程将非光滑摩擦这一传统上需要组合搜索或启发式光滑化的问题，完全纳入了光滑优化的统一框架，且每个模块的因果关系清晰：对数障碍提供可微性 → 原始-对偶转化提供对称结构 → Newton迭代提供二阶收敛速度 → 工程slot保证鲁棒性。

![[assets/figures/papers/paper_list_l31_https_visualcomputing_ist_ac_at_publications_2024_PDNSF/figures/006_Figure_3.jpg]]
*Figure 3: A high-speed armadillo demolishes a castle built with 5185 bricks. Pig model by user printable_models on Free3D.com*

![[assets/figures/papers/paper_list_l31_https_visualcomputing_ist_ac_at_publications_2024_PDNSF/figures/008_Figure_5.jpg]]
*Figure 5: A heavy ball is dropped on a 16 × 16 chain mail net. Examples such as these with both non-convex, interlocking bodies as well as large mass ratios cause problems for Bullet, even at an equal-time ( 0.15??) simulation. Our method robustly handles this case*

## 实验与关键发现

本工作提出的原始-对偶内点法摩擦求解器在多个刚体仿真场景中进行了评估，核心实验围绕求解器稳定性、收敛行为、参数敏感性以及与现有方法的对比展开。

### 主结果：大规模颗粒堆积与摩擦效应验证

论文的核心验证场景是 **Figure 1** 所示的 9122 个多面体颗粒落入浅盘并形成金字塔形堆积的仿真。该场景同时测试了求解器在大规模接触下的稳定性以及摩擦系数对堆积形态的物理合理性。实验展示了不同摩擦系数（μ）下颗粒堆的侧视图，摩擦系数越大，堆积的休止角越大，颗粒堆越陡峭，这与物理直觉一致。该场景是唯一需要启用 **Baumgarte 稳定化**（式 13）的案例，说明在大多数场景下，内点法本身的正则化已经足够维持非穿透约束，只有在极端接触压力下才需要额外的约束稳定化。

### 求解器收敛行为与参数配置

**Table 1** 汇总了各仿真场景的参数配置和每时间步的平均统计量，关键参数如下：

- **最大 Newton 迭代次数**：几乎所有示例中设为 50 次。
- **收敛阈值**：设为 $10^{-4}$。
- **对数障碍参数 κ 的更新策略**：每次 Newton 步后将 κ 缩放为代理对偶间隙（surrogate duality gap）的一个分数，即 $\kappa \leftarrow -k (\lambda^\top \bar{b}) / (2m)$，其中 $k = 0.1$。

这一自适应 κ 更新策略是求解器收敛的核心机制：随着优化进行，对偶间隙缩小，κ 自动减小，使得对数障碍的松弛越来越“硬”，最终逼近精确的非光滑摩擦解。论文指出，这种策略避免了手动调参的需要，且在实践中表现出稳健的收敛性。

### 关键消融：摩擦权重缩放

在 **Section 4.2** 中，作者分析了求解器在接近滑动态时的收敛减速问题，并提出了**摩擦权重缩放**（式 15）作为解决方案：

$$
w_i = \left( \hat{\mathbf{u}}_{T,i}^{\top} \mathbf{H} \mathbf{M}^{-1} \mathbf{H}^{\top} \hat{\mathbf{u}}_{T,i} \right) \frac{\mu \mathbf{r}_{N,i}}{\|\mathbf{u}_{T,i}\|}
$$

该缩放因子对切向摩擦方程进行重新加权，物理意义在于：当接触点接近滑动态时（切向速度较大而法向力相对较小），原始的 Coulomb 锥约束变得病态，Newton 步的搜索方向质量下降。通过引入与法向力和切向速度比值相关的缩放，求解器在滑动态附近的收敛速度得到显著改善。这是求解器实用性的关键设计决策，没有该缩放，求解器在摩擦接触切换频繁的场景中会出现明显的收敛停滞。

### Coulomb 锥正则化

为处理 Coulomb 锥尖端的数值奇异性，论文引入了锥正则化（式 14a, 14b）：将切向力向量增广为 $\mathbf{r}_{T,i}' = [\mathbf{r}_{T,i}, \epsilon_p]^\intercal$，并将约束修改为 $\|\mathbf{r}_{T,i}'\| - \mu \mathbf{r}_{N,i} - \epsilon_p - \epsilon_s \leq 0$。参数 $\epsilon_p$ 和 $\epsilon_s$ 分别控制锥尖的圆角半径和锥面的偏移量。这一正则化使得对数障碍函数在锥尖处可微，从而保证了 Newton 法的适用性。实验表明，适中的正则化参数对仿真结果的影响在视觉上不可察觉，但显著提升了求解器的数值稳定性。

### 与现有方法的定位差异

论文明确将自身置于 **Macklin et al. [2020]** 的滞后迭代框架中，但将其从光滑摩擦推广到非光滑 Coulomb 摩擦。核心差异在于：

- Macklin 等人的方法使用光滑化的摩擦模型，避免了锥约束的不可微性，但牺牲了摩擦的严格非光滑物理特性。
- 本工作通过原始-对偶内点法直接处理非光滑 Coulomb 锥约束，理论上保证了在 κ → 0 时收敛到精确解。

这一差异使得本方法在摩擦行为敏感的仿真场景（如颗粒材料的休止角、刚体堆叠的摩擦稳定性）中具有物理精度优势，但代价是每步需要求解 Newton 系统，计算成本高于光滑化方法。

### 适用边界与失败模式

**需要手动验证的观察**：论文未提供与显式摩擦模型或 LCP 类方法的定量对比实验，也未报告求解器在极端参数（如极高摩擦系数、极低时间步长）下的失败案例。以下边界条件可从方法设计中推断：

1. **Baumgarte 稳定化的必要性**：仅在 Figure 1 的大规模颗粒堆积中启用，暗示在接触压力极大的场景中，内点法的纯对数障碍可能不足以在有限迭代次数内满足非穿透约束，需要额外的稳定化项。这构成了一个实用边界：当接触密度和压力超过某个阈值时，求解器的约束满足精度下降。

2. **Newton 迭代次数限制**：最大迭代次数设为 50，收敛阈值 $10^{-4}$。在实际仿真中，如果某步未能在 50 次内收敛，求解器将以当前近似解继续，这可能导致约束违反累积。论文未讨论此类情况的处理策略。

3. **滞后迭代的近似误差**：方法继承了 Macklin et al. [2020] 的滞后迭代近似（用 s 替换 c 中的 r_N），这意味着法向力在摩擦锥约束中是滞后一步的。这一近似在接触状态快速变化时可能引入误差，但论文未量化该误差。

### 证据强度评估

- **视觉验证充分**：Figure 1 的颗粒堆积展示了方法在大规模场景中的可行性和物理合理性。
- **定量消融缺失**：论文未提供摩擦权重缩放、锥正则化等关键设计的消融实验数据（如收敛迭代次数对比、约束违反量对比），这使得各设计组件的独立贡献难以量化。
- **对比基线缺失**：未与现有非光滑摩擦求解器（如 Anitescu-Potra 的 LCP 方法、增量势能方法等）进行定量对比，方法的相对优势主要基于理论论证而非实验证据。

**总结**：本工作的实验验证侧重于展示方法在大规模非光滑摩擦仿真中的可行性和视觉质量，但定量消融和对比实验的缺失使得部分结论需要谨慎对待。方法的实用价值主要体现在其模块化设计（法向与摩擦力的对数障碍分离）和自适应 κ 更新策略带来的免调参特性，而非在特定指标上超越现有方法。

![[assets/figures/papers/paper_list_l31_https_visualcomputing_ist_ac_at_publications_2024_PDNSF/figures/003_Table_1.jpg]]
*Table 1: Table of simulation parameters and average statistics per timestep. The timings*

## 定位与知识库关联

本文的核心贡献在于将**非光滑摩擦接触问题**从传统的互补性约束/迭代投影框架，整体迁移至**原始-对偶内点法**的求解范式。相对于已有方法，改变的 slot 是**约束处理与求解器的数学结构**：不再使用 LCP（线性互补问题）或 NCP（非线性互补问题）的直接离散化，也不依赖序贯二次规划或高斯-赛德尔迭代投影，而是将对数障碍函数引入原始-对偶框架，将带不等式约束的 min-max 鞍点问题松弛为无约束光滑问题，并通过 Newton 迭代统一求解速度与接触力。

具体而言，相对以下基线工作的本质差异在于：

1. **相对于基于 LCP/NCP 的传统刚体模拟器**（如 Bullet 物理引擎中的序贯脉冲法、以及 Anitescu & Potra 1997 等速度-冲量 LCP 形式）：传统方法将 Coulomb 摩擦锥线性化为多面体锥，从而将问题转化为 LCP。本文彻底放弃了锥的线性化近似，直接处理非线性 Coulomb 锥约束，通过 log-barrier 保持约束的精确非线性几何。这改变了“约束建模”这一 slot——从多面体近似变为精确圆锥约束。

2. **相对于 Macklin et al. 2020 的滞后迭代方案**：本文明确继承了其滞后迭代（lagged iteration）的近似策略，即用上一迭代步的法向力近似当前 Coulomb 锥中的法向分量，将耦合问题解耦。但关键差异在于：Macklin 等的方法仍基于投影动力学框架处理摩擦，而本文将该滞后近似嵌入原始-对偶内点法，改变了“求解器核心算法”这一 slot。作者明确指出：“We use the same lagged iteration scheme as their method but applied to non-smooth friction”——继承的是迭代策略，创新的是数学求解框架。

3. **相对于其他基于障碍函数的接触方法**：已有工作（如 IPC 的增量势接触）使用障碍函数处理法向非穿透约束，但摩擦部分通常仍依赖滞后摩擦或近似模型。本文将 log-barrier 同时应用于**法向非穿透约束和切向 Coulomb 锥约束**，并将两者分离为两个独立的障碍项。这一分离使得法向接触模型与摩擦模型可以独立替换，提高了模块化程度。改变的 slot 是“约束障碍化的范围与结构”——从仅法向障碍扩展为法向-切向联合障碍，且保持模块化解耦。

4. **相对于基于 ADMM 或算子分裂的接触求解器**：这类方法将接触问题分解为多个子问题交替求解。本文的原始-对偶内点法则在单个 Newton 迭代中联合求解速度与接触力，避免了分裂带来的收敛速度慢或调参困难。改变的 slot 是“求解器的分解策略”——从不精确的分裂迭代变为整体的二阶 Newton 求解。

**知识库挂载点**：本文应挂载在物理仿真知识库的“接触与摩擦求解”节点下，具体路径为：**刚体动力学 → 接触力学 → 非光滑摩擦模型 → 原始-对偶内点法**。其上游依赖包括：凸优化中的内点法理论（log-barrier 方法、原始-对偶路径跟踪）、Coulomb 摩擦定律的非光滑分析形式、以及刚体动力学的速度-冲量时间步进格式。其下游可连接至：柔性体摩擦接触的内点法扩展、基于 GPU 的并行内点法实现、以及与其他非光滑现象（如粘滑转换、滚动摩擦）的耦合。

**适用边界**：
- **优势场景**：刚体场景中接触数量大、摩擦效应显著的情况（如颗粒堆积、链甲网、砖块坍塌），尤其是需要精确 Coulomb 锥几何而非线性近似时。由于线性求解基于刚体自由度而非接触点数量，在物体共享大量接触的场景（如螺纹螺栓）中具有效率优势。
- **边界条件**：(1) 滞后迭代近似假设法向力在迭代间变化缓慢，在法向力剧烈跳变的场景（如高速碰撞）中可能引入误差；(2) log-barrier 方法本质上是“近似精确”——随着障碍参数 κ → 0 才收敛到真实解，实际中采用固定比例的 κ 更新策略，得到的是近似解；(3) 需要 Baumgarte 稳定化处理法向穿透，在长时间堆积场景（如图 1 的颗粒堆）中该稳定化是必需的，表明纯粹的 log-barrier 在法向约束上存在漂移；(4) Newton 迭代的最大步数设为 50，退出阈值 10⁻⁴，在极端接触配置下可能未完全收敛。

**后续启发**：
- 法向与切向障碍的模块化分离设计，使得接触法向模型（如替换为更复杂的非线性弹性模型）和摩擦模型（如替换为各向异性摩擦）可以独立升级，为后续研究提供了灵活的框架。
- 摩擦权重重缩放（Eq. 15）和 Coulomb 锥正则化（Eq. 14）揭示了内点法在摩擦锥顶点附近的数值病态问题，这些技术可迁移至其他基于 Newton 优化的接触求解器。
- 文中指出滞后迭代在特定情况下可能导致收敛问题，这提示了未来工作方向：能否在保持效率的前提下，引入法向-切向的完全耦合求解。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/Primal_dual_Non_smooth_Friction_for_Rigid_Body_Animation.pdf]]
