---
title: "Interactive Hair Simulation on the GPU using ADMM"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2023
pdf_ref: paperPDFs/SIGGRAPH_2023/Interactive_Hair_Simulation_on_the_GPU_using_ADMM.pdf
code_link: null
project_link: https://research.nvidia.com/labs/prl/admm_hair/files/editing.mp4
aliases:
- ABGHSDERCF
- IHSGUA
tags:
- SIGGRAPH_2023
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过 ADMM 分解将原始全局问题转化为局部弹性算子、碰撞投影算子和稀疏三对角全局系统，从而利用 GPU 的并行计算能力和高效的三对角求解器。"
primary_logic: "利用 DER 模型的结构特性，将弹性变量 y 和碰撞变量 z 从位置变量 x 分离，使得全局步的线性系统变为三个独立的三对角系统，可通过并行循环约减（PCR）高效求解，在保持物理精度的同时实现实时性能。"
claims:
- "提出的局部-全局求解器利用 GPU 大规模并行能力"
- "全局步解三个独立 SPD 三对角系统，一个坐标轴一个，使用 PCR"
- "采用 Korner 的替代应变度量以提高收敛速度"
- "碰撞检测使用浅层稀疏哈希网格和 18-dops 进行粗剔除"
---

# Interactive Hair Simulation on the GPU using ADMM

