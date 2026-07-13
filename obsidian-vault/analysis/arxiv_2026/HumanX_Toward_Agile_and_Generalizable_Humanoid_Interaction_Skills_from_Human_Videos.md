---
title: "HumanX: Toward Agile and Generalizable Humanoid Interaction Skills from Human Videos"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/HumanX_Toward_Agile_and_Generalizable_Humanoid_Interaction_Skills_from_Human_Videos.pdf
project_link: https://wyhuai.github.io/human-x/
code_link: null
aliases:
- HumanX
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将范式从追求精确三维重建转向基于物理规则的交互轨迹合成，从而能够从单个人类视频中生成大规模、物理一致且多样化的交互数据。
primary_logic: 对于机器人技能获取，物理上合理的交互远比光度学上精确的重建更为重要；这种优先级转换使得高效的数据增强和强烈的泛化能力成为可能。
claims:
- HumanX 在三个代表性任务上的平均泛化成功率（GSR）比先前最佳方法 HDMI 高出超过 8 倍。
- 在篮球接球投篮任务上，HumanX + Tea-Stu 的 GSR 为 64.7%，而 HDMI 仅为 2.4%。
- 在实体 Unitree G1 人形机器人上，无需外部感知即可实现平均成功率超过 80% 的篮球技能，且每个技能仅从单个视频演示学习。
- Basketball Catch-Shot 上 GSR (Generalization Success Rate) = 64.7% (XMimic + Tea-Stu)
---

# HumanX: Toward Agile and Generalizable Humanoid Interaction Skills from Human Videos

> [!tip] 核心洞察
> 对于机器人技能获取，物理上合理的交互远比光度学上精确的重建更为重要；这种优先级转换使得高效的数据增强和强烈的泛化能力成为可能。

