---
title: "SkillOpt: Executive Strategy for Self-Evolving Agent Skills"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/SkillOpt_Executive_Strategy_for_Self_Evolving_Agent_Skills.pdf
project_link: null
code_link: https://aka.ms/SkillOpt
aliases:
- SkillOpt
tags:
- arxiv_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过将技能文档视为可训练的外部状态，引入有界文本编辑预算（学习率）、验证门控、拒绝编辑缓冲区和跨epoch慢速元更新，实现稳定的技能优化。
primary_logic: 将深度学习训练范式（训练/验证/测试分割、学习率调度、动量、负反馈）映射到文本空间，使技能优化成为一种可控的领域适应训练方法，而无需修改模型权重。
claims:
- SkillOpt在52个评估单元（模型×基准×执行环境）中全部达到最佳或并列最佳。
- 在GPT-5.5直接聊天模式下，SkillOpt将六个基准的平均准确率从58.8提升至82.3。
- 移除慢速/元更新和元技能导致SpreadsheetBench得分从77.5降至55.0。
- 优化的技能可以跨模型、跨执行环境和跨基准正向迁移，无负迁移情况。
---

# SkillOpt: Executive Strategy for Self-Evolving Agent Skills

> [!tip] 核心洞察
> 将深度学习训练范式（训练/验证/测试分割、学习率调度、动量、负反馈）映射到文本空间，使技能优化成为一种可控的领域适应训练方法，而无需修改模型权重。

