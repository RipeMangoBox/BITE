---
title: "Causal Discovery in the Wild: A Voting-Theoretic Ensemble Approach"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Causal_Discovery_in_the_Wild_A_Voting_Theoretic_Ensemble_Approach.pdf
project_link: null
code_link: null
openreview_forum_id: WtbPaWO8lH
aliases:
- BE
- CDWVTEA
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/causality
core_operator: "引入基于贝叶斯投票规则的加权聚合机制，并通过最优传输估计专家能力矩阵，从而为聚合提供理论收敛保证和可导优化。"
primary_logic: "将图结构分解为边级子结构，对每个子结构的投票分布进行贝叶斯加权，利用最优传输从投票配置中学习专家能力参数，实现高维因果图的可识别聚合。"
claims:
- "在专家独立且具有信息量的条件下，贝叶斯投票的错误概率随专家数量和平均 KL 散度指数衰减（Theorem 1）。"
- "至少 (2m-1) 名信息量专家可保证参数可识别性（Theorem 2），并在此条件下最小 Kantorovich 估计量一致收敛。"
- "GP-ER (continuous, d=20) 上 SID / SHD / F1 = Plurality + Bayes Est.: 199 / 35 / 0.500"
- "MLP-SF (continuous, d=40) 上 SID / SHD / F1 = Rank + Bayes Est.: 169 / 18 / 0.865"
---

# Causal Discovery in the Wild: A Voting-Theoretic Ensemble Approach

> [!tip] 核心洞察
> 将图结构分解为边级子结构，对每个子结构的投票分布进行贝叶斯加权，利用最优传输从投票配置中学习专家能力参数，实现高维因果图的可识别聚合。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 野外因果发现：一种投票论集成方法 |
| 英文题名 | Causal Discovery in the Wild: A Voting-Theoretic Ensemble Approach |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=WtbPaWO8lH) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/causality |
| Method | Bayes Est.（基于最优传输能力估计的特征级贝叶斯投票聚合） |
| Dataset | GP-ER (continuous, d=20), MLP-SF (continuous, d=40), Sachs (continuous, d=11) |

> [!tip] 效果简介
> - GP-ER (continuous, d=20) 上，SID / SHD / F1 为 Plurality + Bayes Est.: 199 / 35 / 0.500，对比 Plurality + Rank: 204 / 38 / 0.435，变化 SID -5, SHD -3, F1 +0.065。
> - MLP-SF (continuous, d=40) 上，SID / SHD / F1 为 Rank + Bayes Est.: 169 / 18 / 0.865，对比 Rank + Rank: 187 / 20 / 0.851，变化 SID -18, SHD -2, F1 +0.014。
> - Sachs (continuous, d=11) 上，SID / SHD / F1 为 Plurality + Bayes Est.: 99 / 27 / 0.205，对比 Plurality + Rank: 99 / 26 / 0.167，变化 F1 +0.038。

## 概要

现有因果发现集成方法多为启发式聚合——例如无加权多数投票或基于排名的距离聚合——缺乏理论保证，无法回答“需要多少专家”、“专家应具备何种能力与多样性”等关键设计问题。本文的核心洞察是：将因果图结构分解为边级子结构（特征），在每个特征上引入基于贝叶斯投票规则的加权聚合机制，并通过最优传输从投票配置中学习专家能力参数，从而为高维因果图的可识别聚合提供理论收敛保证和可导优化。

方法层面，本文提出 **Bayes Est.**（基于最优传输能力估计的特征级贝叶斯投票聚合）。其关键改进包括：将聚合规则从等权多数投票替换为对数似然加权的贝叶斯投票（权重和偏置由专家能力矩阵与先验决定）；引入基于最优传输距离的最小 Kantorovich 估计量，从投票样本中联合估计先验和能力转移矩阵；以及将聚合粒度从图级别下推至边级三状态空间（$v_i \to v_j$, $v_i \leftarrow v_j$, no edge），使参数空间从超指数规模降至可处理规模。

理论保证方面，Theorem 1 给出：在专家独立且具有信息量的条件下，贝叶斯投票的错误概率随专家数量 $n$ 和平均 KL 散度指数衰减。Theorem 2 进一步表明，至少 $2m-1$ 名信息量专家可保证参数可识别性，且在此条件下最小 Kantorovich 估计量一致收敛。

实验覆盖连续和离散数据类型，包括半合成基准（GP-ER、MLP-SF）和多个真实世界系统（Sachs、Sangiovese、Child 等）。两阶段集成（算法内聚合 + Bayes Est. 最终聚合）在主要指标上一致优于启发式基线：在 GP-ER（d=20）上，Plurality + Bayes Est. 相较 Plurality + Rank 实现 SID 降低 5、SHD 降低 3、F1 提升 0.065；在 MLP-SF（d=40）上，Rank + Bayes Est. 实现 SID 降低 18、SHD 降低 2、F1 提升 0.014。消融实验表明，Bayes Est. 在专家数量增加后逼近 Bayes True 性能，且在不同专家能力水平下显著超越 Plurality 投票，验证了噪声贝叶斯投票的鲁棒性。

