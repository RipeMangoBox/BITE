---
title: "Achieving Olympia-Level Geometry Large Language Model Agent via Complexity Boosting Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Achieving_Olympia_Level_Geometry_Large_Language_Model_Agent_via_Complexity_Boosting_Reinforcement_Learning.pdf
project_link: null
code_link: null
aliases:
- AOLGLLMACBRL
- InternGeometry
tags:
- ICLR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: "通过长周期 LLM‑工具交互（>200 步）积累几何性质并反射反馈，结合动态记忆压缩和复杂度渐进课程，使智能体能从弱启发式逐步过渡到强探索能力。"
primary_logic: "让 LLM 智能体像人类一样进行探索性试探：在每轮中自然语言思考并输出命题或辅助构造，利用符号引擎验证，根据结果反思，并通过压缩历史保持长期记忆，从而无需依赖大规模数据预训练即可解决高难度的几何证明问题。"
claims:
- "InternGeometry 在 IMO 50 测试集上解决 44/50 题，超过金牌选手平均分 40.9 分。"
- "仅使用 13K 训练数据，为 AlphaGeometry 2 的 0.004%，数据效率极大提升。"
- "移除动态记忆压缩后性能暴跌至 23/50，证明长周期记忆是成功关键。"
- "复杂度提升强化学习 (CBRL) 比冷启动 SFT 或均匀难度训练显著提升 IMO 得分 (44 vs 22~38)。"
---

# Achieving Olympia-Level Geometry Large Language Model Agent via Complexity Boosting Reinforcement Learning

> [!tip] 核心洞察
> 让 LLM 智能体像人类一样进行探索性试探：在每轮中自然语言思考并输出命题或辅助构造，利用符号引擎验证，根据结果反思，并通过压缩历史保持长期记忆，从而无需依赖大规模数据预训练即可解决高难度的几何证明问题。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 通过复杂度提升强化学习实现奥林匹克级几何大语言模型智能体 |
| 英文题名 | Achieving Olympia-Level Geometry Large Language Model Agent via Complexity Boosting Reinforcement Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=1sffPGGQyT) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | InternGeometry |
| Dataset | IMO 50 |

> [!tip] 效果简介
> - IMO 50 上，Pass@K (K=256) 为 44/50，对比 42/50 (AlphaGeometry 2)，变化 +2。
> - IMO 50 上，Pass@K (K=256) 为 44/50，对比 43/50 (SeedGeometry)，变化 +1。
> - IMO 50 上，Pass@K (K=256) 为 44/50，对比 约 40.9 (IMO 金牌选手平均分)，变化 约 +3.1。

## 概要

国际数学奥林匹克（IMO）级别的几何问题之所以极具挑战性，根本瓶颈在于解题所需的辅助构造高度依赖启发式直觉，而传统方法**难以系统性地习得这些弱启发式规则**。现有专家系统（如 AlphaGeometry 2、SeedGeometry）通过大规模数据预训练和巨型搜索树来模仿解题过程，但泛化性受限，且**数据效率极低**。

**InternGeometry 提出了一种范式转变**：不再依赖专家模型指导的固定深度搜索，而是让大语言模型（LLM）智能体像人类一样进行探索性交互——在每轮中输出自然语言推理和形式化动作（如构造点、添加辅助线、提出子命题），由符号引擎验证并返回反馈，智能体再根据结果进行反思与调整。这种**长周期 LLM‑工具交互**可达 200 步以上，通过**动态记忆压缩模块**保留核心推理步骤，克服了长上下文带来的信息衰减。在此基础上，**复杂度提升强化学习（CBRL）** 通过动态调控合成问题的证明难度（以 DDAR 步数衡量），使智能体从弱启发式逐步过渡到强探索能力，最大化学习信号。

核心结果如下：

