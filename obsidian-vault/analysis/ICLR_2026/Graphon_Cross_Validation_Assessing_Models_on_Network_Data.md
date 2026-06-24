---
title: "Graphon Cross-Validation: Assessing Models on Network Data"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Graphon_Cross_Validation_Assessing_Models_on_Network_Data.pdf
aliases:
- CIKFRIGCV
- GCVAMND
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "关键干预：在训练时将验证集中的边替换为独立的伯努利随机变量（随机插补），从而切断训练与验证之间的统计依赖，并使训练分布保持原始分布的仿射变换关系。"
primary_logic: "通过随机边缘插补与仿射变换校正，可以从被扰动过的训练网络上获得对原始连接概率矩阵的无偏预测，进而构造出与真实均方误差渐近平行的交叉验证分数，实现可靠的模型与超参数选择。"
claims:
- "Lemma 1 确保训练集与验证集在给定真值 P 下独立，且训练数据的期望是原概率矩阵的仿射变换。"
- "Theorem 1 证明 CV-imputation 分数是实际估计损失加一个常数的相合估计，所选模型渐近收敛到最优模型。"
- "在合成与真实网络上，CV-imputation 选择的模型 MSE 显著低于 ECV 和默认选择，且计算速度成倍提升（例如 PolBlog 上 AUC 0.88 vs 0.80，时间 56.9s vs 258.7s）。"
- "Synthetic Graphon 1 (NS estimator, n=200) 上 MSE (×100) = 0.51±0.07 (CV‑imputation)"
---

# Graphon Cross-Validation: Assessing Models on Network Data

> [!tip] 核心洞察
> 通过随机边缘插补与仿射变换校正，可以从被扰动过的训练网络上获得对原始连接概率矩阵的无偏预测，进而构造出与真实均方误差渐近平行的交叉验证分数，实现可靠的模型与超参数选择。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Graphon 交叉验证：评估网络数据模型 |
| 英文题名 | Graphon Cross-Validation: Assessing Models on Network Data |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=8J3GTeQmwl) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | CV-imputation (K‑fold random‑imputation graphon cross‑validation) |
| Dataset | Synthetic Graphon 1 (NS estimator, n=200), Political Blogs network (PolBlog), Coauthorship network (NetSci), Yeast protein‑protein interaction network |

> [!tip] 效果简介
> - Synthetic Graphon 1 (NS estimator, n=200) 上，MSE (×100) 为 0.51±0.07 (CV‑imputation)，对比 9.15±19.25 (ECV) / 39.05±3.33 (Default M=1)，变化 CV‑imputation 降低 MSE 约 94%（vs ECV）和 98%（vs 默认）。
> - Political Blogs network (PolBlog) 上，AUC 为 0.88±0.01 (CV‑imputation)，对比 0.80±0.02 (ECV)，变化 +0.08。
> - Coauthorship network (NetSci) 上，AUC 为 0.72±0.01 (CV‑imputation)，对比 0.70±0.01 (ECV)，变化 +0.02。

## 概述

网络数据中模型与超参数的评估长期面临根本性困难：传统交叉验证依赖于数据点的独立性假设，而网络节点间固有的依赖结构使得随机节点分割不可行；直接对边进行采样则会改变网络拓扑与连接分布，引入严重偏差，导致模型选择失效。本文针对这一问题，在边缘独立的图核模型（graphon model）框架下提出了一种新颖的图核交叉验证方法 **CV‑imputation**（K‑fold random‑imputation graphon cross‑validation）。其关键干预是在训练时将验证边替换为独立伯努利随机变量（随机插补），从而切断训练与验证集之间的统计依赖，同时使训练分布保持原始概率矩阵的仿射变换关系；继而在得到训练网络上的概率矩阵估计后，通过仿射反变换恢复对原始连接概率的无偏预测，最终构造出与真实均方误差渐近平行的交叉验证分数。

该方法具有模型无关性，可配合任意图核估计器（如 NS、SAS、USVT、ICE 等）使用，用于选择邻域大小、估计方法等超参数。理论上，Lemma 1 保证了训练与验证集的独立性及仿射关系，Theorem 1 证明 CV‑imputation 分数是实际估计损失加上一个常数的一致估计，且其最小值所对应的模型渐近收敛至最优模型。实验结果表明，在合成图核上与真实网络上，CV‑imputation 所选模型的均方误差（MSE）和链接预测 AUC 显著优于主流的边交叉验证方法（ECV）及默认超参数选择，同时计算效率成倍提升——例如在 PolBlog 网络上 AUC 达到 0.88（ECV 为 0.80），时间仅为 56.9 秒（ECV 为 258.7 秒）。该方法的主要局限在于仅适用于边缘独立网络，且现有理论保证限定在图核模型族内；未来可向动态网络、带协变量网络及更一般的潜在空间模型扩展。

## 背景与动机

网络数据通常被建模为图核模型 (graphon model)，其中每条边 $a_{ij}$ 由独立的伯努利分布 $\mathrm{Ber}(p_{ij})$ 生成，连接概率由对称图核函数 $f$ 及节点潜在位置 $\mu_i$ 决定（$p_{ij}=f(\mu_i,\mu_j)$，Equation 2）。模型评估的自然目标是最小化估计概率矩阵 $\hat{\mathbf{P}}(M|\mathbf{A})$ 与真实 $\mathbf{P}$ 之间的均方误差

