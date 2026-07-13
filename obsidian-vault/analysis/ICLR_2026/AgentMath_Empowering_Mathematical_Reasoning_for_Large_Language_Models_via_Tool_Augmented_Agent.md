---
title: "AgentMath: Empowering Mathematical Reasoning for Large Language Models via Tool-Augmented Agent"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AgentMath_Empowering_Mathematical_Reasoning_for_Large_Language_Models_via_Tool_Augmented_Agent.pdf
project_link: null
code_link: null
openreview_forum_id: e2s7YHeVZW
aliases:
- AgentMath
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/language_speech_and_dialog
core_operator: "将代码解释器（工具）集成到推理链中，并通过自动化合成工具增强轨迹数据和Agentic RL让模型自主学习最优工具调用策略。"
primary_logic: "通过工具化数据合成与Agentic RL，模型能够自主决定何时使用代码进行精确计算，显著提升准确率和效率；同时异步式部分展开训练系统解决了超长序列训练的瓶颈，实现4-5倍加速。"
claims:
- "AgentMath-30B-A3B在AIME24上达到90.6%，超越OpenAI-o3-mini和Claude-Opus-4.0-Thinking，接近DeepSeek-R1-671B。"
- "工具增强RL仅需400训练步数达到76.2%，而纯文本RL需要1600步，效率提升约4倍。"
- "逐步多维质量细化将AIME24准确率从35.3%提升至60.5%，验证了数据质量的关键作用。"
- "AIME24 上 Accuracy (avg@32) = 90.6% (AgentMath-30B-A3B)"
---

# AgentMath: Empowering Mathematical Reasoning for Large Language Models via Tool-Augmented Agent

> [!tip] 核心洞察
> 通过工具化数据合成与Agentic RL，模型能够自主决定何时使用代码进行精确计算，显著提升准确率和效率；同时异步式部分展开训练系统解决了超长序列训练的瓶颈，实现4-5倍加速。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AgentMath：通过工具增强的智能体赋能大语言模型数学推理 |
| 英文题名 | AgentMath: Empowering Mathematical Reasoning for Large Language Models via Tool-Augmented Agent |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=e2s7YHeVZW) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/language_speech_and_dialog |
| Method | AgentMath |
| Dataset | AIME24, AIME25, HMMT25 |

> [!tip] 效果简介
> - AIME24 上，Accuracy (avg@32) 为 90.6% (AgentMath-30B-A3B)，对比 87.7% (Qwen3-30B-A3B-Thinking-2507)，变化 +2.9%。
> - AIME25 上，Accuracy (avg@32) 为 86.4% (AgentMath-30B-A3B)，对比 85.0% (Qwen3-30B-A3B-Thinking-2507)，变化 +1.4%。
> - HMMT25 上，Accuracy (avg@32) 为 73.8% (AgentMath-30B-A3B)，对比 71.4% (Qwen3-30B-A3B-Thinking-2507)，变化 +2.4%。

## 概要

数学推理任务中，纯文本的长链思维（Chain‑of‑Thought）在处理需要精确计算或符号操作的步骤时，既容易出错又效率低下；同时，高质量的工具使用数据稀缺，现有强化学习方法难以有效优化工具调用策略，而极长序列的训练效率瓶颈进一步加剧了这一问题。AgentMath 的核心思路是将代码解释器作为工具集成到推理链中，通过**自动化合成工具增强轨迹数据**和**Agentic RL**，让模型自主学习最优的工具调用时机与方式，从而显著提升推理准确率和计算效率。

为支撑这一范式，AgentMath 构建了一套完整的训练流水线：首先，工具增强数据合成模块将纯文本长链推理自动转化为交错包含 `<think>`、`<code>` 和 `<interpreter>` 的工具调用轨迹；其次，Agentic RL 训练模块在 GRPO 框架下引入损失掩码与适应性批次过滤，仅对思考与代码令牌施加优化，并辅以答案正确性奖励与工具使用效率奖励；最后，高效 RL 基础设施通过异步调度、Agentic Partial Rollout 和前缀感知负载均衡，将端到端训练吞吐提升 4–5 倍。

