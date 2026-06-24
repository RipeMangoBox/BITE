---
title: "Verifying Chain-of-Thought Reasoning via Its Computational Graph"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Verifying_Chain_of_Thought_Reasoning_via_Its_Computational_Graph.pdf
openreview_forum_id: CxiNICq0Rr
aliases:
- CBRVC
- VCTRICG
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "操纵transcoder中特定语义特征的激活值（抑制或增强）可直接改变模型的计算路径并纠正错误推理。"
primary_logic: "错误推理步骤的归因图具有与正确步骤不同的结构指纹，且这些指纹高度领域特定，可用于检测和诊断推理失败。"
claims:
- "CRV在所有三个数据集和多个评估指标上显著超越所有黑盒与灰盒基线方法，证明计算图结构指纹包含强烈的错误信号。"
- "跨域泛化实验显示错误指纹高度领域特定：仅在源任务上训练的CRV在其他任务上性能大幅下降，表明不同推理任务的计算失败模式各异。"
- "通过forward hook抑制或增强单个transcoder特征可以成功纠正模型的错误推理路径，表明CRV识别的特征与错误之间存在因果关系。"
- "Synthetic (Boolean) 上 AUROC = 75.87"
---

# Verifying Chain-of-Thought Reasoning via Its Computational Graph

> [!tip] 核心洞察
> 错误推理步骤的归因图具有与正确步骤不同的结构指纹，且这些指纹高度领域特定，可用于检测和诊断推理失败。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 通过计算图验证思维链推理 |
| 英文题名 | Verifying Chain-of-Thought Reasoning via Its Computational Graph |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=CxiNICq0Rr) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | Circuit-based Reasoning Verification (CRV) |
| Dataset | Synthetic (Boolean), Synthetic (Arithmetic), GSM8K |

> [!tip] 效果简介
> - Synthetic (Boolean) 上，AUROC 为 75.87，对比 58.81 (MaxProb)，变化 +17.06。
> - Synthetic (Arithmetic) 上，AUROC 为 92.47，对比 76.45 (Energy)，变化 +16.02。
> - GSM8K 上，AUROC 为 70.17，对比 62.55 (Energy)，变化 +7.62。

## 概述

### 问题背景

大语言模型在数学推理、符号操作等任务中已展现出通过思维链（Chain-of-Thought, CoT）进行逐步推理的能力，但其推理过程仍频繁出错。现有的验证方法主要分为两类：**黑盒方法**（如基于概率、困惑度、熵等输出信号）和**灰盒方法**（利用中间层表征训练探针分类器）。这些方法的共同瓶颈在于：它们无法解释推理失败的**计算原因**，缺乏对模型内部算法执行过程的深入洞察。当模型在某一步出错时，我们不仅需要知道“这一步错了”，更需要理解“模型的计算路径在何处发生了偏离”。

### 核心思路

本文提出了一种**白盒验证方法**——基于电路的推理验证（Circuit-based Reasoning Verification, CRV）。其核心洞察是：**错误推理步骤的归因图具有与正确步骤不同的结构指纹**，且这些指纹高度领域特定，可用于检测和诊断推理失败。

CRV将模型的推理过程视为可解释的**计算图**：首先将LLM中的MLP模块替换为稀疏激活的transcoder，使模型内部特征变得可解释；然后对每个推理步骤构建稀疏有向归因图，追踪从输入token经活跃特征到最终logit的因果流；最后从图中提取全局统计、节点影响和拓扑路径三个层次的结构指纹，训练诊断分类器预测步骤正确性。

### 方法定位

CRV在方法谱系中占据独特位置：

- **相对于黑盒方法**（MaxProb、PPL、Entropy、Energy等）：CRV深入模型内部计算结构，而非仅依赖输出概率分布。在合成算术任务上，CRV的AUROC达到92.47%，远超最强黑盒基线Energy的76.45%（+16.02个百分点）。
- **相对于灰盒方法**（CoE-R、CoE-C、CoT-Kinetics、线性探针等）：灰盒方法虽利用中间表征，但仅训练探针分类器而缺乏对计算路径的因果分析。CRV通过归因图揭示了错误的**结构特征**，在FPR@95指标上优势尤为显著：算术任务上CRV仅37.09%，而CoE-C高达63.33%。
- **相对于电路分析工具**：CRV将原本用于科学理解的电路分析方法（如Dunefsky et al., 2025的贪心路径搜索）转化为实用的验证工具，实现了从“事后解释”到“实时诊断”的跨越。

