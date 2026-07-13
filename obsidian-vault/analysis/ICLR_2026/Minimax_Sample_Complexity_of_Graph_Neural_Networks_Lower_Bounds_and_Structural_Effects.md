---
title: "Minimax Sample Complexity of Graph Neural Networks: Lower Bounds and Structural Effects"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Minimax_Sample_Complexity_of_Graph_Neural_Networks_Lower_Bounds_and_Structural_Effects.pdf
project_link: null
code_link: null
aliases:
- RG
- MSCGNNLBSE
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/graph_neural_networks
core_operator: "谱同质条件 λ₂ ≤ κ/log n 是迫使模型从 1/√n 模式切换到 d/log n 模式的关键结构因素。"
primary_logic: "图拓扑（同质性、谱扩张、混合时间）而非仅仅网络架构，从根本上决定了GNN的样本复杂度。"
claims:
- "Synthetic-FanoWorstCase (Thm-1) 实例的 Ratio₁(n) 近乎常数 1，验证了 √(log d / n) 缩放率。"
- "ogbn_arxiv、ogbn_products_50k、Reddit_50k 上的 Ratio₂(n) 保持稳定，Ratio₁(n) 升高，证明真实数据遵循 d/log n 缩放率。"
- "所有真实图的谱间隙 λ₂ ≤ κ₀/log n，满足定理 2 的谱同质条件。"
- "使用 Fano 不等式和 Varshamov-Gilbert 码的打包构造严格证明了定理 1 和定理 2 的下界。"
---

# Minimax Sample Complexity of Graph Neural Networks: Lower Bounds and Structural Effects

> [!tip] 核心洞察
> 图拓扑（同质性、谱扩张、混合时间）而非仅仅网络架构，从根本上决定了GNN的样本复杂度。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 图神经网络的极小极大样本复杂度：下界与结构性效应 |
| 英文题名 | Minimax Sample Complexity of Graph Neural Networks: Lower Bounds and Structural Effects |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=P2GIT8LpV2) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/graph_neural_networks |
| Method | ReLU 消息传递 GNN 的极小极大分析框架 |
| Dataset | ogbn_products_50k (GAT, GCN, GraphSAGE), ogbn_arxiv, Reddit_50k, Synthetic-FanoWorstCase (Thm-1), WorstCase_Bottleneck_20k |

> [!tip] 效果简介
> - ogbn_products_50k (GAT, GCN, GraphSAGE) 上，最佳拟合缩放律 为 c + δ/log n，对比 c + α/√n，变化 d/log n 为所有三个架构的最佳拟合，优于 1/√n 和 1/n。
> - ogbn_arxiv, Reddit_50k 上，比率诊断（Ratio₂ vs Ratio₁） 为 Ratio₂(n) = Err(n) / (d/log n)，对比 Ratio₁(n) = Err(n) / √(log d/n)，变化 Ratio₂ 在 n 增大时保持平坦，Ratio₁ 持续上升，表明 d/log n 缩放一致。
> - Synthetic-FanoWorstCase (Thm-1) 上，比率诊断（Ratio₁ vs Ratio₂） 为 Ratio₁(n) = Err(n) / √(log d/n)，对比 Ratio₂(n) = Err(n) / (d/log n)，变化 Ratio₁ 恒定 ~1，Ratio₂ 下降，唯一支持 √(log d/n) 缩放。

## 概要

图神经网络（GNN）的泛化能力不仅取决于模型容量，更根本地受限于底层图的结构特性。本文针对 ReLU 消息传递 GNN，建立了极小极大样本复杂度的统一分析框架，揭示了图拓扑——尤其是同质性与谱扩张——在不同设置下如何决定性地区分两种迥异的收敛速率。核心问题在于：给定一个图，GNN 需要多少训练样本才能可靠泛化？哪些图属性会从根本上拉低样本效率？

文章的核心结论给出清晰答案。对于无结构约束的任意图，归纳式（图级）极小极大风险下界为

$$ \mathcal{R}_n^{\mathrm{graph}}(\mathcal{F}_{\mathrm{GNN}}) \ge K_{\mathrm{new}} \frac{\sigma v_s}{L} \sqrt{\frac{\log d}{n}} ，$$

与经典的非参数速率 $1/\sqrt{n}$ 及输入维度的对数成正比，证明在此设置下 GNN 的样本效率与普通前馈网络本质上相同（定理 1）。然而，当图满足谱同质条件 $\lambda_2(\mathcal{L}) \le \kappa / \log n$ 时——即底层拉普拉斯算子的第二特征值足够小，图呈现慢混合与瓶颈结构——转导式（节点级）极小极大风险的行为发生质变，下界坍缩为

$$ \mathcal{R}_{(n,G)}^{\mathrm{node}}(\mathcal{F}_{\mathrm{GNN}}) \ge \frac{\sigma^2 v_s^2}{\Gamma L^2} \cdot \frac{d}{\log n} ，$$

显著慢于 $1/\sqrt{n}$ 的速率（定理 2）。这种退化的根源在于：慢混合导致消息传递邻域高度重叠，使得相邻节点的标签不再提供独立信息，有效样本量骤降至 $\Theta(\log n)$，从而迫使误差无法比 $d/\log n$ 衰减得更快，且要达到泛化误差 $\epsilon^2$ 所需样本量将指数级增长为 $n \ge \exp(\frac{C d}{\epsilon^2})$。

