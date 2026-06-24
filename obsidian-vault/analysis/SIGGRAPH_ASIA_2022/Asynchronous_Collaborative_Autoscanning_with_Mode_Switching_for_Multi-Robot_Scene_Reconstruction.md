---
title: Asynchronous Collaborative Autoscanning with Mode Switching for Multi-Robot Scene Reconstruction
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/Asynchronous_Collaborative_Autoscanning_with_Mode_Switching_for_Multi_Robot_Scene_Reconstruction.pdf
project_link: "https://www.nokov.com/"
code_link: null
aliases:
- ACAMS
- ACAMSMRSR
tags:
- SIGGRAPH_ASIA_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入两种专用扫描模式（探索者模式用于快速扩大已知区域，重建者模式用于精细物体扫描）并进行动态模式切换；采用异步任务流模型，在任一机器人完成当前任务时立即触发全局任务生成与分配；通过改进的多仓库多旅行商问题（MDMTSP）优化任务分配以实现负载均衡与总行程最小化。
primary_logic: 不同扫描任务（探索 vs. 重建）需要不同的机器人运动与感知属性：探索需快速移动与远视野，重建需慢速移动与近视野。将任务分离并与机器人模式绑定，同时采用异步流式调度，可消除机器人空闲等待，在多机器人系统中同时提升探索效率与物体重建质量。
claims:
- 与 Dong et al. 2019 相比，本方法在物体完整性（O-Comp）上由 40.27 提升至 70.03，同时时间消耗更低（24.7 vs. 28.8）。
- 消融实验表明，同时保留探索者与重建者模式（完整方法）在所有指标上均优于单独移除任一模式的变体。
- 异步任务流模型显著减少机器人闲置时间，而无异步模型（NoFlow）存在大量黑色斜线区域表示的空闲等待。
- 本方法在不同初始位置下表现出鲁棒的重建质量与扫描效率，验证了算法对初始配置的不敏感性。
---

# Asynchronous Collaborative Autoscanning with Mode Switching for Multi-Robot Scene Reconstruction

> [!tip] 核心洞察
> 不同扫描任务（探索 vs. 重建）需要不同的机器人运动与感知属性：探索需快速移动与远视野，重建需慢速移动与近视野。将任务分离并与机器人模式绑定，同时采用异步流式调度，可消除机器人空闲等待，在多机器人系统中同时提升探索效率与物体重建质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 模式切换的异步协同自动扫描方法用于多机器人场景重建 |
| 英文题名 | Asynchronous Collaborative Autoscanning with Mode Switching for Multi-Robot Scene Reconstruction |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://arxiv.org/abs/2210.04413) · [Project](https://www.nokov.com/) · [arXiv](https://arxiv.org/abs/2210.04413") |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Asynchronous Collaborative Autoscanning with Mode Switching |
| Dataset | Front3D / MatterPort3D, Front3D |

> [!tip] 效果简介
> - Front3D / MatterPort3D (Large scene) 上，Object Completeness (O-Comp, %) 70.03 vs 40.27 (Dong et al. 2019) (+29.76)。
> - Front3D (Large scene) 上，Time Consumption (min) 24.7 vs 28.8 (Dong et al. 2019) (-4.1)。
> - Front3D (Small scene) 上，Time Consumption (min) 14.0 vs 27.8 (NBO×4 baseline) (-13.8)。

## 概要

