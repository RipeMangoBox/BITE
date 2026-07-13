---
title: "Benchmarking Empirical Privacy Protection for Adaptations of Large Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Benchmarking_Empirical_Privacy_Protection_for_Adaptations_of_Large_Language_Models.pdf
project_link: null
code_link: null
openreview_forum_id: jY7fAo9rfK
aliases:
- BEPPALLM
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning
core_operator: "适配数据与预训练数据之间的分布关系（完全重叠、IID、OOD）以及所选的DP适配方法（如全微调、LoRA、前缀微调等）。"
primary_logic: "分布接近性是隐私泄露的主要驱动因素；IID数据泄露程度与重叠数据相似，说明即使无重叠，分布接近也会削弱DP保护。LoRA在多数场景下提供最佳的隐私‑效用权衡。"
claims:
- "分布变化强烈影响隐私脆弱性：适配数据越接近预训练分布，在相同理论保障下的实际隐私风险越高，即使没有直接数据重叠。"
- "IID数据（预训练验证集）的泄露程度与直接重叠数据相似，揭示了分布接近性是风险的主要驱动因素。"
- "LoRA在OOD数据上实现最高的经验隐私保护，且在整个实验中始终提供最佳的隐私‑效用权衡。"
- "即使在中等隐私预算（如ε=8）下，敏感适配数据仍面临显著的实际成员推断攻击威胁。"
---

# Benchmarking Empirical Privacy Protection for Adaptations of Large Language Models

> [!tip] 核心洞察
> 分布接近性是隐私泄露的主要驱动因素；IID数据泄露程度与重叠数据相似，说明即使无重叠，分布接近也会削弱DP保护。LoRA在多数场景下提供最佳的隐私‑效用权衡。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 大型语言模型适配的经验隐私保护基准评估 |
| 英文题名 | Benchmarking Empirical Privacy Protection for Adaptations of Large Language Models |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=jY7fAo9rfK) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning |
| Method | 预训练‑适配管道的整体隐私审计框架与基准 |
| Dataset | SAMSum (OOD), GermanWiki (OOD), GermanWiki (ε=8, 超参数搜索), OOD平均 (ε=8) |

> [!tip] 效果简介
> - SAMSum (OOD) 上，RMIA AUC (Shadow) 为 LoRA ε=8: 0.69，对比 Full Fine-Tune ε=8: 0.82，变化 -0.13。
> - GermanWiki (OOD) 上，RMIA AUC (Shadow) 为 LoRA ε=8: 0.59，对比 Head Fine-Tune ε=8: 0.76，变化 -0.17。
> - GermanWiki (ε=8, 超参数搜索) 上，隐私‑效用权衡 (AUC vs Perplexity) 为 LoRA: AUC 0.77 @ Perplexity 14.27，对比 Full Fine-Tune: AUC 0.82 @ Perplexity 14.60，变化 更低AUC。

## 概要

大型语言模型（LLM）在隐私敏感领域的适配通常依赖差分隐私（DP）提供理论保障，但理论保障与实际经验隐私风险之间的关系尚不明确。本文提出了一个面向预训练-适配范式的整体隐私审计框架，系统评估了不同DP适配方法在多种数据分布场景下的经验隐私保护效果。

**核心发现**：适配数据与预训练数据之间的分布关系是隐私泄露的主要驱动因素。即使没有直接的数据重叠，分布越接近预训练数据，在相同理论DP保障下的实际隐私风险越高。令人惊讶的是，来自预训练验证集的IID（同分布）数据的泄露程度与直接重叠数据相似，这揭示了分布接近性而非数据重叠才是风险的根本来源。

**方法定位**：在适配方法谱系中，参数高效微调方法（尤其是**LoRA**）在多数场景下提供了最佳的隐私-效用权衡——在OOD（分布外）数据上实现最高的经验隐私保护，同时保持较低的逐字记忆率。相比之下，全微调和Prefix Tuning在非隐私场景下泄露风险更高。即使在中等隐私预算（如ε=8）下，敏感适配数据仍面临显著的成员推断攻击威胁，这提示实践中需要更审慎的隐私预算选择。

**主要结果概览**：在OOD适配场景下，LoRA在ε=8时的RMIA攻击AUC（0.64平均）显著低于Head Fine-Tune（0.87平均）和Full Fine-Tune（0.82）。在IID场景下，所有方法的隐私风险均显著上升，进一步验证了分布接近性的核心作用。消融研究表明，使用至少一个影子模型对RMIA攻击至关重要，而Prefix Tuning在降低预训练数据逐字记忆方面表现突出。