方法上，论文并未依赖特定的架构设计，而是构建了一个通用的极小极大分析框架。其核心思路是：利用常数权重 Varshamov–Gilbert 码，在 GNN 函数类内部构造具有大分隔距离的打包集合，然后借助固定半径的 Fano 不等式将打包数转化为风险下界。定理 1 的证明通过路径图上的最坏情形构造，直接建立了 $\sqrt{\log d / n}$ 的速率；定理 2 则进一步结合谱同质性下的图结构，将打包按社区块进行分块，推导出 $d / \log n$ 的慢速率。这一分析路径不依赖于特定聚合器的选择，只需满足输入独立的局部聚集假设（A1），使得结论广泛适用于标准 GCN、GraphSAGE 等架构，对注意力机制的扩展亦在讨论之列。

实验部分提供了支撑理论的两个层次证据。合成数据集 Synthetic-FanoWorstCase 直接实例化了定理 1 的打包构造，其误差经 $\sqrt{\log d / n}$ 缩放后的比率 Ratio₁(n) 长期保持常数 ~1，确认了 $n^{-1/2}$ 和 $\sqrt{\log d}$ 的依赖关系。同时，合成瓶颈图 WorstCase_Bottleneck_20k 通过精心设计的社区结构满足谱同质条件，其误差经 $d / \log n$ 缩放后的 Ratio₂(n) 保持平坦，证实了定理 2 的紧致性。在真实世界数据集（ogbn_arxiv、ogbn_products_50k、Reddit_50k）上，GAT、GCN、GraphSAGE 三种代表性架构一致表现出 Ratio₂ 稳定而 Ratio₁ 上升的诊断行为，且最佳拟合的缩放律均为 $c + \delta / \log n$，而非 $c + \alpha / \sqrt{n}$。这与表 1 中各数据集的谱间隙均满足 $\lambda_2 \le \kappa_0 / \log n$ 相验证，表明真实图的混合性质天然地驱动模型进入 $d / \log n$ 的缓慢样本效率区域，这一现象跨越架构差异，指向图结构本身而非网络设计的瓶颈作用。

综上，本文首次从信息论上严格刻画了 GNN 样本复杂度中的图结构效应，区分出两类根本不同的学习速率，并用合成与真实实验双重验证了理论的预测。这些结果不仅为 GNN 泛化限定了可达到的下界，也突出了谱同质性作为核心结构因素的角色，为理解真实图上 GNN 的慢泛化行为以及未来设计突破瓶颈的方法提供了理论起点。



图神经网络（GNN）通过迭代地聚合邻域信息，已成为半监督节点分类和图级预测的核心工具。然而，**其泛化能力与训练样本量之间的理论关系**——即样本复杂度——始终未得到充分澄清。一个根本性的问题是：给定一个图，GNN 需要多少训练节点才能学习到目标函数？更重要的是，图的拓扑结构如何制约这一需求？

现有方法缺口在于，尽管大量研究致力于改进聚合函数、注意力权重或消息传递策略，但鲜有工作**从图结构本身的混合性、同质性和谱性质出发**，系统分析其对 GNN 样本效率的根本限制。常见的统计学习理论预期，非参数模型的极小极大风险通常以 $1/\sqrt{n}$ 的经典速率衰减；但这一直觉在图上可能彻底失效——尤其当图的**谱同质性条件**（即归一化拉普拉斯算子的第二特征值 $\lambda_2 \le \kappa/\log n$）成立时，节点邻域高度重合，有效样本量被压缩至 $\Theta(\log n)$ 的量级，导致风险下界骤降为 $\Omega(d/\log n)$，远慢于前馈网络的典型速率。这一现象揭示了图的慢混合瓶颈：消息传递在密集团簇内迅速均质化，使得不同节点的训练信号高度冗余，统计效率急剧退化。

本文的核心动机在于：**揭示图拓扑——而非仅仅网络架构——才是 GNN 样本复杂度的第一性决定因素**，并建立严格的极小极大分析框架予以量化。具体而言，本文旨在回答两方面的问题：(i) 在任意图上，ReLU GNN 的泛化能力是否存在一个普遍的、与图结构无关的极小极大下界？(ii) 在何种结构条件下，图的本征瓶颈会迫使 GNN 彻底偏离 $1/\sqrt{n}$ 的范式，引发灾难性的样本效率坍缩？

为此，本文构造了基于常数权重 Varshamov–Gilbert 码的信息论下界推导流水线（packing + Fano 不等式），分别针对图级归纳风险与节点级转导风险建立了两个互补的极小极大下界：定理 1 保证 $\sqrt{\log d / n}$ 的普遍速率（适用于任意图），而定理 2 则在谱同质条件下证明风险无法快于 $\Omega(d/\log n)$。后者正是**因果调节变量**——谱间隙 $\lambda_2$ 通过 $\kappa_0 := \max_n \lambda_2(\mathcal{L}_n) \log n$ 捕捉图的社区结构与混合时间——当 $\kappa_0$ 有界时，模型被迫从 $1/\sqrt{n}$ 模式切换至 $d/\log n$ 模式。

实证层面，合成 FanoWorstCase 实例明确验证了定理 1 的 $\sqrt{\log d / n}$ 缩放（Ratio₁ 接近常数 1，Figure 1）；而 **ogbn_arxiv、ogbn_products_50k、Reddit_50k 等真实基准上，所有三种主流 GNN（GCN、GAT、GraphSAGE）的 Ratio₂ 保持平坦，Ratio₁ 持续攀升**，为定理 2 提供了高置信度证据（Figures 2–4；证据强度 0.9–0.95）。结构统计表（Table 1）进一步确认，这些真实图的谱间隙确实满足 $\lambda_2 \le \kappa_0/\log n$ 条件，从而将实体验证锚定于理论断言。合成瓶颈图 WorstCase_Bottleneck_20k 显示 Ratio₂ 稳定，确证了定理 2 下界的紧致性（Figure 5）。综上，这些发现有力表明：**图画下的慢混合几何是 GNN 样本复杂度无法超越的结构性屏障**，任何忽略这一因素的架构或训练策略都注定无法本质性地打破 $d/\log n$ 的瓶颈。



