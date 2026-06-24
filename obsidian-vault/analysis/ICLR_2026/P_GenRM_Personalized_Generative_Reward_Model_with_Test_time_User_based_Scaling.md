---
title: "P-GenRM: Personalized Generative Reward Model with Test-time User-based Scaling"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/P_GenRM_Personalized_Generative_Reward_Model_with_Test_time_User_based_Scaling.pdf
openreview_forum_id: hXNApWLBZG
aliases:
- PG
- P-GenRM
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "将用户偏好信号转化为结构化评估链（包含场景特定的用户人设和动态评分准则），并在测试时引入双粒度缩放机制（个体层级评分方案并行采样与基于用户原型的相似用户偏好聚合）。"
primary_logic: "利用生成式奖励模型（GenRM）的测试时扩展能力，通过自适应生成评估链来捕获场景依赖的偏好，同时结合用户原型聚类和原型增强注意力机制，在个体和群体两个粒度上整合偏好信息，既降低了推断噪声，又通过原型迁移提升了对新用户的泛化能力。"
claims:
- "P-GenRM-8B在PersonalRewardBench两个子集上全面超越先前最优的70B开源基线模型。"
- "测试时用户缩放（Ind-16, Pro-8）相比无缩放P-GenRM提升约3个百分点，且以更少的总评分次数超越更大的缩放配置Ind-32。"
- "P-GenRM在冷启动评估（LaMP-QA）中的平均Spearman相关系数显著高于所有基线，甚至超越参数规模大得多Qwen3-235B-A22B。"
- "移除强化学习的任意奖励信号（过程奖励PR或结果奖励OR）均导致性能显著退化，验证了过程级监督的必要性。"
---

# P-GenRM: Personalized Generative Reward Model with Test-time User-based Scaling

