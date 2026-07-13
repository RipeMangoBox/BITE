---
title: "Topological Anomaly Quantification for Semi-supervised Graph Anomaly Detection"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Topological_Anomaly_Quantification_for_Semi_supervised_Graph_Anomaly_Detection.pdf
project_link: null
code_link: null
openreview_forum_id: ZURYrJgigi
aliases:
- TG
- TAQSSGAD
tags:
- ICLR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: "TAQ-GAD 通过拓扑异常量化模块（TAQ）中的节点边界分数（NBS）与代理隔离分数（PIS）从图拓扑角度定量衡量节点异常程度，并利用拓扑异常增强模块（TAE）动态生成虚拟异常中心及增强拓扑连接，从而系统性地提升伪异常质量。"
primary_logic: "利用图拓扑结构信息（边界程度与隔离程度）量化节点异常倾向，可以精准筛选高置信度的伪异常节点；再通过风险导向的伪标签修正与异常中心增强，能够使模型学到更具判别力的节点表征，显著提升仅用正常标签的半监督异常检测性能。"
claims:
- "设计两个拓扑指标 NBS 和 NIS/PIS 量化节点异常程度，NBS 衡量与标记正常邻居的连接稀疏性，NIS/PIS 衡量结构隔离性。"
- "TAE 模块基于节点预测置信度动态生成虚拟异常中心点并构造它们与其他节点的拓扑关系，显著提升模型异常识别性能。"
- "TAQ-GAD 在五个数据集上与 GGAD 相比 AUROC 和 AUPRC 均有显著提升（Amazon 0.9474, T-Finance 0.8675, Reddit 0.6682, Elliptic 0.7453, Photo 0.7107）。"
- "在 DGraph 数据集的不同标记率下，TAQ-GAD 均一致地优于 GGAD（0.5%标记率下 AUROC 0.6623 vs 0.5940，AUPRC 0.0162 vs 0.0083）。"
---

# Topological Anomaly Quantification for Semi-supervised Graph Anomaly Detection

> [!tip] 核心洞察
> 利用图拓扑结构信息（边界程度与隔离程度）量化节点异常倾向，可以精准筛选高置信度的伪异常节点；再通过风险导向的伪标签修正与异常中心增强，能够使模型学到更具判别力的节点表征，显著提升仅用正常标签的半监督异常检测性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于拓扑异常量化的半监督图异常检测 |
| 英文题名 | Topological Anomaly Quantification for Semi-supervised Graph Anomaly Detection |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ZURYrJgigi) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | TAQ-GAD |
| Dataset | Amazon, T-Finance |

> [!tip] 效果简介
> - Amazon 上，AUROC 为 0.9474，对比 0.9188，变化 +0.0286。
> - Amazon 上，AUPRC 为 0.7973，对比 0.7403，变化 +0.0570。
> - T-Finance 上，AUROC 为 0.8675，对比 0.8452，变化 +0.0223。

## 概要

在半监督图异常检测中，现有生成式方法（如特征插值与噪声扰动）普遍缺乏对节点异常程度的定量评估机制，导致生成的伪异常节点代表性差、可靠性低，难以有效模拟真实世界中复杂的异常模式。针对这一瓶颈，本文提出 TAQ-GAD，一种基于拓扑异常量化的生成式图异常检测方法。

TAQ-GAD 的核心思路是：利用图拓扑结构信息（边界程度与隔离程度）量化节点的异常倾向，从而精准筛选高置信度的伪异常节点；再通过风险导向的伪标签修正与异常中心增强，使模型学到更具判别力的节点表征，在仅使用正常标签的半监督设置下显著提升异常检测性能。

方法由两个关键模块构成：**拓扑异常量化模块（TAQ）** 通过节点边界分数（NBS）与代理隔离分数（PIS）从拓扑角度定量衡量节点异常程度；**拓扑异常增强模块（TAE）** 基于节点预测置信度动态生成虚拟异常中心，并概率性地构造节点与中心之间的拓扑连接，系统性地提升伪异常质量。

在五个基准数据集（Amazon、T-Finance、Reddit、Elliptic、Photo）上，TAQ-GAD 相较主要对比方法 GGAD 在 AUROC 和 AUPRC 上均取得显著提升，例如 Amazon 上 AUROC 达 0.9474（+2.86%），Elliptic 上 AUPRC 提升 11.48 个百分点。在 DGraph 数据集的不同标记率下，TAQ-GAD 同样一致优于 GGAD。消融实验证实，NBS、PIS 与 TAE 三个组件均对性能有正向贡献，且拓扑引导的采样策略明显优于随机采样和低度采样策略。



