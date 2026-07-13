---
title: "ScaleCUA: Scaling Open-Source Computer Use Agents with Cross-Platform Data"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ScaleCUA_Scaling_Open_Source_Computer_Use_Agents_with_Cross_Platform_Data.pdf
project_link: null
code_link: https://github.com/OpenGVLab/ScaleCUA
openreview_forum_id: yBFUqdJFZn
aliases:
- ScaleCUA
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "设计并实现了一个跨平台交互数据管道，结合规则驱动的自动化探索与人类专家监督，生成涵盖六个操作系统和三个任务领域的大规模训练数据集，从而赋予模型强大的跨平台理解和操作能力。"
primary_logic: "通过数据驱动的缩放，可以显著提升开源视觉语言模型在计算机使用任务上的性能，使其在多个基准上达到或超越闭源模型；统一的动作空间和灵活的三种推理模式（定位、直接动作、推理动作）使单一模型能够高效整合感知、推理和动作，为通用计算机使用智能体提供了坚实的基础。"
claims:
- "ScaleCUA在WebArena-Lite-v2（50步）上取得了47.4%的成功率，比最强开源基线UI-TARS-72B-DPO（21.4%）提升26.0个百分点。"
- "在MMBench-GUI L1-Hard上，ScaleCUA-32B取得94.4%的准确率，远超原始Qwen2.5-VL-72B的64.6%。"
- "数据增强策略在ScreenSpot-Pro上带来3.5个百分点的绝对性能提升（37.8→41.3）。"
- "使用弱语义轨迹训练可显著改善任务完成性能，例如OSWorld成功率从7.6提高到8.5，WAL-v2从8.4提高到14.3。"
---

# ScaleCUA: Scaling Open-Source Computer Use Agents with Cross-Platform Data