当前框架的主要局限包括：状态空间仅建模有向边与无边，无法处理潜在混淆因子；至少需要 5 名信息量专家才能保证 $m=3$ 状态的可识别性；参数估计依赖大量投票样本且计算成本随专家数和状态空间快速增长。这些方向为后续工作提供了明确的改进空间。



### 因果发现的核心挑战

从观测数据中恢复变量间的因果关系是科学发现与决策制定的基础问题。形式上，数据生成过程通常被建模为结构因果模型（SCM）：

$$X_i := f_i(X_{pa_i}, U_i), \quad i \in [d]$$

其中变量 $X_i$ 由其父节点 $X_{pa_i}$ 和独立噪声 $U_i$ 通过函数 $f_i$ 生成。因果发现的目标是仅从观测样本中推断出编码这些函数依赖关系的有向无环图（DAG）。

然而，现实世界数据往往违反标准因果发现算法所依赖的假设——函数形式未知、噪声分布非高斯、存在非线性依赖，甚至可能包含未观测的混淆因子。单一算法在特定假设下表现良好，但在假设不成立时性能急剧退化。这种**假设脆弱性**构成了因果发现从理论走向应用的核心瓶颈。

### 集成方法的现状与理论真空

一个自然的应对策略是集成多个因果发现算法的输出，以期聚合不同假设空间下的互补信息。现有集成方法大致分为两类：

- **启发式投票聚合**：如 Plurality voting（无加权多数投票），对所有专家赋予相等权重，缺乏对专家能力差异的建模。
- **基于距离的聚合**：如 Rank-based ensemble（Malmi et al., 2015），通过最小化图结构间的某种距离度量来融合输出，但距离函数的选择缺乏统计基础。

这些方法的共同缺陷在于**缺乏理论保证**：它们无法回答以下关键设计问题——需要多少专家？专家的能力和多样性应如何配置？聚合规则在什么条件下能恢复真实因果图？当聚合器本身是一个黑箱启发式时，集成性能的上限和收敛性质完全未知。

### 本文的动机与核心思路

本文旨在填补这一理论真空。核心洞察在于：**将因果图集成形式化为一个贝叶斯投票问题**。具体而言：

1. **图结构分解**：将高维 DAG 分解为边级子结构（每个节点对上的三种互斥状态：$v_i \to v_j$、$v_i \leftarrow v_j$、无边），使状态空间从指数级降至常数级 $m=3$。
2. **贝叶斯加权投票**：推导误差最小化意义下的最优加权投票规则，权重由专家的对数似然比决定，而非均匀赋值。
3. **最优传输参数估计**：通过最小 Kantorovich 估计量从投票样本中联合学习专家的能力转移矩阵 $T_i(\omega)$ 和先验分布 $\pi(\omega)$，为聚合提供可导优化路径。

这一框架带来了两个关键理论成果：
- **收敛保证**：在专家独立且具有信息量的条件下，贝叶斯投票的错误概率随专家数量 $n$ 和平均 KL 散度指数衰减（Theorem 1）。
- **可识别性条件**：至少 $2m-1$ 名信息量专家可保证参数可识别性，且最小 Kantorovich 估计量在此条件下一致收敛（Theorem 2）。

与现有启发式集成方法相比，本框架首次为因果发现的集成聚合提供了从投票规则设计到参数估计的完整理论支撑，使得专家选择、能力评估和聚合优化成为可论证的统计推断过程，而非经验试错。



## 核心方法与创新机理

现有因果发现集成方法大多依赖启发式规则（如多数投票或基于排名的距离聚合），缺乏理论保证，无法回答“需要多少专家、专家应具备何种能力与多样性才能获得最优聚合结果”这一根本问题。本文的核心创新在于将因果图集成形式化为一个**有理论保证的贝叶斯投票问题**，并通过三个关键的“changed slots”实现了从启发式到原理性的跨越。

**1. 聚合投票规则：从等权多数到贝叶斯加权**

基线方法（如 Plurality voting）对所有专家赋予相等权重，忽略了专家能力的异质性。本文引入基于对数似然的贝叶斯加权投票规则：对每个候选图结构 $\mathbf{G}$，其加权投票分数为

$$S_{n,w_{\mathbf{G}}}(\widetilde{G}) = \sum_{i=1}^{n} w_{i,\mathbf{G}} \mathbf{1}[\widetilde{G}_i = \mathbf{G}] + b_{\mathbf{G}},$$

