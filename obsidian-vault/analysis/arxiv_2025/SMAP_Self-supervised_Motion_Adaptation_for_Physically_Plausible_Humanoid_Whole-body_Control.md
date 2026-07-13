---
title: "SMAP: Self-supervised Motion Adaptation for Physically Plausible Humanoid Whole-body Control"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/SMAP_Self_supervised_Motion_Adaptation_for_Physically_Plausible_Humanoid_Whole_body_Control.pdf
project_link: "https://smap-project.github.io/"
code_link: null
aliases:
- SMAP
tags:
- arxiv_2025
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 通过自监督学习将人类运动映射到物理上合理的人形机器人动作空间（Humanoid-Adapter），可消除动作空间不匹配，从而显著提升训练收敛速度和跟踪稳定性。
primary_logic: 使用共享码本的向量量化周期自编码器（VQ-PAE），在无监督条件下学习人类与机器人运动的共享相位流形，将运动分解为离散的原子行为，进而重构出物理一致的人形机器人运动，从而弥合跨域鸿沟。
claims:
- t-SNE可视化显示，经Humanoid-Adapter适配后的运动分布与仿真器中记录的机器人运动分布高度重叠，而重定向的人类运动分布则明显分离。
- 在CMU MoCap数据集上，SMAP在训练样本与新颖样本上的速度跟踪误差、关键点与关节位置误差以及失败次数均显著优于HumanPlus、H2O、OmniH2O、Exbody等现有方法。
- 消融实验表明，移除Humanoid-Adapter导致跟踪误差和失败率明显上升，移除教师-学生蒸馏则显著增加速度误差，从而验证了两项设计的必要性。
- 通过渐进式课程学习和解耦奖励设计，SMAP实现了更快的训练收敛（仅需约一半的迭代次数即可达到Exbody†相同性能水平）。
---

# SMAP: Self-supervised Motion Adaptation for Physically Plausible Humanoid Whole-body Control

> [!tip] 核心洞察
> 使用共享码本的向量量化周期自编码器（VQ-PAE），在无监督条件下学习人类与机器人运动的共享相位流形，将运动分解为离散的原子行为，进而重构出物理一致的人形机器人运动，从而弥合跨域鸿沟。

