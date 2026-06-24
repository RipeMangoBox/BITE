---
title: "From Assumptions to Actions: Turning LLM Reasoning into Uncertainty-Aware Planning for Embodied Agents"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/From_Assumptions_to_Actions_Turning_LLM_Reasoning_into_Uncertainty_Aware_Planning_for_Embodied_Agents.pdf
openreview_forum_id: GODFBZhFcX
aliases:
- PPCE
- FAATLRIUAPEA
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "将 LLM 推理链路中零散的隐含假设提取并组织成一个显式的决策树（每个内部节点为一个环境假设，叶子为行动），然后通过一个评估器根据场景可能性（scenario likelihood）、目标条件增益（conditional gain）和执行成本（execution cost）对每条路径进行评分，以此引导理性行动选择，从而在无需频繁通信的前提下实现不确定性感知..."
primary_logic: "将 LLM 推理中潜在、非结构化的环境假设转化为结构化的决策树，使智能体能够联合评估多个竞争假设并选择预期效用（$U(S,a)$）最高的行动，从而将不确定性处理从「通信为中心」的协调范式转变为以智能体自身信念状态为中心的结构化推理。"
claims:
- "PCE 在两个多智能体基准 C‑WAH 和 TDW‑MAT 上，以 GPT‑4o mini、GPT‑OSS:20B 和 Gemma3:4B 三个异构 LLM 为骨干，均一致地优于 CoELA、REVECA、CaPo、CoTS 等通信密集的基线方法，在成功率与任务效率上取得最优。"
- "消融实验表明，去除 PCE 的任一模块（Planner、Composer、Evaluator）均导致性能下降，其中移除 Planner 使 Total Steps 从 42.76 上升至 56.46；移除 Composer 或 Evaluator 亦使步骤数增加且决策质量降低，证实三个模块对不确定性感知规划缺一不可。"
- "LLM 容量缩放（Gemma3:4B→12B→27B）或推理深度提升（GPT‑OSS:20B Low→Medium→High）对无显式不确定性处理的 ‘Planner only’ 变体仅带来有限增益，而 PCE 在所有缩放级别下均保持显著领先，说明结构化不确定性处理的收益独立于且累加于模型规模与推理深度。"
- "用户研究表明，PCE 产生的通信模式在人类伙伴感知到的效率、可信度、有用性和适当性方面均显著优于 ‘无通信’ 与 ‘始终通信’ 两种极端策略，且实际总步数更低（PCE 72.42 vs. Com always 114.25）。"
---

# From Assumptions to Actions: Turning LLM Reasoning into Uncertainty-Aware Planning for Embodied Agents

> [!tip] 核心洞察
> 将 LLM 推理中潜在、非结构化的环境假设转化为结构化的决策树，使智能体能够联合评估多个竞争假设并选择预期效用（$U(S,a)$）最高的行动，从而将不确定性处理从「通信为中心」的协调范式转变为以智能体自身信念状态为中心的结构化推理。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 从假设到行动：将LLM推理转化为具身智能体的不确定性感知规划 |
| 英文题名 | From Assumptions to Actions: Turning LLM Reasoning into Uncertainty-Aware Planning for Embodied Agents |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=GODFBZhFcX) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | PCE (Planner-Composer-Evaluator) |
| Dataset | C-WAH, TDW-MAT |

> [!tip] 效果简介
> - C-WAH 上，Total Steps ↓ 为 42.76，对比 60.40 (CoELA) / 46.80 (REVECA)，变化 PCE 比最好基线 REVECA 少 4.04 步，比 CoELA 少 17.64 步。
> - C-WAH 上，Comm (通信动作数) 为 1.70，对比 9.88 (CoELA) / 6.00 (REVECA)，变化 PCE 的通信量远低于所有基线。
> - TDW-MAT 上，Total ↑ (运输完成比例 %) 为 87.50，对比 62.50 (CoELA) / 81.25 (REVECA)，变化 PCE 比最好基线 REVECA 高 6.25 个百分点。

## 概述

在部分可观测、去中心化的多智能体协作环境中，现有方法普遍依赖频繁的代理间通信来缓解环境不确定性。这一范式不仅消耗大量 token 与时间，在涉及人类协作者时还会破坏工作流程的连贯性。更深层的问题在于：LLM 在推理过程中自发产生的关于环境不确定性的**隐含假设**始终未能被显式聚合与系统评估，导致智能体无法有效比较和协调多个竞争性假设，从而限制了规划质量。

本文提出 **PCE（Planner-Composer-Evaluator）**，一种将 LLM 推理转化为不确定性感知规划的方法。其核心机制是：从 LLM 的推理链路中提取零散的隐含假设，组织成一颗**显式决策树**（内部节点为环境假设，叶子为候选行动），再由评估器根据场景可能性、目标条件增益和执行成本对每条路径进行评分，引导理性行动选择。这一设计将不确定性处理从“通信为中心”的协调范式转变为以智能体自身信念状态为中心的结构化推理。

