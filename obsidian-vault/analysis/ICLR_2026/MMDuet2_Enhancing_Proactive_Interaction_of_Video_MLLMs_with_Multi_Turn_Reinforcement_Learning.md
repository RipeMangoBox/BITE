---
title: "MMDuet2: Enhancing Proactive Interaction of Video MLLMs with Multi-Turn Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/MMDuet2_Enhancing_Proactive_Interaction_of_Video_MLLMs_with_Multi_Turn_Reinforcement_Learning.pdf
openreview_forum_id: rxQnMSNCUs
aliases:
- MMDuet2
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "采用多轮强化学习框架，设计包含PAUC、去重、跨度内和简洁前缀的复合奖励函数，自动优化模型在流式视频中回复的时机和内容质量，无需标注精确回复时间。"
primary_logic: "将主动交互形式化为基于聊天模板的纯文本对话，使模型在每个用户回合后自主决定回复或静默，从而兼容现有训练与推理框架；并利用强化学习应对缺乏精确回复时间标注的挑战。"
claims:
- "模型采用纯文本方式处理回复时机决策，输出“NO REPLY”或回复内容。"
- "通过强化学习，无需精确回复时间标注即可鼓励模型尽早生成正确回复。"
- "在多轮RL训练后，模型在ProactiveVideoQA和StreamingBench上显著超越现有基线，且保持了离线视频理解能力。"
- "StreamingBench Proactive Output 上 Accuracy = 34.69 (MMDuet2_rl)"
---

# MMDuet2: Enhancing Proactive Interaction of Video MLLMs with Multi-Turn Reinforcement Learning

> [!tip] 核心洞察
> 将主动交互形式化为基于聊天模板的纯文本对话，使模型在每个用户回合后自主决定回复或静默，从而兼容现有训练与推理框架；并利用强化学习应对缺乏精确回复时间标注的挑战。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MMDuet2：多轮强化学习增强视频MLLM主动交互 |
| 英文题名 | MMDuet2: Enhancing Proactive Interaction of Video MLLMs with Multi-Turn Reinforcement Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=rxQnMSNCUs) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | MMDuet2 |
| Dataset | StreamingBench Proactive Output, ProactiveVideoQA [WEB] |

> [!tip] 效果简介
> - StreamingBench Proactive Output 上，Accuracy 为 34.69 (MMDuet2_rl)，对比 29.44 (MMDuet)，变化 +5.25。
> - ProactiveVideoQA [WEB] 上，Reply Duplicate Proportion ↓ 为 4.2 (MMDuet2_rl)，对比 81.3 (MMDuet)，变化 -77.1。

## 概述

### 问题瓶颈

现有视频多模态大模型（Video MLLM）在主动交互场景中面临一个核心瓶颈：**回复时机的决策依赖手动设定的阈值和精确回复时间戳的监督训练**。这类方法不仅导致模型响应不及时、产生大量冗余回复，还难以泛化到不同领域和对话模式。例如，**VideoLLM-Online**（Chen et al., CVPR 2024）通过额外模块预测特殊令牌概率并与手动阈值比较来决定是否回复；**MMDuet**（Wang et al., 2024）虽在此前表现最优，但仍需依赖精确的时间戳标注构建训练数据。这种对精确时间标签的强依赖，使得主动交互系统的可扩展性受到严重制约。

### 核心方法

**MMDuet2** 针对上述瓶颈，提出两个关键机制：

1. **纯文本回复时机决策**：将主动交互形式化为基于聊天模板的纯文本对话。在每个用户回合，模型接收少量视觉帧和可选的文本输入，自主决定输出回复内容或“NO REPLY”以保持静默。这一设计使整个交互过程兼容现有主流训练与推理框架，无需修改底层结构。

2. **多轮强化学习优化**：在监督微调（SFT）之后，采用 GRPO（Group Relative Policy Optimization）强化学习框架，设计复合奖励函数自动优化回复时机与内容质量。奖励函数由四项加权组成：
   $$r = \omega_{PAUC} \times r_{PAUC} + \omega_{rep} \times r_{rep} + \omega_{in\_span} \times r_{in\_span} + \omega_{pfx} \times r_{pfx}$$
   其中 $r_{PAUC}$ 鼓励模型在正确的时间窗口内尽早给出正确回复，$r_{rep}$ 惩罚冗余重复回复，$r_{in\_span}$ 惩罚在有效时间窗口外的回复，$r_{pfx}$ 惩罚过长的回复前缀。该框架无需精确回复时间标注，通过奖励信号引导模型自主习得最优回复策略。

### 方法谱系与知识库定位

MMDuet2 在主动视频交互方法的演进中处于关键节点。其前身 **MMDuet** 建立了视频-文本二重奏交互格式，但依赖监督信号；**VideoLLM-Online** 率先探索流式视频主动问答，但使用额外的预测模块和手动阈值；**Dispider**（Qian et al., 2025）解耦感知、决策和反应模块；**TimeChat-Online**（Yao et al., 2025）则通过视觉令牌压缩处理流式交互。MMDuet2 的创新在于将强化学习引入主动交互训练，用奖励函数替代精确时间标注，同时保持纯文本决策的框架兼容性。这一设计使主动交互模型首次能够在无时间戳监督的条件下，通过试错学习优化回复时机。

