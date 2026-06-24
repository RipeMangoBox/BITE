---
title: Physically Plausible Full Body Hand Object Interaction Synthesis
type: paper
paper_level: A
venue: 3DV
year: 2024
pdf_ref: paperPDFs/3DV_2024/Physically_Plausible_Full_Body_Hand_Object_Interaction_Synthesis.pdf
aliases:
- OPBHRMFBDG
- PPFBHOIS
tags:
- 3DV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过分层解耦训练的身体与手部技能先验，以及用于协调两者的目标引导机制，可以在物理仿真中稳定地完成抓取与轨迹跟随。
primary_logic: 将全身运动与精细手指控制分解到分别训练的对抗技能先验中，再由高层策略在潜空间内进行规划，既能避免统一训练的模式坍塌，又能借助物理仿真消除传统数据驱动方法的典型伪影。
claims:
- 解耦训练对任务至关重要：不分解身体与手部先验会导致潜空间模式坍塌，抓取成功率为零。
- 提出的方法在所有物理指标（地面距离、脚滑、穿透体积/深度）上均优于数据驱动基线，同时保持更高的抓取成功率。
- 目标引导技术进一步提升了轨迹跟随成功率，显式条件化与辅助损失使策略更鲁棒地跟随未见轨迹。
- GRAB (Approaching phase, unseen objects) 上 Grasp Success Rate = 0.79
---

# Physically Plausible Full Body Hand Object Interaction Synthesis

> [!tip] 核心洞察
> 将全身运动与精细手指控制分解到分别训练的对抗技能先验中，再由高层策略在潜空间内进行规划，既能避免统一训练的模式坍塌，又能借助物理仿真消除传统数据驱动方法的典型伪影。