在两个多智能体基准 **C‑WAH** 和 **TDW‑MAT** 上，PCE 以 GPT‑4o mini、GPT‑OSS:20B 和 Gemma3:4B 三个异构 LLM 为骨干，均一致优于 **CoELA**（Zhang et al., 2024b）、**REVECA**（Seo et al., 2025）、**CaPo**（Liu et al., 2025）、**CoTS**（Zu et al., 2025）等通信密集型基线方法。具体而言，在 C‑WAH 上，PCE 的总步数（Total Steps）为 42.76，比最优基线 REVECA 减少 4.04 步，通信动作数仅为 1.70，远低于基线的 6.00–9.88；在 TDW‑MAT 上，PCE 的总运输完成比例达 87.50%，较最优基线 REVECA 提升 6.25 个百分点。消融实验进一步证实，Planner、Composer、Evaluator 三个模块缺一不可：移除任一模块均导致性能显著下降，其中移除 Planner 使总步数从 42.76 骤升至 56.46。LLM 容量缩放实验表明，结构化不确定性处理的收益独立于且可叠加于模型规模与推理深度的提升。用户研究亦显示，PCE 产生的通信模式在效率、可信度、有用性和适当性等维度上均显著优于“无通信”与“始终通信”两种极端策略。

## 背景与动机

在部分可观测、去中心化控制的多智能体协作场景中，智能体仅能获取局部环境信息与协作者的稀疏消息，却需要协同完成搬运、搜索等联合任务。这一设定天然将智能体置于深层不确定性之中：目标物体可能被遮挡、协作者可能正在执行冲突的子任务、环境状态可能因他人行动而改变。现有方法普遍将**频繁的代理间通信**作为缓解不确定性的首要手段——智能体通过持续对话交换状态、验证计划、迭代对齐，典型代表包括 **CoELA**（Zhang et al., 2024b）、**REVECA**（Seo et al., 2025）、**CaPo**（Liu et al., 2025）和 **CoTS**（Zu et al., 2025）。然而，这种“通信为中心”的范式存在两个根本性缺陷。

第一，**通信成本高昂且破坏工作流**。密集的消息交换不仅消耗大量 token 和推理时间，在涉及人类协作者时还会打断其自然工作节奏，降低整体效率。实验表明，通信密集型基线在 C‑WAH 基准上的通信动作数可达 PCE 的 3.5 至 5.8 倍（CoELA 9.88 vs. PCE 1.70，Table 1），而用户研究进一步证实，人类伙伴对“始终通信”策略的感知效率、可信度和适当性评分均显著低于 PCE（Figure 4）。

第二，也是更本质的瓶颈：**LLM 在推理过程中自发产生的隐含环境假设未被显式聚合与系统评估**。当 LLM 规划器生成推理链时，其内部实际上已经对“冰箱里是否有牛奶”“协作者是否已检查过厨房”等不确定性因素做出了隐含假设，但这些假设零散地嵌入推理文本中，既未经过全局比较，也未接受任何定量评估。这导致智能体无法有效权衡多个竞争性假设，只能基于推理链中偶然浮现的单一假设采取行动，从而在假设错误时陷入低效甚至错误的执行路径。

本文的核心动机正是将不确定性处理从“通信为中心”的协调范式转变为**以智能体自身信念状态为中心的结构化推理**。具体而言，我们提出将 LLM 推理链路中潜在、非结构化的环境假设提取并组织为显式的决策树——每个内部节点对应一个环境假设，叶子对应行动——然后通过一个评估器根据场景可能性、目标条件增益和执行成本对每条路径进行评分，引导理性行动选择。这一设计使得智能体能够在无需频繁通信的前提下，联合评估多个竞争假设并选择预期效用最高的行动，从而在保持低通信开销的同时显著提升规划质量。

## 核心创新

PCE 的核心创新在于将部分可观测多智能体协作中的不确定性处理范式，从**以通信为中心的协调**转变为**以智能体自身信念状态为中心的结构化推理**。具体而言，它通过三个相互关联的机制设计（changed slots）实现了这一转变：

### 1. 不确定性处理机制：从通信消歧到结构化信念评估

现有通信密集型基线（如 **CoELA**（Zhang et al., 2024b）、**REVECA**（Seo et al., 2025）、**CaPo**（Liu et al., 2025））将代理间自然语言对话作为缓解不确定性的首要手段——通过频繁交换状态信息、验证计划并迭代对齐来消歧。这一策略在涉及人类协作者时会破坏工作流程，且消耗大量 token 和时间。

PCE 则从根本上改变了这一机制：它将 LLM 推理链中自发产生但原本零散、隐式的环境假设**显式提取并聚合为决策树**，然后通过场景可能性（scenario likelihood）、目标条件增益（conditional gain）和执行成本（execution cost）三个维度进行联合评估。通信在此框架中被降级为一种**原子行动**，仅在评估器判定其预期效用高于物理行动时才被选取。这一转变使得 PCE 在 C‑WAH 上的通信动作数仅为 1.70，远低于 CoELA 的 9.88 和 REVECA 的 6.00（Table 1, GPT‑4o mini），同时任务完成步数更少。

