---
title: "PhysicsFC: Learning User-Controlled Skills for a Physics-Based Football Player Controller"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_2025/PhysicsFC_Learning_User_Controlled_Skills_for_a_Physics_Based_Football_Player_Controller.pdf
aliases:
- PhysicsFC
tags:
- SIGGRAPH_2025
- topic/other_unclear
- topic/other_unclear/general
core_operator: 针对每项技能设计的专门奖励函数与初始状态采样策略（如两阶段停球奖励、盘带多目标奖励），结合技能过渡初始化（STI）和数据嵌入目标条件潜变量引导（DEGCL）方法。
primary_logic: 通过让各个技能策略输出潜变量控制预训练的低层运动模型，并针对每种技能设计独特的奖励和初始化方案，特别是利用技能过渡初始化（STI）让策略学会从中间状态恢复，从而实现了流畅且用户可控的多技能足球模拟。
claims:
- 移除早期终止（DistanceET）导致盘带策略完全无法学习（目标达成率从90.3%骤降至2.0%）。
- STI对技能过渡至关重要：盘带到踢球过渡中使用STI的踢球成功率100%，而不使用STI仅16.95%。
- Trap策略的两阶段奖励和抛射体初始状态（ProjectileInit）使得停球成功率达到78.3%，移除抛射初始化后降至21.1%。
- DEGCL使移动策略在保持目标达成率的同时显著提升运动真实感（潜变量相似度从0.52升至0.62）。
---

# PhysicsFC: Learning User-Controlled Skills for a Physics-Based Football Player Controller

> [!tip] 核心洞察
> 通过让各个技能策略输出潜变量控制预训练的低层运动模型，并针对每种技能设计独特的奖励和初始化方案，特别是利用技能过渡初始化（STI）让策略学会从中间状态恢复，从而实现了流畅且用户可控的多技能足球模拟。

| 字段 | 内容 |
|------|------|
| 中文题名 | PhysicsFC：面向物理足球角色的用户控制技能学习 |
| 英文题名 | PhysicsFC: Learning User-Controlled Skills for a Physics-Based Football Player Controller |
| 会议/期刊 | SIGGRAPH 2025 |
| Links |  |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | PhysicsFC |
| Dataset | Dribble Skill, Trap Skill, Move Skill, Kick Skill |

> [!tip] 效果简介
> - Dribble Skill (Custom) 上，DGAR (%) ↑ 90.3 vs 2.0 (w/o DistanceET) (+88.3)。
> - Trap Skill (Custom) 上，TSR (%) ↑ 78.3 vs 21.1 (w/o ProjectileInit) (+57.2)。
> - Move Skill (Custom) 上，GMLS ↑ 0.62 vs 0.52 (w/o DEGCL) (+0.10)。

## 概述

PhysicsFC 提出了一种在物理仿真环境中实现用户可控、多技能无缝切换的足球角色控制框架。其核心挑战在于：在物理模拟的约束下，让角色同时掌握移动、停球、盘带、踢球等多种足球技能，并能根据用户指令在技能间平滑过渡。

该方法的核心思路是“高层技能策略 + 低层运动嵌入”的分层架构。低层策略基于 CALM（Conditioned Adversarial Latent Models）框架，在足球运动捕捉数据上预训练，将高维运动控制压缩为潜变量 $z$ 的生成。高层策略则针对每种足球技能（移动、停球、盘带、踢球）独立设计，接收角色状态、球状态及用户目标，输出潜变量 $z$ 驱动低层策略。技能间的切换由有限状态机（FSM）管理，用户通过手柄输入实时控制目标速度、方向及技能切换。

实现多技能协同的关键技术突破有两项。**技能过渡初始化（STI）** 在训练各技能策略时，从前序技能的仿真运行中采样中间状态作为初始状态，使策略学会从各种中间姿态恢复并启动当前技能，从而消除技能切换时的生硬跳变。**数据嵌入目标条件潜变量引导（DEGCL）** 则针对移动策略，从训练数据中提取（目标，潜变量）对，在训练中交替使用随机目标和数据参考目标，并增加潜变量相似度奖励，使移动动作在满足任务目标的同时保持运动真实感。

实验表明，各技能策略通过针对性设计的奖励函数和初始化方案取得了显著效果：盘带策略目标达成率 90.3%，停球成功率 78.3%，踢球成功率 99.9%。消融实验揭示了关键设计的作用——移除早期终止使盘带几乎完全失效（降至 2.0%），移除抛射体动力学初始化使停球成功率骤降至 21.1%，而 STI 使盘带到踢球的过渡成功率从 16.95% 跃升至 100%。在交互式场景中，PhysicsFC 支持用户操控角色完成二过一配合、竞争性停球盘带乃至 11v11 足球比赛仿真，展示了从单一技能训练到复杂多智能体场景的可扩展性。

## 背景与动机

### 物理仿真足球控制的挑战

在电子游戏与计算机动画领域，构建具有物理真实感的交互式角色一直是核心目标之一。足球运动因其丰富的技能组合（跑动、停球、盘带、踢球）和高动态的球-人-环境交互，成为检验物理角色控制能力的理想场景。然而，现有方法面临一个根本性瓶颈：**在物理仿真环境中，难以让单一角色同时掌握多项足球技能，并在用户实时操控下实现平滑的技能间切换**。

