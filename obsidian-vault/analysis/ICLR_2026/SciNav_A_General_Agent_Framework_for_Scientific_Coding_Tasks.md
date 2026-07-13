---
title: "SciNav: A General Agent Framework for Scientific Coding Tasks"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SciNav_A_General_Agent_Framework_for_Scientific_Coding_Tasks.pdf
project_link: null
code_link: https://github.com/OSU-NLP-Group/SciNav
openreview_forum_id: 8iEsrg51Fs
aliases:
- SciNav
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/language_speech_and_dialog
core_operator: "基于成对相对判断的自适应Top-K树搜索 (Top-K Comparative Tree Search, TKCTS)"
primary_logic: "相对判断比绝对评分具有更高的区分力和可靠性，将其作为树搜索的指导信号，能够在有限计算预算下优先探索高潜力分支，从而显著提升科学编程任务的求解质量。"
claims:
- "SciNav builds upon Top-K Comparative Tree Search, using pairwise relative judgments to steer solution exploration under constrained budgets."
- "Relative judgments provide finer-grained and more reliable quality distinctions than absolute scoring, enabling effective search without pre-specified success metrics."
- "SciNav significantly outperforms strong baselines such as Self-Debug and OpenHands on multiple benchmarks and base models."
- "ScienceAgentBench 上 Success Rate (SR) = 16.1"
---

# SciNav: A General Agent Framework for Scientific Coding Tasks