| 字段 | 内容 |
|------|------|
| 中文题名 | SkillOpt：自进化智能体技能的优化策略 |
| 英文题名 | SkillOpt: Executive Strategy for Self-Evolving Agent Skills |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2605.23904) · [Code](https://aka.ms/SkillOpt) · [paper](https://arxiv.org/abs/2410.07985) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | SkillOpt |
| Dataset | SearchQA, SpreadsheetBench, OfficeQA, DocVQA |

> [!tip] 效果简介
> - SearchQA 上，准确率 (%) 87.3 vs 77.7 (+9.6)。
> - SpreadsheetBench 上，准确率 (%) 80.7 vs 41.8 (+38.9)。
> - OfficeQA 上，准确率 (%) 72.1 vs 33.1 (+39.0)。

## 概要

### 问题背景与核心瓶颈

大型语言模型驱动的智能体在执行复杂任务时，通常依赖一段自然语言策略文档（即“技能”）来指导行为。现有技能获取方式——人工编写、一次性LLM生成或无约束自修订——均缺乏**受控的、基于验证的迭代优化过程**。其根本瓶颈在于：技能在特定领域反馈下无法可靠改进，因为缺少类似深度学习训练中的训练/验证/测试分割、学习率调度、动量机制和负反馈利用等稳定化手段。

### 核心方法：SkillOpt

**SkillOpt** 将深度学习训练范式映射到文本空间，使技能优化成为一种可控的领域适应训练方法，而无需修改目标模型权重。其核心思想是将技能文档视为可训练的外部状态，通过以下机制实现稳定优化：

- **有界文本编辑预算**（类比学习率）：限制每次更新可应用的编辑数量，防止技能文档的剧烈震荡。
- **验证门控**：在保留选择集上评估候选技能，仅接受严格提升的更新，杜绝测试集信息泄露。
- **拒绝编辑缓冲区**：存储被拒绝的编辑，为后续优化器提供负反馈，避免重复无效修改。
- **跨epoch慢速元更新**：在epoch边界整合长周期经验，分离快速步级更新与慢速跨epoch整合。

优化的技能以独立文档形式部署，推理时不引入额外计算成本。

### 方法定位

在技能生成与优化的方法谱系中，SkillOpt区别于以下基线：

- **人工技能**与**一次性LLM技能**：无迭代优化，缺乏反馈驱动的改进能力。
- **Trace2Skill** 与 **EvoSkill**：从轨迹挖掘或进化技能，但缺少独立的验证步骤和负反馈机制。
- **TextGrad** 与 **GEPA**：基于梯度的提示优化方法，但未引入学习率预算、拒绝缓冲区等文本空间训练稳定性设计。

SkillOpt的关键创新在于引入**分离的优化器模型**（前沿模型）在离线训练中分析轨迹并提议编辑，而目标模型保持冻结，从而在部署时实现零额外推理成本。

### 主要结果

SkillOpt在**52个评估单元**（涵盖不同模型、基准和执行环境）中全部达到最佳或并列最佳。在GPT-5.5直接聊天设置下，六个基准的平均准确率从无技能的58.8提升至82.3（+23.5个百分点），其中SpreadsheetBench提升最为显著（从41.8到80.7，+38.9），OfficeQA次之（从33.1到72.1，+39.0）。优化的技能展现出正向跨模型、跨执行环境和跨基准迁移能力，无任何负迁移情况。消融实验证实，拒绝编辑缓冲区、慢速元更新和元技能等组件对性能有显著贡献——移除这些组件在SpreadsheetBench上导致得分从77.5骤降至55.0。

### 智能体技能文档的生成与优化困境

现代大语言模型（LLM）驱动的智能体在执行复杂任务时，通常依赖一段称为**技能文档（skill）**的自然语言策略。该文档预先注入智能体的上下文窗口，指导其在特定领域（如电子表格推理、文档问答、具身交互）中的行为模式。技能文档的质量直接决定了智能体的任务成功率，然而当前技能生成与优化方法存在显著瓶颈。

现有技能获取范式可归纳为三类，各有其结构性缺陷：

1. **手工编写技能（Human skill）**：依赖领域专家手动总结规则与启发式策略。虽然可解释性强，但编写成本高、迭代周期长，且难以穷举长尾场景中的失败模式。

2. **一次性LLM生成技能（LLM skill）**：通过向强模型提供少量示例，一次性生成技能文档。该方法缺乏针对实际执行反馈的闭环修正机制，生成质量高度依赖提示工程，无法保证在目标领域的泛化表现。

3. **无约束自修订方法**：以 **EvoSkill**、**Trace2Skill** 等为代表的进化方法，允许智能体根据自身轨迹进行技能修订。但这类方法缺少独立的验证门控——修订后的技能未经保留数据检验即被采纳，容易引入性能退化或过拟合训练噪声。同时，修订过程不受编辑预算约束，可能导致技能文档膨胀、引入矛盾规则或丢失有效策略。

### 核心瓶颈：缺乏受控的验证驱动迭代

上述方法的共同症结在于：**技能优化过程缺少受控的、基于验证的迭代机制**。具体表现为四个维度上的缺失：

- **编辑无界**：技能修订通常以全文重写或自由修改方式进行，无法量化控制每次更新的幅度，类似于深度学习中无学习率约束的权重更新。
- **验证缺失**：没有独立的保留选择集（held-out selection split）来门控技能更新，导致劣化修订可能被直接部署。
- **负反馈浪费**：被拒绝的编辑和失败模式未被系统记录和复用，优化器在后续迭代中可能重复同样的错误。
- **长期学习断裂**：缺少跨epoch的整合机制，单次训练中的经验无法沉淀为持久的元知识。

### 本文动机：将深度学习训练范式映射到文本空间

SkillOpt的核心动机源于一个关键洞察：**深度学习训练中的成熟机制——训练/验证/测试分割、学习率调度、动量、负反馈利用——可以映射到文本空间，使技能优化成为一种可控的领域适应训练方法，而无需修改目标模型的权重**。

具体而言，SkillOpt将技能文档视为可训练的外部状态，引入以下对应关系：

| 深度学习概念 | SkillOpt文本空间映射 |
|:---|:---|
| 学习率（learning rate） | 有界文本编辑预算 $L_t$，限制每次更新的添加/删除/替换操作数量 |
| 验证集（validation set） | 保留选择集 $D_{\text{sel}}$，仅接受严格提升的候选技能 |
| 梯度裁剪（gradient clipping） | 编辑预算上限与余弦衰减调度 |
| 动量（momentum）/负反馈 | 拒绝编辑缓冲区，存储失败编辑供后续优化器参考 |
| 多epoch训练 | Epoch-wise慢速/元更新，分离快速步级更新与跨epoch整合 |

通过这一映射，SkillOpt将技能优化从“一次性生成或盲目修订”转变为**受控的、数据驱动的迭代训练过程**。优化器（一个独立的前沿模型）在离线训练阶段分析执行轨迹、提议结构化编辑，并通过验证门控确保每次更新都带来可测量的性能提升。训练完成后，优化后的技能文档以轻量级文本形式部署，不增加推理时的计算开销。

这一方法论的核心优势在于：**优化的技能可跨模型、跨执行环境和跨基准正向迁移**——实验表明，SkillOpt在所有52个评估单元（模型×基准×执行环境）中均达到最佳或并列最佳，且未观察到任何负迁移情况（Table 4）。在GPT-5.5直接聊天模式下，六个基准的平均准确率从无技能的58.8%提升至82.3%，验证了受控迭代优化的有效性。

## 核心方法与创新机理

SkillOpt 的核心创新在于将深度学习训练范式系统性地映射到文本技能优化空间，构建了一个受控的、基于验证的技能自进化框架。与现有方法相比，其关键差异体现在以下五个维度：

### 1. 有界文本编辑预算：从无约束重写到可控优化

现有技能生成方法（手工编写、一次性 LLM 生成、无约束自修订）缺乏对技能更新幅度的精细控制，容易引入破坏性修改或过度拟合训练样本。SkillOpt 引入**文本学习率（textual learning rate）** 的概念，将每次更新的编辑操作数量限制为预算 $L_t$（Section 3.4）。优化器仅允许在技能文档上执行有限次数的结构化操作（追加、插入、替换、删除），并按优先级排序后选择性应用。这种有界更新机制直接对应深度学习中梯度步长的调控作用：过大的学习率导致震荡，过小则收敛缓慢。消融实验证实，$L_t=4$ 在三个基准上取得最佳整体表现（Table 2），验证了文本学习率作为关键控制旋钮的有效性。

### 2. 验证门控与拒绝编辑缓冲区：从无验证到严格接受标准

现有方法（如 EvoSkill、TextGrad）通常直接使用训练反馈进行更新，缺乏独立的验证步骤，导致技能可能过拟合训练分布或接受表面提升但泛化性差的编辑。SkillOpt 在保留选择集（held-out selection split）上执行严格的验证门控（Section 3.5）：仅当候选技能在选择集上取得**严格提升**时才接受更新。被拒绝的编辑存入**拒绝编辑缓冲区**，作为负反馈供后续优化器调用，避免重复尝试已证明无效的修改方向。消融实验显示，移除拒绝编辑缓冲区导致 SearchQA、SpreadsheetBench 和 LiveMath 得分分别下降 1.6、4.6 和 2.4 个百分点（Table 3），证实了负反馈机制对优化稳定性的贡献。

### 3. 慢速/元更新：从单步优化到跨 Epoch 长周期整合

现有方法缺少跨 epoch 的知识整合机制，每次更新仅基于当前批次的局部信息。SkillOpt 引入**Epoch-wise 慢速/元更新**（Section 3.6）：在 epoch 边界，优化器比较两个技能版本间的差异，提取长周期经验教训，编写受保护的元级指导（meta-instructions），并同样通过验证门控筛选。这种设计分离了快速步级编辑（处理即时失败模式）与慢速跨 epoch 整合（提炼持久策略），类似深度学习中动量或学习率衰减的作用。消融实验表明，同时移除慢速/元更新和元技能导致 SpreadsheetBench 得分从 77.5 骤降至 55.0（Table 3），揭示了长周期整合对复杂推理任务的极端重要性。

### 4. 分离的优化器模型：从自我修订到离线专家指导

EvoSkill 等方法让目标模型自身进行技能修订，受限于目标模型的能力边界。SkillOpt 采用**分离的优化器模型**（前沿模型，如 GPT-5.5）在离线训练阶段分析轨迹并提议编辑（Figure 1），部署时仅导出优化后的技能文档，不增加任何推理成本。这种师生架构使得弱模型也能受益于强优化器的编辑能力。Table 5 的分析表明，使用强优化器（GPT-5.5）相比使用目标匹配优化器持续带来额外增益，而部署成本为零。

### 5. 优化器侧元技能：从无记忆到编辑策略的自我改进

SkillOpt 在优化器侧维护**元技能（meta-skill）**，总结历史编辑模式的有效性，指导未来优化器的编辑生成（Section 3.6, Appendix C.2.8）。元技能不随技能部署到目标模型，仅在训练循环内部使用，形成对编辑策略本身的二阶优化。这类似于元学习中“学会如何学习”的思想，使优化过程随经验积累而变得更加高效。

综上，SkillOpt 通过有界编辑预算、验证门控、负反馈缓冲区、慢速/元更新和分离优化器五个相互协同的机制，将技能优化从一次性生成或无约束修订提升为可控的、数据驱动的迭代训练过程，在 52 个评估单元（模型×基准×执行环境）中全部达到最佳或并列最佳（Table 1），证明了该设计范式的有效性。

SkillOpt 将智能体技能文档视为可优化的外部文本状态，通过一个“冻结目标模型 + 离线优化器”的分离式架构实现技能的受控进化。其核心设计理念是将深度学习训练范式（训练/验证/测试分割、学习率调度、动量、负反馈）映射到文本空间，在不修改模型权重的前提下完成领域适应。

### 架构概览

系统由三个关键角色构成（Figure 1）：

- **目标模型 (Target Model)**：冻结的智能体模型，在给定技能文档 $s$ 的指导下执行任务。每步执行产生轨迹 $\tau(s)$ 和标量得分 $r(s) \in [0,1]$。
- **优化器模型 (Optimizer Model)**：一个独立的前沿模型（通常强于目标模型），仅在离线训练阶段运行。它分析目标模型产生的成功/失败轨迹，提出结构化的文本编辑。
- **验证门控 (Held-out Gate)**：基于保留的选择集 $D_{\mathrm{sel}}$ 评估候选技能，仅接受严格提升性能的更新。

### 管道流程

Figure 2 展示了完整的迭代优化管道，包含以下核心模块：

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2605_23904/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline of SkillOpt. A frozen target model executes a rollout batch with the current skill; an optimizer model performs minibatch reflection over successes and failures, proposes bounded add/delete/replace edits, merges and ranks them under a scheduled edit budget, and accepts the candidate skill only through a held-out validation gate. Across epochs, the slow/meta update retains longer-horizon lessons without changing the target model*

1. **Rollout批次执行**：使用当前技能 $s$ 在训练数据 $D_{\mathrm{tr}}$ 上批量执行目标模型，收集轨迹和得分。

2. **Minibatch反思**：将轨迹按成功/失败分组，以 minibatch 为单位进行分析。优化器识别常见失败模式和成功模式，为后续编辑提供依据。

3. **编辑提议与合并**：优化器分别为失败和成功轨迹提议编辑，通过分层合并策略（优先失败相关编辑）生成候选编辑池。

4. **有界编辑应用**：根据文本学习率预算 $L_t$（最大编辑数）排序并选择编辑，以补丁模式操作（追加、插入、替换、删除）更新技能文档。

5. **验证门控**：在选择集 $D_{\mathrm{sel}}$ 上评估候选技能，仅当性能严格提升时才接受更新。被拒绝的编辑存入**拒绝编辑缓冲区 (Rejected-Edit Buffer)**，为后续优化器提供负反馈信号。

6. **慢速/元更新 (Slow/Meta Update)**：在 epoch 边界，比较两个技能版本，编写受保护的长周期指导。优化器侧还维护**元技能 (Meta Skill)**，总结编辑模式的有效性，指导未来优化器的编辑生成。此模块不随技能部署到目标模型。

### 输入输出流

- **输入**：初始技能文档 $s_0$（可为空或人工编写）、训练数据 $D_{\mathrm{tr}}$、选择集 $D_{\mathrm{sel}}$、测试集 $D_{\mathrm{test}}$。
- **内部状态**：当前技能 $s_t$、拒绝编辑缓冲区、优化器侧元技能。
- **输出**：经过选择集验证的最佳技能 $s_{\mathrm{sel}}^{\star}$，即：
  $$s_{\mathrm{sel}}^{\star} = \arg\max_{s \in \mathcal{C}(D_{\mathrm{tr}})} \frac{1}{|D_{\mathrm{sel}}|} \sum_{x \in D_{\mathrm{sel}}} r(s)$$
  最终测试性能为：
  $$\mathrm{Test}(s_{\mathrm{sel}}^{\star}) = \frac{1}{|D_{\mathrm{test}}|} \sum_{x \in D_{\mathrm{test}}} r(s_{\mathrm{sel}}^{\star})$$

### 关键设计特性

- **分离式优化**：优化器仅在离线训练阶段运行，部署时目标模型仅使用优化后的技能文档，无额外推理成本。
- **有界编辑预算**：通过 $L_t$ 控制每步最大编辑数，模拟学习率对更新幅度的约束，防止技能文档的剧烈震荡。
- **严格验证门控**：基于独立选择集的接受机制避免了测试集信息泄露，同时确保技能质量的单调提升。
- **负反馈利用**：拒绝编辑缓冲区使优化器能从失败尝试中学习，避免重复无效的编辑方向。
- **多时间尺度学习**：快速步级更新处理即时反馈，慢速跨 epoch 整合保留长期经验，元技能提供跨任务的编辑策略指导。

SkillOpt 将技能文档视为可训练的外部状态，通过分离的优化器模型在文本空间中对技能进行受控迭代更新，整个流程不修改目标模型的权重。其核心机制可以分解为以下模块。

### 任务执行与评分函数

技能 $s$ 是一段自然语言策略，在执行前被插入到智能体的上下文中。给定执行环境 $h$、目标模型 $M$、任务 $x$ 和技能 $s$，执行过程产生轨迹 $\tau$ 和标量得分 $r$：

$$( \tau ( s ) , r ( s ) ) = h ( M , x , s ) , \qquad r ( s ) \in [ 0 , 1 ]$$

其中 $r(s)$ 是归一化到 $[0,1]$ 区间的标量得分，用于量化技能在该任务上的表现。

### 技能选择与测试评估

从训练数据 $D_{\mathrm{tr}}$ 生成的候选技能集合 $\mathcal{C}(D_{\mathrm{tr}})$ 中，选择在保留选择集 $D_{\mathrm{sel}}$ 上平均得分最高的技能作为最终部署技能：

$$s _ { \mathrm { s e l } } ^ { \star } = \arg \operatorname* { m a x } _ { s \in \mathcal { C } ( D _ { \mathrm { t r } } ) } \frac { 1 } { | D _ { \mathrm { s e l } } | } \sum _ { x \in D _ { \mathrm { s e l } } } r ( s )$$

最终测试性能为所选技能在测试集 $D_{\mathrm{test}}$ 上的平均得分：

$$\mathrm { T e s t } ( s _ { \mathrm { s e l } } ^ { \star } ) = \frac { 1 } { | D _ { \mathrm { t e s t } } | } \sum _ { x \in D _ { \mathrm { t e s t } } } r ( s _ { \mathrm { s e l } } ^ { \star } )$$

这一分离设计确保了测试集信息不会泄露到技能选择过程中。

### 管道核心模块

SkillOpt 的优化管道由以下关键模块串联而成，形成完整的训练循环（参见 Figure 2）：

1. **Rollout 批次执行**：冻结的目标模型使用当前技能在训练数据上批量执行任务，生成轨迹和对应得分。每个任务产生一组成功或失败的执行记录，作为后续反思的原始证据。

2. **Minibatch 反思**：将轨迹按成功和失败分组，以 minibatch 为单位进行分析。优化器模型识别常见的失败模式（如特定类型的推理错误）和成功模式（如有效的解题策略），为编辑生成提供结构化的反馈信号。

3. **编辑提议与合并**：优化器模型针对失败和成功轨迹分别提议编辑操作（追加、插入、替换、删除），然后通过分层合并策略（优先处理失败相关的编辑）生成最终的候选编辑池。编辑以补丁模式作用于技能文档。

4. **有界编辑应用**：引入文本学习率预算 $L_t$，即第 $t$ 步允许应用的最大编辑数量。候选编辑按优先级排序后，在预算约束下被应用到技能文档，形成候选技能。$L_t$ 是深度学习中学习率概念的文本空间类比，控制每次更新的幅度。

5. **验证门控**：候选技能在保留选择集 $D_{\mathrm{sel}}$ 上进行严格评估。仅当候选技能在选择集上的平均得分严格高于当前最佳技能时，该更新才被接受。这一门控机制防止了过拟合和退化更新。

6. **拒绝编辑缓冲区**：被验证门控拒绝的编辑及其关联的失败模式被存入缓冲区。在后续优化步骤中，优化器可以调用这些负反馈信息，避免重复提出已被证明无效的编辑。

7. **慢速/元更新**：在 epoch 边界，优化器比较两个技能版本（当前最佳技能与 epoch 起始技能），编写受保护的长周期指导规则。这些元更新同样通过验证门控筛选，用于捕获跨 epoch 的高层次学习信号，类似于深度学习中的动量或学习率调度机制。

8. **优化器侧元技能**：优化器在训练过程中总结编辑模式的有效性，形成元技能。元技能指导未来优化器的编辑生成策略，但不随最终技能部署到目标模型，因此不增加推理成本。

### 优化器与目标模型的分离

SkillOpt 的一个关键设计选择是使用分离的优化器模型（通常为更强的前沿模型，如 GPT-5.5）在离线训练阶段分析轨迹并提议编辑。目标模型在部署时仅加载优化后的技能文档，无需额外推理开销。实验表明（Table 5），更强的优化器能产生更大的性能增益，且这一优势在部署时零成本。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2605_23904/figures/001_Figure_1.jpg]]
*Figure 1: Overview of SkillOpt. The target model executes tasks with a current skill, an additional frontier optimizer model converts trajectories into bounded add/delete/replace skill edits, and a held-out gate accepts only edits that improve validation performance. Accepted edits are exported as a reusable skill artifact, while rejected edits become negative feedback for later updates*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2605_23904/figures/007_Figure_3.jpg]]
*Figure 3: Performance trends across epoch checkpoints on three benchmarks: (a) SpreadsheetBench, (b) SearchQA, and (c) LiveMath. For each checkpoint, we report the training rollout score, the selection-best score on the validation set, and the final performance on the unseen test set. The results show how skill quality evolves during optimization and whether the checkpoint preferred by validation selection aligns with the checkpoint that yields the best generalization to the test set*

