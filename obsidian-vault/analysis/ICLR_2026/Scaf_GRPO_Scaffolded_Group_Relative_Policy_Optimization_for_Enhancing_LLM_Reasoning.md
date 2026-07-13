---
title: "Scaf-GRPO: Scaffolded Group Relative Policy Optimization for Enhancing LLM Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Scaf_GRPO_Scaffolded_Group_Relative_Policy_Optimization_for_Enhancing_LLM_Reasoning.pdf
project_link: null
code_link: null
openreview_forum_id: bOwVr0yr7r
aliases:
- SG
- Scaf-GRPO
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "在训练过程中，当检测到某一问题的所有轨迹均无法获得正确奖励时，通过分层次注入提示（hints）——从抽象知识到具体步骤——引导当前策略生成一条成功轨迹，并以此替换批次中一条失败轨迹，从而恢复奖励方差与非零优势信号，使学习得以继续。"
primary_logic: "Scaf‑GRPO 不改变 GRPO 的损失函数形式，而是将干预定位在数据层面：当出现学习悬崖时，通过条件性地增强批次（用同策略、经由最小提示生成的正确轨迹替换一条失败轨迹）来重建有意义的梯度，保持同策略性质并规避前缀式引导方法的分布不匹配问题。"
claims:
- "在 Qwen2.5‑Math‑7B 模型上，AIME24 的 pass@1 得分从 0.300 提升至 0.433，相对提升 44.3%。"
- "在七个数学基准平均得分上，Scaf‑GRPO（50.9）显著优于 Vanilla GRPO（45.2）和基于前缀的 LUFFY（46.6），相对 LUFFY 增益 9.2%。"
- "消融实验中，移除解法提示（Solution Hint）导致平均性能下降 5.7%（50.9→48.0），证实分层提示的每个层级均不可或缺。"
- "训练动态图显示，Scaf‑GRPO 能够持续解决原本零奖励的问题，而 Vanilla GRPO 在此指标上趋于停滞。"
---

# Scaf-GRPO: Scaffolded Group Relative Policy Optimization for Enhancing LLM Reasoning

> [!tip] 核心洞察
> Scaf‑GRPO 不改变 GRPO 的损失函数形式，而是将干预定位在数据层面：当出现学习悬崖时，通过条件性地增强批次（用同策略、经由最小提示生成的正确轨迹替换一条失败轨迹）来重建有意义的梯度，保持同策略性质并规避前缀式引导方法的分布不匹配问题。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Scaf-GRPO：脚手架式组相对策略优化以增强大语言模型推理能力 |
| 英文题名 | Scaf-GRPO: Scaffolded Group Relative Policy Optimization for Enhancing LLM Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=bOwVr0yr7r) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Scaf‑GRPO |
| Dataset | AIME24, 7‑benchmark Average (Qwen2.5‑Math‑7B), AIME24 (Qwen2.5‑Math‑1.5B) |

> [!tip] 效果简介
> - AIME24 上，pass@1 为 43.3，对比 30.0 (Vanilla GRPO)，变化 +13.3（相对 +44.3%）。
> - 7‑benchmark Average (Qwen2.5‑Math‑7B) 上，pass@1 为 50.9，对比 45.2 (Vanilla GRPO)，变化 +5.7（相对 +12.6%）。
> - 7‑benchmark Average (Qwen2.5‑Math‑7B) 上，pass@1 为 50.9，对比 46.6 (LUFFY)，变化 +4.3（相对 +9.2%）。

## 概要

基于验证器奖励的强化学习（RLVR）已成为提升大语言模型推理能力的有效范式，但其核心算法 GRPO 存在一个根本性瓶颈：当模型面对远超当前能力的问题时，所有探索尝试均以失败告终，获得恒为零的奖励信号。此时，组标准化优势塌缩为零，这些困难问题对策略梯度完全“不可见”，形成**学习悬崖**（learning cliff），使模型无法从最有挑战性的样本中获得提升。

**Scaf‑GRPO**（Scaffolded Group Relative Policy Optimization）针对这一瓶颈提出了一个数据层面的干预方案。其核心洞察是：不改变 GRPO 的损失函数形式，而是在检测到学习悬崖时，通过分层次注入提示（从抽象知识到具体步骤），引导当前策略生成一条成功轨迹，并以此替换批次中的一条失败轨迹。这一条件性批次增强操作恢复了奖励方差与非零优势信号，同时保持了同策略性质，规避了前缀式引导方法（如 **LUFFY**, Yan et al., 2025）的分布不匹配问题。

在 Qwen2.5‑Math‑7B 模型上的实验表明，Scaf‑GRPO 将 AIME24 的 pass@1 得分从 0.300 提升至 0.433，相对提升 44.3%；在七个数学基准的平均得分上，Scaf‑GRPO（50.9）显著优于 Vanilla GRPO（45.2）和 LUFFY（46.6），相对 LUFFY 增益 9.2%。训练动态显示，Scaf‑GRPO 能够持续解决原本零奖励的问题，而 Vanilla GRPO 在此指标上趋于停滞。值得注意的是，引导探索仅对 17.4% 的样本触发，表明方法以最小干预程度实现了大幅性能提升。