实验结果表明，AgentMath‑30B‑A3B 在 AIME24 上达到 **90.6%**，超越 OpenAI‑o3‑mini 和 Claude‑Opus‑4.0‑Thinking，接近 DeepSeek‑R1‑671B；在 AIME25 和 HMMT25 上分别取得 **86.4%** 和 **73.8%**。消融研究进一步揭示，逐步多维数据细化使 AIME24 准确率从 35.3% 跃升至 60.5%，工具增强 RL 仅需约 400 训练步数即可达到纯文本 RL 约 1600 步的性能水平，效率提升约 4 倍。这些结果一致表明，工具化轨迹合成与 Agentic RL 的组合是提升数学推理性能与效率的关键杠杆。



数学推理是大语言模型迈向通用人工智能的核心能力之一。近年来，以 OpenAI-o1、DeepSeek-R1 为代表的长链思维模型在竞赛级数学基准上取得了显著进展。然而，**纯文本推理范式在处理需要精确计算或符号操作的数学问题时暴露出根本性瓶颈**：模型在长链推理中容易出现数值计算错误、代数化简失误，且为纠正这些错误往往需要生成大量冗余文本，导致推理效率低下。

现有工具增强方法试图通过引入代码解释器来弥补这一缺陷，但面临三个关键缺口：

1. **高质量工具使用数据稀缺**。将自然语言思维链自动转化为结构化的工具调用轨迹并非易事，现有合成方法生成的轨迹质量参差不齐，难以支撑有效的监督微调。
2. **强化学习范式不匹配**。标准 GRPO 等 RL 方法针对纯文本优化设计，无法有效优化“何时调用工具、调用何种工具”的策略决策，导致模型要么过度依赖工具，要么完全回避工具。
3. **训练效率瓶颈**。工具调用产生的超长序列（可达 96k tokens）和动态代码执行使得传统同步批处理训练极其低效，严重制约了大规模工具增强 RL 的可行性。

AgentMath 的工作正是在这一背景下展开：**通过工具化数据合成与 Agentic RL，让模型自主学会在推理链中适时调用代码解释器进行精确计算，从而同时提升准确率和效率**。其核心洞察在于——将代码执行视为推理过程的有机组成部分而非外部辅助，并通过专门的训练系统和奖励设计让模型内化这一能力。



## 核心方法与创新机理

AgentMath 的核心创新在于将数学推理从纯文本长链思维（CoT）重构为**工具增强的智能体交互范式**，并通过自动化数据合成与强化学习（RL）让模型自主掌握工具调用策略。相对于纯文本基线，AgentMath 在四个关键维度上实现了系统性改变：

### 1. 训练数据：从纯文本长链推理到工具增强轨迹合成

传统方法依赖纯文本 CoT 数据进行监督微调（SFT），在处理需要精确计算或符号操作的步骤时容易出错且效率低下。AgentMath 引入了一套**三阶段自动化合成与细化流水线**（Figure 1），将纯文本长链推理转化为包含可执行代码调用和真实解释器反馈的工具增强轨迹：

- **代码注入**：利用教师模型（DeepSeek-V3）将长链 CoT 中的计算密集型推理步骤替换为代码块和模拟输出，形式化为变换 $\tau_{\mathrm{agent}}^{\prime} = \mathcal{F}_{\mathrm{inject}}(\tau_{\mathrm{text}})$，其中计算步骤 $s_{\mathrm{calc}}$ 被映射为代码 $c$ 和模拟输出 $o_{\mathrm{sim}}$（Section 2.2）。
- **多维质量细化**：通过逐步细化策略提升合成数据的质量，将 AIME24 准确率从初始的 35.3% 提升至 60.5%（Table 3），验证了数据质量的关键作用。
- **自校正能力注入**：在轨迹中注入代码执行错误与修正过程，使模型学会从工具调用失败中恢复。

这一数据合成策略使得 AgentMath-SFT 在 AIME24 上达到 60.5%，比纯文本基线高出 3.4 个百分点（Table 2）。

### 2. 推理交互协议：从纯文本 CoT 到交错式代码执行

AgentMath 将推理过程建模为**马尔可夫决策过程（MDP）**，支持模型在生成过程中动态交错自然语言推理（`<think>` 标签）、代码生成（`<code>` 标签）和解释器执行（`<interpreter>` 标签）。这种协议使模型能够在需要精确计算时主动调用代码解释器，而非依赖易出错的文本推理。

实证表明，代码增强推理平均比纯文本减少 1.3k–3k 个 token，且准确率更高（Table 23），体现了工具调用在效率与精度上的双重优势。

