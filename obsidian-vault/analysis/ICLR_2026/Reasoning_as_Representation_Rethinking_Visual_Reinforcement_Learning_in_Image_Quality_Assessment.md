---
title: "Reasoning as Representation: Rethinking Visual Reinforcement Learning in Image Quality Assessment"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Reasoning_as_Representation_Rethinking_Visual_Reinforcement_Learning_in_Image_Quality_Assessment.pdf
project_link: null
code_link: https://github.com/xuanyuzhang21/RALI
openreview_forum_id: DkHt2K1g2Y
aliases:
- RRALI
- RARRVRLIQA
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "是否将图像质量评分的依赖从视觉token转移到质量推理文本token（即压缩视觉信息为文本表征）。"
primary_logic: "RL使MLLM学得的推理本质上是一种从视觉到文本的跨域对齐压缩，该压缩可通过对比学习直接复现，从而无需实际推理过程即可获得同等泛化。"
claims:
- "在生成评分token时，95%的注意力权重集中在先前生成的推理文本token上（Figure 3），证明推理模型主要通过文本表征进行评分。"
- "在不同数据集（KonIQ、KADID）上训练的LLM推理模块在域外数据集（CSIQ、LiveW）上表现高度一致，PLCC差异<0.01（Table 1），表明推理过程本身具有跨域泛化性。"
- "禁用推理能力后，Q-Insight的平均PLCC从0.806骤降至0.768（Table A.1），直接证实推理是实现泛化的关键。"
- "RALI仅使用约4%的参数和3.4%的推理时间，达到与Q-Insight可比的跨数据集评分精度（Figure 1, Table 2, Figure 6）。"
---

# Reasoning as Representation: Rethinking Visual Reinforcement Learning in Image Quality Assessment

