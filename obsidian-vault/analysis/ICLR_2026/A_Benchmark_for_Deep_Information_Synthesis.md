---
title: "A Benchmark for Deep Information Synthesis"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Benchmark_for_Deep_Information_Synthesis.pdf
project_link: null
code_link: null
aliases:
- BDIS
- DEEPSYNTH
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/robustness
core_operator: "工具增强（尤其是网络搜索和代码解释器）是提升性能的主要可调节变量。提供中间推理步骤（Intermediate Steps）也能显著提升性能，例如Smolagent (GPT-4.1) + Intermediate Step的F1从6.33提升至10.50。"
primary_logic: "DEEPSYNTH基准测试揭示了当前最先进的LLM和深度研究智能体在真实世界、多步骤信息综合任务上的根本性不足。最佳模型（o3-deep-research）的F1得分仅为8.97，且仅能解决120个任务中的3个。这表明，尽管模型在简单事实检索上表现良好，但在需要跨多个来源进行规划、导航、提取和推理的综合任务上，能力严重欠缺。"
claims:
- "最佳模型o3-deep-research的F1得分仅为8.97，精确匹配（EM）得分为2.50。"
- "所有模型在非洲相关任务上的F1得分为0.0。"
- "提供中间步骤后，Smolagent (GPT-4.1)的F1得分从6.33提升至10.50，EM从7.14提升至10.0。"
- "OWL (GPT-4.1)的错误分析显示，导航错误和综合错误是最主要的错误类型。"
---

# A Benchmark for Deep Information Synthesis

> [!tip] 核心洞察
> DEEPSYNTH基准测试揭示了当前最先进的LLM和深度研究智能体在真实世界、多步骤信息综合任务上的根本性不足。最佳模型（o3-deep-research）的F1得分仅为8.97，且仅能解决120个任务中的3个。这表明，尽管模型在简单事实检索上表现良好，但在需要跨多个来源进行规划、导航、提取和推理的综合任务上，能力严重欠缺。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 深度信息合成基准 |
| 英文题名 | A Benchmark for Deep Information Synthesis |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=0Dhpt9aY3n) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/robustness |
| Method | DEEPSYNTH |
| Dataset | DEEPSYNTH, DEEPSYNTH-Dev |

> [!tip] 效果简介
> - DEEPSYNTH 上，F1 Score 为 8.97，对比 3.05 (o4-mini)，变化 +5.92。
> - DEEPSYNTH 上，Exact Match 为 2.50，对比 0.0，变化 +2.50。
> - DEEPSYNTH 上，LLMJudge Score 为 17.5，对比 0.0，变化 +17.5。

## 概要

DEEPSYNTH 是一个专为评估智能体在真实世界、多步骤信息综合任务上表现而设计的基准测试。其核心发现是：当前最先进的 LLM 和深度研究智能体在此类任务上表现严重不足。最佳模型（o3-deep-research）的 F1 得分仅为 8.97，精确匹配（EM）得分为 2.50，且仅能解决 120 个任务中的 3 个。这揭示了当前智能体的关键瓶颈不在于推理能力本身，而在于获取推理所需信息的可用性，尤其是在需要从多个来源综合信息时。

该基准测试的方法论定位在于，它从数据源出发，通过假设生成与验证来设计任务，确保了答案不可通过直接查找获得。与主要依赖单一来源（如 Wikipedia）的现有基准不同，DEEPSYNTH 覆盖了 7 个领域、67 个国家的 223 个数据源，包含非英语和代表性不足的地区，旨在评估模型在复杂信息生态中的综合能力。

主要结果进一步证实了上述瓶颈。在消融实验中，提供中间推理步骤（Intermediate Steps）能显著提升性能，例如 Smolagent (GPT-4.1) + Intermediate Step 的 F1 从 6.33 提升至 10.50。此外，工具增强（尤其是代码解释器）是提升性能的主要可调节变量。然而，所有模型在非洲相关任务上的 F1 得分为 0.0，揭示了严重的地理政治偏差。错误分析也表明，导航错误和综合错误是最主要的失败模式。

