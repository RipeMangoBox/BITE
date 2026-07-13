---
title: CHOICE Coordinated Human Object Interaction in Cluttered Environments for Pick and Place Actions
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/CHOICE_Coordinated_Human_Object_Interaction_in_Cluttered_Environments_for_Pick_and_Place_Actions.pdf
project_link: null
code_link: null
aliases:
- CCHOICEPPA
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过层次化目标驱动框架，将抽象的用户指令转化为双手关键帧调度、隐式时间-到达场轨迹规划和频率域深度相位控制，从而在保证无碰撞的同时生成平滑且自适应的全身交互运动。
primary_logic: 将手部抓放运动建模为各向异性水平集传播过程，利用隐式时间-到达场的梯度实现可泛化的轨迹规划；同时，基于DeepPhase的线性动力学模型与Kalman滤波相结合，能够有效平滑离散子任务之间的相位目标过渡，保留高频运动细节。
claims:
- 系统将交互合成建模为层次化目标驱动任务，分解为双手调度、轨迹规划和控制子模块。
- 隐式时间-到达场轨迹规划器在手-物交互轨迹上比cuRobo实现低11%的Fréchet距离（139 vs 157）。
- 基于Kalman滤波的深度相位控制器显著降低了运动不平滑度（5.94 vs 6.54 cm/s²）和脚滑（6.17 vs 7.22 cm/s）。
- 三通道隐式场设计在场景泛化测试中达到98.8%的成功率和最高的安全距离（8.66 cm）。
---

# CHOICE Coordinated Human Object Interaction in Cluttered Environments for Pick and Place Actions

> [!tip] 核心洞察
> 将手部抓放运动建模为各向异性水平集传播过程，利用隐式时间-到达场的梯度实现可泛化的轨迹规划；同时，基于DeepPhase的线性动力学模型与Kalman滤波相结合，能够有效平滑离散子任务之间的相位目标过渡，保留高频运动细节。

