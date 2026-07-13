---
title: "AdaptNet: Policy Adaptation for Physics-Based Character Control"
type: paper
paper_level: A
venue: TOG
year: 2023
pdf_ref: paperPDFs/TOG_2023/AdaptNet_Policy_Adaptation_for_Physics_Based_Character_Control.pdf
project_link: https://motion-lab.github.io/AdaptNet
code_link: null
aliases:
- AdaptNet
tags:
- TOG_2023
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "在预训练策略的潜在空间添加零初始化的注入模块（Latent Space Injector），并在每个全连接层旁路增加可训练分支（Internal Adaptor），使策略从原始行为出发逐步调整控制输出，平衡了对旧技能的保留与新任务的灵活性。"
primary_logic: "将策略分解为固定的预训练编码器与可训练的适应组件，利用零初始化保证训练起点与原始策略一致，通过编辑潜在空间和内部层残差调整实现快速、稳定的策略迁移，避免了对整个网络的重训练。"
claims:
- "在多种风格迁移、形态变化和地形适应任务中，AdaptNet的目标任务奖励和样本效率均显著优于从零训练（Scratch）、直接微调（FT）、带正则化的微调（FT+Reg）以及渐进网络（PNet），且从零训练在给定预算内几乎无法获得有效控制器。"
- "消融实验表明，组合潜在空间适应（LSA）和内部适应（IA）的完整AdaptNet在模仿误差上取得最优（例如Goose Step 0.13m），而单独使用IA或移除了状态编码器的LSA均导致误差显著增大。"
- "在首个潜在空间Z^0进行注入能产生最平滑、最可重复的脚步轨迹；而在更深的Z^2或所有层注入会导致动作抖动甚至训练失败，证明Z^0是适合操控的瓶颈层。"
- "风格迁移 (Goose Step) 上 Imitation Error (m) = AdaptNet (LSA+IA): 0.13±0.07"
---

# AdaptNet: Policy Adaptation for Physics-Based Character Control

