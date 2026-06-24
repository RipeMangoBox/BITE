---
title: "MMedAgent-RL: Optimizing Multi-Agent Collaboration for Multimodal Medical Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/MMedAgent_RL_Optimizing_Multi_Agent_Collaboration_for_Multimodal_Medical_Reasoning.pdf
openreview_forum_id: 2awntLXwR6
aliases:
- MR
- MMedAgent-RL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "基于课程学习（Curriculum Learning）引导的强化学习策略，通过动态调节主治医生在决策时的策略熵，控制其对专家意见的信任与独立思考之间的平衡。具体通过根据专家准确率划分的课程难度（简单、中等、困难）来设定GRPO中的熵奖励系数γ_s实现。"
primary_logic: "将专家输出准确率作为难度标签构建三阶段课程，并在强化学习中动态调节策略熵，使模型能从学习信赖一致专家逐步过渡到主动纠正错误专家，从而显著提升多模态医疗推理的鲁棒性和泛化能力。"
claims:
- "MMedAgent-RL在五个医学VQA基准上显著优于所有开源和专有Med-LVLMs，平均性能提升23.6%。"
- "引入的课程多智能体强化学习（C-MARL）使主治医生更好地理解专家知识，在ID和OOD数据集上平均性能提升18.6%。"
- "经过GRPO优化的分诊医生在三个数据集的测试中准确率超过99%，近乎完美实现科室分配。"
- "在专家全部出错的困难样本上，MMedAgent-RL仍能做出正确判断，在OmniMedVQA上准确率达23.0%，相比基础模型的2.0%提升巨大。"
---

# MMedAgent-RL: Optimizing Multi-Agent Collaboration for Multimodal Medical Reasoning

> [!tip] 核心洞察
> 将专家输出准确率作为难度标签构建三阶段课程，并在强化学习中动态调节策略熵，使模型能从学习信赖一致专家逐步过渡到主动纠正错误专家，从而显著提升多模态医疗推理的鲁棒性和泛化能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MMedAgent-RL：面向多模态医学推理的多智能体协作优化 |
| 英文题名 | MMedAgent-RL: Optimizing Multi-Agent Collaboration for Multimodal Medical Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=2awntLXwR6) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | MMedAgent-RL |
| Dataset | VQA-RAD, SLAKE, PathVQA, OmniMedVQA (OOD) |

> [!tip] 效果简介
> - VQA-RAD 上，Accuracy 为 71.5，对比 SFT method，变化 +10%。
> - SLAKE 上，Accuracy 为 76.2，对比 SFT method，变化 +12%。
> - PathVQA 上，Accuracy 为 72.3，对比 SFT method，变化 +12%。

## 概述

### 问题背景

多模态医学视觉问答（Medical VQA）要求模型同时理解医学图像与文本问题，其高度专业化的特性使单一模型难以在所有子领域保持竞争力。现有医学多智能体系统（如**MedAgents** (Tang et al., 2024)、**MDAgents** (Kim et al., 2024)）虽然引入了“全科医生→专科医生→全科医生”的临床协作范式，但其交互流程是固定、静态的——主治医生对专家意见的整合策略无法根据专家输出的不一致性和可靠性差异进行动态调整。这一瓶颈导致系统在处理复杂病例时性能受限：当专家意见一致但全部错误时，模型缺乏独立纠正的能力；当专家意见分歧时，又缺乏有效的仲裁机制。

### 核心方法

**MMedAgent-RL** 提出了一种基于强化学习的动态多智能体协作框架，其核心创新在于引入**课程多智能体强化学习（C-MARL）** 来训练主治医生的决策策略。关键控制变量是策略熵——通过根据专家准确率将训练数据划分为简单、中等、困难三个课程阶段，并在 GRPO 目标函数中动态调节熵奖励系数 $\gamma_s$，使模型从早期阶段学习信赖一致专家，逐步过渡到后期阶段主动识别并纠正专家错误。这一设计将“何时信任专家、何时独立思考”的决策能力内化为可优化的策略行为，而非依赖手工规则。

### 主要结果

