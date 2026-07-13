---
title: "Global and Local Topology-Aware Graph Generation via Dual Conditioning Diffusion"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Global_and_Local_Topology_Aware_Graph_Generation_via_Dual_Conditioning_Diffusion.pdf
project_link: null
code_link: null
aliases:
- GLTAGGDCD
- DualDiff
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/chemistry_and_drug_discovery
core_operator: "DualDiff runs coupled latent diffusion over node-level local embeddings and cluster-level global embeddings with dual conditioning."
primary_logic: "It alternates global-to-local FiLM conditioning and local-to-global message-pooling conditioning so graph samples preserve local substructures and global topology."
claims:
- "The model decomposes graph generation into local and global latent branches rather than a single node-level process."
- "Dual conditioning enables dynamic information exchange between topology scales."
- "The note reports improved or competitive MMD metrics on Planar and SBM plus molecular generation gains."
---

# Global and Local Topology-Aware Graph Generation via Dual Conditioning Diffusion

> [!tip] 核心洞察
> 将联合分布 p(Z_l, Z_g) 分解为 p(Z_l|Z_g)p(Z_g) 和 p(Z_g|Z_l)p(Z_l) 两种互补形式，利用 FiLM 风格的条件化（全局→局部）和消息传递+池化（局部→全局）交替进行，使模型同时具备全局和局部拓扑感知能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 通过双重条件扩散实现全局与局部拓扑感知的图生成 |
| 英文题名 | Global and Local Topology-Aware Graph Generation via Dual Conditioning Diffusion |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=IZV9k5BGxi) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/chemistry_and_drug_discovery |
| Method | DualDiff |
| Dataset | Planar, SBM |

> [!tip] 效果简介
> - Planar 上，Deg. MMD 为 0.0003，对比 0.0004 (GDSS)，变化 -0.0001。
> - Planar 上，Clus. MMD 为 0.0275，对比 0.0291 (GDSS)，变化 -0.0016。
> - Planar 上，Orbit MMD 为 0.0002，对比 0.0003 (GDSS)，变化 -0.0001。

## 概要

本文提出 **DualDiff**，一个统一的潜在扩散模型，旨在解决图生成中全局拓扑与局部结构联合建模的难题。DualDiff 通过双分支扩散过程（节点级与子图级）和双重条件机制（dual conditioning mechanism），交替利用全局信息指导局部生成、局部信息指导全局生成，从而有效捕捉图中从局部子结构到全局拓扑的多尺度依赖关系。在 Planar、SBM、ZINC250k、QM9 等多个基准数据集上，DualDiff 在度分布、聚类系数、轨道计数等 MMD 指标以及分子生成的 FCD、KL 分数上均达到或超越了现有最优方法。



传统节点级图生成模型（如 GraphRNN、GDSS、DiGress）在生成过程中独立处理每个节点，难以同时捕捉图中从局部子结构到全局拓扑的多尺度依赖关系，尤其是全局与局部信息的联合分布建模不足。尽管已有工作尝试引入全局信息（如 SubgDiff 通过子图预测、Graphusion 使用图级伪标签），但它们通常将全局信息作为静态条件，缺乏全局与局部之间的动态信息交换。

DualDiff 的核心动机是：将联合分布 p(Z_l, Z_g) 分解为 p(Z_l|Z_g)p(Z_g) 和 p(Z_g|Z_l)p(Z_l) 两种互补形式，通过交替条件化实现全局与局部信息的动态交互，使模型同时具备全局和局部拓扑感知能力。



## 核心方法与创新机理

DualDiff 的核心创新可归纳为四个关键设计变更：

| 变更维度 | 基线方法 | DualDiff 方案 | 证据锚点 |
|---------|---------|--------------|---------|
| 生成范式 | 节点级独立生成（如 GDSS, DiGress） | 节点级与子图级双分支联合扩散 | "DualDiff employs a two-branch diffusion process to learn topological dependencies at both the node and subgraph levels within a unified framework" |
| 条件机制 | 无条件或自条件（self-conditioning） | 双重条件：全局↔局部交替条件化 | "a dual conditioning mechanism is introduced to promote interaction between these two branches, wherein global and local information are alternately utilized as conditions" |
| 全局信息提取 | 无显式全局建模或仅使用图级伪标签 | 基于聚类（K-means/谱聚类）的拓扑增强全局嵌入 | "To extract global topological information from a graph, we leverage graph clustering methods... for molecular graphs, we apply the K-means algorithm in the atom coordinate space... For generic graphs, we utilize spectral clustering" |
| 采样策略 | 对称同步更新 | 非对称交替：m 步局部更新 + 1 步全局更新 | "we alternate m steps of process (i) with a single step of process (ii) to enhance the stability of the sampling process." |



