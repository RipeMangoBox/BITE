---
title: A Time-Dependent Inclusion-Based Method for Continuous Collision Detection between Parametric Surfaces
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2024/A_Time_Dependent_Inclusion_Based_Method_for_Continuous_Collision_Detection_between_Parametric_Surfaces.pdf
project_link: null
code_link: "https://github.com/xw-c/TDIB-CCD"
aliases:
- TDIBC
- TDIBMCCDBPS
tags:
- SIGGRAPH_ASIA_2024
- topic/benchmarks_datasets_evaluation
core_operator: 将时间维度从细分空间中分离，通过时间相关的包含函数直接解析出碰撞可能发生的时间子区间。
primary_logic: 利用参数曲面在凸包和线性运动假设下的时间线性性质，设计时间相关的包含函数和与其配套的相交时间区间检测算法，将CCD问题从五维细分降为四维细分，大幅降低迭代次数与计算成本。
claims:
- 相比传统包含式方法实现了36-138倍的加速。
- 完全消除了时间维度的细分，仅对四维空间参数进行细分。
- 在包含函数相交检测时直接给出碰撞可能发生的时间区间，而非布尔结果。
- "1000 random CCD cases (order-3 quadrilateral Bézier patches, OBB) 上 Average time cost [s] (δ=10^{-6}) = 0.079"
---

# A Time-Dependent Inclusion-Based Method for Continuous Collision Detection between Parametric Surfaces

