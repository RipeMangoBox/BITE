---
title: "HWC-Loco: A Hierarchical Whole-Body Control Approach to Robust Humanoid Locomotion"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/HWC_Loco_A_Hierarchical_Whole_Body_Control_Approach_to_Robust_Humanoid_Locomotion.pdf
openreview_forum_id: 3UE3Aatcjy
aliases:
- HL
- HWC-Loco
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "通过分层策略动态切换目标跟踪与安全恢复：高层规划器基于ZMP等稳定性指标决定何时激活恢复策略，而目标跟踪策略模仿人类运动以保证自然性。"
primary_logic: "将人形运动控制形式化为一个鲁棒约束优化问题，最小化最坏情况下的任务性能下降，同时通过Wasserstein距离约束使运动符合人类规范，并通过ZMP约束保证动力学可行性，从而在不牺牲任务效率的前提下实现安全恢复。"
claims:
- "HWC-Loco在高速楼梯地形上达到84.34%的成功率，显著优于DreamWaQ-Humanoid的60.58%，提升超过23个百分点。"
- "在恒定外部力/力矩扰动下，HWC-Loco成功率为75.95%，ZMP偏差仅为6.61，均优于所有基线。"
- "消融实验表明，移除ZMP约束或极端情况不确定性集会大幅降低高冲击扰动下的鲁棒性。"
- "学习的高层规划器相比固定阈值ZMP启发式方法，在成功率和策略切换次数之间取得更好平衡。"
---

# HWC-Loco: A Hierarchical Whole-Body Control Approach to Robust Humanoid Locomotion

> [!tip] 核心洞察
> 将人形运动控制形式化为一个鲁棒约束优化问题，最小化最坏情况下的任务性能下降，同时通过Wasserstein距离约束使运动符合人类规范，并通过ZMP约束保证动力学可行性，从而在不牺牲任务效率的前提下实现安全恢复。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | HWC-Loco：一种面向鲁棒人形运动的分层全身控制方法 |
| 英文题名 | HWC-Loco: A Hierarchical Whole-Body Control Approach to Robust Humanoid Locomotion |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=3UE3Aatcjy) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | HWC-Loco |
| Dataset | Stairs High Speed, Constant External Force/Torque, High-Impulse Perturbation |

> [!tip] 效果简介
> - Stairs High Speed 上，Success Rate 为 84.34 ± 0.43，对比 DreamWaQ-Humanoid: 60.58，变化 +23.76。
> - Constant External Force/Torque 上，Success Rate 为 75.95 ± 0.66，对比 Large-DR-Hist (4.0): 70.53 ± 0.42，变化 +5.42。
> - High-Impulse Perturbation 上，Success Rate 为 81.27 ± 0.80，对比 Large-DR-Hist (4.0): 71.36 ± 0.89，变化 +9.91。

## 概述

人形机器人在复杂地形上的鲁棒运动控制面临一个核心瓶颈：现有基于学习的策略在部署时遭遇训练分布之外的动力学不匹配——如外部冲击、传感器噪声或恶意指令——缺乏从安全关键状态中恢复的机制，导致成功率急剧下降。HWC-Loco 将这一问题形式化为一个**鲁棒约束优化问题**：在最坏情况动力学下最大化任务奖励，同时通过 Wasserstein 距离约束使运动符合人类规范，并通过零力矩点（ZMP）约束保证动力学可行性。

方法的核心洞察是**通过分层策略动态切换目标跟踪与安全恢复**。高层规划器基于历史观测和机器人状态（包括通过 VAE 估计器推断的 ZMP 特征）决定何时激活恢复策略；目标跟踪策略模仿人类运动以保证自然性，安全恢复策略则在极端不确定性集下强制满足 ZMP 约束以维持稳定。

实验表明，HWC-Loco 在高速楼梯地形上达到 **84.34%** 的成功率，较 DreamWaQ-Humanoid 的 60.58% 提升超过 23 个百分点（Table 1）；在恒定外力/力矩扰动下成功率为 75.95%，ZMP 偏差仅 6.61，均优于所有基线（Table 2）。消融实验证实，移除 ZMP 约束或极端情况不确定性集会显著降低高冲击扰动下的鲁棒性（Table 26），而学习的高层规划器相比固定阈值 ZMP 启发式方法在成功率和策略切换次数之间取得了更优平衡（Tables 22–25）。

