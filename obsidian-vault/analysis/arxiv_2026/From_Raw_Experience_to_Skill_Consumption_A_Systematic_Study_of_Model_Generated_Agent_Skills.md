---
title: "From Raw Experience to Skill Consumption: A Systematic Study of Model-Generated Agent Skills"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/From_Raw_Experience_to_Skill_Consumption_A_Systematic_Study_of_Model_Generated_Agent_Skills.pdf
aliases:
- MSGE
- FRESCSSMGAS
tags:
- arxiv_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 技能效用的核心调节因素包括(1)经验池中成功与失败轨迹的配比，(2)提取时是否通过明确的维度（失败机制编码、可执行细节、高风险动作黑名单）来引导内容生成，(3)下游消费者模型自身的技能利用能力，即同一技能文本对不同目标模型效益差异显著。
primary_logic: 通过对高Δ技能对的自动化对比分析，发现三个与下游效用高度一致的文本维度：失败机制编码（更好率65.5%）、可执行细节（66.0%）和高风险动作黑名单（64.6%）。将这些维度固化为提取阶段的meta-skill先验，可以在不改变模型或任务的情况下，一致地提升所有测试单元的性能，并有效缓解负迁移问题。
claims:
- 模型生成的技能在75%的提取-目标配对中带来正向增益，但25%的配对出现负迁移（Δ<0）。ALFWorld域最脆弱，负迁移率高达47%。
- 技能格式（有序列表、无序列表、检查表、散文）对下游任务性能无显著影响（Friedman检验，所有目标p>0.34），但提取器的选择具有显著影响（p<0.01）。
- 未引导的LLM法官评价技能质量的准确率仅为46.4%（随机基准50%），且准确性随效用差距增大而下降：在Δ≥5pp的高差距对上，准确率降至15.8%。
- 由效用验证的三个维度（失败机制编码、可执行细节、高风险动作黑名单）构成的validated rubric，应用于提取meta-skill后，在全部9个测试单元中均提升了性能（平均+1.55 pp），而基于文本合理性的7维rubric在6/9单元中导致性能下降（平均-0.59 pp）。
---

# From Raw Experience to Skill Consumption: A Systematic Study of Model-Generated Agent Skills

> [!tip] 核心洞察
> 通过对高Δ技能对的自动化对比分析，发现三个与下游效用高度一致的文本维度：失败机制编码（更好率65.5%）、可执行细节（66.0%）和高风险动作黑名单（64.6%）。将这些维度固化为提取阶段的meta-skill先验，可以在不改变模型或任务的情况下，一致地提升所有测试单元的性能，并有效缓解负迁移问题。

