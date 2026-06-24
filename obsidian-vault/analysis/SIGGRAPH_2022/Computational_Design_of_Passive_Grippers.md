---
title: Computational Design of Passive Grippers
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Computational_Design_of_Passive_Grippers.pdf
project_link: "https://homes.cs.washington.edu/~milink/passive-gripper/"
code_link: "http://github.com/stevengj/nlopt"
aliases:
- CDPG
tags:
- SIGGRAPH_2022
- topic/other_unclear
core_operator: 将抓取配置（GC）作为可优化的设计变量，并通过参数化骨架抽象实现插入轨迹与夹持器形状的联合优化。
primary_logic: (1) 稳定性完全由物体上的接触点集合（GC）决定，因此可以将 GC 显式作为优化变量；(2) 使用连接接触点与机器人法兰框架原点（FFO）的参数化骨架来抽象表示夹持器几何，可将原本高维的轨迹-形状联合搜索空间缩减到可处理的规模。
claims:
- 算法在所测试的全部 23 个对象上均能生成仿真可行的解决方案。
- 在真实物理抓取实验中，23 个对象中 21 个成功拾起，且 17 个对象具有 100%的成功率。
- 22 个对象（23 个实验）的测试集（包含标准 YCB 对象、工程模型和挑战对象） 上 物理抓取成功率 = 91.3%（21/23）
- 物体特征覆盖（Table 1） 上 可抓取物体类型数 = 内部抓取、对映抵抗、在质心外抓取（3 类）
---

# Computational Design of Passive Grippers

> [!tip] 核心洞察
> (1) 稳定性完全由物体上的接触点集合（GC）决定，因此可以将 GC 显式作为优化变量；(2) 使用连接接触点与机器人法兰框架原点（FFO）的参数化骨架来抽象表示夹持器几何，可将原本高维的轨迹-形状联合搜索空间缩减到可处理的规模。

| 字段 | 内容 |
|------|------|
| 中文题名 | 被动夹持器的计算设计 |
| 英文题名 | Computational Design of Passive Grippers |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://homes.cs.washington.edu/~milink/passive-gripper/) · [Project](https://libigl.github.io/) · [Code](http://github.com/stevengj/nlopt) · [arXiv](http://arxiv.org/abs/1905.10520) |
| Topic | #topic/other_unclear |
| Method | Computational Design of Passive Grippers |
| Dataset | 22 个对象（23 个实验）的测试集（包含标准 YCB 对象、工程模型和挑战对象）, 物体特征覆盖（Table 1） |

> [!tip] 效果简介
> - 22 个对象（23 个实验）的测试集（包含标准 YCB 对象、工程模型和挑战对象） 上，物理抓取成功率 91.3%（21/23） vs 无（尚无其他自动被动夹持器生成方法） (N/A)。
> - 物体特征覆盖（Table 1） 上，可抓取物体类型数 内部抓取、对映抵抗、在质心外抓取（3 类） vs 其他被动/主动夹持器通常最多覆盖 2 类 (扩展了 1–2 种类型)。

## 概要

**问题瓶颈**：被动夹持器无需外部能源即可拾取物体，但现有设计方法严重受限于可抓取物体的形状类型——非致动叉式夹持器只能内部抓取，旋转式被动夹持器仅能实现特定对映抓取，缺乏一种能够同时设计夹持器几何与插入轨迹的自动化方法。

**核心方法**：本文提出一种计算设计算法，将抓取配置（GC）显式作为可优化设计变量，通过参数化骨架抽象实现夹持器形状与插入轨迹的联合优化，最后在碰撞自由体积内进行拓扑优化生成可 3D 打印的实体夹持器。

**主要结果**：在包含 23 个对象（涵盖 YCB 标准物体、工程模型和挑战形状）的测试集上，算法为所有对象均找到仿真可行解；在真实物理实验中，21/23 个对象成功拾起（91.3%），其中 17 个对象达到 100% 抓取成功率。方法扩展了被动夹持器可抓取物体的类型范围，覆盖内部抓取、对映抵抗和质心外抓取三类。