![[assets/figures/papers/iclr26_0001_IZV9k5BGxi_Global_and_Local_Topology-Aware_Graph_Generation/figures/001_Figure_1.jpg]]
*Figure 1: The workflow of DualDiff (Left) and details of the dual conditioning mechanism (Right).*

DualDiff 的整体流程如下：

1. **图自编码器编码**：将原始图 G 通过编码器 E_phi 映射到统一潜在空间 Z ∈ R^{N×d}。
2. **信息分离**：将 Z 分解为局部信息 Z_l ∈ R^{N×d} 和全局信息 Z_g ∈ R^{K×d}（K 为聚类数）。
3. **双分支扩散**：在节点级（Z_l）和子图级（Z_g）分别进行扩散去噪，使用独立的去噪网络 D_theta_l 和 D_theta_g。
4. **双重条件化**：在反向去噪过程中，交替执行全局→局部条件化（FiLM 风格）和局部→全局条件化（消息传递+池化）。
5. **解码重构**：将去噪后的 Z_l 和 Z_g 通过解码器 D_psi 重构图 G_hat。

![Figure 1: The workflow of DualDiff (Left) and details of the dual conditioning mechanism (Right).]()



### 5.1 图自编码器

编码器 E_phi 将图 G 编码为潜在表示 Z，然后分离为局部和全局信息：

