---
title: "Adaptive Debiasing Tsallis Entropy for Test-Time Adaptation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Adaptive_Debiasing_Tsallis_Entropy_for_Test_Time_Adaptation.pdf
project_link: null
code_link: https://github.com/Jinx630/ADTE
aliases:
- ADTEA
- ADTETTA
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "用类别自适应Tsallis熵替代统一Shannon熵进行测试时视图选择。"
primary_logic: "ADTE先估计类别先验偏差并归一化为类别特定q值，再用ADTE筛选高置信视图并集成预测。"
claims:
- "Tsallis熵在q小于1时能缓解VLM头尾类别预测偏差，Shannon熵可视为其极限形式。"
- "类别特定q值使ADTE比SE和固定q的TE更精确地选择高置信度增强视图。"
- "ADTE在ImageNet变体和跨域数据集上稳定优于Zero、Frolic等TTA方法。"
- "尾部类别分析显示ADTE显著提升低置信类别的准确率和预测置信度。"
---

# Adaptive Debiasing Tsallis Entropy for Test-Time Adaptation

> [!tip] 核心洞察
> Tsallis熵（TE）是Shannon熵（SE）的广义形式，当q<1时，TE能自然缓解VLM的预测偏差，且SE的性能是TE的下界；进一步地，通过为每个类别自适应地学习一个q^l参数（基于估计的标签偏差进行min-max归一化），ADTE能更精确地选择高置信度视图，并与logit调整策略无缝集成以增强适应性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向测试时自适应的自适应去偏Tsallis熵 |
| 英文题名 | Adaptive Debiasing Tsallis Entropy for Test-Time Adaptation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=dHj8hC081K) · [GitHub](https://github.com/Jinx630/ADTE) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Adaptive Debiasing Tsallis Entropy (ADTE) |
| Dataset | ImageNet, ImageNet-V2, ImageNet-K |

> [!tip] 效果简介
> - ImageNet 上，Accuracy (%) 为 71.8 (ADTE_Templates, ViT-B/16)，对比 70.9 (Zero_Templates, ViT-B/16)，变化 +0.9。
> - ImageNet 上，Accuracy (%) 为 72.7 (ADTE_CuPL, ViT-B/16)，对比 70.9 (Frolic_CuPL, ViT-B/16)，变化 +1.8。
> - ImageNet-V2 上，Accuracy (%) 为 65.6 (ADTE_Templates, ViT-B/16)，对比 64.7 (Zero_Templates, ViT-B/16)，变化 +0.9。

## 概要

本文提出了一种名为**自适应去偏Tsallis熵（Adaptive Debiasing Tsallis Entropy, ADTE）** 的新型测试时自适应（Test-Time Adaptation, TTA）方法，旨在解决视觉-语言模型（如CLIP）在测试时自适应过程中因预训练数据固有偏差导致的性能退化问题。核心思想是利用Tsallis熵（TE）的非广延参数q来校正模型对头部/尾部类别的预测偏差，并进一步通过为每个类别自适应地学习一个特定的参数q^l，实现更精确的高置信度视图选择。实验结果表明，ADTE在ImageNet及其五个变体数据集以及10个跨域基准测试上均超越了现有最先进方法，特别是在尾部类别上取得了显著的性能提升。

### 2.1 问题背景

视觉-语言模型（VLMs），如CLIP，在大规模网络数据上进行预训练，不可避免地继承了数据中的固有预测偏差。这种偏差导致模型对头部类别（head classes）表现出高置信度和高准确率，而对尾部类别（tail classes）则表现出低置信度和低准确率，如Figure 1(a)所示。

### 2.2 现有方法的不足

现有的基于Shannon熵（SE）的TTA方法（如Zero）在视图选择时采用统一的熵计算公式，无法区分不同类别偏差程度的差异。如原文所述："SE fails to account for varying degrees of bias in probabilities across different classes (i.e., head, middle, and tail classes). Instead, SE applies a uniform computation formula (−p log p) across all probabilities." 这种统一处理方式导致高置信度视图的选择受到偏差影响，进而影响最终的适应性能。

### 2.3 核心动机

本文的核心动机是：利用Tsallis熵（TE）作为Shannon熵的广义形式，通过引入非广延参数q来表征有偏分布，并进一步为每个类别自适应地调整参数，从而在视图选择过程中校正偏差，提升TTA性能。

## 核心方法与创新机理

本文的核心创新点可归纳为以下三个方面：

1. **理论发现：Tsallis熵是Shannon熵的广义形式，且SE的性能是TE的下界。** 当q<1时，TE能自然缓解VLM偏差的影响，且校正幅度随q减小而增大。如结论（Conclusion (3)）所示："when 0 < q < 1, TE can naturally mitigate the effect of VLM bias, with the correction magnitude increasing as q decreases."

2. **方法创新：自适应去偏Tsallis熵（ADTE）。** 通过为每个类别自适应地学习一个参数q^l（基于估计的标签偏差进行min-max归一化），ADTE能更精确地选择高置信度视图，并与logit调整策略无缝集成以增强适应性能。

3. **性能突破：在多个基准测试上超越现有最先进方法。** ADTE在ImageNet及其五个变体上取得了领先性能，并在10个跨域基准测试上取得了最高的平均性能。

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_dHj8hC081K_Adaptiv/figures/001_Figure_1.jpg]]

