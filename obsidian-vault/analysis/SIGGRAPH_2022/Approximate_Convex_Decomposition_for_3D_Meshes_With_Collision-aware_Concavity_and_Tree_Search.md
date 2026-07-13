---
title: Approximate Convex Decomposition for 3D Meshes With Collision-aware Concavity and Tree Search
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Approximate_Convex_Decomposition_for_3D_Meshes_With_Collision_aware_Concavity_and_Tree_Search.pdf
project_link: null
code_link: "https://github.com/SarahWeiii/CoACD"
aliases:
- ACD3MCACTS
tags:
- SIGGRAPH_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 碰撞感知凹度度量（结合边界和内部距离）与多步树搜索策略
primary_logic: 通过同时从边界和内部两个角度以Hausdorff距离衡量形状与凸包的差异，并利用蒙特卡洛树搜索进行多步前瞻规划，可以在更少凸组件的情况下实现更保真、更合理的近似凸分解，同时保持碰撞条件。
claims:
- 在PartNet-Mobility数据集上，CoACD将平均组件数量从HACD的33.5减少至7.3，且凹度分数更优。
- 在OpenCabinetDrawer机器人任务中，使用CoACD分解的碰撞形状成功率达80%，而V-HACD仅为49%。
- 定性比较显示CoACD能够保留烤面包机插槽、水壶嘴、剪刀内环等精细结构，而基线方法填充了这些区域。
- V-HACD dataset 上 avg number of components (vs HACD) = 29.6
---

# Approximate Convex Decomposition for 3D Meshes With Collision-aware Concavity and Tree Search

> [!tip] 核心洞察
> 通过同时从边界和内部两个角度以Hausdorff距离衡量形状与凸包的差异，并利用蒙特卡洛树搜索进行多步前瞻规划，可以在更少凸组件的情况下实现更保真、更合理的近似凸分解，同时保持碰撞条件。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于碰撞感知凹度与树搜索的三维网格近似凸分解 |
| 英文题名 | Approximate Convex Decomposition for 3D Meshes With Collision-aware Concavity and Tree Search |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://arxiv.org/abs/2205.02961v1) · [Code](https://github.com/SarahWeiii/CoACD) · [paper](https://arxiv.org/abs/2205.02961v1") |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | CoACD |
| Dataset | V-HACD dataset, PartNet-Mobility, OpenCabinetDrawer |