### 关键结果

CRV在三个数据集上均显著超越所有基线方法（Table 1）：

- **合成布尔任务**：AUROC 75.87%（最强基线MaxProb 58.81%，提升+17.06）
- **合成算术任务**：AUROC 92.47%（最强基线Energy 76.45%，提升+16.02）；AUPR 28.92%（基线仅5.59%）
- **GSM8K数学推理**：AUROC 70.17%（最强基线Energy 62.55%，提升+7.62）；AUPR 14.3%（基线最高10.80%）

消融实验揭示了关键机制：

- **节点影响和激活特征是最关键的信号**：移除该特征族后，算术任务AUROC从92.47降至88.31，FPR@95增加超过12个百分点。
- **错误指纹高度领域特定**：仅在算术任务上训练的CRV在GSM8K上零样本AUROC仅57.04，表明不同推理任务的计算失败模式各异；但在组合数据集上训练可恢复性能（算术AUROC 90.51）。
- **特征与错误之间存在因果关系**：通过forward hook抑制或增强单个transcoder特征，可直接纠正模型的错误推理路径（Table 4, Table 19），证明CRV识别的结构指纹不仅是相关性信号，更是因果性指标。

### 局限与展望

CRV目前更适合作为科学分析工具而非可扩展的生产级验证器，主要受限于：transcoder训练和归因图构建的高计算成本；特征集尚未充分利用个体特征的语义信息；仅在Llama 3.1 8B Instruct单一模型上验证。未来方向包括：探索结构指纹在MoE架构和大规模模型上的泛化性；研究指令微调对底层特征空间的影响；寻找超越领域特定的普适计算失败模式；开发直接在解耦特征语义上操作的神经符号验证器。

## 背景与动机

大语言模型（LLM）在复杂推理任务上的突破，很大程度上得益于思维链（Chain-of-Thought, CoT）提示技术，它通过生成显式的中间推理步骤来引导模型得出最终答案。然而，CoT推理并非总是可靠——模型可能在逻辑推导、数值计算或符号操作中引入隐蔽的错误。这些错误一旦发生，往往会沿着推理链条传播，最终导致错误结论。因此，**自动验证CoT推理步骤的正确性**成为提升LLM可信度的关键挑战。

现有验证方法大致可分为两类：**黑盒方法**通过分析模型输出的概率分布来评估置信度，如最大概率（MaxProb）、困惑度（PPL）、熵（Entropy）和能量分数（Energy）；**灰盒方法**则进一步利用内部表征或注意力信息，如CoE（Wang et al., 2025a）、CoT-Kinetics（Bi et al., 2025）以及线性探针（LR/MLP Probe）。这些方法的共同局限在于：它们只能给出一个“是否错误”的判断信号，却**无法解释推理失败的计算原因**——即模型在执行推理时，其内部的算法路径究竟在何处、因何而偏离了正确轨迹。

这一瓶颈的根源在于，现有方法缺乏对模型**潜在算法执行过程**的深入洞察。LLM的推理本质上是一种计算——模型通过其参数化的电路对输入进行变换，逐步构建出中间结果。如果我们将CoT步骤视为这一计算过程的“执行痕迹”，那么正确步骤与错误步骤应当对应着不同的电路激活模式。然而，标准LLM的密集MLP层使得这种电路分析几乎不可能：成千上万个神经元以密集连接的方式混合信息，任何单一激活都缺乏可解释的语义。

本文的核心动机正是突破这一可解释性壁垒。我们提出**基于电路推理验证（Circuit-based Reasoning Verification, CRV）**，一种白盒验证框架。其核心假设是：**正确CoT步骤的归因图（attribution graph）具有与错误步骤截然不同的结构指纹**。通过将LLM的MLP模块替换为稀疏激活的transcoder，我们获得了一个可解释的替代模型；在此基础上，我们为每个推理步骤构建稀疏有向归因图，追踪从输入token到最终logit的高归因因果路径。这些图的结构特征——包括全局统计、节点影响分布和拓扑模式——构成了推理步骤的“计算指纹”，可用于训练诊断分类器来预测步骤的正确性。

这种白盒视角填补了现有方法的关键缺口：它不仅判断推理是否正确，更揭示了**错误发生的计算机制**，为理解和修复LLM的推理失败提供了全新的分析工具。