在方法谱系中，HWC-Loco 相对于 DreamWaQ-Humanoid（Nahrendra et al., 2023）和 AHL（Cui et al., 2024）等域随机化基线，引入了三个关键变化：控制架构从单一策略升级为分层策略；安全约束从间接惩罚转为显式的鲁棒约束 RL 框架；模仿学习目标从 KL 散度替换为 Wasserstein-1 距离。这些设计使得 HWC-Loco 在不牺牲任务效率的前提下实现了安全恢复能力。

## 背景与动机

人形机器人在复杂地形上的鲁棒运动控制是机器人学中的核心挑战。近年来，基于强化学习（RL）的方法在仿真环境中取得了显著进展，但将这些策略部署到真实世界时，一个根本性瓶颈暴露出来：**现有学习策略缺乏从安全关键状态中恢复的机制**。当机器人遭遇超出训练分布的动力学不匹配——如外部冲击、传感器噪声或恶意指令——策略往往无法及时调整行为以维持平衡，导致灾难性失败。

这一问题的根源在于，传统RL方法将策略优化视为在固定环境动力学下的期望奖励最大化问题。尽管域随机化（Domain Randomization）在一定程度上扩展了策略的泛化能力，但它本质上是一种**被动适应**：策略在训练时被暴露于多种环境变体，但并未显式地学习如何主动应对最坏情况的动力学扰动。以 **DreamWaQ-Humanoid**（Nahrendra et al., 2023）和 **AHL**（Cui et al., 2024）为代表的方法虽然通过历史信息推断特权状态来提升盲态运动能力，却移除了人类模仿目标，且在安全约束方面仅依赖奖励惩罚或正则化等间接手段，缺乏对动力学可行性的显式保证。

此外，现有方法在**任务效率与安全性之间的权衡**上存在结构性缺陷。单一策略需要同时满足目标跟踪和稳定维持两个可能冲突的目标：当机器人接近跌倒时，任务指令（如保持前进速度）可能与恢复动作（如后退或侧向迈步）直接矛盾。这种冲突在固定策略架构下难以有效解决，因为策略必须在同一组参数中编码两种行为模式，导致在极端场景下两种目标都无法充分达成。

HWC-Loco 的核心洞察在于将人形运动控制形式化为一个**鲁棒约束优化问题**：在最坏情况的动力学扰动下最小化任务性能下降，同时通过 Wasserstein 距离约束使运动符合人类运动规范，并通过 ZMP 约束保证动力学可行性。这一形式化使得策略能够在不牺牲任务效率的前提下实现安全恢复——从根本上改变了安全约束从“事后惩罚”到“先验保证”的范式。

## 核心创新

HWC-Loco 的核心创新在于将人形机器人的全身运动控制重新形式化为一个**分层鲁棒约束优化问题**，从而在不牺牲任务效率的前提下，赋予策略从安全关键状态中自主恢复的能力。这一设计直接回应了现有方法的瓶颈：基于学习的人形运动策略在面对部署中的动力学不匹配时，缺乏结构化的安全恢复机制，导致鲁棒性不足。

具体而言，HWC-Loco 相对于基线方法在以下四个关键维度上实现了结构性改变：

### 1. 控制架构：从单一策略到分层动态切换

基线方法（如 **DreamWaQ-Humanoid**，Nahrendra et al., 2023；**AHL**，Cui et al., 2024）采用单一策略直接输出关节目标，缺乏对安全状态的显式感知与响应。HWC-Loco 引入了**三层分层策略**：
- **高层规划策略（π₀）**：基于历史观察和机器人状态，动态决定激活目标跟踪策略还是安全恢复策略。
- **目标跟踪策略（π₁）**：负责在正常条件下高效、自然地执行速度指令。
- **安全恢复策略（π₂）**：专门处理紧急事件，将机器人从失去平衡等安全关键状态中恢复。

这种架构的核心优势在于**策略切换的决策是学习得到的**，而非依赖固定阈值的启发式规则。消融实验（Tables 22-25）表明，固定阈值 ZMP 切换规则会导致开关次数过高且追踪性能下降，而学习的高层规划器在成功率和切换频率之间取得了更优的平衡。

### 2. 安全约束形式：从隐式惩罚到显式鲁棒约束

