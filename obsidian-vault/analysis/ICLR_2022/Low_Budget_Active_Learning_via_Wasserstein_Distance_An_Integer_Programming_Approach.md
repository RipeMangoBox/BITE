---
title: "Low-Budget Active Learning via Wasserstein Distance: An Integer Programming Approach"
type: paper
paper_level: A
venue: ICLR
year: 2022
pdf_ref: paperPDFs/ICLR_2022/Low_Budget_Active_Learning_via_Wasserstein_Distance_An_Integer_Programming_Approach.pdf
project_link: null
code_link: null
aliases:
- WCSSGBDWEP
- LBALWDIPA
tags:
- ICLR_2022
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "将核心集选择转化为最小化离散Wasserstein距离的MILP，并采用广义Benders分解（GBD）算法进行全局优化。"
primary_logic: "通过GBD将原大规模MILP分解为反复求解小规模Wasserstein距离子问题与松弛主问题，配合增强最优性割（EOC）和剪枝约束（P）加速收敛，可以在合理时间内获得高质量或全局最优解，尤其适合低预算场景。"
claims:
- "定理1证明Wasserstein距离上界核心集损失，为优化目标提供理论依据。"
- "在STL-10、CIFAR-10、SVHN上，低预算（B ≤ 40）下所提方法准确率显著超过最佳基线，例如在STL-10 B=40时提升超过4.9%，在CIFAR-10 B=20时提升超过9.1%。"
- "与k-medoids启发式相比，GBD求解器（Wass.+EOC）获得更低的目标函数值（Wasserstein距离），在SVHN上平均降低约一半。"
- "SVHN 上 Wasserstein distance (目标函数值, B=140) = 0.080 (Wass.+EOC)"
---

# Low-Budget Active Learning via Wasserstein Distance: An Integer Programming Approach