### 2. 规划模块结构：从单一推理到三阶段流水线

基线方法通常采用单一规划器（含 CoT 推理）或迭代式辩论/多计划树搜索（如 **CoTS**（Zu et al., 2025）的蒙特卡洛树搜索）。PCE 则将规划模块重构为 **Planner → Composer → Evaluator** 三阶段流水线（Figure 1, Figure 2）：

- **Planner** 接收目标、进度、消息日志等，输出推理链与初始候选行动，每个候选行动往往隐含单一环境假设；
- **Composer** 从 Planner 的推理链中提取不确定性假设，自顶向下构建决策树（内部节点为假设，叶子为行动），并按不确定性降低程度和行动影响力排序展开分支；
- **Evaluator** 对每条根到叶路径计算最终效用得分 $U(S, a) = \mathbb{E}[\mathrm{gain}] - \lambda C(a)$，其中 $\mathbb{E}[\mathrm{gain}] = \mathscr{L}(S) \cdot \mathscr{G}(a)$，$C(a) = \alpha d(a) \mathbf{1}\{\mathrm{move}(a)\} + \beta \ell(a) \mathbf{1}\{\mathrm{comm}(a)\}$，并按得分排序选择最优行动。

消融实验（Table 3）证实了这一流水线结构的不可分割性：移除 Planner 使 Total Steps 从 42.76 升至 56.46；移除 Composer 升至 46.82；移除 Evaluator 升至 47.34，表明三个阶段分别负责场景探索、假设聚合与定量评估，缺一不可。

### 3. 假设的利用方式：从隐式局部推理到显式全局权衡

在基线方法中，LLM 推理链中出现的环境假设（如“食物可能在客厅”）仅作为局部、隐式的中间步骤存在，不会被系统性地聚合或进行冲突消解。PCE 则将这些假设**显式枚举并二分分支**（True/False），构建多假设场景树，使智能体能够联合评估多个竞争假设并选择预期效用最高的行动。这一机制使得不确定性处理从“通信为中心”的协调范式转变为以智能体自身信念状态为中心的结构化推理。

值得注意的是，LLM 容量缩放实验（Figure 3）表明：仅增大模型容量（Gemma3:4B→12B→27B）或加深推理深度（GPT‑OSS:20B Low→Medium→High）对无显式不确定性处理的“Planner only”变体仅带来有限增益，而 PCE 在所有缩放级别下均保持显著领先。这说明**结构化不确定性处理的收益独立于且累加于模型规模与推理深度的缩放**，是 PCE 优势的核心来源。

## 整体框架

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_GODFBZhFcX/figures/002_Figure_2.jpg]]
*Figure 2: Flow from reasoning trace to action selection. (a) The Planner produces a reasoning trace. (b) The Composer extracts hypotheses from the trace, structures them into a decision tree, and, when needed, generates new assumptions and communication actions to expand unexplored branches. (c) The Evaluator scores each path; The highlighted path indicates the scenario whose leaf node achieves the maximum score (U), determining the agent’s final selected action*

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_GODFBZhFcX/figures/001_Figure_1.jpg]]
*Figure 1: PCE employs a modular architecture with a Planner, Composer, and Evaluator pipeline for planning*

PCE 采用模块化流水线架构，将规划过程解耦为 **Planner → Composer → Evaluator** 三阶段推理，并在外围辅以感知、记忆、通信与执行模块，形成闭环控制（Figure 1）。

**感知与记忆层**：Observation Module 将原始环境信号与协作者消息转化为结构化感知信息（对象名称/ID、位置、房间、交互关系、容器遮挡状态等），Memory Module 统一维护静态信息（任务目标、技能库）与动态信息（任务进度、消息日志、动作历史），其中动作历史与消息日志分别按窗口 $K_{\text{action}}$ 和 $K_{\text{message}}$ 截断以防止无限增长。

**规划核心流水线**：在每一步决策中，Planner 接收目标、进度、消息日志与可用动作列表，输出自然语言推理链及一组初始候选行动，每个候选行动往往隐含单一环境假设。Composer 从推理链中提取不确定性假设，自顶向下构建决策树——内部节点为二值化假设（True/False），叶子为对应路径下的行动；当推理链未覆盖关键分支时，Composer 可自主生成新假设并纳入树结构，树深度受超参数 $D$ 限制。Evaluator 对每条根到叶路径估计三项指标：场景可能性 $\mathscr{L}(S)$（该路径上所有假设同时成立的概率）、条件增益 $\mathscr{G}(a)$（在该场景下行动对目标的推进程度）以及执行成本 $C(a)$，最终按效用得分 $U(S, a) = \mathbb{E}[\text{gain}] - \lambda C(a)$ 排序，选择得分最高的叶子行动输出。