## 核心方法与创新机理

**瓶颈重定义：图拓扑引起的有效样本坍缩，而非模型容量。**  
在慢混合图上，消息传递邻域高度重叠，使得 *n* 个已标记节点所含的独立信息量仅约为 Θ(log *n*)，造成有效样本量坍缩。本文首次严格证明，当归一化拉普拉斯算子的第二特征值 λ₂ ≤ κ/log *n*（谱同质条件）时，节点级转导式极小极大风险下界从经典的 $\sqrt{\log d / n}$ 坍缩为 $\Omega(d / \log n)$，即收敛速率受制于输入维度 *d* 与对数节点数之比，远慢于独立同分布情形。这一瓶颈的产生并不依赖于具体网络架构（GCN、GAT、GraphSAGE），而是由图拓扑的扩张特性所决定。

**因果调节项：谱同质条件作为缩放律切换的开关。**  
λ₂ ≤ κ/log *n* 是迫使模型从 $1/\sqrt{n}$ 模式切换到 *d*/log *n* 模式的关键结构因素。论文不仅定义了该条件，还定量展示了它如何通过限制消息混合速度来降低有效样本量——该条件在 ogbn-arxiv、ogbn-products、Reddit 等真实图上均成立（Table 1），因而这些图上的缩放律一致遵循 *d*/log *n*，而非 $\sqrt{\log d / n}$。

**分析框架创新：面向 ReLU 消息传递 GNN 的极小极大信息论工具链。**  
不同于以往依赖 VC 维或 Rademacher 复杂度的分析，本文构建了一套专门针对 GNN 的极小极大分析管道：
1. **打包集构造**（Appendices C、E、F）：利用常数权重 Varshamov–Gilbert 码与第一层坐标选择器，在路径图上构造出具有大距离的函数集合，为下界提供硬度实例。
2. **Fano 不等式应用**（Lemma 1）：通过控制高斯回归模型下的 KL 散度，将打包度量熵转换为显式的极小极大风险下界。该框架同时处理了图级归纳式风险（Theorem 1：任意图上的 $\sqrt{\log d / n}$ 下界）和节点级转导式风险（Theorem 2：谱同质条件下的 *d*/log *n* 下界），实现了速率紧致性的统一推导。

**实证方法论创新：比率诊断取代曲线拟合。**  
曲线拟合易受噪声、优化偏差与架构差异的混杂，论文因此将其视为次要证据。取而代之的是比率诊断 Ratio₁ = Err(*n*)/$\sqrt{\log d / n}$ 和 Ratio₂ = Err(*n*)/(*d*/log *n*)：若某理论速率正确，对应的比率应在 *n* 增大时保持平坦。合成数据上 Ratio₁ 近常数 1 而 Ratio₂ 下降（Figure 1），直接验证 Theorem 1；三个真实图与合成瓶颈图上 Ratio₂ 平坦、Ratio₁ 持续上升（Figure 2–5），一致支持 Theorem 2 的 *d*/log *n* 缩放。该方法使图结构对缩放律的主导地位能够被清晰分离，独立于特定 GNN 架构。

**相对于现有认知的 changed slots（变更点）：**
- **假设空间**：不再假设训练节点构成独立同分布样本，而是显式建模图拓扑引入的依赖结构与混合时间。
- **决定性因素**：将样本复杂度的决定因素从模型参数量/容量转移至图的谱同质性（λ₂）与混合几何，提出“图拓扑是首要瓶颈”。
- **缩放律形态**：推翻了 GNN 应与 MLP 共享 $1/\sqrt{n}$ 速率的默认预期，在高同质性真实图上确立了显著更慢的 *d*/log *n* 速率，且指出存在从 $1/\sqrt{n}$ 到 *d*/log *n* 的相变可能（由 λ₂ 的大小控制）。
- **推理工具**：以打包集 + Fano 不等式替代容量类方法，使下界能精确捕捉图结构对消息传递的影响，且可直接连接至常数权重码的构造。



本文构建了一个分析框架，用以严格量化 ReLU 消息传递图神经网络（GNN）在图级（归纳式）与节点级（转导式）回归预测中的极小极大样本复杂度，并揭示图拓扑结构（同质性、谱扩张、混合时间）对该复杂度的决定性作用。框架的整体流程由 **问题形式化 → 下界理论构造 → 谱结构分析 → 实验诊断验证** 四个阶段构成，各模块之间通过信息论与图论工具紧密耦合。

**问题设定与风险定义**  
首先明确两类监督学习场景：归纳式图级预测中，训练集由 $n$ 个独立采样的图组成；转导式节点级预测中，在一张固定图上随机选择 $n$ 个有标签节点进行训练。相应的极小极大风险分别定义为：
- 图级风险 $\mathcal{R}_{n}^{\text{graph}}(\mathcal{F}_{\text{GNN}})$（式 (2)），对应任意 $L$ 层 ReLU 消息传递 GNN 类的最坏情况期望平方误差；
- 节点级风险 $\mathcal{R}_{(n,G)}^{\text{node}}(\mathcal{F}_{\text{GNN}})$（式 (3)），衡量固定图 $G$ 上节点预测的极小极大界限。  
模型类 $\mathcal{F}_{\text{GNN}}$ 基于式 (1) 的逐层更新规则 $h_i^{(\ell+1)} = \phi( W^{(\ell)} \operatorname{Agg}_{j\in\mathcal{N}(i)} h_j^{(\ell)} + B^{(\ell)} h_i^{(\ell)})$，$\phi(z)=\max\{0,z\}$，其中聚集函数满足输入无关假设（A1）。