具体而言，这一瓶颈体现在三个层面：

1. **技能多样性带来的奖励设计难题**：控球、盘带、停球、踢球各自需要截然不同的运动策略。例如，盘带要求角色在保持近身控球的同时按目标速度移动，而停球则需要精确判断来球轨迹并用身体特定部位缓冲。为这些技能设计统一的奖励函数极其困难，单一奖励往往导致策略陷入局部最优或完全失效。

2. **技能过渡的分布偏移**：即使各技能策略独立训练成功，从一种技能切换到另一种技能时，新策略面临的初始状态分布与其训练时的状态分布存在显著差异。例如，从停球结束瞬间切换到盘带，球的相对位置和速度与盘带策略训练中随机初始化的状态截然不同，导致策略在过渡时刻表现崩溃。

3. **运动质量与任务完成的权衡**：物理仿真中的移动策略往往在追求目标速度时产生不自然的步态——步频过高、步长异常，甚至出现侧向移动中即将摔倒的姿态。如何在保证任务完成率的同时维持运动真实感，是一个尚未充分解决的问题。

### 现有方法的缺口

此前的工作主要沿两个方向展开：一是基于运动匹配的控制器（motion matching），虽能产生高质量动画但缺乏物理交互能力；二是基于深度强化学习的物理角色控制，虽能实现物理交互，但多聚焦于单一技能（如行走、拳击），鲜有方法能覆盖足球所需的完整技能谱系。在足球领域，现有物理仿真工作通常仅针对传球或射门等孤立动作，缺少一个统一的框架来实现用户可控的多技能足球模拟。

### 本文动机与核心思路

针对上述缺口，PhysicsFC 提出了一套系统性的解决方案，其核心思路是：**为每项足球技能设计专门的奖励函数与初始状态采样策略，并通过技能过渡初始化（STI）和数据嵌入目标条件潜变量引导（DEGCL）两项关键技术，实现技能间的平滑过渡与高质量运动生成**。

具体而言，PhysicsFC 的动机源于以下几个关键观察：

- **分而治之的奖励设计**：盘带策略需要同时优化球速匹配、球-根距离和根速度朝向，单一奖励项（如仅匹配球速）无法引导策略学会近身控球与方向调整。通过三项加权奖励配合目标速度归一化（NTS），策略才能在多种目标速度下稳定盘带。

- **两阶段停球与抛射体初始化**：停球动作天然分为碰撞前（身体部位接近球）和碰撞后（球与身体速度匹配）两个阶段。若不对球的初始状态进行物理约束（如基于抛射体动力学计算落点），策略将面对大量不可达的来球，导致学习效率极低。

- **从中间状态恢复的能力**：技能切换的本质是策略需要从非典型的中间状态开始执行。STI 通过在训练中采样前序技能的终止状态作为初始状态，使策略学会从各种中间状态快速恢复，而非仅依赖随机初始化。

- **运动数据的结构化利用**：移动策略若仅追求任务目标（速度、朝向），容易产生不自然的步态。DEGCL 通过从运动捕捉数据中提取“目标-潜变量”对，在训练中引导策略输出与数据一致的动作潜变量，从而在任务完成与运动质量之间取得平衡。

这些设计共同构成了 PhysicsFC 的方法论基础，使其能够在物理仿真中实现用户可控的、包含跑动、停球、盘带、踢球及平滑过渡的完整足球技能体系。

## 核心创新

PhysicsFC的核心创新在于针对物理仿真足球场景中多技能学习与平滑切换的瓶颈，设计了一套分技能定制化训练与过渡机制。其关键创新点体现在以下几个维度：

### 1. 分技能差异化奖励设计

PhysicsFC放弃了统一奖励函数的思路，为每项足球技能设计了专门的多目标奖励结构，以应对各自独特的物理约束：

- **盘带（Dribble）**：采用三项加权奖励（球速度匹配0.6、球-根距离0.2、根速度朝向球0.2），并通过目标速度归一化（NTS）消除速度尺度差异。消融实验表明，移除早期终止（DistanceET）后目标达成率从90.3%骤降至2.0%（Table 1），证明该奖励设计对策略收敛至关重要。

- **停球（Trap）**：创新性地采用两阶段奖励函数——碰撞前鼓励指定身体部位接近球，碰撞后（持续1/6秒）鼓励球与角色根节点的三维速度匹配。这种分阶段引导使策略能够处理高空球和地面球两种来球模式。

- **移动（Move）**：在任务奖励（速度匹配0.7+朝向匹配0.3）基础上，引入数据嵌入目标条件潜变量引导（DEGCL），通过潜变量相似度奖励引导策略输出与运动捕捉数据一致的动作，使潜变量相似度从0.52提升至0.62（Table 4）。

### 2. 技能过渡初始化（STI）

这是实现多技能无缝切换的核心机制。传统方法从随机状态或前序策略终止状态开始训练，导致策略在过渡时刻表现脆弱。STI通过以下流程解决该问题：

1. 使用已训练的前序技能策略模拟大量回合，将角色与球的状态存入STI缓冲区；
2. 在训练当前技能策略时，从STI缓冲区采样初始状态，使策略学会从各种中间状态恢复并快速进入目标技能。

实验证据极为有力：盘带到踢球过渡中使用STI的踢球成功率达100%，而不使用STI仅16.95%（Table 9）；停球到盘带过渡时间缩短23%（2.71s vs 3.54s，Table 6）。