**行动执行层**：若选中物理行动（移动、抓取、运输等），Execution Module 将其翻译为低层 API 调用，使用 A* 搜索规划路径；若选中通信行动，Communication Module 发送或回复协作者消息，消息传递存在一步延迟。通信在此框架中被降级为原子行动，仅在预期效用高于物理行动时被选取，而非作为默认的消歧手段。

这一流水线的核心创新在于将 LLM 推理中零散、非结构化的隐含假设转化为显式决策树，使智能体能够在自身信念空间内联合评估多个竞争假设并选择预期效用最高的行动，从而在无需频繁通信的前提下实现不确定性感知规划。

## 核心模块与公式推导

PCE 将单次规划拆解为 **Planner → Composer → Evaluator** 三阶段流水线，使隐含于 LLM 推理链中的环境不确定性假设被显式提取、结构化并量化评估。图 1 展示了这一模块化架构，图 2 则给出了从推理链到行动选择的完整流程示意。

### Planner：推理链与候选行动生成

Planner 接收目标、任务进度、消息日志及可用动作列表，输出一条推理链（reasoning trace）与若干候选行动。每个候选行动通常隐含一个单一的环境假设——例如“客厅里有食物”或“冰箱门是开着的”——但这些假设在原始推理链中仅以非结构化文本形式存在，未被显式标注或比较。Planner 的 Prompt 模板见原文 Figure 8。

### Composer：假设提取与决策树构建

Composer 是 PCE 的核心创新模块。它从 Planner 产生的推理链中提取不确定性假设，并以自顶向下的方式构建一棵显式决策树：每个**内部节点**为一个二分假设（True/False），每条**根到叶路径**对应一个累积假设场景 $S$，**叶子节点**为该场景下应执行的行动 $a$。

构建过程遵循局部排序策略：在每个节点处，Composer 优先选择最能降低不确定性且对后续行动选择影响最大的假设进行分支。当推理链中可提取的假设不足以覆盖关键不确定性时，Composer 会自主生成新假设并插入通信动作以请求缺失信息。树深度受超参数 $D$ 限制（默认 $D=3$），或当无更多有意义的假设可分支时提前终止。Composer 的 Prompt 模板见原文 Figure 9。

### Evaluator：基于预期效用的路径评分

Evaluator 对决策树中每条根到叶路径进行量化评分，综合三个维度：

- **场景可能性** $\mathscr{L}(S)$：场景 $S$ 为真的估计概率。
- **条件增益** $\mathscr{G}(a)$：在场景 $S$ 成立的条件下，执行行动 $a$ 对目标推进的程度。
- **执行成本** $C(a)$：行动 $a$ 的代价，分解为物理移动与通信两部分。

**公式 1：预期增益**
$$\mathbb{E}[\mathrm{gain}] = \mathscr{L}(S) \cdot \mathscr{G}(a)$$

预期增益是场景可能性与条件增益的乘积，反映“该场景成真时该行动能带来的期望收益”。

**公式 2：执行成本**
$$C(a) = \alpha \, d(a) \, \mathbf{1}\{\mathrm{move}(a)\} + \beta \, \ell(a) \, \mathbf{1}\{\mathrm{comm}(a)\}$$

执行成本将物理移动距离 $d(a)$ 与通信消息长度 $\ell(a)$ 分别通过指示函数 $\mathbf{1}\{\cdot\}$ 互斥地激活：当行动为移动时仅计算距离成本，为通信时仅计算消息长度成本。$\alpha, \beta > 0$ 为缩放常数（默认均为 1）。

**公式 3：最终效用得分**
$$U(S, a) = \mathbb{E}[\mathrm{gain}] - \lambda \, C(a)$$

最终得分从预期增益中减去经成本敏感系数 $\lambda > 0$（默认 $\lambda=1$）加权的执行成本惩罚。Evaluator 对所有路径计算 $U(S,a)$ 后，选择得分最高的叶子节点对应的行动作为最终输出。Evaluator 的 Prompt 模板及评分标准见原文 Figure 10。

### 辅助模块

- **Observation Module**：将原始环境信号与协作者消息转化为结构化感知信息（对象名称/ID、位置、房间、容器遮挡状态等）。
- **Memory Module**：统一存储静态信息（目标、技能库）与动态信息（任务进度、消息日志、动作历史），按窗口 $K_{\text{action}}$ 和 $K_{\text{message}}$ 截断以防止无限增长。
- **Communication Module**：当规划模块选择通信动作时，发送/回复协作者消息（消息含一步延迟）。
- **Execution Module**：将物理动作（移动、抓取、运输等）翻译为低层 API 调用，使用 A* 搜索规划路径。

### 与基线方法的结构性差异

