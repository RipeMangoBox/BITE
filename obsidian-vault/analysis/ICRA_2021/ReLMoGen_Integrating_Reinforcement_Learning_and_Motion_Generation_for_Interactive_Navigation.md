---
title: "ReLMoGen: Integrating Reinforcement Learning and Motion Generation for Interactive Navigation"
type: paper
paper_level: A
venue: ICRA
year: 2021
pdf_ref: paperPDFs/ICRA_2021/ReLMoGen_Integrating_Reinforcement_Learning_and_Motion_Generation_for_Interactive_Navigation.pdf
code_link: null
project_link: https://svl.stanford.edu/projects/relmogen/
aliases:
- RRLMG
- ReLMoGen
tags:
- ICRA_2021
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "将动作空间从底层关节控制提升为运动生成器（MG）的子目标，使RL仅需学习“往哪里移动/交互”，而将“如何无碰撞地移动”交给经典的规划与控制方法。"
primary_logic: "通过整合经典运动生成与深度强化学习，形成分层控制器：高层学习子目标预测，底层利用基于采样的运动规划器（如RRT-Connect）生成安全轨迹。这一设计显著提升了探索效率、样本效率和训练速度，且学到的子目标策略对底层运动生成器的变化具有鲁棒性。"
claims:
- "ReLMoGen在所有七项移动操控任务中均取得了最高的任务完成度。"
- "ReLMoGen在探索时覆盖的物理空间远大于基线SAC，且能进行更多有意义的交互。"
- "训练时使用RRT-Connect的策略在测试时切换为Lazy PRM，性能几乎无下降，表明子目标策略对运动生成器变化具有鲁棒性。"
- "ReLMoGen所需的梯度更新步数比基线少一个数量级，平均训练速度提升约7倍。"
---

# ReLMoGen: Integrating Reinforcement Learning and Motion Generation for Interactive Navigation

