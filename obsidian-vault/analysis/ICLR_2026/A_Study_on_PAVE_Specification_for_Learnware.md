---
title: "A Study on PAVE Specification for Learnware"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Study_on_PAVE_Specification_for_Learnware.pdf
project_link: null
code_link: null
aliases:
- PVPS
- SPSL
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning
core_operator: "通过微调共享预训练模型以拟合条件概率 p(ŷ|x)，将模型能力和任务需求编码为参数向量（PAVE），并利用其余弦相似度衡量对齐程度，从而统一刻画任务语义与模型质量。"
primary_logic: "在神经正切核（NTK）机制下，PAVE余弦相似度与基于最大均值差异（MMD）的RKME顺序一致，且参数向量可通过低秩分解（仅用B矩阵）高效近似，在保持识别准确性的同时将存储与计算开销降低至原来不足1%。"
claims:
- "参数向量通过拟合 p(ŷ|x) 同时编码任务语义和模型质量，解决了输出空间不可比与模型质量无保证两个关键难题。"
- "PAVE相似度与MMD在NTK假设下具有顺序一致性，意味着基于参数向量的识别与基于分布距离的识别等价。"
- "低秩近似下，仅使用B矩阵计算余弦相似度即可保留完整参数向量的相似度关系，且具有形式化误差界。"
- "在含损坏模型的学件库中，PAVE依然能有效识别高质量模型，显著优于只拟合数据分布的变体。"
---

# A Study on PAVE Specification for Learnware

> [!tip] 核心洞察
> 在神经正切核（NTK）机制下，PAVE余弦相似度与基于最大均值差异（MMD）的RKME顺序一致，且参数向量可通过低秩分解（仅用B矩阵）高效近似，在保持识别准确性的同时将存储与计算开销降低至原来不足1%。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 关于Learnware PAVE规范的研究 |
| 英文题名 | A Study on PAVE Specification for Learnware |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=JkKkquv5lw) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning |
| Method | Parameter Vector (PAVE) Specification |
| Dataset | NLP Datasets (beyond original functionality), Computer Vision Datasets (with corrupted learnwares), Medical LLM Benchmarks (PubMedQA) |

> [!tip] 效果简介
> - NLP Datasets (beyond original functionality) 上，Avg. Accuracy (or task-specific metrics) 为 0.709，对比 BERT-B 0.572, Best FT 0.699，变化 +0.137 over BERT-B。
> - Computer Vision Datasets (with corrupted learnwares) 上，Avg. Accuracy 为 0.887，对比 PAVE* 0.745，变化 +0.142。
> - Medical LLM Benchmarks (PubMedQA) 上，Accuracy 为 76.50，对比 Oracle 76.50，变化 0.00 (matches Oracle)。

## 概要

**问题瓶颈**：在开放、异构的学件市场中，任务语义多样、输出空间不可比，且开发者提交的模型质量参差不齐，使得在不访问原始训练数据的前提下，精准识别对用户任务“有帮助”的模型成为一个核心难题。

**方法定位**：本文提出 **Parameter Vector (PAVE) 规范**——一种通用的学件规格化方案。其关键设计在于，通过微调一个共享的预训练模型去 **拟合已有模型的条件概率 $p(\hat{y}|x)$**（而非原始数据分布），将模型的能力与任务需求统一编码为参数向量 $\tau$，并以向量间的 **余弦相似度** 衡量对齐程度，从而同时解决“任务语义不可比”与“模型质量无保证”两大瓶颈。

**核心理论洞察**：在神经正切核（NTK）假设下，PAVE 的余弦相似度与基于最大均值差异（MMD）的 RKME 分布距离具有 **顺序一致性**（Theorem 3），这意味着参数向量在建模语义对齐的同时，隐式保留了基于分布度量的识别等价性。进一步，通过 **低秩分解** 可将余弦相似度计算仅依赖于低秩矩阵 $B$，在保有理论误差界的前提下，将存储与计算开销降至原方案的 1% 以下。

**主要结果**（压缩）：

