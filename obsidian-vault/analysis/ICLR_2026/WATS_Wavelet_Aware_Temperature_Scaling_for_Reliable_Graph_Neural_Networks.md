---
title: "WATS: Wavelet-Aware Temperature Scaling for Reliable Graph Neural Networks"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/WATS_Wavelet_Aware_Temperature_Scaling_for_Reliable_Graph_Neural_Networks.pdf
project_link: null
code_link: https://github.com/lxy1134/WATS.git
openreview_forum_id: ZrrVEMyQeU
aliases:
- WWATS
- WATS
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/graph_neural_networks
core_operator: "使用热核图小波特征作为节点特定的结构签名，通过可调尺度参数 s 和 Chebyshev 阶数 k 捕获多尺度局部和全局几何信息，驱动节点级温度缩放。"
primary_logic: "图小波能够高效、可扩缩地提取结构信息，不依赖邻居预测或标签，因此可以作为节点校准不确定性的稳定结构代理，实现自适应、架构无关的后处理校准。"
claims:
- "WATS 在绝大多数评测配置中取得最低的 ECE，最高比经典和图特定基线降低 41.2% 的 ECE，校准方差平均降低 15.84%。"
- "图小波特征在多个数据集中始终优于其他结构特征（对数度、介数中心性、聚类系数），提供了最有效的校准输入。"
- "WATS 对同配性高的图表现出低超参数敏感性，Chebyshev 阶数 k 和扩散尺度 s 的变化仅引起微小的 ECE 波动。"
- "9 个数据集 (Citeseer, Cora, Pubmed, Cora-Full, Computers, Photo, Reddit, Roman, Tol... 上 ECE = 在绝大多数配置中取得最低 ECE"
---

# WATS: Wavelet-Aware Temperature Scaling for Reliable Graph Neural Networks

