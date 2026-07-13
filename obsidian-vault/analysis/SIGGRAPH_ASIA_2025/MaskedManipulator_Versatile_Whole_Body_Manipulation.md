---
title: "MaskedManipulator: Versatile Whole-Body Manipulation"
type: paper
paper_level: A
venue: "SIGGRAPH Asia"
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2025/MaskedManipulator_Versatile_Whole_Body_Manipulation.pdf
code_link: null
project_link: https://research.nvidia.com/labs/par/maskedmanipulator/
aliases:
- MaskedManipulator
tags:
- SIGGRAPH_ASIA_2025
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "引入两阶段学习范式（密集目标跟踪 MimicManipulator + 稀疏目标蒸馏 MaskedManipulator），并将 spatio-temporal goal-conditioning 从人体部位扩展到被操纵物体。"
primary_logic: "先利用运动捕捉数据训练跟踪策略掌握丰富的精确交互策略，再通过掩码目标蒸馏将其知识迁移到通用生成策略，使得仅凭稀疏时空目标（如物体终点位置）即可生成多样化、物理合理且类人的全身操作行为。"
claims:
- "MimicManipulator 在 GRAB 测试集上成功率达到 60.2%，远超 InterMimic 的 8.5%，证明紧致跟踪设计的有效性。"
- "紧密早期终止是最重要的设计，移除后成功率从 60.2% 下降至 51.8%。"
- "在线 DAgger 蒸馏对泛化至关重要；离线 Diffusion 策略在遥操作任务上成功率仅为 25.5%，远低于在线版本的 58.2%。"
- "三阶段接触奖励（接近、接合、释放）引导了精确的物体交互，缺失该奖励会导致跟踪质量下降。"
---

# MaskedManipulator: Versatile Whole-Body Manipulation

