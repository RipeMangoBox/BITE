---
title: "Uncover Underlying Correspondence for Robust Multi-view Clustering"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Uncover_Underlying_Correspondence_for_Robust_Multi_view_Clustering.pdf
project_link: null
code_link: https://github.com/XLearning-SCU/2026-ICLR-CorreGen
openreview_forum_id: a4S1nQay3b
aliases:
- UUCRMVC
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "从判别式对比损失转变为生成式最大似然估计，通过EM算法推断软对应分布，并利用GMM引导的边缘概率自适应放大语义一致对、抑制噪声样本，从而从根本上缓解对预定义正负对的依赖。"
primary_logic: "将噪声对应下的多视图聚类建模为隐变量生成问题，最大化观测数据的边际对数似然，迭代估计潜在跨视图对应分布并优化嵌入空间，使模型能够自动发现类别级语义关联，显著提升鲁棒性。"
claims:
- "CorreGen在所有数据集和噪声设定下均取得最优聚类性能"
- "GMM引导的边缘估计与虚拟样本模块对噪声鲁棒性至关重要，移除后性能显著下降"
- "生成式目标在特定条件下退化为标准InfoNCE，证明其一般性"
- "后验分布可视化证实模型能够从噪声对应中逐步发现类别级语义结构"
---

# Uncover Underlying Correspondence for Robust Multi-view Clustering

