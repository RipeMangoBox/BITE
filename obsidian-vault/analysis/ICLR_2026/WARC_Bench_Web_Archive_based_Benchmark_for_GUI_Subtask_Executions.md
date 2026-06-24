---
title: "WARC-Bench: Web Archive based Benchmark for GUI Subtask Executions"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/WARC_Bench_Web_Archive_based_Benchmark_for_GUI_Subtask_Executions.pdf
openreview_forum_id: Hgw56DUFzD
aliases:
- WBSVASSR
- WARC-Bench
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/reinforcement_learning_and_planning
core_operator: "通过基于WARC文件的现实、可回放的沙盒环境与可验证奖励机制，结合监督微调与在线强化学习（RLVR），显著提升模型在GUI子任务中的视觉定位、探索效率和格式遵循能力。"
primary_logic: "GUI子任务（多步交互但单目标、短时程）是构建强大网页智能体所必需但被忽视的原子能力；WARC快照提供高保真、易扩展的评估环境，配合可验证奖励的强化学习，能有效蒸馏教师模型的知识并缩小开源与闭源模型在该能力上的差距。"
claims:
- "Claude Sonnet 4.0在WARC-Bench测试集仅达64.83%，显示出前沿模型在子任务执行上仍有较大改进空间。"
- "提出的Ours-72B-RLVR模型达到52.33%测试成功率，显著优于其基座模型Qwen2.5-VL 72B的37.3%，并超过GPT-5（51.3%）等闭源模型。"
- "在线强化学习（RLVR）在SFT基础上进一步提升了性能：7B模型从27.33%到29.17%，72B模型从48.33%到52.33%。"
- "在WebArena等长程导航任务上的转移实验表明，分层规划器+执行器（Planner+Executor）设计可进一步提升性能，说明WARC-Bench训练的子任务能力有助于复杂工作流。"
---

# WARC-Bench: Web Archive based Benchmark for GUI Subtask Executions