> [!tip] 核心洞察
> 先利用运动捕捉数据训练跟踪策略掌握丰富的精确交互策略，再通过掩码目标蒸馏将其知识迁移到通用生成策略，使得仅凭稀疏时空目标（如物体终点位置）即可生成多样化、物理合理且类人的全身操作行为。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MaskedManipulator：通用全身物体操作 |
| 英文题名 | MaskedManipulator: Versatile Whole-Body Manipulation |
| 会议/期刊 | SIGGRAPH Asia 2025 |
| Links | [paper](https://arxiv.org/abs/2505.19086) · [Project](https://research.nvidia.com/labs/par/maskedmanipulator/) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | MaskedManipulator |
| Dataset | GRAB test set (subject 10) |

> [!tip] 效果简介
> - GRAB test set (subject 10) 上，Full-Sequence Success Rate 为 MimicManipulator: 60.2%，对比 InterMimic: 8.5%，变化 +51.7%。

## 概要

**问题**：让物理模拟的人形角色仅凭稀疏的高层目标（如物体终点位置）就能生成精确、多样且物理合理的全身物体操作行为，是计算机动画与具身智能领域的开放难题。其根本瓶颈在于：精确操作要求高精度控制，而通用任务需要灵活适应稀疏目标，两者存在深层矛盾；直接从稀疏目标学习面临巨大的解空间与信用分配困境。

**核心思路**：MaskedManipulator 提出**两阶段学习范式**——先利用运动捕捉数据训练一个密集目标跟踪策略（MimicManipulator），使其掌握丰富的精确交互技能；再通过掩码目标蒸馏，将跟踪策略的交互知识迁移到通用生成策略（MaskedManipulator），使后者仅凭稀疏时空目标即可生成类人的全身操作行为。同时，该方法将时空目标条件（spatio-temporal goal-conditioning）从人体部位**扩展至被操纵物体**，首次实现了对人体与物体目标的统一控制。

**方法定位**：MaskedManipulator 属于**物理模拟驱动的角色动画与目标条件强化学习的交叉方向**，其方法谱系可追溯至 MaskedMimic（Tessler et al., TOG 2024）的统一人体控制器，但后者仅支持人体部位目标，未涵盖物体交互。与同期工作相比，InterMimic（Xu et al., CVPR 2025）是面向物理人-物交互的通用全身控制基线，但在 GRAB 测试集上的全序列成功率仅为 8.5%；OmniGrasp（Luo et al., NeurIPS 2024）聚焦于基于密集目标的全身体抓取，不适用于长程 goal-conditioned 任务。MaskedManipulator 通过两阶段训练与掩码蒸馏，在**通用性**（同时支持人体与物体目标）与**精确性**（跟踪成功率 60.2%）之间取得了突破性平衡。

**关键结果**：
- MimicManipulator 在 GRAB 测试集上全序列成功率达到 **60.2%**，远超 InterMimic 的 8.5%（Table 1），证明紧致跟踪设计的有效性。
- **紧密早期终止**是最关键的设计，移除后成功率降至 51.8%（Table 1 消融）。
- **在线 DAgger 蒸馏**对泛化至关重要：离线 Diffusion 策略在遥操作任务上成功率仅 25.5%，远低于在线版本的 58.2%（Table 2）。
- 三阶段接触奖励（接近-接合-释放）引导了精确的物体交互，缺失该奖励会导致跟踪质量显著下降（Table 1 消融）。

**局限与展望**：当前方法依赖人工设计的离散终止条件，在接触过渡阶段可能出现不自然行为；简化的碰撞几何体难以复现软体接触动力学，限制了精细操作的保真度。未来方向包括学习可微终止条件、泛化至未见物体类别，以及扩展控制接口以支持更精细的交互指定。

在物理仿真中生成类人的全身物体操作行为，是计算机图形学与机器人学中长期存在的挑战。这一任务要求虚拟角色不仅能够协调全身运动（行走、弯腰、转体），还必须与各类物体进行精确的物理交互（抓取、搬运、使用工具）。当前的主流方法在处理这一问题时，面临一个根本性的矛盾：**精确操作要求高精度控制，而通用任务则需要灵活适应稀疏的高层目标**，两者难以在同一框架内统一实现。

现有方法通常沿两条路径展开，但各自存在明显局限。一方面，基于运动跟踪的方法（如 **InterMimic**，Xu et al., CVPR 2025）试图通过物理仿真重建动作捕捉数据中的交互序列，其成功依赖于密集的参考运动信号，无法泛化到仅给定稀疏目标的新任务。另一方面，基于目标条件生成的方法（如 **MaskedMimic**，Tessler et al., TOG 2024）虽然支持通过稀疏时空目标控制人体部位，但其目标条件范围仅限于人体关节，未涵盖被操纵物体，因此无法处理“将物体从A点移动到B点”这类以物体为中心的操作任务。此外，**OmniGrasp**（Luo et al., NeurIPS 2024）等全身体抓取方法同样依赖密集目标，难以适应长程的 goal-conditioned 场景。

直接从稀疏目标（如物体终点位置）学习全身操作策略，面临巨大的解空间和信用分配难题：策略必须在海量的全身动作组合中，自行发现哪些动作序列能够同时满足物理约束和稀疏的目标条件。这使得从零开始的强化学习（RL）训练极难收敛，生成的交互行为往往缺乏物理合理性和类人特征。

针对上述缺口，**MaskedManipulator** 提出了一个两阶段学习范式，其核心动机在于：先利用丰富的运动捕捉数据，让策略掌握精确的交互技能；再通过知识蒸馏，将这些技能迁移到仅依赖稀疏目标的通用生成策略中。具体而言，第一阶段训练一个名为 **MimicManipulator** 的物理运动跟踪器，在密集参考信号的监督下学习重建全身操作序列；第二阶段则通过在线 DAgger 蒸馏，将跟踪器的交互知识迁移至 **MaskedManipulator** 生成策略，使其仅凭稀疏时空目标（如手腕位置、头部朝向、物体终点位姿）即可生成多样化、物理合理且类人的全身操作行为。该方法的关键创新在于将 spatio-temporal goal-conditioning 的范围从人体部位扩展至被操纵物体，从而首次在一个统一框架内实现了对人体和物体的联合稀疏控制。

## 核心方法与创新机理

MaskedManipulator 的核心创新在于通过**两阶段学习范式**，从根本上解决了精确全身物体操作与通用稀疏目标控制之间的矛盾。其关键洞察是：先利用运动捕捉数据训练一个密集目标跟踪策略（MimicManipulator），使其掌握丰富的精确交互知识；再通过掩码目标蒸馏，将这些知识迁移到通用生成策略（MaskedManipulator），从而仅凭稀疏时空目标即可生成多样化、物理合理且类人的全身操作行为。

### 关键 changed slots

与先前工作相比，MaskedManipulator 在以下四个关键维度上实现了突破性改进：

**1. Goal conditioning scope：从仅人体部位扩展到人体部位与被操纵物体**

先前的统一人体控制器 **MaskedMimic**（Tessler et al., TOG 2024）仅支持对人体部位（如手腕、头部）的稀疏目标条件控制，未涵盖被操纵物体。MaskedManipulator 将 spatio-temporal goal-conditioning 框架扩展至被操纵物体，使得用户可以通过指定物体在特定时间步应到达的位置和姿态来控制交互行为（Figure 6）。这一扩展使得策略能够从稀疏的物体目标中推断出手部应如何与物体交互，是实现通用物体操作控制的基础。

**2. Training paradigm：从单阶段跟踪或从零开始的 RL 到两阶段“跟踪-蒸馏”**

先前方法如 **InterMimic**（Xu et al., CVPR 2025）和 **OmniGrasp**（Luo et al., NeurIPS 2024）采用单阶段训练范式，要么直接跟踪密集参考运动，要么从零开始通过 RL 学习。MaskedManipulator 引入了两阶段学习：第一阶段训练 MimicManipulator 作为基于物理的运动跟踪器，在完全观测条件下通过 RL 精确重建全身操作序列；第二阶段通过在线 DAgger 蒸馏，将跟踪器的交互知识迁移到仅接收稀疏目标的 MaskedManipulator 策略。这一设计有效规避了直接从稀疏目标学习所面临的巨大解空间和信用分配难题。

**3. Contact reward design：从简单接触奖励到三阶段接触奖励**

为实现精确的物体交互，MaskedManipulator 设计了分阶段接触奖励（Figure 2），将交互过程分解为三个连续阶段：（a）**接近阶段**（Approach）：跟踪参考运动的同时，对齐手部相对于物体表面的路径；（b）**接合阶段**（Engagement）：确保关键接触点按照参考运动得以维持；（c）**释放阶段**（Release）：促进平滑且及时的物体脱离。消融实验表明，移除该分阶段接触引导奖励会导致跟踪质量显著下降（Table 1）。

**4. Early termination criteria：从宽松终止条件到严格终止条件**

为定义可行的跟踪范围并防止策略学习不良行为，MimicManipulator 引入了严格的早期终止条件：当任何身体部位偏离参考超过 25cm、物体偏离超过 10cm、非预期接触丢失超过 10 个连续帧、或接触在参考释放后持续超过 0.4 秒时，立即终止回合。消融实验（Table 1）表明，紧密早期终止是最重要的设计决策——移除后测试成功率从 60.2% 下降至 51.8%。

### 蒸馏策略的架构选择

在第二阶段蒸馏中，MaskedManipulator 探索了三种策略架构（Figure 4）：C‑VAE、Deterministic 和 Diffusion。实验表明，Diffusion 策略在多模态行为建模方面具有显著优势：在遥操作任务上，Diffusion 策略成功率达 58.2%，而离线 DAgger 训练（无自我博弈）的 Diffusion 策略仅 25.5%（Table 2）；在长程物体目标运输任务上，Diffusion 同样取得最高成功率（Table 3）。C‑VAE 和 Deterministic 架构在多模态解的表达能力上不及 Diffusion，导致泛化性能下降。

### 数据处理的配套创新

为支持统一的全身操作学习，MaskedManipulator 还引入了物体重定向优化（Figure 3），通过最小化原始接触点与物体接触坐标的绝对差，将不同受试者的运动映射到单一标准人体模型（mean SMPL-X），同时保持交互一致性。这一数据处理管线是两阶段学习得以有效运行的基础保障。

MaskedManipulator 采用**两阶段学习范式**来化解精确控制与通用泛化之间的根本矛盾。第一阶段训练一个基于物理的运动跟踪器 **MimicManipulator**，从密集参考运动数据中学习丰富的精确交互策略；第二阶段通过在线教师-学生蒸馏，将跟踪器的交互知识迁移到通用生成策略 **MaskedManipulator**，使其仅凭稀疏时空目标即可生成多样化、物理合理的全身操作行为。

### 两阶段 Pipeline

**阶段一：MimicManipulator — 密集目标下的运动跟踪**

MimicManipulator 是一个基于强化学习训练的运动跟踪器，目标是从参考运动学数据中精确重建全身物体操作序列。其输入为完整的密集参考轨迹（包含人体关节位姿和被操纵物体的位姿），输出为驱动人体模型在物理模拟器中复现该序列的动作。核心设计包括：

- **乘法奖励结构**：跟踪奖励由姿态、接触、能量和交互四项相乘构成 $R_{\mathrm{track}} = r^{\mathrm{pose}} \cdot r^{\mathrm{contact}} \cdot r^{\mathrm{energy}} \cdot r^{\mathrm{interaction}}$，其中姿态误差进一步分解为人体和物体的平移与旋转误差 $r^{\mathrm{humanoid}} = r^{\mathrm{ht}} \cdot r^{\mathrm{hr}}$ 和 $r^{\mathrm{obj}} = r^{\mathrm{ot}} \cdot r^{\mathrm{or}}$。任何一项失败都会导致整体奖励归零，形成严格的联合约束。
- **三阶段接触奖励**：将物体交互过程分为接近（Approach）、接合（Engagement）和释放（Release）三个阶段，每个阶段对应不同的接触引导目标，引导策略在接触建立、维持和脱离过程中保持精确的时空对齐。
- **紧密早期终止**：设定严格的可行性包络——人体部位偏离参考超过 25cm、物体偏离超过 10cm、非预期接触丢失超过 10 帧、或接触在参考释放后持续超过 0.4 秒，均立即终止回合。这一设计是 MimicManipulator 成功的最关键因素：移除后成功率从 60.2% 下降至 51.8%。

**阶段二：MaskedManipulator — 稀疏目标下的通用生成**

MaskedManipulator 通过在线 DAgger 蒸馏从 MimicManipulator 获取交互知识。在每个时间步，学生策略 $\pi_{\mathrm{versatile}}$ 接收当前状态 $s_t$ 和**随机掩码后的未来参考轨迹** $g_t^{\mathrm{versatile}}$ 作为稀疏目标条件，蒸馏目标为最小化学生动作与教师动作之间的负对数似然 $\mathcal{L}_{\mathrm{distill}} = -\log \pi_{\mathrm{versatile}}(a_t^{\mathrm{track}} | s_t, g_t^{\mathrm{versatile}})$。在线自我博弈机制使学生策略在训练中不断遇到自身诱导的状态分布，对泛化至关重要：离线 DAgger 训练（无自我博弈）导致 Diffusion 策略在遥操作任务上成功率从 58.2% 骤降至 25.5%。

### 目标条件扩展

MaskedManipulator 的核心创新之一是将 spatio-temporal goal-conditioning 从人体部位扩展到被操纵物体。继承自 **MaskedMimic**（Tessler et al., TOG 2024）的掩码目标机制原本仅支持人体部位目标，本文将其推广为同时涵盖人体部位（如手腕、头部）和物体位姿的统一条件接口，使用户可以通过稀疏指定“物体何时到达何处”来驱动全身操作行为。

### 数据处理管线

在训练前，原始运动捕捉数据经过统一的处理流程：
- **运动重定向**：将不同受试者的运动映射到单一标准人体模型（mean SMPL-X），消除形态差异。
- **物体轨迹优化**：通过最小化原始接触点与物体接触坐标的绝对差 $\boldsymbol{p}^* = \operatorname*{argmin}_{\boldsymbol{p}} \sum_{\boldsymbol{j} \in \mathrm{ContactLinks}} \left| \left( \hat{c}_{\boldsymbol{j}, t}^{\mathrm{original}} - \hat{c}_{\boldsymbol{j}, t}^{\mathrm{obj}} \right) \right|$，重定向物体轨迹以保持交互一致性。
- **数据过滤**：排除依赖非手部交互（如面部、脚）或高度复杂双手操作的动作，最终得到 1007 条训练序列和 141 条测试序列（GRAB subject 10）。

### 策略架构

MaskedManipulator 探索了三种架构变体：C-VAE、Deterministic 和 Diffusion 策略。其中 Diffusion 策略通过迭代去噪从高斯噪声中生成动作，在多模态解空间（如遥操作和长程物体目标）上取得最高成功率，显著优于 C-VAE 和确定性架构。

### 模块关系总结

```
运动捕捉数据
    │
    ▼
[数据处理管线] ──► 重定向人体 + 优化物体轨迹
    │
    ▼
[MimicManipulator] ──► 密集目标跟踪，学习精确交互策略（教师）
    │
    │ 在线 DAgger 蒸馏
    ▼
[MaskedManipulator] ──► 稀疏目标生成，通用全身操作（学生）
```

两阶段设计的关键因果机制在于：先在信息完备的环境下掌握“如何精确操作”，再通过掩码蒸馏迫使策略学会从稀疏提示中推断缺失的交互细节，从而在灵活性和精确性之间取得平衡。

### 补充图表

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2505_19086/figures/004_Figure_3.jpg]]
*Figure 3: Object Retargeting for Morphological Differences. Transferring motion between characters of varying shapes can misalign human-object interactions (left). Our method leverages original contact data to retarget the object’s trajectory, preserving interaction consistency (right)*

