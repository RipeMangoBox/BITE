---
title: "Accessible, Realistic, and Fair Evaluation of Positive-Unlabeled Learning Algorithms"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Accessible_Realistic_and_Fair_Evaluation_of_Positive_Unlabeled_Learning_Algorithms.pdf
aliases:
- PBPAPMSIC
- ARFEPULA
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "①仅使用正例与未标注验证数据的代理准确率(PA)与代理AUC(PAUC)进行模型选择；②通过将正例集合并入未标注损失项以校准单样本设置下的数据分布，消除ILS偏差。"
primary_logic: "用PU数据可计算的无偏替代指标（PA/PAUC）进行超参数调优，并通过对未标注集增补正例来消除单样本设置的标签偏移，能在不引入负例的前提下实现现实且公平的跨家族PU算法比较；没有单一算法全面胜出，方法选择应视具体任务而定。"
claims:
- "两样本PU算法在单样本设置下不经校准时性能显著下降，揭示现有文献中偏向单样本评估的陷阱。"
- "提出的校准技术持续提升两样本方法在单样本设置下的分类性能。"
- "PA/PAUC验证指标在超参数选择中有效，但有效性依赖于测试指标类型。"
- "CIFAR-10 Case 1 上 Test Accuracy = uPU-c (with calibration) 86.48 ± 0.21"
---

# Accessible, Realistic, and Fair Evaluation of Positive-Unlabeled Learning Algorithms

> [!tip] 核心洞察
> 用PU数据可计算的无偏替代指标（PA/PAUC）进行超参数调优，并通过对未标注集增补正例来消除单样本设置的标签偏移，能在不引入负例的前提下实现现实且公平的跨家族PU算法比较；没有单一算法全面胜出，方法选择应视具体任务而定。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 可访问、现实且公平的PU学习算法评估 |
| 英文题名 | Accessible, Realistic, and Fair Evaluation of Positive-Unlabeled Learning Algorithms |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=5R11h5o44C) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | PU Benchmark with Proxy Accuracy/PAUC Model Selection and ILS Calibration |
| Dataset | CIFAR-10 Case 1, ImageNette Case 1, CIFAR-10 Case 2, USPS Case 2 |

> [!tip] 效果简介
> - CIFAR-10 Case 1 上，Test Accuracy 为 uPU-c (with calibration) 86.48 ± 0.21，对比 uPU (without calibration) 82.04 ± 0.49，变化 +4.44%。
> - ImageNette Case 1 上，Test Accuracy (OA validation) 为 CVIR 81.01 ± 0.67，对比 PAN 53.29 ± 0.94，变化 +27.72%。
> - CIFAR-10 Case 2 上，AUC (PAUC validation) 为 GLWS 88.08 ± 0.43，对比 uPU 79.81 ± 0.77，变化 +8.27%。

## 概述

**问题瓶颈。** 现有正例-未标注（PU）学习的实验评估存在三个系统性缺陷：其一，实验设置不统一，单样本（OS）与两样本（TS）设定的本质差异被忽视；其二，模型选择普遍依赖包含真实负标签的验证集（如Oracle Accuracy），直接违反PU假设中无负标签可用的前提；其三，将两样本PU算法直接用于单样本设置时，未标注数据内部的标签偏移（Internal Label Shift, ILS）导致性能显著下降，使跨家族比较失效，系统性地低估两样本方法的真实能力。

**核心结论。** 本文提出首个统一的PU学习基准，通过两项关键技术实现可访问、现实且公平的算法评估：（1）仅利用正例与未标注验证数据即可计算的代理准确率（Proxy Accuracy, PA）与代理AUC（Proxy AUC, PAUC）作为模型选择指标，无需真实负标签；（2）针对单样本设置下的ILS问题，提出简单而有效的校准技术，通过将正例集并入未标注损失项以消除标签偏移，使两样本算法在单样本设置下获得公平的性能评估。实验表明，没有单一算法在所有场景中全面胜出，方法选择应依据具体任务、数据集和评估指标而定。

**方法定位。** PA与PAUC作为PU友好的验证指标，分别在类别先验$\pi$已知和未知的条件下，为准确率导向和AUC导向的超参数选择提供无偏替代方案。ILS校准技术（Algorithm 1）可灵活嵌入各类两样本PU算法（如uPU、nnPU、VPU等），使其在单样本设置下不经负标签即可正常工作，从而统一两样本与单样本的评测框架。

