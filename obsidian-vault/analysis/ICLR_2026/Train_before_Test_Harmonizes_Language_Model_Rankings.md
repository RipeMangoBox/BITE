---
title: "Train-before-Test Harmonizes Language Model Rankings"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Train_before_Test_Harmonizes_Language_Model_Rankings.pdf
project_link: null
code_link: https://github.com/socialfoundations/lm-harmony
openreview_forum_id: ORv3SAzus1
aliases:
- TBT
- TBTHLMR
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "在评估前对每个模型进行统一的基准特定微调（train-before-test），消除任务预备程度的差异。"
primary_logic: "通过标准化微调挖掘模型潜力，使得跨基准排名高度一致，模型潜力主要由单一潜在因素（与预训练计算量相关）决定，并恢复了困惑度与下游性能的关系。"
claims:
- "平均 Kendall's τ 从 0.52 提升至 0.76，274/276 个基准对排名一致性提高。"
- "NQ-Open 与其他基准的平均 Kendall's τ 从 0.23 提升至 0.74。"
- "困惑度排名与下游基准排名的一致性从 0.48 提升至 0.74。"
- "第一主成分解释方差比例从 70% 提高到 86%，对于 Qwen 家族达 93%。"
---

# Train-before-Test Harmonizes Language Model Rankings

