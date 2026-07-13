---
title: "A Memory-Efficient Hierarchical Algorithm for Large-scale Optimal Transport Problems"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Memory_Efficient_Hierarchical_Algorithm_for_Large_scale_Optimal_Transport_Problems.pdf
project_link: null
code_link: null
aliases:
- HHALSOT
- MEHALSOTP
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/large_scale_parallel_and_distributed
core_operator: "HALO通过两个关键设计突破瓶颈：(1) 多尺度层次结构，从粗到细逐步求解，粗层解为细层提供高质量初始化；(2) 基于活动支撑集（active support）的稀疏化策略，利用最优传输计划天然稀疏性（最多m+n个非零元），将求解限制在估计的支撑集上，并通过保守更新（包含历史支撑集）和对偶违规校正保证收敛。"
primary_logic: "将多尺度层次结构与GPU友好的无分解一阶LP求解器（如PDHG）相结合，并引入活动支撑集主动剪枝技术，在保持O(n)内存复杂度的同时实现尺度无关的迭代复杂度上界，从而在中等维度大规模OT问题上同时达到高精度、低内存和GPU并行效率。"
claims:
- "HALO在DOTmark上n=1024²时实现8.9倍加速和70.5%内存减少"
- "HALO在ModelNet10上n=2^18时实现1.84倍加速、83.2%内存减少和24.9%更低传输成本"
- "HALO每层内迭代次数与问题规模无关（平均不超过2次）"
- "HALO内存复杂度为O(n)，与现有GPU求解器最低水平相当"
---

# A Memory-Efficient Hierarchical Algorithm for Large-scale Optimal Transport Problems

> [!tip] 核心洞察
> 将多尺度层次结构与GPU友好的无分解一阶LP求解器（如PDHG）相结合，并引入活动支撑集主动剪枝技术，在保持O(n)内存复杂度的同时实现尺度无关的迭代复杂度上界，从而在中等维度大规模OT问题上同时达到高精度、低内存和GPU并行效率。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 一种面向大规模最优传输问题的内存高效分层算法 |
| 英文题名 | A Memory-Efficient Hierarchical Algorithm for Large-scale Optimal Transport Problems |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=CkOBcyntGd) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/large_scale_parallel_and_distributed |
| Method | HALO (Hierarchical Algorithm for Large-scale Optimal Transport) |
| Dataset | DOTmark, ModelNet10 (3D) |

> [!tip] 效果简介
> - DOTmark 上，运行时间 (s) 为 27.73，对比 HOT: 246.00，变化 8.9×加速。
> - DOTmark 上，GPU内存 (GB) 为 6.25，对比 HOT: 21.20，变化 70.5%减少。
> - ModelNet10 (3D) 上，运行时间 (s) 为 ~1.84×加速，对比 HiRef，变化 1.84×加速。

## 概要

大规模最优传输问题的核心瓶颈在于内存与可扩展性。传统线性规划求解器（如网络单纯形法、内点法）需存储完整的 $m \times n$ 耦合矩阵，当 $n = 1024^2$ 时变量数接近 $10^{12}$，导致内存消耗巨大且难以利用GPU并行能力。本文提出的HALO（Hierarchical Algorithm for Large-scale Optimal Transport）通过三个关键设计突破这一瓶颈：**多尺度层次结构**从粗到细逐步求解，粗层解为细层提供高质量初始化；**基于活动支撑集（active support）的稀疏化策略**利用最优传输计划天然稀疏性（最多 $m+n$ 个非零元），通过保守更新（包含历史支撑集）和对偶违规校正保证收敛；**无分解一阶LP求解器（cuPDLPx）** 在GPU上高效求解受限问题。这一组合实现了 $O(n)$ 内存复杂度，与现有GPU求解器最低水平相当。

主要结果方面：在2D图像基准DOTmark上，$n=1024^2$ 时HALO相比最强GPU基线HOT实现 **8.9倍加速** 和 **70.5%内存减少**；在3D点云ModelNet10上，$n=2^{18}$ 时相比低秩方法HiRef实现 **1.84倍加速**、**83.2%内存减少** 和 **24.9%更低传输成本**。消融实验表明，多尺度框架和cuPDLPx均不可或缺：禁用cuPDLPx导致 $r=256$ 时36.9倍减速，禁用多尺度框架导致 $r=64$ 时85.6倍减速并在更高分辨率内存溢出。此外，每层内迭代次数平均不超过2次（见Table 2），验证了尺度无关的迭代复杂度上界。



