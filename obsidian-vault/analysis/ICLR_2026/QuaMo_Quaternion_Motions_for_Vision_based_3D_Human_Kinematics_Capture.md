---
title: "QuaMo: Quaternion Motions for Vision-based 3D Human Kinematics Capture"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/QuaMo_Quaternion_Motions_for_Vision_based_3D_Human_Kinematics_Capture.pdf
project_link: null
code_link: https://github.com/cuongle1206/QuaMo
aliases:
- QuaMo
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将关节旋转表示从欧拉角切换为单位四元数，并在S^3单位球面约束下精确求解四元数微分方程（QDE）；同时在meta-PD控制器中引入基于参考姿态二阶差分的加速度增强项，自适应调节控制信号强度。
primary_logic: 四元数微分方程配合单位球面精确积分彻底消除了旋转表示的不连续性，使运动过渡平滑稳定；加速度增强项根据参考姿态变化速率自适应调节——快速运动时增强控制信号加速收敛，接近目标时降低信号减少过冲，实现了在线场景下的高精度、低抖动运动学捕捉。
claims:
- 四元数表示避免欧拉角不连续性，图4展示根关节不连续时不同表示的重建对比
- S^3精确积分使MPJPE从53.1降至52.0 mm，验证消除近似误差的收益
- 加速度增强项进一步将MPJPE从52.0降至51.3 mm
- QuaMo在Human3.6M数据集上以MPJPE 46.7 mm达到运动学方法中最优，并在Fit3D、SportsPose、AIST上全面超越可比较方法
---

# QuaMo: Quaternion Motions for Vision-based 3D Human Kinematics Capture

> [!tip] 核心洞察
> 四元数微分方程配合单位球面精确积分彻底消除了旋转表示的不连续性，使运动过渡平滑稳定；加速度增强项根据参考姿态变化速率自适应调节——快速运动时增强控制信号加速收敛，接近目标时降低信号减少过冲，实现了在线场景下的高精度、低抖动运动学捕捉。

