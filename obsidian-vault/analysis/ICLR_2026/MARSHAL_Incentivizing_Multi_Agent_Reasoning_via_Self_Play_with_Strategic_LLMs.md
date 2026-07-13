---
title: "MARSHAL: Incentivizing Multi-Agent Reasoning via Self-Play with Strategic LLMs"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/MARSHAL_Incentivizing_Multi_Agent_Reasoning_via_Self_Play_with_Strategic_LLMs.pdf
project_link: https://thu-nics.github.io/MARSHAL/
code_link: https://github.com/thu-nics/MARSHAL
openreview_forum_id: GCd5v3ehmr
aliases:
- MARSHAL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "回合级优势估计器（先求和再归一化）与智能体特定优势归一化（按玩家角色独立归一化）是解决训练不稳定和提升泛化能力的关键设计。"
primary_logic: "通过在多样化的合作与竞争策略游戏中进行自我博弈训练，LLM 能够获得可迁移至下游多智能体推理任务的通用交互能力，而不仅仅是记忆游戏策略；这种能力通过角色理解与意图识别等模式显式涌现。"
claims:
- "MARSHAL 通才模型在 held-out 游戏 Leduc Hold'em 上性能提升 28.7%，Simple Hanabi 上提升 22.9%，证明跨游戏泛化能力。"
- "在 MAD 竞争框架中，MARSHAL 通才模型在 GPQA-Diamond 上零样本提升 7.57%，在 AutoGen 合作框架中 AIME 提升 10.00%，验证了游戏技能向多智能体推理的泛化。"
- "失败模式分析显示 MARSHAL 将 GPQA-Diamond 上的“智能体间不对齐”错误减少 11.5%，主要由于任务偏离和忽略其他智能体输入显著下降。"
- "消融实验表明移除回合级优势估计器或智能体特定归一化会系统性损害游戏表现和下游泛化，固定对手训练则导致严重过拟合。"
---

# MARSHAL: Incentivizing Multi-Agent Reasoning via Self-Play with Strategic LLMs

