---
title: "Detecting Data Contamination from Reinforcement Learning Post-training for Large Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Detecting_Data_Contamination_from_Reinforcement_Learning_Post_training_for_Large_Language_Models.pdf
project_link: null
code_link: https://github.com/yongding-tao/RL-Data-Contamination
openreview_forum_id: EjiJmiA6ea
aliases:
- SC
- DDCFRLPTLLM
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "自我批评探测测量的熵序列相似度（即策略坍塌导致的路径依赖程度）"
primary_logic: "RL后训练使模型对训练样本形成高奖励路径依赖，当要求生成替代推理路径时，污染样本的令牌熵模式保持高度相似，而干净样本表现出较大差异，通过比较初始响应与自我批评响应的熵序列可以有效检测RL阶段的污染。"
claims:
- "Self-Critique在Qwen2.5-7B-Instruct上平均AUC达0.70，比最佳基线（Recall，0.59）提高19%"
- "在双阶段污染分析中，降低预训练污染水平后Self-Critique的AUC显著提升（从0.59增至0.88），证明其对RL阶段污染的特异性"
- "消融实验表明，移除初始响应锚点后Self-Critique性能降至随机水平，说明主动锚点探测至关重要"
- "Self-Critique在PPO、GRPO、DAPO三种RL算法上均保持最高AUC，平均0.60，超越最佳基线18%"
---

# Detecting Data Contamination from Reinforcement Learning Post-training for Large Language Models

