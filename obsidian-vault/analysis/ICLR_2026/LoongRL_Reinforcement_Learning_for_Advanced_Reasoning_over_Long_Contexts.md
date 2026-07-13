---
title: "LoongRL: Reinforcement Learning for Advanced Reasoning over Long Contexts"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/LoongRL_Reinforcement_Learning_for_Advanced_Reasoning_over_Long_Contexts.pdf
project_link: https://loongrl.github.io/
code_link: null
openreview_forum_id: o29E01Q6bv
aliases:
- LoongRL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "KeyChain数据合成方法：通过在扩展的长上下文中插入高熵非语义的UUID链，将短多跳QA转化为需要逐步追踪链式关系、定位真实问题并检索推理的复杂任务，迫使模型习得结构化推理模式。"
primary_logic: "在KeyChain数据上进行GRPO强化学习能够稳定诱导出“计划-检索-推理-复查”的涌现推理模式；该模式具有跨长度泛化能力，使模型在16K上下文中训练后即可有效处理128K的长上下文推理任务。"
claims:
- "LoongRL在长上下文多跳QA上将Qwen2.5-7B-Instruct的准确率绝对提升23.5个百分点，14B版本提升21.1个百分点。"
- "KeyChain数据合成使模型产生逐步追踪UUID链以定位真实问题的推理行为，而非简单的语义捷径。"
- "在16K上下文上训练的LoongRL模型能够有效泛化至128K任务，在RULER-128K上达到79.92的准确率，远优于同尺寸基线。"
- "LongBench v1 (Long-Context Reasoning Average) 上 Accuracy (%) = 72.4 (LoongRL-7B)"
---

# LoongRL: Reinforcement Learning for Advanced Reasoning over Long Contexts

