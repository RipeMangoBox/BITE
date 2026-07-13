---
title: "Shoot First, Ask Questions Later? Building Rational Agents that Explore and Act Like People"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Shoot_First_Ask_Questions_Later_Building_Rational_Agents_that_Explore_and_Act_Like_People.pdf
project_link: https://gabegrand.github.io/battleship
code_link: null
openreview_forum_id: EQhUvWH78U
aliases:
- BQ
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "是否在推理时引入基于贝叶斯实验设计（BED）的策略——包括最大化期望信息增益的问题选择（Bayes-Q）、最大化命中概率的移动选择（Bayes-M）以及基于单步前瞻的探索/利用决策（Bayes-D）。这一开关显著提升了模型性能。"
primary_logic: "将语言模型与贝叶斯推理技术（如序列蒙特卡洛近似和期望信息增益最大化）在推理时相结合，可以构建出具有理性信息寻求能力的智能体，即使较弱的基础模型也能以极低成本实现超人表现。"
claims:
- "添加Bayes-QMD后，Llama-4-Scout的F1从0.367提升至0.764（+0.397），GPT-4o从0.450提升至0.782（+0.332）"
- "Bayes-QMD使Llama-4-Scout对人类的胜率达82%，对GPT-5的胜率达67%，成本仅为GPT-5的约1%"
- "Bayes-Q将冗余问题比例从18.5%降至0.2%（Llama-4-Scout），EIG提升达0.227 bit/问题，达到理论上限的94.2%"
- "代码生成（CoT+Code）将SpotterQA准确率平均提升14.7个百分点，Claude 4 Opus从86.8%提升至94.4%"
---

# Shoot First, Ask Questions Later? Building Rational Agents that Explore and Act Like People

> [!tip] 核心洞察
> 将语言模型与贝叶斯推理技术（如序列蒙特卡洛近似和期望信息增益最大化）在推理时相结合，可以构建出具有理性信息寻求能力的智能体，即使较弱的基础模型也能以极低成本实现超人表现。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 先射击，后提问？构建像人类一样探索和行动的理性智能体 |
| 英文题名 | Shoot First, Ask Questions Later? Building Rational Agents that Explore and Act Like People |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=EQhUvWH78U) · [Project](https://gabegrand.github.io/battleship) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | Bayes-QMD（基于贝叶斯实验设计的推理时策略组合） |
| Dataset | CaptainQA (54 games, Llama-4-Scout), GPT-4o), GPT-5), CaptainQA (Llama-4-Scout vs GPT-5) |

> [!tip] 效果简介
> - CaptainQA (54 games, Llama-4-Scout) 上，F1 为 0.764 (+Bayes-QMD)，对比 0.367 (LM)，变化 +0.397。
> - CaptainQA (54 games, GPT-4o) 上，F1 为 0.782 (+Bayes-QMD)，对比 0.450 (LM)，变化 +0.332。
> - CaptainQA (54 games, GPT-5) 上，F1 为 0.722 (+Bayes-QM)，对比 0.716 (LM)，变化 +0.006。

## 概要

当前语言模型在需要主动寻求信息的交互式任务中存在根本性缺陷：它们产生大量信息量为零的冗余问题，无法有效平衡探索与利用，且在复杂上下文依赖问题上的回答准确性显著下降。核心瓶颈在于模型缺乏将信息理性地转化为行动的结构化推理能力。

本文提出 **Bayes-QMD**，一套基于贝叶斯实验设计（BED）的推理时策略组合，在不修改模型参数的前提下赋予语言模型理性信息寻求能力。该框架包含三个关键策略：

- **Bayes-Q**：从语言模型采样的候选问题集中，选择期望信息增益（EIG）最大的问题，消除冗余提问。
- **Bayes-M**：基于粒子滤波维护的后验信念，计算每个未揭示格子的命中概率，选择最大概率格子进行射击。
- **Bayes-D**：通过单步前瞻比较当前命中概率与提问后的期望命中概率，显式决定提问还是行动。

在观察员端，将自然语言问题转化为可执行 Python 代码（CoT+Code）显著增强了答案的根基性，平均提升准确率 14.7 个百分点。

**决定性证据**：

- 在 CaptainQA 基准上，Bayes-QMD 使 Llama-4-Scout 的 F1 从 0.367 跃升至 0.764（+0.397），GPT-4o 从 0.450 升至 0.782（+0.332）。
- 增强后的 Llama-4-Scout 对人类胜率达 82%，对 GPT-5 胜率达 67%，而成本仅为 GPT-5 的约 1%。
- 冗余问题比例从 18.5% 降至 0.2%，EIG 提升至理论上限的 94.2%。
- 方法在 Guess Who? 上成功泛化：GPT-4o 成功率从 0.617 升至 0.900，Llama-4-Scout 从 0.300 升至 0.724。

这些结果表明，将语言模型与贝叶斯推理在推理时结合，可使较弱的基础模型以极低成本实现超人表现，为构建具有理性信息寻求能力的智能体提供了可行路径。