> [!tip] 核心洞察
> 将噪声对应下的多视图聚类建模为隐变量生成问题，最大化观测数据的边际对数似然，迭代估计潜在跨视图对应分布并优化嵌入空间，使模型能够自动发现类别级语义关联，显著提升鲁棒性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 揭示底层对应以实现鲁棒多视图聚类 |
| 英文题名 | Uncover Underlying Correspondence for Robust Multi-view Clustering |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=a4S1nQay3b) · [GitHub](https://github.com/XLearning-SCU/2026-ICLR-CorreGen) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | CorreGen |
| Dataset | Scene15 (MR=0.2, CR=0.2), UMPC-Food101 (MR=0.2 |

> [!tip] 效果简介
> - Scene15 (MR=0.2, CR=0.2) 上，ACC 为 41.78 (CorreGen)，对比 38.36 (Vanilla InfoNCE)，变化 +3.42。
> - UMPC-Food101 (MR=0.2, CR=0.2) 上，ACC 为 45.97 (CorreGen)，对比 43.84 (Vanilla InfoNCE)，变化 +2.13。

## 概要

多视图聚类（MVC）通过挖掘不同视图间的互补信息实现无监督语义发现，其核心前提是跨视图实例级一一对应。然而，真实多视图数据中普遍存在**噪声对应**问题，表现为两类破坏：**类别级不匹配**（同类样本被误判为负对）和**样本级不匹配**（错配对与不可对齐样本）。现有方法主要沿两条路径处理该问题——对噪声对进行重加权或对实例对进行重对齐——但二者均未从根本上摆脱对预定义正负对指标的依赖，难以在严重噪声下区分真实语义关系与随机关联。

本文提出 **CorreGen**，一种**生成式框架**，将噪声对应下的多视图聚类建模为对潜在跨视图对应的最大似然估计问题。核心思路是：不再通过判别式对比损失（如InfoNCE）强制拉近预设正对、推远预设负对，而是直接最大化观测数据的边际对数似然，将跨视图关联视为隐变量，通过**期望最大化（EM）算法**迭代推断软对应分布并优化嵌入空间。理论分析表明，标准InfoNCE是该生成式目标在特定退化条件下的特例，验证了框架的一般性。

在方法定位上，CorreGen属于**对应生成范式**，区别于重加权和重对齐两类主流方案。其E-step利用GMM引导的边缘概率估计为可信样本赋予更高权重，同时引入虚拟样本机制吸收不可对齐样本，通过熵正则化最优传输求解多对多软分配；M-step则以E-step得到的后验分布为权重，最大化加权对数似然以更新编码器参数。

实验结果表明，CorreGen在多个数据集和噪声设定下均取得最优聚类性能，在极具挑战的UMPC-Food101数据集上准确率提升约10%。消融实验证实，GMM引导的边缘估计与虚拟样本模块对噪声鲁棒性至关重要。后验分布可视化进一步揭示，模型能够从初始噪声对应中逐步发现类别级语义结构，验证了生成式建模在噪声对应学习中的有效性。



多视图聚类旨在利用来自不同来源或模态的互补信息，将样本划分到语义一致的组别中。近年来，对比学习凭借其强大的表示学习能力，已成为该领域的主导范式。其核心思想依赖于一个基本假设：跨视图的实例级对应关系是精确已知的——即第 $i$ 个样本在视图 $v_1$ 中的表示应当与视图 $v_2$ 中的第 $i$ 个样本形成正对，而与其他所有样本形成负对。

然而，这一假设在实际多视图数据中往往难以成立。真实场景下的跨视图对应关系普遍存在噪声，具体表现为两个层面：

- **类别级不匹配**：由于数据集固有的类别不平衡，随机采样形成的负对中大量样本实际属于同一类别。以本文使用的四个基准数据集为例，其类别级不匹配比率均超过 98%（Scene15: 99.65%，Caltech101: 98.25%，LandUse21: 99.00%，UMPC-Food101: 99.53%），这意味着标准对比学习中绝大多数负对实际上是“假阴性”，模型被迫将语义相似的样本推开，严重破坏聚类所需的类内紧凑性。
- **样本级不匹配**：包括跨视图的错配对与不可对齐样本。例如，在图像-文本多视图场景中，某张图片可能与错误的文本描述配对，或某些样本在另一视图中根本没有对应物。

上述噪声对应的存在，使得传统对比学习框架面临根本性困境：其判别式目标（InfoNCE）依赖于硬性的正/负对指标 $t_{ij} \in \{0, 1\}$，一旦这些预定义关系不可靠，模型便无法区分真实的语义关系与噪声，学习到的表示空间将严重偏离聚类目标。

现有处理噪声对应的工作主要沿两条路径展开：**成对重加权**方法试图为每个样本对分配置信度权重，但其本质上仍受限于实例级一对一的对应假设；**成对重对齐**方法通过学习跨视图匹配来修正对应关系，但通常需要额外的匹配网络且难以捕捉类别级的语义关联。这两类范式均未从根本上摆脱对预定义正负对指标的依赖，在处理高噪声场景时性能退化显著。

本文的核心动机在于：**将噪声对应下的多视图聚类从判别式范式转变为生成式范式**。具体而言，我们提出 **CorreGen**，将跨视图对应关系建模为隐变量，通过最大化观测数据的边际对数似然来学习鲁棒表示。该方法无需预设任何正负对，而是通过期望最大化算法迭代推断潜在的软对应分布，使模型能够自动发现类别级语义关联，同时自适应地抑制样本级噪声。这一生成式框架不仅具有理论上的优雅性——标准 InfoNCE 可被证明为其在特定假设下的特例——更在多个噪声设定下取得了显著优于现有方法的聚类性能。



## 核心方法与创新机理

CorreGen的核心创新在于**从判别式对比学习到生成式最大似然估计的范式转换**，将噪声对应下的多视图聚类建模为隐变量生成问题。这一转换带来了三个关键的技术变革：

### 1. 学习目标：从硬性正负对到生成式边际似然

传统对比学习方法（如InfoNCE）依赖显式的正负对指标 $t_{ij}$，将跨视图对应定义为实例级一对一匹配：

$$\mathcal{P}_{v_1,v_2}^{+} = \bigcup_{i=1}^{N} \{ \{ \mathbf{x}_i^{(v_1)}, \mathbf{x}_i^{(v_2)}, t_{ii}^{12}=1 \} \}$$

这种硬性二元关系在噪声对应下会严重误导模型——同类样本被误作负对、错配对与不可对齐样本直接干扰对比学习。CorreGen将目标转化为最大化观测数据的边际对数似然：

$$\theta^{*} = \underset{\theta}{\arg\max} \sum_{i=1}^{N} \log \sum_{j=1}^{N} p(\mathbf{x}_i^{(v_1)}, \mathbf{x}_j^{(v_2)}; \theta)$$

跨视图对应被隐式地作为隐变量处理，模型通过EM算法迭代推断软对应分布并优化嵌入空间，从根本上消除了对预定义正负对的依赖。**Proposition 2** 进一步证明，当边际分布均匀且后验退化为仅保留实例对时，CorreGen的目标退化为标准InfoNCE，揭示了生成式框架的一般性。

### 2. 跨视图对应建模：从硬性一对一匹配到自适应多对多软分配

在E-step中，CorreGen将后验分布的估计转化为最优传输问题，在边际约束下最大化期望语义相似度：

$$P^{*} = \underset{P \in \Pi(p^{(v_1)}, p^{(v_2)})}{\arg\max} \sum_{i,j} P_{ij} s(z_i^{(v_1)}, z_j^{(v_2)})$$

通过熵正则化的Sinkhorn算法高效求解，得到增广联合分布：

$$\tilde{P}^{*} = \text{Diag}(\mathbf{u}) \exp(\tilde{\mathbf{S}} / \lambda) \text{Diag}(\mathbf{v})$$

后验分布 $Q_{ij} = P_{ij}^{*} / p_i^{(v_1)}$ 实现了自适应软分配，能够自然地捕捉类别级语义关联，而非局限于实例级一对一匹配。Figure 3 的可视化证实，随着训练推进，后验分布从初始的噪声状态逐步演化至接近真实类别结构，表明模型能够从噪声对应中自动发现底层语义关系。

### 3. 噪声样本处理：GMM引导的边缘估计与虚拟样本机制

CorreGen引入两个互补机制应对不同层次的噪声：

- **GMM引导的边缘概率**：在嵌入空间拟合高斯混合模型，利用聚类置信度估计每个样本的边际概率 $p(\mathbf{x}_i^{(v)})$，为可信样本赋予更高权重，从而在最优传输的边际约束中自适应放大语义一致对、抑制噪声样本。消融实验（Table 3）表明，移除该模块后Scene15在MR=0.2, CR=0.2下的ACC从41.78降至40.98。

- **虚拟样本模块**：引入虚拟概率质量 $\rho$ 吸收不可对齐样本，将部分传输质量分配给虚拟节点，防止噪声样本强制参与匹配破坏整体分布。该模块在较高噪声下尤为关键，消融实验证实移除后性能显著退化。

这两个机制协同工作，使CorreGen能够同时应对类别级不匹配（同类样本被误作负对）和样本级不匹配（错配对与不可对齐样本），这是现有重加权和重对齐范式所无法实现的。



![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_a4S1nQay3b/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the CorreGen framework which operates via an EM procedure: the E-step infers the underlying correspondence distribution using GMM-guided marginals and a virtual sample mechanism to handle noise; the M-step subsequently utilizes these estimated soft correspondences to guide the robust representation learning*

CorreGen 将噪声对应下的多视图聚类重新建模为一个**生成式隐变量推断问题**，其核心是一个 EM 优化循环，交替估计跨视图软对应分布并最大化加权对数似然以更新嵌入空间。整体架构如图 2 所示，由以下模块串联构成。

**输入流**：给定 $V$ 个视图的 $N$ 个样本 $\{\mathbf{x}_i^{(v)}\}$，所有视图共享一个编码器 $f_\theta$，将原始数据映射到单位超球面上的嵌入 $\mathbf{z}_i^{(v)}=f_\theta(\mathbf{x}_i^{(v)})$。编码器骨干直接继承自 **DIVIDE**（Lu et al., 2024），保证与现有对比学习框架的兼容性。

**E-step：推断潜在对应分布**。该步骤的目标是估计跨视图的软后验 $Q_{ij}=P_{ij}^*/p_i^{(v_1)}$，而非依赖硬性正负对。具体由三个子模块协同完成：

1. **GMM 引导的边缘估计器**：在每个视图内拟合高斯混合模型，利用马氏距离和类别占比计算每个样本的边际概率 $p(\mathbf{x}_i^{(v)})$。高置信度样本（靠近聚类中心）获得更高边际权重，噪声样本则被自然压低。
2. **虚拟样本模块**：引入虚拟概率质量 $\rho$，将不可对齐或严重损坏的样本的部分质量分配给虚拟节点，防止其干扰正常样本的对应推断。
3. **最优传输对应求解器**：以 GMM 估计的边际分布为约束，以嵌入间余弦相似度矩阵 $\mathbf{S}$ 为收益，通过熵正则化 Sinkhorn 算法高效求解最优增广联合分布 $\tilde{P}^*$，进而得到软后验 $Q$。

**M-step：加权对数似然最大化**。利用 E-step 得到的后验 $Q_{ij}$ 作为权重，最大化生成式目标：
$$\theta^* = \arg\max_\theta \sum_{i,j} Q_{ij} \log p(\mathbf{x}_i^{(v_1)}, \mathbf{x}_j^{(v_2)}; \theta)$$
其中联合概率 $p(\mathbf{x}_i^{(v_1)}, \mathbf{x}_j^{(v_2)}; \theta)$ 由归一化的嵌入相似度参数化。这一步等价于用软对应替代硬正负对来更新编码器参数，语义一致的样本对获得更高更新权重。

**关键性质**：该框架具有一般性——当边际分布退化为均匀分布且后验仅保留实例级一对一匹配时，M-step 目标精确退化为标准 InfoNCE 对比损失（Proposition 2），表明 CorreGen 是判别式对比学习的严格泛化。



### 3.1 问题定义与生成式建模

标准对比多视图聚类将跨视图正负对定义为硬性二元关系，依赖实例级一对一匹配：

$$ \mathcal{P}_{v_1,v_2}^{+} = \bigcup_{i=1}^{N} \{ \{ \mathbf{x}_i^{(v_1)}, \mathbf{x}_i^{(v_2)}, t_{ii}^{12}=1 \} \}, \quad \mathcal{P}_{v_1,v_2}^{-} = \bigcup_{i=1}^{N} \bigcup_{j=1, j \neq i}^{N} \{ ( \mathbf{x}_i^{(v_1)}, \mathbf{x}_j^{(v_2)}, t_{ij}^{12}=0 ) \} $$

其中 $t_{ij}$ 为实例一对一指示。该范式在噪声对应（类别级不匹配、样本级错配与不可对齐样本）下，会将同类样本误判为负对，严重破坏跨视图一致性先验。

**CorreGen** 将噪声对应下的多视图聚类建模为隐变量生成问题，最大化观测数据的边际对数似然。以两视图情形为例，目标为：

$$ \theta^{*} = \underset{\theta}{\arg\max} \sum_{i=1}^{N} \log \sum_{j=1}^{N} p(\mathbf{x}_i^{(v_1)}, \mathbf{x}_j^{(v_2)}; \theta) $$

其中跨视图对应关系被视为隐变量，模型需在所有可能的跨样本配对中推断最优联合分布。该目标从根本上摆脱了对预定义正负对指标的依赖。

### 3.2 EM优化框架

CorreGen 通过期望最大化（EM）算法求解上述目标。引入辅助分布 $Q$，利用 Jensen 不等式导出变分下界，当 $Q$ 等于当前参数下的后验分布时下界紧致。

- **E-step**：估计潜在跨视图对应的后验分布 $p(\mathbf{x}_j^{(v_2)} ; \mathbf{x}_i^{(v_1)}, \theta^{(t)})$。
- **M-step**：利用 E-step 得到的后验 $Q$ 加权，最大化期望对数似然以更新编码器参数 $\theta$：

$$ \theta^{*} = \arg\max_{\theta} \sum_{i=1}^{N} \sum_{j=1}^{N} p(\mathbf{x}_j^{(v_2)} ; \mathbf{x}_i^{(v_1)}, \theta^{(t)}) \log p(\mathbf{x}_i^{(v_1)}, \mathbf{x}_j^{(v_2)}; \theta) $$

### 3.3 E-step：最优传输求解软对应分布

E-step 的核心是将后验估计转化为最优传输（Optimal Transport）问题。后验分解为联合分布与边际分布之比：

$$ p(\mathbf{x}_j^{(v_2)} ; \mathbf{x}_i^{(v_1)}, \theta^{(t)}) = \frac{p(\mathbf{x}_i^{(v_1)}, \mathbf{x}_j^{(v_2)}; \theta^{(t)})}{p(\mathbf{x}_i^{(v_1)}; \theta^{(t)})} $$

联合分布 $P^*$ 的估计被形式化为在边际约束下最大化期望语义相似度的最优传输问题：

$$ P^{*} = \underset{P \in \Pi(p^{(v_1)}, p^{(v_2)})}{\arg\max} \sum_{i,j} P_{ij} s(z_i^{(v_1)}, z_j^{(v_2)}), \quad \text{s.t. } P\mathbf{1}_N = p^{(v_1)}, P^{\top}\mathbf{1}_N = p^{(v_2)} $$

其中 $s(\cdot,\cdot)$ 为嵌入向量 $z_i^{(v)} = f_\theta(x_i^{(v)})$ 间的余弦相似度，$\Pi$ 为满足边际约束的联合分布集合。通过熵正则化与 Sinkhorn 缩放算法高效求解：

$$ \tilde{P}^{*} = \text{Diag}(\mathbf{u}) \exp(\tilde{\mathbf{S}} / \lambda) \text{Diag}(\mathbf{v}) $$

该过程输出自适应的多对多软分配矩阵，能够自动发现类别级语义关联，而非仅保留实例级一对一匹配。

### 3.4 GMM引导的边际估计与虚拟样本机制

边际概率 $p(\mathbf{x}_i^{(v)}; \theta)$ 通过拟合高斯混合模型（GMM）估计。每个样本的聚类置信度由其嵌入到各类中心马氏距离的指数衰减量 $d_i$ 刻画，结合类别占比得到：

$$ p(\mathbf{x}_i^{(v)}; \theta^{(t)}) = \frac{m^{d_i} - 1}{m - 1} \cdot \frac{N_c}{N}, \quad d_i = \exp(-\epsilon \sqrt{(z_i^{(v)} - \mu_c)^{\top} \Sigma_c^{-1} (z_i^{(v)} - \mu_c)}) $$

其中 $m$ 为曲线塑形参数，控制置信度映射的陡峭程度。该边际估计为语义一致、聚类置信度高的样本赋予更大权重，从而在 OT 求解中自适应放大可信配对、抑制噪声样本。

为处理不可对齐样本，E-step 引入虚拟样本机制：为每个视图增设一个虚拟节点，分配概率质量 $\rho$，将无法可靠匹配的样本质量吸收至虚拟节点。增广后的边际约束变为 $\tilde{p}^{(v)} = [(1-\rho)p^{(v)}, \rho]$，扩展相似度矩阵 $\tilde{\mathbf{S}}$ 在对应位置填入可学习的虚拟锚点值 $\mathbf{A}$。

### 3.5 M-step与InfoNCE的连接

M-step 中，联合分布由归一化相似度参数化：

$$ p(\mathbf{x}_i^{(v_1)}, \mathbf{x}_j^{(v_2)}; \theta) = \frac{\exp(s(z_i^{(v_1)}, z_j^{(v_2)})/\tau)}{\sum_{m=1}^N \sum_{n=1}^N \exp(s(z_m^{(v_1)}, z_n^{(v_2)})/\tau)} $$

代入 M-step 目标，以 E-step 得到的后验 $Q_{ij} = P_{ij}^* / p_i^{(v_1)}$ 为权重最大化加权对数似然，梯度反向传播更新共享编码器 $f_\theta$。

**命题2** 证明，当边际分布退化为均匀分布且后验仅保留实例对（即 $Q_{ii}=1$，$Q_{ij}=0, j \neq i$）时，CorreGen 的生成式目标严格退化为标准 InfoNCE：

$$ \theta^{*} = \underset{\theta}{\arg\max} \sum_{i=1}^{N} \log \frac{\exp(s(z_i^{(v_1)}, z_i^{(v_2)}) / \tau)}{\sum_{n=1}^{N} \exp(s(z_i^{(v_1)}, z_n^{(v_2)}) / \tau)} $$

这一理论退化表明 CorreGen 是 InfoNCE 的严格泛化——当数据完全清洁时等价于对比学习，当存在噪声对应时通过软后验和自适应边际自动调整学习信号。



## 实验与关键发现

### 实验设置

CorreGen 以 **DIVIDE**（Lu et al., 2024）作为骨干网络，在其对比学习框架上替换为生成式目标，所有基线方法均采用相同的特征提取架构以确保公平比较。评估在四个多视图数据集上进行：Scene15、Caltech101、LandUse21 和 UMPC-Food101，覆盖类别级和样本级噪声对应场景。实验采用两种噪声协议：（1）**不匹配率**（Mismatch Ratio, MR），随机打乱跨视图配对比例；（2）**损坏率**（Corruption Ratio, CR），以随机噪声替换视图内样本的比例。所有实验使用 5 个不同随机种子取均值，批次内采用 512 大小的重对齐策略。

### 主实验结果

**Table 1** 给出了不同 MR 下的聚类性能对比。CorreGen 在所有数据集和噪声设定下均取得最优或次优结果。以 Scene15 为例，在 MR=0%（清洁数据）下 ACC 达到 50.25，在极端 MR=80% 下仍保持 40.96，显著优于 **DIVIDE**、**SURE**、**GCFAgg** 等基线。在类别数更多、语义更复杂的 Caltech101 上，MR=0% 时 ACC 为 68.52，MR=80% 时仍保持 46.93，展现出生成式目标对类别级语义结构的鲁棒捕获能力。


![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_a4S1nQay3b/figures/007_Table_1.jpg]]
*Table 1: The clustering performance with different mismatch ratios (MR). The best results and second best results are marked in bold and underline. All the results are the mean of five individual runs with different random seeds*

**Table 2** 进一步考察 MR 与 CR 联合作用下的性能。当 CR 从 0.0 增至 0.8 时，多数对比方法性能急剧退化，而 CorreGen 的下降幅度显著更缓。例如在 UMPC-Food101 的 MR=0.2、CR=0.2 设定下，CorreGen 的 ACC 为 45.97，相较 Vanilla InfoNCE 的 43.84 提升 2.13 个百分点。**Figure 4** 的曲线对比更直观地展示了这一趋势：实线（MR=0.2）和虚线（MR=0.5）下，CorreGen 在 CR 增大时始终保持领先，验证了 GMM 引导边缘估计与虚拟样本机制对样本级噪声的抑制作用。


![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_a4S1nQay3b/figures/008_Table_2.jpg]]
*Table 2: The clustering performance on four multi-view datasets with different Mismatch Ratios (MR) and Corruption Ratios (CR)*

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_a4S1nQay3b/figures/012_Figure_4.jpg]]
*Figure 4: The clustering performance under varying CR value. Solid lines indicate results with $\begin{array} { r } { \mathbf { M \bar { R } } = 0 . 2 . } \end{array}$ , while dashed lines correspond to MR = 0.5. The CR values varies from 0.0 to 0.8