> [!tip] 核心洞察
> 将策略分解为固定的预训练编码器与可训练的适应组件，利用零初始化保证训练起点与原始策略一致，通过编辑潜在空间和内部层残差调整实现快速、稳定的策略迁移，避免了对整个网络的重训练。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AdaptNet：面向物理角色控制的策略自适应 |
| 英文题名 | AdaptNet: Policy Adaptation for Physics-Based Character Control |
| 会议/期刊 | TOG 2023 |
| Links | [paper](https://arxiv.org/abs/2310.00239) · [Project](https://motion-lab.github.io/AdaptNet) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | AdaptNet |
| Dataset | 风格迁移 (Goose Step), 风格迁移 (Joyful Walk), 风格迁移 (Jaunty Skip), 低摩擦地形 (ice floor, running) |

> [!tip] 效果简介
> - 风格迁移 (Goose Step) 上，Imitation Error (m) 为 AdaptNet (LSA+IA): 0.13±0.07，对比 LSA: 0.21±0.12，变化 -38%。
> - 风格迁移 (Joyful Walk) 上，Imitation Error (m) 为 AdaptNet: 0.17±0.07，对比 LSA: 0.26±0.08，变化 -35%。
> - 风格迁移 (Jaunty Skip) 上，Imitation Error (m) 为 AdaptNet: 0.22±0.07，对比 LSA: 0.28±0.08，变化 -21%。

## 概要

在物理仿真角色控制中，将预训练的强化学习策略迁移到新任务面临一个两难困境：**直接微调**容易导致灾难性遗忘与过拟合，而**从零训练**则样本效率低下、耗时过长。AdaptNet 的核心洞察在于，将策略分解为固定的预训练编码器与可训练的适应组件，利用零初始化保证训练起点与原始策略完全一致，从而在保留已有技能的同时实现快速、稳定的策略迁移。

具体而言，AdaptNet 在两个层级上对预训练策略进行编辑：第一层在**潜在空间**中注入由状态编码器（及可选控制编码器）生成的条件偏移量，支持添加新的控制输入和修改任务目标；第二层在策略网络的每个全连接层旁路添加零初始化的**内部适配器**分支，以残差形式实现更精细的控制调整。训练时仅优化新增的少量参数，并施加 L2 正则化以防止策略过快漂移。

在多种风格迁移、形态变化和地形适应任务中，AdaptNet 的目标任务奖励和样本效率均显著优于从零训练、直接微调、带正则化的微调以及渐进网络，且从零训练在给定训练预算（8M 样本）内几乎无法获得有效控制器。消融实验进一步证实，组合潜在空间适应与内部适应的完整方案在模仿误差上取得最优（如 Goose Step 风格迁移误差为 0.13±0.07 m），而单独使用内部适应或移除状态编码器均导致性能显著下降。此外，潜在空间注入的位置对运动质量有决定性影响：仅在首个潜在空间 $Z^0$ 进行注入能产生平滑、可重复的脚步轨迹，而更深层的注入会导致动作抖动甚至训练失败。

在计算机动画与机器人控制领域，基于物理的角色控制长期面临一个核心矛盾：**通用性与专用性难以兼得**。深度强化学习（Deep RL）使得训练能够模仿复杂运动数据并执行目标导向任务的控制器成为可能，但这类控制器通常针对特定的角色形态、运动风格和环境条件进行优化。一旦任务需求发生变化——例如角色需要模仿新的风格化步态、适应不同的身体比例、在低摩擦冰面奔跑，或在障碍物密集的环境中导航——原有策略的性能便会急剧下降。

应对这一问题的传统路径存在明显的效率瓶颈：

- **从零训练（Scratch）**：为每个新任务重新训练一个完整的策略网络，虽然在理论上能够获得针对性的控制器，但其样本效率极低。在典型的训练预算（800万环境样本）下，从零训练的控制器几乎无法获得有效的目标导向控制能力，这使得该路径在实际应用中不可行。
- **直接微调（Fine‑tuning, FT）**：加载预训练权重并在新任务上继续优化，看似高效，实则容易陷入**灾难性遗忘**与**过拟合**的双重陷阱。在学习曲线（Fig. 13）中可以观察到，FT 在风格迁移任务上的目标奖励在训练开始后即出现明显下降，表明网络在适应新风格时迅速丧失了对原始控制目标的保持能力。即使加入 L2 正则化（FT+Reg），性能改善也十分有限。
- **渐进式网络（Progressive Networks, PNet）**（Rusu et al., 2016b）：通过冻结已有网络并添加新模块来保留旧知识，但该方法在推理时需要两倍的参数量，且无法将新旧知识融合为单一的高效控制器。

上述困境揭示了一个更深层的**瓶颈**：如何在高效复用预训练策略知识的前提下，实现对新任务的快速、稳定适应，同时避免对整个网络进行重训练所带来的过拟合与遗忘风险。AdaptNet 正是在这一背景下提出的解决方案。其核心动机并非设计一个更强的单任务控制器，而是构建一种**通用的策略适应框架**，使预训练策略能够以最小的训练代价和最高的样本效率，泛化到风格迁移、形态变化、地形适应和局部避碰等多样化的下游任务中。

## 核心方法与创新机理

AdaptNet 的核心创新在于将策略适应问题从“重新训练整个网络”转变为“在冻结的预训练策略上叠加可训练的编辑模块”，从而在保留既有技能与快速适应新任务之间取得平衡。这一设计直击直接微调（finetuning）容易导致灾难性遗忘、而从零训练（scratch）样本效率低下的瓶颈。

### 关键创新点：两级适应架构

AdaptNet 引入了一个**两级层次结构**：第一级在潜在空间层面进行语义编辑，第二级在策略网络内部进行精细化控制调整。两级组件均采用**零初始化**，确保训练起点与原始策略的行为完全一致，这是避免初始行为偏移的关键设计。

#### 创新点一：潜在空间注入

在预训练状态编码器 $E_\xi$ 的输出上叠加一个可训练的注入器 $I_\phi$，形成修改后的潜在状态：

$$\mathbf{z}_t = \mathcal{E}_\xi(\mathbf{s}_t) + \mathcal{I}_\phi(\mathbf{s}_t, \mathbf{c}_t)$$

注入器 $I_\phi$ 由独立的状态编码器 $E_\phi$、可选的控制编码器 $G_\phi$ 和最终嵌入层 $F_\phi$ 组成，其最后一层全连接层以零权重和零偏置初始化。这一设计使得适应训练开始时，注入器的输出为零，策略行为与原策略完全一致，随后逐步学习偏移量以支持风格迁移、形态变化等任务。与直接修改整个编码器不同，这种加法式编辑保持了原始潜在空间的稳定性，同时允许注入器从额外的控制输入（如风格标签、地形信息）中提取任务相关特征。

#### 创新点二：内部适应

在策略网络的每个全连接层旁路添加零初始化的可训练分支，形成残差结构：

$$\mathbf{z}_t^i = \mathcal{F}_\theta^i(\mathbf{z}_t^{i-1}) + \mathcal{F}_\eta^i(\mathbf{z}_t^{i-1})$$

其中 $\mathcal{F}_\theta^i$ 是冻结的预训练层，$\mathcal{F}_\eta^i$ 是新增的可训练适配器分支。这种设计允许对控制输出进行更精细的调整，支持更大幅度的任务变更（如地形适应、碰撞避免），而不会破坏预训练层已学到的运动基元。

#### 创新点三：正则化训练目标

适应阶段的优化目标在标准策略梯度的基础上，加入了对注入项 $Z_\phi$ 和适配器参数 $\eta$ 的 L2 正则化：

$$\underset{\phi,\eta}{\operatorname{max}} \mathbb{E}_t \left[ \left( \sum_k \omega_k \bar{A}_t^k \right) \log \pi_\theta \big( \mathbf{a}_t \vert \mathcal{E}_\xi(\mathbf{s}_t) + Z_\phi(\mathbf{s}_t, \mathbf{c}_t); \eta \big) - \beta \vert\vert Z_\phi(\mathbf{s}_t, \mathbf{c}_t) \vert\vert_2 - \kappa \vert\vert \eta \vert\vert_2 \right]$$

正则化项抑制了策略的过快漂移，防止适应过程中对预训练知识的过度覆盖，是维持训练稳定性的重要机制。

### 与基线方法的关键差异

| 对比维度 | 直接微调 | 渐进网络 | AdaptNet |
|---------|---------|---------|----------|
| 训练起点 | 加载预训练权重，初始行为可能偏移 | 添加新模块，冻结旧网络 | 零初始化注入器与适配器，行为完全一致 |
| 参数效率 | 更新全部参数 | 参数量翻倍 | 推理时可合并，参数量不变 |
| 旧技能保留 | 易发生灾难性遗忘 | 通过冻结旧模块保留 | 通过冻结编码器与策略头，仅学习残差 |

消融实验证实了组合设计的必要性：单独使用内部适应在风格迁移任务中表现不佳（模仿误差 0.30m），且无法处理需要额外控制输入的地形适应任务；单独使用潜在空间注入虽优于内部适应，但缺少精细化控制能力。完整 AdaptNet（LSA+IA）在 Goose Step 任务上取得 0.13m 的模仿误差，相比仅使用 LSA 的 0.21m 降低了 38%。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2310_00239/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our approach for adapting motor control policies for physics-based characters. Top: We model both pretraining and adapted tasks using a multi-critic reinforcement learning framework that balances the training of imitation and goal-directed control objectives. After a policy is trained, we can quickly adapt it to a new task using AdaptNet. Bottom: AdaptNet starts with a copy of the pre-trained policy network and modifies it through editing the latent space conditioned on the character’s state and introducing optional adaptation modules for further finetuning*

AdaptNet 的整体设计围绕一个核心原则展开：**将预训练策略分解为冻结的基础组件与可训练的适应组件，通过零初始化保证训练起点与原策略行为完全一致，从而在保留旧技能的前提下实现快速、稳定的新任务适应**。图 2 给出了框架的全貌，自上而下包含两个层次。

### 预训练阶段：多评论家强化学习

在适应之前，首先需要获得一个具备基本运动能力的预训练策略。AdaptNet 采用多评论家（multi-critic）强化学习框架进行预训练，同时优化模仿目标与目标导向控制目标：

- **策略网络**：由状态编码器 $\mathcal{E}_\xi$（RNN 结构）将角色状态 $\mathbf{s}_t$ 映射到潜在空间 $\mathbf{z}_t$，再通过若干全连接层 $\mathcal{F}_\theta^i$ 逐步变换，最终由策略头 $\pi_\theta$ 输出动作分布。
- **多评论家结构**：针对不同目标分别训练独立的评论家网络，估计各自的标准化优势 $\bar{A}_t^k$。预训练目标为最大化加权优势之和：
  $$\operatorname*{max}_{\theta,\xi} \mathbb{E}_t \Big[ \Big( \sum_k \omega_k \bar{A}_t^k \Big) \log \pi_\theta \big( \mathbf{a}_t | \mathcal{E}_\xi(\mathbf{s}_t) \big) \Big]$$
- **模仿奖励**：通过判别器集成（discriminator ensemble）提供。多个判别器以 hinge loss 加梯度惩罚进行训练，其输出的裁剪均值作为模仿奖励 $r^{\text{imit}}$。

预训练完成后，编码器 $\mathcal{E}_\xi$、全连接层 $\mathcal{F}_\theta^i$ 和策略头 $\pi_\theta$ 被冻结，作为后续适应的基础骨架。

### 适应阶段：双层适配架构

AdaptNet 在冻结的预训练策略上叠加两个可训练的适应组件，形成双层适配层次：

**第一层：潜在空间注入（Latent Space Injection, LSA）**

这是适应的入口层，直接编辑策略的潜在表示。注入器 $\mathcal{I}_\phi$ 接收角色状态 $\mathbf{s}_t$ 和可选的控制信号 $\mathbf{c}_t$，生成潜在偏移量并与原始编码器输出相加：
$$\mathbf{z}_t = \mathcal{E}_\xi(\mathbf{s}_t) + \mathcal{I}_\phi(\mathbf{s}_t, \mathbf{c}_t)$$

注入器内部结构为：
$$\mathcal{I}_\phi(\mathbf{s}_t, \mathbf{c}_t) = \mathcal{F}_\phi\big( \operatorname{Concat}(\mathcal{E}_\phi(\mathbf{s}_t), \mathcal{G}_\phi(\mathbf{c}_t)) \big)$$

其中 $\mathcal{E}_\phi$ 从 $\mathcal{E}_\xi$ 复制权重初始化，$\mathcal{F}_\phi$ 的最后一层以零权重和零偏置初始化。这一设计确保训练第一步 $\mathcal{I}_\phi$ 输出为零，潜在空间与原策略完全一致。LSA 支持引入额外的控制输入（如目标方向、地形信息），适用于风格迁移、目标导航等需要条件化适应的任务。

**第二层：内部适应（Internal Adaptation, IA）**

在策略网络的每个全连接层旁路添加可训练分支，形成残差结构：
$$\mathbf{z}_t^i = \mathcal{F}_\theta^i(\mathbf{z}_t^{i-1}) + \mathcal{F}_\eta^i(\mathbf{z}_t^{i-1})$$

适配器分支 $\mathcal{F}_\eta^i$ 同样零初始化，参数 $\eta := \{ \Delta\mathbf{W}_i, \Delta\mathbf{b}_i \}$ 在适应训练中优化，而预训练层 $\mathcal{F}_\theta^i$ 保持冻结。IA 负责对控制输出进行更精细的调整，支持形态变化、地形适应等需要实质性行为改变的复杂任务。

### 适应训练目标

适应阶段仅优化注入器参数 $\phi$ 和适配器参数 $\eta$，目标函数在策略梯度的基础上引入两项 L2 正则化：
$$\underset{\phi,\eta}{\operatorname{max}} \mathbb{E}_t \left[ \left( \sum_k \omega_k \bar{A}_t^k \right) \log \pi_\theta \big( \mathbf{a}_t | \mathcal{E}_\xi(\mathbf{s}_t) + Z_\phi(\mathbf{s}_t, \mathbf{c}_t); \eta \big) - \beta || Z_\phi(\mathbf{s}_t, \mathbf{c}_t) ||_2 - \kappa || \eta ||_2 \right]$$

正则化项 $\beta$ 和 $\kappa$ 分别约束注入偏移和适配器参数的增长速度，防止策略过快漂移导致灾难性遗忘。

### 推理时的结构合并

AdaptNet 的一个关键工程优势在于：适应完成后，注入器和适配器分支可以直接合并回原始网络结构。注入偏移与编码器输出相加，适配器分支的权重与偏置叠加到对应全连接层，使得推理时的参数量与原始策略完全相同。相比之下，渐进网络（PNet）需要保留两倍的参数量。

### 运动插值能力

通过引入缩放系数 $\alpha \in [0, 1]$，AdaptNet 天然支持在原始策略与完全适应策略之间连续过渡：
$$\mathbf{z}_t^0 = \mathcal{E}_\xi(\mathbf{s}_t) + \alpha \mathcal{I}_\phi(\mathbf{s}_t, \mathbf{c}_t), \quad \mathbf{z}_t^i = \mathcal{F}_\theta^i(\mathbf{z}_t^{i-1}) + \alpha \mathcal{F}_\eta^i(\mathbf{z}_t^{i-1})$$

当 $\alpha=0$ 时退化为原始策略，$\alpha=1$ 时为完全适应策略。进一步，还可以在两个独立训练的 AdaptNet 模型之间进行参数加权插值，实现不同风格之间的平滑过渡。

AdaptNet 的核心设计思想是将预训练策略分解为**冻结的基座**与**可训练的适应组件**，通过零初始化保证训练起点与原始行为一致，从而在不破坏已有技能的前提下实现快速策略迁移。其架构包含两个关键适应模块。

### 潜在空间注入 (Latent Space Injection)

预训练策略通过状态编码器 $\mathcal{E}_\xi$ 将角色状态 $\mathbf{s}_t$ 映射到潜在空间 $\mathbf{z}_t$，策略头 $\pi_\theta$ 再据此生成动作分布。AdaptNet 在此潜在空间引入一个可训练的**注入器** $\mathcal{I}_\phi$，以残差方式编辑原始潜在表示：

$$\mathbf{z}_t = \mathcal{E}_\xi(\mathbf{s}_t) + \mathcal{I}_\phi(\mathbf{s}_t, \mathbf{c}_t)$$

其中 $\mathbf{c}_t$ 为可选的控制输入（如目标方向、风格标签）。注入器的内部结构为：

$$\mathcal{I}_\phi(\mathbf{s}_t, \mathbf{c}_t) = \mathcal{F}_\phi(\operatorname{Concat}(\mathcal{E}_\phi(\mathbf{s}_t), \mathcal{G}_\phi(\mathbf{c}_t)))$$

注入器由三部分组成：独立的状态编码器 $\mathcal{E}_\phi$（从预训练编码器复制权重初始化）、可选的控制编码器 $\mathcal{G}_\phi$、以及一个最终的嵌入层 $\mathcal{F}_\phi$。**关键初始化策略**：$\mathcal{F}_\phi$ 的最后一层全连接层权重与偏置均置零，使得训练第一步 $\mathcal{I}_\phi$ 输出为零向量，从而保证适应起点与原始策略完全一致。

适应阶段仅优化注入器参数 $\phi$，预训练编码器 $\mathcal{E}_\xi$ 和策略头 $\pi_\theta$ 保持冻结。

### 内部适应 (Internal Adaptation)

潜在空间注入提供了对策略行为的粗粒度编辑，但对于需要大幅调整控制策略的任务（如地形适应、形态变化），仅修改潜在空间不足以产生足够灵活的控制变化。AdaptNet 在策略网络的每个全连接隐藏层旁路添加**内部适配器**分支，形成残差结构：

$$\mathbf{z}_t^i = \mathcal{F}_\theta^i(\mathbf{z}_t^{i-1}) + \mathcal{F}_\eta^i(\mathbf{z}_t^{i-1})$$

其中 $\mathcal{F}_\theta^i$ 为预训练的第 $i$ 层全连接层（冻结），$\mathcal{F}_\eta^i$ 为新添加的可训练分支，参数 $\eta := \{ \Delta \mathbf{W}_i, \Delta \mathbf{b}_i \}$ 同样采用零初始化。这一设计允许策略在保留原始控制逻辑的基础上，对每一层的潜在表示进行精确的增量调整。

### 适应训练目标

AdaptNet 的优化目标在标准策略梯度基础上加入两项正则化，以防止策略过快漂移：

$$\underset{\phi,\eta}{\operatorname{max}} \mathbb{E}_t \left[ \left( \sum_k \omega_k \bar{A}_t^k \right) \log \pi_\theta \big( \mathbf{a}_t \vert \mathcal{E}_\xi(\mathbf{s}_t) + Z_\phi(\mathbf{s}_t, \mathbf{c}_t); \eta \big) - \beta \vert\vert Z_\phi(\mathbf{s}_t, \mathbf{c}_t) \vert\vert_2 - \kappa \vert\vert \eta \vert\vert_2 \right]$$

- $\bar{A}_t^k$：第 $k$ 个目标（模仿或导向控制）的标准化优势函数
- $\omega_k$：各目标权重
- $\beta \vert\vert Z_\phi \vert\vert_2$：对注入偏移量的 L2 惩罚，约束潜在空间编辑幅度
- $\kappa \vert\vert \eta \vert\vert_2$：对适配器参数的 L2 惩罚，防止内部层过大的权重变化

适应阶段**仅优化 $\phi$ 和 $\eta$**，预训练参数 $\theta, \xi$ 完全冻结。训练采用多批评家（Multi-critic）架构，分别对模仿目标与导向控制目标估计优势，并通过判别器集成（Discriminator Ensemble）基于 GAN 框架提供模仿奖励信号。

### 适应等级插值

通过引入缩放系数 $\alpha \in [0,1]$，可实现从原始策略到完全适应策略的连续过渡：

$$\mathbf{z}_t^0 = \mathcal{E}_\xi(\mathbf{s}_t) + \alpha \mathcal{I}_\phi(\mathbf{s}_t, \mathbf{c}_t), \quad \mathbf{z}_t^i = \mathcal{F}_\theta^i(\mathbf{z}_t^{i-1}) + \alpha \mathcal{F}_\eta^i(\mathbf{z}_t^{i-1})$$

当 $\alpha=0$ 时，角色完全由原始策略控制；$\alpha=1$ 时，AdaptNet 的适应组件完全生效。这一机制支持运动风格插值，也可扩展为两个独立 AdaptNet 模型之间的参数加权混合，实现风格间的平滑过渡。

## 实验与关键发现

### 核心发现与主结果

AdaptNet 在风格迁移、形态变化与地形适应三类任务上均展现出显著的样本效率与最终性能优势。在风格迁移任务（Goose Step、Joyful Walk、Jaunty Skip）中，完整的 AdaptNet（LSA+IA）取得最低的模仿误差：Goose Step 为 0.13±0.07 m，相比仅使用潜在空间适应（LSA）的 0.21±0.12 m 降低 38%；Joyful Walk 为 0.17±0.07 m，降低 35%；Jaunty Skip 为 0.22±0.07 m，降低 21%（Table 2）。在低摩擦地形适应中，AdaptNet 使角色在摩擦系数 0.35 的冰面上保持平衡并奔跑，而无适应的角色完全滑倒失败（Fig. 10），实现了从完全失败到稳定奔跑的质变。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2310_00239/figures/018_Table_2.jpg]]
*Table 2: Imitation error during motion style transfer with different adaptation components. Values are reported in meters in the format of mean±std*

