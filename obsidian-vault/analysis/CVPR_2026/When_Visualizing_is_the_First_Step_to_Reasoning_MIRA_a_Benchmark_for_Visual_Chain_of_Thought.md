---
title: "When Visualizing is the First Step to Reasoning: MIRA, a Benchmark for Visual Chain-of-Thought"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/When_Visualizing_is_the_First_Step_to_Reasoning_MIRA_a_Benchmark_for_Visual_Chain_of_Thought.pdf
project_link: "https://mira-benchmark.github.io/"
code_link: null
aliases:
- WVIFSRMBVCT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 提供人工注释的中间视觉状态（Visual-CoT）作为推理过程的辅助线索。
primary_logic: 对于需要空间推理、几何操作或物理模拟的复杂问题，中间视觉表征是有效推理的关键第一步；视觉思维链弥补了纯文本思维链在表达这些信息上的不足。
claims:
- 在MIRA基准的直接输入设定下，没有任何MLLMs的准确率超过20%，即使是最强的GPT-5也只有16.5%。
- 当提供中间视觉线索（Visual-CoT）时，所有模型和任务的平均性能相对提升33.7%。
- Text-CoT对某些强模型（如Gemini 2.5 Pro和o3）反而降低了准确率（分别下降18.3%和14.0%），表明纯文本推理不足以应对MIRA的问题。
- 物理推理任务在从纯文本到Visual-CoT的条件下准确率几乎翻倍（从20.7%提高到40.0%）。
---

# When Visualizing is the First Step to Reasoning: MIRA, a Benchmark for Visual Chain-of-Thought

> [!tip] 核心洞察
> 对于需要空间推理、几何操作或物理模拟的复杂问题，中间视觉表征是有效推理的关键第一步；视觉思维链弥补了纯文本思维链在表达这些信息上的不足。

