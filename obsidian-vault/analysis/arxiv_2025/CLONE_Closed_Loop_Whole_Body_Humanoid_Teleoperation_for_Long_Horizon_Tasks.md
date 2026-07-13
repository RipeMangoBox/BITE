---
title: "CLONE: Closed-Loop Whole-Body Humanoid Teleoperation for Long-Horizon Tasks"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/CLONE_Closed_Loop_Whole_Body_Humanoid_Teleoperation_for_Long_Horizon_Tasks.pdf
project_link: https://humanoid-clone.github.io/
code_link: null
aliases:
- CLONE
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 采用基于混合专家（MoE）的策略实现多种运动模式自适应协调，并结合LiDAR里程计与空间锚点进行闭环位置误差修正。
primary_logic: 通过MoE专家网络对不同运动类型（行走、下蹲、跳跃等）进行专业化处理，解决了单一策略难以协调多样性运动的难题，同时引入闭环反馈消除累积漂移，从而仅需MR头显的头部与手部追踪即可实现高保真全身遥操作。
claims:
- CLONE在直行跟踪中实现5.1厘米平均全局位置误差，开环系统则因漂移导致任务失败。
- 在CLONED数据集上，CLONE相比MLP架构和OmniH2O数据训练的基线，在运动跟踪误差（MPKPE, R-MPKPE, 速度误差, 手朝向误差）上全面显著优于。
- 消融实验表明，MoE架构（3层4专家）对处理多样化运动至关重要，仅使用约20%的训练数据量就超过了基于全量数据训练的基线。
- CLONE成功完成复杂长时任务（如捡起地面物体），展示了稳定的全身协调能力和低漂移特性。
---

# CLONE: Closed-Loop Whole-Body Humanoid Teleoperation for Long-Horizon Tasks

> [!tip] 核心洞察
> 通过MoE专家网络对不同运动类型（行走、下蹲、跳跃等）进行专业化处理，解决了单一策略难以协调多样性运动的难题，同时引入闭环反馈消除累积漂移，从而仅需MR头显的头部与手部追踪即可实现高保真全身遥操作。