大型语言模型（LLM）的“预训练‑适配”范式已成为主流：先在超大规模公开语料上预训练，再在下游任务数据上微调或适配。当适配数据涉及隐私敏感领域（如医疗、金融、个人对话），直接的适配会暴露训练样本，差分隐私（DP）适配应运而生。然而，现有的DP适配研究存在一个根本性盲区——**它们几乎从未系统考察适配数据与预训练数据之间的分布关系如何影响实际隐私保护效果**。

### 现有方法的缺口

当前DP适配的评估体系存在三重断裂：

1. **审计范围孤立**：隐私审计通常局限于单独的预训练阶段或单独的适配阶段，缺乏对“预训练→适配”全流程中数据依赖关系的整体考量。适配模型不仅可能泄露适配数据本身，还可能改变预训练数据的保护程度，而这两者之间的交互效应长期被忽视。

2. **分布假设缺失**：现有工作默认适配数据与预训练数据是独立同分布（IID）或完全无关的，但真实场景中适配数据可能落在从“完全重叠”到“完全OOD”的连续谱系上。例如，用同一领域的验证集适配模型（IID）与用跨语言、跨领域数据适配（OOD），其隐私风险机制截然不同。这一维度尚未被系统建模。

3. **攻击强度不足**：多数研究依赖较弱的成员推断攻击（MIA），而当前最强的RMIA攻击（Zarifzadeh et al., 2024）在DP适配场景下的有效性尚未被充分基准测试。弱攻击会低估真实风险，导致对DP保障的过度信任。

### 核心动机

本文的核心动机在于揭示一个被理论保障掩盖的经验事实：**即使数学上满足相同的(ε, δ)-DP保障，适配数据的实际隐私风险会因其与预训练数据的分布接近程度而发生数量级的变化**。这意味着，在IID场景下，即使适配数据与预训练数据没有直接重叠，其泄露程度也可能接近完全重叠的情况——分布接近性本身就是隐私泄露的主要驱动因素。

这一洞察直接挑战了当前DP适配的评估范式：仅报告ε值不足以表征实际保护水平，必须将预训练‑适配分布关系纳入审计框架。为此，本文提出一个整体隐私审计框架，覆盖预训练审计、适配审计、联合审计和适配后预训练审计四个阶段，并系统评估从完全重叠到完全OOD的完整分布谱系下的隐私风险。



## 核心方法与创新机理

本工作的核心创新不在于提出一种新的差分隐私适配算法，而在于构建了首个**预训练‑适配管道的整体隐私审计框架**，并基于该框架揭示了现有DP适配方法在实际隐私保护中的关键瓶颈。其创新性主要体现在以下两个维度的范式转变。

### 从单阶段审计到四阶段整体审计框架

已有隐私审计工作通常将预训练与适配视为独立过程分别审计，忽略了二者之间的数据依赖与隐私耦合。本工作将审计视角扩展为覆盖整个预训练‑适配生命周期的四个阶段（Figure 5）：

- **阶段1：预训练审计**——审计预训练数据是否从已适配的LLM中泄露；
- **阶段2：适配审计**——审计适配数据是否从已适配的LLM中泄露；
- **阶段3：联合审计**——评估预训练数据与适配数据在已适配LLM中的联合泄露；
- **阶段4：适配后预训练审计**——评估DP适配对预训练数据保护程度的影响。

这一框架的形式化定义将成员推断博弈从单一数据集扩展为同时考虑预训练数据 $S$ 与适配数据 $D$ 的对抗设定，并通过零假设与备择假设的显式建模（如预训练审计的 $H_0: a=0$ vs $H_A: a=1$，适配审计的 $H_0: b=0$ vs $H_A: b=1$），为预训练‑适配范式的隐私审计提供了统一的分析语言。

### 从理论DP保障到分布驱动的经验隐私评估

已有DP适配研究通常以理论隐私预算 $\varepsilon$ 作为安全保障的充分条件，未系统考察适配数据与预训练数据之间的分布关系对实际隐私泄露的影响。本工作首次系统评估了从**完全重叠**到**IID**再到**完全OOD**的完整分布谱系，并发现了一个关键因果机制：

> **分布接近性是隐私泄露的主要驱动因素**：适配数据越接近预训练分布，在相同理论保障下的实际隐私风险越高，即使没有直接数据重叠。

