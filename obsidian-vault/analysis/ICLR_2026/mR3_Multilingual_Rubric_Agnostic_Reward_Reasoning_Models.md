---
title: "mR3: Multilingual Rubric-Agnostic Reward Reasoning Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/mR3_Multilingual_Rubric_Agnostic_Reward_Reasoning_Models.pdf
openreview_forum_id: ST0wOB1bdX
aliases:
- mR3
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过构建覆盖72种语言的高质量多语言训练数据，结合语言感知的提示与推理策略（ENG-ENG、TGT-ENG、TGT-TGT），以及从易到难的课程学习，显著提升模型在多语言环境下的奖励评估能力。"
primary_logic: "尽管英语仍是最强的提示和推理语言，但针对性的多语言训练可以大幅提升模型对目标语言的鲁棒性，且直接使用目标语言进行推理能在低资源语言上带来显著增益，表明高质量的跨语言推理是提升多语言评估透明度和可访问性的关键。"
claims:
- "MR3-QWEN3-14B 在多语言偏好基准上的平均准确率达到 85.04%，超过 GPT-OSS-120B 0.91 个百分点，参数量仅为后者的 1/9。"
- "MR3 的目标语言推理在人工评估中事实性得分 2.78±0.30、逻辑性得分 2.67±0.45，显著优于基座模型（QWEN3）的 2.06 和 2.05。"
- "EasyToHard 课程学习在验证集 Kendall Tau 上达到 0.4779，优于随机打乱（0.4583）和其他策略。"
- "m-RewardBench (23 languages) 上 Accuracy = MR3-QWEN3-14B: 89.18"
---

# mR3: Multilingual Rubric-Agnostic Reward Reasoning Models

