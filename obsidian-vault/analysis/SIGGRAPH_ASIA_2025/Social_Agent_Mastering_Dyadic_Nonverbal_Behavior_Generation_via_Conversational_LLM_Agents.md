---
title: "Social Agent: Mastering Dyadic Nonverbal Behavior Generation via Conversational LLM Agents"
type: paper
paper_level: A
venue: "SIGGRAPH Asia"
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2025/Social_Agent_Mastering_Dyadic_Nonverbal_Behavior_Generation_via_Conversational_LLM_Agents.pdf
project_link: null
code_link: null
aliases:
- SAMDNBGCLA
tags:
- SIGGRAPH_ASIA_2025
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "引入基于心理学和语言学知识的LLM代理系统，动态推理场景上下文并生成高层控制信号（交互配置、手势同步、注视），将这些信号转化为对扩散模型的约束，从而实现从高层意图到低层动作的因果控制。"
primary_logic: "将LLM的语义理解和推理能力与经过行为学理论强化的提示词相结合，可以模拟人类在交流中本能的非言语行为规划过程，从而显式地建模多尺度社交信号与其具身表达之间的因果联系。"
claims:
- "全模型在用户研究中的人类相似度和交互水平评分显著优于所有单人生成基线（Photoreal、LDA、EMAGE）。"
- "移除动态控制器代理导致交互水平（Interaction Level）和客观同步指标（FDD, DMSS）显著下降，证明高层规划对生成逼真互动至关重要。"
- "消融实验表明，在提示词中增加逐步推理和参考理论指导，大幅提升了布局合理性和行为适当性的评分。"
- "集成社交代理系统可使原本不支持互动的单人生成器（GestureDiffuCLIP）成功生成双人互动行为，证明了框架的通用性。"
---

# Social Agent: Mastering Dyadic Nonverbal Behavior Generation via Conversational LLM Agents