其中权重和偏置由专家能力矩阵与先验分布显式给出：

$$w_{i,\mathbf{G}} = \log p_{i,\mathbf{G}} - \log q_{i,\widetilde{G}_i|\mathbf{G}}, \quad b_{\mathbf{G}} = \sum_{i=1}^{n} \log q_{i,\widetilde{G}_i|\mathbf{G}} + \log \pi_{\mathbf{G}}.$$

这一规则的理论优势由 **Theorem 1** 保证：在专家独立且具有信息量的条件下，贝叶斯投票的错误概率随专家数量 $n$ 和平均 KL 散度指数衰减，其正确决策概率下界为

$$1 - \sum_{j \geq 2} \exp\left( - n \cdot \overline{\mathrm{KL}}_{1,j}^2 / 2\tau^2 \right).$$

这为集成设计提供了明确的指导——增加信息量专家可指数级提升聚合可靠性，而等权投票无法提供此类保证。

**2. 专家能力估计：从无参数到最优传输驱动的最小 Kantorovich 估计**

基线方法不估计专家能力，隐式假设所有专家等可信。本文提出基于最优传输距离的最小 Kantorovich 估计量，从投票样本中联合学习每个特征上的先验分布 $\pi(\omega)$ 和专家能力转移矩阵 $T_i(\omega)$：

$$\widehat{\theta}_N(\omega) = \underset{\theta(\omega) \in \Theta(\omega)}{\arg\min} \, W_c\Big[\mathbb{P}_N(X(\omega) \mid \mathcal{D}); \mathbb{P}_\theta(X(\omega) \mid \mathcal{D})\Big].$$

**Theorem 2** 进一步确立了可识别性条件：至少 $(2m-1)$ 名信息量专家可保证参数可识别（对 $m=3$ 的边级状态空间即至少 5 名），且在此条件下估计量一致收敛。为解除排列歧义，实际估计中引入对角优势约束，使学习到的能力矩阵具有稳定的结构解释。

**3. 聚合粒度：从图级别到特征级分解**

基线方法在图级别或启发式边级别聚合，面临状态空间随节点数组合爆炸的问题（$m^{\binom{d}{2}}$）。本文的关键洞察是将图结构分解为边级子结构（特征），每个特征 $\omega = (v_i, v_j)$ 拥有独立的 3 状态空间（$v_i \rightarrow v_j$、$v_i \leftarrow v_j$、无边），在此粒度上独立进行贝叶斯投票聚合。这使复杂度从指数级降为 $\binom{d}{2}$ 个 $3 \times 3$ 能力矩阵的估计问题，使得高维因果图的可识别聚合在计算上可行。

三个 changed slots 形成闭环：特征分解使状态空间可控，最优传输估计从数据中学习专家能力，贝叶斯加权投票利用估计的能力参数实现有理论收敛保证的最优聚合。这一框架首次将因果发现集成从启发式工程提升为有统计保证的推理过程。



本方法提出一种基于贝叶斯投票的因果图结构集成框架，其核心流水线由四个功能模块串联构成，将来自多个因果发现专家的输出图聚合为单一共识结构（Figure 1 示意整体流程，但此处不嵌入图像）。整个框架的输入是一组专家因果图 $\{\widetilde{G}_i\}_{i=1}^n$，输出为集体决策图 $\widehat{G}$。

### 模块关系与数据流

**1. 特征分解模块**  
完整 DAG 首先被分解为边级子结构（特征 $\omega$），每个特征对应一对节点 $(v_i, v_j)$ 并拥有独立的三状态空间 $S(v_i, v_j) = \{1: v_i \to v_j,\; 2: v_i \leftarrow v_j,\; 3: \text{无边}\}$。这一分解将高维图空间 $\mathcal{G}$ 表示为所有特征状态空间的笛卡尔积 $\mathcal{G} := \prod_{\omega \in \Omega} S(\omega)$，使得后续聚合可在每个特征上独立进行，显著降低计算复杂度——原本需处理大小为 $|\mathcal{G}|$ 的全局状态空间，而特征级贝叶斯投票仅需处理 $\binom{d}{2}$ 个 $3 \times 3$ 的能力矩阵。

**2. 能力参数估计模块**  
该模块从 $N$ 个投票配置样本中学习每个特征 $\omega$ 上的先验分布 $\pi(\omega)$ 和专家能力转移矩阵 $T_i(\omega)$。估计采用最小 Kantorovich 估计量：

$$\widehat{\theta}_N(\omega) = \underset{\theta(\omega) \in \Theta(\omega)}{\arg\min}\; W_c\Big[\mathbb{P}_N(X(\omega) \mid \mathcal{D}); \mathbb{P}_\theta(X(\omega) \mid \mathcal{D})\Big]$$