### 主要结果

在 ProactiveVideoQA 基准的四个子集上，MMDuet2 的强化学习版本（MMDuet2_rl）显著超越现有基线。以 [WEB] 子集为例，PAUC 指标达到 53.3，同时将回复重复比例从 MMDuet 的 81.3% 降至 4.2%（降幅 77.1 个百分点）。在 StreamingBench 的 Proactive Output 任务上，MMDuet2_rl 以 34.69 的准确率超过 MMDuet 的 29.44（提升 5.25 个百分点）。消融实验表明，复合奖励的每个分量都不可或缺：移除重复惩罚（$r_{rep}$）使 [WEB] 重复比例从 4.2% 回升至 17.3%；移除跨度内惩罚（$r_{in\_span}$）在 [EGO] 子集上引发灾难性失败，模型几乎每轮都回复。同时，模型在多个离线视频理解基准上保持了原有性能，未出现灾难性遗忘。

### 局限与开放问题

当前方法存在若干局限：训练数据主要基于问答任务，尚未覆盖教学、体育指导等更复杂的主动交互场景；纯文本的“NO REPLY”决策方式在推理时引入额外计算开销；监控视频等复杂流场景中的主动响应性能仍有较大提升空间。开放问题包括：如何自动标注更精细的回复时间戳以提升监督信号质量，如何在不修改推理框架的前提下实现更高效的决策机制，以及如何将主动交互扩展到语音和情感等多模态信号。

## 背景与动机

视频多模态大语言模型（Video MLLM）在离线视频理解任务上取得了显著进展，然而在流式视频场景中，模型不仅需要理解内容，还需主动判断何时介入对话——这一能力被称为主动交互。现有方法在这一问题上存在根本性瓶颈：它们依赖手动设定的阈值与精确回复时间戳的监督训练，导致模型响应不及时、产生大量冗余回复，且难以泛化至新场景。

具体而言，以 **VideoLLM-Online**（Chen et al., CVPR 2024）为代表的首批流式主动问答模型，以及后续的 **Dispider**（Qian et al., 2025）和 **TimeChat-Online**（Yao et al., 2025），均采用额外模块预测特殊令牌概率或视觉令牌丢弃率，再与手动阈值比较来决定是否回复。这种设计带来两个固有问题：其一，阈值选择高度依赖经验，不同场景需反复调参；其二，训练过程需要精确标注的回复时间戳，而这类标注成本极高，限制了数据规模与场景覆盖。此前表现最优的 **MMDuet**（Wang et al., 2024）虽引入视频-文本二重奏格式，但仍未摆脱对精确时间标注的依赖。

上述问题的根源在于，现有方法将回复时机决策视为一个需要外部信号监督的独立预测任务，而非模型内在推理能力的自然延伸。这导致模型在推理时无法灵活权衡“何时说”与“说什么”，表现为两类典型失败模式：一是频繁输出冗余回复，在 ProactiveVideoQA 基准的 [WEB] 子集上，MMDuet 的回复重复比例高达 81.3%（Table 2）；二是因阈值设置保守而错失最佳回复窗口，造成响应延迟。

针对这一缺口，MMDuet2 提出两条核心动机：**将主动交互完全纳入文本对话范式**，使模型在每个用户回合后自主决定回复或静默，从而兼容现有训练与推理框架；**引入强化学习应对缺乏精确回复时间标注的挑战**，通过精心设计的复合奖励函数，鼓励模型尽早生成正确回复，同时惩罚冗余、越界和冗长前缀等不良行为。

## 核心创新

MMDuet2 的核心创新在于将主动视频交互中**回复时机的决策**从依赖特殊模块和手动阈值的工程化方案，转变为一种**完全基于文本的端到端范式**，并通过**多轮强化学习**在无需精确回复时间标注的条件下优化这一决策。这一设计在三个关键维度上实现了对现有方法的系统性改进。

### 从模块化决策到纯文本自主决策

现有主动交互方法普遍采用模块化解耦策略：**VideoLLM-Online**（Chen et al., CVPR 2024）将主动交互拆分为“看-说”两个独立步骤，依赖特殊令牌概率与手动阈值比较来决定回复时机；**Dispider**（Qian et al., 2025）进一步解耦为感知、决策和反应三个模块；**TimeChat-Online**（Yao et al., 2025）则通过视觉令牌丢弃率来控制响应。这些方案的共同缺陷在于：阈值设定依赖人工经验，难以泛化到不同场景；模块间的信息传递存在瓶颈，且无法与主流训练推理框架无缝兼容。