> [!tip] 效果简介
> - V-HACD dataset 上，avg number of components (vs HACD) 29.6 vs 57.6 (HACD) (-48.6%)；concavity score (matched # components vs Animation) 0.049 vs 0.069 (Animation) (-29.0%)。
> - PartNet-Mobility 上，avg number of components (vs HACD) 7.3 vs 33.5 (HACD) (-78.2%)；avg number of components (vs V-HACD) 20.1 vs 44.6 (V-HACD) (-54.9%)。
> - OpenCabinetDrawer (robot simulation) 上，success rate 80% vs 49% (V-HACD as collision shapes) (+31%)。

## 概要

现有近似凸分解（ACD）方法在凹度度量、组件表示和搜索策略上存在根本缺陷：仅依赖边界距离（HACD）会填充内部空洞，仅依赖体积差（V-HACD）则可能填补薄壁结构，且一步贪婪搜索易陷入局部最优，导致无法保留手柄、插槽等精细功能结构，同时产生大量冗余组件。本文提出 **CoACD**，核心包含三项创新：**碰撞感知凹度度量**，同时从边界和内部以 Hausdorff 距离衡量形状与凸包的差异，全面捕捉各类近似误差；**直接平面切割流形网格**，生成平坦组件边界且避免凸包相交；**蒙特卡洛树搜索（MCTS）**进行多步前瞻规划，替代传统贪婪策略以寻找全局更优解。在 V-HACD 数据集上，CoACD 的平均组件数较 HACD 减少 48.6%（29.6 vs 57.6），凹度分数较 Animation-guided ACD 降低 29.0%；在 PartNet-Mobility 上，组件数较 HACD 从 33.5 锐减至 7.3。下游机器人开门任务中，使用 CoACD 分解作为碰撞形状的成功率达 80%，远超 V-HACD 的 49%。方法定位于以度量-表示-搜索三槽协同改进，替代传统 ACD 流水线的核心模块。

## 核心方法与创新机理

### 问题瓶颈与核心洞察

现有近似凸分解（ACD）方法存在三个系统性缺陷，导致无法在保持碰撞条件的前提下以少量凸组件精确逼近输入形状的精细结构。**HACD**（Mamou and Ghorbel 2009）仅依赖边界距离度量凹度，对中空结构不敏感，会填充手柄、插槽等内部空洞（图3）；**V-HACD**（Mamou et al. 2016）仅使用体积差度量，会填补薄平面结构（图4）。更深层的问题在于：这两类方法将组件表示为三角面片分组或体素，导致组件边界呈锯齿状且凸包间存在相交（图6-7）；同时它们采用一步贪婪搜索，仅优化当前切割的局部收益，无法规划多步后的全局最优解（图9-10）。

CoACD的核心洞察是：**凹度必须同时从边界和内部两个角度以Hausdorff距离衡量形状与凸包的差异**，并通过**蒙特卡洛树搜索（MCTS）进行多步前瞻规划**，才能在更少凸组件下实现更保真的分解。这一设计直接对应三个changed slots：凹度度量、组件表示与切割方式、搜索策略。

### 方法框架与模块顺序

CoACD采用递归分治策略（Algorithm 1），整体流程由六个模块串联构成：

1. **递归分解主循环**：维护一个待处理队列，初始包含整个输入网格。每次从队列取出一个组件，计算其凹度；若凹度超过用户设定的阈值$\tau$，则调用切割模块将其一分为二，并将两个子组件重新入队；否则将该组件加入结果集。循环直至队列为空。
2. **碰撞感知凹度计算**：对当前组件$S$，采样边界点云和内部点云，分别计算与凸包$\mathrm{CH}(S)$的Hausdorff距离，取最大值作为凹度。为加速内部距离计算，引入体积替代项$R_v(S)$。
3. **MCTS搜索**：对每个待切割组件构建搜索树，通过UCB选择、扩展、模拟和回溯，确定最优切割平面序列。
4. **平面细化**：对MCTS输出的第一切割平面进行局部三元搜索微调。
5. **网格平面切割**：使用细化后的3D平面直接切割流形网格，生成两个具有平坦边界的新网格组件。
6. **后处理合并**：遍历所有相邻组件对，若合并后的凹度仍在阈值内则合并，以消除冗余分割。

### Changed Slot 1：碰撞感知凹度度量

**基线缺陷**：HACD的边界距离法仅考察$\partial S$与$\partial\mathrm{CH}(S)$的距离，对内部空洞完全失明；V-HACD的体积差法对薄壁结构的相对体积误差不敏感。

**提出方案**：定义碰撞感知凹度为边界Hausdorff距离与内部Hausdorff距离的最大值：

$$\mathrm{Concavity}(S) = \max(\mathrm{H}_{\mathrm{b}}(S), \mathrm{H}_{\mathrm{i}}(S))$$

其中边界Hausdorff距离衡量形状表面与凸包表面的差异：
$$\mathrm{H}_{\mathrm{b}}(S) = \mathrm{H}(\mathrm{Sample}(\partial S), \mathrm{Sample}(\partial\mathrm{CH}(S)))$$

内部Hausdorff距离衡量形状内部与凸包内部的差异：
$$\mathrm{H}_{\mathrm{i}}(S) = \mathrm{H}(\mathrm{Sample}(\mathrm{Int}S), \mathrm{Sample}(\mathrm{Int}\mathrm{CH}(S)))$$

Hausdorff距离定义为两点集之间的最大最小距离：
$$\mathrm{H}(A, B) = \max\{\sup_{a \in A} d(a, B), \sup_{b \in B} d(b, A)\}$$

**因果机制**：取max操作确保只要边界或内部任一方面存在显著偏差，凹度就会升高，迫使算法在该区域进行切割。这直接解决了单独使用边界度量（遗漏内部空洞）或体积度量（遗漏薄结构）的盲区。图2通过球壳与深孔球体两个案例说明了$H_i$和$H_b$的互补必要性。

**计算加速**：精确计算$H_i(S)$需要在形状内部大量采样并做最近邻查询，开销极大。CoACD引入体积替代半径$R_v(S)$，将体积差映射为等价球体半径：
$$\mathrm{R_v}(S) = \sqrt{\frac{3\sqrt{3(\mathrm{Vol}(\mathrm{CH}(S)) - \mathrm{Vol}(S))}}{4\pi}}$$

近似凹度定义为：
$$\widetilde{\mathrm{Concavity}}(S) = \max(\mathrm{H}_{\mathrm{b}}(S), k\mathrm{R_v}(S))$$

其中系数$k<1$（默认0.3）用于缩放体积替代项，使其在内部误差较小时不主导凹度计算，但仍能在内部误差过大时触发切割。消融实验（补充材料Section E）验证该近似在超过94%的形状上与实际$\max(H_b, H_i)$的绝对误差≤0.02或比值在[0.8, 1.2]内。

### Changed Slot 2：网格平面切割与组件表示

**基线缺陷**：HACD将三角面片分组为组件，导致组件边界呈锯齿状（图6），且各组件的凸包之间存在相交，破坏碰撞条件。V-HACD使用体素化表示，引入离散化误差——即使输入形状本身已是凸的，体素化后的体积差也可能使算法误判为非凸（图7）。

**提出方案**：CoACD直接使用3D平面对流形网格进行切割，生成具有平坦边界的新网格组件。切割操作的关键设计包括：
- 使用精确的平面-三角形求交，沿切割平面将网格一分为二
- 对切割产生的开放边界进行三角化填充，确保子组件仍为封闭流形
- 实现了比CGAL快100倍的轻量级切割函数

**因果机制**：平坦边界确保相邻组件的凸包在切割面处完美贴合，消除相交和间隙，从而在物理仿真中保持碰撞条件的正确性。同时，直接操作网格避免了体素化的离散误差和三角面片分组的锯齿边界。

### Changed Slot 3：蒙特卡洛树搜索

**基线缺陷**：HACD和V-HACD均采用一步贪婪策略——在每个递归步骤中，枚举候选切割平面，选择使当前凹度降低最多的平面立即切割。这种短视策略在图9的“无顶底立方体”案例中完全失效：所有候选切割平面的一步收益相同（都只切断一个面），贪婪搜索无法区分优劣，而多步搜索通过模拟后续切割发现，先水平切割再垂直切割能以恰好4个组件完美分解。

**提出方案**：将切割平面选择建模为序贯决策问题，用MCTS进行多步前瞻搜索。对每个待切割组件构建一棵搜索树：

- **节点**：表示当前组件的切割状态
- **边**：表示一个候选切割平面
- **选择**：从根节点出发，使用UCB公式选择子节点：
  $$\mathrm{Q}(n) + c\sqrt{\frac{2\ln\mathrm{N}(n')}{\mathrm{N}(n)}}$$
  其中$Q(n)$为节点$n$的累积质量分数，$N(n)$为访问次数，$c$为探索参数
- **扩展**：到达叶节点后，随机采样一个未尝试的切割平面，生成新的子节点
- **模拟**：从新节点开始执行随机切割策略直至达到最大深度$d$，计算切割平面序列的质量分数：
  $$\operatorname{Quality}(\{\mathcal{P}_1, \cdots, \mathcal{P}_d\}) = \frac{1}{d}\sum_{i=1}^{d} -\max_{j=1}^{i+1}\operatorname{Concavity}(c_{ij})$$
  该分数取每步后最大组件凹度的负平均，鼓励快速降低最大凹度
- **回溯**：将模拟结果沿路径向上传播，更新各节点的$Q$和$N$值

搜索完成后，选择根节点下访问次数最多的子节点对应的切割平面作为第一切割平面，并通过三元搜索在局部微调平面位置和方向。

**因果机制**：MCTS通过模拟多步未来的切割序列来评估当前候选平面的长期价值，突破了贪婪搜索的局部最优陷阱。消融实验（表2）显示，多步MCTS相比一步贪婪基线将平均组件数从49.9降至34.4（V-HACD数据集），且运行时间反而从271.7s降至229.8s——这是因为更好的切割决策减少了后续递归的深度和广度。探索参数$c$的自适应设置$c=\mathrm{Concavity}(S)/d$能在开发与探索间取得平衡（图20）：$c=0$时退化为贪婪搜索，组件数增加；$c$过大则导致低效探测。

### 切割方向与候选平面

CoACD的候选切割平面从轴对齐方向或PCA主轴方向采样。对每个方向，在组件包围盒范围内均匀采样多个平面位置。消融研究（图15）表明PCA主轴通常优于随机轴对齐方向，因为PCA方向与形状的主要延展方向对齐，能产生更自然的切割。增加候选平面数量可减少最终组件数，但边际收益递减（图13b）。

### 后处理合并

递归分解可能产生冗余组件——某些相邻组件合并后凹度仍在阈值内。后处理步骤遍历所有相邻组件对，贪婪合并满足条件的对，进一步压缩组件数量。该步骤在凹度阈值较小时尤为有效（图13a）。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2205_02961v1_repair/figures/011_Figure_9.jpg]]
*Figure 9: Comparison between one-step greedy and multi-step search. (a) Input shape (a cube without top and bottom). (b) The one-step greedy algorithm fails to find the proper first cutting plane, since all candidate cutting planes lead to the same cost (Equation 7) as illustrated by the blue arrows (Hb). (c) The multi-step search algorithm can instead find the proper first cutting plane by simulating and searching future cuttings, which leads to the globally optimal solution (decomposed into exactly four pieces)*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2205_02961v1_repair/figures/006_Figure_6.jpg]]
*Figure 6: An example of triangle-grouping-based methods (from HACD). From left to right: (a) Input triangle mesh. (b) Grouping results of the triangle faces, where each color indicates a component. There are zig-zag boundaries between different components. (c) Corresponding convex hulls of each component, and they intersect with each other*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2205_02961v1_repair/figures/023_Figure_18.jpg]]
*Figure 18: Illustration of the interval space. Blue lines indicate the solid shape*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2205_02961v1_repair/figures/025_Figure_19.jpg]]
*Figure 19: (a) An example that the maximum inscribed sphere Φ is bounded by the boundary surface of CH(S) and Hi (S) does not equal to the radius ?? . (b) Illustration of the proof in Case 4.2*

