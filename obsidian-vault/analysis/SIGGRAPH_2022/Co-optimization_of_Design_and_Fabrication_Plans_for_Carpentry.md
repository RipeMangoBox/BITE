---
title: Co-optimization of Design and Fabrication Plans for Carpentry
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Co_optimization_of_Design_and_Fabrication_Plans_for_Carpentry.pdf
project_link: null
code_link: null
aliases:
- IICEEGBPBEG
- CODFPC
tags:
- SIGGRAPH_2022
- topic/other_unclear
core_operator: 利用设计变体间共享的部件集合（袋部件）进行表示，并通过反馈引导的 e-图 收缩-扩展（ICEE）管理搜索空间。
primary_logic: 不同设计变体往往共享相同的部件袋（bag of parts），将这些共享子结构表示为 BOP e-graph 可以紧凑编码大量候选并平摊优化成本；反馈驱动的 ICEE 循环则能有效聚焦于有前景的帕累托前沿区域，避免穷举。
claims:
- 与仅优化单一设计制造计划的基线相比，ICEE 在多个模型中分别节省 25% 材料、60% 制造时间和 20% 总成本。
- ICEE 比先前方法快多达 17 倍，同时产生质量相当的帕累托前沿。
- 在 16 个测试模型中的 14 个上，联合优化生成的计划完全支配了人类专家制作的计划。
- "在五个模型上，ICEE 比无共享的嵌套基准方法快约一个数量级（例如 Frame: 2.8 min vs 6.5 min）。"
---

# Co-optimization of Design and Fabrication Plans for Carpentry

> [!tip] 核心洞察
> 不同设计变体往往共享相同的部件袋（bag of parts），将这些共享子结构表示为 BOP e-graph 可以紧凑编码大量候选并平摊优化成本；反馈驱动的 ICEE 循环则能有效聚焦于有前景的帕累托前沿区域，避免穷举。

| 字段 | 内容 |
|------|------|
| 中文题名 | 木工设计与制造计划的协同优化 |
| 英文题名 | Co-optimization of Design and Fabrication Plans for Carpentry |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://arxiv.org/abs/2107.12265) · [arXiv](https://arxiv.org/abs/2107.12265") |
| Topic | #topic/other_unclear |
| Method | ICEE (Iterative Contraction and Expansion on E-graphs) with Bag-of-Parts (BOP) E-graph |
| Dataset | 多个木质家具模型（Bookcase, Frame, Loom, Jungle Gym 等）, 五个代表性模型（Frame, Jungle Gym, L-Frame, Table, Window）, 16个家具模型 |

> [!tip] 效果简介
> - 多个木质家具模型（Bookcase, Frame, Loom, Jungle Gym 等） 上，材料使用量 / 制造时间 / 切割精度 的多目标帕累托改善 在 Bookcase 上材料降低 25%，在其他模型上制造时间降低 60%，误差降低 61-77%，总成本节省 5-20% vs 仅优化单一输入的制造计划（Wu et al.）或专家手工计划 (帕累托前沿显著扩展并支配基线)。
> - 五个代表性模型（Frame, Jungle Gym, L-Frame, Table, Window） 上，总运行时间（分钟） 2.8 / 109.0 / 8.2 / 40.8 / 131.7 min vs 6.5 / 761.2 / 59.7 / 612.8 / 2050.0 min（对每个设计变体独立运行 Wu et al.） (快约一个数量级)。
> - 16个家具模型 上，专家计划被支配的比例 14/16 模型生成的帕累托前沿支配专家计划 vs 人类专家按一个或少量设计变体制定的制造计划 (多数模型得到绝对更优的（设计, 计划）对)。

## 概要

木工制造中，离散设计变体（如连接方式、零件分解）与制造计划（如排料、切割顺序）构成巨大的组合搜索空间，传统方法仅对单一输入设计优化制造计划，未能发掘设计改动带来的成本下降潜力。本文提出一种设计与制造计划的协同双层多目标优化方法：将不同设计变体共享的部件集合表示为**袋部件（Bag-of-Parts, BOP）e-graph**，从而紧凑编码大量候选并平摊优化成本；在此基础上，引入**反馈引导的迭代收缩-扩展（ICEE）循环**，每次提取帕累托前沿后，按 e-class 的贡献与探索度进行剪枝，再生成新的有前景设计变体与制造安排，使搜索聚焦于帕累托前沿区域。