> [!tip] 核心洞察
> 将LLM的语义理解和推理能力与经过行为学理论强化的提示词相结合，可以模拟人类在交流中本能的非言语行为规划过程，从而显式地建模多尺度社交信号与其具身表达之间的因果联系。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 社交代理：基于对话大语言模型的二元非言语行为生成 |
| 英文题名 | Social Agent: Mastering Dyadic Nonverbal Behavior Generation via Conversational LLM Agents |
| 会议/期刊 | SIGGRAPH Asia 2025 |
| Links | [paper](https://arxiv.org/abs/2510.04637) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | Social Agent |
| Dataset | Photoreal |

> [!tip] 效果简介
> - Photoreal 上，人类相似度 / 交互水平 / 节拍匹配 用户评分 为 0.26 / 0.37 / 0.04，对比 LDA: -0.20 / -0.16 / -0.08; EMAGE: -0.25 / -0.15 / -0.04; Photoreal: 0.10 / -0.07 / 0.03，变化 全面显著优于单人生成基线，尤其是交互水平大幅领先。
> - Photoreal 上，运动多样性 (Div) 为 1.98，对比 Ground Truth: 2.13; LDA: 1.41，变化 接近真实分布，显著优于LDA。

## 概要

**问题瓶颈**：数据驱动的单人或双人生成方法难以捕捉稀疏但关键的高层社交信号——如眼神交流、手势同步、社交距离——导致生成的非言语行为缺乏上下文感知和真实的互动性。

**核心洞见**：将大语言模型（LLM）的语义理解与推理能力，同行为学理论强化的提示词相结合，可以模拟人类在交流中本能的非言语行为规划过程，从而显式地建模多尺度社交信号与其具身表达之间的因果联系。

**方法定位**：本文提出 **Social Agent**，一个由 LLM 驱动的代理系统，通过场景设计师代理（Scene Designer Agent）和动态控制器代理（Dynamic Controller Agent）动态推理对话上下文，生成高层控制信号（交互配置、手势同步、注视），并将这些信号通过无训练的交互引导策略注入自回归扩散模型，实现从高层意图到低层动作的因果控制。

**主要结果**：在 Photoreal 数据集上的用户研究表明，Social Agent 在人类相似度（0.26 vs. 最优基线 Photoreal 0.10）和交互水平（0.37 vs. Photoreal -0.07）上全面显著优于所有单人生成基线（LDA、EMAGE、Photoreal）。移除动态控制器代理后，交互水平和客观同步指标（FDD、DMSS）显著下降，证实高层规划对逼真互动的关键作用。此外，该框架可泛化至原本不支持互动的单人生成器（如 GestureDiffuCLIP），使其成功生成双人互动行为。

非言语行为——手势、身体姿势、眼神注视和空间距离——是人类面对面交流的核心组成部分，承载着情感表达、话轮转换和社交意图传递等关键功能。在虚拟人、具身智能体和沉浸式交互系统中，生成逼真、上下文感知的非言语行为对于提升用户体验至关重要。

现有方法主要沿两条路径展开。**单人生成方法**，如 **LDA**（Alexanderson et al., SIGGRAPH 2023）、**EMAGE**（Liu et al., 2023）和 **Photoreal**（Ng et al., 2024），直接从语音特征端到端地生成个体手势，缺乏对互动对象的感知。**双人生成方法**则通常将两个单人模型独立运行，或依赖成对数据进行训练，本质上忽略了交互双方之间的动态耦合。这两种范式共同面临一个根本性瓶颈：**数据驱动的生成模型难以捕捉稀疏但关键的高层社交信号**——例如眼神交流的时机、手势的镜像同步、社交距离的调整——这些信号在数据中分布稀疏，却对感知交互的自然度至关重要。

从因果视角审视，现有方法缺失了一个关键的因果环节：从场景上下文和对话意图到具身行为表达之间的**高层规划与控制**。人类在交流中本能地进行着多尺度的非言语规划——判断与对方的距离、决定何时注视对方、选择是否模仿对方的手势——这些决策并非直接从语音声学特征中涌现，而是源于对社交情境的理解。现有方法跳过了这一规划过程，直接从低层特征映射到动作，导致生成的行为缺乏上下文感知和互动性。

本文的核心动机在于：**将大语言模型（LLM）的语义理解和推理能力引入非言语行为生成，模拟人类在交流中的行为规划过程**。通过构建基于心理学和语言学知识的LLM代理系统，动态推理场景上下文并生成高层控制信号（交互配置、手势同步、注视），将这些信号转化为对扩散模型的约束，从而实现从高层意图到低层动作的因果控制。这一思路的核心洞察是：LLM的语义推理能力，与经过行为学理论强化的提示词相结合，可以显式地建模多尺度社交信号与其具身表达之间的因果联系，填补现有方法在高层规划层面的空白。

## 核心方法与创新机理

Social Agent 的核心创新在于将大语言模型（LLM）的语义推理能力引入二元非言语行为生成，构建了一个从高层社交意图到低层动作的因果控制闭环。与现有数据驱动方法直接由语音特征端到端生成动作不同，本工作通过三个关键的 changed slots 实现了范式跃迁。

### 从端到端生成到分层规划与控制

现有单人生成方法（如 **LDA**（Alexanderson et al., SIGGRAPH 2023）、**EMAGE**（Liu et al., 2023）、**Photoreal**（Ng et al., 2024））缺乏显式的高层行为规划，动作生成完全依赖语音特征的统计关联。这种数据驱动范式难以捕捉稀疏但关键的社交信号——如眼神交流的时机、手势同步的启动、以及社交距离的动态调整——因为这些信号在训练数据中往往被噪声淹没。

Social Agent 的核心洞见在于：人类在交流中本能地进行非言语行为规划，这一过程可以通过 LLM 的语义理解与推理能力来模拟。系统引入了一个基于 LLM 的代理系统（Social Agent），包含两个关键模块：

- **Scene Designer Agent**（场景设计师代理）：在对话开始时分析对话内容，确定初始空间布置（位置配置、距离、姿势），输出定性空间关系并转换为数值参数（Section 3.2.1）。
- **Dynamic Controller Agent**（动态控制器代理）：在每轮生成前分析当前状态，通过空间关系预测器、手势同步预测器和注视预测器输出交互调整信号（Section 3.2.2）。

这种分层设计将行为规划从动作生成中解耦出来，使得高层社交意图可以显式地建模并转化为对扩散模型的约束。

### 从单人生成到双人协同生成

现有方法要么仅生成单人动作，要么将两个单人模型独立运行而完全忽略交互（changed slot: 运动生成架构）。Social Agent 的自回归扩散模型直接在完整身体空间上同时生成两人动作，并通过两种无训练的交互引导策略将控制信号注入生成过程：

- **相似性约束**（Similarity Constraint）：在早期去噪步骤中替换目标动作，实现手势模仿等同步行为。
- **轨迹约束**（Trajectory Constraint）：通过梯度引导更新预测的干净动作，实现空间位置的精确控制。

关键优势在于：训练时控制信号与生成模型完全解耦，控制信号通过分类器引导直接注入，无需重新训练（changed slot: 交互控制集成）。这使得框架具有通用性——实验表明，将 Social Agent 系统集成到原本不支持互动的单人生成器 **GestureDiffuCLIP**（Ao et al., 2023）后，该生成器可成功生成双人互动行为（Figure 12）。

### 因果机制与证据强度

消融实验提供了因果链的关键证据：

1. **移除 Dynamic Controller Agent** 导致交互水平（Interaction Level）和客观同步指标（FDD, DMSS）显著下降（Table 1, Table 2），证明高层规划对生成逼真互动至关重要。
2. **提示词消融**（Figure 9）表明，在提示词中增加逐步推理和参考理论指导（基于心理学和语言学知识），大幅提升了布局合理性和行为适当性的评分，验证了行为学理论注入的有效性。
3. **控制范围参数消融**（Section 4.4.3）揭示了控制强度与运动质量之间的权衡：过小的控制范围导致引导不足，过大的控制范围则引入抖动和不稳定性。

全模型在用户研究中的人类相似度（0.26）和交互水平（0.37）显著优于所有单人生成基线（Photoreal 分别为 0.10 和 -0.07）（Table 1），运动多样性（Div=1.98）接近真实分布（Ground Truth=2.13），显著优于 LDA（1.41），表明分层规划与控制策略在保持运动自然度的同时有效注入了交互感知能力。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2510_04637/figures/002_Figure_2.jpg]]
*Figure 2: Our framework models dyadic interactions by integrating an autoregressive diffusion model for low-level motion generation with an LLM-based agentic system, Social Agent, for nonverbal behavior analysis. This system continuously analyzes and refines nonverbal behavior cues, dynamically guiding the diffusion model to generate natural interpersonal behaviors such as spatial positioning, gaze contact, and gesture synchrony*