> [!tip] 核心洞察
> 通过GBD将原大规模MILP分解为反复求解小规模Wasserstein距离子问题与松弛主问题，配合增强最优性割（EOC）和剪枝约束（P）加速收敛，可以在合理时间内获得高质量或全局最优解，尤其适合低预算场景。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于Wasserstein距离的低预算主动学习：一种整数规划方法 |
| 英文题名 | Low-Budget Active Learning via Wasserstein Distance: An Integer Programming Approach |
| 会议/期刊 | ICLR 2022 |
| Links | [paper](https://arxiv.org/abs/2106.02968) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | Wasserstein Core-set Selection via Generalized Benders Decomposition (Wass. + EOC + P) |
| Dataset | SVHN, CIFAR-10, Office-31 (Web → Amazon) |

> [!tip] 效果简介
> - SVHN 上，Wasserstein distance (目标函数值, B=140) 为 0.080 (Wass.+EOC)，对比 0.173 (k-medoids)，变化 -0.093 (约2×改善)。
> - CIFAR-10 上，classification accuracy (%) at B=20 为 Wass.+EOC+P 显著优于最佳基线，对比 最佳基线（WAAL/k-centers），变化 +9.1%。
> - Office-31 (Web → Amazon) 上，域适应准确率 (%) at B=50 为 65.9 ± 2.3 (Wass.+EOC+P)，对比 61.9 ± 2.1 (k-centers)，变化 +4.0。

## 概要

**核心问题**：在极低标注预算（例如仅标注不到1%的样本）下，现有主动学习启发式策略（如基于不确定性的采样、k-Center贪心核心集）无法保证选出全局最具代表性的样本，导致下游分类性能显著下降；而直接求解核心集选择的混合整数规划（MILP）又因计算不可行而难以应用。

**核心方法**：本文提出**基于Wasserstein距离的整数规划核心集选择框架**，将主动学习样本选择建模为最小化离散Wasserstein距离的MILP，并采用**广义Benders分解（GBD）** 算法进行全局优化。通过将原大规模MILP分解为反复求解小规模Wasserstein距离子问题与松弛主问题，配合**增强最优性割（EOC）** 和**剪枝约束（P）** 加速收敛，在合理时间内获得高质量或全局最优解。

**理论支撑**：定理1证明，在损失函数Lipschitz连续的条件下，Wasserstein距离构成核心集损失的上界，为以Wasserstein距离为优化目标提供了理论依据。

**核心发现**：
- 在STL-10、CIFAR-10、SVHN等图像分类任务上，低预算（B ≤ 40）下所提方法准确率显著超越所有基线，例如在STL-10 B=40时提升超过4.9%，在CIFAR-10 B=20时提升超过9.1%（Table 3）。
- 与k-medoids启发式相比，GBD求解器（Wass.+EOC）获得显著更低的目标函数值（Wasserstein距离），在SVHN上平均降低约一半（Table 1）。
- 即使将GBD运行时间限制在3分钟，其求解质量仍优于k-medoids启发式（Table 2）。
- 该方法可扩展至域适应主动学习，在Office-31的Web→Amazon任务上B=50时准确率提升4.0个百分点（Table 11）。

**方法定位**：该方法属于基于代表性的核心集选择路线，但区别于贪心或启发式近似，它通过整数规划全局优化Wasserstein距离，特别适合**低预算、高质量覆盖**的主动学习场景。其代价是运行时间显著长于启发式基线（数小时 vs 数秒），但在需要精准选择的低预算场景下可接受。



主动学习旨在通过选择最具信息量的样本进行标注，以最小的标注成本训练高性能模型。在标注预算极度有限（例如不到数据集1%）的场景下，这一问题的挑战尤为突出。现有主动学习方法主要分为两类：基于不确定性的策略（如Least Confidence、Maximum Entropy）和基于代表性的策略（如k-Center贪心、k-Medoids聚类中心）。然而，这些方法存在一个共同的瓶颈：它们依赖启发式或贪心准则进行样本选择，无法保证所选核心集在全局意义上对未标注池的代表性，导致在极低预算下分类性能显著下降。

核心集选择为这一瓶颈提供了理论框架——通过选取一个子集，使得在该子集上训练的模型损失能够上界整个数据集的损失。本文的理论分析（Theorem 1）表明，在损失函数Lipschitz连续的条件下，核心集损失的上界由核心集与完整数据集之间的Wasserstein距离决定。这为将主动学习转化为最小化Wasserstein距离的优化问题提供了理论依据。

然而，直接求解该核心集选择问题面临计算上的挑战：该问题本质上是一个大规模混合整数线性规划（MILP），在数据集较大时，现有商业或开源求解器无法在合理时间内获得满意解。因此，现有方法不得不退而求其次，采用贪心近似（如WAAL的贪心估计）或聚类启发式（如k-Medoids），牺牲了全局最优性。

本文的核心动机正是弥合这一理论与实践的鸿沟：能否设计一种算法，在可接受的计算时间内直接求解该MILP，从而在极低预算场景下获得显著优于启发式方法的核心集选择？为此，本文提出采用广义Benders分解（GBD）将原大规模MILP分解为反复求解小规模Wasserstein距离子问题与松弛主问题，并引入增强最优性割（EOC）与剪枝约束（P）加速收敛，使得在合理时间内获得高质量甚至全局最优解成为可能。



## 核心方法与创新机理

本文的核心创新在于将主动学习中的核心集选择问题**首次形式化为一个最小化离散Wasserstein距离的混合整数线性规划（MILP）**，并设计了一套可扩展的**广义Benders分解（GBD）算法**来对其进行全局优化。这一方案直接改变了“核心集选择策略”这一关键模块：基线方法普遍采用启发式或贪心策略（如k-centers贪心、WAAL贪心估计），而本文方法通过求解精确的MILP来最小化Wasserstein距离，从而在理论上保证了所选核心集对未标注池的代表性。

### 从代表性上界到可求解的优化问题

创新链条的起点是一个理论保证：**定理1**证明了在损失函数Lipschitz连续的条件下，核心集损失（即全量数据的经验风险与核心集经验风险之差）被离散Wasserstein距离上界所控制（见公式 `Theorem 1`）。这一结论将“最小化核心集损失”这一主动学习目标，等价地转化为“最小化核心集与未标注池之间的离散Wasserstein距离”。然而，直接求解由此产生的MILP（公式 `Equation (4)`）在大规模数据集上计算不可行——这正是本文要突破的瓶颈。

### GBD分解：将大规模MILP变为可迭代求解

本文的方法论创新在于将上述MILP重构为一个等价的**Wasserstein主问题（W-MP）**（公式 `Equation (5)`），该问题包含无穷多个约束，但每个约束对应一个对偶变量 $\lambda$ 下的Lagrangian松弛。GBD算法的核心思想是：**迭代地在松弛主问题（W-RMP）中求解候选核心集 $\hat{\pi}$，再通过求解小规模Wasserstein距离子问题来生成新的最优性割，逐步收紧下界**。这一分解策略将原问题中同时涉及离散变量 $\pi$ 和连续传输计划 $\Gamma$ 的联合优化，解耦为反复求解一个小规模整数规划主问题和一个纯线性Wasserstein子问题，使得在包含数万样本的数据集上获得高质量解成为可能。

### 增强最优性割与剪枝约束：加速收敛的机制设计

仅靠标准的GBD迭代收敛速度仍然不足。本文进一步引入了两类“changed slots”层面上的增强机制：

- **增强最优性割（EOC）**：在每次迭代中，除了由Wasserstein子问题对偶解生成的Lagrangian割之外，还额外添加两类利用Wasserstein距离性质构造的最优性割——基于最小正距离的下界割（公式 `Equation (6)`）和基于三角不等式的割。这些增强割为松弛主问题提供了更紧的全局下界，显著减少了所需迭代次数。
- **剪枝约束（P）**：通过移除高Wasserstein距离核心集附近的搜索邻域，并引导搜索向低距离邻域集中，进一步压缩可行域。

消融实验证实，EOC和P的引入能加速GBD收敛，并使Wass.+EOC+P在早期迭代中即获得更优的上界（见 **Figure 4 (left)** 和 Section 5.3）。

### 创新效果：低预算场景下的显著增益

这一方法论创新在极低标注预算场景下产生了决定性的性能提升。在STL-10上预算B=40时，所提方法准确率超过最佳基线4.9%以上；在CIFAR-10上B=20时，提升幅度超过9.1%（见 **Table 3** 和 Section 5.2）。这些增益源于GBD求解器能够找到全局代表性更强的核心集——在SVHN上，Wass.+EOC获得的Wasserstein距离目标函数值约为k-medoids的一半（见 **Table 1**），直接体现了优化质量的根本性提升。即使在运行时间被限制为3分钟的情况下，GBD求解器的解质量仍优于k-medoids启发式（见 **Table 2**），表明该方法在效率与精度的权衡上具有实际可行性。



本文提出的主动学习框架将核心集选择建模为一个全局优化问题，其整体流程由三个顺序模块构成：

1. **自监督特征预训练**：首先利用所有无标签数据，通过 SimCLR 等自监督学习方法预训练一个特征编码器，将原始图像映射到具有语义结构的潜在表示空间。该步骤不消耗任何标注预算。
2. **基于 Wasserstein 距离的核心集选择**：在预训练得到的特征空间中，求解一个最小化离散 Wasserstein 距离的混合整数线性规划（MILP），从无标签池中选取固定预算 $B$ 的样本进行标注。该 MILP 通过广义 Benders 分解（GBD）算法求解，并辅以增强最优性割（EOC）和剪枝约束（P）加速收敛。
3. **监督分类器训练**：冻结预训练的编码器权重，仅使用所选标注样本训练下游分类头，完成最终分类任务。

模块间的输入输出流如下：无标签数据集 $\mathcal{D}$ 首先进入 SimCLR 预训练模块，输出特征矩阵 $\mathbf{X}$ 和成对距离矩阵 $\mathbf{D}_{\mathbf{x}}$；距离矩阵作为 GBD 核心集选择模块的输入，输出一个二元选择向量 $\boldsymbol{\pi} \in \{0,1\}^N$（满足 $\boldsymbol{\pi}^{\top}\mathbf{1}=B$），指示被选中的样本；标注后的核心集 $\mathcal{C}(\boldsymbol{\pi})$ 最终送入分类器训练模块，得到下游模型。

图 1（左）直观展示了这一框架：预训练 → 最小化 Wasserstein 距离选取样本 → 训练分类器。图 1（右）的 t-SNE 可视化进一步定性地说明，基于优化的选择策略在特征空间中能更均匀地覆盖数据分布，避免启发式方法遗漏某些区域（例如 STL-10 的右上角区域被基线方法忽略）。

**关键设计动机**：在极低标注预算（$B \leq 40$，即不到数据集的 1%）下，贪心或启发式选择策略无法保证全局代表性。定理 1 为这一设计提供了理论支撑：当损失函数满足 Lipschitz 连续性时，核心集损失被 Wasserstein 距离上界所控制，因此最小化 Wasserstein 距离等价于最小化核心集损失的上界。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2106_02968/figures/001_Figure_1.jpg]]
*Figure 1: (Left) In our active learning framework, we first pre-train our features with self-supervised learning, select samples to label by minimizing the discrete Wasserstein distance, and then train our classifier. (Right) t-SNE plot of the feature space on the STL-10 data set with selected points highlighted. The baseline misses the top right region. See Appendix E.7 for full visual comparisons*



