---
title: "An Information-Theoretic Parameter-Free Bayesian Framework for Probing Labeled Dependency Trees from Attention Score"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/An_Information_Theoretic_Parameter_Free_Bayesian_Framework_for_Probing_Labeled_Dependency_Trees_from_Attention_Score.pdf
openreview_forum_id: q7raIuTQDK
aliases:
- IITPFBP
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/probabilistic_methods
core_operator: "通过精确估计注意力分数与依存标签之间的混合分布并计算二元互信息（MI），能够量化每个注意力头对特定依存关系的贡献，从而无需训练即可有效筛选句法头并为树重建提供信息量。"
primary_logic: "利用核密度估计（KDE）对连续注意力向量建模，通过贝叶斯定理推导后验概率，并设计基于对数意见池化和独立投票概率空间的解码算法，在无外部参数的情况下重建完整带标签的依存树。该方法巧妙地避开了高维KDE的维度灾难，同时提供了透明、可解释的头重要性度量。"
claims:
- "IPBP+MI_pos 在 open_llama_7b 上取得了最优的 LAS (34.8) 和 UAS (49.9)，显著优于现有无监督基线（如表2所示）。"
- "在内部评估中，IPBP 的头选择方法与其它方法的一致性最高（平均 Spearman-R 0.398），证明了其头重要性排序的可靠性。"
- "消融实验证实了对数池化优于算术平均（UAS 49.9 vs 36.2），并且标准带宽设置提供了（局部）最优结果。"
- "UD 2.9 English (open_llama_7b) 上 UAS = 49.9 (IPBP+MI_pos)"
---

# An Information-Theoretic Parameter-Free Bayesian Framework for Probing Labeled Dependency Trees from Attention Score

