---
title: "Learning with Dual-level Noisy Correspondence for Multi-modal Entity Alignment"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Learning_with_Dual_level_Noisy_Correspondence_for_Multi_modal_Entity_Alignment.pdf
project_link: null
code_link: https://github.com/XLearning-SCU/2026-ICLR-RULE
openreview_forum_id: mytIKuRsSE
aliases:
- LDLNCMMEA
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "同时利用不确定性和共识双重原则评估对应可靠性，将跨图对划分为高不确定性、低共识和干净三类，在训练中排除或软化噪声对，并采用加权融合抑制不可靠属性；推理阶段借助 MLLM 进行链式思维推理，挖掘隐式属性连接，实现全链路抗噪。"
primary_logic: "低不确定性不一定保证正确匹配（Theorem 1），因此必须结合共识原则；将主观逻辑与 Dirichlet 分布用于量化证据并控制过拟合；采用边际贡献的贪婪策略自动推断可靠对应，并在测试时利用大模型知识进行深度推理，提升噪声下的鲁棒性。"
claims:
- "定理 1 证明低不确定性不能保证高信念落在标注对应上，因而需要共识原则。"
- "消融实验表明，移除双鲁棒损失（DRL）后 Non-name H@1 从 58.2 骤降至 31.6，移除鲁棒融合（DRF）后降至 50.4，证明各模块对抵抗噪声至关重要。"
- "可靠性分数分布清晰区分噪声与干净配对（Fig. 3b），验证可靠性估计的有效性。"
- "在五个基准、多种 DNC 比例下，RULE 始终显著优于所有对比方法（例如 ICEWS-WIKI Inherent DNC H@1: Ours 64.2 vs. PMF 52.6）。"
---

# Learning with Dual-level Noisy Correspondence for Multi-modal Entity Alignment

