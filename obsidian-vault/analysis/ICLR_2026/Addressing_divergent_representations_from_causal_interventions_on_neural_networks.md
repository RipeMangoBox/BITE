---
title: "Addressing divergent representations from causal interventions on neural networks"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Addressing_divergent_representations_from_causal_interventions_on_neural_networks.pdf
project_link: null
code_link: https://github.com/grantsrb/rep_divergence
openreview_forum_id: cZrTMqYVL6
aliases:
- MCLCLTCS
- ADRFCINN
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "干预表示与自然表示之间的分歧程度，特别是分歧是否位于行为零空间（无害）或超出零空间（有害）。通过控制分歧大小可影响干预的可靠性。"
primary_logic: "采用并修改自Grant (2025)的对比潜在（CL）损失，可以在保持互换干预准确率（IIA）的同时降低表示分歧，尤其将损失限制在因果子空间可提升OOD泛化能力，从而减少有害分歧。"
claims:
- "多种因果干预方法普遍产生表示分歧。"
- "CL损失可在不损害IIA的前提下降低表示分歧（EMD）。"
- "纯CL损失训练的对齐函数在OOD任务上的IIA高于纯行为损失。"
- "训练EMD与OOD的IIA显著反相关（R²=0.73，p<0.001）。"
---

# Addressing divergent representations from causal interventions on neural networks