基线方法通常通过奖励函数中的惩罚项或正则化来间接处理安全性，无法提供最坏情况下的安全保证。HWC-Loco 将安全约束显式化，构建了一个**鲁棒约束 RL 框架**：

- 将运动控制目标形式化为一个 **max-min 优化问题**，在动力学不确定集上最小化最坏情况下的任务性能下降。
- 引入 **ZMP 可行性约束**（ϕ(τ) ≤ ε_ϕ），实时评估零力矩点与支撑多边形中心的距离，作为动态稳定性的显式指标。
- 构建**极端情况不确定性集**，包含多尺度外力/力矩扰动、高强度传感器噪声、恶意速度指令和域随机化，专门用于训练安全恢复策略应对现实世界中可能出现的动力学不匹配。

消融实验（Table 26）证实，移除 ZMP 约束或极端情况不确定性集会显著降低高冲量扰动下的鲁棒性，验证了显式约束的必要性。

### 3. 模仿学习目标：从 KL 散度到 Wasserstein-1 距离

HWC-Loco 采用 **Wasserstein-1 距离**来约束学习策略与人类专家运动分布之间的差异，而非基线方法中常用的 KL 散度或简单的奖励正则化。这一选择的关键在于：Wasserstein 距离具有良好的几何性质，能够更有效地衡量分布间的结构差异，从而引导策略产生更自然的类人运动。具体实现上，通过 Kantorovich-Rubinstein 对偶将 Wasserstein-1 距离转化为一个判别器的优化问题，判别器以梯度惩罚方式训练以保证 Lipschitz 连续性。

### 4. 环境不确定性处理：从域随机化到对抗性不确定集

基线方法仅依赖域随机化来应对环境变化。HWC-Loco 在此基础上进一步构建了**对抗性的极端情况不确定性集**，模拟外部扰动、硬件故障和恶意指令等部署中可能出现的对抗性条件。这一设计使得安全恢复策略能够在训练中主动面对最坏情况动力学，从而在真实部署中具备更强的鲁棒性。实验（Table 2）表明，在恒定外力/力矩扰动下，HWC-Loco 的成功率达到 75.95%，ZMP 偏差仅为 6.61，均显著优于所有基线。

**创新总结**：HWC-Loco 的核心贡献不在于引入全新的算法组件，而在于通过**分层策略架构 + 鲁棒约束优化 + Wasserstein 模仿学习 + 极端不确定性集**的系统性组合，将人形运动控制从“追求平均性能”提升为“在最坏情况下仍可保证安全”，同时不牺牲自然性和任务效率。这一设计思路为人形机器人的鲁棒部署提供了一条可推广的路径。

## 整体框架

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_3UE3Aatcjy/figures/002_Figure_2.jpg]]
*Figure 2: Overview of HWC-Loco: The framework consists of two stages: (a) Training goal-tracking policy to effectively enable human-like locomotion across diverse terrains (Section 4.1) and safety recovery policy to recover from safety-critical states (i.e., extreme-case) (Section 4.2). (b) Training the high-level planning policy to select between the two pre-trained low-level policies (Section 4.3), thereby ensuring stable and consistent locomotion*

HWC-Loco 将人形机器人的全身运动控制形式化为一个**分层策略架构**，其核心设计动机在于解决单一策略在现实部署中面临的动力学不匹配问题：当机器人遭遇训练分布之外的扰动时，缺乏从安全关键状态中恢复的显式机制。

### 问题形式化

整个控制问题被建模为部分可观测马尔可夫决策过程（POMDP），并在目标层面被提升为**鲁棒约束优化问题**。具体而言，策略需要在最坏情况动力学下最大化任务奖励，同时满足两个约束：通过 Wasserstein 距离约束使运动分布符合人类规范，以及通过 ZMP 可行性约束保证动力学稳定性。这一形式化将“任务效率”与“安全恢复”之间的权衡显式纳入优化目标，而非依赖隐式的奖励惩罚。

### 分层策略架构

HWC-Loco 采用三层策略结构，将上述鲁棒约束优化目标分解为两个阶段训练的低层策略和一个协调层：