消融实验进一步验证了框架各组件的重要性：移除解法提示导致平均性能下降 5.7%，取消指导豁免阶段使性能相对下降 9.2%，证实了分层渐进式提示与前期自主探索的必要性。此外，Scaf‑GRPO 在 Llama‑3.2‑3B‑Instruct 等非 Qwen 架构模型上也展现出跨架构的泛化能力。



### 大语言模型推理能力的强化学习训练

近年来，强化学习（RL）已成为提升大语言模型（LLM）复杂推理能力的核心技术路径。以 GRPO（Group Relative Policy Optimization）为代表的在线策略 RL 方法，通过组内奖励标准化构建优势信号，驱动模型在数学推理、代码生成等任务上取得显著进展。这类方法的核心机制在于：模型对同一问题采样多条轨迹，利用验证器提供的二元奖励计算标准化优势，进而通过裁剪替代目标更新策略。

### 学习悬崖：GRPO 训练中的关键瓶颈

然而，当模型面对远超其当前能力的困难问题时，GRPO 的训练过程会遭遇一个结构性障碍——**学习悬崖（learning cliff）**。具体而言，若模型对某一问题的所有探索尝试均无法获得正确奖励（即批次内所有轨迹的奖励恒为零），组标准化的优势值将塌缩为零：

$$\hat{A}_i = \frac{R(o_i) - \mu_{\mathcal{G}}}{\sigma_{\mathcal{G}} + \epsilon_{\mathrm{std}}} = 0$$

此时，策略梯度完全消失，这些最具挑战性的样本对模型更新“不可见”，导致模型无法从能力边界处获得任何学习信号。训练动态数据显示，Vanilla GRPO 在零奖励问题的解决数量上趋于停滞，验证准确率增长也随之饱和（Figure 2）。

### 现有缓解方案的局限性

针对这一问题，学界提出了若干缓解策略，但各有其固有缺陷：

- **DAPO**（Yu et al., 2025）通过动态采样直接丢弃困难样本，虽避免了梯度消失，但放弃了最有价值的学习机会，本质上是一种规避而非解决。
- **LUFFY**（Yan et al., 2025）等基于前缀的离线策略引导方法，在问题前缀中注入提示以增加成功概率，但引入了分布不匹配问题——引导轨迹来自不同于当前策略的分布，破坏了 GRPO 的在线策略性质，导致训练不稳定（Figure 7 中 clip ratio 剧烈波动即为其表征）。

上述方法或牺牲困难样本，或损害训练稳定性，未能从根本上解决学习悬崖问题。

### 本文动机：最小化、同策略的脚手架式干预

本文的核心动机在于回答一个根本性问题：**能否在不改变 GRPO 损失函数、不破坏在线策略性质的前提下，为模型提供恰好足够的引导，使其跨越学习悬崖？**

Scaf‑GRPO 的设计哲学由此出发——将干预严格限定在数据层面：仅在检测到学习悬崖时，通过分层次注入提示（从抽象知识到具体步骤）引导当前策略生成一条成功轨迹，并以此替换批次中一条失败轨迹。这一设计确保：
1. **最小干预**：提示仅对约 17.4% 的样本触发，且采用增量注入策略，仅提供恰好够用的信息量；
2. **同策略保持**：引导轨迹由当前策略采样，概率比计算与标准 GRPO 一致，训练稳定性得以维持；
3. **梯度恢复**：增强后的批次包含非零奖励，优势信号得以重建，学习过程持续推进。

在 Qwen2.5‑Math‑7B 模型上，Scaf‑GRPO 将 AIME24 的 pass@1 得分从 0.300 提升至 0.433，相对提升 44.3%；在七个数学基准上的平均得分（50.9）显著优于 Vanilla GRPO（45.2）和 LUFFY（46.6），相对 LUFFY 增益 9.2%（Table 1）。



## 核心方法与创新机理

### 问题诊断：GRPO 中的“学习悬崖”

在基于验证器奖励的强化学习（RLVR）训练中，当模型面对远超当前能力的问题时，所有采样轨迹均无法获得正确奖励，导致 GRPO 的组标准化优势（advantage）塌缩为零。此时，这些困难问题对策略梯度完全“不可见”，模型无法从中获得任何学习信号，形成**学习悬崖**（learning cliff）——这是 Scaf‑GRPO 所要解决的核心瓶颈。

### 关键干预：条件性批次增强

Scaf‑GRPO 的核心创新在于**不改变 GRPO 的损失函数形式**，而是将干预定位在数据层面。当检测到某一问题的所有轨迹奖励均为零时，框架通过分层提示（hints）引导当前策略生成一条成功轨迹，并用其替换批次中的一条失败轨迹。这一操作恢复了奖励方差与非零优势信号，使学习得以继续。

该设计的因果机制可概括为：

1. **检测**：当批次 $\\mathcal{G}$ 中所有轨迹的奖励 $R(o_i) = 0$ 时，触发干预。
2. **引导探索**：按“知识提示→规划提示→解法提示”的层次，逐步注入最小化的增量提示，直到模型输出正确解。
3. **批次增强**：将引导得到的成功轨迹 $o_h^*$ 替换一条失败轨迹，形成增强批次 $\\mathcal{G}_{\\text{final}}$。
4. **统一优化**：在增强批次上直接应用标准 GRPO 裁剪替代目标，损失函数形式上完全等价：

