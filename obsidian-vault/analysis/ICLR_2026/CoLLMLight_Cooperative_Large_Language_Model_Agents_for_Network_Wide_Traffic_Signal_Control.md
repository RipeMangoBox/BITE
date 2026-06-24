---
title: "CoLLMLight: Cooperative Large Language Model Agents for Network-Wide Traffic Signal Control"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/CoLLMLight_Cooperative_Large_Language_Model_Agents_for_Network_Wide_Traffic_Signal_Control.pdf
openreview_forum_id: KeJqoEVOeY
aliases:
- CoLLMLight
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "引入异步时空协作推理，将缓慢的协作分析从实时决策中解耦，通过缓存协作指导信号选择，实现兼顾全局优化的实时控制。"
primary_logic: "通过异步架构分离‘慢思考’（合作推理）与‘快决策’（实时信号选择），并结合自适应推理深度优化，在保障响应速度的同时提升网络整体通行效率。"
claims:
- "移除协作推理模块（SR）后，平均行程时间显著增加，尤其在纽约数据集上。"
- "CoLLMLight在四个真实路网数据集上零样本性能全面超越所有基线方法。"
- "自适应推理链优化（AR）显著降低推理token数，并提升控制效果。"
- "New York 1 (零样本) 上 ATT (秒) = 1000.4"
---

# CoLLMLight: Cooperative Large Language Model Agents for Network-Wide Traffic Signal Control

> [!tip] 核心洞察
> 通过异步架构分离‘慢思考’（合作推理）与‘快决策’（实时信号选择），并结合自适应推理深度优化，在保障响应速度的同时提升网络整体通行效率。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | CoLLMLight：面向网络级交通信号控制的协作大语言模型智能体 |
| 英文题名 | CoLLMLight: Cooperative Large Language Model Agents for Network-Wide Traffic Signal Control |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=KeJqoEVOeY) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | CoLLMLight |
| Dataset | New York 1 (零样本), Hangzhou (零样本), Large Manhattan (零样本) |

> [!tip] 效果简介
> - New York 1 (零样本) 上，ATT (秒) 为 1000.4，对比 1289.2 (LLMLight-8B)，变化 -288.8。
> - New York 1 (零样本) 上，AQL 为 1816.8，对比 2297.9 (LLMLight-8B)，变化 -481.1。
> - Hangzhou (零样本) 上，ATT (秒) 为 308.5，对比 312.0 (LLMLight-8B)，变化 -3.5。

## 概述

城市路网交通信号控制的核心挑战在于：各路口信号决策相互耦合，局部最优的独立控制极易引发上游拥堵转移，导致网络整体通行效率恶化。现有基于大语言模型（LLM）的交通信号控制方法——如 **LLMLight**（Lai et al., 2025）——将每个路口视为独立智能体，虽具备零样本泛化能力，却因缺乏路口间协同机制，在网络级拥堵场景下性能受限。

针对这一瓶颈，本文提出 **CoLLMLight**，首个面向网络级交通信号控制的协作式LLM智能体框架。其核心洞察是：将“慢思考”（多步时空协作推理）与“快决策”（实时信号选择）通过异步架构解耦，使智能体既能进行深度协作分析，又不牺牲实时响应能力。具体而言，CoLLMLight包含两大关键设计：

1. **异步协作决策架构**：时空感知协作推理模块（SR）异步执行多步推理，生成条件性协作建议并缓存；实时决策模块（RD）基于当前观测与缓存结果快速选择信号相位。
2. **成本感知协作优化**：通过自适应推理链优化（AR）使LLM根据交通复杂度调整推理深度，并结合PPO强化学习（PR）联合优化推理效用与计算成本。

在四个真实路网数据集上的零样本评估表明，CoLLMLight在所有指标上一致超越传统方法、强化学习基线及独立LLM智能体。以New York 1数据集为例，CoLLMLight-8B相较LLMLight-8B将平均行程时间（ATT）从1289.2秒降至1000.4秒（降幅22.4%），平均排队长度（AQL）从2297.9降至1816.8（降幅20.9%）。消融实验进一步验证：移除协作推理模块后ATT显著上升（New York 1: 1000.4→1155.1），移除自适应推理优化后推理token数增加约52%，同时控制效果恶化。这些结果表明，异步协作架构与成本感知优化是CoLLMLight取得性能突破的关键因素。

