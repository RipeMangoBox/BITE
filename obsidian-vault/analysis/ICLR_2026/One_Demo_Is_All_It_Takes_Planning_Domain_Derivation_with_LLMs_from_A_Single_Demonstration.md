---
title: "One Demo Is All It Takes: Planning Domain Derivation with LLMs from A Single Demonstration"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/One_Demo_Is_All_It_Takes_Planning_Domain_Derivation_with_LLMs_from_A_Single_Demonstration.pdf
project_link: null
code_link: null
openreview_forum_id: Y1VgLHbzCC
aliases:
- One_Demo_Is_All_
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "PDDLLM 通过将 LLM 的推理能力与物理仿真反馈相结合，从单次演示中自动生成谓词库和动作库，彻底消除了对手动预定义领域知识的需求。"
primary_logic: "利用物理仿真来验证和细化 LLM 生成的逻辑关系，将连续状态离散化并通过多阶段谓词想象生成可执行的规划域，实现了高度自动化和强可解释性的长时序规划。"
claims:
- "PDDLLM 在 1200+ 个任务、9 种环境上超越六大基线，整体规划成功率至少高出 20%。"
- "在 Tower of Hanoi 等复杂长时序任务上，PDDLLM 成功率达 100%，而最强 LLM 基线仅为 14.3%。"
- "PDDLLM 以远低于推理 LLM（o1/R1）的 token 成本，在复杂任务上获得更高成功率（80.5% vs. 61.5%）。"
- "仅从一次演示即可生成完整的可执行规划域，无需任何预定义谓词或动作。"
---

# One Demo Is All It Takes: Planning Domain Derivation with LLMs from A Single Demonstration

> [!tip] 核心洞察
> 利用物理仿真来验证和细化 LLM 生成的逻辑关系，将连续状态离散化并通过多阶段谓词想象生成可执行的规划域，实现了高度自动化和强可解释性的长时序规划。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 一次演示足矣：利用大语言模型从单次演示推导规划域 |
| 英文题名 | One Demo Is All It Takes: Planning Domain Derivation with LLMs from A Single Demonstration |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Y1VgLHbzCC) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | PDDLLM |
| Dataset | Overall (9 tasks), Tower of Hanoi, Rearrangement, Complex tasks (Rearr., ToH, Bridge) |

> [!tip] 效果简介
> - Overall (9 tasks) 上，Success Rate (%) 为 93.3 ± 0.7，对比 52.5 ± 0.4 (LLMTAMP-FF)，变化 +40.8。
> - Tower of Hanoi 上，Success Rate (%) 为 100 ± 0.0，对比 14.3 ± 0.0 (LLMTAMP-FF)，变化 +85.7。
> - Rearrangement 上，Success Rate (%) 为 64.3 ± 0.7，对比 17.4 ± 1.1 (LLMTAMP-FF)，变化 +46.9。

## 概要

### 问题瓶颈

任务与运动规划（TAMP）是实现复杂长时序机器人操作的核心框架，但其有效性高度依赖人工精心设计的PDDL规划域。构建一个完整的规划域需要领域专家手动定义谓词库、动作库以及逻辑动作与运动规划器之间的物理约束接口，这一过程劳动密集、周期漫长，且难以迁移到新场景。现有基于LLM的TAMP方法虽然降低了对显式域定义的需求，但在复杂任务上成功率仍然有限，最强基线LLMTAMP-FF的整体成功率仅为52.5%，而在Tower of Hanoi等需要长程依赖的任务上更是骤降至14.3%。

### 核心思路

PDDLLM提出了一条根本性的替代路径：**仅从单次人类演示出发，自动推导出完整的可执行规划域**，彻底消除对手动预定义领域知识的依赖。其核心洞察在于将LLM的推理能力与物理仿真反馈深度耦合——通过并行仿真采样探索连续状态空间中的可行区域，由LLM将这些物理交互总结为有意义的符号谓词，再通过逻辑状态转换推断动作定义。这一“仿真验证→LLM抽象→逻辑编译”的闭环机制，使得系统能够在没有人工标注的情况下，自主发现任务相关的抽象表示。

### 方法定位

从方法谱系来看，PDDLLM位于**LLM辅助规划与符号规划的交汇点**，但区别于现有工作的关键之处在于：