| 维度 | 通信中心基线（CoELA, REVECA, CaPo, CoTS） | PCE |
|------|------|-----|
| 不确定性处理 | 依赖频繁代理间通信验证计划、交换信息 | 将隐含假设提取为显式决策树，通过 likelihood–gain–cost 联合评估 |
| 规划结构 | 单一规划器 + CoT 推理，或迭代辩论/多计划树搜索 | Planner → Composer → Evaluator 三阶段流水线 |
| 假设利用 | 仅在推理链中局部、隐式出现，未全局聚合 | 显式枚举并二分分支，按不确定性降低与行动影响力排序展开 |
| 通信定位 | 作为首要消歧手段，以对话驱动搜索 | 降级为原子行动，仅在 $U(S,a)$ 高于物理行动时选取 |

超参数敏感性分析（Table 9）表明，PCE 对树深度 $D$（2→4）、成本权重 $\alpha/\beta$（0.5→1.5）、全局惩罚 $\lambda$（0.5→1.5）及记忆窗口 $K_{\text{action}}/K_{\text{message}}$ 在合理范围内保持稳健，默认设置（$D=3, \alpha=\beta=1, \lambda=1$）总体最优。

## 实验与分析

### 核心机制验证：PCE 在双基准上一致优于通信密集型基线

PCE 的核心主张是：将 LLM 推理中隐含的环境假设显式化为决策树，并通过场景可能性、条件增益和执行成本联合评分来驱动行动选择，可以在**极少通信**的前提下超越依赖频繁对话的现有方法。这一主张在两个互补的多智能体基准上得到了系统验证。

在 **C‑WAH**（协作家务）基准上，以 GPT‑4o mini 为骨干时，PCE 的 Total Steps 降至 **42.76**，比最强通信密集型基线 REVECA（46.80）少 4.04 步，比 CoELA（60.40）少 17.64 步（Table 1）。更关键的是，PCE 的通信动作数（Comm）仅为 **1.70**，而 REVECA 为 6.00，CoELA 高达 9.88——PCE 用不到基线三分之一的通信量完成了更高效的任务协调。这一优势在跨模型验证中保持稳健：无论使用商用模型 GPT‑4o mini、开源通用模型 Gemma3:4B，还是开源大推理模型 GPT‑OSS:20B，PCE 均在 Total Steps 上取得最优或次优，且 Comm 始终远低于所有基线（Table 1）。


![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_GODFBZhFcX/figures/003_Table_1.jpg]]
*Table 1: Experimental results in C-WAH. Best result in bold; second-best underlined*

在 **TDW‑MAT**（三维多智能体运输）基准上，任务目标从"最小化步数"变为"最大化运输完成比例"，PCE 同样展现出跨指标优势。以 GPT‑4o mini 为例，PCE 的 Total 运输比例达 **87.50%**，比 REVECA（81.25%）高 6.25 个百分点，比 CoELA（62.50%）高 25 个百分点；在 Food 和 Stuff 两个子指标上，PCE 分别取得 89.17% 和 85.83%，均领先所有基线（Table 2）。值得注意的是，TDW‑MAT 中 PCE 的 Comm 为 3.58，而 CoELA 高达 13.33，进一步印证了"通信降级为原子动作、仅在预期效用高于物理动作时选取"这一设计理念的有效性。


![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_GODFBZhFcX/figures/004_Table_2.jpg]]
*Table 2: Experimental results in TDW-MAT. Best result in bold; second-best underlined*

**跨模型一致性**是 PCE 区别于基线的重要特征。在三个异构 LLM 骨干上，各基线的性能排序波动较大（例如 REVECA 在 GPT‑4o mini 上表现良好，但在 Gemma3:4B 上可能被 CaPo 超越），而 PCE 在所有骨干上均稳定领先（Table 1 & Table 2）。这表明 PCE 的收益并非依赖特定 LLM 的推理能力，而是源于**结构化不确定性处理机制本身**。

### 消融实验：三模块缺一不可

Table 3 的模块消融实验直接验证了 Planner–Composer–Evaluator 流水线中每个组件的必要性。以 GPT‑4o mini 在 C‑WAH 上的表现为基准：


![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_GODFBZhFcX/figures/008_Table_3.jpg]]
*Table 3: Ablation results in C-WAH. Best result in bold; second-best underlined*

- **移除 Planner**：Total Steps 从 42.76 急剧上升至 **56.46**（增幅 32%），Usages（总 token 消耗）从 44,353.56 暴涨至 139,918.56（增幅 215%）。这表明缺少 Planner 的结构化推理链后，Composer 难以有效提取假设，导致决策树分支不连贯或冗余，代理被迫通过大量试错来弥补规划能力的缺失。
- **移除 Composer**：Total Steps 升至 **46.82**。此时代理仅依赖 Planner 的原始推理链进行评估，无法显式比较多个竞争假设之间的冲突或互补关系，决策完整性下降。
- **移除 Evaluator**：Total Steps 升至 **47.34**。缺乏定量的 likelihood–gain–cost 评估后，代理无法系统化地权衡不同场景路径的预期效用，行动选择退化为启发式判断。

三个模块移除后性能均显著下降，且 Planner 缺失造成的损失最大，说明**结构化不确定性处理的前提是拥有高质量的初始推理链**，而 Composer 和 Evaluator 则分别负责将推理链中的隐含信息"显式化"和"可计算化"。