| 字段 | 内容 |
|------|------|
| 中文题名 | SMAP：自监督运动自适应实现物理合理的人形机器人全身控制 |
| 英文题名 | SMAP: Self-supervised Motion Adaptation for Physically Plausible Humanoid Whole-body Control |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2505.19463) · [Project](https://smap-project.github.io/) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | SMAP |
| Dataset | CMU MoCap |

> [!tip] 效果简介
> - CMU MoCap (已见动作样本) 上，平均线速度误差 (E_vel) SMAP: 0.1698 vs OmniH2O: 0.1791 (降低0.0093 (约5.2%提升))；平均关键点位置误差 (E_mpkpe) SMAP: 0.0608 vs OmniH2O: 0.0619 (降低0.0011)；平均关节位置误差 (E_mpjpe) SMAP: 0.1181 vs OmniH2O: 0.1250 (降低0.0069)。
> - CMU MoCap (新颖动作样本) 上，平均线速度误差 (E_vel) SMAP: 0.2331 vs OmniH2O: 0.2591 (降低0.026 (约10.0%提升))；失败次数 (fail) SMAP: 266 vs OmniH2O: 387 (减少121次)。

## 概要

人形机器人全身控制的核心瓶颈在于**人类运动与机器人动作空间之间存在异构鸿沟**：直接将重定向的人类运动作为模仿目标，往往导致物理上不可行的运动指令，从而降低强化学习（RL）训练效率并引发不稳定行为。为解决这一问题，本文提出 **SMAP（Self-supervised Motion Adaptation）**，一个自监督运动自适应框架，使Unitree H1人形机器人能够执行物理合理且富有表现力的全身动作。

SMAP的核心思想是**通过共享码本的向量量化周期自编码器（VQ-PAE）学习人类与机器人运动的共享相位流形**，将运动分解为离散的原子行为，进而将人类运动映射到物理上可行的人形机器人动作空间。这一关键模块被称为 **Humanoid-Adapter**，它无需显式关节对应即可弥合跨域鸿沟。t-SNE可视化（Figure 2）表明，经Humanoid-Adapter适配后的运动分布与仿真器中记录的机器人运动分布高度重叠，而重定向的人类运动分布则明显分离，从特征空间层面验证了适配的有效性。

在策略学习层面，SMAP采用**渐进式教师-学生蒸馏**：先利用特权信息（真实速度、链接位置、物理参数等）训练教师策略，再通过DAgger框架蒸馏到仅依赖真实传感器观测的学生策略，实现从仿真到真实世界的部署。同时引入**解耦奖励**设计——对上肢赋予更高权重以保证动作精度，对下肢赋予较低权重以优先保持平衡——从而兼顾跟踪精度与运动稳定性。

在CMU MoCap数据集上的仿真评估（Table 1）显示，SMAP在已见动作与新颖动作上的速度跟踪误差、关键点/关节位置误差及失败次数均显著优于HumanPlus、H2O、OmniH2O、Exbody等现有方法。消融实验进一步验证了Humanoid-Adapter与教师-学生蒸馏的必要性：移除前者导致新颖动作失败次数从266激增至392，移除后者则使速度误差从0.1698升至0.2038。渐进式课程学习与解耦奖励的消融同样表明，这两项设计对收敛速度和最终性能均有显著贡献——SMAP仅需约一半的迭代次数即可达到Exbody†的同等性能水平（Figure 9）。

在方法谱系上，SMAP的贡献可归纳为三个关键设计变更：**(1) 训练目标运动来源**从直接使用重定向人类运动转变为经由Humanoid-Adapter适配的物理可行运动；**(2) 策略训练方式**从单阶段RL转变为渐进式教师-学生蒸馏；**(3) 奖励函数结构**从统一全身跟踪奖励转变为上下肢解耦的加权奖励。这些设计共同构成了一个完整的sim-to-real全身控制管线，在保证物理合理性的同时，显著提升了运动模仿的精度与泛化能力。

当前方法的局限性在于：Humanoid-Adapter虽学习了共享相位流形，但缺乏显式关节对应机制，仍可能出现局部微小不匹配；运动多样性受限于所使用的MoCap数据集，对复杂地形或动态交互的泛化尚未充分验证。未来的开放问题包括：如何设计模仿目标以同时保证物理可行性与类人特性，能否引入更精细的时空对齐机制以减少适配误差，以及该方法在大规模多任务场景下的扩展性。



人形机器人因其与人类环境的天然兼容性，被视为执行多样化全身任务的理想载体。然而，实现物理上合理且稳定的全身运动控制，仍是该领域的核心挑战。当前主流方法通常将人类运动捕捉数据通过运动学重定向映射到机器人上，作为模仿学习的参考目标。这一范式面临一个关键瓶颈：**人形机器人与人类之间存在显著的动作空间异构性**。直接使用重定向的人类运动作为模仿目标，往往导致运动在物理上不可行——例如产生违反关节限位、力矩超限或动力学不一致的指令，从而严重降低强化学习的训练效率，并引发不稳定行为。

现有工作虽在全身控制方面取得了进展，但普遍存在以下缺口：**HumanPlus**、**H2O**、**OmniH2O** 和 **Exbody** 等方法均直接以重定向的人类运动为训练目标，未对动作空间的不匹配进行系统性处理。这导致策略在学习初期需要耗费大量样本去“纠正”物理上不可行的参考轨迹，收敛缓慢且对新颖动作的泛化能力受限。此外，这些方法的奖励函数通常采用统一的全身跟踪权重，难以在动作精度与运动稳定性之间取得有效平衡。

针对上述问题，SMAP 的核心动机在于：**能否在模仿学习之前，先行消除人类运动与机器人动作空间之间的域鸿沟？** 如果能够以自监督的方式，将人类运动映射到一个物理上合理、可直接执行的人形机器人动作空间，那么下游的策略学习将不再需要承担“纠正不可行运动”的额外负担，从而显著提升训练效率和跟踪稳定性。这一动机直接引出了 SMAP 的两项关键设计——**Humanoid-Adapter**（自监督运动适配器）和**渐进式教师-学生策略蒸馏**，前者负责弥合跨域鸿沟，后者则在适配运动的基础上实现高效、鲁棒的 sim-to-real 控制。



## 核心方法与创新机理

SMAP 的核心创新在于系统性地解决了**人形机器人与人类运动之间的动作空间异构性**这一瓶颈。现有方法（如 HumanPlus、OmniH2O、Exbody 等）通常直接将重定向的人类运动作为模仿目标，但人类关节构型、质量分布和动力学特性与机器人存在本质差异，导致训练目标在物理上不可行，进而引发训练效率低下和行为不稳定。SMAP 通过三个关键的 **changed slots** 重构了从人类运动到机器人控制的学习范式。

### 1. 训练目标运动来源：从重定向运动到物理适配运动

最根本的改变在于训练目标的生成方式。SMAP 引入 **Humanoid-Adapter**——一个基于向量量化周期自编码器（VQ-PAE）的自监督预训练模块——将人类运动映射到物理上合理的人形机器人动作空间，而非直接使用重定向的人类运动。

Humanoid-Adapter 的核心机制是学习一个**共享相位流形**（shared phase manifold）和**共享码本**（shared codebook）。具体而言，它同时训练两个 VQ-PAE，分别处理人类运动序列 $S^h$ 和机器人运动序列 $S^r$，并通过共享的离散码本 $\mathcal{C} = (c_1, c_2, ..., c_n)$ 将运动分解为有限个原子行为。相位流形映射 $p = \Psi(\alpha, \phi) = \alpha^0 \sin(2\pi\phi) + \alpha^1 \cos(2\pi\phi)$ 将每一帧姿态嵌入到连续的周期性流形上，使得具有相似相位的人类和机器人运动在隐空间中对齐。训练损失为两者的重建损失之和：$\mathcal{L} = \|s^r - \hat{s}^r\|_2 + \|s^h - \hat{s}^h\|_2$。

这一设计的决定性证据来自 t-SNE 可视化：经 Humanoid-Adapter 适配后的运动分布与仿真器中记录的机器人运动分布高度重叠，而重定向的人类运动分布则明显分离（Figure 2）。这表明适配器有效弥合了跨域鸿沟，将不可行的模仿目标转化为机器人可执行的参考运动。

### 2. 策略训练方式：从单阶段 RL 到渐进式教师-学生蒸馏

SMAP 将传统的单阶段强化学习训练重构为**渐进式两阶段教师-学生蒸馏**框架。第一阶段，教师策略 $\hat{\pi}$ 利用仿真器中的特权信息（真实速度、链接位置、物理参数等）进行 RL 训练，获得高质量的控制策略。第二阶段，通过 DAgger 框架将教师策略蒸馏到学生策略，学生策略仅依赖真实世界可获取的观测（IMU、关节状态、历史观测等），蒸馏损失为 $\mathcal{L}_{distill} = \|a_t - \hat{a}_t\|_2$。

这种设计的关键优势在于：教师策略可以充分利用仿真器信息学习精确的运动跟踪，而学生策略通过模仿教师的行为，间接获得了对速度、动力学等隐变量的感知能力。消融实验验证了这一设计的必要性——移除教师-学生蒸馏后，速度误差 $E_{vel}$ 从 0.1698 升至 0.2038，说明蒸馏对速度跟踪精度至关重要。

### 3. 奖励函数结构：从统一跟踪奖励到解耦奖励

SMAP 提出**解耦奖励**设计，将上肢和下肢的跟踪目标分离并赋予不同权重。上肢（手臂、躯干）被赋予更高权重以保证动作表现精度，下肢（腿部）被赋予较低权重以优先保持动态平衡。这一设计源于一个关键洞察：在全身模仿任务中，精确复现手臂姿态与维持稳定行走之间存在天然张力，统一权重往往导致策略在两者之间做出次优折衷。

消融实验中，移除解耦奖励后，关节跟踪误差 $E_{mpjpe}$ 从 0.1181 升至 0.1283，失败次数从 1731 升至 1775，证明分离上下肢权重可同时提升精度与稳定性。

### 创新协同效应

上述三个 changed slots 并非孤立设计，而是形成协同效应：Humanoid-Adapter 提供物理可行的模仿目标，降低了策略学习的难度；教师-学生蒸馏利用特权信息弥补传感器观测的不足；解耦奖励在可行目标基础上进一步平衡精度与稳定性。三者共同作用使得 SMAP 在训练效率上显著优于现有方法——仅需约一半的迭代次数即可达到 Exbody† 的相同性能水平（Figure 9）。



SMAP 的整体流程围绕一个核心矛盾展开：**人类运动与机器人动作空间之间的异构性**。直接使用重定向的人类运动作为模仿目标，会导致运动在物理上不可行，进而降低强化学习训练效率并引发不稳定行为。为此，SMAP 将问题分解为两个阶段：先通过自监督学习弥合跨域鸿沟，再通过渐进式策略学习实现稳定控制。

### 流程概览

图 3 给出了 SMAP 的完整流水线，其输入输出关系如下：

1. **运动适配阶段**：给定一段人类运动序列，预训练的 **Humanoid-Adapter** 将其映射为物理上合理的人形机器人运动。这一模块是 SMAP 的关键创新，它利用向量量化周期自编码器（VQ-PAE）学习人类与机器人运动的共享相位流形，从而将异构的动作空间对齐到同一离散码本空间中。
2. **策略训练阶段**：适配后的机器人运动作为模仿目标，送入渐进式教师-学生蒸馏框架。**教师策略**在仿真器中利用特权信息（真实速度、链接位置、物理参数等）进行 RL 训练，产生高质量的控制信号；**学生策略**则通过 DAgger 蒸馏从教师策略学习，仅依赖真实世界可获取的观测（IMU、关节状态、历史观测等），完成 sim-to-real 部署。
3. **奖励设计**：训练过程中采用**解耦奖励**机制，对上肢跟踪赋予更高权重以保证动作精度，对下肢跟踪赋予较低权重以优先保持平衡。

### 模块间关系

上述三个核心模块——Humanoid-Adapter、教师-学生蒸馏、解耦奖励——并非独立运作，而是构成了一条因果链：

- **Humanoid-Adapter** 从源头上消除了动作空间不匹配，使模仿目标本身变得物理可行。t-SNE 可视化（图 2）直观地验证了这一点：经适配后的运动分布与仿真器中记录的机器人运动分布高度重叠，而重定向的人类运动分布则明显分离。
- **教师-学生蒸馏** 将特权信息的优势压缩到仅依赖真实传感器观测的学生策略中，使速度跟踪等关键能力得以保留。消融实验表明，移除蒸馏后速度误差 $E_{vel}$ 从 0.1698 升至 0.2038。
- **解耦奖励** 在精度与稳定性之间取得平衡：消融解耦奖励后，关节跟踪误差 $E_{mpjpe}$ 从 0.1181 升至 0.1283，失败次数从 1731 升至 1775。

三者协同作用的结果是：SMAP 在 CMU MoCap 数据集上，无论是已见动作还是新颖动作，其速度跟踪误差、关键点与关节位置误差以及失败次数均显著优于 HumanPlus、H2O、OmniH2O、Exbody 等现有方法（见表 1）。同时，渐进式课程学习和解耦奖励设计使训练收敛速度大幅提升——仅需约一半的迭代次数即可达到 Exbody† 的同等性能水平。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2505_19463/figures/003_Figure_3.jpg]]
*Figure 3: Pipeline of SMAP . Given human motion, we use the proposed Humanoid-Adapter (details shown in Fig. 9), pre-trained ( ) to adapt human motion into corresponding, physically plausible humanoid robot motion. Our sim-to-real policy ( ) is distilled via imitation learning from an RL-trained privileged teacher policy that leverages privileged information with proposed decoupled reward. The policy is transferred to the real world*