语言模型（LM）在标准问答基准上已取得显著进步，但当任务需要**主动、序列化地寻求信息**时，它们暴露出一个根本性缺陷：缺乏理性决策能力。本文聚焦于一类被称为“信息寻求任务”的交互场景——智能体必须在不确定环境中自主判断何时收集信息、何时采取行动，以及如何将获取的信息有效转化为正确决策。

### 问题场景：协同战舰游戏

作者设计了一个名为 **Collaborative Battleship** 的双人协作游戏作为研究平台（Fig. 1）。游戏中有两个角色：

- **船长（Captain）**：只能看到部分揭示的棋盘，需要决定是提问获取信息，还是直接射击目标格子。船长必须在有限的移动次数（40次）和提问次数（15次）内，最大化命中船上格子的精度与召回率。
- **观察员（Spotter）**：能看到完整棋盘，但只能对船长的问题回答“Yes”或“No”。

这一设定将信息寻求的核心挑战具象化：船长面临**探索与利用的经典权衡**——是花一个回合提问以降低不确定性，还是利用已有信息直接行动。

### 现有方法的缺口

人类玩家在游戏中表现出色：提问次数与最终F1分数呈正相关（ρ=0.684, Fig. 2a），且人类能自然地在游戏早期集中提问、后期转为行动（Fig. 2b）。然而，当前语言模型在扮演船长时存在三个关键瓶颈：

1. **提问质量低下**：语言模型倾向于提出大量冗余问题——这些问题在给定当前信念下信息量为零。例如，纯语言模型船长（Llama-4-Scout）的问题中有18.5%不产生任何信息增益，而人类的冗余问题比例远低于此。

2. **信息-行动转化失败**：即使模型获得了有用信息，它也难以将信息精确地转化为有效的移动决策。纯语言模型的移动选择接近随机水平，说明语言模型缺乏将概率性信念映射到具体行动的能力。

3. **上下文依赖问题的退化**：在SpotterQA评估中，当问题需要结合对话历史进行复杂推理时，语言模型的准确率显著下降，而人类准确率保持稳定（Fig. 3c）。

### 核心动机与思路

上述瓶颈指向一个深层问题：**语言模型在推理时缺乏结构化的理性推理机制**。它们隐式地进行信息评估和决策，而非显式地维护信念状态并据此优化行为。

本文的核心洞察是：将**贝叶斯实验设计（Bayesian Experimental Design, BED）**与语言模型在推理时相结合，可以赋予智能体理性信息寻求的能力。具体而言，通过序列蒙特卡洛（SMC）粒子滤波维护对隐藏棋盘状态的后验信念，并基于此信念进行三类理性决策：

- **Bayes-Q**：选择最大化期望信息增益（EIG）的问题，而非直接从语言模型采样；
- **Bayes-M**：基于当前信念计算每个格子的命中概率，选择最大概率格子射击；
- **Bayes-D**：通过单步前瞻比较当前命中概率与提问后的期望命中概率，决定是否继续提问。

这一方法的关键优势在于：**它不依赖语言模型自身的隐式推理能力，而是为模型提供了一套外部化的、数学上可证明最优的决策框架**。即使基础模型较弱，也能以极低成本实现超人表现——例如，配备Bayes-QMD的Llama-4-Scout对GPT-5的胜率达67%，而成本仅为后者的约1%。

## 核心方法与创新机理

本文的核心创新在于将**贝叶斯实验设计（BED）**的理性推理框架与语言模型在推理时相结合，构建出能够像人类一样高效探索与行动的智能体。这一框架通过三个互补的策略模块——**Bayes-Q**（理性提问）、**Bayes-M**（理性行动）和**Bayes-D**（理性决策）——系统性地弥补了纯语言模型在信息寻求任务中的结构性缺陷。

### 问题瓶颈：语言模型为何失败？

纯语言模型在协同信息寻求任务中暴露了三重能力断层：

1. **提问质量低下**：语言模型产生大量冗余问题（如 Llama-4-Scout 的冗余问题比例高达 18.5%），这些问题的期望信息增益（EIG）为零，无法有效缩小假设空间。
2. **信息-行动转化失败**：即使获得了高质量信息，语言模型也难以将其精确转化为有效行动——Llama-4-Scout 的纯语言模型 F1 仅为 0.367，接近随机水平。
3. **探索/利用失衡**：语言模型无法理性判断何时应继续提问收集信息、何时应停止探索并执行行动。

### 关键创新：三个贝叶斯策略模块

针对上述断层，本文提出三个推理时可插拔的策略模块（Table 1），每个模块对应一个核心决策槽位：

**Bayes-Q：最大化期望信息增益的提问策略**（Eq. 5）
纯语言模型直接从生成分布中采样问题，而 Bayes-Q 先让语言模型生成候选问题集 $\mathcal{Q}$，再基于当前粒子信念 $\pi_t$ 计算每个候选问题的期望信息增益 $\mathrm{EIG}_{\varepsilon}(q \mid x, \mathcal{H}_{1:t})$，选择信息量最大的问题。EIG 的计算利用了对称二元信道（BSC）假设下的闭合形式（Eq. 4），无需额外模型调用。这一策略将冗余问题比例从 18.5% 降至 0.2%，EIG 提升 0.227 bit/问题，达到理论上限的 94.2%（Fig. 4b, Table 4）。

