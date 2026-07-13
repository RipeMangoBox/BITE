---
title: "Learning to Assist: Physics-Grounded Human-Human Control via Multi-Agent Reinforcement Learning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Learning_to_Assist_Physics_Grounded_Human_Human_Control_via_Multi_Agent_Reinforcement_Learning.pdf
project_link: https://yutoshibata07.github.io/AssistMimic/
code_link: null
aliases:
- LAPGHHCMARL
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 采用多智能体强化学习（MARL）联合训练支持者和接受者策略，允许双方根据物理反馈双向适应；同时通过三个关键机制使学习稳定有效：从单人运动先验初始化策略，动态地将支持者手部参考目标重映射到接受者当前身体锚点，并在近距离接触时用接触促进奖励替代标准的关节跟踪奖励。
primary_logic: 从单人运动跟踪控制器继承的权重提供了基础运动技能，使得策略不必从零学习基本动力学；动态参考重映射确保手部目标始终与接受者的实时姿态对齐，避免因固定全局参考导致的空间错位；接触促进奖励鼓励功能性的力交互而非死板地跟踪嘈杂的手部轨迹，三者协同使紧密接触辅助行为的物理仿真模仿首次成为可能。
claims:
- MARL联合训练显著优于顺序训练（冻结接受者），在Inter-X数据集上的成功率提升12.5个百分点（74.9% vs 62.4%），验证了接受者需要主动学习如何接受支持而非被动重放。
- 移除策略权重初始化导致训练完全失败（Inter-X成功率0%），或出现奖励黑客行为（HHI-Assist成功率19.1%但产生非功能性动作），表明运动先验对于收敛不可或缺。
- 动态参考重映射对HHI-Assist数据集上的物理接触维持至关重要；消融后，在质量增加1.5倍的无扰条件下，成功率从67.8%骤降至49.1%。
- 接触促进奖励显著增强了策略对未见动态的鲁棒性；消融后，在最大髋扭矩减半的条件下，成功率从73.2%降至27.7%。
---

# Learning to Assist: Physics-Grounded Human-Human Control via Multi-Agent Reinforcement Learning

> [!tip] 核心洞察
> 从单人运动跟踪控制器继承的权重提供了基础运动技能，使得策略不必从零学习基本动力学；动态参考重映射确保手部目标始终与接受者的实时姿态对齐，避免因固定全局参考导致的空间错位；接触促进奖励鼓励功能性的力交互而非死板地跟踪嘈杂的手部轨迹，三者协同使紧密接触辅助行为的物理仿真模仿首次成为可能。