> [!tip] 核心洞察
> 利用核密度估计（KDE）对连续注意力向量建模，通过贝叶斯定理推导后验概率，并设计基于对数意见池化和独立投票概率空间的解码算法，在无外部参数的情况下重建完整带标签的依存树。该方法巧妙地避开了高维KDE的维度灾难，同时提供了透明、可解释的头重要性度量。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于信息论的无参数贝叶斯框架：从注意力分数中探测带标签依存句法树 |
| 英文题名 | An Information-Theoretic Parameter-Free Bayesian Framework for Probing Labeled Dependency Trees from Attention Score |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=q7raIuTQDK); [GitHub](https://github.com/ChristLBUPT/IPBP) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/probabilistic_methods |
| Method | IPBP (Information-theoretic Parameter-free Bayesian Probing) |
| Dataset | UD 2.9 English (open_llama_7b), Head-Selection Intrinsic Evaluation (Spearman-R) |

> [!tip] 效果简介
> - UD 2.9 English (open_llama_7b) 上，UAS 为 49.9 (IPBP+MI_pos)，对比 49.1 (IPBP base)，变化 +0.8。
> - UD 2.9 English (open_llama_7b) 上，LAS 为 34.8 (IPBP+MI_pos)，对比 30.6 (IPBP base)，变化 +4.2。
> - Head-Selection Intrinsic Evaluation (Spearman-R) 上，Average Spearman-R 为 0.398 (IPBP)，对比 other methods (e.g., Probeless, IoU, etc.) lower consistency，变化 IPBP highest。

## 概述

现有从大语言模型注意力分数中探测句法结构的方法面临两个核心瓶颈：其一，监督探针方法引入额外可训练网络，使得探针本身可能学会任务，而非从模型中提取句法——这实际上是用“不可解释性来解释可解释性”；其二，直接信任原始注意力分数的方法忽略了注意力头并非专用于句法，需要对注意力头进行筛选和变换。本文提出 **IPBP**（Information-theoretic Parameter-free Bayesian Probing），一个基于信息论的无参数贝叶斯探测框架，其核心思路是通过精确估计注意力分数与依存标签之间的混合分布并计算二元互信息（MI），量化每个注意力头对特定依存关系的贡献，从而无需训练即可有效筛选句法头并为树重建提供信息量。

IPBP 的方法设计围绕三个关键创新展开：首先，利用核密度估计（KDE）对连续注意力向量建模，通过贝叶斯定理推导后验概率，巧妙避开了高维 KDE 的维度灾难；其次，设计基于对数意见池化和独立投票概率空间的解码算法，在无外部参数的情况下重建完整带标签的依存树；最后，以归一化互信息作为自适应头选择阈值，提供了透明、可解释的头重要性度量。

在 UD 2.9 English 数据集上对 open_llama_7b 的评估中，IPBP+MI_pos 取得了无监督设置下的最优结果，LAS 达到 34.8，UAS 达到 49.9，显著优于现有无监督基线。内在评估进一步表明，IPBP 的头选择方法与其他方法的一致性最高（平均 Spearman-R 为 0.398），验证了其头重要性排序的可靠性。消融实验证实了对数池化优于算术平均（UAS 49.9 vs 36.2），且标准带宽设置提供了局部最优结果。此外，针对特定专家头的消融实验表明，移除 top-5 高 MI 头会导致模型在预测需要相应句法信息的下一个 token 时 logits 下降，证明所识别的头确实编码了句法相关信息。

在方法谱系中，IPBP 定位于无参数句法探测方法，区别于有监督探针（如 **ElasticNet**，Dalvi et al., 2019；**V-Information**，Xu et al., 2020）和无参数相关性分数（如 **Probeless**，Antverg & Belinkov, 2022；**IoU**，Mu & Andreas, 2020）。其核心贡献在于将头重要性度量从多种启发式相关性分数替换为归一化二元互信息，将树重建概率源从原始注意力分数替换为 MI 加权的贝叶斯后验概率，并将依存弧概率空间从单一弧存在扩展为面向所有标签的独立投票联合概率空间。

## 背景与动机

### 句法探针面临的信任危机

大型语言模型（LLM）的内部表征是否编码了句法结构，是神经语言处理领域的核心问题之一。探针（probe）方法作为回答该问题的主要工具，近年来却陷入了“用不可解释性来解释”的困境。现有句法探测方法存在两个相互关联的瓶颈：

**瓶颈一：监督探针的“自我学习”陷阱。** 主流的探针方法通过在模型表征上训练一个附加的分类网络来预测句法标签。然而，这一范式存在根本性的逻辑缺陷——探针本身可能学会了从表征中提取句法信息，也可能仅仅依靠自身的归纳偏置完成了任务。换言之，我们无法区分模型是否真正编码了句法知识，还是探针在“替模型完成任务”。这一问题在**线性前馈族方法**（如 ElasticNet, Dalvi et al., 2019）和**V-信息方法**（Xu et al., 2020）中尤为突出，因为它们引入了可训练参数，混淆了“模型能力”与“探针能力”的边界。

**瓶颈二：对原始注意力分数的盲目信任。** 另一类方法试图绕过探针训练，直接利用 Transformer 的注意力分数作为句法结构的指示器。然而，注意力分数并非专为句法解析而设计——一个注意力头可能同时编码语义、位置、共指等多种信息。简单地假设“注意力分数即句法概率”忽略了注意力头的功能多样性，导致从噪声中提取的信号信噪比极低。

### 无参数方法的局限与缺口

为规避监督探针的参数风险，研究者提出了若干无参数相关性分数，如 **Probeless**（Antverg & Belinkov, 2022）基于均值激活差异，以及 **IoU**（Mu & Andreas, 2020）基于 Jaccard 相似度。这些方法虽然避免了额外训练，但其统计量过于粗糙——仅依赖一阶矩或简单的集合重叠，无法捕捉注意力分数分布与依存标签之间复杂的非线性关联。同时，它们缺乏对注意力头进行有效筛选和变换的机制，导致下游树重建质量远逊于监督方法。

### 核心动机：走向严格的无参数贝叶斯推理

本文的动机源于一个根本追问：**能否在不引入任何可训练参数的前提下，以数学上严格的方式从注意力分数中提取完整的带标签依存句法树？**

这要求同时解决两个子问题：
1. **量化与筛选**：精确度量每个注意力头对每种依存关系的贡献，从而识别出真正编码句法信息的“专家头”；
2. **推理与重建**：基于筛选后的注意力证据，通过严格的概率推理重建完整的依存树，而非依赖启发式规则。

论文提出的 IPBP（Information-theoretic Parameter-free Bayesian Probing）框架正是对这一动机的系统性回应。其核心洞察在于：利用核密度估计（KDE）对连续注意力向量建模，通过贝叶斯定理推导后验概率，并设计基于对数意见池化和独立投票概率空间的解码算法，在无外部参数的情况下重建完整带标签的依存树。该方法巧妙地避开了高维 KDE 的维度灾难，同时提供了透明、可解释的头重要性度量。

## 核心创新

IPBP 的核心创新在于将句法探测从“训练一个探针”范式彻底转向“无参数信息估计”范式，通过三个相互耦合的 **changed slots** 解决了现有方法的两个根本瓶颈。

### 瓶颈一：监督探针的“不可解释性”陷阱

现有监督探针（如 **Linear Feedforward Family**，Dalvi et al., 2019）引入额外可训练网络 $W_\theta$，这带来了一个根本性问题：探针本身可能学会了从表示中提取句法，而非模型表示本身编码了句法。换言之，用可学习的参数去“解释”模型，本身就需要被解释。

IPBP 的应对策略是 **完全无参数化**：
- **头重要性度量**：从“训练线性权重”或“计算 V-信息差”（Xu et al., 2020）转变为直接估计注意力分数 $A_{b,h}$ 与依存标签 $L$ 之间的**归一化二元互信息** $\mathrm{MI}_{\mathrm{binary}}(l;A_{b,h}) / \hat{H}(\mathbf{1}_l(L))$。该度量具有明确的信息论意义——它量化了每个注意力头对特定依存关系 $l$ 所贡献的专属信息量，无需任何可学习参数。
- **树重建概率源**：从“将原始注意力分数直接视为弧概率”转变为基于贝叶斯定理推导的**后验概率** $\hat{f}(L=l|A_{b,h})$，并通过 MI 加权的对数意见池化（几何平均）融合多头信息。这一过程完全由概率论驱动，杜绝了探针自我学习的可能。

### 瓶颈二：原始注意力分数的“信噪混淆”

直接信任原始注意力分数忽略了两个事实：1）注意力头并非专用于句法，大量头编码的是语义或位置信息；2）不同头对不同依存关系的贡献差异巨大。IPBP 通过精确的分布估计和自适应筛选解决了这一问题。

**核心因果机制**：利用核密度估计（KDE）对连续注意力向量建模，估计条件密度 $f(A|L)$ 和联合密度 $f(l,a)$，进而通过积分计算二元互信息：

$$\mathrm{MI}_{\mathrm{binary}}(l;A_{b,h}) = \int f(l,a) \log \frac{f(l,a)}{P(l)f(a)} \mathrm{d}a + \int f(\neg l,a) \log \frac{f(\neg l,a)}{P(\neg l)f(a)} \mathrm{d}a$$

这一公式的巧妙之处在于：它将每个头对依存关系 $l$ 的贡献与对所有其他关系的贡献进行了**显式对比**，从而天然具备筛选“专家头”的能力。归一化后的 MI 值落入 $[0,1]$ 区间，可作为自适应阈值，为每个依存标签动态选择高相关头集合 $\mathcal{H}_l$。

### 瓶颈三：概率空间的语义空洞

传统方法仅在“弧存在与否”的单一概率空间中操作，忽略了依存标签的语义信息。IPBP 设计了**面向所有标签的独立投票联合概率空间**：

$$P(x_i, x_j; l) = \mathbf{GP}_{\mathcal{H}_l}(x_i, x_j; l) \times \prod_{l' \in \mathcal{L} \cup \{\phi\} - \{l\}} \left\{1 - \mathbf{GP}_{\mathcal{H}_{l'}}(x_i, x_j; l)\right\}$$