$$J_{\\mathrm{Scaf-GRPO}}(\\theta) = \\hat{\\mathbb{E}}_{i,t} \\left[ \\min\\left( r'_{i,t}(\\theta) \\hat{A}'_i, \\mathrm{clip}(r'_{i,t}(\\theta), 1-\\epsilon, 1+\\epsilon) \\hat{A}'_i \\right) \\right]$$

其中 $\\hat{A}'_i$ 和 $r'_{i,t}$ 基于增强批次计算；当批次中至少存在一条成功轨迹时，Scaf‑GRPO 与标准 GRPO 完全等价：$J_{\\mathrm{Scaf-GRPO}}(\\theta) \\equiv J_{\\mathrm{GRPO}}(\\theta)$。

### Changed Slot：零奖励批次的构建方式

| 维度 | 基线方法（Vanilla GRPO） | Scaf‑GRPO |
|------|------------------------|-----------|
| 零奖励批次处理 | 所有轨迹奖励为零，优势计算全部为零，梯度丢失 | 检测到学习悬崖后，通过分层提示探索找到一条由当前策略生成的正确轨迹，替换一条失败轨迹，恢复梯度信号 |
| 数据来源 | 仅使用原始采样轨迹 | 增强批次中包含一条经由最小提示生成的同策略成功轨迹 |
| 损失函数 | 标准 GRPO 裁剪目标 | 形式完全相同，但应用于增强后的批次 |

### 保持同策略性质的关键设计

与基于前缀的离线策略引导方法（如 **LUFFY**，Yan et al., 2025）不同，Scaf‑GRPO 的引导轨迹 $o_h^*$ 直接从当前策略 $\\pi_\\theta$ 采样，概率比计算遵循标准同策略形式：

$$r'_{i,t}(\\theta) = \\begin{cases} \\frac{\\pi_{\\theta}(o'_{i,t} | o'_{i,<t}, q)}{\\pi_{\\theta_{\\mathrm{old}}}(o'_{i,t} | o'_{i,<t}, q)} & \\text{if } o'_i \\neq o^*_h \\\\ \\frac{\\pi_{\\theta}(o'_{i,t} | o'_{i,<t}, q \\oplus h^*)}{\\pi_{\\theta_{\\mathrm{old}}}(o'_{i,t} | o'_{i,<t}, q \\oplus h^*)} & \\text{if } o'_i = o^*_h \\end{cases}$$

这规避了离线策略方法中因分布不匹配导致的训练不稳定问题。实验证据（Figure 7）显示，Scaf‑GRPO 的 clip ratio 保持低且稳定，而离线策略替代方案波动剧烈。

### 配套创新：指导豁免阶段与分层提示

- **指导豁免阶段**（Phase 1）：前 15% 训练步不提供任何提示，让模型自主探索，以区分真正的能力缺口与格式错误等导致的“伪困难”问题。消融实验表明，取消该阶段使性能相对全框架下降 9.2%（Table 10）。
- **分层提示结构**：三层级提示（知识 $\\rightarrow$ 规划 $\\rightarrow$ 解法）按抽象程度递进，保证以最少的干预重建学习信号。一次性提供全部提示（非增量）导致性能下降 6.3%（Table 2），验证了最小化、逐步介入的必要性。

### 干预程度

Scaf‑GRPO 的引导探索仅对 **17.4%** 的样本触发，表明其以最小干预程度实现大幅性能提升——在 Qwen2.5‑Math‑7B 上，AIME24 的 pass@1 从 0.300 提升至 0.433（相对提升 44.3%），七个数学基准平均分从 45.2 提升至 50.9（相对提升 12.6%）。



![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_bOwVr0yr7r/figures/004_Figure_3.jpg]]
*Figure 3: Overview of the Scaf-GRPO framework. For a given query, the model generates multiple solutions. (Left) If any solution is correct, standard GRPO proceeds. (Right) If all solutions fail (the learning cliff), Scaf-GRPO initiates hierarchical hint-guided exploration. It injects progressively concrete in-prompt hints until a correct solution is found. This successful, minimally-guided trajectory replaces a failed one, restoring the learning gradient and enabling on-policy updates to resume*

Scaf‑GRPO 的核心理念是**不修改 GRPO 的损失函数**，而是将干预定位在**数据层面**：当检测到“学习悬崖”（learning cliff）时，通过条件性地增强训练批次来重建有意义的梯度信号。

### 问题诊断：学习悬崖

在标准的 GRPO 训练中，对于一批问题，模型每条轨迹获得的奖励通过组内标准化计算优势（advantage）：

$$\hat{A}_i = \frac{R(o_i) - \mu_{\mathcal{G}}}{\sigma_{\mathcal{G}} + \epsilon_{\mathrm{std}}}$$