| 字段 | 内容 |
|------|------|
| 中文题名 | 可视化是推理的第一步：MIRA，一个视觉思维链基准 |
| 英文题名 | When Visualizing is the First Step to Reasoning: MIRA, a Benchmark for Visual Chain-of-Thought |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.02779) · [Project](https://mira-benchmark.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MIRA |
| Dataset | MIRA |

> [!tip] 效果简介
> - MIRA 上，Overall Accuracy (Direct) - vs GPT-5: 16.5% (无模型超过20%)；Overall Accuracy (Visual-CoT vs Direct) GPT-5-mini: 23.2% vs GPT-5-mini: 13.7% (+9.5% (绝对), 平均相对 +33.7%)。

## 概述

**核心问题：** 当前多模态大语言模型（MLLMs）在需要精确空间推理、几何操作或物理模拟的任务中存在根本性瓶颈——纯文本思维链（Text-CoT）无法有效表达和操作复杂的中间视觉状态，导致模型“想不清楚”那些必须“以图思考”的问题。

**关键发现：** MIRA基准的评估揭示了三个决定性证据：第一，在直接输入设定下，没有任何MLLMs的准确率超过20%，即使是当前最强的GPT-5也仅达16.5%；第二，当提供人工标注的中间视觉线索（Visual-CoT）时，所有模型和任务的平均性能相对提升33.7%；第三，Text-CoT对某些强模型（如Gemini 2.5 Pro和o3）反而产生负面影响，准确率分别下降18.3%和14.0%，表明纯文本推理不仅不足，甚至可能干扰模型对空间问题的判断。

**方法定位：** MIRA本身是一个诊断性基准，而非推理方法。它通过546个精心构建的多模态问题，覆盖欧几里得几何、物理推理、抽象空间逻辑谜题和因果转换四个领域，系统性地评估模型在三种输入条件下的表现：直接输入、文本思维链和模拟视觉思维链。其核心设计理念是：将中间视觉表征作为因果调节变量，解耦视觉信息与文本推理的贡献。

**主要结果：** 物理推理任务从Visual-CoT中获益最大，准确率从20.7%跃升至40.0%，几乎翻倍；而谜题类任务提升幅度较小，仅从9.5%增至10.5%。扩大搜索空间（Pass@k从1到4）可带来平均15.3%的提升，但k=4到8时增益趋缓至3.0%，说明MIRA任务的本质困难难以通过简单采样策略克服。

## 背景与动机

多模态大型语言模型（MLLMs）在现有视觉-语言基准上已展现出令人瞩目的性能。如 Figure 1 右侧所示，GPT-5、Gemini 2.5 Pro 和 o3 等领先模型在 MMMU、MMMU Pro、MMStar 和 RealWorldQA 等测试中均取得了高分。然而，这些基准主要考察模型对视觉内容的直接理解与文本回答能力，并未系统性地评估模型在需要“以图思考”的任务上的表现——即推理过程中必须生成或操作中间视觉表征才能得出正确答案的场景。

这一缺口构成了当前 MLLMs 的核心瓶颈：**纯文本推理无法准确捕捉和操作复杂的空间关系、几何结构与物理动态**。当问题涉及欧几里得几何中的点集操作、物理模拟中的力合成与运动轨迹推演、或因果转换中的多步状态预测时，仅靠文字描述往往难以承载推理所需的空间信息密度。正如 Figure 1 左侧的示例所示，人类可以自然地借助中间可视化来辅助推理，而现有 MLLMs 在缺乏这种视觉辅助时则暴露出显著的认知差距。

已有研究探索了文本思维链（Text-CoT）在纯文本推理中的作用，但将其直接应用于多模态空间推理任务时效果有限。问题在于，Text-CoT 以语言为载体，而语言在表达精确的空间拓扑、几何变换和物理约束时存在天然的带宽瓶颈——许多“一图胜千言”的信息难以被充分编码为文字。

为系统性地诊断这一瓶颈，MIRA（Multimodal Imagination for Reasoning Assessment）基准被提出。MIRA 的核心洞察是：**对于需要空间推理、几何操作或物理模拟的复杂问题，中间视觉表征是有效推理的关键第一步**；视觉思维链（Visual-CoT）弥补了纯文本思维链在表达这些信息上的不足。通过提供人工标注的中间视觉状态作为推理的辅助线索，MIRA 能够量化“可视化”对推理性能的因果贡献，从而揭示当前模型在自主生成和利用视觉思维方面的真实能力边界。

## 核心创新

MIRA 的核心创新并非提出一种新的模型架构或训练范式，而是**定义并系统化评估了一种被现有基准长期忽视的推理能力——视觉思维链（Visual Chain-of-Thought, Visual-CoT）**。其创新性集中体现在三个相互耦合的“changed slots”上：问题定义、评估协议与数据构造哲学。

### 1. 问题定义的升维：从“看图说话”到“以图思考”

现有主流多模态基准（如 MMMU、MMMU Pro、MMStar 等）的瓶颈在于，它们大多评估的是模型对图像内容的**语义理解**或**事实检索**能力——模型只需“读懂”图像中有什么，即可完成问答。MIRA 则首次将评估焦点系统性地转移到**以视觉图像作为推理媒介**的必要性上：当问题涉及复杂的空间关系、几何操作、物理动态或因果变换时，纯文本思维链（Text-CoT）因无法精确编码和操作空间信息而失效，此时**生成或借助中间视觉状态成为推理成功的关键第一步**。

这一判断有坚实的因果证据支撑：在 MIRA 的直接输入（Direct）设定下，没有任何多模态大模型（MLLM）的准确率超过 20%，即使是最强的 GPT-5 也仅达到 16.5%（Table 1）。这并非模型缺乏视觉理解能力——这些模型在传统基准上表现优异——而是因为**问题本身要求一种模型尚未被训练或评估过的“视觉想象”能力**。

### 2. 三级诊断评估协议：解耦视觉信息与文本推理的贡献

MIRA 的第二项关键创新是其**三级诊断评估协议**（Three-Level Diagnostic Evaluation Protocol），该协议通过受控实验设计，系统解耦了视觉信息与文本推理对模型性能的贡献：

- **Level 1: 直接评估（Direct）**：仅提供问题图像 $I_q$ 和文本问题 $T_q$，测量模型端到端的原生推理能力。
- **Level 2: 文本思维链（Text-CoT）**：在 Direct 基础上加入 CoT 提示，引导模型进行显式文本推理，测量纯语言推理的增益上限。
- **Level 3: 模拟视觉思维链（Visual-CoT）**：向模型提供人工标注的中间视觉状态图像序列，模拟理想的“视觉辅助推理”条件，测量视觉信息注入后的性能天花板。

这一协议的设计精妙之处在于，它**不依赖于模型自主生成视觉中间态的假设**——后者是当前技术尚无法可靠实现的能力——而是通过人工标注的“神谕式”视觉线索，直接回答了核心科学问题：**如果模型能获得正确的中间视觉表征，其推理能力能提升多少？**

答案令人震惊且具有方向性。当提供 Visual-CoT 线索时，所有模型和任务的平均性能相对提升 33.7%（GPT-5-mini 从 13.7% 提升至 23.2%）。更关键的是，**Text-CoT 对某些强模型反而产生了负效应**：Gemini 2.5 Pro 和 o3 在 Text-CoT 设定下的准确率分别相对下降 18.3% 和 14.0%。这一反直觉结果强有力地证明，MIRA 所定义的问题类别的瓶颈**不在文本推理能力，而在视觉信息的表征与操作**——纯文本推理的介入不仅无益，反而可能引入误导性的空间推理路径。

### 3. 数据构造哲学：以“视觉必要性”为驱动的领域覆盖

MIRA 的第三项创新体现在其**数据构造哲学**上。与大多数基准通过众包或从现有数据源收集样本不同，MIRA 的 546 个样本是**自上而下设计**的，其核心原则是：每个问题都必须天然要求中间视觉信息才能有效求解。数据集覆盖了四个互补的挑战性领域：

- **欧几里得几何（Euclidean Geometry）**：如凸包计算、镜像图案、重叠区域判定等，要求精确的空间坐标推理。
- **物理推理（Physics-Based Reasoning）**：如镜面时钟、台球轨迹、电荷受力分析等，涉及物理定律与空间动态的耦合。
- **抽象空间与逻辑谜题（Abstract Spatial & Logical Puzzles）**：如展开立方体、拆弹谜题、多块拼图等，需要多步空间操作与逻辑演绎。
- **因果变换（Causal Transformations）**：如纸飞机折叠、骰子滚动、齿轮旋转等，要求模拟状态转换的因果链。

问题来源包括研究人员手动创建（灵感来自 Reddit 视觉谜题社区及各类思维训练网站）和 Python 脚本程序化生成，随后经 GPT-4o、Gemini 2.5 Flash 等工具进行视觉质量精炼，并通过跨审查和冲突解决确保每个问题具有唯一标准答案和可靠的视觉推理轨迹（Figure 3）。这种**“设计—生成—精炼—审查”**的闭环构造流水线，保证了基准的难度可控性、答案唯一性和评估公平性，是 MIRA 区别于现有视觉推理基准的根本性方法论创新。

### 创新总结

MIRA 的三项创新构成了一条完整的逻辑链：**定义新问题 → 设计诊断性评估协议 → 构造针对性数据**。其本质贡献在于，它首次将“视觉思维链”从一种直觉性的能力描述，转化为一个可量化、可诊断、可改进的评估框架。这一框架揭示的核心发现——现有 MLLM 在需要“以图思考”的任务上存在根本性缺陷，而视觉线索的注入能带来显著且非平凡的增益——为下一代多模态推理模型的研究指明了方向：**可视化不应只是推理的输出，而应成为推理过程本身的第一步**。

## 整体框架

MIRA 基准的整体设计围绕一个核心命题展开：**对于需要空间推理、几何操作或物理模拟的复杂问题，中间视觉表征是有效推理的关键第一步**。现有 MLLM 的纯文本思维链（Text-CoT）无法准确捕捉和操作复杂的空间关系、几何结构与物理动态，而 MIRA 通过提供人工标注的中间视觉状态（Visual-CoT）作为推理过程的辅助线索，系统性地诊断了这一瓶颈。

### 数据设计与构建流水线

MIRA 的数据构建遵循一条严格的四阶段流水线（见 Figure 3），确保每道题目既需要视觉思维链才能求解，又具备唯一的标准答案和可靠的视觉推理轨迹。

![[assets/figures/papers/paper_list_l2756_https_arxiv_org_abs_2511_02779/figures/003_Figure_3.jpg]]
*Figure 3: A high-level overview of the MIRA data design and construction pipeline*

**阶段一：问题设计。** 所有问题由研究生级别的研究人员手动创建，灵感来源包括 Reddit 的视觉谜题社区（r/puzzles, r/VisualPuzzles 等）、各类习题库和脑筋急转弯网站。此外，部分问题通过 Python 脚本程序化自动生成，以保证题目的新颖性和难度可控性。

**阶段二：视觉精炼。** 初始图像输入通过 GPT-4o、Gemini 2.5 Flash 等图像编辑工具进行视觉质量和清晰度的提升，确保中间视觉线索的表达精度。

**阶段三：人工审查。** 最后阶段实施严格的跨审查与冲突解决机制，确保每个问题具有单一、明确的标准答案，并为输入提供可靠的视觉推理轨迹。

**阶段四：领域覆盖。** 最终数据集包含 **546 个精心策划的样本**，横跨四个挑战性领域：
- **欧几里得几何（Euclidean Geometry, EG）**：如凸包计算、镜像图案、重叠区域定位等
- **物理推理（Physics-Based Reasoning, PBR）**：如镜像时钟、台球轨迹、电荷力合成等
- **抽象空间与逻辑谜题（Abstract Spatial & Logical Puzzles, ASLP）**：如立方体展开、拆弹逻辑、多块拼图等
- **因果变换（Causal Transformations, CT）**：如骰子滚动、齿轮旋转、纸飞机折叠等

MIRA 将 Visual-CoT 推理任务分为两大类型：**静态（单步）** 和 **动态（多步）** 视觉思维链，数据集包含 20 种任务类型、546 张输入图像及 936 张人工构建的单步/多步中间图像（见 Figure 2）。

![[assets/figures/papers/paper_list_l2756_https_arxiv_org_abs_2511_02779/figures/002_Figure_2.jpg]]
*Figure 2: MIRA categorizes Visual-CoT reasoning tasks into two primary types: Static (Single-Step) and Dynamic (Multi-Step), with representative examples from each category illustrated in the figure. The dataset includes 20 types of tasks, 546 input images with manually designed questions, and 936 manually constructed single-step and multi-step intermediate images. For more cases, please refer to Appendix D*

### 三级诊断评估协议

为解耦视觉信息与文本推理的贡献，MIRA 实施了一套三级评估协议：

- **Level 1 — 直接评估（Direct Evaluation）**：仅向模型提供问题图像 $I_q$ 和文本描述 $T_q$，要求直接给出答案。此设定测量模型的零样本视觉推理基线能力。
- **Level 2 — 文本思维链推理（Text-CoT Reasoning）**：在 Level 1 基础上附加思维链提示，鼓励模型用纯文本逐步推理。此设定检验纯语言推理能否弥补视觉理解的不足。
- **Level 3 — 模拟视觉思维链推理（Simulated Visual-CoT Reasoning）**：在 Level 2 基础上，额外提供人工标注的中间视觉图像作为推理辅助线索。此设定测量模型利用外部视觉线索提升推理的能力，模拟“以图思考”的理想化条件。

这一协议的设计逻辑在于：通过对比三个 Level 的性能差异，可以定量分离出**视觉信息缺失**对推理能力的制约程度。实验结果表明，在直接输入设定下，没有任何 MLLM 的准确率超过 20%，即使是最强的 GPT-5 也仅达到 16.5%；而当提供中间视觉线索时，所有模型和任务的平均性能相对提升 33.7%，物理推理任务更是几乎翻倍（从 20.7% 跃升至 40.0%）。这些数据有力地验证了视觉思维链在复杂推理中的因果作用。

### 评估设置与公平性保障

所有 API 模型均使用默认解码设置，最大输出长度统一为 16,384 tokens。评估采用微平均准确率（micro-averaged accuracy）作为核心指标，并通过分层答案提取流水线保证评判的鲁棒性：优先从 `<answer></answer>` 标签中解析确定性答案，若失败则回退到启发式正则表达式匹配，最终由 LLM 评判器兜底。这一设计最大限度地减少了人工评估偏差，确保了不同模型间的公平比较。

### 补充图表

![[assets/figures/papers/paper_list_l2756_https_arxiv_org_abs_2511_02779/figures/001_Figure_1.jpg]]
*Figure 1: Left: an example from MIRA with responses from both MLLMs and humans, illustrating the visual reasoning and cognitive gaps revealed by our benchmark; Right: while leading MLLMs demonstrate strong performance on established benchmarks, they struggle significantly on the MIRA, with none surpassing a 20% accuracy rate with direct inputs. This highlights MIRA’s role in exposing the fundamental challenges these models face in complex reasoning tasks that require generating intermediate visual images*

## 核心模块与公式推导

### 关键模块

MIRA基准的核心设计围绕“视觉思维链（Visual-CoT）”展开，其构建与评估体系由以下关键模块组成：

1. **多领域任务设计**：覆盖欧几里得几何（EG）、物理推理（PBR）、抽象空间与逻辑谜题（ASLP）、因果转换（CT）四个领域，共546个样本。每个问题的设计都强调“必须依赖中间视觉信息才能求解”，这是MIRA区别于纯文本推理基准的根本特征。

2. **三级诊断评估协议**：通过三种输入条件解耦视觉信息与文本推理的贡献——
   - **Level 1 直接评估**：仅提供原始问题图像 $I_q$ 与文本 $T_q$；
   - **Level 2 Text-CoT推理**：在Level 1基础上附加文本思维链提示；
   - **Level 3 模拟Visual-CoT推理**：额外提供人工标注的中间视觉状态图像。

3. **数据构建流水线**：问题由研究生级研究人员手动创建或通过Python脚本程序化生成，经GPT-4o、Gemini 2.5 Flash等工具进行视觉精炼，最终通过交叉审查与冲突解决确保每个问题具有唯一标准答案和可靠的视觉推理轨迹。

4. **答案提取与评估**：采用微平均准确率（micro-averaged accuracy）作为核心指标，配合分层提取流水线——优先从 `<answer></answer>` 标签中解析确定性答案，失败时回退至启发式正则表达式匹配，最终由LLM评判兜底，以保证评估的稳健性和公平性。

### 关键公式

MIRA中的物理推理与几何任务涉及若干核心公式，这些公式是构建标准答案和验证推理正确性的基础：

**库仑力计算**（用于Electric Charge任务）：
$$| F _ { i } | = k \frac { | q _ { i } q _ { t } | } { r _ { i } ^ { 2 } }$$
其中 $F_i$ 为点电荷 $q_i$ 对测试电荷 $q_t$ 的静电力大小，$r_i$ 为两电荷间距离，$k$ 为库仑常数。

**净力合成**：
$$\sqrt { F _ { x } ^ { 2 } + F _ { y } ^ { 2 } }$$
将各分力在 $x$、$y$ 方向上的分量 $F_x$、$F_y$ 合成净力大小。

**时钟镜像变换**（用于Mirror Clock任务）：
$$\theta ^ { \prime } = 3 6 0 ^ { \circ } - \theta$$
$$\ m ^ { \prime } \equiv ( 6 0 - m ) \pmod { 6 0 }$$
$$\ h ^ { \prime } \equiv ( 1 2 - h - \mathrm { c a r r y } ) \pmod { 1 2 }$$
其中 $\theta$ 为原始指针角度，$\theta'$ 为左右镜像后的角度；$m$、$h$ 分别为原始分钟和小时数，$m'$、$h'$ 为镜像后的值，$\mathrm{carry}$ 为分钟镜像产生的进位。

**完整长方块高度**（用于Cubes Count等任务）：
$$H_{\mathrm{full}}$$
通过前视图与侧视图推断立体结构中每个位置的最大可能高度，是计数类几何任务的核心推理依据。

## 实验与分析

### 核心瓶颈与评估协议

MIRA 基准的核心发现是：当前多模态大模型（MLLMs）在需要“以图思考”的任务上存在根本性缺陷。其真正的瓶颈不在于语言理解，而在于模型无法在纯文本推理中准确捕捉和操作复杂的空间关系、几何结构与物理动态。为系统诊断这一问题，MIRA 设计了一套三级评估协议：

- **Level 1: Direct Evaluation (D)** — 仅提供问题图像 $I_q$ 和文本 $T_q$，直接要求答案。
- **Level 2: Text-CoT Reasoning (T)** — 在 Level 1 基础上加入文本思维链提示，引导模型进行逐步文字推理。
- **Level 3: Simulated Visual-CoT Reasoning (V)** — 提供人工标注的中间视觉状态作为推理辅助线索，模拟“边看边想”的过程。

这一分层设计使研究者能够解耦视觉信息与文本推理在模型表现中的各自贡献。

### 主实验结果：直接输入下的系统性失败

**Table 1** 汇总了闭源 SOTA 模型、开源权重 MLLM 和统一多模态模型在 MIRA 上的整体表现。最核心的结论是：在直接输入设定下，**没有任何模型的准确率突破 20%**。即使是最强的 GPT-5，其平均准确率也仅为 16.5%。这一结果与这些模型在 MMMU、MMMU Pro、MMStar 等已有基准上的高光表现形成鲜明反差（见 Figure 1 右侧对比），揭示了现有评估体系对视觉推理能力测量的盲区。

当引入人工标注的中间视觉线索（Visual-CoT）后，所有模型和任务的平均性能出现 **33.7% 的相对提升**。以 GPT-5-mini 为例，其准确率从直接输入的 13.7% 跃升至 23.2%（+9.5 个百分点）。这一因果操纵实验有力地证明：**中间视觉表征是有效空间推理的关键第一步**——仅靠文本思维链无法弥补这一信息缺口。

### Text-CoT 的悖论：强模型的反向退化

一个反直觉的发现是，文本思维链（Text-CoT）对某些最强模型反而产生了负面影响。**Gemini 2.5 Pro** 和 **o3** 在 Text-CoT 设定下准确率分别相对下降 18.3% 和 14.0%。这表明，当问题本质上是视觉性的，纯文本的“逐步推理”可能引入噪声或误导性的语言化描述，反而干扰了模型基于图像的直接感知判断。这与传统 NLP 任务中 CoT 普遍有效的经验形成对比，凸显了 MIRA 任务的特殊性。

### 领域差异：物理任务受益最大

Visual-CoT 的提升效果在不同领域间存在显著差异。**物理推理任务**（Physics-Based Reasoning）从纯文本到 Visual-CoT 的条件下，闭源模型的平均准确率几乎翻倍——从 20.7% 跃升至 40.0%。这符合直觉：物理问题（如电荷受力分析、台球轨迹预测）涉及动态模拟和矢量运算，中间可视化能够直接外化这些难以用语言精确编码的空间-物理状态。

相比之下，**抽象空间逻辑谜题**（Abstract Spatial & Logical Puzzles）的提升幅度较小——闭源模型仅从 9.5% 提升至约 10.5%（+1.0 个百分点）。这类任务（如拆弹谜题、多片拼图）可能依赖更高阶的逻辑推理，即使提供了中间视觉状态，模型仍缺乏足够的推理深度来有效利用这些线索。

### 消融实验：提示策略与搜索空间

**Table 2** 展示了提示模板的消融结果。将通用 CoT 提示替换为专门设计的任务特定提示后，闭源模型的平均性能提升了 1.4%。虽然增益有限，但表明针对视觉推理任务优化提示策略仍有挖掘空间。

**Figure 4** 以堆叠柱状图展示了 Pass@k 的缩放行为。将搜索空间从 k=1 扩展到 k=4，所有模型的平均性能提升 15.3%；但从 k=4 到 k=8，增益趋缓至仅 3.0%。这一收敛趋势说明 MIRA 的任务本质上是困难的——单纯增加采样次数无法持续带来收益，模型在多数问题上缺乏正确的推理路径，而非仅仅存在采样方差。

### 失败模式分析

**Figure 5** 展示了一个典型的 Text-CoT 失败案例：在欧几里得几何任务中，即使是最强的 GPT-5，也无法通过纯文本推理正确定位重叠区域并计数红点。其文本描述虽然看似合理，但缺乏对空间结构的精确操作能力。相比之下，Visual-CoT 提供的中间可视化图像使模型能够准确定位重叠区域，从而得出正确答案。

这一失败模式揭示了当前 MLLM 的根本局限：模型在视觉编码-文本解码的架构下，缺乏一个内部“视觉工作记忆”来维护和操作中间空间状态。文本思维链试图用语言模拟这种操作，但语言对空间关系的表征是低效且容易失真的。

### 实验公平性说明

所有 API 模型均使用默认解码设置，最大输出长度统一为 16,384 tokens，保证了不同模型间的可比性。答案提取采用统一的规则流水线加 LLM 评判的层级方案——优先解析 `<answer></answer>` 标签，失败后回退到启发式正则表达式匹配，以减少人工评估偏差。评估在所有模型上使用相同的提示模板（除专有模型的特定适配外），确保了公平比较。

### 局限与待验证问题

需要指出的是，MIRA 目前仅评估模型**使用**人工标注视觉线索的能力，而非**自主生成**中间视觉图像的真实 Visual-CoT 能力。因此，实验所测得的 33.7% 相对提升应被理解为“辅助视觉信息的上限收益”，而非模型“边画边想”的实际表现。此外，基准数据属于特定领域，其泛化性尚未经过系统测试，部分结论可能需要更大规模、更多样化的数据集来进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l2756_https_arxiv_org_abs_2511_02779/figures/004_Table_1.jpg]]
*Table 1: Main results of various models on MIRA. The models are grouped into three categories: Closed-Source SOTA MLLMs, Open-Weight MLLMs, and Open-Weight Unified MLLMs. We report model results under three different inputs: D for direct input, T for Text-Cot, and V for Visual-CoT. Detailed results on each sub-category can be found on Tables 4-10. We highlight the top-three performing models in each column with varying shades of blue, where a darker shade indicates a higher rank*