> [!tip] 核心洞察
> RL使MLLM学得的推理本质上是一种从视觉到文本的跨域对齐压缩，该压缩可通过对比学习直接复现，从而无需实际推理过程即可获得同等泛化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 推理即表征：重新思考图像质量评估中的视觉强化学习 |
| 英文题名 | Reasoning as Representation: Rethinking Visual Reinforcement Learning in Image Quality Assessment |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=DkHt2K1g2Y) · [GitHub](https://github.com/xuanyuzhang21/RALI) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | RALI (Reasoning-Aligned Lightweight IQA) |
| Dataset | 7数据集平均（单域训练）, 4数据集跨域训练（KonIQ+SPAQ+KADID+PIPAL）, 效率对比（Batch size=16） |

> [!tip] 效果简介
> - 7数据集平均（单域训练） 上，PLCC 为 0.798 (RALI)，对比 0.806 (Q-Insight)，变化 -0.008。
> - 4数据集跨域训练（KonIQ+SPAQ+KADID+PIPAL） 上，平均PLCC 为 0.855 (RACT)，对比 0.791 (Q-Insight 混合训练)，变化 +0.064。
> - 效率对比（Batch size=16） 上，推理时间/内存相对占比 为 3.4% (RALI)，对比 100% (Q-Insight)，变化 -96.6%。

## 概要

图像质量评估（IQA）长期以来依赖高维视觉表征，这类方法在不同数据分布间极易过拟合，泛化能力受限。近期，基于强化学习（RL）的多模态大语言模型（MLLM）如**Q-Insight**（Li et al., 2025）通过将图像质量评分转化为逐步推理任务，展现出显著的跨域泛化能力。然而，其推理过程引入了高昂的计算开销。

本文的核心洞察在于：**RL使MLLM学得的推理，本质上是一种从视觉到文本的跨域对齐压缩**。实验证据表明，Q-Insight在生成评分token时，95%的注意力权重集中在先前生成的推理文本token上（Figure 3），而非原始视觉token；且在不同数据集上训练的推理模块在域外测试中表现高度一致，PLCC差异小于0.01（Table 1）。这揭示了推理模型泛化的真正来源是紧凑的文本表征，而非推理过程本身。

基于此，论文提出**RALI（Reasoning-Aligned Lightweight IQA）**，一种无需推理和LLM的轻量级IQA方法。其核心思路是：利用对比学习，将视觉编码器的输出直接对齐到RL模型学得的泛化文本表征空间，再通过特征压缩与可学习基向量评分机制完成质量预测。该方法从根本上解耦了泛化表征与推理计算。

主要结果：

- **精度可比**：在单域训练下，RALI在7个数据集上的平均PLCC达到0.798，与Q-Insight的0.806仅差0.008（Table 2）。
- **极致轻量**：RALI仅使用Q-Insight约4%的参数量，推理时间和内存占用均降低超过95%（Figure 1, Figure 6）。
- **跨域优势**：在四数据集混合训练场景下，RACT框架的平均PLCC达到0.855，显著优于Q-Insight混合训练的0.791（Table A.2）。

RALI的成功表明：在IQA任务中，高质量文本表征所携带的泛化信息，可以通过直接对齐的方式被轻量模型高效继承，推理过程并非泛化的必要条件。



### 图像质量评估的范式演进

图像质量评估（IQA）旨在自动预测与人类感知一致的图像质量分数，是计算机视觉中的基础任务。传统方法可分为两类：基于手工特征的经典算法（如**NIQE**（Mittal et al., 2012b）、**BRISQUE**（Mittal et al., 2012a））和基于深度学习的回归模型（如**CLIP-IQA+**（Wang et al., 2023））。然而，这些方法的核心瓶颈在于：它们依赖高维视觉表征进行质量评分，而视觉特征空间在不同数据集的分布之间存在显著的域间隙（domain gap），导致模型容易在训练集上过拟合，跨域泛化能力薄弱。

近年来，多模态大语言模型（MLLM）的兴起为IQA带来了新范式。研究者尝试利用MLLM的文本理解能力进行质量评分，例如基于监督微调（SFT）的**Q-Align**（Wu et al., 2024b）和**DeQA-Score**（You et al., 2025），以及基于强化学习（RL）的**Q-Insight**（Li et al., 2025）和**VisualQuality-R1**（Wu et al., 2025b）。其中，RL推理模型展现出了令人瞩目的跨域泛化能力——其核心机制在于：模型在输出最终评分之前，先生成一段质量推理文本（位于`<think>`和`</think>`标签之间），再基于该文本生成分数。

### 推理泛化的机制性发现

本文对RL推理模型的泛化机制进行了深入剖析，揭示了一个关键洞察：**推理本质上是一种从视觉到文本的跨域对齐压缩**。具体而言：

- **注意力转移**：在生成评分token时，Q-Insight将95%的注意力权重分配给先前生成的推理文本token，而仅5%分配给视觉token（Figure 3）。这意味着评分决策几乎完全依赖文本表征，而非原始视觉特征。
- **表征压缩**：一幅512×384的图像需要约1000个视觉token进行表征，但推理文本仅需不到100个token（压缩比超过10倍），且文本表征空间的域间隙远小于视觉空间（Figure 4的t-SNE可视化）。
- **跨域一致性**：在KonIQ和KADID两个不同数据集上独立训练的LLM推理模块，在域外数据集（CSIQ、LiveW）上表现出高度一致的性能（PLCC差异<0.01，Table 1），证实推理过程本身具有跨域泛化性，而非依赖特定数据集的视觉分布。
- **推理必要性的直接验证**：当禁用Q-Insight的推理能力后，其平均PLCC从0.806骤降至0.768（Table A.1），直接证明推理是实现泛化的关键。

### 现有方法的缺口与本文动机

尽管RL推理模型实现了优异的跨域泛化，但其代价十分显著：推理过程引入了高昂的计算开销。Q-Insight需要加载完整的7B参数LLM，在推理时逐token生成质量描述文本，导致推理时间和内存消耗远超传统IQA方法。

这引发了一个根本性问题：**既然推理的作用是将视觉信息压缩为紧凑的文本表征，那么能否绕过实际的推理过程，直接学习这种压缩映射？**

本文的核心动机正是基于这一洞察：RL使MLLM学得的推理本质上是一种从视觉到文本的跨域对齐压缩，该压缩可通过对比学习直接复现，从而无需实际推理过程即可获得同等泛化。基于此，本文提出了**RALI（Reasoning-Aligned Lightweight IQA）**框架，仅使用约4%的参数和3.4%的推理时间，达到与Q-Insight可比的跨数据集评分精度（Figure 1）。



## 核心方法与创新机理

### 1. 问题瓶颈与因果调节变量

传统无参考图像质量评估（NR-IQA）方法依赖高维视觉表征（如将图像编码为超过1000个视觉token），容易在不同数据集的分布间产生过拟合。基于强化学习（RL）的多模态大语言模型（MLLM）方法（如 **Q-Insight**，Li et al., 2025）通过将视觉信息压缩为紧凑的文本推理表征（少于100个token），实现了显著的跨域泛化能力，但推理过程本身引入了巨大的计算开销。

本工作的核心因果调节变量在于：**是否将图像质量评分的依赖从视觉token转移到质量推理文本token**。论文通过一系列机制分析证实了这一变量对泛化能力的决定性作用：

- **注意力机制证据**（Figure 3）：在生成评分token时，Q-Insight将95%的注意力权重集中在先前生成的推理文本token上，仅5%分配给视觉token，证明推理模型**主要通过文本表征进行评分**，而非直接依赖视觉特征。
- **跨域一致性证据**（Table 1）：在KonIQ和KADID两个不同数据集上分别训练的LLM推理模块，在域外数据集（CSIQ、LiveW）上的PLCC差异小于0.01，表明推理过程本身具有跨域泛化性，与训练数据来源无关。
- **推理必要性证据**（Table A.1）：禁用Q-Insight的推理能力后，其平均PLCC从0.806骤降至0.768，直接证实推理是泛化能力的关键来源。

这些发现揭示了一个核心洞察：**RL使MLLM学得的推理本质上是一种从视觉到文本的跨域对齐压缩**，该压缩将图像质量信息从高维、域敏感的视觉空间映射到低维、域鲁棒的文本空间。

### 2. 关键创新：从“推理”到“对齐”

基于上述洞察，论文提出了**RALI（Reasoning-Aligned Lightweight IQA）**框架，其核心创新在于**将推理过程解耦为可复现的跨模态对齐问题**，从而在不执行实际推理的情况下获得同等的泛化能力。

RALI相对于RL推理基线（Q-Insight）的**三个关键changed slots**如下：

| 模块 | 基线方法（Q-Insight） | RALI方法 | 证据锚点 |
|------|----------------------|----------|----------|
| **推理过程** | 使用LLM进行显式逐步推理（输出`<think>...</think>`标签内的推理文本） | 无推理，通过CLIP对比学习将图像直接映射到预构建的质量文本空间 | ABSTRACT, Section 4 |
| **特征提取** | 将图像编码为超过1000个视觉token送入LLM处理 | 使用CLIP对齐编码器提取图像嵌入，经PCA降至512维，再通过分桶K-Means聚类得到紧凑基向量集合 | Section 4, Figure 5 |
| **评分计算** | LLM在`<answer>`标签内输出数值分数 | 计算图像嵌入与基向量的余弦相似度，通过softmax归一化得到权重，加权求和基向量对应的代表分数（Eq.(3)） | Eq.(3), Section 4 |

### 3. 技术实现路径

RALI通过三个顺序模块实现从推理到对齐的转化：

**（1）对比对齐（Contrastive Alignment）**：利用CLIP损失微调视觉编码器，使其输出与RL模型生成的质量推理文本空间对齐。这一步将RL模型学到的跨域泛化知识“蒸馏”到视觉编码器中，是后续所有操作的基础。消融实验（Table 4, Case 1 vs. Case 6）表明，去除对比对齐后平均PLCC从0.798下降至0.748，损失显著。

**（2）特征压缩（Feature Compression）**：对对齐后的嵌入进行PCA降维（768→512维），然后采用分桶K-Means聚类。具体而言，先将训练样本按质量分数分桶，在每个桶内独立进行K-Means聚类，得到紧凑的基向量集合 $\{\mu_i\}$ 及其对应的代表分数 $\{f_i\}$。聚类中心的更新公式为：

$$\mu_{nj} = \sum_{m \in \mathcal{I}_n} r_{mj}^{(n)} \hat{\mathbf{E}}_m / \sum_{m \in \mathcal{I}_n} r_{mj}^{(n)}, \quad f_{nj} = \sum_{m \in \mathcal{I}_n} r_{mj}^{(n)} s_m / \sum_{m \in \mathcal{I}_n} r_{mj}^{(n)}$$

其中 $r_{mj}^{(n)}$ 为二元指示变量，表示第 $n$ 个分数桶内的样本 $m$ 是否分配到聚类中心 $j$。分桶策略确保不同质量等级的图像不会在聚类中混淆，去除该模块后平均PLCC从0.798降至0.785（Table 4, Case 3 vs. Case 6）。

**（3）评分定义与微调（Scoring Definition）**：最终评分通过softmax加权的余弦相似度计算：

$$w_i = \frac{\exp(\cos<\mathbf{U}^\top \mathcal{E}_{align}(\mathbf{I}), \mu_i>)}{\sum_{j=1}^K \exp(\cos<\mathbf{U}^\top \mathcal{E}_{align}(\mathbf{I}), \mu_j>)}, \quad \hat{f} = \sum_{i=1}^K w_i f_i$$

该模块端到端优化基向量 $\mu_i$ 和分数 $f_i$，使得加权求和结果逼近人工评分。去除评分微调后平均PLCC从0.798骤降至0.743（Table 4, Case 5 vs. Case 6），是所有消融中损失最大的组件，证明端到端拟合的必要性。

### 4. 效率与泛化的双重突破

RALI的核心创新产生了两个关键结果：

- **参数效率**：RALI仅使用Q-Insight约4%的参数量，达到可比的跨数据集评分精度（平均PLCC: RALI 0.798 vs. Q-Insight 0.806, Table 2），推理时间仅为后者的3.4%，内存占用为14.7%（Figure 6）。
- **跨域泛化**：在四数据集混合训练场景下，RALI的跨域变体RACT（Reasoning-Aligned Cross-Domain Training）达到平均PLCC 0.855，显著优于Q-Insight混合训练的0.791（Table A.2），提升+0.064。

值得注意的是，跨域SFT的消融实验（Table 5）揭示了一个重要发现：仅使用文本标签（无分数）微调视觉编码器，即可达到与同时使用文本+分数标签相近的跨域性能。这表明**推理文本对齐本身已足够支撑跨域泛化**，分数标签携带的标注者偏置反而可能干扰泛化能力。



![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_DkHt2K1g2Y/figures/006_Figure_5.jpg]]
*Figure 5: Illustration of the proposed reasoning-aligned lightweight IQA (RALI) framework. (a) presents the components and functions of the RL-based IQA model. (b)–(d) jointly constitute our lightweight RALI scheme, including contrastive learning with quality reasoning text, feature compression, and score definition. The model’s inference pipeline is identical to (d)*

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_DkHt2K1g2Y/figures/003_Figure_3.jpg]]
*Figure 3: 0Figure 3: Attention heatmap during score-token generation of Q-Insight. It primarily attends to reasoning text tokens instead of visual tokens (95% vs. 5%)*