当某个问题对当前模型而言过于困难时，所有 $N$ 条探索轨迹均无法得到正确奖励（$R(o_i)=0, \forall i$），此时组内均值 $\mu_{\mathcal{G}}=0$、标准差 $\sigma_{\mathcal{G}}=0$，导致所有轨迹的优势 $\hat{A}_i$ 塌缩为零。这意味着该问题对策略梯度**完全不可见**，模型无法从这些最具挑战性的样本中学习——这就是学习悬崖。

### 两阶段框架

Scaf‑GRPO 通过两个阶段来解决这一问题：

**Phase 1：指导豁免阶段（Guidance Exemption Period）**  
在训练的前 15% 步中，框架不提供任何提示，让模型完全自主探索。这一阶段的目的是将“伪困难问题”（模型有能力解决但尚未充分训练的问题）与“真困难问题”（真正超出当前能力的问题）区分开，避免过早产生提示依赖。消融实验表明，取消此阶段会使平均性能相对全框架下降 9.2%（Table 10），而 15% 的时长在所有候选比例中取得最优平衡（Table 11）。

**Phase 2：分层提示引导探索（Hierarchical Hint‑Guided Exploration）**  
当检测到某一问题的所有轨迹均失败（学习悬崖）时，框架启动分层提示机制。提示按抽象层级分为三层：
- **知识提示（Knowledge Hint）**：提供解题所需的核心概念或定理
- **规划提示（Planning Hint）**：给出解题步骤的高层规划
- **解法提示（Solution Hint）**：提供具体的解题步骤

引导探索按“知识→规划→解法”的顺序逐步注入提示，每注入一层后由**当前策略**重新采样一条轨迹。一旦模型生成正确解，探索立即停止——这保证了每次干预都是**最小化、增量式**的。

### 批次增强与统一损失

引导得到的成功轨迹 $o_h^*$ 替换批次中的一条失败轨迹，形成增强批次 $\mathcal{G}_{\mathrm{final}}$。基于此批次重新计算标准化优势 $\hat{A}'_i$，并应用标准 GRPO 的裁剪替代目标：

$$J_{\mathrm{Scaf-GRPO}}(\theta) = \hat{\mathbb{E}}_{i,t} \left[ \min\left( r'_{i,t}(\theta) \hat{A}'_i, \mathrm{clip}(r'_{i,t}(\theta), 1-\epsilon, 1+\epsilon) \hat{A}'_i \right) \right]$$

关键设计在于概率比 $r'_{i,t}(\theta)$ 的处理：对于引导轨迹，其概率比是基于**同一增强提示**下的新旧策略概率计算，而非与无提示轨迹混用。这保证了增强批次的**同策略（on‑policy）性质**，避免了前缀式引导方法（如 LUFFY）因分布不匹配导致的训练不稳定（Figure 7 显示 Scaf‑GRPO 的 clip ratio 保持低且稳定，而 off‑policy 替代方案波动剧烈）。

当批次中已存在至少一条成功轨迹时，Scaf‑GRPO 不进行任何干预，此时：

$$J_{\mathrm{Scaf-GRPO}}(\theta) \equiv J_{\mathrm{GRPO}}(\theta)$$

即框架与标准 GRPO 完全等价。统计表明，引导探索仅对 **17.4%** 的样本触发，体现了“最小干预”的设计原则。

### 数据预处理管线

在训练之前，框架还包含两个离线准备模块：

1. **动态数据筛选**：根据模型初始能力（8 次采样）将训练问题分为三类——太简单问题（丢弃）、可解问题（50% 子采样保留）、困难问题（全部保留），构造聚焦模型能力前沿的训练集。消融表明，此筛选将 Scaf‑GRPO 的平均分从 46.2 提升至 50.9（Table 12）。

2. **提示离线生成**：利用 DeepSeek‑R1 模型，结合真值答案的解题步骤，预先生成三层级提示，供训练中即时注入。提示质量直接影响最终效果：使用 DeepSeek‑R1 生成的提示比 Qwen2.5‑72B‑Instruct 生成的提示带来更高性能（50.9 vs 49.0，Table 14）。



Scaf‑GRPO 的核心设计在于**不改变 GRPO 的损失函数形式**，而是将干预定位在数据层面：当检测到学习悬崖时，通过条件性地增强批次来重建有意义的梯度信号。以下逐一拆解其关键模块与公式。

### 1. 学习悬崖的检测与介入触发

在标准 GRPO 中，对于每个问题 $q$，模型从当前策略 $\pi_\theta$ 采样 $N$ 条轨迹构成组 $\mathcal{G} = \{o_1, o_2, \dots, o_N\}$。每条轨迹的奖励 $R(o_i)$ 由基于规则的验证器给出——数学推理场景中通常为 0（错误）或 1（正确）。组内标准化优势为：

$$\hat{A}_i = \frac{R(o_i) - \mu_{\mathcal{G}}}{\sigma_{\mathcal{G}} + \epsilon_{\mathrm{std}}}$$

当 $\mathcal{G}$ 中所有轨迹均失败时（$R(o_i) = 0, \forall i$），有 $\mu_{\mathcal{G}} = 0$ 且 $\sigma_{\mathcal{G}} = 0$，导致 $\hat{A}_i = 0$，策略梯度完全消失。这些困难问题对优化过程“不可见”，形成学习悬崖。

Scaf‑GRPO 的介入条件即为此：**当且仅当 $\forall o_i \in \mathcal{G}, R(o_i) = 0$ 时**，触发分层提示引导探索；否则，框架与标准 GRPO 完全等价，不产生任何额外干预。

### 2. 分层提示引导探索

当学习悬崖被检测到后，Scaf‑GRPO 启动分层提示引导探索。系统预先为每个问题生成三层级提示 $\mathcal{H} = \{H_{\text{knowledge}}, H_{\text{planning}}, H_{\text{solution}}\}$：

- **知识提示（$H_{\text{knowledge}}$）**：提供解题所需的关键概念、定理或公式，不涉及具体步骤。
- **规划提示（$H_{\text{planning}}$）**：给出解题的高层路线图，但不展开计算细节。
- **解法提示（$H_{\text{solution}}$）**：提供完整的解题步骤。

引导探索按**增量最小化**原则进行：首先仅注入 $H_{\text{knowledge}}$，让当前策略 $\pi_\theta$ 重新生成一条轨迹；若仍失败，则追加 $H_{\text{planning}}$ 再次尝试；若依然失败，最终注入 $H_{\text{solution}}$。一旦生成正确轨迹 $o_h^*$，立即停止注入，确保使用最抽象、最少的干预重建学习信号。

### 3. 批次增强与统一 GRPO 损失

引导得到的成功轨迹 $o_h^*$ 替换原批次中的一条随机失败轨迹，构成增强批次：

$$\mathcal{G}_{\text{final}} = \{o_1', o_2', \dots, o_N'\}$$

其中 $o_i'$ 为原始失败轨迹或替换后的引导轨迹。基于 $\mathcal{G}_{\text{final}}$ 重新计算标准化优势：

$$\hat{A}_i' = \frac{R(o_i') - \mu_{\mathcal{G}_{\text{final}}}}{\sigma_{\mathcal{G}_{\text{final}}} + \epsilon_{\mathrm{std}}}$$

