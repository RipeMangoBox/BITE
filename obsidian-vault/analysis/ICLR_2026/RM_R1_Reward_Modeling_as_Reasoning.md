---
title: "RM-R1: Reward Modeling as Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/RM_R1_Reward_Modeling_as_Reasoning.pdf
project_link: null
code_link: https://github.com/RM-R1-UIUC/RM-R1
openreview_forum_id: 1ZqJ6jj75q
aliases:
- RRRRM
- RM-R1
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "将奖励建模重新定义为推理任务，通过链式评分准则（Chain-of-Rubrics）配合“蒸馏→强化学习”两阶段训练注入充分的推理能力。"
primary_logic: "让奖励模型在评分前先进行长链推理（生成评分标准或自行求解），再基于推理结果评判，能够显著提升解释性与准确率；蒸馏式预训练与GRPO强化学习结合，可以有效克服过拟合，充分释放推理潜力。"
claims:
- "RM-R1在三个奖励模型基准上的平均性能超越更大规模的开源模型（70B INF-ORM）和闭源模型（GPT‑4o），最大提升4.9%。"
- "先蒸馏后RL的训练范式在公平对比下始终优于纯SFT和冷启动RL，蒸馏只在9k数据上也能取得明显收益。"
- "任务类型分类（Chat/Reasoning）和评分准则生成对推理密集型任务提升显著，在RewardBench推理子集上可将准确率从94.2提升至96.3。"
- "平均 (RewardBench, RM-Bench, RMB) 上 平均得分 = 81.2 (RM-R1-Qwen-Instruct-32B)"
---

# RM-R1: Reward Modeling as Reasoning

