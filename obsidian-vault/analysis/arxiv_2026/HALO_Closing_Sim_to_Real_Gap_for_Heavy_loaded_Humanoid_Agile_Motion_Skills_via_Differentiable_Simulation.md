---
title: "HALO: Closing Sim-to-Real Gap for Heavy-loaded Humanoid Agile Motion Skills via Differentiable Simulation"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/HALO_Closing_Sim_to_Real_Gap_for_Heavy_loaded_Humanoid_Agile_Motion_Skills_via_Differentiable_Simulation.pdf
project_link: null
code_link: null
aliases:
- HHLHMC
- HALO
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 两阶段可微系统识别（two-stage differentiable SysID）：先使用无载荷轨迹校准基座模型以消除固有仿真-真实偏差，再使用有载轨迹仅优化有效载荷相关的质量与质心参数，避免误差归因混乱，从而准确恢复重载动力学，为后续RL策略提供高保真仿真环境。
primary_logic: 通过分阶段解耦标称模型校准与有效载荷参数估计，并利用可微仿真提供的解析梯度进行高效轨迹级优化，可以在仅用关节编码器的条件下稳定、精准地识别重载的质量分布，使得零样本迁移的RL策略在真实重载任务中依然保持敏捷性与鲁棒性。
claims:
- 两阶段识别策略有效解耦了全局模型误差与局部有效载荷变化，避免错误归因。
- 在极端重载条件下，CMA-ES（单阶段零阶方法）收敛至物理上不合理的局部最优，而HALO的梯度优化稳健收敛至参考参数附近。
- HALO使真实重载前向行走的最大位置误差（E_fpos）相比WDR降低73.33%，相比CMA-ES基线降低45.45%；终点残余误差（E_epos）分别降低70.79%和42.22%。
- HALO在真实重载的90°原地跳跃任务中将角度跟踪误差（E_ang）降低72.97%，并在三项高敏捷挑战动作（ swallow balancing, side kicking, roundhouse kicking ）中达到100%成功率。
---

# HALO: Closing Sim-to-Real Gap for Heavy-loaded Humanoid Agile Motion Skills via Differentiable Simulation

> [!tip] 核心洞察
> 通过分阶段解耦标称模型校准与有效载荷参数估计，并利用可微仿真提供的解析梯度进行高效轨迹级优化，可以在仅用关节编码器的条件下稳定、精准地识别重载的质量分布，使得零样本迁移的RL策略在真实重载任务中依然保持敏捷性与鲁棒性。

| 字段 | 内容 |
|------|------|
| 中文题名 | HALO：基于可微仿真弥合重载人形机器人敏捷运动的仿真-真实差距 |
| 英文题名 | HALO: Closing Sim-to-Real Gap for Heavy-loaded Humanoid Agile Motion Skills via Differentiable Simulation |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2603.15084) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | HALO (HeAvy-LOaded humanoid motion control) |
| Dataset | Steady-state motion tracking, High-agility motion tracking, Walking forward/backward, In-place 90° yaw jumping |

> [!tip] 效果简介
> - Steady-state motion tracking (sim) 上，E_g-mpjpe (mm) 52.47 ± 2.11 vs WDR 94.91 ± 3.21, CM 85.87 ± 2.54 (↓44.7% vs WDR, ↓38.9% vs CM)。
> - High-agility motion tracking (sim) 上，E_g-mpjpe (mm) 78.83 ± 2.55 vs WDR 132.89 ± 2.89, CM 92.82 ± 3.21 (↓40.7% vs WDR, ↓15.1% vs CM)。
> - Walking forward/backward (real, heavy load) 上，E_fpos (m) 0.12 ± 0.03 vs WDR 0.45 ± 0.13, CM 0.22 ± 0.09 (↓73.33% vs WDR, ↓45.45% vs CM)。

## 概要

人形机器人在执行物流搬运、灾难救援等任务时，常需携带未知重载，而有效载荷会大幅改变系统的质量、质心与惯量分布，导致仿真与真实之间出现**结构化的动力学失配**（structured sim-to-real gap）。传统域随机化（domain randomization）策略虽能提升鲁棒性，但在重载条件下往往产生保守行为，运动精度急剧下降；而单阶段系统识别方法无法解耦标称模型误差与有效载荷误差，参数估计存在归因偏差，策略迁移后性能显著退化。

**HALO** 针对上述瓶颈，提出**两阶段可微系统识别**（two-stage differentiable SysID）框架：**阶段一**利用无载荷轨迹校准基座模型，消除固有仿真-真实偏差；**阶段二**以校准模型为起点，仅优化有效载荷相关的质量与质心参数，避免误差归因混乱。该方法在 **MuJoCo XLA** 可微物理仿真中利用解析梯度进行轨迹级优化，仅依赖关节编码器即可稳定、精准地恢复重载动力学，为后续强化学习策略提供高保真仿真环境。