由于 $\mathcal{G}_{\text{final}}$ 中至少包含一条奖励为 1 的轨迹，$\sigma_{\mathcal{G}_{\text{final}}} > 0$，优势信号得以恢复。

Scaf‑GRPO 的策略更新直接应用标准 GRPO 的裁剪替代目标，但作用于增强后的批次：

$$J_{\mathrm{Scaf\text{-}GRPO}}(\theta) = \hat{\mathbb{E}}_{i,t} \left[ \min\left( r_{i,t}'(\theta) \hat{A}_i', \mathrm{clip}(r_{i,t}'(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_i' \right) \right]$$

其中概率比 $r_{i,t}'(\theta)$ 根据轨迹来源区分计算：

$$r_{i,t}'(\theta) = \begin{cases} \dfrac{\pi_{\theta}(o_{i,t}' \mid o_{i,<t}', q)}{\pi_{\theta_{\mathrm{old}}}(o_{i,t}' \mid o_{i,<t}', q)} & \text{if } o_i' \neq o_h^* \\[8pt] \dfrac{\pi_{\theta}(o_{i,t}' \mid o_{i,<t}', q \oplus h^*)}{\pi_{\theta_{\mathrm{old}}}(o_{i,t}' \mid o_{i,<t}', q \oplus h^*)} & \text{if } o_i' = o_h^* \end{cases}$$

- 对于原始失败轨迹，概率比基于原始问题 $q$ 计算，与标准 GRPO 一致。
- 对于引导成功轨迹 $o_h^*$，概率比基于增强提示 $q \oplus h^*$（$h^*$ 为触发成功的最小提示）计算，且当前策略与旧策略使用**同一增强提示**，保证了同策略性质。

### 4. 与标准 GRPO 的等价性

当批次中至少存在一条成功轨迹时，$\mathcal{G}_{\text{final}} = \mathcal{G}$，无任何替换发生，此时：

$$J_{\mathrm{Scaf\text{-}GRPO}}(\theta) \equiv J_{\mathrm{GRPO}}(\theta)$$

这一性质确保了 Scaf‑GRPO 对正常学习过程零干扰，干预仅精确作用于学习悬崖场景。训练动态图（Figure 2）验证了这一机制的有效性：Scaf‑GRPO 能够持续解决原本零奖励的问题，而 Vanilla GRPO 在此指标上趋于停滞。

### 5. 指导豁免阶段

为避免模型过早产生提示依赖，Scaf‑GRPO 在前 15% 训练步中不提供任何提示（指导豁免阶段），让模型自主探索。此阶段用于区分真正的能力缺口（true‑hard）与因格式错误或初始探索不足导致的伪困难问题（pseudo‑hard）。消融实验证实，取消该阶段使性能相对全框架下降 9.2%。



## 实验与关键发现

### 核心瓶颈与训练动态

本工作的出发点是一个在基于验证器奖励的强化学习（RLVR）中被普遍忽视的现象：**学习悬崖**（learning cliff）。当模型面对远超其当前能力的问题时，所有 $N$ 条采样轨迹均无法获得正确奖励（奖励恒为零）。在标准 GRPO 的组标准化优势计算中：

$$\hat{A}_i = \frac{R(o_i) - \mu_{\mathcal{G}}}{\sigma_{\mathcal{G}} + \epsilon_{\mathrm{std}}}$$

当 $\mu_{\mathcal{G}} = \sigma_{\mathcal{G}} = 0$ 时，所有轨迹的优势 $\hat{A}_i$ 全部塌缩为零，策略梯度完全消失。这意味着这些最具挑战性的样本对模型训练完全“不可见”，模型无法从它们身上获取任何学习信号。

**Figure 2** 清晰地展示了这一现象的严重性：在 Qwen2.5-Math-1.5B 的训练过程中，Vanilla GRPO 面临的零奖励问题数量始终维持在高位且趋于停滞，而 Scaf-GRPO 则能够持续地将零奖励问题转化为可解问题（Figure 2a）。这一差异直接反映在验证准确率上——Scaf-GRPO 在整个训练周期内保持持续且显著的提升，而 Vanilla GRPO 则陷入平台期（Figure 2b）。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_bOwVr0yr7r/figures/003_Figure_2.jpg]]
*Figure 2: Training dynamics of Qwen2.5-Math-1.5B. (a) Scaf-GRPO overcomes the learning cliff by continuously solving zero-reward problems where vanilla GRPO plateaus. (b) This translates to sustained and superior validation accuracy for Scaf-GRPO throughout training*