- 在包含 50 道 IMO 几何题（2000‑2024）的基准上，InternGeometry 以 32B 参数规模的 LLM 智能体**解出 44 题**，超过 IMO 金牌选手平均分（40.9 分），也优于 AlphaGeometry 2（42 题）和 SeedGeometry（43 题）。
- 仅使用 **约 13K 条训练数据**，数据规模仅为 AlphaGeometry 2 的 0.004%，极大提升了数据效率。
- 消融实验表明，**动态记忆压缩**、命题证明步骤、慢思考（multi‑step reasoning）和基于规则的拒绝采样是成功的关键：移除这些组件后，性能从 44 题骤降至 23 题。仅靠冷启动监督微调而不进行强化学习，性能只有 22 题。
- 测试时**延长交互轨迹长度**比单纯增加采样次数更能有效提升解题率，证实了长周期探索在几何推理中的可缩放性。
- 尚未解决的问题（如 2001 P1、2006 P6 等）多涉及数值分析或非纯几何构造，提示当前方法向混合数学领域外推仍需进一步研究。

InternGeometry 的成功表明，通过**构造‑验证‑反思的交互闭环**和**难度渐进式在线强化学习**，LLM 智能体能够突破启发式薄弱这一传统几何定理证明的核心障碍，为通用数学智能体的发展提供了新的范式。



国际数学奥林匹克（IMO）中的几何问题通常表现为构造简单但求解高度复杂的证明题。例如，IMO 2018 Problem 6 的构图仅由少量点线构成，却需要极精巧的辅助构造（如等角共轭点）才能完成证明（Figure 1）。这种“构图简单、思考复杂”的特点，使得单纯依赖固定搜索树或预定义启发式规则的传统几何证明系统面临严峻挑战。

现有顶级几何证明系统 AlphaGeometry 2 和 SeedGeometry 均采用专家模型驱动的大规模符号搜索树。它们需要海量合成数据进行预训练，并依靠复杂的集成搜索策略来弥补启发式规则的不足。然而，这种范式存在三个根本缺口：

1. **辅助构造的启发式极弱**：实际证明中所需的辅助点与线的选择往往缺乏明确的局部信号，专家模型不得不依赖广度优先搜索，导致搜索空间呈指数级膨胀；
2. **缺乏长程上下文保持能力**：现有系统在搜索树中仅维持固定深度的展开（如 beam depth=4），无法像人类一样在长达数十步的推理中积累中间引理并动态调整策略；
3. **训练与推理的数据效率低下**：AlphaGeometry 2 使用了约 3 亿条合成数据，SeedGeometry 也使用了约 2.3 亿条，且模型不具跨问题泛化的探索能力。

上述缺口造成三大后果：性能瓶颈（AlphaGeometry 2 和 SeedGeometry 在 IMO 50 上分别解决 42 和 43 题，但仍遗留多个困难问题）、推理代价高昂（需要并行展开数千个搜索节点）以及无法迁移到非纯几何问题。

本研究的目标是构建一个**类人几何证明智能体**，通过长周期自然语言推理与符号引擎的深度交互，从弱启发式探索逐步过渡到强探索能力，从而仅用极少量数据（约 13K 条，为 AlphaGeometry 2 的 0.004%）达到甚至超越专家模型的性能。该智能体在 IMO 50 基准上解决 44 题，超过了金牌选手平均分（40.9 分），为解决符号推理与语言推理的融合提供了新的范式。



## 核心方法与创新机理

InternGeometry 的核心创新在于将 IMO 级几何证明从传统的**专家模型 + 大规模搜索树**的范式，转变为**LLM 智能体长周期探索式推理**的新范式。其关键突破体现在以下四个"changed slots"：

### 1. 求解范式转换：从搜索树到探索式智能体

AlphaGeometry 2 和 SeedGeometry 等基线方法依赖专家模型指导大规模搜索树（通常 beam depth 4），而 InternGeometry 采用 LLM 智能体通过多轮自然语言推理与符号引擎交互进行探索性证明（confidence 0.95, Abstract & §2.2）。每轮中，智能体以自然语言进行"慢思考"（Slow Thinking），输出**命题证明**（<propose>）或**辅助构造**（<build>/<add>），由符号引擎验证后根据反馈反思调整。这种"试探—验证—反思"的循环模拟了人类几何专家的探索过程，从根本上绕过了对大规模预训练数据的依赖。

**消融证据**：移除命题证明步骤后，IMO 50 得分从 44 降至 35；同时移除命题证明和慢思考后，性能崩溃至 23/50（Table 3, confidence 0.85），证明单纯的辅助构造搜索远不足以支撑 IMO 级推理。

### 2. 交互长度突破：动态记忆支撑超长周期推理

