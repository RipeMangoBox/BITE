---
title: "Causal Structure Learning in Hawkes Processes with Complex Latent Confounder Networks"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Causal_Structure_Learning_in_Hawkes_Processes_with_Complex_Latent_Confounder_Networks.pdf
project_link: null
code_link: null
openreview_forum_id: mA78uXqcnl
aliases:
- TPIDA
- CSLHPCLCN
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "将连续时间Hawkes过程离散化为线性自回归模型（linear autoregressive representation），从而利用交叉协方差矩阵的秩约束（rank constraints）来识别潜在混淆变量。"
primary_logic: "在时间间隔趋近于零时，多元Hawkes过程可表示为离散时间线性因果模型；潜在混淆变量会在观测变量的交叉协方差矩阵中产生特定的低秩特征（rank deficiency），通过检验这种秩亏损可识别其存在及因果影响。"
claims:
- "Theorem 4.1 证明了平稳多元Hawkes过程在时间间隔趋近于0时，可表示为线性自回归模型。"
- "Proposition 4.5 提供了识别影响两个观测子过程的潜在混淆变量的秩条件。"
- "Theorem 4.7 将可识别性扩展到包含观测和推断的潜在子过程之间的任意因果关系，通过引入观测代理变量。"
- "两阶段迭代算法（Algorithm 1）在合成数据和真实世界数据集上有效恢复了包含潜在混淆变量的因果结构。"
---

# Causal Structure Learning in Hawkes Processes with Complex Latent Confounder Networks

> [!tip] 核心洞察
> 在时间间隔趋近于零时，多元Hawkes过程可表示为离散时间线性因果模型；潜在混淆变量会在观测变量的交叉协方差矩阵中产生特定的低秩特征（rank deficiency），通过检验这种秩亏损可识别其存在及因果影响。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 复杂潜在混淆网络下的Hawkes过程因果结构学习 |
| 英文题名 | Causal Structure Learning in Hawkes Processes with Complex Latent Confounder Networks |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=mA78uXqcnl) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Two-Phase Iterative Discovery Algorithm |
| Dataset | Metropolitan cellular network sub-dataset (Alarm ids=0–3,7; device id=8), Larger synthetic causal graph (14 subprocesses, Fig. 9) |

> [!tip] 效果简介
> - Metropolitan cellular network sub-dataset (Alarm ids=0–3,7; device id=8) 上，F1-score 为 0.76，对比 SHP: 0.49, THP: 0.48, NPHC: 0.42, Hier.Rank: 0.00, RLCD: 0.39, LPCMCI: 0.43，变化 +0.27 vs. SHP。
> - Larger synthetic causal graph (14 subprocesses, Fig. 9) 上，F1-score (80k samples) 为 0.75，对比 N/A (only proposed method evaluated)，变化 N/A。

## 概要

### 问题背景

从连续时间事件序列中恢复因果结构是时序因果发现领域的核心挑战。多元Hawkes过程（Multivariate Hawkes Process, MHP）因其能自然刻画事件间的激励效应，被广泛用于建模金融交易、社交媒体传播、生物神经活动等场景。然而，现有基于Hawkes过程的因果发现方法——包括基于分箱计数的**SHP**（Qiao et al., 2023）、基于时间点过程的**THP**（Cai et al., 2022）、以及非参数矩匹配方法**NPHC**（Achab et al., 2018）——均隐含地假设所有子过程均可观测，即满足因果充分性（causal sufficiency）。

这一假设在现实场景中往往不成立：许多关键驱动因素无法被直接观测，形成**潜在混淆变量**（latent confounders），导致观测变量间出现伪相关，使传统方法失效。本文正是针对这一瓶颈，研究在存在复杂潜在混淆网络时，如何从多元Hawkes过程的观测事件序列中恢复因果结构。

### 核心思路

本文的核心洞察在于：**当时间离散化间隔趋近于零时，平稳多元Hawkes过程可精确表示为离散时间的线性自回归模型**（Theorem 4.1）。这一等价性将连续时间点过程的因果发现问题，转化为离散时间线性因果模型的结构学习问题，从而可以借助二阶统计量——特别是交叉协方差矩阵的秩约束——来识别因果关系和潜在混淆变量。

具体而言，潜在混淆变量会在观测变量的交叉协方差矩阵中产生特定的低秩特征（rank deficiency）。通过系统性地检验这种秩亏损，可以在无需事先知晓潜在变量存在与否及其数量的前提下，自动发现它们并推断其因果影响（Proposition 4.5, Theorem 4.7）。

### 方法定位

基于上述理论，本文提出**两阶段迭代发现算法**（Two-Phase Iterative Discovery Algorithm），其定位如下：

- **方法谱系**：属于基于约束的因果发现方法，利用协方差矩阵的秩条件作为统计检验准则。与基于独立同分布（i.i.d.）数据的秩方法如**Hier.Rank**（Huang et al., 2022）和**RLCD**（Dong et al., 2023）不同，本文方法专门针对连续时间事件序列设计，通过Hawkes过程的线性自回归表示将秩约束框架引入时序领域。与处理外生潜变量的时间序列方法**LPCMCI**（Gerhardus & Runge, 2020）相比，本文能处理更一般的潜在混淆结构，包括潜在变量之间的因果交互。

- **关键创新**：
  - **时间表示**：将连续时间Hawkes过程离散化为线性自回归模型，利用二阶统计量替代最大似然估计，避免了对完整似然函数的依赖。
  - **因果发现准则**：从Granger因果性或似然拟合转向基于交叉协方差矩阵的秩约束条件（Lemma 4.2, Proposition 4.3），为潜在混淆变量的识别提供了可检验的充要条件。
  - **潜在混淆处理**：通过两阶段迭代——Phase I 识别已发现子过程间的因果关系，Phase II 检测成对子过程间的秩亏损以发现新的潜在混淆子过程——实现了无需先验知识的自动发现。