## 实验与关键发现

### 主实验结果

SkillOpt在52个评估单元（模型×基准×执行环境）中全部达到最佳或并列最佳（Table 1），且在所有单元上均相对于无技能基线取得正向增益。以GPT-5.5直接聊天模式为例，六个基准的平均准确率从58.8（无技能）提升至82.3（SkillOpt），绝对提升+23.5个百分点。各基准的具体表现如下：

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2605_23904/figures/006_Table_4.jpg]]
*Table 4: Transfer of optimized skills across three axes. (a) Cross-model: a skill optimized for the source model is deployed on the target model. (b) Cross-harness: a skill trained inside the source harness is evaluated inside the target harness, all on GPT–5.5. (c) Cross-benchmark: the source benchmark skill is evaluated on the target benchmark across three target models. Baseline is the target’s no-skill score, Direct is the in-domain SkillOpt score, and Transferred applies the source skill without further optimization. Subscripts show the change over the target baseline. The GPT–5.4→GPT–5.4 transferred cells in (a) are marked – because source and target match (i.e. no transfer occurs); we still r...*

| 基准 | 无技能基线 | SkillOpt | 提升幅度 |
|------|-----------|----------|---------|
| SearchQA | 77.7 | 87.3 | +9.6 |
| SpreadsheetBench | 41.8 | 80.7 | +38.9 |
| OfficeQA | 33.1 | 72.1 | +39.0 |
| DocVQA | 78.8 | 91.2 | +12.4 |
| LiveMathematicianBench | 37.6 | 66.9 | +29.3 |
| ALFWorld | 83.6 | 95.5 | +11.9 |

