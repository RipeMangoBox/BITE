---
title: "3DCS: Datasets and Benchmark for Evaluating Conformational Sensitivity in Molecular Representations"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/3DCS_Datasets_and_Benchmark_for_Evaluating_Conformational_Sensitivity_in_Molecular_Representations.pdf
aliases:
- 33CSBGEF
- 3DBECSMR
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "GCE评估框架中的参考对齐（reference alignment）和流形一致性（manifold consistency）两层指标，以及三个专门设计的数据集（松弛扫描、手性药物候选物、AIMD轨迹）。"
primary_logic: "现代数据驱动的3D分子表示在几何敏感性上表现良好，但在手性区分上不一致，且与能量景观的对齐普遍较差；而经过能量/力监督训练的模型（如GemNet、MACE）在能量对齐上显著优于其他方法。"
claims:
- "几乎所有学习到的表示在几何基准上都优于手工描述符（如E3FP）。"
- "MolSpectra在几何基准上取得了最高的Spearman相关系数（0.682）。"
- "MolAE在手性基准上取得了最高的ES-AUC（0.782）。"
- "MACE在能量基准上取得了最高的Spearman相关系数（0.236）和EJS（0.578）。"
---

# 3DCS: Datasets and Benchmark for Evaluating Conformational Sensitivity in Molecular Representations