在五个医学 VQA 基准（VQA-RAD、SLAKE、PathVQA、OmniMedVQA、MMMU-Med）上，MMedAgent-RL 相比强基线平均性能提升 **23.6%**。其中，C-MARL 的引入在域内和域外数据集上带来 **18.6%** 的平均增益。分诊医生经 GRPO 优化后，在三个数据集的科室分配准确率均超过 **99%**，近乎完美。尤为关键的是，在专家全部出错的困难样本上，MMedAgent-RL 仍能在 OmniMedVQA 上达到 **23.0%** 的准确率，而基础模型仅为 2.0%，验证了动态熵调节赋予模型的独立纠错能力。

### 方法定位

MMedAgent-RL 处于**多模态医学推理**与**多智能体强化学习**的交叉点。与单智能体 Med-LVLM（如 **LLaVA-Med-7B** (Li et al., 2023)、**RadFM** (Wu et al., 2023)）相比，它通过多专家协作弥补单一模型的专科短板；与静态多智能体系统（如 **MedAgents**、**AFlow** (Zhang et al., 2024)）相比，它通过强化学习实现了协作策略的可训练化和动态适应。在技术路线上，该方法将课程学习作为引导强化学习探索的脚手架，为多智能体系统中的“信任校准”问题提供了一种原则性的解决方案。

## 背景与动机

### 多模态医学推理的现实需求

医学诊断本质上是一个多模态推理过程——医生需要综合影像、文本报告、实验室数据等多种信息源做出判断。近年来，多模态大语言模型（LVLMs）在通用视觉问答任务上取得了显著进展，但在医学领域，单一模型面临一个根本性瓶颈：**领域专业化不足**。一个通用LVLM难以同时精通放射学、病理学、超声诊断等差异巨大的医学子领域，导致在专业场景下性能受限。

### 现有多智能体系统的静态缺陷

为弥补单一模型的不足，研究者开始探索多智能体协作范式。现有医学多智能体系统（如 **MedAgents**，Tang et al., 2024；**MDAgents**，Kim et al., 2024；**AFlow**，Zhang et al., 2024）模拟了“全科医生→专科医生→全科医生”的临床会诊流程，但其核心缺陷在于**交互流程的固定性与静态性**：

- **固定工作流**：专科医生的选择和意见聚合方式被预设为静态规则，无法根据病例复杂度动态调整。
- **盲目信任或简单忽略**：主治医生对专家输出的处理方式粗糙，要么采用多数投票等简单聚合策略隐式信任专家，要么完全忽略专家意见——缺乏根据专家可靠性水平进行动态适应的能力。
- **对不一致性的脆弱**：当专家输出相互矛盾或全部出错时，静态系统无法有效识别并纠正错误，导致在复杂病例上性能急剧下降。

### 核心动机：从静态协作走向动态优化

本文的核心动机在于回答一个关键问题：**能否训练一个可学习的多智能体系统，使其动态地、自适应地与专家协作？** 具体而言，系统需要具备两种能力：

1. **精准分诊**：根据图像模态和病例特征，将问题路由到最相关的专科医生，而非依赖预设规则。
2. **智能综合**：主治医生在综合专家意见时，能够根据专家可靠性动态调节“信任专家”与“独立思考”之间的平衡——在专家一致正确时信赖其判断，在专家出错时主动纠正。

这一动机催生了 **MMedAgent-RL**，一个基于强化学习的多智能体框架。其核心洞察是：**将专家输出准确率作为课程难度标签，通过课程学习引导的强化学习，使主治医生从学习信赖一致专家逐步过渡到主动纠正错误专家**，从而显著提升多模态医疗推理的鲁棒性和泛化能力。

## 核心创新

MMedAgent-RL 的核心创新在于将**课程学习引导的强化学习**引入多模态医学多智能体协作框架，通过**动态调节策略熵**实现对专家意见的自适应利用，从而解决了现有医学多智能体系统在专家输出不一致、可靠性参差不齐时的性能瓶颈。

### 从静态协作到动态熵调控

现有医学多智能体系统（如 **MedAgents** (Tang et al., 2024)、**MDAgents** (Kim et al., 2024)）普遍采用固定的交互流程——全科医生（GP）接收专家意见后直接聚合或简单投票，缺乏对专家输出质量的动态感知能力。当多位专家意见冲突或全部出错时，这类静态策略无法有效应对。