> [!tip] 核心洞察
> 通过数据驱动的缩放，可以显著提升开源视觉语言模型在计算机使用任务上的性能，使其在多个基准上达到或超越闭源模型；统一的动作空间和灵活的三种推理模式（定位、直接动作、推理动作）使单一模型能够高效整合感知、推理和动作，为通用计算机使用智能体提供了坚实的基础。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ScaleCUA：利用跨平台数据扩展开源计算机使用智能体 |
| 英文题名 | ScaleCUA: Scaling Open-Source Computer Use Agents with Cross-Platform Data |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=yBFUqdJFZn) · [GitHub](https://github.com/OpenGVLab/ScaleCUA) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | ScaleCUA |
| Dataset | MMBench-GUI L1-Hard, WebArena-Lite-v2 (50 steps), ScreenSpot-Pro |

> [!tip] 效果简介
> - MMBench-GUI L1-Hard 上，Accuracy 为 94.4 (ScaleCUA-32B)，对比 64.6 (Qwen2.5-VL-72B)，变化 +29.8。
> - WebArena-Lite-v2 (50 steps) 上，Success Rate 为 47.4 (ScaleCUA-32B)，对比 21.4 (UI-TARS-72B-DPO)，变化 +26.0。
> - ScreenSpot-Pro 上，Overall Accuracy 为 59.2 (ScaleCUA-32B)，对比 48.5 (previous SOTA without ScaleCUA)，变化 +10.7。

## 概要

当前计算机使用智能体（Computer Use Agent）面临的核心瓶颈在于**缺乏大规模、跨平台的交互轨迹数据**与高质量训练语料，导致模型在多样化的操作系统和应用场景中泛化能力不足。现有数据收集方案或依赖纯人工标注，成本高昂且难以规模化；或仅基于单一平台的自动化探索，覆盖面有限且容易过时。

针对这一问题，ScaleCUA 提出了一条**跨平台交互数据管道**，通过规则驱动的自动化代理与人类专家监督相结合的混合双环架构，系统性地采集并标注覆盖 Windows、Ubuntu、macOS、Web、Android、iOS 六大平台的 GUI 操作轨迹。基于这一数据基础，ScaleCUA 构建了一个统一的视觉语言智能体模型系列，将**感知、推理与动作**整合于单一模型之中，并支持三种灵活的推理范式——定位模式（Grounding Mode）、直接动作模式（Direct Action Mode）与推理动作模式（Reasoned Action Mode），以适应从快速响应到高可靠性决策的不同需求。

实验结果表明，ScaleCUA 通过数据驱动的缩放策略，在多个基准上实现了对闭源模型的超越或持平。具体而言：

- 在 **MMBench-GUI L1-Hard** 上，ScaleCUA-32B 取得 94.4% 的准确率，远超原始 Qwen2.5-VL-72B 的 64.6%（Table 2）。
- 在 **WebArena-Lite-v2**（50 步预算）上，ScaleCUA-32B 以 47.4% 的成功率显著优于最强开源基线 UI-TARS-72B-DPO 的 21.4%，提升达 26.0 个百分点（Table 3）。
- 在 **ScreenSpot-Pro** 定位基准上，ScaleCUA-32B 取得 59.2% 的整体准确率，较此前最佳结果提升 10.7 个百分点（Figure 1, Table 7）。

消融实验进一步揭示了数据策略的关键作用：数据增强为 ScreenSpot-Pro 带来 3.5 个百分点的绝对提升；弱语义轨迹训练使 OSWorld 和 WebArena-Lite-v2 的任务成功率分别从 7.6 提升至 8.5、从 8.4 提升至 14.3；原始坐标表示与更高训练分辨率的采用也均贡献了正向增益（Table 4）。

综上，ScaleCUA 的核心贡献在于证明了**通过大规模、跨平台的交互数据缩放，开源视觉语言模型能够在计算机使用任务上达到甚至超越闭源模型的性能水平**，为通用计算机使用智能体的发展提供了坚实的数据与方法基础。



计算机使用智能体（Computer Use Agent）旨在通过视觉感知图形用户界面（GUI），自主完成跨应用、跨平台的任务操作。近年来，闭源商业模型（如GPT-4o、Claude-3.7）在这一领域展现了强大的能力，但其训练数据和实现细节不透明，难以复现或定制。开源方案则面临根本性瓶颈：**缺乏大规模、跨平台的计算机使用操作轨迹数据和高质量训练语料**，严重限制了通用计算机使用智能体的泛化能力。

现有数据收集方法存在两类典型缺陷。其一，纯人工标注成本高昂，且任务覆盖面受限于标注者的知识范围，难以规模化。其二，纯自动化探索虽能快速生成数据，但产生的轨迹往往缺乏语义目标导向，质量参差不齐，容易过时。此外，现有数据集在平台覆盖上碎片化严重——多数工作仅聚焦单一操作系统（如Android或Web），缺乏对Windows、Ubuntu、macOS、iOS等多平台的统一支持，导致模型难以习得跨平台通用的GUI理解与操作能力。

从模型层面看，现有开源GUI智能体在感知、推理和动作之间缺乏深度整合。部分方法将定位（grounding）与动作执行分离为独立模块，增加了系统复杂度和延迟；另一些方法则采用单一推理模式，无法灵活适配不同任务场景对效率或可解释性的差异化需求。与此同时，动作空间通常为平台专属定义，进一步加剧了跨平台迁移的困难。

上述缺口构成了本文的核心动机：**能否通过构建一个跨平台交互数据管道，系统性地生成大规模、多模态训练数据，并在此基础上训练一个统一的视觉语言模型，使其同时具备感知、推理和动作能力？** 这一思路的核心假设是：数据驱动的缩放（scaling）能够显著提升开源模型在计算机使用任务上的性能，使其在多个基准上达到甚至超越闭源模型。



## 核心方法与创新机理

ScaleCUA的核心创新并非提出全新的模型架构，而是通过**系统性的数据工程与灵活的推理范式设计**，从根本上解决了开源计算机使用智能体泛化能力不足的瓶颈。其创新点可归纳为四个关键维度的“changed slots”：

### 1. 数据收集策略：从单一来源到混合双环管道

现有数据收集方法通常依赖单一来源——要么是纯人类标注，成本高昂且难以规模化；要么是纯自动化探索，覆盖面有限且质量不稳定。ScaleCUA提出了一个**混合双环数据管道**（Figure 2），将两者协同整合：

- **智能体-环境交互循环（Agent-Environment Interaction Loop）**：标准化了跨Windows、Ubuntu、macOS、Web、Android和iOS六大平台的观测获取与动作执行，使自动化代理能够进行规则驱动的探索。
- **智能体-人类混合数据采集循环（Agent-Human Hybrid Data Acquisition Loop）**：自动化代理采集的轨迹与人类专家创建的轨迹合并，且要求专家随机审核20%的自动化数据以保证质量。

这一设计的关键因果机制在于：自动化探索以低成本提供广度覆盖，人类监督以高成本确保深度质量，二者的结合使得最终语料库达到**471K GUI理解样本、超过17.1M定位标注和19K条轨迹（平均9步）**的规模（Table 1），远超现有数据集。

### 2. 动作空间定义：从平台碎片化到统一跨平台抽象

基线方法通常为不同平台设计专属、碎片化的动作空间，导致模型难以跨平台泛化。ScaleCUA定义了一个**统一的跨平台动作空间**（Table 14），将通用操作（如click、write）与平台专属动作（如移动端的long press、open app）整合为一个一致的接口。

这一设计使得单一模型能够无缝地在桌面、移动和Web环境之间切换，无需针对每个平台进行适配。消融实验表明，这种统一性对于跨平台任务的性能至关重要。

### 3. 推理范式：从单一模式到三种互补模式

传统智能体通常仅支持单一推理模式（如直接生成动作），限制了其在不同场景下的灵活性和可解释性。ScaleCUA创新性地支持**三种推理范式**（Figure 3）：

- **定位模式（Grounding Mode）**：专注于定位目标UI元素，适合与外部规划器集成。
- **直接动作模式（Direct Action Mode）**：直接生成可执行动作，实现快速感知-动作循环。
- **推理动作模式（Reasoned Action Mode）**：先产生思维链推理再输出动作，提高可靠性和可解释性。

实验证据（Figure 5b）表明，推理动作模式在所有基准上均优于直接动作模式，成功率提升幅度在**+1.4%至+8.2%**之间。这一设计的深层价值在于：它将感知、推理和动作统一于单一模型，使智能体能够根据任务复杂度自主选择最合适的推理策略。

### 4. 训练数据平衡：从固定比例到规模自适应

通用VLM训练通常不区分通用数据与GUI数据的比例，或采用固定比例。ScaleCUA发现，**通用数据与GUI数据的比例需要根据模型规模进行调整**：3B模型使用25%通用数据、7B使用50%、32B使用75%（Section 4.2）。消融实验（Figure 5d, Table 12）证实，增加通用数据比例会提高通用VLM基准分数，但会逐渐降低GUI基准性能。这一规模自适应的数据平衡策略，是ScaleCUA在不同规模下均保持GUI专业能力的关键。

### 证据强度总结

| 创新维度 | 关键证据 | 置信度 |
|---------|---------|--------|
| 混合双环数据管道 | 最终语料库规模（Table 1）；弱语义轨迹消融（Table 4b）：OSWorld 7.6→8.5，WAL-v2 8.4→14.3 | 高 |
| 统一跨平台动作空间 | 跨平台在线评估（Table 3）：单一模型同时覆盖桌面、移动、Web | 高 |
| 三种推理范式 | 推理动作模式一致优于直接动作模式（Figure 5b） | 高 |
| 规模自适应数据平衡 | 通用数据比例对GUI性能的负向影响（Figure 5d, Table 12） | 中高 |

需要注意的是，虽然数据增强策略（元素裁剪、合成分辨率缩放、推理提示丰富）在ScreenSpot-Pro上带来了**3.5个百分点的提升**（37.8→41.3，Table 4a），但这属于数据层面的优化技巧，而非架构级创新。ScaleCUA真正的壁垒在于**数据管道的系统设计**和**推理范式的灵活整合**，这两者共同构成了其超越闭源模型（如GPT-4o、Claude-3.7）和开源基线（如UI-TARS-72B-DPO）的基础。



![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_yBFUqdJFZn/figures/001_Figure_1.jpg]]
*Figure 1: Performance comparison. The top row showcases performance overview on GUI-centric benchmarks. The bottom row demonstrates the consistent improvements from our collected data*