基线方法的搜索深度固定且有限，而 InternGeometry 引入**动态记忆压缩模块 W**，将多轮交互历史压缩为核心动作与关键反馈的摘要，使智能体能够维持超过 200 步的连续推理（§2.2, confidence 0.95）。这一机制解决了 LLM 上下文窗口有限与长周期探索之间的矛盾。

**消融证据**：移除上下文压缩后性能暴跌至 23/50（Table 3, confidence 0.85），证明动态记忆是实现长周期推理的关键瓶颈。此外，Figure 3（confidence 0.95）显示延长智能体轨迹长度比增加采样次数更有效地提升 Pass@K，验证了长周期交互的独特价值。

### 3. 训练课程创新：复杂度提升强化学习 (CBRL)

基线方法无课程或使用固定难度数据，而 CBRL 通过**合成问题的 DDAR 证明步数**作为复杂度度量 $\kappa$，动态调整训练数据难度，使智能体的平均奖励趋近 0.5 以最大化学习信号（§2.3 & §2.4, confidence 0.95）。其理论依据源于二元奖励下期望绝对优势 $2\sqrt{p(1-p)}$ 在 $p=0.5$ 时取最大（Equation (10)），通过 Algorithm 3 实现 $\kappa$ 的自动调节。

**消融证据**：冷启动 SFT 仅达 22/50，仅使用简单或困难数据分别为 29/50 和 24/50，相同数据但无课程调度为 38/50，均显著低于 Full CBRL 的 44/50（Table 4, confidence 1.0）。这表明 CBRL 的**渐进式复杂度课程**和**在线 GRPO 优化**的组合是性能提升的基础。

### 4. 推理稳健性增强：基于规则的拒绝采样 PassCheck

基线方法的原始解码输出容易出现重复动作或格式错误。InternGeometry 引入 PassCheck 规则过滤（§2.2, confidence 0.9），在推理时自动拒绝重复动作、格式错误和过长无动作回合，防止**动作坍塌**。

**消融证据**：移除拒绝采样后性能降至 38/50（Table 3, confidence 0.85），证实动作过滤机制的有效性。

---

### 方法论局限与待验证线索

上述创新的边界条件需要关注：
- **未解决的 6 道 IMO 题**（2001 P1, 2002 P6, 2003 P3, 2006 P1, 2006 P6, 2020 P6）主要涉及数值分析或非纯几何构造，表明方法在融合数值推理时的泛化能力存在瓶颈，需手动验证其是否因符号引擎表达能力受限。
- **推理成本**：InternGeometry 使用 32B 模型并生成较长 token 序列，推理成本高于传统专家模型，但因其未开源对手无法定量对比，该结论需要手动核实。
- **冷启动数据偏向**：数据合成依赖于形式化已有几何问题，可能导致对特定问题类型的过拟合，论文未提供跨分布泛化的独立测试，需要额外实验验证。



![[assets/figures/papers/iclr26_0006_1sffPGGQyT_Achieving_Olympia-Level_Geometry_Large_Language/figures/002_Figure_2.jpg]]
*Figure 2: An overview of InternGeometry and Complexity-Boosting Reinforcement Learning (CBRL). (a) InternGeometry performs natural-language reasoning (Think), outputs a structured action in a domain-specific language (Action), and receives execution results (Feedback) in each turn. A dynamic memory module W compresses the multi-turn interaction history to preserve essential actions and outcomes. (b) CBRL optimizes the agent policy by generating synthetic training data with controllable difficulty, assigning binary rewards to effective steps and successful outcomes, and optimizing policy through iterative reinforcement learning*

InternGeometry 的整体设计围绕一个核心命题展开：IMO 级别的几何问题通常仅需少量初始构图，但求解却依赖于极难预判的辅助构造和中间命题，这使得单纯依赖搜索或专家模型的方法效率低下。为了突破这一瓶颈，InternGeometry 将证明过程组织成长周期 LLM‑工具交互的闭环，让智能体像人类解题者一样，进行试探性的推理、构造、验证和反思，并通过动态记忆压缩维持长上下文的信息效率。整个系统由一条推理流水线和一条训练流水线共同构成，前者在推理时以超过 200 步的交互逐步逼近证明，后者通过复杂度提升强化学习（CBRL）逐步增强智能体的探索能力。