> [!tip] 核心洞察
> 通过整合经典运动生成与深度强化学习，形成分层控制器：高层学习子目标预测，底层利用基于采样的运动规划器（如RRT-Connect）生成安全轨迹。这一设计显著提升了探索效率、样本效率和训练速度，且学到的子目标策略对底层运动生成器的变化具有鲁棒性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ReLMoGen：将运动生成融入强化学习的移动操控框架 |
| 英文题名 | ReLMoGen: Integrating Reinforcement Learning and Motion Generation for Interactive Navigation |
| 会议/期刊 | ICRA 2021 |
| Links | [paper](https://arxiv.org/abs/2008.07792) · [Project](http://svl.stanford.edu/projects/relmogen) · [Project](https://svl.stanford.edu/projects/relmogen/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | ReLMoGen (Reinforcement Learning + Motion Generation) |
| Dataset | PushDoorNav, ButtonDoorNav, InteractiveObstaclesNav, ArrangeKitchenMM |

> [!tip] 效果简介
> - PushDoorNav 上，Success Rate (SR) 为 0.97 (ReLMoGen-R, 均值)，对比 0.0 (SAC), 0.0 (OAC), 0.0 (HRL4IN)，变化 +0.97。
> - ButtonDoorNav 上，Success Rate (SR) 为 0.73 (ReLMoGen-R)，对比 0.01 (SAC), 0.01 (OAC), 0.0 (HRL4IN)，变化 +0.72。
> - InteractiveObstaclesNav 上，Success Rate (SR) 为 0.79 (ReLMoGen-R)，对比 0.51 (SAC), 0.01 (OAC), 0.0 (HRL4IN)，变化 +0.28。

## 概要

移动操控任务（导航+操作交替）因其长时间跨度、稀疏奖励和高维连续控制空间，对端到端强化学习构成了严重的探索瓶颈。**ReLMoGen** 的核心思路是将动作空间从底层关节速度提升为**运动生成器（Motion Generator, MG）的子目标**：高层策略仅需预测“往哪里移动/交互”，而将“如何无碰撞地安全执行”交由经典的采样规划与关节控制器完成。这一分层设计显著降低了探索难度，使策略能快速覆盖大范围物理空间并产生有意义的交互。

在七项涵盖导航、桌面操作、交互式导航和移动操作的仿真任务上，ReLMoGen 均取得了最高或与最优基线持平的任务完成度，且所需的梯度更新步数比基线少一个数量级，平均训练速度提升约 **7 倍**。更重要的是，训练时使用 RRT-Connect 的策略在测试时切换为 Lazy PRM 后性能几乎无下降，表明学到的子目标策略对底层运动生成器的变化具有鲁棒性。该方法仅依赖模拟传感器信号，未使用环境真值，为后续的 Sim2Real 迁移保留了可行性。



移动操控（Mobile Manipulation）要求机器人在大范围环境中完成导航、避障和物体交互等复合任务。这类任务通常由导航和操作两个子阶段交替构成，时间跨度长、奖励信号稀疏。若直接在关节空间输出速度或扭矩等底层控制量进行强化学习（RL），智能体面临严重的探索困难：高维连续动作空间中，随机探索几乎不可能偶然完成“导航至门前→推动门→穿过门”这类长序列行为，导致训练不稳定或收敛至次优策略。

现有端到端RL方法（如SAC、OAC）在关节空间操作，需要同时学习碰撞避免、精确控制和任务决策，样本效率极低。分层强化学习（HRL）虽然通过高层子目标与底层策略的分离提供了时间抽象，但其底层策略仍需从头学习控制技能，训练难度和样本消耗依然显著。因此，核心瓶颈在于：**如何在不牺牲探索效率的前提下，让RL策略聚焦于高层任务决策，而将底层安全运动执行交给可靠的非学习模块**。

ReLMoGen的动机正是基于这一观察：经典运动规划与控制方法（如基于采样的RRT-Connect规划器）已能在已知环境模型下高效、安全地生成无碰撞轨迹。将这些成熟能力作为“运动生成器”（Motion Generator, MG）嵌入RL环路，将动作空间从关节速度提升为运动生成器的子目标（如基座的2D目标位姿、臂部末端执行器的3D目标位置），可以使RL策略仅需学习“往哪里移动/交互”，而将“如何无碰撞地移动”完全外包给运动生成器。这一设计从根本上改变了探索的粒度——策略每一步跨越的不再是微小的关节增量，而是一段完整的无碰撞运动轨迹，从而显著提升探索效率、样本效率和训练速度。



## 核心方法与创新机理

### 问题瓶颈：移动操控中的探索困境

移动操控任务（如推门导航、桌面物品归位）由导航与操作交替的子阶段构成，任务时间长且奖励稀疏。若直接在关节空间（轮子与机械臂各关节的速度）上训练强化学习策略，智能体面临严重的探索困难：高维连续动作空间中，随机探索几乎不可能发现“先移动到门前，再推开门”这类长序列行为，导致训练不稳定或收敛至次优策略。实验表明，端到端基线 **SAC** 和 **OAC** 在多数任务上的成功率接近于零（Table I），验证了这一瓶颈。

### 核心洞察：动作空间的语义提升

ReLMoGen 的根本创新在于**将动作空间从底层关节控制提升为运动生成器（Motion Generator, MG）的子目标**。原 POMDP 的动作空间 $\mathcal{A}$ 是关节速度连续量，而提升后的动作空间 $\mathcal{A}'$ 变为：

- **基座子目标**：基座的 2D 位置（极坐标表示）与朝向变化；
- **臂部子目标**：末端执行器的 3D 位置（RGB-D 图像上的 $(u,v)$ 坐标加深度）及参数化推动动作。

这一设计使强化学习仅需学习“往哪里移动/交互”，而将“如何无碰撞地移动”交给经典的采样规划器（如 RRT-Connect）与关节控制器。由此，策略的探索粒度从毫秒级的关节控制跃升为秒级的子目标决策，显著降低了探索空间的有效维度。

### 分层架构：学习与规划的解耦

ReLMoGen 形成清晰的分层控制器：

1. **子目标生成策略（Subgoal Generation Policy, SGP）**：高层 RL 策略，根据 RGB-D、LiDAR 和任务信息（如目标位置）输出基座/臂部子目标及交互参数。提供两种参数化方式——SGP-D（离散密集 Q 值图，基于 DQN）和 SGP-R（连续回归，基于 SAC）。
2. **运动生成器（Motion Generator, MG）**：底层非抢占式子程序，接收子目标后，通过 RRT-Connect 等采样规划器搜索无碰撞轨迹，并由关节控制器执行。MG 分为基座运动生成器和臂部运动生成器，各自负责对应子目标的实现。

与分层强化学习基线 **HRL4IN** 的关键区别在于：HRL4IN 的底层策略需要从头学习控制，而 ReLMoGen 的底层是预定义的规划与控制方案。这避免了底层策略学习不充分导致的高层训练失败，使得子目标策略的训练更加稳定高效。

### 关键优势：探索效率与鲁棒性的飞跃

动作空间提升带来的优势在多维度得到验证：

- **探索效率**：在潜在状态空间中，SAC 只能遍历相邻状态，而 ReLMoGen-R 可以在由运动规划连接的距离较远的状态间跳跃（Figure 5a）；在物理空间中，ReLMoGen-R 覆盖的区域远大于 SAC，且能进行更多有意义的环境交互（Figure 5b-c）。
- **样本效率与训练速度**：ReLMoGen 所需的梯度更新步数比基线少一个数量级，平均训练速度提升约 7 倍。
- **对底层变化的鲁棒性**：训练时使用 RRT-Connect 的策略，在测试时切换为 Lazy PRM，任务成功率几乎无下降（Table II），表明学到的子目标策略不依赖于特定运动生成器的实现细节。



ReLMoGen 的核心设计是将经典运动生成（Motion Generation）作为不可抢占的子程序嵌入强化学习闭环，从而将原始 POMDP 中的底层关节控制问题提升为子目标预测问题。整个框架由两个关键模块串联构成：**子目标生成策略（Subgoal Generation Policy, SGP）** 与 **运动生成器（Motion Generator, MG）**。

### 模块关系与数据流

1. **观测输入**：在每个决策步，SGP 接收来自环境的观测 $o_t$，包括 RGB‑D 图像、LiDAR 扫描、基座里程计、关节状态以及任务相关目标信息（如目标物体位置或导航终点）。
2. **子目标生成策略（SGP）**：SGP 是一个由强化学习训练的策略网络，负责将高维观测映射为运动生成器可执行的子目标 $a'_t$。根据动作参数化方式的不同，论文提出了两种变体：
   - **SGP‑D（离散密集 Q 值图）**：在基座可达区域或桌面操作平面上生成密集的 Q 值分布，通过 argmax 选取最优子目标位置。
   - **SGP‑R（连续回归）**：直接回归连续的子目标参数，包括基座在极坐标下的 2D 目标位置与朝向变化、臂部末端执行器的 3D 目标位置（以深度图像上的 $(u, v)$ 坐标及深度值表示），以及一个二值阶段指示器用于在导航阶段与交互阶段之间切换。
3. **运动生成器（MG）**：接收 SGP 输出的子目标 $a'_t$ 后，MG 调用基于采样的运动规划器（训练时默认使用 RRT‑Connect）在从传感器实时构建的局部环境模型中搜索无碰撞轨迹，并由底层关节控制器以闭环方式执行，输出一段变长的底层动作序列 $\{a_t, a_{t+1}, \dots, a_{t+T-1}\}$。MG 分为基座运动生成器和臂部运动生成器，分别处理导航子目标和操作子目标。
4. **奖励与状态转移**：子目标 $a'_t$ 执行期间累积的原始奖励构成提升后的奖励 $\mathcal{R}'(s_t, a'_t) = \sum_{k=t}^{t+T-1} \mathcal{R}(\bar{s}_k, a_k)$，环境状态则经历多步转移后进入 $s_{t+T}$。SGP 基于此提升后的 POMDP $(\mathcal{S}, \mathcal{A}', \mathcal{O}, \mathcal{T}', \mathcal{R}', \gamma)$ 进行策略优化。

### 设计逻辑

这一分层架构将“往哪里移动/交互”的决策与“如何安全到达”的执行解耦：RL 只需在子目标空间中进行探索和信用分配，而碰撞避免、运动学约束满足等底层问题由成熟的规划与控制方法处理。由此带来的因果效应是：
- **探索效率跃升**：子目标空间远小于原始关节动作空间，且 MG 保证了每次子目标执行的有意义位移，避免了端到端 RL 在关节空间中漫无目的的随机抖动（Figure 5 显示 ReLMoGen‑R 的物理空间覆盖和有效环境交互次数远超 SAC）。
- **样本效率与训练速度**：ReLMoGen 所需的梯度更新步数比基线少一个数量级，平均训练壁钟时间快约 7 倍。
- **对底层实现的鲁棒性**：训练时使用 RRT‑Connect 的 SGP，在测试时切换为 Lazy PRM，任务成功率几乎无下降（Table II），表明子目标策略学到的是与具体运动生成器解耦的语义级行为。

### 需要手动验证的细节

论文明确提到当前仅实现了参数化“推动”交互，框架虽支持扩展到抓取、拉拽等其他原语，但尚未给出实现与验证。此外，运动生成器依赖实时传感器数据构建局部模型，在真实机器人部署中感知噪声和动力学差异的影响未经验证，相关结论均基于仿真环境。

### 补充图表

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2008_07792/figures/002_Figure_2.jpg]]
*Figure 2: Two types of action parameterization of ReLMoGen and network architecture of SGP-D and SGP-R. (b) TabletopReachM (c) Push/ButtonDoorNav*



