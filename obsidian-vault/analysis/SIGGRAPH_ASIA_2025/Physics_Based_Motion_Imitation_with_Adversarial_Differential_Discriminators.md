---
title: "Physics-Based Motion Imitation with Adversarial Differential Discriminators"
type: paper
paper_level: A
venue: "SIGGRAPH Asia"
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2025/Physics_Based_Motion_Imitation_with_Adversarial_Differential_Discriminators.pdf
code_link: null
project_link: https://add-moo.github.io/
aliases:
- ADDA
- PBMIADD
tags:
- SIGGRAPH_ASIA_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "引入对抗差分判别器（ADD），将多个目标值组合为差分向量，利用仅以零向量为正样本的判别器，自动学习非线性聚合并动态调整各目标的权重。"
primary_logic: "仅使用零向量作为正样本的对抗判别器，在梯度惩罚正则化下，能够有效引导多目标优化，自动聚焦于更困难的目标，实现动态且非线性的多目标平衡，从而完全替代手工设计的奖励函数。"
claims:
- "在多个运动技能和数据集上，ADD 在位置跟踪误差和自由度速度误差上达到与 DeepMimic 相当甚至更优的性能，且完全无需手工奖励工程。"
- "对于 DeepMimic 失败的复杂运动（如 Double Kong），ADD 成功完成；同时 ADD 在跨随机种子时表现出更好的一致性。"
- "梯度惩罚消融实验证实将梯度惩罚应用于负样本是 ADD 有效训练的关键，而 WGAN-GP 惩罚效果较差。"
- "Humanoid - Double Kong 上 Position Tracking Error [m] = 0.030 ± 0.001"
---

# Physics-Based Motion Imitation with Adversarial Differential Discriminators