图异常检测（Graph Anomaly Detection, GAD）在金融欺诈识别、社交网络虚假信息检测、网络入侵发现等现实场景中具有重要应用价值。其核心任务是在属性图中识别出与大多数节点在特征或拓扑结构上显著偏离的异常节点。近年来，半监督图异常检测方法因能够利用少量标记数据提升检测精度而受到广泛关注，其中基于生成式范式的 GGAD 等方法通过构造伪异常节点来弥补真实异常标签不足的问题。

然而，现有生成式方法存在一个关键瓶颈：**缺乏对节点异常程度的定量评估机制**。当前主流的伪异常生成策略——如特征插值、随机噪声扰动或表示置换——本质上是在特征空间中进行启发式操作，并未利用图拓扑结构所蕴含的丰富判别信息。这导致生成的伪异常节点代表性差、可靠性低，难以有效模拟真实世界中复杂多样的异常模式。具体而言，真实异常节点往往表现出特定的拓扑特征：它们可能位于正常节点簇的边界地带（与标记正常节点连接稀疏），也可能在图中处于结构隔离状态（与同类节点距离遥远）。若伪异常生成过程无法捕捉这些拓扑信号，模型就难以学到具有判别力的异常表征。

针对上述缺口，TAQ-GAD 的核心动机是：**利用图拓扑结构信息定量衡量节点的异常倾向，从而精准筛选高质量的伪异常节点**。通过设计能够刻画边界程度与隔离程度的拓扑指标，可以系统性地提升伪异常质量；在此基础上，进一步通过风险导向的伪标签修正与异常中心增强，使模型在半监督训练中获得更强的异常识别能力。这一思路将伪异常生成从特征空间拓展到拓扑空间，为仅使用正常标签的半监督图异常检测提供了新的技术路径。



## 核心方法与创新机理

TAQ‑GAD 的核心创新在于**将图拓扑结构信息显式地量化为节点的异常倾向，并以此驱动伪异常生成与拓扑增强**，从而系统性地突破了现有生成式图异常检测方法的瓶颈。

### 瓶颈与突破点

现有生成式方法（如 GGAD、DAGAD）普遍采用**随机噪声扰动或特征插值**来构造伪异常节点。这类策略缺乏对节点异常程度的定量评估，导致生成的伪异常代表性差、可靠性低，无法有效模拟真实世界中复杂的异常模式。TAQ‑GAD 的因果性突破在于：**利用图拓扑结构（边界程度与隔离程度）作为异常倾向的信号源**，实现了从“盲目生成”到“拓扑引导生成”的范式转变。

### 关键机制变更（Changed Slots）

以下三个模块构成了 TAQ‑GAD 相对于基线方法的核心变更：

| 变更槽位 | 基线做法 | TAQ‑GAD 做法 | 证据锚点 |
|---------|---------|-------------|---------|
| 伪异常生成机制 | 随机噪声扰动或特征插值（GGAD 的异常先验约束、DAGAD 的表示置换） | 基于拓扑异常量化指标 NBS 与 PIS 的加权得分，筛选高得分标记正常节点作为伪异常 | *“Based on the Score(v_i), we rank all labeled nodes and select the top τ-proportion of highest-scoring nodes as pseudo-anomaly nodes”* |
| 图增强与标签修正 | 无虚拟异常中心或基于简单规则的标签修正 | TAE 模块通过风险估计与标签翻转策略动态生成虚拟异常中心，并概率性地构造节点‑中心连边，增强异常子图拓扑一致性 | *“The TAE module refines graph structure by strengthening connectivity between anomalous nodes and anomaly centroids ... we implement a label flipping strategy ... construct an augmented graph G^{new}”* |
| 训练目标 | 通常仅使用分类损失（如交叉熵） | 联合正则化损失与分类损失的组合训练目标 | *“L_total = α · L_reg + β · L_cls”* |

### 创新一：拓扑异常量化（TAQ 模块）

TAQ 模块从**边界性**和**隔离性**两个维度量化节点的异常倾向：

