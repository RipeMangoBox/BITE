---
title: "MemAgent: Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/MemAgent_Reshaping_Long_Context_LLM_with_Multi_Conv_RL_based_Memory_Agent.pdf
project_link: null
code_link: null
openreview_forum_id: k5nIOvYGCL
aliases:
- MemAgent
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "通过强化学习优化一个固定长度的记忆单元，使模型能够在分块处理时选择性地保留关键信息并丢弃冗余内容，从而实现线性复杂度的无限长文本处理。"
primary_logic: "灵感来源于人类阅读长文本时做笔记并选择性记忆的方式：将文档分块，用固定大小的记忆总结关键信息，最后基于记忆生成答案。通过端到端强化学习训练模型学会最优的记忆更新策略。"
claims:
- "RL-MEMAGENT 从 8K 训练窗口外推到 3.5M token 的 QA 任务，性能损失不到 10%（7K 时 80.47% 降至 3.5M 时 71.09%）。"
- "在 512K NIAH 测试中取得超过 95% 的准确率，而同期开源长上下文模型（如 Qwen2.5-Instruct-1M）性能大幅下降。"
- "在 RULER-HQA 上，基线模型（如 Qwen2.5-Instruct-14B-1M）在 896K 时准确率降至 0%，而 RL-MEMAGENT 在 3.5M 时仍保持 71.09% 准确率。"
- "RULER-HQA 上 Accuracy (%) = RL-MEMAGENT-14B: 80.47 (7K), 75.78 (896K), 71.09 (3.5M)"
---

# MemAgent: Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent

> [!tip] 核心洞察
> 灵感来源于人类阅读长文本时做笔记并选择性记忆的方式：将文档分块，用固定大小的记忆总结关键信息，最后基于记忆生成答案。通过端到端强化学习训练模型学会最优的记忆更新策略。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MemAgent：基于多对话强化学习的记忆代理重塑长上下文大语言模型 |
| 英文题名 | MemAgent: Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=k5nIOvYGCL) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | MEMAGENT |
| Dataset | RULER-HQA, LongBench-QA, NIAH (512K) |

> [!tip] 效果简介
> - RULER-HQA 上，Accuracy (%) 为 RL-MEMAGENT-14B: 80.47 (7K), 75.78 (896K), 71.09 (3.5M)，对比 Qwen2.5-Instruct-14B-1M: 60.16 (7K), 0.00 (896K); Qwen2.5-Instruct-14B: 75.00 (7K), 2.34 (896K)，变化 PROPOSED 性能仅轻微下降（<10%），基线在超长上下文崩溃至 0%。。
> - LongBench-QA 上，AVG Score 为 MEMAGENT-14B: 51.0; MEMAGENT-7B: 48.2，对比 QwenLong-L1-32B: 50.7; DS-Distill-Qwen-32B: 49.0，变化 PROPOSED 以较小的模型规模超越了最强大的长上下文基线。。
> - NIAH (512K) 上，Accuracy 为 RL-MEMAGENT: >95%，对比 Qwen2.5-Instruct-1M 系列在 512K 时出现明显下降，变化 PROPOSED 几乎无性能损失，基线显著下降。。

## 概要

长上下文大语言模型在处理超长文本时面临两个根本性瓶颈：注意力机制的二次复杂度（$O(n^2)$）使推理成本随长度急剧膨胀，而现有长度外推、稀疏注意力和上下文压缩等方法在上下文超过训练窗口后性能严重衰减。本文提出 **MEMAGENT**，一种受人类阅读做笔记行为启发的智能体工作流：将文档分块流式输入，通过固定长度的记忆单元（默认 1024 tokens）选择性保留关键信息并覆盖冗余内容，最后仅依据记忆生成答案。这一设计将端到端复杂度降至 $O(N)$ 线性级别。

核心洞察在于将记忆的“覆写决策”形式化为强化学习问题——通过端到端优化，让模型学会在分块处理时自主判断哪些信息值得保留、哪些可以丢弃。为此，作者扩展了 DAPO 算法，提出 **Multi-Conv DAPO**：在 rollout 阶段为每个样本生成多个上下文无关的对话，以最终答案的规则奖励（等价判据）联合优化所有对话，从而训练出鲁棒的跨上下文记忆能力。

