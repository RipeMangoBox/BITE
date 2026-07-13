---
title: "VerifyBench: Benchmarking Reference-based Reward Systems for Large Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/VerifyBench_Benchmarking_Reference_based_Reward_Systems_for_Large_Language_Models.pdf
project_link: https://zju-real.github.io/VerifyBench/
code_link: https://github.com/ZJU-REAL/VerifyBench
openreview_forum_id: JfsjGmuFxz
aliases:
- VVH
- VerifyBench
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "构建VerifyBench和VerifyBench-Hard两个基准数据集，将评测范式从偏好排序转变为基于参考答案的单一回答正确性判断，并提供平衡和困难两种难度分布，以量化分析不同验证方法的绝对正确性判断能力。"
primary_logic: "基于参考答案的验证在推理模型的强化学习中至关重要；通过提供参考答案并评估模型判断回答正确性的能力，可以更真实地反映训练中的奖励信号。现有大模型在标准样本上表现良好（>90%），但在困难样本（VerifyBench-Hard）上仍有约20%的性能下降，且参考答案的加入可提升5-18%的验证准确度，验证器质量直接影响RL训练效果。"
claims:
- "VerifyBench通过判断单个回答是否与参考答案一致来评估奖励系统，与现有偏好比较基准有本质区别。"
- "VerifyBench-Hard选用了顶尖模型判断高度冲突的样本，提供了更具挑战性的测试。"
- "移除参考答案会导致验证准确率下降5-18个百分点。"
- "在VerifyBench上表现更好的模型作为RL验证器，能带来更显著的性能提升。"
---

# VerifyBench: Benchmarking Reference-based Reward Systems for Large Language Models