### 3. RL 范式：从标准 GRPO 到 Agentic RL

AgentMath 提出了 **Agentic RL** 范式，在标准 GRPO 基础上引入三个关键机制：

- **损失掩码**：仅对 `<think>` 和 `<code>` 部分的 token 计算策略损失，避免解释器输出（固定反馈）干扰梯度更新。
- **复合奖励设计**：奖励函数由正确性奖励和工具使用效率奖励组成：
  $$R_{\mathrm{acc}} = \begin{cases} 1, & \mathrm{if \ is.equivalent}(\hat{a}, a), \\ 0, & \mathrm{otherwise}, \end{cases}$$
  $$R_{\mathrm{tool}} = \min\left(R_{\mathrm{max}}, \alpha + \beta \cdot N_{\mathrm{code}}\right) \quad \mathrm{if} \ N_{\mathrm{code}} > 0$$
  $$R_{\mathrm{total}} = R_{\mathrm{acc}} + \mathbb{I}(R_{\mathrm{acc}} = 1) \cdot R_{\mathrm{tool}}$$
  仅在答案正确时附加工具使用奖励（$\alpha=0.1, \beta=0.01, R_{\mathrm{max}}=1$），鼓励正确且高效的工具调用。消融实验表明，该设计可获得最佳平均准确率 62.6%，优于无工具奖励基线 60.2%（Table 27）。
- **适应性批次过滤**：动态调整训练批次，维持长度截断和工具调用超限率低于 10%。

工具增强 RL 仅需约 400 训练步数即达到 AIME24 上 76.2% 的准确率，而纯文本 RL 需要约 1600 步达到 68.7%，**效率提升约 4 倍**（Table 2, Figure 4）。

### 4. 训练系统：从同步批处理到异步部分展开

针对工具增强推理产生的极长序列（最高 96k tokens）和大容量工具调用（最高 96 次），AgentMath 设计了高效 RL 基础设施：

- **异步解耦架构**：将 GPU 密集型模型推理与 CPU/IO 密集型工具执行分离，通过分布式沙盒集群和请求级调度，将工具调用延迟从 175 秒降至 1.2 秒。
- **Agentic Partial Rollout**：将完整轨迹分解为预算受限的段 $\tau = \tau^{(1)} \oplus \tau^{(2)} \oplus ... \oplus \tau^{(N)}$，实现 2.2–2.5 倍加速。
- **前缀感知负载均衡**：根据请求的前缀长度动态分配权重 $w_j = \left\lfloor \frac{L_j}{L_{\mathrm{base}}} \right\rfloor + w_{\mathrm{base}}$，将请求路由至负载最轻的推理引擎。

整体系统实现端到端训练吞吐量 **4–5 倍提升**（Figure 2）。

### 创新总结

AgentMath 的四个 changed slots 形成闭环：工具增强数据合成为模型提供了高质量的行为示范，Agentic RL 让模型在交互式环境中自主优化工具调用策略，而高效训练系统则使这一范式在大规模训练中切实可行。从因果机制看，**工具化数据合成**是性能提升的基础（SFT 阶段贡献约 3.4 个百分点的提升），而 **Agentic RL** 则是实现高效工具策略优化的关键杠杆（RL 阶段贡献约 7.5 个百分点的额外提升，且训练效率提升 4 倍）。



![[assets/figures/papers/iclr26_0010_e2s7YHeVZW_AgentMath_Empowering_Mathematical_Reasoning_for/figures/002_Figure_2.jpg]]
*Figure 2: The diagram of agentic reinforcement learning. It depicts the structure and workflow of our agentic reinforcement learning system with core functions including Agent Loop, Asynchronous Scheduler, and Partial Rollout, along with key performance improvement. Based on the Asynchronous Scheduler, the Agent Loop continues running by default. It will stop early only when conditions are met: either the content length exceeds the max length (i.e., 32k) or the number of tool calls exceeds the maximum constraint*

![[assets/figures/papers/iclr26_0010_e2s7YHeVZW_AgentMath_Empowering_Mathematical_Reasoning_for/figures/001_Figure_1.jpg]]
*Figure 1: This diagram outlines a three-stage pipeline for creating a high-quality tool-augmented trajectories for training agents, including Agentic Trajectory Generation via Code Injection, Multi-Faceted Quality Refinement and Self-Correction Capability Injection. This automated process transforms pure-text reasoning into verified, executable agentic trajectories*

