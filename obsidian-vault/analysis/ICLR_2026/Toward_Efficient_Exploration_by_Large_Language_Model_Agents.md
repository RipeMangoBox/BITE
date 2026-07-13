---
title: "Toward Efficient Exploration by Large Language Model Agents"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Toward_Efficient_Exploration_by_Large_Language_Model_Agents.pdf
project_link: null
code_link: null
openreview_forum_id: M3vwnscpL2
aliases:
- LBPSRLLP
- TEEBLLMA
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "将经典贝叶斯强化学习算法——后验采样强化学习（PSRL）——显式地分解为三个由LLM实现的子程序（后验采样、最优策略执行、后验更新），使智能体获得PSRL固有的统计高效探索能力。"
primary_logic: "LLM不仅可以用于隐式地模仿RL算法，还可以作为实现已有高效RL算法的“子程序引擎”；通过将PSRL的各个计算步骤分配给专门的LLM，可以在自然语言任务中复现其探索优势，同时扩展经典算法在非结构化环境中的应用范围。"
claims:
- "在5臂伯努利好赌中，LLM实现的PSRL（κ=1.2）在100步内展现出低于经典汤普森采样的累计遗憾，证明其探索效率优于经典方法。"
- "在RiverSwim（硬探索任务）中，将底层LLM从GPT-4o升级为o1-mini后，LLM-PSRL的遗憾从线性降至与表格型PSRL相当的次线性水平，而Reflexion和ICRL几乎未能有效探索。"
- "在组合锁和Wordle等自然语言MDP任务中，LLM-PSRL显著优于所有LLM基线（Reflexion, ICRL, ICPI），且即使基线下载更强的模型（DeepSeek-R1），也无法超越只使用GPT-4o的LLM-PSRL。"
- "5-Armed Bernoulli Bandit (T=100) 上 Cumulative Regret = LLM-PSRL (κ_sampling=1.2)"
---

# Toward Efficient Exploration by Large Language Model Agents

> [!tip] 核心洞察
> LLM不仅可以用于隐式地模仿RL算法，还可以作为实现已有高效RL算法的“子程序引擎”；通过将PSRL的各个计算步骤分配给专门的LLM，可以在自然语言任务中复现其探索优势，同时扩展经典算法在非结构化环境中的应用范围。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向大型语言模型智能体的高效探索研究 |
| 英文题名 | Toward Efficient Exploration by Large Language Model Agents |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=M3vwnscpL2) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | LLM-based Posterior Sampling for Reinforcement Learning (LLM-PSRL) |
| Dataset | 5-Armed Bernoulli Bandit (T=100), RiverSwim (3 states), Combination Lock (H=3, K=8), Wordle (K=5) |

> [!tip] 效果简介
> - 5-Armed Bernoulli Bandit (T=100) 上，Cumulative Regret 为 LLM-PSRL (κ_sampling=1.2)，对比 Thompson Sampling (classic)，变化 Lower regret。
> - RiverSwim (3 states) 上，Cumulative Regret 为 LLM-PSRL (o1-mini)，对比 Vanilla PSRL (tabular)，变化 Comparable sub-linear regret。
> - Combination Lock (H=3, K=8) 上，Turns to identify unlock code 为 LLM-PSRL (GPT-4o)，对比 ICRL (best baseline)，变化 Fewer turns needed。

## 概要

**核心瓶颈**：当前基于LLM的智能体设计（如Reflexion、ICRL、ICPI）在面对需要高效探索的决策任务时，缺乏结构化的探索机制。这些方法仅依赖LLM的随机性输出或上下文学习进行隐式探索，在稀疏奖励或需要深度探索的环境中表现不佳。

**因果调节变量**：本文提出将经典贝叶斯强化学习算法——后验采样强化学习（PSRL）——显式地分解为三个由LLM实现的子程序：后验采样、最优策略执行、后验更新。这一设计使LLM智能体获得了PSRL固有的统计高效探索能力。

**核心洞察**：LLM不仅可以用于隐式地模仿RL算法，还可以作为实现已有高效RL算法的“子程序引擎”。通过将PSRL的各个计算步骤分配给专门的LLM，可以在自然语言任务中复现其探索优势，同时扩展经典算法在非结构化环境中的应用范围。

**方法定位**：**LLM-PSRL** 是一种显式实现经典RL算法的智能体设计范式，区别于隐式诱导RL算法的现有方法（Figure 1）。其架构包含三个LLM模块：后验采样LLM生成对真实环境的合理假设，最优样本策略LLM根据该假设执行最优动作，后验更新LLM根据完整轨迹更新知识状态与不确定性（Figure 2）。

