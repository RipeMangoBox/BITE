---
title: Dual-Agent Reinforcement Learning for Adaptive and Cost-Aware Visual-Inertial Odometry
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Dual_Agent_Reinforcement_Learning_for_Adaptive_and_Cost_Aware_Visual_Inertial_Odometry.pdf
project_link: null
code_link: null
aliases:
- DARBVF
- DARLACAVIO
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 是否运行视觉前端（VO调度）以及以多大权重信任视觉输出（视觉-惯性融合）这两个关键设计决策。
primary_logic: 将VIO中的调度与融合问题建模为序列决策任务，利用轻量级强化学习智能体学习一个长期、成本感知的策略，从而实现计算资源与精度的灵活权衡。
claims:
- 在统一评估中，所提方法比已有GPU-based VO/VIO系统取得了更优的精度–吞吐量–内存权衡：达到最佳平均ATE，速度提升达1.77倍，且GPU显存占用更低。
- 在EuRoC上，CPU侧的BA/VIBA时间从ORB-SLAM3的121.09 ms和DM-VIO的26.49 ms降至12.77 ms，优化负担结构性减少。
- 消融实验表明，移除IMU偏差编码器导致ATE大幅上升，移除选择智能体则主要降低效率（FPS 39→21），验证了各组件的互补作用。
- EuRoC MAV (avg) 上 RMSE ATE (m) = 0.092
---

# Dual-Agent Reinforcement Learning for Adaptive and Cost-Aware Visual-Inertial Odometry

> [!tip] 核心洞察
> 将VIO中的调度与融合问题建模为序列决策任务，利用轻量级强化学习智能体学习一个长期、成本感知的策略，从而实现计算资源与精度的灵活权衡。

| 字段 | 内容 |
|------|------|
| 中文题名 | 自适应与成本感知的视觉-惯性里程计双智能体强化学习方法 |
| 英文题名 | Dual-Agent Reinforcement Learning for Adaptive and Cost-Aware Visual-Inertial Odometry |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.21083) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Dual-Agent RL-based VIO Framework |
| Dataset | EuRoC MAV, TUM-VI |

> [!tip] 效果简介
> - EuRoC MAV (avg) 上，RMSE ATE (m) 0.092 vs DM-VIO 0.069 (+0.023)。
> - TUM-VI (avg) 上，RMSE ATE (m) 0.80 vs DM-VIO 0.77 (+0.03)。
> - EuRoC MAV (GPU methods) 上，Throughput (FPS) 39 vs DPVO ~22 (1.77× speedup) (+17)。

## 概要

视觉-惯性里程计（VIO）是机器人自主导航的核心技术，但其精度与计算效率之间长期存在难以调和的矛盾。传统紧耦合VIO系统依赖计算密集的视觉-惯性束调整（VIBA），在资源受限平台上难以实时运行，构成了本文的核心瓶颈。

本文提出一种**双智能体强化学习VIO框架**，将VIO中的两个关键设计决策——**何时运行视觉前端**（VO调度）和**以多大权重信任视觉输出**（视觉-惯性融合）——建模为序列决策问题，并利用轻量级强化学习（RL）智能体学习长期、成本感知的策略。具体而言：一个**选择智能体**（Select Agent）仅基于高频IMU数据预先决定是否激活整个VO流水线，从而在运动平缓时跳过昂贵的视觉计算；一个**融合智能体**（Fusion Agent）学习自适应地融合IMU传播与稀疏VO更新，输出各轴融合权重。

该方法的核心贡献在于**解耦**了传统VIBA的紧耦合结构（图1），将计算调度与融合策略转化为可学习的策略网络，实现了精度、吞吐量与内存的灵活权衡。

在统一评估中，该方法相较于已有GPU-based VO/VIO系统取得了更优的精度–效率–内存权衡：达到最佳平均ATE，速度提升最高达1.77倍，且GPU显存占用更低。与经典CPU-based系统相比，CPU侧的BA/VIBA时间从ORB-SLAM3的121.09 ms和DM-VIO的26.49 ms结构性降至12.77 ms。消融实验进一步验证了各组件——IMU偏差编码器、选择智能体、融合智能体——对精度与效率的互补贡献。

**方法定位**：该方法在方法谱系上属于**学习型调度与融合**范式，区别于传统filter-based（如MSCKF、ROVIO）、optimization-based（如OKVIS、VINS-MONO、DM-VIO、ORB-SLAM3）以及纯学习型VO/VIO（如DPVO、DROID-VO、iSLAM）方法。其独特之处在于将RL引入VIO的计算调度与自适应融合环节，而非替代核心状态估计器，从而在保持精度的同时显著降低计算开销。