**关键实证结论**：
- 仅用 8K 上下文窗口训练的 RL-MEMAGENT，在 RULER-HQA 基准上外推至 **3.5M tokens** 时准确率仅从 80.47% 降至 71.09%（损失 <10%），而同期 1M 上下文基线模型（如 Qwen2.5-Instruct-14B-1M）在 896K 时已崩溃至 0%。
- 在 512K NIAH 测试中取得 **超过 95%** 的准确率，几乎无性能衰减。
- 在 LongBench-QA 上以 14B 参数规模（51.0 平均分）超越 32B 的长上下文微调模型（QwenLong-L1-32B，50.7 分），展现出极强的参数效率。

消融实验进一步证实：移除 RL 训练后模型在长文本上性能大幅下降，说明 RL 是鲁棒记忆能力的关键来源；记忆长度在 256–4096 tokens 范围内性能稳健，1024 tokens 为最佳平衡点；关键信息在上下文中的位置（0%–100%）对 MEMAGENT 影响极小，未出现灾难性遗忘。



### 长上下文LLM的核心瓶颈

大语言模型（LLM）在处理长文本时面临一个根本性矛盾：注意力机制的二次复杂度（$O(n^2)$）使得原生全上下文推理的计算成本随文本长度急剧膨胀，而现有应对方案在超长上下文场景下普遍存在性能崩溃问题。

当前主流的长文本处理范式可分为三类：

- **长度外推（Length Extrapolation）**：通过位置编码扩展（如RoPE缩放）使模型在训练窗口之外进行推理。然而，如Figure 1所示，即便是经过长上下文持续预训练和外推技术强化的模型（如**Qwen2.5-Instruct-14B-1M**，Yang et al., 2025），在RULER-HQA基准上从7K扩展到896K时，准确率从60.16%骤降至0.00%——模型完全失效。
- **稀疏注意力（Sparse Attention）**：通过跳过部分注意力计算降低复杂度，但信息丢失风险随上下文增长而累积，无法保证关键信息的可靠保留。
- **上下文压缩（Context Compression）**：将长文本压缩为短表示，但压缩过程中的信息损失在超长文档场景下被放大，且缺乏端到端的优化信号来指导“保留什么、丢弃什么”。

这些方法的共同缺陷在于：它们试图在固定的模型架构约束内“硬撑”更长的上下文，而非从根本上改变信息处理的方式。随着上下文长度向百万token级别延伸，性能衰减成为系统性现象，而非个别模型的工程问题。

### 人类阅读的启示：记忆作为信息瓶颈

本文的核心洞察来源于一个朴素的类比：人类在阅读长文档时，并不会一次性将所有内容装入工作记忆。相反，我们会边读边做笔记，用固定容量的外部记忆选择性保留关键信息，最终基于笔记回答问题。这一过程天然具有三个优势：

1. **线性复杂度**：阅读成本与文档长度成线性关系，而非二次关系。
2. **信息筛选**：记忆充当信息瓶颈，强制模型区分关键信号与冗余噪声。
3. **泛化能力**：记忆策略一旦习得，理论上可泛化到任意长度的文档，因为处理每段文本的认知负载是恒定的。

将这个类比迁移到LLM，核心问题转化为：**能否通过训练，使模型学会在分块读取文本时，动态更新一个固定长度的记忆单元，使得最终仅凭记忆即可正确回答任意长度上下文中的问题？**

### 从类比到可训练机制

将上述直觉转化为可优化的机器学习系统，需要解决两个关键挑战：

**挑战一：记忆更新策略如何优化？** 传统的监督微调（SFT）只能教模型“模仿”某种记忆行为，但无法提供关于“记忆质量”的直接反馈——模型是否记住了正确的内容，只有在最终答案的准确性上才能体现。这暗示强化学习（RL）是更合适的优化范式：以任务完成的正确性作为奖励信号，端到端地优化整个记忆更新轨迹。

**挑战二：如何为记忆轨迹提供有效的训练信号？** 单个长文档的问答只产生一个稀疏的最终奖励，难以有效指导分步的记忆更新决策。本文通过**多对话强化学习（Multi-Conv RL）** 解决这一问题：在训练时，每个样本生成多个上下文无关的对话，共享同一奖励信号进行联合优化，从而放大有效的学习信号（见Figure 3）。

### 本工作的定位

本文提出**MEMAGENT**，一个基于强化学习的记忆代理框架。其核心设计原则是：

- 将文档分块处理，每块与固定长度的记忆（默认1024 tokens）交互，实现$O(N)$线性复杂度（见公式(4)的分解）。
- 通过多对话DAPO算法端到端优化记忆更新策略，使模型学会在分块读取中主动识别、保留和覆盖关键信息。
- 训练时仅使用8K上下文窗口，测试时外推至3.5M tokens，验证记忆策略的泛化性而非上下文窗口的硬扩展。