## 背景与动机

城市交通信号控制（Traffic Signal Control, TSC）是缓解拥堵、提升通行效率的关键手段。传统方法如 **FixedTime**（Koonce et al., 2008）依赖预设配时方案，缺乏对动态交通流的适应能力；**MaxPressure**（Varaiya, 2013）虽能响应实时压力，但仅考虑局部路口状态，难以实现网络级优化。

近年来，基于强化学习（RL）的方法在TSC中展现出潜力，如 **MPLight**（Chen et al., 2020）、**AttendLight**（Oroojlooy et al., 2020）、**CoLight**（Wei et al., 2019b）等。然而，这些方法面临两个核心瓶颈：一是**泛化能力不足**——在训练路网上表现良好，但迁移到未见过的路网时性能显著下降（Table 1中RL方法在不同数据集上表现不一致）；二是**协作机制受限**——多数方法要么缺乏路口间协作，要么仅通过隐式表征进行有限交互，难以显式建模复杂的时空依赖关系。

大语言模型（LLM）的兴起为TSC带来了新的范式。**LLMLight**（Lai et al., 2025）首次将LLM作为信号控制智能体，利用其语义推理能力实现零样本泛化。但LLMLight将每个路口视为**独立智能体**，各路口仅基于局部观测进行决策，缺乏对上下游交通流的协同考量。如Figure 1所示，独立智能体可能仅清除本地最长队列，却导致上游车辆被阻塞；而协作智能体则能预判上游来车，主动避免拥堵蔓延。

这一独立决策范式在复杂路网中暴露出严重缺陷：当某个路口因局部优化而放行大量车辆时，下游路口若未提前预留通行能力，将迅速形成级联拥堵。**现有基于LLM的TSC方法的核心瓶颈在于缺乏路口间协作机制，导致网络级拥堵风险增大。**

CoLLMLight正是在此背景下提出的首个面向网络级交通信号控制的协作LLM智能体框架。其核心动机是：**在保持LLM零样本泛化优势的同时，引入异步时空协作推理，使各路口智能体能够“预判”相邻路口的交通动态，从而实现兼顾全局优化的实时控制。**

## 核心创新

CoLLMLight 的核心创新在于重新设计了 LLM 智能体在交通信号控制中的协作范式，将“慢思考”与“快决策”解耦，并通过自适应推理优化实现成本可控的网络级协同。具体而言，其创新体现在以下三个关键维度的改变：

### 1. 从独立决策到异步时空协作

**改变点**：现有基于 LLM 的方法（如 **LLMLight**，Lai et al., 2025）将每个路口视为独立智能体，仅基于局部观测进行决策，缺乏路口间协同，导致网络级拥堵风险增大。CoLLMLight 首次引入协作机制，使智能体能够感知并推理上下游交通状态。

**实现机制**：通过 **时空感知协作推理模块（SR）** 实现。SR 模块以异步方式运行，接收包含车道级特征、空间子图关系与历史交互序列的时空上下文，进行多步推理，生成条件性协作建议并缓存。实时决策模块（RD）则基于当前观测和缓存的协作指导快速选择信号相位，无需等待 SR 完成。

**证据支撑**：消融实验（Table 2）表明，移除 SR 模块后平均行程时间显著增加——在纽约 1 数据集上从 1000.4 秒升至 1155.1 秒，验证了协作推理对复杂路网的关键作用。同时，移除空间或时间上下文均导致性能衰减，且同时移除时衰减更严重（Table 9），进一步证实时空协作信息的必要性。

### 2. 从推理-决策耦合到异步解耦架构

**改变点**：传统 LLM 智能体将推理与决策强耦合，单步推理直接输出信号动作，导致响应延迟高，难以满足实时控制需求（通常需在 3-5 秒黄灯时长内完成决策）。