> [!tip] 核心洞察
> 仅使用零向量作为正样本的对抗判别器，在梯度惩罚正则化下，能够有效引导多目标优化，自动聚焦于更困难的目标，实现动态且非线性的多目标平衡，从而完全替代手工设计的奖励函数。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于对抗差分判别器的物理运动模仿 |
| 英文题名 | Physics-Based Motion Imitation with Adversarial Differential Discriminators |
| 会议/期刊 | SIGGRAPH Asia 2025 |
| Links | [paper](https://arxiv.org/abs/2505.04961) · [Project](https://add-moo.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | Adversarial Differential Discriminator (ADD) |
| Dataset | Humanoid - Double Kong, Humanoid - Dance A (LaFAN1 子集), EVAL 机器人 - Walk, 复合任务 (Run) |

> [!tip] 效果简介
> - Humanoid - Double Kong 上，Position Tracking Error [m] 为 0.030 ± 0.001，对比 失败 (DeepMimic 无法完成该技能)，变化 成功 vs 失败。
> - Humanoid - Dance A (LaFAN1 子集) 上，DoF Velocity Tracking Error [rad/s] 为 0.428 ± 0.014，对比 较高 (DeepMimic 表现出明显抖动)，变化 更低（更平滑）。
> - EVAL 机器人 - Walk 上，Position Tracking Error [m] 为 0.036 ± 0.002，对比 与 DeepMimic 相当，变化 相当。

## 概要

物理仿真角色的运动模仿是计算机图形学与机器人学中的长期挑战。现有方法，如 **DeepMimic**（Peng et al., SIGGRAPH 2018），依赖手工设计的多目标奖励函数——将姿态误差、关节速度误差、末端效应器误差等子项通过固定权重线性组合。这种手工奖励工程不仅需要大量领域知识与反复调参，且固定的线性加权无法捕捉目标间复杂的非线性关系，导致方法难以泛化到多样化的运动技能。

本文提出 **对抗差分判别器（Adversarial Differential Discriminator, ADD）**，一种新颖的对抗式多目标优化技术，从根本上替代手工奖励设计。其核心思想是：将多个目标值组合为差分向量 $\Delta$，并训练一个仅以零向量 $\mathbf{0}$ 为正样本的判别器 $D(\Delta)$，通过对抗训练自动学习目标的非线性聚合，动态调整各子目标的相对权重。在梯度惩罚正则化下，该判别器能够有效引导多目标优化，自动聚焦于更困难的目标，实现动态且非线性的多目标平衡。

在多个运动技能和机器人形态上的实验表明：
- ADD 在仿人角色（28 DoF）和 EVAL 机器人（26 DoF）上，位置跟踪误差与自由度速度误差均达到与 DeepMimic 相当甚至更优的性能（Table 1, Table 2），且**完全无需手工奖励工程**。
- 对于 DeepMimic 失败的复杂运动（如 Double Kong），ADD 成功完成（Table 1）。
- 在复合任务（运动模仿 + 转向目标）中，ADD 在位置跟踪误差（0.029 vs 0.048）和目标速度误差（0.803 vs 0.882）上均优于 DeepMimic（Table 3）。
- 消融实验证实，将梯度惩罚施加于负样本是 ADD 有效训练的关键机制（Figure 9）。

ADD 为物理运动模仿提供了一条摆脱手工奖励工程的可行路径，同时为更广泛的多目标优化问题提供了新的对抗式聚合范式。



### 物理运动模仿的核心挑战

在计算机图形学与机器人学中，使物理模拟角色精确复现参考运动（如跑酷、舞蹈）是一项长期挑战。其核心在于为强化学习策略设计能够衡量模仿质量的奖励函数。传统方法依赖于手工定义多个子奖励项（如姿态误差、关节速度误差、末端效应器位置误差等），并通过线性加权求和来聚合这些目标。这一范式以 **DeepMimic**（Peng et al., SIGGRAPH 2018）为代表，其总奖励形式为：

$$r_{t}^{\mathrm{DM}} = w^{p} r_{t}^{p} + w^{jv} r_{t}^{jv} + w^{rv} r_{t}^{rv} + w^{e} r_{t}^{e} + w^{c} r_{t}^{c}$$

其中各权重 $w^{i}$ 需要针对不同运动技能进行繁琐的手工调参。

### 现有方法的瓶颈

手工奖励工程存在三个根本性局限：

1. **泛化能力弱**：一组固定的权重难以适配从简单行走到高动态空翻的多样化运动技能。例如，DeepMimic 在 Double Kong（双金刚跳）这类复杂跑酷动作上完全失败，角色只能原地踏步而无法跳过障碍物（Table 1）。

2. **线性聚合的固有缺陷**：线性加权求和无法捕捉多个目标之间的非线性关系。当 Pareto 前沿非凸时，线性标量化理论上无法到达某些最优解，导致策略学习陷入次优平衡。

3. **人工成本高昂**：每引入一个新技能或新机器人形态，都需要领域专家重新设计奖励项并反复调整权重。在 LaFAN1 数据集（超过一小时的运动技能）上，这种手工调参的代价尤为突出。

另一方面，**AMP**（Peng et al., SIGGRAPH 2021）通过对抗模仿学习绕过了手工奖励设计，但其目标是分布层面的风格匹配，而非帧级别的精确运动跟踪，因此无法满足需要精确复现运动细节的任务需求。

### 本文动机

针对上述瓶颈，本文提出了一种全新的对抗多目标优化方法——**对抗差分判别器（Adversarial Differential Discriminator, ADD）**。其核心动机在于：

- **自动学习非线性聚合**：利用对抗训练框架，让判别器自动学习多个目标值之间的非线性组合关系，完全替代手工权重设计。
- **动态权重调整**：判别器在训练过程中能够根据当前策略的弱点，动态地将优化压力聚焦于更难满足的目标，实现自适应的多目标平衡。
- **保持精确跟踪能力**：通过将帧级别运动差异构造为差分向量输入判别器，ADD 在消除手工奖励的同时，仍能实现与 DeepMimic 相当甚至更优的精确运动跟踪性能。



## 核心方法与创新机理

ADD 的核心创新在于将运动模仿中的多目标奖励设计问题重新建模为一种**对抗差分判别**任务，从根本上消除了对手工奖励函数工程的依赖。其关键突破体现在以下三个层面。

### 1. 差分向量的非线性聚合替代手工加权求和

传统运动模仿方法（如 **DeepMimic**，Peng et al., SIGGRAPH 2018）依赖手工设计的加权奖励函数，将姿态误差、关节速度误差、根速度误差、末端效应器误差和接触误差等多项子目标线性组合为单一标量奖励（Eq. 11）。这种线性加权方式存在两个根本性局限：其一，权重系数需要大量领域知识和反复调参，难以泛化到多样化的运动技能；其二，固定的线性组合无法捕捉各目标之间复杂的非线性关系。

ADD 将这一范式彻底翻转。它不再直接聚合子目标值，而是将各子目标的当前值组装为一个**差分向量** $\Delta$，然后训练一个判别器 $D(\Delta)$ 来判断该向量是否对应理想解（即零误差状态）。判别器的训练目标为：

$$\max_D \quad \log(D(\mathbf{0})) + \log(1 - D(\Delta))$$

其中**仅以零向量作为正样本**，所有来自策略的实际差分向量均为负样本。这一设计使得判别器自动学习各目标之间的非线性聚合关系，动态调整对不同目标的关注程度——当某个目标误差较大时，判别器自然会对其施加更大的“惩罚”，从而引导优化过程自动聚焦于更困难的目标。策略从判别器获得的奖励为 $r_t = -\log(1 - D(\Delta_t))$，完全取代了手工设计的奖励函数。

### 2. 负样本梯度惩罚：稳定训练的关键机制

对抗训练中判别器的稳定性是核心挑战。ADD 引入了一种**专门施加于负样本的梯度惩罚**机制：

$$\mathcal{L}^{GP}(D) = \left\| \nabla_{\phi} D(\phi) \big|_{\phi = \Delta} \right\|_2^2$$

与 WGAN-GP 中将梯度惩罚施加于正负样本之间插值的做法不同，ADD 将梯度惩罚**仅施加于负样本 $\Delta$ 上**。消融实验（Figure 9, Section 8）提供了决定性证据：去除梯度惩罚或将其施加于正样本均会导致跟踪性能显著下降，而将 WGAN-GP 的插值惩罚方式应用于 ADD 同样效果不佳。这一发现表明，在“仅零向量为正样本”的设定下，约束判别器在负样本区域的梯度范数是防止其退化为 delta 函数、维持有效训练信号的关键。

### 3. 任务目标的统一集成

在复合任务场景中，传统方法通常需要在模仿奖励之外独立添加任务奖励（如转向速度目标），这进一步加剧了手工调参的负担。ADD 通过将任务目标直接**追加到差分向量 $\Delta$ 中**，实现了模仿目标与任务目标的统一建模。判别器自动学习如何在保持运动质量的同时满足任务需求，无需额外的权重平衡。在复合任务（Run + 转向）实验中（Table 3），ADD 在位置跟踪误差和速度跟踪误差上均优于 DeepMimic（位置误差 0.029 vs 0.048，速度误差 0.803 vs 0.882），验证了这一统一框架的有效性。

### 方法谱系与知识库定位

ADD 处于**对抗模仿学习**与**多目标优化**的交叉点。与 **AMP**（Peng et al., SIGGRAPH 2021）的分布匹配范式不同，ADD 保留了帧级别的精确跟踪能力；与 DeepMimic 的手工奖励工程范式不同，ADD 实现了奖励函数的完全自动化学习。其核心贡献在于证明了：在适当的正则化（负样本梯度惩罚）下，仅以零向量为正样本的对抗判别器能够有效引导复杂的多目标物理运动模仿任务，为物理角色动画的奖励设计提供了一种全新的、无需手工调参的解决方案。



ADD 方法的核心思想是将运动模仿重新表述为一个对抗式多目标优化问题，从而完全替代手工设计的加权奖励函数。其整体 pipeline 由五个关键模块串联构成，形成“状态观测 → 差分构建 → 判别评分 → 策略决策 → 价值估计”的闭环。

### 模块关系与数据流

**观测映射 φ(·)** 是整个系统的感知入口。它从物理模拟器的当前状态 $s$ 与参考运动帧 $\hat{s}$ 中提取运动学特征，包括根位姿、各关节相对于根的位置、关节速度、以及以 6D 正切表示编码的关节旋转量。这些特征构成了后续差分计算的基础。

**差分向量 Δ 构建** 将观测映射的输出转化为判别器的输入。具体而言，模块计算帧级别的差异 $\Delta = \phi(\hat{s}) \ominus \phi(s)$，将参考运动与模拟角色之间的多维度偏差压缩为一个统一的差分向量。这个向量的每个分量对应一个隐式的优化目标（如关节位置偏差、速度偏差等），但无需显式命名或手动加权。

**判别器 D(Δ)** 是方法的核心创新。它接收差分向量 Δ 作为输入，输出一个标量分数，表示当前状态与理想解（零误差）的接近程度。判别器的训练目标为：

$$\max_D \; \log(D(\mathbf{0})) + \mathbb{E}_{p(\mathbf{s}|\pi)}\left[\log(1 - D(\Delta))\right] - \lambda^{GP} \mathcal{L}^{GP}(D)$$

其中仅以零向量 $\mathbf{0}$ 作为正样本，所有由策略产生的 Δ 作为负样本。梯度惩罚项 $\mathcal{L}^{GP}(D)$ 专门施加于负样本 Δ 上，计算判别器输出相对于差分向量的梯度二范数：

$$\mathcal{L}^{GP}(D) = \big\| \nabla_{\phi} D(\phi) \big|_{\phi=\Delta} \big\|_2^2$$

这一设计是 ADD 有效训练的关键——消融实验证实，将梯度惩罚施加于负样本（而非正样本或 WGAN-GP 式的插值）能够防止判别器退化为平凡的 delta 函数，同时引导优化过程动态聚焦于当前更困难的目标。

**策略 π(a|s)** 采用高斯策略，输出目标关节旋转量（球关节使用 3D 指数映射，旋转关节使用标量角度），通过 PD 控制器驱动模拟角色。策略从判别器获得的奖励由下式计算：

$$r_t = -\log(1 - D(\Delta_t))$$

该奖励信号完全由判别器自动生成，无需任何手工设计的子奖励项。策略训练使用 PPO 算法。

**价值函数 V(s)** 与策略网络架构相似，用于估计期望回报，为 PPO 的 Actor-Critic 框架提供基线。策略与价值网络均使用固定对角协方差矩阵 $\Sigma = \text{diag}(\sigma_1, \sigma_2, ...)$，其中各标准差为手动指定的超参数。

### 与传统方法的对比

与 DeepMimic（Peng et al., SIGGRAPH 2018）的手工加权奖励形成鲜明对比，后者的总奖励为多个子项的线性组合：

$$r_t^{\text{DM}} = w^p r_t^p + w^{jv} r_t^{jv} + w^{rv} r_t^{rv} + w^e r_t^e + w^c r_t^c$$

其中各权重 $w^i$ 需要针对不同运动技能反复手动调参。ADD 通过对抗判别器自动学习这些目标之间的非线性聚合关系，从根源上消除了奖励工程的需求。与 AMP（Peng et al., SIGGRAPH 2021）的分布匹配方式不同，ADD 通过差分向量的帧级别判别实现了精确的运动跟踪，而非仅模仿整体风格分布。

### 任务目标的集成

对于需要同时完成运动模仿和附加任务（如转向目标）的复合场景，ADD 无需在模仿奖励外独立添加任务奖励。只需将任务目标值直接追加到差分向量 Δ 中，判别器即可自动学习模仿质量与任务完成度之间的平衡。这一设计保持了框架的统一性，避免了引入新的超参数。

### 补充图表

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2505_04961/figures/023_Figure_14.jpg]]
*Figure 14: Learning curves comparing the tracking performance of simulated humanoid characters trained via AMP [Peng et al. 2021], DeepMimic [Peng et al. 2018], and our method ADD. Statistics are computed over 5 training runs initialized with different random seeds, except for the LaFAN1 subset (1 run due to computational cost). ADD is capable of learning highly agile and acrobatic skills, achieving comparable tracking performance and sample efficiency to DeepMimic, without requiring manual reward engineering. Moreover, ADD exhibits better consistency across seeds, whereas DeepMimic often converges to suboptimal behaviors in some seeds*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2505_04961/figures/013_Figure_8.jpg]]
*Figure 8: Learning curves comparing ADD to the manually tuned reward function from Rudin et al. [2022] on training a Go1 quadruped to move. Results are shown across 5 random seeds per method. While ADD performs slightly worse in following linear velocity commands, it achieves lower roll and pitch angular velocities–indicating a more stable robot base–and lower DoF accelerations, which means smoother control over time*