![[assets/figures/papers/paper_list_l2756_https_arxiv_org_abs_2511_02779/figures/005_Figure_4.jpg]]
*Figure 4: A comprehensive performance comparison of leading models across three evaluation settings: Direct Evaluation (D), Text-CoT Reasoning (T), and Simulated Visual-CoT Reasoning (V). This stacked bar chart shows performance scaling: the base indicates pass@1 accuracy, with segments above capturing gains from pass@2, pass@4, and pass@8. The red horizontal marks show majority voting scores over 8 responses*

![[assets/figures/papers/paper_list_l2756_https_arxiv_org_abs_2511_02779/figures/006_Table_2.jpg]]
*Table 2: Comparison of Text-CoT reasoning performance: General Template*

![[assets/figures/papers/paper_list_l2756_https_arxiv_org_abs_2511_02779/figures/007_Figure_5.jpg]]
*Figure 5: A representative failure case of Text-CoT on a Euclidean Geometry (EG) reasoning task. Even the strongest model (GPT-5) struggles to correctly reason through the problem using plain text, due to its inability to manipulate intermediate visual states. In contrast, the Visual-CoT approach, which leverages intermediate visualizations, enables more accurate localization of the overlapping region and correct counting of red points*

![[assets/figures/papers/paper_list_l2756_https_arxiv_org_abs_2511_02779/figures/008_Table_3.jpg]]
*Table 3: A comprehensive list of the models evaluated in our experiments. For all API-based models, the default decoding settings were used, as no specific sampling parameters (e.g., temperature) were set*