### 主要结果

**Table 1** 报告了在七个数学基准上的综合对比结果。核心发现如下：

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_bOwVr0yr7r/figures/006_Table_1.jpg]]
*Table 1: Overall performance on seven benchmarks. We compare our method, SCAF-GRPO, against vanilla GRPO baselines across diverse architectures, including the Qwen2.5 series, a non-Qwen model (Llama-3.2-8B-Instruct), and a specialized long-CoT model (DeepSeek-R1-Distill-Qwen-1.5B). Scores: pass@1 (%). Best results are in bold. The background color of Scaf-GRPO cells indicates performance change vs. Vanilla GRPO (green for improvement, red for decline)*

**Qwen2.5-Math-7B 上的性能：**
- Scaf-GRPO 在 AIME24 上取得 **43.3%** 的 pass@1 得分，相较 Vanilla GRPO 的 30.0% 提升 **13.3 个百分点**，相对提升 **44.3%**。
- 在七个基准的平均得分上，Scaf-GRPO 达到 **50.9**，显著优于 Vanilla GRPO（45.2）和基于前缀的引导方法 LUFFY（46.6），相对 LUFFY 增益 **9.2%**。
- 相较于 SimpleRL-Zero（48.7）和 Oat-Zero（48.3）等先进 GRPO 实现，Scaf-GRPO 同样保持领先。

**跨模型架构的泛化性：**
- 在 Qwen2.5-Math-1.5B 上，Scaf-GRPO 将 AIME24 得分从 13.3% 提升至 **20.0%**，七基准平均从 37.6 提升至 **41.5**。
- 在非 Qwen 架构的 Llama-3.2-3B-Instruct 上，Scaf-GRPO 将平均得分从 26.1 提升至 **28.8**，验证了方法的架构无关性。
- 在专门的长思维链模型 DeepSeek-R1-Distill-Qwen-1.5B 上，Scaf-GRPO 将 AIME24 从 28.9 进一步提升至 **33.3**，证明该方法可与已有的推理增强模型叠加使用。

**Table 3** 进一步表明，在经过动态筛选的更难数据子集上，Scaf-GRPO 的优势更为突出：Qwen2.5-Math-7B 的平均得分进一步提升至 **51.3**，而 Vanilla GRPO 在相同数据上仅为 46.9。这证实了 Scaf-GRPO 的核心价值恰恰体现在对困难问题的处理上。

### 消融实验

**Table 2** 对 Scaf-GRPO 的关键设计要素进行了系统性消融，所有实验基于 Qwen2.5-Math-7B：

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_bOwVr0yr7r/figures/007_Table_2.jpg]]
*Table 2: Ablation study on Scaf-GRPO’s key components using Qwen2.5-Math-7B model. The best performance is highlighted in bold. The “No Guidance” row serves as the vanilla GRPO baseline*

**分层提示的必要性：**
- 完整的三层级提示（K→P→S）取得最优平均分 **50.9**。
- 移除解法提示（K→P 变体）导致平均分降至 48.0，下降 **5.7%**，是所有单项消融中退化最严重的，表明具体解题步骤的引导对克服学习悬崖至关重要。
- 仅保留解法提示（S-only 变体）得分为 49.0，下降 3.7%，说明抽象层级的提示同样不可或缺。
- 移除知识提示或规划提示分别导致 3.3% 和 2.9% 的性能下降。

**增量提示 vs. 一次性提示：**
- 一次性提供全部提示（w/o Incremental Chunking）导致平均分从 50.9 暴跌至 47.7，下降 **6.3%**。这强有力地验证了 Scaf-GRPO 的核心设计原则：以最小化、逐步介入的方式提供引导，避免信息过载和分布不匹配。

