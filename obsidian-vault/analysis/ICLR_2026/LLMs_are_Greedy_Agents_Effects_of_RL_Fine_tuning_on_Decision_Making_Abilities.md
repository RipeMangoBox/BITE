---
title: "LLMs are Greedy Agents: Effects of RL Fine-tuning on Decision-Making Abilities"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/LLMs_are_Greedy_Agents_Effects_of_RL_Fine_tuning_on_Decision_Making_Abilities.pdf
openreview_forum_id: weUP6H5Ko9
aliases:
- RRLFTSGCR
- LAGAERFTDMA
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "Reinforcement Learning Fine-Tuning (RLFT) on self-generated Chain-of-Thought (CoT) rationales using PPO with a KL constraint to a reference policy."
primary_logic: "LLMs' decision-making failures are rooted in behavioral biases (greediness, frequency bias) that prevent effective exploration; RL fine-tuning can teach LLMs to value exploration and transform knowledge into action, evidenced by increased action coverage, reduced regret, and a narrowed knowing-doing gap."
claims:
- "For 10-arm MABs, Gemma2 2B covers only 40% of actions, 27B covers 65%, and without CoT all models cover 25%, demonstrating severe greediness."
- "Gemma2 27B produces 87% correct UCB rationales but selects the greedy action 58% of the time, quantifying the knowing-doing gap."
- "RLFT on Gemma2 2B increases action coverage by +12% (from ∼40% to ∼52%) after 30K updates, directly mitigating greediness."
- "RLFT elevates Gemma2 2B's Tic-tac-toe win-rate against a random agent from 0.15 to 0.75 and enables drawing against optimal MCTS (return −0.95 → 0.0)."
---

# LLMs are Greedy Agents: Effects of RL Fine-tuning on Decision-Making Abilities

> [!tip] 核心洞察
> LLMs' decision-making failures are rooted in behavioral biases (greediness, frequency bias) that prevent effective exploration; RL fine-tuning can teach LLMs to value exploration and transform knowledge into action, evidenced by increased action coverage, reduced regret, and a narrowed knowing-doing gap.

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 大语言模型是贪婪的智能体：强化学习微调对决策能力的影响 |
| 英文题名 | LLMs are Greedy Agents: Effects of RL Fine-tuning on Decision-Making Abilities |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=weUP6H5Ko9) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | RLFT (Reinforcement Learning Fine-Tuning on self-generated CoT rationales) |
| Dataset | Tic-tac-toe vs Random Agent, Tic-tac-toe vs MCTS (optimal), Gaussian MABs (button, 10 arms, medium noise), 10 arms) |

> [!tip] 效果简介
> - Tic-tac-toe vs Random Agent 上，Average Return (win-rate) 为 0.75 (RLFT)，对比 0.15 (ICL)，变化 +0.60。
> - Tic-tac-toe vs MCTS (optimal) 上，Average Return 为 0.0 (RLFT, draws)，对比 −0.95 (ICL, loses)，变化 +0.95。
> - Gaussian MABs (button, 10 arms, medium noise) 上，Action Coverage 为 52% (2B after 30K RLFT steps)，对比 40% (2B without RLFT)，变化 +12 percentage points。

## 概述

**核心瓶颈**：在大语言模型（LLM）被用作决策智能体时，普遍表现出三种行为偏差——**贪婪性**（过早锁定少量高奖励动作，导致高达55%的动作空间从未被探索）、**频率偏差**（机械重复历史高频动作，与奖励信号脱钩）和**知行差距**（能生成正确推理但无法转化为正确行动）。其中，贪婪性是导致次优探索的根本原因。

**因果调节变量**：以自生成的思维链（Chain-of-Thought, CoT）推理为媒介，采用带KL约束的PPO算法进行强化学习微调（Reinforcement Learning Fine-Tuning, RLFT），直接作用于模型的探索行为与知识-行动转化。

**核心洞见**：LLM的决策失败并非源于能力缺失，而是源于行为偏差对有效探索的抑制；RL微调能够教会模型“重视探索”并“将知识转化为行动”，具体表现为动作覆盖率提升、累积遗憾下降以及知行差距收窄。

**方法定位**：本研究提出的RLFT方法属于**基于环境奖励的在线微调范式**，区别于冻结模型的上下文学习（ICL）和基于专家数据的监督微调（SFT）。其技术谱系可追溯至RLHF的约束REINFORCE估计器，但将优化目标从人类偏好奖励替换为环境交互奖励，并在动作生成中强制嵌入结构化CoT推理。在知识库中的定位为：**面向LLM智能体决策偏差的矫正方法**，与经典探索机制（如ϵ-greedy、UCB）和LLM原生策略（如自一致性）形成互补。