## 实验与关键发现

CoACD 在 V-HACD 数据集、PartNet-Mobility 数据集和机器人操作下游任务上进行了系统评估，与 HACD、V-HACD 和 Animation-guided ACD 三个基线方法进行全面对比。评估维度涵盖组件数量、凹度分数、运行效率和下游任务成功率。

### 主定量结果

**V-HACD 数据集。** 在 V-HACD 基准数据集上，CoACD 平均生成 29.6 个凸组件，而 HACD 需要 57.6 个，组件数量减少 48.6%（Table 1）。在凹度分数对比中，将 Animation-guided ACD 方法生成的组件数量控制为与 CoACD 相同以进行公平比较，CoACD 的凹度分数为 0.049，Animation 方法为 0.069，降低 29.0%。这意味着在相同组件数量约束下，CoACD 的近似精度更高。

**PartNet-Mobility 数据集。** 该数据集包含具有复杂内部结构和精细功能部件的日常物品模型（如剪刀、烤面包机、水壶等），是验证碰撞感知凹度优势的关键场景。CoACD 平均生成 7.3 个组件，而 HACD 为 33.5 个（减少 78.2%），V-HACD 为 44.6 个（减少 54.9%）（Table 4）。CoACD 在 100% 的测试案例上组件数量均少于 HACD，在 90.2% 的案例上少于 V-HACD。这一显著差距直接源于碰撞感知凹度度量对内部空洞和薄壁结构的敏感性——HACD 仅依赖边界距离，倾向于填充内部空洞；V-HACD 依赖体积差，对薄平面结构的体积误差不敏感，同样会填补关键功能区域（如烤面包机插槽、水壶嘴）。

