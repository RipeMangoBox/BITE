---
title: "LongWriter-Zero: Mastering Ultra-Long Text Generation via Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/LongWriter_Zero_Mastering_Ultra_Long_Text_Generation_via_Reinforcement_Learning.pdf
project_link: null
code_link: null
openreview_forum_id: JWx4DI2N8k
aliases:
- LZ
- LongWriter-Zero
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "引入完全由强化学习（RL）驱动的训练框架，不依赖任何人工标注或合成数据。设计融合长度控制、写作质量和结构格式的复合奖励函数，通过组相对策略优化（GRPO）对模型进行训练，并配合“思考-回答”提示（<think>/<answer>）鼓励规划式推理。辅以大规模写作语料的持续预训练，提升基础模型的写作先验能力，从而引导模型自发涌现高质量的超长文本生成能力。"
primary_logic: "RL 能够通过奖励信号优化全局写作属性，相比 SFT 能够持续提升长文本质量；测试时思考（长 CoT）和持续预训练对于最大化 RL 在长文本生成中的效果至关重要，三者结合可使 32B 模型超越 100B+ 级别的基线模型。"
claims:
- "LongWriter-Zero在WritingBench上取得最高平均评分8.69，并在Arena-Write上获得Elo 1447，超过所有基线（包括DeepSeek-R1: 8.51/1343, Claude-Sonnet-4: 8.60/1185等）。"
- "消融实验中，移除持续预训练导致WritingBench平均分降至8.12、Elo降至1221；进一步移除思考提示后平均分降至8.04、Elo降至668，证明两项技术的关键性。"
- "RL在Arena-Write上始终优于SFT，即使从更强的持续预训练初始化，RL仍能大幅提升性能（Elo: 1221→1447），而SFT提升有限（Elo: 964→971）。"
- "WritingBench 上 平均批评分数 (1-10) = 8.69 (LongWriter-Zero)"
---

# LongWriter-Zero: Mastering Ultra-Long Text Generation via Reinforcement Learning

> [!tip] 核心洞察
> RL 能够通过奖励信号优化全局写作属性，相比 SFT 能够持续提升长文本质量；测试时思考（长 CoT）和持续预训练对于最大化 RL 在长文本生成中的效果至关重要，三者结合可使 32B 模型超越 100B+ 级别的基线模型。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | LongWriter-Zero：通过强化学习掌握超长文本生成 |
| 英文题名 | LongWriter-Zero: Mastering Ultra-Long Text Generation via Reinforcement Learning |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=JWx4DI2N8k) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | LongWriter-Zero |
| Dataset | WritingBench, Arena-Write, SFT vs RL (Arena-Write) |

> [!tip] 效果简介
> - WritingBench 上，平均批评分数 (1-10) 为 8.69 (LongWriter-Zero)，对比 DeepSeek-R1: 8.55, Claude-Sonnet-4: 8.60, Qwen3-235B: 8.68, GPT-4o: 8.16，变化 最高 (+0.01 ~ +0.53)。
> - Arena-Write 上，Elo评分 为 1447，对比 DeepSeek-R1: 1343, Qwen3-235B: 1343, DeepSeek-V3: 1236，变化 +104 相对于最佳基线。
> - SFT vs RL (Arena-Write) 上，Elo评分 为 RL: 持续预训练 + RL → 1447; Base + RL → 1221，对比 SFT: 持续预训练 + SFT → 971; Base + SFT → 964，变化 RL 显著优于 SFT，持续预训练对 RL 增益更大。

## 概要

当前大型语言模型在生成超长文本时面临根本性瓶颈：随着序列增长，模型普遍出现局部不连贯、内部矛盾、重复措辞、主题漂移乃至结构崩溃等问题。传统应对方案依赖监督微调（SFT）在合成长文本数据上训练，但高质量长文本数据构建困难且成本高昂，合成样本往往缺乏多样性并携带错误；更重要的是，最大似然目标无法显式优化全局写作属性（如连贯性、格式一致性），导致模型在长距离上下文中难以维持稳定的输出质量。

**LongWriter-Zero** 提出了一条完全不同的路径：不依赖任何人工标注或合成数据，从零开始利用强化学习（RL）诱导模型涌现超长、高质量文本生成能力。其核心洞见在于，RL 能够通过奖励信号直接优化全局写作属性，相比 SFT 实现持续且显著的质量提升；而测试时思考（长链思维提示）与大规模写作语料的持续预训练，则是最大化 RL 效果的关键杠杆——三者结合可使 32B 参数模型在长文本写作上超越 100B+ 级别的基线模型。