其中 $W_c$ 为最优传输距离（Eq. (2)），$\mathbb{P}_N$ 为经验投票分布，$\mathbb{P}_\theta$ 为由参数 $\theta = (\pi, \{T_i\}_{i=1}^n)$ 诱导的模型分布。为保证参数可识别性，Theorem 2 要求至少 $2m-1 = 5$ 名信息量专家，并通过对角优势约束解除转移矩阵的行排列歧义。实际优化中，该目标被松弛为结合交叉熵与 JS 散度的可微形式（Appendix C, Eq. (11)），并利用 Cat-Concrete 重参数化（Eq. (8)）实现离散状态的梯度估计。

**3. 贝叶斯投票聚合模块**  
对每个特征 $\omega$，利用估计的参数计算贝叶斯加权分数。对于候选状态 $\mathbf{G} \in S(\omega)$，总分为：

$$S_{n,w_{\mathbf{G}}}(\widetilde{G}) = \sum_{i=1}^{n} w_{i,\mathbf{G}} \mathbf{1}[\widetilde{G}_i = \mathbf{G}] + b_{\mathbf{G}}$$

其中权重和偏置由能力矩阵与先验决定：

$$w_{i,\mathbf{G}} = \log p_{i,\mathbf{G}} - \log q_{i,\widetilde{G}_i|\mathbf{G}}, \quad b_{\mathbf{G}} = \sum_{i=1}^{n} \log q_{i,\widetilde{G}_i|\mathbf{G}} + \log \pi_{\mathbf{G}}$$

选择得分最高的状态作为该特征的集体决策。Theorem 1 保证，在专家独立且具有信息量的条件下，正确决策的概率至少为 $1 - \sum_{j \geq 2} \exp\big(- n \cdot \overline{\mathrm{KL}}_{1,j}^2 / 2\tau^2 \big)$，即错误概率随专家数量 $n$ 和平均 KL 散度指数衰减。

**4. 图重建模块**  
将所有特征 $\omega \in \Omega$ 的集体决策状态按节点对拼接，恢复为完整的因果图结构 $\widehat{G} \in \mathcal{G}$。

### 两阶段集成策略

在实际部署中，论文推荐两阶段集成流程：首先在算法内部通过 Plurality 或 Rank 方法聚合同一算法的多次运行结果，得到各算法的“平均”图；再以这些平均图作为专家输入，应用 Bayes Est. 进行跨算法聚合。Table 1 显示，Rank + Bayes Est. 组合在 GP-ER（d=20）上取得 SID 199、SHD 35、F1 0.500，在 MLP-SF（d=40）上取得 SID 169、SHD 18、F1 0.865，均优于纯启发式组合。



### 3.1 贝叶斯投票规则与最优加权

框架的核心聚合机制是一类加权线性投票规则。对于候选图 $\mathbf{G}$，其总得分由各专家投票的加权和加上一个偏置项构成：

$$S_{n, w_{\mathbf{G}}}(\widetilde{G}) = \sum_{i=1}^{n} w_{i, \mathbf{G}} \mathbf{1}[\widetilde{G}_i = \mathbf{G}] + b_{\mathbf{G}}$$

其中 $\widetilde{G}_i$ 为第 $i$ 个专家输出的图结构，$\mathbf{1}[\cdot]$ 为指示函数。该规则的关键在于权重 $w_{i,\mathbf{G}}$ 和偏置 $b_{\mathbf{G}}$ 的选择。从最小化错误概率的角度出发，推导得到贝叶斯最优权重与偏置：

$$w_{i,\mathbf{G}} = \log p_{i,\mathbf{G}} - \log q_{i,\widetilde{G}_i|\mathbf{G}}, \quad b_{\mathbf{G}} = \sum_{i=1}^{n} \log q_{i,\widetilde{G}_i|\mathbf{G}} + \log \pi_{\mathbf{G}}$$

这里 $p_{i,\mathbf{G}}$ 是专家 $i$ 在真实图为 $\mathbf{G}$ 时正确投票的概率，$q_{i,\widetilde{G}_i|\mathbf{G}}$ 是错误投票的概率，$\pi_{\mathbf{G}}$ 是图 $\mathbf{G}$ 的先验概率。权重由专家的“正确-错误”对数似然差决定：能力越强的专家获得越高的正权重，而偏置项则汇总了所有专家的错误概率和先验信息。

**理论保证**：在专家独立且具有信息量（即 $\mathrm{KL}(p_{i,\mathbf{G}} \| q_{i,\cdot|\mathbf{G}}) > 0$）的条件下，贝叶斯投票规则正确恢复真实图的概率下界为：