> [!tip] 核心洞察
> 低不确定性不一定保证正确匹配（Theorem 1），因此必须结合共识原则；将主观逻辑与 Dirichlet 分布用于量化证据并控制过拟合；采用边际贡献的贪婪策略自动推断可靠对应，并在测试时利用大模型知识进行深度推理，提升噪声下的鲁棒性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向多模态实体对齐的双层次噪声对应学习 |
| 英文题名 | Learning with Dual-level Noisy Correspondence for Multi-modal Entity Alignment |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=mytIKuRsSE) · [GitHub](https://github.com/XLearning-SCU/2026-ICLR-RULE) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | RULE |
| Dataset | ICEWS-WIKI, ICEWS-YAGO, DBP15K ZH-EN, DBP15K JA-EN |

> [!tip] 效果简介
> - ICEWS-WIKI 上，H@1 为 64.2，对比 52.6 (PMF)，变化 +11.6。
> - ICEWS-YAGO 上，H@1 为 48.8，对比 38.3 (PMF)，变化 +10.5。
> - DBP15K ZH-EN 上，H@1 为 85.6，对比 83.9 (PMF)，变化 +1.7。

## 概要

多模态实体对齐（MMEA）旨在将不同知识图谱中指代同一现实世界对象的实体进行匹配，是多源知识融合的关键步骤。现有方法普遍假设实体与属性之间的关联（实体内部对应）以及跨图谱实体/属性匹配（图谱间对应）完全正确。然而，真实的多模态知识图谱中普遍存在**双层次噪声对应（Dual-level Noisy Correspondence, DNC）**：在实体内部，图像、文本等属性可能与实体错误关联；在图谱间，标注的实体对或属性对可能误配。这种噪声导致属性融合引入误导信息，对比学习被错误信号干扰，严重降低对齐准确率。

针对上述瓶颈，本文提出 **RULE** 方法，核心思路是**同时利用不确定性和共识双重原则评估对应的可靠性**，并据此在训练和推理全链路中抑制噪声。具体而言，RULE 首先基于 Dirichlet 证据理论量化跨图谱对应的不确定性，并结合多属性边际贡献的共识信号，将配对划分为高不确定性、低共识和干净三类；在训练中，排除高不确定性对、软化低共识对的目标，并采用加权融合压低不可靠属性的影响；在推理阶段，引入多模态大模型（MLLM）进行链式思维推理，挖掘跨图属性间的隐式连接，进一步提升鲁棒性。

实验在五个主流 MMEA 基准上进行，与七种 SOTA 方法对比。在存在固有 DNC 的 ICEWS-WIKI 上，RULE 的 H@1 达到 64.2，比最优基线 PMF 高出 11.6 个百分点；在 ICEWS-YAGO 上领先 10.5 个百分点；在 DBP15K 的三个跨语言数据集上也一致取得最优。消融实验进一步揭示：移除双鲁棒损失后，Non-name H@1 从 58.2 骤降至 31.6，验证了鲁棒损失是抵抗噪声的核心机制；移除鲁棒融合模块后降至 50.4，证实加权融合能有效抑制不可靠属性；移除测试时推理模块后降至 56.5，表明 MLLM 推理可挖掘隐式连接提升精度。可靠性分数的分布（Figure 3b）清晰分离了噪声与干净配对，验证了可靠性估计的有效性。

RULE 的主要局限在于测试时推理依赖大模型，计算开销较大且可能因领域知识不足而推理失败；此外，方法尚未与主动学习等人机协同范式结合，无法利用额外标注进一步修正噪声。这些方向值得未来探索。

多模态知识图谱（MMKG）将结构化的关系三元组与图像、文本等多模态属性结合，为实体对齐（Entity Alignment, EA）提供了更丰富的匹配信号。然而，现有 MMEA 方法普遍基于一个强假设：实体与其属性之间的关联（intra-entity correspondence）以及跨图谱的实体/属性匹配（inter-graph correspondence）是完全正确的。这一假设在实际场景中难以成立。

**双层次噪声对应（Dual-level Noisy Correspondence, DNC）** 是 MMEA 面临的核心瓶颈。如图 Figure 1(a) 所示，DNC 在两个层次上同时存在：
- **实体内部层次**：实体与属性之间存在错误关联，例如某实体的图像属性被错误地关联到另一实体的名称上；
- **跨图谱层次**：跨图谱的实体-实体对或属性-属性对存在错误匹配，导致对比学习中的正负样本信号被污染。

这两种噪声相互耦合，产生双重危害：一方面，不可靠的属性在融合阶段被错误整合，导致实体表示失真；另一方面，错误的跨图对应在对比学习中被当作正样本，误导模型优化方向。Figure 1(b) 的观测表明，常规的自适应融合（AF）和简单拼接（Concat）在噪声下性能显著退化，而现有方法在跨图对齐时同样遭受严重冲击。

真实数据集中 DNC 的普遍性远超预期。对 ICEWS-WIKI 和 ICEWS-YAGO 基准的分布分析（Figure 6）显示，即使经过人工标注，仍有超过 50% 的实体对存在 DNC 问题，其中实体-属性噪声和属性-属性噪声合计占比超过 40%。这意味着噪声并非边缘情况，而是系统性问题。

现有方法的缺陷可归结为三个层面：
1. **缺乏噪声感知的融合机制**：属性融合时对所有属性一视同仁，无法区分可靠与不可靠的属性关联；
2. **缺乏鲁棒的跨图对齐策略**：对比损失函数对噪声对应高度敏感，容易过拟合到错误的正样本；
3. **测试时推理能力不足**：仅依赖训练阶段学到的相似度度量，无法利用大模型的先验知识挖掘跨图谱属性间的隐式连接。Figure 1(c) 展示了一个典型案例：看似相似的属性对（如足球运动员“Cristiano Ronaldo”与其所属国家）之间的隐式连接常被忽略，导致等价实体被错误排除。

**本文动机**：针对上述缺口，提出一种同时覆盖训练阶段和推理阶段的双层次鲁棒学习方法，通过不确定性-共识双重原则估计对应可靠性，在属性融合和跨图对齐中抑制噪声影响，并在测试时借助多模态大模型进行链式思维推理，实现全链路抗噪。

## 核心方法与创新机理

RULE 针对多模态实体对齐（MMEA）中普遍存在却长期被忽视的**双层次噪声对应（Dual-level Noisy Correspondence, DNC）**问题，提出了从训练到推理的全链路鲁棒框架。其核心创新可归纳为三个相互协同的机制。

### 1. 不确定性与共识双重可靠性估计

现有方法通常仅依赖相似度得分或置信度来评估跨图对应的质量，但 RULE 从理论上揭示了单一原则的根本缺陷：**定理 1** 证明，低不确定性并不保证最高信念质量落在标注对应上，因此仅凭不确定性无法可靠区分噪声与干净配对。RULE 将主观逻辑（Subjective Logic）与 Dirichlet 分布结合，同时引入共识原则作为互补信号，形成双重可靠性估计：

$$w_i = (1 - u_i) \gamma + c_i (1 - \gamma)$$

其中 $u_i$ 为基于证据的不确定性，$c_i$ 度量相似度向量与标注对应之间的一致性，$\gamma$ 平衡二者贡献。这一设计使 RULE 能够将跨图对自适应地划分为三类：高不确定性子集 $\mathcal{S}_U$、低共识子集 $\mathcal{S}_I$ 和干净子集 $\mathcal{S}_C$，为后续差异化处理奠定基础。实验验证了该划分的有效性：干净配对的可靠性分数集中于右侧高值区，噪声配对集中于左侧低值区（Figure 3b）。

### 2. 双鲁棒训练：损失函数与属性融合的协同抗噪

RULE 针对不同可靠性子集设计了差异化的训练策略，形成**双鲁棒损失（Dually Robust Loss, DRL）**与**双鲁棒融合（Dually Robust Fusion, DRF）**的协同机制：

- **DRL** 将高不确定性配对 $\mathcal{S}_U$ 直接排除出损失计算，防止模型拟合噪声；对低共识配对 $\mathcal{S}_I$ 软化训练目标，降低其优化权重；同时引入 KL 正则化项抑制负对证据，避免过拟合：

$$\mathcal{L}_{DR}(\alpha_i, \hat{y}_i) = \mathbb{I}(i \notin S_U) \int \|\hat{y}_i - p_i\|_2^2 D(p_i \mid \alpha_i) dp_i$$

- **DRF** 利用跨图对应的可靠性权重对实体内部的多模态属性进行加权融合，压低不可靠属性的影响：

$$z_i = \bigoplus_{m \in M} (w_i^m \cdot z_i^m)$$

消融实验（Table 3）提供了决定性证据：在 ICEWS-WIKI 50% DNC 设置下，移除 DRL 导致 Non-name H@1 从 58.2 骤降至 31.6，移除 DRF 降至 50.4，证明两个模块各自对抵抗噪声具有不可替代的作用。

### 3. 测试时链式思维推理（TTR）

与仅关注训练阶段鲁棒性的方法不同，RULE 在推理阶段引入多模态大模型（MLLM，如 Qwen2.5-VL）进行链式思维推理，挖掘跨图属性间的隐式连接。当表面相似度无法区分等价实体时（例如“Cristiano Ronaldo”与其国籍之间的隐式关联常被忽略），TTR 通过 CoT 推理修正属性级相似度得分：

$$\hat{\mathbf{s}}_i^m = \mathrm{Softmax}\left( \bigoplus_{j \in \mathcal{T}_i^m} \mathrm{CoT}[x_i^m, \tilde{x}_j^m, \mathbf{s}_i^m] \right)$$

移除 TTR 使 H@1 降至 56.5（Table 3），验证了测试时推理对挖掘隐式连接、提升对齐精度的关键作用。这一训练-推理联合鲁棒的设计，使 RULE 在五个基准、多种 DNC 比例下始终显著优于 PMF 等 SOTA 方法（如 ICEWS-WIKI Inherent DNC H@1: 64.2 vs. 52.6）。

RULE 的整体流水线围绕“双层次噪声对应（DNC）”这一核心瓶颈设计，涵盖训练阶段的可靠性感知学习与推理阶段的跨图属性推理，形成从特征提取到对齐决策的全链路抗噪机制。图 2 给出了方法的总览。

**输入与特征投影。** 给定两个多模态知识图谱，RULE 首先利用属性特定编码器（如预训练 CLIP）将每个实体的结构化、图像、文本等多模态属性分别映射到共享隐空间，得到属性级表示 $z_i^m$，并计算跨图属性间的相似度矩阵。这些相似度是后续可靠性估计与鲁棒学习的输入基础。

**可靠性估计与对应划分（核心控制节点）。** 方法的核心控制逻辑在于同时利用**不确定性**与**共识**双重原则估计每对跨图对应（实体-实体、属性-属性）的可靠性 $w_i = (1 - u_i)\gamma + c_i(1 - \gamma)$。其中不确定性 $u_i$ 基于 Dirichlet 分布从证据强度中导出，共识 $c_i$ 度量相似度向量与标注对应的一致性。定理 1 证明低不确定性不保证高信念落在标注对应上，因此必须结合共识原则才能有效区分噪声与干净配对。基于可靠性估计，跨图对被划分为三个子集：高不确定性对 $S_U$、低共识对 $S_I$ 和干净对 $S_C$，为后续差异化处理提供依据。

**双层次鲁棒训练。** 训练阶段由两个互补模块构成：
- **双鲁棒损失（DRL）**：针对不同可靠性子集设计定制化损失——直接排除 $S_U$ 中的高噪声对，对 $S_I$ 中的低共识对软化优化目标，同时通过 KL 正则化抑制负对证据，防止模型过拟合噪声对应。
- **双鲁棒融合（DRF）**：利用属性-属性对应的可靠性权重 $w_i^m$ 对多模态属性进行加权拼接 $z_i = \bigoplus_{m \in M} (w_i^m \cdot z_i^m)$，压低不可靠属性在实体表示中的贡献，从源头阻断噪声向融合表示的传播。

**测试时推理（TTR）。** 推理阶段引入多模态大模型（默认 Qwen2.5-VL-72B-Instruct）进行链式思维推理，挖掘跨图属性间的隐式连接（如通过“Cristiano Ronaldo”推断其国籍与俱乐部等关联），输出修正后的属性级相似度 $\hat{\mathbf{s}}_i^m$。最终联合原始相似度与修正相似度得到 $\mathbf{s}_i^{joint} = \mathbf{s}_i + \hat{\mathbf{s}}_i$，取 arg max 确定等价实体。

**模块间关系。** 可靠性估计是全局控制节点，其输出同时驱动 DRL 的损失定制、DRF 的权重分配以及 TTR 的候选筛选。DRL 与 DRF 分别在损失空间和表示空间抵抗噪声，形成互补；TTR 则在推理阶段利用大模型知识弥补训练阶段难以捕获的深层语义关联。消融实验表明，移除 DRL 使 Non-name H@1 从 58.2 骤降至 31.6，移除 DRF 降至 50.4，移除 TTR 降至 56.5，验证了各模块对整体鲁棒性的关键贡献。

RULE 围绕双层次噪声对应（DNC）问题构建了三个核心模块：**可靠性估计与对划分**、**双鲁棒学习与融合**、以及**测试时对应推理**。各模块通过一组关键公式耦合，形成从训练到推理的全链路抗噪机制。

### 可靠性估计与对划分

该模块是 RULE 的入口，其核心思想是同时利用**不确定性**和**共识**双重原则评估跨图实体-实体对应的可靠性。定理 1 指出，低不确定性并不保证高信念落在标注对应上，因此必须引入共识原则作为补充。

可靠性权重 $w_i$ 由不确定性与共识的加权组合给出：

$$w_i = (1 - u_i) \gamma + c_i (1 - \gamma)$$

其中 $u_i$ 为不确定性，$c_i$ 为共识，$\gamma$ 为平衡超参数。不确定性 $u_i$ 基于 Dirichlet 分布建模：先将实体对相似度 $s_{ij}$ 通过温度 $\tau$ 转换为证据 $e_{ij} = \exp(\tanh(s_{ij} / \tau))$，再定义 Dirichlet 强度 $Q_i = \sum_j e_{ij}$，则不确定性为 $u_i = \tilde{N} / Q_i$，信念质量为 $b_{ij} = e_{ij} / Q_i$。共识 $c_i$ 度量相似度向量 $\mathbf{s}_i$ 与标注对应 $\mathbf{y}_i$ 的匹配程度：$c_i = \max(0, \mathbf{s}_i \cdot \mathbf{y}_i)$。

在此基础上，依据自适应阈值 $\beta_u$ 和 $\beta_c$ 将跨图对划分为三个子集：高不确定性集 $S_U$、低共识集 $S_I$ 和干净集 $S_C$。

### 双鲁棒学习（DRL）

DRL 为不同可靠性子集设计定制化损失，核心公式为：

$$\mathcal{L}_{DR}(\alpha_i, \hat{y}_i) = \mathbb{I}(i \notin S_U) \int \|\hat{y}_i - p_i\|_2^2 \, D(p_i \mid \alpha_i) \, dp_i$$

该损失直接排除高不确定性对 $S_U$，避免噪声梯度污染训练；对低共识对 $S_I$ 采用软化目标，利用 Dirichlet 先验 $D(p_i \mid \alpha_i)$ 防止过拟合。同时引入 KL 正则化项 $\mathcal{L}_{Reg}$ 惩罚未关联跨图对的证据，总体目标为 $\mathcal{L} = \mathcal{L}_{DR} + \lambda \mathcal{L}_{Reg}$。

### 双鲁棒融合（DRF）

DRF 利用属性级可靠性权重 $w_i^m$ 对多模态属性进行加权融合：

$$z_i = \bigoplus_{m \in M} (w_i^m \cdot z_i^m)$$

其中 $z_i^m$ 为属性 $m$ 的特征表示，$\oplus$ 表示拼接操作。通过压低不可靠属性的权重，DRF 从源头抑制了实体内部噪声对应（intra-entity NC）对融合表示的污染。

### 测试时对应推理（TTR）

TTR 在推理阶段利用多模态大模型（如 Qwen2.5-VL）进行链式思维推理，挖掘跨图属性间的隐式连接，修正属性级相似度：

$$\hat{\mathbf{s}}_i^m = \mathrm{Softmax}\left( \bigoplus_{j \in \mathcal{T}_i^m} \mathrm{CoT}[x_i^m, \tilde{x}_j^m, \mathbf{s}_i^m] \right)$$

最终将原始相似度 $\mathbf{s}_i$ 与修正相似度 $\hat{\mathbf{s}}_i$ 求和得到联合相似度 $\mathbf{s}_i^{joint} = \mathbf{s}_i + \hat{\mathbf{s}}_i$，用于等价实体识别。

### 模块间的因果链路

可靠性估计的输出（$w_i$ 及子集划分）同时驱动 DRL 的损失定制和 DRF 的加权融合；DRF 产生的融合表示又作为 DRL 的输入；TTR 则在测试时独立于训练流程，通过大模型知识补偿训练阶段未能捕获的隐式对应。消融实验（Table 3）验证了这一链路：移除 DRL 使 ICEWS-WIKI Non-name H@1 从 58.2 骤降至 31.6，移除 DRF 降至 50.4，移除 TTR 降至 56.5，证明各模块对抵抗 DNC 均不可或缺。

## 实验与关键发现

### 主要结果

RULE 在五个多模态实体对齐基准上与七种现有方法（EVA、MCLEA、XGEA、MEAformer、UMAEA、PMF、HHEA）进行了系统对比，覆盖固有噪声（Inherent DNC）、20% DNC 和 50% DNC 三种噪声比例。实验设置分为 Non-name（排除名称属性）和 All-attributes（包含全部属性）两种评估模式。

在 Non-name 设置下（Table 1），RULE 在所有噪声水平上均显著超越最优基线。以 ICEWS-WIKI 基准为例，固有噪声下 RULE 的 H@1 达到 64.2，相较最强基线 PMF 的 52.6 提升 **+11.6**；在 50% 极端噪声下，RULE 仍保持 H@1 58.2，而 PMF 降至 47.8。ICEWS-YAGO 上呈现类似趋势，固有噪声下 RULE 领先 PMF **+10.5**（48.8 vs. 38.3）。在 DBP15K 系列基准（ZH-EN、JA-EN、FR-EN）上，由于跨语言场景下名称属性已被排除，性能增益相对收敛，但仍稳定领先 PMF 0.7–1.7 个点（如 ZH-EN：85.6 vs. 83.9）。这一结果表明，RULE 在噪声严重的多模态知识图谱场景中具备显著优势，而在噪声相对有限的干净数据上亦不损失竞争力。

在 All-attributes 设置下（Table 2），RULE 的平均 H@1 在固有噪声、20% DNC、50% DNC 下分别达到 98.8、98.5 和 84.3，全面超越所有对比方法。值得注意的是，RULE 的性能退化速度明显慢于基线方法（Figure 3a），在 0.0–0.7 的宽噪声比例范围内始终保持较高 H@1，验证了双层次鲁棒机制对噪声梯度变化的适应能力。

### 消融实验

Table 3 的消融实验揭示了各模块对整体性能的贡献差异。在 ICEWS-WIKI Non-name 50% DNC 条件下，完整 RULE 的 H@1 为 58.2：

- **移除双鲁棒损失（w/o DRL）**：H@1 骤降至 **31.6**，降幅高达 26.6 点。该模块负责排除高不确定性跨图对并为低共识对软化目标，是抵抗噪声的核心机制。
- **移除鲁棒融合（w/o DRF）**：H@1 降至 **50.4**，损失 7.8 点。这表明基于可靠性权重的多模态属性加权融合能有效抑制不可靠属性对实体表示的污染。
- **移除测试时推理（w/o TTR）**：H@1 降至 **56.5**，损失 1.7 点。TTR 模块通过多模态大模型挖掘跨图属性间的隐式连接，虽贡献相对较小但在推理阶段提供了独立的纠错通道。
- **仅使用不确定性或仅使用共识原则**：二者单独使用时性能均低于完整方案（Table 3 及 Table 15 的 γ 分析），证明不确定性与共识的双重原则具有互补性——低不确定性不能保证高信念落在正确对应上（Theorem 1），必须结合共识进行联合判断。

进一步对损失项与划分策略进行细粒度消融（Table 7），KL 正则化项和子集划分策略各自对最终性能产生正向贡献，移除任一部分均导致性能下降，验证了训练策略设计的合理性。

### 可靠性估计的有效性

Figure 3b 展示了可靠性分数的分布：干净配对集中在右侧高可靠性区域，噪声配对集中在左侧低可靠性区域，二者分离清晰。Figure 4 进一步对名称属性上的不确定性与共识进行了定量分析，表明双重原则能够有效区分可靠与不可靠的跨图对应。Figure 5 可视化展示了干净实体对与注入实体-属性噪声后的可靠性变化：在图像和名称属性上，噪声注入后对应的可靠性权重显著降低，验证了 DRF 模块对不可靠属性的抑制能力。

### 失败模式与局限性

尽管 RULE 在整体上表现鲁棒，但仍存在以下失败模式和局限：

1. **测试时推理依赖 MLLM 的领域知识**：当多模态大模型缺乏特定领域知识或仅依赖表面视觉线索时，链式思维推理可能产生错误判断。Figure 13 展示了测试时推理的典型失败案例，提示在高度专业领域（如医学、法律知识图谱）中需谨慎使用。
2. **计算开销较大**：使用 Qwen2.5-VL-72B-Instruct 作为推理模型需要 8 GPU，推理时间较长（Table 13 的复杂度分析），可能限制资源受限场景下的部署。
3. **属性完整性依赖**：虽然 RULE 在缺失部分属性时仍能工作，但性能增益依赖于可用多模态属性的完整性。当关键模态（如图像）大面积缺失时，可靠性估计和加权融合的有效性会下降。
4. **未结合主动学习**：当前方法未与主动学习或人在回路策略结合，无法利用额外人工标注进一步修正残留噪声对应，在极端噪声场景下可能存在性能天花板。

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_mytIKuRsSE/figures/039_Figure_13.jpg]]
*Figure 13: Failure cases in test-time reasoning*