> [!tip] 核心洞察
> 通过标准化微调挖掘模型潜力，使得跨基准排名高度一致，模型潜力主要由单一潜在因素（与预训练计算量相关）决定，并恢复了困惑度与下游性能的关系。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 先训练后测试统一语言模型排名 |
| 英文题名 | Train-before-Test Harmonizes Language Model Rankings |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=ORv3SAzus1) · [GitHub](https://github.com/socialfoundations/lm-harmony) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | train-before-test |
| Dataset | 24 个基准平均, NQ-Open 与其他基准平均, 困惑度 vs 下游平均, 所有模型 PC1 解释方差 |

> [!tip] 效果简介
> - 24 个基准平均 上，Kendall's τ (排名一致性) 为 0.76，对比 0.52 (direct zero-shot)，变化 +0.24。
> - NQ-Open 与其他基准平均 上，Kendall's τ 为 0.74，对比 0.23，变化 +0.51。
> - 困惑度 vs 下游平均 上，Kendall's τ 为 0.74，对比 0.48，变化 +0.26。

## 概要

当前语言模型评估面临一个根本性困境：直接评估（zero-shot 或 few-shot）下，不同基准给出的模型排名相互矛盾，即使同属问答类别的基准之间排名一致性也较低。这一瓶颈的根源并非模型能力本身不可比较，而是各模型在预训练阶段对特定任务数据的暴露程度不同，导致它们在评估时的“预备程度”参差不齐。

本文提出的 **train-before-test** 方法直击这一因果关键：在评估之前，对每个模型进行统一的基准特定微调，消除任务预备程度的差异，从而挖掘模型的真实潜力。其核心洞见在于——一旦通过标准化微调使所有模型处于同一起跑线，跨基准的模型排名便呈现出高度一致性，且模型潜力主要由单一潜在因素（与预训练计算量高度相关）所主导，同时恢复了困惑度与下游性能之间曾被削弱的相关性。

**关键实证结果：**

- 在 24 个基准上，train-before-test 将平均 Kendall's τ 从 0.52 提升至 0.76，274/276 个基准对的排名一致性得到改善（Figure 2）。
- 原本最异常的 NQ-Open 基准，与其他基准的平均 τ 从 0.23 跃升至 0.74（Table 5）。
- 困惑度排名与下游基准排名的一致性从 0.48 恢复至 0.74（Figure 4）；对于 base 模型，微调前的困惑度即可有效预测微调后的下游排名（平均 τ=0.78，Figure 5）。
- 基准得分矩阵的第一主成分解释方差比例从 70% 提高至 86%，在 Qwen 家族中更达 93%（Figure 6, Figure 8），表明模型潜力近似由单一维度决定。

**方法定位：** train-before-test 并非新的微调技术，而是一种评估范式的转变——将参数高效微调（PEFT/LoRA）作为评估前的标准化预备步骤，使模型排名从“谁准备得更充分”变为“谁的潜力更强”。该方法可视为对传统直接评估协议的根本性修正，其效力在控制模型规模、模型家族后依然稳健（Table 6, Table 7），且在使用统计显著性修正的 Kendall's τ-b 下结论不变（Figure 12）。

**局限与待解决问题：** 微调增加了评估成本；部分基准不再公开训练数据，或商业模型不允许微调，限制了方法适用范围。排名一致性仍未达到完美，残差可能源于 PEFT 的适应局限或不可约的测量噪声。YI 家族改善有限的原因、以及如何设计更轻量的 train-before-test 变体，仍需进一步探索。



语言模型评估的核心挑战在于：不同基准给出的模型排名往往相互矛盾。即使两个基准测试的是同一类能力，模型在它们上的表现排名也可能大相径庭。例如，在 Natural Questions Open 和 ARC Challenge 这两个问答基准上，直接评估下 61 个模型的排名存在显著分歧——统计上不可调和的反转随处可见（Figure 1 上半部分）。这种不一致性并非个例：在所有 24 个基准中，直接评估的成对排名一致性（Kendall's τ）平均仅为 0.52，且同类任务内部的排名一致性同样偏低。

**根本瓶颈**在于模型对基准任务的“预备程度”不同。由于预训练数据的差异，不同模型在预训练阶段接触基准相关数据的程度参差不齐。一些模型可能已经“见过”类似任务格式或领域内容，而另一些则没有。这种差异在直接评估（无论是 zero-shot 还是 few-shot）中被完整保留，导致评估结果混杂了模型固有能力和任务熟悉度两个不可分离的因素。因此，直接评估给出的排名反映的是“模型在当前状态下对该任务的表现”，而非“模型在同等准备下的潜力”。

**现有方法的局限**同样明显。Few-shot 评估通过提供少量示例来缓解任务格式的陌生感，但无法从根本上消除数据暴露程度的差异——模型仍然可能因预训练中接触过类似数据而占据优势。实验表明，5-shot 直接评估虽将平均 Kendall's τ 从 0.52 提升至 0.61，但仍远低于本文方法达到的 0.76，且仅在 89% 的基准对上优于 zero-shot。这意味着 few-shot 提示只能部分弥合预备程度的鸿沟，排名矛盾的根本问题依然存在。

**本文的动机**由此明确：如果能在评估之前消除模型间任务预备程度的差异，是否就能获得稳定、一致的模型排名？换言之，是否存在一个单一的“模型潜力”因素，能够在跨基准的标准化评估中被可靠地捕捉？这一动机驱动了 train-before-test 方法的提出——在评估前对每个模型进行统一的基准特定微调，使所有模型以同等准备状态进入测试，从而将评估焦点从“当前表现”转向“可挖掘潜力”。



## 核心方法与创新机理

本文的核心创新在于提出 **train-before-test** 评估范式：在评估前对每个模型进行统一的基准特定微调，从而消除因预训练数据差异导致的任务预备程度不同，挖掘模型的真实潜力。

### 问题瓶颈

直接评估（zero-shot）下，语言模型的排名严重依赖于其预训练数据与基准任务的偶然重叠程度。不同模型在预训练阶段接触基准相关数据的程度各异，导致即使在同一类任务（如问答）上，排名也出现显著分歧。例如，NQ-Open 与其他基准的平均 Kendall's τ 仅为 0.23，远低于整体平均的 0.52，表明该基准在直接评估下几乎无法反映模型在其他任务上的表现。这种排名不一致性使得任何单一基准的评估结果都难以推广。

### 因果调节变量

**Train-before-test** 通过标准化微调这一单一操作，切断了“预训练数据暴露程度”这一混杂因素对排名的影响。具体而言，该方法在评估前对每个模型在目标基准的训练集上进行参数高效微调（PEFT/LoRA），使所有模型在相同的任务数据上获得同等的适应性准备。这一操作将评估焦点从“模型已知道什么”转向“模型能够学会什么”，即从测量静态知识转向测量学习潜力。

### 方法槽位变更

| 槽位 | 传统方法 (Direct Evaluation) | Train-before-test |
|------|---------------------------|-------------------|
| 预评估微调 | 无微调，直接评估 | 在基准训练集上进行 5 epoch 微调（PEFT/LoRA），学习率搜索 {1e-5, 2e-5, 5e-5} |
| 模型预备程度 | 模型可能已不同程度接触类似数据 | 所有模型接受相同的任务特定微调以确保同等准备 |
| 评估协议 | zero-shot 或 few-shot 直接评估 | 微调后 zero-shot 评估 |

### 核心洞察

标准化微调后，跨基准的模型排名呈现出高度一致性：平均 Kendall's τ 从 0.52 提升至 0.76，274/276 个基准对的排名一致性得到改善。更重要的是，基准得分矩阵的第一主成分解释方差比例从 70% 跃升至 86%（同一模型家族内可达 93%），表明模型潜力主要由单一潜在因素主导。该因素与预训练计算量呈正相关，恢复了困惑度与下游性能之间的强关联（Kendall's τ 从 0.48 提升至 0.74）。这一发现意味着，经过统一微调后，模型的能力本质上是一维的——更多的预训练计算量系统性地转化为更强的下游任务学习潜力。

### 与 Few-shot 评估的区别

Few-shot 直接评估（平均 τ=0.61）虽能在一定程度上提高排名一致性，但其效果远逊于 train-before-test（τ=0.76），且仅在 89% 的基准对上优于 5-shot 直接评估。Few-shot 提供的是上下文示例，而 train-before-test 通过参数更新使模型真正适应任务分布，两者的机制本质不同。



train-before-test 的核心主张是：**在评估前，通过统一的基准特定微调消除模型对任务预备程度的差异，从而挖掘模型潜力并实现跨基准排名的一致性**。该框架由三个顺序模块构成：微调模块、评估模块和排名度量模块。

### 微调模块

对于每一个目标基准，所有待评估模型均在该基准的训练集上进行参数高效微调（PEFT），采用 LoRA 方法。微调统一设定为 5 个 epoch，学习率从 {1e-5, 2e-5, 5e-5} 中搜索。这一步骤的关键在于**标准化**——无论模型在预训练阶段是否接触过类似数据，均在此阶段获得同等的任务特定准备，从而剥离因数据暴露差异造成的排名噪声。

### 评估模块

微调完成后，使用 lm-eval-harness 库对模型进行 zero-shot 评估。与传统的 zero-shot 或 few-shot 直接评估不同，此处的 zero-shot 评估发生在模型已经过任务特定微调之后，因此衡量的是模型在同等预备条件下的表现，而非原始预训练状态的零样本能力。

### 排名度量模块

评估得到各模型在多个基准上的得分后，计算基准对之间的 Kendall's τ 以量化排名一致性。为处理统计不显著的性能差异，框架采用 Kendall's τ-b 变体，将不显著差异视为平局。最终通过平均所有基准对的 τ 值，获得整体排名一致性指标。

### 输入输出流

```
输入: 待评估模型集合 × 基准集合（含训练集和测试集）
  │
  ├─→ [微调模块] → 每个模型在每个基准上获得微调后的 checkpoint
  │
  ├─→ [评估模块] → 每个模型在每个基准上的 zero-shot 得分
  │
  └─→ [排名度量模块] → 基准对之间的 Kendall's τ 矩阵
                        → 平均排名一致性
                        → 主成分分析（PCA）揭示潜在因子结构
```

框架的最终输出不仅是排名一致性指标，还包括对模型得分矩阵的 PCA 分解——在 train-before-test 条件下，第一主成分可解释 86% 的方差（所有模型），在 Qwen 家族内更高达 93%，表明模型潜力主要由单一潜在因素主导，且该因素与预训练计算量正相关。



### 关键模块

train-before-test 方法的核心流程由三个模块串联构成，其设计目标是在评估前消除模型对基准任务预备程度的差异。

**微调模块**：对每个待评估模型，在目标基准的训练集上进行参数高效微调（PEFT），具体采用 LoRA（Hu et al., 2021; Mangrulkar et al., 2022）。微调超参数固定为 5 个 epoch，学习率在 {1e-5, 2e-5, 5e-5} 中搜索最优值。该模块的作用是让所有模型在相同的任务特定数据上获得等效的“准备”，从而消除因预训练数据差异导致的任务暴露程度不均。

**评估模块**：微调完成后，使用 lm-eval-harness 库对模型进行 zero-shot 评估。与直接评估协议的关键区别在于，此处的 zero-shot 评估发生在统一微调之后，而非直接作用于原始模型。

**排名度量模块**：计算跨基准的模型排名相关性，核心指标为 Kendall's τ。具体采用 Kendall's τ-b 以正确处理模型间性能差异不显著时的平局情况（通过标准误差和 t-test 判定显著性，将不显著的差异视为平局）。

### 关键公式

本文未引入新的理论公式，其分析框架建立在标准的 Kendall's τ 相关系数和主成分分析（PCA）之上。排名一致性的核心度量直接使用 Kendall's τ 统计量，该系数衡量两组排名之间的序关系一致性。主成分分析则直接作用于基准得分矩阵（模型 × 基准），通过各主成分的解释方差比例来衡量模型潜力是否由单一潜在因素主导。

由于论文未提供自定义的公式推导，此处仅记录其使用的标准统计量，不做公式猜测。若需精确的 Kendall's τ 定义或 PCA 分解形式，可参考原始文献（Kendall, 1938）及标准多元统计教材。



## 实验与关键发现

### 核心实验设置

本研究在 24 个基准上评估了 61 个语言模型（涵盖多个模型家族，见 Table 2）。基准按任务类型分为六类：语言理解（LU）、常识推理（CR）、问答（QA）、理化生（PBC）、数学（Math）和医学（Med）（见 Table 1）。实验对比两种评估协议：

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_ORv3SAzus1/figures/002_Table_1.jpg]]
*Table 1: We categorize benchmarks into language understanding (LU), commonsense reasoning (CR), question answering (QA), physics/biology/chemistry (PBC), math (Math), and medicine (Med)*

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_ORv3SAzus1/figures/003_Table_2.jpg]]
*Table 2: Models considered, categorized by model family*

