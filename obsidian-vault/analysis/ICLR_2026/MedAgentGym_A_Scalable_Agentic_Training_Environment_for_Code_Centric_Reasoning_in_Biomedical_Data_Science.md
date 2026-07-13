---
title: "MedAgentGym: A Scalable Agentic Training Environment for Code-Centric Reasoning in Biomedical Data Science"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/MedAgentGym_A_Scalable_Agentic_Training_Environment_for_Code_Centric_Reasoning_in_Biomedical_Data_Science.pdf
project_link: https://huggingface.co/MedAgentGym
code_link: https://github.com/wshi83/MedAgentGym
openreview_forum_id: jHDZEUgS4r
aliases:
- MMC
- MedAgentGym
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "构建统一的、可执行、带验证反馈的Docker沙箱环境，并结合在线强化学习（特别是GRPO）训练LLM智能体，能够系统性地提升开源模型的生物医学编码与推理性能。"
primary_logic: "将生物医学数据科学任务转化为可验证的代码生成问题，并在同一交互环境中联合优化编码能力与医学领域推理，是弥合开源模型与商业模型之间性能差距的关键路径。"
claims:
- "对29个LLM的基准测试显示，商业API模型与开源模型在MedAgentGym上存在巨大性能差距（Figure 1）。"
- "Med-Copilot-7B通过离线RL和在线RL分别获得+43.02%和+45.28%的性能提升，达到与gpt-4o可比的水准（Abstract）。"
- "GRPO训练将Qwen2.5-7B平均得分从16.89%提升至62.17%，接近gpt-4.1-mini的61.72%（Table 4）。"
- "在分布外任务上，Med-Copilot-14B（GRPO）平均得分47.02%，较其骨干模型提升+19.10%（Table 5）。"
---

# MedAgentGym: A Scalable Agentic Training Environment for Code-Centric Reasoning in Biomedical Data Science