**Figure 3** 可视化了 Caltech101 上训练过程中后验分布 $Q_{ij}$ 的演化。预热阶段（10 epoch）类别结构几乎不可见；到 100 epoch 时，块状对角线结构已初步显现；200 epoch 时后验分布与真实类别标签高度一致。这直接证实了 CorreGen 能够从噪声对应中逐步发现类别级语义关联，而非仅依赖实例级一对一匹配。

### 消融实验

**Table 3** 报告了组件消融结果。移除 GMM 引导的边缘估计（w/o Guide）后，Scene15 在 MR=0.2、CR=0.2 设定下 ACC 从 41.78 降至 40.98，表明 GMM 引导的边际概率对区分可信样本与噪声样本至关重要。移除虚拟样本模块（w/o Virtual）在较高噪声下性能退化明显，而在清洁数据上影响较小，验证了其专门吸收不可对齐样本的设计意图。同时移除两者时，模型退化为标准 InfoNCE，性能进一步下降，证明两个组件存在协同效应。


![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_a4S1nQay3b/figures/019_Table_3.jpg]]
*Table 3: Ablation study of CorreGen on Scene15 and UMPC-Food101, where w/o denotes the component is not adopted. “Virtual” refers to the Virtual Sample module, “Guide” refers to the GMM-guided marginal estimation, and “Vanilla InfoNCE” denotes training with the standard contrastive objective*