$$
L(M)=\frac{1}{n(n-1)}\|\hat{\mathbf{P}}(M|\mathbf{A})-\mathbf{P}\|_F^2 \quad\text{(Equation 3)},
$$

但 $\mathbf{P}$ 不可观测，因此需要交叉验证来近似 $L(M)$。

传统交叉验证依赖观测独立性，而网络节点通过边紧密耦合，破坏了这一前提。随机分割节点会截断节点间的依赖结构，导致训练与验证之间的统计泄漏；直接采样边作为验证集则改变网络的边密度分布和拓扑连通性，使图核估计器在扭曲的分布上训练，引入严重偏差。Figure 1 直观展示了不同邻域超参数下图核概率矩阵估计质量的剧烈变化，凸显了模型选择对超参数的高度敏感性——这正是网络交叉验证的核心瓶颈：如何在切断训练‑验证依赖的同时，保持网络固有结构的无偏表达。

现有方法 ECV (Edge Cross‑Validation) 通过矩阵补全（如 SVD）估计被移除的验证边，但面临两个缺陷：① 矩阵补全计算成本高昂，需估计大量缺失边；② 补全精度受限于低秩假设，当真实图核不具备精确低秩性时，误差会被放大，损害模型比较的可靠性。实验证据表明，ECV 在合成网络上的 MSE 比本文方法高出一个数量级（Table 1），在真实网络 PolBlog 上的 AUC 仅为 0.80，而本文方法达到 0.88（Table 2）。

本文的动机正是设计一种既保持训练‑验证独立、又避免昂贵补全的交叉验证策略。核心突破在于：在训练阶段将验证边替换为独立伯努利随机变量（随机插补），从机制上切断依赖（Lemma 1 保证了训练集与验证集在给定 $\mathbf{P}$ 下的独立性）；同时，扰动后的训练矩阵其期望 $\mathbf{P}^{[-k]}$ 是原始 $\mathbf{P}$ 的仿射变换（Equation 5），从而可以用解析的仿射校正从训练估计中恢复对 $\mathbf{P}$ 的无偏预测（Equation 6）。基于此构建的交叉验证分数 $V_K(M)$ 与真实损失 $L(M)$ 仅相差一个常数 $\Lambda$ 且渐近收敛（Theorem 1），使可靠、快速的模型与超参数选择成为可能。

## 核心创新

传统交叉验证（CV）在网络数据上的失效，根源于网络观测之间的强依赖关系：节点对不再满足独立同分布假设，直接分割节点或将边缘采样用于验证均会破坏网络拓扑与连接分布，导致模型评估产生严重偏差。**CV‑imputation 通过一次关键干预——在构造训练集时将验证边替换为独立的伯努利随机变量（随机插补）——切断了训练与验证之间的统计依赖，同时使训练数据的分布保持为原始连接概率矩阵的一个仿射变换，从而让被扰动后的训练网络能够无偏地预测原始概率，并构造出与真实均方误差（MSE）渐近平行的交叉验证分数。** 这一设计源自对“边缘独立模型”下依赖结构的深刻洞察，并由此衍生出方法学上的两个核心变更（changed slots）。

### 1. 验证边处理方式：从矩阵补全到随机插补

| 维度     | ECV (基线)                          | CV‑imputation (本文)               |
|----------|------------------------------------|-------------------------------------|
| 策略     | 用矩阵补全算法（如 SVD）估计缺失边 | 用独立的 $\mathrm{Ber}(\omega)$ 随机插补验证边 |
| 依赖消除 | 补全过程仍可能引入训练与验证间未量化的依赖 | 随机性保证训练集与验证集在给定真值 $\mathbf{P}$ 下的条件独立（Lemma 1） |
| 计算成本 | 需多次执行昂贵的矩阵分解，代价高 | 无需分解，计算速度成倍提升 |

训练邻接矩阵由下式构造（Equation 4）：  
$$ \mathbf{A}_{ij}^{[-k]} = \begin{cases} a_{ij} & (v_i,v_j)\notin S_k,\\ b_{ij} & \mathrm{otherwise}, \end{cases} $$  
其中 $b_{ij}\stackrel{\mathrm{iid}}{\sim}\mathrm{Ber}(\omega)$。这一替换不仅消除了训练与验证边之间的直接关联，还赋予了训练矩阵一个可解析刻画的期望结构——$\mathbb{E}[\mathbf{A}^{[-k]}] = \mathbf{P}^{[-k]} = w_k\theta\mathbf{1}\mathbf{1}^T + (1-w_k)\mathbf{P}$（Equation 5），即原始概率矩阵的仿射函数。相比之下，ECV 通过补全获得的估计不仅计算重，而且其分布与原始 $\mathbf{P}$ 的关系缺乏简洁表达，难以从理论上保证无偏性。

### 2. 概率矩阵预测校正：从直接输出到仿射逆变换

| 维度     | ECV (基线)                 | CV‑imputation (本文)                     |
|----------|---------------------------|-----------------------------------------|
| 预测输出 | 直接使用补全后的 $\hat{\mathbf{P}}$ | 基于仿射关系恢复原始 $\mathbf{P}$ 的无偏预测 $\hat{\mathbf{P}}_k(M)$ |
| 校正机制 | 无                   | 通过逆变换消除训练扰动引入的偏移（Equation 6） |