> [!tip] 核心洞察
> 尽管英语仍是最强的提示和推理语言，但针对性的多语言训练可以大幅提升模型对目标语言的鲁棒性，且直接使用目标语言进行推理能在低资源语言上带来显著增益，表明高质量的跨语言推理是提升多语言评估透明度和可访问性的关键。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MR3：多语言且评分标准无关的奖励推理模型 |
| 英文题名 | mR3: Multilingual Rubric-Agnostic Reward Reasoning Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ST0wOB1bdX); [GitHub](https://github.com/rubricreward/mr3) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | MR3 |
| Dataset | m-RewardBench (23 languages), RewardBench (English), MM-Eval (18 languages), INCLUDE-base-44 (44 languages) |

> [!tip] 效果简介
> - m-RewardBench (23 languages) 上，Accuracy 为 MR3-QWEN3-14B: 89.18，对比 GPT-OSS-120B: 89.05，变化 +0.13。
> - RewardBench (English) 上，Accuracy 为 MR3-QWEN3-14B: 90.79，对比 R3-QWEN3-14B (English SFT): 91.00，变化 -0.21。
> - MM-Eval (18 languages) 上，Accuracy 为 MR3-QWEN3-14B: 86.05，对比 GPT-OSS-120B: 85.01，变化 +1.04。

## 概述

### 问题背景与瓶颈

大语言模型（LLM）的评估正从静态基准转向基于模型的自动化判断，奖励模型（Reward Model）作为评判者扮演着核心角色。然而，现有奖励模型面临两个关键瓶颈：**多语言评估能力严重不足**，非英语语言上的性能显著落后于英语；**任务格式单一**，通常仅支持成对比较，难以适配逐点评分、二元判断等多样化评估场景。多语言训练策略的系统性探索仍处于空白状态，导致低资源语言的评估透明度和可访问性受限。

### 核心方法与定位

MR3 提出了一个**大规模多语言、评分标准无关的奖励推理模型框架**，核心设计包括三个维度：

1. **语言覆盖与任务统一**：构建覆盖 72 种语言、10 万条高质量样本的训练数据集，统一支持逐点（point-wise）、成对（pair-wise）和二元（binary）三种评估任务。给定任务指令 $t$、输入 $i$、候选回答 $a$ 和评分标准 $r$，模型生成推理轨迹、简要解释 $e$ 和评分 $s$：
   $$f(x) = y, \quad \text{where } x = (t, i, a, r), \text{ and } y = (\text{trace}, e, s)$$

2. **多语言推理策略**：引入三种语言配置——英语提示+英语推理（ENG-ENG）、目标语提示+英语推理（TGT-ENG）、目标语提示+目标语推理（TGT-TGT），系统研究语言选择对推理质量的影响。

3. **知识蒸馏与课程学习**：利用强教师模型 GPT-OSS-120B 生成监督信号，结合 EasyToHard 课程学习策略（基于正确率和长度排序）进行全参数微调，优化交叉熵损失：
   $$\mathcal{L}_{\mathrm{SFT}}(\theta) = -\frac{1}{N}\sum_{i=1}^{N}\sum_{t=1}^{T_i}\log\pi_\theta\big(y_t^{(i)} \mid y_{<t}^{(i)}, x^{(i)}\big)$$

### 方法谱系与知识库定位

MR3 在现有奖励模型谱系中填补了多语言与多任务统一的空白。与 **Prometheus-7B-v2.0**（Kim et al., 2024）等早期英语评分标准法官模型相比，MR3 将语言覆盖从单一英语扩展到 72 种语言；相较于 **M-Prometheus-14B**（Pombal et al., 2025）的多语言评分标准支持，MR3 进一步融合了推理能力；与 **R3-QWEN3-14B**（Anugraha et al., 2025）的英语推理奖励模型相比，MR3 通过多语言训练策略显著提升了非英语语言的推理质量；相较于 **Nemotron-Multilingual-49B**（Wang et al., 2025c）等生成式多语言奖励模型，MR3 在参数量仅为其 1/9 的情况下实现了更优或相当的性能。

### 主要结果摘要

- **多语言偏好评估**：MR3-QWEN3-14B 在 m-RewardBench（23 种语言）上达到 89.18% 准确率，略超 GPT-OSS-120B（89.05%）；在 MM-Eval（18 种语言）上达到 86.05%，领先 1.04 个百分点；在三个多语言偏好基准上的平均准确率达 85.04%，超过 GPT-OSS-120B 0.91 个百分点。
- **推理质量**：人工评估（20 名标注者，12 种语言）显示，MR3 的目标语言推理在事实性得分（2.78±0.30）和逻辑性得分（2.67±0.45）上均显著优于基座模型 QWEN3（2.06 和 2.05）。
- **课程学习验证**：EasyToHard 策略在验证集 Kendall Tau 上达到 0.4779，优于随机打乱（0.4583）和其他课程策略。
- **英语性能保持**：在英语 RewardBench 上，MR3-QWEN3-14B 达到 90.79%，与仅用英语训练的 R3-QWEN3-14B（91.00%）差距仅 0.21 个百分点，表明多语言训练未牺牲英语核心能力。

### 局限与开放问题

尽管英语仍是最强的提示和推理语言，目标语言推理在低资源语言上的基准准确率仍低于英语推理。模型依赖强教师模型进行知识蒸馏，弱教师会导致性能大幅下降。训练数据中部分极低资源语言完全未见，跨语言泛化能力仍有提升空间。强化学习（RLVR）方法在本研究中未展现出优于纯 SFT 的效果，其潜力有待进一步挖掘。

## 背景与动机

### 多语言奖励评估的瓶颈

大型语言模型（LLM）的快速发展使得自动化评估成为对齐与迭代优化的关键环节。奖励模型（Reward Model, RM）作为评判 LLM 输出质量的核心组件，其评估能力直接影响模型对齐的上限。然而，现有奖励模型在多语言场景下面临两个根本性瓶颈：

**瓶颈一：多语言性能显著落后于英语。** 当前主流的奖励模型——无论是基于偏好的判别式模型还是生成式法官模型——其训练数据和评估基准均高度集中于英语。当面对非英语语言时，这些模型的评估准确率急剧下降，尤其在低资源语言上几乎无法提供可靠的评分信号。这使得非英语用户和场景的模型对齐质量难以保障。

**瓶颈二：任务格式和评分标准支持单一。** 现有奖励模型通常仅支持成对比较（pair-wise）或逐点评分（point-wise）中的一种任务格式，且大多依赖固定的评分标准（rubric）甚至无评分标准。在实际应用中，不同场景需要灵活的评估模式——例如安全检测需要二元判断（binary），指令遵循需要细粒度逐点评分，偏好对齐需要成对比较——单一任务格式的模型无法满足多样化需求。

### 现有方法的缺口

针对上述瓶颈，已有一些初步探索但远未解决问题：

- **多语言覆盖不足**：**NEMOTRON-MULTILINGUAL-49B**（Wang et al., 2025）虽支持多语言，但语言数量有限，且未公开训练细节；**M-PROMETHEUS-14B**（Pombal et al., 2025）仅覆盖 6 种语言。
- **缺乏推理能力**：**PROMETHEUS-7B-V2.0**（Kim et al., 2024）等早期评分标准基法官模型直接输出评分，缺乏可解释的推理过程，评估透明度低。
- **推理模型仅限英语**：**R3-QWEN3-14B**（Anugraha et al., 2025）首次引入评分标准基的奖励推理，但训练和推理均限于英语；**RM-R1-32B**（Chen et al., 2025）基于偏好推理，同样未涉及多语言。
- **多语言训练策略未被系统探索**：如何选择指令语言、推理语言，如何设计训练数据与课程策略以提升跨语言推理质量，这些问题在奖励建模领域几乎是空白。

### 本文动机与核心思路

针对上述缺口，本文提出 **MR3（Multilingual Rubric-Agnostic Reward Reasoning Models）**，一个任务无关的多语言奖励推理框架。其核心动机是：**通过大规模多语言训练数据构建、语言感知的推理策略设计以及从易到难的课程学习，系统性地提升奖励模型在 72 种语言上的评估能力，同时保持英语性能不退化。**

具体而言，MR3 在三个关键维度上突破现有方法的限制：

1. **语言覆盖**：从 125 种语言的初始数据池中筛选构建覆盖 72 种语言的高质量训练集，远超现有模型（最多 6 种）。
2. **任务格式**：统一支持逐点、成对、二元三种评估任务，满足多样化场景需求。
3. **推理策略**：探索三种语言配置——英语提示+英语推理（ENG-ENG）、目标语言提示+英语推理（TGT-ENG）、目标语言提示+目标语言推理（TGT-TGT）——并揭示不同策略对模型性能的影响机制。

核心洞察在于：尽管英语仍是性能最强的提示和推理语言，但针对性的多语言训练可以大幅提升模型对目标语言的鲁棒性；直接使用目标语言进行推理能在低资源语言上带来显著增益，表明高质量的跨语言推理是提升多语言评估透明度和可访问性的关键路径。

## 核心创新

MR3 的核心创新在于将评分标准无关的奖励推理模型从英语单语范式系统性地扩展至大规模多语言场景，其关键设计围绕五个 **changed slots** 展开：

1. **训练数据语言覆盖**：从以往仅覆盖英语或至多 6 种语言，扩展至 **72 种语言**（Table 1），涵盖高、中、低资源语言。这一扩展通过从超过 300 万条多语言样本的初始池中进行多阶段过滤与蒸馏实现。

2. **统一的多任务评分框架**：突破现有模型通常只支持单一任务（如成对比较）的限制，同时支持**逐点（point-wise）、成对（pair-wise）、二元（binary）** 三种评分任务（Section 3.1.1）。模型接收统一输入 $x = (t, i, a, r)$（任务指令、输入、候选回答、评分标准），输出推理轨迹、解释和评分 $y = (\text{trace}, e, s)$，使得同一模型可灵活适配不同评估场景。

3. **混合提示与推理语言策略**：区别于固定使用英语的基线做法，MR3 在训练数据构建中同时生成三种语言配置的输出——**ENG-ENG**（英语提示+英语推理）、**TGT-ENG**（目标语提示+英语推理）、**TGT-TGT**（目标语提示+目标语推理），并仅保留三种配置均正确的样本（Figure 2）。这一设计使模型在推理时可根据需求灵活切换语言模式，显著提升了低资源语言上的推理鲁棒性。

4. **从易到难的课程学习（EasyToHard）**：替代典型的随机打乱 SFT 策略，基于样本正确率和长度构建从易到难的课程顺序。消融实验表明，EasyToHard 在验证集 Kendall Tau 上达到 **0.4779**，优于随机打乱（0.4583）和其他课程策略（Table 24）。

5. **训练数据规模与质量**：将高质量多语言训练样本规模从过去英文模型通常不足 20K 的水平提升至 **10 万条**（Table 23），并通过强教师模型 **GPT-OSS-120B** 蒸馏获取监督信号。数据规模消融显示，从 10K 增至 100K 使多基准平均性能从 80.49 提升至 82.09；而弱教师模型（GPT-OSS-20B）则导致性能大幅下降至 78.21（Table 26），印证了教师质量的关键作用。

这些创新协同作用，使得 MR3-QWEN3-14B 在多语言偏好基准上以 **85.04%** 的平均准确率超越 GPT-OSS-120B（84.13%），参数量仅为后者的 1/9。

## 整体框架

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_ST0wOB1bdX/figures/002_Table_1.jpg]]
*Table 1: A comparison between existing models and MR3 across various dimensions, including data being used, task formats, and evaluation rubrics. ∗The model is neither closed-source nor proprietary*

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_ST0wOB1bdX/figures/003_Figure_2.jpg]]
*Figure 2: MR3 dataset construction that is aligned across different multilingual settings to highlight the trade-offs between using English and the input language for the prompts and reasoning traces. Here, prompt denotes both instruction and rubric, eng denotes English, and tgt denotes target language based on the input. A training sample is accepted if (1) all outputs distilled from GPT-OSS-120B using different prompting and reasoning languages are correct, and (2) GPT-OSS-20B does not solve it consistently after being sampled five times*