## 核心创新

CRV的本质创新在于将思维链验证从“观测输出”转向“观测计算过程”。现有黑盒方法（如MaxProb、PPL、Energy等）仅通过输出概率或熵值判断步骤正确性，灰盒方法（如**CoE-R/C** (Wang et al., 2025a)、**CoT-Kinetics** (Bi et al., 2025)）虽引入部分内部状态，但均无法解释推理失败的计算原因。CRV通过以下关键设计实现了范式转变：

### 关键架构变更：MLP → Transcoder稀疏瓶颈

CRV对LLM架构做出的核心变更是将标准密集MLP层替换为训练好的**逐层transcoder**（per-layer transcoder），采用稀疏TopK激活机制模拟原始MLP的输入-输出功能。这一变更（Table 14显示指令微调数据训练的transcoder性能更优）使得模型内部计算以可解释的稀疏特征形式显式化，为后续构建归因图提供了基础。与直接使用原始MLP激活值的方法不同，transcoder将稠密、纠缠的神经元激活解耦为语义更清晰的稀疏特征，这是CRV能够追踪计算路径的根本前提。

### 核心机制：归因图作为计算执行轨迹

CRV的核心洞察在于将推理步骤的计算过程建模为**稀疏有向归因图** $G_i = (V, E)$。该图并非简单的注意力可视化，而是通过贪心路径搜索算法从最终logit反向追踪高归因连接，节点包括输入token、活跃transcoder特征和输出logit，边表示因果影响路径。这一设计将隐式的“模型如何计算该步骤”显式化为可分析的结构指纹，使得正确与错误推理的计算差异得以量化。

### 关键因果操控变量：Transcoder特征激活值

CRV揭示了transcoder中特定语义特征的激活值是可操纵的因果变量。实验表明，通过forward hook抑制或增强单个transcoder特征（如乘法特征）可直接改变模型的计算路径并纠正错误推理（Table 4, Table 19）。这一发现将错误检测从被动的分类任务升级为可干预的因果诊断，证明CRV识别的特征与推理失败之间存在因果关系，而非仅仅是相关性。

## 整体框架

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_CxiNICq0Rr/figures/001_Figure_1.jpg]]
*Figure 1: The CRV pipeline. (1) The LLM’s MLP modules are replaced with per-layer transcoders (PLTs), making it interpretable. (2) For a given CoT step, we generate an attribution graph capturing causal flow between interpretable features and model components. (3) Structural features are extracted from this graph, and (4) fed to a diagnostic classifier to predict the step’s correctness*

CRV（Circuit-based Reasoning Verification）是一个四阶段的白盒验证管道，其核心思想是将模型内部的推理计算过程显式化为可分析的计算图，并从中提取结构指纹来判断每一步推理的正确性。图1展示了该管道的完整流程。

**阶段一：模型可解释化改造。** 管道的起点是对目标大语言模型进行架构级修改，使其内部计算变得可解释。具体而言，CRV将模型中每个Transformer层的MLP模块替换为对应的逐层transcoder（Per-Layer Transcoder, PLT）。每个transcoder通过稀疏TopK激活来近似原始MLP的输入-输出映射，从而将原本密集、不透明的神经元活动分解为一组可解释的稀疏特征。这一替换使得后续的归因分析可以在语义上有意义的特征单元上进行，而非不可解释的神经元。

**阶段二：归因图构建。** 对于给定的一个思维链推理步骤 $s_i$，CRV从改造后的模型状态出发，采用基于归因的贪心路径搜索算法，从最终输出logit开始反向追踪高归因度的因果连接。该过程产出一个稀疏、加权、有向的归因图 $G_i = (V, E)$，其中顶点 $V$ 包括输入token、活跃的transcoder特征以及输出logit，边 $E$ 代表模型内部从特征到特征、从特征到输出的因果信息流。这些归因图本质上是对模型在执行该推理步骤时潜在算法过程的“执行轨迹”记录。

**阶段三：结构指纹提取。** 从每个归因图 $G_i$ 中，CRV提取一个固定维度的特征向量 $\mathbf{x}_i$ 作为该计算步骤的结构指纹。特征提取涵盖三个层次：(1) 全局统计特征，如图的规模、稀疏度等；(2) 节点影响与激活特征，反映各transcoder特征对最终输出的贡献程度和激活模式；(3) 拓扑与路径特征，捕捉图的结构化模式。在提取前，图会先被剪枝，仅保留对最终logit总影响贡献达到一定阈值（如80%）的节点和边。