**主要结果。** 校准技术在所有数据集（CIFAR-10、ImageNette、USPS、Letter）、算法和评估指标上一致提升分类性能——例如CIFAR-10 Case 1中uPU-c较uPU测试准确率提升$+4.44\%$（86.48% vs. 82.04%）；PA/PAUC在超参数选择中有效，但其相对优势依赖于测试指标类型（如PAUC选出的模型在AUC上通常优于PA所选模型）。综合所有数据集的表现排名（Figure 4）确认，无方法全面占优，不同算法在不同场景下各有擅长，基准测试为公平的跨家族比较提供了可靠依据。

## 背景与动机

正样本-未标注（PU）学习处理仅有一组正例和一组未标注样本的二分类问题，在欺诈检测、医学诊断等现实中广泛存在。尽管已有大量 PU 学习算法，其评估却长期受两个关键缺陷制约：**实验设置不统一**与**模型选择依赖负例**。现有文献往往按各自习惯选择单一数据集和评估协议（通常偏向单样本设置），且超参数调优依赖包含真实负标签的验证集，这不仅违背 PU 学习的核心假设，更使评估结果无法反映真实部署时的可及性。

更隐蔽的缺口出现在算法家族的跨设置比较中。当把为**两样本（TS）设置**（未标注数据仅含负类）设计的算法直接用于**单样本（OS）设置**（未标注数据是正负混合）时，会遭遇**内部标签偏移（ILS）**：TS 方法的损失函数隐式假设未标注集为纯负例，而 OS 中该假设不成立，导致风险估计产生系统性偏差（图 1、图 2）。这使得 TS 类算法在 OS 评估中被严重低估，原有文献中跨家族的比较实质上形成了一种不公平的"评估陷阱"。

针对上述缺口，本文的工作动机在于构建一个**可访问、现实且公平**的 PU 评估框架。具体而言，我们重新考察仅用正例和未标注验证数据就能计算的模型选择指标，提出**代理准确率（PA）**与**代理 AUC（PAUC）**（定义 1、2），摆脱对 oracle accuracy（需要已知负标签）的依赖，使超参数调优完全适应真实 PU 场景。同时，为了消除单样本设置下的 ILS 偏差，我们设计一种简单的**校准策略**（Algorithm 1）：在计算未标注损失时，用正例集补充未标注集，使得补充后的未标注样本分布无偏，从而让 TS 算法在 OS 设置下也能被公正衡量。通过这些努力，我们首次给出一个系统性 PU 学习基准，涵盖多种数据集、正样本比率和两种设置，旨在揭示**没有单一算法全面胜出**的现象，并推动 PU 研究向更可靠的任务导向比较发展。

## 核心创新

现有PU学习评估长期受困于两个互锁的缺陷：**模型选择依赖无法获取的负标签**，以及**忽略单样本（OS）设置下未标注数据的内部标签偏移（Internal Label Shift, ILS）**。这使得跨算法家族（如两样本TS方法与单样本OS方法）的公平比较无法实现。本工作通过三个改变槽位对此进行重构：

1. **PA/PAUC替代OA作为模型选择指标**  
   传统做法使用Oracle Accuracy（OA），其计算需要真实负标签，与PU假设矛盾。本工作定义仅使用正例与未标注验证数据的**Proxy Accuracy (PA)** 与**Proxy AUC (PAUC)**，并提供单调性保证——$\mathbb{E}[\text{PA}]$越高，期望准确率越高（Proposition 1）；$\mathbb{E}[\text{PAUC}]$越高，期望AUC越高（Proposition 2）。由此将超参数选择完全限制于PU可及数据，消除对负例的依赖。

2. **ILS校准技术适配TS→OS**  
   在两样本方法直接用于单样本设置时，未标注训练集并非总体的无偏抽样，导致模型选择与性能评估的系统性偏差（图1, 图2, 图3）。本文提出一种即插即用的校准方法（Algorithm 1）：在计算未标注损失时，将正例集 $D_\mathrm{P}$ 合并进未标注集，使扩充后的集合边际无偏。其风险估计器为  
   