该公式假设各依存标签独立投票：一个弧被赋予标签 $l$ 的概率，等于该标签对应的几何平均后验 $\mathbf{GP}_{\mathcal{H}_l}$ 乘以所有其他标签“不投票”的概率。这一设计构成了一个有效的概率空间，使得 Eisner 解码算法能够直接重建**带标签的完整依存树**，而非仅预测无标签弧。

### 维度灾难的优雅规避

直接对高维注意力向量进行 KDE 会遭遇维度灾难。IPBP 的核心洞察在于：利用混合-联合分布和贝叶斯定理，将估计目标从高维联合密度 $f(A_{b,h}|L)$ 降维为一维条件密度估计（每个头的注意力分数是标量），将所需估计次数降至最低（仅 1 次）。这一技巧使得方法在计算上可行，同时保持了数学严谨性。

### 消融证据支撑

消融实验证实了上述创新设计的有效性：
- **对数池化 vs 算术平均**：对数池化（即 MI 加权的几何平均）使 UAS 从 36.2 提升至 49.9（Table 9），验证了指数加权融合的必要性。
- **Positive MI vs Binary MI**：仅关注正类标签的 $\mathrm{MI}_{\mathrm{pos}}$ 将 LAS 从 30.6 提升至 34.8（Table 2），表明过滤长尾噪声标签能显著改善标签预测。
- **专家头消融**：移除 top-5 高 MI 头后，模型在预测需要相应句法信息的下一个 token 时 logits 显著下降（Table 4），直接证明了所识别头确实编码了句法相关信息。

## 整体框架