> [!tip] 核心洞察
> 基于参考答案的验证在推理模型的强化学习中至关重要；通过提供参考答案并评估模型判断回答正确性的能力，可以更真实地反映训练中的奖励信号。现有大模型在标准样本上表现良好（>90%），但在困难样本（VerifyBench-Hard）上仍有约20%的性能下降，且参考答案的加入可提升5-18%的验证准确度，验证器质量直接影响RL训练效果。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | VerifyBench：面向大语言模型的基于参考答案的奖励系统基准测试 |
| 英文题名 | VerifyBench: Benchmarking Reference-based Reward Systems for Large Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=JfsjGmuFxz) · [GitHub](https://github.com/ZJU-REAL/VerifyBench) · [Project](https://zju-real.github.io/VerifyBench/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | VerifyBench / VerifyBench-Hard |
| Dataset | VerifyBench, VerifyBench-Hard, VerifyBench (小模型对比) |

> [!tip] 效果简介
> - VerifyBench 上，Accuracy (AVG %) 为 gpt-oss-120b 95.85，对比 math-verify 66.95，变化 +28.90。
> - VerifyBench-Hard 上，Accuracy (AVG %) 为 gpt-oss-120b 87.90，对比 math-verify 76.00，变化 +11.90。
> - VerifyBench (小模型对比) 上，Accuracy (%) 为 Qwen3-1.7B 81.10，对比 Llama-3.2-3B-Instruct 60.95，变化 +20.15。

## 概要

当前大语言模型奖励系统的评测主要依赖于成对偏好比较（pairwise preference ranking），即判断同一问题的两个回答中哪一个更好。然而，在推理模型（Large Reasoning Models, LRMs）的强化学习训练中，奖励信号通常来源于基于参考答案的单一回答正确性验证：给定问题、参考答案和模型生成的回答，判断该回答是否正确。现有的偏好基准（如 **Reward Bench**，Lambert et al., 2025）无法有效评估这种参考验证场景下的奖励质量。

针对这一瓶颈，本文提出 **VerifyBench** 和 **VerifyBench-Hard** 两个基准数据集，将评测范式从偏好排序转变为基于参考答案的单一回答正确性验证。VerifyBench 包含 2,000 个经人工标注的 (问题, 参考答案, 回答, 正确性标签) 四元组，覆盖数值、表达式、选择和字符串四种答案类型，并通过受控下采样确保类别和标签的均衡分布。VerifyBench-Hard 则利用多个高性能模型在验证判断上的分歧，筛选出 1,000 个高难度样本，提供更具区分度的测试场景。

核心发现如下：

- **参考答案是关键信号源**：移除参考答案后，各模型的验证准确率下降 5–18 个百分点（绝对值），表明参考信息在正确性判断中不可替代。
- **困难样本暴露能力差距**：顶尖模型在标准 VerifyBench 上的平均准确率超过 95%，但在 VerifyBench-Hard 上降至约 87–88%，性能下降约 8 个百分点，说明困难样本能有效区分模型间的细微差异。
- **验证器质量直接影响强化学习训练**：在 VerifyBench 上得分更高的模型作为 RL 验证器时，能带来更显著的训练收益；而弱验证器（如准确率约 60% 的模型）甚至可能导致训练性能下降。
- **小模型存在较大提升空间**：参数规模小于 3B 的模型在 VerifyBench 上的验证准确率显著低于大模型（如 Llama-3.2-3B-Instruct 仅 60.95%），表明轻量级验证器的能力建设仍是开放问题。

本基准聚焦于答案级别的二值正确性判断，不评估推理过程质量或部分正确回答，且排除了证明题和开放式问题，这些限制为后续扩展留下了明确方向。

大语言模型（LLM）的强化学习（RL）训练依赖于可靠的奖励信号来引导模型行为。当前，奖励系统的评测主要建立在**成对偏好比较**（pairwise preference ranking）范式之上：给定一个查询和两个回答，奖励模型需要判断哪个回答更好，评测指标是正确赋予高分给更佳回答的准确率。这一范式在 **Reward Bench**（Lambert et al., 2025）和 **RM-Bench** 等基准中得到了广泛应用，其核心公式为：

$$reward = R_{\varphi}(q, r)$$

$$\mathrm{Accuracy} = \frac{1}{|D|} \sum_{(q, r_w, r_l) \in D} \mathbb{I}[R_{\varphi}(q, r_w) > R_{\varphi}(q, r_l)]$$

然而，在推理模型（Large Reasoning Models, LRMs）的RL训练中，奖励信号的实际使用方式与上述评测范式存在根本性差异。训练中通常需要**基于参考答案**对单一回答的正确性进行判断，而非在两个回答之间做偏好排序。这一差异揭示了一个关键瓶颈：**当前缺乏专门针对基于参考答案（reference-based）的奖励系统在单一回答正确性验证任务上的标准化基准**，导致无法有效评估推理模型训练中实际使用的验证系统。

具体而言，现有评测体系存在三个核心缺口：

1. **范式不匹配**：偏好比较评测的是相对排序能力，而RL训练需要的是绝对正确性判断——即判断模型生成的回答是否与参考答案一致。两者对应的输入组成和评价指标完全不同：偏好比较的输入为 `(query, 回答A, 回答B)`，而基于参考答案的验证输入为 `(query, 参考答案, 单一回答)`，其奖励信号定义为：

   $$reward = R_{\varphi}(q, gt, r)$$

   评测指标也应从“排序准确率”转变为“预测二值正确性标签的准确率”：

   $$\operatorname{Accuracy} = \frac{1}{|D|} \sum_{(q, gt, r, y) \in D} \mathbb{I}[\mathbb{E}(R_{\varphi}(q, gt, r)) = y]$$

2. **难度分布不足**：现有基准的样本多为自然分布，缺乏对高难度、高冲突场景的系统性覆盖，而这些场景恰恰是验证系统在RL训练中最容易出错的地方。

3. **验证器质量反馈缺失**：现有基准无法回答一个关键问题——验证器的质量差异究竟会在多大程度上影响RL训练的最终效果？换言之，缺乏将验证器评测分数与下游训练收益直接关联的实验证据。

为解决上述问题，本文提出 **VerifyBench** 和 **VerifyBench-Hard** 两个基准数据集，将评测范式从偏好排序转变为基于参考答案的单一回答正确性判断。VerifyBench 提供平衡的难度分布，而 VerifyBench-Hard 则通过筛选顶尖模型判断高度冲突的样本，构建更具挑战性的测试集。这一设计使得研究者能够量化分析不同验证方法在绝对正确性判断上的能力差异，并建立起验证器质量与RL训练效果之间的因果关联。

## 核心方法与创新机理

VerifyBench 的核心创新在于将大语言模型奖励系统的评测范式从**成对偏好排序**（pairwise preference ranking）切换为**基于参考答案的单一回答正确性验证**（single-response correctness verification）。这一转变并非简单的评测形式变化，而是直接对应推理模型（LRM）强化学习训练中实际使用的奖励信号形式，因此能更真实地反映训练中验证系统的质量。

### 范式转变：从偏好比较到正确性判断

现有奖励基准（如 **Reward Bench**，Lambert et al., 2025；**RM-Bench**）的评测逻辑是：给定一个问题 $q$ 和两个回答 $r_w$（较好）与 $r_l$（较差），判断奖励模型是否给 $r_w$ 分配更高的分数。其准确率定义为：

$$\mathrm{Accuracy} = \frac{1}{|D|} \sum_{(q, r_w, r_l) \in D} \mathbb{I}[R_{\varphi}(q, r_w) > R_{\varphi}(q, r_l)]$$

这种范式衡量的是**相对排序能力**，而非奖励系统对单个回答正确性的**绝对判断能力**。

VerifyBench 改变了这一设定：输入变为 $(q, gt, r)$，即问题 $q$、参考答案 $gt$ 和单一回答 $r$，奖励模型输出连续分数后经离散化映射为二值正确性预测，准确率定义为：

$$\operatorname{Accuracy} = \frac{1}{|D|} \sum_{(q, gt, r, y) \in D} \mathbb{I}[\mathbb{E}(R_{\varphi}(q, gt, r)) = y]$$

其中 $y$ 为真实正确性标签，$\mathbb{E}(\cdot)$ 将连续奖励分数映射为离散预测。这一范式直接评估验证系统“判断回答是否正确”的能力，与推理模型 RL 训练中验证器（verifier）的实际角色一致。

### 参考答案的角色

在现有偏好比较基准中，参考答案通常不参与评测流程。VerifyBench 将参考答案显式纳入输入，使其成为验证判断的核心依据。消融实验表明，移除参考答案后各模型在 VerifyBench 上的准确率下降 **5-18 个百分点**（Table 3），证明了参考答案对验证性能的关键支撑作用。这一设计使得基准能够评估验证系统是否真正理解问题与答案之间的对应关系，而非仅依赖回答本身的表面特征做判断。

### 难度分层：VerifyBench-Hard

VerifyBench-Hard 是另一个关键创新。其构建过程利用 **5 个在 VerifyBench 上表现领先的 LLM** 对回答进行评判，筛选出模型判断高度冲突的样本。这意味着这些样本不是随机困难，而是**当前最强模型之间也存在严重分歧的边界案例**。从 Table 1 的统计来看，VerifyBench-Hard 中正确答案仅占 291/1000（约 29%），远低于标准 VerifyBench 的 1000/2000（50%），且多选题（430）和字符串题（276）占比显著偏高，反映了这些类型在边界判断上的固有难度。实验结果显示，顶尖模型在 VerifyBench-Hard 上的平均准确率（如 gpt-oss-120b 的 87.90%）相比标准 VerifyBench（95.85%）下降约 8 个百分点，而规则方法 math-verify 仅从 66.95% 提升至 76.00%，揭示了两类方法在困难样本上的能力差异模式不同。

### 评测指标与难度设计的协同

四个 changed slots——评测范式、输入组成、评价指标和难度设计——并非孤立存在，而是形成了一条完整的创新链条：**因为**输入中加入了参考答案，**所以**评测可以聚焦于单一回答的正确性判断；**因为**目标是绝对正确性，**所以**指标从排序准确率变为二值分类准确率；**因为**标准样本上大模型已接近天花板（>90%），**所以**需要 VerifyBench-Hard 来区分顶尖方法。这一链条使得 VerifyBench 能够捕捉到现有基准无法反映的验证能力差异，尤其是为推理模型 RL 训练中验证器的选择提供了直接相关的评测信号。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_JfsjGmuFxz/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the benchmark construction process. The upper section outlines the pipeline used to construct VerifyBench, whereas the lower section details the pipeline for VerifyBench-Hard. The components highlighted by black boxes denote the final entries included in the benchmark*

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_JfsjGmuFxz/figures/001_Figure_1.jpg]]
*Figure 1: The core distinction between VerifyBench and existing reward benchmarks (Lambert et al., 2025; Liu et al., 2024) is illustrated as follows. Upper panel: Existing reward benchmarks assess the accuracy of a reward system by comparing the ranking of two completions for the same question. Lower panel: In contrast, our proposed VerifyBench evaluates the accuracy of a reward system by determining the correctness of a single completion using a reference answer*