### 问题定位与核心洞察

传统无参考图像质量评估（NR-IQA）方法依赖高维视觉表征（如CLIP特征或ViT编码），容易在不同数据集的分布间过拟合。近期基于强化学习（RL）的多模态大语言模型（MLLM）方法——如 **Q-Insight**（Li et al., 2025）——通过将图像评分过程转化为逐步推理，实现了显著的跨域泛化能力。然而，这种泛化能力的来源及其必要性此前并未得到系统审视。

本文的核心洞察是：**RL使MLLM学得的推理本质上是一种从视觉到文本的跨域对齐压缩**。具体而言，推理模型在生成评分token时，95%的注意力权重集中在先前生成的推理文本token上（Figure 3），而非原始的视觉token——这意味着评分决策几乎完全依赖经过压缩的文本表征，而非高维视觉特征。这一压缩过程将超过1000个视觉token的信息凝练为不足100个文本token，同时显著缩小了不同数据域之间的表征差距（Figure 4）。由此引出的关键问题是：**能否绕过显式的推理过程，直接复现这种从视觉到文本的对齐压缩？**

### RALI 框架总览

基于上述洞察，本文提出 **RALI（Reasoning-Aligned Lightweight IQA）** 框架，其核心设计思路是：利用对比学习直接将图像映射到RL推理模型学得的文本表征空间，从而在不加载LLM、不执行推理过程的前提下，获得与推理模型可比的泛化能力。Figure 5 展示了RALI的整体架构，包含三个顺序模块：