$$
\bar{R}(f) = \frac{\pi}{n_{\mathrm{P}}} \sum_{i=1}^{n_{\mathrm{P}}} \left( \ell(f(\mathbf{x}_i),+1) + (c-1) \ell(f(\mathbf{x}_i),-1) \right) + \frac{1-c\pi}{n_{\mathrm{U}}} \sum_{i=n_{\mathrm{P}}+1}^{n_{\mathrm{P}}+n_{\mathrm{U}}} \ell(f(\mathbf{x}_i),-1)
$$
  
   理论上由泛化界（Theorem 2）保证收敛性，实验上在所有测试任务中一致提升准确率、AUC、F1、精度与召回率（表1‑4, 7‑18中后缀'‑c'对比，如CIFAR‑10 Case 1中uPU由82.04±0.49提升至86.48±0.21），且对多种TS方法有效（uPU, nnPU, Dist‑PU等）。这从原理上消除了因ILS导致的TS方法被低估的"评估陷阱"。

3. **统一的OS/TS基准协议**  
   对比现有文献侧重单样本设置，本基准同时覆盖两种场景，并为TS方法提供ILS校准，使得成本敏感（uPU、nnPU、CVIR）、变分（VPU）、样本选择（PUbN）及生成对抗（PAN）等不同家族算法可以在相同条件下公平排名。整体结果（图4）表明**没有单一算法在所有数据集和指标上碾压对手**，方法选择需视任务而定，这反衬出公平比较的必要性。

上述创新的核心机理在于：用PU可计算的无偏替代指标（PA/PAUC）进行超参数调优，并用校准消除单样本场景的数据分布偏差，从而在不触及负例的前提下，还原真实相对性能。当前证据对模型选择指标的有效性（CIFAR-10、ImageNette、USPS等多数据集一致表现）与校准技术的稳步提升给出强支持（置信度1.0），但PA对类别先验$\pi$的敏感、校准对概率$c$的依赖仍为实际部署留下开放问题。

## 整体框架

![[assets/figures/papers/iclr26_0005_5R11h5o44C_Accessible_Realistic_and_Fair_Evaluation_of_Posi/figures/002_Figure_1.jpg]]
*Figure 1: An example of the comparison of the distribution of unlabeled training data in different PU learning settings*

本工作提出一个统一、可扩展的PU学习基准评估流水线。流水线由四个核心模块串联构成，依次为：**数据生成与设置定义**、**模型选择指标计算**、**内部标签偏移（ILS）校准**及**基准测试执行**。其目标是在不依赖负标签的条件下，为来自不同方法家族（如代价敏感类、样本选择类、生成对抗类）的PU算法提供现实且公平的评估。

流水线从原始多分类数据集（例：CIFAR‑10、ImageNette）出发，按照两类PU学习设定（单样本OS与两样本TS）重新组织正、未标注样本，同时严格划分训练集与验证集。训练集用于模型优化，验证集仅含正例与未标注数据，彻底移除对真实负标签的依赖。这一设计由本文的问题设置自然导出：现实PU场景无法获取验证用负例，因此传统依赖负例的Oracle指标不可用。

随后进入**模型选择指标计算**模块。在构造好的PU验证集上，计算两类仅需正、未标注数据的代理指标——代理准确率（PA）与代理AUC（PAUC）。PA的定义覆盖OS与TS两种设定（定义1），其期望值与真实准确率之间的单调关系由Proposition 1保证；PAUC则直接将未标注样本视为损坏的负例进行计算，且不需要类别先验$\pi$（定义2，Proposition 2保证其与真实AUC的单调关系）。流水线在超参数搜索过程中，根据用户指定的指标（PA或PAUC）在验证集上选择最优模型，从而规避了使用不可获取的负标签信息的陷阱。

当基线算法本身是为两样本（TS）设定设计时，若直接在单样本（OS）训练数据上运行，会遭遇严重的内部标签偏移（ILS）问题——未标注集中因不含补正样本而导致标签分布偏斜，使性能严重下降（图2、图3中的无校准曲线）。此问题由基准流水线中的**ILS校准模块**解决。针对任一TS算法，模块实施Algorithm 1：将正例集$D_{\mathrm{P}}$同时纳入未标注损失项，使得未标注数据的边际分布恢复无偏，从而消除学习过程中的分布偏差。该校准策略由Theorem 2给出的泛化界支撑，且实验表明它在几乎全部算法‑数据集组合上稳定提升准确率、AUC及F1（表1‑4中"‑c"后缀行，置信度0.98）。校准过程不改变算法核心结构，仅调整损失项中数据的利用方式，因此能以极低的实现开销赋予TS方法在单样本设定下公平比较的资格。