### 1. 问题形式化：基础POMDP与提升后的动作空间

ReLMoGen 将视觉-运动移动操控任务建模为离散时间部分可观马尔可夫决策过程（POMDP）。基础POMDP定义为六元组：

$$(S, \mathcal{A}, \mathcal{O}, \mathcal{T}, \mathcal{R}, \gamma)$$

其中 $S$ 为状态空间，$\mathcal{A}$ 为底层动作空间（如关节速度），$\mathcal{O}$ 为观测空间，$\mathcal{T}$ 为状态转移模型，$\mathcal{R}$ 为奖励函数，$\gamma$ 为折扣因子。在此设定下，强化学习智能体需直接从高维观测映射到关节空间控制量，面临严重的探索困难——移动操控任务由导航与操作交替子阶段构成，时间跨度长且奖励稀疏。

ReLMoGen 的核心设计是将上述POMDP**提升**为一个新的POMDP，其动作空间从底层关节控制量变为运动生成器的子目标：

$$(\mathcal{S}, \mathcal{A}', \mathcal{O}, \mathcal{T}', \mathcal{R}', \gamma)$$

其中 $\mathcal{A}'$ 为子目标动作空间。这一提升改变了问题的结构：策略不再需要学习如何无碰撞地移动机器人，而只需学习“往哪里移动/交互”，将“如何移动”交由运动生成器处理。

提升后的奖励函数定义为子目标执行期间累计的原始奖励：

$$\mathcal{R}'(s_t, a'_t) = \sum_{k=t}^{t+T-1} \mathcal{R}(\bar{s_k}, a_k)$$