IPBP 将句法探测拆解为两个串行子任务：**互信息估计**与**依存树重建**。整个流水线无需训练任何外部网络，仅依赖 Transformer 模型在标注语料上产生的注意力分数与依存标签，通过信息论与贝叶斯推理完成从原始注意力到完整带标签依存树的端到端映射。

### 输入

- 目标 Transformer 模型（本文验证范围限于解码器架构 LLM，如 open_llama_7b、Meta-Llama-3-8B、vicuna-7b、Mistral-7B）
- 带依存标注的语料（来自 UD 2.9 的 English/French/Spanish 分片）
- 模型对该语料逐 token 产生的所有层、所有头的注意力矩阵

### 核心流水线（五模块串联）

**模块 1：注意力分数收集与分组**  
对每个注意力头 $(b,h)$，按依存标签 $l \in \mathcal{L} \cup \{\phi\}$ 将所有 token 对之间的注意力分数归入集合 $\mathcal{A}_{b,h;l}$。$\phi$ 表示“无依存关系”类别，用于构建完整的概率空间。

**模块 2：核密度估计 (KDE)**  
对每个 $\mathcal{A}_{b,h;l}$，使用高斯核与经验带宽 $B$ 估计条件密度 $\hat{f}(A_{b,h} \mid L=l)$，同时估计边缘密度 $\hat{f}(A_{b,h})$ 与先验 $\hat{P}(L=l)$。通过贝叶斯定理直接导出后验 $\hat{f}(L=l \mid A_{b,h}=a)$，无需额外参数化。KDE 在 GPU 上批量执行以控制计算开销。

**模块 3：二元互信息估计**  
为量化每个头对特定依存标签的专属信息量，计算二元互信息 $\mathrm{MI}_{\mathrm{binary}}(l; A_{b,h})$——将依存空间二分为“标签 $l$”与“非 $l$”，分别积分联合分布与边缘分布的对数比。该指标是后续头选择与后验加权的唯一信息源。

**模块 4：自适应头选择**  
对每个标签 $l$，将 $\mathrm{MI}_{\mathrm{binary}}$ 用二元指示变量的熵 $\hat{H}(\mathbf{1}_l(L))$ 归一化至 $[0,1]$，据此自适应筛选高相关头集合 $\mathcal{H}_l$。该归一化使不同标签间的阈值具有可比性，避免了固定头数或固定阈值的经验偏差。

**模块 5：后验池化与树解码**  
对每个候选弧 $(x_i, x_j)$ 与标签 $l$，以 $\mathrm{MI}_{\mathrm{binary}}$ 为权重，对 $\mathcal{H}_l$ 内所有头的后验概率进行对数意见池化（几何平均），得到 $\mathrm{GP}_{\mathcal{H}_l}(x_i, x_j; l)$。在此基础上，假设各标签独立投票，计算弧的整体概率：

$$P(x_i, x_j; l) = \mathrm{GP}_{\mathcal{H}_l}(x_i, x_j; l) \times \prod_{l' \in \mathcal{L} \cup \{\phi\} - \{l\}} \bigl(1 - \mathrm{GP}_{\mathcal{H}_{l'}}(x_i, x_j; l)\bigr)$$

最终以 $\max_l P(x_i, x_j; l)$ 作为弧权重，通过 Eisner 动态规划算法解码出完整依存树。

### 关键设计决策

- **维度灾难规避**：不对高维联合注意力向量直接做 KDE，而是利用混合联合分布与贝叶斯定理，将估计限制在一维条件密度上，使非参数估计在计算上可行。
- **概率空间完备性**：独立投票模型保证了 $\sum_{l \in \mathcal{L} \cup \{\phi\}} P(x_i, x_j; l) = 1$，使解码算法拥有合法的概率输入。
- **无训练、无超参**：整个流水线不引入可学习参数；带宽使用标准经验公式，头选择阈值由归一化 MI 自适应确定，唯二的经验性设置是头总数上限（2000）与每标签 top-k（8），且均通过消融或公平性约束加以控制。

### 输出

- 每个标签 $l$ 对应的专家头集合 $\mathcal{H}_l$ 及其 $\mathrm{MI}_{\mathrm{binary}}$ 权重
- 每句的完整带标签依存树（弧方向 + 依存关系类型）
- 可解释的中间产物：后验密度函数、MI 堆叠图、层-深度相关性等分析工具

## 核心模块与公式推导

IPBP 将句法探测分解为两个可分离的子任务：互信息估计与树重建。前者量化每个注意力头对特定依存关系的专属信息量，后者以贝叶斯推断的方式将筛选后的注意力分数转化为完整依存树。