1. **对比对齐（Contrastive Alignment）**：利用CLIP损失微调视觉编码器，使其输出与RL模型生成的质量推理文本嵌入对齐。
2. **特征压缩（Feature Compression）**：通过PCA降维和分桶K-Means聚类，将高维对齐特征压缩为紧凑的基向量集合。
3. **评分定义与微调（Scoring Definition）**：端到端优化基向量及其对应的代表分数，使最终评分由图像嵌入与基向量的余弦相似度加权求和得到。

### 模块一：对比对齐

该模块的目标是让视觉编码器学会输出与质量推理文本语义一致的嵌入。具体做法是：使用RL推理模型（Q-Insight）对训练集图像生成推理文本（位于 `<think>` 和 `</think>` 标签之间），然后以这些文本作为正样本，以同一批次内的其他图像推理文本作为负样本，通过CLIP风格的对比损失微调视觉编码器 $\mathcal{E}_{align}$。这一过程使视觉编码器的输出空间与质量推理的文本空间对齐，从而隐式继承了推理模型的跨域泛化特性。

消融实验表明，去除对比对齐后，平均PLCC从0.798骤降至0.748（Table 4，Case 1 vs. Case 6），证实了对齐到质量文本空间是整个框架的基石。

### 模块二：特征压缩

对齐后的视觉嵌入维度较高（CLIP-ViT-L/14输出768维），直接用于评分计算效率较低。特征压缩模块通过两步操作将其转化为紧凑的基向量集合：

**第一步：PCA降维。** 将对齐嵌入从768维降至512维，保留主要信息的同时减少计算量。

**第二步：分桶K-Means聚类。** 将训练集样本按质量分数等距划分为 $N$ 个桶（$N=240$），在每个桶 $n$ 内独立执行K-Means聚类，得到 $k_n$ 个聚类中心。聚类中心的分配由以下指示函数定义：

$$r_{mj}^{(n)} = \mathbf{1}\Big[ j = \mathrm{argmin}_{j' \in \{1,...,k_n\}} \|\hat{\mathbf{E}}_m - \mu_{nj'}\|_2^2 \Big], \quad m \in \mathcal{I}_n$$