**主要结果**：
- 在5臂伯努利好赌中，LLM-PSRL展现出低于经典汤普森采样的累计遗憾（Figure 4）。
- 在RiverSwim硬探索任务中，将底层LLM从GPT-4o升级为o1-mini后，遗憾从线性降至与表格型PSRL相当的次线性水平，而Reflexion和ICRL几乎未能有效探索（Figure 6）。
- 在组合锁和Wordle等自然语言MDP任务中，LLM-PSRL显著优于所有LLM基线，且即使基线使用更强的模型（DeepSeek-R1），也无法超越仅使用GPT-4o的LLM-PSRL（Figure 7, Figure 8, Figure 15）。

**局限性**：方法在状态-动作空间较大且转移函数随机性较强的MDP中，LLM的规划能力不足会导致遗憾退化；依赖于手工设计的先验分布；计算成本较高；后验更新LLM存在信息遗忘或错误更新的风险。

### 现有LLM智能体在探索任务中的瓶颈

当前基于大型语言模型（LLM）的智能体设计——包括**Reflexion**（Shinn et al., 2024）、**ICRL**（Monea et al., 2024）和**ICPI**（Brooks et al., 2023）——在面对需要高效探索的决策任务时表现出根本性不足。这些方法的核心缺陷在于缺乏结构化的探索机制：它们要么依赖LLM的随机性进行隐式探索（如ICRL从重播缓冲区随机采样经验作为上下文），要么通过自我反思产生口头指导来改善决策（如Reflexion），要么依赖上下文学习进行贪婪策略迭代（如ICPI）。在稀疏奖励或需要深度探索的环境中，这类隐式探索策略难以有效平衡探索与利用，导致智能体过早收敛到次优行为或完全无法发现高奖励区域。

### 从隐式诱导到显式实现：设计范式的转变

本文提出了一种根本不同的智能体设计原则。如Figure 1所示，现有方法通过编排多个LLM来隐式地诱导某种RL算法（左侧路径），而本文主张将已有的高效RL算法显式地实现，即将其各个计算步骤外包给专门的LLM执行（右侧路径）。这一转变的关键洞见在于：LLM不仅可以用于隐式地模仿RL算法，还可以作为实现已有高效RL算法的“子程序引擎”。

### 为什么选择后验采样强化学习

本文选择后验采样强化学习（Posterior Sampling for Reinforcement Learning, PSRL）作为显式实现的目标算法，原因在于PSRL具有统计上可证明的高效探索特性。PSRL的核心机制是汤普森采样：在每个情节开始时，从当前后验分布中采样一个关于真实MDP的假设，然后执行在该采样MDP下的最优策略，最后根据观测到的轨迹更新后验分布。这种显式的后验采样与按采样MDP最优执行的机制，赋予了PSRL固有的统计高效探索能力——这正是现有LLM智能体所缺失的关键要素。

### 核心贡献

本文的核心贡献在于将PSRL分解为三个由LLM实现的子程序：**后验采样LLM**（根据当前后验生成关于真实MDP的合理假设）、**最优样本策略LLM**（在给定状态下按采样MDP执行最优动作）和**后验更新LLM**（根据完整轨迹更新智能体的知识与不确定性）。通过这种显式实现，LLM-PSRL在自然语言任务中复现了经典PSRL的探索优势，同时扩展了经典算法在非结构化环境中的应用范围。

## 核心方法与创新机理

本文的核心创新在于提出了一种全新的**LLM智能体设计范式**：将经典的高效探索算法——后验采样强化学习（PSRL）——显式地分解为三个由LLM实现的独立子程序，而非像现有方法那样依赖LLM的随机性或上下文学习进行隐式探索。

### 设计范式的根本转变

现有LLM智能体设计（如**Reflexion**（Shinn et al., 2024）、**ICRL**（Monea et al., 2024）、**ICPI**（Brooks et al., 2023））的共同瓶颈在于：它们缺乏结构化的探索机制。这些方法本质上是通过编排LLM来**隐式地诱导**某种RL算法（Figure 1左），探索行为仅依靠LLM的随机采样、自我反思或贪婪策略，难以应对稀疏奖励或需要深度探索的环境。

本文提出的范式（Figure 1右）则从根本上改变了这一思路：**不再让LLM隐式地“涌现”探索行为，而是将PSRL这一具有统计高效探索保证的经典算法的各个计算步骤，显式地外包给专门的LLM执行**。这种设计使LLM成为实现已有高效RL算法的“子程序引擎”，从而在自然语言任务中复现PSRL的探索优势。

### 关键机制变更：从隐式探索到显式后验采样

方法层面的核心变更体现在两个关键维度：

**1. 探索机制的显式化**