- **域构建方式**：传统TAMP（如LLMTAMP, Huang et al., 2022a）依赖人工编写或部分预定义的PDDL域；PDDLLM从单次演示中自动生成谓词库和动作库，并通过并行提示与执行反馈机制筛选最优候选域。
- **运动规划接口**：现有方法需为每个逻辑动作手工编写与运动规划器的数学约束接口；PDDLLM通过LoCA（Logical Constraint Adapter）自动从动作效果谓词的物理约束中生成该接口，实现了逻辑层与运动层的无缝衔接。
- **谓词发现机制**：不同于依赖预定义谓词集合的方法，PDDLLM通过两阶段谓词想象——先通过仿真采样与LLM总结生成一阶谓词，再利用逻辑算子（非、全称量词）导出高阶谓词——自动构建完整的谓词库。

与使用推理LLM（o1-TAMP, OpenAI, 2024; R1-TAMP, DeepSeek-AI, 2025）作为规划骨干的方法相比，PDDLLM将LLM的角色从“规划器”转变为“域构建器”：前者在每次新任务中实时推理动作序列，消耗大量token；后者一次性生成可复用的符号域，后续规划由高效的符号求解器完成，在复杂任务上实现更高成功率的同时，token成本降低约38%。

### 主要结果

在9种环境、超过1200个任务的评测中，PDDLLM以**93.3%的整体规划成功率**全面超越六大基线，较最强基线LLMTAMP-FF（52.5%）提升超过40个百分点。在Tower of Hanoi等需要长时序推理的复杂任务上，PDDLLM成功率达到**100%**，而LLMTAMP-FF仅为14.3%。与推理LLM方法相比，PDDLLM在复杂任务子集上以80.5%的成功率优于o1-TAMP的61.5%，且token成本仅为后者的62%。消融实验表明，生成的规划域与专家手工设计域相比，缺失谓词和冗余谓词的比例均控制在较低水平，验证了自动域构建的质量。系统还在Franka、Piper、UR5e三种真实机器人平台上成功部署，进一步证明了方法的实用性。

任务与运动规划（Task and Motion Planning, TAMP）是机器人自主完成复杂长时序操作的核心技术。它需要将高层符号推理与低层连续运动规划相结合，使机器人能够将“把杯子放到架子上”这样的抽象指令，分解为一系列可执行的抓取、移动、放置动作。然而，TAMP 系统的有效性高度依赖于一个关键前提：**规划域（planning domain）必须被精确地预先定义**。

规划域通常以规划域定义语言（Planning Domain Definition Language, PDDL）描述，包含两类核心要素：**谓词库**（predicate library）和**动作库**（action library）。谓词定义了世界中可能存在的逻辑状态（如 `is_on(?o1, ?o2)` 表示物体叠放关系），动作则定义了状态转换的规则（如 `stack` 动作的前提条件和效果）。在现有实践中，这些域知识的构建几乎完全依赖人类专家手工完成——专家需要观察任务场景，抽象出关键物理关系，将其编码为符号谓词，并为每个动作编写与运动规划器之间的数学约束接口。这一过程劳动密集、耗时且极易出错，构成了 TAMP 方法向新场景扩展的**核心瓶颈**。

近年来，大语言模型（LLM）的推理能力为缓解这一问题提供了新思路。以 **LLMTAMP**（Huang et al., 2022a）为代表的方法尝试让 LLM 直接生成规划步骤，但其缺乏对物理世界的真实反馈，生成的计划常常在运动规划阶段失败。后续改进如 **LLMTAMP-FF**（Huang et al., 2022b; Chen et al., 2024a）引入了失败反馈环，**LLMTAMP-FR**（Wang et al., 2024）进一步加入了失败原因推理与重规划机制。然而，这些方法始终在一个根本性局限内运作：**它们仍然依赖人类预先提供的谓词和动作定义**。LLM 只是在已知的符号空间内进行搜索，而非从物理世界中自主构建这个符号空间本身。

更先进的推理型 LLM（如 OpenAI o1、DeepSeek R1）虽然展现出更强的推理链能力，但在复杂长时序任务上仍面临成功率不足和 token 成本过高的问题。**o1-TAMP** 和 **R1-TAMP** 在 Tower of Hanoi 等任务上的成功率分别仅为 14.3% 和 28.6%，而单次规划的 token 消耗可达数千美元级别。

