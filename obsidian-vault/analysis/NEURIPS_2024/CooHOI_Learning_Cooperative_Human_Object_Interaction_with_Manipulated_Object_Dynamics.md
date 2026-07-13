---
title: CooHOI Learning Cooperative Human Object Interaction with Manipulated Object Dynamics
type: paper
paper_level: A
venue: NEURIPS
year: 2024
pdf_ref: paperPDFs/NEURIPS_2024/CooHOI_Learning_Cooperative_Human_Object_Interaction_with_Manipulated_Object_Dynamics.pdf
project_link: null
code_link: null
aliases:
- CLCHOIMOD
tags:
- NEURIPS_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 利用物体动力学信息作为隐式通信通道，使各智能体能够通过观察被操控物体的状态变化来协调动作，并采用两阶段课程学习（单智能体技能预训练 → 多智能体微调）以解决采样效率问题。
primary_logic: 将物体动力学（包围盒状态与速度）作为反馈信号，既让单智能体学习到关注物体动态的技能，又为多智能体提供了无需显式通信的隐式协调机制，从而实现了从单人到多人协作的高效迁移。
claims:
- Two‑agent training from scratch yields 0% success rate, while the two‑stage CooHOI achieves 89.54% success rate.
- Removing dynamic observation results in the agent standing still and unable to carry the object, as shown in training curves.
- Without reverse walk, agents deadlock and cannot transport the box to the destination.
- Restricting object width to 1x while scaling length/height to 1.5x increases two‑agent success rate from 0 to 88.67%.
---

# CooHOI Learning Cooperative Human Object Interaction with Manipulated Object Dynamics

> [!tip] 核心洞察
> 将物体动力学（包围盒状态与速度）作为反馈信号，既让单智能体学习到关注物体动态的技能，又为多智能体提供了无需显式通信的隐式协调机制，从而实现了从单人到多人协作的高效迁移。

| 字段 | 内容 |
|------|------|
| 中文题名 | CooHOI：基于操控物体动力学的协作式人‑物交互学习 |
| 英文题名 | CooHOI Learning Cooperative Human Object Interaction with Manipulated Object Dynamics |
| 会议/期刊 | NEURIPS 2024 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | CooHOI |
| Dataset | Box carrying, Sofa carrying, High stool carrying |

> [!tip] 效果简介
> - Box carrying (single agent) 上，Success Rate 96.48% vs 94.3% (InterPhys) (+2.18%)。
> - Box carrying (two agents) 上，Success Rate 89.54% vs 0% (From Scratch) (+89.54%)。
> - Sofa carrying (two agents) 上，Success Rate 84.17% vs N/A (N/A)。

## 概要

多智能体协作搬运任务面临双重瓶颈：一方面，高质量的多智能体交互动作捕捉数据极度稀缺，难以通过模仿学习直接获取协作策略；另一方面，从零开始的多智能体强化学习（MARL）在复杂物理仿真环境中采样效率极低，策略难以收敛。CooHOI 框架的核心洞察在于，**物体动力学本身可以作为隐式通信通道**——各智能体通过观察被操控物体的包围盒状态与速度变化，无需显式通信即可实现动作协调。

为解决采样效率问题，CooHOI 采用**两阶段课程学习范式**：首先在单智能体场景下，利用 AMP 框架和包含物体动力学信息的观察空间，预训练单人搬运技能；随后将单智能体策略复制到多智能体环境，基于 CTDE-MAPPO 算法进行协作微调。这一设计使得单智能体学得的“关注物体动态”的技能能够自然迁移至多智能体协作场景。

**核心实验结果**：在 Box 搬运任务上，单智能体 CooHOI 成功率达到 96.48%，相比 InterPhys 基线提升 2.18%；两智能体协作场景下，CooHOI 成功率达到 89.54%，而从零开始训练的基线成功率为 0%（Table 1）。消融实验进一步验证了动力学观察、站立点引导和后退行走技能等设计的必要性——移除任一组件均导致策略失败或死锁（Figure 7, Figure 8）。

**方法定位**：CooHOI 属于物理仿真角色控制与多智能体强化学习的交叉领域。其单智能体阶段继承自 AMP 风格的技能模仿范式，多智能体阶段则基于 CTDE 框架实现分布式执行。与依赖参考动作或显式通信的现有方法不同，CooHOI 的核心创新在于将物体动力学信息同时用作单智能体的任务反馈和多智能体的隐式协调信号，从而在无需额外通信开销的条件下实现高效的技能迁移。