> [!tip] 核心洞察
> 在KeyChain数据上进行GRPO强化学习能够稳定诱导出“计划-检索-推理-复查”的涌现推理模式；该模式具有跨长度泛化能力，使模型在16K上下文中训练后即可有效处理128K的长上下文推理任务。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | LoongRL：面向长上下文高级推理的强化学习 |
| 英文题名 | LoongRL: Reinforcement Learning for Advanced Reasoning over Long Contexts |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=o29E01Q6bv) · [Project](https://loongrl.github.io/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | LoongRL |
| Dataset | LongBench v1 (Long-Context Reasoning Average), HELMET (Long-Context Generation Average) |

> [!tip] 效果简介
> - LongBench v1 (Long-Context Reasoning Average) 上，Accuracy (%) 为 72.4 (LoongRL-7B)，对比 48.9 (Qwen2.5-7B-Instruct)，变化 +23.5。
> - LongBench v1 (Long-Context Reasoning Average) 上，Accuracy (%) 为 74.2 (LoongRL-14B)，对比 53.1 (Qwen2.5-14B-Instruct)，变化 +21.1。
> - HELMET (Long-Context Generation Average) 上，Score 为 44.8 (LoongRL-7B)，对比 22.8 (Qwen2.5-7B-Instruct)，变化 +22.0。

## 概要

**问题瓶颈**：长上下文推理要求模型同时完成跨文档检索与深度推理，但现有强化学习方法主要针对短上下文设计，且缺乏高质量、高难度的长上下文训练数据，导致模型难以在长上下文中进行可靠推理。

**核心方法**：LoongRL 是一个面向长上下文高级推理的数据驱动强化学习方法。其关键创新在于 **KeyChain 数据合成方法**——通过在扩展的长上下文中插入高熵非语义的 UUID 链，将短多跳问答转化为需要逐步追踪链式关系、定位真实问题并检索推理的复杂任务。在 KeyChain 数据上采用 GRPO 强化学习训练，能够稳定诱导出**“计划-检索-推理-复查”**的涌现推理模式，且该模式具有跨长度泛化能力。

**方法定位**：LoongRL 属于基于强化学习的推理增强方法，区别于监督微调（SFT）或蒸馏路线（如 **R1-Distill-Qwen**，Guo et al., 2025），其通过多阶段课程 GRPO 训练，结合双向子串精确匹配奖励函数，在 16K 上下文上训练即可实现向 128K 上下文的泛化。

**主要结果**：
- 在长上下文多跳问答上，LoongRL 将 **Qwen2.5-7B-Instruct** 的准确率绝对提升 **+23.5 个百分点**（48.9 → 72.4），**14B 版本提升 +21.1 个百分点**（53.1 → 74.2），达到与 **o3-mini**（74.5）和 **DeepSeek-R1**（74.9）可比的前沿水平。
- 在 HELMET 长上下文生成基准上，7B 版本得分从 22.8 提升至 44.8（+22.0），14B 版本从 40.5 提升至 49.0（+8.5）。
- 仅在 16K 上下文上训练，LoongRL-14B 在 RULER-128K 上达到 **79.92** 的准确率，显著优于同尺寸基线；在 Needle-in-a-Haystack 测试中实现全深度全长度的 **100% 检索准确率**。

**局限与开放问题**：KeyChain 依赖人工构造的 UUID 链，其分布外泛化能力尚待验证；当前方法主要在问答任务上验证，对长文档摘要等开放生成任务的收益有待探索；超长上下文（>128K）下的推理模式泛化边界仍不明确。



大语言模型（LLM）的上下文窗口已扩展至百万Token级别，但**有效利用长上下文进行高级推理**仍然是尚未解决的核心挑战。当前模型在长上下文场景中面临一个双重瓶颈：既需要跨文档的精确检索能力，又需要基于检索结果进行深度多跳推理。然而，现有的强化学习推理方法（如DeepSeek-R1等）主要针对短上下文设计，缺乏高质量、高难度的长上下文训练数据，导致模型难以在长上下文中习得可靠的推理行为。

具体而言，问题的根源在于**训练数据的构造方式**。标准的多跳问答（Multi-hop QA）数据集虽然包含推理需求，但其上下文通常较短，且问题直接暴露给模型，模型可以通过语义捷径（如关键词匹配）而非真正的链式推理来作答。当这些数据被直接扩展至长上下文时，模型往往将检索与推理过程纠缠在一起，缺乏显式的规划步骤，导致错误频繁发生（Figure 1(b)）。

此外，现有的长上下文训练方法（如QwenLong-L1，Wan et al., 2025）主要依赖从强推理模型（如DeepSeek-R1）进行知识蒸馏，而非通过强化学习直接诱导模型自身的长上下文推理能力。这种方法受限于教师模型的能力边界，且无法产生超越蒸馏源的涌现行为。

LoongRL的核心动机在于：**通过精心设计的数据合成方法，将短多跳QA转化为需要逐步追踪链式关系的高难度长上下文任务，并利用强化学习直接训练模型，使其自发涌现出结构化的长上下文推理模式**。这一思路的关键洞察是：如果在训练数据中强制要求模型执行“追踪—检索—推理”的完整链条，模型将不得不放弃语义捷径，从而习得可泛化的推理策略。



## 核心方法与创新机理

LoongRL的核心创新在于提出了一种**数据驱动**的长上下文强化学习范式，通过三个关键环节的协同设计，解决了现有方法在长上下文推理中“检索与推理割裂、缺乏高质量训练数据”的瓶颈。

### 关键瓶颈与因果机制

长上下文推理的根本困难在于：模型需要同时完成**跨文档检索**和**深度推理**，但现有强化学习方法主要面向短上下文设计，且缺乏迫使模型进行结构化推理的高难度训练数据。LoongRL的因果调节变量是**KeyChain数据合成方法**——通过在扩展的长上下文中插入高熵、非语义的UUID链，将短多跳QA转化为需要逐步追踪链式关系、定位真实问题并检索推理的复杂任务。这一设计迫使模型无法依赖语义捷径，必须习得结构化的推理模式。

### 方法创新：三个Changed Slots

相较于基线方法，LoongRL在以下三个维度上做出了实质性改变：

**1. 训练数据构造：KeyChain增强（替代标准多跳QA上下文）**

传统多跳QA的上下文直接暴露问题与文档的语义关联，模型可通过表层匹配绕过深度推理。KeyChain方法的核心操作是：
- 从HotpotQA、MuSiQue、2WikiMultiHopQA等真实多跳QA数据集筛选种子样本；
- 在长上下文中插入多条UUID链（包含干扰链），仅一条链的末端指向真实问题；
- 模型必须从初始key出发，逐步追踪正确的UUID链，才能定位目标问题并完成检索与推理。

这一构造的关键性质是：标识符必须**高熵且非语义**（UUID或随机字符串均可，消融实验表明替换后性能几乎不变），从而阻断语义捷径，强制模型发展出逐步追踪的推理行为。

**2. 奖励函数：双向子串精确匹配（替代精确匹配或LLM裁判）**

奖励设计直接影响强化学习的优化方向。LoongRL采用规则化的二元奖励：

$$r_i = \begin{cases} 1 & \text{if } a \subseteq y_{\text{ans}} \lor y_{\text{ans}} \subseteq a \\ 0 & \text{otherwise} \end{cases}$$

即当模型提取的最终答案与参考答案互为子串时给1分，否则给0分。这一设计在**严格性**与**容错性**之间取得平衡：既避免了精确匹配对答案格式的过度敏感，又防止了LLM-as-a-judge可能引入的奖励黑客问题。消融实验（Table 6）证实，该方案在长上下文推理得分上优于精确匹配（72.4 vs 69.2）和LLM裁判。

**3. 训练算法与课程：多阶段课程GRPO（替代SFT或蒸馏）**

LoongRL采用基于GRPO的强化学习，并结合多阶段课程设计：
- **预热阶段**（仅7B模型）：在基础数据上初步提升检索推理能力；
- **KeyChain增强阶段**：引入KeyChain数据，诱导模型发展出高阶推理模式；
- **困难样本挖掘阶段**：动态淘汰已掌握样本，聚焦剩余难题，防止训练饱和。

训练在16K上下文长度下进行（以控制长序列rollout的计算成本），组大小G=8，学习率1e-6，采样温度0.6。

### 涌现的核心洞察

在KeyChain数据上进行GRPO训练，能够**稳定诱导出“计划-检索-推理-复查”的涌现推理模式**（Figure 1(a)）：模型首先生成明确的计划将问题分解为子步骤，然后逐步检索相关信息，进行推理，并主动复查中间结果。这一模式具有**跨长度泛化能力**——在16K上下文上训练的模型，可有效处理128K的长上下文推理任务（Table 4），且LoongRL-7B在Needle-in-a-Haystack基准上达到完美的100%检索准确率（Figure 3）。



![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_o29E01Q6bv/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our KeyChain data construction*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_o29E01Q6bv/figures/001_Figure_1.jpg]]
*Figure 1: Model trajectories on long-context multi-hop QA with and without KeyChain RL data. (a) With KeyChain data, model exhibits an emergent plan–retrieve–reason–recheck thinking pattern, improving reasoning reliability and can generalize to longer contexts. (b) Without KeyChain data, reasoning and retrieval are entangled, the model often lacks an explicit planning step and does not deeply reason over retrieved information, frequently leading to errors. Reasoning steps are marked in blue and retrieval steps in orange*

