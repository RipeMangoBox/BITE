---
title: "ASE: Large-Scale Reusable Adversarial Skill Embeddings for Physically Simulated Characters"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/ASE_Large_Scale_Reusable_Adversarial_Skill_Embeddings_for_Physically_Simulated_Characters.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/ASE/
aliases:
- ASEA
- ASE
tags:
- SIGGRAPH_2022
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "将对抗模仿学习（匹配状态转移分布）与无监督技能发现（最大化技能与行为互信息）相结合的预训练目标，以及分层控制架构（低层技能策略 + 高层任务策略），使得低层策略能学习到可组合、可指导且多样化的运动技能表示。"
primary_logic: "通过结合对抗模仿和互信息最大化，可以在无结构的大规模运动数据集中预训练出一个既能捕获数据分布、又具有内部多样性和可解释性的技能嵌入空间；该嵌入空间可直接作为高层策略的动作空间，使角色在无额外运动数据的情况下完成新任务，并保持自然运动风格。"
claims:
- "ASE 模型在五个下游任务（Reach, Speed, Steering, Location, Strike）上取得了具有竞争力的归一化回报，并表现出更自然的运动，而从头训练的策略则依赖非自然行为获得高分。"
- "技能发现目标是学习有效技能表示的关键，消融掉后下游任务性能急剧下降（No SD)。"
- "预训练的低层策略能从随机跌倒状态中稳健恢复，平均恢复时间为 0.31 秒，最大 4.1 秒，且数据集不包含起身动作。"
- "ASE 产生的技能间转移覆盖了约 10% 的所有可能转移，远高于移除技能发现和多样性目标后的模型，说明技能组合能力更强。"
---

# ASE: Large-Scale Reusable Adversarial Skill Embeddings for Physically Simulated Characters

> [!tip] 核心洞察
> 通过结合对抗模仿和互信息最大化，可以在无结构的大规模运动数据集中预训练出一个既能捕获数据分布、又具有内部多样性和可解释性的技能嵌入空间；该嵌入空间可直接作为高层策略的动作空间，使角色在无额外运动数据的情况下完成新任务，并保持自然运动风格。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ASE：大规模可复用对抗技能嵌入用于物理模拟角色 |
| 英文题名 | ASE: Large-Scale Reusable Adversarial Skill Embeddings for Physically Simulated Characters |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://arxiv.org/abs/2205.01906); [Project](https://research.nvidia.com/labs/toronto-ai/ASE/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | Adversarial Skill Embeddings (ASE) |
| Dataset | Reach, Speed, Steering, Location |

> [!tip] 效果简介
> - Reach 上，Normalized Return 为 0.75±0.01，对比 0.72±0.01 (Scratch)，变化 +0.03 (ASE 更高，且运动自然)。
> - Speed 上，Normalized Return 为 0.93±0.01，对比 0.95±0.01 (Scratch)，变化 -0.02 (Scratch 略高，但利用非自然行为)。
> - Steering 上，Normalized Return 为 0.90±0.01，对比 0.91±0.01 (Scratch)，变化 -0.01 (Scratch 略高，但利用非自然行为)。

## 概述

物理模拟角色的运动控制面临一个根本性瓶颈：**为每个新任务从零开始训练控制策略**，导致样本效率低下、任务复杂度受限，且运动风格难以自动保持自然。现有方法或依赖单一任务的运动跟踪，或使用对抗运动先验（AMP）指导风格，但均**无法复用已学得的运动技能**，缺乏结构化的技能表示空间。

本文提出 **ASE（Adversarial Skill Embeddings）**，核心思路是将**对抗模仿学习**（匹配状态转移分布）与**无监督技能发现**（最大化技能与行为互信息）相结合，在大规模无结构运动数据集上进行预训练，构建一个**可组合、可指导且多样化的技能嵌入空间**。该嵌入空间直接作为高层策略的动作空间，使角色在无额外运动数据的情况下完成新任务，并保持自然运动风格。

**决定性证据**表明：
- ASE 在五个下游任务（Reach、Speed、Steering、Location、Strike）上取得了具有竞争力的归一化回报，且运动自然度显著优于从头训练的策略（Table 1）。
- 技能发现目标是学习有效技能表示的关键，消融后下游任务性能急剧下降（Figure 11）。
- 预训练的低层策略能从随机跌倒状态中稳健恢复，平均恢复时间 0.31 秒，最大 4.1 秒，而数据集中不包含起身动作（Figure 14）。
- ASE 的技能间转移覆盖了约 10% 的所有可能转移，远高于移除技能发现和多样性目标后的模型，验证了技能组合能力（Figure 9）。

方法上，ASE 采用**分层控制架构**：低层技能策略 $\pi(a|s,z)$ 根据状态和技能潜变量 $z$ 输出关节动作；高层任务策略 $\omega(z|s,g)$ 根据任务目标 $g$ 选择潜变量来指导低层策略。预训练目标为：