### 注意力分数收集与分组

方法的第一步是按依存标签将注意力分数划分到不同的集合中。对于每个注意力头 $(b,h)$，定义集合 $\mathcal{A}_{b,h;l}$，其中 $l \in \mathcal{L} \cup \{\phi\}$，$\mathcal{L}$ 为所有依存标签的集合，$\phi$ 表示“无依存关系”标签。$\mathcal{A}_{b,h;l}$ 收集训练集中所有具有依存关系 $l$ 的词对在该注意力头上的注意力分数。这一分组操作为后续的条件密度估计提供了数据基础。

### 核密度估计与后验推导

为计算互信息，需要估计连续注意力变量 $A_{b,h}$ 在给定离散依存标签 $L$ 下的条件密度。IPBP 采用高斯核密度估计（KDE）：

$$\frac{1}{|\mathcal{A}_{b,h;l}| \cdot B} \sum_{i=1}^{|\mathcal{A}_{b,h;l}|} \frac{1}{\sqrt{2\pi \cdot \sigma_{\mathcal{A}_{b,h;l}}}} \exp{\left(-\frac{x_0 - \mathcal{A}_{b,h;l}^{(i)}}{B}\right)^2}$$

其中 $B$ 为带宽，$\sigma_{\mathcal{A}_{b,h;l}}$ 为集合 $\mathcal{A}_{b,h;l}$ 的标准差。先验概率 $P(L=l)$ 由样本比例经验估计。通过贝叶斯定理，后验概率可直接从联合密度与边缘密度导出：

$$f(L|A_{b,h}) = \frac{f(A_{b,h}|L)P(L)}{f(A_{b,h})} = \frac{f(A_{b,h},L)}{f(A_{b,h})}$$

该后验概率是后续树重建的核心输入。

### 二元互信息与头选择

为识别对特定依存关系具有专属信息量的“专家头”，IPBP 引入二元互信息 $\mathrm{MI}_{\mathrm{binary}}(l;A_{b,h})$。其核心思想是将依存标签空间二值化：将标签 $l$ 视为正类，其余所有标签（包括 $\phi$）归为负类 $\neg l$，然后计算注意力头与这一二值变量之间的互信息：

$$\mathrm{MI}_{\mathrm{binary}}(l;A_{b,h}) = \int f(l,a) \log \frac{f(l,a)}{P(l)f(a)} \mathrm{d}a + \int f(\neg l,a) \log \frac{f(\neg l,a)}{P(\neg l)f(a)} \mathrm{d}a$$

该度量直接量化了注意力头对区分“是否为依存关系 $l$”的贡献。为便于跨标签比较，IPBP 用二元熵进行归一化：

$$\frac{\mathrm{MI}_{\mathrm{binary}}(l;A_{b,h})}{\hat{H}(\mathbf{1}_l(L))}$$

其中 $\hat{H}(\mathbf{1}_l(L))$ 为二值指示变量的经验熵。归一化后的值落入 $[0,1]$ 区间，作为自适应阈值筛选每个标签的高相关头集 $\mathcal{H}_l$。

### 后验池化与弧概率

树重建阶段需要融合多个专家头的后验信息。IPBP 采用对数意见池化（Logarithmic Opinion Pooling），以 $\mathrm{MI}_{\mathrm{binary}}$ 为权重对后验概率进行几何平均：

$$\log \mathrm{GP}_{\mathcal{H}_l}(x_i, x_j; l) = \frac{\sum_{b_k, h_k} \mathrm{MI}_{\mathrm{binary}}(l;A_{b_k, h_k}) \cdot \log \hat{f}(L=l|A_{b_k, h_k})}{\sum_{b_m, h_m} \mathrm{MI}_{\mathrm{binary}}(l;A_{b_m, h_m})}$$

这一设计的直觉是：信息量越大的头，其意见在池化中权重越大。消融实验证实，对数池化显著优于简单算术平均（UAS 49.9 vs 36.2），验证了指数加权机制的有效性。

为构建有效的概率空间，IPBP 假设各标签独立投票，定义词对 $(x_i, x_j)$ 之间依存弧标签为 $l$ 的整体概率：

$$P(x_i, x_j; l) = \mathbf{GP}_{\mathcal{H}_l}(x_i, x_j; l) \times \prod_{l' \in \mathcal{L} \cup \{\phi\} - \{l\}} \left\{1 - \mathbf{GP}_{\mathcal{H}_{l'}}(x_i, x_j; l)\right\}$$