利用 Lemma 1 得出的仿射关系，本文定义的概率矩阵预测为（Equation 6）：  
$$ \hat{\mathbf{P}}_k(M) = \frac{\hat{\mathbf{P}}(M|\mathbf{A}^{[-k]}) - w_k\theta\mathbf{1}\mathbf{1}^T}{1-w_k}. $$  
该变换将训练网络上的估计 $\hat{\mathbf{P}}(M|\mathbf{A}^{[-k]})$ 逆向映射回原始概率空间，抵消了因随机插补引入的全局收缩与常数偏移。这一“先扰动、后校正”的范式使得 CV‑imputation 分数（Equation 7）  
$$ V_K(M) = \frac{2}{n(n-1)} \sum_{k=1}^{K} \sum_{(v_i,v_j)\in S_k} (\hat{p}_{ij}^{[k]}(M) - a_{ij})^2 $$  
与真实的损失 $L(M)$ 仅相差一个可估计的常数 $\Lambda$，且误差以 $O_p(1/n \vee 1/K^{(1+\alpha)/2} \vee 1/K^\alpha)$ 的速度收敛（Theorem 1）。因此，在模型选择任务中，$V_K(M)$ 的极小化过程渐近等价于最小化 $L(M)$，从而保证了所选模型的渐近最优性。

### 3. 实验证据与失效边界

**合成与真实网络上的实验一致表明，以上两个 changed slots 带来了显著的性能飞跃。** 例如，在 Graphon 1（NS 估计器，$n=200$）下，CV‑imputation 所选模型的 MSE 仅为 $0.51\times10^{-2}$，比 ECV（$9.15\times10^{-2}$）和默认超参数（$39.05\times10^{-2}$）分别降低约 94% 与 98%（Table 1）。在 PolBlog 网络上，CV‑imputation 的 AUC 达到 $0.88$，而 ECV 为 $0.80$（Table 2）；同时计算时间从 258.7 s 缩短至 56.9 s，这得益于随机插补完全规避了 SVD 等大型矩阵分解。方法在不同图估计算器（NS、SAS、USVT、ICE）下均稳定选到 MSE 最低的模型，且随节点数增大，选择准确率提升至 100%（Figure 5）。

**但方法存在明确的适用边界：**
- 仅适用于边缘独立的网络模型（无时序、序列依赖）；动态网络因观测间存在时间耦合，独立性假设被违反。
- 理论保证目前限定在图核（graphon）模型框架内；向随机点积图、度校正随机块模型等的推广仍需严格数学证明。
- 随机插补参数 $\omega$ 固定为 0.5，尽管附录中讨论了鲁棒性，但未进行全面的敏感性分析，可能在某些稀疏或稠密场景下非最优。

总体而言，CV‑imputation 以“随机插补 + 仿射校正”两个 changed slots 重构了网络交叉验证的统计基础，在评估准确性、模型选择可靠性与计算效率三个维度上全面超越现有矩阵补全范式，为网络数据的模型评估提供了兼具理论保障与实用性的新基准。

## 整体框架

针对网络数据交叉验证的核心困难——传统节点分割破坏依赖结构，而边缘采样改变连接分布并引入偏差——本文提出 **CV-imputation**（K 折随机插补图核交叉验证）框架。其关键思想是：在训练时用独立伯努利随机变量替换验证边，切断训练与验证的统计依赖，并利用该扰动下训练分布与原始分布的仿射关系，通过显式校正获得对真实连接概率的无偏预测，进而构造出与均方误差渐近平行的交叉验证分数。

整体 pipeline 由五个模块级联构成，输入为观测到的邻接矩阵 $\mathbf{A}$（满足 $a_{ij} \stackrel{\mathrm{ind}}{\sim} \mathrm{Ber}(p_{ij})$），输出为最小化交叉验证分数的模型或超参数。

1. **节点对随机分割**  
   将全部 $\frac{n(n-1)}{2}$ 个无序节点对随机均分为 $K$ 折，记为 $S_1,\dots,S_K$。每一折 $S_k$ 在训练阶段充当验证集，其余节点对构成训练边。

2. **训练邻接矩阵构造**  
   对第 $k$ 折，构造训练矩阵 $\mathbf{A}^{[-k]}$：
   $$
   \mathbf{A}_{ij}^{[-k]} = \begin{cases}
   a_{ij} & \text{if } (v_i,v_j)\notin S_k \\
   b_{ij} & \text{otherwise}
   \end{cases}
   $$
   其中 $b_{ij}\stackrel{\mathrm{i.i.d.}}{\sim}\mathrm{Ber}(\omega)$ 与观测边独立。该步骤使训练集与验证集满足独立性（Lemma 1），同时训练数据的期望 $\mathbf{P}^{[-k]}$ 成为原始概率矩阵 $\mathbf{P}$ 的仿射变换：
   $$
   \mathbf{P}^{[-k]} = w_k\theta\mathbf{1}\mathbf{1}^T + (1-w_k)\mathbf{P},
   $$
   $w_k=1/K$，$\theta$ 与 $\omega$ 相关。

3. **图核概率矩阵估计**  
   以 $\mathbf{A}^{[-k]}$ 为输入，利用指定的图估计器（如 NS、SAS、USVT、ICE）获得对训练均值 $\mathbf{P}^{[-k]}$ 的估计 $\hat{\mathbf{P}}(M|\mathbf{A}^{[-k]})$，其中 $M$ 代表模型及超参数（Algorithm 1）。该估计器可替换，框架保持模型无关性。