SkillOpt在不同目标模型和执行环境（直接聊天、Codex、Claude Code）下均保持一致的领先优势。与现有方法相比，SkillOpt显著优于一次性LLM生成的技能（LLM skill）、人工编写的技能（Human skill）、基于轨迹挖掘的进化方法（Trace2Skill、EvoSkill）以及基于梯度的提示优化方法（TextGrad、GEPA）。

### 消融实验

**文本学习率预算**：将文本学习率 $L_t$ 设为4在三个基准（SearchQA、SpreadsheetBench、LiveMath）上取得最佳整体表现（86.5/78.2/56.5）。使用100%训练数据（而非子集）可进一步提升所有三个基准的性能（Table 2）。

**拒绝编辑缓冲区**：移除拒绝编辑缓冲区导致SearchQA、SpreadsheetBench和LiveMath得分分别下降1.6、4.6和2.4个百分点（Table 3），验证了负反馈机制对避免重复失败编辑的关键作用。

**慢速/元更新与元技能**：移除慢速/元更新和元技能导致SpreadsheetBench得分从77.5骤降至55.0（Table 3），降幅达22.5个百分点。这表明跨epoch的长周期整合对于复杂任务（如电子表格推理）至关重要——仅靠步级快速更新无法有效积累跨批次的领域知识。