- **理论保证**：在激励函数可分离假设（Assumption 1: $\phi_{ij}(s) = a_{ij} w(s)$）和对称无环路径条件（Definition 4.4）下，方法具有可识别性保证。

### 主要结果

**合成数据**：在多种因果图结构（Case 1–6，涵盖从无潜变量到复杂潜在混淆网络）上，所提方法一致优于所有基线方法。消融实验表明：
- 离散化间隔 $\Delta \leq 0.1$ 时性能稳定，$\Delta = 0.3$ 时急剧下降（Table 1），说明细粒度时间分辨率至关重要；
- 即便人为制造秩违反（identical edge coefficients），方法仍保持鲁棒性（Table 3）；
- 在仅5k样本的小样本场景下，仍保持有竞争力的F1分数（Table 4）；
- 在14个子过程的大规模因果图上，F1随样本量增加从0.58（30k）提升至0.75（80k）（Table 6），展现可扩展性。

**真实世界数据**：在城域蜂窝网络告警数据集上，将Alarm id=7手动排除并视为潜在混淆变量，所提方法以F1=0.76显著优于最佳基线SHP（F1=0.49），提升达27个百分点（Table 8），且成功将Alarm id=7识别为潜在子过程并恢复了其主要因果影响（Figure 5）。

### 局限与展望

方法依赖于激励函数可分离假设和对称路径条件，当这些理论条件被违反时，性能虽有下降但仍保持一定鲁棒性（Table 5）。两阶段迭代算法的计算复杂度较高，在极大规模网络上可能面临可扩展性瓶颈。未来工作可探索放松假设条件、开发更低复杂度的发现算法，以及在更多实际应用领域（如社交媒体传播、金融级联）中验证方法的因果洞察力。



### 连续时间事件序列中的因果发现

多元点过程（multivariate point processes）是建模连续时间事件序列的核心工具，广泛应用于社交网络信息传播、金融交易级联、神经脉冲序列和通信网络告警等领域。其中，**Hawkes过程**因其自激励（self-exciting）和互激励（mutually exciting）特性而备受青睐：任意子过程的事件发生会通过激励核函数（excitation kernel）提升其他子过程未来的事件发生率。形式化地，子过程 $i$ 在时刻 $t$ 的条件强度函数为：

$$\lambda_i(t) = \mu_i + \sum_{j=1}^{l} \int_{0}^{t} \phi_{ij}(t-s) dN_j(s)$$

其中 $\mu_i$ 为背景强度，$\phi_{ij}(\cdot)$ 为激励核函数，$N_j(s)$ 为子过程 $j$ 截至时刻 $s$ 的累积事件计数。

从因果推断的视角看，Hawkes过程天然刻画了子过程间的**有向因果影响**：若 $\phi_{ij}(\cdot) \neq 0$，则子过程 $j$ 的事件会因果性地影响子过程 $i$ 的未来事件发生率。因此，从观测到的多元事件序列中恢复这些因果依赖关系——即**因果结构学习**——成为理解复杂系统动态行为的关键。

### 现有方法的瓶颈：因果充分性假设

现有基于Hawkes过程的因果发现方法——包括基于最大似然估计的**SHP**（Qiao et al., 2023）、基于时间点过程的**THP**（Cai et al., 2022）和基于矩匹配的非参数方法**NPHC**（Achab et al., 2018）——虽然在特定场景下取得了进展，但普遍依赖一个根本性假设：**因果充分性（causal sufficiency）**，即所有相关的子过程均可被观测。

这一假设在实际应用中往往不成立。以蜂窝网络告警数据为例，观测到的告警事件（如设备故障告警）可能同时受到某些**未观测到的潜在混淆变量**（latent confounders）的影响——例如未被记录的系统级异常或外部环境因素。当这类潜在混淆变量存在时，直接应用现有方法将导致虚假因果边的推断或真实因果关系的遗漏，从而严重扭曲对系统因果结构的理解。

### 核心挑战与本文动机

在存在潜在混淆变量的Hawkes过程中恢复因果结构面临两个核心挑战：

1. **表示鸿沟**：Hawkes过程本质上是连续时间模型，而因果发现通常需要离散时间框架下的条件独立性或统计约束。如何在保留因果信息的前提下桥接这一鸿沟，是理论上的首要难题。

2. **可识别性缺失**：潜在混淆变量不可观测，其因果影响只能通过观测变量间的统计特征间接推断。在没有额外假设的情况下，潜在混淆变量的存在性和因果结构通常是不可识别的。

本文针对上述挑战，提出**首个无需预先知晓潜在子过程存在性或数量的原则性框架**，能够在连续时间事件序列中同时发现潜在混淆变量并恢复因果结构。核心思路是：将Hawkes过程在极限细粒度时间离散化下表示为线性自回归模型，从而将因果发现问题转化为观测变量交叉协方差矩阵的**秩约束（rank constraints）**检验——潜在混淆变量的存在会在特定协方差块中产生可检测的低秩特征（rank deficiency）。



## 核心方法与创新机理

本文的核心创新在于首次在连续时间事件序列的因果发现中，系统性地解决了**潜在混淆变量**（latent confounders）带来的可识别性挑战。传统基于Hawkes过程的方法（如SHP、THP、NPHC）均假设因果充分性，即所有子过程均可观测，无法处理未观测到的潜在混淆变量。本文通过三个紧密耦合的创新点突破了这一瓶颈。

### 创新一：连续时间到离散时间的线性因果表示

第一个关键创新是建立了Hawkes过程与离散时间线性自回归模型之间的等价性桥梁。**Theorem 4.1** 证明，当离散化时间间隔 $\Delta \to 0$ 时，平稳多元Hawkes过程严格等价于一个线性自回归模型：

$$N_i^{(n)} = \sum_{j=1}^{l} \sum_{k=1}^{n} \theta_{ij}^{(k)} N_j^{(n-k)} + \varepsilon_i^{(n)} + \theta_i^{(0)}$$

