---
title: "TD-JEPA: Latent-predictive Representations for Zero-Shot Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/TD_JEPA_Latent_predictive_Representations_for_Zero_Shot_Reinforcement_Learning.pdf
openreview_forum_id: SzXDuBN8M1
aliases:
- TJ
- TD-JEPA
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "采用策略条件的多步时序差分（TD）潜在预测损失，从离线数据中学习状态和任务编码器，使预测器逼近后继特征，从而实现零样本策略优化。"
primary_logic: "通过TD学习政策条件多步潜在预测，预测器可以直接作为后继特征的近似，使得零样本RL可以在潜在空间中通过简单的回归和最大化内积实现。"
claims:
- "TD-JEPA 训练显式状态编码器、任务编码器、策略条件多步预测器以及一组参数化策略，全部在潜在空间中学习。"
- "预测器以 z 为条件，预测由策略 π_z 访问的未来状态的表示。"
- "TD-JEPA 损失仅需要单步转移和策略动作采样，因此可从离线、非策略数据集中估计。"
- "TD-JEPA 的梯度在最优预测器下与用于后继测度逼近的非潜在预测 TD 损失匹配。"
---

# TD-JEPA: Latent-predictive Representations for Zero-Shot Reinforcement Learning

> [!tip] 核心洞察
> 通过TD学习政策条件多步潜在预测，预测器可以直接作为后继特征的近似，使得零样本RL可以在潜在空间中通过简单的回归和最大化内积实现。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | TD-JEPA: 用于零样本强化学习的潜在预测表示 |
| 英文题名 | TD-JEPA: Latent-predictive Representations for Zero-Shot Reinforcement Learning |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=SzXDuBN8M1); [GitHub](https://github.com/facebookresearch/td_jepa) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | TD-JEPA |
| Dataset | DMCRGB (ExoRL), DMC (ExoRL), OGBenchRGB, OGBench |

> [!tip] 效果简介
> - DMCRGB (ExoRL) 上，平均回报 为 628.8 ± 5.5，对比 最优基线（未提供具体数值），变化 N/A (优于所有基线)。
> - DMC (ExoRL) 上，平均回报 为 661.2 ± 6.3，对比 最优基线（未提供具体数值），变化 N/A (优于所有基线)。
> - OGBenchRGB 上，成功率 为 41.34 ± 0.45，对比 最优基线（未提供具体数值），变化 N/A (优于所有基线)。

## 概述

现有无监督零样本强化学习的核心瓶颈在于：潜在预测方法普遍局限于单任务学习、一步预测或在线数据，无法同时处理多步动态、多策略条件与离线数据，导致表示学习无法有效捕获任务相关的长期行为特征。TD-JEPA 针对这一瓶颈，提出以**策略条件的多步时序差分（TD）潜在预测**作为核心学习机制：训练显式分离的状态编码器与任务编码器，配合策略条件多步预测器，使预测器直接逼近后继特征，从而在潜在空间中实现零样本策略优化——仅需线性回归求解任务嵌入，再通过最大化内积即可提取对应策略。

在方法谱系中，TD-JEPA 区别于 **BYOL⋆**（Grill et al., 2020）和 **BYOL-γ⋆**（Lawson et al., 2025）等仅建模行为策略单步动态的潜在预测方法，也不同于 **FB**（Touati & Ollivier, 2021）采用对比损失且不分离状态与任务编码器的方案。其关键改进在于：预测步长从单步扩展为多步 TD 学习，策略条件从无条件变为以策略参数 $z$ 为条件，编码器从单一表示变为显式分离 $\phi$ 与 $\psi$，数据需求从在线策略或蒙特卡洛采样降为仅需离线一步转移数据，训练目标从对比损失转为非对比的 TD-JEPA 损失。

实验覆盖 ExoRL 和 OGBench 共 13 个数据集、65 个任务，涵盖运动、导航与操作场景，同时支持本体感受与像素输入。在 DMCRGB 上平均回报达 $628.8 \pm 5.5$，DMC 上达 $661.2 \pm 6.3$，OGBenchRGB 成功率为 $41.34 \pm 0.45$，OGBench 为 $37.98 \pm 0.77$，整体匹配或超越所有基线。改进概率分析表明 TD-JEPA 相对 FB 和 HILP 具有统计显著的提升。消融实验进一步确认：直接建模策略后继测度优于仅建模行为策略动力学，分离编码器的非对称变体优于对称变体，且预训练表示在微调时能大幅提升样本效率，冻结表示常足以实现快速适应。

## 背景与动机

### 问题背景：无监督零样本强化学习

强化学习（RL）智能体在部署时往往需要快速适应多样化的下游任务，而传统RL方法通常需要为每个新任务从头训练或依赖密集的在线交互与奖励信号，这在实际应用中代价高昂。无监督零样本RL旨在解决这一瓶颈：其核心思路是在无奖励、无任务的离线数据上预训练一组可复用的表示与策略，使得智能体在测试时仅需接收任务描述（如目标状态或奖励函数），即可在不进行额外学习的情况下直接输出近似最优策略。

这一范式面临两个关键挑战。其一，表示学习必须在无奖励信号的前提下捕获环境的长期动力学结构，从而支持对任意下游任务的泛化。其二，预训练过程必须兼容离线、非策略数据，因为在线交互在许多场景（如机器人操作、自动驾驶）中成本过高或存在安全风险。

### 后继特征与值函数线性化

后继特征（Successor Features, SF）为上述问题提供了优雅的理论框架。给定策略 $\pi$，其后继测度 $M^{\pi}$ 定义为从状态-动作对出发，策略在未来访问各状态的折扣分布：

$$M^{\pi}(\mathcal{X} \mid s, a) = \sum_{t=0}^{\infty} \gamma^{t} \mathrm{Pr}(s_{t+1} \in \mathcal{X} | s, a, \pi)$$

若将奖励函数表示为 $r(s) = \psi(s)^{\top} z_r$（其中 $\psi$ 为任务编码器，$z_r$ 为任务嵌入），则动作值函数可线性分解为：

$$Q_{r}^{\pi}(s, a) = F_{\psi}^{\pi}(s, a)^{\top} z_r$$

其中 $F_{\psi}^{\pi}(s, a) = \mathbb{E}_{s^{+} \sim M^{\pi}(\cdot|s,a)} [\psi(s^{+})]$ 即为后继特征。这一分解意味着：若能预先学习到策略集的后继特征和任务编码器，零样本策略优化便可简化为在潜在空间中最大化内积 $F_{\psi}^{\pi}(s, a)^{\top} z$，无需任何在线交互或奖励信号。

### 现有方法的缺口

尽管后继特征框架理论完备，现有方法在实现无监督零样本RL时存在显著局限：

**1. 数据需求与学习范式的矛盾。** 基于后继测度的方法（如 **FB**（Touati & Ollivier, 2021））虽然支持离线数据，但其对比损失在大批量下计算开销大，且对表示的正交性高度敏感。基于潜在预测的方法（如 **BYOL⋆**（Grill et al., 2020）、**BYOL-γ⋆**（Lawson et al., 2025））通过最小化一步潜在动力学预测误差来学习表示，天然兼容离线数据，但它们仅建模单步转移，无法捕获策略的长期行为。

**2. 策略条件建模的缺失。** 一步潜在预测方法通常不区分策略——它们仅学习行为策略下的动力学，而非针对不同任务策略的后继特征。这使得它们在零样本场景中无法直接为任意策略提供值函数近似。**RLDP**（Jajoo et al., 2025）虽然引入了潜在动态预测，但同样局限于单步、非策略条件的设定。

**3. 编码器角色的模糊性。** 部分方法（如FB）使用单一表示同时充当状态编码器和任务编码器，这在理论上是可行的（通过对称后继测度假设），但限制了表示的表达能力，尤其在视觉输入等复杂观测空间中。

**4. 离线学习的稳定性。** 基于蒙特卡洛采样的多步预测损失需要从策略的后继分布中采样完整轨迹，这要求在线数据或行为策略与目标策略高度一致，在离线、非策略数据集中难以实现。

### 核心动机

上述缺口指向一个核心瓶颈：**现有潜在预测方法局限于单任务学习、一步预测或在线数据，无法同时处理多步、多策略、离线数据，导致在无监督零样本RL中性能受限。**

TD-JEPA的提出正是为了突破这一瓶颈。其核心动机是通过将时序差分（TD）学习引入潜在预测框架，使得多步、策略条件的后继特征逼近可以从离线、非策略数据中高效学习。具体而言：

- **用TD替代蒙特卡洛**：TD学习仅需单步转移数据即可估计长期期望，天然适配离线数据集。
- **策略条件预测器**：让预测器以任务嵌入 $z$ 为条件，直接建模不同策略 $\pi_z$ 的后继特征，而非仅拟合行为策略的动力学。
- **分离状态与任务编码器**：显式训练独立的 $\phi$（状态编码器）和 $\psi$（任务编码器），允许二者在维度和结构上非对称，提升表示灵活性。

通过这一设计，TD-JEPA在潜在空间中同时实现了后继特征学习和策略优化，使得零样本RL可以简化为简单的回归与内积最大化，无需对比损失或在线采样。

## 核心创新

TD-JEPA 的核心创新在于将**时序差分学习**引入多策略潜在预测框架，使预测器直接逼近后继特征，从而在潜在空间中实现零样本策略优化。相对于现有方法，其关键改进体现在以下五个维度。

### 1. 从单步预测到多步 TD 预测

传统潜在预测方法（如 **BYOL⋆**（Grill et al., 2020）、**BYOL-γ⋆**（Lawson et al., 2025））仅建模一步潜在动态：

$$\mathcal{L}_{\mathrm{one-step}}(\phi, T) = \mathbb{E}_{s \sim \rho, a \sim \pi(\cdot|s), s' \sim P(\cdot|s,a)} [||T(\phi(s)) - \overline{\phi(s')}||^{2}]$$