从学习曲线看，AdaptNet 在所有任务上的目标奖励收敛速度和最终值均显著优于四种基线方法：从零训练（Scratch）、直接微调（FT）、带 L2 正则化的微调（FT+Reg）以及渐进网络（PNet）。从零训练在给定的 800 万样本预算内几乎无法获得有效的目标导向控制器，而 AdaptNet 在相同预算下已稳定收敛（Fig. 13，5 次试验均值±标准差）。值得注意的是，AdaptNet 在推理时可合并到原始网络结构中，参数量与预训练策略相同，而 PNet 需要两倍参数。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2310_00239/figures/013_Figure_13.jpg]]
*Figure 13: Learning performance of our adaptation scheme using AdaptNet, training from scratch for each task (Scratch), using a progressive network (PNet), and adaptation via directly finetuning the pre-trained policy (FT) and finetuning with regularization (FT + Reg). Colored regions denote mean values ± a standard deviation based on 5 trials. The top row consists of motion style transfer tasks, while the bottom row focuses on morphological and terrain adaptation tasks*

### 消融实验：适应组件的贡献

Table 2 的消融实验揭示了各适应组件的独立与协同效应：

- **潜在空间适应（LSA）是性能基础**：单独使用 LSA 在 Goose Step 上取得 0.21 m 的模仿误差，已是可用的适应方案。但移除状态编码器 $E_\phi$ 后，误差急剧上升至 0.35 m，证明独立的状态编码器对提取风格特征至关重要。
- **内部适应（IA）单独使用性能不足**：IA 单独使用时 Goose Step 误差为 0.30 m，且无法处理地形适应等需要额外控制输入的任务。IA 必须与 LSA 结合才能发挥完整效用。
- **低秩适应（LoRA）表现不如全秩适应**：以秩=16 的 LoRA 替代全秩内部适应时，Goose Step 误差升至 0.22 m；即使将秩增加到 64，与全秩适应的差距仍然存在。这表明对于规模较小的策略网络，全秩适应更具优势。

