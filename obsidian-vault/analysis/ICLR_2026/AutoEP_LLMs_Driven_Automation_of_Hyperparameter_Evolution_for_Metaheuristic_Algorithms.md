---
title: "AutoEP: LLMs-Driven Automation of Hyperparameter Evolution for Metaheuristic Algorithms"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AutoEP_LLMs_Driven_Automation_of_Hyperparameter_Evolution_for_Metaheuristic_Algorithms.pdf
openreview_forum_id: hit3hGBheP
aliases:
- AutoEP
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning
core_operator: "LLM的零样本推理能力与基于探索性景观分析（ELA）的实时状态反馈相结合，通过结构化多智能体协同（CoR）将搜索动态转化为可解释的超参数调节策略。"
primary_logic: "将LLM定位为高层监督者而非搜索算子，利用在线ELA特征为LLM提供可量化的搜索状态，并通过多LLM推理链（Strategist-Analyst-Actuator）分解控制任务，实现零样本、训练无关的超参数动态适配。"
claims:
- "AutoEP在TSP、CVRP、FSSP、UAV轨迹优化等多个组合优化基准上一致超越现有超参数调优方法（PT、GLEET、BEA）及LLM增强方法（EoH、ReEvo）。"
- "消融研究表明ELA和CoR组件均不可或缺：移除任一组件性能显著下降，移除两者则性能低于未调优基线。"
- "基于Qwen3-30B的CoR架构在性能上与GPT-4等超大模型相当，但推理时间减少一个数量级（5.8 min vs 44.7+ min on eil51）。"
- "AutoEP对底层LLM能力具有鲁棒性，即使使用较小模型仍能保持高性能，而EoH和ReEvo性能显著下降。"
---

# AutoEP: LLMs-Driven Automation of Hyperparameter Evolution for Metaheuristic Algorithms

