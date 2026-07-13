---
title: "EgoProx: Evaluating MLLMs on Egocentric 3D Proximity Reasoning Across a Cognitive Hierarchy"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/EgoProx_Evaluating_MLLMs_on_Egocentric_3D_Proximity_Reasoning_Across_a_Cognitive_Hierarchy.pdf
project_link: "https://lijinzhao30.github.io/Egoprox/"
code_link: null
aliases:
- EBADE
- EgoProx
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 利用基于代理的数据引擎生成的特定任务指令调优数据，尤其是意图类数据，能够显著激活模型中的空间知识，带来跨任务和跨数据集的大幅性能提升。
primary_logic: 按认知层次（意图、探索、利用、动作链）组织自我中心3D接近度推理任务，并通过基于代理的数据引擎自动合成高质量VQA数据，可以系统性地评估和改善MLLMs的空间智能。
claims:
- 人类水平在动作链任务上的动作准确率（Act-Acc）为80.23%，而最佳MLLM（Gemini-2.5-Pro）仅为25.14%，差距巨大（-55.09%），凸显长程推理短板。
- 仅在意图数据上微调后，Qwen2.5-VL-7B在利用任务的近似准确率从38.63%跃升至64.93%（+26.30%），验证了认知层次间的正向迁移。
- 跨数据集微调同样有效：EgoExo4D调优后，在ADT上的利用任务准确率从47.64%提升至64.57%（+16.93%），证明空间知识具有域迁移性。
- EgoProx Chain of Actions 上 Act-Acc = 80.23 (Human Level)
---

# EgoProx: Evaluating MLLMs on Egocentric 3D Proximity Reasoning Across a Cognitive Hierarchy

> [!tip] 核心洞察
> 按认知层次（意图、探索、利用、动作链）组织自我中心3D接近度推理任务，并通过基于代理的数据引擎自动合成高质量VQA数据，可以系统性地评估和改善MLLMs的空间智能。

