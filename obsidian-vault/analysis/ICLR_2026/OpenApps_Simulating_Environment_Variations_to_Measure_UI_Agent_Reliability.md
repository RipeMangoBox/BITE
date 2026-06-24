---
title: "OpenApps: Simulating Environment Variations to Measure UI Agent Reliability"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/OpenApps_Simulating_Environment_Variations_to_Measure_UI_Agent_Reliability.pdf
openreview_forum_id: cj1MAx7lKs
aliases:
- OpenApps
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "通过可配置的YAML文件系统性地改变应用的外观（主题、字体、颜色）和内容（文本、语言、对抗性描述），生成数千种版本，从而可控地测试代理性能对每种变化因素的敏感性。"
primary_logic: "应用变体维度是评估UI代理可靠性的关键盲点；固定应用评估会普遍高估代理的可靠性，且不同代理对不同变体的敏感性具有特异性，需在此维度下重新审视代理行为和部署策略。"
claims:
- "Kimi-VL-3B 的平均成功率在应用变体间从63%剧烈波动至仅4%。"
- "对于 Qwen2.5-VL、Kimi-VL 和 UI-Tars，跨应用变体的任务成功率标准差是固定应用内部的两倍以上。"
- "暗黑主题使纯视觉代理 UI-TARS-1.5-7B 的任务成功率大幅下降，表明外观变化显著影响代理表现。"
- "代理在包含误导性或对抗性内容时更容易产生无效动作（幻觉），如 GPT-4o 在对抗性描述下平均无效动作计数更高。"
---

# OpenApps: Simulating Environment Variations to Measure UI Agent Reliability