后续章节将详细展开MEMAGENT的工作流设计、训练算法，以及在检索型QA、摘要和Needle-in-a-Haystack等任务上的实验验证。



## 核心方法与创新机理

### 问题瓶颈：长上下文处理的根本困境

当前主流的长文本处理方法——包括长度外推（length extrapolation）、稀疏注意力（sparse attention）和上下文压缩（context compression）——在面对无限长文档时面临两个根本性瓶颈。其一，**注意力机制的二次复杂度**（$O(n^2)$）使得推理的计算开销随上下文长度急剧膨胀，阻碍高效推理。其二，即使是通过长上下文继续预训练扩展窗口的模型（如 **Qwen2.5-Instruct-1M** 系列，Yang et al., 2025），在实际超长文本任务中性能依然严重退化：Table 1 显示，Qwen2.5-Instruct-14B-1M 在 7K 上下文时准确率为 60.16%，到 896K 时直接崩溃至 0.00%。这表明单纯扩大上下文窗口并未从根本上解决长程依赖建模问题。

### 核心洞察：仿人类选择性记忆机制

MEMAGENT 的核心洞察源自对人类阅读长文档行为的观察：**人类并非一次性将整本书装入大脑，而是分块阅读，通过做笔记的方式选择性记录关键信息，最后基于笔记回答问题**。这一隐喻直接催生了三个关键设计选择：

1. **分块流式处理**：将任意长度的文档视为受控的证据流，每次仅暴露当前文本块和固定大小的记忆，而非一次性加载全文。
2. **固定长度记忆覆写**：记忆容量恒定（默认 1024 tokens），模型必须学会在有限空间中覆写旧信息以保留新关键信息，这迫使模型发展出信息筛选能力。
3. **端到端强化学习优化**：将“覆写决策”形式化为强化学习问题，通过最终答案的正确性奖励来优化整个记忆更新策略，而非依赖启发式规则。

### 关键方法创新：Multi-Conv DAPO 与线性复杂度分解

相对于基线方法，MEMAGENT 在两个关键维度上实现了根本性改变：

**Changed Slot 1：上下文处理策略——从 $O(n^2)$ 到 $O(N)$ 线性复杂度**

基线方法（包括长上下文微调模型和推理蒸馏模型）直接在全长上下文中采用标准自回归注意力，计算复杂度随序列长度呈二次增长。MEMAGENT 将这一范式替换为基于固定记忆的线性复杂度处理：输入文本被划分为 $K$ 个连续块 $\mathbf{c}^1, \dots, \mathbf{c}^K$，每步的上下文窗口仅包含当前块 $\mathbf{c}^k$ 和上一轮记忆 $\mathbf{m}^{k-1}$。由于记忆长度 $M$ 恒定，每步计算量为 $O(C+M)$，整体复杂度为 $O(N)$，其中 $N$ 为文档总长度。这一分解由以下概率模型形式化表达（§2.3, Eq 4）：

$$p(\mathbf{x}_{1:N}) = \sum_{\mathbf{m}^{1:K-1}} \prod_{k=1}^{K} \underbrace{p(\mathbf{c}^k \mid \mathbf{m}^{k-1})}_{\text{read}} \underbrace{p(\mathbf{m}^k \mid \mathbf{c}^k, \mathbf{m}^{k-1})}_{\text{write}}$$

该分解将自回归语言模型重构为“读-写”两步迭代过程：读取当前块并理解其内容，然后更新记忆以选择性保留关键信息。

**Changed Slot 2：训练目标与算法——从监督微调到多对话强化学习**

基线方法依赖标准的下个 token 预测或监督微调，缺乏显式的记忆优化机制。MEMAGENT 引入 **Multi-Conv DAPO** 算法（基于 DAPO 扩展，Yu et al., 2025），以规则奖励端到端优化记忆更新策略。其核心创新在于：

- **多对话联合优化**：每个训练样本生成多个上下文无关的对话，最终对话的答案用于计算奖励 $R(\hat{y}, y) = \mathbf{1}_{\mathrm{is.equiv}(\mathbf{y}, \hat{\mathbf{y}})}$，该奖励通过优势函数 $\hat{A}_{i,j,t} = R_i - \mathrm{mean}(\{R_i\}_{i=1}^G)$ 反向传播至所有前置对话，使模型学会在每轮对话中做出有利于最终任务的记忆更新决策。
- **两阶段课程 RL**：第一阶段在基础记忆任务上获取记忆能力，第二阶段将能力迁移至多样化上下文和任务，训练过程中模型始终被限制在 8K 上下文窗口内，以验证外推能力。

### 决定性证据