其中 $\hat{\mathbf{E}}_m$ 为样本 $m$ 的PCA降维后嵌入，$\mu_{nj'}$ 为桶 $n$ 内第 $j'$ 个聚类中心。

聚类完成后，每个聚类中心 $\mu_{nj}$ 及其代表分数 $f_{nj}$ 由桶内分配样本的均值和分数均值确定：

$$\mu_{nj} = \sum_{m \in \mathcal{I}_n} r_{mj}^{(n)} \hat{\mathbf{E}}_m / \sum_{m \in \mathcal{I}_n} r_{mj}^{(n)}, \quad f_{nj} = \sum_{m \in \mathcal{I}_n} r_{mj}^{(n)} s_m / \sum_{m \in \mathcal{I}_n} r_{mj}^{(n)}$$

所有桶的聚类中心汇总后得到 $K$ 个基向量（$K=250$）及其对应分数，构成紧凑的“质量码本”。

消融实验表明，去除分桶K-Means后平均PLCC从0.798降至0.785（Table 4，Case 3 vs. Case 6），说明聚类结构化表征有助于评分精度。

### 模块三：评分定义与微调

推理阶段，给定输入图像 $\mathbf{I}$，首先通过对齐编码器提取嵌入 $\mathcal{E}_{align}(\mathbf{I})$，经PCA投影矩阵 $\mathbf{U}^\top$ 降维后，计算其与 $K$ 个基向量 $\mu_i$ 的余弦相似度，通过softmax归一化得到权重：

$$w_i = \frac{\exp(\cos<\mathbf{U}^\top \mathcal{E}_{align}(\mathbf{I}), \mu_i>)}{\sum_{j=1}^K \exp(\cos<\mathbf{U}^\top \mathcal{E}_{align}(\mathbf{I}), \mu_j>)}$$

最终预测分数为基分数的加权求和：

$$\hat{f} = \sum_{i=1}^K w_i f_i$$

在训练阶段，基向量 $\mu_i$ 和基分数 $f_i$ 作为可学习参数进行端到端优化，通过MSE损失拟合人工评分。消融实验表明，去除评分微调后平均PLCC从0.798骤降至0.743（Table 4，Case 5 vs. Case 6），是所有组件中损失最大的，证明端到端拟合的必要性。

### 跨域训练扩展：RACT

为充分利用多个IQA数据集进行训练，本文进一步提出 **RACT（Reasoning-Aligned Cross-Domain Training）** 框架，其流程如Figure A.1所示，包含三个阶段：

1. **单域RL训练**：在每个IQA数据集上独立训练RL推理模型，使其学会生成数据集特定的质量推理文本。
2. **标签对齐**：利用训练好的推理模块为所有图像生成统一的推理文本，消除不同数据集标注偏置对文本表征的影响。
3. **跨域SFT**：以对齐后的推理文本为监督信号，对视觉编码器进行跨数据集监督微调。

实验表明，跨域SFT仅使用文本标签（不使用分数）即可达到与同时使用文本+分数相近的性能（Table 5），且仅微调视觉编码器（VE）即可获得与联合微调VE和LLM相当的效果，进一步证实了推理文本对齐已足以实现跨域泛化。

### 输入输出流总结

**训练阶段：**
- 输入：训练图像 + RL模型生成的推理文本 + 人工质量评分
- 流程：对比对齐（图像→文本空间）→ PCA降维 → 分桶K-Means聚类 → 评分定义模块端到端优化
- 输出：对齐编码器 $\mathcal{E}_{align}$、PCA投影矩阵 $\mathbf{U}^\top$、$K$ 个基向量 $\{\mu_i\}$ 及基分数 $\{f_i\}$

**推理阶段：**
- 输入：单张测试图像
- 流程：$\mathcal{E}_{align}$ 提取嵌入 → $\mathbf{U}^\top$ 降维 → 与基向量计算余弦相似度 → softmax加权求和基分数
- 输出：预测质量分数 $\hat{f}$

整个推理过程不涉及任何LLM加载或文本生成，仅需执行视觉编码器前向传播和轻量级向量运算。这使得RALI在batch size=16时仅消耗Q-Insight约14.7%的显存和3.4%的推理时间（Figure 6），同时保持可比的评分精度（Table 2，平均PLCC 0.798 vs. 0.806）。



### 特征压缩：PCA降维与分桶K-Means聚类

经对比对齐后的图像嵌入首先通过PCA从原始768维降至512维，随后进入分桶K-Means聚类阶段。该阶段的核心思想是：将训练样本按质量分数划分为多个桶（buckets），在每个桶内独立执行K-Means聚类，从而在保留分数结构的前提下构建紧凑的基向量集合。

设第 $n$ 个分数桶内的样本索引集合为 $\mathcal{I}_n$，其PCA降维后的特征为 $\hat{\mathbf{E}}_m$。聚类分配通过最小化样本到聚类中心的欧氏距离完成：

$$r_{mj}^{(n)} = \mathbf{1}\Big[ j = \mathrm{argmin}_{j' \in \{1,...,k_n\}} \|\hat{\mathbf{E}}_m - \mu_{nj'}\|_2^2 \Big], \quad m \in \mathcal{I}_n$$

其中 $r_{mj}^{(n)}$ 为二元指示变量，表示样本 $m$ 是否被分配到桶 $n$ 内的第 $j$ 个聚类。随后，聚类中心 $\mu_{nj}$ 和该簇的代表性分数 $f_{nj}$ 分别由分配样本的均值和分数均值更新：

$$\mu_{nj} = \sum_{m \in \mathcal{I}_n} r_{mj}^{(n)} \hat{\mathbf{E}}_m / \sum_{m \in \mathcal{I}_n} r_{mj}^{(n)}, \quad f_{nj} = \sum_{m \in \mathcal{I}_n} r_{mj}^{(n)} s_m / \sum_{m \in \mathcal{I}_n} r_{mj}^{(n)}$$

所有桶的聚类结果被聚合为一个包含 $K$ 个基向量 $\{\mu_i\}_{i=1}^K$ 和对应基分数 $\{f_i\}_{i=1}^K$ 的紧凑特征空间。这一分桶策略的消融实验表明，去除分桶K-Means后平均PLCC从0.798降至0.785（Table 4, Case 3 vs. Case 6），证实了保留分数结构对评分精度的贡献。

### 评分定义：Softmax加权求和

推理阶段，给定输入图像 $\mathbf{I}$，首先通过对齐编码器 $\mathcal{E}_{align}$ 提取嵌入，再经投影矩阵 $\mathbf{U}^\top$ 映射到基向量空间。最终预测分数 $\hat{f}$ 通过计算图像嵌入与各基向量的余弦相似度，经softmax归一化后作为权重，对所有基分数进行加权求和得到：

$$w_i = \frac{\exp(\cos<\mathbf{U}^\top \mathcal{E}_{align}(\mathbf{I}), \mu_i>)}{\sum_{j=1}^K \exp(\cos<\mathbf{U}^\top \mathcal{E}_{align}(\mathbf{I}), \mu_j>)}, \quad \hat{f} = \sum_{i=1}^K w_i f_i$$

该公式的物理含义是：图像质量评分被解耦为 $K$ 个基分数的软组合，每个基分数代表特征空间中某个局部区域的质量水平。权重 $w_i$ 反映了图像嵌入与各基向量的语义相似度，相似度越高则对应基分数的贡献越大。整个评分模块（基向量 $\mu_i$ 和基分数 $f_i$）在训练阶段端到端优化，使预测分数逼近人工标注。消融实验显示，去除评分微调后平均PLCC从0.798骤降至0.743（Table 4, Case 5 vs. Case 6），损失在所有组件中最大，证明端到端拟合对性能至关重要。



## 实验与关键发现

### 核心实验设置

所有单域实验以 **KonIQ** 数据集为训练集，在七个标准 IQA 数据集上评估 PLCC 和 SRCC。跨域实验则混合 **KonIQ、SPAQ、KADID、PIPAL** 四个数据集进行训练。RALI 采用 CLIP-ViT-L/14 作为视觉编码器，经 PCA 将特征维度从 768 降至 512，分桶 K-Means 的基向量数和桶数分别设为 250 和 240。Q-Insight 的 GRPO 训练中每步采样 N=8 个候选，KL 正则系数 β=1×10⁻³。

### 主结果：单域评分回归

Table 2 展示了各方法在 KonIQ 单域训练下的跨数据集泛化性能。RALI 在七个数据集上的平均 PLCC 达到 **0.798**，仅比基于 RL 的 MLLM 方法 Q-Insight（0.806）低 0.008，却仅使用其约 4% 的参数量。在所有非 MLLM 深度学习方法中，RALI 取得最高平均 PLCC/SRCC，较 CLIP-IQA+ 分别提升 0.056 和 0.059。值得注意的是，RALI 在 SPAQ（0.897）、LiveW（0.896）和 CSIQ（0.828）等域外数据集上表现尤为突出，证明其继承了 RL 推理模型的跨域泛化能力。


![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_DkHt2K1g2Y/figures/007_Table_2.jpg]]
*Table 2: PLCC / SRCC comparison on the single-domain score regression tasks between RALI and other competitive IQA methods. All methods except handcrafted ones are trained on the KonIQ dataset. The best and second-best results of each test setting are highlighted in bold red and underlined blue*