**实现机制**：CoLLMLight 采用异步协作决策架构，将缓慢的协作分析从实时决策中解耦。SR 模块的推理结果被缓存，RD 模块仅需处理当前观测与缓存结果即可做出决策，从而将实时推理延迟控制在可接受范围内。

**证据支撑**：推理延迟对比（Figure 3）显示，CoLLMLight 在所有批量大小下均实现最低延迟，且 RD 模块的推理时间始终低于典型黄灯时长（3-5 秒）。这种解耦设计使系统在保障响应速度的同时，仍能利用深度的时空推理提升网络整体通行效率。

### 3. 从固定推理策略到成本感知自适应优化

**改变点**：现有方法采用固定推理策略，无论交通复杂度高低均执行相同深度的推理，导致算力浪费或推理不足。CoLLMLight 引入自适应推理链优化（AR）与成本感知强化学习（PR）两阶段优化，使 LLM 能够根据交通复杂度动态调整推理深度。

**实现机制**：
- **AR 阶段**：通过筛选最短有效推理链构建 SFT 数据集，使 LLM 学会在简单场景下产生简洁推理、在复杂场景下展开深度分析。
- **PR 阶段**：利用 PPO 和成本感知奖励联合优化 SR 与 RD 模块。SR 奖励综合考虑下游决策收益、推理长度 $L$ 和效用得分 $U$：
  $$R^{\mathrm{SR}} = R^{\mathrm{RD}} \cdot \left[ \beta \left(1 - \frac{L}{L_{\mathrm{max}}}\right) + (1 - \beta) U \right]$$
  其中 $\beta$ 平衡推理简洁性与协作效用。

**证据支撑**：移除 AR 后，推理 token 数在纽约 1 数据集上从 484.2 激增至 738.5（约 52%），在济南数据集上增加约 55%（Table 3），同时 ATT 也显著恶化。同时移除 AR 与 PR 导致性能大幅下降，验证两阶段优化的协同作用。此外，Figure 4 展示了 CoLLMLight 在低车流量下产生更短推理链、在高车流量下增加推理深度的自适应行为，直观证明了自适应机制的有效性。

## 整体框架

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_KeJqoEVOeY/figures/003_Figure_2.jpg]]
*Figure 2: The overview of CoLLMLight framework*

CoLLMLight 提出一种异步协作决策架构，将网络级交通信号控制拆分为两个解耦的核心模块：**时空感知协作推理（Spatiotemporal-Aware Cooperative Reasoning, SR）** 与**实时决策（Real-Time Decision, RD）**。其核心设计理念是“慢思考”与“快决策”分离——SR 模块以较低频率执行多步推理，生成协作指导并缓存；RD 模块则在每个决策时刻结合当前观测与缓存的 SR 结果，快速选择最优信号相位，从而在保障实时响应的同时实现路口间协同。

### 输入构建

每个路口智能体的输入由三类信息构成（见 Figure 2）：

1. **车道级交通观测** $\mathcal{O}_t^i$：对路口 $i$ 所连每条车道 $l$，提取排队车辆数 $n_l^{\mathrm{queue}}$、移动车辆数 $n_l^{\mathrm{move}}$、平均等待时间 $\tau_l$ 和占有率 $\rho_l$，形成特征向量 $\mathbf{o}_t^l$，聚合为 $\mathcal{O}_t^i = \{\mathbf{o}_t^l \mid l \in \mathcal{L}^i\}$。
2. **空间关系子图** $\mathcal{G}^i$：以有向子图表示路口 $i$ 与其邻居路口的拓扑连接关系。
3. **时序交互序列** $\mathcal{T}_t^i$：收集时间窗口 $\Delta t$ 内的历史观测-动作对，捕捉交通流动态演化。

### 模块协作流程

框架的运行流程如下（见 Figure 2）：

