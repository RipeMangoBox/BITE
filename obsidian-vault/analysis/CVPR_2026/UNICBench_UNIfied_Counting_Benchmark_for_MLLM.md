---
title: "UNICBench: UNIfied Counting Benchmark for MLLM"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/UNICBench_UNIfied_Counting_Benchmark_for_MLLM.pdf
project_link: null
code_link: null
aliases:
- UUMCB
- UNICBench
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 统一的、跨模态的标准化评估协议（固定分割、提示、解码设置与匹配规则）与分层难度/能力分类法，能够揭示模型在计数任务上的具体弱点和性能天花板。
primary_logic: 通过构建覆盖图像、文本、音频三种模态的统一计数基准UNICBench，系统性地评估了45个最先进MLLM，发现模型在基础计数（L1）上表现尚可，但在需要语义筛选、去重和推理的L2/L3任务以及高难度样本上性能急剧下降；音频计数错误主要源于事件分割的类别性失败而非数量误差。
claims:
- 在图像计数中，仅三个模型在20%容错率下命中率超过50%，且误差随难度单调递增。
- 文本计数中，结构复杂的类别（如LaTeX、代码）产生显著更高的MAE，推理层级（L3）误差最大。
- 音频计数中，精确匹配、10%和20%误差阈值下的准确率几乎无差别，表明错误是类别性而非轻微偏差。
- 思维链模式在文本高计数样本上显著优于非思维链模式，但无法完全解决极端情况。
---

# UNICBench: UNIfied Counting Benchmark for MLLM

> [!tip] 核心洞察
> 通过构建覆盖图像、文本、音频三种模态的统一计数基准UNICBench，系统性地评估了45个最先进MLLM，发现模型在基础计数（L1）上表现尚可，但在需要语义筛选、去重和推理的L2/L3任务以及高难度样本上性能急剧下降；音频计数错误主要源于事件分割的类别性失败而非数量误差。

| 字段 | 内容 |
|------|------|
| 中文题名 | UNICBench: 面向多模态大语言模型的统一计数基准 |
| 英文题名 | UNICBench: UNIfied Counting Benchmark for MLLM |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.00595) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | UNICBench (Unified Multimodal Counting Benchmark) |
| Dataset | UNICBench Image Track, UNICBench Text Track, UNICBench Audio Track |

> [!tip] 效果简介
> - UNICBench Image Track 上，Overall MAE N/A vs InternVL3.5-241B-A28B: 59.9; GPT-5-mini: 29.8 (N/A)；HitRate@100% N/A vs InternVL3.5-241B-A28B: 21.9%; GPT-5-mini: 17.2% (N/A)。
> - UNICBench Text Track 上，Overall MAE N/A vs Gemini-2.5-Pro-Thinking: 30.5; DeepSeek-R1-0528: 34.6 (N/A)。
> - UNICBench Audio Track 上，Success Rate N/A vs Gemini-2.5-Pro-Thinking: 64.0%; Voxtral-mini: 99.8% (N/A)。

## 概要

多模态大语言模型（MLLM）在视觉问答、文档理解等任务上取得了显著进展，但在**精确计数**这一基础能力上仍面临严峻挑战。现有计数评估多局限于单一模态或特定场景，缺乏统一的跨模态基准来系统诊断模型的计数瓶颈。为此，本文提出 **UNICBench**——首个覆盖图像、文本、音频三模态的统一计数基准，包含约 5,300 张图像（5,508 条问答）、872 个文档（5,888 条问答）和 2,069 个音频片段（2,905 条问答），并对 45 个最先进的 MLLM 进行了标准化评估。

### 核心问题与瓶颈

当前 MLLM 在计数任务上的主要瓶颈并非数值输出格式或基本感知能力，而是**缺乏跨模态的通用推理能力**。这导致模型在以下场景出现大量长尾错误：

- **语义过滤与去重**：需要根据属性筛选实体或消除重复项时（L2 语义级计数）；
- **规则驱动推理**：涉及多步算术或逻辑聚合时（L3 推理级计数）；
- **高难度样本**：高密度场景、长文档、时间重叠音频等。

