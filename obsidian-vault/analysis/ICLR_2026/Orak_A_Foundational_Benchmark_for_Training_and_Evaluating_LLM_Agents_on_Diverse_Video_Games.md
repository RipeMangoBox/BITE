---
title: "Orak: A Foundational Benchmark for Training and Evaluating LLM Agents on Diverse Video Games"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Orak_A_Foundational_Benchmark_for_Training_and_Evaluating_LLM_Agents_on_Diverse_Video_Games.pdf
openreview_forum_id: H1ncX6O6Yh
aliases:
- Orak
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "通过MCP提供标准化的插件式接口，以及利用专家LLM游戏轨迹生成的微调数据集，实现通用游戏能力的评估与提升。"
primary_logic: "利用MCP统一接口可系统化评估各种LLM智能体，结合微调可将通用LLM转化为高效的游戏智能体，而专有模型在扩展的智能体工作流中收益更大。"
claims:
- "专有LLM在所有游戏上的平均排名显著优于开源LLM（Gemini-2.5-pro平均排名3.5，GPT-5/4o排名3.6）"
- "MCP接口实现了对智能体模块的独立研究，如反射、规划等"
- "微调专家轨迹提升小模型在游戏内、跨游戏甚至非游戏任务上的表现"
- "添加智能体模块（reflection-planning）对GPT-4o有显著提升，对小型LLM效果有限"
---

# Orak: A Foundational Benchmark for Training and Evaluating LLM Agents on Diverse Video Games