MMedAgent-RL 的核心因果调控变量是**主治医生（Attending Physician）在决策时的策略熵**。其关键洞察在于：对专家意见的信任程度应随专家可靠性动态变化。具体而言，在 GRPO 目标函数中引入熵正则项：

$$
\mathcal{I}_{\mathrm{C\cdot MARL}}(\theta) = \mathbb{E}\left[\mathcal{I}_{\mathrm{GRPO}}(\theta) + \gamma_s \cdot H_t(\pi_{\theta_{\mathrm{GP}}^{\mathrm{attend}}})\right]
$$

其中熵系数 $\gamma_s$ 由三阶段课程难度 $s$ 决定：

- **简单阶段**（多数专家正确）：设置较低的 $\gamma_s$，鼓励模型信赖并模仿专家意见；
- **中等阶段**（专家意见分歧）：适度提高 $\gamma_s$，促使模型在专家意见与自身知识间寻求平衡；
- **困难阶段**（全部专家错误）：设置较高的 $\gamma_s$，推动模型突破专家误导，依赖自身推理做出独立判断。

这一设计使主治医生从“学习信赖一致专家”逐步过渡到“主动纠正错误专家”，实现了对专家知识的渐进式理解与超越。

### 相对于基线的方法槽位变更

| 方法槽位 | 基线做法 | MMedAgent-RL 做法 |
|---------|---------|------------------|
| **分诊优化** | 预定义或基于规则的固定分诊（如 MedAgents 的静态科室分配） | 使用 GRPO 训练分诊医生，基于图像模态精确选择科室，同时生成推理过程（准确率超 99%） |
| **主治医生训练** | 直接聚合专家输出（多数投票）或静态提示策略 | 通过课程多智能体强化学习（C-MARL）训练，动态调节策略熵以平衡利用与探索 |
| **专家可靠性适应** | 盲目信任或简单忽略专家输出，无法适应其准确性变化 | 基于专家准确率构建三阶段课程难度，并相应调整熵奖励系数 $\gamma_s$ |

消融实验证实了动态熵调节的必要性：移除课程学习（C-MARL）导致性能显著下降（平均降低 18.6%），而固定熵系数同样导致性能损失。在专家全部出错的困难样本上，MMedAgent-RL 在 OmniMedVQA 上达到 23.0% 的准确率，相比基础模型的 2.0% 提升了超过 10 倍，验证了模型在“纠正专家”这一核心能力上的实质性突破。

## 整体框架

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_2awntLXwR6/figures/002_Figure_2.jpg]]
*Figure 2: Overview of MMedAgent-RL, a RL-driven multi-agent framework designed for multimodal medical reasoning. It simulates the clinical loop of General Practitioner (GP) → Specialists → GP. First, MMedAgent-RL optimizes the triage doctor (the first GP) to improve triage accuracy. Then, proprietary LVLMs are used as the specialist doctors for the assigned department. Finally, curriculum learning and RL are combined to progressively train the attending physician (the second GP), who flintegrates the specialist knowledge and makes robust decisions*

MMedAgent-RL 模拟了临床诊疗中“全科医生（GP）→ 专科医生（Specialists）→ 全科医生（GP）”的闭环协作流程，并将其构建为一个可训练的强化学习多智能体框架。整个 pipeline 由三个核心模块串联构成，信息流严格按序传递，最终由主治医生输出综合诊断。

### 模块组成与信息流

**第一阶段：分诊医生（Triage Doctor）**
系统接收多模态医学输入 $x$（图像与文本问题），首先由分诊医生根据视觉信息将病例分配至合适的科室。分诊医生基于 Qwen2.5-VL 构建，使用 GRPO 进行优化，其动作选择遵循：
$$d = \arg \max_k \pi_{\theta_{\mathrm{GP}}^{\mathrm{triage}}}(k \mid x)$$
其中 $d$ 为选中的科室索引，覆盖 7 个预定义科室类别。分诊医生的奖励函数由格式奖励 $R_{\mathrm{format}} \in \{0, 0.5\}$ 和准确率奖励 $R_{\mathrm{accuracy}} \in \{0, 1\}$ 组成，训练后分诊准确率在三个测试集上均超过 99%（Table 7），近乎完美地实现了科室分配。