| 字段 | 内容 |
|------|------|
| 中文题名 | 学习辅助：基于物理约束的人-人控制的多智能体强化学习方法 |
| 英文题名 | Learning to Assist: Physics-Grounded Human-Human Control via Multi-Agent Reinforcement Learning |
| 会议/期刊 | CVPR 2026 |
| Links | [Project](https://yutoshibata07.github.io/AssistMimic/) · [paper](https://arxiv.org/abs/2603.11346) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | AssistMimic |
| Dataset | Inter-X, HHI-Assist |

> [!tip] 效果简介
> - Inter-X (specialist seen dynamics) 上，Success Rate (SR, ↑) 74.9% vs 62.4% (Sequential Training) (+12.5%)。
> - Inter-X (specialist unseen dynamics Mass ×1.2) 上，Success Rate (SR, ↑) 57.9% vs 49.9% (Sequential Training) (+8.0%)。
> - Inter-X (generalist with DAgger) 上，Success Rate (SR, ↑) 94.7% vs 77.3% (AssistMimic w/o DAgger) (+17.4%)。

## 概要

### 问题背景与瓶颈

物理仿真中的人类运动模仿长期聚焦于单人场景或无接触的社会交互。然而，**紧密辅助行为**——例如搀扶、支撑、协助站立——需要持续的双向力交换与实时适应，现有方法在此类任务上几乎完全失效。核心瓶颈在于三个方面：

1. **物理一致性断裂**：单独训练支持者（Supporter）或直接运动学重放接受者（Recipient）轨迹，破坏了力交互的闭环。固定运动学重放无法响应物理反馈，导致穿透、滑脱等非物理行为（Figure 4）。
2. **动作捕捉数据不可靠**：近距离交互造成严重遮挡和噪声，手部接触参考轨迹高度不准确，直接跟踪这些噪声会误导强化学习训练。
3. **训练不稳定**：接触密集的场景下，标准的关节跟踪奖励无法区分功能性接触与偶然靠近，策略难以收敛。

### 核心方法：AssistMimic

AssistMimic 首次将紧密接触的人-人辅助运动模仿建模为**多智能体强化学习（MARL）问题**，联合训练支持者和接受者策略，使双方能够根据物理反馈双向适应。其关键创新包含三个协同机制：

- **从单人运动先验初始化策略权重**：两个智能体的策略网络均继承预训练的单人跟踪控制器（PHC）权重，新增的交互感知特征维度以零填充。这使得策略从一开始就具备基本运动技能，无需从零学习动力学，避免了训练崩溃。
- **动态参考重映射**：当双方根关节距离低于阈值时，支持者的手部跟踪目标不再使用固定的全局坐标，而是实时映射到接受者当前姿态下最近的关节位置，确保手部目标始终与接受者的身体对齐。
- **接触促进奖励**：在近距离接触时，用包含接触力感知项和距离惩罚的奖励函数替代标准的手部轨迹跟踪奖励，鼓励产生功能性的力交互，而非死板地跟踪噪声参考。

三者协同使策略既能利用运动先验快速启动学习，又能通过动态重映射维持有效的空间关系，并通过接触促进奖励学习有意义的力支持。

### 主要结果

在两个基准数据集上，AssistMimic 取得了显著提升：

- **Inter-X 数据集**（专家策略）：成功率 **74.9%**，较顺序训练基线（62.4%）提升 **12.5 个百分点**；在未见动力学条件下（质量×1.2），成功率仍保持 **57.9%**（Table 2）。
- **HHI-Assist 数据集**（专家策略）：成功率达 **85.8%**（Table 3）。
- **通用策略**（经 DAgger 蒸馏）：Inter-X 成功率进一步提升至 **94.7%**（Table 4）。

消融实验验证了每个机制的不可或缺性：移除权重初始化导致训练完全崩溃（Inter-X 成功率 0%）；移除动态参考重映射在质量增加 1.5 倍时成功率从 67.8% 骤降至 49.1%；移除接触促进奖励在髋扭矩减半条件下成功率从 73.2% 降至 27.7%。

### 方法定位与局限

AssistMimic 构建在 PHC 单人跟踪框架之上，属于**基于物理仿真的多智能体运动模仿**方法。其当前局限包括：手部模型灵巧度有限（胶囊手），难以执行抓取等精细操作；依赖动作捕捉参考轨迹，对分布外交互的鲁棒性有限；尚未在真实人形机器人上验证迁移效果。

物理仿真中的人类运动模仿（physics-based human motion imitation）近年来取得了显著进展，但现有工作主要聚焦于单人运动或无接触的社会交互。当场景转向需要持续力交换和双向适应的紧密辅助行为（如扶持行走、辅助起身）时，传统方法面临根本性瓶颈。

**核心难点在于“物理一致性”与“参考可靠性”之间的冲突。** 动作捕捉（MoCap）数据在近距离接触时存在严重遮挡和噪声，导致手部接触参考轨迹不可靠；而若将接受者（recipient）的运动作为固定运动学重放，支持者（supporter）则无法获得真实的物理反馈，容易出现姿态穿透、支撑失效等问题。图2直观地展示了这一差距：接触丰富的辅助行为（底部曲线）的学习难度远高于无接触社交交互（顶部曲线）或孤立运动（灰色曲线），传统方法几乎无法收敛。

具体而言，现有范式存在三个结构性缺口：

1. **训练范式割裂。** 现有方法或独立训练支持者策略（如基于**PHC**的单人跟踪控制器），或将接受者运动作为预处理好的固定轨迹（如**Kinematic-Recipient**基线），缺失了双方在物理反馈下的双向适应。**Phys-Reaction**等方法虽然在单人反应式控制上有效，但在辅助场景下无法生成稳定的接受者轨迹，未能作为直接基线。

2. **空间参考僵化。** 传统的全局坐标手部轨迹来自噪声MoCap数据，当支持者与接受者的相对位置因物理扰动而偏离参考时，固定参考会导致手部目标与实际身体位置错位，无法维持有效接触。

3. **奖励信号误导。** 标准的关节跟踪奖励（指数距离衰减）在近距离接触时会强制策略死板地跟踪噪声手部轨迹，而非鼓励功能性的力交互。这导致支持者可能“过度跟踪”不可靠参考，反而破坏辅助行为。

**本文的动机正是填补上述缺口。** AssistMimic首次将紧密接触辅助行为的物理仿真模仿形式化为多智能体强化学习（MARL）问题，通过联合训练支持者和接受者策略，使双方能够根据物理反馈双向适应。其核心洞察在于：从单人运动先验继承的权重提供了基础运动技能，使策略不必从零学习基本动力学；动态参考重映射确保手部目标始终与接受者的实时姿态对齐；接触促进奖励鼓励功能性的力交互而非死板跟踪噪声轨迹。三者协同，使紧密接触辅助行为的物理仿真模仿首次成为可能。

## 核心方法与创新机理

AssistMimic 的核心创新在于将紧密接触的人-人辅助行为模仿首次建模为**多智能体强化学习（MARL）问题**，并引入三个协同机制克服由此带来的训练不稳定与物理失配挑战。与现有工作形成鲜明对比：**Kinematic-Recipient**（Human-X）固定重放接受者运动学轨迹，导致姿态穿透与无效支持（Figure 4）；**Frozen-Recipient**（Sequential Training，基于 PHC）先冻结接受者再训练支持者，缺失双向适应；**Phys-Reaction** 的单人控制器在辅助场景下甚至无法生成稳定轨迹。AssistMimic 通过以下四个关键槽位变更，系统性地解决了上述瓶颈。

### 1. 训练范式：从顺序训练到联合 MARL

**基线做法**：独立或顺序训练——支持者基于预处理好的接受者运动进行学习，接受者策略被冻结或仅做运动学重放。

**AssistMimic 做法**：将双方策略置于同一个有限时域多智能体 MDP 中联合优化（Sec. 3.1）。支持者与接受者各自独立采样动作：
$$\mathbf{a}_t^{(m)} \sim \pi_m(\cdot \mid \mathbf{s}_t^{(m)}; \phi_m), \quad m \in \{\mathrm{S}, \mathrm{R}\}$$
联合目标为最大化折扣累积总回报：
$$J(\pi_{\mathrm{S}}, \pi_{\mathrm{R}}) = \mathbb{E}_{\tau \sim \mathcal{P}_\kappa} \left[ \sum_{t=0}^{T-1} \gamma^t (r_t^{(\mathrm{S})} + r_t^{(\mathrm{R})}) \right]$$
接受者策略在此框架下主动学习如何接受支持，而非被动重放。

**决定性证据**：Table 2 显示，在 Inter-X 数据集上，AssistMimic 的成功率（SR）达 74.9%，而 Sequential Training 仅为 62.4%，**联合训练提升 12.5 个百分点**。在未见动力学条件（Mass ×1.2）下，优势依然保持（57.9% vs 49.9%）。这证实了接受者需要主动学习接受支持而非被动重放的核心假设。

### 2. 策略初始化：从随机初始化到单人运动先验继承

**基线做法**：随机初始化策略网络权重，或仅对单个代理使用单人先验。

**AssistMimic 做法**：两个代理均从预训练的 PHC 单人跟踪控制器继承输入权重，新增的辅助特征维度用零填充（Sec. 3.2, Eqn. 7）：
$$\mathbf{W}_{\mathrm{new}}^{\mathrm{input}} = \left[ \mathbf{W}_{\mathrm{prior}}^{\mathrm{input}} \mid \mathbf{0} \right]$$
这使得策略在训练初期即具备基础运动技能（行走、平衡、转向等），无需从零学习基本动力学，从而将学习资源集中于交互协调。

**决定性证据**：消融实验表明，移除权重初始化导致**训练完全崩溃**——Inter-X 上成功率为 0%（Table 2），HHI-Assist 上出现奖励黑客行为（成功率 19.1% 但产生非功能性动作，Table 3）。这证明运动先验对于收敛不可或缺。

### 3. 手部参考目标：从固定全局轨迹到动态重映射

**基线做法**：使用动作捕捉数据中的固定全局坐标手部轨迹作为跟踪目标。

**AssistMimic 做法**：当支持者与接受者根关节距离低于阈值 $\tau_{\mathrm{dist}}$ 时，触发动态参考重映射（Sec. 3.3）。门控指示器为：
$$\mathcal{G}_t = \mathbb{I}\left( \left|\left| \mathbf{p}_{root,t}^{(S)} - \mathbf{p}_{root,t}^{(R)} \right|\right|_2 \leq \tau_{\mathrm{dist}} \right)$$
激活后，在标准参考空间中寻找接受者身体上距离支持者手部最近的关节作为锚点：
$$k_{i,t}^{*} = \arg\min_{k \in \mathcal{T}_R} \left|\left| \hat{\mathbf{p}}_{k,t}^{(R)} - \hat{\mathbf{p}}_{i,t}^{(S)} \right|\right|_2$$
手部跟踪目标随即根据该锚点实时偏移，确保目标始终与接受者当前姿态对齐，避免因固定全局参考导致的空间错位。

**决定性证据**：在 HHI-Assist 数据集的 Mass ×1.5 未见动力学条件下，移除动态参考重映射后成功率从 67.8% 骤降至 49.1%（Table 3），表明该模块对于在质量扰动下维持有效物理接触至关重要。定性结果（Figure 5）进一步显示，无此机制时支持者手部无法正确调整至接受者身体。

### 4. 近距离奖励：从跟踪误差到接触促进

**基线做法**：对手部轨迹严格执行标准的指数距离跟踪奖励。

**AssistMimic 做法**：当支持者手部与接受者上身关节邻近时，用接触促进奖励替换标准跟踪奖励（Sec. 3.4, Eqn. 11）：
$$r_{\mathrm{track}_i}^{(S)} = \begin{cases} \exp\left( -D\left( \hat{\mathbf{q}}_{i,t}^{(S)}, \mathbf{q}_{i,t}^{(S)} \right) \right) & \mathrm{if } \chi_{i,t}=0, \\ \beta f_{i,t} \exp(-\alpha d_{i,t}) + b_{\mathrm{contact}} & \mathrm{if } \chi_{i,t}=1 \end{cases}$$
该奖励包含力感知项（鼓励有意义的力交互）、距离惩罚（防止穿透）以及接触稀疏奖励，而不再死板地跟踪嘈杂的手部轨迹。这使策略能够学习功能性的力交换，而非表面地模仿运动学。

**决定性证据**：消融实验显示，移除接触促进奖励后，策略对未见动力学的鲁棒性严重退化——在最大髋扭矩减半条件下，成功率从 73.2% 降至 27.7%（Table 3），降幅达 45.5 个百分点。这证明接触促进奖励是策略泛化到动力学扰动的关键因素。

### 创新协同效应

上述四个创新并非孤立生效，而是形成协同链条：**运动先验初始化**提供稳定的起点，使 MARL 联合训练可行；**动态参考重映射**确保手部目标在空间上始终合理；**接触促进奖励**则引导策略在合理位置上产生功能性力交互。三者共同使紧密接触辅助行为的物理仿真模仿首次成为可能（Figure 2 橙色曲线）。此外，通过 DAgger 将按主题训练的专家策略蒸馏为通用策略后，Inter-X 上的成功率进一步提升至 94.7%（Table 4），验证了该框架的可扩展性。

AssistMimic 将紧密接触、力交换的人-人辅助运动模仿首次建模为一个**多智能体强化学习（MARL）问题**，其整体架构如图 3 所示。框架的核心思路是：不再将接受者（Recipient）视为被动重放的运动学对象，而是让支持者（Supporter）与接受者双方作为独立的物理仿真角色，在共享的物理环境中联合优化各自的策略，从而实现双向适应。

### 问题形式化：非对称多智能体 MDP

系统被定义为一个有限时域的多智能体马尔可夫决策过程 $\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{P}_\kappa, r, \gamma, T)$。两个智能体——支持者 $m = \mathrm{S}$ 与接受者 $m = \mathrm{R}$——在每一步分别从自己的策略中采样动作：