- **SR 模块**：将 $\mathcal{O}_t^i$、$\mathcal{G}^i$、$\mathcal{T}_t^i$ 转换为人类可读的文本提示，送入 LLM 执行多步推理。推理过程自适应地激活必要步骤：识别关键车道、分析空间交互模式、挖掘时间演化规律，最终输出包含协作控制建议的推理结果 $\mathbf{Y}_t^{\mathrm{SR}, i}$ 并缓存。
- **RD 模块**：在每个决策时刻 $t$，以当前观测 $\mathcal{O}_t^i$ 和最新缓存的 $\mathbf{Y}^{\mathrm{SR}, i}$ 为上下文，通过 LLM 快速选择信号相位 $a_t^i$。由于 RD 仅需处理当前观测和已完成的推理结果，其延迟可控制在典型黄灯时长（3–5 秒）以内。

### 两阶段优化

为提升协作质量与推理效率，框架引入成本感知的协作优化策略：

1. **自适应推理链优化（Adaptive Reasoning Chain Optimization, AR）**：从交互轨迹中筛选最短有效推理链（即最短 SR 输出足以支撑 RD 做出最优长期决策的 SR–RD 对），构建监督微调数据集，使 LLM 学会根据交通复杂度自适应调整推理深度。
2. **策略精炼（Policy Refinement via RL, PR）**：利用 PPO 在交通环境中联合优化 SR 与 RD 模块。SR 的奖励函数 $R^{\mathrm{SR}} = R^{\mathrm{RD}} \cdot [\beta(1 - L/L_{\max}) + (1-\beta)U]$ 综合考虑下游决策收益、推理长度 $L$ 和效用得分 $U$，引导模型生成简洁且有效的协作推理。

### 关键证据

消融实验验证了架构设计的有效性：移除 SR 模块后，平均行程时间在 New York 1 数据集上从 1000.4 秒升至 1155.1 秒（Table 2），表明协作推理对复杂路网尤为关键；移除 AR 后，SR 推理 token 数在 New York 1 上增加约 52%（484.2 → 738.5），且 ATT 恶化至 1066.3 秒（Table 3），证实自适应推理深度在效率与效果上的双重收益。

## 核心模块与公式推导

CoLLMLight 的核心架构围绕“异步协作决策”与“成本感知优化”两条主线展开，包含五个关键模块。

### 时空信息构建

每个路口智能体在决策时刻 $t$ 需要构建三类时空上下文。

**车道级特征**：对每条车道 $l$，提取四维特征向量：

$$\mathbf{o}_{t}^{l} = \left[ n_{l}^{\mathrm{queue}}, n_{l}^{\mathrm{move}}, \tau_{l}, \rho_{l} \right]$$

其中 $n_{l}^{\mathrm{queue}}$ 为排队车辆数，$n_{l}^{\mathrm{move}}$ 为移动车辆数，$\tau_{l}$ 为平均等待时间，$\rho_{l}$ 为车道占有率。

**路口观测聚合**：路口 $i$ 的交通观测定义为其所有连接车道的特征集合：

$$\mathcal{O}_{t}^{i} = \left\{ \mathbf{o}_{t}^{l} \vert l \in \mathcal{L}^{i} \right\}$$

**空间关系**：以有向子图 $\mathcal{G}^{i} = ( \mathcal{V}^{i}, \mathcal{L}^{i} )$ 表示路口 $i$ 周围的空间关系。

**时间动态**：收集固定时间窗口 $\Delta t$ 内的历史观测与信号动作序列：

$$\mathcal{T}_{t}^{i} = \left\{ \left( \mathcal{O}_{t^{\prime}}^{i}, \mathbf{a}_{t^{\prime}}^{i} \right) \vert t - \Delta t < t^{\prime} < t \right\}$$

### 时空协作推理

SR 模块将上述时空上下文转化为可读提示，由 LLM 执行多步推理，生成协作控制建议：

$$\mathbf{Y}_{t}^{\mathrm{SR}, i} = f_{\mathrm{LLM}}^{\mathrm{SR}} \left( \operatorname{Prompt}( \mathcal{O}_{t}^{i}, \mathcal{G}^{i}, \mathcal{T}_{t}^{i} ) \right)$$

该推理结果被缓存，用于指导下游实时决策。其核心价值在于：将缓慢的协作分析从实时控制回路中解耦。