### 技能迁移能力

Table 4展示了优化技能在三个轴向上的迁移表现：
- **跨模型迁移**：为源模型优化的技能部署到目标模型时，所有迁移行均为正向迁移，无一行低于目标模型的无技能基线。
- **跨执行环境迁移**：在源环境中训练的GPT-5.5技能迁移到目标环境后，同样全部取得正向增益。
- **跨基准迁移**：源基准的技能在目标基准上评估时，三个目标模型均表现出正向迁移，无负迁移情况。

这一结果表明SkillOpt生成的技能具有高度的泛化性和可移植性，不局限于特定的模型或执行环境。

### 优化器强度分析

Table 5显示，使用强前沿优化器（GPT-5.5）比使用与目标模型匹配的优化器在所有基准上均取得更高增益。由于优化器仅在离线训练阶段运行，部署时使用更强优化器不会增加任何推理成本。Table 6进一步展示了技能学习的成本经济性——以GPT-5.5/GPT-5.5配置为例，最终技能文档在多次有界编辑后保持紧凑，每个测试点绝对增益的训练token成本可控。

### 性能趋势与学习动态

Figure 3展示了三个基准上跨epoch检查点的性能趋势。训练rollout得分、验证集上的选择最佳得分以及测试集上的最终性能曲线揭示了技能质量在优化过程中的演变规律。验证选择偏好的检查点通常与测试集上泛化最佳的检查点对齐，表明验证门控机制有效防止了过拟合。

