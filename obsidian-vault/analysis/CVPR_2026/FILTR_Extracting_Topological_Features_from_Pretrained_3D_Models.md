---
title: "FILTR: Extracting Topological Features from Pretrained 3D Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FILTR_Extracting_Topological_Features_from_Pretrained_3D_Models.pdf
project_link: "https://filtr-topology.github.io/"
code_link: "https://huggingface.co/datasets/LouisM2001/donut"
aliases:
- FFT
- FILTR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 利用冻结的预训练编码器作为特征提取器，结合基于集合预测的Transformer解码器（FILTR），从隐式特征中直接预测持续同调图。
primary_logic: 尽管预训练3D编码器在拓扑探测任务上表现有限，但其特征中仍蕴含有用的局部几何与多尺度拓扑信息，通过合适的解码器架构可以有效提取并预测持续同调图。
claims:
- 冻结预训练编码器的FILTR在持续同调图预测上达到或超过端到端基线性能。
- CKA分析表明MAE类模型（尤其是Point-MAE）在多个层上与向量化持续同调图保持对齐。
- 增加存在性损失（existence loss）显著改善重建质量。
- 在低数据量下，冻结编码器的FILTR显著优于端到端DGCNN基线。
---

# FILTR: Extracting Topological Features from Pretrained 3D Models

> [!tip] 核心洞察
> 尽管预训练3D编码器在拓扑探测任务上表现有限，但其特征中仍蕴含有用的局部几何与多尺度拓扑信息，通过合适的解码器架构可以有效提取并预测持续同调图。