> [!tip] 核心洞察
> 将LLM定位为高层监督者而非搜索算子，利用在线ELA特征为LLM提供可量化的搜索状态，并通过多LLM推理链（Strategist-Analyst-Actuator）分解控制任务，实现零样本、训练无关的超参数动态适配。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AutoEP：基于大语言模型的元启发式算法超参数进化自动化 |
| 英文题名 | AutoEP: LLMs-Driven Automation of Hyperparameter Evolution for Metaheuristic Algorithms |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=hit3hGBheP); [GitHub](https://github.com/YiZheZhang12/AutoEP) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning |
| Method | AutoEP |
| Dataset | TSP eil51, TSP dsj1000, CVRP N=200, FSSP n20m10 |

> [!tip] 效果简介
> - TSP eil51 上，Opt.gap(%) 为 0.00 (GA-2opt+AutoEP)，对比 0.17 (GA-2opt)，变化 -0.17。
> - TSP dsj1000 上，Opt.gap(%) 为 3.58 (GA-2opt+AutoEP)，对比 7.14 (GA-2opt)，变化 -3.56。
> - CVRP N=200 上，Opt.gap(%) 为 1.08 (GA-2opt+AutoEP)，对比 5.89 (GA-2opt)，变化 -4.81。

## 概述

### 1. 问题与瓶颈

元启发式算法（如遗传算法、粒子群优化、蚁群优化）是求解复杂组合优化问题的核心工具，但其性能高度依赖于超参数（如交叉率、变异率、信息素蒸发率）的选择。现有超参数调优方法面临双重瓶颈：

- **训练成本高昂**：基于规则的方法（如 **PT**，Joshi & Bansal, 2020）依赖人工经验，深度强化学习方法（如 **GLEET**，Ma et al., 2024）和贝叶斯优化方法（如 **BEA**，Lan et al., 2022）则需大量离线训练或元训练，泛化性差。
- **缺乏搜索动态感知**：现有方法通常仅依据简单指标（如迭代次数）进行静态调参，无法实时感知种群分布、景观结构和搜索进展，导致调控滞后或失配。

### 2. 核心思路

AutoEP 将大语言模型定位为**高层监督者**而非搜索算子，通过以下机制实现零样本、免训练的超参数动态适配：

- **在线 ELA 状态感知**：在搜索过程中实时计算 5 个探索性景观分析特征（偏度、峰度、决定系数 $R^2$、分散比 $D_{ratio}$、变化率 $V$），将种群适应度分布、景观结构、多样性和搜索进展量化为可解释的状态信号。
- **多智能体推理链（CoR）**：将控制任务分解为 Strategist（生成超参数控制映射）、Analyst（基于 ELA 和经验池诊断搜索状态，决定探索/利用策略）和 Actuator（将策略指令转化为具体超参数值）三个 LLM 智能体的协作推理链，使 LLM 推理始终锚定在经验证据之上。

### 3. 方法定位

| 维度 | 现有方法 | AutoEP |
|------|---------|--------|
| 调优方式 | 手工规则 / DRL / 贝叶斯优化 | LLM 多智能体零样本推理闭环控制 |
| 状态表征 | 简单指标或无/间接状态 | 在线 5 维 ELA 特征 |
| 决策逻辑 | 单一 LLM 或规则 | 多 LLM 推理链（Strategist-Analyst-Actuator） |
| 训练需求 | 需离线训练/元训练 | 完全零样本/免训练 |

AutoEP 区别于 **EoH**（Liu et al., 2024）和 **ReEvo**（YE et al., NeurIPS 2024）等基于 LLM 的元启发式增强方法：后两者将 LLM 用于生成搜索算子或启发式，而 AutoEP 将 LLM 用作超参数调优的闭环控制器，且通过 ELA 特征和结构化 CoR 显著降低幻觉风险。

### 4. 主要结果

在 TSP、CVRP、FSSP 和 UAV 轨迹优化四个组合优化基准上，AutoEP 一致超越现有超参数调优方法及 LLM 增强方法：

- **TSP**：GA-2opt+AutoEP 在 eil51 上达到 0.00% 最优间隙，在 dsj1000 上将最优间隙从 7.14% 降至 3.58%（Table 1）。
- **CVRP**：N=200 规模上，GA-2opt+AutoEP 将最优间隙从 5.89% 降至 1.08%（Table 5）。
- **FSSP**：n20m10 规模上，GA-2opt+AutoEP 将最优间隙从 4.37% 降至 2.09%（Table 6）。
- **UAV 轨迹优化**：ACO+AutoEP 将 N=300 规模的轨迹长度从 1912.74 降至 1574.90（Table 7）。

消融实验（Table 2）证实 ELA 和 CoR 均为关键组件：移除任一组件性能显著下降，同时移除两者则性能劣于未调优基线。基于 Qwen3-30B 的 CoR 架构在性能上与 GPT-4 等超大模型相当，但推理时间减少一个数量级（eil51 上 5.8 min vs 44.7+ min，Table 3）。此外，AutoEP 对底层 LLM 能力具有鲁棒性，即使使用较小模型仍能保持高性能（Figure 4），而 EoH 和 ReEvo 在相同条件下性能显著下降。

### 5. 局限与开放问题

- AutoEP 引入额外 2–5 分钟推理开销，对极度时间敏感的任务需权衡。
- 当前验证集中于组合优化问题，向连续优化问题的迁移能力待验证。
- ELA 特征选择依赖专家先验，对新型黑箱算法的泛化性尚未探讨。
- CoR 框架的级联失败风险未深入分析。
- 能否扩展至多目标优化、带约束优化或深度神经网络超参数调优，仍为开放问题。

## 背景与动机

### 元启发式算法的超参数困境

元启发式算法（如遗传算法GA、粒子群优化PSO、蚁群优化ACO）在求解旅行商问题（TSP）、容量约束车辆路径问题（CVRP）、流水车间调度问题（FSSP）等组合优化任务时，其性能高度依赖超参数配置。种群大小、交叉率、变异率、信息素挥发因子等参数直接影响搜索过程中探索（exploration）与开发（exploitation）的动态平衡。然而，这些参数的最佳取值并非静态——它们应当随搜索阶段、问题景观特征和种群状态而动态变化。

### 现有调优范式的结构性缺陷

当前主流的超参数调优方法可分为三类，各自存在根本性局限：

**基于规则的方法**（如PT, Joshi & Bansal, 2020）依赖人工设计的启发式策略（如按迭代次数线性衰减变异率），虽然简单但缺乏对实时搜索状态的感知能力，无法适应不同问题实例的景观差异。

**基于学习的方法**将超参数控制建模为序列决策问题。其中，深度强化学习方法（如GLEET, Ma et al., 2024）需要大量离线训练，且训练好的策略难以泛化到未见过的算法-问题组合；贝叶斯优化方法（如BEA, Lan et al., 2022）虽能自动搜索参数空间，但每次优化需要数百次完整算法运行，计算成本极高。

**基于大语言模型的方法**（如EoH, Liu et al., 2024；ReEvo, YE et al., NeurIPS 2024）利用LLM生成启发式算子或进行反思演化，但存在两个关键盲点：其一，它们将LLM直接用作搜索算子而非高层监督者，导致推理缺乏对搜索动态的量化感知；其二，依赖单一LLM的端到端推理，缺乏结构化的控制逻辑分解，使得决策质量受限于模型本身的推理能力。

### 核心瓶颈：缺乏实时感知与结构化推理的融合

上述方法的共同缺陷可归结为：**在超参数调优中，缺乏将实时、量化的搜索状态反馈与可解释的结构化推理相结合的能力**。具体而言：

- 规则方法有结构化逻辑但无状态感知；
- 学习方法有状态感知（通过奖励信号）但缺乏可解释的结构化逻辑，且依赖昂贵训练；
- LLM方法有推理能力但缺乏对搜索动态的量化感知，且推理过程缺乏结构化分解。

### 本文动机与核心洞察

AutoEP的核心洞察是：**将LLM定位为高层监督者而非搜索算子，利用在线探索性景观分析（Exploratory Landscape Analysis, ELA）为LLM提供可量化的搜索状态表征，并通过多LLM推理链（Chain of Reasoning, CoR）将控制任务分解为策略制定、状态诊断和参数执行三个子任务**。这一设计实现了三个关键突破：

1. **零样本、免训练**：LLM的推理能力使AutoEP无需任何离线训练即可适配新的算法-问题组合，从根本上消除了泛化性瓶颈。
2. **数据驱动的推理接地**：ELA特征（偏度、峰度、决定系数、分散比、变化率）将搜索动态转化为可量化的统计指标，为LLM推理提供实证基础，缓解幻觉风险。
3. **结构化控制分解**：CoR将超参数调节分解为Strategist（生成控制映射）、Analyst（诊断探索/利用需求）、Actuator（输出具体参数值）三个角色，使推理链的每一步都有明确的功能边界和可验证性。

> **注意**：关于ELA特征的具体数学定义和CoR各Agent的详细工作机制，请参见“核心方法”章节。

## 核心创新

AutoEP的核心创新在于将大语言模型（LLM）从“搜索算子生成器”重新定位为“高层搜索监督者”，并构建了一个**零样本、免训练的闭环超参数控制系统**。与现有方法相比，这一范式转变体现在三个相互耦合的维度上。

### 1. 从离线训练到零样本在线推理

现有超参数调优方法普遍依赖昂贵的离线训练阶段：基于规则的方法（如**PT**, Joshi & Bansal, 2020）需要专家手工设计调度策略；基于深度强化学习的方法（如**GLEET**, Ma et al., 2024）需要大量元训练来学习调参策略；基于贝叶斯优化的方法（如**BEA**, Lan et al., 2022）则依赖代理模型的在线拟合。这些方法不仅在泛化到新问题或新算法时性能退化严重，而且无法感知搜索过程中的实时动态变化。

AutoEP从根本上绕过了训练需求。其关键洞察是：**LLM的零样本推理能力可以被用来替代训练得到的控制策略**，前提是LLM的推理能够被可量化的搜索状态信息所锚定。具体而言，AutoEP将超参数控制建模为一个“感知-推理-动作”的闭环过程（Figure 2），在每个决策点，系统提取在线ELA特征作为状态表征，交由LLM推理链生成超参数调整指令，整个过程无需任何预训练或微调。

### 2. 搜索状态表征：从简单指标到在线ELA特征

传统超参数调优方法对搜索状态的感知极为粗糙——通常仅依赖迭代次数或当前最优解等简单指标，无法刻画种群分布、景观结构和搜索进度等关键动态。深度强化学习方法虽然能隐式学习状态表征，但学到的表征高度耦合于训练环境，缺乏可解释性和可迁移性。

AutoEP引入的**在线ELA特征提取模块**从根本上改变了这一局面。该模块在每个决策点实时计算五个特征，从四个互补维度刻画搜索状态：

- **适应度分布**：通过偏度（Skewness, $S$）和峰度（Kurtosis, $K$）衡量当前种群解分布的形态。偏度指示解分布的不对称性——正偏度意味着少数优异解与多数较差解并存，暗示存在可进一步开发的优质区域；峰度量化分布的尾部厚度——高峰度表明解集中在少数区域，种群多样性可能不足。

- **景观结构**：通过决定系数（$R^2$）评估适应度景观的可预测性。$R^2$通过二次模型拟合解的分布来计算，高$R^2$表明景观呈漏斗状，存在清晰的梯度方向，适合开发；低$R^2$则表明景观崎岖多模，需要更多探索。

- **种群多样性**：通过分散比（$D_{ratio}$）比较最优解集与最差解集的空间离散程度。$D_{ratio} = \frac{D(Q_{best})}{D(Q_{worst})}$，低比值表明最优解已高度聚集，种群面临早熟收敛风险。

- **搜索进度**：通过变异率（$V$）衡量近期种群平均适应度的相对变化。$V = \frac{\frac{1}{m}\sum_{m=g-m}^{g-1} \bar{y}_m}{\bar{y}_g}$，当$V$趋近于1时，表明搜索已陷入停滞，需要注入新的探索动力。

这五个特征共同构成了一个紧凑而信息丰富的搜索状态快照，为LLM的推理提供了可量化的“传感器读数”。消融实验（Table 2）有力地证明了这一模块的关键性：移除ELA后，AutoEP在TSP dsj1000上的Opt.gap从3.58%恶化至6.46%，尽管仍优于未调优基线（7.14%），但性能损失显著。

### 3. 决策逻辑：从单一LLM到多智能体推理链（CoR）

现有的LLM增强优化方法（如**EoH**, Liu et al., 2024; **ReEvo**, YE et al., NeurIPS 2024）通常将LLM作为单体推理器，直接生成搜索算子或超参数。这种设计存在两个根本性问题：一是单一LLM需要同时理解问题结构、诊断搜索状态并生成精确的超参数值，认知负荷过重；二是缺乏结构化推理过程，容易产生幻觉或不一致的决策。

AutoEP的**多LLM推理链（Chain of Reasoning, CoR）**将控制任务分解为三个专门化的智能体（Figure 3）：

- **Strategist LLM**：在搜索开始时一次性运行，接收问题描述和目标元启发式算法信息，生成一个静态的“控制映射”。该映射定义了每个超参数的定性作用——明确哪些参数主导探索（如变异率），哪些参数主导开发（如交叉率），以及各参数与搜索阶段的关系。这一映射为后续的动态决策提供了语义基础，确保所有调整指令在统一的战略框架内。

- **Analyst LLM**：在每个决策点运行，接收实时ELA特征和经验池中的历史状态-动作-奖励记录，诊断当前搜索状态。其核心任务是回答一个根本性问题：**当前应该优先探索还是开发？** 输出是一个定性的战略指令（如“增加探索力度以跳出局部最优”或“加强开发以精细化当前区域”），而非具体的参数值。

- **Actuator LLM**：接收Analyst的战略指令，将其转化为具体的超参数配置。该过程分为两个子阶段：首先选择需要调整的参数（基于Strategist的控制映射），然后确定每个参数的调整方向和幅度。这种“定性指令→定量配置”的两阶段设计有效降低了LLM在数值推理上的幻觉风险。

CoR的设计带来了三重优势：

1. **任务分解降低认知负荷**：每个Agent只需专注于一个子任务，推理质量显著提升。消融实验（Table 2）表明，移除CoR、使用单一LLM直接生成超参数时，性能下降至接近未调优基线水平（TSP dsj1000 Opt.gap 7.11% vs 基线7.14%），而同时移除ELA和CoR时，性能甚至劣于基线（7.72% vs 7.14%），说明盲目的单步调整可能产生负面影响。

2. **模型效率与性能解耦**：CoR使得较小的开源模型也能达到甚至超越大模型的表现。Table 3显示，使用Qwen3-30B的AutoEP+CoR在eil51上达到0.00% Opt.gap，推理时间仅5.8分钟；而使用GPT-o1的无CoR变体虽然也达到0.00% Opt.gap，但推理时间高达44.7分钟——性能相当但效率相差近一个数量级。

3. **对底层LLM的鲁棒性**：Figure 4表明，当使用较小或较弱的基础模型时，EoH和ReEvo的性能显著下降，而AutoEP仍能保持高性能。这是因为CoR的结构化推理框架降低了对LLM原始推理能力的依赖——框架本身提供了推理的结构和约束，LLM只需在限定范围内进行推理。

### 创新总结

AutoEP的三个创新维度——零样本在线推理、ELA驱动的状态感知、CoR结构化决策——形成了紧密的因果耦合：**ELA提供可量化的状态输入，使LLM推理能够被实证证据锚定；CoR将复杂的控制任务分解为可管理的子任务，使较小的LLM也能胜任；两者的结合使得免训练的零样本超参数控制成为可能。** 这种设计从根本上改变了超参数调优的范式：不再需要为每个新算法或新问题训练专用的调参策略，而是通过一个通用的、可解释的闭环框架，实现对任意元启发式算法的即插即用增强。

## 整体框架

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_hit3hGBheP/figures/002_Figure_2.jpg]]
*Figure 2: The AutoEP Framework*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_hit3hGBheP/figures/003_Figure_3.jpg]]
*Figure 3: Demonstration of CoR*