**阶段四：诊断分类。** 最后，一个梯度提升分类器（Gradient Boosting Classifier, GBC）接收结构指纹 $\mathbf{x}_i$ 作为输入，输出对该推理步骤正确性的预测 $\hat{y}_i = f_{\theta}(\mathbf{x}_i)$。分类器在标注好的正确/错误步骤数据上进行训练，学习区分正确推理与错误推理所对应的不同计算图结构模式。

整个管道的核心假设是：正确推理步骤的归因图具有与错误步骤不同的结构指纹，且这些指纹携带了关于计算完整性的强信号，足以支撑高精度的错误检测。

## 核心模块与公式推导

### 问题形式化

CRV 将思维链推理验证形式化为一个二分类任务。给定一个推理步骤 $s_i$，从其模型内部状态中提取结构指纹 $\mathbf{x}_i$，然后通过诊断分类器预测该步骤的正确性：

$$\hat{y}_i = f_{\theta}(\mathbf{x}_i)$$

其中 $\hat{y}_i \in \{0, 1\}$ 表示步骤 $s_i$ 被预测为错误或正确，$f_{\theta}$ 为参数化的分类器（默认使用梯度提升分类器 GBC）。这一形式化将验证问题从表面的 token 序列分析转化为对底层计算图结构的判别。

### 归因图构建

CRV 的核心数据结构是归因图 $G_i = (V, E)$，它捕获了单个推理步骤在模型内部的计算轨迹。该图是一个稀疏、加权、有向图，其构成如下：

- **节点集合 $V$**：由三个互不相交的部分组成——输入 token、当前步骤中激活的 transcoder 特征、以及最终的输出 logit。
- **边集合 $E$**：代表从最终 logit 反向追踪到输入 token 的高归因因果路径。采用 Dunefsky et al.（2025）的贪心路径搜索算法，仅保留对最终 logit 贡献最大的连接，形成稀疏图结构。

这一构建过程的关键在于：transcoder 将原本稠密的 MLP 层替换为稀疏 TopK 激活的可解释瓶颈，使得每个激活特征具有明确的语义含义，从而让归因图中的节点不再是黑盒神经元，而是可追溯的计算原语。

### 结构指纹提取

从每个归因图 $G_i$ 中提取固定维度的特征向量 $\mathbf{x}_i$，作为该步骤计算完整性的结构指纹。特征分为三个层次：

1. **全局统计特征**：图的整体属性，如节点数、边数、图密度等。
2. **节点影响与激活特征**：各节点对最终 logit 的归因强度分布、transcoder 特征的激活模式统计。
3. **拓扑与路径特征**：图中关键路径的长度、分支结构、以及从输入到输出的信息流拓扑特性。

消融实验（Table 3）表明，节点影响与激活特征是最关键的特征族：移除该族后，AUROC 从 92.47 降至 88.31，FPR@95 增加超过 12 个百分点。

### 诊断分类器

诊断分类器 $f_{\theta}$ 将结构指纹 $\mathbf{x}_i$ 映射为正确性预测 $\hat{y}_i$。CRV 默认采用梯度提升分类器（Gradient Boosting Classifier），在所有数据集上提供鲁棒性能。分类器比较实验（Table 18）显示，逻辑回归在某些情况下也具有竞争力，表明归因图特征本身包含强烈的错误信号，对分类器选择具有一定的鲁棒性。

## 实验与分析

### 主实验结果

CRV在三个数据集上全面验证了其有效性。Table 1汇总了CRV与所有黑盒和灰盒基线方法的对比结果。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_CxiNICq0Rr/figures/002_Table_1.jpg]]
*Table 1: Verification performance. Arrows indicate preferred direction (↑ higher is better, ↓ lower is better). Best and second-best results are highlighted for each metric. The low AUPR on the Boolean dataset reflects extreme label imbalance, with the incorrect label only 0.2% (Appendix A.5)*