> [!tip] 核心洞察
> 利用MCP统一接口可系统化评估各种LLM智能体，结合微调可将通用LLM转化为高效的游戏智能体，而专有模型在扩展的智能体工作流中收益更大。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Orak：一个用于在多样化视频游戏上训练和评估LLM智能体的基础基准 |
| 英文题名 | Orak: A Foundational Benchmark for Training and Evaluating LLM Agents on Diverse Video Games |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=H1ncX6O6Yh); [GitHub](https://github.com/krafton-ai/Orak); [Project](https://huggingface.co/datasets/KRAFTON/Orak) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | Orak |
| Dataset | StarCraft II, Super Mario, 2048, Ace Attorney |

> [!tip] 效果简介
> - StarCraft II 上，Win Rate 为 GPT-4o 100.0±0.0，对比 Llama-3.2-1B 0.0±0.0，变化 +100.0。
> - Super Mario 上，Normalized Distance 为 Gemini-2.5-pro 38.0±14.6，对比 Llama-3.2-1B 18.7±8.6，变化 +19.3。
> - 2048 上，Normalized Score 为 o3 34.9±23.4，对比 Llama-3.2-1B 0.0±0.1，变化 +34.9。

## 概述

现有游戏基准（如GAMA-bench、GameBench、GameArena、SmartPlay、Balrog等）仅覆盖部分游戏类型（多为文本或2D网格），缺乏对智能体模块的系统消融支持，且不提供微调数据集，无法将预训练大语言模型（LLM）适应为通用游戏智能体。Orak针对这一瓶颈，提出以模型上下文协议（MCP）构建插件式统一接口，将12款涵盖六大游戏类型的视频游戏环境与反射、规划等智能体模块分别封装为独立MCP服务器，通过`eval.py`配置游戏、LLM后端和智能体策略即可完成标准化评估（Figure 1, Figure 2）。在此基础上，Orak利用专家LLM（如GPT-4o、o3-mini）的游戏轨迹构建约11k样本的高质量微调数据集，支持监督微调以提升小型LLM的游戏能力。

核心发现包括：专有LLM在所有游戏上的平均排名显著优于开源LLM（Gemini-2.5-pro平均排名3.5，GPT-5/4o排名3.6，而Llama-3.2-1B排名13.5，Table 3）；添加反射-规划等智能体模块对GPT-4o有显著提升（平均排名达2.2），但对小型LLM效果有限，甚至因提示复杂度增加而降低准确率（Table 4, Section 5.4）；仅使用图像输入会导致所有模型性能大幅下降（Table 5, Table 6）；微调专家轨迹不仅提升小模型在游戏内的表现，还展现出跨游戏甚至向非游戏任务（如Math500、WebShop）的正向迁移能力（Table 7）。

Orak在方法谱系中的定位：相较于此前基准仅支持单一或少数游戏类型、无智能体消融和微调支持，Orak是首个全面覆盖六大游戏类型、同时支持LLM/VLM、提供系统化智能体模块消融研究并发布微调数据集的基准（Table 1）。其MCP接口实现了对智能体模块的独立研究，而专家轨迹微调机制则将通用LLM转化为高效游戏智能体。主要局限包括部分游戏需用户自行购买商业许可、仅探索了监督微调而未涉及强化学习微调、评估时暂停游戏未能反映实时需求、以及视觉和多模态输入的利用仍不充分。

## 背景与动机

### 核心瓶颈：通用游戏智能体的评估与训练缺失

大语言模型（LLM）在文本推理、代码生成等静态任务中已展现强大能力，但在动态、交互式的视频游戏环境中，将其转化为通用游戏智能体仍面临根本性障碍。现有游戏基准存在三个系统性缺口：

1. **游戏类型覆盖碎片化**：如 GAMA-bench、GameBench、GameArena、SmartPlay、Balrog、Cradle 等基准仅覆盖部分游戏类型（文本冒险、2D网格等），无法全面评估智能体在动作、冒险、角色扮演、模拟、策略、解谜六大主流类型中的表现（Table 1）。这导致不同基准之间的结果难以横向比较，也无法揭示LLM在不同认知维度上的能力边界。

2. **智能体模块无法独立研究**：现有基准大多将LLM调用与游戏交互紧耦合，不支持对反射（reflection）、规划（planning）、技能管理（skill management）等智能体模块进行系统消融。研究者无法区分性能提升究竟来自LLM本身的能力，还是来自智能体工作流的贡献。

3. **缺乏微调支持**：此前没有任何基准提供可用于监督微调（SFT）的专家游戏轨迹数据集。这意味着预训练LLM无法通过游戏交互数据适应特定游戏环境，限制了从通用LLM到专用游戏智能体的转化路径。

### 因果机制：MCP接口与专家轨迹微调

Orak通过两个关键设计突破上述瓶颈：

- **MCP（Model Context Protocol）插件式接口**：每个游戏环境和智能体模块作为独立的MCP服务器运行，向LLM暴露标准化的工具调用接口（Figure 2）。游戏服务器提供状态检索与动作执行功能，智能体服务器提供反射、规划等可调用策略。这种解耦设计使得评估流水线（`eval.py`）只需配置游戏、LLM后端（`llm.py`）和智能体策略（`agent.py`）即可运行，实现了系统化的消融研究。

- **专家轨迹微调数据集**：从GPT-4o、o3-mini等专家LLM在全部12款游戏上使用多种智能体模块的游戏轨迹中，筛选高分轨迹（每款游戏>300条推理序列），构建约11k样本的SFT数据集（Section 4）。数据增强通过GPT-4o改写游戏提示生成10倍扩充样本，进一步提升数据多样性。

### 核心洞察

Orak的核心理念在于：**统一的MCP接口使跨游戏、跨智能体模块的系统评估成为可能**，而**专家轨迹微调可将通用LLM转化为高效游戏智能体**。实验揭示了一个关键发现：专有LLM（如GPT-4o）在扩展的智能体工作流（如reflection-planning）中收益显著，而小型开源LLM添加相同模块反而可能因提示复杂度增加而性能下降（Table 4, Section 5.4）。这表明智能体策略的最优选择与模型容量密切相关，为后续研究指明了方向。

### 证据强度说明

- **高置信度**：MCP接口的模块化解耦设计（Figure 2）和微调数据集的构建流程（Section 4）有明确的技术描述支撑。
- **需注意**：论文未提供MCP接口的延迟开销定量分析，实时游戏场景下的实用性需进一步验证。
- **待验证**：微调从游戏到非游戏任务（Math500、WebShop）的正向迁移（Table 7）虽被报告，但迁移机制（是通用推理能力提升还是任务格式适应）尚未被严格分离。

## 核心创新

Orak 的核心创新在于通过**MCP（Model Context Protocol）插件化接口**统一了多样化视频游戏的评估与训练流程，系统性地填补了现有基准在**游戏类型覆盖、智能体模块消融、微调数据集**三个关键维度上的空白（Table 1）。

### 1. MCP 驱动的标准化评估与模块解耦

Orak 将每个游戏环境和智能体模块（如反射、规划、技能管理）封装为独立的 MCP 服务器，通过 `eval.py` 统一调度（Figure 2）。这一设计实现了两个层面的解耦：

- **游戏环境与LLM后端的解耦**：用户只需在 `eval.py` 中配置游戏、LLM后端和智能体策略，无需为每个游戏编写定制接口。这解决了现有基准（如 GAMA-bench、GameBench、Balrog 等）中“每个游戏一套接口”的碎片化问题。
- **智能体模块的独立可研究性**：反射、规划等模块作为可调用工具独立存在，使得研究者可以系统性地消融各模块对不同LLM的贡献（Section 5.4）。这是此前基准普遍缺失的能力（Table 1 中 Agent Ablation 列仅 Orak 标记为 ✓）。

### 2. 全类型游戏覆盖与能力需求量化

Orak 覆盖了动作、冒险、RPG、模拟、策略、解谜六大游戏类型的 12 款游戏，是首个实现“Full Genre”覆盖的基准（Table 1）。通过 8 名人类参与者对每款游戏所需 LLM 能力（如空间推理、长期规划、实时决策）进行 1-3 级评分（Figure 3），Orak 为不同游戏的能力需求提供了可量化的参考框架，使性能差异可以追溯到具体能力瓶颈。

### 3. 专家轨迹微调数据集

Orak 首次为游戏智能体基准提供了**结构化微调数据集**（Table 1 中 Fine-tuning Set 列仅 Orak 为 ✓）。该数据集由 GPT-4o 和 o3-mini 等专家 LLM 在多种智能体模块下玩游戏生成，经高分筛选后保留约 11k 样本，并通过 GPT-4o 改写游戏提示进行 10 倍数据增强（Section 4）。这一设计使得研究者可以直接研究“从通用LLM到游戏智能体”的微调迁移效应，包括跨游戏泛化甚至向非游戏任务（如 Math500、WebShop）的正向迁移（Table 7）。

### 4. 关键发现与因果机制

- **专有模型的模块增益显著**：GPT-4o 在 “reflection-planning” 智能体下平均排名达到 2.2（Table 4），而小型开源模型（如 Llama-3.2-3B）添加同类模块反而因提示复杂度增加导致准确率下降（Section 5.4）。这表明智能体工作流的收益存在**模型容量门槛**。
- **视觉模态的利用仍是瓶颈**：仅图像输入导致所有模型性能大幅下降（Table 5, 6），且图文融合未带来稳定提升，说明当前 VLM 从原始画面中提取游戏语义的能力严重不足。
- **微调数据的质量与规模存在最优区间**：高质量轨迹微调优于低质量数据，数据增强在 3~10 倍范围内效果最佳（Table 8(a)），过度增强可能引入噪声。

### 5. 相对于基准的 changed slots 总结

| 维度 | 现有基准 | Orak |
|------|---------|------|
| 游戏类型覆盖 | 部分（文字/2D网格为主） | 六大类型全覆盖（12款游戏） |
| 智能体模块消融 | 基本不可用 | 系统化消融研究 |
| 微调数据集 | 未提供 | 专家轨迹 SFT 数据集（~11k） |
| 接口标准化 | 每游戏定制 | MCP 插件化统一接口 |

## 整体框架

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_H1ncX6O6Yh/figures/001_Figure_1.jpg]]
*Figure 1: Overview of Orak, a benchmark designed to train and evaluate LLM agents across 12 video games across genres. Using MCP as a plug-and-play interface, it ensures systematic assessment, supporting gameplay leaderboards, battle arenas, and studies on agentic modules and fine-tuning*

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_H1ncX6O6Yh/figures/002_Table_1.jpg]]
*Table 1: Game Benchmark Comparison. ‘Full Genre’ means whether six major genres are fully covered. ‘Model Type’ indicates whether the benchmark supports LLMs or VLMs. Unlike prior benchmarks, Orak is the only benchmark that fully covers all major genres, supports both LLMs/VLMs, provides ablation studies for agent modules, and releases a fine-tuning set*

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_H1ncX6O6Yh/figures/004_Figure_2.jpg]]
*Figure 2: Evaluation pipeline of Orak. Game scores are computed via eval.py by simply configuring game, LLM backbone, and agentic strategy. Orak supports two types of submissions: (1) customizing llm.py with new backbone LLMs, and (2) customizing agent.py with new agentic strategies. The agentic strategies are callable by LLMs via MCP interface in eval.py (in grey box). Figure 3: LLM capabilities required to play 12 games in Orak. The color theme (red, yellow, etc) represents game genres. See Appendix A for genre categorization details*