### 超参数分析

**Figure 5** 和 **Figure 6** 展示了关键超参数的敏感性。虚拟样本噪声比率 $\rho$ 在 0.1–0.5 范围内性能稳定，超出此范围后因过度吸收或吸收不足导致性能下降；GMM 曲线形状参数 $m$ 在 2–4 之间表现最优。Sinkhorn 迭代次数在 20–50 次内已充分收敛，表明熵正则化最优传输求解效率较高。

### 收敛性分析

**Figure 7** 展示了 Scene15 上的训练收敛曲线。预热阶段（红色虚线前）损失快速下降，进入 EM 优化阶段后损失平稳收敛，ACC 持续上升并趋于稳定，表明 EM 交替优化过程具有良好的数值稳定性。

### 失败模式与局限

尽管 CorreGen 在各类噪声设定下表现优异，仍存在以下局限：

1. **聚类数依赖**：GMM 拟合和边际概率计算需要预先指定聚类数量 $C$，实际应用中 $C$ 可能未知，需借助额外的聚类数估计方法。
2. **噪声比率 $\rho$ 的先验设定**：$\rho$ 的最优值依赖真实噪声比例，当前需人工设定，在完全无先验知识场景下可能次优。
3. **初始嵌入质量敏感**：GMM 边际估计的质量依赖于初始嵌入空间的区分性，若预热阶段训练不充分，E-step 解的质量可能受影响，进而拖慢后续收敛。