AutoEP 是一个闭环控制系统，将大语言模型（LLM）定位为高层监督者，通过在线探索性景观分析（ELA）提供可量化的搜索状态反馈，实现对元启发式算法超参数的零样本、免训练动态调优。整个框架由三个核心组件构成：**在线 ELA 特征提取模块**、**经验池（Experience Pool）**和**多 LLM 推理链（Chain-of-Reasoning, CoR）**。

### 闭环控制流程

AutoEP 以“感知—推理—行动”的闭环模式运行：

1. **状态感知（State-Sensing）**：在每个决策点，在线 ELA 模块从当前种群中提取五维特征向量，量化搜索的分布特性、景观结构、多样性和搜索进展。
2. **推理（Reasoning）**：CoR 推理链中的 Analyst LLM 综合实时 ELA 特征与经验池中的历史状态-动作-奖励记录，诊断当前搜索阶段（探索 vs. 利用），并输出战略指令。
3. **行动（Action）**：Actuator LLM 将战略指令转化为具体的超参数配置，直接注入底层元启发式算法，影响下一阶段的搜索行为。执行后的新状态和奖励被回写至经验池，形成持续学习回路。

框架的整体架构如 Figure 2 所示。

### 模块关系与数据流

各模块间的输入输出关系可概括为以下链路：

