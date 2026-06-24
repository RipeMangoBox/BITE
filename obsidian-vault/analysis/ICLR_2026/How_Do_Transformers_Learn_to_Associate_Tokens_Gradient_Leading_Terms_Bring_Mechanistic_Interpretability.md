---
title: "How Do Transformers Learn to Associate Tokens: Gradient Leading Terms Bring Mechanistic Interpretability"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/How_Do_Transformers_Learn_to_Associate_Tokens_Gradient_Leading_Terms_Bring_Mechanistic_Interpretability.pdf
openreview_forum_id: A4Us8jxVGq
aliases:
- GLTC
- HDTLATGLTBMI
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "训练早期的梯度主导项（Gradient Leading Terms），其闭式解揭示了权重与语料统计的直接关联。"
primary_logic: "在训练初期，Transformer的权重矩阵（输出、值、查询-键、位置编码）可以近似为三个基函数（bigram映射、可互换性映射、上下文映射）的简单组合，这些基函数直接来源于训练语料的统计信息，揭示了模型如何逐步构建语义关联。"
claims:
- "Transformer的权重矩阵可在训练早期表示为bigram映射、可互换性映射和上下文映射三个基函数的组合。"
- "理论预测的权重与实际学习到的权重在TinyStories上高度一致（最小余弦相似度 > 0.998，Table 1）。"
- "即使训练100轮后，所有参数矩阵的余弦相似度仍保持在0.7以上，表明理论超越早期阶段仍具参考价值。"
- "Pythia-1.4B的注意力权重和嵌入的协方差矩阵在训练早期与理论主导项特征高度匹配（Figure 6）。"
---

# How Do Transformers Learn to Associate Tokens: Gradient Leading Terms Bring Mechanistic Interpretability

> [!tip] 核心洞察
> 在训练初期，Transformer的权重矩阵（输出、值、查询-键、位置编码）可以近似为三个基函数（bigram映射、可互换性映射、上下文映射）的简单组合，这些基函数直接来源于训练语料的统计信息，揭示了模型如何逐步构建语义关联。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Transformer如何学习符号关联：梯度主导项带来机制可解释性 |
| 英文题名 | How Do Transformers Learn to Associate Tokens: Gradient Leading Terms Bring Mechanistic Interpretability |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=A4Us8jxVGq) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | 梯度主导项表征理论（Gradient Leading Term Characterization） |
| Dataset | TinyStories, OpenWebText (Pythia-1.4B) |

> [!tip] 效果简介
> - TinyStories 上，余弦相似度 (理论主导项 vs 实际注意力权重) 为 理论主导项 Q̄，对比 实际学习权重 W^{(l)}，变化 相似度 0.999496。
> - TinyStories 上，余弦相似度 (理论主导项 vs 实际值权重) 为 理论主导项 Φ̄^⊤ B̄^⊤，对比 实际学习权重 V^{(l)}，变化 相似度 0.999169。
> - TinyStories 上，余弦相似度 (理论主导项 vs 实际输出权重) 为 理论主导项 B̄，对比 实际学习权重 W_O，变化 相似度 0.998486。

## 概述

**核心问题**：Transformer 语言模型在自然语言数据上通过梯度下降训练时，究竟如何逐步建立起 token 之间的语义关联？尽管这类模型已取得显著成功，其内部权重在训练早期的形成机制一直缺乏可解释的数学刻画。

**核心洞察**：本文提出了一种**梯度主导项表征理论**，核心发现是：在训练初期，Transformer 中 attention-only 架构的各权重矩阵（输出矩阵、值矩阵、查询-键矩阵、位置编码矩阵）可以近似表示为**三个基函数**的简单组合——**bigram 映射**（捕捉相邻 token 的依赖关系）、**可互换性映射**（反映 token 在功能上的相似性）和**上下文映射**（编码长程的前缀-后缀共现关系）。这些基函数直接来源于训练语料的统计信息，为模型的权重赋予了清晰的语义解释。

**方法定位**：本文的技术路径不同于事后解释（post-hoc interpretation）或探测方法，而是从训练动力学的角度出发，对梯度进行展开并提取主导项，从而在训练早期（$O(1/\eta)$ 步内）获得权重的闭式近似解。这一框架将模型权重的涌现直接与语料统计量（如 bigram 频率、上下文共现概率）挂钩，建立了从数据到参数的因果链条。