> [!tip] 核心洞察
> 将生物医学数据科学任务转化为可验证的代码生成问题，并在同一交互环境中联合优化编码能力与医学领域推理，是弥合开源模型与商业模型之间性能差距的关键路径。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MedAgentGym：面向生物医学代码推理的可扩展智能体训练环境 |
| 英文题名 | MedAgentGym: A Scalable Agentic Training Environment for Code-Centric Reasoning in Biomedical Data Science |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=jHDZEUgS4r) · [GitHub](https://github.com/wshi83/MedAgentGym) · [Project](https://huggingface.co/MedAgentGym) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | MedAgentGym (训练环境) + Med-Copilot (训练智能体) |
| Dataset | MedAgentGym (In-Distribution, 8 datasets), EHRSHOT (ML coding, In-Distribution), MedAgentGym (Out-of-Distribution, 4 datasets) |

> [!tip] 效果简介
> - MedAgentGym (In-Distribution, 8 datasets) 上，Avg. Score 为 Med-Copilot-7B + GRPO: 62.17，对比 Qwen2.5-7B-Instruct (base): 16.89，变化 +45.28。
> - MedAgentGym (In-Distribution, 8 datasets) 上，Avg. Score 为 Med-Copilot-14B + GRPO: 71.42，对比 Qwen2.5-14B-Instruct (base): 20.12，变化 +51.30。
> - EHRSHOT (ML coding, In-Distribution) 上，Accuracy 为 Med-Copilot-14B + GRPO: 92.33，对比 Qwen2.5-14B-Instruct: 4.45，变化 +87.88。

## 概要

生物医学数据科学正日益依赖代码生成、执行与验证的闭环能力，然而**开源大型语言模型（LLM）在此类任务上表现显著落后于商业API模型**，且现有基准缺乏统一的、可执行、交互式训练环境，难以系统性地提升代码中心推理能力。MedAgentGym 正是针对这一瓶颈而构建：它将12个真实生物医学场景中的72,413个任务实例封装进可执行的Docker沙箱环境，提供交互式反馈与可验证的真值标注，从而将生物医学推理转化为可验证的代码生成问题。

其核心洞见在于：**在同一交互环境中联合优化编码能力与医学领域推理，是弥合开源模型与商业模型之间性能差距的关键路径**。基于此环境，作者训练了Med-Copilot智能体，采用两阶段微调策略（SFT预热后接离线/在线强化学习），并利用GRPO等在线RL方法实现大规模轨迹采样与自我改进。

关键实验结果如下：
- **零样本基准测试**：29个LLM的评估揭示了商业API模型与开源模型之间存在巨大性能鸿沟（Figure 1）。
- **训练增益**：Med-Copilot-7B通过离线RL和在线RL分别获得+43.02%和+45.28%的性能提升，达到与gpt-4o可比的水准。
- **GRPO突破**：GRPO训练将Qwen2.5-7B平均得分从16.89%提升至62.17%，接近gpt-4.1-mini的61.72%（Table 4）。
- **分布外泛化**：在外部OOD任务上，Med-Copilot-14B（GRPO）平均得分47.02%，较其骨干模型提升+19.10%（Table 5）。

这些结果表明，通过可执行环境与强化学习的结合，开源模型能够在生物医学代码推理任务上实现数量级的性能跃升，为隐私保护、可负担的医疗AI智能体发展提供了可行的技术路径。

### 生物医学数据科学的编码推理困境

生物医学数据科学正面临一个关键瓶颈：**开源大型语言模型（LLM）在需要代码生成、执行与验证的复杂任务上，表现显著落后于商业API模型**。对29个LLM的基准测试揭示了两类模型之间存在巨大的性能鸿沟（Figure 1），这一差距在生物医学软件工程和预测建模等任务上尤为突出。尽管商业模型性能优越，但其闭源特性、高昂的推理成本和潜在的数据隐私风险，严重限制了在真实临床环境中的部署。

造成这一困境的深层原因在于，现有生物医学推理基准普遍缺乏一个**统一的、可执行、带验证反馈的交互式训练环境**。传统方法将任务简化为静态问答对，LLM仅需生成终端文本答案，完全绕过了代码执行和迭代调试这一核心环节。这种“纸上谈兵”的评估范式，无法有效提升模型在真实数据科学工作流中的编码与推理能力。

### 现有基准的结构性缺陷

表1的系统性对比揭示了当前生物医学推理与编码数据集的三个关键缺口：

1. **缺乏可执行环境**：多数数据集仅提供文本问题描述和参考答案，不提供代码执行沙箱，无法验证生成代码的正确性。模型无法获得编译错误、运行时异常等关键反馈信号。
2. **任务类型单一**：现有基准通常聚焦于单一领域（如数据库查询或生物信息学），缺乏覆盖数据库、数据分析、生物信息学和机器学习等多元场景的统一框架。
3. **无法支撑训练**：由于缺少交互式轨迹采样机制，这些数据集仅能用于零样本评估，无法为LLM智能体的系统性微调提供训练信号。

### 核心洞察：代码即推理媒介

本文的核心洞察在于，**将生物医学数据科学任务转化为可验证的代码生成问题，并在同一交互环境中联合优化编码能力与医学领域推理**，是弥合开源模型与商业模型之间性能差距的关键路径。这一洞察基于以下事实：

- 生物医学数据科学的核心工作流（数据检索、转换、分析、建模）本质上都是编码任务，代码执行结果提供了天然的正确性验证信号。
- 通过Docker容器化的可执行沙箱，可以将编译时和运行时错误系统性地转换为自然语言反馈，使LLM能够像人类数据科学家一样进行迭代调试。
- 成功和失败的代码轨迹均可作为训练信号：正例提供模仿学习目标，负例（含错误信息）为偏好优化和强化学习提供对比数据。

基于这一洞察，本文提出了**MedAgentGym**——一个面向生物医学代码推理的可扩展智能体训练环境，以及在其上训练的**Med-Copilot**系列模型。该框架旨在系统性地回答一个核心问题：能否通过统一的交互式训练环境，让开源模型在生物医学编码推理任务上达到甚至超越商业API模型的水平？

## 核心方法与创新机理

MedAgentGym 的核心创新在于将生物医学数据科学任务系统性地重构为**可验证的代码生成问题**，并为此构建了统一的交互式训练环境。相较于现有基准仅提供静态问答对或缺乏代码执行反馈，MedAgentGym 通过以下关键设计变更实现了范式跃迁：

### 从静态评估到可执行交互环境

传统生物医学编码基准（如 BioCoder、BioDS-Bench）仅提供问题描述与参考答案，模型输出后无法获得编译/运行时反馈。MedAgentGym 将每个任务封装进**隔离的 Docker 沙箱**，预装领域依赖库（如 MIMIC-III 数据处理工具、临床计算包），使 LLM 智能体能够实际执行代码并获取执行结果。这一变更的因果效应体现在：编译时和运行时错误被系统性地转化为**统一自然语言格式**的调试信息，使模型能够进行多轮迭代修正（Figure 6 消融实验证实，移除调试功能会显著降低所有任务上的性能）。

### 从单轮推理到 POMDP 多轮交互

MedAgentGym 将交互过程建模为**部分可观测马尔可夫决策过程（POMDP）**，定义了四种主要动作类型：
- `request_info`：请求额外数据信息
- `terminal`：执行终端命令
- `code_execution`：生成并执行代码
- `debugging`：基于错误反馈进行调试

这一设计使智能体不再是单次推理的“黑箱”，而是能够在观察-行动循环中逐步逼近正确解。配合 Ray/Joblib 多线程并行引擎，系统可高效采样大规模多轮轨迹，为后续强化学习提供训练信号。

### 从零样本评估到两阶段智能体训练

MedAgentGym 不仅是一个基准，更是一个**训练环境**。其训练流程包含三个关键层次：

1. **SFT 预热**：使用 gpt-4.1-mini 采样的 2,137 条成功轨迹进行监督微调，使开源模型初步掌握代码生成与调试的基本模式。
2. **离线偏好优化（DPO）**：利用 1,646 条 off-policy 和 2,939 条 on-policy 偏好对进行偏好对齐，特别擅长提升开放式任务（如临床预测建模）的性能。
3. **在线强化学习（PPO/GRPO）**：以正确性奖励和格式奖励为信号，让模型在真实环境中通过自我探索持续改进。其中 GRPO（Group Relative Policy Optimization）表现最优，将 Qwen2.5-7B 的平均得分从 16.89% 提升至 62.17%，接近 gpt-4.1-mini 的 61.72%。

### 从单一正确性到轨迹级验证

MedAgentGym 引入了**结果验证器（Outcome Verifier）**，训练一个输出监督奖励模型（ORM）预测轨迹成功概率 $r = \exp(l_y) / (\exp(l_y) + \exp(l_n))$。这一设计支撑了 Best@K 采样策略：在推理时生成多条轨迹，由验证器选择最可能成功的解，使 Pass@1 从 17.0% 提升至 Best@16 的 41.7%（Figure 4）。

### 关键消融发现

- **SFT 预热对 DPO 至关重要**：SFT+DPO 比单独 DPO 平均分数提升约 5-6 个百分点（Table 10），说明先让模型学习“怎么做”再学习“哪个更好”是有效的课程设计。
- **重复动作惩罚反而有害**：对 GRPO 施加重复动作惩罚导致性能从 62.17% 降至 56.98%（Table 13），因为抑制了有益的自我调试行为——这一反直觉发现揭示了生物医学编码场景中“试错”的独特价值。
- **预定义工具集限制灵活性**：在 MIMIC-III 任务上为 GPT-4 代理提供预定义函数工具集反而导致性能下降（Figure 11），表明不受约束时 LLM 能生成更贴合上下文的代码。

综上，MedAgentGym 通过“可执行沙箱 + POMDP 交互 + 两阶段 RL 训练 + 轨迹验证器”的组合创新，系统性地弥合了开源模型与商业 API 在生物医学代码推理上的性能鸿沟。

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_jHDZEUgS4r/figures/005_Figure_2.jpg]]
*Figure 2: Overview of MedAgentGym. MedAgentGym contains a comprehensive suite of coding-centric biomedical data science tasks with an interactive execution environment for LLM agents*