SMAP 框架的核心由两个模块构成：**Humanoid-Adapter**（运动适配器）与**渐进式控制策略学习**（含教师-学生蒸馏与解耦奖励）。前者解决人类运动与人形机器人动作空间之间的异构鸿沟，后者在适配后的运动空间上高效训练可部署的全身控制策略。

### Humanoid-Adapter：基于共享码本的向量量化周期自编码器

Humanoid-Adapter 是一个预训练的运动映射网络，其设计目标是将人类运动序列 $S^h$ 映射到物理上合理的人形机器人运动序列 $S^r$。该模块的核心创新在于**共享相位流形**与**离散码本**的联合学习。

**相位流形映射** 将每一帧姿态编码为流形上的一个点。给定向量振幅 $\alpha$ 和相位参数 $\phi$，映射函数定义为：

$$p = \Psi(\alpha, \phi) = \alpha^{0} \sin(2\pi\phi) + \alpha^{1} \cos(2\pi\phi)$$

其中 $\alpha^{0}$ 和 $\alpha^{1}$ 为振幅向量的两个分量，$\phi$ 为归一化相位。这一参数化方式将周期性运动（如行走、摆臂）自然嵌入到连续流形中，使得不同运动模式在流形上形成可区分的轨迹。

**离散码本** 用于将连续的流形表示量化为离散的原子行为。码本定义为一个可学习的嵌入向量集合：