### 模型缩放与推理深度的独立增益

Figure 3 的 LLM 缩放消融揭示了 PCE 与模型能力之间的**叠加关系**。当仅使用"Planner only"变体（无显式不确定性处理）时，无论是增大模型容量（Gemma3:4B → 12B → 27B）还是加深推理深度（GPT‑OSS:20B Low → Medium → High），性能改善均十分有限。然而，PCE 在所有缩放级别下均显著优于"Planner only"，且 PCE 自身的性能也随模型缩放而提升。这说明**结构化不确定性处理的收益独立于且累加于模型规模与推理深度的缩放**——更大的模型提供了更准确的假设提取与评分，但仅有更大的模型而不进行显式不确定性建模，收益会大幅缩水。


![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_GODFBZhFcX/figures/007_Figure_3.jpg]]
*Figure 3: Ablation results about LLM Scaling in C-WAH Figure 4: User study results in C-WAH environment. environment*

### 不确定性处理与推理增强的对比

Table 8 进一步将 PCE 与两类替代方案进行对比：(1) **不确定性处理变体**：纯物理动作（Phy-act only）、纯通信动作（Com-act only）、仅 Planner（Planner only）；(2) **推理增强基线**：Chain-of-Thought (CoT)、Tree-of-Thought (ToT)、Self-Consistency (SC)。结果表明，PCE 以最少步数（42.76）完成联合目标，显著优于所有变体和推理增强基线。这排除了"PCE 的优势仅源于更复杂的推理链"这一替代解释——CoT/ToT/SC 虽然增强了推理深度或多样性，但缺乏对不确定性的显式建模与系统评估，无法在部分可观测多智能体场景中有效协调竞争假设。

### 超参数稳健性

Table 9 的超参数敏感性分析表明，PCE 对关键超参数在合理范围内保持稳健：
- **决策树深度 D**（2 → 4）：默认值 D=3 总体最优，过浅（D=2）限制假设探索，过深（D=4）引入冗余分支但未显著恶化。
- **成本权重 α/β**（0.5 → 1.5）和**全局惩罚 λ**（0.5 → 1.5）：在默认值 α=β=λ=1 附近，Total Steps 波动在可接受范围内，表明评分函数对成本参数不敏感。
- **记忆窗口 K_action/K_message**：在合理范围内调整未导致性能剧烈变化，默认设置（K_action=10, K_message=3）总体最优。

### 用户研究：通信策略的人类感知评估

Figure 4 和 Table 11 的用户研究从人类协作者视角评估了三种通信策略：PCE、无通信（w/o Com）、始终通信（Com always）。在效率、可信度、有用性和适当性四个主观评估问题上，PCE 的 Likert 得分均显著高于两种极端策略（p < 0.05）。定量结果同样支持这一结论：PCE 的 Total Steps 为 **72.42**，而无通信为 75.67，始终通信高达 114.25。这说明 PCE 的"按需通信"策略不仅在客观任务效率上优于"从不通信"和"过度通信"，在人类伙伴的主观体验上也更具优势——过度通信会打断工作流程，而完全沉默则导致协调失败，PCE 精准地找到了平衡点。

### 可扩展性与评估器对齐

Table 13 展示了 PCE 随代理数量增加的扩展能力：当代理数从 N=2 增至 N=4 时，Total Steps 从 42.76 降至 34.60 再降至 28.50，表明 PCE 能有效利用更多代理的协作能力而不会产生规划开销膨胀。Table 14 的评估器对齐实验显示，LLM Evaluator 与人类专家在三个评分维度上的 MAE 分别为：执行成本 0.88、场景可能性 0.91、条件增益 1.10（5 分量表）。条件增益的 MAE 略高，反映出在部分可观测环境中估算未来效用具有内在主观性，但整体 MAE 均低于 1.1，表明 LLM 评分与专家直觉之间存在合理对齐。

### 失败模式与局限性

尽管 PCE 在两个基准上表现强劲，但分析揭示了若干值得关注的边界：

1. **条件增益评分的可靠性边界**：Evaluator 在条件增益维度上的 MAE（1.10）高于其他维度，说明当环境反馈稀疏或目标依赖关系复杂时，LLM 对"行动能推进目标多少"的估计可能存在系统性偏差。在对精度要求极高的安全关键领域，这一近似可能不足以替代严格贝叶斯推断。

2. **假设提取的命中率依赖任务难度**：Table 15 显示 Composer 的假设有效性随任务难度上升而下降，表明当环境不确定性空间过大或 Planner 推理链质量不足时，决策树可能遗漏关键假设或引入无效分支。Table 16 进一步证实，包含无效假设的场景会导致 Evaluator 评分质量下降。

3. **扩展上限未充分测试**：虽然 Table 13 显示 PCE 在 N=2→4 范围内有效扩展，但论文明确指出简单的语义聚合在面对极大量代理或具有严格顺序依赖的异构任务时可能面临限制，极端扩展条件仍需进一步研究。