| 维度 | 基线方法 | LLM-PSRL |
|------|----------|----------|
| 探索机制 | 隐式探索（ICRL的随机采样、Reflexion的反思、ICPI的贪婪策略） | 显式的后验采样与按采样MDP最优执行的汤普森采样探索 |
| 知识状态表示 | 非结构化的交互历史或反思文本 | 由专门LLM维护的文字型后验分布，明确编码已知信息和不确定性 |

基线方法的隐式探索在面对硬探索任务时表现乏力。例如在RiverSwim环境中，Reflexion在几次上游游泳失败后便放弃探索，转而收敛于较小的下游奖励；ICRL同样几乎未能有效探索（Figure 6）。相比之下，LLM-PSRL通过在每个情节开始时从后验分布中采样一个关于真实MDP的统计合理假设，然后在整个情节中对该假设执行最优策略，实现了**汤普森采样**所固有的“概率匹配”探索——对不确定性高的动作给予与其成为最优动作概率成比例的探索次数。

**2. 知识状态的显式维护与更新**

LLM-PSRL将PSRL的三个核心计算步骤分配给三个专门的LLM（Figure 2）：

- **后验采样LLM**：根据当前文字型后验分布，生成一个关于真实MDP转移和奖励函数的合理假设（后验样本）。该后验是“一个文本描述，总结了对真实MDP转移和奖励函数的已知方面和不确定方面”。
- **最优样本策略LLM**：在给定当前状态下，根据后验样本执行与自然语言假设一致的最优动作，最大化期望值。
- **后验更新LLM**：在完整轨迹结束后，更新智能体的知识和残余不确定性，实现近似后验更新。与PSRL的设计一致，认知状态在整个情节内保持固定，仅在情节结束时使用完整轨迹进行更新。

这种显式的知识状态维护机制是LLM-PSRL区别于所有基线方法的核心特征。基线方法要么完全缺乏结构化的不确定性表示，要么仅通过反思文本隐式地传递经验，无法系统性地追踪“已知什么”和“不知道什么”。

### 决定性证据

实验证据强有力地支持了上述创新的有效性：

- **探索效率超越经典方法**：在5臂伯努利好赌中，LLM-PSRL（κ=1.2）在100步内的累计遗憾低于经典汤普森采样（Figure 4），证明LLM实现的PSRL不仅复现了TS的探索特性，甚至在某些条件下超越了其数学精确版本。
- **硬探索任务的质变**：在RiverSwim中，将底层LLM从GPT-4o升级为o1-mini后，LLM-PSRL的遗憾从线性降至与表格型PSRL相当的次线性水平，而Reflexion和ICRL几乎未能有效探索（Figure 6）。这揭示了探索机制的质变——更强的LLM放大了显式探索范式的优势，但对隐式探索方法几乎无帮助。
- **自然语言任务的鲁棒优势**：在组合锁和Wordle等自然语言MDP任务中，LLM-PSRL显著优于所有LLM基线，且即使基线使用更强的模型（DeepSeek-R1），也无法超越仅使用GPT-4o的LLM-PSRL（Figure 7, Figure 8, Figure 15）。

### 局限与待验证的边界

尽管创新显著，该方法仍存在明确局限：在状态-动作空间较大且转移随机性较强的MDP中，LLM的规划能力不足会导致遗憾退化（Figure 14）；方法依赖手工设计的先验分布；当前仅适用于有限视界的情节任务。这些边界条件需要在后续研究中进一步验证和突破。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_M3vwnscpL2/figures/001_Figure_1.jpg]]
*Figure 1: Abstractly, an RL algorithm is an ordered sequence of steps. Existing approaches for LLM agent design (left) orchestrate some number of LLMs to implicitly induce a RL algorithm. In contrast, this paper advocates for a novel agent design principle (right) whereby an existing RL algorithm is explicitly implemented by outsourcing individual steps to distinct LLMs*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_M3vwnscpL2/figures/002_Figure_2.jpg]]
*Figure 2: The PSRL algorithm with LLM subroutines of posterior sampling, optimal behavior with respect to a sample, and posterior updating shown. Dotted arrows show data flow*

LLM-PSRL 的核心设计原则是将经典的后验采样强化学习算法显式地分解为三个由 LLM 实现的子程序，而非像现有方法（Reflexion、ICRL、ICPI）那样仅依靠 LLM 的随机性或上下文学习进行隐式探索（Figure 1）。该框架在每情节内保持认知状态固定，仅在情节结束后利用完整轨迹进行后验更新，从而继承了 PSRL 固有的统计高效探索特性。

### 三模块流水线

LLM-PSRL 的流水线由三个功能明确的 LLM 子程序构成，其数据流如 Figure 2 所示：

1. **后验采样 LLM（Posterior Sampling LLM）**：接收当前文字型后验分布作为输入，生成一个关于真实 MDP 转移函数与奖励函数的合理假设（即后验样本）。该后验分布是一个文本描述，显式编码了智能体对环境的已知信息和残留不确定性。