最优传输（Optimal Transport, OT）问题旨在寻找两个概率分布间成本最小的传输方案，其核心公式为Kantorovich公式：$\operatorname* { i n f } _ { \pi \in \Pi ( \mu , \nu ) } \int _ { \mathbb { S } \times \mathbb { D } } c ( s , d ) \mathrm { d } \pi ( s , d )$。在离散场景下，该问题可等价转换为一个标准线性规划（LP）问题：$\operatorname* { m i n } _ { { \pmb x } \geq 0 } { \pmb c } ^ { \top } { \pmb x } , \quad \mathrm { s . t . } \quad { \pmb A } { \pmb x } = { \pmb q }$。然而，当处理大规模问题时，现有求解器面临严重的内存瓶颈和可扩展性限制。传统LP求解器（如网络单纯形法、内点法）需要存储完整的$m \times n$维耦合矩阵$\pmb x$，当$n=1024^2$时变量数接近$10^{12}$，导致内存消耗巨大且无法充分利用GPU并行能力。

针对上述瓶颈，现有方法主要分为几类：基于熵正则化的Sinkhorn算法及其变体（如M3S）、基于Halpern迭代的GPU求解器HOT、基于CPU的多尺度OT求解器ShortCut（使用激进剪枝策略），以及低秩OT方法HiRef。然而，这些方法在可扩展性、内存效率和精度之间难以取得平衡。ShortCut虽然通过多尺度结构和剪枝降低了复杂度，但其基于CPU的LEMON求解器无法利用GPU并行能力，且激进剪枝策略可能导致解质量下降。HOT和HiRef在GPU上运行，但内存消耗仍然较高。

本文提出的HALO（Hierarchical Algorithm for Large-scale Optimal Transport）旨在同时解决上述三个挑战。其核心动机在于：**将多尺度层次结构与GPU友好的无分解一阶LP求解器相结合，并引入活动支撑集主动剪枝技术**，从而在保持$O(n)$内存复杂度的同时实现尺度无关的迭代复杂度上界。具体而言，HALO通过两个关键设计突破瓶颈：(1) 多尺度层次结构，从粗到细逐步求解，粗层解为细层提供高质量初始化；(2) 基于活动支撑集（active support）的稀疏化策略，利用最优传输计划天然稀疏性（最多$m+n$个非零元），将求解限制在估计的支撑集上，并通过保守更新（包含历史支撑集）和对偶违规校正保证收敛。

与ShortCut相比，HALO在三个关键设计维度上做出了改变：首先，底层LP求解器从CPU上的LEMON替换为GPU上的cuPDLPx（基于PDHG的无分解一阶方法），从而充分利用GPU并行能力；其次，活动支撑集更新策略从仅保留当前耦合支撑集的激进剪枝改为保守更新，新支撑集包含历史所有支撑集，并加入对偶违规校正（使用Top_K算子选择最大对偶违规对，推荐$K = \beta |S|$，$\beta=2^{-2}$）；最后，层次构建方式针对图像采用递归合并$2\times 2$像素块并使用块重心作为代表点，针对点云使用$2^d$树或kd树。

实验证据表明，HALO在DOTmark上$n=1024^2$时实现了8.9倍加速和70.5%内存减少，在ModelNet10上$n=2^{18}$时实现了1.84倍加速、83.2%内存减少和24.9%更低传输成本。消融实验进一步验证了多尺度框架和cuPDLPx均不可或缺：禁用cuPDLPx导致$r=256$时36.9倍减速；禁用多尺度框架导致$r=64$时85.6倍减速并在更高分辨率内存溢出。此外，每层内迭代次数平均不超过2次，验证了尺度无关的迭代复杂度上界。



## 核心方法与创新机理