$$1 - \sum_{j \geq 2} \exp\left( - n \cdot \overline{\mathrm{KL}}_{1,j}^2 \big/ 2\tau^2 \right)$$

其中 $\overline{\mathrm{KL}}_{1,j}$ 是真实图与第 $j$ 个候选图之间的平均 KL 散度，$\tau$ 为有界对数似然比的上界。该下界表明，错误概率随专家数量 $n$ 和平均 KL 散度指数衰减——专家越多、能力越强，聚合结果越可靠。

### 3.2 特征分解与边级聚合

直接在整个图空间上进行贝叶斯投票面临状态空间组合爆炸的问题（$m^{d^2}$ 量级）。为此，框架将图结构分解为边级子结构（特征），每个特征 $\omega = (v_i, v_j)$ 拥有独立的 $m=3$ 状态空间：

$$S(v_i, v_j) = \{1: v_i \rightarrow v_j,\; 2: v_i \leftarrow v_j,\; 3: \text{无边}\}$$

完整图空间因此被重新定义为所有特征状态空间的笛卡尔积：

$$\mathcal{G} := \prod_{\omega \in \Omega} S(\omega)$$

这一分解将聚合复杂度从指数级降为 $\binom{d}{2}$ 个独立的 $3 \times 3$ 转移矩阵估计问题，使得框架可扩展到数十个节点的因果图。每个特征上的贝叶斯投票独立进行，最终将所有特征的集体决策拼接为完整的因果图结构。

### 4.1 噪声贝叶斯投票的鲁棒性

实际应用中，专家能力参数 $\theta(\omega) = \{\pi(\omega), T_i(\omega)\}$ 需要从有限投票样本中估计，这引入了估计误差。命题 1 给出了噪声贝叶斯投票的鲁棒性保证：当估计参数的误差被控制在一定范围内时，对于特征 $\omega$，集体决策正确的概率下界为：

$$1 - \sum_{j \geq 2} \exp\left[ - \Theta\left( n \cdot \Delta\overline{\mathrm{KL}}_{1,j}^2(\omega) \big/ 2\widetilde{\tau}^2 \right) \right]$$

其中 $\Delta\overline{\mathrm{KL}}$ 反映了估计误差对有效 KL 散度的折扣。这表明，只要估计质量足够好，噪声贝叶斯投票仍能保持指数级的正确率衰减。

### 4.2 基于最优传输的参数估计

参数估计的核心是最小 Kantorovich 估计量。对于每个特征 $\omega$，从 $N$ 个投票样本中构建经验分布 $\mathbb{P}_N(X(\omega) \mid \mathcal{D})$，然后通过最小化最优传输距离来估计参数：

$$\widehat{\theta}_N(\omega) = \underset{\theta(\omega) \in \Theta(\omega)}{\arg\min}\; W_c\Big[\mathbb{P}_N(X(\omega) \mid \mathcal{D}); \mathbb{P}_\theta(X(\omega) \mid \mathcal{D})\Big]$$

其中 $W_c(\alpha, \beta) := \min_{P \in U(a,b)} \langle C, P \rangle$ 为 Kantorovich 形式的最优传输距离，$C$ 为代价矩阵，$U(a,b)$ 为边缘分布约束下的联合分布集合。该估计量直接度量经验投票分布与参数化模型分布之间的结构差异，而非逐点的似然匹配。

**可识别性条件**：Theorem 2 指出，当至少存在 $(2m-1)$ 名信息量专家时（对 $m=3$ 即至少 5 名），参数可被识别至行排列等价。为解除排列歧义，实际估计中施加对角优势约束，限制 $T_i(\omega)$ 的搜索空间为对角占优矩阵，从而获得稳定的解结构。

**实用优化目标**：为进行可微优化，实际训练中使用松弛的 OT 目标，结合交叉熵和 JS 散度：

$$\min_{\theta} \min_{\phi} \mathbb{E}_{\boldsymbol{x} \sim \mathbb{P}_N, \boldsymbol{\tilde{y}} \sim \phi(\boldsymbol{x})} \left\{ \operatorname{CE}(\boldsymbol{x}; e_{\boldsymbol{\tilde{y}}}; \boldsymbol{T}) + \operatorname{CE}(\boldsymbol{x}; \boldsymbol{\pi}; \boldsymbol{T}) + \lambda \cdot \operatorname{JS}[\phi(\boldsymbol{x}) \| \boldsymbol{\pi}] \right\}$$

其中 $\phi(\boldsymbol{x})$ 是推前耦合的变分近似，$\operatorname{CE}$ 为交叉熵损失，$\operatorname{JS}$ 为 Jensen-Shannon 散度正则项。离散采样通过 Cat-Concrete（Gumbel-Softmax）重参数化实现：