VerifyBench 的整体框架围绕一个核心范式转换展开：将奖励系统的评测从传统的成对偏好排名（pairwise preference ranking）转变为基于参考答案的单一回答正确性验证。这一设计直接回应了当前推理模型（LRM）强化学习训练中的瓶颈——现有基准（如 **Reward Bench**, Lambert et al., 2025）无法有效评估训练中实际使用的、依赖参考答案的验证系统。

### 核心范式对比

图 1 清晰地展示了这一范式差异。传统奖励基准的输入为三元组 $(q, r_w, r_l)$（查询、较好回答、较差回答），评价指标是奖励模型能否正确赋予 $r_w$ 更高的分数，其准确率公式为：

$$\mathrm{Accuracy} = \frac{1}{|D|} \sum_{(q, r_w, r_l) \in D} \mathbb{I}[R_{\varphi}(q, r_w) > R_{\varphi}(q, r_l)]$$

VerifyBench 则将输入重构为 $(q, gt, r)$（查询、参考答案、单一回答），要求系统直接判断该回答是否正确，其奖励函数形式为 $reward = R_{\varphi}(q, gt, r)$，准确率公式变为：

$$\operatorname{Accuracy} = \frac{1}{|D|} \sum_{(q, gt, r, y) \in D} \mathbb{I}[\mathbb{E}(R_{\varphi}(q, gt, r)) = y]$$