HALO（Hierarchical Algorithm for Large-scale Optimal Transport）的核心创新在于将**多尺度层次结构**与**GPU友好的无分解一阶LP求解器**（如PDHG）相结合，并引入**活动支撑集主动剪枝**技术，在保持O(n)内存复杂度的同时实现尺度无关的迭代复杂度上界。这一设计直接针对现有最优传输求解器在处理大规模问题时的根本瓶颈：传统LP求解器（如网络单纯形法、内点法）需要存储完整的mn维耦合矩阵，当n=1024²时变量数接近10¹²，导致内存消耗巨大且无法充分利用GPU并行能力。

**因果机制**：HALO通过两个关键设计突破瓶颈。首先，多尺度层次结构从粗到细逐步求解，粗层解为细层提供高质量初始化，从而加速内层循环（每层内迭代次数平均不超过2次，验证了尺度无关的迭代复杂度）。其次，活动支撑集策略利用最优传输计划的天然稀疏性（最多m+n个非零元），将求解限制在估计的支撑集上，并通过保守更新（包含历史支撑集）和对偶违规校正保证收敛。

**关键改进点（相对于baseline ShortCut）**：
- **活动支撑集更新策略**：ShortCut采用激进剪枝策略，仅保留当前耦合的支撑集；HALO采用保守更新，新支撑集包含历史所有支撑集，并加入对偶违规校正（Top_K选择最大对偶违规对，K=β|S|，推荐β=2^{-2}）。这一改进显著提升了鲁棒性——消融实验（Table 11）显示，β=0（禁用校正）导致r=1024时运行时间从25.42s增加到52.85s。
- **底层LP求解器**：ShortCut使用CPU上的LEMON求解器（传统LP方法）；HALO使用GPU上的cuPDLPx（基于PDHG的无分解一阶方法）。消融实验（Table 4）证明两者均不可或缺：禁用cuPDLPx导致r=256时36.9倍减速；禁用多尺度框架导致r=64时85.6倍减速并在更高分辨率OOM。
- **层次构建方式**：ShortCut使用基于四叉树的多尺度结构；HALO在图像设置中递归合并2×2像素块（使用块重心作为代表点），在点云设置中使用2^d树或kd树。

**核心洞察**：HALO证明了多尺度层次结构与活动支撑集剪枝的结合可以同时实现高精度、低内存和GPU并行效率——在DOTmark上n=1024²时实现8.9倍加速和70.5%内存减少（Table 1），在ModelNet10上n=2^18时实现1.84倍加速、83.2%内存减少和24.9%更低传输成本（Table 7）。理论分析（Appendix B.1）证明了最终支撑集大小满足|N_k| ≤ (1+β)C₀|S|，即与源点数量成线性关系，从而保证了O(n)内存复杂度。



![[assets/figures/papers/iclr26_0003_CkOBcyntGd_A_Memory-Efficient_Hierarchical_Algorithm_for_La/figures/001_Figure_1.jpg]]
*Figure 1: Architecture of HALO*

HALO（Hierarchical Algorithm for Large-scale Optimal Transport）的整体架构围绕一个核心洞察设计：将多尺度层次结构与GPU友好的无分解一阶LP求解器（如PDHG）相结合，并引入活动支撑集主动剪枝技术，从而在保持O(n)内存复杂度的同时实现尺度无关的迭代复杂度上界。其pipeline由三个相互耦合的模块构成，形成一个从粗到细、交替更新的闭环系统。

**层次构建模块**负责构建一个(L+1)级的OT问题层次，从最粗的第L级到最细的第0级。对于图像数据（规则网格），层次通过递归合并2×2像素块构建，使用每个块的重心作为代表点；对于点云数据，则使用2^d树或kd树。这一过程将原始大规模OT问题分解为一系列规模递减的子问题，为粗到细的求解策略提供基础。

**粗层求解与延拓初始化模块**在最粗层L上求解OT问题，得到初始解后，通过延拓操作将粗层解（包括耦合矩阵x、对偶变量f和g）传递到细一层，作为该层的初始解。这一机制是关键瓶颈的因果旋钮之一：高质量初始化极大地加速了内层循环的收敛，使得每层的内迭代次数平均不超过2次，实现了尺度无关的迭代复杂度。