4. **仿射变换校正**  
   通过反转训练均值与原始 $\mathbf{P}$ 的仿射关系，从训练估计恢复对原始概率矩阵的无偏预测：
   $$
   \hat{\mathbf{P}}_k(M) = \frac{\hat{\mathbf{P}}(M|\mathbf{A}^{[-k]}) - w_k\theta\mathbf{1}\mathbf{1}^T}{1-w_k}.
   $$
   该校正利用已知的插补参数 $\omega$ 和训练比例 $w_k$，确保预测以原始 $\mathbf{P}$ 为目标。

5. **预测误差计算与汇总**  
   在第 $k$ 折的验证边 $S_k$ 上计算平方误差，跨折平均得到交叉验证分数：
   $$
   V_K(M) = \frac{2}{n(n-1)}\sum_{k=1}^{K}\sum_{(v_i,v_j)\in S_k} (\hat{p}_{ij}^{[k]}(M) - a_{ij})^2.
   $$
   最终选择 $\hat{M} = \arg\min_M V_K(M)$。理论保证（Theorem 1）表明 $V_K(M)$ 是真实损失 $L(M)$ 加常数 $\Lambda$ 的相合估计，所选模型渐近收敛至 MSE 最优模型。

该框架的突出优势在于：① **计算高效**，避免了 ECV 中昂贵的 SVD 矩阵补全步骤；② **统计无偏**，通过随机插补与仿射校正从根本上解决了依赖性和分布偏移问题；③ **普遍适用**，可与任意图估计器组合，且无需额外调参（除 $K$ 和 $\omega$，其中 $\omega$ 通常固定为 0.5）。需注意的是，上述保证建立在边缘独立假设（如 graphon 模型）之上，扩展到更一般的依赖结构仍需进一步研究。

## 核心模块与公式推导

CV‑imputation 通过**随机边缘插补**与**仿射变换校正**，将网络交叉验证转化为一个可解的统计估计问题。其关键洞察是：在训练阶段用独立的伯努利随机变量替代验证边，既切断了训练集与验证集之间的统计依赖，又保留了原始连接概率矩阵的仿射结构，从而能够从扰动后的训练网络上恢复对原始概率矩阵的无偏预测。整个方法由五个核心模块串联构成，每个模块对应一个明确的数学操作。

### 关键模块
1. **节点对随机分割**：将网络中所有可能的节点对（不包括自环）随机均匀划分为 $K$ 个等大的子集 $S_1, S_2, \dots, S_K$，作为后续交叉验证的折划分。
2. **训练邻接矩阵构造**：对于第 $k$ 折，保持训练边（不在 $S_k$ 中的节点对）上的观测值不变，将验证边（属于 $S_k$ 的节点对）替换为独立同分布的伯努利样本 $b_{ij} \sim \mathrm{Ber}(\omega)$，得到训练矩阵 $\mathbf{A}^{[-k]}$。
3. **概率矩阵估计**：在训练矩阵 $\mathbf{A}^{[-k]}$ 上使用任意图核估计器（如 NS、SAS、USVT、ICE）获得预测的概率矩阵 $\hat{\mathbf{P}}(M \mid \mathbf{A}^{[-k]})$，其中 $M$ 为模型超参数。
4. **仿射变换校正**：利用训练矩阵期望与原始概率矩阵之间的仿射关系，从 $\hat{\mathbf{P}}(M \mid \mathbf{A}^{[-k]})$ 反解出对原始 $\mathbf{P}$ 的预测 $\hat{\mathbf{P}}_k(M)$。
5. **预测误差计算与汇总**：计算在所有验证边上的平方预测误差，跨折平均得到交叉验证分数 $V_K(M)$，选择最小化 $V_K(M)$ 的模型作为最终选择。

### 核心公式与推导
以下公式是方法的数学骨架，所有变量含义在公式下方统一说明。

**（a）数据生成模型**
$$
a_{ij} \stackrel{\mathrm{ind}}{\sim} \mathrm{Ber}(p_{ij}) \tag{1}
$$
$$
p_{ij} = f(\mu_i, \mu_j) \tag{2}
$$
- $a_{ij} \in \{0,1\}$：节点 $i$ 与 $j$ 之间是否存在边。
- $p_{ij}$：连接概率，由对称图核函数 $f$ 及节点潜在位置 $\mu$ 唯一确定。

**（b）模型评估目标——均方误差**
$$
L(M) = \frac{1}{n(n-1)} \|\hat{\mathbf{P}}(M \mid \mathbf{A}) - \mathbf{P}\|_F^2 \tag{3}
$$
- $\hat{\mathbf{P}}(M \mid \mathbf{A})$：基于全观测邻接矩阵 $\mathbf{A}$ 与模型 $M$ 估计的概率矩阵。
- $\mathbf{P}$：真实连接概率矩阵。
- 该损失衡量模型对底层概率结构的恢复能力，但不可直接计算（$\mathbf{P}$ 未知），需要可实际使用的代理损失。

**（c）训练邻接矩阵的构造**
$$
\mathbf{A}_{ij}^{[-k]} = 
\begin{cases}
a_{ij} & \text{if } (v_i, v_j) \notin S_k \\
b_{ij} & \text{otherwise}
\end{cases} \tag{4}
$$
- $S_k$：第 $k$ 折的验证节点对集合。
- $b_{ij} \sim \mathrm{Ber}(\omega)$：独立同分布的随机插补值，与观测数据独立。