- **节点边界分数（NBS）** 衡量节点与标记正常邻居的连接稀疏性：
  $$\mathrm{NBS}(v_i) = 1 - \frac{|\mathcal{N}(v_i) \cap \mathcal{V}_l|}{|\mathcal{N}(v_i)|}$$
  NBS 越高，节点越可能处于正常区域边界，异常倾向越强。

- **代理隔离分数（PIS）** 在缺失异常标签的情况下替代 NIS，同时捕获局部聚类密度和度惩罚：
  $$\mathrm{PIS}(v_i) = 1 - \frac{1}{2} \left( \frac{|E(\mathcal{N}(v_i))|}{\binom{d_i}{2} + \epsilon} + \frac{\log(d_i + e)}{D + 1} \right)$$
  PIS 越高，节点及其邻域越稀疏、越隔离。

两者通过加权和 $\mathrm{Score}(v_i) = \lambda_1 \mathrm{NBS}(v_i) + \lambda_2 \mathrm{PIS}(v_i)$ 综合评估拓扑异常程度，据此选取顶部 τ 比例的标记正常节点作为伪异常。消融实验（Table 3）证实：**NBS 与 PIS 的组合效果优于任一单独指标**，验证了边界性与隔离性信号的互补性。

### 创新二：拓扑异常增强（TAE 模块）

TAE 模块在伪异常生成后进一步**修正伪标签并增强异常拓扑结构**：

1. **风险驱动的标签翻转**：基于预测不确定性与类别平均不确定性的差值计算风险得分 $r(v_i) = \max(0, u(v_i) - \bar{u}_{\hat{y}_i}) \times w_{\hat{y}_i}$，对高风险节点根据邻域类别分布 $p_{v_i}^{\mathrm{post}(c)}$ 进行标签翻转，修正不可靠的伪标签。

2. **虚拟异常中心生成与拓扑连接**：动态生成虚拟异常中心节点，并以概率 $P(v_i, v_c^{\mathrm{virtual}}) = r(v_i) \cdot p_{v_i}^{\mathrm{post}(c)} \cdot (\mathbf{1} - \mathbb{I}[\hat{y}_i = c])$ 在节点与中心之间构造连边，增强异常节点间的拓扑关联。

消融实验（Table 3）表明：**在 NBS+PIS 基础上添加 TAE 模块后，所有数据集上的性能均达到最高**，证明 TAE 对拓扑异常增强的有效性。

### 创新三：拓扑引导的采样策略

TAQ‑GAD 的拓扑引导采样策略（Topology‑guided）在 AUROC 和 AUPRC 上均一致优于随机采样（Random）和低度节点采样（Low‑degree）策略（Table 4）。例如在 Reddit 数据集上，TAQ‑GAD 的 AUROC 达到 0.6682，而随机采样和低度采样分别为 0.5443 和 0.5579，差距显著。这证明**拓扑结构蕴含的异常信号远强于简单的度启发式或随机选择**。

### 整体效能

上述创新的协同效应使 TAQ‑GAD 在五个数据集上相较最强基线 GGAD 均取得显著提升（Table 1），尤其在 Elliptic 数据集上 AUPRC 提升达 +0.1148（0.3573 vs 0.2425），在 DGraph 的 0.5% 标记率下 AUROC 提升 +0.0683（Table 2）。这些结果表明，**拓扑引导的伪异常生成与增强机制能够使模型在仅用正常标签的半监督设置下学到更具判别力的节点表征**。



![[assets/figures/papers/iclr26_0011_ZURYrJgigi_Topological_Anomaly_Quantification_for_Semi-supe/figures/001_Figure_1.jpg]]
*Figure 1: The overall framework of TAQ-GAD*

TAQ-GAD 的整体设计遵循一个两阶段的半监督异常检测范式，核心目标是仅利用少量正常标签生成高质量的伪异常节点，并通过拓扑增强提升模型对异常模式的判别能力。其 pipeline 由三个关键模块串联构成：**拓扑异常量化模块（TAQ）**、**拓扑异常增强模块（TAE）** 和最终的**图神经网络分类器**。

### 阶段一：伪异常生成

输入为一张包含少量标记正常节点和大量未标记节点的图。TAQ 模块首先对每个节点计算两个拓扑指标——**节点边界分数（NBS）** 和**代理隔离分数（PIS）**。NBS 衡量节点与标记正常邻居的连接稀疏性，PIS 在缺失异常标签的条件下作为结构隔离性的替代度量。两者通过加权求和得到综合异常得分：

