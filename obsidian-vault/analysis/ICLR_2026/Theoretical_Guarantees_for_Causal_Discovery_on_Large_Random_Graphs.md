---
title: "Theoretical Guarantees for Causal Discovery on Large Random Graphs"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Theoretical_Guarantees_for_Causal_Discovery_on_Large_Random_Graphs.pdf
aliases:
- TGCDLRG
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/causality
core_operator: "随机干预下基于评分的因果排序误差函数，并用结构 Lipschitz 常数与 McDiarmid 不等式推导 FNR 集中界。"
primary_logic: |
  将最优因果序产生的拓扑错误定义为 f(I)，归一化为 FNR g(I)；先用祖先/后代规模控制单节点干预翻转的 Lipschitz 常数，再将 McDiarmid 不等式应用到随机干预向量，最后在 ER 和 BA 随机图模型中把结构界转化为随图规模 d 收敛的期望与集中速率。
claims:
- "在稠密与稀疏 ER 图以及广义 BA 图上，FNR 的期望上界和围绕期望的集中速率可由随机图结构量给出。"
- "模拟实验显示 ER 图和较轻尾 BA 图中的 FNR 变异随图规模增大而下降，极重尾 BA 情形是主要失效边界。"
---

# Theoretical Guarantees for Causal Discovery on Large Random Graphs

> [!tip] 核心洞察
> 在随机干预和弱化的 ϵ-interventional faithfulness 条件下，因果排序的 FNR 可以通过结构 Lipschitz 常数转化为有界差分集中问题；随机图模型进一步给出随节点规模收敛的平均情况误差界。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Theoretical Guarantees for Causal Discovery on Large Random Graphs |
| 英文题名 | Theoretical Guarantees for Causal Discovery on Large Random Graphs |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=V7pT2ZRoTB) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/causality |
| Method |  |
| Dataset | |

## 概述

本文针对“大规模随机图上的干预式因果发现”这一场景，研究**错误定向率（False Negative Rate, FNR）**如何随着图规模增大而收敛。核心问题是：在只能随机选择干预节点、且允许存在隐混淆的ϵ‑interventional faithfulness假设下，能否为因果序的重建误差提供有限的样本集中保证？

**方法定位：** 作者将因果序优化问题视为一个确定性的组合优化（唯一最优序），然后推导出错误函数关于干预变量和边变量的Lipschitz常数。在此基础上，利用McDiarmid不等式及Warnke的0–1典型有界差异不等式，将结构灵敏度转化为关于误差的有限维集中不等式。

**主要结果（理论）：** 在三类随机图模型上给出了错误率的**期望上界**与**集中速率**。对于稠密 Erdős–Rényi 图，FNR 的期望为 $O(1/d)$，波动集中在 $O(d^{-1})$；对于稀疏 Erdős–Rényi 图（边密度 $p_e = c/d$），期望为 $O(1/d)$，波动集中在 $O(1/\sqrt{d})$；对于 Barabási–Albert 无标度网络，期望上界与干预覆盖率相关，波动集中在 $O(d^{\beta -1})$，其中 $\beta \in (0,1)$ 由度指数 $\gamma$ 决定。

**实验验证：** 模拟实验表明，经验FNR均值始终低于理论界（除极高干预覆盖率外），且误差的标准差和四分位距随图规模 $d$ 增大而单调下降，定量支持了理论预测的“大图更可靠”趋势。

> 注意：实验中出现的高干预覆盖率下界限偶尔被突破的现象，可能与优化算法的次优性有关，需进一步人工核查。
</td><td>

## 背景与动机

因果发现的核心任务是从观测或实验数据中恢复变量间的有向因果关系。当仅靠观测数据无法唯一确定因果方向时，干预实验成为关键的定向工具。然而，现实中的干预往往成本高昂、次数有限，且实验者可能只能对随机选取的节点进行干预，无法精确控制哪些变量被扰动。在此类约束下，基于评分函数的排序方法（即寻找一个与干预数据最一致的变量全序）被证明可以在一定条件下一致地恢复真实因果序。这些方法避免了直接估计等价的因果结构类（MEC），且通过分数优化可实现大规模应用，但其统计行为的理论保障仍存在显著缺口。