| 字段 | 内容 |
|------|------|
| 中文题名 | QuaMo: 基于四元数运动的视觉三维人体运动学捕捉 |
| 英文题名 | QuaMo: Quaternion Motions for Vision-based 3D Human Kinematics Capture |
| 会议/期刊 | ICLR 2026 |
| Links |  [Code](https://github.com/cuongle1206/QuaMo)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | QuaMo |
| Dataset | Human3.6M, AIST, SportsPose |

> [!tip] 效果简介
> - Human3.6M 上，MPJPE (mm) 50.3±0.13 (QuaMo_TRACE) vs 58.7 (OSDCap) (-8.4)；MPJPE (mm) 46.7±0.04 (QuaMo_HMR2.0) vs 运动学方法中最优基线 (SOTA（运动学类别）)；Accel (m/s²) 5.3±0.04 (QuaMo_HMR2.0) vs ≈9.1 (HMR2.0, 降低41.8%) (−41.8%)。
> - AIST 上，MPJPE (mm) 89.1±0.14 (QuaMo_HMR2.0) vs 105.5 (DiffPhy, 离线方法) (-16.4)。
> - SportsPose 上，全部指标 QuaMo_TRACE vs TRACE / OSDCap (大幅超越)。

## 概要

### 问题瓶颈

基于视觉的三维人体运动学捕捉面临一个根本性表示困境：现有方法普遍采用欧拉角或轴角表示关节旋转，但这些表示存在固有的**不连续性**（0与2π处跳变）和**奇异性**（万向锁），导致运动积分过程中出现不稳定重建。在仅依赖单帧未来参考姿态的在线场景下，这种不稳定性尤为严重——欧拉角跳变迫使模型沿不同旋转轴进行错误补偿。此外，传统欧拉积分（一阶Runge-Kutta）在更新四元数时违反单位球面S³约束，引入累积近似误差，进一步加剧了运动漂移。

### 核心方法

**QuaMo**（Quaternion Motions）通过三个关键设计解决上述问题：

1. **四元数表示切换**：将关节旋转从欧拉角切换为单位四元数，在S³单位球面上建模运动，从根本上消除表示的不连续性和奇异性。

2. **精确球面积分**：采用四元数微分方程（QDE）的精确指数映射解 $q_{t+\Delta t} = \exp(\frac{\Delta t}{2} \Omega(\omega_{t+\Delta t})) q_t$，替代传统欧拉积分，确保姿态更新始终在S³球面上，消除近似误差。

3. **加速度增强的meta-PD控制器**：在比例-微分控制基础上引入基于参考姿态二阶差分的加速度增强项 $\kappa_A (\text{vec}(\hat{q}_t \otimes \hat{q}_{t-\Delta t}^*) - \text{vec}(\hat{q}_{t-\Delta t} \otimes \hat{q}_{t-2\Delta t}^*))$，根据参考姿态变化速率自适应调节——快速运动时增强控制信号加速收敛，接近目标时降低信号减少过冲。

系统由两条可微分支构成：角速度ODE（通过meta-PD控制器和欧拉积分更新）和四元数姿态QDE（通过Hamilton四元数乘积沿S³球面精确推进），最终经SMPL蒙皮模块输出人体网格和关键点。

### 核心结论

**消融实验**验证了各组件的因果贡献（Table 3）：以纯PD控制器为基线，数据驱动偏置$f_\omega$使全局平移误差G-MPJPE从132.6降至115.9 mm；S³精确四元数积分使MPJPE从53.1降至52.0 mm；加速度增强项进一步将MPJPE降至51.3 mm，但Accel从5.2升至5.9 m/s²，揭示了精度与平滑性之间的权衡。

**主实验结果**：在Human3.6M数据集上，QuaMo_HMR2.0以MPJPE 46.7 mm达到运动学方法中最优性能（Table 1），同时将加速度抖动Accel降低41.8%（相对HMR2.0输入）。在Fit3D、SportsPose、AIST三个跨数据集测试中，QuaMo全面超越可比较的在线运动学方法OSDCap（Le et al., NeurIPS 2024），甚至在AIST上以在线设置超越离线扩散方法DiffPhy（Yuan et al., ICCV 2023），MPJPE从105.5降至89.1 mm（Table 2）。定性结果（Figure 3, Figure 4）直观展示了QuaMo在减少运动抖动和提升光轴精度方面的显著优势。

### 方法谱系与知识库定位

QuaMo属于**在线运动学方法**，与以下工作形成直接对比：

- **OSDCap**（Le et al., NeurIPS 2024）：同样采用在线设置，但使用欧拉角表示和卡尔曼滤波重积分。QuaMo以四元数表示和精确球面积分实现系统性超越。

- **D&D**（Li et al., ECCV 2022）：在线运动学方法，使用PD控制器与时序卷积。QuaMo的meta-PD控制器与加速度增强项提供了更精细的自适应控制。

- **HuMoR**（Rempe et al., CVPR 2021）：离线运动学方法，基于CVAE与测试时优化。QuaMo在在线约束下实现可比较甚至更优的性能。

- **PhysPT**（Zhang et al., CVPR 2024）、**DiffPhy**（Yuan et al., ICCV 2023）：离线物理感知方法。QuaMo的贡献聚焦于运动学表示层面的改进，尚未整合物理接触约束。

QuaMo依赖现成3D姿态估计器（**TRACE**, Sun et al., CVPR 2023; **HMR2.0**, Goel et al., ICCV 2023）提供参考姿态，其性能受限于估计器本身的噪声水平。当前方法未包含环境接触和物理约束，运动合理性评估局限于运动学指标，这为未来融入物理仿真提供了明确的扩展方向。

### 视觉三维人体运动捕捉的任务定位

从单目视频中恢复平滑、准确的三维人体运动是计算机视觉的核心挑战之一。现有主流方法可分为两类：基于模板的逐帧回归方法（如**HMR2.0** (Goel et al., ICCV 2023)、**TRACE** (Sun et al., CVPR 2023)）直接预测SMPL模型参数，速度快但缺乏时序建模，输出运动常伴随高频抖动；基于运动学/物理的时序方法则通过状态空间模型显式建模帧间依赖，追求运动平滑性与物理合理性。

在运动学方法中，在线（online）设置——仅依赖单个未来时间步的参考姿态进行实时推理——对实际部署至关重要，但也对运动表示的稳定性和控制策略的精度提出了更高要求。

### 瓶颈：欧拉角表示的内在缺陷

现有在线运动学方法（如**OSDCap** (Le et al., NeurIPS 2024)、**D&D** (Li et al., ECCV 2022)）普遍采用欧拉角或轴角表示关节旋转。这一选择引入两类根本性问题：

1. **不连续性**：欧拉角在0与$2\pi$边界处存在跳变。当根关节旋转跨越该边界时，模型为补偿不连续性会错误地沿其他旋转轴产生补偿运动，导致重建失真（Figure 4）。
2. **奇异性（万向锁）**：特定姿态下两个旋转轴对齐，丢失一个自由度，使运动过渡在该区域产生不稳定行为。

此外，传统方法采用欧拉积分（一阶Runge-Kutta）更新姿态，该积分方案天然违反四元数单位球面$S^3$的约束，引入累积近似误差，进一步加剧了在线场景下的运动漂移问题。

### 控制策略的局限：缺少对运动变化速率的感知

以**OSDCap**为代表的在线运动学方法采用meta-PD控制器生成角加速度信号。标准PD控制器仅响应当前姿态误差（比例项）和角速度（微分项），对参考姿态的变化速率不敏感。当参考姿态快速变化时（如运动方向突变、加速起跳），PD控制器响应滞后，导致瞬时误差增大；当接近目标姿态时，缺乏阻尼调节机制又可能引起过冲和振荡。这种“一刀切”的控制策略限制了在线运动学方法在动态场景下的精度上限。

### 动机：从表示和控制两个维度突破

QuaMo的动机源于一个核心洞察：**将关节旋转表示从欧拉角切换为单位四元数，并在$S^3$球面约束下精确求解四元数微分方程（QDE），可从根本上消除旋转表示的不连续性**；同时，**在meta-PD控制器中引入基于参考姿态二阶差分的加速度增强项，使控制信号能自适应匹配运动变化速率**——快速运动时增强驱动力以加速收敛，接近目标时降低信号以减少过冲。这两个维度的改进共同指向一个目标：在仅依赖单帧未来参考的严格在线约束下，实现高精度、低抖动的三维人体运动学捕捉。

## 核心方法与创新机理

QuaMo围绕“在线3D人体运动学捕捉”的稳定性与精度瓶颈，在三个关键维度对现有运动学方法进行了系统性改造：**关节旋转表示**、**微分方程积分精度**和**控制器自适应能力**。这三项创新构成一个因果链条——四元数表示消除不连续性，精确球面积分消除近似误差，加速度增强项提供自适应调节——最终实现在线场景下高精度、低抖动的运动重建。

### 创新1：从欧拉角到单位四元数的旋转表示切换

现有在线运动学方法（如**OSDCap**，Le et al., NeurIPS 2024；**D&D**，Li et al., ECCV 2022）普遍采用欧拉角或轴角表示关节旋转。欧拉角存在两个根本性缺陷：**不连续性**（在0与2π边界处发生跳变）和**奇异性**（万向锁导致自由度丢失）。在仅依赖单帧未来参考姿态的在线设置下，这些缺陷使积分过程极易产生不稳定运动重建。

QuaMo将关节旋转表示切换为**单位四元数**，在S³单位球面上进行姿态演化。四元数避免了欧拉角的周期跳变，保证了旋转空间的连续性和平滑过渡。**图4**提供了决定性定性证据：当根关节旋转出现不连续时，欧拉角、轴角等表示均试图沿不同旋转轴补偿跳变，导致重建姿态偏离真值；而四元数表示完全不受不连续性影响，重建结果与真值保持一致。

### 创新2：S³单位球面约束下的精确四元数积分

传统运动学方法采用**欧拉积分**（一阶Runge-Kutta）更新姿态，但欧拉积分违反四元数的单位球面约束（‖q‖ = 1），每一步积分都会引入近似误差，误差在时序传播中累积。

QuaMo直接求解**四元数微分方程**（QDE）的精确解。在恒定角速度假设下，姿态更新通过指数映射实现：

$$q_{t+\Delta t} = \exp\left( \frac{\Delta t}{2} \Omega(\omega_{t+\Delta t}) \right) q_t = q_\omega \otimes q_t$$

该解天然保持在S³球面上，彻底消除了欧拉积分的近似误差。消融实验（**Table 3**）量化了这一收益：将欧拉积分替换为S³精确积分后，MPJPE从53.1 mm降至52.0 mm，验证了消除近似误差对精度的直接贡献。

### 创新3：基于参考姿态二阶差分的加速度增强项

传统meta-PD控制器仅依赖比例-微分项和数据驱动偏置来生成角加速度信号，对参考姿态的变化速率不敏感。QuaMo引入**加速度增强项**，基于最近三帧参考姿态的四元数二阶差分：

$$\dot{\omega}_t = \underbrace{\kappa_P \big(\mathrm{vec}(\hat{q}_t \otimes q_t^*)\big) - \kappa_D \omega_t}_{\text{meta-PD控制}} + \underbrace{b_t}_{\text{偏置}} + \underbrace{\kappa_A \big(\mathrm{vec}(\hat{q}_t \otimes \hat{q}_{t-\Delta t}^*) - \mathrm{vec}(\hat{q}_{t-\Delta t} \otimes \hat{q}_{t-2\Delta t}^*)\big)}_{\text{加速度增强}}$$

该项的核心机制是**自适应调节**：当参考姿态快速变化时（如运动加速阶段），增强项增大控制信号强度，加速当前姿态向目标收敛；当接近目标姿态时，增强项减小，降低过冲风险。消融实验（**Table 3**）表明，加速度增强项将MPJPE从52.0 mm进一步降至51.3 mm，但Accel从5.2升至5.9 m/s²，揭示了精度与运动平滑性之间的固有权衡。

### 创新间的因果关联

三项创新构成递进关系：四元数表示是基础，消除了旋转空间的结构性缺陷；S³精确积分是保障，确保姿态更新在数学上严格成立；加速度增强项是优化，在正确表示和精确积分的基础上进一步提升控制精度。三者共同作用，使QuaMo在Human3.6M上以MPJPE 46.7 mm（HMR2.0为参考）达到运动学方法的最优水平，并在Fit3D、SportsPose、AIST三个跨域数据集上全面超越可比较的在线和离线方法。

QuaMo 将人体运动建模为离散时间状态空间系统，其核心状态由两个分量构成：以单位四元数表示的关节相对旋转姿态 $q_t \in \mathbb{H}$，以及对应的角速度 $\omega_t \in \mathbb{R}^3$。系统通过两个并行的可微分支进行时序推进——角速度 ODE 分支和四元数姿态 QDE 分支——在每一时间步上实现端到端的在线推理。

**输入与输出流。** 系统在每个时间步接收三类输入：(1) 当前时刻的四元数姿态 $q_t$ 和角速度 $\omega_t$；(2) 外部 3D 姿态估计器（TRACE 或 HMR2.0）提供的单帧未来参考姿态 $\hat{q}_t$；(3) 最近三帧的参考姿态历史 $\hat{q}_{t-2\Delta t:t}$，用于计算加速度增强信号。系统输出下一时刻的姿态 $q_{t+\Delta t}$、角速度 $\omega_{t+\Delta t}$，以及经 SMPL 蒙皮模型线性变换后的人体网格 $m_{t+\Delta t}$ 和关键点 $p_{t+\Delta t}$，同时独立计算根节点的全局平移 $r_{t+\Delta t}$。

**模块关系与数据流。** 图 2 展示了完整的系统架构，数据流按以下顺序传递：

1. **ControlNet 编码器**：以 $q_t$、$\omega_t$ 和参考姿态 $\hat{q}_t$ 为输入，提取融合当前状态与目标信息的潜在嵌入。
2. **控制头**：从潜在嵌入通过线性投影并行预测四组控制参数——比例增益 $\kappa_P$、微分增益 $\kappa_D$、数据驱动偏置 $b_t$，以及加速度增强增益 $\kappa_A$。
3. **Meta-PD 控制器与加速度增强**：依据式 (5) 计算角加速度 $\dot{\omega}_t$，该信号由三部分叠加：比例-微分控制项（以四元数误差的向量部分为比例输入、以当前角速度为阻尼项）、数据驱动偏置 $b_t$，以及基于参考姿态二阶差分的加速度增强项 $\alpha$。
4. **角速度欧拉积分器**：通过 $\omega_{t+\Delta t} = \omega_t + \dot{\omega}_t \Delta t$ 更新角速度。
5. **四元数微分方程求解器**：在单位球面 $S^3$ 约束下，通过 Hamilton 四元数乘积精确推进姿态：$q_{t+\Delta t} = \exp(\frac{\Delta t}{2} \Omega(\omega_{t+\Delta t})) \, q_t = q_\omega \otimes q_t$，其中指数映射将角速度转换为旋转四元数 $q_\omega$，再与当前姿态进行四元数乘法。
6. **SMPL 蒙皮模块**：将更新后的姿态 $q_{t+\Delta t}$ 与体型参数 $\beta$ 输入 SMPL 蒙皮模型，线性变换得到人体网格和关键点。
7. **根节点全局平移模块**：通过独立的 meta-PD 控制器和欧拉积分计算根节点平移 $r_{t+\Delta t}$。

**关键设计决策。** 两条分支的分工明确：角速度 ODE 负责根据控制信号产生驱动力，四元数 QDE 负责在 $S^3$ 流形上保持姿态表示的几何一致性。这种设计使旋转表示的连续性得到严格保证——图 4 的定性消融显示，当根关节旋转出现不连续时，欧拉角和轴角表示均产生补偿性异常旋转，而四元数表示避免了这一问题。SMPL 蒙皮模块作为可微的线性变换层，将抽象的姿态状态映射为可视化的网格和关键点，使整个 pipeline 支持端到端训练。

![[assets/figures/papers/paper_list_l1644_QuaMo_Quaternion_Motions_for_Vision_based_3D_Human_Kinematics_Capture/figures/002_Figure_2.jpg]]
*Figure 2: QuaMo consists of two differentiable equations: ODE for angular velocity ω and QDE for quaternion pose*

QuaMo 的核心是一个**离散时间状态空间模型**，由两条可微分支构成：角速度的常微分方程（ODE）分支和四元数姿态的四元数微分方程（QDE）分支。给定 $N$ 个人体关节，姿态张量 $\mathbf{Q} \in \mathbb{R}^{N \times 4}$ 由 $N$ 个单位四元数 $\mathbf{q} \in \mathbb{H}$ 组成，对应的角速度张量为 $\boldsymbol{\omega} \in \mathbb{R}^{N \times 3}$。

### 状态空间模型

系统以采样率 $\Delta t$ 离散化为：

$$
\begin{bmatrix} \omega_{t+\Delta t} \\ q_{t+\Delta t} \end{bmatrix} = \begin{bmatrix} f_{\mathrm{Euler}}(\omega_t, \dot{\omega}_t, \Delta t) \\ f_{\mathrm{Hamilton}}(q_t, \dot{q}_t, \Delta t) \end{bmatrix}, \quad \begin{bmatrix} \dot{\omega}_t \\ \dot{q}_t \end{bmatrix} = \begin{bmatrix} f_\omega(q_t, \omega_t) + u(q_t, \omega_t, \hat{q}_t) + \alpha(\hat{q}_{t-2\Delta t:t}) \\ f_q(q_t, \omega_{t+\Delta t}) \end{bmatrix}
$$

其中 $\hat{q}_t$ 为参考姿态（由 TRACE 或 HMR2.0 提供），$\omega_{t+\Delta t}$ 通过欧拉积分更新，$q_{t+\Delta t}$ 通过 Hamilton 四元数运算更新。角加速度 $\dot{\omega}_t$ 由三部分构成：数据驱动项 $f_\omega$、meta-PD 控制信号 $u$ 和加速度增强项 $\alpha$。

### 四元数表示与微分方程

关节旋转以单位四元数表示：

$$
q = q_0 + q_1 i + q_2 j + q_3 k
$$

四元数速度与角速度的关系由**四元数微分方程（QDE）**描述：

$$
\dot{q} = \frac{1}{2} \Omega(\omega) q = \frac{1}{2} \begin{bmatrix} -[\omega]_\times & \omega \\ -\omega^\top & 0 \end{bmatrix} q, \quad [\omega]_\times = \begin{bmatrix} 0 & -\omega_3 & \omega_2 \\ \omega_3 & 0 & -\omega_1 \\ -\omega_2 & \omega_1 & 0 \end{bmatrix}
$$

该方程定义了四元数在 $S^3$ 单位球面上的旋转过渡，从根本上避免了欧拉角表示的不连续性（$0$ 与 $2\pi$ 处跳变）和奇异性（万向锁）。

### 精确四元数积分

在恒定角速度假设下，QDE 存在 $S^3$ 球面约束下的精确解，通过指数映射将角速度转换为旋转四元数，再以 Hamilton 乘积旋转当前姿态：

$$
q_{t+\Delta t} = \exp\left( \frac{\Delta t}{2} \Omega(\omega_{t+\Delta t}) \right) q_t = q_\omega \otimes q_t
$$

相比传统欧拉积分（一阶 Runge-Kutta）违反 $S^3$ 约束引入近似误差，该精确解严格保持在单位球面上，消除了积分过程中的误差累积。

### Meta-PD 角加速度 ODE（含加速度增强）

角加速度由二阶 ODE 控制，包含比例-微分控制、数据驱动偏置和加速度增强三项：

$$
\dot{\omega}_t = \underbrace{\kappa_P \big(\mathrm{vec}(\hat{q}_t \otimes q_t^*)\big) - \kappa_D \omega_t}_{\text{meta-PD algorithm}} + \underbrace{b_t}_{\text{bias}} + \underbrace{\kappa_A \big(\mathrm{vec}(\hat{q}_t \otimes \hat{q}_{t-\Delta t}^*) - \mathrm{vec}(\hat{q}_{t-\Delta t} \otimes \hat{q}_{t-2\Delta t}^*)\big)}_{\text{acceleration enhancement}}
$$

- **比例项** $\kappa_P \cdot \mathrm{vec}(\hat{q}_t \otimes q_t^*)$：作用于当前姿态与参考姿态间四元数误差的向量部分，驱动姿态向目标收敛；
- **微分项** $-\kappa_D \omega_t$：阻尼当前角速度，抑制振荡和过冲；
- **数据驱动偏置** $b_t$：由 ControlNet 从潜在嵌入线性投影预测，用于补偿不同数据集间的系统性偏移；
- **加速度增强项** $\kappa_A \cdot (\mathrm{vec}(\hat{q}_t \otimes \hat{q}_{t-\Delta t}^*) - \mathrm{vec}(\hat{q}_{t-\Delta t} \otimes \hat{q}_{t-2\Delta t}^*))$：基于参考姿态最近三帧的四元数二阶差分，自适应调节——当参考姿态快速变化时增强控制信号加速收敛，接近目标时降低信号减少过冲。

控制增益 $\kappa_P, \kappa_D, \kappa_A$ 和偏置 $b_t$ 均由 ControlNet 根据当前四元数姿态 $q_t$、角速度 $\omega_t$ 和参考姿态 $\hat{q}_t$ 的潜在嵌入线性投影预测，实现数据驱动的自适应调节。

### 根节点全局平移

根节点平移 $r_{t+\Delta t}$ 采用独立的 meta-PD 控制和欧拉积分：

$$
r_{t+\Delta t} = r_t + \big(v_t + (\kappa_P(\hat{r}_t - r_t) - \kappa_D v_t) \Delta t\big) \Delta t
$$

### 训练损失

总损失由局部重建损失、全局一致性损失和体型正则化组成：

$$
\mathcal{L}_{\mathrm{local}} = \frac{1}{T}\frac{1}{N}\sum^T\sum^N |p_{0:T}^{GT} - p_{0:T}| + \frac{1}{T}\sum^T |r_{0:T}^{GT} - r_{0:T}|
$$

$$
\mathcal{L}_{\mathrm{global}} = \frac{1}{T}\frac{1}{N}\sum^T\sum^N |\ddot{p}_{0:T}^{GT} - \ddot{p}_{0:T}| + \frac{1}{T}\sum^T |\ddot{r}_{0:T}^{GT} - \ddot{r}_{0:T}|
$$

$$
\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{local}} + \mathcal{L}_{\mathrm{global}} + \lambda \mathcal{L}_{\mathrm{beta}}, \quad \mathcal{L}_{\mathrm{beta}} = \|\beta_{\mathrm{fix}}\|
$$

