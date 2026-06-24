---
title: "FormalML: A Benchmark for Evaluating Formal Subgoal Completion in Machine Learning Theory"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/FormalML_A_Benchmark_for_Evaluating_Formal_Subgoal_Completion_in_Machine_Learning_Theory.pdf
openreview_forum_id: wCRZbspSZi
aliases:
- FT
- FormalML
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "前提利用设置与模型推理风格（如CoT与noCoT）之间的相互作用直接调节子目标完成中的准确性与效率平衡，其中CoT容易诱发对简单子目标的过度思考，而恰当的前提选择能显著提升成功率。"
primary_logic: "虽然LLM在竞赛级定理证明中表现卓越，但在填补研究级证明的子目标时，现有证明器因无法有效利用前提并容易在CoT模式下过度推理，导致高难度问题上性能急剧下降；这一发现表明需要专门的数据集构建方法和训练策略来提升实际辅助数学家的能力。"
claims:
- "思维链提示在子目标完成任务中未能改善证明质量，反而降低效率。"
- "STP以63.21%的Pass@32取得FormalML上的最高整体性能。"
- "DeepSeek-Prover-V1.5在提供所有相关前提时Pass@32达71.86%，比无前提时提升13.49个百分点。"
- "FormalML (Overall) 上 Pass@32 = 63.21% (STP)"
---

# FormalML: A Benchmark for Evaluating Formal Subgoal Completion in Machine Learning Theory