ScaleCUA 的整体框架围绕三个核心设计展开：**跨平台交互数据管道**、**统一的动作空间**，以及**三种灵活的推理范式**。这些设计共同支撑起一个从数据采集到模型推理的完整闭环，使单一模型能够整合感知、推理与动作，在桌面、移动和 Web 等多个平台上执行计算机使用任务。

### 跨平台交互数据管道

数据是 ScaleCUA 能力的根基。如图 2 所示，数据管道由两个协同循环构成：

1. **智能体-环境交互循环（Agent-Environment Interaction Loop）**：标准化了跨 Windows、Ubuntu、macOS、Web 浏览器、Android 和 iOS 六大平台的观测获取与动作执行。每一时间步，智能体模型 $\pi_\theta$ 根据任务描述 $task$、当前观测 $o_t$ 和历史 $h_{<t}$ 生成动作 $a_t$，环境 $\mathcal{E}$ 执行该动作后返回下一观测 $o_{t+1}$：

   $$a_t = \pi_{\theta}(task, o_t, h_{<t}), \quad o_{t+1} = \mathcal{E}(a_t)$$

2. **智能体-人类混合数据采集循环（Agent-Human Hybrid Data Acquisition Loop）**：合并自动化代理与人类专家采集的轨迹。自动化代理通过规则驱动探索产生弱语义轨迹，提供低成本的导航模式；人类专家则创建任务列表并采集高质量演示轨迹，同时随机抽查 20% 的自动化轨迹进行质量审核。这种混合策略在覆盖面与质量之间取得平衡。

