---
title: "Flat-Pack Bench: Evaluating Spatio-Temporal Understanding in Large Vision-Language Models through Furniture Assembly"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Flat_Pack_Bench_Evaluating_Spatio_Temporal_Understanding_in_Large_Vision_Language_Models_through_Furniture_Assembly.pdf
project_link: "https://flat-pack-bench.github.io"
code_link: "https://github.com/justachetan/flat-pack-bench"
aliases:
- FPB
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 部件追踪（tracking）能力和接触关系推理（contact reasoning）是解决家具组装时空理解任务的关键操作，但目前模型和工具在这两个基本能力上均严重不足。
primary_logic: 通过引入带视觉提示（visual prompts）的家具组装视频问答基准，该工作揭示了即使最先进的 LVLM 也缺乏对长视频中多部件交互的逐步理解能力，模型更倾向于依赖静态图像线索和常识捷径，而非真正利用时间上下文。
claims:
- GPT-5 在基准上仅达到约38%准确率，远低于人类的94.18%。
- 移除视频仅使用图像提示时，模型整体性能大幅下降（8.80%），但下降几乎完全来自追踪（TRACK）子任务（-24.51%），其他子任务甚至有所提升，表明模型未能有效利用视频。
- 错误分析显示，目标定位（37.28%）和时空推理（32.45%）是模型错误的主要来源。
- 打乱部件 ID 会显著降低时间排序（TORD）任务性能，进一步表明模型依赖非时间捷径。
---

# Flat-Pack Bench: Evaluating Spatio-Temporal Understanding in Large Vision-Language Models through Furniture Assembly

> [!tip] 核心洞察
> 通过引入带视觉提示（visual prompts）的家具组装视频问答基准，该工作揭示了即使最先进的 LVLM 也缺乏对长视频中多部件交互的逐步理解能力，模型更倾向于依赖静态图像线索和常识捷径，而非真正利用时间上下文。