MaskedManipulator 的核心架构由两个级联模块构成，分别对应两阶段学习范式中的**密集目标跟踪**与**稀疏目标蒸馏**。

### MimicManipulator：基于物理的运动跟踪器

第一阶段训练一个统一的运动跟踪策略 $\pi_{\text{track}}$，即 MimicManipulator。该策略在完全可观测的强化学习设定下，从运动捕捉参考数据中学习推断动作，以在物理模拟中精确重建全身物体操作序列。其核心训练目标由乘法组合的跟踪奖励函数驱动：

$$R_{\mathrm{track}} = r^{\mathrm{pose}} \cdot r^{\mathrm{contact}} \cdot r^{\mathrm{energy}} \cdot r^{\mathrm{interaction}}$$

其中各项含义如下：
- **$r^{\mathrm{pose}}$**：姿态误差项，由人体与物体的平移和旋转误差组成。具体地，人体姿态奖励 $r^{\mathrm{humanoid}} = r^{\mathrm{ht}} \cdot r^{\mathrm{hr}}$，物体姿态奖励 $r^{\mathrm{obj}} = r^{\mathrm{ot}} \cdot r^{\mathrm{or}}$，分别衡量平移（translation）和旋转（rotation）与参考运动的偏差。
- **$r^{\mathrm{contact}}$**：三阶段接触奖励，是 MimicManipulator 实现精确物体交互的关键设计（见 Figure 2）。该奖励将接触过程分解为三个连续阶段：
  - **接近阶段（Approach）**：跟踪参考运动的同时，将手部路径对齐到物体表面。
  - **接合阶段（Engagement）**：确保关键接触点按参考运动的要求得以维持。
  - **释放阶段（Release）**：促使物体在参考运动指定的时机平滑、及时地脱离接触。