Orak 的整体设计围绕一个核心洞察展开：**通过 MCP（Model Context Protocol）统一接口，可以将多样化的游戏环境与可插拔的智能体模块解耦，从而实现对 LLM 游戏智能体的系统化评估与训练**。现有游戏基准（如 GAMA-bench、GameBench、GameArena、SmartPlay、Balrog 等）普遍存在游戏类型覆盖不全、缺乏智能体模块消融支持、未提供微调数据集等瓶颈（Table 1）。Orak 通过标准化流水线填补了这一空白。

### 架构总览

Orak 的架构（Figure 1）由三个核心层构成：

1. **游戏环境层**：涵盖 6 大类型的 12 款视频游戏，覆盖动作、冒险、RPG、模拟、策略、解谜等全部主流类型（Table 1）。
2. **MCP 接口层**：每个游戏环境和智能体模块包均作为独立的 MCP Server 运行，分别提供游戏机制（如检索游戏状态、执行游戏步骤）和智能体策略（如反思、规划）作为可调用工具（Section 3）。
3. **评估与训练层**：通过 `eval.py` 统一调度，用户仅需配置游戏、LLM 后端和智能体策略即可完成评估（Figure 2）。

### 评估流水线

评估流水线（Figure 2）的核心组件包括：

- **`eval.py`**：评估入口，负责编排整个评估流程。用户在配置文件中指定游戏名称、LLM 后端和智能体策略后，`eval.py` 自动完成游戏状态获取、LLM 推理调用和动作执行。
- **`llm.py`**：LLM 后端接口，支持用户自定义任意 LLM 后端（包括专有和开源模型），实现即插即用的模型替换。
- **`agent.py`**：智能体策略接口，支持用户自定义智能体策略（如 zero-shot、reflection、planning、reflection-planning 等），通过 MCP 接口调用智能体模块 Server 提供的工具。
- **Game Environment MCP Server**：封装游戏环境，将游戏状态检索和动作执行暴露为标准化工具，供 LLM 调用。
- **Agentic Module MCP Server**：封装智能体模块（如反思、规划、技能管理），将高级认知策略暴露为可调用工具。