在方法层面，LongWriter-Zero 构建了由长度奖励模型、写作质量奖励模型和格式奖励模型组成的复合奖励函数，通过组相对策略优化（GRPO）对基础模型进行训练，并引入“思考-回答”提示格式（`<think>`/`<answer>`）鼓励模型在生成前进行深度规划与反思。在实验层面，LongWriter-Zero 在 WritingBench 上取得最高平均评分 8.69，在 Arena-Write 上获得 Elo 1447，均超过 DeepSeek-R1（8.55 / 1343）、Claude-Sonnet-4（8.60 / 1185）和 Qwen3-235B（8.68 / 1343）等强基线。消融实验进一步证实：移除持续预训练后 WritingBench 均分降至 8.12、Elo 降至 1221；再移除思考提示后均分进一步降至 8.04、Elo 骤降至 668，验证了两项技术的决定性作用。RL 与 SFT 的直接对比亦表明，即使从更强的持续预训练初始化出发，RL 仍能带来大幅性能跃升（Elo: 1221→1447），而 SFT 的提升极为有限（Elo: 964→971）。

大型语言模型（LLM）在短文本生成任务上已取得显著进展，但当输出长度扩展至数千乃至数万词时，模型普遍面临**局部不连贯、内部矛盾、重复措辞、主题漂移和结构崩溃**等系统性问题。这些失效并非简单的长度外推不足，而是反映了当前训练范式在优化长程依赖和全局一致性方面的根本局限。

传统应对方案主要依赖**监督微调（SFT）**，即利用人工或模型合成的长文本数据进行训练。然而，这一路线存在三重瓶颈：其一，高质量长文本数据的构建成本极高，且合成样本往往缺乏多样性并包含难以检测的错误；其二，最大似然估计（MLE）目标仅优化词级预测精度，无法显式建模连贯性、格式一致性和篇章结构等全局属性；其三，SFT 的改进空间受限于训练数据的质量天花板，难以持续提升。

上述瓶颈指向一个更深层的因果缺口：**长文本生成质量的关键不在词级拟合，而在于模型能否形成并执行全局规划**。这要求训练信号必须能够直接奖励那些跨越数百句乃至整个文档的优良属性，而非仅关注局部的下一个 token 预测。强化学习（RL）天然适合填补这一缺口——通过精心设计的奖励函数，RL 可以将长度控制、写作质量和结构格式等全局约束转化为可优化的目标，引导模型自发涌现高质量的长文本生成能力。

基于此，**LongWriter-Zero** 提出了一条从零开始的 RL 驱动路线：不依赖任何人工标注或合成数据，仅通过复合奖励模型和组相对策略优化（GRPO）训练模型，并辅以大规模写作语料的持续预训练和“思考-回答”提示策略，使 32B 参数模型在长文本生成质量上超越 100B+ 级别的基线系统。

## 核心方法与创新机理

### 从监督微调到强化学习的范式转移

当前大型语言模型在生成超长文本时面临系统性的质量退化：随着序列增长，模型输出逐渐出现局部不连贯、内部矛盾、重复措辞、主题漂移乃至整体结构崩溃。传统应对方案依赖**监督微调（SFT）**在合成长文本数据上训练模型，但这一路线存在两个根本性瓶颈：（1）高质量长文本数据的构建极为困难且成本高昂，合成样本往往缺乏多样性并携带难以检测的错误；（2）词级最大似然目标无法显式优化全局写作属性，如连贯性、格式一致性和长度控制。

LongWriter-Zero 的核心创新在于**完全摒弃对人工标注或合成数据的依赖**，转而采用从零开始的强化学习框架来驱动超长文本生成能力的涌现。这一范式转移体现在以下五个关键维度：

---

### 训练范式：从 SFT 到 GRPO

**基线方案**：在合成长文本数据上进行监督微调，模型通过最小化词级交叉熵损失来模仿训练样本。

**LongWriter-Zero**：采用**组相对策略优化（GRPO）**算法，从基础模型出发，完全通过奖励信号引导策略更新。具体而言，对每个查询从当前策略采样 $G=32$ 条完成结果，计算组内归一化优势：

$$A_i = \frac{r_i - \operatorname{mean}(\{r_1, \dots, r_G\})}{\operatorname{std}(\{r_1, \dots, r_G\})}$$

并通过剪切目标函数稳定训练（$\varepsilon=0.2$，KL 惩罚系数 $\beta=0$）：

$$\mathcal{J}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{q \sim P(Q), \{o_i\}_{i=1}^G \sim \pi_{\theta_{\mathrm{old}}}} \left[ \frac{1}{G} \sum_{i=1}^G \min \left( r_i^{\mathrm{ratio}} A_i, \operatorname{clip}(r_i^{\mathrm{ratio}}, 1-\varepsilon, 1+\varepsilon) A_i \right) \right]$$

这一设计的因果机制在于：GRPO 通过组内相对比较消除了绝对奖励尺度的影响，使模型能够从同一查询的多样化采样中学习相对优劣，而无需依赖外部价值函数或参考模型。

---

### 奖励信号：从词级损失到复合全局奖励

**基线方案**：词级最大似然损失，缺乏对全局写作属性的显式建模。

**LongWriter-Zero**：构建了由三个专业化奖励模型构成的复合奖励函数，最终优势信号为三者的等权平均：

$$A_{\mathrm{final}} = \frac{1}{3}(A_{\mathrm{length}} + A_{\mathrm{write}} + A_{\mathrm{format}})$$