### 问题建模：核心集损失与Wasserstein距离

主动学习的核心目标是在给定标注预算 $B$ 下，从无标签池 $\mathcal{D} = \{\mathbf{x}_i\}_{i=1}^N$ 中选出一个核心集 $\mathcal{C}$，使得在该核心集上训练的分类器能逼近在全量数据上的性能。本文将该目标形式化为**最小化核心集损失（core-set loss）**：

$$\frac{1}{N} \sum_{i=1}^{N} \ell(\mathbf{x}_i, \Omega(\mathbf{x}_i); \mathbf{w}) - \frac{1}{B} \sum_{j=1}^{B} \ell(\mathbf{x}_j, \Omega(\mathbf{x}_j); \mathbf{w})$$

其中 $\ell$ 为损失函数，$\Omega(\mathbf{x})$ 为数据增强策略，$\mathbf{w}$ 为模型参数。

**定理1** 建立了Wasserstein距离与核心集损失之间的理论上界：当损失函数 $\ell$ 关于特征表示满足 $K$-Lipschitz连续性时，核心集损失被离散Wasserstein距离 $W(\mathcal{C}, \mathcal{D})$ 所上界控制（另含一个与数据增强相关的误差项 $\varepsilon K C$）。这为“最小化Wasserstein距离即最小化核心集损失”提供了理论依据（Theorem 1, Section 2.2）。

