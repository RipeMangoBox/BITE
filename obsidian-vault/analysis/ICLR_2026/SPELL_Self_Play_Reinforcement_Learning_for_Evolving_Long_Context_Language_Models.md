---
title: "SPELL: Self-Play Reinforcement Learning for Evolving Long-Context Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SPELL_Self_Play_Reinforcement_Learning_for_Evolving_Long_Context_Language_Models.pdf
project_link: null
code_link: https://github.com/Tongyi-Zhiwen/Qwen-Doc
openreview_forum_id: 83F6YF4Hz6
aliases:
- SPELL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "自我生成的问题难度与验证器提供的语义奖励信号，通过自动课程和角色协同持续调节训练难度。"
primary_logic: "单一模型在自对弈中扮演提问者、回答者和验证者三种角色，利用历史记忆和自动课程生成难度适中的多跳推理问题，并通过语义验证器提供可靠奖励，实现无监督的长上下文推理能力自我进化。"
claims:
- "SPELL在多个基座模型上带来一致且显著的性能提升，例如Qwen2.5‑7B在16K平均分上提高13.9分。"
- "SPELL在强模型Qwen3‑30B‑A3B‑Thinking上持续改善，而传统RLVR基线无增益甚至出现下降。"
- "测试时缩放性能显著增强：+SPELL的Qwen3‑30B‑A3B‑Thinking在pass@4上超越gemini‑2.5‑pro。"
- "消融实验证实提问者更新和历史记忆至关重要，移除历史记忆使平均分下降2.9分。"
---

# SPELL: Self-Play Reinforcement Learning for Evolving Long-Context Language Models