这种单步损失无法捕获长期依赖关系，且无法从离线数据中学习多步动态。TD-JEPA 将预测目标扩展为**多步时序差分形式**：

$$\mathcal{L}_{\mathrm{TD-JEPA}}(\phi, T_{\phi}, \psi) = \mathbb{E}_{(s,a,s')\sim \mathcal{D}, z\sim Z, a'\sim \pi_z(\cdot|s')} \big[ \| T_{\phi}(\phi(s), a, z) - \overline{\psi(s')} - \gamma \overline{T_{\phi}(\phi(s'), a', z)} \|^{2} \big]$$

该损失仅需单步转移和策略动作采样，因此可直接从离线、非策略数据集中估计——这是蒙特卡洛式潜在预测损失无法做到的。

### 2. 策略条件化：从行为策略到多策略建模

**BYOL⋆** 和 **BYOL-γ⋆** 的预测器仅建模行为策略诱导的动力学，不区分不同策略的访问分布。TD-JEPA 将预测器设计为**策略条件化**：以任务隐变量 $z$ 为条件，预测由策略 $\pi_z$ 访问的未来状态表示。训练完成后，预测器 $T_{\phi}$ 直接近似各策略的后继特征 $F_{\psi}^{\pi_z}$，使得零样本策略优化简化为最大化内积：

$$\pi_z(\phi(s)) = \arg\max_a T_{\phi}(\phi(s), a, z)^{\top} z$$

消融实验证实了这一设计的有效性：Figure 3（左）显示，直接建模策略后继测度的 TD-JEPA 在归一化性能上平均优于仅建模行为策略动力学的 BYOL⋆ 和 BYOL-γ⋆。

### 3. 编码器分离：状态编码与任务编码解耦

**FB**（Touati & Ollivier, 2021）使用单一表示同时充当状态和任务编码器，这种对称设计限制了表示的灵活性。TD-JEPA 引入**非对称变体**，显式分离状态编码器 $\phi: \mathcal{S} \to \mathbb{R}^{d_\phi}$ 和任务编码器 $\psi: \mathcal{S} \to \mathbb{R}^{d_\psi}$，并通过双向潜在预测（$T_{\phi}$ 从 $\phi$ 预测 $\psi$ 空间，$T_{\psi}$ 反向预测）联合训练。Figure 3（右）表明，分离编码器的非对称变体在多数领域中优于单一编码器的对称变体，尽管计算开销略高（Table 3）。

### 4. 非对比学习目标

**FB** 采用对比损失，需在每批次中计算成对内积，计算复杂度随批次大小平方增长。TD-JEPA 的核心学习目标是**非对比式**的 TD 潜在预测损失，仅需前向传播和逐元素回归，计算效率更高。Figure 5（右）进一步显示，TD-JEPA 的非对比变体在归一化性能上优于其对比变体。

### 5. 理论保证：梯度等价性

TD-JEPA 提供了首个将潜在预测 TD 学习与后继测度 TD 学习建立联系的理论结果。**Theorem 3** 证明，在最优预测器条件下，TD-JEPA 损失关于编码器 $\phi$ 和 $\psi$ 的梯度与用于后继测度逼近的非潜在预测 TD 损失梯度精确匹配：

$$\nabla_\phi \mathcal{L}_{\mathrm{TD-JEPA}}(\phi, T_z, \psi) = \nabla_\phi \mathcal{L}_{\mathrm{fw}}(\phi, T_z, \psi)$$

$$\nabla_\psi \mathcal{L}_{\mathrm{TD-JEPA}}(\psi, T_z, \phi) = \nabla_\psi \mathcal{L}_{\mathrm{fw}}(\phi, T_z, \psi)$$

这意味着 TD-JEPA 在潜在空间中的学习动态等价于在原始状态空间中显式逼近后继测度，但避免了在高维状态空间中进行矩阵运算的计算负担。

### 方法瓶颈与局限

尽管 TD-JEPA 在上述维度实现了显著改进，仍需注意以下约束：

- **表示坍缩风险**：非对比学习天然面临表示坍缩问题，TD-JEPA 依赖正交正则化 $\widehat{\mathcal{L}}_{\mathrm{REG}}$ 来维持特征多样性，正则化系数需针对不同领域仔细调节。
- **线性奖励假设**：零样本策略检索仅支持任务编码器 $\psi$ 定义的线性奖励函数空间 $r(s) = \psi(s)^{\top} z_r$，对非线性奖励结构的泛化能力受限。
- **离线偏差**：在离线学习场景下，行为策略偏差可能影响预测器对未访问区域的估计精度，需额外行为克隆正则化辅助。

## 整体框架

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_SzXDuBN8M1/figures/003_Figure_2.jpg]]
*Figure 2: Probabilities of improvement: how likely is method X to outperform method Y on a random domain? We report symmetrized 95% simple bootstrap confidence intervals. Dotted lines surround matches in which the improvement is statistically significant*

