---
title: UniHSI Unified Human Scene Interaction via Prompted Chain of Contacts
type: paper
paper_level: A
venue: ICLR
year: 2024
pdf_ref: paperPDFs/ICLR_2024/UniHSI_Unified_Human_Scene_Interaction_via_Prompted_Chain_of_Contacts.pdf
project_link: null
code_link: null
aliases:
- UUHSIPCC
tags:
- ICLR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将交互统一表述为有序的关节-物体部件接触对序列（接触链，CoC），利用大语言模型（LLM）将语言指令自动规划为CoC，并通过统一控制器中的TaskParser将CoC转化为统一的观测和奖励信号，实现无需任务特定工程和交互标注的多样化物理交互。
primary_logic: 交互类型与接触区域之间存在强相关性，因此任何交互都可以分解为有序的接触步骤，每一步定义哪些关节应与哪些物体部件接触及方向；这种结构化表示使得语言模型能够理解并生成交互计划，而物理控制器可以统一执行，无需为每个交互收集专门的动作数据。
claims:
- 在ScenePlan数据集的简单任务上，完整UniHSI的成功率达到85.5%，而移除自适应权重后骤降至21.2%，验证了自适应权重对统一控制的关键作用。
- 在Lie Down等复杂交互任务上，UniHSI的成功率为81.5%，远高于AMP-Vanilla Combination的20.1%，表明统一表示和多步规划显著提升了困难任务的执行能力。
- 使用GPT-4作为LLM规划器时，任务规划正确率达71.9%，执行成功率达57.3%，显著优于GPT-3.5（49.1%和35.6%），证实了规划质量对最终执行效果的影响。
- ScenePlan (PartNet, Simple) 上 Success Rate (%) = 85.5
---

# UniHSI Unified Human Scene Interaction via Prompted Chain of Contacts

> [!tip] 核心洞察
> 交互类型与接触区域之间存在强相关性，因此任何交互都可以分解为有序的接触步骤，每一步定义哪些关节应与哪些物体部件接触及方向；这种结构化表示使得语言模型能够理解并生成交互计划，而物理控制器可以统一执行，无需为每个交互收集专门的动作数据。

| 字段 | 内容 |
|------|------|
| 中文题名 | UniHSI：基于提示链式接触的统一人-场景交互 |
| 英文题名 | UniHSI Unified Human Scene Interaction via Prompted Chain of Contacts |
| 会议/期刊 | ICLR 2024 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | UniHSI |
| Dataset | ScenePlan, Sit, Lie Down, Reach |

> [!tip] 效果简介
> - ScenePlan (PartNet, Simple) 上，Success Rate (%) 85.5 vs 21.2 (wo Adaptive Weights) (+64.3)。
> - Sit (Single Task) 上，Success Rate (%) 94.3 vs 93.7 (InterPhys-Sit) (+0.6)。
> - Lie Down 上，Success Rate (%) 81.5 vs 21.3 (AMP-Lie Down) (+60.2)。

## 概要

物理仿真中的人-场景交互长期面临一个根本性瓶颈：**每个交互任务都需要独立手工设计目标函数和策略网络**，缺乏统一的交互表述界面。这导致现有方法难以扩展到多样化、长时程、多物体交互场景，且严重依赖昂贵的交互标注数据。

UniHSI 的核心洞察在于**交互类型与接触区域之间存在强相关性**——任何交互都可以分解为有序的接触步骤，每一步明确定义哪些人体关节应与哪些物体部件以何种方式接触。基于此，UniHSI 提出**接触链（Chain of Contacts, CoC）**作为统一的交互表示，并构建了由 LLM Planner 和 Unified Controller 组成的两级框架：高层利用大语言模型将自然语言指令自动规划为 CoC 计划，低层通过统一控制器执行计划并生成物理仿真中的全身运动。

**关键因果机制**：CoC 将交互统一表述为有序的关节-物体部件接触对序列，配合 TaskParser 将其转化为统一的观测和奖励信号，从而**消除了对任务特定工程和交互标注数据的依赖**。自适应接触权重模块根据优化进度动态分配奖励权重，使难优化的接触获得更高关注，是实现统一控制的关键组件。

实验表明，在 ScenePlan 数据集的简单任务上，完整 UniHSI 的成功率达到 **85.5%**，而移除自适应权重后骤降至 21.2%（Table 2），验证了该模块对统一控制的核心作用。在 Lie Down 等复杂交互任务上，UniHSI 的成功率为 **81.5%**，远超 AMP-Vanilla Combination 的 20.1%（Table 3），表明统一表示和多步规划显著提升了困难任务的执行能力。使用 GPT-4 作为 LLM 规划器时，任务规划正确率达 **71.9%**，执行成功率达 57.3%，显著优于 GPT-3.5 的 49.1% 和 35.6%（Table 4），证实了规划质量对最终执行效果的影响。

