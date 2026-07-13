---
title: "MMBench-GUI: A Unified Hierarchical Evaluation Framework for Multi-Platform GUI Agents"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MMBench_GUI_A_Unified_Hierarchical_Evaluation_Framework_for_Multi_Platform_GUI_Agents.pdf
project_link: null
code_link: "https://github.com/opencompass/MMBench-GUI"
aliases:
- MG
- MMBench-GUI
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 是否集成专用的视觉定位模块（如UI-TARS、UGround），以及是否优化步骤预算与效率。
primary_logic: 通过层次化多平台基准测试，系统性地揭示了视觉定位能力对GUI任务成功的关键作用；引入EQA（效率-质量感知）指标，同步衡量成功率和交互效率，推动开发更强大且高效的GUI智能体。
claims:
- 精确的视觉定位是决定性能的关键因素，模块化设计集成了专用定位模块的智能体表现显著更好。
- 所有智能体都面临严重的效率问题，即使任务最终成功也经常包含大量冗余步骤。
- 在L3任务自动化上，GPT-4o + UI-TARS-1.5-7B 相比单独 GPT-4o 成功率大幅提升（约20个百分点），证明了专用定位模块的增益。
- L3-GUI Task Automation 上 Success Rate (SR) = GPT-4o + UI-TARS-1.5-7B (26.6%)
---

# MMBench-GUI: A Unified Hierarchical Evaluation Framework for Multi-Platform GUI Agents

> [!tip] 核心洞察
> 通过层次化多平台基准测试，系统性地揭示了视觉定位能力对GUI任务成功的关键作用；引入EQA（效率-质量感知）指标，同步衡量成功率和交互效率，推动开发更强大且高效的GUI智能体。

