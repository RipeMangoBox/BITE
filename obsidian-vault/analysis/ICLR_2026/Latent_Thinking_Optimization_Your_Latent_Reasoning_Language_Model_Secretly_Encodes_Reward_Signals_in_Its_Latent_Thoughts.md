---
title: "Latent Thinking Optimization: Your Latent Reasoning Language Model Secretly Encodes Reward Signals in Its Latent Thoughts"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Latent_Thinking_Optimization_Your_Latent_Reasoning_Language_Model_Secretly_Encodes_Reward_Signals_in_Its_Latent_Thoughts.pdf
project_link: null
code_link: null
openreview_forum_id: 2jkAk3EP0v
aliases:
- LTOL
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "训练一个轻量级潜在分类器（LRM）预测潜在思维轨迹的正确性，并将其作为奖励信号优化潜在思维分布。"
primary_logic: "正确与错误的潜在思维轨迹在潜在空间中呈现高度可区分的模式，LRM能够可靠地预测正确性，从而通过选择性采样提升推理性能。"
claims:
- "正确与错误思维轨迹在潜在空间中具有不同的几何结构和动态特征。"
- "潜在分类器能够以高ROC-AUC（SVAMP上接近1.0，MBPP上约0.8）预测思维正确性。"
- "LTO算法在多个推理任务上相对于基线和多数投票显著提升正确率。"
- "LRM可以泛化到通用LLM的潜在表示，并展现出跨域迁移能力。"
---

# Latent Thinking Optimization: Your Latent Reasoning Language Model Secretly Encodes Reward Signals in Its Latent Thoughts

> [!tip] 核心洞察
> 正确与错误的潜在思维轨迹在潜在空间中呈现高度可区分的模式，LRM能够可靠地预测正确性，从而通过选择性采样提升推理性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 潜在思维优化：您的潜在推理语言模型在潜在思维中秘密编码奖励信号 |
| 英文题名 | Latent Thinking Optimization: Your Latent Reasoning Language Model Secretly Encodes Reward Signals in Its Latent Thoughts |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=2jkAk3EP0v) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Latent Thinking Optimization (LTO) |
| Dataset | GSM8K, GSM-Symbolic, SVAMP, CommonsenseQA |

> [!tip] 效果简介
> - GSM8K 上，Accuracy 为 0.378，对比 0.326，变化 +0.052。
> - GSM-Symbolic 上，Accuracy 为 0.303，对比 0.265，变化 +0.038。
> - SVAMP 上，Accuracy 为 0.539，对比 0.517，变化 +0.022。

## 概要

**核心问题**：当前基于潜在推理的语言模型（如Huginn、Coconut）在连续潜在空间中执行推理时，其“潜在思维轨迹”完全不可解释且缺乏监督信号。模型可能在潜在空间中产生错误推理，却无法被检测或纠正，这构成了提升推理可靠性的关键瓶颈。

**核心发现**：正确与错误的潜在思维轨迹在潜在空间中呈现高度可区分的模式——正确轨迹更紧凑、收敛，且具有更高的熵和各项异性、更低的有效秩（Figure 1, Figure 2）。基于这一发现，可训练一个轻量级潜在分类器（Latent Reward Model, LRM）来预测潜在思维的正确性，其在SVAMP上的ROC-AUC接近1.0，在MBPP上约0.8（Figure 3）。

**提出方法**：**潜在思维优化（Latent Thinking Optimization, LTO）**，将LRM作为奖励模型，通过带KL正则化的接受-拒绝采样从优化后的分布中筛选更可能正确的潜在思维轨迹，从而在不修改基础模型参数的前提下提升推理质量。