Social Agent 的整体 pipeline 由三个解耦的核心组件构成：**双人运动生成模型**、**基于 LLM 的社交代理系统**以及**无训练的运动控制机制**。三者形成闭环反馈：LLM 代理系统在高层分析对话语境并输出交互控制信号，这些信号通过控制机制注入扩散模型，约束低层动作生成；同时，代理系统周期性地检查生成的运动状态，推断意图，实现动态、响应式的交互行为生成。

### 输入输出流与模块关系

系统的输入为双人对话的语音信号（两人各自的音频流），输出为两人的全身三维动作序列。整体流程分为两个阶段：

1. **初始场景规划阶段**：在生成开始前，**场景设计师代理**（Scene Designer Agent）分析对话文本内容，确定两人的初始空间布局——包括姿态状态（站立/行走/坐下）、全局位置、朝向和社交距离。该代理将定性空间关系（如“面对面，距离较近”）转换为数值参数，为后续生成提供空间约束。

2. **逐轮生成与控制阶段**：生成过程采用滑动窗口机制，将双人交互建模为多轮单人运动生成任务。每一轮开始前，**动态控制器代理**（Dynamic Controller Agent）被激活，分析当前语音内容、历史动作状态以及**视觉运动描述器**（Visual Motion Descriptor）提供的多模态上下文，通过三个预测模块——空间关系预测器、手势同步预测器、注视预测器——输出本轮所需的交互调整信号。这些自然语言描述经**控制信号解析器**（Control Signal Parser）转换为结构化数字控制信号（相似性约束和关节轨迹约束），再通过**交互引导模块**（Interaction Guidance Module）注入自回归扩散模型，指导两人动作的协调生成。