### 核心方法与定位

UNICBench 通过以下机制实现统一评估：

1. **分层能力分类法**：将计数任务划分为三个递进层级——
   - **L1 感知级**：$y = |E|$，直接观察实体集大小；
   - **L2 语义级**：$y = |\{ e \in E \mid P(e) \}|$，按谓词条件筛选计数；
   - **L3 推理级**：$y = g(|S_1|, \dots)$，基于子集大小的算术/逻辑函数。

2. **统一评估协议**：固定系统提示、分割策略、解码参数（temperature=0.0, max tokens=4096）和答案匹配规则，确保跨模型可比性。

3. **多维度指标体系**：采用 **SuccessRate**（可解析数值预测比例）、**MAE/MSE**（绝对/平方误差）和 **HitRate@τ**（相对误差容限内命中率）三重指标，从鲁棒性、精度和容错性三个维度刻画模型表现。

在方法谱系上，UNICBench 不同于传统的密度估计（CSRNet 等）、检测后计数（LSC-CNN 等）或点监督方法（P2PNet 等），也区别于仅关注单一模态的 LLM 计数评测，而是首次建立了**跨模态、分层级、标准化**的 MLLM 计数能力诊断框架。

### 核心发现

- **图像计数**：仅三个模型在 20% 容错率下命中率超过 50%，误差随难度单调递增（Table 2）；高密度类别（如 crowd、tree）的 MAE 显著偏高（Figure 28）。
- **文本计数**：结构复杂的类别（LaTeX、代码）产生显著更高的 MAE（Figure 30），推理层级误差最大；思维链模式在极端高计数样本上优于非思维链模式，但无法完全解决长尾问题（Figure 5）。
- **音频计数**：精确匹配、10% 和 20% 误差阈值下的准确率几乎无差别（Figure 25），表明错误是**类别性失败**（事件分割错误）而非轻微数值偏差；环境音相对容易，对话语音产生不成比例的大误差（Figure 32）。

这些发现揭示了 MLLM 在计数任务上的**性能天花板**和**模态特异性弱点**，为后续改进提供了明确的诊断方向。

### 计数任务的核心地位与模态泛化困境

计数是视觉理解、文档分析、音频事件检测等众多领域的基石任务，其本质是从非结构化数据中提取可量化的语义信息。然而，当前多模态大语言模型（MLLM）的评估体系存在一个显著盲区：计数能力通常被淹没在通用问答或视觉定位等复合评测中，缺乏一个跨模态、标准化、难度分层的统一基准。这导致两个关键问题悬而未决——**不同模态下计数错误的根源是否同构？模型在基础感知计数与需要语义筛选、去重、推理的复杂计数之间，性能衰减的拐点在哪里？**

### 现有方法的三个结构性缺口

**缺口一：模态割裂的评估范式。** 图像计数领域长期依赖密度估计（如CSRNet、ChfL、STEERER）、检测后计数（如LSC-CNN、TopoCount）和点监督方法（如P2PNet）等专用架构，评测指标以MAE/MSE为主，但仅覆盖视觉模态。文本和音频计数则缺乏系统化的基准，偶有工作探索LLM的提示计数或思维链计数，却未形成跨模态的统一框架。这使研究者无法判断一个模型的计数能力是模态特化的还是通用的。

**缺口二：难度与能力维度的混淆。** 现有评测往往将“计数”视为单一维度的任务，忽略了其内部的能力层级差异。从直接感知实体集大小（$y = |E|$）到语义过滤（$y = |\{ e \in E \mid P(e) \}|$）再到基于子集计数的逻辑推理（$y = g(|S_1|, \dots)$），认知负荷呈阶梯式上升。若不区分这些层级，模型在简单样本上的高准确率会掩盖其在复杂推理级任务上的系统性失败。