![[assets/figures/papers/paper_list_l2756_https_arxiv_org_abs_2511_02779/figures/009_Table_4.jpg]]
*Table 4: Detailed Results for Euclidean Geometry (Convex Hull, Mirror Pattern) and Physics-Based Reasoning (Mirror Clock) Tasks*

![[assets/figures/papers/paper_list_l2756_https_arxiv_org_abs_2511_02779/figures/010_Table_5.jpg]]
*Table 5: Detailed Results for Euclidean Geometry (Overlap), Abstract Puzzles (Unfolded Cube), and Physics-Based Reasoning (Billiards) Tasks*

![[assets/figures/papers/paper_list_l2756_https_arxiv_org_abs_2511_02779/figures/011_Table_6.jpg]]
*Table 6: Detailed Results for Euclidean Geometry (Localizer), Causal Transformations (Paper Airplane), and Abstract Puzzles (Defuse A Bomb) Tasks*

![[assets/figures/papers/paper_list_l2756_https_arxiv_org_abs_2511_02779/figures/012_Table_7.jpg]]
*Table 7: Detailed Results for Abstract Puzzles (Multi-piece Puzzle), Physics-Based Reasoning (Electric Charge), and Causal Transformations (Rolling Dice: Top) Tasks*

## 方法谱系与知识库定位