-   **跨任务识别效果**：在 NLP 基准（17 组任务，超出原训练功能）上，PAVE 平均性能达 **0.709**，相较最佳微调模型（0.699）和 RKME（0.659）均有显著提升（Table 1）。
-   **抗低质模型能力**：在包含损坏模型的 CV 场景中，拟合 $p(\hat{y}|x)$ 的 PAVE 达到 **0.887**，而仅拟合数据分布 $p(y|x)$ 的消融变体 PAVE* 仅为 0.745，验证了“建模模型能力”的必要性（Table 2）。
-   **低秩近似效率**：仅使用 $B$ 矩阵的模式（c）可保留 **99.4%+ 的性能**，而可训练参数量与存储开销均降至模式（a）的 0.1%–1%（Table A9）。
-   **统计显著性**：分层线性回归与精确多项检验均证实 PAVE 的识别非偶然，$p < 0.002$。

**需注意的局限**：低秩理论界依赖于各层范数均匀假设（未经验证）；实验规模有限（最大 17 任务），大规模异构库下的鲁棒性待检验；隐私保护仅靠低秩压缩的难逆性，缺乏形式化差分隐私保证。

学件（learnware）生态旨在构建一个开放、协同的模型复用体系：开发者将训练好的模型提交至学件坞（learnware dock system），用户无需接触原始训练数据即可检索并适配适合自身任务的模型。然而，这一范式的核心瓶颈在于——在异构、语义多样的任务空间中，模型输出结构互不相同，且模型质量参差不齐，**在不访问原始训练数据的条件下，精准识别对用户任务真正有帮助的模型极为困难**。具体而言，存在两个相互交织的关键难题：1）任务的语义类型与输出空间差异巨大（如文本分类、图像分割、回归），导致传统基于分布距离的模型规范（如 RKME）难以有效捕获模型能力与任务需求的对齐关系；2）模型开发者提交的学件质量并无保障，识别机制必须能够区分高能力模型与低质量甚至损坏的模型，而不能仅凭数据分布的相似性做判断。

现有方案在面对上述挑战时存在明显缺口。基于核均值嵌入（RKME）的规范方法主要适用于表格数据，对复杂语义任务和异构输出空间缺乏表达能力；而直接微调某一个通用预训练模型（如 BERT、ViT）虽然在统一架构下可获得可观性能，但其主要受限于单模型的容量——在样本十分稀缺且用户任务偏离预训练分布较远时，单个模型无法像大规模学件库那样提供跨任务的集体能力（见 **Figure 2**：通过学件库的多样性可解决单一微调难以适应的陌生任务）。另一方面，仅拟合数据分布 $p(y|x)$ 的模型规范无法排除那些在训练数据上表现不佳的模型，导致低质量学件依然可能被误选（见 **Section 1** 以及后续消融实验）。因此，学件规范需要一种既能刻画模型能力、又能有效度量任务需求对齐程度的统一编码方式。

为填补这一缺口，本研究提出 **参数向量规范（PAVE）**，其核心动机是通过共享预训练骨的参数变化量，同时编码**任务语义**与**模型质量**。具体思路为：开发者利用本地训练数据，通过微调预训练模型 $f$ 以拟合模型预测的条件概率 $p(\hat{y}|x)$，得到表示模型能力的参数向量 $\tau_h$；用户则基于少量样本和任务损失，通过类似过程生成代表任务需求的参数向量 $\tau_u$。二者间的余弦相似度 $\cos(\tau_h, \tau_u)$ 被用来定量衡量模型能力与用户需求的对齐程度（**式 (2)**）。这一设计统一解决了输出空间不可比与模型质量无保证两大障碍：参数向量中蕴含了任务语义（来自预训练模型特征空间的梯度）和模型预测能力（来自拟合目标 $h(x)$），因而能够同时区分任务类型差异和模型优劣。在理论上，这一机制在神经正切核（NTK）假设下与基于最大均值差异（MMD）的规范保持顺序一致性，为通过参数向量识别学件提供了严格保证。此外，通过低秩近似进一步将存储与计算开销降低至原先 1% 以下，为大规模学件检索铺平了道路。由此，PAVE 从设计上克服了传统规范在异构任务与质量不确定性下的固有弱点，为学件坞的实用化提供了核心驱动。

## 核心方法与创新机理

PAVE（Parameter Vector Specification）的核心创新在于将学件识别问题转化为**统一参数向量空间中的相似度匹配问题**，从根本上解决了异构输出空间下模型能力描述与质量评估两大瓶颈。

### 1. 统一的能力刻画：从分布到参数向量的表示跃迁

传统学件规范方法（如RKME）依赖核均值嵌入刻画数据分布，但在图像分类、文本回归、医疗问答等异构输出空间下，分布距离缺乏统一的语义可比性。PAVE的关键创新在于**改变规格表示的基底（changed slot: specification representation）**：直接微调共享的预训练模型以拟合模型的条件预测分布 $p(\hat{y}|x)$，将模型能力和任务需求编码为参数空间中的方向向量 $\tau$。