MedAgentGym 构建了一个统一的、可执行的生物医学数据科学智能体训练环境，其核心设计理念是将多样化的生物医学任务转化为**可验证的代码生成问题**，并在同一交互环境中联合优化编码能力与医学领域推理。整个系统由五个紧密协作的功能模块构成，形成从数据构建到智能体训练再到结果验证的完整闭环。

### 任务与数据构建模块

该模块负责整合来自 12 个真实生物医学场景的 72,413 个任务实例，覆盖 129 个细分类别。数据来源包括 MIMIC-III、eICU、TREQS、MedCalcBench、BioCoder、EHRSHOT、BioDS-Bench 等临床与生物信息学数据集（Table 2）。每个实例被标准化为三个组成部分：问题描述、可验证的真值输出以及可选的数据资源（如电子健康记录）。这一标准化过程将数据库查询、数据分析、生物信息学计算、机器学习建模等异构任务统一为“生成代码—执行验证”的范式。

### 可执行沙箱环境

MedAgentGym 为每个任务提供基于 Docker 容器的隔离执行环境（Figure 2），预装任务所需的生物医学依赖库，确保环境一致性与数据安全。该设计解决了现有生物医学基准缺乏统一可执行环境的瓶颈——以往的数据集多为静态问答对，无法支持代码的实际运行与验证（Table 1 对比了相关工作）。沙箱环境支持多线程并行执行与顺序采样，为大规模轨迹生成提供了工程基础。