MEMAGENT 的创新有效性由以下关键实验证据支撑：

1. **极限外推能力**（置信度 0.99）：RL-MEMAGENT-14B 从 8K 训练窗口外推到 3.5M token 的 RULER-HQA 任务，准确率仅从 80.47% 降至 71.09%（性能损失 < 10%）。相比之下，最强基线 Qwen2.5-Instruct-14B-1M 在 896K 时已降至 0.00%（Table 1）。

2. **512K 检索鲁棒性**（置信度 0.95）：在 NIAH 基准测试中，RL-MEMAGENT 在 512K 上下文长度下取得超过 95% 的准确率，而同期开源长上下文模型性能大幅下降（Figure 5）。

3. **RL 训练的因果作用**（置信度 0.95）：消融实验显示，移除 RL 训练后 MEMAGENT 在长文本上性能随长度增长大幅下降（Figure 6, 7），直接证明 RL 是记忆鲁棒性的关键驱动因素。

4. **小模型超越大基线**（置信度 0.98）：MEMAGENT-14B 在 LongBench-QA 上取得 51.0 的平均分，超越了 32B 级别的长上下文基线 QwenLong-L1-32B（50.7）和 DS-Distill-Qwen-32B（49.0）（Table 3），表明记忆机制比模型规模对长文本任务更为关键。



![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_k5nIOvYGCL/figures/002_Figure_2.jpg]]
*Figure 2: MEMAGENT is inspired by the way humans process long documents. It divides the document into multiple chunks and allows LLMs to process them iteratively, recording relevant information in memory. Finally, LLMs generate answers based on the information stored in the memory*

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_k5nIOvYGCL/figures/004_Figure_4.jpg]]
*Figure 4: The architecture and graphic model of MEMAGENT. The memory is modeled as a latent memory variable, thereby enabling the decomposition of the autoregressive language model into multiple steps of reading from and writing to the memory*

MEMAGENT 将任意长度的文档视为一个受控的证据流，通过分块迭代的方式处理文本，其核心流水线由三个模块构成：**上下文处理模块**（Context-Processing Module）、**固定长度记忆**（Memory）和**答案生成模块**（Answer-Generation Module）。

**处理流程。** 输入文档被切分为 $K$ 个连续文本块 $\mathbf{c}^1, \dots, \mathbf{c}^K$（每块长度不超过 $C$），模型逐块处理。在第 $k$ 步，模型同时接收当前文本块 $\mathbf{c}^k$ 和上一轮产生的记忆 $\mathbf{m}^{k-1}$，通过特定的 prompt 模板（Table 5, top）指导模型读取新信息并覆写记忆，生成更新后的记忆 $\mathbf{m}^k$。当所有文本块处理完毕后，答案生成模块被调用：模型仅依据问题陈述和最终记忆 $\mathbf{m}^K$ 生成答案（Table 5, bottom）。整个流程的设计灵感直接来源于人类阅读长文档时“做笔记、选择性记忆、最后凭笔记作答”的方式（Figure 2）。

**记忆的固定长度约束。** 记忆 $\mathbf{m}^k$ 被设定为固定长度的令牌序列（默认 $M = 1024$ tokens），不随输入长度增长而膨胀。这一约束带来了两个关键性质：（1）每步计算量恒定，仅为 $O(C + M)$，端到端复杂度与文本块数量呈线性关系 $O(N)$；（2）模型被迫学习选择性保留策略——通过覆写而非追加的方式更新记忆，必须判断哪些信息值得保留、哪些可以丢弃。

**概率图模型视角。** 从概率建模的角度，MEMAGENT 将自回归语言模型的似然分解为基于固定长度记忆的读写步骤（Figure 4, Eq (4)）：

$$p(\mathbf{x}_{1:N}) = \sum_{\mathbf{m}^{1:K-1}} \prod_{k=1}^{K} \underbrace{p(\mathbf{c}^k \mid \mathbf{m}^{k-1})}_{\text{read}} \underbrace{p(\mathbf{m}^k \mid \mathbf{c}^k, \mathbf{m}^{k-1})}_{\text{write}}$$

其中记忆 $\mathbf{m}^k \in \mathcal{V}^M$ 替代了无界的历史上下文，作为隐变量连接各文本块。这一分解使得模型能够以线性复杂度处理无限长输入，同时通过记忆机制保持跨块的信息传递。