> [!tip] 核心洞察
> 应用变体维度是评估UI代理可靠性的关键盲点；固定应用评估会普遍高估代理的可靠性，且不同代理对不同变体的敏感性具有特异性，需在此维度下重新审视代理行为和部署策略。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | OpenApps：模拟环境变化以衡量UI代理可靠性 |
| 英文题名 | OpenApps: Simulating Environment Variations to Measure UI Agent Reliability |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=cj1MAx7lKs); [Project](https://facebookresearch.github.io/OpenApps/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | OPENAPPS |
| Dataset | UI-TARS-1.5-7B on OpenApps with varying screen resolution and appearance, GPT-4o on OpenApps with content variations, Qwen2.5-VL on OpenApps with content variations |

> [!tip] 效果简介
> - UI-TARS-1.5-7B on OpenApps with varying screen resolution and appearance 上，Task Success Rate (pass@1) 为 0.06 (FHD, Dark theme)，对比 0.69 (FHD, Default)，变化 -0.63。
> - GPT-4o on OpenApps with content variations 上，Avg. Invalid Action Count 为 0.07 (adversarial descriptions)，对比 0.00 (default)，变化 +0.07。
> - Qwen2.5-VL on OpenApps with content variations 上，Intent Misunderstanding Rate 为 0.40-0.45 (long/adversarial content)，对比 0.03 (default)，变化 +0.40~0.42。

## 概述

### 问题背景

当前UI代理（UI Agent）的评估范式存在一个关键盲点：几乎所有基准测试都依赖固定的应用副本，忽略了真实世界中应用版本、外观和内容的多样性。用户在日常生活中使用的应用在主题、字体、语言、页面描述等方面千差万别，而现有评估无法衡量代理在这些分布外变体下的可靠性。这导致了一个根本性的问题——**固定应用评估会系统性地高估代理的真实可靠性**。

### 核心贡献

为填补这一空白，本文提出了 **OPENAPPS**，一个轻量级、可配置的开源应用生态系统。OPENAPPS 包含六款功能完整的应用（待办事项、日历、即时通讯、地图、代码编辑器、商店），覆盖常见数字任务场景。其核心创新在于通过可配置的 YAML 文件系统性地改变应用的外观（主题、字体、颜色）和内容（文本、语言、对抗性描述），从而生成数千种应用版本，使研究者能够可控地测试代理性能对每种变化因素的敏感性。

OPENAPPS 在工程上具有显著优势：单个 Python 进程即可运行，内存占用低于 10MB，无需专用模拟器或 GPU，可在普通 CPU 上轻松并行化部署。这与 WebArena 等需要超过 100GB 内存的现有环境形成鲜明对比。

### 方法定位

OPENAPPS 采用强化学习框架组织代理与环境的交互：环境状态 $s_t$ 由 YAML 配置文件初始化，代理接收视觉截图和可访问性树（AX Tree）作为观察 $o_t$，通过 BrowserGym 标准化动作接口发出点击、输入、滚动等人类操作 $a_t$。任务评估基于完整应用状态的精确指标函数 $r = \delta_{[s_t = s_{\mathrm{target}}]}$，确保奖励无法被对抗性副任务操纵。

在方法谱系中，OPENAPPS 定位于**环境模拟与可靠性评估**这一新兴方向。与依赖轨迹模仿或局部状态变更检查的传统评估不同，OPENAPPS 通过完全暴露应用状态和逻辑，为研究者提供了分析代理行为、扩展任务定义的开放平台。

### 关键发现

在超过 10,000 次独立评估中，研究揭示了应用变体对代理可靠性的决定性影响：

- **性能剧烈波动**：Kimi-VL-3B 的平均成功率在不同应用版本间从 63% 骤降至仅 4%，波动幅度超过 50 个百分点。
- **可靠性被系统性高估**：对于 Qwen2.5-VL、Kimi-VL 和 UI-Tars，跨应用变体的任务成功率标准差是固定应用内部的两倍以上，表明仅评估单一版本会严重低估性能波动。
- **外观敏感性存在特异性**：暗黑主题使纯视觉代理 UI-TARS-1.5-7B 的任务成功率大幅下降，而其他代理对此相对鲁棒，说明不同代理对变体因素的敏感性具有模型特异性。
- **对抗性内容诱发幻觉**：当应用包含误导性或对抗性描述时，GPT-4o 等代理产生无效动作（幻觉）的概率显著上升，UI-Tars 在特定变体下的幻觉概率可达默认设置的 5 倍。
- **循环行为受环境影响**：UI-TARS 在暗黑主题下的平均循环次数约为其他设置的 2 倍，表明代理的重复动作倾向与环境变体密切相关。

这些发现共同指向一个核心结论：**应用变体维度是评估 UI 代理可靠性不可或缺的维度**，忽略这一维度将导致对代理部署能力的严重误判。

## 背景与动机

### UI代理的部署瓶颈：从固定环境到分布外变体

当前，多模态大模型驱动的UI代理在固定应用副本上的评估已展现出令人瞩目的能力，能够完成点击、输入、滚动等类人操作。然而，这一评估范式存在一个关键盲点：它假设代理所面对的应用环境是静态且同质的。在真实世界中，同一应用会因版本迭代、用户自定义设置（如暗黑主题、字体大小）、语言本地化、内容动态更新等因素呈现出数千种不同的外观与内容组合。现有基准测试无法回答一个核心问题：**当同一个代理面对同一应用的不同变体时，其可靠性是否依然成立？**

OpenApps的工作揭示了一个严峻的现实：固定应用评估普遍高估了代理的可靠性。以Kimi-VL-3B为例，其在所有任务上的平均成功率在不同应用版本间从63%剧烈波动至仅4%（见摘要）。对于Qwen2.5-VL、Kimi-VL和UI-Tars等主流代理，跨应用变体的任务成功率标准差是固定应用内部的两倍以上（见第4.1节）。这意味着，仅凭单一固定版本的评估结果来推断代理的部署可靠性，将产生系统性的乐观偏差。

### 现有评估环境的局限性

当前UI代理评估环境在设计上存在三个结构性缺口，使其难以支持分布外可靠性度量：

1. **缺乏可控的变异性**：现有基准（如WebArena、AndroidEnv）依赖固定的应用版本或网页快照，无法系统性地改变应用的外观主题、字体、语言或内容描述。研究者无法回答“暗黑主题是否会导致代理失效”或“德语界面是否引发意图误解”这类具体问题。

2. **资源开销与可扩展性矛盾**：基于完整浏览器或Android模拟器的环境通常需要GPU加速、专用容器和超过100GB的内存（如WebArena），这使得大规模并行实验——例如同时测试数千种应用变体——在成本上不可行。

3. **奖励机制易被操纵**：部分环境依赖轨迹模仿或局部状态变更检查来定义任务成功，代理可能通过完成与任务无关的副作用操作而获得奖励，无法保证评估信号的纯净性。

### OpenApps的动机与设计定位

为填补上述缺口，OpenApps提出了一个轻量级、可配置的应用生态系统。其核心动机并非追求最大化的视觉真实感，而是在**真实性与计算效率之间取得平衡**，使得研究者能够在单CPU、不足10MB内存的条件下，生成并部署数千种应用变体（见第3.1节）。这一设计选择使得**应用变体维度**首次成为一个可系统操作的实验变量，从而将UI代理评估从“在固定环境中的绝对性能”推向“在分布外变体下的可靠性”。

OpenApps通过可配置的YAML文件定义应用的初始状态，涵盖外观（主题、字体、颜色）和内容（文本、语言、对抗性描述）两大类变化因素。代理通过BrowserGym标准动作接口与环境交互，任务成功则由基于完整应用状态的精确指标函数判定——只有当环境状态完全达到目标状态时，奖励才为1，否则为0（见第3.3节）。这一设计确保了评估信号的不可操纵性，并为分析代理在不同变体下的失败模式（如循环行为、无效动作幻觉、意图误解）提供了干净的因果归因基础。

## 核心创新

OPENAPPS 的核心创新在于将 UI 代理的评估从“固定应用副本”范式转向“可控应用变体”范式，从而首次系统性地测量代理在分布外环境下的可靠性。这一转变通过三个关键设计实现：**可配置的应用变异性**、**轻量级可扩展架构**，以及**基于完整状态的精确评估机制**。

### 可配置的应用变异性：从固定版本到数千种变体

现有 UI 代理基准（如 WebArena、AndroidWorld）依赖固定的应用版本，无法反映真实世界中应用在主题、字体、语言、内容描述等方面的多样性。OPENAPPS 通过 YAML 配置文件将应用的外观和内容参数化，使研究者能够系统性地改变以下维度：

- **外观变体**：包括亮色主题、暗黑主题、黑白主题，以及挑战性字体（如 Brush Script MT）等。
- **内容变体**：支持多语言（如德语）、长文本描述、误导性描述和对抗性描述。

每个 YAML 文件完整定义了应用的初始状态 $s_0$，通过组合不同的外观和内容参数，可生成数千种应用版本（Section 3.1）。这种设计使得研究者可以**可控地测试代理对每种变化因素的敏感性**，而非仅获得一个聚合的“平均性能”数字。

### 轻量级可扩展架构：从专用模拟器到单 CPU 部署

传统 UI 代理评估环境（如 WebArena）依赖 Docker 容器或专用模拟器，内存需求常超过 100GB，难以并行化大规模实验。OPENAPPS 的每个实例运行在单个 Python 进程中，仅需不到 10MB 内存和单 CPU 即可运行（Section 3.1）。这一架构优势直接支撑了论文中超过 10,000 次独立评估的实验规模（Section 4），使得在普通硬件上并行部署数百个实验成为可能。

### 基于完整状态的精确评估：杜绝奖励操纵

现有评估方法多基于轨迹模仿或局部状态变更检查，代理可能通过完成无关的“副作用任务”来获取奖励。OPENAPPS 将奖励函数定义为对完整应用状态的确定性指示函数：

$$r = \delta_{[s_t = s_{\mathrm{target}}]}$$

即只有当环境状态完全达到目标状态时奖励为 1，否则为 0（Section 3.3）。由于评估器可直接访问应用的完整内部状态（而非仅依赖界面截图），这一机制从根本上杜绝了奖励操纵的可能性，确保任务成功条件必须被**完全满足**。

### 创新点的因果作用

上述三个 changed slots 共同构成了 OPENAPPS 的因果干预逻辑：

1. **应用变异性**（核心 knob）→ 暴露代理在分布外环境下的性能波动，揭示固定应用评估普遍高估可靠性的瓶颈。
2. **轻量级架构**（使能条件）→ 降低大规模变体实验的成本门槛，使系统性可靠性测量成为可能。
3. **精确评估**（效度保障）→ 确保测量的是真正的任务完成能力，而非代理的“投机取巧”。

实验证据直接验证了这一创新逻辑的有效性：对于 Qwen2.5-VL、Kimi-VL 和 UI-Tars，跨应用变体的任务成功率标准差是固定应用内部的两倍以上（Section 4.1），而 Kimi-VL-3B 的平均成功率在不同应用版本间从 63% 剧烈波动至仅 4%（ABSTRACT），充分说明应用变体维度是评估 UI 代理可靠性时不可忽视的关键盲点。

## 整体框架

OPENAPPS 将代理与应用的交互组织为标准强化学习框架。环境状态 $s_t$ 由设计与内容变量定义，并从 YAML 规格文件初始化。在每个时间步 $t$，代理接收来自 OPENAPPS 的观察 $o_t$（视觉截图以及针对支持文本输入的代理提供的 AX Tree 简化文本表示），随后通过 BrowserGym 动作 API 发出动作 $a_t$。动作空间包含人类常用操作（点击、输入、滚动等），直接作用于 OPENAPPS 环境。任务成功与否通过检查底层应用状态 $s_t$ 是否达到目标状态来评估，奖励函数定义为确定性指示函数：

$$r = \delta_{[s_t = s_{\mathrm{target}}]}$$

该框架的核心模块及数据流如下：

**App Configuration (YAML)** — 定义并初始化应用的外观与内容，形成环境初始状态 $s_0$。所有可配置变量（主题、字体、语言、页面文本等）均通过 YAML 文件声明，使得每个应用版本可被完整复现与版本控制。

**Observation Module** — 捕获当前应用界面的视觉截图与浏览器生成的 AX Tree 文本表示，作为代理观察 $o_t$。视觉截图提供给所有代理，AX Tree 仅提供给支持文本输入的代理（如 GPT-4o、Kimi-VL、Qwen2.5-VL），而纯视觉代理（如 UI-TARS）仅接收截图。

**BrowserGym Action API** — 提供标准化的动作接口，代理通过该接口发出动作 $a_t$ 与环境交互。动作集包括 click、type、scroll 等人类常用操作（完整动作集见 Figure 8），确保代理与环境的交互方式与人类用户一致。

**State Manager** — 根据代理动作更新应用状态 $s_t \rightarrow s_{t+1}$，并将环境状态序列化为轻量级 YAML 文件。完整应用状态对评估器可见，但不对代理暴露——代理仅能通过观察间接感知状态变化。

**Task Evaluator** — 通过检查当前状态是否达到目标状态来评估任务完成，并返回奖励。奖励函数直接访问完整应用状态，确保任务成功条件必须完全满足，无法通过完成对抗性副任务来操纵奖励。

整个系统在单个轻量级 Python 进程中运行，内存占用小于 10MB，单 CPU 即可部署。这种设计使得在普通硬件上即可并行运行数千个独立实验，无需专用模拟器或容器环境（如 WebArena 需超过 100GB 内存）。应用状态与逻辑完全以 Python 代码暴露，便于研究者直接分析代理行为或扩展新功能。

## 核心模块与公式推导

### 核心模块

OPENAPPS 的架构围绕五个关键模块展开，构成一个完整的代理-环境交互闭环。

**App Configuration (YAML)** 模块负责定义和初始化应用的外观与内容。所有可配置变量（主题、字体、颜色、语言、页面文本等）均通过 YAML 文件声明，该文件被视作环境的初始状态 $s_0$。这种设计使得单次配置即可生成数千种应用变体，无需修改代码或重新部署。

**Observation Module** 在每一步 $t$ 捕获当前应用界面的视觉截图和 AX Tree 文本表示，作为代理的观察 $o_t$。视觉截图服务于纯视觉代理（如 UI-TARS），而 AX Tree 则为支持文本输入的代理（如 Kimi-VL、GPT-4o）提供结构化的 UI 元素信息。

**BrowserGym Action API** 提供标准化的动作接口。代理通过该接口发出与人类操作一致的动作 $a_t$，包括 click、type、scroll 等，直接与 OPENAPPS 交互。动作空间定义完整，确保了不同代理在统一接口下的可比性。

**State Manager** 根据代理动作将环境状态从 $s_t$ 更新至 $s_{t+1}$，并将状态序列化为轻量级 YAML 文件。每个 OPENAPPS 实例运行于单个 Python 进程，内存占用低于 10MB，单 CPU 即可部署，极大降低了大规模并行实验的门槛。

**Task Evaluator** 通过检查当前状态是否达到目标状态来评估任务完成情况。该模块拥有对完整应用状态的访问权限，而非仅依赖界面截图或局部变更，从而杜绝了奖励操纵的可能性。

### 核心公式

OPENAPPS 的核心评估机制建立在精确的状态匹配之上。奖励函数定义为确定性的指示函数：

$$r = \delta_{[s_t = s_{\mathrm{target}}]}$$

其中 $s_t$ 为当前环境状态，$s_{\mathrm{target}}$ 为目标状态。当且仅当环境状态完全等于目标状态时，奖励为 1；否则为 0。这一设计确保了任务成功条件必须被完全满足，代理无法通过完成无关的副作用任务来获取奖励。

为量化代理在不同粒度下的可靠性，论文引入了基于平均绝对偏差（MAD）的度量。对于某个固定应用版本 $v_k$，其内部可靠性定义为该版本内所有奖励的 MAD：

$$\frac{1}{n} \sum_{r_i \in R_{vk}} \left| r_i - \frac{1}{n} \sum_{r_j \in R_{vk}} r_j \right|$$

其中 $R_{vk}$ 为版本 $v_k$ 下所有任务和随机种子的奖励集合，$n$ 为奖励数量。

跨应用变体的整体可靠性则定义为所有版本奖励集合 $\{R_{v1}, \ldots, R_{vd}\}$ 的 MAD：

$$\frac{1}{nd} \sum_{r_i \in \{R_{v1}, \ldots, R_{vd}\}} \left| r_i - \frac{1}{nd} \sum_{r_j \in \{R_{v1}, \ldots, R_{vd}\}} r_j \right|$$

其中 $d$ 为应用变体数量。实验表明，跨变体的标准差是固定版本内部的两倍以上（Qwen2.5-VL、Kimi-VL、UI-Tars），证实固定应用评估系统性高估了代理的可靠性。

此外，单个应用版本的固定变化因素集合被形式化为 $A_1 = \{f_{1,1}, f_{1,2}, f_{1,3}, \ldots\}$，其中每个 $f$ 代表一个独立的变化维度（如主题、字体、语言）。这一形式化为后续探索多因素交互效应提供了基础框架。

## 实验与分析

### 核心发现：固定应用评估系统性高估代理可靠性

现有UI代理基准测试普遍依赖固定的应用副本，忽略了真实世界中应用版本、外观和内容的多样性。OpenApps通过系统性地模拟这些变异，揭示了一个关键盲区：**固定应用评估会普遍高估代理的可靠性**。

Figure 5 直接对比了两种设置下的任务成功率标准差——固定应用版本内部 vs. 跨所有应用变体。结果显示，对于 Qwen2.5-VL、Kimi-VL 和 UI-Tars，跨应用变体的标准差是固定应用内部的两倍以上。以平均绝对偏差（MAD）为指标的 Figure 10 进一步印证了这一结论：固定版本内的偏差（蓝色）远低于考虑跨版本变异后的整体偏差。

最极端的案例来自 Kimi-VL-3B：其平均成功率在不同应用版本间从 63% 剧烈波动至仅 4%（见 ABSTRACT）。Table 2 列出了跨应用变体成功率波动最大的任务，展示了最高与最低成功率之间的巨大落差。

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_cj1MAx7lKs/figures/009_Table_2.jpg]]
*Table 2: Tasks with the largest fluctuation in success rate across application variations. We show maximum and minimum success rates across app variations*