**核心结论：**
- 在真实重载前向行走任务中，HALO 的最大位置误差（E_fpos）相比广域域随机化（WDR）降低 **73.33%**，相比 CMA-ES 基线降低 **45.45%**；终点残余误差（E_epos）分别降低 **70.79%** 和 **42.22%**。
- 在真实重载 90° 原地跳跃任务中，HALO 将角度跟踪误差（E_ang）降低 **72.97%**（CMA-ES 基线），WDR 策略则完全失败。
- 在三项高敏捷挑战动作（swallow balancing、side kicking、roundhouse kicking）中，HALO 达到 **100%** 成功率，而 WDR 全部失败，CMA-ES 成功率均低于 70%。

**方法定位：** HALO 属于基于可微仿真的系统识别与 sim-to-real 迁移范式，其两阶段解耦策略区别于传统的单阶段参数估计或纯域随机化方法，为重载人形机器人的零样本敏捷运动部署提供了新的技术路线。

人形机器人在物流、制造与家庭服务等场景中，常需在携带未知重载的条件下执行敏捷运动任务。有效载荷的引入会显著改变系统的质量分布、质心位置与惯性张量，导致仿真环境与真实物理之间出现**结构化、大尺度的动力学失配**（structured sim-to-real gap）。这种失配并非随机扰动，而是由载荷引起的系统性偏移，使得在标称仿真中训练的控制策略直接迁移至真实重载场景时性能急剧退化，甚至完全失效。

现有应对仿真-真实差距的主流范式存在明显局限。**域随机化（Domain Randomization, DR）**通过在训练时对质量、质心、关节编码器偏置等物理参数施加广域扰动来训练鲁棒策略（Peng et al., ICRA 2018）。然而，面对重载引起的大幅参数偏移，广域随机化往往迫使策略学习过于保守的行为，牺牲敏捷性与跟踪精度。另一类方法采用**系统识别（System Identification, SysID）**在仿真中估计真实物理参数，例如基于协方差矩阵自适应进化策略（CMA-ES）的零阶优化方法。但这类单阶段识别将标称模型误差与有效载荷误差混合优化，导致**误差归因混乱**：优化器可能将有效载荷的质量错误地分配到其他身体环节，或收敛至物理上不合理的局部最优——尤其在极端重载条件下，CMA-ES会出现质量估计为负值等违反物理常识的结果（见Table II）。

上述困境的核心瓶颈在于：**标称模型的固有偏差与有效载荷引入的局部变化相互耦合，难以在单一优化阶段中被解耦辨识**。若不能准确恢复重载条件下的动力学参数，后续强化学习（RL）策略便无法获得高保真的仿真训练环境，零样本迁移的性能上限因此被锁定。

HALO的动机正是针对这一瓶颈：通过**两阶段可微系统识别**，先利用无载荷轨迹校准基座模型以消除固有仿真-真实偏差，再利用有载轨迹仅优化有效载荷相关的质量与质心参数，从根本上避免误差归因混乱。借助MuJoCo XLA可微仿真的解析梯度，该框架能以轨迹级优化高效收敛至准确的物理参数，为RL策略提供高保真仿真环境，从而在真实重载任务中同时保持敏捷性与鲁棒性。

## 核心方法与创新机理

HALO 的核心创新在于**将重载人形机器人的仿真-真实迁移问题重新表述为一种分阶段、可微的系统识别范式**，通过解耦标称模型误差与有效载荷动力学偏移，从根本上解决了传统方法在面对大尺度、结构化动力学失配时的保守行为与参数估计偏差。

### 1. 两阶段可微系统识别：解耦标称模型与有效载荷

传统的域随机化（WDR）或单阶段系统识别方法（如 CMA-ES）在面对重载时存在根本性缺陷：它们将基座模型的固有仿真-真实偏差与有效载荷引起的质量/质心偏移混为一谈，导致参数估计被错误归因，策略迁移后性能急剧下降。

HALO 的核心洞察在于**通过分阶段解耦来消除这一混淆**：

- **阶段一：基座模型校准**。首先在无载荷条件下，利用可微仿真对全部模型参数（质量、质心、关节阻尼、摩擦等）进行轨迹级优化，消除机器人本体固有的仿真-真实偏差。这一步骤建立了高保真的标称动力学模型。

- **阶段二：有效载荷参数识别**。以校准后的模型为起点，在有载条件下仅优化与有效载荷直接相关的参数——即躯干和手部等附着载荷环节的质量与质心位置。通过固定已校准的基座参数，优化过程被严格约束在有效载荷引入的局部动力学变化上。