**方法定位**：区别于先固定轨迹再设计几何或先设计几何再规划轨迹的传统范式，本工作以 GC 为枢纽，将夹持器设计转化为“接触点选择—轨迹与骨架联合优化—拓扑优化生成实体”的三阶段生成式流程，属于数据驱动的计算制造与机器人抓取交叉领域。

## 核心方法与创新机理

### 问题瓶颈与设计空间重构

被动夹持器（passive gripper）的核心挑战在于：它没有主动驱动源，完全依赖机器人臂的插入运动来建立并维持抓取。传统方法受限于手工设计或简单规则，只能处理少数特定形状——例如非致动叉式夹持器仅能抓取内部有腔体的物体，旋转式对映夹持器（Mucchiani et al., IEEE RA-L 2018/2021）则依赖物体外部的对映接触面。这些方法的根本局限在于**缺少一种自动化方法能够同时设计夹持器几何形状和插入轨迹以实现稳定抓取**。

本文的核心洞察将这一瓶颈解构为两个可操作的因果杠杆：

1. **稳定性完全由物体上的接触点集合（Grasp Configuration, GC）决定**——只要三个手指的接触点满足部分力封闭条件（partial force closure），抓取就是静态稳定的。因此，GC 可以显式地作为设计变量来优化，而非隐含在几何设计之后。
2. **插入轨迹与夹持器几何高度耦合**——轨迹决定了夹持器在插入过程中扫掠的空间，而夹持器几何又必须在碰撞自由空间内生成。直接在完整几何空间进行联合搜索的维度灾难使得问题不可解。本文提出用**参数化骨架（parametric skeleton）**将夹持器抽象为零厚度的三指结构，将搜索空间从高维几何-轨迹联合空间压缩到可处理的规模。

### Changed Slots：相对于现有范式的三个关键转变

**Slot 1：设计范式——从手工规则到数据驱动的生成式设计。** 现有被动夹持器依赖人工经验或简单几何规则（如“内部空腔可抓取”），泛化能力极弱。本文提出的算法以任意物体的三角网格和机器人运动学模型为输入，自动输出可 3D 打印的夹持器几何及对应的无碰撞插入轨迹。这一转变使被动夹持器从“针对特定形状定制”升级为“针对任意给定物体自动生成”。

**Slot 2：夹持器几何表示——从完整实体到零厚度骨架抽象。** 在轨迹搜索阶段，夹持器被表示为一个连接接触点与机器人法兰框架原点（Flange Frame Origin, FFO）的参数化骨架：三根手指，每根手指由 $m$ 个关节（实现中 $m=4$）组成，即 $\mathcal{G} \in \mathbb{R}^{3 \times m \times 3}$。这一抽象将几何设计变量从连续体/网格的无限自由度缩减为有限个关节坐标，同时保留了夹持器与物体、机器人之间碰撞检测所需的几何信息。最终实体形状仅在骨架和轨迹确定后，通过拓扑优化在碰撞自由体积内生成。

**Slot 3：轨迹与几何的关系——从序贯设计到联合优化。** 传统流程要么先固定轨迹再设计几何，要么先设计几何再规划轨迹，二者解耦导致可行解空间被不必要地收窄。本文在骨架层面执行**轨迹与夹持器形状的协同优化**：目标函数同时包含夹持器碰撞能量、轨迹碰撞能量、机器人碰撞能量和轨迹平滑正则项，优化变量同时涵盖所有手指的中间关节坐标和轨迹中间关键帧。这种联合搜索使得算法能够发现“先插入再旋转”等复杂运动策略所对应的夹持器几何。

### 三阶段管线与模块间因果关系

算法按因果依赖关系组织为三个顺序模块（Figure 2），前一模块的输出构成后一模块的输入约束：

![[assets/figures/papers/paper_list_l8_https_homes_cs_washington_edu_milink_passive_gripper/figures/002_Figure_2.jpg]]
*Figure 2: Steps of our algorithm: (a) Import the object’s shape from a user provided file; (b) Generate multiple promising GC candidates (where the blue cones point to contact points); (c) Optimize gripper shape and trajectory by using a skeleton (shown in red) as the simplified gripper model; (d) Generate the final gripper shape (shown in black) using topology optimization*

