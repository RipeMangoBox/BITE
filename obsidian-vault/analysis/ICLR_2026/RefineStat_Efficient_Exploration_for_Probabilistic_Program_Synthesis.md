---
title: "RefineStat: Efficient Exploration for Probabilistic Program Synthesis"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/RefineStat_Efficient_Exploration_for_Probabilistic_Program_Synthesis.pdf
project_link: null
code_link: https://github.com/structuredllm/RefineStat
openreview_forum_id: SAl337ZX5d
aliases:
- RefineStat
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/probabilistic_methods
core_operator: "通过语义约束解码（六种有效性谓词：可解析性、分布有效性、参数有效性、依赖有效性、支撑集有效性、类型有效性）确保生成程序的基本正确性，并结合基于贝叶斯工作流诊断（R-hat、ESS、发散数、Pareto k等）的细化策略，有针对性地重采样似然或先验组件以提升统计可靠性。"
primary_logic: "将标准贝叶斯工作流诊断指标转化为反馈信号，驱动SLM迭代修正程序片段（似然或先验），配合解码时的语义约束，使得小模型也能生成与大型专有模型（如GPT-4）相媲美甚至更优的可靠概率程序。"
claims:
- "REFINESTAT的运行成功率比无约束标准基线高约40个百分点，比仅语法约束的Syncode高30个百分点。"
- "在Surgical数据集上，标准基线产生超过1000次发散，而REFINESTAT为零；DQ-7B在无约束时所有数据集均失败，而配合REFINESTAT后全部成功。"
- "REFINESTAT配合DQ-7B在Peregrine数据集上的ELPD-LOO远优于BoxLM（-114.29 vs -173.11），并超越OpenAI o3。"
- "移除参数有效性检查导致编译成功率下降14.5个百分点，是所有验证组件中最关键的。"
---

# RefineStat: Efficient Exploration for Probabilistic Program Synthesis