LoongRL 的整体框架围绕一个核心因果机制展开：**通过 KeyChain 数据合成方法将短多跳 QA 转化为高难度长上下文推理任务，再利用 GRPO 强化学习在多阶段课程下训练，诱导模型涌现出“计划-检索-推理-复查”的结构化推理模式**。该框架由三个关键模块串联构成，形成从数据构造到策略优化的完整闭环。

### 输入输出流

- **输入**：一个长上下文 $\mathcal{L}_i$（包含大量干扰文档和隐藏的 UUID 链式关系）、一个需要追踪链式关系才能定位的真实问题 $q_i$，以及对应的参考答案 $a_i$。训练数据集定义为 $\mathbb{D} = \{ \mathcal{L}_i, q_i, a_i \}$。
- **输出**：模型在给定 $\mathcal{L}_i$ 和 $q_i$ 的条件下，通过自主规划、逐步检索与推理，生成包含推理轨迹和最终答案的完整响应。最终答案通过双向子串精确匹配与参考答案进行验证。

### 模块关系

三个核心模块按以下流程协同工作：

1. **KeyChain Data Construction（数据构造模块）**  
   从 HotpotQA、MuSiQue、2WikiMultiHopQA 等真实多跳 QA 数据集中精选种子数据，通过在长上下文中随机插入多条高熵非语义的 UUID 链来隐藏原始问题。其中仅有一条链最终指向真实问题，其余为干扰链。模型必须从初始 key 出发，逐步追踪正确的链式关系以定位目标问题。该模块的泛化性体现在对标识符的具体形式不敏感——将 UUID 替换为随机字符串后性能几乎不变（Table 9）。