现有面向室内场景的多机器人协同扫描方法采用同步间隔式任务分配，机器人必须等待所有同伴完成当前批次任务后方可获得新任务，导致大量空闲时间；同时缺少针对物体精细重建的专用扫描模式，难以兼顾探索效率与重建质量，物体表面常存在孔洞。本文提出一种**模式切换的异步协同自动扫描方法**（Asynchronous Collaborative Autoscanning with Mode Switching），核心思路是将扫描任务解耦为探索任务与物体重建任务，并为机器人定义两种专用扫描模式——**探索者模式**（快速移动、远视野）与**重建者模式**（慢速移动、近视野），机器人根据所分配任务类型动态切换模式。在调度层面，采用**异步任务流模型**：任一机器人完成当前任务序列即触发全局任务重新生成与分配，消除机器人间的空闲等待。任务分配被建模为改进的多仓库多旅行商问题（MDMTSP），引入模式一致性约束与负载均衡项，通过初始聚类、模拟退火与TSP求解的近似算法进行优化。实验表明，与**Dong et al. 2019**相比，本方法在物体完整性指标上从40.27提升至70.03，同时总时间消耗更低（24.7 vs. 28.8分钟）；消融实验验证了双模式设计与异步流调度各自的关键贡献。该方法定位为多机器人协同室内重建任务中，通过**模式解耦+异步调度**两个设计槽位实现效率与质量的双重提升。

## 核心方法与创新机理

### 问题瓶颈与核心洞察

现有多机器人协同场景重建方法（以 **Dong et al.**, TOG 2019 为代表）存在两个根本性瓶颈。其一，任务调度采用**同步间隔式**机制——控制中心必须等待所有机器人完成当前批次任务后，才统一生成并分配下一轮任务。这种“齐步走”策略导致先完成任务的大量空闲等待，系统整体时间利用率低下。其二，机器人采用**统一扫描模式**，未区分“探索未知区域”与“精细重建物体”这两种性质迥异的任务：前者要求机器人快速移动、具备远视野以尽快扩大已知区域；后者则要求机器人慢速移动、采用近视野以获取高密度点云覆盖物体表面。统一模式无法同时满足二者需求，导致物体表面存在大量孔洞，重建完整性不足。

本文的核心洞察在于：**将扫描任务按属性分离，并与机器人运动/感知模式显式绑定，同时以异步流式调度取代同步等待，可从根本上消除空闲时间并同时提升探索效率与重建质量**。基于这一洞察，方法设计了三个关键 changed slots：（1）探索者/重建者双扫描模式；（2）异步任务流调度机制；（3）引入模式一致性约束与负载均衡的改进 MDMTSP 任务分配。

### 系统框架与模块因果链

系统由四个核心模块构成，形成“任务生成→任务分配→任务执行→异步触发”的闭环流水线，如 Figure 2 所示。

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2210_04413/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our asynchronous collaborative autoscanning method. Once a robot finishes its current tasks, robot A in this case (a), new exploration tasks (red viewpoints) and reconstruction tasks (blue viewpoints) will be generated (b) and assigned to the robots by solving a modified Multi-Depot Multiple Traveling Salesman Problem (MDMTSP) (c). The control center will be activated again if any of the robots finishes the new tasks again, robot C in this case (d)*

**模块一：任务生成（Task Generation）**。基于当前重建状态，分别生成两类任务视点。探索任务视点（红色）源于 2D 占用栅格的前沿提取：通过 Canny 算法检测已知与未知区域的边界前沿点，经最远点采样获得均匀分布的前沿集合；对每个前沿生成候选视点，以“距最近机器人距离”和“距障碍物距离”定义有效性分数，贪心选择覆盖最多前沿的视点集（Figure 3）。重建任务视点（蓝色）源于 3D 点云的完整性分析：对语义分割后的物体点云，通过预测完整点云与当前重建点云的最近邻距离定义不完备度分数 $S_c(\mathbf{q}) = \min_{\mathbf{p} \in \mathcal{P}} \|\mathbf{q} - \mathbf{p}\|_2$（Eq. 1）；选择不完备度最高的点构建视锥，在可达范围内采样候选视点，以视锥内可见点的不完备度之和定义视野覆盖度，迭代选择覆盖度最高的视点并更新不完备度分数（Figure 4）。两类任务的视点属性直接决定了后续机器人模式：探索视点绑定探索者模式（快速、远视野），重建视点绑定重建者模式（慢速、近视野）。

**模块二：任务分配（Task Assignment）——改进的 MDMTSP 求解器**。将当前所有未分配任务与各机器人当前位置建模为加权完全图，目标是为每个机器人分配一条任务访问序列，最小化总行程代价并保持负载均衡。形式化目标函数为：