**方法定位**：UniHSI 在方法谱系中处于物理仿真交互与语言驱动控制的交汇点。相较于仅控制少量关节的 **NSM**（Starke et al., 2019）、**SAMP**（Hassan et al., 2021a）和基于固定接触奖励的 **InterPhys**（Hassan et al., 2023），UniHSI 实现了全身 15 个关节的统一控制；相较于使用 BERT 进行语言映射的 **PADL**（Juravsky et al., 2022），UniHSI 利用 LLM 的世界知识实现了更灵活的多步规划。

**主要局限与开放问题**：LLM 规划器可能产生空间关系错误或不可执行的操作；当前系统假设物体为静态，不支持可移动物体交互；运动真实性的客观评估指标仍有待建立。如何将 LLM 无缝集成到强化学习训练循环中、如何扩展至动态物体交互，以及如何利用视觉-语言模型减少场景标注依赖，是值得探索的方向。

### 问题背景

在虚拟现实、具身智能和机器人学中，让虚拟角色在物理仿真环境中根据自然语言指令与三维场景进行自然交互，是一个核心且长期的研究目标。这类人-场景交互（Human-Scene Interaction, HSI）需要同时满足物理真实性、语义准确性和动作自然度三重约束，涉及感知、规划和控制等多个层面的协同。

### 现有方法的瓶颈

当前物理仿真驱动的人-场景交互方法面临一个根本性瓶颈：**缺乏统一的交互界面和任务表述**。具体而言：

1. **任务特定设计泛滥**：现有方法如 **NSM**（Starke et al., 2019）、**SAMP**（Hassan et al., 2021a）和 **InterPhys**（Hassan et al., 2023）等，每个交互任务都需要手工设计独立的目标函数和策略网络。例如，坐下的接触奖励与躺下完全不同，无法复用。这导致系统难以扩展到多样化、长时程、多物体交互场景。

2. **依赖昂贵的交互标注数据**：基于运动先验的方法（如 **AMP**，Peng et al., 2021）需要为每种交互收集大量高质量的动作捕捉数据来训练判别器，数据获取成本极高，且覆盖的交互类型有限。

3. **语言理解与物理执行的脱节**：**PADL**（Juravsky et al., 2022）尝试用BERT将语言指令映射到物理交互，但其任务空间仍受限于预定义的简单映射，缺乏对复杂多步交互的推理能力。

4. **场景感知能力不足**：多数方法对环境几何信息的利用有限，缺乏显式的高度感知机制，导致在复杂场景中容易发生穿透或碰撞。

### 核心洞察与动机

本文的核心洞察是：**交互类型与接触区域之间存在强相关性**。任何人类与物体的交互——无论是坐椅子、躺沙发还是伸手够杯子——本质上都可以分解为一系列有序的“关节-物体部件”接触步骤。例如，“坐到椅子上”可以表述为：首先臀部接触椅面，然后背部接触椅背，同时手部不接触任何物体。

这一观察引出了三个关键动机：

- **统一表示的可能性**：如果将交互定义为结构化的接触序列（Chain of Contacts, CoC），那么所有交互类型都可以用同一套语言描述，无需为每个任务单独设计目标。

- **语言模型的可介入性**：CoC的五元组结构（物体、部件、关节、接触类型、方向）恰好是大型语言模型能够理解和生成的形式，使得自然语言指令到交互计划的自动翻译成为可能。

- **统一控制的可行性**：一旦交互被统一表示为CoC，底层控制器只需要学会“执行接触序列”这一件事，而非为每个任务学习不同的策略，从而实现真正的统一控制。

基于以上洞察，UniHSI提出了一个两阶段框架：高层LLM规划器将自然语言指令转化为CoC计划，低层统一控制器在物理仿真中执行该计划，从而在不依赖任务特定工程和交互标注数据的前提下，实现多样化的物理人-场景交互。

## 核心方法与创新机理

UniHSI 的核心创新在于将异构的人-场景物理交互统一为一种结构化表示——**接触链（Chain of Contacts, CoC）**，并构建了一个由大语言模型驱动规划、统一物理控制器执行的双层框架。这一设计从根本上改变了此前方法“一任务一策略”的范式，实现了从语言指令到全身物理交互的端到端统一。

### 1. 统一交互表示：接触链（CoC）