其中 $\mathcal{L}_{\mathrm{local}}$ 约束逐帧关键点与根节点平移的 L1 距离，$\mathcal{L}_{\mathrm{global}}$ 通过二阶有限差分约束预测轨迹的加速度与真值一致，$\mathcal{L}_{\mathrm{beta}}$ 对 SMPL 体型参数施加 L2 正则化。消融实验确定最优权重 $\lambda = 0.01$，在局部 MPJPE（51.2 mm）和全局 G-MPJPE（116.2 mm）间取得最佳折衷。

## 实验与关键发现

### 主实验结果

QuaMo在两个参考姿态源（TRACE和HMR2.0）下均展现出运动学方法中的最优性能。在Human3.6M数据集上，QuaMo_HMR2.0以**MPJPE 46.7±0.04 mm**、**P-MPJPE 30.6±0.03 mm**达到运动学类别的最优水平（Table 1）。与同为在线运动学方法的**OSDCap**（Le et al., NeurIPS 2024）相比，QuaMo_TRACE将MPJPE从58.7 mm降至**50.3±0.13 mm**，降幅达8.4 mm。在运动平滑性方面，QuaMo_HMR2.0的加速度指标**Accel仅5.3±0.04 m/s²**，相比输入HMR2.0（约9.1 m/s²）降低了41.8%，同时保持了全局平移精度（G-MPJPE 113.5 mm）。