1. **长度奖励模型（Length RM）**：利用 QwQ-32B 预测每个查询的合适目标词数范围 $[L_{\mathrm{lower}}, L_{\mathrm{upper}}]$，采用分段线性奖励函数——输出长度落在目标范围内得满分（$r_{\mathrm{length}}=1$），过短按比例惩罚，过长则线性衰减：

$$r_{\mathrm{length}}(o) = \begin{cases} 1, & \text{if } L_{\mathrm{lower}} \le len(o) \le L_{\mathrm{upper}}, \\ \frac{len(o)}{L_{\mathrm{lower}}}, & \text{if } len(o) < L_{\mathrm{lower}}, \\ \frac{L_{\mathrm{max}} - len(o)}{L_{\mathrm{max}} - L_{\mathrm{upper}}}, & \text{if } len(o) > L_{\mathrm{upper}}. \end{cases}$$

2. **写作质量奖励模型（Writing RM）**：以 Qwen2.5-72B 为骨干，在人工标注的偏好数据上基于 Bradley-Terry 模型训练，损失函数为：

$$\mathcal{L} = -\mathbb{E}_{(x, y_w, y_l) \sim D}[\log(\sigma(r_{\mathrm{write}}(x, y_w) - r_{\mathrm{write}}(x, y_l)))]$$

3. **格式奖励模型（Format RM）**：规则化检查 `<think>/<answer>` 标签结构的完整性和重复内容的出现频率，抑制奖励黑客行为。

---

### 提示策略：从直接生成到规划式推理

**基线方案**：直接生成回答（Direct-Answer），模型在无显式规划步骤的情况下一次性输出完整文本。

**LongWriter-Zero**：引入**“思考-回答”提示（Think Prompt）**，强制模型在 `<think>` 标签内进行深度规划与反思，再在 `<answer>` 标签内输出正式内容。这一设计借鉴了推理模型中长思维链（long CoT）的成功经验，但将其迁移至开放式写作任务。消融实验表明，移除思考提示后，Arena-Write Elo 从 1447 骤降至 668，证明测试时思考对全局结构和规划的因果重要性。

---

### 基础模型初始化：从原始预训练到写作先验注入

**基线方案**：直接使用原始预训练模型（Qwen2.5-32B）进行 RL 训练。

**LongWriter-Zero**：在 30B token 的高质量写作语料（覆盖中英文书籍、报告、学术论文等六大领域，见 Table 2）上进行**持续预训练**，并以 1% 比例混入从 Base-think 模型蒸馏的自校长 CoT 数据。这一步骤的核心作用是增强基础模型的写作先验能力，使 RL 训练在一个更优的初始化点上展开。消融实验显示，移除持续预训练后 WritingBench 平均分从 8.69 降至 8.12，Arena-Write Elo 从 1447 降至 1221，表明持续预训练是提升性能上限的关键因素。

---

### RL 与 SFT 的本质差异

Figure 4 展示了 RL 与 SFT 在 Arena-Write 上的性能对比，揭示了两个关键发现：

- **RL 始终优于 SFT**：无论从基础模型（Base）还是持续预训练模型（Continual Pretrain）初始化，RL 训练均大幅超越对应的 SFT 方案（Elo: 1221→1447 vs. 964→971）。
- **持续预训练对 RL 的增益远超 SFT**：持续预训练为 RL 带来的 Elo 提升达 226 分，而对 SFT 的提升仅 7 分。这表明写作先验的注入与 RL 的全局优化之间存在协同效应——持续预训练提供了更丰富的策略空间，而 RL 能够有效探索并优化这一空间。

Figure 2 和 Figure 3 的训练曲线进一步揭示了这一协同效应的动态过程：持续预训练模型在 RL 训练初期即展现出更高的 Writing RM 和 Length RM 分数，且其思考 token 长度始终长于基础模型（Figure 6），暗示更强的先验能力支撑了更深入的规划式推理。

LongWriter-Zero 提出了一套完全由强化学习驱动的超长文本生成训练框架，其核心设计理念在于**不依赖任何人工标注或合成数据**，从零开始通过奖励信号引导模型自发涌现高质量的长文写作能力。整个流水线由四个关键模块串联构成，形成“数据筛选→能力预训练→策略优化→多维评估”的闭环。

### 查询筛选与长度预测

训练提示的质量直接影响 RL 优化的方向。框架首先从 WildChat-1M 和 LMSYS-Chat-1M 两个大规模对话语料库中采样用户请求，随后利用 **QwQ-32B** 模型进行两阶段筛选：第一，仅保留那些真正需要高质量长输出的请求（如论文撰写、商业报告、文学创作等），过滤掉简单问答或短回复场景；第二，对每个保留的查询预测一个合适的目标词数范围 $[L_{\text{lower}}, L_{\text{upper}}]$，为后续长度奖励模型提供动态的、查询自适应的长度约束。这一步骤确保了 RL 训练始终聚焦于“长文本写作”这一核心场景，避免了无关噪声的干扰。

### 持续预训练