$$\mathcal{C} = (c_{1}, c_{2}, c_{3} \ldots c_{n})$$

每个 $c_i$ 是一个嵌入向量，代表一种原子运动基元。通过向量量化，连续的运动流形被离散化为有限的行为单元，使得人类与机器人运动可以在同一离散空间中对齐。

**双编码器架构** 分别处理人类运动 $S^h$ 和机器人运动 $S^r$，但共享同一个码本 $\mathcal{C}$。训练损失为两个域的重建误差之和：

$$\mathcal{L} = \|s^{r} - \hat{s}^{r}\|_{2} + \|s^{h} - \hat{s}^{h}\|_{2}$$

其中 $\hat{s}^{r}$ 和 $\hat{s}^{h}$ 分别为机器人运动与人类运动通过各自 VQ-PAE 重建的结果。共享码本强制两个编码器学习相同的离散行为空间，从而在无监督条件下实现跨域对齐。训练完成后，将人类运动输入其编码器，经码本量化后由机器人解码器重建，即可获得物理上可行的适配运动。

消融实验验证了码本尺寸对适配质量的影响：码本大小为 32 时，平均关节位置误差最低（10.6 cm），尺寸为 16 或 64 时误差略高，表明适中的离散化粒度最有利于行为空间的表达与泛化。

