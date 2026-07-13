---
title: Scalable Multi-View Subspace Clustering with Tensorized Anchor Guidance
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Scalable_Multi_View_Subspace_Clustering_with_Tensorized_Anchor_Guidance.pdf
project_link: null
code_link: "https://github.com/Jiamiao2024/SMVS-TAG"
aliases:
- STSMVSCTAG
- SMVSCTAG
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 对由视图锚点构造的第三阶锚点张量直接施加张量Schatten p-范数低秩约束，将正则化目标从样本依赖的锚点图转移到锚点表示本身。
primary_logic: 在低维潜在空间中学习各视图的正交锚点，并将其堆叠为第三阶张量；沿锚点维度进行快速傅里叶变换（FFT），在频域对每个 frontal slice 施加 Schatten p-范数以显式挖掘跨视图低秩结构：低频分量聚合视图间共享的一致性信息，高频分量保留各视图特有信息，从而同步提升锚点质量与跨视图协同；该张量正则项的规模仅取决于锚点数量和聚类数，与样本数无关，大幅降低了大规模数据下的计算与内存开销。
claims:
- 构建第三阶锚点张量并施加张量Schatten p-范数约束，显式捕获跨视图低秩结构，同时利用一致性和互补性信息。
- 正则化目标从锚点图移至锚点表示，张量正则项与样本数无关，降低了时间和空间复杂度。
- 锚点矩阵被视为可优化变量，可从零初始化，避免了先验锚点选择导致的不稳定性。
- Dermatology 上 ACC = 97.49
---

# Scalable Multi-View Subspace Clustering with Tensorized Anchor Guidance