**缺口三：评估协议的标准化缺失。** 不同工作使用不同的提示模板、解码参数、答案解析规则和容错阈值，导致结果不可比。部分模型因输出格式不兼容而被低估，另一些则因宽松的匹配规则而虚高。缺乏统一的系统提示、固定随机种子、标准化分割与匹配规则，使得“计数能力排行榜”缺乏可信度。

### 本文动机与核心设计思路

针对上述缺口，UNICBench提出一个覆盖图像、文本、音频三种模态的统一计数基准，核心设计遵循三条原则：

1. **跨模态统一架构**：所有模态共享同一套QA-证据JSON模式、能力层级标签（L1感知/L2语义/L3推理）和难度分层（Easy/Medium/Hard），确保跨模态可比性。
2. **标准化评估协议**：固定系统提示、temperature=0.0（或标注默认值）、max tokens=4096，并对不同模型的包裹格式（`<think>`、`<answer>`、`<begin of box>`等）做适配解析，以消除格式偏差。
3. **大规模模型覆盖**：在统一协议下评估45个最先进MLLM，涵盖闭源与开源模型，从InternVL3.5-241B-A28B到Gemini-2.5-Pro-Thinking、GPT-5-mini等，形成迄今最大规模的跨模态计数能力全景图。

通过这一设计，UNICBench不仅提供了模型排名的“体检报告”，更试图揭示计数能力的长尾错误模式、模态特异的失败机制，以及思维链推理在高难度样本上的真实增益边界。

## 核心方法与创新机理

UNICBench 的核心创新不在于提出新的计数模型，而在于构建了首个跨图像、文本、音频三模态的统一计数评估基准，并以此揭示了当前多模态大语言模型（MLLM）在计数任务上的系统性瓶颈。

### 1. 跨模态统一评估框架

此前计数评估多局限于单一模态（如图像中的目标计数或文本中的模式匹配），缺乏统一的跨模态比较基准。UNICBench 将图像、文本、音频三种模态纳入同一评估体系，采用标准化的系统提示、固定随机种子、统一的分割与解码参数（temperature=0.0, max tokens=4096），以及适配多种模型输出格式的答案提取器，确保不同模型间的可比性。这种统一协议使得跨模态的计数能力差异得以量化——例如，图像计数中仅三个模型在20%容错率下命中率超过50%（Table 2），而音频计数中精确匹配与放宽阈值后的准确率几乎无差别（Figure 25），揭示了不同模态下错误模式的本质差异。

### 2. 分层能力-难度分类法

UNICBench 将计数任务按认知需求划分为三个层级（L1-L3），并依据样本特征标注难度（Easy/Medium/Hard），形成二维分析矩阵：

- **L1 感知级计数**：直接统计实体集合大小，$y = |E|$，如“图中有几辆车？”
- **L2 语义级计数**：需根据语义谓词过滤实体，$y = |\{ e \in E \mid P(e) \}|$，如“图中有几辆红色轿车？”
- **L3 推理级计数**：需对多个子计数结果进行算术或逻辑运算，$y = g(|S_1|, \dots)$，如“红色轿车比蓝色SUV多几辆？”

这一分类法直接暴露了 MLLM 的核心弱点：模型在 L1 任务上表现尚可，但在 L2/L3 任务上性能急剧下降。例如，文本计数中 L3 推理级任务的 MAE 显著高于 L1 感知级（Table 3），图像计数中误差随难度单调递增（Figure 22）。这表明当前 MLLM 的瓶颈并非基础感知，而是缺乏跨模态的通用推理能力，无法有效执行语义过滤、去重和规则驱动的聚合操作。

### 3. 统一QA-证据模式与多源数据整合

UNICBench 设计了跨模态统一的 JSON 问答与证据格式，要求标注提供证据链（evidence），确保标注一致性和可追溯性。数据来源涵盖图像计数数据集（FSC147、NWPU-MOC、CARPK 等）、自建文本语料（包含 LaTeX、代码、长文档等结构复杂类别）以及音频数据集（DESED、AliMeeting），覆盖了从稀疏（如飞机平均5.58个实例）到高密度（如人群355.58个实例）的广泛计数范围（Section 3.3）。这种多源整合使得评估能够覆盖传统基准难以触及的长尾困难样本——例如文本中字符长度跨度从584到8,052,974字符（median: 7,176），音频中时间重叠事件和背景噪声场景。