| 字段 | 内容 |
|------|------|
| 中文题名 | CLONE：面向长时任务的人形机器人闭环全身遥操作 |
| 英文题名 | CLONE: Closed-Loop Whole-Body Humanoid Teleoperation for Long-Horizon Tasks |
| 会议/期刊 | arXiv 2025 |
| Links | [Project](https://humanoid-clone.github.io/) · [paper](https://arxiv.org/abs/2506.08931) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | CLONE |
| Dataset | CLONED dataset, Real-world straight-path tracking, Real-world curved-path tracking |

> [!tip] 效果简介
> - CLONED dataset 上，Mean Per-Keybody Position Error (MPKPE) (mm) 87.84 vs CLONE†: 113.97, CLONE∗: 102.20 (相对 CLONE† 降低 26.13; 相对 CLONE∗ 降低 14.36)；Root-Relative MPKPE (mm) 33.30 vs CLONE†: 35.55, CLONE∗: 41.07 (相对 CLONE† 降低 2.25; 相对 CLONE∗ 降低 7.77)；Average Joint Velocity Error (mm/s) 227.17 vs CLONE†: 245.11, CLONE∗: 309.65 (相对 CLONE† 降低 17.94; 相对 CLONE∗ 降低 82.48)。
> - Real-world straight-path tracking 上，Mean global position tracking error (cm) 5.1 vs 开环遥操作典型漂移无法完成长距离任务（未汇报具体数值） (开环无闭环修正的系统漂移严重，CLONE 保持厘米级精度)。
> - Real-world curved-path tracking 上，Mean translational error / Mean rotational drift 20 cm / 2° vs 开环系统典型漂移更大 (闭环修正有效抑制转角和位移漂移)。

## 概要

人形机器人遥操作面临一个关键瓶颈：现有系统通常将上半身与下半身的控制解耦，以局部稳定性换取全局协调性，牺牲了自然的全身运动能力；同时，开环控制缺乏实时的位置反馈，导致长时间操作中累积显著的位置漂移，使复杂长时任务难以完成。CLONE 系统针对这一瓶颈，提出了两个核心控制变量：**混合专家（MoE）策略架构**与**闭环误差修正机制**。其核心洞察在于，通过 MoE 专家网络对行走、下蹲、跳跃等不同运动类型进行专业化处理，解决了单一策略难以协调多样性运动的难题；同时引入基于 LiDAR 里程计与空间锚点的闭环反馈，消除累积漂移，从而仅需 MR 头显的头部与手部追踪即可实现高保真全身遥操作。

在方法谱系上，CLONE 属于基于强化学习的全身遥操作框架，与 **OmniH2O** 等基于大规模 MLP 的开环系统形成对比。其关键改进包括：将策略架构从单一 MLP 替换为 3 层、4 专家的 MoE 网络（Top-2 路由），引入闭环全局位置误差修正，以及构建精心筛选的 CLONED 数据集（345 个动作序列，仅约 OmniH2O 数据量的 20%）。训练采用教师-学生蒸馏范式，教师策略使用特权信息，学生策略仅依赖真实观测（IMU、里程计、参考运动），并通过 PPO 优化。

实验证据表明，CLONE 在 CLONED 数据集上的运动跟踪误差（MPKPE 87.84 mm、根相对 MPKPE 33.30 mm、速度误差 227.17 mm/s、手朝向误差 3.61）全面优于 MLP 架构变体和 OmniH2O 数据训练的基线（Table 1）。真实世界直行跟踪中，CLONE 实现平均全局位置误差仅 5.1 cm，而开环系统因漂移导致任务失败（Figure 4）；弯曲路径下平移误差约 20 cm、旋转漂移约 2°。消融实验进一步证实，MoE 架构对处理多样化运动至关重要，仅使用约 20% 训练数据即超越全量数据训练的基线（Table A3）。

CLONE 仍存在若干局限：高动态动作（如跳跃）的局部关节精度有所折衷；稀疏输入缺乏足部触地等信息，限制了非结构地形下的极端稳定性；闭环修正依赖 LiDAR，在退化环境中精度可能下降；当前策略专为 Unitree G1 训练，跨形态迁移需重新适配。



人形机器人因其与人类环境的高度兼容性，被认为是执行复杂长时任务的理想载体。然而，实现高保真的全身遥操作仍面临两大核心瓶颈。

**解耦控制与自然协调的矛盾**。现有人形机器人遥操作系统普遍将上半身与下半身的控制解耦，以简化稳定性约束，但这牺牲了人类运动固有的全身协调性。例如，OmniH2O 等基线系统采用单一大规模 MLP 策略，难以同时捕捉行走、下蹲、跳跃等多种运动模式的内在关联，导致动作僵硬且缺乏自然过渡。

**开环控制的累积漂移**。主流遥操作方案依赖开环执行操作者的运动指令，缺乏实时位置反馈。在长时间操作中，LiDAR 里程计、惯性测量单元（IMU）等传感器的微小误差会持续累积，使机器人的全局位置与操作者意图之间产生显著漂移。实验表明，开环系统在直行跟踪任务中会因漂移导致任务失败，而 CLONE 在相同条件下仅产生 5.1 厘米的平均全局位置误差（Figure 4）。

**稀疏输入下的全身控制难题**。为降低操作者负担，理想系统应仅需混合现实（MR）头显提供的头部与手部追踪信息。然而，从如此稀疏的输入中推断出协调的全身运动——尤其是下肢步态与躯干姿态——对策略网络的表征能力提出了极高要求。

上述挑战共同指向一个关键问题：**如何在仅依赖头部和手部稀疏输入的条件下，实现多种运动模式的自适应协调，并消除长时间操作中的累积位置漂移？** CLONE 通过混合专家（MoE）策略架构与闭环误差修正机制对此给出了系统性的回答。



## 核心方法与创新机理

CLONE 的核心创新在于通过**混合专家（MoE）策略架构**与**闭环误差修正机制**两个关键“changed slots”，系统性地解决了现有人形机器人遥操作中的根本瓶颈：上下半身控制解耦导致的不自然协调，以及开环控制下长期操作累积的显著位置漂移。

### 1. 从单一大规模网络到混合专家（MoE）策略

传统遥操作系统（如 OmniH2O）通常采用单一的大规模 MLP 网络来学习从稀疏输入到全身动作的映射。这种方式在面对行走、下蹲、跳跃等高度多样化的运动模式时，单一网络难以有效协调全身自由度，往往牺牲自然的上下半身协调性。

CLONE 将策略架构从**单一大规模 MLP** 替换为**混合专家（MoE）网络**（3 层，4 个专家，Top-2 路由），其核心机理在于：

- **专业化分工**：每个专家网络对不同运动类型进行专业化处理，MoE 层的输出由路由权重加权的 Top-k 专家输出之和构成：

$$f = \sum_{i}^{k} w_{i} \cdot E_{i}(\cdot)$$

- **负载均衡**：为防止策略坍缩至少数专家，引入专家负载均衡损失：

$$\mathcal{L}_{balance} = \sum_{l=1}^{L} \sum_{e=1}^{N} [\mathrm{max}(p_{e} - \frac{1 + \epsilon}{N}, 0) + \mathrm{min}(\frac{1 - \epsilon}{N} - p_{e}, 0)]$$

这一架构改变使得 CLONE 在仅使用约 20% 训练数据量（345 个动作序列 vs. >8k）的情况下，在所有运动跟踪指标上全面超越基于全量数据训练的 MLP 基线（表 1）。消融实验证实，移除 MoE 架构（CLONE†）会导致 MPKPE 从 87.84 mm 恶化至 113.97 mm，验证了 MoE 对处理多样化运动的关键作用。

### 2. 从开环遥操作到闭环误差修正

开环遥操作系统缺乏实时位置反馈，操作员与机器人之间的全局位置误差会随时间累积，导致长时间操作中产生显著漂移，最终使任务失败。

CLONE 引入了**闭环误差修正机制**，将 **LiDAR 里程计**与 **Apple Vision Pro（AVP）空间锚点**追踪提供的全局位置差直接输入学生策略，使其生成能够系统性减少位置漂移的动作。为模拟真实 LiDAR 里程计误差特性，训练阶段引入了速度依赖的随机噪声模型：

$$\mathrm{d} \vec{P}_{\mathrm{head}} = \dot{\vec{p}}_{\mathrm{head}} \mathrm{d} t + (\frac{\| \dot{\vec{p}}_{\mathrm{head}} \|}{c_{\mathrm{vel}}} + c_{\mathrm{min}}) \mathrm{d} \vec{W}$$

其中噪声强度与头部运动速度成正比，使策略在训练中即学会对抗真实部署中的测量噪声。

这一创新带来了决定性的性能提升：在真实世界直行跟踪测试中，CLONE 实现了 **5.1 cm 的平均全局位置跟踪误差**（最大偏差 12.0 cm，距离 8.9 m），而开环系统因漂移累积导致任务失败（图 4）。在弯曲路径跟踪中，CLONE 同样将平移误差和旋转漂移分别控制在 20 cm 和 2° 以内，有效抑制了转角和位移的累积漂移。

### 3. 创新协同效应

MoE 架构与闭环误差修正并非孤立创新，二者形成协同：MoE 提供了多样运动模式下的稳定全身协调能力，闭环修正则确保长时间操作中全局位置与操作员保持精确对应。这一组合使得 CLONE 仅需 MR 头显的头部与手部追踪即可实现高保真全身遥操作，并成功完成如捡起地面物体等复杂长时任务（图 5、图 6）。



CLONE 系统围绕一个核心矛盾展开：如何仅凭混合现实头显提供的稀疏头部与手部追踪信号，驱动人形机器人产生自然协调的全身运动，并在长时间操作中保持精确的全局位置对齐。为此，系统构建了一条从数据策展到策略蒸馏再到闭环部署的完整流水线，其整体架构如 Figure 3 所示。

![[assets/figures/papers/paper_list_l1676_CLONE_Closed_Loop_Whole_Body_Humanoid_Teleoperation_for_Long_Horizon_Tas/figures/003_Figure_3.jpg]]
*Figure 3: The CLONE framework. (a) CLONED curates and augments retargeted AMASS [28] data through motion editing to introduce diverse humanoid motions and detailed hand movements. (b) A teacher policy is trained using privileged information, including full robot state and environmental context. (c) An MoE network serves as the student policy, distilled from the teacher to operate with real-world observations only. (d) For real-world deployment, we integrate LiDAR odometry to obtain real-time humanoid states, enabling closed-loop error correction during teleoperation*

**流水线由四个串行模块构成：**

1. **CLONED 数据集构建**（Figure 3a）。从 AMASS 运动捕捉数据库中筛选并重定向运动序列，通过运动编辑引入多样化的全身动作与精细手部姿态，形成约 345 个动作序列的训练语料。相比 OmniH2O 所使用的 8000+ 序列，CLONED 的数据量仅为其约 20%，但经过针对性筛选与增强，覆盖了行走、下蹲、跳跃、挥手等多类运动模式。

2. **教师策略训练**（Figure 3b）。教师策略基于标准 MLP 架构，接收特权信息——完整的机器人本体状态与环境上下文——通过强化学习训练，学习从参考运动到关节控制指令的映射。特权信息的引入使得教师策略能够在仿真中充分探索运动空间，无需受限于真实传感器的稀疏性与噪声。

3. **学生策略蒸馏**（Figure 3c）。学生策略采用混合专家（MoE）网络替代单一 MLP，其输入严格限定为真实部署时可获取的观测：IMU 数据、里程计估计以及参考运动序列。通过行为蒸馏，学生策略从教师策略中继承全身协调能力，同时 MoE 架构中的多个专家网络对不同运动类型进行专业化处理，解决了单一策略难以同时驾驭行走、下蹲、跳跃等多样化运动的瓶颈。

4. **闭环误差修正部署**（Figure 3d）。在真实机器人运行时，系统通过 LiDAR 里程计获取人形机器人的实时全局位置，并利用 Apple Vision Pro 的空间锚点追踪操作者的头部位置。学生策略直接接收两者之间的全局位置差作为输入，从而生成能够系统性消除位置漂移的控制动作，形成从感知到执行的闭合反馈回路。

**关键设计决策与因果机制：**

- **MoE 架构的选择**直接回应了“单一策略难以协调多样性运动”这一瓶颈。每个 MoE 层的输出由路由权重加权的 Top-k 专家输出之和构成：$f = \sum_{i}^{k} w_{i} \cdot E_{i}(\cdot)$。为防止策略坍缩至少数专家，训练中引入负载均衡损失 $\mathcal{L}_{balance}$（见 Equation 1）。消融实验表明，3 层 4 专家的配置在运动跟踪精度与计算效率之间取得最优平衡（Table A3）；移除 MoE 架构（CLONE†）导致 MPKPE 从 87.84 mm 恶化至 113.97 mm（Table 1）。

- **闭环误差修正**解决了开环遥操作中位置漂移累积的根本缺陷。学生策略显式消费人形机器人与操作者之间的全局位置差，使其能够生成补偿动作。为让策略在训练中适应真实 LiDAR 里程计的噪声特性，系统引入了速度相关的随机微分方程噪声模型（Equation 2），噪声强度与头部运动速度成正比。这一设计使 CLONE 在真实世界直行跟踪中实现了 5.1 cm 的平均全局位置误差（Figure 4），而开环系统则因漂移累积导致任务失败。

- **教师-学生蒸馏范式**弥合了仿真特权信息与真实稀疏观测之间的鸿沟。教师策略在信息完备的仿真环境中学习全身协调，学生策略则通过模仿教师的行为分布，将这一能力迁移到仅依赖真实传感器输入的条件下。这种设计使得 CLONE 仅需 MR 头显的头部与手部追踪即可生成包含下肢步态在内的全身运动，无需额外的足部传感器或外部动捕系统。

**输入输出流：** 系统输入端为操作者的头部 6D 位姿与双手 6D 位姿（来自 Apple Vision Pro），以及人形机器人的本体感知（IMU、关节编码器）和 LiDAR 里程计估计。输出端为人形机器人全身关节的目标位置指令，驱动 Unitree G1 执行协调的全身运动。闭环反馈回路将 LiDAR 里程计与 AVP 空间锚点提供的全局位置差实时注入策略输入，形成持续的漂移补偿。

### 补充图表

![[assets/figures/papers/paper_list_l1676_CLONE_Closed_Loop_Whole_Body_Humanoid_Teleoperation_for_Long_Horizon_Tas/figures/001_Figure_1.jpg]]
*Figure 1: CLONE employs an MoE-based policy with closed-loop error correction for humanoid teleoperation, enabling precise whole-body coordination and long-horizon task execution*



### 3.1 教师-学生策略蒸馏框架

CLONE 采用教师-学生策略蒸馏范式，将稀疏操作者输入映射为协调的全身运动指令。教师策略在仿真环境中利用特权信息（完整机器人状态、环境上下文）通过 PPO 训练获得高性能运动控制能力；学生策略则仅使用真实部署时可获取的观测（IMU 数据、LiDAR 里程计、参考运动序列），通过行为克隆从教师策略中蒸馏知识。这种设计保证了学生策略在仅依赖 MR 头显提供的头部与手部追踪信息时，仍能生成自然的下半身运动与全身协调。

### 3.2 混合专家（MoE）策略架构

为在单一策略中统一处理行走、下蹲、跳跃等多种运动模式，CLONE 将学生策略构建为混合专家网络。MoE 层由 $N$ 个独立的前馈专家网络 $E_i(\cdot)$ 和一个可学习的路由网络组成。对于每层输入，路由网络计算各专家的选择概率，并激活 Top-$k$ 个专家，MoE 层输出为：

$$f = \sum_{i}^{k} w_{i} \cdot E_{i}(\cdot)$$

其中 $w_i$ 为路由权重，$k$ 为激活专家数。不同专家可自发专精于不同运动类型（如专家 A 倾向处理站立姿态，专家 B 倾向处理下蹲动作），使单一策略具备处理多样化运动的能力。

为防止训练中策略坍缩至少数专家，引入专家负载均衡损失：

$$\mathcal{L}_{balance} = \sum_{l=1}^{L} \sum_{e=1}^{N} \left[\mathrm{max}\left(p_{e} - \frac{1 + \epsilon}{N}, 0\right) + \mathrm{min}\left(\frac{1 - \epsilon}{N} - p_{e}, 0\right)\right]$$

其中 $L$ 为 MoE 层数，$N$ 为每层专家数，$p_e$ 为专家 $e$ 在一批数据中的平均选择概率，$\epsilon$ 为容忍偏差。该损失鼓励专家被均匀使用，提升模型容量利用率。消融实验（Table A3, Figure A2-A6）表明，3 层 MoE 配置 4 个专家（$L=3, N=4$）取得最优整体性能；仅 1 层时参数容量不足，8 专家则引入冗余计算且无显著收益。

### 3.3 闭环误差修正机制

开环遥操作因缺乏位置反馈，长时间运行中会累积显著漂移。CLONE 引入闭环误差修正：部署时，LiDAR 里程计实时估计人形机器人的全局位置 $\hat{\mathbf{p}}$，Apple Vision Pro（AVP）提供操作者的全局位置 $\mathbf{p}$，学生策略直接消费全局位置差 $\mathbf{p} - \hat{\mathbf{p}}$ 作为输入，从而生成系统性减少位置漂移的动作指令。该机制使 CLONE 在真实世界直行跟踪中实现 5.1 cm 平均全局位置误差，弯曲路径下位移误差约 20 cm、旋转漂移约 2°（Figure 4, Section 4）。

### 3.4 LiDAR 里程计噪声建模

为使仿真训练的策略能迁移至真实 LiDAR 里程计的噪声特性，CLONE 在训练阶段引入速度依赖的随机微分方程（SDE）噪声模型，对头部位置进行扰动：

$$\mathrm{d} \vec{P}_{\mathrm{head}} = \dot{\vec{p}}_{\mathrm{head}} \mathrm{d} t + \left(\frac{\| \dot{\vec{p}}_{\mathrm{head}} \|}{c_{\mathrm{vel}}} + c_{\mathrm{min}}\right) \mathrm{d} \vec{W}$$

其中 $\dot{\vec{p}}_{\mathrm{head}}$ 为头部运动速度，$c_{\mathrm{vel}}$ 和 $c_{\mathrm{min}}$ 分别为速度缩放常数与最小噪声水平，$\mathrm{d}\vec{W}$ 为维纳过程。噪声强度与头部运动速度成正比，符合真实 LiDAR 里程计在快速运动中误差增大的特性。该域随机化使策略在仿真中即学会对位置估计误差的鲁棒性。

### 3.5 手部朝向跟踪误差

为精确评估手部姿态跟踪质量，CLONE 定义手朝向跟踪误差为参照四元数 $\hat{\mathbf{q}}$ 与机器人四元数 $\mathbf{q}$ 的点积平方偏差：

$$E_{\mathrm{hand}} = 1 - \langle \hat{\mathbf{q}}, \mathbf{q} \rangle^{2}$$

该指标对四元数符号对称性具有不变性，能准确反映手部旋转跟踪的保真度。在 CLONED 数据集上，CLONE 的手朝向误差为 3.61，显著优于 MLP 架构变体 CLONE†（4.73）和使用 OmniH2O 数据训练的变体 CLONE∗（4.61）（Table 1）。



## 实验与关键发现

### 主实验结果

CLONE 在仿真与真实世界两个维度均展现出显著优势，核心指标对比如下。

**仿真运动跟踪精度（CLONED 数据集）**

Table 1 系统对比了 CLONE 与两个消融变体在四项关键指标上的表现。CLONE 在所有指标上均取得最优：

![[assets/figures/papers/paper_list_l1676_CLONE_Closed_Loop_Whole_Body_Humanoid_Teleoperation_for_Long_Horizon_Tas/figures/007_Table_1.jpg]]
*Table 1: Motion tracking evaluation on CLONED dataset. Comparison of CLONE against ablations: CLONE † uses an MLP instead of MoE architecture, while CLONE ∗ trains on OmniH2O data instead of CLONED*

- **平均关键体位置误差（MPKPE）**：87.84 mm，相比使用单一 MLP 架构的 CLONE†（113.97 mm）降低 26.13 mm（约 22.9%），相比使用 OmniH2O 数据训练的 CLONE∗（102.20 mm）降低 14.36 mm。
- **根相对 MPKPE（R-MPKPE）**：33.30 mm，CLONE† 为 35.55 mm，CLONE∗ 为 41.07 mm。该指标剥离全局位置漂移，聚焦局部姿态跟踪质量，CLONE 的优势表明其全身协调能力更强。
- **平均关节速度误差**：227.17 mm/s，CLONE† 为 245.11 mm/s，CLONE∗ 为 309.65 mm/s。速度误差的大幅降低说明 CLONE 对运动动态的复现更为准确。
- **手部朝向跟踪误差**：3.61，CLONE† 为 4.73，CLONE∗ 为 4.61。该指标通过 $E_{\mathrm{hand}} = 1 - \langle \hat{\mathbf{q}}, \mathbf{q} \rangle^{2}$ 计算，数值越低表示手部姿态跟踪越精确。

值得注意的是，CLONE 仅使用约 20% 的训练动作数据量（345 个序列 vs. OmniH2O 的 8k+ 序列），即在全部指标上超越 CLONE∗，排除了数据规模优势的干扰，凸显 CLONED 数据集的精心筛选与 MoE 架构的协同效应。

**真实世界全局位置跟踪**

Figure 4 展示了 CLONE 在真实环境中的闭环位置跟踪性能。在长达 8.9 m 的直行路径上，CLONE 实现 **5.1 cm 的平均全局位置跟踪误差**，最大偏差仅为 12.0 cm。作为对比，开环遥操作系统因缺乏实时位置反馈，漂移会迅速累积，通常无法完成此类长距离任务。在弯曲路径跟踪中，CLONE 的平均平移误差约为 20 cm，平均旋转漂移约为 2°，闭环修正有效抑制了转角与位移的累积误差。

![[assets/figures/papers/paper_list_l1676_CLONE_Closed_Loop_Whole_Body_Humanoid_Teleoperation_for_Long_Horizon_Tas/figures/004_Figure_4.jpg]]
*Figure 4: Global position tracking accuracy in real-world experiments. CLONE achieves mean tracking errors of 5.1cm across distances up to 8.9m, demonstrating effective closed-loop error correction in extended teleoperation*

**定性全身协调能力**

Figure 5 展示了 CLONE 在 Unitree G1 人形机器人上成功跟踪多种运动技能，包括挥手、下蹲和跳跃，验证了 MoE 策略对多样化运动模式的统一协调能力。Figure 6 进一步展示了长时遥操作序列：机器人在复杂导航中同时准确跟踪操作者的局部姿态与全局位移，全程保持低漂移，证明了闭环修正在实际任务中的鲁棒性。

![[assets/figures/papers/paper_list_l1676_CLONE_Closed_Loop_Whole_Body_Humanoid_Teleoperation_for_Long_Horizon_Tas/figures/005_Figure_5.jpg]]
*Figure 5: Whole-body motion tracking on Unitree G1. CLONE successfully tracks diverse skills including (a) waving, (b)(d) squatting, and (c)jumping, showcasing comprehensive whole-body coordination capabilities*

![[assets/figures/papers/paper_list_l1676_CLONE_Closed_Loop_Whole_Body_Humanoid_Teleoperation_for_Long_Horizon_Tas/figures/006_Figure_6.jpg]]
*Figure 6: Long-horizon teleoperation. The humanoid accurately tracks both the operator’s local pose and global translation throughout a complex navigation sequence, demonstrating robust performance*

### 消融实验

**MoE 架构的关键作用**

Table 1 中的 CLONE† 消融直接验证了 MoE 架构的贡献：将 MoE 替换为单一 MLP 后，MPKPE 从 87.84 mm 恶化至 113.97 mm，手部朝向误差从 3.61 升至 4.73。Table A3 进一步对 MoE 配置进行细粒度消融：

![[assets/figures/papers/paper_list_l1676_CLONE_Closed_Loop_Whole_Body_Humanoid_Teleoperation_for_Long_Horizon_Tas/figures/011_Table.jpg]]
*Table: A3: Ablation study on history length and architecture components*

- **层数**：3 层 MoE（4 专家）取得最佳整体性能。仅 1 层时参数容量不足，性能显著下降；增加至 4 层或 5 层未带来额外增益。
- **专家数**：4 专家配置最优。8 专家虽增加模型容量，但引入冗余计算，性能未见提升。Figure A2-A6 可视化了不同配置下的专家激活模式，显示 3 层 4 专家的配置下各专家激活分布最为均衡。

![[assets/figures/papers/paper_list_l1676_CLONE_Closed_Loop_Whole_Body_Humanoid_Teleoperation_for_Long_Horizon_Tas/figures/012_Figure.jpg]]
*Figure: A2: The activation status of each expert. Figure A3: Experts activation when N = 8 Figure A4: Experts activation when L = 4*

**历史窗口长度**

Table A3(a) 表明，历史窗口长度为 25 帧时性能最优。过短（5 帧）导致时序信息不足，过长（50 帧）则引入无关历史，干扰当前决策。

**CLONED 数据集的贡献**

Figure 7 按不同姿态高度（从站立到深蹲）对比了 CLONE、CLONE∗ 和 CLONE† 的运动跟踪性能。CLONE 在所有姿态高度下均保持最低误差，尤其在下蹲深度增加时优势更为明显。Figure A1 的定性对比显示，CLONE∗ 在下蹲动作中出现明显的姿态偏差，而 CLONE 保持了与参考运动的高度一致性。这验证了 CLONED 数据集中针对人形机器人精心筛选与增强的动作序列对训练质量的决定性影响。

![[assets/figures/papers/paper_list_l1676_CLONE_Closed_Loop_Whole_Body_Humanoid_Teleoperation_for_Long_Horizon_Tas/figures/008_Figure_7.jpg]]
*Figure 7: Motion tracking performance across stance heights. Comparison between CLONE (blue solid), CLONE ∗ (green dashed), and*

![[assets/figures/papers/paper_list_l1676_CLONE_Closed_Loop_Whole_Body_Humanoid_Teleoperation_for_Long_Horizon_Tas/figures/010_Figure.jpg]]
*Figure: A1: Qualitative Results of CLONE and CLONE *. (a) and (b) show the “crouch” tracking results of CLONE *, while (c) and (d) present the results of CLONE*

### 失败模式与局限性

尽管 CLONE 在整体指标上表现优异，分析中仍揭示了若干值得关注的失效边界：

1. **高动态运动的精度折衷**：在跳跃等高动态运动中，CLONE 的 MPKPE 指标有所上升。这反映了在追求局部关节精度与全局位置稳定性之间存在固有张力——闭环修正优先保证全局不漂移，可能在瞬时高加速阶段牺牲局部跟踪精度。

2. **稀疏输入的固有局限**：系统仅依赖 MR 头显的头部与手部追踪，缺乏足部触地传感器等精细信息。在非结构地形下，这种输入稀疏性可能限制极端稳定性——例如，无法感知地面起伏时，机器人可能以不恰当的足部姿态着地。

3. **LiDAR 退化环境的脆弱性**：闭环误差修正依赖 LiDAR 里程计与 AVP 空间锚点。在空旷场景或强遮挡环境中，LiDAR 特征退化可能导致里程计精度下降，进而削弱漂移补偿能力。当前论文未报告此类退化场景下的定量性能。

4. **数据集规模与覆盖度**：CLONED 虽经精心筛选，但仅包含 345 个动作序列，可能无法覆盖所有复杂交互场景（如上下楼梯、开门等）。扩展数据集以支持更广泛的技能泛化仍是开放问题。

5. **机器人形态依赖性**：当前学生策略专为 Unitree G1 人形机器人训练，迁移至其他形态的机器人可能需要重新训练或适配，限制了方法的即插即用性。

### 关键图表结论速览

| 图表 | 核心结论 |
|------|----------|
| Table 1 | CLONE 在 MPKPE、R-MPKPE、速度误差、手朝向误差四项指标上全面优于 MLP 架构和 OmniH2O 数据训练的消融变体 |
| Figure 4 | 真实世界直行跟踪平均误差 5.1 cm，闭环修正有效消除开环系统的累积漂移 |
| Figure 5 | MoE 策略成功协调挥手、下蹲、跳跃等多种运动技能 |
| Figure 6 | 长时复杂导航中保持全身姿态与全局位置的双重跟踪精度 |
| Figure 7 | CLONE 在站立至深蹲的全姿态范围内均优于消融变体，低姿态下优势更显著 |
| Table A3 | 3 层 4 专家、25 帧历史窗口为最优配置；MoE 架构和 CLONED 数据集缺一不可 |

### 补充图表

![[assets/figures/papers/paper_list_l1676_CLONE_Closed_Loop_Whole_Body_Humanoid_Teleoperation_for_Long_Horizon_Tas/figures/013_Figure.jpg]]
*Figure: A5: Experts activation when L = 5 Figure A6: Experts activation when L = 1*

![[assets/figures/papers/paper_list_l1676_CLONE_Closed_Loop_Whole_Body_Humanoid_Teleoperation_for_Long_Horizon_Tas/figures/009_Table.jpg]]
*Table: A1: Reward functions. The details of the primary reward function used in our training process. Table A2: Domain Randomization. The details of the primary domain randomization used in our training process*



## 定位与知识库关联

### 核心问题与因果杠杆

现有人形机器人遥操作系统普遍将上半身与下半身的控制解耦，以简化稳定性问题，但代价是牺牲了自然的全身协调能力。同时，主流方案采用开环控制范式，缺乏对机器人实际位置与操作者意图之间偏差的实时感知与修正，导致在长时间操作过程中累积显著的位置漂移，最终使复杂长时任务无法完成。

CLONE 针对上述瓶颈，引入两个因果杠杆：

1. **混合专家（Mixture-of-Experts, MoE）策略架构**：通过多个专家网络对不同运动类型（行走、下蹲、跳跃等）进行专业化处理，以单一策略统一学习多样化的全身运动技能，解决了单一 MLP 架构难以协调异质性运动模式的问题。
2. **闭环误差修正机制**：将 LiDAR 里程计与空间锚点（AVP 追踪）提供的全局位置反馈引入策略输入，使机器人能够实时感知并补偿累积漂移，从而仅依赖 MR 头显的头部与手部追踪即可实现高保真、低漂移的全身遥操作。

### 与基线工作的关系

CLONE 直接对标的是基于大规模运动数据集训练的全身遥操作系统 **OmniH2O**（基线角色：MLP 架构 + 开环控制 + OmniH2O 数据集）。论文通过消融变体系统性地解耦了各设计要素的贡献：

- **CLONE†**：将 MoE 架构替换为单一 MLP，其余训练范式与 CLONE 完全一致（均采用教师-学生蒸馏 + PPO 训练）。该变体在 CLONED 数据集上各项运动跟踪指标均显著劣于 CLONE（MPKPE 从 87.84 mm 升至 113.97 mm，手部朝向误差从 3.61 升至 4.73），直接验证了 MoE 架构对多样化运动协调的关键作用。
- **CLONE\***：保留 MoE 架构，但使用 OmniH2O 数据集（8k+ 动作序列）替代 CLONED（345 个动作序列）进行训练。尽管数据量约为 CLONED 的 5 倍，CLONE\* 在所有指标上仍全面落后于 CLONE（MPKPE 102.20 vs. 87.84 mm，速度误差 309.65 vs. 227.17 mm/s），表明精心筛选与增强的 CLONED 数据集在数据效率和质量上具有决定性优势。

这一对比排除了数据规模优势的干扰：CLONE 仅使用约 20% 的训练动作数据量，就在所有运动跟踪指标上超越了基于更大规模数据训练的变体。

### 方法适用边界

**适用场景**：
- 需要长时间、低漂移全身遥操作的复杂任务，如导航中捡起地面物体、穿越障碍物序列等。
- 操作者仅能提供稀疏输入（头部 + 双手位姿）的场景，CLONE 可自动补全全身运动。
- 结构化或半结构化环境中，LiDAR 里程计与空间锚点可稳定工作。

**不适用或性能受限场景**：
- **高动态运动**：在跳跃等动作中，CLONE 的 MPKPE 指标有所上升，反映出局部关节精度与全局位置稳定性之间存在折衷。系统在追求闭环位置修正时，可能牺牲部分瞬时关节跟踪精度。
- **非结构地形**：系统仅依赖头部和双手的稀疏输入，缺乏足部触地传感器等精细接触信息，在极端不平整或松软地形下的稳定性受限。
- **LiDAR 退化环境**：闭环误差修正依赖 LiDAR 里程计，在空旷场景（缺乏几何特征）、强遮挡或低纹理环境中，里程计精度下降将直接影响位置修正的可靠性。
- **跨形态迁移**：当前学生策略专为 Unitree G1 人形机器人训练，迁移至其他形态（不同自由度配置、质量分布）的机器人平台需要重新训练或适配。

### 局限与开放问题

**已识别的局限**：
1. CLONED 数据集虽经精心筛选与增强，但规模较小（345 个动作序列），可能无法覆盖所有复杂交互场景（如上下楼梯、开门、推拉重物等）。
2. 闭环修正机制对 LiDAR 和空间锚点的依赖，使其在传感器退化场景中的鲁棒性存疑。
3. 跳跃等高动态动作的跟踪精度仍有提升空间，当前设计在全局稳定与局部精度之间存在权衡。

**开放问题**：
1. 能否在不增加额外输入设备的前提下，进一步提升跳跃、跑步等高动态动作的跟踪精度？可能的方向包括改进 MoE 专家的动态路由策略，或在训练中引入更精细的时序约束。
2. 如何扩展 CLONED 数据集，以支持训练一次即可在多类型人形机器人上泛化的通用全身控制策略？这可能需要引入形态条件化的策略表示。
3. 在强遮挡或低纹理环境中，如何提升 LiDAR 里程计的鲁棒性？多传感器融合（如视觉-惯性-激光联合优化）或基于学习的里程计去噪可能是可行的扩展路径。
4. 基于 MoE 的策略是否能够自发涌现出更高级的全身协调行为（如上下楼梯、开门等），而无需显式设计奖励函数或运动先验？这涉及对 MoE 专家功能分化的深入理解与引导。



## 原文 PDF

![[paperPDFs/arxiv_2025/CLONE_Closed_Loop_Whole_Body_Humanoid_Teleoperation_for_Long_Horizon_Tasks.pdf]]