### 渐进式控制策略学习：教师-学生蒸馏与解耦奖励

在获得适配后的运动目标后，SMAP 采用两阶段渐进式训练策略来学习全身控制。

**第一阶段：教师策略训练。** 教师策略 $\hat{\pi}$ 在仿真器中利用特权信息进行强化学习训练。特权信息包括真实速度、链接位置、物理参数等，这些信息在真实世界中无法直接获取，但能为策略提供丰富的监督信号。训练目标为最大化累计折扣奖励：

$$\mathbb{E}\left[\sum_{t=1}^{T} \gamma^{t-1} r_{t}\right]$$

其中 $\gamma$ 为折扣因子，$r_t$ 为解耦奖励函数给出的即时奖励。

**解耦奖励设计** 是 SMAP 区别于统一全身跟踪奖励的关键改进。该设计将上肢与下肢的跟踪目标分离，对上肢（如手臂关节位置和末端关键点）赋予更高权重以保证动作精度，对下肢则降低权重以优先保持平衡。这一设计源于人形机器人的物理约束：下肢承担支撑和平衡任务，过强的位置跟踪约束可能干扰稳定控制。消融实验证实，移除解耦奖励后，关节跟踪误差 $E_{mpjpe}$ 从 0.1181 升至 0.1283，失败次数从 1731 升至 1775。

**第二阶段：学生策略蒸馏。** 学生策略仅使用真实世界可获取的观测（IMU 读数、关节状态、历史观测等），通过 DAgger 框架从教师策略蒸馏。蒸馏损失为教师动作 $a_t$ 与学生动作 $\hat{a}_t$ 之间的 L2 距离：

$$\mathcal{L}_{distill} = \|a_{t} - \hat{a}_{t}\|_{2}$$

这一设计使学生策略在仅依赖真实传感器信息的情况下，仍能逼近教师策略的控制质量。消融实验表明，移除教师-学生蒸馏后，速度跟踪误差 $E_{vel}$ 从 0.1698 显著升至 0.2038，验证了特权信息蒸馏对速度跟踪精度的关键作用。学生策略的历史观测长度设置为 10 步时达到最佳性能。

### 动作空间与 MDP 形式化

SMAP 将全身控制建模为马尔可夫决策过程：

$$\mathcal{M} = \langle \boldsymbol{S}, \mathcal{A}, \bar{T}, \mathcal{R}, \boldsymbol{\gamma} \rangle$$

其中 $\boldsymbol{S}$ 为状态空间，$\mathcal{A}$ 为动作空间，$\bar{T}$ 为转移动态，$\mathcal{R}$ 为奖励函数，$\boldsymbol{\gamma}$ 为折扣因子。人形机器人的动作空间定义为：