完成模型选择（必要时经校准）后，流水线将所有组合送入**基准测试执行**模块：使用统一的骨干网络（图像数据集用ResNet‑34，表格数据集用宽度500的ReLU MLP）和随机搜索超参协议，在每个数据集×设定×算法×验证指标的四维格点上重复实验，最终在测试集上报告准确率、AUC、F1、精确率与召回率（表1‑4、表7‑18）并汇总为整体排名图（图4）。整个流水线严格避免了依赖负标签的任何环节，既还原了真实PU应用场景，又通过ILS校准清除了因设定差异引入的系统性偏差，从而确保跨家族比较的公平性。

> **输入**：原始分类数据集、选取的PU设定（OS/TS）、正样本构建策略（Case 1/Case 2）、类别先验$\pi$的已知值或估计值。  
> **输出**：多套测试指标下的标准化性能表格与图表，及相应最优超参数组合。

## 核心模块与公式推导

作者提出的PU学习评估框架围绕两个核心任务展开：① 在不依赖负例的条件下实现可靠的模型选择（超参数调优）；② 消除单样本（OS）设置下两样本（TS）方法所受的内部标签偏移（ILS）影响。整个流程由四个模块串联：数据生成与设置定义、基于代理指标的模型选择、ILS校准、基准测试执行。下面仅聚焦**模型选择指标**与**ILS校准**这两个带来主要创新且牵涉关键公式的模块。

### 模型选择指标：代理准确率（PA）与代理AUC（PAUC）
传统PU实验往往借用神谕准确率（Oracle Accuracy, OA）选择模型，但OA必须用到未标注数据的真实负标签，这违背了PU问题的根本假设。作者提出两个仅依赖正例与未标注验证数据的指标：

- **代理准确率（Proxy Accuracy, PA）**  
  在OS和TS设置下的计算形式略有差异，统一为仅使用正验证集 $D'_{\mathrm{P}}$ 和未标注验证集 $D'_{\mathrm{U}}$ 的统计量：
  ```math
  \mathrm{PA}(f) =
  \begin{cases}
  \displaystyle \frac{2\pi}{n_{\mathrm{P}}'} \sum_{i=1}^{n_{\mathrm{P}}'} \mathbb{I}\!\left( f(\boldsymbol{x}_i') \geqslant 0 \right)
  + \frac{1}{n_{\mathrm{U}}'} \sum_{i=n_{\mathrm{P}}'+1}^{n_{\mathrm{P}}'+n_{\mathrm{U}}'} \mathbb{I}\!\left( f(\boldsymbol{x}_i') < 0 \right), & \text{TS 设置;} \\[6pt]
  \displaystyle \frac{2\pi}{n_{\mathrm{P}}'} \sum_{i=1}^{n_{\mathrm{P}}'} \mathbb{I}\!\left( f(\boldsymbol{x}_i') \geqslant 0 \right)
  + \frac{1}{n_{\mathrm{P}}'+n_{\mathrm{U}}'} \sum_{i=1}^{n_{\mathrm{P}}'+n_{\mathrm{U}}'} \mathbb{I}\!\left( f(\boldsymbol{x}_i') < 0 \right), & \text{OS 设置.}
  \end{cases}
  ```
  其中 $\pi = p(y=+1)$ 为类别先验，$n_{\mathrm{P}}'$、$n_{\mathrm{U}}'$ 分别为正验证样本数和未标注验证样本数。**Proposition 1** 证明 $\mathbb{E}[\mathrm{PA}(f)] = \mathrm{ACC}(f) + \pi$，因此更高的期望PA严格对应更高的分类准确率。这使得PA可在已知或可估计先验的情况下替代准确率，指导超参数选择。