### 协作搬运的物理交互难题

在物理仿真环境中让多个仿人角色协同搬运物体，是人‑物交互（Human‑Object Interaction, HOI）领域的前沿挑战。与单人搬运不同，多人协作搬运要求多个智能体在无显式通信的条件下，通过各自对物体的施力来共同控制物体的运动轨迹。这一任务的核心难点在于：**多智能体协作搬运任务缺乏高质量交互动作捕捉数据**，传统的运动模仿范式难以直接迁移到多人场景；同时，**从零开始的多智能体强化学习面临采样效率低下和策略难以收敛的问题**，即便将训练步数延长至常规的 4 倍，成功率仍为 0%（Figure 8）。

### 现有方法的缺口

当前物理仿真 HOI 研究主要集中在单智能体场景。以 **InterPhys** 为代表的单智能体物理交互方法，通过模仿人类动作先验实现了单人搬运物体的自然动作生成，但其观察空间未显式建模物体的动力学信息，且训练范式无法直接扩展到多智能体协作场景。当尝试将此类单智能体策略直接复制到多智能体环境进行从零训练（From Scratch）时，智能体之间缺乏有效的协调机制，导致死锁或无法完成搬运任务——这一现象在 CooHOI 的实验中得到了系统验证。

### 核心瓶颈与本文动机

上述困境的根源在于一个**因果性瓶颈**：多智能体协作搬运需要一种高效的协调信号，而现有方法要么依赖稀缺的多人动作捕捉数据，要么依赖低效的试错探索。CooHOI 的出发点是：**物体本身的动力学状态（包围盒顶点、朝向、线速度、角速度）可以作为隐式通信通道**——当多个智能体同时观察并作用于同一物体时，物体的运动变化自然反映了所有智能体的合力效果，从而无需显式通信即可实现动作协调。基于这一洞察，CooHOI 提出**两阶段课程学习范式**（单智能体技能预训练 → 多智能体协作微调），将物体动力学信息作为贯穿两个阶段的反馈信号，既让单智能体学习到关注物体动态的搬运技能，又为多智能体提供了隐式协调机制，从而实现了从单人到多人协作的高效迁移。



## 核心方法与创新机理

CooHOI 的核心创新在于将**物体动力学作为隐式通信通道**与**两阶段课程学习范式**相结合，系统性地解决了多智能体协作搬运中采样效率低下与策略难以收敛的瓶颈。相较于直接多智能体训练（From Scratch）和仅依赖人体动作先验的单智能体方法（InterPhys），CooHOI 在三个关键维度上做出了改变。

**动力学感知的观察空间设计。** 传统方法（如 InterPhys）的观察空间未显式包含物体动力学信息，智能体难以感知被操控物体的实时状态变化。CooHOI 将物体的包围盒顶点、朝向角、线速度与角速度拼接为动力学特征 $\mathcal{D}_t$，并与智能体自身状态、目标位置共同构成观察输入 $\mathbf{o}_t = \mathrm{concatenate}(s_t, d_t^{\mathrm{pos}}, \mathcal{D}_t)$。这一设计使得单智能体在训练阶段即学会关注物体动态，为后续多智能体协作提供了无需显式通信的隐式协调基础——每个智能体通过观察同一物体的局部动力学变化，即可推断其他智能体的行为意图并调整自身动作。

**从单人到多人的两阶段课程学习。** From Scratch 基线直接对多智能体进行强化学习训练，即便将训练步数延长至 CooHOI 的 4 倍，成功率仍为 0%。CooHOI 采用两阶段策略：第一阶段利用 AMP 框架训练单智能体搬运技能，使其掌握行走、接近物体、持握和运送等基本能力；第二阶段将预训练策略复制到多个智能体，在 CTDE MAPPO 框架下进行协作微调。这一范式将困难的多智能体探索问题分解为“先学会单人搬运，再学会协作”的递进过程，显著降低了策略搜索空间。

