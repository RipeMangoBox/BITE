---
title: "VS-Bench: Evaluating VLMs for Strategic Abilities in Multi-Agent Environments"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VS_Bench_Evaluating_VLMs_for_Strategic_Abilities_in_Multi_Agent_Environments.pdf
project_link: null
code_link: null
aliases:
- VBVSB
- VS-Bench
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入显式推理过程（如推理模型或思维链提示）能一定程度上提升多智能体策略能力，但当前模型仍远未达到稳健的博弈论最优表现。
primary_logic: 当前 VLMs 的感知能力较强（最高 84.9% 准确率），但将感知信息转化为有效的多步策略推理和优化的累积回报决策是主要鸿沟，尤其体现在视频类游戏和社交困境中。
claims:
- 最佳推理模型 o3 在十种环境下的平均策略推理准确率仅为 46.6%（Table 3）。
- 最佳模型 o3 的平均决策归一化回报仅为 31.4，远低于随机基线的 0 值，多款模型表现甚至低于随机（Table 4）。
- 人类参与者在相同环境下的平均归一化回报为 62.7，o3 仅超过 12.9% 的人类被试（Section 4.4, Figure 6）。
- 思维链（CoT）提示大幅提升聊天模型在三种环境中的决策表现，但推理模型仍最高（Section 4.2, Figure 4）。
---

# VS-Bench: Evaluating VLMs for Strategic Abilities in Multi-Agent Environments

> [!tip] 核心洞察
> 当前 VLMs 的感知能力较强（最高 84.9% 准确率），但将感知信息转化为有效的多步策略推理和优化的累积回报决策是主要鸿沟，尤其体现在视频类游戏和社交困境中。

| 字段 | 内容 |
|------|------|
| 中文题名 | VS-Bench：评估视觉语言模型在多智能体环境中的策略能力 |
| 英文题名 | VS-Bench: Evaluating VLMs for Strategic Abilities in Multi-Agent Environments |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2506.02387) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VS-BENCH (Visual Strategic Benchmark) |
| Dataset | VS-BENCH Overall, Human Baseline |

> [!tip] 效果简介
> - VS-BENCH Overall 上，Perception Accuracy 84.9% (o3) vs 100% (Oracle) (-15.1%)；Strategic Reasoning Accuracy 46.6% (o3) vs 100% (Oracle) (-53.4%)；Decision-making Normalized Return 31.4 (o3) vs 100 (Oracle) (-68.6)。
> - Human Baseline (VS-BENCH) 上，Normalized Return 31.4 (o3) vs 62.7 (Human avg.) (-31.3)。

## 概要

多智能体环境中的策略交互——从合作烹饪到竞争博弈——要求智能体同时具备精准的视觉感知、对其他参与者意图的推断能力，以及面向长期回报的最优决策规划。现有视觉语言模型（VLMs）在静态视觉问答上表现亮眼，但当任务要求它们在**非平稳多智能体动态**下进行策略推理与决策时，其能力边界尚不清晰。

**VS-Bench** 正是为系统探测这一边界而构建的多模态基准。它将评估建模为**部分可观察马尔可夫博弈（POMG）**，覆盖合作、竞争与混合动机三类博弈结构，在十种视觉环境中从感知、策略推理、决策三个维度对十五款 VLM 进行统一测度。其核心发现是：当前 VLMs 的**感知能力相对稳健**（最佳模型 o3 总体准确率达 84.9%），但将感知信息转化为有效的**多步策略推理与优化决策**构成主要瓶颈——最佳推理模型 o3 的策略推理准确率仅为 46.6%，决策归一化回报仅 31.4，远低于人类平均的 62.7，且仅超过 12.9% 的人类被试。

这一感知-推理-决策的能力断层揭示了关键因果机制：**引入显式推理过程**（如推理模型或思维链提示）可部分弥合鸿沟，但当前最先进模型仍远未达到稳健的博弈论最优表现。多模态视觉输入本身也增加了任务难度——纯文本条件下模型决策表现略优，暗示视觉复杂性对策略推理存在额外干扰。VS-Bench 由此为“多模态基础模型如何走向策略自主”这一开放问题提供了量化标尺与诊断工具。



