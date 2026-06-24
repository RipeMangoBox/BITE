---
title: "xRFM: Accurate, scalable, and interpretable feature learning models for tabular data"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/xRFM_Accurate_scalable_and_interpretable_feature_learning_models_for_tabular_data.pdf
aliases:
- xRFM
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/computer_vision_task
core_operator: "利用平均梯度外积（AGOP）指导的二叉树分裂，将数据分成同质子集，然后在每个叶子节点上训练改进的核递归特征机（leaf RFM），从而实现局部特征学习和线性对数级可扩展性。"
primary_logic: "AGOP 同时充当特征选择器、监督降维工具和可解释性透镜；将其与自适应树结构结合，使核方法既能捕捉局部异质性，又能保持精度和速度。"
claims:
- "xRFM 在 TALENT 回归基准的所有聚合指标下表现最佳，超越了 31 种其他方法（包括 TabPFN-v2、CatBoost、LightGBM 等）。"
- "xRFM 能够学习不同子群（如基于 x0 的符号）的局部相关特征，而标准 RFM 只能将所有相关特征混在一起。"
- "AGOP 对角线能够直接给出可解释的特征重要性，无需额外事后解释工具，如在 California Housing 上识别出经度为最重要特征。"
- "xRFM 的训练时间随样本数呈近似线性增长（O(n log n)），推理时间为 O(log n)，在千样本以下比同类方法快两个数量级。"
---

# xRFM: Accurate, scalable, and interpretable feature learning models for tabular data

