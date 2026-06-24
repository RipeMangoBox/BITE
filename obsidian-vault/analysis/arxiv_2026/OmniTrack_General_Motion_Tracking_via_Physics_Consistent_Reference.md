---
title: "OmniTrack: General Motion Tracking via Physics-Consistent Reference"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/OmniTrack_General_Motion_Tracking_via_Physics_Consistent_Reference.pdf
aliases:
- OmniTrack
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过两阶段训练框架显式解耦物理可行性与运动跟踪：第一阶段在模拟中利用完全特权信息生成物理一致的参考运动，第二阶段在部分可观测条件下训练通用控制策略，使控制器无需处理不可行目标。
primary_logic: 将物理可行性修复负担从控制策略转移至参考生成阶段，确保参考运动动力学自洽后，跟踪策略可专注于泛化与鲁棒性，消除阻碍通用学习的内在权衡。
claims:
- "物理一致性参考完全消除穿透与漂浮伪影，改善运动平滑度（TABLE I: Penetration 0.0%, Floating 0.0%, Smoothness 31.8 vs 33.7）"
- 使用物理参考训练的策略在LAFAN1全数据集上保持92.57%成功率，而原始参考仅88.18%，且MPJPE更优（TABLE A.8）
- OMNITRACK在困难高动态子集上成功率达84.81%，大幅超越BeyondMimic (70.04%)、ExBody2 (58.93%)和OmniH2O (48.32%)（TABLE III）
- 在真实Unitree G1机器人上实现一小时连续户外跟踪和多种动态技能（如侧手翻），验证sim-to-real迁移鲁棒性（Fig. 5, Fig. A.7）
---

# OmniTrack: General Motion Tracking via Physics-Consistent Reference

> [!tip] 核心洞察
> 将物理可行性修复负担从控制策略转移至参考生成阶段，确保参考运动动力学自洽后，跟踪策略可专注于泛化与鲁棒性，消除阻碍通用学习的内在权衡。

