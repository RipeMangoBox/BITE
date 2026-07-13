---
title: "Learning Smooth Humanoid Locomotion through Lipschitz-Constrained Policies"
type: paper
paper_level: A
venue: IROS
year: 2025
pdf_ref: paperPDFs/IROS_2025/Learning_Smooth_Humanoid_Locomotion_through_Lipschitz_Constrained_Policies.pdf
code_link: null
project_link: https://lipschitz-constrained-policy.github.io/
aliases:
- LCPL
- LSHLTLCP
tags:
- IROS_2025
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "对策略输出关于输入观测施加 Lipschitz 约束，具体实现为在训练损失中加入可微分的梯度惩罚项：E[||∇_s log π(a|s)||^2]，直接限制策略函数的变化率。"
primary_logic: "平滑策略天然具有较小的梯度范数（见图 3），因此可以直接通过约束策略梯度的范数来鼓励平滑行为；这种梯度惩罚是完全可微分的，能无缝集成到现有 RL 框架中，替代难以调优的非可微分平滑技术。"
claims:
- "使用平滑奖励训练的策略，其梯度范数明显小于无平滑奖励的策略。"
- "LCP 训练过程中记录的平滑度指标（Action Jitter, DoF Velocity 等）与显式平滑奖励的策略水平相当。"
- "消融实验中 LCP (λ_gp=0.002) 在 Action Jitter、Task Return 等指标上达到或接近平滑奖励方法的性能。"
- "LCP 训练的策略成功零样本部署到多种真实仿人机器人，实现平滑鲁棒的行走。"
---

# Learning Smooth Humanoid Locomotion through Lipschitz-Constrained Policies

