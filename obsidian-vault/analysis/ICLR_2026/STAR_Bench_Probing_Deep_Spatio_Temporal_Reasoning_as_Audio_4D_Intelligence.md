---
title: "STAR-Bench: Probing Deep Spatio-Temporal Reasoning as Audio 4D Intelligence"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/STAR_Bench_Probing_Deep_Spatio_Temporal_Reasoning_as_Audio_4D_Intelligence.pdf
project_link: https://internlm.github.io/StarBench
code_link: https://github.com/InternLM/StarBench
openreview_forum_id: Ts6j3GoZDE
aliases:
- SB
- STAR-Bench
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "多声道音频的统一单声道预处理是导致模型空间推理失败的直接因果旋钮；此外，开源模型缺乏密集音频描述训练，限制了其感知敏感度和知识提取能力。"
primary_logic: "通过程序合成与真人标注的融合，首次系统定义了音频4D智能并构建了层次化基准，揭示了语言难以描述的声学线索对现有模型构成的根本性挑战。"
claims:
- "仅使用音频字幕时，STAR-Bench上的时间推理和空间推理性能分别下降31.5%和35.2%，而现有基准仅下降5.9%和9.0%，表明STAR-Bench专注于语言难描述的线索。"
- "人类在基准上的总体准确率为79.11%，而最佳模型Gemini 2.5 Pro仅为49.59%，随机猜测为24.32%，表明当前模型存在巨大性能差距。"
- "多声道预处理的消融实验证实，现有模型由于在预处理阶段将立体声平均化为单声道，导致空间信息丢失，使得空间推理任务失败。"
- "开源模型在时间推理消融任务中表现停滞，即使简化任务难度也难以提升，显示出其在推理和知识方面的根本性不足。"
---

# STAR-Bench: Probing Deep Spatio-Temporal Reasoning as Audio 4D Intelligence