> [!tip] 核心洞察
> 相对判断比绝对评分具有更高的区分力和可靠性，将其作为树搜索的指导信号，能够在有限计算预算下优先探索高潜力分支，从而显著提升科学编程任务的求解质量。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SciNav：面向科学编程任务的通用智能体框架 |
| 英文题名 | SciNav: A General Agent Framework for Scientific Coding Tasks |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=8iEsrg51Fs) · [GitHub](https://github.com/OSU-NLP-Group/SciNav) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/language_speech_and_dialog |
| Method | SciNav |
| Dataset | ScienceAgentBench, DA-Code (Data Manipulation & Stat. Analysis), DA-Code (Hard tasks) |

> [!tip] 效果简介
> - ScienceAgentBench 上，Success Rate (SR) 为 16.1，对比 14.7 (Self-Debug)，变化 +1.4。
> - ScienceAgentBench 上，Success Rate (SR) 为 18.6，对比 15.0 (Self-Debug)，变化 +3.6。
> - DA-Code (Data Manipulation & Stat. Analysis) 上，Performance Score 为 0.51 (Data Manipulation)，对比 0.22 (Self-Debug)，变化 +0.29 (29 absolute points gain)。

## 概要

科学编程任务（如数据分析、建模与统计推断）要求智能体在复杂解空间中生成正确且可执行的代码。现有科学智能体多面向开放性问题设计，依赖主观评估，难以进行严格比较；而科学编程基准虽提供客观指标，但主流方案仍为工程化的单次生成或迭代调试管道，缺乏结构化框架来高效探索解空间，且往往依赖预定义的成功指标和大量计算预算，难以泛化至实际多样化任务。

SciNav 针对上述瓶颈，提出**基于成对相对判断的自适应 Top-K 树搜索（Top-K Comparative Tree Search, TKCTS）**。其核心洞见在于：相对判断相比绝对评分具有更高的区分力和可靠性，将其作为树搜索的指导信号，能够在有限计算预算下优先扩展高潜力分支，从而显著提升求解质量。

在 ScienceAgentBench 基准上，SciNav 以 GPT-4o（2024-11-20）为基础模型时，成功率达到 18.6%，相较 Self-Debug（15.0%）相对提升 24%，较 OpenHands（13.1%）相对提升 22.9%；在 DA-Code 基准的数据处理与统计分析类任务上，SciNav 较 Self-Debug 取得 29 个绝对百分点的性能增益。消融实验证实，相对判断作为前沿比较器显著优于随机选择（+3.2 个百分点）和 LLM 绝对评分（+2.2 个百分点），而自我改进模块的引入使成功节点数量近乎翻倍。

SciNav 的方法定位与主要结果可概括为：以相对判断驱动的树搜索替代盲目探索，在不依赖预定义成功指标的前提下，实现有限预算下科学编程任务求解质量的跨模型、跨基准提升。



### 科学编程任务的自动化挑战

科学发现正日益依赖代码——从数据清洗、统计建模到数值模拟，编程已贯穿研究全流程。然而，将科学问题转化为正确、可执行的代码并非易事，它要求研究者同时具备领域知识、编程技能和调试经验。这一瓶颈催生了科学智能体的研究：利用大语言模型（LLM）自动完成科学编程任务，有望显著加速研究迭代。

### 现有方法的双重困境

当前的科学智能体研究呈现出明显的两极分化。一方面，面向开放科学发现的智能体（如全周期文献综述、实验设计到报告撰写）虽然展现了宏大的愿景，但其任务定义主观性强，难以进行严格的自动评估——这类系统的成功与否往往依赖人工判断或模糊的语义匹配，缺乏可复现的量化指标。另一方面，以 ScienceAgentBench 和 DA-Code 为代表的科学编程基准提供了客观的自动评估，但现有的智能体方案本质上仍是工程化的管道：它们要么依赖单次生成（Direct Prompting），要么采用无结构探索的迭代调试（Self-Debug），要么使用通用智能体框架逐步执行（OpenHands），却缺乏一个结构化的框架来有效探索庞大的解空间。

更深层的瓶颈在于**解空间探索的效率**。科学编程任务通常没有预先定义的成功指标——不同于数学证明可验证真伪，也不同于代码竞赛有明确的测试用例，科学任务的输出正确性往往需要通过领域知识间接推断。这使得传统基于绝对评分的搜索策略（如让 LLM 对单个方案打分）既不可靠又低效：LLM 的绝对评分容易产生校准偏差，难以在候选方案之间做出细粒度的区分。而随机选择或无探索的单轨迹方法则完全放弃了在有限计算预算内寻找更优解的可能性。

### 核心动机：用相对判断驱动结构化搜索

本文的核心动机源于一个关键洞察：**相对判断比绝对评分具有更高的区分力和可靠性**。已有研究表明，让 LLM 比较两个方案并判断哪个更好，比让它独立给每个方案打分，能产生更一致、更准确的质量信号。基于这一认知，SciNav 提出将成对相对判断嵌入到结构化的树搜索框架中，形成 Top-K 比较树搜索（Top-K Comparative Tree Search, TKCTS）。该方法在搜索早期广泛探索候选方案，但仅保留通过相对判断筛选出的 Top-K 个最有潜力的分支，从而在有限的计算预算下优先分配资源给高潜力轨迹，显著提升科学编程任务的求解质量。



## 核心方法与创新机理

SciNav 的核心创新在于将**成对相对判断**引入结构化树搜索，形成一种名为 **Top-K 比较树搜索 (Top-K Comparative Tree Search, TKCTS)** 的求解策略。这一设计直接回应了现有科学智能体的核心瓶颈：缺乏在有限计算预算下有效探索解空间的结构化框架。

### 从绝对评分到相对判断的范式转换

现有智能体在选择候选方案时，要么采用单次生成的随机选择，要么依赖 LLM 对单个方案进行绝对评分。这两种方式都存在根本性缺陷：随机选择缺乏方向性，而绝对评分——正如多项研究所指出的——在区分力和可靠性上均弱于相对判断 (Yan, 2024; Liu et al., 2024; Peyrard et al., 2021)。

SciNav 的 **Frontier Comparator** 模块将这一洞察工程化：它不再要求 LLM 为每个方案打一个孤立的分数，而是让 LLM 作为公正裁判，对方案进行**迭代式成对比较**。每轮比较后，通过 Elo 评分算法更新候选方案的排序，保留 Top-K 个最有潜力的分支继续探索，其余分支则被剪枝。这一机制的本质是将“哪个方案更好”这一相对问题替代“这个方案有多好”这一绝对问题——前者是 LLM 更擅长回答的。

### 从工程管道到结构化搜索

与 Self-Debug 等迭代调试方法不同，SciNav 不依赖单一轨迹的线性改进，而是构建了一棵以相对判断为导航信号的搜索树。其核心流程可概括为三个关键步骤：

1. **初始规划与候选生成**：基于任务描述生成多个高层计划，每个计划产出一个初步代码方案，形成初始候选池。
2. **前沿比较与剪枝**：Frontier Comparator 通过成对相对判断对候选方案排序，保留 Top-K 分支，其余剪枝。
3. **自我改进与扩展**：对保留的分支，提示模型识别具体改进点并生成精细化版本，扩展搜索树。

这种结构化的搜索策略使得 SciNav 能够在有限预算下优先探索高潜力分支，同时通过 Top-K 选择机制实现可控的回溯——当某个分支的改进陷入瓶颈时，搜索可以回退到其他有希望的方向。

### 关键设计选择：K=2 的平衡点

TKCTS 中的 K 值决定了搜索的宽度与深度的权衡。初步研究在 30 个 DA-Code 任务上测试了 K∈{1,2,3,4,5} 的表现，结果表明 K=2 提供了性能与成本的最佳平衡点——既能保持足够的探索多样性，又不会因分支过多而导致比较成本失控。所有后续实验均采用 K=2。

### 证据支撑

消融实验直接验证了相对判断的因果作用：在相同条件下，Relative Judgments 前沿比较器达到 18.6% 的成功率，显著优于 Random Selection 的 15.4% 和 LLM-Absolute 的 16.4%（Table 3）。自我改进模块的加入进一步将成功率从 45.2% 提升至 57.1%（Table 4），几乎使成功节点数量翻倍，表明相对判断引导的搜索与迭代改进之间存在协同效应。

需要注意的是，相对判断的质量受限于底层 LLM 的能力——当任务标准极为模糊或需要专业领域知识时，比较器可能给出次优指导。此外，树搜索结构虽然比盲目探索更高效，但仍会增加 LLM 调用次数和 token 消耗，相比单次生成成本更高。



![[assets/figures/papers/iclr26_0011_8iEsrg51Fs_SciNav_A_General_Agent_Framework_for_Scientific/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of Top-K Comparative Tree Search (TKCTS). Left: the search tree expands candidate solutions from an initial set, with relative comparisons (grey dashed arrows) guiding which branches and solutions to retain and explore. Right: comparison between absolute scoring, which LLM assigns pointwise scores to individual solutions, and relative judgment, which LLM evaluates solution pairs and provides sharper, more reliable distinctions. Relative judgments guide the search toward higher-quality solutions under constrained budgets*

SciNav 的核心设计目标是在有限计算预算下，对科学编程任务的解空间进行结构化探索。与现有的单次生成或线性调试范式不同，SciNav 将求解过程组织为一棵搜索树，并通过**基于成对相对判断的自适应 Top-K 树搜索 (Top-K Comparative Tree Search, TKCTS)** 来引导探索方向。

### 整体流程

SciNav 的求解流程由四个关键模块串联而成，形成“生成—调试—改进—筛选”的闭环：

1. **初始规划与代码生成 (Initial Planning and Code Generation)**：给定任务描述后，LLM 首先生成多个高层解决方案计划，随后为每个计划产出相应的初步代码实现，构成初始候选池。这一步通过多样化规划来扩大搜索的覆盖面。

2. **自我调试 (Self-Debug)**：利用代码解释器的执行反馈，对语法错误和运行时异常进行即时捕获与修复。该模块在不丢弃整个轨迹的前提下修正有缺陷的步骤，确保候选方案至少具备可执行性。

3. **迭代自我改进 (Iterative Self-Improve)**：针对前沿比较器筛选出的高潜力方案，提示模型通过反思性推理识别具体的改进点，并生成精细化的后续版本。消融实验表明，加入自我改进后，成功节点数量几乎翻倍（成功率从 45.2% 提升至 57.1%）。

4. **前沿比较器 (Frontier Comparator)**：这是整个框架的核心控制模块。它通过迭代式成对相对判断对候选方案进行排序，保留 Top-K 分支进行扩展，同时剪枝低潜力分支。与绝对评分不同，相对判断具有更高的区分力和可靠性，能够在无预定义成功指标的前提下有效指导搜索方向。

### 搜索机制的核心逻辑

TKCTS 的关键创新在于用**相对判断替代绝对评分**作为搜索的引导信号。具体而言，前沿比较器维护一个优先队列，每轮从队列中选取候选方案进行成对比较，随后通过排序算法（如 Elo 评分系统）更新方案的质量排序。Top-K 分支被保留以继续扩展，其余分支则被剪枝。这种策略既实现了受控回溯，又降低了后续比较评估的计算开销。

搜索树的宽度由超参数 K 控制。初步研究表明，K=2 是性能与成本之间的最佳平衡点——在提供有效搜索行为的同时，避免了过度的 LLM 调用开销。



### 整体架构：Top-K 比较树搜索 (TKCTS)

SciNav 的核心是一个由相对判断引导的 Top-K 树搜索框架——Top-K Comparative Tree Search (TKCTS)。其设计动机在于：绝对评分在区分候选方案质量时分辨力不足，而相对判断（成对比较）提供了更细粒度、更可靠的区分信号。TKCTS 将这一信号嵌入结构化搜索中，在有限计算预算下优先探索高潜力分支，同时剪枝低潜力轨迹。

搜索过程遵循 Algorithm 1 的伪代码逻辑，由四个关键模块串联构成。

### 模块一：初始规划与代码生成

给定任务描述，首先提示 LLM 生成多个高层计划，随后为每个计划产出一份对应的代码实现作为候选解。这一阶段构建初始候选池，为后续树搜索提供多样化的起点。

### 模块二：自我调试 (Self-Debug)

候选代码被送入 Python 解释器执行。若遇到语法错误或运行时异常，Self-Debug 模块利用解释器反馈进行即时修复，在不丢弃整条轨迹的前提下修正有缺陷的步骤。该模块确保每条分支在进入比较环节前达到可执行状态。

### 模块三：前沿比较器 (Frontier Comparator)

这是 SciNav 的核心创新模块。前沿比较器不再依赖单次绝对评分，而是将轨迹选择转化为一个比较性的迭代过程：

1. 将当前候选方案放入优先队列。
2. 对队列中的方案进行成对相对判断，由 LLM 以公正裁判的角色比较两个方案的质量并输出偏好。
3. 每轮比较后，对候选方案应用排序算法更新质量排序。
4. 保留 Top-K 个最有前景的分支进行扩展，其余剪枝。

该机制的关键优势在于：相对判断的区分力显著高于绝对评分。消融实验证实，相对判断前沿比较器实现 SR 18.6%，而随机选择仅 15.4%，LLM-Absolute 为 16.4%（Table 3）。即便与使用真实答案的 Rubric-Absolute 相比（SR 21.1%，VER 74.5%），相对判断在无需预定义成功指标的前提下已大幅缩小差距。

### 模块四：迭代自我改进 (Iterative Self-Improve)

针对前沿比较器选定的 Top-K 分支，该模块提示模型通过反思性推理识别具体的改进点，并生成精细化的后续版本。组件消融显示，在 5 个初始方案基础上启用自我改进后，成功率从 45.2% 跃升至 57.1%，成功节点数量几乎翻倍（Table 4）。

### 排序算法：Elo 评分系统

SciNav 采用 Elo 评分算法维护成对比较后的方案质量排序（详见 Appendix F）。核心公式如下：

方案 $P_i$ 面对方案 $P_j$ 时的预期得分：

$$E_i = \frac{1}{1 + 10^{(R_j - R_i)/400}}$$

其中 $R_i$、$R_j$ 分别为两方案的当前评分。每次比较后，根据实际结果 $S_i$（胜=1，平=0.5，负=0）更新评分：

$$R_i' = R_i + K \cdot (S_i - E_i)$$

其中 $K=32$ 为更新步长。该机制将每轮成对比较的结果平滑地整合进全局排序，为前沿比较器的 Top-K 选择提供稳定的数值基础。



## 实验与关键发现

### 主实验结果

SciNav 在多个基准和基模型上均表现出对强基线的显著提升。表 2 汇总了在 ScienceAgentBench 上的核心指标。以 GPT-4o (2024-11-20) 为例，SciNav 的成功率（SR）达到 18.6%，相比 Self-Debug 的 15.0% 提升 3.6 个百分点（相对增益 24%），相比 OpenHands 的 13.1% 提升 5.5 个百分点（相对增益 22.9%）。在有效执行率（VER）上，SciNav 达到 69.9%，比 Self-Debug 高出 7.8 个百分点，表明树搜索不仅提高了任务完成质量，还显著改善了代码的语法与运行时正确性。

![[assets/figures/papers/iclr26_0011_8iEsrg51Fs_SciNav_A_General_Agent_Framework_for_Scientific/figures/003_Table_2.jpg]]
*Table 2: Mean performances of each agent on ScienceAgentBench (Chen et al., 2025). Among the reported metrics, SR (Success Rate) is the most important as it directly reflects task success. VER (Valid Execution Rate) indicates whether a program can be executed without errors and is closely related to the number of debugging steps. Note that we run SciNav with 3 debug steps, while Self-Debug is run with 10 debug steps, which may occasionally allow Self-Debug to achieve higher VER than SciNav*

这一优势在不同基模型上具有一致性。在 GPT-4o (2024-05-13) 上，SciNav 的 SR 为 16.1%，分别超过 Self-Debug（14.7%）和 OpenHands（13.1%）；在 Claude-3.7 和 DeepSeek-R1 上也观察到类似的提升趋势。值得注意的是，Self-Debug 在实验设置中使用了 10 步调试，而 SciNav 仅使用 3 步，这意味着 SciNav 以更少的调试步数获得了更高的成功率，进一步凸显了结构化搜索的效率优势。

在 DA-Code 基准上，SciNav 的优势更加突出。如图 2(a) 所示，在数据操作（Data Manipulation）和统计分析（Statistical Analysis）两类任务上，SciNav 的性能得分分别达到 0.51 和 0.41，而 Self-Debug 仅为 0.22 和 0.18，绝对提升幅度分别达 29 和 23 个百分点。按难度分层后（图 2(b)），SciNav 在所有难度级别上均优于 Self-Debug，且差距随难度增加而扩大：在困难任务上，SciNav 得分为 0.41，Self-Debug 仅 0.18。这表明 TKCTS 的相对判断搜索机制在需要深层推理和复杂编程的科学任务中尤为有效。

![[assets/figures/papers/iclr26_0011_8iEsrg51Fs_SciNav_A_General_Agent_Framework_for_Scientific/figures/004_Figure_2.jpg]]
*Figure 2: (a) Performance by Task Type*

### 消融实验

#### 前沿比较器设计

表 3 对比了不同前沿比较器策略的效果。在 GPT-4o (2024-11-20) 上，基于相对判断（Relative Judgments）的比较器取得了 18.6% 的 SR 和 69.9% 的 VER，显著优于随机选择（Random Selection，SR 15.4%，VER 62.5%）和 LLM 绝对评分（LLM-Absolute，SR 16.4%，VER 65.2%）。相对判断相比随机选择提升了 3.2 个百分点的 SR，相比绝对评分提升了 2.2 个百分点。这一结果验证了核心假设：成对相对判断比单点绝对评分具有更高的区分力和可靠性，能够更有效地指导树搜索中的分支选择。

![[assets/figures/papers/iclr26_0011_8iEsrg51Fs_SciNav_A_General_Agent_Framework_for_Scientific/figures/006_Table_3.jpg]]
*Table 3: The effect of different frontier comparators on our agent. “w/ GT" means using ground truth program information in the frontier comparator. We include Rubric-Absolute only as a reference, since it is impractical in real-world settings*

作为参照，使用真实标签信息的 Rubric-Absolute 取得了最高的 SR（21.1%）和 VER（74.5%），但该方法在实际场景中不可用，仅作为理论上界。相对判断在无需任何先验成功指标的前提下，已接近这一上界。

#### 组件贡献分解

表 4 在 40 个至少被一种方法成功求解过的 ScienceAgentBench 任务上进行了组件消融。将初始方案数量从 1 增加到 5 时，成功率从 40.5% 提升至 45.2%，成功节点数从 1.78 增至 2.22。在此基础上引入自我改进（self-improve）模块后，成功率跃升至 57.1%，成功节点数几乎翻倍至 2.69。这表明自我改进机制通过反思性推理识别并修正方案中的具体缺陷，显著放大了搜索空间的探索收益。

![[assets/figures/papers/iclr26_0011_8iEsrg51Fs_SciNav_A_General_Agent_Framework_for_Scientific/figures/007_Table_4.jpg]]
*Table 4: Component ablation study on SciNav. Model: GPT-4o (2024-11-20). The experiment is conducted on 40 tasks of ScienceAgentBench, each of which has been successfully solved at least once by either a baseline agent or SciNav*

#### Top-K 参数选择

图 4 展示了在 30 个随机抽样的 DA-Code 任务上不同 K 值对性能和成本的影响。K=2 时平均性能得分最高，同时成本保持在可控范围内。随着 K 增大，LLM 调用成本单调递增（从 K=1 的约 0.25 增至 K=5 的约 0.6），但性能不再提升甚至下降。因此，所有后续实验均采用 K=2，在性能与计算预算之间取得最优平衡。

### 错误分析

图 3 对 20 个随机选择且未成功求解的 ScienceAgentBench 任务进行了错误分类。84.2% 的失败归因于探索错误（exploration error），即树搜索未能找到或保留包含正确解的轨迹分支。其余失败包括代码生成错误和执行错误。这一分布揭示了一个关键瓶颈：当前系统的核心限制不在于代码编写或调试能力，而在于搜索策略本身未能充分覆盖高潜力解空间。这也为未来工作指明了方向——将相对判断树搜索与外部知识检索或动态工具调用相结合，可能有效降低探索错误率。

### 统计显著性

在 DA-Code 基准上，Mann-Whitney U 检验给出的 p 值为 0.0177（p < 0.05），表明 SciNav 相对于 Self-Debug 的提升具有统计显著性，排除了随机波动导致性能差异的可能性。

### 补充图表

![[assets/figures/papers/iclr26_0011_8iEsrg51Fs_SciNav_A_General_Agent_Framework_for_Scientific/figures/005_Figure_2.jpg]]
*Figure 2: Performance on DA-Code (Huang et al., 2024): (a) by task type, (b) by task difficulty. Model: GPT-4o (2024-11-20)*



## 定位与知识库关联

### 与现有科学智能体的关系

SciNav 定位在一个明确的交叉点上：它继承了科学编程基准的客观可评估性，同时引入了结构化搜索机制来弥补现有智能体在解空间探索上的不足。表 1 横向对比了 SciNav 与七类现有科学智能体在六个维度上的差异。大多数已有系统（如 PaperQA2、OpenScholar、AI Scientist、MLAgentBench）面向全周期、开放式科学发现流程，其评估依赖主观判断或人工审查，缺乏可复现的客观指标。SciNav 则将焦点收窄至科学编程任务，利用 ScienceAgentBench 和 DA-Code 等基准的自动评估能力，实现了严格且可复现的性能度量。

在规划与搜索机制上，SciNav 与现有方案的关键分水岭在于**多计划生成与相对判断驱动的选择策略**。多数科学智能体要么采用单次生成（如 Direct Prompting），要么依赖绝对评分或启发式规则筛选候选方案。SciNav 首次将成对相对判断引入科学编程的树搜索框架，利用其更高的区分力和可靠性来指导分支的保留与剪枝。这一设计直接回应了核心瓶颈：绝对评分在面对复杂科学任务时区分度不足，而随机选择则浪费计算预算。

与工程管道式方案（如 OpenHands、Self-Debug）相比，SciNav 的区别不在于单步代码生成或调试能力，而在于**搜索结构的系统性**。Self-Debug 依赖 Python 解释器反馈进行线性迭代修正，不涉及候选方案的横向比较或回溯。OpenHands 虽支持逐步完成任务，但缺乏针对科学问题的结构化探索策略。SciNav 的 TKCTS 算法通过维护优先队列和 Top-K 选择，在有限预算下实现了可控的回溯与有向搜索。

### 适用边界与泛化条件

SciNav 的设计假设和实验设置界定了其当前适用边界：

1. **任务类型边界**：方法针对的是具有明确功能需求的科学编程任务，即存在可执行的代码方案和可自动验证的输出。这涵盖了 ScienceAgentBench 的数据分析、可视化和模型实现任务，以及 DA-Code 的数据处理与统计分析。对于需要多模态理解、湿实验操作或开放式科学推理的任务，当前框架未提供相应工具支持。

2. **评估信号可用性**：相对判断的有效性依赖于底层 LLM 对代码质量的判别能力。当任务成功标准极为模糊、需要深度领域专业知识、或两个候选方案质量极为接近时，比较器可能给出噪声信号。实验中的错误分析（Figure 3）表明，84.2% 的失败归因于探索错误——即搜索过程未能找到正确的解路径，这暗示比较器在某些情况下未能有效引导搜索。

3. **计算预算约束**：K=2 的选择是基于 30 个 DA-Code 任务上的初步研究得出的性能-成本平衡点（Figure 4）。在更宽松的预算下，增大 K 值可能进一步提升性能，但成本呈单调递增。对于计算资源极度受限的场景，单次生成方案仍具竞争力。

4. **基模型依赖性**：跨模型实验（Table 2）显示 SciNav 在 GPT-4o、Claude-3.7 和 DeepSeek-R1 上均取得一致提升，表明框架对基模型选择具有一定鲁棒性。但附录中的跨模型评估（Table 6）进一步揭示，生成模型与判断模型的组合会影响最终效果——Claude-3.7 生成配合 GPT-4o 验证获得了最高的 VER（72.5），而混合使用 GPT-4o 和 Claude-3.7 进行生成则取得了最高的 SR（19.6）。这说明相对判断的质量与生成能力并非完全解耦。

### 核心局限与失效模式

1. **探索错误主导失败**：Figure 3 的误差分析显示，在 20 个随机抽样的失败任务中，探索错误占 84.2%，远高于代码错误（10.5%）和规划错误（5.3%）。这意味着即使有相对判断引导，搜索过程仍可能在解空间中被困于次优区域。当前框架仅依赖代码执行环境进行验证，缺乏外部知识检索或工具调用能力，这可能是探索能力受限的结构性原因。

2. **相对判断的上限**：Table 3 的消融实验揭示了一个重要参照点——当使用 Ground Truth 信息进行 Rubric-Absolute 评分时，SR 可达 21.1%，显著高于相对判断的 18.6%。这表明相对判断虽优于 LLM-Absolute（16.4%）和随机选择（15.4%），但与理想的上限仍有差距。相对判断的质量受限于 LLM 对任务需求的语义理解和代码质量评估能力，在需要精确数值验证或特定领域规范的任务中可能给出次优排序。

3. **成本与效率权衡**：树搜索结构不可避免增加 LLM 调用次数。Table 2 显示 SciNav 的成本普遍高于 Self-Debug（例如 GPT-4o 2024-11-20 上 $0.91 vs $0.53）。尽管相对判断减少了盲目搜索，但每轮比较仍需多次 LLM 调用。对于简单任务，这种额外开销可能不带来相应的收益。

4. **工具生态的单一性**：当前 SciNav 仅依赖代码执行器作为外部工具。在 ScienceAgentBench 中，部分任务涉及数据文件操作和特定库的使用，但框架未集成网络搜索、知识库查询或多模态工具。这限制了其在更广泛科学任务类型上的泛化能力。

### 开放问题

1. **外部知识整合能否降低探索错误率？** 84.2% 的探索错误提示，仅靠代码执行反馈和内部比较可能不足以有效导航复杂解空间。将相对判断树搜索与外部知识检索（如文献数据库、代码仓库搜索）或动态工具调用相结合，是否能够为搜索提供更丰富的启发式信号，是一个值得探索的方向。

2. **相对判断在高度歧义任务中的可靠性边界**：当前实验在具有明确成功标准的数据集上进行。在真实科学发现场景中，任务目标往往模糊且成功标准未知。相对判断的可靠性如何随任务歧义度的增加而变化？是否可以通过引入不确定性量化或多轮共识机制来提升鲁棒性？

3. **测试时计算扩展的潜力**：SciNav 本质上是一种测试时计算扩展方法——通过增加搜索预算来提升解质量。能否将这一思想拓展至更长的推理链（如多步科学推理）和多模态科学问题（如实验设计、图表分析）？这需要重新思考搜索树的表示方式和比较器的评估维度。

4. **生成与判断的解耦优化**：Table 6 的跨模型实验暗示，最优的生成模型和判断模型可能不同。是否存在系统性的方法来为特定任务选择最优的生成-判断模型组合？能否通过训练专门的比较器模型来突破通用 LLM 在相对判断上的性能上限？



## 原文 PDF

![[paperPDFs/ICLR_2026/SciNav_A_General_Agent_Framework_for_Scientific_Coding_Tasks.pdf]]