$$ \pmb{Z} = \mathcal{E}_{\phi}(\mathcal{G}) \implies \left\{ \begin{array}{l} \pmb{Z}_l = \pmb{Z} + \sigma_0 \pmb{I} \\ \pmb{Z}_g = \mathrm{GlobalExtraction}(\pmb{Z}, \mathcal{G}) \end{array} \right. \implies \hat{\mathcal{G}} = \mathcal{D}_{\psi}(\pmb{Z}_l, \pmb{Z}_g) $$

重构损失为：

$$ \mathcal{L}_{rec} = -\mathbb{E}_{q(\mathcal{G}) q_{\phi}(\pmb{Z}|\mathcal{G})} \left[ p_{\psi}(\mathcal{G}|\pmb{Z}_l, \pmb{Z}_g) \right] $$

对于分子图，编码器使用 Equivariant Graph Neural Networks (EGNNs) 实现 SE(3)-等变性；对于通用图，使用消息传递图神经网络 (MPNNs)。

### 5.2 全局信息提取

通过聚类方法从局部表示中提取全局信息：

$$ S_g = \mathrm{Clustering}(\mathcal{G}) \implies Z_g = \mathrm{Pooling}(S_g, Z) \in \mathbb{R}^{K \times d} $$

- 对于分子图：在原子坐标空间应用 K-means 聚类
- 对于通用图：在图拉普拉斯矩阵上进行谱分解后应用 K-means

### 5.3 双分支扩散过程

前向 SDE（随机微分方程）：

$$ \left\{ \begin{array}{l} d\pmb{Z}_{l,t} = f_{l,t}(\pmb{Z}_{l,t}) dt + s_{l,t} d\pmb{W}_{l,t} \\ d\pmb{Z}_{g,t} = f_{g,t}(\pmb{Z}_{g,t}) dt + s_{g,t} d\pmb{W}_{g,t} \end{array} \right. $$

反向 SDE：

$$ \left\{ \begin{array}{l} d\bar{\pmb{Z}}_{l,t} = \left( f_{l,t}(\bar{\pmb{Z}}_{l,t}) - s_{l,t}^2 \nabla_{\pmb{Z}_l} \log p_t(\bar{\pmb{Z}}_{l,t}) \right) d\bar{t} + s_{l,t} d\bar{\pmb{W}}_{l,t} \\ d\bar{\pmb{Z}}_{g,t} = \left( f_{g,t}(\bar{\pmb{Z}}_{g,t}) - s_{g,t}^2 \nabla_{\pmb{Z}_g} \log p_t(\bar{\pmb{Z}}_{g,t}) \right) d\bar{t} + s_{g,t} d\bar{\pmb{W}}_{g,t} \end{array} \right. $$

训练目标为两个去噪网络的均方误差之和：

$$ \mathbb{E}_{(Z_{l,0}, Z_{g,0}) \sim q_{\phi}(\cdot|\mathcal{G}) p_{\sigma}(\tilde{Z}_l, \tilde{Z}_g | Z_{l,0}, Z_{g,0})} [ \| D_{\theta_l}(\tilde{Z}_l, \sigma) - Z_{l,0} \|^2 + \| D_{\theta_g}(\tilde{Z}_g, \sigma) - Z_{g,0} \|^2 ] $$

### 5.4 双重条件机制

双重条件机制基于联合概率路径的两种分解方式（附录 E.1）：

$$ p_t(Z_l, Z_g) = \int_{Z_{l,0}, Z_{g,0} \sim \mathrm{data}} p_t(Z_l | Z_{l,0}) p_t(Z_g | Z_l, Z_{g,0}) dZ_{l,0} dZ_{g,0} $$

$$ p_t(Z_l, Z_g) = \int_{Z_{l,0}, Z_{g,0} \sim \mathrm{data}} p_t(Z_l | Z_g, Z_{l,0}) p_t(Z_g | Z_{g,0}) dZ_{l,0} dZ_{g,0} $$

条件选择以概率 p 交替进行：

$$ (C_l, C_g) = \left\{ \begin{array}{ll} ((\hat{Z}_{l,0}, \hat{Z}_{g,0}), 0) & \text{with prob } p \\ (0, (\hat{Z}_{l,0}, \hat{Z}_{g,0})) & \text{with prob } 1-p \end{array} \right. $$

**过程 (i)：全局→局部条件化**（FiLM 风格）

根据节点与全局簇的相似度，应用簇特定的仿射变换：

$$ \hat{Z}_{l,0}^{',i} = \gamma^{y_i} \odot \hat{Z}_{l,0}^i + \beta^{y_i}, \text{ where } y_i = \arg\max_{j} \text{sim}(\hat{Z}_{l,0}^i, \hat{Z}_{g,0}^j) $$

**过程 (ii)：局部→全局条件化**（消息传递+池化）

通过消息传递和池化从局部细节提取全局条件：

$$ C = \mathrm{Linear}(\mathrm{Pool}(\mathrm{MP}(\hat{Z}_{l,0}))) \Rightarrow C = \mathrm{Concat}(\hat{Z}_{g,0}, C) \Rightarrow \hat{Z}_{g,0}' = \mathrm{GNN}(Z_{g,t}, C, \sigma_t) $$

![Figure 2: Comparison between different conditioning methods during the reverse process. (a) diffusion without conditioning; (b) self-conditioning; (c) dual conditioning.]()

### 5.5 采样策略

采用非对称交替策略：每执行 m 步局部更新后，执行 1 步全局更新。这种设计增强了采样过程的稳定性。



## 实验与关键发现

### 6.1 通用图生成结果

**Table 1: Comparison of advanced models on Planar and SBM datasets.**

![[assets/figures/papers/iclr26_0001_IZV9k5BGxi_Global_and_Local_Topology-Aware_Graph_Generation/figures/005_Table_1.jpg]]
*Table 1: Comparison of advanced models on Planar and SBM datasets. More experiments on the Ego-Small, Community-small, and Grid datasets are included in Appendix C.1.*

| 数据集 | 指标 | DualDiff | GDSS (最优基线) | 改进 |
|-------|------|---------|----------------|------|
| Planar | Deg. MMD | **0.0003** | 0.0004 | -0.0001 |
| Planar | Clus. MMD | **0.0275** | 0.0291 | -0.0016 |
| Planar | Orbit MMD | **0.0002** | 0.0003 | -0.0001 |
| SBM | Deg. MMD | **0.0004** | 0.0005 | -0.0001 |
| SBM | Clus. MMD | **0.0473** | 0.0499 | -0.0026 |
| SBM | Orbit MMD | **0.0365** | 0.0400 | -0.0035 |

**Table 8: Experiments on generic graph generation.**

| 数据集 | DualDiff | GDSS | GraphRNN |
|-------|---------|------|---------|
| Ego-small | **0.005** | 0.007 | 0.018 |
| Community-small | **0.007** | 0.009 | 0.022 |
| Grid | **0.0003** | 0.0004 | 0.003 |

### 6.2 分子生成结果

**Table 2: Experiments on ZINC250K dataset.**

![[assets/figures/papers/iclr26_0001_IZV9k5BGxi_Global_and_Local_Topology-Aware_Graph_Generation/figures/006_Table_2.jpg]]
*Table 2: Experiments on ZINC250K dataset. Following previous studies, we report the FCD and KL scores, where higher values indicate better performance. The results are reported from EDM-SyCo and the original papers. Methods that do not report the KL metric are denoted as N.A.*

| 方法 | FCD (↑) | KL (↑) | Novelty | Uniqueness | Validity |
|-----|---------|-------|---------|-----------|---------|
| DualDiff | **0.91±0.02** | **0.98±0.01** | 1.00±0.00 | 1.00±0.00 | 0.92±0.02 |
| EDM-SyCo | 0.87 | 0.97 | 1.00 | 1.00 | 0.93 |
| GEOLDM | 0.82 | 0.93 | 1.00 | 1.00 | 0.91 |

**Table 4: Experiments of 3D molecular generation on the QM9 Dataset.**

![[assets/figures/papers/iclr26_0001_IZV9k5BGxi_Global_and_Local_Topology-Aware_Graph_Generation/figures/008_Table_4.jpg]]
*Table 4: Experiments of 3D molecular generation on the QM9 Dataset.*

| 方法 | Atom Sta (%) | Mol Sta (%) | Valid & Unique (%) |
|-----|-------------|------------|-------------------|
| DualDiff | **98.9** | **88.7** | **99.3** |
| GEOLDM | 98.7 | 82.7 | 99.1 |
| EQUIFM | 98.5 | 80.9 | 98.8 |

**Table 9: Experiments of different generative methods on QM9 dataset.**

| 方法 | FCD | NSPKD |
|-----|-----|-------|
| DualDiff | **0.092** | **0.0001** |
| LGD | 0.112 | 0.0003 |
| GDSS | 0.135 | 0.0005 |

### 6.3 消融研究

**Table 5: Ablation study of dual conditioning.**

![[assets/figures/papers/iclr26_0001_IZV9k5BGxi_Global_and_Local_Topology-Aware_Graph_Generation/figures/009_Table_5.jpg]]

| 条件方法 | FCD (↑) | KL (↑) |
|---------|---------|-------|
| 无条件 | 0.85 | 0.93 |
| 自条件 | 0.88 | 0.95 |
| 双重条件 | **0.91** | **0.98** |

**Table 15: Model performance of different conditioning methods at distinct diffusion steps.**

| 条件方法 | 100 步 | 500 步 | 1000 步 |
|---------|-------|-------|--------|
| 无条件 | 0.038 | 0.029 | 0.024 |
| 自条件 | 0.025 | 0.019 | 0.016 |
| 双重条件 | **0.012** | **0.008** | **0.006** |

**Table 16: Comparison of asymmetric and symmetric methods**

| 策略 | Enzymes (Avg. MMD) | Planar (Avg. MMD) |
|-----|-------------------|------------------|
| 对称 | 0.0447 | 0.0146 |
| 非对称 (m=5) | **0.0333** | **0.0093** |

**Table 13: Experiments of different clustering methods.**

| 聚类方法 | FCD | NSPKD |
|---------|-----|-------|
| K-means | **0.092** | **0.0001** |
| 谱聚类 | 0.094 | 0.0004 |
| Louvain | 0.100 | 0.0003 |

### 6.4 实验公平性说明

- 所有实验在 NVIDIA 4090 GPU 上运行，使用 Adam 优化器，学习率从 {1e-3, 5e-4, 1e-4} 中选择
- 每个实验重复三次，报告平均结果
- 数据集均为公开可用数据集（ZINC250k, QM9, MOSES, Planar, SBM 等），确保可复现性
- 代码将在 https://github.com/Xyhi/DualDiff 公开

### 补充图表

![[assets/figures/papers/iclr26_0001_IZV9k5BGxi_Global_and_Local_Topology-Aware_Graph_Generation/figures/007_Table_3.jpg]]
*Table 3: Comparison between advanced hierarchical models.*



## 定位与知识库关联

DualDiff 属于**潜在扩散模型**在**图生成**领域的扩展，其方法谱系如下：

1. **基础扩散模型**：基于 EDM (Karras et al., 2022) 框架，使用广义噪声调度和反向过程
2. **潜在扩散范式**：继承自 LDM (Rombach et al., 2022) 和 GEOLDM (Xu et al., 2023)，先训练自编码器再训练扩散模型
3. **双分支架构**：区别于单分支扩散（GDSS, DiGress），DualDiff 同时建模节点级和子图级信息
4. **双重条件机制**：超越自条件（self-conditioning），实现全局与局部信息的双向动态交互
5. **层次化生成**：与 PPGN、HiGen 等层次化模型相比，DualDiff 通过扩散过程实现更灵活的层次化建模

**局限性**：
- 未明确讨论模型在超大规模图（如百万节点）上的可扩展性
- 全局信息提取依赖于聚类方法，聚类质量可能影响生成效果，且聚类数 K 需要手动设定
- 双重条件机制引入了额外的计算开销
- 在分子生成中，有效性（Validity）指标（92%）仍有提升空间
- 未讨论模型对图结构噪声或缺失数据的鲁棒性

**开放问题**：
- 双重条件机制中概率 p 的具体设置或学习方式
- 解码器 D_psi 的具体架构细节未完全公开
- 在条件生成任务中，DualDiff 是否能够扩展到其他类型的条件（如分子性质、图标签）
- 非对称交替策略中 m 值（局部更新步数）如何选择
- 模型在动态图或时序图生成任务上的适用性尚未探索



## 原文 PDF

![[paperPDFs/ICLR_2026/Global_and_Local_Topology_Aware_Graph_Generation_via_Dual_Conditioning_Diffusion.pdf]]