**Bayes-M：基于后验信念的命中概率最大化移动**（Eq. 6）
纯语言模型直接预测目标格子，而 Bayes-M 利用序列蒙特卡洛（SMC）粒子滤波维护的信念分布 $\pi_t$，显式计算每个未揭示格子的命中概率 $p_t^{\mathrm{hit}}(u \mid x, \mathcal{H}_{1:t})$，选择最大概率格子射击。这一策略将语言模型从“猜测”转化为“推理”，是 F1 提升的最大单一贡献者（Llama-4-Scout: +0.318; GPT-4o: +0.277，Table 4）。

**Bayes-D：基于单步前瞻的探索/利用决策**（Eq. 7）
纯语言模型隐式决定提问或射击，而 Bayes-D 通过比较当前命中概率与提问后的期望命中概率 $\widehat{p_{t+1}^{\mathrm{hit}}}$，理性判断是否值得花费一个回合提问。若当前命中概率已超过提问后期望命中概率的 $\gamma$ 倍（$\gamma=0.95$），则直接射击；否则继续提问。这一策略使提问时序分布更接近人类和 GPT-5 的行为模式（Fig. 4c），并在 Bayes-QM 基础上进一步优化 F1。

### 观察员侧的互补创新：代码生成增强答案推理

在观察员角色中，本文发现将自然语言问题转化为可执行 Python 代码（Code，或结合思维链的 CoT+Code）能显著提升答案准确性。这一策略的关键在于：代码执行强制模型将模糊的自然语言问题“落地”为精确的形式化推理，从而减少幻觉和上下文误解。在 SpotterQA 基准上，CoT+Code 使 15 个模型的准确率平均提升 14.7 个百分点，其中 Claude 4 Opus 从 86.8% 提升至 94.4%（Fig. 3b）。

### 创新的本质：推理时嫁接而非训练时改造

值得强调的是，上述所有策略均在**推理时**运行，无需微调或强化学习。Bayes-QMD 仅依赖语言模型生成候选问题、SMC 粒子滤波维护信念、以及基于闭合形式 EIG 的快速计算——这些模块的计算开销极低，使得 Llama-4-Scout + Bayes-QMD 以 GPT-5 约 1% 的成本实现了对其 67% 的胜率（Table 5）。这一“弱模型 + 理性推理 > 强模型”的范式，揭示了当前语言模型在结构化推理能力上的根本性短板，以及通过显式推理框架弥补这一短板的巨大潜力。

本文提出了一套推理时策略框架，将语言模型与贝叶斯实验设计（Bayesian Experimental Design, BED）相结合，使智能体能够在信息寻求任务中做出理性决策。该框架围绕一个协作式战舰游戏构建，包含两个不对称角色：**船长（Captain）** 仅能看到部分棋盘，负责决定何时提问、何时射击；**观察员（Spotter）** 能看到完整棋盘，但只能以 Yes/No 形式回答船长的问题（Figure 1）。

### 核心模块与管线

整个智能体系统由以下模块串联构成，形成“感知-推理-决策-执行”的闭环：

1. **语言模型问题生成器**：船长根据当前可见棋盘 $x$ 和历史对话 $\mathcal{H}_{1:t}$，通过语言模型采样生成候选自然语言问题集 $\mathcal{Q}$（§4.3）。该模块不直接输出最终问题，而是提供一个候选池供后续理性筛选。

2. **SMC信念维护器**：使用序列蒙特卡洛（Sequential Monte Carlo）粒子滤波近似后验信念 $\pi_t(s)$，即对隐藏棋盘状态 $s$ 的概率分布。每轮收到观察员的答案后，通过贝叶斯更新重新加权粒子：
   $$\pi_{t+1}(s) \propto \pi_t(s) \Big[ (1 - \varepsilon) \mathbf{1}\{\tilde{a}_t = f_{q_t}(s)\} + \varepsilon \mathbf{1}\{\tilde{a}_t \ne f_{q_t}(s)\} \Big]$$
   其中 $\varepsilon$ 为噪声参数（固定为 0.1），将观察员建模为翻转概率为 $\varepsilon$ 的二元对称信道 BSC($\varepsilon$)。该模块是后续所有理性决策的概率基础。

3. **期望信息增益（EIG）计算模块**：对每个候选问题 $q$，基于当前粒子信念计算其期望信息增益：
   $$\mathrm{EIG}_{\varepsilon}(q_t \mid x, \mathcal{H}_{1:t}) := I(S; \widetilde{A}_t \mid x, \mathcal{H}_{1:t})$$
   在 BSC 信道假设下，EIG 具有闭合形式：
   $$\mathrm{EIG}_{\varepsilon}(q_t \mid x, \mathcal{H}_{1:t}) = \mathrm{H}_b(\varepsilon + (1 - 2\varepsilon)p_t) - \mathrm{H}_b(\varepsilon)$$
   其中 $p_t$ 为问题答案为“Yes”的预测概率，$\mathrm{H}_b$ 为二元熵函数。此模块量化每个问题的信息价值，是 **Bayes-Q** 策略的核心。