**活动支撑集更新与受限OT求解模块**是HALO的核心创新所在。该模块交替执行两个操作：(1) `updateActive`基于当前解更新活动支撑集，采用保守更新策略——新支撑集包含历史所有支撑集，而非仅保留当前耦合的支撑集，并通过对偶违规校正（使用Top_K算子选择最大对偶违规对，K = β|S|，推荐β=2^{-2}）来保证收敛性；(2) `solveRestricted`在更新后的活动支撑集上求解受限OT问题，使用cuPDLPx作为默认底层求解器。活动支撑集策略利用了最优传输计划的天然稀疏性（最多m+n个非零元），将求解限制在估计的支撑集上，从而将内存复杂度从O(mn)降低到O(n)。



HALO的核心设计围绕三个相互耦合的模块展开：多尺度层次结构、活动支撑集稀疏化策略以及GPU友好的无分解一阶LP求解器。本节梳理各模块的关键机制与核心公式。

### 多尺度层次结构与递推求解

HALO构建一个(L+1)级的OT问题层次，从最粗的第L级到最细的第0级。对于图像数据，层次通过递归合并2×2像素块构建，以每个块的重心作为代表点；对于点云，则使用2^d树或kd树。

第ℓ层的OT问题等价地写成min-max形式：

$$
\operatorname* { m i n } _ { \substack { x ^ { ( \ell ) } \in \mathbb { R } _ { + } ^ { m } \varepsilon ^ { n } } } \operatorname* { m a x } _ { \substack { f ^ { ( \ell ) } \in \mathbb { R } ^ { m } \varepsilon , g ^ { ( \ell ) } \in \mathbb { R } ^ { m } \varepsilon } } \langle { \pmb u } ^ { ( \ell ) } , { \pmb f } ^ { ( \ell ) } \rangle + \langle { \pmb v } ^ { ( \ell ) } , { \pmb g } ^ { ( \ell ) } \rangle + \langle { \pmb c } ^ { ( \ell ) } , { \pmb x } ^ { ( \ell ) } \rangle - \langle { \pmb A } ^ { ( \ell ) } { \pmb x } ^ { ( \ell ) } , ( { \pmb f } ^ { ( \ell ) } , { \pmb g } ^ { ( \ell ) } ) \rangle
$$

其中 $\pmb u^{(\ell)}, \pmb v^{(\ell)}$ 为第ℓ层的源和目标测度，$\pmb c^{(\ell)}$ 为成本矩阵，$\pmb A^{(\ell)}$ 为约束矩阵。求解从最粗层L开始，得到初始解 $(u^{(L)}, v^{(L)}, c^{(L)})$ 后，通过延拓操作将粗层解作为细层的初始化。这种粗到细的递推策略使得每层内所需的迭代次数与问题规模无关——实验证据（Table 2）显示平均每层内迭代次数不超过2次。

### 活动支撑集与受限OT求解

最优传输计划的天然稀疏性（最多m+n个非零元）是HALO内存高效的基础。HALO在活动支撑集 $\mathbb{N}$ 上定义受限OT问题：

$$
\operatorname* { m i n } _ { \pmb { x } } ~ \pmb { c } _ { \mathrm { N } } ^ { \top } \pmb { x } _ { \mathrm { N } } ~ s . t . ~ { \cal A } _ { \mathrm { N } } \pmb { x } _ { \mathrm { N } } = \pmb { q } , ~ { \pmb x } _ { \mathrm { N } } \geq \pmb { 0 } ~ { \pmb x } _ { \mathrm { N } } = { \bf 0 }
$$

其中 $\mathbb{N}$ 是当前估计的支撑集，$\pmb{c}_\mathbb{N}$ 和 $\pmb{x}_\mathbb{N}$ 分别为限制在 $\mathbb{N}$ 上的成本和决策变量。

活动支撑集的更新（Algorithm 3 `updateActive`）包含两个关键修改，以解决ShortCut激进剪枝策略导致的收敛问题：(i) 保守更新——新支撑集包含历史所有支撑集；(ii) 对偶违规校正——使用Top_K算子选择对偶违规最大的对加入支撑集，其中 $K = \beta|\mathbb{S}|$，推荐 $\beta = 2^{-2}$。

屏蔽（shielding）组件基于几何条件剪枝：若存在 $(s', d')$ 满足

$$
c ( s , d ) + c ( s ^ { \prime } , d ^ { \prime } ) > c ( s , d ^ { \prime } ) + c ( s ^ { \prime } , d )
$$