**与强化学习的接口。** 记忆的覆写决策被形式化为一个强化学习问题：模型需要学习生成一条使最终答案奖励最大化的“读取-写入”记忆轨迹。训练时，答案生成模块的输出 $\hat{y}$ 与标准答案 $y$ 通过规则验证器进行等价性判断，得到二元奖励 $R(\hat{y}, y) = \mathbf{1}_{\mathrm{is.equiv}(y, \hat{y})}$（Eq (3)）。这一奖励信号通过多对话 DAPO 算法反向传播至整个记忆更新轨迹，驱动模型学会最优的记忆选择策略（详见 §2.2）。

**关键设计选择。** 默认配置中，记忆长度设为 1024 tokens，上下文块大小设为 5000 tokens。训练时模型被刻意限制在 8K 上下文窗口内，以验证其外推能力——即在小窗口习得的记忆策略能否泛化到远超训练长度的输入。



### 流水线模块

MEMAGENT 的工作流由三个核心模块构成，模拟人类阅读长文档时做笔记并选择性记忆的方式（Figure 2）：

1. **Context-Processing Module（上下文处理模块）**：模型以固定大小的文本块（chunk）为单位迭代读取输入文档。在每一步，模型仅接收两个输入——下一个文本块 $\mathbf{c}^k$ 和上一轮产生的记忆 $\mathbf{m}^{k-1}$，然后生成更新后的记忆 $\mathbf{m}^k$。该模块通过一个提示模板（Table 5, top）引导模型完成“读取-写入”操作。

2. **Memory（记忆单元）**：一个固定长度的 token 序列 $\mathbf{m} \in \mathcal{V}^M$，默认长度 $M = 1024$ tokens。记忆采用覆写（overwrite）策略——每次更新时模型自主决定保留哪些旧信息、写入哪些新信息，记忆长度始终保持不变。这保证了每步计算量为常数，端到端复杂度为线性。

3. **Answer-Generation Module（答案生成模块）**：当输入流结束后，模型仅依据问题陈述和最终记忆 $\mathbf{m}^K$ 生成答案（Table 5, bottom），不再访问原始文档。

### 核心公式

#### 1. 基于记忆的序列似然分解

MEMAGENT 将标准自回归语言模型的似然重新分解为基于固定长度记忆的读写步骤（Figure 4）。给定长度为 $N$ 的序列 $\mathbf{x}_{1:N}$，将其划分为 $K$ 个连续块 $\mathbf{c}^1, \dots, \mathbf{c}^K$（每块长度 $\leq C$），引入隐记忆变量 $\mathbf{m}^k$：

$$p(\mathbf{x}_{1:N}) = \sum_{\mathbf{m}^{1:K-1}} \prod_{k=1}^{K} \underbrace{p(\mathbf{c}^k \mid \mathbf{m}^{k-1})}_{\text{read}} \underbrace{p(\mathbf{m}^k \mid \mathbf{c}^k, \mathbf{m}^{k-1})}_{\text{write}}$$

- **read 项**：在给定上一轮记忆 $\mathbf{m}^{k-1}$ 的条件下“读取”当前块 $\mathbf{c}^k$。
- **write 项**：基于当前块和上一轮记忆，生成更新后的记忆 $\mathbf{m}^k$。

由于 $|\mathbf{m}^k| = M$ 为常数，每步的计算和显存消耗为 $O(C + M)$，整体复杂度为 $O(N)$，实现了线性复杂度的无限长文本处理。

#### 2. 多对话 DAPO 损失函数

MEMAGENT 的记忆更新策略通过强化学习端到端优化。论文将 DAPO 算法扩展为多对话版本（Multi-Conv DAPO），对每个样本生成 $G$ 个独立的上下文无关对话，以最终答案的规则奖励联合优化所有对话（Figure 3）。

**优势函数**：样本 $i$ 中所有 token 共享同一优势值，由该样本的奖励减去组内平均奖励得到：

$$\hat{A}_{i,j,t} = R_i - \mathrm{mean}(\{R_i\}_{i=1}^G)$$

**DAPO 损失**：对组内所有对话的所有 token 求平均，包含裁剪后的优势项和 KL 惩罚：

$$\mathcal{T}_{\mathrm{DAP0}}(\theta) = \mathbb{E}_{(q,a)\sim\mathcal{D}, \{\boldsymbol{o}_{i,j}\}_{i=1}^G \sim \pi_{\boldsymbol{\theta}_{\mathrm{old}}}} \left[ \frac{1}{\sum_{i=1}^G \sum_{j=1}^{n_i} |\boldsymbol{o}_{i,j}|} \sum_{i=1}^G \sum_{j=1}^{n_i} \sum_{t=1}^{|\boldsymbol{o}_{i,j}|} (\mathcal{C}_{i,j,t} - \beta D_{\mathrm{KL}}) \right]$$

