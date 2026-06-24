---
title: Scalable Trajectory Generation for Whole-Body Mobile Manipulation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Scalable_Trajectory_Generation_for_Whole_Body_Mobile_Manipulation.pdf
project_link: "https://automoma.pages.dev/"
code_link: null
aliases:
- STGWBMM
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将AKR统一运动学建模与GPU加速的轨迹优化相结合，实现极大幅度生成吞吐量提升，从而提供规模空前的训练数据。
primary_logic: 通过将移动底座、机械臂和物体统一为单一运动学链（AKR），并在GPU上批量进行优化与碰撞检测，可以高效合成物理有效的全身协调轨迹；数据规模突破后，即使是SOTA模仿学习算法也能学习到泛化性强的全身控制策略。
claims:
- AutoMoMa在GPU上达5,000 episodes/GPU-hour，比CPU方法快80倍以上。
- AutoMoMa生成了超过500k条物理有效轨迹，涵盖330个场景、多种铰接物体和机器人形态。
- 即使单个铰接物体任务，SOTA方法也需要数万次演示才能达到~80%成功率，证实数据稀缺是根本约束。
- 在Pick任务上，AutoMoMa轨迹训练的策略成功率51.92%，显著优于MoMaGen基线的35%。
---

# Scalable Trajectory Generation for Whole-Body Mobile Manipulation

> [!tip] 核心洞察
> 通过将移动底座、机械臂和物体统一为单一运动学链（AKR），并在GPU上批量进行优化与碰撞检测，可以高效合成物理有效的全身协调轨迹；数据规模突破后，即使是SOTA模仿学习算法也能学习到泛化性强的全身控制策略。