| 字段 | 内容 |
|------|------|
| 中文题名 | 从原始经验到技能消费：模型生成型Agent技能的系统性研究 |
| 英文题名 | From Raw Experience to Skill Consumption: A Systematic Study of Model-Generated Agent Skills |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2605.23899) · [Code](https://aka.ms/SkillLens) · [arXiv](https://arxiv.org/abs/2604.01687) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Meta-Skill Guided Extraction |
| Dataset | SpreadsheetBench, ALFWorld, SWE-bench-Verified |

> [!tip] 效果简介
> - SpreadsheetBench 上，Accuracy (%) 48.50 vs 46.17 (+2.33 pp)。
> - ALFWorld 上，Accuracy (%) 76.12 vs 75.12 (+1.00 pp)。
> - SWE-bench-Verified 上，Accuracy (%) 70.10 vs 69.72 (+0.38 pp)。

## 概述

**核心问题与瓶颈。** 当前基于模型生成（model-generated）的Agent技能提取方法存在一个隐蔽但关键的失效模式：大约25%的提取-目标配对出现负迁移（Δ<0），即注入技能后下游性能反而下降。在ALFWorld等具身交互领域，负迁移率甚至高达47%。更棘手的是，技能的效用无法通过表面文本特征（如格式、文本合理性）来可靠预测：未经训练的LLM法官在选出更优技能的任务上准确率仅为46.4%（随机基线50%），且当技能对之间的性能差距增大到5个百分点以上时，准确率急剧降至15.8%。这揭示了一个根本性瓶颈——**真正决定技能效用的，不是技能文本写得有多“好”，而是技能中是否编码了领域特定的失败机制、可执行的对策以及高风险行为禁令**，而常规提取往往输出泛泛而谈的指导。

**核心洞察与方法定位。** 本研究通过对高Δ技能对的自动化对比分析，发现了三个与下游效用高度一致的文本维度：失败机制编码（更好率65.5%）、可执行细节（66.0%）和高风险动作黑名单（64.6%）。将这些维度固化为提取阶段的meta-skill先验——即在提取提示中注入一段简短的指导，要求技能内容必须着重体现上述三个维度——可以在不改变模型或任务的情况下，一致地提升所有测试单元的性能（平均+1.55 pp），并有效缓解负迁移问题。这一方法在方法谱系中定位为**提取阶段的先验注入策略**：不同于Trace2Skill（轨迹到技能的蒸馏与冲突消解）或CoEvoSkills（协同进化验证），Meta-Skill Guided Extraction的核心创新在于用下游效用验证过的维度来引导提取器的生成过程，而非改变提取架构或引入额外的验证回路。

**主要结果概览。** 在五个任务领域（ALFWorld、SpreadsheetBench、SWE-bench-Verified、SEAL-0、BFCL-v4）上的系统评估表明：模型生成的技能在75%的配对中带来正向增益，但负迁移风险不可忽视；技能格式（有序列表、无序列表、检查表、散文）对下游性能无显著影响（Friedman检验，所有p>0.34），而提取器的选择具有显著影响（p<0.01）；经验池中成功与失败轨迹的配比是关键调节因素，最佳比例因域而异；基于文本合理性的7维rubric引导提取在6/9测试单元中导致性能下降（平均-0.59 pp），而效用验证的3维rubric在全部9个测试单元中均提升性能（平均+1.55 pp），验证了“效用驱动的内容引导”优于“表面质量引导”这一核心主张。

## 背景与动机

**从经验中学习**是智能体能力演进的核心路径。人类专家在完成复杂任务后，会将成功与失败的经验提炼为可复用的技能——这些技能不仅是操作步骤的罗列，更编码了对领域陷阱的警觉、对关键决策点的判断以及对高风险动作的规避。然而，当前的语言模型智能体虽然能够通过执行任务产生大量轨迹数据，如何系统性地将这些“原始经验”转化为可迁移、可消费的技能，仍是一个开放问题。

**现有技能提取方法的缺口**在于：我们缺乏对“什么真正驱动下游效用”的理解。已有工作如 **Trace2Skill**（轨迹到技能的蒸馏，采用子智能体舰队与冲突消解机制）和 **CoEvoSkills**（协同进化验证的技能包精炼）探索了技能生成的自动化流程，但它们的设计选择——如何组织经验、如何引导提取、如何评估技能质量——大多基于直觉而非系统性验证。这导致两个关键盲区：（1）技能提取过程中的哪些因素真正影响下游性能，哪些只是表面文本特征？（2）我们能否在不依赖昂贵下游评估的情况下，预测甚至保证技能的效用？

**本文的核心动机**正是填补这一认知鸿沟。研究通过一个完整的三阶段生命周期框架（经验生成→技能提取→技能消费，见图1），对模型生成型智能体技能进行了系统性解剖。研究不仅量化了技能效用在不同领域、不同提取器、不同目标模型间的分布，更揭示了一个关键发现：当前技能提取方法在约25%的配对中导致负迁移，且技能效用无法通过表面文本特征（格式、文本合理性）来可靠预测。真正决定效用的是技能中是否编码了**领域特定的失败机制、可执行的对策以及高风险行为禁令**——而常规提取往往输出泛泛而谈的指导。基于这一洞察，研究将效用验证的维度固化为提取阶段的先验指导，实现了对所有测试单元的一致性提升。

## 核心创新

### 创新动机：技能生成的负迁移困境

本研究揭示了一个此前被忽视的关键瓶颈：模型生成的Agent技能在约25%的提取-目标配对中导致负迁移（Δ < 0），其中ALFWorld域最为脆弱，负迁移率高达47%（Table 1）。更棘手的是，这一效用危机无法通过常规手段诊断——未经训练的LLM法官评价技能质量的准确率仅为46.4%（接近随机基准50%），且在高性能差距对（Δ ≥ 5pp）上准确率骤降至15.8%（Figure 3）。技能格式（有序列表、无序列表、检查表、散文）对下游性能无显著影响（Friedman检验，所有目标p > 0.34），意味着表面文本特征无法可靠预测效用（Table 8）。真正决定技能效用的，是技能文本中是否编码了领域特定的失败机制、可执行对策以及高风险行为禁令。

### 核心创新：效用验证的三维Meta-Skill先验

针对上述瓶颈，本研究的核心创新在于**将效用驱动的技能质量维度固化为提取阶段的先验知识**，而非依赖事后评估。具体实现路径如下：

1. **自动化对比发现管道**：以高Δ技能对为输入，通过GPT-5.4自动提取差异并迭代合并，生成包含七个候选维度的原始rubric（Table 13）。
2. **效用验证筛选**：通过下游任务性能验证，筛选出三个与效用高度一致的维度——**失败机制编码**（更好率65.5%）、**可执行细节**（66.0%）和**高风险动作黑名单**（64.6%）。
3. **Meta-Skill注入**：将这三个维度固化为一个紧凑的meta-skill描述，直接注入提取器的系统提示中，引导技能生成过程。

### Changed Slot：提取器系统提示的先验注入

相比于基线方法，核心changed slot位于**提取器的系统提示**：

| 组件 | 基线值 | 创新值 |
|------|--------|--------|
| 提取器系统提示 | 无额外质量指导，仅要求从经验池中提取通用模式并合并为技能 | 注入meta-skill描述，要求技能内容必须着重体现三项效用验证维度：(1)失败机制编码，(2)可执行的具体步骤，(3)高风险动作禁令 |

这一改变发生在技能提取的早期阶段（Section 6），作为生成时的先验约束，而非事后过滤或重排序。

### 创新效果：一致的性能提升与负迁移缓解

Meta-skill引导提取在全部9个测试单元中均提升了性能，平均增益+1.55 pp（Table 11）。典型结果包括：

- **SpreadsheetBench（GPT-5.4目标）**：从46.17提升至48.50（+2.33 pp）
- **ALFWorld（GPT-5.4目标）**：从75.12提升至76.12（+1.00 pp）
- **SWE-bench-Verified（GPT-5.4目标）**：从69.72提升至70.10（+0.38 pp）
- **SpreadsheetBench（Qwen3.5-35B目标）**：从29.33提升至33.02（+3.69 pp）

相比之下，基于文本合理性的7维rubric在6/9单元中导致性能下降，平均-0.59 pp（Figure 5）。这一对比凸显了创新点的关键性：**效用验证的先验维度远优于人类直觉的文本质量维度**。

### 方法定位：与现有工作的差异

与现有技能提取方法的本质区别在于：

- **Trace2Skill**和**CoEvoSkills**等方法聚焦于提取架构的改进（如子代理舰队、协同进化验证），但未触及技能内容本身的效用维度引导。
- 本研究的创新不改变提取架构或目标模型，而是通过**在提取阶段注入效用验证的先验**，从源头提升技能质量。这一策略具有即插即用的特性，可与现有提取框架兼容。

## 整体框架

本研究构建了一个完整的“轨迹到技能”（trajectory-to-skill）生命周期，系统性地评估模型生成型Agent技能从原始经验到下游消费的全过程。该框架将技能生成与评估解耦为三个顺序阶段，并在每个阶段引入可控的实验变量，以揭示影响技能效用的关键因素。

### 三阶段生命周期

如图1所示，整个pipeline由以下三个阶段构成：

**阶段一：经验生成（Experience Generation）**  
目标模型在训练集上执行任务，产生包含成功和失败轨迹的经验池。每条轨迹记录了模型在具体任务实例上的完整交互序列，包括观察、推理步骤和最终结果。经验池的构成（成功与失败轨迹的比例）是后续技能提取的关键输入变量。

**阶段二：技能提取（Skill Extraction）**  
提取器从经验池中蒸馏出结构化的领域级技能。该阶段采用两层分解架构：首先对每条轨迹独立提取成功或失败模式（per-trajectory pattern extraction），然后通过层次化合并（hierarchical consolidation）将分散的模式递归聚合为单一的统一技能文本。形式化地，提取器 $E$ 将轨迹 $\tau_i$ 映射为模式集 $u_i$：

$$E : \tau_i \longmapsto u_i = \{ p_1, \ldots, p_k \}, \qquad U = \{ u_1, \ldots, u_n \}$$

随后，模式集按组大小 $G$ 递归合并，直至得到单一的统一模式集：

$$U^{(0)} = U, \quad U^{(\ell+1)} = \big\{ \mathrm{MERGE}_E \big( u_{G(j-1)+1}^{(\ell)}, \dots, u_{Gj}^{(\ell)} \big) \big\}_j, \; \mathrm{until} |U^{(L)}| = 1$$

**阶段三：技能消费（Skill Consumption）**  
提取的技能被注入目标模型的系统提示，在留出测试集上评估性能变化。技能效用通过下游任务的实际性能增益来量化，而非依赖对技能文本质量的主观判断。

### 核心评估指标

为解耦提取器与目标模型各自的贡献，研究引入两个互补指标：

- **提取效能（Extraction Efficacy, EE）**：固定提取器 $E$ 在不同目标模型上的平均性能增益，衡量提取器产生有用技能的可靠性。
  
  $$\operatorname{EE}(E, \mathcal{D}) = \frac{1}{|\mathcal{M}|} \sum_{M \in \mathcal{M}} \Delta(E, M, \mathcal{D})$$

- **目标可进化性（Target Evolvability, TE）**：固定目标模型 $M$ 使用不同提取器生成的技能所获得的平均增益，衡量目标模型从技能中受益的能力。
  
  $$\mathrm{TE}(M, \mathcal{D}) = \frac{1}{|\mathcal{E}|} \sum_{E \in \mathcal{E}} \Delta(E, M, \mathcal{D})$$

其中 $\Delta(E, M, \mathcal{D})$ 为技能注入带来的性能变化：

$$\Delta(E, M, \mathcal{D}) = \mathrm{Perf}(M \mid S_{E, M, \mathcal{D}}, Q_{\mathcal{D}}^{\mathrm{test}}) - \mathrm{Perf}(M \mid Q_{\mathcal{D}}^{\mathrm{test}})$$

### 关键发现与干预机制

初步实验揭示了一个核心矛盾：模型生成的技能在约75%的提取-目标配对中带来正向增益，但25%的配对出现负迁移（$\Delta < 0$），其中ALFWorld域的负迁移率高达47%（Table 1）。进一步分析表明，技能的表面文本特征（格式、文本合理性）无法可靠预测其效用——技能格式对下游性能无显著影响（Friedman检验，所有目标 $p>0.34$），而未引导的LLM法官评价技能质量的准确率仅为46.4%，接近随机基准。

真正决定技能效用的，是技能文本中是否编码了领域特定的失败机制、可执行的对策以及高风险行为禁令。基于这一发现，研究引入**Meta-Skill引导提取**：在提取阶段的系统提示中注入一个简短的meta-skill描述，要求技能内容必须着重体现三项经过效用验证的维度——（1）失败机制编码，（2）可执行的具体步骤，（3）高风险动作禁令。这一干预在不改变模型或任务的情况下，一致地提升了所有测试单元的性能。

## 核心模块与公式推导

### 技能生成生命周期的三阶段流水线

本研究将“轨迹到技能”的完整过程抽象为三个顺序模块，构成统一的评估框架（Figure 1）：

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2605_23899/figures/001_Figure_1.jpg]]
*Figure 1: Overview of our study design. We evaluate the full trajectory-to-skill lifecycle across three stages: experience generation, skill extraction, and skill consumption*