> [!tip] 核心洞察
> 采用并修改自Grant (2025)的对比潜在（CL）损失，可以在保持互换干预准确率（IIA）的同时降低表示分歧，尤其将损失限制在因果子空间可提升OOD泛化能力，从而减少有害分歧。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 应对因果干预导致的神经网络表征分歧 |
| 英文题名 | Addressing divergent representations from causal interventions on neural networks |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=cZrTMqYVL6) · [GitHub](https://github.com/grantsrb/rep_divergence) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Modified Counterfactual Latent (CL) loss targeting causal subspaces |
| Dataset | Synthetic dataset (10 classes, 2 causal dims), Boundless DAS (LLM, Wu et al. 2023), Synthetic OOD generalization |

> [!tip] 效果简介
> - Synthetic dataset (10 classes, 2 causal dims) 上，IIA (Interchange Intervention Accuracy) 为 0.9988 ± 0.0005 (CL loss only)，对比 0.997 ± 0.001 (DAS behavioral loss only)，变化 +0.0018。
> - Synthetic dataset (10 classes, 2 causal dims) 上，EMD (Earth Mover's Distance) 为 0.007 ± 0.001 (CL loss only)，对比 0.032 ± 0.003 (DAS behavioral loss only)，变化 -0.025。
> - Boundless DAS (LLM, Wu et al. 2023) 上，IIA 为 Maintained (with suitable ε)，对比 DAS without CL loss，变化 No decrease; small ε improves。

## 概要

因果干预（causal intervention）——如激活修补、分布式对齐搜索（DAS）等——是解读神经网络内部机制的核心工具。然而，这些干预方法常常将内部表示**推离模型在自然输入下的分布**，产生所谓的“分歧表示”（divergent representations）。这种分歧并非无害：它可能意外激活隐藏通路，导致表面上符合预期的行为，或引发潜伏的行为变化，从而使干预结果对自然机制的解读变得不可靠。

本文的核心发现是：**表示分歧是多种因果干预方法的普遍现象**，但其危害性取决于分歧是否位于行为的零空间（null-space）之内。若分歧处于零空间，则对下游行为无影响，属于无害分歧；若超出零空间，则可能扭曲对机制的解读。基于此，本文提出并修改了来自 Grant (2025) 的**对比潜在损失（Counterfactual Latent loss, CL loss）**，用以在保持互换干预准确率（IIA）的同时，显著降低干预表示与自然分布之间的分歧。进一步地，将 CL 损失限制在因果子空间内计算，可在分布外（OOD）任务上提升干预的泛化能力。

实验表明：在合成数据集上，纯 CL 损失训练的对齐函数相比仅用行为损失的 DAS，**EMD（Earth Mover’s Distance）从 0.032 降至 0.007，同时 IIA 保持在 0.9988**；在 LLM 的 Boundless DAS 设置中，合适的 CL 权重可在不损害 IIA 的前提下降低分歧。线性回归分析进一步确认，训练过程中的因果轴 EMD 与 OOD 的 IIA 呈显著反相关（系数 -0.34，R²=0.73，p<0.001），为“降低分歧有助于提升干预可靠性”提供了定量证据。

### 因果干预在神经网络解释中的角色

现代神经网络的可解释性研究高度依赖**因果干预**技术来验证关于内部表征的机制性假设。这些干预方法——包括激活修补、分布式对齐搜索（DAS）等——通过对网络中间层表示进行反事实操纵，观察模型行为变化，从而推断特定子空间是否编码了特定的因果变量。然而，一个根本性的问题长期被忽视：**干预所产生的表示是否仍然位于模型自然分布的支撑集上？**

### 核心瓶颈：表示分歧的普遍性与危害

本工作揭示了一个贯穿多种干预方法的系统性现象——**表示分歧**。当通过激活修补、DAS 互换干预或稀疏自编码器投影等方式构造反事实表示 $\hat{h}$ 时，这些干预表示往往会偏离模型自然表示的分布。这种偏离并非偶发：在 **Mean Difference Vector Patching**（Feng & Steinhardt, 2024）、**Sparse Autoencoder Projections**（Bloom et al., 2024）以及 **Boundless DAS**（Wu et al., 2023）三种主流方法上均观察到显著的分布偏移，表现为 L2 距离增大和 Earth Mover's Distance（EMD）上升。

分歧的危害机制在于，神经网络的功能景观中存在两类关键区域：

- **隐藏通路**：分歧表示可能激活自然状态下不被使用的计算路径，产生表面“符合预期”的行为，但其内在机制已偏离自然推理过程，导致对网络机制的解读被误导。
- **潜伏行为边界**：分歧表示可能跨越决策边界，触发在干预评估中未被检测到的行为变化，使研究者误认为干预是“干净的”。

这两种情形分别对应**误导性确认行为**和**潜伏行为变化**，其共同后果是：基于干预结果对网络自然机制做出的因果推断可能不可靠。

### 行为零空间：无害与有害分歧的理论边界

为精确刻画分歧的危害性，本文引入了**行为零空间**的概念。对于网络后续层组成的函数 $\psi$ 和输入集合 $X$，行为零空间定义为：

$$\mathcal{N}(\psi, X) = \{ v \in \mathbb{R}^d \mid \forall x \in X, \psi(x + v) = \psi(x) \}$$

若干预表示与自然表示之间的差异向量 $v$ 完全位于行为零空间内，则该分歧是**无害的**——它不会改变下游行为，因此不会扭曲对网络机制的解读。反之，任何溢出零空间的分歧都是**潜在有害的**，因为它必然在某些上下文中改变了模型行为，而这些变化可能未被当前的评估数据集覆盖。

这一理论框架揭示了现有因果干预方法的一个根本性缺口：**DAS 等方法的训练目标仅优化互换干预准确率（IIA），对表示分歧没有任何约束**。行为损失 $\mathcal{L}_{\mathrm{DAS}}$ 鼓励对齐函数找到能使反事实输出正确的子空间，但并不关心干预表示是否偏离自然分布。这导致训练出的对齐函数可能利用网络的“捷径”——通过将干预表示推向自然分布之外的区域来满足行为目标，从而产生有害分歧。

### 本文动机与解决思路

面对上述问题，本文的核心动机是：**在保持因果干预有效性的前提下，系统性地减少表示分歧，从而提升干预结果对网络自然机制解读的可靠性**。

具体而言，本文借鉴并修改了 Grant (2025) 提出的**对比潜在损失**，将其作为辅助训练目标引入 DAS 的对齐函数训练中。该损失通过拉近干预表示与具有相同因果变量值的自然表示之间的距离，引导干预表示回归自然分布流形。进一步，本文提出仅在因果子空间上施加该损失，以针对性减少最可能有害的分歧成分，并在分布外泛化任务上验证其效果。

## 核心方法与创新机理

本工作的核心创新不在于提出全新的因果干预范式，而是在现有因果干预框架（特别是 DAS）中引入并改造了一种**表示分歧感知的训练机制**，使干预结果在保持行为准确性的同时更贴近模型的自然表示分布。具体而言，关键创新体现在以下两个层面的 **changed slots** 上：

### 1. 训练损失函数：从纯行为损失到行为-表示联合优化

**基线方案**（DAS, Wu et al., 2023）仅使用行为损失 $\mathcal{L}_{\mathrm{DAS}}$ 训练对齐函数 $\mathcal{A}$，该损失以反事实标签为目标，最小化负对数似然：

$$\mathcal{L}_{\mathrm{DAS}}(\mathcal{A}) = -\frac{1}{N} \sum_{k=1}^{N} \log p_{\mathcal{A}}(c^{(k)} \mid x^{(k)}, \hat{h}^{(k)})$$

此方案完全不约束干预表示 $\hat{h}$ 与自然表示分布的关系，是导致表示分歧的根本原因之一。

**本工作提案**：引入总损失 $\mathcal{L}_{\mathrm{total}} = \epsilon \mathcal{L}_{\mathrm{CL}} + \mathcal{L}_{\mathrm{DAS}}$，其中 $\mathcal{L}_{\mathrm{CL}}$ 为改造自 Grant (2025) 的对比潜在（Counterfactual Latent, CL）损失：

$$\mathcal{L}_{\mathrm{CL}}(\hat{h}, h_{\mathrm{CL}}) = \frac{1}{2} \|\hat{h} - h_{\mathrm{CL}}\|_2^2 - \frac{1}{2} \frac{\hat{h} \cdot h_{\mathrm{CL}}}{\|\hat{h}\|_2 \|h_{\mathrm{CL}}\|_2}$$

该损失同时优化 L2 距离和余弦相似度，将干预表示拉向具有相同因果变量值的自然表示（即 CL 向量）。关键证据来自 **Figure 3B**：在合适的 CL 权重 $\epsilon$ 下，互换干预准确率（IIA）得以维持甚至略有提升，同时 Earth Mover's Distance（EMD）显著下降。过大的 $\epsilon$ 会损害 IIA，表明存在一个行为-表示保真度的权衡区间。

### 2. 损失作用空间：从全空间到因果子空间

**基线方案**：CL 损失在全表示空间上计算，这虽然降低了整体分歧，但无法区分分歧中“无害”（位于行为零空间内）与“有害”（超出行为零空间）的成分。

**本工作提案**：将 CL 损失限制在 DAS 发现的因果子空间内，对每个因果变量 $\mathrm{var}_i$ 分别构造干预表示和 CL 反事实表示：

$$\hat{h}^{\mathrm{var}_i} = \mathcal{A}^{-1}( D_{\mathrm{var}_i} \mathcal{A}(\hat{h}) ), \quad h_{\mathrm{CL}}^{\mathrm{var}_i} = \mathrm{stopgrad}(\mathcal{A}^{-1}( D_{\mathrm{var}_i} \mathcal{A}(h_{\mathrm{CL}}) ))$$

然后对每个变量子空间独立施加 CL 损失并求和：

$$\mathcal{L}_{\mathrm{CL}}' = \sum_{i=1}^{n} \mathcal{L}_{\mathrm{CL}}^{\mathrm{var}_i}$$

这一修改的动机在于：只有位于因果子空间的分歧才可能改变因果变量的编码值，从而直接影响下游行为；其他维度的分歧可能仅仅是行为零空间中的扰动，对其施加惩罚不仅无益，反而可能挤占优化容量。**Figure 3F** 的 OOD 泛化实验提供了支持证据：修改后的 CL 损失（仅作用于因果子空间）在 OOD 任务上的 IIA 高于纯行为损失训练的基线，也优于全空间 CL 损失。附录 A.6 的线性回归进一步量化了这一关系：训练阶段的因果轴 EMD 与 OOD 的 IIA 呈显著负相关（系数 $-0.34$，$R^2 = 0.73$，$p < 0.001$），表明**降低因果子空间内的分歧直接有助于提升干预的 OOD 泛化能力**。

### 创新本质总结

上述两个 changed slots 共同构成了一个“分歧最小化”的干预训练范式：通过 $\mathcal{L}_{\mathrm{CL}}$ 引入表示分布的先验约束，再通过因果子空间定位将约束聚焦于行为相关的维度。这一设计不改变 DAS 的互换干预机制本身，也不修改模型的冻结权重，而是**在训练对齐函数时附加了一个分布正则化项**，使学到的对齐函数天然倾向于产生更接近自然分布的干预表示，从而降低激活隐藏通路或触发潜伏行为变化的风险。

本工作的核心流程围绕一个基本问题展开：因果干预产生的表示与模型自然分布之间的“表示分歧”是否可控，以及如何在不损害干预准确率的前提下降低有害分歧。整体框架由四个逻辑层构成：**分歧诊断**、**无害性判定**、**分歧缓解训练**、以及**因果子空间约束**。

### 分歧诊断层

对于给定的因果干预方法——包括激活修补（activation patching）、稀疏自编码器投影（sparse autoencoder projections）、以及分布式对齐搜索（DAS）——框架首先量化干预表示 $\hat{h}$ 与自然表示 $h$ 之间的分歧程度。核心度量指标为 Earth Mover's Distance（EMD），用于比较干预表示分布与自然表示分布的整体偏移（Figure 2）。诊断层揭示了一个普遍现象：**多种主流因果干预技术均会系统性地产生表示分歧**，这一结论在理论上也得到了支持：只要数据流形不是轴对齐的超矩形，坐标式修补几乎必然生成偏离流形的表示（Section 3.1）。

### 无害性判定层

并非所有分歧都会导致误导性的机理解读。框架引入**行为零空间**（behavioral null-space）的概念来区分无害与有害分歧：

$$
\mathcal{N}(\psi, X) = \{ v \in \mathbb{R}^d \mid \forall x \in X, \psi(x + v) = \psi(x) \}
$$

若干预带来的分歧向量 $v$ 完全位于行为零空间内，则它对函数 $\psi$ 的输出不产生任何影响，因而对功能层面的因果主张是无害的（Section 4.1）。反之，若分歧超出零空间，则可能激活**隐藏通路**（hidden circuits）或触发**潜伏行为变化**（dormant behavioral changes）——即在某些未见上下文中改变模型输出，使干预结果表面上确认了错误假设（Section 4.2）。

### 分歧缓解训练层

为主动降低表示分歧，框架引入并修改了来自 Grant (2025) 的**对比潜在损失**（Counterfactual Latent loss, CL loss）。CL 损失的核心思想是：为每个干预表示 $\hat{h}$ 构造一个“CL 向量” $h_{\mathrm{CL}}$——即与 $\hat{h}$ 具有相同因果变量值的自然表示的平均——并强制 $\hat{h}$ 向 $h_{\mathrm{CL}}$ 靠拢。损失函数由 L2 距离和余弦距离的均值构成：

$$
\mathcal{L}_{\mathrm{CL}}(\hat{h}, h_{\mathrm{CL}}) = \frac{1}{2} \|\hat{h} - h_{\mathrm{CL}}\|_2^2 - \frac{1}{2} \frac{\hat{h} \cdot h_{\mathrm{CL}}}{\|\hat{h}\|_2 \|h_{\mathrm{CL}}\|_2}
$$

训练总损失为 CL 损失与 DAS 行为损失 $\mathcal{L}_{\mathrm{DAS}}$ 的加权组合：

$$
\mathcal{L}_{\mathrm{total}} = \epsilon \mathcal{L}_{\mathrm{CL}} + \mathcal{L}_{\mathrm{DAS}}
$$

其中 $\epsilon$ 控制 CL 损失的强度。该层的核心发现在于：**合适的 $\epsilon$ 可在维持互换干预准确率（IIA）的同时显著降低 EMD**（Figure 3B），而过大的 $\epsilon$ 则会损害 IIA。

### 因果子空间约束层

全空间 CL 损失虽然降低了整体分歧，但可能对非因果维度的约束过于松散。框架进一步提出**修改版 CL 损失** $\mathcal{L}_{\mathrm{CL}}'$，仅对已发现的因果变量子空间施加分歧最小化约束。对于每个因果变量 $\mathrm{var}_i$，分别构造子空间干预表示和 CL 反事实表示：

$$
\hat{h}^{\mathrm{var}_i} = \mathcal{A}^{-1}( D_{\mathrm{var}_i} \mathcal{A}(\hat{h}) ), \quad h_{\mathrm{CL}}^{\mathrm{var}_i} = \mathrm{stopgrad}(\mathcal{A}^{-1}( D_{\mathrm{var}_i} \mathcal{A}(h_{\mathrm{CL}}) ))
$$

然后将各子空间的 CL 损失求和：

$$
\mathcal{L}_{\mathrm{CL}}' = \sum_{i=1}^{n} \mathcal{L}_{\mathrm{CL}}^{\mathrm{var}_i}
$$

实验表明，这种针对性约束在分布外（OOD）任务上带来了更高的 IIA（Figure 3F），且训练 EMD 与 OOD IIA 之间存在显著的反相关关系（$R^2 = 0.73$, $p < 0.001$，附录 A.6），定量验证了“降低有害分歧可提升干预泛化能力”这一核心假设。

### 对齐函数与互换干预

本文方法建立在**分布式对齐搜索（DAS）**框架之上。设模型在某一中间层的隐藏状态为 $h \in \mathbb{R}^d$，对齐函数 $\mathcal{A}$ 是一个可学习的可逆线性变换，将 $h$ 映射到由正交子空间组成的可解释向量 $z$：

$$\mathcal{A}(h) = z = [\vec{z}_{\mathrm{var}_1}, \vec{z}_{\mathrm{var}_2}, \ldots, \vec{z}_{\mathrm{var}_n}, \vec{z}_{\mathrm{extra}}]$$

其中每个 $\vec{z}_{\mathrm{var}_i}$ 对应一个因果变量子空间，$\vec{z}_{\mathrm{extra}}$ 为额外维度。

**互换干预**通过修补单个因果变量子空间实现反事实操纵。给定源表示 $h^{\mathrm{src}}$ 和目标表示 $h^{\mathrm{trg}}$，对变量 $\mathrm{var}_i$ 的干预表示为：

$$\hat{h} = \mathcal{A}^{-1}\big((\mathcal{I} - D_{\mathrm{var}_i}) \mathcal{A}(h^{\mathrm{trg}}) + D_{\mathrm{var}_i} \mathcal{A}(h^{\mathrm{src}})\big)$$

其中 $D_{\mathrm{var}_i}$ 是仅保留 $\mathrm{var}_i$ 对应子空间的对角二值矩阵。该操作将源表示中该变量的子空间活动“移植”到目标表示中。

### DAS 行为损失

DAS 通过对齐函数训练来发现神经表示子空间与因果变量之间的对应关系。给定反事实标签 $c^{(k)}$，训练目标为最小化负对数似然：

$$\mathcal{L}_{\mathrm{DAS}}(\mathcal{A}) = -\frac{1}{N} \sum_{k=1}^{N} \log p_{\mathcal{A}}(c^{(k)} \mid x^{(k)}, \hat{h}^{(k)})$$

梯度仅回传至对齐函数 $\mathcal{A}$，模型权重保持冻结。

### 行为零空间

为判断表示分歧是否有害，论文引入**行为零空间**的概念。对于函数 $\psi$ 和输入集合 $X$，行为零空间定义为：

$$\mathcal{N}(\psi, X) = \{ v \in \mathbb{R}^d \mid \forall x \in X,\ \psi(x + v) = \psi(x) \}$$

若干预产生的分歧向量 $v$ 位于行为零空间内，则添加该向量不会改变模型输出，分歧被认为是**无害的**；反之，若分歧超出零空间，则可能激活隐藏通路或引发潜伏行为变化，构成**有害分歧**。

### CL 辅助损失

核心创新在于引入并修改来自 Grant (2025) 的**对比潜在（CL）损失**，以降低干预表示与自然分布之间的分歧。CL 向量 $h_{\mathrm{CL}}$ 定义为与干预后表示具有相同因果变量值的自然表示集合的均值。CL 损失由 L2 距离和余弦距离的平均值组成：

$$\mathcal{L}_{\mathrm{CL}}(\hat{h}, h_{\mathrm{CL}}) = \frac{1}{2} \|\hat{h} - h_{\mathrm{CL}}\|_2^2 - \frac{1}{2} \frac{\hat{h} \cdot h_{\mathrm{CL}}}{\|\hat{h}\|_2 \|h_{\mathrm{CL}}\|_2}$$

总损失为 CL 损失与 DAS 行为损失的加权组合：

$$\mathcal{L}_{\mathrm{total}} = \epsilon \mathcal{L}_{\mathrm{CL}} + \mathcal{L}_{\mathrm{DAS}}$$

其中超参数 $\epsilon$ 控制 CL 损失的强度。实验表明（Figure 3B），合适的 $\epsilon$ 可在维持互换干预准确率（IIA）的同时显著降低 Earth Mover's Distance（EMD）；过大的 $\epsilon$ 则会损害 IIA。

### 修改版 CL 损失：因果子空间约束

为进一步提升 OOD 泛化能力，论文提出修改版 CL 损失，仅作用于各因果变量子空间。对单个变量 $\mathrm{var}_i$，分别构造干预表示和 CL 反事实表示：

$$\hat{h}^{\mathrm{var}_i} = \mathcal{A}^{-1}\big(D_{\mathrm{var}_i} \mathcal{A}(\hat{h})\big), \quad h_{\mathrm{CL}}^{\mathrm{var}_i} = \mathrm{stopgrad}\big(\mathcal{A}^{-1}(D_{\mathrm{var}_i} \mathcal{A}(h_{\mathrm{CL}}))\big)$$

其中 $\mathrm{stopgrad}$ 阻止梯度回传至 CL 向量。修改版 CL 损失将所有因果变量的子空间损失相加：

$$\mathcal{L}_{\mathrm{CL}}' = \sum_{i=1}^{n} \mathcal{L}_{\mathrm{CL}}^{\mathrm{var}_i}$$

与全空间 CL 损失相比，该修改版在合成 OOD 任务上取得了更高的 IIA（Figure 3F）。附录 A.6 的线性回归进一步证实，训练过程中的因果轴 EMD 与 OOD 的 IIA 显著反相关（系数 $-0.34$，$R^2 = 0.73$，$p < 0.001$），表明降低因果子空间内的分歧是提升干预泛化能力的关键机制。

## 实验与关键发现

### 因果干预中的表示分歧是普遍现象

论文首先系统性地验证了一个关键前提：多种主流因果干预方法都会导致干预后的表示偏离模型自然分布。Figure 2 给出了这一现象的实验证据，涵盖三种代表性干预技术：

- **Mean Difference Vector Patching**（Feng & Steinhardt, 2024）：通过替换残差流中的坐标值进行干预。
- **Sparse Autoencoder Projections**（Bloom et al., 2024）：使用 SAELens 重建单层 Transformer 的向量。
- **Boundless DAS**（Wu et al., 2023）：通过可学习的对齐函数进行互换干预。

Figure 2(c) 量化了这种分歧：干预表示与对应自然表示之间的 L2 距离显著大于自然表示之间的基线距离，且干预分布与自然分布之间的 Earth Mover's Distance（EMD）也明显偏离。这一结果构成了全文的动机基础——如果因果干预产生的表示本身不在模型“熟悉”的分布内，那么基于这些干预得出的机制解读就可能被隐藏通路或潜伏行为变化所污染。

### CL 损失在保持干预准确率的同时降低表示分歧

论文的核心实验围绕修改后的 Counterfactual Latent（CL）损失展开。CL 损失源自 Grant (2025)，其核心思想是为每个干预表示 $\hat{h}$ 构造一个“CL 向量” $h_{\mathrm{CL}}$——即从自然分布中选取与 $\hat{h}$ 具有相同因果变量值的表示的平均——然后最小化 $\hat{h}$ 与 $h_{\mathrm{CL}}$ 之间的 L2 距离和余弦距离：

$$\mathcal{L}_{\mathrm{CL}}(\hat{h}, h_{\mathrm{CL}}) = \frac{1}{2} \|\hat{h} - h_{\mathrm{CL}}\|_2^2 - \frac{1}{2} \frac{\hat{h} \cdot h_{\mathrm{CL}}}{\|\hat{h}\|_2 \|h_{\mathrm{CL}}\|_2}$$

总损失为 $\mathcal{L}_{\mathrm{total}} = \epsilon \mathcal{L}_{\mathrm{CL}} + \mathcal{L}_{\mathrm{DAS}}$，其中 $\epsilon$ 控制 CL 损失的权重。

**Boundless DAS 实验（Figure 3B）** 展示了 CL 损失的效果：
- 当 $\epsilon$ 取较小值时，互换干预准确率（IIA）得以维持甚至略有提升，同时 EMD 显著下降。
- 过大的 $\epsilon$ 会损害 IIA，表明存在一个行为损失与表示对齐之间的权衡区间。

这一发现的关键在于：CL 损失并非以牺牲干预有效性为代价来降低分歧，而是在合适的权重下实现了两者的兼顾。

### 合成数据上的定量结果

在具有 10 个类别、2 个因果维度的合成数据集上，论文对比了三种训练策略（Figure 3D/E）：

| 训练策略 | EMD | IIA |
|---------|-----|-----|
| DAS 行为损失（基线） | 0.032 ± 0.003 | 0.997 ± 0.001 |
| 纯 CL 损失 | **0.007 ± 0.001** | **0.9988 ± 0.0005** |

纯 CL 损失在 IIA 上略优于行为损失，同时在 EMD 上降低了约 78%。这一结果令人惊讶：仅通过让干预表示接近自然分布，就能学到有效的因果对齐，甚至在某些情况下比直接优化反事实标签更准确。

### 修改版 CL 损失与 OOD 泛化

论文进一步提出了修改版 CL 损失 $\mathcal{L}_{\mathrm{CL}}'$，其关键改动是**仅在因果子空间上计算 CL 损失**，而非作用于整个表示空间：

$$\hat{h}^{\mathrm{var}_i} = \mathcal{A}^{-1}( D_{\mathrm{var}_i} \mathcal{A}(\hat{h}) ), \quad h_{\mathrm{CL}}^{\mathrm{var}_i} = \mathrm{stopgrad}(\mathcal{A}^{-1}( D_{\mathrm{var}_i} \mathcal{A}(h_{\mathrm{CL}}) ))$$

$$\mathcal{L}_{\mathrm{CL}}' = \sum_{i=1}^{n} \mathcal{L}_{\mathrm{CL}}^{\mathrm{var}_i}$$

**OOD 泛化实验（Figure 3F）** 是论文最具说服力的结果之一：将在一种任务分区上训练的对齐函数迁移到使用相同因果维度但不同类别分布的另一分区上评估。结果显示，纯 CL 损失训练的 OOD IIA 高于纯行为损失训练。这意味着 CL 损失学到的对齐更贴近真实的因果结构，而非过拟合到训练分布的行为表面。

**附录 A.6 的线性回归分析** 提供了定量佐证：训练过程中的因果轴 EMD 与 OOD IIA 之间存在显著的负相关关系（回归系数 = -0.3424，$R^2 = 0.729$，$F(1,28) = 75.28$，$p < 0.001$）。这说明表示分歧越小，干预的泛化能力越强，为“降低分歧有助于提升干预可靠性”这一核心主张提供了统计证据。

### 消融与鲁棒性分析

**CL 权重消融（Figure 3B）**：如前所述，过大的 $\epsilon$ 会损害 IIA，但合适的 $\epsilon$ 可在保持 IIA 的同时降低 EMD，验证了 CL 损失作为辅助损失的有效性范围。

**子空间定位消融（Section 5.2, Figure 3F）**：修改后的 CL 损失（仅作用于因果子空间）在 OOD 任务上优于作用于全空间的 CL 损失，表明针对性减少有害分歧比盲目缩小所有分歧更有效。

**超参数鲁棒性（附录 Figures 6-9）**：在不同学习率和额外噪声维度下，CL 损失普遍降低 EMD 且保持 IIA，说明该方法对超参数选择具有一定的鲁棒性。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_cZrTMqYVL6/figures/010_Figure_9.jpg]]
*Figure 9: In distribution hyperparameter search showing the DAS row-space EMD on validation data for the trained task partition. We see the DAS loss learning rate (lr) and extra concatenated noisy input dimensions (extra_dim) across the panel columns and rows. The DAS+CL reported values include the behavioral loss whereas the CL label excludes the behavioral loss. The pink dashed lines represent DAS trained with the behavioral loss only*