### 实时决策

RD 模块结合当前观测与缓存的 SR 结果，快速选择最优信号相位：

$$a_{t}^{i} = f_{\mathrm{LLM}}^{\mathrm{RD}} \left( \operatorname{Prompt}( \mathcal{O}_{t}^{i}, \mathbf{Y}^{\mathrm{SR}, i} ) \right)$$

### 自适应推理链优化

AR 阶段通过筛选最短有效推理链构建 SFT 数据集，使 LLM 学会根据场景复杂度调整推理深度。优化目标为最小化负对数似然：

$$\mathcal{L}_{\mathrm{SFT}}(\boldsymbol{\theta}) = - \sum_{(\mathbf{X}, \mathbf{Y}^{*}) \in \mathcal{D}_{\mathrm{SFT}}} \sum_{w=1}^{|\mathbf{Y}^{*}|} \log P_{\pi_{\theta}}(y_{w}^{*} \mid \mathbf{X}, \mathbf{Y}_{<w}^{*})$$

### 策略精炼

PR 阶段利用 PPO 联合优化 SR 与 RD 模块。奖励设计分为两层：

**RD 奖励**：信号选择与长期最优信号一致则 +1，否则 -1。

$$R^{\mathrm{RD}} = \binom{+1, \quad \mathrm{if~} a = a^{*}}{-1, \quad \mathrm{otherwise}}$$

**SR 奖励**：综合考虑下游决策收益、推理长度 $L$ 与效用得分 $U$，通过参数 $\beta$ 平衡推理简洁性与协作质量：

$$R^{\mathrm{SR}} = R^{\mathrm{RD}} \cdot \left[ \beta \left(1 - \frac{L}{L_{\mathrm{max}}}\right) + (1 - \beta) U \right]$$

整体 PPO 优化目标为：

$$J^{\mathrm{PPO}}(\theta) = \hat{\mathbb{E}}_{k} \left[ \min \left( r_{k}(\theta) \hat{A}_{k}, \mathrm{clip}(r_{k}(\theta), 1 - \epsilon, 1 + \epsilon) \hat{A}_{k} \right) \right]$$

### 模块间因果机制

上述模块形成“慢思考—快决策”的异步流水线：SR 模块异步执行多步协作推理并缓存结果；RD 模块基于最新观测和缓存协作指导实时选择信号。AR 与 PR 两阶段优化分别从监督微调和强化学习角度，确保推理深度与交通复杂度相匹配，同时保障协作质量与推理效率的平衡。消融实验验证了这一设计的有效性：移除 SR 模块导致平均行程时间显著增加（New York 1 从 1000.4 升至 1155.1 秒）；移除 AR 则使推理 token 数增加约 52%（New York 1 从 484.2 升至 738.5），同时恶化控制效果。

## 实验与分析

### 零样本性能对比

CoLLMLight在四个真实路网数据集上进行了零样本评估，所有学习方法均在相同的合成数据集（Syn-Train）上训练，确保了训练数据的一致性。Table 1展示了CoLLMLight-8B与各类基线方法的全面对比。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_KeJqoEVOeY/figures/004_Table_1.jpg]]
*Table 1: Zero-shot performance comparison across different datasets (lower is better). Best results are shown in bold. Both CoLLMLight-8B and LLMLight-8B are finetuned from Llama3.1-8B*

**与传统及强化学习方法的对比。** CoLLMLight-8B在所有数据集和所有评价指标（ATT、AWT、AQL）上均取得了最优结果。在规模最大的New York 1数据集上，CoLLMLight-8B的ATT为1000.4秒，AQL为1816.8，相较于最强的RL基线**Advanced-CoLight**（Zhang et al., 2022）分别降低了约22%和18%。值得注意的是，RL方法在不同路网间存在明显的性能不一致性——**Advanced-CoLight**在纽约数据集上表现较好，而**AttendLight**（Oroojlooy et al., 2020）在济南和杭州更优——这暴露了RL方法泛化能力的固有瓶颈。相比之下，CoLLMLight通过显式的语义推理理解交通状态，实现了更稳定的跨场景泛化。