4. **命中概率估计器**：根据当前信念 $\pi_t$ 计算每个未揭示格子 $u$ 含有船只的概率：
   $$p_t^{\mathrm{hit}}(u \mid x, \mathcal{H}_{1:t}) := \sum_{s \in \mathcal{S}_{\vdash x}} \pi_t(s) \mathbf{1}\{u \text{ contains ship in } s\}$$
   该模块为 **Bayes-M** 移动策略提供决策依据。

5. **单步前瞻决策模块**：比较当前最大命中概率与提问后的期望命中概率，决定执行提问还是射击（**Bayes-D**）。其核心是计算提问后的期望命中概率：
   $$\widehat{p_{t+1}^{\mathrm{hit}}}(u \mid x, \mathcal{H}_{1:t}, q_t) := \sum_{\tilde{a} \in \{0,1\}} \Pr(\widetilde{A}_t = \tilde{a} \mid x, \mathcal{H}_{1:t}, q) \, p_{t+1}^{\mathrm{hit}}(u \mid x, \mathcal{H}_{1:t}, \tilde{a})$$
   若当前命中概率超过折扣后的期望命中概率（折扣因子 $\gamma=0.95$），则立即射击；否则先提问。

6. **Python代码生成器（观察员）**：将船长的自然语言问题转化为可执行的 Python 程序，通过代码推理棋盘状态并输出 Yes/No 答案。该模块可单独使用（Code），也可与思维链结合（CoT+Code），显著提升了回答的准确性——在 15 个模型的 SpotterQA 评估中，CoT+Code 平均提升 14.7 个百分点（Fig. 3b）。

7. **游戏模拟与数据采集**：管理游戏状态、执行移动/射击动作、验证答案正确性，并提供反馈。该模块同时用于人类行为实验（42 名参与者）和智能体评估。

### 策略组合与数据流

上述模块按策略组合方式形成不同的船长变体（Table 1）：

- **LM-only**：纯语言模型，直接从 LM 采样问题和移动，隐性决定探索/利用。
- **+Bayes-Q**：在 LM 生成的候选问题中，由 EIG 模块筛选最优问题。
- **+Bayes-M**：由命中概率估计器替代 LM 的移动预测，选择最大命中概率的格子。
- **+Bayes-QM**：同时使用理性提问和理性移动。
- **+Bayes-QMD**：在 +Bayes-QM 基础上加入单步前瞻决策，显式控制提问与射击的时机。

数据流方向为：游戏模拟器提供棋盘状态 → 信念维护器更新后验 → EIG 模块与命中概率估计器并行计算 → 决策模块仲裁提问/射击 → 若提问，问题发送至观察员的代码生成器 → 答案返回信念维护器，形成闭环。所有船长实验固定观察员为 GPT-5 (CoT+Code)，以消除观察员质量差异的干扰。

### 核心洞察

该框架的关键瓶颈在于：**语言模型本身缺乏将信息有效转化为行动的能力**。单独添加 Bayes-Q 虽能提升问题质量（EIG 从 0.266 升至 0.490 bit/问题，冗余问题从 18.5% 降至 0.2%），但对 F1 的提升有限（Llama-4-Scout 仅 +0.021）。真正驱动性能飞跃的是 Bayes-M——通过显式边缘化信念来计算命中概率，Llama-4-Scout 的 F1 跃升 +0.318，GPT-4o 跃升 +0.277（Table 4）。这表明，即使拥有高质量信息，语言模型也难以自主完成从概率推理到精确空间定位的转化，而贝叶斯推理模块恰好填补了这一能力缺口。

### 整体框架：贝叶斯实验设计（BED）视角

本方法将协同战舰游戏中的信息寻求问题形式化为**贝叶斯实验设计（BED）**问题。船长面对部分可观测的棋盘 $x$，需通过提问获取信息，并将信息转化为射击行动。核心挑战在于：语言模型（LM）本身缺乏理性的信息-行动权衡能力——它们会提出大量冗余问题（信息量为零），且难以将获取的信息有效转化为精确的射击决策。

为解决这一问题，作者在推理时引入三个基于贝叶斯推理的策略模块，与语言模型协同工作。这些模块不改变模型参数，而是作为推理时的决策层，在 LM 采样候选问题/行动后，依据概率推理进行筛选和决策。

### 核心模块一：SMC 信念维护器

船长对隐藏棋盘状态 $S$ 的信念通过**序列蒙特卡洛（SMC）粒子滤波**近似维护。具体而言，维护一个候选棋盘集合 $\mathcal{S}_{\vdash x}$（即与可见棋盘 $x$ 一致的所有可能完整棋盘），并对每个候选棋盘 $s$ 赋予权重，形成信念分布 $\pi_t(s)$。

信念更新的核心机制是贝叶斯理想观察者模型：观察员被建模为**二元对称信道（BSC）**，翻转概率为 $\varepsilon$（默认 $\varepsilon = 0.1$）。这意味着观察员的回答有 $1-\varepsilon$ 的概率正确，$\varepsilon$ 的概率错误。给定问题 $q_t$ 和观察到的（可能含噪）答案 $\tilde{a}_t$，信念更新公式为：

$$\pi_{t+1}(s) \propto \pi_t(s) \Big[ (1 - \varepsilon) \mathbf{1}\{\tilde{a}_t = f_{q_t}(s)\} + \varepsilon \mathbf{1}\{\tilde{a}_t \ne f_{q_t}(s)\} \Big]$$