> [!tip] 核心洞察
> RL后训练使模型对训练样本形成高奖励路径依赖，当要求生成替代推理路径时，污染样本的令牌熵模式保持高度相似，而干净样本表现出较大差异，通过比较初始响应与自我批评响应的熵序列可以有效检测RL阶段的污染。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 检测大型语言模型强化学习后训练阶段的数据污染 |
| 英文题名 | Detecting Data Contamination from Reinforcement Learning Post-training for Large Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=EjiJmiA6ea) · [GitHub](https://github.com/yongding-tao/RL-Data-Contamination) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Self-Critique |
| Dataset | RL-MIA Avg (Qwen2.5-7B-Instruct), RL-MIA Avg (DeepSeek-Math-7B-Instruct), RL-MIA Avg (Qwen2.5-7B-Math), K&K (Llama-3.1-8B-Instruct) |

> [!tip] 效果简介
> - RL-MIA Avg (Qwen2.5-7B-Instruct) 上，AUC 为 0.70，对比 0.59 (Recall)，变化 +0.11 (+19%)。
> - RL-MIA Avg (DeepSeek-Math-7B-Instruct) 上，AUC 为 0.64，对比 0.54 (Recall)，变化 +0.10 (+19%)。
> - RL-MIA Avg (Qwen2.5-7B-Math) 上，AUC 为 0.74，对比 0.57 (Recall)，变化 +0.17 (+30%)。

## 概要

大型语言模型的后训练流程通常包含强化学习（RL）阶段，旨在通过奖励最大化优化模型的推理与对齐能力。然而，当RL训练数据中包含评估基准的样本时，模型可能通过记忆而非泛化获得高性能，导致基准评估失真。检测此类RL阶段的数据污染面临独特挑战：RL的优化目标从最大似然估计转变为奖励最大化，使得基于困惑度（PPL）等似然度指标的传统检测方法失效；同时，RL导致的策略坍塌（policy collapse）使污染样本与干净样本的简单熵检查不可靠。

针对这一瓶颈，本文提出**Self-Critique**，一种基于主动自我批评探测的熵序列相似度检测方法。其核心洞察是：RL后训练使模型对训练样本形成高奖励路径依赖——当要求模型对同一问题生成替代推理路径时，污染样本的令牌级熵模式保持高度相似，而干净样本则表现出较大差异。Self-Critique通过比较初始响应与自我批评响应的熵序列，以带长度罚分的余弦相似度作为污染得分，有效暴露RL阶段的记忆痕迹。

实验表明，Self-Critique在多个模型和基准上显著优于现有方法：在Qwen2.5-7B-Instruct上平均AUC达0.70，比最佳基线Recall（0.59）提高19%；在PPO、GRPO、DAPO三种RL算法上均保持最高检测AUC（平均0.60），展现出对RL算法的鲁棒性。双阶段污染分析进一步验证了该方法对RL阶段污染的特异性——当降低预训练污染水平后，Self-Critique的AUC从0.59显著提升至0.88。

### 数据污染：从预训练到RL后训练的挑战迁移

大语言模型的训练管线通常包含三个阶段：预训练、监督微调（SFT）和基于人类反馈的强化学习（RLHF）或可验证奖励的强化学习（RLVR）后训练。数据污染——即评估基准数据意外泄漏到训练集中——长期以来被视为威胁模型评估可信度的核心问题。然而，现有检测方法几乎全部针对预训练和SFT阶段设计，其理论基础根植于一个关键假设：**模型通过最大似然估计直接优化令牌级对数概率**。

预训练损失 $\mathcal{L}_{\mathrm{Pretrain}}(\theta) = -\sum_{x \in D_{\mathrm{pretrain}}} \sum_{t=1}^{T} \log p_{\theta}(x_t | x_{<t})$ 和SFT损失 $\mathcal{L}_{\mathrm{SFT}}(\theta) = -\sum_{(q,r) \in D_{\mathrm{SFT}}} \sum_{t=1}^{K} \log p_{\theta}(r_t | q, r_{<t})$ 均显式地最大化目标令牌的似然度。这一优化目标使得污染样本在模型输出中天然呈现低困惑度（PPL）、高令牌概率等可检测特征。因此，基于似然度的检测方法——如**PPL**（Gonen et al., EMNLP 2023）、**Min-K%**（Shi et al., ICLR 2024）和**Min-K%++**（Zhang et al., ICLR 2025）——以及基于前缀注入的**Recall**（Xie et al., EMNLP 2024）和基于输出一致性的**CDD**（Dong et al., ACL 2024）在这一范式下取得了可观的检测效果。

### RL后训练的根本性断裂

RL后训练引入了与前述阶段根本不同的优化目标。以GRPO为代表的RLVR目标函数为：

$$\mathcal{I}_{\mathrm{RL}}(\theta) = \mathbb{E}_{q \sim D_{\mathrm{RL}}, \{o_i\} \sim \pi_{\theta_{\mathrm{old}}}} \left[ f(\mathcal{R}(o_i), \pi_{\theta}) \right]$$

该目标**最大化期望奖励**，而非令牌级对数概率。模型被激励寻找能获得高奖励的特定推理路径，而非在所有可能路径上均匀分配概率质量。这一目标转换带来了两个关键后果：

1. **似然度信号失效**：由于优化不再直接作用于对数概率，污染样本未必呈现低困惑度或高令牌概率，使得PPL、Min-K%等方法退化为接近随机猜测的水平。
2. **策略坍塌**：RL训练导致模型的预测分布变得极度稀疏（熵崩塌），模型对训练中反复出现的污染样本形成**高奖励路径依赖**——即使被要求生成替代推理路径，模型仍会顽固地回到记忆中的解路径。

### 核心洞察：熵序列相似度暴露路径依赖

本文的核心洞察在于：RL后训练引起的策略坍塌使得污染样本与干净样本在**令牌级熵的序列模式**上表现出本质差异。具体而言：

- **污染样本**：当模型被要求对同一问题生成两个不同响应时（初始响应和自我批评响应），由于RL训练使模型将特定推理路径与高奖励强绑定，两个响应的令牌熵序列保持高度相似——模型在相同位置表现出相同的不确定性模式，暴露了其对记忆路径的依赖。
- **干净样本**：模型未对特定推理路径形成奖励绑定，因此两个响应的熵序列表现出较大差异，反映了模型在探索不同推理策略时的灵活性。

这一洞察将检测问题从“模型是否见过该样本”重新表述为“模型是否对该样本形成了不可摆脱的路径依赖”，从而绕开了RL阶段似然度信号不可靠的根本困境。基于此，本文提出**Self-Critique**方法，通过主动自我批评探测机制测量熵序列相似度，实现了对RL后训练阶段数据污染的首次专门检测。

## 核心方法与创新机理

### 检测范式转换：从被动似然度量到主动路径依赖探测

现有数据污染检测方法的设计逻辑根植于预训练和SFT阶段的优化特性——模型通过最大似然估计直接拟合训练数据的令牌分布，因此训练样本往往表现出更低的困惑度（**PPL**, Gonen et al., EMNLP 2023）或更小的最小令牌概率（**Min-K%**, Shi et al., ICLR 2024; **Min-K%++**, Zhang et al., ICLR 2025）。然而，RL后训练的目标函数发生了根本性转变：从最大化令牌级对数概率转向最大化期望奖励（见公式3）。这一目标解耦意味着模型对训练样本的记忆不再必然体现为低困惑度，而是表现为**对高奖励推理路径的策略坍塌**——模型在遇到污染样本时，倾向于重复输出曾经获得高奖励的特定推理轨迹，而非探索替代方案。

Self-Critique的核心创新在于将检测机制从**被动观察似然属性**转变为**主动探测路径依赖**。具体而言，该方法通过三个关键设计实现了这一范式转换：

**1. 主动自我批评探测机制（Self-Critique Probing）**

与Recall方法（Xie et al., EMNLP 2024）注入非成员前缀、CDD方法（Dong et al., ACL 2024）进行多次随机采样不同，Self-Critique采用**确定性初始响应作为锚点**，然后显式要求模型生成替代推理路径。这一设计的因果逻辑是：RL后训练使污染样本形成高奖励路径依赖，当模型被指令"请检查你的答案并提供另一种解法"时，污染样本的替代响应将难以偏离初始路径，而干净样本则能产生显著不同的推理轨迹。消融实验（Figure 4, Appendix C.1）提供了决定性证据：移除初始响应锚点后，Self-Critique的性能暴跌至随机猜测水平，证明主动锚点探测是方法有效性的必要条件。

**2. 令牌级熵作为核心度量信号**

传统方法依赖对数概率或编辑距离作为度量，但这些信号在RL阶段变得不可靠。Self-Critique转而采用**令牌级熵**（公式4）来衡量模型在每一步解码时的不确定性分布。RL后训练导致的策略坍塌会使污染样本的熵序列在两个响应间保持高度相似，而干净样本则表现出较大差异。这一选择具有坚实的因果基础：RL优化并不直接塑造令牌概率分布，但会间接压缩模型对特定路径的探索空间，熵序列恰好能捕捉这种压缩效应。

**3. 带长度罚分的余弦相似度评分**

为量化两个熵序列的相似程度，Self-Critique采用带长度罚分的余弦相似度（公式8-9）。长度罚分项（最小长度/最大长度）惩罚两个响应长度不匹配的情况，确保评分反映的是路径相似性而非长度巧合。这一设计使评分具有明确的物理含义：高相似度意味着策略坍塌，即污染；低相似度意味着路径多样性，即干净。

### 方法分类学定位

Table 1的方法分类学清晰展示了Self-Critique的独特位置：它是首个专门针对**RL后训练阶段**设计的检测方法，与所有面向预训练/SFT的基线方法在探测机制、核心度量和设计阶段三个维度上均存在本质差异。表1中同时引入的Entropy-Temp和Entropy-Noise两种熵基线方法（均使用熵度量但采用不同的探测策略）进一步验证了一个关键结论：**熵信号本身并非充分条件，必须与自我批评探测机制结合才能有效暴露RL阶段的污染特征**。主实验结果（Table 2）表明，Self-Critique在Qwen2.5-7B-Instruct上平均AUC达0.70，比最佳基线Recall（0.59）提高19%，而Entropy-Temp和Entropy-Noise的性能显著低于Self-Critique，直接证明了探测机制与度量的协同必要性。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_EjiJmiA6ea/figures/005_Table_1.jpg]]
*Table 1: A taxonomy of data contamination detection methods. Our work is the first to specifically address the challenges in the RL Post-training phase*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_EjiJmiA6ea/figures/004_Figure_2.jpg]]
*Figure 2: Overview of the Self-Critique detection workflow. The method compares token-level entropy sequences between the initial response and the self-critique response. High similarity in entropy space indicates contamination (policy collapse), while low similarity indicates clean samples*