$$\max_{\pi} -D_{\mathrm{JS}}\left(d^{\pi}(\mathbf{s},\mathbf{s}') \| d^{M}(\mathbf{s},\mathbf{s}')\right) + \beta I\left(\mathbf{s},\mathbf{s}'; \mathbf{z} \mid \pi\right)$$

即同时最大化对数据集中状态转移的模仿，以及技能 $z$ 与状态转移之间的互信息。技能空间定义为单位超球面 $Z=\{z:\|z\|=1\}$，采用 von Mises-Fisher 分布编码器进行互信息的变分下界近似，并引入 WGAN-GP 梯度惩罚以增强对抗训练的稳定性。

**主要局限**包括：基于 GAN 的预训练存在模式崩塌风险；部分生成运动存在高频抖动；恢复动作的逼真度有限；训练需要约十年仿真经验，样本效率有待提升。**开放问题**指向采用扩散模型等替代分布匹配方法、提升恢复策略自然度、以及扩展到更复杂的多步组合任务。

## 背景与动机

### 问题背景：物理角色动画的技能获取瓶颈

在计算机图形学与机器人学中，使物理模拟角色能够自然、高效地完成复杂运动任务是一个长期挑战。传统方法通常为每个新任务从头训练一个控制策略（Scratch），这一范式面临两个根本性困境：

1. **样本效率低下**：每个任务都需要在物理仿真器中积累大量交互经验，而仿真器本身的计算成本高昂。ASE 的预训练阶段即消耗了相当于约十年仿真时间的经验量，若每个下游任务均从头训练，计算开销将难以承受。
2. **运动质量与任务回报的冲突**：从头训练的策略倾向于利用仿真环境的物理漏洞或非自然行为来最大化任务回报，例如通过高频抖动、异常姿态或“作弊”步态获得更高分数，而非学习符合生物力学约束的自然运动。实验表明，Scratch 策略在 Speed 和 Steering 任务上取得了略高于 ASE 的归一化回报（分别为 0.95 vs. 0.93 和 0.91 vs. 0.90），但这些高回报是以牺牲运动自然度为代价的（Table 1）。

### 现有方法的缺口：缺乏可复用的运动技能表示

在 ASE 提出之前，物理角色动画领域已发展出两大类方法，但均未能解决技能复用问题：

**运动模仿方法**（如 Peng et al., 2021 的 AMP）通过对抗判别器使策略产生的运动分布逼近参考运动数据集，能够生成自然风格的运动。然而，这类方法通常为单一任务设计，学习到的策略是“扁平”的——直接输出关节力矩，不产生可解耦、可组合的技能表示。当任务目标改变时，整个策略需要重新训练，无法将已习得的运动技能迁移到新场景。

**无监督技能发现方法**（如 DIAYN、VALOR 等）通过最大化技能潜变量与行为之间的互信息，使智能体自发地发现多样化的行为模式。但这些方法主要在低维状态空间中验证，产生的行为虽然多样，却往往缺乏自然运动的结构约束，难以直接应用于高自由度的人形角色动画。

这两条技术路线之间存在一个明确的缺口：**如何在保留运动自然度的同时，构建一个结构化的、可复用的技能嵌入空间**，使得高层任务策略可以像选择“动作基元”一样调用低层技能，而无需为每个新任务重新学习运动控制。

### 本文动机：大规模预训练 + 技能嵌入迁移

本文的核心动机是填补上述缺口，提出一种两阶段框架：

1. **预训练阶段**：在大规模、无结构（无需分割或标注）的运动捕捉数据集上，结合对抗模仿学习与无监督技能发现，训练一个低层策略 $\pi(a|s,z)$。该策略以技能潜变量 $z$ 为条件，学习将不同的 $z$ 映射到既接近真实运动分布、又彼此可区分的多样化行为上。
2. **迁移阶段**：冻结预训练的低层策略，在其上训练一个任务特定的高层策略 $\omega(z|s,g)$。高层策略的动作空间直接是低层策略的技能嵌入空间，它通过选择适当的 $z$ 来引导低层策略完成下游任务，从而在无需额外运动数据的情况下保持运动自然度。

这一设计使得运动技能成为可复用资产：一次预训练，多次迁移。角色在完成 Reach、Speed、Steering、Location、Strike 等不同任务时，均能保持与数据集一致的自然运动风格，同时取得具有竞争力的任务回报。

## 核心创新

ASE 的核心创新在于将**对抗模仿学习**与**无监督技能发现**融合为一个统一的预训练目标，从而在大规模无结构运动数据集上构建一个可复用、可组合且多样化的技能嵌入空间。该空间直接作为下游任务中高层策略的动作空间，使角色无需额外运动数据即可完成新任务并保持自然运动风格。

### 创新一：对抗模仿与互信息最大化的统一预训练范式

传统方法（如 **AMP**，Peng et al., 2021）仅使用对抗判别器引导运动风格，缺乏对技能空间的显式结构化和可复用性设计。ASE 将预训练目标形式化为两项的联合最大化（Equation 2）：

$$
\max_{\pi} -D_{\mathrm{JS}}\left(d^{\pi}(\mathbf{s},\mathbf{s}') \| d^{M}(\mathbf{s},\mathbf{s}')\right) + \beta I\left(\mathbf{s},\mathbf{s}'; \mathbf{z} \mid \pi\right)
$$

- **第一项**：通过 GAN 框架最小化策略产生的状态转移分布 $d^{\pi}(\mathbf{s},\mathbf{s}')$ 与运动数据集分布 $d^{M}(\mathbf{s},\mathbf{s}')$ 之间的 JS 散度，使低层策略模仿数据中的运动模式。
- **第二项**：最大化技能潜变量 $\mathbf{z}$ 与状态转移 $(\mathbf{s},\mathbf{s}')$ 之间的互信息 $I(\mathbf{s},\mathbf{s}'; \mathbf{z}|\pi)$，迫使不同 $\mathbf{z}$ 产生可区分的、多样化的行为。

这一设计的因果机制在于：对抗模仿提供了运动自然性的约束，而互信息最大化则为技能空间注入了结构——每个 $\mathbf{z}$ 必须对应独特且可辨识的运动模式。两者协同作用，使得预训练的低层策略既能覆盖数据集的运动分布，又能形成内部多样化的技能库。

**消融实验的因果验证**（Figure 11, Table 1）：
- 移除技能发现目标（No SD）后，下游任务性能急剧下降，说明互信息最大化是学习有效技能嵌入的关键。
- 同时移除技能发现和多样性目标（No SD + No Div）会导致模式崩塌，策略几乎只产生单一行为（Figure 10）。
- 与从头训练（Scratch）的策略相比，ASE 在 Location（+0.04）和 Strike（+0.09）等需要技能组合的任务上显著领先；而在 Speed 和 Steering 上 Scratch 略高，但这是通过利用非自然行为（如高频抖动、仿真漏洞）获得的虚假高分。

### 创新二：分层控制架构与技能嵌入的动作空间化

ASE 采用**分层控制架构**（Figure 2）：
- **低层技能策略** $\pi(\mathbf{a}|\mathbf{s},\mathbf{z})$：接收状态 $\mathbf{s}$ 和技能潜变量 $\mathbf{z}$，输出关节动作 $\mathbf{a}$，负责具体的运动执行。
- **高层任务策略** $\omega(\mathbf{z}|\mathbf{s},\mathbf{g})$：接收状态 $\mathbf{s}$ 和任务目标 $\mathbf{g}$，输出技能变量 $\mathbf{z}$，通过选择技能来指导低层策略完成下游任务。

关键设计在于**动作空间的选择**（Figure 12）：高层策略以**非归一化潜在空间** $\tilde{\mathbf{z}}$ 作为动作空间（而非归一化超球面 $\mathcal{Z}$ 或原始关节动作空间 $\mathcal{A}$）。在 $\tilde{\mathbf{z}}$ 空间中，动作分布初始化为原点附近，使得高层策略初始时均匀采样技能，随后通过学习偏移动作分布来聚焦特定技能。实验表明（Figure 12），这一设计使策略能够探索到更结构化、更多样的行为，而直接在 $\mathcal{Z}$ 上采样则需要极大的标准差才能达到类似多样性，且容易导致行为退化。

### 创新三：von Mises-Fisher 编码器与单位超球面技能空间

为配合互信息最大化目标，ASE 将技能空间设计为**单位超球面** $\mathcal{Z} = \{\mathbf{z}: \|\mathbf{z}\| = 1\}$，并采用均匀先验 $p(\mathbf{z})$。技能编码器 $q(\mathbf{z}|\mathbf{s},\mathbf{s}')$ 使用 **von Mises-Fisher 分布**建模，其对数似然 $\log q(\mathbf{z}|\mathbf{s},\mathbf{s}')$ 直接作为变分互信息下界（Equation 8）的核心项：

$$
I(\mathbf{s},\mathbf{s}'; \mathbf{z}|\pi) \geq \max_q \mathcal{H}(\mathbf{z}) + \mathbb{E}_{p(\mathbf{z})} \mathbb{E}_{p(\mathbf{s},\mathbf{s}'|\pi,\mathbf{z})} [\log q(\mathbf{z}|\mathbf{s},\mathbf{s}')]
$$

这一设计的优势在于：超球面空间天然适合表示方向性技能（如移动方向、挥砍角度），且归一化约束避免了潜在空间的无限膨胀，有利于训练的稳定性。

### 创新四：训练稳定性与恢复策略的工程优化

ASE 在对抗训练框架中引入了两项关键工程改进：
- **梯度惩罚**（WGAN-GP, Equation 14）：在判别器损失中加入梯度惩罚项 $w_{\mathrm{gp}} \mathbb{E}[\|\nabla_{\phi} D(\phi)\|^2]$，缓解 GAN 训练的不稳定性。
- **跌倒恢复策略**：以 10% 概率从随机跌倒状态开始 episode，使低层策略学会从异常姿态中恢复。实验显示（Figure 14），策略能在平均 0.31 秒内恢复站立，最大恢复时间 4.1 秒，且数据集不包含起身动作——说明技能嵌入空间具备一定的泛化和鲁棒性。

### 创新五：预训练判别器作为可迁移的运动先验

在下游任务中，ASE 复用预训练阶段训练好的判别器 $D(\mathbf{s},\mathbf{s}')$ 作为**运动风格先验**，将其输出 $-\log(1 - D(\mathbf{s}_t, \mathbf{s}_{t+1}))$ 作为高层策略的辅助奖励项（Section 7.2）：

$$
r_t = w_G r^G(s_t, a_t, s_{t+1}, g) - w_S \log(1 - D(s_t, s_{t+1}))
$$

这一设计使得高层策略在优化任务目标的同时，持续受到运动自然性的约束，无需在下游任务中重新学习运动风格。消融实验表明（Section 10.6），复用判别器可以改善下游任务中的运动质量。

### 创新边界与局限

尽管 ASE 在技能可复用性和运动自然性上取得了显著进展，但以下局限值得关注：
- **GAN 框架的模式崩塌风险**：预训练基于 GAN，可能未能覆盖数据集中所有行为模式，部分生成的运动存在微小抖动或力度过大等不自然伪影。
- **样本效率**：低层策略训练需要约十年的仿真经验（NVIDIA Isaac Gym 大规模并行），实际部署受计算资源限制。
- **恢复动作逼真度**：由于数据集不包含起身动作，恢复策略虽有效但动作的自然度有限。
- **任务复杂度验证不足**：目前仅在单角色、单步任务上验证，尚未扩展到需要长序列技能组合的多步任务或多角色交互场景。

## 整体框架

ASE 框架采用**两阶段设计**：预训练阶段学习可复用的低层技能嵌入，迁移阶段利用该嵌入完成下游任务。整个系统的核心思路是将对抗模仿学习与无监督技能发现统一在一个预训练目标中，从而在无需结构化运动标签的大规模数据上构建一个兼具多样性、可解释性和可组合性的技能空间。

### 两阶段流程

**预训练阶段**：低层策略 $\pi(a|s,z)$ 以技能潜变量 $z$ 为条件，学习将不同的 $z$ 映射到物理上可行的运动行为。训练信号来自两个并行的目标（Figure 2）：

1. **对抗模仿目标**：判别器 $D(s,s')$ 区分来自运动数据集 $d^M(s,s')$ 的状态转移与策略生成的状态转移 $d^\pi(s,s')$，为策略提供模仿奖励。该目标使低层策略的行为分布逼近真实运动数据的分布。
2. **技能发现目标**：编码器 $q(z|s,s')$ 从产生的状态转移中反向推断所使用的技能 $z$，通过最大化 $z$ 与 $(s,s')$ 之间的互信息 $I(s,s';z|\pi)$，迫使不同技能产生可区分的不同行为。

两个目标通过统一的代理奖励函数 $r_t = -\log(1 - D(s_t,s_{t+1})) + \beta \log q(z_t|s_t,s_{t+1})$ 融合为单一强化学习信号，使用 PPO 进行策略优化。

**迁移阶段**：预训练完成后，低层策略 $\pi(a|s,z)$ 被冻结。针对每个下游任务，训练一个高层策略 $\omega(z|s,g)$，其动作空间即为低层策略的技能潜变量 $z$。高层策略根据当前状态 $s$ 和任务目标 $g$ 选择适当的技能 $z$，低层策略负责将其转化为具体的物理动作。这种分层架构使得任务学习与运动控制解耦——高层策略只需关注“做什么”，而“怎么做”由预训练的低层技能负责。

### 模块关系与数据流

系统的核心模块及其交互关系如下：

| 模块 | 输入 | 输出 | 功能 |
|------|------|------|------|
| 低层策略 $\pi(a\|s,z)$ | 角色状态 $s$，技能潜变量 $z$ | 关节动作 $a$ | 将抽象技能转化为物理运动 |
| 高层策略 $\omega(z\|s,g)$ | 状态 $s$，任务目标 $g$ | 技能潜变量 $z$ | 根据任务需求选择技能 |
| 判别器 $D(s,s')$ | 状态转移 $(s,s')$ | 判别分数 $\in [0,1]$ | 区分真实运动与生成运动 |
| 技能编码器 $q(z\|s,s')$ | 状态转移 $(s,s')$ | 技能后验分布 | 从行为推断所用技能 |
| 价值函数 (Critic) | 状态 $s$ | 价值估计 | PPO 的优势估计与 TD($\lambda$) 更新 |

预训练阶段的数据流为：从先验分布 $p(z)$ 采样技能 $z$ → 低层策略产生轨迹 → 判别器评估运动逼真度 → 编码器推断技能 → 两者构成奖励信号 → PPO 更新策略、判别器和编码器。

迁移阶段的数据流为：环境提供状态 $s$ 和任务目标 $g$ → 高层策略输出 $z$ → 低层策略输出动作 $a$ → 仿真器更新状态 → 任务奖励（可选地结合预训练判别器提供的风格奖励）反馈给高层策略进行更新。

### 关键设计选择

**技能空间结构**：技能潜变量 $z$ 被约束在单位超球面 $\mathcal{Z} = \{z: \|z\| = 1\}$ 上，采用均匀先验分布。编码器 $q$ 使用 von Mises-Fisher 分布建模后验，这种归一化设计有助于稳定训练并避免潜空间中的模式崩塌。

**对抗训练稳定性**：判别器训练中加入了 WGAN-GP 风格的梯度惩罚项 $\mathbb{E}_{d^M}[\|\nabla_\phi D(\phi)\|^2]$（Eq. 14），以增强训练稳定性，减轻 GAN 框架中常见的模式崩塌风险。

**多样性正则化**：在代理目标中额外加入了一个显式多样性项（Eq. 15），惩罚潜空间中距离相近的技能产生相似行为的倾向，进一步促进技能空间的覆盖和行为的差异化。

**恢复策略**：为增强鲁棒性，预训练中有 10% 的 episode 从随机跌倒状态开始，使低层策略学会从异常姿态中恢复。值得注意的是，运动数据集中并不包含起身动作，该能力完全由 RL 自主发现（Figure 14）。

### 与现有方法的区别

与 **AMP**（Peng et al., 2021）相比，ASE 的关键区别在于：AMP 仅使用对抗判别器提供运动风格先验，但没有显式的技能发现机制，其策略是扁平的、任务特定的；而 ASE 通过互信息最大化构建了结构化的技能嵌入空间，使低层策略成为一个通用的、可复用的运动生成器，能够被不同任务的高层策略灵活调用。消融实验表明，移除技能发现目标（No SD）会导致下游任务性能急剧下降（Figure 11），验证了该组件在构建有效技能表示中的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2205_01906/figures/005_Figure_4.jpg]]
*Figure 4: Our framework is used to learn skill embeddings for a 37 degrees-offreedom humanoid character, equipped with a sword and shield*

## 核心模块与公式推导

### 两阶段框架总览

ASE 框架分为**预训练**与**迁移**两个阶段（Figure 2）。预训练阶段，低层策略 $\pi(\mathbf{a}|\mathbf{s},\mathbf{z})$ 学习将潜变量 $\mathbf{z}$ 映射为模仿数据集中运动的物理行为；迁移阶段，高层策略 $\omega(\mathbf{z}|\mathbf{s},\mathbf{g})$ 根据任务目标 $\mathbf{g}$ 选择潜变量，指导低层策略完成下游任务。这一分层架构的核心优势在于：低层策略预训练完成后冻结，高层策略只需在技能嵌入空间中进行搜索，无需从头学习运动控制。

### 预训练核心目标

预训练的总目标（Equation 2）将对抗模仿学习与无监督技能发现统一为：

$$\max_{\pi} -D_{\mathrm{JS}}\left(d^{\pi}(\mathbf{s},\mathbf{s}') \| d^{M}(\mathbf{s},\mathbf{s}')\right) + \beta I\left(\mathbf{s},\mathbf{s}';\mathbf{z} \mid \pi\right)$$

其中：
- $d^{\pi}(\mathbf{s},\mathbf{s}')$ 表示策略产生的状态转移分布，$d^{M}(\mathbf{s},\mathbf{s}')$ 表示运动数据集的状态转移分布；
- $D_{\mathrm{JS}}$ 为 Jensen-Shannon 散度，用于度量两个分布的距离；
- $I(\mathbf{s},\mathbf{s}';\mathbf{z}|\pi)$ 为状态转移与技能潜变量 $\mathbf{z}$ 之间的互信息；
- $\beta$ 为平衡两项的权重系数。

第一项驱策策略产生与数据集统计特征一致的运动，第二项驱策策略为不同 $\mathbf{z}$ 产生可区分的独特行为。

### 对抗模仿模块

对抗模仿通过一个判别器 $D(\mathbf{s},\mathbf{s}')$ 实现（Section 5.1），其损失函数为：

$$\min_{D} -\mathbb{E}_{d^{M}(\mathbf{s},\mathbf{s}')}\left[\log\left(D\left(\mathbf{s},\mathbf{s}'\right)\right)\right] - \mathbb{E}_{d^{\pi}(\mathbf{s},\mathbf{s}')}\left[\log\left(1-D\left(\mathbf{s},\mathbf{s}'\right)\right)\right] + w_{\mathrm{gp}} \mathbb{E}_{d^{M}(\mathbf{s},\mathbf{s}')}[\|\nabla_{\phi} D(\phi)|_{\phi=(\mathbf{s},\mathbf{s}')}\|^2]$$

判别器接收状态转移对 $(\mathbf{s}_t,\mathbf{s}_{t+1})$ 作为输入，输出该转移来自真实数据的概率。前两项为标准 GAN 损失，第三项为 WGAN-GP 梯度惩罚项（Equation 14），用于增强训练稳定性。判别器与技能编码器共享网络主体，仅输出层分离（Figure 5）。

### 技能发现模块

技能发现目标最大化互信息 $I(\mathbf{s},\mathbf{s}';\mathbf{z}|\pi)$。为避免直接估计高维状态熵，利用互信息的对称性 $I(\mathbf{s},\mathbf{s}';\mathbf{z}|\pi) = I(\mathbf{z};\mathbf{s},\mathbf{s}'|\pi)$，将其分解为：

$$I(\mathbf{s},\mathbf{s}';\mathbf{z}|\pi) = \mathcal{H}(\mathbf{z}) - \mathcal{H}(\mathbf{z}|\mathbf{s},\mathbf{s}',\pi)$$

其中 $\mathcal{H}(\mathbf{z})$ 为技能先验分布的熵，在均匀先验下为常数；$\mathcal{H}(\mathbf{z}|\mathbf{s},\mathbf{s}',\pi)$ 为给定状态转移后技能的条件熵。最小化条件熵等价于使技能可从行为中预测，这正是技能可区分性的核心。

引入一个编码器 $q(\mathbf{z}|\mathbf{s},\mathbf{s}')$ 来近似后验分布，得到变分下界（Equation 8）：

$$I(\mathbf{s},\mathbf{s}';\mathbf{z}|\pi) \geq \max_q \mathcal{H}(\mathbf{z}) + \mathbb{E}_{p(\mathbf{z})} \mathbb{E}_{p(\mathbf{s},\mathbf{s}'|\pi,\mathbf{z})} [\log q(\mathbf{z}|\mathbf{s},\mathbf{s}')]$$

编码器 $q$ 从状态转移 $(\mathbf{s}_t,\mathbf{s}_{t+1})$ 推断产生该转移的技能 $\mathbf{z}$。最大化 $\log q(\mathbf{z}|\mathbf{s},\mathbf{s}')$ 鼓励策略为每个 $\mathbf{z}$ 产生独特且可识别的行为模式。

### 代理目标与逐步奖励

将上述目标转化为可优化的代理损失（Equation 9），策略在每条轨迹 $\tau$ 上的期望回报为：

$$\arg\max_{\pi} \mathbb{E}_{p(\mathbf{z})} \mathbb{E}_{p(\tau|\pi,\mathbf{z})} \left[ \sum_{t=0}^{T-1} \gamma^t \left( -\log(1-D(\mathbf{s}_t,\mathbf{s}_{t+1})) + \beta \log q(\mathbf{z}_t|\mathbf{s}_t,\mathbf{s}_{t+1}) \right) \right]$$

由此，低层策略的逐步奖励为（Equation 10）：

$$r_t = -{\log\left({1 - D({\bf s}_t, {\bf s}_{t+1})}\right)} + \beta \log q\left( {{\bf z}_t}|{\bf s}_t, {\bf s}_{t+1} \right)$$

- 第一项为对抗模仿奖励：判别器越认为转移来自真实数据，$D(\mathbf{s}_t,\mathbf{s}_{t+1})$ 越接近 1，$-\log(1-D)$ 越大，鼓励策略产生逼真的运动；
- 第二项为技能发现奖励：编码器对技能 $\mathbf{z}_t$ 的对数似然越高，说明该转移越能体现 $\mathbf{z}_t$ 的特征，鼓励行为的可区分性。

### 多样性正则化

为抑制模式崩塌并鼓励技能多样性，引入额外的多样性正则项（Equation 15），惩罚技能间行为分布过于相似的情况：

$$- w_{\mathrm{div}} \mathbb{E}_{d^{\pi}(\mathbf{s})} \mathbb{E}_{\mathbf{z}_1,\mathbf{z}_2 \sim p(\mathbf{z})} \left[ \left( \frac{D_{\mathrm{KL}}(\pi(\cdot|\mathbf{s},\mathbf{z}_1), \pi(\cdot|\mathbf{s},\mathbf{z}_2))}{D_{\mathbf{z}}(\mathbf{z}_1,\mathbf{z}_2)} - 1 \right)^2 \right]$$

其中 $D_{\mathrm{KL}}$ 为两个技能下动作分布的 KL 散度，$D_{\mathbf{z}}$ 为技能潜变量间的距离。该项鼓励 KL 散度与潜变量距离成比例，使得相近的 $\mathbf{z}$ 产生相似行为、远离的 $\mathbf{z}$ 产生差异行为，从而在嵌入空间中形成平滑的行为流形。消融实验（Figure 9, Figure 10）证实，移除该目标（No Div）会显著降低行为多样性，同时移除技能发现和多样性目标（No SD + No Div）则导致严重的模式崩塌。

### 技能嵌入空间设计

技能潜变量 $\mathbf{z}$ 位于单位超球面 $\mathcal{Z} = \{\mathbf{z}: \|\mathbf{z}\| = 1\}$ 上（Section 6.1），先验分布为均匀的 von Mises-Fisher 分布。编码器 $q$ 的输出同样被归一化到球面上。选择球面空间的原因在于：其紧致性避免了无界空间中潜变量发散的问题，且均匀先验自然鼓励技能均匀覆盖空间。

在迁移阶段，高层策略并不直接在 $\mathcal{Z}$ 上输出，而是使用非归一化的潜空间 $\tilde{\mathbf{z}}$ 作为动作空间（Figure 3），通过将动作分布初始化为原点附近，使高层策略能够均匀地从 $\mathcal{Z}$ 上采样技能。Figure 12 的根轨迹对比表明，使用非归一化空间作为高层动作空间能探索到更有结构、更多样的行为。

### 高层策略的迁移奖励

下游任务中，高层策略 $\omega(\mathbf{z}|\mathbf{s},\mathbf{g})$ 的奖励结合任务奖励与运动先验（Section 7.2）：

$$r_t = w_G r^G(\mathbf{s}_t, \mathbf{a}_t, \mathbf{s}_{t+1}, \mathbf{g}) - w_S \log(1 - D(\mathbf{s}_t, \mathbf{s}_{t+1}))$$

- $r^G$ 为任务特定奖励（如到达目标位置、击打目标等），权重为 $w_G$；
- 第二项复用预训练的判别器 $D$ 作为运动风格先验，权重为 $w_S$，惩罚非自然的运动。消融实验（Section 10.6）表明复用判别器能改善下游任务中的运动质量。

### 训练与恢复策略

低层策略使用 PPO 算法进行训练（Section 6.6），价值函数（critic）用于优势估计和 TD($\lambda$) 更新。为增强策略的鲁棒性，训练时以 10% 概率从随机跌倒状态开始 episode（Section 6.5），使策略学会从异常姿态中恢复。Figure 14 显示，预训练后的低层策略能在平均 0.31 秒内从跌倒中恢复，最大恢复时间 4.1 秒，尽管数据集中不包含起身动作。

## 实验与分析

### 核心实验设置

实验基于一个具有 37 个自由度的 3D 人形角色，在 NVIDIA Isaac Gym 物理仿真环境中进行。预训练阶段使用包含约 10 年仿真经验的大规模并行仿真。运动数据集由多个无结构、无标注的动作捕捉片段组成，涵盖行走、跑步、转向、跳跃等多种运动模式，但不包含起身动作。低层策略的潜在技能变量 $\mathbf{z}$ 定义在 16 维单位超球面上，服从均匀先验分布 $p(\mathbf{z})$。预训练完成后，低层策略参数冻结，高层任务策略根据具体任务目标 $g$ 选择技能潜变量 $\mathbf{z}$。

### 下游任务性能

Table 1 报告了 ASE 与各基线模型在五个下游任务上的归一化回报（0 为最低，1 为最高，每个模型 4096 个 episode，3 个不同随机种子取平均）。ASE 在 Reach（0.75±0.01）、Location（0.45±0.01）和 Strike（0.82±0.01）上取得了具有竞争力的归一化回报，且运动表现自然。在 Speed 和 Steering 任务上，从头训练的策略（Scratch）分别以 0.95±0.01 和 0.91±0.01 略高于 ASE 的 0.93±0.01 和 0.90±0.01，但这一优势是通过利用非自然行为获得的——Scratch 策略倾向于采用不稳定的姿态或仿真漏洞来最大化任务回报，而非产生逼真的人类运动。因此，纯回报数值的比较存在不公平性，ASE 的有效性应从运动质量和任务成功率的综合角度评判。

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2205_01906/figures/012_Table_1.jpg]]
*Table 1: Performance of the diferent skill models when applied to various tasks. Performance is recorded as the normalized return, with 0 being the minimum possible return per episode, and 1 being the maximum. The returns are averaged across 3 models using diferent pre-trained low-level policies, with 4096 episodes per model. The policies trained from scratch achieve higher returns on most tasks by utilizing unnatural behaviors*

### 消融实验

**技能发现目标的关键作用**：Figure 11 的学习曲线显示，移除技能发现目标（No SD）后，下游任务性能急剧下降。这一结果直接验证了互信息最大化目标对学习有效技能嵌入的核心作用——没有该目标，低层策略无法形成可区分的结构化技能空间，高层策略便失去了有意义的动作空间。

**多样性目标的必要性**：移除多样性目标（No Div）后，技能之间的转移覆盖显著减少。Figure 9 展示了不同模型下运动片段间的转移概率矩阵：ASE 产生的技能间转移覆盖了约 10% 的所有可能转移，而 No Div 模型的转移密度明显降低。同时移除技能发现和多样性目标（No SD + No Div）导致严重的模式崩塌，策略几乎只产生单一行为（Figure 10），技能空间完全失效。

**潜在空间结构的影响**：Figure 12 比较了不同高层动作空间下随机探索产生的根轨迹。使用原始动作空间 $\mathcal{A}$ 无法产生语义上有意义的行为，角色通常在几步后跌倒。使用归一化潜在空间 $\mathcal{Z}$ 需要更大的动作分布标准差才能产生类似的多样性。而使用非归一化潜在空间 $\tilde{\mathbf{z}}$ 作为高层动作空间，能够探索到更有结构、更多样的行为，验证了空间设计对技能可组合性的重要影响。

### 鲁棒性与恢复能力

尽管训练数据集中不包含任何起身动作，预训练的低层策略展现出了从随机跌倒状态中稳健恢复的能力。Figure 14 的统计显示，在 500 次随机扰动测试中，平均恢复时间为 0.31 秒，最大恢复时间为 4.1 秒，且所有测试均成功恢复。这一涌现行为得益于预训练期间 10% 概率从随机跌倒状态开始 episode 的训练策略，以及技能发现目标迫使策略探索状态空间边界的机制。

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2205_01906/figures/007_Figure.jpg]]
*Figure: (a) Location (c) Reach (b) Strike (d) Speed (e) Steering: Walking Sideways (f) Steering: Walking Backwards*

### 运动先验的复用效果

预训练判别器 $D$ 可以直接作为运动风格先验复用于下游任务。高层策略的总奖励函数结合了任务奖励和由判别器提供的风格奖励 $-\log(1 - D(\mathbf{s}_t, \mathbf{s}_{t+1}))$。实验表明，复用该先验可以改善下游任务中的运动质量，使生成的运动保持与数据集一致的风格特征。

### 失败模式与局限性

尽管 ASE 整体表现优异，实验中仍观察到若干失败模式：

1. **GAN 模式崩塌风险**：基于 GAN 的预训练框架存在模式崩塌倾向，可能导致技能嵌入未能覆盖数据集中所有行为模式。No SD + No Div 消融实验中观察到的单一行为即是极端案例。

2. **运动伪影**：部分生成的运动呈现微小的抖动或过大的力度，影响运动自然度。这源于对抗模仿学习在匹配状态转移分布时的固有偏差。

3. **恢复动作的逼真度有限**：虽然策略能从跌倒中恢复，但由于数据集中不包含起身动作，恢复动作的逼真度仍有限，与真实人类起身动作存在差异。

4. **样本效率**：低层策略预训练需要约十年仿真经验，样本效率仍有较大提升空间。这一计算需求在实际部署时需重点考虑。

5. **任务复杂度限制**：目前未在需要更复杂技能组合的任务或多角色交互场景中进行验证，ASE 在这些场景下的扩展性有待进一步探索。

### 关键超参数

低层策略训练的关键超参数见 Table 2，高层策略训练的超参数见 Table 3。其中，技能发现权重 $\beta$ 和多样性权重 $w_{\text{div}}$ 是平衡模仿质量与技能多样性的核心调节旋钮。梯度惩罚系数 $w_{\text{gp}}$ 对 GAN 训练的稳定性有重要影响。

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2205_01906/figures/016_Table_2.jpg]]
*Table 2: ASE hyperparameters for training low-level policy*

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2205_01906/figures/017_Table_3.jpg]]
*Table 3: ASE hyperparameters for training high-level policy*

### 补充图表

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2205_01906/figures/010_Figure_10.jpg]]
*Figure 10: Frequencies at which the low-level policy produces motions that match individual clips in the dataset. Results are shown for the 50 most frequently matched motion clips. ASE produces diverse behaviors that more evenly covers the dataset. Without the skill discovery objective (No SD) and the diversity objective (No Div.), the policy produces less diverse behaviors and is more prone to collapsing to a single behavior*

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2205_01906/figures/013_Figure_12.jpg]]
*Figure 12: Trajectories of the character’s root produced by random exploration with diferent action spaces for the high-level policy. Random exploration in the original action space A does not produce semantically meaningful behaviors, and tends to cause the character to fall a er a few timesteps. Our method of using the unnormalized latent space $\tilde { z }$ as the action space allows the policy to explore more structured and diverse behaviors. Using the normalized latent space Z can lead to less diverse behaviors, and a much larger standard deviation is needed for the action distribution to produce similar diversity*

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2205_01906/figures/011_Figure_11.jpg]]
*Figure 11: Learning curves comparing performance on downstream tasks using diferent low-level policies. We compare ASE to policies that are trained from scratch for each tasks (Scratch), as well as to low-level policies trained without the skill discovery objective (No SD), without the diversity objective (No Div.), and with both objectives disabled (No SD + No Div.). The skill discovery objective is crucial for learning efective skill representations. The policies trained from scratch o en achieve higher returns by exploiting unnatural behaviors (see Figure 8)*