其中 $a'_t$ 为时刻 $t$ 产生的子目标，$T$ 为运动生成器执行该子目标所需的底层动作步数，$\bar{s_k}$ 和 $a_k$ 分别为执行过程中第 $k$ 步的状态和底层动作。这一累计奖励机制使子目标策略能够感知其决策带来的多步后果。

### 2. 核心模块：子目标生成策略与运动生成器

ReLMoGen 由两个核心模块构成分层控制架构：

**子目标生成策略（Subgoal Generation Policy, SGP）** 作为高层控制器，接收RGB-D、LiDAR和任务信息（如目标位置），输出运动生成器的子目标。论文提出了两种动作参数化方式：
- **SGP-D**：采用离散密集Q值图，将动作空间离散化为网格，输出每个离散动作的Q值。
- **SGP-R**：采用连续回归，直接输出基座子目标（2D极坐标位置及朝向变化）、臂部子目标（末端执行器3D位置及参数化推动动作），以及一个二元阶段指示器（导航阶段/操作阶段）。

**运动生成器（Motion Generator, MG）** 作为底层执行器，是一个不可抢占的子程序。它接收SGP输出的子目标 $a'$，通过基于采样的运动规划器（训练时使用RRT-Connect）搜索无碰撞轨迹，并由底层关节控制器执行变长的动作序列。MG包含两个子模块：
- **基座运动生成器**：接收基座目标位置与朝向，规划并执行底盘运动轨迹。
- **臂部运动生成器**：接收末端执行器目标位置或推动参数，规划并执行机械臂运动轨迹。