![[assets/figures/papers/paper_list_l1644_QuaMo_Quaternion_Motions_for_Vision_based_3D_Human_Kinematics_Capture/figures/003_Table_1.jpg]]
*Table 1: Quantitative results on the Human3.6M dataset (Ionescu et al., 2014). Tmpl.: Templatebased approach (i.e. SMPL-based). Kin.: kinematics-based approach. Onl.: online approach. Online methods work with only one future target pose at each time step. Bold highlights the best results within the kinematics category. The proposed QuaMo reaches state-of-the-art performance on the MPJPE, P-MPJPE, G-MPJPE, and GRE with HMR2.0 as the meta-PD controller target. On the motion plausibly metrics Accel, G-Accel, FS, we consistently record better results compared to other online kinematics-based approaches*

跨数据集泛化实验（Table 2）进一步验证了方法的鲁棒性。在AIST舞蹈数据集上，QuaMo_HMR2.0以**MPJPE 89.1±0.14 mm**显著优于离线扩散方法**DiffPhy**（Yuan et al., ICCV 2023）的105.5 mm，降幅达16.4 mm——在线方法超越离线方法，体现了四元数运动学建模在快速舞蹈动作中的优势。在SportsPose运动数据集上，QuaMo_TRACE在所有指标上大幅超越输入TRACE和OSDCap，尤其在抖动指标上改善显著。定性结果（Figure 3）显示，QuaMo重建的运动（蓝色）相比输入参考姿态（绿色）抖动明显降低，沿光轴方向的精度更高，与真值（红色）吻合更好。

