---
title: "AwareVLN: Reasoning with Self-awareness for Vision-Language Navigation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/AwareVLN_Reasoning_with_Self_awareness_for_Vision_Language_Navigation.pdf
project_link: "https://gwxuan.github.io/AwareVLN/"
code_link: null
aliases:
- AwareVLN
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 在导航关键节点（子任务完成、路径偏离、停止错误）触发稀疏的结构化自我推理，使智能体能够显式分析场景、评估进度并规划下一步，从而赋予其自我意识。
primary_logic: 通过统一视觉语言模型融合自我感知推理与动作预测，利用结构化推理格式（场景描述、进度评估、下一步计划）在关键节点自主决定推理时机，使智能体具备明确的导航自我意识，从而在保持计算效率的同时大幅提升导航鲁棒性和可解释性。
claims:
- AwareVLN在R2R-CE Val-Unseen上仅使用单目RGB输入即取得SR 65.4、SPL 55.1，显著超过所有不依赖仿真预训练路径点预测器的方法（Table 1）。
- 在RxR-CE Val-Unseen上，AwareVLN达到SR 67.6、SPL 56.1，远超同期VLM基线NaVILA的SR 49.3（Table 1）。
- 消融实验表明，移除子任务完成推理节点导致性能下降最严重（R2R-CE SR从65.4降至52.3），验证了结构化自我意识推理的必要性（Table 3）。
- R2R-CE Val-Unseen 上 SR↑ = 65.4
---

# AwareVLN: Reasoning with Self-awareness for Vision-Language Navigation

> [!tip] 核心洞察
> 通过统一视觉语言模型融合自我感知推理与动作预测，利用结构化推理格式（场景描述、进度评估、下一步计划）在关键节点自主决定推理时机，使智能体具备明确的导航自我意识，从而在保持计算效率的同时大幅提升导航鲁棒性和可解释性。