> [!tip] 核心洞察
> 单一模型在自对弈中扮演提问者、回答者和验证者三种角色，利用历史记忆和自动课程生成难度适中的多跳推理问题，并通过语义验证器提供可靠奖励，实现无监督的长上下文推理能力自我进化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SPELL：自对弈强化学习实现长上下文语言模型的自我进化 |
| 英文题名 | SPELL: Self-Play Reinforcement Learning for Evolving Long-Context Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=83F6YF4Hz6) · [GitHub](https://github.com/Tongyi-Zhiwen/Qwen-Doc) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | SPELL |
| Dataset | Overall Average (16K) on Qwen2.5‑7B, Overall Average (16K) on Qwen3‑30B‑A3B‑Thinking, Overall pass@8 on Qwen3‑30B‑A3B‑Thinking |

> [!tip] 效果简介
> - Overall Average (16K) on Qwen2.5‑7B 上，Avg Score 为 40.6，对比 26.7 (Base)，变化 +13.9。
> - Overall Average (16K) on Qwen3‑30B‑A3B‑Thinking 上，Avg Score 为 62.7，对比 60.7 (Base/RLVR)，变化 +2.0。
> - Overall pass@8 on Qwen3‑30B‑A3B‑Thinking 上，pass@8 为 74.5，对比 66.9 (Base)，变化 +7.6。

## 概要

### 问题瓶颈

长上下文推理任务面临一个根本性瓶颈：缺乏可靠的人类标注和可编程验证的奖励信号。传统强化学习（RL）方法依赖精确匹配或规则奖励，无法有效评估长文本中复杂多跳推理的语义正确性，导致模型难以在无监督条件下实现长上下文能力的持续进化。现有RLVR基线（Guo et al., 2025）使用静态合成数据训练，在强模型上几乎无增益甚至出现性能下降，进一步验证了这一瓶颈。

### 核心洞察

SPELL的核心洞察在于：**单一模型可以在自对弈中同时扮演提问者、回答者和验证者三种角色，通过历史记忆和自动课程生成难度适中的多跳推理问题，并利用语义验证器提供可靠奖励，实现长上下文推理能力的无监督自我进化。** 这一闭环互动创造了自动难度调节的课程学习机制——提问者基于历史记忆逐步生成更难的问题，验证者通过多数投票提供语义级别的奖励信号，回答者则持续从这些信号中学习改进。

### 方法定位

SPELL属于**自对弈强化学习**范式，与传统的RLVR、LongPO、SoLoPO等长上下文对齐方法有本质区别。传统方法依赖外部标注或静态合成数据，而SPELL通过角色协同实现训练数据的自主生成和难度自动调节。其关键创新在于：
- **三角色闭环**：提问者、回答者、验证者共享同一策略模型，通过角色特定奖励函数协同进化；
- **语义验证器**：通过多数投票机制判断回答与参考答案的语义等价性，与规则奖励取最大值，有效减少误判；
- **自动课程**：高斯奖励函数（$\mu=0.5, \sigma=0.5/3$）鼓励提问者生成难度适中的问题，历史记忆机制推动难度逐步提升。

### 主要结果

SPELL在多个基座模型上取得一致且显著的性能提升：
- **Qwen2.5‑7B**在16K平均分上从26.7提升至40.6（+13.9分）；
- **Qwen3‑30B‑A3B‑Thinking**在16K平均分上从60.7提升至62.7（+2.0分），而RLVR基线无增益（60.7）；
- 测试时缩放性能显著增强：+SPELL的Qwen3‑30B‑A3B‑Thinking在pass@4上超越gemini‑2.5‑pro，pass@8达到74.5（基座66.9，+7.6分）。

消融实验证实了各组件的关键作用：移除验证器导致平均分下降3.2分（DocMath下降6.4分），冻结提问者更新下降4.6分，去除历史记忆下降2.9分且问题难度变得不稳定。这些结果验证了三角色协同和语义验证器是SPELL性能增益的核心驱动力。



长上下文推理（Long-Context Reasoning）要求语言模型在海量文本中定位、关联并综合多跳信息，从而回答复杂问题。近年来，尽管大语言模型（LLM）在短文本任务上取得了显著进展，但在需要跨文档、跨段落进行深层推理的长上下文场景中，性能仍然受限。核心瓶颈在于：**长上下文推理任务缺乏可靠且可扩展的奖励信号**。人类标注长文档的多跳推理过程成本极高，且难以保证一致性；而基于规则的验证器（如精确匹配）在需要语义理解的开放域问答中几乎失效。这一瓶颈导致传统的强化学习（RL）方法难以在长上下文推理任务上有效扩展——模型无法获得密集、准确的反馈来指导自我改进。

现有工作主要依赖两类策略来缓解上述问题。第一类是**指令微调（Instruction Tuning）**，通过大量人工标注的长上下文问答数据来训练模型，但其扩展性受限于数据获取成本。第二类是**基于静态合成数据的强化学习（RLVR）**，例如使用 DeepSeek-R1 等强模型预先生成训练样本，再通过规则奖励进行优化。然而，**静态数据无法适应模型能力的动态变化**：随着训练推进，固定难度的问题要么过于简单（奖励饱和），要么过于困难（训练崩溃），导致优化信号与策略能力之间逐渐失配。对于强基座模型（如 Qwen3-30B-A3B-Thinking），RLVR 甚至可能带来性能退化——在 DocMath 和 LongBench-V2 上分别下降 0.2 和 1.2 分（Table 1），说明静态课程难以推动模型突破其能力边界。

上述困境揭示了一个根本性需求：**训练信号必须与模型当前能力同步演化**。换言之，模型需要一个能够自动调节难度的课程生成机制，以及一个能够提供语义层面可靠反馈的奖励来源。这构成了本文的核心动机——能否让模型在无外部监督的条件下，通过自我博弈持续生成难度适中的训练任务，并自主验证回答的正确性，从而实现长上下文推理能力的自我进化？



## 核心方法与创新机理

SPELL的核心创新在于将长上下文推理能力的获取，从依赖外部标注或静态合成数据的范式，转变为一个**模型自我驱动的闭环演化系统**。其关键突破并非单一算法组件的替换，而是通过**三角色自对弈机制**与**自动课程生成**的协同，解决了长上下文任务中监督信号匮乏的根本瓶颈。

### 1. 三角色自对弈：从静态数据到动态课程

传统强化学习（如RLVR基线）依赖预先生成的静态问题库，其难度分布与模型当前能力脱节，导致训练后期奖励信号饱和或失效。SPELL将单一策略模型同时赋予**提问者（Questioner）、回答者（Responder）和验证者（Verifier）**三种角色，构建了一个闭环的自对弈循环（Figure 2）：

- **提问者**基于长文档生成多跳推理问题，其核心创新在于引入了**历史记忆（History Memory）**。该记忆缓存了最近 $L=3$ 个可解的问题-答案对及对应文档，使提问者能够基于逐渐扩展的上下文生成更具挑战性的问题。消融实验证实，移除历史记忆导致平均分下降2.9分，且问题难度变得不稳定（Table 2, Figure 4）。
- **回答者**在完整长文档上探索多条推理轨迹，其奖励信号由规则匹配与验证器共识共同决定。
- **验证者**通过多次采样和多数投票判断回答与参考答案的语义等价性，提供可靠的奖励信号。移除验证器使平均分下降3.2分，尤其在需要语义理解的DocMath上下降6.4分（Table 2）。

这一设计使得训练数据的难度能够**自适应地追踪模型当前的能力边界**，形成自动课程：提问者被激励生成回答者正确率约50%的问题（高斯奖励函数，$\mu=0.5, \sigma=0.5/3$），确保训练信号始终处于模型能力的“最近发展区”。

### 2. 关键机制改进

相较于基线方法，SPELL在以下关键槽位上进行了根本性改进：

| 改进槽位 | 基线做法 | SPELL做法 | 因果效应 |
|:---|:---|:---|:---|
| **提问者历史记忆** | 无记忆，仅基于新文档生成问题 | 缓存最近可解问题-答案对，逐步扩展上下文 | 移除后平均分−2.9，难度不稳定 |
| **提问者奖励函数** | 固定或无自适应奖励 | 高斯奖励函数 ($\mu=0.5, \sigma=0.5/3$)，鼓励中等难度，惩罚无依据/格式错误 | 默认$\sigma=0.5/3$取得最高平均分47.2 |
| **验证器集成** | 仅规则精确匹配 (CEM) | 语义多数投票验证器与规则奖励取最大值 | 移除验证器平均分−3.2，DocMath −6.4 |
| **角色特定动态采样** | 所有角色样本均衡使用 | 过滤低方差回答者组，平衡正负提问者样本，削减验证者样本量 | 防止验证器梯度主导训练 |

### 3. 统一策略更新的协同效应

SPELL将三个角色的GRPO目标联合优化（$\mathcal{J}_{\mathrm{GRPO}}(\theta) = \mathcal{J}^{\mathrm{que}}_{\mathrm{GRPO}}(\theta) + \mathcal{J}^{\mathrm{res}}_{\mathrm{GRPO}}(\theta) + \mathcal{J}^{\mathrm{ver}}_{\mathrm{GRPO}}(\theta)$），使得模型在提问、回答、验证三个能力维度上同步进化。消融实验表明，冻结提问者更新导致平均分下降4.6分（Table 2），说明三角色协同更新是实现自我进化的必要条件——提问者能力的停滞将直接导致课程难度无法持续提升，进而限制回答者和验证者的进步空间。

这一协同机制在强基座模型上尤为关键：Qwen3‑30B‑A3B‑Thinking使用传统RLVR训练时性能无增益甚至下降，而SPELL仍能带来2.0分的平均提升（Table 1），表明自对弈课程能够为已具备强推理能力的模型提供有效的持续改进信号。



![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_83F6YF4Hz6/figures/003_Figure_1.jpg]]
*Figure 1: (Left) An overview of the SPELL framework, where a single LLM self-evolves by dynamically adopting the roles of questioner, responder, and verifier. (Right) SPELL consistently boosts performance across various models (top) and exhibits superior test-time scaling over traditional RLVR (bottom)*