这一设计同时解决了两个相互纠缠的难题：
- **语义多样性**：不同任务的输出空间（分类标签、连续值、文本）通过统一的参数向量形式对齐，无需人工定义跨模态相似度。
- **质量无保证**：通过拟合模型预测而非真实数据分布，参数向量天然反映了模型的实际能力，而非假设的理想性能。

证据强度：在含损坏模型的CV学件库中（Table 2），拟合数据分布 $p(y|x)$ 的变体PAVE*仅达0.745准确率，而PAVE通过编码模型能力 $p(\hat{y}|x)$ 达到0.887，提升14.2个百分点，证伪了单纯拟合数据分布的路线的充分性。

### 2. 从MMD到余弦：等价性保证下的度量简化

PAVE用**余弦相似度取代MMD**作为对齐度量（changed slot: similarity metric），其理论合法性由NTK框架下的序一致定理保证：在梯度微调的神经正切核机制下，参数向量内积可分解为跨样本的隐式核函数求和（Lemma 2, Eq. 6），该核函数融合了输入相似性、任务特定损失梯度与模型预测信息。由此导出的核心结论是，PAVE余弦相似度与基于该隐式核的MMD在排序上完全等价（Theorem 3），即模型-任务间的相对对齐关系在两种度量下保持一致。

这意味着PAVE在保留分布距离判别力的同时，将高维RKHS中的复杂计算简化为参数向量的点积运算，计算量从$\mathcal{O}(n^2)$降至$\mathcal{O}(d)$。

证据强度：NLP跨功能实验（Table 1）中，PAVE平均准确率0.709，不仅显著优于随机选择（0.668）和RKME（0.659），甚至超越单模型微调最优方案（0.699），验证了参数空间相似度在真实异构任务中的识别能力。

### 3. 低秩近似：开销压缩至1%而不牺牲识别精度

完整参数向量 $\tau$ 在高维空间中存储与计算开销巨大。PAVE通过**低秩分解仅保留B矩阵计算余弦相似度**（changed slot: approximation strategy），并给出形式化误差界（Theorem 4），证明在一定条件下 $\cos(\tau_1, \tau_2) \approx \cos(\mathbf{B}_1, \mathbf{B}_2)$ 以高概率成立。

这一近似的实际效果显著：仅用B矩阵计算相似度（mode c），可训练参数量和存储开销均降至完整参数的0.1%–1%，而识别性能保留99.4%以上（Table A9）。Figure 3的可视化表明，低秩空间中的余弦相似度矩阵保持了全参数空间的相对序关系，佐证了理论界的实践有效性。

**需注意的理论局限**：Theorem 4的推导依赖于各层B矩阵范数近乎均匀的假设（Eq. 36），该假设在异构网络层中的普适性未经验证。若层间范数差异过大，近似误差可能超出理论界，需要在实际部署中加以监控。

![[assets/figures/papers/iclr26_0004_JkKkquv5lw_A_Study_on_PAVE_Specification_for_Learnware/figures/001_Figure_1.jpg]]
*Figure 1: Identifying helpful learnwares based on parameter vector similarity. 1. The developer trains the model with a large amount of data in $\mathcal { D } _ { t }$ and generates the model vector $\tau _ { h }$ based on the model prediction ${ \hat { y } }$ , then submits them to the system as a learnware. 2. The user generates the task vector $\tau _ { u }$ from a few samples in $\mathcal { D } _ { u }$ . ~ 3 . . The larger the cosine similarity between the model and task vectors means that the more likely the model capability is to fulfill the user task requirements

PAVE 规范围绕一个共享的预训练模型 $f(\mathbf{x}, \theta_0)$，将“学件能解决什么问题”与“用户需要什么”统一编码为**参数向量**，并在参数空间中用余弦相似度快速匹配。整个闭环由开发者、用户和学件坞系统三方协作完成，分为三个核心模块。

**1. 模型向量生成（开发者侧）**  
开发者拥有本地训练数据 $\mathcal{D}_t$ 和一个已训练好的候选模型 $h$。他以 $h$ 的预测作为软标签，微调预训练模型 $f$，最小化两者的输出差异：