其中 $\mathcal{C}_{i,j,t}$ 为裁剪后的替代目标：

$$\mathcal{C}_{i,j,t} = \min\left(r_{i,j,t}(\theta)\hat{A}_{i,j,t}, \mathrm{clip}(r_{i,j,t}(\theta), 1-\varepsilon_{low}, 1+\varepsilon_{high})\hat{A}_{i,j,t}\right)$$

概率比 $r_{i,j,t}(\theta) = \frac{\pi_{\boldsymbol{\theta}}(\boldsymbol{o}_{i,j,t} \mid q, \boldsymbol{o}_{i,j,<t})}{\pi_{\boldsymbol{\theta}_{\mathrm{old}}}(\boldsymbol{o}_{i,j,t} \mid q, \boldsymbol{o}_{i,j,<t})}$。

#### 3. 基于规则的奖励函数

训练采用 RLVR（Reinforcement Learning with Verifiable Rewards）范式，使用规则验证器计算二元结果奖励：

$$R(\hat{y}, y) = \mathbf{1}_{\mathrm{is.equiv}(\mathbf{y}, \hat{\mathbf{y}})}$$

当预测答案 $\hat{y}$ 与标准答案 $y$ 等价时奖励为 1，否则为 0。该奖励信号驱动模型学习生成最优的读写记忆轨迹，即在给定输入上下文的条件下最大化期望奖励的记忆状态分布。



## 实验与关键发现

### 核心结果：从 8K 到 3.5M 的极限外推

MEMAGENT 最关键的实验结论是**长度外推能力**：模型仅在 8K 上下文窗口下训练，却能稳定处理超过 400 倍长度的输入。在 RULER-HQA 基准上，RL-MEMAGENT-14B 从 7K 时的 80.47% 准确率到 3.5M 时仍保持 71.09%，性能损失不到 10%（Table 1）。作为对比，同期最强长上下文基线 **Qwen2.5-Instruct-14B-1M**（Yang et al., 2025）在 7K 时仅为 60.16%，到 896K 时直接崩溃至 0.00%。即使是标准指令微调的 **Qwen2.5-Instruct-14B**（Yang et al., 2024），也从 7K 的 75.00% 骤降至 896K 的 2.34%。


![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_k5nIOvYGCL/figures/005_Table_1.jpg]]
*Table 1: Main experimental results comparing model performance across various context lengths. All values represent accuracy (%)*

这一趋势在 Figure 1 中被直观呈现：所有基线模型随上下文增长性能急剧衰减，而 MEMAGENT 的曲线几乎保持水平。在 512K NIAH 测试中，RL-MEMAGENT 取得超过 95% 的准确率，同期开源长上下文模型则出现显著下降（Figure 5）。


![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_k5nIOvYGCL/figures/001_Figure_1.jpg]]
*Figure 1: Accuracy scores of RULER-HQA (Hsieh et al., 2024; Yang et al., 2018) . Even models that employ long-context continual pretraining and extrapolation techniques fail to maintain consistent performance. In contrast, MEMAGENT with RL only demonstrates marginal performance dropping*

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_k5nIOvYGCL/figures/008_Figure_5.jpg]]
*Figure 5: Performance heatmaps on NIAH benchmark across different context lengths*

### 小模型超越大基线的反直觉结果

在 LongBench-QA 上，MEMAGENT-14B 以 51.0 的平均分超越了更大规模的基线模型，包括 **QwenLong-L1-32B**（Wan et al., 2025）的 50.7 和 **DS-Distill-Qwen-32B**（Guo et al., 2025）的 49.0（Table 3）。在 LongBench-SUM 的摘要任务中，RL-MEMAGENT-14B 在 GOVREPORT 和 QMSUM 两个子集上均取得最高平均 ROUGE 分数（Table 2）。这表明**通过 RL 习得的记忆策略比简单地扩大上下文窗口或推理蒸馏更有效**，且计算开销更低。


![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_k5nIOvYGCL/figures/007_Table_3.jpg]]
*Table 3: Model performance on LongBench-QA*

### 消融实验：RL 训练是外推能力的必要条件

移除 RL 训练后，MEMAGENT 在长文本上的性能随长度增长大幅下降。Figure 6（RULER-HQA）和 Figure 7（Longbench-QA）的消融结果直接证明了这一点：无 RL 训练的模型在上下文超过训练窗口后迅速退化，而 RL 训练使模型学会在固定记忆容量下选择性保留关键信息，从而实现近乎无损的外推。

### 记忆长度的稳健性