### 3. 数据嵌入目标条件潜变量引导（DEGCL）

移动策略面临的核心挑战是：在满足任意目标速度/朝向的同时保持运动真实感。DEGCL通过以下方式解决：

- 从运动捕捉数据集中提取（目标，潜变量）参考对，构建DEGCL缓冲区；
- 训练时交替使用一般随机目标回合和DEGCL参考目标回合，在DEGCL回合中增加潜变量相似度奖励（$r_t^{\mathrm{lt\_sim}} = \bar{\mathbf{z}}_t \cdot \mathbf{z}_t$）。

消融实验显示，移除DEGCL后移动策略出现步长过短、步频过高、侧向移动姿态不稳等问题（Figure 13），潜变量相似度从0.62降至0.52（Table 4）。

### 4. 基于抛射体动力学的训练初始化

停球策略训练中，随机生成球的初始状态会导致大量无效训练样本。PhysicsFC基于抛射体运动方程，根据随机指定的落点位置、初始速度等参数反向计算球的初始状态，确保球落点位于角色可达半圆区域内。移除该初始化后，停球成功率从78.3%降至21.1%（Table 3），证明其不可或缺。

### 5. 足球靴形碰撞网格

使用足球靴凸包碰撞体替代传统盒状碰撞体，使角色脚部与球的物理交互更符合真实足球运动学。论文指出，使用方形脚碰撞时盘带无法学习方向调整，踢球速度偏差显著（Section 4），这一定性观察虽未提供量化指标，但对技能学习具有基础性影响。

### 创新总结

PhysicsFC的创新本质上是**通过分技能奖励工程与状态空间桥接，将复杂的多技能物理控制问题分解为可独立优化的子问题，再通过STI实现子策略间的平滑拼接**。其方法谱系上承CALM等物理运动嵌入模型，但在技能特化训练与过渡机制上提供了系统性的增量贡献。

## 整体框架

PhysicsFC 的整体框架围绕“高层技能策略 + 共享低层运动模型”的分层架构展开，并通过有限状态机（FSM）管理技能间的动态切换。其设计目标是在物理仿真环境中实现用户可控、多技能无缝切换的足球角色控制。

### 核心模块与数据流

系统由以下关键模块构成，形成从用户输入到物理动作的完整闭环：

1. **低层运动模型（CALM）**：基于物理的运动嵌入模型，在足球运动捕捉数据上预训练。它接收高层策略输出的潜变量 $z$ 和角色状态，输出可直接驱动物理仿真的低层动作。该模型为所有足球技能提供共享的运动基元，确保动作的物理合理性与运动真实感。

2. **高层技能策略**：针对四项足球技能分别训练独立的策略网络——**Dribble**（盘带）、**Trap**（停球）、**Move**（移动）、**Kick**（踢球）。每个策略接收角色状态、球状态及特定目标（如目标盘带速度、停球部位、目标移动速度方向、踢球目标），输出潜变量 $z$ 给低层模型。各策略拥有独立设计的奖励函数、回合初始化方案和终止条件。

3. **PhysicsFC 有限状态机（FSM）**：管理技能状态并基于用户输入或上下文条件触发过渡。用户通过游戏手柄输入控制角色，FSM 根据当前状态和输入决定激活哪个技能策略，实现移动、停球、盘带、踢球之间的无缝切换。

4. **技能过渡初始化（STI）缓冲区**：为每个技能存储来自前序策略仿真中产生的过渡时刻状态（角色状态 + 球状态）。在训练当前技能策略时，从相应 STI 缓冲区采样回合初始状态，使策略学会从各种中间状态快速恢复并执行技能，是实现平滑过渡的核心机制。

5. **数据嵌入目标条件潜变量引导（DEGCL）缓冲区**：从运动捕捉数据集中提取运动片段对应的（目标速度/方向，潜变量）对。在移动策略训练时，交替使用一般随机目标回合和 DEGCL 引导回合，通过潜变量相似度奖励引导策略输出与训练数据一致的动作，提升运动质量。

6. **球初始化模块（抛射体动力学）**：专用于停球策略训练。根据抛射体运动方程计算球的初始位置与速度，确保球落点位于角色可达半圆区域内，使策略能够学习处理高吊传球和地面传球。

### 输入输出流

- **输入**：用户通过游戏手柄提供高层指令（目标移动速度/方向、盘带速度、停球部位选择、踢球触发）。FSM 将指令路由至对应技能策略。
- **中间表示**：技能策略输出潜变量 $z$，作为低层运动模型的条件信号。
- **输出**：低层模型生成关节力矩或目标姿态，驱动物理仿真中的角色与球交互。

### 技能过渡机制

技能间的无缝切换依赖于 STI 方法。以盘带策略训练为例：先使用已训练好的停球和移动策略运行大量仿真回合，将终止状态存入各自的 STI 缓冲区；训练盘带策略时，一半回合从停球 STI 缓冲区采样初始状态，另一半从移动 STI 缓冲区采样。这使得盘带策略学会在刚停球后或移动中快速启动盘带，而非仅从静止初始状态学习。消融实验表明，STI 对过渡性能至关重要——盘带到踢球过渡中使用 STI 的踢球成功率达 100%，而不使用 STI 仅 16.95%（Table 9）；移动到停球过渡中 STI 使停球成功率从 55.1% 提升至 74.1%（Table 8）。