### 交互式反馈与调试模块

系统将 LLM 的输出格式化为结构化 JSON，便于解析和代码执行。编译时和运行时错误消息被系统性地转换为统一的自然语言格式，使 LLM 能够理解并迭代修正代码。这一设计是性能提升的关键机制之一：消融实验表明，去除调试功能会显著降低模型在所有任务上的性能（Figure 6）。

交互过程被建模为部分可观测马尔可夫决策过程（POMDP），定义了四种主要动作类型：
- **request_info**：请求额外信息
- **terminal**：终端操作
- **code_execution**：代码执行
- **debugging**：基于错误反馈进行调试

### 轨迹采样与并行引擎

为支持大规模训练数据生成，系统集成了 Ray 和 Joblib 两种多线程后端引擎，实现高效的轨迹采样。在训练 Med-Copilot 时，作者使用 gpt-4.1-mini（温度设为 0）采样了 2,137 条成功轨迹用于 SFT 预热，同时准备了 1,646 条离策略（off-policy）偏好对和 2,939 条同策略（on-policy）偏好对用于后续的 DPO 训练。

### 智能体训练流程

训练采用两阶段微调框架（Figure 3）：
1. **SFT 预热阶段**：在成功轨迹上进行监督微调，使模型初步掌握代码生成和交互的基本能力。仅 SFT 即可将 Qwen2.5-7B-Instruct 的平均得分从 16.89% 提升至 53.87%（Table 4）。
2. **RL 精炼阶段**：支持离线 RL（DPO）和在线 RL（PPO/GRPO）。在线 RL 使用两个奖励信号——正确性奖励（代码执行结果是否匹配真值）和格式奖励（输出是否符合 JSON 规范）。GRPO 最终将 7B 骨干模型的平均得分推升至 62.17%，14B 模型达到 71.42%（Table 4）。

### 结果验证器

系统训练了一个结果监督的奖励模型（ORM），用于预测给定轨迹成功解决编码任务的概率。验证器将任务形式化为二分类问题，利用 YES/NO 的 logit 计算轨迹成功概率：

$$r = \exp(l_y) / (\exp(l_y) + \exp(l_n))$$

验证器训练数据结合了来自 gpt-4.1-mini 的离策略轨迹（2,742 条）和同策略轨迹（2,939 条）。该验证器不仅服务于 Best@K 采样策略（在 K=16 时 Pass@K 从 17.0% 提升至 45.0%，Best@K 达到 41.7%，Figure 4），还支持模型的自我改进循环（Figure 5）。

### 数据流与模块关系

整个系统的数据流可概括为：**任务实例 → Docker 沙箱执行 → 轨迹采样（正/负样本）→ SFT 预热 → RL 精炼（DPO/PPO/GRPO）→ 验证器评估**。各模块之间形成反馈闭环：沙箱环境产生的执行结果和错误信息直接驱动 RL 的奖励计算，验证器的预测概率则指导推理时的采样策略和训练时的自我改进。这种“执行—反馈—学习”的一体化设计是 MedAgentGym 区别于现有静态基准的核心特征。

### 3.1 编码推理的形式化与验证函数

MedAgentGym 将生物医学数据科学任务统一形式化为可验证的代码生成问题。给定问题描述 $x \in \mathcal{X}$，目标是生成代码片段 $c \in \mathcal{C}$，使其执行输出 $y \in \mathcal{Y}$ 与真值 $y^{*}$ 一致。验证函数定义为：

$$\mathcal{E} : \mathcal{C} \times \mathcal{Y} \rightarrow \{0,1\}$$

对于具有显式真值的任务（数据库查询、数据分析、生物信息学），验证函数简化为指示函数：

$$\mathcal{E} = \mathbb{I}(y = y^{*})$$

即当生成输出与真值完全匹配时返回1，否则返回0。对于开放式任务（如临床决策支持的ML编码），则采用测试用例准确率（Accuracy）作为评估指标。

基于此形式化，环境同时捕获成功轨迹 $\{c^{(i)} \mid y^{(i)} = y^{*}\}$ 和失败轨迹 $\{c^{(i)} \mid y^{(i)} \neq y^{*}\}$（含错误消息），为后续训练提供双向学习信号。

### 3.2 可执行沙箱与交互式反馈模块

环境核心由三个紧密耦合的模块构成：