> [!tip] 核心洞察
> 平滑策略天然具有较小的梯度范数（见图 3），因此可以直接通过约束策略梯度的范数来鼓励平滑行为；这种梯度惩罚是完全可微分的，能无缝集成到现有 RL 框架中，替代难以调优的非可微分平滑技术。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 通过 Lipschitz 约束策略学习平滑仿人机器人运动 |
| 英文题名 | Learning Smooth Humanoid Locomotion through Lipschitz-Constrained Policies |
| 会议/期刊 | IROS 2025 |
| Links | [paper](https://arxiv.org/abs/2410.11825) · [Project](https://lipschitz-constrained-policy.github.io) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Lipschitz-Constrained Policies (LCP) |
| Dataset | Fourier GR1 (IsaacGym simulation, 1000 envs, 500 steps), Fourier GR1 (sim-to-sim transfer to MuJoCo), Real-world Fourier GR1 (smooth terrain, 10s per trial) |

> [!tip] 效果简介
> - Fourier GR1 (IsaacGym simulation, 1000 envs, 500 steps) 上，Task Return 为 26.03 ± 1.51，对比 Smoothness Rewards: comparable (see Fig. 5)，变化 similar。
> - Fourier GR1 (IsaacGym simulation, 1000 envs, 500 steps) 上，Action Jitter (rad/s^3) 为 3.21 ± 0.11，对比 Smoothness Rewards: similar smoothness (see Fig. 4)，变化 similar。
> - Fourier GR1 (sim-to-sim transfer to MuJoCo) 上，Task Return 为 24.33 ± 1.25，对比 IsaacGym LCP: 26.03 ± 1.51，变化 -1.7。

## 概要

**核心问题**：基于无模型强化学习的仿人机器人运动控制器，在仿真训练中极易产生高频抖动的 bang-bang 控制行为。这类行为不仅导致策略无法成功迁移至真实机器人，且常用的平滑技术——如平滑奖励（Smoothness Rewards）与低通滤波（Low-pass Filters）——均不可微分、依赖大量手工调参，缺乏通用性。

**核心洞察**：该工作发现，平滑的策略天然具有较小的梯度范数（Fig. 3 证实了这一点）。因此，可以直接通过约束策略输出关于输入观测的梯度范数，来鼓励平滑行为。

**提出方法**：**Lipschitz-Constrained Policies (LCP)**，一种在训练损失中引入可微分梯度惩罚项的方法。具体形式为在最大化期望回报的同时，最小化策略对数概率关于状态的梯度范数平方的期望：

$$\max_{\pi} J(\pi) - \lambda_{\mathrm{gp}} \mathbb{E}_{\mathbf{s}, \mathbf{a} \sim \mathcal{D}} \left[ \|\nabla_{\mathbf{s}} \log \pi(\mathbf{a} | \mathbf{s})\|^2 \right]$$

该方法的核心优势在于：完全可微分，仅需数行代码即可无缝集成到现有 PPO 等强化学习框架中，从而替代难以调优的非可微分平滑技术。

**方法定位**：LCP 属于在策略训练目标中引入平滑正则化项的方法。与需要精心设计奖励项权重的平滑奖励方法，以及作为后处理步骤的低通滤波方法不同，LCP 通过直接惩罚策略函数的局部变化率来强制 Lipschitz 连续性，是一种端到端、可微分的替代方案。

**主要结果**：
- **仿真性能**：在 Fourier GR1 机器人仿真任务中，LCP 在 Action Jitter 等平滑度指标上与显式平滑奖励方法水平相当（Fig. 4），同时任务回报也达到相似水平（TABLE I, Fig. 5）。
- **消融实验**：梯度惩罚系数 $\lambda_{\mathrm{gp}} = 0.002$ 在平滑度与任务回报之间取得最佳平衡（TABLE I(b), Fig. 6）；将梯度惩罚应用于策略的完整观测输入（当前观测 + 历史观测）优于仅应用于当前观测（TABLE I(c)）。
- **真实世界部署**：LCP 训练的策略成功零样本部署至多种真实仿人机器人，在平滑地形上实现平滑鲁棒的行走，Action Jitter 低至 $1.12 \pm 0.16$ rad/s³（TABLE III, Fig. 7）。

**局限性**：目前仅在仿人机器人步行与转向任务上验证，尚未延伸至跑、跳等更高动态技能；梯度惩罚系数 $\lambda_{\mathrm{gp}}$ 仍需手动调节；真实世界测试局限于特定地形与机器人类别。

### 问题背景：从仿真到现实的平滑鸿沟

基于无模型强化学习（RL）的仿人机器人运动控制器，在仿真环境中通常能够学习到高效的运动策略，但这些策略往往表现出高频抖动行为，即所谓的 **bang-bang 控制**。这种不自然的抖动不仅降低了运动的效率和外观质量，更构成了仿真到现实迁移（sim-to-real transfer）的核心障碍——高频动作模式会在真实机器人的执行器、传动机构和传感器链路上产生不可预料的累积误差，导致策略无法成功部署到物理平台上。

### 现有平滑技术的局限性

为了抑制抖动行为，研究者通常采用两类技术：

1. **平滑奖励（Smoothness Rewards）**：在奖励函数中加入惩罚关节速度、加速度或加加速度（jerk）的项，引导策略学习平滑动作。该方法源自 **Fu et al. (CoRL 2021)** 的工作，其本质是通过试错来间接塑造行为，需要人工反复调优多个奖励项的权重系数，且奖励函数本身不可微分，无法通过梯度直接优化平滑性目标。

2. **低通滤波（Low-pass Filters）**：在策略输出端施加动作平滑滤波器，直接滤除高频成分。该方法由 **Ji et al. (IROS 2022)** 等先前工作采用，虽然实现简单，但滤波操作同样不可微分，割裂了端到端的梯度流，且滤波参数的选择高度依赖机器人平台和任务特性，缺乏通用性。

上述两类方法的共同缺陷在于：它们都是**非可微分**的平滑技术，需要大量手工调参，且缺乏对策略函数本身平滑性的直接刻画和约束。

### 核心洞察：平滑策略天然具有小梯度范数

本文的关键动机来源于一个实验观察：**使用平滑奖励训练的策略，其输出动作关于输入观测的梯度范数显著小于无平滑奖励的策略**（见 Fig. 3）。这一现象揭示了平滑行为与策略函数梯度之间的内在联系——平滑的策略天然地对输入变化不敏感，因而具有较小的梯度范数。

从数学角度，这一观察与 Lipschitz 连续性的概念紧密相连。一个函数 $f$ 被称为 Lipschitz 连续的，当且仅当其输出变化率被常数 $K$ 所界：

$$d_{Y}(f(\mathbf{x}_1), f(\mathbf{x}_2)) \leq K d_{X}(\mathbf{x}_1, \mathbf{x}_2)$$

若函数可微，则梯度范数有界 $\|\nabla_{\mathbf{x}} f(\mathbf{x})\| \leq K$ 是 Lipschitz 连续性的充分条件（见 Equation 2）。因此，**直接约束策略梯度的范数，等价于强制策略满足局部 Lipschitz 连续性**，从而鼓励平滑行为。

### 本文动机：可微分的平滑约束

基于上述洞察，本文提出了一种全新的平滑正则化思路：**将 Lipschitz 约束直接嵌入策略优化的训练目标中**。具体而言，在最大化期望回报的同时，加入一个可微分的梯度惩罚项：

$$\max_{\pi} J(\pi) - \lambda_{\mathrm{gp}} \mathbb{E}_{\mathbf{s}, \mathbf{a} \sim \mathcal{D}} \left[ \|\nabla_{\mathbf{s}} \log \pi(\mathbf{a} | \mathbf{s})\|^2 \right]$$

该惩罚项计算策略对数概率关于输入观测的梯度范数的平方，并直接在数据分布上求期望。由于梯度惩罚项是完全可微分的，它可以无缝集成到现有的 RL 框架（如 PPO）中，仅需数行代码即可实现，无需手工设计平滑奖励或引入不可微分的滤波操作。

这种方法的根本优势在于：它将平滑性从间接的奖励塑造或后处理滤波，提升为**策略函数空间上的直接约束**，从而提供了一种简单、通用且可微分的平滑行为生成方案。

## 核心方法与创新机理

### 瓶颈洞察：从“平滑行为”到“平滑策略函数”

基于无模型强化学习的仿人机器人运动控制器，在仿真环境中极易产生高频抖动的 bang-bang 控制行为。这类行为在仿真中或许可行，但一旦迁移到真实机器人，会因执行器饱和、未建模动力学和传感器噪声而彻底失效。社区通常采用两种平滑技术应对：（1）在奖励函数中加入惩罚关节速度、加速度或动作变化率的**平滑奖励项**（Fu et al., CoRL 2021）；（2）对策略输出施加**低通滤波器**（Ji et al., IROS 2022）。然而，这两种方法都存在根本性缺陷：平滑奖励需要大量手工调参，且奖励权重与任务目标之间的平衡极为脆弱；低通滤波则完全不可微分，割裂了策略训练与执行之间的梯度链，无法被端到端优化。

本文的核心洞察在于重新定义了“平滑”的归因对象。作者通过一个关键的动机实验（Fig. 3）发现：**使用平滑奖励训练的策略，其策略函数梯度范数天然小于无平滑策略**。这意味着，平滑的行为输出并非仅仅源于奖励塑形，而是从根本上反映了策略函数本身具有更小的局部变化率。这一发现将“产生平滑动作”的问题转化为“约束策略函数的 Lipschitz 常数”的问题，从而打开了一条全新的技术路径。

### 核心方法：可微分的梯度惩罚替代非可微分平滑技术

基于上述洞察，本文提出 **Lipschitz-Constrained Policies (LCP)**，核心创新在于用一个**可微分的梯度惩罚项**替代传统的平滑奖励或低通滤波。具体而言，LCP 在策略优化目标中直接加入对策略对数概率关于输入观测的梯度范数惩罚：

$$
\operatorname*{max}_{\pi} J(\pi) - \lambda_{\mathrm{gp}} \mathbb{E}_{\mathbf{s},\mathbf{a}\sim\mathcal{D}} \left[ \| \nabla_{\mathbf{s}} \log \pi(\mathbf{a}|\mathbf{s}) \|^2 \right]
$$

其中 $\lambda_{\mathrm{gp}}$ 为梯度惩罚系数，$\mathcal{D}$ 为经验回放数据分布。这一惩罚项强制策略函数满足局部 Lipschitz 连续性——当输入观测发生微小变化时，输出动作不会剧烈跳变，从而从根源上抑制高频抖动行为。

### Changed Slot：平滑正则化的范式转变

| 维度 | 基线方法 | LCP 方法 |
|------|---------|---------|
| **正则化对象** | 行为层面的惩罚（关节速度、加速度、动作变化率）或后处理滤波 | 策略函数层面的梯度约束 |
| **可微分性** | 不可微分（低通滤波）或间接可微（平滑奖励通过环境交互） | 完全可微分，直接参与策略梯度反向传播 |
| **调参复杂度** | 多个奖励权重需要手动平衡，与任务目标耦合 | 单一超参数 $\lambda_{\mathrm{gp}}$，与任务奖励解耦 |
| **通用性** | 需针对不同机器人形态重新设计奖励项 | 即插即用，仅需几行代码即可嵌入现有 RL 框架 |

这一 changed slot 的本质是将平滑性从“奖励塑形问题”重新定义为“函数正则化问题”。LCP 的梯度惩罚项通过 PyTorch 的自动微分即可实现，无需修改环境、奖励函数或网络架构，真正做到了与现有 RL 框架的无缝集成。

### 关键设计选择

消融实验揭示了两个关键设计决策：

1. **梯度惩罚的作用域**：将梯度惩罚应用于策略的**整个输入观测**（包括当前观测和历史观测），比仅应用于当前观测能获得更好的平滑效果和任务性能（TABLE I(c)）。这表明历史信息中的时序一致性对平滑行为同样至关重要。

2. **惩罚系数的平衡点**：$\lambda_{\mathrm{gp}} = 0.002$ 在平滑度和任务回报之间取得了最佳平衡。过大的 $\lambda_{\mathrm{gp}}$ 会过度约束策略的表达能力，导致任务性能显著下降（Fig. 6）；过小则无法有效抑制抖动。这一参数在不同机器人形态（Fourier GR1、Unitree H1、Berkeley Humanoid）上表现出良好的鲁棒性，但仍需手动调节。

### 创新边界与局限

尽管 LCP 在平滑仿人机器人行走任务上展现了简洁而有效的替代方案，其创新仍存在明确的边界：

- **任务范围局限**：当前验证仅限于步行和转向任务，尚未延伸到跑、跳等高动态技能。高动态运动可能需要更大的策略变化率，梯度惩罚是否仍适用有待验证。
- **参数敏感性**：$\lambda_{\mathrm{gp}}$ 仍需手动调节，不同机器人形态或任务可能需要重新搜索最优值，尚未实现自动化调参。
- **动作空间假设**：当前策略输出目标关节位置，通过 PD 控制器转化为力矩。若直接输出力矩，梯度惩罚的效果有待进一步验证。

### 问题背景与设计动机

在基于无模型强化学习的仿人机器人运动控制中，仿真环境训练的策略极易产生高频抖动的 bang-bang 控制行为，导致策略无法成功迁移至真实机器人。常用的平滑技术——如基于关节速度、加速度惩罚的**平滑奖励**（Smoothness Rewards，Fu et al., CoRL 2021）和**动作低通滤波**（Low-pass Filters，Ji et al., IROS 2022）——虽然能缓解抖动，但存在根本性缺陷：平滑奖励需要大量手工调参，且奖励项之间可能相互冲突；低通滤波不可微分，无法与策略参数联合优化，且会引入相位延迟，影响动态响应能力。

本文的核心洞察来自一个关键观察：**平滑的策略天然具有较小的梯度范数**（Fig. 3）。基于这一发现，LCP 提出直接约束策略函数的变化率，而非间接惩罚行为后果，从根本上消除高频抖动。

### 核心方法：Lipschitz 约束策略

LCP 的核心思想是将策略输出关于输入观测的 **Lipschitz 连续性**作为可微分约束引入训练过程。Lipschitz 连续性定义如下：

$$d_{Y}(f(\mathbf{x}_1), f(\mathbf{x}_2)) \leq K d_{X}(\mathbf{x}_1, \mathbf{x}_2)$$

其直观含义是：函数输出的变化被输入变化的常数 $K$ 倍所上界约束（Fig. 2）。对于可微函数，梯度范数有界即可保证 Lipschitz 连续性：

$$\|\nabla_{\mathbf{x}} f(\mathbf{x})\| \leq K$$

LCP 将这一数学性质转化为训练目标中的**梯度惩罚项**（Gradient Penalty）。完整的策略优化目标为：

$$\max_{\pi} J(\pi) - \lambda_{\mathrm{gp}} \mathbb{E}_{\mathbf{s}, \mathbf{a} \sim \mathcal{D}} \left[ \|\nabla_{\mathbf{s}} \log \pi(\mathbf{a} | \mathbf{s})\|^2 \right]$$

其中 $J(\pi)$ 为标准的强化学习目标（期望回报），第二项为梯度惩罚：在数据分布上对策略对数概率关于状态 $\mathbf{s}$ 的梯度的 $\ell^2$ 范数平方求期望。通过惩罚策略梯度的范数，LCP 强制策略在局部满足 Lipschitz 连续性，从而抑制输出动作对输入观测的敏感度，消除高频抖动。

### 整体 Pipeline 架构

LCP 的训练框架建立在 **Regularized Online Adaptation (ROA)** 范式之上，整体 pipeline 包含以下核心模块：

**1. 策略网络 $\pi$**
策略网络接收观测输入，输出目标关节位置。在仿真训练中，策略通过 PPO 算法优化，同时受到梯度惩罚项的约束。

**2. 环境编码器 $\mu$**
编码器 $\mu$ 将仿真环境中的特权信息 $\mathbf{e}$（如地面摩擦系数、机器人质量等无法在真实世界直接观测的参数）嵌入为潜在向量 $\mathbf{z}^{\mu}$，为策略提供环境的隐式表征。

**3. 在线适配模块 $\phi$**
适配模块 $\phi$ 仅基于可观测的传感器历史（关节位置、速度、IMU 读数等）估计潜在向量 $\mathbf{z}^{\phi}$，使策略在真实世界部署时无需特权信息即可自适应环境变化。

**4. 域随机化（Domain Randomization）**
仿真训练期间对环境物理参数（质量、摩擦、电机力矩等）进行大范围随机化，迫使策略学习鲁棒的控制行为，缩小 sim-to-real 差距。

**5. 梯度惩罚正则化**
梯度惩罚项 $L_{\mathrm{gp}}(\pi)$ 作为可微分正则化器，直接作用于策略梯度：

$$L_{\mathrm{gp}}(\pi) = \mathbb{E}_{\mathbf{s}, \mathbf{a} \sim \mathcal{D}} \left[ \|\nabla_{\mathbf{s}} \log \pi(\mathbf{a} | \mathbf{s})\|^2 \right]$$

完整的 ROA 训练损失函数为：

$$L(\theta_{\pi}, \theta_{\mu}, \theta_{\phi}) = -L^{PPO}(\theta_{\pi}, \theta_{\mu}) + \lambda \|\mathbf{z}^{\mu} - \mathrm{sg}[\mathbf{z}^{\phi}]\| + \|\mathrm{sg}[\mathbf{z}^{\mu}] - \mathbf{z}^{\phi}\| + \lambda_{\mathrm{gp}} L_{\mathrm{gp}}(\pi)$$

该损失由四部分组成：PPO 策略损失、编码器与适配模块的双向嵌入对齐损失、以及梯度惩罚项。$\mathrm{sg}[\cdot]$ 表示停止梯度操作，确保编码器和适配模块各自独立优化。

### 输入输出流与训练-部署流程

**训练阶段**（IsaacGym 仿真环境，1000 并行环境）：

1. 环境提供观测 $\mathbf{o}_t$（关节状态、IMU 数据、速度指令等）和特权信息 $\mathbf{e}_t$。
2. 编码器 $\mu$ 将 $\mathbf{e}_t$ 嵌入为 $\mathbf{z}^{\mu}$，适配模块 $\phi$ 从观测历史估计 $\mathbf{z}^{\phi}$。
3. 策略 $\pi$ 接收拼接后的输入 $\mathbf{s}_t = [\mathbf{o}_t, \mathbf{z}^{\phi}]$，输出目标关节位置 $\mathbf{a}_t$。
4. PD 控制器将目标位置转化为关节力矩，驱动机器人执行动作。
5. PPO 算法根据收集的轨迹数据更新策略参数，同时计算梯度惩罚项 $L_{\mathrm{gp}}$ 并反向传播。

**部署阶段**（真实机器人零样本迁移）：

1. 丢弃编码器 $\mu$，仅保留策略 $\pi$ 和适配模块 $\phi$。
2. 适配模块 $\phi$ 从真实传感器历史在线估计 $\mathbf{z}^{\phi}$。
3. 策略 $\pi$ 基于当前观测和估计的潜在向量输出平滑的动作指令。
4. 整个推理过程无需任何微调或额外滤波处理。

消融实验表明，梯度惩罚应用于策略的**完整输入观测**（当前观测 + 历史观测拼接）比仅应用于当前观测能获得更好的平滑效果和任务性能（TABLE I(c)）。梯度惩罚系数 $\lambda_{\mathrm{gp}} = 0.002$ 在平滑度和任务回报之间取得最佳平衡；过大的 $\lambda_{\mathrm{gp}}$ 会过度限制策略的表达能力，显著损害学习效果（TABLE I(b), Fig. 6）。

### 方法定位

LCP 的核心贡献在于**将平滑性约束从奖励函数层面提升到策略函数空间**，通过可微分的梯度惩罚实现端到端优化。相较于平滑奖励和低通滤波，LCP 具有三个关键优势：

- **完全可微分**：梯度惩罚直接作用于策略参数，可通过标准反向传播优化，无需手工设计奖励项或引入不可微操作。
- **实现简洁**：仅需数行代码即可集成到现有 RL 框架中，替代复杂的平滑奖励调参流程。
- **通用性强**：不依赖特定的机器人形态或任务结构，理论上适用于任何连续控制策略的平滑训练。

该方法在 Fourier GR1、Unitree H1、Berkeley Humanoid 等多种仿人机器人平台上验证了有效性，策略可直接零样本部署至真实机器人，实现平滑鲁棒的行走（Fig. 1, Fig. 7, TABLE III）。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2410_11825/figures/001_Figure_1.jpg]]
*Figure 1: Lipschitz-constrained policies (LCP) provide a simple and general method for training policies to produce smooth behaviors, which can be directly deployed on a wide range of real-world humanoid robots. Our policies exhibit robust behaviors that can recover from external forces and walk across irregular terrain. For full videos, please visit the project website*