> [!tip] 核心洞察
> 图小波能够高效、可扩缩地提取结构信息，不依赖邻居预测或标签，因此可以作为节点校准不确定性的稳定结构代理，实现自适应、架构无关的后处理校准。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | WATS：基于小波的温度缩放用于图神经网络的可靠校准 |
| 英文题名 | WATS: Wavelet-Aware Temperature Scaling for Reliable Graph Neural Networks |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ZrrVEMyQeU) · [GitHub](https://github.com/lxy1134/WATS.git) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/graph_neural_networks |
| Method | WATS (Wavelet-Aware Temperature Scaling) |
| Dataset | 9 个数据集 (Citeseer, Cora, Pubmed, Cora-Full, Computers, Photo, Reddit, Roman, Tolokers) 搭配 3 种 GNN 主干 (GCN, GAT, GCNII), Photo (GCN) |

> [!tip] 效果简介
> - 9 个数据集 (Citeseer, Cora, Pubmed, Cora-Full, Computers, Photo, Reddit, Roman, Tol... 上，ECE 为 在绝大多数配置中取得最低 ECE，对比 TS, ETS, CaGCN, GATS, GETS，变化 ECE 最多降低 41.2%，校准方差平均降低 15.84%。
> - Photo (GCN) 上，ECE 为 1.64 ± 0.31，对比 Uncalibrated GCN，变化 显著降低校准误差。

## 概要

图神经网络（GNN）在节点分类任务中普遍存在校准不可靠的问题：模型预测的置信度往往与真实准确率偏离，尤其在网络加深时，准确率下降而置信度反而上升（Figure 1）。现有图校准方法主要依赖一跳邻居统计或潜在嵌入来预测节点温度，忽略了图拓扑的细粒度结构异质性，导致在低度、稀疏或低同配性区域校准偏差大，无法捕捉多跳结构驱动的系统性误校准。

针对这一瓶颈，本文提出 **WATS（Wavelet-Aware Temperature Scaling）**，一种架构无关的后处理校准框架。其核心思路是：使用热核图小波特征作为节点特定的结构签名，通过可调尺度参数 $s$ 和 Chebyshev 阶数 $k$ 捕获多尺度局部和全局几何信息，驱动一个轻量 MLP 为每个节点预测独立的温度参数 $\tau_i$，从而对原始 GNN 输出的 logits 进行节点级缩放。图小波能够高效、可扩缩地提取结构信息，不依赖邻居预测或标签，因此可以作为节点校准不确定性的稳定结构代理。

在 9 个数据集、3 种 GNN 主干（GCN、GAT、GCNII）上的实验表明，WATS 在绝大多数配置中取得最低的期望校准误差（ECE），最高比经典和图特定基线降低 **41.2%** 的 ECE，校准方差平均降低 **15.84%**。消融研究证实，图小波特征始终优于对数度、介数中心性、聚类系数等替代结构特征；在高度同配图上，WATS 对超参数 $k$ 和 $s$ 不敏感，推荐默认设置为 $k=3$、$s=2.0$。WATS 不修改预训练 GNN 参数，仅需静态小波特征和两层 MLP 即可完成校准训练，兼具有效性与轻量性。



图神经网络（GNN）通过消息传递机制聚合邻居信息，在节点分类等任务中取得了显著成功。然而，GNN 的预测置信度往往与其实际正确率之间存在系统性偏差，即模型校准（calibration）问题。Figure 1 揭示了这一现象的典型表现：在 Cora、Pubmed 和 Citeseer 三个数据集上，随着 GCN 层数加深，模型的测试准确率持续下降，但平均预测置信度反而上升。这种深度诱导的误校准（depth-induced miscalibration）意味着深层 GNN 在变得更“自信”的同时，其预测质量却在恶化，严重损害了模型在实际高风险场景中的可靠性。

校准问题的核心在于模型输出的概率估计是否真实反映了其正确性。通常以期望校准误差（ECE）来量化这一偏差：

$$\mathrm{ECE} = \sum_{m=1}^{M} \frac{|B_m|}{|\mathcal{N}|} \left| \mathrm{Acc}(B_m) - \mathrm{Conf}(B_m) \right|$$

该指标将预测按置信度分箱，衡量每个箱内平均置信度与平均准确率之间的差距。ECE 越低，校准越好。

### 现有方法的局限

为缓解 GNN 的校准问题，研究者提出了一系列后处理温度缩放（temperature scaling）方法。经典方法 TS（Temperature Scaling）为所有节点学习一个全局温度参数，简单但忽略了图结构的异质性。随后的图特定方法尝试引入结构信息：CaGCN 利用图卷积网络从节点特征预测温度；GATS 通过注意力机制聚合一跳邻居的温度；GETS 则基于度嵌入的混合专家模型进行温度预测。

然而，这些方法存在一个共同的瓶颈：**它们主要依赖一跳邻居统计或潜在嵌入，无法捕捉图拓扑中细粒度的多跳结构异质性**。具体而言，现有方法隐含地假设一跳邻居的标签分布能够充分反映节点的校准不确定性。但这一假设在低度节点、稀疏区域或低同配性（heterophily）图中往往不成立。考虑一个消息传递聚合器：

$$h_i^{(\ell+1)} = \frac{1}{d_i+1} \left( h_i^{(\ell)} + \sum_{j \in \mathcal{N}(i)} h_j^{(\ell)} \right)$$

节点的校准偏置可近似为：

$$\mathrm{bias}_i = \left| \hat{c}_i - \mathbf{1}(\hat{y}_i = y_i) \right| \approx \left| y_i - \frac{1}{d_i+1} \sum_{j \in \mathcal{N}(i)} y_j \right|$$

这一近似表明，当节点的标签与其局部邻域存在显著差异时（例如异配图中的边界节点），仅靠一跳统计无法提供准确的校准信号。更关键的是，GNN 的多层消息传递使得节点的预测实际上受多跳邻居影响，而一跳方法完全忽略了这种长程结构驱动的系统性误校准。

### 本文动机

上述分析揭示了现有图校准方法的核心缺口：**缺乏一个能够高效捕获多尺度结构信息的通用代理，用于指导节点级的自适应校准**。理想的解决方案应当满足三个条件：（1）能够提取从局部到全局的多跳结构特征；（2）不依赖邻居的预测标签或 logits，避免误差传播；（3）计算高效，可扩展到大规模图。

图小波变换（graph wavelet transform）天然满足这些要求。通过热核函数定义的可调尺度小波算子：

$$\pmb{\Psi}_{s} = \mathbf{U} \mathrm{diag}(g(s\lambda_1), \dots, g(s\lambda_N)) \mathbf{U}^{\top}$$

图小波能够在频谱域中实现局部化和稀疏性，通过调节扩散尺度参数 $s$ 控制感受野大小，从而捕获从紧邻到全局的多尺度结构签名。这为构建结构感知的节点级温度缩放提供了理论基础。

基于此，本文提出 **WATS（Wavelet-Aware Temperature Scaling）**，一个轻量级的后处理校准框架。WATS 的核心思想是：将图小波系数作为节点不确定性的结构签名，驱动一个简单的 MLP 为每个节点预测特定的温度参数，从而在不修改预训练 GNN 参数、不访问邻居预测的前提下，实现细粒度的自适应校准。



## 核心方法与创新机理

现有图校准方法（CaGCN、GATS、GETS）的核心瓶颈在于，它们依赖一跳邻居统计或潜在嵌入来预测节点温度，忽略了图拓扑的细粒度结构异质性。这导致在低度节点、稀疏区域或低同配性图上出现系统性误校准——深层 GCN 在准确率下降的同时置信度反而上升（Figure 1），而一跳邻居的标签统计无法提供准确的节点不确定性估计（式 (3) 的偏置近似暴露了这一局限）。

WATS 的关键创新在于引入**可调的热核图小波特征**作为节点特定的结构签名，驱动节点级温度缩放。与 baseline 的 changed slot 对比如下：

| 温度参数生成的输入特征 | Baseline（TS/ETS/CaGCN/GATS/GETS） | WATS |
|---|---|---|
| 信息源 | 全局固定标量，或基于一跳邻居统计/潜在嵌入预测的温度 | 基于可调热核图小波特征预测的节点特定温度 |
| 是否需要邻居 logits/标签 | CaGCN、GATS 需要邻居 logits 或预测 | **不需要**，仅使用静态结构信号 |

这一 changed slot 带来三个因果性优势：

1. **结构代理的独立性**：小波特征通过 Chebyshev 多项式逼近（式 (5)）高效提取多尺度局部和全局几何信息，不依赖邻居预测或标签，因此校准过程与 GNN 架构解耦，可作为通用的后处理模块。

2. **多尺度结构捕获**：通过可调扩散尺度 $s$ 和 Chebyshev 阶数 $k$，小波算子 $\pmb{\Psi}_{s}$（式 (4)）能够在不同尺度上编码节点的结构角色。对数度作为基信号经小波变换后，生成归一化特征矩阵 $\mathbf{H}_i$（式 (6)），再由两层 MLP 经 Softplus 映射为节点温度 $\tau_i$（式 (7)）。这种设计使 WATS 能捕捉多跳结构驱动的校准偏差，而非仅依赖一跳邻居。

3. **自适应校准能力**：在 Citeseer 的可靠性图（Figure 2）中，WATS 显著修正了低度节点的欠置信问题，使校准曲线更贴近对角线。消融实验（Table 3）证实，图小波特征在绝大多数数据集上持续优于对数度、介数中心性和聚类系数等替代结构特征，验证了小波签名作为校准不确定性代理的有效性。

总体而言，WATS 将图校准从“依赖邻居预测”的范式转变为“利用多尺度结构签名”的范式，实现了架构无关、仅需静态图结构的后处理校准。



WATS 是一种后处理（post-hoc）校准框架，专为图神经网络节点分类任务设计。其核心思想是利用热核图小波特征作为节点特定的结构签名，预测节点级温度参数，从而对预训练 GNN 输出的 logits 进行自适应缩放。整个 pipeline 由两个顺序模块构成，不修改预训练 GNN 的任何参数，也不依赖邻居的预测或标签信息。

### Pipeline 总览

WATS 的工作流程可概括为以下步骤：

1. **预训练 GNN 前向传播**：使用已训练好的 GNN 主干（如 GCN、GAT、GCNII）对输入图进行推理，得到每个节点的原始 logits 向量 $z_i$。此步骤与 WATS 解耦，WATS 仅使用冻结的 logits 输出。

2. **图小波特征提取**：以节点的对数度作为基信号，通过 Chebyshev 多项式逼近计算热核图小波变换，生成多尺度结构特征矩阵 $\mathbf{H}$。该模块利用可调参数——扩散尺度 $s$ 和 Chebyshev 阶数 $k$——控制局部与全局结构信息的捕获范围。

3. **节点温度预测**：将每个节点的归一化小波特征 $\mathbf{H}_i$ 输入一个两层 MLP，经 Softplus 激活函数输出正值温度 $\tau_i$。

4. **温度缩放校准**：使用预测的节点特定温度对原始 logits 进行缩放，得到校准后的 logits $\hat{z}_i = z_i / \tau_i$，再经 softmax 获得校准后的预测概率。

### 模块关系与数据流

两个核心模块之间的依赖关系清晰：小波特征提取模块为温度预测模块提供结构嵌入，而温度预测模块的输出直接作用于原始 logits。数据流如下：

```
原始图结构 + 对数度信号
        ↓
[图小波特征提取] → 多尺度特征矩阵 S → ℓ₁ 归一化 → H
        ↓
[温度预测 MLP] → τᵢ = Softplus(MLP(Hᵢ))
        ↓
原始 logits zᵢ → zᵢ / τᵢ → 校准后概率
```

### 关键设计决策

**为何选择图小波特征**：现有图校准方法（如 CaGCN、GATS）主要依赖一跳邻居统计或潜在嵌入来预测温度，忽略了图拓扑的细粒度结构异质性。在低度节点、稀疏区域或低同配性子图中，一跳信息不足以捕捉多跳结构驱动的系统性误校准。图小波变换通过热核函数在谱域引入局部化特性，能够在不同尺度 $s$ 下提取节点的多跳结构上下文，作为校准不确定性的稳定结构代理。

**为何使用对数度作为基信号**：消融实验（Table 2）表明，对数度在多数数据集上达到最优或并列最优的 ECE，优于原始度或单位矩阵。这与理论分析一致——节点的校准偏置与其局部邻域的标签同质性密切相关，而对数度能有效编码节点的局部结构信息。

**温度预测的简洁性**：温度预测仅使用一个两层 MLP 加 Softplus 激活，无需复杂的图神经网络或注意力机制。这种设计使得 WATS 的校准训练极为轻量——小波特征可预计算并作为静态输入复用，校准阶段仅需优化 MLP 参数。

### 与基线方法的本质区别

| 方法 | 温度粒度 | 输入信号 | 是否依赖邻居预测/标签 |
|------|---------|---------|---------------------|
| TS | 全局单标量 | 无（可学习参数） | 否 |
| CaGCN | 节点级 | GCN 对 logits 的图卷积 | 是（邻居 logits） |
| GATS | 节点级 | 注意力聚合的一跳邻居温度 | 是（邻居温度预测） |
| GETS | 节点级 | 度嵌入 + 混合专家 | 否 |
| **WATS** | **节点级** | **多尺度图小波特征** | **否** |

WATS 的关键优势在于：既不依赖邻居的预测或标签（避免误差传播），又能通过可调尺度的小波特征捕获多跳结构信息，从而在结构异质性强的区域实现更精准的校准。这种架构无关的设计使其可无缝适配任意预训练 GNN 主干，无需重新训练或修改原始模型。



### 3.1 图校准问题与期望校准误差

节点分类任务中，校准衡量模型预测置信度与真实正确率的一致性。期望校准误差（ECE）是标准度量，其分箱近似定义为：

$$\mathrm{ECE} = \sum_{m=1}^{M} \frac{|B_m|}{|\mathcal{N}|} \left| \mathrm{Acc}(B_m) - \mathrm{Conf}(B_m) \right|$$

其中 $B_m$ 为第 $m$ 个置信度分箱，$\mathcal{N}$ 为节点集合，$\mathrm{Acc}(B_m)$ 和 $\mathrm{Conf}(B_m)$ 分别表示该分箱内的平均准确率与平均置信度。ECE 越低，校准越好。

### 3.2 图结构驱动的误校准根源

现有校准方法（CaGCN、GATS 等）依赖一跳邻居统计或潜在嵌入预测节点温度，忽略了图拓扑的细粒度结构异质性。论文通过分析 GNN 消息传递机制揭示了这一瓶颈：对于采用度数归一化均值聚合的 GNN 层，

$$h_i^{(\ell+1)} = \frac{1}{d_i+1} \left( h_i^{(\ell)} + \sum_{j \in \mathcal{N}(i)} h_j^{(\ell)} \right)$$

每个节点的校准偏置可近似为：

$$\mathrm{bias}_i = \left| \hat{c}_i - \mathbf{1}(\hat{y}_i = y_i) \right| \approx \left| y_i - \frac{1}{d_i+1} \sum_{j \in \mathcal{N}(i)} y_j \right|$$

该近似表明，节点校准误差与其一跳邻居标签的同质性密切相关。然而，一跳统计无法捕捉多跳结构驱动的系统性误校准，尤其在低度、稀疏或低同配性区域，导致现有方法校准偏差大、方差高。

### 3.3 WATS：基于图小波的结构感知温度缩放

WATS 的核心思路是用热核图小波特征作为节点特定的结构签名，通过可调尺度参数捕获多尺度局部和全局几何信息，驱动节点级温度缩放。方法包含两个关键模块。

**模块一：图小波特征提取。** 为克服图傅里叶变换缺乏局部性和稀疏性的局限，WATS 采用热核图小波变换。小波算子定义为：

$$\pmb{\Psi}_{s} = \mathbf{U} \mathrm{diag}(g(s\lambda_1), \dots, g(s\lambda_N)) \mathbf{U}^{\top}$$

其中 $\mathbf{U}$ 为图拉普拉斯矩阵的特征向量矩阵，$\lambda_i$ 为特征值，$g(s\lambda) = e^{-s\lambda}$ 为热核缩放函数，$s$ 为可调扩散尺度。为避免显式特征分解的高昂开销，WATS 使用 Chebyshev 多项式逼近计算小波变换后的特征矩阵：

$$\mathbf{S} = \frac{1}{2} c_0 \mathbf{T}_0 + \sum_{k=1}^{K} c_k \mathbf{T}_k$$

其中 $K$ 为 Chebyshev 阶数，$\mathbf{T}_k$ 为递推多项式项，$c_k$ 为对应系数。该逼近将计算复杂度控制在 $\mathcal{O}(K|\mathcal{E}|)$，仅与边数线性相关。输入信号采用节点的对数度，经消融验证在多数数据集上优于原始度或单位矩阵（Table 2）。最后对每个节点 $i$ 进行行方向 $\ell_1$ 归一化：

$$\mathbf{H}_i = \frac{\mathbf{S}_i}{\lVert \mathbf{S}_i \rVert_1}$$

得到归一化的小波特征矩阵 $\mathbf{H}$，作为节点结构嵌入。

**模块二：温度预测 MLP。** WATS 使用一个两层 MLP 将每个节点的小波特征映射为节点特定的温度参数：

$$\tau_i = \mathrm{Softplus}(\mathbf{MLP}(\mathbf{H}_i))$$

Softplus 激活函数保证温度 $\tau_i > 0$。该温度用于缩放预训练 GNN 的原始 logits，实现后处理校准。整个过程不修改 GNN 参数，不依赖邻居预测或标签，仅使用静态小波特征。

**总时间复杂度**为 $\mathcal{O}(K|\mathcal{E}| + |\mathcal{V}|K h)$，其中 $|\mathcal{V}|$ 为节点数，$h$ 为隐藏维度。小波特征可预计算并复用，进一步降低校准阶段开销。



## 实验与关键发现

### 瓶颈与动机验证

现有图校准方法（CaGCN、GATS、GETS）依赖一跳邻居统计或潜在嵌入预测节点温度，忽略了图拓扑的细粒度结构异质性。这种设计在低度节点、稀疏区域或低同配性图上产生系统性校准偏差，因为一跳信息无法捕捉多跳结构驱动的误校准模式。WATS 的核心假设是：图小波特征可以作为节点校准不确定性的稳定结构代理，不依赖邻居预测或标签，实现自适应后处理校准。

Figure 1 提供了直接的动机证据：在 Cora、Pubmed、Citeseer 三个数据集上，随着 GCN 层数加深，模型准确率持续下降，而平均预测置信度反而上升。这种“深度诱导的误校准”表明，GNN 的置信度估计与真实正确率之间存在结构性背离，仅靠全局温度缩放（TS）或一跳邻居信息无法有效纠正。

![[assets/figures/papers/iclr26_0009_ZrrVEMyQeU_WATS_Wavelet-Aware_Temperature_Scaling_for_Relia/figures/003_Figure_1.jpg]]
*Figure 1: Test accuracy (ACC) and average predictive confidence of GCNs with increasing depth on Cora, Pubmed, and Citeseer. In all three datasets, deeper models exhibit decreasing accuracy while confidence increases, indicating depth-induced miscalibration*

### 主实验结果

Table 1 汇总了 WATS 与五种基线方法（TS、ETS、CaGCN、GATS、GETS）在 9 个数据集、3 种 GNN 主干（GCN、GAT、GCNII）上的 ECE 对比（均值 ± 标准差，10 次运行）。关键发现如下：

![[assets/figures/papers/iclr26_0009_ZrrVEMyQeU_WATS_Wavelet-Aware_Temperature_Scaling_for_Relia/figures/004_Table_1.jpg]]
*Table 1: Each result is reported as the mean ± standard deviation over 10 runs. ‘Uncalib’ refers to uncalibrated outputs, and ‘oom’ indicates out-of-memory failures where the method could not complete. Best performance on ECE are highlighted for each configuration*

- **WATS 在绝大多数配置中取得最低 ECE**。在 27 个（数据集 × 模型）配置中，WATS 的 ECE 最优或并列最优的比例显著高于所有基线方法。
- **ECE 最大降幅达 41.2%**（与经典和图特定基线相比），校准方差平均降低 15.84%（与图特定方法相比）。
- **即使基础模型本身校准较好，WATS 仍能进一步降低误差**。例如，Photo 数据集上 GCN 的未校准 ECE 已经较低，WATS 将其降至 1.64±0.31；Computers 上 GCN 降至 1.20±0.19。
- **GATS 在 Reddit 等大图上遭遇内存溢出（OOM）**，而 WATS 在所有数据集上均能正常完成校准。

Figure 2 以 Citeseer 为例展示了校准效果的两个维度：(a) 可靠性图显示，校准后的曲线更贴近对角线（完美校准线），说明预测置信度与真实准确率的一致性显著改善；(b) 按度数分箱的分析表明，低度节点的欠自信现象得到有效纠正，校准后的准确率曲线与置信度曲线趋于重合。

![[assets/figures/papers/iclr26_0009_ZrrVEMyQeU_WATS_Wavelet-Aware_Temperature_Scaling_for_Relia/figures/006_Figure_2.jpg]]
*Figure 2: “Uncali” refers to the uncalibrated result and “Cali” refers to the calibrated result. (a) shows the reliability diagram comparing calibrated and uncalibrated outputs. The diagonal dashed line indicates perfect calibration (b) presents a degree-binned analysis of accuracy and confidence. Solid and dashed lines represent calibrated accuracy and confidence respectively*

### 消融实验

**基信号选择**（Table 2）：WATS 的小波特征提取以节点结构信号为输入。消融实验对比了对数度（log-degree）、原始度（raw degree）和单位矩阵（identity）三种基信号。结果表明，对数度在多数数据集上达到最优或并列最优的 ECE，优于原始度（可能因为度数分布长尾，对数变换压缩了动态范围）和单位矩阵（完全忽略结构信息）。这一发现验证了度数信息作为结构代理的有效性，同时说明对数变换是简单而关键的预处理步骤。

![[assets/figures/papers/iclr26_0009_ZrrVEMyQeU_WATS_Wavelet-Aware_Temperature_Scaling_for_Relia/figures/007_Table_2.jpg]]
*Table 2: ECE (↓) comparison between log-degree, raw degree, and an identity matrix as base signal. This comparison isolates the effect of the base structural signal used by the temperature regressor*

**结构特征对比**（Table 3）：将图小波特征与三种替代结构特征——对数度（Deg）、介数中心性（Cen）、聚类系数（Clus）——进行对比。图小波特征在 6/8 数据集上取得最低 ECE（Citeseer、Computers、Cora、Cora-full、Pubmed、Reddit），在 Photo 和 Roman 上与最优替代特征差距极小。介数中心性和聚类系数在部分数据集上表现尚可，但缺乏一致性和跨数据集的鲁棒性。这验证了核心论断：图小波的多尺度局部-全局几何信息捕获能力，使其成为更通用、更有效的校准输入特征。

![[assets/figures/papers/iclr26_0009_ZrrVEMyQeU_WATS_Wavelet-Aware_Temperature_Scaling_for_Relia/figures/008_Table_3.jpg]]
*Table 3: ECE (↓) comparison between graph wavelet and alternative structural features, where "Deg" denote log transformed degree, "Cen" denote betweenness centrality, "Clus" denote clustering coefficient, and ‘oom’ indicates out-of-memory failures where the method could not complete. Graph wavelet consistently outperforms other variants across most datasets*

**超参数敏感度**（Figure 3）：在高度同配图上（如 Cora、Citeseer、Pubmed），WATS 对 Chebyshev 阶数 k 和扩散尺度 s 表现出低敏感性——k 从 2 到 4、s 在合理范围内变化时，ECE 仅产生微小波动。论文推荐默认设置 k=3, s=2.0 作为新图的合理起点。需要注意的是，在异配性较高的图上（如 Roman、Tolokers），超参数敏感度可能上升，需要根据具体图结构调整。

![[assets/figures/papers/iclr26_0009_ZrrVEMyQeU_WATS_Wavelet-Aware_Temperature_Scaling_for_Relia/figures/012_Figure_3.jpg]]
*Figure 3: Sensitivity analysis of wavelet hyper-parameters. Each plot shows the ECE scores on different datasets with varying wavelet scale parameter s (x-axis) and polynomial order k. Each line represents a different Chebyshev order k: blue for k = 2, orange for k = 3 , 3, green for k = 4 and grey for previous SOTA*

### 计算效率与资源开销

WATS 的总时间复杂度为 $\mathcal{O}(k|\mathcal{E}| + |\mathcal{V}|kh)$，其中 k 为 Chebyshev 阶数，|E| 为边数，|V| 为节点数，h 为隐藏维度。小波特征可以预计算并作为静态输入复用，实际校准训练仅涉及两层 MLP 的参数优化。

Table 8（附录）的校准时间对比显示，WATS 的校准时间低于 GETS 和 GATS。例如在 Cora 上，WATS 校准耗时 1.01s，而 GETS 需 22.25s，GATS 需 2.12s。但小波特征提取本身在超大图上开销较大：Reddit 上特征提取耗时 42.66s，占总时间的主要部分。

Table 9（附录）的内存使用对比表明，WATS 的校准内存高于 TS 和 CaGCN（Cora 上 WATS 207.92 MB vs TS 94.65 MB），但低于 GATS。这是小波特征矩阵存储带来的固有开销，在资源受限环境下需要权衡。

### 失败模式与局限性

1. **后处理的天花板效应**：WATS 不修改预训练 GNN 参数，校准效果受限于原始 logits 的质量。当基础模型产生极端错误预测（如高置信度错误分类）时，节点温度缩放可能不足以完全纠正。
2. **大规模图上的特征提取开销**：Reddit 上的小波特征提取耗时显著，虽可通过预计算缓解，但对超大规模图（百万节点级）的适用性需要进一步验证。
3. **异配图的超参数敏感度**：虽然默认 k=3, s=2.0 在多数数据集上有效，但在 Roman、Tolokers 等异配图上，最优 s 值可能偏离默认值，需要额外调参。
4. **任务范围限制**：当前方法仅针对节点分类任务设计，尚未扩展到边预测、动态图或图分类任务。



## 定位与知识库关联

### 与现有校准方法的因果差异

现有图校准方法的核心瓶颈在于**结构信息利用不足**：TS 使用全局单温度，完全忽略节点间的结构异质性；CaGCN 和 GATS 依赖一跳邻居的预测置信度或 logits 来预测节点温度，但一跳统计无法捕捉多跳结构驱动的系统性误校准（见分析锚点：Section 3.2 的偏置近似推导）；GETS 虽然引入了度嵌入作为结构信号，但仍局限于节点自身的度信息，缺乏对局部拓扑几何的细粒度刻画。

WATS 的关键突破在于**将温度预测的输入从“邻居预测驱动的信号”替换为“多尺度结构签名”**。具体而言，WATS 使用热核图小波特征作为节点特定的结构代理，通过可调尺度参数 $s$ 和 Chebyshev 阶数 $k$ 捕获多跳局部和全局几何信息，驱动节点级温度缩放。这一设计使得 WATS 具备三个差异化优势：

1. **架构无关的后处理**：WATS 不修改预训练 GNN 参数，不访问邻居 logits 或标签，仅使用静态小波特征和两层 MLP 进行温度预测，因此可适配任意 GNN 主干。
2. **结构驱动的校准逻辑**：小波系数天然编码了节点在图谱中的多尺度位置信息，能够反映低度节点、稀疏区域或低同配性区域中的不确定性模式，而这些正是传统方法校准偏差最大的区域。
3. **高效可扩缩**：通过 Chebyshev 多项式逼近避免显式特征分解，小波特征可预计算并复用，总时间复杂度为 $\mathcal{O}(k|\mathcal{E}| + |\mathcal{V}|kh)$。

### 适用边界与任务范围

WATS 当前的设计和验证聚焦于**节点分类任务**，其适用边界可归纳如下：

- **图类型**：在 9 个数据集上验证，涵盖引文网络（Cora、Citeseer、Pubmed、Cora-Full）、共购网络（Computers、Photo）、社交网络（Reddit）和异配图（Roman、Tolokers），覆盖了从高同配到低同配的谱系。在高度同配图上，WATS 表现出极低的超参数敏感性（Figure 3）。
- **GNN 主干**：已验证兼容 GCN、GAT、GCNII 三种主流架构，理论上可推广至任意产生 logits 的 GNN。
- **任务限制**：方法仅针对节点分类设计，**尚未扩展到边预测、动态图或图分类任务**。这是明确的适用边界，而非隐含假设。

### 已知局限

1. **校准上限受限于预训练 logits 质量**：作为后处理方法，WATS 不改变 GNN 参数，因此极端错误的预测无法通过温度缩放完全纠正。在极高置信或严重偏离校准的情形下，节点温度缩放可能不足以恢复完美校准。

2. **大规模图上的特征提取开销**：小波特征提取在超大图（如 Reddit）上耗时较高（约 42.7 秒），内存使用（约 4322 MB）高于 TS 和 CaGCN，但低于 GATS（Table 8 & Table 9）。对于超大规模图，特征预计算可能成为瓶颈。

3. **超参数需根据图结构调整**：虽然默认设置 $k=3, s=2.0$ 在多数数据集上广泛有效，但在某些异配图上可能仍需微调。扩散尺度 $s$ 控制小波的空间传播范围，Chebyshev 阶数 $k$ 影响逼近精度，二者共同决定了结构信息的捕获粒度。

4. **结构特征的信息完备性**：当前小波特征基于对数度作为基信号，虽然消融实验（Table 2）表明对数度优于原始度或单位矩阵，但基信号的选择是否充分捕捉了校准所需的结构信息，仍需进一步理论分析。

### 开放问题

1. **全局结构信息的整合**：当前小波特征主要捕捉节点的局部多跳邻域几何，尚未利用空间上远离但结构相似的节点信息。如何将全局结构上下文（如结构角色相似性）融入小波特征，以进一步提升校准精度，是一个有价值的方向。

2. **多任务图校准框架的扩展**：WATS 的节点特定温度缩放逻辑是否可推广至边预测、动态图或图分类任务？这需要重新定义“校准”在这些任务中的语义，并设计相应的结构代理信号。

3. **与训练时校准方法的协同**：WATS 作为后处理方法，与训练时校准技术（如标签平滑、正则化）的关系尚未探索。二者是否存在互补或冲突，值得进一步研究。



## 原文 PDF

![[paperPDFs/ICLR_2026/WATS_Wavelet_Aware_Temperature_Scaling_for_Reliable_Graph_Neural_Networks.pdf]]