> [!tip] 核心洞察
> 通过在多样化的合作与竞争策略游戏中进行自我博弈训练，LLM 能够获得可迁移至下游多智能体推理任务的通用交互能力，而不仅仅是记忆游戏策略；这种能力通过角色理解与意图识别等模式显式涌现。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MARSHAL：通过战略型大语言模型自我博弈激励多智能体推理 |
| 英文题名 | MARSHAL: Incentivizing Multi-Agent Reasoning via Self-Play with Strategic LLMs |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=GCd5v3ehmr) · [GitHub](https://github.com/thu-nics/MARSHAL) · [Project](https://thu-nics.github.io/MARSHAL/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | MARSHAL |
| Dataset | Leduc Hold'em（held-out 测试游戏）, Simple Hanabi（held-out 测试游戏）, AIME（AutoGen 合作框架）, GPQA-Diamond（MAD 竞争框架） |

> [!tip] 效果简介
> - Leduc Hold'em（held-out 测试游戏） 上，相对基础模型性能提升 为 比 Qwen3-4B 基础模型提升 28.7%，对比 Qwen3-4B 未训练基线，变化 +28.7%。
> - Simple Hanabi（held-out 测试游戏） 上，相对基础模型性能提升 为 比 Qwen3-4B 基础模型提升 22.9%，对比 Qwen3-4B 未训练基线，变化 +22.9%。
> - AIME（AutoGen 合作框架） 上，准确率 为 66.67，对比 56.67 (Qwen3-4B)，变化 +10.00。

## 概要

多智能体推理是当前大语言模型（LLM）应用的关键瓶颈：在多轮交互中，不同角色智能体的长序列信用分配困难，且优势估计方差过大，导致强化学习训练不稳定，学到的策略难以泛化到下游任务。MARSHAL 针对这一瓶颈，提出**回合级优势估计器**与**智能体特定优势归一化**两项关键设计，在合作与竞争策略游戏中通过自我博弈端到端训练 LLM，使其获得可迁移的通用多智能体交互能力。

核心发现是：通过在多样化游戏环境中进行自我博弈训练，LLM 不仅学会游戏策略，更涌现出角色理解、意图识别等推理模式，这些能力可零样本迁移至下游多智能体推理任务。实验表明，MARSHAL 通才模型在 held-out 游戏 Leduc Hold’em 上性能提升 28.7%，在 Simple Hanabi 上提升 22.9%（Figure 3）；在 MAD 竞争框架下的 GPQA-Diamond 上零样本提升 7.57%，在 AutoGen 合作框架下的 AIME 上提升 10.00%（Table 1）。失败模式分析进一步显示，MARSHAL 将 GPQA-Diamond 上“智能体间不对齐”错误减少 11.5%（Figure 5）。消融实验证实，移除回合级优势估计器或智能体特定归一化均会系统性损害游戏表现与下游泛化能力（Table 3, Table 4）。



大语言模型（LLM）在单智能体推理任务中已展现出卓越能力，但在多智能体系统中，模型需要同时具备策略规划、对手建模、意图识别和协作沟通等复合能力，这对现有范式提出了根本性挑战。当前主流方法通常依赖精心设计的提示工程或针对特定下游任务进行微调，这些方法存在一个共同的瓶颈：**多轮多智能体强化学习训练中长序列信用分配困难，以及不同角色智能体的优势估计方差过大，导致训练不稳定且难以泛化到下游多智能体任务**。

具体而言，在多回合交互场景下，一条轨迹可能包含数十个回合，每个回合的决策对最终结果的贡献程度差异巨大。朴素的多回合 GRPO 方法（公式 2）对所有轨迹的最终回报进行全局归一化，将同一个优势值广播给轨迹内的所有回合和智能体，这种做法忽略了回合间的因果结构，使得早期关键决策与后期无关动作获得相同的学习信号。此外，在竞争性游戏中，先手与后手玩家面临完全不同的策略空间和回报分布，将它们混合归一化会引入虚假的方差，进一步加剧训练的不稳定性。

现有基线方法 **SPIRAL**（Liu et al., 2025）虽然引入了基于奖励感知探索（RAE）的纯竞争性自我博弈机制，但其优势估计策略仍沿用单回合 GRPO 的全局归一化思路，未能有效解决多回合信用分配和角色不对称的问题。直接使用未微调的预训练模型（如 Qwen3-4B）则完全缺乏多智能体交互的结构化理解，在下游多智能体推理任务中表现不佳。

本文的核心洞察在于：**通过在多样化的合作与竞争策略游戏中进行自我博弈训练，LLM 能够获得可迁移至下游多智能体推理任务的通用交互能力，而不仅仅是记忆游戏策略；这种能力通过角色理解与意图识别等模式显式涌现**。基于此，我们提出 MARSHAL 框架，其关键设计包括两个因果性调节旋钮——回合级优势估计器（先求和再归一化）与智能体特定优势归一化（按玩家角色独立归一化），从根本上解决了训练不稳定和泛化能力不足的问题。



## 核心方法与创新机理

MARSHAL 的核心创新在于解决多轮多智能体强化学习训练中的两个根本性瓶颈：**长序列信用分配困难**与**不同角色智能体的优势估计方差过大**。为此，MARSHAL 在朴素 GRPO 多回合扩展的基础上，引入了两个相互关联的关键技术改进。

### 回合级优势估计器：先求和再归一化

朴素 GRPO 在多回合场景下的扩展（公式 2）沿用了原始 GRPO 的“先归一化再求和”逻辑：先将每个回合的即时奖励进行全局归一化得到优势，再将同一终局回报广播给轨迹内的所有回合。这种做法在长时程游戏中会导致严重的信用分配模糊——早期回合的关键决策与最终胜负之间的因果关系被稀释。

MARSHAL 提出了一种**关键的步骤反转**：先对每个回合 $k$ 到终局 $K$ 的即时奖励求和，得到回合级蒙特卡洛回报 $R_k^i$，然后在子组内对这些累积回报进行均值归一化。这一“先求和再归一化”的设计等价于 $\gamma=1, \lambda=1$ 的 GAE，使得每个回合的优势估计直接反映该回合对最终结果的累积贡献，从而为长序列中的每个决策提供更精确的学习信号。

### 智能体特定优势归一化：按角色独立分组

在多智能体自我博弈中，不同玩家角色（如先手与后手）面临截然不同的策略环境和回报分布。朴素 GRPO 将所有玩家轨迹混合进行全局归一化，导致优势估计被不同角色的回报方差污染，训练信号不稳定。

MARSHAL 将批次轨迹按玩家角色拆分为独立子组 $G^p$，在每个子组内部独立执行回合级优势估计。最终优势计算为 $A_{k,t}^{p,i} = R_k^{p,i} - \text{mean}(\mathbf{R}^p)$，确保每个角色的优势相对于该角色的平均水平居中。这一设计有效降低了跨角色方差对训练的干扰，使得竞争游戏中双方玩家都能获得稳定的优化信号。

### 奖励结构的三元设计

MARSHAL 的奖励信号由三部分组成，共同约束智能体的行为空间：

- **内在游戏奖励**：跨游戏最大标准化为 4，保证不同游戏间的公平比较。
- **格式奖励**：有效动作 +0.05，无效动作 -10.0 并终止游戏，强制模型遵循游戏规则。
- **响应长度惩罚**（公式 4）：$r_{\text{length}}(l) = \alpha \cdot \max(0, 1 - \frac{l - l_{\min}}{l_{\max} - l_{\min}})$，$\alpha=0.5$，鼓励简洁输出，对合作任务尤为关键。

### 与基线 SPIRAL 的差异

与基于 RAE（Reward-Aware Exploration）的纯竞争性自我博弈基线 **SPIRAL**（Liu et al., 2025）相比，MARSHAL 的关键差异不在于自我博弈本身，而在于**优势估计的粒度与分组策略**。SPIRAL 依赖探索奖励驱动策略多样性，而 MARSHAL 通过回合级信用分配和角色感知归一化从根本上解决了训练稳定性和泛化能力的问题——消融实验表明，移除这两个组件中的任何一个都会系统性地损害游戏表现和下游泛化。



![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_GCd5v3ehmr/figures/002_Figure_2.jpg]]
*Figure 2: Overview of MARSHAL. Left column: generating player trajectories through self-play in strategic games. Middle column: naive advantage estimation by GRPO. Right column: advantage estimation by MARSHAL for accurate credit assignment in multi-turn, multi-agent setting*