当前文献中的理论结果主要针对最坏情况的图结构——例如限定最大度或有界树宽——提供的性能界虽具通用性，却往往过于保守，难以反映真实随机图（如 Erdős–Rényi、无尺度网络）在“平均情况”下的实际表现。较少的工作尝试在平均意义上分析因果发现算法的错误率，且多数分析仍依赖较强的假设：完整 faithfulness、因果充分性（不存在潜在混杂），以及已知观测等价类的骨架。对于干预随机选择、允许潜在混杂且仅满足弱 faithfulness 条件（如 ε‑interventional faithfulness）的场景，缺乏对关键评价指标——错误定向率（false negative rate，FNR）——的系统理论刻画。

针对上述缺口，本文聚焦于随机图模型上基于随机干预的因果序恢复问题，在仅假设 ε‑interventional faithfulness 且允许潜在混杂的框架下，分析 FNR 的期望上界及其围绕期望的集中性。目标是推导有限维度的偏差界，从而定量回答：在大规模图中，误定向比例如何随节点数增长而趋于零，其波动幅度（方差或标准差）以何种速率收缩。相关理论结果总结于 [Table 1](#table-1)，覆盖稠密 Erdős–Rényi、稀疏 Erdős–Rényi 与广义 Barabási–Albert 三类典型随机图，为理解非最坏情况下的干预实验效率提供了更精确的指导。

## 核心创新

本研究的核心贡献在于 **理论层面**：它不再提出新的因果发现算法，而是为现有基于评分的拓扑排序方法在随机干预下的统计行为建立了首个 **有限维浓度边界**（finite‑dimension deviation bounds）。与 prior work 相比，关键的 **changed slots** 集中在假设条件、干预机制与分析目标三个维度。

### 1. 放宽的因果假设：从完全忠实性到 ϵ‑干预忠实性
以往的大多数因果发现理论要求 **完全忠实性**（full faithfulness），甚至默认不存在隐混杂。本工作采用更弱的 **ϵ‑interventional faithfulness**（`We adopt an ϵ‑interventional faithfulness assumption … allows for latent confounding and does not require the full faithfulness property to hold`），显式允许潜在的混杂因子存在，且不要求所有条件独立性都对应到图上的缺失边。这一变化使理论覆盖了更真实的因果场景。

### 2. 随机干预机制替代自适应干预设计
传统理论常将干预视为 **精心选择** 的集合（如充足干预集、自适应策略），而本文假定干预是 **完全随机** 的（`Interventions are assumed to be selected at random, mimicking experimental designs where only limited control over perturbations is feasible`）。这种设定更贴近高通量干预实验，但也导致错误率成为随机变量，需要概率浓度分析。

### 3. 从最坏情形保证转向典型情形浓度分析
此前的工作多为 **最坏情况** 误差界（例如 bounded‑degree 图下的保证），但这类界可能过于保守且不反映实际大规模图中的行为。本文聚焦于 **随机图模型下的平均情形**，为一族常用的随机图模型（稠密 ER、稀疏 ER、广义 BA 模型）导出了 **拓扑错误** $f(\mathbf{I})$ 以及 **归一化假阴性率（FNR）** $g(\mathbf{I})=f(\mathbf{I})/|E|$ 在期望值附近的 **钟型浓度界**（例如 `Theorem 8` 给出稠密 ER 中 FNR 的标准化波动为 $O(1/\sqrt{d})$）。这些结果表明：随着图规模增长，FNR 的变化性会迅速消失，从而提供了一种维度依赖的行为预测。

### 4. 结构敏感性的显式刻画：Lipschitz 常数
为了应用 McDiarmid 不等式，本文引入 **局部 Lipschitz 常数**（`Flipping the intervention status of a node k can only affect edges that “use k as evidence.” Counting these provides a structural bound`）。该常数直接由节点的 **祖先** 与 **子孙** 规模界定（`c_k ≤ |Anc(k)| + |Desc(k)|`），将拓扑误差函数对单个干预变量的敏感度转化为可控量，进而得到在各随机图参数下的尾概率界（ER、BA 模型的渐近阶见表 1）。

### 5. 理论覆盖的图族与尺度律
通过统一的分析框架，本文首次系统给出了三类随机 DAG 模型下 **期望 FNR 与浓度速率的渐近阶**：

* **稠密 ER**：期望 FNR 约为 $O\bigl(2(1-p_{\mathrm{int}})^2/(p_{\mathrm{int}} d)\bigr)$，浓度率 $O(d^{-1/2})$。
* **稀疏 ER**：浓度率增至 $O(d^{-1/2} \log d)$ 规模，仍随 $d$ 消失。
* **广义 BA 模型**（幂律指数 $\gamma = 2+\kappa/m$）：浓度率依赖于 $d^{-\beta/2}$，其中 $\beta = 1/(\gamma-1)$；当尾部极重（$\gamma<3$，即 $\kappa=1$）时浓度失效，与仿真中 IQR 不稳定的现象吻合。

这些结果形成了一个与真实图结构特征（密度、度分布）挂钩的 **尺度律**，为干预实验的规模规划提供了定量参考。

> **需要说明**：由于原始分析材料未提取出论文的具体方法名称及显式 baseline 算法，上述“changed slots”是基于理论贡献描述与 prior work 对比推断的。若需指明精确的对比基准（例如 Chevalley et al. 2024 的算法），请结合附录中的 ‑related‑work 部分进行人工核实。

## 整体框架

![[assets/figures/papers/iclr26_0016_V7pT2ZRoTB_Theoretical_Guarantees_for_Causal_Discovery_on_L/figures/001_Table_1.jpg]]
*Table 1: Summary of theoretical results Asymptotic orders for the expected topological error and the concentration rate (typical deviation scale around the mean) in the three random-graph regimes considered. For the generalized Barabasi–Albert (BA) model, ´ $\begin{array} { r } { \beta = \frac { 1 } { \gamma - 1 } } \end{array}$ with $\gamma$ = 2 + $\kappa$ / m , $\kappa$ > 0 f measures the number of misorentations in the predicted causal order, whereas g is normalized by the number of true edges (false-negative rate (FNR)). The probability for a variable to be intervened on is denoted $p _ { i n t }$

本文的理论分析围绕单一核心问题展开：**在随机干预设计下，基于得分最大化的因果顺序估计器产生的错误发现率（False Negative Rate, FNR）如何在随机图模型中集中于其期望。** 分析框架将这一问题拆解为三个相互衔接的步骤：首先在**固定图**上建立误差对干预扰动的灵敏度控制，然后通过**有界差异不等式**得到一般图的集中界，最后借助**随机图模型的度分布性质**将一般界收缩为仅依赖于图规模（节点数 $d$）的均匀偏差速率。整个过程对应的输入、中介与分析输出如下所示。

### 问题设定与误差度量

- **干预模型**：每个节点独立以概率 $p_{\mathrm{int}}$ 被干预，干预向量 $\mathbf{I} \in \{0,1\}^d$ 标记每个节点的干预状态。图 $\mathcal{G}$ 来自随机图族 $\mathcal{G}$（Erdős–Rényi 或 Barabási–Albert），边集 $\mathbf{E}$ 与干预向量 $\mathbf{I}$ 相互独立。
- **因果顺序估计**：基于得分函数 $S(\pi, \epsilon, D, \mathcal{T}, P_X^{\mathcal{C},(\emptyset)}, \mathcal{P}_{\mathrm{int}}, c)$ 并采用确定性打破平局规则（Assumption 2），得到唯一最优顺序 $\pi_{\mathrm{opt}}$。
- **误差度量**：定义未归一化的拓扑错误 $f(\mathbf{I}) := D_{\mathrm{top}}(\mathcal{G}, \pi_{\mathrm{opt}}(\mathbf{I}))$（方向与真实顺序相反的总边数）及归一化版本 $g(\mathbf{I}) := f(\mathbf{I}) / |E|$（即 FNR）。

### 分析流水线

**步骤 1：灵敏度分析（Lipschitz 界）**  
翻转任意节点 $k$ 的干预状态对误差的影响受限于其祖先与后代集合的规模之和：
$$c_k = |\mathrm{Anc}(k)| + |\mathrm{Desc}(k)|,\qquad c_k^g = \frac{c_k}{|E|}.$$
这一结构灵敏度将空间扰动的局部效应转化为可计算的图论量（Lemma 3）。

**步骤 2：通用集中不等式（McDiarmid 应用于 $\mathbf{I}$）**  
对任意固定图 $\mathcal{G}$，利用上述 Lipschitz 常数，误差相对其均值的偏差满足：
$$\Pr\!\big( |f(\mathbf{I}) - \mathbb{E}[f(\mathbf{I})]| \ge t \big) \le 2\exp\!\left( -\frac{2t^2}{\sum_{k=1}^{|V|} c_k^2} \right),$$
对归一化误差 $g$ 亦成立类似不等式。这一步将干预向量的随机性转化为仅依赖图结构的尾部控制。

**步骤 3：随机图集成与分模型分析**  
将图 $\mathcal{G}$ 也视为随机对象（取自 ER 稠密、ER 稀疏或广义 BA 模型），利用这些随机图的度分布和边数的高概率界，求出 $\sum c_k^2$ 的一致上界，从而得到仅与图大小 $d$、图密度参数和干预概率 $p_{\mathrm{int}}$ 相关的偏差速率。例如：
- **ER 稠密**（$p_e = \Theta(1)$）：$\sum c_k^2 \le C_1 d^4$，给出 $f$ 的 $O(d^2)$ 尺度集中。
- **ER 稀疏**（$p_e = c/d$）：$\sum c_k^2 \le C_2 d^3 \log d$，集中尺度为 $O(d\log d)$。
- **BA 幂律图**（度指数 $\gamma = 2 + \kappa/m$）：最大度以 $O(d^\beta)$ 被控制（$\beta = 1/(\gamma-1)$），派生相应的偏差尾界（Theorem １０ 等）。

表　1 汇总了各图族下期望误差与集中速率的渐近阶。

整个框架的输入是随机图模型与干预设计，输出是 FNR 的期望渐近界和围绕期望的偏差概率界，从而为一类基于得分的因果发现算法提供了平均情形下的可靠性与变异性刻画。

## 核心模块与公式推导

**误差度量与问题形式化**  
记 $\mathcal{G}$ 为真实的底层有向无环图（DAG），$\pi$ 为变量的一个拓扑排序。定义**拓扑误差**为排序中反序边的总数：
$$D_{\mathrm{top}}(\mathcal{G}, \pi) = \sum_{\pi(i) > \pi(j)} \mathbf{A}_{ij}^{\mathcal{G}},$$
其中 $\mathbf{A}^{\mathcal{G}}$ 是 $\mathcal{G}$ 的邻接矩阵。给定干预变量向量 $\mathbf{I} \in \{0,1\}^{|V|}$（$I_k=1$ 表示节点 $k$ 被施加硬干预）和边集 $\mathbf{E}$，最优排序 $\pi_{\mathrm{opt}}$ 通过最大化一个评分函数得到（假设满足唯一性条件，Assumption 2）：
$$\pi_{\mathrm{opt}} = \arg\max_{\pi}^{\star} S(\pi, \epsilon, D, \mathcal{T}, P_X^{\mathcal{C},(\emptyset)}, \mathcal{P}_{\mathrm{int}}, c).$$
在此基础上定义两个核心误差函数：

- **未归一化误差**（unormalised error）  
  $$f(\mathbf{I}) := D_{\mathrm{top}}(\mathcal{G}, \pi_{\mathrm{opt}}(\mathbf{I})),$$
- **归一化误差/假阴性率**（FNR）  
  $$g(\mathbf{I}) := \frac{f(\mathbf{I})}{|E|},$$
其中 $|E|$ 为图的总边数。$g$ 即被错误定向的边所占的比例，是本文主要的浓度分析对象。

**Lipschitz 性质与有界差分结构**  
为应用麦克迪阿米德（McDiarmid）不等式，需要将误差函数对单个随机变量（干预 $I_k$ 或边 $E_{ij}$）的敏感性控制在一个 Lipschitz 常数内。论文证明：翻转某个节点 $k$ 的干预状态所影响的边只能是那些“以 $k$ 为证据”的边，其数量由 $k$ 的祖先集与后代集大小决定。由此得到对 $f$ 和 $g$ 的利普希茨常数：
$$c_k \le |\mathrm{Anc}(k)| + |\mathrm{Desc}(k)|, \qquad c_k^g = \frac{c_k}{|E|}.$$
$c_k$ 是 $f$ 关于 $I_k$ 的最大可能变化量，$c_k^g$ 是 $g$ 的对应常数。这一有界差分结构将图的结构特征（祖先/后代规模）直接转化为对随机扰动灵敏度的数值控制，是后续所有浓度界推导的枢纽。

**通用浓度不等式**  
将上述利普希茨常数代入麦克迪阿米德不等式，立刻得到适用于任意图的浓度尾概率界。对未归一化误差：
$$P\left( \left| f(\mathbf{I}) - \mathbb{E}[f(\mathbf{I})] \right| \ge t \right) \le 2 \exp\left( -\frac{2 t^2}{\sum_{k=1}^{|V|} c_k^2} \right),$$
对归一化误差（FNR）：
$$P\left( \left| g(\mathbf{I}) - \mathbb{E}[g(\mathbf{I})] \right| \ge t \right) \le 2 \exp\left( -\frac{2 t^2 |E|^2}{\sum_{k=1}^{|V|} c_k^2} \right).$$
这两个不等式将尾概率的衰减速率与各节点影响力 $c_k$ 的平方和绑定，是全文分析的理论模板。

**随机图模型中的具体浓度阶数**  
将通用界应用于三种随机图模型，通过对 $c_k$ 的阶进行概率分析，得到渐近浓度速率与图尺寸 $d$ 的显式关系。

- **稠密 Erdős–Rényi (ER)**（$p_e = \Theta(1)$）：所有节点的度集中在 $\Theta(d)$，$\sum_k c_k^2 = O(d^4)$。定理 8 给出：
  $$P\left( \left| f(\mathbf{I},\mathbf{E}) - \mathbb{E}[f(\mathbf{I},\mathbf{E})] \right| \ge t \right) \le 2 \exp\left( -\frac{2 t^2}{C_1 d^4} \right),$$
  且归一化误差 $g$ 在 $O(1/\sqrt{d})$ 尺度上集中。

- **稀疏 ER**（$p_e = c/d$）：最大度约为 $O(\log d)$，定理 9 表明 $f$ 在 $O(d \log d)$ 尺度上集中。

- **广义 Barabási–Albert (BA) 模型**：新节点按优先连接概率  
  $$P(i) = \frac{k_i + \kappa}{\sum_j (k_j + \kappa)}$$
  依附于已有节点，并强制所有边从旧指向新以保证 DAG 性质。度分布服从幂律 $P(k) \sim k^{-\gamma}$，其中 $\gamma = 2 + \kappa/m$，并记 $\beta = 1/(\gamma-1)$。引理 10 导出最大度的高概率界 $\deg(i) \le m + C d^{\beta}$，以此控制 $c_k$ 的上界。该模型下 $g$ 的浓度行为取决于参数 $\kappa$：当 $\kappa \ge 3$ 时理论保证强，IQR 随 $d$ 衰减；但当 $\kappa = 1$（$\gamma = 7/3 < 3$）时，理论界失效，实证也显示方差不再消失。

以上阶数关系汇总在 Table 1 中，完整给出了未归一化误差的期望阶与两种误差度量在不同图族下的浓度速率。

## 实验与分析

### 主结果：FNR 的浓度行为随图尺度变化
论文通过模拟实验验证了归一化拓扑误差（即假阴性率 FNR）围绕其期望的浓度性质。实验在三种随机图模型上进行：稠密 Erdős–Rényi（ER, $p_e = \Theta(1)$）、稀疏 ER（$p_e = c/d$）和广义 Barabási–Albert（BA）无标度网络。对每种图族，扫描了三个密度参数与三个干预覆盖概率 $p_{\mathrm{int}}$，在多个图尺寸 $d$ 下独立生成图、随机干预，并计算最优因果序下的 FNR 的四分位距 (interquartile range, IQR)，以刻画样本间变异（见 Figure 1）。


![[assets/figures/papers/iclr26_0016_V7pT2ZRoTB_Theoretical_Guarantees_for_Causal_Discovery_on_L/figures/004_Figure_1.jpg]]
*Figure 1: Interquartile range (IQR) of the FNR as a function of graph size d. For each graph family, results are shown across three density parameters and three values of intervention coverage $p _ { \mathrm { i n t } }$ . The IQR decreases with d , demonstrating vanishing variability as predicted by our theoretical results, except for scale-free BA graphs with $\kappa$ = 1 , which correspond to the heavy-tailed regime with exponent $\begin{array} { r } { \gamma = \frac { 7 } { 3 } < 3 } \end{array}$

- **ER 图（稠密与稀疏）**：IQR 随 $d$ 增大迅速收敛到零，与理论给出的 $O(d^{-1/2})$（稠密）或 $O(d^{-1})$（稀疏）浓度速率一致。
- **BA 图**：当吸引参数 $\kappa = 3.0$ 和 $\kappa = 9.0$（对应度指数 $\gamma \approx 3.5$ 和 $\gamma \approx 4.6$）时，IQR 随 $d$ 明显减小；但当 $\kappa = 1.0$（$\gamma = 7/3 < 3$）时，IQR 呈现剧烈波动，并未随图尺寸增大而消失。这一现象与理论分析相吻合：$\kappa=1$ 对应于度分布过于重尾，此时最大度上界 $O(d^{\beta})$ 中的指数 $\beta = 1/(\gamma-1) > 1$ 不再满足理论框架所需的约束。

### 消融实验
论文未提供针对算法组件或假设的消融实验。作者仅在有限条件下验证了浓度不等式的定性行为，未对不同成分（如评分函数、干预策略、优化准则）进行剥离分析。若需正交验证干预概率 $p_{\mathrm{int}}$ 的影响，现有实验仅通过固定离散取值扫描，并未给出独立消融。

### 失败模式与局限
- **BA 图 $\kappa=1$ 下的失效**：如上所述，当度分布极重尾时，误差函数的 Lipschitz 常数增长过快，使得 McDiarmid 不等式边界变得空虚，IQR 不随 $d$ 缩小。这表明理论保证对图模型的度尾特性敏感，且当前界限未达到对任意 BA 参数均有效的程度。
- **$p_{\mathrm{int}}$ 的非显式依赖**：实验虽然设置了不同干预概率，但论文的理论结果目前未能刻画误差浓度与 $p_{\mathrm{int}}$ 的函数关系；未来工作需对此给出更精细的界限。
- **平均情况与随机设计的局限**：所有分析建立在干预随机分配、无自适应策略的前提下。论文承认，向自适应干预或更广泛图分布的外推是开放问题。

### 重要图表结论
- **Table 1** 总结了三种图模型下期望拓扑误差 $f$ 与归一化误差 $g$ 的渐近界及其理论浓度率。实验定性符合这些渐近趋势：稠密和稀疏 ER 的 FNR 均值小且变异性低；BA 图当 $\kappa$ 较大时行为接近理论预测。
- **Figure 1** 直观展示了浓度速率的定性有效性，同时提供了唯一反例（$\kappa=1$），明确了理论适用边界。该图也可作为未来改进理论的基准：任何更一般的浓度定理都应能复现图中除 $\kappa=1$ 外的缩小趋势，并合理解释重尾失效情形。

### 补充图表

![[assets/figures/papers/iclr26_0016_V7pT2ZRoTB_Theoretical_Guarantees_for_Causal_Discovery_on_L/figures/010_Figure_3.jpg]]
*Figure 3: Mean false negative rate (FNR) versus graph size d across Erdos–R ˝ enyi (ER), scale-free ER, ´ and Barabasi–Albert (BA) graphs. The solid lines with points denote empirical averages; lines without ´ points show theoretical upper bounds from Appendix E. The bounds hold across all settings, with a slight mismatch at high intervention coverage ( $p _ { \mathrm { i n t } }$ = 0 . 7 5 ) , likely due to optimization difficulties in DiffIntersort. 30*

![[assets/figures/papers/iclr26_0016_V7pT2ZRoTB_Theoretical_Guarantees_for_Causal_Discovery_on_L/figures/007_Figure_2.jpg]]
*Figure 2: Standard deviation of the FNR as a function of graph size d . For each graph family, results are shown across three density parameters and three values of intervention coverage $p _ { \mathrm { i n t } }$ . The deviation vanishes with growing d , in line with theory, except for scale-free BA graphs with $\kappa$ = 1 ， corresponding to a heavy-tailed regime with exponent $\begin{array} { r } { \gamma = \frac { 7 } { 3 } < 3 } \end{array}$

![[assets/figures/papers/iclr26_0016_V7pT2ZRoTB_Theoretical_Guarantees_for_Causal_Discovery_on_L/figures/013_Figure_4.jpg]]
*Figure 4: Mean unnormalized error $D _ { \mathrm { t o p } }$ versus graph size d across Erdos–R ˝ enyi (ER), scale-free ER, ´ and Barabasi–Albert (BA) graphs. ´*

![[assets/figures/papers/iclr26_0016_V7pT2ZRoTB_Theoretical_Guarantees_for_Causal_Discovery_on_L/figures/020_Figure_7.jpg]]
*Figure 7: Empirical scaling of the maximum degree in BA graphs with m = 3 edges per node for different values of $\kappa$ . Fitted lines correspond to estimated exponents $\hat { \gamma }$ , compared against theoretical predictions. Graph sizes range from d = 3 0 to d = 4 0 0 0 . The close match confirms that the generated graphs reproduce the expected heavy-tailed scaling


## 方法谱系与知识库定位

本文属于**因果发现平均情况理论分析**的早期工作，其直接影响来自 Chevalley 等人 (2025c) 提出的基于 `$\epsilon$`-interventional faithfulness 和单节点随机干预的评分排序框架。该框架本身已将传统因果发现从最坏情形（如固定度图）的保守保证[2] 转向可扩展的目标函数优化，本文则进一步将理论扩展至**平均情况**：在随机图模型（ER 稠密/稀疏、广义 BA）和随机干预设计下，首次为错误率 `$g(\mathbf{I},\mathbf{E})$`（FNR）导出了有限样本偏差界（concentration bounds）。与此前主要关注无向骨架识别或有向边的*存在性*保证不同，本文通过 McDiarmid 不等式与结构 Lipschitz 常数（Lemma 3）将图的结构敏感性转化为误差函数的波动控制，从而建立了**误差围绕期望的典型偏差尺度**（见表 1）。

### 与基线/后续工作的关系

- **相对基底方法**：此前最坏情形分析的偏差界通常针对有界度图，结果为 `$O(\text{poly}(d))$` 级别但过于悲观。本文在稠密 ER 图中显示未归一化误差的 concentration 尺度为 `$O(d^2)$`，归一化 FNR 的尺度则为 `$O(d^{-1/2})$`（Theorem 8），表明在大图极限下波动以多项式速率消失——这在平均意义上显著收紧了已有认识。
- **从算法到理论的反哺**：Chevalley 等人 (2024) 已给出大规模求解该评分问题的算法，本文的浓度结果解释了为何**在随机干预稀疏甚至仅少量干预时算法仍能稳定输出**，并预测了 FNR 的波动随图规模 `$d$` 衰减的速率（图 1 实证支持）。未来算法优化可将偏差界作为干预预算分配的指导信号。
- **方法与误差度量扩展**：现有工作常关注结构汉明距离（SHD）或未归一化拓扑误差 `$f$`，本文首次将分析转向 FNR，建立了 `$g$` 的 concentration，并与期望值分析（Appendix E）结合，形成**完整的理论图景**。后续研究可进一步推广到其他复合误差度量（如因果效应估计误差）。

### 适用边界

1. **图模型假设**：理论成立的严格前提是图来自 ER 稠密、ER 稀疏或广义 BA 模型，且 ER 中的边独立、BA 中依附概率遵循 `$P(i) = (k_i+\kappa)/\sum_j (k_j+\kappa)$` 并强制时间顺序形成 DAG。偏离这些分布（如存在社区结构或幂律尾极重）时，给定的偏差界可能不确。
2. **干预机制与目标函数**：要求干预随机均匀分配（`$p_{\mathrm{int}}$` 固定），且最优排序 `$\pi_{\mathrm{opt}}$` 由评分函数唯一确定（Assumption 2 保证确定性 tie‑breaking）。若干预自适应、目标函数非光滑或存在多个最优点，现有 Lipschitz 分析需重新修正。
3. **因果假设**：依赖 `$\epsilon$`-interventional faithfulness（允许隐混淆但限制违背程度），未强制因果充分性。因此结果适用于存在隐变量但 faithfulness 仅轻微违反的场景；完全任意隐变量结构下浓度结论需审慎评估。

### 局限与开放问题

**关键局限**：
- **尺度依赖隐晦**：理论给出 `$\mathbb{E}[g]$` 和偏差的渐近阶，但并未显式揭示偏差如何依赖干预概率 `$p_{\mathrm{int}}$`（Table 1 中的 `$O(d^{-1/2})$` 等与 `$p_{\mathrm{int}}$` 无关）；这对实际选择干预预算指导有限。
- **实证覆盖有限**：模拟仅在有限参数范围内验证，且对广义 BA 模型 `$\kappa=1$`（对应 `$\gamma=7/3<3$`，无有限方差）表现不稳定，IQR 未随 `$d$` 单调收敛，表明理论在**极重尾情形**可能失效。
- **算法依赖性抽象**：分析假设 `$\pi_{\mathrm{opt}}$` 准确可计算，但现实算法仅求得近似解；近似解对 concentration 的影响未被纳入。

**开放问题**（直接摘自原文与不足识别）：
1. **自适应干预策略的扩展**：将浓度结果扩展到序贯或主动干预选择，给出依赖 `$p_{\mathrm{int}}$` 的非渐近界。
2. **超出现有误差度量**：分析结构干预距离（SID）、精确恢复概率等其他拓扑误差的 concentration 行为。
3. **更广泛图族**：放宽随机图模型的强结构假设（如允许潜在块结构、几何随机图），开发更通用的分析方法。
4. **实用算法衔接**：针对单节点干预下的大规模因果发现，设计能利用 concentration 特性的近似算法，使理论保证转化为可实用的误差控制（如置信区间）。

（注：文中部分结论需结合原文 Table 1 与 Appendix E 的理论期望界综合评估；Figure 1 仅提供仿真佐证，未涵盖所有图族‑密度‑干预覆盖组合，因此表述“普遍性”需人工核实。）

## 原文 PDF

![[paperPDFs/ICLR_2026/Theoretical_Guarantees_for_Causal_Discovery_on_Large_Random_Graphs.pdf]]