$$E_d = \sum_{r=1}^{R} \left( \sum_{T_k \in \mathcal{T}_r} d(T_k, T_{k+1}) \right)$$

$$E_c = \sum_{r=1}^{R} \left( (|\mathcal{T}_r| + |\mathcal{T}_r^{\text{rest}}| - C_r)^2 \right)$$

$$\mathcal{T}^* = \underset{\mathcal{T} = \{\mathcal{T}_r\}_{r=1}^R}{\arg\min} \; E_d + E_c$$

其中 $E_d$ 为所有机器人访问其任务序列的总路径长度（Eq. 2），$E_c$ 为负载均衡容量项，惩罚各机器人分配任务数与平均容量 $C_r$ 的偏差（Eq. 3）。关键创新在于引入**模式一致性约束**：

$$\prod_{T_k \in \mathcal{T}_r} \mathcal{I}(T_k) + \prod_{T_k \in \mathcal{T}_r} (1 - \mathcal{I}(T_k)) = 1$$

该约束强制每个机器人的任务序列中所有任务必须属于同一扫描模式（全为探索者或全为重建者），避免机器人在不同模式间频繁切换导致的运动属性冲突与效率损失。

由于该组合优化问题 NP-hard，方法设计了三阶段近似求解器（Algorithm 1）：（1）**扫描模式分配**：根据当前探索/重建任务比例与各机器人当前位置，决定各机器人本轮执行探索者还是重建者模式；（2）**初始聚类**：将同模式任务按空间位置聚类分配给各机器人；（3）**模拟退火优化**：以近似行程能量 $\dot{E}_d'$ 为目标，通过交换不同机器人簇间的任务来优化分配，同时满足行程能量约束——若某任务到机器人簇中心的距离超出阈值，则删除该任务及其后续任务，留待下一轮分配（Figure 5）；（4）**TSP 求解**：对每个机器人的任务簇内部，求解最优访问顺序。

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2210_04413/figures/005_Figure_5.jpg]]
*Figure 5: Illustration of traveling energy constraint. When assigned with a task that has a long traveling distance, e.g., the task 3 for robot A in this case, the scanning efficiency can be significantly reduced, thus all the subsequent tasks of task 3, including task 4, are deleted together for robot A, and it will wait for the task assignment in next iteration*

**模块三：任务执行（Task Execution）**。机器人按分配的任务序列依次移动至各视点，过程中根据任务类型自动切换扫描模式：探索任务下采用快速移动速度与远视野参数，重建任务下切换为慢速移动与近视野参数。扫描数据实时融合进全局三维重建，更新占用栅格与物体点云。

**模块四：异步调度模块（Asynchronous Task-Flow）**。这是消除空闲等待的核心机制。控制中心持续监控各机器人任务完成状态：**一旦任一机器人完成其当前所有任务，立即触发新一轮任务生成与分配**，新任务被追加到所有机器人（包括尚未完成当前任务的机器人）的任务队列末尾。这一“即完即分”的流水线模式（Figure 2(e)）与同步间隔式调度形成鲜明对比——后者在 Figure 9 的 NoFlow 消融实验中表现为大量黑色斜线区域（空闲等待），而完整方法中机器人几乎无空闲，模式切换（红色探索者/蓝色重建者）紧凑衔接。

### 因果机制总结

四个模块的因果链路为：**双模式任务生成**为不同类型任务绑定差异化的机器人运动/感知属性→**模式一致性约束的 MDMTSP** 在保证各机器人任务同质的前提下全局优化分配与路径→**异步任务流**在任一机器人完成当前任务时立即触发新一轮生成与分配，消除同步等待→**模式自动切换**使机器人在执行层面无缝适配任务需求。这一设计使得探索效率（快速扩大已知区域）与重建质量（慢速精细覆盖物体表面）在多机器人系统中首次实现协同提升，而非传统方法中的折中取舍。

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2210_04413/figures/003_Figure_3.jpg]]
*Figure 3: Exploration task generation with viewpoint selection on 2D occupancy grid. (a) A set of frontiers (red circles) are first selected to determine the corresponding candidate viewpoints, and the validity score of each candidate viewpoint is defined by measuring how close it is to the nearest robot (???? ) and how far from the nearest obstacle*