当前智能体在需要跨多个来源综合信息的任务上表现极差，这一瓶颈并非源于推理能力本身，而是获取推理所需信息的可用性不足。现有基准测试（如Wei et al., 2025的工作）主要依赖从已知事实反向设计问题，且多集中于Wikipedia等单一知名来源的浅层事实检索，无法反映真实世界中多步骤、多源信息综合的复杂性。DEEPSYNTH基准测试正是为填补这一缺口而设计。

DEEPSYNTH的核心动机在于构建一个能够系统评估“深度信息综合”能力的测试平台。其任务设计方法从根本上区别于以往：从数据源出发，先由16位专家提出多样化数据源和主题，标注者据此生成可验证假设，再对数据源进行详细分析验证假设，最后制定包含中间步骤、支持证据和答案的任务。所有任务经过第二位标注者独立验证，仅保留答案一致的任务。这一流程确保了任务答案无法通过直接查找获得，且需要智能体执行规划、导航、提取和推理等多步操作（Figure 1）。

基准测试覆盖7个领域、67个国家的223个数据源，包含非英语和代表性不足的地区，旨在评估模型在全球信息生态系统中的表现。评估指标上，DEEPSYNTH同时使用严格的精确匹配（EM）、F1分数以及一个软性的LLM-as-a-judge指标，以捕捉语义等价和微小数值偏差。

实验结果表明，当前最先进的模型和深度研究智能体在DEEPSYNTH上表现严重不足。最佳模型（o3-deep-research）的F1得分仅为8.97，精确匹配（EM）得分为2.50，且仅能解决120个任务中的3个（Table 2）。推理模型（如Gemini-2.5-Pro, GPT-5.1, DeepSeek-R1）与通用LLM（如GPT-4.1）在F1得分上的差距很小，这直接支持了“瓶颈不在推理，而在信息可用性”的核心洞察。工具增强（尤其是网络搜索和代码解释器）是提升性能的主要可调节变量，提供中间推理步骤也能显著提升性能，例如Smolagent (GPT-4.1) + Intermediate Step的F1从6.33提升至10.50（Table 3）。错误分析显示，导航错误和综合错误是最主要的失败模式（Table 4）。

此外，所有模型在非洲相关任务上的F1得分为0.0（Table 5），揭示了严重的地理政治偏差，这进一步凸显了当前模型在处理代表性不足地区数据时的根本性缺陷。

## 核心方法与创新机理

DEEPSYNTH 的核心创新不在于提出一个新的模型或算法，而在于构建了一个能够揭示当前智能体根本瓶颈的评估框架。其关键创新体现在三个 changed slots 上：

1.  **任务设计方法**：从“事实导向”转向“假设驱动”。传统基准（如 Wei et al., 2025）从已知事实反向设计问题，导致答案可通过直接查找获得。DEEPSYNTH 则从数据源出发，经过“提出假设 → 验证假设 → 设计任务”的流程（Section 2.2），确保答案必须通过跨来源综合推理才能得出，无法被简单记忆或检索。

2.  **评估指标**：引入多层级指标体系。在保留严格精确匹配（EM）和 F1 的基础上，额外采用 LLM-as-a-judge 软指标（Section 3），用于捕捉语义等价和微小数值偏差（如“U.S.” vs. “United States”或 1%–5.5% 的数值误差）。这一设计避免了单一硬指标对部分正确输出的误判。

3.  **数据来源多样性**：大幅扩展覆盖范围。不同于以往主要依赖单一知名来源（如 Wikipedia）的基准，DEEPSYNTH 覆盖 7 个领域、67 个国家的 223 个数据源，并刻意纳入非英语和代表性不足的地区（如非洲）。这一设计直接暴露了模型在数据稀疏区域的灾难性失败（非洲任务 F1=0.0，Table 5）。

**核心洞察**：实验证据表明，当前瓶颈不在于推理能力，而在于获取推理所需信息的可用性。推理模型（如 Gemini-2.5-Pro, DeepSeek-R1）与通用 LLM（如 GPT-4.1）在 F1 上的差距很小（Section 4.1），而提供中间步骤（Intermediate Steps）却能带来显著提升——Smolagent (GPT-4.1) 的 F1 从 6.33 跃升至 10.50，EM 从 7.14 升至 10.0（Table 3）。这揭示了因果机制中的关键可调节变量：**工具增强（尤其是代码解释器）和显式规划引导**是提升性能的主要杠杆，而非模型本身的推理能力。