视觉语言模型（Vision-Language Models, VLMs）近年来在图像描述、视觉问答等静态感知任务上取得了显著进展。然而，现实世界中的智能体往往需要在多智能体环境中运作——自动驾驶车辆需预判其他驾驶者的意图，家用机器人需与家庭成员协作完成任务。这类场景的核心挑战在于：**智能体不仅要准确感知环境，还必须对非平稳的其他智能体行为进行策略推理，并在此基础上做出长期最优决策**。

现有的 VLM 评估基准（如 MMLU、MMBench 等）主要聚焦于单智能体的静态感知与知识问答，几乎不涉及多智能体动态交互下的策略能力评测。少数涉及博弈或决策的基准（如 GTBench、GameBench）则缺乏对感知、推理、决策三个维度的系统性解耦评估，难以定位 VLM 在多智能体场景中的具体能力瓶颈。这导致一个关键问题悬而未决：**当前 VLMs 是否具备在视觉感知基础上进行多步策略推理与博弈决策的能力？**

为填补这一空白，本文提出了 **VS-BENCH（Visual Strategic Benchmark）**，一个面向多智能体环境的 VLM 策略能力评估基准。VS-BENCH 将多智能体交互形式化为部分可观察马尔可夫博弈（Partially Observable Markov Game, POMG）：

$$\mathcal { G } = ( \mathcal { N } , S , \{ \mathcal { A } _ { i } \} _ { i \in \mathcal { N } } , \{ \mathcal { O } _ { i } \} _ { i \in \mathcal { N } } , \mathcal { P } , \{ \mathcal { R } _ { i } \} _ { i \in \mathcal { N } } , \gamma )$$

其中每个智能体 $i$ 接收多模态观察 $\mathcal{O}_i$（包含图像与文本），目标是最大化期望折扣累积回报：

$$\mathbb { E } _ { \pi _ { 1 } , \cdots , \pi _ { n } } \left[ \sum _ { t } \gamma ^ { t } r _ { i , t } \right]$$

基准涵盖了合作（$\mathcal{R}_1 = \cdots = \mathcal{R}_n$）、竞争（$\sum_i \mathcal{R}_i = 0$）以及混合动机（回报既不相同也不为零和）三类博弈结构，覆盖十种视觉环境（包括 Hanabi、Overcooked、Breakthrough、Poker 等），并在三个维度上对 VLM 进行解耦评估：**感知**（元素识别准确率）、**策略推理**（对其他智能体下一步行动的预测准确率）、**决策**（归一化回合回报）。这一设计使得研究者能够精确诊断 VLM 在多智能体场景中“卡在哪里”。



## 核心方法与创新机理

VS-BENCH 的核心创新并非提出新的模型架构或训练范式，而在于**构建了首个系统性评估视觉语言模型（VLMs）在多智能体环境中策略能力的多模态基准**，并通过三维度解耦评估框架，揭示了当前 VLMs 从感知到策略决策的深层能力鸿沟。

### 1. 问题定义的创新：将 VLM 评估拓展至多智能体策略博弈

现有 VLM 基准主要关注单智能体的视觉问答、图像描述或简单指令遵循。VS-BENCH 首次将评估场景形式化地置于**部分可观察马尔可夫博弈（POMG）**框架下：

$$\mathcal { G } = ( \mathcal { N } , S , \{ \mathcal { A } _ { i } \} _ { i \in \mathcal { N } } , \{ \mathcal { O } _ { i } \} _ { i \in \mathcal { N } } , \mathcal { P } , \{ \mathcal { R } _ { i } \} _ { i \in \mathcal { N } } , \gamma )$$

其中每个 VLM 智能体通过多模态观察空间 $\mathcal { O } _ { i } = ( \mathcal { T } _ { i } , \mathcal { T } _ { i } )$（图像与文本）感知环境，并输出文本动作。这一设定要求模型同时应对**非平稳动态**（其他智能体的策略随时间变化）和**部分可观察性**，这是传统 VLM 基准从未触及的挑战。

### 2. 评估维度的创新：感知-推理-决策三层解耦

VS-BENCH 的关键设计在于将策略能力拆解为三个递进的评估维度，形成因果诊断链路：

- **感知模块**：测量基本视觉元素识别准确率，作为策略能力的下界保障。
- **策略推理模块**：测量模型对其他智能体下一步行动的预测准确率，直接评估意图建模能力。
- **决策模块**：测量归一化回合回报，综合评估长期规划与均衡选择能力。