**模块一：经验生成（Experience Generation）**
目标模型 $M$ 在任务域 $\mathcal{D}$ 的训练分割 $Q_{\mathcal{D}}^{\text{train}}$ 上执行任务，产生包含成功与失败轨迹的经验池 $T_{M,\mathcal{D}}$。每条轨迹 $\tau_i$ 记录模型在具体任务实例上的完整交互历史，包括观察、动作和最终结果。经验池的构成（成功与失败轨迹的比例）是后续技能质量的关键上游因素。

**模块二：技能提取（Skill Extraction）**
提取器 $E$ 将经验池中的轨迹集合转化为单一的结构化技能文本 $S_{E,M,\mathcal{D}}$。该模块采用两阶段分解架构：
- **逐轨迹模式提取**：对每条轨迹 $\tau_i$ 独立分析，输出一组成功或失败模式 $u_i = \{p_1, \ldots, p_k\}$，形成所有轨迹的模式集 $U = \{u_1, \ldots, u_n\}$。
- **层次化合并**：将模式集按组大小 $G$ 递归合并，直到得到统一的模式集。设 $U^{(0)} = U$，第 $\ell+1$ 层的合并操作为：
$$U^{(\ell+1)} = \big\{ \mathrm{MERGE}_E \big( u_{G(j-1)+1}^{(\ell)}, \dots, u_{Gj}^{(\ell)} \big) \big\}_j, \quad \text{直到 } |U^{(L)}| = 1$$
最终技能 $S$ 由唯一的合并模式集 $U^{(L)}$ 经最终合成步骤生成。