$$\mathrm{Score}(v_i) = \lambda_1 \mathrm{NBS}(v_i) + \lambda_2 \mathrm{PIS}(v_i)$$

基于该得分对所有标记正常节点进行排序，选取顶部 $\tau$ 比例的最高分节点作为伪异常节点，从而将拓扑上更可能位于正常区域边界或结构上更孤立的节点筛选出来。这一策略从图拓扑角度提供了对节点异常程度的定量评估，解决了传统随机扰动或特征插值方法无法精准筛选伪异常的问题。

### 阶段二：拓扑增强与联合训练

筛选出的伪异常节点与原始正常节点一同送入 GNN 进行初步预测。TAE 模块在此阶段介入，执行两个关键操作：

1. **风险驱动的伪标签修正**：计算每个节点的风险得分 $r(v_i)$，该得分基于预测不确定性 $u(v_i)$ 与类别平均不确定性的差值，并经类别权重缩放。对于高风险节点，结合其邻域类别分布 $p_{v_i}^{\mathrm{post}(c)}$ 执行标签翻转策略，修正不可靠的伪标签。

2. **虚拟异常中心增强**：基于修正后的伪标签动态生成虚拟异常中心节点，并按照连接概率 $P(v_i, v_c^{\mathrm{virtual}})$ 在节点与中心之间概率性地构造连边。这一操作显式增强了异常节点之间的拓扑联系，使异常子图的结构更加一致，为 GNN 提供更强的判别信号。

增强后的图结构 $\mathcal{G}^{\mathrm{new}}$ 融合了正常节点、修正后的伪异常节点以及虚拟异常中心，最终送入 GNN 分类器进行半监督训练。训练目标为联合损失：

$$\mathcal{L}_{\mathrm{total}} = \alpha \cdot \mathcal{L}_{\mathrm{reg}} + \beta \cdot \mathcal{L}_{\mathrm{cls}}$$

其中 $\mathcal{L}_{\mathrm{reg}}$ 为正则化损失，$\mathcal{L}_{\mathrm{cls}}$ 为分类损失，二者加权组合以平衡模型约束与判别能力。

### 模块间关系

三个模块的依赖关系清晰且单向：TAQ 的输出（伪异常节点集合）是 TAE 的输入基础；TAE 在此基础上修正伪标签并增强图拓扑；增强后的图直接供给 GNN 分类器进行最终预测。整个流程无需真实异常标签参与伪异常的筛选与增强，仅在最终训练阶段利用少量正常标签进行监督，属于典型的半监督生成式异常检测框架。



### 问题瓶颈与设计动机

现有生成式图异常检测方法（如 GGAD 的特征插值与噪声扰动）在生成伪异常节点时，缺乏对节点异常程度的定量评估机制。这导致生成的伪异常节点代表性差、可靠性低，无法有效模拟真实场景中复杂多样的异常模式。TAQ-GAD 的核心思路是：**利用图拓扑结构信息（边界程度与隔离程度）量化节点异常倾向，精准筛选高置信度的伪异常节点；再通过风险导向的伪标签修正与异常中心增强，使模型学到更具判别力的节点表征。**

### 拓扑异常量化模块（TAQ）

TAQ 模块从图拓扑角度定量衡量节点的异常程度，设计了两个互补的拓扑指标：节点边界分数（NBS）和节点隔离分数（NIS）/代理隔离分数（PIS）。

**节点边界分数（NBS）** 衡量节点与标记正常邻居的连接稀疏性。直觉上，处于正常区域边界的节点与已标记正常节点的连接较少，更可能具有异常倾向。其定义为：

$$\mathrm{NBS}(v_i) = 1 - \frac{|\mathcal{N}(v_i) \cap \mathcal{V}_l|}{|\mathcal{N}(v_i)|}$$

其中 $\mathcal{N}(v_i)$ 为节点 $v_i$ 的 $K$ 跳邻域（实验中使用 $K=2$），$\mathcal{V}_l$ 为已标记正常节点集合。NBS 值越高，表示该节点邻域中标记正常节点占比越低，边界程度越强，异常倾向越大。

**节点隔离分数（NIS）** 衡量节点在其所属类别内部的结构隔离性。其定义为节点到同类别其他节点的平均最短路径长度：

$$\mathrm{NIS}(v_i) = \frac{1}{|\mathcal{N}_s(v_i)|} \sum_{v_j \in \mathcal{N}_s(v_i)} \mathrm{path}(v_i, v_j)$$

