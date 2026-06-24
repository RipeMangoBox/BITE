---
title: "TokenHSI: Unified Synthesis of Physical Human-Scene Interactions through Task Tokenization"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/TokenHSI_Unified_Synthesis_of_Physical_Human_Scene_Interactions_through_Task_Tokenization.pdf
aliases:
- TokenHSI
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将角色本体感知建模为独立的共享令牌(proprioception token)，并通过Transformer中的掩码机制与不同任务令牌结合，实现跨任务知识共享和高效多任务训练。
primary_logic: 解耦本体感知与任务观测，利用共享本体感知令牌实现跨任务运动知识迁移；借助Transformer的可变长输入和掩码注意力，单网络统一多技能并支持仅需少量额外参数的高效策略适应。
claims:
- 统一的Transformer策略在四项基础HSI技能上超越或持平单任务专用策略。
- 共享本体感知令牌Tprop消融导致所有任务成功率下降。
- 在技能组合任务中，TokenHSI显著优于现有方法，尤其在Climb+Carry上达到99.2%成功率，而CML仅为68.3%。
- 策略适应时仅需训练少量参数（适配器层和新任务令牌），避免全量微调，效率优于AdaptNet。
---

# TokenHSI: Unified Synthesis of Physical Human-Scene Interactions through Task Tokenization

> [!tip] 核心洞察
> 解耦本体感知与任务观测，利用共享本体感知令牌实现跨任务运动知识迁移；借助Transformer的可变长输入和掩码注意力，单网络统一多技能并支持仅需少量额外参数的高效策略适应。