**隐式通信机制替代显式通信。** 在多智能体协作微调阶段，CooHOI 不依赖任何显式通信协议或参考动作轨迹。每个智能体独立观察物体动力学特征 $\mathcal{D}_t$，物体状态的改变成为智能体之间唯一的协调信号。这一机制的因果有效性由消融实验证实：移除动力学观察后，智能体原地站立、无法搬运物体（Figure 8）；不训练倒退行走技能时，两智能体出现死锁，无法将箱子运达目的地（Figure 8）。此外，奖励函数被细化为行走奖励 $r_{\mathrm{walk}}^G$、持握奖励 $r_{\mathrm{held}}^G$ 和运送奖励 $r_{\mathrm{target}}^G$ 的组合，并引入站立点（stand point）和持有点（held point）作为空间引导，进一步提升了策略训练的稳定性。



CooHOI 采用**两阶段课程学习范式**，将多智能体协作搬运任务分解为可独立训练、可迁移复用的子问题，从而避开从零开始的 MARL 所面临的采样效率瓶颈与策略收敛难题。

### 阶段一：单智能体技能预训练

第一阶段的目标是让单个仿真人形角色学会**关注物体动力学**的搬运技能。该阶段以 AMP（Adversarial Motion Priors）框架为基础，利用真实人体动作捕捉数据作为运动风格先验，训练一个低层控制策略。与已有工作（如 **InterPhys**）的关键区别在于，CooHOI 在观察空间中显式引入了**被操控物体的动力学特征**：

$$
\mathcal{D}_t = \mathrm{concatenate}(b_t^{\mathrm{ver}}, b_t^{\mathrm{facing}}, b_t^v, b_t^w)
$$

其中 $b_t^{\mathrm{ver}}$ 为物体包围盒的顶点位置，$b_t^{\mathrm{facing}}$ 为朝向角，$b_t^v$ 和 $b_t^w$ 分别为线速度与角速度。完整的动力学感知观察由智能体自身状态、目标位置与物体动力学拼接而成：

$$
\mathbf{o}_t = \mathrm{concatenate}(s_t, d_t^{\mathrm{pos}}, \mathcal{D}_t)
$$

这一设计迫使策略在模仿人类动作的同时，必须持续关注物体的运动状态，从而内化出“物体如何随力移动”的因果感知能力。

任务奖励被细分为三个子目标以提供稠密的学习信号：

- **行走奖励** $r_{\mathrm{walk}}^G$：引导智能体从任意初始位置走向物体背后的站立点（stand point），包含距离项、速度方向项与朝向项；
- **持握奖励** $r_{\mathrm{held}}^G$：鼓励双手中心接近物体预定义的持有点（held point），公式为 $\exp(-5.0\|x_t^{\mathrm{hand}} - h_t\|^2)$；
- **目标运送奖励** $r_{\mathrm{target}}^G$：引导智能体将物体搬运至指定目标位置。

三个子奖励按 $0.2 : 0.4 : 0.4$ 的权重组合为任务奖励 $r^G$，再与风格奖励 $r^S$ 加权求和形成最终奖励：

$$
r_t = w^G r^G(\mathbf{s}_t, \mathbf{g}_t, \mathbf{s}_{t+1}) + w^S r^S(\mathbf{s}_t, \mathbf{s}_{t+1})
$$

### 阶段二：多智能体协作微调

第二阶段将预训练好的单智能体策略**复制为多个同构智能体**，在协作搬运场景下进行微调。训练采用 CTDE（集中训练、分散执行）架构，基于 MAPPO 算法进行多智能体策略优化。价值函数网络 $V_\phi$ 利用所有智能体累积的共享轨迹 $\mathcal{D}_k$ 进行集中式更新，而每个智能体的策略网络仅依赖自身局部观察进行分布式执行。

多智能体优化的目标为最大化折扣累积奖励：

$$
J(\theta) = \mathbb{E}_{\mathbf{a}_1^t, \cdots, \mathbf{a}_n^t, s^t} \left[ \sum_{t=0}^T \gamma^t \mathbf{r}_t \right]
$$

### 隐式通信机制

整个框架的核心设计在于：**物体动力学同时充当了单智能体技能学习的反馈信号与多智能体间的隐式通信通道**。每个智能体独立观察同一物体的包围盒状态与速度变化，无需显式通信即可感知其他智能体施加的力与运动意图。当一方推动或抬升物体时，物体的速度、角速度与顶点位移会即时反映在另一方的观察中，从而自然形成协调。消融实验（Figure 8）表明，移除动力学观察后智能体将静止不动、无法完成搬运，证实了这一隐式通道的不可替代性。