### 问题定位：RL后训练阶段的检测盲区

传统数据污染检测方法（如基于困惑度PPL的**Gonen et al., EMNLP 2023**、Min-K%的**Shi et al., ICLR 2024**及Min-K%++的**Zhang et al., ICLR 2025**）均建立在预训练或监督微调（SFT）阶段的最大似然估计优化目标之上。然而，RL后训练阶段的目标函数从令牌级对数概率最大似然转变为奖励最大化（见公式3），导致模型对训练样本形成**高奖励路径依赖**——即使被要求生成不同的推理路径，模型仍倾向于重复训练时习得的特定推理轨迹。这一现象被称为**策略坍塌**（policy collapse），其直接后果是：污染样本与干净样本在简单熵检查下无法可靠区分，基于似然度的检测方法近乎随机猜测。

本工作将RL后训练阶段的数据污染检测形式化为**黑盒成员推理攻击**（Membership Inference Attack, MIA）问题，并首次针对该阶段提出系统性的检测框架。

### 方法分类学定位

Table 1给出了数据污染检测方法的系统分类。现有方法按探测机制可划分为三类：**内在属性检测**（PPL、Min-K%、Min-K%++）、**非成员前缀注入**（Recall，**Xie et al., EMNLP 2024**）和**随机采样探测**（CDD，**Dong et al., ACL 2024**）。这些方法的核心度量分别为对数概率和编辑距离，设计阶段均为预训练或SFT。

本文提出的Self-Critique在三个关键维度上实现了根本性转变：**探测机制**从被动属性检查或随机扰动转向主动自我批评探测，**核心度量**从似然度转向令牌级熵，**适用阶段**从预训练/SFT转向RL后训练。这一转变的深层动因在于：RL优化使模型对污染样本形成路径依赖，而熵作为预测分布不确定性的直接度量，能够敏感地捕捉到这种依赖——当模型被要求生成替代推理路径时，污染样本的熵模式保持高度相似，而干净样本则表现出显著差异。

### Pipeline架构与模块关系

Figure 2展示了Self-Critique的完整检测流程，包含四个顺序执行的模块：

**模块一：初始响应生成。** 给定待检测问题$q$，使用贪婪解码（确定性策略）生成模型的初始响应$r_1 = \mathcal{M}(T(q))$，作为后续比较的基准锚点。选择贪婪解码的关键原因在于：它排除了采样随机性，能够最纯粹地暴露RL训练导致的策略坍塌效应。消融实验证实，移除该初始响应锚点后，Self-Critique的性能暴跌至随机猜测水平（Figure 4），验证了主动锚点探测的必要性。