![[assets/figures/papers/paper_list_l1805_PhysicsFC_Learning_User_Controlled_Skills_for_a_Physics_Based_Football_P/figures/019_Table_8.jpg]]
*Table 8: Comparison of Move-to-Trap transition performance with and without STI*

### 物理仿真细节

所有策略训练和运行时仿真均基于 Isaac Gym Preview 4，使用固定的物理参数配置。角色脚部采用足球靴凸包碰撞体（而非简单盒状碰撞体），这对盘带和踢球技能的学习至关重要——使用方形脚碰撞时，盘带无法学习方向调整，踢球速度偏差显著。

## 核心模块与公式推导

PhysicsFC 的完整技能控制器由四个核心设计要素构成：共享的低层运动嵌入模型、面向各足球技能的高层策略、实现无缝切换的技能过渡初始化（STI）机制，以及提升运动质量的数据嵌入目标条件潜变量引导（DEGCL）方法。以下逐一展开其关键模块与公式。

### 低层运动嵌入模型（CALM）

所有技能策略共享一个基于物理的运动嵌入模型，该模型在足球运动捕捉数据上预训练，接收高层策略输出的潜变量 $z$ 和角色状态，生成低层关节扭矩动作。这一设计使高层策略只需学习“选择什么动作”而非“如何执行动作”，大幅降低了技能学习的难度。模型结构见原文 Figure 14，预训练细节见 Appendix A。

![[assets/figures/papers/paper_list_l1805_PhysicsFC_Learning_User_Controlled_Skills_for_a_Physics_Based_Football_P/figures/023_Figure_14.jpg]]
*Figure 14: Structure of CALM model*

### 盘带策略（Dribble Policy）

盘带策略以目标盘带速度 $\hat{\mathbf{v}}_t^{\mathrm{drib}} \in \mathbb{R}^2$ 为输入目标，输出潜变量 $z$ 驱动低层模型。其奖励函数由三项加权组成：

$$r_t^{\mathrm{drib}} = 0.6\, r_t^{\mathrm{ball\_vel}}\big(\hat{\mathbf{v}}_t^{\mathrm{drib}}, \mathbf{v}_t^{\mathrm{ball}(2)}\big) + 0.2\, r_t^{\mathrm{ball\_root\_pos}}\big(\mathbf{x}_t^{\mathrm{root}(2)}, \mathbf{x}_t^{\mathrm{ball}(2)}\big) + 0.2\, r_t^{\mathrm{root\_vel}}\big(\hat{\mathbf{v}}_t^{\mathrm{drib}}, \mathbf{v}_t^{\mathrm{root}(2)}, \mathbf{x}_t^{\mathrm{root}(2)}, \mathbf{x}_t^{\mathrm{ball}(2)}\big)$$

三项子奖励的具体形式如下（详见 Appendix C）：

**球速度匹配奖励** $r_t^{\mathrm{ball\_vel}}$ 鼓励球的水平速度 $\mathbf{v}_t^{\mathrm{ball}(2)}$ 在方向和大小上同时逼近目标盘带速度 $\hat{\mathbf{v}}_t^{\mathrm{drib}}$，并以目标速度进行归一化（Normalized Target Speed, NTS）：

$$r_t^{\mathrm{ball\_vel}} = \exp\!\left(-10\left[\left(\frac{\|\hat{\mathbf{v}}_t^{\mathrm{drib}} - \mathbf{v}_t^{\mathrm{ball}(2)}\|}{\|\hat{\mathbf{v}}_t^{\mathrm{drib}}\| + \epsilon}\right)^2 + 0.1\left(\frac{\|\hat{\mathbf{v}}_t^{\mathrm{drib}}\| - \|\mathbf{v}_t^{\mathrm{ball}(2)}\|}{\|\hat{\mathbf{v}}_t^{\mathrm{drib}}\| + \epsilon}\right)^2\right]\right)$$

**球-根距离奖励** $r_t^{\mathrm{ball\_root\_pos}}$ 鼓励角色根节点与球的水平距离尽可能小，以维持近身控球：

$$r_t^{\mathrm{ball\_root\_pos}} = \exp\!\left(-10\left\|\mathbf{x}_t^{\mathrm{ball}(2)} - \mathbf{x}_t^{\mathrm{root}(2)}\right\|^2\right)$$

**根速度朝向球奖励** $r_t^{\mathrm{root\_vel}}$ 鼓励角色根节点以目标速度大小沿指向球的方向移动。其中 $\mathbf{d}_t^{\mathrm{r2b}}$ 为水平面上从根节点指向球的单位方向向量：

$$\mathbf{d}_t^{\mathrm{r2b}} = \frac{\mathbf{x}_t^{\mathrm{ball}(2)} - \mathbf{x}_t^{\mathrm{root}(2)}}{\|\mathbf{x}_t^{\mathrm{ball}(2)} - \mathbf{x}_t^{\mathrm{root}(2)}\|}$$