TD-JEPA 的整体训练流程如图 1 所示，其核心思想是：**在潜在空间中同时学习状态编码器、任务编码器、策略条件多步预测器以及一组参数化策略，使预测器逼近后继特征，从而在零样本 RL 中直接通过回归和内积最大化实现策略优化。**

### 模块组成与数据流

系统包含以下核心模块，它们从离线、无奖励的转移数据中端到端联合训练：

**1. 状态编码器 φ**
将原始状态 $s$ 映射为 $d_\phi$ 维潜在向量 $\phi(s)$。该表示供预测器和策略共享使用，是所有下游计算的基础。

**2. 任务编码器 ψ**
将状态 $s$ 映射为 $d_\psi$ 维任务表示 $\psi(s)$，用于定义奖励函数空间。给定任务嵌入 $z$，奖励函数可线性表示为 $r(s) = \psi(s)^\top z$。这一设计使得零样本策略检索仅需对少量奖励样本进行线性回归即可获得 $z_r$。

**3. 策略条件预测器 $T_\phi$ 与 $T_\psi$**
$T_\phi: \mathbb{R}^{d_\phi} \times \mathcal{A} \times \mathcal{Z} \to \mathbb{R}^{d_\psi}$ 以状态编码 $\phi(s)$、动作 $a$ 和策略隐变量 $z$ 为条件，预测由 $\pi_z$ 访问的未来状态在 $\psi$ 空间下的期望表示。对称地，$T_\psi$ 从 $\psi(s)$ 预测未来状态在 $\phi$ 空间下的期望。训练收敛后，$T_\phi$ 直接近似后继特征 $F_\psi^{\pi_z}$。