**与LLM基线的对比。** 相较于独立智能体方法**LLMLight-8B**（Lai et al., 2025），CoLLMLight-8B在New York 1上ATT降低了288.8秒（降幅22.4%），AQL降低了481.1（降幅20.9%）。在Large Manhattan路网（Table 11）上，CoLLMLight-8B同样以1008.10秒的ATT显著优于**LEMLight-8B**的1065.6秒。然而，在杭州数据集上，CoLLMLight-8B的ATT（308.5秒）仅比LLMLight-8B（312.0秒）降低3.5秒，提升幅度有限。这表明协作推理的收益与路网复杂度正相关——路网越复杂、路口间耦合越强，协作带来的增益越显著。

### 消融实验

**协作推理模块（SR）的必要性。** Table 2对比了三种SR设计：异步SR（Async SR）、同步SR（Sync SR）和移除SR（w/o SR）。移除SR后，New York 1的ATT从1000.4秒骤升至1155.1秒（增加15.4%），New York 2从1345.1秒升至1477.3秒（增加9.8%），验证了协作推理对缓解网络级拥堵的关键作用。同步SR虽然也提供了协作信息，但由于推理延迟与决策强耦合，在复杂路网下性能弱于异步SR。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_KeJqoEVOeY/figures/006_Table_2.jpg]]
*Table 2: Impact of SR design on average travel time (in seconds) across four datasets*

**自适应推理链优化（AR）的效果。** Table 3显示，移除AR后SR模块的推理token数显著增加——New York 1从484.2增至738.5（增加52.5%），济南从约390增至约605（增加55.1%）——同时ATT从1000.4秒恶化至1066.3秒。这表明AR不仅有效压缩了推理成本，还通过筛选最短有效推理链提升了控制质量。同时移除AR与PR（w/o Both）导致性能进一步下降，验证了两阶段优化策略的协同作用。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_KeJqoEVOeY/figures/007_Table_3.jpg]]
*Table 3: Ablation study of optimization stages on average travel time (ATT, in seconds) and reasoning length (Token) of the SR module across New York 1 and Jinan*

**时空上下文的贡献。** Table 9的消融显示，单独移除空间上下文或时间上下文均导致ATT上升，且同时移除两者时性能衰减更为严重，证实了时空联合建模对协作推理的必要性。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_KeJqoEVOeY/figures/023_Table_9.jpg]]
*Table 9: Ablation study results (ATT, lower is better)*

### 推理效率分析

Figure 3展示了8B规模LLM在不同批处理大小下的推理延迟对比。CoLLMLight的RD模块延迟在所有批处理配置下均为最低，且保持在典型黄灯时长（3-5秒）以内，满足实时控制需求。SR模块的异步执行使其推理耗时不影响实时决策，这验证了异步解耦架构设计的有效性。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_KeJqoEVOeY/figures/005_Figure_3.jpg]]
*Figure 3: Inference time comparison of 8B-scale LLMs over batch sizes b $\in \{$ 1 , 5 , 1 0 $\}$*

Figure 4进一步展示了SR模块的自适应推理行为：在低车流量场景下，SR生成的推理链较短；随着车流量增加，推理token数自适应增长，体现了模型根据交通复杂度动态调整推理深度的能力。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_KeJqoEVOeY/figures/009_Figure_4.jpg]]
*Figure 4: SR token length across traffic conditions with different vehicle counts*

### 鲁棒性测试

Table 4评估了CoLLMLight在两类退化场景下的鲁棒性：SR缓存陈旧（Stale SR）和通信故障（Communication Failure）。在New York 1上，Stale SR场景的ATT仅从1000.4秒升至1017.7秒（增加1.7%），通信故障场景升至1028.1秒（增加2.8%）。性能衰减幅度较小，原因在于RD模块基于实时观测独立决策，不完全依赖SR缓存，而SR模块基于历史状态推理，对间歇性通信问题具有天然容错性。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_KeJqoEVOeY/figures/010_Table_4.jpg]]
*Table 4: Robustness test of CoLLMLight (ATT, lower is better)*