> [!tip] 核心洞察
> 将标准贝叶斯工作流诊断指标转化为反馈信号，驱动SLM迭代修正程序片段（似然或先验），配合解码时的语义约束，使得小模型也能生成与大型专有模型（如GPT-4）相媲美甚至更优的可靠概率程序。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | RefineStat：概率程序合成的高效探索 |
| 英文题名 | RefineStat: Efficient Exploration for Probabilistic Program Synthesis |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=SAl337ZX5d) · [GitHub](https://github.com/structuredllm/RefineStat) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/probabilistic_methods |
| Method | REFINESTAT |
| Dataset | All 5 datasets (aggregated), Surgical, Peregrine, All 5 datasets |

> [!tip] 效果简介
> - All 5 datasets (aggregated) 上，Run rate (Temp 0.2) 为 0.45，对比 0.10 (Standard)，变化 +0.35。
> - Surgical 上，Divergences 为 0，对比 >1000 (Standard, Meta-Llama)，变化 −1000+。
> - Peregrine 上，ELPD LOO 为 -114.29 ± 2.76 (REFINESTAT w/ DQ-7B)，对比 -173.11 (BoxLM w/ GPT-4)，变化 +58.82。

## 概要

**问题瓶颈**：小语言模型（SLM）在生成概率程序时频繁出现语义错误——例如将方差错误地用作标准差参数、调用不存在的API——以及采样发散问题，导致程序无法通过贝叶斯工作流诊断，统计推断不可靠。

**核心思路**：REFINESTAT 将标准贝叶斯工作流诊断指标转化为反馈信号，驱动 SLM 迭代修正程序片段（似然或先验），配合解码时的语义约束，使得小模型也能生成与大型专有模型（如 GPT-4）相媲美甚至更优的可靠概率程序。

**方法定位**：REFINESTAT 通过两条互补路径实现可靠性保障。其一为**语义约束解码**，在逐语句生成过程中以六种有效性谓词（可解析性、分布有效性、参数有效性、依赖有效性、支撑集有效性、类型有效性）进行局部拒绝采样，确保生成片段的基本正确性。其二为**诊断感知的细化循环**，当程序通过 MCMC 推理后未能达到贝叶斯工作流可靠性得分阈值（≥5/7）时，有针对性地重采样似然或先验组件，直至收集到足够有效的候选程序，最终选取 ELPD-LOO 最高的模型输出。

**主要结果**：

- **运行成功率**：REFINESTAT 的运行成功率比无约束标准基线高约 35 个百分点，比仅语法约束的 Syncode 高约 30 个百分点（Table 1）。
- **采样健康性**：在 Surgical 数据集上，标准基线产生超过 1000 次发散，而 REFINESTAT 为零；DQ-7B 在无约束时所有数据集均失败，配合 REFINESTAT 后全部成功（Table 2, Section 5.2）。
- **预测性能**：REFINESTAT 配合 DQ-7B 在 Peregrine 数据集上的 ELPD-LOO 远优于使用 GPT-4 的 BoxLM（-114.29 vs -173.11），并超越 OpenAI o3（Table 3）。
- **消融关键发现**：移除参数有效性检查导致编译成功率下降 14.5 个百分点，是所有验证组件中最关键的（Table 4）。

概率编程是贝叶斯统计推断的核心工具，它允许研究者以声明式的方式定义先验和似然，并依赖现代概率编程语言（PPL）如PyMC、Stan等自动执行马尔可夫链蒙特卡洛（MCMC）推理。然而，编写一个语法正确且统计可靠的概率程序需要深厚的领域知识——不仅要熟悉PPL的API规范，还要理解贝叶斯工作流中的诊断指标（如收敛性、发散性、预测有效性），这对非专业用户构成了极高的门槛。

近年来，大语言模型（LLM）在代码生成领域展现出令人瞩目的能力。但将LLM直接应用于概率程序合成面临一个**核心瓶颈**：小语言模型（SLM）在生成概率程序时经常产生语义错误和采样发散问题。具体表现为：（1）错误地将方差用作标准差参数（如PyMC中废弃的`sd`参数）；（2）调用目标PPL中不存在的API；（3）生成的程序虽然语法正确，但MCMC推理后产生大量发散或无法收敛，导致统计推断完全不可靠。这些失败模式使得“生成-执行-报错”的简单循环难以奏效，因为程序可能成功运行却产生错误的统计结论。

现有方法在此问题上存在明显缺口。**无约束生成**（Standard baseline）直接向LLM查询生成程序，缺乏任何正确性保障，运行成功率极低（约10%）。**Syncode**（Ugare et al., 2024）引入了语法约束解码，能消除语法错误，但完全无法处理语义层面的问题——它无法阻止模型使用错误的分布参数或生成统计上不可靠的似然函数。**BoxLM**（Li et al., 2024）代表了另一条路线：使用两个GPT-4实例进行迭代式的程序提议和精炼。虽然取得了较好的效果，但该方法依赖大型专有模型，计算成本高昂，且其精炼策略缺乏对贝叶斯工作流诊断指标的系统利用。

本文的**核心动机**在于：能否让单个开源小语言模型（≤8B参数）通过系统性的语义约束和诊断感知的迭代细化，生成与大型专有模型相媲美甚至更优的可靠概率程序？这一目标的实现需要解决两个关键挑战：（1）如何在解码阶段就阻止语义无效的程序片段生成；（2）如何将标准贝叶斯工作流诊断指标（如R-hat、ESS、发散数、Pareto k等）转化为有效的反馈信号，驱动模型有针对性地修正统计可靠性问题。

## 核心方法与创新机理

REFINESTAT 的核心创新在于将**语义约束解码**与**诊断感知的迭代细化**组合为一个闭环系统，使小语言模型（SLM，≤8B 参数）能够生成统计可靠的概率程序。与现有方法相比，其关键变化槽位体现在三个层面。

### 从无约束生成到语义约束解码

标准方法直接向语言模型查询生成完整程序，仅依赖模型自身的采样分布，产生大量语法错误和语义错误（如将方差误用作标准差参数 `sd`、调用不存在的 API）。Syncode（Ugare et al., 2024）仅执行语法约束解码，消除了语法错误，但无法处理语义问题。

REFINESTAT 在逐语句生成过程中嵌入**六种有效性谓词**，通过局部拒绝采样确保每个程序片段同时满足语法和基本语义约束：

- **可解析性**（parse-ability）：生成的代码片段能否被目标概率编程语言解析；
- **分布有效性**：引用的概率分布是否存在于语言标准库中；
- **参数有效性**：传递给分布的参数是否属于其认可的规范集合；
- **依赖有效性**：变量间的依赖关系是否符合模型规范；
- **支撑集有效性**：分布的支撑集与数据范围是否兼容；
- **类型有效性**：表达式的类型是否与上下文期望一致。

总体有效性检查为上述谓词的合取：

$$\Phi ( n , \pi ) = \phi ^ { 1 } ( n , \pi ) \wedge \phi ^ { 2 } ( n , \pi ) \wedge \dots \wedge \phi ^ { m } ( n , \pi )$$

其中参数有效性谓词的形式化定义为：

$$\phi _ { 3 } ( s , \Pi ) = \prod _ { f \in \mathcal { F } ( s ) } \mathbf { 1 } \{ P ( f ) \subseteq P _ { \operatorname { a c c } } ( f ) \}$$

该机制在生成阶段即拦截了大部分导致程序编译失败的语义错误。消融实验（Table 4）表明，移除参数有效性检查导致编译成功率下降 **14.5 个百分点**，是所有验证组件中影响最大的；移除分布有效性检查下降 9 个百分点，移除语法解析检查下降 5.5 个百分点。

### 从单次生成到诊断感知的迭代细化

标准方法和 Syncode 均采用单次生成即返回的策略，无法修复推理阶段暴露的统计问题（如采样发散、收敛失败）。BoxLM（Li et al., 2024）使用两个 GPT-4 实例进行迭代提议和精炼，但依赖大型专有模型。

REFINESTAT 将**贝叶斯工作流诊断指标**转化为反馈信号，驱动 SLM 进行有针对性的程序片段修正。具体而言：

1. **可靠性评估**：对完整程序执行 MCMC 推理，计算七项诊断指标（split-R̂、ESS_bulk、ESS_tail、发散数、BFMI、Pareto k、有限 ELPD），汇总为贝叶斯工作流可靠性得分 $\mathcal{B}(M)$。当 $\mathcal{B}(M) < \zeta = 5$ 时触发细化。

2. **分层细化策略**：首先在数据-先验上下文中通过约束解码重新生成似然块（最多 2 次尝试）；若仍无效，则在数据上下文中重新生成先验块（总预算 100 轮）。这种分层策略针对性地修复了最常见的两类失败模式——似然规范错误和先验规范错误。

3. **模型选择**：在所有通过可靠性检查的候选程序中，选择 ELPD-LOO 最高的程序作为最终输出：

$$M^{*} = \arg\max_{M \in \mathcal{M}_{\mathrm{valid}}} \widehat{\mathrm{elpd}}(M)$$

其中有效模型空间定义为：

$$\mathcal{M}_{\mathrm{valid}} = \{ M \in \mathcal{M} : \mathcal{B}(M) \geq \zeta \}$$

### 因果机制：为什么小模型能超越大模型

REFINESTAT 的有效性源于一个关键的因果闭环：**语义约束解码缩小了搜索空间，使 SLM 的有限容量集中在统计合理的程序子集上；诊断反馈进一步引导搜索朝向贝叶斯工作流可靠的区域**。这一机制解释了为什么配合 DQ-7B 的 REFINESTAT 能在 Peregrine 数据集上以 ELPD-LOO −114.29 显著超越 BoxLM（GPT-4）的 −173.11，并在 Surgical 数据集上将发散数从标准基线的 1000+ 降至零。核心洞察在于：概率程序合成的瓶颈并非模型规模，而是缺乏结构化的正确性保障和统计反馈回路。

REFINESTAT 是一个两阶段概率程序合成框架，其核心目标是将小语言模型（SLM）生成的不可靠程序，转化为符合贝叶斯工作流标准的统计推断工具。整个 pipeline 由五个关键模块串联构成，形成一个“生成—约束—诊断—细化—选择”的闭环。

### 输入与输出

框架的输入包含两部分：用户提供的观测数据 $\mathcal{D}$ 和自然语言描述的任务提示。输出是一个通过贝叶斯可靠性检查、且 ELPD-LOO 估计值最优的完整概率程序 $\mathcal{D} \| \mathcal{P} \| \mathcal{L}$（数据块、先验块、似然块的组合）。

### 管道模块

**1. 语义约束解码 (Semantically-Constrained Decoding)**

这是管道的第一道防线。语言模型逐语句生成程序片段时，框架对每个片段执行局部拒绝采样：反复从 $S_N$ 中采样候选片段 $s$，直到找到满足总体有效性谓词 $\Phi(s, \Pi) = \bigwedge_{i=1}^{6} \phi_i(s, \Pi)$ 的 $s^*$。六种谓词分别检查：

- **可解析性** ($\phi_1$)：程序片段是否可被概率编程语言的解析器正确解析。
- **分布有效性** ($\phi_2$)：调用的概率分布是否在目标语言（如 PyMC）中存在。
- **参数有效性** ($\phi_3$)：分布的参数是否属于其认可的规范集合，例如将废弃的 `sd` 参数自动纠正为 `sigma`（见 Figure 2）。
- **依赖有效性** ($\phi_4$)：变量之间的依赖关系是否符合模型规范。
- **支撑集有效性** ($\phi_5$)：分布的支撑集是否与数据兼容。
- **类型有效性** ($\phi_6$)：表达式的类型是否与上下文一致。

该模块确保生成的程序片段在语法和基础语义层面正确，大幅削减了后续推理阶段的编译失败风险。

**2. 贝叶斯可靠性检查 (Bayesian Reliability Check)**

完整程序生成后，框架对其执行 MCMC 推理，并计算七项诊断指标：split-$\hat{R}$、ESS_bulk、ESS_tail、发散数、BFMI、Pareto k 和有限 ELPD 可用性。这些指标被汇总为贝叶斯工作流可靠性得分 $\mathcal{B}(M) = \sum_{j=1}^7 s_j(M)$，其中每个 $s_j(M) \in \{0,1\}$ 表示对应诊断是否通过。若 $\mathcal{B}(M) \geq \zeta$（阈值 $\zeta=5$），则程序进入有效模型空间 $\mathcal{M}_{\mathrm{valid}}$；否则触发细化流程。

**3. 似然细化 (Likelihood Refinement)**

当诊断失败时，框架首先尝试在数据-先验上下文中通过约束解码重新生成似然块：$\mathcal{L} \leftarrow \mathcal{L}_{\mathrm{CD}}(\mathcal{D} \| \mathcal{P})$。似然重采样最多执行两次，旨在修复收敛或采样健康问题。

**4. 先验细化 (Prior Refinement)**

若似然重采样后程序仍未通过可靠性检查，框架回退到先验块的重生成：$\mathcal{P} \leftarrow \mathcal{L}_{\mathrm{CD}}(\mathcal{D})$。整个细化循环的总预算为 100 轮，确保在有限资源内尽可能收集有效程序。

**5. 模型选择 (Model Selection)**

在所有通过可靠性检查的候选模型中，框架选择 ELPD-LOO 估计值最高的程序作为最终输出：

$$M^{*} = \arg\max_{M \in \mathcal{M}_{\mathrm{valid}}} \widehat{\mathrm{elpd}}(M)$$

其中 $\widehat{\mathrm{elpd}}_{\mathrm{PSIS-LOO}} = \sum_{i=1}^{n} \log \Big[ \frac{1}{S} \sum_{s=1}^{S} \tilde{w}_i^{(s)} p(y_i \mid \theta^{(s)}) \Big]$ 是 Pareto 平滑重要性采样留一交叉验证对期望对数逐点预测密度的估计，用于最大化样本外预测精度。

### 数据流与控制流

整个流程的控制逻辑如 Algorithm 1 所述：首先生成语义正确的程序骨架，然后评估贝叶斯诊断，根据诊断结果决定是否进入似然或先验细化循环。Figure 1 直观展示了从用户输入到最终可靠程序的四步流程——生成、语义约束解码、贝叶斯可靠性检查与细化、输出。

### 关键设计决策

框架的两个核心创新点——语义约束解码和诊断感知细化——分别针对概率程序合成的两大瓶颈：语义错误（如 API 幻觉、参数误用）和统计不可靠性（如采样发散、收敛失败）。前者通过局部拒绝采样在生成阶段拦截错误，后者通过贝叶斯工作流诊断驱动迭代修正。两者配合使得单个未修改的 7B 参数 SLM 即可生成与大型专有模型相媲美的可靠程序。

REFINESTAT 的核心由三个关键模块串联构成：语义约束解码、贝叶斯可靠性检查、以及诊断感知的迭代细化。以下逐一阐述其机制与核心公式。

### 语义约束解码

语言模型在生成概率程序时，逐语句产生代码片段。REFINESTAT 在每一语句生成后，立即通过局部拒绝采样机制验证其语义有效性：若当前片段违反任何约束谓词，则丢弃并重新采样，直至找到满足所有谓词的片段。

整体有效性由六个谓词的合取定义：

$$\Phi ( n , \pi ) = \phi ^ { 1 } ( n , \pi ) \wedge \phi ^ { 2 } ( n , \pi ) \wedge \dots \wedge \phi ^ { m } ( n , \pi )$$

其中 $n$ 为当前语法节点，$\pi$ 为部分解析树。六个谓词分别检查：

- **可解析性**：代码片段能否被概率编程语言解析器成功解析。
- **分布有效性**：调用的概率分布是否属于该语言认可的有效分布集合。
- **参数有效性**：传入分布的参数是否属于其合法参数规范。这是消融实验中影响最大的组件（移除后编译成功率下降14.5个百分点），其形式化定义为：

$$\phi _ { 3 } ( s , \Pi ) = \prod _ { f \in \mathcal { F } ( s ) } \mathbf { 1 } \{ P ( f ) \subseteq P _ { \operatorname { a c c } } ( f ) \}$$

其中 $\mathcal{F}(s)$ 为语句 $s$ 中调用的所有分布函数，$P(f)$ 为实际传入的参数集合，$P_{\text{acc}}(f)$ 为该分布认可的合法参数集合。

- **依赖有效性**：变量间的依赖关系是否合法（如似然中引用的变量是否已在先验中定义）。
- **支撑集有效性**：分布的支撑集是否与数据范围兼容。
- **类型有效性**：变量类型是否符合语言语义（如方差参数必须为正实数）。

通过这六项检查，REFINESTAT 在解码阶段即可拦截诸如“将方差误用作标准差参数”（`sd` vs `sigma`）或调用不存在 API 等典型错误，使得生成程序在进入推理阶段前即具备语法与基本语义正确性。

### 贝叶斯可靠性检查

完整程序生成后，REFINESTAT 执行 MCMC 推理并计算七项诊断指标，汇总为贝叶斯工作流可靠性得分 $\mathcal{B}(M)$。七项指标包括：split-$\hat{R}$（链间收敛）、ESS_bulk（有效样本量）、ESS_tail（尾部有效样本量）、发散数、BFMI（贝叶斯分数缺失信息）、Pareto $k$ 诊断、以及有限 ELPD 可用性。每项指标满足阈值则得 1 分，否则 0 分，总分范围 0–7。

有效模型空间定义为可靠性得分不低于阈值 $\zeta = 5$ 的候选模型集合：

$$\mathcal{M}_{\mathrm{valid}} = \{ M \in \mathcal{M} : \mathcal{B}(M) \geq \zeta \}$$

### 诊断感知的迭代细化

当程序未通过可靠性检查时，REFINESTAT 不丢弃整个程序，而是针对性地重采样问题组件。细化分两步：首先在数据-先验上下文中通过约束解码重新生成似然块；若似然重采样仍无法修复，则在数据上下文中重新生成先验块。整个过程受预算约束（似然最多重采样 2 次，先验总预算 100 轮），直至收集到足够的有效候选程序。

### 模型选择

在所有通过可靠性检查的候选程序中，REFINESTAT 选择 ELPD-LOO 估计值最高的程序作为最终输出。ELPD-LOO 通过 Pareto 平滑重要性采样留一交叉验证估计：

$$\widehat{\mathrm{elpd}}_{\mathrm{PSIS-LOO}} = \sum_{i=1}^{n} \log \Big[ \frac{1}{S} \sum_{s=1}^{S} \tilde{w}_i^{(s)} p(y_i \mid \theta^{(s)}) \Big]$$

其中 $n$ 为观测数，$S$ 为后验样本数，$\tilde{w}_i^{(s)}$ 为 Pareto 平滑后的重要性权重，$p(y_i \mid \theta^{(s)})$ 为第 $i$ 个观测在第 $s$ 个后验样本下的预测密度。最终优化目标为：

$$M^{*} = \arg\max_{M \in \mathcal{M}_{\mathrm{valid}}} \widehat{\mathrm{elpd}}(M)$$

即在有效模型空间中选取样本外预测精度最高的模型，从而在统计可靠性与预测性能之间取得平衡。

## 实验与关键发现

### 核心结果：运行成功率与诊断可靠性

REFINESTAT在程序合成成功率上展现出对基线方法的显著优势。Table 1汇总了不同温度设置下各方法的运行率（Run rate）：标准无约束基线在温度0.2时仅达0.10，仅引入语法约束的Syncode（Ugare et al., 2024）提升至0.21，而REFINESTAT达到0.45，比标准基线高出约35个百分点，比Syncode高出约24个百分点。这一差距源于语义约束解码对六类有效性谓词的强制执行——模型在逐语句生成过程中被阻止产生语法正确但语义无效的代码片段（如将方差误用作标准差参数、调用不存在的API）。

Table 2进一步揭示了程序质量的深层差异。在Surgical数据集上，标准基线（Meta-Llama）产生超过1000次MCMC采样发散，而REFINESTAT将发散数降至零。这直接验证了诊断感知细化循环的核心机制：当贝叶斯工作流可靠性得分低于阈值（ζ=5/7）时，系统自动重采样似然或先验组件，直至采样健康指标恢复正常。DQ-7B模型在无约束条件下所有五个数据集均失败（0/5成功率），而配合REFINESTAT后全部成功（5/5），表明语义约束与诊断反馈的结合使小模型也能跨越从“无法运行”到“统计可靠”的鸿沟。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_SAl337ZX5d/figures/005_Table_2.jpg]]
*Table 2: Comparison of Diagnostic Scores and ELPD-LOO for Standard vs. REFINESTAT*