- **直接评估**：对模型进行 zero-shot 直接评估，不进行任何微调。
- **train-before-test**：在评估前，对每个模型在目标基准的训练集上进行 5 epoch 的参数高效微调（PEFT/LoRA），学习率从 {1e-5, 2e-5, 5e-5} 中搜索，随后进行 zero-shot 评估。

排名一致性使用 Kendall's τ 衡量，并采用 τ-b 变体处理统计不显著的性能差异（将其视为平局）。

### 主结果：排名一致性的大幅提升

**全局排名一致性。** train-before-test 将 24 个基准间的平均 Kendall's τ 从 0.52（直接评估）提升至 0.76，在 276 个基准对中，有 274 对实现了排名一致性改善（Figure 2）。对于直接评估下与所有其他基准平均 τ 仅 0.23 的 NQ-Open，train-before-test 将其提升至 0.74（Table 5），表明该方法能有效修复原本高度不一致的基准。

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_ORv3SAzus1/figures/019_Table_5.jpg]]
*Table 5: We calculate Kendall’s τ between each benchmark and every other benchmark, and then average the results*

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_ORv3SAzus1/figures/004_Figure_2.jpg]]
*Figure 2: Mean ranking agreement between each benchmark and all others. We calculate Kendall’s τ between each benchmark and every other benchmark, and then average the results. Compared to direct evaluation, train-before-test consistently improves ranking agreement. A detailed comparison of Kendall’s τ values for every benchmark pair is provided in Appendix B.1. On average, the overall average Kendall’s τ is 0.52 for direct evaluation and 0.76 for train-before-test*