### 关键辅助设计

除上述核心模块外，框架还引入了两个对收敛至关重要的辅助机制：

- **站立点**：在物体后方设置引导点，强制智能体先走到物体正后方再尝试持握，避免其从侧面接近导致抓取失败或死锁；
- **反向行走技能**：在单智能体阶段训练智能体后退行走的能力，使多智能体协作时双方可以面对面搬运，而非发生路径冲突。

消融实验（Figure 7, Figure 8）表明，缺少站立点会导致智能体走向次优面而无法抬起物体；缺少反向行走则使双智能体陷入死锁，无法将箱子运达目的地。

### 补充图表

![[assets/figures/papers/paper_list_l1789_CooHOI_Learning_Cooperative_Human_Object_Interaction_with_Manipulated_Ob/figures/002_Figure_2.jpg]]
*Figure 2: Our framework employs a two-phase learning paradigm. In the first phase, depicted on the left, we train single-agent carrying skills by imitating from human motion priors. In the second phase, we transfer these single-agent skills to a cooperative context. Notably, we use the dynamics of the object as feedback information, as illustrated by the bounding box shown in the figures*

![[assets/figures/papers/paper_list_l1789_CooHOI_Learning_Cooperative_Human_Object_Interaction_with_Manipulated_Ob/figures/001_Figure_1.jpg]]
*Figure 1: Our framework empowers physically simulated characters to execute multi-agent humanobject interaction (HOI) tasks with naturalness and precision*



CooHOI 框架的核心设计围绕一个因果机制展开：**将物体动力学作为隐式通信通道**，使多智能体能够通过观察被操控物体的状态变化来协调动作。这一机制贯穿于整个两阶段训练流程，并通过精心设计的观察空间与奖励函数实现。

### 动力学感知观察模块

该模块是整个框架的感知基础。传统方法（如 InterPhys）的观察空间未显式包含物体动力学信息，导致智能体对物体运动状态不敏感。CooHOI 将物体的动力学特征显式编码为观察输入的一部分。

物体动力学特征 $\mathcal{D}_t$ 定义为：

$$\mathcal{D}_t = \mathrm{concatenate}(b_t^{\mathrm{ver}}, b_t^{\mathrm{facing}}, b_t^v, b_t^w)$$

其中 $b_t^{\mathrm{ver}}$ 为物体包围盒的顶点坐标，$b_t^{\mathrm{facing}}$ 为包围盒的朝向角，$b_t^v$ 为线速度，$b_t^w$ 为角速度。这一设计使智能体能够感知物体的空间姿态与运动趋势。

最终每个智能体的动力学感知观察为：

$$\mathbf{o}_t = \mathrm{concatenate}(s_t, d_t^{\mathrm{pos}}, \mathcal{D}_t)$$

其中 $s_t$ 为智能体自身状态，$d_t^{\mathrm{pos}}$ 为目标位置。消融实验（Figure 8）直接验证了该模块的决定性作用：移除动力学观察后，智能体原地站立，无法搬运物体，训练曲线停滞。

### 任务奖励模块

CooHOI 将搬运任务分解为三个子任务，分别设计奖励函数，引导智能体逐步完成“走近—持握—运送”的完整流程。总任务奖励为三项子奖励的加权组合：

$$r^G = 0.2 \cdot r_{\mathrm{walk}}^G + 0.4 \cdot r_{\mathrm{held}}^G + 0.4 \cdot r_{\mathrm{target}}^G$$

**行走奖励** $r_{\mathrm{walk}}^G$ 鼓励智能体走近物体的站立点（stand point）。该奖励包含距离项、速度方向项和朝向项，当智能体与目标点距离大于 0.2m 时生效，否则直接给予满分。站立点的引入是策略成功的关键：消融实验（Figure 7）表明，移除站立点后智能体会走向物体的次优面，导致持握奖励降低，无法完成抬起动作。

**持握奖励** $r_{\mathrm{held}}^G$ 鼓励智能体双手中心接近物体持有点：

$$r_{\mathrm{held}}^G = \exp(-5.0 \lVert x_t^{\mathrm{hand}} - h_t \rVert^2)$$