## 方法谱系与知识库定位

### 1. 方法定位与谱系

ASE 位于**对抗运动先验**（Adversarial Motion Priors）与**无监督技能发现**两条技术路线的交汇点。其直接前身是 **AMP**（Peng et al., SIGGRAPH 2021），后者首次将 GAN 风格的判别器引入物理角色控制，使策略能从运动数据中学习自然运动风格，但 AMP 本质上是单任务或单风格的模仿学习，无法产生可组合、可复用的技能表示。ASE 在 AMP 的基础上引入了两个关键扩展：

1. **技能潜变量 $z$ 与互信息最大化**：借鉴无监督技能发现文献（如 DIAYN、VALOR 等）中“最大化技能与行为互信息”的思想，ASE 在预训练阶段要求低层策略 $\pi(a|s,z)$ 产生的状态转移 $(s,s')$ 能够被编码器 $q(z|s,s')$ 解码回原来的 $z$。这使得不同的 $z$ 对应可区分的运动模式，从而在模仿数据分布的同时获得内部结构化。

2. **分层控制架构**：将预训练的低层策略 $\pi(a|s,z)$ 作为可复用的运动引擎，高层任务策略 $\omega(z|s,g)$ 直接在技能嵌入空间上操作，而非原始动作空间。这一设计使得下游任务训练只需学习“何时使用哪个技能”，而无需从零开始探索动作空间。