这一解耦设计使得研究者能够定位 VLM 失败的具体环节。实验证据表明，**感知能力并非主要瓶颈**——最佳模型 o3 在感知维度达到 84.9% 的总体准确率（Table 2），但策略推理准确率骤降至 46.6%（Table 3），决策归一化回报仅为 31.4（Oracle=100，Table 4）。这清晰地揭示了**从“看见”到“理解意图”再到“做出最优决策”之间存在显著的逐级能力衰减**。

### 3. 环境设计的创新：覆盖三大博弈类型的十种视觉场景

VS-BENCH 的环境分类体系（Table 1）系统性地覆盖了多智能体交互的三种核心博弈类型：

- **合作博弈**：$\mathcal { R } _ { 1 } ( s , a ) = \cdots = \mathcal { R } _ { n } ( s , a )$，所有智能体共享回报函数。
- **竞争博弈**：$\sum _ { i = 1 } ^ { n } \mathcal { R } _ { i } ( s , a ) = 0$，满足零和性质。
- **混合动机博弈**：$\mathcal { R } _ { i } ( s , a ) \neq \mathcal { R } _ { j } ( s , a ) \text { 且 } \sum _ { i = 1 } ^ { n } \mathcal { R } _ { i } ( s , a ) \neq 0$，回报既不相同也不为零和。

十种环境横跨棋类博弈（Breakthrough）、体育竞技（Pong）、资源竞争（Hunt）、社交困境（Coin Dilemma、Battle）和协作任务（Overcooked、Hanabi）等场景，要求模型具备空间推理、意图预测、博弈论均衡选择和长期规划等差异化能力。

### 4. 相对于现有基准的 changed slots

| 维度 | 现有 VLM 基准 | VS-BENCH 的改变 |
|------|--------------|----------------|
| 智能体数量 | 单智能体为主 | 多智能体（2 名及以上） |
| 环境动态性 | 静态或平稳 | 非平稳（对手策略自适应变化） |
| 评估目标 | 感知/问答准确率 | 感知→推理→决策的三层策略能力 |
| 博弈类型 | 无 | 合作/竞争/混合动机全覆盖 |
| 基线参照 | 人工标注真值 | Random Agent（下界）与 Oracle Agent（上界）双边界校准 |
| 人类对标 | 通常缺失 | 提供人类参与者在相同环境下的决策分布（Figure 6） |

### 5. 因果调控变量的发现

VS-BENCH 的消融分析揭示了两个关键的因果调控变量：

- **推理过程的显式注入**：思维链（CoT）提示可显著提升聊天模型的决策性能，但推理模型（如 o3）仍保持最优（Figure 4），表明**架构级的推理能力**比提示工程更有效。
- **多模态视觉输入的影响**：纯文本观察条件下 VLMs 决策表现略优于多模态输入（Figure 3），暗示当前模型的视觉-策略转化通路存在信息损耗，但即便在纯文本条件下，性能仍远低于 Oracle，说明**策略推理本身**（而非视觉感知）是核心短板。

这些发现为后续研究指明了方向：提升 VLM 在多智能体环境中的策略能力，关键在于增强其博弈论推理和长期规划能力，而非单纯改进视觉编码器。



VS-BENCH 将多智能体环境中的 VLM 能力评估建模为一个部分可观察马尔可夫博弈（POMG），并围绕该形式化框架构建了三阶段评估管线。整个基准的输入是多模态观察，输出是分层的能力度量，其核心逻辑如图 Figure 2 所示。

![[assets/figures/papers/paper_list_l2050_https_arxiv_org_abs_2506_02387/figures/002_Figure_2.jpg]]
*Figure 2: Overview of VS-BENCH, a multimodal benchmark for evaluating VLMs in multi-agent environments. We evaluate fifteen models in ten vision-grounded environments across three dimensions, including perception measured by element recognition accuracy, strategic reasoning measured by next-action prediction accuracy, and decision-making measured by normalized episode return*

### 形式化建模

基准将多智能体交互定义为一个 POMG 元组：

$$
\mathcal{G} = (\mathcal{N}, S, \{\mathcal{A}_i\}_{i \in \mathcal{N}}, \{\mathcal{O}_i\}_{i \in \mathcal{N}}, \mathcal{P}, \{\mathcal{R}_i\}_{i \in \mathcal{N}}, \gamma)
$$