这一分层设计的关键在于：运动生成器是**预定义的经典规划与控制方案**，而非需要学习的策略。这使得子目标策略的训练避开了底层控制的探索困难，同时保留了运动生成器带来的安全性与可靠性保证。



## 实验与关键发现

### 核心结果：ReLMoGen在所有任务上取得最高完成度

Table I汇总了ReLMoGen及其变体与三个基线方法在全部七项任务上的最终性能。ReLMoGen-R（连续子目标参数化）在所有任务上均取得了最高的平均任务完成度，而基线方法在多数需要长序列导航与交互的任务上几乎完全失败。

在**交互式导航任务**上，ReLMoGen的优势最为显著。以PushDoorNav为例，ReLMoGen-R的平均成功率达到**0.97**，而SAC、OAC和HRL4IN的成功率均为**0.0**——这些基线方法从未成功完成推门并导航至目标点的完整序列。ButtonDoorNav任务同样呈现类似格局：ReLMoGen-R达到0.73，基线方法几乎为零（SAC 0.01，OAC 0.01，HRL4IN 0.0）。InteractiveObstaclesNav任务中，ReLMoGen-R取得0.79，而SAC仅0.51，OAC和HRL4IN则完全无法完成。

在**移动操作任务**上，ReLMoGen与SAC的表现各有千秋。ArrangeKitchenMM任务中，ReLMoGen-R的“# Closed”指标（10°/10 cm容差）为4.91，与SAC的4.95基本持平，但显著优于OAC（3.55）和HRL4IN（4.67）。更具挑战性的ArrangeChairMM任务中，仅ReLMoGen-R取得了非零结果（0.11），所有基线均为0.0。这表明当任务需要精确的基座-臂部协调时，分层子目标策略展现出独特的优势。

在**纯导航任务**PointNav上，ReLMoGen-R的SPL达到0.63，略优于SAC（0.60），显著领先OAC（0.45）和HRL4IN（0.27）。值得注意的是，即使是在SAC能够取得一定进展的任务上，ReLMoGen仍然保持了领先或持平的性能，同时训练效率远高于基线。

### 训练效率：数量级的梯度更新减少

ReLMoGen不仅在最终性能上领先，其训练效率的提升更为突出。如Fig. 4所示，ReLMoGen在相同数量的环境episode内获得了更高的回报和任务完成度。更重要的是，**ReLMoGen所需的梯度更新步数比基线少一个数量级**，这转化为约**7倍的平均壁钟时间加速**。

这一效率提升的根源在于动作空间的提升设计：SGP每次决策对应一个子目标，该子目标由运动生成器展开为多步底层执行（每次episode使用25个子目标步，等效于基线的750个关节控制步）。因此，RL智能体只需学习稀疏的子目标级决策，而非密集的关节级控制，大幅压缩了有效决策步数。

### 探索行为分析：物理空间覆盖与有意义交互的质变

Fig. 5从三个维度揭示了ReLMoGen与SAC在探索模式上的结构性差异：

- **潜在状态空间**（Fig. 5a）：通过t-SNE将策略的循环神经网络隐藏状态投影至二维，ReLMoGen-R的轨迹在潜在空间中覆盖更广的区域，跳跃距离更大。这表明子目标级动作空间使得智能体能够在状态空间中实现更大幅度的跨越，而非被限制在局部邻域内。
- **物理位置覆盖**（Fig. 5b）：在PushDoorNav任务的俯视图中，ReLMoGen-R的基座轨迹几乎遍布整个可达区域，而SAC的轨迹高度集中在起始位置附近。SAC难以探索远离起点的区域，因为关节空间的随机扰动很少能产生有意义的基座位移。
- **有意义交互分布**（Fig. 5c）：ReLMoGen-R在门、按钮等任务相关物体附近产生了密集的交互热区，而SAC的交互稀疏且分散。这说明运动生成器不仅提升了探索广度，更将探索引导至任务相关的结构上——智能体无需学习如何接近物体，只需学习“接近物体”这一子目标本身。

### 消融实验与鲁棒性验证

**运动规划器泛化性**：Table II和Table A.8展示了ReLMoGen对底层运动生成器变化的鲁棒性。训练时仅使用RRT-Connect作为基座和臂部的运动规划器，测试时切换为Lazy PRM（一种更高效但路径质量可能较低的规划器），在PushDoorNav、TabletopReachM、InteractiveObstaclesNav和ArrangeChairMM等任务上性能几乎无下降。这一结果表明，**子目标生成策略学到的是任务级的语义知识，而非对特定规划器行为的过拟合**。