$$\boldsymbol{a}_{t} \in \mathbb{R}^{n \times 3}$$

其中 $n$ 为驱动自由度数，每个自由度由 PD 控制器的目标位置指定。策略输出的动作直接作为 PD 控制器的参考输入，驱动机器人关节跟踪目标姿态。



## 实验与关键发现

### 实验设置

所有实验均基于Unitree H1人形机器人模型，在IsaacGym仿真环境中使用4096个并行环境进行训练。评估数据集为CMU MoCap，分为已见动作样本（Trained Motion Sample）和新颖动作样本（Novel Motion Sample）两部分。对比方法包括**HumanPlus**、**H2O**、**OmniH2O**、**Exbody**、**Exbody†**以及**Exbody + AMP**，均按照各自原始论文的设置进行复现或直接引用其报告的结果。评估指标包括平均线速度误差 $E_{vel}$、平均关键点位置误差 $E_{mpkpe}$、平均关节位置误差 $E_{mpjpe}$ 以及失败次数（fail）。

### 主实验结果

Table 1 展示了SMAP与各基线方法在CMU MoCap数据集上的定量对比。在已见动作样本上，SMAP在所有指标上均取得最优结果：$E_{vel}$ 达到0.1698，相比最强基线OmniH2O的0.1791降低约5.2%；$E_{mpkpe}$ 为0.0608，$E_{mpjpe}$ 为0.1181，失败次数为1731，均优于所有对比方法。在新颖动作样本上，SMAP的优势更为显著：$E_{vel}$ 从OmniH2O的0.2591降至0.2331（提升约10.0%），失败次数从387降至266，表明Humanoid-Adapter赋予的物理合理性显著增强了策略对未见过动作的泛化能力。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2505_19463/figures/005_Table_1.jpg]]
*Table 1: Quantitative Comparisons and Ablation Study. Simulation-based motion imitation evaluation of our method and state-of-the-art (SOTA) approaches on the CMU MoCap dataset [5] for the Unitree H1 robot*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2505_19463/figures/013_Table_1.jpg]]
*Table 1: Regularization rewards Regularization rewards for preventing undesired behaviors for sim-to-real transfer*

值得注意的是，SMAP在速度跟踪精度上的优势尤为突出。这源于教师-学生蒸馏机制将特权信息（如真实速度）有效蒸馏到仅依赖历史观测的学生策略中，使学生策略能够更精准地跟踪速度目标。

### 消融实验

Table 1 同时报告了完整的消融实验结果，Figure 6 提供了挑战性动作上的可视化对比。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2505_19463/figures/007_Figure_6.jpg]]
*Figure 6: Ablation study. Visualization performance in the simulation on challenging motion sample*

**Humanoid-Adapter的作用。** 移除Humanoid-Adapter后，所有指标均出现恶化，尤其是新颖动作上的失败次数从266激增至392，$E_{vel}$ 从0.2331升至0.2465。这验证了Humanoid-Adapter通过将人类运动适配到物理可行的人形机器人动作空间，是提升训练稳定性和泛化能力的关键设计。

**教师-学生蒸馏的作用。** 移除教师-学生蒸馏（w/o teacher-student distillation）导致速度误差 $E_{vel}$ 从0.1698显著升至0.2038，为所有消融项中速度指标降幅最大的一项。Figure 7 通过绿色目标点与红色实际关节位置的可视化对比，直观展示了蒸馏对跟踪精度的贡献。

**渐进式学习的作用。** 去除渐进式课程学习（w/o progressive）后，新颖动作上的失败次数从266升至299，表明课程式地从适配运动逐步过渡到重定向运动有助于策略平稳学习。

**解耦奖励的作用。** 移除解耦奖励（w/o decoupled reward）后，$E_{mpjpe}$ 从0.1181升至0.1283，失败次数从1731升至1775，证明分离上下肢权重（对上肢赋予更高精度权重，对下肢降低权重以优先保持平衡）可同时提升跟踪精度与运动稳定性。

**码本尺寸的影响。** Table 3（附录）显示，Humanoid-Adapter的码本尺寸为32时平均关节位置误差最低（10.6 cm），尺寸为16和64时误差略高，表明适中的离散化粒度最有利于学习共享相位流形。

**历史观测长度的影响。** 学生策略的历史观测长度设置为10步时达到最佳性能（见Figure 10），过短则信息不足，过长则引入冗余。