MIRA 并非提出新的推理算法或模型架构，而是一个**诊断性基准**。它的核心贡献在于系统性地揭示了一个被现有评测掩盖的瓶颈：当前多模态大模型（MLLMs）在需要“以图思考”的空间推理、几何操作和物理模拟任务上存在根本性困难。因此，MIRA 在知识库中的定位更接近能力探针（capability probe），而非方法改进。

### 与现有基准的关系

MIRA 填补了现有 VQA 和推理基准之间的空白。如图 1 右侧所示，GPT-5、Gemini 2.5 Pro、o3 等前沿模型在 MMMU、MMMU Pro、MMStar、RealWorldQA 等成熟基准上表现强劲，但在 MIRA 的直接输入设定下无一超过 20% 准确率。这种“高分低能”的对比表明，现有基准的任务设计未能充分暴露模型在**中间视觉表征生成**上的缺陷。MIRA 通过引入四个专门领域——欧几里得几何（EG）、物理推理（PBR）、抽象空间与逻辑谜题（ASLP）、因果变换（CT）——将评测重心从“看图回答”转移到“画图推理”。

与传统的文本思维链（Text-CoT）评测不同，MIRA 的三级诊断协议（直接输入 D、文本思维链 T、模拟视觉思维链 V）实现了对视觉信息与文本推理贡献的解耦。这一设计使得 MIRA 能够直接量化“视觉线索”的边际收益，而不仅仅是报告端到端准确率。