**Docker隔离沙箱**：每个任务实例封装在独立的Docker容器中，预装任务所需的生物医学库和依赖项。这保证了环境一致性、可复现性及数据安全——敏感临床数据（如MIMIC-III、eICU）不会离开本地计算环境。

**结构化交互界面**：遵循 CodeAct（Wang et al., 2024a）框架，交互过程被建模为部分可观察马尔可夫决策过程（POMDP），定义四种原子动作类型：
- `request_info`：请求数据模式、表结构等上下文信息
- `terminal`：执行Shell命令（如文件操作、包安装）
- `code_execution`：提交代码并获取执行输出
- `debugging`：接收编译/运行时错误并迭代修正

LLM输出统一为结构化JSON格式，便于解析和代码提取执行。

**错误转换与调试**：编译时和运行时错误消息被系统性地转换为统一的自然语言格式，使LLM能够更有效地理解错误语义并进行迭代调试。消融实验表明，去除调试功能会导致所有任务上的性能显著下降（Figure 6）。

### 3.3 轨迹采样与并行引擎

为支持大规模训练数据生成，环境集成了Ray和Joblib两种多线程后端引擎，实现并行轨迹采样。具体而言，使用gpt-4.1-mini（temperature=0）采样了2,137条成功轨迹用于SFT预热，同时准备了1,646条离策略（off-policy）偏好对和2,939条在策略（on-policy）偏好对用于后续的DPO训练。

### 3.4 结果验证器（Outcome Verifier）

为支持Best@K采样和自我改进，训练了一个结果监督的奖励模型（ORM）。验证器任务形式化为预测给定轨迹成功解决编码任务的概率：

$$r = \frac{\exp(l_y)}{\exp(l_y) + \exp(l_n)}$$

其中 $l_y$ 和 $l_n$ 分别为验证器对"YES"和"NO"类别的logit输出。训练数据融合了离策略轨迹（gpt-4.1-mini采样的2,742条样本）和在策略轨迹（2,939条样本）。

### 3.5 强化学习训练模块

训练采用两阶段微调框架：SFT预热后接RL精炼。

**奖励设计**：在线RL（PPO和GRPO）使用两个奖励信号：
- **正确性奖励**：基于代码执行结果与真值的匹配
- **格式奖励**：确保输出符合结构化JSON格式

GRPO训练的超参数配置为：KL散度正则化系数 $\beta = 1 \times 10^{-3}$，学习率 $1 \times 10^{-5}$。值得注意的是，对重复动作施加额外惩罚反而导致性能下降（从62.17%降至56.98%），因为抑制了有益的自我调试行为（Table 13）。

## 实验与关键发现

### 零样本基准测试：商业API与开源LLM之间的巨大鸿沟

在MedAgentGym的8个分布内数据集上对29个LLM进行零样本评估（Table 3），结果揭示了两个关键发现。**第一，商业API模型与开源模型之间存在系统性性能差距**。表现最强的商业模型gpt-4.1平均得分达到70.15%，而最优开源模型Qwen3-32B仅取得48.19%，差距超过20个百分点。即使是较小规模的商业模型（如gpt-4o-mini），其性能也普遍优于同等甚至更大规模的开源模型。**第二，结构化任务与开放式任务之间存在显著难度差异**。LLM在数据库查询、医学计算等结构化任务上表现相对稳定，但在生物信息学工程（BioCoder）和预测建模（EHRSHOT）等需要复杂代码生成与调试的开放式任务上急剧下降——gpt-4.1在EHRSHOT上取得87.93%准确率，而绝大多数开源模型在该任务上的得分低于10%。

值得注意的是，**医学推理专用LLM（如HuatuoGPT-o1-7B）在代码密集型任务上普遍弱于其基础模型**，仅在知识密集型任务上略有优势。这表明现有医学推理模型的语言能力提升并未有效迁移到可执行代码生成场景。Figure 1以排行榜形式直观呈现了这一性能鸿沟，突显了构建隐私保护、可负担的开源生物医学编码智能体的紧迫性。

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_jHDZEUgS4r/figures/002_Figure_1.jpg]]
*Figure 1: Overview of (a) task-specific and (b) overall leaderboard evaluation in MedAgentGym. The results show the (a) performance variations across biomedical data science tasks and (b) large gaps between proprietary and open-source (OSS) LLMs, highlighting the need for continued development of privacy-preserving, affordable LLM agents, especially for complex code-based biomedical reasoning tasks such as biomedical software engineering and predictive modeling*

### 离线与在线强化学习：Med-Copilot的训练效果