核心矛盾在于：**人类专家无法为每一个新场景预先编写规划域，而 LLM 又缺乏从物理世界自主抽象符号知识的能力**。本文的核心动机正是打破这一僵局——能否让系统仅通过观察一次人类演示，就自动推导出完整的、可执行的规划域？这要求系统同时具备两种能力：从连续物理轨迹中抽象出离散逻辑关系，以及验证这些逻辑关系在真实物理约束下的正确性。

## 核心方法与创新机理

PDDLLM 的核心创新在于将**规划域构建**从“人工编写”彻底转变为“从单次演示自动推导”，消除了 TAMP 对专家手工设计 PDDL 域的依赖。这一转变通过三个关键 slot 的替换实现：

| 关键模块 | 基线方法 | PDDLLM 方法 |
|---------|---------|------------|
| **域构建** | 人工编写 PDDL 域（依赖专家知识，耗时且易错） | 从单次演示自动生成（LLM 推理 + 物理仿真验证） |
| **运动规划接口** | 为每个逻辑动作手工编写与运动规划的数学约束接口 | 通过 LoCA 自动从动作效果谓词的物理约束生成接口 |
| **谓词库** | 预定义或部分预定义的谓词集合 | 通过谓词想象（仿真采样 + LLM 总结）自动生成完整谓词库 |

这三个 slot 构成了 PDDLLM 的因果杠杆：**物理仿真反馈**作为 LLM 推理的验证器，将连续状态离散化后通过多阶段谓词想象生成可执行的规划域，实现了高度自动化和强可解释性的长时序规划。

### 谓词想象：从仿真中归纳逻辑关系

传统方法需要人工预定义谓词集合，而 PDDLLM 通过两阶段谓词想象自动构建谓词库：

- **一阶谓词生成**：在仿真中采样对象位姿并执行物理模拟，滤除不可行配置后，将可行子空间提供给 LLM，由其总结出直接描述物理属性或关系的一阶谓词（如 `(is_on ?o1 ?o2)`）。
- **高阶谓词导出**：通过逻辑算子（非、全称量词）组合一阶谓词，自动导出高阶谓词（如 `(∀_¬ o1_ not_is_on :?o1 ::?o2)` 表示没有任何物体在 ?o2 上面）。

这一机制的本质是**用物理仿真将连续状态离散化**，使 LLM 能够从仿真 roll-out 中提取有意义的逻辑关系，而非凭空猜测。

### 动作发明：从状态转换推断动作定义

PDDLLM 从演示轨迹中提取逻辑状态转换对（当前状态 → 下一状态），将其呈现给 LLM，由 LLM 总结出 PDDL 动作的前置条件与效果。这一过程将动作发明转化为“状态转换模式识别”问题，避免了手工定义动作模式的繁琐。

### LoCA：自动桥接逻辑规划与运动规划

LoCA 是 PDDLLM 消除人工接口设计的核心组件。它直接检索动作效果集 $\mathcal{P}_{eff}$ 中每个一阶谓词关联的物理约束，将逻辑动作自动转换为标准约束运动规划问题。这意味着**动作的语义含义被自动翻译为运动规划的数学约束**，无需为每个动作手工编写接口。

### 并行提示与反馈筛选

为避免单次 LLM 调用可能导致的域生成失败，PDDLLM 采用并行提示策略：对同一演示多次调用 LLM 生成多个候选域，通过执行反馈筛选并多数表决选出最优域。消融实验表明，当并行提示数 $n_{prompt} \geq 15$ 时，域生成失败率降至 0%（Table 15），证明了该策略的有效性。

综上，PDDLLM 的创新并非在单个模块上修修补补，而是**重构了 TAMP 的域构建范式**：从“人工定义 + 手工接口”变为“仿真验证 + LLM 归纳 + 自动接口”，仅需一次演示即可生成完整的可执行规划域。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_Y1VgLHbzCC/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the proposed framework. (1) Human demonstrations, in the form of manipulation trajectories, and the corresponding task descriptions, serve as input. Implementation details is shown in Section B.12. (2) PDDLLM initiates thousands of parallel simulations, using the resulting roll-outs and rich physics-based feedback to guide the LLM in summarizing them into meaningful predicates, and returns a predicate library annotated with each predicate’s relevance to the current task. (3) Actions are invented by an LLM that summarizes logical state transition patterns from the demonstration, which is grounded into logical states using the imagined predicates. (4) The predicates and actions ar...*