### 外观变异的影响

Figure 6 和 Table 5 展示了代理在不同外观设置下的性能分化：

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_cj1MAx7lKs/figures/006_Figure_6.jpg]]
*Figure 6: Agent reliability can be low in terms of performance across app variations. Model performance (as measured by the task success rate across random seeds, averaged over all tasks) can differ greatly across appearance and content variations (shown in Figure 7). For example, we notice a sizable drop in the performance of UI-TARS-1.5-7B (a vision-only model) compared to the default when the app has a dark theme, and likewise a drop in the performance of Kimi-VL-A3B-Instruct when the app is in German or contains adversarial page descriptions. The black bars capture the standard deviation of rewards across seeds, averaged over tasks. The task prompt is explicit and fixed. Kimi uses visual and AX t...*

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_cj1MAx7lKs/figures/015_Table_5.jpg]]
*Table 5: Agent reliability can be low in terms of performance across appearance variations. Model performance (as measured by the pass@1 across random seeds averaged over all tasks) can differ greatly across content variations. We report the standard deviation and mean absolute deviation of rewards across seeds, averaged over tasks. The task prompt is explicit and fixed*

- **暗黑主题**对纯视觉代理 UI-TARS-1.5-7B 造成显著冲击，其任务成功率相比默认主题出现大幅下降。Table 11 进一步揭示，UI-TARS 在暗黑主题下的平均循环次数约为其他设置的 2 倍，表明外观变化不仅影响成功率，还改变了代理的行为模式。
- **挑战性字体**（如 Brush Script MT）同样降低了 UI-TARS 的成功率，证明字体是影响视觉代理的一个独立因素。
- 屏幕分辨率与外观存在交互效应：Table 7 显示，在固定内容、仅改变外观时，FHD 分辨率下 UI-TARS 在暗黑主题的成功率仅 0.06，而默认主题为 0.69，降幅达 0.63——高分辨率并非在所有条件下都是优势。

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_cj1MAx7lKs/figures/017_Table_7.jpg]]
*Table 7: Higher HD is no longer always better when we fix the the content and vary the appearance*