### 预测性能：与大型模型和人类专家的对比

Table 3展示了ELPD-LOO（期望对数逐点预测密度的留一交叉验证估计）的对比结果。在Peregrine数据集上，REFINESTAT配合DQ-7B（7B参数）达到-114.29 ± 2.76，显著优于使用两个GPT-4实例的BoxLM（Li et al., 2024）的-173.11，并超越OpenAI o3。在Eight Schools数据集上，REFINESTAT的ELPD-LOO（-30.68 ± 0.11）与人类专家编写的Stan程序（-30.70）几乎持平。这得益于模型选择策略：在所有通过可靠性检查的候选程序中，系统选取ELPD-LOO最高的模型作为最终输出（Definition 4），从而在有效模型空间内最大化样本外预测精度。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_SAl337ZX5d/figures/004_Table_3.jpg]]
*Table 3: Comparison of ELPD LOO scores with BoxLM (Li et al., 2024), REFINESTAT using DQ-7B, and Expert values*

值得注意的失败模式出现在Dugongs数据集：尽管REFINESTAT的可靠性得分和收敛指标优于基线，其ELPD仍与专家程序存在差距。这表明当前诊断集合（R-hat、ESS、发散数、BFMI、Pareto k等）虽能有效过滤统计不可靠的程序，但未必能保证选出预测性能最优的模型——这是诊断覆盖范围的已知局限。