> [!tip] 核心洞察
> 让奖励模型在评分前先进行长链推理（生成评分标准或自行求解），再基于推理结果评判，能够显著提升解释性与准确率；蒸馏式预训练与GRPO强化学习结合，可以有效克服过拟合，充分释放推理潜力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | RM-R1：将奖励建模作为推理任务 |
| 英文题名 | RM-R1: Reward Modeling as Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=1ZqJ6jj75q) · [GitHub](https://github.com/RM-R1-UIUC/RM-R1) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | RM-R1 (Reasoning Reward Model) |
| Dataset | 平均 (RewardBench, RM-Bench, RMB), 平均 (三个基准) |

> [!tip] 效果简介
> - 平均 (RewardBench, RM-Bench, RMB) 上，平均得分 为 81.2 (RM-R1-Qwen-Instruct-32B)，对比 78.8 (INF-ORM-Llama3.1-70B)，变化 +2.4。
> - RM-Bench 上，平均准确率 为 83.9 (RM-R1-DeepSeek-Distilled-Qwen-32B)，对比 75.2 (Gemini-1.5-pro)，变化 +8.7。
> - 平均 (三个基准) 上，平均得分 为 79.6 (RM-R1-DeepSeek-Distilled-Qwen-14B)，对比 77.7 (GPT-4o-0806)，变化 +1.9。

## 概要

### 问题瓶颈

现有生成式奖励模型（GenRM）在判断人类偏好时，普遍缺少深度推理能力。它们倾向于捕捉训练数据中的表面统计模式——例如文本长度、词汇分布等浅层特征——而非深入理解响应内容的实质质量。这一缺陷导致模型在面对复杂、微妙的偏好判断时评估不可靠，尤其容易忽略情感伤害、逻辑谬误等深层问题（Figure 1）。标量奖励模型虽在部分基准上表现强劲，但缺乏可解释的评判过程；而直接使用指令微调模型进行偏好判断，则面临严重的过拟合风险。

### 核心方法：将奖励建模重新定义为推理任务

RM-R1 的核心洞察是：**让奖励模型在评分前先进行长链推理，再基于推理结果做出判断**。具体而言，RM-R1 引入了链式评分准则（Chain-of-Rubrics, CoR）机制：对于 Chat 类任务，模型首先生成细粒度的评分 rubric，再逐条对照评估；对于 Reasoning 类任务（数学、代码等），模型先自行求解问题，再基于求解结果评判候选响应的正确性。

训练上，RM-R1 采用“蒸馏→强化学习”两阶段范式：
1. **推理蒸馏**：利用高性能教师模型（Claude + O3）合成的高质量推理链，将指令模型转化为具备初步推理能力的奖励模型。
2. **GRPO 强化学习**：在偏好数据上进一步优化，克服蒸馏阶段的过拟合，提升泛化性。奖励函数仅基于预测正确性给出 ±1 二值奖励，不依赖格式匹配等辅助信号。

### 主要结果

在 RewardBench、RM-Bench、RMB 三个奖励模型基准上，RM-R1 的平均性能超越了更大规模的开源模型和闭源模型：

- **RM-R1-Qwen-Instruct-32B** 在三基准平均得分上达到 81.2，超越 70B 的 INF-ORM（78.8）和 GPT-4o（77.7），最大提升 4.9%。
- **RM-R1-DeepSeek-Distilled-Qwen-32B** 在 RM-Bench 上达到 83.9，显著优于 Gemini-1.5-pro（75.2），提升 8.7 个百分点。
- 消融实验证实，蒸馏预训练和任务类型分类（QC）是性能的关键驱动因素：加入蒸馏后平均分从 90.8 提升至 91.4；加入 QC 后 Reasoning 子集准确率从 94.2 跃升至 96.3。

### 方法定位

RM-R1 属于**推理增强型生成式奖励模型（REASRM）**，区别于传统的标量奖励模型（ScalarRM）和普通生成式奖励模型（GenRM）。其核心贡献在于将奖励建模从“直接输出偏好标签”转变为“先推理、后判断”的范式，并通过蒸馏与强化学习的协同训练充分释放推理潜力。



### 奖励建模的范式转变：从标量回归到生成式判断

在大语言模型对齐流程中，奖励模型（Reward Model, RM）承担着关键角色：它接收一个提示 $x$ 和一对候选响应 $(y_a, y_b)$，输出偏好判断以指导策略优化。传统方法将奖励建模为标量回归问题——为每个响应分配一个实数值分数，通过分数比较确定偏好。然而，近年来生成式奖励模型（Generative RM, GenRM）逐渐兴起，它将奖励建模重新定义为文本生成任务：模型直接生成偏好判断文本 $j$，其似然由自回归概率给出：

$$r_{\theta}(j | x, y_{a}, y_{b}) = \prod_{t=1}^{T} r_{\theta}(j_{t} | x, y_{a}, y_{b}, j_{<t})$$

训练目标是最大化预测偏好标签 $\hat{l}$ 与真实标签 $l$ 一致的期望准确率：

$$\max_{r_{\theta}} \mathbb{E}_{(x,y_a,y_b,l)\sim\mathcal{D}, \hat{l}\sim r_{\theta}(j|x,y_a,y_b)} [\mathbb{1}(\hat{l}=l)]$$

这种生成式范式赋予了奖励模型更强的可解释性——它不仅能输出判断结果，还能以自然语言阐述判断理由。然而，现有生成式奖励模型存在一个根本性缺陷：**它们往往依赖表面模式而非内容实质进行判断**。

### 核心瓶颈：缺少深度推理的“伪判断”

如 Figure 1 所示，直接使用指令微调模型（Instruct Model）作为奖励模型时，模型容易过拟合到监督数据中的浅层模式。例如，当被要求评判一个包含情感伤害但表面措辞礼貌的响应时，指令模型可能仅因“格式规范”或“没有脏话”就给出高分，完全忽略了对深层情感影响的评估。这种“表面正确”的判断在复杂偏好场景下尤其不可靠。

这一瓶颈的根源在于：**现有生成式奖励模型缺少深度推理能力**。它们被训练为直接输出判断，却未经历“先分析、后评判”的认知过程。当面对需要多步逻辑推演（如数学证明验证）或需要细粒度标准权衡（如安全性 vs. 有用性）的偏好判断时，缺乏推理的模型只能退回到训练数据中习得的统计相关性，而非对内容实质的把握。

### 核心思路：将奖励建模重新定义为推理任务

RM-R1 的核心洞察是：**让奖励模型在评分前先进行长链推理，再基于推理结果做出评判**。具体而言，模型根据任务类型生成不同的中间推理链：

- **对话类任务（Chat）**：模型首先生成细粒度的评分准则（rubrics），逐条列出理想响应应满足的标准，然后将候选响应与这些准则逐一对照评估。
- **推理类任务（Reasoning）**：模型先自行求解问题（如推导数学证明、执行代码逻辑），再基于正确答案评判候选响应的质量。

这种“链式评分准则”（Chain-of-Rubrics, CoR）机制将奖励建模从“黑箱判断”转变为“推理-评判”两阶段过程，既提升了判断的准确率，又提供了可审计的解释链。

### 训练范式：蒸馏与强化学习的协同

仅有推理形式还不够——模型需要被训练成真正擅长推理。RM-R1 采用“蒸馏→强化学习”两阶段训练范式：

1. **推理蒸馏（Reasoning Distillation）**：利用强教师模型（如 Claude 和 O3）合成的高质量推理链，将基础指令模型引导为具备初步推理能力的奖励模型。蒸馏轨迹将教师推理链 $r^{(i)}$ 与正确标签 $l^{(i)}$ 拼接作为训练目标 $y_{\text{trace}}^{(i)} = r^{(i)} \oplus l^{(i)}$，通过负对数似然损失 $\mathcal{L}_{\text{distill}}$ 进行优化。

2. **强化学习微调（RL with GRPO）**：蒸馏模型容易过拟合到教师推理的特定模式，泛化能力受限。为此，RM-R1 引入基于 Group Relative Policy Optimization（GRPO）的强化学习阶段，使用仅基于预测正确性的二值奖励函数 $\mathcal{R}(x,j|y_a,y_b) \in \{+1, -1\}$，在偏好数据上进一步优化模型，使其推理链更加精炼且泛化。

这种两阶段设计的关键在于：蒸馏提供了高质量的推理“种子”，RL 则让模型超越教师、学会自主推理。消融实验表明，纯强化学习（Cold Start RL）虽然能带来一定提升，但缺少蒸馏热启动时，弱模型往往难以在 RL 过程中探索出高质量的推理链；而纯 SFT 方法则始终被推理训练（蒸馏+RL）大幅超越，即使后者仅使用 9k 条蒸馏数据。



## 核心方法与创新机理

RM-R1的核心创新在于将奖励建模重新定义为**推理任务**，并通过“蒸馏→强化学习”两阶段训练范式注入深度推理能力，从而突破现有生成式奖励模型仅依赖表面模式、缺乏内容实质评判的瓶颈。

### 从直接判断到链式评分准则推理

传统生成式奖励模型直接输出偏好判断，缺少结构化的中间推理过程。RM-R1引入**链式评分准则（Chain-of-Rubrics, CoR）**机制，根据任务类型自动选择推理策略：

- **Chat类型**：模型首先生成细粒度的评分准则（rubric），再基于准则对候选回复进行逐项评估。
- **Reasoning类型**（数学/代码）：模型先自行求解问题，再以求解结果作为参照评判候选答案的正确性。

这一策略使奖励模型从“黑箱打分”转变为“可解释推理评判”。消融实验表明，仅添加CoR提示即可在RewardBench上带来0.6个百分点的提升（Table 2: Cold Start RL + Rubrics vs Cold Start RL），而进一步引入任务类型分类（QC）后，Reasoning子集的准确率从94.2跃升至96.3。

### 蒸馏→强化学习两阶段训练范式

RM-R1的训练范式是另一关键创新。现有方法或采用纯SFT（过拟合表面模式），或采用冷启动RL（训练不稳定且性能有限）。RM-R1提出**先蒸馏后RL**的方案：

1. **推理蒸馏阶段**：利用教师模型（Claude + O3）合成的高质量推理链，通过负对数似然损失将指令模型转化为具备初步推理能力的奖励模型。
2. **强化学习阶段**：采用GRPO（Group Relative Policy Optimization）进一步优化，克服蒸馏带来的过拟合，提升泛化性。

这一范式在公平对比下始终优于纯SFT和冷启动RL。Table 3显示，RM-R1（蒸馏+RL）在三基准上的平均分达81.2，而纯SFT方法仅77.4；即使仅使用9k蒸馏数据（Instruct+Distilled 9k），也以79.2分大幅超越全量SFT的76.6分。

### 简化奖励函数：仅依赖正确性

与许多RL训练中同时使用格式奖励和正确性奖励的做法不同，RM-R1的RL阶段采用**纯正确性二值奖励**（±1），不设格式奖励：

$$\mathcal{R}(x,j|y_a,y_b) = \begin{cases} 1 & \text{if } \hat{l}=l \\ -1 & \text{otherwise} \end{cases}$$

这一设计避免了格式奖励对推理行为的干扰，使模型专注于提升评判准确性。训练动态（Figure 5）显示，热启动RL（蒸馏后）相比冷启动RL更为稳定，推理链在训练过程中逐步精炼而非简单变长。

### 创新点的协同效应

上述三个创新并非孤立存在。CoR提供了推理的结构化形式，蒸馏注入高质量的推理先验，RL则通过正确性奖励强化推理与准确评判之间的因果关联。Table 2的消融实验完整揭示了这一协同路径：从基础指令模型出发，依次加入冷启动RL（+3.7）、评分准则（+0.6）、任务分类（+0.7）、蒸馏（+0.6），最终RM-R1在RewardBench上达到91.4的平均分，其中Reasoning子集从86.3提升至96.3，Chat Hard从72.0提升至82.6。



![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_1ZqJ6jj75q/figures/002_Figure_2.jpg]]
*Figure 2: Training pipeline of RM-R1. Starting from an instruct model (GenRM), RM-R1 training involves two stages: Distillation and Reinforcement Learning (RL). In the Distillation stage, we use high-quality synthesized data to bootstrap RM-R1’s reasoning ability. In the RL stage, RM-R1’s reasoning ability for reward modeling is further strengthened. After distillation, a GenRM evolves into a REASRM. RM-R1 further differentiates itself by being RL finetuned on preference data*