其中 $x_t^{\mathrm{hand}}$ 为双手中心位置，$h_t$ 为物体持有点位置。该指数衰减形式对偏差高度敏感，迫使智能体精确对准持握位置。

**目标运送奖励** $r_{\mathrm{target}}^G$ 在物体接近目标位置时给予正向激励（具体公式在原文 Section 3.2.2 中定义，此处不推导）。

智能体总奖励为任务奖励与风格奖励的加权和：

$$r_t = w^G r^G(\mathbf{s}_t, \mathbf{g}_t, \mathbf{s}_{t+1}) + w^S r^S(\mathbf{s}_t, \mathbf{s}_{t+1})$$

风格奖励 $r^S$ 来自 AMP（Adversarial Motion Prior）框架的判别器，用于保持动作的自然性。

### 两阶段训练流程

**阶段一：单智能体技能预训练。** 使用 AMP 框架和上述动力学感知观察空间，通过模仿人类动作先验学习单人搬运技能。此阶段智能体学会关注物体动态，并掌握前进与后退行走（reverse walk）等基础技能。消融实验（Figure 8）表明，移除后退行走训练后，双智能体会出现死锁，无法将箱子运送到目的地。

**阶段二：多智能体协作微调。** 基于 CTDE（集中训练、分散执行）方案，采用 MAPPO 算法。将单智能体策略复制给所有智能体，在协作场景下微调。此时物体动力学自然成为隐式通信通道——每个智能体通过观察同一物体的局部动力学变化，无需显式通信即可协调动作。值函数网络按以下目标更新：

$$\phi_{k+1} = \arg\min_\phi \frac{1}{|\mathcal{D}_k| T} \sum_{\tau \in \mathcal{D}_k} \sum_{t=0}^T \left( V_\phi(o_t) - \hat{R}_t \right)^2$$

其中 $\mathcal{D}_k$ 为所有智能体累积共享的轨迹，$\hat{R}_t$ 为回报估计。这一设计使得 Critic 能够利用全局信息，而 Actor 仅依赖局部观察执行。

### 关键设计决策的证据强度

上述模块的有效性在消融实验中得到系统验证。从零开始的多智能体训练（From Scratch）即使延长至 4 倍训练步数，成功率仍为 0%（Figure 8），而 CooHOI 两阶段训练达到 89.54%（Table 1）。物体宽度限制为 1 倍、长度和高度缩放至 1.5 倍时，双智能体成功率从 0 跃升至 88.67%（Figure 5），进一步证实了物体几何属性对协作可行性的影响。



## 实验与关键发现

### 核心定量结果

CooHOI 在单人搬运任务上与基线持平，在双人协作搬运上实现从零到可用的大幅跨越。Table 1 显示，单人 Box 搬运中 CooHOI 成功率达 **96.48%**，略高于 InterPhys 的 94.3%；而双人 Box 搬运中，CooHOI 成功率达 **89.54%**，相比之下，从零开始训练的多智能体基线（From Scratch）成功率为 **0%**——即使将其训练步数延长至 CooHOI 的 4 倍，策略仍无法收敛（Figure 8）。这一对比直接验证了核心因果机制：两阶段课程学习（单智能体技能预训练→多智能体微调）是解决多智能体强化学习采样效率瓶颈的关键。

![[assets/figures/papers/paper_list_l1789_CooHOI_Learning_Cooperative_Human_Object_Interaction_with_Manipulated_Ob/figures/003_Table_1.jpg]]
*Table 1: This table presents our results for single-agent and two-agent carrying of the Box object. “CooHOI” refers to the policy trained using the complete CooHOI framework in both single-agent and two-agent settings. “CooHOI+WeightAug” indicates that we applied the same weight augmentation design as InterPhys [7]*

![[assets/figures/papers/paper_list_l1789_CooHOI_Learning_Cooperative_Human_Object_Interaction_with_Manipulated_Ob/figures/012_Figure_8.jpg]]
*Figure 8: Training curves for carry reward and held reward in the two-agent setting, using four random seeds, consistent with the definitions provided in Section 3. To ensure different models were trained for the same duration, we extended the training steps for the ‘From Scratch’ model by a factor of 4, as indicated by ‘Scale 4’ in the graph. The curves were plotted by sampling every four frames*