**证据支撑**：消融实验（Table IV, Fig. 4）证实了两阶段策略的有效性。HALO 识别的躯干质量为 $13.83 \pm 0.43$ kg，与参考值 $13.82$ kg 高度吻合；而单阶段方法仅达到 $12.93 \pm 0.32$ kg，显著低估了有效载荷质量。论文明确指出：“This improvement suggests that our coarse-to-fine strategy effectively decouples global modeling errors from local payload variations.”

### 2. 梯度优化替代零阶搜索：鲁棒收敛与物理合理性

HALO 的第二个关键创新在于**利用可微仿真提供的解析梯度进行高效轨迹级优化**，替代传统系统识别中常用的零阶进化算法（CMA-ES）。

CMA-ES 作为零阶方法，在高维参数空间中依赖种群采样，缺乏梯度引导，在极端重载条件下容易收敛至物理上不合理的局部最优。相比之下，HALO 通过 MuJoCo XLA 可微仿真计算整个轨迹的解析梯度，使优化过程能够稳健地向参考参数收敛。

**证据支撑**：在极端重载扰动设置下（Table II），CMA-ES 的躯干质量估计偏差高达 $+12.43 \pm 0.92$ kg（参考值 $+6.00$ kg），而 HALO 的估计为 $+11.99 \pm 0.00$ kg，显著更接近参考值。论文明确指出：“under extremely heavy-loaded conditions (e.g., Perturbation Setting 3), CMA-ES using certain seeds converge to local optima with physically unreasonable values, whereas our gradient-based method robustly converges to the vicinity of the reference parameters.”

### 3. 仅依赖关节编码器的数据采集管线

HALO 的第三个重要创新是**摆脱了对运动捕捉系统或关节扭矩传感器的依赖**，仅使用机器人自身的关节编码器完成系统识别所需的数据采集。

具体而言，通过机械约束（台钳）固定机器人的一只脚，利用正向运动学从关节状态重建全身笛卡尔轨迹。为消除传感器噪声导致的左右脚高度不一致问题，HALO 在每个时间步求解一个带约束的二次规划（QP），以最小调整根节点和下肢关节增量，强制被约束脚保持地面接触。这一设计使得数据采集可以在任意实验室环境中完成，极大降低了系统识别的硬件门槛。

### 4. 零样本迁移的敏捷运动策略

基于识别后的高保真动力学参数，HALO 在仿真中使用 PPO 训练运动模仿策略，随后直接零样本部署至真实重载人形机器人。这一端到端管线使得策略在真实世界中依然保持敏捷性与鲁棒性，无需任何在线自适应或微调。

**证据支撑**：真实重载实验中，HALO 相比 WDR 将前向行走最大位置误差降低 $73.33\%$，相比 CMA-ES 降低 $45.45\%$；在 $90^\circ$ 原地跳跃任务中将角度跟踪误差降低 $72.97\%$；在三项高敏捷挑战动作（燕式平衡、侧踢、回旋踢）中达到 $100\%$ 成功率，而基线方法均出现任务失败。

HALO 面向重载人形机器人的仿真-真实迁移，构建了一条从数据采集到零样本部署的完整管线。其核心思路是将有效载荷引起的结构化动力学失配建模为可解耦的参数识别问题，而非单纯依靠域随机化进行保守的鲁棒训练。

**管线总览**（参见 Figure 2）：

1. **轨迹数据采集**：在真实机器人上，使用宽域随机化（WDR）预训练的探索策略，分别在无载荷和有载荷两种状态下收集关节轨迹。采集时通过机械夹具将机器人一只脚固定，从而仅依赖关节编码器即可通过正向运动学重建全身笛卡尔轨迹，无需运动捕捉系统或关节扭矩传感器。

2. **数据处理与足高对齐**：传感器噪声会导致左右脚在世界坐标系中的高度不一致（例如，固定脚本应贴地却呈现悬空）。HALO 在每个时间步求解一个带约束的二次规划（QP），对根节点和下肢关节增量进行最小调整，以消除足高差异，恢复物理一致的地面接触（Figure 3）。

3. **两阶段可微系统识别**：这是 HALO 的核心模块。系统识别被形式化为轨迹匹配优化问题——在可微物理仿真器 MuJoCo XLA 中，以真实控制序列驱动仿真模型，最小化仿真轨迹与真实轨迹之间的跟踪损失与正则化项之和。优化分两阶段进行：
   - **阶段一（基座模型校准）**：利用无载荷轨迹优化全部模型参数（质量、质心、关节阻尼等），消除仿真模型固有的标称偏差。
   - **阶段二（有效载荷参数识别）**：以校准后的模型为起点，利用有载轨迹仅优化与有效载荷附着相关的躯干和手部环节的质量与质心参数，避免将全局模型误差错误归因到局部载荷变化上。