$$
\tau_h = \underset{\tau}{\mathrm{argmin}} \sum_{(\mathbf{x}, y) \in \mathcal{D}_t} \mathcal{L}_t\big(g_t \circ f(\mathbf{x}, \theta_0 + \tau),\; h(\mathbf{x})\big)
$$

得到的参数更新 $\tau_h$ 即为**模型向量**，它刻画了模型能力 $p(h(\mathbf{x})|\mathbf{x})$。开发者只需将 $\tau_h$ 提交至学件坞，无需暴露原始数据或完整模型。

**2. 任务向量生成（用户侧）**  
用户仅持有少量标注样本 $\mathcal{D}_u$。他将微调目标从模型预测 $h(\mathbf{x})$ 替换为真实标签 $y$，用相同的对齐损失生成**任务向量** $\tau_u$，表达任务需求 $p_u(y|\mathbf{x})$。

**3. 相似度识别（系统侧）**  
学件坞系统对库中每个 $\tau_h$ 计算其与用户 $\tau_u$ 的余弦相似度：

$$
\cos(\tau_h, \tau_u) = \mathrm{Similarity}\big(p(h(\mathbf{x})|\mathbf{x}),\; p_u(y|\mathbf{x})\big)
$$

相似度越高，表明模型能力与用户任务越对齐。系统最终选取余弦相似度最高的学件推荐给用户。

这一流程在 NTK 假设下等价于在分布间执行 MMD 比较，从而无需访问原始数据即可可靠筛选。为应对大规模学件库的存储和计算压力，PAVE 进一步引入**低秩近似**：将参数向量分解为固定随机矩阵 $\mathbf{A}$ 与可学习矩阵 $\mathbf{B}$ 的乘积 $\tilde{\tau} = \mathbf{B}\mathbf{A}$，仅保留 $\mathbf{B}$ 参与相似度计算。近似关系 $\cos(\tilde{\tau}_1, \tilde{\tau}_2) \approx \cos(\mathbf{B}_1, \mathbf{B}_2)$ 在形式化误差界保证下，将存储和计算开销降低到完整方案的 1% 以下，同时几乎不损失识别精度。

### 设计动机与核心机制
在开放、异构的学件生态中，任务的语义多样且输出空间不可直接比较，加之模型质量参差不齐，使得在不访问原始训练数据的前提下精准识别有用模型极为困难。PAVE（参数向量规范）通过**同时拟合模型能力 p(ŷ|x) 和任务需求 p(y|x)** 来构建统一的表征，并利用向量余弦相似度度量对齐程度，一举解决语义异构与质量无保证两大难题。在神经正切核（NTK）条件下，该相似度与基于最大均值差异（MMD）的 RKME 排序一致，等价于在隐含核空间中进行分布匹配。

### 核心模块

#### 1. 模型向量生成（开发者侧）
开发者使用本地数据 $\mathcal{D}_t$，通过微调共享的预训练模型 $f(\cdot,\theta_0)$，使其输出逼近已提交模型 $h(\mathbf{x})$ 的预测，由此构建代表模型能力的参数向量 $\tau_h$：

$$
\tau_h = \underset{\tau}{\mathrm{argmin}} \sum_{(\mathbf{x}, y) \in \mathcal{D}_t} \mathcal{L}_t \big( g_t \circ f(\mathbf{x}, \theta_0 + \tau), h(\mathbf{x}) \big) \tag{1}
$$

其中 $g_t$ 为任务相关的输出头，$\mathcal{L}_t$ 为任务特定损失（如交叉熵）。通过拟合 $h$ 的软标签，$\tau_h$ 编码了模型的能力而非单纯的数据分布。

#### 2. 任务向量生成（用户侧）
用户基于少量样本和任务标签，以类似方式微调预训练模型生成任务向量 $\tau_u$。此时将式 (1) 中的 $h(\mathbf{x})$ 替换为真实标签 $y$，因此 $\tau_u$ 反映用户任务所需的条件分布 $p_u(y|\mathbf{x})$。

#### 3. 相似度驱动的学件识别（系统侧）
学件坞系统计算模型向量与任务向量的余弦相似度：

$$
\cos(\tau_h, \tau_u) = \mathrm{Similarity}\big(p(h(\mathbf{x})|\mathbf{x}), p_u(y|\mathbf{x})\big) \tag{2}
$$

相似度愈高，表示模型能力与用户需求愈对齐，系统由此选出 top‑k 学件推荐给用户。

### 关键公式与理论支撑