MR3 构建了一个**任务无关、评分标准可定制**的统一评估框架，将奖励建模形式化为一个生成式推理问题。给定任务指令 $t$、输入上下文 $i$、候选回答 $a$ 以及评分标准 $r$，模型输出一个三元组 $y = (\text{trace}, e, s)$，其中 $\text{trace}$ 为推理轨迹，$e$ 为简要解释，$s$ 为最终评分。该框架在统一的接口下同时支持三种评估范式：**逐点评分**（对单一回答给出绝对分数）、**成对比较**（在两个候选回答中选择更优者）和**二元判断**（对单一回答给出真/假判定），这从根本上改变了现有奖励模型通常只支持单一任务格式的局限。

整个 pipeline 由七个核心模块串联而成，形成从原始数据到最终模型的完整链路：

**1. 初始数据收集**：从公开数据源汇集超过 300 万条多语言样本，覆盖 125 种语言和多个领域，作为候选数据池。这一规模远超以往英文模型通常不足 2 万条的体量。

**2. 评分标准自动生成**：对于缺少人工评分标准的数据集，系统使用 GPT-4.1 根据任务类型和描述自动生成英语评分标准，并配套生成多个释义变体以增强鲁棒性。这一步骤确保了框架的“评分标准无关”特性——无论原始数据是否包含评分标准，模型都能获得结构化的评估依据。