### 核心洞察：平滑策略的梯度特性

本方法的核心洞察源自一个简单的经验观察：**平滑策略天然具有较小的梯度范数**。如 Fig. 3 所示，使用显式平滑奖励（惩罚关节速度、加速度等）训练的策略，其策略函数关于输入观测的梯度范数显著小于无平滑奖励的策略。这一现象揭示了平滑行为与策略函数梯度之间的内在联系——策略输出关于输入的变化率越小，产生的动作序列越平滑。基于此，LCP 将“鼓励平滑”问题转化为“约束策略梯度范数”问题，从而绕开了传统平滑技术不可微分的根本缺陷。

### Lipschitz 连续性的数学基础

LCP 的理论锚点是 Lipschitz 连续性。一个函数 $f$ 若满足：

$$d_Y(f(\mathbf{x}_1), f(\mathbf{x}_2)) \leq K \cdot d_X(\mathbf{x}_1, \mathbf{x}_2)$$

则称 $f$ 是 $K$-Lipschitz 连续的（Equation 1）。其直观含义如 Fig. 2 所示：函数输出之间的距离被输入距离的常数 $K$ 倍严格上界约束，即函数的变化率受到限制。对于可微函数，梯度范数有界是 Lipschitz 连续性的充分条件：

$$\|\nabla_{\mathbf{x}} f(\mathbf{x})\| \leq K$$