### 潜在空间注入位置的决定性影响

注入位置对运动质量有决定性影响。Fig. 16 的足部高度曲线显示，在首个潜在空间 $Z^0$ 进行注入能产生最平滑、最可重复的脚步轨迹。当注入移至更深的 $Z^2$ 或在所有层同时注入时，足部轨迹出现明显抖动，甚至导致训练失败。这验证了 $Z^0$ 是适合操控的瓶颈层，深层注入会破坏已编码的运动基元结构。

### 适应效率与正则化

AdaptNet 的快速适应能力得益于两个设计：零初始化保证训练起点与原始策略行为完全一致，避免初期策略漂移；适应目标中的 L2 正则化项（对注入输出 $Z_\phi$ 和适配器参数 $\eta$ 的惩罚，Eq. 12）进一步抑制过快的行为变化。简单风格迁移任务可在 10-30 分钟内完成适应，复杂地形适应任务约需 4 小时，相比从零训练所需的 26 小时大幅缩短。

### 公平性说明

所有对比方法均使用相同的训练预算（800 万样本）和固定超参数，在 5 个随机种子上进行测试。从零训练在给定预算内无法获得具备目标导向控制能力的控制器，而 AdaptNet 在相同预算下已收敛并表现稳定，确保了比较的公平性。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2310_00239/figures/003_Figure_3.jpg]]
*Figure 3: (c) Discriminator Fig. 3. Network structures. Here, ⊙ denotes the concatenation operator and ⊖ denotes the average operator. The state encoder $\varepsilon _ { \xi }$ is shown in the dashed block. An optional control input encoding module G is included if the additional control input $\mathbf { c } _ { t }$ is provided during adaptation training

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2310_00239/figures/004_Table_1.jpg]]
*Table 1: Reference motions for policy pre-training (top) and stylized motion learning (bottom)*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2310_00239/figures/021_Table_3.jpg]]
*Table 3: Training hyperparameters*

