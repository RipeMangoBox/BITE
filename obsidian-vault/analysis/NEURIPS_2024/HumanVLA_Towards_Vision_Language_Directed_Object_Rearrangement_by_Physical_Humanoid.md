---
title: "HumanVLA: Towards Vision Language Directed Object Rearrangement by Physical Humanoid"
type: paper
paper_level: A
venue: NEURIPS
year: 2024
pdf_ref: paperPDFs/NEURIPS_2024/HumanVLA_Towards_Vision_Language_Directed_Object_Rearrangement_by_Physical_Humanoid.pdf
code_link: https://github.com/AllenXuuu/HumanVLA
aliases:
- HumanVLA
tags:
- NEURIPS_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过教师-学生框架，先利用目标条件强化学习和对抗运动先验训练状态教师策略，并引入几何编码、搬运课程、风格奖励裁剪、路径规划四项改进以处理多样化物体动力学；再将教师策略通过行为克隆蒸馏为基于自我中心视觉和自然语言指令的视觉-语言-动作模型，并采用主动渲染提高感知质量。
primary_logic: 物理人形机器人可以通过教师-学生框架，将特权状态下的状态策略有效蒸馏到视觉语言模型，结合主动渲染机制和多种训练技巧（风格奖励裁剪、搬运课程学习、路径规划），实现由视觉和语言指导的通用物体重排。
claims:
- 在盒子重排任务上，HumanVLA-Teacher的成功率达到98.1%，精度4.2 cm，均优于InterPhys基线。
- 在未见任务上，HumanVLA成功率为60.2%，远高于Offline GC-BC的10.2%，且消融表明去除主动渲染导致成功率下降6.9%。
- 消融实验表明，去除几何编码或搬运课程使成功率下降约20%；去除风格奖励裁剪下降6%；去除路径规划下降18.5%。
- 学习曲线显示，风格奖励裁剪加快任务收敛，主动渲染提高学生策略的感知质量和学习效率。
---

# HumanVLA: Towards Vision Language Directed Object Rearrangement by Physical Humanoid