4. **重载运动技能学习**：基于识别后的高保真动力学参数，在仿真中使用 PPO 训练运动模仿策略。策略以关节状态和身体姿态跟随参考轨迹为目标，训练完成后直接零样本部署至真实重载人形机器人，无需在线自适应或额外微调。

**输入输出流**：管线输入为真实机器人的关节编码器数据与控制指令序列，输出为可直接部署的敏捷运动控制策略。中间产物为校准后的仿真动力学模型参数。整个过程仅需一次离线数据采集和系统识别，策略训练完全在仿真中完成，实现了从“真实数据→识别模型→仿真训练→真实部署”的闭环。

**关键设计选择**：
- **可微仿真梯度**：利用 MuJoCo XLA 提供的解析梯度进行轨迹级优化（学习率：质量 0.03，质心位置 0.0002），相比 CMA-ES 等零阶方法在极端载荷下具有更强的收敛鲁棒性。
- **解耦识别策略**：两阶段设计是弥合结构化 sim-to-real gap 的核心机制，消融实验表明其参数估计精度显著优于单阶段直接优化所有参数的方法（Figure 4）。

![[assets/figures/papers/paper_list_l50_https_arxiv_org_abs_2603_15084/figures/002_Figure_2.jpg]]
*Figure 2: Overview of HALO. (a) Data Collection: Trajectories are collected under both loaded and unloaded conditions using exploration policy trained with wide DR, followed by real-world deployment with a fixed foot constraint. (b) Data Processing: Full-body trajectories reconstruction from joint-state measurements via forward kinematics and foot-height alignment. (c) Two-stage Payload-related Parameter Identification: Stage 1 optimize the full set of model parameters to yield a calibrated base model using trajectories without payload. Based on the calibrated model, stage 2 optimize only the payload-related parameters, using trajectories collected under loaded conditions. (d) Heavy-loaded Motion Ski...*

HALO 的核心管线由四个模块串联构成（对应 Figure 2），其理论根基是将系统识别形式化为可微仿真中的**轨迹级优化问题**，并通过两阶段解耦策略实现重载参数的精准估计。

### 模块一：轨迹数据采集

在真实机器人上，使用**广域域随机化（WDR）**训练的探索策略分别收集无载荷和有载荷状态下的关节位置与控制目标轨迹。为去除对外部运动捕捉系统的依赖，HALO 将机器人一只脚通过台钳机械固定，使全身笛卡尔轨迹可通过正向运动学从关节编码器测量值中重建。这一约束同时保证了数据采集过程中机器人本体与地面的稳定接触。

### 模块二：数据处理与足高对齐

由于关节编码器噪声和机械间隙，正向运动学重建的左右脚高度常出现物理不一致——例如右脚本应着地却悬空（Figure 3a）。HALO 在每个时间步求解一个**约束二次规划（QP）**，对根关节和下肢关节增量进行最小调整，消除足高差异：

$$\min_{\Delta \mathbf{q}} \ \|\Delta \mathbf{q}\|^2 \quad \text{s.t.} \quad h_{\text{foot}}(\mathbf{q} + \Delta \mathbf{q}) = 0$$

其中 $\mathbf{q}$ 为当前关节构型，$h_{\text{foot}}$ 为足部高度函数，约束强制固定脚保持地面接触。优化后的轨迹确保物理一致的地面接触（Figure 3b），为后续系统识别提供干净数据。

### 模块三：两阶段可微系统识别

这是 HALO 的核心理论贡献。系统识别被形式化为在可微物理仿真中最小化轨迹匹配误差的优化问题。

**问题形式化**：设真实系统状态转移为 $s_{i+1}^r = \Phi_{\mathrm{real}}(s_i^r, a_i^r; \pmb{\theta}^r)$，仿真转移为 $s_{i+1}^s = \Phi_{\mathrm{sim}}(s_i^s, a_i^r; \pmb{\theta})$，两者使用相同的控制序列 $a_i^r$。优化目标为：

$$\min_{\pmb{\theta}} \ \mathcal{L}_{\mathrm{total}}(\pmb{\theta}) = \mathcal{L}_{\mathrm{track}}(\pmb{\theta}) + \mathcal{R}(\pmb{\theta})$$

其中跟踪损失 $\mathcal{L}_{\mathrm{track}}$ 分解为全身位置误差与上半身加权误差之和：

