---
title: "Optimizing Data Collection for Machine Learning"
type: paper
paper_level: A
venue: NeurIPS
year: 2022
pdf_ref: paperPDFs/NEURIPS_2022/Optimizing_Data_Collection_for_Machine_Learning.pdf
code_link: null
project_link: https://research.nvidia.com/labs/toronto-ai/LearnOptimizeCollect/
aliases:
- LOCL
- ODCML
tags:
- NEURIPS_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "通过对最小数据需求量 D* 的分布进行建模（利用 Bootstrap 集成回归和密度估计），并在随机优化框架中直接利用该分布的不确定性进行决策，从而在收集成本与失败风险之间取得最优平衡。"
primary_logic: "将多轮数据采集视为一个部分可观测的随机序贯决策问题，不依赖单一点估计，而是通过估计 D* 的完整分布（PDF/CDF）并将期望总成本最小化。通过梯度下降求解此连续松弛的随机规划，LOC 能够在给定的失败风险下保守而高效地确定每一轮应采集的数据量。"
claims:
- "在 K=1 的 18 个实验设置中，LOC 在 12 个设置上的失败率低于 10%，而基于回归的基线方法在 15 个设置上的失败率超过 30%"
- "LOC 的成本比率在 12/18 的设置中始终低于 0.5，即其总成本最多仅比理论最低成本高出 50%"
- "在 CIFAR-100 上，T=1 时 LOC 将失败率从 56% 降至 4%，同时成本比的增加在可接受范围内；在 ImageNet、BDD100K 等任务上同样大幅降低失败率"
- "多变量设置（K=2）下，LOC 对不均匀的成本和不同的数据源表现出较强的鲁棒性，在 T>1 时保持低失败率且成本比接近 1"
---

# Optimizing Data Collection for Machine Learning