- **$r^{\mathrm{energy}}$**：能量效率项，约束策略生成的动作不过度消耗能量。
- **$r^{\mathrm{interaction}}$**：交互一致性项，惩罚非预期的接触丢失或穿透等物理不合理行为。

为保障跟踪质量，MimicManipulator 采用严格的**早期终止条件**：当任何人身体部位与参考偏差超过 25 cm、物体偏差超过 10 cm、非预期接触丢失持续超过 10 帧、或接触在参考释放后仍保持超过 0.4 秒时，立即终止当前回合。消融实验（Table 1）表明，移除该紧密终止条件后，测试成功率从 60.2% 下降至 51.8%，证实其作为最关键设计组件的作用。

此外，数据预处理管线通过**物体重定向优化**解决不同受试者形态差异导致的交互错位问题（见 Figure 3）。给定原始运动中的接触点信息，该优化通过最小化原始接触坐标与物体表面接触坐标的绝对偏差，求解物体平移偏移量 $\boldsymbol{p}^*$：

$$\boldsymbol{p}^* = \operatorname*{argmin}_{\boldsymbol{p}} \sum_{\boldsymbol{j} \in \mathrm{ContactLinks}} \left| \left( \hat{c}_{\boldsymbol{j}, t}^{\mathrm{original}} - \hat{c}_{\boldsymbol{j}, t}^{\mathrm{obj}} \right) \right|$$

