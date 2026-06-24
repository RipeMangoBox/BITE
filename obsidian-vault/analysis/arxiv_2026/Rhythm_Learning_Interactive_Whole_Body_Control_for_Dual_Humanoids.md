---
title: "Rhythm: Learning Interactive Whole-Body Control for Dual Humanoids"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/Rhythm_Learning_Interactive_Whole_Body_Control_for_Dual_Humanoids.pdf
aliases:
- Rhythm
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 交互感知运动重定向（IAMR）通过将交互网格拓扑解耦为自身边（intra-agent edges）与交互边（inter-agent edges），并采用基于距离可变刚度的优化，动态平衡自身运动保真度与交互几何一致性，为下游策略学习提供一致且物理可行的参考。
primary_logic: 显式建模并解耦自身运动结构与交互几何结构的拓扑划分与独立参考匹配，是解决人类到人形机器人交互迁移中运动学冲突的核心机制；结合基于图的奖励引导强化学习，可使双机器人掌握耦合动力学。
claims:
- IAMR 在 Intensive Contact 场景下完全消除穿透（IPR=0%），而 OR 的 IPR 高达 47.3%
- IAMR 在 Inter-X 数据集上的严格接触 F1 分数比耦合基线 DOR 提高 43%（0.843 vs 0.589）
- 完整 IGRL 策略在 Light Contact 任务中的接触成功率（CSR）达到 78.0%，远超移除接触奖励变体的 52.1%
- 真实机器人实验中，Rhythm 在 Hug 任务上的成功率达 86.7%，而单智能体基线仅 26.7%
---

# Rhythm: Learning Interactive Whole-Body Control for Dual Humanoids

> [!tip] 核心洞察
> 显式建模并解耦自身运动结构与交互几何结构的拓扑划分与独立参考匹配，是解决人类到人形机器人交互迁移中运动学冲突的核心机制；结合基于图的奖励引导强化学习，可使双机器人掌握耦合动力学。