> [!tip] 核心洞察
> 利用生成式奖励模型（GenRM）的测试时扩展能力，通过自适应生成评估链来捕获场景依赖的偏好，同时结合用户原型聚类和原型增强注意力机制，在个体和群体两个粒度上整合偏好信息，既降低了推断噪声，又通过原型迁移提升了对新用户的泛化能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | P-GenRM：基于测试时用户缩放机制的个性化生成式奖励模型 |
| 英文题名 | P-GenRM: Personalized Generative Reward Model with Test-time User-based Scaling |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=hXNApWLBZG); [GitHub](https://github.com/Tongyi-ConvAI/Qwen-Character/tree/main/Character-GenRM) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | P-GenRM |
| Dataset | Chatbot Arena-Personalized (8B), PRISM-Personalized (8B), LaMP-QA (cold-start) |

> [!tip] 效果简介
> - Chatbot Arena-Personalized (8B) 上，Accuracy (%) 为 72.68，对比 69.78 (FTRM+SynthesizeMe-8B)，变化 +2.90。
> - PRISM-Personalized (8B) 上，Accuracy (%) 为 65.32，对比 62.84 (FTRM+SynthesizeMe-8B)，变化 +2.48。
> - LaMP-QA (cold-start) 上，Spearman's ρ (平均) 为 0.638，对比 0.599 (Qwen3-235B-A22B)，变化 +0.039。

## 概述

个性化奖励模型旨在根据用户的历史偏好信号，为不同用户对同一模型输出的主观评价提供精准预测。现有方法面临两个核心瓶颈：其一，将多样化、场景特定的用户偏好过度简化为固定、少量的评估准则，无法捕捉同一用户在不同情境下的偏好变化；其二，面对反馈稀疏的新用户时泛化能力薄弱，难以适应冷启动场景。

P-GenRM 通过两条关键路径突破上述瓶颈。**在建模层面**，它将混合偏好信号转化为结构化评估链，动态生成场景特定的用户人设与加权评分准则，取代了传统的静态评估规则。**在推断层面**，它引入测试时双粒度用户缩放机制：个体层级并行采样生成多个评分方案以降低推断噪声，原型层级通过用户聚类与原型增强注意力机制融入相似用户的偏好信息，从而提升对新用户的泛化能力。

训练策略上，P-GenRM 采用三段式框架：人设引导评分诱导（PSI）的监督微调、过程与结果双奖励的强化学习（CRE），以及硬负例课程学习，三者协同确保评估链的生成质量与鲁棒性。

在主要基准测试中，P-GenRM-8B 以显著更小的参数规模超越了先前最优的 70B 开源基线模型：Chatbot Arena 子集准确率达 72.68%（对比 FTRM+SynthesizeMe-70B 的 72.05%），PRISM 子集达 65.32%（对比 63.74%）。测试时用户缩放进一步带来约 3 个百分点的增益，且以更少的总评分次数超越了更大的缩放配置。在冷启动评估中，P-GenRM-8B 的平均 Spearman 相关系数（0.638）甚至超越了参数规模大得多的 Qwen3-235B-A22B（0.599）。消融实验证实，过程奖励与结果奖励的任意缺失均会导致性能显著退化，验证了过程级监督的必要性。

## 背景与动机

大语言模型（LLM）的快速演进使其在开放域对话、推理与工具使用等任务中展现出前所未有的能力，但如何让模型输出与多样化、动态变化的用户偏好保持精准对齐，始终是制约其实际部署的关键瓶颈。传统的对齐方法——无论是基于人类反馈的强化学习（RLHF）还是直接偏好优化（DPO）——通常假设存在一组普适、固定的评估准则，并通过聚合全体用户的偏好数据来训练单一的奖励模型。这种做法隐含地将“用户”视为同质整体，忽略了不同个体在风格、详细程度、安全性容忍度乃至价值观上的深层差异。

这一假设在实际应用中面临严峻挑战。同一用户在不同场景下的偏好可能截然不同：在寻求编程帮助时偏好简洁、可直接运行的代码，而在探讨哲学问题时则期待富有洞见的冗长论述。更棘手的是，新用户往往只提供极少量反馈，传统方法难以在稀疏信号下建立可靠的偏好模型，导致冷启动场景下的泛化能力严重不足。

### 现有方法的两个核心瓶颈

当前个性化奖励建模的研究试图通过引入用户特定表示来缓解上述问题，但仍存在两个根本性瓶颈：

**瓶颈一：偏好建模的过度简化。** 现有工作——无论是基于组偏好优化的 **GPO**（Zhao et al., 2023）、基于变分推断的 **VPL**（Poddar et al., 2024）、基于原型偏好点的 **PAL**（Chen et al., 2024），还是此前达到最优性能的 **SynthesizeMe**（Ryan et al., 2025）——均将用户偏好压缩为固定、少量的评估准则或静态人设。这种简化无法捕捉同一用户在不同情境下的偏好变化，本质上将“场景依赖的偏好”错误地建模为“用户恒定的属性”。当用户从技术问答切换到创意写作时，模型仍套用同一套评分标准，导致判断失准。

**瓶颈二：冷启动场景下的泛化薄弱。** 面对反馈稀疏的新用户，现有方法要么退化为无个性化的通用评分，要么因数据不足而产生高方差推断。参数规模更大的模型（如Qwen3-235B-A22B）虽能通过更强的先验知识部分弥补，但并未从根本上解决“如何从少量交互中提取可靠偏好信号”的问题。

### P-GenRM的动机与核心思路

P-GenRM的提出正是为了系统性地突破上述两个瓶颈。其核心洞察在于：**生成式奖励模型（GenRM）的测试时扩展能力**可以成为个性化建模的关键杠杆——与其将用户偏好固化为静态参数，不如让模型在每次评分时动态生成适配当前场景的结构化评估链。

具体而言，P-GenRM将混合偏好信号（隐式的历史选择与显式的用户陈述）转化为包含两个核心组件的评估链：**场景特定的用户人设**（persona）和**动态加权评分准则**（scoring rubrics）。这一设计使模型能够根据对话主题、用户历史行为模式以及当前候选响应的特征，自适应地调整评分依据的侧重点。

在训练策略上，P-GenRM采用三段式框架：先通过监督微调建立基础个性化评分能力，再利用过程奖励与结果奖励的双重强化学习提升评估链质量，最后通过硬负例课程学习增强对高度主观任务的鲁棒性。在测试时，P-GenRM引入**双粒度用户缩放机制**——在个体层级并行采样生成多个评分假设方案以降低推断噪声，同时在原型层级融入相似用户的偏好信息以增强泛化，从而在冷启动场景下实现有效的知识迁移。

这一设计将个性化奖励建模从“学习固定的用户表示”重新定义为“学习如何根据场景生成适配的评估逻辑”，从根本上回应了偏好动态性与数据稀疏性两大挑战。

## 核心创新

P-GenRM 的核心创新围绕“将个性化奖励建模从静态准则匹配转变为动态、场景自适应的评估链生成”展开。与现有方法相比，它在三个关键维度上实现了根本性转变。

### 从固定评估准则到结构化评估链

现有方法（如 **GPO** (Zhao et al., 2023)、**VPL** (Poddar et al., 2024)、**PAL** (Chen et al., 2024)）通常将用户偏好压缩为固定数量的评估维度或静态潜在变量，无法捕捉同一用户在不同场景下的偏好变化。**SynthesizeMe** (Ryan et al., 2025) 虽引入合成人设，但仍以静态先验的形式注入模型，缺乏对具体查询上下文的适应性。

P-GenRM 通过 **Persona-guided Scoring Induction (PSI)** 将混合偏好信号转化为结构化评估链，包含两个动态组件：
- **场景特定的用户人设**（Persona）：从历史交互和显式偏好中推断当前查询场景下的用户角色描述；
- **加权评分准则**（Scoring Rubrics）：根据推断的人设动态生成带有重要性权重的评分维度。

这一转变使得模型能够对不同场景生成差异化的评估标准——例如，同一用户在“音乐推荐”场景可能偏好新颖性，而在“严肃讨论”场景则更重视逻辑严谨性。消融实验证实了自适应人设的优越性：在 Qwen3-8B 基座上，PSI 在 Chatbot Arena 上达到 64.22%，而静态人设方法 SynthesizeMe 仅取得 62.84%（Table 3）。

### 从简单监督训练到过程级强化学习

传统奖励模型训练依赖 Bradley-Terry 微调或简单的监督学习，仅优化最终排序结果，缺乏对推理过程的监督。P-GenRM 引入三阶段训练框架：

1. **PSI 监督微调**：构建结构化评估链（SEC）数据集，使模型具备基本的个性化评分能力；
2. **Criteria-based Reasoning Enhancement (CRE)**：采用 GRPO 强化学习，同时施加**过程奖励**（PR）和**结果奖励**（OR），总奖励为 $\mathrm{R}_t = \alpha \cdot \mathrm{PR}_t + \beta \cdot \mathrm{OR}_t$，迫使模型在生成评估链的每一步都保持推理质量；
3. **硬负例课程学习**：逐步增加困难负例比例，并在后期禁用过程奖励，提升模型对高度主观任务的鲁棒性。

消融实验揭示了各阶段的关键性：同时移除课程学习和强化学习（w/o CL,RL）导致 Chatbot Arena 准确率从 72.68% 骤降至 66.76%；单独移除过程奖励（w/o CL,PR）降至 70.22%，单独移除结果奖励（w/o CL,OR）降至 69.05%（Table 2）。这表明过程级监督与结果监督具有互补性，二者缺一不可。

### 从单次评分到双粒度测试时缩放

现有方法在测试时通常仅执行单次评分或简单多数投票，无法有效应对偏好推断中的固有噪声和对新用户的泛化困难。P-GenRM 提出**测试时用户缩放机制**，在个体和原型两个粒度上并行采样并聚合评分：

- **个体层级**：对同一用户并行生成 $m$ 个评分方案，通过多次采样降低单次推断的随机噪声；
- **原型层级**：通过离线 K-means 聚类初始化用户原型，并利用原型增强注意力机制 $\alpha_\tau = \mathrm{softmax}_\tau \left( \frac{o_\tau^\top q_t}{\sqrt{d}} + \rho \frac{o_\tau^\top a_j}{\sqrt{d}} \right)$ 迭代优化原型表示，在测试时引入 $n$ 个相似用户的评分进行加权聚合。

最终评分由两层聚合得到：
$$s_t^i = \frac{1}{m} \sum_{x=1}^{m} \mathrm{Extract}(S_{t,x}^i) + \frac{1}{n} \sum_{w=1}^{n} \mathrm{Extract}\bigl( (S_t^i)^{(u_w)} \bigr)$$

这一机制的关键优势在于：原型层级的迁移使模型能够利用相似用户的偏好信息来补偿目标用户的数据稀疏性，从而显著提升冷启动场景下的泛化能力。实验显示，Ind-16 + Pro-8 配置以更少的总采样次数（24 次）超越了纯个体缩放 Ind-32（32 次）的性能（Table 1），验证了双粒度协同的有效性。在冷启动评估 LaMP-QA 上，P-GenRM-8B（Ind-8, Pro-4）的平均 Spearman 相关系数达到 0.638，甚至超越参数规模大得多的 Qwen3-235B-A22B（0.599）（Table 5）。

## 整体框架

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_hXNApWLBZG/figures/002_Figure_2.jpg]]
*Figure 2: (a) The three-stage training framework of P-GenRM (b) An illustration of the personalized evaluation chain, showing how preference modeling and derived scoring schemes lead to interpretable, criterion-weighted judgments for responses*