### 失败模式与局限性

尽管实验结果整体正面，论文明确指出以下局限：

1. **分歧最小化不等于风险消除**：降低 EMD 只能缩小干预表示偏离自然分布的程度，但即使很小的分歧也可能恰好落在隐藏通路或潜伏行为边界上。论文提出的无害/有害判定算法（Algorithm 1）仅为近似方法，无法穷举所有上下文进行验证。

2. **潜伏行为变化的检测盲区**：Figure 1(b) 底部所示的情形——干预表示虽未改变当前上下文下的输出，但在其他上下文中可能触发不同行为——是当前方法无法系统处理的。论文将此定义为“潜伏行为变化”（dormant behavioral changes），并承认缺乏高效的检测手段。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_cZrTMqYVL6/figures/001_Figure_1.jpg]]
*Figure 1: Causal interventions can recruit hidden circuits that produce misleadingly confirmatory or dormant behavior. (a) Consider natural pathways (dashed arrows) for two classes A and B that carry activity to different behavioral outputs y. In a hypothetical intervention meant to find path A, patching h ^ { 1 } with a divergent representation can activate distinct, hidden pathways (solid arrows) that result in misleadingly confirmatory behavior (orange) and/or undetected behavior (red). (b) Consider 2D projections of the neural activity of h ^ { 1 } for a different network that classifies states into one of 10 classes (denoted by hue). Suppose that natural representations (dark points) lie within...*