| 字段 | 内容 |
|------|------|
| 中文题名 | AwareVLN：基于自我意识推理的视觉语言导航 |
| 英文题名 | AwareVLN: Reasoning with Self-awareness for Vision-Language Navigation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.22816) · [Project](https://gwxuan.github.io/AwareVLN/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | AwareVLN |
| Dataset | R2R-CE Val-Unseen, RxR-CE Val-Unseen |

> [!tip] 效果简介
> - R2R-CE Val-Unseen 上，SR↑ 65.4 vs 54.0 (NaVILA) (+11.4)；SPL↑ 55.1 vs 49.0 (NaVILA) (+6.1)。
> - RxR-CE Val-Unseen 上，SR↑ 67.6 vs 49.3 (NaVILA) (+18.3)；SPL↑ 56.1 vs 44.0 (NaVILA) (+12.1)。
> - RxR-CE Val-Unseen (cross-dataset) 上，SR↑ 39.8 vs 34.3 (NaVILA) (+5.5)。

## 概述

现有视觉语言导航（VLN）方法主要采用端到端动作预测范式，缺乏对智能体自身状态和任务进展的显式认知。这种“无意识”的导航策略导致两个核心问题：其一，导航过程不可解释，无法追溯决策依据；其二，缺乏鲁棒性，难以应对子任务划分、路径偏离和错误纠正等复杂场景。**AwareVLN** 针对这一瓶颈，提出在导航关键节点触发稀疏的结构化自我推理，使智能体能够显式分析场景、评估进度并规划下一步，从而赋予其导航自我意识。

该工作的核心洞察在于：通过统一视觉语言模型融合自我感知推理与动作预测，利用结构化推理格式（场景描述、进度评估、下一步计划）在关键节点自主决定推理时机，使智能体在保持计算效率的同时大幅提升导航鲁棒性和可解释性。具体而言，AwareVLN 在子任务完成、路径偏离和停止错误三类关键事件触发推理，由模型自主通过特殊令牌 [REASON] / [ACT] 决定进入推理模式或动作模式。

在方法谱系中，AwareVLN 区别于 NaVILA、NaVid 等仅依赖端到端动作预测的 VLM 导航方法，也不同于 ETPNav* 等需要仿真预训练路径点预测器并依赖全景、里程计等额外传感器的方法。AwareVLN 仅使用单目 RGB 输入，在不依赖路径点预测器的方法中取得领先性能。

主要实验结果验证了该范式的有效性：在 R2R-CE Val-Unseen 上，AwareVLN 取得 SR 65.4、SPL 55.1，显著超过 NaVILA 的 SR 54.0（Table 1）；在 RxR-CE Val-Unseen 上，SR 达 67.6，远超 NaVILA 的 49.3。消融实验进一步揭示，移除子任务完成推理节点导致 SR 从 65.4 骤降至 52.3，验证了结构化自我意识推理的必要性（Table 3）。

## 背景与动机

视觉语言导航（Vision-Language Navigation, VLN）要求智能体在连续环境中根据自然语言指令完成导航任务。近年来，随着视觉语言模型（VLM）的快速发展，端到端VLN方法取得了显著进展，代表性工作包括**NaVILA**、**NaVid**和**Uni-NaVid**等。这些方法将导航建模为从视觉观测到动作指令的直接映射，绕过了传统方法对仿真预训练路径点预测器（waypoint predictor）的依赖，展现出良好的泛化潜力。

然而，现有基于VLM的VLN方法存在一个核心瓶颈：**缺乏对智能体自身状态和任务进展的显式自我感知**。具体而言，端到端动作预测范式使智能体在导航过程中无法回答以下关键问题：当前场景与指令的关系是什么？任务进展到哪一步？是否存在路径偏离？这种“黑箱”式决策导致三个突出问题：

1. **不可解释性**：智能体无法说明其决策依据，难以理解为何选择特定动作。
2. **鲁棒性不足**：当遭遇歧义指令或复杂场景时，缺乏自我纠错能力，错误会持续累积。
3. **子任务划分困难**：长指令通常包含多个子目标，端到端方法难以在子任务边界进行结构化规划。

针对上述问题，AwareVLN提出了一个根本性的思路转变：**赋予智能体导航自我意识（self-awareness）**。其核心动机是——如果智能体能够在导航关键节点（如子任务完成、路径偏离、停止错误）主动触发结构化推理，显式分析场景、评估进度并规划下一步，就能在保持端到端效率的同时，大幅提升导航的鲁棒性和可解释性。这一动机在Figure 1中得到了直观展示：AwareVLN在关键导航点选择性触发自我感知推理，而非全程依赖端到端动作预测。

实现这一目标面临两个关键挑战：一是如何设计推理机制使其仅在必要时触发，避免密集推理带来的计算开销；二是如何获取高质量的结构化推理监督信号，因为人工标注成本高昂且难以规模化。AwareVLN分别通过**稀疏推理调度机制**和**自动数据引擎**解决了这两个挑战，为视觉语言导航中的自我意识推理开辟了新路径。

## 核心创新

AwareVLN 的核心创新在于将**稀疏的结构化自我感知推理**显式注入视觉语言导航（VLN）智能体的决策循环中，使其从“端到端黑盒动作预测”跃迁为“可解释、可纠错的自我意识导航”。这一转变通过三个相互耦合的 changed slots 实现。

### 从无推理到关键节点触发的稀疏推理

现有基于 VLM 的 VLN 方法（如 **NaVILA**、**NaVid**）直接以指令和视觉观测为条件预测导航动作，缺乏对智能体自身状态和任务进展的显式建模。AwareVLN 的**推理机制**将这一范式替换为：在导航关键节点（子任务完成、路径偏离、停止错误）触发稀疏的结构化推理，而在常规行进中仅执行轻量动作预测（Section 3.2, Algorithm 1）。

具体而言，统一策略在每个时间步输出两个特殊令牌的 logit——`[REASON]` 和 `[ACT]`——并根据其大小自主决定进入推理模式还是动作模式（Eq. 3）。推理模式生成三元组结构化文本：**场景描述**→**进度评估**→**下一步计划**（Figure 2b），该文本经时空融合（Eq. 1，融入自上次推理以来的相对步数距离）后反馈至后续决策，形成因果闭环。消融实验（Table 4）证实了这一设计的必要性：取消特殊令牌、强制直接预测动作或推理导致 R2R-CE SR 从 65.4 降至 62.5；每帧密集推理不仅性能更低（SR 63.8），且计算开销更大。

### 从无监督到自动化推理标注生成

传统 VLN 训练数据仅包含导航轨迹和动作标签，缺乏推理监督信号。AwareVLN 的**训练数据生成**通过自动数据引擎（Section 3.3, Figure 3）填补了这一空白：利用仿真环境中的房间级语义和真值路径点自动识别三类关键推理节点，提取富多模态上下文（指令片段、RGB 观测序列、空间关系），并调用通用 VLM 生成结构化推理标注。这一管线实现了零人工标注的可扩展高质量推理数据构建。

### 推理调度的稀疏化与自主化

与无推理或每帧密集推理的基线不同，AwareVLN 的**推理调度**由模型自主决定，仅在关键节点触发（Table 4 中 “w/ special tokens” 即代表这一稀疏调度）。消融实验进一步揭示了不同推理节点的重要性梯度（Table 3）：移除子任务完成推理节点导致性能崩塌最严重（R2R-CE SR 从 65.4 降至 52.3），移除路径偏离推理节点降至 55.1，移除停止误差推理节点降至 60.0。这表明**自我意识的三个维度存在因果层级**——对任务进度的宏观感知是导航鲁棒性的根基，而对局部错误的识别与纠正则在此基础上提供精细调控。

综合来看，AwareVLN 通过“何时推理”“推理什么”“如何获取推理监督”三个维度的协同创新，在不依赖仿真预训练路径点预测器、仅使用单目 RGB 输入的约束下，实现了 R2R-CE Val-Unseen SR 65.4、SPL 55.1，以及 RxR-CE Val-Unseen SR 67.6、SPL 56.1 的领先性能（Table 1），同时赋予了导航过程可解释性和错误自纠正能力（Figure 4）。

## 整体框架

AwareVLN 的核心设计是将**自我感知的结构化推理**嵌入到统一的视觉语言导航模型中，使智能体不再仅仅依赖端到端的动作预测，而是能够在导航的关键节点自主触发推理，显式分析自身状态与任务进展。

### 框架总览

整个 pipeline 由四个主要模块构成，形成“感知—推理—决策”的闭环（Figure 2）：

![[assets/figures/papers/paper_list_l2373_https_arxiv_org_abs_2605_22816/figures/002_Figure_2.jpg]]
*Figure 2: Framework of AwareVLN. (a) AwareVLN equips a unified vision-language model with both action prediction and self-reflective reasoning, allowing the agent to leverage past reasoning to guide future decisions. (b) The reasoning process is multi-dimensional and causal, sequentially describing the current scene, assessing progress, and planning the next step.(c) As illustrated by the BEV monitor, reasoning is sparsely and structurally triggered at key nodes, such as subtask boundaries*

1. **视觉编码器**：从单目 RGB 观测流 `O_t` 中提取视觉特征，作为环境感知的基础。
2. **文本令牌化与时空融合**：将导航指令 `T` 和历史推理文本 `R` 进行令牌化，并通过公式 `R' = R ⊕ (t - t_prev)` 将推理文本与自上次推理以来的相对步数距离融合，为模型提供时序上下文（Eq. 1）。
3. **统一推理-动作决策模块**：这是 AwareVLN 的核心。模型基于融合后的指令、历史推理和当前视觉观测，通过统一策略 `π_θ` 同时输出一个决策 logit `d` 和文本输出 `y_t`（Eq. 2）。决策 logit 在特殊令牌 `[REASON]` 和 `[ACT]` 之间进行比较，自主决定当前帧进入推理模式还是动作模式（Eq. 3, Algorithm 1）。
4. **自动数据引擎**：在训练阶段，利用仿真环境中的房间级语义和真值路径点自动识别关键推理节点（子任务完成、路径偏离、停止误差），并调用通用 VLM 生成结构化的推理监督信号（Figure 3），从而无需人工标注即可规模化构建高质量训练数据。

### 推理的触发与格式

推理并非每帧执行，而是**稀疏地**在关键导航节点触发。具体而言，模型在以下三类关键状态自主进入推理模式：

- **子任务完成**：当智能体完成指令中的一个子目标（如“进入厨房”）时，触发推理以评估进度并规划下一步。
- **路径偏离**：当智能体的行进方向与指令描述不一致时，触发推理以识别偏差并生成纠正计划。
- **停止误差**：当智能体过早或错误地发出停止动作时，触发推理以重新定位目标。

每次推理均遵循**三元组结构化格式**（Figure 2b）：
1. **场景描述**：描述当前观测到的环境。
2. **进度评估**：评估相对于指令的任务完成进度。
3. **下一步计划**：规划接下来的导航动作。

这种结构化推理使智能体具备了因果性的自我意识：先理解场景，再评估进度，最后制定计划，从而赋予导航过程更强的可解释性和鲁棒性。

### 输入输出流

- **输入**：单目 RGB 图像序列 + 自然语言导航指令。
- **输出**：在动作模式下输出具体的导航动作指令；在推理模式下输出结构化推理文本，该文本随后被反馈到上下文中以指导后续决策。
- **推理调度**：由模型自主通过 `[REASON]` / `[ACT]` 令牌的 logit 比较决定，无需外部调度器。

> **注意**：AwareVLN 仅使用单目 RGB 输入，而部分对比方法使用了全景 RGB、深度或里程计等额外传感器。即便如此，AwareVLN 在所有不依赖仿真预训练路径点预测器的方法中仍取得领先性能（Table 1）。

### 补充图表

![[assets/figures/papers/paper_list_l2373_https_arxiv_org_abs_2605_22816/figures/001_Figure_1.jpg]]
*Figure 1: AwareVLN equips a VLN agent with self-aware, structured reasoning that is selectively triggered at key navigation points. Instead of relying solely on end-to-end action prediction, AwareVLN enables the agent to explicitly analyze its spatial state, task progress, and alignment with the instruction when such reasoning is truly needed, achieving more robust and explainable instruction following*

## 核心模块与公式推导

### 问题形式化

AwareVLN 将视觉语言导航定义为一个序列决策问题。给定一条由 $l$ 个词组成的自然语言指令 $\mathcal{T} = \{w_1, \ldots, w_l\}$，智能体在时间步 $t$ 接收以自我为中心的单目 RGB 观测流 $\mathcal{O}_t = \{\mathbf{x}_0, \ldots, \mathbf{x}_t\}$，并输出导航动作。与传统端到端动作预测不同，AwareVLN 在关键导航节点额外引入结构化自我推理，使智能体能够显式分析场景、评估任务进展并规划下一步。

### 统一推理-动作决策模块

AwareVLN 的核心是一个统一的视觉语言模型，将动作预测与自我反思推理融合在同一框架内。该模块包含三个关键子组件：

**视觉编码器** ($f_{\text{vis}}$)：从当前 RGB 观测 $\mathcal{O}_t$ 中提取视觉特征，为后续推理和决策提供场景理解基础。

**文本令牌化与时空融合**：指令 $\mathcal{T}$ 被令牌化为 $\mathbb{Z}$。推理文本 $\mathcal{R}$ 在融合前需注入时序上下文——将自上次推理以来的相对步数距离 $(t - t_{\text{prev}})$ 拼接到推理表示中：

$$\mathcal{R}' = \mathcal{R} \oplus (t - t_{\text{prev}}) \tag{1}$$

这一设计使模型能够感知推理的时间间隔，从而区分“刚完成子任务”与“已行进多步后重新评估”等不同情境。

**统一策略输出**：模型接收指令令牌、融合推理令牌和视觉特征，同时输出模式决策 logit 和文本内容：

$$d, y_t = \pi_{\theta} \left( f_{\text{tok}}(\mathbb{Z}), f_{\text{tok}}(\mathcal{R}'), f_{\text{vis}}(\mathcal{O}_t) \right) \tag{2}$$

其中 $d$ 为 $[\text{REASON}]$ 和 $[\text{ACT}]$ 两个特殊令牌的 logit 向量，$y_t$ 为生成的文本输出。

### 稀疏推理调度机制

AwareVLN 的关键创新在于自主决定何时触发推理，而非每帧密集推理或完全不做推理。模式决策遵循以下规则：

$$\mathcal{D} = \begin{cases} [\text{REASON}], & \text{if } d_{[\text{REASON}]} > d_{[\text{ACT}]}, \\ [\text{ACT}], & \text{otherwise}. \end{cases} \tag{3}$$

当模型判定当前状态需要推理时（$d_{[\text{REASON}]} > d_{[\text{ACT}]}$），进入推理模式，生成结构化的三元组推理文本：**场景描述**（当前观测到的空间布局和物体）、**进度评估**（已完成哪些子任务、与指令的对齐程度）、**下一步计划**（需要前往的区域或需要执行的纠正动作）。否则进入动作模式，直接输出导航动作指令。

推理仅在三种关键节点被触发：**子任务完成**（如进入指令指定的房间）、**路径偏离**（智能体行进方向与指令不符）、**停止误差**（过早或过晚发出停止指令）。消融实验（Table 3）验证了这一稀疏调度的重要性：每帧密集推理不仅计算开销更大，且 SR 从 65.4 降至 63.8；而完全移除特殊令牌、强制模型直接预测动作或推理，SR 降至 62.5。

### 自动数据引擎

为生成结构化推理的监督信号，AwareVLN 设计了一个无需人工标注的自动数据引擎。该引擎利用仿真环境中的房间级语义和真值路径点自动识别三种关键推理节点，并提取每个节点的多模态上下文（包括当前观测、历史轨迹、指令片段），调用通用 VLM 生成结构化的因果推理标注。这一流水线使得大规模、高质量的推理数据构建成为可能，支撑了模型自我意识能力的训练。

### 补充图表

![[assets/figures/papers/paper_list_l2373_https_arxiv_org_abs_2605_22816/figures/003_Figure_3.jpg]]
*Figure 3: Automatic Data Engine. Key reasoning nodes are automatically identified using room-level semantics and ground-truth waypoints in the simulator, covering key events including subtask completion, path deviation, and incorrect stopping. For each key node, rich multimodal context is extracted and fed into a general VLM to automatically generate structured, causal reasoning supervision. This pipeline enables scalable, annotation-free construction of high-quality reasoning data*

![[assets/figures/papers/paper_list_l2373_https_arxiv_org_abs_2605_22816/figures/010_Figure_6.jpg]]
*Figure 6: Example of our multi-turn reasoning supervision process (Part 1): global understanding of the navigation episode and reasoning for subtask completion based on localized observations*

![[assets/figures/papers/paper_list_l2373_https_arxiv_org_abs_2605_22816/figures/011_Figure_7.jpg]]
*Figure 7: Example of our multi-turn reasoning supervision process (Part 2): reasoning for subsequent node types, including path deviation and stopping error, demonstrating error interpretation and recovery planning*

## 实验与分析

### 核心性能对比

AwareVLN在仅使用单目RGB输入的设定下，在R2R-CE和RxR-CE两个标准VLN基准上均取得了领先性能。在R2R-CE Val-Unseen上，AwareVLN达到**SR 65.4、SPL 55.1**，比同期VLM基线**NaVILA**（SR 54.0、SPL 49.0）分别提升11.4和6.1个百分点。在更具挑战性的RxR-CE Val-Unseen上，优势更为显著——AwareVLN取得**SR 67.6、SPL 56.1**，远超NaVILA的SR 49.3和SPL 44.0，SR提升达18.3个百分点。

需要特别指出公平比较的边界：AwareVLN不使用仿真预训练的路径点预测器（waypoint predictor），而部分对比方法（如**ETPNav\***）依赖该预测器并使用了全景RGB、深度和里程计等额外传感器。在所有不依赖路径点预测器的方法中，AwareVLN表现最佳；即便与使用全景RGB+里程计的**Uni-NaVid**相比，AwareVLN仅凭单目RGB也取得了更高的SR（65.4 vs. 62.0）。

### 消融实验：结构化自我意识推理的必要性

消融实验系统性地验证了三类关键推理节点各自对导航性能的因果贡献。完整模型在R2R-CE上SR为65.4，移除各类推理节点后性能均有显著下降：

- **移除子任务完成推理节点**（w/o Subtask Completion）：SR骤降至52.3，降幅达13.1个百分点，为影响最大的消融项。这表明对导航进度的显式评估是自我意识的核心——智能体需要知道“已完成什么、还需做什么”才能做出正确的后续决策。
- **移除路径偏离推理节点**（w/o Path Deviation）：SR降至55.1。该节点赋予智能体识别自身错误的能力——当实际路径偏离指令意图时，通过比较观测与指令进行纠错，是导航鲁棒性的关键保障。
- **移除停止误差推理节点**（w/o Stopping Error）：SR降至60.0。该节点影响目标定位精度，缺失时智能体可能在接近目标时过早或过晚停止。

### 消融实验：推理调度与输出结构

推理调度策略和输出格式同样对性能有显著影响：

- **取消特殊令牌**（w/o special tokens，即强制模型直接预测动作或推理）：SR从65.4降至62.5。这表明通过[REASON]和[ACT]特殊令牌显式分解推理与动作两种模式，比让模型隐式切换更为有效。
- **每帧密集推理**（Reason with action densely）：SR降至63.8，且计算开销更大。这验证了稀疏推理调度（仅在关键节点触发推理）的优越性——密集推理不仅增加计算负担，还可能引入噪声干扰决策。

### 跨数据集泛化

在未经RxR-CE训练的情况下，AwareVLN在RxR-CE Val-Unseen上取得**SR 39.8**，优于NaVILA的34.3。该结果（Table 5）表明结构化自我感知推理具有一定的跨数据集迁移能力，推理模式本身不过度拟合单一数据分布。

![[assets/figures/papers/paper_list_l2373_https_arxiv_org_abs_2605_22816/figures/012_Table_5.jpg]]
*Table 5: Cross-dataset performance on the RxR-CE Val-Unseen split. All results are obtained without training on RxR-CE*

### 真实世界部署验证

AwareVLN在仅使用仿真数据训练的条件下，被部署到四足机器人上完成真实世界的长程VLN任务（Table 2, Figure 5）。这验证了方法的sim-to-real迁移潜力。但由于仅依赖单目RGB，3D感知能力不足，真实部署中仍存在碰撞风险和停止位置偏离目标的问题，这是当前方法的一个明确局限。

![[assets/figures/papers/paper_list_l2373_https_arxiv_org_abs_2605_22816/figures/005_Table_2.jpg]]
*Table 2: Real-world evaluation across three environments*

### 推理效率

推理阶段使用单张NVIDIA RTX 4090 GPU，速度约为1 FPS。考虑到该方法在关键节点才触发结构化推理、其余帧仅执行轻量动作预测，这一速度在VLM导航方法中处于可接受范围，且性能收益远超计算开销。

### 失败模式分析

结合消融实验和定性案例（Figure 4），AwareVLN的主要失败模式可归纳为：

![[assets/figures/papers/paper_list_l2373_https_arxiv_org_abs_2605_22816/figures/009_Figure_4.jpg]]
*Figure 4: Rollout in Habitat simulator. AwareVLN performs self-aware reasoning during navigation. As shown in the left part, the agent mistakenly interprets the instruction’s “turn right”. By comparing observations with the instruction, the agent identifies the deviation, and generates a corrective plan. As shown in the right part, after successfully entering the kitchen, AwareVLN recognizes that a subtask has been completed and accurately assesses the navigation progress, producing an appropriate next-step plan aligned with the instruction*

1. **子任务边界误判**：当场景语义模糊或指令描述不精确时，智能体可能无法正确识别子任务完成节点，导致进度评估错误，进而做出与指令不一致的后续规划。
2. **路径偏离检测滞后**：路径偏离推理依赖当前观测与指令的比对，当偏离发生在视觉相似区域时，检测可能延迟，纠错动作的时效性不足。
3. **单目3D感知局限**：在真实世界中，缺乏深度信息导致停止位置不够精确，且障碍物感知不足可能引发碰撞。这是仅使用单目RGB的固有限制，需要进一步研究增强3D感知能力。

### 补充图表

![[assets/figures/papers/paper_list_l2373_https_arxiv_org_abs_2605_22816/figures/004_Table_1.jpg]]
*Table 1: Comparison with state-of-the-art methods on the Val-Unseen split of R2R-CE [24] and RxR-CE [26]. ∗ indicates methods using the waypoint predictor from Hong et al. [19]. AwareVLN outperforms all methods that do not rely on simulator pre-trained waypoint predictors, even when those methods leverage additional inputs such as depth, panoramic views, and odometry*

![[assets/figures/papers/paper_list_l2373_https_arxiv_org_abs_2605_22816/figures/006_Table_3.jpg]]
*Table 3: Ablation study of different key reasoning nodes defined in automatic data engine on R2R-CE and RxR-CE Val-Unseen splits*

![[assets/figures/papers/paper_list_l2373_https_arxiv_org_abs_2605_22816/figures/007_Table_4.jpg]]
*Table 4: Comparison of performance with and without special tokens on R2R-CE and RxR-CE Val-Unseen splits*

![[assets/figures/papers/paper_list_l2373_https_arxiv_org_abs_2605_22816/figures/015_Figure_8.jpg]]
*Figure 8: Example 1 of an automatically collected training trajectory, illustrating three key nodes: path deviation, correction completion, and subtask completion. The agent interprets the evolving visual scene and progressively generates structured reasoning outputs aligned with the navigation instruction*

## 方法谱系与知识库定位

### 1. 在视觉语言导航（VLN）方法谱系中的位置

AwareVLN 处于**基于视觉语言模型（VLM）的端到端导航**与**结构化推理增强**两条技术路线的交汇点。为理解其定位，需先梳理 VLN 领域的方法演进脉络。

**经典 VLN 范式：路径点预测器依赖。** 早期 VLN 方法普遍采用“路径点预测器 + 导航策略”的分离式架构。路径点预测器利用仿真环境中的全景图、深度图和里程计信息，通过大规模预训练学习预测候选路径点；导航策略则从候选路径点中选择下一步目标。代表性工作如 **ETPNav**（带 `*` 标记的方法，Table 1，依赖 Hong et al. 的路径点预测器）在 R2R-CE Val-Unseen 上可达到 SR 70.4、SPL 58.9 的领先性能。然而，这类方法对仿真预训练的路径点预测器存在强依赖，限制了其在真实场景中的泛化能力。

**VLM 驱动的端到端导航：摆脱路径点依赖。** 近年来，以 **NaVILA**、**NaVid** 和 **Uni-NaVid** 为代表的方法尝试利用预训练视觉语言模型直接输出导航动作，从而摆脱对路径点预测器的依赖。NaVILA 在 R2R-CE Val-Unseen 上取得 SR 54.0、SPL 49.0；NaVid 和 Uni-NaVid 分别达到 SR 51.5 和 52.6。这些方法虽然消除了路径点预测器的束缚，但普遍缺乏对智能体自身状态和任务进展的显式建模，导航过程表现为“黑箱”式的端到端动作映射，可解释性和鲁棒性不足。

**AwareVLN 的突破：结构化自我意识推理。** AwareVLN 在 VLM 端到端导航的基础上引入**稀疏结构化自我推理机制**，使智能体能够在关键导航节点（子任务完成、路径偏离、停止错误）自主触发推理，显式分析场景、评估进度并规划下一步。这一设计使 AwareVLN 在仅使用单目 RGB 输入的条件下，于 R2R-CE Val-Unseen 取得 SR 65.4、SPL 55.1，显著超越所有不依赖路径点预测器的方法（Table 1）。在更具挑战性的 RxR-CE Val-Unseen 上，AwareVLN 的 SR 67.6 更是远超 NaVILA 的 SR 49.3，提升幅度达 +18.3 个百分点。

### 2. 关键技术决策与 baseline 的本质差异

AwareVLN 与现有 VLM 导航方法的核心差异体现在三个关键设计维度：

| 设计维度 | 现有 VLM 方法（NaVILA 等） | AwareVLN |
|---------|--------------------------|----------|
| **推理机制** | 无显式推理，仅端到端动作预测 | 在关键节点触发稀疏结构化推理（`[REASON]`/`[ACT]` 特殊令牌决定模式切换） |
| **训练监督** | 仅使用导航轨迹数据，无推理监督信号 | 通过自动数据引擎利用仿真语义和通用 VLM 生成结构化推理标注 |
| **推理调度** | 无推理或每帧密集推理 | 模型自主决定稀疏推理时机（仅在关键节点推理） |

**推理机制的差异。** NaVILA 等方法的输出空间仅包含导航动作，智能体缺乏对“为何选择该动作”的显式建模。AwareVLN 将输出空间扩展为推理与动作的联合空间：模型在每个时间步输出一个决策 logit $d$，通过比较 $d_{[\text{REASON}]}$ 和 $d_{[\text{ACT}]}$ 的大小自主决定进入推理模式或动作模式（Eq. (3)）。推理模式下，模型生成结构化的三元组推理文本——场景描述、进度评估、下一步计划；动作模式下，模型直接输出导航动作指令。

**训练监督的差异。** 现有方法仅利用导航轨迹中的动作序列作为监督信号。AwareVLN 设计了自动数据引擎（Figure 3），利用仿真环境中的房间级语义标签和真值路径点自动识别三类关键推理节点——子任务完成、路径偏离、停止错误——并为每个节点提取丰富的多模态上下文，调用通用 VLM 自动生成结构化推理标注。这一流水线实现了零人工标注的高质量推理数据规模化构建。

**推理调度的差异。** 消融实验（Table 4）揭示了调度策略的关键影响：若取消特殊令牌、强制模型直接预测动作或推理，SR 从 65.4 降至 62.5；若改为每帧密集推理，SR 进一步降至 63.8，且计算开销更大。这表明**稀疏且自主的推理调度**是 AwareVLN 在效率和性能之间取得最优平衡的核心设计。

### 3. 适用边界与局限性

**传感器约束下的性能边界。** AwareVLN 仅依赖单目 RGB 流输入，这一设计简化了部署要求，但也构成了其性能上限的硬约束。Table 1 显示，使用全景 RGB-D 和里程计的 ETPNav* 在 R2R-CE 上仍以 SR 70.4 领先于 AwareVLN 的 SR 65.4。这表明在仿真环境中，多传感器融合带来的 3D 感知优势尚无法被纯单目推理完全弥补。

**真实环境部署的挑战。** 论文在真实世界四足机器人上验证了 AwareVLN 的迁移能力（Figure 5，Table 2），但也明确指出两个关键局限：（1）由于仅依赖单目 RGB，3D 感知能力不足，可能导致碰撞或停止位置偏离目标；（2）训练数据由仿真环境自动生成，视觉域差异可能限制某些真实场景的泛化性能。Table 5 的跨数据集实验（R2R-CE 训练、RxR-CE 测试）显示 SR 39.8，虽优于 NaVILA 的 34.3，但绝对性能仍有较大提升空间。

**推理覆盖的边界。** 消融实验（Table 3）揭示了不同推理节点的重要性梯度：移除子任务完成推理节点导致 SR 从 65.4 骤降至 52.3（-13.1），为最关键成分；移除路径偏离推理节点降至 55.1（-10.3）；移除停止误差推理节点降至 60.0（-5.4）。这表明 AwareVLN 的性能高度依赖对关键导航事件的覆盖完整性——若自动数据引擎未能识别某类关键节点，模型在该场景下的自我意识将出现盲区。

### 4. 开放问题与未来方向

**如何增强单目 RGB 的 3D 感知能力？** AwareVLN 在真实世界中面临的碰撞和停止误差问题，根源在于单目 RGB 缺乏显式深度信息。一个值得探索的方向是将单目深度估计或神经辐射场（NeRF）等隐式 3D 表征融入自我推理过程，使智能体在推理时能够更准确地评估空间关系和障碍物分布。

**如何将结构化自我感知推理扩展到更复杂的指令场景？** 当前 AwareVLN 在 R2R-CE 和 RxR-CE 上的验证集中于单条指令的室内导航。将这一范式扩展到更长期、多语言指令、甚至需要常识推理的导航任务中，需要自动数据引擎能够识别更丰富多样的关键推理节点类型，并生成相应的高质量推理监督。

**推理与动作的更深层耦合。** 当前 AwareVLN 的推理与动作是时序上的交替关系（先推理、后动作）。一个更激进的设计方向是让推理直接参与动作空间的约束或重排序——例如，推理模块识别出路径偏离后，直接修改动作候选集的概率分布——从而实现推理与决策的更紧密耦合。

## 原文 PDF

![[paperPDFs/CVPR_2026/AwareVLN_Reasoning_with_Self_awareness_for_Vision_Language_Navigation.pdf]]