**理论分析流水线**  
理论推导通过三个顺序模块构建下界，贯穿附录 E–H。

1. **构造打包集**（Appendices C、E、F）：利用 Varshamov‑Gilbert 界设计常数权重二进制码，并映射为 GNN 第一层权重的坐标选择器，从而在函数空间 $\mathcal{F}_{\text{GNN}}$ 中构建具有足够大 $L_2$ 距离的 $\delta$‑打包集。该步骤为硬度实例提供信息论基础，打包度量熵下界 $\log\mathcal{M}(2\epsilon,\mathcal{F}_{\text{GNN}},\|\cdot\|_{L_2}) \ge C_A \, v_s^2 \log d / (L^2\epsilon^2)$（Lemma 2）是后续所有下界的核心输入。

2. **信息论下界推导**（Sections E、F；Lemma 1）：将打包集嵌入固定设计的高斯噪声回归模型，利用 KL 散度控制（式 (7) 及相关引理）将函数间的 $L_2$ 距离转换为 $n$ 样本分布间的信息量，再通过 Fano 不等式（固定半径版本）将打包数转化为极小极大风险下界。由此得到：
   - 定理 1：任意图上归纳式风险的统一下界 $\mathcal{R}_n^{\text{graph}} \ge K_{\text{new}} \, \sigma v_s \sqrt{\log d / n}$，与经典 $1/\sqrt{n}$ 速率一致；
   - 定理 2（预备形式）：在谱同质条件下，节点级风险受限于图结构参数。

3. **谱同质条件分析**（Sections 3、G、H）：引入归一化拉普拉斯算子的第二特征值 $\lambda_2(\mathcal{L})$ 来刻画图的混合时间与瓶颈效应。当图满足谱同质条件 $\lambda_2 \le \kappa / \log n$ 时，消息传递邻域高度重叠，有效样本量坍缩至 $K \approx \log n$，使得 Fano 打包划分为 $K$ 个几乎独立的块。此时定理 2 给出节点级风险的严格下界：
   $$\mathcal{R}_{(n,G)}^{\text{node}} \ge \frac{\sigma^2 v_s^2}{\Gamma L^2} \cdot \frac{d}{\log n},$$
   表明在此类图上，模型误差无法以 $1/\sqrt{n}$ 速率衰减，而由维度距 $d$ 和 $\log n$ 支配。

**实验验证流水线**  
实验部分以 **比率诊断** 为核心工具，直接检验两种理论速率的稳定性，避免曲线拟合的混淆偏差。

- **输入**：选择两类图数据——合成图 `Synthetic-FanoWorstCase`（直接实例化定理 1 的打包构造）与 `WorstCase_Bottleneck_20k`（社区瓶颈结构满足谱同质条件）；真实基准 `ogbn_arxiv`、`ogbn_products_50k`、`Reddit_50k`，其结构属性经 Table 1 验证满足 $\lambda_2 \log n \le \kappa_0$。所有图均带有 $d$ 维节点特征与连续型回归标签。
- **模型**：固定三类代表性 GNN 架构（GCN、GAT、GraphSAGE），训练过程仅改变训练节点数 $n$，记录测试误差 $\mathrm{Err}(n)$。
- **诊断指标**：定义比率 $\mathrm{Ratio}_1(n) = \mathrm{Err}(n) / \sqrt{\log d / n}$ 与 $\mathrm{Ratio}_2(n) = \mathrm{Err}(n) / (d / \log n)$，若某一比率随 $n$ 增大保持平坦，则支持对应缩放律。
- **输出**：合成 FanoWorstCase 上 $\mathrm{Ratio}_1(n)$ 近乎常数 1（Figure 1），证实 $\sqrt{\log d / n}$ 缩放；真实数据集与瓶颈合成图上 $\mathrm{Ratio}_2(n)$ 均保持稳定（Figures 2–5），而 $\mathrm{Ratio}_1(n)$ 持续升高，一致支持 $d/\log n$ 的慢缩放率。此外，`ogbn_products_50k` 上的最佳拟合律为 $c + \delta / \log n$（Table 2），进一步佐证上述结论。

**模块关系与信息流**  
理论构造为实验提供可检验的量化预测：打包集构造确定了 $\log d$ 项的来源与 $1/\sqrt{n}$ 的基线；信息论下界将函数的几何分离转化为样本需求；谱同质分析则揭示出真实图中有效样本量坍缩的根本原因，预测了 $d/\log n$ 的异常缩放。实验反过来通过比率稳定性与拟合优度验证这些预测，并确认图拓扑（而非具体网络架构）是决定样本复杂度的主导因素。这一闭环确立了框架的完整性与可复现性。



### 1 消息传递架构与两类风险定义
本研究考虑的 ReLU 图神经网络（GNN）采用标准的消息传递范式，第 $\ell$ 层到第 $\ell+1$ 层的更新为

$$h_i^{(\ell+1)} = \phi\Bigl( W^{(\ell)} \mathrm{Agg}_{j\in\mathcal{N}(i)} h_j^{(\ell)} + \mathcal{B}^{(\ell)} h_i^{(\ell)} \Bigr), \quad \phi(z)=\max\{0,z\},$$