### 核心设计思想

该框架的关键创新在于将 LLM 的语义理解与推理能力系统性地引入运动生成 pipeline。与传统的端到端方法直接从语音特征映射到动作不同，Social Agent 显式地建模了从高层社交意图（眼神交流、手势同步、空间关系）到低层动作表达的因果链路。LLM 代理系统扮演了“社交规划器”的角色，其提示词设计中融入了行为学理论参考、逐步推理引导和空间映射规则，使得代理能够模拟人类在交流中本能的非言语行为规划过程。

同时，控制信号与生成模型的解耦设计（训练时完全分离，推理时通过分类器引导注入）使得该框架具备通用性——即使是原本不支持互动的单人生成器（如 GestureDiffuCLIP, Ao et al., 2023），在集成 Social Agent 系统后也能成功生成双人互动行为（见 Figure 12），验证了代理系统作为独立规划层的可迁移性。

### 3.1 双人运动生成模型

系统底层采用一个基于自回归扩散模型的双人协同手势生成器。该模型直接在完整身体运动空间（full-body motion space）上训练，而非分两阶段在隐空间操作，从而避免信息损失。每帧运动编码为向量 $m_t \in \mathbb{R}^{(J \times Q + G)}$，其中 $J$ 为关节数，$Q$ 为关节特征维度，$G$ 为全局根节点特征维度。

生成过程通过滑动窗口机制将双人交互建模为多轮单代理运动生成任务。在第 $i$ 轮，角色 I 的运动生成条件概率为：

$$p ( M _ { i } ^ { \mathrm { I } } | M _ { i - 1 } ^ { \mathrm { I } } , S _ { i } ^ { \mathrm { I } } , S _ { i } ^ { \mathrm { I I } } )$$

其中 $M_{i-1}^{\mathrm{I}}$ 为角色 I 上一轮的运动历史，$S_i^{\mathrm{I}}$ 和 $S_i^{\mathrm{II}}$ 分别为两角色当前轮的语音信号。该公式表明，生成某一角色的动作时，模型同时接收双方语音作为条件输入，这是实现协同互动的基础。

扩散过程的正向加噪定义为：

$$p ( x _ { t } | x _ { 0 } ) \sim \mathcal{N} ( x _ { t } ; \sqrt { \bar { \alpha } _ { t } } x _ { 0 } , ( 1 - \bar { \alpha } _ { t } ) I )$$

其中 $x_0 = M_i^{\mathrm{I}}$ 为干净运动，$\bar{\alpha}_t$ 为累积噪声调度参数。去噪器 $\mathcal{D}_\theta$ 的训练目标为预测所加噪声 $\epsilon$：

$$\mathcal { L } = \mathbb{E} _ { { x } _ { 0 } = M _ { i } ^ { \mathrm { I } } , \epsilon \sim \mathcal { N } ( 0 , 1 ) , t \in [ 0 , T ] } \| \epsilon - \mathcal { D } _ { \theta } ( { x } _ { t } , t , c ) \|$$

推理阶段采用无分类器引导（classifier-free guidance），将语音条件 $c$ 拆分为条件预测与无条件预测的加权组合：

$$\mathcal { D } _ { \theta } ( x _ { t } , t , c ) = \lambda \mathcal { D } _ { \theta } \left( x _ { t } , t , s ; M _ { i - 1 } ^ { \mathrm { I } } , S _ { i } ^ { \mathrm { I } } , S _ { i } ^ { \mathrm { I I } } \right) + (1-\lambda)\mathcal{D}_\theta(x_t, t, \varnothing)$$