**4. 策略 $\pi_z$**
以 $\phi(s)$ 和任务 $z$ 为输入，通过最大化 $T_\phi(\phi(s), a, z)^\top z$ 输出动作。策略与编码器、预测器同步训练，无需额外奖励信号。

**5. 目标网络（EMA）**
通过指数移动平均维护 $\phi^-$、$T_\phi^-$、$\psi^-$、$T_\psi^-$ 的慢更新副本，为 TD 学习提供稳定目标，防止训练震荡。

**6. 协方差正则化**
对 $\phi$ 和 $\psi$ 施加正交正则化 $\widehat{\mathcal{L}}_{\text{REG}}$，鼓励特征间去相关，防止表示坍缩到平凡解。这是非对比学习方法稳定训练的关键。

### 训练流程

TD-JEPA 的训练循环（Algorithm 1）从离线数据集中采样批量转移 $(s, a, s')$，同时采样策略隐变量 $z \sim \mathcal{Z}$。每一步迭代执行以下更新：

1. **更新 $\phi$ 和 $T_\phi$**：最小化非对称 TD-JEPA 损失 $\widehat{\mathcal{L}}_{\text{TD-JEPA}}(\phi, T_\phi, \psi)$ 与正交正则项 $\lambda \widehat{\mathcal{L}}_{\text{REG}}(\phi)$。
2. **更新 $\psi$ 和 $T_\psi$**：最小化对称的 TD-JEPA 损失 $\widehat{\mathcal{L}}_{\text{TD-JEPA}}(\psi, T_\psi, \phi)$ 与正交正则项 $\lambda \widehat{\mathcal{L}}_{\text{REG}}(\psi)$。
3. **更新策略 $\pi$**：最小化 actor 损失 $\widehat{\mathcal{L}}_{\text{actor}}(\pi) = -\frac{1}{B} \sum_i T_\phi(\phi(s_i), \hat{a}_i, z_i)^\top z_i$。
4. **更新目标网络**：通过 EMA 同步 $\phi^-$、$T_\phi^-$、$\psi^-$、$T_\psi^-$。

### 零样本策略检索

预训练完成后，面对新任务时仅需少量带奖励样本 $\mathcal{D}_{\text{rsd}} = \{(s, r)\}$，通过线性回归求解任务嵌入：
$$z_r = \arg\min_z \mathbb{E}_{(s,r) \sim \mathcal{D}_{\text{rsd}}}[(r - \psi(s)^\top z)^2]$$
随后直接使用策略 $\pi_{z_r}$ 执行，无需任何额外训练。

### 关键设计选择

- **非对称架构**：显式分离状态编码器 $\phi$ 和任务编码器 $\psi$，使两者可学习不同维度和结构的表示，平均性能优于单一编码器的对称变体（Figure 3 右）。
- **TD 而非 MC**：TD-JEPA 损失仅需单步转移和策略动作采样，因此可从离线、非策略数据集中估计，无需蒙特卡洛回滚（Eq. 9 vs Eq. 8）。
- **非对比学习**：与 FB 的对比损失不同，TD-JEPA 核心为非对比的潜在预测，避免了批量内成对点积的计算开销。

### 理论支撑

定理 3 表明，在最优预测器下，TD-JEPA 对 $\phi$ 和 $\psi$ 的梯度与用于后继测度逼近的非潜在预测 TD 损失的梯度完全一致。这建立了潜在预测 TD 学习与后继测度 TD 学习之间的形式化联系，为方法的正确性提供了理论保证。

## 核心模块与公式推导

### 3.1 核心模块架构

TD-JEPA 的核心架构由四个显式分离的模块组成，全部在潜在空间中端到端训练：

- **状态编码器** $\phi: \mathcal{S} \to \mathbb{R}^{d_\phi}$：将原始状态映射为 $d_\phi$ 维潜在向量，供预测器和策略使用。
- **任务编码器** $\psi: \mathcal{S} \to \mathbb{R}^{d_\psi}$：将状态映射为 $d_\psi$ 维任务表示，定义线性奖励函数空间（即 $r(s) = \psi(s)^\top z_r$）。
- **策略条件预测器** $T_\phi: \mathbb{R}^{d_\phi} \times \mathcal{A} \times \mathcal{Z} \to \mathbb{R}^{d_\psi}$ 和对称预测器 $T_\psi: \mathbb{R}^{d_\psi} \times \mathcal{A} \times \mathcal{Z} \to \mathbb{R}^{d_\phi}$：以策略参数 $z$ 为条件，预测未来状态在对方编码器空间下的期望表示。
- **参数化策略** $\pi_z$：以 $\phi(s)$ 和任务嵌入 $z$ 为输入，通过最大化 $T_\phi(\phi(s), a, z)^\top z$ 输出动作。

此外，训练中维护目标网络 $\phi^-, T_\phi^-, \psi^-, T_\psi^-$ 通过指数移动平均（EMA）提供稳定的自举目标，并施加协方差正则化 $\widehat{\mathcal{L}}_{\text{REG}}$ 防止表示坍缩。

### 3.2 核心公式推导

#### 3.2.1 后继测度与后继特征

策略 $\pi$ 诱导的折扣状态访问分布由**后继测度**定义：

$$M^{\pi}(\mathcal{X} \mid s, a) = \sum_{t=0}^{\infty} \gamma^{t} \mathrm{Pr}(s_{t+1} \in \mathcal{X} \mid s, a, \pi) \tag{Eq. 1}$$

对于线性奖励函数 $r(s) = \psi(s)^\top z_r$，Q 值可分解为**后继特征**与任务嵌入的内积：

$$Q_r^{\pi}(s, a) = F_\psi^{\pi}(s, a)^\top z_r, \quad F_\psi^{\pi}(s, a) = \mathbb{E}_{s^+ \sim M^{\pi}(\cdot \mid s, a)}[\psi(s^+)] \tag{Eq. 4}$$

其中 $F_\psi^{\pi}$ 是策略 $\pi$ 在 $\psi$ 空间下的后继特征。

#### 3.2.2 从蒙特卡洛到时序差分的潜在预测

若直接以蒙特卡洛方式训练预测器逼近后继特征，需从 $M^{\pi_z}$ 中采样未来状态 $s^+$：

$$\mathcal{L}_{\mathrm{MC-JEPA}}(\phi, T_\phi, \psi) = \mathbb{E}_{(s,a)\sim\mathcal{D}, z\sim\mathcal{Z}, s^+\sim M^{\pi_z}(\cdot|s,a)} \big[ \| T_\phi(\phi(s), a, z) - \overline{\psi(s^+)} \|^2 \big] \tag{Eq. 8}$$

其中上划线表示停止梯度。该损失依赖多步轨迹采样，无法从离线一步转移数据中估计。

**关键突破**：利用后继测度满足的 Bellman 方程 $M^{\pi} = P^{\pi} + \gamma P^{\pi} M^{\pi}$，可将其转化为仅需单步转移的时序差分形式：

$$\mathcal{L}_{\mathrm{TD-JEPA}}(\phi, T_\phi, \psi) = \mathbb{E}_{\substack{(s,a,s')\sim\mathcal{D}, z\sim\mathcal{Z} \\ a'\sim\pi_z(\cdot|s')}} \big[ \| T_\phi(\phi(s), a, z) - \overline{\psi(s')} - \gamma \overline{T_\phi(\phi(s'), a', z)} \|^2 \big] \tag{Eq. 9}$$

- $T_\phi(\phi(s), a, z)$：当前状态-动作对的预测。
- $\overline{\psi(s')}$：下一状态在 $\psi$ 空间下的即时特征（停止梯度）。
- $\gamma \overline{T_\phi(\phi(s'), a', z)}$：下一状态-动作对预测的折扣自举目标（停止梯度）。

该 TD 损失仅需采样单步转移 $(s, a, s')$ 和策略动作 $a' \sim \pi_z(\cdot|s')$，因此可从离线、非策略数据集中估计。对称方向 $\mathcal{L}_{\mathrm{TD-JEPA}}(\psi, T_\psi, \phi)$ 结构完全对称。

#### 3.2.3 理论等价性

在最优预测器条件下，TD-JEPA 的梯度与非潜在预测的 TD 损失梯度完全匹配（Theorem 3）：

$$\nabla_\phi \mathcal{L}_{\mathrm{TD-JEPA}}(\phi, T_z, \psi) = \nabla_\phi \mathcal{L}_{\mathrm{fw}}(\phi, T_z, \psi)$$

$$\nabla_\psi \mathcal{L}_{\mathrm{TD-JEPA}}(\psi, T_z, \phi) = \nabla_\psi \mathcal{L}_{\mathrm{fw}}(\phi, T_z, \psi)$$

其中 $\mathcal{L}_{\mathrm{fw}}$ 是直接在后继测度空间上的前向 TD 损失。这意味着 TD-JEPA 在潜在空间中的学习动态等价于显式逼近后继测度，但无需在高维状态空间中操作。

#### 3.2.4 策略训练与零样本检索

策略通过最大化预测器输出与任务嵌入的内积训练：

$$\widehat{\mathcal{L}}_{\mathrm{actor}}(\pi) = -\frac{1}{B} \sum_{i=1}^{B} T_\phi(\phi(s_i), \hat{a}_i, z_i)^\top z_i$$

零样本推理时，给定少量奖励样本 $\mathcal{D}_{\mathrm{rsd}}$，通过线性回归求解任务嵌入：

$$z_r = \arg\min_z \mathbb{E}_{(s,r)\sim\mathcal{D}_{\mathrm{rsd}}} [(r - \psi(s)^\top z)^2]$$

随后直接使用 $\pi_{z_r}$ 执行，无需任何梯度更新。

#### 3.2.5 正则化

为防止表示坍缩，施加正交正则化：

$$\widehat{\mathcal{L}}_{\mathrm{REG}}(\phi) = \frac{1}{2B(B-1)} \sum_{i\neq j} (\phi(s_i)^\top \phi(s_j))^2 - \frac{1}{B} \sum_i \phi(s_i)^\top \phi(s_i)$$

该正则项鼓励特征间余弦相似度趋近于零，同时约束特征范数。

## 实验与分析

### 主结果：零样本RL基准性能

TD-JEPA 在 ExoRL 和 OGBench 共计 13 个数据集、65 个任务上进行了零样本评估，涵盖运动（walker, cheetah, quadruped）、导航（pointmass, antmaze 系列）和操作（cube-single, cube-double, scene, puzzle-3x3）任务，同时支持本体感受和像素级视觉输入。

**Table 1** 汇总了各算法的平均得分。TD-JEPA 在所有四个聚合基准上均取得最优：

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_SzXDuBN8M1/figures/002_Table_1.jpg]]

- **DMCRGB**（视觉运动控制）：TD-JEPA 平均回报 **628.8 ± 5.5**，优于所有基线。
- **DMC**（本体感受运动控制）：平均回报 **661.2 ± 6.3**，同样最优。
- **OGBenchRGB**（视觉导航与操作）：成功率 **41.34 ± 0.45**。
- **OGBench**（本体感受导航与操作）：成功率 **37.98 ± 0.77**。

在统计显著性层面，**Figure 2** 展示了各方法对的改进概率矩阵。TD-JEPA 相对于 **FB**（Touati & Ollivier, 2021）和 **HILP**（Park et al., 2024）的改进在多数视觉域上达到统计显著（对称化 95% bootstrap 置信区间不跨越零线），表明其零样本策略质量具有稳健优势。

### 消融实验：关键设计选择

#### 策略条件多步预测 vs. 单步行为动力学

**Figure 3 (左)** 比较了 TD-JEPA 与两类潜在预测方法——**BYOL⋆**（Grill et al., 2020）和 **BYOL-γ⋆**（Lawson et al., 2025）。后两者仅建模行为策略诱导的单步潜在动力学，缺乏策略条件能力。结果表明，TD-JEPA 的归一化零样本性能在平均意义上显著高于这两类方法，验证了直接建模策略后继测度（而非行为策略动力学）对零样本泛化的关键作用。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_SzXDuBN8M1/figures/005_Figure_3.jpg]]
*Figure 3: Left: normalized zero-shot performance for latent-predictive methods. Right: difference in normalized performance between TD-JEPA and its symmetric variant. Error bars represent standard errors on normalized performance or its differences, respectively*

#### 非对称编码器 vs. 对称编码器

**Figure 3 (右)** 展示了 TD-JEPA 与其对称变体（单一编码器同时充当状态和任务编码器）的性能差异。非对称变体（显式分离状态编码器 φ 和任务编码器 ψ）在多数任务上带来正向增益，说明分离的编码器结构有助于学习更具判别力的任务表示。**Table 3** 提供了完整的数值对比，非对称 TD-JEPA 在 DMCRGB 和 OGBenchRGB 上均优于对称变体，但训练速度较慢（见 **Table 4**）。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_SzXDuBN8M1/figures/020_Table_3.jpg]]
*Table 3: Performance of TD-JEPA and symmetric variants (contrastive and latent-predictive) in DMC (returns) and OGBench (success rate) with either proprioception or RGB inputs. We report means and standard errors across seeds. Numbers are bold for top algorithms if confidence intervals overlap*

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_SzXDuBN8M1/figures/021_Table_4.jpg]]
*Table 4: Average number of iterations (gradient steps) per second of each algorithm for the experiments in Table 1. All methods are trained on the same hardware (a single V100 GPU) and use similarly sized architectures (see Appendix E). One training iteration samples a batch from the dataset and updates all networks once*