![[assets/figures/papers/iclr26_0001_0Dhpt9aY3n_A_Benchmark_for_Deep_Information_Synthesis/figures/002_Figure_2.jpg]]
*Figure 2: An overview of our data collection process for building the DEEPSYNTH benchmark*

DEEPSYNTH基准测试的构建与评估遵循一个可复现的、以数据源为起点的逆向设计流程，其核心pipeline由四个依次执行的模块组成：**数据源识别 → 假设生成 → 假设验证 → 任务制定**（Figure 2）。该流程与现有基准（如Wei et al., 2025）从已知事实反向设计问题的做法不同，其关键创新在于：标注者首先从真实数据源出发提出可验证的假设，再对数据源进行详细分析以确认假设的有效性，最后才制定问题、中间步骤、支持证据和封闭形式的答案。所有任务均要求模型输出JSON格式（或JSON对象列表）的答案，且需通过第二位标注者的独立验证——仅当两位标注者的答案完全一致时任务才被保留，从而确保答案的可自动验证性和时间稳定性。

在评估层面，DEEPSYNTH同时采用三个互补的指标：**精确匹配（EM）** 要求所有键值对完全正确，适用于超过95%答案为数值型且键对应明确事实字段的场景；**F1分数** 通过检查键值对的正确比例实现部分匹配评估；**LLM-as-a-judge** 作为软性指标，能够捕捉语义等价（如"U.S." vs. "United States"）并容忍约1%–5.5%的数值偏差。这种三级评估体系的设计动机在于：单纯的EM过于严苛（最佳模型仅2.50），而LLM Judge可能引入新的偏差，F1则在两者之间提供了平衡的粒度。

整个基准测试的输入输出流可概括为：输入是一个包含问题描述、领域标签、地区标签和可选中间步骤的DEEPSYNTH任务；模型（无论是纯LLM还是基于智能体框架的系统）需通过多步操作（包括网络浏览、多源信息收集、推理和答案生成）输出结构化的JSON答案；输出通过上述三个指标与人工标注的标准答案进行比对。该pipeline的关键瓶颈不在于模型的推理能力本身（推理模型与通用LLM在F1得分上的差距很小），而在于获取推理所需信息的可用性——这体现在所有模型在非洲相关任务上F1得分为0.0，以及OWL (GPT-4.1)的错误分析中导航错误和综合错误是最主要的失败类型。

### 基准构建模块

DEEPSYNTH 基准的构建流程包含四个核心模块，其设计旨在避免模型通过直接检索已知事实即可作答：

1. **数据源识别**：由 16 位人类专家提出覆盖 7 个领域、67 个国家的 223 个多样化数据源，确保任务不依赖单一知名来源（如 Wikipedia）。
2. **假设生成**：标注者基于选定数据源提出 1-2 个可验证的假设，这些假设是“从数据中可推断出的合理见解”，而非直接可查的事实。
3. **假设验证**：标注者对数据源进行详细分析以验证假设有效性，生成中间步骤、支持证据和答案。
4. **数据验证**：由第二位标注者独立回答问题，仅保留两位标注者答案完全一致的任务，确保答案的封闭性和可验证性。

这一流程的因果逻辑在于：**从数据源出发而非从已知事实出发**，迫使任务答案无法通过简单检索获得，从而测量模型真正的信息综合能力。

### 评估指标模块

基准采用三级评估体系，各有侧重：

- **精确匹配（EM）**：要求输出 JSON 的所有键和值完全正确。论文指出超过 95% 的答案为数值型，且所有键对应无歧义的事实字段，因此 EM 在此场景下是合适的严格指标。
- **F1 分数**：计算正确键值对占总键值对的比例，报告精确率、召回率和 F1，用于部分正确性评估。
- **LLM-as-a-Judge 软指标**：作为补充指标，用于捕捉语义等价输出（如“U.S.” vs “United States”）并容忍约 1%-5.5% 的数值偏差。

**关键公式**——归一化相似度分数（用于 LLM Judge 的精确度计算）：

$$1 - \frac{|\text{correct\_answer} - \text{extracted\_final\_answer}|}{\max(|\text{correct\_answer}|, |\text{extracted\_final\_answer}|)}$$

该公式计算数值答案的归一化相似度，作为 LLM Judge 指标中精确度（precision）的评分依据。当两个数值完全相等时得分为 1，偏差越大得分趋近于 0。

