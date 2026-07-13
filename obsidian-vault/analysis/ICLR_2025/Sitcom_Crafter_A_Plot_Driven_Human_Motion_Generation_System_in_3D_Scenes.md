---
title: Sitcom Crafter A Plot Driven Human Motion Generation System in 3D Scenes
type: paper
paper_level: A
venue: ICLR
year: 2025
pdf_ref: paperPDFs/ICLR_2025/Sitcom_Crafter_A_Plot_Driven_Human_Motion_Generation_System_in_3D_Scenes.pdf
project_link: https://windvchen.github.io/Sitcom-Crafter
code_link: https://github.com/nkeeline/
aliases:
- SCPDHMGS3S
tags:
- ICLR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 自监督场景感知人-人交互模块：通过合成二进制SDF点注入场景信息、采用统一标记点表示、改进数据标准化和分阶段训练，在不增加数据采集成本的前提下有效避免碰撞并实现系统集成。
primary_logic: 通过在现有交互数据上合成SDF点来模拟3D场景约束，使生成器学习避免人与场景碰撞，结合标准化的标记点表示和分阶段物理约束训练，解决了多类型运动生成的集成难题。
claims:
- 在Replica数据集上，我们的方法在人类-人类扰动(HHP)上达到0.1687，显著低于InterGen (0.1774)和ComMDM (0.2712)。
- 在InterHuman数据集上，我们的方法在HSP上达到1.6950，远低于InterGen (6.6408)和ComMDM (6.2802)。
- 改进的数据标准化策略将人-场景扰动(HSP)偏差从4.791降低到1.471。
- 引入SDF条件后，HSP指标从15.897降至1.852，表明自监督场景信息有效减少了碰撞。
---

# Sitcom Crafter A Plot Driven Human Motion Generation System in 3D Scenes

> [!tip] 核心洞察
> 通过在现有交互数据上合成SDF点来模拟3D场景约束，使生成器学习避免人与场景碰撞，结合标准化的标记点表示和分阶段物理约束训练，解决了多类型运动生成的集成难题。