其中 $\mathcal{N}_s(v_i)$ 表示与 $v_i$ 同类的其他节点集合，$\mathrm{path}(v_i, v_j)$ 为两节点间的最短路径长度。NIS 值越高，表示节点在其类别内部越孤立，异常可能性越大。然而，在半监督设置下异常标签不可用，NIS 无法直接计算。

**代理隔离分数（PIS）** 作为 NIS 的替代指标，同时考虑局部聚类密度和度惩罚：

$$\mathrm{PIS}(v_i) = 1 - \frac{1}{2} \left( \frac{|E(\mathcal{N}(v_i))|}{\binom{d_i}{2} + \epsilon} + \frac{\log(d_i + e)}{D + 1} \right)$$

其中 $|E(\mathcal{N}(v_i))|$ 为节点 $v_i$ 邻域内的边数，$d_i$ 为节点度，$D$ 为图中最大节点度，$\epsilon$ 为小常数防止除零。第一项衡量邻域内的局部聚类密度——聚类越稀疏，节点越孤立；第二项为度惩罚项——高度节点通常连接更紧密，需施加惩罚。PIS 越高，表示节点及其邻域越稀疏、越隔离，异常可能性越大。

**综合异常得分** 将 NBS 与 PIS 加权求和，得到节点的拓扑异常量化得分：

$$\mathrm{Score}(v_i) = \lambda_1 \mathrm{NBS}(v_i) + \lambda_2 \mathrm{PIS}(v_i)$$

基于该得分对所有标记正常节点排序，选取顶部 $\tau$ 比例的最高分节点作为伪异常节点，用于后续模型训练。实验表明 $\tau$ 在 0.05 附近时性能达到峰值。

### 拓扑异常增强模块（TAE）

TAE 模块在 TAQ 生成的伪异常节点基础上，进一步通过风险估计与标签翻转策略生成虚拟异常中心，并概率性地构造节点-中心连边，增强异常子图的拓扑一致性。

**风险得分** 基于节点预测不确定性与类别平均预测不确定性的差值，经类别权重缩放后得到：

$$r(v_i) = \max\left(0, u(v_i) - \bar{u}_{\hat{y}_i}\right) \times w_{\hat{y}_i}$$

其中 $u(v_i)$ 为节点 $v_i$ 的预测不确定性（如预测概率的熵），$\bar{u}_{\hat{y}_i}$ 为预测类别 $\hat{y}_i$ 的平均不确定性，$w_{\hat{y}_i}$ 为类别权重（通常设为类别频率的倒数）。风险得分越高，表示该节点的伪标签越不可靠。

**邻域类别分布** 计算节点邻域内被预测为类别 $c$ 的节点比例，作为后验概率参与风险驱动的伪标签修正：

$$p_{v_i}^{\mathrm{post}(c)} = \frac{|\{v_j \in \mathcal{N}(v_i) : \hat{y}_j = c\}|}{|\mathcal{N}(v_i)|}$$

对于高风险节点（$r(v_i) > 0$），若其邻域在相反类别上表现出高置信度，则翻转该节点的伪标签。这一机制能够有效纠正 TAQ 阶段可能产生的伪标签错误。

**虚拟中心连接概率** 节点与虚拟异常中心之间建立连接的概率由风险得分、邻域类别分布和标签一致性综合决定：

$$P(v_i, v_c^{\mathrm{virtual}}) = r(v_i) \cdot p_{v_i}^{\mathrm{post}(c)} \cdot (\mathbf{1} - \mathbb{I}[\hat{y}_i = c])$$

其中 $\mathbb{I}[\hat{y}_i = c]$ 为指示函数，当节点已被预测为类别 $c$ 时该项为 0，避免自连接。该概率综合了三个信号：预测风险越高、邻域中类别 $c$ 占比越大、且节点当前标签与 $c$ 不一致时，连接概率越大。TAE 据此构造增强图 $G^{\text{new}}$，增强异常节点间的拓扑联系。

### 联合训练目标

TAQ-GAD 在增强后的图上融合正常节点与伪异常节点进行半监督训练，采用联合正则化损失与分类损失的组合目标：

$$\mathcal{L}_{\mathrm{total}} = \alpha \cdot \mathcal{L}_{\mathrm{reg}} + \beta \cdot \mathcal{L}_{\mathrm{cls}}$$