### 训练效率分析

Figure 9 对比了SMAP与Exbody†的训练曲线。得益于渐进式课程学习和解耦奖励设计，SMAP仅需约一半的迭代次数即可达到Exbody†的相同性能水平，展现出显著的训练效率优势。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2505_19463/figures/010_Figure_9.jpg]]
*Figure 9: Training Curves Comparison between SAMP and Exbody†*

### 定性结果

Figure 5 展示了仿真中H1机器人执行转身行走、挥手、单腿跳跃等多种全身表现性动作的定性结果。Figure 8 展示了真实世界中H1机器人的成功部署效果，验证了SMAP的sim-to-real迁移能力。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2505_19463/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative results on the H1 robot in simulation*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2505_19463/figures/009_Figure_8.jpg]]
*Figure 8: Qualitative result on the H1 robot in real world*

### 失败模式与局限

尽管SMAP在整体性能上表现优异，消融实验揭示了以下边界情况：（1）移除Humanoid-Adapter后，机器人在新颖动作上失败率急剧上升，说明未经适配的重定向人类运动在物理上不可行，导致策略无法稳定跟踪；（2）在解耦奖励消融中，上下肢统一权重使得平衡与精度之间出现冲突，尤其在快速移动或单腿支撑等挑战性动作上失败增多；（3）由于Humanoid-Adapter缺乏显式的关节对应机制，在局部关节位置上仍可能出现微小不匹配，这在复杂动作的精细跟踪中可能累积为可见误差。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2505_19463/figures/008_Figure_7.jpg]]
*Figure 7: Ablation study of teacher-student distillation. The green points represent the imitation goal, while the red points correspond to the DOF position*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2505_19463/figures/011_Figure_10.jpg]]
*Figure 10: Ablation Study Results (Best values in bold)*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2505_19463/figures/015_Table_3.jpg]]
*Table 3: Mean per joint position error (cm) of Humanoid-Adapter*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2505_19463/figures/001_Figure_1.jpg]]
*Figure 1: Our framework enables humanoid robot execute various expressive whole-body motions. The robot can (a) turn around and walk forward, (b) wave hello, (c) swing arms while advancing, (d) jump on one leg, (e) walk fast*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2505_19463/figures/002_Figure_2.jpg]]
*Figure 2: t-SNE visualization of the distribution of retargeted human motion, noid robot motion (recorded within the simulator), and motion adapted by Humanoid-Adapter on the CMU MoCap dataset [5]*



## 定位与知识库关联

### 1. 核心问题定位：人形机器人运动模仿中的动作空间异构性

SMAP 的核心贡献在于识别并解决了人形机器人全身控制中长期被忽视的一个瓶颈问题：**人类运动与人形机器人运动之间的动作空间异构性**。传统方法（如 HumanPlus、H2O、OmniH2O、Exbody 等）通常直接使用重定向的人类运动作为模仿目标进行强化学习训练。然而，由于人形机器人的运动学约束、质量分布和驱动方式与人类存在本质差异，重定向后的运动往往在物理上不可行，导致学习效率低下、跟踪不稳定，甚至引发灾难性失败。

SMAP 的关键洞察在于：**通过自监督学习将人类运动映射到物理上合理的人形机器人动作空间，可消除动作空间不匹配，从而显著提升训练收敛速度和跟踪稳定性**。这一洞察的验证证据来自 t-SNE 可视化（Figure 2）：经 Humanoid-Adapter 适配后的运动分布与仿真器中记录的机器人运动分布高度重叠，而重定向的人类运动分布则明显分离，直观地证明了跨域鸿沟的存在及其弥合效果。

### 2. 方法谱系中的定位与创新维度

SMAP 在人形机器人全身控制的方法谱系中占据了一个独特位置，其创新体现在三个相互耦合的维度上：

**维度一：训练目标运动来源的范式转换。** 现有方法（HumanPlus、H2O、OmniH2O、Exbody 等）直接使用重定向的人类运动作为模仿目标。SMAP 引入了 **Humanoid-Adapter**——一个基于向量量化周期自编码器（VQ-PAE）的预训练模块，将人类运动适配为物理上可行的人形机器人运动。这一设计的核心机制是：利用共享码本学习人类与机器人运动的共享相位流形，将运动分解为离散的原子行为，进而重构出物理一致的人形机器人运动。码本尺寸的消融实验表明，尺寸为 32 时平均关节位置误差最低（10.6 cm），16 和 64 时略高，验证了离散表示在运动适配中的有效性。

