---
title: "DistDF: Time-series Forecasting Needs Joint-distribution Wasserstein Alignment"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/DistDF_Time_series_Forecasting_Needs_Joint_distribution_Wasserstein_Alignment.pdf
project_link: null
code_link: https://github.com/Master-PLC/DistDF
openreview_forum_id: VrdLwUmzBy
aliases:
- DistDF
tags:
- ICLR_2026
- topic/time_series_dynamical_systems
- topic/time_series_dynamical_systems/time_series_forecasting
core_operator: "通过最小化联合分布的Wasserstein差异来对齐预测与标签的条件分布，从而绕过自相关偏差。"
primary_logic: "联合分布Wasserstein差异可证明地作为条件分布差异的上界，并且可以通过有限样本进行可微、无偏的估计，适用于梯度优化训练。"
claims:
- "MSE忽略标签序列的自相关结构，导致有偏的负对数似然估计（自相关偏差）。"
- "频域（FreDF）和PCA（Time-o1）变换仅保证边缘去相关，条件自相关依然存在，偏差持续。"
- "联合分布Wasserstein差异上界期望条件差异（Lemma 3.3），且最小化至零可保证条件分布对齐（Theorem 3.4）。"
- "在多个模型和数据集上，DistDF始终优于标准DF和其他学习目标，消融实验证实均值与协方差对齐的协同作用。"
---

# DistDF: Time-series Forecasting Needs Joint-distribution Wasserstein Alignment