**关键实证结论**（高置信度）：
- Gemma2 2B在10臂赌博机中仅覆盖40%的动作，27B覆盖65%，去除CoT后所有模型仅覆盖约25%（Figure 3）。
- Gemma2 27B生成87%的正确UCB推理，却在58%的情况下选择贪婪动作（Figure 5）。
- RLFT使Gemma2 2B的动作覆盖率从约40%提升至约52%（30K更新步后），并在井字棋中将随机对手胜率从0.15提升至0.75，对最优MCTS对手从平均回报−0.95提升至0.0（平局）（Figure 7, Figure 9a）。
- 在RLFT中加入探索奖励（+1给未尝试动作），动作覆盖率从50%进一步提升至70%（Figure 8）。

**局限与待验证边界**：当前实验限于中小规模模型（2B–27B）和简单环境（赌博机、井字棋），向更大规模模型和复杂状态化任务的迁移性尚未验证。非单调的规模效应（如Qwen-2.5 7B表现优于14B）和RLFT无法完全消除的频率偏差表明，当前架构存在根本性限制。知行差距的完全闭合仍是开放问题。

## 背景与动机

### 大语言模型作为决策智能体

将大语言模型（LLM）从文本生成器转变为能够在真实环境中行动的自主智能体，是当前人工智能研究的前沿方向。在这一范式下，LLM 需要在多步交互中持续做出决策——从选择哪个按钮以获得最高奖励，到在棋盘上落子以赢得对局。然而，现有研究表明，预训练 LLM 在面对此类序列决策任务时，往往表现出系统性的行为偏差，而非理性的探索-利用平衡。

### 三个核心失败模式

本文通过对 Gemma2、Llama3、Qwen2.5 三个模型家族的系统性诊断，揭示了 LLM 在决策场景中普遍存在的三种失败模式：

**贪婪性（Greediness）** 是最为普遍且影响最深远的偏差。模型在获得少量正反馈后，会过早地将选择锁定在极少数已尝试过的动作上，停止探索剩余的动作空间。在 10 臂赌博机场景中，Gemma2 2B 仅覆盖约 40% 的动作，27B 覆盖约 65%，而在移除思维链（CoT）提示后，所有模型的覆盖率骤降至约 25%（Figure 3, Section 4.2）。这意味着高达 55% 的动作空间从未被探索，模型在信息严重不足的情况下做出次优决策。

**频率偏差（Frequency Bias）** 表现为模型机械地重复上下文中出现频率最高的动作，而忽视该动作的实际奖励信号。Gemma2 2B 在低重复窗口中，频繁动作的比例高达 70%（Figure 19, Section 4.3）。这种偏差使得模型的行为被历史序列的统计特征而非奖励反馈所驱动。

**知行鸿沟（Knowing-Doing Gap）** 揭示了模型“知道该做什么”与“实际做了什么”之间的断裂。当 Gemma2 27B 被明确指示像 UCB 算法一样行动时，它生成了 87% 的正确推理链，但在 58% 的情况下仍然选择了贪婪动作（Figure 5, Section 4.2）。模型在推理层面理解了最优策略，却无法将其转化为实际行动。

### 现有方法的局限

传统的强化学习探索机制（如 ϵ-greedy、UCB）在数值环境中表现良好，但难以直接迁移到基于文本的 LLM 决策框架中。现有的 LLM 对齐方法（如 RLHF）主要关注单步回答的质量和对齐，并未针对多步决策中的探索-利用权衡进行优化。而仅依赖上下文学习（ICL）的 LLM 智能体，虽然可以通过 CoT 提示获得一定的推理能力，但上述三种行为偏差仍然根深蒂固。

### 本文动机

上述发现指向一个核心问题：**LLM 的决策失败根植于其预训练过程中形成的行为偏差，而非推理能力的缺失。** 因此，本文提出通过强化学习微调（RLFT），让 LLM 在与环境交互的过程中，基于自生成的思维链推理和实际环境奖励进行策略优化。核心假设是：RLFT 能够教会模型为探索行为赋予价值，从而将“知道”转化为“做到”——缩小知行鸿沟，克服贪婪性和频率偏差，最终提升决策质量。

## 核心创新

### 问题诊断：LLM 决策中的三种行为偏差

本研究首先系统性地诊断了预训练大语言模型在序列决策任务中表现不佳的根因，识别出三种普遍存在的行为偏差：