### 数据集噪声特性

**Table 4** 统计了各数据集的类别级不匹配比率（CMR），揭示出真实多视图数据中固有的噪声对应程度。UMPC-Food101 的 CMR 显著高于其他数据集，解释了该数据集上基线方法普遍表现较差的原因，也凸显了 CorreGen 在该挑战性场景下 10% 准确率提升的实质意义。


![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_a4S1nQay3b/figures/021_Table_4.jpg]]
*Table 4: The Category-level Mismatch Ratio (CMR) for the datasets used in our experiments*



## 定位与知识库关联

### 1. 问题定位：噪声对应下的多视图聚类瓶颈

多视图聚类（Multi-view Clustering, MVC）的核心假设是跨视图数据间存在一致的语义对应关系。然而，实际数据中普遍存在**噪声对应**（Noisy Correspondence），具体表现为两类：**类别级不匹配**（同类样本被误作负对）和**样本级不匹配**（错配对与不可对齐样本）。这种噪声严重破坏了跨视图一致性先验，直接导致依赖固定正负对指标的判别式对比学习方法性能退化。

现有处理噪声对应的范式可分为两类（见 Figure 1）：
- **成对重加权**：通过估计样本对的可信度来调整损失权重，但本质上仍依赖预定义的实例级一对一匹配，无法发现跨实例的类别级语义关联。
- **成对重对齐**：尝试重新排列跨视图对应关系，但通常局限于硬性二元匹配，难以建模多对多的软性语义对应。