> [!tip] 核心洞察
> 将多轮数据采集视为一个部分可观测的随机序贯决策问题，不依赖单一点估计，而是通过估计 D* 的完整分布（PDF/CDF）并将期望总成本最小化。通过梯度下降求解此连续松弛的随机规划，LOC 能够在给定的失败风险下保守而高效地确定每一轮应采集的数据量。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 机器学习数据采集的优化 |
| 英文题名 | Optimizing Data Collection for Machine Learning |
| 会议/期刊 | NeurIPS 2022 |
| Links | [paper](https://arxiv.org/abs/2210.01234) · [Project](https://nv-tlabs.github.io/LearnOptimizeCollect/) · [Project](https://research.nvidia.com/labs/toronto-ai/LearnOptimizeCollect/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | Learn-Optimize-Collect (LOC) |
| Dataset | CIFAR-100 (classification), ImageNet (classification), BDD100K (segmentation) |

> [!tip] 效果简介
> - CIFAR-100 (classification) 上，Failure rate (T=1) 为 4%，对比 56% (Power Law Regression)，变化 -52%。
> - CIFAR-100 (classification) 上，Cost ratio (T=1) 为 0.99，对比 0.12 (Power Law Regression)，变化 +0.87。
> - ImageNet (classification) 上，Failure rate (T=5) 为 2%，对比 56% (Power Law Regression)，变化 -54%。

## 概要

机器学习系统对大规模标注数据的依赖日益加深，但数据采集的预算和时机往往依赖经验法则或简单的“越多越好”策略。传统方法通过外推神经网络的缩放定律来点估计所需数据量，然而外推误差极大，极易导致严重的数据过采或欠采，无法在采集初期就可靠地达到目标性能。

本文提出了一种全新的范式，将多轮数据采集工作流建模为一个**部分可观测的随机序贯决策问题**，并给出形式化的最优数据采集目标：在给定性能目标 $V^*$、收集成本 $c$、时间轮次 $T$ 和失败惩罚 $P$ 的条件下，最小化总成本与失败风险。核心洞察在于，不依赖单一点估计，而是通过对最小数据需求量 $D^*$ 的完整分布（PDF/CDF）进行建模，并在随机优化框架中直接利用该分布的不确定性进行决策。

基于此，作者开发了 **Learn-Optimize-Collect (LOC)** 方法。LOC 通过 Bootstrap 集成回归与核密度估计（或高斯混合模型）获得 $D^*$ 的分布 $F(q)$，然后将期望总成本最小化问题转化为可微分的连续优化问题，利用梯度下降求解每一轮应采集的数据量。该方法在单变量（$K=1$）和多变量（$K=2$）场景下均展现出显著优势：在 CIFAR-100、ImageNet、BDD100K、nuScenes 等多个分类、分割与检测任务上，LOC 将失败率从基线方法的 30%–62% 大幅降至接近 0%，同时成本比保持在理论最低成本的 1.5 倍以内。

**方法谱系与知识库定位**：LOC 的核心贡献在于将数据采集决策从“点估计 + 启发式修正”升级为“分布估计 + 随机优化”。与此前基于幂律回归（Power Law Regression, Mahmood et al.）及其手动校正因子的基线相比，LOC 在三个关键维度上进行了系统性改进：（1）**数据需求建模方式**从单一参数化函数外推变为 Bootstrap 集成 + 密度估计；（2）**决策优化问题**从直接求解点估计值变为最小化期望成本的随机规划；（3）**不确定性的利用**从完全忽略变为将 $D^*$ 的不确定性编码为分布 $F(q)$，使优化问题能自适应地平衡保守与激进。LOC 的回归模块可替换为对数回归、反正切回归、代数根回归等多种函数，展现出良好的方法泛化性。

**证据强度与边界**：决定性证据来自 18 个实验设置（Table 1）：LOC 在 12/18 设置上失败率低于 10%，而基线在 15/18 设置上失败率超过 30%；成本比在 12/18 设置中低于 0.5。多变量实验（Table 2, Figure 4）进一步验证了 LOC 在不均匀成本下的鲁棒性。然而，所有实验均建立在仿真的 ground truth 学习曲线之上，未在真实反复采集-训练环境中验证；多变量场景扩展到 $K>2$ 时计算开销极大；极端参数下可能产生不切实际的数据需求。此外，论文未涉及数据采集中的隐私、公平性约束以及验证集偏差问题，这些是实际部署中需要额外考虑的边界条件。



现代机器学习系统的性能高度依赖训练数据的规模。然而，数据采集本身是一项昂贵且不可逆的投入——标注成本、隐私合规、计算资源等因素使得“采集多少数据”成为一个关键的战略决策。实践中，项目方通常需要在有限的预算轮次内，逐步采集数据并迭代训练模型，直至模型性能达到预设的目标指标 $V^*$。

这一过程的根本困难在于：**在数据采集的早期阶段，我们无法准确预知究竟需要多少数据才能达到目标性能**。设 $D^*$ 为使模型性能首次达到 $V^*$ 的最小训练集规模，即停止时间 $D^* := \arg \min_q \{ q \mid V_q \geq V^* \}$。$D^*$ 本身是一个受模型架构、数据分布、优化算法等多重因素影响的随机变量，在采集完成之前是不可观测的。

现有方法几乎完全依赖**神经网络缩放定律**的外推来应对这一不确定性。具体而言，它们对已观测的学习曲线 $R_t$ 拟合一个参数化函数（最常用的是幂律模型 $\hat{v}(q; \pmb{\theta}) := \theta_0 q^{\theta_1} + \theta_2$），然后通过求解 $\hat{q} = \arg\min_q \{ q \mid \hat{v}(q; \pmb{\theta}) \geq V^* \}$ 来获得 $D^*$ 的单一点估计，并据此决定下一轮的数据采集量。部分工作（如 Mahmood et al.）进一步引入人工校正因子 $\tau$，将目标从 $V^*$ 上调为 $V^* + \tau$，以试图弥补外推的低估风险。

然而，这一范式存在一个根本性缺陷：**外推误差极大**。在数据量远未达到 $D^*$ 的早期轮次，学习曲线仅覆盖了极窄的观测窗口，任何参数化外推都面临严重的方差和偏差。单一点估计 $\hat{q}$ 完全无法刻画 $D^*$ 的真实不确定性，导致两种灾难性后果：
- **欠采**：$\hat{q}$ 远小于真实的 $D^*$，最终模型未能达标，项目失败；
- **过采**：$\hat{q}$ 远大于 $D^*$，采集了远超必要的数据，造成资源浪费。

这一瓶颈的本质在于：**传统方法将数据采集视为一个确定性外推问题，而非一个不确定性下的序贯决策问题**。它们没有对 $D^*$ 的完整分布进行建模，也无法在采集成本与失败风险之间进行系统性的权衡。因此，亟需一种新的框架，能够显式地利用 $D^*$ 分布中的不确定性，在给定的失败容忍度下，最小化期望总成本。



## 核心方法与创新机理

### 1. 问题建模范式的根本转变：从点估计到分布驱动的随机优化

传统方法（如 **Power Law Regression**，Mahmood et al.）的核心逻辑是：对已采集数据上的模型性能（学习曲线 $R$）拟合一个参数化函数（通常为幂律 $\hat{v}(q;\theta) = \theta_0 q^{\theta_1} + \theta_2$），然后通过外推求解满足目标性能 $V^*$ 的最小数据量 $\hat{D} = \arg\min_q \{ q \mid \hat{v}(q;\theta) \geq V^* \}$，并以此点估计作为下一轮采集量的决策依据。

这一范式存在一个根本性瓶颈：**外推误差的单点脆弱性**。由于学习曲线外推在数据稀缺的初期极不稳定，单一的点估计 $\hat{D}$ 可能严重偏离真实的最小数据需求量 $D^*$，导致两种系统性失败——过采（采集远超必要的数据，浪费成本）或欠采（采集不足，无法达到目标性能，触发失败惩罚）。

LOC 的核心创新在于**将决策对象从“一个点估计”升级为“一个完整的概率分布”**。具体而言，LOC 并不试图精确猜测 $D^*$ 是多少，而是通过 Bootstrap 集成回归和密度估计，构建 $D^*$ 的概率密度函数 $f(q)$ 和累积分布函数 $F(q)$，然后将整个分布嵌入到一个随机优化框架中，直接利用不确定性进行风险感知的决策。

这一转变的因果机制可以概括为：

- **传统范式**：学习曲线 → 单次回归拟合 → 点估计 $\hat{D}$ → 确定性采集量 → 外推误差直接转化为过采/欠采风险
- **LOC 范式**：学习曲线 → Bootstrap 集成回归 → $D^*$ 的分布 $F(q)$ → 随机优化求解最优采集量 → 不确定性被显式编码和利用，风险可控

### 2. 三个关键 changed slots 的技术细节

#### 2.1 数据需求建模方式：从单一点估计到 Bootstrap 集成分布估计

**Baseline 做法**：对学习曲线 $R$ 拟合单一参数化函数，求解 $\hat{D} = \arg\min_q \{ q \mid \hat{v}(q;\theta) \geq V^* \}$，得到一个标量估计。

**LOC 做法**（Section 4.2, Appendix E.3）：对 $R$ 进行 $B$ 次 Bootstrap 重采样，每次重采样后独立拟合回归函数（默认为幂律，但支持 Logarithmic、Arctan、Algebraic Root 等多种形式），得到 $B$ 个估计值 $\{\hat{D}_b\}_{b=1}^B$。随后通过核密度估计（KDE）或高斯混合模型（GMM）对这些样本进行密度估计，得到 $D^*$ 的概率密度函数 $f(q)$，并通过数值积分获得累积分布函数 $F(q)$。

**创新的本质**：这一做法将外推的不确定性从“隐藏的误差项”提升为“显式的概率分布”。Bootstrap 集成自然地捕捉了由于数据稀缺和模型选择导致的外推方差，而 KDE/GMM 则提供了平滑且可微的分布表示，为后续的梯度优化铺平了道路。Figure 5 和 Figure 6 直观展示了这一过程：Bootstrap 集成产生的学习曲线族（蓝色）覆盖了真实学习曲线（黑色）的合理变异范围，而 $D^*$ 的估计直方图则反映了外推不确定性的完整形态。

#### 2.2 决策优化问题：从确定性求解到期望成本最小化的随机规划

**Baseline 做法**：直接以 $\hat{D}$ 作为下一轮采集量，或辅以人工设计的校正因子 $\tau$（即以 $V^* + \tau$ 为目标进行外推），缺乏对不确定性的系统利用。

**LOC 做法**（Section 4.1, Equation 4）：构建并求解以下随机优化问题：

$$\operatorname*{min}_{q_1,\cdots,q_T} {c} \sum_{t=1}^{T} (q_t - q_{t-1}) (1 - F(q_{t-1})) + P (1 - F(q_T)) \quad \mathrm{s.t.} \ q_0 \leq q_1 \leq \cdots \leq q_T$$

其中 $1 - F(q_{t-1})$ 表示在第 $t-1$ 轮尚未达到目标性能（即 $D^* > q_{t-1}$）的概率，$(q_t - q_{t-1})(1 - F(q_{t-1}))$ 为第 $t$ 轮采集的期望成本，$P(1 - F(q_T))$ 为 $T$ 轮后仍未达标的期望惩罚。

**创新的本质**：这一目标函数将数据采集问题从“猜测一个正确数字”转变为“在不确定下做出最优序贯决策”。$F(q)$ 的引入使得优化器能够根据当前的失败概率自适应地权衡：当 $F(q_{t-1})$ 较低（即当前数据量很可能不足）时，$(1 - F(q_{t-1}))$ 较高，优化器倾向于采集更多数据以降低风险；反之，当 $F(q_{t-1})$ 已接近 1（即很可能已达标），进一步采集的期望收益递减，优化器会趋于保守。

#### 2.3 不确定性的利用：从忽视到显式编码与风险控制

**Baseline 做法**：未显式考虑 $D^*$ 的不确定性，单一点估计易受外推误差影响，导致失败率失控。

**LOC 做法**：将 $D^*$ 的不确定性完整编码在分布 $F(q)$ 中，使得优化问题能够根据失败概率自适应地选择保守或激进的收集量。这一机制在理论上有优雅的体现：**Theorem 1**（Section 5）证明，在单轮（$T=1$）设置下，当惩罚 $P$ 通过失败风险 $\epsilon$ 指定时，最优解恰好是 $D^*$ 分布的 $1-\epsilon$ 分位数：

$$q_1^* = F^{-1}(1 - \epsilon)$$

这意味着 LOC 在单轮场景下提供了一种**概率保证**：以 $1-\epsilon$ 的概率达到目标性能，而采集量恰好是满足该置信水平的最小值。这一性质将数据采集决策与统计置信度直接挂钩，使得设计者可以通过调节 $\epsilon$（或等价的 $P$）在成本与风险之间进行可解释的权衡。

在多轮（$T>1$）场景下，LOC 通过梯度下降（Momentum 或 Adam）求解连续松弛后的优化问题（Section B.3, Section D.2），利用 Gaussian softplus 变换消除非负约束，最后对最优解取整。这种连续松弛 + 梯度优化的策略使得 LOC 能够高效处理多轮序贯决策，同时保持对 $F(q)$ 的完整利用。

### 3. 创新间的因果关系与协同效应

上述三个 changed slots 并非孤立的技术改进，而是形成了一个**因果闭环**：

1. **分布估计**（Slot 1）为优化问题提供了输入——$F(q)$ 的质量直接决定了决策的质量；
2. **随机优化**（Slot 2）将 $F(q)$ 转化为风险感知的采集量——这是 LOC 区别于简单“取分位数”的关键，尤其在多轮场景下，优化器会考虑未来轮次的期望成本，做出更全局的权衡；
3. **不确定性利用**（Slot 3）是整个框架的理论内核——Theorem 1 揭示了单轮场景下的最优解结构，而多轮优化则是在此基础上的序贯扩展。

三者协同的结果是：LOC 能够在给定的失败风险下**保守而高效**地确定每一轮应采集的数据量。Table 1 的核心证据直接支撑了这一协同效应：在 $K=1$ 的 18 个实验设置中，LOC 在 12 个设置上的失败率低于 10%，而基于回归的基线方法在 15 个设置上的失败率超过 30%；同时，LOC 的成本比率在 12/18 的设置中始终低于 0.5，即总成本最多仅比理论最低成本高出 50%。这种“低失败率 + 低成本比”的组合是点估计方法难以同时实现的——后者要么因外推不足而频繁失败，要么因过度校正而成本飙升。

### 4. 多变量扩展的结构性创新

在 $K>1$ 的多数据源场景（Section 6），LOC 将单变量框架自然地推广到多变量随机优化：

$$\operatorname*{min}_{\mathbf{q}_1,\cdots,\mathbf{q}_T} {\mathbf{c}^{\top}} \sum_{t=1}^{T} (\mathbf{q}_t - \mathbf{q}_{t-1}) (1 - F(\mathbf{q}_{t-1})) + P (1 - F(\mathbf{q}_T)) \quad \mathrm{s.t.} \ \mathbf{q}_0 \leq \mathbf{q}_1 \leq \cdots \leq \mathbf{q}_T$$

其中 $\mathbf{c}$ 为不同数据源的成本向量，$F(\mathbf{q})$ 为多变量 $D^*$ 分布的 CDF。这一扩展的创新之处在于：它将不同成本和影响的数据源统一到同一个优化框架中，使得 LOC 能够自动学习“在便宜但低效的数据源上多采集”还是“在昂贵但高效的数据源上精准投入”之间的最优组合。Table 2 和 Figure 4 的结果表明，LOC 在不均匀成本和不同数据源下表现出较强的鲁棒性，在 $T>1$ 时保持低失败率且成本比接近 1。

**需要手动验证**：多变量场景下 $F(\mathbf{q})$ 的估计依赖加性幂律外推模型（如 $\hat{v}(q^1,q^2; \pmb{\theta}) = \theta_{1,0} (q^1)^{\theta_{1,1}} + \theta_{2,0} (q^2)^{\theta_{2,1}} + \theta_3$），论文未提供该模型在更复杂交互效应下的充分性证据，且构建高维 ground truth 需要 $O(\prod M_k)$ 次模型训练（见 limitations），实际可扩展性存疑。



LOC（Learn-Optimize-Collect）将多轮数据采集建模为一个**部分可观测的随机序贯决策问题**，其核心流程由三个循环执行的模块构成：性能统计收集、数据需求分布估计、随机优化问题求解，最终驱动实际的数据收集与模型更新。该框架的总体目标是在给定的失败风险容忍度下，最小化期望总收集成本。

### 问题形式化

在每一轮 $t$，我们拥有当前数据集 $\mathcal{D}_{q_{t-1}}$（大小为 $q_{t-1}$），需要决定本轮应采集的数据量 $q_t$（满足 $q_0 \leq q_1 \leq \cdots \leq q_T$）。最终模型在 $\mathcal{D}_{q_T}$ 上训练完成后，若性能未达到目标 $V^*$，则产生惩罚 $P$。全局优化目标为：

$$
\operatorname*{min}_{q_1,\ldots,q_T} \ c(q_T - q_0) + P \mathbb{1}\{V(\mathcal{D}_{q_T}) < V^*\} \ \mathrm{s.t.} \ q_0 \leq q_1 \leq \cdots \leq q_T
$$

其中 $c$ 为单位数据收集成本。定义**最小数据需求量** $D^*$ 为首次使模型性能达到 $V^*$ 的训练集大小：

$$
D^* := \arg \operatorname*{min}_q \{ q \mid V_q \geq V^* \}
$$

传统方法直接对学习曲线外推得到 $D^*$ 的点估计 $\hat{D}$，并以此决定收集量。由于外推误差极大（尤其在数据量较少时），容易导致严重的数据过采或欠采。LOC 的关键洞察在于：**不依赖单一点估计，而是对 $D^*$ 的完整分布进行建模，并在随机优化框架中利用该分布的不确定性进行决策**。

### Pipeline 模块

LOC 的每一轮迭代包含以下四个步骤（参见 Figure 1）：

**1. 性能统计收集**  
基于当前数据集 $\mathcal{D}_{q_{t-1}}$，通过子采样构建不同规模的训练集并训练模型，获得学习曲线 $R_t = \{(q_i, V_{q_i})\}_{i=1}^{n}$。这些统计量是后续分布估计的输入。

**2. 数据需求分布估计**  
对学习曲线 $R_t$ 进行 $B$ 次 Bootstrap 重采样，每次拟合一个回归函数（默认为幂律 $\hat{v}(q;\theta) = \theta_0 q^{\theta_1} + \theta_2$），得到一组 $D^*$ 的估计值 $\{\hat{D}_b\}_{b=1}^B$。随后通过核密度估计（KDE）或高斯混合模型（GMM）建模 $D^*$ 的概率密度函数 $f(q)$，并通过数值积分获得累积分布函数 $F(q)$。这一步骤将 $D^*$ 的不确定性完整编码在分布中，使得后续优化能够根据失败概率自适应地选择保守或激进的收集量。

**3. 随机优化问题求解**  
利用估计的 CDF $F(q)$，将原始问题转化为期望成本最小化问题（单变量情形）：

$$
\operatorname*{min}_{q_1,\cdots q_T} {c} \sum_{t=1}^{T} (q_t - q_{t-1}) (1 - F(q_{t-1})) + P (1 - F(q_T)) \ \mathrm{s.t.} \ q_0 \leq q_1 \leq \cdots \leq q_T
$$

其中 $(1-F(q_{t-1}))$ 表示在已收集 $q_{t-1}$ 数据后仍未达到目标的概率。该问题通过解除整数约束并使用 Gaussian softplus 变换消除非负约束后，采用动量或 Adam 梯度下降求解连续最优解，最后对结果取整得到 $q_t^*$。

**4. 数据收集与模型更新**  
根据求解出的 $q_t^*$ 实际采集数据，扩充训练集，重新训练或微调模型，并评估当前性能。若性能已达到 $V^*$，流程终止；否则进入下一轮迭代。

### 多变量扩展

当存在 $K$ 个不同成本和影响的数据源时，LOC 将决策变量推广为向量 $\mathbf{q}_t = (q_t^1, \ldots, q_t^K)$，成本向量为 $\mathbf{c}$，优化目标变为：

$$
\operatorname*{min}_{\mathbf{q}_1,\cdots,\mathbf{q}_T} {\mathbf{c}^{\top}} \sum_{t=1}^{T} (\mathbf{q}_t - \mathbf{q}_{t-1}) (1 - F(\mathbf{q}_{t-1})) + P (1 - F(\mathbf{q}_T)) \ \mathrm{s.t.} \ \mathbf{q}_0 \leq \mathbf{q}_1 \leq \cdots \leq \mathbf{q}_T
$$

其中 $F(\mathbf{q})$ 为多变量最小数据需求 $\mathbf{D}^*$ 的联合 CDF。此时回归模型需扩展为加性形式（如 $\hat{v}(q^1,q^2; \pmb{\theta}) = \theta_{1,0} (q^1)^{\theta_{1,1}} + \theta_{2,0} (q^2)^{\theta_{2,1}} + \theta_3$），以捕捉不同数据源对性能的独立贡献。

### 理论支撑

**定理 1（单轮最优解）**：当惩罚 $P$ 通过失败风险 $\epsilon$ 指定时，单轮问题的最优解为 $D^*$ 分布的 $1-\epsilon$ 分位数：

$$
q_1^* := F^{-1}(1 - \epsilon)
$$

这为 LOC 的单轮决策提供了严格的理论基础：在给定可接受的失败概率下，最优收集量恰好是 $D^*$ 分布的对应上分位数，无需依赖启发式校正因子。



LOC 框架将多轮数据采集视为一个部分可观测的随机序贯决策问题，其核心由三个模块串联构成，每个模块对应一个关键公式体系。

### 模块一：最小数据需求的形式化

问题的起点是将“达到目标性能所需的最少数据量”严格定义为一个停止时间。设 $V_q$ 为在训练集 $\mathcal{D}_q$（大小为 $q$）上模型的性能得分，$V^*$ 为预设的目标性能，则最小数据需求量 $D^*$ 定义为首次使 $V_q \geq V^*$ 的最小 $q$：

$$D^* := \arg \min_q \{ q \mid V_q \geq V^* \} \tag{2}$$

基于此，最优数据采集问题被形式化为在 $T$ 轮内最小化总成本与失败惩罚之和：

$$\min_{q_1,\ldots,q_T} \ c(q_T - q_0) + P \mathbb{1}\{V(\mathcal{D}_{q_T}) < V^*\} \quad \mathrm{s.t.} \ q_0 \leq q_1 \leq \cdots \leq q_T \tag{1}$$

其中 $c$ 为单位数据收集成本，$P$ 为未达到目标性能 $V^*$ 时的失败惩罚，$\mathbb{1}\{\cdot\}$ 为指示函数。该约束确保各轮数据量非递减。

### 模块二：数据需求分布估计

传统方法直接对学习曲线拟合单一参数化函数（如幂律 $\hat{v}(q;\theta) = \theta_0 q^{\theta_1} + \theta_2$），通过外推点估计 $\hat{D}$。由于外推误差极大，这种单一点估计极易导致过采或欠采。LOC 的核心改进在于对 $D^*$ 的完整分布进行建模。

具体而言，在每一轮 $t$，基于当前训练集 $\mathcal{D}_{q_{t-1}}$ 构建子采样集合并训练模型，获得学习曲线 $R_t$。随后进行 $B$ 次 Bootstrap 重采样，每次拟合回归函数得到一组估计值 $\{\hat{D}_b\}_{b=1}^B$。通过核密度估计（KDE）或高斯混合模型（GMM）对这些样本建模，得到 $D^*$ 的概率密度函数 $f(q)$，并通过数值积分获得累积分布函数 $F(q) = P(D^* \leq q)$。

### 模块三：随机优化问题求解

利用 $F(q)$，原始问题 (1) 可转化为期望成本最小化的随机规划问题。对于单变量（$K=1$）场景：

$$\min_{q_1,\cdots,q_T} \ c \sum_{t=1}^{T} (q_t - q_{t-1}) (1 - F(q_{t-1})) + P (1 - F(q_T)) \quad \mathrm{s.t.} \ q_0 \leq q_1 \leq \cdots \leq q_T \tag{4}$$

其中 $(1 - F(q_{t-1}))$ 表示在 $q_{t-1}$ 处仍未满足需求的概率，即第 $t$ 轮收集的增量数据 $(q_t - q_{t-1})$ 实际需要被支付的概率；$(1 - F(q_T))$ 为 $T$ 轮后仍失败的概率。

对于多变量场景（$K$ 个数据源，各有不同成本 $\mathbf{c} \in \mathbb{R}^K$），问题推广为：

$$\min_{\mathbf{q}_1,\cdots,\mathbf{q}_T} \ \mathbf{c}^{\top} \sum_{t=1}^{T} (\mathbf{q}_t - \mathbf{q}_{t-1}) (1 - F(\mathbf{q}_{t-1})) + P (1 - F(\mathbf{q}_T)) \quad \mathrm{s.t.} \ \mathbf{q}_0 \leq \mathbf{q}_1 \leq \cdots \leq \mathbf{q}_T \tag{7}$$

求解时，LOC 先解除整数约束，通过 Gaussian softplus 变换消除非负约束，使用动量或 Adam 梯度下降求解连续最优解 $\mathbf{d}_t^*$，最后对最优解取整得到实际收集量 $\mathbf{q}_t^*$。

### 定理 1：单轮最优解的解析形式

当 $T=1$ 且惩罚 $P$ 通过可接受的失败风险 $\epsilon$ 指定时，问题 (4) 退化为：

$$\min_{q_1} \ c(q_1 - q_0) + P(1 - F(q_1)) \quad \mathrm{s.t.} \ q_0 \leq q_1 \tag{5}$$

**定理 1** 给出了该情况下的最优解：当 $P$ 满足 $P = c / f(F^{-1}(1 - \epsilon))$ 时，最优解恰为 $D^*$ 分布的 $1-\epsilon$ 分位数：

$$q_1^* = F^{-1}(1 - \epsilon)$$

这一结果揭示了 LOC 的决策本质：不依赖单一点估计，而是根据可容忍的失败概率 $\epsilon$，直接从 $D^*$ 的分布中选择一个保守程度可控的分位数作为收集量。当 $\epsilon \to 0$ 时，$q_1^*$ 趋向于分布的右尾，确保高概率成功；当 $\epsilon$ 较大时，则允许更激进的收集策略以降低成本。



## 实验与关键发现

### 核心实验设置

论文在六个不同规模的视觉任务上评估 LOC，涵盖图像分类、语义分割、BEV 分割和目标检测（Table 4）。每个任务使用分段线性近似的“ground truth”学习曲线作为仿真环境，初始化数据量为全数据集的 10%（$q_0$）。主要基线为 **Power Law Regression**（Mahmood et al.），它直接对学习曲线拟合幂律函数并外推求解最小数据需求量 $D^*$。评估指标包括 **失败率**（最终未达到目标性能 $V^*$ 的比例）和 **成本比率**（实际收集成本相对于理论最低成本 $c(D^*-q_0)$ 的比值，越低越好）。默认参数固定 $c=1$，$P=10^7$（VOC 上 $P=10^6$，ImageNet 上 $P=10^8$），每组实验运行 5 个随机种子。

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2210_01234/figures/008_Table_4.jpg]]
*Table 4: Data sets, tasks, and score functions considered*