推理流水线的核心是一个多轮、状态化的交互循环（参见 Figure 2a）。给定一个形式化几何问题 $X$，智能体（基于 InternThinker‑32B 的 LLM）在每一轮执行三个紧密耦合的阶段：
1. **思考（Think）**：智能体根据动态记忆模块 $\mathfrak{W}$ 压缩后的历史 $H_{t-1}$，生成自然语言推理 $P_t$，表达当前阶段的猜测、目标和直觉。
2. **动作（Action）**：紧接着输出形式化的领域特定语言（DSL）动作代码 $A_t$，包含三类基础操作：`<build>`（构造基本几何元素）、`<add>`（添加辅助点/线/圆）和 `<propose>`（声明并请求验证一个几何命题）。输出会经过 PassCheck 拒绝采样过滤，仅当动作不重复、格式正确且不与历史冲突时才会被执行，从而防止动作坍塌。
3. **反馈（Feedback）**：InternGeometry‑DDAR 符号引擎（基于 Newelid 的交互式几何证明环境）执行 $A_t$，返回执行结果 $O_t$ 并更新引擎状态 $\mathfrak{E}_t$。若命题被引擎验证为真，该结论会成为后续推理可引用的已知事实；若失败，智能体将获得失败的信号。随后，整轮交互内容 $[P_t, A_t, O_t]$ 被追加入历史 $H_t$。

这一过程可形式化为

$$
[P_t, A_t] = \mathbb{G}\big(X, \mathfrak{W}(H_{t-1})\big), \qquad
O_t, \mathfrak{E}_t = \mathfrak{E}_{t-1}(A_t), \qquad
H_t = H_{t-1} + [P_t, A_t, O_t],
$$

其中 $\mathbb{G}$ 为智能体策略，$\mathfrak{W}$ 为动态记忆压缩模块。该循环持续进行，直到智能体输出终止动作或达到最大步长限制。正是这种"思考—行动—反思"的闭环，使 LLM 能够利用符号引擎的严格验证不断修正其启发式搜索方向，无需依赖大规模专家数据即可逼近复杂构造。

长周期交互之所以可行，关键在于动态记忆模块 $\mathfrak{W}$。随着轮次增加，完整历史会迅速超出模型的上下文窗口。$\mathfrak{W}$ 负责将多轮历史压缩为一则简洁摘要，仅保留已成功证明的核心命题、关键辅助构造以及重要反馈，丢弃冗余的尝试和失败的中间步骤。这一设计使得交互步数能够扩展至 200 步以上，且消融实验表明移除该模块后 IMO‑50 的通过率会从 44/50 暴跌至 23/50，证明长周期记忆是实现高水平推理的必要条件。

训练侧的流水线则围绕复杂度提升强化学习（CBRL）展开（Figure 2b）。CBRL 在两条核心原则下运作：
1. **可控难度的数据合成**：通过数据合成管道，系统以 DDAR 证明步数 $\kappa$ 作为任务复杂度的度量，生成大量形式化几何问题‑解答对。冷启动阶段，这些数据用于监督微调（SFT），使智能体初步掌握交互范式。
2. **基于奖励信号的在线课程**：SFT 之后，采用 GRPO 进行在线策略优化。每一条完整轨迹获得复合二元奖励 $r = r^o \wedge r^s$，其中 $r^o$ 表示整体证明是否成功，$r^s$ 表示该步动作是否有效。CBRL 的核心机制在于动态调节合成数据的难度 $\kappa$：当智能体在某个 $\kappa$ 范围内的平均成功率过高（平均奖励 > 0.5）时，上调 $\kappa$ 以增加难度；反之则下调。这样做的理论依据是，在二元奖励下，当成功概率 $p = 0.5$ 时期望优势最大，从而能最大化策略梯度的学习信号。

综上，InternGeometry 的整体框架将几何证明重塑为一个由符号引擎反馈指导的、具备动态记忆和难度递增课程的长周期探索过程。输入为形式化问题 $X$，输出为成功或失败的证明轨迹；训练则以合成数据为驱动，通过 CBRL 使智能体从弱启发式逐步进化到具备对标 IMO 金牌选手的强探索能力。这一设计从根本上规避了传统方法对专家模型和有界搜索的巨大依赖，在仅使用约 13K 训练数据（约为 AlphaGeometry 2 的 0.004%）的条件下实现了 44/50 的 IMO‑50 成绩。