| 字段 | 内容 |
|------|------|
| 中文题名 | FILTR：从预训练3D模型中提取拓扑特征 |
| 英文题名 | FILTR: Extracting Topological Features from Pretrained 3D Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.22334) · [Project](https://filtr-topology.github.io/) · [HuggingFace](https://huggingface.co/datasets/LouisM2001/donut) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | FILTR (Filtration Transformer) |
| Dataset | DONUT, ModelNet40, ABC |

> [!tip] 效果简介
> - DONUT (test set) 上，W2 (×10⁻²) / dB (×10⁻³) / PIE Point-MAEc: W2=16.02, dB=9.838, PIE=1.214 vs DGCNN (E2E): W2=24.69, dB=9.948, PIE=1.178 (W2 -8.67)。
> - ModelNet40 (test set) 上，W2 (×10⁻²) / dB (×10⁻³) / PIE Point-MAEc: W2=47.26, dB=13.80, PIE=11.93 vs DGCNN (E2E): W2=47.79, dB=12.51, PIE=9.773 (W2 -0.53)。
> - ABC (subset 3K) 上，W2 (×10⁻²) / dB (×10⁻³) / PIE Point-MAEc: W2=47.99, dB=32.72, PIE=4.393 vs DGCNN (E2E): W2=48.29, dB=31.70, PIE=3.760 (W2 -0.30)。

## 概要

3D点云理解在自动驾驶、机器人等领域至关重要，但当前预训练的3D编码器能否真正捕获形状的全局拓扑结构，仍是一个悬而未决的问题。本工作系统性地评估了主流预训练3D点云编码器（Point-BERT、Point-MAE、PointGPT、PCP-MAE等）对拓扑信息的隐式编码能力，发现这些模型在直接探测任务（连通分量数、亏格数）上表现有限，但其深层特征中仍保留了可提取的多尺度拓扑信号。

核心瓶颈在于：预训练编码器缺乏对全局拓扑结构的显式建模，仅部分保留了局部几何与多尺度拓扑信息。为此，本文提出**FILTR（Filtration Transformer）**，将持久同调图预测建模为集合预测任务，利用冻结的预训练编码器作为特征提取器，结合Transformer解码器直接从隐式特征中预测持续同调对。

关键发现与结果：
- **拓扑探测**：RepSurf在连通分量数上达到83.3%准确率，在亏格数上达到57.7%（Table 1），显著优于其他编码器；CKA分析表明MAE类模型（尤其Point-MAE）在多个层上与向量化持续同调图保持对齐（Figure 6）。
- **持续同调图重建**：冻结编码器的FILTR在DONUT测试集上达到W2=16.02（×10⁻²），优于端到端DGCNN的24.69（Table 3）；在ModelNet40和ABC子集上也达到或超越端到端基线。
- **低数据场景**：在仅2000个训练样本时，冻结Point-MAE的FILTR取得W2=29.74，远优于端到端DGCNN的113.1（Table 11）。
- **损失设计**：存在性损失（existence loss）显著改善重建质量（Table 8），对角线正则化器迫使未匹配预测落在对角线上，贡献零Wasserstein距离。

FILTR的核心方法论借鉴了DETR的集合预测范式，将图像目标检测中的边界框预测迁移为点云拓扑中的持续同调对预测，通过匈牙利匹配与多损失联合优化实现端到端训练。该方法对编码器预训练方法无特殊偏好，且可适配不同filtration类型。

### 拓扑特征在3D理解中的角色

拓扑特征——如连通分量数、亏格、持续同调图——刻画了三维形状的全局结构属性，在形状分类、分割与生成等任务中具有潜在价值。然而，现代3D点云编码器（如 **Point-BERT**、**Point-MAE**、**PointGPT**、**PCP-MAE**）普遍以语义或重建目标进行预训练，其隐层表示是否保留了可提取的拓扑信息，仍是一个开放问题。

### 现有方法缺口

当前预训练的3D点云编码器缺乏对全局拓扑结构信息的显式捕获能力。尽管这些模型在标准语义基准上表现优异，但它们仅能部分保留多尺度拓扑信号。具体而言：

- **探测能力有限**：在DONUT数据集上的线性探测实验（Table 1）表明，即使是最优的预训练编码器 **RepSurf**，在连通分量数预测上仅达83.3%准确率，在亏格预测上仅达57.7%；而 **Point-BERT** 的CLS token在两项任务上分别仅为57.2%和25.9%。
- **逐层衰减模式**：Figure 5的逐层探测曲线揭示，拓扑信息主要集中在Transformer的中间层，深层特征中拓扑信号显著衰减，这与语义信息向深层聚集的趋势形成对比。
- **对齐强度有限**：CKA分析（Figure 6）显示，仅MAE类模型（尤其是Point-MAE）在多个层上与向量化持续同调图保持中等程度的对齐，其他编码器的对齐水平普遍较低。

上述发现指向一个核心瓶颈：**预训练3D编码器的隐层特征中虽蕴含拓扑信息，但无法直接解码为结构化的拓扑描述符**（如持续同调图）。现有的端到端基线方法（如DGCNN、PointNet++）需要从头训练，在低数据场景下表现脆弱，且无法利用大规模预训练模型的泛化能力。

### 本文动机

针对上述缺口，本文提出两个递进的研究目标：

1. **系统评估**：通过线性探测和CKA分析，量化不同预训练3D编码器中拓扑信息的保留程度与分布模式。
2. **特征提取**：设计一个解码器架构，能够从冻结的预训练编码器特征中直接预测持续同调图，将拓扑特征提取转化为集合预测问题。

这一思路的核心洞察在于：尽管预训练3D编码器在拓扑探测任务上表现有限，但其特征中仍蕴含有用的局部几何与多尺度拓扑信息；通过合适的解码器架构，可以有效提取并预测持续同调图，从而在不修改编码器参数的前提下实现拓扑特征的重建。

## 核心方法与创新机理

FILTR的核心创新在于将**持续同调图预测**重新定义为**集合预测问题**，并借鉴目标检测领域DETR的架构范式，构建了一个与编码器预训练方法无关的解码器框架。其关键设计突破体现在以下七个维度：

### 1. 从边界框到持续同调对：任务定义的迁移

FILTR将DETR的集合预测逻辑从图像域迁移至3D拓扑域，在多个关键槽位上进行了系统性替换（Table 2）：

| 设计槽位 | 基线（DETR） | FILTR |
|---------|-------------|-------|
| 输入 | 图像 | 点云 |
| 目标 | 边界框 | 持续同调对 $(b, d)$ |
| 位置编码 | 2D正弦 | 3D补丁中心 |
| 输出约束 | $\text{box} \in [0,1]^4$ | $(b, d)$ 满足 $d > b$ |
| 空类 | 无对象 | 无对 |
| 匹配损失 | 类别+框损失 | 存在性 + 对回归 |
| 正则化 | 无 | 对角线正则化器 |

这种迁移并非简单的输入输出替换，而是针对拓扑对象的特殊性质——**可变数量的点对**、**出生-死亡的顺序约束**、**对角线上的退化点**——进行了精细适配。

### 2. 冻结编码器 + 可学习解码器的分离架构

FILTR的核心架构决策是**完全冻结预训练3D编码器**，仅训练下游的Transformer解码器。这一设计基于一个关键洞察：尽管预训练编码器在拓扑探测任务上表现有限（Table 1中最佳准确率仅为83.3%和57.7%），但其特征中仍蕴含有用的局部几何与多尺度拓扑信号。CKA分析（Figure 6）进一步证实，MAE类模型（尤其是Point-MAE）在多个层上与向量化持续同调图保持对齐。

冻结编码器的策略带来了显著的**数据效率优势**：在仅使用2000个训练样本的低数据量设定下，冻结Point-MAE编码器的FILTR达到2-Wasserstein距离29.74，而端到端训练的DGCNN基线高达113.1（Table 11），差距达83.36。

### 3. 存在性损失：区分真实对与空预测

持续同调图中不同形状的对数量差异显著，解码器需输出固定数量 $N$ 的查询（超过最大图尺寸），因此必须学会“拒绝”多余的预测。FILTR引入**存在性损失** $\mathcal{L}_{\text{exist}}$，对每个预测对输出存在性对数几率，并通过二分类交叉熵监督：

$$\mathcal{L}_{\text{exist}} = -\frac{1}{N} \left( \sum_{i=1}^{M} \log \sigma(\hat{l}_{\pi^{*}(i)}) + \sum_{j \in \bar{\mathcal{M}}} \log (1 - \sigma(\hat{l}_j)) \right)$$

消融实验（Table 8）表明，加入存在性损失使2-Wasserstein距离从23.63降至16.42，证明存在性监督对集合预测质量至关重要。

### 4. 对角线损失：将未匹配预测约束为零贡献

未匹配的预测对在理想情况下应对Wasserstein距离贡献为零，即落在对角线上（出生=死亡）。FILTR通过**对角线损失** $\mathcal{L}_{\text{diag}}$ 显式强制这一约束：

$$\mathcal{L}_{\text{diag}} = \frac{1}{|\bar{\mathcal{M}}|} \sum_{j \in \bar{\mathcal{M}}} (\hat{d}_j - \hat{b}_j)^2$$

该设计的精妙之处在于：使未匹配预测精确落在对角线上后，**无需依赖存在性阈值**即可获得同等重建质量（Table 8, Figure 18），从而消除了阈值调参的工程负担。

### 5. 出生-死亡顺序约束的解码器设计

为保证预测的物理有效性（出生时间必须早于死亡时间），FILTR在解码器输出端施加了结构化的参数化约束：

$$\hat{b}_i = \sigma(\hat{p}_i^{(1)}), \quad \hat{d}_i = \hat{b}_i + \text{softplus}(\hat{p}_i^{(2)})$$

通过sigmoid将出生时间限制在 $(0,1)$，再通过softplus确保死亡时间严格大于出生时间，避免了后处理修正的需要。

### 6. 匈牙利匹配与联合匹配代价

训练时，预测集与真实集之间通过匈牙利算法寻找最优一对一匹配 $\pi^{*}$：

$$\pi^{*} = \arg\min_{\pi} \sum_{i=1}^{M} \mathcal{L}_{\text{match}}(\hat{y}_{\pi(i)}, y_i)$$

匹配代价联合考虑了坐标距离与存在性概率：

$$\mathcal{L}_{\text{match}}(\hat{y}_i, y_j) = \lambda_{\text{reg}} \|\hat{y}_i - y_j\|_2^2 + \lambda_{\text{exist}} (1 - \sigma(\hat{l}_i))$$

这种设计使得匹配过程不仅关注几何精度，同时惩罚将低置信度预测分配给真实对的行为。

### 7. 编码器无关的通用性

FILTR的解码器对编码器的预训练方法无特殊偏好，可适配Point-BERT、Point-MAE、PointGPT、PCP-MAE等多种预训练编码器。实验表明，不同编码器下的FILTR均能达到或超过端到端DGCNN基线的重建性能（Table 3），验证了该架构的**通用性**。

FILTR（Filtration Transformer）的核心设计思想是将持续同调图的预测问题转化为**集合预测（set prediction）任务**。该方法借鉴了目标检测领域DETR的架构范式，但针对拓扑特征提取进行了七项关键适配（Table 2）：输入从图像变为点云，目标从边界框变为持续同调对 $(b, d)$，位置编码从2D正弦函数变为3D补丁中心坐标，输出约束从 $[0,1]^4$ 的边界框变为满足 $d > b$ 的出生-死亡坐标对，空类从“无对象”变为“无对”，匹配损失从类别加框损失变为存在性损失加对回归损失，并新增了对角线正则化器。

整个流水线由四个核心模块串联构成（Figure 7）：

![[assets/figures/papers/paper_list_l2080_https_arxiv_org_abs_2604_22334/figures/008_Figure_7.jpg]]
*Figure 7: FILTR Pipeline. A frozen 3D point-cloud encoder produces features and positional encodings. These condition the decoder through cross-attention. The decoder processes a fixed set of learned queries to predict persistence pairs and their existence probabilities (shown as gray intensities). Training uses a set-prediction loss to match predicted and ground-truth pairs*

1. **冻结的预训练3D编码器**：接收 $p \times 3$ 的点云输入，输出补丁级特征 $\mathbf{F} = \{\mathbf{f}_i\}_{i=1}^n$ 及对应的3D位置编码。编码器在训练期间保持冻结，仅作为特征提取器使用，其预训练方法（Point-BERT、Point-MAE、PointGPT、PCP-MAE等）对FILTR解码器透明。

2. **适配器**：由层归一化与线性投影组成，将编码器输出的特征维度映射到解码器所需的统一维度空间，确保不同预训练编码器的特征可无缝接入解码器。

3. **Transformer解码器**：维护 $N$ 个可学习的查询向量（$N$ 超过最大持续同调图规模），通过交叉注意力机制与编码器特征交互。解码器以逐层自注意力与交叉注意力的方式逐步精炼查询表示，最终每个查询对应一个候选持续同调对。

4. **双头预测层（MLP）**：
   - **持久性预测头**输出原始坐标 $\hat{p}_i^{(1)}, \hat{p}_i^{(2)}$，经解码得到满足出生-死亡约束的坐标：
     $$\hat{b}_i = \sigma(\hat{p}_i^{(1)}), \quad \hat{d}_i = \hat{b}_i + \mathrm{softplus}(\hat{p}_i^{(2)})$$
   - **存在性预测头**输出对数几率 $\hat{l}_i$，经sigmoid函数 $\sigma(\hat{l}_i)$ 转换为该对真实存在的概率，用于区分有效预测与“无对”填充。

训练时，预测集与真实集之间通过匈牙利算法建立最优一对一匹配，损失函数为三项加权和：
$$\mathcal{L} = \mu_{\mathrm{recon}} \mathcal{L}_{\mathrm{recon}} + \mu_{\mathrm{exist}} \mathcal{L}_{\mathrm{exist}} + \mu_{\mathrm{diag}} \mathcal{L}_{\mathrm{diag}}$$
其中重建损失 $\mathcal{L}_{\mathrm{recon}}$ 约束匹配对的坐标精度，存在性损失 $\mathcal{L}_{\mathrm{exist}}$ 以二分类交叉熵监督存在性判定，对角线损失 $\mathcal{L}_{\mathrm{diag}}$ 强制未匹配预测落在对角线（出生=死亡），使其对Wasserstein距离贡献为零。

FILTR提供两种特征聚合变体（Figure 8左）：**L变体**仅使用编码器最后一个Transformer块的特征，**C变体**则将各中间块的特征求和后送入解码器。实验表明C变体通常能捕获更丰富的多尺度拓扑信息。

### 补充图表

![[assets/figures/papers/paper_list_l2080_https_arxiv_org_abs_2604_22334/figures/001_Figure_1.jpg]]
*Figure 1: We evaluate the topological information implicitly captured by pretrained 3D point-cloud encoders through three distinct tasks. The first two tasks assess whether features produced by modern 3D encoders capture the number of connected components (top) and the genus (middle) of the underlying shapes. We introduce DONUT, a novel benchmark with topological labels, and an adapted probing mechanism. The third task (bottom) evaluates to what extent (i) information contained in persistence diagrams is present in encoder features, and (ii) how it can be extracted. To this end, we propose FILTR (Filtration Transformer), the first model that predicts persistence diagrams directly from pretrained, fro...*

### 3.1 流水线总览

FILTR 的整体架构由四个核心模块串联构成，如 Figure 7 所示：

1. **冻结的预训练 3D 编码器**：将输入点云 $X \in \mathbb{R}^{p \times 3}$ 编码为补丁特征 $F = \{f_i\}_{i=1}^n$ 及对应的 3D 补丁中心位置编码。编码器在整个训练过程中保持冻结，不参与梯度更新。
2. **适配器**：由层归一化（LayerNorm）与线性投影组成，将编码器输出的特征维度映射到 Transformer 解码器的隐藏维度，实现不同预训练编码器与解码器之间的即插即用兼容。
3. **Transformer 解码器**：接收 $N$ 个可学习的查询向量（$N$ 大于数据集中最大持续同调对数目），通过交叉注意力与编码器特征交互，以集合预测的方式并行生成所有持续同调对。
4. **双头预测层**：每个查询经解码器处理后，分别送入两个 MLP 头——持久性预测头输出出生-死亡坐标，存在性预测头输出该对是否真实存在的对数几率。

### 3.2 从 DETR 到 FILTR 的迁移适配

FILTR 将目标检测框架 DETR 的集合预测范式迁移到持续同调图生成任务上。Table 2 总结了核心概念的一一对应关系：

![[assets/figures/papers/paper_list_l2080_https_arxiv_org_abs_2604_22334/figures/009_Table_2.jpg]]
*Table 2: Core DETR-FILTR analogies*

- **输入**：从图像变为点云。
- **目标**：从边界框变为持续同调对 $(b, d)$。
- **位置编码**：从 2D 正弦编码变为 3D 补丁中心坐标。
- **输出约束**：从 $\text{box} \in [0,1]^4$ 变为 $(b, d)$ 满足 $d > b$。
- **空类**：从“无对象”变为“无对”（即不存在有效持续同调对）。
- **匹配损失**：从类别损失 + 框回归损失变为存在性损失 + 持续同调对回归损失。
- **正则化**：新增对角线正则化器，用于约束未匹配预测点的位置。

### 3.3 持续同调对解码

解码器的每个查询 $i$ 输出两个原始值 $\hat{p}_i^{(1)}$ 和 $\hat{p}_i^{(2)}$，通过以下约束解码为出生值 $\hat{b}_i$ 和死亡值 $\hat{d}_i$：

$$\hat{b}_i = \sigma(\hat{p}_i^{(1)}), \quad \hat{d}_i = \hat{b}_i + \mathrm{softplus}(\hat{p}_i^{(2)})$$

其中 $\sigma$ 为 sigmoid 函数，$\mathrm{softplus}(x) = \log(1 + e^x)$。该设计强制保证 $\hat{d}_i > \hat{b}_i$，满足持续同调对的半平面约束。同时，存在性预测头输出对数几率 $\hat{l}_i$，其 sigmoid 值 $\sigma(\hat{l}_i)$ 表示该预测对为真实同调对的概率。

### 3.4 损失函数

FILTR 的训练目标由三项加权损失组成：

$$\mathcal{L} = \mu_{\mathrm{recon}} \mathcal{L}_{\mathrm{recon}} + \mu_{\mathrm{exist}} \mathcal{L}_{\mathrm{exist}} + \mu_{\mathrm{diag}} \mathcal{L}_{\mathrm{diag}}$$

#### 3.4.1 最优匹配

给定 $N$ 个预测对 $\{\hat{y}_i\}_{i=1}^N$ 和 $M$ 个真实对 $\{y_j\}_{j=1}^M$（$N > M$），首先通过匈牙利算法求解最优一对一匹配 $\pi^*$：

$$\pi^{*} = \arg\min_{\pi} \sum_{i=1}^{M} \mathcal{L}_{\mathrm{match}}(\hat{y}_{\pi(i)}, y_i)$$

其中匹配代价函数同时考虑坐标距离与存在性置信度：

$$\mathcal{L}_{\mathrm{match}}(\hat{y}_i, y_j) = \lambda_{\mathrm{reg}} \|\hat{y}_i - y_j\|_2^2 + \lambda_{\mathrm{exist}} (1 - \sigma(\hat{l}_i))$$

第一项惩罚预测坐标与真实坐标的欧氏距离，第二项惩罚低存在性概率的预测被匹配。

#### 3.4.2 重建损失

对匹配成功的 $M$ 个预测对，计算均方误差：

$$\mathcal{L}_{\mathrm{recon}} = \frac{1}{M} \sum_{i=1}^{M} \|\hat{y}_{\pi^{*}(i)} - y_i\|_2^2$$

#### 3.4.3 存在性损失

对所有 $N$ 个预测进行二分类监督，匹配上的对标签为 1，未匹配的集合 $\bar{\mathcal{M}}$ 标签为 0：

$$\mathcal{L}_{\mathrm{exist}} = -\frac{1}{N} \left( \sum_{i=1}^{M} \log \sigma(\hat{l}_{\pi^{*}(i)}) + \sum_{j \in \bar{\mathcal{M}}} \log (1 - \sigma(\hat{l}_j)) \right)$$

消融实验（Table 8）表明，加入存在性损失使 2-Wasserstein 距离从 $23.63 \times 10^{-2}$ 降至 $16.42 \times 10^{-2}$，证明存在性监督对集合预测质量至关重要。

#### 3.4.4 对角线损失

强制未匹配的预测对落在持续同调图的对角线上（即 $\hat{d}_j = \hat{b}_j$），使其对 Wasserstein 距离的贡献为零：

$$\mathcal{L}_{\mathrm{diag}} = \frac{1}{|\bar{\mathcal{M}}|} \sum_{j \in \bar{\mathcal{M}}} (\hat{d}_j - \hat{b}_j)^2$$

消融实验（Table 8, Figure 18）表明，对角线损失使未匹配预测精确收敛到对角线，从而无需依赖存在性概率阈值即可获得同等重建质量。

### 补充图表

![[assets/figures/papers/paper_list_l2080_https_arxiv_org_abs_2604_22334/figures/004_Figure_4.jpg]]
*Figure 4: Encoder Probing Pipeline. We probe the features of each (frozen) transformer block on DONUT to predict the number of connected components and the genus*

## 实验与关键发现

### 主结果：持续同调图重建

FILTR 的核心实验评估冻结预训练编码器特征在持续同调图预测任务上的表现。所有模型均在 DONUT 训练集（23,579 个网格，每网格采样 1024 点）上训练，并在 DONUT 测试集、ModelNet40 测试集及 ABC 子集（3K 样本）上评估。评估指标包括 2-Wasserstein 距离（W2，×10⁻²）、dB 归一化距离（×10⁻³）和 PIE。

**Table 3** 展示了 FILTR 在不同编码器下的重建结果。关键发现：冻结 Point-MAE 编码器的 FILTR（Point-MAEc）在 DONUT 测试集上取得 W2=16.02，显著优于端到端训练的 DGCNN 基线（W2=24.69），降幅达 8.67。在 ModelNet40 上，Point-MAEc 的 W2=47.26，略优于 DGCNN 的 47.79；在 ABC 子集上，Point-MAEc 的 W2=47.99，同样略优于 DGCNN 的 48.29。这表明冻结编码器搭配 FILTR 解码器在分布内数据上具有显著优势，在分布外数据上至少与端到端基线持平。

值得注意的是，**PointNet++** 在所有数据集上的重建误差均显著高于其他架构，这与其作为较早期点云网络的设计局限性一致。

### 低数据量下的鲁棒性

**Table 11** 揭示了冻结编码器方案在低数据场景下的突出优势。当训练数据缩减至仅 2K 样本时，冻结 Point-MAE 编码器的 FILTR 保持 W2=29.74，而端到端 DGCNN 基线急剧退化至 W2=113.1，差距达 83.36。这一结果表明，预训练编码器提取的通用几何特征为拓扑重建提供了强先验，在标注数据稀缺时尤为关键。

### 消融实验

#### 存在性损失与对角线损失

**Table 8** 系统消融了损失函数各组件的作用。加入存在性损失（existence loss）后，W2 从 23.63 降至 16.42（使用阈值过滤），证明存在性监督对集合预测质量至关重要——它使模型学会区分有效同调对与空预测。

对角线损失（diagonal loss）进一步优化了未匹配预测的行为：它强制未匹配的预测点精确落在出生-死亡对角线上，使其对 Wasserstein 距离贡献为零。消融表明，引入对角线损失后，模型无需依赖存在性阈值即可获得同等重建质量（参见 **Figure 18**）。完整损失函数为：

![[assets/figures/papers/paper_list_l2080_https_arxiv_org_abs_2604_22334/figures/030_Figure_18.jpg]]
*Figure 18: Effect of*

$$\mathcal{L} = \mu_{\mathrm{recon}} \mathcal{L}_{\mathrm{recon}} + \mu_{\mathrm{exist}} \mathcal{L}_{\mathrm{exist}} + \mu_{\mathrm{diag}} \mathcal{L}_{\mathrm{diag}}$$

#### 解码器深度

**Figure 15** 展示了以 Point-MAE 为骨干时，解码器深度对 2-Wasserstein 距离的影响。在 DONUT 测试集、ModelNet 和 ABC 三个数据集上，解码器深度从 2 层增加至 6 层时，W2 持续改善；超过 6 层后收益递减。这一趋势验证了 Transformer 解码器在集合预测任务上的可扩展性，同时表明 6 层是精度与效率的合理平衡点。

### 特征对齐分析

**Figure 6** 通过线性 CKA（Centered Kernel Alignment）量化编码器特征与向量化持续同调图之间的相似度。核心发现：MAE 类预训练模型（尤其是 Point-MAE）在多个 Transformer 层上与向量化持续同调图保持较高对齐，而其他预训练策略（如 Point-BERT 的 CLS token）对齐度较低。这解释了为何 Point-MAE 作为冻结骨干时重建性能最优——其隐式特征中保留了更多拓扑结构信息。

**Figure 14** 通过受控特征失配实验验证了 CKA 指标的可靠性：随机置换部分特征后，CKA 相似度随置换比例 α 增加而单调下降，确认高 CKA 值真实反映了特征空间与拓扑表示之间的结构对齐，而非伪影。

### 失败模式与局限性

尽管 FILTR 在整体重建指标上表现优异，但存在明确的失败模式：

1. **最持久同调对预测能力有限**：预训练编码器难以捕获全局几何结构，导致模型对代表形状主要拓扑特征的最持久同调对预测精度不足。这是当前冻结编码器方案的根本瓶颈。

2. **分布外泛化退化**：在 ABC 等与 ShapeNet 预训练分布差异较大的数据集上，预测误差显著增大（ABC 上 W2=47.99，远高于 DONUT 的 16.02）。这表明预训练特征的拓扑信息具有领域依赖性。

3. **filtration 类型限制**：主要验证基于 α-filtration；Vietoris-Rips filtration 仅在低数据量下测试，其泛化性尚需进一步验证。

### 探测实验补充

**Table 1** 报告了各编码器在 DONUT 上的拓扑探测准确率。端到端训练的 RepSurf 在连通分量数（83.3%）和亏格数（57.7%）预测上均取得最高准确率，而冻结预训练编码器的探测性能普遍较低（Point-BERT CLS token 仅 57.2% 和 25.9%）。**Figure 5** 的逐层分析进一步揭示，不同编码器的拓扑信息分布在不同深度的层中，且亏格数预测（右图）的层间波动显著大于连通分量数预测（左图），说明高阶拓扑特征更难被编码器捕获。

### 补充图表

![[assets/figures/papers/paper_list_l2080_https_arxiv_org_abs_2604_22334/figures/011_Table_3.jpg]]
*Table 3: Reconstruction results of FILTR. All the models are trained on DONUT, and evaluated on: a held-out test set from DONUT, ModelNet40 test set, a subset of ABC. We use the same configuration for all pretrained backbones, and report results obtained by training FILTR with either the features of the last transformer block (L), or a combination of the features from all transformer blocks (C) (see Fig. 8 (left)). We highlight PointNet++ for its remarkably higher reconstruction errors compared to other architectures. We discuss this point and provide training details in the Appendix*

## 定位与知识库关联

### 1. 方法溯源：DETR 集合预测范式的 3D 拓扑迁移

FILTR 的核心方法论直接继承自 2D 目标检测领域的 DETR（Detection Transformer）框架，将持久同调图预测重新表述为**集合预测问题**。Table 2 系统性地列举了两者之间的概念类比，揭示了方法论迁移中的关键适配：

| 设计维度 | DETR（2D 目标检测） | FILTR（拓扑特征提取） |
|---------|-------------------|---------------------|
| 输入 | 图像 | 点云 |
| 目标 | 边界框 | 持续同调对 |
| 位置编码 | 2D 正弦编码 | 3D 补丁中心 |
| 输出约束 | box ∈ [0,1]⁴ | (b,d) 满足 d>b |
| 空类 | 无对象 | 无对 |
| 匹配损失 | 类别+框损失 | 存在性 + 对回归 |
| 正则化 | 无 | 对角线正则化器 |

这一迁移并非简单的领域替换，而是针对拓扑对象的独特性质进行了三项关键创新：

1. **输出空间的几何约束**：持久同调对必须满足出生时间严格小于死亡时间（b < d）。FILTR 通过解码器设计强制该约束：$\hat{b}_i = \sigma(\hat{p}_i^{(1)}), \quad \hat{d}_i = \hat{b}_i + \mathrm{softplus}(\hat{p}_i^{(2)})$，其中 softplus 保证死亡时间相对于出生时间的增量始终为正。

2. **存在性建模与对角线正则化**：DETR 的“无对象”类别在拓扑语境下对应“无持久同调对”。FILTR 引入存在性损失 $\mathcal{L}_{\mathrm{exist}}$（二分类交叉熵）和对角线损失 $\mathcal{L}_{\mathrm{diag}} = \frac{1}{|\bar{\mathcal{M}}|} \sum_{j \in \bar{\mathcal{M}}} (\hat{d}_j - \hat{b}_j)^2$，强制未匹配的预测对收敛到对角线（b=d），使其对 Wasserstein 距离的贡献为零。消融实验（Table 8）表明，添加存在性损失使 W2 从 23.63 降至 16.42；对角线损失则使模型无需依赖存在性阈值即可获得同等重建质量。

3. **匹配代价的联合设计**：匈牙利算法的最优匹配代价函数 $\mathcal{L}_{\mathrm{match}}(\hat{y}_i, y_j) = \lambda_{\mathrm{reg}} \|\hat{y}_i - y_j\|_2^2 + \lambda_{\mathrm{exist}} (1 - \sigma(\hat{l}_i))$ 同时考虑坐标距离和存在性概率，实现了集合级预测与真实持久图的结构对齐。

### 2. 编码器生态中的定位：冻结预训练模型作为特征提取器

FILTR 在方法谱系中的独特定位在于**将预训练 3D 编码器视为不可微的黑盒特征提取器**，而非端到端微调的对象。这一设计选择使其与以下基线形成明确对比：

- **端到端基线**（PointNet, PointNet++, DGCNN, RepSurf）：这些模型从零开始在 DONUT 上训练以直接预测拓扑标签。Table 1 显示，RepSurf 在连通分量数预测上达到 83.3% 准确率，在亏格预测上达到 57.7%，均显著优于冻结编码器的探测结果。然而，Table 3 揭示了一个关键反转：当使用冻结的 Point-MAE 编码器配合 FILTR 解码器时，在 DONUT 测试集上的 W2 距离（16.02）显著优于端到端 DGCNN（24.69），表明**预训练特征中蕴含的拓扑信息可通过合适的解码架构有效提取，且优于从零开始的端到端学习**。

- **预训练编码器探测**（Point-BERT, Point-MAE, PointGPT, PCP-MAE）：直接在这些冻结编码器的各层特征上训练线性分类器以预测拓扑不变量。Table 1 显示，即使最佳层（Point-BERT 的 CLS token）也仅达到 57.2%（连通分量）和 25.9%（亏格）的准确率，表明**预训练编码器并未显式编码全局拓扑信息**。然而，Figure 6 的 CKA 分析揭示了更深层的现象：MAE 类模型（尤其是 Point-MAE）在多个层上与向量化持久同调图保持对齐，说明**拓扑信号以分布式、多尺度的形式隐含存在于特征中**，而非集中在某一层或某个 token 中。

- **潜在预测模型**（Point2Vec）：该模型通过自监督学习直接预测拓扑描述符，在 CKA 对齐分析中作为参考基线。

FILTR 的关键洞察在于：**编码器探测的失败并不意味着拓扑信息的缺失，而是表明需要更强大的解码机制来聚合和重组分布式拓扑信号**。Figure 5 的逐层探测曲线进一步支持这一观点——不同编码器在不同层深度上表现出拓扑信息的非单调分布，而 FILTR 的 (C) 变体通过聚合所有中间层特征，在多个数据集上取得了最优或接近最优的重建性能。

### 3. 适用边界与失效模式

基于实验证据，FILTR 的适用边界可归纳为以下约束：

1. **预训练数据分布依赖**：Table 3 显示，当评估数据与预训练数据分布差异增大时，性能显著退化。在 DONUT 测试集（与 ShapeNet 预训练分布接近）上，Point-MAEc 的 W2 为 16.02；在 ModelNet40 上增至 47.26；在 ABC 子集上进一步升至 47.99。这表明**冻结编码器的特征质量高度依赖于预训练域与目标域的对齐程度**。

2. **全局拓扑的捕获瓶颈**：论文明确指出，预测最持久同调对（代表形状的主要拓扑特征）的能力有限，因为预训练编码器难以捕获全局几何结构。这一局限根源于当前 3D 预训练方法（如 MAE）主要关注局部几何重建，缺乏对全局拓扑的显式建模。

3. **filtration 类型的泛化限制**：主要实验基于 α-filtration 进行验证，Vietoris-Rips filtration 仅在低数据量场景下测试。不同 filtration 类型产生的持久图具有不同的统计特性，FILTR 在更广泛的 filtration 类型上的泛化能力尚待验证。

4. **低数据量下的相对优势**：Table 11 显示，在仅 2K 训练样本的低数据量场景下，冻结 Point-MAEc 的 W2 为 29.74，而端到端 DGCNN 高达 113.1。这一巨大差距（-83.36）表明，**当标注数据稀缺时，冻结预训练编码器的 FILTR 具有显著的样本效率优势**，因为解码器只需学习如何从已有的丰富特征中提取拓扑信息，而非同时学习特征提取和拓扑推理。

### 4. 开放问题与未来方向

论文提出了两个值得关注的开放问题，指向方法论的潜在扩展方向：

1. **跨模态拓扑推理**：多模态基础模型（如文本、图像编码器）如何以不同于 3D 模型的方式编码结构化或关系性信息，以用于拓扑推理？这一问题暗示 FILTR 的集合预测框架可能迁移到其他模态，但需要验证不同模态编码器是否同样隐含保留了拓扑信号。

2. **跨领域迁移**：结论能否迁移到图学习等缺乏强通用编码器的领域？当前 FILTR 的成功依赖于 3D 点云领域成熟的预训练编码器生态。在图结构数据领域，通用预训练模型尚未达到同等成熟度，FILTR 范式的直接迁移可能面临特征质量瓶颈。

此外，基于本文的实验证据，以下方向值得进一步探索：能否通过**拓扑感知的预训练目标**（如在 MAE 预训练中引入持久同调损失）增强编码器对全局拓扑的捕获能力，从而提升 FILTR 对最持久同调对的预测精度？解码器深度消融（Figure 15）显示 6 层 Transformer 块后收益递减，这是否暗示当前编码器特征的拓扑信息容量存在上限？这些问题指向 FILTR 框架与编码器预训练策略之间的深层协同优化空间。

### 5. 知识库定位总结

FILTR 在 3D 视觉与拓扑数据分析的交叉地带占据了一个独特的方法论位置：它**不是**一个新的拓扑特征提取器，也**不是**一个改进的预训练方法，而是一个**连接预训练视觉表征与拓扑推理的通用解码框架**。其核心贡献在于揭示了“预训练编码器隐含拓扑信息”这一现象，并提供了系统性的探测、对齐和重建工具链来验证和利用这一现象。在方法谱系中，FILTR 可被视为 DETR 集合预测范式在拓扑领域的成功迁移，同时为未来拓扑感知的 3D 表征学习提供了新的评估基准和研究视角。

## 原文 PDF

![[paperPDFs/CVPR_2026/FILTR_Extracting_Topological_Features_from_Pretrained_3D_Models.pdf]]