### 方法边界与适用条件

MIRA 的评估框架存在明确的边界：

1. **模拟而非真实的 Visual-CoT**：MIRA 当前提供的是人工标注的中间视觉图像，而非由模型自主生成的视觉推理轨迹。这意味着它评估的是模型“利用给定视觉线索”的能力，而非“边思考边绘图”的能力。这是 MIRA 与真正 Visual-CoT 之间的核心差距。

2. **领域覆盖的局限性**：MIRA 的 546 个样本覆盖 20 种任务类型，集中在几何、物理、谜题和因果变换四类。这些领域经过精心挑选以突出视觉推理的必要性，但未必能代表所有需要视觉思维链的真实场景（如医学影像诊断、机械维修路径规划等）。

3. **固定测试集风险**：作为静态基准，MIRA 尚未测试其泛化性和抗过拟合能力。随着社区对该基准的持续关注，模型可能通过训练数据污染获得虚假的性能提升。

### 关键发现与因果机制

MIRA 的核心洞察可以通过以下因果链概括：

- **瓶颈**：纯文本推理无法准确捕捉和操作复杂的空间关系、几何结构与物理动态。
- **干预**：提供人工标注的中间视觉状态（Visual-CoT）作为推理的辅助线索。
- **效果**：所有模型和任务的平均性能相对提升 33.7%，其中物理推理任务从 20.7% 跃升至 40.0%，几乎翻倍。