- **目标跟踪策略（π₁）**：在标准训练环境（学习动力学）下最大化任务奖励，同时通过 Wasserstein-1 距离约束模仿人类运动分布。该策略负责高效、自然地执行速度指令跟踪，保证任务性能与类人运动质量。
- **安全恢复策略（π₂）**：在极端情况不确定性集（包含多尺度外力/力矩、高强度传感器噪声、恶意速度指令等）下，求解 max-min 鲁棒优化问题，并显式施加 ZMP 可行性约束。该策略专注于处理安全关键事件，使机器人从失稳状态中恢复。
- **高层规划策略（π₀）**：基于历史观测和当前机器人状态，动态决定激活 π₁ 或 π₂。其奖励函数包含任务跟踪奖励、策略切换惩罚和终止惩罚，通过调整终止惩罚权重 α 来控制安全性与任务完成之间的敏感度。

### 特权信息推断

由于真实部署中无法直接获取身体速度、ZMP 等关键状态，HWC-Loco 采用基于 VAE 的特权信息估计器，从历史观测中推断这些隐式特征。估计器的输出同时作为 π₀ 的输入，使高层规划器能够在部分可观测条件下做出可靠的策略切换决策。

### 训练流程

训练分为两个阶段（Figure 2）：首先独立训练 π₁ 和 π₂，其中 π₂ 在极端情况不确定性集下进行鲁棒优化；随后冻结低层策略，训练 π₀ 学习动态切换逻辑。这种分阶段训练方式避免了联合优化中 π₀ 与低层策略的相互干扰，但也意味着策略过渡的平滑性可能未达到最优——这是该方法的一个已知局限。

### 关键设计决策

| 设计维度 | 基线方法 | HWC-Loco |
|---------|---------|----------|
| 控制架构 | 单一策略直接输出关节目标 | 分层策略，高层规划器动态选择目标跟踪或安全恢复 |
| 安全约束形式 | 通过惩罚奖励或正则化间接处理 | 鲁棒约束 RL + ZMP 可行性约束显式保证最坏情况安全性 |
| 模仿学习目标 | KL 散度或未使用模仿学习 | Wasserstein-1 距离约束策略与人类专家运动分布差异 |
| 环境不确定性处理 | 仅域随机化 | 构建极端情况不确定性集，训练恢复策略应对对抗性动力学 |

这一架构的核心洞察在于：**将安全恢复从任务跟踪中解耦为独立策略，并通过鲁棒优化显式保证其最坏情况性能**，从而在不牺牲任务效率的前提下实现从安全关键状态中的可靠恢复。

## 核心模块与公式推导

### 3.1 问题形式化：鲁棒约束优化

HWC-Loco 将人形机器人的全身运动控制形式化为一个**鲁棒约束马尔可夫决策过程**。核心洞察在于：真实部署中的动力学不匹配（域偏移）会导致依赖单一策略的方法在安全关键状态下失效。为此，论文将策略优化目标构造为在最坏情况动力学下的约束最大化问题。

首先定义动力学不确定性集。令 $P_{\mathcal{T}}^{L}$ 为训练环境中的标称转移函数，$\bar{P}_{\mathcal{T}}$ 为任意可能的真实动力学。不确定性集 $\mathfrak{P}_{\alpha}^{L}$ 包含所有由标称动力学与未知动力学按比例 $\alpha$ 混合而成的转移函数：

$$\mathfrak{P}_{\alpha}^{L} = \{ \alpha P_{\mathcal{T}}^{L} + (1 - \alpha) \bar{P_{\mathcal{T}}}, \forall \bar{P_{\mathcal{T}}} \in \mathfrak{P} \}$$

其中 $\alpha \in [0, 1]$ 控制动力学不匹配的强度——$\alpha$ 越小，真实环境与训练环境的偏差越大。

在此不确定性集上，鲁棒人形运动目标被形式化为：

$$\operatorname*{max}_{\pi} \operatorname*{min}_{\widehat{P_T} \in \mathfrak{P}_{\alpha}^{L}} \mathbb{E}_{\mu_0, P_T^L, \pi} \left[ \sum_{t=0}^{\infty} \gamma^t r_{\mathfrak{T}}(s_t, a_t) \right] \quad s.t. \quad \mathcal{D}_f(\rho_{M^{P_T^L}}^{\pi} \| \rho_{M^{P_T^L}}^{\pi^E}) \leq \epsilon_f \quad \text{and} \quad \mathbb{E}_{\tau \sim (\mu_0, \widehat{P_T}, \pi)} \left[ \phi(\tau) \right] \leq \epsilon_{\phi}$$