**关键证据**：
- 在 TinyStories 数据集上训练的 3 层 attention-only 模型中，理论预测的权重与实际学习到的权重之间的余弦相似度极高：注意力权重达 0.9995，值权重达 0.9992，输出权重达 0.9985（Table 1）。
- 即使训练 100 轮后（loss 已从 8.00 降至 5.35），所有参数矩阵的余弦相似度仍保持在 0.7 以上（Figure 4），表明理论在早期阶段之后仍具有参考价值。
- 在更大规模的 Pythia-1.4B 模型上，注意力权重和嵌入的协方差矩阵在训练早期与理论主导项特征高度匹配（Figure 6），验证了理论在真实 LLM 训练初期的适用性。
- 消融实验表明，移除输出矩阵主导项导致 loss 从 5.349 急剧上升至 8.287，而逐层移除注意力主导项对 loss 影响甚微（5.349 → 5.350~5.361），揭示了不同模块主导项对预测贡献的差异（Table 3）。

**方法谱系与知识库定位**：本文属于**机械可解释性（Mechanistic Interpretability）** 领域，但区别于通过逆向工程（reverse engineering）分析已训练模型的工作，它从训练动态的角度提供了权重形成的**前向推导**。与基于线性探针或注意力可视化的事后方法不同，本文的梯度主导项理论直接揭示了权重与语料统计之间的函数关系，为理解 Transformer 早期学习提供了可验证的定量预测。这一框架在理论上受限于 attention-only 架构和训练初期，但实验表明其核心结论在包含 MLP 的 Pythia 模型中仍有部分成立，为该方向的推广留下了开放空间。

**局限与展望**：理论仅保证训练早期的权重演化，无法直接解释收敛后的复杂行为；分析假设纯自注意力架构，未完全建模 MLP 在特征学习中的作用；实验验证限于较小规模模型，尚未在更大规模的最新 LLM 上系统检验。未来工作可探索训练后期主导项特征的演变规律、将分析推广至完整 Transformer 架构，以及利用基函数分解提出关于模型概念涌现的更广泛假设。

## 背景与动机

Transformer 架构已成为现代大语言模型的基石，其在自然语言数据上通过下一词预测（next-token prediction）训练后展现出强大的语义理解与生成能力。然而，一个根本性的问题长期悬而未决：**Transformer 究竟如何通过梯度下降从语料中学习到词元之间的语义关联？** 换言之，模型权重中编码了什么样的语料统计结构，这些结构又是如何在训练过程中逐步涌现的？

现有的机制可解释性研究主要聚焦于已训练好的模型，通过探测单个神经元、注意力头或电路来解释模型行为。这类事后分析方法虽然揭示了诸多有趣现象，但**无法回答“这些特征从何而来”的问题**——它们缺少对训练动力学（training dynamics）的刻画，因而难以建立权重与训练数据之间的因果联系。另一方面，关于神经网络训练动力学的理论工作大多局限于简化设置（如线性网络、无限宽度极限或合成数据），难以直接推广到在真实文本语料上训练的实际 Transformer。

因此，该领域的核心瓶颈在于：**缺乏一个能够在真实自然语言数据上，将 Transformer 的训练过程与可解释的语料统计量直接关联的理论框架**。这一缺口使得我们无法系统性地理解语义关联特征的形成机制，也难以预测模型在训练早期的行为演化。

本文正是在这一背景下展开。其核心动机是：**通过分析训练早期梯度的主导项（Gradient Leading Terms），推导出权重矩阵的闭式解，从而揭示 Transformer 学习语义关联的机制性原理**。这一思路的关键洞见在于——在训练初期，权重的演化主要由梯度展开中的低阶项支配，而这些低阶项恰好可以表示为训练语料中若干基础统计量（如 bigram 频率、token 可互换性、上下文共现）的简单组合。通过刻画这些“基函数”如何组合成注意力模块的各个权重矩阵，本文旨在为 Transformer 的早期训练动力学提供一个可解释、可验证的理论表征。

## 核心创新

本工作的核心创新在于提出了一种**梯度主导项表征理论**（Gradient Leading Term Characterization），首次为在自然语言语料上训练的自注意力Transformer的权重矩阵提供了显式的闭式表达式。这一理论将Transformer在训练早期的学习过程分解为三个可解释的基函数（bigram映射、可互换性映射、上下文映射）的简单组合，从而揭示了语义关联特征从语料统计中涌现的机制性过程。

### 关键突破：从梯度主导项到权重闭式解