该公式确保 $\sum_{l} P(x_i, x_j; l) = 1$，构成合法的概率分布。最终，通过 Eisner 动态规划算法和 $\max_l P(x_i, x_j; l)$ 解码出完整依存树。

### 维度灾难的规避

IPBP 的一个关键设计在于规避了高维 KDE 的维度灾难。传统方法若直接对多变量联合分布建模，所需样本量随维度指数增长。IPBP 利用混合联合分布与贝叶斯定理，将估计限制在一维条件密度 $f(A_{b,h}|L=l)$ 上，使 KDE 在有限样本下仍保持可靠。

## 实验与分析

### 4.1 实验设置概述

IPBP 的实验评估围绕两个核心子任务展开：**互信息估计（MI Estimation）** 与**依存树重建（Tree Reconstruction）**。前者衡量各注意力头对特定依存关系的信息编码能力，后者则直接检验从注意力分数中恢复完整带标签依存树的质量。

实验在以下模型上开展：`open_llama_7b`、`Meta-Llama-3-8B`、`vicuna-7b` 和 `Mistral-7B`，数据集采用 UD 2.9 的英语、法语和西班牙语分区（数据划分统计见 Table 7）。所有基线方法在公平条件下比较：头选择的总句法头数量统一限制为 2000 个，树重建基线同样使用 MI 进行头选择（top-8），仅概率来源不同，从而隔离后验估计的影响。密度估计和推断均在 RTX 4090 GPU 上完成，保证了计算效率对比的公平性。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_q7raIuTQDK/figures/009_Table_7.jpg]]
*Table 7: Number of train/dev samples of different language partitions of our dataset*

### 4.2 主结果：树重建性能

Table 2 展示了在 `open_llama_7b` 上 IPBP 与各类基线的树重建结果。IPBP 基础版本（使用二元互信息 MI_binary）取得 UAS 49.1、LAS 30.6，已显著优于所有无监督基线。进一步引入正类互信息（MI_pos）后，**IPBP+MI_pos 达到 UAS 49.9、LAS 34.8**，LAS 提升 4.2 点，成为当前最优的无监督探测方法。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_q7raIuTQDK/figures/001_Table_2.jpg]]
*Table 2: Tree reconstruction results of our IPBP and different baselines. For undirected settings, results∗ are UUAS and ULAS instead*

**关键对比**：原始注意力分数基线（Raw Attention Score）仅取得 UAS 32.2、LAS 17.9，表明直接信任原始注意力远不如经过 MI 筛选和贝叶斯后验变换后的结果。无参数基线 Probeless 和 IoU 的表现更弱，而监督方法（如 ElasticNet、V-Information）虽在头重要性排序上可用，但无法直接生成依存树。

Table 1 进一步展示了跨模型和跨语言的结果概览，验证了 IPBP 在不同 LLM 架构和语言上的泛化能力。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_q7raIuTQDK/figures/002_Table_1.jpg]]
*Table 1: Results across models and languages*

### 4.3 头选择的内在评估

头重要性排序的可靠性通过内在评估（Table 3）进行检验。该评估计算各方法两两之间的 label-averaged Spearman-R 一致性。**IPBP 的平均 Spearman-R 达到 0.398，在所有方法中最高**，表明其头重要性排序与其他方法的一致性最强。相比之下，Probeless 和 IoU 等无参数方法的平均一致性较低，而监督方法（如 ElasticNet）虽然在某些标签上表现良好，但整体一致性不及 IPBP。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_q7raIuTQDK/figures/003_Table_3.jpg]]
*Table 3: Intrinsic evaluation (label-averaged Spearman-R) between each pair of head-selection methods. Higher value means higher consistency with other methods. Values are averaged for each method in the last row*

### 4.4 消融实验

#### 4.4.1 正类互信息（MI_pos）的作用

将 MI_binary 替换为 MI_pos（仅考虑非 φ 标签）后，LAS 从 30.6 跃升至 34.8（Table 2）。这一提升表明，**排除长尾的“无依存关系”（φ 标签）噪声，专注于正类标签能显著改善标签预测质量**。混合 MI（MI_mix）的探索表明，通过平衡因子 α 调节二元与正类 MI 的权重，可在 UAS 和 LAS 之间取得折中。

#### 4.4.2 带宽消融

Table 8 展示了核密度估计中带宽参数的影响。**标准经验带宽（1×）取得最优 UAS 49.9 和 LAS 34.8**。带宽过小（0.5×）或过大（2×）均导致性能下降，验证了 KDE 对带宽的敏感性以及默认设置的有效性。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_q7raIuTQDK/figures/010_Table_8.jpg]]
*Table 8: Ablation results on different bandwidths*