$$r_t^{\mathrm{root\_vel}} = \exp\!\left(-10\left[\left(\frac{\big\|\|\hat{\mathbf{v}}_t^{\mathrm{drib}}\|\,\mathbf{d}_t^{\mathrm{r2b}} - \mathbf{v}_t^{\mathrm{root}(2)}\big\|}{\|\hat{\mathbf{v}}_t^{\mathrm{drib}}\| + \epsilon}\right)^2 + 0.1\left(\frac{\|\hat{\mathbf{v}}_t^{\mathrm{drib}}\| - \|\mathbf{v}_t^{\mathrm{root}(2)}\|}{\|\hat{\mathbf{v}}_t^{\mathrm{drib}}\| + \epsilon}\right)^2\right]\right)$$

**关键消融发现**：移除早期终止条件 DistanceET 后，盘带目标达成率（DGAR）从 90.3% 骤降至 2.0%（Table 1），表明在训练中及时终止偏离目标速度过远的回合对策略收敛至关重要。

### 停球策略（Trap Policy）

停球策略以指定触球身体部位的一维 one-hot 向量为输入，采用**两阶段奖励**设计，以碰撞时刻 $t_c$ 为分界：

$$r_t^{\mathrm{trap}} = \begin{cases} r_t^{\mathrm{before}} = \exp\!\left(-10\left\|\mathbf{x}_t^{\mathrm{ball}(3)} - \mathbf{x}_t^{\mathrm{body}}\right\|^2\right), & t \leq t_c \\[6pt] r_t^{\mathrm{after}} = \exp\!\left(-10\left\|\mathbf{v}_t^{\mathrm{ball}(3)} - \mathbf{v}_t^{\mathrm{root}(3)}\right\|^2\right), & \text{otherwise} \end{cases}$$

- **碰撞前**（$t \leq t_c$）：鼓励指定身体部位 $\mathbf{x}_t^{\mathrm{body}}$ 在三维空间中接近球的位置 $\mathbf{x}_t^{\mathrm{ball}(3)}$。
- **碰撞后**（$t > t_c$）：鼓励球的三维速度 $\mathbf{v}_t^{\mathrm{ball}(3)}$ 与角色根节点速度 $\mathbf{v}_t^{\mathrm{root}(3)}$ 匹配，持续 1/6 秒，使球被“卸力”后随角色平稳运动。

**抛射体动力学初始化（ProjectileInit）** 是停球策略训练的另一个关键设计：球的初始状态并非随机生成，而是基于抛射体运动方程解析计算，确保球落点位于角色可达的半圆区域内（Figure 7）。消融实验表明，移除该初始化后停球成功率（TSR）从 78.3% 降至 21.1%（Table 3），说明合理的初始状态分布对策略学习空中停球能力不可或缺。

### 移动策略（Move Policy）与 DEGCL

移动策略以目标速度和朝向为输入，其任务奖励由速度匹配（权重 0.7）和朝向匹配（权重 0.3）组成：

$$r_t^{\mathrm{mv\_task}} = 0.7\, r_t^{\mathrm{vel}}\big(\mathbf{v}_t^{\mathrm{target}}, \mathbf{v}_t^{\mathrm{root}(2)}\big) + 0.3\, r_t^{\mathrm{dir}}\big(\mathbf{d}_t^{\mathrm{target}}, \mathbf{d}_t^{\mathrm{root}}\big)$$

其中速度奖励 $r_t^{\mathrm{vel}}$ 同样采用目标速度归一化（NTS）的指数形式（见 Appendix E, Equation 18），朝向奖励 $r_t^{\mathrm{dir}}$ 为目标朝向与角色朝向的点积（见 Appendix E, Equation 19）。

**DEGCL 机制** 是移动策略的核心创新。训练分为两类回合交替进行：
- **通用回合**：仅使用上述任务奖励。
- **DEGCL 回合**：从预构建的 DEGCL 缓冲区（存储来自运动捕捉数据的“目标-潜变量”对）中采样参考目标，并引入潜变量相似度奖励：

$$r_t^{\mathrm{lt\_sim}} = \bar{\mathbf{z}}_t \cdot \mathbf{z}_t$$

其中 $\bar{\mathbf{z}}_t$ 为缓冲区中的参考潜变量，$\mathbf{z}_t$ 为策略当前输出的潜变量，二者点积鼓励策略输出与参考动作一致的潜变量。DEGCL 回合的总奖励为：

$$r_t^{\mathrm{move}} = 0.5\, r_t^{\mathrm{mv\_task}} + 0.5\, r_t^{\mathrm{lt\_sim}}$$

消融实验（Table 4）证实，移除 DEGCL 后潜变量相似度 GMLS 从 0.62 降至 0.52，运动质量明显退化——具体表现为后向移动步长过短、步频过高，侧向移动出现即将侧倒的姿态（Figure 13）。

### 技能过渡初始化（STI）

STI 是打通技能间无缝切换的枢纽机制。其流程为：先用已训练的前序技能策略（如停球、移动）模拟大量回合，将角色和球的状态存入各技能的 STI 缓冲区；在训练目标技能（如盘带）时，一半回合从相关前序技能的 STI 缓冲区中随机采样初始状态，使策略学会从各种中间状态快速恢复并启动新技能（Figure 3）。