| 字段 | 内容 |
|------|------|
| 中文题名 | Sitcom-Crafter：情节驱动的3D场景人体运动生成系统 |
| 英文题名 | Sitcom Crafter A Plot Driven Human Motion Generation System in 3D Scenes |
| 会议/期刊 | ICLR 2025 |
| Links | [Project](https://windvchen.github.io/Sitcom-Crafter) · [Code](https://github.com/nkeeline/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Sitcom-Crafter |
| Dataset | Replica, InterHuman |

> [!tip] 效果简介
> - Replica (11 scenes, 110 plots) 上，HSP (人-场景扰动) / HHP (人-人扰动) HSP 5.7529, HHP 0.1687 vs Baseline HSP 5.5119, HHP 0.1991; InterGen HSP 9.6035, HHP 0.1774; ComMDM HSP 10... (HSP略高于无交互基线但大幅优于其他；HHP最优)。
> - InterHuman 上，HSP / HHP HSP 1.6950, HHP 0.0742 vs InterGen HSP 6.6408, HHP 0.0989; ComMDM HSP 6.2802, HHP 0.1336; Real HSP 0.0043... (HSP降低70%以上，HHP接近真实数据)。

## 概要

**问题背景** 现有3D场景下的人体运动生成方法各自为政，仅能处理单一运动类型——或为人移动（locomotion）、或为人-场景交互（human-scene interaction）、或为人-人交互（human-human interaction）。缺乏一个统一的多类型运动生成系统。更棘手的是，人-人交互生成方法在设计时并未考虑3D场景约束，导致生成的角色运动频繁与场景物体发生碰撞；同时，不同方法采用各异的身体表示与数据规范，使得系统集成面临严重的兼容性障碍。

**核心方法** Sitcom-Crafter 是一个情节驱动（plot-driven）的3D场景人体运动生成系统，由三个运动生成模块与五个功能增强模块构成。其核心创新在于**自监督场景感知人-人交互模块**：在不增加数据采集成本的前提下，通过在现有交互数据上合成二进制SDF点来模拟3D场景约束，使生成器学会避免人与场景碰撞；配合统一的67标记点身体表示、改进的数据标准化策略以及三阶段分阶段训练，有效解决了多类型运动生成的集成难题。

**关键发现** 实验表明，所提方法在人-人扰动（HHP）和人-场景扰动（HSP）两项物理一致性指标上均显著优于现有方法。在Replica数据集上，HHP达到0.1687，低于InterGen（0.1774）和ComMDM（0.2712）；在InterHuman数据集上，HSP降至1.6950，而InterGen和ComMDM分别为6.6408和6.2802。消融研究进一步揭示：改进的标准化策略将HSP偏差从4.791降至1.471；引入SDF条件后HSP从15.897骤降至1.852；分阶段训练是保证生成质量的关键，合并训练会导致FID从10.251恶化至22以上。

**局限与展望** 当前系统仍存在若干约束：相机姿势需手动设置；人-场景交互类型仅限于坐下、躺下等有限动作；三个生成模块因训练策略和数据集不同，运动过渡仍可察觉；在狭窄空间中物理约束会限制动态交互的丰富性。这些方向为后续研究留下了明确的改进空间。



### 研究背景

生成逼真的三维人体运动是计算机视觉与图形学领域的核心挑战之一，在情景剧创作、虚拟现实、游戏开发等应用中具有重要价值。近年来，随着扩散模型（diffusion models）的快速发展，人体运动生成取得了显著进展，涌现出多种针对特定运动类型的方法：人移动生成（human locomotion generation）、人-场景交互生成（human-scene interaction generation）以及人-人交互生成（human-human interaction generation）。

然而，这些方法长期处于割裂发展状态——每种方法针对单一运动类型设计，采用不同的身体表示、训练策略和数据集，难以直接整合为一个统一的多类型运动生成系统。具体而言，**GAMMA**（Zhang & Tang, 2022）专注于基于路径规划的人移动生成，**DIMOS**（Zhao et al., 2023）处理人与场景物体的交互（如坐下、躺下），而 **InterGen**（Liang et al., 2024）和 **ComMDM**（Shafir et al., 2024）则聚焦于双人交互运动生成。这些方法各自独立运作，缺乏一个能够根据情节上下文协调调度多种运动类型的系统框架。

### 核心瓶颈

现有方法在系统集成层面面临三个关键瓶颈：

**第一，人-人交互生成缺乏3D场景感知能力。** 以InterGen为代表的人-人交互生成方法在生成双人运动时不考虑周围场景信息，导致生成的交互运动在放入3D场景后容易与场景物体发生碰撞。这一问题在Replica数据集上的量化表现为：InterGen的人-场景扰动（HSP）高达9.6035，ComMDM更高达10.5532（Table 1），表明生成的交互运动与场景存在严重冲突。

**第二，不同方法采用不一致的身体表示，造成集成困难。** 人移动生成通常使用SMPL/SMPL-X参数模型，人-场景交互依赖特定的关节表示，而人-人交互生成（如InterGen）则使用包含全局位置、速度、关节旋转和足部接触标签的复合表示 $\mathbf{\tilde{x}}_{i(IG)} = \{ j_q^p, j_q^v, j^r, c^f \}$。这些异构表示使得模块间的运动传递和同步变得异常复杂，阻碍了统一系统的构建。

**第三，多类型运动生成缺乏统一的调度与同步机制。** 即使将各模块强行集成，不同运动类型之间的过渡、时序对齐和物理一致性维护仍面临巨大挑战。特别是当情节涉及“移动→场景交互→人-人交互”的复杂序列时，如何确保角色在正确的时间到达正确的位置、以正确的姿态执行交互，是一个尚未被充分探索的问题。

### 本文动机

针对上述瓶颈，Sitcom-Crafter提出了一套完整的解决方案，核心动机体现在以下三个层面：

1. **构建自监督场景感知的人-人交互生成模块**：通过在现有交互数据上合成二进制SDF点来模拟3D场景约束，使生成器在不增加数据采集成本的前提下学习避免人与场景碰撞。这一设计直接回应了“人-人交互缺乏场景感知”的核心痛点。

2. **采用统一的标记点（marker points）表示贯穿全系统**：以67个标记点作为统一的身体表示格式，取代各模块原本异构的表示方式。这一选择不仅降低了系统集成的复杂度，还通过改进的数据标准化策略（将每个角色的骨盆设为局部原点，将学习目标从67个发散分布简化为1个）显著提升了学习效率。

3. **设计模块化的系统架构与分阶段训练策略**：系统由8个模块组成（3个生成模块 + 5个增强模块），通过情节理解模块实现自然语言指令到运动命令的解析与分发，通过运动同步模块确保不同运动类型间的平滑过渡。在训练层面，采用三阶段分阶段训练策略（Phase1无物理约束、Phase2加入场景碰撞约束、Phase3加入人-人碰撞约束），有效平衡了运动质量与物理一致性。

通过这些设计，Sitcom-Crafter首次实现了在3D场景中根据长情节上下文统一生成人移动、人-场景交互和人-人交互三类运动，为情景剧等应用场景提供了端到端的运动生成系统。



## 核心方法与创新机理

Sitcom-Crafter 的核心创新并非单一算法突破，而是通过**统一表示、自监督场景注入、改进标准化与分阶段训练**四个相互咬合的 changed slots，解决了多类型人体运动生成（移动、人-场景交互、人-人交互）在3D场景中集成时的**表示不一致**与**物理碰撞**两大瓶颈。

### 1. 统一标记点表示：打通多模块集成的“语言”

现有方法各自采用不同的身体表示——**GAMMA** (Zhang & Tang, 2022) 和 **DIMOS** (Zhao et al., 2023) 使用 SMPL/SMPL-X 参数，**InterGen** (Liang et al., 2024) 使用全局位置、速度、关节旋转和足部接触标签的混合表示（$\mathbf{\tilde{x}}_{i(IG)} = \{ j_q^p, j_q^v, j^r, c^f \}$）。这种异构性使得三个生成模块无法直接串联。

Sitcom-Crafter 将**67个标记点（marker points）**作为全系统统一的运动表示。这一选择的关键因果效应是：任何模块的输出都可以作为下一模块的条件输入，无需额外的表示转换层。在 InterHuman 数据集上的实验表明，仅将 InterGen 的表示替换为标记点格式（无其他条件或损失），即可在保持生成质量的同时实现系统集成（Table 3）。

### 2. 自监督场景感知：在不增加采集成本的前提下注入3D约束

人-人交互生成方法（如 InterGen、ComMDM）原本**不具备场景感知能力**，在3D场景中生成的运动容易与场景物体发生穿透。传统方案需要采集带场景标注的交互数据，成本高昂。

Sitcom-Crafter 的解决方案是**自监督合成二进制SDF条件**（Figure 3）：
1. 从现有交互数据中提取可行走区域；
2. 在该区域周围随机采样 $K$ 个几何图案（旋转椭圆、矩形等）模拟障碍物；
3. 在3D空间中分布二进制SDF点网格 $P \in \mathbb{R}^{S_{hor} \times S_{hor} \times S_{ver}}$，根据高度阈值划分地板和天花板点集；
4. 将每个点的位置和SDF值拼接为4维条件向量 $p_{cond} = \{ p_{x,y,z}, p_{value} \}$，注入生成器。

消融实验（Table 5）给出了决定性证据：**引入SDF条件后，人-场景扰动（HSP）从15.897骤降至1.852**，降幅达88%。这证明生成器确实学会了利用合成SDF点来避免与场景物体的碰撞，而整个过程无需任何额外的真实场景标注数据。

### 3. 改进的数据标准化：消除角色间学习偏差

InterGen 的标准化策略将角色A置于全局坐标原点，角色B相对于A定位。这导致角色B的运动分布高度发散（受A位置影响），而角色A始终在原点附近，产生**不对称的学习难度**。

Sitcom-Crafter 改为**以每个角色自身骨盆关节为局部原点**，仅保留骨盆的全局平移信息。这一调整将需要建模的分布从67个发散分布缩减为1个（骨盆平移）。消融实验（Table 4）证实：改进标准化后，HSP偏差从4.791降至1.471，表明两个角色的运动学习更加均衡。

### 4. 分阶段物理约束训练：解决多目标冲突

总损失函数包含9个项（$\mathcal{L} = \mathcal{L}_{MSE} + \mathcal{L}_{DM} + \mathcal{L}_{RO} + \mathcal{L}_{Vel} + \mathcal{L}_{foot} + \mathcal{L}_{scenePene} + \mathcal{L}_{sceneReg} + \mathcal{L}_{humanPene} + \mathcal{L}_{humanReg}$），如果从训练初期就全部施加，物理约束会严重限制运动生成的学习能力。

Sitcom-Crafter 采用**三阶段训练策略**（Table 7）：
- **Phase 1**：仅使用基础损失（无物理约束），让生成器学习运动分布；
- **Phase 2**：加入场景碰撞约束（$\mathcal{L}_{scenePene} + \mathcal{L}_{sceneReg}$）；
- **Phase 3**：加入人-人碰撞约束（$\mathcal{L}_{humanPene} + \mathcal{L}_{humanReg}$）。

实验显示，分阶段训练将FID从合并训练的>22降至10.251，同时HHP从0.0989优化至0.0742（Table 6, 7）。**关键trade-off**：引入人-人碰撞损失后，FID从3.871升至10.251，文本匹配指标也出现下降——物理一致性的提升以运动多样性和文本对齐为代价。

### 创新总结

四个 changed slots 之间存在因果依赖关系：统一标记点表示是系统集成的前提；自监督SDF条件解决了场景感知问题；改进标准化消除了训练偏差；分阶段训练则化解了多目标优化的冲突。这些创新共同使得 Sitcom-Crafter 在 Replica 数据集上达到最优 HHP（0.1687，低于 InterGen 的0.1774和 ComMDM 的0.2712），在 InterHuman 数据集上将 HSP 降低了70%以上（1.6950 vs. InterGen 6.6408）。



Sitcom-Crafter 是一个情节驱动的人体运动生成系统，其核心设计目标是在统一的框架内支持三类人体运动：**人移动**、**人-场景交互**和**人-人交互**。系统由八个模块组成，其中三个负责运动生成，五个负责功能增强，各模块之间通过明确的输入输出流协同工作，最终在给定的3D场景中产出协调的多角色运动序列。

### 系统工作流

系统的整体工作流如 Figure 2 所示。用户提供的情节文本首先进入**情节理解模块 (Plot Comprehension Module)**，该模块利用大语言模型将自然语言情节解析为系统可识别的运动指令，并根据指令类型将其分发至对应的生成模块。三个生成模块按指令顺序依次执行：

![[assets/figures/papers/paper_list_l1784_Sitcom_Crafter_A_Plot_Driven_Human_Motion_Generation_System_in_3D_Scenes/figures/002_Figure_2.jpg]]
*Figure 2: The workflow of Sitcom-Crafter. The Sitcom-Crafter system consists of eight modules, three for motion generation and five for function enhancement. The arrows between modules indicate the workflow direction. The system supports generation guided by 3D scene structure and long plot context. The plot comprehension module is for interpreting the guiding context into recognizable commands and distributing them to the generation modules. The three generation modules synthesize different motion types: human-scene interaction, human locomotion, and human-human interaction. The motion synchronization module ensures motion consistency between the different generation modules. The hand pose retrieval...*

1. **人移动生成模块 (Human Locomotion Generation Module)**：基于 **GAMMA** (Zhang & Tang, 2022) 构建，负责生成角色在场景中的行走、跑动等位移运动。
2. **人-场景交互生成模块 (Human-Scene Interaction Generation Module)**：基于 **DIMOS** (Zhao et al., 2023) 构建，处理角色与场景物体（如坐下、躺下）的交互。
3. **场景感知人-人交互生成模块 (Scene-Aware Human-Human Interaction Generation Module)**：基于 **InterGen** (Liang et al., 2024) 改进，生成两个角色之间的交互运动，并引入自监督场景信息以避免与场景物体的碰撞。

生成模块之间的衔接由**运动同步模块 (Motion Synchronization Module)** 负责，它确保当前模块的生成结果与前一模块的输出在运动状态上保持一致。随后，**手部姿态检索模块 (Hand Pose Retrieval Module)** 通过 CLIP 检索为运动补充手部细节；**碰撞修正模块 (Collision Revision Module)** 对角色间发生穿透的帧进行修正；最后，**运动重定向模块 (Motion Retargeting Module)** 将 SMPL/SMPL-X 参数化模型映射到 Mixamo 提供的高质量3D角色资产上。

### 统一的身体表示

为解决不同方法间表示不一致导致的集成困难，系统全流程采用**统一的67标记点表示**。这一选择使得各模块的输出可以直接作为下游模块的输入，无需额外的格式转换，从而降低了系统集成的复杂度。

### 输入输出流

系统的输入包括三要素：
- **3D场景结构**：提供场景几何信息，用于约束运动的物理合理性；
- **长情节文本**：描述角色的行为序列和交互关系；
- **角色定义**：指定参与运动的角色数量及其初始位置。

输出为多角色在3D场景中的协调运动序列，可直接用于情景剧等应用的渲染。当前系统支持同一楼层内的运动生成，跨楼层交互尚需专门的生成模块支持。

### 补充图表

![[assets/figures/papers/paper_list_l1784_Sitcom_Crafter_A_Plot_Driven_Human_Motion_Generation_System_in_3D_Scenes/figures/008_Figure_6.jpg]]
*Figure 6: Visual illustrations of the generations of the whole system guided by long plots. The plots are shown at the top, with some key motion words highlighted in green. For better illustration, we include two cameras from different angles. Each row, from left to right, shows screenshots captured at different times, progressing from earlier to more recent frames*

![[assets/figures/papers/paper_list_l1784_Sitcom_Crafter_A_Plot_Driven_Human_Motion_Generation_System_in_3D_Scenes/figures/034_Figure_26.jpg]]
*Figure 26: More visual illustrations of the generations of the whole system guided by long plots. The plots are shown at the top, with some key motion words highlighted in green. For better illustration, we include two cameras from different angles. Each row, from left to right, shows screenshots captured at different times, progressing from earlier to more recent frames*



### 系统模块架构

Sitcom-Crafter 由八个模块构成，其中三个负责运动生成，五个负责功能增强（Figure 2）。三个生成模块分别处理人体移动、人-场景交互和人-人交互，其余模块负责情节理解、运动同步、手部姿态检索、碰撞修正和运动重定向。

**情节理解模块**利用语言模型将用户提供的情节文本转化为角色可识别的运动指令序列，并分发给对应的生成模块。指令按类型和执行顺序依次处理，当前模块的运动生成以上一步生成的运动帧为条件，实现运动片段的链式拼接（Figure 7）。

**人体移动生成模块**基于 **GAMMA**（Zhang & Tang, 2022），**人-场景交互生成模块**基于 **DIMOS**（Zhao et al., 2023）。**场景感知人-人交互生成模块**以 **InterGen**（Liang et al., 2024）为基础，但在运动表示、网络条件和训练策略上做了关键修改。

### 场景感知人-人交互模块核心机制

该模块的核心创新在于**自监督场景条件注入**和**改进的数据标准化策略**。

**自监督SDF场景构建**（Figure 3）：从运动数据中提取可行走区域，在该区域周围模拟随机物体（旋转椭圆、矩形等模式），为每个模式内的点列分配统一高度值，最终在3D空间中分布二进制SDF点。SDF点网格定义为：

$$P \in \mathbb{R}^{S_{hor} \times S_{hor} \times S_{ver}}$$

其中 $S_{hor}$ 和 $S_{ver}$ 分别为水平和垂直维度。地板和天花板点集通过高度阈值划分：

$$\{P_{floor}, P_{ceiling}\} = \{ (p_x, p_y, p_z) \mid p_z \leq T_{floor} \lor p_z \geq T_{ceiling} \}$$

每个SDF条件向量由点位置和SDF值拼接为4维向量：

$$p_{cond} = \{ p_{x,y,z}, p_{value} \}$$

**改进的数据标准化**（Figure 4）：原始InterGen将角色A置于全局坐标原点、角色B相对A定位，这导致角色间学习偏差——靠近原点的角色更易建模。改进策略将每个角色的骨盆关节设为局部原点，仅保留骨盆全局平移，将学习难度从67个发散分布降至1个。角色B的运动帧表示为：

$$\pmb{x}_i \in \mathbb{R}^{(67+1) \times 3}$$

即67个标记点位置加1个骨盆关节位置。

**分阶段训练策略**（Appendix B.2）：训练分为三个阶段——Phase1仅使用基础损失（无物理约束），Phase2加入场景碰撞损失，Phase3加入人-人碰撞损失。消融实验表明，合并训练会导致FID从10.251恶化至>22，分阶段策略对收敛至关重要。

### 关键损失函数

总损失函数包含多项约束（Appendix B.2）：

$$\mathcal{L} = \mathcal{L}_{MSE} + \mathcal{L}_{DM} + \mathcal{L}_{RO} + \mathcal{L}_{Vel} + \mathcal{L}_{foot} + \mathcal{L}_{scenePene} + \mathcal{L}_{sceneReg} + \mathcal{L}_{humanPene} + \mathcal{L}_{humanReg}$$

其中场景正则化损失约束标记点间相对距离与真值一致：

$$\mathcal{L}_{sceneReg} = \sum_{j}^{67} \sum_{k}^{67} \left( \| x^{j} - x^{k} \|_1 - \| x_{gt}^{j} - x_{gt}^{k} \|_1 \right)$$

消融实验（Table 6）表明，引入人-人碰撞损失（$\mathcal{L}_{humanPene} + \mathcal{L}_{humanReg}$）后，HHP从0.0989降至0.0742，但FID从3.871升至10.251，提示物理约束与运动质量间存在权衡。

### 运动序列表示

整个系统采用统一的67标记点表示，运动序列定义为N帧标记点序列：

$$\pmb{X} = \{ \pmb{x}_1, \pmb{x}_2, \ldots, \pmb{x}_N \}$$

与之对比，InterGen的运动表示包含全局位置、速度、关节旋转和足部接触标签：

$$\mathbf{\tilde{x}}_{i(IG)} = \{ j_q^p, j_q^v, j^r, c^f \}$$

统一标记点表示使得不同生成模块间的运动衔接无需复杂的表示转换，是实现系统集成的关键设计选择。

### 补充图表


![[assets/figures/papers/paper_list_l1784_Sitcom_Crafter_A_Plot_Driven_Human_Motion_Generation_System_in_3D_Scenes/figures/004_Figure_4.jpg]]
*Figure 4: Illustration of different canonicalization strategies. In this example, character A is initially canonicalized to the global coordinate origin, while character B is positioned relative to character A*

![[assets/figures/papers/paper_list_l1784_Sitcom_Crafter_A_Plot_Driven_Human_Motion_Generation_System_in_3D_Scenes/figures/009_Figure_7.jpg]]
*Figure 7: Workflow within Generation Modules. Given the command lists derived from the Plot Comprehension module, each command is sequentially processed by the corresponding generation module based on its type and order. The motion generation of the current module is conditioned on the motion frames generated in the previous step, ensuring seamless chaining of motion segments. Note that the flowchart provides a simplified overview of the logic within the generation modules. For detailed explanations, please refer to the sections dedicated to each system module*



## 实验与关键发现

### 系统级主结果（Replica 数据集）

Sitcom-Crafter 在 Replica 数据集（11 个场景，110 段情节）上进行了系统级评估，对比对象包括：**Baseline**（仅含移动和场景交互，无人-人交互模块）、**InterGen**（Liang et al., 2024）和 **ComMDM**（Shafir et al., 2024）。评估指标涵盖人-场景扰动（HSP）、人-人扰动（HHP）、足部滑动（FS）和浮动（FP）。如 Table 1 所示，完整系统在 HHP 上达到 **0.1687**，优于 InterGen（0.1774）、ComMDM（0.2712）和 Baseline（0.1991），证明场景感知人-人交互模块有效减少了角色间的穿透。在 HSP 指标上，完整系统（5.7529）略高于 Baseline（5.5119），但远低于 InterGen（9.6035）和 ComMDM（10.5532），表明引入人-人交互后场景碰撞仅轻微增加，且显著优于直接将无场景约束的交互生成器嵌入系统的方案。FS 和 FP 指标上完整系统与 Baseline 持平或略优，说明新增模块未引入额外的足部滑动或浮动问题。

![[assets/figures/papers/paper_list_l1784_Sitcom_Crafter_A_Plot_Driven_Human_Motion_Generation_System_in_3D_Scenes/figures/007_Table_1.jpg]]
*Table 1: Comparisons of Systems with Different Human-Human Interaction Generators on the Replica Dataset. “Baseline” refers to generations without human-human interactions. The best results are highlighted in bold*

### 人-人交互模块独立评估（InterHuman 数据集）

为单独衡量场景感知人-人交互生成模块的质量，在 InterHuman 数据集上与 InterGen 和 ComMDM 进行对比。如 Table 2 所示，Sitcom-Crafter 的 HSP 降至 **1.6950**，相较 InterGen（6.6408）和 ComMDM（6.2802）降低超过 70%，接近真实数据的 0.0043；HHP 达到 **0.0742**，优于 InterGen（0.0989）和 ComMDM（0.1336），甚至略优于真实数据（0.0807）。这表明自监督 SDF 条件与改进的标准化策略在无真实场景标注的情况下，仍能有效约束角色运动，避免与虚拟场景物体和角色间的碰撞。

![[assets/figures/papers/paper_list_l1784_Sitcom_Crafter_A_Plot_Driven_Human_Motion_Generation_System_in_3D_Scenes/figures/006_Table_2.jpg]]
*Table 2: Comparisons with other human-human interaction methods on the InterHuman dataset. “Real” represents the performance of real data. The best results are in bold*

### 标记点表示的有效性

Table 3 比较了标记点格式生成器与其他交互生成器在 InterHuman 数据集上的表现。在仅使用标记点格式、不添加 SDF 条件和碰撞损失的情况下，Sitcom-Crafter 的 FID 达到 **3.871**，优于 InterGen（5.917）和 ComMDM（5.538）；R-Precision Top 1 为 0.602，高于 InterGen（0.509）和 ComMDM（0.566）；多样性（Diversity）为 2.573，略低于 InterGen（2.689）但高于 ComMDM（2.178）。这说明统一的 67 标记点表示本身已具备竞争力，且为后续场景条件注入提供了统一接口。

### 消融研究

#### 标准化策略

Table 4 对比了两种标准化策略：初始方案将角色 A 置于原点、角色 B 相对 A 放置；改进方案将每个角色以自身骨盆为局部原点，仅保留骨盆全局平移。结果显示，改进方案将角色 B 的 HSP 从 4.791 降至 **1.471**，HHP 从 0.0147 降至 0.0114，同时 FID 从 6.768 降至 3.871。这表明原始方案使模型倾向于学习角色 A（位于原点附近）的运动分布，而对角色 B 建模能力不足；改进方案将 67 个标记点的发散分布问题缩减为 1 个（骨盆平移），显著缓解了学习偏差。

![[assets/figures/papers/paper_list_l1784_Sitcom_Crafter_A_Plot_Driven_Human_Motion_Generation_System_in_3D_Scenes/figures/026_Table_4.jpg]]
*Table 4: Comparisons between different canonicalization strategies. “A” represents the character centered around the origin, while “B” represents the character positioned relative to A. “R-P T1” denotes R-Precision Top 1. The best results are highlighted in bold*

#### SDF 条件与运动条件

Table 5 展示了条件和损失的累积消融。在基础运动条件（角色 A 的运动序列）之上添加 SDF 条件后，HSP 从 15.897 骤降至 **1.852**，HHP 从 0.0993 降至 0.0989，验证了自监督场景信息对减少人与场景碰撞的关键作用。进一步添加场景正则化损失 $\mathcal{L}_{sceneReg}$ 后，HSP 继续降至 1.695，HHP 降至 0.0884，但 FID 从 3.871 升至 4.878，提示物理约束与运动质量之间存在权衡。

![[assets/figures/papers/paper_list_l1784_Sitcom_Crafter_A_Plot_Driven_Human_Motion_Generation_System_in_3D_Scenes/figures/027_Table_5.jpg]]
*Table 5: Ablation study of the effectiveness of motion and SDF conditions. Conditions are added cumulatively rather than individually. The best results are highlighted in bold*

#### 损失函数

Table 6 从基础损失（$\mathcal{L}_{MSE} + \mathcal{L}_{DM} + \mathcal{L}_{RO} + \mathcal{L}_{Vel} + \mathcal{L}_{foot}$）出发，逐步添加碰撞相关损失。引入人-人穿透损失 $\mathcal{L}_{humanPene}$ 和人-人正则化损失 $\mathcal{L}_{humanReg}$ 后，HHP 从 0.0989 降至 **0.0742**，但 FID 从 3.871 升至 10.251，R-Precision Top 1 从 0.602 降至 0.537。这一显著退化表明，直接添加人-人碰撞约束会严重限制生成器的运动表达能力，需要更精细的训练策略来平衡物理一致性与运动质量。

![[assets/figures/papers/paper_list_l1784_Sitcom_Crafter_A_Plot_Driven_Human_Motion_Generation_System_in_3D_Scenes/figures/028_Table_6.jpg]]
*Table 6: Ablation study of the effectiveness of different conditions. Losses are added cumulatively rather than individually. “Base Losses” refers to losses excluding collision-related terms as shown in Eq. 3. The best results are highlighted in bold*

#### 训练策略

Table 7 对比了不同训练策略。将 Phase 2（场景约束）和 Phase 3（人-人约束）合并训练（Phase 1 & 2 & 3）导致 FID 飙升至 **22.088**，远差于分阶段训练（FID 10.251）。若仅合并 Phase 1 和 Phase 2（Phase 1 & 2 + Phase 3），FID 为 11.784，仍劣于完全分阶段方案。这表明早期引入物理约束会严重阻碍运动基础能力的学习，分阶段训练是保证最终性能的必要设计。

![[assets/figures/papers/paper_list_l1784_Sitcom_Crafter_A_Plot_Driven_Human_Motion_Generation_System_in_3D_Scenes/figures/029_Table_7.jpg]]
*Table 7: Ablation study of different training strategies. “+” denotes phased training, while “&” denotes merged training phases. The best results are highlighted in bold*

#### 数据规模

Table 8 探索了在 InterHuman 数据之外整合 Inter-X 数据集的效果。整合后 HSP 从 1.852 进一步降至 **1.542**，但 FID 从 3.871 升至 4.689，R-Precision 和多样性指标也出现下降。这说明更大规模的数据有助于改善物理一致性，但可能因数据分布差异导致文本-运动对齐能力下降。

### 失败模式与局限性

1. **碰撞修正的边界失效**：如 Figure 20 所示，在狭窄走廊场景中，碰撞修正模块无法完全避免角色间碰撞。物理约束在受限空间内限制了动态交互的生成空间，导致修正策略失效。

2. **运动多样性不足**：场景感知人-人交互模块虽然显著提升了物理一致性，但未能丰富交互运动的多样性。消融实验中 FID 和文本匹配指标的退化也印证了物理约束对运动表达能力的压制。

3. **模块间过渡不自然**：三个生成模块（移动、人-场景交互、人-人交互）采用不同的训练策略和数据集，导致不同运动类型之间仍存在可察觉的过渡。

4. **交互类型受限**：人-场景交互目前仅限于坐下和躺下等动作，扩展需要更多高质量训练数据；系统仅支持同一楼层内的运动，跨楼层交互需要专门的生成模块。

5. **相机依赖手动设置**：系统缺乏自动化的镜头跟随机制，相机姿势仍需手动配置。



## 定位与知识库关联

### 1. 生成模块的基线继承关系

Sitcom-Crafter 的三个核心运动生成模块分别建立在不同子领域的现有方法之上，体现了“集成优于重构”的系统设计思路：

- **人移动生成模块** 直接基于 **GAMMA**（Zhang & Tang, 2022），继承了其在3D场景约束下生成人体移动运动的能力。该模块负责处理“走、跑、转向”等基础移动指令，是整个系统的运动基础层。
- **人-场景交互生成模块** 基于 **DIMOS**（Zhao et al., 2023），负责生成“坐下、躺下”等与场景物体直接交互的动作。该模块的适用边界受限于训练数据中可用的交互类型，目前仅支持有限的几类动作。
- **人-人交互生成模块** 构建于 **InterGen**（Liang et al., 2024）之上，但进行了五项关键改进：统一标记点表示、自监督场景感知条件、改进的数据标准化策略、分阶段训练策略，以及新增的身体回归器。这些改进使该模块从“无场景约束的双人交互生成器”升级为“场景感知的人-人交互生成器”。

### 2. 对比基线的谱系定位

论文在实验中与以下方法进行了系统级和模块级对比：

- **InterGen**（Liang et al., 2024）：人-人交互生成的直接基线。在Replica数据集上，Sitcom-Crafter的HHP（人-人扰动）为0.1687，优于InterGen的0.1774；在InterHuman数据集上，HSP（人-场景扰动）从InterGen的6.6408降至1.6950，降幅超过70%（Table 1, Table 2）。
- **ComMDM**（Shafir et al., 2024）：另一人-人交互方法。在Replica上HHP为0.2712，在InterHuman上HSP为6.2802，均显著弱于Sitcom-Crafter。
- **Baseline（无人-人交互）**：仅包含移动和人-场景交互模块的系统版本。在Replica上HSP为5.5119，Sitcom-Crafter完整系统为5.7529，略有上升但仍在可接受范围，而HHP从0.1991降至0.1687，表明引入场景感知后碰撞反而减少。

### 3. 关键改进槽位与因果机制

Sitcom-Crafter在人-人交互模块上相对于InterGen的改进，构成了其核心方法贡献：

| 改进槽位 | InterGen基线 | Sitcom-Crafter方案 | 因果效果 |
|---------|-------------|-------------------|---------|
| 身体表示 | 全局位置+速度+关节旋转+足部接触 | 统一67标记点表示 | 实现系统内模块间表示一致性，降低集成复杂度 |
| 场景条件 | 无 | 自监督合成二进制SDF点 | HSP从15.897降至1.852（Table 5），有效减少人-场景碰撞 |
| 数据标准化 | 角色A置原点，B相对A | 各自以骨盆为局部原点 | HSP偏差从4.791降至1.471（Table 4），缓解角色间学习偏差 |
| 训练策略 | 单阶段 | 三阶段分阶段训练 | FID从>22降至10.251（Table 7），避免物理约束过早限制运动学习 |
| 手部姿态 | 默认或无 | CLIP检索增强 | 提升手部表现力，无定量指标但定性改善明显 |

### 4. 适用边界与已知局限

Sitcom-Crafter的设计存在以下明确边界：

- **交互类型受限**：人-场景交互目前仅支持坐下和躺下等有限动作，扩展需要更多高质量训练数据。
- **场景假设简化**：系统仅处理同一楼层内的运动，且假设场景物体不可移动，不涉及跨楼层交互或动态物体。
- **空间约束**：在狭窄空间中，物理约束会限制动态交互的生成；碰撞修正模块在窄通道中可能失效（Figure 20）。
- **运动多样性未显著提升**：场景感知模块提升了物理一致性，但未能显著丰富交互运动的多样性。
- **模块间过渡**：三个生成模块采用不同的训练策略和数据集，导致不同运动类型之间仍存在可察觉的过渡不自然。
- **相机依赖手动**：缺乏自动化的镜头跟随系统，渲染质量受限于人工设置。

### 5. 开放问题与后续工作方向

论文明确指出了以下待解决问题：

1. **自动相机跟随**：如何实现智能相机调度以提升情景剧渲染质量？
2. **交互类型扩展**：能否通过大规模数据采集或自动提取扩展人-场景交互的类型？
3. **训练统一化**：如何统一三个生成模块的训练设置以减少运动间的过渡不自然？
4. **多样性与物理约束的权衡**：引入人-人碰撞损失后，HHP从0.0989降至0.0742，但FID从3.871升至10.251（Table 6），揭示了物理约束与运动质量之间的内在张力。如何在保证物理一致性的同时增加交互运动的多样性和复杂性？
5. **碰撞修正的鲁棒性**：碰撞修正模块在更复杂场景（如多角色或狭窄空间）中的成功率和局限性需要系统评估。
6. **手部姿态语义对齐**：手部姿态检索模块如何处理指令与Inter-X数据集中无语义相似标注的情况？
7. **分阶段训练的机制理解**：早期引入物理约束具体如何限制运动学习能力，是否存在更优的训练调度策略？



## 原文 PDF

![[paperPDFs/ICLR_2025/Sitcom_Crafter_A_Plot_Driven_Human_Motion_Generation_System_in_3D_Scenes.pdf]]