| 字段 | 内容 |
|------|------|
| 中文题名 | 物理可信的全身手-物体交互合成 |
| 英文题名 | Physically Plausible Full Body Hand Object Interaction Synthesis |
| 会议/期刊 | 3DV 2024 |
| Links | [Project](https://eth-ait.github.io/physfullbody-grasp/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Our physics-based hierarchical RL method for full-body dexterous grasping |
| Dataset | GRAB |

> [!tip] 效果简介
> - GRAB (Approaching phase, unseen objects) 上，Grasp Success Rate 0.79 vs GOAL: 0.55, IMoS: 0.56 (+0.24 / +0.23)。
> - GRAB (Manipulation phase, GOAL test split) 上，Grasp Success Rate 0.79 vs N/A (kinematic baselines evaluated differently) (N/A)。
> - GRAB (Approaching phase) 上，Ground Distance (GD) [mm] ↓ 2.1 vs GOAL: 3.8, IMoS: 4.1 (-1.7 / -2.0)。

## 概述

生成物理可信的全身手-物体交互序列是具身智能与角色动画领域的核心挑战。现有数据驱动方法——如运动学合成框架 **GOAL** 与 **IMoS**——能够生成视觉上合理的全身抓取动作，却普遍存在脚滑、地面穿透、手-物体相互穿透等物理伪影。另一方面，基于物理仿真的方法虽能缓解此类伪影，但要么仅关注粗粒度的身体-物体交互，要么局限于孤立的手部灵巧抓取（如 **D-Grasp**），尚未实现全身协调运动与精细手指操控的物理级统一。

本文提出首个基于物理仿真的全身灵巧抓取方法，其核心瓶颈与突破可归纳如下：

- **瓶颈**：将高维全身运动（105 自由度）与精细手指控制统一在单一策略中训练极易导致模式坍塌，抓取成功率为零。
- **核心机制**：将全身运动与手指控制**解耦**为分别训练的对抗技能先验（身体先验与手先验），再由一个高层手-物交互策略在两者的潜空间内进行规划。这一分层设计既避免了统一训练的模式坍塌，又借助刚体物理仿真从根本上消除了运动学方法中常见的穿透与脚滑伪影。
- **关键证据**：在 GRAB 数据集上的实验表明，本文方法在接近阶段的抓取成功率达 **0.79**，较 GOAL（0.55）和 IMoS（0.56）提升约 24%；同时物理指标全面占优——地面距离（GD）降至 **2.1 mm**（GOAL: 3.8, IMoS: 4.1），脚滑率（FS）仅为 **0.9%**（GOAL: 6.2%, IMoS: 5.1%）。消融实验证实，移除身体与手先验的解耦训练直接导致抓取成功率为零，而两阶段训练与目标引导技术各自对成功率有显著贡献。

**方法定位**：本文属于物理仿真驱动的分层强化学习范式，其方法谱系可置于 Table 1 的四维空间——在 Full Body、Physics、Whole Interaction、Dexterous Grasping 四个维度上首次实现全面覆盖。与纯运动学方法（GOAL、IMoS）相比，其核心差异在于引入了 Isaac Gym 刚体仿真与 PD 控制器驱动的物理约束；与物理抓取方法（D-Grasp）相比，其将控制范围从孤立手部扩展至全身协调；与粗粒度物理交互方法相比，其通过解耦手先验实现了灵巧手指操控。目标引导机制（通过辅助轨迹损失 $\mathcal{L}_{\xi} = ||\overline{\pmb{\xi}} - \tilde{\pmb{\xi}}||_2^2$ 显式条件化）进一步使策略能够跟随未见过的腕部与根轨迹，实现了灵活的任务级控制。

**局限与展望**：当前方法仅支持单一中性身体形状，对大尺寸物体的抓取性能下降，且依赖静态手部姿态参考来控制抓取方式，尚未支持语言或语义指令驱动的交互生成。如何纳入多样化身体形态、提升仿真精度以减少残余穿透、以及摆脱对参考抓取姿态的依赖，是未来研究的重要方向。

## 背景与动机

### 问题背景

生成真实可信的人类运动是计算机视觉与图形学的核心挑战之一。当任务从孤立的身体运动扩展到**全身手-物交互**时，问题难度急剧上升：系统必须同时协调身体位移、手臂运动与灵巧手指操控，并在物理层面保持一致性。传统数据驱动方法（如基于运动学模型的动作合成）虽然能够产生视觉上流畅的序列，但往往缺乏物理约束，导致**脚滑、地面穿透、手-物穿透**等典型伪影。这些伪影不仅降低视觉真实感，更使生成的运动无法直接用于机器人学习或物理仿真环境。

### 现有方法的缺口

**基于运动学的全身抓取方法**，如 **GOAL** 和 **IMoS**，直接从数据中回归身体与手部姿态，能够生成多样化的交互序列，但它们不包含物理仿真环节。这意味着生成的抓取姿态在动力学上可能不成立——物体可能漂浮、手指可能穿透物体表面、脚与地面的接触缺乏摩擦力约束。这些方法在物理指标上表现不佳：例如在 GRAB 数据集上，GOAL 和 IMoS 的脚滑率分别达到 6.2% 和 5.1%，而地面距离误差也显著偏高。

**基于物理的方法**则走向了另一个极端。以 **D-Grasp** 为代表的工作专注于孤立手部的灵巧抓取，在物理仿真中实现了稳定的手指操控，但完全忽略了身体运动。另一类工作（如 **Hassan et al.**）在物理仿真中处理粗粒度的身体-物体交互，但手部被简化为刚体或仅做粗略建模，无法实现精细的手指控制。**Table 1** 的方法对比清晰地揭示了这一断层：现有工作要么覆盖“全身+物理”但缺乏灵巧抓取，要么覆盖“灵巧抓取+物理”但仅限于手部，没有方法同时实现物理仿真下的全身协调与精细手指操控。

### 核心瓶颈

这一断层的根本原因在于**统一训练的困难**：将全身运动与精细手指控制纳入单一策略进行端到端强化学习，极易导致潜空间的**模式坍塌**。身体运动的自由度远高于手部，且两者的动力学特性差异巨大，联合训练时策略往往会忽略手指控制而只关注粗粒度的身体平衡，抓取成功率降为零（见 **Table 3** 消融实验）。因此，如何在学习框架中有效分解这两类运动技能，同时保证它们在执行时协调一致，成为突破瓶颈的关键。

### 本文动机与核心思路

本文提出首个**基于物理的全身灵巧抓取方法**，核心思路是**分层解耦**：

1. **技能先验解耦**：将全身运动与精细手指控制分解到分别训练的对抗技能先验中——身体先验负责躯干与手臂的协调运动，手先验负责手指的灵巧操控。两者在预训练阶段完全独立，避免模式坍塌。
2. **高层策略协调**：在解耦先验的潜空间之上，训练一个高层手-物交互策略，通过预测身体与手部的潜变量来协调两者的行为，同时引入**目标引导机制**使策略能够灵活跟随任意手腕与根轨迹。
3. **物理仿真消除伪影**：整个系统运行在刚体物理仿真中，通过 PD 控制器将策略输出的残差动作与参考姿态结合，计算关节力矩驱动角色。物理约束自然消除了脚滑和穿透问题。

这一设计使得方法既保留了数据驱动方法的运动自然性（通过对抗模仿奖励），又获得了物理仿真的真实交互特性，首次在全身灵巧抓取任务上同时实现了高成功率和低物理误差。

## 核心创新

本文的核心突破在于**首次将物理仿真引入全身灵巧抓取任务**，解决了现有数据驱动方法普遍存在的脚滑、穿透等物理伪影问题。此前的运动合成方法可分为两类：基于运动学的方法（如 **GOAL** 和 **IMoS**）能够生成全身手-物交互序列，但缺乏物理约束，导致地面穿透和手-物穿透严重；基于物理的方法（如 **D-Grasp** 仅处理孤立手部抓取，Hassan et al. 仅关注粗粒度身体-物体交互）则未能同时实现全身协调与灵巧手指操控。本文的方法填补了这一空白（Table 1），其关键创新体现在以下三个相互关联的设计上。

### 1. 解耦的身体与手部技能先验

第一个核心创新是将全身运动与精细手指控制**分解到两个独立训练的对抗技能先验中**。身体先验（Body Prior）负责躯干、手臂等 57 个自由度的运动技能，手部先验（Hand Prior）则专注于 48 个手指自由度的灵巧操控。两者均采用结合运动模仿与无监督技能发现（unsupervised skill discovery）的对抗训练范式，奖励函数形式为：

$$r = - \log ( 1 - D ( \phi ( \mathbf { s } ) , \phi ( \mathbf { s } ^ { \prime } ) ) + \beta \log q ( \mathbf { z } _ { t } \mid \phi ( \mathbf { s } ) , \phi ( \mathbf { s } ^ { \prime } ) )$$

其中判别器 $D$ 区分参考运动与生成运动以提供模仿奖励，第二项则鼓励潜编码 $z_t$ 可从状态转移中恢复，从而促进技能空间的覆盖。

**这一解耦设计是任务成功的关键瓶颈**。消融实验（Table 3）表明，若将身体与手部先验合并为单一先验进行训练，潜空间会发生模式坍塌（mode collapse），抓取成功率直接降为零。其因果机制在于：全身运动与手指操控的动作分布差异巨大，统一训练时判别器容易被某一模态主导，导致策略丧失对另一模态的探索能力。解耦后，两个先验各自在低维潜空间中形成结构化的技能表示，为高层策略提供了稳定且可组合的动作原语。

### 2. 分层规划与高层手-物交互策略

第二个创新是**在预训练先验之上构建高层手-物交互策略**（hand-object interaction policy $\pi_{ho}$），该策略在身体和手部先验的潜空间内进行规划，而非直接输出关节动作。具体而言，$\pi_{ho}$ 接收身体特征 $\phi_b(\mathbf{s})$、手部特征 $\phi_h(\mathbf{s})$ 以及手-物交互特征 $\phi_{ho}(\mathbf{s}, \Psi, \xi)$，输出潜向量 $\mathbf{z}_b$ 和 $\mathbf{z}_h$，分别由身体和手部先验解码为具体的关节目标角度。

手-物交互特征 $\phi_{ho}$ 的设计是实现灵巧抓取与轨迹跟随的关键，包含物体姿态与速度、手部到参考姿态的距离误差、接触目标、轨迹路径点、接触力、桌面距离以及相位变量等丰富信息。这使得策略能够同时感知抓取进度和导航目标。

任务奖励 $r_T$ 进一步细化为姿态误差、接触、轨迹跟随和正则项的加权和：

$$r_T = r_x + r_\theta + r_c + r_\xi + r_{\mathrm{reg}}$$

而风格奖励 $r_S$ 则分别对全身和手部运动使用独立的判别器，鼓励生成动作保持自然性：

$$r_S = - \log ( 1 - D_b ( \phi_b ( \mathbf{s} ), \phi_b ( \mathbf{s}' ) ) ) - \log ( 1 - D_h ( \phi_h ( \mathbf{s} ), \phi_h ( \mathbf{s}' ) ) )$$

最终的总奖励为 $r_{\mathrm{HO}} = w_T r_T + w_S r_S$。这种分层设计使得高层策略只需关注任务级决策，而将运动执行的细节交由预训练先验处理，显著降低了强化学习的探索难度。

### 3. 目标引导机制

第三个创新是**目标引导（Target Guidance）技术**，用于提升策略对未见轨迹的跟随鲁棒性。在训练过程中，$\pi_{ho}$ 除了输出潜向量外，还额外预测根节点和手腕的目标位置 $\tilde{\pmb{\xi}}$。训练时交替使用真实目标 $\overline{\pmb{\xi}}$ 和预测目标 $\tilde{\pmb{\xi}}$ 作为条件输入，并通过辅助损失约束预测精度：

$$\mathcal{L}_{\xi} = || \overline{\pmb{\xi}} - \tilde{\pmb{\xi}} ||_2^2$$

这一设计的因果机制是：通过显式条件化轨迹信息并施加预测监督，策略学会将轨迹目标内化为自身规划的组成部分，而非被动跟随外部信号。消融实验（Table 3）证实，目标引导进一步提升了轨迹跟随的成功率，使策略在面对训练中未见过的轨迹时表现更为鲁棒。

### 创新总结

上述三个创新构成了一个完整的因果链条：**解耦先验**防止模式坍塌，为复杂技能提供稳定的表示基础；**分层规划**将任务决策与运动执行分离，降低了学习难度；**目标引导**增强了策略对空间目标的泛化能力。三者的协同使得本文方法在 GRAB 数据集上实现了 0.79 的抓取成功率（相比 GOAL 的 0.55 和 IMoS 的 0.56），同时将地面距离降至 2.1 mm（GOAL: 3.8 mm, IMoS: 4.1 mm），脚滑比例降至 0.9%（GOAL: 6.2%, IMoS: 5.1%），在物理可信度上实现了数量级的提升。

## 整体框架

本文提出一种基于物理仿真的分层强化学习框架，用于生成物理可信的全身手-物体交互序列。框架的核心设计思路是**解耦全身运动与精细手指控制**：将两者分别建模为独立的低层技能先验（skill priors），再由一个高层策略在潜空间内进行协调规划。这种解耦设计避免了统一训练时潜空间的模式坍塌，同时借助物理仿真消除了传统数据驱动方法中常见的脚滑、穿透等伪影。

### 输入与输出

框架的输入由两部分组成：

- **手-物姿态参考** $\Psi = ( \overline{\pmb{\theta}}_h, \overline{\mathbf{t}}_h^0, \overline{\mathbf{T}}_o )$：一帧静态的手部抓取参考，包含目标手腕旋转、手腕平移以及参考物体位姿，用于定义“如何抓取”；
- **根与手腕目标轨迹** $\xi$：一系列定义身体根部和手腕在空间中移动方式的路径点，用于指定“抓取后如何移动”。

框架的输出是一段完整的全身运动序列，涵盖从接近物体、抓取到沿轨迹操纵物体的全过程。生成的序列在 Isaac Gym 刚体仿真环境中运行，由 PD 控制器驱动 105 个自由度的 SMPL-X 人体模型（身体 57 DoF + 手指 48 DoF）。

### 模块关系与数据流

整个 pipeline 由三个核心模块构成，按训练与推理的层级关系组织如下：

**1. 身体先验策略（Body Prior Policy）**  
该模块是一个目标条件化的低层技能先验，在预训练阶段从全身运动捕捉数据中学习多样化的身体运动技能。它以身体状态特征 $\phi_b(\mathbf{s})$ 和潜编码 $\mathbf{z}_b$ 为输入，解码输出身体关节（不含手部）的残差动作。训练采用对抗模仿与无监督技能发现的组合目标，奖励函数为：

$$r = - \log ( 1 - D ( \phi ( \mathbf { s } ) , \phi ( \mathbf { s } ^ { \prime } ) ) + \beta \log q ( \mathbf { z } _ { t } \mid \phi ( \mathbf { s } ) , \phi ( \mathbf { s } ^ { \prime } ) )$$

其中判别器 $D$ 区分生成运动与参考运动的差异以提供模仿奖励，后验 $q$ 则鼓励潜编码的可恢复性以实现技能发现。

**2. 手部先验策略（Hand Prior Policy）**  
与身体先验对称，该模块在孤立右手数据上训练，学习手指与手腕的精细操控技能。它以手部状态特征 $\phi_h(\mathbf{s})$ 和潜编码 $\mathbf{z}_h$ 为输入，解码输出手指关节的残差动作。身体与手先验的关键区别在于**解耦训练**：两者使用独立的判别器与潜空间，互不共享参数，从而避免模式坍塌（消融实验证实，若不解耦，抓取成功率降为零）。

**3. 手-物交互策略（Hand-Object Interaction Policy）**  
这是框架的高层规划策略 $\pi_{\mathrm{ho}}$，在预训练好的身体与手先验之上运行。该策略以身体特征 $\phi_b(\mathbf{s})$、手部特征 $\phi_h(\mathbf{s})$ 以及任务相关的手-物特征 $\phi_{\mathrm{ho}}(\mathbf{s}, \Psi, \xi)$ 为输入，输出四个量：

- 身体潜编码 $\mathbf{z}_b$：传递给身体先验以控制全身运动；
- 手部潜编码 $\mathbf{z}_h$：传递给手先验以控制手指动作；
- 预测的根目标 $\tilde{\mathbf{t}}_b$ 和手腕目标 $\tilde{\mathbf{t}}_h$：用于目标引导机制。

手-物特征 $\phi_{\mathrm{ho}}$ 编码了抓取与轨迹跟随所需的关键信息，包括物体位姿与速度、手部到参考姿态的距离、接触目标、轨迹路径点、接触力、桌面距离以及运动相位。

**4. PD 控制器**  
所有策略输出的残差动作 $\mathbf{a}$ 与参考姿态相加得到目标关节角度，再由 PD 控制器计算关节力矩：

$$\hat{\pmb{\theta}} = \pmb{\theta}_{\mathrm{ref}} + k_s \mathbf{a}$$

$$\pmb{\tau} = k_p \circ (\hat{\pmb{\theta}} - \pmb{\theta}) - k_d \dot{\pmb{\theta}}$$

### 训练流程

训练采用两阶段策略：

- **第一阶段（静态抓取预训练）**：手-物交互策略仅学习接近并稳定抓取物体，不涉及轨迹跟随；
- **第二阶段（轨迹跟随微调）**：在抓取成功的基础上引入轨迹跟随目标，联合优化抓取稳定性与轨迹精度。

消融实验表明，两阶段训练使成功率提升约 24%。此外，**目标引导技术**（Target Guidance）在第二阶段交替使用真实轨迹 $\overline{\pmb{\xi}}$ 与策略预测轨迹 $\tilde{\pmb{\xi}}$ 进行条件化，并引入辅助损失 $\mathcal{L}_{\xi} = ||\overline{\pmb{\xi}} - \tilde{\pmb{\xi}}||_2^2$，进一步提升了策略对未见轨迹的跟随鲁棒性。

手-物交互策略的总奖励由任务奖励 $r_T$（姿态误差、接触、轨迹跟随、正则项）和风格奖励 $r_S$（身体与手部分别使用判别器评估运动自然度）加权组合：

$$r_{\mathrm{HO}} = w_T r_T(\mathbf{s}, \mathbf{a}) + w_S r_S(\mathbf{s})$$

$$r_S = -\log(1 - D_b(\phi_b(\mathbf{s}), \phi_b(\mathbf{s}'))) - \log(1 - D_h(\phi_h(\mathbf{s}), \phi_h(\mathbf{s}')))$$

### 框架定位

Table 1 从四个维度将本文方法置于现有工作的坐标系中：**全身性**（Full Body）、**物理仿真**（Physics）、**完整交互**（Whole Interaction，含接近与操纵）、**灵巧抓取**（Dexterous Grasping）。此前的方法要么仅覆盖其中两到三个维度——例如 GOAL 和 IMoS 是运动学全身方法但无物理仿真，D-Grasp 是物理仿真灵巧抓取但仅限手部，Hassan et al. 处理物理仿真全身交互但缺乏精细手指控制——本文是首个同时满足全部四个维度的工作。

### 补充图表

![[assets/figures/papers/paper_list_l1657_Physically_Plausible_Full_Body_Hand_Object_Interaction_Synthesis/figures/003_Figure_2.jpg]]
*Figure 2: Method Overview. Given a hand-object pose reference Ψ and a root and wrist target trajectory*

## 核心模块与公式推导

### 1. 仿真环境与关节驱动

方法基于 Isaac Gym 刚体物理仿真环境构建。人体模型包含 57 个身体关节自由度和 48 个手指关节自由度，共计 105 个驱动自由度。关节驱动力矩由比例-微分（PD）控制器计算：

$$\pmb{\tau} = k_p \circ (\hat{\pmb{\theta}} - \pmb{\theta}) - k_d \dot{\pmb{\theta}}$$

其中 $\pmb{\theta}$ 和 $\dot{\pmb{\theta}}$ 分别为当前关节角度和角速度，$k_p$ 和 $k_d$ 为 PD 控制器的增益参数。目标关节角度 $\hat{\pmb{\theta}}$ 由参考姿态与策略输出的残差动作组合而成：

$$\hat{\pmb{\theta}} = \pmb{\theta}_{\mathrm{ref}} + k_s \mathbf{a}$$

这里 $\pmb{\theta}_{\mathrm{ref}}$ 是从运动捕捉数据中获取的参考关节角度，$\mathbf{a}$ 是策略网络输出的残差动作，$k_s$ 是缩放因子。这种“参考姿态 + 残差”的设计使策略能够在运动学参考附近进行物理修正，既保持了动作的自然性，又允许仿真器根据接触力和动力学约束进行必要的调整。

### 2. 分层控制架构

整体框架采用分层强化学习设计，分为低层技能先验和高层交互策略两个层级。

**低层技能先验**负责将潜空间编码解码为具体的关节运动。身体先验和手先验分别独立训练，各自学习从潜向量到关节动作的映射。这种解耦设计是方法的核心创新——统一训练单一先验会导致潜空间模式坍塌，使抓取成功率降为零（Table 3）。

**高层手-物交互策略** $\pi_{\mathrm{ho}}$ 在预训练好的身体和手先验的潜空间内进行规划。其输入包括身体特征 $\phi_b(\mathbf{s})$、手部特征 $\phi_h(\mathbf{s})$ 以及任务相关的手-物特征 $\phi_{\mathrm{ho}}(\mathbf{s}, \Psi, \xi)$，输出为身体潜向量 $\mathbf{z}_b$、手潜向量 $\mathbf{z}_h$，以及辅助的身体根部和手腕目标位置预测 $\tilde{\mathbf{t}}_b, \tilde{\mathbf{t}}_h$。

手-物特征 $\phi_{\mathrm{ho}}$ 是高层策略感知任务上下文的关键，具体包含：

$$\phi_{\mathrm{ho}}(\mathbf{s}, \Psi, \xi) = (\mathbf{T}_o, \dot{\mathbf{T}}_o, \mathbf{g}_x, \mathbf{g}_\theta, \mathbf{g}_c, \mathbf{g}_\xi, \mathbf{f}_h, d_{\mathrm{table}}, \varphi)$$

各分量的含义为：$\mathbf{T}_o$ 和 $\dot{\mathbf{T}}_o$ 是物体的位姿和速度；$\mathbf{g}_x$ 和 $\mathbf{g}_\theta$ 是手部相对于参考抓取姿态的位置和旋转误差；$\mathbf{g}_c$ 是指定接触点的接触状态；$\mathbf{g}_\xi$ 是当前手腕位置与目标轨迹点的偏差；$\mathbf{f}_h$ 是手部受到的接触力；$d_{\mathrm{table}}$ 是手到桌面的距离；$\varphi$ 是运动相位变量，用于编码周期性步态信息。

### 3. 技能先验的对抗训练

身体和手先验的训练结合了运动模仿和无监督技能发现两个目标，其奖励函数为：

$$r = -\log(1 - D(\phi(\mathbf{s}), \phi(\mathbf{s}'))) + \beta \log q(\mathbf{z}_t \mid \phi(\mathbf{s}), \phi(\mathbf{s}'))$$

第一项是判别器 $D$ 给出的模仿奖励，判别器学习区分参考运动数据和策略生成的状态转移对 $(\phi(\mathbf{s}), \phi(\mathbf{s}'))$，策略则试图“欺骗”判别器以产生与参考数据分布一致的运动。第二项是技能发现项，其中 $q$ 是一个从状态转移中恢复潜编码 $\mathbf{z}_t$ 的后验网络，通过最大化潜编码的可恢复性来鼓励策略产生多样化的运动技能。$\beta$ 是两项之间的平衡系数。

身体先验额外引入目标条件化：以身体根部和手腕的目标位置为条件，使先验能够根据高层指令生成相应的全身运动。手先验则在孤立的右手模型上训练，专注于灵巧手指运动的技能学习。

### 4. 高层策略的奖励设计

高层手-物交互策略的总奖励由任务奖励和风格奖励加权组合：

$$r_{\mathrm{HO}} = w_T r_T(\mathbf{s}, \mathbf{a}) + w_S r_S(\mathbf{s})$$

**任务奖励** $r_T$ 进一步分解为五个子项：

$$r_T = r_x + r_\theta + r_c + r_\xi + r_{\mathrm{reg}}$$

- $r_x$：手部关键点位置误差的负值，驱动手部接近参考抓取位置；
- $r_\theta$：手部关节旋转误差的负值，确保抓取姿态的准确性；
- $r_c$：接触奖励，鼓励指定手指区域与物体建立并维持接触；
- $r_\xi$：轨迹跟随奖励，衡量手腕位置与目标轨迹点的接近程度；
- $r_{\mathrm{reg}}$：正则化项，惩罚过大的关节加速度和接触力，保证运动平滑。

**风格奖励** $r_S$ 采用与先验训练类似的判别器结构，但分别对身体和手部运动使用独立的判别器：

$$r_S = -\log(1 - D_b(\phi_b(\mathbf{s}), \phi_b(\mathbf{s}'))) - \log(1 - D_h(\phi_h(\mathbf{s}), \phi_h(\mathbf{s}')))$$

$D_b$ 和 $D_h$ 分别判别全身运动和手部运动的自然程度，两者联合优化确保生成的交互序列在整体协调性和手指精细程度上都符合参考数据的分布。

### 5. 目标引导机制

为使策略能够灵活跟随用户指定的手腕和身体根部轨迹，方法引入了目标引导技术。高层策略在预测潜向量 $\mathbf{z}_b, \mathbf{z}_h$ 的同时，额外输出身体根部和手腕的目标位置预测 $\tilde{\pmb{\xi}} = (\tilde{\mathbf{t}}_b, \tilde{\mathbf{t}}_h)$。训练时，以一定概率在真实目标 $\overline{\pmb{\xi}}$ 和策略预测目标 $\tilde{\pmb{\xi}}$ 之间交替作为身体先验的条件输入，并施加辅助损失：

$$\mathcal{L}_{\xi} = ||\overline{\pmb{\xi}} - \tilde{\pmb{\xi}}||_2^2$$

这一设计使策略学会预测合理的子目标，同时在推理时能够接受用户指定的轨迹作为条件。消融实验（Table 3）表明，目标引导技术对轨迹跟随的鲁棒性有显著贡献。

### 6. 两阶段训练策略

高层策略的训练分为两个阶段：
- **第一阶段（静态抓取）**：仅优化抓取成功率，不引入轨迹跟随目标，使策略首先学会稳定接近并抓取物体；
- **第二阶段（轨迹跟随）**：在抓取能力基础上引入轨迹跟随奖励 $r_\xi$ 和目标引导机制，联合优化抓取与跟随。

消融实验（Table 3）表明，两阶段训练使成功率提升约 24%。直接联合训练所有目标会导致优化困难，策略难以同时学会抓取和跟随两个具有不同时间尺度的子任务。

## 实验与分析

### 评估设置与基线

本文在 **GRAB** 数据集上评估所提出的物理可信全身手-物交互合成方法。评估分为两个阶段：**接近直至抓取**（Approaching until grasping）和**抓取后操纵**（Manipulation after grasping）。前者测试智能体在未见物体上完成接近和稳定抓取的能力，后者进一步要求智能体在抓取物体后跟随指定的根节点与腕部轨迹进行移动。

对比基线涵盖运动学方法与物理方法两类：
- **GOAL**：运动学全身抓取运动合成方法，不运行物理仿真。
- **IMoS**：运动学全身物体操纵合成方法，同样为纯运动学生成。
- **D-Grasp**：基于物理的灵巧手抓取方法，仅处理孤立手部，不含全身运动。
- **Hassan et al.**：基于物理的粗粒度身体-物体交互方法，不涉及手指级灵巧操控。

需要指出公平性问题：运动学基线不运行物理仿真，其抓取成功率是通过在固定抓取姿态下运行物理仿真仅验证抓取稳定性得到的，评估协议与本文方法不完全对等。此外，穿透体积和地面距离等物理指标受刚体仿真中网格近似的影响，在 SMPL-X 参数空间中并不严格为零，论文对此进行了明确说明。

### 主要定量结果

**接近阶段**（Table 2 Approaching）：本文方法在抓取成功率上达到 **0.79**，显著优于 GOAL（0.55）和 IMoS（0.56），提升幅度分别达 +0.24 和 +0.23。在物理可信度指标上，地面距离（GD）降至 **2.1 mm**（GOAL: 3.8 mm, IMoS: 4.1 mm），脚滑率（FS）仅为 **0.2%**，而两个运动学基线分别为 0.5% 和 0.4%。手-物穿透体积（PV）和穿透深度（PD）也全面优于基线。

**操纵阶段**（Table 2 Manipulation）：在 S10 测试集上，本文方法抓取成功率为 **0.64**，脚滑率降至 **0.9%**（GOAL: 6.2%, IMoS: 5.1%），降幅超过 4 个百分点。在 GOAL 测试集上，成功率达到 **0.79**，地面距离为 1.9 mm，穿透深度仅为 0.2 mm。这些结果表明，物理仿真有效消除了数据驱动方法中常见的脚滑和穿透伪影，同时保持了较高的任务成功率。

**轨迹跟随评估**（Table 5）：在 GOAL 测试集上（物体和轨迹均未见于训练），本文方法平均成功率为 0.79，轨迹目标达成率（TTR）按物体类别在 0.66 至 0.91 之间，表明策略能够泛化到未见轨迹。

### 消融实验

Table 3 系统消融了三个核心设计组件：

![[assets/figures/papers/paper_list_l1657_Physically_Plausible_Full_Body_Hand_Object_Interaction_Synthesis/figures/007_Table_3.jpg]]
*Table 3: Ablations. We ablate the components of our method. The decoupling of priors is crucial to solve the task, while the two-stage training procedure and target guidance each contribute to higher success rates in grasping and trajectory following*

1. **解耦训练（Decoupling）**：移除身体与手先验的解耦训练，改为联合训练单一先验，导致潜空间模式坍塌，抓取成功率为零。该结果证实解耦是任务可解的前提条件。
2. **两阶段训练（Two-stage training）**：跳过两阶段训练（先学静态抓取再学轨迹跟随），直接进行端到端训练，成功率下降约 24%。这表明分阶段课程学习对稳定抓取策略至关重要。
3. **目标引导（Target guidance）**：移除目标引导机制（显式条件化与辅助轨迹预测损失 $L_{\xi} = ||\overline{\pmb{\xi}} - \tilde{\pmb{\xi}}||_2^2$），策略在跟随未见轨迹时的鲁棒性下降，轨迹跟随成功率降低。

此外，Table 4 考察了高斯平滑的影响：移除高斯平滑后，脚滑率和穿透指标略有上升，但抓取成功率和 TTR 不受影响（因为这些指标在物理仿真中评估，平滑仅影响渲染到 SMPL-X 网格的视觉质量）。

![[assets/figures/papers/paper_list_l1657_Physically_Plausible_Full_Body_Hand_Object_Interaction_Synthesis/figures/008_Table_4.jpg]]
*Table 4: Evaluation. We evaluate our model without Gaussian smoothing (w/o smoothing) and compare with the results from the main paper. Note that the success rate and trajectory targets reached (TTR) are not affected as they are evaluated in the physics simulation*

### 定性分析

**Figure 3** 展示了在未见测试物体上生成的连续交互序列，每行对应一个完整动作：从接近物体、抓取到沿轨迹移动，动作自然连贯。

**Figure 4** 提供了与运动学基线的定性对比：基于物理的方法生成的运动中，手与物体之间、身体与地面之间的穿透明显少于运动学基线。这直观体现了物理仿真在消除穿透伪影方面的优势。

### 失败模式与局限性

尽管整体表现优异，方法仍存在以下失败模式：
- **大尺寸物体**：当物体尺寸较大、手指需要完全伸展才能抓握时，策略性能下降，抓取成功率降低。
- **穿透残留**：为加速仿真对物体网格和身体形状进行了减面处理，转换回 SMPL-X 参数空间时仍会产生轻微穿透伪影。
- **身体形状单一**：仅使用中性身体形状训练，未覆盖不同人体形态，限制了方法的泛化性。
- **抓取多样性受限**：依赖静态手部姿态参考 $\Psi$ 来控制抓取方式，可能约束抓取姿态的多样性。
- **交互模态有限**：不支持基于语言或语义命令的交互生成，无法响应高层任务描述。

### 方法谱系与知识库定位

Table 1 从四个维度系统定位了本文贡献：**Full Body**（全身运动）、**Physics**（物理仿真）、**Whole Interaction**（完整交互过程）、**Dexterous Grasping**（灵巧抓取）。现有方法仅覆盖其中部分维度：GOAL 和 IMoS 实现全身运动学合成但无物理仿真；D-Grasp 实现物理灵巧抓取但仅限手部；Hassan et al. 实现物理全身交互但无手指级操控。本文是首个同时满足全部四个维度的方法。

![[assets/figures/papers/paper_list_l1657_Physically_Plausible_Full_Body_Hand_Object_Interaction_Synthesis/figures/002_Table_1.jpg]]
*Table 1: Method Comparison. We put our method into context with kinematics-based and physics-based approaches. Our method is the first to achieve physics-based full-body dexterous grasping*

在技术路线上，本文继承了对抗技能嵌入（ASE）的框架，但通过**分层解耦**将全身运动与精细手指控制分解到分别训练的对抗技能先验中，再由高层策略在潜空间内进行协调规划。这种设计避免了统一训练中的模式坍塌问题，同时借助物理仿真消除了传统数据驱动方法的典型伪影。目标引导机制进一步通过显式轨迹条件化和辅助预测损失增强了策略对未见轨迹的泛化能力。

### 补充图表

![[assets/figures/papers/paper_list_l1657_Physically_Plausible_Full_Body_Hand_Object_Interaction_Synthesis/figures/005_Table_2.jpg]]
*Table 2: Evaluation. We compare our method against the relevant baselines on approaching until grasping and manipulation after grasping. In both settings, we find that our method achieves better performance across all of the metrics. We also provide the metrics for the groundtruth motion capture data (GT) as reference. Notably, our method can correct artifacts present in motion capture data, such as ground penetration or floating. The success rates show that our method leads to most stable grasps in the physics simulation. * The ground distance (GD) in the SMPL-X space is not zero as a consequence of the rigid body approximation of the human in the physics simulation. This metric equates to 0.0 when...*

![[assets/figures/papers/paper_list_l1657_Physically_Plausible_Full_Body_Hand_Object_Interaction_Synthesis/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative Comparison. Our physics-based method generates motions that exhibit less hand-object interpenetration and ground interpenetration than the kinematics baselines*

![[assets/figures/papers/paper_list_l1657_Physically_Plausible_Full_Body_Hand_Object_Interaction_Synthesis/figures/001_Figure_1.jpg]]
*Figure 1: Our method generates physically plausible full-body hand-object interaction sequences. We can synthesize sequences with unseen objects while following a flexibly definable wrist trajectory (left). We can also generate motions of approaching an object, grasping it, then walking to a different location while lifting the object (middle, right). The target trajectories are indicated by the dashed lines*

![[assets/figures/papers/paper_list_l1657_Physically_Plausible_Full_Body_Hand_Object_Interaction_Synthesis/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative Results. Each row shows a motion sequence generated by our model for an unseen object from the test set*

![[assets/figures/papers/paper_list_l1657_Physically_Plausible_Full_Body_Hand_Object_Interaction_Synthesis/figures/009_Table_5.jpg]]
*Table 5: Success And Trajectory Imitation Evaluation. We evaluate the average success rate and the ratio of trajectory targets reached (TTR) of our method on the GOAL test set. The objects and trajectories are unseen during training*

## 方法谱系与知识库定位

### 问题定位与核心瓶颈

全身手-物交互生成领域长期存在一条清晰的分界线：运动学方法与物理仿真方法各自解决了问题的一部分，但始终未能在一个统一框架内同时实现**全身协调运动**与**灵巧手指操控**。运动学方法（如 **GOAL** 和 **IMoS**）可以直接从数据中回归出视觉上自然的全身抓取与操纵序列，但缺乏物理约束，导致脚滑、手-物穿透、地面穿透等典型伪影。物理仿真方法则走向另一个极端——**D-Grasp** 专注于孤立手部的物理抓取，不考虑身体的参与；**Hassan et al.** 的工作虽然引入了全身物理仿真，但仅处理粗粒度的身体-物体交互（如搬运大箱子），不涉及精细的手指操控。

本文的核心瓶颈判断是：现有数据驱动方法生成的序列存在物理不可信伪影，而现有物理方法要么只关注身体、要么只关注手部，**缺少一个能同时完成“全身逼近-灵巧抓取-轨迹跟随”这一完整交互链的物理仿真框架**。论文通过 Table 1 从 Full Body、Physics、Whole Interaction、Dexterous Grasping 四个维度系统定位了这一空白。

### 因果机制与核心洞察

解决上述瓶颈的关键因果旋钮在于**分层解耦的技能先验**。具体而言：

1. **解耦训练的身体先验与手先验**：将全身运动（57 DoF 身体关节）与精细手指控制（48 DoF 手指关节）分解到两个分别训练的对抗技能先验中。每个先验通过结合运动模仿与无监督技能发现（ASE 框架）来学习多样化的运动技能，将潜变量 $z_b$ 和 $z_h$ 解码为具体的关节动作。这一解耦设计直接避免了统一训练时潜空间的模式坍塌——消融实验（Table 3）表明，若不分解先验，抓取成功率为零。

2. **高层手-物交互策略在潜空间内规划**：预训练的先验提供了一个结构化的低维潜空间，高层策略 $\pi_{ho}$ 在该空间内输出 $z_b$ 和 $z_h$，而非直接输出高维关节动作。这种分层设计使得策略可以专注于“何时抓取、如何跟随轨迹”等高层决策，将运动实现委托给预训练的技能先验。

3. **目标引导机制协调全身与手部**：通过交替使用真实轨迹与策略自身预测的轨迹目标，并施加辅助 L2 损失 $\mathcal{L}_{\xi} = ||\overline{\pmb{\xi}} - \tilde{\pmb{\xi}}||_2^2$，策略学会了在未见轨迹上鲁棒地协调身体移动与手部抓取。

核心洞察可以总结为：**将全身运动与精细手指控制分解到分别训练的对抗技能先验中，再由高层策略在潜空间内进行规划，既能避免统一训练的模式坍塌，又能借助物理仿真消除传统数据驱动方法的典型伪影**。

### 技术路线对比

| 维度 | 运动学基线 (GOAL, IMoS) | 物理基线 (D-Grasp, Hassan et al.) | 本文方法 |
|------|-------------------------|-----------------------------------|---------|
| 物理仿真 | 不使用 | 部分使用 | 全物理仿真 (Isaac Gym) |
| 全身运动 | 支持 | D-Grasp 不支持，Hassan et al. 支持 | 支持 |
| 灵巧抓取 | 支持 | D-Grasp 支持，Hassan et al. 不支持 | 支持 |
| 完整交互链 | 支持 | 不支持 | 支持 |
| 技能先验 | 无显式先验 | 无显式先验 | 解耦的身体与手先验 |
| 控制层级 | 单层 | 单层 | 分层（高层策略 + 低层先验） |
| 轨迹跟随 | 隐式 | 不适用 | 显式目标引导 |

### 关键证据与置信度评估

**强证据（置信度 ≥ 0.9）**：
- 解耦训练的必要性由 Table 3 消融实验直接验证：移除解耦后抓取成功率为零。
- Table 2 的主实验表明，本文方法在接近阶段抓取成功率（0.79）显著优于 GOAL（0.55）和 IMoS（0.56），同时地面距离（2.1 mm vs. 3.8/4.1 mm）和脚滑率等物理指标全面占优。
- 两阶段训练（先学静态抓取再学轨迹跟随）使成功率提升约 24%（Table 3）。

**需注意的评估不对等**：
- 运动学基线的成功率评估协议与物理方法不完全对等：GOAL 和 IMoS 生成的是运动学姿态，其抓取成功率是通过将固定抓取姿态放入物理仿真仅验证抓取稳定性得到的，而非在完整物理仿真中端到端评估。
- 物理指标（穿透体积、地面距离）受刚体仿真中网格减面近似的影响，转换回 SMPL-X 参数空间时仍会产生轻微穿透，论文对此进行了说明。

### 适用边界与局限

本文方法的适用边界由以下设计选择划定：

1. **身体形状单一**：仅使用单一中性身体形状进行训练和评估，未覆盖不同人体形态（如不同身高、体型的角色）。这限制了方法在个性化虚拟角色或人群多样性场景中的直接应用。

2. **物体尺寸受限**：对于大尺寸物体（需要手指完全伸展才能抓握），策略性能显著下降。这是因为手先验的训练数据中极端伸展姿态的覆盖不足。

3. **仿真精度与计算效率的权衡**：为加速仿真，对物体网格和身体形状进行了减面处理，导致在渲染回高精度网格时仍存在轻微穿透伪影。如何在可接受的计算开销内提高仿真精度是一个开放问题。

4. **抓取多样性的依赖**：方法依赖静态手部姿态参考 $\Psi$ 来控制抓取方式，这意味着抓取的多样性受限于参考姿态的多样性，无法自主探索新的抓取策略。

5. **交互模态单一**：当前框架不支持基于语言指令或语义命令的交互生成，输入仅限于手-物姿态参考和轨迹目标。

### 开放问题与后续方向

1. **身体形状泛化**：如何将身体形状多变纳入基于物理的角色控制框架，使同一策略能驱动不同体型的角色完成灵巧抓取？

2. **仿真精度提升**：能否在不显著增加计算开销的前提下提高仿真精度（如使用更精细的碰撞几何体或软体接触模型），以进一步减少穿透伪影？

3. **双手协同扩展**：当前方法仅处理单手抓取，能否将解耦先验的分层框架扩展到双手协同的全身抓取任务（如双手搬运大物体或双手协作操纵）？

4. **高级任务接口**：能否引入语言或语义命令作为额外的条件输入，使框架支持“抓起杯子并放到桌上”这类高级任务描述？

5. **无参考抓取生成**：如何摆脱对单帧手部参考姿态的依赖，实现全自动的无参考抓取生成——即策略自主根据物体几何和任务目标决定抓取方式？

6. **跨形态迁移**：解耦的身体与手先验框架是否具备向不同形态（如四足机器人上半身操作）迁移的潜力？

## 原文 PDF

![[paperPDFs/3DV_2024/Physically_Plausible_Full_Body_Hand_Object_Interaction_Synthesis.pdf]]