此前方法（如 **InterPhys** (Hassan et al., 2023)、**PADL** (Juravsky et al., 2022)）为每种交互任务手工设计特定的目标函数和状态表示，缺乏跨任务的统一界面。UniHSI 的核心洞察在于：**交互类型与接触区域之间存在强相关性**——任何物理交互都可以分解为一系列有序的“关节-物体部件”接触对。

基于这一洞察，UniHSI 将交互统一表述为接触链 $\mathcal{C} = \{ S_1, S_2, \ldots \}$（Eq. 1），其中每个步骤 $S$ 包含多个接触五元组 $\{ o, p, j, c, d \}$（Eq. 2），分别指定：
- **物体 $o$** 与 **部件 $p$**：明确交互的目标物体及其语义部件（如“椅子座位”）；
- **关节 $j$**：指定参与接触的人体关节（UniHSI 支持 15 个全身关节，而此前方法如 **NSM** (Starke et al., 2019) 仅控制少量关节，见 Table 1）；
- **接触类型 $c$**：区分“接触”、“不接触”、“不关心”三种模式；
- **相对方向 $d$**：定义关节到目标部件的期望方向向量。

这一结构化表示具有双重优势：一方面，它足够抽象，使得语言模型能够理解并生成交互计划；另一方面，它又足够具体，使得物理控制器可以将其直接转化为统一的观测和奖励信号，无需为每个交互收集专门的动作数据。

### 2. LLM 驱动的任务规划

传统方法依赖预定义的步骤序列或基于规则的简单映射来生成交互计划，难以泛化到多样化、长时程的复杂交互。UniHSI 引入 **LLM Planner** 模块（Sec 3.2, Fig. 3），利用大语言模型的世界知识，将自然语言指令与场景背景信息（物体部件标注）自动转化为多步 CoC 计划。

LLM Planner 的输入包括场景中所有物体的部件列表和用户的自然语言命令，输出为结构化的接触链。这一设计实现了**零样本任务规划**——无需为每种新交互设计专门的规划逻辑。实验表明，使用 GPT-4 作为规划器时，任务规划正确率达 71.9%，执行成功率达 57.3%（Table 4），显著优于 GPT-3.5（49.1% 和 35.6%），验证了更强 LLM 对规划质量的关键作用。

### 3. 统一控制器中的关键设计

在物理执行层面，UniHSI 的 **Unified Controller** 基于 AMP（Adversarial Motion Prior）框架（**AMP** (Peng et al., 2021)），但引入了三项关键创新，使其能够统一执行多样化的接触计划：

**（1）TaskParser：从 CoC 到统一观测与奖励**

TaskParser 模块（Fig. 4a）将 CoC 中的每个接触五元组转化为统一的观测特征和分段奖励函数 $R_k$（Eq. 7）。根据接触类型，奖励机制自动切换：
- 当 $c_k = \text{contact}$ 时，鼓励关节接近目标部件且方向正确；
- 当 $c_k = \text{not contact}$ 时，惩罚关节接近目标部件；
- 当 $c_k = \text{not care}$ 时，该接触对不产生奖励。

这一设计使得同一控制器无需修改即可处理“坐”（臀部接触座位）、“躺”（多关节接触床面）、“伸手”（手部接触目标）等截然不同的任务。

**（2）自适应接触权重**

多步交互中不同接触对的优化难度差异显著。固定经验权重（此前方法的通用做法）会导致简单接触对过拟合而困难接触对欠优化。UniHSI 提出**自适应权重机制**（Eq. 8）：

$$w_k = \frac{1 - R_k}{n - \sum_{i=1}^n R_i + e}$$

该机制根据当前奖励值动态分配权重：奖励低的接触对（难优化）获得更高权重，奖励高的接触对（已学会或未使用）权重自动降低。消融实验（Table 2）显示，移除自适应权重后，简单任务的成功率从 85.5% 骤降至 21.2%，验证了这一设计对统一控制的关键作用。

**（3）自我中心高度图**

为赋予角色场景几何感知能力，UniHSI 构建了**自我中心高度图**（Fig. 4b），采样角色周围的物体高度信息用于避障。消融实验表明，移除高度图后困难任务的成功率降至 0%（Table 2），证明环境感知对复杂场景至关重要。这一设计弥补了此前方法（如 **SAMP** (Hassan et al., 2021a)）缺乏显式场景感知的不足。

### 4. 相对于基线的关键差异总结

| 设计维度 | 此前方法 | UniHSI |
|---------|---------|--------|
| 任务表示 | 手工设计的任务特定目标 | 统一的 CoC 五元组 |
| 任务规划 | 预定义步骤或规则映射 | LLM 自动生成多步计划 |
| 奖励权重 | 固定经验权重 | 自适应动态权重 |
| 场景感知 | 有限或无显式高度信息 | 自我中心高度图 |
| 控制关节 | 少量关节（如盆骨、手） | 全身 15 个关节 |
| 语言接口 | 无或受限（如 PADL 使用 BERT） | 自然语言指令 |