PDDLLM 的核心管线由四个串行模块构成，输入为单次人类演示的操作轨迹与对应的任务描述，输出为可直接送入运动规划器执行的可执行规划域。

### 输入与输出定义

框架的形式化目标如公式 (1) 所示：

$$
\tilde{a}^{(0)}, \tilde{a}^{(1)}, \dots, \tilde{a}^{(L-1)} = MotionPlanner(PDDLLM(S_{new}^{(init)}, S_{new}^{(goal)}, T_{demo}, \tau_{demo}))
$$

给定新场景的初始状态 $S_{new}^{(init)}$ 与目标状态 $S_{new}^{(goal)}$，以及演示的任务描述 $T_{demo}$ 和操作轨迹 $\tau_{demo}$，PDDLLM 自动推导出一个 PDDL 规划域，再由运动规划器将其转化为可执行的机器人轨迹序列。

### 管线模块

1. **谓词想象 (Predicate Imagination)**：从物理仿真中采样大量对象交互状态，利用仿真反馈过滤不可行配置，将可行子空间提供给 LLM 进行总结。该过程分两阶段——首先生成一阶谓词（直接描述物理属性或空间关系，如 `(is_on ?o1 ?o2)`），再通过逻辑算子（非、全称量词）组合一阶谓词导出高阶谓词（如 `(∀_¬o1_ not_is_on ?o1 ?o2)`，表示 ?o2 上方无任何物体）。最终输出一个标注了任务相关性的谓词库。

2. **动作发明 (Action Invention)**：将演示轨迹中的连续状态通过已生成的谓词库接地为逻辑状态，提取状态转换对（当前逻辑状态 → 下一逻辑状态），由 LLM 归纳出 PDDL 动作的定义（前提条件与效果集）。

3. **并行提示与反馈筛选 (Parallel Prompting with Feedback)**：为避免单次生成失败，系统并行生成多个候选域，通过执行反馈进行验证，最终以多数表决选出最优域。

4. **逻辑约束适配器 (LoCA)**：自动将每个逻辑动作效果集中的一阶谓词所关联的物理约束检索出来，转化为标准约束运动规划问题，从而将任务规划与运动规划无缝桥接，无需人工编写接口。

### 关键设计决策

- **仿真反馈闭环**：谓词想象依赖数千次并行仿真来验证物理可行性，LLM 仅对仿真筛选后的可行子空间进行语义总结，而非凭空生成。
- **离散化尺度 $u_f$**：连续特征 $f$ 的离散化粒度初始设为该特征在所有相关物体间的最小非零差异 $d_{min}$，平衡了谓词精度与冗余度。
- **一次性域推导**：整个流程仅需单次演示，不依赖任何预定义谓词或动作模板，也不需要在执行新任务时重复调用 LLM——token 消耗仅发生在域推导阶段，后续规划由 PDDL 求解器零成本完成。

### 问题形式化

PDDLLM 框架的总问题表述为：给定新场景的初始状态 $S_{new}^{(init)}$ 和目标状态 $S_{new}^{(goal)}$，以及一次演示的任务描述 $T_{demo}$ 和轨迹 $\tau_{demo}$，系统自动推导出可执行的机器人轨迹：

$$
\tilde{a}^{(0)}, \tilde{a}^{(1)}, \dots, \tilde{a}^{(L-1)} = MotionPlanner(PDDLLM(S_{new}^{(init)}, S_{new}^{(goal)}, T_{demo}, \tau_{demo}))
$$

其中 $PDDLLM(\cdot)$ 输出符号任务规划，$MotionPlanner(\cdot)$ 将其转化为物理可执行的动作序列。该公式锚定于 Section 4 的问题陈述。

### 核心模块

PDDLLM 的自动化域推导由四个关键模块串联而成，加上一个连接运动规划器的接口组件：

**模块一：谓词想象（Predicate Imagination）**

该模块从模拟的物理交互中自动生成谓词库，分两阶段执行：