$$\mathcal{L}_{\mathrm{track}}(\pmb{\theta}) = \mathcal{L}_{\mathrm{track}}^{\text{all}}(\pmb{\theta}) + \alpha^u \mathcal{L}_{\mathrm{track}}^{\text{upper}}(\pmb{\theta})$$

上半身加权项 $\alpha^u > 1$ 反映了有效载荷对躯干和手部运动的影响更为显著。正则化项 $\mathcal{R}$ 由四部分构成：

$$\mathcal{R}_{\mathrm{total}} = \lambda_{\mathrm{com}} \mathcal{R}_{\mathrm{com}} + \lambda_{\mathrm{mass}} \mathcal{R}_{\mathrm{mass}} + \lambda_{\mathrm{damp}} \mathcal{R}_{\mathrm{damp}} + \lambda_{\mathrm{fric}} \mathcal{R}_{\mathrm{fric}}$$

分别惩罚质心位移、质量变化、关节阻尼和摩擦偏离标称值。参数约束通过软边界函数实现：

$$\phi(\alpha; l, u) = \max(0, l - \alpha)^2 + \max(0, \alpha - u)^2$$

仅当参数 $\alpha$ 超出区间 $[l, u]$ 时产生二次惩罚。

**梯度优化**：利用 MuJoCo XLA 可微仿真提供的解析梯度，参数通过梯度下降迭代更新：

$$\pmb{\theta}_{k+1} = \pmb{\theta}_k - \eta \nabla_{\theta} \mathcal{L}_{\mathrm{total}}(\pmb{\theta}_k)$$

学习率设置为：质量参数 0.03，质心位置参数 0.0002。与 CMA-ES（零阶进化算法，种群规模 10）相比，解析梯度在极端重载条件下避免了收敛至物理不合理局部最优的问题（Table II）。

**两阶段策略**：阶段一使用无载荷轨迹优化全部模型参数（质量、质心、关节阻尼等），校准基座模型以消除固有仿真-真实偏差；阶段二以校准模型为起点，使用有载轨迹**仅优化**与有效载荷附着环节（躯干、手部）相关的质量与质心参数。这一粗到细的解耦设计避免了将全局模型误差错误归因于有效载荷变化。

### 模块四：重载运动技能学习

基于识别后的动力学参数，在 mjlab 框架中使用 PPO 训练运动模仿策略。奖励函数鼓励关节状态与身体姿态跟随参考轨迹，随后直接零样本部署至真实重载人形机器人。所有策略使用相同的 MLP 网络架构和 PPO 超参数，域随机化范围保持一致以保证公平对比（Table I）。

![[assets/figures/papers/paper_list_l50_https_arxiv_org_abs_2603_15084/figures/007_Figure_4.jpg]]
*Figure 4: Comparison of convergence performance between two-stage and one-stage methods. The proposed Two-Stage method HALO (orange) demonstrates superior accuracy, converging significantly closer to the estimated reference values (red dashed lines) compared to the One-Stage baseline (blue)*

## 实验与关键发现

### 核心实验设计逻辑

实验验证围绕一个中心命题展开：**两阶段可微系统识别能否在重载条件下准确恢复动力学参数，从而使零样本迁移的RL策略保持敏捷性与鲁棒性？** 为此，作者构建了三条递进的证据链——(1) 参数估计的收敛性与准确性，(2) 仿真环境中的运动跟踪精度，(3) 真实世界重载任务的表现与成功率。基线选择具有明确的对比维度：**WDR**（Peng et al., ICRA 2018）代表“不识别、纯鲁棒化”的策略，**CMA-ES-based SysID (CM)** 代表“单阶段零阶识别”策略，两者共同覆盖了当前应对sim-to-real gap的主流范式。

### 参数识别：梯度优化与两阶段解耦的双重优势

**Table II** 报告了CMA-ES与HALO在三组递增有效载荷扰动下的参数估计收敛结果。在轻度扰动（Setting 1, 2）下，两者均能收敛至参考值附近，表现相当。然而，在极端重载条件（Setting 3）下，差距显著拉大：CMA-ES的部分随机种子收敛至物理上不合理的局部最优，躯干质量估计偏移高达+12.43±0.92 kg（参考值+6.00 kg），左手质量偏移+4.79±2.74 kg（参考值+2.40 kg），标准差暴露了零阶优化的不稳定性。相比之下，HALO利用MuJoCo XLA的解析梯度，在相同2000次迭代内稳健收敛至参考参数附近（躯干+11.99±0.00 kg，左手+3.50±0.00 kg）。