### 单变量数据采集（K=1）主结果

**Table 1** 汇总了 18 个实验设置（6 个数据集 × 3 个时间跨度 $T \in \{1,3,5\}$）的聚合失败率和成本比率。LOC 在 12/18 个设置上的失败率低于 10%，而基于回归的基线方法在 15/18 个设置上的失败率超过 30%。具体而言：

- **CIFAR-100**：$T=1$ 时，LOC 将失败率从 Power Law Regression 的 56% 降至 4%，成本比率从 0.12 升至 0.99——这意味着 LOC 以接近理论最低成本 1 倍的代价，换取了失败风险的近 14 倍降低。$T=3$ 时失败率进一步降至 2%，$T=5$ 时降至 0%。
- **ImageNet**：$T=5$ 时 LOC 将失败率从 56% 降至 2%，成本比率从 0.26 升至 0.75。
- **BDD100K（语义分割）**：$T=3$ 时 LOC 实现 0% 失败率，而基线失败率达 31%。
- **nuScenes（BEV 分割）**：$T=5$ 时 LOC 同样实现 0% 失败率，基线为 62%。

**Figure 2** 以散点图形式展示了不同 $V^*$ 下的数据收集比率 $q_T^*/D^*$。LOC 的数据收集量几乎始终略高于黑线（$q_T^*/D^*=1$），意味着它极少未能达到目标，而基线的收集量则频繁低于黑线，解释了其高失败率。