**模块二：自我批评响应生成。** 将初始响应$r_1$嵌入元指令$I_{\mathrm{critique}}$中，构造增强提示$q' = q \oplus I_{\mathrm{critique}}(r_1)$，要求模型生成一条不同于初始响应的替代推理路径。随后再次使用贪婪解码获得自我批评响应$r_2 = \mathcal{M}(T(q'))$。这一步骤的核心设计在于：元指令明确要求模型“改变推理路径”，从而主动探测模型是否能够摆脱训练时形成的路径依赖。消融实验表明，贪婪-贪婪采样策略（初始和自我批评均使用贪婪解码）在所有采样策略组合中性能最佳（Figure 5），因为它最大化地排除了随机性干扰。

**模块三：令牌级熵序列计算。** 对两个响应分别计算每一步解码的令牌级熵$H_t = -\sum_{v \in V} p_\theta(v \mid x_{<t}) \log p_\theta(v \mid x_{<t})$，形成熵序列$E_1$和$E_2$。为降低全词表熵计算的计算开销，引入Top-K熵近似——仅使用预测分布中概率最高的前K个令牌近似计算熵值。消融实验表明，K值取3时已足够有效，K值变化带来的AUC方差极小（<1e-4），验证了计算效率与检测精度的平衡（Table 4）。

**模块四：带长度罚分的余弦相似度评分。** 计算两个熵序列的相似度作为污染得分：$\mathrm{Score}_{\mathrm{Self-Critique}}(q) = \cos_{\mathrm{penalized}}(E_1, E_2)$。其中带长度罚分的余弦相似度定义为：对较短序列进行零填充后计算标准余弦相似度，再乘以长度比$\frac{\min(|A|,|B|)}{\max(|A|,|B|)}$，以惩罚因响应长度差异过大导致的虚假高相似度。**高相似度表示污染**——模型在明确要求改变推理路径后仍保持高度相似的熵模式，说明RL训练使其陷入了对特定推理路径的策略坍塌。

### 输入输出流

- **输入**：待检测问题文本$q$（自然语言形式）
- **中间产物**：初始响应$r_1$及其熵序列$E_1$，自我批评响应$r_2$及其熵序列$E_2$
- **输出**：污染得分$\mathrm{Score}_{\mathrm{Self-Critique}}(q) \in [-1, 1]$，高分表示高污染概率
- **决策**：通过设定阈值（如Youden指数下的最优阈值）将连续得分二值化为污染/干净判定

### 方法鲁棒性

Self-Critique在多个维度上展现出强鲁棒性：（1）对元指令措辞不敏感，不同提示下的AUC标准差仅为0.025左右（Table 9）；（2）在PPO、GRPO、DAPO三种不同RL算法训练的模型上均保持最高检测AUC（Table 3），表明其不依赖特定RL算法；（3）在RLHF对齐场景（PPO、DPO、TDPO、RTO）下同样保持一致的检测优势（Table 8）。

### 3.1 问题形式化：RL后训练阶段的成员推理攻击

Self-Critique将RL后训练阶段的数据污染检测形式化为黑盒成员推理攻击问题。给定一个RL后训练模型的输出接口，检测器需要判断某个问题 $q$ 是否属于RL训练集 $D_{\mathrm{RL}}$。这一设定与预训练/SFT阶段的MIA检测（Shi et al., ICLR 2024）共享基本框架，但面临根本性挑战：RL后训练的目标函数与似然度解耦。

### 3.2 瓶颈分析：RL目标函数与似然度信号失效

理解Self-Critique的设计需要先理解RL后训练与传统训练阶段的本质差异。预训练和SFT的损失函数直接优化令牌级对数概率：

$$ \mathcal{L}_{\mathrm{Pretrain}}(\theta) = -\sum_{x \in D_{\mathrm{pretrain}}} \sum_{t=1}^{T} \log p_{\theta}(x_t | x_{<t}) $$

$$ \mathcal{L}_{\mathrm{SFT}}(\theta) = -\sum_{(q,r) \in D_{\mathrm{SFT}}} \sum_{t=1}^{K} \log p_{\theta}(r_t | q, r_{<t}) $$

而RL后训练（以GRPO为代表）的目标是最大化期望奖励，与令牌级对数概率解耦：

$$ \mathcal{I}_{\mathrm{RL}}(\theta) = \mathbb{E}_{q \sim D_{\mathrm{RL}}, \{o_i\} \sim \pi_{\theta_{\mathrm{old}}}} \left[ f(\mathcal{R}(o_i), \pi_{\theta}) \right] $$

这一根本差异导致两个关键后果：（1）基于困惑度或最小概率的似然度方法（PPL、Min-K%、Min-K%++）在RL阶段失效，因为模型不再被训练为对污染样本分配更高概率；（2）RL通过奖励信号引导模型收敛到特定的高奖励推理路径，形成**策略坍塌**——模型对训练样本产生路径依赖，即使被要求生成替代方案，其推理路径仍高度相似。