RM-R1 将奖励建模重新定义为推理任务，其训练流程由两个阶段构成：**推理蒸馏**与**强化学习微调**。整体管线以现成的指令微调生成式奖励模型为起点，依次注入推理能力并优化泛化性，最终产出具备深度推理能力的奖励模型。

### 管线总览

整个训练管线遵循“指令模型 → 蒸馏 → RL → 推理奖励模型”的路径：

1. **起点：生成式奖励模型**。给定输入提示 $x$ 和两个候选响应 $y_a, y_b$，模型自回归地生成文本判断 $j$，其概率为 $r_{\theta}(j | x, y_{a}, y_{b}) = \prod_{t=1}^{T} r_{\theta}(j_{t} | x, y_{a}, y_{b}, j_{<t})$。整体目标为最大化预测偏好标签 $\hat{l}$ 与真实标签 $l$ 一致的期望准确率。

2. **阶段一：推理蒸馏**。利用教师模型合成的高质量推理链，将指令模型转化为具备初步推理能力的奖励模型。蒸馏数据中，每条样本的推理轨迹由教师推理链 $r^{(i)}$ 与正确标签 $l^{(i)}$ 拼接而成：$y_{\mathrm{trace}}^{(i)} = r^{(i)} \oplus l^{(i)}$。模型通过最大化该轨迹的负对数似然进行训练。