### 内容变异的影响

Table 6 汇总了代理在不同内容设置下的性能：

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_cj1MAx7lKs/figures/016_Table_6.jpg]]
*Table 6: Agent reliability can be low in terms of performance across content variations. Model performance (as measured by the pass@1 across random seeds averaged over all tasks) can differ greatly across content variations. We report the standard deviation and mean absolute deviation of rewards across seeds, averaged over tasks. The task prompt is explicit and fixed*

- **语言切换**：Kimi-VL-A3B-Instruct 在应用切换为德语后性能显著下降。
- **对抗性描述**：GPT-4o 在对抗性描述下的平均无效动作计数从默认的 0.00 上升至 0.07（Table 12），说明对抗性内容更易引发幻觉——代理产生了不存在的函数调用和 UI 元素。
- **意图误解**：Qwen2.5-VL 在长文本或对抗性内容下的意图误解率从默认的 0.03 飙升至 0.40–0.45（Table 13），增幅超过 10 倍。

### 变异因素的交互效应

Table 8 展示了外观与内容变体组合时的代理任务成功率。单独德语设置下 UI-TARS 成功率为 0.75，但暗黑主题与德语组合后骤降至 0.11，揭示了变体因素之间存在不可忽视的交互效应——单因素分析可能严重低估真实场景中的性能退化。

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_cj1MAx7lKs/figures/018_Table_8.jpg]]
*Table 8: Variations can interact to form new combinations of app versions. We show agent task success across 15 tasks covering navigation, adding items to todo, and add calendar events*