**指导豁免阶段：**
- **Table 10** 显示，取消 Phase 1（指导豁免阶段）使性能从 50.9 降至 46.2，相对下降 **9.2%**。这表明前期的自主探索对于区分“真困难”问题和“伪困难”问题、避免模型过早产生提示依赖具有决定性作用。
- **Table 11** 对豁免时长的消融表明，15% 的训练步数是最优选择：0% 豁免（全程引导）仅得 46.2，100% 豁免（无引导）即为 Vanilla GRPO 的 45.2，而 15% 的设置实现了最佳的自主探索与引导干预平衡。

**数据筛选策略：**
- **Table 12** 的消融显示，动态数据筛选对 Scaf-GRPO 的性能至关重要。使用完整数据集时平均分为 46.2；去除“太简单”问题后提升至 48.8；进一步对“可解”问题进行 50% 子采样后达到最优的 **50.9**。该策略将训练集聚焦于模型的能力前沿，最大化学习悬崖的暴露频率，从而充分发挥 Scaf-GRPO 的引导机制。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_bOwVr0yr7r/figures/019_Table_12.jpg]]
*Table 12: Ablation study on dataset filtering strategies. We compare the Scaf-GRPO performance under different dataset settings. The selected configuration is highlighted*

**提示质量的影响：**
- **Table 14** 对比了不同提示生成源的效果：使用 DeepSeek-R1 生成的提示（50.9）显著优于使用 Qwen2.5-72B-Instruct 生成的提示（49.0），提示质量与最终模型性能呈正相关。

### 引导效率与“毕业”现象

Scaf-GRPO 的高效性体现在其引导机制的稀疏触发上：在整个训练过程中，分层提示引导探索仅对 **17.4%** 的样本被触发（Section 4.4）。这意味着模型在绝大多数情况下仍进行自主探索，仅在真正遇到学习悬崖时才获得最小化的外部支架。

**Table 4** 统计了不同模型骨架下的“毕业”问题数量——即训练初期模型完全无法解决、但在 Scaf-GRPO 训练后变为可解的问题。在 Qwen2.5-Math-1.5B 上，Scaf-GRPO 相较 Vanilla GRPO 实现了 **+137.8%** 的毕业问题相对增长，直观地量化了该方法将“不可见”样本转化为有效学习信号的能力。

**Figure 5** 通过具体案例展示了模型从模仿到自主的推理能力演化：模型首先模仿具体的解法提示（a），随后仅需抽象的知识提示即可解题（b），最终完全自主地解决问题（c），表明引导支架成功地被内化而非形成依赖。

### 训练效率与分布外泛化

**Table 5** 显示，Scaf-GRPO 的训练效率与 Vanilla GRPO 相当甚至更优：在 Qwen2.5-Math-7B 上，Scaf-GRPO 达到最优 checkpoint（50.9%）仅需约 12 小时，而 Vanilla GRPO 达到其最优（45.2%）需约 13 小时。显存开销两者基本持平（~73 GB vs ~72 GB），表明批次增强策略引入的计算开销极小。

**Table 6** 考察了在 GPQA-Diamond 科学推理基准上的分布外泛化能力。Scaf-GRPO 在 Qwen2.5-Math-7B 上取得 **37.3%**，与 LUFFY 持平，显著优于 Vanilla GRPO（33.3%）和未训练的基模型（24.7%），表明通过支架引导获得的推理能力具有一定的跨领域迁移性。

### 同策略设计的关键性

**Table 9** 与 **Figure 7** 共同验证了 Scaf-GRPO 坚持同策略（on-policy）设计的关键性。若将引导轨迹替换为离线策略数据（Off-Policy 替代方案），虽然也能恢复梯度信号，但会导致训练稳定性严重恶化：clip ratio 剧烈波动且频繁触发裁剪（Figure 7 蓝线），最终性能全面落后于 Scaf-GRPO（Table 9）。Scaf-GRPO 通过从当前策略 $\pi_\theta$ 采样引导轨迹，保持了低且稳定的 clip ratio（Figure 7 红线），确保了策略更新的平稳性。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_bOwVr0yr7r/figures/015_Figure_7.jpg]]
*Figure 7: Comparison of the clip ratio during training. The proposed Scaf-GRPO (red) maintains a low and stable clip ratio, indicating effective on-policy learning. The off-policy alternative (blue) exhibits high volatility and frequent clipping, indicative of distributional mismatch and training instability*

### 公平性说明

所有自训练方法（Vanilla GRPO、LUFFY、Scaf-GRPO）均使用相同的数据集、训练轮数、框架（veRL）和关键超参数（KL 惩罚为零，rollout 数 $N=8$ 等）以保证对比公平。SimpleRL-Zero 和 Oat-Zero 直接采用其官方发布的模型权重进行评测，作为外部参考。LUFFY 使用其原论文的超参数在本文数据上重新训练，排除数据差异的影响。评估统一采用贪心解码 pass@1 度量，避免了后处理对结果的影响。



## 定位与知识库关联

### 与现有方法的继承与分化

Scaf‑GRPO 建立在 **GRPO**（Shao et al., 2024）的在线策略强化学习框架之上，完全保留了其裁剪替代目标函数的形式：