**模块一：GC 候选生成与排序（Section 4）。** 输入为物体网格，输出为一组按质量排序的 GC 候选列表。具体流程：
- **采样**：在物体表面上随机采样不接触地面的点，并过滤出可被 FFO 直接无碰撞访问的点；从合格点中均匀随机选取三点构成一个 GC。
- **静态稳定性过滤**：对每个候选 GC，验证其是否满足部分力封闭条件。使用 Coulomb 摩擦模型 $|\mathbf{f}_i^T| \leq \mu_i |\mathbf{f}_i^N|$，并将摩擦锥近似为多面体锥。被动抓取的特殊性在于：面向上的接触点无法提供支持力，因此摩擦系数按 $\mu_i = \max(0, \mathbf{n}_i \cdot \mathbf{g}) \mu$ 调整——法向与重力方向夹角大于 90° 时摩擦设为零。稳定性条件要求存在非负系数组合 $k_{ij}$ 使得接触力旋量恰好平衡重力旋量：
  $$\sum_{i}^{3} \sum_{j}^{q} k_{ij} \mathbf{w}_{ij} = [\mathbf{g}_{\alpha} \; \mathbf{0}]^T$$
- **可到达性过滤**：通过最小化一个惩罚违反脱开约束的损失函数来判断 GC 是否可到达。该损失函数寻找一个瞬时刚体运动 $(\mathbf{v}, \boldsymbol{\omega}, \mathbf{c})$，使得所有接触点能同时脱离物体表面：
  $$\min_{(\mathbf{v}, \boldsymbol{\omega}, \mathbf{c})} \sum_i \left[ [\cos(\theta_{\max}) - \mathbf{v}_i \cdot \mathbf{n}_i]_+ + [|\mathbf{v}_i| - 1]_+ \right]$$
  若损失收敛至零，则 GC 可到达。
- **Pareto 排序**：对通过过滤的 GC，基于两个指标进行非支配排序——部分最小扳手（partial minimum wrench，衡量抗扰动能力）和估计手指长度（影响结构刚度）。排序靠前的 GC 优先进入轨迹优化。

**模块二：轨迹与骨架联合优化（Section 5）。** 输入为选定 GC，输出为无碰撞插入轨迹 $\mathcal{T}$ 和对应的骨架几何 $\mathcal{G}$。轨迹表示为 $n$ 个关键帧（实现中 $n=4$），每个关键帧包含机器人末端执行器的 6 自由度位姿（$d=6$）。总优化变量维度为：
$$N := 3 \cdot (m-2) \cdot 3 + d \cdot (n-2)$$
即所有手指的中间关节坐标加上轨迹中间关键帧的自由度。

目标函数包含四项：
$$\min_{\mathbf{x}} \; E_g(\mathcal{G}, \mathcal{T}) + E_t(\mathcal{G}, \mathcal{T}) + \lambda_1 E_r(\mathcal{T}) + \lambda_2 L(\mathcal{T})$$
- **$E_g$（夹持器碰撞能量）**：沿轨迹的每个时刻，测量整个骨架与物体的最大碰撞深度。
- **$E_t$（轨迹碰撞能量）**：沿骨架的每个点，测量其在整个轨迹中与物体的最大碰撞深度。$E_g$ 与 $E_t$ 形成双向离散测量（Figure 4），确保骨架扫掠表面在时空两个方向上都无碰撞。
- **$E_r$（机器人碰撞能量）**：惩罚机器人与环境的碰撞。
- **$L(\mathcal{T})$**：轨迹复杂度的 L2 正则项，抑制不必要的大幅度运动。

![[assets/figures/papers/paper_list_l8_https_homes_cs_washington_edu_milink_passive_gripper/figures/005_Figure_4.jpg]]
*Figure 4: Our collision energy measures the collision of the surface swept by the skeleton over trajectory shown in pink. We compute collision using path intersections along two directions: In (a), the path along the skeleton is tested at different time steps in the trajectory (shown by vertical red lines); In (b), the path along the trajectory is tested at different points on the skeleton (shown by horizontal orange lines). Collisions by the paths are shown in blue. Maximum collision of the paths in (a) defines the gripper collision energy, and likewise maximum of those in (b) defines the trajectory collision energy. Note: a simple box and a linear path is used for simplicity of the visualization*