Orak 支持两种提交模式：（1）通过自定义 `llm.py` 接入新的 LLM 后端；（2）通过自定义 `agent.py` 实现新的智能体策略。这种设计使得对智能体模块的独立研究成为可能——这是先前基准所不具备的关键能力（Table 1）。

### 能力需求评估

为系统化衡量游戏对 LLM 的能力要求，Orak 采用了一套原则性标准（Figure 3）。8 名人类参与者在 1-3 的尺度上评估每款游戏对各项能力（如空间推理、长期规划、实时决策等）的需求程度，最终报告中等值。这一评估揭示了不同游戏类型对 LLM 能力的差异化需求，为后续分析模型性能差异提供了结构化框架。

### 微调数据流

Orak 还提供了首个面向通用游戏智能体的微调数据集（约 11k 样本），其构建流程为：

1. **轨迹收集**：使用专家 LLM（如 GPT-4o、o3-mini）在全部 12 款游戏上运行多种智能体模块，生成游戏轨迹 $\mathcal{T} = \{\tau_1, ..., \tau_T\}$。
2. **数据筛选**：按游戏得分排序，保留得分最高的轨迹，直至选中轨迹数超过 300。
3. **数据增强**：使用 GPT-4o 对每个样本的游戏提示 $X^a$ 进行改写，生成 10 个增强样本，同时保留所有游戏相关信息。

每条轨迹 $\tau = \{(X^{a_i}, S, Y^{a_i})\}_{i=1}^{n}$ 包含 $n$ 次 LLM 推理序列，其中 $a_i$ 为智能体模块，$S$ 为游戏状态，$Y^a$ 为 LLM 响应。该数据集主要用于监督微调（SFT），强化学习微调留待未来工作。

## 核心模块与公式推导

### 评估流水线核心模块

Orak的评估流水线由五个核心模块构成，通过MCP（Model Context Protocol）实现插件式解耦（Figure 2）。每个游戏环境和智能体模块包作为独立的MCP服务器运行，将游戏机制（如检索游戏状态、执行游戏步骤）或智能体策略（如反思、规划）作为可调用工具暴露给LLM。