**跨类别一致性。** 无论是类别内还是类别间，train-before-test 均一致地提升了排名一致性（Figure 3）。例如，语言理解类别的类内平均 τ 从 0.52 升至 0.75，数学类别从 0.55 升至 0.84。这表明 train-before-test 消除了因任务准备程度不同而造成的类别间排名分歧。

**与困惑度的关系恢复。** 直接评估下，困惑度排名与下游基准排名的平均 τ 仅为 0.48；train-before-test 将其恢复至 0.74（Figure 4）。值得注意的是，困惑度排名自身在不同评估方案下均保持高度一致（平均 τ 分别为 0.76 和 0.78），说明困惑度是稳定的模型内在属性，而直接评估掩盖了其与下游性能的真实关系。

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_ORv3SAzus1/figures/007_Figure_4.jpg]]
*Figure 4: Ranking agreement between perplexity rankings and downstream benchmark rankings under direct evaluation (top) and train-before-test (bottom). Perplexity rankings are consistent with each other under both evaluation schemes, with an average Kendall’s τ of 0.76 and 0.78, respectively. However, for direct evaluation, agreement between perplexity rankings and downstream rankings is low, with an average Kendall’s τ of just 0.48. Fortunately, train-before-test results in higher agreement between perplexity and downstream, increasing average Kendall’s τ to 0.74*

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_ORv3SAzus1/figures/008_Figure_5.jpg]]
*Figure 5: Ranking agreement between perplexity rankings before fine-tuning (direct evaluation) and downstream benchmark rankings after fine-tuning (train-before-test) for base models (top) and instruction-tuned models (bottom). Unlike Figure 4 where both rankings in each comparison use the same evaluation scheme, here we test whether pre-fine-tuning perplexity can predict postfine-tuning downstream performance. Base models show strong correlation (average Kendall’s τ = 0.78), suggesting perplexity is a good predictor of model potential. This indicates that the ranking consistency we observe reflects inherent model potential rather than artifacts introduced by fine-tuning. Instruction-tuned models sho...*