这一发现的核心证据来自两个层面：其一，IID数据（预训练验证集）的泄露程度与直接重叠数据相似，表明分布接近性本身即可显著削弱DP保护；其二，Wasserstein距离（Table 1）作为分布偏移的实证量化指标，与成员推断攻击AUC之间存在系统关联——OOD数据集（如SAMSum的Wasserstein距离0.0250、GermanWiki的0.0556）的泄露程度普遍低于IID/重叠数据集（如Bookcorpus2 Train的0.0171）。

基于这一框架，本工作进一步识别出**LoRA在多数场景下提供最佳的隐私‑效用权衡**：在OOD数据上，LoRA（$\varepsilon=8$）的RMIA AUC仅为0.69（SAMSum）和0.59（GermanWiki），显著低于Full Fine-Tune的0.82和Head Fine-Tune的0.76；在隐私‑效用曲线上（Figure 4），LoRA在相同困惑度下始终维持更低的AUC。这一结论并非来自新算法的设计，而是通过统一的审计框架对现有方法进行公平比较后的经验发现，为DP适配方法的选择提供了分布感知的决策依据。

需要注意的是，该框架目前仅完整实现了适配审计和适配后预训练审计两个阶段，联合审计的完整方法论仍为开放问题；此外，评估范围限于可进行DP适配的开源模型（Pythia、GPT-Neo、OLMo），尚未覆盖闭源大模型。



![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_jY7fAo9rfK/figures/010_Figure_5.jpg]]
*Figure 5: Stages of Auditing. We analyze four stages of auditing: 1 Auditing Pretraining, 2 Auditing Adaptation, 3 Joint Auditing of Pretraining and Adaptations, 4 Post-Adaptation Auditing of the Pretraining. Figure 6: Setup for Joint Adaptation Auditing (3). We consider different datasets for pretraining and adaptation and the two separate training stages, distinguishing it from standard ML privacy auditing*

本研究构建了一个面向**预训练‑适配范式**的整体隐私审计框架，将审计过程划分为四个阶段，系统覆盖从预训练到适配后全生命周期的隐私风险评估（Figure 5）。该框架的核心创新在于将传统单一阶段的审计扩展为多阶段联合分析，并显式建模适配数据与预训练数据之间的分布关系对隐私泄露的影响。

### 审计四阶段

**阶段1：预训练审计（Auditing Pretraining）** 评估预训练数据是否从已适配的LLM中泄露。攻击者猜测样本 $x$ 是否在预训练数据 $S$ 中，对应的假设检验为：

$$H_0 : a = 0 \qquad H_A : a = 1$$

其中 $a=0$ 表示样本不在预训练数据中，$a=1$ 表示在。

**阶段2：适配审计（Auditing Adaptation）** 评估适配数据是否从已适配的LLM中泄露。攻击者猜测样本 $x$ 是否在适配数据 $D$ 中：

$$H_0 : b = 0 \qquad H_A : b = 1$$

其中 $b=0$ 表示样本不在适配数据中，$b=1$ 表示在。这一阶段是现有工作最常关注的审计维度。

**阶段3：联合审计（Joint Auditing of Pretraining and Adaptations）** 评估预训练数据和适配数据在已适配LLM中的联合泄露。这一阶段考虑了预训练和适配两个训练阶段的复合效应，区别于标准机器学习隐私审计的单阶段设置（Figure 6）。联合审计的假设检验涉及对 $(a, b)$ 状态的联合推断。

**阶段4：适配后预训练审计（Post-Adaptation Auditing of the Pretraining）** 评估适配过程对预训练数据保护程度的影响。由于预训练通常缺乏形式化的隐私保障，这一阶段旨在揭示适配操作是否会削弱或增强对预训练数据的保护。对应的假设检验为：

$$H_0 : (a, b) = (0, 0) \qquad H_A : (a, b) = (1, 0)$$

即攻击者判断样本是否仅在预训练数据中出现而未在适配数据中出现。

### 分布关系谱系

框架的另一个关键设计是**系统评估适配数据相对于预训练数据的完整分布谱系**——从完全重叠、IID（独立同分布）到完全OOD（分布外）。这一设计直接回应了核心研究发现：分布接近性是隐私泄露的主要驱动因素。实验通过Wasserstein距离实证量化了不同数据集的分布偏移程度（Table 1），其中Pile相关数据集（Bookcorpus、GitHub、Enron）距离较低，而OOD数据集（SAMSum、GermanWiki）距离显著更高。

### 攻击方法体系