- **代理AUC（PAUC）**  
  将未标注数据视为"损坏的负例"，直接计算AUC，**无须先验** $\pi$：
  ```math
  \mathrm{PAUC}(f) = \frac{1}{n_{\mathrm{P}}' n_{\mathrm{U}}'} \sum_{i=1}^{n_{\mathrm{P}}'} \sum_{j=n_{\mathrm{P}}'+1}^{n_{\mathrm{P}}'+n_{\mathrm{U}}'}
  \Bigg(
    \mathbb{I}\!\left( f(\boldsymbol{x}_i') > f(\boldsymbol{x}_j') \right)
    + \frac{1}{2} \mathbb{I}\!\left( f(\boldsymbol{x}_i') = f(\boldsymbol{x}_j') \right)
  \Bigg).
  ```
  **Proposition 2** 保证无论OS还是TS设置，期望PAUC更高的分类器其真实AUC也更高。因此PAUC可作为AUC的代理，直接用于模型选择。

- **神谕准确率（OA）**  
  作为对比基准给出，但需要负标签，无法在实际PU学习中计算：
  ```math
  \mathrm{OA}(f) =
  \begin{cases}
  \displaystyle \frac{1}{n_{\mathrm{U}}'} \sum_{i=n_{\mathrm{P}}'+1}^{n_{\mathrm{P}}'+n_{\mathrm{U}}'} \mathbb{I}\!\left( y_i' f(\boldsymbol{x}_i') \geqslant 0 \right), & \text{TS;} \\[6pt]
  \displaystyle \frac{1}{n_{\mathrm{P}}'+n_{\mathrm{U}}'} \sum_{i=1}^{n_{\mathrm{P}}'+n_{\mathrm{U}}'} \mathbb{I}\!\left( y_i' f(\boldsymbol{x}_i') \geqslant 0 \right), & \text{OS.}
  \end{cases}
  ```
  OA在本文中仅作为上界参考，不参与任何实用选择。

### 内部标签偏移（ILS）校准
单样本设置下，未标注训练集 $D_{\mathrm{U}}$ 中混入正例，导致其边际分布与真实总体不一致。直接将为两样本设计的风险估计器（如uPU）套用在OS数据上，会引入系统性偏差。分析表明：
- uPU的无偏风险估计器为
  ```math
  \widehat{R}(f) = \frac{\pi}{n_{\mathrm{P}}} \sum_{i=1}^{n_{\mathrm{P}}} \left[ \ell(f(x_i),+1) - \ell(f(x_i),-1) \right] + \frac{1}{n_{\mathrm{U}}} \sum_{i=n_{\mathrm{P}}+1}^{n_{\mathrm{P}}+n_{\mathrm{U}}} \ell(f(x_i),-1),
  ```
  但在OS设置下，其期望不再等于真实风险，且达到最小值的模型与真实最优模型不一致。

为解决这一问题，作者提出**校准的风险估计器**（Calibrated Risk Estimator）。核心思路是将正例集 $D_{\mathrm{P}}$ 并入未标注损失项的计算，使参与未标注损失的集合成为 $D_{\mathrm{P}} \cup D_{\mathrm{U}}$，从而消除边际偏差。校准后的风险估计为：
```math
\bar{R}(f) = \frac{\pi}{n_{\mathrm{P}}} \sum_{i=1}^{n_{\mathrm{P}}} \Big[ \ell(f(\mathbf{x}_i),+1) + (c-1) \ell(f(\mathbf{x}_i),-1) \Big] + \frac{1 - c\pi}{n_{\mathrm{U}}} \sum_{i=n_{\mathrm{P}}+1}^{n_{\mathrm{P}}+n_{\mathrm{U}}} \ell(f(\mathbf{x}_i),-1),
```
其中 $c$ 为正例的观察概率估计：$c = \frac{n_{\mathrm{P}}}{\pi (n_{\mathrm{P}} + n_{\mathrm{U}})}$。该估计器在OS设置下恢复了无偏性，**Theorem 2** 给出了泛化界，表明当 $n_{\mathrm{P}}, n_{\mathrm{U}}$ 足够大时 $\bar{R}(f)$ 的极小值点收敛到最优分类器（对参数范数有界的深度网络成立）。实际实现时，只需按 **Algorithm 1** 的做法——在损失函数中将未标注部分的输入从 $D_{\mathrm{U}}$ 替换为 $D_{\mathrm{P}} \cup D_{\mathrm{U}}$——即可透明地完成校准，无需改动原学习算法主体。

> **证据强度说明**：以上公式均直接来自论文 Definition 1–3、Equation 8 和 Algorithm 1，并在附录中提供了严格证明（Propositions 1–2、Theorem 2）。校准效果的实证支持在所有基准表中均有体现（例如 Table 1 中 uPU-c 相较 uPU 的准确率提升 +4.44%，以及多组表格中校准版本的一致性领先），证据可靠。