MARSHAL 是一个端到端强化学习框架，通过在多样化的合作与竞争策略游戏中进行自我博弈训练，激励大语言模型获得可迁移的多智能体推理能力。其核心瓶颈在于多轮多智能体 RL 训练中长序列信用分配困难以及不同角色智能体的优势估计方差过大，导致训练不稳定且难以泛化。MARSHAL 通过两个关键设计解决这一问题：**回合级优势估计器**（先对回合奖励求和再归一化）与**智能体特定优势归一化**（按玩家角色独立归一化）。

### Pipeline 总览

框架的整体流程如 Figure 2 所示，包含六个核心模块：

1. **自我博弈轨迹生成**
   同一 LLM 同时控制对局双方（如 player_0 与 player_1），在策略游戏中交替进行多回合交互。每个玩家产生独立的轨迹 $\{o_k^i\}_{k=1}^{K^i}$，其中 $K^i$ 为玩家 $i$ 的总回合数。训练基于 Group-Relative Policy Optimization（GRPO）框架展开。

2. **回合级奖励计算**
   每个回合 $k$ 获得即时奖励信号，由三部分组成（Section 3.4）：
   - **内在游戏奖励**：来自游戏规则的结果奖励（如胜负、得分），跨游戏最大标准化为 4；
   - **格式奖励**：有效动作 +0.05，无效动作 -10.0 并终止游戏；
   - **响应长度惩罚**：鼓励简洁输出，当响应长度 $l$ 超过阈值时线性施加惩罚，惩罚强度由 $\alpha=0.5$ 控制（公式 4）。

3. **累积回报求和**
   对每个玩家 $i$，从当前回合 $k$ 到终局回合 $K^i$ 对即时奖励求和，得到回合级蒙特卡洛回报：
   $$R_k^i = \sum_{t=k}^{K^i} r_t^i$$
   这一步是 MARSHAL 与朴素 GRPO 的关键差异——**先求和再归一化**，而非先归一化再广播。

4. **智能体特定子组划分**
   按玩家角色（如 player_0 和 player_1）将批次内的轨迹划分为独立子组 $G^p$。这一设计确保不同角色的优势估计不会相互污染：竞争游戏中先手与后手的回报分布天然不同，合作游戏中也可能存在角色不对称。