在进入 RL 优化之前，框架对基础模型 **Qwen2.5-32B** 进行面向写作能力的持续预训练。该阶段使用约 30B token 的高质量写作语料（涵盖中英文书籍、学术论文、技术报告、文学作品等多个领域），并以 1% 的比例混入从 Base-think 模型中蒸馏得到的长链思维（long CoT）数据。这一设计的双重目的在于：**增强模型的写作先验知识**，使其在 RL 训练的初始阶段就具备基本的文体感知和结构组织能力；同时通过微量 CoT 数据的注入，提前建立对 `<think>/<answer>` 格式的隐式对齐，为后续的思考提示策略奠定基础。消融实验表明，移除持续预训练会导致 WritingBench 平均分从 8.69 降至 8.12、Arena-Write Elo 从 1447 降至 1221，充分验证了该模块对性能上限的关键支撑作用。

### GRPO 强化学习训练

RL 训练采用 **组相对策略优化**（Group Relative Policy Optimization, GRPO）算法。在每个训练步中，从当前策略 $\pi_{\theta_{\text{old}}}$ 采样一组 $G=32$ 条完成结果，计算每条结果相对于组内均值和标准差的归一化优势：

$$A_i = \frac{r_i - \operatorname{mean}(\{r_1, \dots, r_G\})}{\operatorname{std}(\{r_1, \dots, r_G\})}$$

随后通过剪切重要性采样比率来稳定更新：

$$\mathcal{J}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{q \sim P(Q), \{o_i\}_{i=1}^G \sim \pi_{\theta_{\mathrm{old}}}} \left[ \frac{1}{G} \sum_{i=1}^G \min \left( r_i^{\mathrm{ratio}} A_i, \operatorname{clip}(r_i^{\mathrm{ratio}}, 1-\varepsilon, 1+\varepsilon) A_i \right) \right]$$

其中剪切阈值 $\varepsilon=0.2$，KL 惩罚系数 $\beta=0$（即不施加显式的 KL 约束），采样温度 $T=0.8$，最大输出长度设为 14,000 token。训练在 8 个节点（共 64 块 H800 GPU）上基于 Megatron 框架进行，共执行 150 步 RL 优化。

### 复合奖励模型

框架的核心创新之一在于将多个维度的奖励信号融合为统一的优化目标。复合奖励函数由三个独立的奖励模型构成：

- **长度奖励模型（Length RM）**：采用分段线性函数，当输出长度落在 QwQ-32B 预测的目标范围内时给予满分 1；过短则按比例惩罚 $len(o)/L_{\text{lower}}$；过长则线性衰减 $(L_{\text{max}} - len(o))/(L_{\text{max}} - L_{\text{upper}})$。该设计既鼓励模型生成足够长的内容，又防止无限制的长度膨胀。

- **写作质量奖励模型（Writing RM）**：基于人工标注的偏好数据，使用 Qwen2.5-72B 作为骨干网络，通过 Bradley-Terry 偏好优化损失训练：
  $$\mathcal{L} = -\mathbb{E}_{(x, y_w, y_l) \sim D}[\log(\sigma(r_{\text{write}}(x, y_w) - r_{\text{write}}(x, y_l)))]$$
  该模型从整体上评估回答的写作质量，涵盖连贯性、信息密度、修辞水平等全局属性。

- **格式奖励模型（Format RM）**：检查输出是否遵循 `<think>/<answer>` 的结构要求，并检测是否存在明显的重复内容或格式违规，起到抑制奖励黑客行为的作用。

三个奖励信号分别经过组内归一化后直接平均，形成最终优势信号：

$$A_{\text{final}} = \frac{1}{3}(A_{\text{length}} + A_{\text{write}} + A_{\text{format}})$$

### “思考-回答”提示策略

与传统的直接生成（Direct-Answer）方式不同，LongWriter-Zero 采用 **“思考-回答”提示（Think Prompt）**，要求模型先在 `<think>` 标签内进行深度的规划与反思（如构思文章结构、明确各段落要点、检查逻辑一致性），再在 `<answer>` 标签中输出正式内容。这一策略实质上引入了测试时的长链思维（long CoT），使模型能够将全局结构的规划与局部内容的生成解耦。消融实验显示，移除思考提示后 Arena-Write Elo 从 1447 骤降至 668，证明测试时思考对于维持长文本的全局连贯性和结构完整性具有不可替代的作用。

### 评估模块

框架采用多层次的评估体系验证长文本生成质量：**WritingBench** 使用经过 50K 人类标注样本微调的 Qwen2.5-7B 批评模型，从风格、格式和长度三个维度对六个领域（学术工程、金融商业、政治法律、文学艺术、教育、广告营销）的输出进行 1-10 分评分；**Arena-Write** 则通过基于 Elo 的成对比较机制，利用 GPT-4.1 评判器衡量模型在开放式写作任务中的相对优势；此外还引入人工在环的胜率评估，通过交换回答顺序以减轻位置偏差，确保自动评判结果与人类偏好的一致性（批评模型与人类判断达到 83% 一致）。