### 离散Wasserstein距离的LP形式

给定核心集 $\mathcal{C}(\boldsymbol{\pi})$（由二值选择向量 $\boldsymbol{\pi} \in \{0,1\}^N$ 指示）与全量数据集 $\mathcal{D}$，二者之间的离散Wasserstein距离定义为以下**原始线性规划（Primal LP）**：

$$W(\mathcal{C}(\boldsymbol{\pi}), \mathcal{D}) := \min_{\Gamma \geq 0} \left\{ \langle \mathbf{D}_{\mathbf{x}}, \boldsymbol{\Gamma} \rangle \mid \boldsymbol{\Gamma} \mathbf{1} = \frac{1}{N} \mathbf{1}, \ \boldsymbol{\Gamma}^{\top} \mathbf{1} = \frac{1}{B} \boldsymbol{\pi} \right\}$$

其中 $\mathbf{D}_{\mathbf{x}}$ 为成对距离矩阵，$\boldsymbol{\Gamma}$ 为传输计划矩阵。对应的**对偶线性规划（Dual LP）**为：

$$\max_{\lambda, \mu} \left\{ \frac{1}{N} \mu^{\mathsf{T}} \mathbf{1} - \frac{1}{B} \lambda^{\mathsf{T}} \boldsymbol{\pi} \mid \mu \otimes \mathbf{1}^{\mathsf{T}} - \lambda^{\mathsf{T}} \otimes \mathbf{1} \leq \mathbf{D}_{\mathbf{x}} \right\}$$

对偶变量 $\lambda$ 和 $\mu$ 在后续GBD分解中作为生成最优性割的关键量出现。

### 核心集选择的MILP模型

将选择变量 $\boldsymbol{\pi}$ 与传输计划 $\boldsymbol{\Gamma}$ 联合优化，得到**混合整数线性规划（MILP）**：

$$\min_{\pi \in \{0,1\}^N, \Gamma \geq 0} \langle \mathbf{D}_{\mathbf{x}}, \Gamma \rangle \quad \mathrm{s.t.} \quad \Gamma \mathbf{1} = \frac{1}{N} \mathbf{1}, \ \Gamma^{\top} \mathbf{1} = \frac{1}{B} \pi, \ \pi^{\top} \mathbf{1} = B$$

直接求解该MILP在大规模数据集上计算不可行。为此，本文采用**广义Benders分解（GBD）**将其分解为主-子问题迭代框架。

### GBD分解：主问题与子问题

GBD的核心思想是将原MILP等价转化为**Wasserstein主问题（W-MP）**：

$$\min_{\eta, \pi \in \mathcal{P}} \eta \quad \mathrm{s.t.} \quad \eta \geq \inf_{\Gamma \in \mathcal{G}} \left\{ \langle \mathbf{D}_{\mathbf{x}}, \Gamma \rangle + \lambda^{\intercal} \left( \frac{1}{B} \pi - \Gamma^{\intercal} \mathbf{1} \right) \right\}, \ \forall \lambda \in \mathbb{R}^N$$

该问题包含无穷多个约束（对应所有可能的对偶变量 $\lambda$）。GBD通过迭代求解以下两个子问题来逼近最优解：

1. **Wasserstein子问题**：给定当前核心集选择 $\hat{\boldsymbol{\pi}}$，求解离散Wasserstein距离的原始/对偶LP，获得目标值 $\eta^*$ 和对偶变量 $\lambda^*$。
2. **松弛主问题（W-RMP）**：将子问题生成的最优性割 $\eta \geq \frac{1}{B} (\lambda^*)^{\intercal} \boldsymbol{\pi}$ 加入主问题，求解更新后的MILP以获得新的 $\hat{\boldsymbol{\pi}}$。

GBD在有限次迭代内收敛到全局最优解。

### 增强最优性割（EOC）与剪枝约束（P）

为加速GBD收敛，本文引入两类额外约束：

**增强最优性割（Enhanced Optimality Cuts, EOC）** 利用Wasserstein距离的结构性质，在每次迭代中向W-RMP添加比标准Lagrangian割更紧的下界。关键割包括：