其中 $\mathbb{E}(\cdot)$ 将连续奖励分数映射为离散的二值正确性标签。这一设计更真实地反映了 RL 训练中的奖励信号形态。

### 双基准构建流程

图 2 展示了 VerifyBench 和 VerifyBench-Hard 两条并行的构建流水线，二者共享前半部分模块，在难度筛选环节分叉。

**VerifyBench 构建流水线**包含五个核心模块：

1. **问题收集与答案类型标注（Query Curation & Answer Type Labeling）**：从 41 个开源数据集收集推理问题，利用 LLM 将答案标注为数值（Numeric Values）、表达式（Expressions）、选择题（Multi-choice）、字符串（String）四种类型。
2. **回答生成与预标注（Completion Generation & Pre-annotation）**：使用 22 个开源和闭源模型为每个问题生成回答，由 Llama-3.3-70B-Instruct 初步判断正确性。
3. **人工标注（Human Annotation）**：至少两名标注者对答案类型和回答正确性进行独立标注，不一致时由元标注者仲裁。
4. **均衡下采样（Controlled Downsampling）**：确保每种答案类型保留 250 个问题，每个问题配一正一负两个回答，最终形成 2,000 个平衡的元组，消除类别不平衡对评测的干扰。

**VerifyBench-Hard 构建流水线**在前三步基础上引入额外的难度筛选模块：

5. **难度筛选（Difficulty Filtering）**：利用 5 个在 VerifyBench 上表现领先的 LLM 对回答进行评判，选择模型判断高度冲突的样本——即顶尖模型之间也存在显著分歧的题目-回答对。这一设计使 VerifyBench-Hard 能够揭示模型在边界情况下的验证能力差异。

### 输入输出流

整个框架的输入输出关系清晰：输入为 $(q, gt, r)$ 三元组，输出为二值正确性判断。两条基准的区别在于样本难度分布——VerifyBench 保持自然分布下的类别平衡，VerifyBench-Hard 则聚焦于高冲突样本，提供更具挑战性的测试场景。实验表明，顶尖模型在 VerifyBench 上可达 95% 以上的准确率，但在 VerifyBench-Hard 上下降约 8-10 个百分点，验证了困难集的设计有效性。

