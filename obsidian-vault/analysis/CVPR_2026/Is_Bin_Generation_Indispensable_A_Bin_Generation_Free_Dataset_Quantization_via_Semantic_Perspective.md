---
title: Is Bin Generation Indispensable? A Bin-Generation-Free Dataset Quantization via Semantic Perspective
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Is_Bin_Generation_Indispensable_A_Bin_Generation_Free_Dataset_Quantization_via_Semantic_Perspective.pdf
project_link: null
code_link: "https://github.com/MaijieDeng/BGFDQ"
aliases:
- BGFDQB
- IBGIBGFDQSP
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 用基于KNN的邻居识别替代分箱生成，同时设计邻居感知的核心集选择策略和语义偏移驱动的自适应图像块丢弃模块。
primary_logic: 通过样本间的语义邻居关系来引导核心集选择，能够以更低的计算成本实现更高的覆盖率和更低的冗余度；利用语义偏移阈值自适应调整每个样本的图像块丢弃率，可在保持语义完整性的前提下最大化压缩比。
claims:
- BGFDQ（不含SPD）在CIFAR-10上相比基线减少15%-35%的总运行时间，同时验证准确率提升超过1%。
- BGFDQ（含SPD）相对于基线获得超过2%的性能提升。
- NI+NCS在理论上有更高的覆盖率和更低的冗余度，优于基于分箱的随机选择。
- NI+NCS策略在所有样本规模上均优于随机选择和BG+RS，验证了邻居语义结构的重要性。
---

# Is Bin Generation Indispensable? A Bin-Generation-Free Dataset Quantization via Semantic Perspective

> [!tip] 核心洞察
> 通过样本间的语义邻居关系来引导核心集选择，能够以更低的计算成本实现更高的覆盖率和更低的冗余度；利用语义偏移阈值自适应调整每个样本的图像块丢弃率，可在保持语义完整性的前提下最大化压缩比。