**维度二：策略训练方式的渐进式设计。** 传统方法通常采用单阶段强化学习直接训练可部署策略。SMAP 采用**渐进式教师-学生蒸馏**：第一阶段利用特权信息（真实速度、链接位置、物理参数等）训练教师策略，提供高质量监督信号；第二阶段通过 DAgger 框架将教师策略蒸馏到仅使用真实传感器观测（IMU、关节状态、历史观测）的学生策略。消融实验显示，移除教师-学生蒸馏导致速度误差 $E_{vel}$ 从 0.1698 升至 0.2038，表明蒸馏对速度跟踪精度至关重要。学生策略的历史观测长度设置为 10 步时达到最佳性能。

**维度三：奖励函数结构的解耦设计。** 现有方法通常采用统一的全身跟踪奖励。SMAP 引入**解耦奖励**：对上肢（包括手臂和手部关键点）赋予更高权重以保证动作精度，对下肢赋予较低权重以优先保持平衡。消融实验表明，移除解耦奖励后，关节跟踪误差 $E_{mpjpe}$ 从 0.1181 升至 0.1283，失败次数从 1731 升至 1775，证明分离上下肢权重可同时提升精度与稳定性。

### 3. 与现有方法的对比分析

在 CMU MoCap 数据集上的定量对比（Table 1）显示，SMAP 在已见动作和新颖动作样本上均显著优于现有方法：

- **已见动作样本**：SMAP 的平均线速度误差 $E_{vel}$ 为 0.1698，优于 OmniH2O 的 0.1791；平均关键点位置误差 $E_{mpkpe}$ 为 0.0608，优于 OmniH2O 的 0.0619；失败次数为 1731，少于 OmniH2O 的 1899。
- **新颖动作样本**：SMAP 的 $E_{vel}$ 为 0.2331，较 OmniH2O 的 0.2591 降低约 10.0%；失败次数为 266，较 OmniH2O 的 387 减少 121 次。

值得注意的是，SMAP 在训练效率上也展现出优势：通过渐进式课程学习和解耦奖励设计，SMAP 仅需约一半的迭代次数即可达到 Exbody† 相同性能水平（Figure 9）。

### 4. 适用边界与局限

尽管 SMAP 在运动适配和跟踪稳定性上取得了显著进展，其适用边界仍需审慎界定：

1. **关节对应关系的隐式性**：Humanoid-Adapter 通过共享码本学习隐式的相位流形对齐，但缺乏显式的关节对应机制。这可能导致局部微小不匹配，尤其是在复杂或极端姿态下。如何引入显式的关节对应或更精细的时空对齐方法，是进一步提升适配精度的开放问题。

2. **数据依赖性**：当前方法依赖于人类运动捕捉数据（CMU MoCap）和模拟器中的 RL 训练，运动多样性受限于数据集规模。对于复杂地形、动态交互或多任务场景的泛化能力尚未充分验证。

3. **运动类人性的保持**：Humanoid-Adapter 在保证物理可行性的同时，可能牺牲部分类人特性。如何设计模仿目标，使其既保证物理可行性又保持类人特性，是一个根本性的开放问题。

### 5. 知识库定位与未来方向

SMAP 在人形机器人全身控制的知识库中定位为**连接人类运动与机器人执行的桥梁方法**。其核心贡献——VQ-PAE 驱动的运动适配器——为后续研究提供了可扩展的框架。未来的研究方向包括：

- **显式关节对应机制**：引入基于运动学链的显式对应关系，减少适配中的微小不匹配。
- **更大规模数据集的扩展性**：验证方法在更大规模、更复杂的人类运动数据集上的表现。
- **多任务与动态交互**：将运动适配框架扩展到需要实时环境感知和交互的任务场景。

总体而言，SMAP 通过自监督运动适配、渐进式教师-学生蒸馏和解耦奖励设计，在人形机器人全身控制领域建立了一个新的性能基线，其核心洞察——消除动作空间异构性——为后续研究指明了关键方向。



## 原文 PDF

![[paperPDFs/arxiv_2025/SMAP_Self_supervised_Motion_Adaptation_for_Physically_Plausible_Humanoid_Whole_body_Control.pdf]]