## 实验与分析

本基准通过**仅使用PU验证数据（无负样本）进行模型选择**与**校正单样本（OS）设置下两样本（TS）算法的内部标签偏移（ILS）**，首次为PU学习提供了现实且公平的比较框架。所有方法统一使用ResNet‑34（图像）或MLP‑500（表格），在相同超参数搜索协议下运行，避免实现偏差。下面从ILS校正效果、代理验证指标的表现、整体算法排名及关键失败模式四个维度展开。

**1. 校准消除内部标签偏移，挽回两样本算法的性能损失**

在OS设置下，未标注训练数据中正例比例偏离整体分布（ILS），直接运行TS类成本敏感或样本选择算法会导致风险估计有偏，性能显著退化。Figure 2和Figure 3分别在CIFAR‑10和ImageNette上证实：未经校准的TS算法在OS下的准确率大幅低于其TS设置下的表现，且正样本量越少退化越大。引入Algorithm 1的校准（将正例集 $D_P$ 同时纳入未标注损失项，使未标注数据边际分布无偏）后，带后缀"‑c"的算法在几乎所有实验配置中均取得一致提升。典型例子：CIFAR‑10 Case 1上，uPU‑c的测试准确率从82.04±0.49（uPU）升至86.48±0.21（Table 1）；AUC、F1等指标同样获得显著增益。这证明**校准是跨家族（TS vs. OS）公平比较的必要环节**，否则两样本方法将被系统性低估。

![[assets/figures/papers/iclr26_0005_5R11h5o44C_Accessible_Realistic_and_Fair_Evaluation_of_Posi/figures/014_Figure_2.jpg]]
*Figure 2: Classification accuracies of TS PU learning algorithms in OS and TS settings of a PU version of CIFAR-10 with varying amounts of positive data. Figures (a) to (f) are for Case 1, and Figures (g) to (l) are for Case 2*

![[assets/figures/papers/iclr26_0005_5R11h5o44C_Accessible_Realistic_and_Fair_Evaluation_of_Posi/figures/024_Figure_3.jpg]]
*Figure 3: Classification accuracies of TS PU learning algorithms in OS and TS settings of a PU version of ImageNette with varying amounts of positive data. Figures (a) to (e) are for Case 1, and Figures (f) to (j) are for Case 2*

![[assets/figures/papers/iclr26_0005_5R11h5o44C_Accessible_Realistic_and_Fair_Evaluation_of_Posi/figures/025_Table_1.jpg]]

**2. 代理验证指标PA/PAUC有效驱动模型选择，但效果依赖于测试指标**

传统Oracle Accuracy (OA) 需要未标注数据的真实标签，违反PU假设。本文仅将其作为对照。**无偏替代指标**：

- **PA（代理准确率）** 需要类别先验 $\pi$，其期望与真实准确率单调相关（Proposition 1），可仅凭正例和未标注验证数据计算。
- **PAUC（代理AUC）** **不需要** $\pi$，且期望与真实AUC单调相关（Proposition 2），更具普适性。

实验表明：使用PA或PAUC进行超参数选择，所获模型的测试性能与采用"作弊"的OA接近，证明二者在实际PU场景下是可靠的。然而，**测试指标和验证指标之间存在不匹配风险**——若最终关注AUC，用PAUC调参通常优于用PA（例如Table 1）。这提示使用者应根据下游需求选择验证指标，而非依赖单一准则。

**3. 整体排名：无单一算法全面胜出，场景依赖性明显**

Figure 4及Appendix中的F1、AUC、Precision、Recall汇总图显示：在不同数据集、正例配置和验证指标下，算法排名剧烈变化。以OA验证为例的安全环境（即已知真实标签的oracle比较）中，CVIR、Dist‑PU‑c、uPU‑c等成本敏感家系表现强劲；而在PA/PAUC等PU友好验证下，样本选择方法（如P3MIX）与对抗方法（如PAN）在特定场景凸显优势。**没有普适的最优算法**。表格中的典型数据点：

![[assets/figures/papers/iclr26_0005_5R11h5o44C_Accessible_Realistic_and_Fair_Evaluation_of_Posi/figures/034_Figure_4.jpg]]
*Figure 4: Overall performance w.r.t. accuracy and the F1 score across all datasets. Hyperparameters were tuned using PA, PAUC and OA, respectively; bar colors indicate means*