碰撞能量的计算引入了**内部距离（inside distance）**和**包裹距离（wrap-around distance）**两个启发式度量（Figure 5, 6），为优化器提供梯度信息：内部距离衡量骨架穿过物体内部的深度，包裹距离则通过计算骨架与物体表面交点对之间的测地线距离来评估“绕出”物体所需的路径长度。优化采用控制随机搜索（Controlled Random Search, CRS）算法，利用 NLopt 库实现。

![[assets/figures/papers/paper_list_l8_https_homes_cs_washington_edu_milink_passive_gripper/figures/006_Figure_5.jpg]]
*Figure 5: Illustrations of the inside distance (pink) and wrap-around distance (cyan) of the skeleton (red) through some objects. The path in (b) is closer to a collision-free state than that in (a), but the inside distance is the same. The path in (c) has lower inside distance than (a) and (b), but it needs more work to reach a collision-free state*

**模块三：拓扑优化生成最终夹持器（Section 6）。** 输入为模块二输出的轨迹和 GC，输出为可 3D 打印的实体夹持器几何。首先在机器人参考系中计算物体沿轨迹的扫掠体积（swept volume），其补集即为碰撞自由空间（Figure 7）。在该空间内执行离散拓扑优化，目标函数同时最小化结构柔度（compliance）和材料重量，生成平衡刚度与质量的最终夹持器形状。这一模块将抽象的骨架“实体化”，同时保证结构在承受抓取力时的力学性能。

### 模块间因果链

三个模块形成严格的因果依赖：模块一的 GC 质量直接决定模块二是否存在可行的轨迹解——若 GC 选择不当（如接触点位于狭缝深处），即使轨迹优化收敛也可能无可行解（Figure 11 的失败案例正是这一因果断裂的体现）。模块二的输出（轨迹 + GC）定义了模块三的碰撞自由空间边界——轨迹扫掠体积的补集越大，拓扑优化的设计自由度越高，越可能生成轻量且高刚度的夹持器。这种解耦设计（GC 选择与轨迹优化分离）是当前方法的已知局限：某些情况下算法自动找到的高排名 GC 无法获得可行轨迹，而手动指定的较低质量 GC 反而可行。

![[assets/figures/papers/paper_list_l8_https_homes_cs_washington_edu_milink_passive_gripper/figures/008_Figure_7.jpg]]
*Figure 7: In the robot’s reference frame, the swept volume of the bunny (shown in white) is the space occupied by the bunny throughout the trajectory. The complementary space is the collision-free space for topology optimization. The topology optimized gripper is shown in black*

## 实验与关键发现

### 评估对象集与实验设置

实验在包含 22 个对象（23 个实验）的数据集上进行，涵盖四类物体（Figure 8）：工程模型（A 类）、Stanford Bunny（B 类）、挑战模型（C 类）以及 YCB 标准数据集样本（D 类）。所有物理实验使用统一的 UR5 机器人臂与 3D 打印夹持器，物体初始位姿固定，抓取后均采用垂直抬起动作；每个对象重复测试 10 次以评估抓取可靠性。

![[assets/figures/papers/paper_list_l8_https_homes_cs_washington_edu_milink_passive_gripper/figures/009_Figure_8.jpg]]
*Figure 8: Evaluation set. A: engineered models; B: bunny; C: challenge models; D: samples from YCB dataset*

### 主结果：物理抓取成功率

Table 2 汇总了物理验证的核心结果：在 23 组实验中，**21 组成功拾起物体，整体成功率 91.3%**；其中 17 个对象的 10 次重复测试均达到 100% 成功率。这一结果直接支撑了方法的核心主张——算法能够在仿真和物理世界中为广泛形状的物体自动生成可行的被动夹持器设计与插入轨迹。