3. **实验设置的限制**：当前验证仅在简单合成数据集和 LLM 的 Boundless DAS 设置上进行，是否适用于更复杂的网络结构（如深层 Transformer 的多层交互）和更多因果变量的场景尚不明确。

4. **零空间之外的分歧不可穷举验证**：理论分析指出，任何位于行为零空间之外的分歧都可能是“有害的”，但在实践中不可能对所有输入上下文进行穷举测试来确认其无害性。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_cZrTMqYVL6/figures/005_Figure_4.jpg]]
*Figure 4: A number of additional divergence measures to demonstrate the difference between the natural and intervened distributions. Each is labeled by its y-axis. Each metric is computed over a random sample of natural vectors to simulate the natural manifold, and a sampled set of intervened or natural vectors for which to measure the distance from the natural distribution. We refer to this distribution as the "compared" distribution. The sampled intervened and natural vectors are always the "ground-truth pair" described at the beginning of Appendix A.1. Nearest Cosine Distance: refers to the cosine distance to the nearest sample in the natural manifold. Multiple sampes in the compared distribution...*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_cZrTMqYVL6/figures/004_Table.jpg]]

## 定位与知识库关联

### 问题来源与基线脉络

本文的核心问题——因果干预产生的表示分歧——源于分布式对齐搜索（DAS）及其变体在机制可解释性中的广泛应用。DAS（**Wu et al., 2023**）通过可学习的可逆线性变换 $\mathcal{A}$ 将隐藏状态映射到可解释子空间，再通过互换干预（Interchange Intervention）操纵单个因果变量，以验证因果抽象假设。其训练目标仅依赖行为损失 $\mathcal{L}_{\mathrm{DAS}}$（交叉熵），不约束干预表示与自然分布的关系。