SPELL 是一个基于自对弈强化学习的自进化框架，其核心设计是让**单一策略模型**在训练循环中动态扮演三个互补角色——提问者（Questioner）、回答者（Responder）和验证者（Verifier）——通过角色间的闭环交互生成训练信号，驱动模型持续自我提升（Figure 1 左，Figure 2）。

### 瓶颈与核心机制

长上下文推理任务面临一个关键瓶颈：缺乏可靠的人类标注和可编程验证的奖励信号，使得传统强化学习难以扩展。SPELL 通过两条因果链路突破这一限制：

1. **自我生成的问题难度调控**：提问者利用历史记忆和自动课程机制，生成难度适中的多跳推理问题，使训练信号始终处于模型能力边界附近。
2. **语义验证器提供的可靠奖励**：验证器通过多数投票判断回答与参考答案的语义等价性，与规则奖励取最大值，有效减少误判，为无监督训练提供稳定梯度。

### 三角色自对弈循环

框架以两阶段循环运行（Figure 2）：

**阶段一：角色特定采样（Role-Specific Rollout）**

- **提问者**（$\pi_\theta^{\text{que}}$）：基于新采样的文档子集 $C_{\text{new}}$ 和历史记忆 $H_C$（包含最近 $L=3$ 个可解问题-答案对及对应文档），生成多跳推理问题及参考答案。通过**接地过滤器**（Grounding Filter）丢弃无需文档即可回答的问题，确保上下文依赖性。
- **回答者**（$\pi_\theta^{\text{res}}$）：阅读完整长文档，对每个问题生成 $G$ 条独立回答轨迹，探索多样化解题路径。
- **验证者**（$\pi_\theta^{\text{ver}}$）：对每条回答进行 $G$ 次独立语义等价判断，通过多数投票聚合为二元奖励信号 $v_i^{\text{ver}}$。