采集到的原始轨迹随后由高级 VLM（如 GPT-4o、Claude-3.7）标注为三类任务数据：**GUI 理解**（元素级与截图级的外观、OCR、布局、功能、状态转换标注）、**GUI 定位**（点、框和动作级定位标注），以及**任务完成**（弱语义轨迹与专家演示）。最终语料库包含 471K 条 GUI 理解样本、超过 17.1M 个定位标注，以及 19K 条平均 9 步的轨迹。

### 模型架构与推理范式

ScaleCUA 家族基于 Qwen2.5-VL 构建，支持三种推理范式（图 3）：

- **定位模式（Grounding Mode）**：专注于定位目标 UI 元素，输出坐标或边界框，适合与外部规划器集成。
- **直接动作模式（Direct Action Mode）**：直接生成可执行动作，实现快速的感知-动作循环。
- **推理动作模式（Reasoned Action Mode）**：先产生思维链推理，再输出动作，提高可靠性和可解释性。实验表明，该模式在所有基准上均优于直接动作模式，绝对增益在 +1.4% 到 +8.2% 之间。

### 统一动作空间

为消除平台间的碎片化，ScaleCUA 定义了一套统一的跨平台动作空间（Table 14），将通用操作（如 click、write）与平台专属动作（如移动端的 long press、open app）整合在一起，使单一模型能够无缝地在桌面、移动和 Web 环境间切换。

### 训练策略

训练时，ScaleCUA 根据模型规模控制通用数据与 GUI 数据的混合比例：3B 模型使用 25% 通用数据，7B 使用 50%，32B 使用 75%。这种数据平衡策略被证明是保留 GUI 专业化能力而不损害通用推理能力的关键。



### 智能体-环境交互范式

ScaleCUA 将计算机使用任务形式化为一个标准化的智能体-环境交互过程。在每一时间步 $t$，智能体模型 $\pi_{\theta}$ 根据任务描述 $task$、当前视觉观测 $o_t$ 和历史信息 $h_{<t}$ 生成动作 $a_t$；环境 $\mathcal{E}$ 执行该动作并返回下一观测 $o_{t+1}$。该交互范式可表达为：