> [!tip] 核心洞察
> 通过程序合成与真人标注的融合，首次系统定义了音频4D智能并构建了层次化基准，揭示了语言难以描述的声学线索对现有模型构成的根本性挑战。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | STAR-Bench：探索深度时空推理作为音频4D智能 |
| 英文题名 | STAR-Bench: Probing Deep Spatio-Temporal Reasoning as Audio 4D Intelligence |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Ts6j3GoZDE) · [GitHub](https://github.com/InternLM/StarBench) · [Project](https://internlm.github.io/StarBench) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | STAR-BENCH |
| Dataset | STAR-BENCH (Overall), Foundational Perception, Temporal Reasoning |

> [!tip] 效果简介
> - STAR-BENCH (Overall) 上，MA (%) 为 79.11 (Human)，对比 24.32 (Random Guess)，变化 +54.79。
> - STAR-BENCH (Overall) 上，MA (%) 为 49.59 (Gemini 2.5 Pro)，对比 24.32 (Random Guess)，变化 +25.27。
> - Foundational Perception 上，MA (%) 为 75.60 (Human) / 46.64 (Gemini 2.5 Pro)，对比 25.33 (Random Guess)，变化 +50.27 (Human) / +21.31 (Gemini 2.5 Pro)。

## 概要

### 问题背景与核心瓶颈

现有音频理解基准（如 **AIR-Bench**、**MMAU**、**MMAU-Pro**、**MMAR**）主要评估可通过文本描述恢复的语义内容，忽视了难以语言化的精细声学时空线索。这一结构性缺陷导致两个严重后果：其一，仅使用音频字幕时，现有基准上的性能下降有限（MMAU下降5.9%，MMAR下降9.0%），而 **STAR-Bench** 上的时间推理和空间推理分别骤降31.5%和35.2%（Figure 1），证明本基准精确瞄准了语言难描述的声学线索；其二，当前音频语言模型普遍采用多声道平均化为单声道的预处理策略，导致关键双耳空间信息在输入阶段即被丢弃（Figure 3），成为空间推理失败的直接因果旋钮。

### 核心方法定位

**STAR-Bench** 首次系统定义**音频4D智能**，构建了“基础声学感知—整体时空推理”的层次化评估体系。基础感知层使用程序合成与物理仿真音频，在绝对感知和相对辨别两种机制下量化评估音高、响度、时长、方位角、仰角、距离六项核心属性；整体推理层则通过四阶段人机协同标注流水线（Figure 5）构建真实场景任务，覆盖连续过程与离散事件的时间推理，以及单源定位、多源关系、动态轨迹跟踪的空间推理。与现有基准的功能对比（Table 1）显示，STAR-Bench 在时间深度推理、空间深度推理、量化属性评估、多音频支持等七个维度上均为唯一完全支持的基准。

### 主要发现

**人机性能鸿沟**：人类总体准确率达79.11%，而最佳闭源模型 **Gemini 2.5 Pro** 仅为49.59%，随机猜测基线为24.32%（Table 2）。空间推理任务上差距尤为突出——人类73.72% vs. Gemini 2.5 Pro 43.62%。

**闭源模型的瓶颈转移**：Gemini 2.5 Pro 在知识与推理层面表现较强（完整音频+思维链提示下时间推理准确率达99%），其主要瓶颈已转移至精细感知——随着感知粒度从粗到细增加，准确率急剧下降（Figure 8）。

**开源模型的根本性缺陷**：开源模型在时间推理消融实验中，即使任务难度逐级简化，准确率始终接近随机猜测，未见趋势性改善（Figure 9），表明其缺乏密集音频描述能力和跨片段推理机制，存在感知、知识、推理三个维度的系统性不足。

**空间推理的双耳信息困境**：通道分离输入相比原生输入对多数模型带来的提升极为有限（Table 6），证实当前音频模型缺乏有效利用双耳空间线索的机制，这是空间推理任务整体低迷的结构性原因。



音频理解是构建具身智能与多模态感知系统的关键环节。人类能够从日常声学信号中提取丰富的时空信息——例如判断声源的运动方向、感知距离变化、追踪多个同时发生的声学事件——这种能力可被称为“音频4D智能”。然而，当前主流的音频理解基准与模型是否真正具备此类深度时空推理能力，仍是一个未被充分检验的问题。

现有音频基准（如 **AIR-Bench**、**MMAU**、**MMAU-Pro**、**MMAR** 等）主要评估模型对语义内容的识别能力，即模型能否通过文本描述恢复音频中的“发生了什么”。这类任务高度依赖语言可描述的信息，忽视了难以语言化的精细声学时空线索。如图1所示，当仅向模型提供音频的文字描述（caption）而非原始音频时，现有基准上的性能下降极为有限——Gemini 2.5 Pro在MMAU和MMAR上分别仅下降5.9%和9.0%——这表明这些基准所测试的能力本质上可以通过纯文本近似恢复，并未真正触及声学信号的核心时空维度。

更深层的瓶颈在于模型预处理环节。现有音频语言模型普遍采用将多声道音频平均化为单声道的预处理策略（Figure 3），这一操作直接丢弃了双耳线索所承载的空间定位信息，使得空间推理任务在输入层面就已丧失了关键依据。消融实验证实，这一预处理选择是导致模型空间推理失败的直接因果旋钮。

与此同时，开源模型还面临着训练数据层面的结构性缺陷：缺乏密集音频描述训练，限制了其对精细声学属性的感知敏感度，以及在跨片段推理中整合上下文知识的能力。这导致开源模型即便在简化后的任务设定下，其表现仍停滞在随机猜测水平附近（Figure 9），暴露出推理与知识层面的根本性不足。

上述缺口共同指向一个核心问题：**现有基准与模型尚未系统性地评估和构建“音频4D智能”所需的三项核心能力——精细感知、知识推理与跨片段时空整合**。STAR-Bench的提出正是为了填补这一空白，通过程序合成与真人标注的融合，首次构建了一个层次化、可量化、且专注于语言难以描述线索的深度时空推理基准。



## 核心方法与创新机理

STAR-Bench 的核心创新在于首次系统定义了**音频4D智能**的概念，并通过层次化基准设计，将评估重心从传统语义理解转向**语言难以描述的精细声学时空线索**。这一转向直指现有音频基准的根本性瓶颈。

### 1. 从语义理解到声学感知的范式转移

现有音频基准（如 AIR-Bench、MMAU、MMAR、MMAU-Pro）主要评估可通过文本描述恢复的语义内容，忽视了难以语言化的精细声学时空线索。STAR-Bench 通过**程序合成与真人标注的融合**，构建了专门探测这些线索的测试体系。决定性证据来自 Figure 1：当仅使用音频字幕（去除原始声学信号）时，Gemini 2.5 Pro 在 STAR-Bench 的时间推理和空间推理任务上准确率分别下降 **31.5%** 和 **35.2%**，而在 MMAU 和 MMAR 上仅下降 5.9% 和 9.0%。这表明 STAR-Bench 成功捕捉了现有基准所遗漏的、语言难以描述的关键声学信息。

### 2. 双层次评估架构：基础感知与整体推理的解耦

STAR-Bench 将评估分解为两个互补子任务，形成“感知—推理”解耦的诊断框架：

- **基础声学感知**：使用参数化合成或 Pyroomacoustics 物理模拟器生成的音频，在绝对感知范围和相对辨别灵敏度两个维度上，定量评估模型对六种核心声学属性（音高、响度、时长、方位角、高度角、距离）的感知能力。
- **整体时空推理**：使用真实世界音频，评估复杂动态场景下的时间推理（片段重排序、连续事件演化）和空间推理（单源静态定位、多源空间关系、动态轨迹跟踪）。

这一设计使得研究者可以分别诊断模型的感知瓶颈与推理瓶颈，而非混淆两者。

### 3. 揭示多声道预处理的关键因果旋钮

Figure 3 和 Section 3.2.2 的消融实验揭示了一个被长期忽视的因果机制：**现有音频语言模型在预处理阶段将多声道音频平均化为单声道**，导致双耳空间信息完全丢失。实验证实，模型在处理伪立体声信号时因信号抵消而持续失败。这一发现将多声道预处理定位为空间推理失败的直接因果旋钮，为后续模型设计提供了明确的改进方向。

### 4. 鲁棒性评估策略

STAR-Bench 引入**多次扰动提示的鲁棒性评估**，报告平均准确率（AA）和全正确率（ACR）两个指标。实验表明，最佳模型 Gemini 2.5 Pro 的 ACR 比 AA 低约 25 个百分点，多数开源模型 ACR 接近零，揭示了当前模型输出的高度不稳定性。

### 5. 四阶段数据标注流水线

为保证数据质量，STAR-Bench 设计了四阶段标注流水线（Figure 5）：分类体系构建与数据采集 → AI 辅助自动过滤（基础规则 + LLM + MLLM 三级漏斗）→ 人工标注与质量控制（交叉验证 + 专家抽检）→ 最终验证（仅保留至少 2/3 专家独立正确回答的题目）。这一流程确保了基准的生态效度和标签可靠性。



![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_Ts6j3GoZDE/figures/001_Figure_1.jpg]]
*Figure 1: (Left): A comparison between humans and the Gemini 2.5 Pro with and without audio captions on various audio benchmarks. Our STAR-Bench evaluates linguistically hard-to-describe audio cues. See Appendix B.1 for audio caption details. (Right): The three core abilities required to solve tasks in the STAR-Bench benchmark*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_Ts6j3GoZDE/figures/007_Figure_4.jpg]]
*Figure 4: (a) The data distribution of STAR-BENCH across three main tasks. (b) Data statistics Continuous Evolution 30% Motion 23.9%Loudness 16% Distance 5% Absolute 39% Static Spatial Localization 56%of our benchmark, including the total number of questions for each task and their sub-categories, AzimuthDuration5%and the average audio length for reasoning tasks. Static SpatialLocalization 56Static Spatial Localization 56% Static SpatialLocalization 56%Static Spatial Localization 56%Figure 5: The four-stage data annotation pipeline for constructing our STAR-BENCH*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_Ts6j3GoZDE/figures/002_Table_1.jpg]]
*Table 1: A comparative overview of our benchmark against other representative audio benchmarks. (✓: Fully supported, : Partially supported or limited amount, ✗: Not supported)*