ADTE的整体框架如Figure 1(d)所示，其核心流程包括以下步骤：

1. **随机视图增强**：对每个测试实例生成N个增强视图。
2. **偏差估计**：使用Frolic的方法，通过Jacobi迭代从测试实例中估计每个类别的先验偏差。
3. **ADTE计算与视图选择**：根据估计的偏差计算每个类别的q^l，然后计算每个视图的ADTE值，并选择ADTE值最低的视图作为高置信度视图。
4. **高置信度视图集成**：对所选高置信度视图的预测分布进行平均，得到最终预测。

### 5.1 Shannon熵（SE）

Shannon熵是TTA中高置信度视图选择的常用指标，其定义为：

$$\mathbf{H}_{\mathtt{SE}}(\mathbf{P}(\cdot \mid \mathbf{x}_j^{\mathrm{test}})) = -\sum_{l=1}^{L} \mathbf{P}(y=l \mid \mathbf{x}_j^{\mathrm{test}}) \log[\mathbf{P}(y=l \mid \mathbf{x}_j^{\mathrm{test}})]$$

### 5.2 Tsallis熵（TE）

Tsallis熵是Shannon熵的广义形式，通过引入非广延参数q来表征有偏分布：

$$\mathbf{H}_{\mathrm{TE}}(\mathbf{P}(\cdot \mid \mathbf{x}_j^{\mathrm{test}})) = \frac{1}{1-q} \left( \sum_{l=1}^{L} \mathbf{P}(y=l \mid \mathbf{x}_j^{\mathrm{test}})^q - 1 \right)$$

**性质1**：当q趋近于1时，Tsallis熵退化为Shannon熵：

$$\lim_{q \to 1} \mathbf{H}_{\mathrm{TE}}(\mathbf{P}(\cdot \mid \mathbf{x}_j^{\mathrm{test}})) = \mathbf{H}_{\mathrm{SE}}(\mathbf{P}(\cdot \mid \mathbf{x}_j^{\mathrm{test}}))$$

**性质2**：随着参数q减小，TE选择的高置信度视图集倾向于具有更高的平均TcrK值（对于K>1）。

### 5.3 自适应去偏Tsallis熵（ADTE）

ADTE为每个类别l定制一个特定的参数q^l，其定义为：

$$\mathbf{H}_{\mathtt{ADTE}}(\mathrm{P}) = \sum_{l=1}^L \frac{\mathrm{P}_l^{q^l}}{1 - q^l}$$

### 5.4 偏差估计

ADTE采用Frolic的偏差估计方法，通过求解以下线性方程组来估计每个类别的先验概率：

$$\tilde{\mathrm{p}}_l = \sum_{l' \in \mathcal{V}^{\mathrm{test}}} \tilde{\mathrm{p}}_{l'} \cdot \mathbb{E}_{\mathbf{x} \sim \mathbf{P}(\mathbf{x}|l')}[\mathbf{P}(l \mid \mathbf{x})]$$

其中，期望通过伪标签近似计算：

$$\mathbb{E}_{{\mathbf{x}} \sim {\mathbf{P}}({\mathbf{x}} \mid l')}[{\mathbf{P}}(l \mid {\mathbf{x}})] = \frac{1}{N_{l'}} \sum_{{\mathbf{x}} \mid \hat{l}({\mathbf{x}}) = l'} {\mathbf{P}}(l \mid {\mathbf{x}})$$

该线性方程组通过Jacobi迭代求解：

$$\tilde{\mathrm{p}}_l^{(t+1)} = \sum_{l' \in \mathcal{V}^{\mathrm{test}}} \tilde{\mathrm{p}}_{l'}^{(t)} \cdot \mathbb{E}_{\mathbf{x} \sim \mathbf{p}(\mathbf{x} \mid l')}[\mathbf{P}(l \mid \mathbf{x})]$$

### 5.5 类别特定参数q^l的计算

基于估计的偏差，通过min-max归一化计算每个类别的参数q^l：

$$q^l = \alpha + (\beta - \alpha) \frac{-\log \tilde{\mathbf{p}}_l - \operatorname*{min}(\tilde{\mathbf{p}})}{\operatorname*{max}(\tilde{\mathbf{p}}) - \operatorname*{min}(\tilde{\mathbf{p}})}$$

其中，[α, β]是归一化区间，默认设置为[0.01, 0.9]。

## 实验与关键发现

### 6.1 主实验结果

**Table 1**展示了在ImageNet及其五个变体上的准确率比较结果。ADTE在ViT-B/16和ViT-L/14两种骨干网络上均取得了最优性能：

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_dHj8hC081K_Adaptiv/figures/008_Table_1.jpg]]
*Table 1: Accuracy comparison (%) on ImageNet and its variants for CLIP ViT-B/16 and ViT-L/14.*

- ADTE_Templates在ImageNet上达到71.8%，比Zero高0.9%。
- ADTE_CuPL在ImageNet上达到72.7%，比Frolic高1.8%。
- 在ImageNet-A上，ADTE_Templates达到65.5%，比Zero高3.1%。

**Table 2**展示了在10个跨域数据集上的平均准确率：

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_dHj8hC081K_Adaptiv/figures/009_Table_2.jpg]]
*Table 2: Accuracy comparison (%) on 10 cross-domain datasets for CLIP ViT-B/16 and ViT-L/14.*

- ADTE_Templates（ViT-B/16）达到69.0%，优于所有基于模板的方法。
- ADTE_CuPL（ViT-B/16）达到71.8%，超过Frolic的71.1%。

### 6.2 消融实验

**Table 3**的消融实验表明，移除ADTE组件（退化为Zero）导致ViT-B/16在ImageNet上准确率下降1.1%，在变体上下降0.7%，在10个数据集上下降2.1%。

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_dHj8hC081K_Adaptiv/figures/010_Table_3.jpg]]
*Table 3: Accuracy (%) of different models on 10-datasets, including ImageNet and its five variant datasets.*