**Game Environment MCP Server**：封装游戏状态检索与动作执行功能，为LLM智能体提供标准化的游戏交互接口。该模块负责将异构游戏（涵盖动作、冒险、RPG、模拟、策略、解谜六大类）统一为结构化的文本状态表示。

**Agentic Module MCP Server**：提供反思（reflection）、规划（planning）、技能管理等可调用工具。LLM可在推理过程中自主选择调用这些模块，形成可扩展的智能体工作流。消融实验表明，添加“reflection-planning”模块对GPT-4o有显著提升（平均排名2.2），但对小型LLM（如Llama-3.2-3B）可能因提示复杂度增加而降低决策准确率（Table 4, Section 5.4）。

**eval.py**：评估入口脚本，负责配置游戏、LLM后端和智能体策略，计算最终游戏得分。用户可通过自定义`llm.py`提交新后端LLM，或通过自定义`agent.py`提交新智能体策略。

**llm.py** 与 **agent.py**：分别允许用户自定义LLM后端和智能体策略，支持灵活的实验配置和可复现研究。

### 关键公式

**Elo预期胜率**（Appendix C.4）：

$$P(i \text{ beats } j) = \frac{1}{1 + 10^{(R_j - R_i)/400}}$$

其中 $R_i$、$R_j$ 分别为智能体 $i$ 和 $j$ 的Elo评分。该公式用于计算竞技场（Street Fighter III、StarCraft II）中智能体间的预期胜率，支撑对战排名系统的构建。

**Darkest Dungeon复合得分**（Appendix H.3）：

$$\text{Score} = \begin{cases} 
40 \cdot \left( \frac{\# \text{combats cleared}}{\# \text{total combats}} \right) + 30 \cdot \left( \frac{\# \text{heroes survived}}{4} \right) + 30 \cdot \left( 1 - \frac{\text{total stress}}{800} \right), & \text{if stage is cleared} \\ 
40 \cdot \left( \frac{\# \text{combats cleared}}{\# \text{total combats}} \right), & \text{otherwise}
\end{cases}$$

该公式综合了战斗清除比例、英雄存活数量和压力管理三个维度：清除关卡时，战斗清除占40%权重，英雄存活和压力管理各占30%；未清除关卡时仅计算战斗清除比例。这种多维度设计确保了对策略深度和资源管理能力的全面评估。

**奖励折扣估计**（Section T，RL微调讨论部分）：

$$R_t = \gamma^{T-t} S_{\text{final}}$$

使用折扣因子 $\gamma$ 从最终游戏得分 $S_{\text{final}}$ 反向估算中间时间步 $t$ 的奖励，为未来强化学习微调提供信用分配基础。

**混合回合奖励**（Section T）：

$$R_t = \lambda S_t + (1-\lambda) \gamma^{T-t} S_{\text{final}}$$

混合当前回合分数 $S_t$ 与折扣后的最终分数，通过 $\lambda$ 控制即时反馈与长期目标的权衡，旨在实现更平滑的功劳分配。该方法目前仅作为RL微调方向的讨论，尚未在实验中验证。

## 实验与分析

### 核心结果：专有模型全面领先，能力鸿沟显著

Orak在12款涵盖6大类型的视频游戏上对15个LLM进行了系统评估（默认零样本智能体策略）。**Table 3** 汇总了各模型归一化后的游戏得分与平均排名，揭示了清晰的性能分层：

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_H1ncX6O6Yh/figures/006_Table_3.jpg]]

- **Gemini-2.5-pro** 综合表现最优，在12款游戏中的5款上排名第一，平均排名 **3.5**，展现出最强的通用游戏能力。
- **GPT-5** 与 **GPT-4o** 紧随其后，平均排名均为 **3.6**。GPT-5在解谜类游戏（*Baba Is You*、*2048*）上具有显著优势，而GPT-4o在*StarCraft II*上达到 **100%** 胜率（Table 35）。
- **开源模型与专有模型之间存在巨大鸿沟**：表现最好的开源模型 **Qwen3-235B** 平均排名仅 **7.3**，而最小的 **Llama-3.2-1B** 平均排名垫底（**13.5**），在多数游戏上完全无法有效操作（如*2048*归一化得分 0.0±0.1，*Ace Attorney*综合得分 1.3±2.2）。

这一结果表明，当前开源LLM在需要长程规划、空间推理和复杂状态追踪的游戏环境中，与顶级专有模型存在根本性的能力差距。

### 竞技场对战：格斗与策略的差异化表现

在*Street Fighter III*和*StarCraft II*的对战竞技场中（**Figure 4**），模型表现呈现出与主基准不同的格局：

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_H1ncX6O6Yh/figures/009_Figure_4.jpg]]
*Figure 4: Match outcomes and Elo ratings for LLMs in two competitive environments. Table 4: Ablation study for agentic modules. ‘Ref-Plan’ refers to the ‘Reflection-Planning’ agent*