这些创新共同实现了 **无需任务特定工程和交互标注** 的多样化物理交互，使得 UniHSI 在复杂任务（如 Lie Down）上达到 81.5% 的成功率，远超 AMP-Vanilla Combination 的 20.1%（Table 3）。

UniHSI 的整体设计遵循“高层规划 + 低层执行”的分层架构，将任意人-场景交互统一为**提示链式接触（Chain of Contacts, CoC）** 的生成与物理执行过程。系统由两大核心组件构成：**LLM Planner** 与 **Unified Controller**，二者通过 CoC 这一结构化表示实现解耦与协同。

### 输入输出流

系统的输入为**自然语言指令**与**场景背景信息**（包括场景中物体的部件标注与空间位置）。LLM Planner 接收上述输入后，将其转化为一个有序的接触步骤序列，即 CoC 计划。Unified Controller 则按步骤执行该计划，在物理仿真环境中生成全身运动，最终输出符合指令语义的交互动作。

### 核心组件关系

**LLM Planner**（详见第 3.2 节）负责将语言指令翻译为 CoC。它利用大语言模型的世界知识，根据场景中可用的物体与部件，规划出每一步应有哪些人体关节与哪些物体部件发生何种类型的接触。这一过程将模糊的语言意图转化为精确的、可被控制器消费的结构化任务描述。

**Unified Controller**（详见第 3.3 节）基于对抗运动先验（AMP）框架构建，其内部包含三个关键子模块：

- **TaskParser**：将 CoC 计划中的每个接触步骤解析为统一的**任务观测**与**奖励信号**。这是实现“统一界面”的关键——无论交互类型如何变化，控制器始终消费相同格式的观测与奖励，无需为不同任务设计独立的奖励函数或状态表示。
- **Motion Discriminator**：对抗判别器，提供运动风格奖励，确保生成的动作保持自然、逼真的人体运动模式。
- **Adaptive Weights Module**：动态平衡各接触对的奖励权重，使优化困难的接触对获得更高的权重，从而提升整体训练效率与成功率。

此外，控制器还集成了**自我中心高度图（Ego-centric Heightmap）**，使角色能够感知周围物体的高度信息，从而在导航和交互过程中有效避障。

### 统一性的关键设计

图 4(a) 对比了传统任务特定设计与 UniHSI 统一设计的差异。在传统方法中，每个交互任务需要独立的观测空间、奖励函数和策略网络设计；而 UniHSI 通过 **CoC 统一接口**与 **TaskParser** 的解耦，使得所有任务共享同一套控制器架构。CoC 将交互抽象为“关节-物体部件接触对”的有序序列，TaskParser 则负责将这一抽象表示转化为具体的物理奖励信号，从而屏蔽了底层任务的差异性。

![[assets/figures/papers/paper_list_l1780_UniHSI_Unified_Human_Scene_Interaction_via_Prompted_Chain_of_Contacts/figures/003_Figure_2.jpg]]
*Figure 2: Comprehensive Overview of UniHSI. The entire pipeline comprises two principal components: the LLM Planner and the Unified Controller. The LLM Planner processes language inputs and background scenario information to generate multi-step plans in the form of CoC. Subsequently, the Unified Controller executes CoC step by step, producing interaction movements*

UniHSI 的整体框架由两个核心组件构成：**LLM Planner** 和 **Unified Controller**（图2）。LLM Planner 负责将自然语言指令转化为结构化的接触链（Chain of Contacts, CoC）计划；Unified Controller 则在物理仿真环境中逐步执行该计划，生成全身交互运动。

### 3.1 接触链（Chain of Contacts）

UniHSI 的核心洞察是：**任何交互都可以分解为有序的接触步骤序列**。每个步骤明确定义了哪些人体关节应与哪些物体部件接触，以及接触的方向。这一结构化表示构成了统一交互界面的基础。

交互被形式化定义为接触链 $\mathcal{C}$：

$$\mathcal{C} = \{ S_1, S_2, \ldots \}$$

其中每个接触步骤 $S$ 包含若干接触五元组：

$$S = \{ \{ o_1, p_1, j_1, c_1, d_1 \}, \{ o_2, p_2, j_2, c_2, d_2 \}, \ldots \}$$