这确保了将不同受试者的运动映射到单一规范人体模型（mean SMPL‑X）后，人-物交互的接触一致性得以保持。

### MaskedManipulator：通用生成策略的蒸馏

第二阶段通过在线教师-学生蒸馏（基于 DAgger），将 MimicManipulator 的交互知识迁移到通用生成策略 $\pi_{\text{versatile}}$。学生策略在每一步接收当前状态 $s_t$ 和**随机掩码后的未来参考轨迹** $g_t^{\text{versatile}}$ 作为稀疏目标条件，蒸馏目标为最小化学生策略在稀疏目标条件下对教师动作 $a_t^{\text{track}}$ 的负对数似然：

$$\mathcal{L}_{\mathrm{distill}} = -\log \pi_{\mathrm{versatile}}(a_t^{\mathrm{track}} | s_t, g_t^{\mathrm{versatile}})$$

该框架的核心创新在于将 spatio‑temporal goal‑conditioning 的覆盖范围从人体部位扩展到**被操纵物体**，使策略能够仅凭稀疏时空目标（如物体终点位置、手腕轨迹或头部朝向）生成多样化、物理合理且类人的全身操作行为。

在策略架构层面，MaskedManipulator 考察了三种生成式设计（见 Figure 4）：C‑VAE、Deterministic 和 Diffusion。其中 Diffusion 策略通过从高斯噪声迭代去噪生成动作，在多模态解建模方面表现出显著优势——在遥操作任务上成功率（58.2%）远超 C‑VAE 和 Deterministic 架构，离线训练版本（无自我博弈）更是骤降至 25.5%（Table 2），验证了在线 DAgger 蒸馏对泛化的关键作用。