则 $(s', d')$ 屏蔽了 $s$ 与 $d$ 之间的传输。理论分析（附录B.1）表明，对于平方欧氏距离成本，收敛后活动支撑集大小满足线性上界：

$$
| \mathbb { N } _ { k } | \le C _ { 0 } | \mathbb { S } | + \beta C _ { 0 } | \mathbb { S } | = ( 1 + \beta ) C _ { 0 } | \mathbb { S } |
$$

其中 $C_0$ 为与问题规模无关的常数，$\mathbb{S}$ 为源点集。这一上界揭示了HALO $O(n)$ 内存复杂度的理论根源。

### GPU友好的一阶求解器与重缩放

受限OT问题使用cuPDLPx（基于PDHG的无分解一阶方法）在GPU上求解。为加速收敛，对约束矩阵进行Pock-Chambolle重缩放：

$$
D _ { r } = \mathrm { d i a g } \big ( \sqrt { r _ { 1 } } , \ldots , \sqrt { r _ { m } } , \sqrt { c _ { 1 } } , \ldots , \sqrt { c _ { n } } \big ), \quad D _ { c } = \sqrt { 2 } I , \quad \widetilde { B } = D _ { r } ^ { - 1 } B D _ { c } ^ { - 1 }
$$

重缩放后的矩阵满足 $\| \widetilde { B } \| _ { 2 } = 1$，这一单位谱范数性质使得PDHG算法可以采用常数步长，避免了幂迭代法的额外计算开销。实验（Table 6）验证了常数步长相对幂迭代法的加速效果。

### 解质量评估指标

HALO使用两个指标评估解质量：相对目标值差距（gap）和可行性误差（feas）：

$$
\mathrm { g a p } = { \frac { | \langle c , x \rangle - \langle c , x _ { b } \rangle | } { | \langle c , x _ { b } \rangle | + 1 } }, \quad \mathrm { feas } = \max\left\{ \frac{\|\min(x,0)\|}{1+\|x\|}, \frac{\|Ax - q\|}{1+\|q\|} \right\}
$$

其中 $x_b$ 为参考解（对于小规模问题使用Gurobi精确解，大规模问题使用HALO自身结果）。



## 实验与关键发现

### 主要结果

HALO在两类大规模OT基准测试上展现了显著的性能优势。在2D图像数据集DOTmark上，当分辨率达到n = 1024²（约100万像素）时，HALO相较于当前最先进的GPU求解器HOT实现了**8.9倍加速**（27.73秒 vs. 246.00秒），同时将GPU内存占用从21.20 GB降低至6.25 GB，降幅达**70.5%**（Table 1）。在解质量方面，HALO的gap和feas指标与精确求解器Gurobi处于同一量级，远优于其他近似方法。值得注意的是，在r=512和1024分辨率下，Gurobi因内存溢出而无法求解降阶模型，而HALO仅使用约6 GB GPU内存即可完成计算。


![[assets/figures/papers/iclr26_0003_CkOBcyntGd_A_Memory-Efficient_Hierarchical_Algorithm_for_La/figures/003_Table_1.jpg]]
*Table 1: The numerical results on DOTmark. “GPU/CPU memory” denotes GPU VRAM for GPUbased methods and CPU RAM for CPU methods (shown in gray). Time is reported in seconds (s) and memory is in gigabytes (GB). gap at r = 512, 1024 are unavailable because solving the reduced model with Gurobi runs out of memory*

在3D点云数据集ModelNet10上（Table 7），当点云规模达到n = 2^18时，HALO相较于最佳基线HiRef实现了**1.84倍加速**和**83.2%的GPU内存减少**（从HiRef的约20 GB降至HALO的约3 GB）。更关键的是，HALO的传输成本比HiRef低**24.9%**，表明其解更接近真实最优解。对于n ≤ 2^14的较小规模，HALO的解与标准EMD求解器的精确解几乎一致（gap < 1e-9），验证了其解的高精度。

**可扩展性分析**（Figure 3）进一步揭示了HALO的规模适应能力：在DOTmark上，HALO的运行时间随问题规模呈近线性增长（拟合斜率α ≈ 1），而所有基线方法的运行时间增长斜率均大于1。内存方面，HALO的终端斜率约为2（对应O(n)复杂度），是GPU方法中最低的，且远低于HOT的O(mn)内存增长曲线。