| 字段 | 内容 |
|------|------|
| 中文题名 | TokenHSI：通过任务标记化的统一物理人-场景交互合成 |
| 英文题名 | TokenHSI: Unified Synthesis of Physical Human-Scene Interactions through Task Tokenization |
| 会议/期刊 | CVPR 2025 |
| Links | [Project](https://liangpan99.github.io/TokenHSI) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | TokenHSI |
| Dataset | Foundational HSI Skills, Skill Composition: Climb+Carry, Object Shape Variation: Chair, Terrain Shape Variation: Carry |

> [!tip] 效果简介
> - Foundational HSI Skills (Follow, Sit, Climb, Carry) 上，Success Rate (%) Follow: 99.7, Sit: 99.6, Climb: 99.8, Carry: 92.2 vs Specialist: Follow 98.7, Sit 98.2, Climb 99.7, Carry 83.1 (Follow +1.0, Sit +1.4, Climb +0.1, Carry +9.1)。
> - Skill Composition: Climb+Carry 上，Success Rate (%) 99.2 vs CML 68.3, CML (dual) 51.3 (vs CML +30.9)。
> - Object Shape Variation: Chair 上，Success Rate (%) 88.8 vs AdaptNet 84.5 (+4.3)。

## 概述

物理仿真下的角色控制是构建真实人-场景交互（Human-Scene Interaction, HSI）的关键技术。然而，现有方法通常为单一任务（如跟随路径、坐下、攀爬或搬运物体）独立设计专用策略，缺乏多技能的统一与泛化能力。当面对需要多技能协同的复杂任务——例如在复杂地形上搬运物体，或顺序执行多个子任务的长程任务——这些孤立训练的控制器难以有效组合与迁移。这一瓶颈的根源在于，传统策略架构将角色本体感知与任务观测耦合为单一联合状态，并通过固定长度的MLP网络处理，导致不同任务之间的运动知识无法共享。

**TokenHSI** 针对上述问题提出了一个统一的Transformer策略框架。其核心洞察是：**将角色本体感知建模为一个独立的共享令牌（proprioception token），与不同任务的观测令牌解耦，并通过Transformer中的掩码注意力机制实现跨任务知识迁移。** 具体而言，TokenHSI将本体感知和各类任务观测分别通过独立的令牌化器（tokenizer）编码为固定维度的特征令牌，送入一个共享的Transformer编码器进行融合。训练时，通过掩码抑制与当前任务无关的令牌，使单一网络能够同时掌握多种技能，且仅需少量额外参数即可高效适应新任务。

实验表明，TokenHSI在四项基础HSI技能（Follow、Sit、Climb、Carry）上全面超越或持平单任务专用策略，尤其在Carry任务上将成功率从83.1%提升至92.2%（Table 1）。在技能组合任务中，TokenHSI的优势更为显著：Climb+Carry组合任务的成功率达到99.2%，而基线方法CML仅为68.3%（Table 2）。此外，通过冻结预训练参数并仅训练新增任务令牌与零初始化适配器层，TokenHSI能够高效适应物体形状变化、地形变化乃至长程任务完成等更具挑战性的场景，展现出较强的泛化能力和样本效率。

## 背景与动机

物理仿真角色与三维场景的交互（Physical Human-Scene Interaction, HSI）是计算机图形学与具身智能交叉领域的核心挑战，其目标是在物理模拟器中驱动力学角色完成诸如路径跟随、坐下、攀爬、搬运等多样化任务。近年来，基于强化学习（RL）的运动控制方法取得了显著进展，但现有工作普遍存在一个结构性瓶颈：**控制器通常为单一任务独立设计，缺乏多技能统一与泛化能力**。例如，一个能精准跟随路径的角色策略，往往无法同时完成搬运箱子或攀爬障碍等任务，更难以应对需要多技能协同的复杂组合场景。

这一瓶颈的根源在于传统策略架构的固有限制。主流方法（如AMP及其衍生工作）通常采用固定长度的MLP策略网络，将角色本体感知状态与任务目标状态拼接为单一联合观测（joint character-goal state space）作为输入。这种设计导致两个关键缺陷：（1）观测空间随任务变化而剧烈变动，不同任务之间无法共享运动知识；（2）网络输入维度固定，难以灵活扩展至任意数量的任务组合。当面对需要“攀爬并搬运”（Climb+Carry）或“在复杂地形上跟随并搬运”等技能组合任务时，现有方法要么需要从头训练新策略（Scratch），要么依赖组合动作学习（CML）等方案，但这些方案在成功率上存在显著不足——例如CML在Climb+Carry任务上仅达到68.3%的成功率（见Table 2）。

此外，策略的持续适应与扩展同样面临效率困境。当预训练策略需要泛化到新的物体形状、地形变化或长期任务时，全量微调（Finetune）计算开销大且容易遗忘已学技能，而专门的适应架构（如AdaptNet）虽然部分缓解了这一问题，但在收敛速度和最终性能上仍有提升空间。

**TokenHSI的核心动机**正是针对上述缺口：通过重新设计观测表示与策略架构，实现单一网络对多项基础HSI技能的统一学习，并支持以极低的参数代价高效适应到更复杂的组合与泛化任务。其关键洞察在于**解耦本体感知与任务观测**——将角色自身的运动状态建模为独立的共享本体感知令牌（proprioception token），而将不同任务的特定观测分别编码为独立的任务令牌。借助Transformer编码器的可变长输入支持和掩码注意力机制，共享的本体感知令牌能够在不同任务间传递运动知识，而掩码机制则抑制无关任务令牌的干扰，从而在单网络中实现高效的多任务联合训练与跨技能知识迁移。

## 核心创新

TokenHSI 的核心创新在于通过**任务标记化（Task Tokenization）** 将物理人-场景交互（HSI）建模从“单一任务专用策略”范式转变为 **“统一 Transformer 多任务策略 + 轻量适应”** 范式。其关键设计变更体现在以下四个维度：

**1. 观测空间解耦与独立令牌化**

传统方法（如 AMP 专用策略）将角色本体感知与任务目标状态合并为单一联合观测（joint character-goal state space），导致不同任务的观测维度固定且难以扩展。TokenHSI 将观测空间拆分为**共享本体感知令牌** $T^{prop}$ 和**多个任务专用令牌**（如 $T^f$ 跟随、$T^s$ 坐下、$T^m$ 攀爬、$T^c$ 搬运），每个令牌通过独立 tokenizer 标准化为 64 维特征。这一解耦使得模型能够以可变长输入方式无缝整合任意数量的任务，从根本上打破了固定观测空间的限制。

**2. 策略网络架构从固定 MLP 转向掩码 Transformer**

基线方法通常采用固定长度的 MLP 策略网络，无法处理变长输入。TokenHSI 引入 **Transformer 编码器 $\phi$**（4 层、2 注意力头、512 维前馈层），利用其原生支持可变长序列的特性，将多个任务令牌与输出嵌入 $e$ 拼接后输入。通过**掩码注意力机制**，模型可根据任务标签 $l_t$ 选择性屏蔽无关任务令牌，使角色仅关注当前任务所需的观测信息。这一设计使得单一网络能够同时掌握四项基础 HSI 技能，且无需为每个任务维护独立参数。

**3. 跨任务知识共享机制**

传统多任务训练中各任务策略独立，缺乏显式的知识迁移通道。TokenHSI 的共享 $T^{prop}$ 令牌和 Transformer 编码器构成了跨任务知识共享的核心枢纽：本体感知令牌在多样任务中联合训练，学习到泛化性更强的运动表征；编码器通过自注意力融合所有令牌信息，使得不同任务间可通过共享表示相互促进。消融实验证实，移除 $T^{prop}$ 会导致所有基础技能成功率下降（如 Carry 从 92.2% 降至 90.9%），验证了该共享机制的关键作用。

**4. 高效策略适应：冻结主干 + 适配器层**

在将预训练技能迁移到新任务（如技能组合、物体/地形形状变化）时，基线方法要么从头训练（Scratch），要么全量微调（Finetune），或依赖专门设计的适应架构（AdaptNet）。TokenHSI 提出**冻结预训练组件**（$T^{prop}$、编码器 $\phi$、输出嵌入 $e$、动作头 $H$），仅训练**新增任务令牌**和**动作头中插入的零初始化适配器层** $\xi^A$。这一轻量适应策略在 Climb+Carry 技能组合任务上达到 99.2% 成功率（CML 仅 68.3%），在地形变化搬运任务上达到 74.0%（AdaptNet 为 63.4%），同时训练参数量远小于全量微调，实现了效率与性能的双重优势。

## 整体框架

TokenHSI 构建了一个两阶段统一框架，通过将人-场景交互建模为可组合的**任务令牌**，在单个 Transformer 网络中实现多技能学习与高效策略适应。如图 2 所示，整体流程分为**基础技能学习**（左）与**策略适应**（右）两个阶段。

### 阶段一：基础技能学习

该阶段的核心是将角色的**本体感知**与**任务观测**解耦为独立令牌，通过掩码注意力机制实现多任务联合训练。

**输入令牌化**：框架设计了多个专用令牌化器（Tokenizers），将异构观测统一为 64 维特征令牌：
- **共享本体感知令牌** $T^{prop}$：编码角色自身状态（关节位置、速度等），在所有任务间共享，是跨任务知识迁移的枢纽。
- **任务令牌** $T^{f}$（路径跟随）、$T^{s}$（就坐）、$T^{m}$（攀爬）、$T^{c}$（搬运）：分别将对应任务的观测（目标路径、座椅位置、攀爬目标、箱子状态等）编码为固定维度特征。

**Transformer 编码与掩码**：令牌序列与一个可学习的**输出嵌入** $e$（64 维）拼接后送入 Transformer 编码器 $\phi$（4 层，2 注意力头，512 维前馈层）。通过**掩码注意力**，模型在执行特定任务时仅允许 $T^{prop}$ 与对应任务令牌交互，抑制无关任务令牌，从而实现“单网络多技能”的精准控制。

**动作生成**：编码器输出的 $e$ 对应表示经**动作头** $H$（MLP，[1024, 512, 32] 单元）映射为最终动作。同时，**条件运动判别器** $D$ 以 one-hot 任务标签为条件，防止策略学习与当前任务无关的运动技能。

### 阶段二：策略适应

为将基础技能泛化至更复杂的下游任务（技能组合、物体/地形变化、长程任务），TokenHSI 采用**参数高效适应**策略：
- **冻结**预训练的 $T^{prop}$、$e$、$H$ 和 $\phi$ 的大部分参数。
- **新增**任务令牌（如 $T^{new}$）以处理新观测模态（例如高度图令牌用于地形感知）。
- **插入适配器层** $\xi^{A}$（零初始化残差模块）至动作头中，仅训练这些轻量级参数和新令牌。

这一设计避免了从头训练或全量微调，仅需少量额外参数即可实现高效策略迁移。

### 推理时的任务切换

在长程任务执行中，框架引入**有限状态机**（FSM）实现自动化子任务切换：FSM 根据当前状态输出 one-hot 任务标签 $l_t$，该标签直接作为 Transformer 的注意力掩码，动态激活对应的任务令牌，使角色无需人工干预即可顺序完成多个子任务。

### 补充图表

![[assets/figures/papers/paper_list_l1751_TokenHSI_Unified_Synthesis_of_Physical_Human_Scene_Interactions_through/figures/001_Figure_1.jpg]]
*Figure 1: Introducing TokenHSI, a unified model that enables physics-based characters to perform diverse human-scene interaction tasks. It excels at seamlessly unifying multiple foundational HSI skills within a single transformer network and flexibly adapting learned skills to challenging new tasks, including skill composition, object/terrain shape variation, and long-horizon task completion*

![[assets/figures/papers/paper_list_l1751_TokenHSI_Unified_Synthesis_of_Physical_Human_Scene_Interactions_through/figures/002_Figure_2.jpg]]
*Figure 2: TokenHSI consists of two stages: (left) foundational skill learning and (right) policy adaptation. Through multi-task policy training, the proposed framework learns versatile interaction skills in a single transformer network. Theses learned skills can be flexibly adapted to more challenging HSI tasks by training the lightweight modules, e.g., Tnew, Tc, and*

## 核心模块与公式推导

### 3.1 多令牌观测空间构建

TokenHSI的核心创新在于将传统物理角色控制中“角色状态与任务目标合并为单一联合观测”的做法，解耦为独立的多令牌输入。具体而言，系统构建了以下关键令牌化模块：

- **本体感知令牌化器 $T^{prop}$**：将角色的本体感知状态（关节位置、速度、姿态等）编码为固定64维特征令牌。该令牌在所有任务间共享，是实现跨任务运动知识迁移的关键载体。
- **任务令牌化器 $\{T^f, T^s, T^m, T^c\}$**：分别对应路径跟随(Follow)、坐下(Sit)、攀爬(Climb)和搬运(Carry)四类基础HSI技能。每个令牌化器将对应任务的观测（如目标路径点、座椅位置、攀爬目标、箱子位姿等）标准化为统一的64维特征，解决了不同任务观测维度异构的问题。

上述设计将原本固定长度的MLP输入转换为可变长的令牌序列，使策略网络能够自然地支持任意数量和类型的任务组合。

### 3.2 Transformer编码器与掩码注意力

策略网络的核心是一个Transformer编码器 $\phi$，由4层编码器层堆叠而成，每层包含2个注意力头和512维的前馈层。其工作流程如下：

1. **输入构建**：对于给定任务标签 $l_t$，将本体感知令牌 $T^{prop}$ 与对应任务令牌拼接为输入序列。
2. **掩码机制**：利用任务标签 $l_t$ 生成注意力掩码，抑制与当前任务无关的其他任务令牌参与自注意力计算，确保策略仅关注当前任务相关信息。
3. **输出令牌**：引入可学习的64维嵌入向量 $e$ 作为输出令牌，与输入令牌一同参与编码器计算，最终提取融合了本体感知与任务上下文的综合表示。
4. **动作生成**：动作头 $H$ 是一个MLP（结构为[1024, 512, 32]），将编码器输出映射为最终的动作指令。

### 3.3 值函数与判别器

- **值函数 $V$**：采用MLP网络，包含4个隐藏层（[2048, 1024, 512, 1]），以状态和所有任务目标为输入。训练时，与当前任务无关的目标输入被置零，简化为 $V(s_t, g_t^{l_t})$。
- **运动判别器 $D$**：条件GAN判别器，以one-hot任务标签 $l_t$ 为条件，防止策略学习与当前任务无关的运动技能，保证生成动作的任务针对性。

### 3.4 策略适应中的适配器层

在策略适应阶段，TokenHSI冻结预训练的大部分参数（包括 $T^{prop}$、$e$、$H$、$\phi$），仅训练以下轻量模块：

- **新任务令牌 $T^{new}$**：针对新任务设计的令牌化器。
- **适配器层 $\xi^A = \{\xi_0^A, \xi_1^A\}$**：零初始化的残差适配器，插入动作头中。由于初始输出为零，适配器不会破坏预训练策略的原始行为，随后通过少量训练即可快速适应新任务。

### 3.5 关键公式

#### MDP优化目标
策略通过PPO最大化累积折扣奖励：
$$\sum_{t=0}^{T} \gamma^{t} r_{t}$$

#### 路径跟随误差
衡量骨盆位置与目标轨迹点的平均L2距离：
$$\frac{1}{n} \sum_{t=1}^{n} \left\| x_{t}^{pelvis} - x_{t}^{tar} \right\|_{2}$$

#### 搬运任务奖励函数
搬运任务采用分阶段奖励设计。第一阶段鼓励角色走到箱子附近：
$$r_{t}^{c.walk} = \begin{cases} 0.2, & \|x_{t}^{obj.2d} - x_{t}^{root.2d}\| < 0.5 \\ 0.2 \exp(-5.0 \|1.5 - d_{t}^{*} \cdot \dot{x}_{t}^{root.2d}\|^2), & \text{otherwise} \end{cases}$$

第二阶段鼓励角色用手拾起箱子：
$$r_{t}^{c.pick} = \begin{cases} 0.0, & \|x_{t}^{obj.2d} - x_{t}^{root.2d}\| > 0.7 \\ 0.2 \exp(-5.0 \|x_{t}^{obj} - x_{t}^{hand}\|^2), & \text{otherwise} \end{cases}$$

#### 组合任务奖励
对于路径跟随与搬运的组合技能，采用加权融合：
$$r_{t}^{f+c} = \begin{cases} 0.0, & \|x_{t}^{obj.2d} - x_{t}^{root.2d}\| > 0.7 \\ 0.5 r_{t}^{f} + 0.5 r_{t}^{c.pick}, & \text{otherwise} \end{cases}$$

其中 $r_t^f$ 为路径跟随奖励，$r_t^{c.pick}$ 为搬运拾取奖励，权重各0.5实现技能平衡。

## 实验与分析

### 基础技能统一学习

TokenHSI 首先在四项基础人-场景交互技能（路径跟随 Follow、坐下 Sit、攀爬 Climb、搬运 Carry）上进行多任务联合训练，并与单任务专用策略（Specialist，基于 AMP 框架）进行对比。**Table 1** 展示了各任务的定量结果。

![[assets/figures/papers/paper_list_l1751_TokenHSI_Unified_Synthesis_of_Physical_Human_Scene_Interactions_through/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison between our unified multi-task policy and specialist policies across four foundational HSI skills. Values are reported in the format of mean±std*

统一 Transformer 策略在所有四项技能上的成功率均超越或持平专用策略：Follow 达到 99.7%（Specialist 98.7%），Sit 达到 99.6%（Specialist 98.2%），Climb 达到 99.8%（Specialist 99.7%），Carry 达到 92.2%（Specialist 83.1%）。其中搬运任务提升最为显著，达 9.1 个百分点，表明多任务联合训练通过共享本体感知令牌实现了有效的跨任务知识迁移。路径跟随误差（定义为 $\frac{1}{n} \sum_{t=1}^{n} \left\| x_{t}^{\text{pelvis}} - x_{t}^{\text{tar}} \right\|_{2}$）方面，TokenHSI 与专用策略保持可比水平。

消融实验验证了共享本体感知令牌 $T^{\text{prop}}$ 的核心作用：移除该令牌后（Ours w/o $T^{\text{prop}}$），四项技能的成功率普遍下降，其中 Sit 从 99.6% 降至 98.7%，Carry 从 92.2% 降至 90.9%，证实了跨任务共享本体感知表征对运动知识迁移的关键价值。

### 策略适应：技能组合与场景泛化

在基础技能学习完成后，TokenHSI 通过冻结大部分预训练参数、仅训练新增任务令牌和动作头中的零初始化适配器层，实现高效策略适应。

**技能组合任务**（**Table 2** 与 **Figure 3**）：在同时执行攀爬与搬运（Climb+Carry）的复合任务上，TokenHSI 达到 99.2% 成功率，远超从头训练（Scratch 26.8%）、组合动作学习基线 CML（68.3%）及改进版 CML (dual)（51.3%）。学习曲线显示 TokenHSI 收敛速度显著快于所有基线，且方差更小。这一优势源于共享本体感知令牌 $T^{\text{prop}}$ 在多任务预训练中习得的泛化表征——相比 CML 依赖的单一任务基础策略，TokenHSI 的跨任务先验知识为技能组合提供了更强的初始化。移除 $T^{\text{prop}}$ 的消融实验进一步确认了其贡献。

**物体形状变化**（**Table 3** 与 **Figure 5**）：在椅子形状的坐下任务上，TokenHSI 以 88.8% 成功率优于全量微调（Finetune 87.5%）和专用适应架构 AdaptNet（84.5%），且仅需训练少量参数，避免了 AdaptNet 的复杂设计。

**地形变化**（**Table 4** 与 **Figure 6**）：在楼梯地形上的路径跟随和搬运任务中，TokenHSI 分别达到 96.0% 和 74.0% 成功率。相比之下，从头训练（Scratch）在搬运任务上完全失败（0%），AdaptNet 仅达 63.4%。消融实验表明，移除适配器层（Ours w/o adapters）会导致性能急剧下降（Follow 降至 63%，Carry 降至 10.8%），验证了零初始化适配器在策略适应中的必要性。

### 长时域任务完成

在需要顺序执行多个子任务的长时域场景中（**Figure 7** 与 **Figure B**），TokenHSI 平均完成 3.79 个子任务（最大 4 个），显著优于从头训练（0.82）和迭代微调多个专用策略的 Finetune 基线（1.86）。推理阶段通过有限状态机（FSM）实现自动化任务切换，利用任务标签作为注意力掩码激活对应令牌，无需人工干预。

![[assets/figures/papers/paper_list_l1751_TokenHSI_Unified_Synthesis_of_Physical_Human_Scene_Interactions_through/figures/010_Figure_7.jpg]]
*Figure 7: Long-horizon task completion by sequentially executing (a) pre-trained skills and (b) adapted skills by our approach*

### 失败模式与局限

尽管 TokenHSI 在多数任务上表现优异，仍存在以下局限：① 复杂奖励函数的设计依赖大量试错工程，限制了新技能的快速拓展；② 长时域任务完成仍需人类设计的 FSM 进行子任务调度，尚未实现完全自主的端到端决策；③ 实验环境相对简化，向真实世界复杂场景的迁移仍面临挑战。

### 补充图表

![[assets/figures/papers/paper_list_l1751_TokenHSI_Unified_Synthesis_of_Physical_Human_Scene_Interactions_through/figures/003_Table_2.jpg]]
*Table 2: Quantitative results across skill composition tasks*

![[assets/figures/papers/paper_list_l1751_TokenHSI_Unified_Synthesis_of_Physical_Human_Scene_Interactions_through/figures/005_Figure_3.jpg]]
*Figure 3: Learning curves comparing the efficiency on skill composition tasks using TokenHSI, policies trained from scratch [79], CML [110], and its improved version CML (dual). Colored regions denote mean values ± a standard deviation based on 3 models initialized with different random seeds*

![[assets/figures/papers/paper_list_l1751_TokenHSI_Unified_Synthesis_of_Physical_Human_Scene_Interactions_through/figures/007_Figure_4.jpg]]
*Figure 4: Through policy adaptation, TokenHSI can generalize learned foundational skills to more challenging scene interaction tasks*

![[assets/figures/papers/paper_list_l1751_TokenHSI_Unified_Synthesis_of_Physical_Human_Scene_Interactions_through/figures/008_Figure_5.jpg]]
*Figure 5: Learning curves comparing the efficiency on object shape variation tasks using TokenHSI, full fine-tuning of pretrained policies, and AdaptNet [111]*

![[assets/figures/papers/paper_list_l1751_TokenHSI_Unified_Synthesis_of_Physical_Human_Scene_Interactions_through/figures/009_Table_4.jpg]]
*Table 4: Quantitative results across terrain shape variation tasks*

![[assets/figures/papers/paper_list_l1751_TokenHSI_Unified_Synthesis_of_Physical_Human_Scene_Interactions_through/figures/011_Figure_6.jpg]]
*Figure 6: Learning curves comparing the efficiency on terrain shape variation tasks using TokenHSI, Scratch [79], and Adapt-Net [111]. We ablate the adapter layers during training*

![[assets/figures/papers/paper_list_l1751_TokenHSI_Unified_Synthesis_of_Physical_Human_Scene_Interactions_through/figures/014_Figure.jpg]]
*Figure: B. Learning curves comparing the efficiency on longhorizon task completion using TokenHSI, Scratch, and iterative fine-tuning of multiple pre-trained specialist policies, namely Finetune*

![[assets/figures/papers/paper_list_l1751_TokenHSI_Unified_Synthesis_of_Physical_Human_Scene_Interactions_through/figures/013_Table.jpg]]
*Table: A. The overview of all 12 tasks implemented in this paper. Key settings for each task are summarized, including the number of task tokens, the construction of reference motion and object datasets, the episode length, and early termination conditions. The available termination conditions contain character fall, object fall, path distance, and interaction early termination (IET). A slash (/) indicates that the specific configuration is not applicable*

## 方法谱系与知识库定位

### 核心瓶颈与设计动机

物理人-场景交互（HSI）合成面临一个根本性瓶颈：现有控制器通常为单一任务独立设计，缺乏多技能统一与泛化能力。例如，路径跟随、坐下、攀爬、搬运等基础技能各自需要独立的策略网络和奖励工程，当面对需要多技能协同的复杂任务（如“攀爬并搬运物体”）时，这些孤立训练的模型难以有效组合，导致性能急剧下降。TokenHSI 正是针对这一“技能碎片化”问题提出统一解决方案。

### 因果机制：共享本体感知令牌与掩码注意力

TokenHSI 的核心因果调节旋钮在于将角色本体感知（proprioception）建模为独立的共享令牌 $T_{prop}$，并通过 Transformer 中的掩码机制与不同任务令牌结合。这一设计实现了三个层面的知识迁移：

1. **解耦观测空间**：将传统方法中“角色状态与目标状态合并为单一联合观测”的做法，替换为本体感知与任务观测分别独立令牌化。$T_{prop}$ 捕捉角色自身的运动动力学特征，而 $T_f, T_s, T_m, T_c$ 等任务令牌分别编码路径跟随、坐下、攀爬、搬运等任务目标。这种解耦使得跨任务的运动知识可以通过共享的 $T_{prop}$ 自然流动。

2. **可变长输入与掩码注意力**：利用 Transformer 编码器 $\phi$（4层，2个注意力头，512维前馈层）支持可变长输入的特性，单网络可无缝整合任意数量的任务令牌。训练时，通过掩码机制抑制当前无关的任务令牌，使策略仅关注本体感知与目标任务的交互；推理时，通过有限状态机（FSM）自动切换任务标签作为注意力掩码，实现多技能的无缝衔接。

3. **高效策略适应**：在适应新任务时，冻结大部分预训练参数（$T_{prop}, e, H, \phi$），仅训练新增任务令牌和动作头 $H$ 中插入的零初始化适配器层 $\xi^A$。这与全量微调（Finetune）或专门设计适配架构（AdaptNet）形成鲜明对比——TokenHSI 仅需训练少量参数即可将预训练技能泛化到物体形状变化、地形变化乃至长程任务完成等挑战性场景。

### 与基线方法的关系定位

#### 单任务专用策略（Specialist/AMP）

TokenHSI 的直接对比基线是基于 AMP 风格的单任务专用策略（Specialist）。这些策略为每个 HSI 技能独立训练，使用固定长度的 MLP 网络，观测空间为角色状态与目标状态的联合编码。TokenHSI 在四项基础技能上均超越或持平专用策略（Table 1）：Follow 99.7% vs 98.7%，Sit 99.6% vs 98.2%，Climb 99.8% vs 99.7%，Carry 92.2% vs 83.1%。值得注意的是，搬运任务的提升最为显著（+9.1%），这表明共享 $T_{prop}$ 带来的跨任务知识迁移对复杂操作技能尤为关键。

#### 组合动作学习（CML）

CML 方法尝试将多个预训练策略组合以完成复合任务，但其性能受限于各策略独立训练导致的表征不兼容。TokenHSI 在技能组合任务 Climb+Carry 上达到 99.2% 成功率，而 CML 仅为 68.3%，改进版 CML (dual) 甚至降至 51.3%（Table 2）。这一巨大差距的根本原因在于：TokenHSI 的 $T_{prop}$ 在多样化任务上联合训练，习得了更通用的运动表征，而 CML 的基策略仅从单一任务中学习，组合时面临严重的分布偏移。

#### AdaptNet

AdaptNet 是专门设计的策略适应架构基线。在物体形状变化（Chair）任务上，TokenHSI 达到 88.8%，超过 AdaptNet 的 84.5%（Table 3）；在地形变化（Carry）任务上，TokenHSI 达到 74.0%，而 AdaptNet 为 63.4%，Scratch（从头训练）则为 0%（Table 4）。TokenHSI 的优势在于其统一的适配方案——仅需添加适配器层和新任务令牌，避免了 AdaptNet 复杂的架构修改，同时保持了更高的适应效率。

### 消融证据与设计验证

消融实验直接验证了 TokenHSI 关键设计组件的因果作用：

- **移除共享 $T_{prop}$**：在基础技能上，Follow 从 99.7% 降至 99.3%，Sit 从 99.6% 降至 98.7%，Climb 从 99.8% 降至 99.5%，Carry 从 92.2% 降至 90.9%（Table 1）。在技能组合任务 Climb+Carry 上，性能下降更为显著（Table 2）。这证实了共享本体感知令牌是实现跨任务知识迁移的核心机制。

- **移除适配器层**：在策略适应中仅训练新令牌而不使用适配器层，导致地形任务几乎失败——Follow 降至 63%，Carry 降至 10.8%（Table 4）。这表明适配器层在将预训练知识迁移到分布外场景时起着关键的调节作用。

### 适用边界与局限

1. **奖励工程依赖**：TokenHSI 学习技能仍需设计复杂的奖励函数，涉及大量试错。论文中给出的搬运任务奖励函数（Equ. 9, 13, 16）展示了分阶段、多条件的奖励设计复杂度。这限制了方法的可扩展性——每增加一个新技能，都需要人工精心设计奖励结构。

2. **非自主长程任务**：当前的长距离任务完成仍依赖人类设计的有限状态机（FSM）来切换子任务，而非策略自主决策何时切换技能。Figure 7 展示的长期任务完成中，子任务序列是预先编排的，策略仅负责执行各子任务的运动控制。

3. **场景复杂度受限**：实验环境相对简单（平坦地面、规则楼梯、标准物体），扩展到真实世界的复杂场景（不规则地形、多样物体几何、动态障碍）仍有挑战。虽然 TokenHSI 通过引入高度图令牌展示了初步的地形泛化能力，但 Carry 在复杂地形上仅 74.0% 的成功率表明仍有较大提升空间。

### 开放问题

论文明确指出了两个关键开放问题，这些方向也构成了后续工作的潜在路径：

1. **减少奖励工程成本**：如何利用大规模人类数据或互联网知识自动构建或学习奖励函数，从而减少人工设计负担？这指向了基于离线数据或视觉-语言模型引导的奖励学习方向。

2. **全自主长程任务完成**：如何在不依赖人类指导（如 FSM 编排）的情况下，使策略能够自主感知任务进度并决定技能切换时机？这需要策略具备高层任务规划能力，可能涉及分层强化学习或与大语言模型的集成。

### 方法谱系总结

TokenHSI 在物理 HSI 合成领域的方法谱系中占据了“统一多技能策略”这一节点。其上游是单任务专用控制器（AMP 系列）和组合动作学习方法（CML），下游则指向更自主、更少人工干预的交互合成系统。核心贡献在于通过 Transformer 令牌化机制优雅地解决了多技能统一与高效适应的问题，但距离完全自主的复杂场景交互仍有距离。

## 原文 PDF

![[paperPDFs/CVPR_2025/TokenHSI_Unified_Synthesis_of_Physical_Human_Scene_Interactions_through_Task_Tokenization.pdf]]