**主要结果**：在Huginn-3.5B上，LTO在GSM8K、GSM-Symbolic、SVAMP、CommonsenseQA、MBPP五个推理基准上一致优于多数投票、自我修正等基线方法（Table 1）。LRM展现出强跨域迁移能力：在数学数据上训练的LRM可直接用于代码推理，反之亦然（Figure 4）。LTO还可泛化至通用LLM（Llama-2、Llama-3、Mistral等），在GSM8K上为Llama-2-7B带来+16.6%的绝对提升（Table 2）。

**方法定位**：LTO属于推理时优化方法，与多数投票（答案级校正）和链式连续思考修正（CoE-R/CoE-C，潜在级启发式校正）形成互补。其核心创新在于首次将潜在空间中的可学习奖励信号引入推理轨迹选择，为潜在推理的可控性开辟了新路径。



大型语言模型在复杂推理任务上的突破，很大程度上得益于推理时计算扩展（test-time compute scaling）。其中，潜在推理语言模型（Latent Reasoning Language Models）通过在连续潜在空间中执行迭代推理步骤，无需生成冗长的自然语言思维链即可进行深度思考，显著降低了推理延迟和计算开销。然而，这一范式面临一个核心瓶颈：**潜在思维过程缺乏可解释性与监督信号**。由于潜在思维以连续向量序列形式存在，我们难以直观理解模型“在想什么”，更无法在推理过程中直接检测并纠正潜在推理错误。当模型产生错误的潜在思维轨迹时，后续的解码步骤将不可避免地输出错误答案。

现有方法主要从两个层面尝试解决这一问题。在**答案层面**，多数投票（Majority Voting, Wang et al., 2023）和基于置信度的自我修正方法（Ren et al., 2023b; Manakul et al., 2023）通过对多次采样的最终答案进行聚合或评估来提升可靠性，但这些方法完全忽略了潜在思维过程本身的质量。在**潜在思维层面**，CoE-R/CoE-C（Wang et al., 2025c）等启发式方法尝试基于潜在表示的某些统计特性进行校正，但缺乏对思维正确性的直接监督信号，校正效果有限。

本文的核心动机源于一个关键观察：**正确与错误的潜在思维轨迹在潜在空间中呈现出高度可区分的模式**。如 Figure 1 所示，通过 PCA 降维可视化可以发现，正确和错误的潜在思维轨迹在几何分布和动态演化上存在显著差异——正确轨迹展现出更稳定的演化方向，而错误轨迹则表现出漂移和波动。进一步的定量分析（Figure 2）表明，正确潜在思维在信息熵、有效秩和各向异性等表示质量指标上均与错误思维呈现系统性差异。这一发现暗示了一个重要可能性：**潜在思维轨迹中隐含地编码了关于答案正确性的奖励信号**。

基于此，本文提出训练一个轻量级潜在分类器（Latent Reward Model, LRM），直接从潜在思维轨迹预测答案正确性，并将其作为奖励信号来优化潜在思维分布。这一思路将潜在推理的改进问题转化为一个“从潜在表示中读取奖励信号并据此重采样”的过程，无需对基础模型进行昂贵的微调，即可实现推理时潜在思维质量的提升。



## 核心方法与创新机理

本文的核心创新在于将**潜在推理轨迹的可区分性**转化为**可操作的优化信号**，从而在不修改基础模型的前提下提升推理质量。具体而言，该方法围绕两个关键的 **changed slots** 展开：

### 1. 奖励信号来源：从语言空间到潜在空间

传统方法依赖语言空间的过程奖励模型（Process Reward Model）或基于置信度的启发式信号来评估推理质量。本文的关键转变在于：**直接在潜在空间中训练一个轻量级分类器（Latent Reward Model，LRM）作为奖励信号来源**。

这一转变的可行性建立在两个关键发现之上：