视觉-惯性里程计（VIO）是机器人导航与增强现实的核心模块，通过融合相机与惯性测量单元（IMU）数据实现高精度位姿估计。然而，现代VIO系统面临一个根本性瓶颈：**视觉-惯性束调整（VIBA）的高计算开销**。传统框架中，视觉前端与惯性融合被紧密耦合为单一的VIBA优化块（Figure 1a），这导致在资源受限平台上难以实时运行，迫使系统在精度与效率之间做出艰难取舍。

现有方法在这一权衡上各有侧重。基于滤波的方法（如 **MSCKF**、**ROVIO**）计算轻量但精度受限；基于优化的方法（如 **OKVIS**、**VINS-MONO**、**DM-VIO**、**ORB-SLAM3**）精度较高，但VIBA的CPU耗时可达数十甚至上百毫秒；基于学习的方法（如 **DPVO**、**DROID-VO**、**iSLAM**）将计算迁移至GPU，提升了吞吐量，却引入了显著的显存占用与功耗问题。这些方法共同暴露了一个结构性问题：**系统缺乏对“何时运行视觉前端”和“以多大权重信任视觉输出”这两个关键决策的灵活控制**，导致计算资源在运动平缓或视觉信息冗余时被无差别消耗。

本文的核心动机在于：将VIO中的调度与融合问题**重新建模为序列决策任务**。直觉上，并非每一帧都需要完整的视觉处理——当IMU传播已足够可靠时，跳过VO计算可以大幅节省资源；同样，融合权重应根据运动动态和视觉质量自适应调整，而非采用固定策略。这一视角将VIO从“被动优化”转变为“主动决策”，为突破VIBA瓶颈提供了新的可能性。

为此，本文提出**双智能体强化学习VIO框架**（Figure 1b）：一个**选择智能体**基于高频IMU信号预先决定是否激活VO流水线，从源头规避冗余计算；一个**融合智能体**学习上下文依赖的融合策略，自适应地权衡IMU预测与VO观测。通过轻量级RL策略，系统能够在精度、吞吐量与显存之间实现更优的帕累托前沿——在统一评估中达到最佳平均ATE，同时速度提升最高1.77倍且GPU显存占用更低。

## 核心方法与创新机理

### 问题瓶颈与因果抓手

传统视觉-惯性里程计（VIO）系统依赖紧耦合的视觉-惯性束调整（VIBA）模块，该模块在CPU上计算开销极高——ORB-SLAM3和DM-VIO的BA/VIBA时间分别达121.09 ms和26.49 ms（Table 3），严重制约了资源受限平台上的实时运行。本文识别出两个关键的因果调节变量（causal knobs）：**何时运行视觉前端**（VO调度）以及**以多大权重信任视觉输出**（视觉-惯性融合）。这两个设计决策直接决定了系统的计算负载与精度边界。

### 核心洞察：将VIO设计决策建模为序列决策问题

本文的核心洞察在于将上述两个设计选择统一建模为**序列决策问题**，并引入轻量级强化学习（RL）智能体来学习长期、成本感知的策略，从而实现计算资源与精度的灵活权衡。这与传统VIO中固定调度和固定融合权重的范式形成根本性差异。

### Changed Slots：相对基线的方法创新

#### Slot 1：VO调度策略——从“每帧执行”到“智能门控”

| 维度 | 基线方法 | 本文方法 |
|------|----------|----------|
| 调度策略 | 每帧执行VO/VIBA（如ORB-SLAM3、DM-VIO） | 基于IMU的RL选择智能体，仅在必要时激活VO |
| 决策依据 | 无选择机制 | 仅依赖高频IMU数据（角速度、加速度）的先验调度 |
| 计算代价 | 固定高开销 | 动态可调，可跳过整帧VO流水线 |

**选择智能体（Select Agent）** 将VO调度形式化为马尔可夫决策过程（MDP），其终端奖励函数为：

$$R_{\mathrm{episode}} = \frac{A}{\mathrm{ATE} + \epsilon} - B N_f$$

该奖励鼓励低ATE（高精度）和少量VO调用（低成本），通过调节权重A和B实现精度-效率权衡的显式控制。智能体仅观察紧凑的IMU状态，输出二元动作：跳过VO或运行VO。这一设计的关键优势在于**IMU-only先验调度**——决策不依赖视觉信息，从而避免了视觉前端本身的延迟和计算开销。

#### Slot 2：视觉-惯性融合权重——从“固定/优化”到“自适应RL融合”