1. **贪婪性（Greediness）**：模型过早锁定少数高奖励动作，停止探索。在10臂高斯赌博机中，Gemma2 2B 仅覆盖约40%的动作空间，即使最大规模的27B模型也仅覆盖65%；去除思维链后，所有模型的覆盖率骤降至25%。当臂数增加到20时，最大模型的覆盖率进一步下降至45%，表明贪婪性随动作空间增大而加剧。

2. **频率偏差（Frequency Bias）**：模型倾向于重复上下文中出现频率最高的动作，而非基于奖励进行理性选择。Gemma2 2B 表现出极端的频率依赖——频繁动作占比高达96%；而27B模型虽能克服频率偏差（频繁动作占比降至14%），却因此变得更加贪婪。

3. **知行差距（Knowing-Doing Gap）**：模型在推理层面“知道”正确策略，但在行动层面无法执行。Gemma2 27B 生成的87%的思维链推理是正确的（正确计算UCB值并识别最优臂），但在推理正确的情况下仍有58%的概率选择贪婪动作而非最优动作。

这三种偏差中，**贪婪性是最普遍且危害最大的失败模式**，是导致次优探索的根本原因。

### 核心方法：基于自生成思维链的强化学习微调（RLFT）

针对上述偏差，论文提出 **RLFT（Reinforcement Learning Fine-Tuning）**——在自生成的思维链（CoT）推理上进行强化学习微调。其关键创新体现在以下四个维度的改变：

| 改变维度 | 基线方案 | RLFT 方案 |
|---------|---------|----------|
| **微调方法** | 冻结LLM + CoT上下文学习（ICL） | 在自生成CoT推理上使用PPO-clip + KL散度约束进行在线RL微调 |
| **探索机制** | 无显式探索策略（仅依赖CoT的隐式探索） | 可叠加探索奖励（未尝试动作+1）、ε-greedy、try-all等机制 |
| **动作生成格式** | 非结构化动作预测（可能产生无效输出） | 结构化CoT生成 + 正则表达式提取动作，通过奖励塑形（无效动作惩罚−5）强制模板遵循 |
| **训练信号** | 无训练或基于专家数据的监督微调（SFT） | 环境奖励直接作为优化信号，通过PPO进行策略梯度优化 |

**RLFT 的核心机制**：模型在每一步接收任务指令、输出指令和近期交互历史，自回归生成推理词元和动作词元 $z_t = [z_t^{CoT}; a_t]$，然后通过正则表达式提取有效动作并与环境交互获取奖励。优化目标采用带裁剪的PPO目标，并附加对冻结参考策略的KL散度惩罚：

$$\max_\theta \mathbb{E}_{(c,z)\sim\mathcal{D}} \left[ \min\left( \frac{\pi_\theta(z|c)}{\pi_{\theta_{old}}(z|c)} A_{adv}, \mathrm{clip}_\epsilon\left( \frac{\pi_\theta(z|c)}{\pi_{\theta_{old}}(z|c)} \right) A_{adv} \right) - \beta D_{KL}(\pi_\theta(\cdot|c) || \pi_{ref}(\cdot|c)) \right]$$

### 创新效果：从知识到行动的转化

RLFT 的核心价值在于**教会LLM将“知道”转化为“做到”**，具体表现为：

- **直接缓解贪婪性**：Gemma2 2B 经过30K步RLFT后，动作覆盖率从约40%提升至约52%（+12个百分点），且覆盖率在训练过程中呈现先降后升的动态，表明模型在RL训练后期学会了探索的价值。
- **部分抵消频率偏差**：在低重复窗口（0-10次），频繁动作占比从70%降至35%，其他动作占比从8%升至35%，但高重复窗口下的频率偏差仍存残余。
- **显著缩小知行差距**：在井字棋任务中，RLFT将Gemma2 2B对随机智能体的胜率从0.15提升至0.75，对最优MCTS智能体的平均回报从−0.95（几乎全败）提升至0.0（全部平局），实现了从“知道规则但无法赢棋”到“稳定不败”的跨越。
- **探索奖励的叠加效应**：在RLFT中加入简单探索奖励（未尝试动作+1），可将动作覆盖率从50%进一步提升至70%，并降低累积遗憾。

### 与基线方法的关键区别

- **vs. ICL（上下文学习）**：ICL 依赖冻结模型的一次性推理，虽能通过CoT产生一定探索行为，但无法从根本上克服贪婪性和频率偏差。RLFT 通过在线交互反馈持续优化策略，使模型学会“探索是有价值的”。
- **vs. SFT（监督微调）**：在专家数据（UCB）上进行行为克隆可达到与UCB相近的遗憾，但需要预先获取专家策略，且无法泛化至无专家数据的环境。RLFT 仅需环境奖励信号，具有更强的通用性。
- **vs. 经典探索机制**：ε-greedy、try-all等机制在冻结模型上效果有限，但与RLFT结合时能产生协同效应——try-all初始策略（每个动作先试一次）在所有探索机制中带来最大的性能提升。