**（d）训练矩阵期望的仿射关系**
$$
\mathbf{P}^{[-k]} = \mathbb{E}[\mathbf{A}^{[-k]}] = w_k \theta \mathbf{1}\mathbf{1}^T + (1-w_k)\mathbf{P} \tag{5}
$$
- $\mathbf{P}^{[-k]}$：训练矩阵的期望概率矩阵。
- $w_k$：由折划分比例决定的权重系数。
- $\theta$：由插补参数 $\omega$ 及采样机制产生的常数偏移项。
- 该仿射关系是后续校正的数学基础，保证了从训练估计可线性恢复到原始 $\mathbf{P}$。

**（e）原始概率矩阵的预测**
$$
\hat{\mathbf{P}}_k(M) = \frac{\hat{\mathbf{P}}(M \mid \mathbf{A}^{[-k]}) - w_k \theta \mathbf{1}\mathbf{1}^T}{1-w_k} \tag{6}
$$
- 给定训练矩阵下的估计 $\hat{\mathbf{P}}(M \mid \mathbf{A}^{[-k]})$ 经过线性去偏，得到对 $\mathbf{P}$ 的无偏预测。
- 该预测直接用于后续的验证误差计算。

**（f）$K$ 折交叉验证分数**
$$
V_K(M) = \frac{2}{n(n-1)} \sum_{k=1}^{K} \sum_{(v_i, v_j) \in S_k} \big( \hat{p}_{ij}^{[k]}(M) - a_{ij} \big)^2 \tag{7}
$$
- $V_K(M)$ 即 CV‑imputation 对模型 $M$ 的评分，值越小表示模型预测能力越强。
- 分子 2 用于补偿无向边对称计数，确保损失尺度与 (3) 式可比。

**（g）渐近一致性**
$$
V_K(M) - L(M) - \Lambda = O_p\left(\frac{1}{n} \vee \frac{1}{K^{(1+\alpha)/2}} \vee \frac{1}{K^{\alpha}}\right) \tag{Theorem 1}
$$
- $\Lambda$：与模型无关的常数偏移，因插补所引入的期望结构差异。
- 该定理保证：当节点数 $n$ 和折数 $K$ 充分大时，$V_K(M)$ 与真实损失 $L(M)$ 的差几乎固定，因此最小化 $V_K(M)$ 与最小化 $L(M)$ 所选择的模型渐近一致。

> 上述公式中，所有未在正文定义的符号（如 $w_k, \theta$）均由折划分设计和 $\omega$ 完全确定，使用中无需额外调节；具体推导细节可参见原文 Lemma 1 与相应附录。

本模块全景展现了 CV‑imputation 从数据扰动、概率校正到泛化误差估计的闭环逻辑。五个模块与七个核心公式共同构成了方法的技术主干，也是后续实验对比与消融分析的理论基石。

## 实验与分析

网络交叉验证面临的核心瓶颈在于，传统的随机节点分割破坏了节点之间的相互依赖，而直接的边采样则会改变网络拓扑和连接分布，引入显著的评估偏差[^1]。CV‑imputation 通过随机插补与仿射校正解决了这一困境：在训练阶段，验证集上的边被独立的伯努利随机变量替换，切断了训练‑验证间的统计依赖（Lemma 1）；随后，利用训练分布与原分布的仿射关系（Equation 6）恢复出对原始连接概率矩阵的无偏预测，从而构造出一个与真实均方误差渐近平行的 CV 分数（Theorem 1）。以下实验系统评估该方法在合成与真实网络上的性能。

[^1]: 这一瓶颈在本工作中通过 Lemma 1 的理论保证被突破，Lemma 1 确保了训练集与验证集的条件独立，以及训练数据期望是原概率矩阵的仿射变换。

### 主实验结果

**合成数据上的模型选择（Table 1）**  
在四个图核（Graphon 1‑4）和四种图估计算器（NS、SAS、USVT、ICE）上，CV‑imputation 均能挑选出 MSE 最低的模型，其 MSE 均值较 ECV 和默认选择大幅降低。例如，对于 Graphon 1 和 NS 估计器（n=200），CV‑imputation 的 MSE 仅为 0.51±0.07（×10⁻²），而 ECV 高达 9.15±19.25，默认选择（M=1）更是达到 39.05±3.33，降幅分别约 94% 和 98%。类似趋势出现在几乎所有估计器‑图核组合中：CV‑imputation 始终取得最低或接近最低的 MSE，同时标准差很小，表明选择过程稳定。默认选择往往失败，再次证明超参数调优的必要性。

![[assets/figures/papers/iclr26_0016_8J3GTeQmwl_Graphon_Cross-Validation_Assessing_Models_on_Net/figures/003_Table_1.jpg]]
*Table 1: The mean ± standard deviation of MSE across 100 replicates are calculated using M selected by CV-imputation, ECV, and default selection. To facilitate comparison, all values are multiplied by 100. Note that ICE does not have a default model setup, so the default ICE results are not shown in this table*

**真实网络上的链接预测（Table 2）**  
在三个大规模网络上比较 AUC 与计算时间：  
- **PolBlog 网络**：CV‑imputation 取得 AUC = 0.88±0.01，较 ECV 的 0.80±0.02 提升 0.08。  
- **NetSci 合著网络**：AUC 从 0.70±0.01（ECV）提升至 0.72±0.01。  
- **Yeast 蛋白质相互作用网络**：两种方法 AUC 持平（均为 0.80±0.02），无显著差异。  

![[assets/figures/papers/iclr26_0016_8J3GTeQmwl_Graphon_Cross-Validation_Assessing_Models_on_Net/figures/010_Table_2.jpg]]
*Table 2: AUC (average standard deviation) and computational time in minutes (average standard deviation) of CV-imputation and ECV, over 100 replications*