> [!tip] 核心洞察
> 利用 DER 模型的结构特性，将弹性变量 y 和碰撞变量 z 从位置变量 x 分离，使得全局步的线性系统变为三个独立的三对角系统，可通过并行循环约减（PCR）高效求解，在保持物理精度的同时实现实时性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于 ADMM 的 GPU 交互式头发模拟 |
| 英文题名 | Interactive Hair Simulation on the GPU using ADMM |
| 会议/期刊 | SIGGRAPH 2023 |
| Links | [paper](https://research.nvidia.com/labs/prl/daviet23/interactivehair2023.pdf) · [Project](https://research.nvidia.com/labs/prl/admm_hair/files/editing.mp4) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | ADMM-based GPU Hair Simulation for Discrete Elastic Rods with Coulomb Friction |
| Dataset | Hairball 16k (proximity-only), Hairball 128k (proximity-only), Long 47k (realistic groom) |

> [!tip] 效果简介
> - Hairball 16k (proximity-only) 上，平均帧时间 (s) 为 0.18，对比 传统 CPU 求解器 (数分钟至数小时)，变化 无定量比较。
> - Hairball 128k (proximity-only) 上，平均帧时间 (s) 为 3.14，对比 传统 CPU 求解器 (约半周)，变化 无定量比较。
> - Long 47k (realistic groom) 上，平均帧时间 (s) 为 2.28。

## 概要

本文提出了一种基于交替方向乘子法（ADMM）的 GPU 大规模并行求解器，用于交互式模拟离散弹性棒（Discrete Elastic Rods, DER）模型下的头发动力学，并支持库仑摩擦接触。核心瓶颈在于：传统 CPU 全局求解器（如 Newton 法）因带状矩阵条件数差和内存访问模式无法充分利用 GPU 并行性，而纯局部求解器（如 XPBD）收敛缓慢，导致高分辨率头发仿真难以满足交互式编辑的实时性需求。

**核心思路**：通过精心设计的 ADMM 分解，将原始隐式时间积分的全局非线性问题拆解为三个可高效并行的子问题——局部弹性算子、碰撞可行投影算子，以及一个稀疏三对角全局线性系统。其中，全局步的关键洞察在于利用 DER 模型的结构特性，将弹性辅助变量 $\mathbf{y}$ 和碰撞辅助变量 $\mathbf{z}$ 从位置变量 $\mathbf{x}$ 中分离，使得全局线性系统退化为三个独立的三对角对称正定系统（每个空间坐标轴一个），从而可通过并行循环约减（Parallel Cyclic Reduction, PCR）在 GPU 上高效求解。该方法在保持 DER 物理精度的同时，实现了实时乃至交互式的性能。

**主要结果**：在 16k 根发丝的 Hairball 场景中，平均帧时间仅为 0.18 秒；在 128k 根发丝的规模下，帧时间为 3.14 秒，相比传统 CPU 求解器（需数分钟至数小时）实现了数量级的加速。在包含 47k 根发丝的真实发型（Long 47k）上，帧时间为 2.28 秒，证明了该方法在复杂发型交互式编辑场景中的实用性。数值验证实验表明，求解器能够精确复现 Romero 等人（2021）提出的悬臂梁、弯扭耦合和粘滑摩擦等标准测试的理论结果。

**方法定位**：该方法属于基于物理的头发模拟中“局部-全局混合求解器”这一技术路线，是对 Projective Dynamics 的 ADMM 推广（Narain 等, 2016）在 DER 模型上的系统化延伸。其关键改进包括：采用 Korner 等（2021）的非发散弯曲应变度量以加速收敛；将全局矩阵从带宽约 10 的带状结构简化为三对角结构；以及设计了混合 Gauss-Seidel/Jacobi 并行策略的摩擦接触可行投影。

### 问题背景

数字角色中的头发模拟是视觉计算领域的长期挑战。一根头发可以被建模为一根细长的弹性棒，其力学行为由**离散弹性棒（Discrete Elastic Rods, DER）**模型描述，该模型能够捕捉拉伸、弯曲和扭转三种基本形变模式，并支持库仑摩擦接触。然而，要在交互式应用中实现高分辨率、物理精确的头发仿真，面临一个根本性矛盾：**物理精度要求全局耦合求解，而交互性要求每帧计算时间在毫秒量级**。

传统 CPU 求解器通常采用 Newton 法进行全局求解，但 DER 模型产生的系统矩阵为带宽约 10 的带状矩阵，条件数较差，且内存访问模式无法充分利用 GPU 的大规模并行计算能力。这导致即使是中等规模的头发场景（数万根发丝），单帧计算也需要数分钟甚至数小时。另一方面，纯局部求解器（如 XPBD）虽然并行性好，但收敛速度慢，需要大量迭代才能达到可接受的精度，同样难以满足实时编辑的需求。

### 现有方法缺口

现有方法在求解策略上存在明显的性能瓶颈：

1. **全局求解器的 GPU 适配困难**：Newton 法及其变体需要组装和求解一个耦合的全局线性系统。DER 模型的系统矩阵虽然是稀疏的，但其带宽结构和间接寻址模式阻碍了 GPU 上的高效并行化。单精度浮点运算在这种病态系统上容易导致数值不稳定，进一步限制了 GPU 的适用性。

2. **局部求解器的收敛速度不足**：以 Projective Dynamics（PD）和 XPBD 为代表的局部-全局交替方法虽然天然适合 GPU 并行，但其全局步的收敛速度受限于交替方向乘子法（ADMM）的原始形式，在头发这种高刚度比（弯曲刚度与拉伸刚度之比可达 $10^4$ 量级）的材料上表现尤为缓慢。

3. **碰撞处理的并行化挑战**：库仑摩擦接触引入了非光滑的互补性约束。在 CPU 上，这类约束通常通过内嵌的互补求解器处理，但将其高效映射到 GPU 的大规模并行架构上仍然是一个开放问题。

### 本文动机

本文的核心动机是**打破头发模拟中物理精度与交互性能之间的权衡**。具体而言，我们观察到 DER 模型的一个关键结构特性：其弹性变量（弯曲和拉伸）和碰撞变量可以从位置变量中分离出来。这一观察启发我们设计一种精心构造的 ADMM 分解策略，将原始的全局问题转化为三个独立可并行的子问题：

- **局部弹性步**：每个边对独立求解弯曲和拉伸能量的 proximal 算子，天然适合 GPU 大规模并行。
- **碰撞投影步**：将中间位置投影到满足摩擦接触约束的可行集，通过混合 Gauss-Seidel/Jacobi 策略实现高效并行。
- **全局三对角步**：利用 DER 模型的链式拓扑结构，将全局线性系统化为三个独立的三对角系统（每个空间坐标轴一个），可通过并行循环约减（Parallel Cyclic Reduction, PCR）高效求解。

这种分解使得整个求解器能够**充分利用现代 GPU 的大规模并行计算能力**，同时在单精度浮点运算下保持数值稳定性。最终目标是实现**实时交互式物理编辑**——允许艺术家在模拟过程中直接选择、拖拽、修剪发束，并即时看到符合物理规律的结果，如图 1 所示的 86,000 根发束的实时编辑会话。

### 核心贡献预览

本文的主要贡献可概括为：

- 提出了一种基于 ADMM 的局部-全局求解器，专为带库仑摩擦的 DER 头发模拟设计，能够充分利用 GPU 的大规模并行能力。
- 通过引入 Korner 等人（2021）的非发散应变度量替代传统 Bergou 等人（2008）的应变度量，显著提升了 ADMM 的收敛速度。
- 设计了一种混合 Gauss-Seidel/Jacobi 的碰撞求解策略，在保持并行性的同时改善了接触求解的收敛性。
- 实现了完整的实时交互式头发编辑系统，支持选择、拖拽、修剪等操作，性能较传统 CPU 求解器提升数个数量级。

## 核心方法与创新机理

本文的核心贡献在于**将 ADMM（交替方向乘子法）分解策略系统性地应用于带库仑摩擦的离散弹性棒（DER）模型**，从而将原本难以在 GPU 上高效并行求解的全局隐式时间积分问题，转化为一系列高度并行友好的子问题。这一分解直接回应了传统方法的根本瓶颈：**CPU 全局求解器（如 Newton 法）因带状矩阵条件数差和内存访问模式无法充分利用 GPU 并行性，而纯局部求解器（如 XPBD）收敛速度慢，导致高分辨率头发仿真无法满足交互式编辑需求**。

### 关键创新点

**1. 求解策略：从全局耦合到 ADMM 局部-全局分解**

传统方法（Newton 全局求解器或 XPBD 局部求解器）在 GPU 并行性和收敛速度之间难以兼顾。本文通过精心设计的 ADMM 分解，将原始增量问题中的变量进行分离：
- 引入辅助变量 $\mathbf{y}$ 分离弹性算子，使其独立于位置变量 $\mathbf{x}$
- 引入辅助变量 $\mathbf{z}$ 分离碰撞约束，将摩擦接触投影与弹性求解解耦

这一分解使得每个 ADMM 迭代中的各子步骤均可充分利用 GPU 的大规模并行能力，同时保持单精度友好的数值特性。

**2. 全局矩阵结构：从带状矩阵到三对角系统**

这是本方法性能突破的核心因果机制。传统 DER 模型的全局步通常产生带宽约为 10 的带状矩阵，不利于 GPU 上的高效求解。本文利用 DER 模型的结构特性——弹性变量 $\mathbf{y}$ 和碰撞变量 $\mathbf{z}$ 从位置变量 $\mathbf{x}$ 分离后，全局步的线性系统 $\hat{M} \Delta \mathbf{x} = \hat{\mathbf{f}}$ 退化为**三个独立的三对角对称正定（SPD）系统**，每个对应一个空间坐标轴：

$$ \hat{M}_{|k} \Delta \mathbf{x}_{|k} = \hat{\mathbf{f}}_{|k}, \quad k = 1, 2, 3 $$

这三个系统可通过**并行循环约减（PCR）**在 GPU 上高效求解，在保持物理精度的同时实现实时性能。

**3. 弹性应变度量：从原始度量到非发散度量**

本文采用 **Körner 等（2021）** 提出的替代应变度量，替代 **Bergou 等（2008）** 的原始度量。实验观察表明，非发散弯曲能量在 ADMM 框架下表现出更快的收敛速度，这一选择对所有示例均有效。

**4. 碰撞求解：从 Newton 内嵌互补到混合 Gauss-Seidel/Jacobi 并行投影**

传统方法将碰撞作为 Newton 求解器的内嵌互补约束，难以并行化。本文基于 ADMM 的可行投影框架，采用**启发式分批混合策略**：将接触点分为少量批次（实现中为 8 个），批次间以 Gauss-Seidel 方式顺序处理，批次内则以完全并行的 Jacobi 方式求解。这一策略相对于纯 Jacobi 方法显著改善了收敛性。

### 方法局限性

尽管取得了显著的性能突破，该方法仍存在以下局限：
- ADMM 的收敛理论尚不完善，约束权重（如 $w^0=25$）依赖启发式选择，缺乏自动调优机制
- 求解器在非均匀棒（边长或弹性模量差异大）以及各向异性材料上收敛速度较慢
- 碰撞处理基于接触点位于中心线的假设，忽略扭转产生的接触扭矩，可能不适用于极粗发丝或大扭转场景
- 无法提供严格的穿透保证，与基于障碍函数的方法（如 IPC）相比安全性较低

本文提出了一种基于交替方向乘子法（ADMM）的 GPU 头发模拟框架，其核心思想是将离散弹性棒（DER）模型与库仑摩擦的隐式时间积分增量问题分解为一系列可在 GPU 上大规模并行的子问题。整个时间步的求解流程如 **Algorithm 1** 所示，形成了一条清晰的“检测-局部求解-全局求解-更新”的流水线。

### 输入与输出

**输入**：当前时间步 $t$ 的头发状态，包括所有顶点的位置 $\mathbf{x}^t$、扭转角 $\theta^t$、速度 $\mathbf{v}^t$ 和角速度 $\omega^t$，以及发束的附着约束和外部力场（如重力、空气阻力）。

**输出**：下一时间步 $t+1$ 的状态 $(\mathbf{x}^{t+1}, \theta^{t+1}, \mathbf{v}^{t+1}, \omega^{t+1})$，满足弹性力学方程和摩擦接触约束。

### 核心流水线

框架以 ADMM 迭代循环为核心，每次迭代依次执行以下模块：

1. **碰撞检测**：基于浅层稀疏哈希网格和 18-DOPs 包围体进行粗剔除，执行邻近碰撞检测和可选的连续碰撞检测，构建接触约束集。此模块为后续的可行投影提供约束输入。

2. **局部弹性求解**：对每对相邻边（即每个内部顶点对应的 6 自由度变量 $\mathbf{y}_i$）独立求解弯曲和拉伸能量的 proximal 算子，得到更新的弹性辅助变量 $\mathbf{y}$。该步骤完全解耦，天然适合 GPU 并行。

3. **可行投影**：将中间位置投影到满足摩擦接触约束的可行集上，得到更新的碰撞辅助变量 $\mathbf{z}$。接触求解采用混合 Gauss-Seidel/Jacobi 策略：将接触点分为 8 个批次按 Gauss-Seidel 顺序处理，批次内部则完全 Jacobi 并行。

4. **拉格朗日乘子更新**：沿残差方向更新对偶变量 $\lambda_y$ 和 $\lambda_z$，驱动 ADMM 收敛。

5. **全局三对角求解**：组装并求解三个独立的三对角对称正定（SPD）系统，每个对应一个空间坐标轴，通过并行循环约减（PCR）高效求解，得到位置更新 $\Delta\mathbf{x}$。这是整个框架中唯一需要全局通信的步骤，但其三对角结构使得求解极为高效。

6. **扭转牛顿步**：对扭转变量 $\theta$ 执行一次牛顿步，同样组装并求解一个三对角系统。

7. **DER 参考系更新**：更新离散弹性棒的参考系和材料系，为下一迭代或下一时间步准备几何信息。

### 模块间的数据流

ADMM 分解的关键在于引入辅助变量 $\mathbf{y}$ 和 $\mathbf{z}$，将原本耦合的全局问题解耦：

- **$\mathbf{y}$** 承接弹性算子，通过约束 $\mathbf{y} \approx B\mathbf{x}$ 与位置变量 $\mathbf{x}$ 关联，其中 $B$ 是从顶点位置到边向量的线性映射。
- **$\mathbf{z}$** 承接碰撞投影算子，通过约束 $\mathbf{z} \approx \mathbf{x}$ 与位置变量 $\mathbf{x}$ 关联。

局部弹性求解和可行投影分别更新 $\mathbf{y}$ 和 $\mathbf{z}$，而全局三对角求解则综合两者的反馈（通过增广拉格朗日项中的 $W_y(\mathbf{y} - B\mathbf{x})$ 和 $W_z(\mathbf{z} - \mathbf{x})$）来更新 $\mathbf{x}$。这种分离使得每个子问题都能充分利用 GPU 的并行能力：局部步骤是完全并行的，全局步骤则退化为三个独立的三对角系统，避免了传统牛顿求解器中带状矩阵条件数差和内存访问模式不佳的问题。

### 收敛与迭代

ADMM 迭代在每个时间步内执行固定次数（文中典型设置为 10-20 次），无需检测收敛条件。约束权重 $W_y$ 和 $W_z$ 的选择基于启发式规则（如弹性约束权重取接近约束有效刚度的值，碰撞约束权重 $w^0=25$），这些权重直接影响收敛速度，但目前缺乏自动调优机制。

### 问题形式化：增量能量最小化

每时间步采用后向欧拉积分，待求解的增量问题为在附着约束和 Coulomb 摩擦接触约束下最小化弹性势能与外部势能之和。令 $\mathbf{x}$ 为顶点位置向量，$\theta$ 为扭转角向量，则目标函数为：

$$
\min_{(\mathbf{x},\theta) \in \mathcal{A}, (H\mathbf{x}+\mathbf{u}^{\mathrm{kin}},\mathbf{r}) \in C_{\mu,\mathbf{n}}} \mathcal{E}_s(\mathbf{x}) + \mathcal{E}_b(\mathbf{x},\theta) + \mathcal{E}_e(\mathbf{x},\theta) \tag{1}
$$

其中 $\mathcal{E}_s$ 为拉伸能量，$\mathcal{E}_b$ 为弯曲能量，$\mathcal{E}_e$ 为包含惯性和空气阻力的外部势能。约束集 $\mathcal{A}$ 编码附着条件，$C_{\mu,\mathbf{n}}$ 编码摩擦接触条件。

**拉伸能量**定义在每条边 $j$ 上：

$$
\mathcal{E}_{s,j} := \frac{E_s}{2} A \overline{e_j} \varepsilon_j^2
$$

其中 $E_s$ 为拉伸模量，$A$ 为截面积，$\overline{e_j}$ 为边 $j$ 的静止长度，$\varepsilon_j$ 为拉伸应变。

**弯曲能量**定义在每个内部顶点 $i$ 上：

$$
\mathcal{E}_{b,i} := \frac{E_b}{2} (\kappa_i - \bar{\kappa}_i)^T \frac{K}{\overline{v}_i} (\kappa_i - \bar{\kappa}_i)
$$

其中 $E_b$ 为弯曲模量，$\kappa_i$ 为当前曲率，$\bar{\kappa}_i$ 为自然曲率，$K$ 为截面惯性矩张量，$\overline{v}_i$ 为顶点 $i$ 的 Voronoi 域长度。

> **关键设计**：论文采用 Korner 等人（2021）提出的非发散弯曲能量度量替代 Bergou 等人（2008）的原始应变度量，实验观察到其收敛速度更快。

---

### ADMM 分解：分离弹性、碰撞与全局耦合

核心瓶颈在于原始问题中弹性、碰撞和全局惯性耦合导致难以 GPU 并行化。论文通过 ADMM 引入辅助变量 $\mathbf{y}$（弹性变量）和 $\mathbf{z}$（碰撞变量），将问题分解为可并行的局部步和结构简单的全局步。

**增广拉格朗日**定义为：

$$
\mathcal{L}(\mathbf{x},\theta,\mathbf{y},\mathbf{z},\lambda_y,\lambda_z) := \mathcal{E}_s(\mathbf{y}) + \mathcal{E}_b(\mathbf{y},\theta) + \mathcal{E}_e(\mathbf{x},\theta) + \lambda_y^T W_y (\mathbf{y} - B\mathbf{x}) + \lambda_z^T W_z (\mathbf{z} - \mathbf{x}) + \frac{1}{2} \| \mathbf{y} - B\mathbf{x} \|_{W_y}^2 + \frac{1}{2} \| \mathbf{z} - \mathbf{x} \|_{W_z}^2 \tag{2}
$$

其中 $B$ 将顶点位置映射到边对变量，$W_y$、$W_z$ 为约束权重矩阵，$\lambda_y$、$\lambda_z$ 为拉格朗日乘子。

每个 ADMM 迭代依次执行以下子步：

1. **局部弹性求解**：固定 $\mathbf{x}$，对每个边对独立求解 $\mathbf{y}$ 的 proximal 算子
2. **可行投影**：固定 $\mathbf{x}$，将 $\mathbf{z}$ 投影到满足摩擦接触约束的可行集
3. **拉格朗日乘子更新**：沿残差方向更新 $\lambda_y$、$\lambda_z$
4. **全局位置求解**：固定 $\mathbf{y}$、$\mathbf{z}$，求解 $\mathbf{x}$ 的线性系统
5. **扭转牛顿步**：固定 $\mathbf{x}$，对 $\theta$ 执行一次牛顿迭代

---

### 全局三对角求解：从带状矩阵到独立三对角系统

全局步的核心贡献在于将传统 DER 求解器中带宽约 10 的带状矩阵转化为三个独立的三对角系统。通过将外部势能 $\mathcal{E}_e$ 中的惯性和空气阻力项与 ADMM 增广项合并，系统矩阵 $\hat{M}$ 具有以下结构：

$$
\hat{M} \Delta \mathbf{x} = \hat{\mathbf{f}}
$$

其中 $\hat{M} := \left[ \Pi_{\mathcal{R}^\perp} M \Pi_{\mathcal{R}^\perp}^T + \Pi_{\mathcal{R}} \Pi_{\mathcal{R}}^T \right]$，$M$ 为质量和阻尼矩阵，$\Pi_{\mathcal{R}}$ 为附着约束的投影算子。

**关键性质**：由于 DER 模型的一维拓扑结构，$\hat{M}$ 在按坐标轴分离后变为三个独立的对称正定三对角系统，每个维度一个：

$$
\hat{M}_{|k} \Delta \mathbf{x}_{|k} = \hat{\mathbf{f}}_{|k}, \quad k = 1, 2, 3
$$

这三个系统可通过**并行循环约减**高效求解，充分利用 GPU 的大规模并行能力。

---

### 局部弹性求解：边对独立的 Gauss-Newton 步

局部步对每个边对 $\mathbf{y}_i \in \mathbb{R}^6$ 独立求解以下 proximal 算子：

$$
\min_{\mathbf{y}_i \in \mathbb{R}^6} \mathcal{E}_{b,i}(\mathbf{y}_i) + \mathcal{E}_{s,i}(\mathbf{y}_i) + \frac{W_{y,i}}{2} \| (B\mathbf{x})_i - \lambda_{y,i} - \mathbf{y}_i \|^2
$$

为避免弯曲和拉伸分离导致的零模问题，论文将二者合并求解。采用单步 Gauss-Newton 近似，每个边对需求解一个 $6 \times 6$ 线性系统，使用单精度 LDLT 分解（无需数值 pivoting），可在 GPU 上完全并行。

**应变率阻尼**以拉伸为例：

$$
\mathcal{D}_{s,i}(\mathbf{y}_i) := \frac{\tau A E_s}{4 \Delta_t} \left( \overline{e_{i-1}} (\varepsilon(\mathbf{e}_{i-1}) - \varepsilon_{i-1}^t)^2 + \overline{e_i} (\varepsilon(\mathbf{e}_i) - \varepsilon_i^t)^2 \right)
$$

---

### 碰撞处理：混合 Gauss-Seidel/Jacobi 可行投影

碰撞检测采用**浅层稀疏哈希网格**加速邻近查询，**18-dops** 进行粗剔除。接触求解将碰撞分为少量批次（实现中为 8 批），批次间以 Gauss-Seidel 方式串行处理以保证收敛性，批次内以完全并行的 Jacobi 方式求解。

接触问题的离散形式为寻找 $\mathbf{z}$、$\mathbf{u}$、$\mathbf{r}$ 满足：

$$
\begin{cases}
W_z \mathbf{z} = W_z (\mathbf{x} - \lambda_z) + H \mathbf{r}^T \\
\mathbf{u} = H \mathbf{z} + \mathbf{u}^{\mathrm{kin}} \\
\text{接触互补条件与 Coulomb 摩擦锥约束}
\end{cases}
$$

顶点位置更新使用 Delassus 算子的对角近似：

$$
D := \mathrm{diag}\left( \sum_{i \in \mathcal{I}_c} h_{c,i}^2 / W_{z,i} \right)_{c=1\ldots n}
$$

---

### 扭转牛顿步

在每次 ADMM 迭代中，固定位置 $\mathbf{x}$ 后对扭转变量 $\theta$ 执行一次牛顿步，求解另一个三对角系统：

$$
\frac{\partial^2 (\mathcal{E}_b + \mathcal{E}_s)}{\partial \theta^2} \Delta \theta = -\frac{\partial (\mathcal{E}_b + \mathcal{E}_s)}{\partial \theta}
$$

该系统的三对角结构同样可通过 PCR 高效求解。

---

### 约束权重选取

弹性约束权重 $W_y$ 选取为接近约束的有效刚度，以保证数值稳定性。碰撞约束权重 $W_z$ 依赖启发式选择（如 $w^0=25$），目前缺乏自动调优机制，这也是论文指出的局限性之一。

## 实验与关键发现

### 数值验证

为验证模拟器的物理正确性，本文首先复现了 **Romero 等 (2021)** 提出的三个标准数值实验：悬臂梁、弯扭耦合和粘滑摩擦。在悬臂梁实验中，杆长从 0.5 cm 到 128 cm 变化，跨越 7 个数量级的无量纲参数 Γ；弯扭实验的自然曲率从 0.175 到 2 cm⁻¹，扭转角 φ 从 0.25π 到 25π，杆长范围 0.4 到 444 cm；粘滑实验使用 10 cm 长的杆。所有测试均采用 2.5 mm 的边分辨率，每根杆至少 16 条边，物理参数代表真实人类头发（半径 R=0.05 mm，密度 ρ=1300 kg·m⁻³，弯曲模量 E_b=3 GPa，泊松比 ν=0.45）。模拟器在所有实验中均成功复现理论结果（**Figure 2**），验证了 DER 模型和 Coulomb 摩擦接触求解的正确性。

![[assets/figures/papers/paper_list_l50_https_research_nvidia_com_labs_prl_daviet23_interactivehair2023_pdf/figures/004_Figure_2.jpg]]
*Figure 2: Results for the numerical verification of our simulator on the cantilever (left), bend–twist (middle) and stick–slip (right) experiments from Romero et al. [2021]. Physical parameters in these tests are representative of human hair: 𝑅 = 0.05mm, $\rho = \mathbf { 1 3 0 0 } \mathbf { k g . m ^ { - 3 } }$ , \| $\mathbf { g }$ \| = $\mathbf { 9 . 8 1 m . s ^ { - 1 } } , E _ { b }$ = 3 $\mathbf { G P a } , \nu = \mathbf { 0 . 4 5 }$ . All results are shown for a resolution of 2.5mm per edge, with a minimum of 16 edges per rod. For the cantilever test, we varied the length from 0.5cm to 128cm to span 7 orders of magnitude of Γ. For the bend-twist test, we varied the natural curvature from 0.175 to 2 ~ $\ma$...

![[assets/figures/papers/paper_list_l50_https_research_nvidia_com_labs_prl_daviet23_interactivehair2023_pdf/figures/005_Figure.jpg]]

### 主要性能结果

**Table 1** 汇总了各测试场景的性能统计。核心结果如下：

- **Hairball 16k**（仅邻近碰撞检测）：平均帧时间 **0.18 s**，其中碰撞检测占 49%，可行投影占 38%，全局三对角求解仅占 1.3%。
- **Hairball 128k**（仅邻近碰撞检测）：平均帧时间 **3.14 s**。作为参照，传统 CPU 求解器处理同等规模需要约半周时间，本文方法实现了数量级的加速。
- **Long 47k**（真实发型，含连续碰撞检测）：平均帧时间 **2.28 s**，计算时间主要分布在碰撞检测（37%）、可行投影（27%）和局部弹性求解（15%）。

所有测试均在 GPU 上以单精度浮点执行，求解器在均质各向同性材料上表现最优。**Figure 4** 进一步展示了 Long 10k、Long 47k 和 Curly 24k 三个场景的模拟截图及前 20 帧的计算时间分布，直观反映了不同模块的相对开销。

### 消融分析

#### 连续碰撞检测的影响

**Figure 3** 对比了 Hairball 16k 和 128k 场景在有无连续碰撞检测下的最终状态。跳过连续碰撞检测会导致发丝在高速冲击阶段发生穿透和纠缠，这些错过的碰撞在后续阶段因发丝维持邻近关系而无法自行分离，最终呈现更结块的聚集状态。启用连续碰撞检测可有效避免此问题，但会增加约 15%–25% 的计算开销（见 Table 1 中 Hairball 16k 和 128k 的 proximity-only 与 continuous-time 变体对比）。

#### 混合 Gauss-Seidel/Jacobi 接触求解

可行投影步骤中，接触求解采用启发式分批策略：将接触约束分为 8 个批次，批次间以 Gauss-Seidel 方式串行处理，批次内以完全并行的 Jacobi 方式求解。实验表明，这种混合策略相对于纯 Jacobi 求解改善了收敛性，在保持 GPU 并行度的同时减少了迭代次数。该设计的有效性在 Hairball 128k 的高密度接触场景中尤为突出。

#### 应变度量选择

弯曲能量采用 **Korner 等 (2021)** 的非发散应变度量，而非 Bergou 等 (2008) 的原始度量。实际观察表明，该替代度量在 ADMM 迭代中表现出更快的收敛速度，被所有示例采用。

### 失败模式与局限性

1. **非均匀材料的收敛退化**：当发丝边长或弹性模量差异较大时，ADMM 迭代的收敛速度显著下降。这是因为全局三对角系统的条件数受材料非均匀性影响，而约束权重 $W_y$ 的启发式选择（如 $w^0=25$）缺乏自适应性。

2. **碰撞处理的简化假设**：接触求解基于接触点位于中心线的假设，忽略扭转产生的接触扭矩。在极粗发丝或大扭转场景下，这一简化可能导致接触响应的物理精度下降。

3. **穿透保证缺失**：与基于障碍函数的方法（如 IPC）不同，本求解器无法提供严格的穿透保证。在极端变形或高速碰撞下，仍可能出现穿透。

4. **物理效果覆盖不足**：当前框架不支持头发产品效果、与空气的双向耦合、以及与软体或刚体的双向耦合，限制了其在完整虚拟角色管线中的直接应用。

5. **交互编辑工具尚处概念验证阶段**：程序化编辑功能（如 **Figure 5** 所示的生长、卷曲、修剪和外部加速度动画）虽能从一个输入发型生成变体，但缺乏成熟的用户交互设计（如触觉反馈、智能选择），距离实用美术工具仍有差距。

![[assets/figures/papers/paper_list_l50_https_research_nvidia_com_labs_prl_daviet23_interactivehair2023_pdf/figures/003_Figure.jpg]]
*Figure: Gravito-bending parameter \Gamma = 4 \frac { \rho g L ^ { 3 } } { E _ { b } R ^ { 2 } } Curvature parameter { \sqrt [ 3 ] { \Gamma } } / \varphi Relative vertical displacement \varepsilon _ { y }*

![[assets/figures/papers/paper_list_l50_https_research_nvidia_com_labs_prl_daviet23_interactivehair2023_pdf/figures/002_Table_1.jpg]]
*Table 1: Performance statistics*

## 定位与知识库关联

### 方法溯源与谱系定位

本工作位于**基于物理的弹性杆模拟**与**GPU加速交互式头发仿真**的交叉点，其核心求解器可视为两条技术路线的融合与突破：

**离散弹性杆（DER）模型线**：该线源自Bergou等人（2008）对Kirchhoff杆理论的离散化，将头发建模为具有拉伸、弯曲和扭转自由度的弹性杆。Romero等人（2021）进一步引入了库仑摩擦接触的隐式积分框架，但依赖CPU上的Newton型全局求解器，导致高分辨率模拟耗时数分钟至数小时。本文继承了DER模型，但采用了Körner等人（2021）提出的非发散弯曲应变度量，以改善ADMM迭代的收敛速度。

**交替方向乘子法（ADMM）分解线**：Narain等人（2016）提出了Projective Dynamics的ADMM推广，将隐式时间积分分解为局部投影和全局线性求解。本文将该思想创造性地应用于DER模型，但面临关键挑战：DER的全局矩阵原本是带宽约10的带状矩阵，条件数差且无法直接利用GPU的三对角求解器。作者通过精心设计的变量分离——将弹性变量 $\mathbf{y}$ 和碰撞变量 $\mathbf{z}$ 从位置变量 $\mathbf{x}$ 解耦——使得全局步的线性系统退化为三个独立的三对角对称正定系统，每个对应一个空间坐标轴。这一结构特性使并行循环约减（PCR）求解器得以高效运行，是本文区别于Narain等人框架的核心创新。

**碰撞处理线**：在接触求解方面，本文采用基于ADMM的可行投影，将摩擦接触约束转化为局部投影子问题。为平衡并行性与收敛性，作者将接触点启发式地分为8个批次，批次间采用Gauss-Seidel顺序处理，批次内采用完全并行的Jacobi方式求解。碰撞检测则使用浅层稀疏哈希网格和18-dops包围体进行粗剔除，属于空间哈希加速结构的标准实践。

### 适用边界

**材料同质性与几何均匀性**：求解器在均质各向同性材料上性能最优。当发丝间的边长或弹性模量差异显著时，ADMM的收敛速度会明显下降，因为约束权重 $W_y$ 的选择依赖于局部有效刚度的启发式估计，缺乏对非均匀性的自适应调节。

**接触假设**：碰撞处理基于“接触点位于中心线上”的假设，忽略扭转产生的接触扭矩。这意味着该求解器可能不适用于极粗发丝（如动物鬃毛）或大扭转场景，因为扭转-接触耦合效应在这些情况下不可忽略。

**物理效应的覆盖范围**：当前框架不支持真实头发产品效果（如发胶、摩丝的粘弹性行为）、头发与空气的双向流固耦合，以及头发与软体或刚体的双向耦合。这些效果的缺失限制了其在电影级视觉特效中的直接应用。

**穿透保证**：与基于障碍函数的方法（如IPC）不同，本文的ADMM碰撞投影无法提供严格的穿透保证。作者明确指出，在高速冲击阶段，即使启用连续碰撞检测，仍可能出现穿透，且一旦发丝纠缠，后期难以分离。

### 局限与开放问题

**算法收敛性**：ADMM的收敛理论尚不完善，约束权重（如 $w^0=25$）依赖启发式选择，缺乏自动调优机制。在非均匀材料或大变形场景下，迭代次数可能显著增加，影响交互式编辑的帧率稳定性。

**用户交互成熟度**：论文展示的物理梳理编辑工具（选择、拖拽、修剪）仅为概念验证，缺乏触觉反馈、智能选择、撤销/重做等成熟交互功能，距离实际美术生产流程仍有距离。

**开放问题**：
1. **无穿透保证的融合**：能否将本求解器与IPC的时间步钳位思想结合，在保持GPU并行优势的同时提供无穿透保证？
2. **自适应预处理**：是否可以引入基于模型的自适应约束权重或预处理技术来加速ADMM在不同材料参数下的收敛？
3. **复杂物理效应的GPU化**：如何高效地将头发产品、空气动力学或双向耦合等效果纳入这种GPU求解框架，同时不破坏三对角全局步的结构优势？
4. **交互设计的系统化**：交互式物理发型设计的用户界面和交互范式的关键挑战是什么？如何将美术师的直觉操作映射到物理参数空间？
5. **数据驱动的加速**：能否利用深度学习（如神经插值或潜空间模拟）进一步加速模拟或辅助美术编辑，例如从少量模拟导丝插值出完整发型？

## 原文 PDF

![[paperPDFs/SIGGRAPH_2023/Interactive_Hair_Simulation_on_the_GPU_using_ADMM.pdf]]