MMDuet2 的核心突破在于**将回复时机决策统一到语言模型的文本生成空间中**。具体而言，模型在每个用户回合后，接收少量视觉信息（1-2帧流式视频帧）和可选的用户文本，随后自主决定输出内容：可以生成有意义的文本回复，也可以输出“NO REPLY”表示本轮不回复。这一设计使得整个交互过程——包括视频输入、用户输入、回复时机决策和回复内容生成——被格式化为标准的 user/assistant 交替消息序列，从而**天然兼容现有的训练和推理框架**（如 SGLang、vLLM），无需任何架构层面的特殊适配。

这一纯文本决策范式的优势体现在两方面：其一，模型不再依赖外部模块或人工阈值，回复时机的判断完全由语言模型基于对视频内容和对话语境的理解自主完成，具备更强的泛化潜力；其二，统一的聊天模板使得模型可以在同一框架下同时学习“何时回复”和“回复什么”，避免了模块间优化目标不一致的问题。

### 从监督学习到强化学习：摆脱精确时间标注的依赖

监督微调（SFT）是现有方法的主要训练范式，但构建主动交互的监督数据面临一个根本性困难：**需要精确标注每一轮回复应该发生的时刻**。这一标注成本极高且主观性强——对于同一视频片段，不同标注者对“最佳回复时机”的判断可能存在显著差异。此前的**MMDuet**（Wang et al., 2024）虽然提出了视频-文本二重奏的交互格式，但其训练仍依赖精确的回复时间戳来构建监督信号，导致模型在回复时机上表现僵硬，容易产生大量冗余回复（如在ProactiveVideoQA [WEB]子集上，回复重复比例高达81.3%）。

MMDuet2 通过引入**多轮强化学习（GRPO）**从根本上绕开了这一难题。其核心设计在于：**不要求标注精确的回复时间，而是通过精心设计的奖励函数来引导模型学习合理的回复时机**。奖励函数由四个组件加权组合而成：

$$
\boldsymbol{r} = \omega_{PAUC} \times \boldsymbol{r}_{PAUC} + \omega_{rep} \times \boldsymbol{r}_{rep} + \omega_{in\_span} \times \boldsymbol{r}_{in\_span} + \omega_{pfx} \times \boldsymbol{r}_{pfx}
$$

其中，$\boldsymbol{r}_{PAUC}$ 是核心奖励，基于PAUC（Proactive Area Under Curve）指标设计。PAUC衡量模型回复正确性与及时性的综合表现：在标注的回复时间跨度 $[t^{start}, t^{end}]$ 内，模型越早给出正确回复，得分越高；在跨度外回复或回复错误则不得分。这一设计自然地鼓励模型在观察到足够信息后尽早做出正确响应，而无需指定精确的回复时刻。其余三项奖励分别用于惩罚不良行为：$\boldsymbol{r}_{rep}$ 惩罚重复回复，$\boldsymbol{r}_{in\_span}$ 惩罚在标注回复跨度之外的回复，$\boldsymbol{r}_{pfx}$ 惩罚过长的回复前缀（鼓励简洁性）。

RL训练使模型行为发生了质变。在ProactiveVideoQA [WEB]子集上，MMDuet2_rl 将回复重复比例从 SFT 基线的 81.3% 降至 4.2%（Table 2），同时 PAUC 从 44.1 提升至 53.3。消融实验（Table 6）进一步揭示了各项奖励的关键作用：移除 $\boldsymbol{r}_{rep}$ 导致 [WEB] 上重复比例回升至 17.3%，[EGO] 上回升至 31.9%；移除 $\boldsymbol{r}_{in\_span}$ 在 [EGO] 上引发灾难性失败，模型几乎每轮都回复；移除 $\boldsymbol{r}_{pfx}$ 则使 [EGO] 上 PAUC 从 33.6 降至 27.5。这些结果表明，复合奖励函数的设计是模型获得合理回复行为的关键。

### 从单一问答到多类型主动对话的数据构造

为支撑上述训练范式，MMDuet2 构建了包含约 52k 视频的主动对话数据集，设计了两种对话类型：**1QnA**（一个问题，多个答案）和 **nQnA**（多个问题，多个答案）。数据构造流程包括：视频场景分割与标注、基于场景描述的问答生成、以及主动对话构建。这一数据构造策略使得模型能够学习在不同粒度的问题上主动提供信息，而非被动等待用户逐一提问，为纯文本决策和强化学习优化提供了充分的训练素材。

### 创新边界与遗留问题

尽管纯文本决策带来了框架兼容性和泛化性的优势，但其代价是推理时额外的计算开销——模型需要为每一帧生成“NO REPLY”或回复内容。论文在附录中探讨了一种更高效的令牌级决策方案（预测 `<vis start>` 或 `<im end>` 来指示是否需要更多视觉信息），但该方案需要修改推理框架，增加了部署复杂度，被留作未来工作。此外，当前训练数据主要覆盖问答场景，尚未扩展到教学、体育指导等更复杂的主动交互场景，且强化学习的奖励权重依赖经验设定，训练中通过截取短视频段（20-60秒）来缓解稀疏奖励问题，可能影响长期依赖的建模能力。