（Equation 2）。LCP 正是利用这一性质，通过约束策略梯度的范数来强制策略满足局部 Lipschitz 连续性，从而产生平滑的动作输出。

### 梯度惩罚正则化项

LCP 的训练目标在标准强化学习目标上增加了一个可微分的梯度惩罚项：

$$\max_{\pi} J(\pi) - \lambda_{\mathrm{gp}} \mathbb{E}_{\mathbf{s}, \mathbf{a} \sim \mathcal{D}} \left[ \|\nabla_{\mathbf{s}} \log \pi(\mathbf{a} | \mathbf{s})\|^2 \right]$$

（Equation 7）。其中：

- $J(\pi)$ 是标准的策略优化目标（期望累积回报）；
- $\lambda_{\mathrm{gp}}$ 是梯度惩罚系数，控制平滑约束的强度；
- $\nabla_{\mathbf{s}} \log \pi(\mathbf{a} | \mathbf{s})$ 是策略对数概率关于输入状态 $\mathbf{s}$ 的梯度；
- $\mathbb{E}_{\mathbf{s}, \mathbf{a} \sim \mathcal{D}}$ 表示在训练数据分布 $\mathcal{D}$ 上求期望。

该惩罚项直接作用于策略函数的梯度范数平方，迫使策略在训练数据分布上对输入变化不敏感，从而抑制高频抖动行为。由于梯度惩罚完全可微分，它可以无缝集成到任何基于梯度的策略优化框架中，无需手工调参或引入不可微操作。