### 基准定位与核心挑战

STAR-BENCH 是首个系统定义并评估**音频4D智能**（Audio 4D Intelligence）的层次化基准，旨在探测模型对难以语言化的精细声学时空线索的推理能力。现有音频基准（如 AIR-Bench、MMAU、MMAR 等）主要评估可通过文本描述恢复的语义内容，而 STAR-BENCH 聚焦于语言难以捕捉的深层声学信息。图 1 的消融实验提供了决定性证据：当仅提供音频字幕（去除原始音频）时，Gemini 2.5 Pro 在 STAR-BENCH 的时间推理和空间推理任务上准确率分别下降 **31.5%** 和 **35.2%**，而在 MMAU 和 MMAR 上仅下降 5.9% 和 9.0%，表明本基准成功捕捉了现有基准所忽视的声学线索。

### 任务层次与能力模型

基准由两个互补的子任务构成，对应音频4D智能所需的三种核心能力（图 1 右）：

1. **基础声学感知**（Foundational Acoustic Perception）：使用程序合成音频，在受控条件下对六个核心声学属性（音高、响度、时长、方位角、高度角、距离）进行绝对感知范围与相对辨别灵敏度的细粒度量化评估。
2. **整体时空推理**（Holistic Spatio-Temporal Reasoning）：使用真实世界音频，评估动态场景下的复杂推理能力，包含时间推理（片段重排序、连续演化）和空间推理（单源静态定位、多源空间关系、动态轨迹跟踪）两个维度。