## 整体框架

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_rxQnMSNCUs/figures/002_Table_1.jpg]]
*Table 1: Dataset Statistics*

MMDuet2 的整体框架围绕“将主动交互统一为纯文本对话”这一核心洞察构建，通过监督微调（SFT）与多轮强化学习（RL）两阶段训练，优化模型在流式视频中回复的时机与内容质量。其 pipeline 由数据构造、训练和推理三个层次有机衔接而成。

### 数据构造流水线

数据构造是方法的基础环节，包含三个顺序模块：

1. **视频场景分割与标注**：将每个视频 $V$ 划分为 $n$ 个独立场景 $[v_1, v_2, ..., v_n]$，并为每个场景生成详细描述 $[c_1, c_2, ..., c_n]$（见 **Figure 3** 的场景分割示例）。这一步骤为后续问答生成提供了结构化的视觉语义基础。

2. **问题-答案生成**：以所有场景描述为输入，利用大语言模型（LLM）生成一个问题 $q$ 及其对应的 $n$ 个答案列表 $[a_1, ..., a_n]$。每个答案 $a_i$ 可以是针对场景 $v_i$ 的具体回复，也可以是“NO REPLY”，表示该时刻无需响应。这一设计使得数据天然包含了对回复时机的隐式标注。

3. **主动对话构建**：将生成的问答列表转化为两类多轮交互数据——**1QnA**（一个问题，多个答案）和 **nQnA**（多个问题，多个答案）。前者模拟用户提问后模型在视频推进过程中逐步给出或推迟回复的场景；后者模拟更复杂的多轮主动交互。最终数据集包含约 52k 视频，涵盖网络视频和自我中心视频，统计信息见 **Table 1**。

### 训练流水线

训练阶段分为监督微调（SFT）和强化学习（RL）两个步骤，二者共享统一的聊天模板。

**聊天模板**（**Figure 2**）是框架的核心设计：它将视频输入、用户文本、回复时机决策和回复内容生成全部格式化为 `user` 和 `assistant` 交替的消息序列。在每个用户回合中，用户提供可选的文本内容以及来自在线视频的少量视觉信息（1-2 帧），随后助手自动发起自己的回合。助手可以选择输出文本回复，或输出 `NO REPLY` 表示当前轮次不回复。这一纯文本决策方式使得模型无需额外模块或手动阈值即可自主决定回复时机，同时兼容主流的训练与推理框架。

**SFT 阶段**：使用构造的对话数据和离线视频任务数据对基座模型进行监督微调。关键策略是将模型回复放置在回复时间窗口的末端，确保相关事件已经发生后再做出响应。SFT 在 16 块 H800 GPU 上约需 8 小时。

**RL 阶段**：采用 GRPO（Group Relative Policy Optimization）算法进行多轮强化学习，每次训练使用 4 个 rollout，基于 SGLang 和 verl 框架实现。为解决稀疏奖励和时间信用分配问题，每步训练仅从视频中截取 20 至 60 秒的短视频段。RL 的核心是复合奖励函数：

$$\boldsymbol{r} = \omega_{PAUC} \times \boldsymbol{r}_{PAUC} + \omega_{rep} \times \boldsymbol{r}_{rep} + \omega_{in\_span} \times \boldsymbol{r}_{in\_span} + \omega_{pfx} \times \boldsymbol{r}_{pfx}$$

其中：
- $\boldsymbol{r}_{PAUC}$（Proactive Area Under Curve）衡量回复正确性与及时性的综合得分，鼓励模型在正确的时间窗口内尽早给出正确回复；
- $\boldsymbol{r}_{rep}$ 惩罚重复回复，防止模型通过反复输出相同内容来刷高 PAUC；
- $\boldsymbol{r}_{in\_span}$ 惩罚超出合理时间窗口的回复，避免模型在无关时刻频繁发言；
- $\boldsymbol{r}_{pfx}$ 惩罚回复前缀过长，促使模型生成简洁直接的响应。

消融实验（**Table 6**）证实了各奖励项的必要性：移除 $\boldsymbol{r}_{rep}$ 导致 [WEB] 子集上回复重复比例从 4.2% 升至 17.3%，[EGO] 上从 8.1% 升至 31.9%；移除 $\boldsymbol{r}_{in\_span}$ 在 [EGO] 上引发灾难性失败，模型几乎每轮都回复；移除 $\boldsymbol{r}_{pfx}$ 使 [EGO] 上 PAUC 从 33.6 降至 27.5。

### 推理流水线

推理阶段严格遵循训练时的聊天模板。系统提示定义模型角色与行为规范，随后进入 `user` 和 `assistant` 的交替循环。每个用户回合输入当前视频帧和可选文本，助手回合则自主生成 `NO REPLY`（静默）或具体回复内容。这一设计使得 MMDuet2 能够无缝部署到现有推理框架中，无需修改底层代码。推理效率方面，在 [WEB] 子集上 MMDuet2 的端到端推理时间为 2 分 52 秒，与 MMDuet 的 2 分 27 秒基本可比（**Table 3**）。