**机器人操作任务。** 在 OpenCabinetDrawer 任务中，使用 CoACD 分解结果作为碰撞形状训练强化学习代理打开抽屉，成功率达 80%，而使用 V-HACD 分解结果的成功率仅为 49%（Table 3）。性能差异的核心原因在于：V-HACD 的体素化过程会填充抽屉手柄的孔洞，导致碰撞形状无法准确表示可抓取区域；CoACD 通过碰撞感知凹度保留手柄的精细几何结构，使物理仿真中的抓取操作成为可能。

### 消融实验

**多步树搜索 vs. 一步贪婪搜索。** 这是 CoACD 搜索策略的核心消融。在 V-HACD 数据集上，使用相同凹度度量，一步贪婪策略平均生成 49.9 个组件，而多步 MCTS 搜索仅需 34.4 个组件，减少 31.1%（Table 2）。值得注意的是，MCTS 搜索的运行时间反而更短（229.8s vs. 271.7s），因为更优的切割决策减少了后续需要处理的组件数量，抵消了搜索本身的额外开销。定性对比（Figure 12）显示，一步贪婪策略在多个案例上产生冗余切割，而多步搜索通过前瞻模拟找到了全局更优的切割序列。

**MCTS 探索参数 c。** 探索参数 c 控制 UCB 公式中开发与探索的平衡。当 c=0 时 MCTS 退化为贪婪搜索，组件数量明显增加；c 过大则导致低效的过度探索。实验表明自适应设置 $c = \text{Concavity}(S) / d$（其中 d 为形状包围盒对角线长度）能在不同形状上取得最佳平衡（Figure 20）。