2. **最优样本策略 LLM（Optimal Sample Policy LLM）**：在给定当前状态和后验样本的条件下，执行与样本假设一致的、最大化期望值的动作。该模块本质上是在后验样本所描述的“想象 MDP”中执行最优策略。

3. **后验更新 LLM（Posterior Update LLM）**：在每情节结束后，根据完整轨迹更新智能体的知识状态与残留不确定性，实现近似的后验更新。更新后的后验分布将作为下一情节后验采样 LLM 的输入。

Figure 3 以 Wordle 游戏为例，展示了 LLM 生成的后验分布（上）与后验样本（下）的实际样貌。

### 与现有方法的本质差异

现有 LLM 智能体设计（Figure 1 左）通过编排若干 LLM 来隐式地诱导某种 RL 算法，其探索行为源于 LLM 的随机性（如 ICRL 从重播缓冲区随机采样）或启发式反思（如 Reflexion 的自我反思），缺乏结构化的探索机制。LLM-PSRL（Figure 1 右）则显式实现了 PSRL 的汤普森采样探索逻辑：先根据后验分布采样一个统计上合理的环境假设，再对该假设执行最优策略。这一差异在方法层面体现为两个关键槽位的变化：

- **探索机制**：从隐式探索（ICRL 的随机采样、Reflexion 的反思、ICPI 的贪婪策略）转变为显式的后验采样与按采样 MDP 最优执行的汤普森采样探索。
- **知识状态表示**：从非结构化的交互历史或反思文本，转变为由专门 LLM 维护的文字型后验分布，明确编码已知信息和不确定性。

### 输入输出流

在每情节 $k$ 中，流水线按以下顺序执行：

1. 后验更新 LLM 输出当前后验分布（初始情节使用手工设计的先验）。
2. 后验采样 LLM 读取后验分布，生成后验样本 $\mathcal{M}_k$。
3. 最优样本策略 LLM 在 $\mathcal{M}_k$ 中逐步执行动作，收集完整轨迹 $\tau_k$。
4. 后验更新 LLM 利用 $\tau_k$ 更新后验分布，进入下一情节。

该设计的关键在于，后验采样 LLM 的温度参数 $\kappa_{\text{sampling}}$ 是控制探索行为的核心旋钮：$\kappa_{\text{sampling}} \leq 1$ 时趋向贪婪，$\kappa_{\text{sampling}} > 1$ 时更接近经典汤普森采样的探索分布。这一机制使得 LLM-PSRL 在 5 臂伯努利好赌中能以 $\kappa_{\text{sampling}}=1.2$ 取得低于经典汤普森采样的累计遗憾（Figure 4），验证了显式实现经典算法子程序的设计原则的有效性。

### 问题形式化与评估指标

论文将LLM智能体的探索任务建模为有限视界的情节式马尔可夫决策过程（MDP）。在每个情节 $k$ 中，智能体与一个未知的MDP $\mathcal{M} = (\mathcal{S}, \mathcal{A}, H, \mathcal{R}, \mathcal{P}, s_1)$ 交互，其中 $\mathcal{S}$ 为状态空间，$\mathcal{A}$ 为动作空间，$H$ 为视界长度，$\mathcal{R}$ 为奖励函数，$\mathcal{P}$ 为转移函数，$s_1$ 为固定初始状态。

对于给定MDP $\mathcal{M}$ 和策略 $\pi$，动作价值函数定义为从状态 $s$ 和动作 $a$ 开始，在剩余时间步内遵循 $\pi$ 获得的期望累积奖励：