5. **优势归一化**
   在每个子组 $G^p$ 内独立计算回合级优势：
   $$A_{k,t}^{p,i} = R_k^{p,i} - \text{mean}(\mathbf{R}^p)$$
   优势值相对于该角色子组的平均水平居中，有效控制了不同角色的优势方差。

6. **GRPO 策略更新**
   使用 PPO 裁剪代理目标，以 token 级优势进行策略优化，更新 LLM 参数。MARSHAL 的最终训练目标为（公式 3）：
   $$\mathcal{T}_{\mathrm{MARSHAL}}(\theta) = \mathbb{E}_{s_k^{p,i}, o_{k,t}^{p,i}} \frac{1}{P} \sum_{p=1}^{P} \frac{1}{G_p} \sum_{i=1}^{G_p} \frac{1}{K^i} \sum_{k=1}^{K^i} \frac{1}{|o_k^{p,i}|} \sum_{t=1}^{|o_k^{p,i}|} \mathcal{T}_{\mathrm{surr}}(\pi_{\theta}; \pi_{\theta_{old}}, A_{k,t}^{p,i}, \varepsilon)$$

### 与朴素 GRPO 的关键差异

朴素多回合 GRPO（公式 2）对所有轨迹的最终回报进行全局归一化，将同一个优势值广播给轨迹内的所有回合和智能体。这在多回合多智能体场景下产生两个严重问题：
- **信用分配失效**：早期回合的决策无法与远期结果建立正确的因果关联；
- **优势方差过大**：不同角色的回报分布混合归一化，导致训练信号噪声。

MARSHAL 通过“先求和再归一化 + 按角色分组”的组合策略从根本上解决了这两个问题。消融实验（Table 4）证实：移除回合级优势估计器使 Mini Hanabi 性能从 50.48 降至 34.80，Tic-Tac-Toe 第二玩家回报从 32.10 降至 24.15；移除智能体特定归一化则导致竞争游戏性能不均衡，Kuhn Poker 整体回报下降。

### 训练配置

所有游戏训练使用统一超参数，内在奖励标准化到相同尺度（最大 4），保证不同游戏间的公平比较。训练硬件为单台 8×NVIDIA H100 GPU 服务器，所有模型均使用相同的基础模型 Qwen3-4B 和一致的训练步数（200 步）。



MARSHAL 的训练目标建立在 GRPO（Group-Relative Policy Optimization）基础之上，针对多轮多智能体场景中的长序列信用分配和不同角色智能体的优势估计方差过大这两个瓶颈，进行了两项关键改造：回合级优势估计器与智能体特定优势归一化。

### 背景：GRPO 目标函数

标准 GRPO 的优化目标为：

$$
\mathcal{I}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{q \sim P(Q), \{o^i\}_{i=1}^{G} \sim \pi_{\theta_{old}}(O|q)} \frac{1}{G} \sum_{i=1}^{G} \frac{1}{|o^i|} \sum_{t=1}^{|o^i|} \mathcal{I}_{\mathrm{surr}}(\pi_{\theta}; \pi_{\theta_{old}}, A_t^i, \varepsilon)
$$

其中 $A_t^i = \frac{r^i - \mathrm{mean}(\mathbf{r})}{\mathrm{std}(\mathbf{r})}$，优势由整组回复的最终回报归一化得到。该公式适用于单回合场景。

### 朴素多回合扩展及其缺陷

将 GRPO 直接扩展到多回合场景得到朴素目标：

$$
\mathcal{T}_{\mathrm{GRP}}^{\mathrm{muli}}(\theta) = \mathbb{E}_{s_k^i \sim P(S), o_{k,t}^i \sim \pi_{\theta,id}(O|s_k^i, o_{k,<t}^i)} \frac{1}{G} \sum_{i=1}^{G} \frac{1}{K^i} \sum_{k=1}^{K^i} \frac{|o_k^i|}{|o_k^i|} \sum_{t=1}^{|o_k^i|} \mathcal{T}_{\mathrm{sur}}(\pi_{\theta}; \pi_{\theta_{old}}, A_{k,t}^i, \varepsilon)
$$