### 主结果：跨域评分回归

Table 3 展示了 RACT 框架在四数据集混合训练下的表现。RACT 在域内平均 PLCC 达 0.853，域外平均 PLCC 达 0.858，在所有 MLLM 方法中均取得最优。相比之下，直接将 Q-Insight 应用于混合数据集会出现严重的收敛问题，而 VisualQuality-R1 在 KonIQ 上的 PLCC 较单独训练下降了 0.024。这验证了 RACT 的“独立 RL 训练→推理文本对齐→跨域 SFT”三阶段策略能有效解决多数据集标注偏置导致的训练冲突。

### 消融实验：RALI 组件贡献

Table 4 系统验证了 RALI 各关键组件的贡献（以 Case 6 完整配置为基准，平均 PLCC=0.798）：


![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_DkHt2K1g2Y/figures/009_Table_4.jpg]]
*Table 4: Ablation studies on the key components of RALI. It can be observed that alignment to descriptions and scoring definition based on basis vectors with scores significantly enhance the performance of our method*

- **去除对比对齐**（Case 1）：平均 PLCC 骤降至 0.748（-0.050），损失最大，证实将视觉特征对齐到质量推理文本空间是整个框架的核心。
- **去除评分定义微调**（Case 5）：平均 PLCC 降至 0.743（-0.055），表明端到端优化基向量分数对拟合人工评分至关重要。
- **去除分桶 K-Means**（Case 3）：平均 PLCC 降至 0.785（-0.013），说明按分数桶分别聚类能更好地保留质量相关的结构化信息。
- **去除 PCA 降维**（Case 2）：平均 PLCC 降至 0.777（-0.021），降维有助于去除噪声并提升特征判别性。
- **去除种子增强**（Case 4）：平均 PLCC 降至 0.788（-0.010），影响相对较小但仍有贡献。