#### NTK 机制下的内积分解
在一阶泰勒近似的 NTK 假设下，微调过程中的参数更新可累加为梯度。模型向量 $\tau_h$ 和任务向量 $\tau_u$ 的内积可分解为成对样本之间的隐式核函数求和：

$$
\langle \tau_h, \tau_u \rangle = \sum_{(\mathbf{x}_i, y_i) \in \mathcal{D}_t} \sum_{(\mathbf{x}_j, y_j) \in \mathcal{D}_u} \tilde{k}_{f,\mathcal{L},g}\big(\mathbf{x}_i, h(\mathbf{x}_i), \mathbf{x}_j, y_j\big) \tag{3}
$$

该核 $\tilde{k}_{f,\mathcal{L},g}$ 由两部分组成：$\tilde{K}_f$ 捕捉输入在预训练特征空间中的相似度，$\tilde{K}_{\mathcal{L},g}$ 融合任务语义与模型预测的梯度信息。由此导出**顺序一致性定理**：PAVE 余弦相似度与基于该核的 MMD 保持相同的排序。

#### 低秩近似与高效相似度计算
为降低存储和计算开销，参数向量通过低秩矩阵 $\mathbf{B}$ 和随机初始化且固定的 $\mathbf{A}$ 进行因子化，$\tilde{\tau} = \mathbf{B}\mathbf{A}$，优化目标仅涉及 $\mathbf{B}$：

$$
\mathbf{B}^* = \arg\min_{\mathbf{B}} \sum_{(\mathbf{x}, y) \in \mathcal{D}} \mathcal{L}\big(g \circ f(\mathbf{x}, \theta_0 + \mathbf{B}\mathbf{A}), \cdot \big) \tag{4}
$$

在适当条件下，完整参数向量的余弦相似度可用仅基于 $\mathbf{B}$ 的余弦相似度高效近似：

$$
\cos(\tilde{\tau}_1, \tilde{\tau}_2) \approx \cos(\mathbf{B}_1, \mathbf{B}_2) \tag{5}
$$

其理论保障由**概率误差界**给出：当各层 $\mathbf{B}$ 的范数较为均衡，且 $\epsilon \le 0.5$ 时，下式以高概率成立

$$
\begin{aligned}
-2\epsilon + \min\!\Big(&\frac{1}{1+\epsilon}\cos(\mathbf{B}_1,\mathbf{B}_2),\; \frac{1}{1-\epsilon}\cos(\mathbf{B}_1,\mathbf{B}_2)\Big) \\
\leq \cos&(\mathbf{B}_1\mathbf{A},\mathbf{B}_2\mathbf{A}) \\
\leq \max\!\Big(&\frac{1}{1-\epsilon}\cos(\mathbf{B}_1,\mathbf{B}_2),\; \frac{1}{1+\epsilon}\cos(\mathbf{B}_1,\mathbf{B}_2)\Big) + 2\epsilon
\end{aligned}
$$

从而在仅需存储 $\mathbf{B}$ 的条件下（参数量降至原来的 0.1%–1%）仍能可靠保持相似度排序，支撑学件库的大规模高效检索。

## 实验与关键发现

PAVE 在跨任务、跨模态的学件识别场景中展现出一致的优势，其核心在于通过拟合模型预测分布 $p(\hat{y}|\mathbf{x})$ 构建参数向量，同时编码任务语义与模型能力，解决了输出空间不可比和模型质量无保证两个根本瓶颈。以下围绕主结果、关键消融、效率分析和失效边界展开。

### 主结果：跨基准识别性能

**NLP 跨任务识别（Table 1）** 在 17 个经典语言理解任务上，PAVE 平均得分 0.709，较直接微调 BERT-Base 的基线 0.572 提升 0.137，也高于最佳微调模型 RoBERTa-Large 的 0.699。在领域差异极大的 CoLA（Mcc 0.100 vs. 最佳微调 0.086）和 MRPC（Acc 0.782 / F1 0.854）上，PAVE 显著优于所有单模型微调方案，证实学件组合能力可超越单个大模型的泛化极限。

![[assets/figures/papers/iclr26_0004_JkKkquv5lw_A_Study_on_PAVE_Specification_for_Learnware/figures/004_Table_1.jpg]]
*Table 1: Performances on NLP datasets beyond the original functionality*

