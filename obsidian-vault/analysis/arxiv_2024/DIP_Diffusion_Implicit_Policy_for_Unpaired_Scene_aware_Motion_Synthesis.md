---
title: DIP Diffusion Implicit Policy for Unpaired Scene aware Motion Synthesis
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/ICLR_2025/CLoSD_Closing_the_Loop_between_Simulation_and_Diffusion_for_Multi_Task_Character_Control.pdf
project_link: https://guytevet.github.io/CLoSD-page/
code_link: null
aliases:
- DDIPUSAMS
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 采用自回归快速扩散运动规划器（DiP），与鲁棒物理跟踪控制器（PHC）构成闭环反馈，并对跟踪策略进行多任务在线微调。通过大幅减少扩散步数和缩短规划片段实现实时性，通过文本与目标位置联合条件实现灵活的任务描述。
primary_logic: 运动扩散模型可以作为物理仿真控制器的在线通用规划器，借助自回归和极低扩散步数实现实时响应，并通过仿真状态反馈实现闭环修正，从而将文本驱动的语义丰富性与物理逼真度统一于一个框架。
claims:
- CLoSD在目标打击和起身任务上成功率大幅领先：打击成功率0.9 (vs UniHSI 0.02)，起身成功率0.98 (vs UniHSI 0.08)。
- DiP仅需10步扩散即可生成高质量运动（FID 0.32），且推理速度高达3500 fps（175倍实时）。
- 在HumanML3D文本到运动基准上，CLoSD全面超越MoConVQ（FID 1.798 vs 3.279），同时物理正确性指标也显著改善。
- 移除闭环或取消微调会导致任务成功率骤降（开环坐下成功率仅0.19，起身0.23），验证了闭环和微调的必要性。
---

# DIP Diffusion Implicit Policy for Unpaired Scene aware Motion Synthesis

> [!tip] 核心洞察
> 运动扩散模型可以作为物理仿真控制器的在线通用规划器，借助自回归和极低扩散步数实现实时响应，并通过仿真状态反馈实现闭环修正，从而将文本驱动的语义丰富性与物理逼真度统一于一个框架。