### 集成到 ROA 训练框架

LCP 被集成到 Regularized Online Adaptation (ROA) 框架中，完整的训练损失函数为：

$$L(\theta_{\pi}, \theta_{\mu}, \theta_{\phi}) = -L^{\mathrm{PPO}}(\theta_{\pi}, \theta_{\mu}) + \lambda \|\mathbf{z}^{\mu} - \mathrm{sg}[\mathbf{z}^{\phi}]\| + \|\mathrm{sg}[\mathbf{z}^{\mu}] - \mathbf{z}^{\phi}\| + \lambda_{\mathrm{gp}} L_{\mathrm{gp}}(\pi)$$

（Equation 8）。其中：

- $L^{\mathrm{PPO}}$ 是标准 PPO 损失；
- $\mathbf{z}^{\mu}$ 是编码器 $\mu$ 从特权信息 $\mathbf{e}$ 中提取的潜在向量；
- $\mathbf{z}^{\phi}$ 是适配模块 $\phi$ 仅基于观测历史估计的潜在向量；
- $\mathrm{sg}[\cdot]$ 表示停止梯度操作符；
- 中间两项是对编码器和适配模块的嵌入对齐损失；
- $L_{\mathrm{gp}}(\pi)$ 是梯度惩罚项，其具体形式为：