其中激励系数 $\theta_{ij}^{(k)} = \int_{(k-1)\Delta}^{k\Delta} \phi_{ij}(s) ds$ 编码了子过程间的因果影响强度。这一表示将连续时间点过程因果发现转化为离散时间线性因果模型的结构学习问题，使得可以利用二阶统计量（交叉协方差矩阵）而非复杂的似然函数进行因果推断。与基线方法依赖Granger因果性或似然拟合不同，本文方法在计算上更为高效，且为后续秩约束理论提供了数学基础。

### 创新二：基于秩约束的潜在混淆变量识别理论

第二个核心创新是利用交叉协方差矩阵的**秩亏损**（rank deficiency）特征来识别潜在混淆变量。核心理论链条如下：

- **Lemma 4.2** 建立了窗因果图中的d-分离与秩约束的等价关系：变量集 $\mathbf{A}_v$ 和 $\mathbf{B}_v$ 被 $\mathbf{C}_v$ d-分离，当且仅当 $\mathrm{rank}(\Sigma_{\mathbf{A}_v \cup \mathbf{C}_v, \mathbf{B}_v \cup \mathbf{C}_v}) = |\mathbf{C}_v|$。

- **Proposition 4.5** 进一步证明，当两个观测子过程 $O_1$ 和 $O_2$ 受到同一潜在混淆变量 $L_1$ 影响时，其交叉协方差矩阵满足 $\mathrm{rank}(\Sigma_{\{O_i^{(j)}\}, \mathbf{O}_v \setminus \{O_1^{(n)}, O_2^{(n)}\}}) = 2m + 1$。其中 $2m$ 对应自环引入的时滞变量，$+1$ 则对应潜在混淆变量的单一影响通道。

- **Theorem 4.7** 和 **Theorem 4.8** 将秩约束框架推广到包含观测代理变量的任意因果结构，允许在已推断的潜在子过程与观测子过程之间进一步发现因果关系。

这一理论的本质洞察在于：潜在混淆变量在观测变量的二阶统计量中留下了一个**低秩签名**——它通过单一的低维通道影响多个观测变量，使得交叉协方差矩阵的秩比完全观测情况下预期值更低。通过检测这种秩亏损，无需事先知道潜在变量的存在或数量即可自动发现它们。

### 创新三：两阶段迭代发现算法

基于上述理论，本文设计了**两阶段迭代发现算法**（Algorithm 1），交替执行因果结构恢复和潜在变量发现：

- **Phase I（因果关系识别）**：利用 Proposition 4.3 和 Theorem 4.7，通过最小化满足秩条件的变量集来识别每个子过程的父因果集。对于已推断的潜在子过程，使用其观测代理变量（Definition 4.6）参与秩检验。

- **Phase II（新潜在子过程发现）**：利用 Proposition 4.5 和 Theorem 4.8，在成对的观测或已推断子过程之间检测秩亏损，发现新的潜在混淆变量。

- **迭代终止**：重复两阶段直至无新发现，输出包含潜在子过程的汇总因果图。

该算法的关键优势在于**无需预设潜在变量的数量或结构**，能够自动发现任意复杂的潜在混淆网络（包括潜在变量之间的因果边，如 Figure 3d 所示）。实验表明，在合成数据上该方法显著优于所有基线方法（Table 8: F1=0.76 vs. SHP 0.49），在真实蜂窝网络数据上成功将 Alarm id=7 识别为潜在子过程（Figure 5）。

### 方法谱系与知识库定位

从方法谱系看，本文处于三个研究方向的交汇点：

1. **Hawkes过程因果发现**：超越 SHP（Qiao et al., 2023）、THP（Cai et al., 2022）、NPHC（Achab et al., 2018）等因果充分性假设方法，首次引入潜在变量可识别性理论。

2. **基于秩约束的因果发现**：借鉴 i.i.d. 数据下的潜变量方法如 Hier.Rank（Huang et al., 2022）和 RLCD（Dong et al., 2023），将其推广到时间序列/点过程场景，并处理自环和时滞结构。

3. **时间序列潜在变量因果发现**：区别于 LPCMCI（Gerhardus & Runge, 2020）等仅处理外生潜在变量的方法，本文框架允许潜在变量参与任意因果交互（包括潜在变量间的边、潜在变量作为中间节点等）。

本文的**changed slots** 可归纳为：
- **时间表示与建模**：从连续时间似然 → 离散时间线性自回归 + 二阶统计量
- **因果发现准则**：从 Granger因果/似然拟合 → 交叉协方差矩阵的秩约束
- **潜在混淆处理**：从无（假设因果充分性）→ 基于秩亏损的自动发现与迭代推断



![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_mA78uXqcnl/figures/004_Figure_1.jpg]]
*Figure 1: Illustration of multivariate Hawkes processes. (a) Point process representation with three subprocesses $N _ { 1 } , N _ { 2 } , N _ { 3 }$ , where the continuous timeline is partitioned into intervals of length ∆. (b) The corresponding summary causal graph, the central object of this paper, with causal relations $N _ { 1 } N _ { 2 } N _ { 3 }$ and self-loops on all nodes. (c) The window causal graph, showing the underlying time-lagged causal mechanism: each node denotes the count in one interval of length $\Delta$ modeled as a weighted sum of lagged parent nodes plus noise (Eq. 1). (d) A minimal example with a latent subprocess $L _ { 1 }$ confounding $O _ { 1 }$ and $O _ { 2 }$ , , highlighting the p...*

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_mA78uXqcnl/figures/008_Figure_2.jpg]]
*Figure 2: Examples of causal graphs with latent confounder subprocesses. (a) Summary graph where O _ { 1 } , O _ { 2 } , O _ { 3 } , O _ { 4 } are observed and L _ { 1 } is latent. (Unlike Figure 1d, O _ { 1 } , O _ { 2 } are shown without self-loops to simplify the derivation.) (b) Corresponding window causal graph among O _ { 1 } , O _ { 2 } , and L _ { 1 } with two effective lags. (c) More complex case where L _ { 1 } connects O _ { 1 } , O _ { 2 } via intermediate latent subprocesses L _ { 2 } , L _ { 3 } . All subprocesses have self-loops except L _ { 2 } and L _ { 3 } . (d) An even more intricate case, extending (c) with more complex intermediate latent subprocess paths and an additional edge O...*