**阶段二：统一策略更新（Unified Policy Update）**

收集三个角色的所有轨迹后，通过**角色特定动态采样**（Role-Specific Dynamic Sampling）平衡样本：仅保留奖励方差非零的回答者组、平衡正负提问者样本、削减验证者样本量，防止验证器梯度主导训练。最终联合优化三个角色的 GRPO 目标：

$$\mathcal{J}_{\text{GRPO}}(\theta) = \mathcal{J}_{\text{GRPO}}^{\text{que}}(\theta) + \mathcal{J}_{\text{GRPO}}^{\text{res}}(\theta) + \mathcal{J}_{\text{GRPO}}^{\text{ver}}(\theta)$$

更新后的策略模型直接用于下一轮迭代的所有角色，形成持续进化的闭环。

### 奖励设计的关键创新

**回答者奖励**取规则精确匹配（CEM）与验证器共识分数的最大值：

$$r_i^{\text{res}} = \max\left(\mathcal{R}_{\text{rule}}(y_i, a),\; v_i^{\text{ver}}\right)$$

这一设计防止语义正确但表述不同的回答被误判为错误。

**提问者奖励**采用以回答者正确率 $0.5$ 为中心的高斯函数（$\mu=0.5$，$\sigma=0.5/3$），鼓励生成难度适中的问题，并对无依据（$-0.5$）或格式错误（$-1$）的问题施加惩罚。消融实验证实，该配置取得最高平均分 47.2（Table 3）。

**验证者奖励**基于个体判断与多数票的一致性：$r_{i,j}^{\text{ver}} = \mathbb{I}(v_{i,j} = v_i^{\text{ver}})$，激励验证者输出稳定的共识判断。

### 历史记忆与自动课程

历史记忆 $H_C$ 是提问者持续提升问题难度的关键机制。通过缓存最近可解的问题-答案对和文档，提问者的上下文逐步扩展，形成自动课程。消融实验表明，移除历史记忆使平均分下降 2.9 分，且问题难度变得不稳定（Table 2，Figure 4 右）。冻结提问者更新则导致平均分下降 4.6 分，难度停滞不前（Table 2，Figure 4 中），证实提问者的自适应进化对维持有效训练信号至关重要。

### 输入输出流总结

| 模块 | 输入 | 输出 |
|------|------|------|
| 提问者 | 新文档 $C_{\text{new}}$ + 历史记忆 $H_C$ | 多跳推理问题 + 参考答案 |
| 回答者 | 完整长文档 + 问题 | $G$ 条回答轨迹 |
| 验证者 | 回答 + 参考答案 | $G$ 次二元判断 → 多数投票奖励 |
| 统一策略更新 | 三角色轨迹 | 更新后的单一策略模型 $\pi_\theta$ |

整个框架无需外部标注数据，仅依赖文档语料库和模型自身的自对弈交互即可实现长上下文推理能力的持续进化。



### 三角色自对弈循环

SPELL的核心架构是一个闭环的自对弈强化学习系统，单一策略模型 $\pi_\theta$ 动态扮演三个互补角色：**提问者**（Questioner）$\pi_\theta^{\text{que}}$、**回答者**（Responder）$\pi_\theta^{\text{res}}$ 和**验证者**（Verifier）$\pi_\theta^{\text{ver}}$。该循环由两个阶段交替构成：