$$
\mathbf{a}_t^{(m)} \sim \pi_m(\cdot \mid \mathbf{s}_t^{(m)}; \phi_m), \quad m \in \{\mathrm{S}, \mathrm{R}\}
$$

关键设计在于**非对称动力学**：接受者被施加了物理损伤约束 $\kappa = (k_p, k_d, \tau_{\max})$，即降低的 PD 控制器增益与最大关节扭矩（详见表 1），以模拟需要辅助的身体状态。联合优化目标为最大化折扣累积总回报：

$$
J(\pi_{\mathrm{S}}, \pi_{\mathrm{R}}) = \mathbb{E}_{\tau \sim \mathcal{P}_\kappa} \left[ \sum_{t=0}^{T-1} \gamma^t (r_t^{(\mathrm{S})} + r_t^{(\mathrm{R})}) \right]
$$

### 策略网络架构与输入输出流

策略网络基于单人跟踪框架 PHC 扩展而来，每个智能体的策略 $\pi_m$ 接收三类输入：

- **本体感知状态** $s_{\mathrm{prior},t}^{(m)}$：包含自身关节旋转、位置、角速度与线速度；
- **辅助状态** $s_{\mathrm{assist},t}^{(m)}$：伙伴感知特征，包括伙伴的观测信息、双方的接触状态、自身受力以及上一步动作；
- **目标** $g_t^{(m)}$：来自参考运动序列的跟踪目标。