$$\mathrm{Cat-Concrete}(p) = \left[ \frac{\exp\{(\log p^{(j)} + G^{(j)})/\tau\}}{\sum_{k=1}^{m} \exp\{(\log p^{(k)} + G^{(k)})/\tau\}} \right]_{j \in [m]}$$

其中 $G^{(j)}$ 为 Gumbel 噪声，$\tau$ 为温度参数，控制离散化程度。



## 实验与关键发现

### 实验设置概览

实验在两类数据上验证 Bayes Est. 的有效性：(1) 合成模拟，用于精确控制专家能力并检验理论预测；(2) 真实世界与半合成基准，覆盖连续型（Sachs、Artic、Sangiovese、GP-ER、MLP-SF）和离散型（Child、Insurance、Asia、Earthquake）数据集。基础专家包括 PC、GES、LiNGAM、NOTEARS、DAG-GNN 等经典因果发现算法；对于输出 CPDAG 的算法，无向边被均分概率分配给两个方向，以公平对待方向信息。由于 LLM 基础专家在当前基准上性能不佳，被排除在实验之外。

实验采用两阶段集成策略：第一阶段在同类算法内部进行聚合（Plurality 或 Rank），第二阶段在算法间进行聚合（Rank、Plurality 或 Bayes Est.）。最终评估指标包括结构干预距离（SID）、结构汉明距离（SHD）和 F1 分数。

### 合成模拟：验证理论鲁棒性

Figure 1（d=50，50^n 投票配置）展示了 Bayes Est. 在不同专家能力水平下的核心行为。关键结论如下：

![[assets/figures/papers/iclr26_0010_WtbPaWO8lH_Causal_Discovery_in_the_Wild_A_Voting-Theoretic/figures/001_Figure_1.jpg]]
*Figure 1: Simulations for graph size d = 50 on 5 0 ^ { n } voting profiles*

- **Bayes Est. 随专家数量 n 增大而逼近 Bayes True（Oracle 贝叶斯规则）**，验证了 Theorem 1 的指数衰减保证：当专家独立且具有信息量时，贝叶斯投票的错误概率以 $\exp(-n \cdot \overline{\mathrm{KL}}_{1,j}^2 / 2\tau^2)$ 的速度衰减。
- **Bayes Est. 在所有能力水平下显著优于 Plurality 投票（无加权多数投票）**，且方差更低。这直接体现了加权机制的价值：Plurality 将各专家等权对待，而 Bayes Est. 通过估计的能力矩阵对更可靠的专家赋予更高权重。
- 当专家能力极低（接近随机猜测）时，Bayes Est. 仍保持稳健，退化幅度远小于 Plurality，验证了 Proposition 1 对“噪声贝叶斯投票”的鲁棒性保证。

Figures 12–38 进一步展示了在不同图大小（d=10–50）和投票样本数（p=10^n、30^n、50^n）下的模拟结果。Bayes Est. 在所有这些配置下均表现出一致的优越性和较低的方差，表明参数估计模块（最小 Kantorovich 估计量）在不同数据规模下均能有效恢复专家能力矩阵。

### 真实世界与半合成基准：两阶段集成性能

Table 1 汇总了两阶段集成的最终聚合图结果。核心发现：

![[assets/figures/papers/iclr26_0010_WtbPaWO8lH_Causal_Discovery_in_the_Wild_A_Voting-Theoretic/figures/039_Table_1.jpg]]
*Table 1: Results of the final aggregated graphs from two-phase ensembling*

- **Rank + Bayes Est. 是最有效且最稳定的组合**。在连续型数据集上表现尤为突出：GP-ER（d=20）上 SID 从 Plurality + Rank 的 204 降至 199，SHD 从 38 降至 35，F1 从 0.435 提升至 0.500；MLP-SF（d=40）上 SID 从 187 降至 169，SHD 从 20 降至 18，F1 从 0.851 提升至 0.865。
- **Bayes Est. 作为第二阶段聚合器普遍优于 Rank 和 Plurality**。在 Sachs（d=11）上，Plurality + Bayes Est. 的 F1 达到 0.205，而 Plurality + Rank 仅为 0.167（SID 和 SHD 持平）。这表明即使第一阶段聚合质量一般，Bayes Est. 的能力加权机制仍能提取额外信号。
- 离散数据集（Child、Insurance）上的改进幅度相对较小，但 Bayes Est. 始终不劣于其他集成方法，且方差更低。

Figures 2–11 提供了各数据集上集成方法与单专家性能的详细对比。值得注意的失败模式：

![[assets/figures/papers/iclr26_0010_WtbPaWO8lH_Causal_Discovery_in_the_Wild_A_Voting-Theoretic/figures/018_Figure_6.jpg]]
*Figure 6: Experiments on GP-ER model (continuous, d = 20)*