AgentMath 将大语言模型的数学推理形式化为一个**工具增强的马尔可夫决策过程**（MDP），其核心思路是将代码解释器作为可调用的外部工具，嵌入到推理链中，使模型在生成自然语言思维链的同时，能够实时执行精确的符号计算与数值运算。

整个框架由三个紧密协作的模块构成，形成一条从数据合成到策略优化的完整流水线：

### 1. 工具增强数据合成模块

该模块负责将已有的纯文本长链推理轨迹转化为包含代码调用与解释器反馈的智能体式演示数据。其输入为教师模型（如 DeepSeek-R1/DeepSeek-V3）生成的纯文本 CoT 轨迹 $\tau_{\text{text}}$，输出为工具增强轨迹 $\tau_{\text{agent}}'$。核心变换可形式化为：

$$\tau_{\mathrm{agent}}^{\prime} = \mathcal{F}_{\mathrm{inject}}(\tau_{\mathrm{text}})$$

其中 $\mathcal{F}_{\mathrm{inject}}$ 将轨迹中的计算密集型步骤 $s_{\mathrm{calc}}$ 替换为代码块 $c$ 及模拟执行输出 $o_{\mathrm{sim}}$。该模块采用**三阶段流水线**（见 Figure 1）：
- **阶段一（代码注入）**：利用教师模型将长 CoT 分段，识别适合代码化的推理步骤，注入可执行代码块并生成模拟输出。
- **阶段二（多维质量细化）**：对注入后的轨迹进行多维度质量评估与修正，包括代码正确性、推理连贯性和答案一致性。消融实验表明，逐步细化将 AIME24 准确率从 35.3% 提升至 60.5%（Table 3），验证了数据质量的关键作用。
- **阶段三（自校正能力注入）**：在轨迹中插入代码执行失败后的自我修正片段，使模型学会在工具调用出错时自主恢复。

合成后的数据经过严格的 n-gram 和语义去重，确保与评估集无重叠，随后用于监督微调（SFT）。

### 2. Agentic RL 训练模块

该模块在 SFT 模型的基础上，通过强化学习进一步优化模型的工具调用策略。其输入为 SFT 初始化后的模型，输出为经过 RL 优化的策略模型。训练采用 **GRPO（Group Relative Policy Optimization）** 框架，但引入了三项关键改进：

- **损失掩码**：仅对 `<think>` 和 `<code>` 部分的 token 施加策略梯度损失，避免解释器输出等不可控 token 干扰学习。
- **复合奖励设计**：总奖励由正确性奖励和工具使用效率奖励组合而成：

$$R_{\mathrm{acc}} = \begin{cases} 1, & \mathrm{if\ is.equivalent}(\hat{a}, a), \\ 0, & \mathrm{otherwise} \end{cases}$$

$$R_{\mathrm{tool}} = \min\left(R_{\mathrm{max}}, \alpha + \beta \cdot N_{\mathrm{code}}\right) \quad \mathrm{if} \ N_{\mathrm{code}} > 0$$

$$R_{\mathrm{total}} = R_{\mathrm{acc}} + \mathbb{I}(R_{\mathrm{acc}} = 1) \cdot R_{\mathrm{tool}}$$

其中 $\alpha=0.1$ 为基础奖励，$\beta=0.01$ 为每次代码调用的增量系数，$R_{\mathrm{max}}=1$ 为奖励上限。工具使用奖励仅在答案正确时生效，鼓励模型在保证准确性的前提下高效使用工具。消融实验（Table 27）证实该设计可获得最佳平均准确率 62.6%，优于无工具奖励的基线 60.2%。

- **适应性批次过滤**：动态剔除超出长度或工具调用上限的无效样本，维持训练稳定性。

RL 训练分多个阶段进行，逐步扩展上下文长度（48k → 72k → 96k tokens）和工具调用上限（48 → 72 → 96 次），使模型逐渐适应更复杂的推理场景（Figure 3）。

### 3. 高效 RL 基础设施模块

工具增强 RL 面临的核心工程瓶颈在于：单条轨迹可能包含数十次代码调用，每次调用需等待沙箱执行并返回结果，导致传统同步批处理方案效率极低。该模块通过三项技术实现 **4-5 倍端到端训练吞吐量提升**（Figure 2）：