| 字段 | 内容 |
|------|------|
| 中文题名 | Flat-Pack Bench：通过家具组装评估大型视觉-语言模型的时空理解能力 |
| 英文题名 | Flat-Pack Bench: Evaluating Spatio-Temporal Understanding in Large Vision-Language Models through Furniture Assembly |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.21625) · [Project](https://flat-pack-bench.github.io) · [Code](https://github.com/justachetan/flat-pack-bench) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | FLAT-PACK BENCH（基于家具组装的视频时空理解基准） |
| Dataset | FLAT-PACK BENCH |

> [!tip] 效果简介
> - FLAT-PACK BENCH 上，Micro Avg. Human Performance vs Frequency Chance (+67.44)；Micro Avg. GPT-5 (best proprietary) vs Frequency Chance (+10.97)；Micro Avg. InternVL3-78B (best open) vs Frequency Chance (+14.29)。

## 概述

**问题本质**：现有大型视觉-语言模型（LVLM）在视频理解基准上表现不断提升，但这些进步是否意味着模型真正掌握了细粒度的时空推理能力？本文指出，当前 LVLM 在需要多帧关联的目标追踪和空间交互理解上存在根本性缺陷，模型更倾向于依赖静态图像线索和常识捷径，而非有效利用视频中的时间信息。

**核心洞察**：通过家具组装这一天然需要逐步时空推理的任务，作者揭示了即使是最先进的 LVLM 也无法真正理解长视频中多部件交互的时序过程。部件追踪（tracking）和接触关系推理（contact reasoning）是解决此类任务的关键操作，而目前模型在这两项基本能力上严重不足。

**方法与定位**：该工作提出了 **FLAT-PACK BENCH**，一个基于家具组装视频的时空理解基准。基准包含 602 道多项选择题，覆盖时间排序（Temporal Ordering）、时间定位（Temporal Localization）、部件配对（Mating）和目标追踪（Tracking）四类细粒度任务，并引入带颜色掩膜、边界线和标签的视觉提示（visual prompts）作为部件参考。该方法属于**视频理解评测基准**范畴，与现有工作不同的是，它通过需要精确多帧关联的组装任务来探测模型的时空推理瓶颈，而非仅评估粗粒度的视频问答能力。

**主要结果**：人类在该基准上达到 94.18% 的准确率，而最强闭源模型 GPT-5 仅取得约 38%，最强开源模型 InternVL3-78B 约为 41%。移除视频仅使用图像提示时，追踪子任务性能骤降 24.51%，而其他子任务反而有所提升，直接证实了模型未能有效利用视频中的时间信息。错误分析进一步表明，目标定位错误（37.28%）和时空推理错误（32.45%）是模型失效的主要来源。

## 背景与动机

大型视觉-语言模型（LVLM）在静态图像理解上取得了显著进展，但在需要细粒度时空推理的视频理解任务中仍面临根本性瓶颈。现有模型无法有效利用视频中的时间信息，尤其在目标追踪和空间交互理解上存在严重缺陷，导致其在需要多帧关联的任务上表现远低于人类。

### 问题背景

现实世界中的许多日常任务——例如家具组装、烹饪操作或设备维修——要求智能体通过观察视频来理解逐步操作过程。这需要模型具备以下细粒度时空理解能力：判断动作发生的先后顺序（时间排序）、定位特定状态出现的时间点（时间定位）、理解部件之间的配合关系（部件配对），以及持续追踪特定部件在视频中的位置变化（部件追踪）。

然而，当前 LVLM 的视频理解评测主要集中在粗粒度的行为识别或视频问答，缺乏对上述细粒度时空推理能力的系统性评估。模型往往倾向于依赖静态图像线索和常识捷径，而非真正利用时间上下文进行推理。

### 现有方法缺口

已有的视频理解基准存在两方面不足。其一，任务设计偏向全局语义理解，未能拆解出追踪、接触关系推理等基本操作原语。其二，评测形式未能有效隔离模型对视频时间信息的依赖程度，难以诊断模型失败的根本原因。

### 本文动机

针对上述缺口，本文提出 **FLAT-PACK BENCH**——一个基于家具组装视频的时空理解基准。该基准以宜家家具组装视频为素材，通过引入带颜色掩膜、边界线和标签的视觉提示（visual prompts），将细粒度问题锚定到具体部件上，从而系统评估 LVLM 在时间排序（Temporal Ordering, TORD）、时间定位（Temporal Localization, TLOC）、部件配对（Mating, MATE）和部件追踪（Tracking, TRACK）四项任务上的表现。

核心洞察在于：部件追踪能力和接触关系推理是解决家具组装时空理解任务的关键操作，而现有模型在这两个基本能力上均严重不足。通过构建该基准，工作旨在揭示 LVLM 在长视频多部件交互理解上的根本性缺陷，并为未来研究提供诊断工具。

## 核心创新

Flat-Pack Bench 的核心创新不在于提出一个新的模型架构，而在于**构建了一个精准诊断大型视觉-语言模型（LVLM）时空理解缺陷的基准**，并通过系统性的实验设计揭示了当前最先进模型在视频理解上的根本性瓶颈。其创新点主要体现在以下三个维度：

### 1. 任务设计：将时空理解分解为可诊断的原语

现有视频理解基准多聚焦于高层语义或粗粒度事件识别，难以定位模型的具体能力短板。Flat-Pack Bench 将家具组装这一复杂长时程任务**显式分解为四个细粒度时空推理原语**：

- **时间排序（Temporal Ordering, TORD）**：判断组装步骤的先后顺序。
- **时间定位（Temporal Localization, TLOC）**：识别特定组装状态在视频中的时间位置。
- **部件配对（Mating, MATE）**：判断两个部件是否最终连接在一起。
- **部件追踪（Tracking, TRACK）**：在视频中持续定位特定部件的位置。

这种分解使得基准不仅能给出总分，更能**精确诊断模型在哪个子能力上存在缺陷**。例如，实验表明模型在 TRACK 任务上的表现远低于其他子任务，直接暴露了当前 LVLM 在细粒度目标追踪上的核心弱点。

### 2. 视觉提示机制：构建部件级参考锚点

与传统的纯视频问答不同，Flat-Pack Bench 引入了**带颜色掩膜、边界线和标签的视觉提示（visual prompts）**作为部件参考。这一设计的关键创新在于：

- **消除指代歧义**：通过精确标注的部件分割图像，确保问题中的部件指代与视觉输入严格对应，避免模型因部件识别错误而导致的“假阴性”评估。
- **解耦视频利用效率**：通过对比“视频 + 视觉提示”与“仅视觉提示”两种输入条件，**直接量化模型对视频时间信息的实际利用程度**。消融实验（Table 4）显示，移除视频后模型整体性能仅下降 8.80%，且下降几乎完全来自 TRACK 子任务（-24.51%），而 TLOC 和 MATE 任务反而有所提升——这有力地证明了模型**并未真正利用视频中的时间信息**，而是依赖静态图像线索和常识捷径作答。

### 3. 评估方法论：从端到端评分到机制诊断

Flat-Pack Bench 的评估体系超越了简单的准确率比较，构建了一套**多层次的诊断框架**：

- **人类表现校准**：通过计算机科学专业学生和众包平台（Prolific）收集人类表现（Micro Avg. 94.18%），建立了可靠的上界参考，明确显示 GPT-5 的 37.71% 准确率存在巨大差距。
- **思维链反直觉发现**：零样本思维链（ZS-CoT）和自洽思维链（SC-CoT）提示在语言推理中通常有效，但在本基准上**均未提升性能，甚至导致下降**（Table 3）。这一反直觉结果揭示了当前 LVLM 的“推理”能力在时空视觉领域存在根本性局限，模型生成的解释往往与正确推理过程脱节。
- **捷径利用检测**：通过打乱部件 ID 顺序（Table 4, Shuffled Parts）发现 TORD 性能显著下降，**直接证明了模型依赖 ID 编号的序列捷径而非真正理解时间顺序**。

综上，Flat-Pack Bench 的核心贡献在于**将 LVLM 时空理解评估从“能不能”推进到“为什么不能”的诊断层面**，通过精心设计的任务分解、视觉提示机制和消融实验，系统性地揭示了部件追踪能力和接触关系推理是当前模型的关键能力缺口，为后续研究指明了明确的改进方向。

## 整体框架

FLAT-PACK BENCH 的评估框架围绕一个核心洞察构建：现有 LVLM 在细粒度时空推理上的根本性缺陷，源于其无法有效利用视频中的时间信息进行多帧关联。为此，该基准设计了一套从数据构建到标准化评测的完整流水线，将家具组装视频转化为可精确量化模型时空理解能力的多项选择问答。

### 流水线总览

整个框架由五个核心模块串联而成，形成“数据增强 → 视觉提示 → 任务模板 → 多模态提示工程 → 零样本评估”的闭环：

1.  **IMaW 数据增强与标注**：以 IKEA-Manuals-at-Work (IMaW) 数据集为基础，手工标注部件分割掩膜、部件间连接关系及对应的关键时间戳。这些细粒度标注是生成追踪、配对等复杂问题的前提。
2.  **视觉提示构建**：为每个问题生成带有颜色掩膜、边界线和文本标签的静态参考图像。这些视觉提示将视频中模糊的“部件”概念转化为模型可明确指代的目标，是连接视频动态与问题语义的关键桥梁。
3.  **任务模板生成**：围绕四个核心时空能力——时间排序 (TORD)、时间定位 (TLOC)、部件配对 (MATE) 和部件追踪 (TRACK)——设计多项选择模板。所有问题均由标注员手动审核，以消除仅凭常识或静态线索即可作答的捷径。
4.  **多模态提示工程**：将视频、视觉提示与文本问题组合为模型输入。框架测试了三种提示组织方式：**混合-媒体**（视频与图像作为独立输入）、**拼贴**（每帧视频与视觉提示拼接为网格）和**拼接**（视觉提示作为视频的额外帧追加），并系统评估了关键帧采样与修剪视频的影响。
5.  **零样本评估**：采用贪心解码与正则表达式匹配，对所有闭源和开源 LVLM 进行标准化评测，确保可复现性。

### 输入输出规范

-   **输入**：一个完整的评测样本包含三部分——一段家具组装视频、1-2 张视觉提示图像、以及一个多项选择问题与固定的任务指令。任务指令明确描述了多模态输入的格式和期望的输出形式。
-   **输出**：模型需从四个选项中选出唯一正确答案。评估指标为微平均准确率 (Micro Avg.)，按 TORD、TLOC、MATE、TRACK 四个子任务分别统计。

### 关键设计决策

框架的两个设计决策直接对应了分析中揭示的因果机制：

-   **视觉提示作为追踪锚点**：部件追踪能力是解决时空理解任务的关键操作，但模型在开放视频中难以稳定锁定目标。视觉提示通过提供目标部件的明确外观和标识，将追踪问题转化为“视频中的某区域是否与提示图像中的部件匹配”，降低了纯视觉搜索的难度，从而更纯粹地暴露模型的时空关联能力。
-   **手工审核消除捷径**：错误分析表明，模型倾向于依赖静态图像线索和常识捷径（如部件 ID 的顺序），而非真正利用时间上下文。通过人工审核每个问题的选项，框架确保正确答案必须通过理解视频中的时间演化或空间交互才能得出，使得基准分数能够真实反映模型的时空推理水平。

### 代理基线：Temporal Video Agent (TVA)

除直接评估 LVLM 外，框架还引入了一个代理基线（Figure 5），以探测专用视觉工具能否弥补 LVLM 的追踪缺陷。TVA 的工作流为：由代码 LLM 根据 API 规范和输入问题生成程序，该程序调用 SAM2 等视觉工具对视频进行目标分割与追踪，最终基于工具返回的掩膜和帧索引生成答案。这一设计将“感知”与“推理”显式分离，为分析 LVLM 的瓶颈究竟在视觉编码端还是时序推理端提供了对照。然而，实验结果表明，即使借助 SAM2 的精确分割，TVA 在 TRACK 任务上的表现依然有限，进一步印证了接触关系推理等高层时空理解才是当前系统的核心短板。

![[assets/figures/papers/paper_list_l2741_https_arxiv_org_abs_2605_21625/figures/009_Figure_5.jpg]]
*Figure 5: Temporal Video Agent. An overview of our agentic baseline. First, a Code LLM uses the API specification and the input question to generate a program. The generated program uses the assembly video and the visual prompt’s frame index and mask to produce a response for the question. We also show an example trace for a question. We can analyse the execution trace to pin-point the sources of error*

### 补充图表

![[assets/figures/papers/paper_list_l2741_https_arxiv_org_abs_2605_21625/figures/001_Figure_1.jpg]]
*Figure 1: Motivation for FLAT-PACK BENCH. For AI assistants to understand an assembly process through observation, they need to be adept at fine-grained spatio-temporal reasoning about the video. We propose FLAT-PACK BENCH to evaluate Large Vision-Language Models on four such fine-grained video understanding tasks, namely – Temporal Ordering, Temporal Localization, Tracking, and Mating*

![[assets/figures/papers/paper_list_l2741_https_arxiv_org_abs_2605_21625/figures/003_Figure_2.jpg]]
*Figure 2: Snapshot of FLAT-PACK BENCH. Each question consists of an assembly video (top row), one or two visual prompts (Images A, B), and a multiple-choice question. The corresponding visual inputs are shown within each question box. Videos are sourced from the internet and may include artifacts like overlaid text. For clarity, part labels are enlarged, as the visual prompts are shown at reduced scale*

## 核心模块与公式推导

本文的核心贡献在于构建了一个系统化的视频时空理解评估框架，而非提出新的模型架构或数学公式。因此，本节将重点阐述构成该基准的四个关键功能模块及其设计逻辑，文中未涉及需要推导的数学公式。

### 1. 数据增强与细粒度标注模块

该模块以 **IMaW**（IKEA-Manuals-at-Work）数据集为基础，进行深度二次标注，是基准构建的根基。其核心操作包括：
- **部件分割与连接关系标注**：对家具的各个部件进行像素级分割掩膜标注，并明确记录部件之间的连接关系（如螺丝与孔洞的配对）及其发生的时间戳。这为后续生成需要精确时空理解的问题提供了真值依据。
- **时间戳对齐**：将部件的装配动作、状态变化与视频时间轴精确对齐，使得生成的问题能够考察模型对“何时发生何事”的定位能力。

### 2. 视觉提示构建模块

为了将细粒度的部件查询与视频内容关联，该工作设计了视觉提示机制，这是连接问题与多模态输入的桥梁。其构建流程如下：
- **部件渲染**：对于每个问题，系统会生成一张或多张静态图像。在这些图像上，目标部件被高亮显示，具体通过以下元素组合实现：
  - **颜色掩膜**：覆盖在部件上的半透明彩色区域。
  - **边界线**：勾勒部件轮廓的实线。
  - **文本标签**：标注在部件旁的唯一标识符（如“A”、“B”）。
- **参考锚定**：这些视觉提示作为问题的一部分，为模型提供了明确的视觉参考，避免了在视频帧中直接进行复杂文字描述的歧义。

### 3. 任务模板与问题生成模块

该模块定义了基准的评测维度，通过四类任务模板系统性地考察时空理解能力。所有问题均为多项选择题，由人工标注员基于标注数据手动创建并审核，以防止模型利用统计捷径。

| 任务类型 | 核心考察能力 | 问题示例 |
| :--- | :--- | :--- |
| **TORD** (Temporal Ordering) | 时序排序：判断装配动作的先后顺序。 | 给定两个部件的视觉提示，判断哪个部件先被安装。 |
| **TLOC** (Temporal Localization) | 时间定位：识别特定装配状态发生的时刻。 | 在视频中定位两块木板何时被拼接在一起。 |
| **MATE** (Part Mating) | 部件匹配：理解部件间的空间连接关系。 | 给定一个部件的视觉提示，判断它应该与哪个部件连接。 |
| **TRACK** (Tracking) | 目标追踪：在视频全程中持续定位并识别特定部件。 | 在视频中追踪带有特定颜色标记的部件，判断其最终位置。 |

### 4. 多模态提示工程模块

为探索LVLM处理视频和图像的最优输入方式，该工作设计并测试了三种多模态提示组合策略：
- **混合-媒体**：将视频和视觉提示图像作为两个独立的输入模态提供给模型。
- **拼贴**：将视觉提示图像固定地嵌入到视频每一帧的网格中，形成一个新视频。
- **拼接**：将视觉提示图像拼接在视频帧序列之后，作为一个超长视觉序列输入。

实验表明，**混合-媒体**策略在多数任务上表现更优，这可能因为它允许模型独立地对视频和提示进行特征提取，避免了信息干扰。

### 核心瓶颈与机制分析

尽管上述模块构成了一个严密的评估体系，但分析揭示了当前模型在解决此类任务时的根本性缺陷，这构成了本工作的核心发现而非公式：
- **追踪与接触推理是关键操作**：模型在 **TRACK** 和 **MATE** 任务上的糟糕表现表明，缺乏有效的部件追踪能力和部件间接触关系推理能力是主要瓶颈。
- **视频时间信息利用失效**：消融实验（Table 4）显示，移除视频仅保留图像提示时，模型在 **TRACK** 任务上性能断崖式下降，但在 **TLOC** 和 **MATE** 任务上反而提升。这证明模型并未真正利用视频中的时间上下文进行推理，而是过度依赖静态图像线索和常识性捷径。打乱部件ID标签会损害 **TORD** 性能，进一步证实了模型依赖非时间性捷径的结论。

## 实验与分析

### 主实验结果

FLAT-PACK BENCH 在 602 道多项选择题上对一系列闭源和开源大型视觉-语言模型（LVLM）进行了零样本评估，结果如 Table 2 所示。人类表现（内部计算机科学专业学生小组与 Prolific 众包平台，采用多数投票）达到 **94.18%** 的 Micro Avg. 准确率，且在所有四个子任务上均超过 90%，验证了基准的可解性。相比之下，当前最先进的 LVLM 表现严重滞后：

![[assets/figures/papers/paper_list_l2741_https_arxiv_org_abs_2605_21625/figures/004_Table_2.jpg]]
*Table 2: Results on FLAT-PACK BENCH. Best model and best open model are highlighted in each column*

- 最强闭源模型 **GPT-5** 仅取得 **37.71%** 的 Micro Avg.，仅比频率随机基线（26.74%）高约 11 个百分点。
- 最强开源模型 **InternVL3-78B** 达到 **41.03%**，略优于 GPT-5，但仍远低于人类水平。
- 其他模型如 **Gemini 2.5 Pro**（40.20%）、**Qwen2.5-VL-72B**（40.20%）表现相近，整体集中在 30%–41% 区间。

这一巨大差距揭示了一个根本性瓶颈：**现有 LVLM 无法有效利用视频中的时间信息进行细粒度时空推理**，尤其是在需要多帧关联的目标追踪和空间交互理解上。

### 子任务难度分析

从 Table 2 的分任务结果来看，四类子任务的难度存在显著差异：

- **TRACK（部件追踪）** 是模型表现最差的任务，GPT-5 仅 28.21%，InternVL3-78B 为 30.77%，表明模型在长视频中持续定位和关联同一部件的能力极度薄弱。
- **TORD（时间排序）** 相对表现较好，GPT-5 达到 52.38%，但考虑到该任务仅有 2–3 个选项，这一成绩仍不理想。
- **TLOC（时间定位）** 和 **MATE（部件匹配）** 的表现介于两者之间，多数模型在 30%–45% 区间。

值得注意的是，人类在所有子任务上均表现均衡（>90%），而模型的表现差异暗示其可能依赖不同的、非时间性的捷径策略。

### 语言提示策略消融

为探究推理增强技术是否有助于时空理解，论文测试了零样本思维链（ZS-CoT）和自洽思维链（SC-CoT）两种策略（Table 3）。以 Qwen2.5-VL-72B 为测试对象：

![[assets/figures/papers/paper_list_l2741_https_arxiv_org_abs_2605_21625/figures/005_Table_3.jpg]]
*Table 3: Effect of Lingustic Prompting Strategies. Both ZS-CoT and SC-CoT fail to improve performance on FLAT-PACK BENCH*

- 原始提示（Vanilla）Micro Avg. 为 **40.19%**。
- ZS-CoT 降至 **39.20%**（−0.99），SC-CoT 大幅降至 **32.23%**（−7.96）。
- InternVL3-78B 上观察到类似趋势（Table S.4），两种 CoT 策略均未带来提升。

这一反直觉的结果表明：**在语言推理中有效的思维链提示，在时空视觉理解中反而适得其反**。可能的原因是模型生成的解释引入了错误的时间推理链条，或模型无法将语言推理能力有效迁移到视觉-时间域。

### 视觉数据消融

Figure 3 展示了视觉提示和视频处理方式的系统消融结果：

![[assets/figures/papers/paper_list_l2741_https_arxiv_org_abs_2605_21625/figures/006_Figure_3.jpg]]
*Figure 3: Visual Data Ablation. We study the effect of different strategies of providing the visual prompt and video processing (a). Next, we analyze how the (b) color scheme, (c) mark type, and (d) mark size affect the LVLM’s performance on our benchmark*

- **提示方式**（Figure 3a）：混合-媒体（Mixed-media）提示普遍优于拼贴（Collage）和拼接（Concat）方式。这可能是因为混合-媒体方式保持了视频和视觉提示的独立性，避免了拼贴造成的空间分辨率损失和拼接造成的时间信息稀释。
- **颜色方案**（Figure 3b）：颜色对比度对性能影响有限，但使用高对比度颜色标记不同部件时略有优势。
- **标记类型**（Figure 3c）：同时渲染标签、边界框和分割掩膜对模型性能至关重要，单独使用任一种标记方式均导致性能下降。
- **标记大小**（Figure 3d）：标记尺寸变化对性能影响不显著。

### 视频信息的关键作用

Table 4 的“仅图像提示”消融实验是揭示模型缺陷的关键证据。当移除视频、仅提供视觉提示图像时：

![[assets/figures/papers/paper_list_l2741_https_arxiv_org_abs_2605_21625/figures/007_Table_4.jpg]]
*Table 4: Image-only Prompt. Performance of the LVLM using image-only prompts, along with the change (∆) in performance from when the video is included in the prompt*

- 整体 Micro Avg. 下降 **8.80** 个百分点（从 40.20% 降至 31.40%）。
- 但下降几乎完全来自 **TRACK 子任务**（−24.51%），而 **TLOC**（+4.85%）和 **MATE**（+5.75%）反而有所提升。

这一发现表明：**模型并未真正利用视频中的时间信息**。在 TRACK 任务中，模型可能仅依赖视觉提示中的部件外观进行猜测，缺乏视频时性能崩溃；而在 TLOC 和 MATE 任务中，模型可能依赖静态图像线索和常识捷径，视频的加入反而引入了噪声。

### 部件 ID 捷径

Table 4 还报告了打乱部件 ID 的影响。打乱后 TORD 任务性能显著下降，揭示模型利用了部件 ID 的排列顺序作为非时间性捷径——模型可能通过记忆 ID 的字母/数字顺序来判断组装步骤，而非真正理解视频中的时间先后关系。

### 错误分析

论文对模型错误进行了分类统计（Section 5.4），主要错误来源为：

- **目标定位错误**（37.28%）：模型无法在视频帧中准确定位目标部件。
- **时空推理错误**（32.45%）：模型对部件间的时间关系和空间交互理解错误。
- 其余错误涉及视觉提示误读、选项混淆等。

Figure 4 展示了 Gemini 2.5 Pro 的自我探测解释示例：模型虽然“看到”了视频中的相关连接事件，但由于时空推理中的缺口而做出错误判断，进一步证实了追踪和接触关系推理是当前 LVLM 的核心短板。

![[assets/figures/papers/paper_list_l2741_https_arxiv_org_abs_2605_21625/figures/008_Figure_4.jpg]]
*Figure 4: Self-probing Explanations. Qualitative example from Gemini 2.5 Pro. We highlight the video with the relevant connection events for clarity. We can observe that the model looks at the video, but makes an error due to gaps in its spatio-temporal reasoning*

### 代理基线实验

论文还设计了一个基于编程的 Temporal Video Agent（TVA，Figure 5），该代理使用代码 LLM 生成程序，调用 SAM2 等视觉工具进行部件追踪和接触推理。Table 5 的结果显示：

![[assets/figures/papers/paper_list_l2741_https_arxiv_org_abs_2605_21625/figures/010_Table_5.jpg]]
*Table 5: Agent performance. Acc. (Answered) is accuracy over non-abstained questions*

- TVA 的总体准确率仍不理想，且存在较高的弃权率。
- 即使借助专用视觉工具，代理在接触推理任务上的表现依然很差（Table S.3，Qwen2.5-VL 在接触推理模板上表现极低）。

这表明：**当前的视觉工具（如 SAM2）在细粒度部件追踪和接触关系理解上同样存在严重不足**，简单的工具集成无法弥补 LVLM 的根本性缺陷。

### 关键结论

综合以上实验分析，FLAT-PACK BENCH 揭示了以下核心发现：

1. **人类与模型之间存在巨大差距**（94.18% vs. ~38%），家具组装视频理解远未解决。
2. **部件追踪（TRACK）和接触关系推理是当前模型的核心瓶颈**，模型严重依赖静态图像线索和 ID 顺序等非时间性捷径。
3. **思维链提示在时空视觉理解中失效**，暗示语言推理与视觉-时间推理之间存在根本性的迁移障碍。
4. **混合-媒体提示是目前最优的视觉提示策略**，但视觉提示设计对性能的提升有限，根本问题在于模型缺乏细粒度时空交互理解能力。

### 补充图表

![[assets/figures/papers/paper_list_l2741_https_arxiv_org_abs_2605_21625/figures/002_Table_1.jpg]]
*Table 1: Dataset composition: Shows the number of videos (#V), questions (#Q), and templates per category (#T), along with average questions per video (Q/V), per template (Q/T), and unique templates per video (uT/V)*

![[assets/figures/papers/paper_list_l2741_https_arxiv_org_abs_2605_21625/figures/014_Table_S.2.jpg]]
*Table S.2: Human evaluation summary on FLAT-PACK BENCH. We show the performance of Prolific and our in-house participants, along with some reference models on the same subset of questions. Agreement is measured by unanimous response rate*

![[assets/figures/papers/paper_list_l2741_https_arxiv_org_abs_2605_21625/figures/017_Table_S.3.jpg]]
*Table S.3: Contact-Reasoning Results. We show the performance of Qwen2.5-VL (32B & 72B) across two question templates. The overall performance is quite poor across all settings*

## 方法谱系与知识库定位

### 任务定义与问题边界

FLAT-PACK BENCH 面向的是**长视频中多物体交互的细粒度时空理解**，其核心任务可分解为四类操作：时间排序（TORD）、时间定位（TLOC）、部件配对（MATE）和部件追踪（TRACK）。这四类任务共同要求模型不仅理解单帧的空间关系，还必须建立跨帧的时间因果链——即“谁在何时与谁发生了何种交互”。

该基准的适用边界明确：当前版本仅覆盖家具组装领域（50个视频，602道多选题），且视频均来自 IMaW 数据集。对于其他需要长时程时空推理的场景（如手术操作、机械维修、烹饪流程），其泛化性尚未验证。此外，基准设计依赖视觉提示（visual prompts）来指代特定部件，这意味着模型必须同时理解视频流和静态标注图像之间的对应关系，这对多模态融合能力提出了额外要求。

### 与现有基准的关系定位

FLAT-PACK BENCH 在视频理解评测谱系中占据了一个独特的生态位。传统视频问答基准（如 ActivityNet-QA、Next-QA）侧重动作识别或粗略时序定位，而该基准将粒度推进到**部件级交互理解**——需要模型判断“螺丝 A 是否已插入孔 B”或“面板 C 在视频的哪个时间段被安装”。这种粒度要求模型具备接触关系推理（contact reasoning）能力，而非仅依赖场景上下文进行推断。

在方法层面，该工作揭示了现有 LVLM 的一个根本性瓶颈：**即使最先进的模型也无法有效利用视频中的时间信息**。消融实验（Table 4）给出了决定性证据——移除视频仅保留图像提示时，模型整体性能仅下降 8.80 个百分点，且下降几乎完全来自 TRACK 子任务（-24.51%），而 TLOC 和 MATE 反而分别提升 4.85 和 5.75 个百分点。这说明模型在 TLOC 和 MATE 任务上主要依赖静态图像线索和常识捷径，而非真正理解时间进程。打乱部件 ID 后 TORD 性能下降的现象（Table 4）进一步证实了这种捷径依赖。

### 方法适用性与局限

**思维链的失效**是该工作最值得关注的方法论发现之一。零样本思维链（ZS-CoT）和自洽思维链（SC-CoT）在语言推理中已被广泛验证有效，但在该基准上均未带来提升，SC-CoT 甚至导致性能从 40.19 降至 32.23（Table 3）。这一反直觉现象暗示：语言化的逐步推理可能与视觉时空信息的处理机制存在根本性冲突——模型在生成文本解释时可能分散了对视频时序线索的注意力，或文本推理路径无法有效编码空间交互的动态变化。

**视觉提示设计**方面，消融实验（Figure 3）表明同时渲染标签、边界和掩膜对模型性能至关重要，而颜色对比度和标记大小的影响相对有限。混合-媒体提示（将视觉提示作为独立图像与视频分开输入）普遍优于拼贴和拼接方式，这可能因为前者保持了视频帧的原始分辨率，避免了拼接导致的细节丢失。

**代理方法的局限**同样值得关注。Temporal Video Agent（TVA）尝试借助 SAM2 等专用视觉工具来弥补 LVLM 的追踪缺陷，但效果有限（Table 5）。这暴露出当前视觉基础模型在接触关系推理上的共同短板——即使将任务分解为“检测-追踪-推理”的流水线，接触事件的判定仍缺乏可靠的算法原语。

### 开放问题

1. **思维链的负面效应机制**：为何语言推理中有效的 CoT 策略在时空视觉理解中适得其反？这是否意味着需要设计专门的视觉思维链（visual chain-of-thought），而非简单套用文本推理模板？

2. **追踪与接触推理的原语化**：能否将复杂时空任务分解为追踪和接触推理两个基本原语，并分别训练专用模块？这需要构建富含部件级交互标注的训练数据。

3. **混合-媒体提示的优势根源**：该提示方式为何普遍优于拼贴和拼接？是分辨率保持、注意力分配还是模态对齐的差异所致？

4. **长视频交互的合成数据路径**：能否通过大规模合成数据（如物理仿真环境中的装配过程）或强化学习来提升 LVLM 对多物体交互的追踪能力？这可能是突破当前性能瓶颈的关键方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/Flat_Pack_Bench_Evaluating_Spatio_Temporal_Understanding_in_Large_Vision_Language_Models_through_Furniture_Assembly.pdf]]