### 局限与待验证点

- 研究限于中小规模模型（2B–27B），在更大规模前沿模型上的效果尚待验证。
- 实验环境为简单赌博机和井字棋，向复杂状态化RL任务的迁移性未测试。
- 知行差距未完全消除——RLFT后模型仍偶有贪婪选择。
- 非单调缩放现象（如Qwen-2.5 7B > 14B）提示预训练因素对探索行为有复杂影响，机制尚不明确。

## 整体框架

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_weUP6H5Ko9/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of our Reinforcement Learning Fine Tuning (RLFT) pipeline. We fine-tune a pre-trained LLM πθ via self-generated Chain-of-Thought (CoT) rationales on environment rewards*

本文提出的**RLFT（Reinforcement Learning Fine-Tuning）**流水线，核心思路是在预训练大语言模型上进行强化学习微调，微调信号来自模型**自生成的思维链（Chain-of-Thought, CoT）推理**与环境交互获得的奖励。整个流水线由五个关键模块串联构成，形成“编码—推理—提取—塑形—优化”的闭环。

### 输入编码：Context Encoder

每个交互步骤 $t$，Context Encoder 将三类信息拼接为输入 token 序列 $c_t$：
- **任务指令** $c_t^{in}$：描述当前决策问题的规则与目标；
- **输出指令** $c_t^{out}$：规定模型应先生成推理过程，再输出具体动作；
- **近期交互历史** $c_t^{\tau_{t-C:t}}$：包含最近 $C$ 步的状态、动作与奖励记录。

这种结构化上下文表示（Figure 2 展示了 Button MAB 场景下的具体模板）为后续的 CoT 推理提供了完整的情境信息。

### 推理与动作生成：CoT & Action Generator

模型在每一步自回归生成动作 token 序列 $z_t = [z_t^{CoT}; a_t]$，其中：
- $z_t^{CoT}$ 为思维链推理 token，承载模型对当前局面与历史信息的分析；
- $a_t$ 为最终输出的动作。

这种“先推理后行动”的生成方式，是 RLFT 能够利用 CoT 进行探索性决策的结构基础。

### 动作提取与格式约束：Action Extractor + Reward Shaper

由于自回归生成可能产出无效动作，流水线引入了一个基于正则表达式的 **Action Extractor**，从 $z_t$ 中提取合法动作。若提取失败，则执行一个随机动作作为安全回退。

为抑制无效输出，**Reward Shaper** 对无效动作施加 $-5$ 的奖励惩罚。这一奖励塑形机制促使模型学习遵守输出模板，确保训练信号的可靠性。实验表明，各模型的无效动作率均低于 3.2%，未对结果造成系统性偏差。

### 策略优化：PPO-based Fine-Tuner

RLFT 的核心优化模块采用 PPO 裁剪目标，并额外引入对冻结参考策略 $\pi_{ref}$ 的 KL 散度惩罚项：

$$\max_{\theta} \mathbb{E}_{(c,z) \sim \mathcal{D}} \left[ \min\left( \frac{\pi_{\theta}(z|c)}{\pi_{\theta_{old}}(z|c)} A_{adv}, \operatorname{clip}_{\epsilon}\left( \frac{\pi_{\theta}(z|c)}{\pi_{\theta_{old}}(z|c)} \right) A_{adv} \right) - \beta D_{KL}(\pi_{\theta}(\cdot|c) || \pi_{ref}(\cdot|c)) \right]$$

其中 $A_{adv}$ 为优势估计，$\beta$ 控制 KL 惩罚强度。这一目标在鼓励策略改进的同时，防止模型偏离预训练分布过远。训练使用自生成 CoT 推理与环境奖励作为信号，无需外部专家数据。

### 与基线的关键差异

相较于不进行微调的 **ICL（In-Context Learning）** 基线，RLFT 在四个维度上引入了结构性改变：

| 维度 | ICL 基线 | RLFT 方案 |
|------|---------|----------|
| **微调方式** | 冻结模型，仅靠提示词引导 | 在自生成 CoT 推理上进行 PPO + KL 约束微调 |
| **探索机制** | 仅依赖 CoT 的隐式探索 | 可叠加探索奖励（+1 对未尝试动作）或启发式策略（ϵ-greedy、try-all） |
| **动作格式** | 非结构化预测，可能产出无效输出 | 结构化 CoT + 正则提取，辅以 −5 惩罚强制模板遵循 |
| **训练信号** | 无训练 | 环境奖励 + 奖励塑形，通过 PPO 优化 |