- **异步解耦架构**：将 GPU 密集型模型推理与 CPU/IO 密集型的沙箱执行完全解耦。分布式沙箱集群并行处理代码执行请求，将工具调用延迟从 175s 降至 1.2s。
- **Agentic Partial Rollout**：将完整轨迹 $\tau$ 分解为 $N$ 个预算受限的段：

$$\tau = \tau^{(1)} \oplus \tau^{(2)} \oplus ... \oplus \tau^{(N)}$$

每段独立展开，避免长序列阻塞训练循环，实现 2.2-2.5 倍加速。
- **前缀感知负载均衡**：根据请求的前缀长度 $L_j$ 分配动态权重 $w_j = \left\lfloor \frac{L_j}{L_{\mathrm{base}}} \right\rfloor + w_{\mathrm{base}}$，将请求路由至当前负载 $W_k$ 最小的推理引擎，最小化流水线气泡。

### 模块间数据流

整体流程为：**纯文本 CoT 轨迹 → 工具增强数据合成 → SFT 训练 → Agentic RL 训练 → 最终模型**。SFT 阶段为 RL 提供具备基本工具调用能力的初始策略；RL 阶段通过与环境（代码解释器）的交互反馈，进一步优化工具调用的时机与效率。实验表明，工具增强 RL 仅需约 400 训练步数即可在 AIME24 上达到 76.2%，而纯文本 RL 需要约 1600 步，效率提升约 4 倍（Table 2, Figure 4）。



AgentMath 的整体技术路线围绕三个核心模块展开：工具增强数据合成、Agentic RL 训练范式，以及高效RL基础设施。以下逐一展开其关键设计与形式化表达。

### 工具增强数据合成模块

该模块的核心任务是将纯文本长链推理（CoT）转化为包含代码调用与解释器反馈的工具增强轨迹。其形式化定义为代码注入变换：

$$\tau_{\mathrm{agent}}^{\prime} = \mathcal{F}_{\mathrm{inject}}(\tau_{\mathrm{text}}), \quad \mathrm{where} \ \mathcal{F}_{\mathrm{inject}} : \tau_{\mathrm{text}} \mapsto \left( \tau_{\mathrm{text}} \ \mathrm{with} \ s_{\mathrm{calc}} \Rightarrow (c, o_{\mathrm{sim}}) \right).$$

其中，$\tau_{\mathrm{text}}$ 为原始纯文本推理轨迹，$s_{\mathrm{calc}}$ 为轨迹中需要精确计算的步骤，$c$ 为注入的可执行代码块，$o_{\mathrm{sim}}$ 为模拟的解释器输出。该变换由教师模型（DeepSeek-V3）驱动，将长链推理分段后逐段注入代码，生成结构化的工具调用轨迹。

合成流水线包含三个阶段：代码注入（Stage 1）、多维质量细化（Stage 2）与自校正能力注入（Stage 3）。其中，逐步多维质量细化是性能提升的关键瓶颈——消融实验表明，经过完整细化流程后，AIME24 准确率从初始的 35.3% 提升至 60.5%（Table 3），验证了数据质量的决定性作用。

### Agentic RL 训练模块

工具增强数学推理被形式化为马尔可夫决策过程（MDP），模型在每一步自主决定是否调用代码解释器。RL 训练基于 GRPO 算法，核心创新在于奖励设计与损失掩码。

**奖励函数** 由正确性奖励与工具使用效率奖励复合而成。正确性奖励为二元信号，通过数学等价性判断预测答案 $\hat{a}$ 与标准答案 $a$ 是否一致：

$$R_{\mathrm{acc}} = \begin{cases} 1, & \mathrm{if \ is.equivalent}(\hat{a}, a), \\ 0, & \mathrm{otherwise}. \end{cases}$$

工具使用效率奖励鼓励模型在保证正确性的前提下高效调用代码，定义为：

$$R_{\mathrm{tool}} = \min\left(R_{\mathrm{max}}, \alpha + \beta \cdot N_{\mathrm{code}}\right) \quad \mathrm{if} \ N_{\mathrm{code}} > 0,$$

其中 $N_{\mathrm{code}}$ 为代码调用次数，$\alpha = 0.1$ 为基础奖励，$\beta = 0.01$ 为每次调用的增量系数，$R_{\mathrm{max}} = 1$ 为奖励上限。最终复合奖励仅在答案正确时附加工具奖励：