> [!tip] 核心洞察
> 物理人形机器人可以通过教师-学生框架，将特权状态下的状态策略有效蒸馏到视觉语言模型，结合主动渲染机制和多种训练技巧（风格奖励裁剪、搬运课程学习、路径规划），实现由视觉和语言指导的通用物体重排。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向视觉语言引导的物理人形机器人物体重排的HumanVLA |
| 英文题名 | HumanVLA: Towards Vision Language Directed Object Rearrangement by Physical Humanoid |
| 会议/期刊 | NEURIPS 2024 |
| Links |  [Code](https://github.com/AllenXuuu/HumanVLA)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | HumanVLA |
| Dataset | Box Rearrangement, Unseen Tasks |

> [!tip] 效果简介
> - Box Rearrangement (HITR subset) 上，Success Rate (%) ↑ 98.1 vs 97.8 (InterPhys†) (+0.3)；Precision (cm) ↓ 4.2 vs 12.6 (InterPhys†) (-8.4)；Execution Time (s) ↓ 4.6 vs 5.3 (InterPhys†) (-0.7)。
> - Unseen Tasks (HITR test split) 上，Success Rate (%) ↑ 60.2 vs 10.2 (Offline GC-BC) (+50.0)；Precision (cm) ↓ 57.0 vs 152.3 (Offline GC-BC) (-95.3)；Execution Time (s) ↓ 5.8 vs 8.5 (Offline GC-BC) (-2.7)。

## 概述

物理人形机器人在真实世界中完成通用物体重排任务，需要同时理解视觉场景与自然语言指令，并适应多样化的物体动力学。现有方法普遍依赖特权状态信息（如精确的物体姿态与目标坐标），且仅能处理单一或静态物体，无法应对由视觉语言指令指定的复杂重排场景。

针对这一瓶颈，本文提出 **HumanVLA**，一个面向物理人形机器人的视觉-语言-动作模型。其核心思路是通过教师-学生框架，将基于特权状态信息训练的高性能策略蒸馏到仅依赖自我中心视觉与自然语言指令的学生模型中。具体而言，先利用目标条件强化学习与对抗运动先验训练状态教师策略 **HumanVLA-Teacher**，并引入几何编码、搬运课程预训练、风格奖励裁剪和路径规划四项改进来处理多样化物体动力学；再通过 DAgger 在线行为克隆将教师策略蒸馏为 **HumanVLA** 学生模型，同时采用主动渲染机制提升自我中心视觉的感知质量。

在 HITR 基准的盒子重排任务上，HumanVLA-Teacher 达到 98.1% 的成功率与 4.2 cm 的放置精度，显著优于 InterPhys 基线。在未见任务上，HumanVLA 成功率为 60.2%，远高于离线行为克隆基线的 10.2%。消融实验表明，几何编码与搬运课程各贡献约 20% 的成功率提升，路径规划贡献 18.5%，主动渲染与在线学习分别贡献 6.9% 和约 45% 的成功率增益，验证了各组件的有效性。

HumanVLA 首次在物理人形机器人上实现了由视觉和语言联合指导的通用物体重排，为具身智能体的语言引导物理交互提供了新的基准与方法范式。

## 背景与动机

### 物理人形交互的现实需求与技术瓶颈

让通用人形机器人在物理世界中像人类一样，仅凭视觉观察和自然语言指令就能灵活地移动和重排物体，是具身智能领域的长期目标。这一能力对于家庭服务、仓储物流、灾难救援等场景具有重要价值。然而，当前物理人形交互研究面临一个核心瓶颈：**现有方法普遍依赖特权状态信息**，如精确的物体6D姿态和目标坐标，且仅能处理单一物体或静态物体动力学，无法应对多样化物体和通用视觉语言指令驱动的复杂重排任务。

### 现有方法的局限

从方法谱系来看，此前的工作存在明显的维度缺失。如 Table 1 所系统对比的，过往研究在物理模拟、物体交互、物体动力学、语言指令、自我中心视觉、可移动物体数量等关键维度上均存在短板。**InterPhys** 等方法虽能实现物理人形的物体操作，但其策略训练需要精确的目标坐标作为输入，缺乏对自然语言指令和视觉感知的理解能力。**Offline GC-BC** 等离线目标条件行为克隆方法则面临严重的协变量偏移问题，在未见任务上的成功率仅为10.2%（Table 4），几乎不具备泛化能力。

更具体地，现有物理人形交互系统的关键缺口可归纳为：
- **感知层面**：无法从自我中心视觉和自然语言中自主理解任务目标，必须依赖外部提供的精确状态信息。
- **动力学层面**：只能处理单一物体类别（如固定尺寸的盒子），缺乏对不同几何形状、质量和摩擦特性的泛化能力。
- **运动控制层面**：缺乏有效的路径规划和避障机制，难以在复杂场景中安全导航至目标物体。

### 核心研究问题

本文旨在回答一个关键问题：**能否让物理人形机器人摆脱对特权状态信息的依赖，仅通过自我中心视觉和自然语言指令，实现面向多种物体的通用重排？** 这要求系统同时解决视觉语言理解、多样化物体动力学建模、以及鲁棒的全身运动控制三大挑战。

### 技术动机与核心思路

为突破上述瓶颈，HumanVLA 采用**教师-学生框架**作为核心因果调节手段。其基本逻辑是：先利用特权状态信息训练一个高性能的“教师”策略，再将教师的知识蒸馏到仅依赖视觉和语言的“学生”模型中。这一思路的合理性在于，特权状态信息（如物体精确位姿、目标坐标）在模拟器中可以廉价获取，它们为策略学习提供了密集的监督信号；而通过蒸馏，学生模型可以隐式地学会从视觉和语言中推断这些潜在信息，从而在部署时摆脱对特权状态的依赖。

在教师策略训练阶段，HumanVLA-Teacher 结合目标条件强化学习和对抗运动先验（AMP），并引入四项关键改进以处理多样化物体动力学：**几何编码**（通过Basis Point Set编码物体形状）、**搬运课程预训练**（先学习抱起物体的先验）、**风格奖励裁剪**（优先保证任务执行而非运动风格）、以及**上下文路径规划**（基于A*算法生成避障导航路径）。在学生蒸馏阶段，HumanVLA 通过行为克隆将教师策略转化为端到端的视觉-语言-动作模型，并引入**主动渲染**机制使机器人主动调整头部姿态以获取更高质量的操作物体视觉感知。

### 预期贡献

基于上述技术路线，HumanVLA 预期在以下方面实现突破：在已知物体重排任务上达到与特权状态方法相当甚至更优的性能；在未见物体和场景上展现出显著的泛化能力；通过消融实验系统验证各项设计组件的独立贡献。这些成果将为物理人形机器人从“精确编程”走向“视觉语言引导的通用交互”提供一条可行路径。

## 核心创新

HumanVLA 的核心创新在于通过**教师-学生框架**，将依赖特权状态信息的物理人形物体操作能力蒸馏为仅需自我中心视觉和自然语言指令的视觉-语言-动作模型。该框架在教师策略训练中引入四项关键设计以处理多样化物体动力学，并在学生蒸馏阶段引入主动渲染机制以弥补感知信息损失。

### 教师策略的关键创新

状态教师策略 HumanVLA-Teacher 基于目标条件强化学习和对抗运动先验（AMP）训练。与直接从头训练完整重排任务的基线方法不同，HumanVLA 在教师训练中引入了四项 changed slots：

**几何编码（Geometry Encoding）**：基线方法仅使用物体的位置、旋转和速度作为观测，无法区分不同几何形状的物体。HumanVLA 通过 Basis Point Set（BPS）编码物体的几何信息，形成全面的物体观测表示。消融实验表明，去除几何编码后教师成功率从约 85.9% 骤降至 64.5%（‑21.4%），精度恶化至 43.4 cm（Table 3），证明几何感知对多样化物体操作至关重要。

**搬运课程预训练（Carry Curriculum）**：基线方法直接从头训练包含行走、接触和重定位的三阶段重排任务，面临探索困难。HumanVLA 首先进行搬运课程预训练，学习抱起物体的先验知识，其奖励由行走奖励 $r_t^{walk}$ 和接触奖励 $r_t^{contact}$ 组成。预训练后再训练完整重排任务。去除搬运课程导致成功率降至 66.3%（‑19.6%），精度恶化至 73.4 cm（Table 3）。

**风格奖励裁剪（Style Reward Clipping）**：标准 AMP 框架中风格奖励与任务奖励直接加权求和，可能导致运动风格目标与任务目标冲突。HumanVLA 对风格奖励施加自适应上界裁剪，上界 $\xi_t = \max(r^G(g, s_t, s_{t+1}), \xi_{min})$，确保风格奖励不会超过任务奖励。总奖励为 $r_t = w^G r^G(g, s_t, s_{t+1}) + w^S \min(r^S(s_{:t+1}), \xi_t)$。该设计优先保证任务执行，同时保留自然运动特性。去除裁剪后成功率下降 6.0%，且学习曲线（Figure 9）显示裁剪显著加快任务收敛。

**上下文路径规划（In-context Path Planning）**：基线方法无显式路径规划，人形机器人直接向物体位置移动，容易与场景障碍物碰撞。HumanVLA 通过将物体点云投影生成 2D 障碍地图，使用 A* 算法规划从起始位置到物体、再到目标的稀疏导航路径点，逐步引导移动。去除路径规划导致成功率下降 18.5%，精度恶化至 37.2 cm（Table 3），定性结果（Figure 11）显示无路径规划时人形机器人无法绕过障碍物接近目标。

### 视觉-语言蒸馏的关键创新

学生模型 HumanVLA 通过行为克隆将教师策略蒸馏为以自我中心图像和语言指令为输入的视觉-语言-动作模型。核心创新在于**主动渲染（Active Rendering）**机制：

基线方法直接使用教师策略输出的头部姿态作为相机视角，物体可能不在视野中心，导致感知质量下降。HumanVLA 根据物体点云计算期望视角，通过逆运动学生成颈部主动渲染动作 $a_t^{ar}$，并与教师动作按比例混合作为学生监督信号：$a_t^{vla} = (1 - w^{ar}) a_t^{tch} + w^{ar} a_t^{ar}$，混合仅应用于颈部关节。该设计使相机主动关注操作物体，提升视觉感知质量（Figure 3 右对比）。去除主动渲染后 HumanVLA 成功率下降 6.9%，精度恶化至 55.6 cm（Table 3），学习曲线（Figure 10）显示主动渲染加速学生策略学习。

此外，HumanVLA 采用 DAgger 框架进行在线交互学习，通过指数衰减的混合策略减轻协变量偏移。使用离线行为克隆（无 DAgger）导致严重协变量偏移，成功率仅为 15.3%，精度 145.0 cm（Table 3），凸显在线学习的必要性。

### 创新总结

上述六项 changed slots 形成互补体系：几何编码和搬运课程解决多样化物体动力学的感知与操作先验问题；风格裁剪和路径规划分别从奖励设计和导航引导角度提升任务执行效率；主动渲染和在线学习则弥补从特权状态到视觉感知的信息损失。这些设计共同支撑 HumanVLA 在盒子重排任务上达到 98.1% 成功率和 4.2 cm 精度，在未见任务上达到 60.2% 成功率，远超 Offline GC-BC 的 10.2%。

## 整体框架

HumanVLA 的整体框架采用**教师-学生蒸馏**范式，将依赖特权状态信息的状态教师策略，转化为仅以自我中心视觉和自然语言指令为输入的视觉-语言-动作（VLA）学生模型。

### 两阶段训练流程

**第一阶段：状态教师策略训练（HumanVLA-Teacher）**
在 IsaacGym 物理仿真环境中，利用目标条件强化学习（Goal-Conditioned RL）和对抗运动先验（Adversarial Motion Prior, AMP），在生成对抗模仿学习（GAIL）范式下训练状态教师策略。教师策略接收完整的特权状态信息，包括物体精确姿态、目标坐标、人形机器人本体状态等。为处理多样化物体动力学并提升策略鲁棒性，教师训练引入了四项关键改进：**几何编码**通过 Basis Point Set（BPS）编码物体几何信息；**搬运课程预训练**先学习抱起物体的先验技能；**风格奖励裁剪**优先保证任务执行；**上下文路径规划**使用 A* 算法生成导航路径点。教师策略输出全身关节动作，作为后续蒸馏的监督信号来源。

**第二阶段：视觉-语言学生蒸馏（HumanVLA）**
通过行为克隆（Behavior Cloning）将教师策略蒸馏为学生 HumanVLA 模型。学生模型仅接收自我中心相机图像和自然语言指令，输出全身动作。训练采用 DAgger 在线学习框架，通过指数衰减的混合策略逐步引入学生自主交互，减轻协变量偏移问题。同时引入**主动渲染**机制：根据物体点云计算期望相机视角，通过逆运动学生成颈部主动渲染动作，与教师动作按比例混合作为监督信号（仅作用于颈部关节），显著提升自我中心视角下的人-物关系感知质量。

### 数据流与模块关系

整个 pipeline 的数据流可概括为：

1. **环境感知** → 物理仿真环境提供人形机器人状态、物体状态及场景点云。
2. **路径规划模块** → 基于物体点云投影生成 2D 障碍地图，使用 A* 算法规划从初始位置到物体、再到目标位置的稀疏导航路径点，作为教师策略的条件输入。
3. **教师策略推理** → 接收状态观测、目标条件及路径点，输出全身关节动作 $a_t^{tch}$。
4. **主动渲染模块** → 根据物体位置计算期望颈部姿态，生成主动渲染动作 $a_t^{ar}$，与教师动作混合得到学生监督信号 $a_t^{vla} = (1 - w^{ar}) a_t^{tch} + w^{ar} a_t^{ar}$（见 Eq. 5）。
5. **学生策略学习** → 以自我中心图像和语言指令为输入，模仿混合动作监督，通过 DAgger 在线交互逐步提升自主执行能力。

该框架实现了从“特权状态下的专家策略”到“通用视觉-语言驱动策略”的有效知识迁移，使物理人形机器人能够在未见物体和未见任务场景下，仅凭视觉和语言指令完成物体重排。

### 补充图表

![[assets/figures/papers/paper_list_l1792_HumanVLA_Towards_Vision_Language_Directed_Object_Rearrangement_by_Physic/figures/003_Figure_2.jpg]]
*Figure 2: An overview of learning state-based HumanVLA-Teacher policy using goal-conditioned reinforcement learning and adversarial motion prior*

![[assets/figures/papers/paper_list_l1792_HumanVLA_Towards_Vision_Language_Directed_Object_Rearrangement_by_Physic/figures/004_Figure_3.jpg]]
*Figure 3: Left: An overview of learning HumanVLA by mimicking teacher action and active rendering action. Right: Comparison between w/ and w/o active rendering. Active rendering leads to a more informative perception of human-object relationships*

## 核心模块与公式推导

HumanVLA 采用教师-学生框架，分两阶段构建：先训练一个依赖特权状态信息的教师策略，再将其蒸馏为仅依赖自我中心视觉与自然语言指令的学生模型。整体架构由四个核心模块构成：**状态教师策略训练**、**视觉-语言学生蒸馏**、**主动渲染模块**和**路径规划模块**。

### 3.1 状态教师策略训练

教师策略 HumanVLA-Teacher 基于目标条件强化学习与对抗运动先验（AMP）训练。AMP 通过判别器区分参考运动数据与策略生成的运动，迫使策略合成自然运动。判别器训练目标为：

$$
\underset{D}{\arg\min} -E_{d^M(s_{t:t+t^*})}[\log(D(s_{t:t+t^*}))] - E_{d^\pi(s_{t:t+t^*})}[\log(1-D(s_{t:t+t^*}))] + w^{gp} E_{d^M(s_{t:t+t^*})}[||\nabla_\phi D(\phi)|_{\phi=s_{t:t+t^*}}||^2]
$$

其中 $d^M$ 为参考运动分布，$d^\pi$ 为策略生成的运动分布，$t^*$ 为时间窗口长度，$w^{gp}$ 为梯度惩罚系数。判别器输出的风格奖励定义为：

$$
r^S(s_{:t+1}) = -\log(1 - D(s_{t+1-t^*:t+1}))
$$

该奖励鼓励策略生成与参考运动风格一致的关节轨迹。总奖励为任务奖励与风格奖励的加权和。

为处理多样化物体动力学，教师策略引入四项关键改进：

**几何编码**：通过 Basis Point Set (BPS) 编码物体几何信息，将任意形状物体的表面点云映射为固定维度的特征向量，形成全面的物体观测。

**搬运课程预训练**：先进行包含行走和接触的搬运课程预训练，学习抱起物体的先验，再训练完整重排任务。搬运课程的总奖励为：

$$
r_t = r_t^{walk} + r_t^{contact}
$$

其中行走奖励 $r_t^{walk}$ 鼓励人形走向物体并按路径点方向移动，接触奖励 $r_t^{contact}$ 鼓励双手接触物体并将其抬起。

**风格奖励裁剪**：为避免风格奖励压倒任务奖励，对风格奖励施加上界裁剪。上界取任务奖励与最小界限的最大值：

$$
\xi_t = \max(r^G(g, s_t, s_{t+1}), \xi_{min})
$$

裁剪后的总奖励为：

$$
r_t = w^G r^G(g, s_t, s_{t+1}) + w^S \min(r^S(s_{:t+1}), \xi_t)
$$

其中 $r^G$ 为任务奖励，$w^G$ 和 $w^S$ 分别为任务和风格奖励的权重，$\xi_{min}$ 为预设的最小界限。

**上下文路径规划**：通过物体点云投影生成 2D 障碍地图，使用 A* 算法规划从起点到物体、再从物体到目标的稀疏导航路径点，逐步引导人形移动。

### 3.2 视觉-语言学生蒸馏

学生模型 HumanVLA 通过行为克隆从教师策略蒸馏，输入为自我中心图像和自然语言指令，输出为关节动作。为缓解协变量偏移，采用 DAgger 框架在线交互收集数据，通过指数衰减的混合策略逐步从教师主导过渡到学生自主。

**主动渲染模块**：根据物体点云计算期望视角，通过逆运动学生成颈部主动渲染动作 $a_t^{ar}$，并与教师动作按比例混合作为监督信号：

$$
a_t^{vla} = (1 - w^{ar}) a_t^{tch} + w^{ar} a_t^{ar}
$$

其中 $w^{ar}$ 为主动渲染权重，混合仅应用于颈部关节，其余关节完全跟随教师动作。主动渲染使相机主动朝向操作物体，提升自我中心视觉中的人-物关系感知质量。

### 3.3 完整重排奖励

完整重排任务的总奖励由行走、接触和重新定位三部分组成：

$$
r_t = r_t^{walk} + r_t^{contact} + r_t^{relocation}
$$

重新定位奖励 $r_t^{relocation}$ 进一步分解为速度、远距离、近距离和旋转四项子奖励，引导物体从初始位置精确移动到目标位置。

### 补充图表

![[assets/figures/papers/paper_list_l1792_HumanVLA_Towards_Vision_Language_Directed_Object_Rearrangement_by_Physic/figures/012_Figure_8.jpg]]
*Figure 8: An overview of the path planning process. The blue mark denotes the initial position. Red marks denote the path from the initial position to the object. Green marks denote the path from the object to the goal*

![[assets/figures/papers/paper_list_l1792_HumanVLA_Towards_Vision_Language_Directed_Object_Rearrangement_by_Physic/figures/015_Figure_9.jpg]]
*Figure 9: Learning curve comparison w/ and w/o style reward clipping*

![[assets/figures/papers/paper_list_l1792_HumanVLA_Towards_Vision_Language_Directed_Object_Rearrangement_by_Physic/figures/016_Figure_10.jpg]]
*Figure 10: Learning curve comparison w/ and w/o active rendering. The process is dominated by the teacher policy in the early stage with high β and demonstrates the reward upper bound*

## 实验与分析

### 整体实验设计

实验分为两个阶段评估：首先在盒子重排（Box Rearrangement）任务上验证状态教师策略 **HumanVLA-Teacher** 的性能，并与基线 **InterPhys** 对比；随后在未见任务（Unseen Tasks）上评估视觉-语言学生模型 **HumanVLA** 的泛化能力，与离线目标条件行为克隆基线 **Offline GC-BC** 对比。所有实验基于 IsaacGym 仿真器中的 HITR 任务集，每组实验重复 10 次，时间上限统一为 10 秒。考虑到视觉-语言方法仅接收粗粒度自然语言指令而无精确目标坐标，评估时对成功判据做了差异化处理：状态方法成功阈值为 $\theta=20$ cm，视觉-语言方法放宽至 $\theta=40$ cm。

### 盒子重排任务：状态教师策略性能

在盒子重排任务上，HumanVLA-Teacher 取得了 **98.1% 的成功率**，精度达到 **4.2 cm**，执行时间仅 **4.6 s**（Table 2）。与重新实现的 InterPhys 相比，成功率提升 0.3 个百分点，精度提升 8.4 cm（从 12.6 cm 降至 4.2 cm），执行时间缩短 0.7 s。值得注意的是，InterPhys 原论文报告的精度为 8.3 cm，但本文作者重新实现后精度恶化至 12.6 cm，这进一步凸显了 HumanVLA-Teacher 在多样化物体动力学下的鲁棒性优势——InterPhys 仅处理单一盒子物体，而 HumanVLA 面向多种物体类别。

![[assets/figures/papers/paper_list_l1792_HumanVLA_Towards_Vision_Language_Directed_Object_Rearrangement_by_Physic/figures/005_Table_2.jpg]]
*Table 2: Results in box rearrangement. † denotes our implementation*

### 消融实验：各组件贡献分析

Table 3 的消融实验系统性地验证了教师策略和学生策略中各项设计的作用。默认 HumanVLA 配置在盒子重排上的成功率为 74.8%，精度为 42.6 cm。

![[assets/figures/papers/paper_list_l1792_HumanVLA_Towards_Vision_Language_Directed_Object_Rearrangement_by_Physic/figures/006_Table_3.jpg]]
*Table 3: Ablation study*

**教师策略组件消融：**

- **去除几何编码（w/o geometry encoding）** 导致成功率骤降至 64.5%（‑21.4%），精度恶化至 43.4 cm。这表明通过 Basis Point Set (BPS) 编码物体几何信息对处理多样化物体形状至关重要——仅依赖位置、旋转和速度等传统状态不足以泛化到不同几何外形的物体。

- **去除搬运课程预训练（w/o carry curriculum）** 使成功率降至 66.3%（‑19.6%），精度恶化至 73.4 cm。搬运课程通过先学习“走向物体-接触-抱起”这一先验技能，为后续完整重排任务提供了关键的行为基础，跳过了从零开始探索抱起动作的高难度阶段。

- **去除风格奖励裁剪（w/o style clipping）** 使成功率下降 6.0%，精度降至 27.5 cm。风格奖励裁剪通过将运动模仿奖励限制在任务奖励水平以下（$\xi_t = \max(r^G, \xi_{min})$），强制策略在任务执行与自然运动之间优先保证任务完成。Figure 9 的学习曲线进一步表明，风格裁剪显著加快了任务收敛速度。

- **去除路径规划（w/o path planning）** 使成功率下降 18.5%，精度降至 37.2 cm，执行时间延长。路径规划模块通过将物体点云投影生成 2D 障碍地图并使用 A* 算法生成稀疏导航路径点，有效引导人形机器人绕过障碍物接近目标物体。Figure 11 的定性对比显示，无路径引导的策略无法绕开中央桌子接近沙发上的目标，而有路径引导的策略成功学会了规避行为。

![[assets/figures/papers/paper_list_l1792_HumanVLA_Towards_Vision_Language_Directed_Object_Rearrangement_by_Physic/figures/017_Figure_11.jpg]]
*Figure 11: Comparison w/ and w/o path planning. The green humanoid without path guidance fails to get close to the sofa, while the yellow humanoid with path guidance learns to go around the central table. Instruction: Move the pillow to the sofa*

**学生策略组件消融：**

- **去除主动渲染（w/o active rendering）** 使 HumanVLA 成功率下降 6.9%，精度恶化至 55.6 cm。主动渲染通过逆运动学计算颈部期望姿态，使自我中心相机主动关注操作物体，显著提升视觉感知质量。Figure 3 的对比图和 Figure 10 的学习曲线均表明，主动渲染不仅提高了感知信息量，还加速了学生策略的学习效率。

- **去除在线学习（w/o online learning）** 即仅使用离线行为克隆而不用 DAgger 框架，导致严重的协变量偏移，成功率暴跌至 15.3%，精度恶化至 145.0 cm。这验证了在视觉-语言策略蒸馏中，通过指数衰减混合策略在线收集交互数据对于缓解分布偏移是不可或缺的。

### 未见任务泛化：视觉-语言学生模型

在未见任务测试集上（Table 4），HumanVLA 取得了 **60.2% 的成功率**、57.0 cm 的精度和 5.8 s 的执行时间，而 Offline GC-BC 基线成功率仅为 10.2%，精度恶化至 152.3 cm。50 个百分点的成功率差距表明，HumanVLA 的教师-学生蒸馏框架结合主动渲染和在线学习，有效将特权状态下的操作能力迁移到了基于自我中心视觉和自然语言指令的策略中。定性结果（Figure 4）展示了从绿色到黄色的颜色渐变过程，直观呈现了重排任务的逐步执行。

![[assets/figures/papers/paper_list_l1792_HumanVLA_Towards_Vision_Language_Directed_Object_Rearrangement_by_Physic/figures/007_Table_4.jpg]]
*Table 4: Results in unseen tasks*

![[assets/figures/papers/paper_list_l1792_HumanVLA_Towards_Vision_Language_Directed_Object_Rearrangement_by_Physic/figures/008_Figure_4.jpg]]
*Figure 4: Qualitative results. The color transitions from green to yellow as the task progresses*

### 泛化边界与失败模式

Table 7 的未见数据分析揭示了 HumanVLA 的泛化边界：

![[assets/figures/papers/paper_list_l1792_HumanVLA_Towards_Vision_Language_Directed_Object_Rearrangement_by_Physic/figures/018_Table_7.jpg]]
*Table 7: Unseen data analysis*

- **未见文本指令**：成功率保持在较高水平，表明语言编码器对指令表述变化具有一定鲁棒性。
- **未见物体视觉特征/几何**：当物体类别与训练集差异较大时，性能显著下降。例如，训练中未见过的杯子几何类型导致成功率骤降至约 20%，说明模型对物体几何外形的泛化能力有限，BPS 编码虽能缓解但未根本解决该问题。
- **未见场景布局**：场景布局变化对性能的影响相对可控，路径规划模块提供了一定的布局适应能力。

### 局限性与待验证点

当前实验体系存在以下需注意的边界：

- **灵巧操作缺失**：人形机器人模型使用球形手掌，无法完成细小物体的抓取或复杂灵巧操作，这限制了方法在精细操作场景中的适用性。
- **单物体限制**：实验仅覆盖单物体重排任务，未扩展到长时域多物体顺序交互，该场景下的性能尚待验证。
- **物体类别泛化**：对未见几何类型的物体成功率骤降至 20%，该数值来自 Table 7 的分析，但具体测试规模和类别分布需查阅原文确认。
- **InterPhys 复现差异**：InterPhys 原论文报告精度 8.3 cm，本文复现为 12.6 cm，该差异可能源于仿真环境配置或超参数调整，需注意对比的公平性边界。

### 补充图表

![[assets/figures/papers/paper_list_l1792_HumanVLA_Towards_Vision_Language_Directed_Object_Rearrangement_by_Physic/figures/002_Table_1.jpg]]
*Table 1: Comparisons between HumanVLA and past works*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

HumanVLA 的核心定位是**首个面向物理人形机器人的视觉语言引导物体重排方法**，其在方法谱系上同时跨越了物理人形控制、物体交互和视觉语言指令跟随三个领域。与现有工作的关系可从以下维度理解：

**状态教师策略层面**：HumanVLA-Teacher 与 **InterPhys** 构成直接对比。InterPhys 是此前物理人形物体交互的代表性工作，但其依赖特权状态信息（精确物体姿态和目标坐标），且仅能处理单一或静态物体动力学。HumanVLA-Teacher 在相同盒子重排任务上达到 98.1% 成功率、4.2 cm 精度，优于复现的 InterPhys（97.8% 成功率、12.6 cm 精度），精度提升达 8.4 cm（Table 2）。这一差距的核心来源是 HumanVLA 引入的四项关键改进：几何编码（Basis Point Set 编码物体形状）、搬运课程预训练、风格奖励裁剪和路径规划。消融实验表明，去除几何编码使成功率骤降至 64.5%（‑21.4%），去除搬运课程降至 66.3%（‑19.6%），去除路径规划下降 18.5%（Table 3），说明 InterPhys 的瓶颈在于缺乏对多样化物体几何的感知能力和结构化导航引导。

**视觉语言学生策略层面**：HumanVLA 与 **Offline GC-BC**（离线目标条件行为克隆）构成对比。在未见任务上，HumanVLA 成功率为 60.2%，而 Offline GC-BC 仅为 10.2%，精度差距达 95.3 cm（Table 4）。这一巨大差距揭示了离线行为克隆在视觉语言策略中的根本缺陷：协变量偏移导致策略在分布外状态下迅速崩溃。HumanVLA 通过 DAgger 框架在线交互收集数据，以指数衰减的混合策略逐步从教师主导过渡到学生自主，有效缓解了该问题。去除在线学习后，HumanVLA 成功率降至 15.3%（Table 3），进一步验证了在线纠偏对于视觉语言策略的关键性。

**主动渲染的独特贡献**：主动渲染是 HumanVLA 区别于现有视觉语言方法的关键设计。传统方法直接使用教师策略输出的头部姿态，相机视角不受控，导致自我中心图像中物体信息不完整。HumanVLA 根据物体点云计算期望视角，通过逆运动学生成颈部主动渲染动作，并与教师动作按比例混合（Eq. 5），仅在颈部关节上施加混合监督。去除主动渲染使成功率下降 6.9%，精度恶化至 55.6 cm（Table 3），学习曲线（Figure 10）显示主动渲染在训练早期即显著提升感知质量和学习效率。

### 2. 适用边界

HumanVLA 的适用边界由以下设计假设和实验条件界定：

- **物理模拟环境**：所有训练和评估均在 IsaacGym 物理仿真器中进行，尚未在真实人形机器人上验证。仿真到现实的迁移（sim-to-real gap）是潜在障碍。
- **任务类型**：目前仅支持单物体重排任务（从初始位置搬运到目标位置），不支持长时域的多物体顺序交互或复杂灵巧操作。
- **物体类别**：训练和评估基于 HITR 数据集中的家具类物体（沙发、枕头、盒子等）。对未见物体类别的几何和材质泛化有限——当物体类别与训练集差异较大时（如训练中未见过的杯子几何类型），成功率骤降至约 20%（Table 7）。
- **操作方式**：人形机器人模型使用球形手掌，无法完成细小物体的抓取或灵巧操作。这限制了方法向需要精细手指运动的任务扩展。
- **语言指令**：支持自然语言指令指定目标和物体，但指令的复杂度和组合性受限于 HITR 数据集的模板生成方式（Figure 5）。

### 3. 局限与开放问题

**已确认的局限**：

1. **灵巧操作缺失**：球形手掌设计使得方法无法处理需要精确抓取的小物体或需要手指协调的复杂操作。这是物理人形机器人领域的基础设施性限制。
2. **单物体任务限制**：当前框架仅处理单物体重排，缺乏对多物体顺序交互和长期任务规划的支持。路径规划模块（A* 算法）仅用于单次导航，未扩展到多目标序列。
3. **泛化边界明确**：对未见物体几何和材质的泛化能力有限，Table 7 显示在未见物体类别上成功率大幅下降，表明视觉编码器和几何编码的泛化能力是瓶颈。
4. **特权信息依赖的残留影响**：虽然学生策略仅使用视觉和语言输入，但教师策略依赖特权状态信息（精确物体姿态、点云），学生策略的性能上限受教师策略质量约束。

**开放问题**：

1. **显式规划与记忆的整合**：当前路径规划和主动渲染是隐式嵌入在策略中的模块。如何将规划、记忆、导航等模块显式整合为可解释的认知架构，以支持更复杂的长期物体重排与多代理协作，是重要的研究方向。
2. **零样本几何和视觉泛化**：如何在不依赖特权状态信息的前提下，设计更鲁棒的视觉语言模型以实现对未知物体类别的零样本泛化？Table 7 的结果表明这是当前方法的显著短板。
3. **灵巧操作的视觉语言引导**：在不依赖特权状态信息的前提下，能否设计支持复杂灵巧操作的视觉语言模型？这需要在机械手设计、触觉感知和精细动作策略等多个层面取得突破。
4. **真实世界部署**：从仿真到真实物理环境的迁移面临感知噪声、动力学不确定性和实时性要求等挑战，主动渲染在真实相机上的效果也有待验证。

## 原文 PDF

![[paperPDFs/NEURIPS_2024/HumanVLA_Towards_Vision_Language_Directed_Object_Rearrangement_by_Physical_Humanoid.pdf]]