- **下界最优性割（Lower Bound Cut）**：基于每个样本到其最近邻的正距离，为 $\eta$ 提供与 $\boldsymbol{\pi}$ 线性相关的下界：

  $$\eta \geq \frac{1}{B} \sum_{i=1}^{N} \min_{i' \in \{1,\cdots,N\}} \left\{ D_{i,i'} \mid D_{i,i'} > 0 \right\} \pi_i$$

- **三角不等式割（Triangle Inequality Cut）**：利用度量空间的三角不等式，基于已知核心集 $\mathcal{C}(\hat{\pi})$ 的Wasserstein距离约束新候选解。

**剪枝约束（Pruning Constraints, P）** 则从搜索空间角度加速：移除目标函数值较高的核心集邻域，同时引导搜索向已知低Wasserstein距离的区域集中。该约束可能牺牲全局最优性，但在实践中显著提升了早期迭代的求解质量。

### 整体流程

完整的 **Wass. + EOC + P** 方法由三个模块串联：

1. **自监督特征预训练**（如SimCLR）：为无标签数据生成高质量潜在表示，作为Wasserstein距离计算的特征空间。
2. **GBD核心集选择**：在特征空间中迭代求解带EOC和P约束的MILP，输出最优标注样本子集。
3. **监督分类器训练**：冻结编码器权重，仅使用所选标注样本训练下游分类头。

GBD框架为低预算场景下的核心集选择提供了全局优化能力，而EOC和P的引入则使得该优化在合理时间内可解。



## 实验与关键发现

### 核心实验设置

实验遵循统一的主动学习流程：首先通过自监督预训练（SimCLR）为无标签数据生成特征表示；随后在特征空间中运行核心集选择算法；最后使用所选标注样本训练下游分类模型（冻结编码器权重），评估分类准确率。图像分类实验在STL-10、CIFAR-10和SVHN三个数据集上进行，域适应实验在Office-31数据集上进行（Table 5、Table 6）。

### 主实验结果

#### 目标函数值对比：Wasserstein距离最小化

论文首先直接比较了各方法在核心集选择问题（Equation 4）上的目标函数值——即离散Wasserstein距离。Table 1展示了GBD求解器（Wass.+EOC）与k-medoids启发式在SVHN、CIFAR-10和STL-10上的head-to-head对比。在所有预算水平下，Wass.+EOC均获得更低（更优）的Wasserstein距离。以SVHN在预算B=140时为例，Wass.+EOC的目标函数值为0.080，而k-medoids为0.173，改善幅度约2倍。这一优势在低预算和高预算场景下均保持一致，表明全局优化策略在最小化分布距离方面显著优于启发式近似。

Table 2进一步考察了有限运行时间下的求解质量。在CIFAR-10上，即使将GBD运行时间限制在3分钟，Wass.+EOC获得的目标函数值（B=120时为0.082）仍优于k-medoids（0.095），证明该方法在时间受限条件下依然保持竞争力。

#### 低预算主动学习准确率

Figure 2展示了三个图像分类数据集上各方法的准确率随标注预算变化的曲线。在极低预算区间（B ≤ 40），所提方法显著优于所有基线。Table 3提供了详细数值：

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2106_02968/figures/008_Figure.jpg]]

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2106_02968/figures/020_Figure.jpg]]

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2106_02968/figures/022_Figure.jpg]]

- **STL-10（B=40）**：Wass.+EOC+P准确率提升超过4.9个百分点（相对于最佳基线）。
- **CIFAR-10（B=20）**：准确率提升超过9.1个百分点。
- **SVHN（B=20）**：同样观察到显著优势，GBD方法在极低预算下展现出对特征空间全局结构的更好捕捉能力。

随着预算增加，各方法性能差距缩小，但Wass.+EOC+P在多数预算点仍保持领先。这一趋势验证了核心洞察：在标注样本极度稀缺时，启发式选择策略容易遗漏重要区域，而全局优化能确保所选子集在整个特征空间上的代表性。

#### 域适应主动学习

在Office-31域适应任务中（Figure 3，Table 11），Wass.+EOC+P在Web→Amazon任务上表现突出，B=50时准确率达到65.9±2.3%，显著优于k-centers的61.9±2.1%（提升4.0个百分点，经t检验验证）。然而，在Amazon→Web任务的中等预算场景下，k-centers表现优于所提方法，论文指出这可能是剪枝约束（P）限制了搜索空间，导致GBD陷入局部最优。这一发现揭示了剪枝策略的双刃剑效应：加速收敛的同时可能牺牲全局最优性。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2106_02968/figures/006_Figure_3.jpg]]
*Figure 3: Active learning with domain adaptation for D→A, W→A, and D→W on Office-31 using f -DAL pre-trained features. The solid line is our best model and the dashed lines are baselines. All plots show mean ± standard error over three runs. See Appendix E.4 for full results*