其中 $\mathcal{L}_{\mathrm{reg}}$ 为正则化损失（用于约束伪异常节点的表征分布），$\mathcal{L}_{\mathrm{cls}}$ 为分类损失（如交叉熵）。消融实验表明，联合使用两种损失在所有数据集上均优于仅使用分类损失，且模型对 $\alpha$ 和 $\beta$ 表现出较强的鲁棒性。

### 模块协同机制总结

TAQ 与 TAE 形成两阶段协同：TAQ 从图拓扑角度量化节点异常程度，筛选高置信度伪异常节点；TAE 在此基础上通过风险驱动的伪标签修正与虚拟中心增强，进一步提升伪异常质量。消融实验（Table 3）证明 NBS、PIS 和 TAE 三个模块均对性能有正向贡献，三者的组合在所有数据集上达到最优效果。



## 实验与关键发现

### 主实验结果

TAQ-GAD 在五个公开数据集上与多种无监督及半监督方法进行了对比，主要基线为 GGAD（生成式半监督图异常检测方法）。Table 1 报告了 AUROC 和 AUPRC 两项指标。TAQ-GAD 在所有数据集上均取得最优的半监督性能：

![[assets/figures/papers/iclr26_0011_ZURYrJgigi_Topological_Anomaly_Quantification_for_Semi-supe/figures/003_Table_1.jpg]]
*Table 1: Performance comparison of different GAD methods. We report GGAD and TAQ-GAD results under different label rates, with the highest scores bolded*

- **Amazon**：AUROC 0.9474（+2.86%），AUPRC 0.7973（+5.70%）。
- **T-Finance**：AUROC 0.8675（+2.23%），AUPRC 0.2255（+4.30%）。
- **Reddit**：AUROC 0.6682（+2.96%），AUPRC 0.0780（+0.87%）。
- **Elliptic**：AUROC 0.7453（+1.92%），AUPRC 0.3573（+11.48%）。
- **Photo**：AUROC 0.7107（+2.82%），AUPRC 0.2073（+2.72%）。

其中 Elliptic 数据集的 AUPRC 提升最为显著（+11.48%），表明 TAQ-GAD 在类别不平衡严重的场景下能更有效地提升异常检出精度。该增益的核心机制在于：TAQ 模块通过 NBS 和 PIS 从拓扑角度筛选出高置信度的伪异常节点，使模型在训练阶段接触到更具代表性的异常模式；TAE 模块进一步通过风险估计与标签翻转修正伪标签，并构造虚拟异常中心增强异常节点间的拓扑连接，从而强化了模型对异常子图结构的判别能力。

在 DGraph 数据集上的不同标记率实验（Table 2）进一步验证了方法的鲁棒性。在 0.5% 标记率下，TAQ-GAD 的 AUROC 为 0.6623，显著优于 GGAD 的 0.5940（+6.83%）；AUPRC 为 0.0162 vs 0.0083（+7.9%）。在其他标记率（0.05%、0.2%、0.35%）下，TAQ-GAD 同样一致优于 GGAD，说明拓扑引导的伪异常生成策略在标签极度稀疏时仍能保持稳定的性能增益。

![[assets/figures/papers/iclr26_0011_ZURYrJgigi_Topological_Anomaly_Quantification_for_Semi-supe/figures/004_Table_2.jpg]]
*Table 2: Performance comparison on DGraph dataset. We report GGAD (G) and TAQ-GAD (T) results under different label rates, with the highest scores bolded*

### 消融实验

Table 3 系统消融了 TAQ-GAD 各组件及损失函数的贡献：

![[assets/figures/papers/iclr26_0011_ZURYrJgigi_Topological_Anomaly_Quantification_for_Semi-supe/figures/005_Table_3.jpg]]
*Table 3: Ablation study results on different components of TAQ-GAD. We bold the highest scores*

**模块消融**：
- **+NBS**：在基线模型上仅添加 NBS 模块，所有数据集的 AUROC 和 AUPRC 均有提升，验证了边界分数对伪异常筛选的有效性。
- **+PIS**：单独添加 PIS 模块同样带来正向增益，且与 NBS 形成互补——NBS 捕获边界程度，PIS 捕获结构隔离程度。
- **+NBS+PIS**：联合使用两个指标的效果优于任一单独模块，证明二者从不同拓扑维度提供了互补的异常量化信号。
- **+NBS+PIS+TAE**（完整 TAQ-GAD）：在 NBS+PIS 基础上加入拓扑增强模块后，所有数据集性能均达到最高。TAE 通过风险驱动的伪标签修正与虚拟异常中心构造，进一步提升了伪异常质量与模型判别力。