实验表明，相较于仅优化单一设计制造计划的基线，ICEE 在多个模型中分别节省 25% 材料、60% 制造时间和 20% 总成本；在 16 个测试模型中的 14 个上，联合优化生成的计划完全支配了人类专家制作的计划；ICEE 比逐变体独立优化的嵌套基线快约一个数量级（最高达 17 倍）。该方法属于**程序合成与制造优化的交叉**，以 e-graph 等价表示和反馈驱动搜索为核心创新，为离散设计-制造联合优化提供了可扩展的新范式。

## 核心方法与创新机理

### 问题瓶颈与核心思路

木工制造中，一个家具设计通常存在大量离散的设计变体（如连接件类型、部件排列方式的不同选择），而每个设计变体又对应一个庞大的制造计划空间（包括零件在板材上的排样、加工顺序等）。这两个空间的笛卡尔积构成了一个极其巨大的组合搜索空间，使得直接进行联合优化在计算上不可行。本文的核心洞察在于：**不同设计变体往往共享相同的部件袋（bag of parts）**——即它们需要切割的零件种类和数量完全相同，只是组装方式不同。例如，一个框架的四种连接件各有三种变体，产生 81 个设计变体，但其中许多变体使用的零件集合是相同的。如果能将这种共享子结构紧凑地编码并复用制造计划的搜索结果，就可以大幅摊薄优化成本。

基于此，本文提出两个关键技术：**Bag-of-Parts (BOP) E-graph** 作为紧凑的搜索空间表示，以及 **ICEE (Iterative Contraction and Expansion on E-graphs)** 作为反馈驱动的双层多目标优化算法。

### 问题形式化：双层多目标优化

木工设计与制造的联合优化被形式化为一个双层多目标优化问题：

$$\operatorname* { m i n } _ { d } F ( d , p ) \ { \mathrm { ~ s . t . ~ } } d \in { \mathcal { D } } , \ p = \arg \operatorname* { m i n } _ { p } F ( d , p )$$

外层选择设计变体 $d$，内层在给定 $d$ 的条件下求解制造计划 $p$ 的帕累托最优。目标向量 $F(s) = (f_m(s), f_p(s), f_t(s))$ 包含三个制造代价：材料用量 $f_m$、加工精度 $f_p$（切割误差）和加工时间 $f_t$。搜索空间 $\mathcal{D}$ 是所有可行设计变体的集合，每个 $d$ 对应一个制造计划空间。

### Changed Slot 1：从单一设计到设计变体 × 制造计划的联合空间

基线方法 **Carpentry Compiler**（Wu et al., ACM TOG 2019）仅对用户给定的单一输入设计优化制造计划，不探索设计变体。本文的 **changed slot** 是将搜索空间从“给定设计的制造计划空间”扩展为“设计变体 × 制造计划的联合空间”。这使得系统能够主动发现那些材料更省、加工更快或精度更高的设计替代方案，而非被动接受用户输入的设计。

### Changed Slot 2：从传统 E-graph 到 BOP E-graph 的等价表示

传统 e-graph 基于程序语义等价来共享子表达式。本文的 **BOP E-graph** 重新定义了等价条件：只要两个（子）设计产生相同的部件袋（multiset of parts），即使零件的分配和板材上的排样方式不同，它们也被视为等价，放入同一个 e-class 中。这种等价定义实现了跨设计变体的最大程度共享。

具体而言，BOP E-graph 包含两类 e-node：

- **原子节点（atomic node）**：$\{\Pi, \Pi, \triangle\}_{p, b}$ 表示将两个正方形和一个三角形通过排样方案 $p$ 打包到同一块类型为 $b$ 的板材上。
- **并集节点（union node）**：$\{\mathsf{D}, \mathsf{D}\}_{\pmb{p}_1, b} \cup \{\triangle\}_{\pmb{p}_2, b}$ 表示将部件分到多块板材上，各自独立排样。

一个根 e-class 可以包含多个等价 e-node，每个 e-node 代表一种不同的制造安排方式。当两个设计变体共享相同的部件袋时，它们的制造安排被放入相同的 e-class，后续的制造计划搜索只需进行一次即可服务于两个设计。

### Changed Slot 3：从无反馈扩展到 ICEE 反馈驱动搜索

传统 e-graph 采用无反馈的饱和扩展策略（持续应用重写规则直到饱和），然后单次提取最优项。这在联合空间中将导致 e-graph 快速膨胀，无法在合理时间内处理。**ICEE** 引入了反馈驱动的迭代收缩-扩展循环，包含五个核心模块：