P-GenRM 的核心设计是将个性化奖励建模重新定义为**结构化评估链（Structured Evaluation Chain）的生成问题**。与以往将用户偏好压缩为固定规则或静态人设的方法不同，P-GenRM 从混合偏好信号（隐式历史交互与显式陈述）中动态推断场景特定的用户人设和加权评分准则，并据此对候选响应进行逐标准打分。

### 三阶段训练管线

模型训练分为三个递进阶段（Figure 2a），逐步提升评估链的质量与鲁棒性：

1. **人设引导评分诱导（Persona-guided Scoring Induction, PSI）**：通过监督微调（SFT）为模型注入基础的个性化评分能力。具体而言，先用指令大模型将用户的隐式偏好历史 $H_t^{(u)}$ 和显式偏好 $E^{(u)}$ 翻译为包含“用户人设 + 偏好分析 + 评分准则 + 逐响应判断”的结构化评估链，构建 SEC 数据集，再以此微调基座模型。

2. **基于准则的推理增强（Criteria-based Reasoning Enhancement, CRE）**：在 RL 阶段引入双重奖励信号——过程奖励 $\mathrm{PR}_t$ 评估推理链与评分准则的一致性，结果奖励 $\mathrm{OR}_t$ 评估最终排序的准确性，总奖励 $\mathrm{R}_t = \alpha \cdot \mathrm{PR}_t + \beta \cdot \mathrm{OR}_t$。采用 GRPO 算法优化，使模型在缺少显式偏好时仍能生成高质量的评估链。