五元组的各元素含义为：
- $o$：目标物体
- $p$：物体的部件（如椅面、扶手）
- $j$：人体关节（如左手、臀部）
- $c$：接触类型（contact / not contact / not care）
- $d$：从关节到部件的相对方向向量

这种表示的关键优势在于：**交互类型与接触区域之间存在强相关性**，因此 CoC 能够以统一的方式编码从简单（如伸手触碰）到复杂（如躺下）的各类交互，无需为每个任务单独设计状态空间和奖励函数。

### 3.2 LLM Planner

LLM Planner 接收自然语言指令和场景背景信息（物体部件标注），经推理生成多步 CoC 计划（图3）。该模块利用大语言模型的世界知识来理解指令意图，并将其映射为结构化的接触序列。例如，“坐在椅子上”会被规划为：先走近椅子，然后臀部接触椅面，手部接触扶手等步骤。

### 3.3 Unified Controller

Unified Controller 基于对抗运动先验（AMP）框架，在物理仿真中执行 CoC 计划。其包含以下关键子模块：

**TaskParser**：将 CoC 中的每个接触步骤转化为统一的观测和奖励信号（图4a），管理多步执行的状态切换。当当前步骤的接触条件满足后，自动推进到下一步骤。

**Motion Discriminator**：对抗判别器 $D$ 提供运动风格奖励，确保生成的动作自然、符合人体运动学规律。判别器的训练目标为：

$$\arg\min_D -\mathbb{E}_{d^{\mathcal{M}}(s_t, s_{t+1})}[\log(D(s_t^A, s_{t+1}^A))] - \mathbb{E}_{d^{\pi}(s_t, s_{t+1})}[\log(1 - D(s_t^A, s_{t+1}^A))] + w^{\text{gp}} R^{\text{gp}}$$

策略的风格奖励据此计算：

$$R^S(s_t, s_{t+1}) = -\log(1 - D(s_t^A, s_{t+1}^A))$$

总奖励由任务奖励 $R^G$ 和风格奖励 $R^S$ 加权求和：

$$R(s_t, a_t, s_{t+1}, \mathcal{G}) = w^G R^G(\cdot) + w^S R^S(\cdot)$$

**接触奖励**：针对每个接触对 $k$，根据接触类型分段计算：

$$R_k = \begin{cases} w_{\text{dis}} e^{-w_{dk}\|\mathbf{d}_k\|} + w_{\text{dir}} \max(\bar{\mathbf{d}}_k \cdot \hat{\mathbf{d}}_k, 0), & c_k = \text{contact} \\ 1 - e^{-w_{dk}\|\mathbf{d}_k\|}, & c_k = \text{not contact} \\ 1, & c_k = \text{not care} \end{cases}$$

其中 $\mathbf{d}_k$ 为关节到目标部件的实际距离向量，$\hat{\mathbf{d}}_k$ 为期望方向。当接触类型为 contact 时，奖励鼓励关节接近目标且方向正确；为 not contact 时，惩罚关节接近目标；not care 时给予最大奖励。

**自适应权重**：不同接触对的优化难度差异显著，固定权重会导致简单接触对主导训练。UniHSI 引入启发式自适应权重，根据当前优化进度动态分配：

$$w_k = \frac{1 - R_k}{n - \sum_{i=1}^n R_i + e}$$

其中 $n$ 为当前步骤的接触对数量，$e$ 为防止除零的小常数。该公式使当前奖励较低（难优化）的接触对获得更高权重，迫使策略关注瓶颈接触。消融实验（Table 2）证实：移除自适应权重后，简单任务成功率从 85.5% 骤降至 21.2%，验证了其关键作用。

**自我中心高度图**：为赋予角色场景几何感知能力，UniHSI 构建以角色为中心的周围高度图（图4b），采样周围物体的高度信息用于避障和导航。消融实验表明，移除高度图后困难任务成功率降至 0%，表明环境感知对复杂场景至关重要。

**接触误差**：评估指标定义为所有非“not care”接触对的平均误差：

$$\text{ContactError} = \frac{\sum_{i, c_i \neq 0} er_i}{|\{i : c_i \neq 0\}|}, \quad er_i = \begin{cases} \|\mathbf{d}_k\|, & c_i = \text{contact} \\ \min(0.3 - \|\mathbf{d}_k\|, 0), & c_i = \text{not contact} \end{cases}$$

对于 contact 对，误差为实际距离；对于 not contact 对，误差为距离小于 0.3 米的惩罚值。

![[assets/figures/papers/paper_list_l1780_UniHSI_Unified_Human_Scene_Interaction_via_Prompted_Chain_of_Contacts/figures/005_Figure_4.jpg]]
*Figure 4: Design Visualization. (a) Our framework ensures a unified design across tasks using the unified interface and the TaskParser. (b) The ego-centric height map in a ScanNet scene is depicted by green dots, with darker shades indicating greater height*