**模型潜力由单一因素主导。** 对基准得分矩阵进行主成分分析（PCA），train-before-test 将第一主成分（PC1）的解释方差比例从 70% 提升至 86%（Figure 6）。对于 Qwen 家族，这一比例高达 93%（Figure 8），得分矩阵几乎退化为秩 1。进一步分析表明，PC1 得分与预训练计算量（FLOPs）正相关（Figure 7），说明 train-before-test 揭示的模型潜力主要由预训练投入这一单一潜在因素决定。

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_ORv3SAzus1/figures/018_Table_4.jpg]]
*Table 4: The models used in Figure 7. The number of training tokens of these models is publicly available. We compute the number of pre-training FLOPs as 6 × #Parameters × #Tokens*

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_ORv3SAzus1/figures/010_Figure_6.jpg]]
*Figure 6: Explained variance ratios of the top five principal components of the benchmark score matrix, under direct evaluation (left) and train-before-test (right). Train-before-test substantially increases the amount of variance explained by the first principal component, from 70% to 86%. This indicates the model potential is dominated by one single latent factor*

**预微调困惑度预测微调后性能。** 对于 base 模型，直接评估时的困惑度排名与 train-before-test 后的下游排名高度相关（平均 τ=0.78，Figure 5 上），表明困惑度是模型潜力的良好预测指标。但对于 instruction-tuned 模型，这一相关性显著下降（平均 τ=0.51，Figure 5 下），说明指令微调可能引入了额外的干扰因素。

### 消融实验与鲁棒性分析

**Few-shot 对比。** 5-shot 直接评估的平均 τ 为 0.61，虽优于 zero-shot 的 0.52，但仍远低于 train-before-test 的 0.76，且仅在 89% 的基准对上优于 5-shot（Appendix B.4; Table 5）。这表明增加上下文示例无法替代统一的微调准备。

