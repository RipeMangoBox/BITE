---
title: "An Efficient SE(p)-Invariant Transport Metric Driven by Polar Transport Discrepancy-based Representation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/An_Efficient_SEp_Invariant_Transport_Metric_Driven_by_Polar_Transport_Discrepancy_based_Representation.pdf
project_link: null
code_link: null
aliases:
- SSPIT
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "SEINT builds an SE(p)-invariant transport metric from polar transport discrepancy and distance-convoluted scalar representations."
primary_logic: "It maps distributions from possibly different spaces into isometry-invariant one-dimensional DcPTD representations and compares them with Wasserstein distance."
claims:
- "PTD and DcPTD combine norm information, optimal couplings, and intrinsic distances into dimension-independent scalar features."
- "The resulting SEINT distance is described as a true metric on isometry classes."
- "Experiments show strong invariance performance and useful regularization for molecular generation."
---

# An Efficient SE(p)-Invariant Transport Metric Driven by Polar Transport Discrepancy-based Representation

> [!tip] 核心洞察
> 通过将极地长度信息与最优传输耦合结合，再与内在距离进行卷积，得到等距不变且维度无关的标量表示，从而将跨空间分布比较转化为同一空间上的可解最优传输问题。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于极地传输差异表示的高效SE(p)不变传输度量 |
| 英文题名 | An Efficient SE(p)-Invariant Transport Metric Driven by Polar Transport Discrepancy-based Representation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=oyxExc7TEl) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | SEINT (SE(p)-Invariant Transport) |
| Dataset | ModelNet40-SE(3), QM9 (预训练, EDM) |

> [!tip] 效果简介
> - ModelNet40-SE(3) 上，Accuracy (k=1) 为 100.0 ± 0.0，对比 GW: 100.0 ± 0.0, EGW: 100.0 ± 0.0, RISGW: 100.0 ± 0.0, SGW: 100.0 ± 0.0, SW: 100.0 ± 0.0, W2: 100.0 ± 0.0，变化 0.0。
> - ModelNet40-SE(3) 上，Time (h) 为 9.01，对比 GW: >72, EGW: >72, RISGW: 0.18, SGW: 0.18, SW: 0.18, W2: 0.18，变化 远快于GW/EGW。
> - QM9 (预训练, EDM) 上，Atom. (%) 为 99.1，对比 EDM: 98.7，变化 +0.4。

## 概要

本文提出了一种名为SEINT（SE(p)-Invariant Transport）的新型特殊欧几里得群不变度量，用于比较p维赋范Banach空间上的概率分布。SEINT通过极地传输差异（Polar Transport Discrepancy, PTD）与距离卷积（Distance-convoluted PTD, DcPTD）提取SE(p)不变表示，将高维分布映射为1维标量表示，再通过最优传输计算距离。该方法在保持严格度量性质的同时，实现了O(n log n)至O(n²)的计算复杂度，显著优于现有方法。实验表明，SEINT在ModelNet40-SE(3)上达到100%分类准确率，运行时间（9.01小时）远低于GW（>72小时）和EGW（>72小时）；在分子生成预训练中，以0.3权重集成到UniGEM后，原子稳定性达99.3%，分子稳定性达93.5%，均达到SOTA。

现有基于最优传输的SE(p)不变方法可分为三类策略（Figure 1）：

- **外在策略**：联合优化正交变换与最优传输问题，如EMD under Transformation Sets（EMD^G）、Softassign Procrustes Matching（SPM）、Rotation-Invariant Sliced Gromov-Wasserstein（RISGW）。这些方法计算开销大，且部分不满足度量性质。
- **内在策略**：利用数据的几何结构，如Gromov–Hausdorff（GH）距离和Gromov–Wasserstein（GW）距离。复杂度高达O(n³)-O(n⁴)，难以扩展到大规模数据。
- **表示策略**：直接提取SE(p)不变特征，如Spherical Harmonic Representations（SHR）、Rotation-Invariant Transformers（RIT）。这些方法可能仅产生伪度量而非真度量。

**核心瓶颈**：现有方法无法同时满足计算效率、严格的度量性质以及跨等距类通用性。Table 1总结了各类方法的性质对比。

## 核心方法与创新机理

本文的核心创新在于提出无监督的极地传输差异（PTD）及其距离卷积变体（DcPTD），通过将极地长度信息与最优传输耦合结合，再与内在距离进行卷积，得到等距不变且维度无关的标量表示，从而将跨空间分布比较转化为同一空间上的可解最优传输问题。

**关键改进点**：

