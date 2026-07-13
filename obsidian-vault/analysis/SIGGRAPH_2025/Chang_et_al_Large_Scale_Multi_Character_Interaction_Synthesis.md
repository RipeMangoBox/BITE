---
title: Large-Scale Multi-Character Interaction Synthesis
type: paper
paper_level: A
venue: SIGGRAPH
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_2025/Chang_et_al_Large_Scale_Multi_Character_Interaction_Synthesis.pdf
project_link: null
code_link: null
aliases:
- CGPCMCI
- LSMCIS
tags:
- SIGGRAPH_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过将多角色交互分解为两角色组（利用预训练的两角色扩散模型）并引入基于强化学习的过渡规划网络，在无多角色数据的情况下实现了可扩展的协调交互。
primary_logic: 将复杂的多角色协调交互分解为可组合的两角色交互合成（预训练扩散模型）与高层次的过渡规划（强化学习策略），从而在不依赖多角色训练数据的前提下，生成可扩展且平滑的角色间协调交互。
claims:
- We propose a conditional generative pipeline comprising a coordinatable multi-character interaction space for interaction synthesis and a transition planning network for coordinat...
- Our method achieves best transition smoothness (TS) of 0.071 and hip distance (HD) of 1.963, avoiding character overlap compared to InterGen.
- 94.12% of participants prefer our method over InterGen and InterGen† in user study.
- InterHuman dancing subset (4 characters) 上 TS↓ = 0.071
---

# Large-Scale Multi-Character Interaction Synthesis

> [!tip] 核心洞察
> 将复杂的多角色协调交互分解为可组合的两角色交互合成（预训练扩散模型）与高层次的过渡规划（强化学习策略），从而在不依赖多角色训练数据的前提下，生成可扩展且平滑的角色间协调交互。

| 字段 | 内容 |
|------|------|
| 中文题名 | 大规模多角色交互合成 |
| 英文题名 | Large-Scale Multi-Character Interaction Synthesis |
| 会议/期刊 | SIGGRAPH 2025 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Conditional Generative Pipeline for Coordinated Multi-Character Interaction |
| Dataset | InterHuman dancing subset, Adding New Characters, Generating Large Scenes, Transfer to Boxing |

> [!tip] 效果简介
> - InterHuman dancing subset (4 characters) 上，TS↓ 0.071 vs 0.073 (InterGen) (-0.002)；HD 1.963 vs 0.567 (InterGen) (+1.396)。
> - Adding New Characters 上，TS↓ 0.026 vs N/A。
> - Generating Large Scenes (12 characters) 上，TS↓ 0.075 vs N/A。

## 概要

多角色交互合成是计算机动画与具身智能领域的核心挑战，其根本瓶颈在于两个方面：**缺乏多角色密集交互的训练数据**，以及**如何在时空上下文中为多个角色规划接近且密集的交互过渡**。现有方法（如 InterGen）仅支持两角色交互合成，当扩展到多角色场景时，角色间会出现严重重叠，且无法协调交互过渡。

本文提出一种**条件生成流水线**，将复杂的多角色协调交互分解为两个可组合的子问题：**交互合成**与**过渡规划**。核心思路是：利用预训练的两角色扩散模型作为交互生成基座，通过将多角色划分为两角色组并自回归生成各组交互，构建**可协调多角色交互空间**；同时引入基于深度强化学习的**过渡规划网络**，根据观察到的运动片段预测高层次的组重组选择，作为交互合成的条件信号。这一分解策略使得方法**无需任何多角色训练数据**，即可实现可扩展的协调交互。

实验表明，该方法在 4 角色舞蹈场景上达到最佳过渡平滑度（TS=0.071）和髋关节距离（HD=1.963），有效避免了角色重叠；在扩展到 12 角色大场景及迁移到拳击动作时仍保持稳定性能。用户研究中，94.12% 的参与者偏好本方法优于 InterGen 及其增强版本。消融实验进一步验证了可协调空间与规划网络各自的关键作用：移除规划后平滑度急剧劣化（TS 从 0.075 升至 0.202），而移除可协调空间则导致角色严重重叠（HD 降至 0.564）。