由于缺乏同类自动被动夹持器生成方法作为量化基线，实验的主要验证目标是真实物理可行性而非相对增益。Table 1 从能力覆盖维度提供了定性对比：本方法可处理**内部抓取、对映抵抗、在质心外抓取**三类抓取模式，而现有被动或主动夹持器通常最多覆盖其中两类。这一定性差异源于方法将抓取配置（GC）显式作为优化变量，从而扩展了可被动抓取的物体形状空间。

![[assets/figures/papers/paper_list_l8_https_homes_cs_washington_edu_milink_passive_gripper/figures/003_Table_1.jpg]]
*Table 1: Comparisons of different grippers on types of objects they are able to pick up*

### 抓取后稳定性评估

除拾取成功率外，Table 2 还报告了每个对象的抓取后稳定性指标——最大翻滚角（roll）与俯仰角（pitch），即物体在被正确装载后从夹持器中脱落前能承受的最大倾斜角度。Figure 10 以 Bunny 为例展示了测试设置。部分对象（A3、C1、C3、C4、C6、D7）表现出多种脱落模式，物体可能在多个不同姿态下找到额外的稳定区域，导致较大的标准差。这一现象提示基于随机采样的稳定性评估可能产生次优的鲁棒性估计。

### 消融分析：碰撞能量项的影响

在轨迹优化目标函数中，论文考察了移除部分能量项对收敛行为的影响。关键消融发现为：**当轨迹采样足够密集时，从目标函数中移除轨迹碰撞能量 $E_t$ 和包裹距离项可以改善优化收敛**。这一反直觉结果的原因在于，密集采样下轨迹碰撞能量引入的梯度信号可能过于嘈杂，反而干扰了基于控制随机搜索（CRS）的全局优化器的搜索效率。该消融直接指导了实际部署中的目标函数配置选择。

### 失败模式与适用边界

**虚拟-物理几何偏差导致失败**。两个对象（D4 和 C8）在物理实验中未能成功拾取，根本原因在于其 3D 虚拟模型与真实物体形状存在根本性差异——这是仿真到现实迁移中的经典问题，而非算法本身的失效。

**GC 与轨迹解耦优化的次优性**。Figure 11 揭示了一个结构性局限：当算法被限制仅能在物体内部选择接触点时，自动找到的 GC 候选均无法产生可行轨迹，因为 GC 排序阶段优先考虑稳定性而无法预知槽口形状对轨迹可行性的影响。然而，当手动指定一个合适的 GC 后，算法能够成功找到解决方案并在物理实验中达到 100% 可靠性。这一案例表明，GC 选择与轨迹优化的解耦处理在某些几何场景下会导致算法舍弃可行解，构成了方法的一个已知边界，并指向 GC 与轨迹完全联合优化的未来方向。

**抓取后运动假设的限制**。方法假设抓取后仅执行垂直抬起动作，因此无法处理无底面支撑的物体（如圆柱、圆锥），这些物体需要更复杂的抓取后运动（如旋转）才能实现稳定拾取。

**轨迹优化的局部极小问题**。基于 CRS 的全局优化虽然避免了梯度下降的局部极小，但仍可能在复杂几何场景中陷入次优解，导致算法放弃可行的 GC 或选择排名较低的 GC。

## 定位与知识库关联

### 1. 改变了什么 Slot：从“固定范式 + 分离设计”到“GC 驱动 + 联合设计”

本文的核心贡献在于改变了被动夹持器设计中的 **设计范式 slot** 与 **几何-轨迹关系 slot**。现有被动夹持器（如 **Non-Actuated Fork Lift** 仅能内部抓取；**Mucchiani et al.** 的旋转式对映抓取器，IEEE RA-L 2018/2021）均依赖手工设计的固定几何与预定义的简单插入路径，其可抓取物体类型受限于特定形状类别（Table 1 显示传统方法最多覆盖 2 类）。本文将这些 slot 从“手工规则驱动”改为“数据驱动的生成式设计”，核心机制是将 **抓取配置（GC）显式作为可优化设计变量**，并在参数化骨架层面实现夹持器形状与插入轨迹的联合优化。