| 字段 | 内容 |
|------|------|
| 中文题名 | HumanX：从人类视频实现敏捷且可泛化的人形机器人交互技能 |
| 英文题名 | HumanX: Toward Agile and Generalizable Humanoid Interaction Skills from Human Videos |
| 会议/期刊 | arXiv 2026 |
| Links | [Project](https://wyhuai.github.io/human-x/) · [paper](https://arxiv.org/abs/2602.02473) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | HumanX |
| Dataset | Basketball Catch-Shot, Badminton Hitting, Cargo Pickup |

> [!tip] 效果简介
> - Basketball Catch-Shot 上，GSR (Generalization Success Rate) 64.7% (XMimic + Tea-Stu) vs 2.4% (HDMI) (+62.3%)。
> - Badminton Hitting 上，GSR 90.6% (XMimic + Tea-Stu) vs 25.3% (HDMI) (+65.3%)。
> - Cargo Pickup 上，GSR 96.3% (XMimic + Tea-Stu) vs 1.8% (HDMI) (+94.5%)。

## 概要

**问题与瓶颈**：人形机器人要习得敏捷、可泛化的交互技能（如篮球、羽毛球、货物搬运），核心瓶颈并非运动控制本身，而是缺乏大规模、物理合理且多样化的交互数据。现有方法要么依赖稀缺的真实交互数据，要么需要为每一项任务精心设计特定奖励函数，难以扩展到多样化的交互技能。

**核心洞察与范式转换**：HumanX 的出发点是一个关键判断——对于机器人技能获取，**物理上合理的交互远比光度学上精确的重建更为重要**。基于此，HumanX 将范式从“追求精确三维重建”转向“基于物理先验的交互轨迹合成”，从而能够从单个人类视频中生成大规模、物理一致且多样化的交互数据。这一优先级转换是后续高效数据增强和强泛化能力的根本原因。

**方法定位**：HumanX 由两个协同设计的组件构成：**XGen**（数据生成管道）和 **XMimic**（统一模仿学习框架）。XGen 从人类视频中提取运动、重定向到机器人，并在物理约束下合成物体交互轨迹，同时支持可扩展的数据增强；XMimic 则通过两阶段教师-学生训练和统一的任务无关交互模仿奖励，学习可泛化的交互策略。在方法谱系中，HumanX 区别于基于精确重建的管线（如 **HDMI**，Weng et al., arXiv 2025）和需要逐任务奖励设计的方案，转而建立了一条以物理合成数据驱动、统一奖励驱动的新路径。

**主要结果**：
- **仿真泛化**：在篮球接球投篮、羽毛球击球、货物拾取三个代表性任务上，HumanX 的平均泛化成功率（GSR）比先前最佳方法 HDMI 高出超过 8 倍（Table I）。其中篮球接球投篮 GSR 从 HDMI 的 2.4% 提升至 64.7%，羽毛球击球从 25.3% 提升至 90.6%，货物拾取从 1.8% 提升至 96.3%。
- **真实机器人验证**：在实体 Unitree G1 人形机器人上，无需外部感知（NEP 模式）即可实现平均成功率超过 80% 的篮球技能，且每个技能仅从单个视频演示学习（Table III）。
- **消融关键发现**：XGen 的数据增强是泛化能力的关键来源——仅加入数据增强即可将篮球接球投篮 GSR 从 4.9% 提升至 60.6%（Table I）。

**局限与开放问题**：无外部感知模式无法处理非接触交互（如接飞行中的球）；部署依赖特定 IMU/MoCap 硬件；当前系统主要处理相对简单的单物体操作。未来方向包括扩展到完全依赖视觉感知的零样本部署、利用更大规模互联网人类视频提升技能多样性，以及在更复杂的多接触、动态场景中弥合 Sim-to-Real 差距。



### 人形机器人交互技能的困境

使通用人形机器人在现实世界中执行敏捷、多样化的物体交互技能，是具身智能领域的核心目标之一。然而，当前方法在这一目标面前面临根本性的瓶颈：**真实交互数据的极度稀缺**。与导航或简单抓取不同，全身动态交互（如接球投篮、羽毛球击球、足球踢球）需要精确的全身协调、物体动态感知和物理一致性，这使得数据采集成本极高。

现有方法主要沿两条路径尝试解决这一问题。第一条路径依赖于**精确的三维重建**，即从人类视频中估计人体和物体的运动轨迹，然后将其直接组合并重定向到机器人上，如 **SkillMimic**（Wang et al., CVPR 2025）和 **OmniRetarget**（Yang et al., arXiv 2025）。第二条路径则通过**精心设计的任务特定奖励函数**来训练强化学习策略，如 **HDMI**（Weng et al., arXiv 2025）。然而，这两种范式都存在固有的局限性：

- **重建路径的脆弱性**：从单目视频中精确重建人体和物体的三维运动本身就是一个极具挑战性的问题。重建误差会直接传递到机器人的控制策略中，导致物理上不可行的交互轨迹。更重要的是，这种方法本质上是“复制”而非“理解”交互——它无法泛化到与原始演示不同的物体位置、轨迹或目标。
- **奖励设计的不可扩展性**：为每个新任务手动设计奖励函数需要大量的领域知识和反复试错。当任务涉及多样化的交互模式（如足球的推射、挑射、弧线球）时，设计一套能覆盖所有模式的奖励几乎是不可能的。

### 核心洞察：范式转换

HumanX 的提出基于一个关键洞察：**对于机器人技能获取而言，物理上合理的交互远比光度学上精确的重建更为重要**。这一优先级转换带来了根本性的范式变化——从“精确重建后模仿”转向“在物理约束下合成交互轨迹”。

这一洞察的因果逻辑在于：机器人最终执行的是物理世界中的交互行为，而非像素级的运动复现。只要生成的交互轨迹满足物理定律（如接触力、动量守恒、力封闭）并且在语义上与原始演示一致，机器人就能学到可泛化的技能。更重要的是，这种基于物理先验的合成方法天然支持数据增强——通过改变物体几何形状、接触轨迹和非接触阶段的速度分布，可以从单个视频中生成大规模、多样化的训练数据。

### 技术挑战

实现这一范式转换需要解决三个核心挑战：

1. **从单目视频到物理一致交互数据的转换**：如何从仅包含二维投影信息的视频中提取三维人体运动，并在物理模拟器中合成与之协调的物体交互轨迹？
2. **统一的交互模仿学习**：如何设计一个任务无关的奖励机制，使其能够驱动策略学习从篮球到羽毛球到货物搬运等截然不同的交互技能？
3. **灵活的真实世界部署**：如何使策略既能利用外部感知（如动作捕捉系统）实现高精度交互，又能在无外部感知的条件下仅凭本体感受完成动态技能？

HumanX 通过两个协同设计的组件——**XGen**（数据生成管道）和 **XMimic**（统一模仿学习框架）——系统性地回应了这些挑战，从而实现了从单个人类视频到多样化、可泛化人形机器人交互技能的端到端流程。



## 核心方法与创新机理

### 范式转换：从视觉重建到物理交互合成

HumanX 的核心洞察在于对机器人技能获取目标的重新定义——**物理上合理的交互远比光度学上精确的重建更为重要**。这一优先级转换直接改变了数据合成范式：

- **Baseline 路径**：现有方法（如 **SkillMimic**（Wang et al., CVPR 2025）、**HDMI**（Weng et al., arXiv 2025））依赖从人类视频中精确估计人体与物体的三维运动，再将其直接组合为机器人交互轨迹。这一路径受限于真实交互数据的稀缺性，且对估计误差高度敏感。
- **HumanX 路径**：XGen 从根本上抛弃了“精确重建”的目标，转而**基于物理先验合成交互轨迹**。具体而言，在接触阶段利用锚点（如双手掌中点）与物体的相对位姿不变性，通过力封闭优化生成物理一致的物体轨迹；在非接触阶段则使用物理模拟器生成物体运动。这使得从单个视频即可生成大规模、物理一致且多样化的交互数据。

这一范式转换带来的因果效应是：数据稀缺瓶颈被打破，泛化能力显著增强。消融实验表明，仅加入 XGen 数据增强（+Data Aug），篮球接球投篮任务的泛化成功率（GSR）便从 4.9% 跃升至 60.6%（Table I），证明了数据增强是泛化能力的关键来源。

### 统一的任务无关奖励设计

传统方法需要为每个交互任务精心设计特定的奖励函数，导致难以扩展到多样化的技能。HumanX 的 XMimic 框架引入了一套**统一的任务无关的交互模仿奖励**（Section IV.C）：

$$r _ { t } = r _ { t } ^ { \mathrm { b o d y } } + r _ { t } ^ { \mathrm { o } \tilde { \mathrm { b j } } } { + } r _ { t } ^ { \mathrm { r e l } } { + } r _ { t } ^ { c } { + } r _ { t } ^ { \mathrm { r e g } }$$

该复合奖励由五个组件构成：
- **身体模仿奖励**（$r_t^{\mathrm{body}}$）：跟踪身体位置、旋转、关节位置及速度，并引入对抗运动先验（AMP）以保证动作自然性。
- **物体奖励**（$r_t^{\mathrm{obj}}$）：衡量物体位姿的跟踪精度。
- **相对运动奖励**（$r_t^{\mathrm{rel}}$）：约束机器人关键身体部位与物体的相对运动关系。
- **接触图奖励**（$r_t^c$）：监督接触状态的匹配。
- **正则化奖励**（$r_t^{\mathrm{reg}}$）：防止策略产生异常动作。

这一统一奖励方案使得同一框架能够处理篮球、羽毛球、足球、货物拾取等多种交互技能，无需针对每个任务重新设计奖励函数。

### 灵活的双模式感知部署

现有方法（如 HDMI）在部署时通常依赖外部物体跟踪（真值或完美感知），限制了真实场景的适用性。HumanX 的 XMimic 支持两种灵活的部署模式（Section IV.B.2）：

- **无外部感知模式（NEP）**：完全依赖本体感受（proprioception）控制物体。其理论依据在于浮动基座人形机器人的动力学方程（Eq. 13）：

  $$\boldsymbol \tau = \mathbf { M } ( \mathbf { q } ) \ddot { \mathbf { q } } + \mathbf { C } ( \mathbf { q } , \dot { \mathbf { q } } ) \dot { \mathbf { q } } + \mathbf { G } ( \mathbf { q } ) + \boldsymbol \tau _ { f } + \mathbf { J } _ { \mathrm { e x t } } ^ { \top } \mathbf { F } _ { \mathrm { e x t } }$$

  外部力 $\mathbf{F}_{\mathrm{ext}}$ 通过雅可比矩阵映射到关节力矩，因此机器人可以通过本体感受间接感知物体交互状态。在实体 Unitree G1 机器人上，NEP 模式实现了平均超过 80% 的篮球技能成功率（Table III）。

- **MoCap 模式**：利用动作捕捉系统感知物体或人体运动，并在训练中引入模拟的信号丢失（frame loss），使策略对感知中断具有鲁棒性。消融实验（Fig. 12）表明，若训练中不模拟 MoCap 信号丢失，机器人在信号暂时丢失时会直接崩溃。

### Teacher-Student 两阶段训练

XMimic 采用 Teacher-Student 两阶段训练范式（Section IV.A），进一步提升了多模式技能的泛化能力：

- **第一阶段**：教师策略使用特权信息（包括物体真值状态、接触标签等）在统一交互模仿奖励下训练，掌握单个技能。
- **第二阶段**：通过行为克隆损失将教师策略蒸馏为学生策略：

  $$\mathcal { L } _ { \mathrm { B C } } = \mathbb { E } _ { ( s , i ) \sim \mathcal { G } } \left[ \| \pi _ { \mathrm { s u } } ( \boldsymbol { a } \mid s ) - \pi _ { \mathrm { t e a } } ^ { i } ( \boldsymbol { a } \mid s ) \| ^ { 2 } \right]$$

  学生策略在现实感知约束下运行，仅使用本体感受或带噪声的 MoCap 信号。

该方案的效果在足球踢球等多模式技能上尤为显著：加入 Teacher-Student 后，GSR 从 74.2% 提升至 93.1%（Table II），表明蒸馏过程有效将特权信息转化为可部署策略的隐式知识。

### 创新总结

HumanX 的三项核心创新——物理先验驱动的数据合成、统一任务无关奖励、灵活双模式部署——构成了一条完整的因果链：**范式转换使得从单个人类视频生成大规模多样化交互数据成为可能，统一奖励使得同一框架覆盖多种技能，双模式部署则弥合了从仿真到真实世界的感知差距**。这一组合使 HumanX 在三个代表性任务上的平均泛化成功率比先前最佳方法高出超过 8 倍（Table I）。



HumanX 提出了一套从单目人类视频到可部署人形机器人交互技能的完整流水线，其核心设计理念是**将范式从追求精确三维重建转向基于物理先验的交互轨迹合成**。系统由两个协同设计的组件构成：

- **XGen**：数据生成管道，负责从人类演示视频中合成物理上合理的人形交互数据，并支持可扩展的数据增强。
- **XMimic**：统一的模仿学习框架，利用 XGen 生成的数据学习可泛化的交互技能，并通过教师-学生蒸馏实现可部署策略。

### 数据生成管道（XGen）

XGen 的输入是一段包含人-物交互的单目 RGB 视频，输出是物理一致的人形机器人交互轨迹数据。其处理流程分为三个阶段（见 Fig. 2）：

1. **人体运动提取与重定向**（Section III.A）：使用 GVHMR 从视频中估计基于 SMPL 的 3D 人体姿态序列 $\mathbf{h}_i = (\mathbf{h}_i^{\mathrm{root}}, \mathbf{h}_i^{\mathrm{joint}})$，其中 $\mathbf{h}_i^{\mathrm{root}} \in \mathbb{R}^6$ 为根姿态，$\mathbf{h}_i^{\mathrm{joint}}$ 为 $J$ 个 SMPL 关节的 3D 旋转。随后通过 GMR 将人体姿态重定向到目标人形机器人的形态学空间，得到机器人姿态序列 $\mathbf{r}_i = (\mathbf{r}_i^{\mathrm{root}}, \mathbf{r}_i^{\mathrm{joint}})$，其中 $\mathbf{r}_i^{\mathrm{root}} \in \mathbb{R}^6$，$\mathbf{r}_i^{\mathrm{joint}}$ 为 $N$ 个机器人关节的 1D 旋转。

2. **基于物理的交互轨迹合成**（Section III.B）：将视频序列分割为接触阶段和非接触阶段，采用不同的物理先验合成物体轨迹：
   - **接触阶段**：利用预定义锚点（如双手掌中点）与物体之间相对姿态的不变性，基于锚点在世界坐标系中的运动推导物体的刚性变换；同时对接触力进行力封闭优化，确保合成轨迹的物理可行性。
   - **非接触阶段**：使用物理模拟器，以估计的初始线速度和角速度作为初值，模拟物体在重力等外力作用下的自由运动轨迹。

3. **交互数据增强**（Section III.C）：为提升策略的泛化能力，XGen 在合成数据上施加系统性的增强：
   - **物体几何缩放**：随机缩放物体尺寸（见 Fig. 3）。
   - **接触阶段轨迹变换**：对接触阶段的物体轨迹施加平移和旋转扰动（见 Fig. 3）。
   - **非接触阶段速度随机化**：参数化随机化物体的初始速度（见 Fig. 4）。

### 模仿学习框架（XMimic）

XMimic 采用**两阶段教师-学生训练范式**（见 Fig. 5），将 XGen 生成的多样化交互数据转化为可部署的交互策略：

- **第一阶段——教师策略训练**（Section IV.A.1）：教师策略 $\pi_{\mathrm{tea}}$ 以高斯分布 $\pi(\boldsymbol{a}_t \mid \boldsymbol{s}_t) \sim \mathcal{N}(\phi_\pi(\boldsymbol{s}_t), \Sigma_\pi)$ 的形式输出动作，其中均值由 MLP $\phi_\pi$ 预测，协方差 $\Sigma_\pi$ 可学习。教师可访问特权状态信息（如物体真值位姿、速度等），并在**统一的交互模仿奖励**下训练。该奖励函数由五项组成：

$$r_t = r_t^{\mathrm{body}} + r_t^{\mathrm{obj}} + r_t^{\mathrm{rel}} + r_t^{c} + r_t^{\mathrm{reg}}$$

其中 $r_t^{\mathrm{body}}$ 跟踪身体位置、旋转、关节位置及速度（含对抗运动先验 AMP 项以保持动作自然性），$r_t^{\mathrm{obj}}$ 衡量物体位姿跟踪误差，$r_t^{\mathrm{rel}}$ 衡量人-物相对运动误差，$r_t^{c}$ 基于接触图监督接触时序，$r_t^{\mathrm{reg}}$ 为正则化项。该统一奖励设计使框架无需为每个任务单独设计奖励函数，即可准确模仿多样化的复杂交互行为。

- **第二阶段——学生策略蒸馏**（Section IV.A.3）：学生策略 $\pi_{\mathrm{su}}$ 在现实感知约束下运行（支持两种部署模式：无外部感知 NEP 模式和带模拟信号丢失的 MoCap 模式），通过行为克隆损失最小化与教师策略的动作分布差异：

$$\mathcal{L}_{\mathrm{BC}} = \mathbb{E}_{(s,i) \sim \mathcal{G}} \left[ \| \pi_{\mathrm{su}}(\boldsymbol{a} \mid s) - \pi_{\mathrm{tea}}^i(\boldsymbol{a} \mid s) \|^2 \right]$$

此外，框架通过**扰动初始化**（Disturbed Initialization, +DI）和**交互终止**（Interaction Termination, +IT）机制增强泛化能力：+DI 在 episode 开始时随机扰动物体位姿，迫使策略适应非理想初始条件；+IT 在接触阶段监控物体与关键身体部位的相对位置误差，超过阈值时以一定概率终止 episode，使策略专注于交互成功。

### 输入输出流总结

整个 HumanX 系统的端到端信息流为：

| 阶段 | 输入 | 输出 | 核心模块 |
|------|------|------|----------|
| 数据生成 | 单目人类交互视频 | 物理一致的人形交互轨迹（含增强变体） | XGen（GVHMR → GMR → 物理合成 → 增强） |
| 策略学习 | 增强后的人形交互数据 | 可部署的学生策略 | XMimic（教师训练 → 蒸馏 → 学生策略） |
| 真实部署 | 本体感受（NEP）或 MoCap 信号 | 人形机器人关节力矩指令 | 蒸馏后的学生策略 |

这一设计使得 HumanX 能够从**单个**人类视频演示出发，生成大规模、物理一致且多样化的训练数据，并学习出在仿真和真实环境中均展现出强烈泛化能力的交互技能。

### 补充图表

![[assets/figures/papers/paper_list_l1703_HumanX_Toward_Agile_and_Generalizable_Humanoid_Interaction_Skills_from_H/figures/001_Figure_1.jpg]]
*Figure 1: HumanX enables diverse interaction skills through two core components. XGen synthesizes and augments humanoid interaction data from human video, which XMimic then uses to learn generalizable interaction skills. This results in autonomous interaction behaviors such as diverse basketball skills, consecutive football kicking, generalizable cargo pickup, and real-time counterattack against a human*



HumanX 的系统架构由两个协同设计的核心组件构成：**XGen**（数据生成管道）和 **XMimic**（统一模仿学习框架）。XGen 负责从单目人类视频中合成物理合理的人形交互数据，XMimic 则利用这些数据学习可泛化的交互技能策略。以下分别阐述两个组件的关键模块及其核心公式。

### XGen：基于物理先验的交互数据合成

XGen 的核心设计理念是将范式从“追求精确三维重建”转向“基于物理规则的交互轨迹合成”。这一定位转变使得从单个人类视频中生成大规模、多样化且物理一致的交互数据成为可能。

#### 人体运动提取与重定向

给定一段包含 $K$ 帧的单目 RGB 视频，XGen 首先使用 **GVHMR** 估计 3D 人体姿态序列，随后通过 **GMR** 将其重定向到目标人形机器人的形态结构。

第 $i$ 帧的 3D 人体姿态表示为：
$$
\mathbf{h}_i = \left( \mathbf{h}_i^{\mathrm{root}}, \mathbf{h}_i^{\mathrm{joint}} \right), \quad i = 1, \ldots, K \tag{1}
$$
其中 $\mathbf{h}_i^{\mathrm{root}}$ 为 6D 根姿态（全局位置与朝向），$\mathbf{h}_i^{\mathrm{joint}}$ 为 $J$ 个 SMPL 关节的 3D 旋转。

重定向后的机器人姿态序列为：
$$
\mathbf{r}_i = \left( \mathbf{r}_i^{\mathrm{root}}, \mathbf{r}_i^{\mathrm{joint}} \right), \quad i = 1, \ldots, K \tag{2}
$$
其中 $\mathbf{r}_i^{\mathrm{root}}$ 为机器人根部的 6D 姿态，$\mathbf{r}_i^{\mathrm{joint}}$ 为 $N$ 个机器人关节的 1D 旋转。

#### 基于物理的交互轨迹合成

XGen 将视频分割为接触阶段（contact phase）和非接触阶段（non-contact phase），并采用不同的物理规则合成物体轨迹。

**接触阶段**：利用预定义锚点（如双手掌中点）与物体之间相对姿态的不变性来合成物体轨迹。在锚点与物体保持接触的帧区间内，物体的世界姿态由锚点姿态和固定的相对变换关系确定。合成后，XGen 进一步执行力封闭（force-closure）优化，确保接触配置在物理上可行。

**非接触阶段**：当物体脱离接触时，XGen 使用物理模拟器根据初始状态（位置和速度）生成物体的自由运动轨迹，保证轨迹满足牛顿力学约束。

#### 交互数据增强

为提升策略的泛化能力，XGen 在合成数据的基础上施加三种增强策略（Fig. 3、Fig. 4）：

![[assets/figures/papers/paper_list_l1703_HumanX_Toward_Agile_and_Generalizable_Humanoid_Interaction_Skills_from_H/figures/003_Figure_3.jpg]]
*Figure 3: Data Augmentation for Contact Phase*

![[assets/figures/papers/paper_list_l1703_HumanX_Toward_Agile_and_Generalizable_Humanoid_Interaction_Skills_from_H/figures/004_Figure_4.jpg]]
*Figure 4: Data Augmentation for Non-Contact Phase*

1. **物体几何缩放**：在接触阶段随机缩放物体尺寸。
2. **接触阶段轨迹变换**：对接触阶段物体的相对轨迹施加平移和旋转变换。
3. **非接触阶段速度随机化**：在非接触阶段对物体的初始速度进行参数化随机采样。

这些增强操作与领域随机化（domain randomization）相结合，使策略能够适应未见过的物体尺寸、质量和运动轨迹。

### XMimic：统一模仿学习框架

XMimic 采用两阶段教师-学生训练范式（Fig. 5）：第一阶段利用特权信息训练教师策略，第二阶段通过行为克隆将教师策略蒸馏为可在真实约束下部署的学生策略。

![[assets/figures/papers/paper_list_l1703_HumanX_Toward_Agile_and_Generalizable_Humanoid_Interaction_Skills_from_H/figures/005_Figure_5.jpg]]
*Figure 5: XMimic follows a two-stage training pipeline. In the Stage 1, a teacher policy is learned with privileged state information under a unified interaction-imitation reward. In Stage 2, the teacher is distilled into a student policy that operates under realistic perceptual constraints, combining interaction imitation with behavior cloning. The resulting student policy can be deployed directly in real-world settings*

#### 策略参数化

策略输出被参数化为高斯分布：
$$
\pi ( \boldsymbol { a } _ { t } \mid \boldsymbol { s } _ { t } ) \sim \mathcal { N } ( \phi _ { \pi } ( \boldsymbol { s } _ { t } ) , \Sigma _ { \pi } ) \tag{3}
$$
其中 $\phi_{\pi}$ 为 MLP 网络，预测给定状态 $\boldsymbol{s}_t$ 下的动作均值；$\Sigma_{\pi}$ 为可学习的协方差矩阵，刻画动作的探索范围。

#### 教师-学生蒸馏

第二阶段的行为克隆损失定义为学生策略与教师策略动作分布之间的 $L_2$ 距离期望：
$$
\mathcal { L } _ { \mathrm { B C } } = \mathbb { E } _ { ( s , i ) \sim \mathcal { G } } \left[ \| \pi _ { \mathrm { s u } } ( \boldsymbol { a } \mid s ) - \pi _ { \mathrm { t e a } } ^ { i } ( \boldsymbol { a } \mid s ) \| ^ { 2 } \right] \tag{4}
$$
其中 $\mathcal{G}$ 为教师策略的经验回放缓冲区，$i$ 为技能索引。该损失使学生策略在多技能场景下复现教师的行为分布。

#### 统一交互模仿奖励

XMimic 设计了一套任务无关的统一奖励函数，无需为每个交互任务单独设计奖励。总奖励由五项加权组合而成：
$$
r _ { t } = r _ { t } ^ { \mathrm { b o d y } } + r _ { t } ^ { \mathrm { o } \tilde { \mathrm { b j } } } { + } r _ { t } ^ { \mathrm { r e l } } { + } r _ { t } ^ { c } { + } r _ { t } ^ { \mathrm { r e g } } \tag{5}
$$
各项含义如下：

- **$r_t^{\mathrm{body}}$**：身体模仿奖励，跟踪身体位置、旋转、关节位置及其速度，并包含对抗运动先验（AMP）项以保持动作自然度。
- **$r_t^{\mathrm{obj}}$**：物体模仿奖励，衡量物体位置和旋转与参考轨迹的误差。
- **$r_t^{\mathrm{rel}}$**：相对运动奖励，衡量机器人与物体之间相对位姿的跟踪精度。
- **$r_t^{c}$**：接触图奖励，监督机器人关键部位与物体的接触状态是否与参考一致。
- **$r_t^{\mathrm{reg}}$**：正则化奖励，包括动作平滑项和能量惩罚项，抑制抖动并提高策略的物理合理性。

#### 灵活部署的感知模式

XMimic 支持两种部署模式以适应不同的感知条件：

- **无外部感知模式（NEP）**：完全不依赖外部物体跟踪，仅利用本体感受（proprioception）控制物体。其理论基础在于浮动基座人形机器人的动力学方程：
  $$
  \boldsymbol \tau = \mathbf { M } ( \mathbf { q } ) \ddot { \mathbf { q } } + \mathbf { C } ( \mathbf { q } , \dot { \mathbf { q } } ) \dot { \mathbf { q } } + \mathbf { G } ( \mathbf { q } ) + \boldsymbol \tau _ { f } + \mathbf { J } _ { \mathrm { e x t } } ^ { \top } \mathbf { F } _ { \mathrm { e x t } } \tag{13}
  $$
  该方程表明，外部接触力 $\mathbf{F}_{\mathrm{ext}}$ 通过雅可比矩阵 $\mathbf{J}_{\mathrm{ext}}$ 反映在关节力矩中，因此机器人可通过本体感受间接推断物体状态。这一模式适用于接触密集型技能（如运球、投篮）。

- **MoCap 模式**：引入动作捕捉系统提供物体或人体的位姿信息，但训练时模拟真实的信号丢失（frame loss），使策略在感知信号间歇性缺失时仍能保持鲁棒。该模式适用于需要精确空间感知的非接触交互（如接球、羽毛球击球）。

### 补充图表

![[assets/figures/papers/paper_list_l1703_HumanX_Toward_Agile_and_Generalizable_Humanoid_Interaction_Skills_from_H/figures/002_Figure_2.jpg]]
*Figure 2: Overview of XGen. The pipeline begins by estimating SMPL-based human motion from video and retargeting it to the humanoid’s morphology. The video is segmented into contact and non-contact phases. For the contact phase, a predefined anchor (e.g., the midpoint between the two palms) is used. The object mesh and its relative pose to the anchor are estimated from a keyframe (or defined manually). The object trajectory is then generated by transforming the object according to the anchor’s pose over time, followed by force-closure optimization to refine the robot poses. During the non-contact phases, diverse and physically plausible object trajectories are generated via simulation. Complete inter...*



## 实验与关键发现

### 核心瓶颈与实验动机

现有从人类视频学习人形机器人交互技能的方法面临一个根本性瓶颈：真实交互数据的稀缺性与任务特定奖励函数设计的复杂性之间的矛盾。**SkillMimic**（Wang et al., CVPR 2025）、**OmniRetarget**（Yang et al., arXiv 2025）和**HDMI**（Weng et al., arXiv 2025）等方法要么依赖精确的三维重建来组合人与物体的运动，要么需要为每个交互任务精心设计奖励函数，难以扩展到多样化的交互技能。HumanX 的核心洞察在于：对于机器人技能获取，物理上合理的交互远比光度学上精确的重建更为重要。这一优先级转换使得从单个人类视频中高效生成大规模、物理一致且多样化的交互数据成为可能。

实验设计围绕三个关键问题展开：（1）从单个视频演示出发，HumanX 能否学习到可泛化的交互技能？（2）XGen 的数据增强与 XMimic 的各技术组件对泛化能力的贡献如何？（3）所学的技能能否成功部署到真实人形机器人上？所有仿真实验均基于统一的 Isaac Gym 平台，每个策略使用 16,384 个并行环境在单张 NVIDIA RTX 4090 GPU 上训练 20,000 次迭代，确保比较的公平性。

### 主要仿真结果：泛化能力的定量飞跃

Table I 报告了在篮球接球投篮（Basketball Catch-Shot）、羽毛球击球（Badminton Hitting）和货物拾取（Cargo Pickup）三个代表性任务上的主要结果。评估指标包括：原始数据上的成功率（SR）、泛化成功率（GSR）、物体位置跟踪误差（Eₒ）和关键身体位置跟踪误差（Eₕ）。

**泛化成功率的数量级提升。** 在最具挑战性的泛化指标 GSR 上，完整的 HumanX 系统（XMimic + Tea-Stu）相比先前最佳方法 HDMI 展现出压倒性优势：

- **Basketball Catch-Shot**：GSR 从 HDMI 的 2.4% 跃升至 64.7%，提升幅度超过 25 倍。
- **Badminton Hitting**：GSR 从 25.3% 提升至 90.6%，提升约 3.6 倍。
- **Cargo Pickup**：GSR 从 1.8% 提升至 96.3%，提升超过 50 倍。

三个任务的平均 GSR 提升超过 8 倍，验证了核心论断：从精确重建范式转向物理先验驱动的交互轨迹合成，是解锁泛化能力的关键。值得注意的是，HDMI 在原始数据上的 SR 并不低（如 Cargo Pickup 达到 98.4%），但其 GSR 急剧下降，说明该方法过度拟合了演示中的特定物体轨迹，缺乏对未见物体状态的适应能力。相比之下，HumanX 在保持高原始成功率的同时，GSR 大幅领先，体现了数据增强与统一模仿奖励的协同效应。

**物体跟踪精度的显著改善。** 物体位置跟踪误差 Eₒ 的对比进一步揭示了泛化能力的来源。在 Basketball Catch-Shot 上，HDMI 的 Eₒ 高达 1.105 m，而 XMimic + Tea-Stu 降至 0.141 m；在 Badminton Hitting 上，从 0.689 m 降至 0.079 m。这表明 HumanX 的策略学会了在物体状态偏离演示分布时进行主动调整，而非机械地复现参考轨迹。

### 消融研究：技术组件的贡献分解

Table I 的消融实验逐层揭示了 XMimic 各组件对泛化能力的贡献。以 XMimic Base（仅使用基础身体模仿奖励，无数据增强）为起点，GSR 在 Basketball Catch-Shot 和 Badminton Hitting 上分别仅为 4.9% 和 41.6%。

**数据增强（+Data Aug）是泛化能力的最强驱动力。** 引入 XGen 的数据增强后，Basketball Catch-Shot 的 GSR 从 4.9% 飙升至 60.6%，提升幅度超过 11 倍；Badminton Hitting 从 41.6% 提升至 83.9%。这一结果直接证明了 XGen 的核心价值：通过物体几何缩放、接触阶段轨迹变换和非接触阶段速度随机化（见 Fig. 3 和 Fig. 4），策略在训练期间接触到了远超单个视频所能提供的交互多样性，从而学会了应对未见物体状态的能力。

**扰动初始化（+DI）增强鲁棒性。** 在数据增强基础上加入扰动初始化后，Basketball Catch-Shot 的 GSR 从 4.9% 进一步提升至 13.5%（从 Base 的视角），表明在训练初期引入状态扰动有助于策略探索更优的修正行为。

**交互终止（+IT）引导策略聚焦交互成功。** 交互终止机制在参考帧处于接触状态时监测物体与关键身体部位的相对位置误差，一旦超过阈值则概率性终止回合。这一设计将 Badminton Hitting 的 GSR 从 41.6% 提升至 60.5%（与 Base 相比），因为它迫使策略优先保证交互的成功完成，而非仅仅模仿身体姿态。

**Teacher-Student 方案（+Tea-Stu）进一步提升多模式技能。** Table II 报告了多模式交互技能的评估结果。以足球踢球为例，无 Teacher-Student 方案时 GSR 为 74.2%，加入后提升至 93.1%。教师策略在第一阶段利用特权信息（如精确的物体状态）学习高质量的行为，学生策略通过行为克隆损失 $\mathcal{L}_{\mathrm{BC}} = \mathbb{E}_{(s,i)\sim\mathcal{G}}[\|\pi_{\mathrm{su}}(\boldsymbol{a}\mid s) - \pi_{\mathrm{tea}}^{i}(\boldsymbol{a}\mid s)\|^2]$ 进行蒸馏，在仅使用可部署感知的条件下逼近教师的表现。

### 真实机器人实验：从仿真到实体的技能迁移

Table III 报告了在 Unitree G1 人形机器人上的真实实验定量结果。实验涵盖两种部署模式：无外部感知模式（NEP）和 MoCap 模式。

**NEP 模式：本体感受驱动的盲操作技能。** 在没有任何外部物体感知的条件下，机器人仅依赖本体感受信号（如关节力矩、IMU 数据）完成篮球技能。篮球跳投成功率为 8/10，运球为 7/10，转身后仰跳投为 9/10，平均成功率超过 80%。这一结果验证了 HumanX 的一个关键设计选择：通过动力学方程 $\boldsymbol{\tau} = \mathbf{M}(\mathbf{q})\ddot{\mathbf{q}} + \mathbf{C}(\mathbf{q},\dot{\mathbf{q}})\dot{\mathbf{q}} + \mathbf{G}(\mathbf{q}) + \boldsymbol{\tau}_f + \mathbf{J}_{\mathrm{ext}}^{\top}\mathbf{F}_{\mathrm{ext}}$，外部接触力 $\mathbf{F}_{\mathrm{ext}}$ 会通过雅可比矩阵 $\mathbf{J}_{\mathrm{ext}}^{\top}$ 映射为关节力矩，使得本体感受信号隐式编码了物体交互信息。Fig. 9 展示了机器人在 NEP 模式下完成多种篮球技能的快照，体现了高度动态和复杂的交互能力。

**MoCap 模式：持续交互与泛化。** 当利用 MoCap 系统感知物体或人类运动时，HumanX 实现了持续的交互能力。在羽毛球对打任务中，机器人能够与人类进行多回合的实时对抗（Fig. 10），每个技能仅从单个视频演示学习。这得益于训练阶段模拟了 MoCap 信号丢失（Fig. 12 右），使策略在真实部署中遇到信号短暂丢失时不会崩溃。

**Sim-to-Real 的关键设计。** Fig. 12 揭示了两个对成功迁移至关重要的训练要素：（1）持续随机外力注入：如果训练中不包含持续的随机外力，机器人在真实世界中受到意外扰动时可能失去平衡；（2）MoCap 信号丢失模拟：在训练中模拟感知信号的帧丢失，使策略学会在信号不可靠时依靠本体感受维持稳定，避免真实部署中的崩溃。

### 涌现行为与失败模式

HumanX 展现出超出显式训练的涌现行为。在货物拾取任务中，当研究人员用力踢踹机器人并夺走其手中的物体后，机器人能够自主调整姿态、重新定位并完成拾取（Fig. 11）。这种行为并非通过特定奖励函数设计，而是源于统一模仿奖励中身体、物体、相对运动和接触图的多目标协同优化，以及数据增强带来的分布外适应能力。

![[assets/figures/papers/paper_list_l1703_HumanX_Toward_Agile_and_Generalizable_Humanoid_Interaction_Skills_from_H/figures/012_Figure_11.jpg]]
*Figure 11: Emergent Behaviors. During the execution of the Cargo Pickup skill, a researcher first kicks the robot forcefully, then takes the object from its hand and places it on the ground. The robot demonstrates robust adaptation in response to such complex disturbances*

然而，系统存在明确的失败模式与局限性。NEP 模式无法处理非接触交互（如接住飞行中的篮球），因为本体感受在没有物理接触时无法感知物体状态。此外，当前系统处理相对简单的单个物体操作，对于复杂的多物体、长时间任务尚未验证。真实实验的空间和时间范围有限，部署依赖于特定的 IMU/MoCap 硬件，限制了更广泛场景的验证。

### 开放问题与未来方向

基于当前实验结果，若干开放问题值得进一步探索：（1）如何将该框架扩展到完全依赖视觉感知的零样本真实世界部署，以摆脱对 MoCap 硬件的依赖？（2）能否利用更大规模、更多样的互联网人类视频，进一步提升技能的多样性和鲁棒性？（3）在更复杂的多接触、动态场景中，Sim-to-Real 差距还有多大，以及如何通过改进域随机化策略来弥合？（4）当前系统是否能从人类交互视频中学习到更高级的协作或竞争策略？这些问题指向了从单技能模仿向通用人形交互智能演进的关键路径。

### 补充图表

![[assets/figures/papers/paper_list_l1703_HumanX_Toward_Agile_and_Generalizable_Humanoid_Interaction_Skills_from_H/figures/008_Table.jpg]]
*Table: I: Main Simulation Results. SR, $E _ { o }$ , and $E _ { h }$ measure the success rate on the original data, the object position tracking error, and the key-body position tracking error, respectively, while GSR measures the success rate of skill generalization*

![[assets/figures/papers/paper_list_l1703_HumanX_Toward_Agile_and_Generalizable_Humanoid_Interaction_Skills_from_H/figures/013_Table.jpg]]
*Table: II: Evaluation on Multi-Pattern Interaction Skills in Simulation. Each skill contains three distinct interaction patterns. TABLE III: Quantitative Results on Real Robot Experiments*

![[assets/figures/papers/paper_list_l1703_HumanX_Toward_Agile_and_Generalizable_Humanoid_Interaction_Skills_from_H/figures/006_Figure_6.jpg]]
*Figure 6: Simulation Results on Basketball Catch-Shot. XMimic generalizes to novel ball-passing trajectories and target positions (green sphere) with accurate and natural interactions*

![[assets/figures/papers/paper_list_l1703_HumanX_Toward_Agile_and_Generalizable_Humanoid_Interaction_Skills_from_H/figures/010_Figure_9.jpg]]
*Figure 9: Real Robot Experiment on Blind Basketball Skills. The proposed method fully leverages proprioception to control objects and enables diverse, highly dynamic, and complex interactions without any explicit object perception*

![[assets/figures/papers/paper_list_l1703_HumanX_Toward_Agile_and_Generalizable_Humanoid_Interaction_Skills_from_H/figures/011_Figure_10.jpg]]
*Figure 10: Real Robot Experiment on MoCap-based Interaction Skills. When utilizing MoCap system to perceive object or human motion, our method enables sustained interaction, demonstrating high precision, agility, robustness, and generalization capability. Notably, each task shown here is learned from a single demonstration video without any task-specific reward*

![[assets/figures/papers/paper_list_l1703_HumanX_Toward_Agile_and_Generalizable_Humanoid_Interaction_Skills_from_H/figures/014_Figure_12.jpg]]
*Figure 12: Sim-to-Real Analysis. (Left) If the training does not include sustained random external forces, the robot may lose balance during highly dynamic interactions. (Right) Without simulating MoCap signal loss during training, the robot may collapse when the object signal is temporarily lost during deployment*



## 定位与知识库关联

### 1. 问题定位与范式转换

HumanX 解决的核心瓶颈在于：**现有方法难以从极少量人类演示中学习多样化、可泛化的全身交互技能**。这一瓶颈的根源并非模仿学习算法本身的能力不足，而是数据获取范式的根本性限制——真实人形机器人的交互数据极度稀缺，而仿真中为每个任务精心设计奖励函数又无法规模化扩展至多样化的交互行为。

HumanX 的关键因果调节变量在于**将数据生成范式从“追求精确三维重建”转向“基于物理先验的交互轨迹合成”**。这一转换的核心洞察是：对于机器人技能获取而言，物理上合理的交互远比光度学上精确的重建更为重要。这种优先级转换使得从单个人类视频中生成大规模、物理一致且多样化的交互数据成为可能，从而同时解决了数据稀缺和奖励设计困难两个瓶颈。

### 2. 与基线方法的关系

#### 2.1 数据生成范式对比

**HDMI**（Weng et al., arXiv 2025）代表了基于精确重建的主流范式：先估计人类和物体的运动，再将其组合为人形交互数据。这一方法受限于重建精度和组合的物理一致性，导致其泛化能力极弱——在篮球接球投篮任务上仅获得 2.4% 的泛化成功率（GSR）（Table I）。HumanX 的 XGen 从根本上改变了这一范式：它不再追求精确重建，而是利用接触阶段的相对姿态不变性和非接触阶段的物理模拟来合成交互轨迹。这一范式转换带来的性能跃迁是决定性的：在相同任务上，HumanX 的 GSR 达到 64.7%，提升超过 25 倍。

**SkillMimic**（Wang et al., CVPR 2025）和 **OmniRetarget**（Yang et al., arXiv 2025）同样是基于 HOI 模仿或交互保持的数据生成方法，其共同局限在于依赖精确的物体运动估计和手工设计的交互保持约束，难以应对多样化的物体几何和运动变化。XGen 通过接触阶段的数据增强（物体几何缩放、轨迹变换）和非接触阶段的速度随机化，从根本上突破了这一局限。

#### 2.2 奖励设计范式对比

现有方法通常需要为每个任务精心设计特定的奖励函数，这在技能种类增加时变得不可持续。HumanX 的 XMimic 提出了一套**统一的任务无关的交互模仿奖励**，由身体模仿、物体跟踪、相对运动、接触图和正则化五项组成（Eq. 5）。这一统一的奖励方案使得同一框架可以处理篮球、羽毛球、足球、货物拾取等多种截然不同的交互技能，无需针对每个技能调整奖励权重。

#### 2.3 感知模式对比

现有方法在部署时通常依赖外部物体跟踪（如真值状态或完美感知），这在实际应用中难以保证。HumanX 支持两种灵活的部署模式：**无外部感知模式（NEP）** 完全依赖本体感受（proprioception）来控制物体，在实体 Unitree G1 机器人上实现了平均超过 80% 的篮球技能成功率（Table III）；**MoCap 模式**则引入模拟的信号丢失训练，使策略对真实世界中不可避免的感知中断具有鲁棒性（Fig. 12）。

### 3. 适用边界

HumanX 的适用边界由以下因素界定：

- **物体交互类型**：当前系统处理相对简单的单个物体操作（球类、货物），对于复杂的多物体、长时间任务尚未验证。
- **感知条件**：NEP 模式无法处理非接触交互（如接住飞行中的球），这类技能需要 MoCap 或视觉感知来获取物体状态。
- **硬件依赖**：部署依赖于特定的 IMU/MoCap 硬件，尚未实现纯视觉的零样本真实世界部署。
- **技能来源**：每个技能仅需单个视频演示即可学习，但技能间的组合和切换策略尚未被系统研究。

### 4. 局限与开放问题

**已确认的局限**（来自论文自身讨论）：
1. NEP 模式无法处理非接触交互，如接住飞行中的球。
2. 部署依赖于特定的 IMU/MoCap 硬件，且真实实验空间和天数有限。
3. 当前系统处理相对简单的单个物体操作，对于复杂的多物体、长时间任务尚未验证。

**开放问题**：
1. **纯视觉部署**：如何将该框架扩展到完全依赖视觉感知（而非 MoCap）的零样本真实世界部署？这需要解决从仿真到真实的视觉域适应问题，以及视觉感知噪声下的策略鲁棒性。
2. **数据规模化**：能否利用更大规模、更多样的互联网人类视频，进一步提升技能的多样性和鲁棒性？XGen 的增强管道为此提供了技术基础，但大规模视频数据的自动筛选和有效利用仍是一个开放挑战。
3. **Sim-to-Real 差距**：在更复杂的多接触、动态场景中，Sim-to-Real 差距还有多大，以及如何弥合？论文通过随机外力和 MoCap 信号丢失模拟部分弥合了这一差距（Fig. 12），但在更极端的真实世界扰动下，策略的鲁棒性边界尚不明确。
4. **高级交互策略**：当前系统是否能从人类交互视频中学习到更高级的协作或竞争策略？例如，从双人对抗运动中学习实时决策和策略规划，这需要超越当前的轨迹模仿范式，引入更高层次的策略理解。

### 5. 在知识库中的定位

HumanX 在“从人类视频学习人形机器人全身交互技能”这一研究方向上，代表了从“精确重建驱动”到“物理先验驱动”的范式转换。其核心贡献在于证明了：**对于交互技能获取，物理合理性比视觉精确性更重要**。这一洞察将数据生成从重建问题转化为合成问题，使得数据增强和泛化成为可能。

在技术谱系上，HumanX 结合了基于物理的角色动画（physics-based character animation）中的运动模仿技术、Sim-to-Real 迁移中的域随机化策略，以及模仿学习中的教师-学生蒸馏范式，将其统一为一个从人类视频到真实机器人部署的完整管道。其 8 倍以上的泛化性能提升（相对于 HDMI）和实体机器人上超过 80% 的成功率，为该方向的实用化提供了强有力的证据。



## 原文 PDF

![[paperPDFs/arxiv_2026/HumanX_Toward_Agile_and_Generalizable_Humanoid_Interaction_Skills_from_Human_Videos.pdf]]