策略输出关节动作 $\mathbf{a}_t^{(m)}$，驱动物理仿真角色运动。两个策略共享相同的网络结构，但权重独立优化。

### 四大核心模块的协同关系

AssistMimic 的 pipeline 由四个关键机制串联构成，共同解决了从噪声动作捕捉数据中学习紧密接触辅助行为的根本困难：

1. **运动先验初始化（Motion Prior Initialization）**：两个智能体的策略权重均从 PHC 单人跟踪控制器继承，新增的辅助输入维度对应的权重置零：
   $$
   \mathbf{W}_{\mathrm{new}}^{\mathrm{input}} = \left[ \mathbf{W}_{\mathrm{prior}}^{\mathrm{input}} \mid \mathbf{0} \right]
   $$
   这使得策略在训练初期保留基本运动技能，无需从零学习行走、平衡等动力学。

2. **动态参考重映射（Dynamic Reference Retargeting）**：当双方根关节距离低于阈值 $\tau_{\mathrm{dist}}$ 时触发门控：
   $$
   \mathcal{G}_t = \mathbb{I}\left( \left|\left| \mathbf{p}_{root,t}^{(S)} - \mathbf{p}_{root,t}^{(R)} \right|\right|_2 \leq \tau_{\mathrm{dist}} \right)
   $$
   触发后，在标准参考空间中寻找接受者身体上距支持者手部最近的关节 $k_{i,t}^{*}$，并以此计算手部跟踪目标的偏移。这确保了手部参考始终与接受者的实时姿态对齐，避免因固定全局参考导致的空间错位。

3. **接触促进奖励（Contact-Promoting Reward）**：当支持者手部与接受者上身关节邻近时，用包含力感知项、距离惩罚与接触稀疏奖励的复合目标替换标准的指数距离跟踪奖励，鼓励功能性力交互而非死板跟踪嘈杂的手部轨迹。

4. **专家到通才蒸馏（Specialist-to-Generalist Distillation）**：先按主题聚类训练多个专家策略，再通过 DAgger 蒸馏为单一通才策略，以处理多样化的辅助行为。

这四个模块的因果链条清晰：运动先验提供训练的“可行起点”，动态参考重映射保证空间对齐的“物理合理性”，接触促进奖励定义“功能性成功”的优化方向，蒸馏则扩展“行为覆盖范围”。三者缺一不可——消融实验表明，移除任一机制都将导致训练崩溃或鲁棒性严重退化（详见实验分析部分）。

![[assets/figures/papers/paper_list_l1752_Learning_to_Assist_Physics_Grounded_Human_Human_Control_via_Multi_Agent/figures/004_Figure_3.jpg]]
*Figure 3: Overview of AssistMimic. We train tracking-based humanoid control policies for both the recipient and the supporter, optimizing them to imitate a paired reference motion sequence. Our architecture builds on the single-agent tracking framework of PHC [10], extending it with partner-aware state inputs and augmenting standard imitation rewards with recipient-aware reference retargeting and contact-incentivizing reward terms. The policy*