- **Street Fighter III**：**Minitron-8B** 出人意料地获得最高Elo评分，表明小型模型在反应速度敏感、策略深度较浅的格斗游戏中可能具有独特优势。
- **StarCraft II**：专有模型（GPT-4o、Gemini-2.5-pro）在对战中保持统治地位，反映了实时战略游戏对高层策略规划和资源管理的更高要求。

这种差异揭示了游戏类型对智能体能力的差异化需求：格斗游戏更依赖快速反应和局部模式匹配，而策略游戏则考验全局规划与长期推理。

### 智能体模块消融：大模型受益，小模型受损

**Table 4** 的消融实验揭示了智能体模块（反射、规划）对不同规模LLM的异质性影响：

- **对GPT-4o**：“reflection-planning”智能体在所有游戏中表现最佳，平均排名 **2.2**，相比基础零样本策略有显著提升。这表明专有模型能够有效利用结构化的反思与规划工作流来改进决策质量。
- **对Llama-3.2-3B**：添加反射模块后平均排名从 **4.9** 恶化至 **5.6**，添加反射-规划模块后进一步恶化至 **6.1**。论文分析认为，模块引入的额外提示增加了上下文复杂度，超出了小型模型的指令遵循和处理能力，反而干扰了基础决策。

这一发现指向一个关键的瓶颈：**智能体工作流的收益与模型基础能力之间存在阈值效应**。小型模型缺乏足够的推理容量来消化和利用结构化的元认知信息。

### 模态消融：视觉输入仍是瓶颈

模态比较实验（**Table 5, Table 6**）将游戏分为两组：Group 1（文本状态可从视觉截图推导）和Group 2（文本状态包含当前帧之外的长期信息）。核心发现：

- **纯图像输入导致所有模型性能大幅下降**。在Group 1中，各模型的平均排名相比纯文本输入显著恶化，说明当前VLM从原始游戏画面中提取结构化状态信息的能力严重不足。
- **图文双模态融合并未带来稳定提升**。在*Street Fighter III*中，Claude的得分因图像输入提升了16.6分，但在*Ace Attorney*中，GPT-4o的得分下降了31.8分。融合效果高度依赖游戏类型和模型架构，未形成一致的正向趋势。

这暴露了当前多模态LLM在游戏场景中的核心缺陷：视觉编码器无法可靠地将游戏截图转化为可供推理使用的精确状态表示，反而可能引入噪声。

### 微调与泛化：从游戏到非游戏的正向迁移

基于专家LLM（GPT-4o、o3-mini）游戏轨迹构建的约11k样本微调数据集（**Section 4**），Orak系统性地研究了监督微调的泛化效果（**Table 7**）：

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_H1ncX6O6Yh/figures/012_Table_7.jpg]]
*Table 7: Generalization performance of LLMs fine-tuned on expert gameplay trajectories from Orak*

- **游戏内泛化**：微调后的Llama-3.2-1B/3B在5款游戏中的3款上超越了预训练基线，但在*Baba Is You*等需要空间推理的游戏中未见提升，说明SFT难以弥补模型在特定推理能力上的先天不足。
- **跨游戏泛化**：在未见的OOD游戏（*Super Mario*、*2048*）上，微调模型表现显著优于预训练模型，证明游戏操作中的通用策略（如状态理解、动作选择）具有可迁移性。
- **非游戏泛化**：这是一个引人注目的发现——在Orak游戏轨迹上微调的LLaMA-3.2-3B，在数学推理（Math500）和网页交互（WebShop）任务上也取得了提升（WebShop得分从0.0%提升至8.4%~12.6%）。这表明游戏环境中的序列决策训练可能培养了通用的推理和工具使用能力。