Med-Copilot采用两阶段微调范式：首先在2,137条gpt-4.1-mini生成的成功轨迹上进行SFT预热，随后通过RL方法（DPO/PPO/GRPO）进行精细化优化。

**Table 4的核心结果**：以Qwen2.5-7B-Instruct为骨干模型（零样本平均得分16.89%）：

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_jHDZEUgS4r/figures/008_Table_4.jpg]]
*Table 4: Med-Copilot performance on MedAgentGym finetuned with sampled trajectories*

- **SFT单独训练**：平均得分提升至53.87%（+36.98个百分点），证明成功轨迹的行为克隆已能带来显著增益。
- **离线RL（DPO）**：在SFT基础上进一步使用1,646条off-policy和2,939条on-policy偏好对进行DPO训练，平均得分达到59.91%（+43.02%）。
- **在线RL（GRPO）**：采用GRPO进行在线探索与优化，平均得分飙升至62.17%（+45.28%），**接近gpt-4.1-mini的61.72%**，实现了开源7B模型与商业API模型性能的实质性弥合。

扩展到14B骨干模型（Qwen2.5-14B-Instruct，零样本20.12%），GRPO训练后的Med-Copilot-14B达到71.42%（+51.30%），**超越了gpt-4o的69.73%**。在EHRSHOT这一最具挑战性的ML编码任务上，Med-Copilot-14B（GRPO）取得92.33%准确率，而其骨干模型仅4.45%，提升幅度高达+87.88个百分点。

**关键机制差异**：SFT在结构化编码任务上提升最为显著，因为它直接模仿了正确的代码模式；而DPO通过对比正负轨迹，更擅长优化开放式任务中的代码生成策略；GRPO则通过在线探索与即时反馈，在两类任务上均实现了最优性能。

### 分布外泛化能力

在4个外部/分布外数据集上（Table 5），Med-Copilot-14B（GRPO）取得47.02%平均得分，较其骨干模型（27.92%）提升+19.10个百分点，验证了训练环境所培养的代码推理能力具有一定的任务迁移性。但需注意，分布外性能仍显著低于分布内（71.42% vs 47.02%），说明模型对特定生物医学数据格式和任务模式存在一定程度的过拟合。

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_jHDZEUgS4r/figures/014_Table_5.jpg]]
*Table 5: External test set results on MedAgentGym*

### 消融实验：关键设计选择

**调试功能的必要性**（Figure 6）：移除交互式调试（debug）能力后，模型在所有任务上的性能均显著下降。编译时和运行时错误被系统性地转换为统一自然语言格式的反馈，使LLM能够理解错误并进行迭代修正——这一机制是代码生成成功率的关键保障。

**SFT预热对DPO至关重要**（Table 10）：直接进行DPO而不经过SFT预热，7B和14B模型的平均得分分别比SFT+DPO低约5-6个百分点。SFT阶段提供的成功轨迹先验为后续偏好优化建立了有效的策略起点，单独DPO因缺乏正向引导而难以收敛到高质量策略。

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_jHDZEUgS4r/figures/028_Table_10.jpg]]
*Table 10: Effect of SFT stage in two-stage finetuning framework. Table 10 shows the effect of the initial SFT stage during agentic RL finetuning. Although DPO alone slightly underperforms compared to SFT, combining an initial SFT warm-up with subsequent DPO further improves overall results by leveraging their complementary strengths*

**奖励设计的敏感性**（Table 13）：在GRPO中对重复动作施加惩罚（reward penalty）反而导致性能下降，平均得分从62.17%降至56.98%。原因在于生物医学编码任务天然需要多轮自我调试，惩罚重复动作抑制了有益的迭代修正行为。

**预定义工具集的负面效应**（Figure 11）：为GPT-4代理提供预定义函数工具集后，其在MIMIC-III任务上的性能反而下降。不受限时LLM能生成更灵活、上下文适配度更高的代码，而预定义工具约束限制了其代码生成空间的表达能力。

### 扩展性分析

**推理时扩展**（Figure 4左）：对于Qwen2.5-7B-Instruct基础模型，Pass@K从K=1时的17.0%提升至K=16时的45.0%；结合验证器（ORM）的Best@K策略将性能进一步提升至41.7%（K=16）。验证器通过预测轨迹成功概率 $r = \exp(l_y) / (\exp(l_y) + \exp(l_n))$ 进行最优轨迹选择，在固定推理预算下显著提高了任务完成率。