### 问题设定与输入输出

本文解决的核心问题是在**部分可观测**的多元 Hawkes 过程中恢复因果结构。输入为多个子过程的事件序列 $\{N_i(t)\}_{i=1}^{l_o}$，其中仅 $l_o$ 个子过程可观测，其余 $l_h = l - l_o$ 个为潜在混淆子过程（latent confounder subprocesses）。输出为**汇总因果图**（summary causal graph）$\mathcal{G} = (\mathbf{N}_\mathcal{G}, \mathbf{E}_\mathcal{G})$，节点表示子过程（含推断出的潜在子过程），有向边 $N_j \to N_i$ 表示激励函数 $\phi_{ij}(s) \not\equiv 0$。

### 核心洞察：离散化线性自回归表示

整个框架的基石是 **Theorem 4.1**，它证明了当离散化时间间隔 $\Delta \to 0$ 时，平稳多元 Hawkes 过程可精确表示为线性自回归模型：

$$N_i^{(n)} = \sum_{j=1}^{l} \sum_{k=1}^{n} \theta_{ij}^{(k)} N_j^{(n-k)} + \varepsilon_i^{(n)} + \theta_i^{(0)}$$

其中 $N_i^{(n)} := N_i(n\Delta) - N_i((n-1)\Delta)$ 为第 $n$ 个时间窗内的事件计数，激励系数 $\theta_{ij}^{(k)} = \int_{(k-1)\Delta}^{k\Delta} \phi_{ij}(s) ds$。这一转换将连续时间点过程的因果发现问题转化为离散时间线性因果模型的结构学习问题，使得可以利用**交叉协方差矩阵的秩约束**来识别因果关系和潜在混淆变量。

### 理论支柱：秩约束条件体系

框架依赖一套递进的秩约束理论，从简单到复杂逐层构建可识别性保证：

1. **Lemma 4.2（d-分离与秩约束）**：在窗因果图（window causal graph）中，变量集 $\mathbf{A}_v$ 和 $\mathbf{B}_v$ 被 $\mathbf{C}_v$ d-分离当且仅当 $\mathrm{rank}(\Sigma_{\mathbf{A}_v \cup \mathbf{C}_v, \mathbf{B}_v \cup \mathbf{C}_v}) = |\mathbf{C}_v|$。这建立了图论条件与统计量之间的桥梁。

2. **Proposition 4.3（观测父因集识别）**：在因果充分性假设下，通过寻找满足秩条件的最小变量集来识别每个子过程的父因集。

3. **Proposition 4.5（潜在混淆变量发现）**：当两个观测子过程 $O_1, O_2$ 共享潜在混淆变量 $L_1$ 时，其交叉协方差矩阵呈现特定的秩亏损特征——秩为 $2m+1$（$m$ 为有效时滞），其中 $2m$ 来自自环的滞后变量，$1$ 对应潜在混淆变量。这一低秩特征是实现自动发现的关键。

4. **Theorem 4.7（含潜在变量的父因集识别）**：引入**观测代理变量**（observed surrogate）$\hat{D}_e(L_1)$ 替代推断出的潜在子过程，将 Proposition 4.3 推广到包含潜在变量的场景。

5. **Theorem 4.8（潜在混淆变量的递归发现）**：将 Proposition 4.5 推广至潜在混淆变量之间也存在因果或混淆关系的复杂场景（如 Figure 3d）。

### 两阶段迭代算法

基于上述理论，算法采用**交替迭代**的两阶段设计（Algorithm 1）：

**Phase I：因果关系识别**
- 对每个已发现子过程（含观测和已推断的潜在子过程），利用 Proposition 4.3 和 Theorem 4.7 识别其父因集。
- 通过检验交叉协方差矩阵的秩条件，确定最小父因集 $\mathbf{P}'_G$。

**Phase II：新潜在子过程发现**
- 对每对尚未被同一潜在变量解释的子过程，利用 Proposition 4.5 和 Theorem 4.8 检测是否存在秩亏损。
- 若满足秩条件，则创建新的潜在子过程节点，并将其加入已发现集合。

**迭代终止**：重复 Phase I 和 Phase II，直至无新潜在子过程被发现且所有因果关系稳定。由于子过程总数有限，算法必然终止。

### 关键假设与前提

框架的有效性依赖以下核心假设：

- **Assumption 1（激励函数可分离）**：$\phi_{ij}(s) = a_{ij} w(s)$，即激励函数可分解为恒定的节点间影响系数 $a_{ij}$ 和仅依赖于时滞的公共衰减函数 $w(s)$。这是利用秩约束的必要前提。

- **Definition 4.4（对称无环路径条件）**：要求潜在混淆变量对其观测子节点的影响路径满足一定的对称性，这是理论可识别性的关键条件。实验表明该条件在实际中被轻度违反时方法仍保持鲁棒性（F1 约 0.89–0.92）。

- **离散化间隔 $\Delta$ 的选择**：Table 1 显示，当 $\Delta \leq 0.1$ 时性能保持稳定和高水平，但 $\Delta = 0.3$ 时性能急剧下降，说明细粒度时间分辨率至关重要。秩检验阈值 $\tau = 0.10$ 在不同场景下取得良好平衡（Table 2）。

### 方法定位与差异化

与现有方法的本质区别体现在三个维度：