#### 经典主动学习设置

Table 4展示了在Shui et al.（2020）的经典主动学习设置下的对比结果。Wass.+EOC+P在SVHN和CIFAR-10上均取得最佳性能，验证了该方法在不同实验协议下的鲁棒性。

### 消融实验

#### 增强最优性割与剪枝约束的效果

Figure 4（左）展示了GBD迭代过程中上界（即当前最佳可行解的Wasserstein距离）的收敛行为。Wass.+EOC+P在早期迭代中即获得更好的上界，收敛速度显著快于仅使用Lagrangian约束的基础GBD。这归因于：
- **增强最优性割（EOC）**：利用Wasserstein距离的性质（如三角不等式、最小正距离下界）为松弛主问题提供更紧的下界，加速搜索。
- **剪枝约束（P）**：移除高Wasserstein距离核心集附近的搜索邻域，引导搜索向更有希望的区域集中。

消融结果证实，EOC和P共同作用使GBD在合理时间内获得高质量解，是实现低预算主动学习优势的关键技术组件。

#### 距离度量的选择

Figure 6展示了使用Cosine距离替代Euclidean距离作为Wasserstein度量基础的消融实验。在CIFAR-10上，Cosine距离在多数预算下获得更好的下游分类准确率。论文分析认为，这源于SimCLR预训练目标本身基于Cosine相似度，因此在同一度量空间中进行核心集选择能更好地保持特征结构的一致性。这一发现提示：核心集选择所用的距离度量应与特征预训练目标对齐。

### 定性分析

Figure 7提供了特征空间的t-SNE可视化对比。在STL-10（B=10）和CIFAR-10（B=20）上，k-centers和k-medoids选择的核心集存在明显的覆盖盲区（如STL-10的右上区域），而Wass.+EOC选择的样本更均匀地覆盖了整个特征流形。这一可视化证据直观解释了GBD方法在低预算下准确率优势的来源：避免遗漏特征空间中的重要聚类区域。

Figure 8–10展示了各方法实际选中的图像示例。Wass.+EOC倾向于选择更多样化、更具代表性的样本，而随机选择和启发式方法则可能出现冗余选择或遗漏关键类别。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2106_02968/figures/021_Figure_8.jpg]]
*Figure 8: Images selected for labeling on STL-10 with different methods: Wass. + EOC (top left), k-centers (top right), k-medoids (bottom left), Random (bottom right). The first two rows were selected in the first two rounds and every two rows after were selected in the subsequent rounds*

### 失败模式与局限性

1. **运行时间瓶颈**：GBD求解器运行时间显著长于启发式基线（数小时 vs 数秒，Table 12）。虽然3分钟限制下仍优于k-medoids，但在需要频繁重新采样或处理超大规模数据集的场景下仍不实用。

2. **剪枝约束的局部最优风险**：在Amazon→Web域适应任务中，剪枝约束可能导致搜索空间过度受限，使GBD陷入局部最优，性能不及k-centers。这表明剪枝策略需要在探索与利用之间更精细地平衡。

3. **理论假设与实际使用的差距**：Theorem 1要求损失函数Lipschitz连续以保证Wasserstein距离上界核心集损失，但实验中使用的是交叉熵损失，该条件并不严格成立。虽然经验结果有效，但理论保证的适用性存在缺口。

4. **对特征质量的依赖**：整个方法建立在高质量特征表示之上（SimCLR预训练）。当特征空间不能良好反映样本语义相似性时，最小化Wasserstein距离的核心集选择可能无法转化为下游分类性能的提升。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2106_02968/figures/004_Figure_2.jpg]]
*Figure 2: Low budget active learning on CIFAR-10, SVHN and STL-10 using SimCLR pre-trained features. See Table 3 for detailed results for B $\leq$ 4 0 . See Appendix E.3 for full results up 1 0 ~ B $\le$ 1 8 0 . The solid lines are our models and the dashed lines are baselines. All plots show mean standard error over five runs. Our best models outperform baselines for most budgets

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2106_02968/figures/013_Table_9.jpg]]
*Table 9: Numerical values of main results in Figure 2. All entries show mean standard deviation over five runs. The best model for each budget range is bolded and underlined and the second best model is underlined*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2106_02968/figures/014_Table_10.jpg]]
*Table 10: Numerical values of results on domain adaptation. All entries show mean standard deviation over five runs. The best model for each budget range is bolded and underlined and the second best model is underlined*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2106_02968/figures/023_Figure_9.jpg]]
*Figure 9: Images selected for labeling on CIFAR-10 with different methods: Wass. + EOC (top left), k-centers (top right), k-medoids (bottom left), Random (bottom right). The first two rows were selected in the first two rounds and every two rows after were selected in the subsequent rounds*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2106_02968/figures/002_Table_1.jpg]]
*Table 1: Head-to-head comparison of our solver using Enhanced Optimality Cuts (EOC) versus kmedoids on the objective function value of problem (4) at different budgets. Lower values are better. For each data set, the best solution at each budget is bolded and underlined. All entries show means over five runs. See Appendix E.2 for standard deviations. We use a ResNet-18 (He et al., 2016) feature encoder for STL-10, ResNet-34 for CIFAR-10 and SVHN, and Resnet-50 for Office-31. Our head is a two-layer MLP. The downstream classifier is the pre-trained encoder (whose weights are frozen) with a new head in each round. Supervised learning is performed with cross entropy loss. We compute Wasserstein distanc...*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2106_02968/figures/003_Table_2.jpg]]
*Table 2: Wass. + EOC with limited runtimes versus k-medoids on problem (4) for CIFAR-10. The best solution for each budget is bolded and underlined. See Appendix E.2 for full results and Appendix E.6 for details on k-medoids runtime*