CorreGen 提出第三种范式——**对应生成**（Correspondence Generation），从根本上改变了学习目标：从判别式对比损失转向生成式最大似然估计，将跨视图对应建模为隐变量，通过 EM 算法迭代推断软对应分布并优化嵌入空间。

### 2. 方法谱系：与基线工作的关系

#### 2.1 作为骨干网络的继承

CorreGen 以 **DIVIDE**（Lu et al., 2024）作为基础特征提取骨干。DIVIDE 本身是一种鲁棒多视图聚类方法，CorreGen 在其之上替换了学习目标，将生成式框架无缝集成到现有对比学习架构中。这种设计使得 CorreGen 的方法论贡献集中于对应建模层面，而非特征提取架构的创新。

#### 2.2 与判别式对比学习基线的关系

标准对比 MVC 方法（如 InfoNCE 范式）定义跨视图正负对为：

$$\mathcal{P}_{v_1,v_2}^{+} = \bigcup_{i=1}^{N} \{ \{ \mathbf{x}_i^{(v_1)}, \mathbf{x}_i^{(v_2)}, t_{ii}^{12}=1 \} \}, \quad \mathcal{P}_{v_1,v_2}^{-} = \bigcup_{i=1}^{N} \bigcup_{j=1, j \neq i}^{N} \{ ( \mathbf{x}_i^{(v_1)}, \mathbf{x}_j^{(v_2)}, t_{ij}^{12}=0 ) \}$$