### 消融实验

**多尺度框架和底层求解器的必要性**（Table 4）：消融实验表明，HALO的两个核心组件均不可或缺。禁用cuPDLPx（替换为Gurobi的Barrier方法）导致r=256时运行时间从0.34秒飙升至12.55秒（36.9倍减速）；禁用多尺度框架（即仅在最细层直接求解）导致r=64时运行时间从0.08秒增至6.85秒（85.6倍减速），且在更高分辨率下直接内存溢出（OOM）。这验证了层次化粗到细策略和GPU友好的一阶求解器的协同效应。


![[assets/figures/papers/iclr26_0003_CkOBcyntGd_A_Memory-Efficient_Hierarchical_Algorithm_for_La/figures/008_Table_4.jpg]]
*Table 4: Ablation on HALO. An ‘✗’ in the PDHG-based column indicates that cuPDLPx is replaced by Gurobi’s barrier method with crossover*

**活动支撑集更新策略的鲁棒性**（Table 5）：对偶违规校正（dual-violation correction）是保证HALO鲁棒性的关键。禁用该校正（β=0）后，在DOTmark r=1024时运行时间从25.42秒翻倍至52.85秒（Table 11），且在某些实例上出现收敛停滞。相比之下，β在[2^{-3}, 2^0]范围内性能稳定，推荐默认值β = 2^{-2}。这一机制通过保守更新（保留历史支撑集）和Top_K对偶违规对添加，有效避免了ShortCut激进剪枝策略导致的收敛失败。


![[assets/figures/papers/iclr26_0003_CkOBcyntGd_A_Memory-Efficient_Hierarchical_Algorithm_for_La/figures/009_Table_5.jpg]]
*Table 5: Ablation on updateActive: dual-violation augmentation (✓) improves robustness*

**尺度无关的迭代复杂度**（Table 2）：HALO每层的内迭代次数平均不超过2次，且与问题规模无关。这一经验结果直接验证了理论分析的尺度无关迭代复杂度上界。常数步长相比幂迭代法（power iteration）带来额外加速（Table 6），进一步提升了实际运行效率。


![[assets/figures/papers/iclr26_0003_CkOBcyntGd_A_Memory-Efficient_Hierarchical_Algorithm_for_La/figures/006_Table_2.jpg]]
*Table 2: Number of inner iterations per scale*

### 失败模式与局限性

尽管HALO在平方欧氏距离成本下表现优异，但存在以下已知局限：（1）**一般成本函数的适用性**：当前方法主要针对平方欧氏距离设计，对于欧氏距离等成本函数，一阶求解器可能导致传输计划稀疏性降低，从而影响活动支撑集剪枝效率。（2）**高维扩展性**：屏蔽（shielding）组件的计算开销在高维空间（如数千维）中可能显著增长，限制方法的可扩展性。（3）**参数敏感性**：虽然β在较宽范围内稳定，但最优值在不同数据集上可能略有变化，需要手动调整。此外，ShortCut-GPU在GPU精度下出现的数值停滞问题（Table 12），其具体机制仍需进一步研究。

### 补充图表

![[assets/figures/papers/iclr26_0003_CkOBcyntGd_A_Memory-Efficient_Hierarchical_Algorithm_for_La/figures/007_Table_3.jpg]]
*Table 3: Performance breakdown by image class in DOTmark at resolution 1024 × 1024. Metric sparsity denotes the pixel intensity sparsity, defined as the percentage of pixels with strictly zero mass. Time is reported in seconds (s) Table 4 presents an ablation that isolates the effects of the multiscale framework and the GPUbased LP solver cuPDLPx. When cuPDLPx is disabled, we use Gurobi’s barrier with crossover, as updateActive relies on the sparsity of solutions. Disabling cuPDLPx in HALO results in a 36.9× increase in runtime at r \ = \ 2 5 6 . Removing the multiscale framework from HALO also causes an 85.6× slowdown at r = 64 and leads to OOM at higher resolutions. Taken together, the multiscale...*




## 定位与知识库关联

### 与 baseline/follow-up 的关系