### 温度参数的消融分析

Figure 9 比较了 Claude 和 Kimi-VL 在不同温度参数（0.5–1.0）下的性能。结果显示，温度在合理范围内对代理性能的影响相对较小，表明观察到的性能波动主要来自环境变异而非采样温度。这一消融实验强化了核心主张：应用变体是代理可靠性波动的主要驱动因素。

### 多步任务的部分成功分析

Table 9 报告了多步任务上的部分成功率。代理在完成增量步骤时表现各异，部分代理即使未能完全完成任务，也能正确执行至少一步操作。这提示在评估代理可靠性时，除了二元成功指标，还应关注渐进完成能力。

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_cj1MAx7lKs/figures/019_Table_9.jpg]]
*Table 9: We show performance on tasks requiring multiple steps across todo, messenger, and calendar. We measure partial reward with respect to whether the agent completed each incremental step in each app. We also show whether at least on step was correctly completed*

### 流行选择的性能差异

Table 10 测试了流行字体、颜色和语言选择下的任务成功率。即使在这些“常见”设置中，代理成功率仍存在显著差异，表明应用变体问题并非仅存在于极端或罕见配置中，而是普遍存在于用户日常可能遇到的环境。

### 失败模式总结

跨实验识别出三类关键失败模式：

1. **循环行为**：代理在特定变体下（如暗黑主题）更易陷入重复动作循环，UI-TARS 的循环次数可达其他设置的 2 倍（Table 11）。
2. **幻觉动作**：对抗性或误导性内容显著增加无效动作的产生率，GPT-4o 在对抗性描述下无效动作计数上升（Table 12）。
3. **意图误解**：长文本或对抗性内容导致代理导航到与任务无关的页面，Qwen2.5-VL 的误解率从 3% 升至 40% 以上（Table 13）。