这表明 CV‑imputation 至少不会劣于 ECV，且在部分网络上带来实质性增益。更重要的是，计算效率优势显著：所有数据集上 CV‑imputation 的计算时间均远低于 ECV（如 PolBlog 上 56.9 s vs 258.7 s），避免了后者必需的昂贵矩阵补全步骤。

**计算效率的压倒性优势（Figures 3, 5 下方）**  
无论使用哪种图核和估计器，随着节点数 n 和折数 K 的增长，ECV 的耗时快速膨胀，而 CV‑imputation 始终维持较低水平（部分情形下快 2‑10 倍）。例如在 NS 方法上，n=200 时 CV‑imputation 的平均时间仅为 ECV 的约 1/5。这一效率来源于随机插补无需迭代优化或矩阵分解，使其尤其适合大规模网络分析。

![[assets/figures/papers/iclr26_0016_8J3GTeQmwl_Graphon_Cross-Validation_Assessing_Models_on_Net/figures/006_Figure_5.jpg]]
*Figure 5: Method selection performance across different graphon designs. The plots display the average selection accuracy and computational time (in seconds) for Graphons 1 to 4, arranged from left to right. The top panel illustrates CV-imputation’s model selection accuracy as n increases from 50 to 200 in steps of 50, while the bottom panel shows the corresponding computational time. Here, accuracy is defined as the percentage of cases where the model with the smallest mean squared error (MSE) is selected from the top-tuned estimators obtained using NS, SAS, USVT, and ICE, respectively*

![[assets/figures/papers/iclr26_0016_8J3GTeQmwl_Graphon_Cross-Validation_Assessing_Models_on_Net/figures/005_Figure_3.jpg]]
*Figure 3: The plots display the average computational time (in seconds) for Graphons 1 to 4 with n → {50, 100, 150, 200}, arranged from left to right. The panel from top to bottom corresponds to the NS method, the USVT method, the SAS method, and the ICE method, respectively. Figure 4: Plotted here are the scores for CV-imputation (red) and MSE (black) under varying values of the tuning parameters for the NS method. We vary the neighborhood size parameter M from 0.5 to 5 with increments of 0.5, while the number of nodes n ranges from 50 to 200 with an increment of 50. Each row corresponds to a specific graphon function listed in Figure 2*

### 消融研究

**模型选择准确率随 n 提升至完美（Figure 5 上方）**  
当 n=50 时，CV‑imputation 在四个图核上的选择准确率已超过 60‑80%；随着 n 增大，准确率单调提升，至 n=200 时在所有图核上均达到 100%。这一趋势与理论预测一致：随着网络规模增大，CV‑imputation 分数与真实 MSE 的平行关系愈发精确，保证了选出的模型渐近最优。

**对多种估计器的通用性（Table 1）**  
无论是基于邻域平滑的 NS，还是低秩近似的 USVT 和 ICE，CV‑imputation 均能为其选择出低 MSE 的模型。从未出现 ECV 优于 CV‑imputation 的情况，证明随机插补与仿射校正的通用性，不依赖于特定估计器的结构假设。

**代理损失的有效性（Figure 4）**  
通过对比 CV‑imputation 分数与真实 MSE 随超参数（如邻域大小 M）的变化曲线，可以看出当 n≥200 时，两条曲线的峰谷形态、最优值位置高度一致。这说明 CV‑imputation 分数是 MSE 的良好代理，可以替代不可观察的真实损失来指导超参数调优。

### 失败模式与局限

- **模型假设边界**：方法的核心推导依赖边缘独立和图核模型（graphon）。对于具有时序依赖的动态网络，或带有节点协变量、权重边等复杂结构的网络，边独立性被打破，随机插补无法切断依赖，仿射校正也将失效。目前该方法不能直接适用。
- **理论覆盖不足**：现有渐近一致性定理（Theorem 1）仅在图核框架下建立，对于随机点积图、度校正随机块模型等更一般的潜在空间模型，尚缺少严格理论保证。实验表明 CV‑imputation 在这些模型上亦能工作，但理论上的推广是待解问题。
- **插补概率 ω 的敏感性未知**：实验中 ω 固定为 0.5，附录虽讨论了鲁棒性，但未系统研究不同 ω 对模型选择准确率和最终预测效果的影响。在更稀疏或密集的网络中，固定的 ω 可能引入不必要的偏差。
- **因估计器而异的计算瓶颈**：CV‑imputation 虽优于 ECV，但其计算时间仍由所选图估计器决定。对于极大规模网络（n > 10⁴），若估计器本身复杂度高，整个流程依然可能耗时过长，需结合子采样或近似算法。
- **判别力不足的案例**：在 Yeast 网络上，CV‑imputation 与 ECV 的 AUC 平分秋色，未能展现显著优势，暗示在某些网络结构下简单的矩阵补全可能同样胜任。不过，即使如此，CV‑imputation 仍以更低计算成本达到同等效果。

### 重要图表结论速览