**第二阶段：专科医生（Specialist Doctors）**
被选中的科室对应的专科医生独立给出初步诊断意见。专科医生由专有 LVLMs（如 GPT-4o）扮演，固定使用 3 位专家，其输出遵循：
$$y_d \sim \pi_{\theta_{\mathrm{SP}}^{(d)}}(y \mid x)$$
此阶段不涉及专家间的复杂交互，每位专家仅基于自身专业知识独立生成意见 $y_d$，随后将所有专家意见汇交给下一阶段的主治医生。

**第三阶段：主治医生（Attending Physician）**
主治医生综合专科医生的意见与自身医学知识，做出最终诊断决策。这是框架的核心决策节点，其训练采用课程多智能体强化学习（C-MARL）。C-MARL 根据专家输出的准确率将训练样本划分为简单、中等、困难三个难度等级，构建三阶段课程，并在 GRPO 目标函数中引入动态熵正则项：
$$\mathcal{I}_{\mathrm{C \cdot MARL}}(\theta) = \mathbb{E}\left[\mathcal{I}_{\mathrm{GRPO}}(\theta) + \gamma_s \cdot H_t(\pi_{\theta_{\mathrm{GP}}^{\mathrm{attend}}})\right]$$
其中熵系数 $\gamma_s$ 随课程难度 $s$ 动态调节——在简单阶段鼓励模型信赖专家意见（低熵），在困难阶段鼓励独立思考以纠正专家错误（高熵），从而实现从“模仿专家”到“纠正专家”的渐进式能力跃迁。

### 训练策略

框架采用两阶段训练范式：首先独立优化分诊医生，使其具备精准的科室分配能力；随后固定分诊医生和专科医生，通过 C-MARL 训练主治医生。这种解耦设计使得各模块可独立迭代，同时保证了端到端推理时信息流的稳定性。

## 核心模块与公式推导

MMedAgent‑RL 模拟临床“全科医生→专科医生→全科医生”的闭环，将整个多智能体协作流程分解为三个可优化的核心模块：**分诊医生**、**专科医生** 和 **主治医生**。其中分诊医生与主治医生均通过强化学习训练，而专科医生为固定模型，仅负责提供独立意见。

### 分诊医生（Triage Doctor）

分诊医生接收输入 $x$（包含图像与文本），从预定义的 7 个科室中选择最匹配的科室 $d$：

$$d = \arg\max_{k} \pi_{\theta_{\mathrm{GP}}^{\mathrm{triage}}}(k \mid x)$$

训练采用 GRPO 算法，奖励函数由格式奖励 $R_{\mathrm{format}} \in \{0, 0.5\}$ 和准确率奖励 $R_{\mathrm{accuracy}} \in \{0, 1\}$ 组成。GRPO 的核心思想是利用同一输入下采样得到的 $G$ 条响应构建组内相对优势，避免训练外部价值函数。

### 专科医生（Specialist Doctors）

被选中的专科医生 $d$ 根据输入 $x$ 独立生成专家意见 $y_d$：

$$y_d \sim \pi_{\theta_{\mathrm{SP}}^{(d)}}(y \mid x)$$

框架中固定使用 3 位由专有 LVLM（如 GPT‑4o）扮演的专科医生，不参与训练，不进行交互。

### 主治医生与 C‑MARL 算法（Attending Physician & C‑MARL）

主治医生负责综合专科医生意见与自身知识做出最终诊断，其训练是 MMedAgent‑RL 的核心创新所在。基本训练框架仍为 GRPO，其目标函数为：

$$\mathcal{I}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{x, \{y_i\}} \left[ \frac{1}{G} \sum_{i=1}^{G} \left( \min\left( r_i A_i, \ \mathrm{clip}(r_i, 1-\epsilon, 1+\epsilon) A_i \right) - \beta \mathbb{D}_{\mathsf{KL}}(\pi_{\theta} || \pi_{\mathrm{ref}}) \right) \right]$$