### 关键设计优势

整个框架的核心优势在于将主动交互的“何时回复”和“回复什么”两个子问题统一为文本生成任务，从而：
- **消除对精确回复时间戳标注的依赖**：SFT 阶段仅需将回复放在时间窗口末端，RL 阶段通过 PAUC 奖励自动学习最优回复时机；
- **兼容现有基础设施**：聊天模板格式与主流 MLLM 训练和推理框架完全兼容；
- **避免手动阈值调参**：模型自主学会在适当时候输出 `NO REPLY`，无需外部模块预测特殊令牌概率并与阈值比较。

### 已知局限

- 训练数据主要集中在问答任务，尚未覆盖教学、体育指导等更复杂的主动交互场景；
- 纯文本的 `NO REPLY` 决策方式在推理时引入了额外的文本生成开销，更高效的令牌级决策需要修改推理框架；
- 模型在监控视频等复杂流场景中的主动响应性能仍有较大提升空间；
- RL 训练中奖励权重依赖经验设定，截取短视频段的策略可能影响长期依赖的建模。

## 核心模块与公式推导

### 纯文本回复时机决策模块

MMDuet2将主动交互中的回复时机决策完全形式化为基于文本的生成任务。在每一轮用户交互中，系统向模型提供当前视频帧的少量视觉信息（1-2帧）以及可选文本内容，随后模型自主决定：输出实质性的文本回复，或生成特殊标记 `NO REPLY` 表示本轮保持静默。这一设计将回复时机预测问题转化为标准的文本生成问题，无需额外的预测模块或手动阈值设定。

该方法的核心优势在于其**统一的聊天模板**（Chat Template）。整个交互过程——包括视频输入、用户输入、回复时机决策和回复内容生成——均被格式化为标准的 `user` 与 `assistant` 交替的消息序列。这使得MMDuet2能够直接兼容现有的多模态大语言模型训练与推理框架，无需修改底层架构。

### 多轮强化学习优化框架

在监督微调（SFT）之后，MMDuet2引入多轮强化学习来进一步优化模型的主动交互行为。SFT阶段将模型回复放置在对应回复时间窗的末端，以确保相关事件已经发生；然而，这种策略无法教会模型在时间窗内尽早做出正确回复。强化学习的设计动机正在于此：**在缺乏精确回复时间戳标注的条件下，通过奖励信号鼓励模型尽早生成正确回复，同时惩罚错误回复和过度延迟回复**。

训练采用GRPO（Group Relative Policy Optimization）算法，每次生成4个rollout，基于SGLang和verl框架实现。为缓解长视频序列中的稀疏奖励和时间信用分配问题，每步训练仅从视频中截取20至60秒的短片段。

### 复合奖励函数

总奖励函数由四个子奖励加权求和构成：

$$
\boldsymbol{r} = \omega_{PAUC} \times \boldsymbol{r}_{PAUC} + \omega_{rep} \times \boldsymbol{r}_{rep} + \omega_{in\_span} \times \boldsymbol{r}_{in\_span} + \omega_{pfx} \times \boldsymbol{r}_{pfx}
$$

各子奖励的含义与作用如下：

**PAUC奖励（$r_{PAUC}$）**：PAUC（Proactive Area Under Curve）是衡量主动回复质量的核心指标。给定一个回复时间窗 $[t^{start}, t^{end}]$，模型在窗内各时刻的回复得分构成一条折线，PAUC计算该折线下面积与最大可能面积之比：

$$
PAUC = \frac{ [(\tau_1 - t^{start}) \times 0.5 + \sum_{p=1}^{P-1} (\tau_{p+1} - \tau_p) \times s_p + (t^{end} - \tau_P) \times s_P] }{(t^{end} - t^{start}) \times S}
$$

其中 $\tau_p$ 为模型第 $p$ 次回复的时刻，$s_p$ 为该回复的正确性得分，$S$ 为最大可能得分。该指标同时衡量回复的**正确性**（得分越高越好）和**及时性**（越早正确回复，曲线下面积越大）。将 $r_{PAUC}$ 作为奖励信号，直接驱动模型学习在时间窗内尽早给出正确回复。

**去重奖励（$r_{rep}$）**：惩罚模型在时间窗内生成重复内容。若模型多次回复但内容高度重复，该奖励项为负值，迫使模型减少冗余输出。

**跨度内奖励（$r_{in\_span}$）**：惩罚模型在时间窗之外（即事件尚未发生或已经结束后）生成回复。该奖励项确保模型仅在适当的时间范围内做出响应。消融实验表明，移除该奖励在EGO数据集上会导致灾难性失败——模型几乎每轮都输出回复，完全丧失时机判断能力。

**前缀奖励（$r_{pfx}$）**：鼓励模型生成简洁的回复前缀，避免冗长的铺垫。消融实验显示，移除该奖励会导致EGO数据集上PAUC从33.6降至27.5，表明简洁性对主动交互质量有显著影响。