其中 $h_i^{(\ell)}$ 为节点 $i$ 在第 $\ell$ 层的表示，$\mathcal{N}(i)$ 为邻居集合，$\mathrm{Agg}$ 为局部聚合函数（满足输入独立假设 A1），$W^{(\ell)},\mathcal{B}^{(\ell)}$ 为可训练权重，$\phi$ 为 ReLU 激活（Equation 1）。

为刻画样本复杂度极限，定义两类极小极大风险。
- **归纳式（图级）风险**（Equation 2）

$$\mathcal{R}_n^{\mathrm{graph}}(\mathcal{F}_{\mathrm{GNN}}) := \inf_{\hat{f}}\sup_{f^\star\in\mathcal{F}_{\mathrm{GNN}}} \mathbb{E}_{\mathrm{train}}\,\mathbb{E}_{G\sim\mathbb{P}_G}\Bigl[(\hat{f}(G)-f^\star(G))^2\Bigr],$$

其中 $\hat{f}$ 为任意估计器，$f^\star$ 为真实函数，$n$ 为训练图数量，$\mathbb{P}_G$ 为图分布，$\mathcal{F}_{\mathrm{GNN}}$ 为所考虑的 GNN 函数类。
- **转导式（节点级）风险**（Equation 3）

$$\mathcal{R}_{(n,G)}^{\mathrm{node}}(\mathcal{F}_{\mathrm{GNN}}) := \inf_{\hat{f}}\sup_{f^\star\in\mathcal{F}_{\mathrm{GNN}}} \mathbb{E}_{S}\Bigl[\frac{1}{|V|}\sum_{v\in V}(\hat{f}(v)-f^\star(v))^2\Bigr],$$

其中 $G=(V,E)$ 为固定图，训练集 $S$ 包含 $n$ 个有标签节点，期望同时涵盖训练采样和观测噪声。

### 2 打包构造与无结构图的下界
**模块：构造打包集**。 利用第一层权重作为坐标选择器，并借助常重量 Varshamov–Gilbert 码建立大距离的函数集合，为极小极大下界提供硬度实例。核心结果为度量为 $\|\cdot\|_{L_2}$ 的打包数下界（Lemma 2, Equation 6）

$$\log \mathcal{M}(2\epsilon,\mathcal{F}_{\mathrm{GNN}}(v_s,L),\|\cdot\|_{L_2}) \geq C_A\frac{v_s^2}{L^2\epsilon^2}\log d,$$

其中 $\epsilon$ 为分离半径，$v_s$ 为信号振幅，$L$ 为网络深度/权重范数控制参数，$d$ 为输入特征维度，$C_A$ 为常数。

**模块：信息论下界推导**。 在上述打包集上应用固定半径的 Fano 不等式，并结合高斯回归的 KL 散度控制（KL 散度 $\propto$ 训练点上的 $L_2$ 距离平方），可导出对**任意图**的统一下界（Theorem 1, Equation 4）

$$\mathcal{R}_n^{\mathrm{graph}}(\mathcal{F}_{\mathrm{GNN}}) \geq K_{\mathrm{new}}\frac{\sigma v_s}{L}\sqrt{\frac{\log d}{n}},$$

其中 $\sigma$ 为观测噪声标准差，$K_{\mathrm{new}}$ 为数值常数。该速率与标准 $1/\sqrt{n}$ 渐近行为一致，表明在不施加图结构约束时，GNN 的样本复杂度由特征维度对数 $\log d$ 和样本量 $n$ 共同决定。

### 3 谱同质条件与结构化图的下界
**模块：谱同质条件分析**。 当图显示出慢混合特性时，消息传递的邻域高度重叠，导致标签样本的有效信息量坍缩。这一结构因素通过归一化拉普拉斯算子 $\mathcal{L}$ 的第二特征值量化，即**谱同质条件**（Section 3）

$$\lambda_2(\mathcal{L}) \leq \frac{\kappa}{\log n},$$

其中 $\kappa$ 为与图无关的常数。该条件保证图的连通瓶颈限制了信息传播，使得 $n$ 个标注节点不能提供 $n$ 个独立样本。

在谱同质条件下，利用块打包（block packing）技术再次结合 Fano 不等式，可得到节点级风险的更慢下界（Theorem 2, Equation 8）

$$\mathcal{R}_{(n,G)}^{\mathrm{node}}(\mathcal{F}_{\mathrm{GNN}}) \geq \frac{\sigma^2 v_s^2}{\Gamma L^2}\cdot\frac{d}{\log n},$$

其中 $\Gamma$ 为结构常数。此速率远慢于 $1/\sqrt{n}$，从根本上解释了在真实同质图上 GNN 难以通过增加标注节点获得快速增益的现象。等价地，要将泛化误差压制到 $\epsilon^2$ 所需的样本量必须满足（Equation 9）

$$n \geq \exp\Bigl(\frac{\sigma^2 v_s^2\,d}{\Gamma L^2 \epsilon^2}\Bigr),$$

呈指数级依赖于特征维度与误差目标。

### 4 实证诊断比率
为实验验证上述两种缩放律，定义两个无单位的比率诊断量（Section 4）：
- **定理 1 模式检测**： $\displaystyle\mathrm{Ratio}_1(n)=\frac{\mathrm{Err}(n)}{\sqrt{\log d / n}}$
- **定理 2 模式检测**： $\displaystyle\mathrm{Ratio}_2(n)=\frac{\mathrm{Err}(n)}{d / \log n}$