| 改进维度 | 基线方法 | 本文方法 | 证据 |
|---------|---------|---------|------|
| 特征提取方式 | 外在：联合优化正交矩阵；内在：比较度量空间内蕴结构；表示：手工或学习特征 | 无监督PTD/DcPTD：通过极地长度与参考分布的最优传输耦合，再与距离矩阵卷积，得到1维等距不变表示 | Definition 1, Definition 2 |
| 距离计算方式 | 外在：迭代优化OT+正交矩阵；内在：双层OT（GW）；表示：在特征空间计算距离 | 在DcPTD表示空间上计算1维Wasserstein距离，通过inf sup优化选择最不利参考分布 | Definition 3, equation (7) |
| 计算复杂度 | 外在：O(n³)-O(n³ log n)；内在：O(n³)-O(n⁴)；表示：O(n² log n)（如SFGW） | O(n log n)至O(n²)，当距离矩阵可分解时可达O(n log n) | 复杂度分析 |
| 度量性质 | 外在：EMD^G是度量，SPM/RISGW不是；内在：GH/GW是度量；表示：SHR/RIT不是度量 | SEINT是等距类空间上的真度量（满足同一性、对称性、三角不等式） | Theorem 1 |
| 跨空间比较能力 | 外在：不支持；内在：支持；表示：部分支持 | 支持，通过DcPTD的等距不变性和维度无关性将不同空间映射到公共表示域 | Remark 1 |

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_oyxExc7TEl_An_Effi/figures/001_Figure_1.jpg]]
*Figure 1: (a) Extrinsic strategy*

SEINT的数值实现流程如Figure 2所示，包含四个核心步骤：

1. **计算范数**：对输入数据X和Y，分别计算其范数（或到基点的距离）。
2. **PTD计算**：对每个范数，通过随机生成的参考分布计算最优传输，得到极地传输差异。
3. **DcPTD计算**：将PTD与距离矩阵卷积，得到距离卷积极地传输差异。
4. **1维Wasserstein距离**：计算两个DcPTD表示之间的1维Wasserstein距离作为最终SEINT距离。

### 5.1 极地传输差异（PTD）

首先定义范数分布与参考分布之间的最优耦合集合：

$$\Pi_{X,Z}^* := \{ \pi \in \Pi(\mu_X, \mu_Z) : \mathbb{E}_\pi |\|x\|_X - z| = \inf_{\pi' \in \Pi(\mu_X, \mu_Z)} \mathbb{E}_{\pi'} |\|x\|_X - z| \}$$

在此基础上，PTD定义为在最优耦合下，x的范数与参考变量z的条件期望绝对偏差：

$$\zeta_{\pi_{X,Z}^*}(x) := \int_{\mathbb{R}} |\|x\|_X - z| d\pi_{Z|X=x}^*(z)$$

### 5.2 距离卷积极地传输差异（DcPTD）

DcPTD将PTD与内在距离函数进行卷积，产生等距不变的标量表示：

$$\phi_{\pi_{X,Z}^*}(x) := \int_X d_X(x, x') \zeta_{\pi_{X,Z}^*}(x') d\mu_X(x')$$

**Remark 1**：DcPTD具有等距不变性——对于任意等距映射f: X → Y，有φ_{π_{X,Z}^*}(x) = φ_{π_{Y,Z}^*}(f(x))。同时，DcPTD产生维度无关的表示，输出始终为非负标量值。

### 5.3 SEINT距离

SEINT距离定义为在耦合和参考分布上的inf-sup优化：

$$\mathcal{L}_{\mathrm{SEINT}}(X,Y,\mu_X,\mu_Y) := \inf_{\pi \in \Pi(\mu_X,\mu_Y)} \sup_{\mu_Z \in \mathcal{P}_{X,Y}(\mathbb{R})} \left( \mathbb{E}_\pi \left[ |\phi_{\pi_{X,Z}^*}(x) - \phi_{\pi_{Y,Z}^*}(y)|^p \right] \right)^{1/p}$$

其中参考测度μ_Z限制在P_{X,Y}(ℝ) = P_X(ℝ) ∪ P_Y(ℝ)中，以简化耦合选择。

**Theorem 1 (等距类上的度量性质)**：L_SEINT在度量测度空间的等距类空间上定义了一个度量，满足同一性、对称性和三角不等式。

**Corollary 1 (SE(p)不变性)**：SEINT距离在SE(p)变换下保持不变：

$$\mathcal{L}_{\mathrm{SEINT}}(X,Y,\mu_X,\mu_Y) = \mathcal{L}_{\mathrm{SEINT}}(g(X),Y,g_\#\mu_X,\mu_Y)$$

### 5.4 积分变体ISEINT

为降低计算复杂度，提出积分SEINT距离（ISEINT），对参考分布取平均而非最大值：

$$\mathcal{L}_{\mathrm{ISEINT}}(X,Y,\mu_X,\mu_Y) := \inf_{\pi \in \Pi(\mu_X,\mu_Y)} \left( \mathbb{E}_{\pi \times \mathcal{D}(\mathcal{P}_{X,Y}(\mathbb{R}))} \left[ |\phi_{\pi_{X,Z}^*}(x) - \phi_{\pi_{Y,Z}^*}(y)|^p \right] \right)^{\frac{1}{p}}$$

## 实验与关键发现

### 6.1 SE(p)不变性验证

在ModelNet40-SE(3)数据集上，SEINT在k=1,5,10时均达到100%分类准确率，运行时间仅4.46ms，远快于SFGW（485.19ms）（Table 7）。在ModelNet40-SE(3)完整实验中，SEINT以9.01小时完成，远低于GW和EGW的>72小时（Table 2）。

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_oyxExc7TEl_An_Effi/figures/006_Table_2.jpg]]
*Table 2: Comparisons of classification accuracy (%) across different numbers of neighbors (k)*