本工作的核心贡献在于：**首次实现了无需多角色数据的大规模多角色交互合成**，通过“分解-组合”范式将两角色交互模型与强化学习规划相结合，为多智能体运动生成提供了新的方法论视角。



### 问题背景

生成逼真且协调的多角色交互是计算机图形学与具身人工智能中的核心挑战，直接关系到虚拟现实、动画制作、游戏开发等应用的沉浸感与表现力。随着扩散模型在单角色和两角色运动生成上的突破，研究者开始探索将交互合成扩展到三个及以上角色的场景。然而，**多角色交互合成面临两个根本性瓶颈**：

1. **数据稀缺**：现有交互运动数据集（如 InterHuman）仅包含两角色密集交互的标注数据，缺乏三个及以上角色同时进行紧密交互的训练样本。这直接限制了监督学习方法在此任务上的适用性。
2. **时空协调困难**：多角色场景不仅要求每个角色自身的运动自然，还需要在时空上下文中为多个角色规划接近且密集的交互过渡——即角色之间何时、如何切换交互伙伴，同时避免穿透、重叠等物理不合理现象。

### 现有方法缺口

当前主流的两角色交互生成方法（如 **InterGen**，基于扩散模型的两角色交互合成）在多角色场景下存在明显不足：

- **缺乏多角色协调能力**：InterGen 等模型仅能生成两角色交互，无法处理三个及以上角色的交互组合与过渡规划。当直接扩展到多角色时，角色之间会出现严重重叠（如 Figure 5 所示），交互质量急剧下降。
- **无过渡规划机制**：现有方法缺乏对角色间交互切换的高层次规划，导致生成的交互序列缺乏连贯性和目的性。即使将两角色模型自回归地应用于多角色场景，由于缺少全局协调信号，角色运动往往陷入混乱。

这些缺口的核心在于：**如何在无多角色训练数据的条件下，实现可扩展且平滑的角色间协调交互**。

### 本文动机

针对上述瓶颈，本文提出一个条件生成流水线，通过**分解与组合**的策略绕开数据稀缺问题：

- **分解**：将复杂的多角色协调交互分解为两个可独立处理的子问题——两角色交互合成（利用预训练扩散模型）与高层次的过渡规划（通过强化学习策略实现）。
- **组合**：设计可协调多角色交互空间，将多角色划分为两角色组并自回归生成各组交互，同时引入过渡规划网络预测重组选择，为交互合成提供条件信号。

这一思路的核心洞见在于：**多角色协调交互的本质不在于同时生成所有角色的运动，而在于在合适的时机让合适的角色组成交互对，并确保组间运动的一致性**。通过将协调问题转化为规划问题，该方法在不依赖多角色训练数据的前提下，实现了从4角色到12角色的可扩展交互合成，并支持向拳击等新运动类型的迁移。



## 核心方法与创新机理

### 瓶颈与因果调控

多角色交互合成面临两个核心瓶颈：**缺乏多角色密集交互的训练数据**，以及**如何在时空上下文下为多个角色规划接近且密集的交互过渡**。现有方法（如 InterGen）仅能生成两角色交互，无法在无多角色训练数据的条件下实现可扩展的协调。

本工作的因果调控手段在于将复杂的多角色协调交互**分解为两个可组合的层次**：低层次的两角色交互合成（复用预训练的扩散模型）与高层次的过渡规划（通过强化学习策略网络学习重组选择）。这一分解使得系统在完全不依赖多角色训练数据的前提下，实现了可扩展且平滑的角色间协调交互。

### Changed Slots：相对基线的方法变更

#### Slot 1：交互合成模块

- **基线值（InterGen）**：两角色扩散模型，只能生成两角色交互，不具备多角色协调能力。
- **提出方案**：构建**可协调多角色交互空间**。将 N 个角色划分为两角色组，利用预训练扩散模型对每组进行自回归生成；同时引入基于 proxemics 理论的分类器引导，通过髋关节距离约束（Eq. 4）维护组间社交距离，避免角色重叠。