本文在实验中将 DAS（仅行为损失）作为**主要对比基线**，同时考察了另外两种常见因果干预方法以展示分歧现象的普遍性：
- **Mean Difference Vector Patching**（**Feng & Steinhardt, 2024**）：通过替换类别均值差异向量进行激活修补。
- **Sparse Autoencoder Projections**（**Bloom et al., 2024**）：利用稀疏自编码器对单层 Transformer 的重构向量进行投影干预。
- **Boundless DAS**（**Wu et al., 2023**）：DAS 在 LLM 上的设置，本文用于 LLM 实验验证。

### 方法继承与修改

本文的核心技术组件——对比潜在（CL）损失——直接继承自 **Grant (2025)**，但进行了两项关键修改：

**修改一：引入行为损失联合训练。** Grant (2025) 的原始 CL 损失作为独立目标使用；本文将其与 DAS 行为损失组合为加权总损失：
$$\mathcal{L}_{\mathrm{total}} = \epsilon \mathcal{L}_{\mathrm{CL}} + \mathcal{L}_{\mathrm{DAS}}$$
其中 $\epsilon$ 为超参数，控制表示对齐与行为保真之间的权衡。CL 损失本身定义为干预表示 $\hat{h}$ 与 CL 向量 $h_{\mathrm{CL}}$ 之间的 L2 距离和余弦距离的均值：
$$\mathcal{L}_{\mathrm{CL}}(\hat{h}, h_{\mathrm{CL}}) = \frac{1}{2} \|\hat{h} - h_{\mathrm{CL}}\|_2^2 - \frac{1}{2} \frac{\hat{h} \cdot h_{\mathrm{CL}}}{\|\hat{h}\|_2 \|h_{\mathrm{CL}}\|_2}$$
CL 向量来自具有相同因果变量值的自然表示集合，作为干预表示应靠近的“自然锚点”。