其中 $f_{q_t}(s)$ 表示在真实棋盘 $s$ 下问题 $q_t$ 的正确答案。该公式的含义是：若观察到的答案与候选棋盘一致，则以高概率 $(1-\varepsilon)$ 保留该候选棋盘；若不一致，则以低概率 $\varepsilon$ 保留（允许观察员出错的可能）。通过逐轮重加权，粒子集逐渐收敛到真实棋盘。

### 核心模块二：期望信息增益（EIG）计算模块

**Bayes-Q** 策略的核心是选择能最大化**期望信息增益（EIG）**的问题。EIG 定义为棋盘状态 $S$ 与（可能含噪的）答案 $\widetilde{A}_t$ 之间的互信息：

$$\mathrm{EIG}_{\varepsilon}(q_t \mid x, \mathcal{H}_{1:t}) := I(S; \widetilde{A}_t \mid x, \mathcal{H}_{1:t})$$

直观上，EIG 衡量的是：在给定当前信念和历史的情况下，提出某个问题能期望获得多少关于隐藏棋盘状态的信息（以比特计）。

关键创新在于：在 BSC 假设下，EIG 具有**闭合形式解**，无需蒙特卡洛估计即可高效计算。具体地，令 $p_t := \Pr(A_t = 1 \mid x, \mathcal{H}_{1:t})$ 为问题 $q_t$ 答案为“Yes”的预测概率（通过对粒子信念加权求和得到），则：

$$\mathrm{EIG}_{\varepsilon}(q_t \mid x, \mathcal{H}_{1:t}) = \mathrm{H}_b(\varepsilon + (1 - 2\varepsilon)p_t) - \mathrm{H}_b(\varepsilon)$$

其中 $\mathrm{H}_b(\cdot)$ 为二元熵函数。该公式的直观解释是：EIG 等于“后验不确定性”减去“先验不确定性”（即信道噪声本身的不确定性）。当 $p_t = 0.5$ 时 EIG 最大，因为此时答案最不确定、信息量最高；当 $p_t$ 接近 0 或 1 时 EIG 趋近于 0，因为答案几乎确定，提问无法获得新信息。

给定 $\varepsilon = 0.1$，理论上限 EIG 为 $1 - \mathrm{H}_b(0.1) \approx 0.531$ 比特。

### 核心模块三：命中概率估计器与 Bayes-M

**Bayes-M** 策略基于当前信念 $\pi_t$ 计算每个未揭示格子 $u$ 的命中概率：

$$p_t^{\mathrm{hit}}(u \mid x, \mathcal{H}_{1:t}) := \sum_{s \in \mathcal{S}_{\vdash x}} \pi_t(s) \mathbf{1}\{u \text{ contains ship in } s\}$$

然后选择命中概率最大的格子进行射击：

$$u_t^{\star} \in \arg\max_u p_t^{\mathrm{hit}}(u \mid x, \mathcal{H}_{1:t})$$

这一策略本质上是在当前信念下执行最大后验概率（MAP）决策。其效果显著：单独添加 Bayes-M 使 Llama-4-Scout 的 F1 提升 +0.318，GPT-4o 提升 +0.277（Table 4），表明 LM 自身难以将信息有效转化为精确的空间移动。

### 核心模块四：单步前瞻决策模块与 Bayes-D

**Bayes-D** 策略解决**探索/利用权衡**：船长应在何时停止提问并开始射击？该模块采用**单步前瞻**（one-step lookahead）方法，比较两个量：

- **当前命中概率**：$\max_u p_t^{\mathrm{hit}}(u \mid x, \mathcal{H}_{1:t})$
- **提问后的期望命中概率**：若提出最佳问题 $q_t$ 并收到答案 $\tilde{a}$ 后更新信念，再计算最大命中概率的期望值：

$$\widehat{p_{t+1}^{\mathrm{hit}}}(u \mid x, \mathcal{H}_{1:t}, q_t) := \sum_{\tilde{a} \in \{0,1\}} \Pr(\widetilde{A}_t = \tilde{a} \mid x, \mathcal{H}_{1:t}, q) \, p_{t+1}^{\mathrm{hit}}(u \mid x, \mathcal{H}_{1:t}, \tilde{a})$$

决策规则为：若 $p_t^{\mathrm{hit}} > \gamma \cdot \widehat{p_{t+1}^{\mathrm{hit}}}$（其中 $\gamma = 0.95$ 为折扣因子），则立即射击；否则继续提问。折扣因子 $\gamma < 1$ 编码了对“提问成本”的偏好——只有当提问能带来足够大的命中概率提升时，才值得花费一轮进行提问。

实验表明，Bayes-D 在 Bayes-QM 的基础上进一步优化了提问时序分布，使其更接近人类和 GPT-5 的行为模式（Fig. 4c），并略微提升 F1（Llama-4-Scout: +0.024, GPT-4o: +0.029）。

### 观察员模块：Python 代码生成器