## 定位与知识库关联

### 1. 问题定位与核心瓶颈

在物理角色控制领域，强化学习（RL）策略的复用面临两难困境：直接微调（finetuning）预训练策略容易导致过拟合与灾难性遗忘，而从零训练（scratch）则样本效率低下、耗时过长。AdaptNet 的核心瓶颈在于**如何高效复用已有策略知识，实现快速且稳定的新任务适应**。

### 2. 方法谱系中的位置

AdaptNet 属于**参数高效迁移学习**（Parameter-Efficient Transfer Learning）在物理角色控制领域的应用，其设计思想与以下基线方法形成对比：

| 方法 | 核心机制 | 与 AdaptNet 的关系 |
|------|----------|-------------------|
| **Scratch** | 为每个新任务从零训练完整策略 | 样本效率最低，在给定预算（8M样本）内无法获得有效控制器，作为性能下界 |
| **FT**（直接微调） | 对预训练策略所有参数进行梯度更新 | 容易过拟合到新任务风格，丧失目标导向控制能力（如 Fig. 14 所示，FT 策略在 Pace 风格下无法转弯） |
| **FT+Reg**（带正则化微调） | 在 FT 基础上加入 L2 正则化约束参数偏移 | 部分缓解遗忘，但在复杂适应任务中仍不及 AdaptNet |
| **PNet**（Progressive Networks, Rusu et al., 2016b） | 冻结已有网络，添加新模块并横向连接 | 推理时参数量翻倍，且无法像 AdaptNet 那样通过插值系数 α 实现连续风格过渡 |