LongWriter-Zero 的训练流水线由四个核心模块构成：**查询筛选与长度预测**、**持续预训练**、**GRPO 强化学习训练**，以及**复合奖励模型**。各模块协同工作，使模型从零开始涌现超长文本生成能力，无需任何人工标注或合成数据。

### 查询筛选与长度预测

训练提示从 WildChat-1M 和 LMSYS-Chat-1M 中采样，利用 QwQ-32B 进行过滤，仅保留需要高质量长输出的请求。同时，QwQ-32B 为每条查询预测一个合适的目标词数范围 $[L_{\text{lower}}, L_{\text{upper}}]$，作为后续长度奖励的基准。

### 持续预训练

在 RL 训练之前，对 Qwen2.5-32B 基础模型进行 30B token 的持续预训练，语料以高质量写作为主（中英文书籍、报告、学术论文等，数据分布见 Table 2），并以 1% 的比例混入从 Base-think 模型蒸馏的长 CoT 数据。该模块旨在增强模型的写作先验和对思考格式的对齐能力。

### GRPO 强化学习训练

采用组相对策略优化（GRPO）算法，每组采样 $G=32$ 条轨迹，剪切参数 $\varepsilon=0.2$，KL 惩罚系数 $\beta=0$，采样温度 $T=0.8$，最大输出长度 14,000 token。训练在 8 节点（每节点 8×H800 GPU）上进行。

**归一化优势**：对一组完成结果 $\{o_1, \dots, o_G\}$，计算每个样本相对于组内均值和标准差的归一化优势：

$$A_i = \frac{r_i - \operatorname{mean}(\{r_1, \dots, r_G\})}{\operatorname{std}(\{r_1, \dots, r_G\})}$$

**剪切目标**：GRPO 通过剪切重要性采样比率来稳定训练：

$$\mathcal{J}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{q \sim P(Q), \{o_i\}_{i=1}^G \sim \pi_{\theta_{\mathrm{old}}}} \left[ \frac{1}{G} \sum_{i=1}^G \min \left( r_i^{\mathrm{ratio}} A_i, \operatorname{clip}(r_i^{\mathrm{ratio}}, 1-\varepsilon, 1+\varepsilon) A_i \right) - \beta D_{\mathrm{KL}}(\pi_\theta \parallel \pi_{\mathrm{ref}}) \right]$$

其中 $r_i^{\mathrm{ratio}} = \frac{\pi_\theta(o_i|q)}{\pi_{\theta_{\text{old}}}(o_i|q)}$，本工作中 $\beta=0$，即不施加 KL 惩罚。

### 复合奖励模型

复合奖励由三个子奖励模型构成，分别针对长度控制、写作质量和结构格式：

**长度奖励模型（Length RM）**：采用分段线性奖励函数，鼓励输出长度落在 QwQ-32B 预测的目标范围内：

$$r_{\mathrm{length}}(o) = \begin{cases} 1, & \text{if } L_{\mathrm{lower}} \le len(o) \le L_{\mathrm{upper}}, \\ \frac{len(o)}{L_{\mathrm{lower}}}, & \text{if } len(o) < L_{\mathrm{lower}}, \\ \frac{L_{\mathrm{max}} - len(o)}{L_{\mathrm{max}} - L_{\mathrm{upper}}}, & \text{if } len(o) > L_{\mathrm{upper}}. \end{cases}$$

过短按比例惩罚，过长则线性衰减至 $L_{\text{max}}$ 处归零。

**写作质量奖励模型（Writing RM）**：基于人工标注的偏好数据，以 Qwen2.5-72B 为骨干，使用 Bradley-Terry 偏好优化损失训练：

$$\mathcal{L} = -\mathbb{E}_{(x, y_w, y_l) \sim D}[\log(\sigma(r_{\mathrm{write}}(x, y_w) - r_{\mathrm{write}}(x, y_l)))]$$

其中 $y_w$ 和 $y_l$ 分别为同一输入 $x$ 下的好回答与差回答。

**格式奖励模型（Format RM）**：检查输出是否包含正确的 `<think>`/`<answer>` 结构，并检测重复内容以防止奖励黑客行为。

**最终优势**：将三个子奖励分别进行组内归一化后直接平均，作为 RL 训练的最终信号：

$$A_{\mathrm{final}} = \frac{1}{3}(A_{\mathrm{length}} + A_{\mathrm{write}} + A_{\mathrm{format}})$$

### 提示策略

训练与推理阶段采用“思考-回答”提示（Think Prompt），要求模型在 `<think>` 标签内进行深度规划与反思，再在 `<answer>` 标签内输出最终内容。消融实验表明，移除该提示后 Arena-Write Elo 从 1447 骤降至 668，证明测试时思考对全局结构和规划至关重要。

## 实验与关键发现