| 字段 | 内容 |
|------|------|
| 中文题名 | EgoProx：认知层次下的自我中心3D接近度推理评估基准 |
| 英文题名 | EgoProx: Evaluating MLLMs on Egocentric 3D Proximity Reasoning Across a Cognitive Hierarchy |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Li_EgoProx_Evaluating_MLLMs_on_Egocentric_3D_Proximity_Reasoning_Across_a_CVPR_2026_paper.html) · [Project](https://lijinzhao30.github.io/Egoprox/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | EgoProx Benchmark and Agentic Data Engine |
| Dataset | EgoProx Chain of Actions, EgoProx Exploitation, EgoProx Intention, EgoProx Cross-dataset Exploitation |

> [!tip] 效果简介
> - EgoProx Chain of Actions 上，Act-Acc 80.23 (Human Level) vs 25.14 (Gemini-2.5-Pro) (-55.09)。
> - EgoProx Exploitation 上，Approx. Accuracy 64.93 (Qwen2.5-VL-7B + Intention Tuning) vs 38.63 (Qwen2.5-VL-7B) (+26.30)。
> - EgoProx Intention 上，Approx. Accuracy 56.48 (Qwen2.5-VL-7B + Exploitation Tuning) vs 33.68 (Qwen2.5-VL-7B) (+22.80)。

## 概要

**问题瓶颈**：现有MLLMs的预训练数据中虽蕴含隐式空间知识，但缺乏结构化的监督信号来有效检索和利用这些知识进行空间推理。这导致模型在需要认知层次推理的自我中心3D接近度任务上表现显著不足——人类在动作链任务上的动作准确率（Act-Acc）达80.23%，而最佳MLLM（Gemini-2.5-Pro）仅为25.14%，差距高达55.09个百分点（Table 2）。

**核心方法**：本文提出EgoProx基准，按认知层次（意图、探索、利用、动作链）组织自我中心3D接近度推理任务，并开发基于代理的数据引擎自动合成高质量VQA数据。该引擎以Gemini-2.5-Pro为基础，协调显著片段采样器、占据地图生成器、A*路径生成器、空间计算器、注视解析器、可供性检测器、关键步骤提取与链构建器等专用工具，针对不同任务类型定制数据生成流程（Figure 2）。

**方法谱系与知识库定位**：EgoProx属于**空间推理评估基准与数据增强方法**。与现有3D推理VQA基准（如**SpatialVLM**、**3D-LLM**等）相比，EgoProx首次将自我中心视频中的接近度推理按认知层次系统化，并引入基于代理的自动化数据生成范式（Table 1）。其数据引擎生成的指令调优数据可作为现有MLLMs（**Qwen2.5-VL-7B**、**LLaVA-NeXT-Video-7B**等）的训练增强，弥补预训练中结构化空间监督信号的缺失。

**主要结果**：
- **跨类别迁移**：仅在意图数据上微调后，Qwen2.5-VL-7B在利用任务的近似准确率从38.63%跃升至64.93%（+26.30%）；反之，利用调优也使意图任务提升22.80个百分点（Table 3），验证了认知层次间的正向迁移。
- **跨数据集泛化**：在EgoExo4D上调优后，模型在ADT上的利用任务准确率从47.64%提升至64.57%（+16.93%），证明空间知识具有域迁移性（Table 4）。
- **关键洞察**：基于代理的数据引擎生成的特定任务指令调优数据——尤其是意图类数据——能够显著激活模型中的隐式空间知识，带来跨任务和跨数据集的大幅性能提升。

**局限与开放问题**：基准规模有限（2405个样本），场景多样性受限于EgoExo4D和ADT两个数据集；动作链任务的严格空间关系评估指标可能过于苛刻。未来需探索将数据引擎扩展至更广泛的自我中心视频，以及通过模型架构创新（如融入显式3D表征）更彻底地解决空间推理瓶颈。



### 问题背景：自我中心3D空间智能的评测困境

具身智能体在真实世界中执行任务时，必须持续感知自身与周围物体的空间关系，并据此做出行动决策。这种以第一人称视角进行的**自我中心3D接近度推理**（Egocentric 3D Proximity Reasoning）是空间智能的核心能力之一。然而，现有评测体系对此类能力的系统性评估存在显著缺口。

当前多模态大语言模型（MLLMs）在图像理解、视频问答等任务上取得了长足进步，但其空间推理能力——尤其是从自我中心视频中推断物体间的距离、方向和空间变换关系——仍然远未达到人类水平。问题的根源在于：**MLLMs在预训练阶段虽已编码了大量隐式空间知识，但缺乏结构化的监督信号来有效检索和激活这些知识**，导致模型在面对需要深层空间理解的查询时表现乏力。

### 现有基准的局限

已有的3D推理或自我中心活动VQA基准存在多方面不足（见Table 1对比）。从推理类型来看，现有工作多聚焦于单帧的空间定位或短时动作识别，缺乏对**长时程、多步骤空间关系推理**的支持。从数据构造方式来看，人工标注成本高昂且难以规模化，而基于MLLM/LLM的自动生成方法又难以保证3D空间标注的精度。更关键的是，现有基准未能按照认知层次对空间推理任务进行系统化组织，导致评估结果难以揭示模型在不同认知深度上的能力差异。

### 本文动机

针对上述缺口，本文提出**EgoProx基准**，核心动机包括：

1. **建立认知层次化的评测体系**：将自我中心3D接近度推理任务按照认知层次组织为意图（Intention）、探索（Exploration）、利用（Exploitation）和动作链（Chain of Actions）四个维度，从单步空间预测到多步关系推理逐级递进，系统性地评估MLLMs的空间智能。

2. **构建可规模化的数据生成引擎**：开发基于代理的数据引擎，通过协调多个专用工具（如显著片段采样器、占据地图生成器、空间计算器等）自动合成高质量VQA数据，解决人工标注的瓶颈问题。

3. **揭示认知层次间的迁移机制**：通过跨类别指令调优实验，验证认知层次间的正向迁移效应——例如，意图推理能力的提升能否带动利用阶段的空间推理表现，从而为模型的空间智能增强提供可操作的训练策略。



## 核心方法与创新机理

EgoProx 的核心创新不在于提出一个全新的模型架构，而在于构建了一套**系统性的评估与数据生成框架**，直击当前多模态大模型（MLLM）在自我中心 3D 空间推理上的结构性短板。其创新点可归纳为以下三个紧密耦合的层面：

### 1. 认知层次驱动的任务组织方式

现有空间推理基准（如 SpatialVLM、SceneScript）多聚焦于单一维度的 3D 理解，而 EgoProx 首次将自我中心 3D 接近度推理按照**认知层次**组织为四个递进维度：**意图（Intention）→ 探索（Exploration）→ 利用（Exploitation）→ 动作链（Chain of Actions）**。这一设计并非简单的任务堆砌——其内在逻辑是：意图驱动中间目标的选择，进而引导对环境的探索与利用，最终串联为长程动作序列。这种层次化组织使得基准能够诊断模型在哪个认知阶段出现能力断裂，而非仅仅给出一个聚合分数。

### 2. 基于代理的数据引擎：从隐式知识到显式监督信号

这是本文最具方法论价值的创新。核心洞察在于：现有 MLLM 的预训练数据中**已编码了大量隐式空间知识**，但缺乏结构化的监督信号来有效检索和利用这些知识。EgoProx 提出的**代理数据引擎**以 Gemini-2.5-Pro 为基座，编排了一套专用工具链（包括 Salient Clip Sampler、Occupancy Map Generator、Exploration Path Generator、Spatial Calculator、Gaze Parser、Affordance Detector、Chain Constructor 等），自动从长视频中合成高质量 VQA 数据。其关键设计在于：

- **任务感知的片段采样**：Salient Clip Sampler 基于交互与注视信息提取关键片段，确保每个样本都承载有效的空间推理信号。
- **3D 真值自动标注**：利用数据集自带的 3D 边界框、注视数据等，通过工具链自动计算平移距离、方向角度、占据地图和可行路径，生成结构化空间真值，避免了昂贵的人工标注。
- **可控的 QA 合成**：针对不同认知层次任务定制生成流程，确保数据与评估维度精确对齐。

这一引擎的产出直接转化为**指令调优数据**，成为激活模型隐式空间知识的“因果旋钮”。

### 3. 跨层次与跨域的知识迁移验证

EgoProx 的实验设计揭示了认知层次间的**正向迁移效应**——这是超出基准构建本身的科学发现。具体而言：

- **意图调优 → 利用提升**：仅在意图数据上微调后，Qwen2.5-VL-7B 在利用任务的近似准确率从 38.63% 跃升至 64.93%（+26.30%），表明意图推理能力可正向迁移至空间利用阶段。
- **探索调优 → 动作链提升**：探索数据调优后，动作链任务的动作准确率（Act-Acc）从 5.98 提升至 7.61，严格关系准确率（Rel-Acc-S）从 2.27 跃升至 14.29，证明空间路径规划能力有助于多步推理。
- **跨数据集迁移**：在 EgoExo4D 上调优后，模型在 ADT 数据集上的利用任务准确率从 47.64% 提升至 64.57%（+16.93%），验证了空间推理知识的**域迁移性**。

这一发现的意义在于：它证明了按认知层次组织训练数据是高效激活空间智能的有效策略，而非仅仅堆砌数据量。

### 与 Baseline 的本质差异

相较于现有基准（Table 1），EgoProx 的关键区分点在于：

- **构建方式**：采用代理自动生成（agent-based generation），而非纯人工标注或 LLM 生成，兼顾了规模性与 3D 真值的精确性。
- **推理类型覆盖**：同时涵盖预测（F）、规划（P）和因果推理（C），而多数现有基准仅覆盖其中 1-2 类。
- **时序推理范围**：动作链任务要求模型在长时序窗口内进行多步空间关系推理，这在现有基准中几乎未被触及。

综上，EgoProx 的创新本质是**“诊断工具 + 修复方案”的一体化**：基准本身揭示了 MLLM 在认知层次空间推理上的巨大鸿沟（人类 80.23% vs. 最佳模型 25.14%），而数据引擎则提供了填补这一鸿沟的可行路径。



EgoProx 的整体框架由两部分构成：一个按认知层次组织的**3D接近度推理基准**，以及一个用于自动合成高质量VQA数据的**基于代理的数据引擎**。两者协同工作，前者定义了评估空间智能的任务体系，后者为这些任务提供可扩展的标注数据。

### 基准的认知层次结构

EgoProx 基准将自我中心3D接近度推理任务沿认知层次组织为四个维度：**意图（Intention）**、**探索（Exploration）**、**利用（Exploitation）**和**动作链（Chain of Actions）**。这一层次结构反映了人类空间认知的递进关系——意图驱动中间目标的选择，进而引导对3D环境的探索与利用，而动作链则要求对多步操作序列及其空间依赖进行长程推理。

基准采用两类接近度度量方式：
- **近似接近度（Approximate proximity）**：编码最后可观测时间步所需的粗略度量变换，包括角度旋转和平移距离，经离散化后映射为人类可解释的区间；
- **相对接近度（Relative proximity）**：将3D方向投影到指定平面后转换为八个离散方向，用于表示物体间的空间关系。

### 基于代理的数据引擎

为系统性地生成跨任务类别的高质量VQA数据，EgoProx 构建了一个以 **Gemini-2.5-Pro** 为基础代理的数据引擎，该代理编排多个专用工具，以可控方式合成问答对。其流水线包含以下核心模块：

| 模块 | 功能 | 证据锚点 |
|------|------|----------|
| **Salient Clip Sampler** | 从长时程自我中心视频中提取与任务相关的关键片段 | Section 4.1 |
| **Occupancy Map Generator** | 根据3D边界框生成占据地图 | Section 4.2 |
| **Exploration Path Generator** | 使用A*算法计算可行路径 | Section 4.2 |
| **Spatial Calculator** | 计算平移距离和方向角度 | Section 4.2 |
| **Gaze Parser** | 将2D注视数据转换为3D注视射线并定位注视物体 | Section 4.2 |
| **Affordance Detector** | 检测未来帧中与目标物体的交互提供性 | Section 4.2 |
| **Keystep Extraction Tool** | 提取视频中的关键动作步骤 | Section 4.2 |
| **Chain Constructor** | 构建可能的关键步骤链并计算步骤间的空间关系 | Section 4.2 |

### 数据生成流程

数据引擎的工作流程针对每个任务类型进行定制。首先，**Salient Clip Sampler** 采用交互和注视驱动的采样策略，从长视频中识别显著时刻，提取包含 $T$ 帧的理想片段 $\mathcal{X} = \{ x_1, x_2, \dots, x_T \}$，其中 $x_T$ 为当前帧，$x_1, \dots, x_{T-1}$ 为过去帧。随后，**3D分析工具集**提取空间线索，包括物体位置、注视目标、占据地图和动作链。**Spatial Calculator** 据此推导3D距离、方向和接近度关系，生成结构化的3D接近度真值。最终，经过必要的后处理，输出基准所需的问答对。

### 关键设计决策

该框架的核心设计在于**通过认知层次组织任务**，使数据引擎能够按层次生成训练数据，从而验证不同认知层次间的正向迁移效应。实验表明，仅在意图数据上微调即可显著提升利用任务的性能（+26.30%，Table 3），验证了这一层次结构的内在关联性。同时，数据引擎的自动化特性使其具备跨数据集扩展能力——在EgoExo4D上生成的调优数据可有效迁移至ADT数据集（+16.93%，Table 4），证明空间推理知识具有域迁移性。

### 补充图表

![[assets/figures/papers/paper_list_l819_https_openaccess_thecvf_com_content_CVPR2026_html_Li_EgoProx_Evaluating/figures/001_Figure_1.jpg]]
*Figure 1: Visual illustration of the EgoProx benchmark. We aim to evaluate multimodal large language models (MLLMs) on complex egocentric proximity reasoning tasks that require 4D action and scene understanding. Our benchmark spans four core dimensions following a cognitive hierarchy: Intention, Exploration, Exploitation, and Chain of Actions. We adopt approximate transformations and relative spatial relationships to represent proximity. The examples illustrate the model’s need to interpret long-term contextual cues, spatial dependencies, and action-state changes from first-person visual inputs, providing a comprehensive assessment of egocentric spatial intelligence*



EgoProx 的数据引擎以一个基于 **Gemini-2.5-Pro** 的智能代理为核心，编排七个专用工具模块，按认知层次自动合成高质量 VQA 数据。整体流程遵循“关键片段采样 → 3D 空间解析 → 接近度计算 → 问答对生成”的级联结构。

### 关键模块

**Salient Clip Sampler（关键片段采样器）** 从长程自我中心视频中提取与任务相关的关键片段。它结合交互检测与注视（fixation）信号，识别出具备丰富空间语义的时间窗口，输出一个包含 $T$ 帧的视频片段 $\mathcal{X} = \{ x_1, x_2, \dots, x_T \}$，其中 $x_T$ 为当前帧，$x_1, \dots, x_{T-1}$ 为历史帧。该模块决定了后续所有空间计算的时空边界。

**Occupancy Map Generator（占据地图生成器）** 根据场景中物体的 3D 边界框生成二维占据地图，为路径规划提供可通行区域与障碍物分布的结构化表征。

**Exploration Path Generator（探索路径生成器）** 在占据地图上使用 A* 搜索算法计算从当前视点到目标物体的可行路径，输出路径节点序列及其空间坐标。

**Spatial Calculator（空间计算器）** 计算平移距离与方向角度，将原始 3D 度量转化为离散化的近似变换区间和相对空间关系，使模型输出可与人类判读对齐。

**Gaze Parser（注视解析器）** 将 2D 注视坐标投影为 3D 注视射线，并定位射线命中的目标物体，用于意图类任务中推断“注视目标”与“交互目标”之间的空间关系。

**Affordance Detector（提供性检测器）** 在视频未来帧中检测与目标物体可能发生的交互（如抓取、触碰），为利用类任务提供“可达性”与“交互可行性”的判定依据。

**Keystep Extraction Tool 与 Chain Constructor（关键步骤提取与动作链构建器）** 从视频中提取关键动作步骤，构建可能的关键步骤链，并计算步骤间的空间关系（如相对方向），支撑动作链类任务的真实标注生成。

### 关键公式与变量含义

EgoProx 的评估公式围绕动作链任务设计，核心指标定义如下：

- **输入视频片段**：$\mathcal{X} = \{ x_1, x_2, \dots, x_T \}$，其中 $x_T$ 为当前帧，$x_1, \dots, x_{T-1}$ 为过去帧。该符号贯穿所有任务类型，定义了模型可观测的时空上下文。

- **动作准确率（Act-Acc）**：$\text{Act-Acc}$，比较模型预测的动作序列节点集合与真实动作节点集合的一致性，衡量“做了什么”的准确性。

- **关系准确率（严格版，Rel-Acc-S）**：$c / (k - 1)$，其中 $c$ 为正确预测的空间关系边数，$k$ 为动作链中的节点数，分母 $k-1$ 为总边数。该指标衡量“步骤间的空间方向关系”是否被精确还原。

- **关系准确率（宽松版，Rel-Acc-L）**：$\text{Rel-Acc-L}$，当预测方向与真实方向在离散化的八个方位中相邻时即视为正确，降低对空间关系严格匹配的惩罚。

这些公式的核心设计意图在于：将连续 3D 空间中的接近度推理转化为可离散评估的符号化判断，使得 MLLM 的空间推理能力可以被严格量化。





## 实验与关键发现

### 评测设置与指标

EgoProx 在统一的评测框架下对所有模型进行零样本思维链（Chain‑of‑Thought）评估。提示模板明确定义了自我中心坐标系、世界坐标系和图像平面坐标系，确保专有模型与开源模型在相同信息条件下比较。对于需要离散化输出的任务，作者将连续的空间变换量化为人类可解释的区间：平移距离和旋转角度被映射到预定义的粗粒度区间，三维空间方向被投影到指定平面并离散为八个方位。动作链任务采用三项指标——动作准确率（Act‑Acc）比较预测动作序列与真实序列的匹配程度，严格关系准确率（Rel‑Acc‑S）定义为 $c / (k - 1)$（$c$ 为正确预测的空间关系边数，$k-1$ 为总边数），宽松关系准确率（Rel‑Acc‑L）允许预测方向与真实方向相邻即算正确。人类水平结果由至少三名评估者独立标注后取平均值获得。

### 主结果：MLLMs 与人类水平的显著差距

Table 2 汇总了主流 MLLMs 在 EgoProx 四个认知层次上的表现。最突出的瓶颈出现在动作链任务：人类水平的 Act‑Acc 达到 **80.23%**，而表现最佳的专有模型 Gemini‑2.5‑Pro 仅为 **25.14%**（差距 **‑55.09%**），开源模型 Qwen2.5‑VL‑7B 更是低至 **5.98%**。这一巨大鸿沟表明当前 MLLMs 在长程空间推理与动作序列建模上存在根本性短板，而非简单的感知不足。

![[assets/figures/papers/paper_list_l819_https_openaccess_thecvf_com_content_CVPR2026_html_Li_EgoProx_Evaluating/figures/004_Table_2.jpg]]
*Table 2: Evaluation results of prevailing MLLMs on the EgoProx benchmark, where best scores are colored with red and the second best scores are colored with orange . All models are evaluated using a unified prompt that defines the egocentric, world, and image-plane coordinate systems, and adopts zero-shot chain-of-thought prompting following [66]*

在探索任务上，专有模型整体略优于开源模型，但所有模型的绝对准确率仍远低于人类水平。利用任务和意图任务同样呈现类似趋势：MLLMs 能够捕捉部分短程空间关系，但在需要多步推理或未来状态预测的场景中性能急剧下降。值得注意的是，GPT‑5 和 Gemini‑2.5‑Pro 等最先进专有模型在各项任务上虽排名靠前，但与第二名之间的优势并不悬殊，说明该基准揭示的是整个模型家族的共性瓶颈，而非个别模型的弱点。

### 消融实验：认知层次间的正向迁移

Table 3 展示了跨类别指令调优的关键发现。作者利用数据引擎生成某一类别的额外训练数据，对 Qwen2.5‑VL‑7B 进行微调，然后评估所有类别的性能变化。

![[assets/figures/papers/paper_list_l819_https_openaccess_thecvf_com_content_CVPR2026_html_Li_EgoProx_Evaluating/figures/005_Table_3.jpg]]
*Table 3: Cross-category experimental results where best scores are colored with red . We leverage extra training data from one category generated by our data engine and evaluate performance across all categories. The additional data not only improves performance within the source category but also enhances cross-category generalization, revealing the inherent hierarchical structure of human cognition*

**意图调优的强迁移效应**：仅在意图数据上微调后，模型在利用任务的近似准确率从 **38.63% 跃升至 64.93%**（**+26.30%**），在探索任务上也获得显著增益。这意味着意图推理能力——理解“将要做什么”——能够有效激活模型中隐式的空间知识，并正向迁移至需要精确空间判断的下游任务。这一发现直接支持了论文的核心因果假设：MLLMs 并非缺乏空间知识，而是缺乏结构化的监督信号来检索和运用这些知识。

**探索调优对动作链的促进**：在探索数据上微调使动作链任务的 Act‑Acc 从 5.98 提升至 7.61，Rel‑Acc‑S 从 2.27 提升至 14.29。虽然绝对数值仍然较低，但相对改善幅度可观，表明空间路径规划能力是多步动作推理的重要基础组件。

**利用调优的反向迁移**：利用数据微调使意图任务的近似准确率从 33.68 提升至 **56.48%**（**+22.80%**），揭示了认知层次间的双向关联——精确的空间执行知识同样可以增强高层意图理解。

### 跨数据集泛化：空间知识的域迁移性

Table 4 验证了空间推理能力的跨数据集可迁移性。在 EgoExo4D 数据集上微调 Qwen2.5‑VL‑7B 后，模型在 ADT 数据集上的利用任务准确率从 47.64% 提升至 **64.57%**（**+16.93%**）。这一结果表明，通过 EgoProx 数据引擎合成的空间推理监督信号并非过拟合于单一数据分布，而是提炼出了可泛化的 3D 空间理解能力。该发现也为未来将基准扩展至更多自我中心视频数据集提供了实证支撑。

![[assets/figures/papers/paper_list_l819_https_openaccess_thecvf_com_content_CVPR2026_html_Li_EgoProx_Evaluating/figures/006_Table_4.jpg]]
*Table 4: Cross-dataset experimental results. Fine-tuning on one dataset improves proximity reasoning on the other*

### 定性分析：调优模型超越专有模型

Figure 3 展示了意图调优后的 Qwen2.5‑VL‑7B 在具体案例上超越 GPT‑5 的场景。这些案例通常涉及需要从长时程自我中心视频中提取细微空间线索的任务——例如判断物体间的相对方位变化、预测下一步的移动方向等。调优后的模型展现出更准确的空间关系推理，而未经调优的专有模型尽管拥有更强的通用能力，在这些特定空间任务上仍会出现方向误判或距离估计偏差。

![[assets/figures/papers/paper_list_l819_https_openaccess_thecvf_com_content_CVPR2026_html_Li_EgoProx_Evaluating/figures/007_Figure_3.jpg]]
*Figure 3: Visual examples of our benchmark and model performance. We show cases where the intention-tuned model outperforms the proprietary GPT-5 model*

### 补充图表

![[assets/figures/papers/paper_list_l819_https_openaccess_thecvf_com_content_CVPR2026_html_Li_EgoProx_Evaluating/figures/002_Table_1.jpg]]
*Table 1: Comparison of EgoProx with existing 3D reasoning VQA or egocentric activity VQA benchmarks. We summarize key properties including 3D awareness, dataset scale, reasoning types, construction methodology, and temporal reasoning range. The reasoning types include grounding (G), forecasting (F), planning (P), and causality (C). Benchmark construction types include human annotation, MLLM/LLM-based generation, and agent-based generation. For clarity, note that human review for quality assurance is adopted by all existing QA-generation pipelines, including ours*



## 定位与知识库关联

### 任务定位：自我中心3D空间推理的认知层次基准

EgoProx 的核心贡献在于将自我中心视频中的3D接近度推理（proximity reasoning）系统化为一个认知层次框架，而非孤立的任务集合。该框架包含四个递进的推理维度：**意图（Intention）**、**探索（Exploration）**、**利用（Exploitation）** 和 **动作链（Chain of Actions）**。这一设计区别于现有基准：

- **EgoSchema**（Mangalam et al., NeurIPS 2023）和 **EgoTaskQA**（Jia et al., CVPR 2024）等自我中心VQA基准主要关注2D场景理解和短期动作识别，缺乏对3D空间关系的显式建模。
- **SpatialBench**（Chen et al., 2024）和 **BLINK**（Fu et al., 2024）等3D推理基准虽然涉及空间关系，但多基于静态场景或第三人称视角，未覆盖自我中心视频中特有的4D动作-场景交互。
- **EgoExo4D**（Grauman et al., CVPR 2024）和 **ADT**（Pan et al., ECCV 2024）提供了丰富的自我中心多模态标注，但未将空间推理任务按认知层次组织，也未提供系统化的VQA评估框架。

EgoProx 通过**认知层次**这一组织原则，将意图预测、空间探索、目标利用和长程动作链推理统一在一个评估框架下，为MLLMs的空间智能提供了分层诊断工具。

### 数据构建方法谱系

EgoProx 的数据引擎采用了**基于代理（agent-based）的自动合成**范式，与现有数据构建方法形成对比：

| 构建范式 | 代表工作 | 特点 | EgoProx的差异 |
|---------|---------|------|-------------|
| 纯人工标注 | Ego4D (Grauman et al., CVPR 2022) | 高质量但成本高、规模受限 | 自动化合成，人工仅做质量验证 |
| LLM/MLLM生成 | LLaVA-Instruct (Liu et al., NeurIPS 2023) | 利用模型生成QA对 | 引入专用3D分析工具集，确保空间真值的物理准确性 |
| 代理+工具编排 | **EgoProx** (本文, CVPR 2026) | 代理协调多工具生成结构化QA | 任务感知的片段采样 + 3D分析工具集 + 空间计算器 |

EgoProx 的代理（基于 **Gemini-2.5-Pro**，Google DeepMind, 2024）协调以下专用工具：**Salient Clip Sampler**（基于交互和注视的任务驱动采样）、**Occupancy Map Generator**（3D占据地图生成）、**Exploration Path Generator**（A*路径规划）、**Spatial Calculator**（距离和方向计算）、**Gaze Parser**（2D注视到3D射线转换）、**Affordance Detector**（交互提供性检测）以及 **Chain Constructor**（关键步骤链构建）。这种“代理+工具集”的架构确保了生成数据的物理一致性和任务针对性，区别于纯模型生成方法可能引入的幻觉。

### 评估模型谱系

EgoProx 评估了当前主流的专有和开源MLLMs：

- **专有模型**：**Gemini-2.5-Pro**（Google DeepMind, 2024）、**GPT-5**（OpenAI, 2025）
- **开源模型**：**LLaVA-NeXT-Video-7B**（Li et al., 2024）、**Qwen2.5-VL-7B**（Wang et al., 2024）、**Qwen3-VL-235B**

所有模型均采用统一的零样本思维链（Chain-of-Thought）提示，明确定义自我中心、世界和图像平面三个坐标系，确保比较的公平性。

### 适用边界与局限

**适用边界**：
- 基准适用于评估MLLMs在自我中心视频中的3D空间推理能力，特别是需要整合长时序上下文和4D场景理解的任务。
- 基于代理的数据引擎适用于已有3D标注（如相机姿态、物体边界框、注视数据）的自我中心视频数据集，可自动扩展至新的数据源。
- 认知层次框架中的正向迁移现象（意图→利用、探索→动作链）表明，该框架可用于指导具身AI系统的分阶段训练。

**局限**（需人工验证的标注偏差风险除外）：
- **规模有限**：基准仅包含2405个样本，可能不足以覆盖所有自我中心场景的多样性。
- **数据来源单一**：仅基于EgoExo4D和ADT两个数据集，场景类型（主要是人类日常活动和运动技能）受限。
- **评估粒度**：动作链任务的严格关系准确率（Rel-Acc-S）可能过于苛刻，尽管已引入宽松版本（Rel-Acc-L），但离散化的空间关系表示仍可能丢失部分细粒度信息。
- **域迁移验证不足**：跨数据集调优实验（EgoExo4D→ADT）仅验证了利用任务，对其他认知层次的域迁移效果尚不明确。

### 开放问题

1. **隐式空间知识的检索瓶颈**：现有MLLMs在预训练数据中已编码大量隐式空间知识，但缺乏结构化的监督信号来有效检索和利用这些知识。性能受限究竟是因为空间智能的缺失，还是检索机制的不足？指令调优的显著提升（意图调优使利用任务准确率+26.30%）暗示后者，但需要更直接的证据。

2. **认知层次的泛化性**：意图、探索、利用、动作链这一层次结构是否可推广至其他具身AI任务（如机器人操作、导航）？在EgoProx中观察到的正向迁移现象是否在物理交互场景中同样成立？

3. **长程动作链推理的根本性改进**：最佳MLLM（Gemini-2.5-Pro）在动作链任务上的动作准确率（Act-Acc）仅为25.14%，与人类水平（80.23%）差距达-55.09%。指令调优的改善有限（探索调优仅将Act-Acc从5.98提升至7.61），表明需要更根本的架构创新，如显式融入3D空间表征或记忆机制。

4. **数据引擎的扩展性**：如何将基于代理的数据引擎扩展到更广泛的自我中心视频数据集（如Ego4D的日常活动场景），以增强基准的多样性和覆盖度？这要求目标数据集具备足够的3D标注，而这类标注的获取本身就是一个瓶颈。

5. **评估指标的改进空间**：当前对空间关系的离散化处理（8个方向）和近似距离的区间化虽然提高了可解释性，但可能掩盖模型在连续空间推理中的细微差异。是否需要更细粒度的评估方案？



## 原文 PDF

![[paperPDFs/CVPR_2026/EgoProx_Evaluating_MLLMs_on_Egocentric_3D_Proximity_Reasoning_Across_a_Cognitive_Hierarchy.pdf]]