其核心问题在于：对所有轨迹的最终回报进行全局归一化后，将同一个优势值广播给轨迹内的所有回合和智能体。这导致两个严重后果——早期关键回合无法获得独立的信用信号，且不同玩家角色的优势被强制在同一分布下比较，方差过大。

### 关键改造一：回合级优势估计器

MARSHAL 将 GRPO 的“先归一化再求和”流程颠倒为**先求和再归一化**。具体而言，对每条轨迹 $i$，从当前回合 $k$ 到最终回合 $K$ 对即时奖励求和，得到回合级蒙特卡洛回报：

$$R_k^i = \sum_{t=k}^{K} r_t^i$$

该回报等价于 $\gamma=1, \lambda=1$ 的 GAE，使每个回合获得独立的累积信用信号。随后在子组内对累积回报进行均值归一化，而非对最终标量奖励归一化。

### 关键改造二：智能体特定优势归一化

将批次轨迹按玩家角色拆分为独立子组 $G^p$（如 player_0 和 player_1），在每个子组内部独立应用回合级优势估计。最终优势为：

$$A_{k,t}^{p,i} = R_k^{p,i} - \mathrm{mean}(\mathbf{R}^p)$$

这确保优势估计相对于该角色的平均水平居中，消除不同角色回报分布差异带来的方差干扰。

### MARSHAL 最终目标函数

结合上述两项改造，MARSHAL 的训练目标为：

$$
\mathcal{T}_{\mathrm{MARSHAL}}(\theta) = \mathbb{E}_{s_k^{p,i} \sim P(S), o_{k,t}^{p,i} \sim \pi_{\theta_{old}}(O|s_k^{p,i}, o_{k,<t}^{p,i})} \frac{1}{P} \sum_{p=1}^{P} \frac{1}{G_p} \sum_{i=1}^{G_p} \frac{1}{K^i} \sum_{k=1}^{K^i} \frac{1}{|o_k^{p,i}|} \sum_{t=1}^{|o_k^{p,i}|} \mathcal{T}_{\mathrm{surr}}(\pi_{\theta}; \pi_{\theta_{old}}, A_{k,t}^{p,i}, \varepsilon)
$$

其中 $P$ 为玩家角色数，$G_p$ 为角色 $p$ 的轨迹组大小，$K^i$ 为轨迹 $i$ 的回合数。

### 奖励结构

每个回合的即时奖励由三部分组成：**内在游戏奖励**（跨游戏最大标准化为 4，如 Tic-Tac-Toe 奖励乘以因子 2）、**格式奖励**（有效动作 +0.05，无效动作 -10.0 并终止游戏）、**响应长度惩罚**：

$$r_{\mathrm{length}}(l) = \alpha \cdot \max\left(0, 1 - \frac{l - l_{\mathrm{min}}}{l_{\mathrm{max}} - l_{\mathrm{min}}}\right)$$

其中 $l$ 为响应 token 长度，$\alpha=0.5$ 控制惩罚强度。该惩罚鼓励简洁输出，消融实验表明去除该惩罚（$\alpha=0$）会导致 Mini Hanabi 性能从 50.48 骤降至 38.18，超过长损失率高达 20.4%。

### 训练流程

整体流程为：同一模型同时控制双方玩家，在策略游戏中交替进行多回合交互生成独立轨迹 → 按回合计算即时奖励（内在 + 格式 + 长度惩罚）→ 从当前回合到终局求和得到累积回报 → 按玩家角色划分子组 → 子组内独立计算优势 → 使用 PPO 裁剪代理目标进行 token 级策略优化。



## 实验与关键发现

### 核心瓶颈与方法动机

MARSHAL 要解决的根本问题是：在多轮多智能体强化学习训练中，长序列信用分配困难，且不同角色智能体的优势估计方差过大，导致训练不稳定、难以泛化到下游多智能体任务。为此，方法引入了两个关键设计——**回合级优势估计器**（先求和再归一化）与**智能体特定优势归一化**（按玩家角色独立归一化），二者构成训练稳定性和泛化能力的因果旋钮。

### 策略游戏泛化能力