### 数据构建流水线

训练数据的构建分为三个关键步骤：

1. **视频场景分割与标注**：将视频划分为独立场景，并为每个场景生成详细的文本描述。
2. **问题-答案生成**：以所有场景描述为输入，使用大语言模型生成多跳问题及每个场景对应的答案列表（或 `NO REPLY`）。
3. **主动对话构建**：将问答列表转化为两类多轮交互数据——**1QnA**（一个问题，多个答案）和**nQnA**（多个问题，多个答案）——分别模拟单问题贯穿全视频和多问题连续交互的场景。

### 推理流程

推理阶段，系统按固定帧间隔（默认2秒）从流式视频中抽取帧，每帧作为一轮用户输入。模型在每轮后自主生成 `NO REPLY` 或回复内容。若生成回复，该回复作为助手消息加入对话历史；若生成 `NO REPLY`，则直接进入下一轮。整个流程由统一的聊天模板驱动，系统提示词定义了主动交互的行为规范。

## 实验与分析

### 主实验：主动交互性能

MMDuet2_rl在主动视频问答的两个核心基准上均显著超越现有方法，同时大幅抑制了冗余回复。

在**ProactiveVideoQA**基准上（Table 2），模型在四个子集上均取得最优PAUC（ω=0.5），同时将回复重复比例降至极低水平：

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_rxQnMSNCUs/figures/004_Table_2.jpg]]
*Table 2: Performance on ProactiveVideoQA. Metrics reported are PAUC (ω = 0.5) ↑/ reply duplicate proportion ↓, as defined in (Wang et al., 2025). †: Videollm-online generated more than 1 reply for only less than 10 answer turns on the [WEB], [EGO], and [VAD] datasets. Since the sample size is too small, we are not reporting this result as they have overly-large variance*

| 子集 | MMDuet2_rl PAUC↑ | MMDuet PAUC↑ | 重复比例↓ (ours vs MMDuet) |
|------|-----------------|-------------|---------------------------|
| [WEB] | 53.3 | 39.0 | 4.2 vs 81.3 |
| [EGO] | 33.6 | 23.9 | 8.1 vs 65.6 |
| [TV] | 43.4 | 41.4 | 1.0 vs 0.0 |
| [VAD] | 28.9 | 24.3 | 15.2 vs 50.0 |

关键发现：MMDuet虽在[TV]子集上重复比例极低，但其PAUC落后于MMDuet2_rl，且在其他子集上产生大量冗余回复（如[WEB]高达81.3%）。MMDuet2_rl在所有子集上将重复比例控制在15.2%以下，同时PAUC全面领先。

在**StreamingBench的Proactive Output**任务上（Table 5），MMDuet2_rl以34.69%的准确率超过MMDuet（29.44%）和Dispider（25.34%），提升幅度达+5.25个百分点。值得注意的是，MMDuet2_sft（仅监督微调）在该基准上仅为19.59%，表明强化学习阶段对回复时机决策的质量提升至关重要。

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_rxQnMSNCUs/figures/007_Table_5.jpg]]
*Table 5: Performance on Proactive Output task of Streaming-Bench*

### 离线能力保持

Table 4显示，经过SFT和RL两个阶段的训练后，MMDuet2在Video-MME、MVBench和LongVideoBench三个离线视频理解基准上的性能与原始Qwen2.5-VL 3B几乎持平，部分指标甚至略有提升（如Video-MME w/o subs从54.1升至55.1）。这表明多轮强化学习并未损害模型的通用视频理解能力，成功避免了灾难性遗忘。

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_rxQnMSNCUs/figures/006_Table_4.jpg]]
*Table 4: Performance on several popular offline video understanding benchmarks. †: Our implementations*

### 推理效率

Table 3对比了[WEB]子集上的推理端到端时间：MMDuet2平均生成3.3个回复轮次（标准差1.9），总耗时2分52秒；MMDuet平均生成5.7个回复轮次（标准差3.4），总耗时2分27秒。尽管MMDuet2的回复轮次更少，但由于纯文本“NO REPLY”决策方式在每轮仍需完整前向传播，总时间略高于MMDuet。这一开销是文本化决策机制的固有代价。

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_rxQnMSNCUs/figures/005_Table_3.jpg]]
*Table 3: Inference Wall Time on [WEB]*

### 消融实验：奖励函数各组分的作用

Table 6通过逐一移除奖励项，揭示了复合奖励函数中每个组分的不可替代性：

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_rxQnMSNCUs/figures/008_Table_6.jpg]]
*Table 6: Ablation studies on each reward item. Metrics reported are PAUC↑/ reply duplicate proportion ↓/num reply turns. Adverse consequences caused by removing a reward item are marked in red. ∗FAIL: The model generates response at almost every turn, regardless of whether truly relevant to the question. Evaluation on this task is unfeasible as inference on a single data point can take more than 20 minutes*