### 消融实验：语义验证组件的贡献

Table 4的系统消融揭示了各验证谓词的相对重要性。移除参数有效性检查（φ₃）导致编译成功率下降14.5个百分点，是所有组件中最关键的。该谓词验证调用的概率分布函数的参数是否属于其认可规范集合（如正态分布的标准差参数必须为正），直接阻止了最常见的语义错误类型。移除分布有效性检查（φ₂）导致9个百分点的下降，移除语法解析能力检查（φ₁）导致5.5个百分点的下降。此外，完全移除语法引导生成（即退化为无约束解码）使成功率下降10个百分点，证实了约束解码框架本身的必要性。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_SAl337ZX5d/figures/006_Table_4.jpg]]
*Table 4: Ablation Study: Impact of Semantic Validation Checks on Run rate*

### 跨后端泛化与效率分析

REFINESTAT的设计不绑定特定概率编程后端。Table 5和Table 6显示，在NumPyro后端上，REFINESTAT的运行率比标准基线提高一倍以上（0.33 vs 0.15），且获得相等或更高的可靠性得分和ELPD-LOO。这验证了语义约束谓词可在不同PPL间迁移，仅需调整API规范映射。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_SAl337ZX5d/figures/007_Table_5.jpg]]
*Table 5: Run-rate comparison when using NumPyro as the inference backend*