从更广的谱系来看，ASE 属于**预训练-迁移**范式在物理角色控制领域的应用。与视觉领域的 ImageNet 预训练或 NLP 中的语言模型预训练类似，ASE 试图从大规模无结构运动数据中提取可迁移的运动知识。其核心创新在于将**分布匹配**（对抗模仿）与**表示学习**（互信息最大化）统一在同一个预训练目标中，使得学到的嵌入既忠实于数据分布，又具有可解释的内部结构。

### 2. 与基线方法的对比

论文设置了三个主要消融基线和一个从头训练基线：

- **Scratch**：为每个下游任务从零开始训练扁平策略，无预训练。在 Speed 和 Steering 任务上，Scratch 的归一化回报略高于 ASE（分别为 0.95 vs 0.93 和 0.91 vs 0.90），但这是通过利用非自然行为（如高频抖动、过度用力）获得的，运动质量显著劣于 ASE。在需要更复杂技能组合的 Location 和 Strike 任务上，ASE 显著优于 Scratch（0.45 vs 0.41 和 0.82 vs 0.73），说明预训练技能嵌入在复杂任务上的优势更为突出。

- **No SD（移除技能发现目标）**：消融掉互信息最大化项后，下游任务性能急剧下降（Figure 11），技能间转移覆盖大幅减少（Figure 9），说明单纯的对抗模仿不足以产生可区分的技能表示。这是 ASE 最关键的消融实验，直接验证了技能发现目标的必要性。