### 消融实验：推理能力与泛化

Table A.1 直接验证了推理对泛化的因果作用：禁用 Q-Insight 的推理能力后，其平均 PLCC 从 0.806 降至 0.768（-0.038），降幅显著。这证实了 RL 学得的推理过程——而非模型规模或训练策略——是实现跨域泛化的决定性因素。

### 消融实验：跨域 SFT 的标签与模块

Table 5 分析了 RACT 跨域 SFT 阶段中标签类型和训练模块的影响。关键发现：
- **分数标签对域外泛化无增益**：仅使用文本标签（无分数）训练与同时使用文本+分数训练，域外性能相当。原因是跨数据集标注携带标注者主观偏置，文本保留了客观质量描述，而分数引入了主观偏差。
- **仅微调视觉编码器即足够**：单独训练视觉编码器与联合训练 LLM 的跨域性能相当。这与前文结论一致——单数据集学得的推理过程本身具有泛化性，跨域训练只需让视觉编码器适配不同域的图像输入。

### 效率对比

Figure 6 展示了 RALI 与 Q-Insight 在推理效率上的巨大差距。在 batch size=16 的设置下，RALI 的显存占用仅为 Q-Insight 的 **14.7%**，推理时间仅为其 **3.4%**。这一效率优势源于 RALI 完全摒弃了 LLM 的加载与自回归解码，仅需一次视觉编码前向传播和轻量级余弦相似度计算。

### 跨域训练的一致性验证

Table 1 验证了推理过程的跨域一致性：在 KonIQ 和 KADID 上分别训练的 Q-Insight，其 LLM 推理模块在域外数据集（CSIQ、LiveW）上的 PLCC 差异小于 0.01。这表明 RL 学得的推理策略高度一致，不依赖于特定训练数据的分布，为 RALI 的“对齐即可泛化”提供了直接证据。

### 失败模式与局限性

1. **视觉编码器容量瓶颈**：RALI 的性能上限受 CLIP-ViT-L/14 编码器限制。Table A.6 显示，即使将 Q-Insight 参数减半（3B 版本），其平均 PLCC 仍低于 RALI，但若采用更强的编码器（如 SigLIP），RALI 可能进一步缩小与完整 Q-Insight 的差距。
2. **复杂场景未验证**：当前实验集中于自然图像质量评估，尚未在视频 IQA 和 AIGC 评价任务上验证方法的可扩展性。
3. **极端缺陷的泛化边界**：面对极其复杂的复合质量缺陷时，轻量对齐方法是否仍能保持与显式推理同等的泛化能力，尚需进一步探索。

### 补充图表

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_DkHt2K1g2Y/figures/001_Figure_1.jpg]]
*Figure 1: Performance comparison among IQA methods in PLCC/SRCC and parameter numbers. RALI uses only about 4% of Q-Insight’s (Li et al. (2025)) parameters while achieving comparable accuracy*

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_DkHt2K1g2Y/figures/012_Table_6.jpg]]
*Table 6: Table A.1: PLCC / SRCC comparison of different training strategies. Q-Insight with the reasoning capability disabled exhibits a significant performance drop*




## 定位与知识库关联

### 1. 核心问题与因果机制

传统图像质量评估（IQA）方法面临的核心瓶颈是视觉表征的高维性与数据集分布间的过拟合。基于强化学习（RL）的多模态大语言模型（MLLM）方法（如 Q-Insight）通过将图像质量评分从依赖超过1000个视觉 token 压缩为不到100个文本推理 token，实现了显著的跨域泛化能力。然而，这种推理过程引入了巨大的计算开销。