2. **Group Relative Policy Optimization — GRPO（策略优化模块）**  
   采用基于组奖励相对化的强化学习算法进行策略更新。对每个问题采样 $G=8$ 个 rollout，计算组内标准化的优势函数：
   $$A_{i,t} = \frac{r_i - \operatorname{mean}(\{r_1, r_2, \cdots, r_G\})}{\operatorname{std}(\{r_1, r_2, \cdots, r_G\})}$$
   奖励函数采用双向子串精确匹配：
   $$r_i = \begin{cases} 1 & \text{if } a \subseteq y_{\text{ans}} \lor y_{\text{ans}} \subseteq a \\ 0 & \text{otherwise} \end{cases}$$
   该设计在容忍答案表达形式变化的同时，有效避免了 LLM-as-a-judge 可能引入的奖励黑客问题。消融实验表明，双向子串匹配在长上下文推理上达到 72.4 分，优于精确匹配（69.2）和 LLM 裁判（Table 6）。

3. **Multi-Stage Curriculum（课程训练模块）**  
   训练上下文长度限制在 16K，通过多阶段课程逐步提升难度：
   - **Warm-up 阶段**（仅 7B 模型）：在标准多跳 QA 数据上初步提升检索与推理能力。
   - **Stage I（KeyChain 增强阶段）**：引入 KeyChain 数据，诱导模型习得结构化推理模式。
   - **Stage II（困难样本挖掘阶段）**：动态淘汰已掌握样本，聚焦困难样本防止过拟合。
   
   对于 14B 模型，跳过 warm-up 直接进行双阶段训练。训练过程中响应长度随步数稳步增长，反映模型逐步扩展检索与推理链（Figure 4）。

### 关键设计选择

- **训练上下文 16K 而非完整 128K**：避免全长度 RL rollout 的高计算成本，同时验证推理模式的跨长度泛化能力。
- **高熵非语义标识符**：KeyChain 的核心在于标识符的高熵和非语义特性，而非特定格式（如 UUID），这确保了模型习得的是通用的链式追踪能力而非格式记忆。
- **规则化奖励验证**：放弃 LLM-as-a-judge，采用双向子串匹配，在严格性与容错性之间取得平衡。

> **注意**：KeyChain 数据依赖人工构造的 UUID 链，其与真实世界长上下文推理多样性的分布外泛化能力尚待进一步验证；当前训练上下文限制在 16K，在极端 128K 上的性能可能未达上限。



### 3.1 KeyChain 数据构造

LoongRL 的核心瓶颈在于长上下文推理同时需要跨文档检索与深度推理，但现有强化学习方法主要针对短上下文，且缺乏高质量、高难度的长上下文训练数据。KeyChain 数据合成方法通过**因果操纵**解决了这一问题：在扩展的长上下文中插入高熵非语义的 UUID 链，将短多跳 QA 转化为需要逐步追踪链式关系、定位真实问题并检索推理的复杂任务，迫使模型习得结构化推理模式。

具体流程如下（Figure 2）：从 HotpotQA、MuSiQue 和 2WikiMultiHopQA 三个真实多跳 QA 数据集中筛选高质量种子数据，构成基础训练集 $\mathbb{D} = \{ \mathcal{L}_i, q_i, a_i \}$。KeyChain 在此基础上随机插入多条 key-value 链，其中仅一条链最终指向真实问题 $q_i$，其余为干扰链（从其他 QA 实例采样问题填充）。模型必须从初始 key 出发，沿正确链逐步追踪，才能定位隐藏的目标问题并回答。这一设计迫使模型发展出显式的规划与检索步骤，而非依赖语义捷径。

该方法对标识符的具体形式不敏感——将 UUID 替换为随机生成字符串后性能几乎不变（Table 9），关键属性在于标识符的高熵和非语义性。

### 3.2 长上下文强化学习

#### 3.2.1 奖励函数与 GRPO 优化

LoongRL 采用 Group Relative Policy Optimization（GRPO）进行策略优化，其目标函数为：