1. **角色特定采样**（Role-Specific Rollout）：单一策略模型以三种角色生成训练数据。
2. **统一策略更新**（Unified Policy Update）：利用收集的数据联合优化策略，增强后的模型作为下一轮采样的起点。

### 提问者与历史记忆

提问者基于新采样的文档子集 $C_{\text{new}}$ 和**历史记忆** $H_C$ 生成多跳推理问题及参考答案。历史记忆缓存最近 $L$ 个（默认 $L=3$）可解的问题-答案对和对应文档，使提问者的上下文逐步扩展：

$$X^{\text{que}} = \left( \bigcup_{l=1}^{L} C_{\text{old}}^{(l)} \cup \{q^{(l)}, a^{(l)}\} \right) \cup C_{\text{new}}$$

通过不断将已解决的问题纳入记忆，提问者被迫生成更具挑战性的新问题，形成自动课程。同时，**基础性过滤器**（Grounding Filter）丢弃无需文档即可回答的问题，强制模型依赖上下文。

### 验证者与语义奖励

验证者对回答者的输出 $y_i$ 与提问者的参考答案 $a$ 进行语义等价判断。对每个 $y_i$，验证者生成 $G$ 个独立的二元判定 $v_{i,j} \in \{0,1\}$，通过多数投票聚合为共识分数：

$$v_i^{\text{ver}} = \mathbb{I}\left( \sum_{j=1}^{G} v_{i,j} > \frac{G}{2} \right)$$

其中 $\mathbb{I}(\cdot)$ 为指示函数。验证者自身的奖励基于与多数票的一致性：

$$r_{i,j}^{\text{ver}} = \mathbb{I}(v_{i,j} = v_i^{\text{ver}})$$

### 回答者奖励函数

回答者的奖励取规则匹配与验证者共识的最大值，防止语义正确的释义被精确匹配误判：

$$r_i^{\text{res}} = \max\left( \mathcal{R}_{\text{rule}}(y_i, a), v_i^{\text{ver}} \right)$$

其中 $\mathcal{R}_{\text{rule}}$ 为基于规则的精确匹配检查（CEM）。

### 提问者奖励函数

提问者的奖励以回答者平均成功率 $\bar{r}^{\text{res}} = \frac{1}{G}\sum_{i=1}^{G} r_i^{\text{res}}$ 为输入，采用高斯函数鼓励生成难度适中的问题（中心 $\mu=0.5$），并惩罚无依据或格式错误：

$$r^{\text{que}} = \begin{cases}
\exp\left( -\frac{(\bar{r}^{\text{res}} - \mu)^2}{2\sigma^2} \right) & \text{if } 0 < \bar{r}^{\text{res}} < 1 \\
0 & \text{if } \bar{r}^{\text{res}} = 0 \text{ or } \bar{r}^{\text{res}} = 1 \\
-0.5 & \text{if the question is not grounded in documents} \\
-1 & \text{if the question-answer pair has formatting errors}
\end{cases}$$

标准差设定为 $\sigma = 0.5/3$，由 $3\sigma = 0.5$ 推导，确保奖励的有效范围覆盖回答者准确率空间 $[0,1]$。

### GRPO优化目标

SPELL采用组相对策略优化（GRPO）作为底层RL算法，通过组内奖励归一化估计优势函数，无需值函数网络。对于上下文 $c$ 和问题 $q$，采样 $G$ 条轨迹 $\{y_i\}_{i=1}^{G}$，组相对优势为：

$$A_i = \frac{r_i - \text{mean}(\{r_k\}_{k=1}^{G})}{\text{std}(\{r_k\}_{k=1}^{G})}$$

GRPO目标函数为：

$$\mathcal{J}_{\text{GRPO}}(\boldsymbol{\theta}) = \mathbb{E}_{\boldsymbol{c},\boldsymbol{q} \sim \mathcal{D}, \{y_i\}_{i=1}^{G} \sim \pi_{\theta_{\text{old}}}(\cdot|\boldsymbol{c},\boldsymbol{q})} \Bigg[ \frac{1}{G} \sum_{i=1}^{G} \frac{1}{|y_i|} \sum_{t=1}^{|y_i|} \Bigg( \min\Big( \rho_{i,t}(\boldsymbol{\theta}) A_i, \text{clip}\Big( \rho_{i,t}(\boldsymbol{\theta}), 1-\varepsilon, 1+\varepsilon \Big) A_i \Big) - \beta \mathbb{D}_{\text{KL}}(\pi_{\theta} || \pi_{\text{ref}}) \Bigg) \Bigg]$$