**模型规模控制。** 按模型规模分 bin 后，train-before-test 在各个规模区间内均一致提升排名一致性（Table 6），排除了“仅对大模型或小模型有效”的可能性。

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_ORv3SAzus1/figures/020_Table_6.jpg]]
*Table 6: The overall average Kendall’s τ across all benchmark pairs for models in each size bin*

**模型家族分析。** 对于不同模型家族，train-before-test 均提高排名一致性（Table 7），但 YI 家族改善有限。这可能源于该家族内部预训练计算量差异较小，导致模型潜力本身趋同，而非方法失效。

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_ORv3SAzus1/figures/021_Table_7.jpg]]
*Table 7: The overall average Kendall’s τ across all benchmark pairs for each model family*

**统计显著性处理。** 使用 Kendall's τ-b 并排除不显著差异后，train-before-test 仍将平均一致性从 0.58 提升至 0.77（Figure 12），跨类别一致性同样全面提升（Figure 13），验证了结果的统计稳健性。

### 失败模式与局限

**GEMMA 模型的困惑度异常。** 在困惑度实验中，8 个 GEMMA 模型因 lm-eval-harness 的滚动窗口实现问题，在 Wiki 和 Stack 数据集上表现出异常高的 bits per byte（Table 3），被排除出分析。这一技术细节提示困惑度评估对实现方式敏感。

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_ORv3SAzus1/figures/016_Table_3.jpg]]
*Table 3: Bits per byte (BPB) of eight excluded GEMMA models compared to PYTHIA-410M across the three newly collected corpora. The GEMMA models exhibit abnormally high BPB values on Wiki and Stack, likely due to the greater average sequence length in these two datasets. Specifically, Arxiv has an average of 163 words per document, compared to 250 for Stack and 1502 for Wiki*

**残差不完美相关性。** 尽管 train-before-test 大幅提升了排名一致性，但相关性仍未达到完美（τ=1.0）。可能的原因包括：PEFT 无法完全适应所有任务、基准本身存在不可约的测量噪声，或某些模型家族（如 YI）的潜力差异确实较小。

**实际应用的障碍。** 许多现代基准不再公开训练数据，且部分商业模型不允许微调，限制了 train-before-test 的适用范围。此外，微调增加了评估成本，但作者指出可通过减少所需基准数量来抵消——因为排名一致后，少量基准即可可靠地反映模型潜力。

### 补充图表

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_ORv3SAzus1/figures/022_Table_8.jpg]]
*Table 8: Explained variance ratios for the top five principal components of the score matrix for each model family, under direct evaluation and train-before-test, respectively*



## 定位与知识库关联

### 1. 方法定位：从“直接评估”到“标准化潜力评估”

传统语言模型评估遵循**直接评估**范式：模型完成预训练或指令微调后，直接在各类基准测试上进行 zero-shot 或 few-shot 推理，以得分排名。这一范式隐含假设所有模型对基准任务的“预备程度”相当。然而，由于不同模型在预训练阶段对基准相关数据的暴露程度差异显著，该假设在实践中并不成立——即使是同类任务（如问答）的不同基准之间，模型排名也常出现严重分歧。

本文提出的 **train-before-test** 方法对这一范式进行了根本性修正。其核心操作是在评估前引入一个统一的**基准特定微调**步骤：对每个待评估模型，使用相同基准训练集进行参数高效微调（PEFT/LoRA），使所有模型在评估前获得同等的任务预备。这一设计将评估目标从“模型当前表现”转向“模型潜力”，从而消除了预训练数据差异带来的混淆效应。

### 2. 与基线方法的对比

| 评估协议 | 平均 Kendall's τ | 核心差异 |
|---------|-----------------|---------|
| Direct evaluation (zero-shot) | 0.52 | 模型预备程度不均，排名一致性低 |
| Direct evaluation (few-shot, 5-shot) | 0.61 | 通过上下文示例部分缓解预备差异，但仍远低于 train-before-test |
| **Train-before-test** | **0.76** | 通过统一微调消除预备差异，排名高度一致 |