![[assets/figures/papers/paper_list_l1752_Learning_to_Assist_Physics_Grounded_Human_Human_Control_via_Multi_Agent/figures/001_Figure_1.jpg]]
*Figure 1: AssistMimic: We propose a multi-agent RL framework capable of learning robust Supporter and Recipient policies from noisy, close-proximity motion sequences. By leveraging single-person motion priors, a novel recipient-adaptive reference retargeting mechanism, and contact-promoting rewards, AssistMimic becomes the first physics-based controller to successfully track such complex, high-contact reference motions. Snapshots are arranged chronologically from left to right*

AssistMimic 将紧密接触的人-人辅助运动模仿建模为有限时域的多智能体马尔科夫决策过程（Multi-Agent MDP），其核心架构由四个关键模块协同构成：基于运动先验的权重初始化、伙伴感知的策略网络、动态参考重映射机制，以及接触促进奖励设计。以下逐一解析各模块的数学形式与设计逻辑。

### 多智能体 MDP 建模

问题被形式化为元组 $\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{P}_\kappa, r, \gamma, T)$，其中支持者（Supporter, S）和接受者（Recipient, R）构成两个独立智能体。接受者的动力学通过参数 $\kappa = (k_p, k_d, \tau_{\max})$ 显式约束，即降低其 PD 控制器增益和最大关节力矩以模拟物理损伤（参见 Table 1）。两智能体在每一步独立采样动作：

$$\mathbf{a}_t^{(m)} \sim \pi_m(\cdot \mid \mathbf{s}_t^{(m)}; \phi_m), \quad m \in \{\mathrm{S}, \mathrm{R}\}$$

联合优化目标为最大化折扣累积总回报：

$$J(\pi_{\mathrm{S}}, \pi_{\mathrm{R}}) = \mathbb{E}_{\tau \sim \mathcal{P}_\kappa} \left[ \sum_{t=0}^{T-1} \gamma^t (r_t^{(\mathrm{S})} + r_t^{(\mathrm{R})}) \right]$$

其中 $r_t^{(m)}$ 为各智能体单步奖励，由任务奖励和 AMP 判别器奖励加权组成：

$$r_{t}^{(m)} = \lambda_{\mathrm{task}} r_{\mathrm{task},t}^{(m)} + \lambda_{\mathrm{disc}} r_{\mathrm{disc},t}$$

任务奖励进一步分解为跟踪项、功率惩罚和辅助项：

$$r_{\mathrm{task},t}^{(m)} = \lambda_{\mathrm{track}} r_{\mathrm{track},t}^{(m)} + \lambda_{\mathrm{power}} r_{\mathrm{power},t}^{(m)} + \lambda_{\mathrm{assist}} r_{\mathrm{assist},t}^{(m)}$$

### 运动先验权重初始化

策略网络基于 PHC 单人跟踪控制器架构扩展，新增辅助状态输入维度。关键操作是将预训练的 PHC 输入权重矩阵 $\mathbf{W}_{\mathrm{prior}}^{\mathrm{input}}$ 与零矩阵拼接，使网络初始行为完全继承单人运动先验，而辅助特征对应的权重从零开始学习：

$$\mathbf{W}_{\mathrm{new}}^{\mathrm{input}} = \left[ \mathbf{W}_{\mathrm{prior}}^{\mathrm{input}} \mid \mathbf{0} \right]$$

这一设计确保策略不必从零学习基本动力学，而是以已有的稳定运动技能为基础逐步习得交互行为。消融实验表明，移除该初始化导致 Inter-X 数据集上成功率为 0%，HHI-Assist 上出现奖励黑客行为（成功率 19.1% 但动作无功能），证实运动先验是不可或缺的收敛条件。

### 伙伴感知策略网络

每个智能体的策略网络输入由三部分组成：本体感知状态 $s_{\mathrm{prior},t}^{(m)}$（包含关节旋转、位置、角速度和线速度）、辅助状态 $s_{\mathrm{assist},t}^{(m)}$（包含伙伴观测、接触状态、自身受力、上一步动作），以及目标 $g_t^{(m)}$。网络输出关节动作 $\mathbf{a}_t^{(m)}$，整体架构如 Figure 3 所示。支持者的最终奖励还耦合了接受者的奖励，以显式鼓励协助行为：

$$r_t^{(S)} = \frac{1}{2} \tilde{r}_t^{(S)} + \frac{1}{2} \tilde{r}_t^{(R)}, \quad r_t^{(R)} = \tilde{r}_t^{(R)}$$

### 动态参考重映射

动作捕捉数据中的手部参考轨迹是固定全局坐标，当接受者姿态偏移时直接跟踪会导致空间错位。AssistMimic 引入门控机制，当两角色根关节距离低于阈值 $\tau_{\mathrm{dist}}$ 时激活重映射：

$$\mathcal{G}_t = \mathbb{I}\left( \left|\left| \mathbf{p}_{root,t}^{(S)} - \mathbf{p}_{root,t}^{(R)} \right|\right|_2 \leq \tau_{\mathrm{dist}} \right)$$

激活后，在标准参考空间中寻找接受者身体上距支持者手部最近的关节作为锚点：

$$k_{i,t}^{*} = \arg\min_{k \in \mathcal{T}_R} \left|\left| \hat{\mathbf{p}}_{k,t}^{(R)} - \hat{\mathbf{p}}_{i,t}^{(S)} \right|\right|_2$$