$$a_t = \pi_{\theta}(task, o_t, h_{<t}), \quad o_{t+1} = \mathcal{E}(a_t)$$

这一公式是 ScaleCUA 所有推理模式的基础框架，其核心在于模型需要同时具备感知（理解 $o_t$）、推理（结合 $task$ 与 $h_{<t}$ 规划下一步）和动作（生成 $a_t$）的能力。

### 跨平台交互数据管道

ScaleCUA 的数据获取依赖一个双环协同的跨平台交互数据管道（参见 Figure 2），由两个核心模块构成：

1.  **智能体-环境交互环**：标准化跨平台观测获取与动作执行。该模块统一了 Windows、Ubuntu、macOS、Web、Android 和 iOS 六大平台的交互接口，确保智能体或人类操作者能以一致的方式获取屏幕截图并执行动作，从而消除平台碎片化带来的数据格式差异。

2.  **智能体-人类混合数据采集环**：合并自动化代理与人类专家采集的轨迹。自动化代理通过规则驱动的方式在环境中探索，生成大规模弱语义轨迹；人类专家则创建任务列表并采集高质量演示轨迹，同时对 20% 的自动化采集数据进行随机抽检，保障数据质量。

采集到的原始轨迹随后被送入标注阶段，由高级视觉语言模型（如 GPT-4o 和 Claude-3.7）加工为三类核心任务数据：GUI 理解（元素级与截图级的语义、布局、功能标注）、GUI 定位（点、框和动作级定位对齐）和任务完成（弱语义轨迹与专家演示）。最终语料包含 471K 理解样本、超过 17.1M 定位标注和 19K 条平均长度为 9 步的交互轨迹。

### 统一动作空间

为实现真正的跨平台操作，ScaleCUA 定义了一个统一的动作空间（详见 Table 14），将桌面、移动和 Web 平台的动作抽象为通用操作与平台专属操作两个层次。通用操作包括 `click`、`write`、`scroll` 等跨平台基础动作；平台专属操作则针对特定交互范式设计，例如移动端的 `long press` 和 `open app`。这种分层设计使单一模型能够在不依赖平台特定适配器的情况下，直接输出可执行的动作指令。

### 三种推理模式

ScaleCUA 支持三种灵活切换的推理模式（参见 Figure 3），以适应不同的应用场景：

1.  **定位模式**：专注于定位目标 UI 元素，输出元素的坐标或边界框。该模式适合与外部规划器集成，将感知与决策解耦。

2.  **直接动作模式**：直接基于当前观测和指令生成可执行动作，实现快速的感知-动作循环。该模式延迟最低，适合对实时性要求高的场景。

3.  **推理动作模式**：先生成思维链推理过程，再输出动作。该模式通过显式推理提高了决策的可靠性和可解释性，实验表明其成功率相比直接动作模式有 +1.4% 到 +8.2% 的绝对提升，但代价是更高的推理成本。

三种模式共享同一模型权重，仅在推理时的提示词和输出格式上有所区分，实现了感知、推理与动作的高效整合。

### 数据平衡策略

在多任务训练中，ScaleCUA 针对不同模型规模采用了差异化的数据平衡策略：3B 模型使用 25% 通用数据与 75% GUI 数据，7B 模型使用 50%/50%，32B 模型使用 75%/25%。消融实验表明，增加通用数据比例会提升通用视觉语言基准分数，但会逐渐削弱 GUI 任务的专项性能。这一策略在保持通用推理能力的同时，最大化了对 GUI 任务的适配度，是实现模型“通专兼备”的关键设计。



## 实验与关键发现

### 核心性能突破

ScaleCUA在GUI理解、定位与端到端任务完成三个维度上均展现出显著优势，其核心驱动力来自跨平台数据管道的规模化训练。