- **潜在轨迹的可区分性**：正确与错误的潜在思维轨迹在潜在空间中呈现高度可区分的模式。PCA可视化（Figure 1）显示，正确的潜在思维轨迹呈现紧凑、收敛的分布特征，而错误的轨迹则分散且缺乏收敛性。定量分析（Figure 2）进一步表明，正确轨迹具有更高的熵、更低的有效秩和更高的各向异性。
- **分类器的可靠性**：基于上述可区分性，LRM 能够以高精度预测潜在思维的正确性。在 SVAMP 数据集上，ROC-AUC 接近 1.0；在 MBPP 上约 0.8（Figure 3）。这为后续优化提供了可靠的奖励信号。

### 2. 推理阶段策略：从直接采样到基于奖励的接受-拒绝采样

基线方法（如多数投票 Majority Voting）从原始潜在策略中直接采样多个轨迹，然后对答案进行聚合。本文提出的 LTO（Latent Thinking Optimization）将推理阶段的轨迹选择策略替换为**基于 LRM 奖励的接受-拒绝采样**（Algorithm 1），并以 KL 正则化控制分布偏移。

其核心机制如下：

1. **优化目标**：在 KL 正则化约束下，最大化期望奖励（即 LRM 预测的正确性概率）：
   $$\pi ^ { * } ( z | x ) = \arg \operatorname* { m a x } _ { \pi ( z | x ) } \mathbb { E } _ { z \sim \pi ( z | x ) } \left[ r ( x , z ) \right] - \beta \mathbb { D } _ { \mathsf { K L } } ( \pi ( z | x ) | | \pi _ { \mathsf { r e f } } ( z | x ) )$$

2. **采样实现**：从参考策略中采样候选轨迹 $z_i$，以接受概率 $\phi _ { i } = \exp ( ( r ( x , z _ { i } ) - r _ { \mathrm { m a x } } ) / \beta )$ 进行筛选。高奖励轨迹更可能被接受，低奖励轨迹倾向于被拒绝，从而在不显式计算最优分布的情况下，实现从优化分布中采样。

3. **理论保证**：Theorem 2 证明了该接受-拒绝过程等价于从目标分布 $\pi_r(z|x)$ 中采样；Theorem 3 给出了训练奖励策略与完美奖励策略之间期望正确率差距的上界 $\sqrt{4\epsilon/\beta}$，为方法的可靠性提供了理论支撑。

### 与基线的本质区别

| 维度 | 基线方法 | LTO |
|------|----------|-----|
| 奖励信号来源 | 无监督或语言过程奖励模型 | 潜在空间中训练的 LRM |
| 推理阶段策略 | 直接采样或多数投票 | 基于 LRM 奖励的接受-拒绝采样 |
| 优化对象 | 答案层面（投票、修正） | 潜在思维分布层面 |

与 CoE-R/CoE-C（Wang et al., 2025c）等同样在潜在空间进行校正的方法相比，LTO 的关键差异在于使用了**学习得到的分类器**而非启发式得分，从而更准确地捕捉正确性模式。与答案层面的自我修正方法（如 Self-Correction with Confidence Score, Ren et al., 2023b）相比，LTO 直接在潜在思维层面进行优化，而非仅在最终答案上进行后处理。

### 方法优势

这一创新设计带来了两个显著优势：
- **计算轻量**：LRM 是一个轻量级分类器，训练成本低；LTO 仅需调整采样策略，无需微调基础模型。
- **即插即用**：LRM 可以泛化到不同通用 LLM 的潜在表示（Table 2），并展现出跨域迁移能力（Figure 4），无需为每个模型或领域重新训练。



![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_2jkAk3EP0v/figures/001_Figure_1.jpg]]
*Figure 1: Visualization of the distribution of the correct and incorrect latent thoughts projected onto 3D space using PCA for dimension reduction. The arrows along the lines indicate the progression from the current step to the next step of the latent thought. More examples are in Appendix B*

LTO 的整体工作流分为**训练**与**推理**两个阶段，核心思想是将潜在思维轨迹的正确性预测问题转化为一个轻量级奖励模型，并以此引导推理时的轨迹采样。

### 训练阶段：构建潜在奖励模型（LRM）