精度指标上，双人协作的终点位置误差仅为 **3.86 cm**，优于单人的 6.9 cm，说明多智能体隐式协调不仅可行，还带来了更稳定的搬运精度。在引入物体重量信息与随机目标距离（1–20 m）后，单人成功率进一步提升至 **97.26%**（Table 1），表明动力学感知观察对任务难度变化具有鲁棒性。

### 跨物体类别泛化

CooHOI 的策略在经过简单微调后，可泛化至多种日常物体。Table 2 显示，双人搬运沙发达 **84.17%** 成功率，单人搬运高脚凳达 **99.21%**。Figure 3 可视化了搬运桌子、扶手椅和高脚凳的过程，所有物体均需移动 4 米。值得注意的是，这些物体的几何形状和尺寸差异显著，策略仍能保持较高的成功率，说明基于包围盒的动力学表示具有一定的形状泛化能力——但其局限性也在此：对于形状过于复杂或无法用包围盒有效描述的物体，泛化能力会下降（见失败模式分析）。

![[assets/figures/papers/paper_list_l1789_CooHOI_Learning_Cooperative_Human_Object_Interaction_with_Manipulated_Ob/figures/005_Table_2.jpg]]
*Table 2: The trained policy exhibits the ability to handle various object categories encountered in daily life with simple fine-tuning. We tested the performance of our policy model across different objects*

![[assets/figures/papers/paper_list_l1789_CooHOI_Learning_Cooperative_Human_Object_Interaction_with_Manipulated_Ob/figures/004_Figure_3.jpg]]
*Figure 3: Carrying performance for objects of different categories. From left to right: Table, Armchair, and High Stools. All objects were required to be moved to a location 4 meters away*

### 消融实验：哪些设计不可或缺？

消融实验揭示了 CooHOI 框架中三个设计要素的因果贡献，任一缺失都会导致训练失败或性能崩溃。

**动力学观察（Dynamic Observation）。** 移除物体动力学信息后，智能体在双人任务中“站在原地不动，无法搬运物体”（Figure 8 训练曲线）。这是隐式通信通道的直接证据：当智能体无法感知物体的速度、角速度和包围盒状态变化时，它们丧失了协调动作的唯一信号来源，策略无法从零学会协作。

**反向行走技能（Reverse Walk）。** 单智能体预训练阶段若不包含反向行走技能，双人微调时会出现死锁——两个智能体面对面僵持，无法将箱子运送到目标位置（Figure 7, Figure 8）。这是因为双人搬运中至少一个智能体需要倒退行走，而该技能必须在单智能体阶段预先习得，多智能体阶段难以从零涌现。

**站立点引导（Stand Point）。** 移除站立点后，智能体会趋向物体的次优面（非最短边），导致持握奖励下降，无法完成抬起动作（Figure 7）。站立点通过引入物体前方的引导点，强制智能体从合理方向接近物体，是任务奖励设计中“行走奖励”得以生效的空间锚点。

**物体尺寸缩放的影响。** Figure 5 展示了物体尺寸对双人协作成功率的非线性影响：当物体宽度保持不变（1×）而长度和高度缩放至 1.5× 时，双人成功率从 0 跃升至 **88.67%**。这表明物体宽度是双人协作的关键瓶颈维度——过宽的物体会使两个智能体的持有点间距超出可操作范围，导致协调失败。

### 失败模式分析

Figure 7 系统展示了三种典型失败模式：
1. **无站立点**：智能体从错误方向接近物体，无法形成有效持握。
2. **无动力学观察**：智能体缺乏物体状态反馈，策略退化至静止状态。
3. **无反向行走**：双人协作陷入死锁，无法完成运输。

![[assets/figures/papers/paper_list_l1789_CooHOI_Learning_Cooperative_Human_Object_Interaction_with_Manipulated_Ob/figures/010_Figure_7.jpg]]
*Figure 7: Some visualization on failure cases. "Stand point" means a leading point behind the object to encourage the agent to walk to the object. "Dynamic Observation" means that each agent has its unique input. "Reverse Walk" indicates whether a single agent possesses the skill to walk backward. Without any of the methods we propose, the policy cannot be successfully trained*

这些失败模式共同指向一个核心机制：CooHOI 的成功依赖于“动力学感知→隐式协调→技能复用”这一因果链的完整性，任一环节断裂都会导致系统崩溃。

### 噪声鲁棒性