**3. 教师模型蒸馏**：以 GPT-OSS-120B 作为教师模型，为每个样本生成期望的推理轨迹、解释和评分，形成高质量的监督信号。教师模型的选择至关重要——消融实验表明，若改用较弱的 GPT-OSS-20B，模型平均性能将从 82.09 骤降至 78.21，甚至低于未微调的基座模型。

**4. 多语言推理策略构建**：这是 MR3 区别于现有工作的关键创新。系统为每个样本生成三种语言配置的输出：**ENG-ENG**（英语提示 + 英语推理）、**TGT-ENG**（目标语言提示 + 英语推理）、**TGT-TGT**（目标语言提示 + 目标语言推理）。随后执行严格的质量过滤——仅保留三种配置下评分均正确的样本，确保跨语言推理的一致性。这一设计直接回应了核心瓶颈：现有模型在多语言评估中性能显著落后于英语，且缺乏对多语言训练策略的系统探索。

**5. 难度过滤**：使用 GPT-OSS-20B 对样本进行多次测试，移除那些连续多次都能正确解答的简单样本，保留高难度样本以提升训练效率。经过前述所有过滤后，得到约 44 万条高质量样本。

**6. 最终数据集选择**：从 44 万条样本中下采样至 10 万条，在数据多样性和训练规模之间取得平衡。消融实验证实，将数据量从 1 万逐步增加至 10 万，模型在多个基准上的平均性能从 80.49 持续提升至 82.09，验证了大规模高质量多语言数据的重要性。

**7. 有监督微调与课程学习**：使用 EasyToHard 课程顺序对基座模型（QWEN3 系列）进行全参数微调。课程学习将样本按正确率和长度排序，从简单样本开始逐步过渡到困难样本。验证集上的 Kendall Tau 达到 0.4779，优于随机打乱（0.4583）和其他课程策略，表明从易到难的训练顺序对多语言奖励建模具有显著正向作用。训练目标为标准交叉熵损失，最大化参考回答的对数似然。

整个框架的输入输出流清晰：多语言任务输入经过评分标准注入后，通过教师蒸馏获得监督信号，再经由多语言对齐和难度过滤形成训练数据，最终通过课程微调产出可部署的奖励模型。该设计使得 MR3 在仅使用 GPT-OSS-120B 约 1/9 参数量的情况下，在多语言偏好基准上实现了 85.04% 的平均准确率，超越教师模型 0.91 个百分点。

## 核心模块与公式推导

### 统一评估框架

MR3 将奖励评估建模为一个统一的生成式框架。给定任务指令 $t$、输入 $i$、候选回答 $a$ 和评分标准 $r$，模型生成推理轨迹 $\text{trace}$、简要解释 $e$ 和最终评分 $s$：

$$f(x) = y, \quad \text{where } x = (t, i, a, r), \text{ and } y = (\text{trace}, e, s)$$

该框架通过改变 $a$ 和 $s$ 的定义，自然地支持三种评分任务（Section 3.1.1）：