其中：
- $r_i = \frac{\pi_{\theta}(y_i \mid x)}{\pi_{\mathrm{old}}(y_i \mid x)}$ 为当前策略与旧策略的概率比；
- $A_i = \frac{R_i - \mathrm{mean}(\{R_j\}_{j=0}^{G})}{\mathrm{std}(\{R_j\}_{j=0}^{G})}$ 为组内标准化后的优势；
- $\mathbb{D}_{\mathsf{KL}}$ 为与参考策略的 KL 散度正则项，系数 $\beta$ 控制偏离程度。

为解决专家输出质量参差不齐的问题，MMedAgent‑RL 引入**课程多智能体强化学习（C‑MARL）**，在 GRPO 目标上附加动态熵正则项：

$$\mathcal{I}_{\mathrm{C\cdot MARL}}(\theta) = \mathbb{E}\left[ \mathcal{I}_{\mathrm{GRPO}}(\theta) + \gamma_s \cdot H_t(\pi_{\theta_{\mathrm{GP}}^{\mathrm{attend}}}) \right], \quad H_t = -\sum_{j=1}^{V} p_{t,j} \log p_{t,j}$$

- $H_t$ 为主治医生策略在时间步 $t$ 的熵，$\mathbf{p}_t = \pi_{\theta}(\cdot \mid \mathcal{R}_{<t}, x; T) = \mathrm{Softmax}(\mathbf{Z}_t / \tau)$；
- $\gamma_s$ 为动态熵系数，其值随课程难度级别 $s$ 变化。

课程难度依据专家准确率划分为三个阶段（简单/中等/困难），对应不同的 $\gamma_s$ 设置：在简单阶段给予较高熵奖励以鼓励模仿专家，在困难阶段降低熵奖励以促使模型独立思考并纠正错误。这一机制使主治医生从“信任专家”逐步过渡到“批判性综合”，是实现鲁棒多模态医学推理的关键因果调节变量。

## 实验与分析

### 核心性能：多模态医学VQA全面领先

MMedAgent-RL 在五个医学视觉问答基准上展现出系统性的性能优势。**表1** 汇总了在域内（VQA-RAD、SLAKE、PathVQA）和分布外（OmniMedVQA、MMMU-Med）数据集上的对比结果。以 Qwen2.5-VL-7B 为基座的 MMedAgent-RL 在域内三个数据集上平均准确率达 73.3%，在分布外两个数据集上平均 72.6%，整体平均 73.0%。这一结果不仅大幅超越其基座模型 Qwen2.5-VL-7B（提升约 21%），也显著优于所有开源医学 LVLM 和专有模型 GPT-4o（68.6%）。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_2awntLXwR6/figures/003_Table_1.jpg]]
*Table 1: The results of the medical VQA benchmark. Here, MMMU denotes MMMU (Health & Medicine track). The best results and second best results are highlighted in red and blue , respectively. Majority voting is used for the test-time scaling (TTS)*

此外，引入测试时缩放（test-time scaling）后，通过多数投票（majority voting）机制，MMedAgent-RL 的域内平均进一步提升至 76.1%，整体平均达 76.6%，进一步拉大了与单智能体方法的差距。

**表1 关键数据速览**：
- VQA-RAD：MMedAgent-RL 达 71.5%，超过 GPT-4o 的 68.1%
- SLAKE：MMedAgent-RL 达 76.2%，超过 GPT-4o 的 74.8%
- PathVQA：MMedAgent-RL 达 72.3%，超过 GPT-4o 的 63.0%
- OmniMedVQA（OOD）：MMedAgent-RL 达 73.3%，超过 GPT-4o 的 69.2%
- MMMU-Med（OOD）：MMedAgent-RL 达 71.9%，超过 GPT-4o 的 68.2%

值得注意的是，MMedAgent-RL 在分布外数据集上的优势更为突出——相对基座模型提升 21%，相对 SFT 方法提升 23.6%，表明课程强化学习（C-MARL）赋予了主治医生更强的泛化能力，而非简单的训练集记忆。

### 消融实验：各组件的因果贡献

**表2** 和 **表12** 通过逐步叠加组件的方式，量化了框架中每个模块的独立贡献。以 Qwen2.5-VL-7B 裸模型为起点（域内平均约 59.2%，OOD 平均约 58.7%）：

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_2awntLXwR6/figures/006_Table_2.jpg]]
*Table 2: Ablation results on ID and OOD datasets*

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_2awntLXwR6/figures/017_Table_12.jpg]]
*Table 12: Performance progressively adding components*