3. **阶段二：强化学习微调**。蒸馏模型容易过拟合到训练数据的特定模式，因此引入基于 GRPO 的强化学习阶段。该阶段仅依据预测正确性给予二值奖励：$\mathcal{R}(x,j|y_a,y_b) = 1$（若 $\hat{l}=l$）或 $-1$（其他情况），不设格式奖励。训练目标为带 KL 正则的期望奖励最大化。

### 推理时的链式评分准则

在推理阶段，RM-R1 采用**链式评分准则**策略生成最终判断：

- **Chat 类型任务**：模型先生成针对样本的评分 rubric，再对照 rubric 评估两个响应。
- **Reasoning 类型任务**：模型先自行求解问题，再基于求解结果评判候选响应的正确性。

任务类型由模型根据系统提示自动分类，无需外部分类器。这一设计使奖励模型在做出偏好判断前执行显式的中间推理，从而超越表面模式，深入评估响应内容实质。

### 模块关系与数据流

| 模块 | 输入 | 输出 | 核心作用 |
|------|------|------|----------|
| 推理蒸馏 | 教师合成的高质量推理链 + 偏好数据 | 具备初步推理能力的奖励模型 | 通过监督学习注入推理行为模式 |
| 强化学习训练 | 蒸馏后的模型 + 偏好数据 | 泛化优化的推理奖励模型 | 克服蒸馏过拟合，释放推理潜力 |
| 链式评分准则推理 | 输入提示 + 两个候选响应 | 包含推理链的偏好判断文本 | 在推理时引导模型进行结构化中间推理 |
| 规则化奖励函数 | 模型输出 + 真实标签 | ±1 标量奖励 | 为 RL 提供简洁无偏的训练信号 |