> [!tip] 核心洞察
> GUI子任务（多步交互但单目标、短时程）是构建强大网页智能体所必需但被忽视的原子能力；WARC快照提供高保真、易扩展的评估环境，配合可验证奖励的强化学习，能有效蒸馏教师模型的知识并缩小开源与闭源模型在该能力上的差距。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | WARC-Bench：基于Web Archive的GUI子任务执行基准 |
| 英文题名 | WARC-Bench: Web Archive based Benchmark for GUI Subtask Executions |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Hgw56DUFzD); [Project](https://sanjari-orb.github.io/warc-bench/) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/reinforcement_learning_and_planning |
| Method | WARC-Bench + Subtask Vision Agent (SVA) with SFT+RLVR |
| Dataset | WARC-Bench (Test), WARC-Bench (Dev[TOTAL]), ScreenSpot V2 (OOD, Desktop/Mobile only), WebArena-Lite (WA-Lite) |

> [!tip] 效果简介
> - WARC-Bench (Test) 上，Task Success Rate (%) 为 Ours-72B-RLVR: 52.33，对比 Qwen2.5-VL 72B: 37.3; Claude Sonnet 4.0: 64.83，变化 +15.03 / -12.50 against baselines。
> - WARC-Bench (Dev[TOTAL]) 上，Success Rate (%) 为 Ours-72B-RLVR: 84.31，对比 Claude Sonnet 4.0: 83.61; Qwen2.5-VL 72B: 61.06，变化 +0.70 vs Claude; +23.25 vs Qwen。
> - ScreenSpot V2 (OOD, Desktop/Mobile only) 上，Success Rate (%) 为 Ours-72B-RLVR: 82.74，对比 Qwen2.5-VL 72B: 87.42; GPT-5: 29.67，变化 -4.68 vs Qwen; +53.07 vs GPT-5。

## 概述

现有前沿多模态模型在真实网页 GUI 子任务执行上表现远未饱和：Claude Sonnet 4.0 在 WARC-Bench 测试集上仅达 64.8% 成功率（Table 2），瓶颈集中于复杂 UI 控件交互失误（如日期选择器格式误判、预填充文本字段未清除）与网页探索策略不足。然而，当前基准普遍缺乏对这种短时程、组合式交互能力的系统评估。

本文提出 **WARC-Bench**——一个基于 Web Archive（WARC）文件的交互式基准，配合可回放的沙盒环境与程序化可验证奖励，专门衡量 GUI 子任务执行能力。在此基础上，作者设计了 **Subtask Vision Agent (SVA)**——一种仅依赖截图的轻量级代理架构，并通过监督微调（SFT）与在线强化学习（RLVR）的组合训练策略，显著提升模型的视觉定位、探索效率和格式遵循能力。

核心发现可概括为三条因果链：

1. **WARC 快照提供高保真、易扩展的评估环境**，解决了现有基准在任务隔离、确定性奖励和可扩展性上的短板（Table 1）。
2. **SFT 从强教师模型蒸馏知识**，将 Qwen2.5-VL 72B 的测试成功率从 37.3% 提升至 48.3%；**在线 RLVR 进一步推高至 52.3%**，超过 GPT-5（51.3%）等闭源模型（Table 2）。
3. **子任务执行能力可迁移至长程导航**：在 WebArena-Lite 上，分层 Planner+Executor 设计使 Qwen2.5-VL 72B 提升 8.46 个百分点（Table 4），表明该原子能力是构建强大网页智能体的必要组件。

方法层面，SVA 采用 8 种基本动作、5 步历史窗口和思维链推理（Figure 3），RLVR 训练使用带 KL 惩罚的截断 PPO 目标函数（Appendix D），在合成子任务上进行在线策略优化。消融实验证实，离线 RL 方法（GRPO、PPO）在小规模模型上性能下降，在线 RLVR 是唯一稳定提升的方案（Table 5）。

主要局限包括：WARC 无法录制依赖反爬机制的动态网站；合成任务仍需人工验证；子任务执行器在长程代理中的最优集成方式尚未系统探索。

## 背景与动机

### 网页智能体的能力瓶颈：长程导航与短程子任务

近年来，基于多模态大模型的网页智能体（Web Agent）取得了显著进展，能够在浏览器中自主完成信息检索、表单填写、购物结算等复杂工作流。现有基准测试（如WebArena、MiniWoB++）主要评估智能体在长程导航任务上的端到端成功率，即从一个初始页面出发，经过多步操作达成最终目标。然而，这类评估范式掩盖了一个关键问题：**长程任务的成功依赖于大量原子性的GUI子任务执行能力**——例如在日历组件中选择特定日期、从下拉菜单中筛选选项、在文本字段中输入格式化内容等。这些子任务具有“多步交互但单目标、短时程”的特征，是构建鲁棒网页智能体所必需但长期被忽视的原子能力。

### 现有基准的评估盲区

当前主流GUI智能体基准存在三个结构性缺陷，导致无法有效评估子任务执行能力：

1. **缺乏任务隔离机制**：长程基准中的子任务执行质量难以独立归因——智能体可能因高层规划失误而失败，而非底层交互能力不足。
2. **环境不可控与不可复现**：依赖实时网站的基准面临网站更新、反爬虫机制、会话过期等问题，导致评估结果不可复现且难以规模化。
3. **奖励信号模糊**：多数基准缺乏程序化的、确定性的中间状态验证，难以精确判断单个子任务是否成功完成。

Table 1 对比了WARC-Bench与现有基准在交互环境、任务隔离、确定性奖励、可扩展设计等维度的差异，凸显了现有工作在子任务评估上的系统性缺失。

### 前沿模型的子任务执行表现揭示能力缺口

即便最先进的多模态模型，在真实网页子任务执行上仍表现不佳。在WARC-Bench测试集上，Claude Sonnet 4.0仅达到64.83%的任务成功率，GPT-5为51.33%，而开源的Qwen2.5-VL 72B更是低至37.33%（Table 2）。这些结果揭示了两个核心瓶颈：

- **复杂UI控件的交互失误**：前沿模型频繁在日期选择器的格式匹配（如需要“YYYY/MM/DD”却输入“YYYY-MM-DD”）、预填充文本字段的清理（未删除默认值直接追加输入）等场景中失败（Figure 6, Figure 7）。
- **缺乏有效的网页探索策略**：模型倾向于执行最少的操作后即宣告完成，而非主动滚动页面以发现隐藏的目标元素，导致信息检索类子任务成功率偏低（Figure 4）。

### 本文动机：构建子任务执行能力的系统性训练与评估框架

上述分析表明，**GUI子任务执行是一项可独立定义、可精确评估、且具有显著提升空间的原子能力**。本文的动机在于：

1. **构建高保真、可扩展的评估环境**：利用Web Archive（WARC）文件录制并回放真实与合成网页，在隔离的沙盒环境中提供可复现的交互式评估，配合程序化可验证奖励函数实现自动化评测。
2. **设计面向子任务的专用智能体架构**：提出Subtask Vision Agent（SVA），采用纯截图观察、最小化动作空间（8种原子操作）、5步历史窗口与结构化思维链推理，专注于短时程子任务的高效执行。
3. **通过监督微调与在线强化学习缩小能力差距**：利用前沿模型（教师）生成的蒸馏数据进行监督微调，再通过可验证奖励的在线强化学习（RLVR）进一步优化模型的视觉定位、探索效率与格式遵循能力，显著提升开源模型在子任务执行上的竞争力。

## 核心创新

WARC-Bench 的核心创新围绕三个紧密耦合的“变更槽”（changed slots）展开，形成一条从评估环境构建到智能体设计，再到训练范式升级的完整技术链路。

**变更槽 1：评估环境 — 从静态基准到基于 WARC 的可交互、可验证沙盒**

现有 GUI 智能体基准（如 WebArena、MiniWoB++、ScreenSpot）普遍存在任务不可隔离、环境不可控、奖励需人工评判或依赖 LLM 近似等问题（Table 1）。WARC-Bench 改用 Web Archive（WARC）文件作为网页快照的载体，在基于 Playwright 的 Chromium 浏览器中实现高保真回放。这一设计的因果机制在于：WARC 快照将真实网页的 DOM、样式与资源完整归档，既保留了交互性，又隔离了外部网络噪声（如反爬虫、动态 URI），从而为每个任务提供**确定性的初始状态与可编程验证的终态奖励**。基准数据集由三要素构成：(a) 基于 WARC 的交互环境，(b) 自然语言子任务目标，(c) 程序化奖励函数。这种设计使得大规模自动评估成为可能，同时避免了 LLM-as-judge 引入的评分偏差。

**变更槽 2：智能体设计 — Subtask Vision Agent（SVA）：纯视觉观察 + 极简动作空间**

与 Claude Computer-Use、OpenAI CUA 等闭源代理内置的复杂动作模式和观察模型不同，SVA 采用了一种刻意简化的设计（Figure 3）。其核心约束包括：
- **纯截图观察**：仅以 1280×720 的浏览器视口截图作为环境状态输入，不依赖 DOM 树或可访问性树信息。
- **8 种基本动作**：`click`、`scroll`、`type`、`hover`、`key_press`、`drag_and_release`、`wait`、`complete`（Table 6），足以覆盖绝大多数子任务交互需求。
- **5 步历史截断**：仅保留最近 5 步的观察-动作历史，抑制长程上下文膨胀。
- **结构化思维链推理**：模型需依次回答“当前网页状态是什么？”“上一步是否成功？为什么？”“任务是否完成？”等问题后再输出动作。

这一设计的瓶颈突破逻辑在于：子任务本身是短时程、单目标的原子操作，过度的动作空间和观察冗余反而引入干扰。SVA 通过强制模型聚焦于视觉定位与简洁交互，在显著降低 token 消耗和平均轨迹步数的同时，保持了具有竞争力的任务完成率（Table 2, Figure 5）。

**变更槽 3：训练范式 — 从纯 SFT 到 SFT + 在线强化学习（RLVR）**

基线方法仅依赖监督微调（SFT）来蒸馏强教师模型（如 Claude）的轨迹数据。本文在此基础上引入**在线强化学习与可验证奖励（RLVR）**，使用带 KL 散度惩罚的截断 PPO 目标进行策略优化：

$$ \mathcal{L}^{\mathrm{PPO}}(\theta) = \mathbb{E}_t \Big[ \min \big( r_t(\theta) A_t, \mathrm{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon) A_t \big) \Big] - \beta \mathrm{KL}[\pi_\theta \parallel \pi_{\mathrm{ref}}] $$

其中熵正则系数 $\alpha$ 在实际训练中被设为 0（Appendix D）。RLVR 的关键因果机制在于：SFT 仅教会模型“模仿正确动作”，而 RLVR 通过在线环境交互与确定性奖励信号，直接优化任务完成这一终极目标。这使得模型能够自主探索更高效的交互策略——消融实验显示，RLVR 模型的动作分布中 `scroll` 动作显著增加，平均轨迹步数减少约 0.94 步（Figure 4），表明模型学会了更主动地探索页面而非被动等待。

**变更槽间的协同效应**

三条变更槽并非孤立存在，而是形成正向反馈循环：WARC 的可回放性与程序化奖励为 RLVR 提供了低成本、高吞吐的在线训练环境；SVA 的极简设计降低了 RLVR 的探索空间复杂度；RLVR 反过来弥补了 SFT 在探索策略上的不足。这一协同在 72B 规模上尤为显著——Ours-72B-RLVR 在 WARC-Bench 测试集达到 52.33%，较其 SFT 基线（48.33%）提升 4 个百分点，较基座模型 Qwen2.5-VL 72B（37.3%）提升 15 个百分点，并超越 GPT-5（51.3%）等闭源模型（Table 2）。

值得注意的是，**离线 RL 方法（GRPO、PPO）在此任务上表现不稳定**：7B 模型上离线 RL 反而劣于 SFT（GRPO_offline 63.86% vs SFT 66.54%），仅在 72B 上 GRPO_offline 略微超过 SFT（76.89% vs 75.88%），而在线 RLVR 是唯一在两个规模上均稳定提升的方案（Table 5）。这一对比强化了在线交互与可验证奖励对于子任务执行能力训练的必要性。

## 整体框架

![[assets/figures/papers/iclr26_0012_Hgw56DUFzD_WARC-Bench_Web_Archive_based_Benchmark_for_GUI_S/figures/004_Table_1.jpg]]
*Table 1: Comparison of Multimodal Benchmarks for Web Task Performance of GUI Agents. (—) templates indicate that all benchmark tasks are unique*

![[assets/figures/papers/iclr26_0012_Hgw56DUFzD_WARC-Bench_Web_Archive_based_Benchmark_for_GUI_S/figures/006_Figure_3.jpg]]
*Figure 3: Diagram of the Subtask Vision Agent (SVA) design*

### 问题定义与设计动机

WARC-Bench 的目标是系统评估和提升 GUI 智能体在真实网页环境中执行**子任务**（subtask）的能力。子任务被定义为多步交互但目标单一、时程较短的操作单元，例如填写表单、选择日期、提取特定信息等。这类能力是构建长程网页智能体所必需的原子技能，但现有基准（如 WebArena、MiniWoB++）或侧重长程导航，或依赖简化的合成环境，难以精确衡量模型在真实 UI 控件上的交互精度。

### 核心 Pipeline 架构

整个框架由三个核心层构成：**环境层**、**智能体层**和**训练层**，它们之间的数据流关系如下：

```
WARC 文件 → BrowserGym 沙盒 → 截图观察 → SVA 智能体 → 动作执行 → 可验证奖励
                ↑                                    ↓
           任务目标（自然语言）              程序化奖励函数
```

#### 1. 环境层：WARC 快照 + BrowserGym 沙盒

WARC-Bench 使用 **Web Archive (WARC)** 文件作为网页的持久化快照。WARC 格式完整录制了网页的 HTML、CSS、JavaScript 及媒体资源，使得同一网页可以在 Chromium 浏览器中反复回放，不受原始网站可用性或动态 URI 变化的影响。

每个基准任务由三个组件构成（证据锚点：Section 1 INTRODUCTION）：
- **(a) WARC 文件**：录制真实或合成网站的交互式网页环境；
- **(b) 自然语言子任务目标**：描述需要完成的具体操作；
- **(c) 程序化可验证奖励函数**：基于 DOM 状态或页面内容，自动判定任务是否成功。

回放环境基于 **BrowserGym** 框架，使用 Playwright 驱动 Chromium 浏览器。智能体通过标准化的动作 API 与页面交互，环境返回 1280×720 的视口截图作为观察。

#### 2. 智能体层：Subtask Vision Agent (SVA)

SVA 是一个极简但有效的智能体设计（证据锚点：Section 3.2，Figure 3），其核心特征如下：

- **纯截图观察**：SVA 仅使用浏览器视口的截图作为状态输入，不依赖 DOM 树或可访问性树。这一设计既降低了不同网站间观察空间的异构性，也使得智能体更接近人类用户的感知方式。
- **最小化动作空间**：SVA 提供 8 种原子动作类型（证据锚点：Table 6）：`click`、`complete`、`drag_and_release`、`hover`、`key_press`、`scroll`、`type`、`wait`。每种动作以 Python 风格函数签名的形式定义，模型输出函数调用即可执行。
- **5 步历史截断**：为控制提示词长度，SVA 仅保留最近 5 步的观察-动作历史，更早的信息被截断（证据锚点：Appendix G）。
- **结构化思维链推理**：模型在输出动作前，需依次回答以下问题（证据锚点：Appendix G）：
  - 当前网页状态是什么？
  - 上一步动作是否成功？为什么？
  - 任务是否已完成？
  - 下一步应该执行什么动作？

这一设计使 SVA 在保持低推理开销的同时，在 WARC-Bench 上取得了与专用计算机使用代理（如 Claude CUA、OpenAI CUA）相当甚至更优的性能（证据锚点：Table 2）。

#### 3. 训练层：SFT + 在线强化学习（RLVR）

训练流程分为两个阶段：

**阶段一：监督微调（SFT）**
使用强前沿模型（如 Claude）在合成子任务上生成的轨迹作为教师数据进行蒸馏。SFT 将基座模型（Qwen2.5-VL 7B/72B）的成功率从极低水平大幅提升：7B 模型从 4.67% 提升至 27.33%，72B 模型从 37.33% 提升至 48.33%（证据锚点：Table 2，Section 5）。

**阶段二：在线强化学习（RLVR）**
在 SFT 模型基础上，使用 PPO 算法进行在线策略优化。奖励信号直接来自环境的程序化可验证奖励函数（成功=1，失败=0），无需人工标注或奖励模型。PPO 损失函数采用标准截断形式，并加入 KL 散度惩罚项（证据锚点：Appendix D）：

$$\mathcal{L}^{\mathrm{PPO}}(\theta) = \mathbb{E}_t \Big[ \min \big( r_t(\theta) A_t, \mathrm{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon) A_t \big) \Big] - \beta \mathrm{KL}[\pi_\theta \parallel \pi_{\mathrm{ref}}] + \alpha \mathcal{H}[\pi_\theta]$$

实际训练中，熵正则系数 $\alpha=0$ 被省略。7B 模型使用 $\epsilon=0.20$，$\beta=0.10$；72B 模型使用 $\epsilon=0.15$，$\beta=0.03$（证据锚点：Appendix E）。

RLVR 训练在 SFT 基础上进一步提升了性能：7B 模型从 27.33% 提升至 29.17%，72B 模型从 48.33% 提升至 52.33%（证据锚点：Table 2）。行为分析显示，RLVR 模型的动作分布更高效，平均轨迹长度减少约 0.94 步，且探索性滚动（scroll）动作显著增加（证据锚点：Figure 4）。

### 关键设计优势

Table 1 将 WARC-Bench 与现有多模态 GUI 基准进行了系统对比，其核心优势体现在：

- **交互式环境**：与仅提供静态截图的基准（如 ScreenSpot）不同，WARC-Bench 提供完整的浏览器交互环境。
- **任务隔离**：每个任务在独立的 WARC 快照中执行，避免任务间状态污染。
- **确定性奖励**：程序化奖励函数提供无噪声的成功/失败判定，适合强化学习训练。
- **可扩展设计**：WARC 文件可来自真实网站录制或程序化合成，支持大规模任务扩展（尽管合成网站仍需人工验证任务可行性，见局限性说明）。

### 局限与待验证假设

当前框架存在以下已知局限：
1. WARC 录制无法捕获依赖 Cloudflare 防护、反爬虫机制或包含动态会话 ID 的网站。
2. 合成网站的创建仍需人工验证任务目标和评估函数的正确性，限制了全自动扩展。
3. SVA 的纯截图观察可能丢失可访问性树中的结构化信息，在需要精确文本定位的场景中可能处于劣势。
4. RLVR 的训练目前仅针对短时程子任务，其在长程工作流中的泛化效果仅通过分层规划器设计进行了初步验证（证据锚点：Table 4，+8.46% 提升）。

## 核心模块与公式推导

WARC-Bench 的系统管线由四个核心模块串联构成，支撑从网页状态感知到动作执行的闭环。

**网页快照捕获模块**：以 1280×720 分辨率截取当前浏览器视口的完整截图，作为环境状态的唯一观察源（SVA 仅依赖截图，不使用 DOM 树或可访问性树信息）。

**思维链推理模块**：模型基于任务目标、当前截图及最近 5 步历史，生成结构化推理。推理内容需依次回答：当前网页状态分析、上一步动作是否成功及原因、任务是否已完成、若未完成则下一步应执行什么操作及其理由。

**动作预测模块**：根据推理结论，从 8 种原子动作中选择下一步操作。动作空间定义如下（Table 6）：

| 动作 | 函数签名 | 描述 |
|------|----------|------|
| click | `click(element_id: int)` | 点击指定元素 |
| complete | `complete(answer: str)` | 任务完成，返回答案 |
| drag_and_release | `drag_and_release(start_id: int, end_id: int)` | 拖拽元素至目标位置 |
| hover | `hover(element_id: int)` | 悬停在指定元素上 |
| key_press | `key_press(key_comb: str)` | 按下键盘组合键 |
| scroll | `scroll(x: int, y: int)` | 滚动页面 |
| type | `type(element_id: int, text: str)` | 在指定元素中输入文本 |
| wait | `wait()` | 等待页面加载 |

**BrowserGym 执行模块**：在 Playwright 驱动的 Chromium 浏览器中执行预测的动作，并将执行后的新截图和反馈返回给模型，形成下一轮观察。

---

**RLVR 训练的核心公式**

在线强化学习（RLVR）采用带 KL 散度惩罚的截断 PPO 目标函数（Appendix D）：

$$ \mathcal{L}^{\mathrm{PPO}}(\theta) = \mathbb{E}_t \Big[ \min \big( r_t(\theta) A_t, \mathrm{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon) A_t \big) \Big] - \beta \,\mathrm{KL}[\pi_\theta \parallel \pi_{\mathrm{ref}}] + \alpha \mathcal{H}[\pi_\theta] $$

其中：
- $r_t(\theta) = \frac{\pi_\theta(a_t|s_t)}{\pi_{\text{old}}(a_t|s_t)}$ 为当前策略与旧策略的概率比；
- $A_t$ 为优势函数，由可验证奖励（程序化判定任务是否完成）计算得出；
- $\epsilon$ 为截断阈值（7B 模型设为 0.20，72B 模型设为 0.15）；
- $\beta$ 为 KL 惩罚系数（7B 模型设为 0.10，72B 模型设为 0.03），约束当前策略 $\pi_\theta$ 不偏离参考策略 $\pi_{\text{ref}}$（SFT 模型）；
- $\alpha$ 为熵正则系数，实际训练中设为 0，即省略熵奖励项。

奖励信号完全来自 WARC-Bench 内置的程序化验证函数，无需人工标注或判别模型评分，这使得 RLVR 训练可在线、大规模地自动进行。

## 实验与分析

### 主结果：前沿模型在子任务执行上仍有显著瓶颈

WARC-Bench 测试集上的轨迹级成功率（Table 2）揭示了当前多模态模型在真实网页 GUI 子任务执行上的能力上限。表现最好的闭源模型 **Claude Sonnet 4.0 仅达到 64.83%** 的成功率，说明即便是最强前沿模型，在短时程、单目标的子任务（如填写表单、选择日期、提取数据）上仍有超过三分之一的失败率。GPT-5 在同一测试集上仅获得 51.33%，而未经微调的开源模型 Qwen2.5-VL 72B 更是低至 37.33%。

![[assets/figures/papers/iclr26_0012_Hgw56DUFzD_WARC-Bench_Web_Archive_based_Benchmark_for_GUI_S/figures/007_Table_2.jpg]]
*Table 2: Trajectory-Level Success Rates on WARC-Bench. Small VLMs (7B params) are in gray. Results are divided into closed (top) vs. open-source (bottom) models. CUA indicates models evaluated with the provider’s computer-use agent. All other models use SVA. All values are averages across 3 runs, however ∗ indicates single-run results due to prohibitive HuggingFace inference costs for OpenCUA. Best per benchmark is in bold. Best inside its sector (small/large open source vs closed source) is underlined*

这种性能落差的核心原因并非模型缺乏视觉理解能力，而是**交互层面的系统性失误**：模型在复杂 UI 控件（如日期选择器的格式遵循、预填充文本字段的清除）上频繁出错，且缺乏有效的网页探索策略。Figure 6 和 Figure 7 展示了 Claude Sonnet 4.0 的两个典型失败案例——传入错误日期格式 `YYYY/MM/DD`，以及未删除预填充文本直接追加输入——这些错误在真实网页交互中极为常见，但现有基准（如 WebArena、MiniWoB++）因任务粒度过粗或环境过于简化而难以捕捉。

### 训练策略对比：在线 RLVR 是唯一稳定提升的方案

Table 5 的消融实验系统比较了四种训练算法在子任务完成率上的表现。核心发现如下：

![[assets/figures/papers/iclr26_0012_Hgw56DUFzD_WARC-Bench_Web_Archive_based_Benchmark_for_GUI_S/figures/014_Table_5.jpg]]
*Table 5: Performance Comparison of Training algorithms on Subtasks Completion (%). All models use SVA agent design*

| 训练方法 | 7B 模型 Dev[TOTAL] | 72B 模型 Dev[TOTAL] |
|---------|-------------------|---------------------|
| SFT（基线） | 66.54% | 75.88% |
| 离线 GRPO | 63.86% (↓2.68) | 76.89% (↑1.01) |
| 离线 PPO | 61.76% (↓4.78) | 75.66% (↓0.22) |
| **在线 RLVR (PPO)** | **72.13% (↑5.59)** | **84.31% (↑8.43)** |

**在线 RLVR 是唯一在两个模型规模上均稳定提升的方法**。7B 模型从 SFT 的 66.54% 提升至 72.13%（+5.59 个百分点），72B 模型从 75.88% 提升至 84.31%（+8.43 个百分点），后者甚至超越了 Claude Sonnet 4.0 的开发集表现（83.61%）。

相比之下，离线强化学习方法在小规模模型上出现了明显的性能退化：7B 模型使用离线 GRPO 降至 63.86%，离线 PPO 降至 61.76%，均低于 SFT 基线。72B 模型上离线 GRPO 仅有微弱提升（+1.01 个百分点），离线 PPO 则略有下降。这一现象表明，**离线 RL 的奖励建模或策略约束在子任务执行场景中不足以替代在线环境交互提供的探索信号**——模型需要通过与真实网页环境的实时交互来学习 UI 控件的格式约束和操作序列的因果结构。

### RLVR 驱动的行为变化：更高效、更具探索性

Figure 4 的行为分析揭示了 RLVR 训练对模型动作策略的深层影响：

![[assets/figures/papers/iclr26_0012_Hgw56DUFzD_WARC-Bench_Web_Archive_based_Benchmark_for_GUI_S/figures/010_Figure_4.jpg]]
*Figure 4: Behavioral analysis of Ours-72B-SFT (SFT) v/s Ours-72B-RLVR (RLVR) model*

- **动作分布变化**：RLVR 模型的 `scroll` 动作占比显著增加，表明模型学会了更主动地探索页面内容，而非仅依赖初始视口信息。这与子任务执行中需要定位非首屏元素的实际需求一致。
- **轨迹长度缩短**：RLVR 模型的平均任务完成步数比 SFT 模型减少约 0.94 步（Figure 4c），说明模型在强化学习过程中学到了更直接有效的操作路径，减少了冗余交互。
- **成功率提升的因果链条**：从 SFT 到 RLVR 的改进并非简单的模式记忆，而是通过可验证奖励信号（程序化检查任务是否完成）驱动模型在合成子任务环境中进行策略优化，最终蒸馏出更高效的视觉定位和格式遵循能力。

### 跨基准泛化与迁移

**域外定位能力验证**：在 ScreenSpot V2 的桌面/移动设备子集上（Table 7），Ours-72B-RLVR 达到 82.74% 的成功率，显著超越 GPT-5（29.67%），并接近其基座模型 Qwen2.5-VL 72B（87.42%）。值得注意的是，该评估排除了网页截图（避免训练数据污染），仅保留桌面和移动 GUI 截图，证明 RLVR 训练的视觉定位能力具有一定的跨平台泛化性。

**长程导航任务的迁移**：在 WebArena-Lite 上的分层代理实验（Table 4）表明，将 WARC-Bench 训练的子任务执行器作为分层架构中的 Executor，可以提升整体导航性能。使用 Qwen2.5-VL-72B 作为 Planner、Ours-72B-RLVR 作为 Executor 的分层设计达到 24.63% 的成功率，相比单循环 SVA 基线的 16.17% 提升了 **+8.46 个百分点**。这验证了子任务执行能力是构建复杂网页智能体的可复用原子能力。

![[assets/figures/papers/iclr26_0012_Hgw56DUFzD_WARC-Bench_Web_Archive_based_Benchmark_for_GUI_S/figures/012_Table_4.jpg]]
*Table 4: Web navigation accuracies on a simple SVA agent v/s Hierarchical Planner+Executor agent designs. SVA – Single-loop execution agent detailed in Section 3.2. Hier.[P,E] – Hierarchical agent consisting of a Planner that determines what subtasks to perform, and an SVA agent acting as an Executor. Executor completes the subtask before returning control to the Planner*

然而，分层设计并非万能：当使用 Claude-4.0-Sonnet 时，SVA 基线（36.32%）反而优于所有分层变体（最佳 35.82%），说明**最优代理架构可能依赖于基座模型本身的能力水平**——强模型在单循环设计中已能有效隐式规划，分层引入的额外通信开销反而可能降低效率。

### 效率-准确率权衡

Figure 5 的准确率-延迟权衡分析显示，Ours-RLVR 变体处于帕累托前沿：在达到有竞争力的成功率的同时，保持了较高的任务吞吐量。与 Claude 模型家族相比，本文模型在吞吐量（tasks/hour）上具有显著优势，这对于需要批量执行网页子任务的实际部署场景尤为重要。

### 失败模式与剩余挑战

基于分析数据和论文报告的定性失败案例，WARC-Bench 上的主要失败模式可归纳为三类：

1. **格式遵循失败**：模型未能正确理解或遵循 UI 控件的隐式格式约束（如日期格式 `MM/DD/YYYY` vs `YYYY/MM/DD`），即使视觉定位正确，输出内容仍被拒绝。
2. **状态感知不足**：模型未能在操作前充分感知当前字段状态（如是否存在预填充文本），导致操作无效或产生错误叠加。
3. **探索终止过早**：模型在未完成目标时过早调用 `complete` 动作，或因历史截断（5 步限制）丢失关键上下文而陷入重复操作。

这些失败模式指向一个核心问题：**纯截图观察在缺乏显式 UI 结构信息（如可访问性树、DOM 状态）时，难以可靠地传递控件的约束规则和当前状态**。这是 SVA 设计的固有权衡——简化观察空间以降低 token 消耗和延迟，但牺牲了部分关键的结构化信息。

## 方法谱系与知识库定位

### 1. 在现有基准与智能体谱系中的位置

WARC-Bench 所解决的问题位于 GUI 智能体评测的三个断层交汇处。Table 1 的系统对比清晰地揭示了这一点：现有基准（如 WebArena、MiniWoB++、ScreenSpot）或缺乏交互式环境，或任务不可隔离，或不具备确定性奖励函数。WARC-Bench 通过“WARC 快照 + 程序化可验证奖励 + 任务隔离”三重设计，填补了短时程、组合式 GUI 子任务评测的空白。

在智能体设计谱系中，Subtask Vision Agent (SVA) 采取了一条极简路线：纯截图观察、8 种原子动作（Table 6）、5 步历史截断、思维链推理（Figure 3）。这与 Anthropic Claude Computer-Use 或 OpenAI CUA 等闭源代理的复杂动作空间和长上下文设计形成鲜明对比。实验结果表明，这种极简设计并未牺牲竞争力——在相同基座模型上，SVA 框架下的 Qwen2.5-VL 72B 在 WARC-Bench Dev[TOTAL] 上达到 61.06%，而该基座模型配合专用计算机使用代理的表现明显更差（Table 2 中 Qwen2.5-VL 72B 的 SVA 结果 vs 各 CUA 基线）。

从训练范式看，本文的方法链路——监督微调（SFT）蒸馏教师模型知识 + 在线强化学习（RLVR）优化探索策略——属于“蒸馏-强化”混合范式。这与 UI-TARS 1.5、OpenCUA 等纯 SFT 开源方案形成对比。关键差异在于 RLVR 阶段：通过在合成子任务上的在线 PPO 训练（带 KL 正则，熵系数 α=0），模型不仅学会了更高效的动作序列（平均步数减少约 0.94 步），还习得了更积极的探索行为（scroll 动作占比显著增加，Figure 4a）。

### 2. 适用边界与能力迁移

**短时程子任务 vs 长程导航。** WARC-Bench 的训练直接提升的是原子化子任务执行能力。Table 4 的分层规划实验提供了能力迁移的初步证据：将 Ours-72B-RLVR 作为执行器嵌入 Planner+Executor 架构后，在 WebArena-Lite 上的成功率从 SVA 基线的 16.17% 提升至 24.63%（+8.46 个百分点）。这表明子任务能力的提升确实有助于复杂工作流，但迁移效率有限——即使是最佳分层方案（24.63%）仍远低于 Claude-4.0-Sonnet 的 SVA 基线（36.32%）。这说明子任务执行能力是长程导航的必要但不充分条件，规划能力的瓶颈同样关键。

**域外泛化。** Table 7 的 ScreenSpot V2 评估（仅桌面/移动截图，排除训练中可能见过的网页截图）显示，Ours-72B-RLVR 达到 82.74% 成功率，显著超过 GPT-5（29.67%），但略低于其基座模型 Qwen2.5-VL 72B（87.42%）。RLVR 训练在提升子任务执行效率的同时，可能在纯视觉定位能力上有轻微退化（-4.68 个百分点），这需要进一步研究。

**强基座模型的分层增益递减。** Table 4 揭示了一个重要边界：分层 Planner+Executor 设计对较弱基座模型（Qwen2.5-VL-72B）有显著提升（+8.46%），但对强基座模型（Claude-4.0-Sonnet）反而略有下降（35.82% vs SVA 36.32%）。最优智能体框架依赖于基座模型的能力水平，不存在普适的架构优势。

### 3. 局限与已知失效模式

**环境覆盖盲区。** WARC 录制机制无法归档依赖 Cloudflare 防护、反爬虫机制或包含动态时间戳/会话 ID 的 URI 的网站。这意味着 WARC-Bench 的任务分布天然排除了部分高难度真实网页，可能导致评测结果对真实世界难度的低估。

**合成任务的验证瓶颈。** 虽然 WARC-Bench 支持合成网站的大规模生成，但任务目标和评估函数的可行性仍需人工验证。这一瓶颈限制了全自动扩展的闭环。

**前沿模型的子任务失误模式。** Claude Sonnet 4.0 在测试集上仅达 64.83%，其典型失败案例揭示了当前 GUI 智能体的深层缺陷：Figure 6 展示了日期格式错误（输入 YYYY/MM/DD 而非系统要求的格式），Figure 7 展示了未清除预填充文本字段。这些不是视觉定位失败，而是对 UI 控件语义约定的理解不足——这正是 WARC-Bench 设计所要暴露的“原子能力缺口”。

**离线 RL 的退化现象。** Table 5 的消融实验揭示了一个反直觉的结果：离线 GRPO 和 PPO 在 7B 模型上不仅未能提升 SFT 基线（66.54%），反而导致性能下降（GRPO_offline: 63.86%, PPO_offline: 61.76%）。仅在 72B 模型上，离线 GRPO 才略微超过 SFT（76.89% vs 75.88%）。在线 RLVR 是唯一在两个规模上均稳定提升的方案（7B: +5.59%, 72B: +8.43%）。这表明，在 GUI 子任务场景中，策略外数据的奖励建模误差可能淹没了离线 RL 的潜在收益。

### 4. 开放问题

1. **自动化扩展的闭环。** 如何进一步自动化 WARC-Bench 样本的生成与验证，使合成任务创建和奖励函数编写不再依赖人工检查，是实现大规模扩展的关键。

2. **子任务能力与长程规划的有机融合。** 本文仅提供了分层 Planner+Executor 的初步探索。子任务执行器能否通过代码生成、记忆增强或递归分解等架构更深度地嵌入通用长程代理，仍有待系统研究。

3. **离线 RL 为何在小模型上失败。** 离线 GRPO/PPO 在 7B 模型上的退化现象尚未得到充分解释。是否可以通过改进奖励建模（如学习奖励模型而非规则奖励）、增加策略约束或数据增强来弥合这一差距，是一个值得深入的方向。

4. **纯截图观察的信息损失。** SVA 仅使用截图作为观察，在可访问性树（A11y tree）信息丰富的场景中可能丢失了关键的结构化线索。如何在不显著增加上下文长度的前提下融合多模态观察，是提升子任务执行上限的潜在路径。

## 原文 PDF

![[paperPDFs/ICLR_2026/WARC_Bench_Web_Archive_based_Benchmark_for_GUI_Subtask_Executions.pdf]]