在GUI内容理解方面，ScaleCUA-32B在**MMBench-GUI L1-Hard**上取得94.4%的准确率，远超原始基础模型Qwen2.5-VL-72B的64.6%（+29.8个百分点）。更值得注意的是，仅3B参数的ScaleCUA-3B即达到89.9%，已超越72B的基础模型（Table 2），表明领域数据的注入比单纯扩大基础模型规模更为高效。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_yBFUqdJFZn/figures/005_Table_2.jpg]]
*Table 2: Results on MMBench-GUI L1 (GUI Content Understanding) (Wang et al., 2025c)*

在GUI定位能力上，ScaleCUA-32B在**ScreenSpot-Pro**上取得59.2%的整体准确率，较此前最优结果提升10.7个百分点（Figure 1）。在OSWorld-G和ScreenSpot-v2等定位基准上同样保持领先（Figure 4, Table 6-9）。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_yBFUqdJFZn/figures/015_Table_6.jpg]]
*Table 6: (c) The ablation on coordinate types*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_yBFUqdJFZn/figures/018_Table_6.jpg]]
*Table 6: Results on ScreenSpot-v2 (Wu et al., 2024b)*

端到端任务完成是衡量智能体实用性的关键指标。在**WebArena-Lite-v2**（50步预算）上，ScaleCUA-32B取得47.4%的成功率，比最强开源基线UI-TARS-72B-DPO（21.4%）提升26.0个百分点（Table 3）。在OSWorld上达到30.6%，在AndroidWorld上同样表现出色。这些结果表明，统一的感知-推理-动作模型在真实网页和桌面环境中具备可靠的执行能力。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_yBFUqdJFZn/figures/006_Table_3.jpg]]
*Table 3: Online evaluation across different platforms. AndroidWorld has its own predefined step budget. ♣ denotes the unkown step budget and ⋆ indicates more than 50 steps is used*

### 推理模式对比

ScaleCUA支持三种推理范式：直接动作模式（DAM）和推理动作模式（RAM）。消融实验显示，**推理动作模式在所有在线基准上均优于直接动作模式**，绝对提升幅度为1.4%至8.2%（Figure 5b）。这一差异在需要多步规划和复杂决策的任务上尤为明显，验证了思维链推理对任务完成质量的因果性贡献。

### 数据策略消融

数据管道的每个设计选择均经过严格验证（Table 4）：

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_yBFUqdJFZn/figures/013_Table_4.jpg]]
*Table 4: (a) The ablation on data augmentation. We only use GUI-related data in training*

- **数据增强**：在ScreenSpot-Pro上，数据增强（元素裁剪、合成分辨率缩放、推理提示丰富）带来3.5个百分点的绝对提升（37.8→41.3），证明多样化训练信号对定位鲁棒性的重要性。
- **弱语义轨迹**：引入规则驱动的弱语义轨迹训练后，OSWorld成功率从7.6提升至8.5，WebArena-Lite-v2从8.4提升至14.3。这类低成本轨迹提供了关键的导航先验，显著改善了任务完成性能。
- **坐标表示**：原始坐标表示优于归一化坐标（ScreenSpot-Pro: 42.3 vs 37.9），表明保留像素级空间信息有利于精确定位。
- **训练分辨率**：将训练分辨率从1080p提升至2K，ScreenSpot-Pro从42.3提升至45.5，但OSWorld和AndroidWorld的成功率略有下降。这一权衡提示高分辨率训练对定位任务有益，但可能引入与任务完成数据分布不匹配的视觉特征。

### 数据规模与平衡的缩放效应

数据缩放实验揭示了两个关键规律（Figure 5c-d）：

1. **数据量单调增益**：WebArena-Lite-v2的成功率随训练数据量近乎线性增长，而ScreenSpot-Pro在使用约一半数据时即达到较强准确率，表明定位任务对数据量的需求低于任务完成。
2. **通用数据比例需按模型规模调整**：增加通用VLM数据比例会提升通用基准分数，但逐渐降低GUI专项性能。ScaleCUA采用规模相关的平衡策略：3B模型使用25%通用数据，7B使用50%，32B使用75%。这一策略在保持GUI专业能力的同时，避免了大规模模型的通用能力退化。