| 维度 | 现有方法 | 本文方法 |
|------|---------|---------|
| 时间建模 | 连续时间最大似然估计（SHP, THP）或分箱计数似然 | 离散时间线性自回归表示 + 二阶统计量 |
| 因果准则 | Granger 因果性或似然拟合 | 交叉协方差矩阵的秩约束条件 |
| 潜在混淆处理 | 无（假设因果充分性） | 利用秩亏损自动迭代发现 |

传统 Hawkes 因果发现方法（如 **NPHC** (Achab et al., 2018)、**SHP** (Qiao et al., 2023)、**THP** (Cai et al., 2022)）均假设所有子过程可观测，而基于 i.i.d. 数据的秩方法（如 **Hier.Rank** (Huang et al., 2022)、**RLCD** (Dong et al., 2023)）和时间序列方法（如 **LPCMCI** (Gerhardus & Runge, 2020)）未针对 Hawkes 过程的连续时间特性设计。本文方法首次在统一框架内同时解决这两个挑战。



### 瓶颈与核心洞察

现有Hawkes过程因果发现方法的根本瓶颈在于**因果充分性假设**——即假定所有子过程均可观测，无法处理未观测到的潜在混淆变量。本文的核心洞察是：当离散化时间间隔 $\Delta \to 0$ 时，多元Hawkes过程可表示为离散时间线性因果模型，而潜在混淆变量会在观测变量的交叉协方差矩阵中产生特定的**秩亏损**（rank deficiency），通过检验这种低秩特征即可识别其存在及因果影响。

### 关键假设

**Assumption 1（激励函数可分离性）**：激励函数可分解为恒定影响系数与公共时滞衰减函数的乘积：

$$\phi_{ij}(s) = a_{ij} w(s)$$

其中 $a_{ij}$ 表示子过程 $j$ 对 $i$ 的恒定影响强度，$w(s)$ 是仅依赖于时滞 $s$ 的公共衰减函数。该假设是后续秩约束条件成立的理论前提。

### 模块一：离散化与线性自回归表示

将连续事件序列按固定间隔 $\Delta$ 离散化，定义第 $n$ 个时间窗内的事件计数：

$$N_i^{(n)} := N_i(n\Delta) - N_i((n-1)\Delta)$$

**Theorem 4.1（Hawkes过程的线性自回归表示）**：当 $\Delta \to 0$ 时，平稳多元Hawkes过程可表示为：

$$N_i^{(n)} = \sum_{j=1}^{l} \sum_{k=1}^{n} \theta_{ij}^{(k)} N_j^{(n-k)} + \varepsilon_i^{(n)} + \theta_i^{(0)}$$

其中激励系数 $\theta_{ij}^{(k)} = \int_{(k-1)\Delta}^{k\Delta} \phi_{ij}(s) ds$，背景参数 $\theta_i^{(0)} = \Delta \cdot \mu_i$。这一表示将连续时间因果结构编码为离散变量间的线性关系，是后续所有秩约束方法的基础。

### 模块二：秩约束与因果发现准则

**Lemma 4.2（窗因果图中的d-分离与秩约束）**：在窗因果图（window causal graph）中，变量集 $\mathbf{A}_v$ 与 $\mathbf{B}_v$ 被 $\mathbf{C}_v$ d-分离，当且仅当：

$$\mathrm{rank}(\Sigma_{\mathbf{A}_v \cup \mathbf{C}_v, \mathbf{B}_v \cup \mathbf{C}_v}) = |\mathbf{C}_v|$$

该引理将图结构中的条件独立性转化为交叉协方差矩阵的秩条件，是因果发现的算子级基础。

**Proposition 4.3（识别观测父因集）**：子过程 $N_1$ 的观测父因集 $P_G$ 是满足以下秩条件的最小集合：

$$\mathrm{rank}(\Sigma_{\{O_1^{(n)}\} \cup \mathbf{P}_v, \mathbf{O}_v \setminus \{O_1^{(n)}\}}) = |\mathbf{P}_v|$$

### 模块三：潜在混淆变量识别

**Proposition 4.5（识别潜在混淆变量）**：存在一个潜在混淆子过程 $L_1$ 同时影响观测子过程 $O_1$ 和 $O_2$，当且仅当：

$$\mathrm{rank}\left( \Sigma_{ \{O_i^{(j)}\}_{i\in\{1,2\}}^{j\in\{n-m,\dots,n\}}, \mathbf{O}_v \setminus \{O_1^{(n)}, O_2^{(n)}\} } \right) = 2m + 1$$

其中 $2m$ 对应 $O_1$ 和 $O_2$ 各自的 $m$ 个滞后变量（自环效应），额外的秩 $1$ 即来自潜在混淆变量 $L_1$。该命题揭示了潜在混淆变量在二阶统计量中留下的**低秩足迹**。

**Definition 4.6（观测代理变量）**：对每个从观测效应 $\{O_1, O_2\}$ 推断出的潜在子过程 $L_1$，指定其一个观测效应 $\hat{D}e(L_1) := O_1$ 作为 $L_1$ 的观测代理（observed surrogate），用于后续涉及该潜在变量的秩条件评估。

**Theorem 4.7（一般父因集识别）**：当涉及潜在混淆变量时，子过程 $N_1$ 的父因集 $P'_G$ 是满足以下秩条件的最小集合：

$$\mathrm{rank}( \Sigma_{\mathbf{A}_v, \mathbf{B}_v} ) = |\mathbf{A}_v| - 1$$

其中 $\mathbf{A}_v$ 包含目标子过程的滞后变量、已推断潜在子过程的代理变量滞后项、以及观测父因的滞后变量。该定理将 Proposition 4.3 推广至包含潜在变量的任意因果结构。

**Theorem 4.8（从潜在混淆变量识别潜在混淆变量）**：将 Theorem 4.7 和 Proposition 4.5 中的潜在子过程替换为其观测代理，即可识别潜在混淆变量之间的因果关系（如 Figure 3d 所示结构）。

### 模块四：两阶段迭代算法