该目标包含三个关键组件：
- **最大化最坏情况任务奖励**：内层 $\min$ 确保策略在不确定性集中最不利的动力学下仍能完成任务；
- **模仿学习约束**：通过 $f$-散度 $\mathcal{D}_f$ 约束学习策略与人类专家策略的占用测度分布差异，保证运动的自然性；
- **可行性约束**：通过 $\phi(\tau)$ 约束轨迹的动力学可行性，防止策略进入不可恢复的危险状态。

### 3.2 分层策略架构

直接求解上述鲁棒约束优化问题极为困难。HWC-Loco 的核心设计是将目标分解为两个阶段，由三个策略模块协同工作：

**目标跟踪策略（$\pi_1$）** 在标称训练环境下优化，其目标为：

$$\operatorname*{max}_{\pi_1} \mathbb{E}_{\rho^{\pi_1}} \left[ \sum_{t=0}^{\infty} \gamma^t \left[ r_{\mathfrak{T}}(s_t, a_t) - \lambda f_d(s^d) \right] \right]$$

其中 $r_{\mathfrak{T}}$ 为任务奖励，采用高斯形式的速度跟踪奖励：

$$r_{\mathfrak{T}} = \alpha_{1} \exp\left(-\frac{\|v_{\mathrm{xy}}^{c} - v_{\mathrm{xy}}\|_{2}^{2}}{\sigma_{\mathrm{lin}}^{2}}\right) + \alpha_{2} \exp\left(-\frac{\|w_{\mathrm{z}}^{c} - w_{\mathrm{z}}\|_{2}^{2}}{\sigma_{\mathrm{ang}}^{2}}\right)$$

$f_d$ 为鉴别器，用于实现 Wasserstein-1 距离约束。通过 Kantorovich-Rubinstein 对偶，分布差异被转化为：

$$\mathcal{D}_f(\rho^{\pi^E} \| \rho^{\pi_1}) = \sup_{\|f_d\|_L \leq 1} \mathbb{E}_{\boldsymbol{x} \sim \rho^{\pi^E}} [f_d(\boldsymbol{x})] - \mathbb{E}_{\boldsymbol{x} \sim \rho^{\pi_1}} [f_d(\boldsymbol{x})]$$

鉴别器以梯度惩罚训练，强制满足 1-Lipschitz 连续性，从而精确度量策略运动分布与人类运动分布之间的 Wasserstein-1 距离。

**安全恢复策略（$\pi_2$）** 在极端情况不确定性集下训练，处理安全关键事件：

$$\operatorname*{max}_{\pi_2} \operatorname*{min}_{\widehat{P_T} \in \mathfrak{P}_{\alpha}^{L}} \mathbb{E}_{\mu_0, \widehat{P_T}, \pi_2} \left[ \sum_{t=0}^{\infty} \gamma^t r_{\mathfrak{T}}(s_t, a_t) - \lambda f_d(s_t, a_t) \right] \quad s.t. \quad \mathbb{E}_{\tau \sim (\mu_0, \widehat{P_T}, \pi_2)} \left[ \phi(\tau) \right] \leq \epsilon_{\phi}$$

极端情况不确定性集通过以下方式构建：施加多尺度外部力/力矩、注入高强度传感器噪声、发送恶意速度指令、以及激进的域随机化。可行性约束 $\phi(\tau)$ 通过零力矩点（ZMP）实时评估：

$$\phi(s, a) = \| \mathbf{p}_{\mathrm{ZMP}}(s, a) - \mathbf{p}_{\mathrm{ac}} \|_2 \quad \text{where} \quad \mathbf{p}_{\mathrm{ZMP}}(s, a) = \mathbf{p}_{\mathrm{CoM}}(s, a) - \frac{z_{\mathrm{CoM}}(s, a)}{g} \cdot \ddot{\mathbf{p}}_{\mathrm{CoM}}(s, a)$$

其中 $\mathbf{p}_{\mathrm{ZMP}}$ 为零力矩点位置，$\mathbf{p}_{\mathrm{ac}}$ 为支撑多边形中心。该指标实时反映 ZMP 偏离支撑区域的程度——偏离越大，机器人倾倒风险越高。通过约束 $\phi$，安全恢复策略被显式要求将 ZMP 维持在支撑多边形内，从而保证动力学可行性。