$$Q_{\mathcal{M}, h}^{\pi}(s, a) = \mathbb{E}\left[ \sum_{h' = h}^{H} \mathcal{R}(s_{h'}, a_{h'}) \mid s_h = s, a_h = a \right]$$

智能体的最优策略 $\pi^{\star}$ 满足 $V_{\mathcal{M}, h}^{\star}(s) = \max_{a \in \mathcal{A}} Q_{\mathcal{M}, h}^{\star}(s, a)$。衡量算法效率的核心指标是**累计遗憾**（Cumulative Regret），定义为 $K$ 个情节中实际策略与最优策略的价值差距之和：

$$\text{REGRET}(\{\pi^{(k)}\}_{k \in [K]}, \mathcal{M}) = \mathbb{E}\left[ \sum_{k=1}^{K} \left( V_{\mathcal{M}, 1}^{\star}(s_1) - V_{\mathcal{M}, 1}^{\pi^{(k)}}(s_1) \right) \mid \mathcal{M} \right]$$

进一步，**贝叶斯遗憾**（Bayesian Regret）在智能体先验分布下对模型不确定性进行积分，反映贝叶斯意义上的期望性能：

$$\text{BAYESREGRET}(\{\pi^{(k)}\}_{k \in [K]}) = \mathbb{E}\left[ \text{REGRET}(\{\pi^{(k)}\}_{k \in [K]}, \mathcal{M}) \right]$$

### LLM-PSRL的三模块架构

本方法的核心设计原则是将经典的后验采样强化学习算法显式分解为三个由LLM实现的子程序，如Figure 2所示。每个模块承担PSRL算法中的一个独立计算步骤，数据流通过自然语言文本在模块间传递。

**模块一：后验采样LLM（Posterior Sampling LLM）**

该模块接收智能体当前的文字型后验分布，负责生成一个关于真实MDP转移函数和奖励函数的合理假设——即后验样本。后验分布本身是一个文本描述，概括了已知信息和残留不确定性（如Figure 3上半部分所示）。后验样本则是一个具体的、统计上合理的MDP假设（如Figure 3下半部分所示）。这一步骤实现了汤普森采样的核心机制：从认知不确定性中采样一个可能的世界模型。

**模块二：最优样本策略LLM（Optimal Sample Policy LLM）**

给定当前状态和后验样本，该模块执行与采样MDP假设一致的最优动作，以最大化期望价值。这对应于PSRL算法中“在采样模型上执行最优策略”的步骤。LLM需要理解自然语言描述的后验样本，并在当前状态下推理出最优动作。

**模块三：后验更新LLM（Posterior Update LLM）**

在每个情节结束后，该模块根据完整轨迹 $\tau_k$ 更新智能体对世界的知识和残留不确定性。更新后的后验分布用于下一情节的采样。这一设计遵循PSRL的关键特性：认知状态在情节内保持固定，仅在情节边界处更新，从而保证探索的结构化。

### 经典PSRL的先验形式

在表格型MDP（如RiverSwim）的对比实验中，经典PSRL使用狄利克雷分布建模转移函数的不确定性。其先验参数初始化为均匀分布：

$$\alpha_0 = \frac{1}{|S|}$$

其中 $|S|$ 为状态空间大小。这一先验对应 $|S||A|$ 个独立的狄利克雷分布，每个分布编码一个状态-动作对下转移至各后继状态的概率信念。LLM-PSRL则通过自然语言描述实现类似的不确定性表示，例如在多臂好赌任务中，每个臂的先验被指定为 $\text{Beta}(1,1)$ 的文字形式。

### LLM-IDS变体的目标函数

作为扩展，论文在附录中探索了信息导向采样（Information-Directed Sampling）的LLM实现。LLM-IDS在每个时间步求解以下最小化问题，以平衡探索与利用：

$$\min_{\pi \in \Delta(\mathcal{A})} \frac{\mathbb{E}_{a\sim\pi}[\rho(a)]^2}{\mathbb{E}_{a\sim\pi}[I(a)]}$$

其中 $\rho(a)$ 为选择动作 $a$ 的期望单步遗憾，$I(a)$ 为选择该动作获得的信息增益。该目标函数最小化期望遗憾平方与信息增益之比，使智能体优先选择那些以较小遗憾代价换取较大信息量的动作。在11臂信息动作好赌任务中，LLM-IDS展现出优于LLM-PSRL的指导性探索能力。

## 实验与关键发现

### 核心瓶颈与探索机制验证

当前基于LLM的智能体设计——包括**Reflexion**（Shinn et al., 2024）、**ICRL**（Monea et al., 2024）和**ICPI**（Brooks et al., 2023）——在面对需要高效探索的决策任务时普遍表现不佳。这些方法的探索行为本质上是**隐式的**：ICRL依赖从重播缓冲区随机采样经验作为上下文并借助LLM的随机性进行探索，Reflexion通过对轨迹的自我反思产生口头指导来改善决策，而ICPI则通过三个LLM分别模拟转移函数、奖励函数和rollout策略，使用上下文学习进行贪婪的策略迭代。它们缺乏结构化的探索机制，难以应对具有稀疏奖励或需要深度探索的环境。

本文提出的**LLM-PSRL**（LLM-based Posterior Sampling for Reinforcement Learning）将经典贝叶斯强化学习算法——后验采样强化学习（PSRL）——**显式分解**为三个由LLM实现的子程序：后验采样LLM、最优样本策略LLM和后验更新LLM。这一设计使智能体获得PSRL固有的统计高效探索能力，其核心机制是**汤普森采样**：每个情节开始时从当前后验分布中采样一个关于真实MDP的合理假设，然后在该假设下执行最优策略，情节结束后根据完整轨迹更新后验。

### 多臂好赌：超越经典汤普森采样

在5臂伯努利好赌（T=100）中，LLM-PSRL展现出令人惊讶的探索效率。如Figure 4所示，当后验采样LLM的温度参数$\kappa_{\text{sampling}} = 1.2$时，LLM-PSRL的累计遗憾曲线**低于经典汤普森采样**，表明其探索效率优于这一理论基础深厚的经典方法。这一结果并非偶然：温度参数对探索行为有决定性影响。当$\kappa_{\text{sampling}} \leq 1$时，LLM趋向贪婪行为，探索不足；而当温度适当升高时，LLM的采样分布更接近经典汤普森采样的探索特性。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_M3vwnscpL2/figures/004_Figure_4.jpg]]
*Figure 4: Cumulative regret curves for a 5-armed Bernoulli bandit*