**Phase I（因果关系识别）**：利用 Proposition 4.3 和 Theorem 4.7，对每个已发现子过程，通过最小化满足秩条件的变量集来识别其父因集。

**Phase II（新潜在子过程发现）**：利用 Proposition 4.5 和 Theorem 4.8，检测成对子过程间的秩亏损，发现新的潜在混淆变量，并为其指定观测代理。

两阶段交替迭代，直至无新子过程被发现。算法必然终止，因为每次迭代要么发现新子过程（有限数量），要么确认当前因果结构。

### 理论依赖链

整个方法的理论保证建立在以下依赖链上：Assumption 1（激励函数可分离）→ Theorem 4.1（线性自回归表示）→ Lemma 4.2（d-分离的秩条件）→ Proposition 4.3/4.5（观测/潜在父因集识别）→ Theorem 4.7/4.8（一般因果结构识别）。其中 **Definition 4.4 的对称无环路径条件**是 Proposition 4.5 可识别性的关键前提，实验表明该方法对该条件的轻度违反具有一定鲁棒性。



## 实验与关键发现

### 主要结果

#### 合成数据：因果结构恢复能力

方法在六个合成因果图（Case 1–6）上进行了系统评估，覆盖从无混淆到复杂多层潜在混淆的场景。Figure 4 和 Figure 8 展示了所提方法与六种基线的 F1-score 对比。在所有包含潜在混淆变量的案例中，所提方法显著优于基线方法，验证了其处理潜在混淆的核心优势。

在完全观测的 Case 1（Fig. 1b）中，方法表现与最优基线 SHP 相当，表明在因果充分性假设成立时，离散化线性自回归框架未引入信息损失。当引入潜在混淆变量（Case 2, Fig. 2a）后，所提方法保持高 F1-score，而所有基线方法性能大幅下降——因为它们假设因果充分性，无法处理未观测的混淆子过程。Case 3–6 进一步引入更复杂的潜在混淆结构（Fig. 3a–3d），方法仍能有效恢复因果图，证明了 Proposition 4.5 和 Theorem 4.8 在迭代发现中的有效性。

在更大规模因果图（Fig. 9，14个子过程）上，方法展现出良好的可扩展性：F1-score 随样本量增加单调提升（30k: 0.58, 50k: 0.64, 80k: 0.75），表明随着观测数据增多，秩约束条件的统计检验更加可靠。

#### 真实世界数据：蜂窝网络告警因果发现

在蜂窝网络子数据集（Alarm ids=0–3,7; device id=8）上，将 Alarm id=7 人工排除并视为潜在混淆子过程。Table 8 显示，所提方法取得 F1-score 0.76，较最优基线 SHP（0.49）提升 27 个百分点。Figure 5 展示了推断的因果子图，方法成功将 Alarm id=7 识别为潜在子过程，并恢复了其主要因果影响关系。这验证了方法在真实时序事件数据中发现隐藏因果结构的实用价值。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_mA78uXqcnl/figures/028_Table_8.jpg]]
*Table 8: F1-scores on the cellular network sub-dataset (Alarm ids=0-3 and 7, device id = 8) where Alarm id=7 is manually excluded and treated as a latent subprocess; averages over 10 runs*

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_mA78uXqcnl/figures/014_Figure_5.jpg]]
*Figure 5: Inferred causal subgraph from the cellular network dataset, where Alarm id=7 is successfully identified as a latent subprocess*

### 消融实验

#### 离散化间隔 Δ 的敏感性

Table 1 展示了在指数激励核（β=1）下，不同 Δ 值对性能的影响。当 Δ ≤ 0.1 时，方法性能保持稳定且高水平（F1-score 0.82–0.97）；但当 Δ = 0.3 时，性能急剧下降（F1-score 降至 0.25–0.59）。这一结果直接验证了 Theorem 4.1 的理论条件：线性自回归表示仅在 Δ → 0 时精确成立，过大的离散化间隔会丢失细粒度时序信息，破坏秩约束条件的有效性。实际应用中需根据激励函数的支撑域选择足够小的 Δ。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_mA78uXqcnl/figures/019_Table_1.jpg]]
*Table 1: Performance of our method under varying $\Delta$ values using 80k Hawkes process samples generated by the $\pm \mathrm { i } \mathrm { c k }$ library with decay parameter $\beta$ = 1 in the exponential excitation function. Case 1–3 correspond to Figs. 1b, 2a, and 3a, respectively. Results are averaged over ten runs. Performance remains stable and high when $\Delta \leq$ 0 . 1 , but degrades significantly at $\Delta$ = 0 . 3 due to the loss of fine-grained temporal information

#### 秩检验阈值 τ 的敏感性

Table 2 测试了 τ ∈ {0.01, 0.05, 0.10, 0.20} 对性能的影响。τ = 0.10 在不同场景下取得良好平衡（Case 1: F1=0.74; Case 2: F1=0.73; Case 3: F1=0.72）。过小的 τ（0.01）导致召回率下降，因为过于严格的秩条件拒绝真实边；过大的 τ（0.20）导致精度下降，因为噪声被误判为秩亏损信号。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_mA78uXqcnl/figures/020_Table_2.jpg]]
*Table 2: Sensitivity to the rank-test threshold τ . Each entry is averaged over ten runs on 30k samples generated with an exponential kernel ( $\beta$ = 1 ) Case 1–3 correspond to Figs. 1b, 2a, and 3a, respectively. Overall, a threshold of 0.10 provides a good balance across different scenarios. Table 3: Performance of our method when, in each run, two edges in each graph are randomly assigned identical coefficients $\alpha _ { i j }$ for the exponential excitation function, increasing the risk of rank deficiency. Hawkes process samples are generated by the tick library. Case 1–3 correspond to Figs. 1b, 2a, and 3a, respectively. Results are averaged over ten runs. Despite these perturbations, our method...

#### 秩违反条件下的鲁棒性