**训练时扩展**（Figure 4右）：SFT性能随训练数据量增加呈现对数增长趋势，从1K样本到全量2,137样本，平均得分持续提升，未出现明显饱和，暗示更大规模轨迹采样可能带来进一步增益。

### 失败模式分析

对最强模型gpt-4.1的错误类型分布（Figure 7）分析表明，**循环相关错误（loop-related errors）**是最主要的失败模式——模型在调试过程中陷入反复生成相似错误代码的循环，无法有效跳出局部策略空间。其次为**领域知识错误**，如Figure 15所示，基线模型在染色体拷贝数计算任务中错误地将女性X染色体数硬编码为2，未能考虑非整倍体场景（如四倍体肿瘤细胞）；经过DPO训练的模型则正确实现了与倍性参数成比例的动态缩放。Figure 16进一步揭示了语义正确性错误：基线模型在代谢网络质量守恒的线性规划任务中生成了语法合理但语义错误的代码（使用Python列表而非LinearExpr对象），GRPO训练后的模型则准确使用了优化库的API约束。

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_jHDZEUgS4r/figures/026_Figure_13.jpg]]
*Figure 13: Med-Copilot SFT performance on MedAgentGym across various backbone LLMs*

## 定位与知识库关联

### 1. 核心问题定位

生物医学数据科学中代码中心推理的核心瓶颈在于：**开源大型语言模型（LLM）在需要代码生成、执行与验证的复杂任务上，与商业API模型之间存在巨大性能鸿沟**。MedAgentGym对29个LLM的零样本基准测试（Figure 1, Table 3）揭示：最强商业模型 **gpt-4.1**（OpenAI, 2025a）平均得分70.15，而最强开源模型 **Qwen3-32B** 仅48.19；在7B量级，开源模型平均得分普遍低于20%。这一差距在需要领域特定编码的任务（如生物医学软件工程、预测建模）上尤为突出。

造成这一瓶颈的深层原因并非单纯的能力不足，而是**缺乏统一的、可执行、带验证反馈的交互式训练环境**。现有生物医学推理基准（如MedQA、PubMedQA）以静态问答为主，不涉及代码执行；而现有编码基准（如HumanEval、MBPP）又缺乏生物医学领域深度。MedAgentGym通过将12个真实生物医学场景的72K+任务实例标准化为可验证编码任务，并封装于Docker沙箱中，首次构建了面向LLM智能体的生物医学编码训练环境。

### 2. 方法谱系与关键差异

MedAgentGym在方法谱系中处于**生物医学推理基准 × 代码智能体训练环境**的交叉点。Table 1系统比较了其与相关工作的差异：

| 维度 | 现有工作 | MedAgentGym |
|------|---------|-------------|
| **任务类型** | 以QA为主（MedQA, PubMedQA）或单一编码类型 | 覆盖数据库、数据分析、生物信息学、机器学习四类编码任务 |
| **执行环境** | 无或仅离线评估 | Docker隔离沙箱，预装依赖，支持实时代码执行 |
| **反馈机制** | 静态真值比对 | 编译/运行时错误自动转译为自然语言调试信息 |
| **训练支持** | 不支持或仅支持SFT | 支持大规模轨迹采样 + 两阶段微调（SFT→DPO/PPO/GRPO） |
| **交互模式** | 单次推理 | 多轮POMDP交互，支持请求信息、终端操作、代码执行、调试 |

具体而言，MedAgentGym区别于以下工作类别：

- **生物医学QA基准**（如MedQA, MedMCQA, PubMedQA）：仅评估医学知识推理，不涉及代码生成与执行。MedAgentGym强调计算密集型任务，要求智能体检索、转换、分析生物医学数据并生成可执行代码。
- **通用编码基准**（如HumanEval, MBPP, SWE-bench）：缺乏生物医学领域深度和特定库依赖（如MIMIC-III的EHR数据结构、生物信息学工具链）。
- **生物医学编码数据集**（如BioCoder, BioDS-Bench）：虽涉及生物信息学或ML编码，但不提供统一的可执行环境、交互式反馈和训练轨迹生成能力。MedAgentGym首次将这三者整合为完整的智能体训练基础设施。
- **LLM智能体框架**（如SWE-Agent, OpenHands）：面向通用软件工程，未针对生物医学数据科学的特定需求（数据隐私、临床数据库访问、领域特定错误模式）进行优化。

### 3. 技术路线选择与因果机制

MedAgentGym的设计围绕一个核心因果假设：**将生物医学数据科学任务转化为可验证的代码生成问题，并在同一交互环境中联合优化编码能力与医学领域推理，是弥合开源与商业模型性能差距的关键路径**。这一假设通过以下因果链条得到验证：