### 4. 系统性能力诊断

通过45个最先进 MLLM 的大规模评估，UNICBench 揭示了几个关键发现，这些发现构成了对现有模型能力的精确诊断：

- **图像计数**：提高图像分辨率对超高密度场景的提升有限，存在表征瓶颈（Section 4.3）；长尾极端错误（如罕见类别、标签噪声）显著拉高 MAE/MSE，即使中位误差较小（Figure 4）。
- **文本计数**：结构复杂类别（如 LaTeX、代码）产生显著更高的 MAE（Figure 30）；思维链（CoT）模式在高计数样本上显著优于非 CoT 模式，但无法完全解决极端情况（Figure 5）。
- **音频计数**：精确匹配、10%和20%误差阈值下的准确率几乎无差别，表明错误是类别性的（如事件分割失败）而非轻微数值偏差（Figure 25）；环境声相对容易，会话语音产生不成比例的大误差（Figure 32）。

这些诊断性发现超越了简单的性能排名，为后续改进提供了明确的指向——例如，音频计数需要改进事件分割架构，文本计数需要增强长文档的跨段落语义去重能力，图像计数需要突破高密度场景的表征瓶颈。

UNICBench 构建了一套端到端的统一评估流水线，将多模态计数任务标准化为可比较的评测范式。整个框架围绕四个核心模块展开：多源数据收集、统一 QA-证据模式构建、能力与难度标注、以及标准化评估协议执行。

**多源数据收集** 模块汇聚了图像、文本、音频三个模态的计数数据。图像样本来自 FSC147、NWPU-MOC、CARPK、JHU-CROWD++、UCF-QNRF 等经典计数数据集；文本样本为自建语料，涵盖 LaTeX 公式、代码片段、长文档等多种结构复杂类别；音频样本则来源于 DESED 和 AliMeeting 等事件检测与会议场景数据集。这种跨模态、跨来源的数据汇聚策略，确保了基准在计数场景上的广泛覆盖。

**统一 QA-证据模式** 将所有模态的标注统一为 JSON 格式的问答对，每条样本包含问题文本、数值答案以及可选的证据链。该模式的设计原则是“先证据后答案”（evidence-first GT），即标注者需先明确计数的依据实体或规则，再给出最终数值，从而为后续的错误归因分析提供可追溯的中间信息。

**能力与难度标注** 模块是框架的分类学核心。每道题目按计数所需的认知层级被标注为三级：
- **L1 感知级**：直接计数实体集 $E$ 的大小，$y = |E|$；
- **L2 语义级**：计数满足谓词 $P(e)$ 的实体子集，$y = |\{ e \in E \mid P(e) \}|$；
- **L3 推理级**：基于多个子集计数结果进行算术或逻辑运算，$y = g(|S_1|, \dots)$。

同时，根据真实计数值的分布密度，样本被划分为 Easy、Medium、Hard 三个难度层级，形成 $3 \times 3$ 的能力-难度交叉分类矩阵。

**标准化评估协议** 是流水线的执行末端。所有模型在统一配置下运行：系统提示固定、最大输出 token 数 4096、温度设为 0.0（不支持温度调节的模型使用默认值并在结果中注明）、超时时间 120 秒。答案提取器针对不同模型的包裹格式（如 `<think>`、`<answer>`、`<begin of box>` 等标签）做了适配，以减少格式偏差。评估指标包括成功率（Success Rate）、平均绝对误差（MAE）、均方误差（MSE）以及多级容错命中率（HitRate@100%/90%/80%），从输出鲁棒性、数值精度和近似能力三个维度全面刻画模型表现。