### 跨噪声类型与泛化性

在单一噪声类型（仅实体-实体噪声或仅实体-属性噪声）的 NC 设置下（Table 5 和 Table 6），RULE 仍全面优于对比方法，证明其双层次鲁棒机制对不同类型的噪声对应均有效。此外，在多种视觉骨干（CLIP、SigLIP、BLIP）和不同 MLLM 架构（Table 12）上的实验表明，RULE 的性能对底层编码器和推理模型的选择具有一定鲁棒性，具备良好的泛化潜力。


![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_mytIKuRsSE/figures/012_Figure.jpg]]
*Figure: ID:7125 ID:26134*

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_mytIKuRsSE/figures/013_Figure.jpg]]
*Figure: ID:7125 Name:African Development Fund*

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_mytIKuRsSE/figures/016_Figure_7.jpg]]
*Figure 7: The parameter analysis of the trade-off parameter λ in Eq. 9, the temperature τ in Eq. 2, and the threshold β in Eq. 8*

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_mytIKuRsSE/figures/020_Figure_8.jpg]]
*Figure 8: Performance with various DNC ratios on the $\mathrm { D B P 1 5 K _ { Z H - E N } }$ dataset*

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_mytIKuRsSE/figures/022_Figure_9.jpg]]
*Figure 9: Quantitative analysis of the uncertainty and consensus on the integrated entity*