Table 4 展示了在观察空间添加高斯噪声后的策略性能。噪声水平以标准差定义，测试覆盖单人和双人 Box 搬运场景。结果表明策略对一定程度的观测噪声具有鲁棒性，这为向真实世界迁移提供了初步证据——但需注意，所有训练仍依赖仿真器提供的真值状态，真实环境中的传感器噪声、遮挡和延迟等问题尚未被充分验证。

![[assets/figures/papers/paper_list_l1789_CooHOI_Learning_Cooperative_Human_Object_Interaction_with_Manipulated_Ob/figures/011_Table_4.jpg]]
*Table 4: Results of our policy under noisy conditions: We tested both single-agent and two-agent box-carrying scenarios. The noise level is defined by the standard deviation of the Gaussian noise used. SR stands for success rate. The definitions of success rate and precision are consistent with those in Section 4.1 of our paper*

### 训练曲线分析

Figure 8 的双人训练曲线提供了收敛过程的动态视角。CooHOI 的搬运奖励和持握奖励在训练早期即快速上升并稳定收敛，而 From Scratch 基线即使训练步数延长 4 倍，奖励始终在低位震荡。消融模型的曲线则显示：移除动力学观察或反向行走后，奖励完全无法增长，进一步验证了这些组件是策略收敛的必要条件而非锦上添花。

### 实验公平性说明

- From Scratch 基线的训练步数延长至 CooHOI 的 4 倍，确保比较的公平性。
- 所有实验使用相同的超参数、随机种子数量和仿真环境。
- 噪声鲁棒性实验通过在观察空间注入高斯噪声模拟真实环境的不确定性。

### 补充图表

![[assets/figures/papers/paper_list_l1789_CooHOI_Learning_Cooperative_Human_Object_Interaction_with_Manipulated_Ob/figures/007_Figure_5.jpg]]
*Figure 5: Detailed ablation experiments on single and two agents cases. "Step" measures the average consumed time in the successful cases. In the 2nd figure, the green circle represents the single-agent scenario without scaling the object’s width, while the purple circle represents the multi-agent scenario*

![[assets/figures/papers/paper_list_l1789_CooHOI_Learning_Cooperative_Human_Object_Interaction_with_Manipulated_Ob/figures/006_Figure_4.jpg]]
*Figure 4: Visualization of cooperative carrying in the multi-agent scenario*

![[assets/figures/papers/paper_list_l1789_CooHOI_Learning_Cooperative_Human_Object_Interaction_with_Manipulated_Ob/figures/009_Table_3.jpg]]
*Table 3: Hyperparameters for CooHOI*

![[assets/figures/papers/paper_list_l1789_CooHOI_Learning_Cooperative_Human_Object_Interaction_with_Manipulated_Ob/figures/008_Figure_6.jpg]]
*Figure 6: Some visualization of daily-life objects*



## 定位与知识库关联

### 一、与基线方法的关系与核心改进

CooHOI 的方法谱系可追溯到两条主线：基于物理仿真的人‑物交互（Physics‑based HOI）与多智能体强化学习（MARL）。论文明确对比的基线包括单智能体基线 **InterPhys** 和直接多智能体训练基线 **From Scratch**。由于论文未提供 InterPhys 的具体作者/会议/年份元数据，此处无法给出完整引用，需读者手动核实。

**相对 InterPhys 的改进**：InterPhys 作为单智能体物理仿真 HOI 方法，未显式建模物体动力学信息。CooHOI 将物体包围盒的顶点、朝向角、线速度与角速度拼接为动力学特征 $\mathcal{D}_t$，并纳入智能体的观察空间，使策略学会关注被操控物体的动态变化。这一改动使单智能体搬运成功率从 94.3% 提升至 96.48%（Table 1），精度达到 6.9 cm。进一步引入重量增强（Weight Augmentation）后，单智能体成功率可达 97.26%。

**相对 From Scratch 的改进**：直接多智能体训练面临采样效率低下和策略难以收敛的瓶颈。CooHOI 采用两阶段课程学习——先通过 AMP 框架预训练单智能体搬运技能，再基于 CTDE 架构的 MAPPO 算法进行多智能体协作微调。这一范式使双人搬运成功率从 0% 跃升至 89.54%（Table 1），精度达 3.86 cm。即使将 From Scratch 的训练步数延长至 CooHOI 的 4 倍，成功率仍为 0%（Figure 8），说明课程学习而非训练时长是成功的关键。