#### 显式状态编码器的作用

**Figure 5 (左)** 分析了有无显式状态编码器对零样本基线的影响。结果显示，引入显式编码器（而非直接在原始观测上操作）对多数方法带来正向收益，但影响程度因方法而异。TD-JEPA 本身即依赖显式编码器，该消融主要针对其他基线方法，验证了统一架构比较的公平性。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_SzXDuBN8M1/figures/009_Figure_5.jpg]]
*Figure 5: Difference in normalized performance between zero-shot baselines with and without an explicit encoder (left); normalized performance difference between symmetric TD-JEPA and its contrastive variant (right). Error bars represent standard errors on normalized performance differences*

#### 对比损失 vs. 非对比损失

TD-JEPA 的核心是非对比损失（基于潜在预测的 TD 学习），而 **FB** 使用对比损失。**Figure 5 (右)** 展示了对称 TD-JEPA 与其对比变体的性能差异。非对比变体在多数任务上表现更优，表明潜在预测范式在零样本 RL 场景下可能比对比学习更具优势，且避免了大规模 batch 内 pairwise 计算的开销。

#### 编码器深度的影响

**Table 2** 和 **Figure 7** 系统消融了编码器和预测器的隐藏层数。结果显示，编码器深度对性能的影响具有领域特异性：

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_SzXDuBN8M1/figures/007_Table_2.jpg]]

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_SzXDuBN8M1/figures/016_Figure_7.jpg]]
*Figure 7: Zero-shot performance of TD-JEPA in antmaze-ln (top) and antmaze-ls (bottom) as the number of hidden layers in the encoders and predictors varies (from 0 to 4 and from 1 to 4, respectively)*