HALO 的核心创新在于将**多尺度层次结构**与**GPU友好的无分解一阶LP求解器**（cuPDLPx）相结合，并引入**活动支撑集主动剪枝**技术。其直接baseline是ShortCut（基于CPU的多尺度OT求解器）和HOT（基于Halpern迭代的GPU求解器）。与ShortCut相比，HALO在两个关键槽位上做出了改变：

- **活动支撑集更新策略**：ShortCut采用激进剪枝（仅保留当前耦合的支撑集），而HALO采用保守更新（新支撑集包含历史所有支撑集），并加入对偶违规校正（Top_K选择最大对偶违规对）。这一改变直接解决了ShortCut在GPU精度下停滞的问题（数值精度影响机制仍需进一步验证）。
- **底层LP求解器**：ShortCut使用CPU上的LEMON求解器（传统LP方法），HALO则使用GPU上的cuPDLPx（基于PDHG的无分解一阶方法）。这一替换使得HALO能够充分利用GPU并行能力，同时避免了传统LP求解器需要存储完整mn维耦合矩阵的内存瓶颈。

与HOT相比，HALO通过多尺度层次结构提供了高质量初始化，显著减少了内层迭代次数（Table 2显示每层内迭代次数平均不超过2次，验证了尺度无关的迭代复杂度）。消融实验（Table 4）表明，多尺度框架和cuPDLPx均不可或缺：禁用cuPDLPx导致r=256时36.9倍减速；禁用多尺度框架导致r=64时85.6倍减速并在更高分辨率OOM。

### 适用边界

HALO的适用边界由以下几个因素决定：

1. **问题规模**：HALO主要针对中等维度大规模OT问题（n=1024²到2^18）。在DOTmark上n=1024²时，HALO实现8.9倍加速和70.5%内存减少；在ModelNet10上n=2^18时，实现1.84倍加速、83.2%内存减少和24.9%更低传输成本。内存复杂度为O(n)，与现有GPU求解器最低水平相当。
2. **成本函数**：当前方法主要针对平方欧氏距离成本设计。对于一般成本函数（如欧氏距离），一阶求解器可能导致稀疏性降低，适用性尚未验证。
3. **数据类型**：HALO支持网格数据（通过递归合并2×2像素块构建层次）和非网格数据（通过2^d树或kd树构建层次，或使用KNN替代局部邻域，k_nn=4×d）。在ModelNet10-PCA 2D非网格数据上，HALO也表现出一致优势（3.47倍加速、82.4%内存减少、32.5%更低传输成本）。
4. **维度**：在高维空间（如数千维）中，屏蔽（shielding）组件的计算开销可能显著增长，扩展性受限。

### 局限与开放问题

**已知局限**：
- 理论分析中的尺度无关迭代复杂度上界依赖于平方欧氏成本等假设，对于更一般的成本函数是否成立尚不明确。
- 对偶违规校正中的β参数需要手动调整（推荐β=2^{-2}），虽然Table 11显示在β∈[2^{-3}, 2^0]范围内性能稳定，但在不同数据集上最优值可能略有变化。
- 对于n≥2^15的ModelNet10，由于EMD求解器不可行，参考解使用HALO自身结果，这在一定程度上限制了大规模场景下的解质量验证。

**开放问题**：
1. 如何将HALO扩展到高维（如数千维）场景，以应对屏蔽组件增长带来的计算开销？
2. 如何处理一般传输成本（如欧氏距离），其中一阶求解器可能导致稀疏性降低？
3. HALO与未来更快的GPU LP求解器结合时性能如何进一步提升？（Table 13显示HALO集成HPR-LP求解器时，在1024分辨率下运行时间为40.76秒，内存6.61GB，表明求解器替换仍有优化空间）
4. ShortCut-GPU在GPU精度下停滞的具体数值精度影响机制是什么？
5. 对于非平方欧氏距离成本函数，屏蔽条件 $c(s,d) + c(s',d') > c(s,d') + c(s',d)$ 是否仍然成立？这直接影响活动支撑集剪枝的有效性。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Memory_Efficient_Hierarchical_Algorithm_for_Large_scale_Optimal_Transport_Problems.pdf

![[paperPDFs/ICLR_2026/A_Memory_Efficient_Hierarchical_Algorithm_for_Large_scale_Optimal_Transport_Problems.pdf]]
