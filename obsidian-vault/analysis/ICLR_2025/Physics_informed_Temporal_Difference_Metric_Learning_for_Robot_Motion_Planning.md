---
title: "Physics-informed Temporal Difference Metric Learning for Robot Motion Planning"
type: paper
paper_level: A
venue: ICLR
year: 2025
pdf_ref: paperPDFs/ICLR_2025/Physics_informed_Temporal_Difference_Metric_Learning_for_Robot_Motion_Planning.pdf
aliases:
- PPITDML
- PITDMLRMP
tags:
- ICLR_2025
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "将时序差分学习与Eikonal方程损失相结合，在整个有限时间域上施加Bellman最优性原理，同时设计度量学习架构来保留测地线属性，并使用采样模型预测控制（MPC）进行路径推断。"
primary_logic: "将Eikonal方程解释为具有单位速度约束的最优控制问题的最优值函数，并同时作为黎曼流形上的测地线距离。通过时间离散Bellman损失来捕捉全局结构，通过度量学习网络保证距离函数的基本性质，并利用注意力机制实现跨环境的泛化。"
claims:
- "引入时序差分（TD）损失有效补偿了仅使用Eikonal损失时产生的过拟合和局部错误。"
- "消融实验表明，移除TD损失或Eikonal损失均会导致值函数精度显著下降，表明两者互补至关重要。"
- "所提出的度量学习架构（L1与L∞组合）在迷宫实验中优于IQE、PQE、MRN、DN等其他度量表示。"
- "在Cluttered 3D和7-DOF机械臂任务上，本文方法的成功率大幅超越NTFields和P-NTFields，同时将推理时间降低到采样规划器的水平。"
---

# Physics-informed Temporal Difference Metric Learning for Robot Motion Planning