| 字段 | 内容 |
|------|------|
| 中文题名 | OmniTrack：通过物理一致性参考实现通用运动跟踪 |
| 英文题名 | OmniTrack: General Motion Tracking via Physics-Consistent Reference |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2602.23832) · [Project](https://omnitrack-humanoid.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | OMNITRACK |
| Dataset | LAFAN1 Seen Motions, LAFAN1 Hard Motions, LAFAN1 Unseen Motions, High-Dynamic Subset |

> [!tip] 效果简介
> - LAFAN1 Seen Motions 上，SR (%) 96.13 vs 92.46 (Dagger) (+3.67)。
> - LAFAN1 Hard Motions 上，SR (%) 84.81 vs 67.40 (Dagger) (+17.41)。
> - LAFAN1 Unseen Motions 上，SR (%) 96.88 vs 96.56 (Dagger) (+0.32)。

## 概述

类人机器人通用运动跟踪的核心瓶颈在于：从人体运动捕捉数据重定向得到的参考运动，往往包含穿透、漂浮、足部滑动等物理不可行伪影（Fig. 2）。这些伪影迫使控制策略在跟踪保真度与物理可行性之间做出根本性权衡——既要忠实复现目标姿态，又要维持机器人平衡与接触约束，导致现有方法难以稳定学习覆盖多样化运动类别、长时间跨度的通用控制策略。

OMNITRACK 的核心洞察是：**将物理可行性修复的负担从控制策略前移至参考生成阶段**。通过显式解耦物理可行性与运动跟踪，使参考运动动力学自洽后，跟踪策略可以专注于泛化与鲁棒性，从而消除阻碍通用学习的内在冲突。

为此，OMNITRACK 采用两阶段训练框架（Fig. 3）：**阶段I** 在仿真中利用完全特权信息，通过强化学习将原始重定向运动转化为无穿透、无漂浮的物理一致性参考轨迹；**阶段II** 在部分可观测和域随机化条件下，训练通用控制策略鲁棒跟踪这些自洽参考运动。两阶段均建模为马尔可夫决策过程，使用 PPO 优化，总奖励由跟踪项 $r_{\mathrm{track}}$ 与正则项 $r_{\mathrm{reg}}$ 构成。

实验表明，物理一致性参考完全消除了穿透与漂浮伪影，并改善了运动平滑度（TABLE I: Penetration 0.0%, Floating 0.0%, Smoothness 31.8 vs 33.7）。使用物理参考训练的策略在全量 LAFAN1 数据集上保持 92.57% 成功率，而原始参考仅 88.18%，且 MPJPE 更优（TABLE A.8）。在困难高动态子集上，OMNITRACK 成功率达 84.81%，大幅超越 **BeyondMimic** (Mehta et al., arXiv 2025) 的 70.04%、**ExBody2** (Tessler et al., arXiv 2024) 的 58.93% 和 **OmniH2O** (He et al., arXiv 2024) 的 48.32%（TABLE III）。在真实 Unitree G1 机器人上，OMNITRACK 实现了一小时连续户外跟踪和侧手翻等高动态技能，验证了 sim-to-real 迁移的鲁棒性（Fig. 5, Fig. A.7）。

在方法谱系上，OMNITRACK 与现有工作的关键差异在于物理可行性处理方式：**Dagger**（Ross et al., AISTATS 2011）、**AAC**（Pinto et al., arXiv 2017）等基线在单一策略中同时处理跟踪与物理可行性，而 OMNITRACK 将两者解耦为独立的生成与跟踪阶段。这一设计使其在通用运动覆盖、跟踪精度和真实世界鲁棒性上均取得显著优势。

## 背景与动机

### 人形机器人运动跟踪的核心瓶颈

人形机器人运动跟踪旨在使机器人复现多样化的人类运动，涵盖平衡控制、高动态动作和接触丰富的交互行为。现有方法通常将人类运动数据通过运动学重定向映射到机器人模型上，生成参考轨迹，再由控制策略进行跟踪。然而，这一流程面临一个根本性瓶颈：**重定向生成的人体运动参考中普遍存在物理不可行伪影**，如足部穿透地面、身体漂浮、质心运动不一致和足部滑移等（Fig. 2）。这些伪影源于人类运动捕捉数据与机器人动力学约束之间的不匹配——人类运动在运动学层面看似合理，但映射到具有特定质量分布、关节限位和驱动能力的机器人上时，往往违背物理定律。

这一瓶颈引发了一个内在权衡：控制策略在部分可观测条件下，既要实现高保真运动跟踪，又要自行补偿参考运动中的物理不可行性。当运动数据集规模扩大、动作难度增加时，这种双重负担导致训练不稳定、跟踪精度下降，策略难以同时实现通用性和鲁棒性。实验证据表明，使用原始重定向参考训练的策略在LAFAN1全数据集上成功率仅为88.18%，而高动态子集上的表现更是显著恶化（TABLE A.8, TABLE III）。

### 现有方法的局限

当前主流方法可归纳为两类范式。第一类采用**端到端学习**，在单一阶段内同时处理跟踪与物理可行性，如**Dagger**（Ross et al., AISTATS 2011）及其变体通过模仿学习蒸馏特权信息，**AAC**（Pinto et al., arXiv 2017）利用非对称Actor-Critic架构。这些方法将物理可行性修复的负担完全置于控制策略之上，在多样化运动场景下难以扩展。第二类方法如**OmniH2O**（He et al., arXiv 2024）、**ExBody2**（Tessler et al., arXiv 2024）和**BeyondMimic**（Mehta et al., arXiv 2025）引入了更复杂的策略架构或分层强化学习，但本质上仍未改变参考运动本身包含物理伪影这一根本问题。在高动态子集上，BeyondMimic的成功率仅为70.04%，ExBody2为58.93%，OmniH2O更是低至48.32%（TABLE III），表明现有范式在困难动作上的泛化能力严重受限。

### 本文动机与核心洞察

本文的核心洞察是：**将物理可行性修复的负担从控制策略转移至参考生成阶段，是消除通用学习内在权衡的关键**。如果参考运动本身是动力学自洽的——即无穿透、无漂浮、满足接触约束和质心动力学——那么控制策略就无需在跟踪过程中同时补偿物理不可行性，从而可以专注于泛化与鲁棒性。基于这一洞察，OMNITRACK提出了一种**两阶段解耦框架**：第一阶段在模拟中利用完全特权信息生成物理一致的参考运动，第二阶段在部分可观测条件下训练通用控制策略仅负责跟踪。这种结构性解耦从根本上消除了物理不可行目标对策略学习的干扰，为大规模、长时间跨度的通用运动跟踪奠定了基础。

实验表明，物理一致性参考完全消除了穿透和漂浮伪影，运动平滑度从33.7改善至31.8（TABLE I），且使用物理参考训练的策略在LAFAN1全数据集上保持92.57%成功率，显著优于原始参考的88.18%（TABLE A.8）。在真实Unitree G1机器人上，OMNITRACK实现了长达一小时的连续户外跟踪和侧手翻等高动态技能（Fig. 5, Fig. A.7），验证了该框架的sim-to-real迁移鲁棒性。

## 核心创新

OMNITRACK 的核心创新在于**将物理可行性修复的负担从控制策略转移至参考生成阶段**，通过一个两阶段训练框架显式解耦“物理可行性”与“通用运动跟踪”这两个相互冲突的目标。

### 瓶颈洞察：物理不可行伪影导致的根本冲突

现有方法通常采用单一策略，在部分可观测条件下同时处理运动跟踪与物理可行性。然而，从人体运动捕捉数据经重定向得到的原始参考运动，普遍包含**地面穿透、足部漂浮、质心运动不一致**等物理不可行伪影（Fig. 2）。当控制策略被迫跟踪这些不可行目标时，会产生一个根本性的冲突：提高跟踪保真度会破坏机器人稳定性，而维持稳定则意味着牺牲跟踪精度。这一内在权衡使得现有策略难以在多样化、长时间跨度的运动上实现稳定的通用学习。

### 关键机制：两阶段解耦框架

OMNITRACK 通过结构化解耦消除了上述冲突（Fig. 3）：

- **阶段 I：物理运动生成（Physical Motion Generation）**。在仿真环境中利用完全特权信息（包括全局位姿、精确接触力、外部扰动等），训练一个通用策略将原始重定向运动转化为物理一致的参考轨迹。该策略仅作为运动生成模块使用，其输出消除了穿透与漂浮伪影，并确保动力学自洽（TABLE I：Penetration 0.0%，Floating 0.0%，Smoothness 31.8 vs 33.7）。

- **阶段 II：通用运动跟踪（General Motion Tracking）**。在部分可观测条件（仅本体感知）和域随机化下，训练一个通用控制策略跟踪阶段 I 生成的物理一致性参考运动。由于参考运动已具备物理可行性，该策略无需再补偿不可行目标，可专注于泛化与鲁棒性。

### 与基线方法的核心差异

| 维度 | 现有基线 | OMNITRACK |
|------|---------|-----------|
| **物理可行性处理** | 单一策略在部分观测下同时处理跟踪与可行性 | 两阶段解耦：阶段 I 利用特权信息修复，阶段 II 仅负责跟踪 |
| **训练参考质量** | 包含穿透、漂浮等物理伪影的原始重定向运动 | 无穿透/漂浮、动力学自洽的物理一致性运动 |
| **策略优化目标** | 跟踪精度与物理可行性之间的折衷 | 阶段 II 专注于跟踪精度，无内在冲突 |

### 创新效果验证

这一结构化解耦带来了可量化的性能提升。在 LAFAN1 数据集上，使用物理一致性参考训练的策略在全数据集上保持 **92.57%** 成功率，而使用原始参考仅 **88.18%**（TABLE A.8）。在高动态困难子集上，OMNITRACK 成功率达 **84.81%**，大幅超越 **BeyondMimic**（Mehta et al., arXiv 2025）的 70.04%、**ExBody2**（Tessler et al., arXiv 2024）的 58.93% 和 **OmniH2O**（He et al., arXiv 2024）的 48.32%（TABLE III）。在真实 Unitree G1 机器人上，该框架实现了长达一小时的连续户外跟踪及侧手翻等高动态技能，验证了 sim-to-real 迁移的鲁棒性（Fig. 5, Fig. A.7）。

## 整体框架

OMNITRACK 提出一种**两阶段学习框架**，其核心设计动机在于显式解耦物理可行性与通用运动跟踪之间的根本冲突。原始重定向人体运动参考中普遍存在穿透、漂浮、足部滑移等物理不可行伪影（Fig. 2），这些伪影迫使控制策略在跟踪精度与机器人稳定性之间进行内在权衡，严重阻碍了大规模、多样化运动数据上的稳定学习。OMNITRACK 的关键洞察是：**将物理可行性修复的负担从控制策略转移至参考生成阶段**，使跟踪策略面对的是动力学自洽的目标运动，从而可以专注于泛化与鲁棒性。

框架的两个阶段均被形式化为马尔可夫决策过程（MDP），并使用 PPO 进行优化。

### 阶段 I：物理运动生成（Physical Motion Generation）

该阶段在仿真环境中，利用完全特权信息（包括全局位置、速度、接触力等仿真器内部状态）训练一个通用策略，将原始的、物理不一致的重定向人体运动转换为**物理一致的参考运动**。

- **输入**：原始重定向运动（包含穿透、漂浮等伪影）及完整的仿真器特权观测。
- **处理**：策略在 IsaacLab 仿真器中执行 rollout，通过强化学习优化，使生成的运动满足物理约束（无穿透、无漂浮、接触力合理、质心运动一致）。
- **输出**：物理可行的机器人参考轨迹，其关节位置、身体朝向等动力学量自洽，可直接作为阶段 II 的跟踪目标。
- **效果**：经此阶段处理后，参考运动的穿透率与漂浮率降至 0.0%，运动平滑度显著改善（TABLE I: LAFAN1 平滑度 31.8 vs 原始 33.7），同时 MPJPE 因动力学一致性修正而适度增加（TABLE I: LAFAN1 上 21.0 mm vs 原始 0.0 mm，反映的是物理可行调整而非跟踪误差）。

### 阶段 II：通用运动跟踪（General Motion Tracking）

该阶段在部分可观测条件下训练通用控制策略，使其能够鲁棒地跟踪阶段 I 生成的物理一致性参考运动。

- **输入**：
  - **本体感知观测**：关节位置 $\pmb{q}_t$、关节速度 $\dot{\pmb{q}}_t$、根朝向 $\pmb{R}_t$、根角速度 $\omega_t$、上一时间步的动作 $\pmb{a}_{t-1}$。
  - **参考运动特征**：来自阶段 I 的物理一致性运动的目标关节位置、身体朝向等。
  - **域随机化**：施加于质量、摩擦力、关节阻尼、外部扰动等物理参数（TABLE A.6），以增强 sim-to-real 迁移鲁棒性。
- **处理**：策略以本体感知与参考运动特征为输入，输出关节目标位置，通过 PD 控制器驱动机器人。奖励函数由跟踪奖励 $r_{\mathrm{track}}$ 与正则化奖励 $r_{\mathrm{reg}}$ 组成（$r_t = r_{\mathrm{track}} + r_{\mathrm{reg}}$），其中跟踪奖励基于身体链节位置误差（$\exp \big( - \big( \frac{1}{|\mathcal{B}|} \sum_{b \in \mathcal{B}} \| \mathbf{p}_b^{\mathrm{ref}} - \mathbf{p}_b \|^2 \big) / 0.3^2 \big)$）和方向误差（$\exp \big( - \big( \frac{1}{|\mathcal{B}|} \sum_{b \in \mathcal{B}} \| \log( \phi_b^{\mathrm{ref}} \phi_b^{\top} ) \|^2 \big) / 0.4^2 \big)$）的指数惩罚项构成（TABLE A.5）。
- **输出**：可直接部署于真实机器人的关节目标指令，支持离线运动跟踪与在线遥操作两种模式。

### 两阶段解耦的关键优势

这一结构分离带来了三个层面的收益：

1. **消除内在权衡**：阶段 II 的策略不再需要同时处理跟踪精度与物理可行性修正，消除了导致训练不稳定和泛化受限的根本冲突。
2. **规模化学习**：使用物理一致性参考训练的策略在全 LAFAN1 数据集上保持 92.57% 成功率，而使用原始参考训练的策略下降至 88.18%（TABLE A.8），证明物理一致性参考是实现大规模通用运动学习的必要条件。
3. **困难运动泛化**：在高动态子集（包含翻转、侧手翻等）上，OMNITRACK 成功率达 84.81%，大幅超越现有最优方法 BeyondMimic（70.04%）、ExBody2（58.93%）和 OmniH2O（48.32%）（TABLE III），验证了解耦设计对极端动态技能的覆盖能力。

整体框架概览见 Fig. 3，真实机器人上的多样化运动技能与一小时连续户外跟踪验证了 sim-to-real 迁移的鲁棒性（Fig. 5, Fig. A.7）。

![[assets/figures/papers/paper_list_l60_https_arxiv_org_abs_2602_23832/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the OMNITRACK framework. Our method adopts a two-stage pipeline that first converts raw, physically inconsistent reference motions into physics-consistent motions in simulation, and then trains a general policy to robustly track these motions under realistic conditions. The resulting system supports both offline motion tracking and online teleoperation*

### 补充图表

![[assets/figures/papers/paper_list_l60_https_arxiv_org_abs_2602_23832/figures/001_Figure_1.jpg]]
*Figure 1: Capabilities of OMNITRACK in general motion tracking and real-time teleoperation. Leveraging physics-consistent reference motions, OmniTrack achieves general tracking across diverse motion categories, including balance control, highdynamic maneuvers, and contact-rich interactions. OmniTrack supports real-time teleoperation, enabling the execution of diverse human-style dynamic movements as well as interactive behaviors. These results demonstrate the generality of the framework in handling both physically demanding motions and unstructured motion commands*

## 核心模块与公式推导

OMNITRACK 将通用运动跟踪拆解为两个解耦的阶段，每个阶段均被形式化为马尔可夫决策过程（MDP），并使用 PPO 进行优化。这种解耦的核心动机在于：原始重定向的人体运动参考中存在穿透、漂浮、足部滑动等物理不可行伪影（Fig. 2），若直接在部分可观测条件下训练单一策略同时处理跟踪与物理可行性，将导致跟踪保真度与机器人稳定性之间的根本冲突。两阶段框架将物理可行性修复的负担从控制策略转移至参考生成阶段，使阶段 II 的策略无需处理不可行目标。

![[assets/figures/papers/paper_list_l60_https_arxiv_org_abs_2602_23832/figures/002_Figure_2.jpg]]
*Figure 2: Examples of physically infeasible artifacts in retargeted human motions (blue) compared with physically feasible robot motions (black/gray), including inconsistent center-of-mass motion, foot skating, floating, and ground penetration, which hinder stable humanoid control*

### 阶段 I：物理运动生成（Physical Motion Generation）

该阶段的目标是将原始重定向运动转换为物理一致的参考轨迹。在仿真环境中，利用**完全特权信息**（包括全局坐标、接触力、外部扰动等仿真状态）训练一个通用策略，使其在跟踪原始参考的同时满足物理约束。该策略仅作为运动生成模块使用——它通过仿真 rollout 产生物理可行的运动序列，而非直接部署到真实机器人。

这一设计的关键效果在 **TABLE I** 中得到量化验证：物理一致性参考完全消除了穿透（Penetration 0.0%）和漂浮（Floating 0.0%）伪影，同时改善了运动平滑度（LAFAN1 上 Smoothness 从 33.7 降至 31.8，数值越低越平滑）。代价是 MPJPE 从 18.8 mm 适度上升至 21.0 mm，这是动力学一致性修正的必然结果。

### 阶段 II：通用运动跟踪（General Motion Tracking）

阶段 II 在**部分可观测**条件下训练通用控制策略。观测空间被严格限制为机器人本体感知信息：

$$o_t^{\bar{p}} = (\mathbf{q}_t, \dot{\mathbf{q}}_t, \mathbf{R}_t, \omega_t, \mathbf{a}_{t-1})$$

其中 $\mathbf{q}_t$ 和 $\dot{\mathbf{q}}_t$ 为关节位置与速度，$\mathbf{R}_t$ 和 $\omega_t$ 为根链节方向与角速度，$\mathbf{a}_{t-1}$ 为上一时间步的动作。策略不访问任何全局状态或外部感知信息，仅依赖本体感知和阶段 I 生成的物理一致性参考轨迹进行跟踪。

为提升 sim-to-real 迁移鲁棒性，阶段 II 引入了域随机化（**TABLE A.6**），包括地面摩擦力、质量、质心位置、关节阻尼、电机力矩延迟、外部推力的随机扰动，以及自适应采样策略（**TABLE A.7**）来平衡不同难度运动片段的训练分布。

### 奖励函数

两个阶段共享相同的奖励结构，总奖励为跟踪奖励与正则化奖励之和：

$$r_t = r_{\mathrm{track}} + r_{\mathrm{reg}}$$

跟踪奖励的核心是身体链节位置误差的指数惩罚项（**TABLE A.5**）：

$$\exp \Big( - \big( \frac{1}{|\mathcal{B}|} \sum_{b \in \mathcal{B}} \| \mathbf{p}_b^{\mathrm{ref}} - \mathbf{p}_b \|^2 \big) / 0.3^2 \Big)$$

以及身体链节方向误差的指数惩罚项：

$$\exp \Big( - \big( \frac{1}{|\mathcal{B}|} \sum_{b \in \mathcal{B}} \| \log( \phi_b^{\mathrm{ref}} \phi_b^{\top} ) \|^2 \big) / 0.4^2 \Big)$$

其中 $\mathcal{B}$ 为身体链节集合，$\mathbf{p}_b$ 和 $\phi_b$ 分别为链节位置和方向四元数。正则化项 $r_{\mathrm{reg}}$ 包含关节力矩惩罚、动作平滑惩罚、关节加速度惩罚等，防止策略产生震荡或过大的控制信号。

### 关键设计决策

两阶段解耦的核心价值在 **TABLE A.8** 中得到系统性验证：使用物理一致性参考训练的策略在全 LAFAN1 数据集上保持 92.57% 成功率，而使用原始参考的策略降至 88.18%。**Fig. 4** 进一步揭示了这一差距随数据集规模扩大而加剧的趋势——物理一致性参考使训练在数据量增加时保持稳定收敛，而原始参考下的训练收益递减甚至退化。这证实了“将物理可行性修复从策略中剥离”是通用运动跟踪可扩展性的关键因果机制。

![[assets/figures/papers/paper_list_l60_https_arxiv_org_abs_2602_23832/figures/005_Figure_4.jpg]]
*Figure 4: Impact of physically plausible motions under varying dataset sizes. From left to right: mean reward and mean episode length during training, followed by success rate and tracking error (MPJPE) under different dataset sizes (1/8, 1/2, and full LAFAN1). Dark colors denote training with physically plausible motions, while light colors denote training with raw reference motions*

## 实验与分析

### 核心发现：物理一致性参考消除训练瓶颈

OMNITRACK的核心实验结论围绕一个关键因果机制展开：**当参考运动本身是物理自洽的，控制策略无需在跟踪精度与物理可行性之间进行内部权衡，从而释放出更强的泛化与鲁棒性。** 这一机制在两个层面得到验证。

**参考运动质量层面**，TABLE I 给出了物理一致性生成阶段（Stage I）的定量效果。原始重定向人体运动普遍存在穿透（Penetration > 0）与漂浮（Floating > 0）伪影，而经过Stage I处理后的物理一致性运动将两者完全归零（Penetration 0.0%，Floating 0.0%），同时运动平滑度指标显著改善（LAFAN1上Smoothness从33.7降至31.8，数值越低越平滑）。值得注意的是，这一物理修正带来了MPJPE的适度上升（LAFAN1上从0.0增至21.0 mm），这是动力学自洽校正的必然代价——原始运动与物理可行运动之间存在不可消除的偏差，但该偏差处于可控范围。

**控制策略训练层面**，Fig. 4 揭示了物理一致性参考对规模化学习的决定性影响。当训练数据从1/8 LAFAN1扩展至全数据集时，使用物理一致性参考训练的策略保持约92.6%的高成功率，而使用原始参考的策略从约91%下降至88.18%（TABLE A.8）。这一趋势在平均奖励和平均回合长度指标上同样显著（Fig. 4左两列），表明物理不可行目标在大规模多样化数据上会导致训练不稳定，而物理一致性参考从根本上消除了这一瓶颈。

### 主结果：训练管道对比与最先进方法比较

TABLE II 对比了不同训练管道在LAFAN1运动跟踪任务上的表现。OMNITRACK的两阶段管道在所有运动类别上均优于替代策略：

- **已见运动（Seen）**：成功率96.13%，对比Dagger（92.46%）、Dagger_hist（93.03%）、AAC（92.78%），提升3.67个百分点；MPJPE 37.61 mm，对比Dagger的40.79 mm，降低3.18 mm。
- **困难已见运动（Hard）**：成功率84.81%，对比Dagger（67.40%）提升17.41个百分点，对比AAC（73.41%）提升11.40个百分点，优势最为显著。
- **未见运动（Unseen）**：成功率96.88%，与Dagger（96.56%）接近，表明物理一致性参考未损害泛化能力，反而在MPJPE上略有优势（37.87 vs 40.29 mm）。

困难子集上的大幅领先验证了核心洞察：高动态运动（如翻转、侧手翻）中物理伪影最为严重，原始参考的不可行性迫使策略在跟踪精度与稳定性之间做出妥协，而OMNITRACK通过解耦消除了这一冲突。

TABLE III 将OMNITRACK与三类最先进方法进行对比，使用高动态子集作为统一测试基准：

| 方法 | 成功率 (%) | MPJPE (mm) |
|------|-----------|------------|
| **OMNITRACK** | **84.81** | **37.61** |
| BeyondMimic (Mehta et al., arXiv 2025) | 70.04 | 45.39 |
| ExBody2 (Tessler et al., arXiv 2024) | 58.93 | 52.50 |
| OmniH2O (He et al., arXiv 2024) | 48.32 | 58.34 |

OMNITRACK的成功率较第二名BeyondMimic高出14.77个百分点，MPJPE低7.78 mm。这一差距在高动态场景下尤为突出，因为基于单一策略的方法（如OmniH2O、ExBody2）必须在部分观测下同时处理跟踪与物理可行性，而OMNITRACK通过Stage I将可行性负担前置，使Stage II策略专注于跟踪本身。

### 公平性保障

所有基线方法均在相同条件下重新实现：统一的IsaacLab模拟器环境、Unitree G1机器人平台、LAFAN1+AMASS子集训练数据、相同的部分观测设置（Sec. IV-B1）。对比结果排除了平台差异与数据偏差，差异可归因于管道设计的结构性优势。

### 真实世界验证

Fig. 5 展示了OMNITRACK策略在真实Unitree G1机器人上的零样本sim-to-real迁移能力。机器人成功执行了平衡控制、高动态机动（侧手翻等）和接触丰富交互等多种运动技能。Fig. A.7 进一步验证了长期稳定性——在户外环境中实现了一小时连续运动跟踪，从满电运行至电池耗尽，全程无需重置。Fig. 6 和 Fig. A.8 展示了实时遥操作能力，操作员通过VR头显捕捉SMPL运动，经GMR重定向和Stage I物理修正后，由Stage II策略实时跟踪执行。

![[assets/figures/papers/paper_list_l60_https_arxiv_org_abs_2602_23832/figures/007_Figure_5.jpg]]
*Figure 5: Diverse motion skills executed on the real humanoid robot. Our policy enables hour-long continuous and stable tracking of a wide range of human-like behaviors, demonstrating broad motion coverage, strong real-world versatility, and long-term control stability*

![[assets/figures/papers/paper_list_l60_https_arxiv_org_abs_2602_23832/figures/009_Figure_6.jpg]]
*Figure 6: Real-time teleoperation on the humanoid robot. Under real-time teleoperation, the robot executes dynamic, static, and contact-rich behaviors with natural, human-like motion style, demonstrating responsive control and high-fidelity whole-body coordination in the real world*

### 消融分析

TABLE A.8 系统性地考察了数据集规模与参考类型的交互效应。核心发现：**物理一致性参考的优势随数据规模扩大而增强。** 在小规模数据（1/8 LAFAN1）上，两种参考类型的成功率差距较小（物理92.08% vs 原始91.06%）；但在全数据集上，差距扩大至4.39个百分点（92.57% vs 88.18%）。这证实了物理不可行目标在大规模多样化数据上产生的累积冲突效应，以及物理一致性参考作为可扩展训练基础的必要性。

### 失败模式与局限

尽管OMNITRACK在整体指标上表现优异，分析揭示了以下边界条件：

1. **高动态子集的15.19%失败率**（TABLE III）：即使在物理一致性参考下，部分极端高动态运动（如快速翻转序列）仍导致跟踪失败。这指向了控制策略本身的能力边界，而非参考质量不足。
2. **MPJPE的适度上升**（TABLE I）：物理一致性修正引入的动力学偏差（LAFAN1上21.0 mm）是不可避免的结构性代价，在高度精确的位姿复现场景中可能成为限制因素。
3. **仿真依赖**：Stage I完全依赖仿真器生成物理一致性参考，仿真精度直接影响参考质量。在真实世界中遇到仿真未覆盖的物理现象时，参考的物理自洽性可能退化。该问题需要手动验证。

### 开放问题

实验分析揭示了以下待探索方向：

- 两阶段框架能否推广到不同执行器配置或更高自由度的类人机器人？
- 在野外复杂、非结构化环境中，长时间运行的安全性和鲁棒性如何保证？
- 能否利用无模型方法学习物理一致性修复，减少Stage I对仿真器的依赖？

### 补充图表

![[assets/figures/papers/paper_list_l60_https_arxiv_org_abs_2602_23832/figures/004_Table.jpg]]
*Table: I: Comparison of raw and physically plausible motions. Physically plausible motions eliminate penetration and floating artifacts while improving motion smoothness, with a moderate increase in MPJPE due to dynamics-consistent corrections*

![[assets/figures/papers/paper_list_l60_https_arxiv_org_abs_2602_23832/figures/006_Table.jpg]]
*Table: II: Comparison of training pipelines for motion tracking. Our training pipeline consistently outperforms alternative training strategies across all motion categories, with particularly significant advantages on challenging motion sequences*

![[assets/figures/papers/paper_list_l60_https_arxiv_org_abs_2602_23832/figures/008_Table.jpg]]
*Table: III: Comparison with state-of-the-art humanoid motion tracking methods. Our method achieves the best overall performance, showing higher success rates and lower tracking errors compared with prior approaches*

![[assets/figures/papers/paper_list_l60_https_arxiv_org_abs_2602_23832/figures/013_Table.jpg]]
*Table: A.8: Effect of Dataset Size and Reference Type on Controller Performance*

![[assets/figures/papers/paper_list_l60_https_arxiv_org_abs_2602_23832/figures/014_Figure.jpg]]
*Figure: Fig. A.7: One-hour continuous outdoor motion tracking without reset. Starting from a fully charged battery, the robot continuously performs motion tracking in an outdoor environment for one hour until the battery is depleted. Please refer to the supplementary video demo for the full execution*

![[assets/figures/papers/paper_list_l60_https_arxiv_org_abs_2602_23832/figures/015_Figure.jpg]]
*Figure: Fig. A.8: VR Headset Real-time Teleoperation on the Humanoid Robot. The raw SMPL motion is captured using the Pico VR Headset and then retargeted to the humanoid robot via GMR. The retargeted motion is further processed by the physical motion generation stage to produce physically consistent motions, which are finally tracked by the robot through the general motion tracking stage, enabling real-time teleoperation*

## 方法谱系与知识库定位

### 1. 核心思路定位：物理可行性与运动跟踪的结构化解耦

OMNITRACK 的核心贡献在于将**物理可行性修复**从控制策略的学习目标中剥离，上移至参考生成阶段。这一设计直接回应了类人机器人运动跟踪领域长期存在的一个根本性冲突：从人体运动捕捉数据重定向而来的参考轨迹天然包含物理不可行伪影（如地面穿透、足部漂浮、质心运动不一致），而控制策略在部分可观测条件下被迫同时处理“跟踪精度”与“物理可行性”这两个相互矛盾的目标，导致训练不稳定、泛化能力受限。

现有主流方法普遍采用**单阶段端到端**范式：策略在部分观测下接收原始重定向运动作为参考，通过奖励函数中的跟踪项与正则化项隐式地权衡物理可行性。这种设计的瓶颈在于，策略必须“猜测”哪些参考目标是物理上可达的，哪些是不可行的，从而在跟踪保真度与机器人稳定性之间做出妥协。OMNITRACK 通过**两阶段结构化解耦**改变了这一范式：

- **阶段 I（物理运动生成）**：在模拟器中利用完全特权信息（全局坐标、接触力、质心状态等）训练一个通用策略，将原始重定向运动转化为物理自洽的参考轨迹。该策略仅用于离线生成参考，不参与实际部署。
- **阶段 II（通用运动跟踪）**：在部分可观测和域随机化条件下，训练控制策略跟踪阶段 I 生成的物理一致性参考。由于参考本身已满足动力学约束，策略可以专注于泛化与鲁棒性，无需处理不可行目标。

这一设计将物理可行性修复的负担从在线控制转移至离线生成，本质上是对“参考质量”这一被长期忽视的变量进行了系统性控制。

### 2. 与基线方法的关系与差异

**与 Teacher-Student 蒸馏方法的对比**：**Dagger**（Ross et al., AISTATS 2011）及其变体 Dagger_hist 采用特权教师策略生成监督信号，学生策略在部分观测下模仿教师行为。OMNITRACK 的阶段 II 在形式上与 Dagger 类似（均使用教师生成的目标分布进行训练），但关键区别在于：Dagger 系列方法的教师与学生共享相同的参考运动（原始重定向数据），因此教师策略同样需要处理物理不可行性；而 OMNITRACK 的阶段 I 教师策略的**唯一目的**是生成物理自洽的参考，其输出作为阶段 II 的“净化后”目标，而非直接的行为克隆标签。TABLE II 显示，OMNITRACK 在困难高动态子集上的成功率（84.81%）远超 Dagger（67.40%）和 Dagger_hist（74.01%），验证了参考净化带来的增益远超教师蒸馏本身。

**与非对称 Actor-Critic 方法的对比**：**AAC**（Pinto et al., arXiv 2017）通过 Critic 访问特权信息、Actor 仅依赖部分观测来缓解信息不对称。OMNITRACK 的阶段 II 同样面临部分观测约束，但其核心差异在于 AAC 仍然使用原始参考运动，Critic 的特权信息主要用于价值估计的准确性，而非解决参考本身的不可行性。TABLE II 中 OMNITRACK 在 Seen Motions 上的成功率（96.13%）优于 AAC（92.78%），表明参考质量的控制比价值函数的信息增强更为关键。

**与 SOTA 类人运动跟踪方法的对比**：**OmniH2O**（He et al., arXiv 2024）专注于遥操作场景下的全身控制，**ExBody2**（Tessler et al., arXiv 2024）强调表达性全身行为生成，**BeyondMimic**（Mehta et al., arXiv 2025）采用分层强化学习实现可泛化的全身控制。这三者均采用单阶段训练范式，策略直接面向原始重定向运动进行优化。TABLE III 显示，在统一的高动态子集评估中，OMNITRACK 的成功率（84.81%）大幅领先于 BeyondMimic（70.04%）、ExBody2（58.93%）和 OmniH2O（48.32%）。这一差距在动作难度增加时急剧扩大，印证了单阶段方法在物理不可行目标面前的根本性局限——策略不得不在跟踪精度与物理可行性之间做出妥协，导致高动态场景下的控制失效。

### 3. 适用边界与能力范围

OMNITRACK 的能力边界由其两阶段结构定义：

- **运动覆盖范围**：阶段 I 的物理运动生成策略在 LAFAN1 和 AMASS 子集上训练，能够处理平衡控制、高动态机动和接触丰富的交互动作。在真实 Unitree G1 机器人上实现了连续一小时户外跟踪（Fig. 5, Fig. A.7），覆盖了侧手翻等动态技能，表明 sim-to-real 迁移具有较好的鲁棒性。
- **遥操作支持**：框架同时支持离线运动跟踪和在线遥操作。遥操作场景下，VR 头显捕获的 SMPL 运动经 GMR 重定向后，通过阶段 I 实时转化为物理一致性参考，再由阶段 II 策略执行跟踪（Fig. A.8）。
- **数据效率**：Fig. 4 和 TABLE A.8 显示，使用物理一致性参考训练的策略在数据集规模扩大时保持稳定的成功率（全 LAFAN1 上 92.57%），而原始参考训练的策略则从 1/8 数据集的较高水平下降至全数据集的 88.18%。这表明物理一致性参考消除了数据规模增大带来的“不可行目标噪声”累积效应，使得策略训练具有更好的可扩展性。

### 4. 局限性与开放问题

尽管 OMNITRACK 在实验评估中表现突出，但其设计和评估中仍存在若干值得关注的局限：

- **机器人平台与执行器配置的泛化性**：所有实验均在 Unitree G1 平台上完成。两阶段框架能否推广到不同执行器配置（如液压驱动、串联弹性执行器）或更高自由度的类人机器人，尚未得到验证。阶段 I 的物理运动生成依赖于特定机器人的动力学模型，更换平台可能需要重新训练。
- **阶段 I 对仿真精度的依赖**：物理一致性参考的质量直接取决于仿真器的动力学精度。在仿真-现实差距较大的场景（如复杂接触力学、柔性关节效应），阶段 I 生成的参考可能仍然包含现实世界中不可行的成分，进而影响阶段 II 的跟踪性能。论文未对仿真精度敏感性进行消融分析。
- **野外非结构化环境的安全性**：一小时的户外跟踪演示（Fig. A.7）令人印象深刻，但论文未报告在非平整地形、动态障碍物或外部扰动下的鲁棒性评估。长时间运行中的累积误差和突发扰动的恢复机制尚不明确。
- **无模型物理可行性修复的可能性**：阶段 I 依赖强化学习在仿真中的 rollout 来生成物理一致性运动，计算成本较高。能否利用无模型的运动修复方法（如基于物理约束的优化或扩散模型）直接对重定向运动进行“净化”，从而减少对仿真器的依赖，是一个值得探索的方向。
- **评估指标的局限性**：主要指标成功率（SR）和 MPJPE 侧重于跟踪精度，但对运动风格的自然度、能量效率、接触力分布合理性等维度的覆盖不足。TABLE I 中物理一致性运动的 MPJPE 相比原始运动有所增加（21.0 mm vs 原始值），论文将其解释为“动力学一致性修正”，但这一精度损失在高精度操作场景下的可接受性需要进一步验证。

## 原文 PDF

![[paperPDFs/arxiv_2026/OmniTrack_General_Motion_Tracking_via_Physics_Consistent_Reference.pdf]]