### 3.3 核心信号：令牌级熵

Self-Critique引入令牌级熵作为检测RL污染的核心信号。对于解码步 $t$，令牌级熵定义为预测分布的不确定性：

$$ H_t = -\sum_{v \in V} p_{\theta}(v \mid x_{<t}) \log p_{\theta}(v \mid x_{<t}) $$

选择熵而非对数概率的理由在于：RL后训练不直接优化似然度，但策略坍塌会导致模型对训练样本的推理路径高度确定，表现为低熵且路径固定的生成模式。当模型被要求生成替代推理路径时，污染样本的熵序列保持高度相似，而干净样本的熵序列则表现出较大差异——这种**熵序列相似度**成为检测RL阶段污染的可操作因果旋钮。

### 3.4 Self-Critique检测流程

Self-Critique由四个核心模块串联组成：

**模块一：初始响应生成。** 使用贪婪解码获取模型最自信的确定性响应，作为后续比较的基准锚点：

$$ r_1 = \mathcal{M}(T(q)) $$

其中 $\mathcal{M}$ 为模型，$T(q)$ 为问题 $q$ 的对话模板格式。贪婪解码排除了采样随机性，确保初始响应反映模型在给定问题上的首选推理路径。

**模块二：自我批评响应生成。** 将初始响应嵌入元指令，构造自我批评提示，要求模型生成不同的替代推理路径：

$$ q' = q \oplus I_{\mathrm{critique}}(r_1) $$

$$ r_2 = \mathcal{M}(T(q')), \quad E_2 = \{H_t(r_2)\}_{t=1}^{|r_2|} $$

其中 $I_{\mathrm{critique}}(r_1)$ 为包含初始响应的自我批评指令，$E_2$ 为自我批评响应的令牌级熵序列。这一主动探测机制是Self-Critique区别于被动似然度方法的关键创新：它不依赖模型对样本的概率赋值，而是通过指令迫使模型暴露其路径依赖程度。

**模块三：熵序列相似度评分。** 计算初始响应熵序列 $E_1$ 与自我批评响应熵序列 $E_2$ 的带长度罚分余弦相似度：

$$ \operatorname{Score}_{\operatorname{Self-Critique}}(q) = \cos_{\operatorname{penalized}}(E_1, E_2) $$

$$ \cos_{\mathrm{penalized}}(A, B) = \cos\bigl(\mathrm{pad}(A), \mathrm{pad}(B)\bigr) \times \frac{\mathrm{min}(|A|, |B|)}{\mathrm{max}(|A|, |B|)} $$

长度罚分机制通过惩罚序列长度不匹配，避免因响应长度差异导致的相似度假性偏高。高相似度分数表明模型即使在被要求改变推理路径后，其令牌级不确定性模式仍与初始响应高度一致，即存在RL导致的策略坍塌和记忆化——这是污染样本的标志。

**模块四（优化）：Top-K熵近似。** 为降低全词表熵计算的开销，Self-Critique支持仅使用前 $K$ 个最高概率令牌近似熵值。消融实验（Table 4）表明，$K=3$ 时已足够有效，不同 $K$ 值间的AUC方差极小（$<10^{-4}$），验证了计算效率与检测精度的良好平衡。

## 实验与关键发现

### 核心发现：RL后训练阶段检测的范式转移

在RL后训练阶段，优化目标从最大似然估计（MLE）转变为奖励最大化，导致基于似然度（如困惑度PPL、Min-K%概率）的传统检测方法系统性失效。实验表明，**PPL**（Gonen et al., EMNLP 2023）、**Min-K%**（Shi et al., ICLR 2024）和**Min-K%++**（Zhang et al., ICLR 2025）在RL-MIA基准上的AUC普遍徘徊在0.50左右（Table 2），接近随机猜测水平。这一现象的根本原因在于：RL后训练不再直接优化令牌级对数概率（Equation 3），而是通过奖励信号驱动策略更新，使得模型对训练样本形成**高奖励路径依赖**——即策略坍塌。因此，检测的关键从“模型是否对某样本赋予高概率”转变为“模型是否被锁定在特定推理路径上”。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_EjiJmiA6ea/figures/006_Table_2.jpg]]
*Table 2: Performance of different detection methods on the RL-MIA benchmark across two models. The AVG column is the average AUC across all benchmarks. Best AUC is in bold; the second best is underlined*

Self-Critique通过**主动自我批评探测**捕捉这一路径依赖：首先以贪婪解码生成确定性初始响应作为锚点，然后要求模型基于该响应生成替代推理路径，最终比较两条路径的令牌级熵序列相似度。高相似度表明模型即使被指令改变推理方向，仍无法摆脱已记忆的路径，即存在RL阶段污染。

### 主实验结果