### 代表性学习规则

Figure 4展示了从最终部署技能中提取的代表性学习规则，每个基准一条。值得注意的是，所有规则都是过程性的（procedural）而非实例特定的，其中多条规则编码了前沿模型零样本时不会自发应用的“纪律”——如答案格式约束、证据绑定要求、搜索前沿管理等。这印证了SkillOpt的核心机制：通过受控的迭代优化，将领域反馈转化为可执行的文本策略，而无需修改模型权重。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2605_23904/figures/005_Table_2.jpg]]
*Table 2: Hyperparameter analysis for the text optimizer. Each panel changes one scalar or scheduling factor from the default setting unless noted. Panel (a) fixes the split to 4:1:5 train/selection/test; the 1-example, 20%, 40%, and 80% rows use subsets of the training partition, and the 100% row reuses the completed 4:1:5 split-ratio run. Panel (b) sweeps the reflection mini-batchsize B _ { m } ; panel (c) sweeps the rollout batchsize B. Table 3 Component ablations for learning-rate form, rejected buffer, and epoch-wise slow/meta update. Light-blue rows mark the default setting within each component group; the learning-rate group uses the default lr=4 setting. Bold values mark the best measured res...*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2605_23904/figures/009_Table_5.jpg]]
*Table 5: Effect of optimizer strength. Each (benchmark, target) pair is optimized either by a strong frontier optimizer (GPT–5.5, bolded) or by a target-matched optimizer that shares the target model; everything else in the SkillOpt loop is held fixed. Gains over the target’s no-skill baseline are shown as small green subscripts; the same baseline is used for both optimizer settings within a row. The optimizer runs only during offline training, so the stronger-optimizer column adds zero cost at deployment. Table 6 Cost and edit economy of the GPT–5.5 / GPT–5.5 (student / teacher) skill runs. Initial and final best_skill.md lengths are in tokens; Edits is the number of accepted bounded updates; Cost...*