3. **硬负例课程学习**：逐步增加困难负例（如偏好相近的候选对）的比例，并在后期禁用过程奖励，迫使模型在高度主观的场景下依然保持稳健的判别能力。

消融实验（Table 2）验证了这一管线设计的必要性：移除课程学习和 RL（w/o CL,RL）后，Chatbot Arena 准确率从 72.68% 骤降至 66.76%；同时移除课程学习和过程奖励（w/o CL,PR）或结果奖励（w/o CL,OR）也分别降至 70.22% 和 69.05%，表明**过程监督与结果监督缺一不可**。

### 测试时双粒度用户缩放

训练完成后，P-GenRM 在推理阶段引入**测试时用户缩放（Test-time User-based Scaling）**机制，从两个粒度聚合偏好信息以降低推断噪声并提升对新用户的泛化能力：

- **个体层级（Individual-level）**：对同一用户并行采样 $m$ 次，生成多个差异化的评分方案，取平均得到个体层级评分。
- **原型层级（Prototype-level）**：预先通过 K-means 聚类初始化用户原型，并在训练中利用原型增强注意力机制与成对损失迭代优化原型表示。测试时，从最近邻原型引入 $n$ 个相似用户的评分方案参与聚合。

最终评分为两个粒度评分的均值：
$$s_t^i = \frac{1}{m} \sum_{x=1}^{m} \mathrm{Extract}(S_{t,x}^i) + \frac{1}{n} \sum_{w=1}^{n} \mathrm{Extract}\bigl( (S_t^i)^{(u_w)} \bigr)$$

这一设计的关键洞察在于：**个体层级采样捕捉用户自身的偏好多样性，原型层级聚合则通过相似用户群体的共性偏好平滑个体噪声，同时借助原型迁移提升冷启动场景下的泛化能力**。实验表明，Ind-16 + Pro-8 配置以更少的总评分次数（24 次 vs 32 次）超越了纯个体缩放 Ind-32 的性能（Chatbot Arena 75.92% vs 75.50%），验证了双粒度互补的有效性。

### 输入输出流

整体流程（Figure 1）可概括为：
- **输入**：当前查询 $q_t$、用户历史交互 $H_t^{(u)}$、显式偏好陈述 $E^{(u)}$、候选响应 $\{y_t^i\}$
- **推理**：模型 $R_\theta$ 生成偏好建模 $P_t^{(u)}$（场景特定人设与偏好分析）和评分过程 $S_t^{(u)}$（加权评分准则与逐响应判断）
- **输出**：从 $S_t^{(u)}$ 中提取标量分数 $\{s_t^i\}$，经双粒度缩放聚合后得到最终排序

## 核心模块与公式推导

### 3.1 问题形式化

P-GenRM 将个性化奖励建模定义为一个条件生成任务。给定用户 $u$ 在第 $t$ 轮之前的隐式交互历史 $H_t^{(u)}$ 和显式偏好 $E^{(u)}$，模型需为当前查询 $q_t$ 下的候选响应 $y_t^i$ 生成个性化评分。交互历史的形式化为：

$$H_{t}^{(u)} = \left\{ (q_{1}, y_{1}^{+}, y_{1}^{-}), \ldots, (q_{\tau}, y_{\tau}^{+}, y_{\tau}^{-}), \ldots, (q_{t-1}, y_{t-1}^{+}, y_{t-1}^{-}) \right\}^{(u)}$$

其中每一轮包含查询 $q_\tau$ 及用户偏好的正响应 $y_\tau^+$ 和负响应 $y_\tau^-$。模型 $R_\theta$ 的推理过程为：

$$[P_{t}^{(u)}; S_{t}^{(u)}] \sim R_{\theta}(q_{t}, H_{t}^{(u)}, E^{(u)}, y_{t}^{i}), \quad \{s_{t}^{i}\}_{i=1}^{b} = \mathrm{Extract}(S_{t}^{(u)})$$