### 公平性说明

所有评估采用相同的任务提示，指定随机种子，并尽可能使用模型官方推荐的系统提示和配置。代理的输入模态（仅视觉或视觉+AXTree）根据其能力优化，确保公平比较。超过 10,000 次独立评估覆盖了七个代理，为结论提供了充分的统计基础。

### 补充图表

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_cj1MAx7lKs/figures/001_Figure_1.jpg]]
*Figure 1: OPENAPPS can generate thousands of configurable versions of apps. OPENAPPS contains six apps covering common digital tasks with configurable appearance and app data for measuring a new dimension of reliability: across app variations agents are likely to encounter. OPENAPPS can be deployed anywhere Python can run with a single CPU (without specialized hardware, emulators or setup). In the right panel, we see average success rates for the same tasks and agents can fluctuate across app versions, suggesting app variation is a key axis of reliability*

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_cj1MAx7lKs/figures/002_Figure_2.jpg]]
*Figure 2: Screenshots with example appearance variations of all six apps in OPENAPPS: OpenToDo, OpenCalendar, OpenMessenger, OpenMaps, OpenCodeEditor, and OpenShop. Each app is a fully functional Python application with editable state and appearance. OpenApps can be configured via simple YAML files*

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_cj1MAx7lKs/figures/008_Figure_8.jpg]]
*Figure 8: The action set provided through BrowserGym, copied from Appendix A (23)*

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_cj1MAx7lKs/figures/010_Table_3.jpg]]
*Table 3: Tasks with variable success rate across app variations. We show all app variations for each task*

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_cj1MAx7lKs/figures/014_Table_4.jpg]]
*Table 4: Breakdown of model performance by task. Model performance (as measured by pass@1 over random seeds) on all tasks. We report the mean absolute deviation (MAD) and standard deviation (std) of rewards over random seeds. We use the default environment content and appearance, and the task prompt is explicit and fixed. All models use visual and AX tree inputs, with the exception of UI-TARS, which is a UI-visual only model*