### 数据构建流水线

STAR-BENCH 的数据构建整合了程序合成与真人标注两条路径（图 5），形成四阶段流水线：

- **阶段一：分类体系构建与数据采集**。建立层次化任务分类体系，基础感知任务通过精确参数化或 Pyroomacoustics 物理仿真引擎合成音频；整体推理任务从开源库和网络采集候选数据。
- **阶段二：AI 辅助自动过滤**。采用基础规则、LLM 和 MLLM 三级漏斗式过滤，快速筛选合适样本（图 10–11）。
- **阶段三：人工标注与质量控制**。招募标注员进行专业标注，经交叉验证和专家抽检确保标签质量。
- **阶段四：人类表现终验**。由领域专家作为应试者解决任务，仅保留至少 2/3 专家独立正确回答的题目，确保基准的可解性与标注可靠性。

最终基准包含 **2,353** 道多项选择题，其中基础感知 951 题、时间推理 900 题、空间推理 502 题，平均音频时长约 14 秒（图 4）。

### 评估协议

所有问题均采用多项选择形式，通过字符串匹配判定正确性。为应对模型输出的不稳定性，采用多次扰动提示的鲁棒性评估策略（详见附录 C），报告两个核心指标：

- **平均准确率**（Average Accuracy, AA）：多次运行的平均正确率。
- **全正确率**（All-Correct Rate, ACR）：所有运行中均正确回答的题目比例，作为输出稳定性的更强指标。

### 关键因果旋钮：多声道预处理

现有音频语言模型普遍在预处理阶段将多声道音频平均化为单声道，导致空间信息丢失。图 3 的消融实验证实，这一预处理策略是空间推理失败的直接因果旋钮——模型在伪立体声信号上因信号抵消而持续失败。为此，基准在空间推理中引入两种输入策略：原生输入（native）和通道分离输入（channel-wise），以系统评估模型利用双耳信息的能力。

### 性能全景