LongWriter-Zero 的评估围绕两个核心基准展开：**WritingBench**（维度化批评评分，1–10 分）和 **Arena-Write**（基于 Elo 的成对偏好评分）。主实验结果（Table 1）显示，基于 Qwen2.5-32B 的 LongWriter-Zero 在 WritingBench 上取得平均分 **8.69**，在 Arena-Write 上取得 Elo **1447**，均超过所有对比基线，包括 DeepSeek-R1（8.55 / 1343）、Claude-Sonnet-4（8.60 / 1185）、Qwen3-235B-A22B（8.68 / 1343）和 GPT-4o-2024-11-20（8.16 / —）。值得注意的是，这一成绩由一个 32B 参数模型取得，而最强基线 Qwen3-235B 是 235B 参数的 MoE 模型，表明 RL 驱动的训练范式在长文本生成任务上具有显著的参数效率优势。

### 消融实验：持续预训练与测试时思考的关键作用

Table 1 同时报告了两项关键消融结果。移除持续预训练后，WritingBench 平均分从 8.69 降至 **8.12**，Arena-Write Elo 从 1447 降至 **1221**；进一步移除“思考”提示（即使用 Direct-Answer 模式）后，平均分进一步降至 **8.04**，Elo 骤降至 **668**。这一衰减幅度表明，测试时思考（长 CoT）对全局结构和规划能力的贡献甚至超过持续预训练，是 RL 训练发挥上限的必要条件。

训练曲线（Figure 2, Figure 3）进一步揭示了各组件的作用机制。Base-nothink 设置（无思考、无持续预训练）的 RL 训练已能稳定提升 Writing RM 和 Length RM 分数，Arena-Write Elo 从约 200 上升至 600 以上，证明纯 RL 信号即可驱动长文本能力的涌现。引入 Think 提示后（Base-think），Writing RM 分数在初期落后于 Base-nothink，但最终实现反超并达到更高上限，Elo 提升至约 1200。叠加持续预训练后（Continual-Pretrain-think），模型在训练初期即表现出更高的起点和更快的收敛速度，最终 Elo 达到约 1400。Figure 6 显示，持续预训练模型在 RL 过程中始终产生更长的推理链，暗示更强的写作先验使模型更愿意“投入思考”。

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_JWx4DI2N8k/figures/002_Figure_2.jpg]]
*Figure 2: RL Training curves of three setups (Base-nothink, Base-think, and Continual-Pretrain-think) across three metrics: Writing RM (left), Length RM (middle), and Mean Non-Overlong Generation Length (right)*

### RL vs. SFT：训练范式的决定性差异

Figure 4 直接对比了 RL 与 SFT 在 Arena-Write 上的表现。从 Base 初始化出发，SFT 仅将 Elo 从 964 提升至 971，几乎无增益；而 RL 将 Elo 从 964 提升至 1221。从持续预训练初始化出发，SFT 同样几乎无提升（964→971），而 RL 将 Elo 从 1221 推升至 1447。这一对比清晰表明：**RL 能够优化 SFT 无法触及的全局写作属性**，且持续预训练对 RL 的增益远大于对 SFT 的增益——RL 将更强的先验知识有效转化为更优的生成策略，而 SFT 仅能模仿训练分布。

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_JWx4DI2N8k/figures/005_Figure_4.jpg]]
*Figure 4: Arena-Write performance across RL training steps, comparing RL (solid) and SFT (dashed) starting from Base (orange) and Continual Pretrain (blue) initializations*

Table 4 提供了与 LongWriter SFT 基线的直接对比：使用 LongWriter 合成数据训练的 Qwen2.5-32B SFT 模型在 WritingBench 和 Arena-Write 上均显著落后于 LongWriter-Zero-32B，进一步验证了 RL 流程的绝对优势。

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_JWx4DI2N8k/figures/011_Table_4.jpg]]
*Table 4: LongWriter-on-32B SFT baseline. We evaluate Qwen2.5-32B trained with LongWriter synthetic data against our LONGWRITER-ZERO-32B. Our RL pipeline achieves substantial improvements on both WritingBench and ArenaWriter ELO*

### 人类在环评估与跨基准验证

Figure 5 展示了人类在环胜率评估结果。左侧六图由 GPT-4.1 评判，LongWriter-Zero 对阵 Llama-4-Scout、DeepSeek-V3、DeepSeek-R1、Claude-Sonnet-4、Gemini-2.5-Pro 和 Qwen3-235B-A22B 均取得显著胜率优势；右侧两图由人工标注者评判，对阵 DeepSeek-R1 和 Qwen3-235B-A22B 同样确认了优势。评估中交换回答顺序以减轻位置偏差，自动评判与人工评判趋势一致。

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_JWx4DI2N8k/figures/007_Figure_5.jpg]]
*Figure 5: Win-rate results of LongWriter-Zero in human-in-the-loop win-rate evaluation. Left six charts: Outcomes judged by GPT-4.1 against six baselines (Llama-4-Scout, DeepSeek-V3, DeepSeek-R1, Claude-Sonnet-4, Gemini-2.5-Pro, Qwen3-235B-A22B). Right two charts: Outcomes judged by human annotators (comparing against DeepSeek-R1 and Qwen3-235B-A22B). The percentage in the center indicates the overall win rate, with ties counted as 0.5 wins for each side*