## 定位与知识库关联

### 技能生成方法的演进脉络

SkillOpt 处于**基于文本的智能体技能自动优化**这一研究脉络中，其核心贡献在于将深度学习训练范式系统地映射到文本空间，实现了可控的、基于验证的技能迭代优化。

传统技能获取方法存在明显的瓶颈：
- **手工编写**和**一次性LLM生成**：缺乏基于任务反馈的改进机制，技能质量完全依赖初始设计。
- **Trace2Skill**：从执行轨迹中挖掘技能，但缺少受控的迭代优化循环。
- **EvoSkill**：允许技能自我进化，但目标模型自身进行无约束修订，缺乏独立验证步骤，容易引入退化更新。
- **TextGrad** 和 **GEPA**：基于梯度的提示优化方法，主要针对单轮提示优化，缺乏跨epoch的长期学习机制和系统的负反馈利用。

SkillOpt 通过以下核心机制突破了上述瓶颈：

1. **分离的优化器角色**：引入一个独立的前沿优化器模型（而非目标模型自身）在离线训练中分析轨迹并提议编辑。优化器仅在训练时运行，部署时无额外推理成本。Table 5 的实验表明，使用更强的优化器（GPT-5.5）可带来显著的性能增益，且不增加部署成本。

2. **有界文本编辑预算**：将文本编辑操作（追加、插入、替换、删除）受限于可调度的学习率预算 $L_t$，模拟深度学习中学习率对参数更新的约束。Table 2 的消融显示 $L_t=4$ 在三个基准上取得最佳整体表现（86.5/78.2/56.5），验证了适度编辑预算的重要性。