手部跟踪目标随即被重映射为该锚点的当前位置加上偏移量，确保手部参考始终与接受者实时姿态对齐。消融实验显示，移除该模块后，在 HHI-Assist 的 Mass×1.5 未见动力学条件下成功率从 67.8% 骤降至 49.1%，证明其对维持有效物理接触至关重要。

### 接触促进奖励

标准跟踪奖励在近距离接触时对手部轨迹严格执行，但动作捕捉中的手部数据常因遮挡而严重噪声化。AssistMimic 根据手部与接受者上身关节的距离门控 $\chi_{i,t}$ 切换奖励函数：

$$r_{\mathrm{track}_i}^{(S)} = \begin{cases} \exp\left( -D\left( \hat{\mathbf{q}}_{i,t}^{(S)}, \mathbf{q}_{i,t}^{(S)} \right) \right) & \mathrm{if } \chi_{i,t}=0, \\ \beta f_{i,t} \exp(-\alpha d_{i,t}) + b_{\mathrm{contact}} & \mathrm{if } \chi_{i,t}=1 \end{cases}$$

当双方远离时（$\chi_{i,t}=0$），使用标准指数距离跟踪奖励；当接近时（$\chi_{i,t}=1$），切换为接触促进奖励，其中 $f_{i,t}$ 为接触力，$d_{i,t}$ 为手部到目标关节的距离，$\beta$ 和 $\alpha$ 为缩放系数，$b_{\mathrm{contact}}$ 为接触稀疏奖励。这一设计鼓励功能性的力交互而非死板跟踪噪声轨迹。消融表明，移除该奖励后，在最大髋扭矩减半条件下成功率从 73.2% 暴跌至 27.7%，验证了其对未见动态鲁棒性的关键作用。

## 实验与关键发现

### 核心实验设置

实验在两个具有物理接触的辅助交互数据集上评估：**Inter-X**（Xu et al., ECCV 2024）和 **HHI-Assist**（Shibata et al., 2024）。受助者（Recipient）被施加标准化的物理限制——降低的 PD 增益和最大关节力矩（详见表 1），以模拟一致的损伤程度。支持者（Supporter）保持正常动力学参数。

评估采用两个主要指标：
- **成功率（Success Rate, SR↑）**：两个角色全身位置偏差均保持在 0.5 m 阈值内的回合百分比。
- **平均每关节位置误差（MPJPE↓）**：仿真与参考关节位置的平均偏差。

在 HHI-Assist 床场景评估中，丢弃每段末尾 15 帧——此时支持者已离开，受助者的自然摔倒不应算作辅助失败，确保各方法在可比的时间窗口内被评估。训练采用 PPO，按主题聚类训练专家策略（specialist），并通过 DAgger 蒸馏为通用策略（generalist）。所有消融实验均保持此公平性框架。

### 主结果：MARL 联合训练的必要性

表 2 展示了 Inter-X 数据集上专家策略的定量结果。AssistMimic 在标准动力学下达到 **74.9%** 的成功率，相比顺序训练基线（Sequential Training，先微调并冻结受助者策略再训练支持者）的 62.4% 提升 **+12.5 个百分点**。在未见动力学（Mass ×1.2）条件下，AssistMimic 保持 57.9% 的成功率，仍领先顺序训练的 49.9%（+8.0 个百分点）。

这一差距的因果机制在于：顺序训练中受助者被动重放运动学轨迹，无法根据支持者的实际接触力进行双向适应，导致物理不一致累积和姿态穿透。相比之下，MARL 联合训练允许受助者主动学习“如何被支持”，从而在力交换中形成稳定的耦合动力学。

表 4 进一步显示，经 DAgger 蒸馏的通用策略在 Inter-X 上达到 **94.7%** 的成功率，显著优于未蒸馏的 AssistMimic（77.3%），提升 +17.4 个百分点，表明专家到通用的知识迁移有效聚合了多主题的辅助技能。

在 HHI-Assist 数据集上（表 3），AssistMimic 专家策略在标准动力学下达到 **85.8%** 的成功率，验证了方法在不同辅助场景（如床到轮椅转移）上的泛化能力。

### 消融实验：三个关键机制的证据链

消融实验系统性地拆解了 AssistMimic 的三个核心设计，揭示了各自的因果贡献：

**1. 策略权重初始化（Weight Initialization）——训练收敛的必要条件**

移除从 PHC 单人运动跟踪控制器继承的权重（随机初始化），导致训练完全崩溃：Inter-X 上成功率为 **0%**；HHI-Assist 上虽出现 19.1% 的成功率，但产生的是奖励黑客行为——策略学会满足形式上的跟踪指标却未产生功能性辅助动作（图 9 定性展示）。这一消融证明：单人运动先验提供了基础运动技能（平衡、行走、姿态控制），使策略不必从零学习基本动力学，是多智能体交互学习的必要前提。

**2. 动态参考重映射（Dynamic Reference Retargeting）——接触维持的空间锚定**

移除该模块后，在 HHI-Assist 的 Mass ×1.5 未见动力学条件下，成功率从 **67.8% 骤降至 49.1%**（表 3）。当受助者质量增加 1.5 倍时，其运动轨迹与参考发生显著偏移；固定全局手部参考导致支持者手部目标与受助者身体空间错位，无法维持有效接触。动态重映射通过实时将手部目标绑定到受助者当前姿态下的最近关节（公式 8-9），确保支持者始终“跟随”受助者的身体，从而在动力学扰动下保持接触。