传统上，Transformer的训练动态分析面临高度非线性的挑战。本工作的技术突破在于：在训练初期（$O(1/\eta)$步内），每个权重矩阵的梯度展开式中的主导项可以被解析地表达为训练语料统计量的函数。通过在全批量梯度下降（学习率 $\eta$）和零初始化或高斯初始化条件下展开梯度，作者发现：

- **输出矩阵** $W_O$ 的主导项直接对应于bigram映射 $\bar{B}$（乘以缩放因子 $s\eta$），即 $W_O \approx s\eta \bar{B}$；
- **值矩阵** $V^{(l)}$ 的主导项由上下文映射 $\bar{\Phi}$ 和bigram映射 $\bar{B}$ 的组合构成：$V^{(l)} \approx \binom{s}{2} \eta^2 \bar{\Phi}^\top \bar{B}^\top$；
- **查询-键矩阵** $W^{(l)}$ 的主导项基于可互换性映射和上下文映射的复合特征 $\bar{Q}$；
- **相对位置编码** $P^{(l)}$ 的主导项将关联映射到位置差 $\Delta$，而非词汇差。

这三个基函数分别捕获了不同层次的语料统计信息：
- **Bigram映射** $\bar{B}$：捕获token间的直接相邻依赖关系（下一个token的预测概率）；
- **可互换性映射** $\Sigma_{\bar{B}}$：基于先前token分布的相似性，度量token在功能上的可互换性；
- **上下文映射** $\bar{\Phi}$：编码更长范围的前缀-后缀共现关系。

### 与现有工作的本质差异

与以往从模型行为或表示空间出发的解释性工作不同，本工作从**训练动态的梯度结构**入手，建立了权重矩阵与语料统计之间的直接数学联系。这一方法不依赖于对已训练模型的逆向工程，而是从学习的源头——梯度下降的第一步——推导出模型所学特征的形式。这使得理论预测具有**先验可验证性**：无需训练模型，仅需统计训练语料的bigram、可互换性和上下文分布，即可预测模型在训练早期的权重结构。

### 理论的核心洞察：关联特征的层级组合

更深入的洞察在于，这些基函数并非孤立地存储在不同的权重矩阵中，而是通过自注意力的计算图**层级式地组合**。单层模型的整体计算可展开为：

$$(\mathcal{S}(\mathrm{Mask}(\mathbf{X}\bar{\mathbf{Q}}\mathbf{X}^\top + \mathrm{DM}(\pmb{\Delta})))\mathbf{X}\bar{\pmb{\Phi}}^\top\bar{\mathbf{B}}^\top + \mathbf{X})\bar{\mathbf{B}}$$

其中，自注意力模块的输出为：

$$\mathcal{S}(\mathrm{Mask}(\mathbf{X}\bar{\mathbf{Q}}\mathbf{X}^\top + \mathrm{DM}(\pmb{\Delta})))\mathbf{X}\bar{\pmb{\Phi}}^\top\Sigma_{\bar{\mathbf{B}}}$$

这一展开揭示了Transformer如何**逐步构建语义关联**：注意力分布（由 $\bar{Q}$ 和 $\Delta$ 控制）对输入token进行加权，然后将加权结果通过值矩阵（编码了 $\bar{\Phi}$ 和 $\Sigma_{\bar{B}}$）映射到语义更丰富的表示空间，最终通过输出矩阵（编码了 $\bar{B}$）预测下一个token。这种“注意力选择—值映射—输出投影”的三阶段组合，构成了语义关联特征从语料统计中涌现的基本机制。

### 实验验证的强度

理论预测与实际学习权重在TinyStories数据集上的余弦相似度极高：注意力权重0.999496，值权重0.999169，输出权重0.998486（Table 1）。即使训练100轮后，所有参数矩阵的余弦相似度仍保持在0.7以上（Figure 4），表明理论的主导项表征在训练早期具有极强的解释力。消融实验进一步验证了各主导项的功能重要性：移除输出矩阵主导项导致loss从5.349上升至8.287，移除值矩阵主导项使loss升至6.192-6.526，而移除注意力主导项对loss影响甚微（5.350-5.361），揭示了不同模块在初始阶段的功能分工。

值得注意的是，该理论在Pythia-1.4B（基于OpenWebText训练）上也得到了部分验证：注意力权重和嵌入的协方差矩阵在训练早期与理论主导项特征高度匹配（Figure 6），说明理论的核心机制可能在大规模模型中同样成立，尽管MLP层的存在使得完全刻画更具挑战。

