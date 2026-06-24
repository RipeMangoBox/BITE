---
title: "ArtiGrasp: Physically Plausible Synthesis of Bi-Manual Dexterous Grasping and Articulation"
type: paper
paper_level: A
venue: 3DV
year: 2024
pdf_ref: paperPDFs/3DV_2024/ArtiGrasp_Physically_Plausible_Synthesis_of_Bi_Manual_Dexterous_Grasping_and_Articulation.pdf
aliases:
- ArtiGrasp
tags:
- 3DV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 两阶段课程学习：第一阶段在物体固定、双手分别单独训练的环境中学习手指精细控制和铰接动作；第二阶段在共享环境中移除固定约束，使双手协同操作，从而逐步掌握全任务。
primary_logic: 通过单一强化学习策略统一抓取和铰接，并结合通用奖励函数和课程训练，仅需静态手部参考姿势即可生成物理合理、可泛化的双手交互运动。
claims:
- 在动态抓取与铰接任务上，ArtiGrasp成功率0.50，显著优于D-Grasp的0.09，提升约5倍
- 在单独铰接任务中，ArtiGrasp成功率0.55，明显超过D-Grasp的0.22和PD+IK的0.28，且物体基部位移仅为0.01m
- 消融实验表明，缺少课程训练、协同训练或铰接特征均导致铰接成功率显著下降，验证每个组件的必要性
- Grasping (decoupled) 上 Grasp Success Rate (Suc.G↑) = 0.71
---

# ArtiGrasp: Physically Plausible Synthesis of Bi-Manual Dexterous Grasping and Articulation