## 定位与知识库关联

### 问题定位：双层次噪声对应（DNC）

RULE 的核心贡献在于首次系统性地定义并解决多模态实体对齐（MMEA）中的**双层次噪声对应**（Dual-level Noisy Correspondence, DNC）问题。现有 MMEA 方法——包括 **EVA**、**MCLEA**、**XGEA**、**MEAformer**、**UMAEA**、**PMF** 和 **HHEA**——均假设实体-属性对应（intra-entity）和跨图实体/属性对应（inter-graph）完全正确。然而，实际多模态知识图谱中普遍存在两类噪声：实体内部错误关联的属性（如配错图片），以及跨图实体或属性之间的错误匹配标注。这两种噪声相互耦合：错误的属性融合误导跨图对齐学习，而错误的跨图监督信号又放大了属性融合的偏差，形成恶性循环。

Figure 1(a) 直观展示了 DNC 的双层次结构，Figure 1(b) 则通过实验揭示：传统自适应融合（AF）和简单拼接（Concat）在噪声下性能显著退化，而 RULE 通过可靠性估计实现了鲁棒融合；同时，现有对比方法在跨图噪声下对齐精度大幅下降，RULE 则通过抑制 intra-entity 噪声的负面影响实现了性能提升。

### 方法谱系中的位置