- **逐点评分**：$a = a_1$，$s \in [1, 5]$，模型对单一回答给出 1–5 分的标量评分。
- **成对比较**：$a = (a_1, a_2)$，$s \in \{a_1, a_2\}$，模型在两个候选回答中选择更优者。
- **二元判断**：$a = a_1$，$s \in \{\text{true, false}\}$，模型对单一回答给出真/假判断。

这一设计的核心优势在于**任务格式与推理逻辑的解耦**：模型通过统一的生成式接口处理不同评分任务，无需为每种任务维护独立的模型头或架构分支。

### 数据构建流水线

MR3 的数据构建分为六个关键模块，形成从原始数据到高质量训练集的完整链路（Section 3.1.2–3.1.3，Figure 2）：

1. **初始数据收集**：从公开数据集收集超过 300 万条多语言样本，覆盖 125 种语言和多个领域（知识、数学、安全、指令遵循等）。
2. **评分标准自动生成**：对于缺少评分标准的数据集，使用 GPT-4.1 自动生成英语评分标准及多个释义变体，确保模型在推理时能获得细粒度、可定制的评估依据。
3. **教师模型蒸馏**：利用 GPT-OSS-120B 作为教师模型，为每个样本生成期望的推理轨迹、解释和评分，作为监督信号。
4. **多语言推理策略构建**：为每个样本生成三种语言配置的输出——ENG-ENG（英语提示 + 英语推理）、TGT-ENG（目标语提示 + 英语推理）、TGT-TGT（目标语提示 + 目标语推理）——仅保留三种配置均正确的样本，确保跨语言一致性。
5. **难度过滤**：移除 GPT-OSS-20B 连续多次都能正确解答的简单样本，保留高难度样本以提升训练信号密度。
6. **最终数据集选择**：从约 44 万条高质量样本中下采样至 10 万条，覆盖 72 种语言，兼顾数据多样性和训练效率。

### 监督微调损失函数

MR3 采用全参数监督微调，优化标准交叉熵损失，最大化参考回答的对数似然：

$$\mathcal{L}_{\mathrm{SFT}}(\theta) = -\frac{1}{N}\sum_{i=1}^{N}\sum_{t=1}^{T_i}\log\pi_\theta\big(y_t^{(i)} \mid y_{<t}^{(i)}, x^{(i)}\big)$$

其中 $N$ 为训练样本数，$T_i$ 为第 $i$ 个样本的目标序列长度，$y_t^{(i)}$ 为第 $t$ 个目标 token，$y_{<t}^{(i)}$ 为前序 token，$x^{(i)}$ 为输入上下文。该损失鼓励模型生成高质量的推理轨迹、解释和期望格式的评分（Section 3.2.1）。

### 课程学习策略

在训练顺序上，MR3 采用 **EasyToHard 课程学习**（Section 3.2.2）：基于教师模型对每个样本的正确率和输出长度进行排序，从简单样本开始训练，逐步过渡到困难样本。消融实验（Table 24）表明，EasyToHard 在验证集 Kendall Tau 上达到 0.4779，优于随机打乱（0.4583）和其他课程策略，验证了从易到难的训练顺序对多语言奖励建模的有效性。

## 实验与分析

### 核心瓶颈与因果机制

现有奖励模型在多语言评估中存在两个关键瓶颈：其一，性能显著落后于英语，尤其在低资源语言上差距悬殊；其二，多数模型仅支持单一评分任务（如成对比较），缺乏对逐点评分、二元判断等多样化评估范式的覆盖。MR3 通过构建覆盖 72 种语言的高质量多语言训练数据，结合语言感知的提示与推理策略（ENG-ENG、TGT-ENG、TGT-TGT），以及从易到难的课程学习，系统性地缓解了上述瓶颈。核心因果链条可概括为：**高质量多语言蒸馏数据 × 多语言推理策略 → 跨语言奖励评估鲁棒性提升**。尽管英语仍是最强的提示和推理语言，但针对性的多语言训练大幅提升了模型对目标语言的鲁棒性，且直接使用目标语言进行推理能在低资源语言上带来显著增益。

### 主结果：多语言偏好基准

Table 2 展示了 MR3 在四个成对偏好基准上的综合表现。**MR3-QWEN3-14B 在 m-RewardBench（23 种语言）上达到 89.18% 准确率，以 0.13 个百分点的微弱优势超越 GPT-OSS-120B（89.05%），而参数量仅为后者的约 1/9。** 在 MM-Eval（18 种语言）上，MR3-QWEN3-14B 以 86.05% 显著领先 GPT-OSS-120B 的 85.01%（+1.04 个百分点），并在 IndoPref 上取得 71.78% 的最佳成绩。与同类多语言生成式奖励模型 **NEMOTRON-MULTILINGUAL-49B**（Wang et al., 2025c）相比，MR3-QWEN3-14B 在 m-RewardBench 上的优势高达 +4.21 个百分点。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_ST0wOB1bdX/figures/004_Table_2.jpg]]
*Table 2: Overall results of MR3 compared to other baselines when prompted with English and think on English (when applicable for reasoning models) on pairwise evaluation benchmarks, reported as average ± standard deviation across 5 runs. Bolded and underlined indicate the best-performing results and second-best-performing results, respectively. Note that some standard deviations are not reported because they were not included in the corresponding works*

