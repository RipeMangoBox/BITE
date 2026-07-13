---
title: "Adversarial Encoding Perturbation and Synthesis for Set Representation Auxiliary Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Adversarial_Encoding_Perturbation_and_Synthesis_for_Set_Representation_Auxiliary_Learning.pdf
project_link: null
code_link: null
aliases:
- SSRAL
- AEPSSRAL
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "SRAL用2-Sliced-Wasserstein集合编码和特征级对抗扰动来学习鲁棒的集合间分布表示。"
primary_logic: "集合先与可学习参考分布比较得到嵌入，再通过对抗InfoNCE辅助目标强化集合间相关性。"
claims:
- "将集合视为经验分布能显式建模传统池化方法忽略的集合间差异。"
- "对抗性编码扰动迫使编码器学习对最坏情况特征变化稳健的集合表示。"
- "SRAL在集合相似性、捆绑推荐、点云分类和主题集扩展任务中优于多类基线。"
---

# Adversarial Encoding Perturbation and Synthesis for Set Representation Auxiliary Learning

> [!tip] 核心洞察
> 将集合视为高维分布，利用2-Sliced-Wasserstein距离度量分布差异，并通过理论证明对抗性扰动目标在期望上等价于优化集合间的Wasserstein距离，从而迫使编码器学习到能够捕捉细粒度集合间相关性的表示。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向集合表示辅助学习的对抗性编码扰动与合成 |
| 英文题名 | Adversarial Encoding Perturbation and Synthesis for Set Representation Auxiliary Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=13r06yROEZ) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | SRAL (Set Representation Auxiliary Learning) |
| Dataset | Friendster (Task 1: Set Similarity Learning), LIVEJ (Task 1: Set Similarity Learning), Youshu (Task 2: Bundle Recommendation) |

> [!tip] 效果简介
> - Friendster (Task 1: Set Similarity Learning) 上，Recall@20 为 91.57 ± 0.22，对比 最佳基线约83.6，变化 +9.56%*。
> - Friendster (Task 1: Set Similarity Learning) 上，NDCG@20 为 92.22 ± 0.22，对比 最佳基线约84.4，变化 +9.28%*。
> - LIVEJ (Task 1: Set Similarity Learning) 上，Recall@20 为 89.31 ± 0.31，对比 最佳基线约82.5，变化 +8.26%*。

## 概要

本文提出 **SRAL (Set Representation Auxiliary Learning)** 框架，旨在通过显式建模集合间（inter-set）相关性来提升集合表示的质量。SRAL 将集合视为高维分布，利用 **2-Sliced-Wasserstein 距离** 度量分布差异，并引入对抗性辅助学习机制，在特征层面施加最坏情况扰动，迫使模型学习高判别性的鲁棒表示。理论分析表明，对抗性目标在期望上等价于优化集合间的 Wasserstein 距离。在四个下游任务（集合相似性排序、捆绑推荐、点云分类、主题集扩展）上的实验表明，SRAL 显著优于现有方法，例如在 Friendster 数据集上 Recall@20 达到 91.57，相比最佳基线提升 9.56%。



现有集合表示学习方法主要关注集合内部（intra-set）的置换不变性和基数独立性，缺乏对集合间（inter-set）相关性的显式建模。这导致在需要细粒度集合比较的下游任务（如集合检索、捆绑推荐）中表示能力不足。传统方法如 DeepSet (Zaheer et al., 2017) 和 RepSet (Skianis et al., 2020) 虽然能有效处理集合内部结构，但未能充分利用集合之间的分布差异信息。SRAL 的核心动机是：通过将集合视为分布并度量其差异，结合对抗性学习，迫使编码器学习到能够捕捉细粒度集合间相关性的表示。



## 核心方法与创新机理

SRAL 的核心创新体现在三个关键设计变更上：