模型首先推断上下文感知的用户偏好建模 $P_t^{(u)}$ 和评分过程 $S_t^{(u)}$，随后从中提取 $b$ 个候选响应的标量分数 $\{s_t^i\}$。这一设计的核心在于将偏好信号转化为结构化的评估链，而非直接输出标量值。

### 3.2 三阶段训练框架

P-GenRM 的训练包含三个递进阶段：

**阶段一：人设引导评分诱导（PSI）**。利用指令微调 LLM，从用户混合偏好信号 $\{H_t^{(u)}, E^{(u)}\}$ 中合成结构化评估链（SEC）数据集。评估链包含场景特定的用户人设和带权重的动态评分准则，模型通过 SFT 学习将偏好信号翻译为可解释的评分过程。

**阶段二：基于准则的推理增强（CRE）**。采用 GRPO 算法进行强化学习，引入双重奖励信号：

$$\mathrm{R}_t = \alpha \cdot \mathrm{PR}_t + \beta \cdot \mathrm{OR}_t$$

其中 $\mathrm{PR}_t$ 为过程奖励，评估评估链中准则与用户偏好的对齐程度；$\mathrm{OR}_t$ 为结果奖励，基于规则验证最终评分是否与用户真实偏好一致。$\alpha$ 和 $\beta$ 为平衡超参数。GRPO 目标函数为：

$$J_{GRPO}(\theta) = \mathbb{E}_{(q_t, H_t^{(u)}, y_t^i) \sim \mathcal{D}} \left[ \frac{1}{K} \sum_{k=1}^{K} \frac{1}{|c_t^{(k)}|} \sum_{j=1}^{|c_t^{(k)}|} \left\{ \min\left( \frac{\pi_\theta(c_{t,j}^{(k)} | q_t, H_t^{(u)}, y_t^i)}{\pi_{\theta_{old}}(c_{t,j}^{(k)} | q_t, H_t^{(u)}, y_t^i)} A_k, \text{clip}(\cdot) A_k \right) - \beta_{KL} \mathbb{D}_{KL}(\pi_\theta \| \pi_{ref}) \right\} \right]$$

**阶段三：硬负例感知课程学习**。逐步增加困难负例（偏好差异微小的响应对）的比例，并在后期禁用过程奖励，迫使模型在高度主观场景下依赖结果信号进行鲁棒推理。

### 3.3 离线原型初始化与精炼

用户原型的构建分为两步。首先，对跨场景用户偏好嵌入矩阵进行 K-means 聚类，获得 $k$ 个初始原型 $\mathbf{A} \in \mathbb{R}^{k \times d}$。随后，通过原型增强注意力机制和历史感知更新迭代精炼原型。

**原型增强注意力**。给定用户的历史记录表示 $\{o_\tau\}_{\tau=1}^h$，原型 $a_j$ 与当前查询 $q_t$ 共同引导注意力权重分配：

$$v_H = \sum_{\tau=1}^{\mathbf{h}} \alpha_\tau o_\tau, \quad \alpha_\tau = \mathrm{softmax}_\tau \left( \frac{o_\tau^\top q_t}{\sqrt{d}} + \rho \frac{o_\tau^\top a_j}{\sqrt{d}} \right)$$

其中 $\rho$ 控制原型对注意力权重的影响强度，$v_H$ 为加权聚合的显著历史信息。

**判别先验更新**。将原型、当前查询和显著历史融合为区分正负样本的先验表示：

$$z_t = a_j + \lambda_q W_q q_t + \lambda_s W_s v_H$$

**原型优化损失**。通过成对损失最大化正负样本间的判别分数差：

$$\Delta_t = z_t^\top y_t^{+} - z_t^\top y_t^{-}, \qquad \mathcal{L}_{\mathrm{pair}} = -\log \sigma(\Delta_t)$$

总体损失加入聚类中心约束和平滑更新正则项：

$$\mathcal{L} = \mathcal{L}_{\mathrm{pair}} + \lambda_{\mathrm{cent}} \| a_j - \mu_j \|_2^2 + \lambda_{\mathrm{tr}} \| a_j - p_j \|_2^2$$

其中 $\mu_j$ 为分配给原型 $j$ 的用户的嵌入均值，$p_j$ 为原型的历史状态，$\lambda_{\mathrm{cent}}$ 和 $\lambda_{\mathrm{tr}}$ 分别控制靠近聚类中心和保持平滑更新的强度。

### 3.4 测试时双粒度用户缩放

测试时，P-GenRM 在个体和原型两个粒度上并行扩展评分方案并聚合结果。最终评分由 $m$ 次个体层级采样和 $n$ 个相似用户评分的均值组成：