Figure 3 展示了专家模型与通才模型在训练游戏和 held-out 测试游戏上的归一化回报。通才模型在未参与训练的 Leduc Hold'em 上相对 Qwen3-4B 基础模型提升 **28.7%**，在 Simple Hanabi 上提升 **22.9%**，证明跨游戏泛化能力。专家模型不仅掌握其训练领域，还能有效泛化到更复杂的同类 held-out 游戏（如从 Tic-Tac-Toe 到 Connect Four）。通才模型在所有游戏上表现一致且稳健，被确认为最通用、最鲁棒的智能体。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_GCd5v3ehmr/figures/003_Figure_3.jpg]]
*Figure 3: Average normalized game returns. Specialist agents not only master their training domains but also generalize effectively to their more complex, held-out counterparts (e.g., from Tic-Tac-Toe to Connect Four). The generalist model achieves consistently high performance across the entire suite of games, establishing it as the most robust and versatile agent*

Figure 4 的 Tic-Tac-Toe 专家训练曲线进一步显示，模型在训练游戏上持续改善的同时，在 OOD 合作游戏 Mini Hanabi 上也呈现平滑提升，表明训练过程中获得的交互能力具有跨类别迁移性。

### 下游多智能体推理泛化

Table 1 报告了在 MAD 竞争框架和 AutoGen 合作框架下的零样本推理基准结果。MARSHAL 通才模型在 MAD 框架中 GPQA-Diamond 上提升 **7.57%**（45.45 vs. 37.88），在 AutoGen 框架中 AIME 上提升 **10.00%**（66.67 vs. 56.67）。整体来看，通才模型在 MAD 框架所有基准平均提升 **3.51%**，在 AutoGen 框架平均提升 **3.01%**，验证了游戏自我博弈训练获得的技能可迁移至下游多智能体推理任务。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_GCd5v3ehmr/figures/005_Table_1.jpg]]
*Table 1: Evaluation results on downstream reasoning benchmarks within multi-agent systems. Competitive game-trained agents excel in the competitive MAD framework, while the cooperativetrained agent excels in the cooperative AutoGen framework. The generalist model performs robustly across both. Bold and underlined indicate the best and second-best scores, respectively*

一个值得注意的模式是：竞争游戏训练的智能体在竞争性 MAD 框架中表现更优，而合作游戏训练的智能体在合作性 AutoGen 框架中表现更优，通才模型则在两类场景中均表现稳健。

### 失败模式分析

Figure 5 对 GPQA-Diamond 上的失败模式进行了分类统计。MARSHAL 训练后，“智能体间不对齐”（Inter-Agent Misalignment）的发生率显著降低 **11.5%**。这一改善主要源于两个子类错误的下降：**任务偏离**（Task Derailment）和**忽略其他智能体输入**（Ignored Other Agent's Input）。这表明游戏自我博弈训练使 LLM 获得了更好的角色理解和意图识别能力，从而在多智能体交互中更有效地利用同伴信息、保持任务聚焦。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_GCd5v3ehmr/figures/007_Figure_5.jpg]]
*Figure 5: Percentage of different failure modes in GPQA-Dimond. Through MARSHAL training, the generalist agent significantly reduces the occurrence of Inter-Agent Misalignment*

### 消融实验

**自我博弈 vs. 固定对手（Table 3）**：使用固定对手训练的模型表现出严重的过拟合。例如，Kuhn Poker 固定对手专家在 Connect Four 等非训练游戏上的回报降至 0.00/0.00，远低于标准 MARSHAL 模型。这证实了自我博弈提供的自适应课程对发展鲁棒、可泛化的策略至关重要。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_GCd5v3ehmr/figures/008_Table_3.jpg]]
*Table 3: Generalization comparison between MARSHAL (self-play) and its fixed-opponent variant. The latter exhibits significant overfitting to static environments and opponents. Values denote average normalized game returns; for competitive games, entries indicate first-move / second-move returns. Underlined scores indicate performance degradation compared to the standard MARSHAL model*

**回合级优势估计器（Table 4）**：移除回合级优势估计器（w/o Turn-Level）导致长时程游戏性能系统性下降——Mini Hanabi 从 50.48 降至 34.80，Tic-Tac-Toe 第二玩家回报从 32.10 降至 24.15，证明回合级信用分配对多回合场景不可或缺。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_GCd5v3ehmr/figures/009_Table_4.jpg]]
*Table 4: Ablation results for algorithmic design. Both our turn-level advantage estimator and agentspecific advantage normalization prove essential for performance. Notation follows Table 3*