- **第一阶段（一阶谓词生成）**：对连续状态空间按离散化尺度 $u_f$ 进行分区采样，通过物理仿真过滤不可行配置，将可行子空间提交给 LLM 总结为一阶谓词。一阶谓词直接描述物体的物理属性或关系，例如 $( \mathrm{is\_on} \; ?o_1 \; ?o_2 )$ 表示物体 $o_1$ 叠在 $o_2$ 上。离散化尺度 $u_f$ 的初始值设为该特征在所有相关物体间的最小非零差异 $d_{min}$。
- **第二阶段（高阶谓词推导）**：通过逻辑算子（非、全称量词）组合一阶谓词，导出高阶谓词。例如 $( \forall_{\neg} o_{1\_} \mathrm{not\_is\_on} \; ?o_1 \; ?o_2 )$ 表示没有任何物体在 $?o_2$ 上面。谓词想象的总复杂度定义为 $\mathrm{complexity} = \sum_i n_{p,i}^{n_{\dim,i}}$，即每类谓词在各维度上分区数乘方的求和。

**模块二：动作发明（Action Invention）**

从演示轨迹的逻辑状态转换中推断 PDDL 动作定义。具体而言，利用已生成的谓词将演示的连续状态离散化为逻辑状态序列 $\bar{\tau}_{demo}^{logic}$，提取状态转换前后的逻辑状态对，提交给 LLM 生成动作的 PDDL 定义（包括前提条件和效果）。

**模块三：并行提示与反馈筛选（Parallel Prompting with Feedback）**

为规避单次生成可能导致的域失败，系统并行生成多个候选 PDDL 域，通过执行反馈筛选并采用多数表决机制选出最优域。实验表明，当并行提示数 $n_{prompt} \geq 15$ 时，域生成失败率降至 0%。

**模块四：逻辑约束适配器（LoCA）**

LoCA 自动将逻辑动作与运动规划器对接，无需人工编写数学约束接口。其核心机制是：检索动作效果集 $\mathcal{P}_{eff}$ 中每个一阶谓词关联的物理约束，将逻辑动作自动转化为标准约束运动规划问题，确保生成轨迹与动作语义一致。

## 实验与关键发现

### 核心瓶颈与因果机制验证

实验设计的核心验证目标围绕一个关键瓶颈展开：**传统TAMP系统对人工精心设计PDDL域的强依赖**。PDDLLM通过将LLM的推理能力与物理仿真反馈相结合，从单次演示中自动生成谓词库和动作库，彻底消除对手动预定义领域知识的需求。这一因果机制的验证贯穿所有实验维度。

#### 主结果：规划成功率与泛化能力

**Table 1** 汇总了9项操作任务、1200+个规划问题上的成功率对比（统一50秒时限）。PDDLLM以 **93.3% ± 0.7%** 的总体成功率全面领先，较最强LLM基线LLMTAMP-FF（52.5% ± 0.4%）提升超过40个百分点。在需要长时序推理的复杂任务上优势更为突出：

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_Y1VgLHbzCC/figures/003_Table_1.jpg]]
*Table 1: Planning success rate (%) across tasks for all methods (time limit = 50 s). The best results are highlighted in bold. Expert is excluded from the comparison, as it requires additional manual effort and serves as an upper bound*

- **Tower of Hanoi**：PDDLLM达到100%成功率，而LLMTAMP-FF仅为14.3%（+85.7%），验证了自动生成的逻辑域能够支撑深层递归规划。
- **Rearrangement**：PDDLLM为64.3%，LLMTAMP-FF仅17.4%（+46.9%），说明系统在空间关系复杂的重排任务中仍能有效运作。
- **Color Classification、Alignment、Parts Assembly**：PDDLLM均达到100%成功率，表明生成的谓词能准确捕获颜色、对齐、装配等物理约束。

LLMTAMP基础版本（无反馈）的总体成功率仅35.7%，凸显了仿真反馈在域验证中的决定性作用。RuleAsMem（将生成的域作为LLM上下文记忆而不使用符号求解器）的表现介于LLMTAMP-FF与PDDLLM之间，说明符号求解器对规划可靠性有额外贡献但非唯一因素。

**Figure 3** 从两个维度进一步验证泛化性：左图显示PDDLLM在物体数量增至20个时仍保持较高成功率，性能衰减远慢于基线；右图表明PDDLLM在不同时间限制下均饱和最快，50秒即接近性能上限，而基线方法需更长时间才趋于稳定。

#### 与推理LLM的效率对比