**合成数据集上的压倒性优势**：在Synthetic (Arithmetic)任务上，CRV取得了92.47的AUROC，相比最强基线Energy的76.45提升了16.02个百分点。在FPR@95指标上，CRV达到37.09，比最优灰盒方法CoE-C的63.33降低了26.24个百分点，表明在高召回率区间误报率大幅减少。AUPR从Energy的5.59跃升至28.92，提升超过23个百分点，说明CRV在极端类别不平衡下仍能有效识别错误步骤。在Synthetic (Boolean)任务上，CRV的AUROC为75.87，比MaxProb的58.81高出17.06个百分点，尽管该数据集的错误标签占比仅0.2%，导致AUPR绝对值偏低（0.97），但CRV仍在所有指标上保持领先。

**GSM8K上的稳健表现**：在真实数学推理场景中，CRV的AUROC达到70.17，超过最优基线Energy的62.55，提升7.62个百分点。AUPR为14.3，优于CoE-C的10.80。FPR@95为79.61，相比最强基线CoE-C的82.27有所改善。GSM8K上整体性能低于合成数据集，这反映了自然语言推理中计算图结构的复杂性和噪声更大。

**随难度增长的鲁棒性**：Figure 2展示了各方法在Synthetic (Arithmetic)任务上随运算符数量增加的性能变化。CRV在所有难度级别上保持明显优势，且性能衰减速度慢于基线方法。当运算符数量增加时，黑盒方法的AUROC下降显著，而CRV依靠计算图结构指纹维持了相对稳定的错误检测能力。

| 方法 | 类型 | Boolean AUROC↑ | Arithmetic AUROC↑ | GSM8K AUROC↑ | Arithmetic FPR@95↓ |
|------|------|----------------|-------------------|--------------|-------------------|
| MaxProb | 黑盒 | 58.81 | 75.37 | 60.53 | 67.99 |
| Energy | 黑盒 | 63.95 | 76.45 | 62.55 | 62.60 |
| CoE-C | 灰盒 | 60.05 | 74.22 | 61.46 | 63.33 |
| **CRV** | **白盒** | **75.87** | **92.47** | **70.17** | **37.09** |

### 跨域泛化分析

Table 2揭示了CRV错误指纹的关键特性：**高度领域特异性**。当CRV仅在Synthetic (Arithmetic)上训练后零样本迁移至GSM8K时，AUROC骤降至57.04，甚至低于GSM8K上的黑盒基线。同样，从GSM8K迁移至Arithmetic的AUROC仅为57.68。这表明不同推理任务的计算失败模式具有本质差异——算术运算中的错误图结构与数学应用题中的错误图结构不可互换。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_CxiNICq0Rr/figures/003_Table_2.jpg]]
*Table 2: Cross-domain generalization performance. For each test dataset, we compare the strongest baseline (based on AUROC) against CRV trained in-domain and out-of-domain. Best out-of-domain results are highlighted*

值得注意的是，当在组合数据集（Combined）上训练时，CRV在Arithmetic上的AUROC恢复至90.51，接近域内专家模型的92.47。这说明错误指纹并非互斥，而是需要分类器在训练阶段接触多样化的失败模式才能建立鲁棒的决策边界。

### 消融实验

**特征族重要性排序**：Table 3的留一法消融实验在Synthetic (Arithmetic)上揭示了清晰的特征层次。移除节点影响与激活特征（Node Influence & Activation）导致AUROC从92.47降至88.31，FPR@95从37.09飙升至超过49，增幅超12个百分点，表明该类特征对错误检测最为关键。全局统计特征和拓扑/路径特征的移除也造成性能下降，但影响程度较小。三类特征联合使用才能达到最优性能，说明它们捕获了互补的错误信号。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_CxiNICq0Rr/figures/007_Table_3.jpg]]
*Table 3: Leave-one-out ablation study on the Synthetic (Arithmetic) dataset*

**分类器选择**：Table 18显示梯度提升分类器（GBC）在所有数据集上提供最鲁棒的性能，但逻辑回归在部分场景下表现竞争力，这反向证明了CRV提取的结构指纹信号强度足够支撑线性可分性。

**归因图构建位置**：Table 15确认使用当前步骤最后一个token（"After"位置）构建归因图始终优于使用前一步骤的最后一个token（"Before"位置），验证了错误信号集中在步骤执行后的计算状态中。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_CxiNICq0Rr/figures/024_Table_15.jpg]]
*Table 15: Performance comparison of CRV using different token positions for attribution graph computation. The “After” setting computes the graph at the final token of the current step, while “Before” uses the final token of the previous step. Arrows indicate preferred direction (↑ higher is better, ↓ lower is better)*