**后处理合并。** 后处理合并步骤遍历相邻组件对，若合并后凹度仍在阈值内则合并。消融显示该步骤能有效减少冗余分割，尤其在凹度阈值较小时效果更为显著（Figure 13a）。

**候选切割平面数量。** 增加从每个轴对齐方向采样的候选平面数量可以减少最终组件数量，但边际收益递减；同时平面细化步骤的改进幅度随候选平面数增加而变小（Figure 13b）。

**近似凹度精度验证。** 近似凹度 $\widetilde{\text{Concavity}}(S) = \max(\mathrm{H_b}(S), k \mathrm{R_v}(S))$ 用体积替代项 $\mathrm{R_v}(S)$ 代替精确的内部 Hausdorff 距离 $\mathrm{H_i}(S)$。在超过 94% 的测试形状上，近似值与精确值 $\max(\mathrm{H_b}(S), \mathrm{H_i}(S))$ 的绝对误差 ≤0.02 或比值在 [0.8, 1.2] 内，验证了该近似策略的可靠性（补充材料 Section E）。

### 定性分析

Figure 11 展示了 PartNet-Mobility 数据集上的定性对比。CoACD 能够保留烤面包机的插槽、水壶的壶嘴、剪刀的内环等精细结构，而 HACD 和 V-HACD 在这些区域均出现填充或过度分割。Figure 9-10 进一步揭示了多步搜索相比一步贪婪搜索的关键优势：在一个无顶底立方体案例中，所有候选切割平面在一步贪婪框架下具有相同代价，导致算法无法做出有效决策；多步搜索通过模拟未来切割找到全局最优解，将形状精确分解为四个组件。

### 失败模式与适用边界