### 奖励模型的形式化定义

VerifyBench区分了两类奖励模型，并在基准评测中统一形式化。

**无参考答案的奖励模型**（传统范式）仅依赖查询 $q$ 和模型回答 $r$ 输出奖励信号：

$$reward = R_{\varphi}(q, r) \tag{1}$$

其评测采用成对比较准确率——给定同一查询的更好回答 $r_w$ 和较差回答 $r_l$，计算奖励模型赋予更高分给 $r_w$ 的比例：

$$\mathrm{Accuracy} = \frac{1}{|D|} \sum_{(q, r_w, r_l) \in D} \mathbb{I}[R_{\varphi}(q, r_w) > R_{\varphi}(q, r_l)] \tag{2}$$

**基于参考答案的奖励模型**（VerifyBench评测目标）额外引入参考答案 $gt$：

$$reward = R_{\varphi}(q, gt, r) \tag{3}$$

其评测范式从成对排序转变为单一回答的二值正确性判断。引入离散化操作 $E(\cdot)$，将连续奖励分数映射为正确/错误预测，并与真实标签 $y$ 比较：

$$\operatorname{Accuracy} = \frac{1}{|D|} \sum_{(q, gt, r, y) \in D} \mathbb{I}[E(R_{\varphi}(q, gt, r)) = y] \tag{4}$$

其中 $E(\cdot)$ 的具体实现（如阈值化或离散化）由各验证方法自行定义。这一公式是VerifyBench评测的核心——它直接衡量奖励系统判断单个回答是否与参考答案一致的绝对正确性，而非相对偏好排序能力。

### 基准构建的流水线模块

VerifyBench的构建包含五个关键模块（见Figure 2），VerifyBench-Hard在此基础上增加难度筛选环节。

1. **问题收集与答案类型标注**：从41个开源数据集收集推理问题，利用LLM将参考答案标注为数值、表达式、选择题、字符串四种类型。标注结果经人工复核，不一致时由元标注者仲裁。

2. **回答生成与预标注**：使用22个开源/闭源模型（VerifyBench）或18个模型（VerifyBench-Hard）为每个问题生成回答，由Llama-3.3-70B-Instruct初步判断回答的正确性，作为后续人工标注的参考。

3. **难度筛选**（仅用于VerifyBench-Hard）：选取5个在VerifyBench上性能领先的LLM对回答进行评判，筛选出模型判断高度冲突的样本——这些样本被定义为“困难”样本，构成VerifyBench-Hard的核心挑战。

4. **人工标注**：至少两名标注者对答案类型和回答正确性进行独立标注。当标注不一致时，由元标注者进行仲裁，确保标签的可靠性。

5. **均衡下采样**（仅用于VerifyBench）：对标注后的数据进行受控下采样，确保每个答案类型保留250个问题，且每个问题配有一正一负两个回答，消除类别不平衡对评测的干扰。最终VerifyBench包含1000个问题、2000个(问题-答案-回答-正确性)四元组。

### 范式转换的核心设计

VerifyBench与现有奖励基准（如Reward Bench、RM-Bench）的本质区别体现在三个维度的范式转换：

- **输入组成**：从 `(query, 回答A, 回答B)` 转变为 `(query, 参考答案, 单一回答)`，使评测更贴近推理模型RL训练中验证器接收参考答案的实际场景。
- **评价指标**：从“正确赋予高分给更佳回答的准确率”转变为“预测二值正确性标签的准确率”，直接衡量验证系统的绝对判断能力。
- **难度设计**：在自然分布样本（VerifyBench）之外，引入基于多模型分歧筛选的困难子集（VerifyBench-Hard），提供更具区分度的评测层次。

## 实验与关键发现

### 评估设置与基准统计