![[assets/figures/papers/paper_list_l1644_QuaMo_Quaternion_Motions_for_Vision_based_3D_Human_Kinematics_Capture/figures/004_Table_2.jpg]]
*Table 2: Quantitative results on the Fit3D (Fieraru et al., 2021) (top), SportsPose (Ingwersen et al., 2023) (middle) and the AIST (Li et al., 2021b) (bottom) dataset. Compared to OSDCap (Le et al., 2024a), QuaMo achieves a better performance on Fit3D and SportsPose, especially on the jittery metrics, using the same input TRACE. On AIST, with HMR2.0 as input, the proposed online QuaMo outperforms an offline method, DiffPhy, on both pose accuracy and motion jitter*

![[assets/figures/papers/paper_list_l1644_QuaMo_Quaternion_Motions_for_Vision_based_3D_Human_Kinematics_Capture/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative results on three datasets: Fit3D (left), SportsPose (middle), AIST (right). QuaMo’s predictions are shown in blue, the input (from TRACE or HMR2.0) in green, and ground truth keypoints in red for reference. The start frame has lower transparency. The reconstructed motions from QuaMo have significantly lower jitter and higher accuracy along the optical axis*

### 消融实验

Table 3的消融实验以纯PD控制器为基线，逐步验证各模块贡献：

**数据驱动偏置f_ω**：引入数据驱动偏置后，全局平移误差G-MPJPE从132.6 mm骤降至**115.9 mm**，降幅达16.7 mm。这表明学习到的偏置项有效补偿了不同数据集之间的系统性偏移，是保证全局平移精度的关键组件。

**S³精确四元数积分**：将传统欧拉积分替换为球面约束下的精确四元数指数映射积分后，MPJPE从53.1 mm降至**52.0 mm**。这一改进虽看似微小（1.1 mm），但其因果机制明确——欧拉积分违反四元数单位球面约束，引入累积近似误差；S³精确积分消除了这一误差源，使运动过渡在旋转空间内保持平滑连续。

**加速度增强项α**：加入基于参考姿态二阶差分的加速度增强项后，MPJPE进一步从52.0 mm降至**51.3 mm**。Table 3同时揭示了精度与平滑性的权衡：Accel从5.2升至5.9 m/s²。这表明加速度增强项在快速运动变化时加大控制信号以加速收敛，但略微增加了运动抖动——这是自适应调节机制的内在特性。

**旋转表示定性对比**（Figure 4）：当根关节旋转出现不连续性（0与2π处跳变）时，欧拉角和轴角表示的重建出现明显偏差，模型试图通过绕不同旋转轴补偿不连续性；而四元数表示的重建保持稳定，彻底消除了旋转表示不连续性带来的重建失真。

**体型正则化权重λ**（Table 4）：λ=0.01在局部MPJPE（51.2 mm）和全局G-MPJPE（116.2 mm）之间取得最佳折衷，被选为最终配置。

### 失败模式与局限性

尽管QuaMo在运动学指标上表现优异，仍存在以下局限：

1. **在线设置的固有限制**：方法仅依赖单帧未来参考姿态，缺乏离线方法的全局轨迹精修能力。在需要长时序一致性的复杂场景（如长时间遮挡后恢复）下，可能不及**HuMoR**（Rempe et al., CVPR 2021）等基于CVAE和测试时优化的离线方法。

2. **精度-平滑性权衡**：加速度增强项在提升MPJPE精度的同时，Accel从5.2升至5.9 m/s²。在极端运动或噪声输入下，二阶差分的放大效应可能导致抖动加剧。

3. **缺乏物理约束**：当前方法仅基于运动学状态空间建模，未包含环境接触（如脚-地面交互）和物理约束。运动合理性的评估局限于运动学指标（Accel, FS），无法保证物理层面的合理性。与**SimPoE**（Yuan et al., CVPR 2021）等物理仿真方法相比，QuaMo在足部滑动等物理合理性方面可能存在差距。

4. **对输入估计器的依赖**：方法依赖现成3D姿态估计器（TRACE/HMR2.0）提供参考姿态。估计器本身的噪声和不准确性会通过控制信号传播到四元数运动学系统中，尤其在遮挡或极端姿态下，参考姿态的误差可能导致控制信号失真。

### 公平性说明

所有在线运动学方法均限制为仅使用单个未来时间步的参考姿态，确保在线设置的公平比较。QuaMo_TRACE与OSDCap使用相同输入TRACE进行对比（Table 2）。所有方法在相同数据集上以相同指标评估，QuaMo结果报告了多次运行的标准差。SMPL模板化方法与非模板化方法（如从2D关键点提升的方法）不可直接比较，论文已明确区分两类方法。

![[assets/figures/papers/paper_list_l1644_QuaMo_Quaternion_Motions_for_Vision_based_3D_Human_Kinematics_Capture/figures/006_Table_3.jpg]]
*Table 3: Ablation studies. The baseline uses only a PD controller (PD only), taking TRACE as targets. The*

![[assets/figures/papers/paper_list_l1644_QuaMo_Quaternion_Motions_for_Vision_based_3D_Human_Kinematics_Capture/figures/008_Table_4.jpg]]
*Table 4: Ablation study on the shape loss scaling λ. We choose λ = 0.01 as our final selection due to the good performance trade-off between the local MPJPE and the global G-MPJPE*

## 定位与知识库关联

### 在运动学人体捕捉中的定位

QuaMo 属于**在线运动学人体运动捕捉**方法，其核心贡献在于将关节旋转的表示从欧拉角/轴角切换为单位四元数，并在 S³ 单位球面约束下精确求解四元数微分方程（QDE）。这一设计直接回应了现有在线运动学方法的两大瓶颈：

1. **欧拉角的不连续性与奇异性**：**OSDCap**（Le et al., NeurIPS 2024）和 **D&D**（Li et al., ECCV 2022）等在线运动学方法均依赖欧拉角表示关节旋转。欧拉角在 0 与 2π 处存在跳变（不连续性），且存在万向锁（奇异性），导致积分过程中出现不稳定运动重建。QuaMo 的四元数表示配合 S³ 精确积分彻底消除了这一问题——图 4 清晰展示了根关节不连续发生时，欧拉角和轴角表示均试图通过绕不同旋转轴补偿不连续，而四元数表示则保持平滑过渡。

2. **欧拉积分的近似误差**：传统方法使用一阶欧拉积分（即一阶 Runge-Kutta）更新四元数姿态，但该方法违反四元数单位球面约束，引入近似误差。QuaMo 通过指数映射沿 S³ 球面精确推进姿态（Eq. 4），消融实验证实这一改进使 MPJPE 从 53.1 降至 52.0 mm（Table 3）。

在 PD 控制策略层面，QuaMo 在传统 meta-PD 控制器基础上引入了**二阶加速度增强项 α**，该增强项基于最近三帧参考姿态的四元数二阶差分，能够自适应调节控制信号强度：快速运动时增强信号加速收敛，接近目标时降低信号减少过冲。这一设计使 MPJPE 从 52.0 进一步降至 51.3 mm（Table 3），但存在精度与平滑性的权衡——Accel 从 5.2 升至 5.9 m/s²。

### 与可比较方法的差异化分析

#### 在线运动学方法

| 方法 | 旋转表示 | 积分方案 | 控制策略 | 核心局限 |
|------|----------|----------|----------|----------|
| **D&D** (Li et al., ECCV 2022) | 欧拉角 | 欧拉积分 | PD 控制器 + 时序卷积 | 欧拉角不连续性；缺乏自适应控制 |
| **OSDCap** (Le et al., NeurIPS 2024) | 欧拉角 | 卡尔曼滤波重积分 | 数据驱动 | 欧拉角奇异性；卡尔曼滤波假设线性高斯噪声 |
| **QuaMo** (本文) | 单位四元数 | S³ 精确指数映射 | meta-PD + 加速度增强 α | 加速度增强引入轻微抖动；依赖参考姿态质量 |

QuaMo 在 Human3.6M 上以 MPJPE 46.7 mm（QuaMo_HMR2.0）达到运动学方法中最优，显著优于 OSDCap 的 58.7 mm（Table 1）。在 Fit3D 和 SportsPose 上，使用相同输入 TRACE 的 QuaMo_TRACE 在所有指标上超越 OSDCap，尤其在运动抖动指标上优势明显（Table 2）。

#### 离线运动学与物理方法

QuaMo 作为在线方法，仅依赖单帧未来参考姿态，而离线方法可利用完整时序信息进行全局优化。尽管如此，QuaMo 在多个基准上仍展现出竞争力：

- **HuMoR**（Rempe et al., CVPR 2021）：基于 CVAE 与测试时优化的离线运动学方法，在 Human3.6M 上 MPJPE 为 56.6 mm，QuaMo_HMR2.0（46.7 mm）显著更优（Table 1）。
- **DiffPhy**（Yuan et al., ICCV 2023）：离线物理引导扩散运动模型，在 AIST 上 MPJPE 为 105.5 mm，而在线 QuaMo_HMR2.0 达到 89.1 mm，在姿态精度和运动抖动上均超越该离线方法（Table 2）。
- **PhysPT**（Zhang et al., CVPR 2024）：离线物理感知 Transformer，在 Human3.6M 上 MPJPE 为 47.3 mm，与 QuaMo_HMR2.0（46.7 mm）接近，但 QuaMo 以在线约束实现了可比精度。

与物理仿真方法（**SimPoE** Yuan et al., CVPR 2021；**Neural MoCon** Huang et al., CVPR 2022）相比，QuaMo 的差异化在于：物理方法显式建模环境接触与动力学约束，运动合理性更强，但通常需要复杂的仿真环境和奖励设计；QuaMo 则通过运动学状态空间建模实现轻量高效的在线捕捉，代价是缺乏物理层面的合理性保证。

### 适用边界与局限

1. **在线约束的固有局限**：QuaMo 仅依赖单帧未来参考姿态，缺乏离线方法的全局轨迹精修能力。在需要长时序一致性的复杂场景（如长时间遮挡后的重现身）下，可能不及离线优化方法（如 HuMoR 的测试时优化）。

2. **精度与平滑性的权衡**：加速度增强项 α 在提升 MPJPE 的同时使 Accel 从 5.2 升至 5.9 m/s²（Table 3），表明更激进的姿态追踪会牺牲运动平滑性。这一权衡在需要高平滑性的应用（如动画生成）中需要谨慎调节。

3. **运动学层面的合理性**：当前方法仅基于运动学状态空间建模，未包含环境接触（如脚-地面交互）和物理约束（如动量守恒）。运动合理性的评估局限于运动学指标（Accel、FS），无法保证物理层面的合理性（如足部滑动、空中悬浮）。

4. **上游估计器的噪声传播**：QuaMo 依赖现成 3D 姿态估计器（**TRACE** Sun et al., CVPR 2023；**HMR2.0** Goel et al., ICCV 2023）提供参考姿态。估计器本身的噪声和不准确性（尤其在深度方向）会传播到四元数运动学系统中，影响最终捕捉质量。

5. **极端运动的泛化性**：方法在训练分布内的运动类型上表现良好，但在极端运动（快速旋转、杂技、摔跤等超出训练分布的动作）下的鲁棒性和泛化能力尚未验证。

### 开放问题

1. **物理约束的融合路径**：如何在四元数运动学框架中融入物理接触和交互约束（如足部滑动惩罚、地面反作用力），以在不牺牲在线效率的前提下提升运动在物理层面的合理性？

2. **控制增益的自适应行为**：学习到的控制增益 κ_P、κ_D、κ_A 在不同运动类型（行走、跑步、跳跃、舞蹈）下的分布和自适应调节行为如何？是否可解释为某种运动基元的隐式编码？

3. **加速度增强项的泛化性**：加速度增强项 α 的设计基于参考姿态的二阶差分，这一思想是否可推广到其他基于 PD 控制的运动生成或控制任务中（如物理仿真角色控制、机器人运动规划）？

4. **极端运动鲁棒性**：方法在快速旋转、杂技、摔跤等超出训练分布的动作下的鲁棒性和泛化能力如何？是否需要额外的数据增强或域适应策略？

5. **ControlNet 架构的透明性**：ControlNet 的具体网络架构（层数、注意力机制、时序编码方式）和训练超参数未被详细描述，其潜在嵌入如何有效融合当前状态 q_t、ω_t 与参考姿态 q̂_t 的信息？这一设计空间是否对性能有显著影响？

## 原文 PDF

![[paperPDFs/ICLR_2026/QuaMo_Quaternion_Motions_for_Vision_based_3D_Human_Kinematics_Capture.pdf]]