1. **数据采集**：对训练集中的每个问题 $x$，从基础模型的潜在思维策略 $\pi_{\text{ref}}(z|x)$ 中采样多条潜在思维轨迹 $z = (\mathbf{h}_1, \dots, \mathbf{h}_T)$，并解码得到自然语言答案。根据答案是否正确，为每条轨迹打上二值标签 $\mathcal{O} \in \{0, 1\}$（Section 3.3）。
2. **分类器训练**：以潜在思维轨迹序列为输入，训练一个轻量级序列分类器，通过二元交叉熵损失预测该轨迹导向正确答案的概率。该分类器即为**潜在奖励模型（Latent Reward Model, LRM）** $r(x, z)$（Section 4）。

### 推理阶段：LTO 采样与答案解码

1. **候选轨迹采样**：对于测试问题 $x$，从参考策略 $\pi_{\text{ref}}(z|x)$ 中采样 $N$ 条候选潜在思维轨迹 $\{z_1, \dots, z_N\}$。
2. **接受-拒绝采样**：利用 LRM 为每条候选轨迹计算奖励分数 $r(x, z_i)$，并通过 **Algorithm 1** 的接受-拒绝机制进行筛选——高奖励轨迹以更高概率被接受，低奖励轨迹倾向于被丢弃。接受概率为：
   $$\phi_i = \exp\left(\frac{r(x, z_i) - r_{\max}}{\beta}\right)$$
   其中 $\beta$ 控制分布偏移的 KL 正则化强度（Theorem 2 保证该过程等价于从 KL 正则化最优策略 $\pi_r(z|x)$ 中采样）。
3. **答案解码**：从最终被接受的潜在思考状态出发，生成自然语言答案。

### 模块关系与数据流

```
训练数据 → [采样轨迹 + 答案标注] → 训练 LRM（轻量分类器）
                                            ↓
测试问题 → [候选轨迹采样] → [LRM 评分] → [接受-拒绝采样] → 答案解码
```

三个核心模块的职责边界清晰：
- **LRM 训练**：将潜在空间中的轨迹模式映射为标量奖励信号，是整个 pipeline 的监督来源。
- **LTO 采样（Algorithm 1）**：在推理时以零额外训练成本，通过选择性采样提升潜在思维质量。
- **答案解码**：复用基础模型的生成能力，将优化后的潜在状态转化为最终答案。

该框架的关键优势在于**解耦**：LRM 作为轻量级探针独立训练，无需修改基础模型的潜在策略参数；推理时的优化仅通过采样分布的重加权实现，计算开销可控。



LTO 方法围绕一个核心洞察构建：正确与错误的潜在思维轨迹在潜在空间中呈现高度可区分的模式。基于此，LTO 将潜在推理的优化形式化为一个概率策略优化问题，并通过三个关键模块实现。

### 模块一：潜在奖励模型（LRM）训练

LRM 是一个轻量级序列分类器，其训练目标是预测一条潜在思维轨迹是否导向正确答案。具体而言，对于训练集中的每个问题，从初始潜在状态 $h_0$ 出发，以不同随机种子采样多条潜在思维轨迹并解码答案，根据答案正确性为每条轨迹赋予二值标签。分类器以潜在思维轨迹 $z = (h_1, \dots, h_T)$ 为输入，输出该轨迹正确的概率 $p(\mathcal{O}=1 \mid x, z)$，训练损失为二元交叉熵。

LRM 的核心作用在于将不可解释的潜在空间模式转化为可操作的奖励信号 $r(x, z)$，作为后续策略优化的指引。

### 模块二：LTO 策略优化目标

LTO 将“提升潜在思维正确率”建模为在潜在策略空间中的优化问题。其无正则化目标为最大化生成正确潜在思维轨迹的期望概率：

$$\pi^*(z \mid x) = \arg\max_{\pi(z \mid x)} \mathbb{E}_{z \sim \pi(z \mid x)} \, p(\mathcal{O}=1 \mid x, z)$$