VerifyBench 包含 1 000 个问题、2 000 条回答（每个问题配一正一负），VerifyBench-Hard 包含 945 个问题、1 000 条回答（Table 1）。两套基准均覆盖数值、表达式、选择题、字符串四种答案类型，但分布差异显著：VB 经均衡下采样后各类型均匀（各 250 题），VB-Hard 则偏向选择题（430 题）和字符串（332 题），且正确回答占比仅 29.1%（291/1 000），远低于 VB 的 50%，体现了困难样本的设计意图。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_JfsjGmuFxz/figures/003_Table_1.jpg]]
*Table 1: Benchmark statistics of VerifyBench (VB) and VerifyBench-Hard (VB-H)*

评测对象分为三类：（1）基于规则的验证器 **math-verify**（Kydlíček, 2025）；（2）LLM-as-a-judge，包括 GPT-4o、GPT-4o-mini、DeepSeek-R1、Qwen3 系列、Llama-3 系列等；（3）模型化验证器，如 **xVerify**（Chen et al., 2025）和 **Compass Verifier**（Su et al., 2025）。评价指标为二值正确性预测准确率：

$$\operatorname{Accuracy} = \frac{1}{|D|} \sum_{(q, gt, r, y) \in D} \mathbb{I}[\mathbb{E}(R_{\varphi}(q, gt, r)) = y]$$

其中 $\mathbb{E}(\cdot)$ 将连续奖励分数离散化为正确/错误判断。

### 主结果：大模型表现优异，困难集暴露瓶颈

**Table 2** 汇总了各方法在 VB 和 VB-Hard 上的总体及分项准确率。核心发现：

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_JfsjGmuFxz/figures/004_Table_2.jpg]]
*Table 2: Overall performance(%) of VerifyBench and VerifyBench-Hard. Num stands for Numeric Values, Exp stands for Expressions, MC stands for Multi-choice and Str stands for String*

1. **顶尖大模型在 VB 上接近饱和**。GPT-oss-120b 以 95.85% 的平均准确率居首，DeepSeek-R1-0528（95.15%）和 Qwen3-32B（95.80%）紧随其后。GPT-4o-mini 亦达 92.85%，说明当前强模型在标准分布样本上的参考答案验证能力已相当成熟。

2. **VB-Hard 显著拉开差距**。GPT-oss-120b 在 VB-Hard 上降至 87.90%，DeepSeek-R1-0528 降至 86.60%，整体降幅约 8–10 个百分点。基于规则的 math-verify 从 VB 的 66.95% 升至 VB-Hard 的 76.00%，这一反常上升可能源于 VB-Hard 中选择题和字符串占比较高，规则匹配在这些类型上更具优势。

3. **模型规模与性能强相关**。小模型（<3B 参数）表现显著落后：Qwen3-1.7B 仅 81.10%，Llama-3.2-3B-Instruct 低至 60.95%，与大模型差距超过 30 个百分点。这表明小模型的参考答案验证能力存在巨大提升空间，是降低 RL 训练推理成本的关键瓶颈。

4. **答案类型差异明显**。选择题（MC）普遍得分最高（多数模型 >95%），字符串（Str）和表达式（Exp）相对困难。以 Qwen3-32B 为例，MC 达 99.00%，而 Exp 仅 94.00%，Str 为 92.60%（Table 5）。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_JfsjGmuFxz/figures/010_Table_5.jpg]]
*Table 5: Model performance(%) across the finegrained taxonomy on VerifyBench. Q32B stands for Qwen3-32B, g4o stands for gpt-4o-2024-11- 20, L70B stands for Llama-3.3-70B-Instruct and L3B stands for Llama-3.2-3B-Instruct*

### 消融实验：参考答案是关键信号源

**Table 3** 展示了移除参考答案后 LLM-as-a-judge 的性能变化。核心结论：

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_JfsjGmuFxz/figures/005_Table_3.jpg]]
*Table 3: Evaluation results(%) about how including the reference answer in the prompt influences the performance of LLM-as-a-judge*

- **所有模型在无参考答案时准确率均下降**，降幅约 5–18 个百分点（绝对值）。Qwen3 系列降幅最大（Qwen3-32B 从 95.80% 降至 78.70%，下降 17.10%），说明这些模型高度依赖参考答案进行正确性判断。
- Llama-3.2-1B 是唯一例外（+0.35%），但其绝对准确率仅约 50%，接近随机水平，波动无统计意义。
- 这一结果直接验证了论文的核心主张：**参考答案是验证信号的关键组成部分**，移除后模型不得不依赖自身知识进行判断，准确率大幅下降。