值得注意的是，该模块在 Inter-X 数据集上未见显著增益，表明某些交互场景下固定参考已足够，但论文未深入分析原因——这一点需要读者自行验证具体场景差异。

**3. 接触促进奖励（Contact-Promoting Reward）——鲁棒性的关键**

移除接触促进奖励（回退到标准指数距离跟踪），对未见动力学的鲁棒性严重退化：在最大髋扭矩减半（Max hip torque ×0.5）条件下，成功率从 **73.2% 降至 27.7%**（表 3）。标准跟踪奖励在近距离接触时强制执行嘈杂的手部轨迹，导致策略为满足跟踪指标而牺牲功能性力交互。接触促进奖励在近距离时切换到力感知项 $\beta f_{i,t} \exp(-\alpha d_{i,t})$ 和接触稀疏奖励 $b_{\mathrm{contact}}$（公式 11），鼓励产生有意义的接触力而非死板跟踪，从而在受助者动力学能力变化时保持辅助有效性。

### 稳定性分析：受助者质心控制

表 5 报告了 HHI-Assist 上受助者质心（COM）标准差。AssistMimic 达到 **0.0921**，优于移除动态参考重映射的变体（0.0989）。更低的 COM 标准差表明受助者在辅助过程中的姿态更稳定，间接验证了动态参考重映射通过维持有效接触减少了受助者的平衡补偿需求。

### 失败模式与局限

定性分析揭示了以下主要失败模式：

1. **手部灵巧度不足**：当前手部模型为胶囊手（capsule hand），缺乏手指关节的精细控制能力，导致抓取等精细交互失败（图 7(b)）。这是物理仿真人形角色的固有局限，需要更复杂的手部模型和相应的强化学习探索。

2. **参考质量依赖**：方法依赖动作捕捉参考轨迹；当参考存在严重遮挡噪声或属于分布外交互时，跟踪质量下降。图 6 展示了对运动扩散模型生成轨迹的跟踪结果，虽能实现基本跟随，但精度低于对动作捕捉数据的跟踪。

3. **仿真到真实的鸿沟**：所有实验在 Isaac Gym 物理仿真器中进行，尚未在真实人形机器人硬件上验证。多智能体接触场景下的 sim-to-real 迁移面临接触动力学建模误差、状态估计噪声等额外挑战。

4. **动态重映射的场景依赖性**：如前所述，该模块在 Inter-X 上增益不显著，其适用条件（接触距离、交互类型）需要进一步表征。

![[assets/figures/papers/paper_list_l1752_Learning_to_Assist_Physics_Grounded_Human_Human_Control_via_Multi_Agent/figures/006_Table_2.jpg]]
*Table 2: Evaluation of specialist policies on the Inter-X dataset*

![[assets/figures/papers/paper_list_l1752_Learning_to_Assist_Physics_Grounded_Human_Human_Control_via_Multi_Agent/figures/007_Table_3.jpg]]
*Table 3: Evaluation of specialist policies on the HHI-Assist dataset*

![[assets/figures/papers/paper_list_l1752_Learning_to_Assist_Physics_Grounded_Human_Human_Control_via_Multi_Agent/figures/011_Figure_5.jpg]]
*Figure 5: Qualitative results on HHI-Assist. Red boxes indicate correct hand adjustment and support*

![[assets/figures/papers/paper_list_l1752_Learning_to_Assist_Physics_Grounded_Human_Human_Control_via_Multi_Agent/figures/009_Figure_7.jpg]]
*Figure 7: Qualitative results: unseen interactions and failures*

## 定位与知识库关联

### 1. 问题定位：从单人模仿到紧密接触辅助的范式缺口

AssistMimic 试图填补物理仿真人类运动模仿领域的一个明确空白。现有的物理仿真方法已能较好地处理两类场景：一是**单人运动跟踪**，如 PHC 等基于强化学习的控制器可在孤立动作上取得高成功率；二是**无接触的社会交互**，如两人共舞或并行行走，此时角色间无需力交换，各自跟踪独立参考即可。然而，**紧密接触的辅助行为**（如搀扶行走、床上翻身辅助）提出了根本不同的挑战——角色之间必须发生持续的力交换，且双方需要根据物理反馈进行**双向适应**。在此类场景下，单独训练或运动学重放的范式会破坏物理一致性：若接受者仅被动重放动作捕捉轨迹，支持者施加的力将导致姿态穿透、滑步甚至摔倒（Figure 4 展示了运动学基线的典型失败模式）。同时，动作捕捉数据在近距离交互时存在严重遮挡和噪声，使得手部接触参考本身不可靠，直接将其作为跟踪目标会导致强化学习训练不稳定。

### 2. 与基线方法的关系

#### 2.1 运动学重放基线：Human-X 范式

最直接的对比基线是**固定运动学重放接受者轨迹**的范式（文中称为 Human-X ）。在该设定下，接受者按动作捕捉数据以运动学方式重放，支持者则学习一个反应式策略去配合。这一方法本质上是将辅助问题退化为单人跟踪问题，完全回避了接受者的物理响应。AssistMimic 的实验表明，该范式在需要力支撑的场景中系统性失败——接受者无法对支持者的力做出物理反应，导致穿透和无效支撑（Figure 4）。

#### 2.2 顺序训练基线：Frozen-Recipient