为防止优化后的策略过度偏离原始模型分布，引入 KL 正则化项，得到实用目标：

$$\pi^*(z \mid x) = \arg\max_{\pi(z \mid x)} \mathbb{E}_{z \sim \pi(z \mid x)} [r(x, z)] - \beta \, \mathbb{D}_{\mathsf{KL}}(\pi(z \mid x) \parallel \pi_{\mathsf{ref}}(z \mid x))$$

其中 $\pi_{\mathsf{ref}}$ 为参考策略（即原始模型的潜在思维分布），$\beta$ 控制正则化强度。

该 KL 正则化目标存在闭合形式的最优解（**Theorem 1**）：对于从 $\pi_{\mathsf{ref}}$ 中采样的 $N$ 条候选轨迹 $\{z_i\}_{i=1}^N$，最优策略下的采样权重为：

$$\pi_r(z_i \mid x) = \frac{\pi_{\mathsf{ref}}(z_i \mid x) \exp\left(\frac{1}{\beta} r(x, z_i)\right)}{\sum_{j=1}^N \pi_{\mathsf{ref}}(z_j \mid x) \exp\left(\frac{1}{\beta} r(x, z_j)\right)}$$

该式表明：奖励越高的轨迹被赋予越大的采样权重，而 $\beta$ 控制权重分布的锐度——$\beta \to 0$ 时退化为贪心选择最高奖励轨迹，$\beta \to \infty$ 时退化为原始参考分布。

### 模块三：接受-拒绝采样（Algorithm 1）

直接按 $\pi_r$ 的权重采样需要计算所有 $N$ 条轨迹的归一化因子，计算开销较大。LTO 采用接受-拒绝采样策略高效地从目标分布中抽取轨迹：

1. 从参考分布 $\pi_{\mathsf{ref}}$ 中采样候选轨迹 $z_i$，计算其奖励 $r(x, z_i)$；
2. 以接受概率 $\phi_i = \exp((r(x, z_i) - r_{\max}) / \beta)$ 决定是否保留该轨迹，其中 $r_{\max}$ 为当前批次中的最大奖励值；
3. 重复采样直到获得所需数量的轨迹，然后从最终潜在状态解码答案。

**Theorem 2** 保证了该采样过程产生的轨迹分布恰好等于目标分布 $\pi_r$。这种设计使得高奖励轨迹以更高概率被接受，同时无需显式计算归一化常数。

### 性能保证

**Theorem 3** 给出了训练得到的奖励策略与完美奖励策略之间的期望正确率差距上界：

$$\left| \mathbb{E}_{z \sim \pi_r(z \mid x)} r^*(x, z) - \mathbb{E}_{z \sim \pi_{r^*}(z \mid x)} r^*(x, z) \right| \le \sqrt{\frac{4\epsilon}{\beta}}$$

其中 $\epsilon$ 为 LRM 的训练误差。该定理揭示了核心权衡：更小的 $\beta$ 放大奖励信号的影响，但也放大 LRM 误差带来的风险；更大的 $\beta$ 则使策略更接近参考分布，限制了优化空间。



## 实验与关键发现

### 主实验结果

LTO在多个推理基准上对潜在推理语言模型Huginn-3.5B实现了统计显著的性能提升（Table 1）。在32步思考设置下，LTO在GSM8K上达到0.378的正确率，较基线模型的0.326提升5.2个百分点；在GSM-Symbolic上达到0.303（基线0.265，+3.8pp）；在SVAMP上达到0.539（基线0.517，+2.2pp）；在CommonsenseQA上达到0.520（基线0.500，+2.0pp）；在MBPP上达到0.295（基线0.278，+1.7pp）。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_2jkAk3EP0v/figures/012_Table_1.jpg]]
*Table 1: Comparison of the answer correctness rate of Huginn-3.5B using different correction methods. The best performance in each column is in bold, and the performance of the best baseline in each column is underlined. ∗ indicates statistically significant improvement with p \< 0.05*