## 定位与知识库关联

### 1. 核心瓶颈与因果机制

**真实瓶颈**：在极低标注预算（如总样本数的1%以下）的主动学习场景中，现有启发式选择策略（如基于不确定性的Least Confidence/Maximum Entropy，或基于代表性的贪心k-centers）无法确保选出全局最具代表性的样本，导致分类性能明显下降。同时，直接求解核心集选择的大规模混合整数规划（MILP）在数据集较大时计算不可行。

**因果调节变量**：将核心集选择转化为最小化离散Wasserstein距离的MILP，并采用广义Benders分解（GBD）算法进行全局优化。该方法的核心机制在于：通过GBD将原大规模MILP分解为反复求解小规模Wasserstein距离子问题与松弛主问题，配合增强最优性割（EOC）和剪枝约束（P）加速收敛，从而在合理时间内获得高质量或全局最优解。

**核心洞察**：Wasserstein距离在Lipschitz连续损失函数条件下构成核心集损失的上界（Theorem 1），这为优化目标提供了理论依据。GBD框架天然适合此类具有可分结构的混合整数问题——子问题求解给定核心集下的Wasserstein距离（标准LP），主问题则通过累积的次梯度约束逐步逼近原问题的最优值。

### 2. 方法谱系中的定位

#### 2.1 与代表性基线方法的关系

所提方法**Wasserstein Core-set Selection via GBD (Wass. + EOC + P)** 在主动学习的代表性-多样性方法谱系中占据全局优化的一端，与以下基线形成清晰对比：

- **Random Selection**：简单下界基线，完全不考虑样本信息，在极低预算下表现最差。

- **基于不确定性的方法**：Least Confidence（Settles, 2009）和Maximum Entropy（Settles, 2012）仅利用分类器当前预测的不确定性来选择样本，忽略了数据分布的代表性。在低预算下，由于分类器尚未充分训练，不确定性估计不可靠，这些方法容易选择离群点或噪声样本。

- **基于代表性的贪心/启发式方法**：
  - **Greedy k-centers**（Sener & Savarese, 2017）：通过贪心最小化最大距离来覆盖特征空间，属于核心集方法的经典代表。其局限性在于贪心选择的次优性——每一步的局部最优无法保证全局覆盖质量。
  - **k-Medoids Cluster Centers**（Heitsch & Römisch, 2003）：将聚类中心作为代表性样本，计算效率高但同样缺乏全局最优性保证。实验表明，在SVHN上k-medoids获得的Wasserstein距离目标函数值约为GBD求解器的两倍（Table 1：0.173 vs. 0.080，B=140）。
  - **Wasserstein Adversarial Active Learning (WAAL)**（Shui et al., 2020）：同样利用Wasserstein距离，但采用对抗训练的贪心估计方式，未进行全局优化。在经典主动学习设置（Table 4）和极低预算场景下，Wass.+EOC+P均优于WAAL。

#### 2.2 方法改进的关键维度

| 改进维度 | 基线做法 | 本文做法 | 证据锚点 |
|---------|---------|---------|---------|
| 核心集选择策略 | 启发式或贪心方法（k-centers贪心、WAAL贪心） | 最小化Wasserstein距离的MILP，通过GBD进行全局优化 | Section 3, 3.2 |
| 优化保证 | 无最优性保证 | GBD在有限时间内收敛到全局最优解 | Section 3.1 |
| 求解加速 | 不适用 | 增强最优性割（EOC）+ 剪枝约束（P） | Section 3.2, Figure 4 |

#### 2.3 与后续工作的潜在关联