- 在视觉域（DMCRGB），更深的编码器（如 4 层 CNN）通常带来更高性能。
- 在本体感受域（如 antmaze），较浅的编码器（1-2 层 MLP）即可达到饱和，过深反而可能导致性能下降。

这一发现对实际部署具有指导意义：不同输入模态需要独立选择编码器容量。

#### 微调样本效率

**Figure 4** 展示了零样本策略在离线（上）和在线（下）微调下的归一化性能曲线。以 TD-JEPA 零样本策略初始化（蓝线和黄线）大幅提升了样本效率，且冻结预训练表示（虚线）通常足以实现快速适应。**Figure 6** 补充了仅加载编码器权重或仅冻结卷积层的微调结果，进一步验证了预训练表示的可迁移性。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_SzXDuBN8M1/figures/006_Figure_4.jpg]]
*Figure 4: Normalized performance of zero-shot policies when fine-tuned offline (top) or online (bottom). Initializing the agent to zero-shot solutions (blue and yellow lines) results in sample-efficient learning; frozen representations (dashed) are often expressive enough to enable fast adaptation*

#### 数据量与训练步长

**Figure 11** 和 **Figure 12** 展示了不同数据集大小（1M、2M、3M 步）下的性能变化。TD-JEPA 在所有数据规模下均保持优势，且性能随数据量增加而提升，表明其离线学习框架具有良好的数据扩展性。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_SzXDuBN8M1/figures/022_Figure_11.jpg]]
*Figure 11: Average performance over all DMC walker and quadruped tasks for varying dataset sizes and number of training steps (1M, 2M, or 3M)*