表 2 汇总了 19 个模型的评估结果。人类总体准确率达 **79.11%**，最佳闭源模型 Gemini 2.5 Pro 仅为 **49.59%**，随机猜测基线为 24.32%，揭示出巨大的性能差距。开源模型表现尤为薄弱，在时间推理消融实验中即使大幅简化任务，准确率仍接近随机水平（图 9），显示出感知敏感度与知识推理能力的根本性不足。



### 3.1 基准任务体系的双层架构

STAR-BENCH 的核心设计在于将音频4D智能的评估解耦为两个互补的子任务：**基础声学感知（Foundational Acoustic Perception）** 与 **整体时空推理（Holistic Spatio-Temporal Reasoning）**。这一架构的因果逻辑在于：感知是推理的前提，而现有基准恰恰混淆了二者，导致无法定位模型的真实瓶颈。

- **基础声学感知**：使用程序合成与物理仿真音频（基于 Pyroomacoustics 引擎），在受控条件下对模型的六项核心声学属性（音高、响度、时长、方位角、高度角、距离）进行绝对感知范围与相对辨别灵敏度的定量剖析。该模块的因果旋钮在于：通过参数化合成消除了真实场景中的混淆变量，使得感知能力的测量具有可归因性。
- **整体时空推理**：使用真实世界音频，评估模型在动态场景中的复杂推理能力。其中时间推理包含连续演变与片段重排序两个子类，空间推理则涵盖单源静态定位、多源空间关系与动态轨迹跟踪三个子类。

### 3.2 空间推理的双输入策略

针对现有音频语言模型（LALMs）普遍将多声道平均化为单声道的预处理瓶颈，STAR-BENCH 在空间推理任务中引入了两种互补的评估策略（见 Sec 3.2.2）：

- **原生输入（Native Input）**：直接馈送原始多声道音频，考验模型对双耳空间线索的原生利用能力。
- **通道分离输入（Channel-wise Input）**：将左右声道分别输入模型，以探测其是否具备独立处理双耳信息并融合定位的机制。

消融实验（Table 6）揭示了一个决定性的因果事实：通道分离输入对大部分模型带来的提升极为有限，证明当前音频模型**缺乏有效利用双耳信息的机制**，而非仅仅是输入格式的问题。Figure 3 进一步通过伪立体声信号的消融实验证实，现有模型在单声道转换过程中因信号抵消而彻底丧失空间信息，导致空间推理任务系统性失败。

### 3.3 数据标注流水线的四阶段漏斗架构

STAR-BENCH 的数据构建采用程序合成与人工标注融合的四阶段流水线（Figure 5），其核心逻辑是通过逐级过滤确保标签质量与任务难度：

1. **分类体系构建与数据采集（Taxonomy Construction and Data Sourcing）**：从开源音效库与网络资源采集候选数据，覆盖层次化任务分类体系。
2. **AI辅助自动过滤（AI-Assisted Automated Filtering）**：通过基础规则、LLM 与 MLLM 构成的三级漏斗式过滤，快速筛除不合适的样本。
3. **人工标注与质量控制（Human Annotation and Quality Control）**：招募标注员进行专业标注，经交叉验证与专家抽检确保标签质量。
4. **人类表现终验（Final Validation via Human Performance Evaluation）**：由领域专家作为应试者独立解决任务，仅保留至少 2/3 专家正确回答的题目，以此作为难度的最终标尺。

### 3.4 关键公式：基础感知任务的话语计数

基础感知任务中，绝对感知与相对辨别子任务的样本量由以下公式确定（见 Appendix B.2.1）：

**绝对方位话语数量**：
$$8 \times (3 \times 2 \times 2) = 96$$
其中：8 个角度 ×（3 个房间 × 2 个听者位置 × 2 个源片段）。

**绝对高度话语数量**：
$$6 \times (3 \times 2 \times 2) = 72$$
其中：6 个角度 ×（3 个房间 × 2 个听者位置 × 2 个源片段）。

**绝对距离话语数量**：
$$42 + 9 = 51$$
其中：每（房间 × 听者）组中，1–7 米各有 6 个样本，8–10 米各有 3 个样本。