### 关键设计权衡

- **蒸馏 → RL 的顺序不可逆**：纯冷启动 RL 缺乏初始推理能力，训练后期不稳定；纯蒸馏则泛化受限。两阶段结合使模型既获得推理行为先验，又通过 RL 进一步精炼。
- **奖励函数去格式化**：移除了常见的格式奖励分量，仅保留正确性信号，避免模型为迎合格式而牺牲判断质量。
- **推理预算可配置**：训练时的 rollout 预算与推理时的计算预算保持一致，使模型在不同推理开销下均能稳定工作。



### 生成式奖励建模的形式化

RM‑R1 将奖励建模定义为生成任务。给定输入提示 $x$ 和两个候选响应 $y_a, y_b$，模型以自回归方式生成判断文本 $j$，其概率为：

$$r_{\theta}(j | x, y_{a}, y_{b}) = \prod_{t=1}^{T} r_{\theta}(j_{t} | x, y_{a}, y_{b}, j_{<t}) \tag{2}$$

其中 $j_t$ 为第 $t$ 个 token，$j_{<t}$ 为前序 token 序列。从生成的 $j$ 中可提取预测偏好标签 $\hat{l}$，整体优化目标为最大化预测准确率的期望：

$$\max_{r_{\theta}} \mathbb{E}_{(x,y_a,y_b,l)\sim\mathcal{D}, \hat{l}\sim r_{\theta}(j|x,y_a,y_b)} [\mathbb{1}(\hat{l}=l)] \tag{3}$$

### 推理蒸馏阶段

蒸馏阶段的核心是构造高质量的推理轨迹作为监督信号。对于每个偏好样本，将教师模型生成的推理链 $r^{(i)}$ 与真实标签 $l^{(i)}$ 拼接，形成训练目标：

$$y_{\mathrm{trace}}^{(i)} = r^{(i)} \oplus l^{(i)} \tag{4}$$

蒸馏损失为标准的下一个 token 预测的负对数似然：

$$\mathcal{L}_{\mathrm{distill}}(\theta) = - \sum_{(x,y)\in\mathcal{D}_{\mathrm{distill}}} \sum_{t\in[|y|]} \log r_{\theta}(y_t | x, y_{<t}) \tag{6}$$

此阶段使指令模型初步具备推理能力，进化为推理奖励模型（REASRM）。但蒸馏后的模型易过拟合到训练数据的表面模式，因此需要后续的强化学习阶段来提升泛化性。

### 强化学习阶段

RL 阶段采用带 KL 正则的期望奖励最大化目标：

$$\max_{r_{\theta}} \mathbb{E}[\mathcal{R}(x,j)] - \beta \mathbb{D}_{\mathrm{KL}}(r_{\theta} \| r_{\mathrm{ref}}) \tag{7}$$

其中 $r_{\mathrm{ref}}$ 为蒸馏后的参考模型，$\beta$ 控制策略偏移的惩罚强度。

**奖励函数**的设计极为精简——仅依据预测正确性，不设格式奖励：

$$\mathcal{R}(x,j|y_a,y_b) = \begin{cases} 1 & \text{if } \hat{l}=l \\ -1 & \text{otherwise} \end{cases} \tag{8}$$

这一选择源于实验观察：格式奖励会引入噪声信号，干扰模型对内容实质的关注。

**优化算法**采用 Group Relative Policy Optimization（GRPO）。对于每组 $G$ 个采样输出，计算组内归一化的优势函数：

$$\hat{A}_i = \frac{r_i - \mathrm{mean}(\{r_1,\dots,r_G\})}{\mathrm{std}(\{r_1,\dots,r_G\})} \tag{11}$$

GRPO 通过组内相对比较而非绝对奖励值来更新策略，有效降低了奖励尺度波动对训练稳定性的影响。

### 链式评分准则推理

在推理时，RM‑R1 通过链式评分准则（Chain‑of‑Rubrics, CoR）生成结构化的中间推理。系统提示（Figure 3）指导模型先将输入分类为 Chat 或 Reasoning 类型，再分别采用不同策略：

- **Chat 类型**：自生成评分 rubric，逐条对照评估两个响应的优劣
- **Reasoning 类型**（数学/代码等）：先自行求解问题，再基于求解结果评判候选响应的正确性