### 多变量数据采集（K=2）结果

多变量设置（Table 2, Figure 4）考察了两个数据源具有不同采集成本的情况。LOC 对不均匀的成本结构表现出较强的鲁棒性：当第一个数据源的成本 $c^1$ 逐步升高（从与 $c^2$ 相等升至 100 倍）时，LOC 在 $T=5$ 时维持接近 0 的失败率，且成本比率始终接近 1。相比之下，Power Law Regression 的失败率始终高于 30%，且成本比率波动剧烈。$T=1$ 时 LOC 的成本比率可能偏高（Figure 9, Figure 10），但引入多轮采集（$T>1$）后成本比率显著改善并低于基线。

### 消融实验

**回归函数的选择**（Table 6）：LOC 框架不依赖特定回归函数。在 CIFAR-100 上分别使用 Logarithmic、Arctan 和 Algebraic Root 回归替代默认的幂律回归，LOC 仍能大幅降低失败率（多数设置下失败率 ≤10%），且成本比率增长有限。这表明 LOC 的核心优势来自“对 $D^*$ 分布建模并优化期望成本”这一范式，而非特定外推函数的精度。

**与校正因子基线的对比**（Table 7）：Mahmood et al. 提出的带校正因子的幂律回归基线（通过手动调整目标 $V^* + \tau$ 来增加保守性）在 $T \geq 3$ 时，LOC 能以更低的成本达到同样低的失败率，成本降低幅度可达一个数量级。这验证了显式建模不确定性并通过优化求解的优势，优于启发式的校正策略。