1. **切割方向限制。** 当前切割方向限定为轴对齐方向或 PCA 主轴，对于某些需要斜向切割才能获得最优分解的形状可能非最优（Figure 15 比较了随机轴与 PCA 主轴的差异）。
2. **凹度阈值需手动设置。** 凹度阈值 $\epsilon$ 是控制分解粒度的关键参数，需要用户根据应用场景手动调整，缺乏针对不同零件功能重要度的自适应机制。
3. **MCTS 搜索复杂度。** 虽然单次切割操作比 CGAL 快 100 倍，但 MCTS 搜索的迭代和模拟过程在大场景或极复杂模型上仍可能导致较长运行时间。
4. **输入假设。** 算法假设输入为封闭的 2-流形三角网格，对于非流形、非水密或带有自交的网格需要额外的预处理步骤。
5. **近似系数 k 的经验性。** 近似凹度中的系数 k 默认取 0.3，该值基于经验设定，在不同几何特征的应用中可能需要调整以获得最佳近似精度与计算效率的平衡。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2205_02961v1_repair/figures/002_Figure_2.jpg]]
*Figure 2: From left to right: a spherical shell with a small opening, a solid sphere with a deep hole, and a solid sphere indicating the convex hull of the left two shapes. Both Hi ( S) and Hb ( S) are necessary to measure the difference between a shape and its convex hull. In the blue example, Hi ( S) ≫ Hb ( S), while in the green example, Hb ( S) ≫ Hi ( S). The purple polygons surrounding the cross-sections indicate the boundary surface of the convex hull*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2205_02961v1_repair/figures/003_Figure_3.jpg]]
*Figure 3: Failure cases of the boundary-distance-based methods (from HACD [Mamou and Ghorbel 2009]). Focusing only on the boundary distance between the shape and its convex hull, HACD may fail to handle the hollow structures and fill the interior space*

## 定位与知识库关联

CoACD 的核心贡献在于对近似凸分解（Approximate Convex Decomposition, ACD）问题中三个关键设计槽位（slot）的系统性改进：**凹度度量**、**组件表示与切割方式**、以及**搜索策略**。理解其相对已有基线方法的本质差异，需要逐一审视这些槽位的变化。

### 改变的三个关键槽位

**槽位一：凹度度量 — 从“单视角”到“碰撞感知”**

传统 ACD 方法的凹度度量仅从单一视角衡量形状与其凸包的差异。**HACD**（Mamou and Ghorbel, 2009）仅依赖边界距离，导致其对内部空洞结构不敏感，常将空心区域错误填充（见 Figure 3）。**V-HACD**（Mamou et al., 2016）转而使用体积差度量，但在处理薄平面结构时，由于相对体积误差不大，仍会填充孔洞或插槽（见 Figure 4）。**Animation-guided ACD**（Thul et al., 2018）虽然引入了体素化的凹度度量，但受限于离散化误差。

CoACD 将凹度重新定义为边界 Hausdorff 距离 $H_b(S)$ 与内部 Hausdorff 距离 $H_i(S)$ 的最大值：
$$\mathrm{Concavity}(S) = \max(H_b(S), H_i(S))$$

这一“碰撞感知”设计的关键洞察在于：**任何导致凸包侵占原始形状内部空间的近似误差，都必然在边界或内部距离上有所体现**（见 Figure 2 的球壳与深孔示例）。为了加速计算，CoACD 进一步用体积替代半径 $R_v(S)$ 乘以经验系数 $k$ 替代昂贵的内部采样，得到近似凹度 $\widetilde{\mathrm{Concavity}}(S) = \max(H_b(S), k R_v(S))$。补充材料验证该近似在超过 94% 的形状上保持良好保真度（绝对误差 ≤ 0.02 或比值在 [0.8, 1.2] 内）。

**槽位二：组件表示与切割方式 — 从“面片分组/体素化”到“平面直接切割流形网格”**

HACD 采用三角面片分组的方式生成组件，导致组件边界呈锯齿状，且各组件的凸包之间可能产生相交（见 Figure 6）。V-HACD 和 Animation-guided ACD 依赖体素化表示，引入了离散化误差，甚至可能将本已凸的形状误判为非凸（见 Figure 7）。这些表示层面的缺陷直接损害了分解的几何保真度和碰撞检测的可靠性。