这一分类决策（Query Classification, QC）对推理密集型任务尤为关键。消融实验（Table 2）表明，加入 QC 后 Reasoning 子集准确率从 94.2 跃升至 96.3，验证了任务感知的推理策略设计的必要性。



## 实验与关键发现

### 核心瓶颈与训练范式验证

RM‑R1的核心假设是：现有生成式奖励模型（GenRM）缺乏深度推理能力，往往依赖表面模式而非内容实质进行偏好判断，导致在复杂场景下评估不可靠。为验证这一假设，作者设计了一套“蒸馏→强化学习”的两阶段训练范式，并通过系统的消融实验量化各组件的贡献。

**推理训练的必要性。** 表3直接对比了纯监督微调（SFT）与推理训练（蒸馏+RL）的差异。在全量数据设定下，RM‑R1的平均得分（81.2）显著高于Instruct+SFT（77.4），提升幅度达3.8个百分点。更具说服力的是，即使在仅使用9k蒸馏数据的极端条件下，Instruct+Distilled（79.2）也大幅超越同等数据量下的Instruct+SFT（76.6），甚至逼近全量SFT的性能。这组对比清晰地表明：**高质量推理链的引入，而非单纯的数据规模，是性能提升的关键因果杠杆。**

**各组件贡献的逐层拆解。** 表2在RewardBench上对设计选择进行了精细的消融。以指令模型为起点（Avg 86.3），冷启动RL（Cold Start RL）带来+3.7的平均提升，主要来自推理子集的大幅改善（86.3→94.2）。在此基础上，引入链式评分准则（+Rubrics）使Chat Hard子集从46.6提升至49.5，整体平均分再增0.6。任务类型分类（+QC）的加入将推理准确率从94.2推至96.3，平均分达到90.8。最终，蒸馏预训练（RM‑R1）将平均分进一步提升至91.4，验证了“先蒸馏后RL”范式的必要性——**纯RL无法弥补缺少高质量推理种子带来的上限瓶颈。**

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_1ZqJ6jj75q/figures/005_Table_2.jpg]]
*Table 2: Ablation study of the design choices for Reasoning Training on RewardBench*

### 主实验结果与基线对比

表1汇总了RM‑R1与三类基线模型在三个基准上的对比。RM‑R1‑Qwen‑Instruct‑32B以81.2的平均分超越最佳标量模型INF‑ORM‑Llama3.1‑70B（78.8）和最佳生成式模型GPT‑4o‑0806（77.7），相对提升分别为+2.4和+3.5。值得注意的是，RM‑R1‑DeepSeek‑Distilled‑Qwen‑14B（79.6）仅以14B参数量即超越GPT‑4o，表明推理能力的注入可以在较小模型上实现高效的知识压缩。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_1ZqJ6jj75q/figures/004_Table_1.jpg]]
*Table 1: The performance comparison between best-performing baselines. Bold numbers indicate the best performance, Underlined numbers indicate the second best. The DeepSeek-GRM models are not open-weighted, so we use the numbers on their tech report. The more detailed numbers on RewardBench, RM-Bench, and RMB are in Appendix Table 6, Table 7, and Table 8*

在领域细分上，RM‑Bench的结果（表7）进一步揭示了推理增强的差异化收益。RM‑R1‑DeepSeek‑Distilled‑Qwen‑32B在Math子集上达到91.8%的准确率，远超Gemini‑1.5‑pro（75.2）和GPT‑4o（74.3）；在Code子集上以74.1%领先所有基线；Safety子集上95.4%的表现同样最优。这些推理密集型任务恰恰是传统标量模型和生成式模型的薄弱环节，印证了链式评分准则中“先自行求解再评判”策略的有效性。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_1ZqJ6jj75q/figures/017_Table_7.jpg]]
*Table 7: The full results of tested reward models on RM-Bench. Chat, Math, Code, Safety show the model’s Average Accuracy on each domain. Easy, Normal, Hard show the model’s Accuracy on each difficulty level across all domains. Bold numbers indicate the best performance, Underlined numbers indicate the second best*

### 扩展效应与训练动态