## 方法谱系与知识库定位

### 1. 方法定位与基线关系

OPENAPPS 并非提出新的代理架构或训练算法，而是构建了一套**评估基础设施**，用于测量 UI 代理在应用变体下的可靠性。其核心贡献在于揭示了一个被现有基准普遍忽略的评估维度：代理对应用外观和内容变化的敏感性。

在评估方法论层面，OPENAPPS 与现有 UI 代理基准形成以下对比：

- **固定环境基准**（如 WebArena、MiniWoB++）：这些基准使用固定不变的应用版本，代理在单一环境状态下执行任务。OPENAPPS 的实验表明，此类评估会系统性高估代理的可靠性——对于 Qwen2.5-VL、Kimi-VL 和 UI-Tars，跨应用变体的任务成功率标准差是固定应用内部的两倍以上（Figure 5）。这意味着仅凭固定环境下的性能报告无法预测代理在真实世界中面对应用版本变化时的表现。

- **基于轨迹模仿的评估**：部分现有方法通过比较代理轨迹与人类示范来评估性能，但这种机制容易被奖励操纵（reward hacking）。OPENAPPS 采用基于完整应用状态的精确指标函数 $r = \delta_{[s_t = s_{\mathrm{target}}]}$，确保任务成功条件必须完全满足，避免了代理通过完成对抗性副任务来获得奖励的可能性（Section 3.3）。

- **高资源消耗模拟器**：以 WebArena 为代表的环境需要专用模拟器或容器，内存需求超过 100GB。OPENAPPS 通过单 Python 进程运行，内存占用小于 10MB，单 CPU 即可部署，显著降低了大规模并行评估的门槛（Section 3.1）。这种轻量化设计使研究者能够在普通硬件上生成数千种应用版本进行可靠性测试。

### 2. 适用边界与约束条件

OPENAPPS 的设计存在以下适用边界，使用和解读时需注意：