### 参数敏感性

LOC 对成本参数 $c$ 和惩罚参数 $P$ 的变化具有较好的鲁棒性（Figure 3, Figure 7, Figure 8）。在 CIFAR-100 和 BDD100K 上扫描 $c$ 从 0.001 到 1，或 $P$ 从 $10^6$ 到 $10^9$，LOC 的数据收集比率和失败率保持相似量级。但在极端参数设置下（如 VOC 上 $P=10^9$），LOC 可能产生不切实际的大量数据需求（收集了 10000 倍于最低需求的数据量），实际部署时需要额外约束。

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2210_01234/figures/012_Figure_7.jpg]]
*Figure 7: Mean ± standard deviation of the ratio of data collected q _ { T } ^ { * } / D ^ { * } for different V ^ { * } when we sweep the cost parameter from 0.001 to 1 and fix P = 1 0 ^ { 7 } . We show T = 1 , 3 and refer to the main paper for T = 5 . The dashed black line corresponds to collecting exactly the minimum data requirement*

### 失败模式与局限性

1. **高维扩展瓶颈**：多变量（$K>2$）场景下，构建分段线性 ground truth 需要 $O(\prod M_k)$ 次模型训练，计算开销随数据源数量指数增长，当前框架难以直接扩展到高维场景。
2. **仿真环境的局限**：所有实验均建立在仿真的 ground truth 学习曲线之上，未在真实反复采集-训练的管线中验证。实际工作流中的噪声、延迟、模型版本迭代等因素可能影响 $D^*$ 分布估计的准确性。
3. **极端参数下的失控**：当惩罚参数 $P$ 设置过高时，LOC 可能因过度保守而收集远超需求的数据量，需引入硬性上限约束。
4. **公平性与隐私未建模**：论文未考虑数据采集中的子群体平衡、隐私损失等约束，所有实验假定独立同分布采样。