流水线的输入是原始多模态数据与计数问题，输出是 45 个 MLLM 在三个模态赛道上的标准化性能剖面。这一设计使得不同模态、不同模型的结果可以直接横向对比，同时保留了按能力层级和难度分层下钻分析的能力。

UNICBench 本身是一个统一评估基准，而非提出新模型架构，因此其“核心模块”体现为构建标准化评估管线的四个功能模块，以及配套的度量公式体系。

### 评估管线模块

**多源数据采集（Multi-source Data Collection）**：从既有计数数据集与自建语料中收集图像、文本、音频三模态样本。图像来源包括 FSC147、NWPU-MOC、CARPK、JHU-CROWD++、UCF-QNRF、ShanghaiTech、IOCfish5K 等经典计数数据集；文本与音频则通过自建方式补充（Section 3.2）。该模块决定了基准的跨模态覆盖广度和样本多样性。

**统一QA-证据模式（Unified QA-Evidence Schema）**：将跨模态数据统一为结构化 JSON 格式，每条样本包含问题（question）、答案（answer）与证据（evidence）三个字段。证据字段记录了计数目标的标注依据，使评估不仅关注最终数值，还可追溯模型的推理过程（Section 6.1）。这一设计为后续的层级能力分析提供了结构化基础。

**能力与难度标注（Capability & Difficulty Labeling）**：依据三级能力分类法为每道题目赋予层级标签：
- **L1 感知级（Pattern level）**：直接观察实体集 $E$ 并计数，$y = |E|$。
- **L2 语义级（Semantic level）**：需筛选满足谓词 $P(e)$ 的实体子集，$y = |\{ e \in E \mid P(e) \}|$。
- **L3 推理级（Reasoning level）**：基于多个子集大小进行算术或逻辑运算，$y = g(|S_1|, \dots)$。

同时，根据真实计数值的分布特征，将样本划分为 Easy / Medium / Hard 三个难度层级（Section 3.1）。这种双维度标注使得评估能够区分“模型在什么类型的计数任务上失败”。

**标准化评估协议（Standardized Evaluation Protocol）**：固定系统提示、解码参数（temperature=0.0, max tokens=4096）、解析器与匹配规则，对 45 个 MLLM 进行统一评估。对于不支持温度设置的模型（如 GPT-5 系列默认 temperature=1.0），在结果中注明差异（Section 4.2）。答案提取器针对不同模型的包裹格式（如 `<think>` / `<answer>` / `<begin of box>`）做了适配，以减少格式偏差。

### 关键公式与度量指标

**成功率（Success Rate）**：衡量模型能够输出可解析数值预测的样本比例，反映格式鲁棒性而非计数精度。

$$\mathrm{SuccessRate} = \frac{1}{N} \sum_{i=1}^N \mathbf{v}_i$$

其中 $\mathbf{v}_i \in \{0, 1\}$ 指示第 $i$ 个样本是否产生有效数值预测（Eq 1）。

**平均绝对误差与均方误差**：

$$\mathrm{MAE} = \frac{1}{N} \sum_{i=1}^N |\hat{y}_i - y_i|, \quad \mathrm{MSE} = \frac{1}{N} \sum_{i=1}^N (\hat{y}_i - y_i)^2$$

MAE 衡量平均偏差幅度，MSE 对极端错误施加更大惩罚（Eq 2）。

**命中率（Hit Rate）**：引入相对容错阈值 $\tau$，定义命中指示器 $\mathbf{1}_i^{(\tau)}$，当相对误差不超过 $\tau$ 时视为命中：

$$\mathrm{HitRate}@(1-\tau) = \frac{1}{N} \sum_{i=1}^N \mathbf{1}_i^{(\tau)}$$

典型阈值取 $\tau \in \{0, 0.10, 0.20\}$，对应精确匹配、10% 容错和 20% 容错（Eq 3-4）。该指标区分了“近似正确”与“精确正确”两种能力层次——实验表明，多数模型在 20% 容错下命中率显著提升，但精确匹配率普遍很低，说明模型具备粗略计数能力而缺乏精确计数能力。