- **移除r_rep（去重奖励）**：在[WEB]上重复比例从4.2%飙升至17.3%，[EGO]上从8.1%升至31.9%。模型倾向于通过重复输出正确答案来获取更高的PAUC分数，验证了去重惩罚对抑制投机性重复的必要性。

- **移除r_in_span（跨度内奖励）**：在[EGO]上引发灾难性失败（FAIL*），模型几乎在每一轮都生成回复，完全丧失回复时机判断能力。这表明跨度约束是防止模型退化为“始终回复”策略的关键防线。

- **移除r_pfx（简洁前缀奖励）**：在[EGO]上PAUC从33.6降至27.5，说明前缀惩罚有效抑制了模型在回复前输出冗长无关前缀的行为，对回复及时性有实质贡献。

### 帧间隔的影响

Table 7分析了SFT、RL和推理阶段使用不同帧间隔的组合效应。核心结论：SFT阶段使用1秒帧间隔对性能至关重要——即使RL和推理阶段使用2秒间隔，只要SFT阶段使用1秒间隔，性能仍显著优于SFT阶段使用2秒间隔的所有配置。这表明密集的监督信号为后续强化学习提供了更精细的时序先验。

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_rxQnMSNCUs/figures/012_Table_7.jpg]]
*Table 7: Performance of using different frame interval for SFT, RL and inference*

### RL训练动态

Figure 5展示了RL训练过程中关键指标的变化趋势。随着训练推进，模型的PAUC逐步上升，同时回复频率和重复比例下降，表明复合奖励函数有效引导模型在“及时回复”与“避免冗余”之间取得了平衡。训练曲线未出现剧烈震荡，说明GRPO算法在该任务上具有稳定的收敛特性。

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_rxQnMSNCUs/figures/011_Figure_5.jpg]]
*Figure 5: Dynamics of key metrics of model behavior during RL training*

### 失败模式与局限

尽管整体表现优异，MMDuet2在[VAD]监控视频子集上的PAUC仅为28.9，远低于[WEB]的53.3，且重复比例（15.2%）相对较高。监控场景中事件稀疏、背景噪声大的特点对模型的场景理解与时机判断构成显著挑战。此外，模型在开放式对话和实时变化目标场景中的主动交互能力尚未验证，训练数据主要局限于问答范式。

## 方法谱系与知识库定位

### 1. 问题定位与核心瓶颈

MMDuet2 瞄准的是**流式视频中多模态大语言模型（Video MLLM）的主动交互**问题。传统视频理解模型通常被动等待用户提问，而主动交互要求模型在观看流式视频的过程中，自主判断何时发起回复以及回复什么内容。

该领域存在一个关键瓶颈：**现有方法依赖手动设定阈值与精确回复时间戳的监督训练**。具体而言，**VideoLLM-Online**（Chen et al., CVPR 2024）作为首个面向流式视频的主动问答模型，通过额外模块预测特殊令牌概率并与手动阈值比较来决定回复时机；**Dispider**（Qian et al., 2025）采用解耦感知、决策和反应的框架；**TimeChat-Online**（Yao et al., 2025）则基于视觉令牌压缩进行流式交互。这些方法共同面临三个问题：
- **响应不及时**：阈值难以适应复杂多变的视频内容；
- **冗余回复严重**：模型倾向于频繁输出，产生大量重复内容；
- **泛化能力弱**：对精确回复时间戳标注的依赖限制了数据规模和场景多样性。

MMDuet（Wang et al., 2024）在此前表现最优，但其同样依赖监督信号中的精确时间戳，未能从根本上解决上述问题。

### 2. 方法演进与关键改进

MMDuet2 在 MMDuet 的基础上进行了两个层面的根本性改进：

**第一，将回复时机决策完全文本化。** 此前方法（包括 MMDuet）需要额外模块预测特殊令牌或视觉令牌丢弃率，再与手动阈值比较。MMDuet2 将这一过程统一到聊天模板中：在每个用户回合后，模型自主输出 `"NO REPLY"` 表示静默，或输出具体回复内容。这一设计使整个交互过程——包括视频输入、用户输入、回复时机决策和回复内容生成——格式化为标准的 user/assistant 消息序列，天然兼容主流训练与推理框架（如 SGLang、vLLM）。

**第二，引入多轮强化学习替代纯监督训练。** 监督微调（SFT）需要精确标注的回复时间戳来构建训练数据，而 MMDuet2 在 SFT 之后采用 GRPO（Group Relative Policy Optimization）进行强化学习，通过精心设计的复合奖励函数自动优化回复时机和内容质量，**无需精确回复时间标注**。

### 3. 奖励函数设计与因果机制

MMDuet2 的强化学习奖励函数是其方法的核心创新，由四个组件加权构成：

$$r = \omega_{PAUC} \times r_{PAUC} + \omega_{rep} \times r_{rep} + \omega_{in\_span} \times r_{in\_span} + \omega_{pfx} \times r_{pfx}$$