**模块三：技能消费（Skill Consumption）**
所提取的技能 $S$ 被注入目标模型的系统提示（采用单技能注入模板，见 Table 5），在留出测试集 $Q_{\mathcal{D}}^{\text{test}}$ 上评估性能变化。技能注入不改变模型参数，仅通过上下文指令影响模型的推理与决策。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2605_23899/figures/007_Table_5.jpg]]
*Table 5: Single-skill injection prompt template*

**模块四：元技能注入（Meta-Skill Injection）**
在提取阶段的系统提示中注入经过效用验证的元技能先验，要求提取器在生成技能内容时着重体现三个关键维度：（1）失败机制编码，（2）可执行的具体步骤，（3）高风险动作禁令。该模块作为提取阶段的即插即用增强，不改变下游消费流程。

---

### 核心评估公式

**性能增益 $\Delta$**
技能注入对目标模型 $M$ 在测试集上的性能改变定义为：
$$\Delta(E, M, \mathcal{D}) = \mathrm{Perf}(M \mid S_{E, M, \mathcal{D}}, Q_{\mathcal{D}}^{\text{test}}) - \mathrm{Perf}(M \mid Q_{\mathcal{D}}^{\text{test}})$$
其中 $\mathrm{Perf}(M \mid \cdot)$ 表示模型 $M$ 在给定条件下的任务准确率。$\Delta > 0$ 表示正向迁移，$\Delta < 0$ 表示负迁移。