![[assets/figures/papers/iclr26_0010_WtbPaWO8lH_Causal_Discovery_in_the_Wild_A_Voting-Theoretic/figures/022_Figure_7.jpg]]
*Figure 7: Experiments on MLP-SF model (continuous, d = 40)*

![[assets/figures/papers/iclr26_0010_WtbPaWO8lH_Causal_Discovery_in_the_Wild_A_Voting-Theoretic/figures/006_Figure_3.jpg]]
*Figure 3: Experiments on Sachs dataset (continuous, d = 11)*

![[assets/figures/papers/iclr26_0010_WtbPaWO8lH_Causal_Discovery_in_the_Wild_A_Voting-Theoretic/figures/025_Figure_8.jpg]]
*Figure 8: Experiments on Child dataset (discrete, d = 20)*

- **Artic 数据集（Figure 4）**：所有专家和集成方法的 SID 均达到理论上限 $d(d-1)=132$，表明该数据集对现有因果发现算法构成极端挑战。此时集成方法也无法超越最佳单专家，提示当所有基础专家系统性失效时，投票聚合无法产生有意义的改进。
- **Sachs 数据集（Figure 3）**：SID 和 SHD 的绝对数值较高，反映了该生物学数据中因果结构的高度不确定性。Bayes Est. 在 F1 上的提升主要来自对边方向的更准确判断，而非减少错误边数。

### 消融分析：专家数量与能力的影响

Figure 1 的消融维度直接揭示了专家数量的作用：当 n 从 5 增加到 50 时，Bayes Est. 的 SHD 单调下降并收敛至 Bayes True，而 Plurality 的改进趋于平缓。这与 Theorem 1 的指数衰减界一致——更多专家意味着更大的平均 KL 散度累积，从而指数级降低错误概率。

另一方面，当专家能力矩阵的对角优势减弱（即专家更不可靠）时，Bayes Est. 相对于 Plurality 的优势更加明显。这是因为 Plurality 在低能力专家下容易被噪声投票淹没，而 Bayes Est. 通过对数似然加权（$w_{i,\mathbf{G}} = \log p_{i,\mathbf{G}} - \log q_{i,\widetilde{G}_i|\mathbf{G}}$）有效压制了不可靠专家的影响。

### 局限性与开放问题

实验揭示了若干实际限制：

1. **专家数量需求**：为保证 m=3 状态的可识别性，至少需要 $2m-1=5$ 名信息量专家（Theorem 2）。当可用算法数量不足或部分专家性能极差时，参数估计可能退化。
2. **CPDAG 方向模糊**：对输出无向边的算法，均分概率引入额外的方向不确定性，在边方向密集的数据集上可能削弱 Bayes Est. 的加权优势。
3. **计算成本**：参数估计依赖大量投票样本（模拟中使用 p=50），且计算复杂度随专家数和状态空间超指数增长。实际部署中需要在样本效率与精度间权衡。
4. **状态空间限制**：当前仅建模有向边和无边（m=3），无法处理潜在混淆因子。这限制了框架在存在隐含共因场景下的适用性。



## 定位与知识库关联

### 在因果发现集成方法中的定位

因果发现集成方法旨在将多个因果图预测融合为单一共识结构，以提升鲁棒性和准确性。现有方法大致可分为三类：基于图距离的优化聚合（如将集成问题形式化为寻找与所有专家图距离之和最小的中位图）、基于排名的聚合（如 Malmi et al., 2015 将边置信度排序后阈值截断），以及基于投票的边级加权聚合。然而，这些方法多为启发式设计，缺乏理论保证来指导集成设计——例如，应选择多少专家、专家的能力和多样性如何影响最终聚合性能，均无系统性回答。

本文提出的 **Bayes Est.** 框架填补了这一理论空白。其核心推进在于：

1. **从启发式投票到贝叶斯加权投票**：Plurality voting 等基线方法对所有专家等权处理，相当于假设专家能力均匀且独立于真实图结构。Bayes Est. 则通过贝叶斯决策论推导出最优权重 $w_{i,\mathbf{G}} = \log p_{i,\mathbf{G}} - \log q_{i,\widetilde{G}_i|\mathbf{G}}$ 和偏置 $b_{\mathbf{G}}$（式 (4)），权重由专家能力转移矩阵 $T_i$ 和先验 $\pi$ 显式决定。这一规则在专家独立且具有信息量的条件下，错误概率随专家数量 $n$ 和平均 KL 散度指数衰减（Theorem 1），为集成规模设计提供了定量指导。