**计算机视觉含损坏模型（Table 2）** 为模拟开放环境中模型良莠不齐的现实，学件库包含低质量模型后，PAVE 平均准确率为 0.887，而拟合数据分布 $p(y|\mathbf{x})$ 的变体 PAVE* 仅为 0.745（+0.142）。这直接证明了只刻画数据分布无法过滤低质量学件，必须编码模型真实预测能力。

![[assets/figures/papers/iclr26_0004_JkKkquv5lw_A_Study_on_PAVE_Specification_for_Learnware/figures/005_Table_2.jpg]]
*Table 2: Performances on computer vision datasets with corrupted learnwares*

**医学 LLM 基准（Table A4）** 在 PubMedQA 上，PAVE 的 top‑1 推荐准确率达到 76.50，与 Oracle 一致；在其他 8 个医学考试基准上同样逼近最优水平，显示该方法对生成式模型同样有效。

### 消融研究

**模型能力 vs. 数据分布** 上述 CV 损坏实验已构成核心消融：PAVE* 替换 $p(\hat{y}|\mathbf{x})$ 为 $p(y|\mathbf{x})$ 后性能骤降。因果机制在于，参数向量通过最小化微调损失 $\mathcal{L}(g_t \circ f(x,\theta_0+\tau), h(x))$ 累积梯度，该梯度隐含模型预测的置信和错误模式；仅仅拟合真实标签分布会丢失这些关于模型质量的关键信息。统计支持来自分层线性回归和精确多项检验（Table A12），所有场景下 p < 0.002，拒绝“识别结果随机”的零假设。

**低秩近似：仅用 B 矩阵计算相似度**  
对 $\tilde{\tau} = \mathbf{B}\mathbf{A}$ 做随机低秩分解后，余弦相似度 $\cos(\tilde{\tau}_1, \tilde{\tau}_2)$ 可仅通过 $\cos(\mathbf{B}_1, \mathbf{B}_2)$ 高效近似，并享有概率界（Theorem 4，在 $\epsilon \le 0.5$ 且各层 $\mathbf{B}$ 范数均匀假设下成立）。实际表现（Table A9）中，模式 (c) 仅保留约 1% 的可训练参数（即仅 B 矩阵），相对完整参数向量的性能保持 99.4%–100%，同时存储和计算开销降至原来的不足 1%。视觉证据（Figure 3、A13、A14）显示低秩近似完好地保存了模型间余弦相似度的相对次序，保证了推荐排序的稳定性。

![[assets/figures/papers/iclr26_0004_JkKkquv5lw_A_Study_on_PAVE_Specification_for_Learnware/figures/003_Figure_3.jpg]]
*Figure 3: Consistency of the cosine similarity between parameter vectors, with the diagonal colors omitted to enhance visual contrast. (a) shows the exact similarity of the parameter vectors with full parameter fine-tuning. (b) shows the approximating similarity in the low-rank space after expanding parameter vectors to ( $\mathbf { B A } ) _ { m \times n }$ in full size. (c) shows the approximating similarity computed using B alone for improved storage and computational efficiency, which is the method we propose

**鲁棒性可视化** 箱线图（Figure A4、A5、A6）刻画了所有学件性能分布以及 PAVE 基于相似度选择的 top‑1/top‑2 表现。在 NLP 和 CV 的几乎所有数据集上，top‑1 选择均落在分布的上尾，且中位性能接近 Oracle，进一步佐证余弦相似度与下游任务性能之间的强正序关系。

### 局限与失败模式

1. **大规模异质场景未验证**——当前实验最多包含 17 个 NLP 任务，学件库规模有限。当模型数量膨胀至数百或数千且任务语义极度发散时，余弦相似度是否仍能维持细致的鉴别力尚需验证，存在排序崩溃的风险。

2. **低秩近似的关键假设未充分检验**——Theorem 4 的推导依赖“各层 B 矩阵的范数近似均匀分布”（式 36），该假设在实践中的适用范围未经系统消融。若某些层方差过大，概率界可能失效，导致实际近似误差大于预期，需要手动核实其在不同网络拓扑下的泛化性。

3. **隐私保障仅依赖压缩难逆性**——参数向量构建过程可能隐式编码训练数据的梯度信息，但目前仅靠低秩分解增加复原难度，未进行差分隐私标定或成员推理攻击测试，因此宣称“隐私安全”的证据薄弱，实际部署中不可直接采信。

4. **任务类型覆盖狭隘**——所有实验均限于分类与回归任务，生成、检索、强化学习等输出空间更复杂的场景未被探索。这些场景下损失函数 $\mathcal{L}_t$ 和梯度结构可能与当前定义差异极大，参数向量的表征能力需重新评估。