$$s_t^i = \frac{1}{m} \sum_{x=1}^{m} \mathrm{Extract}(S_{t,x}^i) + \frac{1}{n} \sum_{w=1}^{n} \mathrm{Extract}\bigl( (S_t^i)^{(u_w)} \bigr)$$

个体层级缩放通过多次采样生成多样化的评分假设，降低单次推断的噪声方差；原型层级缩放从最近邻原型引入相似用户的偏好信息，增强对新用户和稀疏反馈场景的泛化能力。两者结合使得 P-GenRM 以更少的总评分次数（如 Ind-16 + Pro-8）超越单纯扩大个体采样的配置（如 Ind-32）。

## 实验与分析

### 主实验结果

P-GenRM在个性化奖励评估基准PersonalRewardBench的两个子集上均取得最优结果，且以8B参数规模超越了此前最优的70B开源基线模型。Table 1汇总了核心对比数据：在Chatbot Arena-Personalized子集上，P-GenRM-8B达到72.68%准确率，较先前最优基线**FTRM+SynthesizeMe-8B**（Ryan et al., 2025）的69.78%提升2.90个百分点，并超越FTRM+SynthesizeMe-70B的72.05%；在PRISM-Personalized子集上，P-GenRM-8B达到65.32%，较FTRM+SynthesizeMe-8B的62.84%提升2.48个百分点，同样超越其70B版本的63.74%。这一跨尺度的性能优势表明，P-GenRM的个性化评估链生成机制比单纯扩大模型规模更有效。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_hXNApWLBZG/figures/003_Table_1.jpg]]
*Table 1: Results on PersonalRewardBench. P-GenRM outperforms all baselines on both datasets and model scales, while Test-time User-based Scaling brings further gains. Best and second-best results are marked in bold and underline. Ind and Pro denote the Individual and Prototype level scaling, respectively. Results are reported as “mean ± standard error” over 5 independent runs*

引入测试时用户缩放后，性能进一步提升。最优配置Ind-16、Pro-8在Chatbot Arena上达到75.92%（+3.24%），在PRISM上达到68.06%（+2.74%），且以更少的总评分次数（16+8=24）超越了纯个体缩放配置Ind-32的75.33%（Chatbot Arena）。这表明原型层级的相似用户偏好聚合不仅提升了评分准确性，还提高了缩放效率。

### 消融实验

Table 2系统拆解了P-GenRM各训练组件的作用。移除课程学习（w/o CL）导致Chatbot Arena准确率从72.68%降至71.07%，PRISM从65.32%降至63.41%。进一步移除过程奖励PR（w/o CL,PR）使性能降至70.22%/62.39%；移除结果奖励OR（w/o CL,OR）则降至69.05%/61.80%。完全移除RL和课程学习、仅保留SFT（w/o CL,RL）的性能退化最为严重，降至66.76%/57.08%。这组消融揭示了两个关键因果机制：

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_hXNApWLBZG/figures/004_Table_2.jpg]]
*Table 2: Ablation studies of P-GenRM components: CL (Curriculum Learning), PR (Process Reward), OR (Outcome Reward). Results are reported as “mean ± standard error” over 5 independent runs. Table 3: Comparison of adaptive (PSI, Personaguided Scoring Induction) and static (SMe, SynthesizeMe) persona methods across base models. Results are reported as “mean ± standard error” over 5 independent runs*

1. **过程奖励与结果奖励具有互补性但不可相互替代**：单独移除PR或OR均导致约1.5–2.6个百分点的退化，说明PR引导的评估链生成质量与OR验证的评分准确性共同支撑了模型性能。
2. **课程学习对高度主观场景的鲁棒性至关重要**：在PRISM这类用户偏好差异更大的数据集上，移除CL的退化幅度（约1.9个百分点）高于Chatbot Arena（约1.6个百分点），印证了硬负例课程学习对处理偏好冲突的有效性。

Table 3进一步对比了自适应人设生成（PSI）与静态人设方法（SynthesizeMe）。在Qwen3-8B基座上，PSI在Chatbot Arena上达到64.22%，显著高于SynthesizeMe的60.13%；在PRISM上达到58.01% vs 55.32%。这一差距在更大基座模型上依然保持，验证了场景特定动态人设相较于固定用户画像的核心优势。

### 原型机制分析

原型数量的选择通过PCA保留方差比确定（Figure 3左图）。在Chatbot Arena和PRISM上，保留前50个奇异向量可解释约85%以上的方差，因此选定k=50作为原型数量。Figure 3右图显示，原型数量从0增至50时性能持续提升，增至100时趋于饱和甚至略有下降，表明50个原型已能充分捕捉用户群体的偏好异质性，过多原型反而引入冗余噪声。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_hXNApWLBZG/figures/005_Figure_3.jpg]]
*Figure 3: Determination of prototype numbers and their effect on scaling performance. Left: retained variance ratio as a function of the number of singular vectors on Chatbot Arena and PRISM. Right: performance of P-GenRM with different prototype numbers*