**Table 2** 汇总了各方法在RL-MIA基准上的核心性能。Self-Critique在两个主流模型上均取得最佳平均AUC：

| 模型 | Self-Critique AUC | 最佳基线 AUC | 提升幅度 |
|------|-------------------|--------------|----------|
| Qwen2.5-7B-Instruct | **0.70** | 0.59 (Recall) | +19% |
| DeepSeek-Math-7B-Instruct | **0.64** | 0.54 (Recall) | +19% |

在Qwen2.5-7B-Math模型上（Table 5），Self-Critique的优势进一步扩大，平均AUC达到**0.74**，比最佳基线Recall（0.57）提升**30%**。在Llama-3.1-8B-Instruct的逻辑推理数据集上（Table 6），Self-Critique在Knights & Knaves上取得**0.81**的AUC，远超Recall的0.62。

值得注意的是，本文提出的两个熵基线——**Entropy-Temp**（随机采样探测+熵度量）和**Entropy-Noise**（非成员前缀探测+熵度量）——虽未超越Self-Critique，但已显著优于传统似然度方法。这验证了一个关键洞察：**熵作为RL阶段变化的敏感指标，天然比对数概率更适合RL后训练场景的污染检测**。然而，仅靠被动熵探测（随机采样或前缀注入）无法充分暴露策略坍塌，必须结合Self-Critique的主动锚点机制才能实现最优检测。

### 消融实验：方法设计的因果验证

#### 1. 自我批评探测的必要性

**Figure 4** 直接对比了完整Self-Critique与移除初始响应锚点的变体。结果显示，当去掉自我批评探测（即仅比较两次独立随机采样的熵序列）时，检测性能暴跌至随机猜测水平。这确证了**主动锚点探测是方法有效性的核心因果旋钮**——模型必须被明确要求“在看到自己的初始推理后生成替代方案”，才能暴露其对训练路径的依赖程度。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_EjiJmiA6ea/figures/015_Figure_4.jpg]]
*Figure 4: Self-critique probing vs. no self-critique*

#### 2. 采样策略的选择

**Figure 5** 对比了贪婪-贪婪、贪婪-温度、温度-贪婪、温度-温度四种采样策略组合。贪婪-贪婪策略（初始响应和自我批评响应均使用确定性贪婪解码）在所有配置中性能最佳。原因在于：确定性解码排除了随机性对熵序列的干扰，使两次响应的差异纯粹反映模型对推理路径的依赖程度，而非采样噪声。温度采样引入的随机性反而模糊了污染与干净样本之间的信号差异。

#### 3. Top-K熵近似的效率与精度平衡

计算完整词表熵（Equation 4）在推理时开销较大。**Table 4** 的消融表明，仅使用前K个令牌概率近似熵（Top-K entropy）在K=3时已足够有效：

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_EjiJmiA6ea/figures/009_Table_4.jpg]]
*Table 4: Ablation on Top-K entropy approximation (Qwen2.5-7B-Instruct). We report AUC for different K and the row-wise variance across K ∈ {3, 5, 10, 20, 50}. We also provide additional ablation studies about why self-critique probing is better, the sampling strategy and sensitivity to meta-instructions in Appendix C*

- AIME25上K=3的AUC为0.7022，K=50为0.7156，差异极小
- 跨K值（3, 5, 10, 20, 50）的逐行方差仅为2.39×10⁻⁵（AIME25）和3.62×10⁻⁵（K&K）

这说明RL后训练导致的策略坍塌主要反映在**高概率令牌的分布集中度**上，低概率尾部令牌对检测信号贡献微弱。Top-K近似在几乎不损失精度的前提下大幅降低计算开销，使Self-Critique具备实际部署的可行性。

#### 4. 元指令的鲁棒性

**Table 9** 测试了6种不同的自我批评提示变体，跨AIME25和K&K数据集的AUC标准差仅为0.025左右。这表明Self-Critique不依赖特定的提示措辞，方法具有工程上的稳定性和可复现性。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_EjiJmiA6ea/figures/017_Table_9.jpg]]
*Table 9: Ablation study on different Self-Critique meta-instructions. The method shows high robustness to prompt variations, as indicated by the low standard deviation*

### 跨RL算法与跨阶段的泛化验证

#### RL算法无关性

**Table 3** 在Qwen2.5-3B-Instruct上对比了PPO、GRPO、DAPO三种主流RL算法训练的模型。Self-Critique在三种算法下均保持最高AUC（平均0.60），超越最佳基线18%。这表明方法捕捉的是RL后训练共有的策略坍塌现象，而非特定算法的优化偏差。

在RLHF对齐场景（UltraFeedback数据集，Table 8）中，Self-Critique在PPO、DPO、TDPO、RTO四种对齐算法上同样一致优于基线，AUC范围0.62-0.70，进一步验证了方法的跨范式适用性。

#### 双阶段污染分析：RL阶段特异性的关键证据