**相对方位话语数量**：
$$6 \times 20 = 120$$
其中：6 个差异等级 × 20 个样本。

这些公式揭示了基础感知任务设计的核心原则：通过控制声学参数的组合空间，系统覆盖感知范围与辨别灵敏度的关键维度，从而实现对模型感知能力的细粒度诊断。



## 实验与关键发现

### 整体性能全景：人类与模型之间的巨大鸿沟

Table 2 汇总了19个模型在STAR-BENCH三大任务上的主要评估结果。人类基线以 **79.11%** 的宏观准确率（MA）确立了性能上界，而随机猜测基线仅为 **24.32%**。当前最先进的闭源模型 **Gemini 2.5 Pro** 仅取得 **49.59%** 的MA，与人类水平相差近30个百分点，揭示出深度时空推理任务对现有模型构成的根本性挑战。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_Ts6j3GoZDE/figures/008_Table_2.jpg]]
*Table 2: Evaluation results of various models on STAR-BENCH. The best performance is highlighted in bold, and the second-best ones are underlined. MA (Macro Accuracy) denotes the unweighted mean of class-wise accuracies, while OA (Overall Accuracy) denotes the proportion of correctly answered instances. All reported values are AA (Average Accuracy across multiple runs) only; for ACR (All-Correct Rate), see Appendix D*

从任务维度拆解：
- **基础感知**：人类准确率为75.60%，Gemini 2.5 Pro为46.64%，差距约29个百分点。
- **时间推理**：人类整体准确率（OA）达88.00%，Gemini 2.5 Pro为58.52%，差距约29个百分点。
- **空间推理（原生输入）**：人类OA为73.72%，Gemini 2.5 Pro仅43.62%，差距扩大至30个百分点，且仅略高于随机猜测的33.33%，表明空间推理是当前模型最薄弱的环节。

开源模型的表现更为严峻。多数开源模型在时间推理和空间推理上的准确率接近或仅略高于随机猜测，且在多次扰动评估下的全正确率（ACR）趋近于零，反映出输出高度不稳定和推理能力的根本性缺失。

### 基础感知：精细粒度感知是闭源模型的核心瓶颈

Figure 8 的基础感知范围和灵敏度分析揭示了一个关键发现：随着感知粒度从粗到细递增，**Gemini 2.5 Pro** 的准确率急剧下降。这一趋势表明，尽管闭源模型在知识推理层面表现出色，其**主要瓶颈已转移至精细声学感知**——即对音高微小差异、响度细微变化、方位精确角度等低层声学属性的分辨能力严重不足。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_Ts6j3GoZDE/figures/012_Figure_8.jpg]]
*Figure 8: The range and sensitivity analysis in foun- Figure 9: The ablation study on temporal dational perception. reasoning*

Table 4 的详细结果进一步印证了这一结论。在绝对感知范围（Absolute Perception Range）任务中，Gemini 2.5 Pro在方位角（Azimuth）和高度（Elevation）上的AA/ACR显著低于音高响度（Pitch & Loudness），说明空间属性的绝对量化感知是突出的薄弱环节。相对辨别灵敏度（Relative Discrimination Sensitivity）任务中，所有模型在精细难度级别上的ACR几乎为零，验证了模型输出在感知边界附近的高度随机性。

### 时间推理：上下文完整性与知识推理的双重依赖

Figure 9 的时间推理消融实验提供了因果性证据。**Gemini 2.5 Pro** 在“完整未剪切音频 + 思维链提示”设置下准确率高达 **99%**，而一旦去除连续听觉上下文，性能大幅下降。这直接证实：时间推理严重依赖完整的时间信息流，任何信息截断都会导致推理链条断裂。

相比之下，**开源模型在多级简化的时间推理设置下表现停滞**，即使任务难度显著降低（如减少推理步数、提供更明确的线索），其准确率始终接近随机猜测水平，未见明显的趋势性改善。这一现象揭示了开源模型在**密集音频描述能力和跨片段知识整合**方面的根本性缺陷——它们缺乏将声学感知转化为可推理知识表征的机制。