Figure 4的用户-原型分布可视化进一步验证了原型建模的有效性：同一原型簇内的用户共享核心偏好模式（蓝色高亮），同时保留个体差异（红色高亮）；不同簇之间则呈现明确分离的偏好倾向。Figure 5显示各原型的样本分配相对均衡，且P-GenRM在各原型上的性能保持稳定（Table 9），未出现对多数群体的过拟合。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_hXNApWLBZG/figures/014_Table_9.jpg]]
*Table 9: Stable performance of P-GenRM across prototypes*

### 冷启动泛化

在LaMP-QA冷启动评估中（Table 5），P-GenRM-8B（Ind-8, Pro-4）取得0.638的平均Spearman相关系数，显著超越所有基线，包括参数规模大得多的Qwen3-235B-A22B（0.599）。这一结果的关键在于原型迁移机制：当新用户历史交互稀疏时，原型层级的相似用户偏好聚合提供了有效的先验信息，弥补了个体层级推断的不确定性。

### 公平性分析

P-GenRM在宏观准确率（每个用户组单独计算准确率后取平均）上达到65.21%（Table 10），超越所有基线方法，且在各用户组上的性能分布均衡（Table 9），表明模型未因追求整体准确率而牺牲少数群体的评估质量。这一特性源于双粒度缩放机制中个体层级采样的多样性保留与原型层级聚合的噪声平滑之间的平衡。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_hXNApWLBZG/figures/015_Table_10.jpg]]
*Table 10: P-GenRM outperforms baselines methods using macro-accuracy as the metric*

### 推理效率与局限

尽管测试时用户缩放在准确率上带来显著增益，但其推理开销与缩放次数呈线性关系（Table 11）。与直接输出标量值的传统奖励模型相比，P-GenRM需要生成完整评估链，在低延迟场景下存在效率瓶颈。此外，模型依赖至少三条历史偏好选择来构建合理的偏好分析（Table 12），在绝对冷启动（零历史交互）场景下的性能仍需进一步验证。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_hXNApWLBZG/figures/018_Table_11.jpg]]
*Table 11: Inference time comparison between P-GenRM with test-time user-based scaling and baseline methods*

### 补充图表

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_hXNApWLBZG/figures/006_Table.jpg]]

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_hXNApWLBZG/figures/008_Table.jpg]]

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_hXNApWLBZG/figures/009_Table_6.jpg]]
*Table 6: Accuracy(%) of LLM-as-a-Judge with different types of user preference indicators*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_hXNApWLBZG/figures/010_Table_7.jpg]]
*Table 7: Performance changes of the model after reinforcement learning under different $\alpha \cdot \beta$ settings

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_hXNApWLBZG/figures/012_Table_8.jpg]]
*Table 8: Distribution of user groups in the PRISM dataset*

## 方法谱系与知识库定位

### 问题定位：从固定准则到场景自适应偏好建模

传统个性化奖励模型面临两个根本性瓶颈：其一，将多样化、场景特定的用户偏好过度简化为固定、少量的评估准则，无法捕捉同一用户在不同情境下的偏好变化；其二，面对反馈稀疏的新用户时泛化能力薄弱，难以适应冷启动场景。P-GenRM 的核心洞察在于，生成式奖励模型（GenRM）的测试时扩展能力为同时解决这两个问题提供了可能——通过自适应生成评估链来捕获场景依赖的偏好，同时结合用户原型聚类和原型增强注意力机制，在个体和群体两个粒度上整合偏好信息。

### 与基线方法的关系

**GPO**（Zhao et al., 2023）采用组偏好优化策略，其局限性在于将用户偏好建模为固定组的静态归属，无法处理同一用户在不同场景下的偏好漂移。P-GenRM 通过结构化评估链中的动态人设生成机制，使偏好建模随查询场景自适应变化，而非依赖预设的组标签。

**VPL**（Poddar et al., 2024）基于变分推断学习用户特定的潜在变量，虽然引入了用户个性化表示，但其潜在空间建模缺乏可解释性，且面对新用户时需要重新推断潜在变量，冷启动能力受限。P-GenRM 的原型机制则通过 K-means 初始化用户原型并利用历史感知注意力迭代优化，使新用户可以通过最近邻原型快速获得合理的偏好先验，无需从零开始推断。

**PAL**（Chen et al., 2024）通过原型偏好点实现多元化对齐，其原型思想与 P-GenRM 的用户原型聚类存在概念关联。但 PAL 的原型主要用于策略模型的对齐目标多样化，而 P-GenRM 的原型机制直接服务于奖励模型的测试时缩放——通过原型增强注意力机制将相似用户的评分方案加权聚合，在推断阶段降低个体噪声。