### 补充图表

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2210_01234/figures/010_Figure_5.jpg]]
*Figure 5: For a fixed seed, ground truth learning curves (black) and the estimated power law learning curves (blue) obtained via bootstrapping and ensembling. The shaded region represents the 95 percentile of the ensemble and the dashed blue line represents the mean of the regression functions. The mean is consistently higher than the unknown ground truth, whereas the shaded region can at times cover it*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2210_01234/figures/011_Figure_6.jpg]]
*Figure 6: For a fixed seed, the histogram of estimates of D ^ { * } from different bootstrapped models (blue bars), the estimated F ( q ) (orange curve), and the ground truth D ^ { * } (black dashed line). Each plot corresponds to a different V ^ { * } for CIFAR-100 (see Figure 5 for the learning curve). With higher targets, regression (i.e., collecting the mean of the distribution) will lead to larger under-estimations*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2210_01234/figures/003_Table.jpg]]

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2210_01234/figures/006_Table.jpg]]

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2210_01234/figures/007_Table_3.jpg]]
*Table 3: Table of notation used throughout paper*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2210_01234/figures/009_Table_5.jpg]]
*Table 5: Summary of hyperparameters used in our experiments*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2210_01234/figures/016_Table.jpg]]

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2210_01234/figures/017_Table_6.jpg]]
*Table 6: For experiments on CIFAR-100, average cost ratio $\mathbf { c } ^ { \mathsf { T } } ( \mathbf { q } _ { T } ^ { * } - \mathbf { q } _ { 0 }$ ) / $\mathbf { c } ^ { \mathsf { T } } ( \mathbf { D } ^ { * } - \mathbf { q } _ { 0 }$ ) - 1 and failure rate measured over a range of $V ^ { * }$ and T . We fix c = 1 and $\mathrm { \dot { \it P } }$ = 1 $0 ^ { 7 }$ . The best performing failure rate for each setting is bolded. The cost ratio is measured only for instances that achieve $V ^ { * }$ LOC consistently reduces the average failure rate, almost consistently down to 0%