> [!tip] 核心洞察
> 虽然LLM在竞赛级定理证明中表现卓越，但在填补研究级证明的子目标时，现有证明器因无法有效利用前提并容易在CoT模式下过度推理，导致高难度问题上性能急剧下降；这一发现表明需要专门的数据集构建方法和训练策略来提升实际辅助数学家的能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | FormalML：面向机器学习理论中形式化子目标完成的基准测试 |
| 英文题名 | FormalML: A Benchmark for Evaluating Formal Subgoal Completion in Machine Learning Theory |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=wCRZbspSZi); [GitHub](https://github.com/njuyxw/FormalML); [Project](https://huggingface.co/datasets/zzhisthebest/FormalML) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | FormalML基准构建（基于to_theorem策略的子目标提取） |
| Dataset | FormalML (Overall), FormalML premise utilization |

> [!tip] 效果简介
> - FormalML (Overall) 上，Pass@32 为 63.21% (STP)，对比 ~57.12% (DeepSeek-Prover-V2 noCoT，估计值)，变化 约+6%。
> - FormalML premise utilization 上，Pass@32 为 71.86% (DeepSeek-Prover-V1.5, M=*)，对比 58.37% (DeepSeek-Prover-V1.5, M=0)，变化 +13.49%。

## 概述

FormalML 是一个面向机器学习理论中**形式化子目标完成**的基准测试，旨在评估大语言模型在填补研究级证明过程中遗留的中间证明义务时的能力。现有 LLM 定理证明器虽然在竞赛级完整证明生成中表现卓越，但在处理具有复杂上下文的子目标时面临准确性与效率的双重瓶颈——思维链推理往往诱发对简单子目标的过度思考，而恰当的前提利用则能显著提升成功率。

本文的核心贡献在于：基于 Optlib 与 FoML 两个 Lean 4 形式化库，利用自定义的 `to_theorem` 策略从过程式证明脚本中自动提取子目标，构建了包含 4,937 个问题的数据集。实验表明，整体证明生成方法 STP 以 63.21% 的 Pass@32 取得最优性能，但所有证明器在高难度级别上通过率大幅下降；在前提利用方面，DeepSeek-Prover-V1.5 在提供所有相关前提时 Pass@32 达到 71.86%，较无前提设置提升 13.49 个百分点。这些发现揭示了子目标完成任务中推理深度与计算成本之间的根本性张力，为 LLM 辅助形式化定理证明的实用化指明了关键改进方向。

## 背景与动机

形式化定理证明在机器学习理论中的核心瓶颈，并非完整证明的自动生成，而是在复杂研究级上下文中**填补子目标**（subgoal completion）的能力。现有LLM定理证明器在竞赛级问题上已展现出卓越性能，但当面对研究级证明中遗留的短小但非平凡的子目标时，准确性和效率均面临持续限制。这一现象的背后存在两个相互关联的因果机制：

**前提利用的失调**。研究级证明通常依赖大量领域特定的前提（premises），而现有基准测试和证明器对此缺乏系统性支持。FormalML数据集中有1,547个定理需要显式使用前提才能完成证明（Table 3统计），但多数现有证明器在设计上未将前提选择作为核心能力进行优化。实验表明，当提供所有相关前提时，DeepSeek-Prover-V1.5的Pass@32可达71.86%，比无前提设置下的58.37%提升13.49个百分点（Table 4）——前提利用的质量直接调节了证明成功率。

**思维链推理的失效**。在自然语言推理中有效的思维链提示（chain-of-thought prompting），在子目标完成场景下不仅未能改善证明质量，反而降低效率。这一反直觉现象源于Long-CoT模型频繁误判子目标的复杂度：对于简单子目标，模型倾向于生成过细粒度的中间步骤（如通过`have`策略引入不必要的子目标），导致“过度思考”（overthinking）——生成更多证明行却降低了有效证明的比例（Appendix G.2）。效率加权准确率（Efficiency-Weighted Accuracy, EWA@K）指标进一步量化了这种准确性-效率的权衡：

$$EWA@K = Pass@K \times \frac{100}{\mathrm{ResponseLength}}$$

该公式将证明成功率与输出长度耦合，揭示了CoT模式下响应膨胀对实际可用性的损害。

**现有基准的缺口**。Table 1系统对比了现有Lean 4基准测试的覆盖维度：MiniF2F、PutnamBench、ProofNet、FormalMATH、LeanDojo和MiniCTX在问题类型、前提使用、复杂上下文和子目标完成四个维度上均存在不同程度的缺失。FormalML是首个在全部四个维度上均满足条件的基准，包含4,937个子目标完成问题，覆盖优化理论（Optlib库，2,907个定理）和概率理论（FoML库，2,030个定理）两大ML理论子领域（Table 2），并按证明长度划分为1、3、5三个难度级别（Figure 3左）。

**动机**。上述发现指向一个明确的研究方向：要推动LLM辅助形式化证明从竞赛级走向研究级实用化，必须解决子目标完成中的前提利用和推理效率问题。这需要专门的数据集构建方法——通过`to_theorem`策略从过程式证明脚本中提取子目标并封装为独立定理（Figure 2）——以及针对性的训练策略来抑制过度思考行为。

## 核心创新

FormalML 的核心创新在于将定理证明的评估范式从“完整证明生成”迁移到“子目标完成”，并围绕这一任务构建了首个系统性的基准。这一转变捕捉了实际形式化工作流中的真实瓶颈：人类数学家编写证明框架（sketch）后，大量简短但非平凡的子目标需要被自动消解，而现有证明器在此场景下暴露出准确性和效率的双重不足。

### 任务迁移：从完整证明到子目标完成

传统基准（如 miniF2F、ProofNet）要求模型从零生成完整证明，而 FormalML 将任务重新定义为**子目标完成**——给定一个包含复杂上下文和显式前提的证明环境，模型只需填补人类留下的证明空缺（`sorry` 占位符）。这一设计更贴近实际形式化场景中的交互模式：用户依赖自动证明器在冗长且复杂的证明中关闭子目标。

### 前提利用的强制性设计

FormalML 引入了**强制性的前提利用要求**——数据集中 1,547 个定理需要显式使用前提才能完成证明。这一设计直接针对现有证明器在前提选择上的薄弱环节。实验表明，前提利用设置与模型性能之间存在显著的因果交互：当提供所有相关前提时，DeepSeek-Prover-V1.5 的 Pass@32 从 58.37% 跃升至 71.86%（+13.49 个百分点），而简单增加候选前提数量（M=20）反而导致部分模型性能下降。这说明前提选择的质量而非数量是决定子目标完成成功率的关键调节变量。

### 上下文复杂度的系统性引入

与现有基准中相对孤立的证明问题不同，FormalML 的子目标嵌入在**复杂的研究级证明上下文**中。这种上下文复杂性使得思维链推理的局限性被显著放大——Long-CoT 模型频繁误判子目标复杂度，生成过多细粒度子目标（如通过 `have` 策略），导致过度思考并降低有效证明比例。这一发现揭示了现有推理范式在形式化证明场景中的根本性不匹配：自然语言推理中有效的 CoT 策略，在需要精确利用上下文的子目标完成中反而成为效率瓶颈。

### 数据集构建的符号化策略

为支撑上述创新，FormalML 采用了一种**符号化的数据集构建策略**——通过自定义的 `to_theorem` 策略，从过程式证明脚本中自动提取子目标。该策略捕获每个证明步骤执行前后的证明状态，抽象其状态转换，并合成为独立定理。通过调整提取时的证明段长度，可进一步生成不同难度级别（证明长度 1、3、5）的问题。这一策略保证了数据集的规模（4,937 个问题）和可复现性，同时避免了人工标注的成本和偏差。

## 整体框架

![[assets/figures/papers/iclr26_0011_wCRZbspSZi_FormalML_A_Benchmark_for_Evaluating_Formal_Subgo/figures/002_Figure_2.jpg]]
*Figure 2: An example of the to_theorem tactic illustrates its functionality. When applied to the tactic repeat rw [dotProduct]; simp [mul_comm], it captures pre- and post-execution proof states, abstracts their transition, and synthesizes a subgoal*

![[assets/figures/papers/iclr26_0011_wCRZbspSZi_FormalML_A_Benchmark_for_Evaluating_Formal_Subgo/figures/001_Table_1.jpg]]
*Table 1: Comparison of existing Lean 4 benchmarks*

![[assets/figures/papers/iclr26_0011_wCRZbspSZi_FormalML_A_Benchmark_for_Evaluating_Formal_Subgo/figures/003_Table_2.jpg]]
*Table 2: Statistics of theorems in FormalML across various machine learning theories*

FormalML 基准的构建围绕一个核心思想：将研究级证明中遗留的子目标转化为可独立评估的定理完成问题。整体流水线由四个串联模块构成，输入为 Optlib 与 FoML 两个 Lean 4 形式化库中的过程式证明脚本，输出为封装了源信息、形式化陈述、导入、策略序列与前提的 JSON 格式定理数据。

**数据源**。流水线的起点是两个覆盖机器学习理论核心分支的 Lean 4 库：Optlib（优化理论，含梯度下降、次梯度法、ADMM 等）与 FoML（概率理论，含集中不等式、测度论等）。二者合计提供 4,937 个定理的原始证明材料（Table 2），形成当前最大规模的 ML 理论形式化定理集合。

**子目标提取引擎**。核心模块是自定义的 `to_theorem` 策略。该策略在 Lean 4 内核层面运行，逐行捕获过程式证明脚本中每条策略执行前后的证明状态，将单步或多步（由难度参数控制）证明片段合成为独立子目标定理。通过调节提取的证明片段长度（1、3、5 步），同一原始证明可生成不同难度级别的子目标问题（Figure 3 左），从而构造出难度分级的评估体系。

**难度分级与前提统计**。提取后的子目标按证明长度划分为三个难度等级，并自动统计每个定理所需的外部前提。FormalML 中 1,547 个定理要求显式使用前提（Figure 3 右），这一设计直接催生了后续的前提利用实验（Table 4），构成该基准区别于现有 Lean 4 基准的关键特征之一（Table 1）。

**JSON 封装**。最终，每个定理被打包为结构化 JSON 对象，包含：源位置元数据、Lean 4 形式化陈述、所需模块导入与命名空间声明、完整的策略序列，以及前提列表。这一封装使得下游 LLM 证明器可直接解析问题描述与上下文，无需额外预处理。

整个流水线的设计瓶颈在于 `to_theorem` 策略对证明状态的捕获精度——若原始证明中存在隐式依赖或复杂上下文，提取的子目标可能丢失必要的前提信息。但从 Table 4 的前提利用实验（提供全部相关前提时 DeepSeek-Prover-V1.5 的 Pass@32 提升 13.49 个百分点）来看，该策略在多数情况下成功保留了子目标完成所需的关键上下文。

## 核心模块与公式推导

### 关键模块

#### 1. 子目标提取引擎：to_theorem 策略

FormalML 数据集构建的核心是一个定制的 Lean 4 策略 `to_theorem`，其功能是将过程式证明脚本中的逐行证明步骤自动提取为独立的子目标定理。该策略的操作机制如下：

- **状态捕获**：记录每个证明步骤执行前后的证明状态（proof state）。
- **转换抽象**：将前后状态的差异抽象为一个独立的子目标，该子目标包含了从当前状态到目标状态的完整逻辑跳跃。
- **难度控制**：通过调整提取时包含的证明步骤长度（1、3、5 行），生成不同难度级别的子目标问题。

这一策略使得原本嵌入在冗长证明上下文中的“证明义务”（proof obligations）被显式化为可独立求解的定理，构成了 FormalML 基准中 4,937 个子目标完成问题的基础。

#### 2. 数据封装格式

每个提取出的定理以 JSON 格式存储，包含以下字段：

- **源位置元数据**：定理在原始库中的位置信息。
- **形式化 Lean 4 定理陈述**：待证明的目标命题。
- **所需模块导入与命名空间声明**：确保定理可独立编译的上下文。
- **完整策略序列**：原始证明中对应步骤的完整策略代码。
- **前提列表**：定理证明所依赖的外部引理或定义。

其中，前提列表的显式记录是 FormalML 区别于其他基准的关键特征——共有 1,547 个定理需要显式使用前提才能完成证明。

### 关键公式

#### 效率加权准确率（Efficiency-Weighted Accuracy, EWA@K）

为同时评估证明器的准确性和生成效率，FormalML 引入了效率加权准确率指标：

$$EWA@K = Pass@K \times \frac{100}{\mathrm{ResponseLength}}$$

其中：
- **Pass@K**：在 K 次采样中至少有一次证明通过的比例，衡量证明成功率。
- **ResponseLength**：生成证明的平均输出长度（以 token 或字符计），衡量计算开销。

该指标的设计动机源于实验观察：长思维链（Long-CoT）模型虽然在自然语言推理中有效，但在子目标完成中频繁误判问题复杂度，生成过多的 `have` 语句等细粒度子目标，导致输出冗长却未能提升证明成功率。EWA@K 通过将成功率与输出长度直接挂钩，惩罚了这种“过度思考”（overthinking）行为，从而更真实地反映证明器在实际辅助数学家场景中的效用。

## 实验与分析

### 整体性能对比

FormalML 上自动化策略与 LLM 定理证明器的性能对比见 Table 3。以 Pass@32 衡量，**STP** 以 **63.21%** 取得最高整体通过率，DeepSeek-Prover-V2 (noCoT) 紧随其后（约 57.12%，估计值），两者差距约 6 个百分点。这一结果确立了全证明生成方法在当前基准上的主导地位。

![[assets/figures/papers/iclr26_0011_wCRZbspSZi_FormalML_A_Benchmark_for_Evaluating_Formal_Subgo/figures/006_Table_3.jpg]]
*Table 3: Performance comparison of automation tactics and LLM-based theorem provers on FormalML. The best results are in bold, and the second-best are underlined*

基于最佳优先搜索（BFS）的方法表现明显逊色——Reprover 和 BFS-Prover 的 Pass@K 均未突破 30%。内置自动化策略中，`aesop` 在低采样预算下（Pass@1/4）可超越部分 LLM，但在高预算下（Pass@32 达 43.29%）仍落后于顶级证明器；`simp`、`linarith` 等单策略工具则几乎无法独立完成子目标。

**关键瓶颈**：所有方法在难度提升时均出现性能急剧下降。Figure 4（右）显示，当证明长度从 1 增加到 3 和 5 时，通过率大幅下滑——即使最优的 STP，在难度 5 上 Pass@128 也仅 **33.36%**。这表明现有证明器在处理需要多步推理的复杂子目标时存在根本性局限。

![[assets/figures/papers/iclr26_0011_wCRZbspSZi_FormalML_A_Benchmark_for_Evaluating_Formal_Subgo/figures/009_Figure_4.jpg]]
*Figure 4: The left figure presents results of pass rate across various specific problem domains, while the right figure shows the performances under different difficulty levels*

### 前提利用的因果效应

前提利用设置构成调节准确率的关键因果旋钮。Table 4 揭示了清晰的剂量-响应关系：

![[assets/figures/papers/iclr26_0011_wCRZbspSZi_FormalML_A_Benchmark_for_Evaluating_Formal_Subgo/figures/010_Table_4.jpg]]
*Table 4: Pass@16/32 (%) of premise utilization. Relative improvements compared to M = 0 are shown in green (increase) or red (decrease)*

- **DeepSeek-Prover-V1.5**：当提供所有相关前提（M=*）时，Pass@32 从无前提时的 58.37% 跃升至 **71.86%**，提升 **+13.49 个百分点**，为所有证明器中最大增幅。
- **DeepSeek-Prover-V2 (noCoT)**：同样受益于完整前提，Pass@32 提升约 10 个百分点。
- **STP** 则呈现反常模式：在 M=10 和 M=20 时性能反而下降（M=20 时 Pass@32 降低 **-1.68%**），暗示该模型对前提候选集大小敏感，可能因上下文干扰而退化。

这一发现揭示了 **前提选择质量而非数量** 才是子目标完成效率的决定因素——不当的前提注入反而会损害证明器性能。

### CoT 的失效机制与效率权衡

思维链提示（CoT）在子目标完成中普遍失效，构成该基准最反直觉的发现。实验证据指向两类失效模式：

**过度思考**：Long-CoT 模型频繁误判子目标复杂度，生成过细粒度的中间子目标（如通过 `have` 策略引入不必要的辅助陈述），导致证明膨胀但有效完成率下降（Appendix G.2）。Table 5 的错误类型分析佐证了这一点——DeepSeek-Prover-V2 (CoT) 的 `has_error` 率低于 Goedel-Prover，但 `is_valid_with_sorry` 率更高（优化类 Pass@16 下为 10.68%），说明 CoT 模型倾向于用 `sorry` 占位符逃避困难子目标。

**效率代价**：为量化这一权衡，论文引入效率加权准确率：

$$EWA@K = Pass@K \times \frac{100}{\mathrm{ResponseLength}}$$

Figure 5（左）的效率对比显示，noCoT 变体在 EWA 指标上系统性优于 CoT 变体——CoT 虽未提升准确率，却显著增加了输出长度。这一结果挑战了“更深推理必然带来更好证明”的直觉，揭示了子目标完成场景下 **推理深度与计算成本之间的失衡**。

### 专家迭代的边际收益

Figure 5（右）展示了基于 88,174 个额外子目标进行专家迭代训练前后的性能变化。整体而言，专家迭代带来的提升有限，表明 **单纯扩大训练数据规模不足以解决子目标完成的核心困难**——模型需要更针对性的训练策略来学习前提选择与推理深度控制。

## 方法谱系与知识库定位

### 与现有定理证明基准的关系

FormalML 填补了现有 Lean 4 基准测试中的一项关键空白：**子目标完成**（subgoal completion）。Table 1 的对比显示，MiniF2F、PutnamBench、ProofNet、FormalMATH 等主流基准均聚焦于完整证明生成，而 LeanDojo 虽支持策略预测，却不涉及复杂上下文中子目标的独立证明。FormalML 是当前唯一在“前提利用”“复杂上下文”和“子目标完成”三个维度上同时满足条件的基准，这使其成为评估 LLM 在类人交互式证明辅助场景中实际能力的独特测试平台。

这一差异化定位源于数据构建策略的本质差异：FormalML 的 `to_theorem` 策略从过程式证明脚本中逐行提取子目标，而非直接采用人类手写的独立定理。这使得每个问题天然携带其原始证明上下文（包括已引入的变量、假设和中间结论），从而更真实地模拟了数学家在实际证明过程中“请帮我完成这个小目标”的交互模式。

### 与现有定理证明方法的适用边界

**Best-First Tree-Search（BFS）方法**（Reprover、BFS-Prover）在 FormalML 上的 Pass@K 均低于 30%（Table 3），暴露了启发式搜索在复杂上下文子目标上的根本局限。BFS 方法依赖对证明状态的启发式评分来分配搜索优先级，但当子目标嵌入了大量上下文变量和假设时，评分函数难以有效区分有希望的路径与死胡同，导致搜索效率急剧下降。

**Whole-Proof Generation 方法**（STP、DeepSeek-Prover-V2、Goedel-Prover 等）整体表现优于 BFS 方法，其中 STP 以 63.21% 的 Pass@32 取得最高整体性能（Table 3）。然而，这类方法在 FormalML 上的成功高度依赖于**前提利用设置**：DeepSeek-Prover-V1.5 在提供所有相关前提时 Pass@32 达 71.86%，比无前提时提升 13.49 个百分点（Table 4）。这一因果调节效应表明，当前证明器的瓶颈不在于生成能力本身，而在于**缺乏有效的上下文感知与前提检索机制**——当手动提供正确前提时，性能可大幅跃升，但模型自身尚无法可靠地完成这一选择。

**Lean 4 内置自动化策略**（aesop、simp、linarith 等）在低预算下可与部分 LLM 竞争（aesop Pass@1 达 43.29%），但其性能天花板明显——无法像 LLM 那样通过增加采样预算持续提升通过率。这表明符号化策略在简单子目标上具有效率优势，但在需要语义理解的高难度问题上存在不可逾越的边界。

### 思维链推理的失效机制

一个值得深入讨论的发现是：**思维链提示（CoT）在子目标完成中不仅未能改善证明质量，反而降低了效率**。Appendix G.2 的案例分析揭示了失效的因果链条：Long-CoT 模型频繁误判子目标的复杂度，将本可一步完成的简单子目标过度分解为多个 `have` 语句，生成大量不必要的细粒度中间目标。这种“过度思考”行为直接增加了输出长度，进而降低了效率加权准确率（EWA@K，定义为 $EWA@K = Pass@K \times \frac{100}{\mathrm{ResponseLength}}$），却未带来通过率的相应提升。

这一现象与 CoT 在自然语言推理中的有效性形成鲜明对比，暗示了形式化证明子目标与自然语言推理任务之间存在结构差异：子目标通常已由人类证明者进行了充分的难度分解，留给模型的部分往往不需要额外的推理步骤分解，而更需要精确的符号操作与前提匹配。

### 局限与开放问题

**领域覆盖的局限**：当前基准主要覆盖机器学习理论中的优化（Optlib）与概率（FoML）两个子领域，共 4,937 个定理。尚未扩展到信息论、统计学习理论、强化学习理论等其他 ML 相关领域。这一局限限制了基准在评估 LLM 辅助形式化证明时的领域泛化性。

**前提利用的未解难题**：Table 4 显示，当候选前提数量增加到 10 或 20 时，多数证明器的性能提升显著缩小甚至出现下降（STP 在 M=20 时 Pass@32 反而下降 1.68 个百分点）。这表明**大规模前提检索与精确选择**仍是未解决的瓶颈——模型在少量前提时能有效利用，但在更真实的“大海捞针”场景下表现不佳。

**推理效率与深度的平衡**：CoT 的失效和 EWA 指标的引入共同指向一个开放问题：如何在子目标完成中实现推理深度与计算成本的最优平衡？当前模型要么推理不足（noCoT 模式在复杂子目标上通过率低），要么推理过度（CoT 模式在简单子目标上浪费计算），缺乏根据子目标实际难度自适应调节推理深度的能力。

**训练策略的潜在方向**：Figure 5（右）的专家迭代实验表明，利用 `to_theorem` 策略从多个 Lean 仓库提取的 88,174 个问题进行训练后，模型在 FormalML 上的性能有所提升。这暗示了**大规模子目标完成数据的自动生成与训练**可能是提升实际辅助能力的关键路径，但如何设计更有效的训练策略以同时改善前提利用和推理效率，仍需进一步探索。

## 原文 PDF

![[paperPDFs/ICLR_2026/FormalML_A_Benchmark_for_Evaluating_Formal_Subgoal_Completion_in_Machine_Learning_Theory.pdf]]