**修改二：将 CL 损失限制在因果子空间。** 原始 CL 损失在全空间上计算；本文提出修改版 $\mathcal{L}_{\mathrm{CL}}'$，仅对每个已发现的因果变量子空间单独施加 CL 损失：
$$\hat{h}^{\mathrm{var}_i} = \mathcal{A}^{-1}( D_{\mathrm{var}_i} \mathcal{A}(\hat{h}) ), \quad h_{\mathrm{CL}}^{\mathrm{var}_i} = \mathrm{stopgrad}(\mathcal{A}^{-1}( D_{\mathrm{var}_i} \mathcal{A}(h_{\mathrm{CL}}) ))$$
$$\mathcal{L}_{\mathrm{CL}}' = \sum_{i=1}^{n} \mathcal{L}_{\mathrm{CL}}^{\mathrm{var}_i}$$
这一修改的动机在于：仅因果子空间中的分歧可能超出行为零空间而变得有害，全空间约束可能引入不必要的正则化。

### 理论贡献与知识定位

本文的理论框架独立于上述基线方法，其核心贡献在于**形式化了表示分歧的“无害/有害”判定条件**：

- **行为零空间**（Behavioral Null-space）：$\mathcal{N}(\psi, X) = \{ v \in \mathbb{R}^d \mid \forall x \in X, \psi(x + v) = \psi(x) \}$。位于零空间内的分歧对功能声明无害。
- **潜伏行为变化**（Dormant Behavioral Changes）：$\mathcal{V}(\psi, X, \mathcal{C}_1, \mathcal{C}) = \mathcal{N}(\psi, X, \mathcal{C}_1) \setminus \mathcal{N}(\psi, X, \mathcal{C})$，即某些上下文中无害、但在更广泛上下文中改变行为的分歧——这是当前方法无法系统检测的盲区。