## 整体框架

本文提出了一套完整的分析框架，旨在从梯度动力学的角度揭示Transformer在自然语言数据上学习符号关联的机制。该框架的核心流程可概括为：**从训练语料中提取统计基函数 → 推导权重矩阵的梯度主导项闭式解 → 将模型计算重构为基函数的组合 → 通过实验验证理论预测与实际学习权重的一致性**。

### 核心分析路径

**Step 1: 梯度主导项展开。** 研究假设模型采用全批量梯度下降，学习率为常数 $\eta$。在训练初期（约 $O(1/\eta)$ 步内），权重矩阵的演化可由其梯度展开的主导项精确近似。这一近似将复杂的训练动态简化为可直接从语料统计计算的闭式解。

**Step 2: 语料统计基函数构造。** 从训练语料中提取三个核心基函数，它们共同刻画了模型学习到的关联特征：
- **Bigram映射 B̄**：捕获token间的直接邻接概率，反映"下一个token"的依赖关系；
- **可互换性映射 Σ_{B̄}**：基于前驱token分布的相似性，度量token间的功能可替代性；
- **上下文映射 Φ̄**：编码长程的前缀-后缀共现统计，捕获更丰富的语境信息。

**Step 3: 权重矩阵表征。** 理论推导表明，Transformer各权重矩阵在训练早期可表示为上述基函数的简单组合（Theorem 4.1）：
- **输出矩阵 $W_O$**：由bigram映射主导，$W_O \approx s\eta \bar{B}$；
- **值矩阵 $V^{(l)}$**：组合上下文映射与bigram映射，$V^{(l)} \approx \binom{s}{2}\eta^2 \bar{\Phi}^\top \bar{B}^\top$；
- **查询-键矩阵 $W^{(l)}$**：基于可互换性和上下文映射的复合特征，$W^{(l)} \approx (3C(s,4) + 2C(s,3))\eta^4 \bar{Q}$；
- **相对位置编码 $P^{(l)}$**：与 $W^{(l)}$ 结构类似，但将关联映射到位置差而非词汇差。

**Step 4: 模型计算重构。** 将这些权重表征代入Transformer的前向计算，可将整个模型的计算过程重构为基函数的组合。单层attention-only模型的主导项计算为：

$$( \mathcal{S} ( \mathrm{Mask} ( \mathbf{X} \bar{\mathbf{Q}} \mathbf{X}^{\top} + \mathrm{DM} ( \pmb{\Delta} ) ) ) \mathbf{X} \bar{\pmb{\Phi}}^{\top} \bar{\mathbf{B}}^{\top} + \mathbf{X} ) \bar{\mathbf{B}}$$

其中自注意力块的核心贡献为：

$$\mathcal{S} ( \mathrm{Mask} ( \mathbf{X} \bar{\mathbf{Q}} \mathbf{X}^{\top} + \mathrm{DM} ( \pmb{\Delta} ) ) ) \mathbf{X} \bar{\pmb{\Phi}}^{\top} \Sigma_{\bar{\mathbf{B}}}$$

该重构揭示了注意力分布（由 $\bar{Q}$ 和 $\Delta$ 决定）如何对基于 $\bar{\Phi}$ 和 $\Sigma_{\bar{B}}$ 的值表示进行加权，从而逐步细化下一个token的预测。

### 实验验证闭环

框架的实证验证分为三个层次：
1. **直接权重对比**：在TinyStories上训练的3层attention-only模型中，理论主导项与实际学习权重的余弦相似度均超过0.998（Table 1），且即使训练100轮后仍保持在0.7以上（Figure 4）。
2. **消融验证**：逐模块移除主导项后，输出矩阵的移除导致loss从5.349跃升至8.287，值矩阵的移除使loss显著上升至6.192–6.526，而注意力矩阵的移除影响甚微（5.350–5.361），与理论预测的功能重要性一致（Table 3）。
3. **大模型泛化**：在Pythia-1.4B上，注意力权重和嵌入的协方差矩阵在训练早期与理论主导项特征高度匹配（Figure 6），表明框架的核心洞察可部分推广至包含MLP的大规模模型。

### 适用范围与边界

本框架的理论保证严格限定于训练早期（梯度主导项有效的阶段）和纯自注意力架构。随着训练深入，权重会从固定的关联特征逐渐漂移以表示更丰富的知识，且MLP层的存在尚未被完全建模。这些边界条件构成了框架的固有局限，也指明了未来扩展的方向。