### 失败模式与局限

1. **表示坍缩风险**：TD-JEPA 依赖正交正则化（见 Algorithm 1 中的 $\widehat{\mathcal{L}}_{\mathrm{REG}}$）防止表示坍缩，正则化系数需针对不同域仔细调节（搜索范围见 **Table 6**），增加了调参负担。
2. **行为策略偏差**：离线学习场景下可能受行为策略分布偏差影响，需额外行为克隆正则化来稳定训练。
3. **线性奖励假设**：零样本策略检索基于 $\psi(s)^\top z_r$ 的线性奖励分解，仅支持任务编码器 ψ 张成的线性奖励函数空间，对非线性奖励结构的任务泛化能力有限。
4. **真实机器人验证缺失**：当前实验全部在模拟器（ExoRL 和 OGBench）上进行，在大规模真实机器人数据集上的表现尚未验证。
5. **计算效率**：非对称 TD-JEPA 虽性能更优，但训练速度慢于对称变体（**Table 4**），在资源受限场景下需权衡。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_SzXDuBN8M1/figures/026_Table_6.jpg]]
*Table 6: Orthonormal regularization ranges for each algorithm. (nav) and (man) indicate navigation and manipulation domains, respectively*

### 关键图表结论总结

| 图表 | 核心结论 |
|------|----------|
| **Table 1** | TD-JEPA 在四大基准上均取得最优平均性能 |
| **Figure 2** | 相对 FB 和 HILP 的改进在多数视觉域统计显著 |
| **Figure 3 (左)** | 策略条件多步预测显著优于单步行为动力学建模 |
| **Figure 3 (右)** | 非对称编码器分离普遍优于对称设计 |
| **Figure 4** | 零样本初始化大幅提升微调样本效率，冻结表示即可快速适应 |
| **Figure 5 (右)** | 非对比损失在零样本 RL 中优于对比损失 |
| **Table 2/Figure 7** | 编码器深度影响具有领域特异性，需独立调节 |
| **Figure 11/12** | TD-JEPA 随数据量增加性能持续提升 |

### 补充图表

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_SzXDuBN8M1/figures/025_Table_5.jpg]]
*Table 5: Architectural (top) and training (bottom) hyperparameters*

## 方法谱系与知识库定位

### 1. 核心瓶颈与设计动机

现有无监督零样本强化学习（RL）的潜在预测方法存在一个根本性瓶颈：它们局限于单任务学习、一步预测或依赖在线策略数据，无法同时处理多步、多策略和离线数据。具体而言：

- **BYOL⋆**（Grill et al., 2020）和 **BYOL-γ⋆**（Lawson et al., 2025）仅建模行为策略诱导的单步潜在动力学，缺乏对多步累积效应和策略条件的显式建模。
- **FB**（Touati & Ollivier, 2021）采用对比损失学习前向-后向表示，但使用单一编码器同时承担状态和任务表示的角色，且其对比机制在大规模离线场景下计算开销较高。
- **HILP**（Park et al., 2024）基于Hilbert范数，同样未显式分离状态与任务编码器。

TD-JEPA的核心洞察在于：通过时序差分（TD）学习策略条件的多步潜在预测，预测器可以直接作为后继特征（successor features）的近似，从而使零样本RL可以在潜在空间中通过简单的回归和最大化内积实现。

### 2. 方法谱系中的关键设计变化

TD-JEPA相对于上述基线方法做出了五项关键设计变化，这些变化构成了其性能优势的因果机制：

| 设计维度 | 基线方法 | TD-JEPA | 证据锚点 |
|---------|---------|---------|---------|
| 预测步长 | 单步预测（BYOL⋆） | 多步时序差分预测 | Section 3.1：潜在预测损失可建模多步和策略依赖动力学 |
| 策略条件 | 非条件或仅依赖行为策略（BYOL⋆） | 以策略参数 $z$ 为条件（policy-conditioned） | Section 3.1：训练策略依赖预测器 $T_\phi$ 以捕获 $\pi_z$ 的长期动力学 |
| 编码器分离 | 单一表示同时作为状态和任务编码器（FB） | 显式分离状态编码器 $\phi$ 和任务编码器 $\psi$ | Section 3.2：引入非对称变体，训练独立的 $\psi$ 作为任务编码器 |
| 数据需求 | 需要在线策略数据或蒙特卡洛采样 | 仅需离线一步转移数据 | Section 3.1：TD-JEPA损失仅需单步转移和策略动作采样，可从离线非策略数据集估计 |
| 训练目标 | 对比损失（FB）或一步潜在预测损失 | 基于TD的非对比潜在预测损失 | Section 5：FB采用对比损失，而TD-JEPA本质上是非对比的 |

其中，**策略条件的多步TD预测**和**编码器分离**是最关键的两项变化。策略条件使预测器 $T_\phi(\phi(s), a, z)$ 能够逼近特定策略 $\pi_z$ 的后继特征 $F_\psi^{\pi_z}$，而非仅建模行为策略的动力学。编码器分离则允许状态编码器 $\phi$ 和任务编码器 $\psi$ 分别优化，前者服务于策略执行和预测，后者定义奖励函数空间。

### 3. 理论基础的继承与拓展