1. **+ Specialists（专家咨询）**：引入三位专有 LVLM 专家的意见后，域内平均提升至 62.6%（+3.4%），OOD 平均提升至 61.7%（+3.0%）。这表明即使未经优化，多专家意见的简单引入已能提供有价值的信息增益。

2. **+ Triage（分诊优化）**：在专家咨询基础上加入 GRPO 训练的分诊医生，域内平均进一步提升至 64.1%（+1.5%），OOD 平均提升至 63.4%（+1.7%）。分诊医生近乎完美的科室分配能力（**表7**：VQA-RAD 99.98%、SLAKE 99.94%、PathVQA 99.06%）确保了正确的专家被激活，避免了错误科室专家的噪声干扰。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_2awntLXwR6/figures/011_Table_7.jpg]]
*Table 7: The performance of triage doctor*

3. **+ Curriculum RL（课程强化学习）**：最终加入 C-MARL 后，域内平均跃升至 73.3%（+9.2%），OOD 平均跃升至 72.6%（+9.2%）。**这是整个框架中贡献最大的单一组件**，平均性能提升达 18.6%。该结果表明，动态熵调节的课程学习策略是 MMedAgent-RL 性能突破的核心驱动力——它使主治医生从被动聚合专家意见转变为主动评估并纠正专家错误。

### 课程学习的难度分层效应

**图4** 展示了不同决策难度下的性能表现。将测试样本按专家一致程度分为三类：
- **简单样本**（所有专家一致且正确）：MMedAgent-RL 准确率接近 100%，表明模型能有效识别并信赖共识。
- **中等样本**（专家意见不一致）：MMedAgent-RL 仍保持较高准确率，显著优于无课程学习的变体，说明动态熵调节帮助模型在冲突信息中做出合理选择。
- **困难样本**（所有专家均错误）：这是最具挑战性的场景。**表9** 显示，在 OmniMedVQA 上，当所有专家都给出错误答案时，基座模型准确率仅 2.0%，而 MMedAgent-RL 达到 23.0%。这一 21% 的绝对提升是课程学习策略最直接的成效证据——经过“困难”课程阶段（低熵系数 γ_s）的训练，主治医生学会了在专家不可靠时依靠自身知识进行独立判断。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_2awntLXwR6/figures/014_Table_9.jpg]]
*Table 9: Correctness ratio (accuracy on hard samples where all specialists failed)*

### 专家配置与路由机制分析

**图3** 探索了不同专家医生配置的影响。实验表明：
- 使用三个不同科室的专有 LVLM 作为专家优于使用单一通用模型多次采样。
- 专家数量的增加（从 1 到 3）带来持续但递减的收益，三个专家在性能与计算成本间取得了良好平衡。

**表10** 对比了有无路由（triage）机制的性能差异。随机分配科室的路由方式在多数数据集上甚至劣于不使用路由的基线，这验证了精确分诊的必要性——错误的科室分配会引入不相关甚至有害的专家信息。GRPO 训练的分诊医生（**表11**）显著优于 SFT 训练版本（无论是否包含推理过程），准确率提升 2.1-7.4 个百分点，证明了强化学习在分诊任务上的独特优势。

### 测试时缩放与基线对比

**表8** 将 MMedAgent-RL 与多种测试时缩放基线进行了对比。Qwen2.5-VL-7B 的自一致性（self-consistency）方法整体平均 63.0%，GPT-4o 的自一致性方法整体平均 70.1%，而 MMedAgent-RL 单次推理即达 73.0%，使用多数投票后进一步提升至 76.6%。这表明 MMedAgent-RL 的优势并非来自简单的集成策略，而是源于训练过程中习得的动态协作能力。

### 失败模式与局限性

尽管整体性能优异，分析揭示了几个值得关注的失败模式：

1. **对专家模型质量的依赖**：**表6** 显示，当将专家从 GPT-4o 替换为较弱的开源模型时，整体性能出现明显下降。MMedAgent-RL 可以纠正专家的部分错误，但无法完全弥补专家能力的根本不足。