| 变更维度 | 基线方法 | SRAL 方案 | 证据锚点 |
|---------|---------|-----------|---------|
| **集合编码方式** | 元素特征求和/平均/最大池化，或基于自注意力的聚合 | 基于 2-Sliced-Wasserstein 距离的分布差异编码，将集合视为经验分布并计算与可学习参考分布的距离 | Section 3.2: our encoder leverages the distributional distance between an input set and a learnable reference distribution O |
| **数据增强/扰动策略** | 元素丢弃/添加或子集采样等输入级操作 | 在特征层面引入对抗性扰动，通过最小-最大优化生成最坏情况扰动 | Section 3.3.1: z_{i,k}' = z_{i,k} + ε_{i,k}', where ε_{i,k}' is drawn from \|\|ε\|\|_2 ≤ π (Eq. 7) |
| **辅助学习目标** | 无显式集合间相关性建模的辅助目标 | 基于 InfoNCE 的自监督对比损失，其期望等价于 2-Sliced-Wasserstein 距离 | Section 3.3.2: L_wd = Σ_{S_i∈S} -log( exp(-||v_i' - v_i''||_2/ψ) / Σ_{S_j∈S} exp(-||v_i' - v_j''||_2/ψ) ) (Eq. 8) |



![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_13r06yROEZ_Adversa/figures/001_Figure_1.jpg]]
*Figure 1: SRAL captures inter-set correlations for adversarial optimization (left); normalized ratiosFigure 1: SRAL captures inter-set correlations for adversarial optimization (left); normalized ratios of second-best methods over SRAL are reported due to varying metric scales (right).of second-best methods over SRAL are reported due to varying metric scales (right).*

SRAL 的整体目标函数为：

$$L = L_{\mathrm{Main}} + \lambda_1 L_{\mathrm{Aux}} + \lambda_2 \|\Xi\|_2^2 \quad \text{(Eq. 3)}$$

其中 $L_{\mathrm{Main}}$ 是与具体下游任务相关的主损失函数，$L_{\mathrm{Aux}}$ 是对抗性辅助损失，$\lambda_1$ 和 $\lambda_2$ 是平衡超参数。框架由三个核心模块组成：

1. **Set Feature Encoder (SFE)**：基于 2-Sliced-Wasserstein 距离的集合编码器，将输入集合映射为固定大小的嵌入向量。
2. **Adversarial Encoding Perturbation and Optimization (AEPO)**：对抗性编码扰动与优化模块，生成最坏情况扰动并优化模型鲁棒性。
3. **Main Task Loss**：与具体下游任务相关的主损失函数（如排序损失、分类损失等）。



### 5.1 预备知识：Wasserstein 距离

**α-Wasserstein 距离** (Eq. 1)：
$$D_\alpha(P,Q) = \left( \operatorname*{inf}_{g \in \operatorname{Plans}(P,Q)} \int \|x - g(x)\|^\alpha dP(x) \right)^{\frac{1}{\alpha}}, \alpha \geq 1$$

**α-Sliced-Wasserstein 距离** (Eq. 2)：
$$SD_\alpha(P,Q) = \left( \int_{\mathbb{S}^{d-1}} \left( D_\alpha(P^\theta, Q^\theta) \right)^\alpha d\theta \right)^{\frac{1}{\alpha}}, \alpha \geq 1$$

### 5.2 Set Feature Encoder (SFE)

SFE 模块的核心思想是将输入集合 $S_i$ 视为经验分布 $P_i$，并与一个可学习的参考分布 $O$ 进行比较。通过 2-Sliced-Wasserstein 距离，SFE 能够捕捉集合间的分布差异。

**最优传输映射（切片分布）** (Eq. 4)：
$$g^+(x^\theta | V_i^\theta) = F_{P_i^\theta}^{-1}(F_{O^\theta}(x^\theta))$$

**实际排名匹配实现** (Eq. 5)：
$$g^+(x^\theta | V_i^\theta) = \arg\min_{x' \in V_i^\theta} \left( \tau(x' | V_i^\theta) \geq \frac{|S_i|}{H} \cdot \tau(x^\theta | V_O^\theta) \right)$$