| 字段 | 内容 |
|------|------|
| 中文题名 | Rhythm：面向双人形机器人的交互式全身控制学习 |
| 英文题名 | Rhythm: Learning Interactive Whole-Body Control for Dual Humanoids |
| 会议/期刊 | arXiv 2026 |
| Links | [Project](https://hoshi-no-ai.github.io/Rhythm/) · [paper](https://arxiv.org/abs/2603.02856) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Rhythm |
| Dataset | MAGIC Intensive Contact, Inter-X, MAGIC Light Contact, MAGIC Collaborate |

> [!tip] 效果简介
> - MAGIC Intensive Contact 上，IPR (%) 0.00 vs 47.3 (OR) (-47.3)；DSR (%) 78.3 vs 63.3 (DOR) (+15.0)。
> - Inter-X (跨数据集泛化) 上，F1-Strict (接触F1) 0.843 vs 0.589 (DOR) (+0.254 (+43%))。
> - MAGIC Light Contact (策略) 上，CSR (%) 78.0 vs 52.1 (w/o Contact Rew) (+25.9)。

## 概述

**核心问题**：从人类交互演示中学习双人形机器人的全身控制面临两个根本性瓶颈——异构形态迁移导致的**运动学冲突**（kinematic conflict），以及物理接触引入的**耦合动力学**建模困难。现有方法或忽略交互约束将双机器人视为独立个体，或将系统作为统一整体建模，均无法在保持自身运动风格的同时维持精确的交互几何。

**核心方法**：Rhythm 提出**交互感知运动重定向（IAMR）**与**交互引导强化学习（IGRL）**两级框架。IAMR 通过将交互网格拓扑解耦为自身边（intra-agent edges）与交互边（inter-agent edges），并采用基于距离的指数衰减变刚度优化，动态平衡自身运动保真度与交互几何一致性，为下游策略提供运动学可行且物理一致的参考。IGRL 继承 IAMR 的图结构先验，设计交互图奖励与接触图奖励，引导多智能体 PPO 策略掌握双机器人的耦合动力学。

**主要结果**：
- **重定向层面**：IAMR 在 Intensive Contact 场景下完全消除穿透（IPR=0%），而 OR 基线高达 47.3%；在 Inter-X 跨数据集泛化中，严格接触 F1 分数比耦合基线 DOR 提升 43%（0.843 vs 0.589）。
- **策略层面**：完整 IGRL 在 Light Contact 任务中接触成功率（CSR）达 78.0%，远超移除接触奖励变体的 52.1%；Collaborate 任务交互成功率（ISR）达 92.9%，而单智能体基线仅 18.7%。
- **真实机器人**：在 Unitree G1 双机器人平台上，Rhythm 在 Hug 任务成功率达 86.7%（单智能体基线仅 26.7%），并展现出对外部扰动（推、拉、踢）的鲁棒恢复能力。

**方法定位**：Rhythm 属于**基于图先验的交互迁移与多智能体强化学习**方法，其核心贡献在于首次将交互拓扑的解耦建模与距离感知动态刚度机制引入人形机器人交互重定向，并通过图结构奖励将重定向先验无缝桥接至物理仿真策略学习，形成从人类演示到真实双机器人交互的完整管线。

## 背景与动机

### 问题背景：双人形机器人交互控制的挑战

使两台人形机器人像人类一样进行物理交互——拥抱、握手、共舞——是具身智能领域的长期愿景。这类任务要求机器人不仅维持自身平衡与运动精度，还必须在动态耦合中感知并响应同伴的动作与接触力。然而，从人类演示数据迁移到双人形机器人时，面临两个根本性瓶颈：

1. **异构形态导致的运动学冲突（kinematic conflict）**：人类与人形机器人在骨骼长度、关节自由度、质量分布上存在显著差异。当两台机器人试图复现一对人类的交互动作时，各自独立的运动学约束可能与交互几何要求产生矛盾——例如，为保持握手接触，两台机器人的末端执行器必须在空间中精确会合，但这可能迫使某一方超出其关节限位或采取不自然的姿态。

2. **物理接触引入的复杂耦合动力学**：一旦机器人之间发生物理接触，两个原本独立的动力学系统便耦合为一个整体。接触力的产生、传递与消失使系统状态空间急剧膨胀，且接触的间歇性（如握手时的接触-分离切换）引入了非光滑动力学，使得基于模型的控制方法难以建模，而纯数据驱动方法则面临样本效率低下的问题。

### 现有方法缺口

现有工作在处理双人形机器人交互时存在明显的结构性缺陷，可归纳为三个层面：

**运动重定向层面**：传统方法将双机器人系统视为两个独立单体的简单叠加。**GMR** 等标准笛卡尔空间重定向方法为每个机器人独立求解运动学映射，完全忽略交互约束。**OmniRetarget（OR）** 虽引入了交互网格（I-Mesh）以保持个体身体拓扑，但仍缺乏跨智能体的交互建模。**Dual-OmniRetarget（DOR）** 将 OR 扩展至多智能体设定，构建包含所有身体节点的统一交互网格，但未能区分自身运动约束与交互约束——这种“一刀切”的处理方式导致：当交互紧密度高时，自身运动保真度被牺牲；当交互松散时，不必要的强约束又限制了运动的自然性。定量证据表明，OR 在 Intensive Contact 场景下的穿透率（IPR）高达 47.3%，而 DOR 在跨数据集泛化（Inter-X）上的严格接触 F1 分数仅为 0.589（Table I）。

**控制策略层面**：主流的单智能体全身控制方法（Single Agent）仅跟踪自身参考运动，完全忽略同伴状态与交互目标。这导致在需要紧耦合协调的任务中，策略无法感知同伴的位置、朝向与运动相位，从而产生漂移、碰撞或“空中握手”（contact loss）等失败模式。消融实验显示，单智能体基线在 Collaborate 任务上的交互成功率（ISR）仅为 18.7%（Table II），几乎无法完成任何有意义的协作。

**真实部署层面**：仿真环境通常假设全局可观测性和同步执行，而真实系统缺乏相对状态估计能力，且两台机器人天然异步运行。如何在仅依赖机载传感器的条件下实现稳定的相对定位与时间同步，是策略从仿真迁移至实物的关键工程挑战。

### 本文动机

上述缺口的共同根源在于：**现有方法未能显式建模并解耦双机器人交互中的自身运动结构与交互几何结构**。自身运动要求每台机器人保持运动学可行且风格自然的姿态，交互几何则要求两台机器人的相对空间关系（尤其是接触区域的拓扑）与参考一致。当这两类约束被混为一谈时，优化过程便陷入不可调和的冲突。

Rhythm 的核心动机正是通过**拓扑解耦**来化解这一冲突：将双机器人系统的空间关系显式划分为自身边（intra-agent edges）与交互边（inter-agent edges），对前者匹配独立参考以保持自身运动保真度，对后者匹配统一参考以强制交互几何一致性，并通过距离依赖的可变刚度动态平衡两者。这一解耦思路贯穿整个框架——从运动重定向（IAMR）到强化学习奖励设计（IGRL），再到真实部署的同步机制——形成了一条从“理解交互结构”到“执行交互行为”的完整因果链。

## 核心创新

Rhythm 的核心创新在于将双人形机器人交互控制拆解为两个递进且互补的阶段——**交互感知运动重定向（IAMR）** 与 **交互引导强化学习（IGRL）**——并辅以面向真实部署的软同步机制。其关键突破在于首次显式建模并解耦了“自身运动结构”与“交互几何结构”，从而系统性地解决了人类演示到双人形机器人迁移中的运动学冲突与物理耦合动力学难题。

### 创新一：解耦交互网格与距离自适应刚度优化（IAMR）

**核心矛盾与解决思路。** 现有重定向方法（如 **GMR**、**OR (OmniRetarget)**、**DOR (Dual-OmniRetarget)**）将双机器人系统要么视为两个独立单体，要么视为一个统一整体。前者完全忽略交互约束，导致接触丢失或穿透；后者虽构建了包含所有身体节点的统一交互网格，却无法区分“保持自身姿态”与“维持交互接触”这两类相互冲突的约束——当源人类形态与目标机器人形态存在显著差异时，统一优化必然产生运动学冲突（kinematic conflict）。

IAMR 的关键洞察是：**将交互网格的拓扑显式划分为“自身边（intra-agent edges）”与“交互边（inter-agent edges）”两个互斥子图，并为它们分配独立的几何参考。** 具体而言：
- **自身边** $\mathcal{E}_{self}$ 连接同一机器人内部的网格顶点，其优化目标 $E_{self}$ 使各机器人分别匹配独立参考（Individual Manifold），以保留自身运动风格与身体拓扑；
- **交互边** $\mathcal{E}_{inter}$ 连接不同机器人间的顶点，其优化目标 $E_{inter}$ 使交互顶点对匹配统一参考（Unified Manifold），以强制维持交互几何一致性。

**距离依赖的可变刚度机制。** 交互约束并非均匀施加——近距离接触（如握手时的指尖）需要高精度匹配，而远距离空间关系（如舞蹈中的相对站位）可适当松弛。IAMR 将交互边建模为可变刚度弹簧：

$$E_{inter}(q) = \sum_{(i,j) \in \mathcal{E}_{inter}} \omega_{ij}(d_{ij}) \cdot \| (p_i - p_j) - (\hat{p}_i^{uni} - \hat{p}_j^{uni}) \|^2$$

其中刚度 $\omega_{ij}$ 随源距离 $d_{ij}$ 呈指数衰减：

$$\omega_{ij}(d_{ij}) = \omega_{max} \cdot e^{-\gamma d_{ij}}$$

这一设计使优化器在接触紧密处施加强约束以消除穿透，在远处则放松以允许自然的姿态调整，从而在“自身保真度”与“交互几何精度”之间实现自适应平衡。

**证据强度。** 该创新的有效性在定量实验中得到了有力验证：在 MAGIC 数据集的 Intensive Contact 场景下，IAMR 的穿透率（IPR）为 0%，而 OR 基线高达 47.3%（Table I）；在跨数据集泛化测试（Inter-X）中，IAMR 的严格接触 F1 分数达到 0.843，比耦合基线 DOR 的 0.589 提升了 43%（Table I）。定性可视化（Fig. 4）进一步显示，基线方法在握手任务中出现“空气握手”（接触丢失），而 IAMR 保持了精确的接触几何。

### 创新二：基于图奖励的交互引导强化学习（IGRL）

**从运动学到动力学的跨越。** IAMR 提供的参考运动是纯运动学的，无法编码物理接触所需的力信息。IGRL 的创新在于：将 IAMR 提取的交互图与接触图先验直接转化为强化学习的奖励信号，使策略在学习全身控制的同时，显式地受到交互拓扑和物理接触的引导。

具体而言，IGRL 在标准多智能体 PPO（MAPPO）框架的基础上，引入了三个关键组件：

1. **自我中心的同伴感知（ego-centric peer observation）**：策略观测 $o_{peer}$ 包含同伴相对于自身的位姿（$P_{rel}$, $R_{rel}$）及同伴关节位置，使每个机器人具备闭环的相互感知能力。这不同于单智能体基线（Single Agent）完全忽略同伴状态，也不同于仿真中假设的全局可观测性——ego-centric 设计是后续真实部署中依赖相对定位的前提。

2. **交互图奖励（$r_{inter}$）**：继承 IAMR 中交互边的距离动态权重 $w_{ij}$，以指数形式惩罚仿真中交互顶点对位置与参考的偏差：

$$r_{inter} = \exp \left( - \frac{1}{\sigma_{inter}} \sum_{(i,j) \in \mathcal{E}_{inter}} w_{ij} \| p_{ij}^{sim} - p_{ij}^{ref} \|^2 \right)$$

这使得策略优先学习维持空间交互拓扑，而非仅仅跟踪自身关节轨迹。

3. **接触图奖励（$r_{contact}$）**：由激活接触误差（考虑接触状态与接触力一致性）和未激活接触误差（抑制非接触部位的虚假力）两部分组成，显式正则化物理接触的真实性。

**消融实验揭示了各组件的因果作用**（Table II）：
- **移除交互图奖励（w/o Interaction Rew）** 导致所有指标崩溃：Collaborate 任务的交互成功率（ISR）从 92.9% 骤降至 58.1%，Light Contact 的接触成功率（CSR）从 78.0% 降至 28.1%，证明交互拓扑引导是策略成功的必要条件。
- **移除接触图奖励（w/o Contact Rew）** 产生了“幽灵”效应：尽管几何精度较高（ISR 93.4%），但接触真实性严重不足（CSR 仅 52.1%），机器人看似对齐却未建立真实物理接触（Fig. 5 定性展示），验证了基于力的接触正则化对物理耦合是不可或缺的。
- **移除同伴观测（w/o Peer Obs）** 使策略丧失闭环同步能力，Light Contact 的 CSR 降至 18.6%，证明 ego-centric 的相对状态感知对紧耦合交互至关重要。

### 创新三：面向真实部署的软同步与层次化定位

仿真到真实（Sim-to-Real）的迁移面临两个实际挑战：两机器人异步执行导致的时域失配，以及缺乏全局可观测性。Rhythm 的部署模块（Sec. III-C）通过两个轻量但有效的设计解决：
- **相位比例反馈软同步**：机器人通过无线桥接交换当前相位 $\phi$，ego 智能体根据相位差动态调整自身推进速率 $\dot{\phi}_{ego} = 1.0 + k (\phi_{peer} - \phi_{ego})$，实现无需全局时钟的软时间对齐。
- **LiDAR-IMU 融合层次化定位**：通过 Point-LIO + GICP + 卡尔曼滤波器的组合，在预构建地图中提供全局位姿估计，支撑 ego-centric 同伴感知的输入。

真实机器人实验中（Table III），完整 Rhythm 系统在 Hug 任务上的成功率达 86.7%，而单智能体基线仅 26.7%，验证了上述创新的整体有效性。

## 整体框架

Rhythm 是一个面向双人形机器人的交互式全身控制学习框架，其核心挑战在于：从人类演示数据迁移到双人形机器人时，异构形态导致的运动学冲突与物理接触引入的复杂耦合动力学，使得多智能体全身控制在真实世界中难以稳定实现。

为解决这一问题，Rhythm 构建了三个紧密耦合的模块，形成从数据到真实部署的完整流水线（Fig. 2）：

![[assets/figures/papers/paper_list_l1705_Rhythm_Learning_Interactive_Whole_Body_Control_for_Dual_Humanoids/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Rhythm. IAMR utilizes decoupled optimization to generate high-quality humanoid-humanoid motion interaction references from human demonstrations. Guided by these references, IGRL employs MAPPO and graph-based rewards to learn robust coupled dynamics. Finally, the deployment module facilitates Sim-to-Real transfer via Lidar-fused state estimation and inter-agent synchronization*

1. **交互感知运动重定向（Interaction-Aware Motion Retargeting，IAMR）**：负责从人类交互数据生成运动学一致且保持交互几何的双人形机器人参考运动。该模块将交互网格拓扑显式解耦为自身边（intra-agent edges）与交互边（inter-agent edges），并采用基于距离可变刚度的优化，在自身运动保真度与交互几何一致性之间实现自适应平衡。输出不仅包含关节级参考轨迹，还包括交互图（interaction graph）与接触图（contact graph）作为下游策略的先验。

2. **交互引导强化学习（Interaction-Guided Reinforcement Learning，IGRL）**：基于多智能体 MAPPO 框架，利用 IAMR 提供的图先验构建奖励函数，学习具有物理耦合的动态交互控制策略。IGRL 包含 ego-centric 的同伴感知（相对位置、相对朝向及同伴关节位置），并引入交互图奖励与接触图奖励，分别强制空间对齐与物理接触一致性。

3. **真实世界部署系统（Real-World Deployment System）**：通过 LiDAR-IMU 融合的层次化定位系统（Point-LIO + GICP + 卡尔曼滤波）提供全局位姿，并采用基于相位比例反馈的代理间软同步机制（$\dot{\phi}_{ego} = 1.0 + k (\phi_{peer} - \phi_{ego})$），将仿真中学习的策略迁移至实物双机器人。

**输入输出流**：原始人类交互运动数据首先进入 IAMR，经解耦优化输出运动学可行的双机器人参考轨迹及图结构先验；IGRL 以这些参考和先验为引导，输出耦合控制策略；部署系统则负责将策略从仿真桥接至真实机器人，实现稳定的物理交互。

### 补充图表

![[assets/figures/papers/paper_list_l1705_Rhythm_Learning_Interactive_Whole_Body_Control_for_Dual_Humanoids/figures/001_Figure_1.jpg]]
*Figure 1: The proposed framework, Rhythm, facilitates a spectrum of humanoid–humanoid interactions. (a–c) Contact-Rich Interaction: The method handles interactions ranging from light contact (Greeting) to intensive contact (Hug, Shoulder-to-Shoulder), maintaining fine-grained contact geometry without penetration (shown in the zoomed-in views). (d) Coordinated Interaction: The humanoids perform synchronized long-horizon dance (La La Land), with trajectories showing consistent spatiotemporal alignment and stable relative positioning over time*

![[assets/figures/papers/paper_list_l1705_Rhythm_Learning_Interactive_Whole_Body_Control_for_Dual_Humanoids/figures/004_Figure_3.jpg]]
*Figure 3: Overview of MAGIC. MAGIC contains ∼3 hours of high-fidelity interaction data balanced across five semantic categories (inner chart). Representative snapshots (outer ring) illustrate the diversity ranging from loose spatiotemporal coordination to intensive contact*

## 核心模块与公式推导

Rhythm 系统由三个紧密集成的模块构成：**交互感知运动重定向（IAMR）**、**交互引导强化学习（IGRL）** 和 **真实世界部署系统**。其核心瓶颈在于：从人类演示数据迁移到双人形机器人时，异构形态导致的运动学冲突和物理接触引入的复杂耦合动力学，使得多智能体全身控制在真实世界中难以稳定实现。以下逐一解析各模块的关键设计与公式。

---

### 交互感知运动重定向（IAMR）

IAMR 的核心洞察是：显式建模并解耦自身运动结构与交互几何结构的拓扑划分与独立参考匹配，是解决人类到人形机器人交互迁移中运动学冲突的关键机制。

**1. 交互网格的拓扑解耦**

IAMR 首先将双人交互网格的边集 $E$ 显式划分为两个不相交的功能组：
- **自身边（Intra-Agent Edges）** $E_{self}$：连接同一智能体内部的节点，负责编码个体身体拓扑与运动风格。
- **交互边（Inter-Agent Edges）** $E_{inter}$：跨越两个智能体的边，负责编码交互几何约束（如握手时手掌之间的相对位置）。

这种拓扑划分使得后续优化可以为两类边分配不同的几何参考，从根本上避免运动学冲突。

**2. 拉普拉斯坐标编码局部几何**

对于网格顶点 $p_i$，其拉普拉斯坐标定义为该顶点相对于其邻居加权平均的偏差：

$$\mathcal{L}(p_i) = p_i - \sum_{j \in \mathcal{N}(i)} c_{ij} p_j$$

其中 $\mathcal{N}(i)$ 是 $p_i$ 的邻居集合，$c_{ij}$ 为归一化余切权重。拉普拉斯坐标编码了局部几何细节，在优化中用于保持身体表面的局部形状。

**3. 解耦优化目标**

IAMR 将重定向形式化为一个约束优化问题，目标函数由自身运动项与交互项组成：

$$\boldsymbol{q}^* = \arg\min_{\boldsymbol{q}} \left( E_{self}(\boldsymbol{q}) + E_{inter}(\boldsymbol{q}) \right) \quad \mathrm{s.t.} \quad \boldsymbol{q} \in \mathcal{C}_{phy}$$

其中 $\mathcal{C}_{phy}$ 为物理可行性约束（关节限位、自穿透避免等）。

**自身运动项** $E_{self}$ 使各机器人的拉普拉斯坐标与骨骼朝向匹配独立参考（Individual Manifold），以保留自身运动风格：

$$E_{self}(q) = \sum_{a \in \{1,2\}} \sum_{p_i \in \mathcal{V}_a} \| \mathcal{L}(p_i) - \mathcal{L}(p_i^{ind}) \|^2 + \lambda_{rot} \sum_{a} \sum_{k \in \mathcal{B}_a} \| \theta_k \ominus \hat{\theta}_k^{src} \|^2$$

其中 $\mathcal{V}_a$ 是智能体 $a$ 的顶点集，$\mathcal{B}_a$ 是骨骼关节集，$\ominus$ 表示旋转空间中的测地距离。

**交互项** $E_{inter}$ 是 IAMR 的核心创新——将跨智能体交互建模为**距离可变刚度的弹簧势能**：

$$E_{inter}(q) = \sum_{(i,j) \in \mathcal{E}_{inter}} \omega_{ij}(d_{ij}) \cdot \| (p_i - p_j) - (\hat{p}_i^{uni} - \hat{p}_j^{uni}) \|^2$$

其中 $(\hat{p}_i^{uni} - \hat{p}_j^{uni})$ 来自统一参考（Unified Manifold）中对应交互边的相对位置向量。刚度函数 $\omega_{ij}$ 采用指数衰减形式：

$$\omega_{ij}(d_{ij}) = \omega_{max} \cdot e^{-\gamma d_{ij}}$$

这里 $d_{ij}$ 是源运动中两顶点的欧氏距离。这一设计的物理直觉是：**接触越紧密的交互边，其约束刚度越大**，从而优先保证接触区域的几何一致性；而对于距离较远的交互边（如两人身体躯干之间），约束则自然松弛，避免因过度约束导致不自然的僵硬姿态。

IAMR 的输出不仅是运动学一致的双机器人参考运动，还提取了两种拓扑先验——**交互图**（黄色边，编码空间对齐约束）和**接触图**（红色边，编码物理接触关系），为下游强化学习提供引导。

---

### 交互引导强化学习（IGRL）

IGRL 基于多智能体 PPO（MAPPO）框架，利用 IAMR 提取的图先验设计奖励函数，使策略学习具有物理耦合的动态交互。

**1. 同伴感知观测**

与单智能体基线忽略同伴状态不同，IGRL 的策略观测包含 ego-centric 的同伴感知信息：相对位置 $P_{rel}$、相对朝向 $R_{rel}$ 以及同伴关节位置。这使得策略能够感知交互对象的实时状态并做出闭环调整。

**2. 交互图奖励**

交互图奖励直接继承 IAMR 的动态权重，强制策略维持空间交互拓扑：

$$r_{inter} = \exp \left( - \frac{1}{\sigma_{inter}} \sum_{(i,j) \in \mathcal{E}_{inter}} w_{ij} \| p_{ij}^{sim} - p_{ij}^{ref} \|^2 \right)$$

其中 $w_{ij}$ 复用 IAMR 的距离衰减权重，$\sigma_{inter}$ 为温度参数。该奖励使策略优先学习维持近距离交互边的几何精度，而对远距离边则给予更大容差。

**3. 接触图奖励**

由于运动学参考缺乏力信息，IGRL 引入接触图奖励来正则化物理交互，设计为组合形式：

$$r_{contact} = \lambda_{act} \cdot e^{-E_{act}/\sigma_c^2} + \lambda_{inact} \cdot e^{-E_{inact}/\sigma_c^2}$$

- **激活接触误差** $E_{act}$：惩罚应接触但未接触或接触力不匹配的情况，同时考虑接触状态与接触力。
- **未激活接触误差** $E_{inact}$：抑制非接触区域的不期望接触力，防止“幽灵”效应。

---

### 真实世界部署中的软同步

在真实部署中，两机器人通过无线网桥交换当前运动相位 $\phi$。收到同伴相位 $\phi_{peer}$ 后，ego 智能体通过比例反馈动态调整自身相位推进速率：

$$\dot{\phi}_{ego} = 1.0 + k (\phi_{peer} - \phi_{ego})$$

其中 $k$ 为同步增益。这一软同步机制避免了硬性锁步带来的脆性，允许策略在外部扰动下自适应恢复时间对齐。全局位姿估计则依赖 LiDAR-IMU 融合的层次化定位系统（Point-LIO + GICP + 卡尔曼滤波），当前系统需预构建 LiDAR 地图，限制了其在未知环境中的部署能力。

### 补充图表

![[assets/figures/papers/paper_list_l1705_Rhythm_Learning_Interactive_Whole_Body_Control_for_Dual_Humanoids/figures/009_Figure_7.jpg]]
*Figure 7: Visualization of Topological Interaction Priors. We illustrate the extracted graph structures on a representative interaction task, where yellow edges denote spatial interaction constraints and red edges indicate physical contacts*

## 实验与分析

### 1. 实验设置概览

Rhythm 的实验体系分为三个层次：**运动重定向质量评估**、**仿真策略性能消融**与**真实机器人部署验证**。

**数据集**：重定向实验在自建的 **MAGIC** 数据集（约 3 小时高保真双人交互数据，覆盖 Coordinated、Intimate/Care、Contact、Social Rituals、Competitive 五类语义，Fig. 3）和公开跨域数据集 **Inter-X** 上进行。策略实验在 MAGIC 上按交互强度划分的 Intensive Contact、Light Contact、Collaborate 三个子集上评估。

**评估指标**：
- **安全性**：交互穿透率（IPR, %）、最小对偶距离（MPD, m）
- **保真度**：交互边误差（IEE, m）、接触 F1 分数（F1-Strict）
- **下游效用**：下游成功率（DSR, %）、交互成功率（ISR, %）、物理接触成功率（CSR, %）

**公平性保障**：
- 所有重定向方法共享相同的原始运动数据和骨骼缩放预处理
- 所有 RL 变体基于相同的 PPO 超参与网络架构，仅移除或修改特定组件（如置零特定观测、移除特定奖励项），保证消融比较的因果性
- 真实机器人实验中，完整 Rhythm 系统与单智能体基线共享相同的软硬件平台与通信系统，结果为 10 次试验平均

---

### 2. 运动重定向：IAMR 的核心优势

#### 2.1 定量结果（Table I）

Table I 报告了在 MAGIC 四个交互类别上的重定向结果。IAMR 在安全性-保真度-效用三角中实现了最优平衡：

| 场景 | 指标 | IAMR | 最强基线 | 提升 |
|------|------|------|----------|------|
| Intensive Contact | IPR (%) | **0.00** | 47.3 (OR) | 完全消除穿透 |
| Intensive Contact | DSR (%) | **78.3** | 63.3 (DOR) | +15.0 |
| Inter-X（跨数据集） | F1-Strict | **0.843** | 0.589 (DOR) | +0.254 (+43%) |

**关键发现**：
- **OR** 在密集接触场景中穿透率高达 47.3%，几乎无法产生物理可行的参考——其交互网格虽保持了身体拓扑，但缺乏跨智能体约束建模，导致身体相互穿透。
- **DOR** 将双机器人统一建模为单一交互网格，虽在 MPD 上有所改善，但因未区分自身运动与交互约束，在 Inter-X 上接触 F1 仅 0.589，且 DSR 落后 IAMR 15 个百分点。
- **IAMR 的 0% 穿透率**直接归因于其核心机制——将交互网格解耦为自身边（$\mathcal{E}_{self}$）与交互边（$\mathcal{E}_{inter}$），并分别匹配独立参考与统一参考，从根本上消解了运动学冲突。

#### 2.2 定性可视化（Fig. 4）

![[assets/figures/papers/paper_list_l1705_Rhythm_Learning_Interactive_Whole_Body_Control_for_Dual_Humanoids/figures/003_Figure_4.jpg]]
*Figure 4: Qualitative Visualization of Retargeting on Inter-X. Top: Baselines suffer from contact loss (“air handshakes”), whereas IAMR preserves precise interaction geometry. Bottom: OR leads to severe penetration while DOR forces unnatural stiff postures; IAMR maintains close-proximity topology without collisions*

Fig. 4 展示了在 Inter-X 跨域场景下的重定向质量对比：
- **接触丢失问题**：基线方法在握手任务中出现“空气握手”（air handshakes），即视觉上两手接近但实际无接触；IAMR 保持了精确的交互几何。
- **穿透与僵硬问题**：OR 导致严重穿透，DOR 则因统一约束过强而迫使机器人呈现不自然的僵硬姿态；IAMR 维持了紧密接触拓扑且无碰撞。

这验证了 IAMR 中**距离依赖的变刚度机制**（$\omega_{ij}(d_{ij}) = \omega_{max} \cdot e^{-\gamma d_{ij}}$）的有效性——近距离交互边获得高刚度以强制接触一致性，远距离边则松弛以避免过度约束自身运动。

---

### 3. 策略学习：IGRL 的消融分析

#### 3.1 核心消融结果（Table II）

Table II 通过系统性移除 IGRL 的关键组件，揭示了各机制的因果贡献：

| 变体 | Collaborate ISR (%) | Light Contact CSR (%) | 核心洞察 |
|------|--------------------|-----------------------|----------|
| **Ours (完整)** | **92.9** | **78.0** | 最优平衡 |
| w/o Interaction Rew | 58.1 (-34.8) | 28.1 (-49.9) | 交互拓扑引导是策略成功的前提 |
| w/o Contact Rew | 93.4 (+0.5) | 52.1 (-25.9) | 几何精度高但物理耦合不足（“幽灵”效应） |
| w/o Peer Obs | 65.2 (-27.7) | 18.6 (-59.4) | 闭环同步能力丧失 |
| Single Agent | 18.7 (-74.2) | — | 无交互建模几乎无法成功 |

**因果链条分析**：

1. **交互图奖励（$r_{inter}$）是空间对齐的前提**：移除后 Collaborate 的 ISR 从 92.9% 暴跌至 58.1%，Light Contact 的 CSR 从 78.0% 降至 28.1%。该奖励继承 IAMR 的距离动态权重，使策略优先学习维持交互拓扑，而非仅跟踪自身运动。

2. **接触图奖励（$r_{contact}$）消除“幽灵”效应**：移除接触奖励后，ISR 甚至微升至 93.4%，但 CSR 骤降至 52.1%。Fig. 5 的可视化揭示了原因——机器人虽在几何上精准对齐（低 IEE），但未产生真实的物理接触力，呈现“幽灵”般的视觉穿透。这验证了基于力的接触正则化（激活接触误差与未激活接触误差的组合奖励）对物理耦合是必要的。

![[assets/figures/papers/paper_list_l1705_Rhythm_Learning_Interactive_Whole_Body_Control_for_Dual_Humanoids/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative Visualization of Policy. Single Agent (blue) drifts into collisions. w/o Contact Rew (green) achieves low error but exhibits physical “ghosting”. In contrast, Ours enforces valid physical contact*

3. **同伴感知（$o_{peer}$）是闭环同步的关键**：移除 ego-centric 的相对位置、朝向与关节位置观测后，Light Contact 的 CSR 降至 18.6%，证明紧耦合交互需要实时相对状态反馈以维持同步。

4. **单智能体基线的彻底失败**：在 Collaborate 任务中 ISR 仅 18.7%，证实显式多智能体交互建模是解决耦合动力学的必要条件。

#### 3.2 定性行为对比（Fig. 5）

Fig. 5 提供了策略行为的直观对比：
- **Single Agent（蓝色）**：完全忽略同伴，导致漂移与碰撞
- **w/o Contact Rew（绿色）**：几何误差低但物理上“穿透”同伴，无有效接触力
- **Ours（完整）**：建立真实物理接触，同时保持空间对齐

---

### 4. 真实机器人验证

#### 4.1 成功率对比（Table III）

在 Unitree G1 双机器人平台上，Rhythm 在三个任务上进行了 10 次重复试验：

| 任务 | Rhythm 成功率 | Single Agent 成功率 | 提升 |
|------|-------------|-------------------|------|
| Hug | **86.7%** | 26.7% | +60.0% |
| Handshake | **80.0%** | 33.3% | +46.7% |
| Dance | **73.3%** | 20.0% | +53.3% |

**成功率差距的根源**：单智能体基线仅跟踪自身参考运动，在 Hug 任务中因缺乏同伴感知而无法调整末端执行器位置以匹配同伴身体，导致接触建立失败。Rhythm 通过 IAMR 提供的交互图先验与 IGRL 的同伴感知，使机器人能动态调整以建立并维持物理接触。

#### 4.2 鲁棒性测试（Fig. 6）

![[assets/figures/papers/paper_list_l1705_Rhythm_Learning_Interactive_Whole_Body_Control_for_Dual_Humanoids/figures/008_Figure_6.jpg]]
*Figure 6: Robustness to disturbances. Our policy demonstrates strong resilience against aggressive external perturbations (pulling, pushing, and kicking), successfully recovering balance and synchronization*

Fig. 6 展示了策略对外部扰动的鲁棒性。在推、拉、踢等攻击性扰动下，Rhythm 策略能够恢复平衡并重新建立同步，表明 IGRL 学到的耦合动力学策略具有较强的抗干扰能力。这一鲁棒性部分归功于域随机化训练（Table V）和软同步机制（$\dot{\phi}_{ego} = 1.0 + k (\phi_{peer} - \phi_{ego})$）提供的时序弹性。

---

### 5. 失败模式与局限性

1. **未知环境定位依赖**：当前系统依赖预构建的 LiDAR 地图进行全局定位（通过 Point-LIO + GICP + KF 的层次化系统），在未知或动态环境中部署能力受限。这是真实机器人实验中未在完全陌生场景测试的原因。

2. **双智能体上限**：所有实验仅验证了双人形机器人系统，尚未扩展到三个或更多智能体的协作场景。当智能体数量增加时，交互图的拓扑复杂度呈组合增长，IAMR 的解耦优化和 IGRL 的图奖励是否仍可扩展尚待验证。

3. **形态差异的边界**：虽然 IAMR 在 Inter-X 跨域数据上表现优异，但当源人类与目标人形机器人的形态差异极端时（如臂长比例严重不匹配），变刚度机制可能无法完全补偿，需手动调整 $\gamma$ 参数或引入额外的运动学约束。

4. **接触力精度**：尽管接触图奖励有效抑制了“幽灵”现象，但真实机器人的接触力仍受限于仿真到现实的动力学差距（如关节摩擦、地面反力建模误差），在极高精度力控任务中可能需要额外的在线力反馈。

---

### 6. 关键图表索引

| 图表 | 核心信息 |
|------|----------|
| Table I | IAMR 在四类交互场景中实现 0% 穿透，Inter-X 上 F1-Strict 超 DOR 43% |
| Table II | 完整消融：交互图奖励、接触图奖励、同伴观测的因果贡献 |
| Table III | 真实机器人 Hug 成功率 86.7% vs 单智能体 26.7% |
| Fig. 4 | 重定向定性对比：IAMR 消除穿透与“空气握手” |
| Fig. 5 | 策略行为定性对比：揭示“幽灵”效应与物理接触差异 |
| Fig. 6 | 鲁棒性测试：抵抗推、拉、踢等外部扰动 |
| Table IV | IGRL 完整奖励项与权重配置 |
| Table V | 域随机化参数配置 |

### 补充图表

![[assets/figures/papers/paper_list_l1705_Rhythm_Learning_Interactive_Whole_Body_Control_for_Dual_Humanoids/figures/005_Table.jpg]]
*Table: I: Quantitative Results of Retargeting. Comparison across four interaction categories. Metrics include Safety (IPR, MPD), Fidelity (IEE, F1), and Utility (DSR). IAMR achieves the best balance, strictly eliminating penetration (IPR=0) while maximizing contact F1 scores. TABLE II: Quantitative Results of Policy. We evaluate the contribution of each component. Our full method achieves the most robust balance, effectively integrating coarse-grained geometric alignment (low IEE) with fine-grained physical contact fidelity (high CSR)*

![[assets/figures/papers/paper_list_l1705_Rhythm_Learning_Interactive_Whole_Body_Control_for_Dual_Humanoids/figures/007_Table.jpg]]
*Table: III: Main Results for Real Robot Experiments. We conducted 10 trials for each task and evaluated success based on contact establishment at specific keyframes (K frames per trial)*

![[assets/figures/papers/paper_list_l1705_Rhythm_Learning_Interactive_Whole_Body_Control_for_Dual_Humanoids/figures/010_Table.jpg]]
*Table: IV: Reward Terms and Weights used in IGRL TABLE V: Domain Randomization Parameters*

## 方法谱系与知识库定位

### 1. 问题定位：从单智能体全身控制到双人形交互耦合动力学

Rhythm 所解决的核心问题处于**人形机器人全身控制**与**多智能体物理交互**的交叉地带。传统的人形机器人运动重定向与强化学习控制主要聚焦于单智能体设定——将人类运动映射到单个机器人并学习其全身跟踪策略。当场景扩展至双人形机器人时，出现两个根本性瓶颈：

1. **运动学冲突**：从人类交互数据到双人形机器人的映射中，异构形态导致自身运动保真度与交互几何一致性不可兼得。标准方法将两个机器人视为独立单体（如 **GMR**）或统一整体（如 **DOR**，扩展自 OmniRetarget），无法区分自身约束与交互约束，导致穿透（penetration）或接触丢失（"air handshakes"）。
2. **耦合动力学**：物理接触引入的复杂耦合动力学使得多智能体全身控制在真实世界中难以稳定实现。单智能体基线（**Single Agent**）仅跟踪自身参考运动，忽略同伴状态与交互目标，在协作任务中几乎无法成功（Collaborate 任务 ISR 仅 18.7%，Table II）。

### 2. 方法谱系中的关键锚点

Rhythm 的方法贡献可定位于以下技术谱系：

#### 2.1 运动重定向：从笛卡尔空间跟踪到拓扑解耦优化

| 方法 | 核心机制 | 交互建模方式 | 关键局限 |
|------|----------|-------------|----------|
| **GMR** | 标准笛卡尔空间重定向 | 将双机器人视为独立单体，无交互约束 | 完全忽略交互几何，导致穿透与接触丢失 |
| **OR** (OmniRetarget) | 交互网格（I-Mesh）保持个体身体拓扑 | 仅建模单智能体自身拓扑，缺乏跨智能体交互边 | 在密集接触场景中穿透率高达 47.3%（Table I, Intensive Contact） |
| **DOR** (Dual-OmniRetarget) | 统一交互网格包含所有身体节点 | 构建全局网格但不区分自身边与交互边 | 强制统一参考导致姿势僵硬，接触 F1 仅 0.589（Inter-X, Table I） |
| **IAMR** (Rhythm) | 解耦优化：自身边匹配独立参考，交互边匹配统一参考 | 显式拓扑划分 + 距离依赖变刚度弹簧 | — |

IAMR 的关键创新在于**拓扑解耦**：将交互网格 $\mathcal{E}$ 显式划分为自身边 $\mathcal{E}_{self}$（匹配独立流形 $\mathcal{M}_{ind}$）与交互边 $\mathcal{E}_{inter}$（匹配统一流形 $\mathcal{M}_{uni}$），并通过距离依赖的指数衰减刚度 $\omega_{ij}(d_{ij}) = \omega_{max} \cdot e^{-\gamma d_{ij}}$ 实现自适应平衡。这一设计使得近距离接触时刚度大以保证几何一致性，远处则松弛以保留自身运动风格。

**证据强度**：Table I 显示 IAMR 在 Intensive Contact 场景下完全消除穿透（IPR=0%），而 OR 的 IPR 为 47.3%；在跨数据集泛化（Inter-X）上，IAMR 的严格接触 F1 分数比 DOR 提高 43%（0.843 vs 0.589）。这些结果直接验证了解耦优化对解决运动学冲突的有效性。

#### 2.2 强化学习控制：从独立跟踪到图引导的多智能体耦合学习

| 方法 | 观测空间 | 奖励函数 | 关键局限 |
|------|----------|----------|----------|
| **Single Agent** | 仅自身状态，忽略同伴 | 自身关节跟踪奖励 | 无交互感知，Collaborate 任务 ISR 仅 18.7% |
| **Ours w/o Peer Obs** | 置零同伴观测 $o_{peer}$ | 完整图奖励 | 丧失闭环同步能力，Light Contact CSR 降至 18.6% |
| **Ours w/o Contact Rew** | 完整观测 | 移除物理接触图奖励 $r_{contact}$ | 产生"幽灵"效应：几何精度高（ISR 93.4%）但无真实物理接触（CSR 52.1%） |
| **Ours w/o Interaction Rew** | 完整观测 | 移除空间交互图奖励 $r_{inter}$ | 所有指标大幅下降，Collaborate ISR 从 92.9% 降至 58.1% |
| **IGRL** (Rhythm) | ego-centric 同伴感知 + 完整图奖励 | 交互图奖励 + 接触图奖励（混合） | — |

IGRL 在 **MAPPO** 多智能体框架基础上引入两个关键设计：

- **ego-centric 同伴感知**：观测 $o_{peer}$ 包含相对位置 $P_{rel}$、相对朝向 $R_{rel}$ 及同伴关节位置，使策略具备闭环同步能力。
- **图引导奖励**：交互图奖励 $r_{inter}$ 继承 IAMR 的动态权重以强制空间对齐；接触图奖励 $r_{contact}$ 采用混合设计（激活接触误差 + 未激活接触抑制），同时保证接触一致性并正则化接触力。

**证据强度**：Table II 的消融实验构成完整的因果链——移除交互图奖励导致所有指标崩溃，移除接触图奖励导致"幽灵"现象（Fig. 5 定性展示），移除同伴观测使紧耦合交互几乎无法完成。完整 IGRL 在 Light Contact 的 CSR 达 78.0%，Collaborate 的 ISR 达 92.9%。

#### 2.3 真实部署：从仿真到物理双机器人的同步与定位

真实部署模块解决两个仿真中不存在的挑战：

- **相对状态估计**：通过 LiDAR-IMU 融合的层次化定位系统（Point-LIO + GICP + KF）提供全局位姿，弥补仿真中全局可观测性与真实系统之间的差距。
- **代理间软同步**：采用相位比例反馈 $\dot{\phi}_{ego} = 1.0 + k (\phi_{peer} - \phi_{ego})$ 实现时间对齐，避免因两机器人异步执行导致的交互失败。

**证据强度**：真实机器人实验中，Rhythm 在 Hug 任务的成功率达 86.7%，而单智能体基线仅 26.7%（Table III, 10 次试验平均）。Fig. 6 展示了策略对外部扰动（推、拉、踢）的鲁棒恢复能力。

### 3. 适用边界与局限

#### 3.1 已知适用条件

- **双智能体设定**：当前系统仅验证了双人形机器人交互，尚未扩展至三个或更多智能体。
- **预构建地图依赖**：真实部署依赖预构建的 LiDAR 地图进行全局定位，限制了在未知或动态环境中的即时部署能力。
- **人形形态假设**：IAMR 的解耦优化假设源数据与目标机器人之间存在可映射的骨骼拓扑，当形态差异极大时（如人类到手部高度特化的机器人），重定向质量需要进一步验证。

#### 3.2 开放问题

1. **无地图自我中心感知**：如何实现完全无地图的自我中心感知定位，以支持在开放世界中即时协作？
2. **多智能体扩展**：该方法如何扩展至三个或更多人形机器人的复杂交互场景，并处理更复杂的拓扑变化（如多人协作搬运）？
3. **跨形态泛化**：当源人机形态差异极大时，重定向的解耦优化是否仍能保持交互几何？基于图的奖励能否推广到其他类型的多机器人协同任务（如人-机器人物体操纵）？
4. **动态交互拓扑**：当前交互图结构在重定向阶段静态提取，对于交互拓扑动态变化的场景（如交替握手与分离），如何实现在线拓扑更新？

### 4. 知识库定位总结

Rhythm 在以下维度对领域知识库做出贡献：

- **概念层面**：首次显式建模并解耦自身运动结构与交互几何结构，揭示拓扑划分是解决人类到人形机器人交互迁移中运动学冲突的核心机制。
- **方法层面**：提供了一套完整的 pipeline（IAMR → IGRL → 真实部署），其中距离依赖变刚度优化和图引导强化学习可作为通用模块嵌入其他多智能体物理交互系统。
- **实证层面**：通过 MAGIC 数据集（约 3 小时高质量交互数据，覆盖 5 个语义类别）和真实机器人实验，建立了双人形机器人交互控制的基准，证明了从人类演示到物理机器人交互的可行性。

## 原文 PDF

![[paperPDFs/arxiv_2026/Rhythm_Learning_Interactive_Whole_Body_Control_for_Dual_Humanoids.pdf]]