框架采用**RMIA（Robust Membership Inference Attack）** 作为主要攻击手段，这是当前针对LLM隐私审计的最强威胁模型，并辅以数据提取攻击（金丝雀暴露度评估）进行补充验证。同时引入Reference方法和Min-K%作为基线攻击，其中Min-K%作为无参考模型基线提供对比视角。金丝雀暴露度评估中，采用采样和分布建模两种近似方法估计暴露度，当使用256个非成员金丝雀时两种方法性能相似，框架采用采样方法以提高效率。

### 输入输出流

整个审计框架的输入包括：预训练LLM、适配数据集（按分布关系分类）、隐私预算 $\varepsilon$ 及适配方法选择。输出包括：各阶段的成员推断AUC分数、金丝雀暴露度、逐字记忆样本数量，以及隐私‑效用权衡曲线（以困惑度为效用代理，经Rouge-1验证有效）。框架通过统一的预训练基座模型和一致的攻击设置，确保不同适配方法之间的公平比较。



### 差分隐私适配的形式化定义

论文所评估的所有私有适配方法均建立在差分隐私（Differential Privacy, DP）的理论框架之上。其核心定义为：对于任意相邻数据集 $D$ 和 $D'$（仅相差一条记录），随机机制 $\mathcal{M}$ 满足 $(\varepsilon, \delta)$-差分隐私，当且仅当：

$$\operatorname* { P r } [ \mathcal { M } ( D ) \in S ] \leq e ^ { \varepsilon } \cdot \operatorname* { P r } [ \mathcal { M } ( D ^ { \prime } ) \in S ] + \delta .$$

其中 $\varepsilon$ 为隐私预算（值越小保护越强），$\delta$ 为失败概率。所有被评估的适配方法——包括 **Full DP Fine-Tuning**（Li et al., 2022）、**Head DP Fine-Tuning**（Li et al., 2022）、**DP-LoRA**（Hu et al., 2022; Yu et al., 2022）、**DP-Prefix Tuning**（Liu et al., 2021; Duan et al., 2023a）以及 **DP Prompting**（Duan et al., 2023a）——均通过 DPSGD（Abadi et al., 2016）或其变体实现该保障，即在梯度下降过程中对梯度进行裁剪并注入高斯噪声。

### 隐私审计的攻击工具：RMIA 与暴露度

为量化经验隐私泄露，论文以 **RMIA（Robust Membership Inference Attack）**（Zarifzadeh et al., 2024）作为主要审计工具，并辅以数据提取攻击中的**金丝雀暴露度（Canary Exposure）** 指标。

**RMIA 分数** 定义为目标样本 $x$ 相对于总体样本 $z$ 的似然比超过阈值 $\gamma$ 的概率：

$$\mathrm { S c o r e } _ { \mathrm { M I A } } ( x ; \theta ) = \mathrm { P r } _ { \pi } \left( \mathbf { L R } _ { \theta } ( x , z ) \geq \gamma \right)$$

该攻击利用影子模型（shadow models）来校准目标模型的输出分布，从而判断某一样本是否属于适配训练集。消融实验表明，使用至少一个影子模型对 RMIA 至关重要，尤其在 DP 适配场景下，无影子模型时攻击性能接近随机（Figure 11）；参数 $\gamma = 1$ 通常是最佳选择（Figure 14）。

**金丝雀暴露度** 衡量攻击者对目标样本 $z$ 的排名能力：

$$\mathbf { e x p o s u r e } ( z , \hat { Z } ) = \log _ { 2 } | \mathcal { U } | - \log _ { 2 } \bigl ( \mathrm { r a n k } ( z ; \hat { Z } ) \bigr ) .$$

其中 $\mathcal{U}$ 为候选全集，$\hat{Z}$ 为攻击者的排名列表。暴露度越高，表示目标样本排名越靠前，泄露风险越大。论文通过在适配数据中插入对抗性金丝雀，并采用两种近似方法（采样与分布建模）来估计暴露度；当使用 256 个非成员金丝雀时，两种方法性能相似（Figure 13）。

### 整体审计框架的四阶段结构

论文的核心方法论贡献在于形式化了一个面向“预训练‑适配”范式的整体隐私审计框架，包含四个阶段（Figure 5）：

1. **阶段1：预训练审计（Auditing Pretraining）**  
   审计预训练数据是否从已适配的 LLM 中泄露。零假设与备择假设为：
   $$H_0 : a = 0 \qquad H_A : a = 1$$
   其中 $a=0$ 表示样本 $x$ 不在预训练数据 $S$ 中，$a=1$ 表示在。