其中 $\mathrm{Err}(n)$ 为测试集上的均方误差。若 $\mathrm{Ratio}_1(n)$ 随 $n$ 保持平坦，则误差按 $1/\sqrt{n}$ 尺度缩；若 $\mathrm{Ratio}_2(n)$ 平坦，则误差由 $d/\log n$ 主导。实证分析正是通过观察这两种比率在合成图与真实图上的稳定性来诊断样本复杂度的主导律。



## 实验与关键发现

### 实验设计与诊断框架
为检验定理1和定理2给出的极小极大缩放速率，作者在三个真实图基准（ogbn_arxiv、ogbn_products_50k、Reddit_50k）和两个受控合成图（Synthetic‑FanoWorstCase、WorstCase_Bottleneck_20k）上，对三种代表性GNN（GCN、GAT、GraphSAGE）进行系统性评估。核心工具是比率诊断：  
$$
\mathrm{Ratio}_1(n)=\frac{\mathrm{Err}(n)}{\sqrt{\log d / n}},\qquad
\mathrm{Ratio}_2(n)=\frac{\mathrm{Err}(n)}{d / \log n},
$$
其中 $\mathrm{Err}(n)$ 为训练集大小 $n$ 时的测试误差，$d$ 为输入维度。若数据遵循某一理论速率，则对应的比率随 $n$ 增大应趋于常数；另一比率则将明显漂移。比率诊断直接检验渐近结构，被作者视为比曲线拟合更可靠的证据，因为曲线拟合可能被噪声、架构偏差和优化方差混淆（verified_analysis limitations）。

### 主结果：缩放律的实证区分

**定理1的验证（任意图下界 $\sqrt{\log d / n}$）**  
在合成 FanoWorstCase 图上，该图直接实例化定理1的打包构造（附录R；Figures 8–9），$\mathrm{Ratio}_1(n)$ 保持近乎常数 ~1，而 $\mathrm{Ratio}_2(n)$ 随 $n$ 增大持续下降（Figure 1）。这一行为表明误差确实按 $\sqrt{\log d / n}$ 衰减，与定理1的极小极大下界一致。相应曲线拟合在 Table 2 中也确认 $1/\sqrt{n}$ 对该合成图是最佳缩放律。

![[assets/figures/papers/iclr26_0014_P2GIT8LpV2_Minimax_Sample_Complexity_of_Graph_Neural_Networ/figures/009_Table_2.jpg]]
*Table 2: Comparison of Fit Metrics Across All Models and Datasets (Updated Results)*

![[assets/figures/papers/iclr26_0014_P2GIT8LpV2_Minimax_Sample_Complexity_of_Graph_Neural_Networ/figures/002_Figure_1.jpg]]
*Figure 1: Stability comparison of scaling-law ratios for Synthetic-FanoWorstCase (Thm-1)*

**定理2的验证（谱同质条件下的 $d/\log n$ 瓶颈）**  
所有三个真实图的归一化拉普拉斯第二特征值均满足谱同质条件 $\lambda_2 \le \kappa_0 / \log n$（Table 1），其中 $\kappa_0$ 为数据集级别的界常数。在此条件下，所有架构的 $\mathrm{Ratio}_2(n)$ 均保持平坦，而 $\mathrm{Ratio}_1(n)$ 随 $n$ 增大明显升高（Figures 2、3、4）。这确凿地表明，真实图上的误差下降速率并非 $1/\sqrt{n}$，而是显著更慢的 $d/\log n$，与定理2的极小极大下界 
$$
\mathcal{R}_{(n,G)}^{\mathrm{node}}(\mathcal{F}_{\mathrm{GNN}}) \geq \frac{\sigma^2 v_s^2}{\Gamma L^2}\cdot\frac{d}{\log n}
$$
相吻合。  
此外，在合成瓶颈图 WorstCase_Bottleneck_20k 上，该图通过社团瓶颈结构直接满足谱同质条件，$\mathrm{Ratio}_2(n)$ 也呈现平坦（Figure 5），进一步证实定理2的紧致性。

![[assets/figures/papers/iclr26_0014_P2GIT8LpV2_Minimax_Sample_Complexity_of_Graph_Neural_Networ/figures/001_Table_1.jpg]]
*Table 1: Graph Structural Properties Relevant to Theorem 2*

![[assets/figures/papers/iclr26_0014_P2GIT8LpV2_Minimax_Sample_Complexity_of_Graph_Neural_Networ/figures/005_Figure_2.jpg]]
*Figure 2: Stability comparison of scaling-law ratios for ogbn_arxiv (left: GAT, middle: GCN, right: GraphSAGE)*

**曲线拟合的侧面印证**  
Table 2 汇总了四种候选缩放律（$c+\alpha/\sqrt{n}$、$c+\beta/n$、$c+\delta/\log n$、$c+\gamma/n^2$）的拟合优度。对于 ogbn_products_50k，所有三种架构的最佳拟合均为 $c+\delta/\log n$（即 $d/\log n$ 速率），而在 ogbn_arxiv 和 Reddit_50k 上，最优拟合有时偏向 $1/n$ 或 $1/\sqrt{n}$，但作者强调曲线拟合仅作为次要证据，因为拟合指标可能受限于有限样本和噪声。

### 消融实验

**构造与理论的直接对应**  
合成图 FanoWorstCase 完全按照定理1的打包构造生成，利用常数权重 Varshamov–Gilbert 码实现维度 $d$ 的对数依赖。实验不仅验证了 $n^{-1/2}$ 的下降斜率（Appendix R；Figure 8），还确认了误差随 $d$ 按 $\sqrt{\log d}$ 增长（Figure 9），与理论预测的 $\sqrt{\log d / n}$ 结构一致。