这一对比揭示了**因果机制**：零阶方法在高维参数空间中缺乏有效的梯度信号引导，容易陷入局部最优；而可微仿真提供的轨迹级解析梯度将“参数→多步状态轨迹”的全局依赖编码为明确的下降方向，在极端动力学偏移下仍能保持收敛方向正确。值得注意的是，HALO对质量参数使用0.03的学习率，对质心位置使用0.0002的学习率，这种差异化的学习率设置反映了两类参数对轨迹误差敏感度的本质不同。

**Two-Stage vs. One-Stage消融实验**（Table IV, Figure 4）进一步验证了分阶段解耦的必要性。单阶段方法直接优化所有参数，将标称模型误差与有效载荷误差混为一谈，导致误差归因混乱——其估计的躯干质量为12.93±0.32 kg，显著偏离参考值13.82 kg。HALO的两阶段策略先通过无载荷轨迹校准基座模型，再仅优化载荷相关参数，估计的躯干质量达到13.83±0.43 kg，与参考值高度吻合。正如原文所断言：“This improvement suggests that our coarse-to-fine strategy effectively decouples global modeling errors from local payload variations”——这一解耦机制是HALO参数识别准确性的根本保障。

### 仿真运动跟踪：精度提升的量化证据

**Table III** 报告了在仿真环境中，基于识别后动力学参数训练的RL策略的运动跟踪性能。指标 $E_{\text{g-mpjpe}}$ 衡量全局平均关节位置误差（mm），越低越好。

在稳态运动跟踪任务中，HALO取得52.47±2.11 mm，相比WDR（94.91±3.21 mm）降低44.7%，相比CM（85.87±2.54 mm）降低38.9%。在高敏捷运动跟踪任务中，HALO取得78.83±2.55 mm，相比WDR（132.89±2.89 mm）降低40.7%，相比CM（92.82±3.21 mm）降低15.1%。

两个观察值得注意：第一，WDR在高敏捷任务中性能急剧恶化（132.89 mm），说明广域随机化训练的策略在动力学大幅偏移时趋于保守，无法精准执行快速动作；第二，CM在高敏捷任务中与HALO的差距（15.1%）小于稳态任务（38.9%），暗示单阶段识别在动态激励更丰富时可能部分补偿参数归因误差，但仍无法达到两阶段解耦的精度。

### 真实世界重载任务：零样本迁移的决胜证据

真实世界实验在人形机器人平台上进行，有效载荷配置固定，采用相同的关节PD控制器，所有策略零样本部署，无任何在线适配。**Table V** 报告了重载双向行走与90°原地跳跃的定量结果。

**行走任务**定义了两个核心指标：$E_{\text{fpos}}$（最大前向位置误差，m）和 $E_{\text{epos}}$（终点残余误差，m）。HALO的 $E_{\text{fpos}}$ 为0.12±0.03 m，相比WDR（0.45±0.13 m）降低73.33%，相比CM（0.22±0.09 m）降低45.45%。$E_{\text{epos}}$ 为0.26±0.07 m，相比WDR（0.89±0.15 m）降低70.79%，相比CM（0.45±0.13 m）降低42.22%。WDR的终点残余误差高达0.89 m，表明即使训练时施加了广域随机化，缺乏精确参数估计的策略在真实重载下仍会产生系统性漂移。

**跳跃任务**中，WDR直接失败（task failure），无法完成90°原地偏航跳跃。CM虽能执行，但角度跟踪误差 $E_{\text{ang}}$ 高达41.8±3.6°。HALO将误差降至11.3±2.1°，降幅达72.97%。这一结果说明：高敏捷任务对动力学精度极为敏感，参数偏差导致的力矩计算错误在快速运动中会被急剧放大，而HALO的精确参数估计为策略提供了可靠的动力学先验。

**Table VI** 展示了三项高难度挑战动作的成功率对比：swallow balancing（燕式平衡）、side kicking（侧踢）、roundhouse kicking（回旋踢）。HALO在所有任务中均取得10/10的100%成功率。WDR三项任务全部0/10失败。CM分别取得5/10、7/10、5/10，成功率均未超过70%。这组数据构成了HALO方法有效性最直观的证据——在需要精细平衡控制与快速重心转移的动作中，只有精确的动力学参数才能使RL策略在零样本条件下可靠执行。

### 失败模式与边界条件分析

尽管整体表现优异，实验中仍可识别出若干边界条件与潜在失败模式：

1. **WDR的保守性陷阱**：广域随机化迫使策略在训练时适应极宽的参数分布，导致其学习到的是“对所有可能动力学都安全”的保守行为，而非针对真实动力学的精准控制。这在行走任务中表现为系统性漂移，在高敏捷任务中直接导致任务失败。

2. **CMA-ES的局部最优困境**：零阶优化在极端重载下收敛至物理不合理的参数值（Table II, Setting 3），这些错误参数若用于策略训练，将导致仿真与真实之间的残余动力学失配，进而损害策略迁移性能。