2. **阶段2：适配审计（Auditing Adaptation）**  
   审计适配数据是否从已适配的 LLM 中泄露。假设检验为：
   $$H_0 : b = 0 \qquad H_A : b = 1$$
   其中 $b=0$ 表示样本 $x$ 不在适配数据 $D$ 中，$b=1$ 表示在。这是论文实验部分主要执行的审计阶段。

3. **阶段3：联合审计（Joint Auditing）**  
   评估预训练和适配数据在已适配 LLM 中的联合泄露。该阶段考虑两个独立的训练阶段和可能不同的数据集（Figure 6），区别于标准 ML 隐私审计。

4. **阶段4：适配后预训练审计（Post-Adaptation Auditing）**  
   评估适配过程对预训练数据保护程度的影响。假设检验为：
   $$H_{0} : (a, b) = (0, 0) \qquad H_{A} : (a, b) = (1, 0)$$
   即样本在预训练中但不在适配中，考察适配是否削弱了原本缺乏形式化保障的预训练数据保护。

> **方法局限**：论文明确指出现有工作仅完成了阶段2（适配审计）和阶段4（适配后预训练审计）的实证评估，阶段1和阶段3的完整联合审计方法尚未提供，属于开放问题。



## 实验与关键发现

### 核心发现：分布接近性是隐私泄露的主要驱动力

本研究的中心发现是，适配数据与预训练数据之间的分布关系对DP适配的实际隐私风险产生决定性影响，其作用甚至超过理论隐私预算本身。即使适配数据与预训练数据不存在直接重叠，只要两者分布足够接近，泄露程度就可能与完全重叠的场景相当。

**实证量化**：作者通过Sentence-BERT嵌入计算Wasserstein距离来量化分布偏移（Table 1）。基于Pile的IID数据集（Bookcorpus2、GitHub、Enron）距离值极低（例如Bookcorpus2 Train为0.0171），而OOD数据集（SAMSum为0.0250，GermanWiki为0.0556）则显著偏高。这一量化结果为后续的隐私泄露差异提供了结构性解释。


![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_jY7fAo9rfK/figures/002_Table_1.jpg]]
*Table 1: Empirical quantification of dataset shift via the Wasserstein distance*

**关键证据**：Figure 9展示了训练过程中重叠数据和IID数据的隐私泄露曲线几乎完全重合。这一发现颠覆了“无重叠即安全”的直觉——分布接近性本身足以驱动严重的成员推断风险。在ε=8的中等隐私预算下，IID数据的RMIA AUC与直接重叠数据相当，表明理论DP保障在实际分布接近场景下可能被显著削弱。

### 不同适配方法的经验隐私保护对比

本研究系统评估了五种DP适配策略在OOD和IID场景下的成员推断脆弱性，以RMIA（影子模型变体）作为主要攻击手段。

**OOD场景下的表现**（Table 2）：在所有OOD数据集上，LoRA一致展现出最低的AUC值。以ε=8为例：

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_jY7fAo9rfK/figures/003_Table_2.jpg]]
*Table 2: Membership Inference for OOD Adaptations. We audit only the adaptations and assume the same pretrained LLM is used for all adaptations. We present the AUC scores obtained with RMIA for the Pythia 1B model adapted on different datasets with ε ∈ {0.1, 8, ∞}*

- SAMSum数据集：LoRA AUC为0.69，Full Fine-Tuning为0.82（差距-0.13）
- GermanWiki数据集：LoRA AUC为0.59，Head Fine-Tuning为0.76（差距-0.17）
- OOD平均：LoRA平均AUC为0.64，Head Fine-Tuning平均为0.87（差距-0.23）

Prefix Tuning在非隐私设置（ε=∞）下极其脆弱，AUC达到1.00，但在DP保护下（ε=8）降至0.62–0.63，表现出对隐私预算的强依赖性。相比之下，Reference方法和Min-K%方法（Table 4）在DP设置下表现接近随机猜测（AUC≈0.50），说明无影子模型的攻击对DP适配几乎无效。


![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_jY7fAo9rfK/figures/017_Table_4.jpg]]
*Table 4: Membership Inference for OOD Adaptations. We audit only the adaptations and assume the same pretrained LLM is used for all adaptations. We present the AUC scores obtained with reference, and Min-K% MIAs for the Pythia 1B model adapted on different datasets with $\varepsilon \in \{$ 0 . 1 , 8 , $\infty \}$