**架构无关性**  
无论在真实图还是在合成瓶颈图上，GCN、GAT、GraphSAGE 的比率行为高度一致（Figures 2–5）。这表明缩放律由图的谱结构（同质性、混合时间）决定，而非特定 GNN 架构的选择。尤其值得注意的是，尽管定理1的打包构造依赖于输入无关的聚集函数（A1）而排除了标准 GAT 的注意力机制，但在真实图实验中 GAT 仍表现出与另两种架构相同的 $d/\log n$ 行为，提示谱同质效应可能覆盖了架构差异。

![[assets/figures/papers/iclr26_0014_P2GIT8LpV2_Minimax_Sample_Complexity_of_Graph_Neural_Networ/figures/008_Figure_3.jpg]]
*Figure 3: Stability comparison of scaling-law ratios for ogbn_products_50k (left: GAT, middle: GCN, right: GraphSAGE)*

![[assets/figures/papers/iclr26_0014_P2GIT8LpV2_Minimax_Sample_Complexity_of_Graph_Neural_Networ/figures/012_Figure_4.jpg]]
*Figure 4: Stability comparison of scaling-law ratios for Reddit_50k (left: GAT, middle: GCN, right: GraphSAGE)*

### 失败模式与局限

- **定理假设的限制**：定理1的证明依赖聚集函数的输入独立性（A1），直接排除了标准注意力机制（如 GAT）在其打包构造中的作用；定理2虽可扩展至掩码注意力，但要求有界算子范数。当图不满足谱同质条件（例如扩展图）时，$\lambda_2$ 过大将导致定理2的 $d/\log n$ 下界不再成立，此时样本复杂度可能恢复至 $1/\sqrt{n}$ 水平，但该情形尚未经实验验证。
- **图类型的覆盖范围**：实验仅涵盖 ogbn_arxiv、ogbn_products、Reddit 三个真实图及两个受控合成图，未涉及异配图、有向图或强扩张图等更广泛的图结构。对于异配图，谱同质条件可能不再相关，相应的结构度量和缩放律需要独立定义与验证。
- **数据完整性问题**：Reddit_50k 的 GAT 测试准确率数据因日志丢失而缺失（截至提交版本，Table 9 备注说明已重新运行但最终表格尚未更新）；该部分结论需要人工核查后续版本。
- **损失函数假设**：整个理论分析基于平方误差回归与高斯噪声假设。对于分类任务和交叉熵损失，对应的极小极大下界和缩放律尚需单独推导，本文未提供实验证据。
- **曲线拟合的混淆因素**：作者明确指出曲线拟合易受噪声、优化偏差和架构差异的混淆，因此主要结论不依赖单一最优拟合，而是通过比率诊断的视觉稳定性来判断速率。

### 重要图表结论

- **Table 1**：列出所有数据集的 $\lambda_2$、$\kappa_0$ 及同质性，确认真实图均满足谱同质条件，是触发 $d/\log n$ 下界的结构性前提。
- **Figures 1–5**：比率稳定性对比图直接分离了两种缩放律：Figure 1 支持定理1的 $\sqrt{\log d / n}$；Figures 2–4、5 则一致支持定理2的 $d/\log n$，构成全篇实证证据的核心。
- **Figures 8–9**：合成实验的 log‑log 图验证了 $n$ 和 $d$ 的精确依赖关系，为定理1的紧致性提供受控环境下的直接证明。
- **Table 2**：尽管作者视其为次要证据，Table 2 汇总的拟合度量仍为各模型的缩放行为提供了数值参考，尤其表明在 $d/\log n$ 占主导的数据集上，$1/\log n$ 形式的拟合优于传统 $1/\sqrt{n}$ 模型。

> **注意**：上述结论基于论文提供的分析 JSON 和证据锚点，其中部分数值（如 Ratio₁ 的绝对幅度）需查阅原文图表确认。Reddit_50k 的 GAT 结果因数据缺失，其可靠性有待作者更新后再次核验。



## 定位与知识库关联

本工作并非提出一种新的图神经网络架构，而是构造了一个 **信息论极小极大分析框架**，用于精确量化 ReLU 消息传递 GNN 在归纳式（图级）和转导式（节点级）回归任务中的样本复杂度下界。其实验部分以 GCN、GAT、GraphSAGE 三种标准架构作为验证对象，因此这些模型在本研究中充当 **对照基线**，用以检验理论速率的普适性。尽管本文未直接涉及 follow-up 方法，但它通过揭示图谱结构（慢混合与瓶颈）对泛化能力的根本制约，为后续设计更加样本高效的架构、采样策略和预训练方法提供了明确的 **理论基础与改进方向**。核心瓶颈在于：在谱同质条件下，消息传递邻域的高度重叠导致有效样本量坍缩至 $\Theta(\log n)$，从而将下界从经典的非参数速率 $1/\sqrt{n}$ 推向更慢的 $d/\log n$。因果调节枢纽是归一化拉普拉斯第二特征值 $\lambda_2(\mathcal{L})$ 的大小，当满足 $\lambda_2 \leq \kappa/\log n$ 时，系统从快速混合区域切换至 **慢混合模式**。

### 与 baseline 的关系及 follow-up 指向