**高层规划策略（$\pi_0$）** 在 $\pi_1$ 和 $\pi_2$ 预训练完成后进行训练，基于历史观察和当前状态动态选择激活的低层策略。其目标为最大化任务奖励，同时惩罚频繁的策略切换和任务终止：

$$\operatorname*{max}_{\pi_0} \mathbb{E}\left[ \sum_{t=0}^{\infty} \gamma^t \left[ r_{\mathfrak{T}}(s_t, \bar{a}_t) - \mathbb{1}(\bar{a}_{t-1} \neq \bar{a}_t) - \alpha \mathbb{1}(s_t) \right] \right]$$

其中 $\bar{a}_t \in \{0, 1\}$ 为离散动作（0 激活 $\pi_1$，1 激活 $\pi_2$），$\mathbb{1}(\bar{a}_{t-1} \neq \bar{a}_t)$ 为切换惩罚，$\mathbb{1}(s_t)$ 为终止指示函数。超参数 $\alpha$ 控制安全性与任务完成之间的权衡：$\alpha$ 越大，高层策略对失败事件越敏感，越倾向于激活恢复策略。

### 3.3 特权信息估计器

由于真实部署中无法直接获取身体速度和 ZMP 等特权信息，HWC-Loco 采用基于 VAE 的估计器从历史观测中推断这些隐变量。该模块继承自 DreamWaQ（Nahrendra et al., 2023）的设计，为高层规划策略提供决策所需的稳定性指标。

## 实验与分析

### 核心结果：运动性能与鲁棒性

HWC-Loco在仿真环境中的运动成功率和鲁棒性均显著优于现有基线。在高速楼梯地形上，HWC-Loco达到**84.34%**的成功率，相比**DreamWaQ-Humanoid**（Nahrendra et al., 2023）的60.58%提升超过23个百分点（Table 1）。在低速斜坡和楼梯场景中，HWC-Loco几乎达到100%的成功率，而基线方法在高速条件下性能急剧下降。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_3UE3Aatcjy/figures/004_Table_1.jpg]]
*Table 1: Locomotion performance in simulated environments. Each evaluation runs for 1200 steps, which is equivalent to 12 seconds of real clock time. ± corresponds to the standard deviation of the performance on 3 random seeds. The best result of each setting is marked as bold*

在扰动鲁棒性测试中（Table 2），HWC-Loco在恒定外部力/力矩扰动下成功率为**75.95%**，ZMP偏差仅为**6.61**，均优于所有基线。在高冲量扰动下，成功率优势更为明显（81.27% vs. Large-DR-Hist (4.0)的71.36%，提升约10个百分点）。这验证了分层策略中安全恢复机制的有效性：当机器人遭遇突发冲击时，恢复行为（如快速降低重心、挥动手臂）能够缓解冲击并加速恢复稳定。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_3UE3Aatcjy/figures/005_Table_2.jpg]]
*Table 2: Robustness of locomotion under different disturbances*

在类人运动质量方面，HWC-Loco在G1平台上Wasserstein距离降至**3.11**，优于CRL的3.56（Table 27），表明Wasserstein-1距离约束有效缩小了策略运动分布与人类专家分布之间的差异。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_3UE3Aatcjy/figures/043_Table_27.jpg]]
*Table 27: Performance comparison with non-robust constrained methods*

### 消融实验：关键设计的作用

**分层切换策略的必要性。** 移除安全恢复机制后（Goal-Tracking Policy），高速楼梯成功率从84.34%降至72.60%（Table 1），在高冲量扰动下成功率进一步下降。降低高层规划器对失败事件的敏感度（HWC-Loco-l）同样导致鲁棒性下降，表明动态策略切换是处理安全关键状态的核心机制。

**ZMP约束与极端情况不确定性集。** Table 26的消融表明，仅使用ZMP约束而省略极端情况不确定性集，会大幅降低高冲量扰动下的鲁棒性；反之亦然。两者共同作用才能保证最坏情况动力学下的可行性。极端情况不确定性集通过施加多尺度外力、传感器噪声和恶意速度指令来模拟部署中可能出现的对抗性动力学。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_3UE3Aatcjy/figures/042_Table_26.jpg]]
*Table 26: Robust-optimization ablation on success rate (%). “w/o” denotes training without the extreme-case uncertainty set*