## 核心模块与公式推导

### 架构假设与训练设定

本文的分析对象为纯自注意力Transformer（attention-only），保留相对位置编码、因果掩码和残差流，但不包含MLP层。模型的逐层递归关系为：

$$\mathbf{h}^{(l)} = \mathbf{h}^{(l-1)} + \mathcal{S}(\mathrm{Mask}(\mathbf{h}^{(l-1)} \mathbf{W}^{(l)} \mathbf{h}^{(l-1)\top} + \mathrm{DM}(\mathbf{P}^{(l)}))) \mathbf{h}^{(l-1)} \mathbf{V}^{(l)}$$

其中 $\mathbf{h}^{(l)}$ 为第 $l$ 层隐藏状态，$\mathbf{W}^{(l)}$ 为查询-键矩阵，$\mathbf{P}^{(l)}$ 为相对位置编码矩阵，$\mathbf{V}^{(l)}$ 为值矩阵，$\mathcal{S}$ 为softmax函数，$\mathrm{Mask}$ 为因果掩码，$\mathrm{DM}$ 为距离映射函数。最终输出由 $\mathbf{F}_{\Theta}(\mathbf{X}) = \mathbf{h}^{(L)} \mathbf{W}_O$ 给出，$\mathbf{W}_O$ 为输出矩阵。

训练采用全批量梯度下降，学习率 $\eta$ 恒定：

$$\Theta(t) = \Theta(t-1) - \eta \nabla_{\Theta} \mathcal{L}(\Theta)$$

损失函数为标准的下一个token预测交叉熵损失。核心理论成立的时间窗口为 $\tilde{O}(1/\eta)$ 步，即训练早期阶段。

### 梯度主导项的核心洞察

该工作的关键技术创新在于：对每个权重矩阵的梯度进行展开，提取其主导项（gradient leading terms），从而获得权重在训练早期的闭式近似解。这些近似解表明，所有权重矩阵均可表示为三个基函数的组合，而这些基函数直接源自训练语料的统计信息。

### 三个基函数的定义

**Bigram映射 $\bar{\mathbf{B}}$**（Eq. 9）：

$$\bar{B}_{ij} = \mathcal{P}_t(\mathbf{e}_i) \mathcal{P}_t(\mathbf{e}_j | \mathbf{e}_i) - \mathcal{P}_t(\mathbf{e}_i) / |\mathcal{V}|$$

$\bar{B}_{ij}$ 捕获token $\mathbf{e}_i$ 后紧跟token $\mathbf{e}_j$ 的概率关联，其中 $\mathcal{P}_t(\mathbf{e}_i)$ 为token $\mathbf{e}_i$ 的频率，$\mathcal{P}_t(\mathbf{e}_j | \mathbf{e}_i)$ 为条件概率，减去的中心化项消除了均匀分布的影响。该映射是输出矩阵 $\mathbf{W}_O$ 的主导特征。

**可互换性映射 $\Sigma_{\bar{\mathbf{B}}}$**（Eq. 10）：

$$\underbrace{\mathcal{P}_t(\mathbf{e}_i) \mathcal{P}_t(\mathbf{e}_j)}_{\text{频率加权}} \sum_{k=1}^{|\mathcal{V}|} \underbrace{\mathcal{P}_t(\mathbf{e}_k | \mathbf{e}_i) \mathcal{P}_t(\mathbf{e}_k | \mathbf{e}_j)}_{\text{前驱token分布相似度}}$$

该映射度量两个token在功能上的可互换性：若它们的前驱token分布高度相似，则它们在语法或语义角色上更可能相互替换。频率加权确保高频token对获得更大权重。

**上下文映射 $\bar{\mathbf{\Phi}}$**（Eq. 11）：

$$\frac{1}{T} \sum_{k=1}^{T} \frac{1}{k} \sum_{m=1}^{k} \mathcal{P}_t(\text{第 }k+1\text{ token 是 } \mathbf{e}_i, \text{第 }m\text{ token 是 } \mathbf{e}_j) - \mu_j$$

该映射捕获token $\mathbf{e}_j$ 作为token $\mathbf{e}_i$ 的前缀上下文的平均概率。内层求和遍历前缀中所有位置，$1/k$ 加权使近端上下文贡献更大；$\mu_j$ 为中心化常数。该映射是值矩阵 $\mathbf{V}^{(l)}$ 的关键组成部分。