**提取效能 EE（Extraction Efficacy）**
固定提取器 $E$ 在不同目标模型集 $\mathcal{M}$ 上的平均性能增益：
$$\operatorname{EE}(E, \mathcal{D}) = \frac{1}{|\mathcal{M}|} \sum_{M \in \mathcal{M}} \Delta(E, M, \mathcal{D})$$
该指标衡量提取器生成技能的跨模型鲁棒性。

**目标可进化性 TE（Target Evolvability）**
固定目标模型 $M$ 使用不同提取器集 $\mathcal{E}$ 的技能所获得的平均增益：
$$\mathrm{TE}(M, \mathcal{D}) = \frac{1}{|\mathcal{E}|} \sum_{E \in \mathcal{E}} \Delta(E, M, \mathcal{D})$$
该指标衡量目标模型从技能中受益的整体能力，反映模型自身的技能利用潜力。

**$\sigma$-ratio（效应量指标）**
用于量化实验因素（如格式、提取器选择）相对于评估轮次噪声的效应大小：
$$\sigma\text{-ratio} = \sigma_{\mathrm{factor}} / \sigma_{\mathrm{round}}$$
当 $\sigma$-ratio > 1 时，表明该因素的效应超过了评估的随机波动，具有统计意义上的实质性影响。该指标在格式效应分析（Table 8）中用于证明格式选择的影响不显著（所有目标的 $\sigma$-ratio 均未超过噪声阈值），而提取器选择的影响显著。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2605_23899/figures/005_Figure_5.jpg]]
*Figure 5: Effect of meta-skill guidance on downstream skill utility. The plausibility rubric hurts most times, while the validated rubric improves all the generated skills compared with original skill*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2605_23899/figures/006_Figure_4.jpg]]
*Figure 4: Cross-model skill transfer. Strong-pool and weakpool skills are injected into each target separately*

## 实验与分析

### 主结果：技能效用的全局图景

本研究在五个任务领域（ALFWorld、SpreadsheetBench、SWE-bench-Verified、SEAL-0、BFCL-v4）上，对模型生成技能的完整生命周期进行了系统性评估。核心发现是：**模型生成的技能在75%的提取-目标配对中带来了正向增益，但25%的配对出现了负迁移（Δ<0）**（Table 1）。这一结果揭示了技能提取方法的一个关键瓶颈——即使平均效用为正，负迁移风险在部分领域依然严重。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2605_23899/figures/002_Table_1.jpg]]
*Table 1: Skill-induced performance gain (∆) across domains. Base is the no-skill baseline. TE denotes Target Evolvability, averaged across extractors, and EE denotes Extraction Efficacy, averaged across targets. Green: ∆ > 0; Red: ∆ \< 0*

各领域的脆弱性差异显著。SpreadsheetBench和SWE-bench-Verified的负迁移率最低（13%），而ALFWorld作为具身交互域最为脆弱，负迁移率高达47%。这一差异暗示，**技能效用在很大程度上取决于领域特性与技能内容之间的匹配度**，而非技能文本的表面质量。