**模型规模扩展。** 图4a展示了不同规模基座模型在推理训练后的相对提升。趋势近似线性：更大模型从推理训练中获益更多。这一现象与蒸馏阶段引入的推理链质量相关——更强的基座模型能更有效地内化教师推理模式，并在RL阶段释放更大的优化空间。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_1ZqJ6jj75q/figures/008_Figure_4.jpg]]
*Figure 4: Scaling effect of RM-R1. (a) Larger models benefit more from reasoning training. (b) Longer reasoning chains improve RM performance. Table 3: Comparison of reasoning-based training versus SFT across benchmarks. * indicates reasoning-based methods. Reasoning training consistently yields better performance*

**推理计算量扩展。** 图4b揭示了推理链长度与性能的正相关关系。在训练时匹配推理预算的条件下，增加推理token预算持续提升评估准确率。这为实际部署提供了“以计算换准确率”的灵活权衡依据，但也凸显了推理开销显著高于标量模型这一部署限制。

**训练稳定性对比。** 图5对比了冷启动RL与热启动RL（蒸馏后）的训练动态。冷启动RL（图5a）的响应长度虽持续增长，但训练后期奖励曲线出现急剧下降，表明模型在缺乏推理先验时容易陷入不稳定优化。相比之下，热启动RL（图5b）的训练过程更为平稳，推理链在RL阶段逐步精炼而非突变，验证了蒸馏作为“推理锚点”对稳定RL训练的关键作用。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_1ZqJ6jj75q/figures/012_Figure_5.jpg]]
*Figure 5: RL training dynamics under different settings: (a) Cold Start RL (Eq. 11) and (b) Warm Start RL (Eq. 8). In Cold Start RL, the response length steadily increases as the model learns to reason, but training becomes unstable near the end. In Warm Start RL, the model exhibits more stable training, with effective refinement of reasoning traces throughout the process*

### 失败模式与公平性警示

尽管RM‑R1在多数基准上表现优异，但RewardBench完整结果（表6）显示，标量模型INF‑ORM‑Llama3.1‑70B的总体分数（95.1）仍略高于RM‑R1（91.4），说明**推理增强并非在所有子场景下都是最优策略**——在偏好信号明确、无需深度推理的简单样本上，推理链的生成可能引入噪声或冗余。

此外，表6中以✥标记的Skywork‑Reward‑Gemma‑2‑27B存在训练数据与测试集重叠的潜在污染，其异常高分不应作为公平比较的参照。RM‑R1默认使用较长推理链，在与不生成推理的标量模型对比时未统一控制推理预算，这一差异在解读“超越更大模型”的结论时需加以注意。



## 定位与知识库关联

### 核心洞察：将奖励建模重新定义为推理任务

RM-R1 的根本洞察在于识别出当前生成式奖励模型（Generative Reward Model, GenRM）的核心瓶颈：**模型倾向于依赖表面模式而非内容实质进行偏好判断**，缺乏对复杂样本的深度推理能力。这一瓶颈导致现有模型在需要细粒度语义理解或逻辑验证的场景下表现不可靠。RM-R1 的因果调控旋钮是将奖励建模重新定义为推理任务——通过链式评分准则（Chain-of-Rubrics, CoR）让模型在评分前先进行长链推理，再基于推理结果做出判断。

### 方法谱系定位

RM-R1 处于**推理增强型生成式奖励模型（REASRM）**这一新兴子领域，其方法谱系可沿三个维度展开：

**（1）奖励模型的范式演进：标量 → 生成式 → 推理增强**

传统奖励建模以标量奖励模型（ScalarRM）为主流，代表性工作如 **INF-ORM-Llama3.1-70B**，通过回归头输出单一偏好分数。生成式奖励模型（GenRM）将奖励建模转化为文本生成任务，代表性工作包括 **GPT-4o-0806** 和 **Gemini-1.5-pro** 等闭源模型，以及 **Self-taught-evaluator-llama3.1-70B** 等开源推理增强模型。RM-R1 在此基础上进一步引入结构化推理链，属于推理增强型奖励模型（REASRM）的最新进展。

**（2）推理增强策略：CoR 的差异化设计**

与现有推理增强方法相比，RM-R1 的 CoR 机制具有两个关键差异化设计：