### 6.2 分子生成

**预训练结果**（Table 3）：SEINT以0.3权重集成到UniGEM后，原子稳定性达99.3%，分子稳定性达93.5%，均达到SOTA。集成到EDM后，原子稳定性从98.7%提升至99.1%，分子稳定性从87.2%提升至91.5%。

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_oyxExc7TEl_An_Effi/figures/010_Table_3.jpg]]
*Table 3: Pre-training results: Comparison of methods on atom stability (Atom.), molecular stability (Mol.), validity (Val.), and validity×uniqueness (V*U.), each drawing 10000 samples from the model.*

**微调结果**（Table 4）：在QM9上，SEINT_0.3达到原子稳定性99.4%、分子稳定性94.9%、有效性97.8%。在GEOM-Drugs上，原子稳定性达90.7%，分子稳定性达13.0%。

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_oyxExc7TEl_An_Effi/figures/011_Table_4.jpg]]
*Table 4: Fine-tuning results on QM9 and GEOM-Drugs.*

### 6.3 跨空间动态序列分析

在动态马序列实验中（Figure 3），SEINT距离展现出三个清晰连续的峰值，与马步态阶段对齐，而EGW响应幅度更弱，GW和RISGW无法保持一致的距离关系。

### 6.4 消融与鲁棒性分析

- **参考分布数量**（Figure 5）：SEINT损失随参考分布数量增加而稳定，表明有限参考足以捕捉最大区分度。
- **参考点数量**（Figure 8）：仅需相对较少的参考点即可达到稳定性能。
- **噪声鲁棒性**（Figure 6）：SEINT损失随噪声水平增加而平滑上升，初步证明其对分布变化的连续性。
- **高维行为**（Figure 7）：在n=200,p=50和n=50,p=200的高维设置下均表现出平滑一致的趋势。
- **旋转不变性**（Figure 9）：MDS可视化显示，SEINT在随机旋转后仍保持马奔跑数据的闭环模式，而SW和SGW无法保持。

### 6.5 点云分类正则化

SEINT和ISEINT正则化持续提升Point-MAE在点云分类任务上的准确率（Table 6）。例如，ISEINT_0.1在PB-T50-RS上达到85.39%，优于Point-MAE的84.67%。

### 6.6 公平性说明

所有实验均使用公开数据集（ModelNet40, QM9, GEOM-Drugs, ShapeNet, ScanObjectNN）。分子生成实验遵循EDM和UniGEM的标准数据划分（100K训练/18K验证/13K测试）。点云实验使用Point-MAE的默认超参数，仅替换正则化项。SE(p)-不变性实验中，所有方法使用相同的随机旋转和采样配置。代码已开源（https://github.com/junyilin559/SEINT），确保可复现性。

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_oyxExc7TEl_An_Effi/figures/004_Table_1.jpg]]

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_oyxExc7TEl_An_Effi/figures/013_Table_5.jpg]]
*Table 5: Comparison of three regularization terms on validity, atom stability, molecular stability, and uniqueness, each drawing 10000 samples from the model.*

## 定位与知识库关联

SEINT属于表示策略的SE(p)不变最优传输方法，其核心创新在于将极地长度信息与最优传输耦合结合，再与内在距离进行卷积，从而克服了现有方法的三大局限：

1. **计算效率**：相比外在策略（EMD^G, SPM）和内在策略（GW, EGW）的高复杂度，SEINT实现了O(n log n)至O(n²)的复杂度，在保持度量性质的同时大幅提升效率。
2. **度量性质**：相比表示策略（SHR, RIT）可能仅产生伪度量，SEINT被严格证明是等距类空间上的真度量。
3. **跨空间通用性**：通过DcPTD的等距不变性和维度无关性，SEINT支持不同空间之间的分布比较，这是外在策略所不具备的能力。

**局限性**：
- SEINT的连续性尚未给出正式证明，仅提供了经验证据。
- 连续版本的SEINT需要进一步的理论研究。
- 在分子生成中，SEINT在提升有效性的同时导致唯一性下降，存在有效性-唯一性权衡。
- 当样本量n较小时，SEINT的计算开销相对于某些方法（如SW）略高。
- 参考分布的选择（如支撑集范围M）需要根据数据统计量手动设定。

**开放问题**：
- SEINT的连续性是否能在理论上得到严格证明？
- SEINT在更高维数据（如p>1000）上的表现如何？
- 有效性-唯一性权衡在分子生成中是否有更优的平衡策略？
- SEINT能否扩展到非欧几里得域（如流形或图结构）？
- 参考分布的数量和支撑集大小对SEINT性能的理论影响是什么？
- SEINT是否可以作为其他生成模型（如GAN、VAE）的正则化项？

## 原文 PDF

![[paperPDFs/ICLR_2026/An_Efficient_SEp_Invariant_Transport_Metric_Driven_by_Polar_Transport_Discrepancy_based_Representation.pdf]]