AdaptNet 的关键创新在于将策略分解为**固定的预训练编码器**与**可训练的适应组件**，通过零初始化保证训练起点与原始策略完全一致，从而在保留旧技能与获取新能力之间取得平衡。

### 3. 技术贡献的因果机制

AdaptNet 的两层适应架构对应不同的功能粒度：

- **潜在空间注入（Latent Space Injection, LSA）**：在预训练编码器 $\mathcal{E}_\xi$ 的输出上叠加可训练注入器 $\mathcal{I}_\phi$ 的偏移量，实现行为风格的"编辑"。注入器由独立的状态编码器 $\mathcal{E}_\phi$ 和可选控制编码器 $\mathcal{G}_\phi$ 组成，其最终层零初始化确保训练第一步行为不变。
  
- **内部适应（Internal Adaptation, IA）**：在每个冻结的全连接层 $\mathcal{F}_\theta^i$ 旁路添加零初始化分支 $\mathcal{F}_\eta^i$，形成残差结构 $\mathbf{z}_t^i = \mathcal{F}_\theta^i(\mathbf{z}_t^{i-1}) + \mathcal{F}_\eta^i(\mathbf{z}_t^{i-1})$，支持更精细的控制调整。

消融实验揭示了二者的分工：**单独使用 IA 性能不足**（如 Goose Step 模仿误差 0.30m），且无法处理地形适应等需要额外控制输入的任务；**单独使用 LSA** 虽能完成风格迁移（Goose Step 误差 0.21m），但完整 AdaptNet（LSA+IA）将误差进一步降至 0.13m（Table 2）。这表明 LSA 负责提取任务相关的状态表示，IA 则在此基础上进行策略层的精细化调整。