引导尺度因子 $\lambda = 2$，扩散步数 $T = 1000$，推理时采用 200 步 DDIM 加速。

### 3.2 LLM社交代理系统

该系统包含两个核心模块，构成从高层语义规划到低层运动约束的因果控制链路。

**场景设计师代理（Scene Designer Agent）** 在对话开始前运行，分析对话文本以确定初始空间布局。其空间关系规划器输出角色姿态状态 $s \in \{\text{stand}, \text{walk}, \text{sit}\}$、全局位置和朝向，这些定性空间关系随后被转化为数值参数。

**动态控制器代理（Dynamic Controller Agent）** 在每轮生成前被激活，分析当前对话与运动状态，输出三类交互调整信号：
- **空间关系预测器**：根据文本上下文进行细粒度空间推理，调整两角色的相对位置；
- **手势同步预测器**：判断是否触发手势模仿行为；
- **注视预测器**：确定目光交流的时机与目标词。

视觉运动描述器（Visual Motion Descriptor）利用视觉-语言模块对当前动作状态进行描述，为动态控制器提供多模态上下文。决策整合器将三个预测模块的建议聚合为统一的调整方案。

### 3.3 无训练交互引导模块

控制信号解析器将 LLM 代理的自然语言输出转换为两类数字控制信号，通过无训练方式直接注入扩散生成过程。

**相似性约束**：在去噪早期步骤（截断步 $\tilde{t} = 200$）中，直接将目标运动 $\tilde{x}$ 替换当前预测：

$$x _ { t < \tilde { t } } ^ { 0 } = \tilde { x }$$

**轨迹约束**：通过梯度引导实现关节级精确控制。定义损失函数衡量预测关节参数 $J(x_t^0)$ 与目标轨迹 $\tilde{J}$ 的加权差异：

$$\mathcal { L } ( x _ { t } ^ { 0 } ) = \| W \odot ( J ( x _ { t } ^ { 0 } ) - \tilde{J} ) \|$$

其中 $W$ 为关节权重矩阵。梯度引导更新公式为：

$$\tilde { x } _ { t } ^ { 0 } = x _ { t } ^ { 0 } - \alpha \nabla _ { x _ { t } ^ { 0 } } \mathcal { L } ( x _ { t } ^ { 0 } )$$

$\alpha$ 为引导强度。控制范围参数决定引导作用的去噪步数比例——消融实验表明，控制范围过小会导致引导不足，过大则引入运动抖动和伪影。

### 关键设计决策

整个框架的核心因果机制在于：LLM 代理系统将稀疏的高层社交信号（眼神交流、手势同步、社交距离）显式建模为可解析的控制约束，并通过训练时完全解耦的引导策略将这些约束注入扩散模型。这使得系统能够在不重新训练底层生成器的情况下，将原本仅支持单人生成的模型（如 GestureDiffuCLIP）改造为具备双人互动能力的系统，验证了框架的通用性。

## 实验与关键发现

### 主实验结果

#### 用户研究

为评估生成行为的真实感与交互性，作者在Photoreal数据集上进行了用户偏好研究，将Social Agent与三类单人生成基线进行对比：**LDA** (Alexanderson et al., SIGGRAPH 2023)、**EMAGE** (Liu et al., 2023) 和 **Photoreal** (Ng et al., 2024)。评估维度包括人类相似度（Human Likeness）、交互水平（Interaction Level）和节拍匹配（Beat Matching）。

如表1所示，Social Agent在人类相似度和交互水平上均显著优于所有基线。人类相似度得分达0.26，远高于Photoreal的0.10，而LDA和EMAGE分别为-0.20和-0.25。交互水平的优势更为突出：Social Agent获得0.37，而Photoreal仅为-0.07，LDA和EMAGE分别为-0.16和-0.15。这表明端到端的单人生成方法完全无法捕捉对话中的互动信号。节拍匹配方面，各方法差异较小（Social Agent 0.04 vs Photoreal 0.03），说明语音-动作同步并非本方法的瓶颈所在。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2510_04637/figures/008_Table_1.jpg]]
*Table 1: Average scores of user study with 95% confidence intervals. Ours (w/o DCA) excludes the Dynamic Controller Agent for the pre-trained generator. Asterisks indicate the significant effects*