$$R_{\mathrm{total}} = R_{\mathrm{acc}} + \mathbb{I}(R_{\mathrm{acc}} = 1) \cdot R_{\mathrm{tool}}.$$

消融实验（Table 27）表明，该设计（仅在正确回答上施加工具奖励）可获得最佳平均准确率 62.6%，优于无工具奖励基线 60.2%。此外，损失掩码仅对 `<think>` 和 `<code>` 部分的 token 计算 RL 损失，避免解释器输出 token 干扰梯度。

### 高效RL基础设施模块

为应对工具增强推理产生的超长序列（最高 96k tokens）与频繁代码调用（最高 96 次），AgentMath 设计了异步解耦的训练系统，核心机制包括 Agentic Partial Rollout 与前缀感知负载均衡。

**Agentic Partial Rollout** 将完整轨迹分解为 $N$ 个预算受限的段：

$$\tau = \tau^{(1)} \oplus \tau^{(2)} \oplus ... \oplus \tau^{(N)},$$

每段在预算内生成后即暂停，交由调度器统一管理，从而实现 2.2–2.5 倍加速。**前缀感知负载均衡** 根据请求的前缀长度 $L_j$ 赋予动态权重：

$$w_j = \left\lfloor \frac{L_j}{L_{\mathrm{base}}} \right\rfloor + w_{\mathrm{base}},$$

并路由至当前负载最小的推理引擎 $k^*$：

$$k^* = \arg \min_{k \in \{1, \dots, M\}} W_k, \quad W_{k^*} \gets W_{k^*} + w_j.$$

结合分布式沙盒集群的请求级异步调度（将工具调用延迟从 175s 降至 1.2s），整体端到端训练吞吐量实现 4–5 倍提升（Figure 2）。



## 实验与关键发现

### 主要结果

AgentMath 在多个竞赛级数学基准上取得了领先性能。Table 1 展示了 AgentMath 各规模模型与前沿模型的对比。**AgentMath‑30B‑A3B** 在 AIME24 上达到 **90.6%**，超过 OpenAI‑o3‑mini（87.7%）和 Claude‑Opus‑4.0‑Thinking（88.3%），逼近 DeepSeek‑R1‑671B（91.0%）；在 AIME25 上为 **86.4%**，在 HMMT25 上为 **73.8%**。**AgentMath‑8B** 同样表现强劲，AIME24 达到 89.8%，较纯文本基线 DS‑0528‑Qwen3‑8B 提升 +3.8%；AIME25 达到 84.7%，提升幅度高达 +8.4%。即使是 1.7B 的小规模模型也取得了 59.6%（AIME24）和 48.1%（AIME25）的成绩，验证了工具增强方法在不同模型规模下的有效性。

Table 2 和 Figure 4 进一步对比了 AgentMath 与纯文本模型在 SFT 和 RL 阶段的性能差异。在 SFT 阶段，AgentMath 已优于纯文本基线（AIME24 60.5% vs. 57.1%）；进入 RL 阶段后，差距显著扩大：AgentMath‑RL 在约 400 训练步达到 **76.2%**，而纯文本 RL 需要约 1600 步才达到 68.7%，**训练效率提升约 4 倍**。这表明工具增强的 RL 范式不仅提升了最终准确率，还大幅加速了收敛。


![[assets/figures/papers/iclr26_0010_e2s7YHeVZW_AgentMath_Empowering_Mathematical_Reasoning_for/figures/010_Table_2.jpg]]
*Table 2: Performance comparison between AgentMath and Text-Based Model in SFT and RL stages*

![[assets/figures/papers/iclr26_0010_e2s7YHeVZW_AgentMath_Empowering_Mathematical_Reasoning_for/figures/012_Figure_4.jpg]]
*Figure 4: Performance Comparison of AgentMath vs. Text-Based Model in the RL phase on AIME24/25. Both models were initialized from their best SFT checkpoint trained on 20k data*

### 消融分析

**数据质量的关键作用**：Table 3 展示了逐步多维质量细化对性能的影响。未经细化的初始合成数据在 AIME24 上仅达 35.3%，经过代码注入、轨迹验证、自校正注入等累积细化步骤后，准确率提升至 **60.5%**（+25.2%），证明数据质量是性能提升的核心杠杆。


