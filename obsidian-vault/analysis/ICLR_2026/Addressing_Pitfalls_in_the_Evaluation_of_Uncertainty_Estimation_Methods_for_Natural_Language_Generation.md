---
title: "Addressing Pitfalls in the Evaluation of Uncertainty Estimation Methods for Natural Language Generation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Addressing_Pitfalls_in_the_Evaluation_of_Uncertainty_Estimation_Methods_for_Natural_Language_Generation.pdf
project_link: null
code_link: null
openreview_forum_id: OxWnOV5q8w
aliases:
- SMSTEAUE
- APEUEMNLG
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "通过边缘化多个LLM-as-a-judge的变体（SP-MoJI）或采用结构化任务中的精确正确性验证，可以显著降低风险指标的偏差和方差，从而获得更稳定的不确定性方法排名。"
primary_logic: "选择性预测的性能同时依赖于不确定性估计的质量和正确性标签的偏差/方差。通过对多个法官模型和指令变体的输出求均值（SP-MoJI），可以边缘化正确性标签的参数，减少评估偏差；结构化任务（如代码生成、约束文本生成）提供了确定性的非参数化正确性函数，完全消除了标签边缘化的需要；Elo聚合则能综合多维度实验信息，提供客观的整体排名。"
claims:
- "不同近似正确性函数在QA数据集上存在显著分歧，导致不确定性估计方法排名不一致。"
- "对抗性地选择正确性函数可以显著抬升特定不确定性方法的排名；例如，G-NLL的Top-3频率从0.375升至0.688。"
- "使用SP-MoJI并集成4个法官可将性能估计器的标准差（SD）降低约两倍；单法官SD可达0.04，对应95%置信区间约±8%。"
- "Elo评级系统能够有效汇总跨模型、数据集和风险指标的多维实验结果，揭示简单方法在QA域外也具备竞争力。"
---

# Addressing Pitfalls in the Evaluation of Uncertainty Estimation Methods for Natural Language Generation

> [!tip] 核心洞察
> 选择性预测的性能同时依赖于不确定性估计的质量和正确性标签的偏差/方差。通过对多个法官模型和指令变体的输出求均值（SP-MoJI），可以边缘化正确性标签的参数，减少评估偏差；结构化任务（如代码生成、约束文本生成）提供了确定性的非参数化正确性函数，完全消除了标签边缘化的需要；Elo聚合则能综合多维度实验信息，提供客观的整体排名。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 解决自然语言生成中不确定性估计方法评估的陷阱 |
| 英文题名 | Addressing Pitfalls in the Evaluation of Uncertainty Estimation Methods for Natural Language Generation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=OxWnOV5q8w) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | SP-MoJI, Structured Tasks, and Elo Aggregation for Uncertainty Evaluation |
| Dataset | CoQA / SQuAD (QA datasets), Various QA benchmarks, ALL TASKS (QA + CODE + C.TEXT + OOD + PERT) |

> [!tip] 效果简介
> - CoQA / SQuAD (QA datasets) 上，SD of mean AUROC (bootstrap estimate) 为 使用4个法官时SD降低约50%，对比 单个法官SD可达0.04，变化 ~2x reduction in SD。
> - Various QA benchmarks 上，频率 of Top‑3 membership (adversarial correctness selection vs reference) 为 参考值: G‑NLL=0.375, Perplexity=0.125，对比 对抗选择: G‑NLL=0.688 (+0.312), Perplexity=0.444 (+0.319)，变化 大幅虚增（up to +0.375 for Min Token Log‑Prob）。
> - ALL TASKS (QA + CODE + C.TEXT + OOD + PERT) 上，Elo rating 为 简单方法（如G‑NLL、Perplexity）在Elo汇总中总体表现好于许多复杂方法，对比 无统一汇总基线；传统评估以孤立表格呈现，变化 Elo aggregation reveals competitive performance of simple methods outside QA。

## 概要

**核心瓶颈**：当前自然语言生成（NLG）不确定性估计方法的评估严重依赖近似正确性函数（如 ROUGE、BLEU、LLM‑as‑a‑judge）。这些函数之间存在显著分歧（Fig. 1），导致不确定性方法的排名在不同正确性函数下不一致。更严重的是，正确性标签的偏差和方差会扭曲 AUROC 估计——对抗性地选择正确性函数即可大幅虚增特定方法的排名（Table 2），暴露出评估协议的系统性漏洞。

**因果机制**：选择性预测的性能同时取决于不确定性估计的质量和正确性标签的偏差/方差。论文通过理论分析揭示了标签噪声和样本依赖扭曲如何影响 AUROC 估计（Eq. 3, Eq. 5），并指出近似正确性函数的参数化特性是评估不稳定的根源。