其中 $\mathcal{N}$ 为智能体集合，$S$ 为全局状态空间，$\mathcal{A}_i$ 为智能体 $i$ 的动作空间，$\mathcal{O}_i$ 为观察空间，$\mathcal{P}$ 为状态转移概率，$\mathcal{R}_i$ 为回报函数，$\gamma$ 为折扣因子。每个智能体的目标是最大化期望累积回报：

$$
\mathbb{E}_{\pi_1, \cdots, \pi_n} \left[ \sum_t \gamma^t r_{i,t} \right]
$$

为适配 VLM 的输入输出特性，VS-BENCH 将观察空间设计为多模态形式 $\mathcal{O}_i = (\mathcal{I}_i, \mathcal{T}_i)$，其中 $\mathcal{I}_i$ 为图像观察空间，$\mathcal{T}_i$ 为文本观察空间。动作空间则映射为文本动作空间 $\tilde{\mathcal{A}}_i$，并通过映射函数 $\mathcal{M}: \tilde{\mathcal{A}}_i \to \mathcal{A}_i$ 将文本动作转换为环境可执行的原生动作。

根据回报函数的结构，十种环境被分为三类博弈形态：
- **合作博弈**：$\mathcal{R}_1(s, a) = \cdots = \mathcal{R}_n(s, a)$，所有智能体共享同一回报；
- **竞争博弈**：$\sum_{i=1}^{n} \mathcal{R}_i(s, a) = 0$，满足零和性质；
- **混合动机博弈**：$\mathcal{R}_i(s, a) \neq \mathcal{R}_j(s, a)$ 且 $\sum_{i=1}^{n} \mathcal{R}_i(s, a) \neq 0$，回报既不相同也不为零和。

### 三阶段评估管线

评估管线由三个级联模块组成，每个模块度量 VLM 在策略决策链上不同层级的能力（Figure 2）：

1. **感知评估模块**：测量模型对视觉观察中基本元素的识别准确率（element recognition accuracy）。该模块作为能力基线的第一道关口，检验模型是否具备“看见”环境状态的前提条件。实验表明，所有模型至少达到 67.8% 的整体准确率，最佳模型 o3 达到 84.9%（Table 2），感知能力整体较强。

2. **策略推理评估模块**：测量模型对其他智能体下一步行动的预测准确率。该模块直接评估模型在非平稳多智能体动态中推断对手意图的能力。最佳模型 o3 的整体准确率仅为 46.6%（Table 3），在六个环境中排名第一，但这一结果揭示了从感知到意图推理的巨大落差。

3. **决策评估模块**：测量模型在多步交互中的归一化回合回报（normalized return），以 Oracle 策略为 100、随机策略为 0 进行归一化。该模块综合评估长期规划与均衡选择能力。最佳模型 o3 的归一化回报仅为 31.4，四款模型表现低于随机基线（Table 4），表明当前 VLMs 在将感知与推理转化为优化决策的环节存在系统性缺陷。

### 评估配置

评估覆盖十五款主流 VLM，包括推理模型（如 o3、gemini-2.5-pro）和聊天模型（如 gpt-4.1、claude-3-7-sonnet）。所有模型在相同条件下测试：温度设为 1.0，最大输出 tokens 为 8k，推理模型的额外 tokens 上限设为 16k，以确保可比性。十种环境覆盖合作、竞争、混合动机三类博弈，具体分类与所需能力矩阵见 Table 1。



### 2.1 多智能体部分可观察马尔可夫博弈（POMG）建模

VS-BENCH 将多智能体环境形式化为部分可观察马尔可夫博弈（Partially Observable Markov Game, POMG）。该框架为评估 VLM 智能体在非平稳动态下的策略能力提供了统一的数学基础。

**POMG 形式化定义**（Section 2.1）：

$$
\mathcal { G } = ( \mathcal { N } , S , \{ \mathcal { A } _ { i } \} _ { i \in \mathcal { N } } , \{ \mathcal { O } _ { i } \} _ { i \in \mathcal { N } } , \mathcal { P } , \{ \mathcal { R } _ { i } \} _ { i \in \mathcal { N } } , \gamma )
$$

