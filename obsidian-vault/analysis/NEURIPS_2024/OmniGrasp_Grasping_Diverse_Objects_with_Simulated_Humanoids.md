---
title: "OmniGrasp: Grasping Diverse Objects with Simulated Humanoids"
type: paper
paper_level: A
venue: NEURIPS
year: 2024
pdf_ref: paperPDFs/NEURIPS_2024/OmniGrasp_Grasping_Diverse_Objects_with_Simulated_Humanoids.pdf
aliases:
- OmniGrasp
tags:
- NEURIPS_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 使用预训练的通用灵巧人形运动隐空间（PULSE-X，48维）作为策略的动作空间，将原始的PD目标替换为紧凑的、具有人类运动先验的隐变量，从而大幅提高样本效率，并结合预抓取（pre‑grasp）奖励引导。
primary_logic: 以大规模人类运动数据预训练的灵巧人形运动隐空间作为RL动作空间，可以在极简的状态和奖励设计下实现多样化物体的稳定抓取与任意轨迹跟踪，无需配对的全身‑物体运动数据。
claims:
- 使用预训练的通用灵巧运动表征作为动作空间是本文的核心洞察。
- 运动先验将直接训练导致的不自然运动和探索问题转化为高效学习，消除对手部参考运动或专门交互图的依赖。
- 即使只使用物体信息和随机生成轨迹，也能取得100%抓取成功率和94.1%轨迹成功率，超越先前SOTA。
- 消融实验证实PULSE‑X运动先验和预抓取奖励是成功的关键。
---

# OmniGrasp: Grasping Diverse Objects with Simulated Humanoids

> [!tip] 核心洞察
> 以大规模人类运动数据预训练的灵巧人形运动隐空间作为RL动作空间，可以在极简的状态和奖励设计下实现多样化物体的稳定抓取与任意轨迹跟踪，无需配对的全身‑物体运动数据。