| 字段 | 内容 |
|------|------|
| 中文题名 | 可扩展的全身移动操作轨迹生成 |
| 英文题名 | Scalable Trajectory Generation for Whole-Body Mobile Manipulation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.12565) · [Project](https://automoma.pages.dev/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | AutoMoMa |
| Dataset | 微波炉开门（30场景，未见场景）, Pick任务 |

> [!tip] 效果简介
> - 移动操作数据集规模对比 上，轨迹数 (# Episodes) 500,000 vs 39,350 (BC-Z) (>10x)。
> - 轨迹生成速率 上，Episodes per hour 5,000 (GPU) vs ~60 (CPU AKR) (~83x)。
> - 微波炉开门（固定基座） 上，成功率 100% (<800 轨迹)。

## 概述

全身移动操作要求机器人同时协调移动底盘与机械臂，在复杂环境中完成开门、抓取等铰接物体交互任务。这一领域长期受困于一个根本瓶颈：**缺乏大规模、物理有效的全身协调轨迹数据**。现有数据获取手段——人工遥操作虽保真度高但规模极小，脚本化策略虽可自动生成但缺乏全身协调性——均无法在规模、多样性与保真度上同时满足策略学习的需求。证据表明，即使针对单个铰接物体任务，SOTA模仿学习方法也需要数万条演示才能达到约80%的成功率，数据稀缺构成了策略泛化的刚性约束。

AutoMoMa 框架针对这一瓶颈提出了一个因果性解决方案：**将增强运动学表示（AKR）与GPU加速轨迹优化相结合，实现轨迹生成吞吐量的数量级跃升**。其核心洞察在于，将移动底盘、机械臂和目标物体统一建模为单一运动学链，并在GPU上批量进行约束优化与碰撞检测，可以高效合成物理有效的全身协调轨迹。一旦数据规模突破临界点，即使采用现有的SOTA模仿学习架构，也能学习出对未见环境具有强泛化能力的全身控制策略。

具体而言，AutoMoMa 在单个GPU上达到每小时生成5,000条有效轨迹的速率，较CPU基线方法加速80倍以上。凭借这一生成能力，该框架构建了包含超过50万条物理有效轨迹的数据集，覆盖330个场景、多种铰接物体类别和多种机器人形态——在规模上超过现有最大移动操作数据集一个数量级（如BC-Z的约3.9万条）。在Pick任务上，使用AutoMoMa轨迹训练的策略在到达阶段成功率达51.92%，显著优于MoMaGen基线的35%；在微波炉开门任务上，随着场景多样性从1个扩展到30个，策略对未见环境的泛化成功率从约20%提升至约75%。这些结果表明，数据规模与多样性的突破能够直接转化为策略性能的系统性提升。

从方法谱系来看，AutoMoMa 位于**自动规划驱动的大规模数据生成**范式，与遥操作数据采集（如BC-Z）和脚本化策略生成（如MoMaGen）形成互补。其技术贡献不在于提出新的模仿学习算法，而在于通过GPU并行化与统一运动学建模，将运动规划从离线分析工具转变为可扩展的数据生产流水线。这一思路与近年来在计算机视觉和语言模型中验证的“数据规模化驱动能力涌现”的逻辑一脉相承，为机器人学习领域的数据瓶颈问题提供了可操作的解决路径。

## 背景与动机

移动操作（mobile manipulation）要求机器人在移动基座与机械臂之间实现协调的全身运动，以完成开门、抓取、放置等日常任务。这类协调行为的学习高度依赖大规模、物理有效的轨迹数据。然而，现有数据获取范式在规模、多样性与保真度之间始终存在不可调和的三角矛盾：

**遥操作（teleoperation）** 能够提供高保真度的关节空间轨迹，但采集成本极高，导致数据集规模受限。例如，BC-Z 仅包含约 39,350 条轨迹（Table 1），远不足以覆盖全身协调所需的场景与物体多样性。

**脚本化策略（scripted policies）** 虽然可以自动生成数据，但通常将基座与手臂解耦规划，缺乏真正的全身协调，且难以泛化到复杂的铰接物体交互。

**基于优化的规划方法** 理论上可以生成物理有效的全身轨迹，但现有 CPU 实现（如 Jiao 等人的 AKR 规划器）吞吐量极低——约 60 episodes/小时——无法支撑策略学习所需的数据规模。

这一数据瓶颈的核心后果在实验中得到了明确量化：**即使对于单个铰接物体任务（如微波炉开门），SOTA 模仿学习方法也需要数万次演示才能达到约 80% 的成功率**（Abstract, Fig. 6a）。当场景从固定基座扩展到移动基座时，数据需求进一步急剧膨胀——移动基座策略在单一场景中需要 3,200 条轨迹才能达到约 70% 的成功率，而固定基座仅需不到 800 条轨迹即可达到 100%（Fig. 6a）。这揭示了根本性的数据稀缺问题：**全身移动操作策略的泛化能力被数据生成能力所严格约束**。

因此，该领域的核心瓶颈并非策略架构或学习算法本身，而在于**缺乏可扩展的、能大规模生成物理有效全身移动操作轨迹数据的流水线**。本文的动机正是打破这一瓶颈：通过将统一运动学建模与 GPU 加速的轨迹优化相结合，实现轨迹生成吞吐量的数量级提升，从而为全身移动操作策略学习提供规模空前的训练数据，并系统性地研究数据规模与多样性如何影响策略的泛化能力。

## 核心创新

AutoMoMa 的核心创新并非提出全新的规划算法或策略架构，而是**系统性地重构了全身移动操作轨迹数据的生成范式**。其关键突破在于将两条原本独立的技术线索——统一运动学建模（AKR）与 GPU 加速的轨迹优化——进行深度整合，从而将数据生成从稀缺的手工采集模式转变为可扩展的自动化工厂模式。

### 创新一：从解耦规划到统一运动学链建模

传统移动操作规划通常将移动底座与机械臂视为解耦的两个子系统，分别规划后再进行协调。AutoMoMa 通过 **AKR（Augmented Kinematic Representation）** 将底座、机械臂和操作物体统一为单条运动学链：

$$
\pmb { x } = \left[ \pmb { q } _ { B } ^ { \top } , \pmb { q } _ { M } ^ { \top } , \pmb { q } _ { O } ^ { \top } \right] ^ { \top } \in \mathcal { X } _ { \mathrm { f r e e } }
$$

其中，移动底座的平面运动通过虚拟基座（两个正交棱柱关节 + 一个旋转关节）建模，操作物体通过虚拟关节耦合到机械臂末端，形成从世界坐标系到物体关节的连续运动学链（Figure 2）。这一建模使得全身协调运动可以在统一的配置空间中通过单个约束优化问题求解，从根本上避免了底座与手臂规划之间的协调误差。

### 创新二：从 CPU 串行到 GPU 批量并行

AutoMoMa 将轨迹优化与碰撞检测批量迁移至 GPU，实现了生成吞吐量的数量级跃升。具体而言，通过将连杆几何近似为球体（spherical approximations），碰撞检测可高效并行化。这一硬件层面的 changed slot 带来了 **约 83 倍的加速**：从 CPU 基线的约 60 episodes/hour 提升至 5,000 episodes/GPU-hour。正是这一加速能力，使得生成超过 500k 条物理有效轨迹成为可能——这一规模远超现有最大移动操作数据集（如 BC-Z 的 39,350 条，Table 1），跨越了使模仿学习策略有效泛化的数据门槛。

### 创新三：数据规模突破解锁策略泛化能力

AutoMoMa 的深层贡献在于揭示了**数据规模与多样性是全身移动操作策略泛化的根本约束**。实验表明，即使对于单个铰接物体任务，SOTA 方法也需要数万次演示才能达到约 80% 的成功率。AutoMoMa 通过自动化生成打破了这一瓶颈：在 Pick 任务上，使用 AutoMoMa 轨迹训练的策略达到 51.92% 的成功率，显著优于 MoMaGen 基线的 35%（Sec E.3）。更关键的是，通过将场景多样性从 1 扩展到 30，策略对未见环境的泛化能力持续单调提升（Figure 6b），这直接验证了“数据规模驱动泛化”的核心假设。

### Changed Slots 总结

| 维度 | 基线方法 | AutoMoMa |
|------|----------|-----------|
| 规划加速硬件 | CPU 串行 | GPU 批量并行 |
| 运动学表示 | 底座-手臂解耦 | AKR 统一链 |
| 碰撞几何表示 | 原始网格（推测） | 球体近似 |
| 数据生成范式 | 遥操作/脚本化 | 全自动 GPU 加速规划 |

这些 changed slots 并非孤立的技术改进，而是围绕“规模化生成物理有效的全身协调轨迹”这一目标形成的协同系统。AKR 提供了统一的优化空间，GPU 并行化提供了求解速度，两者的结合使得数据规模突破成为可能，最终驱动了策略泛化能力的质变。

## 整体框架

AutoMoMa 是一个 GPU 加速的全身移动操作轨迹生成框架，其核心设计理念是将数据生成从遥操作或脚本化策略的规模瓶颈中解放出来。框架通过四个顺序集成的阶段，将任务定义转化为可用于模仿学习训练的大规模物理有效轨迹数据（Fig. 3）。

![[assets/figures/papers/paper_list_l959_https_arxiv_org_abs_2604_12565/figures/004_Figure_3.jpg]]
*Figure 3: The AutoMoMa data generation pipeline. Starting from a task specification triplet pS, O, Rq (left), AutoMoMa proceeds through four stages: (i) Task Specification defines the environmental, robotic, and object context; (ii) Problem Instantiation transforms raw scene assets into planning-ready primitives via ESDF construction and AKR assembly with spherical collision approximations; (iii) Trajectory Generation solves for optimal AKR states under task-specific constraints to produce physically valid whole-body motions; and (iv) Rendering in NVIDIA Isaac Sim produces synchronized RGB-D sequences and point clouds. The resulting trajectories span diverse scenes, objects, and robot embodiments (ri...*

### 输入与任务定义

框架的入口是一个**任务三元组** $(S, O, R)$，分别指定场景、物体和机器人形态。场景 $S$ 定义了环境几何与语义上下文，物体 $O$ 指定操作目标（可以是刚体或铰接物体），机器人 $R$ 则确定移动基座与机械臂的运动学模型。这一抽象使得 AutoMoMa 能够覆盖多样化的机器人形态（如 Ridgeback-UR5、Fetch 等）和操作任务（开门、抽屉、抓取等）。

### 问题实例化

在问题实例化阶段，原始场景资产被转换为规划所需的计算原语。具体而言，系统构建**欧几里德符号距离场（ESDF）** 以支持高效碰撞检测，并将机器人连杆几何体用**球体近似**替代原始网格，从而在 GPU 上实现大规模并行碰撞检验。同时，移动基座、机械臂和目标物体被组装为统一的**增强运动学表示（AKR）** 串行链——基座的平面运动通过虚拟基座关节建模，物体则通过虚拟关节耦合到机械臂末端，形成从世界坐标系到物体内部关节的完整运动学通路（Fig. 2）。

### 轨迹生成

轨迹生成阶段在统一的 AKR 配置空间中求解约束优化问题。优化目标为最小化总行程与轨迹不光滑度：

$$
\mathcal { I } ( \pmb { x } _ { 1 : T } ) = \sum _ { t = 1 } ^ { T - 1 } \left\| \pmb { w } _ { v } \Delta \pmb { x } _ { [ t ] } \right\| _ { 2 } ^ { 2 } + \sum _ { t = 2 } ^ { T - 1 } \left\| \pmb { w } _ { a } \Delta \dot { \pmb { x } } _ { [ t ] } \right\| _ { 2 } ^ { 2 }
$$

其中权重矩阵 $\pmb{w}_v$ 和 $\pmb{w}_a$ 调节基座与手臂之间的协调策略。约束条件包括运动学链闭环约束 $h_{\mathrm{chain}}(\pmb{x}_{[t]}) = 0$ 和终端任务完成约束 $\| f_{\mathrm{task}}(\pmb{x}_{[T]}) - \pmb{g}_{\mathrm{goal}} \|_2^2 \leqslant \xi_{\mathrm{goal}}$。通过在 GPU 上批量求解该优化问题，AutoMoMa 达到 **5,000 episodes/GPU-hour** 的生成速率，相比 CPU 基线方法（约 60 episodes/hour）实现了超过 80 倍的加速。

### 渲染与观测生成

生成的最优轨迹 $\pmb{x}_{1:T}^\star$ 随后在 NVIDIA Isaac Sim 中被渲染为同步的多模态观测数据。每条轨迹包含 30 个关节空间路径点，每个路径点对应 RGB-D 图像和 4,096 点的点云，以 120 帧/轨迹的密度输出。这为下游策略学习提供了丰富的感知输入。

### 输出与数据规模

通过上述流水线，AutoMoMa 生成了**超过 500k 条物理有效轨迹**，覆盖 330 个场景、多种铰接物体和机器人形态。相比现有移动操作数据集（如 BC-Z 的 39,350 条轨迹），AutoMoMa 在规模上实现了超过一个数量级的突破（Table 1），同时保持了全身协调性——这是遥操作数据（规模小）和脚本化策略（缺乏全身协调）均无法单独达成的组合优势。

### 补充图表

![[assets/figures/papers/paper_list_l959_https_arxiv_org_abs_2604_12565/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the AutoMoMa framework. Coordinated mobile manipulation demands large-scale, physically valid trajectory data—a bottleneck that existing teleoperation and planning methods cannot overcome at scale. AutoMoMa addresses this by unifying Augmented Kinematic Representation (AKR) modeling, which consolidates base, arm, and object kinematics into a single chain, with GPU-accelerated trajectory optimization. Given diverse robot embodiments, interactive scenes, and task objectives as inputs (left), AutoMoMa efficiently synthesizes over 500k trajectories exhibiting broad diversity across solutions, scenes, embodiments, and complex tasks such as grasp switching (center). This high-quality...*

## 核心模块与公式推导

AutoMoMa 将全身移动操作轨迹生成拆解为四个级联模块，其核心在于将移动基座、机械臂与目标物体统一建模为单一运动学链（AKR），并在该统一表示下求解约束轨迹优化问题。

### 统一运动学建模：AKR

传统方法将基座规划与手臂规划解耦，难以生成协调的全身行为。AutoMoMa 采用 **Augmented Kinematic Representation (AKR)**，将基座、机械臂和物体整合为一条串行运动学链。具体而言：

- **虚拟基座**：用两个正交的移动副和一个转动副对移动基座的平面运动进行建模，连接世界坐标系与机器人基座。
- **虚拟关节**：在机械臂末端与目标物体之间引入虚拟关节，将抓取关系编码为运动学约束。
- **物体运动学反转**：对于铰接物体，将运动学树从物体附着点反转到抓取点，形成一条以虚拟世界坐标系为根的连续链（Figure 2）。

![[assets/figures/papers/paper_list_l959_https_arxiv_org_abs_2604_12565/figures/003_Figure_2.jpg]]
*Figure 2: An example of the AKR construction. The AKR unifies independent kinematic trees into a single serial chain, enabling joint whole-body optimization of the base, arm, and object. The mobile base’s planar motion is modeled via a virtual base (blue), while a virtual joint (black) couples the manipulator (orange) to the target object (green). For articulated objects, the kinematic tree is inverted to reconfigure the kinematic root to the grasp point, forming a continuous chain (highlighted in yellow) rooted at the virtual world frame*

基于 AKR，系统的统一状态向量定义为：

$$
\pmb{x} = \left[ \pmb{q}_B^{\top}, \pmb{q}_M^{\top}, \pmb{q}_O^{\top} \right]^{\top} \in \mathcal{X}_{\mathrm{free}}
$$

其中 $\pmb{q}_B$ 为基座位姿（含虚拟基座关节），$\pmb{q}_M$ 为机械臂关节向量，$\pmb{q}_O$ 为物体关节状态。所有状态需处于无碰撞自由空间 $\mathcal{X}_{\mathrm{free}}$ 内。

### 约束建模

**运动学链约束**确保物体与其环境附着点之间的闭环运动学关系在每个时间步成立：

$$
h_{\mathrm{chain}}({\pmb{x}}_{[t]}) = 0, \qquad \forall t = 1, \ldots, T
$$

**任务完成约束**要求终端状态达到目标误差容许范围 $\xi_{\mathrm{goal}}$：

$$
\| f_{\mathrm{task}}(\pmb{x}_{[T]}) - \pmb{g}_{\mathrm{goal}} \|_2^2 \leqslant \xi_{\mathrm{goal}}
$$

### 轨迹优化目标

在满足上述约束的前提下，AutoMoMa 求解最小化总行程与轨迹不光滑度的优化问题。目标函数定义为：

$$
\mathcal{I}(\pmb{x}_{1:T}) = \sum_{t=1}^{T-1} \left\| \pmb{w}_v \Delta \pmb{x}_{[t]} \right\|_2^2 + \sum_{t=2}^{T-1} \left\| \pmb{w}_a \Delta \dot{\pmb{x}}_{[t]} \right\|_2^2
$$

其中 $\Delta \pmb{x}_{[t]} = \pmb{x}_{[t+1]} - \pmb{x}_{[t]}$ 为相邻状态差分，$\Delta \dot{\pmb{x}}_{[t]} = \Delta \pmb{x}_{[t]} - \Delta \pmb{x}_{[t-1]}$ 为速度差分。对角权重矩阵 $\pmb{w}_v$ 和 $\pmb{w}_a$ 调节各关节在行程最小化与平滑性之间的相对重要性——例如，为移动基座分配较低权重以鼓励基座运动，或为物体关节分配较高权重以抑制不必要的物体扰动。

最优轨迹为：

$$
\pmb{x}_{1:T}^{\star} = \arg\min_{\pmb{x}_{1:T}} \mathcal{I}(\pmb{x}_{1:T})
$$

### 数据生成流水线

AutoMoMa 将上述建模与优化集成到四个阶段中（Figure 3）：

1. **任务定义 (Task Specification)**：输入场景-物体-机器人三元组 $(S, O, R)$，定义任务语义与几何上下文。
2. **问题实例化 (Problem Instantiation)**：构建 ESDF 碰撞场、组装 AKR 链、将连杆几何近似为球体以加速碰撞检测。
3. **轨迹生成 (Trajectory Generation)**：在统一 AKR 配置空间中批量求解约束优化，每条轨迹包含 30 个关节空间路径点，同步输出 120 帧多模态观测（RGB-D 图像与 4,096 点/帧的点云）。
4. **渲染 (Rendering)**：在 NVIDIA Isaac Sim 中生成同步的视觉观测数据。

### 轨迹质量检验

对于固定物体任务，通过计算轨迹点相对于参考轨迹的位置偏差 $d$ 与方向偏差 $\theta$ 来量化执行精度：

$$
d = \| p(\pmb{x}_{[t]}) - p(\pmb{x}_{\mathrm{ref}}) \|_2, \quad \theta = \operatorname{arccos}(2 \langle r(\pmb{x}_{[t]}), r(\pmb{x}_{\mathrm{ref}}) \rangle^2 - 1)
$$

对于平面约束任务，检验垂直位移 $d_z$ 与 roll/pitch 角度偏差 $\theta_{\mathrm{planar}}$：

$$
d_z = | p_z(\pmb{x}_{[t]}) - p_z(\pmb{x}_{\mathrm{ref}}) |, \quad \theta_{\mathrm{planar}} = \| \psi(\pmb{x}_{[t]}) - \psi(\pmb{x}_{\mathrm{ref}}) \|_2
$$

### 关键设计决策与失效模式

**GPU 加速**是实现规模突破的核心：通过将轨迹优化与碰撞检测批量并行化，AutoMoMa 达到 5,000 episodes/GPU-hour 的生成吞吐量，较 CPU 基线加速 80 倍以上。**球体碰撞近似**虽大幅降低计算开销，但偶尔无法精确捕捉原始形状，导致规划中出现意外碰撞（Figure A3）。此外，固定基座约束违反仍可能发生（Figure A4），表明约束求解在复杂场景下并非完全可靠。

## 实验与分析

### 核心发现：数据规模与多样性是全身移动操作策略泛化的决定性瓶颈

AutoMoMa 的实验体系围绕一个中心命题展开：**大规模、物理有效且多样化的轨迹数据是训练可泛化全身移动操作策略的必要条件**。实验从数据生成效率、数据集规模、策略学习三个维度系统验证了这一命题。

**数据生成吞吐量突破**是 AutoMoMa 最直接的实证贡献。在 GPU 加速下，AutoMoMa 达到 **5,000 episodes/GPU-hour** 的生成速率，相较 CPU 基线的 AKR 规划器（约 60 episodes/hour）实现了 **约 83 倍加速**（Abstract, Sec 5.1）。这一吞吐量使得构建超 50 万条轨迹的数据集成为可能——如表 1 所示，AutoMoMa 的 500,000 条轨迹远超此前最大规模数据集 BC-Z 的 39,350 条，且是唯一同时具备全身协调性（Coord.）、大规模、高多样性和关节空间保真度的数据集。

**数据规模对策略成功率的因果效应**在微波炉开门任务上得到清晰展示。在固定基座配置下，仅需不到 800 条轨迹即可达到 **100% 成功率**（Fig 6a）；但引入移动基座后，即使提供 3,200 条轨迹，成功率仅约 **70%**，且见/未见场景之间存在持续的性能差距。当场景多样性从 1 扩展到 30 时，未见场景的泛化能力单调提升（Fig 6b）；在 30 场景设定下，将每场景轨迹密度从 750 提升至 30,000，成功率可达约 **75%**（Fig 6c）。这组消融实验揭示了两个关键机制：（1）移动基座引入的自由度使状态空间急剧膨胀，需要数量级更多的演示；（2）场景多样性与每场景轨迹密度对泛化能力存在互补效应。

**起始状态多样性的独立贡献**通过 Fig A10 的消融得到验证。即使总轨迹数固定（6,400 条），增加独特起始状态数量（从 50 到 1,000）仍能带来单调的性能改进；完整 12,800 条轨迹数据集达到最高成功率。这表明数据集的覆盖广度与密度同等重要。

### 跨架构泛化与任务扩展

AutoMoMa 生成的数据并非仅适用于单一策略架构。在相同的 30 场景微波炉开门设定下，**DP**（Diffusion Policy）和 **ACT**（Action Chunking Transformer）均随轨迹密度增加而持续提升性能（Fig 7），证明 AutoMoMa 作为数据生成流水线具有架构无关的通用性。

![[assets/figures/papers/paper_list_l959_https_arxiv_org_abs_2604_12565/figures/007_Figure_7.jpg]]
*Figure 7: Architectural generalization of AutoMoMa. When evaluated across the same 30-scene setup as DP3 [49], both DP [6] and ACT [13] exhibit consistent performance gains with increasing trajectory density, demonstrating AutoMoMa’s compatibility with diverse whole-body IL architectures*

在 Pick 任务（刚性物体抓取）上，AutoMoMa 训练的策略在到达阶段达到 **51.92% 成功率**，显著优于 MoMaGen 基线的 35%（Sec E.3）。这一结果进一步证实：自动规划生成的数据质量优于脚本化策略生成的数据，即便在相对简单的任务上也能带来显著收益。

在 100k 轨迹规模下，跨物体评估（Fig 8）显示 DP3 策略在五个 SAPIEN 物体上均能实现未见场景的泛化，尽管见/未见场景之间仍存在性能差距，表明物体级别的泛化仍需更大规模或更智能的数据策略。

![[assets/figures/papers/paper_list_l959_https_arxiv_org_abs_2604_12565/figures/009_Figure_8.jpg]]
*Figure 8: Per-object success rates at 100k trajectories. Success rates of the DP3 policy evaluated on five representative SAPIEN [47] objects. The bar plot compares performance under unseen (orange) and seen (blue) environments*

### 生成效率与场景复杂度

AutoMoMa 的生成吞吐量受场景杂乱度影响。Fig 4b 显示，随着场景空间约束增强（从场景 a 到 f），有效轨迹生成速率下降，这源于碰撞检测开销的增加。同时，Fig 4c-d 揭示了全身协调的补偿机制：在受限环境中，移动底座的平移运动减少，而机械臂的旋转运动增加，表明优化器自动在基座与手臂之间分配运动负荷。

### 失败模式与局限性

AutoMoMa 存在两类典型的规划失败模式：

1. **球体近似碰撞误判**（Fig A3）：为 GPU 加速而采用的球体近似几何有时无法精确捕捉原始形状，导致规划期间产生意外碰撞。这是计算效率与碰撞检测精度之间的固有权衡。
2. **固定基座约束违反**（Fig A4）：部分规划轨迹错误地包含了与物体固定基座约束不一致的运动，表明约束优化在边界情况下仍可能失效。

![[assets/figures/papers/paper_list_l959_https_arxiv_org_abs_2604_12565/figures/016_Figure.jpg]]
*Figure: A3. Trajectory failure caused by collision. Sphere-based geometry approximations occasionally fail to capture the original shape precisely, resulting in unintended collisions during planning. Figure A4. Trajectory failure caused by fixed-base constraint violation. The planned trajectory erroneously involves movements inconsistent with the object’s fixed-base constraint*

在策略推理端，失败主要表现为小误差累积（Fig A7）：基座或手臂姿态预测中的微小不一致随时间复合放大，最终将机器人推入不可行构型。

![[assets/figures/papers/paper_list_l959_https_arxiv_org_abs_2604_12565/figures/019_Figure.jpg]]
*Figure: A7. Representative inference failure. Small inconsistencies in base or arm pose predictions compound over time, eventually pushing the robot into an infeasible configuration. (a) Drawer-opening trajectory on the UR5-Ridgeback platform. (b) Cabinet door opening trajectory on the UR5-Ridgeback platform. Figure A8. Real-world validation on a UR5-Ridgeback platform. Planned trajectories for drawer opening and cabinet door opening are executed smoothly without collision or constraint violation*

真实世界验证仅在 UR5-Ridgeback 平台上进行了小规模抽屉和柜门开启测试（Fig A8），sim-to-real 差距的系统性评估尚未开展。此外，当前 50 万条轨迹虽规模空前，但场景和物体多样性仍有限，训练成本高，且数据生成本身依赖 GPU 资源。球体碰撞近似和约束违反问题提示，进一步改进几何表示和约束求解鲁棒性是提升数据质量的关键方向。

### 补充图表

![[assets/figures/papers/paper_list_l959_https_arxiv_org_abs_2604_12565/figures/002_Table_1.jpg]]
*Table 1: Comparison of AutoMoMa with existing mobile manipulation datasets. Existing datasets are constrained by their acquisition methods: teleoperation yields high-fidelity but small-scale data, while scripted policies lack whole-body coordination. AutoMoMa overcomes these limitations through GPU-accelerated automated planning, simultaneously achieving large scale, broad diversity, and highfidelity joint-space trajectories—a combination no prior dataset provides. “Coord.”: presence of whole-body base-arm coordination*

![[assets/figures/papers/paper_list_l959_https_arxiv_org_abs_2604_12565/figures/008_Figure_6.jpg]]
*Figure 6: Data scaling experiments. (a) In a single scene, the mobile base policy requires substantially more data than the fixed-base counterpart, with a persistent seen/unseen gap indicating manifold memorization. (b) Increasing scene diversity from 1 to 30 steadily improves generalization to unseen environments. (c) With 30 scenes, higher per-scene trajectory density further refines execution precision, enabling consistent generalization across seen and unseen scenes*

![[assets/figures/papers/paper_list_l959_https_arxiv_org_abs_2604_12565/figures/005_Figure_4.jpg]]
*Figure 4: Trajectory generation performance across six representative household scenes. (a) Test scenes with increasing spatial confinement. (b) Generation throughput (valid trajectories per second) decreases as scene clutter increases collision-checking overhead. (c) Average translational effort of the mobile base per trajectory (error bars: standard deviation). (d) Average rotational effort of the manipulator, reflecting compensatory whole-body motion in constrained environments*

![[assets/figures/papers/paper_list_l959_https_arxiv_org_abs_2604_12565/figures/006_Figure_5.jpg]]
*Figure 5: Distribution of trajectory base positions. Blue and orange spheres denote start and goal base placements, respectively, illustrating the broad spatial coverage achieved by the IK clustering strategy*

![[assets/figures/papers/paper_list_l959_https_arxiv_org_abs_2604_12565/figures/021_Figure.jpg]]
*Figure: Impact of Unique Start States Impact of Unique Start States and Trajectories Trajectory Configuration*

## 方法谱系与知识库定位

### 1. 问题定位：数据稀缺作为全身移动操作的根本瓶颈

全身移动操作（whole-body mobile manipulation）要求机器人同时协调移动底座与机械臂的运动，以完成开门、拾取等交互任务。现有数据获取范式在此问题上形成结构性瓶颈：

- **遥操作（teleoperation）** 可产生高保真轨迹，但采集成本极高，规模受限（例如 BC-Z 仅提供约 39,350 条轨迹，见 Table 1）。
- **脚本化策略（scripted policy）** 可批量生成数据，但缺乏真正的全身协调——底座与手臂通常是解耦规划的，导致轨迹物理保真度不足。
- **基于 CPU 的运动规划**（如 Jiao et al. 的 AKR planner）虽然能生成物理有效轨迹，但吞吐量极低（约 60 episodes/小时），无法满足策略学习对大规模数据的需求。

因果链条清晰：数据稀缺 → 策略学习只能在小规模、低多样性数据上进行 → 泛化能力受限。论文以实验直接验证了这一瓶颈：**即使在单个铰接物体任务上，SOTA 方法也需要数万次演示才能达到约 80% 的成功率**，说明数据量而非算法架构才是当前的根本约束。

### 2. 核心方法：AutoMoMa 的因果杠杆

AutoMoMa 的关键创新并非提出新的模仿学习算法，而是通过**重构数据生成流水线**来解除上述数据瓶颈。其因果杠杆在于两个相互增强的技术决策：

1. **统一运动学建模（AKR）**：将移动底座、机械臂和操作物体整合为单一串联运动学链（Figure 2），使得全身协调运动可在统一优化框架内求解，而非分步解耦规划。
2. **GPU 加速的批量轨迹优化**：将轨迹优化与碰撞检测批量部署在 GPU 上，配合球体近似几何（sphere-based collision approximation），将生成吞吐量提升至约 5,000 episodes/GPU-hour，**相比 CPU 基线加速约 83 倍**。

这一组合使 AutoMoMa 能够生成超过 500,000 条物理有效轨迹，覆盖 330 个场景、多种铰接物体和机器人形态——在数据规模上超越现有数据集一个数量级以上（Table 1）。

### 3. 与相关工作的关系定位

#### 3.1 数据生成范式对比

| 范式 | 代表工作 | 规模 | 全身协调 | 物理保真度 |
|------|----------|------|----------|------------|
| 遥操作 | BC-Z, RoboTurk | 小（~10³–10⁴） | 有（人工） | 高 |
| 脚本化策略 | Habitat 2.0 等 | 中–大 | 无/弱 | 低–中 |
| CPU 运动规划 | Jiao et al. (AKR) | 小 | 有 | 高 |
| **GPU 加速规划** | **AutoMoMa** | **大（5×10⁵）** | **有** | **高** |

AutoMoMa 在“规模 × 全身协调 × 物理保真度”的三维空间中占据了此前空白的位置。

#### 3.2 与模仿学习架构的关系

AutoMoMa 本身是**数据生成框架**，而非策略学习算法。论文通过实验证明，其生成的数据可有效训练多种 SOTA 模仿学习架构：

- **DP3**（3D 扩散策略）：作为主要验证架构，在 AutoMoMa 数据上训练的 DP3 策略在微波炉开门任务（30 场景未见环境）上达到约 75% 成功率，而单场景基线仅约 20%（Figure 6）。
- **DP**（扩散策略）与 **ACT**（动作分块 Transformer）：在相同 30 场景设置下，两者均随轨迹密度增加而持续获得性能提升（Figure 7），表明 AutoMoMa 数据对不同架构具有通用兼容性。

在 Pick 任务上，AutoMoMa 轨迹训练的 DP3 策略在到达阶段成功率达 51.92%，显著优于 MoMaGen 基线的 35%（Sec E.3），进一步验证了数据质量对策略性能的因果影响。

#### 3.3 知识库定位

AutoMoMa 在知识体系中的定位可概括为：

- **上游贡献**：为全身移动操作提供可扩展的、物理有效的轨迹数据生成能力，解决数据稀缺这一根本瓶颈。
- **下游兼容**：生成的轨迹可直接用于训练各类模仿学习策略（DP、ACT、DP3 等），无需修改策略架构或训练流程。
- **方法论定位**：属于“**数据驱动方法的数据基础设施**”——通过自动化规划替代人工遥操作，使大规模策略学习成为可能。

### 4. 适用边界与局限

#### 4.1 已知局限

1. **球体碰撞近似的精度问题**：球体近似有时无法精确捕捉原始几何形状，导致规划期间发生意外碰撞（Figure A3）。这在狭窄空间或复杂几何场景中尤为突出。
2. **约束违反风险**：固定基座约束可能被违反，规划出与物体约束不一致的轨迹（Figure A4）。
3. **仿真到现实的差距**：当前工作主要局限于仿真环境（Isaac Sim），真实世界验证仅在小规模上进行（Figure A8，UR5-Ridgeback 平台上的抽屉和柜门开启）。sim-to-real 的泛化能力需进一步系统研究。
4. **计算资源需求**：数据生成依赖 GPU 资源（500,000 条轨迹约需 100 GPU-hours），策略训练本身也需要大量演示（数万条轨迹才能达到高成功率），整体训练成本较高。
5. **场景与物体多样性有限**：尽管覆盖 330 个场景，但仍可能无法覆盖所有真实场景条件下的全身协调行为，特别是动态环境和移动障碍物场景。

#### 4.2 适用边界

- **适用场景**：静态环境中的铰接物体操作（开门、开抽屉、拾取放置），机器人形态为带移动底座的单臂系统。
- **不适用/未验证场景**：动态障碍物、多机器人协作、双臂操作、非刚性物体操作、需要力控的精细操作。
- **策略泛化边界**：实验表明，增加场景多样性（1→30）和每场景轨迹密度可单调提升泛化能力（Figure 6b, 6c），但仍存在 seen/unseen 场景间的持续性能差距，暗示策略可能部分依赖对训练流形的记忆。

### 5. 开放问题

1. **动态环境扩展**：AutoMoMa 框架是否可直接扩展到包含移动障碍物或动态环境的场景？当前 AKR 建模和轨迹优化均假设静态环境。
2. **零样本 sim-to-real 迁移**：生成的仿真轨迹能否未经微调直接部署到物理机器人并保持可靠泛化？目前仅有小规模概念验证。
3. **与在线学习的结合**：能否将 AutoMoMa 的批量生成能力与在线强化学习相结合，在部署过程中持续提升策略对未见场景的鲁棒性？
4. **数据效率提升**：能否通过更智能的采样策略（如基于不确定性的主动采样）或数据增强方法，减轻对大规模生成数据的依赖，降低训练成本？
5. **碰撞近似精度与速度的权衡**：球体近似带来的碰撞检测误差是否可通过自适应几何简化（如凸包分解）来缓解，同时保持 GPU 加速优势？

## 原文 PDF

![[paperPDFs/CVPR_2026/Scalable_Trajectory_Generation_for_Whole_Body_Mobile_Manipulation.pdf]]