**学习规划器 vs. 固定阈值启发式。** Tables 22-25对比了学习的高层规划器与基于固定ZMP阈值的切换规则。固定阈值方法导致策略切换次数过高且追踪性能下降，而学习规划器在成功率和切换频率之间取得更优平衡。这得益于规划器从历史观察中学习到更平滑的切换策略。

**观测历史长度的影响。** Table 28显示，过长的观测历史（$H=40$）虽略微提升成功率，但损害目标追踪精度和类人程度。这表明规划器需要足够的历史信息来检测安全关键状态，但过长的记忆窗口会引入冗余信息，干扰任务执行。

### 真实世界部署与局限性

HWC-Loco在真实机器人上展示了跨多种地形的泛化能力，包括平地、草地、上坡和下坡（Figure 11），以及15 cm台阶和20°斜坡的攀爬（Figure 10）。在外部扰动下，策略切换机制有效触发恢复行为（Figure 12），机器人通过挥臂和步态调整维持平衡（Figure 13）。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_3UE3Aatcjy/figures/045_Figure_10.jpg]]
*Figure 10: Climb Stairs Test. The blue segments indicate the activation of the goal-tracking policy, while the orange segments correspond to the safety recovery policy*

然而，真实部署中仍存在超出训练分布的故障模式：极低摩擦地面、超出训练范围的速度指令以及传感器通信延迟均可能导致策略失效。恢复策略在仿真中训练，可能无法完全覆盖真实世界中扰动的多样性。此外，当前真实机器人仅有19自由度，限制了复杂恢复行为的实现。VAE估计器在极高噪声下性能下降（Table 21），可能影响策略切换的可靠性，这一点需在实际部署中进一步验证。

## 方法谱系与知识库定位

### 1. 与基线方法的关系

HWC-Loco 的核心贡献在于将人形运动控制从“单一策略 + 域随机化”范式推进到“分层鲁棒约束优化”范式。其与主要基线的关系可沿四个关键维度展开：

**控制架构的跃迁。** 传统方法如 **DreamWaQ-Humanoid**（Nahrendra et al., 2023）和 **AHL**（Cui et al., 2024）采用单一策略直接输出关节目标，依赖域随机化来应对动力学扰动。HWC-Loco 引入分层策略：高层规划器（π₀）基于历史观察和机器人状态动态选择目标跟踪策略（π₁）或安全恢复策略（π₂），低层分别优化任务奖励与安全约束。这一架构跃迁使系统能够在“高效任务执行”与“安全关键恢复”之间动态权衡，而非将两者混入单一奖励函数。

**安全约束的形式化。** 基线方法通过惩罚奖励项或正则化间接处理安全性，缺乏对最坏情况动力学的显式保证。HWC-Loco 将问题形式化为鲁棒约束 RL 框架（式 1），通过 ZMP 可行性约束 $\mathbb{E}[\phi(\tau)] \leq \epsilon_\phi$ 显式保证动力学可行性。这一差异在消融实验中表现显著：移除 ZMP 约束或极端情况不确定性集后，高冲击扰动下的成功率大幅下降（Table 26），验证了显式约束对鲁棒性的因果贡献。

**模仿学习目标的升级。** DreamWaQ-Humanoid 移除了人类模仿目标，AHL 则可能使用 KL 散度。HWC-Loco 采用 Wasserstein-1 距离作为分布散度度量，通过 Kantorovich-Rubinstein 对偶实现（式 5），在 Lipschitz 约束下训练判别器 $f_d$。Table 27 显示，HWC-Loco 的 Wasserstein 距离（3.11 ± 0.03）显著低于使用 KL 散度的 CRL 方法（3.56 ± 0.14），表明 Wasserstein 距离在捕获人类运动分布方面更具优势。

**不确定性处理的深化。** 基线方法仅采用域随机化（Table 12 中的参数范围）。HWC-Loco 在此之上构建了极端情况不确定性集 $\mathfrak{P}_{\alpha}^{L}$，包含多尺度外部力/力矩、高强度传感器噪声、恶意速度指令等（Table 11）。这一设计使安全恢复策略 $\pi_2$ 专门针对对抗性动力学进行训练，从而在恒定扰动（75.95% vs DreamWaQ-Humanoid 的约 60%）和高冲量扰动（81.27% vs 71.36%）下取得显著优势（Table 2 / Table 19）。