4. **环境泛化性有限**：实验仅覆盖 C‑WAH 和 TDW‑MAT 两个室内协作基准，在更开放、动态变化或包含对抗性场景的环境中，PCE 的假设提取与评估机制是否仍然有效尚未验证。

## 方法谱系与知识库定位

### 1. 问题定位：从“通信中心”到“信念中心”的范式转移

PCE 的提出根植于一个具体且未被充分解决的技术瓶颈：在部分可观测、去中心化的多智能体协作环境中，现有方法几乎无一例外地将**代理间通信**作为处理不确定性的首要甚至唯一机制。无论是 **CoELA**（Zhang et al., 2024b）的频繁对话共享状态与计划，**REVECA**（Seo et al., 2025）的带记忆管理与计划验证的请求式信息交换，还是 **CaPo**（Liu et al., 2025）的迭代辩论式多步计划优化，其核心逻辑均为“通信即消歧”——通过增加通信轮次来弥补个体观测的不足。这一范式在涉及人类协作者时尤为脆弱：频繁的通信不仅消耗大量 token 与时间成本，更会打断人类工作流，降低协作的自然性与可信度。

PCE 对此进行了根本性的重新定位。其核心洞察在于：LLM 在推理链中已经自发产生了大量关于环境不确定性的隐含假设（如“食物可能在客厅”），但这些假设零散、非结构化，从未被显式聚合与系统评估。PCE 将不确定性处理从“以通信为中心的协调范式”转变为“以智能体自身信念状态为中心的结构化推理”，通信被降级为决策树中的一个原子动作，仅在预期效用高于物理动作时才被选取。这一范式转移使得智能体能够在**无需频繁通信**的前提下完成高质量的不确定性感知规划。

### 2. 与基线方法的关键设计差异

#### 2.1 不确定性处理机制：从隐式推理到显式决策树

- **CoELA / REVECA / CaPo**：假设（如有）仅在 LLM 的 Chain-of-Thought 推理链中局部、隐式出现，未被提取、聚合或进行跨假设的冲突消解。当环境假设被证伪时，这些方法通常需要重新调用 LLM 进行重规划，缺乏对多个竞争假设的系统化权衡。
- **CoTS**（Zu et al., 2025）：虽然引入了多计划探索与蒙特卡洛树搜索，但其搜索空间以**对话为展开前提**，本质上仍是通信中心范式，延迟与 token 消耗高，且未对不确定性本身进行显式建模。
- **MHP（MCTS-based）**：在部分可观测多智能体场景下，未显式建模不确定性，其树搜索主要针对动作序列而非环境假设空间。

PCE 的关键差异化设计在于 **Planner → Composer → Evaluator 三阶段流水线**：
1. **Planner** 生成推理链与初始候选行动，每个候选行动往往隐含单一环境假设；
2. **Composer** 从推理链中提取不确定性假设，自顶向下构建决策树——每个内部节点为一个二分假设（True/False），叶子为对应行动——按不确定性降低程度与行动影响力排序展开，缺失假设时生成新假设；
3. **Evaluator** 对每条根到叶路径，基于场景可能性 $\mathscr{L}(S)$、目标条件增益 $\mathscr{G}(a)$ 和执行成本 $C(a)$ 计算最终效用得分 $U(S, a) = \mathbb{E}[\mathrm{gain}] - \lambda C(a)$，并按得分排序选择行动。

这一设计将 LLM 推理中潜在、非结构化的环境假设转化为结构化的决策树，使智能体能够联合评估多个竞争假设并选择预期效用最高的行动。

#### 2.2 规划模块结构：从单一规划器到三阶段流水线

基线方法普遍采用单一规划器（含 CoT 推理）或迭代式辩论/多计划树搜索作为规划核心。PCE 的模块化拆分具有明确的因果分工：
- **Planner** 负责生成候选行动与推理链（广度探索）；
- **Composer** 负责提取、组织并扩展不确定性假设（深度结构化）；
- **Evaluator** 负责定量评分与理性选择（效用驱动决策）。

消融实验（Table 3）以量化证据支撑了这一设计的必要性：移除任一模块均导致性能显著下降。其中，移除 Planner 使 Total Steps 从 42.76 升至 56.46（场景探索困难、分支不连贯），移除 Composer 升至 46.82（无法考量多假设冲突），移除 Evaluator 升至 47.34（缺乏定量 likelihood–gain–cost 评估）。

#### 2.3 通信的角色：从搜索机制到原子动作

在 CoTS 等基线中，通信是搜索过程本身的前提与载体；在 CoELA 中，通信是状态对齐的主要手段。PCE 将通信重新定义为决策树中的**原子动作**，与物理动作（移动、抓取、运输）处于同一评估平面。Evaluator 对通信动作同样施加执行成本惩罚 $C(a) = \beta \ell(a)$（$\ell(a)$ 为消息长度），仅当通信的预期增益超过其成本时，通信才会被选中。这一机制从原理上解释了 PCE 为何能在通信动作数上远低于所有基线（C‑WAH 上 PCE 仅 1.70，CoELA 为 9.88，REVECA 为 6.00）。