在 LongBench-Write（Table 5）上，LongWriter-Zero-32B 在整体质量（$\bar{S}$）、长距离结构（$S_l$）和内容质量（$S_q$）三个维度均取得最佳成绩，进一步验证了其在独立长文本写作任务上的泛化能力。

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_JWx4DI2N8k/figures/012_Table_5.jpg]]
*Table 5: LongBench-Write results. Baseline scores follow Bai et al. (2025). LongWriter-Zero-32B obtains the best overall quality (S¯), long-horizon structure (Sl), and content quality (Sq)*

### 小规模验证

Table 3 报告了 LongWriter-Zero-14B 的结果。即使在 14B 参数规模下，RL 框架仍在 WritingBench 绝对批评分数和 Arena-Write Elo 上带来大幅提升，证明该方法具有良好的可扩展性。

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_JWx4DI2N8k/figures/010_Table_3.jpg]]
*Table 3: LongWriter-Zero-14B achieves strong gains at smaller scale. Even at 14B parameters, our RL framework produces substantial improvements in both absolute critic scores (WritingBench) and pairwise preference evaluations (ArenaWriter ELO)*

### 失败模式与局限

尽管整体表现优异，分析揭示了若干值得关注的失败模式：

1. **奖励黑客风险**：长度奖励的分段线性设计（Eq. 3）可能被模型通过重复生成或关键词堆砌利用。虽然格式奖励模型（Format RM）包含了重复检测模块，但无法完全杜绝此类行为。在 Base-nothink 训练初期，观察到非超长生成的平均长度（Figure 2 右）出现波动，暗示模型在探索奖励边界时存在不稳定性。

2. **自动评判偏差**：WritingBench 使用经 50K 人类标注样本微调的 Qwen2.5-7B 批评模型（与人类判断 83% 一致），Arena-Write 使用 Qwen2.5-72B 和 GPT-4.1 作为评判器。尽管通过人工评估交叉验证，仍不能完全排除模型家族偏差对分数的影响。

3. **计算开销**：RL 训练需 8 节点、64 块 H800 GPU，限制了在资源受限环境中的直接应用。

## 定位与知识库关联

### 1. 训练范式转换：从 SFT 到纯 RL 驱动的长文本生成

LongWriter-Zero 的核心方法论突破在于完全摒弃了传统长文本生成中对监督微调（SFT）和合成数据的依赖。此前的主流方案，如 **LongWriter-8B**（Bai et al., 2025），通过在人工构造的合成长文本数据上进行 SFT 来突破模型的原生长度限制。然而，这一范式面临双重瓶颈：合成数据的构建成本高昂且多样性不足，最大似然目标无法显式优化全局写作属性（如连贯性、格式一致性、主题聚焦度）。LongWriter-Zero 转而采用从零开始的强化学习框架，以 **GRPO**（Group Relative Policy Optimization）算法为核心，仅通过奖励信号引导模型自发涌现超长文本生成能力，无需任何标注或合成数据。

这一转换在方法论层面与 DeepSeek-R1（DeepSeek-AI et al., 2025a）等推理模型的 RL 训练思路形成呼应——两者均依赖 GRPO 和组内归一化优势来稳定策略优化。但 LongWriter-Zero 将 RL 的应用场景从数学推理和代码生成拓展至开放域长文本写作，面临更复杂的奖励设计挑战：写作质量难以通过简单的规则验证来判定，长度控制需要灵活的分段奖励，格式结构要求全局一致性。

### 2. 复合奖励设计：多维度信号融合

LongWriter-Zero 的奖励体系由三个独立模块构成，分别对应长文本生成的三个核心维度：

- **长度奖励模型（Length RM）**：采用分段线性函数，当输出长度落在预测的目标范围内时给予满分奖励，过短按比例惩罚，过长则线性衰减。目标词数范围由 QwQ-32B 对每个查询动态预测，避免了固定长度约束的僵化。

- **写作质量奖励模型（Writing RM）**：基于人工标注的偏好数据，使用 Bradley-Terry 模型在 Qwen2.5-72B 骨干上训练，损失函数为 $\mathcal{L} = -\mathbb{E}_{(x, y_w, y_l) \sim D}[\log(\sigma(r_{\mathrm{write}}(x, y_w) - r_{\mathrm{write}}(x, y_l)))]$。该模型从整体写作质量角度区分优劣回答，弥补了长度和格式奖励无法覆盖的内容质量维度。

- **格式奖励模型（Format RM）**：检查 `<think>/<answer>` 标签结构的完整性和重复内容的抑制，防止模型通过简单堆砌文本来获取长度奖励。

三个奖励信号经组内归一化后直接平均，形成最终优势函数 $A_{\mathrm{final}} = \frac{1}{3}(A_{\mathrm{length}} + A_{\mathrm{write}} + A_{\mathrm{format}})$。这种简单平均策略在实验中表现出良好的稳定性，但论文也明确指出启发式奖励存在被模型利用的风险（如重复生成、关键词堆砌），尽管已加入格式检查和重复检测模块，仍无法完全杜绝奖励黑客行为。