### 2. 适用边界

HWC-Loco 的设计假设和实验验证界定了其适用范围：

- **硬件条件**：当前验证基于 Unitree H1 和 G1 平台（19 自由度，Table 29），依赖平坦脚底与地面的面接触。方法的核心约束——ZMP 可行性指标 $\phi(s, a) = \|\mathbf{p}_{\mathrm{ZMP}} - \mathbf{p}_{\mathrm{ac}}\|_2$——假设存在明确的支撑多边形，因此不直接适用于多接触或非平面接触场景（如攀岩、抓握地形）。
- **扰动类型**：极端情况不确定性集覆盖了外部力/力矩、传感器噪声和恶意指令，但未包含硬件故障（如关节锁死、电机过热）或极低摩擦地面（如冰面）。真实部署中已观察到超出训练分布的操作条件导致故障。
- **速度指令范围**：训练和评估在特定速度范围内进行，超出该范围的指令可能导致策略退化。
- **通信延迟**：VAE 估计器在极高噪声下性能下降（Table 21），可能影响高层规划器的切换可靠性。传感器通信延迟在真实部署中被列为已知故障模式。

### 3. 局限性与已知故障模式

**训练-部署差距。** 安全恢复策略完全在仿真中训练，真实世界的扰动多样性（特别是未建模的硬件故障和极端地面条件）可能超出极端情况不确定性集的覆盖范围。论文明确指出“极低摩擦地面、超出训练范围的速度指令、传感器通信延迟”是已知的故障触发条件。

**自由度限制。** 当前真实机器人仅有 19 自由度，限制了全身协调和复杂恢复行为（如大幅度躯干扭转、不对称手臂支撑）的实现。更丰富的运动学表达可能进一步提升恢复能力。

**分阶段训练的次优性。** 高层规划器和低层策略是分阶段训练的：先固定 $\pi_1$ 和 $\pi_2$，再训练 $\pi_0$。这种解耦简化了训练，但可能牺牲联合优化带来的策略过渡平滑性。论文将此列为未来工作方向。

**VAE 估计器的脆弱性。** 虽然 VAE 估计器对中等噪声具有鲁棒性，但在极高噪声下性能下降（Table 21），可能影响高层规划器对特权信息（身体速度、ZMP 特征）的推断精度，进而导致不恰当的策略切换。

**α 参数的敏感性。** 高层策略目标中的终止惩罚权重 α 控制安全性与任务完成之间的权衡。Figure 3 显示 α ∈ {0, 20, 50} 时 π₁ 占主导，α = 200 时训练不稳定。这一敏感性与消融实验 HWC-Loco-l（降低 α 值）的性能下降相呼应，表明该参数需要仔细调优。

### 4. 开放问题

1. **非平面接触扩展**：如何将 ZMP 约束推广到无平坦脚底的多接触场景，而不需要显式建模接触几何？可能的路径包括学习隐式稳定性指标或引入互补约束。
2. **传感器退化下的鲁棒性**：当关键传感器缺失或质量较差时，VAE 估计器对隐式特征推断的鲁棒性如何？多模态融合（如视觉-惯性-关节编码器联合）能否进一步改善？
3. **连续策略插值**：高层规划器当前使用离散动作空间（切换二值），是否可以用连续输出（例如混合系数 $\beta \in [0,1]$）实现更平滑的策略插值，从而减少切换振荡？
4. **人机交互约束集成**：在大规模人机交互任务（如搬运、协作）中，该方法能否自然地引入任务相关的安全约束（如接触力限制、碰撞避免），而不破坏现有的鲁棒性保证？
5. **高层任务规划集成**：本文聚焦于运动控制层面，尚未探讨高层任务规划（如导航、操作序列决策）如何与该分层控制框架集成。规划器输出的子目标如何与 ZMP 约束和恢复策略协调，是一个开放的系统性问题。
6. **联合训练优化**：分阶段训练的次优性提示联合优化的潜力，但如何在保证训练稳定性的前提下同时优化 π₀、π₁、π₂ 仍是一个挑战。

## 原文 PDF

![[paperPDFs/ICLR_2026/HWC_Loco_A_Hierarchical_Whole_Body_Control_Approach_to_Robust_Humanoid_Locomotion.pdf]]