```
元启发式种群 → ELA模块 → 状态向量 → Analyst LLM
                                          ↑
                                    经验池（历史记录）
                                          ↓
                                  战略指令 → Actuator LLM → 超参数配置 → 元启发式算法
```

- **ELA 模块**接收种群中所有解的适应度值和决策变量，输出 Skewness、Kurtosis、R²、Dispersion Ratio 和 Variability 五个特征值，作为搜索状态的定量快照。
- **经验池**采用滑动窗口机制（默认窗口长度 L=20），仅保留最近 L 次迭代的状态-动作-奖励三元组，避免提示膨胀和噪声干扰。
- **CoR 推理链**由三个分工明确的 LLM Agent 组成：
  - **Strategist LLM**：在每次运行开始时一次性生成静态的“控制映射”，定义各超参数的定性作用（如“交叉率控制探索强度”），为后续推理提供语义锚点。
  - **Analyst LLM**：在每个决策点综合 ELA 特征和经验池历史，诊断当前搜索状态，输出“优先探索”或“优先利用”的战略指令。
  - **Actuator LLM**：接收战略指令，分两个子阶段完成参数选择（确定调整哪些超参数）和幅度确定（给出具体数值），最终输出可直接执行的超参数配置。

### 关键设计决策

- **LLM 作为监督者而非搜索算子**：与 EoH、ReEvo 等将 LLM 直接用于生成搜索算子不同，AutoEP 将 LLM 定位为元层面的控制者，利用其零样本推理能力解读搜索动态，而非替代底层算法的搜索机制。
- **ELA 特征作为 grounding 机制**：五维 ELA 特征为 LLM 推理提供了可量化的实证基础，有效缓解幻觉问题。消融实验表明，移除 ELA 模块后性能显著下降，但仍在未调优基线之上，说明 LLM 仅凭经验池仍保留部分推理能力；同时移除 ELA 和 CoR 则性能低于基线，证实盲目调整会产生负面影响（Table 2）。
- **CoR 推理链的效率优势**：将控制任务分解为 Strategist-Analyst-Actuator 三个子任务，使得较小的开源模型（如 Qwen3-30B）在配合 CoR 时即可达到与 GPT-o1 等超大模型相当的性能，而推理时间减少一个数量级（eil51 上 5.8 min vs. 44.7+ min，Table 3）。