Figure 1 以架构图形式完整展示了这一流水线：从上下文构建到 CoT 生成，再到奖励塑形与 PPO 优化的闭环流程。

## 核心模块与公式推导

RLFT 方法将决策任务形式化为一个**上下文条件化的自回归生成问题**，并通过强化学习对预训练大语言模型进行微调。其技术架构由五个核心模块串联构成，围绕一个带 KL 约束的 PPO 裁剪目标进行优化。

### 上下文编码器

在每一个交互步骤 $t$，模型接收的输入 token 序列 $c_t$ 由三部分拼接而成：**输入指令** $c_t^{in}$（描述任务规则与目标）、**输出指令** $c_t^{out}$（规定 CoT 推理与动作的输出格式），以及**最近的交互历史** $c_t^{\tau_{t-C:t}}$（包含过去 $C$ 步的动作与奖励记录）。这一结构化的上下文表示确保模型能够基于环境反馈进行条件化推理。

### CoT 与动作生成器

模型以自回归方式生成动作 token 序列 $z_t = [z_t^{CoT}; a_t]$，其中 $z_t^{CoT}$ 为思维链推理 token，$a_t$ 为最终执行的动作。这种分解将“推理”与“决策”统一在同一个生成过程中，使得探索行为可以通过 CoT 中的策略性推理自然涌现，而非依赖外部探索机制。

### 动作提取器与奖励整形器

由于自回归生成可能产生不符合格式要求的输出，系统使用**正则表达式**从生成 token 中提取有效动作。若提取失败，则执行随机动作并施加 **−5 的奖励惩罚**，以此激励模型遵守输出模板。这一奖励整形机制对保证训练稳定性至关重要。

### PPO 微调器与核心优化目标

RLFT 的核心优化目标是一个带 KL 约束的 PPO 裁剪损失函数：

$$
\begin{aligned}
\max_{\theta} \mathbb{E}_{(c,z) \sim \mathcal{D}} \Big[ \min \Big( & \frac{\pi_{\theta}(z|c)}{\pi_{\theta_{old}}(z|c)} A_{adv}, \\
& \text{clip}_{\epsilon}\Big(\frac{\pi_{\theta}(z|c)}{\pi_{\theta_{old}}(z|c)}\Big) A_{adv} \Big) \\
& - \beta D_{KL}\big(\pi_{\theta}(\cdot|c) \| \pi_{ref}(\cdot|c)\big) \Big]
\end{aligned}
$$

其中各变量含义如下：
- $\pi_{\theta}$：当前待优化的策略（即微调中的 LLM）；
- $\pi_{\theta_{old}}$：更新前的旧策略，用于计算重要性采样比率；
- $\pi_{ref}$：冻结的参考策略（预训练模型），KL 散度约束防止策略偏离过远；
- $A_{adv}$：优势函数，基于环境奖励计算；
- $\text{clip}_{\epsilon}$：裁剪函数，将比率限制在 $[1-\epsilon, 1+\epsilon]$ 区间内，防止更新步长过大；
- $\beta$：KL 惩罚系数，控制策略与参考策略的接近程度。

该目标函数的本质是：在限制策略突变幅度（裁剪项）和防止灾难性遗忘（KL 约束项）的双重约束下，最大化模型生成高优势动作序列的概率。与标准 RLHF 中使用的约束 REINFORCE 估计器不同，RLFT 直接采用 PPO 的裁剪机制，更适合多步交互场景中的信用分配。

### 方法谱系与知识库定位

RLFT 位于**LLM 决策智能体**与**强化学习微调**的交汇点。与传统方法相比，其关键差异体现在四个维度：

| 方法维度 | 基线方案 | RLFT 方案 |
|---------|---------|----------|
| 微调方式 | 冻结 LLM + CoT 上下文学习（ICL） | 基于自生成 CoT 的 PPO 强化学习微调 |
| 探索机制 | 无显式探索策略（仅依赖 CoT 的隐式探索） | 可通过探索奖励（+1 奖励给未尝试动作）或启发式策略（ϵ-greedy、try-all）增强 |
| 动作生成格式 | 非结构化动作预测（可能产生无效输出） | 结构化 CoT 生成 + 正则表达式提取，配合 −5 惩罚强制格式合规 |
| 训练信号 | 专家数据监督微调（SFT）或无训练 | 环境奖励 + 奖励整形，通过 PPO 优化 |