观察员（Spotter）的核心挑战是将自然语言问题转化为准确的 Yes/No 答案。本文发现，**语言到代码的翻译（Code）** 是提升回答准确性的关键。观察员收到问题后，不是直接回答，而是生成 Python 代码来推理完整棋盘状态并输出答案。这一策略在 15 个 LM 上平均提升准确率 14.7 个百分点（CoT+Code），其中 Claude 4 Opus 从 86.8% 提升至 94.4%（Fig. 3b）。

### 模块间的协同机制

各模块并非独立运作，而是形成协同效应。语言模型问题生成器负责从当前棋盘和历史中采样候选自然语言问题；EIG 计算模块对这些候选问题进行筛选；SMC 信念维护器基于收到的答案更新信念；命中概率估计器基于更新后的信念指导射击；单步前瞻决策模块决定何时停止提问。消融实验（Table 4）揭示了关键因果链条：

1. **仅加 Bayes-Q**（高质量提问）对 F1 提升有限（Llama-4-Scout: +0.021），因为 LM 无法有效利用获取的信息。
2. **仅加 Bayes-M**（贝叶斯移动）大幅提升 F1（+0.318），说明信息到行动的转化是核心瓶颈。
3. **组合 Bayes-QM** 产生协同增益（+0.373），高质量提问为贝叶斯移动提供了更精确的信念。
4. **完整 Bayes-QMD** 达到最优（+0.397），进一步优化了探索/利用的时序分配。

## 实验与关键发现

### 核心发现：贝叶斯策略使弱模型实现超人表现

在CaptainQA基准上，引入Bayes-QMD策略组合后，较弱的基础模型性能出现跃升。Llama-4-Scout的F1从0.367提升至0.764（+0.397），GPT-4o从0.450提升至0.782（+0.332）（Table 4）。这一提升使这些模型在对阵人类时取得82%的胜率，对阵GPT-5时取得67%的胜率，而纯LM基线对阵GPT-5的胜率为0%（Fig. 4a）。值得注意的是，Llama-4-Scout搭配Bayes-QMD的总API成本约8美元，而GPT-5基线成本约700美元（Table 5），实现了以约1%成本超越昂贵模型的效率。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_EQhUvWH78U/figures/026_Table_4.jpg]]
*Table 4: CaptainQA: Overall results. F1 Score (Targeting Score) is the harmonic mean of Precision and Recall over the board as a binary classification task. Moves (out of 40) and Questions (out of 15) count the total number of moves and questions asked, respectively. EIG ( $\varepsilon$ = 1 . 0 ) measures the average expected information gain of questions asked, with ceiling value ≈ 0.531. Redundant Qs is the fraction of questions yield no information gain (i.e., EIGε(q) = 0)*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_EQhUvWH78U/figures/029_Table_5.jpg]]
*Table 5: Token usage and dollar cost of agents on the CaptainQA benchmark. We report totals summed across all 54 games for each Captain. Note the difference in pricing across LMs spanning two orders of magnitude: while Llama-4-Scout costs approx. 8 USD total across all experiments, GPT-5 costs approx. 900 USD*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_EQhUvWH78U/figures/008_Figure_4.jpg]]
*Figure 4: CaptainQA key results. (a) Incorporating Bayesian strategies for questions ( $Q _ { \mathrm { B a y e s } }$ ) , moves ( $M _ { \mathrm { B a y e s } }$ ) , and decisions ( $D _ { \mathrm { B a y e s } }$ ) brings weaker LMs from near-random performance to super-human levels. (b) Sampling up to 10 questions with $Q _ { \mathrm { B a y e s } }$ yields higher EIG. (c) $D _ { \mathrm { B a y e s } }$ helps Llama-4-Scout and GPT-4o to spread out questions over time, more closely matching the behavior of humans and GPT-5

在SpotterQA上，代码生成策略（CoT+Code）在15个模型上平均提升准确率14.7个百分点（Fig. 3b）。最强模型Claude 4 Opus从86.8%提升至94.4%，o3、o4-mini和GPT-5达到或超过人类92.5%的准确率水平。然而，所有模型在复杂上下文依赖问题上均出现显著退化：GPT-4o从72.8%（简单）降至60.4%（复杂），Llama-4-Scout从68.0%降至54.0%，而人类准确率保持稳定（92.8% vs 91.9%）（Fig. 3c）。

方法在Guess Who?游戏上展现出泛化能力：GPT-4o成功率从0.617升至0.900（+0.283），Llama-4-Scout从0.300升至0.724（+0.424）（Table 9），验证了贝叶斯推理策略不限于战舰场景。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_EQhUvWH78U/figures/033_Table_9.jpg]]
*Table 9: Guess Who? QA: aggregated success rates and breakdown by model and strategy*

### 消融实验：各组件的贡献与协同

**Bayes-Q的独立效应**。单独添加Bayes-Q问题选择策略时，Llama-4-Scout的F1仅提升0.021，GPT-4o提升0.021（Table 4）。尽管Bayes-Q将期望信息增益从0.266 bits提升至0.490 bits（Llama-4-Scout），并将冗余问题比例从18.5%降至0.2%（Table 4），但高质量提问本身不足以转化为更好的行动——语言模型无法有效利用获得的信息进行精确移动。这一发现揭示了信息获取与行动执行之间的关键脱节。