$$
\mathcal{J}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{(\mathcal{L}, \boldsymbol{q}, \boldsymbol{a}) \sim \mathcal{D}, \{\sigma_{\boldsymbol{a}}\}_{\mathrm{i}=1}^{G} \sim \pi_{\theta_{\mathrm{old}}}(\cdot \vert \boldsymbol{q})} \left[ \frac{1}{G} \sum_{i=1}^{G} \frac{1}{\vert \sigma_i \vert} \sum_{t=1}^{\vert \alpha_i \vert} \left( \min \left[ \rho_{i,t}(\theta) A_{i,t}, \mathrm{clip}(\rho_{i,t}(\theta), 1-\varepsilon, 1+\varepsilon) A_{i,t} \right] - \beta D_{\mathrm{KL}}(\pi_{\theta} \| \pi_{\mathrm{ref}}) \right) \right]
$$

其中 $\rho_{i,t}(\theta)$ 为新旧策略概率比，$A_{i,t}$ 为组优势估计，$\varepsilon$ 为裁剪参数，$\beta$ 控制 KL 惩罚强度以防止策略偏移。

组优势估计基于同一问题下 $G$ 个 rollout 的奖励标准化计算：

$$
A_{i,t} = \frac{r_i - \operatorname{mean}(\{r_1, r_2, \cdots, r_G\})}{\operatorname{std}(\{r_1, r_2, \cdots, r_G\})}
$$

奖励函数采用**双向子串精确匹配**规则：

$$
r_i = \begin{cases} 1 & \text{if } a \subseteq y_{\text{ans}} \lor y_{\text{ans}} \subseteq a \\ 0 & \text{otherwise} \end{cases}
$$

当模型提取的最终答案 $y_{\text{ans}}$ 与参考答案 $a$ 互为子串时给 1，否则给 0。这一设计在保持高精度的同时容忍答案表达形式的变化，避免奖励黑客。消融实验（Table 6）证实其优于严格精确匹配（72.4 vs 69.2）和 LLM-as-a-judge。

#### 3.2.2 多阶段课程训练

为避免全 128K RL rollout 的高计算成本，训练上下文长度限制为 16K，通过三阶段课程（7B 模型）或双阶段课程（14B 模型）逐步提升推理能力：

- **预热阶段**（仅 7B）：42 步，提升基本检索推理能力。
- **Stage I（KeyChain 增强）**：168 步，引入 KeyChain 数据诱导高阶推理模式。
- **Stage II（困难样本挖掘）**：118 步（7B）或 150 步（14B），动态淘汰已掌握样本，聚焦困难样本避免过拟合。

训练超参数：GRPO 组大小 $G=8$，学习率 $1\times10^{-6}$，rollout 温度 0.6，top-p=0.95，最大输出长度 4096 tokens。Figure 4 显示响应长度随训练稳步增长，反映模型逐步扩展检索与推理链；多阶段课程持续提供学习信号，防止性能饱和。



## 实验与关键发现

### 主要结果：长上下文推理的跨越式提升

LoongRL在长上下文多跳推理任务上取得了显著且一致的性能跃升。在LongBench v1的长上下文推理子集上，**LoongRL-7B**将基座模型**Qwen2.5-7B-Instruct**的平均准确率从48.9%提升至72.4%，绝对提升达**+23.5个百分点**；**LoongRL-14B**则从53.1%提升至74.2%，绝对提升**+21.1个百分点**（Table 2）。这一结果使7B/14B规模的模型直接达到了与前沿大模型**o3-mini**（74.5%）和**DeepSeek-R1**（74.9%）可比的水平，同时显著超越了基于蒸馏的**R1-Distill-Qwen-7B/14B**以及更大规模的**QwenLong-L1-32B**。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_o29E01Q6bv/figures/004_Table_2.jpg]]
*Table 2: Results of LoongRL and frontier LLMs on long-context reasoning and general short tasks. LoongRL delivers frontier-level long-context reasoning at much smaller scales (7B/14B), rivaling o3-mini and DeepSeek-R1, while preserving general short-context abilities across all scales*

在更具挑战性的长上下文生成基准HELMET上，LoongRL同样展现出强大的泛化能力。**LoongRL-7B**的平均得分从基线的22.8跃升至44.8（+22.0），**LoongRL-14B**从40.5提升至49.0（+8.5），在RAG、引用生成和长文档摘要等任务上均大幅领先同尺寸基线（Table 3）。这证明KeyChain数据诱导的推理模式不仅适用于抽取式QA，也能迁移至生成式长上下文任务。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_o29E01Q6bv/figures/005_Table_3.jpg]]
*Table 3: Results of LoongRL and frontier LLMs on the HELMET long-context generation benchmark. LoongRL-7B and LoongRL-14B substantially outperform baseline models*