**损失函数消融**：
- 联合使用正则化损失 $\mathcal{L}_{\mathrm{reg}}$ 和分类损失 $\mathcal{L}_{\mathrm{cls}}$ 在所有数据集上均优于仅使用分类损失，表明正则化项对稳定训练和提升泛化能力有实质性贡献。

### 采样策略对比

Table 4 比较了三种伪异常采样策略：随机采样（Random）、低度节点采样（Low-degree）和 TAQ-GAD 的拓扑引导采样。结果表明，TAQ-GAD 的拓扑引导策略在 AUROC 和 AUPRC 上均一致且显著优于两种基线策略。尤其在 Reddit 数据集上，TAQ-GAD 的 AUROC 为 0.6682，而随机采样仅 0.5443，低度采样为 0.5579，差距超过 11 个百分点。这证明仅靠随机性或简单的度启发式无法有效识别真正的拓扑异常节点，而 NBS 和 PIS 联合量化的拓扑异常倾向能够精准定位高质量伪异常。

![[assets/figures/papers/iclr26_0011_ZURYrJgigi_Topological_Anomaly_Quantification_for_Semi-supe/figures/020_Table_4.jpg]]
*Table 4: Performance comparison of different sampling strategies*

### 超参数敏感性分析

**伪异常比例 τ**（Figure 3）：在 Amazon、Elliptic、T-Finance 等数据集上，性能在 τ≈0.05 附近达到峰值。τ 过小则伪异常样本不足，模型缺乏足够的异常对比信号；τ 过大则可能引入过多低质量的伪异常，引入噪声。TAQ-GAD 在较宽的 τ 范围内（0.02–0.10）性能波动较小，表现出良好的鲁棒性。

**损失系数 α 和 β**（Figure 4）：模型对 α 和 β 的取值不敏感，在多个数量级变化下性能保持稳定，说明联合训练目标的设计具有良好的数值稳定性，无需精细调参。

**标记正常节点比例 ρ**（Figure 5）：在不同 ρ 设置下 TAQ-GAD 性能波动有限，验证了方法对标记率的鲁棒性。

**NBS 权重 λ₁ 和 PIS 权重 λ₂**（Figure 6）：固定 λ₁=1 时，性能对 λ₂ 不敏感，表明两个拓扑指标的组合得分对权重分配具有较强的容错性。

### 失败模式与局限

尽管 TAQ-GAD 在多个数据集上表现优异，但存在以下已知局限：

1. **复杂拓扑模式的先验缺失**：当前 NBS 和 PIS 指标主要针对同配性较强的图结构设计，对于异配图或高低频混合信号的场景，拓扑异常量化可能不够精准。需要手动验证在强异配图上的适用性。
2. **大规模图的计算开销**：TAE 模块需要计算节点预测风险并动态构造虚拟中心及连边，在大规模图（如千万级节点）上可能存在计算瓶颈。论文未给出大规模图上的效率分析，该点需手动验证。
3. **静态图假设**：方法针对静态图设计，尚未扩展到动态图的时序异常检测。对于节点和边随时间演化的场景，需要重新设计拓扑量化与时序增强机制。
4. **极端标签稀疏场景**：在标记率接近 0% 时，NBS 依赖标记正常邻居的比例计算，其可靠性可能下降。论文未系统评估 0.01% 以下标记率的性能，该边界条件需手动验证。

### 补充图表

![[assets/figures/papers/iclr26_0011_ZURYrJgigi_Topological_Anomaly_Quantification_for_Semi-supe/figures/002_Figure_2.jpg]]
*Figure 2: NBS and NIS metrics for quantifying the degree of node anomaly. The $\mathcal { N } ( v _ { i }$ ) is defined as the 2-hop neighborhood of node $v _ { i }$*



## 定位与知识库关联

### 与现有方法的继承与区别

TAQ-GAD 的核心方法论植根于**生成式半监督图异常检测**范式，其直接对标方法为 GGAD。两者的共同前提是：仅利用少量正常节点标签，通过生成“伪异常”来弥补异常标签的缺失。然而，TAQ-GAD 在伪异常生成机制上做出了根本性改变。