虽然本文发表于2021年，其方法设计为后续研究提供了以下可扩展方向：

- **与Sinkhorn距离的结合**：本文明确提出了将Sinkhorn距离及其梯度融入GBD框架的开放问题。Sinkhorn距离通过熵正则化使Wasserstein距离的计算更高效且可微，若能与GBD的最优性割兼容，有望大幅提升求解效率。
- **扩展到更复杂任务**：本文方法目前仅验证于图像分类和域适应任务。将其整数规划框架扩展到多标签分类、回归、目标检测或语义分割等任务，需要重新设计核心集损失的上界理论。
- **与自监督预训练的协同**：方法性能高度依赖特征表示质量（SimCLR预训练）。后续工作可探索如何将核心集选择与特征学习进行端到端联合优化。

### 3. 适用边界与局限性

#### 3.1 理论假设的边界

**Lipschitz连续性要求**：Theorem 1要求损失函数关于输入特征的Lipschitz连续性，这是Wasserstein距离上界核心集损失的关键前提。然而，实际使用的交叉熵损失并不严格满足这一条件（在预测概率接近0或1时梯度趋于无穷）。尽管经验结果表明方法仍然有效，但在理论严格性上存在缺口。

**离散Wasserstein距离的度量选择**：消融实验（Figure 6, Appendix E.7）表明，使用Cosine距离作为Wasserstein度量的基础比Euclidean距离在多数预算下获得更好的下游准确率，因为Cosine距离与SimCLR预训练目标一致。这意味着方法性能对度量函数的选择敏感——当特征空间与度量函数不匹配时，优化目标可能与下游任务目标偏离。

#### 3.2 计算效率的约束

**运行时间显著长于启发式方法**：GBD求解器需要数小时量级的运行时间，而k-medoids等启发式方法仅需数秒（Table 12）。虽然实验表明即使将GBD运行时间限制在3分钟，其求解质量仍优于k-medoids启发式（Table 2：CIFAR-10上Wass.+EOC在3分钟内获得0.082 vs. k-medoids的0.095），但对于需要频繁重新采样或大规模部署的场景，计算成本仍然过高。

**可扩展性上限**：论文声称方法在75,000样本的数据集上可优雅扩展（Section 4），但未在更大规模数据集（如ImageNet的百万级样本）上验证。每次GBD迭代需要求解一个完整的Wasserstein距离LP子问题，其复杂度至少为$O(N^3)$（其中$N$为未标注池大小），这在大规模场景下可能成为瓶颈。

#### 3.3 优化质量的潜在风险

**剪枝约束的局部最优风险**：剪枝约束（P）通过移除高Wasserstein距离核心集附近的搜索邻域来加速收敛，但这可能使GBD陷入局部最优，牺牲全局最优性保证。在域适应任务Amazon→Web中，k-centers在中等预算下的表现优于本文方法（Table 11），这暗示剪枝约束可能过度限制了搜索空间。

**对特征质量的依赖**：整个方法建立在高质量特征表示的基础上（通过SimCLR或f-DAL预训练获得）。当特征质量较差（如预训练数据与目标任务分布差异大）时，Wasserstein距离在特征空间中的代表性可能与真实标签空间中的代表性出现偏差，导致所选样本的标注价值下降。

### 4. 开放问题

1. **Sinkhorn距离的集成**：能否将Sinkhorn距离及其梯度直接融入GBD框架，并保证增强最优性割的可行性？这需要解决熵正则化项对偶形式与现有最优性割的兼容性问题。

2. **任务泛化**：如何将该整数规划方法扩展到多标签分类、回归、目标检测或语义分割等更复杂的任务？核心挑战在于为这些任务设计合适的核心集损失上界（类似Theorem 1）。

3. **求解效率提升**：是否可以通过自适应调整GBD参数（如剪枝强度、割平面添加频率）或结合强化学习来进一步缩短运行时间并保持优化质量？

4. **大规模验证**：在更大规模数据集（如ImageNet）上，该方法是否依然可行且优于启发式方法？需要验证GBD在百万级样本下的收敛行为。

5. **跨模态与持续学习扩展**：是否存在针对跨模态主动学习（如视觉-语言模型的选择）或主动持续学习（需要在避免灾难性遗忘的同时选择新任务样本）的扩展？这需要重新定义Wasserstein距离的度量空间和核心集损失的上界。

6. **与不确定性方法的融合**：本文方法纯基于代表性，是否可以将不确定性信息（如分类器的熵）作为Wasserstein距离度量中的加权项，从而同时优化代表性和信息量？



## 原文 PDF

![[paperPDFs/ICLR_2022/Low_Budget_Active_Learning_via_Wasserstein_Distance_An_Integer_Programming_Approach.pdf]]