**任务复杂度边界**：当前任务集包含 15 个简单任务，通常仅需 1-3 步操作（如添加待办事项、导航到特定页面）。这些任务被有意设计为简单，以**隔离环境变化对可靠性的影响**，避免任务难度本身成为混淆变量。但这也意味着 OPENAPPS 的评估结论不能直接外推到需要长程规划和多步推理的复杂任务场景。论文作者明确指出，未来可扩展到更复杂、更长周期的任务（Section Limitations）。

**变体因素的独立研究**：实验设计中，外观变体（主题、字体、颜色）和内容变体（语言、对抗性描述）被独立操控和分析。虽然部分实验探索了组合变体（如暗黑主题 + 德语，Table 8），但多因素交互效应的系统性研究仍属开放问题。真实世界中，应用版本、语言、主题等因素往往同时变化，其交互效应可能导致比单因素更剧烈的性能波动。

**完全自主代理假设**：评估聚焦于完全自主的 UI 代理，未涉及人机协同场景。在人类提供实时反馈或纠正的部署模式下，代理对应用变体的敏感性可能呈现不同特征。

**静态状态评估**：奖励函数基于环境状态的完全匹配（$s_t = s_{\mathrm{target}}$），不区分部分完成或中间步骤的正确性。虽然论文提供了部分成功率的分析（Table 9），但主要结论仍基于二元成功指标。

### 3. 局限与已知失败模式

**代理特异性敏感模式**：不同代理对不同变体因素的脆弱性存在显著差异，无法用单一因素解释所有代理的行为退化。例如：
- UI-TARS-1.5-7B（纯视觉模型）在暗黑主题下成功率大幅下降（Figure 6），且在暗黑主题下的平均循环次数约为其他设置的 2 倍（Table 11）。
- Kimi-VL-A3B-Instruct 在应用语言为德语或包含对抗性页面描述时性能退化最严重（Figure 6）。
- GPT-4o 在对抗性描述下产生无效动作（幻觉）的比率显著升高（Table 12）。
- Qwen2.5-VL 在长文本或对抗性内容下的意图误解率从默认的 0.03 升至 0.40-0.45（Table 13）。

这种**特异性**意味着无法通过单一“鲁棒性分数”来概括代理的可靠性，需要针对具体部署场景的变体维度进行针对性评估。

**组合变体的非线性效应**：Table 8 显示，暗黑主题与德语组合可使 UI-TARS 成功率从单独德语时的 0.75 下降至 0.11，表明变体因素之间存在非线性交互。当前实验仅覆盖了有限的组合空间，系统性的组合变体评估仍属空白。

**温度参数的有限影响**：Figure 9 表明，温度参数在合理范围内（0.5-1.0）对代理性能影响相对较小，说明主要性能波动来自环境变化而非采样随机性。这增强了将性能波动归因于环境变体的信心，但也提示当前研究未充分探索极端温度设置下的行为模式。

### 4. 开放问题与后续方向

基于 OPENAPPS 揭示的现象，以下研究方向值得关注：

1. **多因素交互评估框架**：如何在多个应用变体因素交互的情况下系统性地评估代理可靠性？这需要发展能够高效采样组合变体空间、并量化交互效应强度的实验设计方法。

2. **变体感知的训练策略**：什么样的训练数据分布能使代理泛化到特定因素（如字体、颜色、布局）？OPENAPPS 生成的大规模应用变体数据是否可用于训练更鲁棒的 UI 代理？这涉及分布外泛化（OOD generalization）和领域随机化（domain randomization）技术的应用。

3. **在线失败检测与缓解**：在开放世界部署中，如何在线检测和缓解由于应用变体导致的失败模式（如循环行为、幻觉动作、意图误解）？这需要发展实时监控机制，能够在代理进入失败循环或产生无效动作时进行干预。

4. **扩展任务复杂度**：将 OPENAPPS 的任务集扩展到更复杂、更长周期的场景，使其能够作为标准化的 UI 代理可靠性基准。这需要在保持环境可控性的同时增加任务的现实性和难度。

5. **人机协同场景的可靠性**：在人类提供监督或干预的混合自主模式下，应用变体对代理可靠性的影响是否呈现不同模式？人类反馈能否有效补偿代理对特定变体的脆弱性？

## 原文 PDF

![[paperPDFs/ICLR_2026/OpenApps_Simulating_Environment_Variations_to_Measure_UI_Agent_Reliability.pdf]]