3. **两阶段策略的隐含假设**：第二阶段仅优化有效载荷相关的质量与质心参数，未对惯性张量进行估计。在质量分布极度不对称的载荷场景下，这一简化可能成为精度瓶颈——但当前实验载荷配置尚未触及该边界。

4. **数据采集的物理约束依赖**：固定一脚的机械约束（台钳）是轨迹重建精度的保障，但这也意味着当前方法无法在自由行走中实现在线系统识别，限制了其向动态变化载荷场景的扩展。

### 实验公平性保障

所有RL策略使用相同的MLP网络架构与PPO超参数，在相同的MuJoCo环境中训练，域随机化范围设定一致（详见表I）。系统识别阶段HALO与CMA-ES均运行2000次迭代。真实世界实验在同一机器人平台、相同有效载荷配置、相同关节PD控制器下执行。参考运动轨迹保持一致。这些控制措施确保了性能差异可归因于系统识别策略本身，而非训练或实验条件的混杂因素。

![[assets/figures/papers/paper_list_l50_https_arxiv_org_abs_2603_15084/figures/005_Table.jpg]]
*Table: II: Convergence comparison between CMA-ES and HALO. Results are reported as mean ± standard deviation. Groundtruth values (e.g., +6.000, +2.4000) denote the incremental offsets added to the absolute nominal values. Bold values indicate performance closer to the ground truth. While CMA-ES converges under light payloads, it exhibits sensitivity to random seeds under heavy payloads*

![[assets/figures/papers/paper_list_l50_https_arxiv_org_abs_2603_15084/figures/006_Table.jpg]]
*Table: III: Experimental results of motion tracking performance across various tasks*

![[assets/figures/papers/paper_list_l50_https_arxiv_org_abs_2603_15084/figures/010_Table.jpg]]
*Table: IV: Summary of identified parameters*

![[assets/figures/papers/paper_list_l50_https_arxiv_org_abs_2603_15084/figures/011_Table.jpg]]
*Table: VI: Comparison of success rates for performing challenging maneuvers between HALO and baselines*

## 定位与知识库关联

### 问题定位：重载人形机器人的结构化仿真-真实差距

人形机器人在携带未知重载时面临一个独特且严峻的挑战：有效载荷会引起系统质量、质心位置和惯量张量的大幅偏移，导致仿真环境与真实物理系统之间出现**结构化的、大尺度的动力学失配**（structured sim-to-real gap）。这种失配并非简单的噪声或随机扰动，而是系统性的参数偏差，使得在仿真中训练的控制策略直接迁移到真实重载场景时性能急剧退化。

传统的应对策略主要分为两类，各自存在根本性局限：

- **域随机化（Domain Randomization, DR）**：在训练时对物理参数施加广域随机扰动，迫使策略学会对参数变化鲁棒。然而，当参数偏移幅度过大时（如躯干质量增加数公斤），DR往往导致策略趋于保守，丧失敏捷性。论文中采用的**WDR基线**（Peng et al., ICRA 2018 ）即属于此类方法，其核心思想是在仿真中对质量、质心、关节编码器偏置等施加广域随机化，直接训练鲁棒策略，但**不使用显式系统识别**来恢复真实的动力学参数。

- **单阶段系统识别（Single-Stage SysID）**：在仿真中直接优化所有物理参数以匹配真实轨迹数据。论文中的**CM基线**采用协方差矩阵自适应进化策略（CMA-ES）进行零阶优化，估计物理参数。然而，该方法**不区分标称模型误差与有效载荷误差**，导致两类误差的归因相互混淆——标称模型的固有偏差可能被错误地吸收进有效载荷参数估计中，反之亦然。实验证实，在极端重载条件下（Perturbation Setting 3），CMA-ES使用某些随机种子会收敛至物理上不合理的局部最优，而HALO的梯度优化则稳健收敛至参考参数附近（Table II）。

### HALO的核心创新：两阶段可微系统识别

HALO的方法论突破在于**将标称模型校准与有效载荷参数估计解耦为两个独立阶段**，并利用可微仿真提供的解析梯度进行高效的轨迹级优化。这一设计的因果逻辑如下：

1. **阶段一（Base Model Calibration）**：利用**无载荷**轨迹数据优化全部模型参数（质量、质心、关节阻尼等），消除仿真模型固有的系统性偏差。此时优化的目标是标称模型本身，不受有效载荷干扰。

2. **阶段二（Payload Parameter Identification）**：以阶段一校准后的模型为起点，利用**有载荷**轨迹数据，**仅优化与有效载荷附着相关的环节参数**（躯干、手部的质量与质心位置）。由于标称模型误差已在阶段一消除，此阶段的优化信号纯粹来源于有效载荷引起的动力学变化，避免了误差归因的混淆。