2. **课程难度划分的静态性**：当前课程难度依赖离线计算的专家准确率，无法在训练过程中动态调整。这意味着如果专家模型在训练期间发生变化（如 API 更新），课程标签将不再准确。

3. **少数派意见的淹没风险**：在多数投票的测试时缩放中，当仅有一位专家给出正确答案而其他两位错误时，系统可能无法识别这一少数派意见的正确性。课程学习在训练阶段部分缓解了此问题，但在推理阶段仍存在改进空间。

4. **科室覆盖的局限性**：当前分诊系统仅覆盖 7 个科室类别，对于超出此范围的医学子领域，系统可能做出错误的科室分配，进而影响后续专家选择的准确性。

5. **计算成本与外部依赖**：框架依赖 GPT-4o 等商业模型作为专家，引入了 API 调用成本和潜在的服务不稳定性。在资源受限或离线场景中，这一依赖可能成为部署瓶颈。

## 方法谱系与知识库定位

### 1. 方法在领域中的坐标

MMedAgent-RL 处于**多模态医学推理**与**多智能体协作**的交叉地带。其核心设计——模拟“全科医生→专科医生→全科医生”的临床会诊闭环——并非孤立出现，而是对两条技术路线的整合与超越：

**路线一：单智能体医学 LVLM**。以 **Med-Flamingo** (Moor et al., 2023)、**RadFM** (Wu et al., 2023)、**LLaVA-Med-7B** (Li et al., 2023) 为代表的专有医学视觉语言模型，以及 **GPT-4o** (OpenAI, 2024)、**Qwen-VL-Chat** (Bai et al., 2025)、**Yi-VL-34B** (Young et al., 2024) 等通用 LVLM，均试图通过单一模型覆盖全科室。瓶颈在于：单模型在跨领域专业知识覆盖上存在天然上限，尤其在面对罕见病或跨学科病例时，缺乏领域深度。

**路线二：静态多智能体协作**。**MedAgents** (Tang et al., 2024) 和 **MDAgents** (Kim et al., 2024) 率先将多智能体引入医学推理，但采用固定的交互流程——前者依赖预定义规则分配专家，后者通过静态提示策略聚合输出。**AFlow** (Zhang et al., 2024) 进一步探索了自动化工作流生成，但本质上仍是离线优化的静态拓扑。这些方法的共同缺陷在于：**无法动态适应专家输出质量的变化**——当专家意见一致但集体错误时，静态聚合机制会强化错误；当专家意见分歧时，缺乏可靠的信度校准手段。

MMedAgent-RL 的定位是**从“静态协作”迈向“动态优化协作”**。其关键创新不是引入多智能体本身，而是通过强化学习使主治医生学会**何时信任专家、何时独立判断**——这是一个从“固定路由”到“自适应决策”的范式跃迁。具体而言：

- **分诊医生优化**：不同于 MedAgents 的静态科室分配，MMedAgent-RL 使用 GRPO 训练分诊医生，使其根据图像模态精确选择科室并生成推理过程。在 VQA-RAD、SLAKE、PathVQA 三个基准上，分诊准确率分别达到 99.98%、99.94%、99.06%（Table 7），近乎完美。
- **主治医生训练**：不同于多数投票或直接聚合，MMedAgent-RL 通过课程多智能体强化学习（C-MARL）训练主治医生，使其在“简单样本（专家一致正确）→中等样本（专家部分正确）→困难样本（专家全部错误）”的三阶段课程中，逐步从模仿专家过渡到纠正专家错误。

### 2. 核心因果机制：动态熵调节

MMedAgent-RL 的核心因果旋钮是**基于课程难度动态调节的策略熵**。其背后的洞察是：主治医生对专家意见的“信任程度”可以通过策略熵来量化控制——高熵鼓励探索（不盲从专家），低熵鼓励利用（信赖专家）。

具体实现上，C-MARL 在标准 GRPO 目标函数中引入动态熵正则项：

$$
\mathcal{I}_{\mathrm{C\cdot MARL}}(\theta) = \mathbb{E}\left[\mathcal{I}_{\mathrm{GRPO}}(\theta) + \gamma_s \cdot H_t(\pi_{\theta_{\mathrm{GP}}^{\mathrm{attend}}})\right]
$$