其中各符号含义如下：
- $\mathcal{N}$：智能体集合
- $S$：全局状态空间
- $\mathcal{A}_i$：智能体 $i$ 的动作空间
- $\mathcal{O}_i$：智能体 $i$ 的观察空间
- $\mathcal{P}$：状态转移概率函数
- $\mathcal{R}_i$：智能体 $i$ 的回报函数
- $\gamma$：折扣因子

每个智能体 $i$ 的目标是最大化其期望折扣累积回报：

$$
\mathbb { E } _ { \pi _ { 1 } , \cdots , \pi _ { n } } \left[ \sum _ { t } \gamma ^ { t } r _ { i , t } \right]
$$

其中 $r_{i,t} = \mathcal{R}_i(s_t, a_t)$ 表示智能体 $i$ 在时刻 $t$ 获得的即时奖励。

### 2.2 面向 VLM 智能体的多模态观察与动作空间

为适配 VLM 的输入输出特性，VS-BENCH 对标准 POMG 框架进行了两项关键改造（Section 2.2）：

**多模态观察空间**：将原始的观察空间 $\mathcal{O}_i$ 扩展为图像与文本的联合空间 $\mathcal{O}_i = (\mathcal{I}_i, \mathcal{T}_i)$，其中 $\mathcal{I}_i$ 为图像观察空间（如游戏截图），$\mathcal{T}_i$ 为文本观察空间（如状态描述、历史动作序列）。这一设计使评估能同时考察 VLMs 的视觉感知与文本理解能力。

**文本动作空间与映射**：引入文本动作空间 $\tilde{\mathcal{A}}_i$ 及映射函数 $\mathcal{M}: \tilde{\mathcal{A}}_i \to \mathcal{A}_i$，将 VLM 输出的自然语言动作指令转换为环境可执行的动作。这保证了评估协议与原始环境接口的兼容性。

### 2.3 三类博弈关系的回报约束

根据智能体间回报函数的关系，VS-BENCH 覆盖了三种博弈类型（Section 2.2），其数学条件如下：

- **合作博弈**：所有智能体共享同一回报函数
  $$\mathcal { R } _ { 1 } ( s , a ) = \cdots = \mathcal { R } _ { n } ( s , a )$$

- **竞争博弈（零和）**：回报函数满足零和性质
  $$\sum _ { i = 1 } ^ { n } \mathcal { R } _ { i } ( s , a ) = 0$$

- **混合动机博弈**：回报既不相同也不为零和
  $$\mathcal { R } _ { i } ( s , a ) \neq \mathcal { R } _ { j } ( s , a ) \text { 且 } \sum _ { i = 1 } ^ { n } \mathcal { R } _ { i } ( s , a ) \neq 0$$

这三类约束直接决定了智能体的最优策略形态——从合作中的协调均衡，到竞争中的极小化极大策略，再到混合动机中的纳什均衡选择。VS-BENCH 通过覆盖全部三类关系，系统性地暴露 VLMs 在不同博弈结构下的策略推理短板。

### 2.4 三维度评估模块

基于上述形式化框架，VS-BENCH 设计了三个递进式评估模块，分别测量 VLMs 在感知、推理与决策层面的能力（Section 3）：

1. **感知评估模块**（Section 3.1）：测量 VLM 对视觉观察中基本元素的识别准确率，作为策略推理的下限保障。
2. **策略推理评估模块**（Section 3.2）：测量 VLM 对其他智能体下一步行动的预测准确率，直接考察意图理解与对手建模能力。
3. **决策评估模块**（Section 3.3）：测量 VLM 在完整回合中的归一化累积回报，综合评估长期规划与均衡选择能力。

三个模块形成从“看到”到“想到”再到“做到”的递进诊断链路，使研究者能够精确定位 VLMs 在多智能体场景中的能力断裂点。



## 实验与关键发现

### 评估设置

VS-BENCH 在十种视觉多智能体环境中对十五款前沿 VLM 进行了系统性评估，覆盖合作、竞争与混合动机三类博弈关系（Table 1）。评估沿三个维度展开：**感知**（元素识别准确率）、**策略推理**（对其他智能体下一步行动的多选题预测准确率）和**决策**（归一化回合回报）。所有模型统一使用 temperature=1.0、最大输出 tokens 8k（推理模型额外 tokens 上限 16k），对手策略由脚本或离线专家生成以保证可比性。随机智能体（Random Agent）作为决策下界，Oracle Agent（基于规则或专家策略）作为上界。