| 字段 | 内容 |
|------|------|
| 中文题名 | CHOICE：杂乱环境下协调人-物交互的抓放动作系统 |
| 英文题名 | CHOICE Coordinated Human Object Interaction in Cluttered Environments for Pick and Place Actions |
| 会议/期刊 | arXiv 2024 |
| Links |  [paper](https://arxiv.org/abs/2412.06702)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | CHOICE |
| Dataset | Pick-and-place in cluttered scenes |

> [!tip] 效果简介
> - Pick-and-place in cluttered scenes (full-body motion quality) 上，Fréchet distance (↓) 139 vs 157 (cuRobo traj.) (-11%)。
> - 同上 上，Unsmoothness (cm/s²) (↓) 5.94 vs 6.54 (-9.2%)；Sliding (cm/s) (↓) 6.17 vs 7.22 (-14.5%)；EE RMSC (cm⁻¹) (↓) 0.0408 vs 0.0725 (-43.7%)。

## 概要

杂乱环境下的抓放操作是具身智能体执行日常任务的基础能力，但现有工作主要聚焦于开放空间中的单步抓取，难以处理多步骤交互（如打开容器、移除障碍物）所要求的双手协调、无碰撞轨迹规划以及离散子任务间的平滑过渡。**CHOICE** 系统将交互合成分解为层次化目标驱动任务，通过双手调度器（Bimanual Scheduler）将抽象的用户指令转化为双手关键帧序列，利用隐式神经时间-到达场（Implicit Neural Trajectory Planner, INTP）生成可泛化的无碰撞手部轨迹，并基于 DeepPhase 线性动力学模型与 Kalman 滤波实现相位目标的平滑过渡，从而在保留高频运动细节的同时生成自适应的全身交互运动。

核心实验结果表明：INTP 在手-物交互轨迹上的 Fréchet 距离相比 **cuRobo**（Sundaralingam et al., ICRA 2023）降低 11%（139 vs 157）；基于 Kalman 滤波的深度相位控制器使运动不平滑度降低 9.2%（5.94 vs 6.54 cm/s²）、脚滑降低 14.5%（6.17 vs 7.22 cm/s）；三通道隐式场设计在场景泛化测试中达到 98.8% 的成功率与最高的安全距离（8.66 cm）。系统在多样化的杂乱厨房场景中展现了协调的双手交互能力，但其全身碰撞避免、对未见容器结构的泛化以及 3D 感知导航仍存在局限。

### 问题场景：杂乱环境下的全身协调交互

在复杂的室内环境中执行抓取和放置（pick-and-place）任务，是人类日常活动中最常见但也最具挑战性的交互形式之一。这类任务往往不是简单的“伸手—抓取—放置”的单步操作，而是包含多个子任务的序列化过程：用户可能需要先打开容器、移除遮挡物、调整物体姿态，再完成最终的抓取与放置。图 1 展示了这类任务的典型场景——在杂乱的厨房环境中，角色需要双手协作完成从柜中取物、避让障碍物、将物品放置到指定位置等一系列动作。

这一问题的核心挑战在于**多步骤交互的层次化协调**。具体而言，系统需要同时解决三个层面的难题：

1. **双手调度**：在杂乱场景中，两只手需要被分配不同的子任务（如一手扶住容器，另一手取物），且这些子任务之间存在时序依赖和空间约束。
2. **无碰撞轨迹规划**：手部在接近和离开目标物体时，需要避开场景中的障碍物和其他物体，而物体的几何形状和布局在不同场景中差异巨大。
3. **全身运动合成**：手部轨迹的变化必须与身体的其他部位（躯干、下肢）自然协调，生成平滑、无滑步的全身运动。

### 现有方法的缺口

现有工作在上述三个层面各自取得了进展，但缺乏一个能够将它们统一起来的框架：

**轨迹规划方面**，传统方法如 **cuRobo**（Sundaralingam et al., ICRA 2023）基于优化的路径规划算法，能够在已知场景中生成无碰撞的末端执行器轨迹。然而，这类方法通常需要针对每个新场景进行独立的优化求解，难以从运动捕捉数据中学习人类运动的自然模式，导致生成的轨迹在运动学上不够自然。基于学习的方法（如 Diffusion Policy）虽然能够从数据中学习运动先验，但在面对训练分布之外的新场景时，泛化能力和碰撞避免的可靠性仍然有限。

**全身运动控制方面**，**DeepPhase**（Starke et al. 2022）通过周期性自编码器（Periodical Auto-Encoder, PAE）在频域中学习运动的高效低维表示，在非周期性运动（如舞蹈）上展示了高质量的合成能力。然而，DeepPhase 本身是一个数据驱动的生成模型，缺乏根据运行时环境动态调整运动目标的机制——它无法自动适应变化的手部目标位置和场景约束。

**双手协调方面**，大多数现有工作要么假设单手操作，要么将双手运动独立处理，忽略了双手在复杂任务中的时序耦合和空间协调。当任务需要“先移除障碍物，再抓取目标物体”这样的序列化操作时，缺乏统一的调度机制会导致运动的不连贯和碰撞。

### 核心动机：从目标驱动到层次化合成

本文的核心动机在于：**将杂乱环境下的抓放交互建模为一个层次化的目标驱动任务**，通过将抽象的用户指令（如“拿起茶壶”）逐步分解为可执行的子目标，并在每个层次上引入专门的模块来解决对应的技术挑战。

这一设计理念的关键洞察在于：

- **手部抓放运动可以视为各向异性的水平集传播过程**。从运动捕捉数据中观察到，手部在接近和离开物体时的轨迹呈现出类似波前传播的模式——轨迹的梯度方向指向时间最短的路径。这启发我们将手部轨迹规划建模为隐式时间-到达场（time-of-arrival field）的构建与梯度追踪问题。

- **离散子任务之间的过渡可以通过频域相位控制来平滑**。DeepPhase 的线性动力学模型为运动提供了一个低维的相位空间，而 Kalman 滤波可以在这个空间中平滑地估计和过渡目标相位，从而在保留高频运动细节的同时消除子任务切换时的不连续性。

基于上述动机，CHOICE 系统将交互合成分解为三个协同工作的子模块：隐式神经轨迹规划器（INTP）负责生成无碰撞的手部轨迹，DeepPhase 交互控制器负责自回归地预测全身运动，双手调度器负责根据用户指令和场景状态安排关键帧序列。这种层次化的分解使得每个模块可以专注于解决特定的技术挑战，同时通过明确的目标接口实现模块间的无缝协作。

## 核心方法与创新机理

CHOICE 面向杂乱环境中多步骤、双手协调的抓放任务，其核心创新在于将交互合成建模为**层次化目标驱动任务**，在三个关键维度上实现了相对于现有方法的范式转变。

### 1. 从优化规划到隐式神经时间-到达场规划

传统轨迹规划方法（如基于优化的 **cuRobo**，Sundaralingam et al., ICRA 2023）依赖显式路径搜索和碰撞检测，难以直接学习人类手部运动的自然特性。CHOICE 提出**隐式神经轨迹规划器**（INTP），将手部抓放运动建模为各向异性水平集传播过程，通过一个三通道隐式场联合编码场景几何与运动先验：

$$\mathbf{f}:\mathbb{R}^3\to\mathbb{R}^3,\quad \mathbf{f}(\mathbf{x})=\mathbf{D}(\mathbf{x})=(D_t(\mathbf{x}),D_o(\mathbf{x}),D_{toa}(\mathbf{x}))$$

其中 $D_t$ 为目标距离场，$D_o$ 为障碍物距离场，$D_{toa}$ 为时间-到达场。训练时通过重建损失联合优化：

$$\mathcal{L}_{\mathrm{Rec}}=\sum_{\mathbf{x}\in E}\big(\|f_{\theta}(\mathbf{x},\mathbf{z};\mathbf{c})_0-D_t(\mathbf{x})\|_1+\|f_{\theta}(\mathbf{x},\mathbf{z};\mathbf{c})_1-D_o(\mathbf{x})\|_1+\|f_{\theta}(\mathbf{x},\mathbf{z};\mathbf{c})_2-D_{toa}(\mathbf{x})\|_2^2\big)$$

推理时，手腕速度通过时间-到达场的梯度求逆获得：

$$\mathbf{v}(\mathbf{x})=-\nabla\hat{\phi}(\mathbf{x})^{\circ-1}$$

这一设计的因果机制在于：**隐式场将场景几何、物体形状和人类运动先验压缩至统一的潜空间**，测试时仅需优化潜变量 $\mathbf{z}$ 即可泛化至新场景，无需重新训练。实验证实，INTP 在手-物交互轨迹上的 Fréchet 距离比 cuRobo 低 11%（139 vs 157），且三通道设计（分离目标、障碍物和时间-到达）是成功率的决定性因素——若将距离场合并为单通道，成功率大幅下降（Table 5）。

### 2. 从直接匹配到 Kalman 滤波平滑的相位目标过渡

现有运动控制方法（如 **Diffusion Policy**）通常直接匹配运动数据先验，在子任务切换时容易产生不连续。CHOICE 构建了基于 DeepPhase 的交互控制器，其关键创新在于引入 **Kalman 滤波器估计目标相位状态**，替代直接切换：

$$\mathbf{X}_{t+\Delta t}^{\mathcal{P}}=\mathbf{A}\mathbf{X}_t^{\mathcal{P}}+\mathbf{B}\mathbf{U}$$

Kalman 滤波器根据目标关键关节变换估计目标相位，通过预测-更新循环平滑离散子任务之间的过渡，同时保留高频运动细节。消融实验表明，去除目标相位和 Kalman 滤波会导致脚滑（Sliding）和不平滑度（Unsmoothness）显著增加（Table 4）；而仅用 MoE 网络直接估计目标相位虽略微改善曲率，但在子任务切换时出现明显不连续（Fig. 12）。该设计的因果机制在于：**频率域线性动力学模型天然适配周期性运动模式，Kalman 滤波则提供了贝叶斯最优的状态融合框架**，使系统能在保持运动多样性的同时实现平滑过渡。

### 3. 从单手调度到双手协调的层次化目标编排

针对杂乱环境中的多步骤交互，CHOICE 设计了**双手调度器**（Bimanual Scheduler）与状态机，根据用户点击和场景状态自动分配双手关键帧、导航目标和交互顺序。当目标物体被遮挡时，系统能检测不可抓取情况，先移除障碍物再重新规划（Fig. 7）。这一创新将抽象的用户指令转化为可执行的双手协调计划，填补了从单步抓取到多步骤全身交互的空白。

### 创新总结

| 关键槽位 | 基线方案 | CHOICE 方案 | 因果机制 |
|---------|---------|------------|---------|
| 轨迹规划方式 | 基于优化的路径规划（cuRobo） | 隐式神经时间-到达场（INTP） | 潜空间编码场景-运动先验，测试时优化潜变量泛化 |
| 控制目标过渡 | 直接匹配运动数据先验 | Kalman 滤波平滑相位目标状态 | 频率域线性动力学 + 贝叶斯最优状态融合 |
| 双手协调策略 | 独立或单手抓取调度 | 双手调度器 + 状态机 | 层次化目标分解，障碍物检测与重规划 |

> **注意**：Diffusion Policy 的具体引用元数据未在分析中提供，如需精确引用请手动核实。

CHOICE 将杂乱环境下的双手抓放交互合成建模为一个**层次化目标驱动任务**，自上而下分解为三个核心子任务：手-物轨迹规划、全身运动控制，以及双手目标调度。系统接收用户通过键盘发出的抽象动作指令（如“抓取茶壶并放置到指定位置”）和鼠标点击的目标物体，输出角色全身运动序列。

### 三阶段流水线

系统流水线（见 Fig. 2）由以下三个子系统级联构成：

![[assets/figures/papers/paper_list_l1666_CHOICE_Coordinated_Human_Object_Interaction_in_Cluttered_Environments_fo/figures/003_Figure_2.jpg]]
*Figure 2: Overview of our CHOICE System: Perceiving the involved objects around the clicking goal object (pic.1) with the action instruction from the keyboard, our system arrange tasks and motions to the empty hands, and match bimanual goals based on the character state and the goal tasks (green block that outputs pic.2). The matched hand goal priors are then re-planned by our trajectory planning sub-system (in dashed brown) to generate a trajectory of manipulation goals that fit the runtime environment (pic.4). A er planning a set of navigation goals (pic.3) alongside the manipulation trajectory, our goal coordination arranges the goal for the joints (pic.5) and sets a goal phase prior for the curre...*

1. **双手目标调度与状态机（Bimanual Goal Scheduling & State Machine）**
   根据用户点击的目标物体和动作指令，结合场景中物体的占用状态，为双手分配关键帧和导航目标。该模块包含目标匹配子系统，从运动捕捉数据集中检索与当前角色状态和目标任务最匹配的运动先验，作为后续控制的相位目标先验。

2. **隐式神经轨迹规划器（Implicit Neural Trajectory Planner, INTP）**
   以自解码器结构为基础，将手部抓取与放置轨迹建模为各向异性水平集传播过程。输入为场景的三维坐标 $\mathbf{x}$、编码环境与物体几何的隐向量 $\mathbf{z}$ 以及条件向量 $\mathbf{c}$，输出三通道隐式场：
   $$\mathbf{f}(\mathbf{x}) = \mathbf{D}(\mathbf{x}) = (D_t(\mathbf{x}), D_o(\mathbf{x}), D_{toa}(\mathbf{x}))$$
   其中 $D_t$ 为目标距离场，$D_o$ 为障碍物距离场，$D_{toa}$ 为时间-到达场。通过梯度求逆 $\mathbf{v}(\mathbf{x}) = -\nabla\hat{\phi}(\mathbf{x})^{\circ-1}$ 获得手腕速度，生成适应运行时环境的无碰撞手部轨迹。

3. **DeepPhase 交互控制器（DeepPhase Interaction Controller）**
   基于 DeepPhase 的周期性自编码器，在频率域对全身运动进行自回归预测。控制器通过 Kalman 滤波器估计与目标关键关节变换相关的目标相位状态，利用线性动力学模型 $\mathbf{X}_{t+\Delta t}^{\mathcal{P}} = \mathbf{A}\mathbf{X}_t^{\mathcal{P}} + \mathbf{B}\mathbf{U}$ 平滑离散子任务之间的相位过渡，保留高频运动细节。

### 模块间数据流

系统的信息流遵循“调度→规划→控制”的顺序：

- **目标调度**输出双手关键帧（抓取/放置姿态）和导航目标点；
- **轨迹规划器**接收关键帧位置和场景几何，生成从当前手部位置到目标位置的无碰撞手腕轨迹；
- **交互控制器**以规划轨迹作为关键关节目标，结合 Kalman 滤波估计的相位先验，自回归地生成下一帧的全身关节姿态，并通过双向控制混合反馈协方差以修正 Kalman 滤波器状态。

三个子系统形成闭环：控制器输出的角色状态反馈至调度器，用于判断任务完成状态并触发下一子任务的目标切换。

### 4.1 手-物轨迹的联合神经隐式表示

CHOICE 将手部抓取与放置轨迹建模为一个**各向异性水平集传播过程**，核心在于构建一个联合的隐式神经场，将三维空间坐标映射为包含场景几何与时间信息的特征向量。具体而言，系统定义映射函数：

$$\mathbf{f}:\mathbb{R}^3\to\mathbb{R}^3,\;\mathbf{f}(\mathbf{x})=\mathbf{D}(\mathbf{x})=(D_t(\mathbf{x}),D_o(\mathbf{x}),D_{toa}(\mathbf{x}))$$

其中三个通道的物理含义分别为：
- **$D_t(\mathbf{x})$**：空间中点 $\mathbf{x}$ 到目标物体表面的**逆距离**，基于快速行进法（FMM）求解 Eikonal 方程得到。在物体外部取有限正值，内部设为无穷大，为手部接近目标提供全局引导。
- **$D_o(\mathbf{x})$**：空间中点 $\mathbf{x}$ 到最近障碍物表面的**逆距离**，同样通过 FMM 计算。该通道使规划器能够感知环境中的碰撞风险，是实现无碰撞轨迹的关键。
- **$D_{toa}(\mathbf{x})$**：**时间-到达场**，定义为 $\phi(\mathbf{x})$ 的倒数 $D_{toa}(\mathbf{x}) = 1 / \max(\phi(\mathbf{x}), \epsilon)$，其中 $\phi(\mathbf{x})$ 表示从目标物体出发到达点 $\mathbf{x}$ 的累积时间。取倒数是为了保证场在远离目标处的连续性，避免无穷值。

### 4.2 隐式神经轨迹规划器（INTP）

INTP 采用基于自动解码器（auto-decoder）的架构，灵感来源于 DeepSDF（Park et al., 2019）。网络 $f_\theta$ 接收三个输入：
- **潜码** $\mathbf{z} \in \mathbb{R}^{128}$：编码当前场景的环境布局、物体几何形状以及手部运动轨迹的全局特征；
- **条件向量** $\mathbf{c}$：包含目标物体类别、操作类型等任务条件；
- **查询位置** $\mathbf{x}$：待查询的三维空间坐标。

网络输出上述三通道场值，训练时通过重建损失优化：

$$\mathcal{L}_{\mathrm{Rec}}=\sum_{\mathbf{x}\in E}\left(\|f_{\theta}(\mathbf{x},\mathbf{z};\mathbf{c})_0-D_t(\mathbf{x})\|_1+\|f_{\theta}(\mathbf{x},\mathbf{z};\mathbf{c})_1-D_o(\mathbf{x})\|_1+\|f_{\theta}(\mathbf{x},\mathbf{z};\mathbf{c})_2-D_{toa}(\mathbf{x})\|_2^2\right)$$

该损失对距离场 $D_t$ 和 $D_o$ 采用 L1 损失以保持边界锐度，对时间-到达场 $D_{toa}$ 采用 L2 损失以保证平滑性。推理时，给定新场景的部分观测，通过优化潜码 $\mathbf{z}$ 重建已知区域，即可泛化出完整的三通道场。

**轨迹生成机制**：手部手腕速度 $\mathbf{v}(\mathbf{x})$ 通过时间-到达场的梯度求逆得到：

$$\mathbf{v}(\mathbf{x})=-\nabla\hat{\phi}(\mathbf{x})^{\circ-1}$$

该公式的物理直觉是：手部沿时间-到达场下降最快的方向运动，即从当前位置以最短时间到达目标。这一设计使得规划器天然具备泛化能力——只要隐式场能够正确重建，轨迹便自动适应场景几何的变化。

### 5.2 DeepPhase 交互控制器与 Kalman 滤波

全身运动控制建立在 DeepPhase 模型（Starke et al., 2022）之上，其核心是将运动表示为频率域中的低维相位变量。相位状态的线性动力学方程为：

$$\mathbf{X}_{t+\Delta t}^{\mathcal{P}}=\mathbf{A}\mathbf{X}_t^{\mathcal{P}}+\mathbf{B}\mathbf{U}$$

其中 $\mathbf{X}^{\mathcal{P}}$ 包含各关节的相位、频率和振幅，控制输入 $\mathbf{U}$ 用于调节运动的节奏与幅度。CHOICE 的关键改进在于**目标相位估计机制**：当子任务切换时（如从导航切换到抓取），系统需要平滑过渡到新的运动模式。

为此，系统引入 **Kalman 滤波器**来估计目标相位状态。滤波器以 Goal Matching 子系统从数据集中检索的运动先验作为观测，结合当前角色状态进行预测-更新循环，输出平滑的目标相位特征。消融实验（Table 4）表明，去除 Kalman 滤波后，运动不平滑度从 5.94 升至 6.54 cm/s²，脚滑从 6.17 升至 7.22 cm/s，验证了该模块对运动质量的关键作用。

### 6.1–6.3 双手目标调度与状态机

双手调度器（Bimanual Scheduler）负责将抽象的用户指令（如“拿起茶壶”）分解为具体的双手关键帧序列。其核心是一个**状态机**（Fig. 6），根据当前场景和任务阶段自适应分配目标：
- **导航阶段**：生成全身导航目标，引导角色靠近操作区域（§6.2）；
- **交互阶段**：为双手分配抓取、移除障碍物、放置等操作目标（§6.3）。

![[assets/figures/papers/paper_list_l1666_CHOICE_Coordinated_Human_Object_Interaction_in_Cluttered_Environments_fo/figures/007_Figure_6.jpg]]
*Figure 6: Overview of our state-machine structure for synthesis coordinate interaction-guiding goals (corresponds to Fig. 2, the goal coordination block before ge ing the fused goal). It adaptively allocates coordinated goals for both the hands and the entire body according to the test environment as described in § 6.3. The navigation goal before arrival (see § 6.2) and the interaction goals during manipulation (plot in green capsules) are sequentially generated to guide the DeepPhase interaction controller*

当检测到目标物体被遮挡时（Fig. 7），调度器会自动插入“移除障碍物→抓取目标→放回障碍物”的子任务序列，利用空闲手完成协调操作。Goal Matching 子系统（§6.1）则从捕获的运动数据集中检索与当前目标关节变换最匹配的运动先验，作为 DeepPhase 控制器的目标相位参考。

**模块间的因果链路**：INTP 为双手提供无碰撞的手腕轨迹 → 双手调度器将轨迹转化为关键帧目标 → Goal Matching 检索对应的运动先验 → Kalman 滤波器平滑相位过渡 → DeepPhase 控制器自回归生成全身运动。这一层次化分解使得系统能够独立优化各子问题，同时通过目标信号实现端到端的协调。

![[assets/figures/papers/paper_list_l1666_CHOICE_Coordinated_Human_Object_Interaction_in_Cluttered_Environments_fo/figures/004_Figure_3.jpg]]
*Figure 3: Implicit neural trajectory planner: The scene visualization of the three fields uses the green color to show its value, deeper green represents a lower distance, and the blue color highlights the region of infinity distance. The right-side images give the 2D slices at the teapot height, where the zerolevel set was shown in orange curves. Under a test scene, z was optimized to reconstruct the known part of the output, which was encircled by the blue rectangles. The dashed blue rectangle illustrates the pre-known part of the time-of-arrival field*

![[assets/figures/papers/paper_list_l1666_CHOICE_Coordinated_Human_Object_Interaction_in_Cluttered_Environments_fo/figures/005_Figure_4.jpg]]
*Figure 4: Framework of Our DeepPhase interaction controller: The Kalman filter estimates the target phase correlated to the goal key-joint transformations. The Gating Network compares the features of key-joint transformations and the phase features from the current and goal frame, and a er each motion prediction for the next frame, our bi-directional control blends the key-joint transformation prediction, and also feeds back the covariance to the Kalman filter based on the displacement of the bi-directional prediction*

## 实验与关键发现

### 核心实验设计

CHOICE 系统在三个层面接受评估：手-物轨迹规划的质量与安全性、全身运动合成的逼真度与平滑性，以及系统各模块的消融贡献。实验场景覆盖标准厨房布局与泛化场景（如变窄的橱柜、加深的物体放置、新增障碍物），评估指标包括 Fréchet 距离（FD）、不平滑度（Unsmoothness）、脚滑动量（Sliding）、末端执行器轨迹曲率（EE RMSC）以及安全距离。

### 主实验结果

**全身运动质量对比。** 表 4 报告了 CHOICE 与采用 cuRobo 轨迹规划 + 相同运动控制器的基线在全身运动质量上的对比。核心结论如下：

- **Fréchet 距离（FD）**：CHOICE 的 FD 为 **139**，cuRobo 基线为 **157**，降低约 **11%**。FD 以 2 秒滑动窗口的姿态为特征向量，评估生成运动与数据集的相似度——数值越低表示运动越接近真实人体运动分布。
- **不平滑度（Unsmoothness）**：CHOICE 为 **5.94 cm/s²**，基线为 **6.54 cm/s²**，降低约 **9.2%**。该指标在根节点对齐的局部坐标系下计算，反映运动加速度的平滑程度。
- **脚滑动量（Sliding）**：CHOICE 为 **6.17 cm/s**，基线为 **7.22 cm/s**，降低约 **14.5%**。该指标衡量足部在地面支撑时的滑动速度，直接关联运动物理合理性。
- **末端执行器轨迹曲率（EE RMSC）**：CHOICE 为 **0.0408 cm⁻¹**，基线为 **0.0725 cm⁻¹**，降低约 **43.7%**。曲率越低，手腕运动越平滑自然。

这些改进的因果机制在于：INTP 规划器直接从运动捕捉数据学习真实手腕轨迹分布，避免了 cuRobo 等基于优化的规划器产生的机械式路径；同时，DeepPhase 交互控制器通过 Kalman 滤波平滑子任务间的相位目标过渡，消除了运动不连续。

**轨迹规划器泛化性能。** 表 5 报告了 INTP 与其他 SE(3) 轨迹规划器在场景泛化测试中的对比：

- **三通道 INTP（完整设计）**：成功率达 **98.8%**，安全距离为 **8.66 cm**。
- **合并距离场通道的 INTP-merged（2 通道消融）**：成功率大幅下降，安全距离显著降低。这验证了将目标距离场与障碍物距离场分离编码的必要性——合并后的单一距离场丧失了区分目标与障碍物的能力，导致轨迹规划在复杂场景中失效。
- **cuRobo**（Sundaralingam et al., ICRA 2023）：基于优化的规划器在泛化场景中表现受限，尤其在窄空间和深度放置场景中难以生成无碰撞轨迹。
- **Diffusion Policy**：基于扩散策略的学习方法在轨迹曲率和安全性上均不及 INTP。

Fig. 9 提供了定性对比：在变窄橱柜和扩展障碍物的代表性泛化场景中，INTP 生成的蓝色（接近）和绿色（离开）手腕轨迹平滑且远离障碍物，而 cuRobo 和 Diffusion Policy 的轨迹出现明显抖动或不安全接近。

![[assets/figures/papers/paper_list_l1666_CHOICE_Coordinated_Human_Object_Interaction_in_Cluttered_Environments_fo/figures/012_Figure_9.jpg]]
*Figure 9: Comparison of trajectory planners under representative generalization scenes with narrowed cabinets and expanded obstacles. The blue and green curves shown in two views record the approaching and leaving trajectory of the wrist, respectively. See more comparisons in our supplementary video*

### 消融实验

**目标相位与 Kalman 滤波。** 表 4 的消融行揭示了 DeepPhase 交互控制器中两个关键设计的贡献：

- **去除目标相位先验（w/o goal phase）**：脚滑动和不平滑度显著增加。目标相位先验为运动控制器提供了子任务切换时的运动风格指引，缺失时控制器仅依赖关键关节目标变换，导致运动僵硬。
- **去除 Kalman 滤波（w/o Kalman）**：类似地，运动质量下降。Kalman 滤波器的作用是在子任务边界处平滑相位目标状态估计，避免直接切换带来的突变。
- **仅用 MoE 网络估计目标相位**：虽然略微改善了轨迹曲率，但在子任务切换时出现明显不连续（见 Fig. 12）。MoE 网络直接输出的相位目标缺乏时序一致性约束，而 Kalman 滤波通过状态空间模型融合当前运动状态与目标先验，实现了平滑过渡。

![[assets/figures/papers/paper_list_l1666_CHOICE_Coordinated_Human_Object_Interaction_in_Cluttered_Environments_fo/figures/017_Figure_12.jpg]]
*Figure 12: Ablation study for our DeepPhase interaction controller in typical full-body interactions. We visualize the hand trace for the target approaching at (a,b), where the trajectory pieces with high curvature are highlighted by red heatmaps. In line (c), we show the bipedal trace of a pivot turning case, and line (d) shows a side-stepping case, where the skeletons from green to blue are from sequentially generated key-frames where both feet are on the ground, with red curves highlighting the sliding pieces. We annotate each approaching trajectory with its RMS curvature in 𝑐𝑚−1, the mean sliding during stepping in 𝑐𝑚/𝑠, and the duration time in seconds*

Fig. 12 的可视化消融进一步支持上述结论：(a-b) 中，去除 Kalman 滤波和 MoE 直接估计导致手部接近轨迹出现高曲率区域（红色热力图标注），RMS 曲率升高；(c-d) 中，全身转向和侧步运动出现更多脚滑动（红色曲线标注），平均滑动速度增加。

**隐式场通道设计。** 表 5 的 INTP-merged 消融表明，将目标距离场和障碍物距离场合并为单一通道会破坏轨迹规划的核心机制。三通道设计的因果逻辑在于：时间-到达场 $D_{toa}$ 的梯度 $\nabla \hat{\phi}$ 决定手腕速度方向（Eq. 10），而 $D_t$ 和 $D_o$ 分别为梯度传播提供目标吸引和障碍物排斥的边界条件。合并后，网络无法区分两种距离信号，导致梯度场在障碍物附近错误地指向目标方向，造成碰撞。

**双手调度与状态机。** 系统通过状态机（Fig. 6）自适应分配双手关键帧和导航目标。Fig. 7 展示了处理遮挡抓取的能力：当目标物体（茶壶）被障碍物阻挡时，系统先用一只手移除障碍物，再用另一只手取出目标物体，最后可将障碍物放回指定位置。这一能力依赖于双手调度器对任务顺序的规划，以及 INTP 对变化场景的实时重规划。

### 数据集与抓取精度

CHOICE 数据集包含烹饪、制作奶茶、清理桌面等多种双手交互任务（Fig. 8）。表 3 评估了抓取精度，指标包括最大穿透体积、穿透深度和浮动位移。这些指标验证了运动捕捉数据中手-物交互的物理合理性，为轨迹规划器提供了高质量的训练信号。

### 失败模式与局限性

Fig. 13 展示了系统在全新场景下的典型失败案例：

1. **全身碰撞避免不足**：碰撞解决方法仅通过平移关键关节目标变换来调整姿态，无法保证全身无穿透。在密集障碍物场景中，身体躯干或手臂可能穿入物体。
2. **导航感知局限**：全身导航基于 2D 路径规划，无法感知 3D 距离障碍物，导致角色在接近目标时可能与高处或侧面障碍物碰撞。
3. **容器泛化有限**：系统依赖运动捕捉数据，对未见容器结构（如不同形状的抽屉、柜门）的泛化能力有限，无法自动学习开门或打开抽屉的运动模式。
4. **轨迹规划假设**：INTP 假设运动守恒（$\nabla \times \mathbf{v} = 0$），不考虑旋度和动态变化，限制了处理旋转操作或动态避障的能力。

### 关键图表结论汇总

- **Fig. 2**（系统架构）：三阶段流水线——目标匹配与调度 → 隐式轨迹规划 → DeepPhase 交互控制——构成闭环，Kalman 滤波器在控制回路中持续修正相位目标状态。
- **Fig. 3**（INTP 架构）：潜码 $\mathbf{z}$ 通过测试时优化重建已知场区域，实现对未见场景的泛化；t-SNE 投影（Fig. 11）显示潜空间自动按家具类型聚类，相似布局连续分布。
- **Fig. 4**（DeepPhase 控制器）：双向控制混合关键关节变换预测，并将双向预测的位移反馈为 Kalman 滤波器的协方差，形成自适应控制回路。
- **Fig. 5**（相位控制分布）：频率域控制信号 $\mathbf{U}$ 的振幅和频率分量呈零均值高斯分布，揭示了运动过渡中一致的加速-减速模式。
- **Fig. 10**（轨迹自适应）：INTP 在标准橱柜、80% 窄橱柜（宽 29.5cm）、加深放置和增加障碍物四种条件下均生成合理接近轨迹，场变形自然适应空间约束。

## 定位与知识库关联

### 1. 方法定位与核心差异

CHOICE 面向**杂乱环境下的多步骤双手抓放任务**，将交互合成建模为层次化目标驱动问题，自上而下分解为双手调度、轨迹规划与全身控制三个子模块。与之对比，现有方法主要针对简单开放空间中的单步抓取，难以处理场景多样性与物体几何形状变化带来的双手协调和无碰撞轨迹规划挑战。

在**轨迹规划**层面，系统提出**隐式神经时间-到达场规划器（INTP）**，将手部抓放运动建模为各向异性水平集传播过程，利用三通道隐式场（目标距离场 $D_t$、障碍物距离场 $D_o$、时间-到达场 $D_{toa}$）的梯度实现可泛化的轨迹生成。这一设计直接学习运动捕捉数据中的真实手腕轨迹，避免了传统方法中轨迹规划算法与运动控制器之间的适配阶段。相比之下，基于优化的碰撞避免规划器 **cuRobo**（Sundaralingam et al., ICRA 2023）依赖显式路径优化，而基于扩散策略的 **Diffusion Policy** 学习方法则需要大量采样和去噪过程。

在**全身运动控制**层面，系统基于 **DeepPhase**（Starke et al. 2022）的周期性自编码器（PAE）构建交互控制器，将空间-时间运动映射到频域低维表示。其关键创新在于引入**Kalman滤波平滑的相位目标状态估计**：通过门控网络比较当前帧与目标帧的关键关节变换特征和相位特征，Kalman滤波器估计与目标姿态相关的目标相位，从而在离散子任务切换时平滑相位过渡，保留高频运动细节。这一机制解决了直接匹配运动数据先验时子任务切换出现明显不连续的问题。

在**双手协调**层面，系统设计了**双手调度器（Bimanual Scheduler）与状态机**，根据用户点击和目标安排双手关键帧和导航目标，支持检测目标被遮挡时自动移除障碍物并重新规划的序列化操作（见 Figure 7）。这区别于独立或单手抓取调度策略，能够处理需要双手协同的复杂任务（如打开容器、移除障碍物后抓取）。

### 2. 方法谱系与知识继承

CHOICE 的方法设计体现了对以下工作的继承与创新：

- **隐式神经表示**：INTP 的自动解码器结构受 **DeepSDF**（Park et al. 2019）启发，将场景几何和手部轨迹编码为 128 维潜在向量 $\mathbf{z}$，结合条件向量 $\mathbf{c}$ 和空间坐标 $\mathbf{x}$ 输出三通道场值。训练使用 L1 距离场损失和 L2 时间-到达场损失的联合重建目标（Eq. 7），测试时通过优化 $\mathbf{z}$ 重建已知场部分来实现场景泛化。

- **频域运动控制**：DeepPhase 交互控制器继承了 PAE 的线性动力学模型 $\mathbf{X}_{t+\Delta t}^{\mathcal{P}}=\mathbf{A}\mathbf{X}_t^{\mathcal{P}}+\mathbf{B}\mathbf{U}$（Eq. 15），通过控制信号 $\mathbf{U}$ 更新相位、频率和振幅。系统进一步揭示了控制信号的分布特性：振幅和频率控制遵循零均值高斯分布，表现出自然的加速与减速模式（Figure 5）。

- **水平集与快速行进法**：时间-到达场 $D_{toa}(\mathbf{x}) = 1 / \max(\phi(\mathbf{x}), \epsilon)$ 的计算基于快速行进法（FMM, Sethian 1996; Tsitsiklis 1995）求解 Eikonal 方程，将抓放轨迹建模为从目标表面向外传播的水平集过程。手腕速度通过时间-到达场梯度的逆计算得到：$\mathbf{v}(\mathbf{x})=-\nabla\hat{\phi}(\mathbf{x})^{\circ-1}$（Eq. 10）。

### 3. 适用边界与局限性

系统当前存在以下明确限制，需要在应用中审慎评估：

1. **全身导航的感知局限**：导航目标基于 2D 路径规划和导航匹配生成，无法感知 3D 距离障碍物，可能导致导航路径在三维空间中不够安全。

2. **碰撞解决的保守性**：碰撞解决方法仅通过平移关键关节的目标变换来实现，无法保证全身无穿透。在全新场景下，生成协调的全身无碰撞交互性能有限（Figure 13 展示了相关失败案例）。

3. **数据依赖性**：系统依赖运动捕捉数据训练，对未见容器结构（如不同形状的柜门、抽屉）和开门过程的泛化有限。轨迹规划器假设运动守恒，不考虑旋度和动态变化，限制了在更复杂操作任务中的适用性。

4. **调度策略的预定义性**：双手调度依赖预定义的对象模板和操作顺序，对完全新颖的场景组合可能不足，需要人工设计任务逻辑。

### 4. 关键证据强度评估

系统的核心性能主张具有较充分的定量支撑：

- **轨迹规划质量**：INTP 在手-物交互轨迹上相比 cuRobo 实现 11% 的 Fréchet 距离降低（139 vs 157, Table 4），且三通道隐式场设计在场景泛化测试中达到 98.8% 的成功率和 8.66 cm 的安全距离（Table 5）。消融实验证实，将距离场通道合并为单一距离场（2 通道）会大幅降低成功率和安全距离（Table 5, INTP-merged 行）。

- **运动平滑性**：基于 Kalman 滤波的深度相位控制器显著降低运动不平滑度（5.94 vs 6.54 cm/s²）和脚滑（6.17 vs 7.22 cm/s），末端执行器曲率指标 RMSC 降低 43.7%（0.0408 vs 0.0725 cm⁻¹, Table 4）。去除 Goal Phase 和 Kalman Filter 的消融实验证实这两个组件对运动真实度的关键贡献（Table 4）。

- **相位过渡质量**：仅用 MoE 网络直接估计目标相位虽略微改善曲率，但在子任务切换时出现明显不连续（Figure 12 对比），验证了 Kalman 滤波平滑机制的必要性。

### 5. 开放问题与未来方向

论文明确提出了以下待解决问题，为后续工作提供了直接切入点：

1. **矢量场推广**：如何将时间-到达场推广到包含旋度或动态变化，以处理更复杂的操作任务（如搅拌、倾倒等非保守运动）？

2. **容器泛化**：如何学习任意容器的内部结构和开门过程，使系统能够泛化到未见容器类型？

3. **3D 导航感知**：如何将 3D 距离传感器信息融入当前 2D 路径规划框架，实现真正无碰撞的全身导航？

4. **目标姿态计算**：如何利用视频先验计算适应多样化场景的最优目标可达姿态，减少对预定义模板的依赖？

这些问题指向了从运动守恒假设向动态矢量场、从预定义模板向学习式场景理解、从 2D 导航向 3D 感知的关键技术跃迁方向。

## 原文 PDF

![[paperPDFs/arxiv_2024/CHOICE_Coordinated_Human_Object_Interaction_in_Cluttered_Environments_for_Pick_and_Place_Actions.pdf]]