从提取器与目标模型的交互视角看，两个解耦指标——Extraction Efficacy（EE，固定提取器在不同目标上的平均增益）和Target Evolvability（TE，固定目标使用不同提取器技能的平均增益）——揭示了不对称性：某些目标模型（如GPT-5.4）在SpreadsheetBench上的TE可达+9.66 pp，而同一提取器在不同目标上的EE波动显著，说明**技能消费阶段的目标模型利用能力是效用的重要调节因素**。

### 生命周期各阶段的归因分析

#### 经验生成阶段：成功与失败的配比是关键

为隔离经验池组成的影响，研究通过直接操纵池中成功轨迹的比例（100%、75%、50%、25%、0%）并固定提取器（GPT-5.4-mini）进行实验（Figure 2）。结果一致表明：**全失败轨迹池产生的技能质量最差**，但最优成功-失败比例因域而异——SpreadsheetBench偏好高成功率池，而ALFWorld反而在高失败率池下表现更好。这一发现说明，失败轨迹中编码的领域特定失败机制和规避策略，在某些场景下比成功模式更具信息价值。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2605_23899/figures/003_Figure_2.jpg]]
*Figure 2: Effect of success ratio in the experience pool on downstream tasks*

#### 技能提取阶段：格式无关，内容决定效用

一个反直觉的发现是：**技能文本的格式（有序列表、无序列表、检查表、散文）对下游任务性能无显著影响**。通过将同一技能改写为四种规范格式并重新评估，Friedman检验在所有目标模型上均未检测到显著差异（所有p>0.34，Table 8）。相比之下，提取器的选择具有显著影响（p<0.01 for 5/6 targets），σ-ratio分析进一步证实提取器效应远超评估噪声。这直接否定了“格式优化可以提升技能质量”的直觉假设，将问题焦点锁定在**技能内容的实质性维度**上。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2605_23899/figures/009_Table_8.jpg]]
*Table 8: Format vs. extractor effect on SpreadsheetBench. σ-ratio = $\sigma _ { \mathrm { f a c t o r } } / \sigma _ { \mathrm { r o u n d } }$ ; values >1 indicate the factor exceeds noise

进一步地，未经训练的LLM法官在技能质量评估上表现堪忧。在成对比较任务中，LLM法官选择更优技能的总体准确率仅为46.4%（随机基准50%），且准确性随性能差距增大而**下降**——在Δ≥5 pp的高差距对上，准确率降至15.8%（Figure 3）。这一反直觉的下降趋势表明，**表面文本特征（如条理性、专业性）不仅无法预测技能效用，甚至可能在高差距场景下产生系统性误导**。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2605_23899/figures/004_Figure_3.jpg]]
*Figure 3: Pairwise selection accuracy by δ*

#### 技能消费阶段：跨模型迁移的不对称性

跨模型技能迁移实验（Figure 4）揭示了技能消费的另一个关键维度：**同一技能文本对不同目标模型的增益差异显著**。强模型池提取的技能注入弱模型时，并不总是带来正向迁移；反之亦然。这表明技能效用并非技能文本的固有属性，而是技能内容与消费者模型能力之间的**交互产物**。

### 效用驱动维度的发现与验证

为识别真正驱动技能效用的文本维度，研究设计了一个全自动化的rubric发现管道：从交叉矩阵中选取高Δ差距的技能对，由GPT-5.4分析每对差异，经迭代合并后形成七个候选维度（raw rubric，Table 13）。随后，通过大规模成对比较验证每个维度与下游效用的对齐程度，发现三个维度具有显著的一致性：

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2605_23899/figures/012_Table_13.jpg]]
*Table 13: Seven dimensions of the raw rubric, discovered via the automated contrastive pipeline. Better-rate measures alignment with downstream utility; the three bold dimensions form the validated rubric used for guided evaluation and meta-skill extraction*

- **失败机制编码**（better-rate 65.5%）：技能是否明确指出典型失败模式及其成因
- **可执行细节**（better-rate 66.0%）：是否提供可操作的具体步骤，而非抽象建议
- **高风险动作黑名单**（better-rate 64.6%）：是否明确禁止已知的危险操作

这三个维度的better-rate均显著高于随机水平（50%），而其余四个维度（如文本条理性、领域知识覆盖度）的对齐率接近随机。

### 干预实验：Meta-Skill引导提取