### 工具增强与推理链消融模块

消融实验揭示了两个关键可调节变量：

1. **工具增强**：代码解释器（Code Interpreter）对性能提升贡献最大，网络搜索次之。这直接支持了论文的核心结论——瓶颈在于信息可用性而非推理能力。
2. **中间步骤（Intermediate Steps）**：提供中间推理步骤能显著提升性能。具体数据为：GPT-4.1 + Intermediate Step 的 F1 从 3.46 提升至 9.36，EM 从 0.0 提升至 5.0；Smolagent (GPT-4.1) + Intermediate Step 的 F1 从 6.33 提升至 10.50，EM 从 7.14 提升至 10.0。

### 错误分析模块

对 OWL (GPT-4.1) 的错误分析（Table 4）显示，**导航错误**和**综合错误**是最主要的错误类型，进一步印证了核心瓶颈在于信息获取与多源整合，而非单纯的推理失败。

### 公式变量含义

| 变量 | 含义 |
|------|------|
| `correct_answer` | 标准答案中的数值 |
| `extracted_final_answer` | 模型输出中提取的最终数值 |
| `abs(...)` | 绝对值函数 |
| `max(...)` | 取最大值函数 |

## 实验与关键发现

### 主结果：DEEPSYNTH 基准测试上的性能表现

DEEPSYNTH 基准测试揭示了当前最先进的 LLM 和深度研究智能体在真实世界、多步骤信息综合任务上的根本性不足。表 2 展示了所有模型在 120 个任务上的 Pass@1 性能对比。最佳模型 o3-deep-research 的 F1 得分仅为 8.97，精确匹配（EM）得分为 2.50，LLM Judge 得分为 17.5。更值得注意的是，它仅能解决 120 个任务中的 3 个。作为对比，最强的 LLM 基线模型 o4-mini 的 F1 得分为 3.05，EM 得分为 0.0，LLM Judge 得分为 0.0。这表明，尽管深度研究智能体框架（如 o3-deep-research）相比基础 LLM 有显著提升（F1 提升 +5.92，EM 提升 +2.50），但整体性能仍然极低，远未达到实用水平。

![[assets/figures/papers/iclr26_0001_0Dhpt9aY3n_A_Benchmark_for_Deep_Information_Synthesis/figures/005_Table_2.jpg]]
*Table 2: Performance comparison on the DEEPSYNTH benchmark (Pass@1). F1, Precision, Recall and Exact Match measure the quality of model predictions. LLM Judge (%) reports the average precision. Models with  are models or framework which are closed, while  are open-source*

在 DEEPSYNTH-Dev 子集上（表 13），o3-deep-research 的 F1 得分为 9.88，LLM Judge 得分为 20.0，与主基准测试的结果一致。推理模型（如 Gemini-2.5-Pro, GPT-5.1, DeepSeek-R1）与通用 LLM（如 GPT-4.1）在 F1 得分上的差距很小（例如 GPT-5.2-Pro 的 F1 为 8.70，而 GPT-4.1 为 3.46），这一发现证实了关键瓶颈不在于推理能力本身，而在于获取推理所需信息的可用性。

### 消融研究：工具与推理链的影响

表 3 的消融实验揭示了两个关键的因果调节变量：

![[assets/figures/papers/iclr26_0001_0Dhpt9aY3n_A_Benchmark_for_Deep_Information_Synthesis/figures/008_Table_3.jpg]]
*Table 3: Ablation Study. Tool Ablation: Comparing the benefits of using different tools on DEEP-SYNTH. Reasoning Chain Ablation: Studying the role of planning given the intermediate steps*

1. **工具增强**：对 OWL (GPT-4.1) 的工具消融实验显示，代码解释器（Code Interpreter）对性能提升贡献最大。完整工具集（Web Search + Code Interpreter + Web Browser）的 F1 得分为 5.41，而移除代码解释器后，F1 降至 3.16，表明数值计算和数据处理能力是综合任务的关键支撑。

2. **提供中间步骤（Intermediate Steps）**：这是提升性能最有效的单一干预。GPT-4.1 在获得中间步骤后，F1 从 3.46 提升至 9.36（+5.90），EM 从 0.0 提升至 5.0。Smolagent (GPT-4.1) 的 F1 从 6.33 提升至 10.50（+4.17），EM 从 7.14 提升至 10.0。这证实了规划能力（即分解任务为可执行的子步骤）是信息综合的关键瓶颈。