移除动态控制器代理（w/o DCA）后，交互水平大幅下降，进一步证实高层规划对逼真互动的关键作用（详见消融部分）。

#### 客观指标评估

在Photoreal和InterAct两个数据集上的客观指标评估（表2）进一步验证了上述结论。Social Agent在节拍对齐（BeatAlign）和动态运动相似性（DMSS）上均取得最优结果：Photoreal数据集上BeatAlign为0.827，DMSS为0.457；InterAct数据集上BeatAlign为0.802，DMSS为0.439。DMSS指标衡量双人动作的同步程度，Social Agent的领先优势表明其生成的互动行为在时间维度上更接近真实人际交流模式。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2510_04637/figures/010_Table_2.jpg]]
*Table 2: Quantitative evaluation on the Photoreal and InterAct datasets. All methods are trained on the same training data, and evaluated on the test audio. Note that FDD cannot be computed on the Photoreal dataset, as it lacks ground-truth paired two-person motion sequences*

运动多样性方面（表4），Social Agent的Div得分为1.98，接近真实数据的2.13，显著优于LDA的1.41，说明引入高层规划并未牺牲生成动作的丰富性。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2510_04637/figures/015_Table_4.jpg]]
*Table 4: Quantitative comparison of diversity scores (Div?? ) on the Photoreal dataset. All systems are trained on the same dataset and evaluated using the same test audio inputs*

### 消融实验

#### 动态控制器代理（DCA）消融

移除动态控制器代理（w/o DCA）是最关键的消融。如表1所示，w/o DCA的交互水平得分显著下降。表2中，FDD和DMSS指标同样出现明显退化。图10的定性对比显示，缺乏DCA的模型在生成过程中丢失了高层引导，导致角色间缺乏互动意识——例如，当一方说话时，另一方不会做出注视或手势响应。

对DCA内部模块的细粒度消融（表3）表明，空间关系预测器、手势同步预测器和注视预测器各自对最终交互质量均有贡献，移除任一模块都会导致用户评分下降。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2510_04637/figures/013_Table_3.jpg]]
*Table 3: Average scores of user study on the fine-grained ablation of DCA, with 95% confidence intervals*

#### 提示词设计消融

图9展示了提示词设计的消融结果。基线提示词仅包含映射规则和任务定义，逐步推理引导（+ Stepwise Reasoning Guides）的加入显著提升了布局合理性（Layout Plausibility）和行为适当性（Behavior Appropriateness）的评分。在此基础上进一步引入参考行为学理论（+ Reference Theories）后，评分再次获得明显提升。这验证了将心理学和语言学知识注入LLM提示词是提升高层规划质量的有效手段。

#### 交互引导控制范围消融

交互引导策略中的控制范围参数决定了梯度引导施加的去噪步数比例。实验测试了100%、80%和50%三种设置。结果表明，控制范围过小（50%）会导致引导不足，交互约束无法有效注入生成过程；控制范围过大（100%）则引入不稳定性和抖动，损害运动质量。最终模型采用80%作为平衡点。

### 框架通用性验证

为验证Social Agent框架的通用性，作者将其集成到原本不支持互动的单人生成器**GestureDiffuCLIP** (Ao et al., 2023)中。如图12所示，集成前的GestureDiffuCLIP只能独立生成单人动作，缺乏互动；集成Social Agent后，该生成器成功输出了具有明显互动特征的双人行为。这一结果证明，LLM代理系统提供的高层规划与训练解耦的交互引导策略，可以作为通用组件赋能不同的底层运动生成模型。

### 方法谱系与知识库定位