将上述三个验证维度固化为提取阶段的meta-skill先验，注入提取器的系统提示中，在全部9个测试单元（3个域 × 3个目标模型）上进行评估（Table 11，Figure 5）：

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2605_23899/figures/011_Table_11.jpg]]
*Table 11: Effect of meta-skill guidance on downstream skill utility (accuracy %). The plausibility-based rubric (all 7 dimensions, unscreened) hurts on average; the utility-validated rubric (3 screened dimensions) improves all nine cells*

- **效用验证rubric（3维度）**：在所有9个单元中均提升了性能，平均增益+1.55 pp。典型提升包括SpreadsheetBench GPT-5.4从46.17%提升至48.50%（+2.33 pp），Qwen3.5-35B从29.33%提升至33.02%（+3.69 pp）。
- **文本合理性rubric（7维度，未经筛选）**：在6/9单元中导致性能下降，平均Δ为-0.59 pp。

这一对比有力地证明了：**基于表面文本质量的引导不仅无效，反而有害；只有经过效用验证的实质性维度才能一致地提升技能质量**。同时，rubric引导也将LLM法官的成对选择准确率从46.4%提升至73.8%，进一步验证了这些维度在技能评估中的有效性。

### 失败模式与负迁移分析

负迁移现象呈现明显的领域聚集性。ALFWorld域47%的负迁移率与其具身交互特性密切相关——该域要求精确的动作序列和状态操作，而常规提取往往输出泛泛而谈的指导（如“理解目标”、“找到瓶颈”），缺乏可执行的动作模式。对比案例（Table 15）显示，高Δ技能提供了三个针对ALFWorld机制定制的可执行动作模式：深度检查（显式打开封闭容器）、主动状态转换（定位-获取-运输-调用的具体管道）、前置条件解决（在尝试放置前先导航并打开目的地）。低Δ技能描述了相同的高层逻辑，但抽象层次无法映射到ALFWorld的动作词汇表，迫使agent自行重新发现操作细节。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2605_23899/figures/015_Table_15.jpg]]
*Table 15: Analysis. The higher-∆ skill provides three executable action patterns tailored to ALFWorld’s mechanics: (1) deep inspection—explicitly open closed containers rather than assuming visibility equals absence; (2) active state transformations—a concrete locate-acquire-transport-invoke pipeline for state changes; (3) prerequisite resolution—navigate and open destinations before attempting placement. The lower-∆ skill describes the same high-level logic (“ground the goal,” “find the bottleneck,” “manage preconditions”) but at a level of abstraction that does not map onto ALFWorld’s action vocabulary, leaving the agent to rediscover the operational details on its own. Table 15 Contrastive case: A...*

这一失败模式揭示了当前技能提取方法的根本局限：**常规提取倾向于输出抽象指导，而真正决定效用的是技能中是否编码了领域特定的失败机制、可执行对策和高风险行为禁令**。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2605_23899/figures/008_Table_6.jpg]]
*Table 6: Multi-skill injection prompt template (text-mode skill tool protocol). Table 7 Default extraction hyperparameters*

## 方法谱系与知识库定位

### 技能提取方法谱系

本研究提出的 **Meta-Skill Guided Extraction** 处于“从轨迹中蒸馏可复用技能”这一新兴范式的核心位置。与现有工作相比，其关键区别在于提取阶段引入了经过下游效用验证的先验知识（meta-skill），而非依赖文本表面质量或启发式合并策略。

**Trace2Skill** 是该方向的重要前置工作，采用子代理舰队（sub-agent fleet）从轨迹中提取模式并进行冲突消解，最终合并为统一技能。其核心假设是：通过多代理投票和冲突消解可以提升技能质量。然而本研究的系统分析表明，这一假设存在根本性局限——未经下游效用验证的LLM法官在技能对选择任务上的准确率仅为46.4%（接近随机基准50%），且在高性能差距对（Δ≥5 pp）上进一步降至15.8%（Figure 3）。这意味着仅依赖LLM自身判断的合并策略无法可靠地区分高效用与低效用技能。

**CoEvoSkills** 采用协同进化验证框架对技能包进行迭代精炼，其核心思路是通过多轮验证-更新循环逐步提升技能质量。该方法与本研究共享“技能需要验证”的基本直觉，但其验证依赖任务执行反馈，而本研究进一步揭示了反馈信号的结构化维度（失败机制编码、可执行细节、高风险动作黑名单），并将这些维度前移至提取阶段作为生成先验，从而在源头提升技能质量，而非仅在事后筛选。