与现有校正方法的对比进一步验证了LTO的有效性。多数投票（Majority Voting）虽能提升基线性能，但LTO在所有五个基准上均优于多数投票。基于置信度的自我修正（Self-Correction with Confidence Score）和基于语言评估的自我修正（Self-Correction with Verbal Evaluation）表现更弱，甚至在某些数据集上低于基线。CoE-R和CoE-C作为基于启发式潜在得分的潜在思维校正方法，在部分数据集上接近多数投票，但仍不及LTO。值得注意的是，将LRM的奖励信号用于加权多数投票（Weighted Majority Voting w. LRM）已能超越标准多数投票，这表明LRM本身具有检测错误潜在思维模式的能力；而LTO通过接受-拒绝采样进一步优化潜在分布，取得了最佳性能。

在通用LLM上的迁移实验（Table 2）表明，LTO不依赖于特定的潜在推理架构。在OLMo-7B、Llama-2-7B、Llama-2-13B和Mistral-7B上，LTO在所有五个基准上均优于基线模型和多数投票。其中Llama-2-7B在GSM8K上的提升最为显著：LTO达到0.389，而基线仅为0.223，提升达16.6个百分点。在更具挑战性的MATH和GPQA基准上（Table A5），LTO同样展现出稳健的提升：Llama-3-8B在MATH上从基线的0.267提升至0.375（+10.8pp），Qwen-3-4B在GPQA上从0.263提升至0.318（+5.5pp）。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_2jkAk3EP0v/figures/013_Table_2.jpg]]
*Table 2: Performance of LTO on general LLMs. The best-performing method for each model is in bold. ∗ indicates the improvement over the best runner-up is statistically significant with p \< 0 . 0 5*

### 潜在分类器的预测能力

LTO的核心驱动力来自潜在分类器（LRM）对思维轨迹正确性的预测能力。Figure 3展示了LRM在不同思考步数下的ROC-AUC性能：在SVAMP上，ROC-AUC接近1.0，表明数学推理的潜在思维模式具有高度可区分的正确/错误特征；在MBPP上，ROC-AUC约在0.8左右，说明代码推理的潜在思维判别更具挑战性，但仍保持可靠的预测能力。分类性能随思考步数增加而单调提升，在约10-12步后趋于平台期，这表明早期到中期的潜在思维步骤已编码了大部分关于正确性的判别信息。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_2jkAk3EP0v/figures/011_Figure_3.jpg]]
*Figure 3: Performance of the latent classifier trained with varying numbers of latent thinking steps on the SVAMP and MBPP datasets. Additional metrics and results are available in Appendix H.1*

### 消融实验

**采样预算的影响**（Figure A4）：将LTO的采样预算N从1增至20时，性能稳步提升，验证了更多候选轨迹能提高选中高奖励轨迹的概率。这一趋势与Theorem 3的理论保证一致——更大的采样预算缩小了经验分布与最优分布的期望奖励差距。

**KL正则化系数β的鲁棒性**（Figure A5）：在β取值从1e-3到1e-1的宽范围内，LTO始终优于基线模型，表明方法对超参数选择不敏感。β控制着优化分布与参考分布的偏离程度：过小的β可能导致分布坍缩到少数高奖励轨迹，过大的β则退化为随机采样。

**思考步数的影响**（Table A3）：将思考步数从16增至32时，基线模型的性能提升，但答案多样性下降，导致LTO的提升空间缩小。例如在GSM8K上，16步时LTO相对基线的提升为6.7个百分点（0.369 vs 0.302），而32步时缩小至5.2个百分点（0.378 vs 0.326）。这一现象揭示了正确率与多样性之间的权衡：更多思考步数使模型更确定地收敛到某一答案，减少了可供LTO筛选的多样性。