**Table 4** 进一步考察了现有无参考答案奖励模型在 VB（无参考答案设定）上的表现。结果令人警醒：

- 所有无参考答案奖励模型的准确率均低于 80%。表现最好的领域专用模型 Qwen2.5-Math-RM-72B 仅 78.00%，通用模型 internlm2-20b-reward 仅 66.95%。
- 这些模型在传统偏好基准（Reward Bench、RM-Bench）上得分较高，但在 VB 上表现平庸，揭示了**偏好排序能力与绝对正确性判断能力之间的本质差异**。

### 下游验证：VerifyBench 得分预测 RL 训练收益

**Figure 3** 展示了使用不同 VerifyBench 得分的 LLM 作为 RL 验证器时，模型在 MinervaMath 上的训练曲线。核心发现：

- **验证器质量与 RL 训练效果呈正相关**。使用 VerifyBench 得分最高的 gpt-oss-20b（94.8%）作为验证器，训练收益最大且稳定上升；Qwen3-4B（92.00%）次之；Qwen3-1.7B（81.10%）收益较小。
- **弱验证器可能导致性能退化**。使用 Llama-3.2-3B-Instruct（60.95%）作为验证器时，训练曲线几乎无提升甚至波动下降，说明低质量奖励信号会误导策略优化。
- 附录 **Figure 10** 重复验证了这一正相关关系，**Figure 11** 在 RFT（拒绝采样微调）场景下进一步证实：VerifyBench 得分更高的验证器同样带来更优的 RFT 结果。

这一发现具有重要实践意义：**VerifyBench 可作为 RL 训练前筛选验证器的有效代理指标**，避免使用弱验证器导致的训练失败。

### 细粒度错误分析

**Table 5** 按细粒度答案子类型分解了四款模型的性能。主要失败模式包括：

- **多值排序错误**：当参考答案包含多个数值且需按特定顺序排列时，模型容易误判等价性。Llama-3.2-3B-Instruct 在数值子类型上准确率普遍低于 70%。
- **数学表达式等价性判断困难**：表达式类型（Exp）是各模型的共同弱项，即使最强的 Qwen3-32B 也仅 94.00%，反映了模型对数学表达式语义等价的深层理解仍有不足。
- **字符串精确匹配的边界情况**：字符串类型中，模型在大小写、空格、标点等细节上的容错判断不一致，导致假阳性/假阴性。

### 局限性与未解决问题

1. **二值判断的粒度限制**：基准仅支持对/错二值标签，无法评估部分正确或推理过程质量，可能低估模型的部分能力。
2. **任务覆盖范围**：排除了证明题和开放式问题，限制了在完整推理链验证上的适用性。
3. **奖励欺骗未评估**：未对 RL 训练中可能出现的奖励欺骗（reward hacking）现象进行系统性评测，无法反映训练中奖励信号的被利用风险。
4. **小模型验证能力提升**：如何以低成本提升 <3B 模型的参考答案验证能力，是降低大规模 RL 训练推理成本的关键开放问题。
5. **步骤级验证的缺失**：当前基准仅评估答案级正确性，能否设计步骤级验证基准来更精细地指导推理模型训练，值得进一步探索。

## 定位与知识库关联

### 1. 评测范式转变：从偏好排序到参考答案验证

VerifyBench 的核心贡献在于将奖励系统的评测范式从“成对偏好排序”转变为“基于参考答案的单一回答正确性验证”。传统奖励基准——如 **Reward Bench**（Lambert et al., 2025）和 **RM-Bench**——采用成对比较范式：给定同一问题的两个回答，评估奖励模型是否能将更高分数赋予更优回答。其评价指标为成对准确率：

$$\mathrm{Accuracy} = \frac{1}{|D|} \sum_{(q, r_w, r_l) \in D} \mathbb{I}[R_{\varphi}(q, r_w) > R_{\varphi}(q, r_l)]$$