InternGeometry 以交互式 LLM‑符号引擎协作范式替代传统的专家搜索树，其能力核心由五个关键模块支撑：InternGeometry‑DDAR 几何证明引擎、长周期 LLM 智能体、动态记忆压缩、先验引导的拒绝采样 (PassCheck) 以及复杂度提升强化学习 (CBRL) 的训练框架。以下逐项阐述模块机制与决定性公式，未在文中出现的公式或推导不作臆造。

### 1. 交互式几何证明引擎 InternGeometry‑DDAR
引擎基于 Newclid，支持动态构图、约束优化和子目标验证（Section 2.1）。智能体通过三种 DSL 标签 `<build>`、`<add>` 和 `<propose>` 发出形式化动作，引擎执行后返回状态更新与反馈。它既是智能体的验证工具，也是后续合成难控数据的构造基础。

### 2. 长周期 LLM 智能体与动态记忆压缩
智能体采用 InternThinker‑32B，在每一轮先进行自然语言推理（Think），再输出形式化动作（Action）。为支撑超 200 步的长程探索，引入动态记忆压缩模块 $\mathfrak{W}$，将多轮交互历史压缩为保留核心动作与结果的高效摘要，从而在有限上下文窗口内持续积累几何性质。

第 $t$ 步的输出形式化为：
$$
[P_t, A_t] = \mathbb{G}\big(X,\, \mathfrak{W}(H_{t-1})\big) \tag{1}
$$
其中 $X$ 为问题文本，$H_{t-1}$ 为前 $t-1$ 步的完整历史，$\mathfrak{W}$ 为压缩函数；$P_t$ 为自然语言推理，$A_t$ 为形式化动作代码。

执行动作并更新历史：
$$
O_t,\; \mathfrak{E}_t = \mathfrak{E}_{t-1}(A_t),\qquad H_t = H_{t-1} + [P_t,\, A_t,\, O_t] \tag{2}
$$
$O_t$ 为引擎返回的观察（如成功/失败或运算结果），$\mathfrak{E}_t$ 为更新后的引擎状态。

### 3. 先验引导的拒绝采样（PassCheck）
为防止动作坍塌，每一轮采样得到候选输出 $[\hat{P}_t, \hat{A}_t]$ 后，仅当通过规则检查时才被接受，否则重新采样：
$$
\text{If } \mathrm{PassCheck}\big([\hat{P}_t,\hat{A}_t]\big) : \quad \mathbb{G}\big(X,\, \mathfrak{W}(H_{t-1})\big) = [\hat{P}_t,\hat{A}_t] \tag{3}
$$
规则包括：动作不得与历史重复、格式符合 DSL 语法、不能出现连续多轮无有效动作等（Section 2.2）。

### 4. 复杂度提升强化学习 (CBRL) 训练框架
CBRL 通过控制合成问题的 DDAR 证明步数 $\kappa$ 来调节难度，使智能体在合适的学习信号密度下进行在线强化学习。训练流程包含冷启动监督微调、GRPO 策略优化、复合奖励设计和复杂度自适应调节。

#### 4.1 冷启动监督微调损失
使用形式化的问题‑解答序列，最小化负对数似然：
$$
L_{st} = \frac{1}{N}\sum_{i=1}^N \left[-\sum_{t=1}^T \log G_\theta\!\big(y_t^i \mid x^i,\, h_t^i\big)\right] \tag{4}
$$
其中 $G_\theta$ 为参数 $\theta$ 的策略网络，$y_t^i$ 为第 $i$ 个样本第 $t$ 步的真实动作，$h_t^i = \mathfrak{W}(H_{t-1}^i)$ 为压缩历史。

#### 4.2 GRPO 策略梯度
在线 RL 采用 PPO 风格的目标，加入 KL 正则项以约束策略更新幅度：
$$
\nabla J_{rl}(X,\theta) = \mathbb{E}_{y,h\sim G_\theta(\cdot\mid X)} \sum_{t=1}^T \min\!\left(\frac{G_\theta(y_t\mid X,h_t)}{G_{\theta_{old}}(y_t\mid X,h_t)},\,\mathrm{clip}(\dots)\right) A(X,y_t)\,\nabla G_\theta(y_t\mid X,h_t) \;-\; \beta\,\nabla \mathbb{D}_{\mathrm{KL}}\big(G_\theta \parallel G_{ref}\big) \tag{5}
$$
式中 $G_{\theta_{old}}$ 为旧策略，$A$ 为优势函数，$\beta$ 控制 KL 惩罚强度。