### 错误分析：导航与综合是主要失败模式

表 4 对 OWL (GPT-4.1) 的错误分析显示，导航错误（Navigation errors）和综合错误（Synthesis errors）是最主要的错误类型。导航错误指智能体无法找到正确的数据源或网页，综合错误指智能体无法将来自多个来源的信息整合成一致的答案。图 9 展示了一个典型的失败案例：OWL 找到了正确的 URL，但未能从网站的数据库界面查询到正确的数据，随后又尝试从错误的 URL 下载数据文件，导致“未找到”错误。这揭示了当前智能体在复杂、非结构化的网络环境中进行有效信息检索和整合的根本性缺陷。

![[assets/figures/papers/iclr26_0001_0Dhpt9aY3n_A_Benchmark_for_Deep_Information_Synthesis/figures/012_Table_4.jpg]]
*Table 4: Error analysis for OWL (GPT-4.1). Navigation and synthesis errors are the most prominent*

### 区域分析：严重的地理政治偏差

表 5 的多区域分析揭示了严重的性能偏差。所有模型在非洲相关任务上的 F1 得分均为 0.0，而在欧洲和亚洲任务上的表现相对较好（例如 o3-deep-research 在欧洲任务上的 F1 为 13.33，在亚洲任务上为 6.67）。这一结果直接源于基准测试中数据源的地理分布不均——非洲地区的代表性严重不足。这不仅是基准测试的局限性，更暴露了当前 AI 系统在全球信息生态系统中的结构性偏见：模型在数据丰富的地区表现尚可，但在数据稀缺的地区完全失效。

![[assets/figures/papers/iclr26_0001_0Dhpt9aY3n_A_Benchmark_for_Deep_Information_Synthesis/figures/011_Table_5.jpg]]
*Table 5: Multi-Regional Analysis: Agent performance across region-specific tasks (F1 score). NOTE: A question may span multiple regions. “Others” contains tasks without regional association*

### 中间步骤准确率与错误传播

表 8 对 40 个任务的中间步骤准确率进行分析，揭示了严重的错误传播问题。例如，GPT-4.1 在第 1 步的 F1 为 59.1%，但到第 4 步时降至 18.2%；其错误传播率（Prop.）在第 1 步到第 2 步为 100%，即所有在第 1 步失败的情况都导致第 2 步也失败。所有模型（包括 GPT-5.2 和 DeepSeek-R1）都表现出陡峭的准确率衰减和近乎完全的错误传播。这解释了为什么即使提供了中间步骤，整体性能仍然很低——错误在早期步骤中产生，并沿着推理链级联放大。

### 综合操作分析：异常检测相对容易

图 6 展示了模型在不同综合操作类型上的 F1 得分。o3 模型在异常检测（Anomaly Detection）任务上取得了最高的 F1 得分（26.51%），而在其他操作（如趋势识别、比较分析）上的表现普遍较低。这暗示了当前模型在处理需要识别模式偏差的任务上相对擅长，但在需要跨多个来源进行复杂推理和整合的任务上能力严重不足。

### Best-of-N 与自一致性

图 4b 的 Best-of-N 分析显示，在 DEEPSYNTH-Dev 上，Smolagents (GPT-4.1) 的 Best@5 LLM-Judge 准确率达到 25.0%，而 GPT-4.1 为 17.5%。然而，自一致性（Self-Consistency@5）仅产生 5% 的准确率，远低于 Best@5 的 25%。这一巨大差距表明，DEEPSYNTH 任务需要多样化的探索策略（Best-of-N 通过采样不同轨迹来探索解空间），而非简单的多数投票（自一致性假设正确解在多次采样中占多数）。这进一步证实了任务的开放性和复杂性。

![[assets/figures/papers/iclr26_0001_0Dhpt9aY3n_A_Benchmark_for_Deep_Information_Synthesis/figures/003_Table_1.jpg]]
*Table 1: DEEPSYNTH statistics across tasks*

## 定位与知识库关联

### 与现有基准的关系

DEEPSYNTH 定位为首个系统性评估多步、多源信息综合能力的基准。其核心设计差异体现在三个层面：