## 定位与知识库关联

### 核心瓶颈与因果机制

传统数据采集策略的核心瓶颈在于：仅通过对神经网络缩放定律（neural scaling laws）进行外推来获得最小数据需求量 $D^*$ 的单一点估计。由于外推误差极大——尤其是在小样本初期——这种点估计极易导致严重的**数据过采**（over-collection，浪费成本）或**数据欠采**（under-collection，无法达到目标性能 $V^*$）。论文的实验证据表明，基于幂律回归（Power Law Regression）的基线方法在 15/18 个实验设置上的失败率超过 30%，而 LOC 在 12/18 个设置上将失败率控制在 10% 以下（Table 1），这直接验证了“点估计+外推”范式的根本脆弱性。

LOC 的因果调节变量（causal knob）在于：**将 $D^*$ 的不确定性完整编码为一个概率分布**，并在随机优化框架中利用该分布进行风险感知的决策。具体而言，LOC 通过对学习曲线 $R$ 进行 Bootstrap 重采样、集成多个回归函数（如幂律）来生成 $D^*$ 的样本集 $\{\hat{D}_b\}$，再通过核密度估计（KDE）或高斯混合模型（GMM）建模其 PDF $f(q)$ 和 CDF $F(q)$。这一分布完整捕获了外推误差的结构，使得优化问题能够根据失败概率自适应地选择保守或激进的收集量——这正是传统基线完全缺失的机制。

### 与基线方法的关系