**潜在表示聚合策略**（Table A1）：对潜在思维轨迹的全token平均池化（all tokens）在准确率和ROC-AUC上均优于仅使用前10个或后10个token，表明关于正确性的判别信息分布在整个思考序列中，而非仅集中在初始或最终阶段。

### 跨域迁移能力

Figure 4展示了LRM的跨域迁移效果。使用GSM8K训练的LRM应用于GSM-Symbolic时，LTO性能与使用域内LRM相当，说明数学推理的潜在思维模式具有跨数据集的可迁移性。然而，使用GSM8K的LRM应用于CommonsenseQA时性能下降明显，表明不同推理类型（数学 vs. 常识）的潜在思维特征存在领域特异性。将多个领域数据混合训练通用LRM（General LRM）能在所有目标域上取得接近域内LRM的性能，证明了构建统一潜在奖励模型的可行性。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_2jkAk3EP0v/figures/014_Figure_4.jpg]]
*Figure 4: Performance of LTO using different LRMs. “GSM-S” refers to the GSM-Symbolic dataset. “CQA” refers to the CommonsenseQA dataset. “None” refers to the performance of the base model without LTO*

### 失败模式与局限性

LTO的根本局限在于其仅通过选择性采样优化分布，而非修改基础模型的潜在策略。当模型能力不足，即所有采样的潜在思维轨迹均导致错误答案时，LTO无法提升性能——LRM只能识别相对更优的轨迹，但无法创造正确轨迹。这一局限性在MBPP等模型表现较弱的任务上尤为明显：尽管LRM的ROC-AUC约0.8，LTO的绝对提升仅为1.7个百分点，因为基线模型的正确率本身较低（0.278），可用的正确轨迹稀缺。

此外，当前LRM的奖励信号仅指示答案正确性这一单一维度，未涵盖安全性、有帮助性、诚实性等其他重要维度。这意味着LTO可能在优化正确性的同时，无意中放大其他维度的风险。

### 补充图表

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_2jkAk3EP0v/figures/055_Table_5.jpg]]
*Table 5: Table A3: Performance of LTO with different numbers of thinking steps. For each thinking step, the best-performing method is highlighted in bold. ∗ indicates the improvement over the best runner-up is statistically significant with p \< 0 . 0 5*



## 定位与知识库关联

### 1. 方法谱系：从答案校正到潜在思维校正

LTO 的核心贡献在于将推理校正的干预点从**输出答案层**前移至**潜在思维层**。现有校正方法沿两条路径演进：

**答案层校正方法**直接对模型生成的最终答案进行后处理，不触及内部推理过程。代表性工作包括：
- **Majority Voting**（Wang et al., 2023）：对多次采样答案进行多数投票，利用答案分布的集中性提升可靠性。
- **Self-Correction with Confidence Score**（Ren et al., 2023b）：基于模型自身的置信度估计进行答案修正。
- **Self-Correction with Verbal Evaluation**（Manakul et al., 2023）：通过语言化的自我评估进行答案校正。

这些方法的根本局限在于：它们仅能利用答案信号，无法感知或纠正导致错误答案的潜在推理缺陷。

**潜在思维校正方法**试图在潜在空间中直接干预推理过程。LTO 的直接前驱是 **CoE-R / CoE-C**（Wang et al., 2025c），该方法基于启发式潜在得分（如表示质量指标）筛选潜在思维轨迹。然而，启发式得分与答案正确性的关联缺乏明确的理论保证，且无法端到端优化。

LTO 的关键突破在于将潜在思维校正转化为**可优化的奖励驱动采样问题**：训练一个轻量级潜在分类器（LRM）直接预测潜在思维轨迹的正确性，并将其作为奖励信号，通过接受-拒绝采样从优化分布中抽取更可能正确的潜在轨迹。这一设计将校正信号从启发式提升为可学习的、直接对齐于答案正确性的奖励函数。