## 核心模块与公式推导

AutoEP 的核心架构由三个功能模块构成闭环控制系统：**在线 ELA 特征提取模块**负责将搜索动态量化为可计算的状态向量；**经验池**存储历史状态-动作-奖励三元组，为 LLM 提供决策上下文；**多智能体推理链（CoR）** 将高层控制任务分解为 Strategist、Analyst、Actuator 三个 LLM 角色的协同推理。

### 在线 ELA 特征提取

ELA 模块在每个决策点从当前种群中提取五维特征，覆盖四个关键维度：适应度分布、景观结构、解多样性和搜索进度。

**适应度分布特征**（Fitness Distribution）刻画当前种群解质量的统计形态：

- **偏度（Skewness, S）**：衡量解分布的对称性。正偏度表明种群中少数解显著优于均值，暗示存在可进一步开发的优质区域；负偏度则表明多数解集中在较优水平，可能需要更多探索。

$$S = \frac { \frac { 1 } { n } \sum _ { i = 1 } ^ { n } \left( y _ { i } - \bar { y } \right) ^ { 3 } } { \left( \sqrt { \frac { 1 } { n } \sum _ { i = 1 } ^ { n } \left( y _ { i } - \bar { y } \right) ^ { 2 } } \right) ^ { 3 } }$$

其中 $y_i$ 为第 $i$ 个个体的适应度值，$\bar{y}$ 为种群适应度均值，$n$ 为种群规模。

- **峰度（Kurtosis, K）**：量化分布的尾部厚度。高峰度意味着解集中在均值附近（收敛风险高），低峰度意味着分布更分散（多样性较好）。公式中减去 3 使得正态分布的峰度为零。

$$K = \frac { \frac { 1 } { n } \sum _ { i = 1 } ^ { n } \left( y _ { i } - \bar { y } \right) ^ { 4 } } { \left( \sqrt { \frac { 1 } { n } \sum _ { i = 1 } ^ { n } \left( y _ { i } - \bar { y } \right) ^ { 2 } } \right) ^ { 4 } } - 3$$

**景观结构特征**（Landscape Structure）评估搜索空间的可预测性：

- **决定系数（R²）**：用二次模型拟合当前种群解在搜索空间中的分布，衡量景观的“漏斗状”程度。高 R² 表明景观结构简单、可预测（适合开发），低 R² 表明景观崎岖多模（需要探索）。

$$R ^ { 2 } = 1 - \frac { \sum _ { i = 1 } ^ { n } ( y _ { i } - f ( \vec { x } _ { i } ) ) ^ { 2 } } { \sum _ { i = 1 } ^ { n } ( y _ { i } - \bar { y } ) ^ { 2 } }$$

其中 $f(\vec{x}_i)$ 为二次模型在解 $\vec{x}_i$ 处的预测值。

**多样性特征**（Diversity）监测种群的空间收敛状态：

- **分散比（$D_{ratio}$）**：比较最优解子集与最差解子集在搜索空间中的离散程度。低比值表明最优解已高度聚集于单一区域，种群多样性不足，需要增强探索。

$$D _ { r a t i o } = \frac { D ( Q _ { \mathrm { b e s t } } ) } { D ( Q _ { \mathrm { w o r s t } } ) }$$

其中 $D(Q_{best})$ 和 $D(Q_{worst})$ 分别为最优解集和最差解集的空间离散度。

**搜索进度特征**（Search Progress）检测搜索停滞：

- **变化率（Variability, V）**：衡量近期 $m$ 代种群平均适应度相对于当前代的比值。当 $V$ 接近 1 时，表明搜索已停滞多代，需要改变策略。

$$V = \frac { \frac { 1 } { m } \sum _ { m = g - m } ^ { g - 1 } \bar { y } _ { m } } { \bar { y } _ { g } }$$

其中 $\bar{y}_g$ 为第 $g$ 代种群的平均适应度。

### 经验池

经验池以滑动窗口（默认长度 $L=20$）存储最近的状态-动作-奖励三元组。消融实验（Table 4）表明 $L=20$ 是性能与效率的最佳平衡点：过小的窗口（$L=5$）缺乏足够历史上下文，性能退化（Opt.gap 从 0.01% 升至 0.04%）；全历史记录则引入噪声和幻觉风险，性能显著下降（Opt.gap 升至 0.17%），同时推理延迟增加。

### CoR 多智能体推理链

CoR 将超参数控制分解为三个 LLM 角色的串行推理：

1. **Strategist**：在优化运行开始时一次性生成静态“控制映射”，定义每个超参数的定性作用（偏向探索或开发），为后续动态决策提供高层语义锚点。
2. **Analyst**：在每个决策点接收实时 ELA 特征和经验池历史，诊断当前搜索状态，输出探索/利用的战略指令（如“当前种群多样性不足，应增强探索”）。
3. **Actuator**：将战略指令转化为具体超参数配置，分两个子阶段执行——先选择需要调整的参数，再确定调整幅度。

消融实验（Table 2）证实了该分解的必要性：移除 CoR 而使用单一 LLM 直接决策，性能退化为与未调优基线相当的水平（TSP dsj1000 Opt.gap 7.11% vs 基线 7.14%），表明结构化推理链对于将搜索状态有效转化为超参数调节策略至关重要。