值得注意的是，在英语基准 RewardBench 上，MR3-QWEN3-14B（90.79%）略低于仅用英语训练的 **R3-QWEN3-14B**（Anugraha et al., 2025）的 91.00%（-0.21），表明多语言训练在英语任务上存在微弱的性能代价。然而，这一代价换来了多语言场景下的大幅提升，整体平均准确率达到 85.04%，超越所有先前奖励模型。

### 跨领域泛化验证

Table 3 进一步验证了 MR3 在知识、数学、安全三个领域的泛化能力。在覆盖 44 种语言的 INCLUDE-base-44 知识基准上，MR3-QWEN3-14B 达到 70.61%，较 R3-QWEN3-14B 提升 1.20 个百分点。在 11 种语言的数学推理基准 MGSM 上，MR3-QWEN3-14B 取得 94.00%，与 R3-QWEN3-14B（94.07%）基本持平。在安全基准 RTP-LX（27 种语言）上，MR3-QWEN3-14B 的 F1 分数达到 90.19%，较基座模型 QWEN3-14B（78.36%）提升 11.83 个百分点，展示了在不平衡类别下的鲁棒性。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_ST0wOB1bdX/figures/005_Table_3.jpg]]
*Table 3: Overall results of MR3 compared to other baselines when prompted with English and think on English (when applicable for reasoning models) on INCLUDE-base-44 (general knowledge), MGSM (math), and RTP-LX (safety) evaluation benchmarks, reported as average ± standard deviation across 5 runs. Bolded numbers indicate the best-performing results, while underlined numbers indicate the second-best-performing results*

### 多语言提示与推理策略的影响

Figure 3 揭示了不同语言策略下的性能差异。微调后的 MR3 模型在所有策略上均显著优于基座模型，且随着模型规模增大，对非英语提示的鲁棒性增强。**ENG-ENG 策略（英语提示 + 英语推理）在绝对性能上仍最强，但 TGT-ENG（目标语言提示 + 英语推理）紧随其后，TGT-TGT（目标语言提示 + 目标语言推理）在低资源语言上带来显著增益。** 这一发现表明，尽管英语仍是推理质量最高的语言，但目标语言推理对于提升低资源语言评估的透明度和可访问性至关重要。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_ST0wOB1bdX/figures/006_Figure_3.jpg]]
*Figure 3: Average performance of the MR3 models (solid bars) and their base models (hatched bars) across different parameter sizes and multilingual prompting and reasoning strategies. The performance of each MR3 model consistently improves its corresponding base model for every different strategy, especially when thinking in the target language, which is important*

### 策略模型对齐实验

Table 4 展示了使用 MR3-QWEN3-14B 作为奖励模型进行 DPO 对齐训练的结果。在 QWEN3-30B-A3B-INSTRUCT-2507 基座上，MR3 驱动的 DPO 在 INCLUDE-base-44 上达到 68.75% 准确率，优于使用 NEMOTRON-MULTILINGUAL-49B 的 66.09%。在多语言指令遵循基准 m-ArenaHard-v2.0 上，MR3-DPO 的整体胜率达到 45.2%，英语胜率达 57.3%，验证了 MR3 作为策略优化奖励信号的有效性。

### 消融实验与关键发现

**数据规模消融**（Table 23）：将训练数据从 10K 逐步增加到 100K，模型在多个基准上的平均性能从 80.49 单调提升至 82.09，表明更大规模的高质量多语言数据持续带来收益。

**课程学习策略**（Table 24）：EasyToHard 课程学习在验证集 Kendall Tau 上达到 0.4779，优于随机打乱（0.4583）、HardToEasy（0.4651）和基于长度的课程（0.4680）。该策略基于正确率和长度对样本排序，使模型从简单样本逐步过渡到困难样本，有效稳定了训练过程。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_ST0wOB1bdX/figures/030_Table_24.jpg]]
*Table 24: Validation-set performance across different curriculum strategies on QWEN3-4B. Here, EasyToHard is shown to perform the best, so we select this curriculum as our final curriculum*

