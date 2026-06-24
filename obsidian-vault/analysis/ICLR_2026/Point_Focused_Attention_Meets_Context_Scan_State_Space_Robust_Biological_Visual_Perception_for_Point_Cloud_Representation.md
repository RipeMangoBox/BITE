---
title: "Point-Focused Attention Meets Context-Scan State Space: Robust Biological Visual Perception for Point Cloud Representation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Point_Focused_Attention_Meets_Context_Scan_State_Space_Robust_Biological_Visual_Perception_for_Point_Cloud_Representation.pdf
openreview_forum_id: KQPoMbxInu
aliases:
- Point-Focused_At
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/classification_and_understanding
core_operator: "受生物视觉中央凹视觉与眼跳推理启发的point-focused attention和context-scan state space，通过双分支竞争归一化注意力与希尔伯特曲线引导的双向S6实现局部-全局协同建模。"
primary_logic: "在单softmax中计算局部邻居和空间下采样特征的注意力权重，以竞争归一化方式动态融合细粒度与粗粒度特征，模拟中央凹视觉感知；并利用保持空间邻近性的希尔伯特曲线序列化点云，引导状态空间模型进行准确的全局推理，从而以线性复杂度实现局部几何与长程交互的高效整合。"
claims:
- "PointLearner在ModelNet40上达到94.2%的OA，成为新的最佳结果。"
- "在S3DIS语义分割上，PointLearner的mIoU为74.3%，超过最优注意力方法MVNet(73.8%)和最优SSM方法HydraMamba(73.6%)。"
- "S3DIS 上 mIoU = 74.3"
- "ScanObjectNN 上 OA = 89.8"
---

# Point-Focused Attention Meets Context-Scan State Space: Robust Biological Visual Perception for Point Cloud Representation