这种“粗到精”（coarse-to-fine）的策略在消融实验中得到了直接验证：两阶段方法（HALO）估计的躯干质量为13.83±0.43 kg，显著优于一阶段方法的12.93±0.32 kg，且更接近参考值13.82 kg（Table IV）。论文明确指出：“This improvement suggests that our coarse-to-fine strategy effectively decouples global modeling errors from local payload variations.”

### 技术路径对比：梯度优化 vs 零阶优化

HALO在优化方法层面也做出了关键选择：**使用可微仿真（MuJoCo XLA）的解析梯度进行参数更新，而非CMA-ES等零阶进化算法**。

- **CMA-ES基线**：配置种群规模为10，通过对参数空间采样来估计梯度方向。在参数维度较高或优化景观复杂时，零阶方法容易陷入局部最优，且收敛速度较慢。

- **HALO梯度优化**：利用公式 $\pmb{\theta}_{k+1} = \pmb{\theta}_k - \eta \nabla_{\theta} \mathcal{L}_{\mathrm{total}}(\pmb{\theta}_k)$ 进行迭代更新，其中质量参数学习率为0.03，质心位置学习率为0.0002。解析梯度提供了精确的优化方向，使得HALO在极端扰动下仍能稳健收敛。

实验对比（Table II）显示：在轻载扰动下两者性能相当，但在极端重载条件下，CMA-ES的估计值出现物理上不合理的偏差（如左手质量偏移+4.7885±2.7441 kg），而HALO保持高精度（+3.5014±0.0000 kg）。

### 数据采集方式的简化

HALO的另一个重要设计选择是**仅依赖关节编码器进行数据采集**，而不使用运动捕捉系统或关节扭矩传感器。通过在真实机器人上将一只脚用两个台钳机械固定，HALO利用正向运动学从关节状态重建全身笛卡尔轨迹，并通过求解带约束的二次规划（QP）以消除传感器噪声导致的左右脚高度不一致问题（Fig. 3）。这种简化的数据采集方式降低了硬件门槛，但同时也引入了**固定脚约束**的限制——该方法无法直接应用于自由行走场景中的在线系统识别。

### 适用边界与局限性

HALO的方法论边界主要体现在以下几个方面：

1. **参数估计范围受限**：第二阶段仅优化有效载荷相关的质量与质心位置，**未对惯性张量进行估计**。对于质量分布复杂的有效载荷（如非均匀密度的物体），这一简化可能限制控制精度的进一步提升。

2. **数据采集依赖机械约束**：固定脚的数据采集方式要求机器人处于受约束状态，无法在自由运动中实现在线增量更新。这限制了HALO在载荷随时间缓慢变化场景（如液体消耗）中的应用。

3. **仿真平台依赖性**：整个管线依赖MuJoCo XLA可微仿真的解析梯度，向其他仿真平台（如Isaac Gym、PyBullet）迁移时需要额外的适配工作。

4. **探索策略的局限性**：数据采集阶段使用的探索策略依赖预定义的固定脚参考轨迹进行模仿训练，可能无法充分激发所有动力学模式，导致某些参数的可辨识性不足。

5. **验证场景有限**：真实世界实验仅在有限的有效载荷配置和实验室环境中进行，极度动态变化的载荷或野外地形下的表现尚未测试。

### 开放问题

HALO框架留下了若干值得后续探索的方向：

- **在线增量识别**：两阶段识别流程能否实现在线增量更新，以适应随时间缓慢变化的载荷（如液体消耗、磨损引起的质量变化）？

- **无约束数据采集**：固定脚约束能否被基于IMU与视觉的即时足底接触估计替代，从而去除机械约束，实现自由行走中的系统识别？

- **惯性张量估计**：如何将惯性张量有效纳入第二阶段优化，同时保持数值稳定性和样本效率？这可能需要更丰富的激励轨迹设计。

- **初始误差敏感性**：当前框架对不同初始标称参数误差的敏感性如何？若标称模型与真实模型相差过大（如使用完全不同的机器人平台），两阶段策略是否仍然有效？

- **鲁棒性与安全边界**：所生成的敏捷运动策略在承受突发外部冲击（如碰撞、推力干扰）时的安全边界和泛化能力如何？这涉及从参数识别到策略鲁棒性的完整闭环验证。

## 原文 PDF

![[paperPDFs/arxiv_2026/HALO_Closing_Sim_to_Real_Gap_for_Heavy_loaded_Humanoid_Agile_Motion_Skills_via_Differentiable_Simulation.pdf]]