- **任务类型自适应推理**：将输入样本分类为 Chat 类型和 Reasoning 类型。对 Chat 类型，模型生成评分准则（rubric）并对标评估；对 Reasoning 类型（数学/代码），模型先自行求解再评判。这种分类引导的推理策略（Query Classification, QC）在 RewardBench 推理子集上将准确率从 94.2 提升至 96.3（Table 2）。
- **纯正确性奖励信号**：RL 阶段仅使用基于预测正确性的二值奖励（±1），不设格式奖励。这与多数 RL 训练中依赖格式奖励的做法形成对比，避免了模型为迎合格式奖励而产生表面合规但内容空洞的推理链。

**（3）训练范式：蒸馏→RL 两阶段的必要性**

RM-R1 的训练范式由推理蒸馏（Reasoning Distillation）和 GRPO 强化学习两阶段构成。消融实验（Table 2）揭示了各阶段的作用边界：

- **纯 RL 冷启动不足**：Cold Start RL 仅将平均分从基础指令模型的 86.4 提升至 90.1，且训练后期不稳定（Figure 5a），响应长度持续增长但奖励曲线出现急剧下降。
- **蒸馏提供关键初始化**：仅使用 9k 蒸馏数据即可将 Instruct+SFT (9k) 的 76.6 提升至 Instruct+Distilled (9k) 的 79.2（Table 3），证明高质量推理链的预训练比同等规模 SFT 数据更高效。
- **RL 克服蒸馏过拟合**：蒸馏模型易过拟合到训练数据的特定模式，RL 阶段进一步将平均分从 90.8 提升至 91.4（Table 2），且在 Warm Start 下训练更稳定（Figure 5b），推理链逐步精炼而非单纯变长。

### 适用边界与局限

**（1）推理开销与部署约束**

RM-R1 的推理链生成大幅增加推断计算量。在主实验中，RM-R1 默认使用较长推理链，其推理开销显著高于不生成推理的标量奖励模型，但比较中未统一控制推理预算。尽管 Figure 4b 显示性能随推理计算预算增加而单调提升，实际部署时需要在准确率与延迟之间进行权衡。对于对延迟敏感的在线 RLHF 场景，这一开销可能构成瓶颈。

**（2）基准覆盖与泛化风险**

当前评估仅覆盖 RewardBench、RM-Bench、RMB 三个现有基准。这些基准的偏好判断类型（Chat/Chat Hard/Safety/Reasoning）可能无法充分代表真实场景中的偏好多样性。论文未在更开放或对抗性的偏好判断场景下验证模型鲁棒性。此外，部分基线模型（如 Skywork-Reward-Gemma-2-27B）被标记为可能存在训练数据与测试集重叠（✥），影响比较的公平性。

**（3）标量模型的局部优势**

在 RewardBench 上，标量模型 INF-ORM-Llama3.1-70B 的总体分数（95.1）仍略高于 RM-R1-DEEPSEEK-DISTILLED-QWEN-32B（94.4，Table 6），说明推理增强并非在所有子场景下都是最优策略。这可能与标量模型在该基准特定子集上的训练数据优势有关，也可能反映某些简单偏好判断任务不需要深度推理。

**（4）模态与场景限制**

当前工作未涉及多模态或智能体场景下的奖励建模。CoR 机制中的任务类型分类（Chat vs Reasoning）和评分准则生成策略是否可扩展到视觉、代码执行轨迹等多模态输入尚未验证。

### 开放问题

1. **评分准则的跨模态扩展**：链式评分准则能否扩展到多模态/智能体任务，使推理奖励模型处理视觉内容、交互轨迹等更丰富的输入？

2. **主动偏好收集的触发机制**：当模型生成的评分准则不足以做出可靠判断时，能否自动触发人类标注进行主动偏好收集（active preference collection），进一步提升模型在分布外样本上的稳健性？

3. **推理链的在线 RLHF 复用**：推理奖励模型生成的细粒度评分准则是否可以直接用于 RLHF 在线训练，替代传统的标量奖励信号，为策略模型提供更可解释的反馈？

4. **任务分类提示的统一化**：当前 CoR 依赖显式的任务类型分类提示来区分 Chat 和 Reasoning 的推理策略，这一分类是否可以被模型隐式学习，从而消除对人工分类提示的依赖？

5. **推理预算的自适应分配**：Figure 4b 显示性能随推理预算增加而提升，但如何根据样本难度自适应分配推理预算，避免在简单样本上浪费计算资源，仍是一个开放问题。



## 原文 PDF

![[paperPDFs/ICLR_2026/RM_R1_Reward_Modeling_as_Reasoning.pdf]]