#### 4.4.3 后验池化方法消融

Table 9 比较了不同后验池化策略。**对数池化（Logarithmic Pooling）取得 UAS 49.9，显著优于简单算术平均（UAS 36.2）和加权算术平均（UAS 36.3）**。这一结果证实了以 MI 为权重的几何平均（对数意见池化）在融合多专家头信息时的关键作用——指数加权形式能更有效地放大高 MI 头的贡献，同时抑制低信息头的噪声。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_q7raIuTQDK/figures/011_Table_9.jpg]]
*Table 9: Ablation results on different posterior pooling methods*

#### 4.4.4 专家头消融的因果验证

Table 4 展示了一个案例研究：移除 top-5 高 MI 头后，模型在预测需要相应句法信息的下一个 token 时的 logits 出现下降。例如，移除与 `nsubj` 相关的高 MI 头后，后续动词的 logits 显著降低。这一因果证据直接证明，**IPBP 识别的高 MI 头确实编码了与句法相关的功能信息**，而非统计假象。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_q7raIuTQDK/figures/005_Table_4.jpg]]
*Table 4: (Unnormalized) next-token logits for sentence In order to protect the environment, ecofriendly industries were before/after top-5 head ablation and random head ablation. ↓ means the logits has decreased, and vice versa*

### 4.5 层深度与树高的对应关系

论文探索了“模型层是否与树高对应”这一开放问题。通过计算 MI 加权的层索引与各依存标签平均深度的相关性，得到 Pearson ρ = 0.69（p = 0.03）。这一中等强度的正相关提供了初步证据，表明**较深的句法结构（如嵌套从句）倾向于由更深层的注意力头编码**，但因果关系尚未完全证实，需进一步实验验证。

### 4.6 失败模式与局限性

尽管 IPBP 在无监督句法探测中取得了最优结果，仍需注意以下局限：

1. **绝对性能差距**：与完全监督的依存解析器相比，IPBP 的 LAS/UAS 仍然较低，无法替代监督方法。
2. **架构依赖**：IPBP 目前仅针对基于 Transformer 的解码器架构 LLM 验证，尚未在编码器-解码器模型中测试；对于未来可能改变注意力机制的模型，需相应适配。
3. **计算效率**：对于极长句子，Eisner 算法的计算开销可能增大，效率有待优化。
4. **超参数敏感性**：头选择总数（如 2000）是经验性超参数，缺乏理论指导；带宽选择虽经验最优，但在不同模型和数据分布下可能需要调整。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_q7raIuTQDK/figures/006_Table_5.jpg]]
*Table 5: Maximum attention-based unbiased attention head analysis results for dependency relationships having top-10 largest maximum attention label recalls*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_q7raIuTQDK/figures/007_Table_6.jpg]]
*Table 6: Average token ranks (and average token rank proportions) on UD-2.9 English/French/Spanish train/dev set*

## 方法谱系与知识库定位

### 核心瓶颈与设计动机

现有基于注意力分数的句法探测方法面临两个根本性瓶颈。第一，**监督探针的不可解释性悖论**：以 **Linear Feedforward Family**（Dalvi et al., 2019）和 **V-Information**（Xu et al., 2020）为代表的有监督方法，通过训练可学习网络来评估注意力头的重要性，但引入的额外参数使探针本身可能学会任务，而非从模型中提取句法知识——用不可解释的组件去解释模型，逻辑上存在缺陷。第二，**原始注意力分数的信噪比问题**：直接信任注意力分数（Raw Attention Score baseline）忽略了注意力头并非专用于句法的事实，大量头编码的是语义或位置信息，需要有效的筛选与变换机制。

IPBP 的设计正是围绕这两个瓶颈展开：通过精确估计注意力分数与依存标签之间的混合分布并计算二元互信息（MI_binary），量化每个注意力头对特定依存关系的专属贡献，从而在**无训练参数**的条件下实现头筛选与树重建。这一思路将探测问题从“学习映射”转化为“信息量化”，从根本上规避了探针本身的学习能力干扰。

### 方法谱系中的定位

在句法探测方法谱系中，IPBP 占据了**无参数、基于信息论**的独特位置，与以下三类基线形成对比：