3. **验证门控机制**：在保留选择集上严格评估候选技能，仅接受严格提升的技能更新，避免了测试集信息泄露和退化更新。这一机制直接对应深度学习中的验证集早停策略。

4. **拒绝编辑缓冲区**：存储被拒绝的编辑和失败模式，为后续优化器提供负反馈。Table 3 消融显示，移除该缓冲区导致 SearchQA、SpreadsheetBench 和 LiveMath 分别下降 1.6、4.6 和 2.4 个百分点。

5. **慢速/元更新**：在 epoch 边界进行跨周期整合，分离快速步级更新和慢速长周期指导。Table 3 显示，移除慢速/元更新和元技能导致 SpreadsheetBench 得分从 77.5 骤降至 55.0，降幅达 22.5 个百分点，是该消融中影响最大的组件。

### 适用边界与泛化能力

SkillOpt 的适用边界由以下因素界定：

**正向适用场景**：
- 目标模型冻结、不可微调的智能体系统
- 需要跨模型、跨执行环境迁移技能的部署场景
- 有明确标量奖励信号的任务（如准确率、成功率）

**迁移能力验证**：Table 4 展示了技能在三个轴向上的正向迁移：
- **跨模型迁移**：为源模型优化的技能部署到目标模型上，所有迁移行均为正向（无一行低于目标模型的无技能基线）
- **跨执行环境迁移**：在一种 harness 中训练的技能在另一种 harness 中评估，全部正向迁移
- **跨基准迁移**：源基准技能在目标基准上评估，同样全部正向迁移

**关键限制**：
- 依赖标量奖励信号，对于开放式任务需要无奖励或偏好驱动的验证门控（论文列为开放问题）
- 优化器侧元技能是否可在不同基准之间重用尚待验证
- 技能文档作为外部状态，不改变模型权重，可能无法捕捉需要权重级适应的深层模式

### 开放问题

SkillOpt 框架开启了若干值得探索的方向：

1. **技能库基础设施共享**：能否在不同领域间共享技能库基础设施，形成可复用的技能生态？
2. **元技能跨基准重用**：优化器侧的元技能是否可以在不同基准之间迁移，减少新任务的冷启动成本？
3. **无奖励验证门控**：对于开放式任务，能否使用偏好驱动或自洽性驱动的验证门控替代标量奖励？
4. **技能自蒸馏**：能否将优化后的技能自蒸馏回目标模型，实现权重级适应，同时保留文本技能的显式可解释性？

### 知识库定位总结

SkillOpt 在智能体技能优化领域的位置可概括为：**将受控训练范式引入文本空间技能优化的系统性框架**。它区别于无约束自我修订方法（EvoSkill）、单轮提示优化方法（TextGrad, GEPA）和轨迹挖掘方法（Trace2Skill），通过文本学习率预算、验证门控、负反馈缓冲区和慢速元更新四个机制，实现了稳定、可迁移的技能优化。其核心洞察——将训练/验证/测试分割、学习率调度、动量等深度学习概念映射到文本空间——为未来文本空间优化方法的设计提供了可复用的范式。

## 原文 PDF

![[paperPDFs/arxiv_2026/SkillOpt_Executive_Strategy_for_Self_Evolving_Agent_Skills.pdf]]