时间推理的错误分布（Figure 6）和错误案例（Figure 7）进一步显示，模型的主要失败模式包括：无法追踪连续状态演化（如物体空间运动）、将听觉线索错误解释为视觉经验（“视觉中心幻觉”）、以及在需要因果链推理的场景中产生逻辑断裂。

### 空间推理：多声道信息丢失的因果性证据

空间推理是模型表现最差的任务维度。Figure 3 揭示了这一失败的**直接因果旋钮**：现有音频语言模型在预处理阶段将立体声或多声道音频**平均化为单声道**，导致关键的双耳空间线索（如耳间时间差、耳间声级差）被不可逆地丢失。实验证实，模型在伪立体声信号上一致失败，因为信号在单声道转换过程中发生了相消干涉。

Table 6 对比了原生输入（Native Input）与通道分离输入（Channel-wise Input）两种评估策略。结果显示，**通道分离输入对大部分模型带来的性能提升极为有限**，证明当前音频模型缺乏有效利用双耳信息的原生机制——即使将左右声道分别输入，模型也无法像人类听觉系统那样从中提取空间关系。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_Ts6j3GoZDE/figures/018_Table_6.jpg]]
*Table 6: Results for the spatial reasoning task using native and channel-wise audio input. Each cell reports AA / ACR: Average Accuracy (AA; overall accuracy across all runs) / All-Correct Rate (ACR; proportion of samples that are correct on every run). The best model in each category is shown in bold, and the second best is underlined*

空间推理的三个子类别中，多声源空间关系判断和动态轨迹跟踪是最困难的场景，模型在这些任务上的准确率远低于单源静态定位，表明对复杂空间场景的结构化理解仍是未解决的挑战。

### 输出稳定性危机

所有模型在STAR-BENCH上均表现出严重的输出不稳定性。以Gemini 2.5 Pro为例，其全正确率（ACR）比平均准确率（AA）低约25个百分点，意味着即使是最佳模型，在相同问题的多次评估中也频繁产生不一致的答案。多数开源模型的ACR接近零，说明其输出在轻微提示扰动下即发生翻转。这一发现对音频语言模型在实际部署中的可靠性提出了严峻质疑，也验证了STAR-BENCH采用多次扰动评估策略的必要性。



## 定位与知识库关联

### 任务定位：从语义理解到物理时空推理的跨越

STAR-BENCH 在音频理解基准谱系中占据一个此前空缺的位置——深度时空推理。现有基准的演进脉络清晰地揭示了这一空白：

- **语义感知阶段**：以 **AIR-Bench** 为代表的早期基准主要评估模型对音频中语义内容（事件类别、场景标签）的识别能力，任务可通过文本描述充分恢复。
- **初步推理阶段**：**MMAU** 和 **MMAU-Pro** 引入了少量时间问题和空间问题，但推理深度停留在感知层面——时间任务多为简单的事件顺序判断，空间任务局限于单声源定位。**MMAR** 进一步引入逻辑推理，但空间维度仍未突破单源静态场景。
- **通用处理阶段**：**Dynamic-SUPERB Phase-2** 作为通用音频处理基准，部分支持多音频评估，但覆盖的时空推理深度不足。

STAR-BENCH 的关键区分点在于：它系统性地要求模型将声学感知与物理因果知识结合，在动态、多声源的现实场景中执行多步推理。Figure 1 的消融实验提供了决定性证据：当仅使用音频字幕（剥离声学线索）时，现有基准 MMAU 和 MMAR 上的性能仅下降 5.9% 和 9.0%，而 STAR-BENCH 的时间推理和空间推理分别骤降 31.5% 和 35.2%。这表明 STAR-BENCH 成功聚焦于语言难以描述的精细声学时空线索，而非可文本化的语义内容。

### 核心瓶颈与因果机制

分析揭示了两层递进的瓶颈结构：