1. **任务构建逻辑**：不同于从已知事实反向设计问题（如 Wei et al., 2025），DEEPSYNTH 采用“数据源→假设→验证→任务”的正向流程。16 位专家先识别 223 个数据源（覆盖 67 个国家、7 个领域），再提出可验证假设，经分析确认后制定任务。这一机制旨在确保答案无法通过直接查找获得，且答案形式封闭可自动验证。

2. **评估体系**：同时使用精确匹配（EM）、F1 和 LLM-as-a-judge 软指标。EM 适用于 95% 以上为数值答案的任务；F1 捕获部分正确性；LLM Judge 容忍语义等价（如“U.S.”与“United States”）及约 1%–5.5% 的数值偏差。三者联合揭示出模型在严格匹配与语义近似之间的巨大鸿沟——例如某模型输出 `{“India”: 100.7, “U.S.”: 100.6, “China”: 7.8}`，EM=0.0，F1=33.3，LLM Score=0.0，说明 LLM Judge 并未因 F1 较高而放松评分。

3. **数据多样性**：相比主要依赖 Wikipedia 等单一知名来源的基准，DEEPSYNTH 涵盖非英语和代表性不足地区的数据源。但这一设计也暴露了自身偏差——欧洲和亚洲任务比例偏高，非洲任务极少，导致所有模型在非洲任务上 F1=0.0。

### 关键瓶颈与因果机制

实验证据指向一个清晰的因果链：

- **瓶颈不在推理能力**：推理模型（Gemini-2.5-Pro、GPT-5.1、DeepSeek-R1）与通用 LLM（GPT-4.1）在 F1 上的差距很小。o3-deep-research 虽为最佳模型（F1=8.97，EM=2.50），但仅能解决 120 个任务中的 3 个。
- **工具增强是主要可调节变量**：代码解释器对性能提升贡献最大。提供中间步骤（Intermediate Steps）使 GPT-4.1 的 F1 从 3.46 提升至 9.36，Smolagent (GPT-4.1) 从 6.33 提升至 10.50。
- **错误传播是核心失效模式**：中间步骤准确率随步数急剧衰减，且错误近乎完全传播（Propagation rate 接近 100%）。OWL (GPT-4.1) 的错误分析显示，导航错误和综合错误是最主要类型。

### 适用边界与局限

1. **地理政治偏差**：非洲任务 F1=0.0 是系统性的，不因模型或框架改变。标注者 75% 为男性、81.25% 拥有博士学位，可能引入人口统计学偏差。任务虽覆盖 42 个国家，但数据源多样性仍不足以代表全球信息生态。

2. **答案形式限制**：所有任务要求封闭式 JSON 输出，无法评估开放形式、论证充分的答案。这对衡量深度研究智能体的“研究质量”构成根本性限制。

3. **标注成本**：平均每个任务耗时 5.5 小时，依赖专家标注，可扩展性有限。

4. **预训练数据污染**：尽管设计了防记忆措施（如使用非英语源、动态数据），但无法完全排除。

5. **LLM Judge 的潜在偏差**：软指标本身可能引入新的不一致性，实验中也观察到 LLM Judge 与 F1 之间存在持续差距。

### 开放问题

1. **探索 vs. 多数投票**：自一致性（Self-Consistency@5）仅产生 5% 准确率，远低于 Best@5 的 25%。这表明任务需要多样化的探索路径，而非简单的多数投票——但如何有效引导探索仍不明确。

2. **导航与综合的改进**：导航错误和综合错误是最主要的失效模式。如何设计智能体在大型信息空间中减少幻觉和推理错误？提供中间步骤有效但不够，需要更根本的规划与回溯机制。

3. **全球代表性**：如何构建更平衡、更具全球代表性的信息综合基准？非洲等地 F1=0.0 的问题不仅是数据问题，也反映了当前智能体在处理非英语、非结构化、低可见性数据源时的系统性缺陷。

4. **评估框架的扩展**：如何设计能衡量开放形式、论证充分答案的评估方法？这需要超越封闭式 JSON 匹配的范式。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Benchmark_for_Deep_Information_Synthesis.pdf

![[paperPDFs/ICLR_2026/A_Benchmark_for_Deep_Information_Synthesis.pdf]]