- CIFAR‑10 Case 1：OA验证下Dist‑PU‑c准确率88.47±0.25最高（Table 1）；PAUC验证下GLWS的AUC达88.08±0.43显著领先（Table 2）。
- ImageNette Case 1：样本选择家族P3MIX‑E在多种指标下均排名靠前（Table 3, 9）。
- 更小的USPS与Letter数据集（Tables 16–18等）呈现类似趋势，进一步强化"方法选择需视任务而定"的结论。

![[assets/figures/papers/iclr26_0005_5R11h5o44C_Accessible_Realistic_and_Fair_Evaluation_of_Posi/figures/027_Table_3.jpg]]
*Table 3: Test results (mean˘std) of accuracy, AUC, and F1 score for each algorithm on ImageNette (Case 1) under different model selection criteria. The best performance w.r.t. each validation metric is shown in bold*

**4. 消融实验：校准技术的普适性**

后缀"‑c"的校准不仅适用于uPU、nnPU、VPU等风险最小化方法，也可移植到部分样本选择算法（如PUbN）。Appendix中的附加表（Table 7–18）一致表明，**在所有数据集、所有评估指标（准确率、AUC、F1、精确率、召回率）上，校准版本均优于或至少持平无校准版本**，证实校准的通用性，并构成基准的重要组成部分。

**5. 失败模式与局限性**

尽管基准解决了模型选择和ILS偏差两大核心问题，仍存在以下限制：

- **先验依赖性**：PA的计算需要准确已知或估计类别先验 $\pi$，而$\pi$的估计本身是PU学习的难点；PAUC虽无需$\pi$，但其作为AUC代理受正未标注排位影响，对分类阈值不敏感。
- **校准参数假设**：校准需正例观察概率 $c = n_P / [\pi (n_P + n_U)]$，实验中假设$c$已知。实际场景中$c$的估计误差会传导至校准效果，需进一步研究鲁棒性。
- **优化目标单一**：PA和PAUC均针对准确率/AUC，对F1、精确率、召回率等非对称指标无直接优化准则。Tables 7–10反映出在某些组合下，高AUC模型未必给出最优F1，说明缺少PU原生的指标专用选择器。
- **规模限制**：实验数据集最大2万样本，校准方法在大规模真实PU数据上的扩展性尚未验证。

综上，本基准通过校准技术与PU友好的验证指标构建了一个公平且可复现的评估范式，揭示了现有文献中的评估陷阱，同时指明未来方向——包括设计针对F1等任务的PU模型选择准则、将先验估计与校准集成到端到端流程，以及在大规模真实PU场景中进行验证。

## 方法谱系与知识库定位

### 与已有方法的区别与贡献

本文工作围绕"**可访问、现实且公平的PU学习算法比较**"这一核心目标，对现有PU方法的评估范式进行了关键性修正，并非提出全新的学习器，而是构建统一的基准测试平台。在此平台上，比较的基线方法涵盖成本敏感类（uPU, nnPU, CVIR）、变分类（VPU）、样本选择类（PUbN）和生成对抗类（PAN）等主流家族（见`baseline_methods`列表）。相较于先前零散且依赖于负例验证的个别实验，本文做出了以下两个根本性的 **"插槽替换"**。

**第一，模型选择指标与验证集组成的切换。**  
以往工作普遍采用 Oracle Accuracy (OA)，即根据真实负标签计算验证准确率来选择超参数，这等同于暗中假设负例可获取，违背PU假设。本文改用仅由正例与未标记数据构成的代理准确率（PA）与代理AUC（PAUC）。这两个指标被证明具有无偏保障：在两类设置下，更高的期望PA保证更高的期望准确率，更高的期望PAUC保证更高的期望AUC（见`Proposition 1`与`Proposition 2`）。由此，模型选择不再需要负例，使评估贴近真实PU应用场景。

**第二，单样本（OS）设置下对两样本（TS）算法的适配。**  
大量TS方法（如uPU、nnPU等）常被直接用于OS设置而未经校准，导致其性能被系统性低估。本文识别出"未标注数据的内部标签偏移（ILS）"是导致这一陷阱的因果机制（Fig. 1），并提出纠偏方案：将正例集$D_{\mathrm{P}}$注入未标注损失项，使得增补后的未标注数据边际无偏，适配TS风险估计器（Algorithm 1）。该校准技术（带"-c"后缀）在所有数据集、所有TS算法、多种指标（准确率、AUC、F1、精确率、召回率）上均带来一致的性能提升（如CIFAR‑10 Case 1中uPU准确率从82.04%升至86.48%），清晰证明了消除ILS偏差的必要性。