**Table 2** 将PDDLLM与使用推理LLM骨干（OpenAI o1、DeepSeek R1）的TAMP方法在三个最复杂任务（Rearrangement、Tower of Hanoi、Bridge Building）上对比。PDDLLM以 **80.5%** 的总体成功率超越o1-TAMP（61.5%）和R1-TAMP（35.9%），同时Token消耗仅为415k，远低于o1-TAMP（666k）和R1-TAMP（725k）。这验证了PDDLLM的核心设计优势：Token仅在域推导阶段一次性消耗，后续规划由符号求解器零Token执行，而推理LLM方法需在每个规划步骤反复调用大模型。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_Y1VgLHbzCC/figures/006_Table_2.jpg]]
*Table 2: Comparison of planning success rate (%) and token cost (k) between PDDLLM and LLMTAMP and the reasoning LLM variants. The best results are shown in bold, and the second-best results are underlined*

**Table 6** 的时间成本对比进一步佐证：PDDLLM在各项任务上的平均规划时间显著低于o1-TAMP变体，域推导的固定开销在复杂任务中被高效的符号求解充分摊薄。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_Y1VgLHbzCC/figures/026_Table_6.jpg]]
*Table 6: Comparison of time cost between PDDLLM and LLMTAMP reasoning variants*

#### 生成域质量分析

**Table 3** 量化了自动生成域与专家设计域（性能上界）的差距。在Stack、Burger Cooking、Bridge Building、Tower of Hanoi四个任务上，缺失谓词比例最高为22.2%（Burger Cooking和Bridge Building），冗余谓词比例最高为16.7%（Tower of Hanoi）。缺失的谓词多为复杂高阶逻辑关系（如“clear”的变体），但未直接导致规划失败——这与消融实验中“缺失谓词增加规划时间但不一定导致失败”的观察一致。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_Y1VgLHbzCC/figures/007_Table_3.jpg]]
*Table 3: Percentage of missing or redun- Table 4: Bridge-building success rate (%) under varying dant predicates and actions across tasks. demonstration conditions*

**Table 4** 展示了域修复能力：在Bridge Building任务中，仅提供pick演示时成功率为0%；补充stack演示后升至20%；再补充align演示后跃升至86.7%；即使加入冗余的unstack演示，成功率仍稳定在83.3%。这表明系统能通过增加演示或优化语言指导有效修补缺失谓词。

#### 真实机器人验证

**Figure 4** 和 **Table 5** 展示了在三个不同硬件平台（Franka、Piper、UR5e）上的部署结果。Tower of Hanoi（Franka）成功率为9/10，Bridge Building（Franka）为8/10，Burger（Piper）和Table-top Stacking（UR5e）均为7/10。逻辑动作直接作为策略条件输入，绕过了仿真中的显式运动约束，验证了从仿真域到真实执行的迁移可行性。

### 消融实验

#### 并行提示与域生成可靠性

**Table 15**（原文附录）验证了并行提示策略的必要性：当并行提示数n_prompt≥15时，域生成失败率降至0%。主实验采用的n_prompt=10在多数任务上已足够，但复杂域可能需要更高并行度以多数表决确保质量。

#### 离散化尺度的影响

**Table 14** 分析了离散化尺度u_f对谓词质量的影响。减小u_f（更细粒度离散化）会增加冗余谓词比例，但对缺失谓词的影响较小。主实验采用u_f = d_min（最小非零差异）在谓词完整性与冗余度之间取得平衡。

#### 提示风格鲁棒性

**Table 7** 显示PDDLLM对不同提示风格具有高度鲁棒性，生成域的成功率始终接近100%，说明框架不依赖特定的提示工程技巧。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_Y1VgLHbzCC/figures/027_Table_7.jpg]]
*Table 7: Planning success rate for domains generated using different prompt styles*

#### LLM骨干的可替换性

**Table 19**（原文附录）表明PDDLLM在不同LLM骨干（GPT-4o、Qwen3-4B、Qwen3-8B）下总体成功率均维持在~93%水平，验证了方法对底层模型的低敏感性。

### 失败模式与局限性

1. **复杂高阶谓词缺失**：LLM生成的复杂高阶谓词偶尔缺失（Table 3），虽不直接导致规划失败，但在严格时限下可能因搜索空间增大而超时。
2. **感知噪声敏感性**：**Table 13**（原文附录）显示，当感知噪声超过20%时，谓词评估准确率降至约78%，限制了在低精度感知系统中的部署。
3. **物理仿真依赖**：方法依赖高精度物理仿真进行谓词验证，在仿真与真实世界差距较大的接触丰富任务（如紧公差插入）中仍具挑战性。
4. **非刚性物体局限**：当前方法主要适用于具有一致物理属性的刚性物体，不适用于可变形物体、流体或高度非结构化场景。