令牌效率方面（Table 8），REFINESTAT的平均令牌消耗约为基线的2倍，但在Dugongs上因提前收敛而降至0.6倍。这一开销主要来自约束解码中的局部拒绝采样和细化循环中的重采样，但考虑到成功率的大幅提升和统计可靠性的保障，该成本是可接受的。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_SAl337ZX5d/figures/010_Table_8.jpg]]
*Table 8: Comparison of Itergen, Baseline, and REFINESTAT Variants with Multipliers*

### 记忆化压力测试

为排除性能源于训练语料记忆的可能性，Table 9报告了记忆化压力测试结果。匿名化提示（AP）变体移除了变量名和上下文线索，语法混淆（SO）变体将数值改写为科学记数法，两者结合（AP+SO）进一步增加识别难度。在所有变体下，REFINESTAT保持了与原始版本相似的可靠性分数和ELPD，表明其有效性来自语义约束和诊断反馈机制，而非对训练集中特定程序的复现。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_SAl337ZX5d/figures/011_Table_9.jpg]]
*Table 9: Comparison of Diagnostic Scores and ELPD-LOO for REFINESTAT variants*

## 定位与知识库关联

### 与现有方法的谱系关系

REFINESTAT 处于概率程序合成与语言模型辅助统计建模的交叉地带，其核心贡献在于将**贝叶斯工作流诊断**系统性地嵌入小语言模型的生成-细化循环中。与相关工作的关系可沿两条轴线定位：