**无参数相关性方法**：**Probeless**（Antverg & Belinkov, 2022）通过计算有无特定概念时注意力均值的绝对差来衡量相关性；**IoU**（Mu & Andreas, 2020）则使用 Jaccard 相似度作为相关性准则。这些方法虽无需训练，但仅依赖一阶统计量（均值差）或启发式阈值（IoU 的 τ 截断），缺乏对注意力分数分布的完整建模。IPBP 通过 KDE 估计完整条件密度并计算互信息，提供了更严格的数学基础。实验证据表明，IPBP 在头选择的内在评估中取得了最高的平均 Spearman-R（0.398），显著优于 Probeless 和 IoU（Table 3），验证了信息论度量的优越性。

**有监督线性探针**：Linear Feedforward Family 和 V-Information 通过训练线性网络来排序头重要性，虽然可解释性较强（仅线性变换），但仍引入了可训练参数。IPBP 在完全无参数的前提下，通过内部评估中的最高一致性得分（0.398），证明了其头重要性排序的可靠性不亚于有监督方法。

**树重建基线**：Raw Attention Score、Left/Right Branching 和 Random Model 构成了树重建的对比基线。IPBP 的核心创新在于将树重建形式化为贝叶斯推理过程：以 MI 为权重的几何平均后验概率（对数意见池化）融合多专家头信息，并通过独立投票模型构建有效的概率空间。消融实验证实，对数池化显著优于算术平均（UAS 49.9 vs 36.2，Table 9），验证了指数加权机制的关键作用。

### 方法适用边界

IPBP 的适用性受以下条件约束：

1. **架构依赖**：方法目前仅在基于 Transformer 的解码器架构 LLM（open_llama_7b、Meta-Llama-3-8B、vicuna-7b、Mistral-7B）上验证，尚未在编码器-解码器模型中测试。对于未来可能改变注意力机制（如线性注意力、稀疏注意力）的模型，需要相应适配。

2. **无掩码注意力要求**：方法依赖于完整的、未被因果掩码截断的注意力分数，这限制了其在自回归解码场景下的直接应用范围。

3. **性能上限**：尽管 IPBP+MI_pos 在 open_llama_7b 上取得了当前最优的无监督结果（LAS 34.8, UAS 49.9），但与完全监督的依存解析器相比仍有较大差距，无法替代监督方法。

4. **计算效率边界**：对于极长句子，Eisner 算法的 $O(n^3)$ 复杂度可能成为瓶颈，效率有待优化。此外，头选择总数（如 2000）是经验性超参数，暂时缺乏理论指导。

### 已知局限与失效模式

1. **长尾噪声敏感性**：Binary MI 同时建模正类（特定依存标签）和负类（所有其他标签），导致长尾噪声影响性能。消融实验证实，仅关注正类标签的 Positive MI（MI_pos）使 LAS 提升 4.2 点（30.6→34.8），说明 Binary MI 在长尾分布下存在信息稀释问题。

2. **带宽敏感但可调**：KDE 带宽消融显示，标准经验带宽（1×）取得最佳 UAS（49.9），过小或过大带宽均导致性能下降（Table 8）。虽然标准设置在实验中表现稳定，但在不同模型或数据分布下可能需要重新校准。

3. **头选择阈值缺乏理论指导**：自适应阈值使用 MI_binary / H(1_l(L)) 归一化到 [0,1]，但总选择头数（2000）的设定依赖经验，缺乏信息论或统计学习理论的支持。

4. **跨语言泛化的未解问题**：虽然 Table 1 报告了多语言结果，但不同语言句法结构差异（如语序、形态丰富度）如何影响 MI 估计的有效性，尚未系统分析。

### 开放问题

1. **层-深度对应关系的因果性**：论文通过 MI 加权层索引与平均深度的 Pearson 相关性（ρ=0.69, p=0.03）给出了初步证据，但相关性不等于因果性，模型层是否真正按树高组织句法信息仍需进一步验证。

2. **向其他语法结构的拓展**：IPBP 的细粒度 MI 和概率函数框架能否拓展到成分句法或其他语言概念的解释，是一个自然的延伸方向。

3. **训练过程的融入**：能否将 IPBP 的 MI 估计作为正则项融入 LLM 训练，引导模型学习更好的句法表示，具有潜在的应用价值。

4. **无监督句法发现**：在没有现成标注的情况下，能否利用 IPBP 的框架进行无监督的句法发现，值得探索。

5. **跨模型句法知识存储模式**：不同 LLM 的句法知识存储模式有何差异？IPBP 的跨模型系统化分析仍有待开展，这可能为理解模型架构与句法涌现的关系提供关键线索。

## 原文 PDF

![[paperPDFs/ICLR_2026/An_Information_Theoretic_Parameter_Free_Bayesian_Framework_for_Probing_Labeled_Dependency_Trees_from_Attention_Score.pdf]]