### 3. 与推理增强方法的对比边界

PCE 的优势并非来自单纯更复杂的推理链。Table 8 的补充消融将 PCE 与 CoT（Chain-of-Thought）、ToT（Tree-of-Thoughts）、SC（Self-Consistency）等推理增强基线进行了直接对比。结果显示，这些推理增强方法虽在一定程度上提升了基线性能，但仍显著弱于 PCE。关键在于：CoT/ToT/SC 增强的是推理过程的广度或自洽性，但并未对**不确定性本身**进行显式建模与评估。PCE 的增益来源于结构化不确定性处理，而非推理链的复杂度提升。

LLM 缩放实验（Figure 3）进一步强化了这一结论：仅增大模型容量（Gemma3:4B→12B→27B）或加深推理深度（GPT-OSS:20B Low→Medium→High）对无显式不确定性处理的“Planner only”变体仅带来有限增益，而 PCE 在所有缩放级别下均保持显著领先。这表明**结构化不确定性处理的收益独立于且累加于模型规模与推理深度**。

### 4. 适用边界与局限

#### 4.1 团队规模与任务异质性

当前 PCE 在小型到中等规模团队（N ≤ 4）上已验证有效（Table 13 显示随代理数量增加，Total Steps 下降，表明协调有效且无规划开销膨胀）。然而，简单的语义聚合在面对极大量代理或具有严格顺序依赖的异构任务时可能面临限制。随着代理数量增长，不确定性空间呈指数扩张，Composer 的决策树构建与 Evaluator 的路径评分成本将随之增加。这一扩展性问题需要进一步研究。

#### 4.2 Evaluator 的主观评分可靠性

Evaluator 对条件增益 $\mathscr{G}(a)$ 的评分与人类专家之间的 MAE 为 1.10（Table 14），高于场景可能性（0.85）和执行成本（0.78）的 MAE。这表明在部分可观测环境中估算未来效用的主观性较强，LLM 评分的可靠性可能受上下文模糊性影响。在对精度要求极高的安全关键领域，当前的 LLM 近似可能不足以替代严格的贝叶斯推断。

#### 4.3 环境泛化边界

实验仅局限于两个特定的室内协作基准（C‑WAH 和 TDW‑MAT）。在更开放、动态变化或包含对抗性场景的环境中，PCE 的有效性尚未验证。Composer 的假设提取依赖于 LLM 对室内物品协作场景的常识推理能力，当环境语义发生根本性变化时（如自动驾驶、搜救机器人），假设提取的命中率与 Evaluator 的评分准确性可能需要重新校准。

#### 4.4 实时自适应能力

当前框架的决策树在每步规划时静态构建，未包含在实时执行过程中动态发现并引入新假设的机制。当环境出现决策树初始构建时未涵盖的意外状态时，智能体可能需要等待下一轮规划周期才能将其纳入不确定性推理。

### 5. 开放问题

1. **极端扩展条件下的语义聚合**：PCE 如何扩展到 N ≫ 4 的团队以及具有严格时序依赖的异构任务？简单的语义聚合是否足以处理指数增长的不确定性空间，还是需要引入层次化或分布式的信念聚合机制？

2. **自适应不确定性推理**：能否在实时执行过程中动态发现并引入最初决策树中未涵盖的新假设？这需要 Composer 具备在线增量更新决策树的能力，而非每步从零构建。

3. **Evaluator 可靠性的进一步提升**：如何降低条件增益评分的主观性误差？可能的路径包括多轮自我改进、集成多个 LLM 评分、引入轻量级环境模型进行蒙特卡洛模拟，或通过人类反馈进行微调对齐。

4. **计算成本的可扩展性**：PCE 的每步内部推理调用了三次 LLM 推理（Planner, Composer, Evaluator），而某些基线仅需两次。随着问题规模增长，决策树的构建与评估成本的增长速度如何？是否存在更高效的近似或剪枝策略（如基于信息增益的提前终止、路径束搜索）以应对超长视距任务？

5. **跨领域迁移**：在完全不同于室内物品协作的领域（如自动驾驶、搜救机器人），PCE 的假设提取与评估机制是否仍然有效？Composer 依赖的常识推理能力在不同领域中的覆盖度与准确性需要系统性评估。

6. **通信内容的优化**：PCE 目前将通信视为原子动作并在决策树中与物理动作一同评估，但通信内容的生成仍由 LLM 直接完成。是否能进一步优化通信的内容生成策略，使其更具信息量和针对性（例如，仅传递高不确定性的关键假设及其置信度），从而进一步降低通信开销？

## 原文 PDF

![[paperPDFs/ICLR_2026/From_Assumptions_to_Actions_Turning_LLM_Reasoning_into_Uncertainty_Aware_Planning_for_Embodied_Agents.pdf]]