上述两项改变使得跨家族比较从"依赖负例的不公平赛道"转变为"仅利用PU数据的统一赛道"，从而建立了一个**结构化公平的PU基准**。

### 适用边界与前提假设

本基准测试与校正方法适用于以下场合，但其有效性严格受若干条件约束。

- **PU设置假设**：评测在严格的正例‑未标记数据框架下进行，可处理OS和TS两种设置。若实际数据来自于有标注负例的场景，则传统监督学习的验证指标可能更为直接。
- **类别先验$\pi$必须已知或可准确估计**：PA的计算显式依赖$\pi$（见Definition 1）。当$\pi$未知且估计不准时，PA作为模型选择指标的可靠性下降，需要谨慎。
- **正例观察概率$c$需已知**：校准方法要求掌握OS设置下正例在未标注集中的观察概率$c$。真实应用中$c$的估计误差会传播至校准后的风险估计器，进而影响模型优化效果（尽管Theorem 2给出了理论收敛保证）。
- **数据集规模**：实验仅在小型至中型数据集（如CIFAR‑10、ImageNette、USPS、Letter，样本量≤20K）上进行。在大规模PU基准或高维复杂数据下的扩展性与对外部模型的迁移性尚未经过验证。
- **模型选择指标与最终测试指标的匹配**：PA/PAUC在超参数选择中有效，但其效力与目标测试指标类型有关。例如，当测试指标为AUC时，使用PAUC优选出的模型可能优于OA优选出的模型；但当最终评价指标为F1或精确率时，PA/PAUC仅能提供间接选择，并不保证最优。

### 理论与实证上的局限

尽管基准与校正策略展现出坚实效果，但分析仍揭示出若干值得明确指出的**失效边界**。

1. **对先验$\pi$的依赖性**：PA存在理论无偏性（Proposition 1）的前提是$\pi$被精确给定；若$\pi$有误，PA的单调性保障可能不再成立，导致模型选择方向偏离目标。  
2. **校准未覆盖全部方法族**：校准技术专门针对成本敏感类（uPU、nnPU等）等依赖风险估计器的TS方法设计，对于样本选择类或生成对抗类PU算法，直接应用Algorithm 1的有效性尚未得到验证。  
3. **无专用非对称指标验证准则**：基准仅提供了PA/PAUC用于模型选择，没有设计PU友好的、直接优化F1、精确率或召回率的验证度量。这意味着在非均衡代价需求下，超参数选择可能无法精准贴合业务目标。  
4. **有限的规模与域多样性**：实验所有数据均为人工划分的PU版本，且缺乏真实PU场景（如异常检测、生物信息学等）中带有噪声与领域偏移的测试。

### 开放问题

基于当前的发现与限制，本工作自然引出一系列待解决的关键问题：

- **大规模真实PU基准的构建与泛化性验证**：将现有算法及校准技术部署到真实世界的大规模PU数据集上，检验其性能排序是否保持，并探查在小样本下有效的结论是否可迁移。
- **为F1、精确率、召回率设计直接优化且仅依赖PU数据的验证指标**：需从理论上建立这些非对称度量的偏分布估计方法，避免通过PA/PAUC间接推断可能造成的匹配偏差。
- **类别先验$\pi$的全自动集成**：将$\pi$的在线估计器（如利用PU数据性质的估计算法）与模型选择指标打通，构建从数据到分类器的完全无监督PU学习流水线，减少外部先验假设。
- **校准技术的无缝融合**：探索如何将ILS校准思想融入样本选择、对抗生成等其他PU范式，并验证其与mixup等数据增强或正则化手段的协同作用，以增强未来方法的通用性与稳健性。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/Accessible_Realistic_and_Fair_Evaluation_of_Positive_Unlabeled_Learning_Algorithms.pdf

![[paperPDFs/ICLR_2026/Accessible_Realistic_and_Fair_Evaluation_of_Positive_Unlabeled_Learning_Algorithms.pdf]]