其中 $\rho_{i,t}(\boldsymbol{\theta})$ 为新旧策略的概率比，$\varepsilon$ 为裁剪参数，$\beta$ 控制KL散度正则化强度。

### 统一策略更新

最终的策略参数 $\theta$ 通过联合优化三个角色的GRPO目标来更新：

$$\mathcal{J}_{\text{GRPO}}(\theta) = \mathcal{J}_{\text{GRPO}}^{\text{que}}(\theta) + \mathcal{J}_{\text{GRPO}}^{\text{res}}(\theta) + \mathcal{J}_{\text{GRPO}}^{\text{ver}}(\theta)$$

### 角色特定动态采样

为防止验证者梯度主导训练，SPELL采用角色特定动态采样策略：仅保留奖励方差非零的回答者组，平衡正负提问者样本，并削减验证者样本量。更新后的策略 $\pi_\theta$ 直接复用于下一轮迭代的所有角色，形成持续的自进化闭环。



## 实验与关键发现

### 主要结果：跨模型一致提升与测试时缩放

SPELL 在多个基座模型上带来了显著且一致的性能增益。以 16K 上下文下的总体平均分为例，**Qwen2.5‑7B** 从基线的 26.7 分提升至 40.6 分（+13.9），**Qwen2.5‑14B** 提升 14.4 分，**Qwen2.5‑32B** 提升 9.1 分（Table 1）。对于更强的 **Qwen3‑30B‑A3B‑Thinking**，基线平均分为 60.7，SPELL 进一步提升至 62.7（+2.0），而同期 RLVR 基线则完全无增益（60.7）（Table 1）。在更具挑战性的子任务上，RLVR 甚至出现了性能下降（DocMath −0.2，LongBench‑V2 −1.2），而 SPELL 仍分别获得 +1.2 和 +2.6 的增益，表明自对弈课程在模型能力边界附近持续提供有效训练信号。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_83F6YF4Hz6/figures/005_Table_1.jpg]]
*Table 1: Overall results of our proposed SPELL method with maximum input lengths of 16K and 100K on longcontext benchmarks. “LB-MQA” represents the average performance across 2WikiMultihopQA, HotpotQA, and MuSiQue. “LB-V2” refers to LongBench-v2. For the average score (Avg.), + indicates the relative improvement over the base model within each group. The best score in each model group is highlighted in bold*

测试时缩放（test‑time scaling）方面，SPELL 带来的提升幅度显著超过基线和 RLVR。Qwen3‑30B‑A3B‑Thinking 的 pass@8 从基线的 66.9 提升至 74.5（Figure 3），且 pass@4 时即超越 **gemini‑2.5‑pro**。这表明 SPELL 训练不仅提升了单次推理的准确率，还增强了模型在多次采样下的探索能力和性能上限。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_83F6YF4Hz6/figures/006_Figure_3.jpg]]
*Figure 3: Test-time scaling performance (pass@k) across all benchmarks. The Qwen3-30B-A3B-Thinking model trained with SPELL shows a significantly steeper improvement as the number of samples (K) increases compared to the base model and the RLVR baseline. Notably, its pass@4 performance surpasses gemini-2.5-pro*

### 消融实验：三角色协同的关键组件

消融实验基于 Qwen2.5‑7B‑Instruct 进行，完整 SPELL 的平均分为 47.2（Table 2）。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_83F6YF4Hz6/figures/008_Table_2.jpg]]