**核心解决方案**：
- **SP‑MoJI**（Selective Prediction with Mixture of Judges and Instructions）：对多个法官模型和指令变体的 AUROC 取平均，边缘化正确性标签的参数，显著降低评估方差（4 个法官即可将标准差降低约两倍，Fig. 2）。
- **结构化任务精确正确性**：在代码生成（BigCodeBench）和约束文本生成（COLLIE）等可符号验证的任务上使用确定性非参数化正确性函数，完全消除标签边缘化的需要。
- **多维度风险指标**：将评估从单一选择性预测扩展至分布外检测（OOD）、扰动检测（Perturbation）和结构化任务精确正确性，覆盖更广泛的不确定性使用场景。
- **Elo 聚合**：将每个数据集‑模型组合的实验视为一场比赛，通过 Elo 评分系统汇总相对表现，提供概率化解释和间接比较能力（Fig. 3）。

**关键发现**：Elo 聚合揭示，简单的启发式方法（如 G‑NLL、Perplexity）在跨任务、跨模型的综合评估中总体表现优于许多复杂方法，这一结论在传统孤立表格评估中难以显现。SP‑MoJI 与人工标注的相关性也高于单个法官的平均相关性（Fig. 7），进一步验证了多法官边缘化的有效性。

自然语言生成（NLG）中的不确定性估计（Uncertainty Estimation, UE）旨在量化模型输出的可信度，其核心评估范式是**风险相关性实验**：将估计的不确定性 $\hat{u}(x_i, w; \theta_u)$ 与某种风险指标 $r(x_i, y_i')$ 进行相关性度量（通常使用AUROC或Spearman $\rho$）[Eq. 1]。其中，**选择性预测**（Selective Prediction）是最广泛使用的评估场景——用否定正确性 $\neg c(\pmb{y}_i', \pmb{y}_i, \pmb{x}_i; \pmb{\theta}_c)$ 作为风险指标，检验不确定性方法能否区分正确与错误输出[Eq. 2]。

然而，当前NLG不确定性评估存在一个根本性的瓶颈：**评估严重依赖于近似的正确性函数**。在自由文本生成任务中，精确的正确性判断通常不可得，研究者不得不使用ROUGE、BLEU等基于n-gram重叠的指标，或LLM-as-a-judge等参数化判断模型来近似正确性标签。如Table 1所总结的，近期大多数UE评估工作仅依赖这类近似函数，且评估范围局限于QA任务上的选择性预测。

这一依赖带来了两个深层问题：

**第一，近似正确性函数之间存在显著分歧。** 如Fig. 1所示，不同正确性函数（ROUGE变体、BLEU、不同法官模型）在QA数据集上的相互AUROC一致性有限，且这些分歧直接导致不确定性方法排名的系统性不一致——同一组UE方法在不同正确性函数下的排序Spearman $\rho$ 可能极低。这意味着，**“哪种不确定性方法更好”的结论高度依赖于选择哪个正确性函数**。

**第二，正确性标签的偏差和方差会系统性扭曲AUROC估计。** 选择性预测的性能同时依赖于不确定性估计的质量和正确性标签的偏差/方差。在独立伯努利标签噪声下，AUROC的期望变化为 $\mathrm{AUROC}^{\mathrm{noisy}} = \mathrm{AUROC}^{\mathrm{orig}} \cdot (1 - 2p) + p$ [Eq. 3]，即噪声概率 $p$ 会直接压缩AUROC的动态范围。更严重的是，当标签扭曲与样本特征相关时（即 $c_{x_i}^{\mathrm{biased}}$ 的翻转概率依赖于 $x_i$），不同UE方法受偏差影响的程度不同，导致排名可以被**对抗性地操纵**。Table 2的实验直接证明了这一漏洞：通过对抗性地选择正确性函数，G-NLL的Top-3频率可以从0.375被虚增至0.688，Perplexity从0.125被虚增至0.444。这种“正确性黑客攻击”表明，现有评估协议缺乏对正确性函数参数选择自由度的控制。

**第三，评估维度单一。** 绝大多数工作仅使用QA数据集上的选择性预测作为评估手段，忽视了分布外（OOD）检测、扰动检测等其他风险指标。这些替代指标可以验证不确定性估计是否在不同类型的风险场景下保持一致的判别能力，从而提供更全面的评估。

上述问题共同指向一个核心洞察：**需要一种能够边缘化正确性标签参数、拓展风险指标维度、并综合多维实验信息的评估框架**，以消除单一近似正确性函数引入的评估偏差，获得更稳定、更客观的不确定性方法排名。本文正是围绕这一目标，提出SP-MoJI（多法官混合选择性预测）、结构化任务精确正确性验证、以及基于Elo评分的概率化聚合三个互补方案。

## 核心方法与创新机理

### 问题诊断：近似正确性函数作为评估陷阱

当前NLG不确定性估计（UE）的评估协议存在一个根本性缺陷：几乎所有工作都依赖**近似的正确性函数**（如ROUGE-L、BLEU、LLM-as-a-judge）来标记模型输出的“正确/错误”，并以此作为选择性预测的风险指标。Table 1 的协议综述表明，现有UE评估极少超出QA任务上的选择性预测，且普遍使用近似正确性函数或少量人工标注。

这一做法的核心问题在于：**近似正确性函数是参数化的**——它们依赖于与参考答案的相似度计算，且其参数 $\theta_c$（包括法官模型选择、提示模板、采样温度等）对评估结果有系统性影响。如 Eq. (2) 所示，选择性预测的AUROC同时取决于不确定性估计的质量和正确性标签的偏差/方差：

