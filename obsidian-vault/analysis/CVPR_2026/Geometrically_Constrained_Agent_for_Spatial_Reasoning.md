---
title: Geometrically-Constrained Agent for Spatial Reasoning
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Geometrically_Constrained_Agent_for_Spatial_Reasoning.pdf
project_link: "https://gca-spatial-reasoning.github.io"
code_link: null
aliases:
- GC
- GCASR
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: Geometrically-Constrained
primary_logic: Geometrically-Constrained
claims:
- Geometrically-Constrained
---

# Geometrically-Constrained Agent for Spatial Reasoning

> [!tip] 核心洞察
> Geometrically-Constrained

| 字段 | 内容 |
|------|------|
| 中文题名 | Geometrically-Constrained Agent for Spatial Reasoning |
| 英文题名 | Geometrically-Constrained Agent for Spatial Reasoning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.22659) · [Project](https://gca-spatial-reasoning.github.io) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method |  |
| Dataset | MMSI-Bench, MindCube, SpatialBench, CV-Bench |

> [!tip] 效果简介
> 本笔记的既有实验指标、对比结果与适用边界见“实验与关键发现”；本轮仅统一结构，不改写证据。

## 概要

视觉语言模型（VLM）在空间推理任务中长期面临一个根本性瓶颈：**语义-几何鸿沟（Semantic-Geometric Gap）**。当视觉信息被转换为文本空间时，精确的几何细节——如方向、距离、物体朝向——不可避免地丢失，导致VLM产生错误的推理或无约束的规划幻觉（Figure 1a）。

针对这一问题，本文提出 **GCA（Geometrically-Constrained Agent）**，一种无需训练的智能体范式。其核心思想是引入一个形式化的**任务约束** $\mathcal{C}_{\mathrm{task}}$，作为语义与几何之间的确定性桥梁。GCA将VLM的角色解耦为两个阶段：**任务形式化（Task Formalization）**——由VLM将模糊的自然语言查询翻译为可验证的形式约束；**约束几何计算（Constrained Geometric Computation）**——在不可变约束下，通过知识增强的代码生成与工具编排执行精确的几何计算（Figure 1b）。

在多个空间推理基准上的实验表明，GCA取得了显著的性能提升：以 **Gemini-2.5-Pro** 为基座时，平均准确率达到 **65.1%**，较基线的58.5%提升 **+6.6个百分点**（Table 1, Avg列）。更广泛地，GCA在多个基础VLM上平均带来约 **37%** 的相对性能增益，验证了该范式的通用性与有效性。



### 语义-几何鸿沟：VLM 空间推理的根本瓶颈

视觉语言模型（VLM）在一般视觉理解任务上取得了显著进展，但在需要精确空间推理的场景中暴露出系统性缺陷。其核心问题在于 **语义-几何鸿沟（Semantic-Geometric Gap）**：当视觉信息被转换为文本空间中的语义表征时，精确的几何细节（如相对位置、朝向、距离等）不可避免地丢失。VLM 在语义空间中进行的推理因此缺乏几何约束，导致规划无约束、推理结果不可靠。

这一鸿沟的存在使得现有方法面临两难困境：纯 VLM 的链式思维（CoT）推理缺乏几何准确性，而传统的基于状态的符号推理方法又难以表达视点、参考系等复杂空间概念。问题的关键在于缺少一种能够将语义理解与几何计算有效桥接的机制。

### 现有方法的缺口

当前空间推理方法主要分为两类：

1. **端到端 VLM 推理**：直接让 VLM 在语义空间中完成推理，但几何信息在视觉到文本的转换过程中被严重压缩，导致推理过程缺乏必要的空间约束。
2. **工具增强方法**：引入外部几何计算工具，但工具的调用本身缺乏形式化的任务约束来指导。VLM 在何时调用工具、如何解释工具反馈等问题上仍然依赖不可靠的语义推理。

这两种方法都未能解决一个根本问题：**在推理开始之前，需要先明确“要解什么”，再决定“怎么解”**。缺乏形式化的任务约束，VLM 的推理始终在损失几何信息的语义空间中进行。

### 本文动机：几何约束代理范式

基于上述分析，本文提出 **几何约束代理（Geometrically-Constrained Agent, GCA）**——一种无需训练的代理范式。其核心动机是引入一个 **形式化任务约束 $\mathcal{C}_{\mathrm{task}}$**，将 VLM 的角色解耦为两个阶段：

1. **任务形式化（Task Formalization）**：VLM 作为语义分析器，将模糊的空间推理查询转化为形式化的 $\mathcal{C}_{\mathrm{task}}$，明确定义参考系和求解目标。
2. **约束几何计算（Constrained Geometric Computation）**：VLM 作为任务求解器，在 $\mathcal{C}_{\mathrm{task}}$ 的指导下管理外部几何工具，完成精确的几何计算。

这一解耦策略的本质在于：**通过形式化约束将几何推理从 VLM 的损失语义空间中剥离出来，交给精确的几何工具完成，同时保留 VLM 在语义理解上的优势**。$\mathcal{C}_{\mathrm{task}}$ 作为语义与几何之间的确定性桥梁，需要满足三个条件：语法足够丰富以定义视点等复杂空间概念、语义足够清晰以消除歧义、几何足够完备以支持精确计算。



## 核心方法与创新机理

GCA 的核心创新在于通过一个形式化任务约束 $\mathcal{C}_{\mathrm{task}}$ 将空间推理中语义与几何之间的鸿沟进行了解耦与桥接。这一设计并非简单地增加推理步骤或工具调用，而是从根本上改变了 VLM 在推理过程中的角色定位与信息流动方式。

**从“端到端猜测”到“先定义，后求解”的范式转变。** 传统 VLM 在空间推理任务中直接面对模糊的自然语言查询和视觉输入，试图一步到位地给出答案。这一过程极易丢失关键的几何细节，导致推理失准或幻觉（Figure 1a）。GCA 将这一过程强制拆分为两个阶段：**任务形式化**（$\mathcal{F}_{\mathrm{formalize}}$）与**约束几何计算**（$\mathcal{F}_{\mathrm{compute}}$）。在形式化阶段，VLM 作为“语义分析师”，将查询 $q$ 和视觉信息 $v$ 翻译为一个确定的、可验证的形式化任务约束 $\mathcal{C}_{\mathrm{task}}$；在计算阶段，VLM 的角色切换为“约束任务求解器”，在 $\mathcal{C}_{\mathrm{task}}$ 的刚性约束下进行几何推理与工具调度。这一范式转变的核心效果在于：VLM 必须首先明确“要解什么”，然后才能决定“怎么解”，从而将几何推理从不可靠的语义空间中剥离出来，交由确定性的几何工具链完成。

**$\mathcal{C}_{\mathrm{task}}$ 作为语义-几何的确定性桥梁。** $\mathcal{C}_{\mathrm{task}}$ 被定义为一个元组 $\mathcal{C}_{\mathrm{task}} = (\mathcal{C}_{\mathcal{R}}, \mathcal{C}_{\mathcal{O}})$，包含两个不可协商的子约束：**参考系约束**（$\mathcal{C}_{\mathcal{R}}$）和**目标约束**（$\mathcal{C}_{\mathcal{O}}$）。$\mathcal{C}_{\mathcal{R}}$ 通过点、对象、向量等几何基元显式锚定空间推理的坐标系（Figure 3），解决了“从谁的视角看”这一核心歧义；$\mathcal{C}_{\mathcal{O}}$ 则明确指定了需要计算或判定的空间关系。这一设计使得原本隐含在自然语言中的空间意图被转化为结构化的几何描述，成为连接 VLM 语义理解与底层几何计算的唯一接口。消融实验（Figure 4）证实，仅靠思维链（CoT）或无约束的工具调用无法达到同等效果，而引入形式化约束后性能大幅跃升，表明 $\mathcal{C}_{\mathrm{task}}$ 是性能提升的关键杠杆。

**知识增强的代码生成与工具反馈闭环。** 在计算阶段，GCA 并未让 VLM 自由生成几何计算代码，而是维护了一个经过验证的基础几何公式库。系统根据 $\mathcal{C}_{\mathrm{task}}$ 中绑定变量的数据类型，自动检索相关公式集合并注入 VLM 的代码生成过程（知识增强代码生成，KACG）。同时，VLM 负责管理工具执行后的反馈，对歧义或异常结果进行闭环修正。Table 2 的消融表明，KACG 和反馈机制各自贡献了显著的性能增益，二者叠加构成了 GCA 在计算阶段的完整能力。

**与现有方法的本质差异。** 与 ReAct 等通用智能体框架不同，GCA 并非简单地让 VLM 在思考-行动-观察循环中自由探索，而是通过 $\mathcal{C}_{\mathrm{task}}$ 对探索空间进行了刚性约束。与依赖微调或大量示例的方法相比，GCA 是一种免训练范式，其泛化能力来源于形式化约束本身的几何完备性，而非模型对特定数据分布的拟合。Figure 5 显示，GCA 在不同基础 VLM 上平均带来约 37% 的相对性能提升，验证了这一范式的模型无关性。



GCA 是一个**免训练的智能体范式**，专为几何约束下的空间推理设计。其核心思想是通过引入一个形式化任务约束 $\mathcal{C}_{\mathrm{task}}$，将视觉语言模型（VLM）的推理过程解耦为两个阶段，从而弥合语义理解与几何计算之间的鸿沟（Figure 1）。

![[assets/figures/papers/paper_list_l2638_https_arxiv_org_abs_2511_22659/figures/001_Figure_1.jpg]]
*Figure 1: Overview. (a) Semantic-Geometric Gap. The geometric details required for spatial reasoning are lost when translating visual information into textual space, leading to VLM’s flawed reasoning or unconstrained planning. (b) Geometrically-Constrained Spatial Reasoning. We propose a formal task constraint that serves as a deterministic bridge between semantics and geometry in spatial reasoning*

### 两阶段流水线

GCA 的整体范式如 Figure 2 所示，包含以下两个关键阶段：

![[assets/figures/papers/paper_list_l2638_https_arxiv_org_abs_2511_22659/figures/002_Figure_2.jpg]]
*Figure 2: Overall Paradigm of GCA. Given a spatial reasoning query, our GCA leverages a geometrically-constrained reasoning strategy centered on the formal task constraint*

**阶段一：任务形式化（Task Formalization）**  
在此阶段，VLM 扮演**语义分析师**的角色，将模糊的自然语言查询 $q$ 和视觉信息 $v$ 翻译为一个形式化、可验证的任务约束 $\mathcal{C}_{\mathrm{task}}$。该过程可表示为：
$$\mathcal{C}_{\mathrm{task}} = \mathcal{F}_{\mathrm{formalize}}(q, v)$$

$\mathcal{C}_{\mathrm{task}}$ 被定义为一个元组，包含两个不可协商的子约束：
- **参考系约束** $\mathcal{C}_{\mathcal{R}}$：定义了空间推理所依据的坐标系，可基于对象、观察者或环境等几何原语进行锚定（Figure 3）。
- **目标约束** $\mathcal{C}_{\mathcal{O}}$：明确指定需要求解的空间关系或几何目标。

形式化任务约束必须满足三个条件：语法上足够丰富以定义复杂空间概念（如视点）、语义上足够清晰以消除歧义、几何上足够严谨以支持精确计算。

**阶段二：约束几何计算（Constrained Geometric Computation）**  
一旦 $\mathcal{C}_{\mathrm{task}}$ 确立，VLM 的角色转变为**受约束的任务求解器**。此阶段以 ReAct 风格框架运行，将 $\mathcal{C}_{\mathrm{task}}$ 作为不可变约束：
$$r_t = \mathcal{F}_{\mathrm{compute}}(\mathcal{C}_{\mathrm{task}}, v, \mathcal{T}, r_{t-1})$$
其中 $\mathcal{T}$ 表示可调用的工具集，$r_{t-1}$ 为历史响应。

该阶段的关键机制是**知识增强的代码生成策略**：系统维护一个预置的、经过验证的几何公式库。根据约束中绑定变量的数据类型，自动检索相关公式集合并注入到代码生成过程中。这使得智能体能够通过调用现成的视觉基础模型工具来获取必要的几何数据（如目标质心、朝向等），并执行精确的几何计算。

### 输入输出流

- **输入**：自然语言空间推理查询 $q$ 与对应的视觉输入 $v$（图像或三维场景）。
- **中间表示**：形式化任务约束 $\mathcal{C}_{\mathrm{task}} = (\mathcal{C}_{\mathcal{R}}, \mathcal{C}_{\mathcal{O}})$，作为语义与几何之间的确定性桥梁。
- **输出**：空间推理的最终答案 $r_t$，由阶段二通过受约束的代码生成与工具编排产生。

与传统的 ReAct 策略 $r_t = \mathcal{A}(q, v, \mathcal{T}, r_{t-1})$ 相比，GCA 的关键区别在于强制 VLM 先确定“求解什么”（通过 $\mathcal{C}_{\mathrm{task}}$ 形式化），再决定“如何求解”（通过受约束的几何计算），从而避免了纯文本推理中的几何信息丢失问题。



GCA 的核心在于引入一个形式化的任务约束 $\mathcal{C}_{\mathrm{task}}$，作为语义理解与几何计算之间的确定性桥梁。整个推理过程被解耦为两个阶段，VLM 在其中的角色随之发生转变。

### 语义分析阶段：任务形式化

在 $\mathcal{F}_{\mathrm{formalize}}$ 阶段，VLM 充当**语义分析师**，将模糊的查询 $q$ 和视觉信息 $v$ 翻译为一个形式化、可验证的任务约束 $\mathcal{C}_{\mathrm{task}}$。这一约束必须满足三个条件：

1. **语法足够丰富**，能够定义复杂空间概念（如视角），这些概念是传统基于状态的体系所无法表达的；
2. **语义足够清晰**，使 VLM 能准确理解并生成；
3. **几何上足够严谨**，可直接由几何工具执行。

形式化后的任务约束被定义为一个元组：

$$\mathcal{C}_{\mathrm{task}} = (\mathcal{C}_{\mathcal{R}}, \mathcal{C}_{\mathcal{O}})$$

其中：
- $\mathcal{C}_{\mathcal{R}}$ 为**参考系约束**（Reference Frame Constraint），定义了推理所依据的坐标系与锚定方式（例如基于特定物体、基于观测者视角等）；
- $\mathcal{C}_{\mathcal{O}}$ 为**目标约束**（Objective Constraint），明确规定了需要求解的空间关系或几何目标。

### 计算执行阶段：约束化几何计算

一旦 $\mathcal{C}_{\mathrm{task}}$ 确立，VLM 的角色转变为**受约束的任务求解器**。$\mathcal{F}_{\mathrm{compute}}$ 阶段采用 ReAct 风格的框架运行，将 $\mathcal{C}_{\mathrm{task}}$ 作为不可变约束来消费：

$$r_t = \mathcal{F}_{\mathrm{compute}}(\mathcal{C}_{\mathrm{task}}, \mathcal{T}, r_{t-1})$$

其中 $\mathcal{T}$ 表示可调用的工具集，$r_{t-1}$ 为历史响应。

该阶段的核心机制包括：

- **知识增强的代码生成（KACG）**：系统维护一个预置的、经过验证的几何公式库。根据绑定变量的数据类型，自动检索相关公式集合并注入代码生成过程，避免 VLM 凭空编造几何计算逻辑。
- **工具反馈管理**：VLM 负责协调一系列现成的基础模型工具，处理工具返回的反馈信息并解决歧义。

### 两阶段形式化总览

整体范式可概括为以下两步：

$$\mathcal{C}_{\mathrm{task}} = \mathcal{F}_{\mathrm{formalize}}(\boldsymbol{q}, \boldsymbol{v})$$

$$r_t = \mathcal{F}_{\mathrm{compute}}(\mathcal{C}_{\mathrm{task}}, \mathcal{T}, r_{t-1})$$

这一设计的核心洞察在于：通过强制 VLM 先确立“求解什么”（$\mathcal{C}_{\mathrm{task}}$），再决定“如何求解”（$\mathcal{F}_{\mathrm{compute}}$），从根本上缩小了语义理解与几何计算之间的鸿沟。整个框架无需模型微调，以训练无关的智能体范式运行。

### 补充图表

![[assets/figures/papers/paper_list_l2638_https_arxiv_org_abs_2511_22659/figures/003_Figure_3.jpg]]
*Figure 3: Reference Frame. Here*



## 实验与关键发现

### 整体性能：GCA 在空间推理基准上的主结果

Table 1 汇总了 GCA 在多个空间推理基准上与现有方法的对比。以 **Gemini-2.5-Pro** 作为最强 VLM 基线（平均准确率 58.5%），GCA 取得了 **65.1%** 的平均准确率，绝对提升 **+6.6 个百分点**。这一增益在各项基准上表现一致：

![[assets/figures/papers/paper_list_l2638_https_arxiv_org_abs_2511_22659/figures/004_Table_1.jpg]]
*Table 1: Experimental Results on Several Spatial Reasoning Benchmarks. The best and second best results are shown in bold and underlined, respectively. “Avg.” denotes the average of overall accuracy across all benchmarks. More details about these benchmarks’ subcategory (e.g., “PR.”) are provided in Appendix*

- 在 **MMSI-Bench** 上，GCA 的整体准确率达到 47.6%，相较 Gemini-2.5-Pro 实现了约 28% 的相对提升；其中 PR（Perspective Reasoning）子类得分为 52.8。
- 在 **MindCube-tiny** 上，GCA 以 64.2% 的准确率显著超越所有基线方法。

值得注意的是，GCA 是一种 **training-free** 的 agentic 范式，无需对 VLM 进行任何微调。其性能增益完全来源于推理流程的结构性改进——将 VLM 的角色解耦为语义分析（形式化阶段）与约束几何计算（求解阶段），并通过形式化任务约束 $\mathcal{C}_{\mathrm{task}}$ 桥接语义与几何。

### 消融研究：各组件的贡献

#### 形式化策略的影响

Figure 4 对比了不同形式化策略的效果。基线方法包括：(1) 纯 CoT 推理（无工具集成）；(2) 无约束工具集成（Tool Uncon.）；(3) 通过 prompt 引导的工具集成（Tool Prompt）。GCA 的形式化约束策略在所有设置下均取得最优，验证了“先确立解什么，再决定怎么解”这一设计原则的有效性。引入 $\mathcal{C}_{\mathrm{task}}$ 迫使 VLM 在调用几何工具前明确参考系与目标约束，从而避免无约束推理中的语义漂移。

![[assets/figures/papers/paper_list_l2638_https_arxiv_org_abs_2511_22659/figures/006_Figure_4.jpg]]
*Figure 4: Ablation Study on Formalization. We compare our method in against several baselines: (1) no tool integration (“Baseline (CoT-Only)”), (2) unconstrained tool integration with (“Tool (Prompt)”) or without (“Tool (Uncon.)”) hints, (3) using a humanannotated*

#### 各模块的增量贡献

Table 2 展示了 GCA 内部模块的消融结果。关键发现：

![[assets/figures/papers/paper_list_l2638_https_arxiv_org_abs_2511_22659/figures/008_Table_2.jpg]]
*Table 2: Ablation Study on Each Component in GCA. Here, “KACG” denotes applying knowledge-augmented code generation, and “Feedback” denotes applying the VLM to manage tool feedback and resolve ambiguity*

- **知识增强代码生成（KACG）**：通过维护一个经过验证的几何公式库，根据绑定变量的数据类型自动检索相关公式，避免了 VLM 凭空生成错误几何代码的风险。移除 KACG 导致性能显著下降。
- **工具反馈管理（Feedback）**：让 VLM 管理工具返回的反馈并消解歧义，进一步提升了系统的鲁棒性。

Table 3 进一步消融了任务约束 $\mathcal{C}_{\mathrm{task}}$ 本身，确认参考系约束 $\mathcal{C}_{\mathcal{R}}$ 与目标约束 $\mathcal{C}_{\mathcal{O}}$ 各自对最终性能都有不可替代的贡献。

![[assets/figures/papers/paper_list_l2638_https_arxiv_org_abs_2511_22659/figures/009_Table_3.jpg]]
*Table 3: Ablation Study on Task Constraint*

#### 跨 VLM 的泛化性

Figure 5 展示了 GCA 在不同基础 VLM 上的泛化能力。在所有测试的 VLM 上，GCA 平均带来约 **37% 的相对性能提升**。这表明 GCA 的形式化-计算解耦范式不依赖于特定 VLM 的能力边界，而是作为一种通用的推理增强策略发挥作用。

![[assets/figures/papers/paper_list_l2638_https_arxiv_org_abs_2511_22659/figures/005_Figure_5.jpg]]
*Figure 5: Ablation Study on Generalizability across Different VLMs. Our GCA achieves an average of 37% relative performance improvement across all tested foundation VLMs*

### 失败模式与局限

尽管 GCA 在整体上表现优异，其性能仍受限于以下因素：

1. **形式化阶段的错误传播**：如果 $\mathcal{F}_{\mathrm{formalize}}$ 阶段生成的 $\mathcal{C}_{\mathrm{task}}$ 本身存在语义理解偏差（例如选错参考对象或误解空间关系），后续的约束计算将基于错误的前提进行，且系统缺乏自我纠错机制。这一瓶颈在需要复杂视角推理（如 MMSI-Bench 的 PR 子类）时尤为突出。
2. **度量尺度估计的困难**：如 Figure 13 的 Case Study #6 所示，涉及绝对度量尺度（metric-scale）的空间估计任务仍然是挑战。VLM 从视觉信息中提取精确的深度或距离信息的能力有限，而几何工具库目前主要处理相对几何关系，无法弥补这一感知层面的不足。
3. **工具库的覆盖范围**：当前固定的几何公式库覆盖了基本几何运算，但对于更复杂的空间推理场景（如动态场景、非刚性变换），可能需要扩展工具集或引入更灵活的代码生成策略。

![[assets/figures/papers/paper_list_l2638_https_arxiv_org_abs_2511_22659/figures/016_Figure_13.jpg]]
*Figure 13: Case Study #6. Metric-scale estimation*

### 关键图表结论

- **Table 1**：GCA 在多个空间推理基准上建立了新的 state-of-the-art，以 training-free 的方式超越强 VLM 基线。
- **Figure 4 & Table 2**：形式化约束与知识增强代码生成是 GCA 性能增益的核心来源，二者缺一不可。
- **Figure 5**：GCA 的范式对不同 VLM 具有广泛适用性，平均相对提升达 37%，验证了其作为通用空间推理增强策略的潜力。

### 补充图表

![[assets/figures/papers/paper_list_l2638_https_arxiv_org_abs_2511_22659/figures/007_Figure_6.jpg]]
*Figure 6: Error Attribution and Failure Cases. We provide a detailed error attribution analysis to identify the main failure modes within the VLM’s reasoning trajectory*



## 定位与知识库关联

### 1. 与基线方法的关系

GCA 的核心贡献在于提出了一种**训练无关的智能体范式**，将空间推理中的语义理解与几何计算进行了解耦。这一设计直接回应了当前视觉-语言模型（VLM）在空间推理任务中面临的“语义-几何鸿沟”（Semantic-Geometric Gap）问题。

在基线对比中，GCA 与两类方法形成了明确的参照关系：

**（1）纯 VLM 推理基线**

最强的纯 VLM 基线为 **Gemini-2.5-Pro**，其在所有基准测试上的平均准确率为 58.5%。GCA 在同一设定下取得了 65.1% 的平均准确率，实现了 **+6.6 个百分点的绝对提升**（Table 1, Avg 列）。在更具挑战性的 MMSI-Bench 上，GCA 以 47.6% 的总体准确率超越了 Gemini-2.5-Pro，相对提升幅度达到约 28%。这一对比揭示了纯 VLM 在将视觉信息转换为文本空间时，几何细节的丢失会导致推理缺陷或不受约束的规划，而 GCA 通过形式化任务约束（$\mathcal{C}_{\mathrm{task}}$）强制建立了语义到几何的确定性桥梁。

**（2）工具增强基线**

论文在消融实验中系统比较了无约束工具集成方案（Table 1 中各类 Tool-based 方法），包括带提示（Tool Prompt）和不带提示（Tool Uncon.）的变体。结果表明，仅将工具交给 VLM 而不施加几何约束，其性能远低于 GCA。这验证了 GCA 的核心洞察：**关键在于“先确定求解什么，再确定如何求解”**——即通过 $\mathcal{F}_{\mathrm{formalize}}$ 阶段生成形式化任务约束，再在 $\mathcal{F}_{\mathrm{compute}}$ 阶段进行受约束的几何计算。

GCA 的范式可视为对 ReAct 框架的几何约束增强。传统 ReAct 策略 $r_t = \mathcal{A}(q, v, \mathcal{T}, r_{t-1})$ 中，智能体的行动空间未被结构化约束；而 GCA 将其重构为两阶段过程 $\mathcal{C}_{\mathrm{task}} = \mathcal{F}_{\mathrm{formalize}}(\boldsymbol{q}, \boldsymbol{v}), \quad r_t = \mathcal{F}_{\mathrm{compute}}(\mathcal{C}_{\mathrm{task}}, \mathcal{T}, r_{t-1})$，使 $\mathcal{C}_{\mathrm{task}}$ 成为不可变的约束条件，从根本上限制了 VLM 的推理漂移。

### 2. 适用边界

GCA 的设计依赖于以下前提条件，这些条件同时定义了其适用边界：

- **形式化可行性**：任务必须能被表达为参考系约束（$\mathcal{C}_{\mathcal{R}}$）与目标约束（$\mathcal{C}_{\mathcal{O}}$）的元组 $\mathcal{C}_{\mathrm{task}} = (\mathcal{C}_{\mathcal{R}}, \mathcal{C}_{\mathcal{O}})$。参考系约束要求 VLM 能从查询中识别出锚定几何基元（如物体的中心点、朝向向量等），这限制了其在极弱视觉信号或高度抽象空间关系场景下的适用性。
- **工具生态依赖**：$\mathcal{F}_{\mathrm{compute}}$ 阶段依赖一套现成的基础模型工具（包括分割、深度估计等）来获取几何数据。工具的可用性和精度直接影响 GCA 的性能上限。
- **知识库覆盖**：知识增强代码生成（KACG）策略依赖预置的几何公式库，该库按绑定变量的数据类型自动检索公式。当任务所需的几何操作超出公式库覆盖范围时，系统将回退到 VLM 自行生成代码，此时约束的有效性可能减弱。
- **VLM 语义能力**：虽然 GCA 将几何计算外包给工具，但 $\mathcal{F}_{\mathrm{formalize}}$ 阶段仍完全依赖 VLM 的语义理解能力来生成 $\mathcal{C}_{\mathrm{task}}$。若 VLM 无法正确识别查询中的空间语义（如误解“左侧”的参照对象），错误将在后续阶段被传播和放大。

### 3. 局限与开放问题

**已知局限（需人工核实具体细节）：**

论文在错误归因分析（Figure 6）中识别了 VLM 推理轨迹中的主要失败模式，但分析材料中未提供具体的失败类别分布数据。从方法设计推断，潜在局限包括：

1. **形式化阶段的错误传播**：$\mathcal{C}_{\mathrm{task}}$ 的质量完全取决于 VLM 的语义分析能力。一旦参考系约束（$\mathcal{C}_{\mathcal{R}}$）中锚定的对象或方向出错，后续的几何计算将在错误的坐标系下进行，导致系统性失败。
2. **工具反馈的模糊性处理**：$\mathcal{F}_{\mathrm{compute}}$ 阶段中，VLM 需要管理工具反馈并解决歧义。当工具返回的几何数据存在噪声或不一致时（如分割掩码边界模糊），VLM 的约束求解能力可能不足。
3. **跨 VLM 泛化的上限**：尽管 GCA 在多个基础 VLM 上平均实现了约 37% 的相对性能提升（Figure 5），但绝对性能仍受限于底层 VLM 的语义能力。对于语义理解极弱的 VLM，形式化阶段可能成为瓶颈。

**开放问题：**

1. **形式化约束的自动化验证**：当前 $\mathcal{C}_{\mathrm{task}}$ 的正确性缺乏自动验证机制。是否可以利用几何一致性检查（如参考系定义的内部自洽性）来自动检测和修正形式化错误？
2. **动态场景与时间维度的扩展**：GCA 当前处理的是静态空间关系。对于涉及动态物体运动、视角连续变化的场景，参考系约束（$\mathcal{C}_{\mathcal{R}}$）需要引入时间维度，这超出了现有框架的覆盖范围。
3. **公式库的自动扩展**：知识增强代码生成依赖预置公式库。是否可以通过从成功推理轨迹中自动挖掘新的几何关系模式来动态扩展公式库，从而提升系统的覆盖面和鲁棒性？
4. **与训练方法的协同**：GCA 是训练无关范式，但其形式化-计算两阶段结构是否可以作为训练信号，用于微调 VLM 以提升其空间语义分析能力？这可能是连接 agentic 方法与模型能力提升的潜在方向。



## 原文 PDF

![[paperPDFs/CVPR_2026/Geometrically_Constrained_Agent_for_Spatial_Reasoning.pdf]]