**智能体特定优势归一化（Table 4）**：移除智能体特定归一化（w/o Agent-Specific）损害竞争游戏性能——Kuhn Poker 回报下降，Tic-Tac-Toe 第一玩家回报虚高但泛化更差，整体表现不均衡。Figure 6 的回报分布进一步说明，该设计在竞争游戏中效果显著（两玩家回报分布差异大），在合作游戏中效果温和（两玩家回报分布相似），与理论预期一致。

**长度惩罚权重 α（Table 13）**：去除长度惩罚（α=0）使响应平均长度大幅增加，导致 Mini Hanabi 性能从 50.48 骤降至 38.18，超过长响应比例高达 20.4%。默认设置 α=0.5 在性能与简洁性之间取得最佳平衡。

### 关键图表结论汇总

| 图表 | 核心结论 |
|------|----------|
| Figure 3 | 通才模型跨游戏泛化最优，held-out 游戏提升 22.9%–28.7% |
| Figure 5 | 智能体间不对齐错误减少 11.5%，归因于任务偏离和忽略输入下降 |
| Table 1 | 下游多智能体推理零样本提升：GPQA-Diamond +7.57%，AIME +10.00% |
| Table 3 | 固定对手训练导致严重过拟合，自我博弈是泛化的必要条件 |
| Table 4 | 回合级优势估计和智能体特定归一化均为关键设计，移除任一损害性能 |
| Table 13 | 长度惩罚对合作任务至关重要，α=0 导致 Mini Hanabi 性能骤降 |

### 公平性说明

所有游戏训练使用统一超参数，内在奖励被标准化到相同尺度（最大 4），保证不同游戏间的公平比较。训练硬件为单台 8×NVIDIA H100 GPU 服务器，所有模型均基于相同的 Qwen3-4B 基础模型和一致的训练步数（200 步）。



## 定位与知识库关联

### 方法谱系：从单回合 GRPO 到多智能体自我博弈

MARSHAL 的核心训练框架建立在 **Group-Relative Policy Optimization (GRPO)**（Shao et al., 2024）之上。标准 GRPO 针对单回合场景设计：对同一问题采样一组回复，以组内相对奖励归一化计算优势函数，再进行 PPO 裁剪策略更新（公式 1）。其优势估计公式为：

$$A_t^i = \frac{r^i - \mathrm{mean}(\mathbf{r})}{\mathrm{std}(\mathbf{r})}$$

当直接将 GRPO 扩展到多回合、多智能体场景时，朴素做法是对所有轨迹的最终回报进行全局归一化，然后将同一个优势值广播给轨迹内的所有回合和所有智能体（公式 2）。这一做法存在两个关键缺陷：**（1）长序列信用分配困难**——早期回合的决策质量无法与最终回报建立精确的因果关联；**（2）优势估计方差过大**——不同玩家角色（如先手与后手）面对的博弈结构和回报分布截然不同，混合归一化导致学习信号失真。

MARSHAL 通过两个关键设计解决上述问题：

- **回合级优势估计器（Turn-Level Advantage Estimator）**：逆转 GRPO 的“先归一化再求和”流程，改为**先求和再归一化**。具体而言，从当前回合 $k$ 到终局 $K$ 对即时奖励求和得到蒙特卡洛回报 $R_k^i$，然后在子组内对累积回报进行均值归一化。这一设计等价于 $\gamma=1, \lambda=1$ 的 GAE，使得每个回合的优势估计直接反映该回合对最终结果的贡献。

- **智能体特定优势归一化（Agent-Specific Advantage Normalization）**：按玩家角色（如 player_0 和 player_1）将批次轨迹拆分为独立子组 $G^p$，每个子组内部独立进行回合级优势估计。最终优势为 $A_{k,t}^{p,i} = R_k^{p,i} - \mathrm{mean}(\mathbf{R}^p)$，确保每个角色的优势估计相对于该角色的平均水平居中，消除角色间回报分布差异带来的噪声。

MARSHAL 的最终训练目标（公式 3）整合了上述设计，在自我博弈框架下同时对多个玩家角色进行策略优化。

### 与现有方法的对比定位