## 实验与关键发现

### 核心实验设计

UniHSI在两类场景下进行评估：**ScenePlan数据集**（包含PartNet和ScanNet两个来源，分为简单/中等/困难三个难度级别）和**三个单任务基准**（Sit、Lie Down、Reach）。主要指标为**成功率**（Success Rate）和**接触误差**（Contact Error，定义见式9）。

#### 基线方法

对比方法包括：
- **NSM**（Starke et al., 2019）：基于运动学的交互合成，仅控制少量关节
- **SAMP**（Hassan et al., 2021a）：基于物理的坐下交互，使用运动先验
- **InterPhys**（Hassan et al., 2023）：基于物理的交互，支持接触奖励和多关节控制
- **AMP**（Peng et al., 2021）：对抗运动先验框架
- **PADL**（Juravsky et al., 2022）：基于BERT的语言驱动物理交互

由于部分方法代码未公开且训练数据不同，本文在可能的情况下复现了核心设计，但定量对比存在一定的不公平性。

---

### ScenePlan数据集主结果

**Table 2**展示了ScenePlan数据集上的性能。在PartNet来源的简单任务上，完整UniHSI的成功率达到**85.5%**，接触误差为0.026，平均成功步数为1.07。在ScanNet来源的简单任务上，成功率为**73.2%**，接触误差0.034。ScanNet性能下降主要源于训练数据与真实扫描场景之间的模态差异。

**关键消融发现**（Table 2）：
- **移除自适应权重**（wo Adaptive Weights）：简单任务成功率从85.5%骤降至**21.2%**，接触误差从0.026升至0.155。这验证了自适应权重对统一控制的关键作用——固定权重无法有效平衡多个接触对的优化难度。
- **移除自我中心高度图**（wo Heightmap）：简单任务成功率降至61.6%，困难任务成功率降至**0%**。高度图是智能体在场景中导航和避障的必要感知模块。

---

### 单任务对比与消融

**Table 3**报告了Sit、Lie Down、Reach三个单任务上的定量对比：

| 任务 | 方法 | 成功率(%) | 接触误差 |
|------|------|-----------|----------|
| Sit | InterPhys-Sit | 93.7 | 0.033 |
| Sit | **UniHSI** | **94.3** | **0.032** |
| Lie Down | AMP-Lie Down | 21.3 | 0.112 |
| Lie Down | **UniHSI** | **81.5** | **0.061** |
| Reach | AMP-Reach | 98.1 | 0.015 |
| Reach | **UniHSI** | **97.5** | **0.016** |

UniHSI在Sit任务上与InterPhys持平（+0.6%），在Lie Down任务上大幅领先AMP（+60.2%），在Reach任务上略低于AMP（-0.6%）。Reach任务本身简单，AMP的专用设计已足够；而Lie Down需要全身多关节协调接触，UniHSI的统一表示和多步规划展现出显著优势。

**Vanilla Combination对比**（Table 3）：将多个AMP策略简单组合（Vanilla Combination）在Lie Down任务上仅达**20.1%**，远低于UniHSI的81.5%。**Figure 6(b)**的收敛曲线进一步显示，UniHSI不仅最终性能更优，训练效率也更高。

---

### LLM规划器消融

**Table 4**评估了不同LLM规划器的影响：

| 规划器 | 规划正确率(%) | 执行成功率(%) |
|--------|---------------|----------------|
| 人类 | 100.0 | 91.4 |
| GPT-3.5 | 49.1 | 35.6 |
| **GPT-4** | **71.9** | **57.3** |

GPT-4的规划正确率（71.9%）和执行成功率（57.3%）均显著优于GPT-3.5（49.1%和35.6%），表明更强的LLM能生成更合理的接触链计划。人类规划的上限（91.4%）说明当前LLM规划仍有较大提升空间。

---

### 失败模式分析

**Table 5**展示了LLM规划器的典型失败案例：
- **空间关系错误**：LLM可能生成物理上不可达的接触配置
- **不可执行操作**：如要求“打开笔记本电脑”，但当前系统仅支持静态物体交互
- **语义歧义**：模糊指令导致规划偏离真实意图

在控制器层面，失败主要源于：
- 多接触对同时优化时的奖励冲突
- 复杂场景中的导航失败（无高度图时困难任务成功率为0%）
- 模态差异导致的泛化不足（ScanNet性能低于PartNet）

---

### 运动真实性与用户研究