CoACD 直接使用 3D 平面对封闭的 2-流形三角网格进行切割，生成具有平坦边界的子网格。这一设计带来了三重收益：(1) 组件边界平坦，避免锯齿；(2) 凸包之间无相交，保证碰撞条件的正确性；(3) 切割实现比 CGAL 快约 100 倍。该槽位的改变是 CoACD 在下游机器人任务中取得成功的基础——只有平坦且无相交的凸包才能作为可靠的碰撞形状。

**槽位三：搜索策略 — 从“一步贪婪”到“蒙特卡洛树搜索多步前瞻”**

HACD 和 V-HACD 均采用一步贪婪策略：在每一步递归中仅选择使当前凹度下降最大的切割平面。这种短视策略容易陷入局部最优，尤其当多个候选切割平面的即时收益相同时，贪婪搜索无法区分（见 Figure 9 的无顶底立方体示例）。此外，贪婪搜索常产生冗余组件（见 Figure 10）。

CoACD 引入蒙特卡洛树搜索（MCTS）进行多步前瞻规划。对每个待切割组件，算法构建搜索树，通过 UCB 公式平衡探索与利用，模拟未来若干步切割，以切割平面质量分数 $\operatorname{Quality}(\{\mathcal{P}_1, \cdots, \mathcal{P}_d\}) = \frac{1}{d} \sum_{i=1}^{d} - \max_{j=1}^{i+1} \operatorname{Concavity}(c_{ij})$ 评估路径优劣。这一设计使算法能够发现需要多步协调才能达成的全局更优解，同时消除了对辅助启发式项的依赖。消融实验（Table 2）证实：多步 MCTS 相比一步贪婪基线，平均组件数从 49.9 降至 34.4，且运行时间反而更短（229.8s vs 271.7s）——因为更优的早期切割减少了后续递归的深度和广度。

### 知识库挂载点

CoACD 可被定位为 **ACD 方法谱系中的“度量-表示-搜索”协同改进节点**。其上游连接包括：
- **Hausdorff 距离**在形状分析中的应用（如形状匹配、简化）；
- **Mamou 系列工作**（HACD 2009, V-HACD 2016）奠定的层次化近似凸分解框架；
- **蒙特卡洛树搜索**在组合优化中的成功应用（如 AlphaGo 系列）。

其下游可挂载的应用场景包括：
- **机器人抓取与操作**：CoACD 生成的凸包可直接作为物理仿真中的碰撞形状，在 OpenCabinetDrawer 任务中将成功率从 V-HACD 的 49% 提升至 80%（Table 3）；
- **实时碰撞检测**：更少且更精确的凸组件可加速 broad-phase 碰撞检测；
- **形状匹配与检索**：凸分解结果可作为形状描述符。

### 适用边界与限制

CoACD 的适用性受以下条件约束：
1. **输入必须为封闭的 2-流形三角网格**，非流形或非水密网格需要额外预处理。
2. **切割方向固定为轴对齐或 PCA 主轴**，对于某些具有倾斜特征的结构可能非最优（见 Figure 15 的对比）。
3. **凹度阈值 $\varepsilon$ 需用户手动设置**，缺乏针对不同零件功能重要性的自适应机制。
4. **近似凹度中的系数 $k$ 默认为 0.3**，在不同几何特征的应用中可能需要调整。
5. **MCTS 搜索复杂度**在大规模场景或极其复杂模型上仍可能成为瓶颈，尽管已比贪婪搜索更快。

### 后续工作启发

CoACD 打开的后续研究方向包括：
- **学习驱动的切割平面选择**：利用深度学习模型直接预测切割平面，以替代固定的轴对齐/PCA 方向，进一步提升效率与质量。
- **自适应凹度阈值**：根据零件的语义重要性或下游任务需求（如抓取点附近的保真度要求更高）自动调整阈值。
- **MCTS 的并行化**：探索更高效的并行搜索策略，利用多核/GPU 加速大规模分解。
- **动态形状扩展**：将碰撞感知凹度度量推广到时态变形网格的近似凸分解。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Approximate_Convex_Decomposition_for_3D_Meshes_With_Collision_aware_Concavity_and_Tree_Search.pdf]]