TD-JEPA的理论根基可追溯至后继测度（successor measure）框架。其核心参数化形式为：

$$M^{\pi_z} \approx \phi T_z \psi^{\mathsf{T}}$$

这一分解将策略条件的后继测度表示为共享状态表示 $\phi$、$\psi$ 和任务特定矩阵 $T_z$ 的双线性形式。论文在Section 4中证明了TD-JEPA的梯度与后继测度逼近的非潜在预测TD损失梯度完全匹配（Theorem 3），这意味着TD-JEPA在潜在空间中的学习等价于在后继测度空间中的学习，但避免了显式建模高维状态转移矩阵。

与 **ICVF⋆**（Ghosh et al., 2023）的意图条件值函数不同，TD-JEPA不直接学习值函数，而是通过学习潜在空间中的后继特征，使得零样本策略优化退化为简单的内积最大化：$\pi_z(\phi(s)) = \arg\max_a T_\phi(\phi(s), a, z)^{\top} z$。

### 4. 适用边界与局限

尽管TD-JEPA在多个基准上表现优异，其适用性仍受以下边界约束：

1. **表示坍缩的脆弱性**：TD-JEPA依赖正交正则化 $\widehat{\mathcal{L}}_{\text{REG}}$ 防止表示坍缩，正则化系数需仔细调节（Algorithm 1）。这与 **RLDP**（Jajoo et al., 2025）的观察一致，后者同样强调正交正则化对避免坍缩至关重要。

2. **离线偏差敏感性**：在离线学习场景下，TD-JEPA可能受行为策略偏差影响，需额外行为克隆正则化（Section 5相关讨论）。这与离线RL领域的普遍挑战一致，但论文未提供与保守离线RL方法（如CQL）的系统比较。

3. **线性奖励空间限制**：TD-JEPA仅支持任务编码器 $\psi$ 定义的线性奖励函数空间，即 $Q_r^\pi(s, a) = F_\psi^\pi(s, a)^{\top} z_r$。对于高度非线性的奖励结构，该假设可能约束表示的表达能力。

4. **大规模真实数据验证缺失**：论文在ExoRL和OGBench的13个数据集上进行了评估，覆盖65个任务，但尚未在大型真实机器人数据集上充分验证。

### 5. 开放问题

论文识别了以下尚未解决的开放问题：

- **非对称后继测度的学习目标**：当前理论假设状态分布均匀和转移对称，如何设计兼容非对称后继测度且适合实际优化的学习目标仍待探索。
- **大规模真实机器人基准**：在大型真实机器人数据集上基准测试潜在预测零样本目标，以验证方法的实际可扩展性。
- **理论假设的松弛**：移除理论中对状态分布均匀和转移对称的假设后，性能如何变化？这关系到方法在更一般MDP中的适用性。
- **与保守离线RL的结合**：将TD-JEPA与更保守的离线RL方法（如CQL）结合，以缓解离线偏差的潜力尚未被探索。

### 6. 消融实验揭示的因果证据

消融实验为TD-JEPA的设计选择提供了因果支持：

- **策略条件 vs. 行为策略建模**：Figure 3（左）显示TD-JEPA在平均归一化性能上优于BYOL⋆和BYOL-γ⋆，直接验证了直接建模策略后继测度优于仅建模行为策略动力学的假设。
- **编码器分离 vs. 单一编码器**：Figure 3（右）显示非对称变体（分离 $\phi$ 和 $\psi$）在更多领域上优于对称变体，尽管计算速度较慢（Table 3和D.7）。
- **显式编码器的必要性**：Figure 5（左）显示有显式编码器的基线方法在归一化性能上一致优于无显式编码器的变体，验证了显式状态编码器对零样本RL的关键作用。
- **表示冻结的样本效率**：Figure 4显示冻结预训练表示通常足以实现快速适应，表明TD-JEPA学习的表示具有足够的表达力，无需在微调时大幅更新。

### 7. 与其他方法的对比定位

| 方法 | 核心机制 | 编码器设计 | 损失类型 | 数据需求 |
|------|---------|-----------|---------|---------|
| **Laplacian**（Wu et al., 2019） | 拉普拉斯特征分解 | 单一 | 谱分解 | 在线 |
| **FB**（Touati & Ollivier, 2021） | 前向-后向表示 | 单一 | 对比 | 离线 |
| **HILP**（Park et al., 2024） | Hilbert范数 | 单一 | 范数最小化 | 离线 |
| **ICVF⋆**（Ghosh et al., 2023） | 意图条件值函数 | 单一 | TD | 离线 |
| **BYOL⋆**（Grill et al., 2020） | 一步潜在预测 | 单一 | 预测MSE | 在线 |
| **BYOL-γ⋆**（Lawson et al., 2025） | 折扣一步潜在预测 | 单一 | 预测MSE | 在线 |
| **RLDP**（Jajoo et al., 2025） | 潜在动态预测 | 单一 | 预测MSE | 在线 |
| **TD-JEPA** | 策略条件多步TD潜在预测 | 分离 $\phi$/$\psi$ | TD预测MSE | 离线 |

TD-JEPA是首个将潜在预测TD学习与多策略后继测度逼近建立理论联系的方法（Section 4），其非对比本质使其在大规模离线场景下具有潜在的计算优势，但正交正则化的调参敏感性和线性奖励空间的限制仍是实际部署中需要关注的边界条件。

## 原文 PDF

![[paperPDFs/ICLR_2026/TD_JEPA_Latent_predictive_Representations_for_Zero_Shot_Reinforcement_Learning.pdf]]