## 实验与分析

### 核心瓶颈验证：从静态调参到动态感知

现有超参数调优方法面临双重困境：基于规则的方法（如 **PT**，Joshi & Bansal, 2020）依赖手工设计的固定调度，无法适应搜索过程中的状态变化；基于深度强化学习的方法（如 **GLEET**，Ma et al., 2024）虽能学习动态策略，却需要昂贵的离线训练且泛化性差——换一个算法或问题实例往往需要重新训练。AutoEP 的核心突破在于将 LLM 定位为**零样本高层监督者**而非搜索算子，利用在线探索性景观分析（ELA）为 LLM 提供可量化的搜索状态反馈，从而绕过训练瓶颈，实现跨算法、跨问题的通用动态超参数适配。

### 主实验结果：跨基准一致超越

**TSP 基准（Table 1）。** 在 6 个 TSP 实例上，GA-2opt+AutoEP 取得了接近最优的性能：eil51 上 Opt.gap 为 0.00%，dsj1000 上为 3.58%，分别比未调优的 GA-2opt 基线（0.17% 和 7.14%）降低了 0.17 和 3.56 个百分点。更关键的是，AutoEP 增强后的 GA-2opt 不仅超越了所有传统超参数调优方法（PT、GLEET、BEA），还超越了基于 LLM 的算子生成方法 **EoH**（Liu et al., 2024）和反射演化方法 **ReEvo**（YE et al., NeurIPS 2024），以及神经组合优化方法 **LEHD**（Luo et al., 2023）和 **DACT**（Ma et al., 2021）。值得注意的是，AutoEP 作为即插即用模块，可以叠加在 EoH 和 ReEvo 之上进一步提效，例如 GA-2opt+ReEvo+AutoEP 在 dsj1000 上的 Opt.gap 从 ReEvo 单独使用的 3.62% 进一步降至 3.59%。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_hit3hGBheP/figures/004_Table_1.jpg]]
*Table 1: Comparison with various baselines on TSP. Opt.gap represents the percentage gap between the average run result and the optimal solution for this dataset; a smaller value is better. Time is the average runtime (unit: minute)*

**CVRP 基准（Table 5）。** 在容量约束车辆路径问题上，GA-2opt+AutoEP 在 N=200 规模上取得 1.08% 的 Opt.gap，相比基线 GA-2opt 的 5.89% 降低了 4.81 个百分点。随着问题规模增大至 N=500，AutoEP 的优势依然显著（3.17% vs 6.12%），证明 ELA 特征和 CoR 推理链在大规模搜索空间中仍能有效感知搜索状态。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_hit3hGBheP/figures/014_Table_5.jpg]]
*Table 5: Comparison with various baselines on CVRP. Opt.gap represents the percentage gap between the average run result and the optimal solution; a smaller value is better. Time is the average runtime (unit: minute)*

**FSSP 基准（Table 6）。** 在流水车间调度问题上，GA-2opt+AutoEP 在所有 5 个问题规模上均取得最优 Opt.gap（n20m10 上 2.09% 至 N500m20 上 2.83%），超越了包括 **NEH**（Nawaz et al., 1983）、**NEHFF**（Fernandez-Viagas & Framinan, 2014）等构造启发式以及 **PFSPNet_NEH**（Pan et al., 2021）等深度强化学习方法。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_hit3hGBheP/figures/015_Table_6.jpg]]
*Table 6: Comparison with various baselines on FSSP. Opt.gap represents the percentage gap between the average run result and the optimal solution; a smaller value is better. Time is the average runtime (unit: minute)*

**UAV 轨迹优化（Table 7）。** 在无人机数据采集轨迹优化任务上，ACO+AutoEP 在 N=300 规模上取得 1574.90 的轨迹长度，相比基线 ACO 的 1912.74 缩短了 337.84 个单位（约 17.7%），且在所有 5 个问题规模上均保持最优，验证了 AutoEP 在非经典组合优化场景中的迁移能力。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_hit3hGBheP/figures/016_Table_7.jpg]]
*Table 7: Comparison of UAV Trajectory Optimization Experiments. Traj.Length is the length of the drone’s flight trajectory, where a lower value indicates a better performance. Time is the average runtime (unit: minute)*

### 消融研究：ELA 与 CoR 的因果贡献

**Table 2** 的组件消融实验揭示了两个核心模块的独立贡献与协同效应：

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_hit3hGBheP/figures/005_Table_2.jpg]]
*Table 2: Component ablation study of AutoEP on TSP*

- **移除 ELA 模块**：GA-2opt+AutoEP (Without ELA) 在 dsj1000 上 Opt.gap 从 3.58% 升至 6.46%，性能显著退化，但仍优于未调优基线（7.14%）。这表明 LLM 仅凭经验池中的历史状态-动作-奖励信息仍能进行一定程度的推理，但缺乏实时景观特征导致决策质量大幅下降。

- **移除 CoR 推理链**：使用单一 LLM 替代多智能体协同后（Without CoR），dsj1000 上 Opt.gap 升至 7.11%，几乎退化至基线水平（7.14%）。这证明将控制任务分解为 Strategist-Analyst-Actuator 的结构化推理链是性能的关键来源，单一 LLM 难以同时处理战略规划、状态诊断和参数量化的复杂推理。