| 字段 | 内容 |
|------|------|
| 中文题名 | MMBench-GUI：面向多平台GUI智能体的统一分层评估框架 |
| 英文题名 | MMBench-GUI: A Unified Hierarchical Evaluation Framework for Multi-Platform GUI Agents |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_MMBench-GUI_A_Unified_Hierarchical_Evaluation_Framework_for_Multi-Platform_GUI_Agents_CVPR_2026_paper.html) · [Code](https://github.com/opencompass/MMBench-GUI) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | MMBench-GUI |
| Dataset | L3-GUI Task Automation, L4-GUI Task Collaboration |

> [!tip] 效果简介
> - L3-GUI Task Automation 上，Success Rate (SR) GPT-4o + UI-TARS-1.5-7B (26.6%) vs GPT-4o (6.13%) (+20.47%)。
> - L4-GUI Task Collaboration (Max Steps=15) 上，Success Rate (SR) GPT-4o + UI-TARS-1.5-7B (12.3) vs GPT-4o (7.5) (+4.8%)。

## 概要

GUI 智能体正逐步成为人机交互自动化的核心范式，但其评估体系长期受限于平台碎片化与指标单一化两大瓶颈。现有基准或聚焦单一平台（如仅 Web），或仅衡量最终成功率而忽略交互效率，难以系统诊断智能体的真实能力边界。

MMBench-GUI 针对上述缺口，提出了**统一分层评估框架**，核心设计包含三个维度：

1. **四层次递进任务体系**：从离线静态的 GUI 内容理解（L1）与元素定位（L2），递进到在线交互的单应用任务自动化（L3）与跨应用任务协作（L4），逐层加压，全面探测智能体的感知、规划与泛化能力。
2. **六大平台统一覆盖**：数据集横跨 Windows、macOS、Linux、iOS、Android 与 Web，消除平台偏差对评估结论的干扰。
3. **效率-质量感知（EQA）指标**：在成功率之外引入步骤预算约束，同步衡量任务完成质量与交互效率，暴露智能体的冗余操作问题。

**核心发现**：精确的视觉定位（visual grounding）是决定 GUI 智能体性能的关键瓶颈。集成专用定位模块（如 UI-TARS）的模块化智能体相较通用模型，在 L3 任务自动化上成功率可提升约 20 个百分点（GPT-4o 从 6.13% 提升至 26.6%）。然而，所有智能体均面临严重的效率问题——即使任务最终成功，也常伴随大量冗余步骤；在 L4 跨应用协作场景中，性能普遍急剧下降，最高成功率仅约 12.3%（步骤预算 15 步），揭示出当前智能体在记忆、规划与自适应推理方面的显著不足。

**方法定位**：MMBench-GUI 并非提出新的智能体架构，而是构建了一套标准化的诊断工具。在方法谱系中，它填补了从单一技能评测到端到端交互评测之间的空白——相比仅关注元素定位的 ScreenSpot 或仅关注 Web 导航的 Mind2Web，本框架通过四层递进设计与多平台覆盖，为 GUI 智能体的能力剖面提供了更完整的量化视图。其 EQA 指标也为后续研究设立了效率维度的评估基准，推动社区从“能做”向“高效地做”转变。



图形用户界面（GUI）是人与数字系统交互的核心媒介。近年来，基于多模态大模型的GUI智能体取得了显著进展，能够理解屏幕内容并自主执行操作。然而，该领域的评估体系仍存在三个关键缺口：

**评估维度单一。** 现有基准测试大多聚焦于孤立的技能评估，如仅测试元素定位或仅测试内容问答，缺乏对智能体综合能力的递进式度量。真实场景中的GUI任务往往需要从理解界面语义、到精确定位元素、再到多步规划与执行的完整链路，单一维度的评估无法揭示智能体的能力瓶颈。

**平台覆盖碎片化。** 多数基准仅针对单一平台（如仅Web端或仅移动端）构建，难以衡量智能体在跨平台场景下的泛化能力。现代工作流频繁跨越桌面、移动、Web等多端环境，碎片化的评估无法反映这一现实需求。

**效率维度缺失。** 现有评估几乎完全以成功率（Success Rate）为唯一指标，忽视了交互效率这一关键维度。一个智能体即使最终完成任务，若需大量冗余步骤，其实用价值将大打折扣。当前缺乏将效率与质量统一考量的评估框架。

针对上述缺口，本文提出 **MMBench-GUI**，一个面向多平台GUI智能体的统一分层评估框架。其核心设计思路包括：（1）构建四个递进层次——内容理解（L1）、元素定位（L2）、任务自动化（L3）和任务协作（L4），系统性地度量智能体从基础语义理解到复杂跨应用协作的全谱系能力；（2）覆盖Windows、macOS、Linux、iOS、Android和Web六大主流平台，提供统一的跨平台评估基准；（3）引入效率-质量感知指标（EQA），同步衡量任务成功率和步骤预算，推动开发更强大且高效的GUI智能体。



## 核心方法与创新机理

MMBench-GUI 的核心创新并非提出一个新的智能体模型，而是构建了一套**统一的、层次化的评估体系**，系统性地改变了 GUI 智能体的评测范式。相对于以往仅关注单一技能或单一平台的基准，本工作在以下四个关键维度上实现了根本性的改变。

### 1. 从单一技能到四层递进评估

现有基准通常仅评估孤立的 GUI 技能（如仅做元素定位或仅做截图问答），无法反映真实任务中感知、定位、规划、执行的级联依赖关系。MMBench-GUI 将评估组织为四个难度递增的层次（Figure 1）：

- **L1-GUI 内容理解**：离线的多项选择问答，评估模型对 GUI 截图中语义信息的理解能力。
- **L2-GUI 元素定位**：离线的点坐标预测，评估模型根据自然语言指令精准定位界面元素的能力。
- **L3-GUI 任务自动化**：在线的单应用多步交互，要求智能体在单一应用内完成一个完整任务流程。
- **L4-GUI 任务协作**：在线的跨应用多步交互，要求智能体在多个应用之间切换以完成复杂协作任务。

这一递进设计形成了一个“认知漏斗”：L1/L2 作为离线快速筛选层，L3/L4 作为在线深度验证层。这种结构不仅降低了全面评估的计算成本，更关键的是，它允许研究者**逐层定位智能体的能力瓶颈**——例如，一个智能体在 L3 上表现差，究竟是因为不理解界面内容（L1），还是因为无法精准点击目标（L2），抑或是缺乏多步规划能力（L3 自身）。这种可诊断性是此前任何单一维度基准所不具备的。

### 2. 从单平台到六大平台统一覆盖

GUI 智能体的一个核心挑战是跨平台泛化——在 Web 上表现良好的策略可能在移动端完全失效。然而，此前的工作大多局限于单一平台（如仅 Web 或仅 Android）。MMBench-GUI 首次构建了覆盖 **Windows、macOS、Linux、iOS、Android 和 Web** 六大主流平台的数据集，包含超过 8000 个任务实例。

这种多平台设计使得跨平台泛化能力成为可量化指标。从实验结果来看，模型在不同平台上的性能差异显著（Table 1, Table 2），揭示了当前 GUI 智能体在平台迁移时的脆弱性，为后续研究提供了明确的改进方向。

### 3. 从仅成功率到效率-质量感知指标（EQA）

传统 GUI 智能体评估几乎完全依赖成功率（Success Rate），这掩盖了一个严重问题：**即使任务最终成功，智能体也可能执行了大量冗余、低效的操作**。MMBench-GUI 提出了效率-质量感知指标（Efficiency-Quality-Aware, EQA），其核心思想是：

$$
\mathrm{EQA} \propto \sum_{m=1}^{M} \mathrm{SR}(B_m)
$$

该指标在不同步骤预算 $B_m$ 下计算成功率，并对其累加求和后归一化到 $[0,1]$ 区间。在较少步骤内达到高成功率的智能体获得更高的 EQA 分数，而仅通过冗长操作序列才能成功的智能体则受到惩罚。

这一设计将“效率”内嵌为评估的一等公民，而非事后分析。实验结果显示，所有被评估的智能体都存在严重的效率问题——即使在宽松的步骤预算下成功，其操作序列中也充斥着冗余步骤。EQA 指标使得这种低效性可以被精确量化，推动社区关注“既对且快”的 GUI 智能体设计。

### 4. 离线静态与在线交互任务的有机结合

L1 和 L2 采用离线静态评估，无需启动虚拟环境，可在数分钟内完成对模型基本感知能力的快速诊断；L3 和 L4 则在真实虚拟环境中进行在线交互评估，捕捉规划、执行和错误恢复等动态能力。这种“离线快筛 + 在线深测”的混合设计在评估成本和评估深度之间取得了实用平衡，为大规模、高频次的模型迭代提供了可行方案。

### 总结

MMBench-GUI 的核心贡献在于**重新定义了 GUI 智能体的评估标准**：从“能不能完成任务”的单一维度，升级为“在多大平台上、以多高效率、完成多复杂任务”的多维综合评估。这一范式的转变直接揭示了当前 GUI 智能体的两个关键瓶颈——**视觉定位精度不足**和**操作效率低下**——为后续研究指明了方向：集成专用定位模块（如 UI-TARS）和优化步骤规划效率是提升性能的关键路径。



MMBench-GUI 是一个面向多平台 GUI 智能体的统一分层评估框架，其设计核心在于**将评估难度从静态理解递进到动态交互与跨应用协作**，从而系统性地揭示智能体在不同能力维度上的瓶颈。框架整体由四个层次、一个效率感知指标和统一的评估协议构成。

### 四层递进式任务体系

如图 Figure 1 所示，框架将 GUI 智能体评估组织为四个难度递增的层次：

![[assets/figures/papers/paper_list_l766_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_MMBench_GUI_A_Uni/figures/001_Figure_1.jpg]]
*Figure 1: MMBench-GUI: a hierarchical benchmark spanning four levels of increasing difficulty, covering over 8,000 tasks across six commonly used platforms. From L1 to L4, task complexity increases progressively, placing growing demands on the agent’s generalization and reasoning abilities. Based on this benchmark, we visualize the performance of various models in the right figure, clearly illustrating their respective strengths as well as areas with substantial room for improvement*

- **L1 — GUI 内容理解 (GUI Content Understanding)**：离线多项选择问答任务。给定 GUI 截图 $\mathbf{V}$、问题 $q$ 和选项集 $\mathcal{O}$，智能体需选出正确选项 $o^* = \mathrm{Agent}(\mathbf{V}, q, \mathcal{O})$。该层评估智能体对界面语义元素的识别与理解能力。

- **L2 — GUI 元素定位 (GUI Element Grounding)**：离线定位任务。给定自然语言指令 $\mathrm{ins}$ 和 GUI 截图 $\mathbf{V}$，智能体需预测目标元素的交互点坐标 $p = \mathrm{Agent}(\mathrm{ins}, \mathbf{V})$。该层直接衡量视觉定位（visual grounding）精度。

- **L3 — GUI 任务自动化 (GUI Task Automation)**：在线交互任务，要求智能体在**单个应用**内完成多步操作。交互循环为：
  $$A_t, P_t = \operatorname{Agent}(\operatorname{ins}, \mathbf{V}_t, \mathcal{H}_t, S_s), \quad \mathbf{V}_{t+1} = \operatorname{Env}(A_t, P_t), \quad \mathcal{H}_{t+1} = \{\mathcal{H}_t, (\mathbf{V}_t, A_t, P_t)\}$$
  其中 $S_s$ 为当前应用状态空间，$\mathcal{H}_t$ 为历史记录。智能体每步产生动作 $A_t$ 与参数 $P_t$，环境据此更新视图。

- **L4 — GUI 任务协作 (GUI Task Collaboration)**：在线交互任务，要求智能体在**多个应用之间**协调完成复杂任务。交互循环与 L3 类似，但状态空间扩展为多应用集合 $\mathcal{S}_m$：
  $$A_t, P_t = \operatorname{Agent}(\operatorname{ins}, \mathbf{V}_t, \mathcal{H}_t, \mathcal{S}_m)$$

L1 和 L2 为离线静态任务，支持快速评估；L3 和 L4 在虚拟环境中以在线方式执行，评估智能体的规划、记忆与自适应推理能力。Figure 2 展示了四个层次的典型任务示例。

### 效率-质量感知指标 (EQA)

传统评估仅关注成功率（Success Rate），忽略了智能体的操作效率。MMBench-GUI 提出了 **EQA (Efficiency-Quality-Aware)** 指标，同步衡量任务成功与步骤冗余：

$$\mathrm{EQA} \propto \sum_{m=1}^{M} \mathrm{SR}(B_m)$$

该指标正比于不同步骤预算 $B_m$ 下成功率的累加和，归一化到 $[0, 1]$ 区间。智能体若以较少步骤完成任务，将在多个预算档位上均获得成功，从而累积更高的 EQA 分数；反之，包含大量冗余步骤的智能体仅在宽松预算下成功，EQA 得分较低。

### 统一评估协议

为确保公平比较，框架对所有模型采用统一评估管线：通用视觉语言模型（如 **GPT-4o**、**Claude-3.7**、**InternVL3-72B**、**Qwen2.5-VL-72B**）使用标准化的提示模板和动作空间；专用 GUI 智能体（如 **UI-TARS-72B-DPO**、**Aguvis-72B**）则使用其官方推荐设置。L1 采用加权准确率，L2 采用点落入边界框（point-in-box）准确率，L3/L4 通过程序化成功检查（检查最终环境状态，如文件存在性与内容）判定任务是否达成。

### 关键设计优势

与仅覆盖单一技能或单一平台的现有基准相比，MMBench-GUI 的核心差异在于：

| 评估维度 | 现有基准 | MMBench-GUI |
|---------|---------|-------------|
| 任务层次 | 单一技能（仅定位或仅问答） | 四层递进（理解→定位→自动化→协作） |
| 平台覆盖 | 受限（仅 Web 或单平台） | 六大平台统一覆盖（Windows, macOS, Linux, iOS, Android, Web） |
| 效率评估 | 仅成功率 | EQA 指标综合成功与步骤预算 |
| 任务类型 | 仅离线或仅在线 | 离线静态（L1/L2）+ 在线交互（L3/L4）结合 |

这种层次化设计使得框架能够**逐层定位智能体的能力瓶颈**：L1/L2 揭示感知与定位缺陷，L3/L4 暴露规划与效率问题，从而为模型改进提供明确方向。



### 四层递进评估架构

MMBench-GUI 将 GUI 智能体评估组织为四个递进难度层级，每层对应不同的能力维度与评估范式：

- **L1-GUI 内容理解 (Content Understanding)**：离线多项选择问答，评估模型对 GUI 截图语义信息的理解能力。
- **L2-GUI 元素定位 (Element Grounding)**：离线元素定位，评估模型根据自然语言指令在截图中准确定位目标交互点的能力。
- **L3-GUI 任务自动化 (Task Automation)**：在线单应用多步交互任务，评估智能体在单一应用内完成复杂操作的规划与执行能力。
- **L4-GUI 任务协作 (Task Collaboration)**：在线跨应用多步交互任务，评估智能体在多个应用间切换协作完成目标的能力。

其中 L1 和 L2 为离线静态任务，可快速批量评估；L3 和 L4 在虚拟环境中以在线交互方式运行。

### 关键公式与变量定义

**L1 内容理解预测公式**

$$o ^ { * } = \mathrm { A g e n t } ( \mathbf { V } , q , \mathcal { O } )$$

给定 GUI 截图的视觉观察 $\mathbf{V}$ 和自然语言问题 $q$，智能体从候选选项集合 $\mathcal{O}$ 中选择正确选项 $o^*$。该公式将 GUI 内容理解形式化为标准的多项选择问答任务。

**L2 元素定位公式**

$$p = \mathrm { A g e n t } ( \mathrm { i n s } , \mathbf { V } )$$

给定自然语言指令 $\mathrm{ins}$ 和 GUI 截图 $\mathbf{V}$，智能体预测目标元素的交互点 $p$（二维坐标）。评估采用点入框（point-in-box）准确率：当预测坐标落在目标元素的真实边界框内时判定为正确。

**L3 单应用交互循环**

$$A_t, P_t = \operatorname { A g e n t } ( \operatorname { i n s } , \mathbf { V } _ t , \mathcal { H } _ t , S_s ), \quad \mathbf { V } _ { t + 1 } = \operatorname { E n v } ( A_t , P_t ), \quad \mathcal { H } _ { t + 1 } = \{ \mathcal { H } _ t , ( \mathbf { V } _ t , A_t , P_t ) \}$$

在时刻 $t$，智能体基于任务指令 $\mathrm{ins}$、当前视觉观察 $\mathbf{V}_t$、交互历史 $\mathcal{H}_t$ 和当前应用状态 $S_s$，产生动作 $A_t$ 及其参数 $P_t$。环境执行该动作后更新为新的视觉状态 $\mathbf{V}_{t+1}$，并将本轮交互追加到历史 $\mathcal{H}_{t+1}$。循环持续至任务完成或达到步骤预算上限。

**L4 多应用交互循环**

$$A_t, P_t = \operatorname { A g e n t } ( \operatorname { i n s } , \mathbf { V } _ t , \mathcal { H } _ t , \mathcal { S } _ m ), \quad \mathbf { V } _ { t + 1 } = \operatorname { E n v } ( A_t , P_t ), \quad \mathcal { H } _ { t + 1 } = \{ \mathcal { H } _ t , ( \mathbf { V } _ t , A_t , P_t ) \}$$

与 L3 的关键差异在于，智能体需感知多个相关应用的集合 $\mathcal{S}_m$，在跨应用场景中进行状态切换与协作。这要求智能体具备更强的上下文记忆、任务规划与自适应推理能力。

**EQA 效率-质量感知指标**

$$\mathrm { E Q A } \propto \sum _ { m = 1 } ^ { M } \mathrm { S R } ( B _ { m } )$$

EQA 指标正比于不同步骤预算 $B_m$ 下成功率 $\mathrm{SR}(B_m)$ 的累加和，最终归一化到 $[0,1]$ 区间。该设计同时捕捉任务完成质量（是否成功）与交互效率（所需步骤数）：以较少步骤稳定成功的智能体获得更高 EQA 分数，而依赖大量冗余步骤才能完成任务的智能体得分较低。

### 评估协议设计

L3/L4 的任务成功判定采用程序化检查：每个任务配备一个自动化的成功验证函数，直接检测最终环境状态（如文件是否存在及其内容是否正确），而非依赖模型自报或人工评判，确保评估的客观性和可复现性。评估时使用统一的离散步骤预算集合和规范化的任务排序，保证不同智能体间的公平比较。

### 补充图表

![[assets/figures/papers/paper_list_l766_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_MMBench_GUI_A_Uni/figures/002_Figure_2.jpg]]
*Figure 2: Examples for all levels. Both of L1 and L2 are offline tasks for quick evaluation. Tasks of L3 and L4 are evaluated in the virtual environment with an online manner*



## 实验与关键发现

### 评估设置

MMBench-GUI 采用统一的评估协议，确保所有智能体在公平条件下进行比较。对于通用视觉语言模型（如 **GPT-4o** (Hurst et al., 2024)、**Claude-3.7** (Anthropic, 2025)、**InternVL3-72B** (Zhu et al., 2025)），使用标准化的提示词和动作空间；对于专用 GUI 智能体（如 **UI-TARS-72B-DPO** (Qin et al., 2025)、**Aguvis-72B** (Xu et al., 2024)），则使用其官方推荐设置。L1 和 L2 任务为离线评估，可直接在静态截图上完成；L3 和 L4 任务在虚拟环境中以在线交互方式运行，每个任务配备程序化成功检查，通过检测最终环境状态（如文件存在性与内容）判定任务是否达成。

为衡量操作效率，论文提出 **EQA（Efficiency-Quality-Aware）** 指标，其核心定义为：

$$\mathrm { E Q A } \propto \sum _ { m = 1 } ^ { M } \mathrm { S R } ( B _ { m } )$$

该指标正比于不同步骤预算 $B_m$ 下成功率的累加和，并归一化到 $[0, 1]$ 区间。智能体若能在较少步骤内达成高成功率，则获得更高的 EQA 分数；仅通过冗长或冗余动作序列才能成功的智能体将受到惩罚。实践中使用一组固定的离散预算和跨智能体共享的规范任务排序，以保证公平性。

### L1-GUI 内容理解结果

Table 1 展示了各模型在 L1 层次（GUI 内容理解）上的表现。该层次将任务形式化为基于 GUI 截图的单项选择题：

![[assets/figures/papers/paper_list_l766_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_MMBench_GUI_A_Uni/figures/003_Table_1.jpg]]
*Table 1: Performance on L1-GUI Content Understanding. ‘Overall’ represents the aggregated score across all platforms, calculated as a weighted sum of individual platform scores*

$$o ^ { * } = \mathrm { A g e n t } ( \mathbf { V } , q , \mathcal { O } )$$

给定视觉观察 $\mathbf{V}$ 和问题 $q$，智能体从选项集 $\mathcal{O}$ 中选择正确选项 $o^*$。

**InternVL3-72B** 在所有难度级别上均取得最高综合得分（Easy 79.15, Medium 77.89, Hard 75.70），展现出最强的 GUI 截图理解能力。一个普遍趋势是：所有模型的性能随任务难度递增而下降（Easy > Medium > Hard），表明复杂 GUI 场景中的语义理解仍是挑战。Overall 分数为各平台分数的加权和，反映了跨平台的综合表现。

### L2-GUI 元素定位结果

Table 2 给出了 L2 层次（GUI 元素定位）的结果。该任务要求智能体根据指令预测目标元素的交互点：

![[assets/figures/papers/paper_list_l766_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_MMBench_GUI_A_Uni/figures/004_Table_2.jpg]]
*Table 2: Performance on the L2-GUI Element Grounding. “Adv.” stands for advanced, while “Avg.” refers to the weighted average of all results in a row, where the weights correspond to the proportion of tasks for each platform and mode relative to the total number of tasks*

$$p = \mathrm { A g e n t } ( \mathrm { i n s } , \mathbf { V } )$$

预测的二维坐标 $p$ 若落在目标元素的边界框内，则判定为正确。

**UI-TARS-72B-DPO** 取得最高平均定位准确率（Avg. 74.3），显著优于通用模型，验证了专用 GUI 定位模块的优势。表中区分了基础指令和高级指令（Adv.）两种模式，后者涉及更复杂的语义描述，普遍导致准确率下降，揭示了现有模型在理解抽象指令与视觉元素对应关系上的不足。

### L3/L4 任务自动化与协作结果

Table 3 呈现了 L3（单应用任务自动化）和 L4（跨应用任务协作）的核心结果，这是整个基准测试中最具挑战性的两个层次。

![[assets/figures/papers/paper_list_l766_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_MMBench_GUI_A_Uni/figures/005_Table_3.jpg]]
*Table 3: Evaluation result of L3-GUI Task Automation and L4-GUI Task Collaboration. Values in bold indicate the highest score within each group; underlined values indicate the second highest*

**L3 单应用多步任务** 的交互循环定义为：

$$A_t, P_t = \operatorname { A g e n t } ( \operatorname { i n s } , \mathbf { V } _ t , \mathcal { H } _ t , S_s ), \mathbf { V } _ { t + 1 } = \operatorname { E n v } ( A_t , P_t ), \mathcal { H } _ { t + 1 } = \{ \mathcal { H } _ t , ( \mathbf { V } _ t , A_t , P_t ) \}$$

智能体根据指令、当前视图 $\mathbf{V}_t$、历史 $\mathcal{H}_t$ 和当前应用状态 $S_s$ 产生动作和参数，环境据此更新状态。

- **GPT-4o 单独使用** 在 L3 上的成功率仅为 **6.13%**，表现极弱。
- **GPT-4o + UI-TARS-1.5-7B** 组合取得 **26.6%** 的成功率，提升约 **20 个百分点**，是该层次的最优结果。这一巨大差异有力地证明了集成专用视觉定位模块是提升 GUI 任务成功率的关键因果机制。

**L4 跨应用多步协作** 进一步将动作空间扩展到多个应用集合 $\mathcal{S}_m$：

$$A_t, P_t = \operatorname { A g e n t } ( \operatorname { i n s } , \mathbf { V } _ t , \mathcal { H } _ t , \mathcal { S } _ m ), \mathbf { V } _ { t + 1 } = \operatorname { E n v } ( A_t , P_t ), \mathcal { H } _ { t + 1 } = \{ \mathcal { H } _ t , ( \mathbf { V } _ t , A_t , P_t ) \}$$

在最大步数限制为 15 的条件下，所有智能体的成功率均大幅降低。GPT-4o + UI-TARS-1.5-7B 的成功率仅为 **12.3%**，相比 GPT-4o 单独使用（7.5%）的提升幅度远小于 L3（+4.8 个百分点 vs. +20 个百分点），表明跨应用协作场景对记忆、规划和自适应推理提出了更高要求，现有智能体普遍存在严重的能力瓶颈。

### 关键发现与失败模式分析

综合四个层次的实验结果，可归纳以下核心发现：

1. **视觉定位是性能瓶颈**：从 L2 到 L3 的性能跃迁中，是否集成专用定位模块（如 UI-TARS）是区分高低表现的决定性因素。GPT-4o + UI-TARS 组合相比纯 GPT-4o 的 L3 成功率提升高达 20 个百分点，直接验证了这一因果机制。

2. **操作效率普遍低下**：所有智能体均面临严重的效率问题。即使任务最终成功，也经常包含大量冗余步骤。EQA 指标通过联合衡量成功率和步骤预算，系统性地暴露了这一缺陷——当前智能体倾向于通过“暴力尝试”而非高效规划来完成任务。

3. **跨应用协作是未解决的难题**：L4 任务中所有智能体的成功率均处于极低水平（最高仅 12.3%），暴露出记忆管理、跨应用状态追踪和自适应推理方面的根本性不足。这一发现为后续研究指明了明确的改进方向。

4. **难度梯度设计的有效性**：从 L1 到 L4，任务复杂度递增对智能体的泛化和推理能力提出了逐步增长的需求，性能的阶梯式下降验证了层次化基准设计能够有效区分不同能力维度的强弱项。



## 定位与知识库关联

### 1. 任务定义与范式定位

MMBench-GUI 将 GUI 智能体评估组织为四个递进层次，形成“理解→定位→规划→协作”的完整能力链：

- **L1-GUI Content Understanding**：离线多项选择问答（MCQA），给定 GUI 截图 $\mathbf{V}$ 和问题 $q$，从选项集 $\mathcal{O}$ 中选择正确选项 $o^*$：
  $$o ^ { * } = \mathrm { A g e n t } ( \mathbf { V } , q , \mathcal { O } )$$
- **L2-GUI Element Grounding**：离线元素定位，给定指令 $\mathrm{ins}$ 和 GUI 截图 $\mathbf{V}$，预测目标元素的交互点 $p$（二维坐标）：
  $$p = \mathrm { A g e n t } ( \mathrm { i n s } , \mathbf { V } )$$
- **L3-GUI Task Automation**：在线单应用多步任务，智能体在单个应用 $S_s$ 内根据指令、当前视图 $\mathbf{V}_t$、历史 $\mathcal{H}_t$ 产生动作和参数，环境更新状态：
  $$A_t, P_t = \operatorname { A g e n t } ( \operatorname { i n s } , \mathbf { V } _ t , \mathcal { H } _ t , S_s ), \quad \mathbf { V } _ { t + 1 } = \operatorname { E n v } ( A_t , P_t )$$
- **L4-GUI Task Collaboration**：在线跨应用多步协作，将单应用 $S_s$ 扩展为多应用集合 $\mathcal{S}_m$，其余交互循环结构与 L3 一致。

该框架的**核心创新**在于将离线静态评估（L1/L2）与在线交互评估（L3/L4）统一在同一基准中，并引入 **EQA（Efficiency-Quality-Aware）指标**，正比于不同步骤预算 $B_m$ 下成功率 $\mathrm{SR}(B_m)$ 的累加和，归一化到 $[0,1]$：
$$\mathrm { E Q A } \propto \sum _ { m = 1 } ^ { M } \mathrm { S R } ( B _ { m } )$$

### 2. 与基线工作的关系

MMBench-GUI 评估了多类代表性基线，覆盖通用视觉语言模型和 GUI 专用智能体：

| 基线模型 | 类型 | 来源 |
|---------|------|------|
| **GPT-4o** | 通用 VLM | Hurst et al., 2024 |
| **Claude-3.7** | 通用 VLM | Anthropic, 2025 |
| **InternVL3-72B** | 开源多模态 | Zhu et al., 2025 |
| **Qwen2.5-VL-72B** | 开源多模态 | Bai et al., 2025 |
| **UI-TARS-72B-DPO** | GUI 专用 | Qin et al., 2025 |
| **Aguvis-72B** | 纯视觉 GUI 智能体 | Xu et al., 2024 |

**关键性能差异**：在 L3 任务自动化中，GPT-4o 单独使用时成功率仅 6.13%，而集成专用视觉定位模块 **UI-TARS-1.5-7B** 后提升至 26.6%（+20.47 个百分点），验证了“视觉定位是核心瓶颈”这一论断。在 L4 跨应用协作中，同样组合在 15 步预算下达到 12.3% 成功率，相比 GPT-4o 的 7.5% 提升 4.8 个百分点，但绝对值仍然很低，表明复杂跨应用场景对所有智能体都构成严峻挑战。

### 3. 方法谱系中的位置

MMBench-GUI 在 GUI 智能体评估领域引入了三个关键维度变化：

| 维度 | 先前工作 | MMBench-GUI |
|------|---------|-------------|
| 评估层次 | 单一技能（如仅定位或仅问答） | 四层次递进（理解→定位→自动化→协作） |
| 平台覆盖 | 受限平台（如仅 Web） | 六大平台统一（Windows, macOS, Linux, iOS, Android, Web） |
| 效率评估 | 仅成功率（SR） | EQA 指标，综合成功率和步骤预算 |

该基准的**适用边界**明确：L1/L2 为离线任务，适合快速评估理解和定位能力；L3/L4 为在线交互任务，需要在虚拟环境中运行，评估完整的规划与执行能力。评估协议确保公平性——通用模型使用标准化提示和动作空间，专用 GUI 模型使用其官方设置。

### 4. 局限与开放问题

**已识别的核心局限**：

1. **视觉定位是主要瓶颈**：精确的 visual grounding 是决定 GUI 智能体性能的关键因素，模块化设计集成了专用定位模块（如 UI-TARS、UGround）的智能体表现显著优于纯端到端方案。
2. **操作效率普遍低下**：所有智能体都面临严重的效率问题，即使任务最终成功也经常包含大量冗余步骤。EQA 指标量化了这一现象，但尚未提出系统性的效率优化方案。
3. **跨应用协作能力薄弱**：在 L4 任务中，所有智能体性能急剧下降，暴露出记忆、规划和自适应推理的不足。当前方法缺乏有效的跨应用上下文管理和任务分解机制。

**开放问题**：

- 如何设计更高效的视觉定位模块，在保持精度的同时降低计算开销？
- 能否通过强化学习或偏好优化直接优化 EQA 指标，从而训练出既准确又高效的 GUI 智能体？
- L4 跨应用协作场景需要何种记忆架构和规划策略才能实现可靠性能？当前基于历史 $\mathcal{H}_t$ 的简单上下文窗口是否足以支撑复杂协作？
- 六大平台的统一评估是否掩盖了平台特异性挑战？不同操作系统和交互范式可能需要对智能体架构进行平台特化调整。



## 原文 PDF

![[paperPDFs/CVPR_2026/MMBench_GUI_A_Unified_Hierarchical_Evaluation_Framework_for_Multi_Platform_GUI_Agents.pdf]]