**Bayes-M的核心作用**。Bayes-M移动选择策略单独使用时，Llama-4-Scout的F1提升0.318，GPT-4o提升0.277（Table 4），贡献了总增益的绝大部分。这表明语言模型在将对话历史中的信息转化为精确棋盘坐标时存在根本性困难，而基于粒子信念的命中概率计算直接解决了这一瓶颈。

**Bayes-QM的协同效应**。组合Bayes-Q与Bayes-M时，F1进一步提升至+0.373（Llama-4-Scout）和+0.303（GPT-4o）（Table 4），超过两者单独增益之和。这说明高质量问题与贝叶斯移动之间存在正反馈：更精确的信念状态使EIG最大化的问题选择更有效，而高信息量的问题反过来使信念更新更准确，从而提升移动精度。

**Bayes-D的边际优化**。Bayes-QMD在Bayes-QM基础上加入单步前瞻探索/利用决策，F1达到最终值+0.397（Llama-4-Scout）和+0.332（GPT-4o）（Table 4）。增益虽小，但Bayes-D显著改变了智能体的行为模式：提问时序分布更接近人类和GPT-5，即将问题分散在游戏全程而非集中在前期（Fig. 4c），减少了不必要的移动次数。

**GPT-5的例外**。GPT-5在纯LM条件下F1已达0.716，添加Bayes-QM后仅提升至0.722（+0.006）（Table 4）。这表明GPT-5本身已具备较强的隐式贝叶斯推理能力，外部显式策略的边际收益有限。该结果暗示，随着基础模型能力增强，推理时策略的增益可能递减，但同时也说明弱模型通过推理时策略可以弥合与强模型之间的差距。

### 失败模式分析

**信息到行动的转化失败**。纯LM船长即使提出高质量问题，也无法将答案有效转化为精确移动。Bayes-Q单独添加时EIG提升显著但F1几乎不变（Table 4），说明语言模型在空间推理和信念整合方面存在系统性缺陷。这一失败模式在需要精确坐标输出的任务中尤为突出。

**复杂上下文依赖问题的退化**。在SpotterQA中，所有模型在需要理解对话历史上下文的问题上准确率显著下降（Fig. 3c）。即使最强的o3模型在复杂问题上准确率87.4%，仍低于人类91.9%。这表明当前语言模型在语用推理和上下文消歧方面存在根本性局限，代码生成虽能缓解但无法完全解决。

**固定噪声参数的局限**。方法使用固定的观察员噪声参数ε=0.1，未根据具体人类或AI观察员的可靠性进行动态调整。在人类实验中，不同参与者的回答可靠性存在显著差异（Figs. 14-15），固定参数可能导致信念更新次优。

**单步前瞻的短视**。Bayes-D采用单步前瞻而非全局规划，在需要长序列信息获取的任务中可能表现次优。当前游戏设置中这一局限不显著，但在更复杂的科学发现场景中可能成为瓶颈。

### 关键图表结论

**Table 4** 完整呈现了CaptainQA的主结果。除F1外，关键指标包括：Bayes-QMD将Llama-4-Scout的移动次数从40次（用尽）优化至更合理的分布，EIG从0.266提升至0.490（达到理论上限0.531的92.3%），冗余问题比例从18.5%降至0.2%。

**Fig. 4a** 直观展示了贝叶斯策略的阶梯式增益：从Random/Greedy基线的低F1，到纯LM的中等水平，再到逐步添加Q、M、D后的跃升。图中还标注了人类和GPT-5的F1参考线，清晰显示Bayes-QMD使弱模型超越人类水平。

**Fig. 4b** 揭示了问题采样数量与EIG的缩放关系：采样10个候选问题时EIG接近饱和，验证了Bayes-Q策略在有限采样下的高效性。

**Fig. 18** 的成对胜率热力图显示，Bayes-QMD策略对所有其他策略（包括人类和GPT-5）均取得>0.50的胜率，确认了该策略的一致优越性。

**Table 5** 的成本分析揭示了关键效率洞察：Llama-4-Scout的API成本仅为GPT-5的约1%，但搭配Bayes-QMD后胜率达67%。这一发现表明，在推理时投入计算资源进行贝叶斯推理，比单纯依赖更大规模预训练模型更具成本效益。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_EQhUvWH78U/figures/007_Table_1.jpg]]
*Table 1: In this section, we evaluate the ability of LMs to play the Captain role in the full game setting. We compare a variety of Captain strategies that differ in how they select moves, ask questions, and decide whether to ask or shoot (as formalized in §3.1). A summary is provided in Table 1. Table 1: Summary of Captain strategies. Random and Greedy are move-only baselines; LM is a pure language model, which the Bayes strategies build upon. Triple-dots indicates inheritance from the row above*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_EQhUvWH78U/figures/011_Table_2.jpg]]
*Table 2: shows the distribution of labels in the dataset. Inter-annotator agreement ranged from 94.0– 99.6%; further details are given in Fig. 7a. Table 2: Expert-labeled attributes of human questions. (Questions are multi-label; definitions in §A.3.)*

## 定位与知识库关联

### 与现有基线的定位关系