更接近的竞争基线是**顺序训练**（Sequential Training），即先基于 PHC 微调并冻结接受者策略，再训练支持者去协调。这代表了“去耦合学习”的思路：先让接受者学会在受损状态下独立运动，再让支持者适应一个固定的接受者。在 Inter-X 数据集上，顺序训练的成功率为 62.4%，而 AssistMimic 的联合 MARL 训练达到 74.9%（Table 2），提升 **12.5 个百分点**。这一差距直接验证了核心假设：**接受者需要主动学习如何接受支持**，而非被动重放或执行固定的受损运动策略。在未见动力学条件下（质量 ×1.2），差距仍达 8.0 个百分点（57.9% vs 49.9%），表明双向适应对泛化同样关键。

#### 2.3 不可行的基线：Phys-Reaction

文中还提及了 **Phys-Reaction **，该方法采用隔离回放的单人控制器。但在辅助场景下，接受者的运动因外力干扰而显著偏离其原始参考，导致该控制器无法生成稳定轨迹，因此未能作为直接基线参与定量比较。

### 3. 方法适用边界

AssistMimic 的有效性建立在以下前提之上：

- **参考数据可用**：方法依赖成对的动作捕捉参考轨迹（如 Inter-X 和 HHI-Assist 数据集）。对于完全生成的或分布外的交互序列，跟踪质量可能下降，尽管 Figure 6 展示了在运动扩散模型生成的交互轨迹上的初步跟踪结果。
- **接触类型为辅助性支撑**：方法针对的是“支持者用手部接触接受者上身”的辅助范式（搀扶、翻身等），动态参考重映射和接触促进奖励均围绕这一交互模式设计。对于其他类型的紧密接触（如格斗、双人杂技），奖励设计和参考重映射逻辑可能需要调整。
- **仿真环境中的类人机器人**：所有训练和评估在 Isaac Gym 物理仿真器中进行，角色模型为类人机器人。尚未在真实硬件上验证。
- **手部灵巧度有限**：当前使用胶囊手模型，无法执行抓取等精细操作，这成为部分失败案例的直接原因（Figure 7(b)）。

### 4. 局限性与开放问题

#### 4.1 已明确的局限

1. **手部建模粗糙**：胶囊手缺乏手指自由度，难以可靠地实现抓握、拉拽等需要精细接触的辅助动作。这是当前方法最直接的工程瓶颈。
2. **对参考质量的依赖**：方法未联合优化动作捕捉去噪与控制器学习。在高度遮挡的近距离交互数据中，参考轨迹的噪声会通过奖励信号传导至策略学习，可能限制最终性能。
3. **仿真到真实的鸿沟**：多智能体接触场景下的 sim-to-real 迁移尚未探索。接触动力学的仿真误差、状态估计噪声以及真实机器人的执行延迟都是潜在的迁移障碍。
4. **动态参考重映射的适用性差异**：消融实验显示，动态参考重映射在 HHI-Assist 上至关重要（移除后 Mass×1.5 条件下成功率从 67.8% 降至 49.1%，Table 3），但在 Inter-X 上未见显著增益。这一现象的原因尚未深入分析，可能与 Inter-X 中支持者手部轨迹本身已与接受者身体保持较好对齐有关。

#### 4.2 开放问题

1. **感知集成**：当前策略仅依赖本体感知和辅助状态（包括合作伙伴的身体状态）。能否将视觉观察（如 RGB-D 相机）集成到策略中，使角色实时感知并适应合作者的视觉状态，是向真实部署迈进的关键一步。
2. **规划与控制耦合**：Figure 6 展示了 AssistMimic 跟踪运动扩散模型生成轨迹的初步结果。能否更紧密地耦合运动规划器和物理控制器——例如在规划阶段就引入物理可行性先验——以提升对动态合作者的在线协调能力？
3. **动作捕捉去噪的联合学习**：能否将去噪与控制器学习纳入同一优化框架，从高度遮挡的近距离交互数据中提取可靠参考，同时学习鲁棒的物理策略？
4. **跨形态迁移**：方法在类人机器人上验证。对于不同形态的辅助机器人（如移动机械臂、外骨骼），框架的适应性如何？这涉及状态空间和动作空间的重新设计，以及接触奖励的重新定义。

### 5. 在知识库中的位置

AssistMimic 在物理仿真人类运动模仿的知识谱系中占据了一个独特位置：

- **上游继承**：直接建立在 PHC（单人物理跟踪控制器）的架构和预训练权重之上，继承了其基于 AMP 判别器的风格奖励和 PPO 训练框架。
- **横向对比**：区别于 Human-X 的运动学重放范式和 Phys-Reaction 的隔离回放范式，首次将紧密接触辅助行为形式化为多智能体强化学习问题，并通过三个关键机制（运动先验初始化、动态参考重映射、接触促进奖励）使其可行。
- **下游可能影响**：为物理仿真中的社会交互研究开辟了新方向——从无接触交互走向力交换交互。其“专家到通才蒸馏”的范式（Table 4，DAgger 蒸馏后 Inter-X 通才成功率达 94.7%）也为多任务物理交互控制提供了可参考的路线。

## 原文 PDF

![[paperPDFs/CVPR_2026/Learning_to_Assist_Physics_Grounded_Human_Human_Control_via_Multi_Agent_Reinforcement_Learning.pdf]]