![[assets/figures/papers/paper_list_l2050_https_arxiv_org_abs_2506_02387/figures/003_Table_1.jpg]]
*Table 1: Taxonomy and required abilities of the ten multi-agent environments in VS-BENCH*

### 感知：VLM 基础视觉能力较强

Table 2 报告了各模型在十种环境中的元素识别准确率。所有模型整体准确率均不低于 67.8%，最佳模型 **o3** 达到 84.9%，仅比 Oracle（100%）低 15.1 个百分点。排名靠前的还包括 **gemini-2.5 w/o thinking**（84.5%）和 **gemini-2.5-pro**（83.4%），表明当前 VLMs 在多智能体场景下的基础视觉感知能力已较为成熟。这一结果为后续策略推理与决策评估提供了可靠的感知基线——模型确实“看到了”环境中的关键元素。

![[assets/figures/papers/paper_list_l2050_https_arxiv_org_abs_2506_02387/figures/004_Table_2.jpg]]
*Table 2: Perception evaluation results. For each environment, the first , second , and third best results are highlighted in green*

### 策略推理：从感知到意图预测的巨大落差

Table 3 揭示了核心瓶颈。当任务从“识别元素”转向“预测其他智能体下一步行动”时，模型表现急剧下降：最佳模型 **o3** 的整体策略推理准确率仅为 **46.6%**，较 Oracle（100%）低 53.4 个百分点。o3 在十种环境中的六种排名第一，但绝对水平仍远未达到可靠推理的标准。多款模型在部分环境中甚至低于随机基线（Table 3 红色标注），说明在非平稳多智能体动态下，现有 VLMs 的意图建模与对手策略预测能力严重不足。视觉复杂性进一步加剧了这一困难——多模态输入下的推理准确率系统性低于纯文本条件。

![[assets/figures/papers/paper_list_l2050_https_arxiv_org_abs_2506_02387/figures/005_Table_3.jpg]]
*Table 3: Strategic reasoning evaluation results. For each environment, the first , second , and third best results are highlighted in green, while the results below random are highlighted in red*

### 决策：长期规划与均衡选择是主要鸿沟

Table 4 的决策结果最为严峻。最佳模型 **o3** 的平均归一化回报仅为 **31.4**（Oracle = 100，Random = 0），且 **15 款模型中有 4 款整体表现低于随机智能体**（claude-3-7 w/o thinking: -0.6; doubao-1-5-vision-pro: -0.9; grok-2-vision: -6.7; Llama-3.2-90B-Vision-Ins.: -6.3）。这意味着部分 VLMs 在多智能体环境中的决策不仅无益，反而有害。o3 虽在多数环境中领先，但其归一化回报仅超过 12.9% 的人类被试（Figure 6），而人类平均归一化回报高达 62.7（Table 10）。感知→推理→决策的链条中，决策环节的退化最为剧烈，表明将感知信息转化为多步策略优化和博弈均衡选择是当前 VLMs 面临的最大挑战。

![[assets/figures/papers/paper_list_l2050_https_arxiv_org_abs_2506_02387/figures/006_Table_4.jpg]]
*Table 4: Decision-making evaluation results. For each environment, the first , second , and third best results are highlighted in green, while the results below or equal to random are in red*

![[assets/figures/papers/paper_list_l2050_https_arxiv_org_abs_2506_02387/figures/010_Figure_6.jpg]]
*Figure 6: Decision-making results of human participants*

![[assets/figures/papers/paper_list_l2050_https_arxiv_org_abs_2506_02387/figures/030_Table_10.jpg]]
*Table 10: Decision-making results for the human baseline. For comparison, we also report the performance of the best reasoning, chat, and open-source models. All values are normalized scores. For each environment, the best result is highlighted in green*

### 模态影响：视觉输入加剧决策困难

Figure 3 对比了推理 VLMs 在多模态与纯文本观察下的决策表现。纯文本条件下模型整体表现略优，但两种设置均远低于 Oracle。视觉模态引入的额外复杂性并非源于感知失败（感知准确率已达 84.9%），而更可能在于视觉信息增加了策略推理的搜索空间与噪声，模型难以从丰富但冗余的视觉观察中提取博弈论关键信息。