**约束解码轴线。** 最直接的对比对象是 **Syncode**（Ugare et al., 2024），后者仅执行语法层面的约束解码，能消除解析错误但无法处理语义问题——例如将方差错误地用作标准差参数、调用不存在的API签名等。REFINESTAT 将约束从语法层拓展到语义层，通过六种有效性谓词（可解析性、分布有效性、参数有效性、依赖有效性、支撑集有效性、类型有效性）进行局部拒绝采样，在生成阶段即阻断大量语义错误。实验证据表明，这一拓展带来了约30个百分点的运行率提升（Table 1：REFINESTAT 0.45 vs Syncode 0.21，温度0.2）。

**迭代精炼轴线。** **BoxLM**（Li et al., 2024）代表了使用大语言模型进行概率程序迭代合成的方法，其部署两个GPT-4实例分别负责提议和精炼程序。REFINESTAT 在方法论上与之共享“生成-诊断-修复”的循环结构，但存在三个关键差异：其一，REFINESTAT 使用单个未经微调的小语言模型（最大8B参数），而非双大模型协作；其二，精炼决策由标准贝叶斯工作流诊断指标（split-R̂、ESS_bulk、ESS_tail、发散数、BFMI、Pareto k、有限ELPD）驱动，而非依赖语言模型自身的判断；其三，精炼操作是结构化的——仅重采样似然块或先验块，而非重新生成整个程序。值得注意的是，REFINESTAT配合DQ-7B在Peregrine数据集上的ELPD-LOO（-114.29）显著优于BoxLM配合GPT-4（-173.11），且超越了OpenAI o3（Table 3），表明诊断感知的结构化精炼策略在统计可靠性上可以弥补模型规模的差距。