- **验证器不可替代**：移除验证器（w/o Verifier）使平均分下降 3.2 分（降至 44.0），其中在需要深层语义理解的 DocMath 上降幅最大（−6.4 分）。这证实了基于多数投票的语义验证器对提供可靠奖励信号至关重要，仅靠规则匹配（CEM）无法有效处理释义等价问题。
- **提问者更新至关重要**：冻结提问者更新（w/o Que Update）导致平均分下降 4.6 分，且问题难度在训练过程中停滞不前（Figure 4 中图）。这表明提问者必须同步进化，才能持续生成处于回答者能力边界的问题，维持课程的有效性。
- **历史记忆驱动难度爬升**：移除历史记忆（w/o History Memory）使平均分下降 2.9 分，同时问题难度变得不稳定（Figure 4 右图）。历史记忆通过缓存近期可解的问题‑答案对和文档，使提问者能够在扩展上下文中生成更具挑战性的多跳推理问题，是实现自动课程的核心机制。
- **提问者奖励函数设计**：高斯奖励函数的标准差 $\sigma = 0.5/3$（默认配置）取得最高平均分 47.2（Table 3），验证了以回答者正确率 0.5 为中心、覆盖 [0,1] 区间的奖励设计能有效引导提问者生成难度适中的问题。
- **组大小选择**：组大小 $G=8$ 达到最佳平均分 47.2，$G=16$ 性能接近但略低（Table 3），说明适度的组内对比足以提供稳定的优势估计。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_83F6YF4Hz6/figures/007_Figure_4.jpg]]
*Figure 4: Analysis of question difficulty (1 - pass@1) on three tasks over training steps. (Left): The full SPELL framework shows a clear upward trend in difficulty. (Middle): Without questioner updates, difficulty stagnates. (Right): Without the history memory, difficulty becomes erratic and unstable*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_83F6YF4Hz6/figures/013_Table_3.jpg]]
*Table 3: Ablation analysis of SPELL varying the standard deviation σ and the rollout group size G using Qwen2.5-7B-Instruct. The default configuration is $\sigma$ = 0 . 5 / 3 and G = 8*

### 外部法官与验证器依赖

当引入外部法官（gpt‑oss‑120b）替代规则匹配时，移除内部验证器仅导致平均分轻微下降 0.5 分（Table 4），远小于使用规则法官时的 3.2 分降幅。这说明外部法官本身能提供较可靠的语义奖励，减弱了对内部验证器的依赖。但考虑到外部法官引入的计算成本和潜在偏见，内置验证器在自对弈框架中仍是高效且必要的组件。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_83F6YF4Hz6/figures/014_Table_4.jpg]]
*Table 4: Comparison of SPELL trained with rule-based judge versus an external judge (gpt-oss-120b). The verifier is crucial when using a rule-based judge, but becomes less critical when including an external judge*

### 泛化性：零样本长上下文扩展

所有模型均在 16K 上下文下训练，但在 100K 条件下进行零样本评估。SPELL 的增益不仅保持，甚至有所放大：例如 Qwen2.5‑14B 在 16K 下提升 14.4 分，100K 下提升 15.0 分（Table 1）。这表明自对弈过程中习得的推理能力具有上下文长度泛化性，不局限于训练时的输入规模。

### 失败模式与局限

尽管 SPELL 在多数场景下表现优异，但仍存在以下值得注意的边界：

1. **验证器“自欺”风险**：验证器本身可能产生系统性误判，尤其在面对复杂语义等价判断时。当前依赖一致性检查（多数投票）作为启发式缓解手段，但未从根本上解决问题。
2. **超长上下文扩展未验证**：训练上下文限定在 16K，虽然零样本泛化至 100K 表现良好，但在 128K 及以上规模下的扩展效率和稳定性尚待探索。
3. **任务格式固定**：自对弈仍依赖预定义的任务格式和文档语料，无法自主发现新的任务类型或与环境交互获取反馈。
4. **协同进化缺乏理论分析**：三角色协同演化的动力学机制尚缺乏理论解释，可解释性有限。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_83F6YF4Hz6/figures/017_Table_6.jpg]]
*Table 6: Details of open-source models and datasets in our experiments*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_83F6YF4Hz6/figures/019_Table_7.jpg]]
*Table 7: Evaluation results for base models on short-context reasoning tasks*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_83F6YF4Hz6/figures/020_Table_8.jpg]]
*Table 8: Evaluation results for base models on MRCR and HELMET subsets. The best score in each model group is highlighted in bold*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_83F6YF4Hz6/figures/021_Table_9.jpg]]
*Table 9: Comparison of SPELL against different long-context alignment baselines. The best score is highlighted in bold*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_83F6YF4Hz6/figures/024_Table_9.jpg]]



## 定位与知识库关联

### 与现有基线的结构关系