Social Agent在方法谱系中占据独特位置。传统协同语音手势生成方法（如LDA、EMAGE、Photoreal）依赖数据驱动的端到端映射，缺乏对高层社交信号的显式建模。Social Agent的核心贡献在于引入基于LLM的代理系统作为规划层，将心理学理论编码为提示词，动态推理场景上下文并生成交互约束，再通过无训练的引导策略注入扩散模型。这一设计实现了高层语义到低层动作的因果控制链路，且与底层生成器完全解耦。

关键创新点包括：(1) 场景设计师代理在对话开始前确定空间布局；(2) 动态控制器代理在每轮生成前输出注视、手势同步和空间关系调整信号；(3) 通过早期去噪替换和梯度引导施加约束，无需重新训练生成器。这种架构为其他需要高层规划的运动生成任务提供了可复用的范式。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2510_04637/figures/006_Figure_6.jpg]]
*Figure 6: This example illustrates how the Spatial Relation Predictor conducts fine-grained spatial reasoning based solely on textual input. Red text in the input highlights the current spatial state of both characters. The 3D image on the right visualizes the input configuration but is not part of the model’s input. In the output, blue text emphasizes the model’s spatial reasoning process, such as the inferred direction and distance of Character I’s movement. This is a concise version of the agent’s output, preserving essential information*

## 定位与知识库关联

### 问题定位与核心瓶颈

现有的协同语音手势生成方法主要面向单人场景，数据驱动范式直接从语音特征端到端地回归动作序列。这类方法——包括 **LDA**（Alexanderson et al., SIGGRAPH 2023）、**EMAGE**（Liu et al., 2023）和 **Photoreal**（Ng et al., 2024）——在单人节拍匹配和动作自然度上取得了进展，但当场景扩展到二元交互（dyadic interaction）时暴露出根本性缺陷：它们无法捕捉稀疏但关键的高层社交信号，如眼神交流、手势同步和社交距离调节。即便将两个单人模型独立运行后拼接，也无法产生上下文感知的互动行为，因为模型缺乏对“谁在看谁”“何时模仿手势”“空间关系是否合适”等高层意图的显式建模能力。

这一瓶颈的深层原因在于，二元非言语行为的生成本质上是一个从高层社交意图到低层具身动作的因果映射问题，而纯数据驱动的端到端方案将这两个层级混为一谈，导致生成结果在交互水平（Interaction Level）上严重不足——用户研究中单人生成基线的交互水平评分均为负值（LDA: -0.16, EMAGE: -0.15, Photoreal: -0.07），表明评估者普遍认为这些方法生成的互动不自然甚至不存在。

### 方法谱系中的位置

**Social Agent** 在方法谱系中占据了一个独特的位置：它将大语言模型（LLM）的语义推理能力引入运动生成管线，在高层规划与低层生成之间建立了显式的因果接口。这一设计思路与现有工作形成以下对比：

| 方法类别 | 代表工作 | 高层规划 | 交互建模 | 控制注入方式 |
|---------|---------|---------|---------|------------|
| 单人生成 | LDA, EMAGE, Photoreal | 无 | 无 | 端到端回归 |
| 风格化单人生成 | **GestureDiffuCLIP**（Ao et al., 2023） | 文本风格描述 | 无 | CLIP嵌入引导 |
| 双人LLM规划 + 扩散生成 | **Social Agent**（本文） | LLM代理系统 | 显式多尺度 | 分类器引导 + 早期替换 |

**GestureDiffuCLIP** 是本文在通用性验证中的重要参照点。该方法原本仅支持单人的风格化手势生成，缺乏二元交互能力。Social Agent 通过将自身的代理系统集成到 GestureDiffuCLIP 之上（Figure 12），成功使其生成双人互动行为，证明了框架的生成器无关性。这一结果意味着 Social Agent 的高层规划模块可以被视为一个“交互增强层”，理论上可叠加于任何单人扩散生成器之上。

### 关键设计决策与因果机制

Social Agent 的核心创新在于将交互控制分解为三个可独立运作的层级，每一层对应一个因果调节旋钮：

