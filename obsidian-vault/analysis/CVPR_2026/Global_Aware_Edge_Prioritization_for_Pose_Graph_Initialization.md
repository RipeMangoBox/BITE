---
title: Global-Aware Edge Prioritization for Pose Graph Initialization
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Global_Aware_Edge_Prioritization_for_Pose_Graph_Initialization.pdf
project_link: null
code_link: "https://github.com/weitong8591/global_edge_prior"
aliases:
- GEP
- GAEPPGI
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过图神经网络学习全局边可靠性排名，并以此指导多最小生成树构造，辅以连通性感知的距离调制来强化弱连接区域并降低图直径。
primary_logic: 在几何验证之前，利用自监督的SfM几何信号（RANSAC内点数和3D点重叠度）训练GNN，预测体现全局结构关系的边匹配分数；进而通过多MST与距离调制使初始位姿图不仅全局连通、冗余，而且直径更短，从而显著提升稀疏连接下的重建鲁棒性和精度。
claims:
- 在IMC23-PhotoTourism上，去除GNN后k=1时AUC@5°从61.2降至55.4，证实GNN全局推理不可替代。
- 在高度歧义的VisymScenes上，我们的方法在k=5时达到75.6 AUC@5°，超过专用的Doppelganger++后处理，证明全局边优先级排序对视觉歧义具有强鲁棒性。
- IMC23-PhotoTourism 上 AUC@5° (k=5 MSTs, COLMAP relative pose) = 73.1
- VisymScenes 上 AUC@5° (k=5 MSTs, COLMAP relative pose) = 75.6 (all modulation components enabled)
---

# Global-Aware Edge Prioritization for Pose Graph Initialization