本文提出的 **Bayes-QMD** 策略组合并非一个独立的新模型，而是一套在推理时（inference-time）叠加于语言模型之上的贝叶斯决策模块。其核心定位是：**将语言模型作为候选动作的生成器，将贝叶斯实验设计（BED）作为动作的筛选器与决策器**。

具体而言，论文构建了以下基线谱系：

- **非学习型船长基准**：Random（随机射击）和 Greedy（最大后验射击）仅执行移动，不提问。它们构成了性能下界，验证了信息寻求的必要性。
- **纯语言模型船长**：Llama-4-Scout、GPT-4o、GPT-5 直接以自然语言生成问题、选择移动并隐式决定探索/利用。这些构成了“标准智能体”基线，其核心瓶颈在于**无法将信息有效转化为行动**（纯LM的F1仅为0.367–0.716）。
- **+Bayes 增量变体**：通过逐步叠加 Bayes-Q（问题选择）、Bayes-M（移动选择）、Bayes-D（探索/利用决策），形成消融链。这一定位方式清晰揭示了每个模块的边际贡献：Bayes-M 是 F1 提升的最大单一来源（Llama-4-Scout +0.318），而 Bayes-Q 的主要贡献在于提升信息效率（EIG +0.224 bit，冗余问题从18.5%降至0.2%），两者组合产生协同增益。

在观察员（Spotter）一侧，基线包括直接回答、思维链（CoT）和代码生成（Code）。Code 策略将自然语言问题转化为可执行 Python 程序，在15个模型的平均准确率上提升14.7个百分点，验证了**将符号推理外化到代码执行环境**是提升接地性（grounding）的有效路径。

### 方法适用边界

Bayes-QMD 的有效性依赖于以下前提条件，这些条件同时划定了其适用边界：

1. **可采样的世界模型**：贝叶斯策略需要从生成式世界模型中高效抽取条件样本 $s \sim p(s \mid x, \mathcal{H})$。在战舰游戏中，世界模型是规则化的棋盘枚举；在 Guess Who? 中，是角色特征的组合空间。当任务缺乏此类显式生成模型时（如开放域科学发现），方法的实用性受限。

2. **固定噪声参数假设**：当前实现使用固定 $\varepsilon = 0.1$ 对观察员的回答噪声进行建模（二元对称信道 BSC($\varepsilon$)）。这意味着方法假设观察员的可靠性是恒定且先验已知的，无法根据具体人类或AI观察员的行为动态推断可靠性。

3. **单步前瞻决策**：Bayes-D 采用单步前瞻（one-step lookahead）比较当前命中概率与提问后的期望命中概率，而非全局最优规划。在需要长序列信息获取的任务中，这种贪心策略可能表现次优。

4. **结构化问答环境**：方法仅在战舰和 Guess Who? 两类结构化游戏中验证。这些环境具有明确的动作空间、二值答案和可枚举的状态空间，向真实世界任务（如交互式科学探索、多轮医疗问诊）的迁移尚未评估。

### 局限与开放问题

**已识别的局限**：

- GPT-5 几乎未从 Bayes-QM 中获益（F1 仅从 0.716 提升至 0.722），表明当基础模型已具备较强的隐式推理能力时，显式贝叶斯模块的边际价值递减。论文推测 GPT-5 可能已在内部近似了类似的信息增益计算，但这一假设缺乏直接证据。
- 在 SpotterQA 的复杂上下文依赖问题上，即使最佳模型（o3 的 87.4%）仍落后于人类（91.9%），说明代码生成虽然提升了接地性，但未能解决语用推理的根本困难。
- 方法未建模观察员的策略性回答行为——真实人类可能根据对船长意图的推断调整回答，而当前框架将观察员视为被动噪声信道。

**开放问题**：

1. **自适应可靠性推断**：如何根据对话历史在线学习或推断观察员的噪声参数 $\varepsilon$？这需要将 $\varepsilon$ 从固定超参数升级为隐变量，并引入元推理机制。论文指出，人类玩家在实验中表现出对信息可靠性的敏感性（Figs. 14–15），但当前智能体缺乏这一能力。

2. **语言模型作为隐式世界模型**：能否绕过显式粒子滤波，直接利用语言模型从前文生成条件样本？这将消除对预定义状态枚举的依赖，使框架适用于更开放的任务，但需要解决语言模型采样的一致性和校准问题。

3. **与规划算法的结合**：如何将 Bayes-QMD 与蒙特卡洛树搜索（MCTS）等更复杂的规划算法结合？单步前瞻可视为深度为1的搜索特例；扩展到多步前瞻有望处理需要长序列信息获取的任务，但需解决信念空间中的搜索效率问题。

4. **语用推理的嵌入**：如何将理性语用推理（Rational Speech Acts, RSA）嵌入 Spotter，使其能推理船长的提问意图并给出更具信息量的回答？这可能缓解当前模型在复杂上下文问题上的性能退化。

5. **动态环境中的在线适应**：在不可预知的真实世界任务中，智能体应如何在线更新世界模型并调整探索策略？当前框架假设世界模型是静态且完全已知的，而真实场景中环境动态变化且部分可观测。

## 原文 PDF

![[paperPDFs/ICLR_2026/Shoot_First_Ask_Questions_Later_Building_Rational_Agents_that_Explore_and_Act_Like_People.pdf]]