消融分析进一步揭示了探索行为的微观结构。Figure 9展示了后缀失败频率（suffix failure frequency）随时间的演化——后缀失败指在时间$t$后最优动作$A^\star$再未被选中。Figure 10展示了最少选择动作的缩放频率，衡量探索分布的均衡性。Figure 11将两者绘制为散点图，对比了经典TS与不同温度的LLM-PSRL，直观展示了温度如何调节探索-利用的权衡。

在真实世界客户服务好赌任务中（Figure 5），当先验设定正确时，LLM-PSRL的表现远超所有基线方法。值得注意的是，即使先验设定错误，基线方法也无法显著超越PSRL（Figure 12），这表明PSRL的探索框架本身具有较强的鲁棒性。

### 硬探索MDP：RiverSwim的关键发现

RiverSwim是一个经典的硬探索任务，智能体需要逆流游向上游以获得较大奖励，但逆流动作有失败概率。这一环境对探索能力的要求极高。

Figure 6展示了3状态RiverSwim的累计遗憾曲线，揭示了**底层LLM能力的关键作用**。当使用GPT-4o时，LLM-PSRL的遗憾接近线性，与Reflexion和ICRL一样几乎未能有效探索。然而，当底层LLM从GPT-4o升级为**o1-mini**时，LLM-PSRL的遗憾从线性降至**与表格型PSRL（Vanilla PSRL, Osband et al., 2013）相当的次线性水平**，而同样的模型升级对Reflexion和ICRL**无显著改进甚至产生负面影响**。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_M3vwnscpL2/figures/006_Figure_6.jpg]]
*Figure 6: Cumulative regret curves for the RiverSwim environment with 3 states. Labels show the choice of constituent LLM model (GPT-4o or o1-mini) in each LLM agent*

这一发现指向一个深层机制：LLM-PSRL将探索问题分解为后验采样、最优策略执行和后验更新三个子任务，更强的推理模型（o1-mini）能够更准确地执行这些子程序，从而释放PSRL算法本身的探索优势。相比之下，隐式探索方法即使使用更强的模型，也无法获得结构化的探索能力。

Figure 13揭示了GPT-4o版PSRL失败的原因：当LLM缺乏对确定性转移的先验知识时，其规划能力不足以在随机环境中有效导航。但当提供所有确定性转移的先验知识后，遗憾显著改善，说明问题出在**LLM的规划能力**而非探索机制本身。

### 自然语言MDP：组合锁与Wordle

在组合锁环境（H=3, K=8）中（Figure 7），LLM-PSRL（GPT-4o）识别解锁代码所需的回合数显著少于所有LLM基线。这一环境要求智能体系统地探索代码空间，LLM-PSRL的后验采样机制天然适合这种结构化探索。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_M3vwnscpL2/figures/007_Figure_7.jpg]]
*Figure 7: Cumulative regret curves for the combination lock environment. The vertical axis shows turns to identify the unlock code*

在Wordle任务（K=5）中（Figure 8），LLM-PSRL同样展现出最优的累计遗憾。值得注意的是，即使基线方法下载更强的模型（**DeepSeek-R1**），也无法超越只使用GPT-4o的LLM-PSRL（Figure 15）。DeepSeek-R1确实普遍提升了所有LLM智能体的表现，但这一提升未能弥补隐式探索与显式汤普森采样之间的结构性差距。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_M3vwnscpL2/figures/008_Figure_8.jpg]]
*Figure 8: Cumulative regret curves for the Wordle environment. Labels show the choice of constituent LLM model (GPT-4o or DeepSeek-R1) in each LLM agent*

### 令牌效率与成本分析

一个合理的质疑是：LLM-PSRL调用三个LLM子程序，是否仅因消耗更多计算资源而占优？Figure 19和Figure 20分别展示了组合锁和Wordle环境下累计遗憾与累计令牌数的关系。在将PSRL截断至与其他方法相同的令牌预算后，LLM-PSRL在同等预算下仍然更优，证明其**信息增益效率**而非资源消耗是性能优势的来源。