### 局限性与失败模式

尽管CoLLMLight在零样本场景下表现优异，但存在以下局限：（1）仅支持离散的预设信号相位，无法处理连续配时优化；（2）协作范围仅延伸至邻居路口（单跳），在超长距离交通流协调场景下可能不足；（3）LLM推理仍增加了部署成本和算力需求，在极端资源受限环境下存在挑战。此外，杭州数据集上协作增益有限的现象提示，在路网规模较小或路口间耦合较弱时，协作推理的边际收益可能不足以覆盖其额外开销。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_KeJqoEVOeY/figures/011_Table_5.jpg]]
*Table 5: Statistics of datasets*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_KeJqoEVOeY/figures/019_Table_6.jpg]]
*Table 6: Comparative Performance of Learning-based Methods at Syn-Train*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_KeJqoEVOeY/figures/020_Table_7.jpg]]

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_KeJqoEVOeY/figures/021_Table_8.jpg]]
*Table 8: Zero-shot performance comparison across different datasets (lower is better). Best results are shown in bold. The lower block shows LLMs evaluated with the CoLLMLight agent framework*

## 方法谱系与知识库定位

### 1. 与现有基线的谱系关系

CoLLMLight 的提出建立在交通信号控制（TSC）的两个主要技术谱系之上：传统的交通工程方法与基于学习的控制方法，并直接回应了最新涌现的基于大语言模型（LLM）的智能体方法的根本缺陷。

**传统交通工程方法**构成了控制策略的下界。**FixedTime**（Koonce et al., 2008）依赖预设的固定周期和相位配时，完全无法适应动态交通流。**MaxPressure**（Varaiya, 2013）引入实时排队信息，通过最小化相邻车道压力差来动态选择相位，但仅考虑局部路口信息，缺乏网络级协同视野。这两类方法在表1中均表现出显著更高的平均行程时间（ATT），构成了CoLLMLight超越的基准。

**基于强化学习的方法**代表了深度学习时代的控制范式。这些方法利用神经网络从高维交通状态中学习控制策略，但面临严重的泛化瓶颈。**MPLight**（Chen et al., 2020）、**AttendLight**（Oroojlooy et al., 2020）、**PressLight**（Wei et al., 2019a）等独立RL智能体将每个路口视为独立决策单元，通过局部观测学习信号选择，但完全忽略路口间的交通流交互。**CoLight**（Wei et al., 2019b）及其改进版本 **Efficient-CoLight**（Wu et al., 2021）、**Advanced-CoLight**（Zhang et al., 2022）引入了图注意力网络来建模相邻路口间的空间关系，但其协同机制被隐式编码在模型参数中，缺乏显式的语义推理能力。这导致RL方法在不同路网拓扑间的零样本迁移性能极不稳定——如表1所示，Advanced-CoLight在纽约数据集表现较好，而AttendLight在济南和杭州更优，这种不一致性暴露了隐式协同的脆弱性。

**基于LLM的智能体方法**是CoLLMLight的直接前身。**LLMLight**（Lai et al., 2025）首次将LLM引入交通信号控制，利用LLM的语义理解和推理能力，将交通状态转化为自然语言提示，使LLM直接输出信号相位。LLMLight的核心局限在于将每个路口视为独立智能体，各路口仅基于局部观测进行推理和决策，完全缺乏路口间的协同机制。这一设计瓶颈直接导致了网络级拥堵风险——当某个路口仅根据自身排队长度选择信号时，可能将车辆推向下游已接近饱和的路口，引发级联拥堵。CoLLMLight正是在LLMLight的基础上，通过引入异步时空协作推理（SR）和成本感知优化，将独立智能体范式升级为协作智能体框架，填补了这一关键空白。

### 2. 核心机制创新与适用边界

CoLLMLight的方法贡献可分解为三个相互耦合的机制创新，每个创新都针对特定瓶颈，并具有明确的适用条件。