**无约束生成基线。** 标准无约束查询方式（即直接向语言模型索要概率程序）代表了最朴素的基线。REFINESTAT 相对于该基线的提升幅度约40个百分点（Table 1），且在诊断指标上表现出一致性优势——例如在Surgical数据集上，标准基线产生超过1000次发散，而REFINESTAT为零（Table 2, Section 5.2）。特别地，DQ-7B在无约束条件下所有五个数据集均失败（成功率0%），而配合REFINESTAT后全部成功（成功率100%），这直接证明了语义约束和诊断感知细化对于弱模型的赋能效应。

### 适用边界与局限性

**搜索空间的局部吸引子问题。** 尽管语义约束解码能过滤无效程序片段，但语言模型可能反复生成先前已被拒绝的代码模式（如持续使用已废弃的“sd”参数而非正确的“sigma”），难以逃离局部吸引子。这表明约束解码本身不改变语言模型的底层分布，仅做拒绝采样，当模型对错误模式赋予过高质量时，搜索效率会显著下降。

**数值不稳定性。** 即使程序通过了全部六种语义检查，仍可能因数值问题（如取零的对数、数值溢出）导致后验采样初始化失败。当前框架未在解码阶段捕获此类运行时数值异常，它们仅在MCMC推理阶段暴露。