### 问题形式化：从线性加权到对抗差分判别

传统多目标优化（MOO）将多个损失函数通过手工权重组合为标量目标：

$$
\operatorname*{min}_{\theta} \sum_{i} w^{i} l^{i}(\theta) \tag{Eq. 2}
$$

该形式依赖人工指定各目标相对重要性的先验知识，且线性聚合无法捕捉目标间复杂的非线性关系。本文的核心洞察是：**将多目标值组合为差分向量，通过对抗判别器自动学习非线性聚合函数**。

### ADD 对抗目标

设差分向量 $\Delta = (l^{1}(\theta), \dots, l^{n}(\theta))$ 由各子目标值拼接而成。判别器 $D(\Delta)$ 的目标是区分理想解（$\Delta = \mathbf{0}$，即所有目标完美达成）与当前解（$\Delta \neq \mathbf{0}$）：

$$
\operatorname*{min}_{\theta} \operatorname*{max}_{D} \quad \log(D(\mathbf{0})) + \log(1 - D(\Delta)) \tag{Eq. 3}
$$

仅以零向量作为正样本，使判别器学习从差分向量的模式中推断解的质量，从而隐式地实现多目标的非线性聚合。

### 梯度惩罚正则化

为防止判别器退化为仅在 $\Delta = \mathbf{0}$ 处输出高值的 delta 函数，引入梯度惩罚项：