### 跨长度泛化：16K训练，128K推理

一个关键发现是LoongRL展现出的卓越长度泛化能力。所有模型仅在**16K上下文长度**上进行RL训练，但推理时可直接扩展至128K。在NarrativeQA基准上，**LoongRL-7B**在32K-64K区间达到57.2%准确率，较基线的42.4%提升14.8个百分点（Table 4）。在RULER-128K上，**LoongRL-14B**达到79.92%准确率，显著优于**Qwen2.5-14B-Instruct**的73.57%，在所有14B-32B级别模型中表现最优（Table 8）。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_o29E01Q6bv/figures/006_Table_4.jpg]]
*Table 4: While being trained only on 16K, LoongRL generalizes impressively to context up to 128K*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_o29E01Q6bv/figures/026_Table_8.jpg]]
*Table 8: RULER benchmark results across different context lengths. For QwQ, QwenLong, Qwen2.5 model series, we report their YaRN variants for 64k and 128k*

Needle-in-a-Haystack实验进一步验证了这一泛化能力：**LoongRL-7B**在所有上下文长度（1K-128K）和所有文档深度（0%-100%）上均达到**100%完美检索准确率**（Figure 3），而基座模型Qwen2.5-7B-Instruct在部分深度/长度位置存在明显失败。**LoongRL-14B**同样达到全范围完美检索（Figure 9）。这表明涌现的“计划-检索-推理-复查”推理模式使模型获得了稳健的长程信息定位能力，而非依赖位置先验或语义捷径。

### 消融实验：KeyChain数据的核心作用

消融实验明确揭示了KeyChain数据的关键贡献。移除KeyChain数据后，仅使用标准多跳QA数据进行RL训练，模型在长上下文多跳QA上的平均得分从**72.4降至66.2**（-6.2），其中在MuSiQue（-8.3）和2WikiMultiHopQA（-7.0）等需要深度推理的任务上降幅尤为显著（Table 5）。这证实KeyChain数据中的UUID链追踪机制是诱导模型习得结构化推理模式的核心驱动力，而非简单的上下文扩展或数据增强。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_o29E01Q6bv/figures/015_Table_5.jpg]]
*Table 5: Ablation study on the effectiveness of KeyChain data*

关于KeyChain的设计选择，实验表明该方法对标识符的具体形式不敏感：将UUID替换为随机生成字符串后，模型性能几乎保持不变（Table 9）。这验证了核心机制在于标识符的**高熵非语义特性**——迫使模型必须通过逐步追踪链式关系来定位真实问题，而非依赖语义匹配。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_o29E01Q6bv/figures/028_Table_9.jpg]]
*Table 9: Analysis of the design choice of KeyChain data. The RL experiments are conducted on Qwen2.5-7B-Instruct*

### 奖励函数与训练课程的消融

奖励验证器的设计对RL训练效果有显著影响。双向子串精确匹配（Two-way Substring Exact Match）在7B模型上达到72.4的平均得分，优于严格精确匹配的69.2和F1评分的70.1，也优于LLM-as-a-judge方案（Table 6）。该设计在保持高精度的同时容忍答案表达形式的合理变化（如大小写、标点差异），有效避免了奖励黑客问题。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_o29E01Q6bv/figures/016_Table_6.jpg]]
*Table 6: Ablation study on the different answer verifiers on the 7B*

多阶段课程训练对持续提升至关重要。训练曲线（Figure 4）显示，长上下文推理准确率在三个阶段中持续增长，而非快速饱和。同时，模型的平均响应长度随训练步数稳步增加，反映出模型逐步扩展其检索与推理链的长度和复杂度。困难样本挖掘阶段（Stage III）通过动态淘汰已掌握样本、聚焦剩余难题，提供了持续的学习信号，防止模型在简单样本上过拟合。

### 涌现推理模式的行为证据