现实场景中，RL训练数据往往已在预训练阶段被模型见过，形成**预训练+RL双阶段污染**。**Figure 3** 和 **Table 7** 通过控制预训练污染水平（按分位数筛选）来解耦两个阶段的贡献。核心发现：

- 当保留的预训练污染分位数从1.0降至0.0时，Self-Critique的AUC从0.59**急剧提升至0.88**
- 这一趋势表明：预训练污染会混淆RL阶段的检测信号（因为模型在预训练阶段已通过MLE记住了部分样本），但Self-Critique对**纯RL阶段污染**具有极高的特异性
- 在实际部署中，若能将预训练污染的影响降至最低（如使用严格去污的基座模型），Self-Critique可达到接近0.9的检测AUC

### 失败模式与局限性

尽管Self-Critique在数学推理和逻辑推理任务上表现出色，但存在以下已知局限：

1. **任务领域局限**：实验主要覆盖数学推理（AIME 2024/2025）和逻辑推理（Knights & Knaves、SAT），尚未在代码生成、机器翻译等具有更高解决方案多样性的领域验证。这些领域中“替代推理路径”的语义空间更大，策略坍塌的表现形式可能不同。

2. **模型规模范围**：评估模型参数在0.5B至8B之间，虽具代表性，但未涵盖数十亿至数百亿参数的前沿模型。大规模模型的策略坍塌和记忆效应可能呈现不同的熵分布特征，需要进一步验证。

3. **污染重复次数的模拟有限**：RL-MIA基准中污染样本的重复次数（Occurrences）为2-4次，可能未完全模拟真实场景中更严重的重复污染（如数据被多次采样训练）。更高频次的污染可能导致更深的策略坍塌，但也可能使熵信号饱和。

4. **RL超参数影响未系统研究**：学习率、批次大小、KL散度惩罚系数等RL超参数可能影响策略坍塌的程度，进而影响Self-Critique的检测灵敏度，但目前缺乏系统性的参数敏感性分析。

### 关键图表解读

- **Figure 6**：污染与干净样本的Self-Critique分数分布直方图及核密度估计显示，两组分布存在明显分离（污染样本的熵序列相似度系统性偏高），但仍有部分重叠区域，这解释了AUC在0.64-0.81而非接近1.0的原因。
- **Table 12**：Bootstrap分析（1000次重采样）显示Self-Critique在SAT数据集上的95%置信区间为[0.56, 0.76]（Qwen）和[0.55, 0.77]（DeepSeek），区间下限均显著高于0.5，验证了检测性能的统计显著性。

## 定位与知识库关联

### 1. 检测方法分类学定位

RL后训练阶段的数据污染检测是一个此前未被专门探索的空白地带。如表1所示，现有方法可根据**探测机制**和**核心度量**两个维度进行系统分类：

**预训练/SFT阶段方法**（基于似然度）：
- **PPL**（Gonen et al., EMNLP 2023）：利用低困惑度作为污染信号，依赖最大似然估计训练目标下污染样本获得更高对数概率的特性。
- **Min-K%**（Shi et al., ICLR 2024）：取生成序列中概率最低的K%令牌的平均对数概率，增强对局部记忆痕迹的敏感性。
- **Min-K%++**（Zhang et al., ICLR 2025）：对Min-K%进行标准化改进，减少令牌频率偏差的影响。
- **Recall**（Xie et al., EMNLP 2024）：通过注入非成员前缀探测模型对已知后缀的似然度，将检测转化为前缀引导的成员推断。
- **CDD**（Dong et al., ACL 2024）：基于多次随机采样的输出一致性，使用编辑距离度量生成多样性，低多样性暗示污染。

这些方法的共同瓶颈在于：RL后训练将优化目标从最大似然估计转变为奖励最大化（见Equation 3），切断了似然度与记忆之间的直接关联。实验证实，PPL、Min-K%和Min-K%++在RL-MIA基准上的平均AUC接近随机猜测水平（约0.50），验证了这一根本性失效。

**RL后训练阶段方法**（本文提出及对比）：
- **Entropy-Temp**：采用随机采样探测（温度采样）配合令牌级熵度量，检验随机性是否足以暴露策略坍塌。
- **Entropy-Noise**：采用非成员前缀注入探测配合熵度量，测试外部扰动能否破坏污染样本的路径依赖。
- **Self-Critique**（本文核心方法）：采用自我批评探测配合熵序列相似度度量，主动要求模型生成替代推理路径，通过比较初始响应与批评响应的熵序列相似度来量化RL诱导的策略坍塌程度。

### 2. 机制差异与方法边界

Self-Critique与基线方法的核心差异体现在三个关键设计槽位：