### 错误的结构指纹可视化

Figure 4和Figure 3从不同角度验证了计算图包含可分离的错误信号。Figure 4展示了GSM8K上五个高预测力特征的分布对比——正确步骤（蓝色）与错误步骤（红色）在节点出度、路径长度、特征激活稀疏性等拓扑指标上呈现显著差异。独立t检验显示每个特征的组间差异均达到p < 0.001，Cohen's d效应量为中到大。Figure 3的PCA降维投影进一步显示，尽管存在重叠区域，正确与错误步骤在二维空间中形成了可辨别的聚类趋势，这解释了CRV分类器能够有效运作的原因。Synthetic (Arithmetic)和Synthetic (Boolean)数据集上的对应可视化（Figure 6和Figure 7）呈现类似模式，但不同任务间的具体分离特征存在差异。

### 因果干预验证

CRV的白盒特性使其能够从相关性分析推进到因果性验证。Table 4展示了一个典型案例：模型在计算`7*14`时错误地输出98（应为98，但后续推理路径错误），CRV识别出与该错误相关的乘法transcoder特征。通过forward hook将该特征的激活值钳制为零后，模型的计算路径发生根本改变——转而执行`14+7=21`，随后正确计算`7*21=147`，最终得到正确答案。Table 19展示了另一个通过增强乘法特征纠正减法错误的案例。这些因果干预实验直接证明：CRV识别的transcoder特征与推理错误之间存在操纵关系，而非仅仅是相关性。抑制或增强单个特征即可改变模型的计算路径，这为理解大语言模型的推理失败机制提供了机制性证据。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_CxiNICq0Rr/figures/016_Table_4.jpg]]
*Table 4: Side-by-side comparison of a reasoning trace before and after causal intervention. The highlight indicates the point of divergence where suppressing a single multiplication transcoder feature corrects the model’s computational path*

### 局限性与失败模式

尽管CRV在验证性能上表现出色，其实际部署面临显著挑战。首先，**计算开销巨大**：训练多个transcoder、替换模型MLP模块、为每个推理步骤构建归因图，使得CRV的资源消耗远超黑盒和灰盒方法，目前更适合作为科学分析工具而非生产级验证器。其次，**跨架构泛化未验证**：所有实验基于Llama 3.1 8B Instruct单一模型家族，MoE架构或更大规模模型上的适用性未知。第三，**特征粒度限制**：当前特征集主要捕获图的统计和拓扑属性，未充分利用个体transcoder特征的语义信息，限制了更精细的符号级推理验证。最后，**工具链保真度依赖**：CRV的有效性建立在transcoder近似精度和归因方法准确性的基础上，这些可解释性工具本身存在近似误差，可能影响错误指纹的可靠性。

### 补充图表

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_CxiNICq0Rr/figures/017_Table_5.jpg]]
*Table 5: Prompts used for CoT generation across the three datasets. Placeholders for dynamic content are shown in italics*

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_CxiNICq0Rr/figures/019_Table_10.jpg]]
*Table 10: Inter-Annotator Agreement (IAA) statistics for the human validation study. The comparison shows moderate-to-high agreement, with lower Kappa scores reflecting the extreme class imbalance*

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_CxiNICq0Rr/figures/020_Table_12.jpg]]
*Table 12: Final statistics of our curated datasets, showing the number of reasoning steps and the distribution of correct/incorrect labels after our full annotation and filtering process*

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_CxiNICq0Rr/figures/021_Table_13.jpg]]
*Table 13: End-to-end task accuracy of our base model (Llama 3.1 8B Instruct). For the synthetic datasets, we provide a fine-grained breakdown by difficulty, controlled by the number of operators (n)*

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_CxiNICq0Rr/figures/023_Table_14.jpg]]
*Table 14: Performance comparison of CRV with Base transcoders vs. transcoders further trained on Instruction-Tuning (IT) data. Arrows indicate preferred direction (↑ higher is better, ↓ lower is better)*

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_CxiNICq0Rr/figures/025_Table_16.jpg]]
*Table 16: Hyperparameter search space for the MLP Probe baseline*

## 方法谱系与知识库定位

### 白盒验证范式的确立