### 关键图表索引

| 图表 | 核心结论 |
|------|----------|
| **Table 1** | PDDLLM总体成功率93.3%，较最佳基线提升40%+ |
| **Table 2** | 较推理LLM方法成功率高19%且Token成本低38% |
| **Table 3** | 生成域缺失谓词≤22.2%，冗余谓词≤16.7% |
| **Table 4** | 通过补充演示可修复缺失谓词，成功率从0%恢复至86.7% |
| **Figure 3** | 性能随物体数和时限增加保持鲁棒，饱和速度最快 |
| **Figure 4** | 三个真实机器人平台成功执行多项操作任务 |

## 定位与知识库关联

### 1. 核心瓶颈与因果机制

任务与运动规划（TAMP）长期受困于一个根本性瓶颈：**规划域（PDDL domain）的构建高度依赖人工专家知识**，需要手动定义谓词库、动作模型及其与底层运动规划的数学约束接口。这一过程不仅劳动密集、易出错，且难以扩展到新任务与新场景，构成了机器人自主长时序操作的关键卡点。

PDDLLM 的因果调节变量在于**将 LLM 的符号推理能力与物理仿真反馈深度耦合**，实现了从单次演示到可执行规划域的全自动推导。其核心洞察可概括为三点：

- **仿真驱动的谓词发现**：通过大规模并行物理仿真采样对象间的连续空间关系，利用仿真器过滤不可行配置，再交由 LLM 将可行子空间总结为有物理意义的一阶谓词，并通过逻辑算子（`not`、`forall`）组合导出高阶谓词（如 `(forall_?o1 (not_is_on ?o1 ?o2))` 表示 ?o2 上方无任何物体）。这一“仿真采样→LLM 总结”的闭环，将连续状态离散化过程自动化，彻底消除了对手动定义谓词的需求。
- **逻辑状态转换驱动的动作发明**：从演示轨迹中提取逻辑状态的前后变化，将其作为 LLM 提示，直接推断出 PDDL 动作的完整定义（前提条件与效果），无需任何预定义动作模板。
- **逻辑-运动自动桥接（LoCA）**：通过检索动作效果谓词所关联的物理约束，自动将逻辑动作转化为标准约束运动规划问题，消除了传统方法中为每个动作手工编写运动约束接口的繁琐步骤。

### 2. 在 LLM 驱动规划谱系中的定位

PDDLLM 处于 **LLM 驱动规划方法谱系**中“域推导”这一独特位置。现有 LLM 规划方法可大致分为三类，PDDLLM 在每一类上均体现出结构性差异：

**第一类：直接任务规划（LLMTAMP 系列）**
- **LLMTAMP**（Huang et al., 2022a）将 LLM 作为端到端任务规划器，直接输出动作序列，但缺少反馈机制，在复杂长时序任务上整体成功率仅 35.7%。
- **LLMTAMP-FF**（Huang et al., 2022b; Chen et al., 2024a）加入失败反馈环，允许失败后重新规划，但仍依赖 LLM 在线推理，在 Hanoi 塔等需要深度逻辑推理的任务上成功率仅 14.3%。
- **LLMTAMP-FR**（Wang et al., 2024）进一步引入失败原因推理，但本质上仍属于“在线推理”范式，未解决域知识缺失的根本问题。

PDDLLM 与上述方法的本质区别在于**将“域知识获取”与“任务规划执行”解耦**：域推导仅需一次（one-shot），后续所有规划任务由经典符号求解器（PDDLStream）完成，无需 LLM 在线参与。这解释了为何 PDDLLM 在 1200+ 任务上整体成功率（93.3%）比最强 LLM 基线高出 40 个百分点。

**第二类：推理增强型 LLM 规划（o1-TAMP、R1-TAMP）**
- **o1-TAMP**（OpenAI, 2024）和 **R1-TAMP**（DeepSeek-AI, 2025）使用具有链式思维推理能力的 LLM 作为规划骨干，试图通过更强的推理弥补域知识缺失。在复杂任务上，o1-TAMP 成功率达 61.5%，R1-TAMP 为 35.9%。