**臂部碰撞检测的域差距**：为加速训练，训练时关闭了臂部运动规划的碰撞检测。Table A.2的消融显示，这一简化导致的评估性能下降极小（多数任务降幅<0.05），验证了框架对运动生成器内部实现细节的低敏感性。

**新场景微调**：Table A.7展示了ReLMoGen的迁移能力。将在Scene-A上训练的PushDoorNav策略直接部署到Scene-B（不同布局），初始成功率为0.0；但仅需**2×10⁴个episode的微调**，成功率即恢复至**0.88**。这表明学到的子目标策略具备良好的场景泛化基础，仅需少量适应即可迁移。

### 基线方法的失败模式分析

SAC和OAC在关节空间操作的失败并非源于算法本身的缺陷，而是**探索困难的结构性后果**。在长达数百步的episode中，随机探索关节速度几乎不可能偶然完成“导航至门前→对准门→推动门→穿过门→导航至目标”的完整序列。即使OAC引入了乐观探索机制，在高维观测空间和连续动作空间的组合下，其效果也十分有限——这与分析中指出的“深度探索仍是开放问题”一致。

HRL4IN虽然采用了分层结构，但其底层策略仍需从头学习控制，因此继承了端到端RL的探索困难。相比之下，ReLMoGen的底层运动生成器是预定义的经典方法，无需学习即可提供无碰撞的轨迹执行，使得高层RL只需专注于“往哪里去”的战略决策。