Table 3 测试了人为制造秩违反（随机分配相同边系数）时的性能。即便存在这种对理论假设的直接扰动，方法仍保持较强鲁棒性（Case 1 F1=0.92, Case 2 F1=0.82, Case 3 F1=0.80），尤其在样本量增大时性能恢复明显。这表明秩约束方法在实际应用中具有一定容错能力。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_mA78uXqcnl/figures/021_Table_3.jpg]]

#### 小样本性能

Table 4 展示了仅 5k 样本下 Case 1 的性能对比。SHP 凭借最大似然估计在小样本下表现最优（F1=0.96），所提方法（F1=0.71–0.74）虽不及 SHP，但仍保持有竞争力的水平，且显著优于其他基线（如 Hier.Rank F1=0.00, RLCD F1=0.19）。这反映了基于二阶统计量的方法在极小样本下的固有局限——协方差矩阵估计需要足够样本量。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_mA78uXqcnl/figures/022_Table_4.jpg]]
*Table 4: Performance of all methods on Case 1 (fully observed, no latent confounders) using only 5k samples. Values are mean scores across ten runs, with standard deviation shown in parentheses*

#### 对称路径条件违反

Table 5 测试了违反 Definition 4.4 对称路径条件时的性能。当条件被轻度破坏时，性能仅轻微下降（F1 约 0.89–0.92），证明方法具有实际鲁棒性。但需注意，严重违反该条件可能导致可识别性丧失，这是理论框架的已知边界。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_mA78uXqcnl/figures/023_Table_5.jpg]]
*Table 5: Performance under violations of the symmetric path condition in Definition 4.4 (Case 2 in Fig. 2a). Values are mean ± standard deviation*

### 关键图表结论

- **Figure 4 & 8**：所提方法在全部六个合成案例上一致优于基线，尤其在存在潜在混淆时优势显著，验证了秩约束框架的有效性。
- **Figure 5**：真实世界推断图成功恢复 Alarm id=7 作为潜在子过程及其因果影响，证明方法的实践价值。
- **Table 1**：Δ ≤ 0.1 时性能稳定，Δ = 0.3 时急剧下降——细粒度时间分辨率是方法有效的前提。
- **Table 6**：方法在 14 节点因果图上随样本量增加稳定提升，F1 从 0.58 升至 0.75，表明可扩展性良好。
- **Table 7**：运行时间统计显示，两阶段迭代算法的计算开销在可接受范围内，但极大规模网络仍需优化。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_mA78uXqcnl/figures/025_Table_6.jpg]]
*Table 6: Performance of our method on the larger causal graph in Fig. 9, using Hawkes process data generated by the tick library. Results are averaged over ten runs. The method consistently recovers the causal structure with improving accuracy as sample size increases*

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_mA78uXqcnl/figures/026_Table_7.jpg]]
*Table 7: Runtime across synthetic and real-world settings*

### 失败模式与局限

1. **大 Δ 导致性能崩溃**：当离散化间隔过大时，线性自回归近似失效，秩条件不再可靠。这是方法最显著的失败模式，需根据数据特性谨慎选择 Δ。
2. **小样本下协方差估计不稳定**：5k 样本时性能明显低于最大似然方法，二阶统计量的估计方差在高维场景下进一步放大。
3. **对称路径条件违反**：虽然实验显示一定鲁棒性，但严重违反该条件时理论可识别性不保，可能导致漏检或误检潜在混淆变量。
4. **计算复杂度瓶颈**：Phase I 的最坏情况复杂度接近 O(n!·...)，在极大规模网络上可能不可行，Table 7 的运行时间统计提供了参考量级。



## 定位与知识库关联

### 问题瓶颈与核心创新

现有基于Hawkes过程的因果发现方法——包括基于离散化计数的最大化似然估计 **SHP** (Qiao et al., 2023)、基于时间点过程的 **THP** (Cai et al., 2022) 以及非参数矩匹配方法 **NPHC** (Achab et al., 2018)——均假定所有子过程均可观测（因果充分性）。这一假定在现实场景中几乎不成立：当存在未观测到的潜在混淆变量时，上述方法无法正确恢复因果结构，这是该领域长期悬置的核心瓶颈。

本文提出的两阶段迭代发现算法（Two-Phase Iterative Discovery Algorithm）通过三个关键创新突破这一瓶颈：

1. **时间表示与建模的范式转换**：从连续时间最大似然估计或分箱计数似然，转向离散时间线性自回归表示。Theorem 4.1 严格证明了当离散化间隔 $\Delta \to 0$ 时，平稳多元Hawkes过程可表示为线性自回归模型 $N_i^{(n)} = \sum_{j=1}^{l} \sum_{k=1}^{n} \theta_{ij}^{(k)} N_j^{(n-k)} + \varepsilon_i^{(n)} + \theta_i^{(0)}$，从而将因果发现问题转化为对离散变量二阶统计量的分析，避免了复杂的似然优化。

2. **因果发现准则的根本变革**：从Granger因果性或似然拟合，转向基于交叉协方差矩阵的秩约束条件。Lemma 4.2 建立了窗因果图中d-分离与秩条件 $\mathrm{rank}(\Sigma_{\mathbf{A}_v \cup \mathbf{C}_v, \mathbf{B}_v \cup \mathbf{C}_v}) = |\mathbf{C}_v|$ 的等价关系，Proposition 4.3 进一步将其转化为识别观测父因集的充分必要条件。这一秩约束框架为后续的潜在变量发现奠定了理论基础。

3. **潜在混淆变量的自动发现机制**：从假设因果充分性，转向利用秩亏损（rank deficiency）自动检测潜在混淆变量。核心洞察是：潜在混淆变量会在观测变量的交叉协方差矩阵中产生特定的低秩特征——Proposition 4.5 给出了识别影响两个观测子过程的潜在混淆变量的充要秩条件 $\mathrm{rank}( \Sigma_{ \{ O_i^{(j)} \}_{i\in\{1,2\}}^{j\in\{n-m,\dots,n\}}, \mathbf{O}_v \setminus \{O_1^{(n)}, O_2^{(n)}\} } ) = 2m + 1$，Theorem 4.7 和 Theorem 4.8 进一步将可识别性扩展到包含观测和推断潜在子过程之间的任意因果关系。