#### 4.3 复合二元奖励
每一步的即时奖励定义为整体证明成功与当前动作有效的逻辑与：
$$
r = r^o \;\wedge\; r^s \tag{7}
$$
$r^o=1$ 表示整题被完全证明，$r^s=1$ 表示该步动作语法正确且被引擎接受；两者同时为 1 时智能体获得正奖励。

#### 4.4 CBRL 的训练目标与复杂度自适应
CBRL 的优化目标是最大化复杂度为 $\kappa$ 的合成问题分布上的 RL 目标：
$$
\theta^* = \arg\max_\theta \mathbb{E}_{X\sim \mathfrak{X}(\kappa)} J_{rl}(X,\theta) \tag{8}
$$
二元奖励下的期望绝对优势 $\mathbb{E}[|A_i|]$ 解析表达式为：
$$
\mathbb{E}[|A_i|] = 2\sqrt{p(1-p)} \tag{10}
$$
该值在平均成功率 $p \approx 0.5$ 时达到最大。训练中根据当前策略在难度 $\kappa$ 上的平均奖励，动态调整 $\kappa$ 使奖励均值趋近 0.5，从而最大化策略梯度的有效幅度（Algorithm 3, Appendix D）。

#### 4.5 数据合成管道
配合 CBRL，合成管道通过首先生成随机几何构图，再利用 DDAR 引擎筛选出证明步数恰好为 $\kappa$ 的非平凡问题‑解答对（Algorithm 1‑2, Appendix D）。合成实例经引擎验证有效，其复杂度 $\kappa$ 直接由 DDAR 证明步数标定。训练时从最新分布 $\mathfrak{X}(\kappa)$ 中采样，支持在线更新策略而无需人工标注。

上述模块级联使得 InternGeometry 能够从弱启发式逐步进化到强探索策略，仅用 13K 训练数据即在 IMO 50 基准上求解 44/50 题。消融实验表明确舍去动态记忆压缩或 CBRL 课程均会导致性能大幅衰退（Table 3, Table 4），印证了模块与公式在高难度几何推理中的不可替代性。



## 实验与关键发现

InternGeometry 在 IMO‑50（2000‑2024 年所有 IMO 几何题）上以 256 次采样（Pass@256）解出 44/50 题（Table 1），超过 IMO 金牌选手的平均分 40.9 分和此前的专家模型 AlphaGeometry 2（42/50）与 SeedGeometry（43/50），而训练数据仅约 13 K，约为 AlphaGeometry 2 数据量的 0.004%。逐题对比（Table 2）显示，InternGeometry 额外攻克了早期方法无法解决的 IMO 2018 P6、2023 P6 等难题，表明长周期智能体范式在弱启发式辅助构造问题上的优势。

![[assets/figures/papers/iclr26_0006_1sffPGGQyT_Achieving_Olympia-Level_Geometry_Large_Language/figures/003_Table_1.jpg]]
*Table 1: Comparison of overall performance on IMO 50 between InternGeometry and SOTA geometry expert models*

### 长周期交互能力的消融分析

为刻画"思考‑动作‑反馈"循环中各组件的贡献，论文依次移除四个关键设计（Table 3）。移除命题证明步骤（仅保留添加辅助构造）导致 solvable 题数从 44 降至 35；进一步取消慢思考（长链自然语言推理）后性能再降回 23/50。独立移除上下文压缩（动态记忆模块 $\mathfrak{W}$）同样使性能暴跌至 23/50。这些结果表明，将多轮交互历史压缩为简洁摘要以维持超过 200 步的有效上下文，是智能体在困难问题上不断改进试探策略的核心条件。拒绝采样（PassCheck）移除后性能掉至 38/50，说明通过规则过滤重复、格式错误或无效动作可以防止动作坍塌，稳定探索。