- **同时移除 ELA 和 CoR**：性能反而劣于未调优基线（dsj1000 上 7.61% vs 7.14%），说明在缺乏状态感知和结构化推理的情况下，盲目调整超参数会产生负面影响——LLM 的幻觉在此场景下直接转化为有害的控制决策。

### CoR 架构的效率优势

**Table 3** 展示了 CoR 架构的关键效率优势：AutoEP with CoR (Qwen3-30B) 在 eil51 上取得 0.00% Opt.gap，推理时间仅 5.8 分钟；而 AutoEP without CoR (GPT-o1) 虽然同样取得 0.00% Opt.gap，推理时间却高达 44.7 分钟。CoR 通过将复杂推理任务分解为三个专注的子任务，使得较小的开源模型（30B 参数）能够在性能上匹敌超大闭源模型，同时推理时间减少一个数量级。这一发现具有重要的实践意义：AutoEP 可以在消费级 GPU 上部署，无需依赖昂贵的 API 调用。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_hit3hGBheP/figures/006_Table_3.jpg]]
*Table 3: Comparison of CoR components with other reasoning LLMs*

### 经验池设计的参数敏感性

**Table 4** 分析了经验池滑动窗口大小 L 的影响。默认设置 L=20 在 TSP-100 上取得最优 Opt.gap（0.01%）和合理的推理延迟（0.31 秒/决策）。过小的窗口（L=5）导致历史信息不足，Opt.gap 升至 0.04%；而过大的窗口（L=50）或保留全历史记录（Full History）则引入噪声和上下文过载，全历史条件下 Opt.gap 退化至 0.17%，与未调优基线相当。这一结果揭示了 LLM 上下文管理的微妙平衡：过多历史信息不仅增加推理成本，还可能引发注意力分散和幻觉，反而损害决策质量。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_hit3hGBheP/figures/012_Table_4.jpg]]
*Table 4: Impact of experience pool size (L) on performance and inference latency (TSP-100)*

### 对底层 LLM 能力的鲁棒性

**Figure 4** 展示了 AutoEP 与 EoH、ReEvo 在不同 LLM 上的性能对比。EoH 和 ReEvo 的性能随模型能力下降而显著退化——这是因为它们直接依赖 LLM 生成搜索算子或启发式规则，模型能力不足直接导致生成质量下降。相比之下，AutoEP 即使使用较小的模型仍能保持高性能，因为其 LLM 的角色是分析 ELA 提供的量化状态并做出高层战略决策，而非直接生成搜索算子。这种架构设计将 LLM 从“搜索算子”降级为“状态解释器”，降低了对模型生成能力的依赖，增强了框架的鲁棒性。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_hit3hGBheP/figures/010_Figure_4.jpg]]
*Figure 4: Comparison of Experimental Results Across Different LLMs. The baseline algorithm for adjustment is GA-2opt*

### 调整频率的敏感性

**Figure 5** 在 UAV-300 任务上分析了超参数调整频率的影响。结果表明，即使每 3-5 次迭代调整一次（而非每代调整），AutoEP 仍能提供显著的性能提升。这一特性降低了计算开销，使得 AutoEP 在推理资源受限的场景中仍具实用性。但调整频率过低（如每 10 代以上）会导致搜索状态感知滞后，性能增益逐渐消失。

### 超参数演化可视化

**Figure 6** 可视化了 GA 在 TSP-400 上的超参数演化轨迹。可以观察到，AutoEP 控制的交叉率和变异率呈现出明显的阶段性特征：搜索初期偏向高探索（高变异率），中期逐步过渡到开发（降低变异率、提高交叉率），后期在收敛停滞时再次提升探索力度。这种非单调的动态调整模式是静态规则或预训练策略难以复现的，体现了 AutoEP 基于实时 ELA 反馈进行情境化决策的核心优势。

### 失败模式与局限性

尽管 AutoEP 在组合优化基准上表现优异，仍存在以下值得关注的局限：

1. **推理开销的累积效应**：虽然单次推理延迟仅约 30ms，但整个优化过程中数百次调整累计增加 2-5 分钟的总运行时间。对于极度时间敏感的任务（如实时在线决策），这一开销可能成为瓶颈。

2. **连续优化问题的迁移未验证**：当前实验集中于离散组合优化（TSP、CVRP、FSSP、UAV 轨迹），ELA 特征选择和 CoR 提示设计是否适用于连续优化问题仍需验证。

3. **ELA 特征的专家依赖性**：当前 5 个 ELA 特征（偏度、峰度、R²、分散比、变化率）依赖领域专家选择。对于新型黑箱算法，这些特征是否仍能有效表征搜索状态尚未探讨。

4. **级联失败风险未分析**：CoR 框架依赖 Strategist→Analyst→Actuator 的顺序推理链，如果前序 Agent 产生错误输出，可能导致后续决策的级联失败。文中未对这种失败模式进行深入分析或提出容错机制。

### 补充图表

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_hit3hGBheP/figures/026_Table_8.jpg]]
*Table 8: Parameterization of each meta - heuristic algorithm*

## 方法谱系与知识库定位

### 1. 在超参数调优谱系中的位置

AutoEP 处于一个明确的方法演进节点：从**手工规则**到**学习型调优**，再到**基于LLM的零样本闭环控制**。