- **$r_{PAUC}$（主动问答曲线下面积奖励）**：衡量模型在正确回复时间跨度内尽早给出正确回答的能力。PAUC 计算模型回复得分随时间变化的曲线下面积与最大可能面积之比，同时鼓励回复的正确性和及时性。
- **$r_{rep}$（去重奖励）**：惩罚模型在已回答正确后继续输出相同或相似回复的行为，直接针对冗余回复问题。
- **$r_{in\_span}$（跨度内奖励）**：惩罚在正确时间跨度之外的回复，防止模型在不相关时刻插话。
- **$r_{pfx}$（前缀长度奖励）**：惩罚回复中冗长的前缀（如重复描述已见内容），鼓励简洁直接的回答。

消融实验揭示了各奖励组件的因果作用：移除 $r_{rep}$ 导致 [WEB] 子集上回复重复比例从 4.2% 飙升至 17.3%，[EGO] 子集上从 8.1% 升至 31.9%；移除 $r_{in\_span}$ 在 [EGO] 上引发灾难性失败，模型几乎每轮都回复；移除 $r_{pfx}$ 使 [EGO] 上 PAUC 从 33.6 降至 27.5。

### 4. 与基线方法的关系

MMDuet2 在以下维度上区别于现有工作：

| 维度 | VideoLLM-Online | MMDuet | Dispider | TimeChat-Online | **MMDuet2** |
|------|-----------------|--------|----------|-----------------|-------------|
| 回复时机决策 | 特殊令牌概率+阈值 | 视频-文本二重奏格式 | 解耦感知/决策/反应 | 视觉令牌压缩 | **纯文本自主决策** |
| 训练范式 | 监督微调 | 监督微调 | 监督微调 | 监督微调 | **SFT + 多轮RL** |
| 是否需要精确时间戳 | 是 | 是 | 是 | 是 | **否（RL阶段）** |
| 奖励函数 | 无专门设计 | 对话文本相似度 | 无专门设计 | 无专门设计 | **四组件复合奖励** |

在 ProactiveVideoQA 基准上，MMDuet2_rl 在 [WEB] 子集上 PAUC 达到 53.3，远超 MMDuet 的 43.3；回复重复比例从 81.3% 降至 4.2%。在 StreamingBench 的 Proactive Output 任务上，准确率从 MMDuet 的 29.44 提升至 34.69。

### 5. 适用边界与局限

**适用场景**：MMDuet2 的设计主要面向**基于问答的主动交互**，训练数据来自 YouTube 和第一人称（Ego-Centric）视频，覆盖日常生活、教程、监控等场景。模型在 ProactiveVideoQA 和 StreamingBench 上表现优异，同时保持了离线视频理解能力（Table 4 显示后训练后离线基准性能几乎不变）。

**已知局限**：

1. **场景覆盖有限**：训练数据主要基于问答任务，尚未覆盖教学指导、体育训练等需要更复杂主动交互策略的场景。
2. **推理效率折衷**：纯文本 "NO REPLY" 决策方式在推理时引入额外计算开销。Table 3 显示，尽管 MMDuet2 平均回复轮次更少（3.3 vs 5.7），但推理端到端时间反而略长（2m52s vs 2m27s）。附录中提出了更高效的令牌级决策方案（预测 `<vis start>` 或 `<im end>`），但需要修改推理框架，增加了部署复杂度。
3. **复杂流场景性能不足**：在监控视频（[VAD]）等复杂流场景中，PAUC 仅为 28.9，主动响应性能仍有较大提升空间。
4. **奖励权重依赖经验**：四组件奖励的权重设置依赖人工调参，训练过程中需要处理稀疏奖励问题。当前通过截取 20-60 秒短视频段缓解，可能影响长期依赖的建模。
5. **帧间隔敏感**：Table 7 显示，推理帧间隔从 2 秒降至 1 秒可带来显著性能提升，但计算成本相应增加，需要在效率与性能间权衡。

### 6. 开放问题

1. **精细时间戳自动标注**：如何自动标注更精细的回复时间戳，以进一步提升监督信号质量？当前 RL 方法虽然绕过了这一需求，但更高质量的时间戳可能进一步提升 SFT 阶段的性能上限。
2. **高效回复时机决策**：能否在不修改现有推理框架的前提下，实现更高效的回复时机决策机制？附录中的令牌级方案提供了方向，但需要推理框架的原生支持。
3. **多模态主动交互扩展**：能否将主动交互扩展到语音和情感等多模态信号，实现更自然的人机交互？当前工作仅限于视觉-文本模态。
4. **持续学习与灾难性遗忘**：模型在处理开放式对话和实时变化的目标时，如何进行持续学习以避免灾难性遗忘？Table 4 虽然验证了离线能力的保持，但这是在固定数据集上的静态评估，未涉及动态场景下的持续适应。

## 原文 PDF

![[paperPDFs/ICLR_2026/MMDuet2_Enhancing_Proactive_Interaction_of_Video_MLLMs_with_Multi_Turn_Reinforcement_Learning.pdf]]