### 3. 测试时思考与持续预训练：RL 效果的关键放大器

LongWriter-Zero 的方法论贡献不仅在于 RL 框架本身，更在于揭示了两项对 RL 效果至关重要的配套技术：

- **“思考-回答”提示（Think Prompt）**：要求模型在 `<think>` 标签内进行深度规划与反思，再输出 `<answer>` 内容。消融实验表明，移除思考提示后，Arena-Write Elo 从 1447 骤降至 668（Table 1），证明测试时思考对于全局结构规划和长程连贯性的关键作用。训练过程中，思考 token 长度随 RL 步数增加而趋于收敛（Figure 6），持续预训练模型始终产生更长的推理链。

- **持续预训练（Continual Pretraining）**：在 30B 高质量写作语料（中英文书籍、报告、学术论文等，分布见 Table 2）上继续训练 Qwen2.5-32B，并以 1% 比例混入蒸馏的自校长 CoT 数据。移除持续预训练后，WritingBench 平均分从 8.69 降至 8.12，Arena-Write Elo 从 1447 降至 1221（Table 1），表明写作先验的增强是 RL 达到高上限的前提。

### 4. 与基线方法的关系定位

LongWriter-Zero 在方法论谱系中占据独特位置：

- **相对于 SFT 方法**（如 LongWriter-8B）：RL 在 Arena-Write 上始终显著优于 SFT。即使从相同的持续预训练初始化出发，RL 能将 Elo 从 1221 提升至 1447，而 SFT 仅从 964 提升至 971（Figure 4），说明 RL 对全局写作属性的优化能力远超 SFT 的局部词级拟合。

- **相对于大型推理模型**（如 DeepSeek-R1）：两者共享 GRPO 训练框架，但 DeepSeek-R1 面向数学推理和代码生成，其奖励主要依赖规则验证；LongWriter-Zero 则面向开放域写作，需要训练专门的写作质量奖励模型来替代简单的规则奖励。

- **相对于大型通用模型**（如 GPT-4o、Claude-Sonnet-4、Qwen3-235B-A22B）：LongWriter-Zero 以 32B 参数量在 WritingBench（8.69 vs. 最高 8.68）和 Arena-Write（1447 vs. 最高 1343）上超越 100B+ 级别的闭源和开源模型，证明了专用 RL 训练在长文本生成任务上的效率优势。

### 5. 适用边界与局限

LongWriter-Zero 的适用边界和局限可从以下几个维度界定：

**适用场景**：独立写作任务（论文、报告、文章等需要全局结构和长程连贯性的生成场景），在 WritingBench 的六个领域（学术与工程、金融与商业、政治与法律、文学与艺术、教育、广告与营销）和三个写作要求（风格、格式、长度）上均表现出色。

**已知局限**：

1. **奖励黑客风险**：启发式奖励（长度、格式）存在被模型利用的可能，尽管已加入格式检查和重复检测模块，但无法完全杜绝。论文明确指出需要设计更不易被利用的奖励模型，如融入事实性检查或对抗训练。

2. **评判器偏差**：自动评判器（Qwen2.5-72B judge、GPT-4.1）的偏好可能引入模型家族偏差。虽经人工评估交叉验证（Figure 5 右二图），仍不能完全替代广泛的人类评审。

3. **领域覆盖不足**：持续预训练数据主要来源于 Common Crawl 等通用语料，在特定专业领域写作（如法律文书、高度技术化报告）中可能存在知识覆盖不足的问题。

4. **规模验证有限**：实验仅在 Qwen2.5-32B 及 14B 版本上验证，未在更大规模（如 70B、100B+）模型上展示 RL 长文生成的可扩展性和行为特性。

5. **计算开销**：RL 训练需要 8 节点共 64 块 H800 GPU，可能限制其在资源受限环境中的应用。

### 6. 开放问题与未来方向

论文提出的开放问题为后续研究指明了方向：

- **奖励模型的鲁棒性**：如何设计更不易被利用的奖励模型，如融入事实性检查、语篇结构评价或对抗训练，以进一步抑制奖励黑客行为？

- **Scaling Law**：在更大规模基础模型上，RL 和持续预训练的组合能否继续带来线性或超线性的写作质量提升？是否存在可预测的 scaling law？

- **任务泛化**：本框架主要针对独立写作任务，能否扩展至交互式、增量式长文本生成（如多轮对话中的长篇输出），以及多模态内容创作？

- **思考长度的自适应控制**：思考（CoT）长度与外推效果之间的关系尚不明确——是否总是越长越好？能否开发自适应长度控制机制，根据任务复杂度动态调整推理深度？

- **偏好数据的高效构建**：如何在不依赖昂贵人工标注的情况下，自动构建高质量、抗黑客的长文本偏好数据集，以训练更鲁棒的写作奖励模型？

## 原文 PDF

![[paperPDFs/ICLR_2026/LongWriter_Zero_Mastering_Ultra_Long_Text_Generation_via_Reinforcement_Learning.pdf]]