其中 $t_{ij}$ 为硬性二元指示，仅允许实例级一对一匹配。当噪声对应存在时，该硬性指标直接失效。

CorreGen 与 InfoNCE 的关系具有深刻的理论联系（见 Proposition 2）：**当边际分布均匀且后验退化为仅保留实例对时，CorreGen 的生成式目标退化为标准 InfoNCE**：

$$\theta^{*} = \underset{\theta}{\arg\max} \sum_{i=1}^{N} \log \frac{\exp(s(z_i^{(v_1)}, z_i^{(v_2)}) / \tau)}{\sum_{n=1}^{N} \exp(s(z_i^{(v_1)}, z_n^{(v_2)}) / \tau)}$$

这一退化关系证明了 CorreGen 是 InfoNCE 的严格推广，InfoNCE 是其无噪声、硬对应假设下的特例。

#### 2.3 与鲁棒多视图聚类基线的对比

论文与以下鲁棒 MVC 方法进行了系统比较：

| 基线方法 | 核心策略 | 局限性 |
|---------|---------|--------|
| **DCP**（Lin et al., 2022） | 成对重加权 | 无法发现类别级语义对应 |
| **SURE**（Yang et al., 2022b） | 不确定性估计与重加权 | 依赖硬性正负对指标 |
| **GCFAgg**（Yan et al., 2023） | 图卷积融合 | 对噪声对应敏感 |
| **CGCN**（Wang et al., 2024） | 图卷积网络 | 缺乏噪声对应处理机制 |
| **DIVIDE**（Lu et al., 2024） | 判别式对比学习 | 作为骨干网络，目标函数未改变 |
| **CANDY**（Guo et al., 2024） | 跨视图对齐 | 依赖实例级匹配 |
| **ROLL**（Sun et al., 2025） | 鲁棒优化 | 未建模软性语义对应 |

CorreGen 与这些方法的本质差异在于**学习目标的范式转换**（三个关键槽位变化）：

1. **学习目标**：从判别式对比损失（InfoNCE）→ 生成式最大似然估计，通过 EM 优化变分下界，无需硬性正负对。
2. **跨视图对应建模**：从硬性二元关系 $t_{ij}$（仅实例级一对一）→ 自适应软后验分布 $Q_{ij}=P_{ij}^{*}/p_i$，通过最优传输求解多对多软分配。
3. **噪声样本处理**：从无专门机制 → GMM 引导的边缘概率为可信样本赋予更高权重，虚拟样本机制吸收不可对齐样本（$\rho$ 控制容量）。

