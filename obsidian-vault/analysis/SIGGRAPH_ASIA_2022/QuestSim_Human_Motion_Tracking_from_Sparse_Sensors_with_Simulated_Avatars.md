---
title: "QuestSim: Human Motion Tracking from Sparse Sensors with Simulated Avatars"
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/QuestSim_Human_Motion_Tracking_from_Sparse_Sensors_with_Simulated_Avatars.pdf
project_link: null
code_link: null
aliases:
- QuestSim
tags:
- SIGGRAPH_ASIA_2022
- topic/graphics_animation_interaction
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 引入现成的物理模拟器作为硬约束，结合强化学习在训练时利用全动捕数据密集监督，推理时仅需稀疏输入。
primary_logic: 物理模拟提供了不可违反的物理约束，使策略可以利用模拟角色的完整状态反馈来解析稀疏输入中的模糊性；同时未来观测增强预测能力，简单的MLP策略即可学习输出合适力矩以驱动平衡、行走和慢跑。
claims:
- 在Lafan数据集上，仅用头戴和双手柄的重建误差MPJRE为5.7°，MPJPE为3.7 cm，与使用6个IMU的PIP方法接近。
- 尽管没有下肢传感器，定性结果显示下肢运动与地面真实非常相似。
- Lafan dataset 上 MPJPE (cm) = 3.7
- Lafan dataset 上 MPJRE (deg) = 5.7
---

# QuestSim: Human Motion Tracking from Sparse Sensors with Simulated Avatars

> [!tip] 核心洞察
> 物理模拟提供了不可违反的物理约束，使策略可以利用模拟角色的完整状态反馈来解析稀疏输入中的模糊性；同时未来观测增强预测能力，简单的MLP策略即可学习输出合适力矩以驱动平衡、行走和慢跑。

| 字段 | 内容 |
|------|------|
| 中文题名 | QuestSim：利用模拟化身从稀疏传感器进行人体运动跟踪 |
| 英文题名 | QuestSim: Human Motion Tracking from Sparse Sensors with Simulated Avatars |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://arxiv.org/abs/2209.09391) |
| Topic | #topic/graphics_animation_interaction #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | QuestSim |
| Dataset | Lafan dataset, Comparison with PIP |

> [!tip] 效果简介
> - Lafan dataset 上，MPJPE (cm) 3.7 vs - (-)；MPJRE (deg) 5.7 vs - (-)；RootE (cm) 1.8 vs - (-)。
> - Comparison with PIP 上，SIP (deg) 12.3 vs 12.9 (PIP on TotalCapture) (-0.6)；Jitter (km/s^3) 0.3 vs 0.2 (PIP on TotalCapture) (+0.1)。

## 概要

**问题**：消费级VR头显和手柄仅提供稀疏的头部与双手六自由度追踪，完全缺失下肢信号。纯运动学方法直接回归全身姿态，易产生滑步、抖动等物理上不合理的伪影，且无法保证生成姿态的物理有效性。

**方法**：QuestSim 将现成的物理模拟器（NVIDIA PhysX）作为硬约束嵌入追踪管线，采用强化学习训练一个三层MLP策略。训练时，策略利用全动捕数据作为密集监督，学习输出关节力矩以驱动物理角色；推理时，策略仅接收稀疏的HMD与控制器观测、模拟角色完整状态反馈、未来6帧传感器信息及用户身高，即可在物理模拟器中生成平衡、行走、慢跑等自然运动。

**主要结果**：在 Lafan 数据集上，仅使用头显与双手柄（H+2C）即可达到 MPJRE 5.7°、MPJPE 3.7 cm 的重建精度，与需在腿部佩戴6个IMU的 PIP 方法（SIP 12.9°）性能相当，同时保持极低的抖动（Jitter 0.3 km/s³）。

**定位**：QuestSim 将姿态生成方式从运动学直接回归改为物理模拟驱动的力矩控制，在稀疏传感器人体运动追踪领域首次将物理模拟作为硬约束而非后处理，为 VR 化身驱动提供了物理合理且低延迟的解决方案。

## 核心方法与创新机理

### 问题瓶颈：稀疏传感下的物理合理性缺失