| 字段 | 内容 |
|------|------|
| 中文题名 | CLoSD：仿真与扩散闭环的多任务角色控制 |
| 英文题名 | DIP Diffusion Implicit Policy for Unpaired Scene aware Motion Synthesis |
| 会议/期刊 | arXiv 2024 |
| Links | [Project](https://guytevet.github.io/CLoSD-page/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | CLoSD |
| Dataset | Custom Task Suite - Striking, Custom Task Suite - Get-up, HumanML3D, HumanML3D - Physical Correctness |

> [!tip] 效果简介
> - Custom Task Suite - Striking 上，Success Rate 0.9 (CLoSD) vs 0.02 (UniHSI) (+0.88)。
> - Custom Task Suite - Get-up 上，Success Rate 0.98 (CLoSD) vs 0.08 (UniHSI) (+0.90)。
> - HumanML3D (text-to-motion) 上，FID (lower better) 1.798 (CLoSD) vs 3.279 (MoConVQ) (-1.481)。

## 概要

**问题瓶颈**：现有的数据驱动运动生成方法（如扩散模型）能够产生语义丰富的运动序列，但缺乏物理真实性，常伴随滑步、穿透等伪影；而基于物理仿真的强化学习控制器虽能保证物理正确，却难以扩展到丰富的文本控制和多任务交互。将扩散模型直接用于实时运动规划，还面临推理速度慢和环境感知缺失的挑战。

**核心思路**：CLoSD 通过**闭环反馈**将运动扩散模型与物理仿真控制器统一为一个系统。其核心是一个自回归的快速扩散运动规划器（DiP），仅需极少的扩散步数即可实时生成运动计划；该计划交由鲁棒的物理跟踪控制器执行，而仿真状态又反馈回规划器进行重新规划，形成规划-执行闭环。通过文本提示与目标位置联合条件，系统可灵活描述多样任务。

**方法定位**：CLoSD 属于**仿真与扩散闭环的多任务角色控制**方法。它既不同于纯运动学扩散模型（如 MDM）的开环生成，也不同于仅依赖目标位置而无文本风格控制的物理交互控制器（如 **UniHSI**, Xiao et al., ICLR 2024），同时相比统一物理运动控制模型（如 **MoConVQ**, Yao et al., TOG 2024），增加了细粒度物体交互能力与闭环修正机制。

**主要结果**：
- 在目标打击和起身任务上，CLoSD 成功率分别达到 **0.9** 和 **0.98**，远超 UniHSI 的 0.02 和 0.08（Table 1）。
- DiP 仅需 **10 步扩散**即可生成高质量运动（FID 0.32），推理速度高达 **3500 fps**（175 倍实时）（Table 2）。
- 在 HumanML3D 文本到运动基准上，CLoSD 全面超越 MoConVQ：FID **1.798** vs 3.279，物理穿透指标 **0.022** vs 0.249（Table 3）。
- 消融实验证实，移除闭环或取消跟踪控制器微调会导致任务成功率骤降（开环坐下仅 0.19，起身 0.23），验证了闭环与微调的必要性（Table 1）。

### 问题背景

生成逼真、可控的三维人体运动是计算机图形学与具身智能的核心挑战之一。该问题的难点在于需要同时满足两个往往相互冲突的需求：**语义丰富性**——能够根据自然语言描述生成多样化、符合意图的运动；以及**物理真实性**——运动必须遵守物理定律，能够与环境中的物体产生合理的接触与交互。

近年来，数据驱动的运动生成方法（特别是扩散模型）在文本到运动（text-to-motion）任务上取得了显著进展，能够产生高保真度的运动序列。然而，这些方法通常在运动学层面操作，生成的姿态序列缺乏与物理环境的真实交互，容易出现脚部滑动、地面穿透等物理不合理现象。

### 现有方法的缺口

当前解决物理真实性的主流路径是**基于物理仿真的角色控制**（physics-based character control）。这类方法通过强化学习训练策略网络，在物理模拟器中驱动物理角色跟踪参考运动，从而保证运动的物理正确性。然而，现有工作面临两个关键瓶颈：

1. **任务扩展性受限**：大多数物理控制器针对单一或少数预定义任务设计，难以扩展到丰富的文本控制和多任务交互。例如，**UniHSI**（Xiao et al., ICLR 2024）作为多任务物理场景交互控制器，虽然可以利用大语言模型指定目标位置，但缺乏文本风格控制能力，无法理解“放松地坐下”与“僵硬地坐下”之间的语义差异。

2. **生成与控制的割裂**：将扩散模型直接用于实时运动规划存在推理速度慢和环境感知缺失的挑战。传统扩散模型需要50步甚至更多的去噪迭代，难以满足实时控制需求；而离线一次生成完整序列的开环方式，无法对仿真过程中的状态偏差做出响应。**MoConVQ**（Yao et al., TOG 2024）作为统一物理运动控制模型，虽然在VQ潜在空间内实现了上下文学习，但不支持细粒度的物体交互任务。

### 核心动机

本文的核心动机是**弥合数据驱动的运动学运动生成与基于物理的角色控制之间的鸿沟**。作者观察到，运动扩散模型具有强大的规划能力，而物理仿真控制器能够保证执行的真实性——二者的结合恰好可以实现优势互补。关键问题在于：如何让扩散模型以足够快的速度运行，使其能够作为物理控制回路的在线组件，同时保持生成质量？

CLoSD的解决方案是构建一个**闭环的规划-执行系统**，其中扩散规划器（Diffusion Planner, DiP）与物理跟踪控制器构成实时反馈回路。通过将扩散步数大幅压缩至10步、采用自回归在线规划策略，DiP能够以3500 fps（175倍实时）的速度生成40帧运动计划，使扩散模型首次能够作为物理仿真控制器的实时通用规划器运行。这种设计将文本驱动的语义丰富性与物理仿真的逼真度统一于单一框架，实现了“用文本描述意图，用物理保证执行”的多任务角色控制范式。

## 核心方法与创新机理

CLoSD 的核心创新在于将**运动扩散模型重塑为物理仿真控制器的在线通用规划器**，并通过三个关键机制实现了文本驱动的语义丰富性与物理逼真度的统一：**极低步数自回归扩散规划**、**仿真状态闭环反馈**，以及**多任务联合微调**。这些创新直接回应了现有方法的两个瓶颈——数据驱动运动生成缺乏物理真实性，而物理控制器难以扩展至丰富的文本控制和多任务交互。

### 1. 从离线生成到在线闭环规划

传统运动扩散模型（如 MDM）采用离线方式一次性生成完整运动序列，缺乏对环境反馈的感知能力。CLoSD 将扩散模型重新定位为**自回归在线规划器（DiP）**：每轮仅生成 40 帧（约 2 秒）的运动计划，执行后将实际仿真结果作为前缀反馈给 DiP 进行下一轮规划。这一“规划-执行-反馈”闭环（Figure 2）使系统能够持续感知角色当前状态并动态修正运动，从根本上解决了开环方法在物理交互任务中因缺乏重规划而导致的失败——消融实验表明，开环模式下坐下和起身任务的成功率分别仅为 0.19 和 0.23，而闭环将其提升至 0.86 和 0.98（Table 1）。

### 2. 极低扩散步数的实时推理

扩散模型的推理速度是其实时应用的核心障碍。CLoSD 通过两项设计将推理步数从 MDM 的 50 步压缩至 10 步，同时保持生成质量（FID 0.32，Table 2）：一是采用直接预测干净运动序列的简洁损失函数 $\mathcal{L}_{\mathrm{simple}} = E_{x_0 \sim p(x_0|c), t \sim [1,T]} [\| x_0 - \hat{x}_0 \|_2^2]$，二是在扩散去噪过程中施加目标到达几何约束 $\mathcal{L}_{\mathrm{target}}$。这使得 DiP 在单张 RTX 3090 GPU 上达到 3500 fps 的推理速度（175 倍实时），为在线闭环规划提供了速度基础。消融实验进一步表明，即使仅用 5 步扩散，DiP 仍能保持 FID 0.32 的良好质量（Table 2）。

### 3. 文本与目标位置的联合条件接口

现有方法在任务描述上存在割裂：纯文本运动生成（如 MDM）无法指定精细的空间目标，而物理交互控制器（如 UniHSI）缺乏文本语义理解。CLoSD 设计了**统一的联合条件接口**，使 DiP 同时接受文本提示和可适配的关节目标位置、朝向角度及有效性标记。这一设计使同一模型能够处理从“走到指定位置”到“用右手击打目标”等不同粒度的任务描述，实现了文本语义与空间目标的灵活组合。

### 4. 闭环中的跟踪控制器在线微调

CLoSD 的另一关键创新在于将 RL 跟踪控制器（基于 PHC）置于闭环中进行**多任务同时微调**。微调过程中固定 DiP，每回合随机选择任务，仅使用原始 PHC 奖励函数（无额外奖励工程），通过 PPO 优化跟踪策略以适应 DiP 生成的规划运动与实际物理交互之间的分布偏移。消融实验证实了这一设计的必要性：取消微调后，坐下成功率从 0.86 降至 0.32，起身成功率从 0.98 降至 0.50（Table 1）；同时文本到运动指标也出现退化，R-precision Top1 从 0.381 降至 0.367，FID 从 1.798 升至 2.154（Table 3）。

### 方法谱系与知识库定位

CLoSD 处于**运动扩散生成**与**物理角色控制**的交叉地带。在运动生成侧，其自回归扩散规划继承了 MDM 的扩散框架，但通过极低步数和闭环反馈实现了从离线生成到在线控制的范式转换。在物理控制侧，其跟踪控制器建立在 **PHC**（通用运动跟踪策略）之上，但通过闭环微调弥合了规划运动与物理执行之间的鸿沟。相较于 **UniHSI**（Xiao et al., ICLR 2024）——使用 LLM 指定目标位置但无文本风格控制的多任务物理控制器，CLoSD 同时提供了文本语义理解和精细空间目标控制。相较于 **MoConVQ**（Yao et al., TOG 2024）——利用 VQ 潜在空间进行统一物理运动控制但不支持细粒度物体交互，CLoSD 在 HumanML3D 基准上实现了全面超越（FID 1.798 vs 3.279，R-precision Top1 0.381 vs 0.309），同时物理正确性指标显著改善（穿透率 0.022 vs 0.249，Table 3）。

CLoSD 构建了一个**闭环规划-执行系统**，将实时运动扩散模型与物理仿真跟踪控制器耦合，同时接受文本语义与空间目标作为任务接口。其核心思想在于：运动扩散模型不再作为离线生成器使用，而是充当在线通用规划器，通过自回归和极低扩散步数实现实时响应，并借助仿真状态反馈实现闭环修正，从而将文本驱动的语义丰富性与物理逼真度统一于一个框架。

系统由三个核心模块构成流水线，如图 Figure 2 所示：

![[assets/figures/papers/paper_list_l1668_DIP_Diffusion_Implicit_Policy_for_Unpaired_Scene_aware_Motion_Synthesis/figures/002_Figure_2.jpg]]
*Figure 2: CLoSD Overview. (Left) DiP is a rapid auto-regressive diffusion model conditioned on a text prompt and a Target location. It generates the motion plan*

1. **扩散规划器（Diffusion Planner, DiP）**：一个自回归的实时扩散模型，根据文本提示（text prompt）和可适配的目标关节位置（target joint locations）生成未来运动计划 $\hat{x}^{\mathrm{pred}}$。DiP 仅需 **10 步扩散**即可生成 40 帧运动片段，推理速度高达 **3500 fps（175 倍实时）**，这是实现闭环实时规划的关键使能因素。
2. **RL 跟踪控制器（基于 PHC）**：一个通用运动跟踪策略，接收 DiP 产生的运动计划作为参考轨迹，通过 PD 控制驱动物理仿真角色执行动作。该控制器在 AMASS 模仿任务上达到 **99% 成功率**，最大单关节误差小于 0.5 m，为闭环系统提供了鲁棒的物理执行基础。
3. **高层状态机（High-Level Planner）**：管理多任务序列，根据任务完成信号自动切换文本提示和目标位置，实现连续任务执行（如从“坐下”自动过渡到“起身”）。

**闭环反馈机制**是 CLoSD 区别于开环方案的核心设计。在每个规划-执行周期中，DiP 以当前仿真状态为前缀（prefix），自回归地生成未来运动计划；RL 控制器执行该计划后，仿真角色的实际运动帧被反馈回 DiP 作为下一轮规划的前缀。这一闭环使得系统能够持续感知环境变化（如物体位置偏移、碰撞干扰）并即时重新规划，从而在目标打击（成功率 **0.9** vs UniHSI 的 **0.02**）和起身（成功率 **0.98** vs UniHSI 的 **0.08**）等需要精细物体交互的任务上取得压倒性优势。

**任务条件接口**方面，CLoSD 统一了文本和空间目标两种模态：文本提示通过 CLIP 编码提供语义控制，目标位置通过可适配关节目标（adaptable joint targets）、朝向角度（heading angle）和有效性标记（validity flag）提供空间约束。DiP 在去噪过程中额外施加几何目标损失 $\mathcal{L}_{\mathrm{target}}$，强制生成序列的末端帧关节位置和身体朝向到达指定目标，从而将语义意图与空间精度统一于同一规划框架。

**在线微调**是闭环系统发挥全部潜力的关键。CLoSD 在闭环中固定 DiP，使用 PPO 对跟踪控制器进行多任务同时微调，仅使用原始 PHC 奖励函数，未引入额外奖励工程。消融实验表明，取消微调会导致坐下成功率从 **0.86 降至 0.32**，起身成功率从 **0.98 降至 0.50**，验证了闭环微调对弥合“规划运动”与“物理可执行运动”之间差距的必要性。

### 3.1 扩散运动先验

CLoSD的运动规划器建立在去噪扩散概率模型（DDPM）之上。其前向过程通过马尔可夫链逐步向干净运动序列 $x_0$ 添加高斯噪声：

$$q ( x _ { t } | x _ { t - 1 } ) = \mathcal { N } ( \sqrt { \alpha _ { t } } x _ { t - 1 } , ( 1 - \alpha _ { t } ) I )$$

其中 $\alpha_t$ 为噪声调度参数。与传统扩散模型预测噪声不同，DiP采用简洁损失（Simple Loss），直接预测干净运动序列 $\hat{x}_0$：

$$\mathcal { L } _ { \mathrm { s i m p l e } } = E _ { x _ { 0 } \sim p ( x _ { 0 } | c ) , t \sim [ 1 , T ] } [ \| x _ { 0 } - \hat { x } _ { 0 } \| _ { 2 } ^ { 2 } ]$$

该设计的核心动机在于：直接预测 $x_0$ 使得在去噪过程中施加几何约束成为可能，这是后续目标条件引导的基础。

### 3.2 扩散规划器（DiP）——实时自回归生成

DiP是CLoSD的核心运动生成模块，负责根据文本提示和目标位置实时合成运动计划。其关键设计在于将扩散步数从MDM的50步大幅压缩至10步，同时将生成模式从离线一次生成完整序列改为自回归在线规划。

具体而言，DiP每次生成 $N_g=40$ 帧的运动片段，并将前 $N_p=20$ 帧作为前缀（prefix）与上一轮执行结果拼接，形成自回归的规划-执行循环。这种片段化生成策略使得DiP能够在NVIDIA RTX 3090上达到3500 fps的推理速度（约175倍实时），为闭环反馈提供了时延基础。

### 3.3 自适应目标条件与目标到达损失

DiP的条件接口同时接受文本嵌入与可适配的关节目标位置。为实现精确的物体交互控制，论文在简洁损失之上引入了目标到达损失（Target Loss）：

$$\mathcal { L } _ { \mathrm { t a r g e t } } = \sum _ { j \in J } v _ { j } \| \operatorname { R 2 G } ( \hat { x } _ { 0 } [ N _ { g } ] ) _ { j } - c _ { j } \| _ { 2 } ^ { 2 } + v _ { \theta } \| \operatorname { R 2 G } ( \hat { x } _ { 0 } [ N _ { g } ] ) _ { \theta } \ominus c _ { \theta } \| _ { 2 } ^ { 2 }$$

其中：$J$ 为需要到达目标的关节集合；$\operatorname{R2G}(\cdot)$ 将局部运动表示转换为全局关节位置；$\hat{x}_0[N_g]$ 为预测序列的最后一帧；$c_j$ 和 $c_\theta$ 分别为目标关节位置和身体朝向角度；$v_j$ 和 $v_\theta$ 为有效性标记，允许某些关节或朝向在特定任务中不被约束；$\ominus$ 表示角度差运算。该损失强制DiP生成的末端帧精确到达指定目标，是实现打击、起身等物体交互任务的核心机制。

### 3.4 运动表示

DiP在HumanML3D运动表示空间中进行规划。每帧运动 $x[n]$ 定义为：

$$x [ n ] = ( { \dot { r } } ^ { a } , { \dot { r } } ^ { x } , { \dot { r } } ^ { z } , r ^ { y } , j ^ { p } , j ^ { r } , j ^ { v } , f ) \in \mathbb { R } ^ { F }$$

其中：${\dot{r}}^{a}, {\dot{r}}^{x}, {\dot{r}}^{z}$ 分别为根关节绕垂直轴的角速度及水平面内的线速度；$r^y$ 为根关节高度；$j^p, j^r, j^v$ 分别为局部关节位置、旋转和速度；$f$ 为脚部接触标记。该表示同时编码了运动学信息和环境交互线索，为DiP提供了完整的运动描述。

### 3.5 跟踪控制器与闭环微调

DiP生成的运动计划由基于PHC的RL跟踪控制器执行。控制器输入仿真状态 $x^{\mathrm{sim}}[n] = (\bar{j}^{gp}, \dot{j}^{gv})$（关节全局位置与线速度），通过PD控制器驱动物理仿真角色。闭环的核心在于：仿真执行后的实际状态被反馈至DiP作为下一轮规划的前缀，形成规划-执行-反馈的闭环回路。在此闭环中，使用PPO对跟踪策略进行多任务同时微调，固定DiP参数，仅使用原始PHC奖励函数，使控制器逐步适应DiP生成的多样化运动分布。

### 3.6 高层状态机

任务序列的自动切换由一个简单的状态机管理。每个任务在完成时发出信号（例如，坐下任务在骨盆到达沙发坐垫区域时标记完成），状态机据此切换文本提示和目标位置，实现无人工干预的连续多任务执行。

## 实验与关键发现

### 核心任务成功率：闭环与微调的决定性作用

CLoSD在涉及精细物体交互的任务上展现出压倒性优势。在目标打击（Striking）任务中，CLoSD的成功率达到**0.90**，而多任务物理交互基线**UniHSI**（Xiao et al., ICLR 2024）仅为**0.02**；在起身（Get-up）任务中，CLoSD的成功率为**0.98**，UniHSI仅为**0.08**（Table 1）。这一巨大差距源于两个核心机制：闭环反馈与跟踪控制器的多任务微调。

![[assets/figures/papers/paper_list_l1668_DIP_Diffusion_Implicit_Policy_for_Unpaired_Scene_aware_Motion_Synthesis/figures/004_Table_1.jpg]]
*Table 1: Task success rates. Bold and underscore relate to multi-task only. CLoSD significantly excels on Striking and Get-up, which require careful object interaction*

消融实验揭示了这两者的各自贡献。当系统退化为**开环**模式（即DiP一次性生成完整运动序列后不再根据仿真状态重新规划）时，坐下任务的成功率从0.86骤降至**0.19**，起身任务从0.98降至**0.23**（Table 1）。这验证了闭环反馈对于纠正累积误差、适应环境动态变化的必要性——开环控制器缺乏重规划能力，一旦初始计划与物理现实产生偏差便无法恢复。

同样关键的是**跟踪控制器微调**。取消微调（即使用固定预训练PHC策略）导致坐下成功率从0.86降至**0.32**，起身成功率从0.98降至**0.50**（Table 1, no fine-tuning vs Ours）。Figure 4的定性对比直观展示了这一差异：微调前，角色能够坐下但难以起身；微调后，角色能够以类人方式成功站起。值得注意的是，微调过程仅使用原始PHC奖励函数，未引入任何额外奖励工程，保证了对比的公平性。

### 扩散规划器速度与质量权衡

DiP在推理速度上实现了数量级突破。仅需**10步扩散**即可生成高质量运动（FID 0.32），推理速度高达**3500 fps**，即175倍实时（Table 2 and Section 4.1）。这一加速得益于两个关键设计：将扩散步数从MDM的50步压缩至10步，以及采用自回归生成短运动片段（40帧，约2秒）而非一次性生成完整序列。

![[assets/figures/papers/paper_list_l1668_DIP_Diffusion_Implicit_Policy_for_Unpaired_Scene_aware_Motion_Synthesis/figures/005_Table_2.jpg]]
*Table 2: DiP ablation study. We use DiP with prefix length*

消融实验进一步表明，DiP对扩散步数具有惊人的鲁棒性：即使仅用**5步扩散**，FID仍能保持在0.32的良好水平（Table 2）。10步被确定为性能与速度的最佳平衡点。

规划片段的长度选择也影响运动质量。更长的规划窗口（longer-loop）有利于文本对齐，FID可降至**1.671**；而过短的规划窗口会损害运动质量，FID升至**3.481**（Table 3, longer-loop vs shorter-loop）。这表明自回归规划需要在响应速度与生成质量之间谨慎权衡。

![[assets/figures/papers/paper_list_l1668_DIP_Diffusion_Implicit_Policy_for_Unpaired_Scene_aware_Motion_Synthesis/figures/007_Table_3.jpg]]
*Table 3: Text-to-motion on the HumanML3D benchmark (Guo et al., 2022), alongside the PhysDiff metrics (Yuan et al., 2023), which evaluate aspects of physical correctness. Diversity values closer to the ground truth are preferred*

### 文本到运动基准：物理逼真度与语义对齐的双重提升

在HumanML3D文本到运动基准上，CLoSD全面超越了统一物理运动控制模型**MoConVQ**（Yao et al., TOG 2024）。CLoSD的FID为**1.798**，显著优于MoConVQ的**3.279**；R-precision Top1为**0.381**，高于MoConVQ的**0.309**（Table 3）。这证明闭环规划-执行框架并未牺牲运动质量，反而提升了文本语义的对齐精度。

更关键的是物理正确性指标的改善。CLoSD的穿透率（Penetration）仅为**0.022**，远低于MoConVQ的**0.249**（Table 3）。这一优势源于物理仿真对生成运动的约束——即使DiP产生的运动计划存在微小物理不合理性，跟踪控制器在闭环执行中也会通过仿真反馈进行修正，从而输出物理可行的最终运动。

微调控制器对文本到运动指标也有正向贡献：R-precision Top1从0.367提升至0.381，FID从2.154降至1.798（Table 3, ablation rows）。这表明多任务微调不仅提升了任务成功率，还改善了通用运动生成的质量。

### 失败模式与局限性

尽管CLoSD在测试任务上表现优异，系统仍存在若干结构性局限。首先，任务切换依赖**预定义状态机**，无法处理未预见的任务组合或在线生成的序列。其次，系统仅进行中低层运动规划，缺少更长时间尺度的策略推理能力。此外，尚未集成视觉或高度图等外部感知，限制了在非结构化环境中的应用。固定的规划-执行循环频率可能不适用于高动态运动场景，而长规划窗口下偶发的运动伪影也需进一步缓解。

这些局限指向了未来工作的方向：引入第一人称视觉作为闭环输入以实现感知驱动的通用控制，将规划拓展至分层架构（战略-战术-执行），以及根据运动速度动态调整规划与控制频率。

![[assets/figures/papers/paper_list_l1668_DIP_Diffusion_Implicit_Policy_for_Unpaired_Scene_aware_Motion_Synthesis/figures/006_Figure_4.jpg]]
*Figure 4: Comparisons of the getup task. The pelvis target is marked in cyan. CLoSD is able to get up successfully with a human-like motion. Before fine-tuning on object interaction with the closed-loop, it was able to sit but struggled to get up. The open-loop baseline struggles with any interaction with the sofa due to the lack of re-planning. UniHSI (Xiao et al., 2024) was designed to minimize contact-point distance and thus lifts the pelvis instead of getting up from the sofa*

![[assets/figures/papers/paper_list_l1668_DIP_Diffusion_Implicit_Policy_for_Unpaired_Scene_aware_Motion_Synthesis/figures/003_Figure_3.jpg]]
*Figure 3: (Left) CLoSD generates versatile text-prompted physics-based motions. The SMPLcompatible physics model is rendered with the SMPL mesh. (Right) CLoSD can perform a sequence of RL tasks (see the web page video). Task transitions are user-specified via interactively changing the text, or via a state machine, with transitions on a task done signal*

## 定位与知识库关联

### 核心瓶颈与设计动机

CLoSD 试图弥合两条长期割裂的研究路线：**数据驱动的运动生成**与**基于物理仿真的角色控制**。前者（以扩散模型为代表）能产生语义丰富、风格多样的运动，但缺乏物理真实性——生成的角色会漂浮、穿透地面或违背动力学约束；后者（以强化学习控制器为代表）能产生物理逼真的运动，但难以扩展到丰富的文本控制和多任务交互。这一瓶颈的实质是：**运动生成缺乏物理感知，物理控制缺乏语义泛化**。

CLoSD 的核心洞察在于，运动扩散模型可以被重新定位为物理仿真控制器的**在线通用规划器**。通过自回归生成和极低扩散步数（从 MDM 的 50 步降至 10 步）实现实时响应，并通过仿真状态反馈实现闭环修正，从而将文本驱动的语义丰富性与物理逼真度统一于一个框架。

### 方法谱系定位

#### 相对于运动生成方法的继承与突破

CLoSD 直接继承了 **MDM**（Human Motion Diffusion Model）的扩散生成范式，但做出了三项关键改造：

1. **推理步数压缩**：将扩散-去噪步数从 MDM 的 50 步压缩至 10 步，推理速度提升 5 倍，达到 3500 fps（175 倍实时）。消融实验表明，DiP 甚至仅需 5 步扩散即可保持 FID 0.32 的良好质量（Table 2），10 步为性能与速度的最佳平衡点。
2. **自回归在线规划**：MDM 采用离线一次生成完整序列的方式，而 DiP 以自回归方式持续生成短运动片段（prefix 长度 $N_p=20$，生成长度 $N_g=40$），使规划器能够实时响应环境变化。
3. **任务条件接口扩展**：从仅文本条件扩展为“文本 + 可适配关节目标 + 朝向角度 + 有效性标记”的联合条件，使同一规划器能同时处理风格化运动生成和目标导向的交互任务。

#### 相对于物理控制方法的差异化

与 **UniHSI**（Xiao et al., ICLR 2024）相比，CLoSD 的关键差异在于**闭环规划与文本语义的融合**。UniHSI 使用 LLM 指定目标位置，但缺乏文本风格控制，且其接触点最小化策略导致非自然的运动策略（如在起身任务中直接抬升骨盆而非从沙发起身，见 Figure 4）。CLoSD 在目标打击任务上成功率 0.9 vs UniHSI 的 0.02，起身任务 0.98 vs 0.08（Table 1），差距悬殊。

与 **MoConVQ**（Yao et al., TOG 2024）相比，CLoSD 在 HumanML3D 文本到运动基准上全面超越：FID 1.798 vs 3.279，R-precision Top1 0.381 vs 0.309。更重要的是，CLoSD 的物理正确性指标显著改善（Penetration 0.022 vs 0.249），这源于闭环仿真反馈对运动计划的物理修正。MoConVQ 利用 VQ 潜在空间和上下文学习实现统一物理运动控制，但不支持细粒度物体交互。

#### 闭环与微调的必要性验证

消融实验揭示了两个关键因果机制：

- **闭环 vs 开环**：开环模式下坐下和起身任务成功率分别仅为 0.19 和 0.23，闭环将其提升至 0.86 和 0.98（Table 1），验证了仿真状态反馈对任务成功的关键作用。
- **控制器微调**：取消跟踪控制器微调导致坐下成功率从 0.86 降至 0.32，起身从 0.98 降至 0.50（Table 1）。微调还改善了文本到运动指标，R-precision Top1 从 0.367 提升至 0.381，FID 从 2.154 降至 1.798（Table 3）。

### 适用边界与局限

1. **任务序列依赖预定义状态机**：当前系统依赖预定义的状态机进行任务切换，无法处理未预见的任务组合或在线生成的序列。这意味着 CLoSD 的“多任务”能力受限于人工设计的任务拓扑。
2. **规划时间尺度受限**：系统仅进行中低层运动规划（2 秒片段），缺少更长时间尺度的策略推理（如全局路径规划）。更长的规划片段有利于文本对齐（FID 1.671），但过短会损害质量（FID 3.481）（Table 3）。
3. **缺乏外部感知**：尚未集成视觉或高度图等外部感知，限制了在非结构化环境中的应用。当前系统假设目标位置和文本提示由外部提供。
4. **固定循环频率**：固定的规划-执行循环频率可能不适用于快速或高动态运动，需要自适应调整循环速率。
5. **长序列伪影**：长规划窗口下偶发的运动伪影仍需进一步缓解。

### 开放问题

1. **感知驱动的通用控制**：如何引入第一人称视觉或高程图作为闭环输入，实现基于感知的通用运动控制？
2. **分层规划架构**：能否将规划拓展到更长时间尺度，实现分层规划（战略、战术、执行），使角色具备长期任务推理能力？
3. **自适应循环速率**：可否根据运动速度动态调整规划与控制的频率，从而在慢速运动中节省计算，在快速运动中提高响应？
4. **长序列稳定性**：如何进一步减少长序列生成中的偶发伪影，提高持续交互的稳定性？

## 原文 PDF

![[paperPDFs/ICLR_2025/CLoSD_Closing_the_Loop_between_Simulation_and_Diffusion_for_Multi_Task_Character_Control.pdf]]