![[assets/figures/papers/paper_list_l1805_PhysicsFC_Learning_User_Controlled_Skills_for_a_Physics_Based_Football_P/figures/003_Figure_3.jpg]]
*Figure 3: Example of Dribble Policy Training with Skill Transition-Based State Initialization (STI): (a) Numerous episodes are simulated using trained skill policies, and the character and ball states are stored in STI buffers for each skill. (b) During Dribble policy training, half of the episodes are initialized with states randomly sampled from the Trap STI buffer, while the other half are initialized from the Move STI buffer. Through these episodes, the Dribble policy learns to initiate dribbling quickly in various situations, both while moving and immediately after trapping*

STI 的效果在过渡实验中极为显著：盘带到踢球过渡中，使用 STI 的踢球成功率（KSR）为 100%，而不使用 STI 仅 16.95%（Table 9）；移动到停球过渡中，停球成功率从 55.1% 提升至 74.1%（Table 8）。这表明 STI 使策略具备了从动态中间状态恢复的能力，而非仅能从精心设计的初始状态启动。

### 足球靴形碰撞网格

除奖励和训练机制外，物理建模层面的一个关键设计是采用**足球靴凸包碰撞体**替代默认的盒状脚部碰撞体（Figure 4）。实验表明，使用方形脚碰撞时，盘带策略无法学习方向调整，踢球速度偏差显著。靴形网格提供了更精确的足-球接触几何，是盘带和踢球技能得以成功学习的物理基础。

![[assets/figures/papers/paper_list_l1805_PhysicsFC_Learning_User_Controlled_Skills_for_a_Physics_Based_Football_P/figures/005_Figure_4.jpg]]
*Figure 4: Foot collision mesh*

## 实验与分析

### 核心实验设计

PhysicsFC的实验评估采用**全消融对照范式**，未引入外部基线方法。所有量化指标均为自定义指标，基于Isaac Gym Preview 4物理仿真环境（详细参数见Table 10）。评估围绕两大维度展开：（1）单项技能的独立性能；（2）技能间的过渡性能。四个核心技能——盘带（Dribble）、停球（Trap）、移动（Move）、踢球（Kick）——各自定义了专用评估指标。

**盘带策略**以目标达成率DGAR（Dribble Goal Achievement Rate）为核心指标，衡量球在水平面上速度与方向同时匹配目标盘带速度的比例。**停球策略**使用TSR（Trap Success Rate），评估球在与指定身体部位接触后速度降至阈值以下的比例。**移动策略**采用MGAR（Move Goal Achievement Rate）评估目标速度与朝向的达成率，同时引入GMLS（Goal-Matched Latent Similarity）评估运动真实感——即策略输出的潜变量与数据集中对应目标的速度片段所关联的参考潜变量之间的余弦相似度。**踢球策略**使用KSR（Kick Success Rate），衡量球在踢出后速度方向与目标方向偏差小于阈值的比例。

### 单项技能性能与消融分析

#### 盘带策略：早期终止是学习的关键瓶颈

盘带策略的消融实验（Table 1）揭示了**DistanceET（距离早期终止）机制的决定性作用**。完整模型在目标速度1.5 m/s下达到DGAR 90.3%，而移除DistanceET后骤降至2.0%——策略几乎完全无法学习盘带行为。DistanceET的核心机制是：当球与角色根节点的距离超过阈值（0.9 m）时提前终止回合，从而将策略的探索空间约束在近身控球的可行区域内。没有这一约束，策略在稀疏奖励环境中无法建立球控制与动作之间的因果关联。

![[assets/figures/papers/paper_list_l1805_PhysicsFC_Learning_User_Controlled_Skills_for_a_Physics_Based_Football_P/figures/014_Table_1.jpg]]
*Table 1: Comparison of our Dribble policy and its ablated models*

奖励项权重的消融进一步验证了多目标设计的必要性。单独移除球速度匹配奖励（w/o BallVel）使DGAR降至56.3%，移除球-根距离奖励（w/o BallRootPos）降至48.1%，移除根速度奖励（w/o RootVel）降至49.0%。三项奖励分别对应“球往哪走”、“球在哪”、“人往哪追”三个互补的控制目标，缺一不可。

Table 2展示了不同目标速度下的性能分化。在1.0-2.0 m/s范围内DGAR维持在86.2%-90.3%，但在2.5 m/s时降至67.4%，3.0 m/s时进一步降至56.8%。这表明当前策略在高速盘带场景下存在能力上限，可能与运动捕捉数据中高速盘带样本的稀缺以及物理约束下的步频限制有关。

#### 停球策略：抛射体初始化的关键作用

停球策略的消融（Table 3）表明，**基于抛射体动力学的球初始状态采样（ProjectileInit）是停球学习的核心使能技术**。完整模型的TSR为78.3%，移除ProjectileInit后降至21.1%。ProjectileInit通过解析计算确保球的落点位于角色可达半圆区域内（Figure 7），从而将训练信号集中在“如何用身体停球”而非“能否够到球”上。随机初始化则导致大量回合中球根本无法触及角色，训练信号被噪声淹没。

![[assets/figures/papers/paper_list_l1805_PhysicsFC_Learning_User_Controlled_Skills_for_a_Physics_Based_Football_P/figures/015_Table_3.jpg]]
*Table 3: Comparison of our Trap policy and its ablated models*

两阶段奖励结构同样重要：移除碰撞前奖励（w/o Before）使TSR降至56.5%，移除碰撞后速度匹配奖励（w/o After）降至51.0%。碰撞前阶段引导身体部位接近球，碰撞后阶段（持续1/6秒）引导角色吸收球的速度，两者分别对应停球动作的“迎接”和“缓冲”两个运动学阶段。