在基线方法层面，论文将 RLFT 与三类方案对比：**UCB**（Auer, 2002）作为最优算法上界，**随机智能体**作为性能下界，**ICL**（冻结 LLM + CoT 提示但无微调）作为直接对照。实验表明，SFT 在专家数据上可达到与 UCB 相当的后悔值，但 RLFT 在无需专家数据的情况下实现了更强的跨任务泛化能力。

## 实验与分析

### 核心发现：LLM决策的三种失败模式

在分析RLFT的效果之前，论文首先系统性地揭示了预训练LLM在决策场景中的三种普遍失败模式，这些模式构成了性能瓶颈的根源。

**贪婪性（Greediness）**是最普遍且最根本的问题。LLM倾向于过早地锁定一小部分动作，导致大量动作空间从未被探索。在10臂高斯MAB任务中，Gemma2 2B仅覆盖约40%的动作，9B和27B覆盖约65%（即约6.5个动作），仍有35%的动作从未被尝试。当移除Chain-of-Thought推理后，所有模型的覆盖率骤降至约25%（Figure 3, Section 4.2）。将臂数增加到20时，贪婪性更加严重，最大模型也仅覆盖45%的动作空间。这一现象在Gemma2、Llama3和Qwen2.5三个模型家族中均被观察到，表明贪婪性是跨模型架构的普遍问题。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_weUP6H5Ko9/figures/003_Figure_3.jpg]]
*Figure 3: (a) Action Coverage: 10 arms*

**频率偏差（Frequency Bias）**表现为模型倾向于重复上下文中出现频率最高的动作，而非选择奖励最高的动作。Gemma2 2B严重受频率偏差影响：当某个动作在上下文中重复出现时，选择该动作的概率极高（F_f达96%），动作熵随重复次数增加而显著下降。相比之下，27B模型能够克服频率偏差（F_f仅14%），但代价是变得更加贪婪——它更倾向于锁定当前奖励最高的动作（Figure 4, Section 4.2）。

**知行差距（Knowing-Doing Gap）**是三种模式中最隐蔽的失败形式。以Gemma2 27B为例，该模型在87%的情况下能够生成正确的UCB推理（即“知道”最优策略），但在推理正确时仍有58%的概率选择贪婪动作而非UCB指示的最优动作（Figure 5, Section 4.2）。这说明模型拥有解决任务的知识，却无法将其转化为正确的行为。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_weUP6H5Ko9/figures/009_Figure_5.jpg]]
*Figure 5: Confusion matrix for the knowingdoing gap of Gemma2 27B. The agent “knows” how to solve the task (87% correct rationales, sum of top row), but fails at "doing" (58% greedy actions among correct rationales). See Figure 26 for the CoT instructions and an agent response*

### RLFT的主实验结果

RLFT在多个环境中展现了显著的性能提升，其效果通过以下关键指标得到验证。

**高斯MAB任务**：在中等噪声（σ=1）的10臂设置下，RLFT训练的Gemma2 2B累积遗憾显著低于未微调的ICL基线，并逐步接近UCB最优算法的性能上界。RLFT对9B模型同样有效，在5臂、10臂和20臂设置下均降低了累积遗憾（Figure 6, Section 4.3）。在高噪声（σ=3）和低噪声（σ=0.1）设置下，RLFT的优势同样保持（Figure 20, Appendix）。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_weUP6H5Ko9/figures/010_Figure_6.jpg]]
*Figure 6: Main Comparison on Gaussian MABs button scenario in the medium noise (σ = 1) setting. We compare cumulative regrets (lower is better) of classic baselines against ICL and RLFT performances for 5, 10, and 20 arms. See Figure 20 for $\sigma$ = 0 . 1 and $\sigma$ = 3

**动作覆盖率**：RLFT直接缓解了贪婪性。Gemma2 2B在30K步RLFT训练后，动作覆盖率从约40%提升至约52%（+12个百分点）。值得注意的是，覆盖率在训练初期先下降后上升，表明RLFT需要一定步数才能学会探索的价值（Figure 7, Section 4.3）。

**Tic-tac-toe任务**：RLFT的效果在需要策略性推理的棋盘游戏中更为显著。对随机对手，RLFT将Gemma2 2B的平均回报从0.15提升至0.75（胜率大幅提高）；对最优MCTS对手，RLFT使模型从几乎全败（回报−0.95）提升至能够逼平（回报0.0），这意味着模型学会了Tic-tac-toe的最优防御策略（Figure 9a, Section 4.5）。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_weUP6H5Ko9/figures/015_Figure_9.jpg]]
*Figure 9: Ablations. (a) Effect of RLFT in Tic-tac-toe from Ruoss et al. (2024). (b) Effect of CoT on ICL, RLFT and SFT (expert data) performance on MABs. (c) Effect of increasing the number of "thinking" tokens to generate during RLFT*