### 补充图表

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2008_07792/figures/003_Figure_3.jpg]]
*Figure 3: (f) ArrangeChairMM Fig. 3: The simulation environments and tasks. (a)(b) navigationonly and manipulation-only tasks, (c)(d) three Interactive Navigation tasks, (e)(f) two Mobile Manipulation tasks*

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2008_07792/figures/004_Figure_4.jpg]]
*Figure 4: (g) ArrangeChairMM Fig. 4: Training curves for ReLMoGen and the baselines (SAC, OAC, and HRL4IN). ReLMoGen achieves higher reward with the same number of environment episodes and higher task completion for all seven tasks while the baselines often converge to sub-optimal solutions. The curve indicates the mean and standard deviation of the return across three random seeds. Note that the x-axis indicates environment episodes rather than steps to allow for a fair comparison between solutions that use actions with different time horizons*

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2008_07792/figures/005_Table.jpg]]
*Table: I: Task completion metrics for two version of ReLMoGen, one using DQN with discrete subgoal parameterization (ReLMoGen-D) and one using SAC with continous subgoal parameterization (ReLMoGen-R). We compare with two baselines (see Sec. IV-A). The entries of this table are in the format of mean/std/max over 3 random seeds and the method with the highest mean value is highlighted in bold. (a) PushDoorNav Task (b) ArrangeKitchenMM Task TABLE II: Our policy trained with RRT-Connect as the motion planner for base and arm can perform equally well when changing to Lazy PRM at test time (the first row shows the training setup)*

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2008_07792/figures/006_Figure_5.jpg]]
*Figure 5: (b) Cartesian Space (c) Interaction map Fig. 5: Exploration of ReLMoGen-R and SAC. (a) shows the 2D projection of latent state space: SAC traverses nearby states with low-level actions, while ReLMoGen-R jumps between distant states linked by a motion plan. (b) shows the physical locations visited by ReLMoGen-R and SAC in 100 episodes: ReLMoGen-R covers a much larger area. (c) shows a top-down map of meaningful interactions (duration ≥1s) during exploration. ReLMoGen-R is able to interact with the environment more than SAC*

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2008_07792/figures/009_Table.jpg]]
*Table: A.3: Hyperparameters for SGP-R TABLE A.6: Hyperparameters for iGibson simulator*

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2008_07792/figures/010_Table.jpg]]
*Table: A.4: Hyperparameters for SGP-D TABLE A.7: Fine-tuning performance for PushDoorNav on a new scene*

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2008_07792/figures/012_Figure.jpg]]
*Figure: (a) Movo and Fetch (d) (b) Task Success Rate (c) Arm MP Success Rate (e) (g) Fig. A.1: Fine-tuning on the new robot Movo. (a) We choose Movo because it is geometrically similar to Fetch. (b) We show that with only 2 \times 1 0 ^ { 4 } fine-tuning episodes, we can significantly improve the success rate for the new robot. Our Subgoal Generation Policy learns to adapt the subgoals to better accommodate the new embodiment, e.g. setting the base subgoal slightly further away from the door so that the new, longer arm has enough clearance for planning. (c) shows the arm motion planner success rate through the fine-tuning process, as the subgoal generation gets refined, the arm motion planner succe...*

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2008_07792/figures/014_Table.jpg]]
*Table: (a) TabletopReachM (b) InteractiveObstaclesNav (c) ArrangeChairMM TABLE A.8: This table complements Table II and includes more tasks. Our policy trained with RRT-Connect as the motion planner for base and arm can perform equally well when we change to Lazy PRM at test time (the first row shows the setup used at training)*

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2008_07792/figures/015_Figure.jpg]]
*Figure: (i) InteractiveObstaclesNav Fig. A.2: This figure shows visualization of ReLMoGen-D action maps during evaluation. The image pairs contain the input RGB frames on the left and normalized predicted Q-value maps on the right. The predicted Q-value spikes up at image locations that enable useful interactions, e.g. goals, chairs, cabinets, doors, buttons, and obstacles. (a) shows that the agent correctly predicts high Q-value on the goal. (b) and (c) show that the agent learns to push the most suitable part of the chair. (d) shows that the agent prioritizes pushing a drawer that is “more open” than an almost closed cabinet to harvest more reward. Vice versa for (e). (f) and (i) show that the ag...*

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2008_07792/figures/016_Figure.jpg]]
*Figure: (a) ReLMoGen-R on PushDoorNav (b) ReLMoGen-R on ButtonDoorNav (c) ReLMoGen-D on PushDoorNav (d) ReLMoGen-D on ButtonDoorNav*

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2008_07792/figures/017_Figure.jpg]]
*Figure: Fig. A.3: Subgoal distribution during training. The subgoal success rate increases over time, indicating our policy learns to use MG better and set more feasible subgoals as training progresses. The policy is also able to accomplish the task with fewer and fewer subgoals. (a) PushDoorNav (b) ArrangeKitchenMM Fig. A.4: Policy visualization for ReLMoGen. A base subgoal is depicted as a red circle with an arrow on the floor to indicate the desired base position and yaw angle. An arm subgoal is depicted as a yellow ball that indicates the desired end-effector position, and a red arrow that indicates the desired pushing action from that position. For PushDoorNav task, the robot first navigates t...*



## 定位与知识库关联

### 1. 问题瓶颈与设计动机

移动操控任务（如推开障碍物后导航、开门后通过）天然具有长时间跨度与稀疏奖励的特性。机器人需要在导航与操作子阶段间交替，而直接使用关节空间连续控制量（如各轮子与臂关节的速度）进行端到端强化学习时，智能体面临严重的探索困难：高维连续动作空间中的随机扰动很难偶然产生有意义的任务进展，导致训练不稳定或收敛至次优策略。ReLMoGen 的核心洞察是：**一个成功的移动操控策略可以被描述为一系列面向运动生成器的子目标序列**，而非逐时间步的底层关节指令序列。因此，问题瓶颈不在于“如何移动每个关节”，而在于“往哪里移动/与什么交互”。

### 2. 方法定位：分层架构中的“学习-规划”混合范式

ReLMoGen 在方法论谱系中占据一个特殊位置：它既不是纯粹的端到端强化学习，也不是完整的层次化强化学习（HRL），而是一种**将经典运动规划作为不可学习底层模块嵌入RL训练环路**的混合范式。

与三类基线方法的关系如下：

- **端到端RL基线（SAC, OAC）**：SAC 直接在关节空间输出速度控制量，需要同时学习碰撞避免、精确控制和任务策略。OAC 引入乐观Q函数探索机制，但在高维观测/动作空间下探索效率提升有限。ReLMoGen 将动作空间从关节速度提升为运动生成器的子目标，使RL仅需学习“目标位置预测”，而将“如何无碰撞到达”交给基于采样的运动规划器（如 RRT-Connect）——这从根本上消解了端到端方法面临的探索困难。