![[assets/figures/papers/iclr26_0010_e2s7YHeVZW_AgentMath_Empowering_Mathematical_Reasoning_for/figures/013_Table_3.jpg]]
*Table 3: Performance improvements on AIME24/25 through progressive refinement steps*

**RL 奖励设计**：Table 27 的消融实验表明，仅在答案正确时附加工具使用奖励（α=0.1, β=0.01, R_max=1）可获得最佳平均准确率 62.6%，优于无工具奖励的 60.2%。这验证了复合奖励设计能有效引导模型在保证正确性的前提下高效使用工具。

**效率与 token 节省**：代码增强推理平均比纯文本减少 1.3k–3k 个 token（Table 23），同时准确率更高。这说明工具调用不仅提升了精度，还压缩了推理长度，实现了“更准且更短”的双重收益。

**训练基础设施加速**：异步调度结合 Agentic Partial Rollout 和前缀感知负载均衡，实现了 **4–5 倍**的端到端训练吞吐量提升（Figure 2）。其中，工具调用延迟从 175s 降至 1.2s，Partial Rollout 单独贡献 2.2–2.5 倍加速（Section 2.4）。

### 训练动态与多阶段 RL

Figure 3 展示了多阶段 RL 训练过程中关键指标的演变。随着训练步数增加，模型准确率持续攀升（AIME24 从 78.4% 提升至 89.8%），同时响应长度和代码调用次数逐步增长，但长度截断率和代码截断率始终控制在 10% 以下。训练分三阶段动态扩展上下文窗口（48k → 72k → 96k tokens）和工具调用上限（48 → 72 → 96 次），使模型逐步适应更复杂的推理链。

### 局限性

尽管 AgentMath 取得了显著成果，仍存在以下局限：
- **计算成本高**：完整训练流水线（数据合成+清洗+SFT）在 128 张 GPU 上需约 109 小时。
- **领域泛化未验证**：当前仅在数学竞赛基准上测试，在更广泛的科学推理或现实任务上的表现尚不明确。
- **上限约束**：代码调用次数（96 次）和序列长度（96k tokens）的上限可能制约极复杂问题的求解。
- **教师模型依赖**：数据合成依赖 DeepSeek‑R1/V3 等大型教师模型，可能引入知识偏差或风格偏好。

### 开放性研究问题
- 工具增强数据规模与性能提升之间是否持续保持对数线性增长？
- 模型能否通过大规模 Agent RL 发展出完全自适应的工具调用策略，无需预设调用次数上限？

### 补充图表

![[assets/figures/papers/iclr26_0010_e2s7YHeVZW_AgentMath_Empowering_Mathematical_Reasoning_for/figures/014_Table_4.jpg]]
*Table 4: Performance comparison (avg@32 accuracy) of AgentMath against state-of-the-art models on AIME24, AIME25, and HMMT25 benchmarks. Evaluation follows DeepSeek-R1 framework (temperature=0.6, top p=0.95). AgentMath models (highlighted in blue) achieve superior results across all scales, with the 30B variant competitive against 671B models*




## 定位与知识库关联

### 核心瓶颈与因果机制

AgentMath 的核心洞察在于：纯文本长链推理在处理需要精确计算或符号操作的数学问题时，存在固有的效率与准确性瓶颈。高质量的工具使用数据稀缺，且现有强化学习方法无法有效优化工具调用策略。AgentMath 通过将代码解释器集成到推理链中，并利用自动化合成工具增强轨迹数据与 Agentic RL，使模型自主学习最优工具调用策略，从而显著提升准确率与效率。

### 与基线方法的关系

AgentMath 在多个规模上与纯文本和工具增强基线进行了系统对比。在 1.5B 规模，工具增强基线 CoRT-1.5B 和纯文本基线 OpenReasoning-1.5B 为小规模工具使用提供了参照点。在 8B 规模，AgentMath-8B 在 AIME24 上达到 89.8%，相较纯文本基线 DS-0528-Qwen3-8B 的 86.0% 提升 3.8 个百分点；在 AIME25 上优势更为显著（84.7% vs. 76.3%，+8.4%）。在 30B 级，AgentMath-30B-A3B 在 AIME24 上达到 90.6%，超越纯文本基线 Qwen3-30B-A3B-Thinking-2507（87.7%）和工具增强基线 STILL-3-TOOL-32B，并超越 OpenAI-o3-mini 和 Claude-Opus-4.0-Thinking，接近 DeepSeek-R1-671B 的性能水平。