这一改变的本质在于：传统方法中，稳定性是夹持器几何的“间接后果”，而本文将稳定性直接绑定到 GC 的接触点集合上（通过部分力封闭条件），使得几何与轨迹的搜索空间被压缩到可处理的规模。骨架抽象（三指，每指 4 关节，零厚度）是使联合优化可行的关键——它将原本高维的实体几何表示替换为 $3 \times m \times 3$ 的参数化骨架，从而在控制随机搜索（CRS）框架下实现 $N = 3 \cdot (m-2) \cdot 3 + d \cdot (n-2)$ 维变量的联合优化。

### 2. 知识库挂载点

本文可挂载到以下知识节点：

- **计算设计与 fabrication-aware optimization**：本文属于“为制造而优化”的典型工作，其从输入物体几何到可 3D 打印夹持器的端到端管线，可与 **topology optimization for additive manufacturing** 节点关联。具体而言，最终阶段的离散拓扑优化（在碰撞自由体积内最小化柔度与重量）直接继承自连续体拓扑优化框架，但本文的创新在于其设计域由前序联合优化自动生成（扫掠体积的补集），而非人工指定。

- **抓取规划与力封闭理论**：稳定性评估使用的 Coulomb 摩擦锥近似与部分力封闭条件（$\sum_i^3 \sum_j^q k_{ij} \mathbf{w}_{ij} = [\mathbf{g}_\alpha \ 0]^T$）直接建立在 **Kruger and van der Stappen (2011b)** 的抓取理论之上。被动抓取的特殊处理——面向上的接触点摩擦系数设为零（$\mu_i = \max(0, \mathbf{n}_i \cdot \mathbf{g})\mu$）——是对标准力封闭理论的针对性修改，可挂载到“被动抓取稳定性”子节点。

- **轨迹优化与碰撞检测**：双向离散碰撞能量测量（沿骨架方向与沿轨迹方向分别取最大碰撞值）以及包裹距离（wrap-around distance）作为启发式引导项，可挂载到 motion planning 中的碰撞避免方法节点。图 4 所示的双向测量机制是一种工程化的碰撞近似，而非精确连续碰撞检测。

### 3. 与已有方法的本质差异

与 **Antipodal grippers（主动或被动）** 相比，本文不要求接触点对映，从而扩展了可抓取物体类型（Table 1 显示本文覆盖内部抓取、对映抵抗、质心外抓取三类）。与 **带定制指端的主动对映夹持器** 相比，本文完全消除了对驱动机构的依赖，但代价是牺牲了抓取后主动调整的能力。与 **Vacuum-based active grippers** 相比，本文方法不依赖表面气密性，可处理多孔或非光滑表面，但无法处理无底面支撑的物体（如圆柱、圆锥，见 limitations）。

### 4. 适用边界与失效模式

本文方法的适用边界明确：**(1)** 假设抓取后仅垂直抬起，无法处理需要倾斜或旋转才能拾取的无底物体；**(2)** 稳定性评估依赖随机采样，可能产生次优鲁棒性；**(3)** GC 选择与轨迹优化被解耦处理，导致某些情况下算法自动找到的 GC 无法获得可行轨迹（Figure 11 实例：需手动指定 GC 才能成功）；**(4)** 虚拟模型与真实物体的几何偏差可导致物理抓取失败（D4、C8 两例失败）。

### 5. 后续工作启发

本文开辟了以下可跟进方向：**(1)** 将 GC 选择与轨迹优化进行完全联合优化，避免解耦带来的次优解——这是当前管线中最明显的结构瓶颈；**(2)** 引入数据驱动的稳定性评估替代随机采样，提升鲁棒性；**(3)** 扩展方法以支持复杂的抓取后运动（如旋转插入），从而覆盖无底物体；**(4)** 将该设计框架推广至多个物体或物体类别，实现通用被动夹持器的自动生成。这些方向的核心挑战在于如何在保持计算可处理性的前提下，进一步扩大搜索空间和设计自由度。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Computational_Design_of_Passive_Grippers.pdf]]