在更广泛的Agent技能学习文献中，多数工作聚焦于技能消费阶段的提示工程或检索增强。本研究的方法论贡献在于将问题前移：通过系统性地解耦经验生成、技能提取和技能消费三个生命周期阶段，揭示了技能效用瓶颈主要存在于提取阶段——常规提取倾向于输出泛泛而谈的指导，而真正决定效用的是技能中是否编码了领域特定的失败机制、可执行对策和高风险行为禁令。

### 方法适用边界

本方法的有效性已在五个特定任务领域得到验证：**ALFWorld**（具身交互）、**SpreadsheetBench**（生产力工具）、**SWE-bench-Verified**（软件工程）、**SEAL-0** 和 **BFCL-v4**（函数调用）。在这些领域中，meta-skill引导的提取在所有9个测试单元（3个领域 × 3个目标模型）上均实现了正向增益，平均提升+1.55 pp（Table 11）。

然而，方法的适用边界同样清晰：

1. **领域泛化性待验证**：当前实验覆盖的任务领域均为相对结构化的单代理场景。在开放域规划、多代理协作或动态环境交互等更复杂场景中，meta-skill中编码的三个维度（失败机制编码、可执行细节、高风险动作黑名单）是否仍然充分，仍需进一步检验。

2. **单技能注入假设**：实验采用单技能注入策略，即每个领域仅提取一个统一技能并注入系统提示。在大规模技能库场景下，技能选择、组合和干扰缓解问题尚未涉及。当存在多个可能冲突的技能时，meta-skill引导能否保持一致性提升仍是开放问题。

3. **执行框架依赖性**：技能效用评估基于固定的执行框架（固定脚本式执行）。当更换为更复杂的agent harness（如带规划器或检索增强的框架）时，技能效用的稳定性需要独立检验。Table 10报告了在Claude Code和Codex等交互式工具使用框架下的初步结果，但结论的稳健性仍需更多验证。

4. **经验池质量依赖**：消融实验（Figure 2）表明，全失败轨迹池产生的技能质量最差，且最优成功-失败比例因领域而异。这意味着方法在经验池质量极低（如全部为失败轨迹）的场景下可能失效。

### 局限与开放问题

**已识别的核心局限**：

- **负迁移风险未根除**：尽管meta-skill引导一致提升了所有测试单元的性能，但负迁移的根本原因——目标模型对同一技能文本的利用差异——并未被消除。在ALFWorld域，负迁移率高达47%（Table 1），即使平均效用为正，实际部署仍需逐案测试。
- **安全性维度缺失**：当前框架未涉及技能安全性评估。实际部署中，从经验池提取的技能可能编码了不安全行为模式或偏见，而meta-skill中的三个维度并未覆盖安全性约束。
- **评估成本高昂**：技能效用只能通过下游任务的实际性能来评估，无法依赖文本质量的主观判断。这意味着任何技能选择或迭代优化都需要完整的任务执行评估，计算成本显著。

**关键开放问题**：

1. **无样本效用预测**：能否开发仅基于技能文本（无需下游评估样本）就能预测技能效用的方法？当前LLM法官的46.4%准确率表明这是一个极具挑战性的问题，但rubric引导将准确率提升至73.8%（Figure 3）提示了结构化维度评估的潜力。

2. **技能兼容性机制**：目标模型对同一技能文本的利用差异能否通过微调或指令调整来缩小？跨模型技能迁移实验（Figure 4）显示强模型池技能对弱目标的增益有限，暗示存在模型能力与技能复杂度的匹配问题。

3. **技能持续进化**：在模型不断更新的场景下，技能的版本管理和持续进化策略是什么？当经验池随模型能力提升而更新时，meta-skill本身是否需要同步演化？

4. **多技能组合优化**：面对大规模技能库时，如何设计技能选择、组合与干扰缓解机制？单技能注入的成功并不能直接推广到多技能场景，技能间的交互效应可能引入新的失效模式。

5. **安全性系统集成**：如何将安全性评估系统性地融入当前框架，在不牺牲效用的前提下避免生成带有偏见或危险的指导？这可能需要扩展meta-skill的维度集合，纳入安全性相关的约束维度。

## 原文 PDF

![[paperPDFs/arxiv_2026/From_Raw_Experience_to_Skill_Consumption_A_Systematic_Study_of_Model_Generated_Agent_Skills.pdf]]