### 3. 核心机制与因果链路

CorreGen 的鲁棒性来源于一条清晰的因果链路：

**生成式目标 → EM 迭代 → 软对应发现 → 噪声自适应抑制**

具体展开为五个核心模块的协同：

1. **共享编码器 $f_\theta$**：将多视图数据映射至共享嵌入空间，$z_i^{(v)}=f_\theta(x_i^{(v)})$。
2. **GMM 引导的边缘估计器**：拟合高斯混合模型估计每个样本的聚类置信度，计算边际概率 $p(x_i^{(v)})$，为最优传输提供信息性约束。
3. **最优传输对应求解器（E-step）**：基于边际约束和语义相似性矩阵 $S$，通过熵正则化 Sinkhorn 算法求解最优软联合分布 $P^{*}$。
4. **虚拟样本模块**：引入虚拟概率质量 $\rho$，吸收噪声或不可对齐样本，将部分质量分配给虚拟节点。
5. **加权对数似然最大化器（M-step）**：利用 E-step 得到的后验 $Q_{ij}=P_{ij}^{*}/p_i^{(v_1)}$ 最大化加权对数似然，更新编码器参数 $\theta$。

**决定性证据**：消融实验（Table 3）证实，移除 GMM 引导的边缘估计（w/o Guide）或虚拟样本模块（w/o Virtual）均导致聚类性能显著下降。例如 Scene15（MR=0.2, CR=0.2）上，完整 CorreGen 的 ACC 为 41.78，移除 Guide 降至 40.98，而 Vanilla InfoNCE 仅 38.36。后验分布可视化（Figure 3）进一步证实模型能够从噪声对应中逐步发现类别级语义结构。

### 4. 适用边界与局限

#### 4.1 已知局限

1. **聚类数量依赖**：方法需要预先指定聚类数量 $C$ 以拟合 GMM 和计算边际概率。实际应用中 $C$ 可能未知，限制了方法的即插即用性。
2. **噪声比率 $\rho$ 需人工设定**：虚拟样本的噪声比率 $\rho$ 对性能有一定影响。尽管参数分析（Figure 5, 6）表明在较宽范围内稳定，但其最优值依赖真实噪声比例，目前缺乏自适应估计机制。
3. **初始嵌入质量依赖**：GMM 边际估计的质量依赖于初始嵌入空间的区分性。若初始网络训练不充分（warmup 阶段不足），可能影响 E-step 的解质量，形成错误传播。

#### 4.2 适用场景边界

- **强适用场景**：存在显著类别级不匹配和样本级噪声的多视图数据，尤其是类别数已知、视图间语义对应关系复杂的情况（如 UMPC-Food101 上的 10% 精度提升）。
- **弱适用场景**：完全清洁的数据上，CorreGen 退化为 InfoNCE 特例，增益有限；虚拟样本模块在清洁数据上影响较小（消融分析文本证实）。
- **计算约束**：当视图数量 $V$ 远大于 2 时，最优传输的计算复杂度和内存需求需进一步优化。

### 5. 开放问题

1. **自适应噪声比率估计**：如何从数据中自适应地估计 $\rho$，而非依赖先验设定？这直接关系到方法的自动化程度和实际部署能力。
2. **多视图扩展效率**：当 $V \gg 2$ 时，最优传输矩阵的规模和 Sinkhorn 迭代的计算开销如何进一步降低？是否可以通过视图采样或分层传输策略缓解？
3. **更强骨干网络集成**：CorreGen 目前基于 DIVIDE 实现，能否与更强大的特征提取骨干（如 Transformer）或更复杂的模态（如视频、3D 点云）结合？生成式框架的理论优势是否在更强特征空间中依然显著？
4. **在线/流式场景适配**：在完全在线或流式数据场景下，EM 框架的增量更新策略该如何设计？批量 Sinkhorn 算法难以直接适用于单样本或小批量流式到达的场景。
5. **聚类数量未知时的扩展**：能否通过非参数贝叶斯方法（如 Dirichlet 过程混合模型）替代固定 $C$ 的 GMM，使 CorreGen 适用于聚类数量未知的场景？



## 原文 PDF

![[paperPDFs/ICLR_2026/Uncover_Underlying_Correspondence_for_Robust_Multi_view_Clustering.pdf]]