> [!tip] 核心洞察
> AGOP 同时充当特征选择器、监督降维工具和可解释性透镜；将其与自适应树结构结合，使核方法既能捕捉局部异质性，又能保持精度和速度。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | xRFM: 面向表格数据的准确、可扩展且可解释的特征学习模型 |
| 英文题名 | xRFM: Accurate, scalable, and interpretable feature learning models for tabular data |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=wHuVdpnUFp); [GitHub](https://github.com/dmbeaglehole/xRFM) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/computer_vision_task |
| Method | xRFM |
| Dataset | TALENT Regression (100 datasets), TALENT Binary Classification (120 datasets), Meta-test Large Regression (7 datasets) |

> [!tip] 效果简介
> - TALENT Regression (100 datasets) 上，Shifted Geometric Mean of Error (SGMε) 为 0.311，对比 0.323 (TabPFN-v2)，变化 -0.012。
> - TALENT Binary Classification (120 datasets) 上，Shifted Geometric Mean of Error (SGMε) 为 0.1485，对比 0.1524 (XGBoost)，变化 -0.0039。
> - Meta-test Large Regression (7 datasets) 上，Normalized RMSE 为 0.5514 (AGOP split)，对比 0.5638 (PCA split)，变化 -0.0124。

## 概述

表格数据是现实应用中最普遍的数据模态之一，但构建兼顾准确性、可扩展性与可解释性的学习模型仍是一大挑战。传统核方法（如核岭回归）虽具有闭式解和坚实的数学基础，却无法针对表格数据自适应地学习特征，且难以扩展到超过70k样本的数据集。梯度提升决策树（GBDT）长期作为该领域的主流选择，在精度和效率上占据优势，但其集成与分裂机制天然缺乏对异质性子群差异的内在解释能力，需要依赖事后解释工具。近期基于Transformer的基础模型（如TabPFN‑v2）提升了部分任务上的表现，却以高昂的训练与推理开销和低可解释性为代价。

为同时应对上述瓶颈，本文提出 **xRFM**（eXplainable Recursive Feature Machine），一种将特征学习核机器与自适应二叉树结构相结合的方法。其核心驱动力是 **平均梯度外积（AGOP）**：AGOP 同时充当特征选择器、监督降维工具与可解释性透镜。训练时，xRFM 先在各个节点上训练一个分裂模型并提取 AGOP 的顶部特征向量，依该方向对数据做中位数投影分裂，递归构建平衡二叉树，直至叶子节点样本数低于阈值；随后在每个叶子上独立训练一个改进的核递归特征机（Leaf RFM），该模块对广义核族 $K_{p,q}$ 进行调优，并可仅使用 AGOP 的对角线以引入适合表格数据的轴对齐偏置。这种“全局分裂-局部学习”的架构使核方法既能捕捉不同数据子群的局部相关特征，又将计算复杂度控制在 $O(n \log n)$ 训练时间与 $O(\log n)$ 推理时间，实现了对数线性的可扩展性。

在 **TALENT**、**TabArena‑Lite** 与大规模 **meta‑test** 三个基准上的实验验证了 xRFM 的综合优势：在 TALENT 回归的 100 个数据集上，xRFM 以移位几何均值误差 0.311 的成绩超越 31 种方法（含 TabPFN‑v2、CatBoost、LightGBM 等）排名第一，分类任务中位列前三；在小样本（<3000）场景下，训练加推理速度比其他方法快两个数量级。消融实验证实 AGOP 监督分裂显著优于无监督 PCA 分裂，且对角线近似在不损失精度的同时降低了计算开销。可解释性方面，无需附加任何事后工具，叶子 AGOP 的对角线即可直接输出特征重要性：例如在 California Housing 房价预测中自动识别经度为最重要特征，在合成数据上树结构使模型能够学习到基于符号的局部相关特征，而标准 RFM 只能将所有特征混为一谈。这些结果共同指向一种新的范式：通过 AGOP 驱动树分裂与局部核学习，使表格数据模型在精度、效率与可解释性三个维度上首次得到统筹优化。

## 背景与动机

表格数据是机器学习在商业、科学与工业领域中最普遍的建模对象，但构造一个同时满足**高精度**、**大规模可扩展**和**内在可解释性**的表格学习模型，至今仍是一个公认的开放难题。当前表格任务主要由两大类范式主导：基于核的闭式解方法和基于梯度提升树（GBDT）的集成方法，然而两者在面对现代表格数据需求时各自存在深刻的结构性缺口。

### 核方法：特征学习与可扩展性的两难

经典核岭回归（Kernel Ridge Regression）通过闭式解提供良好的理论性质，但其预测函数 $\widehat{f}(x)=K(x,X)\alpha$ 依赖于固定的核函数 $K$，本身不具备针对数据特征结构的自适应能力。递归特征机（Recursive Feature Machine, RFM）的提出首次将特征学习引入核机器：它交替求解核回归并利用平均梯度外积（AGOP）
$$
\operatorname{AGOP}(\widehat{f}, S)=\frac{1}{n}\sum_{i=1}^{n}\nabla\widehat{f}(x^{(i)})\nabla\widehat{f}(x^{(i)})^{T}
$$
迭代更新特征矩阵 $M_t$，使模型自动放大与预测相关的方向。AGOP 由此充当了**特征选择器**、**监督降维工具**与**可解释性透镜**的多重角色。然而，原始 RFM 的每一轮训练需在全量数据上执行 $\mathcal{O}(n^2)$ 的核运算，使其实际可处理的样本量上限约在 70,000 左右；当数据规模继续增长时，内存和时间成本将迅速失控。更关键的是，单一全局核模型隐式假设整个数据空间中特征与目标的关系是同质的——这一假设在真实表格数据中几乎总是不成立：不同子群往往由完全不同的特征所决定，而单一 RFM 只能将所有相关方向“混合”在一起，无法揭示局部的异质性结构。

### 树集成方法：高性能却欠解释

以 XGBoost、LightGBM 和 CatBoost 为代表的梯度提升树模型通过递归地学习特征交互和残差逼近，在大量表格基准上取得了顶尖预测效果，且其训练/推理复杂度可做到 $\mathcal{O}(n\log n)$。然而，GBDT 的**可解释性鸿沟**长期未得到真正填补：模型通常只提供基于增益或分裂次数的全局特征重要性，这些统计量无法呈现不同数据子群中特征作用方式的差异。对于需要回答“哪类患者对某项指标更敏感”或“何种交易模式由不同因素驱动”的异质性分析场景，GBDT 依然是黑盒，通常必须借助事后解释工具（如 SHAP）来近似，而这类事后工具本身带有忠实性问题。

### 本文动机：通过树枝嫁接局部特征学习

上述矛盾指向一个清晰的动机：**能否构造一种学习范式，使核方法的特征学习能力被约束在局部同质子群上，从而同时收获（i）对数-线性级的可扩展性，（ii）对数据异质性的局部建模能力，以及（iii）无需事后工具的内生可解释性？** 这正是 **xRFM** 的设计出发点。

xRFM 的核心思想是将 AGOP 同时用作**分裂准则**和**局部特征学习引擎**。在训练阶段，它利用 AGOP 的顶部特征向量指导二叉树递归地将数据分割为大小不超过 $C$ 的叶子子集（Algorithm A.2）；当分裂停止后，每一片叶子上独立训练一个改进的 RFM（Leaf RFM），该 Leaf RFM 仅需处理少量样本，并能通过自身的 AGOP 揭示该子群的关键预测特征。这种“以 AGOP 之树枝，嫁接收敛度之叶”的策略带来了以下三重决定性优势，构成论文的直接动机：

1. **打破规模墙**：树结构将一次 $\mathcal{O}(n^2)$ 的高昂核运算降解为大量 $\mathcal{O}(C^2)$ 的叶子级小运算，整体训练时间随样本数呈近似线性增长（$\mathcal{O}(n\log n)$），推理仅需沿树向下路由至某片叶子，复杂度为 $\mathcal{O}(\log n)$。实际测量显示，xRFM 在 3000 样本以下可比同类方法快两个数量级（Fig. 5）。
2. **实现异质性局部特征学习**：不同的 Leaf RFM 可学习完全不同的相关特征——如图 2 的合成实验所示，基于 AGOP 的分裂使得左右子集各自识别出自身与目标相关的方向，而全局 RFM 只能输出混杂的特征图，丧失了辨识力。
3. **提供内生的逐叶可解释性**：每个 Leaf RFM 的 AGOP 对角线天然即为该子群的特征重要性排名，无需附加 SHAP 等外部工具。在 California Housing 上，AGOP 直接将“经度”突出为首要特征（Fig. 7A），并且跨不同 leaf 可以对比子群之间的特征作用差异（如 NYC Taxi Tipping 的三个 Leaf RFM 分别强调不同因素），实现了“所见即所释”的透明性。

综上，xRFM 并非简单地将树结构与核机器进行机械组合，而是识别出 **AGOP 可以同时扮演三个核心角色**——分裂规则提供者、局部特征学习者、可解释性生成器——并将它们有机统一在一个轻量的二叉划分架构中。以此实现一种在精度上超越 TabPFN-v2 和所有经典 GBDT（TALENT 回归 SGMε = 0.311，排名第一，Table E.4）、在速度上逼近树模型、并且在可解释性上无需黑盒代理模型的表格学习新范式。

## 核心创新

传统核机器（如核岭回归）缺乏对表格数据的自适应特征学习，且难以扩展到超过 7 万样本的数据集；GBDT 虽有效，却缺乏内在可解释性，无法揭示异质性子群的不同特征模式。xRFM 的突破在于：将**平均梯度外积（AGOP）指导的二叉树分裂**与**改进的叶子核递归特征机（leaf RFM）**结合，在保持核方法闭式解优势的同时实现了局部特征学习和线性对数级可扩展性。AGOP 在此方案中同时充当特征选择器、监督降维工具和可解释性透镜——将其与自适应树结构融合，使核方法既能捕捉局部异质性，又能保持高精度和快速推理。

与基线方法（普通核岭回归、原始 RFM、GBDT 等）相比，xRFM 通过以下四个关键槽位的创新实现了能力跃迁：

- **模型结构**：由单一全局核机器转变为“二叉树 + 叶子核机器”架构。数据沿 AGOP 顶部特征向量的中位数投影递归分裂，直到叶子样本数不超过阈值 $C$，每个叶子独立训练一个 leaf RFM，实现按子群分治的局部特征学习（`Section 3.2, Algorithm A.2 (TreePartition)`）。
- **核函数族**：从高斯核等正交不变量核扩展为广义核 $K_{p,q}(x,x') = \exp(-\|x-x'\|_p^q / L^q)$（$0<q\leq p\leq 2$），提供对坐标独立性的灵活调控，适应表格数据的特征稀疏性与尺度差异（`Section 3.1, 引用 Schoenberg (1942)`）。
- **AGOP 使用方式**：除完整 AGOP 矩阵外，支持仅保留对角线的形式，引入轴对齐偏置以适配表格数据的特征独立性假设，同时降低计算成本（`Section 3.1, Appendix A.1; 引用 Zhu et al. (2025)`）。
- **分裂策略**：放弃了无分裂的全局建模，转而在每个节点训练一个分裂模型并提取其 AGOP 的主特征向量作为分裂方向，按中位数投影将数据二分，递归构建平衡二叉树。分裂方向完全由任务监督信号驱动，避免了无监督 PCA 或随机分裂的盲目性（`Section 3.2, Fig. 1A`）。

上述组件通过三个核心模块具体实现：`Leaf RFM 训练`对叶子子集执行 AGOP 更新循环（`Algorithm A.1`）；`树划分 (TreePartition)` 自顶向下递归分裂（`Algorithm A.2`）；`推理路由`将测试样本按分裂方向路由至相应叶子的预测器（`Fig. 1B`）。此外，xRFM 对每个 leaf RFM 进行本地化超参数调优（$\lambda$, $p$, $q$, 带宽等），仅使用落入叶子的验证数据，从而缓解了全局超参数难以同时适应所有子群的问题（`Section 3.2, Appendix A.3`）。

实验结果验证了上述创新的有效性：xRFM 在 TALENT 回归基准上取得所有聚合指标的最佳综合性能（SGMε=0.311，排名 4.70），超越了 TabPFN-v2、CatBoost、LightGBM 等 31 种方法（`Fig. 3A; Table E.4`）；在合成数据上，能够根据 $x_0$ 的符号自动分离局部相关特征，而原始 RFM 只能将所有特征混为一体（`Fig. 2; Section 3.2`）；AGOP 对角线可直接提供可解释的特征重要性（如在 California Housing 中识别经度为最重要特征），无需事后解释工具（`Fig. 7A; Section 5`）；运行时数据显示训练复杂度近似 $O(n \log n)$、推理 $O(\log n)$，在千样本以下比同类方法快两个数量级（`Fig. 5; Section 4`）。

目前的局限包括：分裂方向仅使用 AGOP 的顶部特征向量，未探索高阶结构信息；叶子大小的停止准则为经验设定，尚未形成系统的性能权衡分析。但 xRFM 所建立的“监督树划分 + 局部特征学习核机器”框架为表格数据的可扩展、可解释特征学习开辟了新方向。

## 整体框架

![[assets/figures/papers/iclr26_0015_wHuVdpnUFp_xRFM_Accurate_scalable_and_interpretable_feature/figures/001_Figure_1.jpg]]
*Figure 1: Overview of xRFM training and inference procedures. (A) xRFM is trained by splitting the data along the median projections (denoted $c _ { 1 } , c _ { 2 }$ ) onto computed split directions (denoted $v _ { 1 } , v _ { 2 }$ ) . Data is split repeatedly into leaves, which contain at most $\dot { C }$ training samples. Leaf RFMs are trained on the data at each leaf. (B) During inference, test data is routed to the appropriate leaf RFM based on split directions. The prediction is generated by the selected leaf RFM*

xRFM 将特征学习核机器与自适应二叉树相结合，旨在突破传统核方法在表格数据上的两大瓶颈：一是缺乏针对局部异质性的自适应特征学习，二是无法扩展到超过约 7 万样本的数据集（而 GBDT 虽然有效，但其集成性质弱化了内在可解释性）。核心因果杠杆是平均梯度外积（AGOP）：它同时扮演特征选择、监督降维和可解释性透镜三种角色。通过与二叉树结构耦合，xRFM 在树节点上利用 AGOP 指导数据分割，在叶子节点上训练改进的核递归特征机（leaf RFM），从而实现“全局分割、局部精炼”的管线，并将训练复杂度控制在 $O(n \log n)$、推理复杂度控制在 $O(\log n)$。

**整体管线**由四个模块串接（图 1）：

1. **树划分（TreePartition）**  
   输入训练集 $(X, y)$，递归执行以下过程：对当前节点包含的子集 $S$，训练一个分裂模型（通常是一个轻量核 RFM），计算其预测器的 AGOP $\frac{1}{n}\sum_{i=1}^{n}\nabla \hat{f}(x^{(i)})\nabla \hat{f}(x^{(i)})^{\mathsf{T}}$，提取顶部特征向量 $v$。以中位数投影为阈值，将样本分为右子集 $S_1 = \{x \in S \mid v^{\mathsf{T}}x > \text{Median}_{z \in S}(v^{\mathsf{T}}z)\}$ 和左子集 $S_2 = S \setminus S_1$。递归执行直到子集大小 $\le C$（叶子容量）。这一监督分裂确保数据沿预测相关方向被划分，从而为后续局部学习提供同质子群。

2. **叶子 RFM 训练（Leaf RFM）**  
   在每个叶子子集上独立训练一个改进的核 RFM。改进之处包括：（i）采用广义核族 $K_{p,q}(x,x')=\exp(-\|x-x'\|_p^q / L^q)$，其中超参数 $0<q \le p \le 2$ 和带宽 $L$ 可调，以适应表格数据特征的非各向同性；（ii）允许选择使用完整 AGOP 矩阵或仅其对角线来更新特征矩阵 $M_t$，对角线形式引入轴对齐偏置，既降低了计算成本，又更贴合表格数据的坐标独立性。训练交替进行核岭回归求解与 AGOP 更新（公式 3），迭代 $T$ 次后得到局部预测器 $\hat{f}_{\text{leaf}}$。

3. **叶子超参数调优**  
   利用落入各叶子的验证数据，分别调优对应 Leaf RFM 的超参数（$\lambda$、$p$、$q$、带宽、迭代次数、是否使用对角线等）。这种按叶子独立调优使模型能自动适配不同子群的数据特性，是对全局共享超参数的重大改进。

4. **推理路由**  
   测试样本从根节点开始，根据训练时存储的 $v$ 和中位数阈值向下路由，直到落入某个叶子节点。由该叶子的 RFM 计算预测值并输出。推理时间仅依赖于树深度和叶子模型大小，实际中可达到对数级开销。

**关键因果链**：AGOP 同时驱动分裂（识别全局相关方向）和叶子特征学习（捕捉局部相关方向），从而解决了 RFM 在异质数据上将所有相关特征混杂的问题（图 2）。树分裂将大样本空间降为多个小规模叶子问题，使核方法能处理超 7 万样本的数据，且训练时间随样本数近似线性增长（Fig. 5）。可解释性由 AGOP 对角线直接给出：无需额外工具，各叶子的特征重要性即反映出该子群的关键预测特征（Fig. 7A）。

**证据强度**：TALENT 回归基准上 xRFM 在 100 个数据集上聚合指标排名第一（SGMε=0.311，Rank=4.70），超越 31 种基线方法（置信度 0.98）。消融实验证实监督分裂（AGOP 或随机森林准则）显著优于无监督 PCA 分裂，且加入温度微调可进一步提升性能（Tables E.1 E.2，置信度 0.95）。需注意，叶子容量 $C$ 的最佳选择尚未系统研究，当前停止准则为经验值；AGOP 作为可解释性机制与 SHAP 等工具的直接对比亦有待完成。

## 核心模块与公式推导

xRFM 的核心架构由两大组件构成：**AGOP 指导的递归二分树（TreePartition）** 与 **叶子级改进核递归特征机（Leaf RFM）**。前者将数据自适应地划分为同质子集，后者在每个子集上独立进行局部特征学习与预测，二者协同赋予模型对数线性级训练复杂度、对数级推理延时以及内建的可解释性。

### 1. 基础元件：核预测器、AGOP 与核 RFM

所有叶子模型共享同一套数学基础，即核岭回归预测器、平均梯度外积以及原始核 RFM 迭代。

**核机器预测器** 给定训练数据 $(X, y)$、核函数 $K$ 和正则化系数 $\lambda$，闭形解为

$$
\widehat{f}(x) = K(x, X) \alpha,\qquad 
\alpha = \bigl(K(X, X) + \lambda I\bigr)^{-1} y. \tag{1}
$$

**平均梯度外积（AGOP）** 对预测器 $\widehat{f}$ 在样本集 $S=\{x^{(i)}\}_{i=1}^n$ 上，AGOP 定义为梯度的无中心协方差：

$$
\operatorname{AGOP}(\widehat{f}, S) = \frac{1}{n}\sum_{i=1}^{n} \nabla \widehat{f}(x^{(i)})\,\nabla \widehat{f}(x^{(i)})^{\top}. \tag{2}
$$

AGOP 的顶部特征向量指示模型最敏感的方向，构成监督降维与特征选择的基石。

**核 RFM 迭代** 原始 RFM 通过交替求解核回归与更新特征矩阵实现特征学习，第 $t$ 轮为

$$
\begin{aligned}
\text{Step 1:}&\quad \widehat{f}_t(x) = K(M_t x, X M_t)\,\alpha_t,
\quad \alpha_t = \bigl[K(X M_t, X M_t) + \lambda I\bigr]^{-1} y,\\[2mm]
\text{Step 2:}&\quad M_{t+1} = \bigl[\operatorname{AGOP}\bigl(\widehat{f}_t(M_t x), X\bigr)\bigr]^{c}.
\end{aligned} \tag{3}
$$

这里 $M_t\in\mathbb{R}^{d\times d}$ 为特征变换矩阵，幂次 $c$ 常取 $1/2$ 以获得矩阵平方根，迭代结束后 $M$ 编码了任务相关的低秩结构。

### 2. Leaf RFM：针对表格数据的改进核 RFM

xRFM 并不直接使用原始 RFM，而是在每个叶子节点上运行**改进的 Leaf RFM**，主要包含两项调整。

**广义核族** 为适应表格特征中连续与离散变量共存的特点，Leaf RFM 采用

$$
K_{p,q}(x, x') = \exp\!\Bigl(-\|x - x'\|_p^{\,q}\,\big/\,L^{q}\Bigr),
\qquad 0 < q \le p \le 2, \tag{4}
$$

其中 $\|\cdot\|_p$ 为 $L_p$ 范数，$L$ 为带宽，指数 $q$ 控制核的平滑程度。该核族对坐标独立的变量更友好，超参数 $p,q$ 可跟随验证集自动选取。

**AGOP 的对角化与特征矩阵归一化** 表格数据常呈现轴对齐的重要性，Leaf RFM 可选择只保留 AGOP 的对角线以降低计算开销。在第 $t$ 轮，首先计算当前模型梯度的 AGOP（可以是全矩阵或仅对角线），然后更新并归一化特征矩阵：

$$
M_{t+1} \gets \frac{M_{t+1}}{\varepsilon + \max_{i,j}|M_{t+1}[i,j]|},
$$

进而用对角特征变换构造预测器：

$$
f^{(t)}(x) = K\bigl(x \odot \operatorname{diag}(M_t)^{1/2},\; X_M\bigr)\,\alpha_t,
$$

其中 $X_M$ 表示经过 $M_t$ 变换的训练特征，$\odot$ 为逐元素乘法。对角化极大降低了存储与计算成本，在多数表格任务上精度损失轻微（见附录 A.1 及超参数研究）。

Leaf RFM 在每个叶子内独立重复上述步骤 $T$ 次，同时在该叶子的验证子集上调优 $\lambda, p, q, L$ 等超参数。

### 3. AGOP 指导的递归二叉树划分

xRFM 的可扩展性来源于**监督、自适应的二叉树分裂**。对于节点上的样本集 $S$（$|S| > C$），算法：

1. 在 $S$ 的随机子集上训练一个临时“分裂模型”，提取其 AGOP 的顶部特征向量 $v$；
2. 将所有样本投影到 $v$ 方向，按投影值的中位数分成左右两个子集：

$$
\begin{aligned}
S_{\mathrm{right}} &= \{\, x \in S \mid v^{\top}x > \operatorname{Median}\!\bigl(\{v^{\top}z \mid z \in S\}\bigr) \,\},\\
S_{\mathrm{left}}  &= \{\, x \in S \mid v^{\top}x \le \operatorname{Median}\!\bigl(\{v^{\top}z \mid z \in S\}\bigr) \,\}.
\end{aligned} \tag{5}
$$

递归执行该过程直至所有叶节点样本数 $\le C$。由于每次分裂沿中位数进行，整棵树自动保持平衡，训练与推理的复杂度分别为 $O(n\log n)$ 和 $O(\log n)$。

分裂方向 $v$ 完全由监督信号驱动（AGOP 的顶部特征向量），因此每次分裂都聚焦于当前子集上最影响预测的特征方向，使后续 Leaf RFM 能在更同质的数据上学习到局部相关特征。

### 4. 推理路由与内建可解释性

**推理路由** 测试样本 $x_{\mathrm{test}}$ 从根节点开始，逐层与分裂方向 $v$ 及其中位数投影 $c$ 比较：若 $v^{\top}x_{\mathrm{test}} > c$ 则进入右子树，否则进入左子树，最终到达某个叶子。该叶子对应的预训练 Leaf RFM 直接给出预测 $f_{\mathrm{leaf}}(x_{\mathrm{test}})$，单次预测开销与树高（$O(\log n)$）成正比。

**内建可解释性** 每个 Leaf RFM 的 AGOP 对角线天然提供了该叶子子群的特征重要性排序，无需额外的事后解释工具（图 7）。全局视角下，不同叶子可能关注完全不同的一组特征，从而揭示数据中的异质性，例如在 California Housing 数据中某叶子将经度标记为最重要特征，而另一叶子则强调房屋年龄等（图 7A）。

以上模块共同实现了 xRFM 的设计目标：高精度（TALENT 回归基准排名第一，Fig. 3；Table E.4）、对数线性可扩展性（Fig. 5）、以及天然的可解释性。

## 实验与分析

### 主结果
在 TALENT 回归基准（100 个数据集）上，xRFM 在所有聚合指标下均取得最优。其移位几何均值误差 SGM_ε 为 **0.311**，优于 TabPFN‑v2 的 0.323（Table E.4），平均秩次 4.70，远超 31 种对比方法（含 CatBoost、LightGBM、XGBoost 等）。在 TabArena 子集的二分类任务中，xRFM 的 SGM_ε 为 **0.1485**，同样低于 XGBoost 的 0.1524（Table E.15）。图 3A‑C 将这些性能与平均训练+推理时间联合展示：xRFM 在回归任务上同时取得最低误差与极短用时，处于帕累托前沿的显著位置；分类任务上排名第三，但误差与最优方法差距极小，而推理速度远快于多数神经网络方法。

![[assets/figures/papers/iclr26_0015_wHuVdpnUFp_xRFM_Accurate_scalable_and_interpretable_feature/figures/003_Figure_3.jpg]]

![[assets/figures/papers/iclr26_0015_wHuVdpnUFp_xRFM_Accurate_scalable_and_interpretable_feature/figures/024_Figure_3.jpg]]
*Figure 3: Table E.4: Full TALENT Regression results across 100 datasets. Rank is the average rank among the ordered methods over all datasets. Score is the metric we use to compare methods in Figure 3, in this case SGMϵ. Normalized score is the arithmetic mean of the normalized nRMSE. Top-X (%) is the percentage of datasets for which that method is in the top X ranks. The final column is the shifted geometric mean error (SGMε)*

在涵盖 70 k–500 k 样本的大规模 meta‑test 数据集（7 个回归、13 个分类）上，xRFM 的归一化 RMSE 与分类错误率均显著优于 MLP 基线（图 6），并且当采用 AGOP 分裂时归一化 RMSE 均值为 0.5514，显著低于使用 PCA 分裂的 0.5638（Table E.1）。

### 运行效率与可扩展性
xRFM 的训练时间随样本数呈近似 **O(n log n)** 增长，推理时间为 **O(log n)**（图 5）。当数据集样本量低于 3 000 时，xRFM 的总训练+推理时间比同类方法快两个数量级；即使面对数十万样本，仍能保持线性的对数增长，避免了传统核机器对 70 k 以上数据的无法处理问题。这一效率源于二叉树递归分裂将全局核计算分解为局部小规模核机器，从而在保持精度的同时实现了线性对数级可扩展性。

![[assets/figures/papers/iclr26_0015_wHuVdpnUFp_xRFM_Accurate_scalable_and_interpretable_feature/figures/016_Figure_5.jpg]]
*Figure 5: Total training and inference time for the best hyperparameter configuration as a function of the number of samples (training+validation+testing) across the TALENT benchmark. Curves indicate piece-wise linear fit to measures on each dataset (shown as points). (A) Results across 100 regression tasks. (B) Results across 80 multi-class classification tasks. (C) Results across 120 binary classification tasks*

### 消融实验
**分裂策略的影响**：在 meta‑test 大型数据集上系统比较了三种分裂方向（AGOP、PCA、随机森林特征重要性）以及是否添加温度微调（TT）的软路由。结果（Tables E.1, E.2）显示，监督分裂（AGOP 或 RF）在回归和分类任务上均显著优于无监督 PCA 分裂；引入 TT 后性能更进一步，回归 SGM_ε 降至 **0.3440**，分类 SGM_ε 降至 **0.1156**，且 RF+TT 与 AGOP+TT 的算术平均误差几乎无差别。这说明 AGOP 提供的监督分裂与软集成机制对最终性能至关重要。

**与原始 RFM 对比**：在 TALENT 中需要至少一次分裂的大数据集上，xRFM 的归一化算术平均误差从 RFM 的 0.0503 降至 **0.0379**（Table E.3），验证了树结构对核机器在大数据上的必要提升。

**对角线与全矩阵 AGOP**：在多数表格任务中，仅保留 AGOP 对角线的轴对齐偏置版本与使用全矩阵的性能相当，但计算成本显著降低，佐证了该方法对表格数据特征独立性的适配能力。

### 可解释性分析
xRFM 无需附加任何事后解释工具即可直接从叶子 RFM 的 AGOP 对角元提取特征重要性（图 7）。在 California Housing 房价预测中，经度被识别为最重要的特征；在 Covertype 森林类型分类中，海拔与水平/垂直距离等地理特征占据主导；在乳腺癌检测数据上，AGOP 的顶部特征向量指出凹点数均值为最强正相关特征，而紧凑度标准差表现为反向作用。这些结果与领域知识高度一致，表明 AGOP 可同时充当特征选择器、监督降维工具和可解释性透镜。

![[assets/figures/papers/iclr26_0015_wHuVdpnUFp_xRFM_Accurate_scalable_and_interpretable_feature/figures/019_Figure_7.jpg]]
*Figure 7: Interpreting xRFM through the AGOP of its constituent Leaf RFM models. (A) Examining the most important features for xRFM trained on California Housing (price prediction) and Covertype (dominant tree species prediction) datasets, based on the magnitude of diagonal entries. (B) Examining the features identified across three different Leaf RFM models for the NYC Taxi Tipping dataset. (C) Examining features learned for Breast Cancer detection from processed FNA imaging. The spectrum of this AGOP is plotted and the top eigenvector is shown in a bar plot. The most positive and negative entries of this eigenvector are boxed*

### 失败模式与现存局限
1. **叶子大小权衡未系统化**：当前最大叶子容量 C 依靠经验设定，分裂停止准则缺乏基于叶子数据统计的自动优化，可能在某些样本分布下产生欠分裂或过分裂。
2. **可解释性忠实度缺乏严格对比**：虽 AGOP 能输出直观的特征重要性，但尚未与 SHAP、GBDT 的 Gini 重要性等流行方法在表格数据上进行系统的人因评估，其因果解释力有待进一步验证。
3. **内存与超参数优化不足**：尚未整合迭代核求解器（如 EigenPro）以进一步降低内存占用并免除脊回归正则化参数 λ 的手动调优，限制了向千万级样本的极限扩展。
4. **分裂方向信息利用单一**：当前仅使用 AGOP 的顶部特征向量决定分割方向，高阶结构信息可能未被充分利用，导致在需要复杂多特征交互的子群上表现潜力受限。

### 补充图表

![[assets/figures/papers/iclr26_0015_wHuVdpnUFp_xRFM_Accurate_scalable_and_interpretable_feature/figures/021_Table_2.jpg]]
*Table 2: Table E.1: Evaluation of split methods on large regression datasets from meta-test. We consider three methods for choosing split directions - AGOP, Principal Component Analysis (PCA), and Random Forest criterion (RF). We also evaluate ensembling leaf RFM models using the temperature tuning method described in Appendix B*

## 方法谱系与知识库定位

xRFM 并非孤立的方法提案，而是对“核机器 + 特征学习”与“树基表格模型”两条路线的有意识嫁接。理解它的定位，需要先厘清它与两类基准的关系，以及它在设计空间中所做的关键选择。

### 与直接基准的继承与升级

xRFM 的直接前身是 **Recursive Feature Machine (RFM)**，二者共享通过平均梯度外积（AGOP）循环更新特征矩阵的核心机制。原始 RFM 在全局数据上训练单一的核机器，迭代式地利用 AGOP 捕获相关特征子空间，但其特征学习是“全景式”的——同一组特征权重适用于所有样本。这导致了两个关键瓶颈：(1) 无法应对数据中存在异质性子群（例如按某个特征的符号划分后，不同区域的相关特征截然不同）的情形；(2) 核矩阵求逆的 $O(n^3)$ 复杂度使其难以扩展到超过约 70k 样本的数据集（Fig. 5; Section 4）。

xRFM 对 RFM 进行了四个结构性的“槽位替换”（slot changes），形成了新的能力边界：

1. **模型结构**：从单一全局核机器变为“二叉树 + 叶子核机器（leaf RFM）”的层级组合。每个叶子在至多 $C$ 个样本的子集上独立训练，不同叶子的 RFM 学习不同的特征权重。这使得局部特征学习成为可能——合成数据实验清晰展示了这一点：当需要根据 $x_0$ 的符号学习不同的相关特征时，标准 RFM 只能将所有特征混在一起，而 xRFM 通过沿 AGOP 顶部方向递归分裂，成功分离出两个子群并各自学习到正确的局部特征（Fig. 2; Section 3.2）。

2. **核函数族**：从单一的高斯核（及其变体）扩展为更通用的 $K_{p,q}(x,x') = \exp(-\|x - x'\|_p^q / L^q)$ 族，其中 $0 < q \leq p \leq 2$（Schoenberg, 1942）。这一推广允许模型通过超参数搜索自动适应表格数据中常见的坐标独立程度——当 $p, q$ 较小时更适用于轴对齐的特征，较大时则允许更复杂的特征交互。

3. **AGOP 使用方式**：原始 RFM 始终使用完整的 AGOP 矩阵作为特征变换。xRFM 则增加了“仅使用 AGOP 对角线”的选项，这引入了轴对齐偏置（axis-aligned bias），且被证明在多数表格任务上不劣于全矩阵方案，同时显著降低计算成本（Appendix A.1; 引用 Zhu et al., 2025）。这个选择并非纯工程优化——它实质上是让核方法向表格数据的常见特性（特征往往独立而非密集交互）靠拢。

4. **分裂策略**：分裂决策由 AGOP 的顶部特征向量指导：在当前子集上训练一个轻量的“分裂模型”（split model），计算其 AGOP，取顶部特征向量的中位数投影作为分割面，递归直到叶子样本数 ≤ $C$（Algorithm A.2; Fig. 1A）。这不同于 GBDT 逐特征贪心搜索最优分裂点的策略，也不同于随机森林的纯度准则——AGOP 提供的分裂方向来自梯度协方差，直接捕捉对预测最敏感的特征方向。

这一系列设计选择使得 xRFM 继承了 RFM 的特征学习能力，又通过树结构获得了 **$O(n \log n)$ 训练时间**和 **$O(\log n)$ 推理时间**的可扩展性（Fig. 5 展示了近似线性的总时间增长）。

### 与 GBDT 和神经表格方法的关系

**GBDT（XGBoost、LightGBM、CatBoost）** 是表格数据的防御性基线。xRFM 与 GBDT 共享“树 + 局部模型”的结构直觉，但存在本质差异：GBDT 每片叶子输出标量（值或概率），xRFM 每片叶子输出一个完整的核机器——这使其在叶子上保留了捕获非线性特征交互的能力，而 GBDT 需要靠增加深度和树数来近似同样的效果。代价是推理时需要计算核函数（$O(|\text{leaf data}|)$），而不像 GBDT 只需查表和加法。

实验证据表明，这一代价换来了精度提升：在 TALENT 回归基准（100 个数据集）上，xRFM 在移位几何均值误差（SGMε）上达到 **0.311**，优于 XGBoost（0.323）、CatBoost（0.314）以及最新基座模型 TabPFN-v2（0.323），位列全部 32 种方法之首（Table E.4; Fig. 3A）。在分类任务上 xRFM 排名第三，仅次于 TabPFN-v2 和 CatBoost，但其训练+推理总时间在两个数量级内与最快的 GBDT 实现竞争（Fig. 3D-I）。

**TabPFN-v2** 代表了另一条路线：在合成表格数据上预训练 transformer，然后在测试时进行上下文学习。xRFM 与它的关系是“按需学习” vs “先验知识迁移”的对比。TabPFN-v2 的优势在于小样本场景下的快速适应（无需训练），而 xRFM 在样本量超过约 3k 后开始展现精度优势，且无需任何预训练。二者在方法谱系中分别占据“训练免费”和“特征学习+树扩展”的对角。

### 适用边界与局限

xRFM 的强项场景可以归纳为：**中等维度（数十至数百特征）、存在异质性（不同子群依赖不同特征）、样本量从数百到数十万的表格预测任务**。已经有验证的 benchmark 覆盖了回归（RMSE 标准化）、二分类与多分类任务。

但需要注意以下已明确的局限，部分需要人工验证：

1. **叶子大小 $C$ 的经验性质**：$C$ 控制核矩阵求逆的成本与局部学习粒度之间的权衡。论文承认，“叶子大小与性能之间的权衡尚未系统研究”（Section 6）。当前 $C$ 的选择仍依赖经验协议，缺乏基于数据统计特性的自适应停止准则。这使得在新场景下调参需要较多的网格搜索。

2. **分裂方向的单步性**：树分裂仅使用 AGOP 的顶部特征向量（一维投影），可能丢弃了高阶结构信息。虽然消融实验（Tables E.1, E.2）表明 AGOP 分裂与随机森林准则（RF）分裂表现相当，且都优于无监督的 PCA 分裂，但这是否意味着单方向分裂已足够，还是说多维分裂有潜力进一步提升，尚未回答。

3. **可解释性声明的验证深度**：xRFM 的 AGOP 对角线可以直接给出逐叶片的特征重要性（Fig. 7A-C），论文称这“无需堆叠额外的事后解释方法”。但从方法对比角度看，**与 SHAP、LIME 等博弈论或扰动基解释工具的忠实性对比并未进行严格实证**。AGOP 衡量梯度协方差，与 Shapley 值捕捉边际贡献的机制并不等价——例如，强相关的特征可能分散 AGOP 的重要性质量，而 Shapley 值通过联盟采样可以更均衡地分摊。这一差距是否存在、在什么条件下显现，需要人工验证。

4. **核求解器的内存瓶颈**：虽然树结构将核矩阵求逆限制在叶子大小 $C$ 内，但每个叶子仍需 $O(C^3)$ 的求逆或等价的迭代求解。论文明确提出“当前实现尚未利用迭代核求解器（如 EigenPro）以进一步降低内存占用并避免超参数 λ 的调优”（Section 6），这意味着在极端数据规模（千万级）下，即使 $O(n \log n)$ 的树结构也可能因常数因子过大而难以实用。

5. **超参数搜索空间较大**：Leaf RFM 需要在每个叶子独立调优 λ、p、q、带宽等参数（Table A.1），虽然使用了验证数据子集（路由到对应叶子的样本），但这增加了总调优成本，尤其是在叶子数量较多的深度树上。

### 开放问题与潜在延伸

从当前工作的弱点出发，几个方向值得关注，但这些目前尚无答案：

- **自适应叶大小与停止准则**：能否根据叶子样本的 AGOP 谱特性（如顶部特征值占比）判断是否还需要继续分裂？这可以将经验性的 $C$ 替换为有理论支撑的决策规则。
- **更高阶分裂方向**：当前的一维投影分裂是否能被多维子空间分裂所增强？例如使用 AGOP 的顶部 $k$ 个特征向量进行超平面或谱聚类分裂，可能捕获更复杂的子群结构。
- **与其他特征选择/重要性框架的系统对比**：AGOP 作为可解释性机制的忠实度究竟如何？需要在一组标注了真实重要特征的数据集上，与 SHAP、permutation importance、Integrated Gradients 等方法进行定量对比——包括重要性排名的 Kendall τ、最相关特征集的 Jaccard 相似度等指标。这项工作对于 xRFM 作为“可解释学习器”的定位至关重要。
- **时序与图结构表格的扩展**：xRFM 目前假设样本独立同分布。对于具有时序依赖或图结构的表格数据（如传感器序列、社交网络属性），树分裂和 AGOP 机制是否能自然扩展到保留这些结构依赖，仍属未知。
- **与预训练基座模型的集成**：TabPFN-v2 说明了预训练在表格数据上的潜力。xRFM 的核机制是否可以与预训练特征提取器集成——例如用预训练模型提供的表示替代原始特征作为 AGOP 的输入——构成“预训练 + 自适应局部核”的混合体，理论上可以结合先验知识与局部特征学习的优势。

## 原文 PDF

![[paperPDFs/ICLR_2026/xRFM_Accurate_scalable_and_interpretable_feature_learning_models_for_tabular_data.pdf]]