## 实验与关键发现

### 主要定量结果

#### 与 Dong et al. 2019 的对比

本方法在 Front3D 和 MatterPort3D 的大场景上与 **Dong et al. 2019**（同步间隔式多机器人重建系统）进行对比（Table 1）。核心指标为物体完整性（O-Comp）与时间消耗：

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2210_04413/figures/006_Table_1.jpg]]
*Table 1: Comparison with the work of [Dong et al. 2019] on reconstruction quality of objects, reconstruction efficiency, and load balance*

- **物体完整性（O-Comp）**：本方法达到 **70.03%**，相比 Dong et al. 的 40.27% 提升 **+29.76 个百分点**。这一差距揭示了单纯增加机器人数量而不改变扫描策略的瓶颈——同步间隔调度下机器人大量时间处于空闲等待，且统一扫描模式无法针对物体表面进行精细补全。
- **时间消耗**：本方法耗时 **24.7 分钟**，低于 Dong et al. 的 28.8 分钟（−4.1 分钟）。值得注意的是，本方法的总行程距离（848.5）略高于 Dong et al.（738.6），但时间反而更低，这直接验证了异步任务流模型的核心价值：以略高的行程代价换取机器人零空闲等待，最终实现更短的总时间。
- **负载均衡**：本方法任务分配的标准差更小，表明改进的 MDMTSP 中的负载均衡容量项有效避免了某些机器人过载而其他机器人闲置的情况。

从 Fig. 6 的中间重建结果可视化可见，Dong et al. 的方法在物体表面存在明显孔洞，而本方法在相同时间节点已获得更完整的物体表面。Fig. 7 的误差差异地图进一步显示，红色区域（Dong et al. 误差更高）集中在物体表面和复杂结构处，蓝色区域（两者相当）主要在平坦墙壁——说明本方法的重建者模式对物体精细重建起到了关键作用。

#### 与 NBO 基线的对比

与 **Liu et al. 2018** 的单机器人物体感知自动扫描方法（NBO）的对比在两种设置下进行（Table 2）：

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2210_04413/figures/009_Table_2.jpg]]
*Table 2: Comparison with the work of [Liu et al. 2018] used in two different settings on reconstruction quality of objects and reconstruction efficiency*

- **NBO×4（四机器人独立运行）**：在小场景中，本方法耗时 **14.0 分钟**，NBO×4 耗时 27.8 分钟（−13.8 分钟，节省近 50%）。NBO×4 因各机器人独立决策、无协同任务分配，导致大量重复扫描和路径冲突。Fig. 8 的路径可视化清晰展示了这一差异：NBO×4 的路径密集交叠，而本方法的路径分布均匀、覆盖高效。
- **NBO×1（单机器人）**：本方法在物体完整性上同样显著优于单机器人 NBO，验证了多机器人协同本身带来的覆盖优势。

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2210_04413/figures/010_Figure_8.jpg]]
*Figure 8: Visual comparison between the result obtained using baseline NBO × 4 with multiple isolated robots and ours. The traveling paths of different robots are shown with lines in different colors*

#### 真实机器人实验

在 Turtlebot3 上的真实场景实验（Fig. 12）验证了方法的实际可行性。由于真实机器人的视角控制自由度低于仿真环境，且存在传感器噪声，重建质量有所下降，但整体扫描流程和模式切换逻辑在真实世界中正常运行，未出现因通信延迟或运动误差导致的系统崩溃。

### 消融实验

Table 3 的消融实验解耦了各核心组件的贡献：