$$J_{\mathrm{GRPO}}(\theta) = \hat{\mathbb{E}}_{i,t} \left[ \min \left( r_{i,t}(\theta) \hat{A}_i, \mathrm{clip}(r_{i,t}(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_i \right) \right]$$

Scaf‑GRPO 的损失函数在数学形式上与 GRPO 完全相同，差异仅在于当检测到学习悬崖时，优势 $\hat{A}'_i$ 与概率比 $r'_{i,t}(\theta)$ 是作用在增强后的批次 $\mathcal{G}_{\mathrm{final}}$ 上计算，而非原始批次。当批次中至少存在一条成功轨迹时，两者严格等价：$J_{\mathrm{Scaf-GRPO}}(\theta) \equiv J_{\mathrm{GRPO}}(\theta)$。

这一设计使 Scaf‑GRPO 与以下同类方法形成了清晰的分化路径：

- **LUFFY**（Yan et al., 2025）：采用基于前缀的离线策略引导，在输入中预先注入固定引导文本。其根本问题在于引导轨迹来自不同的输入分布，破坏了 GRPO 的在线策略性质，导致训练不稳定。Scaf‑GRPO 的引导轨迹始终由当前策略 $\pi_\theta$ 在同一次推理中采样生成，仅输入侧附加了提示，从而保持了在线策略更新的一致性。实验表明，Scaf‑GRPO 在七个基准上的平均 pass@1 相对 LUFFY 提升 9.2%。

- **DAPO**（Yu et al., 2025）：通过动态采样丢弃困难样本来缓解梯度消失，本质上是在回避学习悬崖而非克服它。Scaf‑GRPO 则通过注入最小化提示将零奖励信号转化为有效学习信号，使模型持续从最困难的问题中获益。直接对比中，Scaf‑GRPO 在所有基准上均优于 DAPO。

- **SimpleRL‑Zero**（Zeng et al., 2025）与 **Oat‑Zero**（Liu et al., 2025a）：两者均为 GRPO 的优化实现，未引入外部引导机制。Scaf‑GRPO 在与其对比时，Qwen2.5‑Math‑7B 模型上的平均 pass@1 达到 50.9，显著优于 SimpleRL‑Zero（46.2）和 Oat‑Zero（48.2），证实了引导机制的增益独立于 GRPO 实现的工程优化。

### 适用边界与前提条件

Scaf‑GRPO 的有效性依赖以下前提：

1. **高质量提示的可用性**：三层级提示（知识→规划→解法）由 DeepSeek‑R1 模型依据真值答案生成。消融实验表明，使用 Qwen2.5‑72B‑Instruct 生成的较低质量提示会使平均性能从 50.9 降至 49.0，提示质量与最终效果呈正相关。

2. **合理的初始能力基线**：动态数据筛选依赖模型初始能力（8 次采样）来划分问题难度。若模型初始能力过弱，几乎所有问题均被归为“困难”，可能触发过频的引导探索，增加计算开销。

3. **数学推理领域的验证**：当前所有实验均在数学推理基准上完成。在 GPQA‑Diamond 科学推理基准上，Scaf‑GRPO 虽取得 37.3% 的 pass@1（与 LUFFY 持平，优于 Vanilla GRPO 的 30.7%），但该领域尚未经过系统消融验证。

### 局限与已知失效模式

1. **提示生成的外部依赖**：当前框架依赖高性能教师模型（DeepSeek‑R1）预先生成提示，无法在训练中自适应调整提示内容与粒度。若提示包含错误信息，框架缺乏验证机制，可能误导模型学习。

2. **最坏情况下的计算开销**：分层探索在最坏情况下需依次尝试知识提示、规划提示和解法提示，每次均需一次完整的模型推理。尽管实际触发率仅 17.4%，但对于极端困难的问题集，此开销可能显著增加。

3. **指导豁免阶段的固定比例**：当前将前 15% 训练步设为无引导阶段，以区分“真困难”与“伪困难”问题。取消此阶段会导致性能相对全框架下降 9.2%，但固定比例可能不适用于所有模型与数据分布。消融显示 15% 为最优，但自适应调度机制尚未实现。

4. **一次性提供全部提示的失效**：消融中“非增量式全提示”变体导致性能下降 6.3%，验证了最小化、逐步介入的必要性。这意味着若提示结构设计不当（如粒度过粗），框架可能退化为低效的模仿学习。

### 开放问题

- 如何实现提示的自动生成与自适应调整，使框架摆脱对高性能教师模型的依赖？
- 能否设计一种机制，根据模型当前能力动态调整提示的具体层级和粒度，实现完全自适应的支架？
- Scaf‑GRPO 是否能够扩展到强化学习以外的训练范式中（例如直接偏好优化 DPO）？
- 在多模态推理或其他复杂推理任务（如定理证明）中，分层提示应如何构造？
- 是否可以通过课程学习自动调度提示强度，而不是固定比例的指导豁免？
- 在更大规模模型（>70B）和更多样化的任务上，Scaf‑GRPO 的表现是否会持续保持优势？



## 原文 PDF

![[paperPDFs/ICLR_2026/Scaf_GRPO_Scaffolded_Group_Relative_Policy_Optimization_for_Enhancing_LLM_Reasoning.pdf]]