**频率偏差的缓解**：RLFT部分抵消了频率偏差。在低重复窗口（0-10次重复）中，高频动作的比例从70%降至35%，其他动作的比例从8%升至35%。但在高重复窗口（40-50次），频率偏差仍然较高，说明RLFT未能完全消除这一偏差（Figure 19, Section 4.3）。

### 探索机制的影响

论文在RLFT框架内测试了多种探索机制，以进一步缓解贪婪性（Figure 8, Section 4.4）。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_weUP6H5Ko9/figures/012_Figure_8.jpg]]
*Figure 8: Effect of exploration mechanisms on action coverage and cumulative regret*

**探索奖励（Exploration Bonus）**是最简单且最有效的机制。在RLFT过程中对未尝试过的动作给予+1额外奖励，使动作覆盖率从50%提升至70%，同时降低了累积遗憾。这表明显式的探索激励信号能够有效引导LLM突破贪婪行为。

**尝试所有动作（Try-all）**策略——在交互初期依次尝试每个动作一次——带来了所有探索机制中最大的性能提升。这一发现说明，在RLFT的早期阶段注入结构化的探索行为对后续学习至关重要。

**ϵ-贪婪（ϵ-greedy）**和**自一致性（Self-consistency）**等机制也表现出一定效果，但不如探索奖励和try-all策略显著。上下文随机化（context randomization）的效果相对有限。

### 关键消融实验

**CoT推理的必要性**：移除CoT推理对RLFT是致命的。在MAB任务中，无CoT的RLFT性能甚至低于有CoT的ICL基线，说明RLFT的探索能力高度依赖于CoT推理过程中产生的结构化思考（Figure 9b, Section 4.5/Appendix D.3）。

**思考时间的影响**：增加生成预算G（即允许模型生成更多推理token）持续提升性能。将G从256增至512时，Gemma2 2B的RLFT性能达到与9B RLFT相当的水平。反之，将G降至16或64会导致性能急剧下降，累积遗憾呈线性增长（Figure 9c, Appendix D.5）。这一发现表明LLM智能体从额外的“思考时间”中获益。

**监督微调（SFT）对比**：使用UCB专家数据进行行为克隆（BC）或轨迹条件（TC）监督微调，在MAB任务上可以达到与UCB本身相当的遗憾水平（Figure 9b, Appendix D.4）。这验证了专家数据蒸馏在简单决策任务中的有效性，但RLFT的优势在于无需预收集专家数据。

**合法动作信息的重要性**：在Tic-tac-toe任务中，从上下文中移除合法动作列表导致平均回报从0.75骤降至0.45（Figure 25, Appendix D.2），说明结构化环境信息对LLM决策至关重要。

### 跨模型家族与扩展性

论文在三个模型家族上验证了发现的鲁棒性。Gemma2、Llama3和Qwen2.5均表现出类似的贪婪性模式，但存在一些值得注意的差异。Qwen-2.5出现了非单调缩放现象：7B模型的动作覆盖率高于14B模型，暗示预训练差异会影响探索行为。此外，所有模型的无效动作率均低于3.2%（Table 2），排除了输出格式错误对结果的系统性偏差。

### 默认超参数配置

所有实验遵循统一的超参数设置（Table 1）。训练采用30K更新步数，累积批次大小为128，优化器为AdaFactor，学习率调度采用线性预热加余弦衰减（范围1e-4至1e-6）。上下文窗口为1792 tokens，生成预算G默认为256 tokens。RLFT使用PPO+KL损失，以蒙特卡洛回报作为基线，KL惩罚系数β=0.04。训练硬件为4块H100 GPU，总训练时间约24小时（2B模型）。多步token生成是训练成本的主要来源——典型配置下，每轮rollout需生成50步×256 tokens=12.8K tokens。

## 方法谱系与知识库定位

### 方法在决策智能体谱系中的位置

本研究提出的 **RLFT (Reinforcement Learning Fine-Tuning)** 位于三个研究传统的交汇处：经典多臂老虎机探索策略、LLM 智能体的上下文学习范式、以及基于人类反馈的强化学习微调技术。