![[assets/figures/papers/iclr26_0006_1sffPGGQyT_Achieving_Olympia-Level_Geometry_Large_Language/figures/007_Table_3.jpg]]
*Table 3: Ablation study on long-horizon agents in InternGeometry*

推理预算的分配实验（Figure 3）进一步揭示，增加单次推理的最大交互步长（即延长轨迹长度）比单纯增加采样次数 $K$ 更能高效提升 Pass@K。当总推理预算固定时，长轨迹（如 200 步）的收益提升速率显著快于短轨迹（64 步）只靠重复采样的情形。这意味着，通过扩大上下文窗口引入更丰富的试探过程，可使智能体逐步积累更强的启发式能力。

![[assets/figures/papers/iclr26_0006_1sffPGGQyT_Achieving_Olympia-Level_Geometry_Large_Language/figures/006_Figure_3.jpg]]
*Figure 3: Left: The effect of long-horizon interaction on the proof. As the interaction steps increase, the proving success rate improves significantly, which holds for different sampling times. As sampling times increase, Pass@K also rises, indicating the test-time scalability of InternGeometry. Right: Extending the agent's trajectory length is more effective than repeated sampling for scaling. The total inference budget is defined as the sampling number K multiplied by the agent's steps. When the maximum length is capped (the blue lines), performance improves with inference budget at a slower rate for shorter trajectories. On the other hand, when the sampling size is fixed (the green lines), increa...*

### 复杂度提升强化学习（CBRL）课程消融

CBRL 课程策略的消融结果（Table 4）显示，仅使用冷启动监督微调（SFT）无法获得有效的探索策略，IMO‑50 仅能解决 22 题。即便采用强化学习，若训练数据只包含简单题（29/50）或只包含难题（24/50），性能仍远不及完整的 CBRL 课程。即便是相同的数据池，若不对难度参数 $\kappa$ 进行动态调度，而使用均匀采样，性能也会从 44/50 下降至 38/50。这说明，依据智能体当前平均奖励动态调整合成问题的 DDAR 证明步长（使平均奖励趋近 0.5 以最大化策略梯度中的期望绝对优势 $2\sqrt{p(1-p)}$），能够有效生成"略高于当前能力"的训练样本，使模型持续获得有意义的学习信号，从而极大提升数据效率和最终训练效果。

![[assets/figures/papers/iclr26_0006_1sffPGGQyT_Achieving_Olympia-Level_Geometry_Large_Language/figures/010_Table_4.jpg]]
*Table 4: Ablation study on CBRL in InternGeometry*

### 训练动态与泛化表现

训练过程中，合成数据的 DDAR 证明长度分布呈现稳定向上的均匀提升（Figure 4 左），体现了 CBRL 从简单到困难的平滑课程安排。智能体在 IMO‑50 上的泛化 Pass@256 曲线（Figure 4 右）在训练轮次中稳步上升，并在第六轮出现显著跳升，说明随课程难度提升，模型成功习得了可迁移到真实 IMO 问题的高阶几何推理策略。

![[assets/figures/papers/iclr26_0006_1sffPGGQyT_Achieving_Olympia-Level_Geometry_Large_Language/figures/009_Figure_4.jpg]]
*Figure 4: Left: The distribution of proof lengths in the synthetic data generated during model training, indicating task complexity. The figure shows that the difficulty distribution of the synthetic data exhibits a fairly uniform improving trend, providing a well-structured curriculum from simple to difficult tasks. Right: Agent's generalization performance on IMO 50 during training. The agent's overall performance on IMO 50 shows a steady upward trend. Notably, there is a significant performance jump in the sixth training round*

### 失败模式与局限性

InternGeometry 在 6 道 IMO‑50 问题上持续失败（2001 P1、2002 P6、2003 P3、2006 P1、2006 P6、2020 P6）。这些问题普遍要求角不等式、距离不等式或多边形面积不等式等纯几何构造难以覆盖的数值与不等式推理，反映出当前方法在融合多数学领域时的泛化瓶颈。此外，InternGeometry 的推理成本因较大的模型（32B）和长链 token 消费而较高，但由于 AlphaGeometry 2 等专家模型未开源，无法进行公平的推理资源定量比较。整个系统依赖符号引擎的表达能力，因此引擎未覆盖的高级几何构造也会导致求解失败；冷启动数据主要来自形式化的现有几何问题，可能存在对特定问题范式的过拟合。