**隐式通信机制**：与依赖显式通信或参考动作的方法不同，CooHOI 利用物体动力学作为隐式通信通道。每个智能体独立观察同一物体的局部动力学特征，通过物体状态变化间接感知协作者的意图与动作效果，从而在不增加通信开销的前提下实现协调。

### 二、适用边界与泛化能力

**物体类别泛化**：CooHOI 通过简单微调即可泛化至多种日常物体。单智能体搬运高脚凳成功率达 99.21%，双人搬运沙发成功率达 84.17%（Table 2）。框架还展示了搬运桌子、扶手椅等物体的能力（Figure 3）。但泛化依赖于物体的包围盒表示，对形状复杂、非凸或可变形物体的适应能力有限。

**维度缩放鲁棒性**：在物体尺寸缩放实验中，将物体宽度限制为 1 倍、长度和高度缩放至 1.5 倍时，双人搬运成功率从 0 提升至 88.67%（Figure 5）。这表明物体宽度是影响多智能体协作的关键几何因素——过宽的物体使两个智能体难以同时接近并协调持握。

**噪声鲁棒性**：在观察空间添加高斯噪声的测试中，单智能体和双智能体策略均表现出一定鲁棒性（Table 4），但具体数值需查阅原表。该测试旨在评估框架在现实世界观测误差下的适应性。

**距离泛化**：单智能体策略在目标距离 1–20 米范围内均能成功搬运，成功率保持在 97% 以上（Table 1），说明策略对任务距离变化具有较好的泛化性。

### 三、局限性与已知失效模式

**硬件与灵巧操作缺失**：当前框架未集成灵巧手，智能体通过简化的持有点与物体交互，无法操作需要精细抓握的物体（如滑溜物体、小物件）。这限制了框架在需要多样化操作技能的场景中的应用。

**仿真到现实的鸿沟**：所有状态信息依赖仿真器的真实数据，现实世界中存在传感器噪声、遮挡和观测误差。虽然噪声鲁棒性实验提供了初步验证，但未在真实人形机器人上部署测试，Sim‑to‑Real 迁移的可行性仍待证实。

**物体表示瓶颈**：物体信息主要通过包围盒表示，对形状复杂、非刚性或铰接式物体的泛化能力有限。论文未探索更丰富的物体表示（如点云、隐式场），这限制了框架在开放环境中的适用性。

**已知失效模式**（Figure 7, Figure 8）：
- **移除动力学观察**：智能体静止不动，无法搬运物体，训练曲线显示持握奖励持续为零。
- **移除逆向行走技能**：双智能体陷入死锁，无法将箱子运送到目标位置。
- **移除站立点（Stand Point）**：智能体趋向于接近物体的非最优面，导致无法完成抬起动作。
- **训练曲线分析**：From Scratch 模型的搬运奖励和持握奖励在延长训练后仍无上升趋势，证实从零开始的多智能体训练在该任务上不可行。

### 四、开放问题

1. **多智能体扩展**：当前框架验证了双人协作，论文提及了四人场景的可能性，但如何扩展到更多智能体并处理负载动态分配仍是一个开放问题。超过两个智能体时，物体动力学的隐式通信是否仍能提供足够的协调信号？

2. **灵巧手集成**：如何将灵巧手纳入框架，使智能体能够操作更多种类的物体并执行精细动作（如拧瓶盖、抓取不规则物体），是提升框架实用性的关键方向。

3. **主动感知与导航**：当前框架假设目标位置已知，且环境无障碍物。如何整合主动感知（如视觉 SLAM）和导航能力，使智能体能在开放、动态的环境中自主完成搬运任务？

4. **统一物体表示学习**：当前针对不同物体类别需要从零训练或微调。能否通过大规模数据学习统一的物体表示，使策略在零样本或少样本条件下泛化到未见过的物体？

5. **现实世界部署**：框架尚未在真实人形机器人上验证。Sim‑to‑Real 迁移中的域随机化、系统辨识和在线自适应策略是需要进一步研究的问题。



## 原文 PDF

![[paperPDFs/NEURIPS_2024/CooHOI_Learning_Cooperative_Human_Object_Interaction_with_Manipulated_Object_Dynamics.pdf]]