#### 模块 1：初始设计变体生成（Initial Generation of Design Variants）
依据零件最大重复数的启发式策略，从完整设计空间 $\mathcal{D}$ 中选取一个初始子集。这一步骤避免从一开始就枚举所有变体，而是选择那些零件重复度高、更可能产生共享的候选。

#### 模块 2：初始制造安排生成（Initial Fabrication Arrangements Generation）
为选定的初始设计变体生成少量制造安排，特别偏好那些可堆叠或紧致打包的排样方式。这些安排构成 BOP E-graph 的初始内容。

#### 模块 3：帕累托前沿提取（Pareto Front Extraction）
使用多目标遗传算法 **NSGA-III** 从当前 BOP E-graph 中提取帕累托最优的（设计, 制造计划）对。这是整个算法中最耗时的步骤，但也是反馈信号的核心来源。

#### 模块 4：E-class 评分与 BOP E-graph 收缩（E-class Scoring and Contraction）
对每个 e-class 计算剪枝分数 $P_{score}$：

$$P_{score} = w \cdot I_{score} + (1 - w) \cdot (1 - E_{score}), \quad w \in [0.0, 1.0]$$

其中 $I_{score}$ 衡量该 e-class 对当前帕累托前沿解的贡献程度（影响得分），$E_{score}$ 衡量该 e-class 已被探索的充分程度（探索得分）。权重 $w$ 控制偏向：$w$ 较大时倾向保留有贡献的 e-class，较小时倾向保留尚未充分探索的 e-class。分数较低的 e-class 被剪枝删除，从而收缩 BOP E-graph，将搜索聚焦于有前景的区域。

#### 模块 5：BOP E-graph 扩展（BOP E-graph Expansion）
基于当前帕累托前沿中的设计变体，通过交叉和变异操作生成新的设计变体，并为这些新变体生成额外的制造安排，将其添加到 BOP E-graph 中。探索的设计变体数量由参数 $K_d$ 控制：

$$K_d = 2^{\lceil \log_{10} |\mathcal{D}| \rceil}$$

$K_d$ 随设计空间大小 $|\mathcal{D}|$ 的对数增长，确保在大空间中也保持可控的探索规模。

### 模块间的因果关系

这五个模块构成一个闭环反馈系统：**初始化（模块 1-2）→ 评估（模块 3）→ 聚焦（模块 4）→ 探索（模块 5）→ 评估（模块 3）**。帕累托前沿提取为收缩提供信号（哪些 e-class 有贡献），收缩释放空间为扩展提供可能，扩展引入新候选又为下一轮提取提供素材。循环终止条件包括达到预设时间上限（实验中设为 4 小时）或帕累托前沿不再改善。这种反馈机制使得 ICEE 能够动态管理 BOP E-graph 的规模，避免穷举带来的组合爆炸，同时保持对高质量解的持续探索。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2107_12265/figures/001_Figure_1.jpg]]
*Figure 1: Our system jointly explores the space of discrete design variants and fabrication plans to generate a Pareto front of (design, fabrication plan) pairs that minimize fabrication cost. In this figure, (a) is the input design for a chair and the Pareto front that only explores the space of fabrication plans for this design, (b) shows the Pareto front generated by joint exploration of both the design variants and fabrication plans for the chair, where each point is a (design, fabrication plan) pair. Design variations indicate different ways to compose the same 3D model from a collection of parts and are illustrated with the same color in the Pareto front. A physical chair is fabricated by follo...*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2107_12265/figures/006_Figure_6.jpg]]
*Figure 6: Algorithm overview used the example in Figure 5. The first step initializes a BOP E-graph (Section 4.3.2, Section 4.3.3) with several design variants and a small number of fabrication arrangements (a). U and A represent union and atomic e-nodes respectively. As part of the ICEE loop, the algorithm extracts a Pareto Front (Section 4.3.4) which is used to score the e-classes in the BOP E-graph (b). For example, the gray e-class containing*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2107_12265/figures/013_Figure_9.jpg]]
*Figure 9: Two examples where searching the design space revealed fabrication plans that completely dominated the fabrication plans generated for the input design. With the design variations, our pipeline could search for a design variation of the frame which turns all angled cutting to vertical. With Design B, we find a fabrication plan which takes less time than the least time-consuming plan A of the input design. Similarly, we show two fabrication plans of the A-Bookcase model where the design and fabrication plan B dominates the input design A. The fabrication costs are indicated in the figure with the order of material cost, precision error, and fabrication time. The cutting orders are labeled wi...*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2107_12265/figures/016_Figure_13.jpg]]
*Figure 13: Pareto fronts computed from by our pipeline for the Frame model with three objective functions, material usage*