成本方面（Table 1），不同领域的单次试验资金成本差异显著：5臂伯努利好赌约$0.11，组合锁约$0.50，Wordle约$0.75，RiverSwim约$1.00。Tables 2-5详细记录了各LLM子程序在不同领域的令牌使用统计。RiverSwim消耗令牌最多（每情节约6200个总令牌），主要因为其后验更新LLM需要处理更复杂的转移函数不确定性。

### 信息导向采样的初步探索

作为扩展，论文初步探索了LLM实现信息导向采样（LLM-IDS）的可能性。在11臂信息动作好赌任务中（Figure 16, Figure 17），LLM-IDS在需要指导性探索的场景下优于LLM-PSRL。在组合锁环境中（Figure 18），LLM-IDS同样展现出优势。LLM-IDS最小化目标函数：

$$\min_{\pi \in \Delta(\mathcal{A})} \frac{\mathbb{E}_{a\sim\pi}[\rho(a)]^2}{\mathbb{E}_{a\sim\pi}[I(a)]}$$

其中$\rho(a)$为期望遗憾，$I(a)$为信息增益，这一目标函数显式平衡探索与利用。

### 失败模式与局限性

尽管LLM-PSRL在多数任务中表现优异，其局限性同样明确：

1. **规模退化**：Figure 14比较了3状态与4状态RiverSwim中o1-mini版PSRL的遗憾曲线。当状态空间从3扩大到4时，遗憾明显恶化，说明LLM的规划能力在状态-动作空间增大时成为瓶颈。

2. **先验敏感性**：方法依赖手工设计的先验分布。在客户服务好赌任务中，先验设定错误时性能会受影响，尽管文中提出了使先验“设定正确”的技巧（向GPT-4o提供数据集解决方案作为先验参考）。

3. **后验更新可靠性**：后验更新LLM有时会忘记信息或错误更新，在长情节中这一问题尤为突出，可能导致后验分布偏离真实不确定性。

4. **计算成本**：每次试验需要大量API调用，限制了大规模试验的可行性。

5. **适用范围**：当前仅适用于有限视界的情节任务，向无限视界及连续控制环境扩展需要解决更严峻的表示和规划挑战。

## 定位与知识库关联

### 设计范式对比：隐式诱导 vs. 显式实现

现有基于LLM的智能体设计普遍采用“隐式诱导”范式（Figure 1 左）：通过编排一个或多个LLM，使其在交互中涌现出某种RL算法的行为，但算法本身并未被显式编程。典型代表包括：

- **Reflexion**（Shinn et al., 2024）：通过对轨迹进行自我反思，生成口头指导以改善决策。其探索能力依赖于LLM从失败经验中归纳出的启发式规则，缺乏系统性的不确定性量化。
- **In-Context RL (ICRL)**（Monea et al., 2024）：从重播缓冲区中随机采样经验作为上下文，利用LLM的随机性进行隐式探索。探索的质量完全取决于上下文采样的偶然性和LLM的随机生成能力。
- **In-Context Policy Iteration (ICPI)**（Brooks et al., 2023）：通过三个LLM分别模拟转移函数、奖励函数和rollout策略，使用上下文学习进行策略迭代。该方法本质上执行的是贪婪策略改进，未内建显式的探索机制。

本文提出的核心范式转变（Figure 1 右）是：**将已有的高效RL算法显式分解为若干计算步骤，每个步骤由一个专门的LLM子程序实现**。这一范式并非主张LLM可以“学会”RL算法，而是将LLM视为执行特定计算角色（后验采样、最优策略执行、后验更新）的语义引擎。因果上，这使得智能体获得了经典算法固有的统计效率保证，而非依赖LLM的涌现能力来隐式地“发现”好的探索策略。

### 与经典PSRL的关系

本文方法直接继承自后验采样强化学习（Posterior Sampling for RL, PSRL），其理论基础可追溯至汤普森采样（Thompson Sampling）和贝叶斯强化学习。经典表格型PSRL（Osband et al., 2013）通过狄利克雷先验（参数初始化为 $\alpha_0 = \frac{1}{|S|}$）对转移函数进行贝叶斯建模，在每个情节开始时从后验中采样一个MDP假设，然后执行该假设下的最优策略，最后根据完整轨迹更新后验。

LLM-PSRL保留了PSRL的算法骨架（Algorithm 1），但将三个核心子程序替换为LLM调用：