**与经典探索算法的关系。** 论文以 **UCB** (Auer, 2002) 作为最优性能上界，以随机智能体作为下界。RLFT 的核心目标并非替代 UCB 等理论最优算法，而是教会 LLM 自发地产生类似探索行为。实验表明，监督微调（BC/TC）在专家 UCB 数据上可以达到与 UCB 相当的 regret（Figure 9b），这验证了 UCB 策略的可学习性；而 RLFT 则通过环境奖励信号，使模型在没有专家演示的情况下习得探索能力。

**与 ICL 基线的对比。** 论文的基线方法是带 CoT 提示的上下文学习（ICL），即冻结的预训练 LLM 通过提示词进行推理和决策。ICL 基线暴露了三个核心失败模式——贪婪性、频率偏差和知行差距——RLFT 正是针对这些缺陷设计的。与 ICL 相比，RLFT 的关键差异在于：
- **训练信号**：从零训练变为 PPO 驱动的环境奖励优化（Equation 2），而非依赖冻结的预训练权重；
- **探索机制**：从 CoT 推理隐含的弱探索，变为可通过奖励塑形（探索奖励 +1）显式增强的探索；
- **输出格式**：通过正则表达式提取动作和 -5 的无效动作惩罚，强制模型遵循结构化输出模板。

**与 RLHF 的技术关联。** RLFT 的优化目标直接继承自 RLHF 的约束 REINFORCE 估计器（Equation 1），使用 PPO-clip 目标并附加对冻结参考策略的 KL 散度惩罚（Equation 2）。关键区别在于：RLHF 依赖人类偏好训练的奖励模型 $r_\phi$，而 RLFT 的奖励直接来自环境交互——这在多步决策场景中更自然，但也带来了信用分配和探索-利用权衡的新挑战。

### 适用边界与局限

**模型规模边界。** 实验覆盖 Gemma2 2B/9B/27B、Llama3 和 Qwen2.5 系列，但未测试 100B+ 的前沿模型。Qwen-2.5 系列中观察到的非单调缩放（7B 在动作覆盖率上优于 14B）提示，预训练语料和架构差异可能比模型规模本身对探索行为的影响更大，这一发现需要更大规模验证。

**环境复杂度边界。** 所有实验局限于两类简单环境：
- 无状态赌博机（高斯 MAB、MovieLens 上下文赌博机），交互步长 50–100 步；
- 完全可观测的井字棋（Tic-tac-toe），状态空间有限。

论文未测试部分可观测环境、需要目标导向探索的复杂 RL 任务（如导航、工具使用），也未涉及需要子语言推理的任务。CoT 推理是 RLFT 有效的关键前提（移除 CoT 后性能降至 ICL 以下），这意味着该方法不适用于纯直觉或感知-运动类决策。

**训练成本边界。** RLFT 的计算开销随生成预算线性增长：以 50 步 × 512 tokens = 25K tokens 的单次 rollout 为例，多步 token 生成可能主导训练时间。论文未提供与 SFT 或其他微调范式的训练效率对比。

**偏差消除的局限性。** RLFT 缓解但未根除三类偏差：
- 贪婪性：动作覆盖率从 40% 提升至 52%（+12 个百分点），但仍有近一半动作空间未被探索；
- 频率偏差：低频重复窗口的频繁动作比例从 70% 降至 35%，但高重复窗口下仍居高不下；
- 知行差距：即使 RLFT 后，模型仍会在某些情况下选择贪婪动作。

### 开放问题

1. **规模泛化性**：当前发现能否迁移到 100B+ 的前沿模型？更大模型的贪婪性和频率偏差模式是加剧还是缓解？
2. **环境迁移性**：习得的探索能力能否泛化到未见过的臂数、奖励分布或完全不同的任务结构？
3. **目标导向探索**：当前探索机制（探索奖励、try-all、ϵ-greedy）均为启发式，如何设计使 LLM 智能体在需要定向探索（如稀疏奖励导航）的环境中有效？
4. **知行差距的本质**：在部分可观测或状态化环境中，知行差距如何表现？其根源是架构限制、预训练偏差，还是优化目标的不匹配？
5. **计算效率**：现代循环架构或记忆机制能否降低长思考时间 rollout 的计算成本，使 RLFT 在更大规模上可行？
6. **非单调缩放的成因**：Qwen-2.5 7B > 14B 的现象是否与特定预训练数据分布、指令微调策略或架构选择有关？
7. **奖励塑形设计空间**：是否存在更优的奖励塑形或探索奖励设计，能够在不引入额外偏差的情况下完全克服贪婪性和频率偏差？

## 原文 PDF

![[paperPDFs/ICLR_2026/LLMs_are_Greedy_Agents_Effects_of_RL_Fine_tuning_on_Decision_Making_Abilities.pdf]]