> [!tip] 核心洞察
> 现代数据驱动的3D分子表示在几何敏感性上表现良好，但在手性区分上不一致，且与能量景观的对齐普遍较差；而经过能量/力监督训练的模型（如GemNet、MACE）在能量对齐上显著优于其他方法。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 3DCS：评估分子表示中构象敏感性的数据集与基准 |
| 英文题名 | 3DCS: Datasets and Benchmark for Evaluating Conformational Sensitivity in Molecular Representations |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=JAb0y8lkqL); [GitHub](https://github.com/ComDec/3DCS) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | 3DCS (3D Conformational Sensitivity) benchmark with GCE evaluation framework |
| Dataset | Geometry (Relaxed Scans), Chirality (ChEMBL) |

> [!tip] 效果简介
> - Geometry (Relaxed Scans) 上，Spearman (↑) 为 MolSpectra: 0.682，对比 E3FP: 0.155，变化 +0.527。
> - Geometry (Relaxed Scans) 上，Kendall (↑) 为 MolSpectra: 0.483，对比 E3FP: 0.107，变化 +0.376。
> - Geometry (Relaxed Scans) 上，CKA (↑) 为 MolAE: 0.975，对比 E3FP: 0.299，变化 +0.676。

## 概述

3DCS（3D Conformational Sensitivity）是首个系统性评估分子表示（MRs）中构象敏感性的基准，由ICLR 2026接收。其核心瓶颈在于：现有分子表示方法在捕捉同一分子内不同构象的几何变化、手性差异和能量景观方面缺乏系统性评估，尤其是能量敏感性被严重忽视。为此，3DCS提出了GCE评估框架，通过参考对齐（reference alignment）和流形一致性（manifold consistency）两层指标，在几何、手性和能量三个维度上评估表示质量。

方法定位上，3DCS包含三个专门数据集：松弛扫描数据集（约150万分子、约1000万构象，使用xTB半经验方法优化）、手性药物候选物数据集（约4000分子、约52000构象，包含Murcko骨架划分以避免泄露）、以及基于AIMD轨迹的能量数据集（10个小有机分子，每个10万构象）。评估覆盖经典3D手工指纹E3FP和六类学习表示：SE(3)-等变Transformer（UniMol、MolAE）、几何消息传递网络（GemNet）、多模态模型（MolSpectra）、E(3)-等变原子模型（MACE）以及基于场的生成模型（FMG）。

主要结果表明：几乎所有学习表示在几何基准上均优于E3FP（如：MolSpectra在Spearman相关系数上达0.682，而E3FP仅0.155）；在手性基准上，MolAE取得最高ES-AUC（0.782），FMG取得最高NN1-acc（0.726）；在能量基准上，经能量/力监督训练的MACE取得最高Spearman（0.236）和EJS（0.578），FMG取得最高TS（0.582）。核心发现是：现代数据驱动的3D分子表示在几何敏感性上表现良好，但在手性区分上不一致，且与能量景观的对齐普遍较差。经过能量/力监督训练的模型（GemNet、MACE）在能量对齐上显著优于其他方法，但整体能量敏感性仍为开放挑战。

## 背景与动机

分子表示学习（Molecular Representations, MRs）旨在将分子的结构与物理化学性质编码为可供下游任务（如性质预测、虚拟筛选）使用的向量或张量。近年来，基于三维几何的深度学习方法（如SE(3)-等变Transformer、几何消息传递网络）在处理分子静态结构方面取得了显著进展。然而，现有基准（如MoleculeNet、Molecule3D、MARCEL）的评估范式存在一个根本性缺口：它们几乎全部聚焦于**分子间**任务（如跨分子分类、性质回归），将每个分子视为一个静态实体，忽略了同一分子内部不同构象（conformer）之间的几何变化、手性差异和能量景观。

这一缺口的实际瓶颈在于：分子并非刚性结构，其物理化学行为（如结合亲和力、反应路径、光谱性质）强烈依赖于构象系综的分布与动态。如果一个分子表示模型无法区分同一分子的不同构象——例如，无法感知一个二面角旋转带来的能量升高，或无法区分一对对映体——那么它在药物设计、催化机理分析等需要精细构象敏感性的场景中将产生不可靠的预测。现有方法对这一“构象敏感性”缺乏系统性的评估框架，尤其是**能量敏感性**被严重忽视：大多数模型仅通过坐标预测或性质回归间接学习能量信息，而非直接评估表示空间与势能面之间的对齐程度。

为填补这一空白，3DCS（3D Conformational Sensitivity）提出了第一个专门评估分子表示中构象敏感性的基准。其核心设计是GCE评估框架，包含两个层次的因果旋钮：**参考对齐（reference alignment）** 测试表示距离是否与物理参考（如RMSD、手性签名、能量差）的序关系一致；**流形一致性（manifold consistency）** 则评估表示空间是否形成连贯的流形，能否保持局部邻域结构、分离对映体、反映能量跳跃。配合三个专门构建的数据集——松弛扫描（~1.5M分子，~10M构象）、手性药物候选物（~4K分子，~52K构象）和AIMD轨迹（10个分子，每分子100K构象）——该框架系统性地覆盖了几何、手性和能量三个维度。

现有方法在该框架下的表现揭示了显著的差距：几乎所有学习到的表示在几何基准上都优于手工描述符（如E3FP），其中MolSpectra在几何基准上取得了最高的Spearman相关系数（0.682）；在手性区分上，MolAE取得了最高的ES-AUC（0.782），但整体表现不一致，SE(3)-等变模型在手性分离上普遍较弱；而在能量基准上，所有方法的绝对性能都很低——MACE取得了最高的Spearman相关系数（0.236）和EJS（0.578），FMG取得了最高的TS（0.582），但这些数值远低于几何基准的水平，说明**能量景观的对齐是当前分子表示学习中最薄弱的环节**。这些发现表明，3DCS基准不仅揭示了现有方法的性能边界，也为未来设计更具物理可信度的分子表示模型提供了明确的方向。

## 核心创新

3DCS的核心创新在于将分子表示评估从传统的**分子间任务性能**（如性质预测）转向**分子内构象敏感性**，即系统性地衡量同一分子不同构象的表示是否忠实反映了几何变化、手性差异和能量景观。这一转变揭示了现有评估范式的根本瓶颈：大量工作优化了分子层面的预测精度，却忽视了表示对构象空间内部物理结构的编码能力，特别是能量敏感性几乎未被触及。

实现这一转变的关键因果机制是**GCE（几何-手性-能量）评估框架**与**三个专门设计的大规模数据集**的耦合。GCE框架通过两层指标——参考对齐（reference alignment）和流形一致性（manifold consistency）——将“表示质量”从单一预测精度分解为多个可诊断的物理维度。参考对齐直接检验表示距离与物理参考（RMSD、二面角、手性签名、能量差）的秩相关性；流形一致性则评估表示空间是否形成连贯的流形结构，包括局部等距性、对映体分离度和能量跳跃敏感性。

与现有基准（如MoleculeNet、QM9）的三个核心槽位变化如下：

- **评估范式**：从静态分子间任务（性质预测、跨分子分类）转变为动态分子内构象敏感性评估。现有方法将分子视为固定实体，而3DCS要求表示在同一分子的不同构象间保留几何变异、捕获手性并反映能量景观。
- **数据集规模与多样性**：从较小或单一类型的数据集（如MD17、QM9）扩展到包含超过100万个分子和1100万个构象的三个大规模数据集：松弛扫描数据集（~150万分子，~1000万构象，覆盖几何灵活性）、手性药物候选物数据集（~4000手性分子，~5.2万构象，聚焦立体化学）、AIMD轨迹数据集（10个分子，每个10万构象，用于能量景观）。
- **评估指标**：从单一的预测精度（MAE、ROC-AUC）扩展到多层诊断指标。参考对齐层使用Spearman秩相关、Kendall秩相关、CKA、等渗回归R²；流形一致性层使用局部等距误差（LIE）、扭转相关性、手性分离AUC、能量跳跃敏感性（EJS）、阈值平滑度（TS）等。

核心洞察在于，现代数据驱动的3D分子表示在几何敏感性上表现良好（几乎所有学习表示都优于手工描述符E3FP，MolSpectra在几何基准上取得最高Spearman相关系数0.682），但在手性区分上表现不一致（MolAE在手性基准上取得最高ES-AUC 0.782，但SE(3)-等变模型如UniMol仅0.622），且与能量景观的对齐普遍较差（最佳模型MACE的Spearman相关系数仅0.236）。值得注意的是，经过能量/力监督训练的模型（GemNet、MACE）在能量对齐上显著优于其他方法，而牺牲旋转不变性以保留手性敏感性的基于场的模型FMG在手性分离上表现突出。图2的雷达图以E3FP为基线展示了各模型在GCE维度上的相对改进，直观揭示了不同架构的能力边界。

## 整体框架

3DCS基准的核心贡献在于将分子表示评估从传统的跨分子性质预测转向**分子内构象敏感性**分析。其整体pipeline由三个串联模块构成：**数据集构建 → 表示提取 → GCE评估**，形成一个闭合的评估循环。

**数据集构建**模块生成了三个针对性的大规模数据集，分别对应构象敏感性的三个维度：几何灵活性、手性区分和能量景观。几何数据集（松弛扫描）包含约150万个分子和约1000万个构象，使用半经验方法GFN2-xTB（xTB软件）进行几何优化和能量计算，通过DBSCAN聚类去除冗余构象。手性数据集包含约4000个药物样分子和约52000个构象，使用Murcko骨架划分（8:1:1）避免子结构泄露，并对每个立体异构体施加小的扭转扰动，使不同对映体的构象在几何空间上重叠，防止模型仅通过粗糙的几何差异来区分对映体。能量数据集源自从头算分子动力学（AIMD）轨迹，包含10个小有机分子，每个分子约10万个构象，提供DFT级别的势能参考。三个数据集的规模（总计超过100万个分子和1100万个构象）显著超越了现有基准（如MD17、QM9）的规模。

**表示提取**模块在零样本设置下从两类表示中提取构象级别的特征向量：手工描述符（E3FP作为经典3D指纹基线）和学习模型（UniMol、MolAE、MolSpectra、GemNet、MACE、FMG）。这些模型覆盖了不同的架构范式：SE(3)-等变Transformer（UniMol、MolAE）、几何消息传递网络（GemNet）、E(3)-等变原子建模架构（MACE）、多模态模型（MolSpectra结合3D去噪与量子力学光谱信息），以及基于场的生成模型（FMG使用多通道3D体素网格，通过PCA对齐牺牲旋转不变性以保留手性敏感性）。表示距离的定义取决于表示类型：学习表示使用余弦距离，二进制指纹使用Tanimoto距离。

**GCE评估**模块是框架的核心创新，包含两层指标：**参考对齐**和**流形一致性**。参考对齐层检验表示距离是否与物理参考距离（几何RMSD、手性签名不匹配分数、能量绝对差值）对齐，使用Spearman秩相关、Kendall秩相关、中心核对齐（CKA）和等渗回归R²（isoR²）四个指标。流形一致性层评估表示是否形成连贯的流形，包括局部等距误差（LIE，衡量局部邻域保持）、扭转相关性（几何维度）、手性分离AUC（ES-AUC和NN1-acc，手性维度）、能量跳跃敏感性（EJS，衡量表示对能量突变的检测能力）和阈值平滑度（TS，衡量表示沿能量轨迹的平滑变化）。评估框架的输出是三个维度（几何、手性、能量）上的综合性能画像，如Figure 1（工作流概览图）和Figure 2（雷达图）所示。

整个pipeline的输入是分子构象（3D坐标），输出是模型在GCE三个维度上的敏感性指标。关键的设计选择包括：零样本评估（除手性微调实验外）、使用半经验方法（xTB）作为几何数据集的能量来源（而非DFT，这是明确承认的局限性之一）、以及对手性数据集施加扭转扰动以防止几何特征泄露。

## 核心模块与公式推导

3DCS基准的核心在于其**GCE评估框架**（Geometry-Chirality-Energy），该框架通过两层指标——**参考对齐（Reference Alignment）** 与**流形一致性（Manifold Consistency）**——来量化分子表示对构象变化的敏感性。评估的前提是明确定义三种物理参考距离与表示空间中的距离度量。

**物理参考距离定义**

对于任意两个构象 $c_i$ 和 $c_j$，三个维度的参考距离定义如下：

- **几何距离**：采用原子位置最优对齐后的均方根偏差（RMSD），单位为Å：
  
$$
D_{ij}^{(G)} = \mathrm{RMSD}(c_i, c_j)
$$

- **手性距离**：对于具有 $m$ 个立体中心的分子，首先定义每个构象 $c_i$ 的手性签名向量 $\chi(c_i) = (s_1, \ldots, s_m) \in \{\pm 1\}^m$，其中 $+1/-1$ 表示R/S或D/L构型。手性距离即为两个构象之间不匹配立体中心的分数：
  
$$
D_{ij}^{(C)} = \frac{1}{m} \sum_{t=1}^m \mathbf{1}[s_t(c_i) \neq s_t(c_j)]
$$

- **能量距离**：直接取两个构象之间势能的绝对差值：
  
$$
D_{ij}^{(E)} = |E(c_i) - E(c_j)|
$$

**表示空间距离度量**

表示空间中的距离 $\Delta_{ij}$ 根据表示类型选择不同度量：

$$
\Delta_{ij} = 
\begin{cases} 
1 - \frac{z_i^\top z_j}{\|z_i\|\|z_j\|}, & \text{余弦距离（学习表示）} \\
\|z_i - z_j\|_2, & \text{欧几里得距离} \\
1 - \frac{|F_i \cap F_j|}{|F_i \cup F_j|}, & \text{Tanimoto距离（二进制指纹）}
\end{cases}
$$

**参考对齐层指标**

该层检验表示距离是否与物理参考距离单调对齐，包含四个相关/相似性指标：

- **Spearman秩相关系数** $\rho_S(m) = \mathrm{Spearman}(\mathrm{vec}_\triangle(D), \mathrm{vec}_\triangle(\Delta))$：衡量距离矩阵上三角向量化后的秩相关性。
- **Kendall秩相关系数** $\tau(m) = \mathrm{Kendall}(\mathrm{vec}_\bigtriangleup(D), \mathrm{vec}_\bigtriangleup(\Delta))$：同样衡量秩相关性，对异常值更鲁棒。
- **中心核对齐（CKA）** $\mathrm{CKA} = \frac{\langle \tilde{K}^{(D)}, \tilde{K}^{(\Delta)} \rangle_F}{\|\tilde{K}^{(D)}\|_F \|\tilde{K}^{(\Delta)}\|_F}$：衡量参考距离核矩阵 $K^{(D)}$ 与表示距离核矩阵 $K^{(\Delta)}$ 之间的相似性，核函数采用RBF核，带宽通过中位数启发式确定。
- **等渗回归R²** $\mathrm{isoR}^2 = 1 - \frac{\sum_{i<j} (D_{ij} - \hat{D}_{ij})^2}{\sum_{i<j} (D_{ij} - \bar{D})^2}$：衡量单调变换 $\hat{D}$ 恢复原始参考尺度的程度。

**流形一致性层指标**

该层评估表示是否形成物理上有意义的流形结构，针对不同维度有专门指标：

- **局部等距误差（LIE）**：衡量表示空间是否保持参考距离下的局部邻域结构。
  
$$
\mathrm{LIE}_i = \sqrt{\frac{1}{k} \sum_{j \in \mathcal{N}_k^{(D)}(i)} \left( \frac{D_{ij}^{(G)}}{\bar{D}_i} - \frac{\Delta_{ij}}{\bar{\Delta}_i} \right)^2}
$$

  其中 $\mathcal{N}_k^{(D)}(i)$ 是构象 $i$ 在参考距离下的 $k$ 近邻，$\bar{D}_i$ 和 $\bar{\Delta}_i$ 是局部均值。LIE越低，表示局部等距保持越好。

- **能量跳跃敏感性（EJS）**：衡量表示距离对能量显著变化的检测能力。
  
$$
\mathrm{EJS}(\lambda) = \mathbb{E}[\mathbf{1}\{dZ_{ij} > \tau\} \mid (i,j) \in \mathcal{I}_\lambda]
$$

  其中 $\mathcal{I}_\lambda = \{(i,j) : D_{ij}^{(E)} > \lambda\}$ 是能量跳跃超过阈值 $\lambda$ 的构象对集合，$dZ_{ij}$ 是标准化后的表示距离，$\tau$ 是表示距离阈值。论文默认 $\lambda = 2.0$，并进一步计算EJS的ROC-AUC来评估二元分类性能。

- **阈值平滑度（TS）**：衡量在能量显著变化的轨迹段上，表示变化的平滑度。
  
$$
\mathrm{TS}_{T_E} = \frac{1}{|\mathcal{K}|} \sum_{k \in \mathcal{K}} \exp\left( -\frac{\Delta_{\pi_k, \pi_{k+1}} / Q_{0.9}^{(\Delta)}}{|E_{\pi_{k+1}} - E_{\pi_k}| / Q_{0.9}^{(E)} + \varepsilon} \right)
$$

  其中 $\mathcal{K}$ 是能量变化超过阈值 $T_E$ 的轨迹段索引集合，$\pi_k$ 是按能量排序的构象序列，$Q_{0.9}$ 是90%分位数用于鲁棒归一化。TS越高，表示在能量跳跃时变化越平滑且与能量变化成比例。

**关键因果机制**

GCE框架的设计揭示了分子表示评估中的核心瓶颈：参考对齐层检测表示是否编码了正确的物理信息（如几何变形、手性差异、能量顺序），而流形一致性层则检测表示空间的结构是否物理可信（如局部几何保持、对映体分离、能量跳变响应）。这两层指标共同构成了对表示质量的完整诊断，而不仅仅是下游任务性能的代理。例如，一个在性质预测上表现良好的模型，可能在能量对齐上完全失败（如MolAE在几何CKA上高达0.975，但在能量Spearman上仅0.051），这暴露了其表示缺乏物理能量信息的本质。

## 实验与分析

### 主结果：GCE三维基准

3DCS基准在几何、手性和能量三个维度上揭示了现有分子表示方法的系统性能力差异。表1至表3报告了所有方法在零样本设置下的完整结果，图2以雷达图形式汇总了相对E3FP基线的改进幅度。

![[assets/figures/papers/iclr26_0001_JAb0y8lkqL_3DCS_Datasets_and_Benchmark_for_Evaluating_Confo/figures/003_Table_1.jpg]]
*Table 1: Geometry benchmark metrics comparing learned representations and handcrafted fingerprints. The number of local neighborhoods for LIE@k is 3 by default*

![[assets/figures/papers/iclr26_0001_JAb0y8lkqL_3DCS_Datasets_and_Benchmark_for_Evaluating_Confo/figures/005_Table_3.jpg]]
*Table 3: Energy benchmark measuring correspondence between representation distances and energetic variation*

**几何基准（表1）**。在松弛扫描数据集上，所有学习到的表示在秩相关指标上均显著优于手工描述符E3FP（Spearman=0.155）。MolSpectra取得了最高的Spearman相关系数（0.682）和Kendall相关系数（0.483），表明其表示距离与RMSD物理参考的对齐最为准确。MolAE在CKA指标上达到0.975，接近完美对齐，但其Spearman（0.599）略低于MolSpectra，说明线性对齐能力强但单调排序精度稍逊。SE(3)-等变Transformer（UniMol、MolAE、MolSpectra）整体优于标准消息传递网络（GemNet），后者因强局部性偏差在几何变化捕捉上存在瓶颈。图5的小提琴图进一步验证了这些差异的统计显著性（Mann–Whitney U检验，p<0.001）。

**手性基准（表2）**。MolAE在手性分离AUC（ES-AUC）上达到最高值0.782，FMG在最近邻准确率（NN1-acc）上达到0.726。然而，所有方法在基于秩相关的指标上表现普遍较差，例如MolAE的Spearman仅为0.109，FMG的Spearman为0.034。这一矛盾表明：模型能够将同一分子的对映体聚为不同簇（高ES-AUC），但无法使表示距离与立体化学标签的差异程度单调对齐（低Spearman）。值得注意的是，E(3)-等变网络（GemNet、MACE）在手性基准上表现最差（ES-AUC分别为0.571和0.582），这与它们的旋转不变性设计一致——旋转不变性在几何任务中是优势，但在区分镜像结构时成为根本性限制。图6的小提琴图显示，FMG在NN1-acc上的分布方差较大，表明其对分子结构的依赖性较强。

![[assets/figures/papers/iclr26_0001_JAb0y8lkqL_3DCS_Datasets_and_Benchmark_for_Evaluating_Confo/figures/004_Table_2.jpg]]
*Table 2: Chirality benchmark. The listed metrics focus on the ability of models to distinguish between stereochemical configurations. Fine-tuned baselines results are reported in Appendix table 5*

**能量基准（表3）**。能量对齐是所有维度中最具挑战性的。MACE在Spearman（0.236）、Kendall（0.159）和能量跳跃敏感性EJS（0.578）上均取得最高值，FMG在阈值平滑度TS（0.582）上最优。经过能量/力监督训练的模型（GemNet、MACE）在能量相关指标上显著优于其他方法，表明显式的能量监督是提升能量对齐的关键瓶颈。相比之下，仅通过几何预训练的模型（如UniMol、MolAE）在能量指标上几乎与E3FP基线持平（Spearman分别为0.016和0.028），说明几何感知不等于能量感知。所有方法的Spearman绝对值均较低（最高0.236），反映出当前表示空间与势能面之间的鸿沟仍然是开放挑战。

### 消融与诊断分析

**监督微调的效果**。在手性数据集上使用监督对比学习微调后（表5），FMG的ES-AUC从0.758提升至接近完美（0.997），MolAE从0.782提升至0.997。这一结果验证了3DCS手性指标不仅具有诊断性，还能指导模型改进。同时，E(3)-等变网络（GemNet、MACE）即使在微调后也无法有效捕捉手性（ES-AUC分别为0.582和0.500），这确认了模型架构层面的根本性限制。

![[assets/figures/papers/iclr26_0001_JAb0y8lkqL_3DCS_Datasets_and_Benchmark_for_Evaluating_Confo/figures/030_Table_5.jpg]]
*Table 5: Fine-tuned model performance on chirality datasets. We use supervised contrastive learning to train the models. E3FP is not a trainable model. The result align well with our zero-shot experiment and agreement to model architecture, while E(3) network like GemNet and MACE cannot represent chirality well*

**能量指标的可预测性**。3DCS能量指标与下游DFT能量预测任务（表8、表9）存在一致的模式：在能量基准上表现较好的模型（如MACE、GemNet）在Revised MD17数据集上的能量预测MAE也较低。这表明3DCS的评估结果具有预测下游任务难度的能力，而非仅提供诊断性信息。

**势能面对齐的可视化**。图7展示了阿司匹林和对乙酰氨基酚的真实势能面与表示空间投影的对比。学习表示能够部分捕捉高能势垒区域（红色框标记），但整体上平滑了能量变化细节，尤其是在低能区域。这一可视化解释了为什么能量对齐的秩相关指标普遍偏低——表示空间倾向于保留拓扑结构而丢失精细的能量梯度信息。

### 失败模式与局限性

1. **手性感知不一致**：SE(3)-等变架构在手性任务上的系统性失败表明，旋转等变性与手性敏感性之间存在根本性权衡。FMG通过PCA对齐牺牲旋转不变性来保留手性信息，但代价是表示对旋转敏感。

2. **能量对齐瓶颈**：即使是最优的MACE，其Spearman也仅为0.236，远低于几何基准的性能。这表明当前表示学习方法缺乏显式的能量景观建模机制。几何数据集使用半经验xTB方法而非DFT计算能量，可能引入近似误差，但这一选择使大规模构象生成成为可能。

3. **数据集覆盖有限**：能量数据集仅包含10个小有机分子，手性数据集仅包含药物样分子，可能无法完全代表复杂分子体系的多样性。评估主要限于零样本设置，微调实验仅在手性维度上进行了探索。

4. **指标超参数敏感性**：LIE、EJS和TS等流形一致性指标依赖于超参数选择（如k近邻数、能量跳跃阈值λ），可能影响跨方法比较的公平性。

### 补充图表

![[assets/figures/papers/iclr26_0001_JAb0y8lkqL_3DCS_Datasets_and_Benchmark_for_Evaluating_Confo/figures/029_Table_4.jpg]]
*Table 4: Chirality metrics of correlation between representation distance and chirality reference, including stereochemical labels and OPD index*

![[assets/figures/papers/iclr26_0001_JAb0y8lkqL_3DCS_Datasets_and_Benchmark_for_Evaluating_Confo/figures/031_Table_6.jpg]]
*Table 6: Summary of representations’ performance on the energy dataset. Values are reported as mean ± 95% CI*

## 方法谱系与知识库定位

3DCS基准的提出，直接回应了现有分子表示评估范式的根本性空白：传统基准（如MoleculeNet、Molecule3D、MARCEL）均聚焦于**分子间**任务——性质预测或跨分子分类——将每个分子视为一个静态、无构象变化的实体。3DCS首次将评估焦点转向**分子内**的构象敏感性，系统考察同一分子不同构象在几何变形、手性差异和能量景观三个维度上的表示质量。这一转变的因果核心在于其提出的GCE（几何-手性-能量）评估框架，该框架通过两层指标——参考对齐（reference alignment）和流形一致性（manifold consistency）——将表示距离与物理参考（RMSD、二面角、手性签名、能量差）进行定量关联。

**与基线方法的关系**：3DCS覆盖了从经典手工描述符到前沿学习模型的广泛谱系。在几何维度，所有学习表示均显著优于手工基线E3FP（Spearman相关系数从0.155提升至MolSpectra的0.682），表明数据驱动的3D表示已能有效捕捉构象几何变化。MolSpectra作为结合3D去噪与量子力学光谱信息的多模态模型，在几何基准上取得最优表现，暗示光谱信息为几何敏感性提供了额外的监督信号。在手性维度，情况更为复杂：MolAE（编码器-解码器架构，使用3D Cloze Test目标）在ES-AUC上达到0.782，而SE(3)-等变模型（如UniMol、GemNet）在手性分离上表现不佳。这一差异揭示了关键瓶颈：严格的SE(3)-等变性虽有利于几何推理，却天然地模糊了手性信息（对映体通过镜像对称关联）。FMG通过PCA对齐牺牲旋转不变性来保留手性敏感性，在手性分离上取得突破，但其代价是失去了对旋转的鲁棒性。在能量维度，几乎所有模型的表现都远低于几何维度——MACE的最高Spearman相关系数仅为0.236，表明能量景观对齐是当前表示学习的**主要开放挑战**。值得注意的是，经能量/力监督训练的模型（GemNet、MACE）在能量对齐上显著优于纯无监督方法，说明显式的物理监督是弥合这一差距的必要条件。

**适用边界与局限**：3DCS的评估框架存在若干明确边界。首先，几何数据集使用半经验xTB方法而非DFT计算能量，可能引入系统近似误差，影响能量相关指标的绝对可靠性。其次，能量数据集仅包含10个小有机分子（来自Revised MD17），规模有限，可能无法代表复杂分子体系（如蛋白质-配体复合物）的能量景观多样性。第三，手性数据集局限于药物样分子，未涵盖无机配合物或大环分子的手性特征。第四，评估主要采用零样本设置（除少量微调实验外），未系统探索模型在特定任务上微调后的表现变化。此外，GCE框架中的某些指标（如LIE的k近邻数、EJS的能量跳跃阈值λ、TS的平滑度参数）依赖于超参数选择，可能影响跨模型比较的公平性。

**开放问题**：3DCS揭示的核心矛盾——学习表示在几何上表现良好，在手性上不一致，在能量上普遍薄弱——指向三个关键研究方向：(1) 如何设计既能保持SE(3)-等变性又能区分手性的表示架构？FMG的成功表明，有选择地打破对称性可能是可行路径，但其泛化性和理论保证仍需验证。(2) 如何使学习表示更好地与能量景观对齐？当前所有模型在能量基准上的表现均远低于几何维度，说明仅靠构象级监督（如去噪、重构）不足以捕捉势能面的精细结构。GemNet和MACE的对比表明，显式的能量/力监督是必要但非充分条件。(3) 3DCS能否扩展到条件设置（如蛋白质-配体对接、姿态预测）和更大分子体系？当前数据集的小分子限制可能掩盖了表示方法在处理柔性大分子时的潜在失败模式。最后，3DCS指标本身能否用作**设计指导**——即利用能量跳跃敏感性（EJS）或阈值平滑度（TS）作为训练目标来直接优化表示的物理可信度——是一个值得探索的方向。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/3DCS_Datasets_and_Benchmark_for_Evaluating_Conformational_Sensitivity_in_Molecular_Representations.pdf

![[paperPDFs/ICLR_2026/3DCS_Datasets_and_Benchmark_for_Evaluating_Conformational_Sensitivity_in_Molecular_Representations.pdf]]