![[assets/figures/papers/paper_list_l2050_https_arxiv_org_abs_2506_02387/figures/007_Figure_3.jpg]]
*Figure 3: Comparison of reasoning VLMs on decision-making with multimodal and text-only observations. The solid and dashed vertical lines represent the average results of two settings*

### 推理增强：Chain-of-Thought 提示的收益与上限

Figure 4 展示了 IO（直接输出）与 CoT（思维链）提示下推理模型和聊天模型的决策对比。CoT 提示显著提升了聊天模型在三种环境中的决策性能，但推理模型仍保持最佳。这一结果表明：① 显式推理过程确实有助于多智能体策略决策；② 但即便最强的推理模型（o3），其决策水平仍远未达到稳健的博弈论最优。Table 7 和 Table 8 分别给出了多模态输入配合 CoT 提示下的策略推理与决策详细结果，进一步印证了上述趋势。

![[assets/figures/papers/paper_list_l2050_https_arxiv_org_abs_2506_02387/figures/008_Figure_4.jpg]]
*Figure 4: Comparison of reasoning VLMs and chat VLMs on decision-making with IO and CoT prompting. The solid, dashed, and dotted vertical lines represent the average results of three settings*

![[assets/figures/papers/paper_list_l2050_https_arxiv_org_abs_2506_02387/figures/025_Table_7.jpg]]
*Table 7: Strategic reasoning results on multimodal input and CoT prompting*

### Persona 操控：社交意识可调节但非鲁棒

Section 4.3 和 Figure 5 考察了通过设定自利或合作 persona 对模型在社交困境游戏中行为的影响。o3 在不同 persona 下的行为模式发生显著变化，合作 persona 下更倾向于互惠行为，自利 persona 下则更频繁背叛。Table 9 给出了三种推理模型在 Coin Dilemma 等游戏中的原始得分变化。然而，这种操控并非鲁棒——模型的行为偏移方向虽符合预期，但幅度和一致性有限，且开源模型的表现更不稳定。这表明当前 VLMs 具备一定的社交意识，但距离可控、可信的角色引导仍有差距。

![[assets/figures/papers/paper_list_l2050_https_arxiv_org_abs_2506_02387/figures/009_Figure_5.jpg]]
*Figure 5: Social behaviors of o3 with different personas and the best-performing open-source model in each social dilemma game. Dimensions are agents’ behaviors described in Appendix J*

![[assets/figures/papers/paper_list_l2050_https_arxiv_org_abs_2506_02387/figures/029_Table_9.jpg]]
*Table 9: Raw decision-making results under different personas in three mixed-motive games across three reasoning models*

### 失败模式总结

综合以上结果，现有 VLMs 在 VS-BENCH 上的失败可归纳为三个层次：

1. **意图预测失败**：在非平稳多智能体动态中，模型无法准确建模对手策略，策略推理准确率不足 50%。
2. **长期规划崩溃**：即使感知正确、短期推理部分有效，模型仍无法将其转化为累积回报最大化的多步决策序列，多款模型表现劣于随机。
3. **视觉-策略耦合障碍**：多模态视觉输入虽未导致感知失败，却系统性地恶化了策略推理与决策质量，提示模态间的信息转化存在深层瓶颈。

这些失败模式共同指向一个核心问题：当前 VLMs 缺乏将多模态感知高效转化为博弈论策略推理与长期规划的结构化机制。



## 定位与知识库关联

**VS-BENCH** 是首个面向视觉语言模型（VLM）在多智能体环境中策略能力的多模态基准。其核心定位并非提出新的模型架构或训练范式，而是构建一个标准化评估框架，以诊断当前 VLMs 在从感知到策略推理再到长期决策这一完整链条上的能力瓶颈。该基准在评估协议上参照了部分可观察马尔可夫博弈（POMG）的形式化框架，将多智能体交互建模为：

$$\mathcal { G } = ( \mathcal { N } , S , \{ \mathcal { A } _ { i } \} _ { i \in \mathcal { N } } , \{ \mathcal { O } _ { i } \} _ { i \in \mathcal { N } } , \mathcal { P } , \{ \mathcal { R } _ { i } \} _ { i \in \mathcal { N } } , \gamma )$$

其中每个智能体 $i$ 的目标是最大化期望折扣累积回报 $\mathbb { E } _ { \pi _ { 1 } , \cdots , \pi _ { n } } \left[ \sum _ { t } \gamma ^ { t } r _ { i , t } \right]$。VS-BENCH 在此框架下为 VLM 智能体定义了多模态观察空间和文本动作空间，并通过映射函数将文本动作转换回原始动作空间。