**教师模型质量**（Table 26）：使用弱教师模型 GPT-OSS-20B 进行蒸馏导致平均性能从 82.09 骤降至 78.21，甚至低于未微调的基座模型。这一结果凸显了 MR3 对强教师模型的高度依赖，构成该方法的实际部署瓶颈。

**训练范式对比**（Table 28）：纯 SFT（100K 样本）在所有训练阶段中表现最优，平均得分 82.09，优于 50K SFT（80.56）和 50K SFT + 50K RLVR（80.43）。RLVR 方法在本研究中未能带来额外增益，且训练成本更高，表明强化学习在多语言奖励建模中的潜力尚未被充分挖掘。

### 推理质量人工评估

Table 31 展示了 20 名标注者（覆盖 12 种语言）对推理质量的人工评估结果。**MR3 的目标语言推理在事实性得分上达到 2.78±0.30，逻辑性得分达到 2.67±0.45，显著优于基座模型 QWEN3 的 2.06 和 2.05。** 训练数据中的推理质量总体较高（事实性/逻辑性 > 2），英语推理最优，目标语言推理轻微下降，翻译推理再略有降低（Table 30）。这一结果验证了多语言训练对推理质量的实际提升效果，即使在训练数据中未见的极低资源语言上，MR3 的推理仍展现出一定的泛化能力（Table 8）。

### 失败模式与局限性

1. **英语优先性**：英语仍是性能最强的提示和推理语言，目标语言推理的基准准确率仍低于英语推理，在低资源语言上差距尤为明显（Figure 3）。
2. **强教师依赖**：模型性能高度依赖 GPT-OSS-120B 的蒸馏质量，弱教师导致性能崩溃（Table 26），限制了在无强教师场景下的应用可行性。
3. **RLVR 无效**：强化学习方法（RLVR）在本研究中未能超越纯 SFT，且训练成本更高（Table 28），多语言奖励建模的 RL 设计空间仍需探索。
4. **未见语言泛化有限**：尽管覆盖 72 种语言，训练数据中某些极低资源语言完全未见，模型的跨语言泛化能力仍有提升空间（Table 8）。
5. **人工评估样本量有限**：仅涉及 20 名标注者（12 种语言），部分低资源语言的标注一致性未深入分析，结论的外推性需谨慎对待。

### 开放问题

- 如何在训练数据中未见的极低资源语言上进一步提升推理质量与基准表现？
- 在混合语言场景（如输入和回答为不同语言）下，模型应如何选择推理语言？
- 翻译质量对目标语言推理准确性的影响有多大？是否存在更优的跨语言对齐方法？
- 进一步扩大训练数据规模（远超 100K）是否能继续带来显著收益？是否会牺牲低资源语言的性能？
- RLVR 或其他强化学习范式是否能在更合适的奖励设计下改善多语言推理与评分质量？

## 方法谱系与知识库定位

### 1. 与现有工作的关系

MR3 的核心框架继承自 **R3**（Anugraha et al., 2025）——首个基于评分标准的生成式奖励推理模型，但将其从英语单语场景大幅扩展至多语言环境。相较于 R3 仅支持英语评分，MR3 的关键突破在于构建了覆盖 72 种语言的训练数据，并引入了三种多语言提示与推理策略（ENG-ENG、TGT-ENG、TGT-TGT），使模型能够根据需求灵活切换推理语言。

在多语言奖励模型领域，MR3 与以下几类基线形成直接对比：

- **多语言生成式奖励模型**：**NEMOTRON-MULTILINGUAL-49B**（Wang et al., 2025c）是此前参数量最大的多语言奖励模型，但 MR3-QWEN3-14B 以仅 1/3.5 的参数量在平均准确率上超越其 4.21 个百分点（Table 2），表明高质量多语言推理数据比单纯扩大模型规模更有效。
- **评分标准基的法官模型**：**M-PROMETHEUS-14B**（Pombal et al., 2025）支持多语言评分标准，但仅覆盖 6 种语言，且缺乏推理能力。MR3 将语言覆盖扩展至 72 种，并引入了可解释的推理轨迹。
- **基于偏好的推理奖励模型**：**RM-R1-32B**（Chen et al., 2025b）专注于偏好任务，但未涉及多语言场景和评分标准定制。MR3 同时支持逐点、成对和二元三种评分任务，通用性更强。
- **早期英语评分标准法官**：**PROMETHEUS-7B-V2.0**（Kim et al., 2024）是评分标准基方法的先驱，但仅限英语且不支持推理。MR3 在此基础上实现了多语言化和推理化。

从方法演进角度看，MR3 将“评分标准基评估”与“推理增强”两条技术路线在多语言维度上进行了融合。其核心贡献不在于提出全新的模型架构，而在于系统性地解决了多语言奖励建模中的数据构建、语言策略选择和课程设计问题，为后续研究提供了可复现的范式。