> [!tip] 核心洞察
> 在单softmax中计算局部邻居和空间下采样特征的注意力权重，以竞争归一化方式动态融合细粒度与粗粒度特征，模拟中央凹视觉感知；并利用保持空间邻近性的希尔伯特曲线序列化点云，引导状态空间模型进行准确的全局推理，从而以线性复杂度实现局部几何与长程交互的高效整合。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 点聚焦注意力与上下文扫描状态空间：面向点云表示的鲁棒生物视觉感知 |
| 英文题名 | Point-Focused Attention Meets Context-Scan State Space: Robust Biological Visual Perception for Point Cloud Representation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=KQPoMbxInu); [GitHub](https://github.com/Point-Cloud-Learning/PointLearner) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/classification_and_understanding |
| Method | PointLearner |
| Dataset | S3DIS, ScanObjectNN |

> [!tip] 效果简介
> - S3DIS 上，mIoU 为 74.3，对比 73.8 (MVNet)，变化 +0.5。
> - ScanObjectNN 上，OA 为 89.8，对比 89.3 (PointMamba)，变化 +0.5。

## 概述

点云表示学习的核心瓶颈在于：基于局部注意力的网络牺牲了全局感知能力，而基于状态空间模型（SSM）的方法在压缩上下文信息时导致局部学习不足，难以同时捕获精细局部结构和全局长程依赖。现有方法通常仅采用单一算子，无法在局部几何建模与全局上下文感知之间取得平衡。

本文提出 **PointLearner**，一种受生物视觉系统启发的混合架构。其核心思想源于中央凹视觉与眼跳推理：在单次 softmax 中计算局部邻居和空间下采样特征的注意力权重，以**竞争归一化**方式动态融合细粒度与粗粒度特征，模拟中央凹视觉感知；并利用保持空间邻近性的**希尔伯特曲线**序列化点云，引导双向 S6 状态空间模型进行准确的全局推理，从而以线性复杂度实现局部几何与长程交互的高效整合。

主要结果：
- 在 ModelNet40 分类上，PointLearner 达到 **94.2% OA**，成为该基准上的最佳结果（Table 1）。
- 在 S3DIS 语义分割上，mIoU 达到 **74.3%**，超过最优注意力方法 MVNet（73.8%）和最优 SSM 方法 HydraMamba（73.6%）（Table 3）。
- 在 ScanObjectNN 鲁棒性测试上，OA 达到 **89.8%**，优于 PointMamba（89.3%）（Table 4）。

消融实验表明，点聚焦注意力与上下文扫描状态空间的结合（94.17%）显著优于各自独立使用（92.93%/91.94%），验证了模块间的协同效应（Table 10）。竞争归一化融合优于简单加和融合（94.17% vs 93.43%），且未增加额外计算量（Table 8）。希尔伯特曲线序列化优于 Z-Order 曲线（94.17% vs 93.06%），并优于可学习序列化（92.78%）（Table 12）。

值得注意的是，PointLearner 目前未采用预训练策略，而对比方法中的部分最佳性能（如 Point-MAE、Point-BERT）借助了大规模预训练，存在性能提升空间。混合架构与现有自监督预训练方法的兼容性尚未探索，极端稀疏条件下的鲁棒性亦有待加强。

## 背景与动机

点云表示学习是三维视觉的基础任务，其核心挑战在于如何同时捕获精细的局部几何结构和全局长程依赖关系。现有方法主要分为两大范式：基于注意力的方法和基于状态空间模型（SSM）的方法，但二者各存瓶颈。

基于注意力的方法（如Point Transformer系列、Swin3D等）通过局部窗口或邻域内的自注意力机制建模点间关系，在局部几何刻画上表现出色。然而，这种局部注意力的设计天然牺牲了对全局上下文的感知能力——每个查询点只能看到其邻域范围内的信息，无法建立跨区域的远距离依赖。尽管部分工作尝试通过下采样和分层结构扩大感受野，但全局信息的整合仍然间接且不充分。

基于SSM的方法（如PointMamba、HydraMamba等）利用状态空间模型的长序列建模能力，将点云序列化后进行全局上下文扫描，在长程依赖捕获上具有线性复杂度的优势。然而，SSM在将三维空间结构压缩为一维序列的过程中，不可避免地损失了局部邻域内的细粒度几何信息，导致局部学习不足。这种“压缩即丢失”的问题在复杂几何结构上尤为突出。

上述困境的实质是：**局部精细感知与全局上下文建模在现有架构中难以兼得**。注意力网络强于局部而弱于全局，SSM网络强于全局而弱于局部，二者形成了互补但割裂的局面。

受生物视觉系统的启发，本文提出了一种新的解决思路。人类视觉系统通过**中央凹视觉（foveal vision）**实现对注视点区域的高分辨率精细感知，同时保持对周边区域的低分辨率全局意识；通过**眼跳推理（saccade inference）**在不同注视点之间快速切换，整合空间上不连续但结构上相关的信息，形成对场景的完整理解。这一“先聚焦、后扫描”的感知模式，为点云的局部-全局协同建模提供了自然的计算隐喻。

基于此，本文提出PointLearner，一个仿生设计的混合架构网络，核心思想是：**用点聚焦注意力（Point-Focused Attention）模拟中央凹视觉的自适应感受野选择，用上下文扫描状态空间（Context-Scan State Space）模拟眼跳推理的序列化几何推断**。前者通过双分支竞争归一化注意力，在同一softmax下动态融合局部细粒度特征和全局粗粒度特征，实现描述性与鲁棒性的平衡；后者利用希尔伯特曲线保持空间邻近性的序列化特性，引导双向S6状态空间模型沿高保真扫描路径进行准确的全局推理。这种混合范式以线性复杂度整合了注意力与SSM的各自优势，为点云表示学习开辟了新的技术路径。

## 核心创新

PointLearner的核心创新在于通过生物视觉启发的双阶段混合架构，解决了现有方法在局部精细建模与全局长程依赖之间的根本性权衡。其关键创新点可归纳为以下四个维度。

### 1. 点聚焦注意力：竞争归一化的双分支局部-全局融合

现有局部注意力方法（如Point Transformer系列）仅计算查询点与其K近邻之间的注意力，牺牲了全局语义感知能力。PointLearner提出**点聚焦注意力（Point-Focused Attention, PFA）**，模拟人眼中央凹视觉（foveal vision）的自适应感受野选择机制，通过双分支设计在同一softmax下实现细粒度与粗粒度特征的**竞争归一化融合**：

- **局部邻居分支（Local Neighbor Branch, LNB）**：对每个查询点 $p_i$ 的 $K$ 个最近邻 $N_i$ 计算细粒度注意力，捕获精细几何结构：
  $$A_i^l = \text{softmax}(\langle Q_i^l, K_{N_i}^l \rangle / \sqrt{D}), \quad \text{LNB}(p_i) = A_i^l V_{N_i}^l$$

- **空间下采样分支（Spatial Downsampling Branch, SDB）**：利用空间下采样特征 $S$ 建立粗粒度全局注意力，感知场景级语义：
  $$A_i^s = \text{softmax}(Q_i^s, K^s / \sqrt{D}), \quad \text{SDB}(p_i) = A_i^s V^s$$

- **竞争归一化融合**：将局部注意力logits与全局注意力logits拼接后输入**同一softmax**，使两类特征在归一化过程中相互竞争，动态平衡局部描述性与全局鲁棒性：
  $$A_i = \text{softmax}(\text{Concat}(Q_i^l K_{N_i}^l, Q_i^s K^s) / \sqrt{D})$$
  $$\text{PFA}(p_i) = A_i^l V_{N_i}^l + A_i^s V^s$$

消融实验证实了该设计的有效性：仅使用LNB时OA为92.11%，加入SDB后提升至94.17%（Table 6-7）；竞争归一化融合（94.17%）显著优于简单加和融合（93.43%），且不增加额外计算量（Table 8）。整个PFA的计算复杂度为 $\Omega(\text{PFA}) = 6ND^2 + 2MD^2 + 2NKD + 4NMD$，与点数 $N$ 成线性关系（Eq.6）。

### 2. 上下文扫描状态空间：希尔伯特曲线引导的双向S6全局推理

基于状态空间模型（SSM）的方法（如PointMamba、HydraMamba）虽能高效捕获长程依赖，但在序列化压缩上下文时导致局部学习不足。PointLearner提出**上下文扫描状态空间（Context-Scan State Space, CSSS）**，模拟人眼眼跳推理（saccade inference）机制，通过以下设计实现高保真全局几何推理：

- **希尔伯特曲线序列化**：采用希尔伯特曲线（Hilbert curve）对PFA输出特征进行序列化，建立具有空间邻近性保证的扫描路径。消融实验表明，希尔伯特曲线序列化（94.17% OA）显著优于Z-Order曲线（93.06%）和可学习序列化（92.78%），验证了空间邻近性保持对SSM推理质量的关键作用（Table 12）。

- **双向S6**：在序列化特征上应用双向Mamba S6算子，同时从正向和反向扫描点云，实现更全面的上下文建模。双向S6（94.17%）相比单向S6（93.08%）带来约1.1个百分点的提升（Table 9）。

PFA与CSSS的协同效应显著：两者结合（94.17%）远超各自独立使用（PFA仅92.93%，CSSS仅91.94%），体现了“先聚焦局部、后扫描全局”的pipeline设计的有效性（Table 10）。

### 3. 可学习诱导点池化：自适应空间下采样

传统最远点采样（FPS）在低采样率下性能退化严重。PointLearner提出**诱导点池化（Induced Point Pooling, IPP）**，引入 $M$ 个可学习的 $D$ 维诱导点 $I \in \mathbb{R}^{M \times D}$，通过交叉注意力自适应地从输入特征 $F$ 中聚合空间下采样特征：
$$\text{IPP}(F) = \text{softmax}(I, K^p / \sqrt{D}) V^p, \quad \text{其中 } (K^p, V^p) = (W_k^p, W_v^p) F$$

实验表明，IPP在极端稀疏条件下（256点采样率）仍保持93.39%的准确率，鲁棒性远超FPS（Figure 6）。

### 4. 注意力-SSM混合架构范式

PointLearner的核心架构贡献在于首次将注意力与SSM以生物视觉系统为框架进行有机整合：每个PointLearner块内，PFA先执行局部-全局竞争注意力，CSSS随后沿希尔伯特路径进行双向状态空间推理（Figure 2）。这种“先聚焦、后扫描”的顺序设计，使得模型能够以线性复杂度同时捕获精细局部几何和长程语义交互，在ModelNet40（94.2% OA）、S3DIS（74.3% mIoU）、ScanObjectNN（89.8% OA）等多个基准上均取得最优结果，且未使用任何预训练策略（Table 1, 3, 4）。

## 整体框架

![[assets/figures/papers/iclr26_0010_KQPoMbxInu_Point-Focused_Attention_Meets_Context-Scan_State/figures/006_Figure_2.jpg]]
*Figure 2: Left: Pipeline of PointLearner. Right: Architecture of PointLearner block, where the line between the red dots represent the saccade path guided by the serialization, which is used for geometric inference by the state space model*

![[assets/figures/papers/iclr26_0010_KQPoMbxInu_Point-Focused_Attention_Meets_Context-Scan_State/figures/007_Figure_3.jpg]]
*Figure 3: Diagram of point-focused attention with the competitive normalized attention mechanism*

PointLearner 的整体 pipeline 遵循编码器-解码器结构，核心创新在于其 PointLearner 块内部的双阶段设计：**点聚焦注意力（Point-Focused Attention, PFA）** 先进行局部-全局特征融合，随后由 **上下文扫描状态空间（Context-Scan State Space, CSSS）** 完成全局长程几何推理。这一“先聚焦、后扫描”的流程直接模拟了生物视觉系统中中央凹视觉与眼跳推理的协同机制。

### 输入输出流

点云输入首先经过嵌入层投影到高维特征空间。编码器采用基于残差连接的分层特征聚合策略：通过最远点采样（FPS）进行下采样，每层包含若干 PointLearner 块串联处理。解码器则通过线性插值上采样恢复空间分辨率，最终由任务头输出全局类别 logits（分类）或逐点类别 logits（分割）。

### PointLearner 块内部结构

每个 PointLearner 块由两个顺序排列的子模块构成：

1. **点聚焦注意力（PFA）**：采用双分支设计——局部邻居分支（Local Neighbor Branch, LNB）对每个查询点的 K 近邻进行细粒度注意力计算，空间下采样分支（Spatial Downsampling Branch, SDB）则利用诱导点池化（Induced Point Pooling, IPP）提取的粗粒度全局特征建立注意力关系。两个分支的注意力权重在**同一个 softmax** 中进行竞争归一化融合，使模型能够动态平衡局部几何细节与全局语义感知，模拟中央凹视觉对外周信息的自适应选择。

2. **上下文扫描状态空间（CSSS）**：接收 PFA 融合后的特征，首先通过希尔伯特曲线将无序点云序列化为保持空间邻近性的一维序列，然后送入双向 S6 状态空间模型进行几何推理。希尔伯特曲线引导的高保真扫描路径确保了可靠的点间结构依赖，双向扫描则实现更全面的上下文建模，模拟眼跳推理过程。

### 关键设计决策

- **模块顺序**：PFA 在前、CSSS 在后，确保状态空间模型处理的是已经过局部-全局注意力精炼的特征，而非原始点特征。
- **下采样策略**：空间下采样分支采用可学习的诱导点池化（IPP）替代传统 FPS，通过 $M$ 个可训练的 $D$ 维诱导点 $I \in \mathbb{R}^{M \times D}$ 自适应地聚合空间特征，在低采样率下表现出更强的鲁棒性。
- **序列化方法**：CSSS 使用希尔伯特曲线而非 Z-Order 曲线或可学习序列化，以更高保真度保持空间相邻关系，为状态空间模型提供更准确的扫描路径。

整个架构的线性复杂度由 PFA 的计算复杂度保证：$\Omega(\text{PFA}) = 6ND^2 + 2MD^2 + 2NKD + 4NMD$，与点数 $N$ 成线性关系，使得 PointLearner 在捕获精细局部结构和全局长程依赖的同时保持计算效率。

## 核心模块与公式推导

PointLearner 的核心由两个顺序排列的模块构成：**点聚焦注意力 (Point-Focused Attention, PFA)** 和 **上下文扫描状态空间 (Context-Scan State Space, CSSS)**。PFA 模拟生物视觉的中央凹感知，在单点级别动态融合细粒度局部几何与粗粒度全局语义；CSSS 模拟眼跳推理，沿空间保持的序列路径进行全局上下文建模。

### 点聚焦注意力 (PFA)

PFA 采用双分支设计，通过竞争归一化机制融合两个尺度的信息。

**局部邻居分支 (Local Neighbor Branch, LNB)** 对查询点 $p_i$ 的 $K$ 个最近邻进行细粒度注意力计算：

$$(Q^l, K^l, V^l) = (W_q^l, W_k^l, W_v^l) F$$

$$A_i^l = \text{softmax}(\langle Q_i^l, K_{N_i}^l \rangle / \sqrt{D})$$

$$\text{LNB}(p_i) = A_i^l V_{N_i}^l$$

其中 $F \in \mathbb{R}^{N \times D}$ 为输入特征，$N_i$ 表示点 $p_i$ 的 $K$ 个邻居索引，$D$ 为特征维度。

**空间下采样分支 (Spatial Downsampling Branch, SDB)** 利用下采样特征 $S \in \mathbb{R}^{M \times D}$ 建立粗粒度全局注意力：

$$(Q^s, K^s, V^s) = (W_q^s F, W_k^s S, W_v^s S)$$

$$A_i^s = \text{softmax}(Q_i^s, K^s / \sqrt{D})$$

$$\text{SDB}(p_i) = A_i^s V^s$$

下采样特征 $S$ 通过**诱导点池化 (Induced Point Pooling, IPP)** 获得。IPP 引入 $M$ 个可学习的诱导点 $I \in \mathbb{R}^{M \times D}$，自适应地从原始特征中提取空间压缩表示：

$$(K^p, V^p) = (W_k^p, W_v^p) F$$

$$\text{IPP}(F) = \text{softmax}(I, K^p / \sqrt{D}) V^p$$

**竞争归一化融合** 是 PFA 的核心创新。不同于简单加和，LNB 和 SDB 的注意力权重在同一个 softmax 中竞争计算：

$$A_i = \text{softmax}(\text{Concat}(Q_i^l K_{N_i}^l, Q_i^s K^s) / \sqrt{D})$$

$$A_i^l, A_i^s = \text{split}(A_i, [K, M])$$

$$\text{PFA}(p_i) = A_i^l V_{N_i}^l + A_i^s V^s$$

该机制迫使模型在局部细粒度特征与全局粗粒度特征之间动态权衡，模拟中央凹视觉自适应选择最有效感受野信息的感知过程。消融实验证实，竞争归一化融合 (94.17% OA) 显著优于加和融合 (93.43% OA)，且不增加额外计算量 (Table 8)。

PFA 的整体计算复杂度为：

$$\Omega(\text{PFA}) = 6ND^2 + 2MD^2 + 2NKD + 4NMD$$

与点数 $N$ 呈线性关系，保证了在大规模点云上的可扩展性。

### 上下文扫描状态空间 (CSSS)

CSSS 在 PFA 提取的局部-全局融合特征基础上，模拟眼跳推理进行全局几何推断。其关键设计在于序列化策略：采用 **希尔伯特曲线 (Hilbert curve)** 将无序点云映射为一维序列，建立高保真度的空间相邻关系。如 Figure 5 所示，希尔伯特曲线在保持空间邻近性上显著优于 Z-Order 曲线。

序列化后的特征送入**双向 S6 (Bidirectional S6)** 状态空间模型。S6 是 Mamba 提出的输入依赖选择性 SSM，其连续形式为：

$$h'(t) = A h(t) + B x(t), \quad y(t) = C h(t)$$

经零阶保持离散化后：

$$h_t = \bar{A} h_{t-1} + \bar{B} x_t, \quad y_t = C h_t$$

$$\bar{A} = e^{\Delta A}, \quad \bar{B} = (\Delta A)^{-1}(e^{\Delta A} - I)(\Delta B)$$

其中 $\Delta$ 为时间尺度参数，$\bar{A}$ 和 $\bar{B}$ 是输入的函数，使模型成为线性时变系统。双向设计同时沿序列正向和反向扫描，实现更全面的上下文建模。消融实验表明，双向 S6 (94.17% OA) 优于单向 S6 (93.08% OA)，希尔伯特序列化 (94.17% OA) 优于 Z-Order (93.06% OA) 和可学习序列化 (92.78% OA) (Table 9, Table 12)。

PFA 与 CSSS 的协同效应在 Table 10 中得到验证：两者结合 (94.17% OA) 显著优于各自独立使用 (92.93% / 91.94%)，证明局部-全局注意力建模与序列化状态空间推理的互补性。

## 实验与分析

### 主实验结果

PointLearner在四个标准基准上进行了系统评估，涵盖物体分类、零件分割、语义分割和鲁棒性测试。所有主实验结果均来自无预训练设置，与部分依赖大规模预训练的对比方法（如Point-MAE、Point-BERT）相比，公平性需注意。

**ModelNet40物体分类**（Table 1）：PointLearner达到**94.2% OA**，成为该数据集上的新最佳结果。该性能超越了基于注意力的Point-BERT（93.2%）和Point-MAE（93.8%），以及基于SSM的PointMamba（93.6%），验证了混合注意力-SSM架构在全局形状识别上的优势。


![[assets/figures/papers/iclr26_0010_KQPoMbxInu_Point-Focused_Attention_Meets_Context-Scan_State/figures/008_Table_1.jpg]]
*Table 1: Experimental results on Model- Table 2: Experimental results on ShapeNet dataset. Net40 dataset. †: Pre-training strategy. †: Pre-training strategy*

**ShapeNet零件分割**（Table 2）：PointLearner取得**86.9% Ins. mIoU**，与最优方法PTv3（87.0%）基本持平，超过HydraMamba（86.7%）和PointMamba（86.5%）。这表明点聚焦注意力在细粒度局部几何建模上具有竞争力。

**S3DIS语义分割**（Table 3）：PointLearner的mIoU达**74.3%**，显著超过最优注意力方法MVNet（73.8%）和最优SSM方法HydraMamba（73.6%），提升幅度为+0.5个百分点。该结果直接支撑了核心瓶颈分析——纯注意力方法牺牲全局感知，纯SSM方法局部学习不足，而PointLearner通过双分支协同有效弥合了这一差距。


![[assets/figures/papers/iclr26_0010_KQPoMbxInu_Point-Focused_Attention_Meets_Context-Scan_State/figures/009_Table_3.jpg]]
*Table 3: Experimental results on S3DIS dataset. †: Pre-training strategy. Table 4: Experimental results on ScanObjectNN dataset. †: Pre-training strategy*

**ScanObjectNN鲁棒性测试**（Table 4）：在包含背景噪声和遮挡的真实扫描数据上，PointLearner达到**89.8% OA**，超过PointMamba（89.3%）和GAD（88.9%），证明生物视觉启发的局部-全局协同建模对真实世界扰动具有更强的鲁棒性。

### 关键消融实验

消融实验在ModelNet40上系统验证了各模块的独立贡献和协同效应（Tables 6-10, 12; Figure 6）。


![[assets/figures/papers/iclr26_0010_KQPoMbxInu_Point-Focused_Attention_Meets_Context-Scan_State/figures/021_Figure_6.jpg]]
*Figure 6: Quantitative results of IPP and FPS*

**局部邻居分支（LNB）的必要性**（Table 6）：移除LNB后，OA从94.17%骤降至92.11%（下降2.06个百分点），参数量仅减少0.79M。该结果证实细粒度局部感知是模型性能的基石，缺失局部邻居注意力会导致几何细节信息的严重丢失。

**空间下采样分支（SDB）的有效性**（Table 7）：单独移除SDB使OA从94.17%降至93.06%（下降1.11个百分点）。SDB以约16%的吞吐量代价（183→163 FPS）换取了粗粒度全局语义的感知能力，验证了模拟中央凹视觉中粗粒度感知的必要性。

**竞争归一化融合的优越性**（Table 8）：与简单加和融合（93.43%）相比，竞争归一化融合达到94.17%，提升0.74个百分点，且参数量和FLOPs完全一致（7.36M / 0.610G）。关键机制在于：在同一softmax下计算局部和全局分支的注意力权重，使两类特征形成"竞争"关系，动态决定每个查询点对细粒度与粗粒度信息的依赖比例，这比独立计算后相加更能模拟生物中央凹视觉的自适应感受野选择。


![[assets/figures/papers/iclr26_0010_KQPoMbxInu_Point-Focused_Attention_Meets_Context-Scan_State/figures/017_Table_8.jpg]]
*Table 8: Ablation results with different multiscale fusion. Table 9: Ablation results with both state space models. Table 10: Ablation results with PFA and CSCC*

**双向S6的必要性**（Table 9）：双向S6（94.17%）显著优于单向S6（93.08%），提升1.09个百分点。单向扫描仅沿希尔伯特曲线的一个方向进行状态空间推理，而双向设计模拟了眼跳过程中来回扫描的推理模式，能捕获更完整的空间上下文依赖。代价是参数增加1.3M，吞吐量从181FPS降至163FPS。

**PFA与CSSS的协同效应**（Table 10）：单独使用PFA（点聚焦注意力）仅达92.93%，单独使用CSSS（上下文扫描状态空间）仅达91.94%，而两者结合跃升至94.17%。该结果揭示了核心因果机制：PFA负责局部几何的精细建模，CSSS负责全局长程依赖的推理，两者并非简单叠加，而是形成"先聚焦后扫描"的级联协同——PFA输出的高质量局部特征为CSSS的状态空间推理提供了更准确的序列化输入。

**希尔伯特曲线序列化的关键作用**（Table 12）：希尔伯特曲线（94.17%）显著优于Z-Order曲线（93.06%）和可学习序列化（92.78%）。原因在于希尔伯特曲线具有最优的空间邻近保持性（Figure 5），序列化后相邻点在三维空间中也倾向于相邻，这为状态空间模型建立了高保真度的点间结构依赖，使S6的几何推理更加准确。代价是序列化计算开销略高，吞吐量（163FPS）低于Z-Order（187FPS）。

**诱导点池化（IPP）的鲁棒性优势**（Figure 6）：在低采样率下，IPP的鲁棒性远强于最远点采样（FPS）。当采样点数降至256时，FPS的准确率急剧下降，而IPP仍保持93.39%的OA。这是因为FPS在稀疏条件下难以保证采样点对全局形状的覆盖，而可学习的诱导点能自适应地调整采样位置，从全局特征中聚合信息。

### 失败模式与局限性

尽管PointLearner在多个基准上取得最优结果，仍存在以下局限：

1. **预训练缺失**：当前未采用任何预训练策略，而对比方法中的最佳性能（如Point-MAE的93.8%）常借助大规模自监督预训练。混合注意力-SSM架构与现有自监督预训练方法（如Masked Autoencoding）的兼容性尚未探索，这限制了在大规模无标注数据上的性能潜力。

2. **极端稀疏条件下的性能下降**：在256点采样率下，OA从1024点的94.17%降至约92.0%（下降约2.2个百分点），表明在极端稀疏条件下局部邻居的KNN图质量和希尔伯特曲线序列化的空间邻近性均会退化。

3. **吞吐量权衡**：双向S6和希尔伯特序列化带来了约20%的吞吐量下降（从约200FPS降至163FPS），在实时性要求较高的应用场景中可能需要针对性优化。

## 方法谱系与知识库定位

### 生物视觉启发的混合架构定位

PointLearner 的核心贡献在于将点云表示学习从“纯注意力”或“纯状态空间模型（SSM）”的单一范式，推进到**注意力与 SSM 协同的混合架构**。这一设计并非简单的模块堆砌，而是受生物视觉系统（中央凹视觉与眼跳推理）的明确引导：

- **与纯注意力方法的关系**：Point-MAE、Point-BERT、PTv3 等方法依赖自注意力机制进行局部或全局建模。然而，现有局部注意力网络（如窗口注意力）牺牲了全局感知能力，而全局注意力则面临二次复杂度瓶颈。PointLearner 通过点聚焦注意力（PFA）在单次 softmax 中同时计算局部邻居和空间下采样特征的注意力权重，以竞争归一化方式动态融合细粒度与粗粒度特征（Eq.(5)），从而在**线性复杂度**下模拟中央凹视觉的自适应感受野选择（Figure 1）。这一机制使 PFA 的计算复杂度与点数 $N$ 保持线性关系（$\Omega(\text{PFA}) = 6ND^2 + 2MD^2 + 2NKD + 4NMD$，Eq.(6)），显著区别于传统注意力的二次增长。

- **与纯 SSM 方法的关系**：PointMamba、HydraMamba 等基于 SSM 的方法虽具有线性复杂度的长程建模优势，但在将点云压缩为一维序列时导致局部几何学习不足。PointLearner 的上下文扫描状态空间（CSSS）采用**希尔伯特曲线序列化**保持空间邻近性（Figure 5），并引入**双向 S6** 实现更全面的上下文推理。消融实验表明，希尔伯特曲线序列化优于 Z-Order 曲线（OA 94.17% vs 93.06%，Table 12）和可学习序列化（92.78%），验证了保真度高的空间相邻扫描路径对 SSM 几何推理的关键作用。

- **混合范式的协同效应**：PFA 与 CSSS 的结合产生了显著的模块协同——两者联合使用达到 OA 94.17%，而各自独立使用仅分别为 92.93% 和 91.94%（Table 10）。这印证了“先聚焦后扫描”的生物视觉流水线在点云理解中的有效性：PFA 负责精细局部几何建模，CSSS 负责全局长程上下文推理。

### 适用边界与约束条件

1. **无预训练场景下的最优性**：PointLearner 在 ModelNet40 上达到 94.2% OA（Table 1），成为不使用预训练方法中的最佳结果。但需注意，Point-MAE 等基于预训练的方法在更大规模数据上可能具有优势，PointLearner 目前未采用预训练策略，其性能上限在标注数据有限时可能受限。

2. **点密度鲁棒性**：得益于诱导点池化（IPP）替代传统最远点采样（FPS），PointLearner 在低采样率下表现出较强鲁棒性——在 256 点采样时仍保持 93.39% 准确率（Figure 6）。然而，从 1024 点降至 256 点时性能仍下降约 2.2%，极端稀疏条件下的鲁棒性有待加强。

3. **序列化策略的精度-效率权衡**：希尔伯特曲线序列化虽精度最高（94.17% OA），但吞吐量（163 FPS）低于 Z-Order 曲线（Table 12）。在实时性要求严格的场景下，需根据应用需求在精度与效率间权衡。

### 局限与开放问题

**已知局限**：

- **预训练兼容性未验证**：PointLearner 的混合架构（注意力 + SSM）与现有基于 Transformer 的自监督预训练方法（如 Point-MAE 的掩码重建）的兼容性尚未探索，限制了在大规模无标注点云数据上的应用潜力。
- **下采样方法的泛化性**：IPP 在低采样率下的优势虽已证明（Figure 6），但其可学习诱导点的初始化策略和在不同任务间的迁移能力缺乏系统分析。
- **希尔伯特曲线的计算开销**：希尔伯特曲线序列化需要额外的空间编码步骤，在极大规模点云（如室外场景）上的可扩展性未经验证。

**开放问题**：

1. 如何设计专门针对混合注意力-SSM 模型的自监督预训练策略？现有掩码重建方法假设统一的特征提取器，而 PFA 与 CSSS 的顺序依赖关系可能要求新的预训练范式。
2. 在更大规模点云数据集（如 Waymo Open Dataset、KITTI-360）上，生物视觉启发的混合范式是否仍能保持线性复杂度和高效性？希尔伯特曲线序列化在高分辨率点云上的空间保真度是否退化？
3. 竞争归一化融合机制是否可以推广到其他多尺度特征融合场景？其“竞争”本质是否适用于视频点云或动态场景理解？

*注：部分对比方法（如 Point-MAE、Point-BERT）使用了大规模预训练，而 PointLearner 未使用预训练，直接性能对比的公平性需在解读时注意。*

## 原文 PDF

![[paperPDFs/ICLR_2026/Point_Focused_Attention_Meets_Context_Scan_State_Space_Robust_Biological_Visual_Perception_for_Point_Cloud_Representation.pdf]]