2. **从图级聚合到特征级可识别聚合**：直接在图空间上应用贝叶斯投票面临状态空间组合爆炸（$m^{\binom{d}{l}}$ 量级）和参数不可识别问题。Bayes Est. 将图分解为边级子结构（$l=2, m=3$：$v_i \to v_j$, $v_i \leftarrow v_j$, 无边），对每个特征独立进行贝叶斯投票。这一分解使参数空间降至 $\binom{d}{2}$ 个 $3\times 3$ 矩阵，且 Theorem 2 证明至少 $2m-1=5$ 名信息量专家即可保证参数可识别性。

3. **从无能力估计到基于最优传输的联合估计**：基线方法不估计专家能力，Bayes Est. 则通过最小 Kantorovich 估计量（式 (7)）从投票样本中联合学习先验和能力转移矩阵。最优传输距离的引入使估计问题可导优化，且在大样本下具有一致性保证（Theorem 2）。

### 适用边界

Bayes Est. 的有效性依赖于以下关键假设：

- **专家独立性**：Theorem 1 和 Theorem 2 均假设专家在给定真实图的条件下独立投票。若专家间存在系统性相关（如使用相似算法或相同数据划分），KL 散度下界和可识别性条件可能被削弱。
- **信息量专家充足**：需要至少 5 名“信息量”专家（即 $T_i$ 非均匀且对角占优）以满足参数可识别性。若可用的可靠因果发现算法不足 5 个，框架的估计质量会退化。
- **状态空间限于无混淆因子的有向边**：当前 $m=3$ 的状态空间仅建模 $v_i \to v_j$、$v_i \leftarrow v_j$ 和无边三种关系，不包含潜在混淆因子（如双向边表示隐共因）。因此，框架无法处理存在未观测共因的场景。
- **CPDAG 输出的方向模糊性**：对于输出 CPDAG 的算法（如 PC、GES），无向边被均分概率分配给两个方向。这一处理引入了额外的方向不确定性，可能在高维稀疏图中累积误差。

### 局限与开放问题

**已识别的局限**：

1. **专家数量与多样性的硬约束**：$m=3$ 时至少需要 5 名信息量专家，这限制了可集成算法的数量和类型。当扩展到 $m \geq 4$（如增加双向边状态建模混淆因子）时，需要至少 7 名可靠专家，进一步加剧了算法筛选的困难。

2. **计算成本随规模超线性增长**：参数估计依赖大量投票样本（实验中 $p=50$），且计算成本随专家数 $n$ 和状态空间 $m$ 呈超指数增长。实用算法（Appendix C）通过 Gumbel-Softmax 重参数化和 JS 散度正则化（式 (11)）进行松弛优化，但大规模图（$d>50$）上的可扩展性仍待验证。

3. **LLM 专家的性能瓶颈**：基于大语言模型的因果发现专家在当前基准上性能低下，未被纳入实验。框架的理论保证假设专家“信息量”，若专家能力过低（接近随机猜测），贝叶斯投票退化为噪声聚合，收敛速率将大幅下降。

4. **真实世界验证的局限性**：实验覆盖的真实数据集（Sachs、Sangiovese、Child 等）节点数较小（$d \leq 27$），且依赖已知的基准因果图。在更大规模、无金标准真实图的野外场景中，Bayes Est. 的实际增益尚需进一步验证。

**开放问题**：

1. **状态空间扩展与混淆因子建模**：如何将状态空间扩展至 $m \geq 4$（如增加双向边表示隐共因），并在更高维度下保持参数可识别性和高效估计？这涉及可识别性条件的重新推导（Theorem 2 需推广）和优化算法的重新设计。

2. **自适应专家选择与集成规模优化**：能否设计自适应机制，根据数据特征和可用算法池动态选择最优专家数量 $n$ 和估计样本数 $p$，以平衡计算效率与聚合精度？当前框架假设专家集合固定，缺乏在线筛选能力。

3. **更丰富的特征层级**：当前仅使用边级（$l=2$）子结构。是否可引入三元组（$l=3$）或更高阶子结构以捕获条件独立性信息？这需要解决状态空间指数增长和特征间一致性约束的问题。

4. **循环图与非 DAG 结构的扩展**：框架基于 DAG 假设设计状态空间。如何扩展到含环的因果图（如反馈系统）或更一般的图结构（如部分有向图），是面向真实复杂系统应用的重要方向。

5. **专家相关性的建模与补偿**：当前独立性假设在算法同质化（如均基于 score-based 方法）时可能不成立。是否可引入专家相关性的显式建模（如 copula 或层次先验），以在专家非独立时仍保持聚合的鲁棒性？



## 原文 PDF

![[paperPDFs/ICLR_2026/Causal_Discovery_in_the_Wild_A_Voting_Theoretic_Ensemble_Approach.pdf]]