$$L_{\mathrm{gp}}(\pi) = \mathbb{E}_{\mathbf{s}, \mathbf{a} \sim \mathcal{D}} \left[ \|\nabla_{\mathbf{s}} \log \pi(\mathbf{a} | \mathbf{s})\|^2 \right]$$

（Equation 9）。

### 关键设计选择：梯度惩罚的作用范围

消融实验（TABLE I(c)）揭示了一个重要的实现细节：**梯度惩罚应用于策略的整个输入观测（当前观测 + 历史观测）比仅应用于当前观测能获得更好的平滑效果和任务性能**。这意味着约束策略对历史信息的敏感性同样关键——仅约束当前观测可能导致策略通过历史窗口“绕过”平滑约束，产生隐式的高频行为。这一发现表明 LCP 的有效性依赖于对策略完整输入上下文的 Lipschitz 约束。

### 超参数敏感性

梯度惩罚系数 $\lambda_{\mathrm{gp}}$ 是 LCP 的核心超参数。消融实验（TABLE I(b), Fig. 6）表明 $\lambda_{\mathrm{gp}} = 0.002$ 在平滑度和任务回报之间取得了最佳平衡；过大的 $\lambda_{\mathrm{gp}}$ 会过度压制策略的表达能力，显著损害任务学习。目前该系数需要针对不同机器人形态手动调节，尚未实现自动化选择。

## 实验与关键发现

### 核心实验设计

所有实验均基于 **Regularized Online Adaptation (ROA)** 框架，采用一致的 PPO 算法和域随机化设置。训练使用 IsaacGym 仿真器，在 1000 个并行环境中进行，每个环境运行 500 步（对应约 10 秒时钟时间）。所有方法均使用三个随机种子训练，结果报告均值和标准差。对比基线包括：

- **No Smoothing**：无任何平滑处理的 RL 训练基线。
- **Smoothness Rewards**：显式惩罚关节速度、加速度、动作变化率等指标（Fu et al., CoRL 2021），权重经人工调优。
- **Low-pass Filters**：对输出动作应用低通滤波（Ji et al., IROS 2022），按先前工作的标准配置。

LCP 使用梯度惩罚系数 $\lambda_{\mathrm{gp}} = 0.002$，惩罚项作用于策略的**整个输入观测**（当前观测 + 历史观测）。

### 主结果：平滑度与任务性能

**LCP 在平滑度指标上与显式平滑奖励方法相当。** Fig. 4 展示了训练过程中记录的多个平滑度指标（Action Jitter、DoF Velocity、Energy 等），LCP 产生的平滑行为与使用显式平滑奖励训练的策略水平相当，且明显优于无平滑基线和低通滤波方法。

**LCP 在任务回报上与平滑奖励方法达到相似水平。** TABLE I(a) 和 Fig. 5 的定量对比显示，LCP（$\lambda_{\mathrm{gp}}=0.002$）在 Fourier GR1 平台上取得的 Task Return 为 $26.03 \pm 1.51$，Action Jitter 为 $3.21 \pm 0.11$ rad/s³，与经过人工调优权重的平滑奖励方法表现相当。这表明 LCP 能够作为平滑奖励的有效替代方案，同时避免了繁琐的手工调参过程。

### 消融实验

**梯度惩罚系数 $\lambda_{\mathrm{gp}}$ 存在最优区间。** TABLE I(b) 和 Fig. 6 显示，$\lambda_{\mathrm{gp}} = 0.002$ 在平滑度和任务回报之间取得了最佳平衡。过大的 $\lambda_{\mathrm{gp}}$（如 0.005）会显著损害策略学习能力，导致任务回报大幅下降。这说明梯度惩罚的强度需要谨慎控制——过强的 Lipschitz 约束会限制策略的表达能力，阻碍其学习有效的运动行为。

**梯度惩罚作用于整个输入观测优于仅作用于当前观测。** TABLE I(c) 比较了两种梯度惩罚作用范围：仅对当前观测施加惩罚，与对包含历史观测的完整输入施加惩罚。结果表明，对完整输入施加梯度惩罚能获得更好的平滑效果和任务性能。这验证了历史观测信息对于生成平滑动作序列的重要性——约束策略对历史状态变化的敏感度，有助于抑制动作序列中的高频抖动。

**LCP 可有效替代低通滤波。** TABLE I(a) 显示，低通滤波方法虽然能改善部分平滑度指标，但其任务回报低于 LCP 和平滑奖励方法。这是因为低通滤波是作用于动作输出的后处理步骤，不可微分，无法在训练过程中被策略优化所感知。

### Sim-to-Sim 迁移

