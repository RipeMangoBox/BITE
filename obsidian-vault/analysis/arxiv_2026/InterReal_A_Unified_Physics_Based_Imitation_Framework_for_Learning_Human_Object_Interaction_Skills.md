---
title: InterReal A Unified Physics Based Imitation Framework for Learning Human Object Interaction Skills
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/InterReal_A_Unified_Physics_Based_Imitation_Framework_for_Learning_Human_Object_Interaction_Skills.pdf
project_link: null
code_link: null
aliases:
- IUPBIFLHOIS
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过元学习策略自适应地调节大规模奖励项的权重系数，结合带手-物接触约束的运动增强，策略能够在交互过程中根据不同任务阶段动态平衡全身控制目标。
primary_logic: 利用关键跟踪误差驱动的元策略动态分配奖励权重，避免手工调参的次优性；同时通过保持接触一致性的逆运动学增强运动，使策略对物体位置扰动具有鲁棒性。
claims:
- InterReal 在搬运箱子和推动箱子任务上取得最低的 DOF 关节角度和物体位置跟踪误差，并在两项任务上取得最高的成功率。
- 自动奖励学习机制（外部循环元策略）显著优于固定启发式奖励，消融实验验证了其有效性。
- HOI 运动增强方法通过注入物体位置偏移并利用逆运动学保持手-物接触，有效提升策略对扰动的泛化能力。
- Box-picking task (in simulation) 上 E_mulpe (mean upper limb position tracking error, lower is... = 0.0028
---

# InterReal A Unified Physics Based Imitation Framework for Learning Human Object Interaction Skills

> [!tip] 核心洞察
> 利用关键跟踪误差驱动的元策略动态分配奖励权重，避免手工调参的次优性；同时通过保持接触一致性的逆运动学增强运动，使策略对物体位置扰动具有鲁棒性。

| 字段 | 内容 |
|------|------|
| 中文题名 | InterReal：面向人-物交互技能的统一物理模仿学习框架 |
| 英文题名 | InterReal A Unified Physics Based Imitation Framework for Learning Human Object Interaction Skills |
| 会议/期刊 | arXiv 2026 |
| Links |  [paper](https://arxiv.org/abs/2603.07516)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | InterReal |
| Dataset | Box-picking task, Box-pushing task, Box-picking task success rate, Box-pushing task success rate |

> [!tip] 效果简介
> - Box-picking task (in simulation) 上，E_mulpe (mean upper limb position tracking error, lower is better) 0.0028 vs InterMimic* / ASAP* (values not explicitly given; higher than InterReal) (outperforms baselines (lowest error))。
> - Box-pushing task (in simulation) 上，E_m3lpe (mean 3-link position error, lower is better) 0.0019 vs InterMimic* / ASAP* (outperforms baselines (lowest error))。
> - Box-picking task success rate 上，Task success rate (%) 96.41% vs InterMimic* / ASAP* (highest among compared methods)。

## 概要

人-物交互（HOI）是具身智能的核心能力，但现有全身控制与遥操作框架普遍缺乏对物体动态及手-物接触的显式闭环感知与反馈，导致在真实世界中难以稳定执行精确的交互任务。这一瓶颈的根本原因在于：大规模多目标奖励函数的手工调参不仅极为耗时，且难以在不同任务阶段实现动态平衡，从而限制了策略的泛化性与鲁棒性。

针对上述问题，本文提出 **InterReal**——一个统一的物理基模仿学习框架。其核心思路是：通过元学习策略自适应调节大规模奖励项的权重系数，并结合带手-物接触约束的运动增强，使策略能够在交互过程中根据不同任务阶段动态平衡全身控制目标。具体而言，InterReal 利用关键跟踪误差驱动的元策略（外循环 SAC）动态分配奖励权重，避免手工调参的次优性；同时，通过保持接触一致性的逆运动学增强运动，使策略对物体位置扰动具有鲁棒性。

实验表明，InterReal 在搬运箱子与推动箱子两项任务上均取得最低的 DOF 关节角度和物体位置跟踪误差，并在两项任务上取得最高的成功率（搬运 96.41%，推动 87.45%）。消融实验进一步验证了自动奖励学习机制显著优于固定启发式奖励，而基于逆运动学的 HOI 运动增强方法有效提升了策略对物体扰动的泛化能力。真实世界部署（Fig. 1）证实了框架在 Unitree G1 机器人上的可行性。

### 1. 研究背景与问题语境

人形机器人执行人-物交互（Human–Object Interaction, HOI）任务，如搬运箱子、推动重物，是通用机器人走向真实世界应用的关键能力之一。这类任务要求机器人同时协调全身运动（行走、弯腰、手臂操作）与对外部物体的精确操控，形成一个高维、强耦合的闭环控制系统。

近年来，基于物理仿真（physics-based simulation）的强化学习方法在全身运动模仿（whole-body motion imitation）上取得了显著进展，使人形机器人能够学习复杂的运动技能。然而，当任务从单纯的“模仿人体运动”扩展到“在交互中操控物体”时，现有框架暴露出一个核心瓶颈：**缺乏对物体动态与手-物接触的显式闭环感知与反馈**。具体而言，现有全身控制与遥操作框架通常将物体视为被动背景，未能将物体的实时状态（位置、姿态、接触力）纳入策略观测与奖励设计的核心回路，导致在真实世界中难以稳定执行精确的交互任务——尤其是当物体因外部扰动或自身运动而发生非预期偏移时，策略容易失效。

### 2. 现有方法的缺口

当前面向 HOI 的物理模仿学习面临两个相互关联的挑战。

**第一，运动数据的鲁棒性不足。** 传统方法通常仅使用单条参考运动或简单的域随机化来训练策略。然而，真实交互中物体位置不可避免地受到扰动（如抓取时的滑移、推动时的地面摩擦变化），单条运动无法覆盖这些分布外（out-of-distribution）场景，导致策略对物体位置偏移高度敏感，泛化能力薄弱。

**第二，奖励函数设计的手工依赖性。** HOI 任务涉及多个优化目标——全身关节跟踪、物体位置跟踪、手-物接触维持、能量效率等——需要精心平衡大规模奖励项的权重。现有方法依赖经验性、固定的启发式权重分配，这不仅是耗时的调参工程，更关键的是，固定权重无法适应不同任务阶段（如抓取初期 vs. 搬运中期）对各类目标的差异化需求，导致次优的策略收敛。

### 3. 本文动机与核心思路

针对上述缺口，**InterReal** 提出了一套统一的物理模仿学习框架，其核心动机在于：**通过数据增强与自适应奖励学习，使 HOI 策略获得对物体扰动的鲁棒性和对多目标权衡的动态调节能力。**

框架围绕两个因果性调节手段展开：

- **HOI 运动增强（Motion Augmentation）**：对物体位置施加平面内偏移，并通过逆运动学（IK）重新求解手臂关节角度，同时保持手-物接触细节，从而从单条锚定运动生成多条增强运动。这一设计使策略在训练阶段即暴露于多样化的物体位置扰动，显著提升泛化能力。

- **自动奖励学习器（Automatic Reward Learner）**：引入一个基于 SAC 的元策略（meta-policy），以关键跟踪误差为驱动信号，动态输出各子奖励的权重系数。该元策略随 PPO 训练进度自适应调节平衡、跟踪、接触等目标之间的权重分配，替代手工调参，使策略能够在不同任务阶段自动聚焦于当前最关键的优化目标。

通过将上述两个机制嵌入内循环 PPO 策略学习与外循环元学习优化，InterReal 构建了一个端到端的 HOI 技能学习范式，最终支持在真实 Unitree G1 机器人上利用 FoundationPose 进行 6D 物体姿态估计，实现 sim-to-real 部署。

## 核心方法与创新机理

InterReal 的核心创新围绕一个闭环因果链条展开：**瓶颈 → 操纵变量 → 核心洞察**。现有全身控制与遥操作框架（如 **InterMimic*** (Xu et al., CVPR 2025) 和 **ASAP*** (He et al., 2025)）缺乏对物体动态与手-物接触的显式闭环感知与反馈，导致在真实世界中难以稳定执行精确的交互任务。InterReal 通过三个相互耦合的 **changed slots** 系统性地解决了这一问题，其因果操纵变量是利用关键跟踪误差驱动的元策略，动态调节大规模奖励项的权重系数。

### 1. HOI 运动增强：从单运动到接触一致性多运动训练

**Baseline** 方法通常仅使用单条参考运动或简单的域随机化，策略对物体位置扰动极为敏感。InterReal 提出了保持手-物接触约束的 **HOI 运动增强** 方案（Section IV.B, Fig. 2(b)）：

- 对物体位置沿 XY 平面施加偏移 $\Delta p_{xy}^j$，生成增强后的世界坐标系位置 $\hat{p}^{(\mathrm{w})}(t) = p^{(\mathrm{w})}(t) + \Delta p_{xy}^j$，同时将末端执行器位置同步偏移 $\hat{p}_{L/R}^{(\mathrm{w})}(t) = p_{L/R}^{(\mathrm{w})}(t) + \Delta p_{xy}^j$（Eq. 2）。
- 通过躯干-骨盆变换矩阵 $T_{(\mathrm{pt})} T_{(\mathrm{tw})}$，将增强后的手腕位置从世界坐标系转换到骨盆坐标系 $\hat{\mathbf{p}}_{L/R}^{(\mathrm{p})}(t)$（Eq. 3），再利用逆运动学（IK）重新求解手臂关节角度，**在保持手-物接触细节的前提下**，从单条锚定运动生成多条增强运动轨迹。

这一设计使策略在训练阶段即暴露于多样化的物体位置扰动，从而在部署时对真实世界的物体检测噪声和延迟具有天然鲁棒性。消融证据表明，该增强方法有效提升了策略对扰动的泛化能力（confidence: 0.9）。

### 2. 自动奖励学习器：元策略驱动的动态权重分配

**Baseline** 方法依赖固定、经验性设定的多目标奖励权重，在全身控制与交互精度之间存在手工调参的次优性。InterReal 引入了双层学习架构：

- **内循环**：PPO 优化 HOI 控制策略 $\pi_\phi$，其目标函数 $\mathcal{L}^{\mathrm{hoi}}$ 集成了自适应加权奖励 $\sum_{t}^{T} \sum_{k=1}^{K} \theta_t^k r^k(t)$，包括交互图跟踪奖励 $r_t^{\mathrm{ig}} = \exp(-\theta_t^{\mathrm{ig}} \cdot \| s_t^{\mathrm{ig}} - s_{\mathrm{ref},t}^{\mathrm{ig}} \|^2)$（Eq. 4, Section IV.C）。
- **外循环**：基于 SAC 的元策略 $\mu_\psi^{\mathrm{meta}}$ 根据 PPO 学习进度，动态输出奖励权重 $\Theta' = \Theta^0 * \sigma(t) \mu_\psi^{\mathrm{meta}}(\Theta_t | u_t)$，其中 $\sigma(t) = \mathrm{clip}(1 - \frac{c_4}{t}, \delta, 1)$ 为时间依赖的缩放因子（Section IV.D）。

**决定性证据**：在箱体抓取与推动任务上，自动奖励学习机制显著优于固定启发式奖励（消融实验验证，confidence: 0.9）。元学习内部系数 $\delta$ 的最佳设置为 0.1，此时 HOI 策略达到最佳跟踪性能（Fig. 4, confidence: 0.95）。Fig. 5 展示了奖励权重系数随训练时间动态调节的自适应曲线，直观反映了元策略如何在不同任务阶段平衡全身控制、跟踪精度与接触目标。

### 3. 非对称 Actor-Critic 与交互图感知

作为训练范式的关键组成部分，InterReal 采用非对称 Actor-Critic 结构：Critic 访问完美状态（包括交互图特征 $s_t^{\mathrm{ig}}$、物体速度与旋转），Actor 仅接收不完美状态（排除交互图与物体速度/旋转）。这一设计使 Critic 能够利用全局信息进行精确的价值估计，同时保证 Actor 在部署时仅依赖可获取的传感器观测，无需交互图真值。

三个 changed slots 形成了完整的创新闭环：运动增强提供物体扰动下的多样化训练数据，自动奖励学习器动态协调多目标优化，非对称结构桥接仿真训练与真实部署的信息不对称。这一组合使 InterReal 在箱体抓取任务上达到 96.41% 的成功率，在箱体推动任务上达到 87.45% 的成功率，均显著优于基线方法（Table II, confidence: 0.95）。

InterReal 的整体框架由三个核心组件构成：**运动数据预处理**、**多运动-多环境学习**以及**真实世界部署**（Fig. 2）。框架以人-物交互（HOI）的运动捕捉数据为输入，经过重定向、物理验证与运动增强后，送入一个双循环的强化学习器进行训练，最终借助 FoundationPose 实现在真实机器人上的零样本部署。

![[assets/figures/papers/paper_list_l22_InterReal_A_Unified_Physics_Based_Imitation_Framework_for_Learning_Human/figures/002_Figure_2.jpg]]
*Figure 2: Overall framework of InterReal. InterReal consists of three main components: motion data preprocessing, multi-motion multienvironment learning, and deployment. It enables retargeting HOI motions into trainable motions with G1 robot shapes, achieves accurate motion tracking in complex HOI training settings, and ultimately supports real-world deployment*

### 运动数据预处理流水线

预处理阶段负责将原始的 SMPL 格式 HOI 运动数据转化为可供 Unitree G1 机器人模型训练的标准化运动片段。

1. **HOI 运动重定向**：将人体运动捕捉数据重定向到 G1 机器人的关节构型，同时优化人-物-地面接触的自然性，确保重定向后的运动在运动学上合理（Fig. 2(a)）。
2. **物理验证**：利用 **InterMimic** 在 IsaacGym 物理仿真器中对重定向后的运动施加物理约束，剔除穿透、碰撞等无效参考帧，生成经过物理验证的 HOI 运动片段。
3. **HOI 运动增强**：对验证后的运动施加物体位置偏移，并通过逆运动学（IK）重新求解手臂关节角度以保持手-物接触一致性，从而从单条锚定运动生成多条增强运动轨迹。这一步骤是提升策略对物体位置扰动鲁棒性的关键机制。

### 多运动-多环境学习器

学习器采用**双循环元学习架构**，包含内环的 HOI 策略学习和外环的自动奖励学习（Fig. 2 中部）。

- **内环 HOI 策略学习**：基于 PPO 算法训练任务特定的 HOI 控制策略 $\pi^{\text{hoi}}$。策略接收非完美状态（不含交互图、物体速度和旋转），而 Critic 网络则访问完美状态（包含完整的本体感知、重力投影、交互图特征和物体特征），形成**非对称 Actor-Critic 结构**。奖励函数由多个子奖励项加权求和构成，其中包含专门设计的**交互图跟踪奖励** $r_t^{\text{ig}} = \exp(-\theta_t^{\text{ig}} \cdot e_t^{\text{ig}})$，用于鼓励准确的人-物接触。
- **外环自动奖励学习**：基于 SAC 的元策略 $\mu_\psi^{\text{meta}}$ 根据 PPO 的学习进度，动态输出各子奖励的权重系数 $\Theta'$。元策略以关键跟踪误差指标为输入，通过最大化 HOI 策略在测试任务上的表现来优化权重分配，从而替代手工调参。权重更新规则为 $\Theta' = \Theta^0 * \sigma(t) \mu_\psi^{\text{meta}}(\Theta_t | u_t)$，其中 $\sigma(t)$ 是随时间衰减的缩放因子。

### Sim-to-Real 部署

在真实世界部署阶段（Fig. 2 右侧），系统利用 **FoundationPose** 进行 6D 物体姿态估计，将物体状态观测输入训练好的 HOI 策略。策略在 Unitree G1 机器人上实时推理，输出关节目标位置，完成箱体抓取与推动等交互任务。该流程实现了从仿真到真实的无缝迁移，无需在真实环境中进行额外微调。

InterReal 将人-物交互（HOI）技能学习形式化为一个马尔可夫决策过程（MDP），并由五个核心模块构成闭环：HOI 运动重定向与物理验证、HOI 运动增强、内环 PPO 策略学习、外环自动奖励学习，以及 Sim-to-Real 部署。以下聚焦于决定系统能力的关键模块与公式。

### 1. HOI 任务的 MDP 形式化

整个交互任务被建模为如下 MDP 元组（Section III.A）：

$$( \mathcal{S}, \mathcal{A}, \mathcal{P}, f_t, \gamma )$$

其中 $\mathcal{S}$ 为状态空间，$\mathcal{A}$ 为动作空间，$\mathcal{P}$ 为状态转移函数，$f_t$ 为奖励函数，$\gamma$ 为折扣因子。时刻 $t$ 的状态由人体、物体、交互三方面特征及任务阶段联合构成：

$$s_t = [s_t^h, s_t^o, s_t^{\mathrm{int}}, p]$$

- **人体本征特征** $s_t^h = [\mathbf{q}_t, \dot{\mathbf{q}}_t, \omega_t^{\mathrm{root}}, \mathbf{g}_t, \mathbf{a}_{t-1}]$：包含关节位置、速度、根角速度、重力投影及上一时刻动作。
- **物体特征** $s_t^o = [\mathbf{q}_t^o, \dot{\mathbf{q}}_t^o, \vartheta_t^o]$：包含物体全局位置、速度与朝向。
- **交互特征** $s_t^{\mathrm{int}} = [\mathbf{h}_t^o, \mathbf{s}_t^{\mathrm{ig}}]$：包含接触布尔状态与交互图特征。
- **任务阶段** $p$：用于指示当前所处任务子阶段。

这一状态设计的关键在于显式引入了交互图特征 $\mathbf{s}_t^{\mathrm{ig}}$，使得策略能够感知手-物接触的空间关系，而非仅依赖末端执行器的位置误差。

### 2. HOI 运动增强：接触约束下的逆运动学求解

运动增强模块是 InterReal 提升策略对物体位置扰动鲁棒性的核心设计。其基本流程为：对原始 HOI 参考运动中的物体位置施加 XY 平面内的随机偏移 $\Delta p_{xy}^j$，随后通过逆运动学（IK）重新求解手臂关节角度，同时严格保持手-物接触细节。

增强后的物体与末端执行器在世界坐标系下的位置为（Eq. 2, Section IV.B）：

$$\hat{p}^{(\mathrm{w})}(t) = p^{(\mathrm{w})}(t) + \Delta p_{xy}^j, \quad \hat{p}_{L/R}^{(\mathrm{w})}(t) = p_{L/R}^{(\mathrm{w})}(t) + \Delta p_{xy}^j$$

为在机器人自身参考系下求解 IK，需将增强后的手腕位置从世界坐标系转换至骨盆坐标系（Eq. 3, Section IV.B）：

$$\hat{\mathbf{p}}_{L/R}^{(\mathrm{p})}(t) = T_{\mathrm{pt}} \, T_{\mathrm{tw}} \, \hat{\mathbf{p}}_{L/R}^{(\mathrm{w})}(t)$$

其中 $T_{\mathrm{tw}}$ 为世界到躯干的变换矩阵，$T_{\mathrm{pt}}$ 为躯干到骨盆的变换矩阵。通过这一变换，IK 求解器可以在骨盆坐标系下计算满足接触约束的手臂关节配置，从而从单条锚定运动生成多条保持手-物接触的增强运动轨迹。

### 3. 内环 HOI 策略：自适应加权奖励与非对称 Actor-Critic

内环采用 PPO 优化 HOI 控制策略，其核心创新在于将交互图跟踪奖励纳入目标函数，并采用非对称 Actor-Critic 架构。

**交互图跟踪奖励**定义为参考交互图特征与当前交互图特征之间 L2 误差的指数衰减形式（Section IV.C）：

$$r_t^{\mathrm{ig}} = \exp\left(-\theta_t^{\mathrm{ig}} \cdot e_t^{\mathrm{ig}}\right), \quad e_t^{\mathrm{ig}} = \| s_t^{\mathrm{ig}} - s_{\mathrm{ref},t}^{\mathrm{ig}} \|^2$$

其中 $\theta_t^{\mathrm{ig}}$ 为外环元策略动态输出的权重系数。该奖励直接鼓励策略在交互过程中维持与参考运动一致的手-物接触模式。

**PPO 策略损失**整合了自适应加权的多目标奖励（Eq. 4, Section IV.C）：

$$\mathcal{L}^{\mathrm{hoi}}(\phi, v; \Theta, \mathcal{D}_t^{\mathrm{hoi}}) = \mathbb{E}_{a_t, s_t, s_t^{\mathrm{im}} \sim \mathcal{D}_t^{\mathrm{hoi}}} \left[ -\frac{\pi_\phi(a_t | s_t^{\mathrm{im}})}{\pi_{\phi'}(a_t | s_t^{\mathrm{im}})} \left( \sum_{t}^{T} \sum_{k=1}^{K} \theta_t^k r^k(t) - V_v(s_t) \right) \right]$$

其中 $\theta_t^k$ 为第 $k$ 个子奖励的权重（由外环元策略输出），$r^k(t)$ 为对应的子奖励项（包括关节跟踪、物体跟踪、接触奖励等），$V_v(s_t)$ 为价值函数。Actor 仅接收不完美状态 $s_t^{\mathrm{im}}$（排除交互图和物体速度/旋转信息），而 Critic 可访问完美状态，这一非对称设计使策略在部署时仅依赖可获取的传感器信息即可运行。

### 4. 外环自动奖励学习：元策略驱动的权重自适应

外环的核心是一个基于 SAC 的元策略 $\mu_\psi^{\mathrm{meta}}$，其目标是通过观察内环 PPO 的训练进度，动态调节各子奖励的权重系数 $\Theta_t$，从而替代手工调参。

**外环元学习目标**为最小化内环策略在测试任务上的期望损失（Section IV.D）：

$$\min_{\Theta, \psi} \mathbb{E}_{\mathcal{T} \sim p(\mathcal{T})} \left[ \mathcal{L}^{\mathrm{hoi}}(\phi, v, \Theta'; \mathcal{D}^{\mathrm{hoi}}, \mathcal{D}_{\mathcal{T}}^{\mathrm{test}}) \right] \quad \mathrm{s.t.} \; \Theta' = U_\psi(\Theta; \mathcal{D}_{\mathcal{T}}^{\mathrm{tr}})$$

其中 $U_\psi$ 为元策略参数化的更新规则，$\mathcal{D}_{\mathcal{T}}^{\mathrm{tr}}$ 和 $\mathcal{D}_{\mathcal{T}}^{\mathrm{test}}$ 分别为任务 $\mathcal{T}$ 的训练与测试数据。

**奖励权重的具体更新规则**为（Section IV.D）：

$$\Theta' = \Theta^0 * \sigma(t) \, \mu_\psi^{\mathrm{meta}}(\Theta_t | u_t), \quad \sigma(t) = \mathrm{clip}\left(1 - \frac{c_4}{t}, \delta, 1\right)$$

其中 $\Theta^0$ 为初始权重，$\sigma(t)$ 为时间依赖的缩放因子（随训练进度从 1 递减至下界 $\delta$），$\mu_\psi^{\mathrm{meta}}$ 为元策略基于观测 $u_t$（包含关键跟踪误差指标）输出的调节系数。三者按元素相乘得到最终权重，实现了从初始启发式权重到数据驱动自适应权重的平滑过渡。消融实验表明，内部系数 $\delta$ 的最优设置为 0.1（Fig. 4）。

![[assets/figures/papers/paper_list_l22_InterReal_A_Unified_Physics_Based_Imitation_Framework_for_Learning_Human/figures/007_Figure_5.jpg]]
*Figure 5: Adaptive curves for reward-related weight coefficients*

## 实验与关键发现

### 实验设置

InterReal 在两个代表性的人-物交互（HOI）任务上进行验证：**箱体抓取（Box-picking）** 与 **箱体推动（Box-pushing）**。所有实验均在 IsaacGym 物理仿真器中以统一的域随机化设置进行训练与评估，保证对比的公平性。基线方法包括两个针对 HOI 任务进行适应性扩展的强基准：

- **InterMimic\***（Xu et al., CVPR 2025）：原为物理基 HOI 跟踪控制器，此处扩展为支持多运动训练；
- **ASAP\***（He et al., 2025, arXiv:2502.01143）：原为全身运动跟踪控制器，此处适配于 HOI 任务。

外环元策略（SAC）采用轻量化参数化，每 $N$ 个内环 PPO 周期训练一次；SAC 动作熵初始温度参数 $\alpha = 0.1$，以增强对最优奖励函数的探索。

### 主结果

#### 跟踪精度

Table I 给出了两个任务上最佳模型的平均跟踪精度对比（20 次评估取平均）。InterReal 在箱体抓取任务上取得了最低的上肢位置跟踪误差（$E_{\text{mulpe}} = 0.0028$）和 3 连杆位置误差（$E_{\text{m3lpe}} = 0.0019$），在箱体推动任务上同样优于所有基线。Fig. 3 的训练曲线进一步表明，InterReal 的归一化跟踪误差在训练过程中持续下降并稳定收敛至更低水平，而 InterMimic\* 和 ASAP\* 的收敛速度与最终精度均不及 InterReal。

![[assets/figures/papers/paper_list_l22_InterReal_A_Unified_Physics_Based_Imitation_Framework_for_Learning_Human/figures/004_Figure_3.jpg]]
*Figure 3: Comparison of tracking accuracy among InterReal and baselines on the box-picking task*

#### 任务成功率

Table II 汇总了任务成功率的对比结果。InterReal 在箱体抓取任务上取得 **96.41%** 的成功率，在箱体推动任务上取得 **87.45%** 的成功率，均为所有方法中最高。这一结果验证了自动奖励学习与 HOI 运动增强对策略鲁棒性和任务完成能力的实质性贡献。

### 消融分析

#### 自动奖励学习机制

消融实验表明，外环元策略驱动的自动奖励学习显著优于固定手工奖励权重。Fig. 5 展示了奖励权重系数随训练时间步的自适应变化曲线：元策略能够根据 PPO 学习进度动态调节各子奖励的相对重要性，在不同任务阶段自动平衡全身跟踪、接触保持与物体操作等目标，从而避免手工调参的次优性。

#### 元学习内部系数 $\delta$

Fig. 4 展示了元学习内部系数 $\delta$（控制权重更新缩放范围的下界）在箱体抓取任务上的消融结果。当 $\delta = 0.1$ 时，HOI 策略达到最佳跟踪性能；过小或过大的 $\delta$ 均会导致性能下降，表明适度的权重探索空间对元策略的有效学习至关重要。

![[assets/figures/papers/paper_list_l22_InterReal_A_Unified_Physics_Based_Imitation_Framework_for_Learning_Human/figures/006_Figure_4.jpg]]
*Figure 4: Ablation results for the internal coefficient δ of the meta-learning on the box-picking task*

#### HOI 运动增强

通过向物体位置施加 XY 平面偏移并利用逆运动学（IK）重新求解手臂关节角度以保持手-物接触，运动增强从单条锚定运动生成多条保持接触一致性的训练轨迹。消融结果显示，该增强方法显著提升了策略对物体位置扰动的泛化能力，是 InterReal 在箱体推动等对接触鲁棒性要求较高的任务上取得高成功率的关键因素之一。

### 失败模式与局限性

尽管 InterReal 在仿真中取得了优异表现，论文明确指出以下局限性：

1. **被动物体跟踪模式**：当前训练范式下，物体运动由参考运动驱动而非策略主动控制，导致策略在面对真实世界中因传感器噪声和检测延迟引起的物体位置扰动时仍存在不稳定性。
2. **任务与平台泛化**：实验仅在 Unitree G1 机器人和箱体搬运/推动两种任务上进行了验证，扩展到更多样化的交互任务（如工具使用、多物体操作）和不同硬件平台仍需进一步工作。
3. **接触动态的边界**：当手-物接触高度动态或涉及非刚体时，基于 IK 的运动增强方法可能存在局限性，该问题尚未在本文中得到系统研究。

### 图表结论速览

| 图表 | 核心结论 |
|------|----------|
| **Table I** | InterReal 在箱体抓取与推动任务上取得最低的 DOF 关节角度和物体位置跟踪误差。 |
| **Table II** | InterReal 在两项任务上均取得最高的任务成功率（96.41% / 87.45%）。 |
| **Fig. 3** | 训练曲线显示 InterReal 的跟踪误差收敛速度和最终精度均优于基线。 |
| **Fig. 4** | $\delta = 0.1$ 时元学习效果最优，验证了权重搜索空间设计的重要性。 |
| **Fig. 5** | 奖励权重系数随训练自适应变化，证明元策略能够动态平衡多目标优化。 |

![[assets/figures/papers/paper_list_l22_InterReal_A_Unified_Physics_Based_Imitation_Framework_for_Learning_Human/figures/003_Table.jpg]]
*Table: I: Comparison of the best mean tracking accuracy on the Box-picking and Box-pushing task. The data records the average of 20 evaluations of the best model on each tracking metric*

![[assets/figures/papers/paper_list_l22_InterReal_A_Unified_Physics_Based_Imitation_Framework_for_Learning_Human/figures/005_Table.jpg]]
*Table: II: Comparison results of task success rate metrics on boxpicking and box-pushing tasks*

## 定位与知识库关联

### 1. 物理模仿学习与全身控制的演进脉络

InterReal 的核心任务——在物理仿真中学习人-物交互（HOI）技能——处于**物理角色动画**与**机器人全身控制**的交叉地带。其直接技术前身可追溯至两类工作：

- **全身运动跟踪控制器**：以 **ASAP**（He et al., 2025, arXiv:2502.01143）为代表，该类方法能够将人体运动数据重定向到仿人机器人上，并在物理仿真中实现高精度的全身运动跟踪。然而，ASAP 等框架在设计时**未显式建模物体动态与手-物接触**，缺乏对交互过程中物体状态变化的闭环感知与反馈。InterReal 正是在 ASAP 架构基础上进行扩展，使其能够同时跟踪人体运动与物体运动，填补了这一空白。

- **物理交互模仿控制器**：**InterMimic**（Xu et al., CVPR 2025）是少数直接针对 HOI 任务的物理模仿方法之一。它通过设计专门的接触奖励与交互约束，实现了对单个 HOI 运动片段的物理跟踪。但 InterMimic 的训练范式是**单运动模仿**——每条策略仅针对一条参考运动进行优化，缺乏对物体位置扰动和运动多样性的泛化能力。InterReal 将 InterMimic 的核心思想纳入更宏大的多运动、多环境训练框架，并通过运动增强与自动奖励学习实现了质的跃升。

实验中的基线方法 **InterMimic\*** 和 **ASAP\*** 即为上述两类工作的 HOI 适应性扩展：前者扩展为多运动训练模式，后者被改造为能够处理 HOI 任务的跟踪控制器，以确保对比的公平性。

### 2. 关键创新与差异化定位

InterReal 的方法论贡献可归结为三个相互耦合的机制，它们共同构成了区别于现有工作的技术壁垒：

**（1）接触感知的运动增强**

现有运动跟踪方法通常采用域随机化（如地面摩擦、质量扰动）来提升策略鲁棒性，但这些扰动**不改变运动本身的几何约束**。InterReal 的 HOI 运动增强方法则直接在运动层面注入结构化扰动：对物体位置施加平面内偏移，并通过逆运动学（IK）重新求解手臂关节角度，**保持手-物接触细节不变**。这意味着增强后的运动在运动学上仍然是“合法”的 HOI 运动，但要求策略学习在物体位置发生偏移时如何调整全身姿态以维持接触。该机制是 InterReal 对物体扰动具有鲁棒性的根本原因。

**（2）元学习驱动的自动奖励调权**

大规模 HOI 任务涉及数十项奖励项（关节跟踪、物体跟踪、接触维持、能量效率等），手工设定固定权重系数不可避免地陷入次优。InterReal 引入的**外环元策略**（基于 SAC）将奖励权重视为可学习的元参数：元策略以关键跟踪误差指标为观测，动态输出各子奖励的权重系数，随内环 PPO 训练进度自适应调节。这一设计使得策略在训练早期可以侧重基础运动跟踪，而在后期逐步加强对接触精度和物体跟踪的优化。消融实验证实，自动奖励学习机制显著优于固定启发式奖励。

**（3）非对称 Actor-Critic 与交互图表征**

InterReal 的策略架构采用非对称设计：Critic 可访问完美状态（包括交互图特征、物体速度与旋转），而 Actor 仅接收不完美状态（排除交互图和部分物体特征）。这一设计在训练时利用额外信息加速价值函数学习，在部署时则不依赖难以精确获取的状态量，增强了 Sim-to-Real 的可行性。交互图（Interaction Graph）作为手-物接触的紧凑表征，被同时用于奖励计算和状态编码，提供了一种统一的人-物关系描述方式。

### 3. 适用边界与约束条件

InterReal 当前的设计存在明确的适用范围限制：

- **任务类型**：仅在**箱体抓取与推动**两类任务上进行了验证。这两类任务的特点是手-物接触相对稳定（抓取后手掌与箱体形成刚性约束，推动时手掌持续接触箱体表面），且物体为刚体。对于涉及多物体协调、工具使用、或非刚体交互的任务，框架的有效性尚待检验。

- **机器人平台**：所有实验均在 **Unitree G1** 仿人机器人模型上进行。G1 的关节构型、质量分布和手掌形态已嵌入运动重定向和物理验证流程中，迁移到其他硬件平台需要重新进行运动重定向和策略训练。

- **被动物体假设**：当前训练模式假定物体是被动的——仅受机器人施加的力作用，不主动运动。这简化了交互建模，但限制了在协作搬运或对抗性交互等场景中的应用。

- **物体感知依赖**：真实部署依赖 **FoundationPose** 进行 6D 物体姿态估计。传感器噪声、遮挡和检测延迟导致的物体位置扰动是尚未完全解决的问题，可能在实际应用中造成任务失败。

### 4. 局限性与开放问题

InterReal 在实验和设计中暴露出若干值得深入探索的开放问题：

**（1）自动奖励学习的可扩展性**

当前元策略的观测空间和动作空间是针对箱体搬运/推动任务定制的。当任务种类扩展至数十种甚至上百种 HOI 技能时，元策略能否学习到可迁移的奖励调权策略？是否存在跨任务的奖励权重共享结构？这涉及元学习的泛化能力边界问题。

**（2）运动增强的接触保真度**

基于逆运动学的增强方法假设手-物接触可以通过腕部位置的重新求解来维持。然而，当接触涉及手指精细操作（如拧瓶盖、按按钮）或接触面发生滑动时，仅调整腕部位置可能不足以保持接触语义。对于高灵巧度操作任务，可能需要引入手指关节的增强或基于动力学的接触仿真。

**（3）真实部署的感知鲁棒性**

Sim-to-Real 部署中，物体姿态估计的噪声和延迟是主要误差源。当前框架未包含针对感知不确定性的显式鲁棒性设计（如状态估计滤波、延迟补偿或基于置信度的策略调节）。如何将感知不确定性纳入策略学习或部署流程，是提升真实世界成功率的关键。

**（4）交互的主动性与适应性**

InterReal 的策略本质上是**运动跟踪器**——其目标是尽可能精确地复现参考运动。这意味着策略缺乏对交互目标的语义理解和主动调整能力。例如，当推动的箱体偏离预期轨迹时，策略是否应该放弃跟踪原始运动、转而采取修正动作？这指向了从“运动模仿”到“任务导向交互”的范式升级需求。

**（5）多机器人协作交互**

当前框架仅考虑单机器人-单物体的交互。扩展到多机器人协作搬运、人-机器人协作组装等场景，需要解决多智能体协调、力分配和通信延迟等新挑战，这超出了现有方法的设计范围。

## 原文 PDF

![[paperPDFs/arxiv_2026/InterReal_A_Unified_Physics_Based_Imitation_Framework_for_Learning_Human_Object_Interaction_Skills.pdf]]