- **No Div（移除多样性目标）**：移除基于 KL 散度的多样性正则化后，行为多样性降低，技能间连接变稀疏。同时移除 SD 和 Div 的模型出现严重的模式崩塌，策略几乎只产生单一行为（Figure 10）。

- **AMP**（Peng et al., 2021）：作为直接前身，AMP 使用对抗判别器指导运动风格，但无显式技能潜变量和互信息目标，因此无法产生结构化的技能空间，也无法直接迁移到新任务。

### 3. 适用边界

ASE 的有效性建立在以下前提之上：

- **大规模无结构运动数据**：预训练需要覆盖丰富运动模式的数据集。论文使用了包含行走、跑步、转向、挥剑等多种动作的数据集，但数据集中不包含起身动作，导致恢复策略的逼真度受限。

- **分层任务结构**：ASE 假设下游任务可以通过“高层决策选技能、低层策略执行技能”的方式解决。对于需要连续精细控制、无法分解为离散技能序列的任务，该架构可能不适用。

- **仿真环境与计算资源**：预训练使用 NVIDIA Isaac Gym 的大规模并行仿真，相当于约十年的仿真经验。在计算资源受限或无法进行大规模并行仿真的场景下，ASE 的训练成本可能过高。

- **角色形态固定**：论文仅在 37-DOF 人形角色上验证，技能嵌入是否可跨形态迁移未作讨论。