**第一层：预处理导致的空间信息丢失。** 现有音频语言模型（LALMs）在预处理阶段普遍将多声道音频平均化为单声道（Figure 3），这一操作直接抹除了双耳线索——人类赖以进行空间定位的核心信息。消融实验（Table 6）证实，即使将音频以通道分离（channel-wise）方式输入，大部分模型的提升仍然有限，说明当前音频编码器缺乏有效利用双耳信息的原生机制。这是空间推理失败的直接因果旋钮。

**第二层：开源模型的知识与推理缺陷。** 时间推理消融实验（Figure 9）揭示了更深层的问题：在多级简化的任务设置下（从完整上下文逐步削减至最简形式），开源模型的准确率始终接近随机猜测，未见趋势性改善。相比之下，闭源模型 Gemini 2.5 Pro 在完整未剪切音频配合思维链提示时准确率达 99%，而去除上下文后大幅下降。这表明闭源模型的主要瓶颈已转向精细感知（Figure 8 的粒度分析佐证了这一点：随着感知粒度从粗到细，Gemini 2.5 Pro 准确率急剧下降），而开源模型在感知、知识和推理三个核心能力上均存在根本性不足。

### 方法边界与适用条件

STAR-BENCH 的设计边界决定了其适用场景和局限：

- **模态边界**：基准仅关注音频模态，尚未与视觉、触觉等传感模态结合。这意味着它评估的是“音频 4D 智能”而非完整的多模态 4D 智能。在真实物理世界中，视觉线索往往与听觉线索互补（如看到声源位置可验证听觉定位），当前基准无法评估这种跨模态协同。
- **任务边界**：空间推理虽覆盖单声源定位、多声源关系和动态轨迹跟踪三个子类，但主要基于静态声学场景的片段推理，尚未涉及长时连续场景中的实时跟踪与预测。
- **评估边界**：所有问题均为多项选择，排除了开放式生成评估可能引入的主观性，但也限制了对模型自由推理能力的考察。此外，人类基线仅由 10 名非专业大学生在约 10% 的随机子集上测试，虽然总体准确率 79.11% 远高于最佳模型（49.59%），但这一基线可能低估了领域专家的表现上限。

### 局限与开放问题

**已知局限：**

1. **输出稳定性极差**：最佳模型 Gemini 2.5 Pro 的全正确率（ACR）比平均准确率（AA）低约 25 个百分点，多数开源模型的 ACR 接近零。这意味着模型在同一问题的多次扰动测试中给出矛盾答案，可靠性不足。
2. **空间推理全面落后**：所有模型在空间推理任务上仍远低于人类水平（人类 73.72% vs. Gemini 2.5 Pro 43.62%），尤其在多声源空间关系和动态轨迹跟踪方面。
3. **开源模型的多音频整合无能**：开源模型缺乏密集音频描述能力，在需要跨片段整合信息的连续推理任务上表现极差，即使简化任务难度也无法激活其推理能力。

**关键开放问题：**

1. **原生多声道编码器设计**：如何构建能够直接利用双耳空间线索的音频编码器，而非依赖后处理的通道分离策略？这需要从模型架构层面重新思考音频输入的表示方式。
2. **细粒度声学描述训练**：如何使开源模型获得生成细粒度声学描述（如“声源从左侧 30 度以每秒 5 米的速度接近”）的能力，从而将感知与知识推理桥接？当前开源模型在这方面的训练数据和方法均严重缺失。
3. **视觉中心幻觉的消除**：现有模型在处理听觉输入时倾向于将其错误解释为视觉经验（如将空间方位判断转化为对“画面”的想象），这种跨模态幻觉的机制和解决方案尚不清楚。
4. **多模态 4D 智能的协同架构**：在包含视觉、触觉等多传感模态的环境中，音频 4D 智能如何与其他模态协同以实现更鲁棒的物理世界推理？这需要超越单一模态基准的评估框架。



## 原文 PDF

![[paperPDFs/ICLR_2026/STAR_Bench_Probing_Deep_Spatio_Temporal_Reasoning_as_Audio_4D_Intelligence.pdf]]