CRV 将推理验证从黑盒置信度估计和灰盒中间表征探测推进到**白盒计算图分析**层次。现有方法的核心瓶颈在于无法解释推理失败的计算原因：黑盒方法（**MaxProb**、**PPL**、**Entropy**、**Temp. Scaling** (Shih et al., 2023)、**Energy** (Liu et al., 2020)）仅依赖输出概率或不确定性信号；灰盒方法（**CoE-R**/**CoE-C** (Wang et al., 2025a)、**CoT-Kinetics** (Bi et al., 2025)、线性/MLP探针）虽能访问中间表征，但缺乏对潜在算法执行过程的因果洞察。CRV 通过将 MLP 层替换为可解释的稀疏 transcoder，并构建从最终 logit 反向追踪的归因图 $G_i = (V, E)$，首次实现了对推理步骤计算完整性的结构级诊断。这一方法论转变的核心假设是：**正确与错误推理步骤的归因图具有可区分的结构指纹**，且这些指纹可直接追溯到特定的可解释特征。

### 与电路分析和可解释性研究的衔接

CRV 的技术架构建立在两条研究线索的交汇处。在**模型可解释性**维度，CRV 采用 per-layer transcoder 替代标准 MLP 层（Section 3.2.1），将密集激活转化为稀疏 TopK 激活，从而在模拟原始 MLP 输入-输出功能的同时提供可解释的瓶颈。这一设计使归因图中的节点直接对应语义可解释的特征，而非不可解释的神经元。在**电路分析**维度，CRV 直接适配了 Dunefsky et al. (2025) 的贪心路径搜索算法，从最终 logit 反向追踪高归因连接，生成稀疏加权有向图。与原始电路分析工作不同，CRV 将这一工具从理解模型行为重新定位为**诊断推理失败**——通过提取图的全局统计、节点影响/激活和拓扑路径三个层次的结构指纹，将电路分析转化为可操作的验证信号。

### 适用边界与泛化性约束

CRV 的跨域泛化实验揭示了其核心约束：**错误指纹具有高度领域特异性**。当仅在 Arithmetic 任务上训练的 CRV 零样本迁移到 GSM8K 时，AUROC 骤降至 57.04（Table 2），远低于域内训练的 70.17。反之，从 Boolean 到 Arithmetic 的迁移同样表现不佳。这表明不同推理任务的计算失败模式各异，不存在通用的“错误计算图”签名。然而，当分类器在组合数据集上训练时，性能可恢复至接近域内专家水平（Arithmetic 上 AUROC 90.51），说明 CRV 的学习能力足以容纳多样化的错误模式，前提是训练数据覆盖目标领域的错误分布。此外，当前实验仅基于 Llama 3.1 8B Instruct 单一模型家族，是否适用于 MoE 架构或更大规模模型仍是开放问题。

### 关键局限与因果干预的边界

CRV 的计算成本构成其最显著的实用性约束。训练多个 per-layer transcoder、替换模型模块、为每一步构建归因图，远比黑盒和灰盒方法资源密集，使其目前更适合作为科学分析工具而非可扩展的生产级验证器。在特征层面，当前特征集主要捕捉图的统计和拓扑特性，未充分利用个体 transcoder 特征的语义信息，限制了更精细的符号级推理能力。

尽管因果干预实验（Table 4, Table 19）展示了令人信服的案例——通过 forward hook 抑制单个乘法 transcoder 特征可将错误的 $7 \times 14 = 98$ 纠正为正确的 $14 + 7 = 21$ 进而得到 $7 \times 21 = 147$——但这一能力的可推广性仍需审慎评估。干预的成功依赖于对特定错误模式对应特征的精确识别，而特征空间在不同任务和错误类型间的分布尚未被系统刻画。此外，分析的有效性整体受限于 transcoder 和归因方法的保真度，这些工具可能存在近似误差。

### 开放问题

CRV 开辟了若干关键研究方向。在架构层面，结构指纹是否能泛化到 MoE 等不同范式或显著更大的模型规模（如 70B+）尚待验证。在特征层面，指令微调如何影响 transcoder 的底层特征空间，以及是否存在超越当前高度领域特定签名的更普遍的计算失败原则，构成了理解模型推理失败机制的核心问题。在方法层面，能否开发出直接在解耦特征语义上操作的更高级分类器或神经符号验证器，将决定白盒验证是否能从诊断工具演进为实用的推理保障机制。

## 原文 PDF

![[paperPDFs/ICLR_2026/Verifying_Chain_of_Thought_Reasoning_via_Its_Computational_Graph.pdf]]