本文的核心发现是：**RL 使 MLLM 学得的推理本质上是一种从视觉到文本的跨域对齐压缩**，该压缩可通过对比学习直接复现，无需实际推理过程即可获得同等泛化。因果调节变量是“是否将图像质量评分的依赖从视觉 token 转移到质量推理文本 token”。

### 2. 方法谱系定位

#### 2.1 上游继承：RL-based MLLM for IQA

本工作直接建立在基于强化学习的 MLLM-IQA 方法之上，尤其是 **Q-Insight**（Li et al., 2025）。Q-Insight 通过 GRPO 强化学习训练 MLLM，使其在输出评分前生成质量推理文本（`<think>...</think>`），再输出分数（`<answer>...</answer>`）。本文通过三项关键证据揭示了 Q-Insight 泛化能力的来源：

- **注意力机制证据**：在生成评分 token 时，95% 的注意力权重集中在先前生成的推理文本 token 上（Figure 3），证明推理模型主要通过文本表征进行评分。
- **跨域一致性证据**：在不同数据集（KonIQ、KADID）上训练的 LLM 推理模块在域外数据集（CSIQ、LiveW）上表现高度一致，PLCC 差异 < 0.01（Table 1），表明推理过程本身具有跨域泛化性。
- **推理必要性证据**：禁用推理能力后，Q-Insight 的平均 PLCC 从 0.806 骤降至 0.768（Table A.1），直接证实推理是实现泛化的关键。

其他基于 SFT 的 MLLM-IQA 方法包括 **Q-Align**（Wu et al., 2024b）、**DeQA-Score**（You et al., 2025），以及基于 RL 的排序方法 **VisualQuality-R1**（Wu et al., 2025b）。这些方法均需在推理时加载完整 LLM，计算成本高。

#### 2.2 横向对比：轻量级 IQA 方法

在轻量级 IQA 领域，代表性方法包括：

- **CLIP-IQA+**（Wang et al., 2023）：基于 CLIP 的无参考 IQA，直接使用视觉-语言对齐特征进行评分，但缺乏对质量推理文本空间的显式对齐。
- **C2Score**（Zhu et al., 2024）：基于排序的 IQA 方法。
- **NIQE**（Mittal et al., 2012b）、**BRISQUE**（Mittal et al., 2012a）：基于手工特征的经典无参考 IQA。

RALI 与上述方法的本质区别在于：它通过对比学习将视觉编码器输出显式对齐到 RL 模型学得的**质量推理文本空间**，而非通用的视觉-语言空间或手工特征空间。

#### 2.3 下游拓展：跨域训练框架 RACT

本文进一步提出了 **Reasoning-Aligned Cross-Domain Training (RACT)** 框架，解决多数据集混合训练时的标注偏置问题。RACT 包含三个阶段：
1. 在每个 IQA 数据集上独立进行单域 RL 训练；
2. 利用推理模块生成图像质量推理文本，实现标签对齐；
3. 跨域 SFT，仅微调视觉编码器（VE），因为单数据集学得的推理已具有泛化性。

实验表明，仅使用文本标签（无分数）微调 VE 即可达到与同时使用文本+分数相近的跨域性能（Table 5），进一步验证了推理文本对齐的充分性。

### 3. 方法边界与局限

1. **视觉编码器容量上限**：RALI 的性能受底层 CLIP 视觉编码器（CLIP-ViT-L/14）容量的限制，尚未尝试更强的编码器（如 SigLIP）。在极其复杂的质量缺陷场景下，轻量对齐方法能否保持与完整推理模型同等的泛化能力，仍有待验证。

2. **模态扩展性未验证**：当前实验主要集中于自然图像质量评估，尚未在视频 IQA 和 AI 生成内容（AIGC）评价任务上验证方法的可扩展性。视频场景可能需要额外的时序对齐设计，AIGC 场景的质量维度与自然图像存在差异。

3. **静态对齐机制**：RALI 采用固定的对比对齐和分桶 K-Means 聚类，缺乏根据图像内容难度自适应调整的能力。能否设计动态机制，在简单样本上跳过推理、复杂样本上调用推理，进一步平衡精度与效率，是一个开放问题。

### 4. 开放问题

1. **推理的不可替代性边界**：推理过程是否在所有图像质量维度上都不再必要？面对极其复杂的质量缺陷（如混合失真、语义级伪影）时，轻量对齐方法是否仍能保持同等泛化？

2. **跨模态迁移**：将 RALI 的思想迁移到视频 IQA 和 AIGC 评价任务中，是否需要额外的时序/结构对齐设计？推理文本空间的压缩特性是否在不同模态中保持一致？

3. **自适应推理调度**：能否设计一种动态机制，根据图像内容难度自适应地选择是否调用推理，从而在保证精度的前提下最大化效率？



## 原文 PDF

![[paperPDFs/ICLR_2026/Reasoning_as_Representation_Rethinking_Visual_Reinforcement_Learning_in_Image_Quality_Assessment.pdf]]