**IID场景下的表现**（Table 3）：IID设置下的AUC普遍高于OOD，进一步验证了分布接近性驱动风险的核心论断。LoRA在IID场景下仍保持相对较低的AUC，但其优势不如OOD场景显著，这提示当适配数据与预训练分布高度一致时，所有方法都面临更大的隐私挑战。


![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_jY7fAo9rfK/figures/004_Table_3.jpg]]
*Table 3: Membership Inference for in-distribution (IID) Adaptations using the setup from Table 2*

### 隐私‑效用权衡分析

Figure 4通过超参数搜索展示了各适配方法在GermanWiki数据集上（ε=8）的隐私‑效用权衡曲线。LoRA在困惑度14.27时AUC为0.77，而Full Fine-Tuning在相近困惑度14.60时AUC高达0.82。LoRA不仅实现了更低的隐私泄露，还维持了可比的模型效用，在帕累托前沿上占据优势位置。

在GitHub（val）数据集上，LoRA以困惑度4.8取得AUC 0.6，而Full Fine-Tuning在相同困惑度下AUC为0.83，差距更为悬殊。这些结果表明，LoRA的隐私优势并非以牺牲效用为代价，而是源于其参数高效特性天然限制了适配数据对模型参数的过度影响。

### 数据提取攻击与逐字记忆

除成员推断外，本研究还通过金丝雀暴露度和逐字记忆测试评估了数据提取风险。Figure 3显示，Prefix Tuning在降低预训练数据的逐字记忆方面效果最为显著，尤其在高隐私（小ε）设置下。当ε=0.1时，Prefix Tuning将记忆样本数降至约430个，而其他方法维持在更高水平。

Table 22和Table 23报告了金丝雀暴露度结果。在ε=∞时，Prefix Tuning和Full Fine-Tuning的暴露度显著高于LoRA和Head Fine-Tuning；但在ε=0.1和ε=8时，所有方法的暴露度均接近随机猜测水平（约1.44），表明DP在防止逐字数据提取方面相对有效。然而，Prefix Tuning在非隐私设置下的高暴露度值得警惕，说明该方法在缺乏DP保护时对数据提取攻击尤为脆弱。

### 攻击有效性的关键消融

**影子模型的重要性**（Figure 11）：RMIA的性能高度依赖影子模型的可用性。使用至少一个影子模型对DP适配的攻击至关重要；无影子模型时，RMIA的AUC接近随机水平（0.50）。这一发现对实际攻击场景有重要启示：攻击者若能获取或训练影子模型，DP保护的实证效果将大打折扣。

**参考模型选择的影响**（Figure 2）：使用预训练基模型作为参考模型时，IID数据的RMIA效果显著优于OOD数据。这进一步支持了分布接近性驱动泄露的论点——预训练模型对IID数据的似然估计更准确，从而为攻击提供了更强的信号。

**RMIA参数γ的选择**（Figure 14）：γ=1在多数场景下是最优或接近最优的选择，可作为强基线使用。暴露估计的两种近似方法（采样与分布建模）在使用256个非成员金丝雀时表现相似（Figure 13），验证了采样方法在效率上的可行性。

### 失败模式与局限性

1. **中等隐私预算的不足**：即使在ε=8的“中等”隐私预算下，IID适配数据仍面临显著的成员推断威胁（AUC远高于0.5）。这表明实践中常用的隐私参数可能无法提供足够保护，尤其当适配数据与预训练分布接近时。

2. **Reference和Min-K%方法的局限性**：这些无影子模型的攻击在DP设置下几乎完全失效（AUC≈0.50），说明它们不适用于审计DP适配的隐私泄露。隐私审计必须依赖更强大的攻击模型（如RMIA with shadow models）才能揭示真实的脆弱性。

3. **Prefix Tuning的双刃剑效应**：虽然Prefix Tuning在DP保护下能有效降低逐字记忆（Figure 3），但在非隐私设置下却是数据提取风险最高的方法。这种极端敏感性使其在实践中的安全性高度依赖于隐私预算的严格配置。

4. **模型覆盖范围的限制**：本研究主要基于Pythia系列、GPT-Neo和OLMo等开源模型，未涵盖无法进行DP适配的闭源大模型（如GPT-4）。对于OLMo模型，由于缺乏已知验证集，分析受到进一步限制。

### 关键图表索引