$$d ( M_{i,j}^{t}, M^{\prime} ) = \frac{1}{|M^{\prime}|} \sum_{n^{\prime}}^{|M^{\prime}|} \min\left( \| p_{i,j} - p_{n^{\prime}} \|_2^2 - \tau , 0 \right)$$

该约束惩罚组间髋关节距离小于阈值 $\tau$ 的情况，从而在生成过程中强制维持合理的社交距离（Section 3.3, Algorithm 1, Figure 3）。

#### Slot 2：过渡协调

- **基线值（InterGen）**：无过渡规划，角色交互随机或手动指定，无法实现有意义的协调过渡。
- **提出方案**：引入**过渡规划网络**，将过渡规划形式化为马尔可夫决策过程（MDP），并通过深度强化学习训练策略网络。该网络根据观察到的四个角色运动片段 $M_{i,j,i',j'}^{t}$，预测高层次的重组选择作为过渡计划 $C^{t}$：

$$C^{t} = f_\theta ( M_{i,j,i',j'}^{t} )$$

训练使用 DQN 框架，奖励函数由**平滑度奖励**（基于 10 帧加速度差）和**多样性奖励**（鼓励新颖的重组选择）组成（Section 3.4, Figure 4）：

$$r_{smooth} = e^{-\| acc^{t} - acc^{t+1} \|_2^2}, \quad r_{div} = \begin{cases} 1, & \text{if } a^t \text{ is novel} \\ 0, & \text{otherwise} \end{cases}$$

### 创新本质：分解-组合范式

核心洞察在于：**将多角色协调交互分解为可组合的两角色交互合成与高层次的过渡规划**。两角色扩散模型负责生成局部的、密集的交互运动；强化学习规划网络负责在全局层面决定“谁与谁在何时交互”。二者通过自回归条件生成框架（Eq. 2）耦合：

$$M_{1:N}^{t} = \mathcal{F}_\theta ( M_{1:N}^{t-1}, \epsilon_{1:N}^{t}, C^{t} )$$

这一分解-组合范式使得系统能够从仅有的两角色交互数据中泛化到任意数量角色的协调场景，同时避免了直接生成多角色运动所需的海量标注数据。



本文提出的多角色交互合成框架是一个自回归条件生成模型，其核心设计思想是将复杂的多角色协调交互分解为两个可组合的子问题：**交互合成**与**过渡规划**。如图 2 所示，整个 pipeline 由两个关键模块串联构成。

**输入与表示。** 多角色交互被形式化为 $T$ 个运动片段的序列，每个片段包含 $N$ 个角色的运动：

$$M_{1:N}^{1:T} = \left[ M_{1:N}^{1}, M_{1:N}^{2}, \cdots, M_{1:N}^{t}, \cdots, M_{1:N}^{T} \right] \tag{1}$$

其中每个片段 $M_{1:N}^{t}$ 是 $N$ 个角色在固定帧数内的运动拼接。框架以自回归方式逐片段生成，第 $t$ 个片段的生成依赖于前一帧片段 $M_{1:N}^{t-1}$、随机噪声 $\epsilon_{1:N}^{t}$ 以及过渡计划 $C^{t}$：

$$M_{1:N}^{t} = \mathcal{F}_\theta ( M_{1:N}^{t-1}, \epsilon_{1:N}^{t}, C^{t} ) \tag{2}$$