- **Table 1**：合成实验中，CV‑imputation 的 MSE 较 ECV 和默认选择下降超过一个数量级，并且展示出低方差特性。  
- **Table 2**：三个真实网络中，CV‑imputation 在两个网络上取得更高 AUC，全部网络上耗时远低于 ECV（最高缩短 4.5 倍）。  
- **Figure 3 与 Figure 5（下方）**：计算时间曲线清晰表明 CV‑imputation 避免了 ECV 中代价高昂的奇异值分解或矩阵补全，计算效率碾压优势随 n 递增。  
- **Figure 5（上方）**：选择准确率随 n 快速收敛至 100%，验证了方法的渐近最优行为。  
- **Figure 4**：CV‑imputation 分数与真实 MSE 曲线高度吻合，为将其作为模型选择的代理损失提供了可信凭据。

综上，CV‑imputation 在准确性、泛化性和计算效率三个维度均表现出显著优势，其核心机制——随机插补加仿射校正——有效绕过了网络交叉验证的传统障碍，为网络数据上的模型评估与超参数选择提供了一个可靠且实用的框架。

## 方法谱系与知识库定位

### 与基线方法的对比关系

CV‑imputation 是在 ECV (Edge Cross‑Validation) 基础上发展的网络交叉验证方法，二者的核心分歧在于如何处理被拆分的验证边。ECV 沿用矩阵补全思路，通过 SVD 等算法填补缺失的边，再基于补全后的邻接矩阵评估模型；这一过程不仅破坏了训练集与验证集之间的统计独立性，而且高昂的矩阵分解开销随节点数急剧增长。CV‑imputation 对此做了两处关键改动（见 `changed_slots`）：

1. **验证边处理**：不再试图重建缺失值，而是将验证边替换为独立的伯努利随机变量（随机插补，Equation 4）。Lemma 1 证明，这样构造的训练集在给定真值矩阵 $\mathbf{P}$ 下与验证集独立，且训练数据的期望是原概率矩阵的仿射变换 $\mathbf{P}^{[-k]} = w_k\theta\mathbf{1}\mathbf{1}^T + (1-w_k)\mathbf{P}$。  
2. **概率矩阵校正**：利用这一仿射关系，从训练集估计 $\hat{\mathbf{P}}(M|\mathbf{A}^{[-k]})$ 中恢复出原概率矩阵的预测 $\hat{\mathbf{P}}_k(M)$（Equation 6），而非直接使用训练估计作为最终输出。

这两项设计使 CV‑imputation 在模型选择中获得了弱于 ECV 的偏差和远低于 ECV 的计算成本。合成实验（Table 1）显示，在对图核 1 采用 NS 估计器时，CV‑imputation 的 MSE 仅为 ECV 的约 5.6%，且标准差显著更小（0.51±0.07 vs 9.15±19.25）。真实网络上的 AUC 也普遍更高：PolBlog 网络上 CV‑imputation 达到 0.88，比 ECV 高 0.08；NetSci 网络上领先 0.02；仅 Yeast 网络上两者 AUC 持平（Table 2）。计算时间方面，CV‑imputation 始终快于 ECV（Figure 3），例如在 NS 方法上耗时少于 ECV 的 1/2～1/10。上述对比在同一台机器上完成，ECV 的 SVD 开销属于其方法固有特性，并非不公平比较。

值得注意的是，CV‑imputation 并非简单的“ECV 加速版”：其关键因果干预在于通过随机插补切断了训练与验证的依赖通路，再以显式仿射变换实现分布校正，从而在机制上规避了边采样对网络拓扑与连接分布的破坏。因此，CV‑imputation 不仅是一种更快的替代方案，更代表了一类基于“随机扰动‑校正”范式的网络交叉验证新思路。

### 适用边界

CV‑imputation 的有效性建立在三个相互关联的前提之上。

**边缘独立假设**是该方法的理论基础。观测网络被建模为 $a_{ij} \stackrel{\mathrm{ind}}{\sim} \mathrm{Ber}(p_{ij})$，且连接概率由对称图核 $p_{ij} = f(\mu_i,\mu_j)$ 生成（Equation 1–2）。这一设定直接排除了具有时间演化、序列依赖或动态交互的网络，因为扰动后的训练矩阵将不再满足 Lemma 1 要求的边缘独立性。

**理论保证目前仅在图核模型框架下建立**。Theorem 1 证明了 CV‑imputation 分数 $V_K(M)$ 与真实均方误差 $L(M)$ 之差以常数 $\Lambda$ 为极限，误差随 $n$ 和 $K$ 收敛，由此所选模型渐近最优。该证明尚未推广到更一般的潜在空间模型（如随机点积图、度校正随机块模型）或广义稀疏图核，尽管这些模型常被视为图核的特例，但在缺乏严格数学推导的情况下，将 CV‑imputation 应用于此类模型需要谨慎。

**实际表现受估计器能力与网络特征共同影响**。从实验看，CV‑imputation 在不同网络上的增益幅度存在差异：在 PolBlog（高度极化博客网络）上 AUC 提升达 8%；而在 Yeast 蛋白相互作用网络上与 ECV 无显著差别（Table 2）。这表明方法的相对优势可能依赖于网络的密度、社区强度或估计器在该网络上的适应性。此外，CV‑imputation 本身是一种模型选择框架，其性能上限受底层图估计器（如 NS、USVT、SAS、ICE）的泛化能力约束——若估计器在扰动数据上表现不佳，则校正后的预测 $\hat{\mathbf{P}}_k(M)$ 也可能劣化，进而影响模型排序。

**使用场景建议**：CV‑imputation 适用于静态、无协变量的二值网络模型选择和超参数调优，尤其在需要频繁评估不同模型的计算受限场景下，其轻量级优势突出。对于动态网络、含节点属性或权重边的网络，以及高度稀疏的图核（如 $p_{ij} = o(\log n/n)$），目前缺乏系统评估，不宜直接套用。