TABLE II 报告了从 IsaacGym 到 MuJoCo 的 sim-to-sim 迁移性能。LCP 训练的策略在迁移后保持了较好的任务性能：Fourier GR1 的 Task Return 从 $26.03 \pm 1.51$ 降至 $24.33 \pm 1.25$，下降幅度较小。较大尺寸的机器人（Fourier GR1、Unitree H1）比较小尺寸的机器人（Berkeley Humanoid，$26.50 \pm 0.57$）表现出更明显的性能下降，这可能与较大机器人的动力学复杂度更高、对仿真环境差异更敏感有关。

### 真实世界部署

LCP 训练的策略成功**零样本部署**到多种真实仿人机器人（Fig. 1, Fig. 7），包括 Fourier GR1 等平台，实现了平滑鲁棒的行走。TABLE III 报告了真实世界部署的定量性能：在平滑地形上，LCP 策略的 Action Jitter 仅为 $1.12 \pm 0.16$ rad/s³，表现出优秀的平滑性。策略还能抵御外力干扰并在不规则地形上恢复稳定行走（Fig. 1），验证了 LCP 在 sim-to-real 迁移中的鲁棒性。

### 失败模式与局限

1. **高动态技能的未知适用性**：LCP 仅在步行和转向任务上验证，尚未在跑、跳等需要更高动态响应能力的技能上测试。高动态任务可能天然需要较大的策略梯度，Lipschitz 约束是否会限制爆发力输出有待验证。

2. **$\lambda_{\mathrm{gp}}$ 的手动调参负担**：虽然 LCP 消除了平滑奖励的多项权重调优，但梯度惩罚系数 $\lambda_{\mathrm{gp}}$ 仍需手动调节。不同机器人形态或任务可能需要重新搜索最优值，目前缺乏自动化调节机制。

3. **真实世界测试的局限性**：真实世界部署的定量评估局限于特定地形（平滑地面）和特定机器人类别，未在更广泛的环境扰动（如粗糙地形、外部推力）下进行系统的定量测试。

4. **力矩控制场景未验证**：当前策略输出目标关节位置，通过 PD 控制器转化为力矩。若策略直接输出力矩指令，梯度惩罚的有效性有待进一步验证——力矩输出的高频变化可能对接触动力学有更复杂的影响。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2410_11825/figures/004_Figure.jpg]]

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2410_11825/figures/007_Table.jpg]]
*Table: I: Ablation Studies. All policies are trained with three random seeds and tested in 1000 environments for 500 steps, corresponding to 10 seconds clock time*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2410_11825/figures/008_Table.jpg]]
*Table: II: Sim-to-sim perfomance when transferring policies trained in IsaacGym to Mujoco. All policies are trained with three random seeds and tested for 3 trials with 500 steps, corresponding to 10 seconds per trial*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2410_11825/figures/010_Table.jpg]]
*Table: III: Performance during real-world deployment. Performance for each method is calculated across 3 models from different training runs. Each model is executed for 10 seconds. Standard deviation is recorded for each test*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2410_11825/figures/011_Table.jpg]]
*Table: IV: Terms and weights of regularization rewards*

## 定位与知识库关联

### 1. 方法关系图谱

#### 1.1 核心基线对比

LCP 直接对标的基线方法可分为三类，分别代表当前处理 RL 策略抖动问题的主流范式：

| 基线方法 | 代表工作 | 核心机制 | 根本局限 |
|----------|----------|----------|----------|
| **Smoothness Rewards** | Fu et al. (CoRL 2021) | 在环境奖励中加入关节速度、加速度、力矩变化率等惩罚项 | 奖励权重需大量手工调参；惩罚项不可微分，无法直接优化策略参数的平滑性；不同机器人形态需重新设计奖励组合 |
| **Low-pass Filters** | Ji et al. (IROS 2022) | 对策略输出的动作序列进行低通滤波，抑制高频分量 | 滤波操作不可微分，阻断了梯度回传；引入相位延迟，影响动态响应；截止频率需手动设定 |
| **No Smoothing** | — | 无任何平滑处理的 PPO 基线 | 产生严重的高频 bang-bang 控制，无法 sim-to-real 迁移 |

LCP 与上述方法的本质差异在于：**将平滑性约束直接嵌入策略的参数优化过程中**，而非作为外部后处理或间接奖励信号。具体而言，LCP 在训练损失中加入可微分的梯度惩罚项 $\lambda_{\mathrm{gp}} \mathbb{E}[||\nabla_{\mathbf{s}} \log \pi(\mathbf{a}|\mathbf{s})||^2]$，直接约束策略函数关于输入观测的局部 Lipschitz 常数。

#### 1.2 与相关工作的联系与差异

**Lipschitz 约束在深度学习中的应用**：Lipschitz 连续性作为神经网络的正则化手段已在多个领域得到验证，包括 GAN 训练的梯度惩罚（Gulrajani et al., 2017）、对抗鲁棒性（Cisse et al., 2017）、以及连续控制的动作平滑性（Song et al., 2023）。然而，这些工作多聚焦于离线设置或监督学习场景。LCP 的独特贡献在于：**首次将可微分的 Lipschitz 约束引入基于 PPO 的在线 RL 训练框架中，专门解决仿人机器人运动控制的平滑性问题**。