**数据质量与规模的影响**（**Table 8(a)**）：高质量（高分）轨迹的微调效果显著优于低质量数据；数据增强（GPT-4o改写游戏提示）在3~10倍增强范围内效果最佳，过度增强收益递减。

### 实时性能：暂停评估的局限性

Orak默认将游戏暂停以消除推理延迟对能力度量的干扰，但**Table 8(b)** 的实时评估揭示了严峻的现实：

- 在暂停模式下，所有模型在*StarCraft II*简单和困难难度均达到 **100%** 胜率。
- 切换到实时模式后，**所有模型在困难难度完全失败**（胜率 0%），即使在简单难度下，性能也大幅下降（GPT-4o-mini从100%降至33.3%）。

这一对比暴露了当前LLM智能体的根本局限：**推理延迟使其无法应对实时决策需求**。模型响应时间（GPT-4o约1.2秒，Gemini-2.5-pro约2.5秒）在暂停评估中无关紧要，但在实时环境中成为致命瓶颈。这指向一个待解决的核心问题：如何在保持推理质量的同时将延迟降低到实时可用的水平。

## 方法谱系与知识库定位

### 1. 基准设计谱系与差异化定位

Orak 定位为“基础性游戏基准”，其核心设计动机源于对现有游戏基准在**领域覆盖、模块化评估和训练支持**三个维度上的系统性不足的回应。Table 1 将 Orak 与 10 个先验游戏基准进行了全面比较，揭示了当前领域的结构性缺口：

| 基准 | 游戏领域 | 全类型覆盖 | 游戏数 | 模型类型 | 智能体消融 | 微调集 |
|------|---------|-----------|--------|---------|-----------|--------|
| GAMA-bench | 文本/2D网格 | ✗ | 多个 | LLM | ✗ | ✗ |
| GameBench | 文本/2D网格 | ✗ | 多个 | LLM | ✗ | ✗ |
| GameArena | 文本/2D网格 | ✗ | 多个 | LLM | ✗ | ✗ |
| SmartPlay | 文本/2D网格 | ✗ | 多个 | LLM | ✗ | ✗ |
| Balrog | 文本/2D网格 | ✗ | 多个 | LLM | ✗ | ✗ |
| LVLM-Playground | 文本/2D网格 | ✗ | 多个 | VLM | ✗ | ✗ |
| Cradle | 文本/2D网格 | ✗ | 多个 | LLM | ✗ | ✗ |
| V-MAGE | 文本/2D网格 | ✗ | 多个 | VLM | ✗ | ✗ |
| DSGBench | 文本/2D网格 | ✗ | 多个 | LLM | ✗ | ✗ |
| LMGame-Bench | 文本/2D网格 | ✗ | 多个 | LLM | ✗ | ✗ |
| **Orak** | **完整视频游戏** | **✓ (6类)** | **12** | **LLM/VLM** | **✓** | **✓ (约11k)** |

**关键差异化机制**：
- **领域覆盖**：先验基准局限于文本游戏或2D网格环境，Orak 首次覆盖动作、冒险、角色扮演、模拟、策略、解谜六大类型的完整视频游戏，使评估更贴近真实游戏场景的复杂性和多样性。
- **接口标准化**：基于 MCP 的插件式接口（Figure 2）将游戏环境与智能体模块解耦为独立服务器，解决了先验基准中“每个游戏定制接口”导致的不可复现和不可比较问题。这一设计使智能体策略（反射、规划、技能管理）成为可独立研究和消融的模块，而非与游戏逻辑耦合的黑箱。
- **训练支持**：Orak 是首个提供专家轨迹微调数据集的游戏基准，将基准从单纯的“评估工具”扩展为“训练平台”，填补了从预训练 LLM 到通用游戏智能体之间的适应空白。

### 2. 适用边界

**适用场景**：
- **LLM/VLM 智能体的系统化评估**：Orak 通过统一接口支持对骨干模型、智能体策略和输入模态的独立消融研究，适用于研究不同 LLM 在多样化游戏场景下的能力边界。
- **游戏能力的监督微调**：专家轨迹数据集（约 11k 样本）支持将小型开源 LLM 微调为游戏智能体，并在游戏内、跨游戏甚至非游戏任务上观察泛化能力（Table 7）。
- **对战竞技场评估**：Street Fighter III 和 StarCraft II 的 Elo 竞技场（Figure 4）为研究 LLM 在多智能体竞争环境中的策略推理提供了标准化平台。