$$
\mathcal{L}^{GP}(D) = \big\| \nabla_{\phi} D(\phi) \big|_{\phi = \Delta} \big\|_{2}^{2} \tag{Eq. 5}
$$

完整目标为：

$$
\operatorname*{min}_{\theta} \operatorname*{max}_{D} \quad \log(D(\mathbf{0})) + \log(1 - D(\boldsymbol{\Delta})) - \lambda^{GP} \mathcal{L}^{GP}(D) \tag{Eq. 4}
$$

**关键设计**：梯度惩罚施加于负样本 $\Delta$（即当前策略产生的差分向量），而非正样本或插值样本。消融实验证实这是 ADD 有效训练的核心要素——去除梯度惩罚或使用 WGAN-GP 式惩罚均导致跟踪性能显著下降（Figure 9, Section 8）。

### 运动模仿中的 ADD 实例化

将 ADD 应用于物理运动模仿时，需将强化学习框架与判别器目标对接。

#### 观测映射与差分向量构建

从状态 $\mathbf{s}$ 与参考运动 $\hat{\mathbf{s}}$ 中提取运动学特征 $\phi(\cdot)$（包括根位姿、关节位置/速度/旋转等），计算帧级别差分：

$$
\Delta = \phi(\hat{\mathbf{s}}) \ominus \phi(\mathbf{s})
$$

作为判别器输入（Section 5.1, Algorithm 1）。