> **需要人工核实**：Diffusion 策略的具体去噪步数在现有材料中标记为“??”，需查阅原文补充。

## 实验与关键发现

### 核心实验设计

MaskedManipulator 的两阶段评估遵循其训练逻辑：第一阶段验证 **MimicManipulator** 从密集参考运动重建全身操作序列的能力；第二阶段检验 **MaskedManipulator** 在稀疏时空目标下生成多样化交互行为的泛化性。所有实验在 Isaac Gym 物理仿真环境中进行，仿真频率 120 FPS，策略控制频率 30 FPS，全局摩擦系数设为 1.5 以补偿刚体模拟与真实软体接触之间的差异。

训练数据来自 GRAB 数据集，经运动重定向与过滤后得到 1007 条训练序列，测试集为受试者 10 的 141 条序列。由于人体模型采用简化的胶囊/盒子碰撞几何体，部分依赖精细指尖接触的动作（如佩戴眼镜）被排除。

### MimicManipulator 跟踪性能

MimicManipulator 的核心指标为**全序列成功率**（Full-Sequence Success Rate），要求整个序列中人体各部位偏差不超过 25 cm、物体偏差不超过 10 cm，且无连续 10 帧以上的非预期接触丢失。在 GRAB 测试集上，MimicManipulator 成功率达到 **60.2%**，远超基线 **InterMimic**（Xu et al., CVPR 2025）的 **8.5%**（提升 +51.7%，Table 1）。这一巨大差距源于 MimicManipulator 的紧致跟踪设计——严格的早期终止条件、分阶段接触奖励以及优先训练困难样本的策略——而 InterMimic 作为通用全身控制基线，缺乏针对物体交互的专门优化。

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2505_19086/figures/007_Table_1.jpg]]
*Table 1: MimicManipulator: We ablate various design decisions, stripping another component and measuring the cumulative importance. E.g., the “Contact guidance” is without “Tight termination” and “Prioritized scenes”. We also compare with our implementation of InterMimic [Xu et al. 2025] (see Section 6.1)*

Table 1 的消融实验揭示了各设计组件的贡献层级：

- **紧密早期终止**是最关键的设计：移除后成功率从 60.2% 下降至 51.8%（−8.4%）。该终止条件通过强制人体偏差 >25 cm、物体偏差 >10 cm、非预期接触丢失 >10 帧或接触保持 >0.4 秒即终止，将策略探索限制在可行包络内，避免了强化学习从失败状态中学习无效策略的信用分配难题。
- **优先训练困难样本**策略进一步贡献约 3–5% 的成功率增益。该策略在训练中提高对复杂交互序列的采样权重，使策略更专注于难以掌握的接触过渡阶段。
- **分阶段接触奖励**（接近、接合、释放，Figure 2）的移除导致跟踪质量下降。该奖励通过三个阶段引导手部与物体的精确交互：接近阶段跟踪参考运动并保持手部相对于物体表面的路径对齐；接合阶段确保关键接触点按参考维持；释放阶段促进平滑及时的物体脱离。缺失该奖励时，策略难以学习精确的抓取与释放时机。

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2505_19086/figures/003_Figure_2.jpg]]
*Figure 2: Phased contact reward for precise manipulation. We design a three-stage contact reward: (a) Approach: Tracks the reference motion while aligning the hand’s path relative to the object surface. (b) Engagement: Ensures critical contacts are maintained according to the reference. (c) Release: Promotes a smooth and timely object disengagement mirroring the demonstration. The spheres illustrate the reference joints and the arrows illustrate vectors to the closest point on the object’s surface*

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2505_19086/figures/011_Figure.jpg]]
*Figure: (a) Sequential goals: The agent picks up and transports the object to the target position. It reacts to changes in the objective. (b) Solution adaptation: The agent picks up the object with its left hand. It then transfers the object to the right hand for a more natural reaching pose*

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2505_19086/figures/012_Figure.jpg]]
*Figure: (a) Inspecting a large torus: The agent picks up the object with its left hand, holds it with both hands while inspecting, transfers to the right hand, and puts it down. (b) Flying an airplane: Observing only the object position and BPS [Prokudin et al. 2019], the agent “flys” the toy airplane through the air*