> [!tip] 核心洞察
> 利用参数曲面在凸包和线性运动假设下的时间线性性质，设计时间相关的包含函数和与其配套的相交时间区间检测算法，将CCD问题从五维细分降为四维细分，大幅降低迭代次数与计算成本。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于时间相关包含函数的参数曲面连续碰撞检测方法 |
| 英文题名 | A Time-Dependent Inclusion-Based Method for Continuous Collision Detection between Parametric Surfaces |
| 会议/期刊 | SIGGRAPH ASIA 2024 |
| Links | [paper](https://xw-c.github.io/publication/siga24/) · [Code](https://github.com/xw-c/TDIB-CCD) |
| Topic | #topic/benchmarks_datasets_evaluation |
| Method | Time-Dependent Inclusion-Based CCD |
| Dataset | 1000 random CCD cases, Simulation sequence, Large-scale benchmark (Wang et al. 2021), Handcrafted Dataset - EE CCD |

> [!tip] 效果简介
> - 1000 random CCD cases (order-3 quadrilateral Bézier patches, OBB) 上，Average time cost [s] (δ=10^{-6}) 0.079 vs 10.871 (Trad. OBB) (~138x speedup)。
> - Simulation sequence (cloth-teapot, bicubic Hermite patches) 上，CCD time per frame [s] (ΔT=0.001 s) 0.34 - 2.13 (various frames) vs 4.30 - 14.43 (Trad. OBB) (5x - 36x faster)。
> - Large-scale benchmark (Wang et al. 2021), Handcrafted Dataset - EE CCD 上，Average runtime [µs] / False negatives 3.85 (Ours. OBB) / 0 FN vs 1097.42 (Trad. OBB) / 0 FN (~285x faster)。

## 概要

参数曲面间的连续碰撞检测（CCD）本质是一个五维约束优化问题：在时间区间内寻找两曲面最早接触的时刻。传统包含式方法将时间与曲面参数统一纳入五维空间进行递归细分，导致计算量随维度爆炸，高精度要求下尤其低效。

本文提出**时间相关包含函数（Time-Dependent Inclusion-Based）CCD方法**，核心创新在于将时间维度从细分空间中分离：构建随连续变化的时间相关包围盒，通过解析求解线性不等式系统直接确定包含函数相交的时间子区间，从而将CCD问题从五维细分降为四维空间参数细分，完全消除时间维度的迭代二分。

实验表明，在1000组随机CCD测试中，本文方法相比传统包含式方法实现**36至138倍加速**（OBB包含函数，容忍度δ=10⁻⁶时平均耗时0.079秒 vs 10.871秒）；在布料-茶壶动态模拟场景中，每帧CCD耗时降低**5至36倍**。方法同时保持了零假阴性，约束残差分布与传统方法相当。

该方法属于包含式CCD路线的改进，将传统静态扫掠体包围盒替换为时间相关的紧致边界，并配套相交时间区间检测算法，在保持保守性前提下大幅提升计算效率。

## 核心方法与创新机理

### 问题定义与瓶颈分析

连续碰撞检测（CCD）的目标是寻找两运动参数曲面在时间区间 $[0, \Delta T]$ 内首次发生接触的最早时刻。该问题可形式化为五维约束优化问题：

$$\min_{t,u_1,v_1,u_2,v_2} t \quad \text{s.t.} \quad S_1(u_1,v_1,t) = S_2(u_2,v_2,t), \; 0 \le u_1,v_1,u_2,v_2 \le 1, \; 0 \le t \le \Delta T$$

其中 $S_1, S_2$ 为两参数曲面，$(u_1,v_1)$ 和 $(u_2,v_2)$ 分别为其空间参数坐标，$t$ 为时间变量。传统包含式CCD方法将整个五维参数区间 $I = [u_1^l, u_1^u] \times [v_1^l, v_1^u] \times [u_2^l, u_2^u] \times [v_2^l, v_2^u] \times [t^l, t^u]$ 统一进行递归细分，每次细分产生 $2^5 = 32$ 个子区间。当精度要求提高时，细分次数急剧增长，导致计算量随维度指数爆炸。这是本文所解决的核心瓶颈。

### 核心创新机制：时间维度分离

本文的关键洞察是：在凸包性质和线性运动假设下，参数曲面随时间的变化是线性的，因此时间维度可以从细分空间中分离出来，通过解析方式直接处理。具体而言，方法提出了一种**时间相关的包含函数**（time-dependent inclusion function），该函数在每个固定时刻 $t$ 给出曲面在该时刻的紧致包围盒，而非传统方法中包围整个时间区间内扫掠体的静态包围盒。

这一创新将CCD问题从五维细分降为四维细分。重新定义的四维参数区间为：

$$\tilde{I} = [u_1^l, u_1^u] \times [v_1^l, v_1^u] \times [u_2^l, u_2^u] \times [v_2^l, v_2^u]$$

时间维度则通过包含函数相交的解析条件来确定。对于给定的四维空间参数区间 $\tilde{I}$，可行的碰撞时间集合定义为：

$$\tilde{\cup} t = \{ t \mid \tilde{\cup} S_1(\tilde{I}, t) \cap \tilde{\cup} S_2(\tilde{I}, t) \neq \emptyset \}$$

其中 $\tilde{\cup} S(\tilde{I}, t)$ 表示曲面 $S$ 在参数区间 $\tilde{I}$ 和时刻 $t$ 下的时间相关包含函数。该集合给出了包含函数可能相交的所有时间子区间，算法仅需在这些子区间内进一步搜索，而无需对整个时间区间进行盲目细分。

### 三个关键Changed Slots

**Slot 1: 包含函数类型——从静态扫掠体包围盒到时间相关连续包围盒**

传统方法使用包围整个时间区间内曲面扫掠体的静态AABB或OBB作为包含函数。该包围盒必须同时覆盖 $t^l$ 到 $t^u$ 之间所有可能的位置，因此极为松散。本文方法使用随 $t$ 连续变化的时间相关包含函数，其AABB形式定义为：

$$\tilde{\Pi} S(\tilde{I}, t) = \{ x \mid \min_{ij}(p_{ij}+t\dot{p}_{ij}) \le x \le \max_{ij}(p_{ij}+t\dot{p}_{ij}) \}$$

其中 $p_{ij}$ 为曲面控制点在 $t=0$ 时的位置，$\dot{p}_{ij}$ 为控制点的速度向量。该包含函数在每个时刻 $t$ 仅包围曲面在该时刻的实际位置，因此比传统扫掠体包围盒紧致得多。OBB版本则进一步利用参数坐标映射方向计算定向轴，并通过分离轴定理构造更紧致的包围盒。

**Slot 2: 细分空间维度——从五维到四维**

传统方法对五维区间 $(u_1, v_1, u_2, v_2, t)$ 进行均匀细分，每次迭代产生32个子区间。本文方法仅对四维空间参数区间 $(u_1, v_1, u_2, v_2)$ 进行细分，每次迭代仅产生 $2^4 = 16$ 个子区间。时间维度的处理完全交由后续的相交时间区间检测算法以解析方式完成，从根本上避免了时间维度细分带来的组合爆炸。

**Slot 3: 碰撞时间确定方式——从迭代二分到解析求解**

传统方法在判断包含函数相交后，需要对时间区间反复二分（bisection）直至满足精度要求 $\delta$。本文方法通过求解线性不等式系统，直接解析计算出包含函数相交的时间子区间 $[\tau_{\min}, \tau_{\max}]$。基于分离轴定理，两时间相关包含函数在某轴方向 $e_k$ 上相交的充要条件为：

$$\min_{ij}[(p_{ij}^{(2)}+t\dot{p}_{ij}^{(2)})\cdot e_k] \le \max_{ij}[(p_{ij}^{(1)}+t\dot{p}_{ij}^{(1)})\cdot e_k]$$

且

$$\min_{ij}[(p_{ij}^{(1)}+t\dot{p}_{ij}^{(1)})\cdot e_k] \le \max_{ij}[(p_{ij}^{(2)}+t\dot{p}_{ij}^{(2)})\cdot e_k]$$

由于控制点位置和速度均为已知常数，上述不等式中的 $\min$ 和 $\max$ 函数均为关于 $t$ 的分段线性函数。通过计算这些分段线性函数的轮廓（profile），可以精确确定每个不等式成立的时间区间，进而对所有轴方向的结果取交集，得到包含函数整体相交的时间子区间。这一过程完全避免了传统方法中反复二分带来的计算开销。

### 算法模块与执行流程

本文CCD算法由三个核心模块串联构成，其执行流程如下：

**模块1: 时间相关包含函数构建**

对于输入的两曲面当前子贴片及其控制点速度，模块构建时间相关的AABB或OBB包含函数。对于AABB，直接计算各坐标轴方向上控制点位置与速度的极值，得到形如 $\min(p+tv)$ 和 $\max(p+tv)$ 的线性函数。对于OBB，首先利用曲面在 $t=0$ 时的形状计算定向轴（通过参数坐标映射方向的平均差分，避免昂贵的SVD分解），然后将控制点投影到各定向轴上，同样得到关于 $t$ 的线性极值函数。OBB轴在单个时间步内保持固定，以维持包含函数的线性性质。

**模块2: 包含相交时间区间检测（IntersectionPeriod算法）**

该模块是本文方法的核心计算单元。对于给定的四维空间参数区间 $\tilde{I}$，模块求解两时间相关包含函数相交的时间子区间。算法遍历分离轴定理要求的所有轴方向（对于AABB为3个坐标轴，对于OBB最多15个轴），在每个轴方向上：

1. 提取 $\min$ 和 $\max$ 函数中所有控制点的线性函数 $p_{ij} + t\dot{p}_{ij}$；
2. 计算这些线性函数的分段轮廓，确定 $\min$ 函数和 $\max$ 函数在 $t \in [0, \Delta T]$ 内的分段线性表达式；
3. 求解不等式 $\min^{(2)}(t) \le \max^{(1)}(t)$ 和 $\min^{(1)}(t) \le \max^{(2)}(t)$ 成立的时间区间；
4. 对所有轴方向的结果取交集，得到最终的相交时间区间 $[\tau_{\min}, \tau_{\max}]$。

若交集为空，则两包含函数在该空间参数区间内不可能相交，该区间被安全排除。若交集非空，则 $[\tau_{\min}, \tau_{\max}]$ 给出了碰撞可能发生的时间范围。为提高对浮点误差的鲁棒性，算法在不等式求解时引入了微小的截距偏移（百万分之一量级），在不显著影响保守性的前提下增强了数值稳定性。

**模块3: 四维空间细分与优先级队列**

算法维护一个按 $\tau_{\min}$ 排序的优先级队列。初始时将整个四维空间参数区间 $\tilde{I} = [0,1]^4$ 入队。每次迭代从队列中取出 $\tau_{\min}$ 最小的区间：

1. 调用模块1构建该区间的时间相关包含函数；
2. 调用模块2计算相交时间区间；
3. 若不相交，则丢弃该区间；
4. 若相交且区间宽度 $w(\tilde{I}) < \delta$（$\delta$ 为预设容忍度），则报告碰撞并返回 $\tau_{\min}$ 作为碰撞时间；
5. 否则，将四维空间参数区间均匀细分为16个子区间，对每个子区间重复上述过程，将存在相交时间区间的子区间按 $\tau_{\min}$ 重新入队。

该优先级队列策略确保算法始终优先探索最早可能发生碰撞的区域，从而快速定位首次碰撞时刻。与传统五维细分方法相比，本文方法每次迭代的细分分支数从32降至16，且时间维度的处理由模块2以解析方式一次性完成，无需迭代逼近。

### 因果链路总结

整个方法的核心因果链可概括为：**线性运动假设 → 时间相关包含函数的线性性质 → 相交时间区间的解析可解性 → 时间维度从细分空间中分离 → 五维细分降为四维细分 → 迭代次数和计算成本的大幅降低**。各模块之间的因果关系为：模块1提供了时间相关包含函数的线性结构，这是模块2能够解析求解相交时间区间的数学基础；模块2输出的 $\tau_{\min}$ 为模块3的优先级队列提供了排序依据，确保算法的高效剪枝；模块3的四维细分策略则充分利用了模块2排除大量无关时间区间的能力，避免了传统方法在时间维度上的盲目细分。

### 适用范围与假设条件

本方法依赖以下关键假设：曲面控制点的运动为定速直线运动（即 $\dot{p}_{ij}$ 为常数），曲面基函数满足凸包性质（因此不适用于含负权重的有理Bézier贴片），且曲面在单个时间步内不发生拓扑变化。在这些假设下，时间相关包含函数关于 $t$ 严格线性，从而保证了相交时间区间检测算法的正确性和完备性。

![[assets/figures/papers/paper_list_l47_https_xw_c_github_io_publication_siga24/figures/001_Figure_1.jpg]]
*Figure 1: We solve the CCD problem between a bunny model composed of linear triangles and a torus model composed of rational Bézier patches. The trajectories are obtained by discretizing a rigid motion into time-linear pieces. Our time-dependent inclusion-based method treats all geometric primitives in an efficient and unified way*

![[assets/figures/papers/paper_list_l47_https_xw_c_github_io_publication_siga24/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline for one iteration of traditional inclusion-based CCD method (top) and our time-dependent inclusion-based CCD method (bottom). Given two surface patches at ?? = 0 and the velocities of their individual control points, the CCD problem, as defined in (a), seeks the earliest time of impact within the time interval [0, Δ?? ]. Under the linear trajectory assumption, the control points’ paths are represented by dashed black lines. For both methods, the main sequential steps are: computing the inclusion functions (b), detecting inclusion intersection (c), and performing subdivision (d). In the traditional method, the inclusion function for each patch is the bounding box of its swept volume...*

![[assets/figures/papers/paper_list_l47_https_xw_c_github_io_publication_siga24/figures/005_Figure_5.jpg]]
*Figure 5: The distribution of the constraint residuals for our method, the traditional inclusion-based method (Trad.) and the SOSP method described in Zhang et al. [2023a] across 1000 random cases*

## 实验与关键发现

### 核心性能：随机案例基准测试

本文在1000个随机生成的CCD案例上进行了系统性评估，覆盖了三角形贴片（T.）和四边形贴片（Q.）的1至3阶Bézier形式，以及两种包含函数类型（AABB和OBB）。Table 1报告了在容忍度 $δ = 10^{-6}$ 下的核心结果：对于三次四边形贴片（order-3 Q.），本文方法配合OBB包含函数的平均耗时为 **0.079 ms**，而传统五维包含式方法（Trad. OBB）为 **10.871 ms**，加速比达到约 **138倍**。即使使用较宽松的AABB包含函数，本文方法（0.111 ms）仍比传统AABB方法（5.479 ms）快约49倍。

这一加速的根本原因在于维度缩减带来的指数级收益：传统方法每次细分将五维区间分裂为 $2^5 = 32$ 个子区间，而本文方法仅需对四维空间参数域进行 $2^4 = 16$ 路细分，且时间维度的处理通过解析求解不等式系统一次性完成，无需迭代二分。Fig. 4的耗时分布直方图进一步揭示了稳定性差异——传统方法的耗时分布呈长尾形态，部分案例耗时极高；本文方法的分布则高度集中，表明其性能对案例几何特征的敏感度显著降低。

与基于平方和规划（SOSP）的CCD方法（Zhang et al., SIGGRAPH 2023）相比，本文方法在低阶贴片上优势更为明显。对于一阶四边形贴片（order-1 Q.），本文方法（0.006 ms）比SOSP（0.130 ms）快约22倍；但随着贴片阶数升高，SOSP的计算成本增长更快，而本文方法保持了较好的可扩展性。

### 精度与收敛性验证

Fig. 5展示了三种方法的约束残差（$|F|_2$）分布。本文方法与SOSP方法的残差分布相近，均集中在较低水平，而传统方法的残差分布更为分散。这表明时间相关包含函数的紧致性并未以牺牲精度为代价。

Fig. 6的收敛性曲线验证了方法的数值收敛行为：随着容忍度 $δ$ 从 $10^{-4}$ 收紧至 $10^{-8}$，时间误差 $E_t$ 和参数误差 $E_{uv}$ 均呈单调下降趋势，且下降速率与理论预期一致。这证明了基于包含函数相交时间区间检测的细分终止准则能够有效控制数值解的精度。

### 容忍度敏感性与可扩展性

Table 1的跨容忍度对比揭示了本文方法的关键可扩展性优势。以三次四边形贴片配合OBB为例：当 $δ$ 从 $10^{-4}$ 收紧至 $10^{-6}$（精度提升100倍），本文方法的耗时仅从0.027 ms增至0.079 ms（增长约 **2.9倍**），而传统方法从0.219 ms飙升至10.871 ms（增长约 **50倍**）。这一差异直接源于时间维度分离的架构优势——传统方法的时间二分迭代次数随精度要求线性增长，而本文方法的解析时间区间计算几乎不受 $δ$ 影响，仅在四维空间细分上产生额外开销。

### 模拟序列中的实际性能

在布料-茶壶动态模拟场景中（Fig. 7，20×20双三次Hermite贴片布料与32贴片茶壶），本文方法在五个常用时间步长（$ΔT = 0.001$ s至 $0.016$ s）下均展现出稳定且显著的加速效果。Table 2记录了选定帧的CCD耗时：在 $ΔT = 0.001$ s时，本文方法单帧耗时范围为 **0.34–2.13 s**，而传统方法为 **4.30–14.43 s**，加速比约 **5–36倍**。值得注意的是，随着时间步长增大（物体在一个步长内移动距离增加），传统方法的扫掠体包围盒变得更加膨胀，导致包含函数相交测试的假阳性率上升、无效细分增多；而本文方法的时间相关包含函数在每个时间实例上保持紧致，因此性能退化更小。

![[assets/figures/papers/paper_list_l47_https_xw_c_github_io_publication_siga24/figures/010_Table_2.jpg]]
*Table 2: The statistic of time costs for performing CCD detection on the selected frames as shown in Fig. 7 using both the traditional method and our method across five commonly used time steps Δ??*

![[assets/figures/papers/paper_list_l47_https_xw_c_github_io_publication_siga24/figures/008_Figure_7.jpg]]
*Figure 7: A square sheet of square cloth (20 × 20 bicubic Hermite patches) drapes on a teapot (32 bicubic Hermite patches) under gravity, eventually sliding down along the handle. The simulation runs smoothly and stably at a 2 ms time step, with no visible interpenetration between cloth and teapot*

在Wang et al. (2021)的大规模基准测试集上（Table 3），本文方法在EE CCD（边-边连续碰撞检测）子集上取得了 **3.85 µs** 的平均运行时间，传统方法为 **1097.42 µs**，加速约285倍，且两种方法的假阴性（FN）均为0。这一结果验证了方法在工业级规模测试中的正确性和效率优势。

![[assets/figures/papers/paper_list_l47_https_xw_c_github_io_publication_siga24/figures/011_Table_3.jpg]]
*Table 3: The statistics of the average runtime in µs (t), number of false positive (FP), and number of false negative (FN) for both of our method and the traditional method (Trad.) on the large-scale benchmark datasets proposed by Wang et al. [2021]*

### 消融实验：包含函数类型的影响

Table 1中的AABB与OBB行对比构成了包含函数类型的消融实验。对于本文方法，OBB相较于AABB在三次四边形贴片上带来了约29%的额外加速（0.111 ms → 0.079 ms），这是因为OBB能更紧致地包围曲面贴片，减少了包含函数相交的假阳性，从而降低了四维空间细分的次数。传统方法中OBB的收益更为显著（5.479 ms → 10.871 ms? 原文此处需注意：Table 1中Trad. AABB为5.479 ms，Trad. OBB为10.871 ms，OBB反而更慢——这似乎与"更紧致"的预期矛盾，需要核实原文是否因OBB构建开销更大或实现细节导致。此点标记为需人工验证）。

### 失败模式与适用边界

本文方法存在以下明确的适用边界和失败模式：

1. **有理Bézier贴片的负权重限制**：当有理Bézier贴片包含负权重时，其凸包性质不再成立，导致基于控制点构建的包含函数可能遗漏实际曲面，产生假阴性。该方法仅保证对所有权重非负的有理贴片的保守性。

2. **运动轨迹假设**：当前方法假设物体在时间步长内做匀速直线运动（定速平移）。对于包含旋转的刚体运动，需预先将弯曲轨迹分段线性化为多条直线段，这引入了额外的近似误差和计算开销。论文未提供自适应线性化策略。

3. **浮点误差的鲁棒性不足**：尽管在不等式求解中引入了百万分之一量级的微小截距偏移以增强鲁棒性（Section 4.3），论文明确指出该方法尚未从理论上保证完全消除浮点误差导致的假阴性。在极端几何配置下（如几乎共面、几乎相切的贴片），浮点舍入误差仍可能导致错误的时间区间判定。

4. **自碰撞与相邻贴片碰撞**：当前框架仅处理两个独立曲面之间的碰撞检测，不支持单个高阶贴片内的自碰撞以及共享边界的相邻贴片间碰撞。这些场景需要额外的参数域约束或细分策略。

### 关键实验结论

综合实验证据，本文方法的核心优势可归纳为：**通过将时间维度从细分空间中分离，以解析方式处理时间相关性，实现了对传统包含式CCD方法36–138倍的加速，且加速比随精度要求提高而进一步扩大**。该方法在保持零假阴性的前提下，将CCD的计算瓶颈从"五维指数细分"转化为"四维细分+线性不等式求解"，为参数曲面的交互式物理仿真提供了实用化的连续碰撞检测方案。

## 定位与知识库关联

本文的核心贡献在于改变了连续碰撞检测（CCD）中“包含式细分方法”的两个关键**slot**：**细分空间的维度**和**包含函数的类型**。传统包含式CCD方法（Snyder et al., SIGGRAPH 1993; Von Herzen et al., SIGGRAPH 1990）将CCD问题建模为五维参数空间 $(u_1, v_1, u_2, v_2, t)$ 上的约束优化，通过递归细分五维区间并使用包围整个时间区间内扫掠体的静态AABB/OBB作为包含函数来检测碰撞。随着精度要求提高，五维细分的计算量呈指数增长，这是该类方法长期存在的瓶颈。

本文的**第一个slot改变**是将细分空间从五维降至四维。作者重新定义CCD问题，将时间维度 $t$ 从细分空间中分离，仅对四维空间参数区间 $\tilde{I} = [u_1^l, u_1^u] \times [v_1^l, v_1^u] \times [u_2^l, u_2^u] \times [v_2^l, v_2^u]$ 进行细分。这一改变的直接后果是每次细分从产生 $2^5 = 32$ 个子区间降为 $2^4 = 16$ 个，从根本上缓解了维度爆炸问题。

**第二个slot改变**是将包含函数从“包围整个时间区间扫掠体的静态边界”替换为“随 $t$ 连续变化的时间相关包含函数” $\tilde{\Pi} S(\tilde{I}, t)$。该函数基于控制点的当前位置和速度，为每个时间实例提供紧致边界，而非对整个时间区间取并集。配合这一改变，本文设计了**相交时间区间检测算法**（IntersectionPeriod），通过求解各分离轴方向上的线性不等式系统，直接解析出包含函数相交的时间子区间 $[\tau_{\min}, \tau_{\max}]$，而非传统方法中反复对时间区间二分的做法。这一设计使得算法能在一次检测中排除大量无关时间区间，仅保留碰撞可能发生的时段。

从**知识库挂载点**来看，本文方法可定位为“**包含式CCD方法**”节点下的一个分支改进。其理论基础继承自区间算术和包含函数框架（Snyder, 1993），但在以下方面形成了新的知识节点：

1. **时间维度分离策略**：将时间从细分空间中解耦，利用参数曲面在凸包和线性运动假设下的时间线性性质，通过解析手段处理时间维度。这一思路可推广至其他需要在空间-时间联合域上进行细分的几何查询问题。

2. **时间相关包含函数**：提供了一种连续表示运动曲面的新工具，其紧致性优于传统的扫掠体包围盒。该函数类型可以作为其他基于包含函数的几何算法（如连续自碰撞检测、连续距离计算）的基础组件。

3. **基于线性不等式系统的相交时间求解**：将包含函数相交条件转化为各轴方向的线性不等式组，通过min/max函数的轮廓分析直接计算相交时段。这一算法模块具有独立复用价值。

**适用边界**明确且重要：(1) 仅适用于具有凸包性质的参数曲面（如Bézier贴片、Hermite贴片），不适用于包含负权重的有理Bézier贴片；(2) 仅支持直线（定速）运动轨迹，无法直接处理曲线轨迹（如刚体旋转），需将弯曲轨迹分段线性化；(3) 不支持单个高阶贴片内的自碰撞以及相邻贴片间的碰撞；(4) 浮点误差的鲁棒性尚未完全保证，存在假阴性的理论风险。

与另一类CCD方法——**Sum-of-Squares Programming (SOSP) CCD**（Zhang et al., SIGGRAPH 2023）相比，本文方法的定位差异显著。SOSP将CCD转化为多项式优化问题并通过平方和规划求解，理论上可给出精确碰撞时间，但计算成本极高（实验显示在所有测试案例中均远慢于本文方法）。本文方法则保持了包含式方法的计算效率优势，同时通过维度分离大幅提升了性能。

**后续启发**方面，本文指出的开放问题具有明确的研究指向：(1) 将精确几何计算（EGC）集成进时间相关包含函数框架，以消除浮点误差导致的假阴性，这将使方法具备形式化正确性保证；(2) 开发自适应轨迹线性化策略，将方法扩展至刚体旋转等曲线运动场景，可显著拓宽应用范围；(3) 针对高阶曲面的连续自碰撞检测方案设计，这是布料仿真等应用中尚未解决的关键问题。此外，时间相关包含函数的思想也可能启发连续距离计算、最近点查询等其他时间相关的几何处理任务。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2024/A_Time_Dependent_Inclusion_Based_Method_for_Continuous_Collision_Detection_between_Parametric_Surfaces.pdf]]