**Table 4**比较了SE、TE和ADTE的性能，ADTE在所有指标上均表现最优。

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_dHj8hC081K_Adaptiv/figures/011_Table_4.jpg]]
*Table 4: Results for SE, TE, and ADTE. Table 5: Computational cost and effect of different intervals.*

### 6.3 尾部类别性能分析

**Table 7**和**Table 8**展示了ADTE在尾部类别上的显著改进：

- 原本准确率为0的尾部类别在ADTE下准确率提升至32.2%至56.5%。
- ADTE将尾部类别的平均预测置信度从0.1466提升至0.3638。
- ADTE将尾部类别的平均预测熵从5.2972降低至3.3761。

### 6.4 鲁棒性分析

**Table 19**表明ADTE对伪标签噪声具有鲁棒性，即使在80%噪声下准确率仍保持稳定（65.9% vs 65.4%）。

**Table 20**显示ADTE在所有偏差水平上均一致优于SE和TE，且优势随偏差增大而增大。

### 6.5 泛化性分析

**Table 23**展示了ADTE在不同CLIP泛化模型上的性能提升，包括OpenCLIP、EVA-CLIP、SigLIP和SigLIP2，均取得了稳定的改进。

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_dHj8hC081K_Adaptiv/figures/012_Table_5.jpg]]

## 定位与知识库关联

### 7.1 方法谱系

ADTE属于测试时自适应（TTA）方法家族，其方法谱系可概括如下：

1. **基于熵最小化的TTA方法**：如Tent（Wang et al., 2021）和Zero（Farina et al., 2024），通过最小化预测分布的熵来实现适应。
2. **基于提示调优的TTA方法**：如TPT（Shu et al., 2022）和DiffTPT，通过调整输入提示来适应测试样本。
3. **基于偏差校正的TTA方法**：如Frolic（Zhu et al., 2024），通过估计和校正模型偏差来提升性能。
4. **本文方法（ADTE）**：将Tsallis熵引入TTA，并通过自适应参数实现类别特定的偏差校正。

### 7.2 知识库定位

ADTE的核心贡献在于：

- **理论层面**：首次证明了Tsallis熵在TTA场景中相对于Shannon熵的理论优势，并建立了SE性能作为TE下界的理论框架。
- **方法层面**：提出了自适应去偏Tsallis熵（ADTE），通过类别特定参数实现了细粒度的偏差校正。
- **实践层面**：在多个基准测试上取得了最先进性能，特别是在尾部类别和跨域场景下表现突出。

### 7.3 局限性

1. ADTE的性能依赖于偏差估计的准确性，而偏差估计又依赖于伪标签的质量。尽管实验表明ADTE对伪标签噪声具有鲁棒性，但在极端噪声下性能仍可能受到影响。
2. ADTE需要维护一个记忆库来存储每个类别的样本，这增加了额外的内存开销。
3. ADTE的类别特定参数q^l通过min-max归一化计算，其区间[α, β]的选择可能需要针对不同任务进行微调。
4. 本文的方法主要针对视觉-语言模型（如CLIP）的TTA场景，其在其他类型的模型或任务上的适用性尚未验证。

## 原文 PDF

![[paperPDFs/ICLR_2026/Adaptive_Debiasing_Tsallis_Entropy_for_Test_Time_Adaptation.pdf]]