## 实验与关键发现

### 实验设置概述

实验覆盖 16 个木质家具模型（Bookcase、Frame、Loom、Jungle Gym、Table、Window 等），模型复杂度从 10 个零件到 200+ 个零件不等（Table 1）。制造代价向量定义为 $F(s) = (f_m(s), f_p(s), f_t(s))$，分别对应材料用量、切割精度和制造时间。ICEE 的超参数设定为：初始设计变体探索数 $t_d=10$、最大探索数 $m t_d=200$、总时间上限 $T=4$ 小时。对比基线包括：(1) **Carpentry Compiler**（Wu et al., TOG 2019）——仅对单一输入设计优化制造计划，不探索设计变体；(2) 人类专家手工制定的制造计划；(3) 对每个设计变体独立运行 Wu et al. 方法的“无共享嵌套基线”。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2107_12265/figures/007_Table_1.jpg]]
*Table 1: Statistics for each input model, showing the complexity in number of parts*

### 主实验结果

**联合优化显著扩展帕累托前沿。** 在 16 个测试模型中的 14 个上，ICEE 生成的帕累托前沿完全支配了人类专家计划（Figure 8）。具体而言：

- **Bookcase 模型**：材料使用量降低 **25%**；
- **其他模型**：制造时间降低高达 **60%**，切割误差降低 **61–77%**；
- **总成本节省**：在多个模型上实现 **5–20%** 的总制造成本下降。