### 4. 局限与开放问题

**已确认的局限**：

1. **GAN 框架的固有风险**：基于 GAN 的对抗训练存在模式崩塌风险，可能导致技能嵌入未能覆盖数据集中所有行为模式。论文通过多样性正则化部分缓解了这一问题，但未完全解决。

2. **运动伪影**：部分生成的运动会呈现微小抖动或过大力度，影响运动自然度。这可能是判别器对高频细节不敏感，或奖励信号不足以约束精细运动质量所致。

3. **恢复策略的逼真度**：尽管低层策略能从随机跌倒状态稳健恢复（平均 0.31 秒，最大 4.1 秒），但由于数据集中不包含起身动作，恢复动作的逼真度有限，更像是一种“仿真漏洞利用”而非真实的起身技能。

4. **样本效率**：预训练需要大量仿真经验，样本效率仍有显著提升空间。

**开放问题**：

1. **替代分布匹配方法**：能否采用 Flow 模型、扩散模型或对比预测编码等替代 GAN，以减轻模式崩塌并提升技能多样性？这直接关系到技能嵌入的覆盖度和下游任务的鲁棒性。

2. **恢复策略的自然化**：如何通过少量起身动作数据或更智能的课程学习，使恢复行为在保持鲁棒性的同时更接近真实人类的起身方式？

3. **长序列技能组合**：ASE 目前在下游任务中由高层策略逐时间步选择技能 $z$，但未显式建模技能间的长期依赖关系。能否扩展到需要多步技能序列的复杂任务（如“跑-跳-挥剑”）或对抗性交互场景？

4. **跨形态迁移**：技能嵌入是否包含与具体形态无关的运动语义？能否将人形角色上学到的技能嵌入迁移到四足或其他形态角色？

5. **运动质量的形式化度量**：论文主要依赖定性观察和下游任务性能来评估运动质量。如何建立更客观、可量化的运动自然度指标，以更公平地比较 ASE 与 Scratch 等方法？

6. **样本效率的进一步提升**：能否通过离线预训练、元学习或模型-based 方法减少所需的仿真经验，使 ASE 更接近人类“看几次就能学会”的技能获取方式？

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/ASE_Large_Scale_Reusable_Adversarial_Skill_Embeddings_for_Physically_Simulated_Characters.pdf]]