5. **预训练基座依赖**——每个子域需预先选定合适的共享预训练模型（如 BERT、ResNet），一旦基座模型的归纳偏置与用户任务严重不匹配，PAVE 可能无法生成有鉴别力的参数向量。该因素未作消融，限制了方法在全新模态上的即插即用能力。

6. **资源公平性与边缘设备**——实验均在有 GPU 的服务器侧完成，未分析小样本、弱算力用户生成任务向量的可行性，也未提供边缘‑云协同的轻量化方案，这对推动学件生态普惠化构成障碍。

综上，PAVE 在中等规模异质任务中提供了高效、有序的学件识别方案，但迈向真正开放世界的部署仍需填补大规模、隐私可证明和跨任务泛化方面的空白。

![[assets/figures/papers/iclr26_0004_JkKkquv5lw_A_Study_on_PAVE_Specification_for_Learnware/figures/021_Table_9.jpg]]
*Table 9: Table A9: In mode (a), parameter similarity is computed exactly using the full parameter vectors obtained through complete fine-tuning. In mode (b), similarity is approximated in the low-rank space after expanding the parameter vectors to their full size as ( $\mathbf { B A } ) _ { m \times n }$ . In mode (c), similarity is approximated both in the low-rank space and computed using only the matrix B, which significantly reduces storage and computational costs—this is the method proposed in our approach

![[assets/figures/papers/iclr26_0004_JkKkquv5lw_A_Study_on_PAVE_Specification_for_Learnware/figures/030_Table_12.jpg]]
*Table 12: Table A12: The statistical significance of our method: p-values*

## 定位与知识库关联

### 与直接微调基线的关系：从单模型适配到学件复用

PAVE的核心定位不是提出一种更强的微调方法，而是将学件复用确立为单模型微调的**范式替代方案**。直接微调预训练模型（BERT/RoBERTa/ResNet/ViT）在样本受限时受限于单一模型的容量瓶颈——即使预训练质量很高，单个模型也难以覆盖所有陌生任务的语义多样性（Figure 2）。PAVE通过参数向量将学件库中多个模型的能力封装为可比较的规格表示，使用户无需访问原始训练数据即可从中检索最有助于当前任务的模型。在NLP任务上，PAVE的平均准确率达0.709，显著优于最优微调预训练模型（RoBERTa-L: 0.699）和随机选择基线（0.668），表明**检索复用优于单模型微调**（Table 1）。

### 与RKME的谱系关系：从分布距离到能力对齐

PAVE与基于核均值嵌入的先前规范方法RKME构成直接谱系继承关系，但两者在**适用模态**和**核心度量维度**上有本质差异：

- **RKME** 面向表格数据，在可再生核希尔伯特空间（RKHS）中通过缩减集嵌入数据的边际分布，以最大均值差异（MMD）衡量任务相似度。它更适合输入空间结构相对简单的场景。
- **PAVE** 则通过微调共享预训练模型拟合条件概率 $p(\hat{y}|\mathbf{x})$，将模型能力与任务需求编码为参数向量，并以余弦相似度 $\cos(\tau_h, \tau_u)$ 衡量对齐程度。它天然适合文本、图像等高维非结构化数据。

在神经正切核（NTK）假设下，二者存在理论上的深层联系：PAVE相似度与基于隐式核 $k_{f,\mathcal{L},g}$ 的MMD具有**顺序一致性**（Theorem 3），这意味着在NTK成立时，基于参数向量的识别与基于分布距离的识别等价。PAVE可视为RKME在预训练模型时代的泛化——它将“分布距离”重新映射为“参数变化方向”，从而统一刻画任务语义与模型质量。

### 方法维度的关键改变点

PAVE相对于基线方法在三个关键维度上做出了改变，构成了其核心贡献：

**1. 规格表示**：从“分布嵌入”到“参数向量”。PAVE将模型规格定义为预训练模型参数的变化量：
$$\tau_h = \underset{\tau}{\mathrm{argmin}} \sum_{(\mathbf{x}, y) \in \mathcal{D}_t} \mathcal{L}_t \big( g_t \circ f(\mathbf{x}, \theta_0 + \tau), h(\mathbf{x}) \big)$$
该参数向量实际上是微调过程梯度累积的结果，同时编码了模型预测行为 $p(h(\mathbf{x})|\mathbf{x})$ 和任务语义结构（Appendix A）。