**SFE 模块输出** (Eq. 6)：
$$SFE(V_i, V_O | \Theta) = \operatorname{Concat}_{r=1\dots R; h=1\dots H} \left( g^+(w_r^\top z_h | V_i^{\theta_r}) \right)$$

### 5.3 Adversarial Encoding Perturbation and Optimization (AEPO)

AEPO 模块在特征层面引入对抗性扰动，通过最小-最大优化迫使模型学习鲁棒表示。

**扰动后的元素嵌入** (Eq. 7)：
$$z_{i,k}' = z_{i,k} + \epsilon_{i,k}', \quad \|\epsilon\|_2 \le \pi$$

**InfoNCE 损失（集合嵌入）** (Eq. 8)：
$$L_{wd} = \sum_{S_i \in \mathcal{S}} -\log \frac{\exp(-\|v_i' - v_i''\|_2 / \psi)}{\sum_{S_j \in \mathcal{S}} \exp(-\|v_i' - v_j''\|_2 / \psi)}$$

**Remark 1 等价性** (Eq. 9)：
$$\mathbb{E}\left[ \frac{\exp(-\|v_i' - v_i''\|_2 / \psi)}{\sum_{S_j \in \mathcal{S}} \exp(-\|v_i' - v_j''\|_2 / \psi)} \right] = \frac{\exp(-\|SD_2(P_i', P_i'')\|_2 / \psi)}{\sum_{S_j \in \mathcal{S}} \exp(-\|SD_2(P_i', P_j'')\|_2 / \psi)}$$

**对抗性辅助损失** (Eq. 10)：
$$L_{\mathrm{Aux}} = \max_{\|\sigma\|_2 \leq \pi} L_{wd}(\Xi, \sigma)$$

**扰动半径裁剪** (Eq. 13)：
$$\sigma = \boldsymbol{\hat{\sigma}} \cdot \operatorname{min}\left(1, \frac{\pi}{\lVert \boldsymbol{\hat{\sigma}} \rVert_2}\right)$$

**参数更新规则** (Eq. 14)：
$$\Xi \leftarrow \Xi - \beta \cdot \nabla_\Xi \left( L_{\mathrm{Main}} + \lambda_1 L_{\mathrm{adv}} + \lambda_2 \|\Xi\|_2^2 \right)$$



## 实验与关键发现

### 6.1 主要结果

SRAL 在四个下游任务上进行了评估，与 14 种基线方法进行了对比。所有实验均使用 Wilcoxon 符号秩检验（p < 0.05）验证统计显著性。

**任务 1：集合相似性学习（Set Similarity Learning）**

| 数据集 | 指标 | SRAL | 最佳基线 | 提升幅度 |
|-------|------|------|---------|---------|
| Friendster | Recall@20 | 91.57 ± 0.22 | ~83.6 | +9.56%* |
| Friendster | NDCG@20 | 92.22 ± 0.22 | ~84.4 | +9.28%* |
| LIVEJ | Recall@20 | 89.31 ± 0.31 | ~82.5 | +8.26%* |

**任务 2：捆绑推荐（Bundle Recommendation）**

| 数据集 | 指标 | SRAL+ | 最佳基线 | 提升幅度 |
|-------|------|-------|---------|---------|
| Youshu | Recall@20 | 26.92 ± 0.09 | ~26.4 | +1.93%* |
| NetEase | Recall@20 | 30.87 ± 0.11 | ~30.2 | +2.22%* |

**任务 3：点云分类（Point Cloud Processing）**

| 骨干网络 | SRAL | FSW | 提升幅度 |
|---------|------|-----|---------|
| ISAB | 87.31 | 86.93 | +0.44%* |

**任务 4：主题集扩展（Topic Set Expansion）**

| 数据集 | SRAL AUC (%) | 最佳基线 AUC (%) | 提升幅度 |
|-------|-------------|-----------------|---------|
| LDA-1k | 80.94 ± 1.38 | 75.67 | +6.96%* |
| LDA-3k | 87.93 ± 1.92 | 79.67 | +10.37%* |
| LDA-5k | 86.20 ± 0.67 | 80.94 | +6.50%* |