### 与现有基准的关系与差异

VS-BENCH 的知识库定位处于**多模态基准**、**博弈论评估**和**智能体决策**三个领域的交叉地带。与现有工作相比，其核心区分度体现在：

1. **相对于纯文本多智能体基准**：现有博弈论推理评估（如基于矩阵博弈或纯文本社交困境的测试）未纳入视觉观察。VS-BENCH 首次将评估扩展至视觉基础环境，涵盖合作（如 Overcooked、Hanabi）、竞争（如 Breakthrough、Poker）和混合动机（如 Coin Dilemma、Hunt、Battle）三类博弈结构。Table 1 系统梳理了十种环境对策略推理、长期规划、合作与竞争等能力的需求矩阵。

2. **相对于通用 VLM 基准**：主流 VLM 评估（如 MMBench、MMMU）侧重于单智能体场景下的视觉理解与问答，不涉及多智能体交互中的非平稳动态、对手建模和均衡选择。VS-BENCH 的三维评估体系（感知→策略推理→决策）直接揭示了 VLMs 在感知层表现尚可（最佳模型 o3 达 84.9% 准确率，Table 2）但策略推理层骤降至 46.6%（Table 3）、决策层归一化回报仅 31.4（Table 4）的能力断层。

3. **相对于强化学习基准**：传统多智能体强化学习（MARL）基准（如 MPE、SMAC）评估的是通过训练获得的策略网络，而 VS-BENCH 评估的是冻结的预训练 VLM 的零样本/少样本策略能力，不涉及环境交互训练。

### 基线设定的合理性边界

VS-BENCH 采用 **Random Agent** 作为随机下界和 **Oracle Agent**（基于规则或专家策略）作为最优上界的双基线设计。这一设定清晰锚定了 VLM 能力的相对位置，但存在以下边界条件：

- **Oracle 的可用性限制**：Oracle 策略依赖于已知的环境动态和对手模型，在真实开放场景中不可获得。因此 Oracle 与 VLM 之间的差距（如决策维度差距达 68.6 个归一化点）应被理解为“已知最优解下的能力缺口”，而非“可达到的性能上限”。
- **对手策略的静态性**：当前评估中对手以脚本或离线专家策略为主，无法模拟在线自适应交互。这意味着 VLM 的评估结果反映的是其对固定策略的应对能力，而非在动态博弈中的鲁棒性。论文在局限中也明确指出这一点。

### 方法适用边界与局限

1. **智能体数量的可扩展性未充分验证**：当前评估主要聚焦于双智能体场景，仅在附录中初步测试了三玩家场景。对于更大规模的多智能体系统（如群体博弈、联盟形成），VLMs 的策略能力是否持续衰减尚不明确。

2. **视觉复杂性与策略推理的干扰机制未解耦**：消融实验（Figure 3）表明纯文本输入下决策表现略优于多模态，但二者均远低于 Oracle。这一发现暗示视觉信息本身可能引入噪声，但其具体干扰路径（是视觉编码失真还是多模态融合瓶颈）尚未被系统分析。

3. **Persona 引导的可控性有限**：通过设定自利或合作 persona 可显著改变模型在社交困境中的行为与收益（Figure 5, Table 9），但 persona 对策略一致性的影响缺乏定量约束——同一 persona 下的模型行为仍可能在不同回合间漂移。

### 开放问题

基于以上分析，该基准揭示的关键开放问题包括：

- 如何在保持强大感知能力的同时，将多模态信息高效转化为多步策略推理与长期规划？
- 多模态视觉输入对策略推理的具体干扰机制是什么？能否通过模态分离或中间表征优化？
- 当前的固定评估协议（自对弈、固定对手）是否足以反映真实世界交互，是否需要引入自适应对手？
- VLMs 的社交意识（persona）如何定量影响合作-竞争均衡，如何设计更可控的角色引导？
- 能否将推理时的计算资源（test-time compute）更结构化地注入博弈论推理，以逼近专家级策略？



## 原文 PDF

![[paperPDFs/CVPR_2026/VS_Bench_Evaluating_VLMs_for_Strategic_Abilities_in_Multi_Agent_Environments.pdf]]