通过分析不同训练阶段的模型响应（Table 10），可以清晰观察到推理能力的逐步涌现过程：早期阶段模型主要进行简单的检索和直接回答；随着训练推进，模型开始展现显式的**规划**行为（将问题分解为子步骤）、**逐步检索**（按UUID链逐跳追踪）、**深度推理**（综合多跳信息得出结论）以及**主动复查**（验证中间结果的正确性）。这一“计划-检索-推理-复查”模式在KeyChain数据训练的模型上稳定涌现（Figure 1a），而未经KeyChain训练的模型则表现出检索与推理纠缠、缺乏显式规划、频繁出错的模式（Figure 1b）。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_o29E01Q6bv/figures/029_Table_10.jpg]]
*Table 10: Example responses of LoongRL-14B at different RL training steps, showing how retrieval, reasoning, rechecking, and planning behaviors evolve over training*

### 失败模式与局限

尽管LoongRL取得了显著进展，仍需注意以下局限：首先，KeyChain数据依赖人工构造的UUID链式结构，其分布外泛化能力——特别是面对真实世界中更复杂、非链式的长上下文推理场景——尚待进一步验证。其次，训练上下文长度限制在16K，虽已展现出色的128K泛化能力，但在极端超长上下文（>128K）上的性能上限尚未探明。此外，当前方法主要在问答任务上验证，对于长文档摘要、多轮对话等更开放的长上下文生成任务，收益程度仍需更多实验支持。最后，长序列RL rollout的计算成本较高，可能限制其在更大规模模型和更长训练上下文上的直接扩展。

### 补充图表

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_o29E01Q6bv/figures/003_Table_1.jpg]]
*Table 1: Data recipe for long-context RL training*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_o29E01Q6bv/figures/025_Table_7.jpg]]
*Table 7: Comparison of LoongRL models with other baselines on the LongBench-v2 benchmark, grouped by Difficulty, Length, and Task Type*



## 定位与知识库关联

### 1. 方法定位与核心差异

LoongRL 的核心定位是**面向长上下文高级推理的数据驱动强化学习框架**。与现有长上下文方法相比，其根本差异在于同时解决了两个耦合瓶颈：**高质量长上下文推理训练数据的缺失**，以及**短上下文推理方法在长上下文上的失效**。

现有长上下文方法大致分为两条路线：
- **检索增强路线**：通过改进检索器或分块策略提升信息定位能力，但缺乏深度推理。
- **推理增强路线**：如 **R1-Distill-Qwen-7B/14B**（Guo et al., 2025）和 **QwenLong-L1-32B**（Wan et al., 2025），通过从强推理模型（如 DeepSeek-R1）蒸馏获得推理能力，但蒸馏数据主要针对短上下文，长上下文推理能力有限。

LoongRL 的关键突破在于 **KeyChain 数据合成方法**：通过在扩展的长上下文中插入高熵非语义的 UUID 链，将短多跳 QA 转化为需要逐步追踪链式关系、定位真实问题并检索推理的复杂任务。这一设计迫使模型在 GRPO 强化学习过程中**自发涌现出“计划-检索-推理-复查”的结构化推理模式**（见 Figure 1），而非依赖外部蒸馏信号。

### 2. 与基线方法的关系

| 方法 | 类型 | 关键差异 |
|------|------|----------|
| **Qwen2.5-7B/14B-Instruct** (Qwen Team, 2024) | 指令微调基线 | 未经长上下文强化学习，缺乏结构化推理模式 |
| **R1-Distill-Qwen-7B/14B** (Guo et al., 2025) | 蒸馏推理模型 | 推理能力来自 DeepSeek-R1 蒸馏，但受限于短上下文训练数据 |
| **DeepSeek-R1** (Guo et al., 2025) | 前沿推理模型 | 规模更大（671B），推理能力更强，但未针对长上下文专门优化 |
| **o3-mini** (OpenAI) | 前沿推理模型 | 闭源，推理能力强，但长上下文推理的透明度有限 |
| **QwenLong-L1-32B** (Wan et al., 2025) | 长上下文 RL 模型 | 基于 R1 蒸馏，规模更大（32B），但 LoongRL-7B 以更小规模达到更高准确率（72.4 vs 66.0，Table 2） |