消费级VR设备（如Meta Quest）仅提供头显（HMD）和双手柄的6自由度姿态，完全缺失下肢运动信息。传统运动学方法（如RNN、Transformer直接回归关节角）面临根本性模糊：相同的上肢传感器信号可对应多种下肢姿态。更重要的是，纯运动学重构缺乏物理约束，常产生滑步、抖动、穿透地面等不自然伪影，且无法保证生成的姿态在物理世界中可执行。

### 核心洞察：物理模拟作为硬约束与完整状态反馈

QuestSim的核心创新在于将**现成的物理模拟器**嵌入姿态生成管线的末端，使其成为不可违反的硬约束，而非事后平滑的软约束。这一设计带来了两个关键优势：

1. **物理合理性自动保证**：模拟器根据力矩驱动角色，自动处理接触力、动量守恒等物理定律，生成的姿态天然满足物理可行性。
2. **完整状态反馈消除模糊性**：策略网络不仅接收稀疏传感器信号，还能访问模拟角色的完整本体感受状态（所有关节角、角速度、位置、速度、接触力等）。这些丰富的反馈信号使策略能够学习从稀疏输入中推断出物理上合理的下肢运动——即使没有下肢传感器。

### 关键方法槽位变更

相较于现有运动学方法，QuestSim在四个核心槽位上进行了根本性替换：

| 方法槽位 | 基线方案 | QuestSim方案 | 因果作用 |
|---------|---------|-------------|---------|
| **姿态生成方式** | 运动学直接回归关节角 | 强化学习策略输出力矩，驱动物理模拟器生成姿态 | 将姿态生成从“预测几何”转变为“控制物理过程” |
| **物理约束** | 无物理模拟，或仅后处理软约束 | NVIDIA PhysX作为硬约束（36fps） | 消除不可行姿态，保证接触力、动量等物理一致性 |
| **观测输入** | 仅传感器信号 | 传感器信号 + 模拟角色完整状态 + 未来6帧观测 + 用户身高 | 利用本体感受反馈解析稀疏输入的模糊性；未来观测增强预测能力 |
| **训练监督** | 运动学损失（MPJPE等） | 模仿奖励（高斯核：关节角/速度/位置/速度） + 足部接触力奖励，PPO优化 | 密集的全动捕监督引导策略学习从稀疏输入到合理力矩的映射 |

### 管线模块与推理/训练路径

QuestSim的架构（图2）包含三个核心模块，训练与推理路径共享策略网络和物理模拟器，仅在监督信号来源上不同。

#### 模块1：传感器观测提取

将HMD和控制器原始数据转换为相对于**角色朝向帧S**的位置和方向。帧S定义为角色根部的水平朝向帧，使观测对角色全局朝向不变。用户观测向量为：
$$o_{\mathrm{user}, t} = [h_S, {}_S R_h, l_S, {}_S R_l, r_S, {}_S R_r]$$
其中 $h_S, l_S, r_S$ 分别为头显、左控制器、右控制器在帧S中的三维位置，${}_S R_h, {}_S R_l, {}_S R_r$ 为对应的旋转矩阵。此外，策略还接收用户身高标量 $o_{\mathrm{user, scale}} \in \mathbb{R}$（米），以及未来6帧（约160ms）的传感器观测，以补偿实时系统中的感知延迟并增强对运动趋势的预测。

#### 模块2：策略网络（MLP）

策略网络是一个简单的3层MLP（隐藏层尺寸[400, 300, 200]，tanh激活），输入为拼接后的观测向量（用户传感器观测 + 模拟角色完整状态 + 身高 + 未来帧），直接输出每个关节的**力矩值**（而非PD控制器的目标角度）。这种直接力矩输出使策略能够学习更精细的动力学控制，避免PD控制器可能引入的僵硬行为。

#### 模块3：物理模拟器

使用NVIDIA PhysX（通过IsaacGym RL训练框架封装），以36fps频率运行。模拟器接收策略输出的力矩，驱动角色刚体动力学前向模拟一步，生成下一帧姿态，并反馈接触力、关节状态等信息给策略网络，形成闭环控制。

#### 训练路径

训练时，策略通过PPO算法优化期望折扣回报：
$$J(\pi_\theta) = \mathbb{E}_{\tau \sim \pi_\theta} \left[ \sum_0^T \gamma^t r_t \right]$$