**Table 6**的用户研究表明，UniHSI在运动自然度和语义保真度上均优于AMP基线。**Figure 6(a)**的定性对比显示，UniHSI生成的坐姿和躺姿动作更自然、接触更准确。然而，运动真实性的定量评估仍缺乏客观统一指标，当前主要依赖主观评价。

---

### 关键图表结论汇总

- **Figure 1**：UniHSI支持统一、长时程、多物体、细粒度交互控制
- **Table 1**：UniHSI在统一界面、语言输入、全身控制等特征上全面超越先前方法
- **Figure 2**：LLM Planner与Unified Controller的两级架构
- **Figure 4(a)**：统一设计vs任务特定设计的架构对比，TaskParser将CoC转化为统一观测和奖励
- **Figure 5**：不同难度级别的交互任务可视化
- **Figure 6**：定性消融和收敛曲线，UniHSI在自然度、准确性和训练效率上均优于基线

![[assets/figures/papers/paper_list_l1780_UniHSI_Unified_Human_Scene_Interaction_via_Prompted_Chain_of_Contacts/figures/009_Figure_6.jpg]]
*Figure 6: Visual Ablations. (a) Our model exhibits superior natural and accurate performance compared to baselines in tasks such as “Sit” and “Lie Down”. (b) Our model demonstrates more efficient and effective training procedures*

![[assets/figures/papers/paper_list_l1780_UniHSI_Unified_Human_Scene_Interaction_via_Prompted_Chain_of_Contacts/figures/002_Table_1.jpg]]
*Table 1: Comparative Analysis of Key Features between UniHSI and Preceding Methods*

![[assets/figures/papers/paper_list_l1780_UniHSI_Unified_Human_Scene_Interaction_via_Prompted_Chain_of_Contacts/figures/007_Figure_5.jpg]]
*Figure 5: Visual Examples Illustrating Tasks of Varying Difficulty Levels*

![[assets/figures/papers/paper_list_l1780_UniHSI_Unified_Human_Scene_Interaction_via_Prompted_Chain_of_Contacts/figures/008_Table_3.jpg]]
*Table 3: Ablation Study on Baseline Models and Vanilla Implementations*

## 定位与知识库关联

### 1. 与先前工作的关系

UniHSI 的核心贡献在于将物理人-场景交互（Physical Human-Scene Interaction, PHSI）从**任务特定工程**推向**统一语言驱动范式**。理解其定位需要沿着两条线索展开：交互表示的统一性，以及控制策略的通用性。

#### 1.1 从运动学交互到物理交互

早期的人-场景交互合成主要依赖运动学方法。**NSM**（Starke et al., 2019）通过神经网络状态机生成交互运动，但仅控制有限关节且缺乏物理合理性。这类方法虽然在视觉上可以产生流畅的运动，但无法处理接触力、物体反作用力等物理约束，导致穿透、滑步等伪影。

物理仿真方法的引入改变了这一局面。**AMP**（Peng et al., 2021）提出对抗运动先验框架，通过判别器约束策略生成的运动与参考运动数据集分布一致，成为后续物理交互工作的基础组件。UniHSI 同样采用 AMP 框架来保证运动风格的自然度，其风格奖励 $R^S$ 通过对抗判别器 $D$ 建模：
$$R^S(s_t, s_{t+1}) = -\log(1 - D(s_t^A, s_{t+1}^A))$$

在此基础上，**SAMP**（Hassan et al., 2021a）将 AMP 扩展到物理坐姿交互，**InterPhys**（Hassan et al., 2023）进一步引入接触奖励和多关节控制。然而，这些方法仍存在根本局限：每个任务需要手工设计特定的奖励函数和目标状态，控制关节范围有限（如仅控制盆骨和手部），且无法处理多步骤、多物体的复杂交互。Table 1 的系统对比清晰展示了这一代际差异——UniHSI 是首个同时支持统一交互表示、语言输入、全身控制（15个关节）和长时程多物体交互的框架。

#### 1.2 从手工奖励到统一接触表示

任务特定设计的根源在于缺乏统一的交互表示。先前方法为“坐”定义臀部与椅面的距离奖励，为“躺”定义背部与床面的接触奖励，这些奖励在语义上互不兼容。UniHSI 的突破性洞察在于：**所有交互都可以分解为有序的关节-物体部件接触对序列**，即接触链（Chain of Contacts, CoC）：
$$\mathcal{C} = \{ S_1, S_2, \ldots \}$$
其中每个接触步骤 $S$ 由多个五元组 $\{o, p, j, c, d\}$ 构成，分别指定物体、部件、关节、接触类型（接触/不接触/不关心）和相对方向。