#### 判别器目标

在策略 $\pi$ 诱导的状态分布下，判别器最大化目标为：

$$
\operatorname*{max}_{D} \quad \log(D(\mathbf{0})) + \mathbb{E}_{p(\mathbf{s} \mid \pi)} \left[ \log(1 - D(\Delta)) \right] - \lambda^{GP} \mathcal{L}^{GP}(D) \tag{Eq. 8}
$$

#### 策略奖励

策略从判别器获得的逐帧奖励为：

$$
r_{t} = -\log(1 - D(\Delta_{t})) \tag{Eq. 10}
$$

该奖励替代了 DeepMimic 中手工设计的加权组合（Eq. 11），后者需为姿态、关节速度、根速度、末端效应器、接触等子项分别设定权重 $w^{p}, w^{jv}, w^{rv}, w^{e}, w^{c}$。

#### 策略优化

策略 $\pi(\mathbf{a}_{t} \mid \mathbf{s}_{t}) = \mathcal{N}(\mu(s_{t}), \Sigma)$ 输出高斯动作分布，其中 $\Sigma = \operatorname{diag}(\sigma_{1}, \sigma_{2}, \dots)$ 为固定对角协方差。动作指定目标关节旋转量（球关节用 3D 指数映射，旋转关节用标量角度），通过 PD 控制器驱动物理仿真。策略与价值函数 $V(s)$ 均使用 PPO 进行 Actor-Critic 训练，优化标准期望折扣回报：

$$
J(\pi) = \mathbb{E}_{p(\tau \mid \pi)} \left[ \sum_{t=0}^{T-1} \gamma^{t} r_{t} \right] \tag{Eq. 1}
$$

### 复合任务的扩展

当任务需要同时满足运动模仿与额外目标（如转向速度匹配）时，ADD 将任务目标值直接追加到差分向量 $\Delta$ 中，无需独立设计任务奖励函数（Section 6.5, Appendix B.6）。这使得同一判别器能够自动平衡模仿质量与任务完成度之间的非线性权衡。

### 与基线方法的核心差异

| 模块 | DeepMimic (Peng et al., SIGGRAPH 2018) | ADD (本文) |
|------|----------------------------------------|------------|
| 奖励聚合 | 手工加权和 $r_{t}^{DM} = \sum w^{i} r_{t}^{i}$ | 判别器 $D(\Delta)$ 学习的非线性聚合 |
| 正样本定义 | 无判别器 | 仅 $\Delta = \mathbf{0}$ |
| 梯度惩罚对象 | 不适用 | 负样本 $\Delta$ |
| 任务目标集成 | 独立添加任务奖励项 | 追加至差分向量 $\Delta$ |

### 评估指标

位置跟踪误差衡量模拟角色与参考运动之间根相对关节位置的差异：

$$
e_{t}^{\mathrm{pos}} = \frac{1}{N^{\mathrm{joint}} + 1} \Bigg( \sum_{j \in \mathrm{joints}} \Big\| (\hat{\mathbf{x}}_{t}^{j} - \hat{\mathbf{x}}_{t}^{\mathrm{root}}) - (\mathbf{x}_{t}^{j} - \mathbf{x}_{t}^{\mathrm{root}}) \Big\|_{2} \Bigg) \tag{Eq. 12}
$$

自由度速度跟踪误差则衡量关节角速度的匹配程度，二者共同构成运动模仿质量的核心度量（Table 1, Table 2）。



## 实验与关键发现

### 核心实验设置

为验证 ADD 的有效性，作者在两类形态上进行了系统评估：28 自由度仿人角色和 26 自由度 Sony EVAL 机器人。实验覆盖了从简单行走、舞蹈到高难度跑酷动作（如 Double Kong）的多种运动技能，数据集包括 Peng et al.（SIGGRAPH 2018）的单段运动片段、AMASS 的 DanceDB 子集以及 LaFAN1 子集（超过一小时的移动技能）。所有结果均经过多次随机种子平均（仿人角色 5 次、EVAL 机器人 3 次），并报告了标准差以确保统计可靠性。基线方法 **DeepMimic**（Peng et al., SIGGRAPH 2018）和 **AMP**（Peng et al., SIGGRAPH 2021）均基于原作者公开代码实现并调优，同时禁用姿态终止条件以保证与不进行帧对齐跟踪的 AMP 方法公平对比。

### 主实验结果

ADD 在运动跟踪质量上达到了与手工设计奖励函数相当甚至更优的性能，且完全无需人工奖励工程。

**仿人角色运动跟踪（Table 1）：** 在 Double Kong 这一高难度跑酷动作上，DeepMimic 策略完全失败（角色无法跳过障碍物，仅学会原地跑动），而 ADD 成功完成了该技能，位置跟踪误差仅为 $0.030 \pm 0.001$ m。在 Dance A（LaFAN1 子集）等舞蹈动作上，ADD 的 DoF 速度跟踪误差为 $0.428 \pm 0.014$ rad/s，显著低于 DeepMimic 的明显抖动表现，表明 ADD 生成的策略更加平滑。在大多数技能上，ADD 的位置跟踪误差与 DeepMimic 相当或更优，且跨随机种子表现出更好的一致性。