**API幻觉。** 语言模型偶尔生成目标概率编程语言（如PyMC）中不存在的方法或签名，需由语义约束捕获。但验证谓词的定义依赖于对目标语言API的完整先验知识，这限制了该方法向新概率编程语言（如Stan、Turing.jl）的迁移——每种语言需要重新定义全部验证谓词。

**预算约束下的截断。** 在最大迭代次数或令牌限制内可能无法合成有效程序，导致截断输出。令牌效率分析（Table 8）显示，REFINESTAT平均令牌消耗是基线的2倍，但在某些数据集（如Dugongs）上因提前收敛而低于基线（0.6倍），说明效率高度依赖于问题难度和模型能力。

**诊断覆盖的有限性。** 当前仅纳入七项贝叶斯工作流诊断，尚未集成先验预测检查或后验预测检查。这意味着程序可能在通过当前诊断后，仍存在先验与数据的不匹配或后验预测的系统性偏差。

**实验覆盖的局限。** 评估仅限于五个标准基准数据集（Eight Schools、Dugongs、Surgical、Peregrine、GP），可能无法完全反映更复杂现实场景（如层次模型、非参数模型）的性能。此外，与人类专家编写的程序相比，在某些数据集（如Dugongs）上ELPD仍存在可观测的差距。

### 开放问题

1. **诊断体系的扩展。** 如何将先验预测检查或后验预测检查无缝集成到诊断感知的细化循环中？这需要定义可自动计算的检查指标，并将其转化为接受/拒绝的二元决策信号。

2. **搜索收敛性保证。** 当前方法缺乏对迭代搜索过程收敛到全局最优概率程序的理论保证。在存在局部吸引子的情况下，如何设计探索策略（如温度调度、多样性激励）以确保充分覆盖有效模型空间？

3. **记忆化效应的系统测量。** 尽管记忆化压力测试（Table 9）表明匿名化提示和语法混淆未显著影响性能，但如何更系统地测量和减轻大规模语言模型在概率程序生成中的记忆效应仍是一个开放问题。

4. **跨语言泛化。** 该方法能否以较小的工程代价扩展到其他概率编程语言（如Stan、Turing.jl），而不需要为每个语言重新定义所有验证谓词？是否存在一套语言无关的语义约束抽象层？

5. **策略优化。** 是否可以通过强化学习或偏好对齐（如基于ELPD的奖励信号）进一步优化程序生成策略，以提升最终模型的预测性能，而非仅依赖拒绝采样和重生成？

## 原文 PDF

![[paperPDFs/ICLR_2026/RefineStat_Efficient_Exploration_for_Probabilistic_Program_Synthesis.pdf]]