记忆长度在 256 到 4096 tokens 之间变化时，MEMAGENT 的性能保持稳健。Figure 8（NIAH）和 Figure 9（Longbench）的消融显示，1024 tokens 为最佳平衡点——更小的记忆可能丢失关键信息，更大的记忆则增加计算开销但收益递减。Table 8 和 Table 9 进一步验证了记忆大小与上下文块大小的联合消融结果：对于 14B 模型，将记忆从 4096 降至 1024 同时将上下文块从 1928 增至 5000，平均分反而从 48.5 提升至 51.0。

### 关键信息位置不敏感

Table 4 的探测实验表明，MEMAGENT 对关键信息在上下文中的位置不敏感。无论关键信息出现在文档开头（0%）、中间（40%-60%）还是末尾（80%-100%），模型准确率与随机分布基线的差异仅在 +0.56 到 +2.79 个百分点之间，未出现传统长上下文模型常见的“中间丢失”或灾难性遗忘现象。

### 与 RAG Agent 的对比优势

Table 10 和 Table 11 将 MEMAGENT 与基于检索增强生成（RAG）的 Agent 进行了系统对比。在 RULER-HQA 上，即使 RAG 使用 top-K=8 的最优设置，RL-MEMAGENT-14B 在所有上下文长度下均保持领先（3.5M 时 71.09 vs. 64.84）。在 LongBench-QA 上，RL-MEMAGENT-14B 的 51.00 平均分远超最优 RAG 配置的 33.00。这揭示了**端到端 RL 优化的记忆策略比固定检索策略更能适应任务需求**。

### 已知失败模式

论文在附录 F 中诚实记录了 MEMAGENT 的三类失败模式：
1. **多跳推理缺失**：当前置证据未在文档中出现时，模型可能无法识别后续关键信息，导致错误答案。
2. **首因偏见**：模型可能过早形成假设，忽略后续出现的反证或补充信息。
3. **记忆覆盖**：在极长对话中，固定长度的记忆可能截断或覆盖早期存储的关键信息。

这些失败模式表明，当前基于结果奖励的 RL 训练虽然赋予了模型强大的选择性记忆能力，但在需要精确时序推理或多轮证据整合的场景下仍有局限。



## 定位与知识库关联

### 核心思想与设计哲学

MEMAGENT 的设计灵感来源于人类处理长文档的认知策略：**分块阅读 + 选择性笔记 + 基于笔记作答**。这一思路将传统 LLM 的自回归生成过程重构为“读-写”交替的记忆更新轨迹，其形式化基础是将序列似然分解为基于固定长度隐变量 $\mathbf{m}$ 的读写步骤：

$$p(\mathbf{x}_{1:N}) = \sum_{\mathbf{m}^{1:K-1}} \prod_{k=1}^{K} \underbrace{p(\mathbf{c}^k \mid \mathbf{m}^{k-1})}_{\text{read}} \underbrace{p(\mathbf{m}^k \mid \mathbf{c}^k, \mathbf{m}^{k-1})}_{\text{write}}$$

这一分解将无界的历史上下文替换为固定长度记忆 $\mathbf{m} \in \mathcal{V}^M$（默认 $M=1024$ tokens），使每一步的计算复杂度恒定为 $O(C+M)$，整体复杂度线性于块数 $O(N)$，从根本上规避了标准 Transformer 注意力机制的二次复杂度瓶颈。

### 与现有方法谱系的关系

**1. 长上下文处理方法**

当前处理长文本的主流范式可分为三类：

- **长度外推（Length Extrapolation）**：通过位置编码改造（如 RoPE 缩放）或持续预训练扩展上下文窗口。代表工作包括 **Qwen2.5-Instruct-1M 系列**（Yang et al., 2025）和 **QwenLong-L1-32B**（Wan et al., 2025）。这些方法本质上仍依赖全注意力机制，在超出训练窗口后性能急剧下降——Table 1 显示 Qwen2.5-Instruct-14B-1M 在 896K 时准确率已降至 0%。

- **稀疏注意力（Sparse Attention）**：通过限制注意力范围降低复杂度，但信息丢失模式不可控，且缺乏任务驱动的优化信号。

- **上下文压缩（Context Compression）**：通过软提示或检索增强压缩历史信息。与 MEMAGENT 最接近，但现有压缩方法通常依赖启发式规则或监督微调，缺乏端到端的任务级优化。

MEMAGENT 的独特之处在于：**将记忆更新策略形式化为强化学习问题，以最终答案正确性为奖励信号，端到端地训练模型学会“何时记住、何时遗忘”**。这使得模型在仅使用 8K 训练窗口的情况下，外推至 3.5M tokens 时性能损失不到 10%（Table 1: 80.47% → 71.09%）。