1. **场景设计师代理（Scene Designer Agent）**：在对话开始前分析对话内容，基于 Kendon 的 F-formation 系统等行为学理论，确定初始空间布置——包括位置配置（面对面/并排/L型）、社交距离和姿态状态（站/坐/走）。这一模块解决了“对话双方应该如何站位”的高层规划问题。

2. **动态控制器代理（Dynamic Controller Agent）**：在每轮生成前分析当前状态，通过三个预测器——空间关系预测器、手势同步预测器和注视预测器——输出交互调整信号。这些信号以自然语言形式描述（例如“角色I应在词X处注视角色II”），随后由控制信号解析器转化为数字约束。这一模块解决了“何时互动、互动什么”的中层时序规划问题。

3. **交互引导模块（Interaction Guidance Module）**：将高层控制信号通过无训练的引导策略注入扩散生成过程——相似性约束通过早期去噪步骤中的目标替换实现（$x_{t < \tilde{t}}^{0} = \tilde{x}$），轨迹约束通过梯度引导更新实现（$\tilde{x}_t^0 = x_t^0 - \alpha \nabla_{x_t^0} \mathcal{L}(x_t^0)$）。这一模块解决了“如何让动作服从规划”的低层执行问题。

这种三层解耦设计的因果逻辑链为：**对话语义 → LLM推理 → 高层控制信号 → 扩散模型约束 → 协调的双人动作**。消融实验提供了该因果链的关键证据：移除动态控制器代理后，交互水平用户评分和客观同步指标（FDD, DMSS）均显著下降（Table 1, Table 2），证明高层规划并非可有可无的附加组件，而是生成逼真互动的必要条件。

### 适用边界与局限

尽管 Social Agent 在二元非言语行为生成上取得了显著进展，其适用边界和局限值得注意：

**已知适用条件**：
- 对话场景为二元交互，且双方均有语音输入作为生成条件
- 动作状态限定为 {站, 走, 坐} 三种离散姿态
- 控制信号以相似性约束和关节轨迹约束两种形式注入，需要生成器支持分类器引导或早期替换机制

**已知局限**（原文明确指出的开放问题）：
- 训练数据稀缺导致某些行为（如点头）可能出现不自然的重复模式
- 存在足部滑动等运动伪影，需要额外的后处理或物理约束
- 当前行为集合尚未覆盖身体接触等更复杂的非言语行为
- 注视生成目前仅处理方向性注视，尚未实现整体的眼球运动生成

**需要人工验证的边界**：
- 控制范围参数（control scope）的最优值（文中测试了100%、80%、50%）可能依赖于具体场景和生成器架构，其泛化规律尚不明确
- 框架在超过两人的多人群组对话场景中的适用性未经验证
- LLM代理的推理延迟对实时交互应用的影响未量化讨论

### 开放问题与后续方向

从方法谱系的视角看，Social Agent 打开了若干值得探索的方向：

1. **代理系统的行为理论扩展**：当前提示词中嵌入了 Kendon 的 F-formation 等空间关系理论，但非言语行为的理论谱系远不止于此——Argyle 的亲密平衡模型、Ekman 的面部表情编码系统等均可作为代理推理的知识来源，以支持更丰富的行为生成。

2. **生成器与控制器的联合优化**：当前框架中生成器训练与控制信号注入完全解耦，虽然保证了通用性，但可能限制了控制精度。如何在保持模块化优势的同时，引入轻量的端到端微调，是一个值得探索的折中方案。

3. **多模态上下文的深度融合**：当前视觉运动描述器（Visual Motion Descriptor）为动态控制器提供当前动作的文本描述，但这一模态转换可能丢失细粒度信息。直接将视觉特征作为LLM的多模态输入，可能提升控制信号的精确度。

4. **评估体系的完善**：当前用户研究主要评估人类相似度、交互水平和节拍匹配三个维度，但二元交互的质量还涉及社交适当性、文化规范符合度等更细致的维度，需要建立更全面的评估基准。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2025/Social_Agent_Mastering_Dyadic_Nonverbal_Behavior_Generation_via_Conversational_LLM_Agents.pdf]]