**EVAL 机器人运动跟踪（Table 2）：** 在 Walk 等任务上，ADD 的位置跟踪误差为 $0.036 \pm 0.002$ m，与 DeepMimic 相当，验证了方法在不同形态上的泛化能力。

**复合任务（Table 3）：** 当运动模仿与目标转向任务结合时，ADD 在 Run 任务上的位置跟踪误差为 $0.029 \pm 0.001$ m（DeepMimic: $0.048 \pm 0.000$ m），目标速度误差为 $0.803 \pm 0.009$ m/s（DeepMimic: $0.882 \pm 0.038$ m/s），在两个维度上均优于 DeepMimic。这得益于 ADD 将任务目标直接追加到差分向量 $\Delta$ 中，使判别器能够自动平衡模仿质量与任务完成度。

**定性结果（Figure 2, Figure 3）：** ADD 训练的仿人角色成功复现了多种跑酷和舞蹈动作，EVAL 机器人也复制了一系列目标运动，视觉质量与手工奖励方法相当。

### 消融实验与机制分析

**梯度惩罚配置（Figure 9）：** 消融实验系统比较了五种梯度惩罚设置：无惩罚（None）、仅正样本（Pos）、仅负样本（Neg）、正负样本均施加（Both）以及 WGAN-GP 惩罚。结果表明，将梯度惩罚施加于负样本（Neg 或 Both 设置）是 ADD 有效训练的关键——去除梯度惩罚或仅施加于正样本会导致跟踪性能显著下降，而 WGAN-GP 惩罚效果较差。这验证了 ADD 的核心设计：梯度惩罚正则化专门作用于负样本 $\Delta$，防止判别器退化为 delta 函数，同时引导优化过程自动聚焦于更困难的目标。

**DeepMimic 敏感性分析（Figure 12）：** 在 LaFAN1 子集上对比了不同参数设置下的 DeepMimic 与 ADD。结果显示 DeepMimic 对奖励权重高度敏感，性能波动显著，而 ADD 无需任何手工调参即可达到稳定且具有竞争力的性能。

### 失败模式与局限性

尽管 ADD 在多数任务上表现优异，但在高度动态的运动（如翻滚）上容易陷入局部最优。例如，角色可能只学会躺下和起身，而非完成完整的翻滚动作。这表明仅依赖零向量正样本的对抗训练在某些复杂运动上可能缺乏足够的探索信号。

此外，对于某些前向移动，ADD 在根位置跟踪方面表现较弱。训练时间方面，ADD 略长于 DeepMimic（例如仿人角色约 9 小时 vs 6.5 小时，LaFAN1 约 10 天 vs 7 天），这主要源于判别器的额外训练开销。

### 鲁棒性测试

在外部随机力扰动测试（Figure 15）中，ADD 训练的运动策略在高达 300 N 的随机外力干扰下仍保持稳定，表明学习到的策略具有良好的鲁棒性。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2505_04961/figures/007_Figure.jpg]]
*Figure: (a) ADD (Ours) (b) Manual Reward*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2505_04961/figures/024_Figure_15.jpg]]
*Figure 15: Robustness of locomotion policies in Sec. 6.5 under random external force perturbations. Policies are trained without perturbations and stress-tested by randomly applying forces up to 300 N during inference. Performance is reported in terms of the episode length until loss of balance, as well as position tracking error and target velocity error before falling. Lighter bars denote nominal performance, and darker bars indicate performance under perturbation. ADD exhibits levels of degradation comparable to DeepMimic, reflecting a similar degree of robustness*