### 6.2 消融实验

消融实验结果（Table 4）揭示了各模块的关键贡献：


![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_13r06yROEZ_Adversa/figures/012_Table_4.jpg]]
*Table 4: Ablation study.*

- **去除 SFE 模块**（替换为平均池化）导致 Task 1 的 Recall@20 下降 26.81%。
- **去除 AEPO 模块**（替换为随机噪声）导致 Task 4 的 AUC 下降 24.70%。
- 使用元素级扰动、集合级扰动或噪声注入等替代方案均不如 SRAL 的对抗性扰动（Figure 4(A)）。
- SRAL 的对抗性辅助学习机制能加速模型收敛并达到更低的损失值（Figure 4(C)）。

### 6.3 公平性说明

- SRAL 在计算效率上略低于部分基线（如 PSWE、FSPool），但总训练时间因收敛加速而保持可比。
- AEPO 模块是计算开销的主要来源（占每 epoch 训练时间的约 59%），但作者认为其带来的收敛加速和性能提升是值得的权衡。
- 将线性插值替换为两层 MLP 进行维度补齐（w/o LI）导致性能下降。

### 补充图表

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_13r06yROEZ_Adversa/figures/003_Table_1.jpg]]
*Table 1: Performance comparison for Tasks 1 (left) and 2 (right). Best and second-best cases are highlighted. Statistically significant improvements (p \< 0.05) are marked with ∗.*

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_13r06yROEZ_Adversa/figures/004_Table_2.jpg]]

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_13r06yROEZ_Adversa/figures/005_Table_2.jpg]]
*Table 2: Performance comparison for Task 3: Point Cloud Processing.*

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_13r06yROEZ_Adversa/figures/006_Table_3.jpg]]
*Table 3: Performance comparison for Task 4: Topic Set Expansion.*




## 定位与知识库关联

SRAL 在集合表示学习领域具有明确的定位：

**与现有方法的关系**：
- **DeepSet (Zaheer et al., 2017)**：SRAL 超越了简单的置换不变聚合，引入了基于最优传输的分布差异编码。
- **RepSet (Skianis et al., 2020)**：SRAL 使用 Sliced-Wasserstein 距离替代了计算成本更高的二分图匹配。
- **FSW (Amir and Dym, 2025)**：SRAL 在 FSW 的傅里叶域方法基础上，引入了对抗性辅助学习机制。
- **PoT (Guo et al., 2021a)**：SRAL 将原型最优传输扩展为可学习的参考分布，并增加了对抗性扰动。

**理论贡献**：
- 证明了对抗性目标在期望上等价于优化 2-Sliced-Wasserstein 距离（Remark 1）。
- 证明了最小-最大优化目标近似等价于对 SFE 局部 Lipschitz 连续性的隐式正则化（Remark 2）。

**局限性**：
- SRAL 的每 epoch 计算成本高于大多数基线方法，主要由于 AEPO 模块的对抗性扰动生成和迭代优化过程。
- AEPO 模块是专门为基于 Sliced-Wasserstein 度量的 SFE 编码器设计的，直接应用于其他编码器（如 RepSet）时效果有限。
- 方法依赖于多个超参数（λ1, λ2, π, ψ, R, H 等），需要针对不同任务进行调优。
- 当前工作未探索在线检索场景下的效率优化（如近似最近邻搜索）。

**开放问题**：
- 如何进一步降低 AEPO 模块的计算开销，使其适用于更大规模的实时应用？
- SRAL 框架能否扩展到其他类型的结构化数据（如图、序列）的表示学习？
- 对抗性扰动与 Sliced-Wasserstein 距离之间的理论联系是否适用于其他距离度量（如最大均值差异 MMD）？
- 如何自动选择最优的超参数（如扰动半径 π、投影数量 R）以减少人工调优成本？



## 原文 PDF

![[paperPDFs/ICLR_2026/Adversarial_Encoding_Perturbation_and_Synthesis_for_Set_Representation_Auxiliary_Learning.pdf]]