其中 $H_t = -\sum_{j=1}^{V} p_{t,j} \log p_{t,j}$ 为时间步 $t$ 的策略熵，$\gamma_s$ 随课程难度 $s$ 动态设定。**在简单阶段，$\gamma_s$ 较小，模型倾向于低熵（信赖专家）；在困难阶段，$\gamma_s$ 较大，模型被鼓励高熵探索（独立思考）**。这一机制使得模型能在训练过程中自然习得“批判性采纳”的能力。

消融实验（Table 2）证实了这一设计的必要性：移除 C-MARL 后，在 ID 和 OOD 数据集上平均性能下降 18.6%。进一步地，固定熵系数或完全移除熵正则项均导致性能降低（Figure 6），验证了**动态调节**而非单纯引入熵正则才是关键。

### 3. 适用边界与约束条件

**适用场景**：该方法适用于需要**多领域专家知识协同**的医学视觉问答任务，尤其是跨科室、跨模态的复杂病例。在五个医学 VQA 基准（VQA-RAD、SLAKE、PathVQA、OmniMedVQA、MMMU-Med）上的实验结果（Table 1）表明，MMedAgent-RL 在分布内和分布外数据上均显著优于单智能体和静态多智能体基线，平均性能提升 23.6%。

**约束条件**：

1. **对商业模型的依赖**：专家医生由专有 LVLM（如 GPT-4o）扮演，这引入了 API 调用成本和模型版本迭代带来的性能不稳定性。论文未探索使用开源模型替代的可行性边界。

2. **课程难度的离线定义**：三阶段课程依赖于对专家准确率的离线预计算，无法在训练过程中动态调整难度划分。这意味着课程质量受限于离线评估的准确性，且无法适应专家模型在训练过程中的性能漂移。

3. **科室覆盖的有限性**：分诊医生仅覆盖 7 个科室类别（基于训练数据的科室分布），对于训练数据中未出现的科室，分诊泛化性未知。

4. **模型规模验证不充分**：当前仅在 7B 参数规模（Qwen2.5-VL-7B）上验证，未探索更大模型或不同架构下的性能表现和效率权衡。

### 4. 局限性与开放问题

**已识别的局限**：

- **公平性与安全性评估缺失**：论文未对模型在不同人口群体、罕见疾病类型上的表现进行公平性分析，也未评估错误诊断的潜在安全风险。这在医学领域尤为关键。
- **专家意见的多样性利用不足**：当前框架使用固定数量的 3 位专家，且主治医生的决策倾向于“多数意见”。在少数派专家正确而多数派错误的场景下，模型可能被多数投票淹没（尽管 C-MARL 在困难样本上有所缓解，Table 9 显示在专家全部错误时准确率达 23.0%，但仍有大量提升空间）。
- **两阶段训练的次优性**：分诊医生和主治医生是分阶段独立训练的，而非端到端联合优化。这可能限制了整体系统的协同潜力。

**开放问题**：

1. **在线专家场景下的课程适应**：当专家模型本身也在持续更新（如在线学习场景）时，C-MARL 的离线课程划分策略如何适应专家性能的动态变化？

2. **更广泛临床决策的泛化**：当前验证集中在医学 VQA 任务，该方法在手术规划、治疗方案推荐等更复杂的临床决策场景中的适用性如何？

3. **端到端联合优化的可能性**：能否通过联合训练分诊医生和主治医生，使分诊策略与最终诊断质量直接对齐，而非仅优化分诊准确率？

4. **少数派意见的平衡机制**：如何设计奖励函数或熵调节策略，使模型在多数专家错误时更有效地识别并采纳少数派（但正确）的意见？

5. **计算效率与部署可行性**：GRPO 训练需要为每个样本生成 8 个 rollout（训练批次大小 128），加上专家 API 调用，整体训练成本较高。在资源受限的真实临床环境中，如何权衡性能与效率？

## 原文 PDF

![[paperPDFs/ICLR_2026/MMedAgent_RL_Optimizing_Multi_Agent_Collaboration_for_Multimodal_Medical_Reasoning.pdf]]