| 维度 | 基线方法 | 本文方法 |
|------|----------|----------|
| 融合机制 | 固定权重或VIBA优化（如DM-VIO的延迟边缘化） | 基于RL的融合智能体输出各轴权重，自适应融合IMU传播与VO观测 |
| 权重来源 | 手工设计或优化求解 | 学习得到，上下文感知 |
| 不确定性建模 | 隐式或协方差传播 | 低成本不确定性代理（IMU残差标准差 + VO置信度） |

**融合智能体（Fusion Agent）** 由两个子模块组成：有监督的速度估计器（MLP1）和RL融合策略（MLP2）。MLP2输出各轴融合权重 $\mathbf{W}_p, \mathbf{W}_v$，执行凸组合融合：

$$p_k = \mathbf{W}_p p_k^{\mathrm{VO}} + (\mathbf{I} - \mathbf{W}_p) p_k^I, \quad v_k = \mathbf{W}_v v_k^{\mathrm{VO}} + (\mathbf{I} - \mathbf{W}_v) v_k^I$$

融合奖励函数为：

$$r_k = -\|\mathbf{p}_k - \mathbf{p}_{gt}\|_2^2 - \lambda \mathrm{Tr}(\boldsymbol{\Sigma}_k)$$

其中不确定性代理 $\boldsymbol{\Sigma}_k = \alpha \mathrm{diag}((\sigma_k^{\mathrm{imu}})^2) + \mathrm{diag}((1 - c_k^{\mathrm{vo}})^2)$ 以极低成本近似融合状态的不确定性，惩罚过度自信但错误的更新。消融实验（Table 5）表明，RL融合智能体在EuRoC MH 04上的ATE为0.112 m，优于启发式融合（0.143 m）和EKF融合（0.127 m）。

### 架构解耦：从紧耦合VIBA到四模块松耦合

传统VIO的VIBA块是**整体性且计算密集**的瓶颈（Figure 1a）。本文框架（Figure 2）将系统解耦为四个独立模块：

1. **IMU预处理**：偏差估计与IMU预积分，为后续模块提供校正后的惯性状态；
2. **选择智能体**：基于IMU的RL调度器，决定是否激活VO流水线；
3. **视觉里程计模块**：当选择智能体激活时，进行基于补丁的递归优化（类似DPVO）更新位姿；
4. **融合智能体**：自适应融合IMU传播与VO观测。

这一解耦设计的核心优势在于：**VIBA的结构性计算负担被两个RL智能体从调度和融合两个维度消解**——选择智能体通过跳过不必要的VO调用减少计算总量，融合智能体通过自适应权重避免昂贵的联合优化，同时保持融合质量。

### 创新点的证据强度

- **计算效率的结构性改进**：CPU侧BA/VIBA时间从ORB-SLAM3的121.09 ms和DM-VIO的26.49 ms降至12.77 ms（Table 3），置信度0.98。
- **精度-效率-内存的全面权衡优势**：在统一GPU评估中，所提方法达到最佳平均ATE，速度比DPVO快1.77倍（39 FPS vs ~22 FPS），且GPU显存占用比DROID-VO降低45.2%（4.37 GB vs 7.98 GB）（Table 4），置信度0.98。
- **组件互补性验证**：消融实验（Table 9）表明，移除IMU偏差编码器导致ATE大幅上升（EuRoC: 0.092→0.279），移除选择智能体则主要降低效率（FPS从39降至21），验证了各组件的互补作用，置信度0.98。

本文提出的双智能体强化学习VIO框架将传统紧耦合的视觉-惯性束调整（VIBA）解耦为四个独立模块，从根本上缓解了VIBA在资源受限平台上难以实时运行的瓶颈。如 **Figure 1** 所示，传统框架依赖单一、计算昂贵的VIBA块，而本框架通过引入两个轻量级RL智能体——选择智能体和融合智能体——实现了计算资源与精度的灵活权衡。

![[assets/figures/papers/paper_list_l2715_https_arxiv_org_abs_2511_21083/figures/001_Figure_1.jpg]]
*Figure 1: The accuracy-efficiency trade-off in VIO. (a) The traditional tightly-coupled VIO framework, which relies on a monolithic and computationally expensive Visual-Inertial Bundle Adjustment (VIBA) block. (b) Our proposed decoupled RL-based framework. We mitigate the VIBA bottleneck by introducing two intelligent agents*

系统整体架构如 **Figure 2** 所示，包含以下四个解耦模块：