### 权重矩阵的主导项表征

根据Theorem 4.1，各权重矩阵在训练早期的梯度主导项可表示为：

- **输出矩阵** $\mathbf{W}_O \approx s\eta \bar{\mathbf{B}}$：由bigram统计直接决定，将最终隐藏状态映射为词汇分布。
- **值矩阵** $\mathbf{V}^{(l)} \approx \binom{s}{2} \eta^2 \bar{\mathbf{\Phi}}^{\top} \bar{\mathbf{B}}^{\top}$：组合了上下文映射与bigram映射，使值表示同时编码前缀上下文和后续token的关联信息。
- **查询-键矩阵** $\mathbf{W}^{(l)} \approx (3 C(s,4) + 2 C(s,3)) \eta^4 \bar{\mathbf{Q}}$：$\bar{\mathbf{Q}}$ 是基于可互换性映射和上下文映射的复合特征，用于计算token间的注意力分数。
- **相对位置编码** $\mathbf{P}^{(l)} \approx (3 C(s,4) + 2 C(s,3)) \eta^4 \mathbf{\Delta}$：$\mathbf{\Delta}$ 将关联映射到位置差而非词汇差，结构上与 $\bar{\mathbf{Q}}$ 类似。

### 单层模型的主导项计算

将上述权重近似代入单层模型的前向计算，得到主导项展开（Eq. 12）：

$$( \mathcal{S} ( \mathrm{Mask} ( \mathbf{X} \bar{\mathbf{Q}} \mathbf{X}^{\top} + \mathrm{DM} ( \pmb{\Delta} ) ) ) \mathbf{X} \bar{\pmb{\Phi}}^{\top} \bar{\mathbf{B}}^{\top} + \mathbf{X} ) \bar{\mathbf{B}}$$

其中自注意力块的核心计算（Eq. 13）为：

$$\mathcal{S} ( \mathrm{Mask} ( \mathbf{X} \bar{\mathbf{Q}} \mathbf{X}^{\top} + \mathrm{DM} ( \pmb{\Delta} ) ) ) \mathbf{X} \bar{\pmb{\Phi}}^{\top} \Sigma_{\bar{\mathbf{B}}}$$

该式揭示了注意力机制如何组合基函数：$\bar{\mathbf{Q}}$ 和 $\mathbf{\Delta}$ 分配注意力权重，$\bar{\mathbf{\Phi}}^{\top} \Sigma_{\bar{\mathbf{B}}}$ 提供基于上下文和可互换性的值表示，残差连接 $\mathbf{X}$ 保留原始token信息，最终通过 $\bar{\mathbf{B}}$ 映射到输出分布。多层模型通过迭代组合这些基函数逐步构建更复杂的语义关联。

### 理论适用范围与实验验证

该理论严格保证仅在训练早期（$\tilde{O}(1/\eta)$ 步内）成立。然而，在TinyStories上训练的3层模型验证显示：注意力、值、输出矩阵的理论主导项与实际学习权重的余弦相似度均超过0.998（Table 1），且训练100轮后仍保持在0.7以上（Figure 4）。在Pythia-1.4B（含MLP层）的OpenWebText训练中，早期注意力权重和嵌入的协方差矩阵也与理论特征高度匹配（Figure 6），表明理论在更实际的设定下仍具参考价值。

## 实验与分析

### 理论验证：主导项与实际权重的余弦相似度

论文通过在TinyStories数据集上训练一个3层纯注意力Transformer，系统验证了梯度主导项理论。核心验证手段是计算理论预测的主导项与实际学习到的权重矩阵之间的余弦相似度。

**Table 1** 给出了所有训练轮次中的最小余弦相似度：注意力权重（$W^{(l)}$）为 **0.999496**，值权重（$V^{(l)}$）为 **0.999169**，输出权重（$W_O$）为 **0.998486**。这三个关键矩阵的相似度均超过0.998，表明理论主导项在训练早期几乎完全解释了实际权重的方向。**Figure 4** 进一步展示了余弦相似度随训练轮次的演化轨迹：即使经过100轮训练，损失从8.00降至5.35，所有参数矩阵的余弦相似度仍保持在0.7以上，说明理论框架在早期阶段之外仍具有显著的参考价值。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_A4Us8jxVGq/figures/005_Figure_4.jpg]]
*Figure 4: Cosine similarity between theoretical and learned weights. Results from a 3-layer transformer model trained on TinyStories*