RULE 处于**鲁棒多模态对齐**与**不确定性感知学习**的交叉点。其技术路线可沿以下维度定位：

**1. 噪声鲁棒对齐方法。** 现有 MMEA 方法（如 PMF、MCLEA）多依赖对比学习或最优传输，但缺乏对标注噪声的显式建模。RULE 引入主观逻辑（Subjective Logic）和 Dirichlet 分布来量化证据与不确定性，这与 EDL（Evidential Deep Learning）系列工作共享思想基础，但将不确定性估计从单模态分类拓展到了跨图对应可靠性评估。

**2. 多模态融合策略。** 传统方法采用等权拼接或注意力融合，RULE 的 Dually Robust Fusion（DRF）通过跨图可靠性权重指导属性融合，形成“跨图信号反馈修正实体内部表示”的双向机制，这在现有 MMEA 工作中未见先例。

**3. 测试时推理增强。** RULE 的 Test-time Correspondence Reasoning（TTR）模块利用多模态大模型（Qwen2.5-VL）进行链式思维推理，挖掘跨图属性间的隐式连接。这一设计将训练时鲁棒性与推理时知识增强解耦，与最近利用 LLM/MLLM 进行知识图谱推理的工作（如 KG-LLM 系列）形成互补，但 RULE 聚焦于细粒度的属性级对应修正，而非整体三元组推理。