### 与现有方法的谱系关系

**基于Hawkes过程的方法（SHP, THP, NPHC）**：这些方法构成了本文的直接基线。它们在因果充分性假设下运行，无法处理潜在混淆变量。本文通过离散化线性表示和秩约束框架，不仅解决了潜在变量问题，在完全观测场景下也展现出显著优势——在蜂窝网络子数据集上，本文方法F1-score达到0.76，而SHP仅为0.49，THP为0.48，NPHC为0.42（Table 8）。这种性能差距表明，即便在无潜在变量的理想条件下，基于二阶统计量的秩约束方法也比似然方法更鲁棒。

**基于i.i.d.数据的秩方法（Hier.Rank, RLCD）**：**Hier.Rank** (Huang et al., 2022) 和 **RLCD** (Dong et al., 2023) 在i.i.d.设定下利用秩约束进行潜变量因果发现，与本文共享了利用协方差矩阵低秩特征识别潜在变量的基本思想。然而，这些方法设计用于独立同分布数据，无法直接处理时间序列中的时序依赖。本文的关键贡献在于将秩约束框架从i.i.d.域推广到连续时间事件序列域：通过Theorem 4.1的线性自回归表示，将Hawkes过程的时序依赖编码为窗因果图中的滞后变量，从而使i.i.d.域中的秩约束技术得以迁移。实验结果表明，在时间序列场景下，Hier.Rank的F1-score为0.00（完全失效），RLCD为0.39（Table 8），验证了直接迁移i.i.d.方法的不可行性。

**时间序列因果发现方法（LPCMCI）**：**LPCMCI** (Gerhardus & Runge, 2020) 是时间序列因果发现的重要方法，可处理外生潜在变量。但其设计基于离散时间条件独立性检验，与本文基于连续时间点过程的框架存在根本差异。在蜂窝网络数据集上，LPCMCI的F1-score为0.43（Table 8），显著低于本文方法，表明基于条件独立性的方法在Hawkes过程数据上的适应性有限。

### 适用边界与理论前提

本文方法的有效性依赖于若干关键假设，这些假设界定了方法的适用边界：

1. **激励函数可分离性（Assumption 1）**：$\phi_{ij}(s) = a_{ij} w(s)$，即激励函数可分解为恒定影响系数 $a_{ij}$ 和仅依赖于时滞的公共衰减函数 $w(s)$。这一假设是秩约束推导的理论基石——它确保了不同子过程间的激励系数矩阵具有低秩结构，从而使得潜在混淆变量的秩亏损特征可被检测。若实际系统中各节点需要不同的衰减速率（例如不同事件类型的记忆衰减速度不同），该假设可能被违反，方法的理论保证将不再成立。这是当前框架最核心的限制条件。

2. **对称无环路径条件（Definition 4.4）**：该条件是Proposition 4.5中潜在混淆变量可识别性的理论前提。它要求潜在混淆变量对两个观测子过程的影响路径在窗因果图中满足特定的对称性。实验表明（Table 5），当该条件被轻度破坏时，方法性能仅轻微下降（F1约0.89–0.92），证明方法具有实际鲁棒性；但理论上的完全可识别性依赖于该条件的严格成立。

3. **离散化间隔的选择**：Theorem 4.1要求 $\Delta \to 0$ 以严格成立，实践中需要在时间分辨率和统计效率之间权衡。消融实验（Table 1）表明，当 $\Delta \leq 0.1$ 时性能保持稳定和高水平，但 $\Delta = 0.3$ 时性能急剧下降，说明细粒度时间分辨率对方法至关重要。这一敏感性意味着在激励函数支撑域未知或数据稀疏的场景下，$\Delta$ 的选择可能需要领域知识或交叉验证。

4. **平稳性与有效时滞**：方法假设Hawkes过程是平稳的，且因果影响在有限时滞 $m$ 内截断。对于非平稳过程或具有长程依赖的系统，当前框架可能需要扩展。

### 计算复杂度的实际考量

两阶段迭代算法的Phase I在最坏情况下复杂度接近 $O(n! \cdot \dots)$，这意味着极大规模网络可能面临可扩展性瓶颈。Table 7报告了合成和真实世界场景下的运行时间统计，但未提供与基线方法在大规模网络上的详细对比。对于包含数十个以上子过程的网络，可能需要引入启发式剪枝或近似秩检验来降低计算负担。这是从理论框架走向大规模实际部署需要解决的关键工程问题。

### 开放问题与未来方向

基于上述分析，以下几个方向值得关注：

1. **放松激励函数假设**：如何将方法推广到允许节点特定的衰减速率 $\phi_{ij}(s) = a_{ij} w_{ij}(s)$，是扩展理论适用性的首要任务。可能的路径包括引入非参数估计或利用核方法对衰减函数进行自适应建模。

2. **可扩展性改进**：开发更低复杂度的发现算法（例如利用启发式剪枝或基于梯度的秩近似），将方法扩展至大规模网络（如社交媒体传播级联、金融网络等），是实际应用的关键需求。

3. **更一般潜在混淆结构的可识别性**：进一步放宽对称路径条件，提高对非对称因果路径、多层级潜在混淆变量等更复杂结构的可识别性，是理论层面的重要挑战。

4. **跨领域验证**：当前仅在合成数据和蜂窝网络数据集上验证，在社交媒体传播、金融级联、神经科学spike train等更多实际领域中，该方法能提供哪些深刻的因果洞见，有待系统探索。



## 原文 PDF

![[paperPDFs/ICLR_2026/Causal_Structure_Learning_in_Hawkes_Processes_with_Complex_Latent_Confounder_Networks.pdf]]