**关键性能对比**（Table 2）：
- LoongRL-7B 在 LongBench v1 长上下文推理平均准确率达到 **72.4**，超越所有 R1 蒸馏模型和 QwenLong-L1-32B（66.0），接近 o3-mini（74.5）和 DeepSeek-R1（74.9）。
- LoongRL-14B 达到 **74.2**，与 o3-mini（74.5）和 DeepSeek-R1（74.9）几乎持平，但模型规模仅为后者的约 1/50。

### 3. 适用边界

**已验证的有效范围**：
- **任务类型**：长上下文多跳 QA（HotpotQA、2WikiMultiHopQA、MuSiQue）、长文档问答（NarrativeQA、QASPER）、长上下文生成（HELMET 基准，含 RAG、引用生成、摘要）。
- **上下文长度**：训练上下文 16K，泛化至 128K 仍保持高性能（RULER-128K 上 LoongRL-14B 达 79.92，Table 8）。
- **模型规模**：在 7B 和 14B 上验证有效，通过涌现推理模式实现小规模模型的前沿性能。

**需要进一步验证的边界**：
- 超长上下文（>128K）下的推理模式衰减点尚不明确。
- 当前验证主要集中在问答任务，对于长文档摘要、多轮对话、代码调试等更开放的长上下文生成任务，收益有待进一步研究。
- KeyChain 数据依赖人工构造的 UUID 链，与真实世界长上下文推理的多样性可能存在分布差异，分布外泛化能力尚待验证。

### 4. 局限性与开放问题

**已知局限**：
1. **数据多样性**：KeyChain 的 UUID 链构造方式虽经消融验证对标识符具体形式不敏感（Table 9），但其“链式追踪”范式可能与某些真实场景（如法律条文推理、科学文献综合）的推理结构不完全匹配。
2. **训练成本**：GRPO 强化学习尤其是长序列 rollout 的计算成本较高，当前仅训练至 16K 上下文，直接扩展到 128K 训练可能面临资源瓶颈。
3. **任务覆盖**：主要收益在 QA 任务上，对于 HELMET 中的长格式生成任务虽有提升（7B 提升 +22.0，Table 3），但绝对分数（44.8）仍有较大提升空间。

**开放问题**：
1. **跨任务泛化**：如何将 KeyChain 思想扩展到非 QA 任务（如长格式文本生成、代码调试）以提升通用长上下文推理？
2. **超长上下文衰减**：涌现的“计划-检索-推理-复查”模式在 >128K 上下文下能泛化多远？是否存在性能衰减的临界点？
3. **训练效率**：能否通过更好的课程设计、离线 RL 或模型压缩技术提升 RL 训练效率，以支持更长的训练上下文？
4. **可解释性与迁移**：涌现的推理模式是否可被显式提取并用于指导其他模型的训练（如作为蒸馏目标或提示模板）？
5. **多语言与跨领域**：当前数据主要基于英文多跳 QA 数据集，在多语言和跨领域（如医疗、法律）场景下的泛化性能如何？

### 5. 在知识库中的定位

LoongRL 处于**长上下文推理**与**强化学习驱动的推理涌现**的交叉点。其核心贡献在于证明了：
- **数据设计驱动推理模式涌现**：通过 KeyChain 这种精心设计的合成数据，可以在 GRPO 框架下稳定诱导出结构化推理行为，而非依赖大规模蒸馏或人工提示工程。
- **长度泛化的可行性**：16K 训练即可泛化至 128K，表明涌现的推理模式具有跨长度迁移能力，这为低成本训练长上下文推理模型提供了新范式。
- **小模型的前沿性能**：7B/14B 模型即可接近或达到 o3-mini、DeepSeek-R1 等大模型的长上下文推理水平，为资源受限场景提供了可行方案。

与现有工作的关系上，LoongRL 可视为对 **DeepSeek-R1 蒸馏路线**（Guo et al., 2025）的补充和超越：蒸馏提供短推理能力，而 KeyChain + GRPO 提供长上下文推理的结构化模式。与 **QwenLong-L1**（Wan et al., 2025）相比，LoongRL 以更小的模型规模和更低的训练上下文长度实现了更高的长上下文推理性能，展示了数据驱动方法相对于纯蒸馏方法的优势。



## 原文 PDF

![[paperPDFs/ICLR_2026/LoongRL_Reinforcement_Learning_for_Advanced_Reasoning_over_Long_Contexts.pdf]]