> [!tip] 核心洞察
> 在低维潜在空间中学习各视图的正交锚点，并将其堆叠为第三阶张量；沿锚点维度进行快速傅里叶变换（FFT），在频域对每个 frontal slice 施加 Schatten p-范数以显式挖掘跨视图低秩结构：低频分量聚合视图间共享的一致性信息，高频分量保留各视图特有信息，从而同步提升锚点质量与跨视图协同；该张量正则项的规模仅取决于锚点数量和聚类数，与样本数无关，大幅降低了大规模数据下的计算与内存开销。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于张量化锚引导的可扩展多视图子空间聚类 |
| 英文题名 | Scalable Multi-View Subspace Clustering with Tensorized Anchor Guidance |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Jia_Scalable_Multi-View_Subspace_Clustering_with_Tensorized_Anchor_Guidance_CVPR_2026_paper.html) · [Code](https://github.com/Jiamiao2024/SMVS-TAG) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | SMVS-TAG (Scalable Multi-view Subspace Clustering with Tensorized Anchor Guidance) |
| Dataset | Dermatology, Scene15, COIL100, Hdigit |

> [!tip] 效果简介
> - Dermatology 上，ACC 97.49 vs N/A (N/A)。
> - Scene15 上，ACC 61.00 vs N/A (N/A)。
> - COIL100 上，ACC 90.60 vs N/A (N/A)。

## 概要

多视图子空间聚类旨在从多个特征表示中挖掘样本间的一致性与互补性结构，以提升聚类质量。然而，现有基于锚的方法普遍面临一个关键瓶颈：各视图独立生成锚点，忽略了跨视图锚点间的交互关系，导致锚点表示噪声大、鲁棒性差，且对初始锚点选择高度敏感。同时，主流方法将正则化施加于锚点图（如拉普拉斯图或张量图），其计算复杂度与样本数线性相关，难以扩展至大规模数据。

针对上述问题，本文提出 **SMVS-TAG**（Scalable Multi-View Subspace Clustering with Tensorized Anchor Guidance），核心思路是将正则化目标从样本依赖的锚点图**迁移至锚点表示本身**。具体而言，方法在低维潜在空间中联合学习各视图的正交锚点，将其堆叠并旋转为第三阶锚点张量 $\mathcal{A} \in \mathbb{R}^{k \times v \times m}$（$k$ 为聚类数，$v$ 为视图数，$m$ 为锚点数），随后沿锚维度进行快速傅里叶变换（FFT），在频域对每个 frontal slice 施加 **Schatten p-范数**约束，以显式捕获跨视图低秩结构。低频分量聚合视图间共享的一致性信息，高频分量保留各视图特有信息，从而同步提升锚点质量与跨视图协同。

这一设计带来三方面优势：其一，锚点矩阵从零初始化且全程可优化，彻底移除了对先验锚点选择的依赖；其二，张量正则项的规模仅取决于锚点数量与聚类数，与样本数无关，大幅降低了大规模数据下的时间与空间复杂度；其三，Schatten p-范数提供了比张量核范数更紧致的秩近似，增强了低秩约束的有效性。

在七个多视图数据集上与十个大型/张量聚类基线的全面对比表明，SMVS-TAG 在 ACC、NMI、Purity 和 Fscore 指标上均取得领先或极具竞争力的结果。消融实验证实，张量锚正则化策略的一致增益显著，移除该模块后所有数据集性能均下降。参数敏感性分析显示，Schatten p-范数中的 $p$ 值在 0.1 附近达到最优，锚点数量 $m$ 设定为聚类数的 3 倍左右时性能最佳。运行时间对比中，该方法在中等规模数据上效率突出，但在超大规模数据集上内存占用仍较高，与部分基线接近。

**方法定位**：SMVS-TAG 属于基于锚的可扩展多视图子空间聚类方法，其核心创新在于将张量低秩正则化从图空间迁移到锚点表示空间，并与频域分解相结合。与 **LMVSC**、**SMVAGC**、**MCHBG** 等大型多视图聚类基线以及 **TBGL**、**TC-MVSC** 等张量方法基线相比，本方法在正则化目标、锚点学习方式和张量正则化维度三个关键设计点上实现了系统性改进。代码已开源，实验在统一硬件环境和公平超参搜索策略下完成，保证了可复现性。

**主要局限**在于超参数需手动调整，且当前仅验证于完整多视图场景，尚未扩展到缺失视图或流式增量数据。未来方向包括将张量锚正则化嵌入深度模型、自适应确定锚点数量，以及探索不完全多视图下的鲁棒性。

### 多视图聚类的规模化挑战

多视图数据在现实应用中普遍存在，例如同一对象通过不同传感器、特征提取器或模态获取的多组描述。多视图子空间聚类（Multi-View Subspace Clustering, MVSC）旨在利用视图间的一致性与互补性信息，将样本划分到其固有的低维子空间中。然而，传统MVSC方法通常需要构建大小为 $n \times n$ 的亲和矩阵并进行谱分解，其时间与空间复杂度随样本数 $n$ 呈平方或立方增长，难以应对大规模数据场景。

### 锚方法的兴起与瓶颈

为缓解计算瓶颈，基于锚（anchor）的大规模多视图聚类方法应运而生。这类方法从原始样本中选择或生成少量代表性锚点，用样本-锚点关系矩阵替代完整的样本-样本亲和矩阵，从而将复杂度从 $O(n^2)$ 降至 $O(nm)$（$m \ll n$ 为锚点数量）。在此范式下，锚点的质量直接决定了聚类性能的上限。

然而，现有锚方法存在两个关键瓶颈：

1. **视图间锚点独立生成，缺乏跨视图协同**：传统方法（如 **LMVSC**、**SMVAGC**、**MCHBG** 等）在各视图独立生成锚点，忽略了跨视图锚点间的交互关系。这导致无法有效发掘和利用视图间的一致性与互补性信息，锚点表示易受噪声污染或陷入次优。
2. **依赖初始锚点选择，鲁棒性不足**：多数方法采用 $k$-means 或随机采样预先选定固定锚点，聚类结果对初始锚点选择高度敏感，缺乏对锚点本身的优化机制。

### 张量正则化的局限

近期工作尝试引入张量低秩正则化来建模多视图数据的高阶结构（如 **TBGL**、**TC-MVSC**、**LMTC** 等）。这些方法对由各视图锚点图堆叠形成的**锚点图张量** $\boldsymbol{\mathcal{Z}} \in \mathbb{R}^{m \times v \times n}$ 施加低秩约束，以挖掘跨视图相关性。但正则化目标锚定在锚点图上，张量规模与样本数 $n$ 线性相关，在大规模数据下仍面临显著的计算与内存压力。此外，张量正则化的潜在能力——直接约束锚点表示本身的跨视图低秩结构——尚未被充分探索。

### 本文动机

上述分析揭示了两个核心改进方向：

- **正则化目标的转移**：将低秩约束从样本依赖的锚点图转移到锚点表示本身，使正则化规模仅取决于锚点数量 $m$ 和聚类数 $k$，与样本数 $n$ 解耦，从根本上降低大规模场景下的时空开销。
- **锚点的联合可学习化**：将锚点视为可优化变量，在潜在空间中联合学习所有视图的正交锚点，消除对先验锚点选择的依赖，同时通过正交约束增强锚点的判别性与多样性。

基于此，本文提出 **SMVS-TAG**（Scalable Multi-View Subspace Clustering with Tensorized Anchor Guidance），通过构建第三阶锚点张量并施加张量 Schatten $p$-范数正则化，在频域显式捕获跨视图低秩结构，同步提升锚点质量与跨视图协同效率。

## 核心方法与创新机理

### 创新动机：锚点独立生成导致跨视图信息割裂

现有基于锚点的大规模多视图聚类方法（如 **LMVSC**、**SMVAGC**、**MCHBG** 等）通常在各视图内独立生成锚点，再通过锚点图进行融合。这种范式存在一个根本性瓶颈：**锚点生成过程忽略了跨视图锚点间的交互关系**，无法有效发现和利用视图间的一致性与互补性信息。其后果是锚点表示质量受限于初始锚点选择，噪声大且鲁棒性差——一旦初始锚点选取不当，后续聚类性能将显著退化。

### 核心创新：从“锚点图正则”到“锚点张量正则”的范式转移

SMVS-TAG 的核心创新在于**将正则化目标从锚点图转移到锚点表示本身**，实现了三个关键维度的突破：

#### 1. 正则化目标的根本性改变

传统方法对锚点图（如拉普拉斯图或样本依赖的锚点图张量）施加低秩或平滑约束，其正则化效果间接依赖于样本分布。SMVS-TAG 则直接对由视图特定锚点构造的**第三阶锚点张量**施加张量 Schatten p-范数正则化，将约束直接作用于锚点表示的低秩结构。这一改变使得正则化不再受样本数量影响，从根本上解耦了锚点质量与样本规模的依赖关系。

#### 2. 锚点学习方式的彻底重构

传统方法要么预先选定固定锚点（如随机采样、k-means 聚类中心），要么在各视图独立学习锚点，均无法保证跨视图锚点的协同最优。SMVS-TAG 将锚点矩阵 $\mathbf{A}_i$ 视为**从零初始化且全程可优化的变量**，在低维潜在空间中联合学习所有视图的正交锚点。正交约束 $\mathbf{A}_i\mathbf{A}_i^\top = \mathbf{I}$ 使学习到的锚点更具判别性和多样性，同时完全移除了对先验锚点选择的需求，消除了初始锚点敏感性这一长期困扰锚点方法的顽疾。

#### 3. 张量正则化维度的结构性压缩

传统张量多视图聚类方法（如 **TBGL**、**TC-MVSC**、**LMTC**）对形状为 $m \times v \times n$ 的锚点图张量进行正则化，其计算量和内存占用与样本数 $n$ 线性相关，在大规模数据下极易遭遇内存溢出（Out-of-Memory）。SMVS-TAG 构建的锚点张量 $\boldsymbol{\mathcal{A}} \in \mathbb{R}^{k \times v \times m}$ 仅依赖于锚点数 $m$ 和聚类数 $k$，与样本数 $n$ 完全无关。这一维度压缩带来了**时间与空间复杂度的数量级降低**，使得张量正则化首次在大规模多视图聚类中变得切实可行。

### 频域低秩挖掘：一致性与互补性的统一建模

锚点张量构建后，SMVS-TAG 沿锚点维度进行快速傅里叶变换（FFT），在频域对每个 frontal slice 施加 Schatten p-范数约束。这一设计的精妙之处在于：

- **低频分量**聚合了跨视图共享的一致性信息，低秩约束强化了视图间的结构对齐；
- **高频分量**保留了各视图的特有信息与噪声，适度的 p-范数惩罚在保留互补性的同时抑制噪声。

通过频域分解，SMVS-TAG 实现了**一致性与互补性的统一建模**——既非简单地对齐所有视图（丢失互补性），也非独立保留各视图信息（忽略一致性），而是在低秩约束的引导下自适应地平衡二者。

### 创新点总结

| 维度 | 传统锚点方法 | SMVS-TAG |
|------|------------|----------|
| 正则化目标 | 锚点图（样本依赖） | 锚点张量（样本无关） |
| 锚点获取 | 预选固定/独立学习 | 联合优化、零初始化 |
| 张量维度 | $m \times v \times n$ | $k \times v \times m$ |
| 跨视图建模 | 间接（图融合） | 直接（频域低秩） |
| 初始锚点依赖 | 强依赖 | 完全消除 |

这些创新共同构成了一个从“锚点图正则”到“锚点张量正则”的完整范式转移，使得 SMVS-TAG 在保持大规模可扩展性的同时，显著提升了锚点质量与跨视图协同能力。

SMVS-TAG 的整体设计遵循“潜在锚点学习 → 锚点张量构建 → 频域低秩正则化 → 共识锚图生成”的四阶段流水线。该框架的核心创新在于将正则化目标从传统的**样本依赖的锚点图**迁移到**锚点表示本身**，从而在低维空间内完成跨视图协同，大幅降低大规模数据下的计算与内存开销。

**输入与输出**：方法接收 $v$ 个视图的原始特征矩阵 $\mathbf{X}_i \in \mathbb{R}^{d_i \times n}$（$d_i$ 为第 $i$ 视图的特征维度，$n$ 为样本数），输出为一个共享的非负锚图 $\mathbf{Z} \in \mathbb{R}^{m \times n}$（$m$ 为锚点数量），最终对 $\mathbf{Z}$ 的左奇异向量执行 k-means 获得聚类结果。

### 模块一：视图特定正交锚点生成

对于每个视图，SMVS-TAG 在低维潜在空间中学习一组**可优化的正交锚矩阵** $\mathbf{A}_i \in \mathbb{R}^{k \times m}$，其中 $k$ 为聚类数。与传统方法预先选定固定锚点不同，此处的 $\mathbf{A}_i$ 从零初始化，并在整个优化过程中作为变量迭代更新，完全移除了对先验锚点选择的依赖。正交约束 $\mathbf{A}_i \mathbf{A}_i^\top = \mathbf{I}$ 使得各锚点更具判别性和多样性，为后续张量构建提供高质量的视图特定表示。

### 模块二：锚点张量构建

将所有视图的锚矩阵合并并旋转，构造一个**第三阶锚点张量** $\boldsymbol{\mathcal{A}} \in \mathbb{R}^{k \times v \times m}$。该张量的三个模态分别对应聚类数、视图数和锚点数，其规模仅取决于 $(k, v, m)$，与样本数 $n$ 完全无关。这一设计是计算效率提升的关键——相比之下，传统方法基于锚点图张量 $\boldsymbol{\mathcal{Z}} \in \mathbb{R}^{m \times v \times n}$ 进行正则化，计算量与 $n$ 线性相关。

### 模块三：频域张量低秩正则化

沿锚点维度对 $\boldsymbol{\mathcal{A}}$ 执行快速傅里叶变换（FFT），将张量变换到频域。频域中每个 frontal slice 捕获了跨视图锚点间的交互信息：**低频切片**聚合各视图共享的一致性信息，**高频切片**保留各视图的特有信息及噪声。随后对每个频域切片施加 Schatten $p$-范数低秩约束，显式挖掘跨视图低秩结构，实现一致性与互补性的联合利用。

### 模块四：投影矩阵学习与共识锚图构建

为将潜在锚点映射回原始特征空间，框架引入一组正交投影矩阵 $\mathbf{W}_i \in \mathbb{R}^{d_i \times k}$，通过最小化重构误差 $\|\mathbf{X}_i - \mathbf{W}_i \mathbf{A}_i \mathbf{Z}\|_F^2$ 来学习。所有视图共享同一个共识锚图 $\mathbf{Z}$，其每一列 $\mathbf{z}_j$ 满足非负与归一化约束（$\mathbf{z}_j^\top \mathbf{1} = 1, \mathbf{z}_j \geq 0$），可解释为样本 $j$ 对各锚点的隶属度分布。

### 总体目标函数

上述模块被整合为统一的目标函数：

$$\min_{\mathbf{W}_i, \mathbf{A}_i, \mathbf{Z}} \alpha \sum_{i=1}^{v} \|\mathbf{X}_i - \mathbf{W}_i\mathbf{A}_i\mathbf{Z}\|_F^2 + \lambda\|\mathbf{Z}\|_F^2 + \|\boldsymbol{\mathcal{A}}\|_{\mathrm{S}_p}^p$$

其中第一项为多视图数据重构损失，第二项为锚图平滑正则，第三项为锚点张量的 Schatten $p$-范数低秩正则。优化采用交替优化策略，引入辅助变量 $\boldsymbol{\mathcal{H}}$ 后构造增广拉格朗日函数，迭代更新 $\mathbf{W}_i$、$\mathbf{A}_i$、$\mathbf{Z}$ 和 $\boldsymbol{\mathcal{H}}$ 直至收敛（完整流程见 Algorithm 1）。

**Figure 2** 直观展示了上述流水线：各视图锚点在潜在空间学习后堆叠为锚点张量，经 FFT 变换到频域进行低秩正则化，最终通过共享锚图实现聚类。**Figure 1** 则从方法论层面对比了传统锚方法与 SMVS-TAG 的本质差异——前者独立生成锚点后构造共识图，后者将锚点重构为张量并直接施加跨视图低秩约束，从而获得更高质量的共识锚图。

![[assets/figures/papers/paper_list_l2110_https_openaccess_thecvf_com_content_CVPR2026_html_Jia_Scalable_Multi_Vie/figures/002_Figure_2.jpg]]
*Figure 2: The framework of our proposed SMVS-TAG. Specifically, anchors for each view are learned in a latent space and the anchor tensor is constructed. Applying FFT to A along the anchor dimension, each frontal slice captures cross-view interactive information among anchors. Low-frequency slices aggregate consistent information shared across views, while high-frequency slices contain view-specific information and noise*

### 整体目标函数

SMVS-TAG 的核心优化问题统一了数据重构、图平滑与锚点张量低秩正则三个目标：

$$
\min_{\mathbf{W}_i,\mathbf{A}_i,\mathbf{Z}} \alpha \sum_{i=1}^{v} \|\mathbf{X}_i - \mathbf{W}_i\mathbf{A}_i\mathbf{Z}\|_F^2 + \lambda\|\mathbf{Z}\|_F^2 + \|\boldsymbol{\mathcal{A}}\|_{\mathrm{S}_p}^p
$$

其中 $\mathbf{X}_i \in \mathbb{R}^{d_i \times n}$ 为第 $i$ 个视图的数据矩阵，$\mathbf{W}_i$ 为视图特定的正交投影矩阵，$\mathbf{A}_i$ 为视图特定锚点矩阵，$\mathbf{Z}$ 为共享的非负锚图，$\boldsymbol{\mathcal{A}}$ 为由各视图锚点构造的第三阶张量。第一项约束原始数据可由锚点与锚图重构，第二项防止 $\mathbf{Z}$ 过拟合，第三项对锚点张量施加 Schatten $p$-范数以捕获跨视图低秩结构。

### 锚点张量构建与频域正则化

各视图锚点矩阵 $\mathbf{A}_i \in \mathbb{R}^{k \times m}$（$k$ 为聚类数，$m$ 为锚点数量）经堆叠与旋转后形成锚点张量 $\boldsymbol{\mathcal{A}} \in \mathbb{R}^{k \times v \times m}$。沿锚点维度对 $\boldsymbol{\mathcal{A}}$ 执行快速傅里叶变换（FFT），得到频域张量 $\widehat{\boldsymbol{\mathcal{A}}}$，其每个 frontal 切片 $\widehat{\boldsymbol{\mathcal{A}}}^i \in \mathbb{R}^{k \times v}$ 捕获跨视图锚点间的交互信息。

张量 Schatten $p$-范数定义为：

$$
\|\boldsymbol{\mathcal{B}}\|_{\mathrm{S}_p}^p = \sum_{i=1}^{n_3} \|\widehat{\boldsymbol{\mathcal{B}}}^i\|_{\mathrm{S}_p}^p = \sum_{i=1}^{n_3} \sum_{j=1}^{h} \widehat{S}_{\boldsymbol{\mathcal{B}}}^i(j,j)^p
$$

其中 $\widehat{S}_{\boldsymbol{\mathcal{B}}}^i(j,j)$ 为第 $i$ 个 frontal 切片经 t-SVD 后的奇异值。该范数比张量核范数（$p=1$）更紧致地逼近张量秩，通过调节 $p \in (0,1]$ 可灵活控制低秩强度。在频域施加此约束的机理为：低频切片聚合视图间共享的一致性信息，高频切片保留各视图特有信息与噪声，低秩正则促使跨视图锚点表示在低维流形上对齐。

### 增广拉格朗日形式与交替优化

引入辅助变量 $\boldsymbol{\mathcal{H}}$ 解耦非光滑正则项后，得到增广拉格朗日函数：

$$
\mathcal{L}(\mathbf{W}_{1:v}, \boldsymbol{\mathcal{H}}, \mathbf{A}_{1:v}, \mathbf{Z}) = \|\boldsymbol{\mathcal{H}}\|_{\mathrm{S}_p}^p + \alpha \sum_{i=1}^{v} \|\mathbf{X}_i - \mathbf{W}_i\mathbf{A}_i\mathbf{Z}\|_F^2 + \lambda\|\mathbf{Z}\|_F^2 + \langle \boldsymbol{\mathcal{V}}, \boldsymbol{\mathcal{A}} - \boldsymbol{\mathcal{H}} \rangle + \frac{\rho}{2}\|\boldsymbol{\mathcal{A}} - \boldsymbol{\mathcal{H}}\|_F^2
$$

采用交替优化策略依次更新各变量：

- **$\mathbf{W}_i$ 更新**：转化为迹最大化问题 $\max_{\mathbf{W}_i} \mathrm{Tr}(\mathbf{W}_i^\top \mathbf{D}_i)$，约束 $\mathbf{W}_i^\top \mathbf{W}_i = \mathbf{I}$，可通过特征分解求得闭式解。
- **$\boldsymbol{\mathcal{H}}$ 更新**：在频域分解为 $m$ 个独立矩阵子问题 $\min_{\widehat{\mathcal{H}}^{i}} \frac{1}{\rho} \|\widehat{\mathcal{H}}^{i}\|_{\mathrm{S}_p}^{p} + \frac{1}{2} \|\widehat{\mathcal{H}}^{i} - \widehat{\mathcal{M}}^{i}\|_F^2$，各切片可并行求解。
- **$\mathbf{A}_i$ 更新**：带正交约束的最小二乘问题，可通过奇异值分解高效求解。
- **$\mathbf{Z}$ 更新**：分解为 $n$ 个独立的二次规划子问题：

$$
\min_{\mathbf{z}_j} \frac{1}{2}\mathbf{z}_j^{\top}\mathbf{G}\mathbf{z}_j + \mathbf{f}^{\top}\mathbf{z}_j, \quad \mathrm{s.t.} \; \mathbf{z}_j^{\top}\mathbf{1}=1,\; \mathbf{z}_j \geq 0
$$

每个子问题仅涉及 $m$ 维变量，可并行处理，适用于大规模样本场景。

### 复杂度分析

锚点张量 $\boldsymbol{\mathcal{A}} \in \mathbb{R}^{k \times v \times m}$ 的规模仅依赖于锚点数 $m$ 和聚类数 $k$，与样本数 $n$ 无关。相比之下，传统张量方法在锚图张量 $\boldsymbol{\mathcal{Z}} \in \mathbb{R}^{m \times v \times n}$ 上正则化，其第三维随 $n$ 线性增长。这一设计使 SMVS-TAG 的时空间复杂度在大规模数据下显著降低。

![[assets/figures/papers/paper_list_l2110_https_openaccess_thecvf_com_content_CVPR2026_html_Jia_Scalable_Multi_Vie/figures/001_Figure_1.jpg]]
*Figure 1: Comparison between traditional anchor-based MVC methods (left) and our proposed SMVS-TAG (right). Traditional methods independently generate view-specific anchors to construct a consensus anchor graph. Our method reconstructs these view-specific anchors into a third-order tensor, employing a tensor Schatten p-norm constraint to explicitly capture cross-view consistency and complementarity, resulting in a higher-quality consensus anchor graph*

## 实验与关键发现

### 主实验结果

SMVS-TAG 在七个多视图基准数据集上与十种大规模多视图聚类方法进行了全面对比，评价指标包括 ACC、NMI、Purity 和 Fscore。**Table 2** 汇总了各方法在所有数据集上的聚类性能。SMVS-TAG 在绝大多数数据集上取得了最优或次优结果，尤其在小规模数据集上优势显著：在 Dermatology 上 ACC 达到 **97.49%**，在 Scene15 上达到 **61.00%**，在 COIL100 上达到 **90.60%**，在 Hdigit 上达到 **92.52%**。

![[assets/figures/papers/paper_list_l2110_https_openaccess_thecvf_com_content_CVPR2026_html_Jia_Scalable_Multi_Vie/figures/004_Table_2.jpg]]
*Table 2: Clustering performance comparison of the proposed SMVS-TAG method and ten large-scale MVC methods on seven multi-view datasets. The best and second-best results are represented by bold and underlined values, respectively*

在大规模数据集上，SMVS-TAG 同样保持竞争力。在 AwA（30,475 样本、50 类、6 视图）和 VGGFace（36,287 样本、100 类、4 视图）上，该方法均取得领先或接近最优的聚类精度。然而，在 YoutubeFace（101,499 样本、31 类、5 视图）上 ACC 为 **36.62%**，提升幅度相对有限，表明超大规模场景下性能增益有所收窄。

性能优势的核心驱动力在于：SMVS-TAG 将正则化目标从样本依赖的锚点图转移到锚点表示本身，通过张量 Schatten p-范数显式捕获跨视图低秩结构，同时利用一致性与互补性信息。此外，锚点矩阵作为可优化变量从零初始化，消除了对先验锚点选择的依赖，提升了鲁棒性。

### 运行时间分析

**Table 3** 给出了各方法在七个数据集上的运行时间对比（单位：秒）。SMVS-TAG 在中等规模数据集上展现出显著的效率优势，这得益于其张量正则项的规模仅依赖于锚点数量 $m$ 和聚类数 $k$，与样本数 $n$ 无关。相比之下，传统张量方法（如 TBGL、TC-MVSC）需对形状为 $m \times v \times n$ 的锚点图张量进行正则化，计算开销随 $n$ 线性增长。

在 YoutubeFace 等超大规模数据集上，SMVS-TAG 的运行时间优势缩小，内存占用仍然较高，与部分基线方法接近。表中部分方法出现 "OT"（超时）或 "OM"（内存溢出）错误，进一步凸显了可扩展性在大规模多视图聚类中的关键瓶颈。

### 消融实验

**Table 4** 展示了张量锚（TA）策略的消融结果。移除 TA 策略后，在所有数据集上聚类性能一致下降，验证了直接在锚点表示上进行张量低秩正则化的关键作用。具体而言，TA 策略的核心贡献体现在两方面：一是将视图锚点堆叠为第三阶张量 $\mathcal{A} \in \mathbb{R}^{k \times v \times m}$，二是沿锚维度进行 FFT 后在频域施加 Schatten p-范数约束，使低频分量聚合跨视图共享的一致性信息，高频分量保留各视图特有信息。

### 参数敏感性

**Figure 3** 展示了 Schatten p-范数中参数 $p$ 的敏感性。在 Dermatology 和 Scene15 上，$p$ 在 **0.1 附近**达到最优性能，表明适中的低秩强度最有利于跨视图锚点协同。$p \to 0$ 时近似张量秩，约束过强可能损失有用信息；$p \to 1$ 时退化为张量核范数，低秩约束过于松弛。

**Figure 4** 展示了锚点数量 $m$ 的影响。当 $m$ 设定为聚类数 $k$ 的 **3 倍左右**时性能最佳，过少的锚点无法充分表示数据结构，过多的锚点则引入冗余和噪声。

**Figure 5** 展示了参数 $\alpha$（重构损失权重）和 $\lambda$（图平滑权重）的敏感性。两个参数在较宽范围内均能保持稳定性能，表明方法对这两个超参数具有较好的鲁棒性。

### 收敛性分析

**Figure 6** 给出了目标函数值随迭代次数的变化曲线。在 Dermatology 和 Scene15 上，目标函数值快速下降并在有限迭代内收敛，验证了交替优化策略的有效性和数值稳定性。

### 失败模式与局限性

尽管 SMVS-TAG 在多数场景下表现优异，仍存在以下值得关注的局限：

1. **超大规模数据效率衰减**：在 YoutubeFace（10 万+ 样本）上，运行时间优势明显缩小，内存占用仍然可观。虽然张量正则项本身与样本数无关，但锚图 $\mathbf{Z} \in \mathbb{R}^{m \times n}$ 的更新涉及 $n$ 个二次规划子问题，成为大规模场景下的计算瓶颈。

2. **超参数依赖**：$p$、$\alpha$、$\lambda$ 和 $m$ 需要针对每个数据集手动调整。参数敏感性实验表明，不当选择（如 $p$ 过大或 $m$ 过小）会导致性能显著下降。目前方法缺乏自适应参数选择机制。

3. **正交约束的表示局限**：锚点学习采用正交约束以增强判别性和多样性，但可能限制了表示灵活性。该方法尚未探索与其他约束（如非负、稀疏）的组合效果，在特定数据分布下可能次优。

4. **缺失视图未验证**：当前方法设计用于完整多视图场景，尚未验证在缺失视图或不完全多视图数据下的有效性，限制了其在真实世界不完整数据上的应用。

![[assets/figures/papers/paper_list_l2110_https_openaccess_thecvf_com_content_CVPR2026_html_Jia_Scalable_Multi_Vie/figures/007_Table_4.jpg]]
*Table 4: Ablation study on tensor anchor (TA) strategy*

![[assets/figures/papers/paper_list_l2110_https_openaccess_thecvf_com_content_CVPR2026_html_Jia_Scalable_Multi_Vie/figures/005_Table_3.jpg]]
*Table 3: Running time comparison of the proposed SMVS-TAG method and ten large-scale MVC methods. Note that, the time is in seconds. ‘OT ’ indicates the “out-of-time error”, ‘OM ’ means the “out-of-memory error”*

![[assets/figures/papers/paper_list_l2110_https_openaccess_thecvf_com_content_CVPR2026_html_Jia_Scalable_Multi_Vie/figures/003_Table_1.jpg]]
*Table 1: A brief summary of multi-view datasets*

## 定位与知识库关联

### 1. 方法谱系：从锚图正则化到锚点张量正则化

SMVS-TAG 的核心贡献在于将多视图子空间聚类的**正则化目标从“样本依赖的锚点图”迁移到“锚点表示本身”**，这一位移决定了它在方法谱系中的独特位置。

**传统锚方法范式。** 以 LMVSC、3AMVC、SMVAGC、AEVC、MVSC-HFD、MCHBG 等为代表的大规模多视图聚类方法，通常遵循“视图锚点选择 → 锚点图构建 → 锚点图正则化”的流程。它们的正则化施加在锚点图（如拉普拉斯图或张量图）上，图的大小与样本数 $n$ 线性相关，导致在大规模数据下计算与内存开销显著。更重要的是，这些方法在各视图独立生成锚点，**忽略了跨视图锚点间的交互关系**，无法系统性地发掘一致性与互补性信息。

**张量方法范式。** TBGL、Orth-NTF、TC-MVSC、LMTC 等张量方法引入了张量低秩约束来建模多视图关系，但其正则化对象通常是形状为 $m \times v \times n$ 的锚点图张量，计算量仍与样本数 $n$ 绑定。SMVS-TAG 的突破在于将张量正则化直接施加于形状为 $k \times v \times m$ 的**锚点张量** $\boldsymbol{\mathcal{A}}$，其规模仅依赖于锚点数 $m$ 和聚类数 $k$，与 $n$ 无关——这一维度缩减是效率提升的结构性原因。

**核心因果机制。** SMVS-TAG 在低维潜在空间中联合学习各视图的正交锚点矩阵 $\mathbf{A}_i$，将其堆叠并旋转为第三阶锚点张量；沿锚点维度进行快速傅里叶变换（FFT）后，对每个频域 frontal slice 施加 Schatten $p$-范数约束。低频分量聚合跨视图共享的一致性信息，高频分量保留各视图特有信息与噪声——这种频域解耦机制使得模型能够**同时利用一致性与互补性**，而非像传统方法那样仅追求一致性融合。

### 2. 适用边界与条件依赖

**数据规模边界。** SMVS-TAG 的设计优势在中等规模多视图数据上最为显著：当样本数 $n$ 远大于锚点数 $m$ 时，张量正则项与 $n$ 无关的特性带来可观的效率增益。然而在超大规模数据集（如 10 万样本的 YoutubeFace）上，运行时间优势缩小，内存占用仍然可观（Table 3 中部分基线出现内存溢出），说明方法的主要瓶颈从张量正则化转移到了数据重构项 $\|\mathbf{X}_i - \mathbf{W}_i\mathbf{A}_i\mathbf{Z}\|_F^2$ 的计算。

**锚点数量敏感性。** 消融实验和参数分析表明，锚点数量 $m$ 设定为聚类数 $k$ 的约 3 倍时性能最优；过少则锚点表示能力不足，过多则引入冗余噪声（Figure 4）。这意味着方法对 $m$ 的选择有一定依赖性，且当前缺乏自适应的锚点数量确定机制。

**超参数敏感性。** Schatten $p$-范数中的 $p$ 值在 0.1 附近达到最优（Figure 3），表明适中的低秩强度最有利于跨视图锚点协同。参数 $\alpha$ 和 $\lambda$ 同样需要针对数据集调整（Figure 5），不当选择会导致性能下降。这些超参数的手动调节需求构成了实际部署中的一个工程负担。

**视图完整性假设。** 当前方法设计针对完整多视图场景，尚未验证在缺失视图或不完全多视图数据下的有效性。正交锚点约束虽增强了判别性，但可能局限了表示灵活性。

### 3. 局限与开放问题

**已确认局限。**
- **超参数调节负担**：$p$、$\alpha$、$\lambda$ 和 $m$ 需针对每个数据集手动设定，参数敏感性实验证实不当选择会导致性能下降。
- **大规模边界效应**：在 YoutubeFace（101,499 样本）上，SMVS-TAG 的效率优势相对部分基线缩小，内存占用仍处于较高水平。
- **视图完整性依赖**：方法未在不完全多视图场景下验证，对缺失视图的鲁棒性未知。
- **锚点约束单一性**：仅采用正交约束，未探索与非负、稀疏等约束的组合效果，可能限制表示空间的丰富性。

**开放问题。**
- **深度化扩展**：能否将张量锚正则化策略嵌入深度多视图模型，实现端到端的特征学习与锚点优化？
- **自适应锚点选择**：如何自适应地确定各视图的最佳锚点数量，避免人工设定对性能的限制？
- **鲁棒性边界**：当跨视图锚点遭受严重噪声或大量缺失时，张量 Schatten $p$-范数是否仍能保持鲁棒？
- **增量与流式场景**：该框架可否推广到不完全多视图聚类，并支持新增视图或流式增量数据？
- **概率解释性**：张量锚正则化是否可被解释为一种贝叶斯先验，从而给出概率聚类结果并提升可解释性？

## 原文 PDF

![[paperPDFs/CVPR_2026/Scalable_Multi_View_Subspace_Clustering_with_Tensorized_Anchor_Guidance.pdf]]