值得注意的是，**Table 2** 显示在使用BPE分词方式时，理论预测与学习权重的最小余弦相似度依然大于0.997，验证了该分析不依赖于特定的分词策略。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_A4Us8jxVGq/figures/009_Table_2.jpg]]
*Table 2: Minimum cosine similarities between theoretical and actually learned weights across all epochs. Results from a 3-layer attention-based model trained on TinyStories and with a BPE tokenization*

### 基函数的语义结构捕获

**Figure 5** 对三个基函数捕获的语义与语法结构进行了定性分析。在TinyStories语料上，bigram映射捕获了相邻token间的直接依赖关系（如"once"→"upon"），可互换性映射识别出功能相似的token聚类（如动词或介词类别），上下文映射则编码了更长距离的前缀-后缀共现模式。这些结果表明，梯度主导项不仅具有数学上的简洁性，其分解出的基函数确实对应了语言学上有意义的关联特征。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_A4Us8jxVGq/figures/006_Figure_5.jpg]]
*Figure 5: Selected tokens from the top 30 correlated tokens under different basis features from TinyStories. The characterized features actually capture both grammatical and semantic structures*

### 消融实验：各模块主导项的贡献

**Table 3** 通过逐模块移除主导项来量化各权重矩阵对模型性能的贡献（原始模型loss为5.349）：

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_A4Us8jxVGq/figures/010_Table_3.jpg]]
*Table 3: Loss of the attention-based model on TinyStories after the leading term component from each weight matrix is removed. The first row corresponds to the original model*

- **输出矩阵主导项 $\bar{B}$** 的移除导致loss大幅上升至 **8.287**，说明bigram统计是模型预测能力的核心支柱，移除后模型几乎丧失有效的下一个token预测能力。
- **值权重主导项（$V^{(l)}$）** 的逐层移除使loss上升至6.192~6.526区间，验证了由$\bar{\Phi}^\top \bar{B}^\top$组合构成的值表示对语义特征建模的重要性。值矩阵主导项将上下文映射与bigram映射融合，提供了比单纯bigram更丰富的语义信息。
- **注意力权重主导项（$W^{(l)}$）** 的逐层移除对loss影响甚微（5.349→5.350~5.361），表明在训练初始阶段，注意力分布本身对预测的边际贡献较小。这与理论分析一致：注意力机制的作用是细化值输出的加权方式，而值表示和输出映射承担了主要的预测功能。

### 大规模模型验证：Pythia-1.4B

论文进一步在Pythia-1.4B上检验了理论的泛化性。由于无法直接获取大规模模型的训练初期权重，作者采用协方差矩阵余弦相似度作为代理指标，比较注意力权重的协方差结构与理论主导项特征$\bar{Q}$的一致性。

**Figure 6** 显示，在OpenWebText语料上，Pythia-1.4B的嵌入映射和注意力权重（除第一层外）在训练早期与理论特征表现出高度一致性。然而，随着训练推进，权重逐渐从固定的关联特征漂移，早期层的偏离尤为明显。**Figure 7** 的逐头分析进一步揭示了层间差异：较早的层（如第2层）学习主导项特征的速度较慢，而较深的层（如第13层）在训练后期表现出更快的头特化现象。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_A4Us8jxVGq/figures/007_Figure_6.jpg]]
*Figure 6: Cosine similarity between covariance matrices for Pythia-1.4B attention weights and embeddings and the corresponding leading term features based on OpenWebText*

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_A4Us8jxVGq/figures/008_Figure_7.jpg]]
*Figure 7: Cosine similarity between covariance matrices for Pythia-1.4B individual attention head weights and the corresponding leading term features based on OpenWebText*

在FineWeb数据集上的验证（**Figure 8**）得到了与OpenWebText一致的结论，增强了结论的稳健性。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_A4Us8jxVGq/figures/011_Figure_8.jpg]]
*Figure 8: Cosine similarity between covariance matrices for Pythia-1.4B attention weights and embeddings and the corresponding leading term features based on FineWeb*

### 局限性与失败模式