## 定位与知识库关联

InternGeometry 的提出标志着几何自动证明从以专家模型为核心的搜索范式转向以通用大语言模型（LLM）智能体为主体的探索式推理范式。在方法谱系中，其最直接的对比对象是 AlphaGeometry 2 与 SeedGeometry——二者均依赖领域特化模型将几何问题分解为大型搜索树，再由符号引擎执行确定性推理。InternGeometry 则以 LLM 智能体为中心，通过多轮"自然语言思考→形式化动作→引擎反馈→记忆压缩"的闭环交互，将求解过程从固定深度的树搜索转化为动态、长周期的探索式证明。这一转变具体体现在以下维度的重构上（Abstract, Section 2.2）：

- **求解范式**：从专家模型指导的搜索树转向 LLM 与工具交互的决策链。
- **交互长度**：从固定搜索树深度（如 beam depth 4）拓展到由动态记忆支持的 200 步以上的长周期交互。
- **历史建模**：从无历史或简单堆叠转为基于可学习压缩模块 ${\mathfrak{W}}$ 的动态记忆，只保留核心动作与关键反馈。
- **训练策略**：从无课程或均匀难度数据替换为复杂度提升强化学习（CBRL），由合成问题的 DDAR 证明步数 $\kappa$ 动态调控难度，使优势方差最大化。
- **动作控制**：引入基于规则的拒绝采样 PassCheck，在推理时滤除重复、格式错误或无效动作，防止动作模式坍缩。

这一系列改变的因果效应集中体现在数据效率与绝对性能的提升上：InternGeometry 仅使用约 13 K 条训练数据（约为 AlphaGeometry 2 的十万分之四），便在 IMO 50 基准上达到 44/50 的 Pass@256 成绩，超出金牌选手平均水平（约 40.9 分）并微弱领先 AlphaGeometry 2（42/50）与 SeedGeometry（43/50）（Table 1）。这表明，LLM 智能体通过探索性试探与长周期记忆，至少可以在纯几何证明问题上匹敌甚至超越依赖海量数据与专家架构的系统。

**适用边界与局限**。该方法的有效性高度依赖符号引擎的表达能力与可验证性：它适用于可由 Newclid 风格的 DDAR 引擎完整形式化与判定的纯几何构造问题。在当前实现下，那些需要数值计算、不等式分析或跨数学领域推理的问题（如 IMO 2001 P1 的角不等式含数值条件、2002 P6 的圆覆盖距离不等式、2003 P3 的六边形距离与角度条件、2006 P1 的内点角不等式、2006 P6 的多边形面积不等式、2020 P6 的平面点集分离线）均超出系统边界，成为未解决的瓶颈。这一失效模式直接反映了符号环境在高级几何构造与数值混合推理方面的覆盖缺口，而非单纯由训练数据或模型规模决定。

其他局限包括：① 推理成本较高——32 B 模型需生成长达数百步的交互序列，但因对比系统未开源而无法严格定量比较；② 训练推理链的冷启动数据主要来自已有几何问题的形式化，可能导致对某种题目风格的过拟合；③ 对长周期记忆压缩的强依赖（消融实验中移除压缩导致 IMO 50 得分暴跌至 23/50，Table 3），暗示系统对上下文管理机制高度敏感；④ 动态课程虽然提升了训练效率，但环境奖励的二元性与稀疏性仍然限制了策略梯度的有效信号密度。

**开放问题**。上述未解决问题指明了系统向更一般数学定理证明方向扩展的核心挑战：如何将 CBRL 与长周期交互推广到需要符号-数值混合推理的问题。与此同时，更大规模的语言模型能否通过继续拓展推理预算来绕过引擎的表达瓶颈，仍有待验证。几何约束优化与不等式推理的整合机制，以及如何在不损失探索效率的前提下增强符号引擎的覆盖，是下一步研究的关键问题。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/Achieving_Olympia_Level_Geometry_Large_Language_Model_Agent_via_Complexity_Boosting_Reinforcement_Learning.pdf

![[paperPDFs/ICLR_2026/Achieving_Olympia_Level_Geometry_Large_Language_Model_Agent_via_Complexity_Boosting_Reinforcement_Learning.pdf]]