**能力层级的形式化定义**：上述 L1-L3 的数学表述不仅是分类标签，更直接对应了任务难度的递增——L1 仅需感知存在性，L2 需理解语义属性并过滤，L3 需多步推理与聚合。实验一致表明，MAE 和 MSE 从 L1 到 L3 单调递增，验证了该分类法的有效性。

## 实验与关键发现

UNICBench对45个最先进MLLM在图像、文本、音频三个模态上进行了系统性评估。所有模型使用统一的系统提示、固定随机种子、标准化分割与解码参数（temperature=0.0, max tokens=4096），答案提取器针对不同模型的包裹格式（如`<think>`/`<answer>`/`<begin of box>`）做了适配，以减少格式偏差。评估指标包括Success Rate（可解析数值预测的样本比例）、MAE/MSE、以及在不同容错阈值（0%、10%、20%）下的Hit Rate。

### 图像计数赛道：精确计数仍是瓶颈

图像计数赛道的结果（Table 2）揭示了当前MLLM的一个核心矛盾：多数模型能达到100%的Success Rate，表明输出数值本身并非瓶颈，但精确计数能力严重不足。**仅三个模型在20%容错率下命中率超过50%**：InternVL3.5-241B-A28B、Gemini-2.5-Pro-Thinking和GPT-5-mini。具体而言，InternVL3.5-241B-A28B取得Overall MAE 59.9、HitRate@100% 21.9%，GPT-5-mini则为MAE 29.8、HitRate@100% 17.2%。放宽容错阈值后性能显著提升（Figure 21），说明模型具备较强的近似计数能力，但精确计数仍是瓶颈。

![[assets/figures/papers/paper_list_l2214_https_arxiv_org_abs_2603_00595/figures/005_Table_2.jpg]]
*Table 2: Benchmark results on the Image-modality counting track. Metrics are: SuccessRate (%), Hit rates (@100%/@90%@80%), MAE/MSE for Overall, per-difficulty, and per-capability. MSE values are shown in scientific notation with one decimal*

![[assets/figures/papers/paper_list_l2214_https_arxiv_org_abs_2603_00595/figures/006_Figure_4.jpg]]
*Figure 4: Distribution of prediction error on image modality. Whiskers and outliers indicate extreme failures—long whiskers or many outliers show a model makes severe errors on some samples (e.g., rare classes, label noise, or collapse cases). Such frequent extreme errors can substantially increase MAE/MSE even when the median error looks small.The model ordering is consistent with that in Table 2*

误差随难度单调递增。从L1（感知级）到L2（语义级）再到L3（推理级），MAE和MSE持续攀升（Figure 22），验证了分层分类法的有效性。Figure 4的箱线图进一步显示，长须和大量离群点表明模型在部分样本上出现严重错误（如稀有类别、标签噪声或模型崩溃），这些极端失败即使在中位误差较小时也能大幅推高MAE/MSE。

消融分析显示，提高图像分辨率对超高密度场景的提升有限，存在表征瓶颈——模型无法仅通过增加像素来克服密集场景中的目标重叠与遮挡问题。

### 文本计数赛道：结构复杂度决定误差天花板

文本计数赛道（Table 3）中，Gemini-2.5-Pro-Thinking取得Overall MAE 30.5，DeepSeek-R1-0528为34.6。误差同样随难度单调递增：以Gemini-2.5-Flash-Nothinking为例，Easy难度MAE仅7.4、MSE 2.6e4，而Hard难度MAE飙升至746.3、MSE达4.1e6。顶级闭源模型在Hard难度上的相对误差膨胀较小（Gemini-2.5-Pro-Thinking Hard MSE 1.2e6 vs GPT-5-mini Hard MSE 2.9e7），显示出更强的鲁棒性。

![[assets/figures/papers/paper_list_l2214_https_arxiv_org_abs_2603_00595/figures/007_Table_3.jpg]]
*Table 3: Benchmark results on the Text-modality counting track. Metrics are: SuccessRate (%), Hit rates (@100%/@90%@80%), MAE/MSE for Overall, per-difficulty, and per-capability. MSE values are shown in scientific notation with one decimal*