**2. 相似度度量**：从“分布距离”到“能力对齐”。余弦相似度 $\cos(\tau_h, \tau_u) = \mathrm{Similarity}(p(h(\mathbf{x})|\mathbf{x}), p_u(y|\mathbf{x}))$ 直接度量的是**模型能力与用户需求的对齐程度**，而非数据分布的接近程度。消融实验证实了这一选择的关键性：当学件库包含低质量模型时，拟合模型能力 $p(\hat{y}|\mathbf{x})$ 的PAVE（0.887）显著优于拟合数据分布 $p(y|\mathbf{x})$ 的变体PAVE*（0.745），差值高达0.142（Table 2）。

**3. 近似策略**：从“全参数”到“低秩矩阵B”。低秩分解 $\tilde{\tau} = \mathbf{B}\mathbf{A}$ 后，仅使用矩阵B计算余弦相似度即可保留完整参数向量的相似度关系：
$$\cos(\tilde{\tau}_1, \tilde{\tau}_2) \approx \cos(\mathbf{B}_1, \mathbf{B}_2)$$
这一近似在保持99.4%以上识别性能的同时，将可训练参数、存储与计算开销降至原来的0.1%–1%（Table A9），且有形式化概率误差界（Theorem 4）。低成本使得PAVE在学件坞系统中可以高效支持大规模学件库的检索。

### 适用边界与关键局限

**已验证的有效范围**：
- 分类与回归任务上的学件识别，涵盖NLP（17个任务）、计算机视觉（12个任务）和医学LLM（9个基准）三个领域
- 学件库中存在质量参差不齐的模型时，PAVE仍能有效筛选高质量学件
- 统计检验确认识别结果具有显著性（分层线性回归和精确多项检验的p值均<0.002）

**关键局限与待验证边界**：

1. **低秩近似假设的脆弱性**：定理4的理论界依赖于各层B矩阵范数近乎均匀分布的假设（式36），该假设在实践中的有效性未经系统评估。当某些层的参数变化远大于其他层时，近似质量可能下降。

2. **规模验证不足**：实验仅在较小规模学件库上进行（最多17个NLP任务），未验证数百乃至数千个异构模型共存时的识别精度和检索效率。随着学件数量增长，余弦相似度的区分能力是否会稀释尚不明确。

3. **任务类型覆盖盲区**：仅测试了分类和回归任务，对生成、检索、强化学习等输出空间更复杂的任务类型未有探索。对于输出空间为序列或结构化对象的任务，基于输出概率 $p(\hat{y}|\mathbf{x})$ 编码的能力向量可能不足以刻画模型的全部功能。

4. **隐私保护的非形式化**：当前仅依赖低秩压缩的难逆性提供隐式隐私保护，未进行差分隐私或成员推理攻击的正式验证。参数向量在构建过程中是否会泄露训练数据信息仍是开放问题。

5. **预训练模型选择的敏感性**：需要为每个任务域选择合适的共享预训练模型作为基座，不同预训练模型的选择对PAVE识别性能的影响未进行消融分析。当用户任务与预训练模型的训练分布偏差较大时，参数向量的表达能力可能受限。

### 开放问题与研究前景

1. **资源受限环境的适配**：如何为移动端或边缘设备生成参数向量，使学件生态覆盖计算资源严重受限的场景？这可能涉及更激进的低秩策略或与参数高效微调技术的深度结合。

2. **极端语义外推**：当用户任务与学件库中任何已有任务的语义相差极大时，PAVE是否仍能提供有意义的相似度排序？在何种条件下参数向量空间中的最近邻搜索会失效？

3. **多模态规范的融合**：能否将PAVE与语义模型描述（如Model Card）融合，在高层次功能指令与底层参数表征之间建立可解释的桥梁？这可能在用户缺乏足够标注样本时降低任务向量的生成门槛。

4. **结构化低秩近似**：低秩近似是否可进一步按模块或层分配不同秩，在Transformer的注意力层和MLP层之间平衡效率与表征精度？

5. **联邦场景下的隐私增强**：在分布式协作构建学件库时，如何在不暴露原始梯度的情况下生成和匹配任务向量？这需要将低秩近似与安全多方计算或联邦学习技术结合。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Study_on_PAVE_Specification_for_Learnware.pdf

![[paperPDFs/ICLR_2026/A_Study_on_PAVE_Specification_for_Learnware.pdf]]