**教师-学生蒸馏框架**：该框架通过特权信息蒸馏实现 sim-to-real 迁移，是 LCP 训练流程的重要组成部分。策略 $\pi$ 在训练阶段通过编码器 $\mu$ 获取特权信息 $\mathbf{e}$（如地面摩擦系数、接触力等），同时训练适配模块 $\phi$ 仅从观测历史中估计潜在向量 $\mathbf{z}^{\phi}$，使其逼近 $\mathbf{z}^{\mu}$。LCP 的梯度惩罚在此框架中作用于策略 $\pi$ 的完整输入观测（当前观测 + 历史观测），消融实验证实这比仅约束当前观测能获得更好的平滑效果和任务性能（TABLE I(c)）。

**域随机化**：LCP 继承了域随机化的训练范式，在仿真中大规模随机化物理参数以增强策略鲁棒性。LCP 的梯度惩罚与域随机化正交——前者约束策略的局部行为平滑性，后者扩展策略的泛化边界。

### 2. 适用边界

#### 2.1 已验证的有效范围

- **任务类型**：仿人机器人步行和原地转向，速度指令范围为 0–0.5 m/s 的前向/侧向移动及 0–0.5 rad/s 的偏航旋转。
- **机器人平台**：Fourier GR1、Unitree H1、Berkeley Humanoid 三种不同形态的仿人机器人，均采用目标关节位置的动作输出，通过 PD 控制器转化为关节力矩。
- **动作空间**：目标关节位置（position control），未验证直接力矩输出场景。
- **观测空间**：包含本体感受信息（关节位置、速度、IMU 数据）和速度指令，以及历史观测的堆叠。
- **训练框架**：基于 PPO 的 Regularized Online Adaptation (ROA) 框架，在 IsaacGym 仿真器中并行训练 1000 个环境。

#### 2.2 已知局限

1. **任务范围受限**：仅在步行和转向任务上验证，尚未延伸到跑、跳、上下楼梯等更高动态技能。论文明确指出，更高动态技能可能需要额外的平滑技巧或不同的 $\lambda_{\mathrm{gp}}$ 设置。

2. **动作空间限制**：策略输出目标关节位置，通过 PD 控制器转化为力矩。若直接输出力矩，LCP 的效果有待进一步验证——力矩输出的高频分量可能对梯度惩罚的敏感度不同。

3. **超参数敏感性**：梯度惩罚系数 $\lambda_{\mathrm{gp}}$ 需要手动调节。消融实验表明，$\lambda_{\mathrm{gp}}=0.002$ 在 Fourier GR1 上取得最佳平衡；过大的 $\lambda_{\mathrm{gp}}$（如 0.01）会显著损害策略学习（Fig. 6）。不同机器人形态或任务可能需要重新搜索最优值，目前缺乏自动化调节机制。

4. **真实世界测试有限**：真实世界部署的定量评估局限于平整地形和特定机器人类别（TABLE III），未在更广泛的环境扰动（如强风、不平坦地形、外力冲击）下充分量化测试。虽然 Fig. 1 和 Fig. 7 展示了对外力干扰的定性鲁棒性，但缺乏系统的定量分析。

5. **Sim-to-sim 迁移的揭示**：从 IsaacGym 到 MuJoCo 的 sim-to-sim 迁移中，较大机器人（Fourier GR1, Unitree H1）的任务回报下降了约 6–8%（TABLE II），表明 LCP 训练的平滑策略仍对仿真器动力学差异敏感，sim-to-real 的泛化边界尚不完全明确。

### 3. 开放问题

1. **动态技能的扩展性**：LCP 是否能直接推广到跑步、跳跃等需要更高加速度和更快速动作切换的动态技能？高动态场景下，过强的 Lipschitz 约束可能抑制必要的快速反应能力，如何自适应地调节约束强度？

2. **超参数自动化**：能否设计自动化策略来调整 $\lambda_{\mathrm{gp}}$，使其适应不同机器人平台和任务？可能的思路包括：基于平滑度指标的在线调节、元学习搜索最优 $\lambda_{\mathrm{gp}}$、或将其作为可学习的参数。

3. **力矩控制的适用性**：在直接力矩输出的控制模式下，LCP 的梯度惩罚是否依然有效？力矩信号的高频特性可能需要不同的约束形式（如对力矩变化率的惩罚），或需与低通滤波等方法结合使用。

4. **操控任务的推广**：在需要高精度力控制的操控任务中，平滑性约束是否会影响精细操作的准确性？Lipschitz 约束与力控精度之间的权衡关系需要进一步研究。

5. **极端 Sim-to-Real 鲁棒性**：LCP 在更极端的 sim-to-real 场景下（如高仿真误差、传感器噪声、执行器延迟）的鲁棒性边界在哪里？梯度惩罚本身是否可能放大仿真偏差对策略的影响？

6. **与其他平滑技术的融合**：LCP 与平滑奖励、低通滤波等方法是否可以互补？例如，在 LCP 基础上加入轻量平滑奖励是否能进一步提升 sim-to-real 迁移性能？初步消融实验（TABLE I(a)）显示 LCP 与平滑奖励的组合效果与单独使用相当，但更系统的组合策略值得探索。

## 原文 PDF

![[paperPDFs/IROS_2025/Learning_Smooth_Humanoid_Locomotion_through_Lipschitz_Constrained_Policies.pdf]]