### 核心机制与因果通路

RULE 通过三个耦合模块实现全链路抗噪：

- **可靠性估计与对应对划分**：基于不确定性和共识的双重原则，将跨图对划分为高不确定性（$S_U$）、低共识（$S_I$）和干净（$S_C$）三个子集。**Theorem 1** 证明低不确定性不保证高信念落在标注对应上，因此必须结合共识原则。
- **Dually Robust Learning（DRL）**：排除 $S_U$ 对，为 $S_I$ 对软化目标，并结合 KL 正则化抑制负对证据，防止过拟合噪声标签。
- **Dually Robust Fusion（DRF）**：根据可靠性权重 $w_i^m$ 对多模态属性加权融合，压低不可靠属性的影响。
- **Test-time Reasoning（TTR）**：利用 MLLM 进行 CoT 推理，修正属性级相似度，挖掘训练时难以捕获的隐式连接（如“C罗”与“葡萄牙”的国籍关联）。

### 适用边界与局限

RULE 的有效性依赖于以下条件：

1. **多模态属性的可用性**：方法通过属性间边际贡献推断可靠对应，当实体缺失关键模态时，性能增益会衰减（尽管方法在部分缺失下仍可工作）。
2. **MLLM 的知识覆盖**：TTR 模块依赖大模型的领域知识。Figure 13 展示了推理失败案例——当 MLLM 缺乏特定领域知识或仅依赖表面视觉线索（如相似背景色）时，可能产生错误推理。此外，72B 模型的推理需要 8 GPU，计算开销限制了资源受限场景的应用。
3. **噪声类型的边界**：当前框架针对实体-属性级和跨图对应级噪声设计，尚未覆盖关系三元组噪声或更复杂的跨语言场景。