**SPIRAL**（Liu et al., 2025）是基于 RAE（Reward-Aware Exploration）的纯竞争性自我博弈基线，同样采用强化学习训练 LLM 的游戏能力。MARSHAL 与之的关键差异在于：（1）MARSHAL 同时覆盖合作与竞争游戏，训练出的通才模型在两类多智能体系统中均表现稳健，而竞争性训练在合作框架中可能失效；（2）MARSHAL 的回合级优势估计器和智能体特定归一化是专门针对多回合信用分配和角色差异化的算法创新，SPIRAL 未涉及此类设计。实验表明（Table 8，需手动核实），MARSHAL 在合作游戏环境中显著优于 RAE-based agent 和纯竞争训练 agent。

**Qwen3-4B** 作为预训练基础模型，未针对游戏或多智能体交互进行任何微调，在下游多智能体推理基准上提供零样本基线。MARSHAL 通才模型在 MAD 竞争框架中平均提升 3.51%，在 AutoGen 合作框架中平均提升 3.01%，核心收益集中在高难度基准（GPQA-Diamond +7.57%，AIME +10.00%）。

### 适用边界与关键前提

MARSHAL 的有效性建立在以下前提之上：

1. **两人对称博弈假设**：当前实验限于两人经典策略游戏（井字棋、库恩扑克、花火等），自我博弈框架天然适配两人零和或合作场景。向更大规模 N 玩家环境扩展时，非平稳动力学和种群多样性维持成为关键挑战，现有方法未提供解决方案。

2. **游戏奖励可标准化**：跨游戏训练要求不同游戏的内在奖励被标准化到相同尺度（最大 4），否则优势估计的归一化将失效。论文通过缩放因子实现标准化，但这一策略对奖励分布极度偏斜的游戏可能不够鲁棒。

3. **角色数量已知且固定**：智能体特定归一化要求预先定义玩家角色并据此划分子组。在角色动态变化或数量不确定的开放场景中，该设计的直接适用性受限。

4. **格式约束可强制执行**：格式奖励（有效动作 +0.05，无效动作 -10.0 并终止游戏）依赖游戏引擎的规则校验。在非结构化多智能体任务（如开放域对话）中，如何定义和检测“有效动作”是一个开放问题。

### 局限与开放问题

**已知局限**：

- **游戏到现实的泛化鸿沟**：论文承认游戏场景与真实世界多智能体应用（如协作软件开发、谈判、具身智能体协调）之间存在差距。当前仅在数学和问答推理基准上验证了下游泛化，这些基准仍属于结构化文本任务，与开放域社会交互有本质区别。

- **规模扩展挑战**：训练使用单台 8×NVIDIA H100 GPU 服务器和 4B 参数模型。向更大模型（如 8B 版本在 Table 6-7 中有初步验证）和更多游戏扩展时，自我博弈的计算开销和训练稳定性需要进一步研究。

- **长度惩罚的敏感性**：消融实验（Table 13）显示去除长度惩罚（$\alpha=0$）使 Mini Hanabi 性能从 50.48 骤降至 38.18，超过长损失率高达 20.4%。这表明模型容易通过冗长输出“作弊”，而惩罚强度 $\alpha=0.5$ 是经验性选择，缺乏理论指导。

**开放问题**：

1. **N 玩家扩展**：如何将回合级优势估计和智能体特定归一化扩展到三个或更多玩家参与的环境？多玩家场景中信用分配的组合复杂度急剧上升，且需要处理联盟形成、通信协议等新维度。

2. **非结构化任务迁移**：通过游戏自我博弈学到的推理技能（角色理解、意图识别、策略规划）在多大程度上可以直接迁移到开放域对话、具身智能体协调等非结构化多智能体任务？是否需要中间适配层或额外的指令微调？

3. **训练效率与课程设计**：当前通才模型在所有游戏上均匀训练 200 步。是否可以通过自动课程学习（如基于难度的游戏排序、动态游戏权重调整）进一步提升训练效率和泛化能力？

4. **安全对齐**：自我博弈训练可能产生欺骗、操纵等非合作策略。如何在保持策略多样性的同时确保学到的行为符合人类价值对齐，是一个尚未探索的方向。



## 原文 PDF

![[paperPDFs/ICLR_2026/MARSHAL_Incentivizing_Multi_Agent_Reasoning_via_Self_Play_with_Strategic_LLMs.pdf]]