**传统规则式调优**（如 **PT**, Joshi & Bansal, 2020）依赖固定的启发式策略（例如随迭代次数线性衰减变异率），缺乏对搜索动态的实时感知，在复杂问题上表现乏力。**贝叶斯优化方法**（如 **BEA**, Lan et al., 2022）通过代理模型搜索超参数空间，但通常需要大量离线评估，且对高维参数空间的扩展性受限。**深度强化学习方法**（如 **GLEET**, Ma et al., 2024）将超参数调优建模为序列决策问题，在特定基准上取得了SOTA性能，但核心瓶颈在于：需要针对每个算法-问题组合进行昂贵的元训练，且训练好的策略难以泛化到未见过的搜索动态。

AutoEP 的因果杠杆在于绕过了训练依赖。它利用LLM的零样本推理能力，将超参数调优从“学习一个策略”转变为“根据实时状态进行推理”。这一转变的关键支撑是在线ELA模块——它将搜索动态量化为可解释的特征向量（偏度、峰度、$R^2$、分散比、变化率），为LLM提供了可操作的“仪表盘”。没有这个量化状态接口，LLM的推理就缺乏经验锚定，这正是消融实验中移除ELA后性能显著退化的原因（Table 2）。

### 2. 与LLM增强优化方法的对比

AutoEP 与两类LLM增强方法存在根本性差异：

**LLM作为搜索算子生成器**（如 **EoH**, Liu et al., 2024）：这类方法让LLM生成新的启发式算子或搜索策略代码，本质上是将LLM用作一次性设计工具。它们缺乏在线适应能力——生成的策略在运行中固定不变。AutoEP 则不同：LLM作为持续的监督者参与整个搜索过程，根据实时状态动态调整参数。

**LLM作为反射式搜索器**（如 **ReEvo**, YE et al., NeurIPS 2024）：ReEvo让LLM直接参与解的生成与反思，LLM承担了部分搜索算子的角色。AutoEP 将LLM定位为更高层的“控制者”而非“搜索者”——它不生成候选解，而是调节底层元启发式算法的行为参数。这种角色分离使得AutoEP可以作为即插即用模块叠加在任何元启发式算法之上，包括已经被EoH或ReEvo增强过的算法（Table 1中GA-2opt+EoH+AutoEP和GA-2opt+ReEvo+AutoEP的结果证实了这一点）。

**对底层模型能力的鲁棒性**是AutoEP区别于其他LLM方法的关键特征。Figure 4显示，当使用较小模型时，EoH和ReEvo的性能显著下降，而AutoEP保持了高性能。这是因为CoR架构将复杂的控制决策分解为三个专门的子任务（Strategist-Analyst-Actuator），每个子任务对推理深度的要求低于“从头生成搜索策略”这样的整体任务，因此较小的模型也能胜任。

### 3. 适用边界与局限

**已验证的适用范围**：AutoEP在以下组合优化问题上展示了有效性：
- TSP（51-1000个城市）
- CVRP（20-500个客户）
- FSSP（20-500个作业）
- UAV轨迹优化（20-300个数据采集点）

在这些问题上，AutoEP一致地提升了GA、PSO、ACO及其2-opt变体的性能。

**已知局限**：

1. **计算开销**：虽然单次推理延迟极低（30ms），但整个运行中AutoEP引入的总开销约为2-5分钟（取决于问题规模）。对于极度时间敏感的应用场景，这一开销可能需要权衡。

2. **问题类型限制**：当前验证集中于组合优化问题。是否可平滑迁移至连续优化问题（如函数优化、神经网络超参数调优）尚未验证。连续空间的ELA特征选择和CoR提示设计可能需要实质性调整。

3. **ELA特征的专家依赖**：当前选择的5个ELA特征（偏度、峰度、$R^2$、分散比、变化率）依赖于专家对搜索动态的先验理解。对于新型黑箱算法或非常规搜索空间，这些特征是否仍然足够描述搜索状态，文中未进行探讨。

4. **级联失败风险**：CoR框架依赖三个Agent输出的正确性。如果Analyst产生错误的搜索状态诊断，Actuator将基于错误指令生成超参数配置，可能导致搜索退化。文中未深入分析这种级联失败的频率和影响程度。

### 4. 开放问题

1. **多目标与约束优化扩展**：AutoEP的ELA特征和CoR提示设计均针对单目标无约束优化。扩展到多目标优化需要定义新的状态表征（如Pareto前沿的分布特征）和探索/利用的判定逻辑。带约束优化还需要将约束违反信息纳入状态反馈。

2. **ELA特征的自动化选择**：当前特征集依赖专家先验。是否可以通过学习型方法（如使用LLM自身或元学习）自动选择或生成适合特定算法-问题组合的ELA特征，以减少人工设计负担？

3. **极大规模问题的实用性**：在10万+城市的TSP或类似规模的问题上，ELA特征的计算开销（特别是$R^2$的二次模型拟合和分散比的空间距离计算）可能成为瓶颈。此外，CoR的推理质量是否会在搜索空间剧增时保持稳定，需要进一步验证。

4. **跨领域迁移**：AutoEP的思路（在线状态感知 + LLM推理链 + 闭环控制）是否可应用于深度神经网络的超参数调优（如学习率调度、正则化强度调节）？这需要重新设计状态表征模块，可能利用训练/验证损失曲线、梯度统计量等作为“ELA”的替代。

## 原文 PDF

![[paperPDFs/ICLR_2026/AutoEP_LLMs_Driven_Automation_of_Hyperparameter_Evolution_for_Metaheuristic_Algorithms.pdf]]