### 补充图表

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2505_04961/figures/033_Figure_16.jpg]]
*Figure 16: Full learning curves for all training objectives on the quadruped task, with results averaged over five training runs initialized with different random seeds. ADD outperforms the manually designed reward function from Rudin et al. [2022] on several metrics associated with torso stability and smooth control. Overall, ADD achieves comparable sample efficiency, final performance, and consistency to the manually-designed reward function*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2505_04961/figures/016_Figure_11.jpg]]
*Figure 11: Magnitudes of the gradients of the discriminator’s output with respect to the prediction error for each sample at different training iterations. As training progresses and ?? (?? ) gradually learns to approximate samples near the origin, the discriminator assigns higher and higher weights to samples farther from the origin, essentially honing in on the more difficult objectives*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2505_04961/figures/004_Table_1.jpg]]
*Table 1: Motion tracking performance of simulated humanoid characters trained using AMP [Peng et al. 2021], DeepMimic [Peng et al. 2018], and our method ADD. Position (Eq. 12) and DoF Velocity tracking errors are averaged ± 1 std across 5 models initialized with random seeds. Due to computational constraints, 1 model is trained for the LaFAN1 subset. For each model, errors are averaged across 4096 test episodes. ADD achieves tracking performance comparable to DeepMimic when imitating individual motion clips and larger motion datasets, while alleviating the need for manual reward engineering*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2505_04961/figures/006_Table_2.jpg]]
*Table 2: Position tracking errors (Eq. 12) of simulated EVAL robots trained using ADD, AMP [Peng et al. 2021], and DeepMimic [Peng et al. 2018]. Only the position tracking errors are reported for brevity, showing the mean ± 1 standard deviation across three random seeds, with 4096 test episodes per seed. The results show that ADD maintains strong tracking performance comparable to DeepMimic on a different character morphology*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2505_04961/figures/008_Table_3.jpg]]
*Table 3: Performance of various methods when applied to a composite task that combines motion imitation with a target steering objective. Motion imitation performance is measured via the position tracking error, while task performance is measured by the velocity error $\left$\| $\mathbf { v } _ { t } - v ^ { * } \mathbf { d } _ { t } ^ { * } \right$\| , where $\mathbf { v } _ { t }$ is the 2D root velocity of the character and $v ^ { * } \mathbf { d } _ { t } ^ { * }$ the 2D target velocity. ADD, via automatically balancing the different objectives, achieved optimal performance on both objectives

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2505_04961/figures/015_Table_4.jpg]]
*Table 4: ADD regression experiment hyperparameters*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2505_04961/figures/017_Table_5.jpg]]
*Table 5: DeepMimic sensitivity analysis parameter settings. Reward weights are listed in the order of $\boldsymbol { w } ^ { p } , \boldsymbol { w } ^ { j v } , \boldsymbol { w } ^ { r v } , \boldsymbol { w } ^ { e }$ , , ???? , and reward scales are listed in the order of $\alpha ^ { p } , \alpha ^ { j v } , \alpha ^ { r v } , \alpha ^ { e } , \alpha ^ { c } . ^ { \star }$ * denotes the final parameter setting used in the experiments

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2505_04961/figures/019_Table_6.jpg]]
*Table 6: ADD humanoid character motion imitation experiment hyperparameters*



## 定位与知识库关联

### 1. 方法谱系：从手工奖励工程到对抗多目标聚合

ADD 的核心贡献在于将运动模仿中的多目标奖励设计问题重新表述为一种对抗多目标优化（Adversarial MOO）范式。其方法谱系可沿两条线索追溯：

**线索一：物理运动模仿中的奖励工程。** 以 **DeepMimic**（Peng et al., SIGGRAPH 2018）为代表的精确运动跟踪方法，依赖手工设计的加权奖励函数，将姿态误差、关节速度误差、根速度误差、末端效应器误差和接触状态等多个子目标线性组合为标量奖励信号（Eq. 11）。这种线性加权方式的根本瓶颈在于：权重需要大量领域知识和反复人工调参才能平衡，且固定的线性组合无法捕捉目标间潜在的非线性权衡关系——当不同目标在优化曲面上呈现非凸 Pareto 前沿时，线性标量化必然丢失可行解。

**线索二：对抗模仿学习中的分布匹配。** **AMP**（Peng et al., SIGGRAPH 2021）引入对抗框架进行运动模仿，但其判别器以状态转移为输入，学习的是运动风格的分布匹配，而非帧级别的精确跟踪。AMP 因此无法保证模拟角色在每一帧都与参考运动对齐，这使其不适用于需要精确时空一致性的任务。

ADD 在这两条线索之间开辟了新路径：它继承了对抗训练的自动学习能力，但将判别器的输入从“状态分布样本”重新设计为“差分向量 $\Delta$”——该向量由多个目标值（在运动模仿中为模拟状态与参考状态在各运动学特征上的差异）拼接而成。判别器的正样本固定为全零向量 $\mathbf{0}$，代表理想解（即所有目标同时达到零误差）。这一设计使 ADD 能够**自动学习各目标的非线性聚合方式**，同时保留了帧级别精确跟踪的能力。如原文所述，“our method enables nonlinear combinations of objectives that can better capture complex relationships among disparate objectives and the potentially non-convex Pareto front.”

### 2. 与基线方法的核心差异

| 维度 | DeepMimic (Peng et al., 2018) | AMP (Peng et al., 2021) | ADD (本文) |
|------|------|------|------|
| 奖励来源 | 手工设计的多项加权和 | 对抗判别器（状态分布匹配） | 对抗差分判别器（目标值聚合） |
| 聚合方式 | 线性加权（固定权重） | 隐式（通过判别器学习分布） | 非线性（通过 $\Delta$ 判别器学习） |
| 跟踪精度 | 帧级别精确跟踪 | 风格级别模仿，无帧对齐 | 帧级别精确跟踪 |
| 权重调参 | 需要大量人工调参 | 无需（但无法精确跟踪） | 无需 |
| 正样本定义 | — | 参考运动的状态转移 | 全零向量 $\mathbf{0}$ |
| 梯度惩罚 | 不适用 | WGAN-GP（插值惩罚） | 专门施加于负样本 $\Delta$ |