| 字段 | 内容 |
|------|------|
| 中文题名 | 分箱生成是否不可或缺？一种从语义视角出发的无分箱数据集量化方法 |
| 英文题名 | Is Bin Generation Indispensable? A Bin-Generation-Free Dataset Quantization via Semantic Perspective |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Deng_Is_Bin_Generation_Indispensable_A_Bin-Generation-Free_Dataset_Quantization_via_Semantic_CVPR_2026_paper.html) · [Code](https://github.com/MaijieDeng/BGFDQ) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Bin-Generation-Free Dataset Quantization (BGFDQ) |
| Dataset | CIFAR-10, CIFAR-100, ImageNet-1K, Fakeddit |

> [!tip] 效果简介
> - CIFAR-10 (ρ=20%) 上，验证准确率 (%) 91.6 vs 89.3 (ADQ) (+2.3)；端到端运行时间 (秒) 1052 (BGFDQ w/o SPD) vs 1640 (ADQ) (-35.9%)。
> - CIFAR-100 上，验证准确率提升 BGFDQ (w/ SPD) vs 现有最佳基线 (+5%)。
> - ImageNet-1K (ρ=30%) 上，验证准确率 (%) 52.8 ± 0.07 (BGFDQ w/ SPD) vs DQ / ADQ (具体数值未提供, 但低于proposed) (≈ +2.3% (基于平均1.0%+1.3%提升推算))。

## 概要

数据集量化旨在通过核心集选择与图像块丢弃来压缩数据集规模，从而降低下游模型训练成本。现有方法遵循“分箱生成 → 核心集选择 → 图像块丢弃”的范式，但其分箱生成步骤基于子模函数迭代采样，计算复杂度高达 $O(CM^3)$，在大规模数据集上极易导致内存溢出或耗时巨大。此外，固定的图像块丢弃率忽略了不同样本间冗余程度的差异，导致压缩后数据质量下降。

针对上述瓶颈，本文提出**无分箱数据集量化方法 BGFDQ**。核心思路是：用基于 KNN 的邻居识别替代昂贵的分箱生成，以样本间的语义邻居关系引导核心集选择，从而以更低计算成本实现更高覆盖率和更低冗余度；同时设计语义偏移驱动的自适应图像块丢弃模块，根据类内语义偏移阈值动态调整每个样本的丢弃率，在保持语义完整性的前提下最大化压缩比。

实验结果表明，BGFDQ（不含 SPD）在 CIFAR-10 上相比基线减少 15%–35% 的总运行时间，同时验证准确率提升超过 1%（见 Figure 1(c)）；加入 SPD 后，性能进一步提升超过 2%。在 CIFAR-100 上，BGFDQ 实现了高达 5% 的验证准确率提升。在 ImageNet-1K 和 Fakeddit 等大规模数据集上，BGFDQ 在现有分箱方法因内存溢出而失败的场景下仍能成功运行，并取得一致的性能优势（见 Table 2、Table 4）。



### 数据集量化的核心任务与挑战

深度学习模型的性能高度依赖大规模、高质量的训练数据，但海量数据带来的存储、传输与训练开销已成为实际部署的瓶颈。数据集量化（Dataset Quantization）作为一种数据压缩范式，旨在从原始数据集中选取一个紧凑且具有代表性的核心集（coreset），并通过图像块丢弃（patch dropping）进一步压缩每个样本的存储体积，从而在保持模型训练精度的前提下大幅降低数据规模。

现有数据集量化方法——如 **DQ**（Zhou et al., ICCV 2023）、**ADQ**（Li et al., AAAI 2025）和 **DQAS**（Zhao et al., ECCV 2024）——遵循一个统一的三阶段范式：

1. **分箱生成（Bin Generation）**：通过迭代采样将数据集划分为互不重叠的“箱”（bins），其目标函数为子模（submodular）形式的多样性-代表性权衡，计算复杂度高达 $O(CM^3)$。
2. **核心集选择（Coreset Selection）**：在每个箱内均匀随机选取样本，构成核心集。
3. **图像块丢弃（Patch Dropping）**：利用 GradCAM++ 计算每个图像块的重要性分数，按固定丢弃率 $\theta$（如 25%）移除低分块。

### 现有方法的两个结构性缺陷

尽管上述范式在中小规模数据集上取得了可观效果，但分析揭示其存在两个根本性瓶颈，严重制约了可扩展性与压缩质量。

**瓶颈一：分箱生成的计算灾难。** 分箱生成的子模优化过程复杂度为 $O(CM^3)$，其中 $C$ 为类别数，$M$ 为每类样本数。当数据集规模增长时（如 ImageNet-1K 单类样本数超 1000，或 Fakeddit 中单类样本数超 200K），该步骤导致内存溢出（OOM）或运行时间急剧膨胀，使现有方法在大规模数据集上不可用。更关键的是，消融实验（Table 5）表明：分箱后随机采样（BG+RS）相比纯随机采样（RS）在 CIFAR-10 和 CIFAR-100 上的平均精度提升仅为 0.1%，这意味着分箱生成所付出的高昂计算代价并未转化为实质性的数据质量增益。

**瓶颈二：固定丢弃率忽略样本间冗余差异。** 现有方法对所有样本施加统一的图像块丢弃率，但不同样本包含的冗余信息量存在显著差异。如 Figure 2(c) 所示，各样本中“不重要图像块”的数量服从长尾分布——部分样本可安全丢弃 40% 以上的块而不损失语义信息，而另一些样本在丢弃 25% 时即出现语义退化。固定丢弃率策略迫使冗余度低的样本过度压缩、冗余度高的样本压缩不足，导致核心集整体质量下降。

### 本文动机与核心思路

上述分析揭示了一个关键洞察：**分箱生成并非数据集量化中不可或缺的步骤**。分箱的本质目的是在样本空间中建立一种分组结构以引导核心集选择，但这一目标可以通过更轻量、更语义化的方式实现。

本文提出 **Bin-Generation-Free Dataset Quantization（BGFDQ）**，从语义视角重新设计数据集量化流程，核心思路包含两个层面：

- **用邻居关系替代分箱结构**：通过 KNN 识别每个样本在特征空间中的语义邻居，以 $O(M \log M)$ 级别的计算成本替代 $O(CM^3)$ 的分箱生成，并基于邻居信息设计概率性的核心集选择策略，实现更高的数据覆盖率与更低的冗余度。
- **用语义偏移驱动自适应压缩**：为每个样本动态计算其最优图像块丢弃率，约束条件为丢弃后的语义偏移不超过类内语义变化阈值，从而在保持语义完整性的前提下最大化压缩比。

Figure 1 从范式层面对比了现有方法与 BGFDQ 的差异，并展示了初步的性能优势：BGFDQ（不含 SPD）相比基线减少 15%–35% 的总运行时间，同时验证准确率提升超过 1%；加入 SPD 后性能进一步提升超过 2%。



## 核心方法与创新机理

本文提出的无分箱数据集量化方法 **BGFDQ** 针对现有数据集量化范式中的两个结构性瓶颈进行了系统性重构：**分箱生成的高计算复杂度**与**固定图像块丢弃率的信息损失**。其核心创新可归纳为三个相互协同的 **changed slots**，分别替换了现有方法中的关键模块。

### 1. 从分箱生成到邻居识别：语义粒度下移与计算解耦

现有数据集量化方法（如 **DQ** (Zhou et al., ICCV 2023)、**ADQ** (Li et al., AAAI 2025)）依赖基于子模函数的分箱生成步骤，通过迭代采样将数据集划分为互不重叠的箱。该过程的时间复杂度为 $O(CM^3)$，其中 $C$ 为类别数、$M$ 为每类样本数，导致在大规模数据集上出现内存溢出或耗时不可接受的问题。

BGFDQ 将数据分区策略从“分组级”下移至“样本级”，用基于 KNN 的邻居识别替代分箱生成。具体而言，对于每个样本 $x_i$，计算其在特征空间中的嵌入向量 $z_i = f(x_i)$，并通过平方欧氏距离度量语义相似性：

$$d_{ij} = \| z_i - z_j \|_2^2 = \| f(x_i) - f(x_j) \|_2^2$$

在此基础上，为每个样本构建类内 K 近邻集合（默认 $K=20$）：

$$\mathcal{N}_i = \operatorname{TopK}_{j \in \mathcal{C}(i), j \neq i} (-d_{ij})$$

这一替换的核心优势在于：邻居识别仅需计算样本间的成对距离，完全规避了分箱生成中的迭代优化过程，从而将计算复杂度从立方级降至二次级。如 Figure 1(c) 所示，BGFDQ（不含 SPD）在 CIFAR-10 上将总运行时间相对基线降低了 15%–35%，同时验证准确率提升超过 1%。

### 2. 从均匀随机选择到邻居感知的核心集选择：覆盖率-冗余度联合优化

现有方法在分箱完成后，通常在每个箱内进行均匀随机选择以构建核心集。这种策略忽略了样本间的语义冗余关系，容易导致核心集中保留过多语义相似的样本，降低数据效率。

BGFDQ 设计了邻居感知的核心集选择策略 **NCS**。在选择一个样本后，按其邻居距离的远近以指数衰减的概率移除其 K 近邻：

$$p_k = e^{-\rho \alpha k}, \quad \alpha > 0$$

其中 $k$ 为邻居排序（$k=1$ 表示最近邻），$\alpha$ 控制衰减速度。距离越近的邻居被移除的概率越大，从而在保证空间覆盖率的同时有效降低冗余度。

理论分析（附录 A）证明，NI+NCS 策略在覆盖率 $R(S)$ 和冗余度 $\Gamma(S)$ 两个指标上均优于基于分箱的随机选择：

$$R(S) = \sup_{x \in D} \min_{s \in S} d(x, s), \quad \Gamma(S) = \min_{s \neq s'} d(s, s')$$

消融实验（Table 5）进一步验证了该策略的有效性：NI+NCS 在所有核心集比例下均优于随机选择（RS）和分箱后随机选择（BG+RS），表明利用样本间的语义邻居关系比依赖分组结构更能提升核心集的代表性。

### 3. 从固定丢弃率到语义偏移驱动的自适应图像块丢弃：个性化压缩决策

现有方法对所有样本采用固定的图像块丢弃率 $\theta$（如 25%），忽略了不同样本间冗余程度的显著差异。如 Figure 2 所示，大量样本的最优丢弃率偏离固定值，导致部分样本被过度压缩（丢失关键信息）或压缩不足（保留冗余块）。

BGFDQ 提出了语义偏移驱动的自适应图像块丢弃模块 **SPD**。其核心思想是：对每个样本在所有候选丢弃率下生成变体 $x_{\theta_i}$，并选择满足语义偏移约束的最大丢弃率：

$$x_{\theta^{*}} = \arg\max_{\theta_i} \{ \theta_i \mid d(x, x_{\theta_i}) < \lambda_C \}$$

其中语义偏移阈值 $\lambda_C$ 定义为类内最小成对语义距离，实际计算时取最小的 50 个非零距离的平均值：

$$\lambda_C = \min\{d_{ij} \mid i,j \in C, i \neq j\}$$

该机制使得每个样本能够根据自身冗余程度获得个性化的压缩比例。Figure 4 的消融实验表明，SPD 在丢弃率从 25% 增加到 40% 时仍能保持与固定丢弃率（25%）相当的准确率，证明其能够有效识别并去除冗余块而不损失语义信息。在整体性能上，加入 SPD 后的 BGFDQ 相对基线获得超过 2% 的性能提升（Figure 1(c)）。

### 创新协同效应

三个 changed slots 构成了从“分组-随机-固定”到“样本-感知-自适应”的完整范式转换。邻居识别为后续的核心集选择和图像块丢弃提供了统一的语义基础；邻居感知选择在样本层面最大化覆盖率并最小化冗余；语义偏移驱动的自适应丢弃则在样本内部进一步去除冗余。这一协同设计使得 BGFDQ 在 CIFAR-100 上实现了高达 5% 的验证准确率提升，并在 Fakeddit 等大规模类数据集上成功运行（而现有分箱方法出现内存溢出），验证了无分箱范式在精度、效率和可扩展性上的综合优势。



BGFDQ 的整体工作流程如图 3 所示，由三个核心模块串联构成：**邻居识别（Neighbor Identification, NI）**、**邻居感知核心集选择（Neighbor-Aware Coreset Selection, NCS）** 和 **语义偏移驱动的图像块丢弃（Semantic-Shift Patch Dropping, SPD）**。这三个模块共同实现了从原始数据集到量化核心集的端到端映射，完全摒弃了传统数据集量化方法中计算代价高昂的分箱生成步骤。

### 输入与输出

- **输入**：原始数据集 $D = \{(x_i, y_i)\}_{i=1}^{N}$，目标核心集比例 $\rho$，邻居数 $K$，以及 SPD 所需的类内语义偏移阈值 $\lambda_C$。
- **输出**：量化核心集 $S^*$，其中每个样本 $x_i$ 经过自适应图像块丢弃处理，且核心集的加权样本数满足 $\rho = \frac{|S^*| \times w_{\text{samples}}}{|D|} \times 100\%$。

### 模块关系与数据流

**第一步：邻居识别（NI）**  
对于原始数据集中的每个样本 $x_i$，使用预训练特征提取器 $f(\cdot)$ 获取其嵌入向量 $z_i = f(x_i)$。然后按类别计算样本间的语义距离 $d_{ij} = \| z_i - z_j \|_2^2$，并为每个样本构建其类内的 $K$ 近邻集合 $\mathcal{N}_i = \operatorname{TopK}_{j \in \mathcal{C}(i), j \neq i} (-d_{ij})$。这一步以 $O(N^2 d)$ 的复杂度替代了传统分箱生成中 $O(CM^3)$ 的迭代子模优化，是 BGFDQ 实现高效量化的关键。

**第二步：邻居感知核心集选择（NCS）**  
基于 NI 构建的邻居关系，NCS 采用随机移除策略生成核心集：每次随机选择一个样本加入核心集，然后以概率 $p_k = e^{-\rho \alpha k}$ 移除其第 $k$ 近邻。距离越近的邻居被移除的概率越大，从而在保证高覆盖的同时降低核心集的冗余度。理论分析表明，NCS 在覆盖率和冗余度两个指标上均优于基于分箱的随机选择策略。

**第三步：语义偏移驱动的图像块丢弃（SPD）**  
对于核心集中的每个样本，SPD 计算其在不同丢弃率 $\theta$ 下的变体 $x_\theta$，并评估变体与原始样本之间的语义距离 $d(x, x_\theta)$。当该距离不超过类内语义偏移阈值 $\lambda_C$ 时，选择满足约束的最大丢弃率 $\theta^*$ 对应的变体作为最终压缩样本。这一自适应机制取代了传统方法中固定的全局丢弃率，使得每个样本都能在不损失语义完整性的前提下达到最优压缩比。

### 与传统范式的对比

传统数据集量化方法遵循“分箱生成 → 核心集选择 → 图像块丢弃”的固定范式，其中分箱生成通过迭代求解子模优化问题将样本划分为互不相交的箱，计算复杂度为 $O(CM^3)$，在大规模数据集上容易导致内存溢出。BGFDQ 将这一范式重构为“邻居识别 → 邻居感知核心集选择 → 语义偏移驱动的图像块丢弃”，以样本粒度的语义邻居关系替代粗粒度的分箱结构，实现了更低计算开销下的更高质量压缩。

### 补充图表

![[assets/figures/papers/paper_list_l2688_https_openaccess_thecvf_com_content_CVPR2026_html_Deng_Is_Bin_Generation/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of paradigms and performance for dataset quantization approaches. (a) Previous works follow a paradigm consisting of bin generation, coreset selection and patch dropping. (b) Our approach first performs neighbor identification to guide coreset selection, followed by a semantic-shift patch dropping to adaptively remove unimportant patches. (c) Runtime breakdown for quantizing CIFAR-10 and the validation accuracy by training ResNet-18 on the quantized coreset. BGFDQ (w/o SPD) reduces total runtime by 15%–35% compared to baselines while achieving over 1% higher accuracy. Although BGFDQ (w/ SPD) introduces additional computation, its more adaptive compression yields over 2% performan...*

![[assets/figures/papers/paper_list_l2688_https_openaccess_thecvf_com_content_CVPR2026_html_Deng_Is_Bin_Generation/figures/003_Figure_3.jpg]]
*Figure 3: Bin-Generation-Free Dataset Quantization (BGFDQ). We first analyze the original dataset using our (a) Neighbor Identification, where each sample is assigned its neighbor information. Then, we perform (b) Neighbor-aware Coreset Selection, which removes samples based on the neighbor information. Finally, we apply (c) Semantic-shift Patch Dropping to drop unimportant sample patches. Each sample is quantized according to its adaptive drop ratio. The output of BGFDQ is a representative quantized coreset of the original dataset*



### 3.1 邻居识别（Neighbor Identification, NI）

现有数据集量化方法依赖分箱生成（Bin Generation）将数据集划分为互不重叠的子集，其目标函数为子模（submodular）多样性-代表性权衡，计算复杂度高达 $O(CM^3)$，在大规模数据集上导致内存溢出或耗时巨大。BGFDQ 用基于 KNN 的邻居识别完全替代分箱生成，在样本粒度上进行语义级分析。

给定样本 $x_i$ 和 $x_j$，首先通过特征提取器 $f(\cdot)$ 获得嵌入向量 $z_i = f(x_i)$、$z_j = f(x_j)$，定义语义距离为欧氏距离平方：

$$d_{ij} = \| z_i - z_j \|_2^2 = \| f(x_i) - f(x_j) \|_2^2 \quad \text{(Eq. 3)}$$

对每个样本 $x_i$，在其所属类别 $\mathcal{C}(i)$ 内选取语义距离最小的 $K$ 个样本（$K=20$），构成邻居集：

$$\mathcal{N}_i = \operatorname{TopK}_{j \in \mathcal{C}(i), j \neq i} (-d_{ij}) \quad \text{(Eq. 4)}$$

邻居集 $\mathcal{N}_i$ 为后续核心集选择提供样本间的语义邻近关系，是 BGFDQ 流水线的第一步（Figure 3(a)）。

### 3.2 邻居感知的核心集选择（Neighbor-Aware Coreset Selection, NCS）

基于 NI 构建的邻居信息，NCS 通过概率性移除冗余样本来生成高覆盖率、低冗余度的核心集。其核心机制是：每选择一个样本 $x_i$ 加入核心集后，对其邻居集 $\mathcal{N}_i$ 中的第 $k$ 近邻，以概率 $p_k$ 将其移除：

$$p_k = e^{-\rho \alpha k}, \quad \alpha > 0 \quad \text{(Eq. 5)}$$

其中 $\rho$ 为核心集比例，$\alpha$ 为衰减系数。距离越近的邻居（$k$ 越小）被移除的概率越大，从而有效抑制冗余。

**理论优势**：NI+NCS 在覆盖率 $R(S)$ 和冗余度 $\Gamma(S)$ 两个指标上均优于基于分箱的随机选择。覆盖率定义为核心集对数据空间的最大覆盖距离：

$$R(S) = \sup_{x \in D} \min_{s \in S} d(x, s) \quad \text{(Eq. 6)}$$

值越小表示覆盖越充分。冗余度定义为核心集样本间的最小距离：

$$\Gamma(S) = \min_{s \neq s'} d(s, s') \quad \text{(Eq. 7)}$$

值越大表示冗余越低。理论推导（详见附录 A）证明，NI+NCS 可获得更低的 $R(S)$ 和更高的 $\Gamma(S)$，从而生成更具代表性的核心集（Figure 3(b)）。

### 3.3 语义偏移驱动的图像块丢弃（Semantic-Shift Patch Dropping, SPD）

现有方法对所有样本采用固定丢弃率 $\theta$（如 25%），忽略了不同样本间冗余程度的差异。SPD 通过评估丢弃图像块后的语义一致性，为每个样本自适应确定最优丢弃率。

首先，为每个类别 $C$ 定义语义偏移阈值 $\lambda_C$，表示类内允许的最大语义偏差：

$$\lambda_C = \min\{d_{ij} \mid i,j \in C, i \neq j\} \quad \text{(Eq. 11)}$$

实际计算时，取最小的 50 个非零类内距离的平均值以增强鲁棒性。

对于样本 $x$，设 $x_{\theta_i}$ 为丢弃比例为 $\theta_i$ 后的变体。SPD 在所有候选丢弃率中选择满足语义偏移约束的最大丢弃率对应的变体作为最优结果：

$$x_{\theta^{*}} = \arg\max_{\theta_i} \{ \theta_i \mid d(x, x_{\theta_i}) < \lambda_C \}$$

该策略确保在保持语义完整性的前提下最大化压缩比，使每个样本的丢弃率与其自身冗余程度相匹配（Figure 3(c)）。

### 3.4 核心集比例定义

为统一度量标准，加权后的核心集比例定义为：

$$\rho = \frac{|S^*| \times w_{\text{samples}}}{|D|} \times 100\%$$

其中 $|S^*|$ 为核心集样本数，$w_{\text{samples}}$ 为 SPD 产生的样本权重（保留的图像块比例），$|D|$ 为原始数据集大小。该定义将图像块丢弃带来的信息损失纳入核心集规模的计算。

### 补充图表

![[assets/figures/papers/paper_list_l2688_https_openaccess_thecvf_com_content_CVPR2026_html_Deng_Is_Bin_Generation/figures/002_Figure_2.jpg]]
*Figure 2: (a) The pipeline of patch dropping; The patch importance scores are computed using GradCAM++ [1]. (b) Examples of suboptimal patch dropping; (c) The diverse distribution of the number of unimportant patches indicates that most samples are not optimally quantized, which degrades the quality of the dataset*



## 实验与关键发现

### 主要结果

BGFDQ 在四个规模与特性各异的数据集上进行了评估：CIFAR-10、CIFAR-100、ImageNet-1K 和 Fakeddit（多模态虚假信息检测）。对比基线涵盖核心集选择（**GradMatch**，Killamsetty et al., ICML 2021）、数据集蒸馏（**DM**，Zhao et al., WACV 2023）和数据集量化方法（**DQ**，Zhou et al., ICCV 2023；**ADQ**，Li et al., AAAI 2025；**DQAS**，Zhao et al., ECCV 2024）。所有方法均在同一硬件环境（RTX 4070 SUPER GPU, i5-14600KF CPU）下重现实时结果。

在 CIFAR-10 上，当核心集比例 ρ=20% 时，BGFDQ（含 SPD）达到 91.6% 的验证准确率，比最佳基线 ADQ（89.3%）高出 2.3 个百分点（Table 4）。不含 SPD 的 BGFDQ 在 CIFAR-10 上的总运行时间仅为 1052 秒，较 ADQ 的 1640 秒减少 35.9%，同时准确率仍高出 1% 以上。在 CIFAR-100 上，BGFDQ 实现了高达 5% 的验证准确率提升。在 ImageNet-1K（ρ=30%）上，BGFDQ（含 SPD）达到 52.8±0.07% 的准确率，相比基线平均提升约 2.3%。在 Fakeddit（ρ=3%）这一大规模类数据集上，现有分箱方法（DQ、ADQ）因内存溢出而失败，BGFDQ 成功运行并取得 85.3±0.07% 的准确率，展现出显著的可扩展性优势。

![[assets/figures/papers/paper_list_l2688_https_openaccess_thecvf_com_content_CVPR2026_html_Deng_Is_Bin_Generation/figures/008_Table_4.jpg]]
*Table 4: End-to-end runtime breakdown (in seconds) and coreset performance on CIFAR-10 with coreset fraction*

在未见架构上的泛化测试（Table 3）表明，BGFDQ 生成的核心集在 ResNet-50 和 ViT 上均保持一致的性能优势，证明其选择的样本具有良好的跨架构泛化能力。

![[assets/figures/papers/paper_list_l2688_https_openaccess_thecvf_com_content_CVPR2026_html_Deng_Is_Bin_Generation/figures/006_Table_3.jpg]]
*Table 3: Validation accuracy on unseen architectures (ResNet-50, ViT) with coreset fraction*

### 消融实验

**核心集选择策略消融。** Table 5 对比了三种核心集选择策略在 CIFAR-10 上的表现：随机选择（RS）、分箱后随机选择（BG+RS）和本文提出的邻居识别+邻居感知核心集选择（NI+NCS）。结果表明，NI+NCS 在所有样本规模上均优于 RS 和 BG+RS，验证了利用邻居语义结构进行核心集选择的有效性。这一结果与理论分析一致——NI+NCS 在覆盖率 $R(S)$ 和冗余度 $\Gamma(S)$ 两个指标上均优于基于分箱的随机选择。

**图像块丢弃策略消融。** Figure 4 展示了不同块丢弃策略的对比。固定丢弃率 25% 的 PD(25%) 作为基线；当丢弃率增加到 40% 时，PD(40%) 的准确率显著下降。而本文提出的语义偏移驱动自适应丢弃（SPD）在丢弃率从 25% 增加到 40% 时，仍能保持与 PD(25%) 相当的准确率，证明 SPD 能够有效识别并去除冗余块，避免丢弃语义关键区域。

**模块组合消融。** Table 4 的运行时分解显示：BGFDQ（不含 SPD）在所有方法中总运行时间最低，且精度高于 DQ 和 ADQ；加入 SPD 后精度进一步提升约 1.3%，但引入了额外的语义偏移计算开销。这表明不含 SPD 的版本适用于计算敏感场景，而含 SPD 的版本适用于精度优先场景。

### 失败模式与局限性

1. **SPD 的计算开销权衡。** BGFDQ（含 SPD）在样本量较小时，SPD 带来的精度增益被其额外计算开销所抵消，性价比下降。实际部署时需根据数据集规模和精度需求选择是否启用 SPD。

2. **语义偏移阈值的启发式设定。** 类内语义偏移阈值 $\lambda_C$ 的计算基于类内最小非零距离的均值，缺乏理论上的最优性保证。在某些类内差异本身较大的类别中，该阈值可能过于宽松，导致 SPD 丢弃过多块而损失语义信息。

3. **模态限制。** 当前方法仅在图像数据集上验证，邻居识别和语义偏移阈值的定义依赖于图像特征提取器 $f(\cdot)$。对于文本、音频等模态，如何定义合适的语义空间和距离度量仍需进一步研究。

### 重要图表结论

- **Figure 1(c)**：BGFDQ（不含 SPD）相比基线减少 15%–35% 的总运行时间，同时验证准确率提升超过 1%；含 SPD 版本进一步提升超过 2%。
- **Table 2**：BGFDQ 在 CIFAR-10、CIFAR-100、ImageNet-1K 和 Fakeddit 四个数据集上，在多个核心集比例下均取得最优或次优的验证准确率。
- **Table 5**：NI+NCS 策略一致优于 RS 和 BG+RS，证明邻居语义信息比分组结构更有效。
- **Figure 4**：SPD 在丢弃 40% 块时仍保持与 PD(25%) 相当的准确率，验证了自适应丢弃机制的有效性。

![[assets/figures/papers/paper_list_l2688_https_openaccess_thecvf_com_content_CVPR2026_html_Deng_Is_Bin_Generation/figures/007_Figure_4.jpg]]
*Figure 4: Ablation study of patch dropping strategies. Different patch dropping strategies are applied to randomly selected samples from CIFAR-10 dataset and use it to train ResNet-18*

![[assets/figures/papers/paper_list_l2688_https_openaccess_thecvf_com_content_CVPR2026_html_Deng_Is_Bin_Generation/figures/005_Table_2.jpg]]
*Table 2: Overall performance of BGFDQ and baseline methods under different coreset fractions*

![[assets/figures/papers/paper_list_l2688_https_openaccess_thecvf_com_content_CVPR2026_html_Deng_Is_Bin_Generation/figures/009_Table_5.jpg]]
*Table 5: Validation accuracy (%) on CIFAR-10 using different coreset selection strategies*

### 补充图表

![[assets/figures/papers/paper_list_l2688_https_openaccess_thecvf_com_content_CVPR2026_html_Deng_Is_Bin_Generation/figures/004_Table_1.jpg]]
*Table 1: Component abbreviations used throughout this paper*



## 定位与知识库关联

### 1. 与数据集压缩方法的谱系关系

BGFDQ 处于**数据集量化**（Dataset Quantization）这一新兴技术线上，其直接前身是 **DQ**（Zhou et al., ICCV 2023）。DQ 首次提出了“分箱生成（bin generation）→ 核心集选择（coreset selection）→ 图像块丢弃（patch dropping）”的三阶段范式，通过子模函数优化将数据集划分为互不重叠的箱，再在每个箱内均匀采样以构建压缩数据集。

**ADQ**（Li et al., AAAI 2025）在 DQ 基础上引入了自适应箱权重，改进了分箱后的样本加权策略，但未触及分箱生成本身的计算瓶颈——其迭代选择过程的复杂度为 $O(CM^3)$，在大规模数据集上导致内存溢出（OOM）或耗时巨大。**DQAS**（Zhao et al., ECCV 2024）则从主动学习角度改进了采样策略，同样建立在分箱基础之上。

BGFDQ 的核心突破在于**完全消解了分箱生成步骤**，用基于 KNN 的邻居识别（Neighbor Identification）取而代之。这一替换不仅是工程上的加速（总运行时间减少 15%–35%），更带来了语义层面的优势：分箱生成依赖子模函数在全局范围内迭代选择，其覆盖率和冗余度受限于箱的划分质量；而邻居识别直接在样本粒度上捕获语义邻近关系，使得后续的核心集选择能够以更高的覆盖率（$R(S)$ 更小）和更低的冗余度（$\Gamma(S)$ 更大）构建代表性更强的压缩集（见 Equation (6)–(7) 及 Appendix A 的理论分析）。

在更广泛的数据集压缩谱系中，BGFDQ 区别于两类主流方法：
- **核心集选择方法**（如 **GradMatch**, Killamsetty et al., ICML 2021）：通常依赖梯度信息进行样本筛选，计算开销大，且未利用图像内部的块级冗余。
- **数据集蒸馏/浓缩方法**（如 **DM**, Zhao et al., WACV 2023）：通过合成少量样本来替代原始数据集，虽然压缩比极高，但合成过程计算密集，且合成样本的语义保真度难以保证。

BGFDQ 继承了数据集量化“选择+压缩”的思路，但通过语义驱动的自适应机制，在压缩效率与数据质量之间取得了更优的平衡。

### 2. 方法适用边界

**适用场景**：
- **大规模图像分类数据集**：在 CIFAR-10/100、ImageNet-1K 上均验证有效，尤其在 CIFAR-100 上验证准确率提升高达 5%。
- **极端类别不平衡或单类样本量巨大的场景**：在 Fakeddit 数据集（单类样本数 > 200K）上，现有分箱方法因 $O(CM^3)$ 复杂度而 OOM，BGFDQ 成功运行并取得显著性能提升（Table 2）。
- **对压缩效率有严格要求的场景**：BGFDQ (w/o SPD) 在所有对比方法中总运行时间最低，且精度高于 DQ 和 ADQ（Table 4）。

**不适用或需谨慎使用的场景**：
- **小规模数据集**：当样本量较小时，SPD 模块带来的额外计算开销可能抵消其精度收益，此时应优先使用 BGFDQ (w/o SPD)。
- **非图像模态**：当前方法的邻居识别基于图像特征提取器（如 ResNet-18）的嵌入空间，语义偏移阈值 $\lambda_C$ 的定义也依赖视觉特征的欧氏距离。对于文本、音频等模态，特征空间的结构和语义距离的物理含义不同，直接迁移可能失效。

### 3. 局限性与开放问题

**已知局限性**（论文明确提及）：
1. **SPD 的额外计算开销**：BGFDQ (w/ SPD) 虽然精度更高，但引入了额外的语义偏移评估计算，在样本量较小时性价比下降。
2. **模态限制**：仅在图像数据集上验证，未扩展到文本、音频等模态。
3. **$\lambda_C$ 的启发式性质**：语义偏移阈值 $\lambda_C$ 的计算基于类内最小非零距离的均值（取最小的 50 个非零距离平均），缺乏理论上的最优性保证。这一启发式设计在实际中有效（见 Figure 4 的消融实验），但其在不同数据分布下的鲁棒性尚待系统验证。

**开放问题**（值得后续探索的方向）：
1. **跨模态泛化**：如何为文本、音频等模态定义合适的邻居识别机制和语义偏移阈值？文本的语义距离是否应基于语言模型的特征空间？音频的时序结构如何纳入邻居定义？
2. **超参数自适应**：邻居感知选择策略中的超参数 $K$（邻居数，当前设为 20）和 $\alpha$（移除概率衰减系数）目前是固定的。能否根据数据集的类内密度、类别数等特性自动调节这些参数？
3. **自适应块丢弃的推广**：SPD 的核心思想——基于语义偏移约束自适应确定压缩率——是否可以推广到其他数据压缩任务，如神经网络剪枝（自适应确定每层的剪枝率）或知识蒸馏（自适应确定每个样本的蒸馏强度）？

### 4. 知识库定位总结

BGFDQ 在数据集量化技术线上完成了从“分箱依赖”到“语义驱动”的范式转换。其核心贡献不在于提出全新的压缩框架，而在于**识别并消解了分箱生成这一计算瓶颈**，同时用语义邻居关系替代了基于子模函数的全局分区。这一思路与近年来计算机视觉中“从全局结构到局部邻域”的范式迁移（如从全连接注意力到局部窗口注意力）形成呼应，暗示了在数据压缩领域，样本粒度的语义分析可能比全局聚类更高效且更保真。



## 原文 PDF

![[paperPDFs/CVPR_2026/Is_Bin_Generation_Indispensable_A_Bin_Generation_Free_Dataset_Quantization_via_Semantic_Perspective.pdf]]