- **移除探索者模式（NoEx）**：仅保留重建者模式，机器人缺乏快速扩大已知区域的能力，导致探索效率骤降，时间消耗显著上升，且因场景覆盖不足，部分物体完全未被发现，O-Comp 大幅下降。
- **移除重建者模式（NoRe）**：仅保留探索者模式，机器人可快速覆盖场景，但缺乏对物体表面的近距精细扫描，O-Comp 和物体重建精度（O-RMS）均明显劣于完整方法。
- **同时保留两种模式（完整方法）**：在所有评估指标上均优于 NoEx 和 NoRe，证明两种扫描模式的互补性是系统性能的关键来源——探索者负责“找到物体”，重建者负责“扫好物体”。
- **移除异步任务流模型（NoFlow）**：恢复为同步间隔式调度。Fig. 9 的调度时序图直观展示了差异：NoFlow 中存在大量黑色斜线区域（机器人空闲等待），而完整方法的机器人几乎持续处于工作状态。NoFlow 的时间消耗显著增加，验证了异步调度对消除等待时间的决定性作用。
- **减少探索者机器人数量**：当探索者机器人数量减少时，探索效率下降导致总时间上升，但对 O-RMS 的影响相对复杂——因为重建者机器人的工作量未变，只是等待探索者提供新区域的时间变长。

### 鲁棒性分析

Fig. 11 展示了不同初始位置下的扫描结果。三台机器人从不同起始点出发，最终均完成了对整个场景的覆盖和物体重建，路径分布和重建质量保持稳定。这表明方法对初始配置不敏感，改进的 MDMTSP 任务分配能够自适应地调整各机器人的任务序列。

### 失败模式与适用边界

1. **MDMTSP 求解器的局部最优**：改进的 MDMTSP 采用初始聚类+模拟退火+TSP 的近似求解策略，在某些任务分布下会陷入局部最优，导致任务分配并非全局最优。这表现为个别机器人路径过长或任务量不均，降低了整体效率。论文未给出该问题的定量发生率，需要在实际部署中关注。
2. **单层场景限制**：系统的 2D 占用栅格仅能表示单层平面，无法处理多层建筑或复合结构（如楼梯、夹层）。这是 2D 前沿探索范式的固有局限。
3. **集中式架构的通信依赖**：所有任务生成与分配由中央控制中心完成，当场景过大导致通信中断时，机器人将失去任务更新能力，退化为无协同状态。
4. **路径规划未考虑机器人间避障**：任务分配仅优化行程距离和负载均衡，未建模机器人之间的物理遮挡与空间占用。在狭窄通道场景中，多机器人可能发生避障死锁，需依赖底层局部路径规划器处理，但该问题未在实验中测试。
5. **真实场景的性能退化**：真实机器人实验中，由于视角控制精度和传感器噪声，重建质量低于仿真。论文未提供真实场景的定量指标，该部分的结论强度较弱，需更多实验验证。

## 定位与知识库关联

本工作在多机器人场景重建的“任务调度—任务分解—任务分配”链条上同时改变了三个相互耦合的核心 slot，构成了区别于既有方法的结构性差异。

**改变的 Slot 一：扫描模式设计（任务分解方式）**。既有方法（包括 **Dong et al., TOG 2019** 的多机器人系统与 **Liu et al., TOG 2018** 的单机器人 NBO 方法）将扫描视为统一任务，机器人以同质化的运动速度与感知视野执行所有视点访问，未区分“扩大已知区域”与“精细重建物体”对机器人行为属性的不同需求。本工作将扫描任务显式分解为探索任务与重建任务，并为之定义两种专用扫描模式——探索者模式（快速移动、远视野）与重建者模式（慢速移动、近视野）。这一 slot 改变的本质是将“任务类型”与“机器人运动/感知属性”进行绑定，使机器人在执行不同子任务时自动切换行为模式，从而在同一个系统中兼顾探索效率与物体重建质量。

**改变的 Slot 二：任务调度机制（从同步间隔到异步流式）**。**Dong et al., TOG 2019** 采用同步间隔式调度：控制中心等待所有机器人完成当前批次任务后，才生成并分配下一轮任务。该设计导致先完成任务的机器人出现大量空闲等待时间，系统整体利用率低。本工作引入异步任务流模型：任一机器人完成其当前任务序列即触发控制中心立即生成新任务并分配给所有机器人，无需等待其他机器人。这一改变消除了机器人间的同步壁垒，将多机器人系统从“轮次式”推进转为“流水线式”持续扫描，是时间消耗显著降低（24.7 min vs. 28.8 min）的核心因果机制。消融实验中移除异步流模型（NoFlow）后，机器人的空闲时间（图 9 中黑色斜线区域）大幅增加，直接验证了这一 slot 的独立贡献。