- **Table 1**：Wasserstein距离量化数据集偏移，为IID/OOD分类提供实证基础
- **Table 2**：OOD适配的RMIA AUC主结果，LoRA表现最优
- **Table 3**：IID适配的RMIA AUC主结果，泄露程度普遍高于OOD
- **Figure 3**：Prefix Tuning降低逐字记忆的效果（跨ε值）
- **Figure 4**：隐私‑效用权衡曲线，LoRA占据帕累托前沿

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_jY7fAo9rfK/figures/008_Figure_4.jpg]]
*Figure 4: Privacy-utility curves for the top perplexity-selected runs from the Pythia-1B hyperparameter search, shown for the chosen adaptation method, dataset, and privacy budget*

- **Figure 9**：重叠与IID数据泄露曲线重合，揭示分布接近性的核心作用

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_jY7fAo9rfK/figures/040_Figure_9.jpg]]
*Figure 9: Overlap and IID data show the same amount of privacy leakage across training. The x-axis shows the difference between the initial pretrained loss and the evaluation loss. The y-axis represents the AUC score. We adapt Pythia 1B with $\varepsilon$ = 8*

- **Figure 11**：影子模型对RMIA有效性的关键消融

### 补充图表

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_jY7fAo9rfK/figures/018_Table_5.jpg]]
*Table 5: Membership Inference for in-distribution (IID) Adaptations. We use the same setup as in Table 4*

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_jY7fAo9rfK/figures/019_Table_6.jpg]]
*Table 6: Membership Inference for OOD Adaptations using Pythia 1.4B. We present the AUC scores obtained with reference, and Min-K% MIAs for the Pythia 1.4B model adapted on different datasets with $\varepsilon \in \{$ 0 . 1 , 8 , $\infty \}$

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_jY7fAo9rfK/figures/020_Table_7.jpg]]
*Table 7: Membership Inference for IID Adaptations using Pythia 1.4B. We present the AUC scores obtained with reference, and Min-K% MIAs for the Pythia 1.4B model adapted on different datasets with $\varepsilon \in \{$ 0 . 1 , 8 , $\infty \}$

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_jY7fAo9rfK/figures/021_Table_8.jpg]]
*Table 8: Membership Inference for OOD Adaptations using Pythia 410M. We present the AUC scores obtained with reference, and Min-K% MIAs for the Pythia 410M model adapted on different datasets with $\varepsilon \in \{$ 0 . 1 , 8 , $\infty \}$

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_jY7fAo9rfK/figures/022_Table_9.jpg]]
*Table 9: Membership Inference for IID Adaptations using Pythia 410M. We present the AUC scores obtained with reference, and Min-K% MIAs for the Pythia 410M model adapted on different datasets with $\varepsilon \in \{$ 0 . 1 , 8 , $\infty \}$





## 定位与知识库关联

### 核心定位：预训练‑适配范式的整体隐私审计

本研究构建了首个面向**预训练‑适配范式**的整体隐私审计框架与基准，核心贡献在于将审计范围从传统的单一训练阶段审计扩展为四个阶段（Figure 5）：（1）预训练审计，（2）适配审计，（3）预训练与适配的联合审计，（4）适配后预训练审计。这一框架的形式化填补了现有工作仅关注独立预训练或独立适配审计的空白——现有MIA研究通常假设单一训练阶段，而忽略了预训练数据与适配数据之间的复杂依赖关系对隐私泄露的传导效应。

### 与现有隐私适配方法的继承关系

本文不提出新的隐私适配算法，而是对**现有DP适配方法谱系**进行系统性基准评估，涵盖以下五类方法的代表性实现：

| 适配方法 | 底层机制 | 代表工作 |
|----------|----------|----------|
| **Full DP Fine‑Tuning** | 基于DPSGD的全参数微调 | Li et al., 2022 |
| **Head DP Fine‑Tuning** | 仅微调最后分类层 | Li et al., 2022 |
| **DP‑LoRA** | 低秩适配矩阵的差分隐私训练 | Hu et al., 2022; Yu et al., 2022 |
| **DP‑Prefix Tuning** | 可学习前缀向量的差分隐私优化 | Liu et al., 2021; Duan et al., 2023a |
| **DP Prompting** | 基于PATE的私有上下文学习 | Duan et al., 2023a |

这些方法覆盖了当前DP适配的两大技术路线：（1）基于DPSGD的私有微调方法（前四类），依赖梯度访问和噪声注入；（2）基于PATE的私有推理时方法（DP Prompting），通过教师集成进行知识迁移。攻击侧则采用当前最强的成员推断攻击**RMIA**（Zarifzadeh et al., 2024）作为主要威胁模型，并辅以Reference方法（Carlini et al., 2021）和Min‑K%作为基线对比。