- **层次化RL基线（HRL4IN）**：HRL4IN 同样采用高层产生子目标、底层执行的分层结构，但其底层控制器需要从头学习。这种“双学习”架构面临非平稳性问题——高层策略在底层策略尚未收敛时的子目标信号缺乏意义，导致训练不稳定。ReLMoGen 的关键差异在于：**底层运动生成器是预定义的、无需训练的规划与控制方案**，在整个训练过程中始终保持一致的执行能力。这使得高层子目标生成策略的训练信号更加稳定，避免了层次化RL中常见的联合训练困难。

从更广的文献背景来看，ReLMoGen 延续了“将经典方法嵌入学习框架”的设计哲学，但其独特之处在于将运动生成器**作为RL训练环路中的非抢占式子程序**使用——每个策略步查询一次运动生成器，由其规划并执行一段变长的无碰撞轨迹，然后RL接收累积奖励进行更新。这与“先规划后学习”或“用学习改进规划器”的范式有本质区别。

### 3. 适用边界与关键假设

ReLMoGen 的有效性建立在以下假设之上：

1. **运动生成器的可靠性**：底层规划器（RRT-Connect 等）需要能够从当前状态找到到达子目标的无碰撞轨迹。在高度杂乱或动态障碍物环境中，规划器可能频繁失败，此时策略的性能将受限于规划器的成功率。

2. **目标位置的先验知识**：导航任务需要预先知道目标位置和基于平面图的最短路径。该假设在完全未知环境中不成立，限制了方法在探索式导航场景中的直接应用。

3. **交互原语的有限性**：当前实现仅验证了“推动”这一种交互原语（参数化推动动作）。尽管框架设计上允许扩展至抓取、拉拽等其他交互类型，但尚未验证子目标生成策略在不同交互类型间自适应切换的能力。

4. **仿真环境的感知完整性**：运动生成器依赖从传感器实时构建的局部环境模型。在真实部署中，传感器噪声和不完整感知（如遮挡、反射）可能导致规划器性能下降，进而影响整体策略表现。

### 4. 核心局限与开放问题

**已识别的局限**：

- **交互类型单一**：仅实现了参数化推动交互，尚未验证框架对更丰富操作原语（抓取、放置、拉拽）的扩展能力。
- **仿真-现实差距未验证**：所有训练和评估均在 iGibson 仿真环境中完成。虽然论文讨论了 Sim2Real 的潜力（如域随机化、运动规划器的现实可用性），但未给出真实机器人实验的结果。感知域差异和动力学域差异可能导致实际部署中的性能下降。
- **导航假设较强**：依赖预知目标位置和最短路径，在完全未知或动态变化的环境中不直接适用。
- **OAC 探索瓶颈**：OAC 基线在多数任务上未能显著超越 SAC，表明高维连续观测/动作空间下的深度探索仍是一个开放问题，ReLMoGen 通过动作空间提升绕过了而非解决了这一挑战。

**开放问题**：

1. 在真实机器人上部署时，感知域差距和动力学域差距会导致多大的性能下降？如何通过域随机化、在线系统辨识或自适应规划器选择来系统性弥合这一差距？
2. 如何将子目标生成策略扩展至更丰富的交互原语（抓取、放置、拉拽），并使策略在不同交互类型间自适应切换——例如，根据任务阶段自动选择“推动”或“抓取”子目标？
3. 在动态障碍物或半结构化环境中，运动生成器可能频繁失败。策略应如何感知规划器的失败信号并做出适应性调整（如重新规划、切换子目标、或回退至安全状态）？
4. 当前方法能否扩展至多机器人协作场景或更复杂的长期任务（如跨多个房间的序列化操作）？多智能体场景中运动生成器间的协调与冲突消解是额外的挑战。
5. 如何进一步提升在高维连续观测/动作空间下的深度探索效率，使乐观探索方法（如 OAC）在机器人任务中真正发挥优势，而非仅依赖动作空间提升来回避探索困难？



## 原文 PDF

![[paperPDFs/ICRA_2021/ReLMoGen_Integrating_Reinforcement_Learning_and_Motion_Generation_for_Interactive_Navigation.pdf]]