奖励函数 $r_t$ 为加权模仿奖励，使用高斯核度量模拟值与全动捕真值之间的距离：
$$r_t = \mathbf{w} [r(q), r(\dot{q}), r(x), r(\dot{x}), r_f]^T$$

其中各项为：
$$r(s) = \exp(-k_s \sum_j \| s_{\mathrm{sim}} - s_{\mathrm{gt}} \|_2^2)$$

分别对**关节角** $q$、**关节角速度** $\dot{q}$、**笛卡尔位置** $x$、**笛卡尔速度** $\dot{x}$ 进行监督。权重设置为 $\mathbf{w} = [0.4, 0.1, 0.2, 0.1, 0.2]$，对应核大小为 $\mathbf{k} = [40.0, 0.3, 6.0, 2.0, 0.01]$。

关键的**足部接触力奖励** $r_f$ 专门设计用于解决无下肢传感器时的步态不自然问题：
$$r_f = \exp(k_f \sum_{i=L,R} \max(0, f_{y,i,\mathrm{prev}} - f_{y,i}))$$

该奖励惩罚垂直接触力的突然下降，鼓励角色在抬脚前先自然卸力，从而避免短促高频的“抽搐式”步态。消融实验证实，移除 $r_f$ 会导致角色产生不自然的短促高频步伐。

#### 推理路径

推理时，仅需用户传感器数据和模拟器反馈，无需真值动捕数据。策略网络以36fps频率输出力矩，物理模拟器生成物理上合理的姿态。用户身高通过初始HMD高度自动确定，驱动角色骨架的线性缩放。

### 因果链路总结

**稀疏传感器模糊性 → 物理模拟器提供硬约束 + 完整状态反馈 → 策略学习从模糊输入推断合理下肢运动 → 力矩驱动物理模拟 → 生成物理可行姿态**。足部接触力奖励进一步引导策略学习自然步态模式，未来观测补偿实时延迟。整个框架将姿态跟踪从“几何回归问题”重构为“物理控制问题”，使得仅需HMD和双手柄即可实现与6个IMU方法接近的重建精度。