公平性方面，论文通过控制实验与 ReTool 等方法进行对比：在相同基础模型和教师数据下，AgentMath 在 SFT 阶段（44.1% vs. 40.9%）和 RL 阶段（74.8% vs. 67.0%）均显著优于对比方法，表明性能增益主要源于工具增强轨迹合成方法与 Agentic RL 范式，而非教师模型或基础模型的选择。

### 关键设计决策与消融证据

**数据质量的关键作用。** 逐步多维质量细化将 AIME24 准确率从初始未细化的 35.3% 提升至完整流水线的 60.5%，验证了数据质量在工具增强轨迹合成中的决定性作用（Table 3）。

**RL 效率的显著提升。** 工具增强 RL 仅需约 400 训练步数即达到 AIME24 上 76.2% 的准确率，而纯文本 RL 需要约 1600 步才能达到 68.7%，效率提升约 4 倍（Table 2, Figure 4）。这表明 Agentic RL 范式在样本效率上具有本质优势。

**奖励设计的精细权衡。** 仅在正确回答上施加工具使用奖励（α=0.1, β=0.01）可获得最佳平均准确率 62.6%，优于无工具奖励基线 60.2%（Table 27）。复合奖励设计 $R_{\mathrm{total}} = R_{\mathrm{acc}} + \mathbb{I}(R_{\mathrm{acc}} = 1) \cdot R_{\mathrm{tool}}$ 有效鼓励了正确且高效的工具使用，避免了盲目调用代码的负面激励。

**推理效率的改善。** 代码增强推理平均比纯文本减少 1.3k–3k 个 token，且准确率更高（Table 23），证明工具调用不仅提升准确性，同时压缩了推理长度。

**训练系统的加速。** 异步式部分展开训练系统实现了 4–5 倍的端到端训练吞吐量提升。其中，并行化将工具调用延迟从 175 秒降至 1.2 秒，Agentic Partial Rollout 贡献 2.2–2.5 倍加速。

### 适用边界与局限

1. **计算成本高昂。** 完整的训练流水线（数据合成+清洗+SFT）在 128 张 GPU 上需要约 109 小时，对资源受限的研究团队构成显著门槛。
2. **领域泛化性未验证。** 当前仅在数学竞赛基准（AIME24/25, HMMT25）上验证，在更广泛的科学推理或现实任务上的泛化性尚未充分探究。
3. **硬性约束限制。** 代码调用次数上限（96 次）和序列长度上限（96k tokens）可能制约极复杂问题的解决能力，模型无法在超出预算时自主调整策略。
4. **教师模型依赖。** 依赖大型教师模型（DeepSeek-R1/V3, Qwen3-30B）生成数据，可能引入教师模型的知识偏差或风格偏好。尽管所有训练数据经过严格的 n‑gram 和语义去重，确保与评估集无重叠，但教师模型的蒸馏过程可能仍引入部分优势。
5. **大规模 RL 未验证。** AgentMath-235B-A22B 因计算资源限制仅通过 SFT 训练，未进行 Agentic RL，大规模下的 RL 扩展性仍有待验证。

### 开放问题

1. **数据规模的扩展性。** 代码辅助数学推理中数据规模与性能提升的关系是否持续保持对数线性增长？当前合成数据量为 20k，更大规模的数据合成是否仍能带来显著增益？
2. **自适应工具调用策略。** 模型是否能通过大规模 Agent RL 持续改进，并发展出完全自适应的工具调用策略（如自主决定何时以及如何使用工具，而无需预设调用次数上限）？当前仍需人工设定预算约束。
3. **跨领域迁移。** AgentMath 的工具增强范式是否能迁移至物理、化学、编程等需要精确计算的领域？不同领域的工具接口和奖励设计可能需要针对性的调整。
4. **工具多样性的扩展。** 当前仅集成代码解释器，未来是否可扩展至符号计算引擎、定理证明器等多种工具，并让模型自主选择最优工具组合？



## 原文 PDF

![[paperPDFs/ICLR_2026/AgentMath_Empowering_Mathematical_Reasoning_for_Large_Language_Models_via_Tool_Augmented_Agent.pdf]]