这些改善源于设计变体与制造计划的协同搜索——仅优化制造计划无法触及这些更优的（设计, 计划）组合。Figure 9 展示了两个典型案例，其中设计空间搜索揭示的制造计划完全支配了输入设计的制造计划。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2107_12265/figures/011_Figure_8.jpg]]
*Figure 8: Pareto fronts computed from our pipeline with design optimization as colored dots. Each color corresponds to a different design. The gray dots indicate the Pareto fronts of all explored design variations. These are compared against Pareto fronts computed without design optimization (fabrication optimization only, using the original model as the input design) as squares, and expert fabrication plans as diamonds. Often, fabrication plans from a design variant are more optimal than those generated from an input design. For the unit of objective metrics, material usage (???? ) is in dollars, cutting precision (???? ) is in inches, fabrication time (???? ) is in minutes. Some (design, fabricatio...*

**ICEE 实现数量级加速。** 在五个代表性模型上的运行时间对比（Table 3）表明，ICEE 比无共享嵌套基线快约一个数量级：

| 模型 | ICEE (min) | 嵌套基线 (min) |
|------|-----------|---------------|
| Frame | **2.8** | 6.5 |
| Jungle Gym | **109.0** | 761.2 |
| L-Frame | **8.2** | 59.7 |
| Table | **40.8** | 612.8 |
| Window | **131.7** | 2050.0 |

在引言中报告的整体加速比达到 **17×**。这一加速的核心机制是 BOP e-graph 的结构共享：不同设计变体共享相同的部件袋时，其制造安排（排列与包装）在 e-graph 中被合并为等价 e-class，避免了重复计算。嵌套基线则对每个设计变体独立调用完整的制造优化流程，无任何工作共享。

### 消融实验与机制分析

**BOP e-graph 结构共享的必要性。** 去除结构共享（即逐变体独立优化的嵌套基线）导致运行时间增加约一个数量级（Table 3）。这直接验证了“部件袋等价”表示的有效性：当多个设计变体产生相同的零件多集时，BOP e-graph 将其制造安排紧凑编码为共享的 e-class 子树，平摊了搜索和代价评估的计算开销。

**ICEE 反馈收缩机制防止搜索空间膨胀。** ICEE 的收缩步骤根据 e-class 对当前帕累托前沿的贡献度（$I_{score}$）和已有探索度（$E_{score}$）计算剪枝分数 $P_{score} = w \cdot I_{score} + (1-w) \cdot (1 - E_{score})$，删除低分 e-class。这一反馈驱动机制将搜索聚焦于有前景的候选区域，使 e-graph 大小维持在可管理范围内。若去除该机制，e-graph 将在迭代中持续膨胀，无法在规定时间（4 小时）内收敛到合理结果。

**帕累托前沿提取是性能瓶颈。** Table 2 的运行时间分解显示，基于 NSGA-III 的帕累托前沿提取是 ICEE 中最耗时的步骤。这限制了整体效率，也是当前方法的主要计算瓶颈。

### 失败模式与适用边界

**离散设计空间的限制。** BOP e-graph 的等价概念建立在“相同部件袋”之上，仅适用于离散设计变体（如连接件类型选择、零件数量变化）。无法处理连续参数变化（如零件尺寸的连续缩放），这排除了大量需要连续几何优化的设计场景。

**启发式方法的固有局限。** ICEE 无法保证找到真正的全局帕累托前沿。搜索结果受参数影响显著：深度/广度权衡参数 $\alpha$ 控制 e-graph 扩展的激进程度，剪枝权重 $w$ 影响搜索的探索-利用平衡。在大规模设计空间中，添加无益的设计变体反而可能导致结果变差——ICEE 的收缩机制能缓解但无法完全消除这一问题。

**计算资源需求。** 对于复杂模型（如 Window 模型需 131.7 分钟），ICEE 的运行时间仍较长。时间上限 $T=4$ 小时意味着最复杂的模型可能无法在实用时间内完成充分探索。

**目标函数的覆盖范围。** 当前制造代价仅考虑材料用量、切割精度和制造时间。装配难度、结构强度、稳定性等实际制造关切尚未纳入优化目标。Figure 13 展示了将稳定性作为第三目标的初步实验，但更全面的多目标扩展仍是开放问题。

### 关键实验证据强度

| 核心论断 | 证据类型 | 证据强度 |
|---------|---------|---------|
| 联合优化支配专家计划 (14/16) | 16 模型对比实验 | 高（多模型一致） |
| 材料节省 25%，时间降低 60% | 单模型具体数值 | 中（案例依赖，非所有模型均达到） |
| 比嵌套基线快约一个数量级 | 5 模型运行时间对比 | 高（一致性加速） |
| BOP e-graph 共享是关键加速因素 | 消融对比 | 高（因果明确） |
| ICEE 收缩机制防止膨胀 | 定性分析 | 中（需手动验证，未提供去除收缩的定量退化数据） |

需要手动验证的点：ICEE 收缩机制的独立消融实验未提供定量对比数据（如去除收缩后的运行时间或帕累托前沿质量退化），该论断主要基于系统设计的定性论证。

## 定位与知识库关联

### 改变的 Slot：从“单设计制造优化”到“设计-制造联合空间搜索”

本文的核心贡献在于将木工制造优化问题中“搜索空间”这一关键 slot 从**给定设计的制造计划空间**扩展为**设计变体 × 制造计划的联合空间**。基线方法 **Carpentry Compiler**（Wu et al., ACM TOG 2019）仅对单一输入设计优化制造计划，设计本身被视为固定输入，优化的自由度局限于零件在板材上的排列、切割顺序等制造层面的决策。本文指出，离散的设计变体（如连接件类型选择、零件分解方式）与制造计划之间存在强耦合：不同设计可能使用相同的部件集合（bag of parts），从而共享大量制造层面的子结构。将这两个层次联合优化，能够在材料用量、制造时间和切割精度之间获得显著更优的帕累托前沿。

为实现这一联合搜索，本文引入了两个紧密配合的新 slot：**等价表示**从传统 e-graph 的程序语义等价转变为 BOP（Bag-of-Parts）e-graph——只要两个（子）设计产生相同的部件多重集，即使零件的分配和打包方式不同，也被视为等价并共享 e-class；**搜索策略**从无反馈的 e-graph 扩展与单次提取转变为 ICEE（反馈驱动的迭代收缩-扩展），利用帕累托前沿的反馈信息对 e-graph 进行剪枝与定向扩展。这三个 slot 的协同改变是方法有效性的结构基础。

### 知识库挂载点

本文可挂载于制造优化与程序合成交叉领域的以下知识节点：

1. **E-graph 在制造优化中的应用**：e-graph 最初用于程序优化中的等价变换探索（如 Tate et al., POPL 2009; Willsey et al., POPL 2021 的 egg 库），其核心思想是通过等价类共享子表达式以紧凑表示指数级搜索空间。Carpentry Compiler（Wu et al., TOG 2019）首次将 e-graph 引入木工制造计划优化，本文在此基础上将等价概念从“相同制造安排”松弛为“相同部件袋”，大幅提升了跨设计变体的共享程度。这一松弛等价的思想可推广至其他需要联合探索离散设计空间与下游规划的问题。

2. **双层多目标优化**：本文将问题形式化为双层多目标优化——外层选择设计 $d$，内层求解给定 $d$ 的制造计划帕累托最优。该形式化与 architecture-search 类方法（如 NAS 中的双层优化）共享结构，但本文通过 BOP e-graph 将内外层统一编码，避免了嵌套循环的计算开销。这一“扁平化”双层优化的策略对于其他设计-制造耦合领域（如 PCB 布局与布线、增材制造中的支撑结构设计）具有方法论参考价值。

3. **反馈驱动的启发式搜索**：ICEE 的收缩-扩展循环本质上是一种 feedback-directed search，与编译器优化中的 FDO（Feedback-Directed Optimization）和程序合成中的 CEGIS（Counter-Example Guided Inductive Synthesis）共享“利用中间结果引导后续探索”的范式。其独特之处在于评分机制同时考虑 e-class 对帕累托前沿的贡献（$I_{score}$）和已有探索度（$E_{score}$），通过权重 $w$ 控制探索-利用权衡。

### 适用边界

- **离散设计空间限制**：BOP e-graph 的等价定义依赖于部件集合的离散性，无法处理连续参数变化（如零件尺寸的连续缩放）。对于需要连续几何优化的设计场景（如拓扑优化），本方法不适用。
- **启发式本质**：ICEE 不保证找到全局帕累托前沿，其解质量受参数影响（如初始设计变体选择、收缩阶段的剪枝权重 $w$、扩展阶段的交叉变异策略）。原文明确指出，在大规模设计空间中，添加无益的设计变体可能导致结果变差。
- **计算瓶颈**：帕累托前沿提取（使用 NSGA-III）是算法中最耗时的部分，限制了可处理的设计空间规模和目标函数数量。当前实验以 4 小时为超时限制。
- **制造模型假设**：方法继承自 Carpentry Compiler 的制造模型（1D 顺序切割和 2D 板材分区），不适用于 3D 打印、CNC 铣削等其他制造工艺。

### 与基线/相关工作的本质差异

| 维度 | Carpentry Compiler (Wu et al., TOG 2019) | 本文 ICEE + BOP E-graph |
|------|------|------|
| 搜索空间 | 单一设计的制造计划 | 设计变体 × 制造计划的联合空间 |
| 等价定义 | 程序语义等价（相同制造安排） | 部件袋等价（相同 multiset of parts） |
| 搜索策略 | 单次 e-graph 扩展与提取 | 反馈驱动的迭代收缩-扩展 |
| 共享粒度 | 仅制造计划子结构 | 跨设计变体的部件集合共享 |
| 输出 | 单一设计的帕累托前沿 | 多设计变体的联合帕累托前沿 |

与更广泛的制造优化文献（如排样优化中的启发式方法）相比，本文的独特之处在于将设计决策纳入优化循环，而非将其视为前置步骤。与基于学习的方法（如用神经网络预测制造代价）相比，本文的符号化 e-graph 方法具有可解释性和精确性优势，但缺乏对连续参数的泛化能力。

### 后续启发

1. **等价概念的连续化扩展**：如何定义连续参数下的“近似等价”以扩展 e-graph 的共享能力，是突破离散限制的关键开放问题。可能的路径包括引入参数化 e-node 或模糊等价类。

2. **学习加速帕累托提取**：帕累托前沿提取是计算瓶颈，用学习模型预测制造代价以替代昂贵的精确评估，或指导 e-graph 的扩展方向，有望显著加速 ICEE 循环。

3. **跨领域迁移**：ICEE 的反馈收缩-扩展策略可迁移至其他基于 e-graph 的优化领域，如浮点精度调优（Herbie 等）、CAD 参数化设计空间探索、硬件设计空间探索等。任何存在“离散变体 × 下游规划”组合爆炸的场景都可能受益。

4. **多目标扩展**：原文已将稳定性作为第三目标进行初步实验（Figure 13），未来可纳入装配难度、结构强度、美学等更丰富的目标，使帕累托前沿更贴近实际制造需求。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Co_optimization_of_Design_and_Fabrication_Plans_for_Carpentry.pdf]]