### 失败模式与改进空间

尽管ScaleCUA在多个基准上达到或超越闭源模型，分析仍揭示了明确的改进方向：

- **规划能力差距**：与GPT-4o相比，ScaleCUA在需要深度规划和推理的长程任务上仍存在显著差距，表明当前模型在任务分解和策略选择方面尚未充分受益于数据缩放。
- **困难平台挑战**：在WindowsAgentArena等复杂基准上，需要更大规模的数据才能达到理想性能，提示当前数据管道的覆盖率仍有扩展空间。
- **历史建模局限**：当前采用扁平的历史表示，无法充分捕获长程依赖关系，限制了模型在需要记忆和状态追踪的任务上的表现。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_yBFUqdJFZn/figures/003_Table_1.jpg]]
*Table 1: Datasets comparisons on computer-use datasets in terms of platform coverage, data types (Understanding, Grounding and Trajectories), and collection methods*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_yBFUqdJFZn/figures/014_Table_13.jpg]]
*Table 13: (b) The ablation on weak semantic trajectories. The public datasets used are shown in Table 13. (d) The ablation on the maximum resolution during training*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_yBFUqdJFZn/figures/016_Table_7.jpg]]

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_yBFUqdJFZn/figures/017_Table_5.jpg]]
*Table 5: Results on MMBench-GUI L1 (GUI Content Understanding) (Wang et al., 2025c)*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_yBFUqdJFZn/figures/019_Table_7.jpg]]
*Table 7: Results on ScreenSpot-Pro (Li et al., 2025)*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_yBFUqdJFZn/figures/020_Table_8.jpg]]
*Table 8: Performance on the MMBench-GUI L2 (GUI Element Grounding) (Wang et al., 2025c)*



## 定位与知识库关联

### 技术路线与基线关系

ScaleCUA 的核心贡献在于通过大规模、跨平台的数据驱动缩放，将通用视觉语言模型（VLM）转化为高性能的计算机使用智能体。该方法建立在 **Qwen2.5-VL**（Bai et al., 2025）基础之上，其技术路线与现有工作形成以下对比关系：

**与通用VLM基线的对比。** 原始 **Qwen2.5-VL-72B** 在 MMBench-GUI L1-Hard 上仅取得 64.6% 的准确率，而 ScaleCUA-32B 达到 94.4%（Table 2），提升 29.8 个百分点。**InternVL3.5-241B-A28B** 等更大规模的通用 VLM 在 GUI 理解任务上同样被 ScaleCUA 显著超越，表明单纯依赖模型规模扩展无法替代领域数据的专业化训练。

**与原生GUI智能体的对比。** **UI-TARS-72B-DPO**（Qin et al., 2025）和 **Aguvis-72B**（Xu et al., 2024）是专门为 GUI 操作设计的智能体。在 WebArena-Lite-v2（50步）上，ScaleCUA-32B 取得 47.4% 的成功率，较 UI-TARS-72B-DPO 的 21.4% 提升 26.0 个百分点（Table 3）。这一差距的核心原因在于 ScaleCUA 的跨平台数据管道覆盖了六个操作系统和三个任务领域，而现有原生 GUI 智能体的训练数据通常局限于单一平台或有限的任务类型。

**与定位器基线的对比。** **JEDI-7B** 等专门定位器仅处理 UI 元素定位任务。ScaleCUA 通过统一的三种推理模式（定位模式、直接动作模式、推理动作模式）将定位、感知和动作整合于单一模型，在 ScreenSpot-Pro 上达到 59.2% 的整体准确率，远超此前不含 ScaleCUA 的最佳结果 48.5%（Figure 1）。