> [!tip] 核心洞察
> 通过单一强化学习策略统一抓取和铰接，并结合通用奖励函数和课程训练，仅需静态手部参考姿势即可生成物理合理、可泛化的双手交互运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | ArtiGrasp：物理合理的双手灵巧抓取与铰接运动合成 |
| 英文题名 | ArtiGrasp: Physically Plausible Synthesis of Bi-Manual Dexterous Grasping and Articulation |
| 会议/期刊 | 3DV 2024 |
| Links | [Project](https://eth-ait.github.io/artigrasp/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ArtiGrasp |
| Dataset | Grasping, Articulation, Dynamic Object Grasping and Articulation |

> [!tip] 效果简介
> - Grasping (decoupled) 上，Grasp Success Rate (Suc.G↑) 0.71 vs 0.72 (D-Grasp) (-0.01)。
> - Articulation (decoupled) 上，Articulation Success Rate (Suc.A↑) 0.55 vs 0.22 (D-Grasp) (+0.33)。
> - Dynamic Object Grasping and Articulation 上，Task Success Rate (Suc.T↑) 0.50 vs 0.09 (D-Grasp) (+0.41)。

## 概述

**核心问题**：在物理模拟中同时实现双手灵巧抓取与铰接操作面临双重挑战——不仅需要精确的单指力控制和手腕协调来稳定抓握，还需在物体可动的前提下施加定向力以完成开合等铰接动作。直接端到端训练会导致双手相互干扰与精细动作冲突，使任务极易失败。现有方法如 **D-Grasp** 仅适用于单手抓取刚性物体，无法处理铰接任务。

**核心思路**：ArtiGrasp 提出将抓取与铰接统一在单一强化学习策略下，仅需静态手部参考姿势作为输入。其关键设计是一套**两阶段课程学习**机制：第一阶段在物体固定、双手分别独立训练的环境中学习手指精细控制与铰接动作；第二阶段移除固定约束，在共享环境中微调双手协同。配合由模仿奖励（姿势、接触、正则化）与任务奖励（铰接目标、基部位移）组成的通用奖励函数，策略逐步掌握全任务。

**方法定位**：ArtiGrasp 属于基于物理模拟的双手灵巧操作合成方法，与现有工作（Table 1）相比，其独特之处在于：1）统一策略同时处理刚性与铰接物体；2）仅需少量静态手部参考姿势（few-shot）；3）通过强化学习在物理仿真中训练，输出物理合理且可泛化的运动序列。

**主要结果**：
- 在**单独铰接任务**上，ArtiGrasp 成功率 0.55，显著优于 D-Grasp（0.22）和 PD+IK（0.28），物体基部位移仅 0.01m（Table 2）。
- 在**动态抓取与铰接联合任务**上，ArtiGrasp 成功率 0.50，约为 D-Grasp（0.09）的 **5 倍**（Table 3）。
- 在**单独抓取任务**上，ArtiGrasp 成功率 0.71，与 D-Grasp（0.72）性能相当，验证了统一策略未牺牲抓取能力（Table 2）。
- 消融实验证实，课程训练、协同训练和铰接特征三个组件对铰接成功率均有显著贡献，缺少任一组件的降幅在 7–19 个百分点（Table 5）。

**局限性**：生成的手部姿态偶有不自然（源于参考姿势噪声与奖励权衡），仅支持单关节铰接物体，训练耗时约三天，尚未在真实机器人上验证。

## 背景与动机

### 问题背景

在具身人工智能与机器人操作领域，使灵巧手在物理模拟中生成逼真的双手操纵运动是一个核心挑战。这类任务要求智能体同时完成两个子目标：**抓取**（Grasping）——将手部稳定地附着于物体表面，以及**铰接**（Articulation）——在保持抓取的同时操控物体的可动部件（如打开笔记本电脑或旋转水龙头）。传统上，这两个子任务被分别建模：抓取关注接触点选择与力闭合，铰接关注关节运动轨迹规划。然而，现实世界中的操作往往是两者的无缝耦合——手必须同时控制手指的精细接触与手腕的全局运动，任何环节的失败都会导致任务崩溃。

物理模拟为验证操作策略提供了安全且可复现的环境，但也在双手灵巧操作场景中引入了独特的困难：双手之间的相互干扰、手指与物体之间的复杂接触动力学、以及铰接任务对关节角度精度的严苛要求，使得直接训练端到端策略的成功率极低。

### 现有方法缺口

当前该领域存在三个主要缺口：

**1. 单手与刚性物体的局限。** 最具代表性的基线方法 **D-Grasp** 专注于单手抓取刚性物体，其手腕控制依赖基于逆运动学（IK）的 PD 控制器。这种设计在抓取任务上表现良好，但无法泛化到铰接场景——铰接任务要求手腕根据物体关节状态动态调整位置和姿态，而 IK 控制器缺乏这种自适应能力。实验数据也印证了这一点：在单独铰接任务中，D-Grasp 的成功率仅为 0.22，而简单的 PD+IK 基线也只有 0.28（Table 2）。

**2. 抓取与铰接的策略割裂。** 现有工作要么仅处理抓取，要么将铰接视为独立的运动规划问题，缺乏一个统一的策略框架来同时控制手指和手腕。这种割裂导致在动态任务（先抓取、再移动、再铰接）中，两个阶段的衔接高度脆弱——D-Grasp 在动态抓取与铰接任务上的成功率仅为 0.09（Table 3），几乎完全失败。

**3. 双手协同训练的缺失。** 双手操作引入的相互干扰是一个被严重低估的挑战。当两只手同时在共享环境中操作同一物体时，一只手的动作可能破坏另一只手的接触稳定性，导致抓取失败或物体滑落。现有方法缺乏有效的训练机制来应对这种双手耦合效应。

### 本文动机

ArtiGrasp 的核心动机源于一个关键洞察：**通过单一强化学习策略统一抓取和铰接，并结合精心设计的课程训练与通用奖励函数，仅需静态手部参考姿势即可生成物理合理、可泛化的双手交互运动。**

这一动机直接回应了上述三个缺口：

- **统一策略替代分治方案**：将手腕控制和手指控制纳入同一个策略网络，使智能体能够学习两者之间的协调关系，而非依赖手工设计的 IK 控制器。
- **课程训练解决双手干扰**：提出两阶段课程——第一阶段在物体固定、双手分别单独训练的环境中学习手指精细控制和铰接动作；第二阶段移除固定约束，使双手在共享环境中协同操作。这种渐进式训练使策略能够逐步掌握全任务，避免直接面对双手干扰导致的训练失败。
- **通用奖励函数桥接抓取与铰接**：奖励函数由模仿奖励（姿势、接触、正则化）和任务奖励（铰接角度目标、物体基部位移惩罚）组成，无需为不同任务设计独立奖励，使得同一策略可以同时处理抓取和铰接。

从更宏观的视角看，ArtiGrasp 的目标是降低双手灵巧操作合成的门槛：仅需一对静态手部参考姿势（可从动作捕捉数据或单目 RGB 图像重建中获得），即可生成完整的动态操作序列。这种“少样本”特性使其在实际应用中具有更低的部署成本，也为未来从视觉输入直接生成操作运动铺平了道路。

## 核心创新

### 瓶颈分析：双手协同抓取与铰接的物理合成难点

在物理模拟中同时实现双手抓取与铰接面临双重挑战：**手指级别的精细控制**与**手腕级别的空间协调**必须高度耦合。直接训练一个统一的强化学习策略会导致双手相互干扰——一只手试图稳定物体时，另一只手的铰接动作会施加相反的力矩，造成任务失败。现有方法如 **D-Grasp** 仅针对单手抓取刚性物体设计，其手腕控制依赖逆运动学（IK），无法适应铰接任务中动态变化的约束条件。这一瓶颈的本质在于：抓取需要固定物体基座，而铰接需要释放特定自由度，两者的控制目标存在内在冲突。

### 因果调节机制：两阶段课程学习

ArtiGrasp 的核心创新在于通过**课程学习**解耦这一冲突，使单一策略逐步掌握全任务。训练分为两个阶段：

- **第一阶段（固定物体·分训）**：将物体基座固定在桌面上，左右手分别在独立环境中训练。此时每只手只需学习手指的精细控制（抓取或铰接），无需处理手腕协调问题。这降低了探索空间，使策略快速收敛到可行的局部动作模式。

- **第二阶段（自由物体·协同）**：移除物体固定约束，将双手置于共享物理环境中进行微调。策略必须在保持第一阶段学到的抓取/铰接能力的同时，学习双手手腕的协同运动以维持物体稳定。这一阶段的关键在于：策略已经具备了基本的抓取和铰接能力，只需学习协调，而非从零开始探索。

消融实验验证了这一设计的必要性：移除课程训练后，铰接成功率从 0.55 降至 0.36，铰接角度误差从 0.57 升至 0.77（Table 5）。移除协同训练（仅用分训策略）则导致抓取成功率从 0.71 骤降至 0.21。

### 关键设计变更：相对基线的三个 changed slots

相比 D-Grasp 等基线方法，ArtiGrasp 在三个关键维度上进行了根本性改进：

| 设计维度 | 基线方法 | ArtiGrasp 改进 | 证据 |
|---------|---------|---------------|------|
| **手腕控制策略** | 基于逆运动学的 PD 控制器（非学习） | 基于强化学习的通用策略，同时控制手腕和手指 | Table 2: Suc.A 0.55 vs D-Grasp 0.22 |
| **训练课程** | 无课程，直接使用可移动物体和双手训练 | 两阶段课程：先固定物体分训，再自由物体协同 | Table 5: 无课程 Suc.A 降至 0.36 |
| **特征设计** | 不包含铰接特定信息 | 加入铰接信息 $I_{\text{art}}$（铰接轴方向、手腕到轴距离、部件重量等） | Table 5: 无铰接特征 Suc.A 降至 0.48 |

其中，**手腕控制策略的变革**是最根本的差异。D-Grasp 的 IK 手腕控制器在铰接任务中频繁失败（成功率仅 0.22），因为 IK 求解缺乏对动态约束的适应性。ArtiGrasp 的策略网络直接输出 PD 控制目标，能够在模拟中学习到适应不同铰接轴方向和角度的手腕运动模式。**铰接特征 $I_{\text{art}}$** 的引入则为策略提供了任务感知能力，使其能够区分不同物体的铰接特性。消融实验表明，缺少该特征会导致角度误差从 0.57 增加到 0.67。

### 统一策略的核心洞察

ArtiGrasp 的深层洞察在于：**抓取和铰接不应被视为两个独立任务，而是一个连续操作序列的不同阶段**。通过单一策略统一两者，策略可以在抓取阶段积累的接触信息和物体状态自然过渡到铰接阶段，避免了任务切换时的信息丢失。这一点在动态抓取与铰接任务中尤为突出：ArtiGrasp 的任务成功率达到 0.50，而 D-Grasp 仅为 0.09（Table 3），提升约 5 倍。D-Grasp 虽然能成功抓取和移动物体，但无法完成后续的铰接动作（Figure 3），而 ArtiGrasp 的统一策略能够在移动物体后顺畅地执行铰接。

### 方法局限与开放问题

尽管创新显著，ArtiGrasp 仍存在若干限制。生成的手部姿势有时不够自然，这源于 ARCTIC 数据集的噪声标签以及任务奖励与模仿奖励之间的权衡（Figure 10）。此外，当前方法仅支持单铰接关节物体，无法处理多关节物体（如剪刀）或需要手指重新定位的任务。训练时间约三天，且未在真实机器人上验证。这些限制指向了未来的研究方向：如何引入手部姿态先验或生物力学约束来提升自然度，如何扩展至多关节物体，以及如何摆脱对静态参考姿势的依赖，实现完全自主的双手操作生成。

## 整体框架

ArtiGrasp 将双手抓取与铰接统一为单一强化学习策略，输入仅需一组静态手部参考姿势，输出物理模拟中连贯的双手操作运动序列。该方法的核心瓶颈在于：在物理模拟中同时实现双手抓取与铰接需要精确的手指控制和手腕协调，直接训练会因双手相互干扰和精细动作要求而导致任务失败。现有方法（如 D-Grasp）仅适用于单手抓取刚性物体，无法处理铰接任务。

为解决这一问题，ArtiGrasp 采用两阶段课程学习作为因果调控机制：第一阶段在物体固定于桌面、双手分别单独训练的环境中学习手指精细控制和铰接动作；第二阶段在共享环境中移除固定约束，使双手协同操作，从而逐步掌握全任务。这一设计使策略能够从简化的子任务中逐步积累能力，避免直接面对高维双手协调空间的探索困难。

### 策略架构与输入输出流

整个 pipeline 由四个核心模块构成，其数据流如下：

1. **特征提取层 $\Phi$**：将物理模拟的状态 $\mathbf{s}$ 和静态参考姿势 $\mathbf{D}$ 转换为策略输入特征向量。如公式所示：
   $$\Phi ( \mathbf { s } , \mathbf { D } ) = ( \mathcal { H } , \mathcal { O } , \mathcal { G } )$$
   其中 $\mathcal{H}$ 为手部特征（包含关节旋转、速度、接触力、手腕相对速度），$\mathcal{O}$ 为物体特征，$\mathcal{G}$ 为目标特征。目标特征中特别融入了铰接信息 $I_{\text{art}}$（铰接轴方向、手腕到轴的距离、部件重量等），这是方法区别于基线的重要设计。

2. **策略网络 $\pi$**：接收特征向量，输出 PD 控制器的目标动作 $\mathbf{a}$，再由 PD 控制器计算关节力矩 $\tau$ 驱动 MANO 手模型。问题被形式化为马尔可夫决策过程（MDP），目标是最大化期望累积奖励：
   $$\mathbb{E}_{\xi \sim \pi} \left[ \sum_{t=0}^{T} \gamma^{t} r_{t} \right]$$

3. **奖励函数 $r$**：由模仿奖励 $r_{\text{im}}$ 和任务奖励 $r_{\text{task}}$ 两部分组成：
   $$r = r_{\mathrm{im}} + r_{\mathrm{task}}$$
   模仿奖励包含姿势奖励 $r_p$、接触奖励 $r_c$ 和正则化项，鼓励手部动作贴近参考姿势并在目标接触点施加适当的力。任务奖励则驱动策略达到目标铰接角度并抑制物体基部位移：
   $$r_{\mathrm{task}} = -w_{tq} || \overline{\omega} - \omega || - w_{tx} || \mathbf{p}^{0} - \mathbf{p} ||^{2}$$

4. **课程调度器**：控制两阶段训练流程（如 Figure 2 中灰色和紫色方框所示）。第一阶段在独立环境中固定物体、分别训练每只手；第二阶段切换至共享环境，移除物体固定约束，进行双手协同微调。

![[assets/figures/papers/paper_list_l1653_ArtiGrasp_Physically_Plausible_Synthesis_of_Bi_Manual_Dexterous_Grasping/figures/003_Figure_2.jpg]]
*Figure 2: Overview of Grasping and Articulation Policy. Our method uses static hand pose references as input (top row) and generates dynamic sequences (bottom row, where higher transparency represents further in time). We propose a curriculum that starts in a simplified setting with separate environments per hand and fixed-base objects (gray solid box on the left) and continues training in a shared environment with non-fixed object base (purple solid box in the middle). Our policies are trained using reinforcement learning and a physics simulation. Rewards are only used during training. The detailed structure of our policy is shown on the right*

### 与基线方法的关键差异

相较于 D-Grasp 和 PD+IK 基线，ArtiGrasp 在三个关键设计点上做出改进：

- **手腕控制策略**：D-Grasp 采用基于逆运动学的 PD 控制器，而 ArtiGrasp 通过强化学习训练统一策略，同时控制手腕和手指以适应不同铰接任务。消融实验（Table 5）表明，缺少协同训练（w/o cooperation）会使抓取成功率从 0.71 降至 0.21，验证了学习型手腕控制的重要性。
- **训练课程**：基线方法无课程设计，直接使用可移动物体和双手训练。移除课程训练（w/o curriculum）后，铰接成功率从 0.55 降至 0.36，铰接角度误差从 0.57 升至 0.77（Table 5），证明分阶段训练对任务成功至关重要。
- **特征设计**：基线不包含铰接特定信息，ArtiGrasp 在目标特征中加入 $I_{\text{art}}$。移除该特征（w/o art. features）导致铰接成功率下降至 0.48，角度误差增加至 0.67（Table 5），表明铰接感知特征对策略性能有实质贡献。

整体而言，ArtiGrasp 通过“特征提取→策略推理→PD 控制→物理模拟”的闭环，配合课程调度和复合奖励函数，仅需静态手部参考姿势即可生成物理合理、可泛化的双手交互运动。

### 补充图表

![[assets/figures/papers/paper_list_l1653_ArtiGrasp_Physically_Plausible_Synthesis_of_Bi_Manual_Dexterous_Grasping/figures/002_Table_1.jpg]]
*Table 1: Comparison between ours and existing methods. Ours generates two-hand manipulations using physics simulation, requires only static hand pose references (few shot), and accommodates both rigid and articulated objects with a unified policy*

## 核心模块与公式推导

ArtiGrasp 的核心架构由四个紧密协作的模块构成，它们共同支撑了“单一策略统一抓取与铰接”的核心目标。

### 特征提取层 Φ

策略网络接收的输入并非原始状态，而是经过特征提取层 Φ 处理后的结构化特征向量。该层将环境状态 **s** 和静态手部参考姿势 **D** 映射为三个组成部分：

$$\Phi ( \mathbf { s } , \mathbf { D } ) = ( \mathcal { H } , \mathcal { O } , \mathcal { G } )$$

其中：
- **手部特征 H**：包含关节旋转 **q**、关节速度 **q̇**、指尖接触力 **f**，以及相对于手腕的指尖速度信息。这些特征为策略提供了手部当前姿态和动力学状态的完整描述。
- **物体特征 O**：描述被操作物体的物理状态，包括其位姿、速度等属性。
- **目标特征 G**：编码任务目标，关键地包含了铰接信息 **I_art**——铰接轴方向、手腕到铰接轴的距离、部件重量等。消融实验证实，移除该铰接特征会导致铰接成功率从 0.55 降至 0.48，角度误差从 0.57 升至 0.67（Table 5），验证了其必要性。

![[assets/figures/papers/paper_list_l1653_ArtiGrasp_Physically_Plausible_Synthesis_of_Bi_Manual_Dexterous_Grasping/figures/010_Table_5.jpg]]
*Table 5: Ablations. We ablate our curriculum, cooperative training, and the articulation features. All components are important aspects to achieve grasping and articulation with a single policy*

### 策略网络 π

策略网络将特征向量 (H, O, G) 映射为动作 **a**，这些动作作为 PD 控制器的目标值，进而计算出驱动 MANO 手模型的关节力矩 **τ**。整个问题被形式化为马尔可夫决策过程，目标是最大化期望累积奖励：

$$\mathbb{E}_{\xi \sim \pi} \left[ \sum_{t=0}^{T} \gamma^{t} r_{t} \right]$$

轨迹 ξ 的概率由策略和物理模拟的动力学共同决定：

$$p_{\theta}(\xi) = p(\mathbf{s}_{0}) \prod_{t=0}^{T} p(\mathbf{s}_{t+1} | \mathbf{s}_{t}, \mathbf{a}_{t}) \pi(\mathbf{a}_{t} | \Phi(\mathbf{s}_{t}, \mathbf{D}))$$

### 奖励函数 r

奖励函数是引导策略学习的关键，由模仿奖励和任务奖励两部分组成：

$$r = r_{\mathrm{im}} + r_{\mathrm{task}}$$

**模仿奖励**鼓励生成的动作接近参考姿势，包含三个子项：
- **姿势奖励**：惩罚关节位置和角度与参考的偏差，对指尖关节赋予更高权重：

$$r_{p} = - \sum_{i=1}^{L} w_{px}^{i} || \overline{\mathbf{x}}^{i} - \mathbf{x}^{i} ||^{2} - w_{pq} || \overline{\mathbf{q}} - \mathbf{q} ||$$

- **接触奖励**：鼓励手指达到目标接触点并施加适当力度。第一项奖励接触点匹配度，第二项奖励施加与物体重量成比例的力（λ 为比例系数，m₀ 为物体质量）：

$$r_{c} = w_{cc} \frac{ \bar{\mathbf{c}}^{T} \mathbf{I}_{f>0} }{ \bar{\mathbf{c}}^{T} \bar{\mathbf{c}} } + w_{cf} \min( \bar{\mathbf{c}}^{T} \mathbf{f}, \lambda m_{o} )$$

- **正则化项**：惩罚过大的动作或速度，促进平滑运动。

**任务奖励**则直接驱动铰接目标的完成，同时约束物体整体不发生位移：

$$r_{\mathrm{task}} = -w_{tq} || \overline{\omega} - \omega || - w_{tx} || \mathbf{p}^{0} - \mathbf{p} ||^{2}$$

其中 ω̄ 为目标铰接角度，ω 为当前角度；**p**⁰ 为物体基座初始位置，**p** 为当前位置。该设计在鼓励达到目标角度的同时，强制物体基座保持稳定——实验表明，ArtiGrasp 的物体基部位移仅为 0.01m，显著优于基线方法。

### 课程调度器

课程调度器并非网络模块，而是控制训练流程的关键机制。它实施两阶段课程学习：

- **第一阶段**：物体被固定在桌面上，左右手在各自独立的环境中分别训练。这降低了任务复杂度，使策略能专注于学习手指精细控制和铰接动作，避免了双手相互干扰的问题。
- **第二阶段**：移除物体固定约束，双手在共享环境中协同操作。策略在此阶段学习手腕协调和双手配合，以完成完整的抓取-铰接任务。

消融实验表明，缺少课程训练直接导致铰接成功率从 0.55 骤降至 0.36，角度误差从 0.57 升至 0.77（Table 5），证实了课程设计对于解决“双手协同铰接”这一核心瓶颈的决定性作用。

### 补充图表

![[assets/figures/papers/paper_list_l1653_ArtiGrasp_Physically_Plausible_Synthesis_of_Bi_Manual_Dexterous_Grasping/figures/015_Figure_9.jpg]]
*Figure 9: Long sequence with multiple objects. We show that our method can generate sequences of manipulating multiple objects. (A) Approaching the mixer with the left hand. (B) Grasping the mixer with the left hand. (C) Articulating the mixer with the right hand while the left hand is holding it. (D) Putting the mixer down on the table. (E) Approaching the box with both hands. (F) Grasping the box with both hands. (G) Relocating the box on the table and moving the left hand to the ketchup bottle. (H) Grasping the ketchup bottle with the left hand and opening the box with the right hand. (I) Relocating the ketchup bottle while the box is being held open. (J) Dropping the ketchup bottle into the box....*

## 实验与分析

### 核心定量结果

ArtiGrasp 在三个递进的任务设定下验证了其统一策略的有效性，关键指标汇总如下：

**解耦任务（抓取与铰接独立评估）**
- **抓取成功率 (Suc.G)**：ArtiGrasp 达到 0.71，与 D-Grasp 的 0.72 基本持平（-0.01），表明引入铰接能力并未牺牲抓取性能。PD+IK 仅为 0.25，说明纯控制器方法难以完成灵巧抓取。
- **铰接成功率 (Suc.A)**：ArtiGrasp 达到 0.55，显著优于 D-Grasp 的 0.22（+0.33）和 PD+IK 的 0.28。同时物体基部位移仅 0.01m，证明策略在铰接过程中有效抑制了不必要的物体整体移动（Table 2）。

**动态抓取与铰接联合任务**
这是核心挑战：策略需先抓取并移动物体，再将其铰接至目标角度。ArtiGrasp 的任务成功率 (Suc.T) 达到 0.50，而 D-Grasp 仅为 0.09，提升约 5 倍。在所有子指标上（抓取成功、铰接成功、基部位移、角度误差），ArtiGrasp 均全面领先（Table 3）。

![[assets/figures/papers/paper_list_l1653_ArtiGrasp_Physically_Plausible_Synthesis_of_Bi_Manual_Dexterous_Grasping/figures/005_Table_3.jpg]]
*Table 3: Evaluation for our Dynamic Object Grasping and Articulation task. Our method outperforms D-Grasp on all metrics when evaluated on the task of transitioning an articulated object into a target articulated object pose*

**定性对比**：Figure 3 展示了典型场景——D-Grasp 能成功抓取和移动物体，但在铰接阶段失败；ArtiGrasp 则能在移动后顺利打开物体，体现了统一策略对完整操作序列的覆盖能力。

### 消融实验

Table 5 的消融实验验证了三个关键设计组件的因果贡献：

| 消融条件 | Suc.G | Suc.A | 角度误差 | 核心发现 |
|---------|-------|-------|---------|---------|
| 完整方法 | 0.71 | 0.55 | 0.57 | 基线 |
| w/o curriculum | 0.61 | 0.36 | 0.77 | 缺少课程训练导致铰接成功率大幅下降，角度误差显著增加 |
| w/o cooperation | 0.21 | 0.49 | 0.62 | 移除双手协同训练后抓取几乎完全失败，位置误差剧增 |
| w/o art. features | 0.68 | 0.48 | 0.67 | 去除铰接特征 I_art 使铰接成功率下降，角度误差上升 |

**因果链解读**：
- **课程训练**是铰接能力的核心使能器。第一阶段在物体固定、双手分离的环境中分别训练每只手，使策略先掌握手指精细控制和铰接动作；第二阶段移除固定约束，在共享环境中微调双手协同。缺少这一渐进过程，策略难以同时应对双手协调和物体运动带来的复杂耦合。
- **协同训练**对抓取至关重要。若双手独立训练而不在共享环境中协同，策略无法学习双手之间的力平衡和空间协调，导致抓取成功率从 0.71 骤降至 0.21。
- **铰接特征 I_art**（包含铰接轴方向、手腕到轴的距离、部件重量等）为策略提供了理解物体运动学结构的关键信息，去除后铰接性能下降约 13%。

### 鲁棒性与泛化能力

**对噪声参考姿势的鲁棒性**：Table 4 显示，当使用从单张 RGB 图像重建的手部参考姿势（而非动捕数据）作为输入时，抓取和铰接性能仅有轻微下降。这表明方法能够容忍现实场景中来自现成姿态估计器的噪声估计，具备向端到端视觉输入扩展的潜力。Figure 5 展示了从噪声参考姿势生成合理运动序列的示例。

**失败恢复能力**：Figure 4 展示了策略在铰接过程中出现失败迹象后的恢复行为，说明强化学习训练的策略具备一定的闭环调整能力，而非仅能执行开环轨迹。

### 失败模式与局限

尽管整体性能显著优于基线，ArtiGrasp 仍存在以下已知失败模式：

1. **不自然的手部姿态**：生成的手部姿态有时呈现非自然的扭曲（Figure 10）。这主要源于两个因素：ARCTIC 数据集中本身存在噪声标签，以及任务奖励（如达到目标铰接角度）与模仿奖励之间的权衡——策略可能牺牲姿态自然度以完成功能性目标。
2. **铰接物体限制**：当前方法仅支持单一铰接关节的物体，无法处理多关节物体（如工具箱）或需要手中操控的任务（如剪刀的开合）。
3. **训练成本**：完整训练约需三天，且尚未在真实机器人上验证，Sim-to-Real 的域差距仍是一个开放问题。
4. **对参考姿势的依赖**：方法需要预先提取或预测的静态手部参考姿势作为输入，尚未实现端到端从视觉直接生成操作序列。

![[assets/figures/papers/paper_list_l1653_ArtiGrasp_Physically_Plausible_Synthesis_of_Bi_Manual_Dexterous_Grasping/figures/016_Figure_10.jpg]]
*Figure 10: Unnatural hand poses (a) Some of the hand pose references we extract from the ARCTIC dataset contain unnatural hand poses. (b) Our method can output some unnatural hand poses, which can be due to noise in the hand pose references or because of the trade-off in the task objective*

### 对比公平性说明

需注意 D-Grasp 原本为单手刚性物体抓取设计，其手腕控制基于逆运动学，并非为铰接任务优化。因此在铰接指标上的大幅领先部分反映了方法定位差异——ArtiGrasp 的核心贡献恰恰在于统一抓取与铰接的单一策略设计。在抓取子任务上两者性能相当，验证了统一策略并未以牺牲抓取能力为代价。

### 补充图表

![[assets/figures/papers/paper_list_l1653_ArtiGrasp_Physically_Plausible_Synthesis_of_Bi_Manual_Dexterous_Grasping/figures/006_Figure_3.jpg]]
*Figure 3: Qualitative evaluation of Dynamic Object Grasping and Articulation. D-Grasp can grasp and relocate the object successfully, but fails to articulate the object. Ours is more successful at tackling this task and can articulate the object after relocation*

![[assets/figures/papers/paper_list_l1653_ArtiGrasp_Physically_Plausible_Synthesis_of_Bi_Manual_Dexterous_Grasping/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative articulation result. The hand shows some recovery ability from failure cases. Zoom in for details*

![[assets/figures/papers/paper_list_l1653_ArtiGrasp_Physically_Plausible_Synthesis_of_Bi_Manual_Dexterous_Grasping/figures/008_Table_4.jpg]]
*Table 4: Results with reconstructed hand pose references. When evaluated with predictions from images, we observe a minor drop in performance for grasping and articulation compared to mocap data. However, the overall performance shows that our method can handle noisy estimates. The asterisk (*) denotes using hand pose references from mocap*

![[assets/figures/papers/paper_list_l1653_ArtiGrasp_Physically_Plausible_Synthesis_of_Bi_Manual_Dexterous_Grasping/figures/009_Figure_5.jpg]]
*Figure 5: Motion generation. Our method can synthesize new motion sequences (c) with a noisy hand pose reference (b) reconstructed from a single RGB image (a)*

![[assets/figures/papers/paper_list_l1653_ArtiGrasp_Physically_Plausible_Synthesis_of_Bi_Manual_Dexterous_Grasping/figures/013_Figure_6.jpg]]
*Figure 6: Qualitative evaluation of grasping. When evaluated only on grasping, PD+IK often fails to successfully grasp the object. On the other hand, D-Grasp and ours succeed at the task*

![[assets/figures/papers/paper_list_l1653_ArtiGrasp_Physically_Plausible_Synthesis_of_Bi_Manual_Dexterous_Grasping/figures/014_Figure_7.jpg]]
*Figure 7: Qualitative evaluation of articulation. When evaluated only on articulation, both PD+IK and D-Grasp often fail at the task. On the other hand, our method can articulate the object successfully*

## 方法谱系与知识库定位

### 与现有方法的关系

ArtiGrasp 处于物理仿真驱动的手-物交互生成这一研究脉络中。该脉络的核心瓶颈在于：在物理模拟中同时实现双手抓取与铰接需要精确的手指控制和手腕协调，直接训练会因双手相互干扰和精细动作要求而导致任务失败。ArtiGrasp 的方法定位可通过以下维度与现有工作区分：

**与 D-Grasp 的关系**（最直接基线）。D-Grasp 是面向单手抓取刚性物体的物理合成方法，其手腕控制基于逆运动学（IK）的 PD 控制器，本质上不具备处理铰接任务的能力。在解耦的抓取任务上，ArtiGrasp 的成功率（Suc.G 0.71）与 D-Grasp（0.72）基本持平，表明统一策略在抓取能力上不退化；但在铰接任务上，D-Grasp 的 Suc.A 仅为 0.22，ArtiGrasp 达到 0.55，提升约 2.5 倍。这一差距的因果来源在于：D-Grasp 的 IK 手腕控制无法适应铰接过程中物体部件运动带来的接触点变化，而 ArtiGrasp 通过强化学习训练的手腕-手指联合策略能够在线调整。

**与 PD+IK 的关系**。PD+IK 作为简单基线，利用 PD 控制器实现参考姿势，手腕通过逆运动学控制。其铰接成功率（0.28）虽略高于 D-Grasp，但仍远低于 ArtiGrasp。PD+IK 的失败模式主要在于：当物体基座不固定时，IK 手腕无法补偿物体位移，导致手指滑脱或无法施加有效力矩。

**与更广泛的手-物交互方法的对比**。Table 1 将 ArtiGrasp 与现有方法在四个维度上进行了区分：（1）是否支持双手操作；（2）是否使用物理仿真；（3）是否仅需静态手部参考姿势（few-shot）；（4）是否用统一策略同时处理刚体和铰接物体。ArtiGrasp 是首个在四个维度上均满足的方法。

### 核心设计决策的因果机制

ArtiGrasp 的关键设计可归结为三个相互依赖的组件，消融实验（Table 5）揭示了各自的贡献：

1. **两阶段课程学习**：第一阶段在物体固定、双手分别单独训练的环境中学习手指精细控制和铰接动作；第二阶段在共享环境中移除固定约束，使双手协同操作。移除课程训练后，铰接成功率从 0.55 降至 0.36，铰接角度误差从 0.57 升至 0.77。课程学习的核心作用是解耦双手协调与精细手指控制的学习难度，避免强化学习在早期探索中陷入局部最优。

2. **协同训练**：移除协同训练（即双手独立训练而不在共享环境中微调）使抓取成功率从 0.71 骤降至 0.21，位置误差显著增加。这表明双手在共享物理空间中的隐式协调（如避免碰撞、力分配）无法通过独立训练习得，必须在共享环境中通过交互学习。

3. **铰接特征 $I_{art}$**：包含铰接轴方向、手腕到轴的距离、部件重量等信息。移除该特征后，铰接成功率降至 0.48，角度误差增至 0.67。$I_{art}$ 为策略提供了关于物体运动学结构的先验，使其能够预判铰接动作的效果方向。

这三个组件的因果链条为：课程学习提供稳定的技能习得路径 → 铰接特征提供任务相关的感知输入 → 协同训练使双手在共享空间中形成有效配合。

### 适用边界与局限

ArtiGrasp 的适用边界受以下因素约束：

1. **物体复杂度限制**：仅支持具有单个铰接关节的物体，无法处理多关节物体或需要手中操控的任务（如剪刀的开合需要手指重新定位）。这是方法框架的结构性限制——特征设计中的铰接信息 $I_{art}$ 假设了单一铰接轴的存在。

2. **输入依赖性**：需要预先提取或预测的静态手部参考姿势作为输入，尚未实现端到端从图像直接生成。Table 4 显示，使用从图像重建的噪声参考姿势时，性能有轻微下降（抓取成功率从 0.71 降至 0.68，铰接成功率从 0.55 降至 0.50），说明方法对输入噪声有一定鲁棒性，但仍依赖外部姿态估计模块。

3. **自然度不足**：生成的手部姿势有时不自然（Figure 10），源于两方面原因：ARCTIC 数据集的噪声标签，以及任务奖励（如达到铰接角度）与模仿奖励之间的权衡。方法未集成生物力学约束或学习的手部先验来提升自然度。

4. **训练成本**：训练时间约三天，且未在真实机器人上验证，其实用部署的域差距和安全性仍是开放问题。

### 开放问题

1. **序列规划与任务耦合**：当前方法依赖启发式规则将抓取、移动、铰接等子阶段串联为完整序列。如何设计高级规划模块，以自动耦合多个子阶段，形成更复杂的操作序列（如 Figure 9 所示的长序列操作），是一个关键扩展方向。

2. **摆脱参考姿势依赖**：静态手部参考姿势是当前方法的必要输入。能否通过目标条件策略或视觉-运动联合学习，实现完全自主的双手操作生成，将显著提升方法的实用性。

3. **复杂物体扩展**：支持具有多个铰接关节或需要手指重新定位的物体（如工具箱、剪刀），需要在特征设计、奖励函数和课程策略上进行根本性扩展。

4. **自然度与物理合理性的权衡**：引入手部姿态先验（如基于大规模抓取数据集的生成模型）或生物力学约束（如关节限位、肌腱力限制），可能在不牺牲任务成功率的前提下提升生成动作的自然度。这需要设计新的奖励项或约束优化框架。

5. **真实机器人部署**：从仿真到真实的迁移面临接触动力学建模误差、状态估计噪声、实时控制延迟等挑战。域随机化和系统辨识是可能的缓解策略，但尚未在 AratiGrasp 框架中验证。

## 原文 PDF

![[paperPDFs/3DV_2024/ArtiGrasp_Physically_Plausible_Synthesis_of_Bi_Manual_Dexterous_Grasping_and_Articulation.pdf]]