该框架将因果干预的可靠性问题从经验观察提升到了可分析的理论层面，但判定算法（Algorithm 1）仅提供近似保障。

### 适用边界与局限

**已验证有效的场景：**
- 合成数据集（10 类、2 个因果维度）上的 DAS 训练。
- Boundless DAS 在 LLM 上的应用（Wu et al., 2023 的设置）。

**明确不适用或未验证的场景：**
- 更复杂的网络结构和更多因果变量。
- 除 DAS 外的其他干预方法（SAE、mean difference patching 等仅用于展示分歧，未验证 CL 损失在这些方法上的效果）。
- 潜伏行为变化的检测——当前方法无法穷举所有上下文进行验证，任何位于零空间之外的分歧都可能是“有害的”。

**方法本身的固有局限：**
- 最小化表示分歧的大小只能降低风险面，不能保证消除隐藏通路的激活。
- 无害/有害的判定依赖于具体的机制声明——修改声明会改变无害分歧的集合。

### 开放问题

1. **有害分歧的自监督分类与缓解**：当前方法依赖已知的因果变量和 CL 向量构造，如何在没有标注的情况下自动识别并针对性减少有害分歧？
2. **任意声明的原则性判定**：如何为任意机理解释主张设计通用的有害分歧判定方法，而非依赖特定的行为零空间假设？
3. **扩展到复杂架构**：修改后的 CL 损失能否推广到更深、更宽的网络以及更多的因果变量，同时保持计算可行？
4. **与其他可解释性方法的结合**：表示分歧最小化能否与 SAE 等方法互补，进一步提升干预的可靠性？
5. **潜伏行为变化的系统检测**：如何高效地在所有可能上下文中发现潜伏的行为变化，而非仅依赖有限采样？

## 原文 PDF

![[paperPDFs/ICLR_2026/Addressing_divergent_representations_from_causal_interventions_on_neural_networks.pdf]]