**SynthesizeMe**（Ryan et al., 2025）是该领域此前的 SOTA 方法，通过合成人设来实现个性化奖励建模。然而，SynthesizeMe 的人设是静态先验，无法随场景动态调整。P-GenRM 的 Persona-guided Scoring Induction（PSI）模块直接针对这一缺陷，从混合偏好信号中动态生成场景特定的用户人设及加权评分准则。实验证据（Table 3）表明，在相同基座模型上，PSI 的自适应人设策略一致优于 SynthesizeMe 的静态人设方法。

**Bradley-Terry Finetuned Reward Model** 作为经典基线，在全体数据上微调 BT 模型，完全忽略了用户个性化差异，其性能上限受限于数据中偏好冲突的不可调和性。P-GenRM 通过结构化评估链将用户偏好显式编码为评分准则，使模型能够对不同用户的冲突偏好做出差异化判断。

### 训练策略的谱系定位

P-GenRM 的三段式训练框架（SFT + RL + 课程学习）在奖励模型训练谱系中引入了两个关键创新：

1. **过程与结果双奖励的强化学习**：传统奖励模型训练通常仅依赖结果监督（如 BT 损失的二元比较），P-GenRM 在 GRPO 框架中同时引入过程奖励 $\mathrm{PR}_t$ 和结果奖励 $\mathrm{OR}_t$（总奖励 $\mathrm{R}_t = \alpha \cdot \mathrm{PR}_t + \beta \cdot \mathrm{OR}_t$），使模型在生成评估链的每一步都能获得细粒度监督信号。消融实验（Table 2）表明，移除任意一种奖励信号均导致性能显著退化（w/o CL,PR 降至 70.22%，w/o CL,OR 降至 69.05%），验证了过程级监督的必要性。

2. **硬负例课程学习**：逐步增加困难负例比例并动态禁用过程奖励，迫使模型在高度主观场景下仍能保持鲁棒判断。这一策略在奖励模型训练中较为罕见，其有效性体现在消融实验中移除课程学习后准确率从 72.68% 下降至 71.07%。

### 测试时缩放的创新边界

P-GenRM 的双粒度测试时用户缩放机制（个体层级并行采样 + 原型层级偏好聚合）在推理阶段实现了“以计算换精度”的范式突破。与简单多数投票不同，个体层级的并行采样生成多个假设评分方案，本质上是对用户偏好推断不确定性的蒙特卡洛近似；原型层级的聚合则通过引入相似用户的评分信息，在群体层面平滑个体推断噪声。最终评分公式 $s_t^i = \frac{1}{m} \sum_{x=1}^{m} \mathrm{Extract}(S_{t,x}^i) + \frac{1}{n} \sum_{w=1}^{n} \mathrm{Extract}\bigl( (S_t^i)^{(u_w)} \bigr)$ 体现了这种双粒度信息融合的设计哲学。

值得注意的是，最优缩放配置 Ind-16, Pro-8 以更少的总评分次数（24次）超越了更大的 Ind-32（32次），说明原型层级的群体信息引入不仅降低了噪声，还提升了缩放效率。

### 适用边界与局限

1. **推理效率瓶颈**：P-GenRM 需要生成完整的评估链来获得可靠的个性化分数，推理效率低于直接输出标量值的传统奖励模型。测试时缩放进一步增加了计算开销，在实际部署中需要在精度和延迟之间权衡。

2. **冷启动的最低数据要求**：尽管 P-GenRM 在冷启动场景下表现优异（LaMP-QA 平均 Spearman 相关系数 0.638，超越 Qwen3-235B-A22B 的 0.599），但模型仍依赖至少三条历史偏好选择来构建合理的偏好分析。对于完全没有历史交互的绝对冷启动用户，模型如何有效初始化并推断偏好仍是开放问题。

3. **评估链的推理偏差风险**：评估链的生成过程可能引入额外的推理偏差，特别是在少数群体用户上。尽管 P-GenRM 在宏观准确率评估中取得了 65.21% 的最高分（Table 10），表明其对不同用户组具有较好的公平性，但评估链生成的可控性和偏差量化仍需进一步研究。

### 开放问题

- 在长对话或多轮交互中，用户偏好可能发生漂移，模型如何动态适应这种变化而无需重新生成完整的评估链？
- 原型数量（当前通过 PCA 保留方差比确定）的自动化选择策略是否可以在线自适应调整？
- 评估链的可解释性是否可以被下游策略模型直接利用，实现更高效的个性化对齐？

## 原文 PDF

![[paperPDFs/ICLR_2026/P_GenRM_Personalized_Generative_Reward_Model_with_Test_time_User_based_Scaling.pdf]]