Few-shot 直接评估（平均 τ=0.61）虽较 zero-shot 有所提升，但仅在 89% 的基准对上优于 5-shot 评估，且提升幅度有限。这揭示了一个关键洞察：**上下文示例无法替代对模型进行任务特定适配**——模型潜力的释放需要参数层面的更新，而非仅仅在推理时提供格式引导。

### 3. 适用边界与约束条件

**有效范围**：
- 该方法在 24 个涵盖语言理解、常识推理、问答、理化生、数学、医学的基准上得到验证，274/276 个基准对的排名一致性均有提升。
- 对于不同模型家族（LLaMA、Mistral、Qwen、Yi 等）和不同规模区间，train-before-test 均能提升排名一致性。
- 该方法恢复了困惑度与下游性能的相关性（τ 从 0.48 提升至 0.74），表明其挖掘的“模型潜力”与预训练质量密切相关。

**约束与局限**：
1. **数据可用性限制**：许多现代基准不再公开训练数据，使得 train-before-test 无法直接应用。这是该方法推广面临的最主要障碍。
2. **模型可微调性限制**：部分商业模型（如 GPT-4 等闭源 API 模型）不允许微调，无法纳入该评估框架。
3. **计算成本增加**：每个模型-基准对需进行一次微调，增加了评估开销。但论文指出，由于排名高度一致，可大幅减少所需评估的基准数量，从而部分抵消额外成本。
4. **残差不完美一致性**：即使经过 train-before-test，排名一致性仍未达到完美。可能原因包括 PEFT 的适配能力有限，或存在不可约的测量噪声。
5. **家族内差异**：Yi 模型家族在 train-before-test 下的改善相对有限，可能由于该家族内模型预训练计算量差异较小，导致潜力本身相近。

### 4. 与相关工作的关系

**评估一致性研究**：此前研究已注意到直接评估下模型排名的不稳定性，但多聚焦于 prompt 敏感性或评估指标选择。train-before-test 从更根本的层面——模型对任务的预备程度——切入问题，提供了一种系统性解决方案。

**微调作为评估工具**：该方法将标准化微调重新定位为评估工具，而非单纯的能力提升手段。这一视角转换使得微调从“改变模型”变为“揭示模型”，与传统的微调研究形成互补。

**模型潜力与预训练计算**：train-before-test 揭示的模型潜力主要由单一潜在因素主导——第一主成分解释方差达 86%（所有模型）至 93%（Qwen 家族），且该因素与预训练计算量正相关。这一发现将评估结果与 scaling laws 研究建立了直接联系。

### 5. 开放问题

1. **残差不一致性的归因**：排名一致性未达完美究竟源于 PEFT 的适配瓶颈，还是评估本身的测量噪声？全微调与 PEFT 的对比实验可能提供答案。
2. **无训练数据场景的扩展**：能否利用弱监督信号或合成数据模拟统一预备过程，使 train-before-test 适用于不公开训练集的基准？
3. **Yi 家族异常**：为何 Yi 家族在 train-before-test 下改善有限？这是否暗示该家族模型潜力本身高度同质化，还是存在其他未被控制的混淆因素？
4. **轻量化变体设计**：能否通过更高效的微调策略（如更少 epoch、更小学习率搜索空间、或 adapter 共享）降低计算成本，同时保持排名一致性的提升效果？
5. **指令微调模型的特殊性**：对于 instruction-tuned 模型，预微调困惑度与微调后下游排名的相关性较弱（平均 τ=0.51），表明指令微调过程可能引入了额外的、与预训练质量不完全对齐的变异来源。这一现象的机制尚待深入探究。



## 原文 PDF

![[paperPDFs/ICLR_2026/Train_before_Test_Harmonizes_Language_Model_Rankings.pdf]]