实验中使用的 GCN、GAT 和 GraphSAGE 均为 **标准标杆架构**，论文并未对它们的网络结构做定制修改，而是将其视为 `ReLU GNN` 类的具体实例。在 ogbn_arxiv、ogbn_products_50k、Reddit_50k 三个真实图数据集上，三种架构的 **比率诊断 Ratio$_2$** 均保持平坦，而 **Ratio$_1$** 持续上升（Figure 2‑4），表明所有模型均服从 $d/\log n$ 缩放，而非 $1/\sqrt{n}$。由此确立了一个与架构选择无关的结构性限制：**图拓扑（同质性、谱间隙、混合时间）主导了 GNN 的样本复杂度**，而非权值参数化或邻域聚合细节。这一发现将现有 GNN 研究从“模型中心”的视角拉向了“数据结构”视角，暗示未来 follow-up 不应仅关注更深的网络或更复杂的注意力，而应着力于 **打破慢混合效应的策略**——如设计感知图瓶颈的采样方式、图增强预训练或分层传播机制，以恢复有效样本量。定理 1 在构造下界时利用了输入独立的聚合函数（A1），直接排除标准 GAT 的注意力系数依赖输入的属性，但定理 2 的扩展可涵盖有界算子范数的掩码注意力，为未来统一分析奠定了桥梁。

### 适用边界与结构假设

理论结果的成立依赖于几个关键假设，划定了方法的适用范围：

1. **聚合函数独立性**（Theorem 1）：要求本地聚合算子不依赖于节点特征，此假设使得图级下界 $\mathcal{R}_n^{\mathrm{graph}} \geq K_{\mathrm{new}} \frac{\sigma v_s}{L} \sqrt{\frac{\log d}{n}}$ 对所有标准 GCN 和 GraphSAGE 成立，但对标准 GAT 不完全适用。  
2. **谱同质条件**（Theorem 2）：核心条件 $\lambda_2(\mathcal{L}) \leq \kappa/\log n$ 要求图具有强瓶颈或弱混合结构，这在实际引文网络、共购网络等普遍满足（Table 1 中所有真实图均满足 $\lambda_2 \leq \kappa_0/\log n$），但在 **强扩张图**（如扩展图或完全图）上不成立。对于扩张图，该下界可能高估真实风险，样本复杂度有望恢复至 $1/\sqrt{n}$ 水平，但论文未给出相应上界或实验验证。  
3. **损失与噪声模型**：全部分析建立在 **平方误差回归** 和高斯噪声假设之上，对分类任务和交叉熵损失的泛化能力需要单独论证。  
4. **实验图类型**：验证仅涵盖 homophily 主导的静态图（同质率 0.316‑0.809），未覆盖异配图、有向图或动态图，因此 $d/\log n$ 速率的普遍性在这些场景下仍需探索。  
5. **最小二乘拟合的可靠性**：论文明确指出，曲线拟合仅作为辅助证据，因噪声、优化偏差及架构差异可能混淆真实速率；**比率诊断**（Ratio$_1$、Ratio$_2$ 的渐进稳定性）是更强有力的证据来源。

### 已知局限与证据强度

实验和理论中的若干局限需要注意：

* 定理 1 的打包构造依赖 **输入独立聚合**（A1），导致 GAT 不直接被覆盖；定理 2 虽通过掩码注意力部分推广，但仍要求有界算子范数，注意力权重的无界性可能打破现有分析。
* 合成瓶颈图 `WorstCase_Bottleneck_20k` 和 `Synthetic‑FanoWorstCase` 虽通过分离结构和编码构造确证了理论紧致性（Figure 5、Figure 1 中 Ratio$_2$ 和 Ratio$_1$ 分别保持平坦），但这些图均受控生成，真实图中的噪声结构可能引入未建模的变异。
* 在 Reddit_50k 数据上，GAT 的准确率数据因日志缺失而缺失，虽已重新运行，但最终表格（截至提交版本）尚未更新。
* 实证常数 $C^\star \approx \mathrm{Err}(n) / (d/\log n)$ 稳定于 10‑25 之间，但其对特征维度 $d$ 的依赖（如 $\sqrt{\log d}$ 或 $d$）尚未通过系统消融（仅合成实验验证了独立于 $n$ 和 $d$ 的幂律）。
* 对比例诊断的视觉判断并未提供统计检验，斜率轻微偏离 0 的可能性未量化。

### 开放问题与未来方向

基于上述局限和理论框架，若干结构性问题指向未来的探索：

1. **如何打破 $d/\log n$ 瓶颈？** 设计能够主动感知并跨瓶颈传播信息的架构、图预训练目标或拓扑感知的采样策略，以提升有效样本量，是下一步的关键。  
2. **注意力与高阶模型的极小极大界限**：含标准注意力的 GNN、图变换器等是否也服从类似的结构下界，还是能够突破 $\Omega(d/\log n)$？  
3. **相变现象**：当 $\lambda_2$ 逐步降低、图从扩张型变为瓶颈型时，极小极大风险是否会呈现从 $1/\sqrt{n}$ 到 $d/\log n$ 的相变？该过渡的结构度量是什么？  
4. **超越 homophily 与无向图**：对于异配图、有向图，应如何定义等效的结构量（如边同质性、有向谱间隙）来刻画有效样本量？比率诊断在这些设定下是否仍适用？  
5. **从回归到分类**：将信息论下界推广至交叉熵损失和分类校准误差，量化图结构在分类问题中的影响，将极大扩展该理论的实际指导意义。  

综上，该工作不仅提供了首个针对 GNN 的非渐近极小极大下界，更揭示了 **图拓扑作为“数据结构”本身的泛化约束**，为未来数据驱动和结构驱动的图学习研究划定了清晰的理论路线图和适用边界。



## 原文 PDF

![[paperPDFs/ICLR_2026/Minimax_Sample_Complexity_of_Graph_Neural_Networks_Lower_Bounds_and_Structural_Effects.pdf]]