1. **后验采样LLM**：将经典方法中从狄利克雷/贝塔分布采样的数学操作，替换为从自然语言描述的后验中生成一个“关于真实MDP的合理假设”。采样温度 $\kappa_{\text{sampling}}$ 成为控制探索程度的可调旋钮。
2. **最优样本策略LLM**：将经典方法中基于动态规划或值迭代的最优策略计算，替换为LLM根据自然语言假设进行的上下文规划与动作选择。
3. **后验更新LLM**：将经典方法中基于共轭先验的解析贝叶斯更新，替换为LLM对交互历史进行语义总结和不确定性修正。

这一设计使得LLM-PSRL在结构上等价于PSRL，因此天然继承了其统计高效探索的理论优势。实验证据表明，这种继承是实质性的：在RiverSwim硬探索任务中，当底层LLM从GPT-4o升级为o1-mini后，LLM-PSRL的累计遗憾从线性降至与表格型PSRL相当的次线性水平（Figure 6），而Reflexion和ICRL几乎未能有效探索。

### 适用边界与局限

#### 已验证的有效域

- **多臂好赌（Bandit）**：在5臂伯努利好赌中，LLM-PSRL（$\kappa_{\text{sampling}}=1.2$）在100步内的累计遗憾低于经典汤普森采样（Figure 4），证明LLM子程序可以忠实地复现甚至超越经典方法的探索效率。
- **自然语言好赌**：在真实世界客户服务好赌任务中，当先验设定正确时，LLM-PSRL的表现远超所有基线（Figure 5, Figure 12）。
- **确定性转移的小规模MDP**：在组合锁（H=3, K=8）和Wordle（K=5）等自然语言任务中，LLM-PSRL显著优于所有LLM基线（Figure 7, Figure 8）。值得注意的是，即使基线方法使用更强的底层模型（DeepSeek-R1），也无法超越仅使用GPT-4o的LLM-PSRL（Figure 15）。
- **信息导向探索扩展**：LLM-IDS变体在需要指导性探索的任务（如11臂信息动作好赌）中优于LLM-PSRL（Figure 16, Figure 17），表明该范式可推广至更复杂的探索策略。

#### 已知失效模式与边界

1. **随机转移函数的规模退化**：在状态-动作空间较大且转移函数具有随机性的MDP中，LLM的规划能力不足导致遗憾从次线性退化为近线性。Figure 13揭示了GPT-4o版PSRL在RiverSwim中失败的原因——LLM无法准确评估在随机转移下持续尝试上游游泳的期望价值。即使使用更强的o1-mini，当RiverSwim从3状态扩展到4状态时，遗憾也出现明显恶化（Figure 14），表明问题未根本解决。

2. **先验依赖**：方法依赖于手工设计的先验分布。在客户服务好赌任务中，当先验设定错误时性能会受影响（Figure 12中“misspecified”条件），尽管文中提出了使先验“设定正确”的技巧（向GPT-4o提供数据集的解决方案作为参考），但这一过程本身需要领域知识。

3. **计算成本约束**：每次试验需要大量API调用（Table 1记录了各领域的单次试验资金成本），限制了大规模试验的可行性。尽管在令牌效率的公平比较中（Figure 19, Figure 20），PSRL在同等令牌预算下仍优于基线，但绝对成本仍然较高。

4. **有限视界限制**：当前设计仅适用于有限视界的情节任务，向无限视界及连续控制环境的扩展需要解决更严峻的表示和规划挑战。

### 开放问题

1. **可靠的后验更新机制**：后验更新LLM在长情节中有时会遗忘信息或产生错误更新。如何设计更可靠的LLM后验更新机制，避免信息被错误遗忘或扭曲，是实现长程探索的关键瓶颈。

2. **模型无关扩展**：能否将LLM-PSRL与模型无关的PSRL变体（如基于值函数后验的随机化方法）结合，以规避对完整转移模型的依赖，从而提升在随机环境中的鲁棒性？

3. **紧凑认知状态表示**：在更大规模的随机环境中，如何利用LLM的语义理解构造更紧凑的认知状态表示（例如环境代理模型），以改善规划质量？

4. **信息导向探索的推广**：LLM-IDS为信息导向探索提供了初步路径，但当前实现仅限于近视的信息增益估计。如何推广到非近视的未来信息增益估计仍是一个开放问题。

5. **范式收敛性**：随着LLM能力的持续提升，是否会出现更简洁的隐式探索方法，还是显式实现经典算法的范式将持续受益于更强的LLM？实验已表明，将底层模型从GPT-4o升级为o1-mini对LLM-PSRL的改进远大于对基线方法的改进（Figure 6），暗示显式实现范式可能具有更好的能力扩展性。

6. **不确定性量化验证**：如何系统地验证和改进LLM在实现算法子程序时的准确性和不确定性量化能力，是确保该方法在实际部署中可靠性的前提。

## 原文 PDF

![[paperPDFs/ICLR_2026/Toward_Efficient_Exploration_by_Large_Language_Model_Agents.pdf]]