**与商业API基线的对比。** **GPT-4o** 和 **Claude-3.7** 作为闭源商业模型，在部分任务完成基准上仍具优势，尤其在需要复杂规划的长期任务中。ScaleCUA 在 OSWorld 等基准上已接近或达到商业模型水平，但在 WindowsAgentArena 等高难度基准上仍存在显著差距，需要更大规模的数据量才能达到预期性能。

### 关键设计决策与因果机制

**混合双环数据管道。** 现有数据收集方法要么依赖纯人类标注（成本高昂、难以扩展），要么仅使用自动化探索（覆盖面有限、质量不稳定）。ScaleCUA 的混合双环管道（Figure 2）将规则驱动的自动化代理与人类专家监督相结合：自动化代理负责大规模轨迹采集，人类专家创建任务列表并随机审核 20% 的采集数据。这一设计直接解决了数据规模与质量之间的权衡，是模型性能提升的根本原因。

**统一动作空间。** 现有方法通常为不同平台定义专属的动作空间，导致跨平台泛化困难。ScaleCUA 定义了统一的跨平台动作空间（Table 14），将通用操作（如 click、write）与平台特定动作（如移动端的 long press、open app）整合。这一设计使单一模型能够无缝操作桌面、移动和 Web 平台，是跨平台性能一致性的关键。

**三种推理模式。** 现有方法通常仅支持单一推理模式（如直接生成动作）。ScaleCUA 提供定位模式、直接动作模式和推理动作模式三种选择（Figure 3）。推理动作模式在所有基准上均优于直接动作模式，绝对提升幅度为 +1.4% 至 +8.2%（Figure 5b），其机制在于思维链推理提高了动作选择的可靠性和可解释性。

**数据平衡策略。** 通用数据与 GUI 数据的比例对性能有显著影响。增加通用数据比例会提高通用 VLM 基准分数，但会逐渐降低 GUI 基准性能（Figure 5d, Table 12）。ScaleCUA 根据模型规模采用不同的数据比例（3B: 25% GUI, 7B: 50%, 32B: 75%），这一策略对保持 GUI 专业化能力至关重要。

### 适用边界与局限

**规划能力的上限。** 尽管 ScaleCUA 在感知和定位任务上表现出色，其规划能力与 GPT-4o 等商业模型相比仍有显著差距。当前的历史设计采用扁平结构，无法充分捕捉长期依赖关系，限制了在需要多步推理的复杂任务上的表现。

**高难度平台的挑战。** 在 WindowsAgentArena 等复杂基准上，ScaleCUA 仍需更大规模的数据量才能达到预期性能。这表明当前的训练数据规模对于高变异性、高复杂度的桌面环境仍不充分。

**分辨率权衡。** 将训练分辨率从 1080p 提高到 2K 可改善 ScreenSpot-Pro 上的定位准确率（45.5% vs 42.3%），但略微降低 OSWorld 和 AndroidWorld 的成功率（Table 4d）。这一权衡表明高分辨率带来的视觉细节增益可能被训练-推理分布偏移所抵消。

**数据收集的可持续性。** 当前的数据管道依赖人类专家创建任务列表和审核轨迹，虽然成本低于纯人工标注，但仍需要持续的人力投入。如何将自动数据收集与迭代优化整合为自我改进循环，仍是一个未充分探索的问题。

### 开放问题

1. **自我改进循环：** 将自动数据收集与迭代优化整合为自我改进循环的机制尚未建立，这是实现持续性能提升的关键瓶颈。

2. **高级智能体技术：** 反思（reflection）、强化学习等高级智能体技术尚未被采用，这些技术可能进一步提升规划能力和长期任务成功率。

3. **长期依赖建模：** 当前扁平的历史表示无法有效捕捉长期依赖关系，需要设计更强大的记忆和上下文管理机制。

4. **跨平台迁移的极限：** 统一动作空间和跨平台训练的有效性边界尚不明确，是否存在某些平台或任务类型需要完全独立的建模策略仍需探索。



## 原文 PDF

![[paperPDFs/ICLR_2026/ScaleCUA_Scaling_Open_Source_Computer_Use_Agents_with_Cross_Platform_Data.pdf]]