GGAD 等前序工作（如 DAGAD 的表示置换策略）依赖**特征空间扰动或插值**来构造伪异常，其瓶颈在于缺乏对节点异常程度的定量评估——生成的伪异常代表性差，无法有效模拟真实世界中复杂的异常模式。TAQ-GAD 则将生成逻辑从特征空间迁移到**拓扑空间**：通过拓扑异常量化模块（TAQ）中的节点边界分数（NBS）与代理隔离分数（PIS），从图结构角度定量衡量每个节点的异常倾向，据此筛选高置信度的伪异常节点。这一转变使得伪异常的筛选有了可解释的结构依据，而非盲目的噪声注入。

在训练机制上，TAQ-GAD 进一步引入了拓扑异常增强模块（TAE），通过风险估计与标签翻转策略动态生成虚拟异常中心，并概率性地构造节点-中心连边以增强异常子图的拓扑一致性。这与 GGAD 中基于非对称局部亲和与自我中心接近性的静态先验约束形成对比——TAE 是一种**数据驱动的、动态的图增强**，而非预设的几何先验。

### 适用边界与约束条件

TAQ-GAD 的设计建立在以下隐式假设之上，这些假设界定了其有效适用范围：

1. **拓扑可分离性假设**：方法假设异常节点在图结构上表现出可量化的边界性或隔离性。当异常节点的拓扑特征与正常节点高度重叠（例如，异常节点嵌入在稠密的正常社区内部且邻居结构无异）时，NBS 与 PIS 指标的判别力将显著下降。

2. **静态图假设**：当前框架仅针对静态图设计，未建模时序演化。对于动态图上的异常检测（如金融交易网络中的突发欺诈模式），方法无法捕获时间维度上的行为漂移。

3. **半监督标签可用性**：NBS 的计算依赖标记正常节点的邻域信息。当标记率极端稀疏（接近 0%）时，NBS 的估计方差增大，可靠性降低。PIS 虽不依赖标签，但其作为 NIS 的代理指标，在语义上与真实隔离程度的对齐程度尚需进一步校准。

4. **同配性偏好**：方法未为异配图（heterophilic graphs）或高低频混合信号设计专门的拓扑先验。在节点类别与邻域结构关联弱的图上，边界分数和隔离分数的异常指示能力可能退化。

### 已识别的局限

论文明确指出了三类局限性：

- **复杂拓扑模式的先验缺失**：当前 NBS 与 PIS 指标主要捕捉一阶和二阶邻域的统计特征，对于层次性图形结构、多尺度社区嵌套等复杂拓扑模式缺乏表达力。这限制了方法在异配图或具有非平凡拓扑基元（motif）的网络上的性能上限。
- **大规模图的计算开销**：TAE 模块需要为每个节点计算风险得分、邻域类别分布，并动态构造增强图。在百万级节点规模的图上，该过程的计算复杂度可能成为瓶颈，需要设计更可扩展的增强技术（如子图采样或近似近邻搜索）。
- **动态图扩展空白**：方法完全面向静态快照图，未涉及动态图中的时序异常检测。如何将拓扑异常量化与增强框架迁移到时序演化建模中，是一个开放的设计空间。

### 开放问题与未来方向

基于上述局限，以下研究方向值得关注：

- **更具表达力的拓扑异常先验**：能否设计超越边界性与隔离性的拓扑指标？例如，引入图曲率（graph curvature）、持久同调（persistent homology）或谱方法，以捕获更细粒度的结构异常信号，特别是在异配图场景下。
- **可扩展的拓扑增强**：如何在保持拓扑语义的前提下，设计线性或亚线性复杂度的图增强算法？可能的路径包括基于节点重要性采样的稀疏增强、低秩近似下的虚拟中心构造，或利用图粗化（graph coarsening）进行分层增强。
- **动态图框架扩展**：将 TAQ 与 TAE 扩展到动态图的核心挑战在于：如何定义时序拓扑异常（如突发的结构隔离或边界漂移），以及如何设计时间感知的伪标签修正与增强机制。这可能需要融合时序点过程或状态空间模型。
- **极端稀疏标签下的校准**：当标记正常节点极少时，NBS 的估计可能严重偏差。研究在此场景下 PIS 与 NBS 的互补校准策略，或引入自监督预训练以提升拓扑表征的鲁棒性，是一个具有实际价值的问题。



## 原文 PDF

![[paperPDFs/ICLR_2026/Topological_Anomaly_Quantification_for_Semi_supervised_Graph_Anomaly_Detection.pdf]]