SPELL 处于**自对弈强化学习**与**长上下文推理**的交叉地带，其核心贡献在于用单一模型的三角色闭环替代传统 RL 对静态标注数据的依赖。与现有工作的关系可从以下维度理解：

**vs. RLVR（Guo et al., 2025）**：RLVR 使用 DeepSeek‑R1‑0528 生成的固定合成数据进行强化学习，训练信号在优化过程中保持静态。SPELL 的关键突破在于将数据生成与策略优化耦合为动态循环——提问者根据当前回答者能力边界生成难度适中的问题，使训练信号始终与策略能力对齐。这一差异在强基座模型上尤为显著：Qwen3‑30B‑A3B‑Thinking 上 RLVR 无增益（16K Avg 保持 60.7），而 SPELL 提升 2.0 分至 62.7；在更具挑战性的 DocMath 和 LongBench‑V2 上，RLVR 甚至出现性能下降（-0.2 / -1.2），SPELL 则分别提升 1.2 和 2.6 分（Table 1）。

**vs. 指令微调模型**：SPELL 使基座模型（如 Qwen2.5‑7B）在无人类标注数据的情况下，超越其指令微调版本（Qwen2.5‑7B‑Instruct）——后者依赖大规模人工标注进行训练。这验证了自对弈课程在长上下文场景下可替代部分人工监督。

**vs. 长上下文对齐方法**：附录比较中提及 LongPO、SoLoPO、QwenLong‑L1 等方法，它们通常依赖预定义的奖励函数或固定策略进行对齐。SPELL 的优势在于自动课程生成与语义验证器的协同，使难度调节无需人工设计。

### 适用边界

SPELL 在以下条件下已验证有效：
- **基座模型规模**：7B 至 30B‑A3B（MoE）均获得一致提升（Table 1），但更大规模模型的扩展行为尚未验证。
- **训练上下文**：限定在 16K tokens，零样本评估可泛化至 100K（Qwen2.5‑14B 的 100K Avg 提升从 14.4 增至 15.0），但超长上下文（128K+）下的训练效率和稳定性仍是开放问题。
- **任务类型**：当前框架依赖预定义的多跳推理问答格式和固定文档语料（以教育、分析、学习类知识密集型内容为主，见 Figure 6），无法自主发现新的任务类型或环境反馈形式。

### 局限性与失败模式

1. **理论可解释性不足**：三角色协同进化缺乏动力学分析，无法解释为何特定角色更新（如提问者冻结导致平均分下降 4.6 分）对整体性能有决定性影响（Table 2）。

2. **验证器自欺风险**：验证器通过多数投票和一致性检查缓解误判，但未从根本上解决模型可能“学会”欺骗自身验证机制的问题。移除验证器导致平均分下降 3.2 分、DocMath 骤降 6.4 分（Table 2），表明系统对验证器高度敏感。引入外部法官（gpt‑oss‑120b）可减弱此依赖（移除验证器时仅下降 0.5 分，Table 4），但增加了外部成本与可控性顾虑。

3. **历史记忆的脆弱性**：移除历史记忆使平均分下降 2.9 分，且问题难度变得不稳定（Figure 4 Right），说明自动课程的质量高度依赖历史信息积累的稳定性。

4. **超长上下文的扩展效率**：当前 16K 训练窗口限制了框架在 128K+ 场景的直接应用。训练成本随上下文长度线性增长的问题未得到解决。

### 开放问题

1. **超长上下文的自对弈效率**：如何设计更高效的采样和奖励机制，使自对弈 RL 框架能在 128K tokens 及以上场景中稳定训练？

2. **自主任务发现**：能否构建与真实世界环境交互的系统，使 LLM 自主生成和进化任务模板、奖励函数，而非依赖预定义的问答格式？

3. **多角色扩展**：三角色协同进化范式是否可推广至更多角色（如批评者、编辑者）或更复杂的推理类型（如多模态长上下文推理）？

4. **安全自我纠偏**：自对弈框架能否自主发现并纠正模型自身的偏见或系统性推理错误，实现更安全的自我提升？当前验证器的“自欺”问题暗示这一方向需要更根本的机制设计。



## 原文 PDF

![[paperPDFs/ICLR_2026/SPELL_Self_Play_Reinforcement_Learning_for_Evolving_Long_Context_Language_Models.pdf]]