![[assets/figures/papers/paper_list_l2715_https_arxiv_org_abs_2511_21083/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our proposed VIO pipeline. The system is composed of four decoupled modules: (1) IMU Preprocess, (2) Select Agent, (3) Visual Odometry, and (4) Fusion Agent. This framework leverages Reinforcement Learning to intelligently schedule and fuse sensor data, offering a highly computationally efficient alternative to traditional, tightly-coupled Visual-Inertial Bundle Adjustment*

1. **IMU预处理（IMU Preprocess）**：利用预训练的偏差估计网络 $f_{bias}^g$ 和 $f_{bias}^a$ 校正原始IMU测量值，并执行IMU预积分，输出帧间惯性状态 $(\Delta \mathbf{p}, \Delta \mathbf{q}, \Delta \mathbf{v}, \Delta t)$，为后续模块提供校正后的惯性先验。

2. **选择智能体（Select Agent）**：基于纯IMU高频信号的RL调度器，将VO调度建模为马尔可夫决策过程（MDP），输出二元动作——跳过VO或运行VO。该智能体仅在必要时激活视觉前端，从源头减少计算开销。

3. **视觉里程计模块（Visual Odometry Module）**：当选择智能体输出运行信号时，执行基于补丁的递归优化（类似DPVO），通过最小化重投影误差更新位姿和深度。该模块仅在激活时消耗GPU资源。

4. **融合智能体（Fusion Agent）**：由两个子模块组成——有监督速度估计器（MLP1）和RL融合策略（MLP2）。MLP2输出各轴融合权重，通过凸组合自适应融合IMU传播状态与VO观测：
   $$p_k = \mathbf{W}_p p_k^{\mathrm{VO}} + (\mathbf{I} - \mathbf{W}_p) p_k^I, \quad v_k = \mathbf{W}_v v_k^{\mathrm{VO}} + (\mathbf{I} - \mathbf{W}_v) v_k^I$$

**输入输出流**：系统以原始IMU测量（角速度、加速度）和相机图像为输入。IMU数据经偏差校正和预积分后，同时供给选择智能体（用于调度决策）和融合智能体（用于状态传播）。当选择智能体激活VO模块时，图像帧经视觉前端处理后输出VO位姿和置信度，送入融合智能体与IMU预测进行自适应融合，最终输出全局一致的位姿估计。这一解耦设计使视觉前端的计算开销与融合策略相互独立，实现了精度-效率-内存的灵活权衡。

### 系统架构总览

所提框架由四个解耦模块构成（Figure 2）：**IMU预处理**、**选择智能体**、**视觉里程计**和**融合智能体**。核心瓶颈在于传统视觉-惯性束调整（VIBA）的高计算开销——每帧运行VO前端并在CPU上执行BA/VIBA导致资源受限平台上难以实时运行。该框架将两个关键设计决策——*何时运行视觉前端*和*以多大权重信任其输出*——建模为序列决策问题，分别由两个轻量级RL智能体求解。

---

### 模块一：IMU预处理

IMU预处理模块包含**偏差估计网络**和**预积分**两部分。

**偏差估计**使用两个预训练网络，从原始IMU测量中校正陀螺仪和加速度计偏差：

$$\hat{\mathbf{b}}_g = f_{bias}^g(\tilde{\Omega}, \mathbf{n}_g)$$

其中 $\tilde{\Omega}$ 为原始角速度序列，$\mathbf{n}_g$ 为噪声剖面。加速度计偏差类似处理。推理时，预训练网络直接校正原始IMU测量，无需在线优化。

**IMU预积分**在两帧之间累积惯性状态，产生帧间预积分量 $(\Delta\mathbf{p}, \Delta\mathbf{q}, \Delta\mathbf{v}, \Delta t)$。离散迭代传播公式为：

$$\begin{array}{rl}
\Delta\mathbf{R}_{k,i+1} &= \Delta\mathbf{R}_{k,i} \operatorname{Exp}(\hat{\omega}_i \Delta t_i) \\
\Delta\mathbf{v}_{k,i+1} &= \Delta\mathbf{v}_{k,i} + \Delta\mathbf{R}_{k,i} \hat{a}_i \Delta t_i \\
\Delta\mathbf{p}_{k,i+1} &= \Delta\mathbf{p}_{k,i} + \Delta\mathbf{v}_{k,i} \Delta t_i + \frac{1}{2} \Delta\mathbf{R}_{k,i} \hat{a}_i \Delta t_i^2
\end{array}$$

这些预积分量作为后续选择智能体和融合智能体的输入特征。

---

### 模块二：选择智能体——RL调度

VO调度被建模为**马尔可夫决策过程（MDP）**。选择智能体仅基于高频IMU数据（预积分状态）做出先验调度决策，输出二值动作：$a_t^{sel} \in \{\text{Skip VO}, \text{Run VO}\}$。跳过VO时，整个视觉前端（特征提取、匹配、BA）均不执行，直接节省计算。

**奖励设计**采用终端奖励形式，平衡精度与计算成本：

$$R_{\mathrm{episode}} = \frac{A}{\mathrm{ATE} + \epsilon} - B \cdot N_f$$

其中 $A$ 为精度权重，$B$ 为VO调用成本权重，$N_f$ 为序列中VO调用次数，$\epsilon$ 防止除零。该奖励鼓励低ATE（高精度）和少量VO调用（高效率），$A$ 和 $B$ 的比例决定了精度-效率权衡的偏好（Figure 8 展示了偏好热图）。

---

### 模块三：视觉里程计模块

当选择智能体输出 $a_t^{sel} = 1$ 时，VO模块被激活。该模块基于补丁的递归优化（类似DPVO），核心是可微束调整层，最小化重投影误差以更新位姿 $\mathbf{T}$ 和深度 $\mathbf{P}$：

$$\Delta\mathbf{T}, \Delta\mathbf{P} = \arg\min \sum_{(k,t)} \left\| \hat{\omega}_{it}(\mathbf{T}, \mathbf{P}_k) - [\hat{P}_{kt}' + \delta_{kt}] \right\|_{\Sigma_{kt}}^2$$

其中 $\hat{\omega}_{it}$ 为重投影函数，$\hat{P}_{kt}'$ 为参考补丁，$\delta_{kt}$ 为校正目标，$\Sigma_{kt}$ 为置信度权重。该可微层通过高斯-牛顿迭代求解最优位姿和深度更新。

---

### 模块四：融合智能体——RL自适应融合

融合智能体由两个子模块组成：**有监督速度估计器（MLP1）** 和 **RL融合策略（MLP2）**。

**MLP1** 从IMU预积分和VO观测中估计速度，提供VO速度观测 $v_k^{\mathrm{VO}}$。

**MLP2** 学习输出各轴融合权重 $\mathbf{W}_p, \mathbf{W}_v$，对IMU传播状态和VO观测进行凸组合融合：

$$p_k = \mathbf{W}_p p_k^{\mathrm{VO}} + (\mathbf{I} - \mathbf{W}_p) p_k^I, \quad v_k = \mathbf{W}_v v_k^{\mathrm{VO}} + (\mathbf{I} - \mathbf{W}_v) v_k^I$$

其中 $p_k^I, v_k^I$ 为IMU传播的位置和速度，由预积分推导：

$$\mathbf{v}_{b_{k+1}}^w = \mathbf{v}_{b_k}^w - \mathbf{g}^w \Delta t_k + \mathbf{R}_{b_k}^{w\top} \boldsymbol{\beta}_{k,k+1}$$

$$\mathbf{p}_{b_{k+1}}^w = \mathbf{p}_{b_k}^w + \mathbf{v}_{b_k}^w \Delta t_k - \frac{1}{2} \mathbf{g}^w \Delta t_k^2 + \mathbf{R}_{b_k}^{w\top} \boldsymbol{\alpha}_{k,k+1}$$

**奖励函数**驱动智能体降低轨迹误差并惩罚过度自信但不准确的更新：

$$r_k = -\|\mathbf{p}_k - \mathbf{p}_{gt}\|_2^2 - \lambda \operatorname{Tr}(\boldsymbol{\Sigma}_k)$$

其中 $\boldsymbol{\Sigma}_k$ 是融合状态不确定性的低成本近似：

$$\boldsymbol{\Sigma}_k = \alpha \operatorname{diag}((\sigma_k^{\mathrm{imu}})^2) + \operatorname{diag}((1 - c_k^{\mathrm{vo}})^2)$$

$\sigma_k^{\mathrm{imu}}$ 为IMU残差标准差，$c_k^{\mathrm{vo}}$ 为VO置信度。该设计使智能体在VO不可靠时自动降低其权重，实现自适应融合。

---

### 系统初始化

初始化阶段将世界坐标系与初始IMU体坐标系对齐，设置 $\mathbf{p}_0^w = 0$，z轴对齐测量重力 $\mathbf{g}$。通过滑动窗口关键帧（Figure 3）收集IMU预积分，构建线性约束估计尺度 $s$ 和初始速度：

$$\mathbf{R}_{c_k}^w \mathbf{p}_{vo}^{(k,k+1)} s - \Delta t_k \mathbf{I} \mathbf{v}_{b_k}^w = \mathbf{R}_{b_k}^{w\top} \boldsymbol{\alpha}_{k,k+1} - \frac{1}{2} \mathbf{g}^w \Delta t_k^2 - (\mathbf{R}_{c_{k+1}}^w - \mathbf{R}_{c_k}^w) \mathbf{t}_{bc}$$

该约束将IMU传播位置与缩放后的VO平移关联，通过最小二乘求解尺度和速度初值。

![[assets/figures/papers/paper_list_l2715_https_arxiv_org_abs_2511_21083/figures/010_Figure_6.jpg]]
*Figure 6: Ablation study for the Select Agent (a) ATE vs. skip ratio comparing our IMU-only prior scheduling, fixed skipping, heuristic gating, and the RL-gating(KF) baseline (b) Throughput under a 50% skip target: IMU-only prior scheduling attains higher FPS than RL-gating(KF) with only a marginal ATE increase*

## 实验与关键发现

### 核心瓶颈与实验设计逻辑

本工作的根本瓶颈在于传统VIO中视觉-惯性束调整（VIBA）的高计算开销，导致在资源受限平台上难以实时运行。实验设计围绕两个因果调节变量展开：**是否运行视觉前端**（VO调度）与**以多大权重信任视觉输出**（视觉-惯性融合）。通过将这两个关键决策建模为序列决策问题，并利用轻量级RL智能体学习长期、成本感知的策略，系统在精度、吞吐量与显存占用之间实现了灵活权衡。

### 精度对比：与传统CPU-based VIO系统

在EuRoC MAV和TUM-VI两个标准数据集上，所提方法与经典CPU-based单目VIO系统进行了系统对比。

**EuRoC MAV数据集**（Table 1）：所提方法取得平均RMSE ATE **0.092 m**，略逊于DM-VIO的0.069 m（+0.023 m），但优于或可比于ORB-SLAM3、VINS-MONO、OKVIS等基线。值得注意的是，该精度是在大幅降低计算开销的前提下实现的——这是传统系统无法提供的权衡。

**TUM-VI数据集**（Table 2）：所提方法取得平均RMSE ATE **0.80 m**，与DM-VIO的0.77 m接近（+0.03 m），在部分场景（如room序列）中表现更具竞争力。完整逐序列结果见Table 8。

**关键洞察**：在精度接近最优传统方法的同时，所提方法在计算效率上取得结构性优势，这是传统紧耦合VIBA架构无法实现的。

### 计算效率突破：CPU侧BA/VIBA时间

Table 3揭示了本方法的核心效率优势来源。在EuRoC上，CPU侧的BA/VIBA时间从ORB-SLAM3的**121.09 ms**和DM-VIO的**26.49 ms**骤降至**12.77 ms**。这一结构性减少源于RL调度智能体仅在必要时激活VO流水线，从根本上降低了优化负担。BA/VIBA在所有方法中均在CPU上运行，因此该对比直接反映了调度策略带来的计算节省。

### GPU-based方法的精度-效率-显存权衡

Table 4将所提方法与SOTA GPU-based VO/VIO系统在EuRoC上进行了统一评估（所有方法在同一NVIDIA RTX 3090上运行，基线使用公开开源实现）。

| 方法 | 类型 | ATE (m) | 吞吐量 (FPS) | GPU显存 (GB) |
|------|------|---------|--------------|-------------|
| DPVO | VO | — | ~22 | — |
| DROID-VO | VO | — | — | ~7.98 |
| **Ours** | VIO | **最佳平均** | **39** | **4.37** |

所提方法在三个维度上均取得有利权衡：
- **精度**：达到最佳平均ATE（VIO方法中）
- **吞吐量**：**39 FPS**，比DPVO快**1.77倍**
- **显存**：**4.37 GB**，比DROID-VO降低**45.2%**

这一结果验证了RL调度策略的有效性——智能体学会了避免冗余计算，在维持精度的同时显著提升效率。

### 消融实验：组件贡献

**Table 9** 的累计消融实验揭示了各组件的互补作用：

- **移除IMU偏差编码器**：EuRoC上ATE从0.092增至**0.279**，TUM-VI上从0.80增至**1.13**，表明偏差估计对精度至关重要。
- **移除选择智能体**：FPS从39骤降至**21**，精度几乎不变，验证了调度策略的效率贡献。
- **移除融合智能体**：精度和效率均出现退化，验证了自适应融合的必要性。

这三个组件形成互补：偏差编码器保障精度基础，选择智能体提升效率，融合智能体在稀疏VO更新下维持精度。

### 融合策略消融

**Table 5** 对比了不同融合策略在EuRoC MH 04上的表现：

- **RL融合智能体**：ATE **0.112 m**
- 启发式融合：ATE 0.143 m
- EKF融合：ATE 0.127 m

RL融合策略显著优于传统融合方法，验证了学习自适应权重的优势。

### 调度策略消融

**Figure 6** 展示了不同调度策略的精度-效率权衡：

- **IMU-only先验调度**：在激进跳帧（75–87.5%跳过率）下维持平缓退化曲线，且吞吐量高于基于特征的RL-gating(KF)基线。
- 固定跳帧和启发式门控在同等跳过率下精度退化更剧烈。

这表明仅依赖IMU信号的先验调度既高效又鲁棒，避免了视觉特征计算的额外开销。

### 鲁棒性测试

**视觉退化鲁棒性**（Table 6）：在EuRoC MH 04上，将5%/10%图像替换为模糊噪声版本后，所提方法ATE退化受控。RL融合智能体在视觉质量下降时自适应降低VO权重，依赖IMU传播维持轨迹。

**跨数据集迁移**（Table 10）：使用KITTI预训练模型（Visual-Selective-VIO）在EuRoC上不重训练直接评估，验证了调度策略的泛化潜力。

**严重传感器退化压力测试**（Table 11）和**尺度鲁棒性测试**（Table 12）进一步验证了系统在VO中断、IMU噪声增大、初始化尺度误差等极端条件下的鲁棒性。

### 局限性与失败模式

基于分析揭示的局限性，需注意以下要点：

1. **泛化边界未充分验证**：仅训练和评估于EuRoC和TUM-VI，跨数据集迁移（Table 10）虽初步验证，但不同平台部署的泛化性有待系统评估。
2. **假设敏感性**：系统假设已校准的VO后端和成功的初始尺度估计。在持续VO退化或严重误校准情况下，当前策略可能无法自主恢复——这需要人工验证。
3. **硬件约束未直接建模**：所有实验在桌面级GPU/CPU上进行，延迟、功耗等真实世界硬件约束未纳入奖励设计。在嵌入式平台上的表现需进一步验证。
4. **长时序退化**：在长时间缺失视觉的场景下，IMU-only传播会累积漂移，当前系统缺乏主动重初始化机制。

### 开放问题

1. 如何将硬件约束（延迟、功耗、内存带宽）直接纳入RL奖励设计？
2. 能否训练更轻量的智能体以在嵌入式低功耗硬件上实时运行？
3. 如何扩展调度机制以协调共享边缘设备上的多个感知模块（VO、建图、语义）？
4. 能否设计主动检测失效并触发重初始化或回退行为的智能体？
5. 引入长时序上下文到置信度估计以进一步减少漂移的潜力。
6. 建立反馈机制，在长时间缺失视觉时利用IMU状态重新初始化VO后端。

![[assets/figures/papers/paper_list_l2715_https_arxiv_org_abs_2511_21083/figures/004_Table_1.jpg]]
*Table 1: Comparison with traditional CPU-based monocular visual-inertial odometry systems on the EuRoC MAV dataset. We report the SE(3)-aligned RMSE ATE (m). The Scale Error (%) row for our method reports the percentage error of our initial scale estimation*

![[assets/figures/papers/paper_list_l2715_https_arxiv_org_abs_2511_21083/figures/009_Table_4.jpg]]
*Table 4: Efficiency and resource comparison with SOTA GPU-based VO/VIO methods on the EuRoC MAV dataset. We report SE(3)- aligned RMSE ATE (m) for VIO, Sim(3) for VO, average throughput (FPS), and peak GPU VRAM usage (GB)*

![[assets/figures/papers/paper_list_l2715_https_arxiv_org_abs_2511_21083/figures/011_Table_5.jpg]]
*Table 5: Ablation study on the Adaptive Fusion Agent*

## 定位与知识库关联

### 1. 方法谱系：从紧耦合优化到解耦智能调度

本文的核心贡献在于将视觉-惯性里程计（VIO）中两个关键设计决策——**何时运行视觉前端**和**以多大权重信任视觉输出**——建模为序列决策问题，并用轻量级强化学习（RL）智能体求解。这一思路在现有VIO方法谱系中开辟了新的维度。

**传统VIO谱系**可大致分为两类：
- **基于滤波的方法**：如 **MSCKF**、**ROVIO**，通过扩展卡尔曼滤波（EKF）融合IMU与视觉观测，计算效率较高但精度受限于线性化误差。
- **基于优化的方法**：如 **OKVIS**、**VINS-MONO**、**VI-DSO**、**DM-VIO** 和 **ORB-SLAM3**，通过视觉-惯性束调整（VIBA）联合优化位姿与地标点，精度更高但计算开销显著。本文的Table 3揭示了这一瓶颈：ORB-SLAM3的CPU侧BA/VIBA耗时达121.09 ms，DM-VIO为26.49 ms，而本文方法降至12.77 ms。

**学习型VO/VIO谱系**近年来兴起：
- **端到端VO**：**DPVO** 和 **DROID-VO** 利用可微束调整在GPU上实现高精度视觉里程计，但缺乏IMU融合且计算资源消耗大（DROID-VO GPU显存占用约7.98 GB）。
- **学习型VIO**：**iSLAM** 等尝试将学习组件嵌入传统SLAM框架，但仍维持紧耦合的VIBA结构。

本文方法的定位是**解耦的、成本感知的VIO框架**：通过RL选择智能体在IMU空间进行先验调度，仅在必要时激活VO流水线；通过RL融合智能体自适应地组合IMU传播与稀疏VO更新。这本质上将VIO从“每帧必算”的紧耦合范式转变为“按需激活、自适应融合”的智能调度范式。

### 2. 关键设计槽位的变化

| 设计槽位 | 基线方法取值 | 本文方法取值 | 机制差异 |
|---------|------------|------------|---------|
| **VO调度策略** | 每帧运行VO/VIBA（如DM-VIO、ORB-SLAM3） | 基于IMU的RL选择智能体，仅在必要时激活VO | 将调度建模为MDP，终端奖励 $R_{\mathrm{episode}} = \frac{A}{\mathrm{ATE} + \epsilon} - B N_f$ 鼓励低ATE和少量VO调用 |
| **视觉-惯性融合权重** | 固定权重或优化为基础的VIBA联合估计 | RL融合智能体输出各轴融合权重 $\mathbf{W}_p, \mathbf{W}_v$ | 凸组合融合 $p_k = \mathbf{W}_p p_k^{\mathrm{VO}} + (\mathbf{I} - \mathbf{W}_p) p_k^I$，奖励函数 $r_k = -\|\mathbf{p}_k - \mathbf{p}_{gt}\|_2^2 - \lambda \mathrm{Tr}(\boldsymbol{\Sigma}_k)$ 驱动降低轨迹误差和不确定性 |
| **IMU偏差估计** | 在线估计（如VINS-MONO的滑动窗口优化） | 预训练的偏差编码器网络 $f_{bias}^g, f_{bias}^a$ | 推理时直接校正原始IMU测量，避免在线估计的计算开销 |

### 3. 适用边界与局限

**已验证的适用场景**：
- 在EuRoC MAV和TUM-VI数据集上，与经典CPU-based VIO系统（DM-VIO、ORB-SLAM3等）精度可比，同时显著降低计算开销。
- 在GPU-based方法统一评估中（Table 4），达到最佳平均ATE，吞吐量达39 FPS（比DPVO快1.77倍），GPU显存仅4.37 GB（比DROID-VO降低45.2%）。

**已知局限**（需手动验证的部分以明确标注）：
1. **数据集泛化性未充分验证**：仅训练和评估于EuRoC和TUM-VI，跨数据集迁移性能仅在Table 10中通过Visual-Selective-VIO的KITTI→EuRoC迁移做了初步测试。更广泛的场景（如室外大尺度、动态环境）泛化性需要额外验证。
2. **依赖已校准的VO后端**：系统假设VO模块和初始尺度估计成功。在持续VO退化或严重误校准情况下，当前策略未包含主动失效检测与重初始化机制。
3. **硬件平台局限**：所有实验在桌面级GPU（NVIDIA RTX 3090）和CPU（双Intel Xeon Platinum 8260）上进行，尚未在嵌入式或低功耗硬件上系统评估。这限制了方法在无人机、AR眼镜等资源受限平台上的适用性判断。
4. **未建模真实硬件约束**：当前奖励设计仅考虑ATE和VO调用次数，未直接纳入延迟、功耗、内存带宽等真实世界硬件约束。

### 4. 开放问题

1. **硬件约束的直接建模**：能否将延迟、功耗、内存等约束直接编码进奖励函数或状态空间，使智能体学习硬件感知的调度策略？
2. **轻量化部署**：当前RL智能体虽称为“轻量级”，但能否进一步压缩网络结构以在微控制器或NPU上高频运行？
3. **多任务协调调度**：如何扩展调度机制以协调共享边缘设备上的多个感知模块（VO、建图、语义分割），实现全局资源最优分配？
4. **主动失效恢复**：能否设计能够检测VO退化（如模糊、弱纹理）并主动触发重初始化或回退到纯惯性模式的智能体？
5. **长时序上下文建模**：引入更长时序的上下文信息到置信度估计中，以进一步减少漂移的潜力。
6. **IMU驱动的VO重初始化**：建立反馈机制，在长时间缺失视觉时利用累积的IMU状态重新初始化VO后端，形成闭环恢复。

## 原文 PDF

![[paperPDFs/CVPR_2026/Dual_Agent_Reinforcement_Learning_for_Adaptive_and_Cost_Aware_Visual_Inertial_Odometry.pdf]]