**不适用或需谨慎使用的场景**：
- **实时游戏性能评估**：当前评估将游戏暂停以消除推理延迟对能力度量的干扰（Table 8(b)），因此不适用于衡量 LLM 在真实实时约束下的表现。实验表明，在实时模式下所有模型在困难等级完全失败，这揭示了当前 LLM 推理延迟与实时游戏需求之间的根本性矛盾。
- **视觉主导的游戏场景**：纯图像输入导致所有模型性能大幅下降（Table 5, Table 6），多模态融合也未带来稳定提升。Orak 目前依赖结构化的文本状态表示，其评估结果不能直接推广到需要从原始像素中提取语义的视觉游戏场景。
- **音频感知场景**：未支持音频模态，限制了在 FPS 等依赖声音线索的游戏类型中的全面感知评估。

### 3. 局限与开放问题

**已确认的局限**（来自论文明确讨论）：
1. **商业游戏的可访问性**：六款游戏需用户自行购买（9.99–24.99 美元），增加了基准使用的经济门槛，但论文指出这一成本相对于 API 调用成本较小。
2. **微调范式的局限**：仅探索了监督微调（SFT），未研究强化学习微调（如 DPO、GRPO）以利用游戏过程中的动态反馈信号。论文在讨论中提出了基于奖励折扣的 RL 微调框架（$R_t = \gamma^{T-t} S_{\mathrm{final}}$ 和 $R_t = \lambda S_t + (1-\lambda) \gamma^{T-t} S_{\mathrm{final}}$），但尚未实现。
3. **实时推理瓶颈**：暂停评估模式掩盖了 LLM 推理延迟问题，实时模式下所有模型在困难等级完全失败，表明当前 LLM 的推理速度远未达到实时游戏的需求。
4. **视觉输入利用不足**：尽管支持多模态输入，但纯图像输入导致性能崩溃，文本+图像融合也未带来一致提升，说明当前 VLM 从游戏截图中提取有效信息的能力仍然有限。
5. **依赖结构化文本表示**：未在完全未整理的原始游戏状态上进行评估，依赖结构化的文本状态表示，这可能高估了 LLM 在真实游戏环境中的感知能力。

**开放问题**（论文提出或隐含的未解决问题）：
1. **最优智能体策略与模型容量的关系**：实验表明，添加反射-规划模块对 GPT-4o 有显著提升（平均排名 2.2），但对小型 LLM（如 Llama-3.2-3B）可能因提示复杂度增加而降低准确率。不同规模的 LLM 的最优智能体策略是什么？小型模型如何从反射、规划模块中获益？
2. **视觉-语言融合的有效机制**：为什么文本+图像融合在某些游戏中提升性能（如 Claude 在 Street Fighter III 得分增加 16.6），而在其他游戏中反而下降（如 GPT-4o 在 Ace Attorney 得分下降 31.8）？如何改进视觉输入的利用，使多模态输入真正提升游戏性能？
3. **游戏到非游戏泛化的最小模型容量**：Table 7 显示 Llama-3.2-3B 微调后从游戏泛化到 Math500 和 WebShop，但 1B 模型未见明显提升。从游戏微调泛化到非游戏推理任务的最小模型容量需求是什么？
4. **实时性能的可行路径**：如何在保持低延迟的同时实现高难度的实时游戏性能？这是否需要模型架构的根本性改进，还是可以通过推理优化策略解决？
5. **音频模态的增量价值**：音频模态的引入能在多大程度上增强 LLM 智能体在游戏中的表现？特别是在 FPS 等依赖声音定位的游戏类型中。
6. **RL 微调的集成与效果**：如何将 RL 微调（如 DPO、GRPO）集成到 Orak 环境中以提升多智能体战略推理？论文提出的奖励折扣框架（$R_t = \gamma^{T-t} S_{\mathrm{final}}$ 和 $R_t = \lambda S_t + (1-\lambda) \gamma^{T-t} S_{\mathrm{final}}$）的实际效果有待验证。

## 原文 PDF

![[paperPDFs/ICLR_2026/Orak_A_Foundational_Benchmark_for_Training_and_Evaluating_LLM_Agents_on_Diverse_Video_Games.pdf]]