### MaskedManipulator 蒸馏与泛化

MaskedManipulator 通过在线 DAgger 蒸馏从 MimicManipulator 获取交互知识。Table 2 的对比实验表明，**在线 DAgger 蒸馏对泛化至关重要**：离线 Diffusion 策略（无自我博弈）在遥操作任务上的成功率仅为 **25.5%**，而在线版本达到 **58.2%**。这一差距揭示了离线蒸馏的分布偏移问题——学生策略在推理时面临的状态分布与教师轨迹的静态分布显著不同，而在线 DAgger 通过学生策略自我博弈收集状态、由教师提供纠正动作，有效缩小了这一分布差距。

在策略架构方面，Table 2 和 Table 3 比较了三种架构变体：

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2505_19086/figures/009_Table_3.jpg]]
*Table 3: Object goals: The agent is provided a sparse objective indicating where (and when) it should transport the object to*

- **Diffusion 策略**在多模态解空间上表现最优，在遥操作和长程物体目标任务上均取得最高成功率。
- **C‑VAE 策略**和 **Deterministic 策略**在多模态交互（如不同抓取方式）上泛化能力不足。C‑VAE 的简化编码器设计——将先验网络的输出直接作为编码器的输入，而非原始参考与目标——虽然降低了计算开销，但可能限制了潜在空间的表达能力。

Table 3 展示了物体目标条件下的性能：策略仅接收稀疏的物体终点位置和到达时间，即可生成物理合理的搬运行为。定性结果（Figure 7）显示，策略能应对顺序目标变化（拾取并搬运至目标位置），并自适应调整解决方案（如左手拾取后换至右手以达成更自然的伸展姿态）。Figure 8 进一步展示了生成性交互能力，包括检查大型圆环时的双手传递操作，以及仅凭物体位置和基础点集表示“飞行”玩具飞机的行为。

### 失败模式与局限性

Figure 9 展示了不当奖励和物理参数导致的穿透问题：当接触奖励权重失衡或摩擦系数设置不当时，手指会穿透物体表面而非形成稳定接触。这暴露了简化碰撞几何体（胶囊/盒子）在模拟人手软体接触动力学方面的固有局限。

此外，基于离散规则的早期终止条件在接触开始或释放阶段可能导致不自然行为——策略为满足严格的偏差阈值，可能产生急促的抓取或释放动作，缺乏平滑过渡。数据过滤排除了依赖非手部交互（如面部、脚部接触物体）或高度复杂的双手操作，限制了通用性。当前的物体重定向方法主要适用于手部中心的操作，未考虑与其他身体部位的交互，这构成了方法向全身任意接触点扩展的障碍。

### 关键图表结论摘要

- **Table 1**：MimicManipulator 以 60.2% 成功率远超 InterMimic 的 8.5%；紧密早期终止是最重要设计组件（移除后 −8.4%），分阶段接触奖励和优先训练策略均有显著贡献。
- **Table 2**：在线 DAgger 蒸馏是泛化的关键，离线版本成功率从 58.2% 骤降至 25.5%；Diffusion 策略在多模态解上优于 C‑VAE 和 Deterministic 架构。
- **Table 3**：Diffusion 策略在稀疏物体目标条件下取得最高成功率，验证了其处理长程目标条件任务的能力。
- **Figure 7–8**：定性证明了策略在顺序目标变化、自适应抓取切换和生成性交互方面的灵活性。
- **Figure 9**：揭示了简化物理模型在精细接触建模上的失败模式，需手动验证具体参数敏感性。

### 补充图表

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2505_19086/figures/010_Table.jpg]]

## 定位与知识库关联

### 问题定位：精确跟踪与通用生成的根本矛盾