$$\xi_{\mathrm{SP}} = \mathrm{Cor}\left[ \left( \hat{u}(x_i, w; \pmb{\theta}_u) \right)_{i=1}^N, \left( \lnot c(\pmb{y}_i', \pmb{y}_i, \pmb{x}_i; \pmb{\theta}_c) \right)_{i=1}^N \right]$$

这意味着：**改变 $\theta_c$ 可以直接改变UE方法的评估排名，而无需改变UE方法本身**。

### 关键证据：正确性函数分歧与排名可操纵性

Figure 1 在CoQA和SQuAD上揭示了不同近似正确性函数之间的显著分歧：(a) 各正确性度量之间的互AUROC并不对称，ROUGE族内部一致性较高，但与LLM-as-a-judge存在系统分歧；(b) 在UE方法排序的Spearman $\rho$ 上，不同正确性函数对之间的 $\rho$ 可低至接近0，表明**排名几乎不相关**。

更严重的是，这种分歧可以被**对抗性地利用**。Table 2 展示了“正确性黑客攻击”的结果：通过对抗性地为每个UE方法选择最有利的正确性函数，G-NLL的Top-3频率从参考值0.375飙升至0.688（+0.312），Perplexity从0.125升至0.444（+0.319）。这意味着在缺乏标准化评估协议的情况下，**UE方法的排名可以被系统地操纵**。

### 核心创新：三个维度的评估协议改进

针对上述瓶颈，本文提出了一套三管齐下的评估改进方案，每个方案对应一个被改变的评估协议槽位：

**1. 正确性函数槽位：从单一近似函数到多法官混合（SP-MoJI）与精确正确性**

对于无法避免近似正确性的QA任务，提出**SP-MoJI（Selective Prediction with Mixture of Judges and Instructions）**：对 $K$ 个不同法官模型/提示的AUROC取平均，以边缘化正确性标签的参数 $\theta_c$：

$$\xi_{\mathrm{SP-MoJI}} = \mathrm{E}_{\theta_c}\left[ \xi_{\mathrm{SP}} \right] \approx \frac{1}{K}\sum_{k=1}^{K} \mathrm{Cor}\left[ \left( \hat{u}(x_i, w; \theta_u) \right)_{i=1}^N, \left( \neg J_k(y_i', y_i, x_i; \theta_k) \right)_{i=1}^N \right]$$

Figure 2 的bootstrap估计表明，使用4个法官即可将性能估计器的标准差降低约两倍；单法官的SD可达0.04（对应95%置信区间约±8%），而超过10个法官后收益递减。Figure 7 进一步显示，MoJI与人工标注的相关性高于单个法官的平均相关性，验证了边缘化的有效性。

对于**结构化任务**（代码完成BigCodeBench、约束文本生成COLLIE），则采用**确定性非参数化正确性函数**（如单元测试、约束验证），从根本上消除了标签边缘化的需求。Figure 10 表明，近似正确性函数在结构化任务上与精确正确性的一致性远低于QA场景，进一步凸显了精确评估的必要性。

**2. 风险指标槽位：从单一选择性预测到多维风险检测**

将评估从仅依赖QA选择性预测（negated correctness）扩展到三个互补的风险指标：
- **选择性预测**：保留传统设置，但使用SP-MoJI降低标签噪声
- **分布外检测（OOD）**：使用Known-Unknowns和SQuADv2不可回答问题，验证UE在分布偏移下的响应
- **扰动检测**：通过随机打乱输入上下文单词并控制扰动强度 $s_p$，评估UE与扰动强度的相关性：

$$\xi_{\mathrm{perturb}} = \frac{1}{N}\sum_{i=1}^{N} \mathrm{Cor}\left[ \hat{u}(p(\pmb{x}_i, s_p), \pmb{w}; \pmb{\theta}_u), s_p \right]$$

**3. 结果聚合槽位：从孤立表格到Elo评分系统**

将每个独立的数据集-模型风险相关实验视为一场“比赛”，使用Elo评分系统汇总UE方法的相对表现。Figure 3 按任务类型（QA、C.TEXT、CODE）、模型类型（IT/PT）和风险指标（OOD、PERT）分区展示Elo评级，提供了概率化解释（400分差对应1:10的胜负比）和间接比较能力。关键发现：简单方法（如G-NLL、Perplexity）在QA域外同样具有竞争力，而长度归一化在几乎所有场景下（除扰动检测外）都是有害的。

### 理论支撑：标签噪声与扭曲下的AUROC行为

Eq. (3) 给出了独立伯努利标签噪声下AUROC的期望变化：$\mathrm{AUROC}^{\mathrm{noisy}} = \mathrm{AUROC}^{\mathrm{orig}} \cdot (1 - 2p) + p$，表明噪声概率 $p$ 会向0.5压缩AUROC。Eq. (5) 进一步将样本依赖标签扭曲下的AUROC分解为未扭曲样本的AUROC贡献、扭曲样本的负贡献和一个偏差项，揭示了**不同UE方法对标签扭曲的敏感度不同**——这是排名可操纵性的数学根源。Figure 9 在合成数据上验证了该分解的无偏性和低方差。

### 局限与展望

SP-MoJI虽降低了方差，但仍依赖LLM-as-a-judge，无法完全消除法官模型的内在偏差。结构化任务的种类有限（仅代码和约束文本），扰动检测中扰动类型和强度的偏差尚未全面分析。Elo评分的解释性依赖于大量比赛的均匀采样。在CoT、多智能体等高级NLG设置下的适配留待未来工作。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_OxWnOV5q8w/figures/007_Figure_5.jpg]]
*Figure 5: UE method ordering heatmaps including AlignScore. In our experiments it was always observed to be in its own cluster. Although the default settings from the AlignScore repository together with ’base’ model were used, it is quite possible that some adjustments would improve its correlation to other correctness methods*

本工作并未提出新的不确定性估计方法，而是针对NLG不确定性估计的**评估协议**本身进行系统性诊断与改进。整个框架围绕一个核心洞察展开：选择性预测的性能同时依赖于不确定性估计的质量和正确性标签的偏差/方差。当前主流评估严重依赖近似的、参数化的正确性函数（如ROUGE、BLEU、LLM-as-a-judge），这些函数之间存在显著分歧（Fig. 1），导致不确定性方法的排名不一致，甚至可被对抗性操纵（Table 2）。

为应对这一问题，框架从三个维度重构评估流程：

### 1. 正确性标签的边缘化：SP-MoJI

在QA等必须依赖近似正确性函数的任务上，提出**SP-MoJI（Selective Prediction with Mixture of Judges and Instructions）**。其核心操作是对 $K$ 个不同法官模型/指令变体的AUROC取平均，以边缘化正确性标签的参数 $\theta_c$：

$$\xi_{\mathrm{SP-MoJI}} = \mathrm{E}_{\theta_c}\left[ \xi_{\mathrm{SP}} \right] \approx \frac{1}{K}\sum_{k=1}^{K} \mathrm{Cor}\left[ \left( \hat{u}(x_i, w; \theta_u) \right)_{i=1}^N, \left( \neg J_k(y_i', y_i, x_i; \theta_k) \right)_{i=1}^N \right]$$

经验上，使用4个法官即可将性能估计器的标准差降低约两倍（Fig. 2），有效缓解单一法官带来的评估偏差。

### 2. 精确正确性评估：结构化任务

在代码完成（BigCodeBench）和约束文本生成（COLLIE）等可符号验证的结构化任务上，直接使用确定性的非参数化正确性函数 $c_e$，**完全消除**了对正确性标签进行边缘化的需求。这是框架中偏差最低的评估分支。

### 3. 多维风险指标

除传统的选择性预测（以否定正确性为风险）外，框架引入两类额外的风险指标以全面评估不确定性估计的质量：

- **分布外检测（OOD）**：使用人工构造的OOD数据集（Known-Unknowns、SQuADv2不可回答问题），验证不确定性在分布偏移时是否升高。
- **扰动检测**：对输入上下文进行随机单词打乱，控制扰动强度 $s_p$，评估不确定性估计与扰动强度的相关性：

$$\xi_{\mathrm{perturb}} = \frac{1}{N}\sum_{i=1}^{N} \mathrm{Cor}\left[ \hat{u}(p(\pmb{x}_i, s_p), \pmb{w}; \pmb{\theta}_u), s_p \right]$$

### 4. 结果聚合：Elo评分系统

由于评估涉及多个数据集、模型、风险指标和正确性函数的组合，直接罗列大表格难以获得全局洞察。框架将每个独立的数据集-模型实验视为一场“比赛”，使用Elo评分系统汇总相对表现，提供概率化解释和间接比较能力（Fig. 3）。

### 模块关系与数据流

整体流程可概括为：对于给定的不确定性估计方法，在多个任务类型（QA / CODE / C.TEXT / OOD / PERT）上分别计算其与风险指标的秩相关（AUROC或Spearman $\rho$），其中QA分支通过SP-MoJI边缘化正确性标签，结构化任务分支使用精确正确性；各实验的结果最终输入Elo评分系统，输出统一的方法排名。该框架不改变不确定性方法本身，仅替换评估协议中的正确性函数、风险指标和聚合方式三个“槽位”。

### 问题形式化：风险相关性评估

NLG不确定性估计方法的效用通过不确定性估计值 $\hat{u}(\cdot)$ 与风险指标 $r(\cdot)$ 之间的相关性来评估：

$$\xi = \mathrm{Cor}\left[ \left( \hat{u}(x_i, w; \theta_u) \right)_{i=1}^N, \left( r(x_i, y_i') \right)_{i=1}^N \right]$$

其中 $\hat{u}(x_i, w; \theta_u)$ 是模型 $w$ 对输入 $x_i$ 的不确定性估计，$r(x_i, y_i')$ 是生成结果 $y_i'$ 的风险指标，$\mathrm{Cor}$ 通常取Spearman秩相关或AUROC。

**选择性预测**是其中最常用的场景，以“不正确性”（negated correctness）作为风险指标：

$$\xi_{\mathrm{SP}} = \mathrm{Cor}\left[ \left( \hat{u}(x_i, w; \pmb{\theta}_u) \right)_{i=1}^N, \left( \lnot c(\pmb{y}_i', \pmb{y}_i, \pmb{x}_i; \pmb{\theta}_c) \right)_{i=1}^N \right]$$

这里 $c(\cdot; \pmb{\theta}_c)$ 是正确性函数，$\lnot c$ 即为“错误”标签。核心瓶颈在于：$\xi_{\mathrm{SP}}$ 同时依赖于不确定性估计的质量和正确性标签的偏差/方差——当正确性函数本身有偏时，评估结果将被系统性扭曲。

---

### 模块一：SP-MoJI——多法官混合边缘化

**动机**：正确性函数 $c(\cdot; \pmb{\theta}_c)$ 是参数化的（如ROUGE-L、BLEURT、LLM-as-a-judge），不同参数化之间存在显著分歧（见Fig. 1），导致不确定性方法排名不一致。SP-MoJI通过对 $K$ 个不同法官模型/指令的AUROC取平均，边缘化正确性标签的参数 $\pmb{\theta}_c$：

$$\xi_{\mathrm{SP-MoJI}} = \mathrm{E}_{\theta_c}\left[ \xi_{\mathrm{SP}} \right] \approx \frac{1}{K}\sum_{k=1}^{K} \mathrm{Cor}\left[ \left( \hat{u}(x_i, w; \theta_u) \right)_{i=1}^N, \left( \neg J_k(y_i', y_i, x_i; \theta_k) \right)_{i=1}^N \right]$$

其中 $J_k$ 表示第 $k$ 个法官模型（可搭配不同提示和采样温度）。关键实证发现：使用4个法官即可将性能估计量的标准差降低约两倍（Fig. 2），单法官SD可达0.04（对应95%置信区间约±8%），超过10个法官后收益递减。

---

### 模块二：结构化任务中的精确正确性

当任务具有确定性的非参数化正确性函数 $c_e$ 时，完全消除了对正确性标签边缘化的需求。论文在两类结构化任务上验证了这一点：

- **代码完成**（BigCodeBench）：通过单元测试精确判断生成代码的正确性。
- **约束文本生成**（COLLIE）：通过符号验证判断输出是否满足给定约束。

在此类任务中，近似正确性函数（如ROUGE、LLM-as-a-judge）与精确正确性之间存在系统性差距（Fig. 10），进一步印证了QA场景下依赖近似函数的评估风险。

---

### 模块三：扰动检测与OOD检测

除选择性预测外，论文引入了两类替代风险指标来扩展评估维度：

**扰动检测**：对输入上下文随机打乱单词，控制扰动强度 $s_p$，评估不确定性与扰动强度的相关性：

$$\xi_{\mathrm{perturb}} = \frac{1}{N}\sum_{i=1}^{N} \mathrm{Cor}\left[ \hat{u}(p(\pmb{x}_i, s_p), \pmb{w}; \pmb{\theta}_u), s_p \right]$$

其中 $p(\pmb{x}_i, s_p)$ 是对输入施加强度 $s_p$ 扰动的函数。该指标在CoQA和SQuADv2上实现。

**OOD检测**：使用人工构造的分布外数据集（Known-Unknowns、SQuADv2不可回答问题）作为风险标签，验证不确定性估计值在OOD样本上是否显著升高。

---

### 模块四：Elo评分聚合

为汇总跨数据集、模型类型和风险指标的多维实验结果，论文将每个独立的数据集‑模型实验视为一场“比赛”，采用Elo评分系统进行概率化聚合。方法A和B的胜负由对应实验中的风险相关性高低决定。Elo系统提供间接比较能力，400分差距对应约1:10的胜率比。该方法在Fig. 3中按任务类型（QA / C.TEXT / CODE）、模型类型（IT指令微调 / PT预训练）和风险指标（OOD / PERT）分别呈现了各不确定性方法的评级。

---

### 标签噪声的理论刻画

为理解正确性标签偏差对AUROC的影响，论文给出了两个关键分解：

**独立伯努利噪声**下，AUROC的期望变化为：

$$\mathrm{AUROC}^{\mathrm{noisy}} = \mathrm{AUROC}^{\mathrm{orig}} \cdot (1 - 2p) + p$$

其中 $p$ 为标签翻转概率。该式揭示了噪声对AUROC的线性压缩效应。

**样本依赖标签扭曲**下，AUROC可分解为（详见Appx. D.2.1 Eq. (27)）：

$$\mathrm{AUROC}^{\mathrm{dist}} = \mathrm{AUROC}^{\mathrm{orig \cdot undist}} \frac{n_0(d_i=0) n_1(d_j=0)}{n_0 n_1} - \mathrm{AUROC}^{\mathrm{orig \cdot dist}} \frac{n_0(d_i=1) n_1(d_j=1)}{n_0 n_1} + 0.5 \left( \frac{n_0(d_i=1)}{n_0} + \frac{n_1(d_j=1)}{n_1} \right)$$

其中 $d_i$ 指示第 $i$ 个样本的标签是否被扭曲。该分解在合成数据上得到了实证验证（Fig. 9），偏差低且方差小，尤其适用于QA数据集常见规模（$10^3$ 量级）。

## 实验与关键发现

### 核心发现：正确性标签偏差是评估失效的根源

实验的核心因果机制在于：选择性预测的AUROC同时依赖于不确定性估计的质量和正确性标签的偏差/方差。当前NLG不确定性评估普遍使用近似正确性函数（ROUGE、BLEU、LLM-as-a-judge等），这些函数的参数化特性使得评估结果可以被系统性操纵。

**正确性函数分歧实验**（Fig. 1）揭示了问题的严重性。在CoQA和SQuAD数据集上，不同近似正确性函数之间的互AUROC和Spearman ρ存在显著分歧。ROUGE族内部（R1/R2/RL）在短答案上高度一致，但与LLM-as-a-judge存在系统性偏差。这种分歧直接导致不确定性估计方法的排名不一致——同一方法在不同正确性函数下可能获得截然不同的排名。

**正确性黑客攻击**（Table 2）进一步验证了评估的脆弱性。通过对抗性地选择正确性函数，可以大幅抬升特定方法的Top-3频率：G-NLL从0.375升至0.688（+0.312），Perplexity从0.125升至0.444（+0.319），Min Token Log-Prob甚至获得+0.375的提升。这表明仅凭选择不同的正确性函数，就可以让一个方法看起来"更好"或"更差"，评估结果缺乏客观性。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_OxWnOV5q8w/figures/003_Table_2.jpg]]
*Table 2: Adversarially selecting a correctness function on the QA benchmark to improve the ranking of individual uncertainty estimation methods. The values are frequencies of uncertainty estimation methods Top-3 membership on the considered QA datasets. The reference for our assessment is an average over LLM-as-a-judge variants introduced in Sec. 4. Details on the settings used to produce this table can be found in Appx. B.5.3*

### SP-MoJI的方差降低效果

**Bootstrap估计实验**（Fig. 2）量化了SP-MoJI对评估稳定性的改善。在选定的QA数据集/模型组合上：

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_OxWnOV5q8w/figures/004_Figure_2.jpg]]
*Figure 2: Bootstrap estimate of the standard deviation of mean of AUC performance on selected QA dataset / model combinations. As a rule of thumb, using SP-MoJI with 4 judges reduces the standard deviation of performance estimator twofold. For implementation details refer to B.5.1*

- 使用单个法官时，性能估计器的标准差（SD）可达0.04，对应95%置信区间约±8%——这意味着仅因标签噪声，AUROC就可能在0.08的范围内波动。
- 使用SP-MoJI集成4个法官可将SD降低约两倍，显著收窄置信区间。
- 超过10个法官调用后，收益递减明显，说明4个法官是实用的性价比最优选择。

这一结果直接验证了边缘化正确性标签参数的有效性：通过对多个法官模型和指令变体的输出求均值，评估偏差和方差得到实质性控制。

### 结构化任务揭示简单方法的竞争力

在代码完成（BigCodeBench）和约束文本生成（COLLIE）等结构化任务上，正确性函数是确定性的非参数化验证（单元测试通过/失败、约束满足/违反），完全消除了标签边缘化的需要。Fig. 10显示，在这些任务上，近似正确性函数与精确正确性之间存在明显差距，尤其是在COLLIE上，LLM-as-a-judge的表现受提示设计影响巨大（Fig. 11）。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_OxWnOV5q8w/figures/013_Figure_10.jpg]]
*Figure 10: Correctness consistency on structured datasets. R indicates ROUGE family, B - BLEU. judge models are indicated with J, ’q’ stands for QA prompt used in Farquhar et al. (2024) while ’g’ stands for a more general prompt to evaluate correctness (see Apx. C.2 for more details on prompting). (a) Agreement of correctness metrics in terms of mutual AUROC (not symmetric). Column values are binarized at 0.5 where applicable. (b) Correlation of UE algorithm orderings when compared between corresponding pairs of correctness functions*

这一实验设置产生了重要的反直觉发现：在传统QA评估中被认为"简单"的方法（如G-NLL、Perplexity），在结构化任务上表现出乎意料的竞争力。这暗示QA基准上的评估可能系统性地低估了简单方法的实际效用。

### Elo聚合揭示全局格局

**Elo评级总结**（Fig. 3）将每个独立的数据集-模型实验视为一场比赛，通过概率化聚合提供客观的整体排名。关键发现：

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_OxWnOV5q8w/figures/005_Figure_3.jpg]]
*Figure 3: Elo ratings of NLG uncertainty estimation methods. The methods are grouped by color according to their category (see Apx. B.1). The line at 1000 Elo indicates the average rating. Elo rating were independently estimated for several key partitions. Per task used: QA - selective prediction on QA datasets, C.TEXT - constrained text generation, CODE - code completion. Per models used: IT - instruction fine tuned models only, PT - pretrained models only. Finally, we report the partitions of the alternative risk indicators: OOD - out-of-distribution and PERT - perturbation*

- **简单方法的跨域竞争力**：在ALL TASKS汇总中，G-NLL和Perplexity等简单方法的Elo评级总体好于许多更复杂的方法。这一发现挑战了"更复杂的方法必然更好"的假设。
- **预训练模型的困难**：在仅使用预训练模型（PT）的分区上，随机基线获得了高Elo评级，表明所有方法在该设置下表现均不理想——这是一个重要的失败模式信号。
- **长度归一化的负面效应**：在除扰动检测外的几乎所有场景中，长度归一化都是有害的。这一消融发现对方法设计具有直接指导意义。
- **分区差异**：方法在不同任务类型（QA vs CODE vs C.TEXT）和风险指标（OOD vs PERT）上的表现存在显著异质性，说明单一基准的评估结论不可泛化。

### 消融实验的关键洞察

**法官配置消融**（Fig. 11）揭示了影响评估质量的细粒度因素：较大法官模型与精确正确性的一致性更好，尤其在COLLIE上；提示设计对评估质量影响显著，尤其在需要隐式计算的结构化任务上；采样温度的影响相对较小。这些发现为实际部署SP-MoJI时的法官选择提供了指导。

**MoJI与人工标注的相关性**（Fig. 7）验证了方法的生态效度：在CoQA的300个问答样本上，MoJI与人工标注的相关性通常高于单个法官的平均相关性，说明集成策略不仅降低方差，还提升了与人类判断的一致性。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_OxWnOV5q8w/figures/010_Figure_7.jpg]]
*Figure 7: Correlation of MoJI to human annotators on a sample of 300 question-answers from CoQA. MoJI shows higher correlation to human annotators than individual judges on average. Figure 8: Average Rank (Left) vs Elo score (Rank) evaluated for the complete and synthetic indirect comparison scenarios. For ranks: lower is better, for Elo scores higher is better*

**标签扭曲分解的实证验证**（Fig. 9）确认了Eq. (27)的理论推导在合成数据上的准确性，在$10^3$样本量（常见QA数据集规模）下分解公式的偏差低、方差小，为理解标签偏差如何影响不同方法提供了可量化的分析工具。

### 失败模式与局限

1. **结构化任务的覆盖范围有限**：目前仅覆盖代码完成和约束文本生成两类任务，尚不能代表一般的NLG场景。在更开放式的文本生成中，精确正确性验证仍然不可行。
2. **扰动检测的敏感性**：不同扰动类型和强度可能导致不同的不确定性响应，当前尚未全面分析扰动方案选择带来的偏差。
3. **法官模型的内在偏差无法完全消除**：SP-MoJI虽然降低了方差，但仍依赖于LLM-as-a-judge，法官模型本身对某些回答类型的系统性偏好可能通过集成被保留而非消除。
4. **Elo评分的稳定性条件**：Elo系统的解释性依赖于大量比赛的均匀采样，在任务高度异构或数据稀疏时可能不稳定。Fig. 6展示了各实验子集上Elo评分的收敛过程，可作为稳定性判断的参考。
5. **高级NLG设置的缺失**：链式推理（CoT）、多智能体对话、更长文本生成等设置尚未纳入评估框架，这些场景下的正确性评估面临更大的挑战。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_OxWnOV5q8w/figures/006_Figure_4.jpg]]
*Figure 4: Agreement of ordering UE methods on TruthfulQA*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_OxWnOV5q8w/figures/001_Table_1.jpg]]
*Table 1: Evaluation protocols recently used for uncertainty estimation in NLG. Few works evaluate their methods beyond selective prediction on QA tasks and rely on approximate correctness functions or a small number of human correctness evaluations*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_OxWnOV5q8w/figures/008_Table_3.jpg]]
*Table 3: Accuracies of the models for evaluated datasets according to corresponding correctness functions. This table lists the dataset / model papers evaluated in this work. Nan values in SQUAD is expected behavior, as there are no correctness labels for the artificially unanswerable OOD part. Known-Unknown (Amayuelas et al., 2024) dataset generations were performed without accuracy computation as we used it strictly as an OOD detection dataset*

## 定位与知识库关联

### 当前评估协议的瓶颈与本文的定位

NLG不确定性估计的评估长期依赖一个隐含假设：近似正确性函数（如ROUGE‑L、BLEURT、LLM‑as‑a‑judge）能够可靠地替代真实正确性标签。本文通过系统分析揭示了这一假设的脆弱性——不同近似正确性函数之间存在显著分歧，直接导致不确定性估计方法的排名不一致（Fig. 1）。Table 1汇总了近期工作的评估协议，显示大多数方法仅依赖QA任务上的选择性预测和近似正确性函数，缺乏对评估协议本身偏差的审视。本文的核心贡献不在于提出新的不确定性估计方法，而是**重新设计评估协议**，使其对正确性标签的偏差和方差具有更强的鲁棒性。

### 方法谱系：从单点评估到参数边缘化

本文提出的评估框架包含三个互补的改进维度，构成了从“单点近似评估”到“参数边缘化评估”的方法谱系：

**（1）SP‑MoJI：在近似正确性空间中的参数边缘化。** 传统选择性预测使用单一近似正确性函数作为风险指标：

$$\xi_{\mathrm{SP}} = \mathrm{Cor}\left[ \hat{u}(x_i, w; \pmb{\theta}_u), \lnot c(\pmb{y}_i', \pmb{y}_i, \pmb{x}_i; \pmb{\theta}_c) \right]$$

其中正确性函数 $c$ 的参数 $\pmb{\theta}_c$（包括法官模型、提示模板、采样温度等）被视为固定值。SP‑MoJI将这一评估扩展为对 $K$ 个不同法官/指令变体的期望：

$$\xi_{\mathrm{SP-MoJI}} = \mathrm{E}_{\theta_c}[\xi_{\mathrm{SP}}] \approx \frac{1}{K}\sum_{k=1}^{K} \mathrm{Cor}\left[ \hat{u}(x_i, w; \theta_u), \lnot J_k(y_i', y_i, x_i; \theta_k) \right]$$

这一设计的因果机制在于：通过边缘化正确性标签的参数空间，降低了评估统计量的方差（Fig. 2显示4个法官可使标准差降低约两倍）和偏差（消融实验显示MoJI与人工标注的相关性高于单个法官的平均相关性，Fig. 7）。

**（2）结构化任务中的精确正确性验证。** 在代码完成（BigCodeBench）和约束文本生成（COLLIE）等可符号验证的任务上，正确性函数 $c_e$ 是确定性和非参数化的，完全消除了对标签边缘化的需求。这构成了评估协议的一个极端但理想的参考点——近似正确性函数的质量可以通过其与精确正确性的一致性来衡量（Fig. 10、Fig. 11）。

**（3）多维风险指标与Elo聚合。** 传统评估仅使用选择性预测的否定正确性作为风险指标，本文将其扩展为选择性预测、分布外检测（OOD）、扰动检测和结构化任务精确正确性的四维风险空间。扰动检测的公式为：

$$\xi_{\mathrm{perturb}} = \frac{1}{N}\sum_{i=1}^{N} \mathrm{Cor}\left[ \hat{u}(p(\pmb{x}_i, s_p), \pmb{w}; \pmb{\theta}_u), s_p \right]$$

通过Elo评分系统汇总跨任务、跨模型、跨风险指标的多维实验结果，提供概率化解释和间接比较能力（Fig. 3）。

### 适用边界与局限

**适用边界：**
- SP‑MoJI适用于必须使用近似正确性函数的QA类任务，在4–10个法官调用范围内收益显著，超过10个法官的收益递减（Fig. 2消融）。
- 结构化任务评估适用于输出可符号验证的场景（代码生成、约束文本生成），目前覆盖的任务类型有限。
- Elo聚合依赖于大量实验的均匀采样，在任务高度异构或实验数量不足时可能不稳定（Fig. 6展示收敛过程）。

**已知局限：**
- 结构化任务的种类有限（仅代码完成和约束文本生成），可能不能完全代表一般的NLG场景。
- 扰动检测中，扰动类型和强度的选择尚未全面分析其偏差，不同扰动可能导致不同的不确定性响应。
- MP‑MoJI虽然降低了方差，但仍依赖于LLM‑as‑a‑judge，无法完全消除法官模型本身的内在偏差。
- 未在链式推理（CoT）、多智能体或更长文本生成等高级NLG设置下验证所提议的评估框架。

### 开放问题

1. **标签噪声的理论分析**：如何推导Spearman $\rho$ 在标签噪声/扭曲条件下的解析表达式？当前仅有AUROC在独立伯努利噪声下的分析（Eq. 3）和样本依赖扭曲的分解（Eq. 5, Eq. 27），但秩相关统计量的理论性质尚不明确。

2. **扰动检测的标准化**：不同扰动检测任务中性能差异的根本原因是什么？如何设计无偏的通用扰动方案，使其在不同任务和模型间具有可比性？

3. **降低法官依赖**：能否开发出更廉价且偏差更低的自动正确性函数？MoJI的高熵样本是否可以作为QA数据集质量问题的一种自动筛选手段？

4. **扩展到复杂NLG设置**：在CoT、多步推理、多智能体对话等更复杂的NLG设定下，如何适配和扩展当前提出的评估框架？论文指出“参数边缘化和有效聚合的基本原则在这些设置中仍然是必要的”，但具体适配方案留待未来工作。

5. **评估协议的形式化标准化**：如何形式化并控制正确性函数参数选择中的自由度，以建立更严格的评估协议标准？当前对抗性选择正确性函数可以显著操纵方法排名（Table 2：G‑NLL的Top‑3频率从0.375升至0.688），表明评估协议的自由度需要被显式约束。

## 原文 PDF

![[paperPDFs/ICLR_2026/Addressing_Pitfalls_in_the_Evaluation_of_Uncertainty_Estimation_Methods_for_Natural_Language_Generation.pdf]]