值得注意的是，Text-CoT 对某些强模型反而产生了**负向干预**：Gemini 2.5 Pro 和 o3 在 Text-CoT 设定下准确率分别相对下降 18.3% 和 14.0%。这表明，对于需要空间推理的任务，纯文本的链式思考不仅无益，反而可能引入错误的推理路径或干扰模型的视觉理解。这一发现挑战了“更多推理总是更好”的普遍假设。

### 局限性与开放问题

MIRA 的局限性直接指向未来的研究方向：

1. **自主视觉思维链的缺失**：如何设计能够自主生成精确且有效中间视觉表征的统一多模态模型，实现真正的“边思考边绘图”？这需要模型同时具备空间理解、几何操作和图像生成能力，目前尚无成熟方案。

2. **自动化数据构建**：MIRA 依赖大量人工标注的视觉推理轨迹。如何在不依赖人工标注的情况下，自动构建类似的大规模数据集？程序化生成（如论文中使用的 Python 脚本）在特定任务上可行，但难以覆盖需要复杂语义理解的场景。

3. **提示策略的优化空间**：论文的消融实验表明，将通用 CoT 提示替换为任务专用提示仅带来平均 1.4% 的提升，而扩大搜索空间（Pass@k 从 1 到 4）可提升 15.3%，但从 k=4 到 k=8 提升趋缓至 3.0%。这说明 MIRA 任务的困难是本质性的，而非提示工程可轻易解决。如何设计更有效的提示策略仍是开放问题。

4. **视觉线索的传递格式**：当前 Visual-CoT 的提升受限于模型对附加视觉信息的理解能力。是否存在更有效的传递视觉线索的格式（如结构化草图、矢量化中间状态、动态标注叠加等），值得进一步探索。

5. **开放权重模型的困境**：部分开放权重模型由于参数规模小且缺乏交错视觉-文本数据训练，在 MIRA 上提升有限。这是否意味着视觉推理能力存在参数规模的临界点，或者需要特定的训练数据配方？

## 原文 PDF

![[paperPDFs/CVPR_2026/When_Visualizing_is_the_First_Step_to_Reasoning_MIRA_a_Benchmark_for_Visual_Chain_of_Thought.pdf]]