精确全身物体操作要求高精度控制，而通用任务需要灵活适应稀疏的高层目标，两者存在根本矛盾。直接从稀疏目标学习面临巨大解空间和信用分配难题——策略必须同时推断身体姿态、手部交互和物体动力学，而奖励信号仅在任务完成时出现。MaskedManipulator 的核心洞察在于：**先利用运动捕捉数据训练跟踪策略掌握丰富的精确交互知识，再通过掩码目标蒸馏将其迁移到通用生成策略**，使得仅凭稀疏时空目标（如物体终点位置）即可生成多样化、物理合理且类人的全身操作行为。

### 与先前工作的关系

**MaskedMimic** (Tessler et al., TOG 2024) 是本文最直接的前身，提出了统一的基于物理的人体控制器，通过时空目标条件化实现对人体部位的控制。MaskedManipulator 在其基础上进行了两个关键扩展：

| 设计维度 | MaskedMimic | MaskedManipulator |
|---------|-------------|-------------------|
| 目标条件化范围 | 仅人体部位 | 人体部位与被操纵物体 |
| 训练范式 | 单阶段跟踪 | 两阶段：MimicManipulator 跟踪 + MaskedManipulator 蒸馏 |

**InterMimic** (Xu et al., CVPR 2025) 是物理人-物交互的通用全身控制基线。在 GRAB 测试集上，MimicManipulator 的完整序列成功率达到 60.2%，而 InterMimic 仅为 8.5%（Table 1），差距达 +51.7%。这一悬殊差距揭示了 InterMimic 的设计瓶颈：其宽松的终止条件和缺乏分阶段接触引导使其难以处理需要精确手-物协调的长程操作序列。

**OmniGrasp** (Luo et al., NeurIPS 2024) 是基于密集目标的全身体抓取方法，依赖完整的参考运动进行跟踪，不适合仅给定稀疏物体目标的长程 goal-conditioned 任务。MaskedManipulator 通过蒸馏机制弥补了这一鸿沟，使策略能从稀疏目标中推断完整的交互行为。

### 方法适用边界

**适用场景**：
- 以手部为中心的单手或双手物体操作（抓取、搬运、使用工具）
- 需要从稀疏高层目标生成多样化交互行为的任务
- 遥操作模拟：给定头部和物体姿态，策略自动推断身体和手部动作

**不适用或表现受限的场景**：
- 依赖非手部交互的操作（如面部接触、脚部操控物体），当前物体重定向方法主要适用于手部中心的操作
- 高度复杂的双手协调操作，数据过滤已排除了部分极端复杂序列
- 精细手指操作（如佩戴眼镜），人体模型使用简化的胶囊/盒子碰撞几何体，无法完全复现真实人手的软体接触动力学
- 训练数据中未见的物体类别和交互类型，策略泛化能力受限于动作捕捉数据的覆盖范围

**物理模拟假设**：所有实验采用统一人体模型（mean SMPL-X），全局摩擦系数设为 1.5，以减轻刚体模拟与软体交互之间的差异。这些简化可能在需要精确接触力建模的场景中引入偏差。

### 关键局限与开放问题

**已知局限**：
1. **离散终止条件的不自然过渡**：基于规则的早期终止条件（人体偏差 >25cm，物体偏差 >10cm，非预期接触丢失 >10 帧，接触保持 >0.4s）可能导致接触开始或释放时偶尔出现不自然行为，缺乏平滑过渡机制。
2. **碰撞几何体的简化**：胶囊/盒子碰撞体无法复现真实人手的软体接触动力学，某些精细操作难以重建。
3. **数据驱动的覆盖限制**：数据过滤排除了依赖非手部交互或高度复杂双手操作的动作，单一策略的表达能力在极长且复杂的序列上仍有不足。
4. **物体重定向的适用范围**：当前方法主要适用于手部中心的操作，未考虑与其他身体部位（如面部、脚）的交互。

**开放问题**：
- 能否用可学习的终止条件替代人工设计的离散终止，使接触过渡更加自然？
- 如何在不依赖大规模动作捕捉数据的情况下，将策略泛化到训练中未见的物体类别和交互类型？
- Diffusion 策略相对于 C‑VAE 的优势在什么条件下最为显著，其迭代去噪生成过程如何影响物理交互的稳定性？
- 能否扩展控制接口，允许用户指定更精细的交互细节，例如物体表面上的精确接触点？
- 如何提升单一策略对极端复杂序列的重建保真度，例如通过更大的模型容量或分阶段训练？

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2025/MaskedManipulator_Versatile_Whole_Body_Manipulation.pdf]]