1. **环境→能力**：Docker沙箱提供的可执行环境使LLM能够通过代码执行获得即时验证信号，将原本隐式的医学推理转化为显式的、可调试的编码过程。消融实验（Figure 6）证实，去除调试功能会显著降低所有任务的性能。

2. **训练范式→性能**：两阶段微调（SFT预热→RL精炼）的设计利用了成功轨迹的模仿学习与偏好优化的互补性。SFT在结构化编码任务上提升显著，DPO更擅长优化开放式任务；SFT预热对DPO训练至关重要，SFT+DPO比单独DPO平均分数提升约5-6个百分点（Table 10）。

3. **在线RL→突破**：GRPO训练将Qwen2.5-7B从16.89%提升至62.17%（+45.28%），接近gpt-4.1-mini的61.72%（Table 4）。这一效果的关键在于在线RL允许模型在训练过程中与环境持续交互，通过正确性奖励和格式奖励的联合优化，学会有效的调试策略。值得注意的是，对重复动作施加惩罚反而降低性能（从62.17%降至56.98%，Table 13），因为抑制了有益的自我调试行为。

4. **验证器→Best@K扩展**：基于结果监督的奖励模型（ORM）通过预测轨迹成功概率 $r = \exp(l_y) / (\exp(l_y) + \exp(l_n))$，在推理时支持Best@K采样。Pass@K从K=1的17.0%提升至K=16的45.0%，Best@K达到41.7%（Figure 4左），展示了推理时扩展的潜力。

### 4. 适用边界与局限

**适用场景**：
- 基于文本/EHR的结构化数据分析和编码任务（数据库查询、数据转换、统计建模）
- 生物信息学流程自动化（序列分析、结构预测）
- 临床预测建模（ML编码，如EHRSHOT上的92.33%准确率）
- 医学计算工具开发（如MedCalcBench中的临床公式实现）

**已知局限**：
1. **小模型能力不足**：小型开源模型（<10B）的零样本性能仍然较低（如Qwen3-8B仅约30%），即使经过训练也难以达到商业API水平。论文受预算限制，未探索更大规模模型（>70B）的GRPO训练效果。
2. **多模态缺失**：当前环境仅支持文本/EHR数据，尚未集成医学影像、脑电图、音频等多模态生物医学数据，限制了在放射学、病理学等领域的应用。
3. **教师模型偏差**：训练轨迹主要来源于gpt-4.1-mini，较强的教师模型可能引入分布偏差；且采样次数有限（2,137条成功轨迹），可能低估性能方差。
4. **评估稳定性未知**：受预算限制，未能进行多轮随机评估以量化模型输出稳定性。单次评估结果可能受随机性影响。
5. **公平性未评估**：数据集主要来源于MIMIC等真实临床数据库，可能存在人口统计学偏差；论文未对模型输出的公平性进行专门评估。

### 5. 开放问题

1. **鲁棒探索机制**：如何在复杂生物医学推理任务中促进有效探索并增强鲁棒性？Figure 7显示循环相关错误（Loop-related errors）是最强模型gpt-4.1的常见错误类型之一，表明现有智能体在长程推理中容易陷入无效循环。

2. **多模态集成**：如何将多模态生物医学数据（影像、EEG、音频等）有效集成到统一的智能体训练框架中？这需要扩展Docker环境以支持GPU加速的深度学习推理，并设计跨模态的验证机制。

3. **低成本多次评估**：在多次运行评估条件下系统的不确定性特征如何？如何实现低成本、高可靠性的多次评估以量化模型输出的稳定性？

4. **深层知识约束**：除了基于执行结果的验证外，如何融入更深层的生物医学知识约束（如生理学合理性、临床指南合规性）以进一步提高代码生成质量？Figure 15和Figure 17的案例显示，即使代码可执行，仍可能存在领域概念错误（如错误使用过时的MDRD公式而非2021 CKD-EPI标准）。

5. **预定义工具集的影响**：Figure 11显示提供预定义工具集反而导致GPT-4代理性能下降，表明不受限时LLM能生成更灵活的代码。如何在提供领域知识辅助与保持代码灵活性之间取得平衡，是值得进一步研究的问题。

## 原文 PDF

![[paperPDFs/ICLR_2026/MedAgentGym_A_Scalable_Agentic_Training_Environment_for_Code_Centric_Reasoning_in_Biomedical_Data_Science.pdf]]