**结构复杂的类别产生显著更高的MAE**。Figure 30的类别级MAE热力图显示，LaTeX、代码等结构化文本的计数误差远大于普通自然语言文本，这是因为模型需要在解析语法结构的同时进行计数，双重认知负荷导致性能下降。推理层级（L3）误差最大，涉及多步推理和语义去重的任务仍是主要失败模式。

**思维链（CoT）模式在文本高计数样本上显著优于非CoT模式**。Figure 5的散点图清晰展示了这一现象：右上角绿色框标记的极端高计数样本中，thinking模式击败了non-thinking模式，这部分样本驱动了整体MAE差距的大部分。但CoT也无法完全解决极端情况，表明当前推理能力的上限仍然存在。

### 音频计数赛道：错误是类别性的而非数量性的

音频计数赛道（Table 4）的结果揭示了一个独特现象：**精确匹配、10%和20%误差阈值下的准确率几乎无差别**（Figure 25）。这说明音频计数错误并非轻微的数值偏差，而是类别性失败——模型要么完全正确，要么完全错误，很少出现“接近但偏差一点”的情况。错误类型分析（Figure 6）进一步表明，模型拒绝或无法产生数值输出时，这些错误不会计入MAE（但会在Success Rate中被惩罚），因此MAE可能低估了实际失败率。

![[assets/figures/papers/paper_list_l2214_https_arxiv_org_abs_2603_00595/figures/009_Table_4.jpg]]
*Table 4: Benchmark results on the audio-modality counting track. Metrics are: SuccessRate (%), Hit rates (@100%/@90%@80%), MAE/MSE for Overall, per-difficulty, and per-capability. MSE values are shown in scientific notation with one decimal. A “-” indicates that no valid values were obtained for this statistical dimension*

![[assets/figures/papers/paper_list_l2214_https_arxiv_org_abs_2603_00595/figures/036_Figure_25.jpg]]
*Figure 25: Audio modality accuracy comparison. Overall accuracy of audio-capable models under Exact Match, 10% error, and 20% error thresholds. Audio counting shows lower precision due to temporal ambiguity and variable acoustic patterns*

Gemini-2.5-Pro-Thinking在音频赛道取得64.0%的Success Rate，而Voxtral-mini高达99.8%，显示出专用音频模型在格式遵从性上的优势。从L1到L3，MAE和MSE持续增加（Figure 26），时间推理是音频计数的主要挑战。类别级分析（Figure 32）显示，环境声音相对容易，而对话语音产生不成比例的大误差，原因在于语音中的事件分割（如说话人转换、重叠语音）是类别性失败的主要来源。

### 跨模态对比：统一基准揭示的共性瓶颈

跨模态对比（Figure 7-11）揭示了各模态的不同计数特征：图像和音频集中在较低计数范围，而文本跨越最宽的计数范围（Figure 8）；文本问题长度显著更长且变化更大，反映了更高的语言复杂度和推理需求（Figure 10）；图像问题以L1模式级为主，文本包含大量L2和L3问题，音频则呈现更均衡的混合（Figure 9）。

![[assets/figures/papers/paper_list_l2214_https_arxiv_org_abs_2603_00595/figures/013_Figure_7.jpg]]
*Figure 7: Modality comprehensive comparison. The figure illustrates cross-modal distributions among image, text, and audio, comparing sample and question counts, average values, difficulty types, and count distributions*

综合三个赛道的结果，当前MLLM在计数任务上的核心瓶颈并非数值输出格式或基本感知，而是**缺乏跨模态的通用推理能力**。模型在L1基础计数上表现尚可，但在需要语义筛选、去重和推理的L2/L3任务以及高密度、长文档、时间重叠等困难样本上出现大量长尾错误。这一发现为未来MLLM的计数能力改进指明了方向：单纯提升感知精度或输出格式控制不足以解决问题，需要增强跨模态的语义理解和多步推理机制。