### 主要局限

论文自身识别出的局限以及实验观察反映出的边界问题可归纳为以下几点。

1. **独立性假设的刚性**。方法仅适用于边缘独立的网络模型，无法处理具有时间或序列依赖的网络数据（原文局限 1）。即便是静态网络，若边缘间存在高阶依赖（如局部三角闭合效应），随机插补也会破坏这种结构，导致训练分布失真。

2. **理论框架不完整**。当前收敛性证明严格限定于图核模型，对于更广泛的潜在空间类模型或广义稀疏图核，缺少统计保证（原文局限 2）。尽管本文作者将其列为开放问题，但已发表的定理无法直接迁移。

3. **插补参数 $\omega$ 缺乏系统分析**。随机插补的伯努利成功概率 $\omega$ 被固定为 0.5，作者在附录中论证了其鲁棒性，但主实验并未对比 $\omega$ 的不同取值对模型选择准确率、MSE 或 AUC 的影响（原文局限 3）。对于极端稀疏或密集的网络，$\omega=0.5$ 可能不是最优设置，但目前没有理论或实验支撑自适应选择。

4. **计算效率依赖于估计器的复杂度**。虽然 CV‑imputation 免去了 ECV 中的 SVD，但总体耗时仍由所选图估计器主导（原文局限 4）。在网络规模极大（如 $n\ge 10^4$）时，即使采用 CV‑imputation，某些估计器本身的计算量仍然可能成为瓶颈，需要结合子采样或分布式算法。

5. **未覆盖复杂真实网络的鲁棒性测试**。现有实验主要在合成图核和少数真实网络上进行，未考察存在缺失数据、异常节点、测量噪声或网络采样偏差时的表现。因此，CV‑imputation 在“脏数据”条件下的可靠性有待验证（此点虽未在原文明确列出，但从实验设计范围看是自然的局限性）。

### 开放问题

围绕 CV‑imputation 的改进与拓展，论文提出或隐含了以下研究方向。

- **超越图核的理论保证**：能否为随机点积图、度校正随机块模型等更一般的潜在空间网络建立 CV‑imputation 的一致性证明？这需要重新审视 Lemma 1 中的仿射关系在这些模型下是否仍然成立，或设计相应的变形（源自开放问题 1）。

- **$\omega$ 的自适应与最优设计**：是否存在依赖网络稀疏度或图核平滑度的最优 $\omega$？能否在交叉验证过程中以数据驱动的方式自适应调整插补参数（源自开放问题 2）？初步结论表明 $\omega=0.5$ 在多数场景下有效，但缺乏理论解释。

- **通用拟合优度检验框架**：CV‑imputation 的分数 $V_K(M)$ 减去常数 $\Lambda$ 后可作为均方误差的代理，是否有可能将其标准化，构造用于图核模型拟合优度检验的统计量？这需要推导 $V_K(M)$ 在原假设下的渐近分布（源自开放问题 3）。

- **复杂网络结构的适配**：对于带有时间戳的序列网络、多重网络、加权网络或包含节点协变量的网络，如何推广随机插补与仿射校正的范式？这可能需要设计保留条件依赖结构的局部扰动策略，而非全网络均匀插补（源自开放问题 4）。

- **K 折最优选择与有限样本理论**：当前 Theorem 1 给出 $K\to\infty$ 时的渐近结果，但在实际中 $K$ 常取 5 或 10。如何在样本量有限或网络高度异质时确定最优 $K$，并给出非渐近的误差界，是提升方法实用性的关键。

- **与其他网络评估范式的融合**：近年来涌现了基于重采样、网络自助法或信息准则的评估方法，CV‑imputation 能否与这些方法形成互补，例如通过 Bootstrap 调整 $\omega$ 或提供置信区间，值得探索。

### 在知识库中的定位

在“网络数据模型评估”这一脉络中，CV‑imputation 填补了 graphon 框架下缺乏严格且高效交叉验证方法的空白。在它之前，ECV 是事实上最系统的尝试，但其理论与计算缺陷限制了适用范围；更早的节点拆分或边删除策略则因破坏依赖结构而未能提供可靠的模型选择准则。CV‑imputation 首次通过“随机插补‑仿射校正”实现了以下突破：

- **机制创新**：用简单的随机扰动打破训练‑验证依赖，再用显式分布变换进行校正，为其他依赖数据（如时空网络、超图）的评估问题提供了可复用的设计模板。
- **理论支撑**：在 graphon 类模型上给出了分数与真实损失渐近平行的严格证明，为模型选择的一致性奠定了理论基础。
- **实用优势**：模型无关、无额外调参需求，且计算效率远超 ECV，使其成为静态网络超参数调优与估计器比较的 ready-to-use 工具。

目前尚未出现直接针对该方法体系的 follow‑up 工作，但开放问题已指明了明确的扩展路径。若后续能在更一般的潜在空间模型、自适应 $\omega$ 设计以及复杂网络适应性上取得进展，CV‑imputation 有望从“graphon 专用工具”升级为“网络模型通用评估框架”。在现阶段，该方法为各种图核估计器（NS、SAS、USVT、ICE 等）提供了一个公平且高效的模型选择基座，显著降低了网络分析中“如何选模型”这一核心问题的执行门槛。

## 原文 PDF

![[paperPDFs/ICLR_2026/Graphon_Cross_Validation_Assessing_Models_on_Network_Data.pdf]]