#### 移动策略：DEGCL提升运动质量

移动策略的核心发现是：**任务奖励（速度+朝向匹配）足以让策略学会到达目标，但不足以产生自然的运动模式**。Table 4显示，完整模型在MGAR上达到93.9%，而移除DEGCL的版本（w/o DEGCL）仍保持93.7%——任务完成度几乎不受影响。然而，GMLS从0.62降至0.52，表明运动质量显著退化。Figure 13的定性对比印证了这一点：无DEGCL的模型在后向移动时步频过高、步长过短，在侧向移动时反复出现近似侧倒的姿态。

DEGCL的核心机制是：在训练中交替使用一般随机目标回合和数据集参考目标回合，并在后者中施加潜变量相似度奖励 $r_t^{\mathrm{lt\_sim}} = \bar{\mathbf{z}}_t \cdot \mathbf{z}_t$。这相当于在策略优化中引入了一个“风格正则项”，约束策略输出的潜变量不偏离数据集中相似目标下的自然运动分布。

#### 踢球策略：目标速度归一化不可或缺

踢球策略的消融（Table 5）呈现了最极端的对比：完整模型KSR达到99.9%，而移除目标速度归一化（w/o NTS）后KSR为0.0%——**策略一次都没有成功踢到球**。NTS（Normalized Target Speed）将奖励中的速度误差除以目标速度的模长，使得不同目标速度下的奖励尺度保持一致。没有NTS时，高目标速度下的奖励梯度主导了优化过程，导致策略无法在低速目标下形成有效的踢球动作。

![[assets/figures/papers/paper_list_l1805_PhysicsFC_Learning_User_Controlled_Skills_for_a_Physics_Based_Football_P/figures/018_Table_5.jpg]]
*Table 5: Comparison of our Kick policy and its ablated models*

### 技能过渡性能与STI机制

PhysicsFC定义了四类技能过渡，每类均通过STI（Skill Transition-Based Initialization）与无STI基线进行对比（Tables 6-9）。

**盘带到踢球过渡**（Table 9）是STI效果最显著的场景：使用STI时KSR达到100%，而不使用STI仅16.95%。这一悬殊差距的原因在于：无STI时，踢球策略训练中从未见过盘带结束时的动态状态（球在运动中、角色在控球跑动），因此无法从盘带的终止状态泛化到踢球的起始条件。STI通过在踢球策略训练时从盘带STI缓冲区采样初始状态，使策略学会了从“边跑边带球”的中间状态直接发起踢球动作。

**停球到盘带过渡**（Table 6）中，STI将过渡时间TADG（Time After Dribble Goal achieved）从3.54秒缩短至2.71秒（加速23%），同时将DGAR从73.3%提升至94.1%。**移动到停球过渡**（Table 8）中，STI将TSR从55.1%提升至74.1%。**移动到盘带过渡**（Table 7）中，STI将DGAR从82.4%提升至95.4%。

STI的有效性源于一个简单的因果机制：强化学习策略对初始状态分布高度敏感。当训练分布与部署分布（即前序技能的终止状态）不匹配时，策略在过渡边界产生显著的分布外误差。STI通过构造与部署分布一致的训练初始状态分布，直接消除了这一分布偏移。

### 足球靴形碰撞网格的定性验证

论文在Section 4中报告了一项关键的物理建模发现：使用**足球靴凸包碰撞体**替代方形脚碰撞体（Figure 4），对于盘带和踢球技能的学习至关重要。方形脚碰撞下，盘带策略无法学习方向调整（球与平面碰撞的反弹方向不可控），踢球时球的出射速度方向偏差显著。这一发现揭示了接触几何在物理技能学习中的基础性作用——不精确的碰撞代理几何体会从根本上破坏接触丰富任务的奖励信号结构。

### 实验公平性与局限性

所有量化结果均来自消融对比，未与外部方法进行直接指标比较，因此无法判断PhysicsFC相对于其他足球角色控制方法的绝对性能优势。交互式场景（如11v11比赛、二过一配合）仅提供定性演示（Figures 10-12），缺乏客观的多人协作或对抗指标。仿真环境固定于Isaac Gym Preview 4，物理参数（Table 10）的敏感性未做系统分析，但论文附录提供了完整配置以便复现。此外，论文明确指出的局限性——包括盘带时单脚偏好、缺乏马格努斯效应、身体部位坐标偏差、高扭矩动作——均未在实验中量化评估其影响程度，这些需要后续工作验证。

### 补充图表

![[assets/figures/papers/paper_list_l1805_PhysicsFC_Learning_User_Controlled_Skills_for_a_Physics_Based_Football_P/figures/017_Table_4.jpg]]
*Table 4: Comparison of our Move policy and its ablated models*

![[assets/figures/papers/paper_list_l1805_PhysicsFC_Learning_User_Controlled_Skills_for_a_Physics_Based_Football_P/figures/022_Table_9.jpg]]
*Table 9: Comparison of Dribble-to-Kick transition performance with and without STI*

![[assets/figures/papers/paper_list_l1805_PhysicsFC_Learning_User_Controlled_Skills_for_a_Physics_Based_Football_P/figures/016_Figure_13.jpg]]
*Figure 13: Effect of DEGCL. (a), (b): For backward movement, the w/o DEGCL model shows excessively short step lengths and high step frequency compared to Ours. (c), (d): For sideways movement, the w/o DEGCL model repeatedly exhibits a posture that appears as if the character is about to fall sideways. In all figures, the character moves from left to right*