### 2. 方法定位：推理时优化而非策略更新

LTO 属于**推理时优化（inference-time optimization）** 范式，其核心操作是在固定基础模型的前提下，通过选择性采样优化潜在思维分布，而非修改模型参数。这与强化学习驱动的偏好优化方法（如 DPO、RLHF）形成互补而非替代关系：

- **LTO 不更新基础策略**：LTO 通过 Algorithm 1 的接受-拒绝采样实现分布偏移，基础模型的潜在策略 $\pi_{\text{ref}}(z|x)$ 保持不变。这意味着当基础模型能力不足（即所有采样轨迹均错误）时，LTO 无法提升性能——这是其根本性适用边界。
- **LRM 可独立扩展**：LRM 的训练仅需采样轨迹和答案标签，计算成本远低于基础模型微调。这使 LTO 的奖励信号可通过增加训练数据、改进分类器架构等方式独立提升，而不触及基础模型。

### 3. 适用边界与关键局限

**适用条件**：
1. **基础模型需具备非零正确率**：LTO 的选择性采样机制要求至少存在部分正确的潜在思维轨迹。当基础模型在特定任务上正确率极低时，LRM 无法学习有效的判别模式，LTO 的增益趋于零。
2. **潜在空间需具备可区分性**：LTO 依赖正确与错误潜在思维轨迹在表示空间中的可分离性。Figure 1 和 Figure 2 的证据表明，这一条件在数学推理（SVAMP）上高度成立（ROC-AUC 接近 1.0），但在代码生成（MBPP）上有所减弱（ROC-AUC 约 0.8），反映了不同领域潜在表示质量的差异。

**关键局限**：
- **奖励信号维度单一**：LRM 仅预测答案正确性（$\mathcal{O}=1$），未涵盖安全性、有帮助性、公平性等其他关键维度。这限制了 LTO 在需要多维对齐的场景中的应用。
- **思考步数的影响**：Table A3 显示，增加潜在思考步数（16→32）会降低答案多样性，导致 LTO 的提升空间缩小。这暗示 LTO 的增益与基础模型的探索空间大小正相关。
- **跨域迁移的不确定性**：虽然 Figure 4 展示了 LRM 的跨域泛化能力，但论文未系统分析迁移失败的条件（如域间潜在表示结构差异过大时的性能退化模式）。

### 4. 开放问题与未来方向

论文明确指出的开放问题指向四个扩展方向：

1. **自适应思考步数**：当前 LTO 使用固定步数，但不同问题可能受益于不同长度的潜在推理。设计自适应机制以平衡正确率与多样性，是提升效率的关键。

2. **LRM 驱动的策略更新**：将 LRM 的奖励信号集成到基于强化学习的偏好优化框架中，直接更新基础模型的潜在策略 $\pi_{\text{ref}}$，可能突破 LTO 当前“仅选择、不改进”的范式限制。

3. **多维奖励扩展**：将潜在奖励模型从单一的答案正确性扩展为捕捉安全性、有帮助性等多维信号的复合奖励函数，使 LTO 适用于更广泛的对齐场景。

4. **多目标优化框架**：将 LTO 扩展为多目标优化框架，同时优化多个奖励维度，可能需要在 Pareto 前沿上进行采样或引入标量化机制。

**需手动验证的点**：论文未提供 LTO 在完全错误轨迹场景下的失效分析（如基础模型正确率接近 0 时的 LRM 训练行为和 LTO 性能），也未系统讨论 LRM 的分类置信度校准及其对接受-拒绝采样效率的影响。这些边界条件的定量刻画需要进一步实验确认。



## 原文 PDF

![[paperPDFs/ICLR_2026/Latent_Thinking_Optimization_Your_Latent_Reasoning_Language_Model_Secretly_Encodes_Reward_Signals_in_Its_Latent_Thoughts.pdf]]