这一表示的核心优势在于**统一性**：TaskParser 模块将任意 CoC 转化为统一的观测向量和奖励信号，无需为不同任务编写不同的代码路径。Figure 4(a) 对比了这种统一设计与传统任务特定设计的差异：传统方法中，每个任务需要独立的奖励计算模块；而 UniHSI 通过 CoC 接口实现了单一控制器处理多样化任务。

#### 1.3 语言驱动交互的探索

将语言引入物理交互并非全新思路。**PADL**（Juravsky et al., 2022）使用 BERT 编码语言指令来驱动物理角色执行简单动作。但 PADL 仍依赖任务特定的奖励设计，且无法处理多步骤交互。UniHSI 的关键不同在于：LLM 不仅用于理解指令，更用于**生成结构化的交互计划**（CoC），将语言理解与物理执行解耦。这种设计使得 LLM 的世界知识可以被充分利用来规划接触序列，而控制器只需专注于执行这些物理上明确定义的接触目标。

### 2. 适用边界与能力范围

#### 2.1 已验证的能力

根据 Table 2 和 Table 3 的实验证据，UniHSI 在以下场景中表现出可靠性能：

- **简单到中等难度的单物体交互**：在 ScenePlan 数据集（PartNet 场景）上，简单任务成功率达 85.5%，中等任务也保持较高成功率（具体数值见 Table 2）。
- **标准单任务交互**：坐姿（94.3%）、伸手（97.5%）的成功率与专门设计的基线方法（InterPhys-Sit 93.7%, AMP-Reach 98.1%）相当或更优。
- **复杂多步交互**：躺下任务的成功率（81.5%）远超 AMP-Lie Down 基线（21.3%）和 AMP 简单组合（Vanilla Combination, 20.1%），验证了 CoC 多步规划的有效性。
- **真实扫描场景泛化**：在 ScanNet 场景上，简单任务成功率达 73.2%，表明系统具有一定的从合成数据到真实场景的迁移能力。

#### 2.2 已知局限

论文明确指出的局限包括：

1. **LLM 规划器的空间推理错误**：LLM Planner 可能生成空间关系错误或物理上不可执行的接触计划（如“打开笔记本电脑”这类需要理解铰接结构的操作），导致控制器无法完成交互。Table 4 显示即使使用 GPT-4，规划正确率也仅为 71.9%，意味着近 30% 的计划存在缺陷。

2. **静态物体假设**：当前系统假设所有场景物体为静态刚体，不支持与可移动物体（如椅子、门）或被携带物体的交互。这从根本上限制了交互的丰富性——无法实现“搬椅子坐下”或“开门进入”等需要先改变物体状态的交互。

3. **运动真实性评估困难**：缺乏客观统一的运动自然度指标，目前主要依赖用户研究进行主观评价。这不仅是 UniHSI 的问题，也是整个物理角色动画领域的共同挑战。

4. **多智能体交互仅停留在规划层面**：虽然 LLM 可以生成涉及多个角色的交互计划，但物理仿真中的协同执行尚未实现。

### 3. 开放问题与未来方向

基于上述局限和方法设计，以下开放问题值得关注：

1. **LLM 与强化学习的端到端集成**：当前 LLM Planner 和 Unified Controller 是分离的两个阶段——LLM 生成计划，控制器执行计划。如果 LLM 在计划执行失败时无法获得反馈并修正，系统的鲁棒性将受限于 LLM 的一次性规划质量。如何将 LLM 无缝集成到 RL 训练循环中，实现可扩展的端到端学习，是一个重要方向。

2. **动态物体交互的扩展**：要支持“开门”、“搬运椅子”等交互，统一控制器需要处理物体状态变化带来的接触目标动态更新。这可能需要将 CoC 表示从静态接触序列扩展为条件接触序列，其中后续步骤的接触目标依赖于前序步骤中物体的新状态。

3. **减少场景标注依赖**：当前 CoC 规划需要场景的部件级标注（如“椅面”、“扶手”），这在真实场景中获取成本高昂。利用更强大的视觉-语言模型（如 GPT-4V）直接从视觉输入理解场景几何和语义，减少对显式部件标注的依赖，是提升实用性的关键路径。

4. **长时程交互的综合评估指标**：现有指标（成功率、接触误差）主要衡量单步接触的准确性，难以全面反映多步交互的语义一致性和运动自然度。如何定义并客观评价“坐在椅子上然后拿起桌上的杯子”这类长时程交互的综合质量，仍是开放问题。

## 原文 PDF

![[paperPDFs/ICLR_2024/UniHSI_Unified_Human_Scene_Interaction_via_Prompted_Chain_of_Contacts.pdf]]