论文将 LOC 与以下基线进行了系统对比：

1. **Power Law Regression**（Mahmood et al.）：直接对学习曲线拟合幂律函数 $\hat{v}(q;\theta) = \theta_0 q^{\theta_1} + \theta_2$，外推后求解 $\hat{D} = \arg\min_q \{ q \mid \hat{v}(q) \geq V^* \}$。该方法是数据需求估计领域的标准做法，但完全忽略了外推不确定性。

2. **Power Law Regression with Correction Factor**（Mahmood et al.）：在上述幂律回归基础上，引入人工设计的校正因子 $\tau$，将目标从 $V^*$ 提升至 $V^* + \tau$ 以降低失败风险。这是该领域最强的启发式基线，但校正因子的选择缺乏理论指导，且无法在多轮设置中动态调整。

3. **Logarithmic / Arctan / Algebraic Root Regression**：作为替代的参数化回归函数，用于验证 LOC 框架对底层回归模型选择的鲁棒性。

LOC 相对于这些基线的根本区别在于**决策范式的转变**：基线方法遵循“估计-求解”的两步范式（先点估计 $D^*$，再据此采集），而 LOC 将多轮数据采集建模为**部分可观测的随机序贯决策问题**，直接在 $F(q)$ 上最小化期望总成本。这一转变使得 LOC 能够：
- 在 $T=1$ 时，根据 Theorem 1 直接输出 $D^*$ 分布的 $1-\epsilon$ 分位数，从理论上保证失败概率不超过 $\epsilon$；
- 在 $T>1$ 时，通过梯度下降求解连续松弛的随机规划，动态权衡“当前轮多采以降低未来失败风险”与“保守采集以节省成本”。

消融实验（Table 6）表明，LOC 框架可使用 Logarithmic、Arctan、Algebraic Root 等多种回归函数来估计 $D^*$ 分布，仍能大幅降低失败率且成本增长有限，验证了框架对底层回归模型选择的鲁棒性。与带校正因子的幂律回归对比（Table 7），LOC 在 $T \geq 3$ 时能以更低的成本达到同样低的失败率，成本减少可达一个数量级。

### 适用边界

LOC 框架的适用边界由以下关键假设和限制定义：

1. **独立同分布采样假设**：所有实验均假定数据从固定分布中独立同分布采样，未考虑分布偏移、概念漂移或主动学习场景下的非独立采样。

2. **单目标性能优化**：LOC 仅优化单一标量性能指标 $V^*$，当存在多个冲突的性能指标（如准确率 vs. 公平性）时需要扩展。

3. **仿真 ground truth 学习曲线**：论文所有实验均建立在分段线性近似的仿真 ground truth 学习曲线之上（Section 7.1），未在真实反复采集-训练-评估的工业管线中验证。实际工作流中的噪声、训练随机性、验证集偏差等因素可能进一步影响 $D^*$ 分布估计的精度。

4. **多变量可扩展性有限**：当数据源数量 $K > 2$ 时，构建高维分段线性 ground truth 需要 $O(\prod M_k)$ 次模型训练，计算开销极大。论文仅在 $K=2$ 的 CIFAR-100 双子集和 BDD100K 半监督场景上验证了多变量 LOC。

5. **极端参数敏感性**：在某些极端参数设置下（如 VOC 上 $P=10^9$），LOC 可能产生不切实际的大量数据需求（收集了 10000 倍最低需求），实际部署时需要额外约束或更精细的参数调优。

### 局限与开放问题

**已知局限**（论文明确讨论或实验揭示）：

- 多变量场景的可扩展性瓶颈：高维 ground truth 构建的计算成本随数据源数量指数增长。
- 仿真环境的验证差距：未在真实采集-训练循环中验证，可能低估实际噪声和延迟的影响。
- 隐私与公平性缺失：未考虑数据采集中的隐私损失约束或群体公平性约束，无法防止对特定子群体的过采样或欠采样。
- 验证集偏差：所有实验假定验证集能无偏估计真实性能 $V_q$，但实际中验证集自身的选择偏差会影响 $D^*$ 估计。

**开放问题**（值得后续工作探索的方向）：

1. **与先进多变量缩放定律的结合**：当前 LOC 使用加性幂律模型（$\hat{v}(q^1,q^2) = \theta_{1,0}(q^1)^{\theta_{1,1}} + \theta_{2,0}(q^2)^{\theta_{2,1}} + \theta_3$）进行多变量外推，能否与更先进的非加性神经缩放定律结合，进一步提高 $D^*$ 分布估计精度？

2. **约束扩展**：能否将隐私预算（如差分隐私的 $\epsilon$ 约束）、群体公平性约束（如各子群体性能差距上界）直接纳入优化问题（4）或（7），形成统一的约束随机优化框架？

3. **在线学习与增量更新**：在真实工业多轮采集-训练管线中，如何高效更新 $D^*$ 分布（增量 Bootstrap 或贝叶斯更新）并求解优化问题，而无需每轮重复完整训练？

4. **动态目标与多目标扩展**：当目标性能 $V^*$ 在项目进行中动态变化，或存在多个冲突的性能指标时，应如何扩展 LOC 框架以支持帕累托最优的数据采集策略？

5. **主动采样与非独立同分布**：能否将 LOC 与主动学习或重要性采样结合，在非独立同分布采样下进一步降低数据需求？



## 原文 PDF

![[paperPDFs/NEURIPS_2022/Optimizing_Data_Collection_for_Machine_Learning.pdf]]