### 关键因果机制：分布接近性驱动隐私泄露

本文的核心发现揭示了**适配数据与预训练数据之间的分布关系**是隐私泄露的主要因果旋钮，而非简单的数据重叠。这一发现对现有DP适配的理论保障提出了重要挑战：

- **IID数据的泄露程度与直接重叠数据相似**（Figure 9），即使适配数据不包含预训练样本，仅凭分布接近就足以使RMIA攻击达到高AUC。这表明理论DP保障在实际中可能不足以防护分布相近场景下的成员推断。
- **OOD数据相对安全**：当适配数据与预训练分布差异较大时（如SAMSum相对于Pile语料），隐私泄露显著降低。Wasserstein距离（Table 1）提供了分布偏移的实证量化——Bookcorpus2 Train距离为0.0171（IID），而GermanWiki为0.0556（OOD）。
- **预训练模型本身是强参考模型**：Figure 2表明，攻击者仅需访问预训练基础模型即可对IID适配数据发起有效MIA，无需额外的影子模型训练，这降低了攻击门槛。

### 方法选择的适用边界

本文的实验设计覆盖了从完全重叠到完全OOD的完整分布谱系，但存在以下适用边界：

1. **模型覆盖有限**：实验仅使用Pythia 1B、GPT‑Neo和OLMo系列模型，未覆盖当前最先进的闭源模型（如GPT‑4）。这些闭源模型无法通过API进行DP适配，限制了框架的直接推广。
2. **联合审计方法未完整实现**：虽然提出了四阶段审计框架，但本文仅完成了适配审计和适配后预训练审计的实证评估，**联合审计所有阶段的方法尚未提供**，这是框架的一个开放缺口。
3. **攻击者知识假设**：RMIA的有效性高度依赖攻击者对目标模型和预训练数据的知识（Figure 2）。当攻击者缺乏预训练数据访问权限时，对DP适配的攻击性能接近随机猜测，这意味着本文的隐私风险估计代表了**强威胁模型下的上界**。

### 关键消融发现

消融实验揭示了几个对后续工作具有指导意义的机制性结论：

- **影子模型对RMIA至关重要**：Figure 11表明，使用至少一个影子模型是RMIA有效的必要条件，尤其对于DP适配场景。无影子模型时攻击性能接近随机。
- **Prefix Tuning降低逐字记忆**：Figure 3显示，Prefix Tuning在高隐私设置（小ε）下能显著减少已适配模型中预训练数据的逐字记忆样本数量，这为缓解预训练数据泄露提供了方法层面的启示。
- **RMIA参数γ=1是强基线**：Figure 14的消融表明，似然比阈值γ的默认选择在实践中已足够鲁棒。

### 局限性与开放问题

**局限性**：
- 联合审计所有过程阶段的完整方法尚未实现，当前仅覆盖适配审计和适配后预训练审计。
- 模型覆盖仅限于开源LLM，缺乏对闭源前沿模型（如GPT‑4）的审计能力。
- 对于OLMo和OLMo2模型，由于缺乏已知验证数据集，分析受到限制。

**开放问题**：
1. 如何在预训练‑适配范式下实现**所有过程阶段的联合审计**？这需要设计能够同时处理预训练成员和适配成员的复合假设检验。
2. 如何将整体隐私审计框架**扩展至无法通过API进行DP适配的闭源大模型**？这可能需要基于查询的审计方法或替代的隐私评估指标。
3. 在存在复杂预训练‑适配数据依赖关系时，如何设计和形式化**更全面的成员推断游戏**？当前的双数据集假设检验框架（$H_0: (a,b) = (0,0)$ vs $H_A: (a,b) = (1,0)$）可能不足以捕捉所有泄露路径。

### 对后续工作的启示

本文为DP适配研究提供了两个关键的方法论指导：（1）**隐私评估必须考虑预训练‑适配的分布关系**，仅报告理论ε值不足以表征实际风险；（2）**LoRA在多数场景下提供最佳的隐私‑效用权衡**（Figure 4），应作为DP适配的默认基线方法。这些发现为设计更安全的LLM适配策略指明了方向——未来的方法设计需要在适配能力与分布泄露风险之间取得平衡，而非单纯追求更低的ε值。



## 原文 PDF

![[paperPDFs/ICLR_2026/Benchmarking_Empirical_Privacy_Protection_for_Adaptations_of_Large_Language_Models.pdf]]