### 2. 适用边界

MR3 的设计使其在以下场景中具有明确优势：

- **高覆盖多语言评估**：训练数据覆盖 72 种语言，涵盖高、中、低资源语言，在 m-RewardBench（23 种语言）和 MM-Eval（18 种语言）上均达到最优或次优性能（Table 2）。
- **多任务评分**：统一框架支持逐点打分、成对比较和二元判断三种任务格式，无需为不同任务训练独立模型。
- **评分标准可定制**：用户可提供自定义评分标准，模型据此进行可控评分，而非输出固定的偏好信号。
- **下游对齐应用**：作为奖励模型用于 DPO 训练时，MR3-QWEN3-14B 能有效提升策略模型的多语言指令遵循能力（Table 4），表明其评分信号具有实际对齐价值。

然而，以下边界条件值得注意：

- **强教师依赖**：训练数据依赖 GPT-OSS-120B 进行知识蒸馏。消融实验显示，使用弱教师模型（GPT-OSS-20B）会导致平均性能从 82.09 降至 78.21，甚至低于未微调的基座模型（Table 26）。这意味着在没有同等规模强教师模型的情况下，方法难以复现。
- **英语仍是锚点语言**：尽管多语言训练大幅缩小了性能差距，但 ENG-ENG 策略在所有模型尺寸下仍是最强配置（Figure 3）。对于极低资源语言，目标语言推理（TGT-TGT）的性能仍明显低于英语推理。
- **训练数据语言覆盖有限**：虽然支持 72 种语言，但部分极低资源语言在训练数据中完全未见（unseen）。模型在这些语言上的泛化能力有限，性能显著低于训练中见过的语言（Table 8）。

### 3. 局限与开放问题

**已知局限**

1. **英语偏置未完全消除**：英语仍是性能最强的提示和推理语言。在低资源语言上，目标语言推理的基准准确率仍低于英语推理，差距在较小模型上尤为明显（Figure 3），说明当前训练策略未能完全实现跨语言推理能力的均等化。

2. **强教师依赖限制可复现性**：蒸馏过程依赖 GPT-OSS-120B 这一超大规模模型。当教师质量下降时，学生模型性能急剧恶化（Table 26），这使得方法在缺乏顶级闭源模型 API 的场景下难以推广。

3. **强化学习未带来增益**：纯 SFT（100K 样本）在所有训练阶段中表现最优（平均得分 82.09），而 50K SFT + 50K RLVR 的组合（80.43）反而略低（Table 28）。这表明当前 RLVR 设计未能有效利用多语言奖励信号，强化学习在该任务上的潜力未被充分挖掘。

4. **人工评估规模有限**：推理质量的人工评估仅涉及 20 名标注者（覆盖 12 种语言），样本量有限。部分低资源语言的标注一致性未深入分析，可能无法完全反映真实的多语言偏好分布。

5. **混合语言场景未覆盖**：当前训练数据假设输入、回答和评分标准使用同一语言。在混合语言场景（如输入为语言 A、回答为语言 B）下，模型应如何选择推理语言，尚未得到探索。

**开放问题**

1. **极低资源语言的泛化**：如何在训练数据中未见过的语言上进一步提升推理质量？是否需要引入跨语言迁移学习或元学习策略？

2. **推理语言的自适应选择**：在混合语言输入场景下，模型应自动选择英语推理还是目标语言推理？是否存在基于语言资源级别的自适应策略？

3. **翻译质量的影响**：TGT-ENG 和 TGT-TGT 策略均涉及翻译环节。翻译质量对目标语言推理准确性的影响有多大？直接使用原始目标语言数据是否优于翻译数据？

4. **数据规模的边际收益**：消融实验表明从 10K 增至 100K 带来持续提升（Table 23）。进一步扩大至 200K 或 500K 是否能继续带来显著收益？是否会因数据多样性稀释而牺牲低资源语言性能？

5. **强化学习的重新设计**：当前 RLVR 不如纯 SFT 有效。是否可以通过更精细的奖励设计（如语言特定的奖励塑形）或离线强化学习范式来改善多语言推理与评分质量？

6. **推理质量与评分准确性的因果关系**：人工评估显示 MR3 的目标语言推理质量优于基座模型（Table 31），但推理质量的提升是否直接导致评分准确性的提升？两者之间的因果机制尚待严格验证。

## 原文 PDF

![[paperPDFs/ICLR_2026/mR3_Multilingual_Rubric_Agnostic_Reward_Reasoning_Models.pdf]]