ADD 在 DeepMimic 的精确跟踪能力与 AMP 的自动学习能力之间取得了关键平衡：它在 Table 1 和 Table 2 中达到了与 DeepMimic 相当甚至更优的位置跟踪误差，同时在 DeepMimic 失败的复杂运动（如 Double Kong）上成功完成任务。值得注意的是，ADD 在 DoF 速度跟踪误差上表现出一致的优势，表明其学习到的聚合方式倾向于产生更平滑的运动——这可能是非线性聚合自动聚焦于更困难目标（如速度一致性）的结果。

### 3. 技术关键：梯度惩罚施加对象的消融验证

ADD 有效训练的一个关键设计选择是将梯度惩罚**专门施加于负样本 $\Delta$**（Eq. 9），而非正样本或正负样本的插值。Figure 9 的消融实验系统验证了这一点：

- **无梯度惩罚（None）**：判别器迅速退化为 delta 函数，训练崩溃。
- **仅施加于正样本（Pos）**：性能显著下降，表明正样本惩罚无法有效约束判别器在负样本区域的梯度行为。
- **WGAN-GP 式插值惩罚**：效果较差，因为插值点分布在正负样本之间，而 ADD 中正样本为固定点 $\mathbf{0}$，插值惩罚的几何意义与标准 GAN 设置不同。
- **仅施加于负样本（Neg）或同时施加于正负样本（Both）**：两者均能有效训练，但 Neg 设置更简洁且效果稳定。

这一发现揭示了 ADD 判别器训练的独特动力学：由于正样本是固定的零向量，判别器在负样本区域的梯度行为直接决定了其对策略的奖励信号质量。将梯度惩罚集中在负样本上，迫使判别器在策略实际探索的区域内保持平滑，从而提供有意义的梯度引导。

### 4. 适用边界与局限

**已验证的适用场景：**
- 仿人角色（28 DoF）的多种运动技能模仿，包括行走、跑步、舞蹈、空翻、障碍跳跃等（Table 1, Figure 2）。
- EVAL 机器人（26 DoF）的运动跟踪（Table 2, Figure 3）。
- 2D Walker 标准 RL 基准任务（Figure 7）。
- Unitree Go1 四足机器人的移动控制，包括转向指令（Figure 6, Table 3）。
- 复合任务：将运动模仿与转向目标结合，通过将任务目标直接追加到差分向量 $\Delta$ 中实现（Section 6.5, Table 3）。

**已知局限：**

1. **局部最优问题**：ADD 在高度动态的运动（如翻滚）上容易陷入局部最优。如 Section 9 所述，角色可能只学会“躺下和起身”而非完成完整翻滚。这表明当目标空间存在欺骗性的局部最优时，仅依赖判别器的奖励信号可能不足以引导策略穿越困难的探索区域。

2. **根位置跟踪的弱项**：对于某些前向移动技能，ADD 在根位置跟踪方面表现弱于 DeepMimic。这可能是因为差分向量中的各目标维度在判别器的非线性聚合中，根位置误差的相对重要性被自动调低。

3. **训练计算开销**：ADD 的训练时间略长于 DeepMimic（仿人角色约 9h vs 6.5h；LaFAN1 子集约 10 天 vs 7 天），主要来自判别器的额外训练开销。

4. **泛化性待验证**：目前仅评估了有限类型的运动技能和两种机器人形态，在更广泛的任务（如灵巧手操作、多智能体协调）上的适用性尚待系统研究。

### 5. 开放问题

1. **架构融合**：ADD 能否与后续工作的架构创新（如风格混合、多域策略、Transformer 编码器）结合，进一步提升跟踪精度和泛化能力？ADD 的差分向量设计本质上是模块化的，理论上可以与任何状态编码器 $\phi(\cdot)$ 兼容。

2. **跨领域迁移**：ADD 的核心思想——仅以零向量为正样本的对抗多目标聚合——能否扩展到更一般的多目标优化或多任务问题，如计算机视觉中的多损失平衡、自然语言处理中的多任务学习？这需要验证差分向量的构建方式在非运动模仿领域的有效性。

3. **通用控制器**：能否利用 ADD 训练完全不依赖手工设计奖励函数的通用运动控制器？当前 ADD 仍需要参考运动作为输入，但若将差分向量的构建方式泛化到高层任务描述（如“向前移动”），可能实现零手工奖励的通用策略学习。

4. **局部最优缓解**：对于极易陷入局部最优的高动态运动，是否可以引入额外的正则化（如熵奖励、好奇心驱动探索）或课程学习策略来缓解？判别器在局部最优处的梯度行为值得进一步理论分析。



## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2025/Physics_Based_Motion_Imitation_with_Adversarial_Differential_Discriminators.pdf]]