VerifyBench 则改变了输入组成和评价指标。其奖励模型接受三元组输入 (查询 $q$，参考答案 $gt$，单一回答 $r$)，输出连续奖励信号 $R_{\varphi}(q, gt, r)$，再通过离散化操作 $E(\cdot)$ 映射为二值正确性预测，最终以预测准确率作为评价指标：

$$\operatorname{Accuracy} = \frac{1}{|D|} \sum_{(q, gt, r, y) \in D} \mathbb{I}[\mathbb{E}(R_{\varphi}(q, gt, r)) = y]$$

这一转变的根本动因在于：当前大推理模型（LRMs）的强化学习训练中，奖励信号通常来自基于参考答案的验证系统（如规则验证器 **math-verify** (Kydlíček, 2025) 或 LLM-as-a-judge），而非无参考答案的偏好奖励模型。VerifyBench 通过直接评估模型判断“回答是否与参考答案一致”的能力，更真实地反映了训练中实际使用的奖励信号质量。

### 2. 与现有模型化验证器的关系

在模型化验证器（model-based verifier）这一类别中，VerifyBench 与 **xVerify**（Chen et al., 2025）和 **Compass Verifier**（Su et al., 2025）等工作的定位有所不同。xVerify 和 Compass Verifier 本身是具体的验证模型，而 VerifyBench 是评测这些验证模型的基准平台。在论文实验中，这些模型化验证器作为被评测对象出现在 VerifyBench 上，其表现可与 LLM-as-a-judge 基线（如 GPT-4o、GPT-4o-mini、DeepSeek-R1）和规则验证器 math-verify 进行横向比较。

### 3. 适用边界与局限

VerifyBench 的设计包含若干明确的适用边界：

**答案级别而非过程级别**：基准仅评估最终答案的正确性，不评估推理过程的正确性或部分正确的回答。这意味着它无法区分“推理过程错误但答案巧合正确”和“推理过程正确”两种情况，可能高估某些模型的验证能力。

**任务类型受限**：基准排除了证明题和开放式问题，仅覆盖数值、表达式、选择题和字符串四种答案类型。这限制了其在完整推理链验证场景中的适用性，尤其在数学证明和开放域推理任务上无法提供有效评测。

**二值判断的粒度限制**：评测仅支持对/错二值判断，无法反映部分正确或近似正确的回答质量。这可能导致对模型能力的低估——一个回答可能推理方向正确但最终答案有微小偏差，在 VerifyBench 中将被完全判错。

**未覆盖奖励欺骗**：基准未对奖励欺骗（reward hacking）场景进行系统性评估。在 RL 训练中，模型可能学会利用验证器的漏洞获得高分但实际质量低下，VerifyBench 无法反映这种风险。

### 4. 开放问题

基于上述局限和实验发现，论文揭示了若干待解决的开放问题：

**小模型验证能力提升**：实验表明小型模型（<3B 参数）在 VerifyBench 上的验证准确率显著低于大模型（如 Qwen3-1.7B 仅 81.10%，Llama-3.2-3B-Instruct 仅 60.95%）。如何提升小模型的参考验证能力，以降低 RL 训练的推理成本，是实用化部署的关键瓶颈。

**基准扩展至证明题和开放式任务**：当前基准排除了需要长推理链验证的任务类型。如何设计适用于证明题和开放式推理任务的参考答案验证基准，是一个重要的扩展方向。

**细粒度评价方案设计**：从二值答案正确性扩展到步骤级正确性判断，可能为推理模型训练提供更精细的奖励信号。论文在细粒度答案类型分析（Table 5）中已初步展示了不同子类型上的性能差异，但尚未构建步骤级的评价体系。

**奖励欺骗的防御机制**：基于参考答案的奖励系统如何有效防止奖励欺骗，是 RL 训练安全性的核心问题。论文未对此展开研究，但 RL 训练实验中弱验证器导致性能下降的现象（Figure 3 中 Llama-3.2-3B-Instruct 作为验证器时的表现）间接暗示了这一风险的存在。

## 原文 PDF

![[paperPDFs/ICLR_2026/VerifyBench_Benchmarking_Reference_based_Reward_Systems_for_Large_Language_Models.pdf]]