| 设计维度 | 基线方法 | Self-Critique | 设计动机 |
|---------|---------|--------------|---------|
| **探测机制** | 被动似然度属性、随机采样或非成员前缀注入 | 主动自我批评探测，以确定性初始响应为锚点 | RL训练使模型对高奖励路径形成依赖，被动探测无法有效扰动该路径；主动要求模型"自我批评"才能暴露其是否被困在单一推理模式中 |
| **核心度量** | 对数概率（PPL类）或编辑距离（CDD） | 令牌级熵（支持Top-K近似） | 熵直接捕捉预测分布的不确定性，对RL导致的分布稀疏化（策略坍塌）更敏感；对数概率受奖励解耦影响，编辑距离受生成长度和表面形式干扰 |
| **适用阶段** | 预训练/SFT | RL后训练 | 预训练/SFT直接优化对数似然，似然度信号有效；RL后训练优化奖励，需要测量路径依赖而非似然度 |

消融实验提供了因果证据支持这些设计选择：
- **移除初始响应锚点后，Self-Critique性能降至随机水平**（Figure 4），证明主动锚点探测是必要的——仅靠两次独立随机采样的熵比较无法区分污染与干净样本。
- **贪婪-贪婪采样策略在所有策略中表现最佳**（Figure 5），因为确定性解码排除了随机性干扰，使RL引起的策略坍塌信号更加纯粹。
- **Entropy-Temp和Entropy-Noise的AUC显著低于Self-Critique**（Table 2），表明仅靠随机性或外部扰动不足以可靠地打破高奖励路径依赖，需要模型自身在元指令引导下主动偏离。

### 3. 跨RL算法与跨模型的泛化边界

Self-Critique展现出对RL算法类型的强鲁棒性：
- 在**PPO、GRPO、DAPO**三种主流RL算法训练的Qwen2.5-3B-Instruct模型上，Self-Critique的平均AUC为0.60，超越最佳基线（Recall，0.51）约18%（Table 3）。
- 在**RLHF对齐场景**（UltraFeedback数据集，PPO/DPO/TDPO/RTO四种对齐算法）中，Self-Critique的AUC在0.62–0.70之间，始终优于所有基线（Table 8）。

跨模型泛化方面：
- **Qwen2.5-7B-Instruct**：平均AUC 0.70（+19% vs. Recall）
- **DeepSeek-Math-7B-Instruct**：平均AUC 0.64（+19% vs. Recall）
- **Qwen2.5-7B-Math**：平均AUC 0.74（+30% vs. Recall）
- **Llama-3.1-8B-Instruct**：K&K数据集AUC 0.81

方法对元指令措辞变化表现出高度鲁棒性（Table 9），不同提示下的AUC标准差仅为0.025左右，降低了实际部署中的提示工程负担。

### 4. 局限性与开放问题

**已识别的局限**：

1. **任务领域受限**：实验主要覆盖数学推理（AIME 2024/2025）和逻辑推理（Knights & Knaves、SAT），尚未在代码生成、机器翻译等具有更高解决方案多样性的领域验证有效性。这些领域中"正确推理路径"的定义可能更加多元，策略坍塌的表现形式可能不同。

2. **模型规模范围有限**：评估模型规模在0.5B至8B参数之间，虽具代表性但未涵盖数十亿至数百亿参数级别的前沿模型。大规模模型可能表现出不同的记忆和坍塌行为模式——一方面，更大的容量可能导致更严重的记忆；另一方面，更强的泛化能力可能削弱路径依赖。

3. **RL超参数敏感性未系统研究**：未探索不同学习率、批次大小、KL惩罚系数、温度参数等RL训练超参数对检测性能的影响。这些超参数直接影响策略坍塌的程度和形式。

4. **污染重复次数有限**：RL-MIA基准中的污染样本重复次数为2–4次，可能未完全模拟真实场景中更严重的数据重复污染。更高频次的重复可能导致更强的策略坍塌，但也可能使检测更容易。

5. **Top-K近似依赖**：虽然Top-K熵近似在K=3时已足够有效（Table 4），但该结论基于当前模型和任务得出，在词表分布差异较大的场景中可能需要重新验证。

**开放问题**：

- **跨领域泛化**：Self-Critique如何适应代码生成（多解性高）、翻译（约束强）等不同特性的任务？是否需要调整自我批评提示的设计范式？
- **规模扩展**：在100B+参数模型中，策略坍塌的表现是否一致？检测信号是否会因模型更强的推理能力而减弱或增强？
- **自适应K值选择**：能否根据模型词表分布、任务类型或生成长度自适应地选择Top-K近似的K值，在计算效率和检测精度之间实现动态最优平衡？
- **多信号融合**：能否将熵序列相似度与奖励分布特征、生成多样性指标、注意力模式等信号融合，构建更鲁棒的多模态检测器？
- **对抗鲁棒性**：如果攻击者知晓Self-Critique的检测机制，能否通过对抗训练或提示注入来规避检测？方法在灰盒和自适应攻击下的鲁棒性需要进一步评估。
- **实时检测与干预**：能否将Self-Critique从离线审计工具发展为在线训练监控机制，在RL训练过程中实时检测并阻止数据污染？

## 原文 PDF

![[paperPDFs/ICLR_2026/Detecting_Data_Contamination_from_Reinforcement_Learning_Post_training_for_Large_Language_Models.pdf]]