## 定位与知识库关联

**任务定位：跨模态统一计数评估**

UNICBench 将多模态大语言模型的计数能力定义为一种跨模态通用推理任务，而非单纯的感知或检测问题。该基准覆盖图像、文本、音频三种模态，构建了统一的 QA-证据格式与标准化评估协议，系统性地评估了 45 个最先进 MLLM。其核心贡献在于提出了一种分层能力分类法（L1 感知级 → L2 语义级 → L3 推理级）与难度分级体系（Easy/Medium/Hard），使得计数任务的评估从“能否数对”细化为“在何种条件下、以何种方式数错”。

**与经典计数方法的继承与分岔**

传统计算机视觉计数方法主要依赖密度估计、检测后计数、点监督和分割/聚类等范式。代表性工作包括密度估计路线中的 CSRNet、ChfL、STEERER，检测路线的 LSC-CNN、TopoCount，以及点监督方法 P2PNet 等。这些方法通常针对特定模态（以图像为主）和特定类别（如人群、细胞）进行优化，评估指标以 MAE/MSE 为主，但缺乏对语义筛选和推理能力的考察。

UNICBench 与上述路线的本质区别在于：它不提出新的计数模型，而是将 MLLM 作为通用计数代理，考察其跨模态、跨类别的零样本计数能力。这一设定使得评估重心从“特征提取与密度回归”转向“跨模态语义理解与推理”，从而揭示了经典方法无法触及的瓶颈——模型在 L2/L3 任务和高难度样本上的长尾错误。

**与 LLM 计数提示方法的关联**

近年来，研究者开始探索通过提示工程和思维链引导 MLLM 进行计数。UNICBench 在评估中直接对比了思维链模式与非思维链模式的性能差异：在文本计数的高计数样本上，思维链模式的 MAE 显著低于非思维链模式（Figure 5），但无法完全解决极端情况。这一发现表明，思维链推理能缓解部分计数错误，但当前 MLLM 的跨模态推理能力仍存在天花板。

**适用边界与公平性约束**

UNICBench 的评估协议通过固定系统提示、统一分割、固定温度（temperature=0.0）和最大 token 数（4096）等设置，最大程度保证了模型间的可比性。对于无法调整温度的模型（如 GPT-5 系列使用默认 temperature=1.0），结果中已注明。答案提取器针对不同模型的包裹格式（如 `<think>`、`<answer>`、`<begin of box>`）做了适配，减少了格式偏差。

然而，该基准的适用边界同样明确：它聚焦于单轮计数问答，未覆盖交互式或增量计数场景；音频模态评估受限于能处理音频的 MLLM 数量较少，部分模型因文件大小限制或 API 超时而失败，导致样本覆盖不完整。

**已知局限**

1. **统计显著性**：部分类别样本量较少，可能影响细粒度分析的可靠性。
2. **参数公平性**：某些模型无法完全统一推理参数（如温度），完全公平比较仍存在挑战。
3. **模态覆盖不均**：音频模态的评估模型数量远少于图像和文本，限制了跨模态结论的普适性。
4. **任务范围**：当前基准未涉及检测、分割等底层视觉能力与计数的联合评估。

**开放问题**

1. **高密度场景的表征瓶颈**：提高图像分辨率对超高密度场景的提升有限（Section 4.3），如何在 MLLM 架构层面突破表征瓶颈？
2. **音频时间推理**：音频事件计数中的时间重叠和背景噪声导致类别性失败（Figure 25），而非轻微偏差，如何通过改进模型架构解决？
3. **长文档语义聚合**：长文档中跨段落、跨页面的语义去重和聚合计数仍面临巨大挑战（Figure 30），未来方向是什么？
4. **混合推理架构**：能否设计一种融合符号推理与神经网络的混合计数方法，以减少 L3 推理级任务中的系统性错误？

## 原文 PDF

![[paperPDFs/CVPR_2026/UNICBench_UNIfied_Counting_Benchmark_for_MLLM.pdf]]