![[assets/figures/papers/paper_list_l1805_PhysicsFC_Learning_User_Controlled_Skills_for_a_Physics_Based_Football_P/figures/011_Figure_11.jpg]]
*Figure 11: Competitive trapping and dribbling*

![[assets/figures/papers/paper_list_l1805_PhysicsFC_Learning_User_Controlled_Skills_for_a_Physics_Based_Football_P/figures/012_Figure_12.jpg]]
*Figure 12: Simulated 11v11 football game with user-controlled player switching*

## 方法谱系与知识库定位

### 技术路线与继承关系

PhysicsFC 的核心架构建立在 **CALM**（Conditional Adversarial Latent Models）这一物理运动嵌入模型之上。CALM 在足球运动捕捉数据上预训练，将高维角色状态映射到低维潜变量空间，使得高层策略只需输出潜变量 $z$ 即可控制角色的低层物理动作。这种“高层策略 + 低层运动先验”的分层架构，继承了近年来基于物理的角色控制方法的主流范式，但将其首次系统性地应用于包含球体交互的足球多技能场景。

在技能训练层面，PhysicsFC 并未直接对标某个单一的外部基线方法，而是通过消融实验验证了各项设计选择的必要性。其技术增量主要体现在三个层面：

1. **技能专用化设计**：针对盘带、停球、移动、踢球四项技能，分别设计了差异化的奖励函数、回合初始化和终止条件。这种“一技能一策略”的分解思路，使得每项技能可以根据其物理特性进行精细调优，而非依赖单一通用策略覆盖所有行为。

2. **过渡平滑化机制**：**技能过渡初始化（STI）** 是 PhysicsFC 的核心贡献之一。该方法在训练阶段从前序技能策略的仿真轨迹中采样中间状态作为初始状态，使当前技能策略学会从各种非理想起始条件中恢复。这一设计解决了分层控制中长期存在的“技能切换时状态分布偏移”问题，其有效性在盘带到踢球过渡中尤为显著——使用 STI 的踢球成功率达 100%，而不使用 STI 仅 16.95%（Table 9）。

3. **运动质量引导**：**数据嵌入目标条件潜变量引导（DEGCL）** 通过从运动捕捉数据中提取目标-潜变量对，在移动策略训练中引入潜变量相似度奖励，使策略在完成速度/朝向目标的同时保持自然运动姿态。消融实验表明，移除 DEGCL 后潜变量相似度从 0.62 降至 0.52（Table 4），角色在侧向移动时出现“即将侧倒”的异常姿态（Figure 13）。

### 适用边界与局限

PhysicsFC 的设计选择决定了其适用边界：

- **仿真环境依赖**：所有训练和评估均在 Isaac Gym Preview 4 的特定物理配置下完成（Table 10 提供了详细参数）。仿真中未考虑马格努斯效应等复杂空气动力学，球的飞行轨迹与真实足球存在差异，可能影响长传、弧线球等高级技能的泛化。

- **角色模型精度**：身体部位（如肩部）的坐标通过绑定模拟计算，可能与视觉模型存在偏差，限制了胸部、肩部停球等精细接触的可靠性。论文明确指出这一局限可能影响停球策略在身体多部位接触场景中的表现。

- **生物力学合理性不足**：训练出的策略有时会产生高扭矩动作，可能与真实人体生物力学负荷不符。摔倒恢复动作可能出现突然的姿态变化，需要结合运动数据或肌骨模型进行改进。

- **单脚控球倾向**：盘带策略在训练中倾向于依赖单脚控球，未激励双脚的均衡使用。这限制了盘带动作的多样性和实战中的灵活性。

- **多智能体评估缺失**：11v11 比赛仿真（Figure 12）仅提供了定性演示，缺乏客观量化指标来评估整体足球表现。竞争性停球与盘带场景（Figure 11）同样未提供系统性的多智能体交互指标。

### 开放问题

PhysicsFC 为物理足球角色控制开辟了若干值得探索的方向：

- **双脚均衡控制**：如何设计奖励机制或课程学习策略，激励盘带策略自然地切换使用双脚，而非固化在单脚模式？

- **空气动力学建模**：在物理仿真中加入马格努斯效应，能否提升球轨迹的真实感，并解锁弧线球、电梯球等更复杂的踢球技能？

- **身体模型精度提升**：如何改进角色模型的身体部位坐标与视觉一致性，以更好地支持肩部、胸部等多部位停球？这是否需要引入更精细的碰撞体建模或基于视觉的接触检测？

- **运动自然性增强**：能否通过模仿学习或肌骨模型约束，在保持任务完成率的同时降低策略输出的扭矩，使动作更符合人体生物力学规律？

- **多智能体定量评估**：在更复杂的多智能体场景（如 2v2、11v11）中，如何设计标准化的定量评估指标来衡量整体足球表现，包括传球成功率、防守干扰下的控球稳定性等？

## 原文 PDF

![[paperPDFs/SIGGRAPH_2025/PhysicsFC_Learning_User_Controlled_Skills_for_a_Physics_Based_Football_Player_Controller.pdf]]