**改变的 Slot 三：任务分配优化（改进的 MDMTSP 建模与求解）**。Dong et al. 虽也使用 MDMTSP 进行任务分配，但其建模未包含模式一致性约束与负载均衡容量项，且求解策略相对简化。本工作在 MDMTSP 目标函数中引入两项关键改进：(1) 模式一致性约束，强制每个机器人的任务序列内所有任务属于同一扫描模式（全为探索者或全为重建者），避免机器人在两种模式间频繁切换带来的效率损失；(2) 负载均衡容量项，惩罚各机器人分配任务数与平均任务数的偏差，防止部分机器人过载而其他机器人闲置。求解层面，采用“初始聚类 + 模拟退火优化簇分配 + TSP 求解访问顺序”的近似算法（Algorithm 1），在可接受的计算时间内获得高质量近似解。

**三个 Slot 的耦合关系**：模式设计（Slot 一）为任务分配（Slot 三）提供了模式一致性约束的必要性——若任务本身未绑定模式属性，则无需在分配中保证序列内模式一致性。异步调度（Slot 二）则为模式切换提供了时间维度的灵活性——机器人完成当前模式的任务序列后，可在下一轮分配中被赋予另一种模式的任务，实现动态模式切换。三者共同构成“分解—分配—调度”的闭环优化。

**知识库挂载点**：本工作可挂载于多机器人协同感知与任务规划知识库的以下节点：
- **多机器人任务分配**：改进的 MDMTSP 建模（模式一致性约束 + 负载均衡）是对经典多旅行商问题在机器人扫描场景下的定制化扩展，可作为该节点下的一个变体模型。
- **主动感知与下一最佳视点**：探索任务的视点生成基于 2D 占用栅格前沿（与经典 frontier-based exploration 一脉相承），重建任务的视点生成基于 3D 点云完整性分析（与基于信息增益的 NBV 方法相关），两者结合构成了“探索-重建”双目标视点规划的新范式。
- **多机器人调度架构**：异步任务流模型提供了一种集中式但事件驱动的调度范式，区别于传统的同步轮次调度与完全去中心化调度，可作为该节点下的一个中间方案。

**适用边界**：
1. **场景结构限制**：系统仅支持单层室内场景，2D 占用栅格无法表示多层或复合结构（如楼梯、跃层）。这是方法的一个硬性约束。
2. **通信架构限制**：仅适用于集中式架构，依赖控制中心与所有机器人的持续通信。当场景过大导致通信中断时，机器人可能失去控制，无法自主完成任务。
3. **路径规划的简化假设**：任务分配中的路径代价基于直线距离估计，未在规划中考虑机器人间的遮挡与物理空间占用。在狭窄通道等场景中，可能引发避障死锁或路径冲突。
4. **求解器的最优性**：改进的 MDMTSP 求解器基于模拟退火，有时会陷入局部最优，降低最终任务分配的效率。这是近似求解的固有 trade-off。

**后续启发**：
- 可探索将场景结构先验（如家具布局、房间功能语义）引入任务生成，驱动机器人优先探索高价值区域，进一步提升扫描效率。
- 任务视点的加权机制（如对复杂表面赋予更高权重）可进一步优化重建质量与扫描时间的 Pareto 前沿。
- 将方法拓展至多层/多楼层场景，并支持去中心化分布式工作模式，是提升系统实用性的重要方向。
- 异步任务流模型的思想可迁移至其他多智能体协同感知任务（如多无人机覆盖搜索、多机器人协同巡检），其“事件驱动 + 全局重分配”的调度范式具有通用性。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/Asynchronous_Collaborative_Autoscanning_with_Mode_Switching_for_Multi_Robot_Scene_Reconstruction.pdf]]