> [!tip] 核心洞察
> 在几何验证之前，利用自监督的SfM几何信号（RANSAC内点数和3D点重叠度）训练GNN，预测体现全局结构关系的边匹配分数；进而通过多MST与距离调制使初始位姿图不仅全局连通、冗余，而且直径更短，从而显著提升稀疏连接下的重建鲁棒性和精度。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向位姿图初始化的全局感知边优先级排序 |
| 英文题名 | Global-Aware Edge Prioritization for Pose Graph Initialization |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.21963) · [Code](https://github.com/weitong8591/global_edge_prior) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Global Edge Prioritization |
| Dataset | IMC23-PhotoTourism, VisymScenes, MegaDepth |

> [!tip] 效果简介
> - IMC23-PhotoTourism 上，AUC@5° (k=5 MSTs, COLMAP relative pose) 73.1 vs 66.5 (MegaLoc) (+6.6)。
> - VisymScenes 上，AUC@5° (k=5 MSTs, COLMAP relative pose) 75.6 (all modulation components enabled) vs – (–)。
> - MegaDepth 上，AUC@5° (COLMAP relative pose) consistently the best across all k MSTs vs MegaLoc, SALAD, DINOv2 (largest margin at k=1, k=2)。

## 概要

### 问题瓶颈

运动恢复结构（Structure-from-Motion, SfM）的重建质量高度依赖初始位姿图的质量。现有方法在构建初始位姿图时，普遍采用**逐图像独立的k近邻检索**——每张图像仅基于自身描述子与其余图像的余弦相似度选择连接边。这一范式存在两个深层缺陷：

1. **忽略全局结构**：图像集合的整体拓扑关系未被利用，导致关键连接缺失或形成弱连接拓扑，尤其在视觉歧义场景（如重复纹理、对称结构）下更为严重。
2. **错误不可恢复**：初始阶段丢弃的边在后续增量重建中无法被重新引入，早期决策错误会持续传播并放大。

本文的核心判断是：位姿图初始化不应是孤立的局部匹配问题，而应是一个**全局感知的边优先级排序与选择问题**。

### 核心方法定位

本文提出 **Global Edge Prioritization**，将位姿图初始化重构为两个协同步骤：

- **全局边排序**：在图神经网络（GNN）上学习预测每条候选边的全局匹配可靠性，训练信号来自SfM几何验证结果（RANSAC内点数与3D点重叠度），而非传统的二值检索标签。
- **全局边选择**：基于预测排序，通过**多最小生成树（multi-MST）迭代构造**与**连通性感知的分数调制**，生成紧凑、低直径且冗余充分的初始位姿图。

该方法在几何验证之前即完成全局推理，使下游增量SfM获得更优的初始化拓扑。

### 主要结果概要

在三个标准基准上，Global Edge Prioritization 一致且显著地超越现有SOTA方法：

- **IMC23-PhotoTourism**：在k=5棵MST配置下，COLMAP相对位姿AUC@5°达到 **73.1**，较MegaLoc（**66.5**）提升 **+6.6** 个百分点。
- **VisymScenes**（高歧义场景）：在全部调制组件启用时，k=5下AUC@5°达到 **75.6**，且重建正确相机比例最高，证明全局边排序对视觉歧义具有强鲁棒性。
- **MegaDepth**：在所有MST数量k下均保持最优，尤其在稀疏区间（k=1, k=2）优势最大。

消融实验进一步揭示：**移除GNN**导致k=1时AUC@5°从61.2骤降至55.4，验证了全局推理的不可替代性；**连通性感知的分数调制**在稀疏区间（k=2–3）持续提升精度，且仅当top-5候选边更新与距离归一化共同作用时达到最佳效果。

### 方法谱系与知识库定位

本文处于**图像检索驱动的SfM位姿图初始化**与**图学习**的交叉点。与现有工作的关系如下：

- 相对于**MegaLoc**（Berton et al., CVPRW 2025）等检索式方法：本文不改变图像描述子的提取方式，而是在描述子之上引入GNN全局重排序，将“检索”升级为“排序”。
- 相对于**Doppelganger++**（Xiangli et al., CVPR 2025）等后验证方法：本文在几何验证之前完成全局推理，与后处理方法互补而非替代。
- 相对于传统kNN构图：本文以多MST替代kNN选择，从根本上改变了边选择策略，使位姿图在连通性、直径和冗余度三个维度上更优。
- 训练范式上，本文采用**自监督几何信号**（RANSAC内点+3D点重叠）作为排序监督，避免了人工标注依赖，属于自监督排序学习在SfM中的新应用。

**代码与模型已开源**：`https://github.com/weitong8591/global_edge_prior`。

> ⚠️ 论文未标注具体发表年份与会议，部分基线方法的引用元数据需手动核实。

### 位姿图初始化在增量SfM中的关键地位

增量式运动恢复结构（Incremental SfM）是三维重建的核心流程，其重建质量高度依赖于初始位姿图（pose graph）的选取。位姿图以图像为节点、以图像对之间的可验证连接为边，决定了后续的相机注册顺序和场景几何估计。一个理想的初始位姿图应当满足两个条件：**全局连通**（避免场景碎片化）和**边高度可靠**（避免错误注册导致漂移）。然而，在实际应用中，这两个目标往往相互冲突——追求连通性可能引入弱连接或错误边，而过分保守地筛选可靠边又可能导致图不连通，使部分图像无法注册。

### 现有方法的瓶颈：局部近邻检索忽略全局结构

当前主流的位姿图初始化方法遵循一个统一的范式：首先用图像检索模型为每张图像独立检索其 k 个最近邻，然后将所有检索到的边取并集构成初始位姿图。这一范式存在两个根本性缺陷：

**第一，检索过程是局部且孤立的。** 每张图像的近邻选择仅基于该图像与候选图像之间的成对相似度（通常是图像描述子的余弦相似度），完全不考虑整个图像集合的全局结构。这意味着，即使某条边在局部看来相似度很高，它可能对整个图的连通性贡献甚微；反之，一条对全局连通性至关重要的边，可能因为局部相似度不够突出而被遗漏。

**第二，初始阶段丢失的边不可恢复。** 增量SfM在注册过程中不会重新考虑初始位姿图之外的候选边。一旦在初始化时遗漏了关键连接，后续重建将永久失去利用这些边的机会，导致重建不完整或精度下降。

这种“局部检索—全局并集”的策略在稀疏连接或视觉歧义场景下尤为脆弱。当图像集合包含重复结构、极端视角变化或弱纹理区域时，局部相似度排名难以区分正确匹配与错误匹配，导致初始位姿图中混入噪声边或缺失关键边。

### 本文动机：将全局推理引入边优先级排序

上述分析揭示了一个清晰的因果机制：**位姿图初始化的核心矛盾不在于检索模型的表达能力不足，而在于边选择过程缺乏对全局图结构的感知。** 即使使用最先进的图像检索模型（如 **MegaLoc**，Berton et al., CVPRW 2025），只要边选择策略仍然是逐图像独立的 kNN，就无法避免弱连接拓扑和关键边遗漏的问题。

本文的核心动机由此确立：**在几何验证之前，利用全局信息对所有候选边进行可靠性排序，并以此指导位姿图的构造。** 具体而言，我们提出训练一个图神经网络（GNN），以SfM几何信号（RANSAC内点数和3D点重叠度）作为自监督标签，学习预测每条边在全局结构中的匹配性分数。进一步，我们用这些全局感知的边排名来指导多个最小生成树（MST）的迭代构造，并通过连通性感知的分数调制强化弱连接区域，最终生成一个紧凑、连通且冗余的初始位姿图。

这一思路的关键洞察在于：**边的“可靠性”不应仅由两幅图像的视觉相似度定义，还应包含该边对全局重建的贡献度。** 两幅图像可能视觉上高度相似，但如果它们共享的3D点极少，则对多视图几何的贡献有限；反之，一条视觉相似度中等但能连接两个稀疏子图的边，对重建完整性的价值可能更高。通过从SfM重建结果中提取RANSAC内点数和3D点重叠度作为监督信号，我们的GNN能够隐式地学习这种全局价值判断。

## 核心方法与创新机理

本文的核心创新在于将**全局结构感知**系统性地引入位姿图初始化的两个关键阶段——边排序与图选择，从而突破了现有方法仅依赖成对局部相似性的根本局限。

### 1. 从成对局部排序到全局边可靠性预测

现有SfM位姿图初始化方法（如**MegaLoc**，Berton et al., CVPRW 2025）仅基于每张图像独立的k近邻检索来构建初始图，完全忽略了图像集合的全局结构。这一设计存在两个致命缺陷：(1) 可能遗漏对全局连通性至关重要的“桥梁边”；(2) 形成弱连接的拓扑结构，且初始阶段丢失的边在后期增量重建中不可恢复。

本文的**核心改变槽位**是将边排序的信号源从“成对余弦相似度”替换为“GNN预测的全局边可靠性分数”。具体而言，方法在图像描述子之上构建完全图，通过两层边-节点消息传递的GNN进行全局推理，最终由MLP输出每条边的匹配性排名。这一设计使得边的重要性评估不再孤立，而是综合考虑了该边在整个图像集合中的结构角色。

**决定性证据**：Table 2显示，移除GNN后，在k=1（最稀疏设定）时AUC@5°从61.2骤降至55.4，降幅达5.8个百分点，直接验证了全局推理的不可替代性。

### 2. 从单图kNN选择到多MST全局优化选择

传统kNN选择策略的另一个缺陷在于：每张图像独立选择固定数量的近邻，无法保证全局图的连通性和低直径。本文提出**多最小生成树（multi-MST）选择策略**：利用GNN预测的边排名作为权重，迭代构建k棵最小生成树，取并集作为初始位姿图。这一策略天然保证了图的全局连通性，且通过多树叠加引入冗余边以提升鲁棒性。

### 3. 连通性感知的距离调制

在多MST迭代构建过程中，本文进一步引入**连通性感知的分数调制机制**，将前一轮图的归一化最短路径距离与预测排名进行加权融合：

$$s_{ij}^{(m)} = (1-\lambda) \hat{r}_{ij} + \lambda \bar{d}^{(m-1)}(i,j)$$

这一设计的直觉是：在已构建的图中距离较远的节点对，其连接边对降低图直径具有更高价值，应在后续MST中获得优先级提升。调制仅在每张图像的top-5候选边上更新，且丢弃预测排名低于0.9的低质量边。

**决定性证据**：Table 1显示，在高度歧义的VisymScenes数据集上，调制在稀疏区间（k=2-3）持续提升精度；Table 3进一步表明，仅当调制、top-5更新和距离归一化三者同时启用时，k=5下AUC@5°达到75.6，超过专用的**Doppelganger++**后处理（Xiangli et al., CVPR 2025）。

### 4. 自监督几何信号驱动的排序学习

与传统依赖分类/二值检索标签的监督方式不同，本文从SfM几何验证结果中自动提取**连续排序信号**：结合RANSAC内点数（反映两视图可验证性）和3D点重叠度（反映多视图一致性贡献），归一化后取平均作为真实边排名：

$$\tilde{r}_{ij} = \frac{1}{2}(\mathrm{norm}(u_{ij}) + \mathrm{norm}(v_{ij}))$$

模型通过可微的NDCG-Loss2++进行LambdaRank优化，直接学习排序而非回归。Table 2最后三行的Oracle实验表明，组合两种几何信号的Oracle排名优于单一信号，验证了该监督设计的合理性。

**创新总结**：三个changed slots形成闭环——GNN提供全局感知的边排名，多MST将排名转化为连通且冗余的图结构，距离调制则在前两者基础上进一步降低图直径。这一“全局推理+全局选择”的范式在IMC23-PhotoTourism上相较MegaLoc提升6.6个AUC@5°百分点（k=5），且在稀疏设定下优势更为显著。

本文提出 **Global Edge Prioritization**，将位姿图初始化从“逐图像独立检索”重构为“全局排序 + 结构化选择”两阶段流水线。整体流程如图 2 所示，包含四个核心模块：

1. **图像编码器**：对输入图像集 $\\{I_i\\}$，采用以 DINOv2 为骨干、SALAD（Izquierdo et al., CVPR 2024）聚合的方式提取全局描述子 $d_i \\in \\mathbb{R}^d$。编码器经过微调，使描述子空间对后续图推理友好。

2. **全连接图构建**：在图像描述子 $\\{d_i\\}$ 之上构建完全图，节点为图像，边特征 $e_{ij}^0$ 由描述子拼接及其余弦相似度经线性层与 ReLU 初始化：
   $$e_{ij}^{0} = \\mathrm{ReLU}\\big(f_l[d_i, d_j, \\langle d_i, d_j\\rangle]\\big)$$
   这一步将所有候选匹配对显式地暴露给后续全局推理。

3. **GNN-MLP 全局边排序**：对完全图执行两轮边-节点消息传递，边特征 $e_{ij}^t$ 根据当前节点嵌入 $d_i^t, d_j^t$ 更新：
   $$e_{ij}^{t} = f_{\\mathrm{edge}}\\big([e_{ij}^{t-1}, d_i^{t}, d_j^{t}]\\big)$$
   最终由 MLP 预测每条边的全局匹配分数 $\\hat{r}_{ij}$。训练时，采用 SfM 几何信号——RANSAC 内点数 $u_{ij}$ 和 3D 点重叠度 $v_{ij}$ 的归一化均值 $\\tilde{r}_{ij} = \\frac{1}{2}(\\mathrm{norm}(u_{ij}) + \\mathrm{norm}(v_{ij}))$——作为真实排序监督，并以可微的 NDCG-Loss2++ 优化排序质量。这一设计使模型在几何验证之前就能感知全局结构关系。

4. **多 MST 选择与分数调制**：推理阶段，利用预测的全局边排名 $\\hat{r}_{ij}$ 迭代构造 $k$ 棵最小生成树（MST），边权重取 $w_{ij} = 1 - \\hat{r}_{ij}$。每次 MST 构造后，仅保留每张图像的 top-5 候选边并丢弃排名低于 0.9 的边，同时对已选边进行掩码（赋 $-\\infty$ 分数）。为强化弱连通区域并降低图直径，引入连通性感知的距离调制分数：
   $$s_{ij}^{(m)} = (1-\\lambda) \\hat{r}_{ij} + \\lambda \\bar{d}^{(m-1)}(i,j)$$
   其中 $\\bar{d}^{(m-1)}(i,j)$ 为前 $m-1$ 棵 MST 并图中节点 $i,j$ 间的最短路径距离经归一化后的值。首棵 MST 时图为空，$\\bar{d}^{(0)}(i,j)=1$，退化为均匀缩放。$k$ 棵 MST 的并集构成初始位姿图 $\\mathcal{E}_0 = \\mathrm{Select}(r, \\mathrm{budget})$。

5. **增量 SfM**：最终由 COLMAP 在选定的位姿图上执行增量式稀疏重建。

**关键设计决策**：将“排序”与“选择”解耦——GNN 负责在完全图上进行全局推理以产生可靠的边优先级，多 MST 选择则保证图的全局连通性、冗余度和低直径。这一分工使得方法在稀疏连接（$k=1$ 或 $k=2$）下尤其受益：消融实验表明，移除 GNN 后 $k=1$ 时 AUC@5° 从 61.2 骤降至 55.4（Table 2），验证了全局推理不可替代；而连通性感知调制在 VisymScenes 上持续提升精度，尤其在 $k=2$–$3$ 稀疏区间效果显著（Table 1）。

![[assets/figures/papers/paper_list_l2103_https_arxiv_org_abs_2602_21963/figures/002_Figure_2.jpg]]
*Figure 2: Overall pipeline. Input images are first encoded using a fine-tuned image encoder (DINOv2 backbone with SALAD aggregation). A complete graph is then constructed over image embeddings and processed by our GNN–MLP model to predict global edge ranks. During training, these predictions are supervised using geometry-derived ranking signals via a differentiable ranking loss. At inference, the predicted ranks guide the construction of multiple minimum spanning trees, whose union forms the initial pose graph. Incremental SfM is finally applied on this graph to recover the sparse 3D reconstruction*

![[assets/figures/papers/paper_list_l2103_https_arxiv_org_abs_2602_21963/figures/001_Figure_1.jpg]]
*Figure 1: Given a set of input image pairs (left), our method ranks all candidate edges by global matchability (middle) and constructs a compact, well-connected pose graph via multi-MST selection (right). The resulting initialization enables accurate and stable 3D reconstruction, even under sparse or ambiguous settings*

### 3.1 问题形式化与初始边选择

给定图像集合 $\{I_i\}_{i=1}^N$，SfM位姿图初始化的目标是选择一个边子集 $\mathcal{E}_0$，使得在该图上运行的增量式SfM能够恢复尽可能多的正确相机位姿。形式上，若所有候选边对已按某种匹配性度量 $r$ 排序，则初始边集为：

$$\mathcal{E}_0 = \mathrm{Select}(r, \mathrm{budget}) \tag{1}$$

其中 $\mathrm{budget}$ 控制所选边的数量。传统方法直接使用图像描述子的余弦相似度作为 $r$，而本文的核心创新在于用GNN学习一个全局感知的边可靠性排序来替代这一局部度量。

### 3.2 图像编码与完全图构建

每张图像 $I_i$ 首先通过微调的图像编码器编码为全局描述子：

$$d_i = f_{\mathrm{en}}(I_i) \in \mathbb{R}^d$$

编码器采用**DINOv2骨干网络配合SALAD聚合**（Izquierdo et al., CVPR 2024），在标准图像检索预训练基础上针对SfM几何信号进行微调。随后，在所有图像嵌入 $\{d_i\}$ 上构建一个完全图，为GNN的全局推理提供拓扑基础。

### 3.3 GNN边排序预测器

GNN的核心任务是从完全图中预测每条候选边的全局匹配可靠性。模型采用两轮边-节点消息传递：

**边特征初始化**：每条边 $(i,j)$ 的初始特征由对应图像描述子及其余弦相似度拼接后经线性层和ReLU激活得到：

$$e_{ij}^{0} = \mathrm{ReLU}\big(f_l[d_i, d_j, \langle d_i, d_j\rangle]\big) \tag{2}$$

**消息传递与更新**：在第 $t$ 轮迭代中，节点嵌入首先由邻接边特征聚合更新，随后边特征基于更新的节点嵌入进行修正：

$$e_{ij}^{t} = f_{\mathrm{edge}}\big([e_{ij}^{t-1}, d_i^{t}, d_j^{t}]\big) \tag{3}$$

经过两轮迭代后，最终的边特征通过MLP映射为标量排序分数 $\hat{r}_{ij}$。这一设计的关键在于：通过节点嵌入的迭代更新，每条边的预测能够间接感知全局图结构，而非仅依赖局部图像对信息。

### 3.4 几何驱动的排序监督信号

训练GNN需要真实排序标签。本文从SfM重建结果中提取两种连续几何信号，而非使用简单的二值匹配标签：

**RANSAC内点数**：反映两视图间的直接可验证性：

$$u_{ij} = \# \{ \text{RANSAC inliers for } (i,j) \} \tag{4}$$

**3D点重叠度**：反映两视图在多视图重建中的共同贡献：

$$v_{ij} = \# \{ \text{3D points visible in both } I_i \text{ and } I_j \} \tag{5}$$

两者经归一化后取平均，构成综合真实排序分数：

$$\tilde{r}_{ij} = \frac{1}{2}(\mathrm{norm}(u_{ij}) + \mathrm{norm}(v_{ij})) \tag{6}$$

### 3.5 可微排序损失

模型采用**NDCG-Loss2++**（基于LambdaRank算法）作为训练损失，将排序问题转化为可微优化。其核心评价指标为折损累积增益：

$$\mathrm{DCG} = \sum_{i=1}^{M} \frac{2^{v_i} - 1}{\log_2(\hat{r}_i + 1)} \tag{7}$$

其中 $v_i$ 为真实相关度（即 $\tilde{r}_{ij}$），$\hat{r}_i$ 为预测排名位置。该损失函数奖励将高相关度边排在列表前端的行为。

### 3.6 多MST选择与连通性感知调制

推理阶段，利用预测的全局边排序 $\hat{r}_{ij}$ 构造位姿图。每条边的MST权重定义为：

$$w_{ij} = 1 - \hat{r}_{ij} \tag{8}$$

即高置信度边获得低权重，优先被选入生成树。为增强图的冗余性和连通性，本文迭代构造 $k$ 棵最小生成树，并在每轮迭代间引入**距离调制分数**：

$$s_{ij}^{(m)} = (1-\lambda) \hat{r}_{ij} + \lambda \bar{d}^{(m-1)}(i,j) \tag{9}$$

其中 $\bar{d}^{(m-1)}(i,j)$ 是前 $m-1$ 棵MST并集中节点 $i$ 与 $j$ 的归一化最短路径距离。该调制机制使已连通区域中的边分数降低，而弱连通或孤立区域中的边分数被提升，从而在后续MST中优先强化薄弱连接。

**调制执行细节**：
- 首轮（$m=1$）时图为空，设定 $\bar{d}^{(0)}(i,j)=1$，调制退化为均匀缩放
- 每棵MST构造后，仅更新每张图像的**top-5候选边**分数，并丢弃预测排名低于0.9的边
- 已选入先前MST的边通过赋 $-\infty$ 分数进行掩码，避免重复选择

## 实验与关键发现

### 主结果

本文在三个具有不同挑战维度的公开基准上评估了所提出的全局边优先级排序方法：**IMC23-PhotoTourism**（大规模地标场景）、**MegaDepth**（自然场景）和**VisymScenes**（高视觉歧义场景）。所有方法均采用相同的COLMAP增量重建流程，仅初始位姿图的构造方式不同，从而保证对比的公平性。

在**IMC23-PhotoTourism**上，当使用k=5棵MST时，本文方法在COLMAP相对位姿精度上达到**AUC@5° = 73.1**，显著优于当前最强的图像检索方法**MegaLoc**（Berton et al., CVPRW 2025）的66.5（采用kNN选择），提升**+6.6个百分点**。性能优势在稀疏图区间尤为突出：Figure 3显示，在k=1和k=2时，本文方法与基线的差距最大，验证了全局边优先级排序在边预算极度受限时的关键价值。

在**MegaDepth**上，本文方法的AUC@5°曲线在所有MST数量k下均保持最优（Figure 3右上），且注册相机比例同样领先。

在**VisymScenes**上，该数据集包含大量视觉上高度相似但几何上不同的场景，对位姿图初始化构成严重歧义挑战。本文方法在启用全部调制组件后，k=5时达到**AUC@5° = 75.6**（Table 3末行），重建正确相机的比例最高（Figure 3右下），甚至超过了专用的后验证视觉消歧过滤器**Doppelganger++**（Xiangli et al., CVPR 2025），证明全局边优先级排序对视觉歧义具有强鲁棒性。

值得注意的是，尽管本文方法在推理时增加了GNN预测步骤，但整体重建时间反而更短（COLMAP耗时：本文2.1k vs MegaLoc 2.3k，见附录D），因为更优的图选择减少了后续几何验证和增量重建的无效计算。

### 消融实验

消融实验围绕三个核心组件展开：GNN全局推理模块、连通性感知的分数调制策略，以及几何监督信号的选择。

**GNN全局推理的必要性。** 在PhotoTourism上，移除GNN后仅保留图像编码器输出的余弦相似度进行排序，k=1时AUC@5°从**61.2骤降至55.4**（Table 2），降幅达5.8个百分点。这一结果表明，仅靠图像对的局部相似性无法捕捉全局结构关系，GNN的边-节点消息传递是预测全局一致边可靠性的不可替代组件。

**连通性感知分数调制的效果。** 在VisymScenes上，Table 1显示调制策略对MegaLoc和本文方法均带来持续提升，尤其在稀疏区间（k=2–3）效果显著。Table 3进一步分解了调制的三个子组件：仅当调制开关、top-5候选边更新和距离归一化三者同时启用时，才能达到最佳精度。若禁用距离归一化或扩大候选边范围，性能均会下降，说明精确的弱连接区域强化机制对维持图连通性至关重要。

**几何监督信号的比较。** Table 2末三行报告了直接从几何信号导出的Oracle排名性能：RANSAC内点数（反映两视图可验证性）、3D点重叠度（反映多视图一致性贡献）以及两者的组合。组合信号在所有k下均优于单一信号，验证了本文设计的复合监督目标 $\tilde{r}_{ij} = \frac{1}{2}(\text{norm}(u_{ij}) + \text{norm}(v_{ij}))$ 的合理性。

**边选择策略对比。** Figure 4直接比较了kNN与多MST两种边选择策略。MST-based选择在所有k下均显著优于kNN，且其性能曲线紧密跟随Oracle排名曲线，表明多MST构造能有效逼近全局最优边集。kNN在稀疏设置下容易产生碎片化的不连通分量，而多MST天然保证全局连通性，这是注册相机比例大幅领先的根本原因。

### 失败模式与局限

尽管方法在多数场景下表现优异，仍存在以下局限：

1. **低纹理/低分辨率场景。** 当输入图像分辨率极低或匹配特征极少（如小地标、重复纹理墙面）时，图像编码器难以提取判别性描述子，GNN的边排名预测质量随之下降，导致重建失败（见附录C failure cases）。
2. **极大规模图像集。** 对于超过500张图像的场景，全连通图的内存和计算开销过大，需借助METIS聚类进行图划分。这一额外步骤可能损失部分全局结构信息，影响最优性。
3. **推理延迟。** GNN推理耗时约0.08秒，虽远小于后续SfM流程，但相比简单余弦相似度（0.01秒）仍有数倍差距，在极端实时场景下可能成为瓶颈。

### 开放问题

* 多MST的数量k目前为固定超参数，如何根据场景规模、歧义程度和计算预算自适应确定k值？
* 距离调制参数λ的跨数据集泛化能力尚需进一步验证。
* 该全局边优先级框架能否扩展到动态视频序列或RGB-D、LiDAR等多模态位姿图初始化场景？

![[assets/figures/papers/paper_list_l2103_https_arxiv_org_abs_2602_21963/figures/003_Figure_3.jpg]]
*Figure 3: COLMAP reconstruction [42] performance using pose graphs constructed from multiple MSTs guided by baseline embedding similarities or our learned global edge ranks. Top row: Relative pose accuracy on IMC23-PhotoTourism [21] (AUC@2.5◦, left*

![[assets/figures/papers/paper_list_l2103_https_arxiv_org_abs_2602_21963/figures/004_Table_1.jpg]]
*Table 1: Ablation of connectivity-aware score modulation on VisymScenes [50]. We report AUC@5◦ for pose graphs built from MegaLoc similarities and from our predicted global edge ranks, with and without modulation, as well as with DoppelGanger++ filtering. Modulation consistently improves accuracy for both methods, especially in the sparse regime (k = 2–3). COLMAP mapping time at k = 5 is shown in minutes*

![[assets/figures/papers/paper_list_l2103_https_arxiv_org_abs_2602_21963/figures/006_Table_3.jpg]]
*Table 3: Ablation of the proposed connectivity-aware score modulation on VisymScenes. We evaluate three components: (i) whether modulation is applied, (ii) whether only the top-5 candidate edges per image are updated after each MST, and (iii) whether graph distances are normalized before modulation. Reported metrics are*

![[assets/figures/papers/paper_list_l2103_https_arxiv_org_abs_2602_21963/figures/007_Figure_4.jpg]]
*Figure 4: Edge selection strategies for pose graph initialization. We report COLMAP [42] relative pose*

## 定位与知识库关联

### 1. 问题定位：位姿图初始化的全局盲区

现有运动恢复结构（SfM）的位姿图初始化普遍遵循“检索-验证-重建”范式：先用图像检索获得每张图像的 k 近邻，再经几何验证保留内点数足够的边，最后增量重建。该范式的一个根本瓶颈在于，**近邻检索完全基于成对相似度，缺乏对图像集合全局结构的感知**。这导致两个后果：（1）可能遗漏那些外观差异大但在三维空间中强关联的关键连接；（2）形成的初始图可能包含弱连接区域甚至断裂成分，且初始阶段丢失的边在后期增量SfM中无法恢复，直接限制了重建精度与完整性。

本文提出的 **Global Edge Prioritization** 方法直接针对这一瓶颈，将位姿图初始化从“独立近邻选择”升级为“全局边优先级排序 + 连通性感知选择”。其核心因果旋钮在于：**在几何验证之前，利用图神经网络（GNN）学习全局边可靠性排名，再通过多最小生成树（MST）与连通性感知分数调制构造初始位姿图**。这一设计使得初始图不仅全局连通、冗余，而且图直径更短，从而在稀疏连接条件下显著提升重建鲁棒性和精度。

### 2. 与现有工作的关系

#### 2.1 图像检索基线与编码器

本文的图像编码器采用微调的 **DINOv2** 骨干网络配合 **SALAD** 聚合（Izquierdo et al., CVPR 2024），生成全局图像描述子。在实验中，主要的检索基线包括：

- **MegaLoc**（Berton et al., CVPRW 2025）：当前位姿图初始化的SOTA图像检索方法，使用成对余弦相似度进行 kNN 选择。本文方法在 IMC23-PhotoTourism 上 k=5 时 AUC@5° 达到 73.1，较 MegaLoc 的 66.5 提升 +6.6（附录A）。
- **SALAD (with DINOv2)** 和 **pretrained DINOv2**：作为编码器基线，本文在保持相同编码器条件下，通过 GNN 全局排序和多MST选择获得一致提升。

关键区别在于：这些基线在获得图像描述子后，直接使用成对相似度进行边选择；本文则在描述子之上构建完全图，通过 GNN 进行全局推理，将边选择问题从“独立评分”转化为“全局排序”。

#### 2.2 视觉歧义处理

在高度歧义的场景（如重复纹理、对称结构）中，成对匹配常常产生大量误匹配。**Doppelganger++**（Xiangli et al., CVPR 2025）作为后验证阶段的视觉消歧滤波器，专门处理此类问题。本文方法与 Doppelganger++ 的关系是**互补而非竞争**：本文工作在几何验证之前的边选择阶段引入全局推理，而 Doppelganger++ 在验证之后进行滤波。在 VisymScenes 上的实验表明，本文方法（含调制）在 k=5 时 AUC@5° 达到 75.6，即使不依赖 Doppelganger++ 后处理也展现出对视觉歧义的强鲁棒性（Table 3）。

#### 2.3 图学习与排序监督

在方法层面，本文将边排序建模为排序学习问题，采用 **NDCG-Loss2++**（基于 LambdaRank 算法）优化 NDCG 的可微近似。这一选择的关键动机在于：SfM 几何信号（RANSAC 内点数和 3D 点重叠度）天然是连续值，更适合排序损失而非分类或回归损失。

监督信号的构建是本文的另一创新点。传统检索方法使用离散的二值标签（匹配/非匹配），本文则从 SfM 重建结果中提取两个互补的连续信号：

- **RANSAC 内点数** $u_{ij}$：反映两视图的可验证性（公式1）
- **3D 点重叠度** $v_{ij}$：反映两视图在多视图一致性中的贡献（公式2）

两者归一化后取平均得到真实排序信号 $\tilde{r}_{ij} = \frac{1}{2}(\mathrm{norm}(u_{ij}) + \mathrm{norm}(v_{ij}))$（公式3）。消融实验（Table 2）表明，组合信号优于任一单独信号，验证了两种几何线索的互补性。

#### 2.4 图构造策略

传统的 kNN 图构造是局部贪心策略，容易产生不连通分量。本文提出的**多MST选择**策略从根本上改变了图构造逻辑：通过迭代构造 k 个最小生成树并取并集，保证全局连通性的同时引入冗余边。Figure 4 的对比清晰展示了 MST 策略相对于 kNN 的优势：在 PhotoTourism 和 MegaDepth 上，MST 选择曲线紧密跟随 Oracle 排名曲线，而 kNN 在稀疏区间（k=1-2）表现明显更差。

连通性感知的分数调制进一步强化了这一策略。调制公式为：

$$s_{ij}^{(m)} = (1-\lambda) \hat{r}_{ij} + \lambda \bar{d}^{(m-1)}(i,j)$$

其中 $\bar{d}^{(m-1)}(i,j)$ 是前 m-1 个 MST 并集中节点 i 和 j 的最短路径距离的归一化值。这一设计的直觉是：**在已选图中距离较远的节点对，即使预测排名稍低，也应被优先考虑以降低图直径**。Table 1 显示，调制在稀疏区间（k=2-3）的提升尤为显著，且对 MegaLoc 基线和本文方法均有效，证明其作为通用图构造策略的价值。

### 3. 适用边界与局限

#### 3.1 已知局限

1. **低分辨率/少特征场景**：在匹配特征极少（如小地标、低纹理区域）的情况下，GNN 预测的边排名可能不可靠，导致重建失败（见附录C failure cases）。
2. **超大规模图像集**：对于超过 500 张图像的场景，需借助 METIS 聚类进行图划分，引入了额外的预处理步骤，可能影响全局最优性。
3. **推理延迟**：GNN 推理本身（0.08s）比简单余弦相似度（0.01s）慢约 8 倍，在极端实时场景下可能成为瓶颈。但需注意，由于更优的图选择，整体 COLMAP 重建时间反而更短（Ours 2.1k vs MegaLoc 2.3k，附录D）。

#### 3.2 适用条件

- **稀疏连接场景**是该方法的强项：当位姿图必须保持非常稀疏（k=1-3）时，全局边优先级排序的优势最大。
- **视觉歧义场景**：在重复纹理、对称结构等导致成对匹配不可靠的数据集上，全局推理带来的鲁棒性增益尤为突出（VisymScenes 上 k=5 时超过 75% 的相机被正确重建）。
- **需要高连通性初始化**的下游任务：如需要稳定初始化的增量SfM、需要完整场景覆盖的稠密重建等。

### 4. 开放问题

1. **自适应 MST 数量**：多 MST 的数量 k 如何根据场景规模、歧义程度和计算预算自适应确定？当前 k 是固定超参数，但在实际应用中，不同场景的最优 k 可能差异显著。
2. **调制参数 λ 的泛化性**：距离调制参数 λ 是否需要针对不同数据集进行调整？论文中 λ 的取值和敏感性分析尚不充分，其跨数据集的泛化能力需要进一步验证。
3. **跨模态扩展**：该全局边优先级框架能否扩展到动态视频序列（需考虑时序一致性）或多模态数据（如 RGB-D、LiDAR 点云）的位姿图初始化？GNN 的边特征设计需要相应调整以融合多模态信息。
4. **与学习的局部特征结合**：当前方法依赖全局图像描述子，若与学习的局部特征（如 SuperPoint、LoFTR）结合，能否进一步提升在极端视角变化下的边排名质量？
5. **端到端训练**：当前 GNN 训练与下游 SfM 是分离的，是否可能将重建质量（如重投影误差、注册相机数）作为训练信号，实现端到端的位姿图初始化学习？

## 原文 PDF

![[paperPDFs/CVPR_2026/Global_Aware_Edge_Prioritization_for_Pose_Graph_Initialization.pdf]]