1. **训练后期的理论偏离**：理论仅保证$O(1/\eta)$步内的权重近似，Figure 4和Figure 6均显示后期余弦相似度下降，理论无法直接解释收敛后的复杂行为。
2. **MLP的缺失**：理论假设纯自注意力架构，虽然Pythia实验表明MLP存在下部分结论仍成立，但MLP在早期学习中的具体贡献未被量化。
3. **规模限制**：直接验证限于3层attention-only模型和Pythia-1.4B，尚未在更大规模的最新LLM上系统检验。
4. **注意力主导项消融的微弱效应**：Table 3中移除注意力主导项对loss影响极小，这可能暗示在初始阶段注意力权重的学习尚未充分展开，或需要更长的训练才能体现其作用——这一点需要手动验证。

## 方法谱系与知识库定位

### 核心贡献与差异化定位

本文的核心贡献在于**首次为在真实自然语言语料上训练的自注意力Transformer提供了权重的显式闭式表征**。与以往工作相比，这一贡献的独特性体现在两个层面：

1. **从训练动态出发，而非事后解释**：大量机制可解释性工作（如特征归因、探测分类器、稀疏自编码器）在模型训练完成后对已学习的表示进行分析。本文则从梯度下降的训练动态入手，通过对梯度展开的主导项分析，**直接建立了权重与语料统计之间的因果联系**，揭示了模型“为什么”会学到特定的关联特征。

2. **从理论建模到实证验证的闭环**：本文不仅给出了理论预测（Theorem 4.1），还在TinyStories训练的3层模型和Pythia-1.4B两个尺度上进行了系统验证。理论预测的权重与实际学习权重的余弦相似度达到0.998以上（Table 1），为理论的可信度提供了强证据。

### 适用边界

本方法的适用性受以下条件约束：

- **架构假设**：理论分析基于纯自注意力架构（attention-only transformer），包含因果掩码、残差连接和相对位置编码，但**不含MLP/前馈网络**。虽然在Pythia-1.4B（含MLP）实验中观察到理论特征与嵌入/注意力权重仍有较高一致性（Figure 6），但MLP在早期学习中的具体贡献尚未被定量刻画。
- **训练阶段假设**：梯度主导项近似仅在训练早期（$O(1/\eta)$步内）有理论保证。实验表明，即使在100轮训练后，余弦相似度仍保持在0.7以上（Figure 4），但权重确实会逐渐偏离固定关联特征，向更丰富的知识表示演化。
- **数据与规模验证范围**：直接验证限于TinyStories数据集（3层模型）和Pythia-1.4B（OpenWebText/FineWeb预训练）。尚未在更大规模的最新LLM（如Llama系列、GPT-4等）上直接检验理论预测的精确性。
- **分词方式**：实验表明理论在字符级和BPE分词下均成立（Table 2，余弦相似度>0.997），但未覆盖其他分词策略（如WordPiece、SentencePiece的特定变体）。

### 局限与开放问题

**已识别的局限**：

1. **后期训练行为的解释缺失**：理论仅保证早期权重演化。训练后期权重从固定关联特征漂移后，主导项特征的具体演变规律尚不清楚，无法直接解释收敛后的复杂行为（如上下文推理、知识融合等）。
2. **MLP建模的缺失**：理论未涵盖MLP层在特征学习中的作用。尽管实验表明MLP存在下部分理论仍成立，但未能完全刻画MLP如何与自注意力模块协同构建语义表示。
3. **与下游能力的定量联系缺失**：理论揭示了基础的语义关联统计特征（bigram、可互换性、上下文），但尚未建立这些基函数与下游任务能力（如推理、知识检索、指令遵循）之间的定量映射。

**开放问题**：

1. **后期演化规律**：训练后期权重从固定关联特征漂移后，主导项特征的具体演变规律是什么？是否存在更高阶的展开可以刻画这一过程？
2. **MLP的早期贡献量化**：如何将梯度主导项分析推广到包含MLP层的完整Transformer，并量化MLP在早期学习中对语义特征构建的贡献？
3. **概念涌现的广泛假设**：能否利用基函数分解框架，提出关于模型中概念涌现的广泛假设（如语法结构、事实知识、推理模式的形成），从而超越对个别机制的解释？
4. **层级学习速率差异**：实验观察到不同层学习主导项特征的速度不同（例如Pythia-1.4B中第2层较慢，第13层更快，见Figure 7），其内在原因是什么？是否与层的深度、感受野大小或梯度流动特性有关？

## 原文 PDF

![[paperPDFs/ICLR_2026/How_Do_Transformers_Learn_to_Associate_Tokens_Gradient_Leading_Terms_Bring_Mechanistic_Interpretability.pdf]]