### 开放问题

1. **噪声类型拓展**：能否将可靠性估计框架推广至关系三元组噪声、时序动态噪声以及跨语言对齐场景？
2. **推理效率优化**：能否通过知识蒸馏或更轻量的视觉-语言模型（如 BLIP-2 的小型变体）降低 TTR 的计算成本，使其适用于实时或边缘场景？
3. **人机协同**：RULE 的可靠性估计天然适合与主动学习结合——高不确定性对可优先交由人工标注，在极少干预下持续提升鲁棒性。
4. **跨任务迁移**：双层次噪声对应的评估范式是否可作为通用模块，迁移至其他多模态对齐任务（如视觉问答中的图文对应、跨模态检索中的匹配噪声）？

### 证据强度说明

- **消融实验**（Table 3）提供了强因果证据：移除 DRL 后 ICEWS-WIKI Non-name H@1 从 58.2 骤降至 31.6，移除 DRF 后降至 50.4，证明各模块对抵抗噪声的关键作用。
- **可靠性分布**（Figure 3b）清晰区分噪声与干净配对，验证了可靠性估计的有效性。
- **跨基准一致性**：在五个基准、多种 DNC 比例下，RULE 始终显著优于所有对比方法（如 ICEWS-WIKI Inherent DNC H@1: 64.2 vs. PMF 52.6），证据链完整。
- **泛化性验证**：在多种视觉骨干（CLIP, SigLIP, BLIP）和 MLLM 架构上验证，降低了骨干选择偏差的担忧。

## 原文 PDF

![[paperPDFs/ICLR_2026/Learning_with_Dual_level_Noisy_Correspondence_for_Multi_modal_Entity_Alignment.pdf]]