然而，PDDLLM 在复杂任务上以 **80.5% 的成功率**超越二者，且 token 消耗（415k）远低于 o1-TAMP（666k）和 R1-TAMP（725k）。这表明，**将推理能力前置投入域推导，而非在每个规划实例上反复推理，是更高效且更可靠的范式**。

**第三类：域记忆增强（RuleAsMem）**
- **RuleAsMem** 作为消融实验，将 PDDLLM 生成的域作为上下文记忆直接提供给 LLM 规划器，而不使用符号求解器。其整体成功率为 70.8%，低于 PDDLLM 的 93.3%，但高于所有纯 LLM 基线。这从反面证明了**符号求解器与自动推导域的协同效应**——域知识本身有价值，但将其与可证明正确的符号搜索结合才能最大化性能。

### 3. 关键方法槽位对比

| 方法槽位 | 传统 TAMP / LLMTAMP | PDDLLM |
|---------|-------------------|--------|
| 域构建 | 人工编写 PDDL 域 | 单次演示自动生成（LLM + 仿真验证） |
| 运动规划接口 | 为每个逻辑动作手工编写数学约束 | LoCA 自动从动作效果谓词生成 |
| 谓词库 | 预定义或部分预定义 | 谓词想象（仿真采样 + LLM 总结）自动生成 |
| 规划执行 | LLM 在线推理或人工域 + 求解器 | 自动域 + 符号求解器 |

### 4. 适用边界与局限

PDDLLM 的能力边界由以下因素界定：

**适用场景**：具有一致物体物理属性、结构化场景几何的操作任务。仿真器能够准确建模刚体交互，且对象间关系可通过空间/物理谓词充分表达的任务类型最为适合。

**已知局限**：
- **物理建模局限**：不适用于可变形物体、流体或高度非刚性材料的操作。仿真器对这些现象的建模精度不足，将导致谓词想象偏差。
- **精细操作挑战**：紧公差插入等需要亚毫米级特征建模的任务仍具挑战性，仿真微小误差可能导致实际行为偏差。
- **动态环境适应性有限**：无法处理不可预测的物体属性变化或接触动态变化，因为域推导依赖于演示中观察到的稳定物理规律。
- **高阶谓词完整性**：LLM 生成的复杂高阶谓词偶尔会缺失（如 Table 3 所示，Burger Cooking 和 Bridge Building 任务缺失率最高达 22.2%）。虽然缺失谓词不直接导致规划失败，但会增加规划时间，在严格时限（50s）下可能超时。
- **感知噪声敏感性**：当感知噪声超过 20% 时，谓词评估准确率降至约 78%，限制了在低精度感知系统中的部署。

### 5. 开放问题与未来方向

PDDLLM 开启的“从演示到域”范式引出以下开放问题：

1. **感知-域推导闭环**：当前系统依赖已知物体状态进行谓词评估。如何集成感知模块，直接从原始感官输入（图像、点云）进行域推导，是走向完全自主的关键一步。
2. **交互式域补全**：当生成的域存在缺失谓词时（如 Table 4 所示，仅提供 pick 演示时成功率为 0%），系统能否主动与环境交互获取反馈，自动发现并补全缺失知识？这需要将当前的“一次推导”扩展为“交互式增量学习”。
3. **部分可观测环境**：如何使系统在部分可观测环境中通过主动探索获取缺失信息，完成域推导与任务规划？
4. **接触丰富操作扩展**：将方法扩展到涉及复杂接触动力学的装配、双手协调等任务，需要仿真器精度和谓词表达能力的同步提升。
5. **仿真-现实差距缓解**：当前方法对高精度物理仿真器有较强依赖。如何在仿真不精确的情况下保持域推导的可靠性，是实际部署中的关键挑战。

**验证说明**：上述局限与开放问题均来自论文明确讨论（Section 9 Limitations, Section 11 Future Works），置信度高。关于具体基线工作的引用信息（如 Huang et al., 2022a 等）来自论文参考文献，作者/年份/会议信息以原文为准，未做额外推断。

## 原文 PDF

![[paperPDFs/ICLR_2026/One_Demo_Is_All_It_Takes_Planning_Domain_Derivation_with_LLMs_from_A_Single_Demonstration.pdf]]