| 字段 | 内容 |
|------|------|
| 中文题名 | OmniGrasp：用仿真人形机器人抓取多样化物体并跟随轨迹 |
| 英文题名 | OmniGrasp: Grasping Diverse Objects with Simulated Humanoids |
| 会议/期刊 | NEURIPS 2024 |
| Links | [Project](https://zhengyiluo.github.io/Omnigrasp) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | OmniGrasp |
| Dataset | GRAB-Goal-Test, GRAB-IMoS-Test, OakInk‑Train, OakInk‑Test |

> [!tip] 效果简介
> - GRAB-Goal-Test (cross‑object, 5 unseen objects) 上，Succ_grasp / Succ_traj 100% / 94.1% vs Braun et al.: 79.4% avg. Succ_grasp (per‑object, Table 9), trajectory succe... (OmniGrasp 全面领先)。
> - GRAB-IMoS-Test (cross‑subject, 44 objects) 上，Succ_grasp / Succ_traj 98.9% / 90.5% vs Braun et al.: inferior (OmniGrasp 显著更高)。
> - OakInk‑Train (1700 objects, 32 categories) 上，Succ_grasp / Succ_traj 93.7% / 86.2% vs N/A (无先前基线) (-)。

## 概述

### 问题背景

让仿真人形机器人抓取多样化物体并沿任意轨迹移动，是具身智能领域的核心挑战。传统方法依赖配对的全身‑物体运动捕捉数据，不仅采集成本高昂，且难以泛化到新物体。若直接在153维关节动作空间中使用强化学习训练抓取策略，躯干的探索噪声会通过运动学链放大到手臂和手指，导致物体被撞飞，形成严重的探索问题，训练几乎无法收敛。

### 核心洞察

OmniGrasp的核心洞察在于：**使用预训练的通用灵巧人形运动隐空间作为强化学习的动作空间**。具体而言，论文将大规模人类运动数据预训练得到的48维运动表征（PULSE‑X）冻结，策略仅需输出紧凑的隐变量残差，经解码器转换为自然的全身运动。这一设计将直接在高维关节空间中难以解决的探索问题，转化为在具有人类运动先验的低维流形上的高效学习，从而在极简的状态和奖励设计下实现稳定抓取与轨迹跟随。

### 方法定位

OmniGrasp属于**动作空间重参数化**范式：它并不改变底层强化学习算法（PPO），而是用预训练的运动表征替换原始的PD目标输出。该方法无需任何配对的全身‑物体运动数据，仅需物体网格、随机生成的参考轨迹，以及由GrabNet生成的预抓取手部姿态作为奖励引导。相比先前最先进的全身抓取方法（如Braun et al.），OmniGrasp在数据需求和泛化能力上均有质的突破。

### 主要结果

- **GRAB‑Goal‑Test（跨物体）**：100%抓取成功率，94.1%轨迹跟随成功率，全面超越先前最优方法。
- **GRAB‑IMoS‑Test（跨受试者，44物体）**：98.9%抓取成功率，90.5%轨迹成功率。
- **OakInk‑Test（未见物体）**：94.3%抓取成功率，87.5%轨迹成功率，展现出跨数据集泛化能力。
- **OMOMO（7个大尺寸铰接物体）**：7/7全部成功抓取。
- 消融实验证实：移除PULSE‑X运动表征后，轨迹成功率从94.1%暴跌至34.6%；移除预抓取奖励引导同样导致性能显著下降。

> **注意**：当前策略仅支持抓取‑保持‑移动，不支持手内精细操作；旋转跟踪精度仍有提升空间；物体表征依赖规范位姿，对真实世界部分可观测场景的扩展性不足。

## 背景与动机

### 问题背景：人形机器人全身抓取与轨迹跟随

使仿真人形机器人抓取多样化物体并沿任意轨迹移动，是通向通用机器人操作的关键能力。该任务要求机器人在高维关节空间中协调全身运动——包括躯干、手臂和手指——以稳定抓取物体并精确跟踪时变的目标位姿。与仅涉及末端执行器的传统抓取不同，全身抓取涉及运动学链的深层耦合：躯干的微小姿态调整会通过手臂放大到手部，直接影响抓取稳定性。

### 现有方法的瓶颈

先前最先进的方法（如 **Braun et al.**）依赖配对的全身-物体运动捕捉数据（MoCap），通过模仿学习让机器人复现人类抓取动作。这一范式面临三重约束：

1. **数据稀缺**：配对的全身体-物体运动数据采集成本极高，且难以覆盖物体形态的多样性。
2. **泛化受限**：策略局限于训练时见过的物体和轨迹模式，对新物体的适应能力弱。
3. **探索灾难**：若直接在153维关节动作空间中使用强化学习（RL）训练，由于运动学链的耦合效应，躯干的探索噪声会放大到手臂和手指，导致物体被撞飞，形成严重的探索问题，训练难以收敛。

### 核心动机：用运动先验替代数据依赖

本文的核心洞察在于：**大规模人类运动数据中蕴含的运动先验，可以作为RL探索的强约束，从而消除对配对抓取数据的依赖**。具体而言，如果能让策略在一个紧凑的、具有人类运动先验的隐空间中行动，而非直接输出高维关节目标，则探索效率将大幅提升，使极简的状态和奖励设计也能驱动稳定抓取行为的涌现。这一思路将问题从“需要教机器人如何抓取”转化为“让机器人在学会自然运动的基础上，学会如何接触和移动物体”。

## 核心创新

OmniGrasp 的核心创新在于**将预训练的通用灵巧人形运动隐空间（PULSE-X）作为强化学习的动作空间**，从而系统性地解决了直接在高维关节空间（153维PD目标）中训练全身抓取策略时面临的严重探索问题。这一设计选择构成了一个“因果旋钮”：通过将策略的输出从原始关节目标替换为48维隐变量，运动先验有效抑制了躯干探索噪声向手臂和手指的放大效应，避免了物体被撞飞等灾难性失败，使得极简的状态与奖励设计即可支撑多样化物体的稳定抓取与任意轨迹跟踪。

### 关键 changed slots

与先前最先进的全身抓取方法（如 **Braun et al.**，依赖配对的全身-物体运动捕捉数据，且仅支持单手）相比，OmniGrasp 在以下维度实现了根本性变革：

| 维度 | 基线做法 | OmniGrasp 创新 | 证据锚点 |
|------|----------|----------------|----------|
| **动作空间** | 直接输出153维PD目标 $a_t \in \mathbb{R}^{51\times3}$ | 输出48维隐变量 $z_t^{\text{omnigrasp}}$，经冻结的PULSE-X解码器与先验残差得到PD目标 | Equation (3), Algo 1 |
| **奖励设计** | 仅基于物体位姿误差的跟踪奖励 | 三阶段奖励：接近奖励 → 预抓取模仿奖励 → 物体轨迹跟踪奖励（含接触指示器） | Equation (4), §4.2 |
| **运动表征训练数据** | 仅使用不含手部运动的AMASS或仅含简单手部运动的小数据集 | 构造“灵巧AMASS”（Dex‑AMASS）：将AMASS全身运动与GRAB、Re:InterHand手部运动随机配对 | §4.1 Data Augmentation |
| **训练数据需求** | 需要配对的全身-物体运动轨迹（MoCap） | 仅需物体网格、随机或合成的参考轨迹，以及来自GrabNet的预抓取手部姿态（无需配对全身运动） | §1 Introduction |
| **初始物体位姿** | 固定或有限扰动 | 训练时随机偏航旋转和位置扰动，增强鲁棒性 | Table 4 Rand‑pose |
| **难例挖掘** | 无特殊策略 | 基于历史抓取失败次数的概率采样，集中训练困难物体 | Table 4 Hard‑neg |

### 创新机制解析

**1. 运动隐空间作为探索约束。** 直接在高维关节空间中使用RL训练时，运动学链的耦合效应使得躯干的微小探索噪声会逐级放大到手臂和手指，导致物体被撞飞，形成严重的探索瓶颈。PULSE‑X的48维隐空间通过变分信息瓶颈从大规模人类运动数据中蒸馏出紧凑的运动先验，将策略探索限制在“类人运动流形”上，大幅提升样本效率。消融实验（Table 4）证实：移除PULSE‑X后，轨迹跟随成功率从94.1%暴跌至34.6%。

**2. 预抓取奖励引导。** 三阶段奖励设计（Equation 4）是学习稳定抓取的关键：前1.5秒内，策略先通过接近奖励将手部引导至预抓取点附近，再切换为手部姿态模仿奖励形成稳定抓握，之后完全由物体轨迹跟踪奖励驱动。移除预抓取引导（Table 4, R2）会导致抓取和轨迹成功率显著下降。

**3. 数据效率的根本性提升。** 传统方法需要昂贵的配对全身-物体运动捕捉数据，而OmniGrasp仅需物体网格和随机生成的参考轨迹即可训练。这一突破得益于：（a）PULSE‑X在灵巧AMASS上预训练获得通用运动先验；（b）GrabNet仅提供预抓取手部姿态作为奖励引导（不参与推理）；（c）轨迹生成器无限供应多样化参考轨迹。

**4. 鲁棒性增强策略。** 物体初始位姿随机化（Rand‑pose）和基于历史失败次数的难例挖掘（Hard‑neg）被消融实验证实为学习鲁棒策略的必要组件（Table 4, R4 & R5），使策略能应对实际部署中的位姿不确定性。

### 与相关工作的本质差异

OmniGrasp 与此前工作的根本区别在于**将“如何运动”的知识从RL训练中解耦**，预训练到运动表征中。这使得抓取策略只需关注“何时、何地抓取”的高层决策，而非同时学习全身协调的低层控制。这一设计哲学使得系统无需手部参考运动或专门设计的交互图（interaction graph），即可在GRAB‑Goal‑Test上达到100%抓取成功率和94.1%轨迹成功率（Table 1），全面超越先前SOTA。

## 整体框架

OmniGrasp 采用**两阶段训练**流水线，将全身人形机器人的抓取与轨迹跟随问题分解为运动表征学习和目标导向的强化学习两个阶段。Figure 2 给出了完整的架构概览。

![[assets/figures/papers/paper_list_l1797_OmniGrasp_Grasping_Diverse_Objects_with_Simulated_Humanoids/figures/002_Figure_2.jpg]]
*Figure 2: Omnigrasp is trained in two stages. (a) A universal and dexterous humanoid motion representation is trained via distillation. (b) Pre-grasp guided grasping training using a pretrained motion representation*

### 阶段一：通用灵巧运动表征学习

第一阶段的目标是获得一个紧凑、通用且包含灵巧手部运动的**人形运动隐空间**。该阶段包含两个串行的学习模块：

1. **PHC‑X（运动模仿器）**：在构造的“灵巧 AMASS”（Dex‑AMASS）数据集上，训练一个人形机器人控制器模仿包含全身与手指关节的多样化人类运动序列。PHC‑X 输出教师动作标签，为后续蒸馏提供监督信号。
2. **PULSE‑X（运动表征蒸馏）**：通过变分信息瓶颈从 PHC‑X 中蒸馏出一个 48 维的运动隐空间。PULSE‑X 包含三个组件：
   - **编码器** $\mathcal{E}_{\text{PULSE-X}}(z_t \mid s_t^{\mathrm{p}}, s_t^{\mathrm{g-mimic}})$：以当前本体感觉状态和目标模仿状态为输入，输出对角高斯分布的均值与方差；
   - **先验** $\mathcal{P}_{\text{PULSE-X}}(z_t \mid s_t^{\mathrm{p}})$：仅依赖本体感觉状态，同样建模为对角高斯分布；
   - **解码器** $\mathcal{D}_{\text{PULSE-X}}$：将隐变量解码为 153 维的 PD 目标（51 个关节 × 3 维）。

训练完成后，PULSE‑X 的解码器和先验被**冻结**，作为下游抓取策略的固定动作空间。

### 阶段二：预抓取引导的抓取策略训练

第二阶段以冻结的 PULSE‑X 为动作空间，训练 OmniGrasp 策略 $\pi_{\text{OmniGrasp}}$ 完成物体抓取与轨迹跟随。核心流程如下：

- **输入**：策略仅接收**物体状态**与**目标轨迹信息** $s_t^{\mathrm{g}}$（包括预测窗口内的参考位姿/速度差、当前物体位姿、物体形状隐编码以及手-物体相对位置），**不依赖任何抓取参考姿态或全身参考运动**。
- **动作生成**：策略输出 48 维残差隐变量 $z_t^{\text{omnigrasp}}$，与 PULSE‑X 先验均值 $\mu_t^p$ 相加后，经冻结的解码器得到最终的 PD 目标：
  $$a_t = \mathcal{D}_{\text{PULSE-X}}\big(\pi_{\text{OmniGrasp}}(z_t^{\text{omnigrasp}} \mid s_t^{\mathrm{p}}, s_t^{\mathrm{g}}) + \mu_t^p\big)$$
  这一设计使得策略在具备人类运动先验的紧凑空间中探索，从根本上缓解了直接在高维关节空间（153 维）中训练时躯干噪声放大导致物体被撞飞的探索难题。
- **奖励设计**：采用**三阶段阶跃奖励**（见 Equation 4）：
  - 手部距预抓取点较远时（$t < \lambda = 1.5\text{s}$ 且距离 $> 0.2$）：使用**接近奖励** $r_t^{\text{approach}}$；
  - 靠近预抓取点后（距离 $\le 0.2$）：切换为**预抓取模仿奖励** $r_t^{\text{pre-grasp}}$，引导手部形成合理的抓取姿态；
  - 抓取阶段结束后（$t \ge \lambda$）：完全由**物体轨迹跟踪奖励** $r_t^{\text{obj}}$ 驱动，该奖励在接触条件下同时激励位姿、速度和角速度跟踪，并额外给予接触奖励。
- **辅助机制**：
  - **轨迹生成器**：随机生成多样化的物体速度和方向序列，为训练提供无限变体的参考轨迹；
  - **GrabNet 预抓取生成**：基于物体形状生成预抓取手部姿态，仅用于训练奖励引导，推理时不需要；
  - **硬负样本挖掘**：根据各物体的历史抓取失败次数进行概率采样，集中训练困难物体；
  - **物体初始位姿随机化**：训练时对物体施加随机偏航旋转和位置扰动，增强策略鲁棒性。

### 输入输出流总结

| 阶段 | 模块 | 输入 | 输出 |
|------|------|------|------|
| 阶段一 | PHC‑X | 灵巧 AMASS 运动序列 | 教师 PD 目标 |
| 阶段一 | PULSE‑X | 本体感觉 + 目标模仿状态 | 48 维隐变量 → PD 目标 |
| 阶段二 | $\pi_{\text{OmniGrasp}}$ | 本体感觉 + 物体目标状态 $s_t^{\mathrm{g}}$ | 48 维残差隐变量 |
| 阶段二 | 冻结的 PULSE‑X 解码器 | 残差隐变量 + 先验均值 | 153 维 PD 目标 → 仿真执行 |

整个流水线的关键设计在于：**用大规模人类运动数据预训练的运动先验替代手工设计的参考运动或交互图**，使策略在极简的状态和奖励设计下即可学习稳定抓取与轨迹跟随，同时天然支持对未见物体的泛化。

### 补充图表

![[assets/figures/papers/paper_list_l1797_OmniGrasp_Grasping_Diverse_Objects_with_Simulated_Humanoids/figures/001_Figure_1.jpg]]
*Figure 1: We control a simulated humanoid to grasp diverse objects and follow complex trajectories. (Top): picking up and holding objects. (Bottom): green dots - reference trajectory; pink dots - object trajectory*

## 核心模块与公式推导

OmniGrasp 的核心架构由两条解耦的训练管线构成：**灵巧通用运动表征学习（PULSE‑X）** 与 **基于预抓取引导的强化学习抓取策略（π_Omnigrasp）**。前者将高维关节动作空间压缩为紧凑的、蕴含人类运动先验的隐空间；后者在该隐空间内执行目标条件强化学习，以极简的状态与奖励设计实现多样化物体的抓取与轨迹跟随。

### 4.1 灵巧通用运动表征：PULSE‑X

#### 4.1.1 灵巧AMASS数据构造

通用运动表征的质量取决于训练数据的多样性与覆盖率。现有的大规模人体运动数据集AMASS仅包含身体关节运动，缺乏手部细节；而GRAB、Re:InterHand等数据集虽包含手部运动，但规模有限。OmniGrasp 通过**随机配对**策略构造“灵巧AMASS”（Dex‑AMASS）数据集：将AMASS中的全身运动序列与GRAB、Re:InterHand中的手部运动序列随机组合，生成约15,000条同时包含身体与手指运动的训练序列。消融实验（Table 4, R3 vs R6）证实，在Dex‑AMASS上训练PULSE‑X对轨迹跟随能力至关重要——缺失时策略仅能抓取物体，但难以在移动中保持稳定跟随。

#### 4.1.2 两阶段蒸馏：PHC‑X → PULSE‑X

运动表征的学习分为两个子阶段：

**阶段一：PHC‑X 运动模仿器。** 使用目标条件强化学习训练一个人形机器人策略，使其在仿真环境中精确复现Dex‑AMASS中的全身运动序列。PHC‑X 的输出为153维PD目标（51个关节 × 3维旋转），作为后续蒸馏的教师信号。Table 6 展示了PHC‑X在灵巧AMASS测试集上的模仿精度，验证了教师策略的运动复现能力。

**阶段二：PULSE‑X 变分信息瓶颈蒸馏。** 核心思想是通过在线蒸馏，将PHC‑X的高维动作空间压缩为48维的紧凑运动隐空间，同时保留运动的多样性与灵巧性。PULSE‑X 由三个组件构成：

- **编码器** $\mathcal{E}_{\mathrm{PULSE-X}}$：输入当前本体感觉状态 $s_t^{\mathrm{p}}$ 与目标模仿状态 $s_t^{\mathrm{g-mimic}}$，输出隐变量 $z_t$ 的对角高斯分布：

$$\mathcal{E}_{\mathrm{PULSE-X}}(z_t \mid s_t^{\mathrm{p}}, s_t^{\mathrm{g-mimic}}) = \mathcal{N}(z_t \mid \mu_t^e, \sigma_t^e)$$

- **先验** $\mathcal{P}_{\mathrm{PULSE-X}}$：仅依赖当前本体感觉状态 $s_t^{\mathrm{p}}$，建模为对角高斯分布：

$$\mathcal{P}_{\mathrm{PULSE-X}}(z_t \mid s_t^{\mathrm{p}}) = \mathcal{N}(z_t \mid \mu_t^p, \sigma_t^p)$$

- **解码器** $\mathcal{D}_{\mathrm{PULSE-X}}$：从隐变量 $z_t$ 解码为153维PD目标 $\boldsymbol{a}_t$，经PHC‑X的低层PD控制器驱动机器人关节。

蒸馏目标是最小化解码动作与教师动作的差异，同时通过KL散度约束编码器分布与先验分布的对齐。这一设计使得先验网络在推理时能够独立生成合理的运动隐变量，为下游任务提供无需目标模仿状态的运动先验。

### 4.2 预抓取引导的抓取策略：π_Omnigrasp

#### 4.2.1 动作空间设计

OmniGrasp 策略的核心创新在于**以PULSE‑X的隐空间作为动作空间**，而非直接输出153维PD目标。策略 $\pi_{\mathrm{Omnigrasp}}$ 基于当前本体感觉状态 $s_t^{\mathrm{p}}$ 与目标状态 $s_t^{\mathrm{g}}$，输出一个48维的残差隐变量 $z_t^{\mathrm{omnigrasp}}$，并与PULSE‑X先验均值 $\mu_t^p$ 相加后送入冻结的解码器：

$$\boldsymbol{a}_t = \mathcal{D}_{\mathrm{PULSE-X}}\big(\pi_{\mathrm{Omnigrasp}}(z_t^{\mathrm{omnigrasp}} \mid s_t^{\mathrm{p}}, s_t^{\mathrm{g}}) + \mu_t^p\big)$$

这一设计的因果机制在于：先验均值 $\mu_t^p$ 提供了“在当前身体状态下人类最可能如何运动”的强先验，策略仅需学习一个残差修正量来适应抓取任务的具体需求。这从根本上解决了直接在高维关节空间中使用RL训练时，躯干探索噪声经运动学链放大导致物体被撞飞的探索难题（§1 Introduction）。

#### 4.2.2 目标状态定义

策略输入中的目标状态 $s_t^{\mathrm{g}}$ 仅包含物体与轨迹跟随信息，**不包含任何抓取姿态或参考身体运动**：

$$s_t^{\mathrm{g}} \triangleq \big(\hat{p}_{t+1:t+\phi}^{\mathrm{obj}} - p_t^{\mathrm{obj}},\ \hat{\theta}_{t+1:t+\phi}^{\mathrm{obj}} \ominus \theta_t^{\mathrm{obj}},\ \hat{v}_{t+1:t+\phi}^{\mathrm{obj}} - v_t^{\mathrm{obj}},\ \hat{\omega}_{t+1:t+\phi}^{\mathrm{obj}} - \omega_t^{\mathrm{obj}},\ p_t^{\mathrm{obj}},\ \theta_t^{\mathrm{obj}},\ \sigma^{\mathrm{obj}},\ p_t^{\mathrm{obj}} - p_t^{\mathrm{hand}}\big)$$

其中 $\phi$ 为预测窗口长度，$\sigma^{\mathrm{obj}}$ 为物体形状的隐编码（通过BPS编码器从物体点云提取），$p_t^{\mathrm{obj}} - p_t^{\mathrm{hand}}$ 为手与物体的相对位置。这一极简的状态设计使得策略无需配对的全身-物体运动数据即可泛化至未见物体。

#### 4.2.3 三阶段奖励设计

OmniGrasp 的奖励函数采用**阶跃式调度**，在时间阈值 $\lambda = 1.5\mathrm{s}$ 前后切换奖励模式：

$$r_t^{\mathrm{omnigrasp}} = \begin{cases} r_t^{\mathrm{approach}}, & \|\hat{p}^{\mathrm{pre-grasp}} - p_t^{\mathrm{hand}}\|_2 > 0.2 \text{ and } t < \lambda \\ r_t^{\mathrm{pre-grasp}}, & \|\hat{p}^{\mathrm{pre-grasp}} - p_t^{\mathrm{hand}}\|_2 \le 0.2 \text{ and } t < \lambda \\ r_t^{\mathrm{obj}}, & t \ge \lambda \end{cases}$$

- **接近奖励** $r_t^{\mathrm{approach}}$：引导手部向预抓取点 $\hat{p}^{\mathrm{pre-grasp}}$（由GrabNet基于物体形状生成）靠近。
- **预抓取模仿奖励** $r_t^{\mathrm{pre-grasp}}$：手部进入预抓取点0.2 m范围内后，激励手部姿态与预抓取姿态对齐。
- **物体轨迹跟随奖励** $r_t^{\mathrm{obj}}$：时间超过 $\lambda$ 后，完全由物体跟踪目标驱动：

$$r_t^{\mathrm{obj}} = \big(w_{\mathrm{op}} e^{-100\|\hat{p}_t^{\mathrm{obj}} - p_t^{\mathrm{obj}}\|_2} + w_{\mathrm{or}} e^{-100\|\hat{\theta}_t^{\mathrm{obj}} - \theta_t^{\mathrm{obj}}\|_2} + w_{\mathrm{or}} e^{-5\|\hat{v}_t^{\mathrm{obj}} - v_t^{\mathrm{obj}}\|_2} + w_{\mathrm{or}} e^{-5\|\hat{\omega}_t^{\mathrm{obj}} - \omega_t^{\mathrm{obj}}\|_2}\big) \cdot \mathbf{1}\{C\} + \mathbf{1}\{C\} \cdot w_c$$

其中 $\mathbf{1}\{C\}$ 为接触指示器（通过距离、受力、速度的启发式规则判定），仅在手与物体接触时激活跟踪奖励与接触奖励 $w_c$。消融实验（Table 4, R2 vs R6）证实，预抓取引导奖励是学习稳定抓取的关键——缺失时抓取成功率和轨迹成功率均显著下降。

#### 4.2.4 训练策略

策略训练采用PPO算法，结合以下增强技术：

- **物体初始位姿随机化**：对物体施加随机偏航旋转和位置扰动，增强策略鲁棒性（Table 4, R4）。
- **硬负样本挖掘**：根据各物体的历史抓取失败次数进行概率采样，失败次数越多采样概率越高：

$$P(j) = \frac{s_j}{\sum_i^J s_i}$$

其中 $s_j$ 为物体 $j$ 的累计失败次数。该策略将训练资源集中于困难物体（Table 4, R5）。
- **提前终止**：当物体偏离参考位置超过0.12 m时立即终止回合，加速训练并避免无效探索。
- **轨迹生成器**：随机生成速度范围 $[0, 2]\ \mathrm{m/s}$、角度范围 $[0, 1]\ \mathrm{rad}$ 的多样化轨迹，为训练提供无限变体的参考信号。

## 实验与分析

### 核心定量结果

OmniGrasp 在多个基准上对物体抓取与轨迹跟随任务进行了评估，核心指标为抓取成功率（Succ_grasp）和轨迹跟随成功率（Succ_traj）。Table 1 展示了在 **GRAB‑Goal‑Test**（跨物体，5 个未见物体）上的表现：使用随机生成轨迹训练的策略达到 **100% 抓取成功率** 和 **94.1% 轨迹成功率**，全面超越先前最优方法 **Braun et al. **（其各物体平均抓取成功率约 79.4%，轨迹成功率显著更低，见 Table 9 逐物体拆解）。在 **GRAB‑IMoS‑Test**（跨被试，44 物体）上，使用 MoCap 轨迹训练的策略达到 98.9% 抓取成功率和 90.5% 轨迹成功率。

![[assets/figures/papers/paper_list_l1797_OmniGrasp_Grasping_Diverse_Objects_with_Simulated_Humanoids/figures/003_Table_1.jpg]]
*Table 1: Quantitative results on object grasp and trajectory following on the GRAB dataset*

![[assets/figures/papers/paper_list_l1797_OmniGrasp_Grasping_Diverse_Objects_with_Simulated_Humanoids/figures/013_Table_9.jpg]]
*Table 9: Per-object breakdown on the GRAB-Goal (cross-object) split*

为验证对大规模物体集合的扩展能力，OmniGrasp 在 **OakInk** 数据集（1700 物体，32 类别）上进行了训练和测试（Table 3）：训练集上抓取/轨迹成功率为 93.7%/86.2%，未见物体测试集上为 94.3%/87.5%。跨数据集泛化实验（GRAB 训练 → OakInk 测试）同样显示出良好的迁移能力。

![[assets/figures/papers/paper_list_l1797_OmniGrasp_Grasping_Diverse_Objects_with_Simulated_Humanoids/figures/005_Table_3.jpg]]
*Table 3: Quantitative results on OakInk with our method. We also test Omnigrasp cross-dataset, where a policy trained on GRAB is tested on the OakInk dataset*

对于大尺度铰接物体，Table 2 显示在 **OMOMO** 数据集（7 个大型物体如椅子、灯具）上，OmniGrasp 实现了 **7/7（100%）的抓取成功率**，验证了方法对非常规尺寸物体的鲁棒性。

![[assets/figures/papers/paper_list_l1797_OmniGrasp_Grasping_Diverse_Objects_with_Simulated_Humanoids/figures/007_Table_2.jpg]]
*Table 2: Quantitative results on the OMOMO dataset*

### 消融研究：关键设计因素的因果效应

Table 4 的系统消融揭示了各设计组件对性能的因果贡献：

![[assets/figures/papers/paper_list_l1797_OmniGrasp_Grasping_Diverse_Objects_with_Simulated_Humanoids/figures/006_Table_4.jpg]]
*Table 4: Ablation on various strategies of training Omnigrasp. PULSE-X: whether to use the latent motion representation. pre-grasp: pre-grasp guidance reward. Dex-AMASS: whether to train PULSE-X on the dexterous AMASS dataset. Rand-pose: randomizing the object initial pose. Hard-neg: hard-negative mining*

**运动表征（PULSE‑X）是成功的首要因素。** 移除 PULSE‑X 隐空间、直接在 PD 目标空间训练策略（R6 vs R1），轨迹成功率从 94.1% 暴跌至 34.6%。这直接验证了核心瓶颈：高维关节空间中的探索噪声通过运动学链耦合放大，导致物体被撞飞，训练难以收敛。48 维运动隐空间通过注入人类运动先验，从根本上解决了这一探索问题。

**预抓取奖励引导是学习稳定抓取的必要条件。** 移除预抓取奖励后（R2 vs R6），抓取成功率和轨迹成功率均显著下降。这表明仅靠物体位姿跟踪奖励不足以让策略自主发现有效的抓取姿态——预抓取阶段的手部姿态模仿奖励为策略提供了关键的课程引导。

**灵巧手部运动数据（Dex‑AMASS）对轨迹跟随至关重要。** 若 PULSE‑X 仅在无手部运动的 AMASS 上训练（R3 vs R6），策略仍能抓取物体，但轨迹跟随能力严重退化。这说明丰富的 finger‑level 运动先验是实现稳定持握和跟随的前提。

**初始位姿随机化和难例挖掘是鲁棒性的保障。** 移除物体初始位姿随机化（R4）或硬负样本挖掘（R5）均导致各项指标下降。难例挖掘通过基于历史失败次数的概率采样（$P(j) = s_j / \sum_i^J s_i$），将训练资源集中于困难物体，有效提升了整体成功率。

Table 8 的补充消融进一步表明：（1）RNN 策略在轨迹跟随任务上优于 MLP（94.1% vs 89.6%），因为时序记忆有助于协调持续的持握与移动；（2）向策略提供真实全身姿态作为输入反而损害性能（Succ_traj 降至 77.8%），并限制了对缺乏配对数据的新物体的泛化能力；（3）物体形状隐编码 $\sigma^{\text{obj}}$ 对性能有正向贡献。

![[assets/figures/papers/paper_list_l1797_OmniGrasp_Grasping_Diverse_Objects_with_Simulated_Humanoids/figures/012_Table_8.jpg]]
*Table 8: Additional ablations: Object-latent refers to whether to provide the object shape latent code*

### 鲁棒性与噪声敏感性

Table 5 测试了预训练策略对观测噪声的鲁棒性。在物体位姿上施加 $\sigma=0.01$ 的高斯噪声后，轨迹成功率从 94.1% 降至 91.4%，仅相对下降 2.7%，表明策略对感知噪声具有较好的容忍度。

![[assets/figures/papers/paper_list_l1797_OmniGrasp_Grasping_Diverse_Objects_with_Simulated_Humanoids/figures/009_Table_5.jpg]]
*Table 5: Study on how noise affects pretrained Omnigrasp Policy*

### 失败模式与局限性分析

尽管整体成功率较高，论文揭示了以下系统性局限：

1. **旋转跟踪精度不足。** 即使提供了完整的 6 维物体位姿和奖励，旋转误差（$E_{\text{rot}}$）仍然偏高。这表明方向控制的精度有限，可能源于运动表征对精细末端姿态的约束不足。

2. **缺乏手内操作能力。** 当前策略仅能实现“抓取‑保持‑移动”，不支持精确的手内操作（in‑hand manipulation）。这是运动表征和奖励设计均未建模的更高阶技能。

3. **物体表征依赖规范位姿。** 系统依赖规范物体姿态（canonical pose）和 BPS 编码，对于现实世界中无明确定义规范位姿或仅部分可观测的物体，扩展性不足。

4. **跨类别泛化仍有差距。** 跨数据集实验（GRAB→OakInk）的成功率低于训练物体上的表现，表明形状泛化存在提升空间。对非常规形状物体（如长条状牙膏）的性能下降尤为明显。

5. **仿真‑现实差距。** 训练环境中的简化（v‑hacd 凸分解、启发式接触检测、抓取后移除桌面）可能影响物理真实性和 sim‑to‑real 迁移潜力。

6. **轨迹分布外泛化未验证。** 随机轨迹生成器的速度（0‑2 m/s）和角度（0‑1 rad）范围有界，策略对超出此分布的极端运动可能存在泛化不足。

### 补充图表

![[assets/figures/papers/paper_list_l1797_OmniGrasp_Grasping_Diverse_Objects_with_Simulated_Humanoids/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative results. Unseen objects are tested for GRAB and OakInk. Green dots: reference trajectories. Best seen in videos on our supplement site*

![[assets/figures/papers/paper_list_l1797_OmniGrasp_Grasping_Diverse_Objects_with_Simulated_Humanoids/figures/008_Figure_4.jpg]]
*Figure 4: (Top rows): grasping different objects using both hands. (Bottom) diverse grasps on the same object*

![[assets/figures/papers/paper_list_l1797_OmniGrasp_Grasping_Diverse_Objects_with_Simulated_Humanoids/figures/010_Table_7.jpg]]
*Table 7: Hyperparameters for Omnigrasp, PHC-X, and PULSE-X*

## 方法谱系与知识库定位

### 1. 核心问题与因果机制

OmniGrasp 试图解决的核心瓶颈是：**直接在高维关节动作空间（153维PD目标）中使用强化学习训练人形机器人抓取物体时，由于运动学链的耦合效应，躯干的探索噪声会放大到手臂和手指，导致物体被撞飞，形成严重的探索问题，训练难以收敛**。这一瓶颈的因果调节旋钮（causal knob）在于**动作空间的表征层级**——将策略的输出从原始的153维PD目标替换为48维的、由大规模人类运动数据预训练得到的紧凑运动隐变量（PULSE-X），从而将无结构的探索空间转化为具有强人类运动先验的平滑流形。配合预抓取（pre-grasp）奖励引导，系统在极简的状态和奖励设计下实现了多样化物体的稳定抓取与任意轨迹跟踪。

### 2. 与基线工作的关系

#### 2.1 与先前全身抓取方法的对比

在全身抓取与轨迹跟随任务上，最直接的基线是 **Braun et al.** 的工作，该方法使用MoCap采集的配对全身-物体运动数据，但仅支持单手操作。OmniGrasp 与之相比，在以下几个关键维度上实现了根本性改进：

- **数据依赖性**：Braun et al. 需要配对的全身-物体运动轨迹（MoCap），获取成本极高且难以扩展到新物体。OmniGrasp 仅需物体网格和随机生成的参考轨迹，无需任何配对全身运动数据。
- **动作空间设计**：Braun et al. 直接在关节空间进行控制，而 OmniGrasp 使用预训练的PULSE-X运动隐空间作为动作空间，将探索复杂度从153维降至48维。
- **性能表现**：在 GRAB-Goal-Test（跨物体）基准上，OmniGrasp 达到100%抓取成功率和94.1%轨迹成功率，全面超越 Braun et al. 的79.4%平均抓取成功率（Table 1, Table 9）。

#### 2.2 与运动表征蒸馏工作的关系

OmniGrasp 的运动表征模块直接扩展自 **PULSE**（Luo et al.）的工作，将其从仅含身体运动的通用人形运动表征扩展到包含灵巧手部运动的 **PULSE-X**。关键改进包括：

- 构造“灵巧AMASS”（Dex-AMASS）数据集：将AMASS全身运动与GRAB、Re:InterHand手部运动随机配对，使运动表征同时覆盖躯干和手指的协调运动。
- 消融实验证实（Table 4, R3 vs R6），在Dex-AMASS上训练PULSE-X对轨迹跟随至关重要——缺失时系统仅能抓取但难以跟随轨迹。

#### 2.3 与直接RL训练的对比（消融基线）

消融实验中的关键对比基线是 **PHC-X（无运动先验）**，即直接在PD目标空间训练抓取策略而不使用PULSE-X运动表征。该基线直接验证了运动先验的核心作用：移除PULSE-X后，GRAB-Goal-Test上的轨迹成功率从94.1%暴跌至34.6%（Table 4, R1 vs R6），证实了直接在高维关节空间中进行RL探索的灾难性失败模式。

### 3. 技术路线定位与适用边界

#### 3.1 方法谱系中的位置

OmniGrasp 位于以下技术路线的交汇点：

- **运动表征蒸馏**：通过变分信息瓶颈从教师策略（PHC-X）蒸馏出紧凑的运动隐空间，属于离线蒸馏-在线RL的两阶段范式。
- **目标条件强化学习**：策略以物体状态和目标轨迹为条件，输出残差隐变量，经冻结的解码器转换为PD目标。
- **预抓取引导**：利用GrabNet生成的预抓取手部姿态作为奖励引导（仅训练时使用），而非直接作为参考动作输入策略。

#### 3.2 适用边界与局限

尽管 OmniGrasp 在多个基准上取得了领先性能，其适用边界受以下因素约束：

1. **无手内操作能力**：当前策略仅支持“抓取-保持-移动”，不支持精确的手内操作（in-hand manipulation）。这是方法设计的明确边界，而非意外失败模式。

2. **旋转跟踪精度有限**：尽管提供了6维物体位姿和奖励，旋转跟踪误差（E_rot）仍然较高，表明方向控制的精度受限于当前运动表征和奖励设计。

3. **物体表征的规范姿态依赖**：系统依赖规范的物体姿态（canonical pose）和BPS编码，对于现实世界中无规范姿态定义或部分可观测的物体扩展性不足。这限制了系统从纯视觉输入（如单帧RGB-D）直接工作的可能性。

4. **仿真-现实差距**：训练环境存在多项简化——物体形状通过v-hacd分解为凸几何体，接触检测使用启发式规则（距离+力+速度），仿真中桌子在抓取后被移除。这些简化可能影响物理真实性和sim-to-real迁移的可行性。

5. **训练物体规模的局限性**：训练物体最大约1700个（OakInk），主要集中在桌面级物体。对于更大规模、形态差异更大的物体集合，训练效率和泛化能力未充分验证。

6. **轨迹分布的有界性**：轨迹生成器的随机分布有界（速度0-2 m/s，角度0-1 rad），策略可能对超出此分布的运动存在泛化不足。

7. **跨类别泛化差距**：尽管策略在未见物体上表现出一定泛化能力，但跨类别泛化（如从GRAB到OakInk）的成功率仍低于在训练物体上的表现，表明形状泛化有提升空间。

### 4. 开放问题

基于上述局限，以下开放问题值得进一步探索：

1. **运动表征的进一步解耦**：能否将身体和手部运动表征解耦，从而更精细地分别控制躯干移动和手指操作？这可能为手内操作能力的引入提供基础。

2. **无规范姿态的物体表征**：如何在没有规范物体位姿的情况下构建鲁棒且通用的物体表征？可能的路径包括基于点云或NeRF的隐式表征，使系统可以仅从视觉输入工作。

3. **更优的运动表征替代方案**：扩散模型或基于Transformer的时序先验是否能在保持紧凑性的同时进一步提升动作质量和探索效率？

4. **环境感知与日常场景扩展**：在考虑避障和桌面交互等环境感知的情况下，如何将OmniGrasp扩展到更真实的日常场景？

5. **Sim-to-Real迁移**：如何通过域随机化等技术将当前仿真成果迁移到真实人形机器人上？此时必须处理传感器噪声、非理想执行器以及安全性约束。

6. **轨迹跟踪精度的提升**：如何进一步提高轨迹跟踪的成功率和精度，尤其是在快速或大角度旋转时？可能需要更精细的奖励设计或更高频的控制策略。

7. **指定抓取类型的可控性**：能否在保持紧凑运动表征的同时实现更多样的抓取策略，如指定的接触点或特定抓取类型？这需要将抓取语义信息融入运动表征或策略输入。

## 原文 PDF

![[paperPDFs/NEURIPS_2024/OmniGrasp_Grasping_Diverse_Objects_with_Simulated_Humanoids.pdf]]