> [!tip] 核心洞察
> 联合分布Wasserstein差异可证明地作为条件分布差异的上界，并且可以通过有限样本进行可微、无偏的估计，适用于梯度优化训练。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DistDF：时间序列预测需要联合分布Wasserstein对齐 |
| 英文题名 | DistDF: Time-series Forecasting Needs Joint-distribution Wasserstein Alignment |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=VrdLwUmzBy) · [GitHub](https://github.com/Master-PLC/DistDF) |
| Topic | #topic/time_series_dynamical_systems #topic/time_series_dynamical_systems/time_series_forecasting |
| Method | DistDF |
| Dataset | ETTm1, ETTh1, ECL, Traffic |

> [!tip] 效果简介
> - ETTm1 上，MSE 为 0.378，对比 0.394 (TimeBridge)，变化 0.016 lower。
> - ETTh1 上，MSE 为 0.430，对比 0.442 (TimeBridge)，变化 0.012 lower。
> - ECL 上，MSE 为 0.172，对比 0.176 (TimeBridge)，变化 0.004 lower。

## 概要

时间序列预测的标准训练目标——均方误差（MSE）——存在一个被长期忽视的结构性问题：它假设标签序列的每个未来时间步相互独立，从而忽略了标签内部的自相关结构。这一疏忽使得MSE成为真实负对数似然的有偏估计，即产生**自相关偏差**（Theorem 3.1）。尽管频域变换（如FreDF）和主成分分析（如Time-o1）等方法试图通过去相关来缓解该问题，但它们仅保证边缘去相关，条件自相关依然存在，偏差并未消除（Figure 1）。

针对这一瓶颈，本文提出**DistDF**，其核心思路是通过最小化预测序列与标签序列在**联合分布**上的Wasserstein差异，间接实现条件分布的对齐。理论分析表明，联合分布Wasserstein差异可证明地作为条件分布差异的上界（Lemma 3.3），且将其最小化至零可保证条件分布对齐（Theorem 3.4）。在高斯假设下，该差异具有闭式解——Bures-Wasserstein差异，可分解为均值对齐项与协方差对齐项，且可通过有限样本进行可微、无偏的估计（Lemma 3.5）。

DistDF作为一种即插即用的学习目标，可与各类预测模型结合。实验覆盖多个主流模型（TimeBridge、Fredformer、iTransformer等）和数据集（ETT、ECL、Traffic等），结果表明DistDF一致优于标准MSE训练及其他学习目标（Table 1、Table 2）。消融实验证实，均值对齐与协方差对齐具有协同效应，二者联合使用方能取得最佳性能（Table 3）。此外，DistDF在自回归预测和概率预测设定下同样表现稳健（Table 16、Table 17）。



时间序列预测的核心任务是根据历史观测 $X$ 预测未来序列 $Y$。当前主流的深度学习预测方法几乎无一例外地采用均方误差（MSE）作为训练目标：

$$\mathcal{L}_{\mathrm{mse}} = \| Y_{|X} - \hat{Y}_{|X} \|_2^2 = \sum_{t=1}^{\mathrm{T}} (Y_{|X,t} - \hat{Y}_{|X,t})^2$$

这一损失函数将每个未来时间步视为独立的预测任务，逐点计算预测值与标签之间的平方误差。然而，MSE 的简洁性背后隐藏着一个根本性的缺陷：**它完全忽略了标签序列内部的自相关结构**。

### 自相关偏差：MSE 的根本缺陷

真实世界的时间序列标签 $Y_{|X}$ 在给定历史 $X$ 的条件下，其不同时间步之间通常存在显著的条件相关性。Figure 1(a) 的可视化结果清晰地揭示了这一现象：在预测长度为 192 的设置下，原始标签的条件相关矩阵中，超过 50.3% 的非对角元素的绝对值超过 0.1，表明标签序列具有不可忽略的自相关结构。

当标签存在条件自相关时，MSE 作为负对数似然的估计量是有偏的。这一偏差可以通过 Theorem 3.1 精确刻画：

$$\mathrm{Bias} = \| Y_{|X} - \hat{Y}_{|X} \|_{\Sigma_{|X}^{-1}}^2 - \| Y_{|X} - \hat{Y}_{|X} \|_2^2$$

其中 $\Sigma_{|X}$ 是给定 $X$ 条件下 $Y$ 的条件协方差矩阵。只有当 $\Sigma_{|X} = I$（即标签各时间步条件独立且方差为 1）时，偏差才为零。在实际情况中，$\Sigma_{|X} \neq I$，MSE 会系统性地偏离真实的似然目标，导致模型训练方向出现偏差。

### 现有方法的局限

为缓解自相关问题，近期工作尝试在变换域中进行预测。FreDF 将标签变换到频域，利用傅里叶基函数对序列进行去相关；Time-o1 则采用主成分分析（PCA）在特征空间中进行类似操作。这些方法的共同假设是：变换后的成分在**边际分布**上是去相关的（即 $\Sigma$ 为对角矩阵）。

然而，Figure 1(b-c) 的证据表明这一策略存在根本性局限。尽管 FreDF 的频域成分和 Time-o1 的主成分在边际上确实实现了去相关，但在给定历史序列 $X$ 的条件下，**条件自相关依然存在**。这是因为傅里叶变换和 PCA 仅保证 $\Sigma$ 对角化，而实际需要的是 $\Sigma_{|X}$ 对角化——两者之间存在本质区别。因此，自相关偏差在这些方法中持续存在，模型训练仍然受到有偏似然估计的困扰。

### 本文动机

上述分析揭示了一个关键瓶颈：**基于似然的 MSE 目标函数因忽略标签自相关结构而导致似然估计偏差，阻碍模型训练**。现有变换域方法仅在边缘分布层面进行去相关，未能从根本上消除条件自相关带来的偏差。

这引出了本文的核心动机：能否设计一种学习目标，直接对齐预测分布与标签分布之间的**条件依赖关系**，从而绕过自相关偏差？具体而言，需要解决两个关键问题：如何度量两个条件分布之间的差异，以及如何使该度量可微且适用于梯度优化训练。



## 核心方法与创新机理

DistDF 的核心创新在于**将时间序列预测的学习目标从逐点误差最小化转向联合分布对齐**，从而从根本上解决 MSE 损失函数忽略标签序列自相关结构所导致的似然估计偏差问题。

### 问题根源：自相关偏差

标准 MSE 损失函数将每个未来时间步视为独立的预测任务，隐含假设标签序列的条件协方差矩阵为单位阵（$\Sigma_{|X} = I$）。然而，实际标签序列的条件分布具有显著的自相关结构——在 ETTm1 数据集上，预测长度 T=192 时，超过 50.3% 的条件相关系数绝对值超过 0.1（Figure 1a）。这一假设违背导致 MSE 相对于真实负对数似然产生系统性偏差：

$$\mathrm{Bias} = \| Y_{|X} - \hat{Y}_{|X} \|_{\Sigma_{|X}^{-1}}^2 - \| Y_{|X} - \hat{Y}_{|X} \|_2^2$$

该偏差仅在 $\Sigma_{|X} = I$ 时消失（Theorem 3.1）。现有方法如 FreDF（频域变换）和 Time-o1（PCA 变换）仅能保证边缘去相关（即 $\Sigma$ 对角化），而无法消除条件自相关（$\Sigma_{|X}$ 非对角），因此偏差持续存在（Figure 1b-c）。

### 核心机制：联合分布 Wasserstein 对齐

DistDF 的关键设计在于**通过最小化联合分布 $P_{X,Y}$ 与 $P_{X,\hat{Y}}$ 之间的 Wasserstein 差异来间接对齐条件分布 $P_{Y|X}$ 与 $P_{\hat{Y}|X}$**。这一策略的理论基础由两个定理支撑：

1. **上界关系**（Lemma 3.3）：期望条件 Wasserstein 差异被联合分布 Wasserstein 差异所上界：
   $$\int \mathcal{W}_p(P_{Y|X}, P_{\hat{Y}|X}) dP(X) \leq \mathcal{W}_p(P_{X,Y}, P_{X,\hat{Y}})$$

2. **对齐保证**（Theorem 3.4）：将联合分布 Wasserstein 差异最小化至零可保证条件分布对齐，即 $P_{Y|X} = P_{\hat{Y}|X}$。

在高斯假设下，联合分布 Wasserstein 差异具有闭式解——Bures-Wasserstein 差异（Lemma 3.5）：

$$\mathcal{BW}(\mu_{X,Y}, \mu_{X,\hat{Y}}, \Sigma_{X,Y}, \Sigma_{X,\hat{Y}}) = \|\mu_{X,Y} - \mu_{X,\hat{Y}}\|_2^2 + \mathcal{B}(\Sigma_{X,Y}, \Sigma_{X,\hat{Y}})$$

其中协方差项为 Bures 度量：
$$\mathcal{B}(\Sigma_{X,Y}, \Sigma_{X,\hat{Y}}) = \mathrm{Tr}(\Sigma_{X,Y} + \Sigma_{X,\hat{Y}} - 2\sqrt{\Sigma_{X,Y}^{1/2}\Sigma_{X,\hat{Y}}\Sigma_{X,Y}^{1/2}})$$

该公式将分布差异分解为**均值对齐**与**协方差对齐**两部分，且均可通过有限样本进行可微、无偏估计，直接嵌入梯度优化训练。

### 与 Baseline 的关键差异

| 维度 | 标准 DF（MSE） | DistDF |
|------|---------------|--------|
| **学习目标** | $\mathcal{L}_{\mathrm{mse}}$ | $\mathcal{L}_{\alpha} = \alpha \cdot \mathcal{L}_{\mathrm{dist}} + (1-\alpha) \cdot \mathcal{L}_{\mathrm{mse}}$ |
| **差异度量** | 逐时间步点误差 | 联合分布 Wasserstein 差异（Bures-Wasserstein） |
| **分布假设** | 隐式假设 $\Sigma_{\|X}=I$ | 显式建模并对齐联合分布的一阶矩和二阶矩 |
| **偏差处理** | 存在自相关偏差 | 理论上绕过自相关偏差 |

### 消融验证：均值与协方差的协同效应

消融实验（Table 3）揭示了两个对齐维度的协同作用：
- **仅对齐均值**（DistDF†）：在 ETTm1 上将 MSE 从 0.387 降至 0.381
- **仅对齐协方差**（DistDF‡）：同样带来改善
- **联合对齐**（DistDF）：取得最优结果，验证了均值与协方差联合匹配的协同效应

### 局限性

DistDF 仅量化联合分布的一阶矩（均值）和二阶矩（协方差）差异，丢弃了预测与标签序列之间的逐元素对应关系。因此，其独立作为损失函数时效果受限，通常需要与 MSE 结合作为正则项（$\alpha$ 取较小正值如 0.001–0.1）才能发挥最佳性能。在高维多元场景下，协方差矩阵的计算开销也值得关注。



![[assets/figures/papers/iclr26_0009_VrdLwUmzBy_DistDF_Time-series_Forecasting_Needs_Joint-distr/figures/003_Figure_1.jpg]]
*Figure 1: The conditional correlation of label components given X, where the forecast horizon is set to $\mathrm { \bar { T } = 1 9 2 }$ . The correlation matrices are computed for the raw labels (a), the frequency components in FreDF (b) (Wang et al., 2025g) and the principal components in Time-o1 (c) (Wang et al., 2025f)

DistDF 并非一种新的预测模型架构，而是一种即插即用的学习目标增强方案，可叠加于任意确定性时间序列预测模型之上。其整体流程围绕一个核心思想展开：将传统的逐点均方误差（MSE）损失扩展为联合分布对齐损失，从而纠正 MSE 因忽略标签自相关结构而产生的似然估计偏差。

### Pipeline 总览

整个训练过程由五个模块串联构成，如下所示：

1. **预测生成（Forecast Model $g$）**：给定历史序列 $X \in \mathbb{R}^{H \times D}$（$H$ 为历史长度，$D$ 为变量数），基础预测模型 $g$ 输出预测序列 $\hat{Y} \in \mathbb{R}^{T \times D}$（$T$ 为预测长度）。该模块对 DistDF 透明，可以是 Transformer、线性模型或频域模型等任意架构。

2. **联合序列构建（Joint Concatenation）**：沿时间轴将历史序列 $X$ 与标签序列 $Y$ 拼接为联合序列 $Z = [X; Y]$，同时将 $X$ 与预测序列 $\hat{Y}$ 拼接为 $\hat{Z} = [X; \hat{Y}]$。这一步将条件分布对齐问题转化为联合分布对齐问题。

3. **统计量计算（Statistics）**：对每个批次样本，分别计算 $Z$ 和 $\hat{Z}$ 的均值向量 $\mu_{X,Y}$、$\mu_{X,\hat{Y}}$ 与协方差矩阵 $\Sigma_{X,Y}$、$\Sigma_{X,\hat{Y}}$。

4. **Bures-Wasserstein 差异计算（BW Discrepancy）**：在高斯假设下，联合分布 $P_{X,Y}$ 与 $P_{X,\hat{Y}}$ 之间的 2-Wasserstein 差异具有闭式解——Bures-Wasserstein 差异：
   $$\mathcal{L}_{\mathrm{dist}} = \|\mu_{X,Y} - \mu_{X,\hat{Y}}\|_2^2 + \mathcal{B}(\Sigma_{X,Y}, \Sigma_{X,\hat{Y}})$$
   其中 Bures 度量 $\mathcal{B}(\Sigma_{X,Y}, \Sigma_{X,\hat{Y}}) = \mathrm{Tr}(\Sigma_{X,Y} + \Sigma_{X,\hat{Y}} - 2\sqrt{\Sigma_{X,Y}^{1/2}\Sigma_{X,\hat{Y}}\Sigma_{X,Y}^{1/2}})$ 量化协方差结构的不相似度。该差异可微且可通过有限样本无偏估计，直接用于梯度优化。

5. **组合损失（Combined Loss）**：将分布差异项与标准 MSE 损失加权组合，形成最终训练目标：
   $$\mathcal{L}_{\alpha} := \alpha \cdot \mathcal{L}_{\mathrm{dist}} + (1-\alpha) \cdot \mathcal{L}_{\mathrm{mse}}$$
   其中 $\alpha \in [0,1]$ 控制分布对齐的强度。

### 输入输出流

- **输入**：历史序列 $X$、标签序列 $Y$（训练时）、预测模型 $g$、权重系数 $\alpha$。
- **前向传播**：$X \xrightarrow{g} \hat{Y}$，然后构建 $Z$ 与 $\hat{Z}$ 并计算 $\mathcal{L}_{\alpha}$。
- **反向传播**：$\mathcal{L}_{\alpha}$ 对预测模型参数求梯度，驱动模型同时优化逐点精度与联合分布对齐。
- **输出**：训练后的预测模型 $g^*$，推理时仅需 $g$ 进行标准前向预测，无额外计算开销。

### 关键设计决策与理论支撑

DistDF 的 pipeline 设计由两条理论保证驱动：

- **上界关系（Lemma 3.3）**：联合分布 Wasserstein 差异是期望条件分布差异的上界，即 $\int \mathcal{W}_p(P_{Y|X}, P_{\hat{Y}|X}) dP(X) \leq \mathcal{W}_p(P_{X,Y}, P_{X,\hat{Y}})$。因此，最小化联合差异可间接约束条件分布对齐。
- **对齐保证（Theorem 3.4）**：当联合分布 Wasserstein 差异被最小化至零时，条件分布 $P_{Y|X}$ 与 $P_{\hat{Y}|X}$ 达到对齐。这为 DistDF 提供了绕过自相关偏差的理论基础。

### 与现有方法的本质区别

现有改进学习目标的方法（如 FreDF 的频域变换、Time-o1 的 PCA 变换）仅保证边缘去相关，条件自相关依然存在（Figure 1 证实了残留的条件相关性），因此偏差持续。DistDF 通过联合分布 Wasserstein 对齐直接针对条件分布差异，从根源上缓解自相关偏差问题。

### 局限性提示

DistDF 仅量化联合分布的一阶矩（均值）和二阶矩（协方差）差异，丢弃了预测与标签序列之间的逐元素对应关系。因此，$\mathcal{L}_{\mathrm{dist}}$ 独立作为损失函数时效果受限，通常需要与 MSE 结合作为正则项才能发挥最佳性能——消融实验中 $\alpha=1$（纯 BW 损失）的表现通常弱于 $\alpha<1$ 的设置。



### 自相关偏差的数学刻画

MSE损失函数将每个未来时间步视为独立预测任务，忽略了标签序列内部的自相关结构。这一忽略导致MSE成为真实负对数似然的有偏估计。定理3.1形式化了这一偏差：

$$
\mathrm{Bias} = \left\| Y_{|X} - \hat{Y}_{|X} \right\|_{\Sigma_{|X}^{-1}}^{2} - \left\| Y_{|X} - \hat{Y}_{|X} \right\|_{2}^{2}
$$

其中 $Y_{|X}$ 为给定历史 $X$ 条件下的标签序列，$\hat{Y}_{|X}$ 为预测序列，$\Sigma_{|X}$ 为条件协方差矩阵。偏差由马氏范数与欧氏范数之差给出：当 $\Sigma_{|X} \neq I$ 时，MSE偏离真实似然。Figure 1(a) 显示原始标签的条件相关性矩阵中超过50.3%的非对角元素超过0.1，证实了自相关结构的存在。

频域变换（FreDF）和主成分变换（Time-o1）仅保证边缘去相关（即 $\Sigma$ 对角化），而非条件去相关（$\Sigma_{|X}$ 对角化），因此偏差持续存在（Figure 1(b-c)）。

### 联合分布Wasserstein差异

为绕过条件协方差估计的困难，DistDF转而对齐预测与标签的联合分布。核心理论保证由以下两条建立：

**上界性质（Lemma 3.3）**：期望条件Wasserstein差异被联合分布Wasserstein差异上界控制：

$$
\int \mathcal{W}_p(\mathbb{P}_{Y|X}, \mathbb{P}_{\hat{Y}|X}) \, d\mathbb{P}(X) \leq \mathcal{W}_p(\mathbb{P}_{X,Y}, \mathbb{P}_{X,\hat{Y}})
$$

**对齐性质（Theorem 3.4）**：若联合分布Wasserstein差异最小化至零，则条件分布对齐，即 $\mathbb{P}_{Y|X} = \mathbb{P}_{\hat{Y}|X}$。

### Bures-Wasserstein闭式解

在高斯假设下，2-Wasserstein差异具有解析形式（Lemma 3.5），称为Bures-Wasserstein差异：

$$
\mathcal{BW}(\mu_{X,Y}, \mu_{X,\hat{Y}}, \Sigma_{X,Y}, \Sigma_{X,\hat{Y}}) = \left\| \mu_{X,Y} - \mu_{X,\hat{Y}} \right\|_{2}^{2} + \mathcal{B}(\Sigma_{X,Y}, \Sigma_{X,\hat{Y}})
$$

其中均值项衡量联合分布中心的对齐，协方差项由Bures度量给出：

$$
\mathcal{B}(\Sigma_{X,Y}, \Sigma_{X,\hat{Y}}) = \mathrm{Tr}\left( \Sigma_{X,Y} + \Sigma_{X,\hat{Y}} - 2\sqrt{\Sigma_{X,Y}^{1/2} \Sigma_{X,\hat{Y}} \Sigma_{X,Y}^{1/2}} \right)
$$

该公式将分布差异分解为均值差异与协方差差异两部分，且通过矩阵平方根运算实现可微、无偏的有限样本估计，可直接嵌入梯度优化训练。

### 组合损失函数

DistDF的最终训练目标将分布差异项与MSE加权组合：

$$
\mathcal{L}_{\alpha} := \alpha \cdot \mathcal{L}_{\mathrm{dist}} + (1 - \alpha) \cdot \mathcal{L}_{\mathrm{mse}}
$$

其中 $\mathcal{L}_{\mathrm{dist}}$ 即为Bures-Wasserstein差异，$\alpha \in [0,1]$ 控制分布对齐的强度。MSE项保留了逐元素对应关系，弥补了BW差异仅量化一阶矩和二阶矩差异而丢弃逐时间步对齐信息的局限。消融实验表明，均值对齐与协方差对齐具有协同效应，二者联合（DistDF）优于各自单独使用（Table 3）。



## 实验与关键发现

### 长期预测主结果

在8个主流时间序列数据集（ETT系列、ECL、Traffic、Weather、PEMS03、PEMS08）上，DistDF以TimeBridge为骨干网络，在绝大多数场景下取得最优或次优的MSE和MAE，显著优于直接预测（DF）基线及其他学习目标。

以Table 1的核心对比为例：在ETTm1上，DistDF将MSE从TimeBridge的0.394降至0.378（降低0.016）；在ETTh1上，从0.442降至0.430（降低0.012）；在ECL上，从0.176降至0.172；在Traffic上，从0.426降至0.417。这些提升在预测长度96至720的范围内保持稳定。

![[assets/figures/papers/iclr26_0009_VrdLwUmzBy_DistDF_Time-series_Forecasting_Needs_Joint-distr/figures/004_Table_1.jpg]]
*Table 1: Long-term forecasting performance*

DistDF的提升机制源于其绕过了MSE的自相关偏差瓶颈。MSE将每个未来时间步视为独立预测任务，忽略了标签序列的条件自相关结构，导致似然估计有偏（Theorem 3.1）。Figure 1(a)显示，原始标签的条件相关矩阵中超过50.3%的非对角元素绝对值超过0.1，表明自相关不可忽略。而DistDF通过最小化联合分布Wasserstein差异来对齐预测与标签的条件分布，从根源上缓解了这一偏差。

### 与现有学习目标的对比

Table 2将DistDF与FreDF（频域去相关）、Time-o1（PCA去相关）、Dilate（动态时间规整）等代表性学习目标进行对比。结果表明，DistDF在多个模型和数据集上一致优于这些方法。FreDF和Time-o1仅保证边缘去相关，条件自相关依然存在（Figure 1(b-c)），因此偏差持续。DistDF通过联合分布对齐直接处理条件分布差异，提供了更根本的解决方案。

![[assets/figures/papers/iclr26_0009_VrdLwUmzBy_DistDF_Time-series_Forecasting_Needs_Joint-distr/figures/008_Table_2.jpg]]
*Table 2: Comparative results with other objectives for time-series forecasting*

### 消融实验：均值与协方差对齐的协同效应

Table 3的消融实验拆分了DistDF的两个核心组件：

![[assets/figures/papers/iclr26_0009_VrdLwUmzBy_DistDF_Time-series_Forecasting_Needs_Joint-distr/figures/009_Table_3.jpg]]
*Table 3: Ablation study results*

- **DistDF†**：仅对齐联合分布的均值（省略Bures度量部分）
- **DistDF‡**：仅对齐联合分布的协方差（仅保留Bures度量部分）
- **DistDF**：同时对齐均值与协方差

在ETTm1上，DF基线MSE为0.387，DistDF†降至0.381，DistDF‡降至0.382，而完整的DistDF达到0.378。在ETTh1上，DF为0.447，DistDF†为0.435，DistDF‡为0.438，DistDF为0.430。这一模式在所有数据集上一致：单独对齐均值或协方差均能改善DF，但两者联合产生协同效应，取得最佳结果。这验证了联合分布匹配需要同时捕捉一阶矩和二阶矩差异。

### 损失权重α的敏感性分析

Table 5和Table 6展示了不同α值对TimeBridge和Fredformer性能的影响。核心发现是：α在较小的正值（0.001–0.1）范围内表现最佳，α=1（纯Bures-Wasserstein损失）通常弱于α<1的组合。例如，Fredformer在ECL上，α=0.01时MSE降低约0.01。这一现象与DistDF的局限性一致：BW损失仅量化均值与协方差差异，丢弃了预测与标签序列之间的逐元素对应关系，因此独立使用时效果受限，作为MSE的正则项才能发挥最佳性能。

### 预测序列可视化

Figure 2展示了DF与DistDF在ETTm1上的预测序列对比（历史长度H=96）。DistDF（红色）相比DF（蓝色）更好地捕捉了标签序列的细节变化，尤其在局部波动和趋势转折点处更为准确。这直观反映了联合分布对齐对预测质量的提升。

![[assets/figures/papers/iclr26_0009_VrdLwUmzBy_DistDF_Time-series_Forecasting_Needs_Joint-distr/figures/007_Figure_2.jpg]]
*Figure 2: The forecast sequence of DF (in blue) and DistDF (in red), with historical length H = 96*

### 训练过程监控

Figure 8展示了DistDF训练过程中各损失项和验证指标的演化曲线。BW损失（L_dist）在训练初期快速下降并趋于稳定，验证MSE和MAE同步改善，表明分布对齐损失有效引导了模型收敛。值得注意的是，L_dist的下降与验证指标的改善高度同步，验证了联合分布差异最小化与预测性能提升之间的因果关联。

### 跨模型泛化验证

Figure 3展示了DistDF应用于TimeBridge、Fredformer、iTransformer、FreTS四个不同架构模型时的性能提升（以MSE降低百分比表示，含50%置信区间）。DistDF在所有模型上均带来一致的正向提升，提升幅度最高达4.3%。这表明所提出的学习目标与具体模型架构解耦，具有广泛的适用性。

![[assets/figures/papers/iclr26_0009_VrdLwUmzBy_DistDF_Time-series_Forecasting_Needs_Joint-distr/figures/013_Figure_3.jpg]]
*Figure 3: Improvement of DistDF applied to different forecast models, shown with colored bars for means over forecast lengths (96, 192, 336, 720) and error bars for 50% confidence intervals*

### 失败模式与局限性

需要指出以下限制：

1. **逐元素对应关系的丢失**：DistDF仅量化联合分布的一阶矩和二阶矩差异，丢弃了预测与标签序列之间的逐时间步对应关系。这解释了为何纯BW损失（α=1）表现不佳——它无法约束逐个时间点的预测精度。

2. **高斯假设的局限**：Bures-Wasserstein公式依赖于高斯分布假设。在非高斯数据上，该度量仅捕捉均值与协方差差异，可能遗漏高阶分布结构。论文未提供非高斯场景下的理论保证。

3. **高维场景的计算开销**：协方差矩阵的矩阵平方根运算（Bures度量）在多元时序数据中可能面临计算瓶颈，论文未讨论高维场景下的近似策略。

### 扩展场景验证

附录中的Table 16和Table 17进一步验证了DistDF在自回归预测和概率预测设定下的有效性。在这些非标准DF场景中，DistDF依然稳定提升性能，表明联合分布对齐的思想具有跨任务迁移能力。但需注意，这些结果的置信度（0.9）略低于主要实验，建议在实际应用中针对具体任务进行验证。



## 定位与知识库关联

### 与现有方法的关系

DistDF 的核心差异在于将学习目标从逐点误差最小化转向条件分布对齐。传统直接预测（DF）方法统一采用 MSE 作为训练目标，其隐含假设是标签序列各时间步相互独立。Theorem 3.1 揭示，当标签存在自相关结构时（即条件协方差 $\Sigma_{|X} \neq I$），MSE 构成有偏的负对数似然估计，偏差量为 $\mathrm{Bias} = \| Y_{|X} - \hat{Y}_{|X} \|_{\Sigma_{|X}^{-1}}^2 - \| Y_{|X} - \hat{Y}_{|X} \|_2^2$。这一偏差在真实数据中普遍存在：Figure 1(a) 显示，预测长度为 192 时，原始标签的条件相关矩阵中超过 50.3% 的非对角元素绝对值超过 0.1。

近期工作试图通过变换缓解此问题，但与 DistDF 存在本质区别：

- **FreDF**（频域预测）：将标签变换到频域后施加 MSE，利用傅里叶基的正交性实现边缘去相关。然而，边缘去相关（$\Sigma$ 对角化）不等价于条件去相关（$\Sigma_{|X}$ 对角化）。Figure 1(b) 证实，FreDF 成分的条件相关矩阵仍存在显著的非对角残留。
- **Time-o1**（PCA 预测）：对标签序列施加主成分变换，同理仅保证边缘不相关。Figure 1(c) 显示其条件相关残留同样不可忽略。
- **Dilate**（DTW 软对齐）：关注预测与标签的形状相似性，但未涉及分布层面的偏差校正。
- **TimeBridge** 等 SOTA 模型：在架构层面（Transformer、频域增强、通道独立等）改进预测能力，但均沿用 MSE 作为训练目标，未解决自相关偏差这一根本瓶颈。

DistDF 不修改模型架构，而是在损失函数层面引入联合分布 Wasserstein 差异作为正则项：$\mathcal{L}_{\alpha} := \alpha \cdot \mathcal{L}_{\mathrm{dist}} + (1-\alpha) \cdot \mathcal{L}_{\mathrm{mse}}$。其理论基础是 Lemma 3.3 建立的联合分布 Wasserstein 差异对期望条件差异的上界关系，以及 Theorem 3.4 保证的最小化至零即可实现条件分布对齐。

### 适用边界

DistDF 的适用性受以下条件约束：

1. **高斯假设**：Bures-Wasserstein 闭式解（Lemma 3.5）依赖于联合分布的高斯近似。在此假设下，差异度量仅捕获一阶矩（均值）和二阶矩（协方差）的差异。对于具有显著高阶矩特征（如厚尾、多模态）的时序数据，该近似的保真度尚需验证。

2. **计算代价**：Bures 度量 $\mathcal{B}(\Sigma_{X,Y}, \Sigma_{X,\hat{Y}}) = \mathrm{Tr}(\Sigma_{X,Y} + \Sigma_{X,\hat{Y}} - 2\sqrt{\Sigma_{X,Y}^{1/2}\Sigma_{X,\hat{Y}}\Sigma_{X,Y}^{1/2}})$ 涉及矩阵平方根运算，其复杂度随序列长度和变量维度增长。在高维多元场景下，协方差矩阵的尺度可能成为计算瓶颈。

3. **正则项角色**：DistDF 独立作为损失函数时效果受限，需与 MSE 结合使用。消融实验（Table 3）表明，纯均值对齐（DistDF†）和纯协方差对齐（DistDF‡）均能改善 DF，但二者联合且与 MSE 加权时取得最佳结果。权重 $\alpha$ 在较小正值（0.001–0.1）时表现最优（Table 5, Table 6），$\alpha=1$（纯 BW）通常弱于 $\alpha<1$。

4. **逐元素对应关系的丢失**：DistDF 仅量化联合分布的一阶和二阶矩差异，丢弃了预测与标签序列之间的逐时间步对应关系。这使其更适合作为全局分布正则项，而非独立的预测精度度量。

### 局限与开放问题

**已知局限**：

- 丢弃逐元素对应关系，限制了其作为独立损失函数的有效性。
- 依赖高斯假设，在非高斯场景下的理论保证可能减弱。
- 仅建模前两阶矩，无法捕获分布的高阶结构差异。

**待探索的开放问题**：

1. **条件分布差异度量的设计**：如何构造既保留全局分布匹配优势、又兼顾逐时间步对齐的差异度量？这需要在联合分布 Wasserstein 差异的框架内引入某种形式的逐点惩罚或注意力机制。

2. **高维场景的高效近似**：当变量维度 $D$ 较大时，协方差矩阵为 $(H+T) \times D$ 维（$H$ 为历史长度，$T$ 为预测长度），Bures 度量的计算和存储开销显著。是否有低秩近似、随机化 SVD 或分块计算策略可以降低复杂度？

3. **非高斯扩展**：能否将框架推广至更一般的分布族？例如，使用切片 Wasserstein 距离或最大均值差异（MMD）替代 Bures-Wasserstein，可能放宽高斯假设但需重新建立条件对齐的理论保证。

4. **与架构设计的协同**：当前 DistDF 作为模型无关的损失函数插件，与具体架构解耦。是否存在与 DistDF 原理协同的架构设计（如显式建模条件协方差结构的预测头），可进一步放大分布对齐的收益？



## 原文 PDF

![[paperPDFs/ICLR_2026/DistDF_Time_series_Forecasting_Needs_Joint_distribution_Wasserstein_Alignment.pdf]]