### 4. 适用边界与已知局限

**有效范围**：
- 风格迁移（Goose Step、Joyful Walk、Jaunty Skip 等）
- 形态变化（身体比例改变、关节锁定）
- 地形适应（低摩擦冰面、崎岖地形）
- 目标导向控制（转向导航、障碍物避碰）
- 运动插值（通过缩放系数 α 连续控制适应程度）

**明确局限**：
1. **潜在空间编辑位置受限**：注入仅在浅层 $\mathcal{Z}^0$ 有效。若在更深层 $\mathcal{Z}^2$ 或所有层注入，会导致足部轨迹抖动甚至训练失败（Fig. 16），限制了编辑的灵活性。
2. **低秩适应不足**：与 NLP 领域流行的 LoRA 不同，在物理控制的小规模策略网络中，全秩内部适应显著优于低秩适应（秩=16 或 64），表明该领域的参数高效迁移需要不同的设计选择（Table 2）。
3. **训练时间仍非实时**：复杂地形适应和障碍物避碰任务仍需数小时训练，虽比从零训练大幅缩短，但未达到实时或极低样本适应。
4. **任务范围受限**：当前仅验证了单一运动技能（行走/奔跑）的适应性，未涉及多技能切换或持续学习场景。

### 5. 开放问题与未来方向

1. **潜在空间的可解释性**：如何使潜在表示具备更好的解纠缠性，支持显式的语义编辑（如逆映射和独立风格维度控制）？
2. **框架兼容性**：AdaptNet 能否与 ASE、CALM 等基于物理的控制器训练框架无缝结合，以利用更丰富的技能嵌入？
3. **少样本/在线适应**：在训练数据极度稀少或在线适应场景下，当前基于策略梯度的优化能否保持样本效率和稳定性？
4. **多技能扩展**：如何将两层适应架构推广到多技能策略的持续学习，避免跨技能的灾难性遗忘？

> **注意**：上述开放问题部分源自论文讨论（Section 9），部分为分析推断，需结合后续文献手动验证。

## 原文 PDF

![[paperPDFs/TOG_2023/AdaptNet_Policy_Adaptation_for_Physics_Based_Character_Control.pdf]]