> [!tip] 核心洞察
> 将Eikonal方程解释为具有单位速度约束的最优控制问题的最优值函数，并同时作为黎曼流形上的测地线距离。通过时间离散Bellman损失来捕捉全局结构，通过度量学习网络保证距离函数的基本性质，并利用注意力机制实现跨环境的泛化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于物理信息的时序差分度量学习在机器人运动规划中的应用 |
| 英文题名 | Physics-informed Temporal Difference Metric Learning for Robot Motion Planning |
| 会议/期刊 | ICLR 2025 |
| Links | [paper](https://arxiv.org/abs/2505.05691); [GitHub](https://github.com/ruiqini/ntrl-demo) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | PTDML (Physics-informed Temporal Difference Metric Learning) |
| Dataset | Cluttered 3D (C3D) 已知环境, 7-DOF 机械臂操作 (已知环境), 12-DOF 双臂真实橱柜环境, Gibson 2D 导航 (已知环境) |

> [!tip] 效果简介
> - Cluttered 3D (C3D) 已知环境 上，成功率 (SR%) 为 99.6，对比 NTF 94.7，变化 +4.9%。
> - 7-DOF 机械臂操作 (已知环境) 上，成功率 (SR%) 为 88.2，对比 NTF 74.6，变化 +13.6%。
> - 12-DOF 双臂真实橱柜环境 上，成功率 (SR%) 为 91，对比 NTF / P-NTF 无法收敛，变化 ～+91%。

## 概述

机器人运动规划的核心挑战在于，如何在复杂、高维的配置空间中高效地找到无碰撞路径。近年来，基于物理信息神经网络的自监督方法——特别是**NTFields**（Ni et al., 2021）——通过求解Eikonal方程来学习行程时间场，展现出无需专家轨迹即可规划的能力。然而，这类方法存在一个根本性瓶颈：**仅依赖局部Eikonal损失难以捕捉值函数的全局最优结构**，在杂乱、多联通环境中容易陷入局部最优，导致泛化失败和路径质量下降。

本文提出**PTDML（Physics-informed Temporal Difference Metric Learning）**，一个将时序差分学习、度量学习与物理信息建模深度融合的运动规划框架。其核心洞察在于：将Eikonal方程的解同时解释为最优控制问题的值函数和黎曼流形上的测地线距离，从而可以同时施加Bellman最优性原理和距离函数的公理化约束。

具体而言，PTDML做出了三项关键改进：

1. **时序差分损失（$L_{TD}$）**：在有限时间步上施加Bellman最优性，强制值函数在全局范围内一致传播，有效补偿了纯Eikonal损失造成的过拟合和局部偏差。Figure 1直观展示了这一机制：仅用Eikonal损失训练的网络可以收敛到满足局部梯度约束的错误解，而TD损失通过强制$T(q_1)-T(q_1-d)=d$这样的时序一致性，将解拉回真值。

2. **度量学习架构**：将行程时间建模为潜在空间中的度量距离$T(q_s,q_g)=D(f_\theta(q_s), f_\theta(q_g))$，天然保证非负性、对称性和三角不等式。特别设计的混合$L_1/L_\infty$距离度量能够在多联通区域中保留多重最短路径结构（Figure 2），避免了传统$L_2$嵌入造成的路径重叠和歧义。

3. **采样模型预测控制（MPC）推理**：摒弃了沿值函数负梯度的确定性下降策略，转而采用随机采样动作并通过softmax加权选择最优轨迹。这一设计使推理过程能够跳出值函数中的局部极小值，同时将规划时间降低到采样规划器的水平。

实验覆盖了从2D迷宫到12-DOF双臂机器人的广泛任务。在Cluttered 3D已知环境中，PTDML的成功率达到**99.6%**，超越NTFields的94.7%；在7-DOF机械臂操作任务上，成功率从NTFields的74.6%提升至**88.2%**；在12-DOF真实橱柜环境中，NTFields和P-NTFields均无法收敛，而PTDML取得了**91%**的成功率，单条轨迹规划仅需0.11秒。消融实验（Figure 3, Table 2）系统验证了每个损失项和度量设计对值函数精度的贡献：移除TD损失使迷宫误差从0.08升至0.21，移除Eikonal损失则使误差急剧恶化至1.13，证明了二者的互补不可或缺。

**方法定位**：PTDML处于物理信息学习与度量强化学习的交叉点。它继承了NTFields自监督、无需专家轨迹的优势，但通过引入时序差分和度量约束，从根本上解决了值函数学习的全局一致性问题。与监督式方法（如MPNet、MPiNet）相比，PTDML的数据生成仅需数秒至数分钟（Table 4），而前者需要数小时的专家轨迹采集。与采样规划器（RRTConnect、LazyPRM）相比，PTDML在保证高成功率的同时将推理时间压缩了数个数量级。

## 背景与动机

机器人运动规划的核心挑战在于：如何在高维、复杂且杂乱的配置空间（C-space）中，为机器人快速找到一条从起始构型到目标构型的无碰撞、平滑路径。传统方法中，基于采样的规划器（如 RRTConnect、LazyPRM）具有概率完备性，但在高维空间中收敛缓慢，且规划时间不可预测；而基于 Eikonal 方程的快速行进法（FMM，Sethian, 1996）虽然能给出全局最优解，却受限于维度灾难，难以扩展到 3 维以上的空间。

近年来，基于学习的方法试图打破这一瓶颈。其中，自监督学习方法 **NTFields**（Ni et al., 2021）及其改进版本 **P-NTFields**（Ni & Qureshi, 2023a）通过将行程时间函数参数化为对欧氏距离的扭曲，并利用 Eikonal 方程损失进行训练，在多个规划任务上取得了显著进展。然而，这类方法存在一个根本性瓶颈：**在复杂、杂乱环境中，仅凭 Eikonal 损失难以同时保持行程时间函数作为最优值函数和黎曼流形上测地线距离的双重属性**，从而导致局部最优和泛化失败。

具体而言，该瓶颈体现在两个层面：

1. **值函数的不一致性**：Eikonal 方程在无穷小时间尺度上成立，但仅凭局部约束训练的网络容易收敛到满足方程却偏离真实解的“虚假解”。Figure 1 清晰地展示了这一点：给定相同的训练采样点，仅用 Eikonal 损失会产生不正确的次优解，而引入时序差分（TD）学习——在有限时间步上强制 Bellman 最优性原理——则能有效锁定真实解。这意味着，**缺乏全局时序一致性约束是现有方法过拟合和产生局部错误的核心原因**。

2. **测地线属性的丢失**：行程时间函数本质上是一个度量函数，应当满足非负性、对称性和三角不等式。然而，NTFields 使用的因子化形式 $T(q_s,q_g) = \|q_s-q_g\| / \tau(q_s,q_g)$ 并不天然保证三角不等式，且其欧氏距离嵌入在多联通区域中会导致多重最短路径的退化和歧义。Figure 2 表明，使用 L2 距离嵌入时，圆上的测地线会坍缩为一条直线；而 L1 距离则能将其转换为菱形，保留测地线结构。这揭示了：**设计正确的度量学习架构对于保留 Eikonal 方程解的测地线属性至关重要**。

本文的动机正是从上述两个缺口切入：**将 Eikonal 方程同时解释为最优控制问题的值函数和黎曼流形上的测地线距离，通过时序差分度量学习框架，在统一的理论基础上同时解决值传播的全局一致性和距离函数的几何完备性**。此外，在推理阶段，本文采用基于采样的模型预测控制（MPC）替代传统的梯度下降，以避免陷入值函数中的局部最小值，进一步提升规划的成功率和效率。

## 核心创新

本文提出的 **PTDML** (Physics-informed Temporal Difference Metric Learning) 针对现有自监督运动规划方法（以 **NTFields** (Ni et al., 2021) 和 **P-NTFields** (Ni & Qureshi, 2023a) 为代表）在复杂杂乱环境中无法同时保持 Eikonal 方程作为最优值函数和测地线距离的双重性质这一瓶颈，从损失函数、网络架构和推理方式三个维度进行了系统性创新。

### 1. 损失函数：从单一物理约束到多目标时序优化

NTFields 仅依赖 Eikonal 损失 $L_E$ 来约束局部波速传播，但该损失本质上只强制了梯度范数与波速的一致性，无法捕捉值函数的全局结构。如图 1 所示，仅用 $L_E$ 训练可产生满足局部 Eikonal 方程但全局错误的解。PTDML 的核心突破在于引入**时序差分（TD）损失** $L_{TD}$，将运动规划重新表述为最优控制问题：

$$T(q_s, q_g) = \min_{u(t)} \int_{t_s}^{t_g} \frac{ \| \dot{q}(t) \| }{ S^*(q(t)) } dt, \quad \| u(t) \| = 1$$

并基于 Bellman 最优性原理在有限时间步 $\Delta t$ 上强制值传播一致性：

$$L_{TD} = \left[ T(q_s, q_g) - \frac{\Delta t}{S^*(q_g)} - T(q_s, q_g + u_g^* \Delta t) \right]^2 + \left[ T(q_s, q_g) - \frac{\Delta t}{S^*(q_s)} - T(q_s + u_s^* \Delta t, q_g) \right]^2$$

这一设计使得值函数学习不再仅依赖局部梯度信息，而是通过离散 Bellman 残差捕捉全局最优结构。消融实验（Figure 3, Table 2）强有力地验证了该设计的必要性：移除 $L_{TD}$ 后迷宫值函数误差从 0.08 升至 0.21，而移除 $L_E$ 则导致误差急剧恶化至 1.13，表明两者互补——$L_E$ 提供局部物理一致性，$L_{TD}$ 保证全局值传播正确性。

此外，PTDML 还引入了两个辅助损失：**障碍法向对齐损失** $L_N$ 鼓励值函数梯度在障碍物附近与安全场法向一致，避免生成穿越障碍物的路径；**因果权重** $L_C = \exp(-\lambda_C T(q_s, q_g))$ 使优化器优先学习离起点较近的小行程时间，保证单向值传播的因果关系。最终组合损失为：

$$L = \left( \lambda_E L_E + \lambda_{TD} L_{TD} + \lambda_N L_N \right) L_C$$

消融表明，移除 $L_N$ 和 $L_C$ 分别使误差升至 0.13 和 0.12，验证了它们在训练早期提供强先验和维持因果结构中的作用。

### 2. 网络架构：从因子化距离到度量学习

NTFields 将行程时间参数化为 $T(q_s, q_g) = \|q_s - q_g\| / \tau(q_s, q_g)$ 的因子化形式，该表示不保证三角不等式，无法准确捕捉测地线距离的基本性质。PTDML 转而采用**度量学习架构**，将行程时间定义为潜在空间中的度量距离：

$$T(q_s, q_g) = D( f_\theta (q_s), f_\theta (q_g) )$$

其中距离度量 $D$ 采用混合 $L_1/L_\infty$ 设计：

$$D(x, y) = \sum_{i=1}^{a} \left[ \max_{1 \leq j \leq b} | x_{i,j} - y_{i,j} | \right]$$

这一设计的核心洞察在于：Eikonal 方程的解在多联通区域中存在多重最短路径，而传统欧氏距离会将测地线“坍缩”为直线，造成歧义。如图 2 所示，混合 $L_1/L_\infty$ 度量将圆上的测地线映射为二维菱形，保留了多路径结构。消融实验（Figure 3, Table 2）将本文度量替换为 IQE、PQE、MRN、DN 后，误差分别升至 0.32、0.46、0.19 和 0.29，证明该度量设计更好地保持了测地线性质。

为实现跨环境泛化，PTDML 引入**环境编码模块**：使用 PointNext 对环境障碍物点云编码为全局潜在特征，通过交叉注意力机制将机器人配置的随机傅里叶特征与环境特征融合，再经 PirateNet MLP 生成条件感知的潜在表示 $f_\theta(q, \mathcal{X}_{obs})$。这使得模型能够泛化到未知环境，而 NTFields 原始架构无此能力（为公平对比，实验为其添加了相同的注意力模块）。

### 3. 推理方式：从梯度下降到采样 MPC

NTFields 沿值函数负梯度进行路径推断，在非凸值函数景观中易陷入局部最优。PTDML 改用**基于采样的模型预测控制（MPC）**：从正态分布中采样动作序列，利用 softmax 加权的成本函数选择最优轨迹，执行回退水平控制。这一设计避免了梯度计算，通过随机采样天然具备跳出局部最小值的能力。实验表明，将推理方式改为梯度下降（Our-G）后，成功率和规划时间均劣于 MPC 方式，验证了采样策略在复杂环境中的鲁棒性优势。

## 整体框架

![[assets/figures/papers/paper_list_l5_Physics_informed_Temporal_Difference_Metric_Learning_for_Robot_Motion_Pl/figures/004_Figure_4.jpg]]
*Figure 4: Depiction of our (a) Gibson, (b) Cluttered 3D (C3D), and (c) 7-DOF Manipulator environments. We also illustrate multiple trajectories planned by our method between different start and goal pairs. It can be seen that our method finds smooth trajectories while avoiding collisions*

PTDML 将机器人运动规划建模为一个最优控制问题，其核心目标是学习一个满足 Eikonal 方程和测地线性质的行程时间函数 $T(q_s, q_g)$。该方法通过三个关键设计实现这一目标：**物理信息损失函数的联合优化**、**度量学习架构的构建**，以及**采样模型预测控制（MPC）的推理策略**。

### 核心建模与输入输出

给定起始构型 $q_s$ 和目标构型 $q_g$，以及环境障碍物点云 $\mathcal{X}_{obs}$，PTDML 的目标是输出从 $q_s$ 到 $q_g$ 的行程时间 $T(q_s, q_g)$，并据此生成无碰撞的平滑路径。该方法将行程时间定义为最优控制问题的值函数：

$$T(q_s, q_g) = \min_{u(t)} \int_{t_s}^{t_g} \frac{\| \dot{q}(t) \|}{S^*(q(t))} dt, \quad \| u(t) \| = 1$$

其中 $S^*(q)$ 是基于障碍物距离的真值波速场，$u(t)$ 是单位速度控制输入。该公式将 Eikonal 方程的解同时解释为最优值函数和黎曼流形上的测地线距离，为后续的损失函数设计和架构选择奠定了理论基础。

### 整体 Pipeline 模块

PTDML 的 pipeline 由以下六个核心模块串联构成，形成从环境感知到路径生成的完整闭环：

1.  **PointNext 编码器**：接收环境障碍物点云 $\mathcal{X}_{obs}$，通过 PointNext 网络将其编码为全局潜在特征向量 $\mathbf{z}$，为后续的条件特征提取提供环境上下文。

2.  **位置编码与交叉注意力**：对机器人构型 $q$ 进行随机傅里叶特征映射 $\gamma(q)$，然后通过交叉注意力机制将构型特征与全局环境特征 $\mathbf{z}$ 融合，生成环境条件感知的构型表示。

3.  **PirateNet MLP**：对注意力输出进行深层非线性变换，生成最终的点配置潜在表示 $f_\theta(q, \mathcal{X}_{obs})$。该模块是整个度量学习的核心编码器。

4.  **度量距离函数 $D$**：计算两个构型的潜在表示之间的混合 $L_1/L_\infty$ 距离，作为行程时间的度量学习形式：
    $$T(q_s, q_g) = D(f_\theta(q_s), f_\theta(q_g))$$
    其中 $D(x, y) = \sum_{i=1}^{a} \left[ \max_{1 \leq j \leq b} | x_{i,j} - y_{i,j} | \right]$，该设计保证了非负性、对称性和三角不等式，同时能够保留多联通区域中的多重最短路径结构。

5.  **多目标损失计算**：基于网络预测的速度与真值速度，计算联合损失函数：
    $$L = \left( \lambda_E L_E + \lambda_{TD} L_{TD} + \lambda_N L_N \right) L_C$$
    其中 $L_E$ 为 Eikonal 损失，$L_{TD}$ 为时序差分损失，$L_N$ 为障碍法向对齐损失，$L_C = \exp(-\lambda_C T(q_s, q_g))$ 为因果权重。该组合损失同时施加了局部物理约束、全局值传播一致性和障碍物避碰先验。

6.  **采样模型预测控制（MPC）**：在推理阶段，从正态分布中采样动作序列，利用 softmax 加权的成本函数选择最优轨迹，执行回退水平控制。该策略避免了梯度下降可能陷入的局部最小值问题，同时显著提升了推理效率。

### 模块间的信息流

环境点云 $\mathcal{X}_{obs}$ 首先通过 PointNext 编码器转化为全局特征 $\mathbf{z}$，该特征被所有后续的构型编码共享。对于任意查询的构型对 $(q_s, q_g)$，分别通过位置编码、交叉注意力和 PirateNet MLP 生成各自的潜在表示 $f_\theta(q_s)$ 和 $f_\theta(q_g)$，再通过度量距离函数 $D$ 计算行程时间。训练时，该行程时间与真值速度场 $S^*(q)$ 共同输入多目标损失计算模块进行优化；推理时，MPC 模块以学到的行程时间函数为代价，通过采样搜索生成最终路径。

该 pipeline 的核心优势在于：**时序差分损失补偿了 Eikonal 损失在全局结构捕捉上的不足**（Figure 1 展示了仅用 Eikonal 损失会产生不正确的次优解，而 TD 损失能强制找到真实解），**度量学习架构保证了距离函数的基本性质**（Figure 2 展示了混合 $L_1/L_\infty$ 度量如何将圆上的测地线转换为二维菱形以保留多重路径结构），**MPC 推理则避免了梯度方法的局部最优问题**。三者协同使得 PTDML 能够在 2-DOF 到 12-DOF 的复杂规划任务中同时实现高成功率和低推理时间。

## 核心模块与公式推导

### 问题形式化：从Eikonal方程到最优控制

PTDML的核心洞察在于将Eikonal方程的解同时解释为最优控制问题的值函数和黎曼流形上的测地线距离。给定真值波速场 $S^*(q)$，行程时间函数 $T(q_s, q_g)$ 被定义为以下最优控制问题的最优值（Eq. 4）：

$$T(q_s, q_g) = \min_{u(t)} \int_{t_s}^{t_g} \frac{ \| \dot{q}(t) \| }{ S^*(q(t)) } dt, \quad \| u(t) \| = 1$$

其中 $u(t)$ 为单位速度控制输入。这一形式化使得Bellman最优性原理可以在有限时间步上施加，而不仅限于Eikonal方程的局部梯度约束。真值波速由截断距离函数给出：$S^*(q) = \text{clip}( d_{obs}(q, X_{obs}) / d_{max}, d_{min}/d_{max}, 1 )$（Section 3.2），确保机器人在障碍物空间内速度趋近于零。

### 损失函数体系：三重约束与因果调制

PTDML的损失函数由三个互补项组成，并以因果权重 $L_C$ 进行全局调制（Eq. 8）：

$$L = \left( \lambda_E L_E + \lambda_{TD} L_{TD} + \lambda_N L_N \right) L_C$$

**Eikonal损失 $L_E$** 通过预测波速与真值波速的比值来强制局部Eikonal方程（Eq. 3）：

$$L_E = \left( \sqrt{ S^*(q_s) / S(q_s) } - 1 \right)^2 + \left( \sqrt{ S^*(q_g) / S(q_g) } - 1 \right)^2$$

其中预测波速由梯度范数给出：$1 / S(q) = \| \nabla_q T(q_s, q_g) \|$。该损失确保值函数在局部满足波前传播的物理约束，但单独使用时容易过拟合到局部模式，无法捕捉全局最优结构（Figure 1）。

**时序差分损失 $L_{TD}$** 是本文的关键创新，通过在有限时间步 $\Delta t$ 上施加Bellman最优性来强制值传播的全局一致性（Eq. 5）：

$$L_{TD} = \left[ T(q_s, q_g) - \frac{\Delta t}{S^*(q_g)} - T(q_s, q_g + u_g^* \Delta t) \right]^2 + \left[ T(q_s, q_g) - \frac{\Delta t}{S^*(q_s)} - T(q_s + u_s^* \Delta t, q_g) \right]^2$$

该损失通过沿最优策略 $u^*$ 的Taylor展开导出，要求从起点和终点两个方向的值传播保持一致。消融实验表明，移除 $L_{TD}$ 后值函数误差从0.08升至0.21（Figure 3, Table 2），证实其对于捕捉全局值传播结构至关重要。

**障碍法向对齐损失 $L_N$** 鼓励值函数梯度在障碍物附近与安全场的法向一致（Eq. 6）：

$$L_N = (1 - S^*(q_s)) \| S^*(q_s) \nabla_{q_s} T(q_s, q_g) + \frac{\nabla_{q_s} S^*(q_s)}{\| \nabla_{q_s} S^*(q_s) \|} \|^2 + \text{(对称项)}$$

该损失仅在障碍物附近（$S^*(q) < 1$）激活，为训练初期提供强先验，避免生成穿越障碍物的路径。消融实验中移除 $L_N$ 使误差升至0.13（Figure 3）。

**因果权重 $L_C$** 以指数形式调制总损失（Eq. 7）：

$$L_C = \exp( -\lambda_C T(q_s, q_g) )$$

该权重使优化器优先学习离起点较近的小行程时间值，保证值传播的单向因果关系。移除 $L_C$ 后误差升至0.12（Figure 3），表明因果调制对于稳定训练不可或缺。

### 度量学习架构：保留测地线性质

PTDML将行程时间定义为潜在空间中的度量距离（Eq. 9）：

$$T(q_s, q_g) = D( f_\theta (q_s), f_\theta (q_g) )$$

其中 $f_\theta$ 为特征编码器，$D$ 为度量函数。该形式天然保证非负性、对称性和三角不等式。本文提出混合 $L_1/L_\infty$ 距离度量（Eq. 10）：

$$D(x, y) = \sum_{i=1}^{a} \left[ \max_{1 \leq j \leq b} | x_{i,j} - y_{i,j} | \right]$$

该度量在潜在空间的一个维度上取 $L_\infty$ 距离，在另一维度上求和。与 $L_2$ 距离将圆上测地线压缩为直线不同，该度量将圆映射为二维菱形，从而保留多联通区域中的多重最短路径结构（Figure 2）。消融实验中，替换为IQE、PQE、MRN、DN等度量后，误差分别升至0.32、0.46、0.19和0.29（Figure 3, Table 2），验证了该度量设计对于保持Eikonal方程解的关键性质至关重要。

### 环境编码与特征提取

特征编码器 $f_\theta(q, \mathcal{X}_{obs})$ 由三个模块级联而成（Section 4.2.2）：

1. **PointNext编码器**：将环境障碍物点云 $\mathcal{X}_{obs}$ 编码为全局潜在特征向量 $\mathbf{z}$。
2. **交叉注意力融合**：对机器人配置 $q$ 进行随机傅里叶特征映射 $\gamma(q)$，通过交叉注意力将其与全局环境特征 $\mathbf{z}$ 融合，产生条件感知的配置特征。
3. **PirateNet MLP**：对注意力输出进行深层非线性变换，生成最终的潜在表示 $f_\theta(q)$。

最终，条件测地线距离计算为 $T(q_s, q_g, \mathcal{X}_{obs}) = D(f_\theta(q_s, \mathcal{X}_{obs}), f_\theta(q_g, \mathcal{X}_{obs}))$，使模型能够泛化到未见环境。

### 推理：采样模型预测控制

推理阶段采用采样MPC（Section 4.3），从正态分布中采样动作序列，通过softmax加权的成本函数选择最优轨迹，执行回退水平控制。该方法避免计算值函数梯度，有助于跳出局部最小值。消融实验表明，替换为梯度下降方式（Our-G）后成功率和规划时间均劣于MPC方式（Section 5.2）。

## 实验与分析

### 核心瓶颈与因果机制验证

本文的核心假设是：仅依赖Eikonal方程损失（$L_E$）的自监督方法（如NTFields、P-NTFields）在复杂杂乱环境中无法同时保持值函数的最优性与测地线距离的基本性质，导致局部最优和泛化失败。PTDML通过三个因果调节变量解决这一问题：（1）引入时序差分损失$L_{TD}$在有限时间域上施加Bellman最优性原理；（2）设计混合$L_1/L_\infty$度量学习架构保留测地线多重路径结构；（3）采用采样MPC推理跳出局部最小值。以下实验系统验证了每个调节变量的必要性。

### 主实验结果

**Table 1** 汇总了在Gibson 2D导航、Cluttered 3D（C3D）和7-DOF机械臂操作三个基准上的综合性能。PTDML在所有任务上均取得最高成功率（SR）和最低规划时间。具体而言：

![[assets/figures/papers/paper_list_l5_Physics_informed_Temporal_Difference_Metric_Learning_for_Robot_Motion_Pl/figures/005_Table_1.jpg]]
*Table 1: Performance comparison on Gibson, C3D, and 7-DOF manipulator datasets*

- **Gibson 2D导航（已知环境）**：PTDML成功率达95.1%，显著优于NTFields（约86.4%，估计值，需原文确认具体数值）和P-NTFields，同时规划时间降低至采样规划器水平。
- **Cluttered 3D（已知环境）**：PTDML成功率为99.6%，较NTFields（94.7%）提升4.9个百分点（Table 3(b) seen）。
- **7-DOF机械臂操作（已知环境）**：PTDML成功率为88.2%，较NTFields（74.6%）提升13.6个百分点（Table 3(c) seen）。这一大幅提升表明TD损失和度量学习在高维配置空间中尤为关键。

![[assets/figures/papers/paper_list_l5_Physics_informed_Temporal_Difference_Metric_Learning_for_Robot_Motion_Pl/figures/010_Table_3.jpg]]
*Table 3: Performance comparison on C3D, and 7-DOF manipulator datasets for seen and unseen environments for our, NTF, and P-NTF methods, while other learning-based methods are not configured for this setting. It can be seen that our method exhibits high SR compared with existing self-supervised learning methods and low planning times*

**跨环境泛化能力**（Table 3）：在C3D和7-DOF机械臂的未知环境测试中，PTDML的成功率显著超越NTFields和P-NTFields。值得注意的是，NTFields和P-NTFields原本不支持多环境泛化，为公平对比，我们为其添加了与PTDML相同的注意力环境编码模块。即便如此，PTDML仍展现出更强的泛化能力，验证了TD损失和度量学习对全局结构捕捉的贡献。

**真实世界验证**：在12-DOF双臂机器人真实橱柜环境中，PTDML成功率达91%，规划时间仅0.11秒（Figure 5），而NTFields和P-NTFields在此任务上无法收敛。这验证了方法在高度复杂真实场景下的可行性。

**与传统规划器和监督学习方法对比**：PTDML在规划时间上大幅优于RRTConnect和LazyPRM（均给予30秒上限），同时无需像MPNet、MPiNet等监督方法那样依赖数小时的专家轨迹数据生成。Table 4显示，自监督方法的数据生成仅需数秒至几分钟，训练时间也显著更短。

![[assets/figures/papers/paper_list_l5_Physics_informed_Temporal_Difference_Metric_Learning_for_Robot_Motion_Pl/figures/012_Table_4.jpg]]
*Table 4: Data generation and training time*

### 消融实验

在二维迷宫环境上的消融实验（Figure 3, Table 2）系统解耦了各损失组件和度量设计的贡献，以与真值FMM的平均绝对误差作为评价指标：

![[assets/figures/papers/paper_list_l5_Physics_informed_Temporal_Difference_Metric_Learning_for_Robot_Motion_Pl/figures/008_Table_2.jpg]]
*Table 2: The error of all methods, including ours, on maze environments. The error denotes the mean absolute difference between the travel time of each method and the ground truth FMM, measured at grid points*

- **完整模型**：误差仅0.08，值函数与FMM真值高度一致。
- **移除Eikonal损失（$-L_E$）**：误差急剧上升至1.13，值函数完全失效。这验证了$L_E$是保证局部波速约束的基石。
- **移除时序差分损失（$-L_{TD}$）**：误差升至0.21。尽管$L_E$保留，但模型无法捕捉全局值传播结构，出现Figure 1所示的次优解问题。这直接证实了核心假设：$L_E$单独训练会产生过拟合和局部错误，$L_{TD}$通过Bellman一致性有效补偿这一缺陷。
- **移除障碍法向对齐损失（$-L_N$）**：误差升至0.13。$L_N$在训练初期提供强先验，防止值函数梯度在障碍物附近产生穿越障碍物的短路路径。
- **移除因果权重（$-L_C$）**：误差升至0.12。$L_C$通过指数衰减权重$\exp(-\lambda_C T(q_s, q_g))$强制优化器优先学习离起点较近的小行程时间，保证值传播的因果关系。
- **度量函数替换**：将PTDML的混合$L_1/L_\infty$度量替换为IQE、PQE、MRN、DN后，误差分别升至0.32、0.46、0.19和0.29。这表明本文度量设计更好地保留了多联通区域中的多重最短路径结构（如Figure 2所示，$L_2$距离将圆上测地线压缩为线段造成歧义，而$L_1$变换为菱形保留结构）。

**推理方式消融**：将MPC推理替换为梯度下降（Our-G）后，成功率和规划时间均显著劣化。这验证了随机采样有助于跳出值函数中的局部最小值，在高维配置空间中尤为关键。

### 失败模式与局限性

尽管整体性能优异，消融实验的误差分布图（Figure 3）显示，即使完整模型在迷宫某些局部区域（如右下角）仍出现值函数精度下降。这表明以下局限性：

- **狭窄通道中的平衡问题**：障碍法向对齐损失$L_N$可能不足以在狭窄通道中平衡目标导向与避障需求，超参数需针对每个环境调整。
- **未知环境泛化衰减**：在高度复杂的Gibson数据集上，模型在完全未知环境下的泛化成功率相较于已知环境有所下降，表明环境编码器（PointNext）在复杂几何结构下的表示能力仍有提升空间。
- **动力学假设限制**：当前方法假设机器人具有完全驱动和平凡动力学（$\|u\|=1$），未在部分可观测或受运动学/动力学约束的任务中验证。

### 关键图表结论

- **Figure 1**：直观展示了仅用$L_E$训练可产生满足局部Eikonal方程但全局错误的次优解，而$L_{TD}$通过强制有限时间步的值一致性找到真值解。
- **Figure 2**：说明混合$L_1/L_\infty$度量如何将圆上测地线嵌入为二维菱形，保留多联通区域中的多重路径结构，避免$L_2$嵌入造成的路径重叠和歧义。
- **Figure 3 + Table 2**：消融实验的定量和定性证据共同验证了$L_E$与$L_{TD}$的互补关系是方法成功的核心，度量学习设计显著优于现有度量表示。
- **Figure 5/8**：真实世界12-DOF双臂机器人橱柜环境中的成功规划（0.1-0.11秒），验证了方法从仿真到真实场景的迁移能力。

## 方法谱系与知识库定位

### 1. 问题瓶颈与核心思路

本文方法 **PTDML** 针对的核心瓶颈是：现有基于物理信息的自监督运动规划方法（以 **NTFields** (Ni et al., 2021) 及其改进版 **P-NTFields** (Ni & Qureshi, 2023a) 为代表）在复杂、杂乱环境中难以同时保持 Eikonal 方程作为最优值函数和测地线距离的关键性质。具体而言，仅依赖 Eikonal 损失 $L_E$ 训练的值函数容易过拟合到局部结构，无法捕捉全局最优值传播（见 Figure 1），导致在狭窄通道和多联通区域中产生次优解甚至规划失败。

PTDML 的核心洞察是将运动规划的行程时间 $T(q_s, q_g)$ 同时解释为：
- 一个具有单位速度约束的最优控制问题的最优值函数，从而可以在有限时间步上施加 Bellman 最优性原理；
- 一个黎曼流形上的测地线距离，从而必须满足非负性、对称性和三角不等式等度量基本性质。

基于这一双重解释，PTDML 引入了三个关键改动：**(1)** 联合优化 Eikonal 损失与时序差分（TD）损失以捕捉全局值传播结构；**(2)** 设计度量学习架构以保证距离函数的基本性质并保留多联通区域中的多重最短路径；**(3)** 采用采样模型预测控制（MPC）进行路径推断以跳出局部最小值。

### 2. 与基线方法的关系

#### 2.1 相对于 NTFields / P-NTFields 的改进

**NTFields** (Ni et al., 2021) 首次将神经距离场引入运动规划，通过因子化形式 $T(q_s, q_g) = \|q_s - q_g\| / \tau(q_s, q_g)$ 参数化行程时间，并仅使用 Eikonal 损失 $L_E$ 进行自监督训练。**P-NTFields** (Ni & Qureshi, 2023a) 在此基础上引入课程学习和粘性 Eikonal 方程以改善训练稳定性。然而，两者存在共同的局限：

| 维度 | NTFields / P-NTFields | PTDML (本文) |
|------|----------------------|-------------|
| 损失函数 | 仅 $L_E$ | $L_E + L_{TD} + L_N$，并以因果权重 $L_C$ 调制 |
| 值函数表示 | 因子化形式，不保证三角不等式 | 度量学习形式 $T = D(f_\theta(q_s), f_\theta(q_g))$，保证度量公理 |
| 推理方式 | 沿值函数负梯度下降 | 采样 MPC，通过 softmax 加权路径 |
| 环境泛化 | 无环境编码（单环境） | PointNext 编码 + 交叉注意力，跨环境泛化 |

消融实验（Figure 3, Table 2）定量验证了这些改进的必要性：移除 TD 损失使迷宫值函数误差从 0.08 升至 0.21；移除 Eikonal 损失则急剧升至 1.13；将本文度量替换为 IQE、PQE、MRN、DN 等替代度量后，误差分别升至 0.32、0.46、0.19 和 0.29，表明本文的混合 $L_1/L_\infty$ 度量更好地保持了测地线性质。

#### 2.2 相对于经典规划方法的定位

- **Fast Marching Method (FMM)** (Sethian, 1996)：直接数值求解 Eikonal 方程，提供真值解，但受维度灾难限制，无法扩展到高维配置空间。PTDML 在 2D 迷宫上将 FMM 作为真值参照（Table 2），但在 7-DOF 和 12-DOF 任务上 FMM 不可行。
- **RRTConnect (RRTC)** (Kuffner & LaValle, 2000) 和 **LazyPRM (L-PRM)** (Bohlin & Kavraki, 2000)：概率完备的采样规划器，在高维空间中仍可使用，但规划时间随维度增长显著（实验中给予 30 秒上限）。PTDML 在 7-DOF 机械臂任务上以 0.03 秒的平均规划时间达到 87.0% 成功率，而 RRTC 需 0.28 秒（成功率 87.5%），L-PRM 需 0.50 秒（成功率 89.6%），表明学习方法在效率上具有显著优势（Table 1）。

#### 2.3 相对于监督学习方法的定位

- **MPNet** (Qureshi et al., 2019) 和 **MPiNet** (Fishman et al., 2023)：基于监督学习，需要大量由经典规划器生成的专家轨迹数据（数据生成时间可达数小时），而 PTDML 仅需距离场和随机采样配置，数据生成仅需数秒到几分钟（Table 4）。在性能上，PTDML 在 Cluttered 3D 已知环境中达到 99.6% 成功率，超过 MPNet 的 98.8%（Table 3）。

#### 2.4 与度量学习和强化学习的关联

PTDML 将行程时间构建为潜在空间中的度量距离 $T(q_s, q_g) = D(f_\theta(q_s), f_\theta(q_g))$，这一思路借鉴了拟度量强化学习（Quasimetric Reinforcement Learning, QRL）的思想（Schaul et al., 2015; Zhang et al., 2020; Bellemare et al., 2019; Wang et al., 2023），但将其从通用 RL 的值函数空间迁移到 Eikonal 方程的解空间。关键创新在于设计了混合 $L_1/L_\infty$ 距离度量 $D(x, y) = \sum_{i=1}^{a} [\max_{1 \leq j \leq b} |x_{i,j} - y_{i,j}|]$，该度量将圆上的测地线映射为二维菱形而非线段（Figure 2），从而在多联通区域中保留多重最短路径的结构信息——这是标准欧氏距离或 $L_2$ 嵌入无法做到的。

### 3. 适用边界与局限

尽管 PTDML 在 2D 到 12-DOF 的多种任务上展现了显著优势，但仍存在以下局限：

1. **局部精度退化**：在迷宫环境的某些局部区域（如右下角），值函数精度仍会出现下降现象（Figure 3），即使整体误差较低（0.08）。这表明模型在复杂几何结构中的全局值传播仍有改进空间。

2. **未知环境泛化衰减**：在 Gibson 数据集上，模型在完全未知环境下的泛化成功率相较于已知环境有所下降（Table 3）。当前使用的 PointNext 编码器可能不足以充分捕获复杂真实场景的几何细节，需要进一步探索更强大的点云编码器（如 Point Transformer）。

3. **动力学假设限制**：当前方法假设机器人具有完全驱动和平凡动力学（$\|u(t)\| = 1$），即速度约束仅为单位范数。在部分可观测或受复杂运动学/动力学约束的任务中，该框架尚未验证。

4. **超参数敏感性**：障碍法向对齐损失 $L_N$ 在狭窄通道中可能不足以平衡目标指向与避障，其超参数 $\lambda_N$ 需要针对每个环境单独调整。因果权重 $\lambda_C$ 的选择也影响值传播的稳定性。

5. **与完备性保证的脱节**：PTDML 使用采样 MPC 进行路径推断，虽然比梯度下降更鲁棒，但本身不具备概率完备性保证。在极端困难的配置空间中，纯学习方法仍可能失败。

### 4. 开放问题

1. **编码器升级**：能否将更强大的点云编码器（如 Point Transformer V2/V3）集成到 PTDML 框架中，以进一步提高在复杂未见环境中的泛化能力？环境编码的质量直接决定了跨场景迁移的上限。

2. **部分可观测与约束扩展**：在部分可观测和随机关节限制的条件下，如何扩展时序差分度量学习框架以保证安全规划？这需要将不确定性量化引入值函数学习。

3. **动态环境适应**：当面临动态障碍物或任务需求变化时，PTDML 能否与在线学习或自适应 MPC 策略结合？当前方法假设静态环境，动态扩展需要重新思考 Bellman 最优性的时间尺度。

4. **混合规划架构**：能否将学到的值函数作为启发式函数嵌入到概率完备的搜索式规划器（如 A* 或 RRT*）中，以同时保证完备性和学习效率？这将是连接学习方法和经典规划理论的重要方向。

5. **理论收敛性分析**：当前工作以实验验证为主，缺乏对组合损失函数 $L = (\lambda_E L_E + \lambda_{TD} L_{TD} + \lambda_N L_N) L_C$ 收敛到真值 Eikonal 解的理论保证。TD 损失的有限时间步离散化误差与神经网络逼近误差之间的定量关系尚不明确。

## 原文 PDF

![[paperPDFs/ICLR_2025/Physics_informed_Temporal_Difference_Metric_Learning_for_Robot_Motion_Planning.pdf]]