**2. 推理增强方法**

与基于检索增强生成（RAG）的方法相比，MEMAGENT 展现出明显优势。Table 10 的对比实验表明，在 RULER-HQA 的所有上下文长度和 top-K 设置下，MEMAGENT 均优于 RAG Agent。这源于 MEMAGENT 的记忆更新是**任务驱动的选择性保留**，而非简单的相关性检索。

与推理蒸馏方法（如 **DS-Distill-Qwen 系列**，Guo et al., 2025）相比，MEMAGENT 在 LongBench-QA 上以更小的模型规模（14B vs 32B）取得了更高的平均分（51.0 vs 49.0-50.7），说明记忆机制带来的信息保持能力超越了单纯推理能力的提升。

**3. 强化学习训练范式**

MEMAGENT 采用的 Multi-Conv DAPO 算法是对 GRPO/DAPO 系列方法的扩展。其关键创新在于：

- **多对话联合优化**：每个样本生成多个上下文无关的对话，以最终对话的答案计算奖励，并将优势信号反向传播至所有前置对话。这解决了长文本处理中稀疏奖励的信用分配问题。
- **组内归一化优势**：$\hat{A}_{i,j,t} = R_i - \mathrm{mean}(\{R_i\}_{i=1}^G)$，通过组内奖励均值作为基线，稳定训练过程。
- **规则奖励**：$R(\hat{y}, y) = \mathbf{1}_{\mathrm{is.equiv}(\mathbf{y}, \hat{\mathbf{y}})}$，使用基于等价性判断的二元奖励，避免奖励模型的偏差。

消融实验（Figure 6, Figure 7）证实，移除 RL 训练后，MEMAGENT 在长文本上的性能随长度增长大幅下降，表明 RL 是模型获得鲁棒记忆能力的关键。

### 适用边界与局限

**已验证的适用场景：**
- 检索型长文本 QA（RULER-HQA, LongBench-QA, NIAH）：在高达 3.5M tokens 的上下文中保持稳定性能
- 长文档摘要（LongBench-SUM）：在 GOVREPORT 和 QMSUM 上取得最优 ROUGE 分数

**已知局限：**

1. **多跳推理的脆弱性**：当关键证据分散在多个块中，且前置证据未被记忆时，模型可能无法建立正确的推理链（附录 F.2）。这是固定长度记忆的固有局限——一旦信息被覆盖，后续推理将失去依据。

2. **首因偏见（Primacy Bias）**：模型可能过早基于早期信息形成假设，并在后续处理中忽略或低估矛盾证据（附录 F.3）。这与人类认知中的确认偏误类似，但缺乏人类的自我纠错机制。

3. **记忆覆盖风险**：在极长对话或信息密集场景中，固定长度的记忆可能不足以容纳所有关键信息，导致重要内容被截断或覆盖（附录 F.1）。当前默认的 1024 tokens 记忆长度在信息密度极高的任务上可能成为瓶颈。

4. **任务泛化性未充分验证**：当前工作主要在检索型 QA 和摘要任务上验证，对需要多步工具调用、代码生成、或复杂推理链的代理任务尚未探索。

### 开放问题

1. **记忆能力的任务泛化**：通过 RL 获得的记忆策略是否能迁移到更复杂的代理场景（如多轮工具使用、交互式代码生成）？这可能需要引入过程奖励或中间步骤的监督信号。

2. **动态记忆分配**：当前记忆长度固定为 1024 tokens，最优比例在不同任务和领域下可能差异显著。能否设计机制使模型根据输入的信息密度动态调整记忆分配？

3. **记忆溢出处理**：当所需记忆量超过固定长度时，当前方案缺乏优雅的降级机制。可能的扩展方向包括层次化记忆、外部存储的受控访问，或允许模型主动请求回顾已处理块。

4. **细粒度奖励设计**：当前的规则奖励仅评估最终答案的正确性，对中间记忆更新质量无直接反馈。引入过程奖励模型或中间步骤的验证信号可能进一步提升记忆更新的精准度。

5. **与长上下文预训练的结合**：MEMAGENT 在 8K 训练窗口下已展现惊人外推能力，若与长上下文持续预训练结合，是否能进一步突破当前 3.5M 的有效上限？



## 原文 PDF

![[paperPDFs/ICLR_2026/MemAgent_Reshaping_Long_Context_LLM_with_Multi_Conv_RL_based_Memory_Agent.pdf]]