**模块一：可协调多角色交互空间。** 该模块负责将多角色交互分解为两角色组，并利用预训练的两角色扩散模型（基于 **InterGen**）自回归地生成各组交互。具体而言，它将 $N$ 个角色划分为若干两角色组，按组依次生成新运动，且后生成组的运动以前已生成组的运动为条件（见 Figure 3 中的红色箭头）。为维持组间合理的社交距离，模块引入了基于 proxemics 理论的分类器引导，通过髋关节距离约束 $d(M_{i,j}^{t}, M')$ 来避免角色重叠。该模块的输出是满足空间协调性的多角色运动片段。

**模块二：过渡规划网络。** 该模块作为策略网络，根据当前观察到的四角色运动 $M_{i,j,i',j'}^{t}$ 预测高层次的重新分组选择作为过渡计划 $C^{t}$：

$$C^{t} = f_\theta ( M_{i,j,i',j'}^{t} ) \tag{7}$$

过渡计划 $C^{t}$ 作为条件信号馈入交互空间模块，指导下一片段中角色间的配对重组。规划网络通过深度强化学习训练，奖励函数由两部分组成：基于加速度差的平滑度奖励 $r_{\text{smooth}} = e^{-\| \text{acc}^{t} - \text{acc}^{t+1} \|_2^2}$，以及鼓励动作新颖性的多样性奖励 $r_{\text{div}}$（动作为新颖分组选择时为 1，否则为 0）。

**数据流闭环。** 整个框架形成闭环：交互空间模块生成当前片段的多角色运动 → 规划网络观察运动并预测下一过渡计划 → 过渡计划作为条件驱动下一片段的交互合成。这一设计使得框架能够仅依赖两角色交互数据训练，即可泛化到任意数量角色的协调交互场景，无需多角色密集交互的真值数据。

### 补充图表

![[assets/figures/papers/paper_list_l1926_Chang_et_al_Large_Scale_Multi_Character_Interaction_Synthesis/figures/002_Figure_2.jpg]]
*Figure 2: Framework overview. Our pipeline is an autoregressive conditional generative model to plan transitions and synthesize interactions for multiple characters. It has two components: The first component divides multiple characters into groups and leverages a pre-trained diffusion-based model to autoregressively generate interactions for each group. The second component predicts a transition plan based on the observed interactions and serves as the conditional signal for the interaction synthesis*

![[assets/figures/papers/paper_list_l1926_Chang_et_al_Large_Scale_Multi_Character_Interaction_Synthesis/figures/001_Figure_1.jpg]]
*Figure 1: Multi-character interactions coordinated with transition planning. (Left) We highlight the three currently interacting characters with blue, purple, and green, while others are grey. The more saturated the color, the more recent the frame. (Upper right) The key frame of the transition where the blue and purple characters proceed to have a coordinated interaction. (Lower right) The key frame of the transition where the blue and green characters proceed to have a coordinated interaction*



### 多角色交互表示

本方法将多角色交互形式化为一个时序运动片段序列。对于 $N$ 个角色在 $T$ 个时间片段上的交互，其整体表示如公式 (1) 所示：

$$M_{1:N}^{1:T} = \left[ M_{1:N}^{1}, M_{1:N}^{2}, \cdots, M_{1:N}^{t}, \cdots, M_{1:N}^{T} \right]$$

其中，第 $t$ 个运动片段 $M_{1:N}^{t}$ 包含 $N$ 个角色在该片段内的运动数据。每个角色 $n$ 的运动表示为 $m_n^t$，整个片段由所有角色的运动拼接而成。

### 自回归条件生成框架

整个管线被构建为一个自回归条件生成模型。给定前一运动片段 $M_{1:N}^{t-1}$、噪声 $\epsilon_{1:N}^{t}$ 以及过渡计划 $C^t$，生成下一运动片段：

$$M_{1:N}^{t} = \mathcal{F}_\theta ( M_{1:N}^{t-1}, \epsilon_{1:N}^{t}, C^{t} )$$

这里 $\mathcal{F}_\theta$ 是条件生成函数，$C^t$ 是由过渡规划网络预测的高层重组选择，作为条件信号指导生成过程。

### 可协调多角色交互空间

核心创新之一是将多角色分解为两角色组，利用预训练的两角色扩散模型进行分组自回归生成。对于过渡计划 $C^t$ 中指定的每个组 $(i,j)$，该组的运动通过与已生成组 $M'$ 的条件关系生成：

$$M_{1:N}^{t} = \left[ g ( M_{i,j}^{t-1}, M' ) , \text{ for } (i,j) \in C^{t} \right]$$

其中 $g$ 是预训练的两角色扩散模型，$M'$ 代表已生成的相邻组运动。这种分组机制使得方法能够在无多角色训练数据的情况下，通过组合两角色交互实现可扩展的多角色协调。

为维护组间的合理社交距离，方法引入基于 proxemics 理论的髋关节距离约束，通过分类器引导施加：

$$d ( M_{i,j}^{t}, M' ) = \frac{1}{|M'|} \sum_{n'}^{|M'|} \min\left( \| p_{i,j} - p_{n'} \|_2^2 - \tau , 0 \right)$$

其中 $p_{i,j}$ 表示组内角色的髋关节位置，$p_{n'}$ 是已生成组中角色的髋关节位置，$\tau$ 是距离阈值。该约束仅在组间距离小于 $\tau$ 时产生惩罚，有效防止角色重叠。

### 过渡规划网络

过渡规划被形式化为马尔可夫决策过程，并通过深度强化学习训练策略网络。规划网络以四个相关角色的运动为输入，输出重组选择作为过渡计划：

$$C^{t} = f_\theta ( M_{i,j,i',j'}^{t} )$$

其中状态 $s := M_{i,j,i',j'}$ 包含当前交互的两组角色（共四个角色）的运动片段，动作空间由可能的重新分组方式构成。

**奖励设计**是训练的关键。平滑度奖励基于相邻片段间的加速度差异：

$$r_{smooth} = e^{-\| acc^{t} - acc^{t+1} \|_2^2}$$

该奖励在 10 帧窗口上计算加速度差的 L2 范数，通过指数函数将其映射到 $(0,1]$ 区间，鼓励过渡前后运动加速度的一致性。

多样性奖励则鼓励探索新颖的过渡模式：

$$r_{div} = \begin{cases} 1, & \text{if } a^t \text{ is novel} \\ 0, & \text{otherwise} \end{cases}$$

当规划网络选择的动作 $a^t$ 是之前未出现过的重组方式时，给予正向奖励，从而促进交互模式的多样性。两个奖励通过加权组合共同指导策略网络的训练。

### 评估指标

在实验评估中，方法使用两个核心指标量化交互质量。髋关节距离（Hip Distance, HD）衡量角色间的空间分离程度：

$$HD = \frac{2}{N(N-1)F} \sum_{f=1}^{F} \sum_{i,j \in N} \| h_i^f - h_j^f \|_2^2$$

其中 $h_i^f$ 表示角色 $i$ 在第 $f$ 帧的髋关节位置，$F$ 为总帧数。该指标对所有角色对在所有帧上的平均平方髋关节距离进行计算，值越大表示角色间距离越远、重叠越少。过渡平滑度（Transition Smoothness, TS）则衡量运动片段衔接处的加速度连续性，值越低表示过渡越平滑。

### 补充图表

![[assets/figures/papers/paper_list_l1926_Chang_et_al_Large_Scale_Multi_Character_Interaction_Synthesis/figures/003_Figure_3.jpg]]
*Figure 3: Coordinatable multi-character interaction space by group division. We divide multiple characters into groups and re-group them for potential coordination. The group synthesis generates new motions group by group. The newly generated group is conditioned on the already generated ones, which is indicated by red arrows*

![[assets/figures/papers/paper_list_l1926_Chang_et_al_Large_Scale_Multi_Character_Interaction_Synthesis/figures/004_Figure_4.jpg]]
*Figure 4: The planning network is learned as a policy network via deep reinforcement learning. The action is a transition plan that contains a high-level grouping choice*



## 实验与关键发现

### 主结果：多角色交互合成的定量与定性评估

本文在 InterHuman 数据集的四人跳舞子集上进行主要定量对比，评估指标为过渡平滑度（Transition Smoothness, TS）和髋关节距离（Hip Distance, HD）。TS 衡量相邻运动片段衔接的连贯性，值越低越好；HD 衡量所有角色对在所有帧上的平均平方髋关节距离，用于评估角色重叠程度。完整方法在 TS 上达到 **0.071**，优于 InterGen 的 0.073；在 HD 上达到 **1.963**，远高于 InterGen 的 0.567（Table 1）。HD 的显著提升表明本方法有效避免了 InterGen 中常见的角色严重重叠问题——InterGen 的 HD 仅 0.567，意味着角色几乎贴在一起，缺乏合理的社交距离。

![[assets/figures/papers/paper_list_l1926_Chang_et_al_Large_Scale_Multi_Character_Interaction_Synthesis/figures/005_Table_1.jpg]]
*Table 1: Comparison with interaction synthesis models. † represents our implementation of the coordinatable interaction space in the original method. TS denotes transition smoothness and HD, the hip distance*

![[assets/figures/papers/paper_list_l1926_Chang_et_al_Large_Scale_Multi_Character_Interaction_Synthesis/figures/014_Table_1.jpg]]
*Table 1: Allowing three-character division choice*

定性对比同样佐证了上述结论。Figure 5 展示了本方法与 InterGen 的生成结果对比：InterGen 生成的四个角色在空间中严重重叠，而本方法通过过渡规划网络协调角色间的分组切换，保持了清晰的空间分离。Figure 6 进一步通过髋关节距离的密度分布揭示了方法差异：本方法的 HD 密度呈现双峰分布，分别对应角色在交互组内（近距离）和组间（远距离）的两种状态，体现了清晰的过渡行为；InterGen†（仅加入可协调交互空间但无规划网络）呈现单峰分布，缺乏过渡规划能力；InterGen 的分布曲线形状与 InterGen† 相似，但峰值对应的距离值远更小，确认了角色严重重叠的问题。

![[assets/figures/papers/paper_list_l1926_Chang_et_al_Large_Scale_Multi_Character_Interaction_Synthesis/figures/006_Figure_5.jpg]]
*Figure 5: (a) An example result from our method. (b) An example from InterGen where characters heavily overlap*

![[assets/figures/papers/paper_list_l1926_Chang_et_al_Large_Scale_Multi_Character_Interaction_Synthesis/figures/007_Figure_6.jpg]]
*Figure 6: The density of hip distance for the three methods evaluated. The two modes in our hip distance density demonstrate minimal character overlap and clear transitions. InterGen† does not have the ability of transition planning, leading to an averaged distance density with a single mode. InterGen has a similar curve shape with InterGen as both of them do not have transition planning. Its much smaller mode value indicates that characters heavily overlap*

用户研究结果提供了更强的主观证据：在 94.12% 的对比中，参与者偏好本方法优于 InterGen 和 InterGen†（Supplementary Section 2.1），表明所生成的协调交互在视觉自然度上获得了高度认可。

### 扩展应用验证

Table 2 展示了方法在三个扩展场景下的表现。在**添加新角色**场景中，TS 达到 0.026，HD 为 2.450，说明系统能平滑地将新角色融入已有交互。在**大规模场景生成**（12 个角色）中，TS 为 0.075，HD 为 3.372，验证了方法的可扩展性——即使角色数从 4 扩展到 12，过渡平滑度仅轻微退化，且髋关节距离保持在合理范围。在**跨动作类型迁移**（拳击）中，TS 为 0.057，表明预训练的两角色扩散模型与过渡规划网络的组合可以泛化到训练时未见过的动作类型，尽管拳击的交互模式与跳舞存在本质差异。

![[assets/figures/papers/paper_list_l1926_Chang_et_al_Large_Scale_Multi_Character_Interaction_Synthesis/figures/008_Table_2.jpg]]
*Table 2: Method performance on extended applications. TS denotes transition smoothness and HD, the hip distance*

![[assets/figures/papers/paper_list_l1926_Chang_et_al_Large_Scale_Multi_Character_Interaction_Synthesis/figures/013_Table_2.jpg]]
*Table 2: Diversity as a quantitative metric*

### 消融实验：组件贡献分析

Table 4 的消融实验系统性地揭示了各组件的贡献。**移除可协调交互空间和规划网络**（即仅使用原始 InterGen 自回归生成）时，HD 仅为 0.564，TS 为 0.071——角色严重重叠，但过渡平滑度尚可，因为此时角色几乎静止重叠，片段间加速度差异小。**仅保留可协调交互空间但移除规划网络**（InterGen†）时，TS 急剧劣化至 **0.202**，HD 上升至 3.422——分类器引导的社交距离约束虽然拉开了角色距离，但缺乏智能的过渡规划导致片段衔接生硬。**完整方法**实现了 TS=0.075 和 HD=3.372 的最佳平衡，证明两个组件是互补的：可协调空间提供组间距离约束，规划网络提供平滑的过渡信号。

![[assets/figures/papers/paper_list_l1926_Chang_et_al_Large_Scale_Multi_Character_Interaction_Synthesis/figures/018_Table_4.jpg]]
*Table 4: An ablation study on method scaling*

### 距离阈值 τ 的敏感性分析

Table 5 展示了社交距离约束中的阈值 τ 从 0.5 增大到 3.0 的影响。随着 τ 增大，TS 从 0.059 单调上升至 0.092，HD 从 1.723 单调上升至 2.355。这表明平滑度与社交距离之间存在明确的权衡关系：更大的距离阈值强制角色保持更远的距离，但增加了运动衔接的难度，导致过渡不够平滑。该结果为实际部署中的参数选择提供了指导——需根据应用场景对自然度和安全距离的偏好来调节 τ。

![[assets/figures/papers/paper_list_l1926_Chang_et_al_Large_Scale_Multi_Character_Interaction_Synthesis/figures/016_Table_5.jpg]]
*Table 5: an ablation study on the distance threshold*

### 失败模式与局限性

尽管方法在定量和定性评估中表现优异，仍存在若干已知局限。首先，**分组策略基于简单的贪婪距离度量**，可能不是最优的分组方式，在复杂场景下可能导致不自然的角色配对。其次，**当角色总数不能被 4 整除时需引入虚拟角色**，虚拟角色的运动由扩散模型自由生成，可能引入不协调的运动模式，影响整体交互质量。第三，**扩散模型在无条件数据集时的控制精度下降**——本方法依赖两角色扩散模型进行组内交互生成，但该模型仅在两角色数据上训练，当通过分类器引导施加组间约束时，生成质量可能受损。这些失败模式提示，在极端场景（如奇数角色数、高度非结构化的交互类型）下，方法的表现需要手动验证。



## 定位与知识库关联

### 与现有工作的关系

本文方法直接构建在两角色交互扩散模型 **InterGen** 之上，将其作为预训练的两角色交互合成引擎。InterGen 本身仅能处理两个角色之间的交互生成，不具备多角色协调能力。本文的核心贡献在于为 InterGen 添加了两个关键组件，使其能够扩展至大规模多角色场景：

1. **可协调多角色交互空间**：将 N 个角色动态划分为若干两角色组，利用 InterGen 对各组进行自回归生成。在生成过程中，通过分类器引导施加基于 proxemics 理论的髋关节距离约束（Eq. 4），强制维持组间角色的社交距离，从而避免角色重叠。这一设计使得多角色交互合成可以在不依赖多角色训练数据的条件下实现。

2. **过渡规划网络**：将多角色交互中的重组选择（即哪些角色在下一片段中编组交互）建模为马尔可夫决策过程，使用深度强化学习训练一个策略网络来预测过渡计划。该网络以观察到的四个角色运动为状态，输出高层次的编组选择作为动作，并通过平滑度奖励（$r_{smooth}=e^{-\|acc^t - acc^{t+1}\|_2^2}$）和多样性奖励（$r_{div}$ 为二进制新颖性奖励）进行优化。

在实验比较中，作者引入了 **InterGen†** 作为消融基线——即仅添加可协调交互空间但移除过渡规划网络的变体。这一设计清晰地分离了两个组件的贡献：InterGen 代表纯两角色模型（无协调能力），InterGen† 代表有空间约束但无智能规划，完整方法则兼具两者。

从方法谱系来看，本文工作属于“组合式生成+规划”范式：将复杂的多智能体协调问题分解为可组合的局部交互生成（预训练扩散模型）与高层次的全局过渡规划（强化学习策略）。这种分解策略与机器人领域的层次化规划、多智能体强化学习中的集中训练分散执行等思想有方法论上的呼应，但在角色动画合成领域属于首次探索。

### 适用边界

**有效适用场景**：
- 角色总数 $N$ 为 4 的倍数时，方法表现最优。此时分组策略可将所有角色完美划分为两角色组，无需引入虚拟角色。
- 交互类型为舞蹈、拳击等具有明确两角色交互模式的运动类型。方法在 InterHuman 舞蹈子集和拳击迁移实验上均取得了可接受的平滑度（TS 分别为 0.071 和 0.057）。
- 场景规模可扩展至 12 个角色（Table 2），且支持动态添加新角色（TS=0.026, HD=2.450）。

**适用受限场景**：
- 当角色总数不能被 4 整除时，需引入虚拟角色来补全分组，这可能影响交互质量。论文未对虚拟角色引入后的质量退化进行定量分析，该点需要手动验证。
- 分组策略基于简单的贪婪距离选择，未考虑更复杂的交互语义或角色关系，可能在需要特定角色配对时表现不佳。
- 扩散模型的控制精度在没有条件数据集的情况下可能下降，这限制了方法向全新交互类型的零样本迁移能力。

### 局限与开放问题

**已明确的局限**（来自论文原文与消融实验）：

1. **分组刚性**：方法将多角色严格划分为两角色组，无法直接处理三个或更多角色同时进行密集交互的场景。这一限制源于训练数据仅包含两角色交互，属于数据驱动的根本性瓶颈。

2. **距离阈值权衡**：消融实验（Table 5）揭示了平滑度与社交距离之间的固有权衡——当距离阈值 $\tau$ 从 0.5 增大到 3.0 时，TS 从 0.059 升至 0.092（平滑度下降），HD 从 1.723 升至 2.355（角色间距增大）。这表明维持社交距离会牺牲运动平滑性，需要在应用中根据需求进行折中。

3. **缺乏多角色真值评估**：由于不存在多角色密集交互的真值数据集，定量评估只能依赖间接指标（TS 和 HD），无法直接衡量交互的真实感和语义正确性。用户研究（94.12% 偏好率）提供了主观验证，但样本量和评估维度有限。

4. **公平性未量化**：论文在补充材料中承认合成运动可能存在偏向性（训练数据代表性不足），并提出了数据增强和扩散少数群体采样等缓解方案，但未进行定量公平性评估。

**开放问题**：

- 如何在缺少条件数据集的情况下提高扩散模型的控制精度，使方法能更可靠地迁移至全新交互类型？
- 如何收集或合成两个以上角色的密集交互数据，以突破两角色分组的基本限制？
- 当角色总数不能被 4 整除时，是否存在比引入虚拟角色更优雅的解决方案？
- 能否利用第一人称感受野、图神经网络或其他更智能的策略替代当前的贪婪距离分组？
- 在缺乏直接可比真值的情况下，如何设计更全面的定量评估指标（如交互语义一致性、角色意图合理性）？

### 证据强度评估

本文的核心声明均有较强的实验支撑：主实验（Table 1）在 InterHuman 舞蹈子集上对比了三种方法，完整方法在 TS 和 HD 上均取得最优或接近最优结果；消融实验（Table 4）系统验证了两个组件的独立贡献；用户研究提供了主观质量背书。扩展实验（Table 2）验证了方法的可扩展性和跨类型迁移能力。

需要注意的是，HD 指标的解读存在微妙之处：InterGen 的 HD 极低（0.567），看似“更好”，实则是角色严重重叠的负面表现（Figure 5b 和 Figure 6 提供了视觉证据）。完整方法的 HD 为 1.963，反映了角色维持了合理的社交距离。这一指标的“好坏”方向依赖于具体上下文，读者需结合定性结果综合判断。



## 原文 PDF

![[paperPDFs/SIGGRAPH_2025/Chang_et_al_Large_Scale_Multi_Character_Interaction_Synthesis.pdf]]