![[assets/figures/papers/paper_list_l79_https_arxiv_org_abs_2209_09391/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our Imitation Learning architecture to track users from sparse sensor data. The dotted paths are only needed to train the policy network (MLP). During inference, this network produces torques for a physics simulator that generates the pose*

![[assets/figures/papers/paper_list_l79_https_arxiv_org_abs_2209_09391/figures/005_Figure_4.jpg]]
*Figure 4: Sparse input used to generate the full-body pose: the position of the headset (saturated) and left and right controller (less saturated). Y is the vertical dimension. Orientation information is also used by the model but not visualized here*

## 实验与关键发现

### 主实验结果

QuestSim 在 Lafan 数据集上的核心重建精度如表 1 所示。在仅使用头戴显示器（HMD）和双手柄（H+2C）的稀疏传感器配置下，方法取得了平均关节位置误差 **MPJPE 3.7 cm**、平均关节旋转误差 **MPJRE 5.7°**、以及全局根节点位置误差 **RootE 1.8 cm** 的结果。这一精度水平与 **PIP**（Yi et al., 2022）——一个在用户腿上佩戴 6 个 IMU 的运动学方法——在 TotalCapture 数据集上的表现接近（PIP 的 SIP 为 12.9°，QuestSim 在 Lafan 上的 SIP 为 12.3°），而 QuestSim 完全不需要任何下肢传感器。这一对比直接验证了核心主张：物理模拟作为硬约束，配合强化学习策略利用模拟角色的完整状态反馈，能够从极度稀疏的上肢传感器信号中解析出合理的下肢运动。

在运动平滑性方面，QuestSim 的加速度急动度（Jitter）为 **0.3 km/s³**，与 PIP 的 0.2 km/s³ 接近，表明物理模拟驱动的运动在时间连续性上并未因力矩控制而引入额外抖动。

仅使用头戴传感器（H only）的配置同样能够重建全身运动，但精度有所下降（MPJRE 约 6.5°，MPJPE 约 4.2 cm），说明双手柄提供的上肢空间信息对下肢运动推理具有辅助约束作用——即使手柄本身并不直接测量腿部运动。

### 关键消融实验

**足部接触力奖励的因果作用**。消融实验表明，若从奖励函数中移除足部接触力项 $r_f$，模拟角色在缺乏下肢传感器观测时会产生短促、高频的不自然步态。该奖励项惩罚垂直接触力的突然下降：
$$r_f = \exp( k_f \sum_{i=L,R} \max(0, f_{y,i,prev} - f_{y,i}) )$$
其机制在于鼓励角色在足部离地时逐渐释放接触力，而非突然切断，从而产生更自然的步态转换。这一消融揭示了物理模拟本身虽能保证动力学可行性，但并不自动保证运动风格的自然性——模仿奖励中的接触力项充当了风格正则化器，将物理可行解空间进一步约束到类人运动流形上。

**未来观测窗口的必要性**。方法依赖未来 6 帧（约 160 ms）的传感器观测作为策略输入。移除未来观测会显著降低预测精度，尤其是在快速转向或起步/停止等瞬态阶段。这是因为策略需要提前感知用户的运动意图以生成适当的力矩序列——物理模拟引入的惯性使得角色无法瞬时响应，必须提前规划。这一设计选择也构成了方法的实时性边界：系统存在固有的 160 ms 延迟。

### 定性评估与泛化能力

**跨体型泛化**。通过将用户身高 $o_{\text{user,scale}} \in \mathbb{R}$ 作为策略输入，并结合线性缩放角色肢体段参数，单一策略可以驱动不同身高的化身（验证范围 167 cm 至 181 cm）。定性结果（Fig. 5）显示同一用户可控制两种不同尺寸的化身，说明身高标量提供了有效的泛化线索。但需注意，线性缩放假设身体比例一致，对于肢体比例显著偏离训练分布的用户，这一简化可能引入误差——这是方法的一个已知边界条件。

**运动类型覆盖**。在未参与训练的测试序列上，定性评估（Fig. 3）展示了白板书写、行走、慢跑、后退行走并转弯等多种动作的重建效果。大部分重建姿态与视频参考吻合，尽管完全没有下肢传感器信号。这说明策略在训练时通过密集的全动捕监督学到了从稀疏上肢信号到全身运动的映射，且该映射在分布内的运动类型上具有良好的泛化性。

**环境交互与适应**。物理模拟框架允许化身与虚拟环境交互（Fig. 6）：化身姿态可受环境物体影响，且当用户的实际游戏空间与虚拟世界地形不一致时（如粗糙地面），模拟器会自动调整步态以适应虚拟地形。这一能力是纯运动学方法难以实现的，体现了物理模拟作为硬约束的独特优势。

### 失败模式与适用边界

**分布外高动态运动**。方法对训练分布外的高动态运动（如霹雳舞、跳跃）表现脆弱。当用户执行此类动作时，策略可能因未学到合适的力矩模式而导致模拟角色摔倒或严重偏离目标姿态。这是模仿学习方法的固有局限——策略仅在训练数据的支持范围内有效，缺乏对未知动作的探索或恢复机制。

**位置漂移与不可恢复性**。由于物理模拟不允许“瞬移”（即角色位置必须通过力矩驱动的运动连续更新），一旦化身位置与用户实际位置之间出现漂移（例如因累积跟踪误差或用户超出游戏空间），系统缺乏有效的重新对齐机制。这与运动学方法可以通过离散位置校正来恢复跟踪形成对比，是物理约束带来的双刃剑效应。

**上下肢运动解耦的模糊性**。当用户的上肢运动与下肢运动不相关时——即相同的 HMD 和手柄信号可以对应多种不同的下肢姿态——方法可能合成出与用户实际下肢运动不一致的姿态。这是稀疏传感器人体运动重建的根本性模糊问题，物理模拟虽然缩小了可行解空间，但无法完全消除这种一对多的映射歧义。

**实时延迟**。依赖未来 6 帧观测导致约 160 ms 的端到端延迟，这对于需要即时反馈的 VR 应用是一个实用限制。论文将此列为开放问题，探讨是否可通过预测未来姿态而非观测未来姿态来降低延迟。

**体型泛化的局限**。身高标量 + 线性缩放的方案可能无法准确表示身体比例差异显著的个体（如四肢与躯干比例异常）。提供更详细的骨架参数（如各肢体段长度）作为策略输入是可能的改进方向，但当前方法尚未验证这一扩展。

### 公平性与数据覆盖说明

训练数据来自 172 名受试者的约 8 小时动捕数据，包含多种动作类型。但论文未提供受试者的人口统计分布（如年龄、性别、体型范围），也未分析不同子群上的性能差异。因此，方法在不同体型、性别或运动风格用户上的公平性尚需独立验证。

![[assets/figures/papers/paper_list_l79_https_arxiv_org_abs_2209_09391/figures/003_Table_1.jpg]]
*Table 1: Pose reconstruction from synthesized and real Meta Quest HMD (H) and controllers (C). We show that despite not having sensors on the lower body, our metrics match state-of-the-art methods like PIP [Yi et al. 2022] that use IMUs attached to the legs. Limitations are discussed in Sec. 5.4*

![[assets/figures/papers/paper_list_l79_https_arxiv_org_abs_2209_09391/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative evaluation of pose reconstruction on motion sequences not used during training, corrected for latency. Most of the reconstructed poses match the video reference footage, despite having no lower-body sensor signal available for reconstruction. The four sequences demonstrate writing on a whiteboard, walking, jogging, and backwards walking with turns. Readers are encouraged to view the video for more examples*

![[assets/figures/papers/paper_list_l79_https_arxiv_org_abs_2209_09391/figures/006_Figure_6.jpg]]
*Figure 6: Top: The avatar pose is influenced by the environment and it can interact with virtual objects. Bottom: If a user controls an avatar in an environment different than their play space, the motion is adapted to match the virtual world (e.g. rough ground)*

![[assets/figures/papers/paper_list_l79_https_arxiv_org_abs_2209_09391/figures/007_Figure_5.jpg]]
*Figure 5: In this example a single user controls avatars of two different sizes using the same policy*

## 定位与知识库关联

**改变的核心 slot：从运动学直接回归到物理模拟驱动的强化学习策略**

QuestSim 相对于现有稀疏传感器人体运动跟踪方法，改变的关键 slot 在于**姿态生成方式**：传统方法（如基于 VAE 的 **Dittadi et al., 2021**、基于 Transformer 的 **Jiang et al., 2022a**、以及 **PIP** (Yi et al., 2022)）采用运动学直接回归——即从传感器信号通过 RNN/Transformer 直接输出关节角度，物理合理性最多作为后处理软约束加入。QuestSim 则将姿态生成完全交给一个物理模拟器（NVIDIA PhysX），策略网络（MLP）输出的是**关节力矩**而非姿态，物理模拟器作为不可违反的硬约束计算下一帧姿态。这一改变是根本性的：运动学方法需要在损失函数中平衡跟踪精度与物理合理性，而 QuestSim 通过模拟器天然保证所有生成姿态满足牛顿力学。

**知识库挂载点：物理模拟 + 模仿学习的运动生成范式**

QuestSim 的知识库挂载点位于**物理模拟驱动的人物动画**与**基于强化学习的运动模仿**两条线的交汇处。在物理模拟人物控制方面，它继承了使用强化学习训练模拟角色完成行走、跑步等运动技能的工作（如 DeepMimic, Peng et al., 2018），但将应用场景从“给定目标轨迹生成运动”转为“从稀疏用户输入实时跟踪运动”。在运动模仿方面，它借鉴了使用全动捕数据作为密集监督训练策略的范式，但创新地将模仿学习框架适配到**仅训练时可获得全动捕、推理时仅有稀疏传感器**的跨模态设置。这一挂载点的核心洞察是：物理模拟器提供的完整角色状态（关节角、速度、接触力等）可以作为“虚拟传感器”，使策略能够利用这些丰富信息来解析稀疏用户输入中的下肢运动模糊性——而纯运动学方法缺乏这种闭环的物理反馈通道。

**与最相关基线 PIP 的本质差异**

PIP (Yi et al., 2022) 是使用 6 个 IMU（包括腿部传感器）的运动学方法，代表了稀疏传感器跟踪的 state-of-the-art。QuestSim 与 PIP 的本质差异体现在三个层面：

1. **传感器需求**：PIP 需要 6 个 IMU 分布在全身（含腿部），QuestSim 仅需 HMD + 2 个手柄（无任何下肢传感器），却在 Lafan 数据集上达到可比的 SIP 指标（QuestSim: 12.3°, PIP: 12.9°）。这表明物理先验可以有效补偿传感器稀疏性。

2. **物理合理性保证**：PIP 通过后处理优化减少滑步，但无法根除物理不自然伪影。QuestSim 的模拟器硬约束使生成的姿态天然满足物理定律，Jitter 指标仅 0.3 km/s³（PIP 为 0.2），说明平滑性相当，但 QuestSim 的姿态同时满足接触力约束和动量守恒。

3. **泛化能力来源**：PIP 依赖大规模动捕数据学习运动先验，QuestSim 则通过物理模拟器隐式编码了运动先验——策略只需学习“如何输出力矩使角色模仿参考运动”，物理可行性由模拟器保证。这使得 QuestSim 能处理训练数据中未见的环境交互（如不平坦地面、虚拟物体交互，见 Fig. 6），而运动学方法通常无法适应环境变化。

**适用边界与关键限制**

QuestSim 的物理模拟驱动范式虽然提供了强物理约束，但也引入了明确的适用边界：

- **运动多样性受限**：策略只能模仿训练集中出现的运动模式。对于分布外的高动态运动（如霹雳舞、跳跃、快速转身），策略可能因未学到合适的力矩模式而导致角色摔倒或跟踪失败。这是模仿学习范式的固有局限，与运动学方法的数据驱动泛化能力形成对比。

- **物理自主性与跟踪精度的权衡**：由于不允许“瞬移”（运动学方法可以任意修正位置），一旦模拟角色与用户实际位置产生漂移，难以快速恢复。这体现了物理约束的代价——在某些需要精确空间对齐的应用中，运动学方法可能更优。

- **实时延迟**：依赖未来 6 帧传感器观测（约 160 ms）来增强预测能力，这虽然提高了下肢运动推断的准确性，但引入了可感知的延迟，限制了在高速交互场景（如节奏游戏、竞技 VR）中的应用。

- **用户体型泛化**：通过身高标量线性缩放所有肢体段参数，无法准确表示身体比例差异大的用户（如长腿短躯干 vs. 短腿长躯干），可能导致跟踪偏差。

**后续研究启发**

QuestSim 的开创性工作为以下方向提供了明确的研究路径：

1. **物理自主性与用户控制的动态平衡**：文中提出的核心开放问题“物理自主性应该多强，何时可以违反物理以精确跟踪用户？”直接指向一个更通用的研究问题——如何在物理模拟框架中引入可调节的约束强度，使系统在“完全物理合理”和“完全运动学跟踪”之间平滑过渡。这可能需要将物理模拟器从硬约束改为软约束，或引入基于置信度的混合策略。

2. **运动多样性的扩展**：通过专家混合（Mixture of Experts）或预训练控制器库，使单一策略能够覆盖更广泛的运动类型（如舞蹈、体育动作、跌倒恢复），这是将物理模拟跟踪推向通用 VR 应用的关键步骤。

3. **降低延迟的预测架构**：当前依赖未来观测的设计可以通过学习一个显式的运动预测模块来替代——策略基于历史观测预测未来姿态，从而在推理时不再需要等待未来传感器数据，将延迟降至模拟器计算时间（约 28 ms）。

4. **个性化身体模型**：将身高标量扩展为更丰富的身体比例参数（如肢体长度比、关节活动范围），甚至从初始校准动作中在线推断用户身体参数，可显著提升不同体型用户的跟踪精度。

5. **影视级动画质量**：文中提到“达到 VFX 级动画质量”的目标，这需要在奖励函数中引入更精细的运动质量指标（如足部滑动惩罚、质心平滑度、风格一致性），并可能需要与运动风格迁移技术结合。

**知识库中的定位总结**

QuestSim 在知识库中占据了一个独特的交叉位置：它既不是纯运动学跟踪方法的增量改进，也不是传统物理模拟角色控制的简单应用，而是**首次将物理模拟作为硬约束引入稀疏传感器人体运动跟踪任务**，并证明了仅用 HMD 和手柄即可达到接近 6-IMU 方法的跟踪精度。其核心贡献在于揭示了物理模拟器提供的完整状态反馈可以作为“免费”的丰富观测，使简单的 MLP 策略能够解析稀疏输入中的下肢运动模糊性——这一洞察对后续的 VR/AR 人体跟踪、远程呈现、以及物理合理的人机交互研究具有重要的范式启发意义。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/QuestSim_Human_Motion_Tracking_from_Sparse_Sensors_with_Simulated_Avatars.pdf]]