**异步协作决策架构**是本工作的核心结构创新。传统方法（包括LLMLight）将推理与决策强耦合：智能体在每一步都需要完成完整的交通状态理解后再输出动作。CoLLMLight通过将系统解耦为“慢思考”的时空协作推理模块（SR）和“快决策”的实时决策模块（RD），实现了协作深度与响应速度的分离。SR模块异步执行多步推理，识别关键车道、分析上下游交通流的空间交互和时间演化模式，并将推理结果缓存为协作指导；RD模块则仅基于当前观测和缓存的SR结果快速选择信号相位。这一架构的关键适用条件是：交通环境的动态变化速度必须慢于SR模块的更新频率，否则缓存的协作指导将失效。表4的鲁棒性测试验证了这一点——在“Stale SR”场景（SR缓存未及时更新）下，ATT从1000.4升至1017.7（纽约1），性能衰减轻微，说明协作指导具有一定的时效容忍度。

**自适应推理链优化（AR）**解决了固定推理策略的冗余问题。LLM推理的token长度直接决定计算成本和延迟。AR通过筛选最短有效推理链构建SFT数据集，使LLM学会根据交通复杂度动态调整推理深度。如图4所示，在低车流量场景下，CoLLMLight产生更短的推理链；随着车流量增加，推理token数自适应增长。这一机制的适用边界在于：交通复杂度的变化必须能被车道级特征（排队车辆数、移动车辆数、平均等待时间、占有率）充分捕获，否则LLM可能无法准确判断所需推理深度。

**成本感知强化学习（PR）**进一步联合优化SR和RD模块。PR的核心创新在于SR奖励函数的设计：$R^{\mathrm{SR}} = R^{\mathrm{RD}} \cdot [ \beta (1 - L/L_{\mathrm{max}}) + (1 - \beta) U ]$，其中$R^{\mathrm{RD}}$是下游决策收益，$L$是推理长度，$U$是推理效用得分。这一设计显式惩罚冗长但效用低的推理，鼓励LLM在协作质量和计算成本间取得平衡。参数$\beta$控制简洁性与效用性的权衡，其取值需要根据部署环境的算力约束进行调整，目前缺乏自适应调整机制。

### 3. 局限性与开放问题

CoLLMLight存在三个明确的局限性，每个局限性都指向未来的研究方向。

**动作空间的离散性限制**。CoLLMLight仅支持从预设的离散信号相位集合中选择动作（如东西直行、南北左转等），未涉及连续配时优化（如绿灯时长调节）。这意味着该方法无法处理需要精细化时间分配的场景，例如主路与支路流量极度不均衡时的动态绿信比调整。将协作推理框架扩展到连续动作空间是一个重要的开放方向。

**协作范围的单跳限制**。当前的协作推理仅延伸到邻居路口（单跳空间子图），未探索更大范围的协同。在超长距离的交通流协调场景中（如城市快速路的绿波带控制），单跳协作可能不足以协调相距较远但交通流高度耦合的路口群。能否将协作推理扩展为多跳（multi-hop），并设计相应的稀疏注意力机制以控制计算复杂度，是一个待探索的问题。

**LLM推理的部署成本**。尽管异步架构将RD延迟控制在典型黄灯时长（3-5秒）以内（图3），但LLM推理仍引入了额外的算力需求和硬件成本。在资源受限的边缘计算环境下，部署8B规模的LLM可能不切实际。探索更小规模模型的协作能力、或设计模型蒸馏方案，是推动该方法实际落地的关键。此外，成本感知优化中的$\beta$参数目前为固定值，能否根据实时交通压力或系统负载自适应调整，也是一个值得研究的问题。

**多模态信息融合的缺失**。当前CoLLMLight仅依赖结构化的车道级交通特征（排队数、等待时间等），未能利用视觉信息（如交叉口摄像头画面）或语义信息（如事故报告、天气状况）。这些多模态信息可能显著提升LLM对异常交通场景的理解和泛化能力，但如何有效融合异构信息并控制提示长度，仍是一个开放挑战。

## 原文 PDF

![[paperPDFs/ICLR_2026/CoLLMLight_Cooperative_Large_Language_Model_Agents_for_Network_Wide_Traffic_Signal_Control.pdf]]
