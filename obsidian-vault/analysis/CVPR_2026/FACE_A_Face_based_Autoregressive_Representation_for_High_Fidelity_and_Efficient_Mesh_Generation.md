---
title: "FACE: A Face-based Autoregressive Representation for High-Fidelity and Efficient Mesh Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FACE_A_Face_based_Autoregressive_Representation_for_High_Fidelity_and_Efficient_Mesh_Generation.pdf
project_link: null
code_link: null
aliases:
- FACE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: “一面一令牌”（one-face-one-token）策略，将每个三角形面视为单个统一令牌，从而将自注意力的序列长度缩短为原来的1/9。
primary_logic: 在面语义级别而非顶点级别进行生成，从根本上降低序列长度，避免复杂的无损压缩方案，同时利用面嵌入层和CausalMLP头实现端到端的高保真网格重建。
claims:
- 序列长度减少为原来的1/9，压缩率达到0.11，仅为先前最佳方法的一半。
- 在Objaverse、Toys4K和Famous数据集上均取得最低的Hausdorff和Chamfer距离，重建质量达到SOTA。
- 在Toys4K上，FACE的Hausdorff距离比最佳基线（EdgeRunner）低26%以上。
- 消融实验证实“一面一令牌”+CausalMLP解码策略在重建精度上大幅领先其他替代方案。
---

# FACE: A Face-based Autoregressive Representation for High-Fidelity and Efficient Mesh Generation

> [!tip] 核心洞察
> 在面语义级别而非顶点级别进行生成，从根本上降低序列长度，避免复杂的无损压缩方案，同时利用面嵌入层和CausalMLP头实现端到端的高保真网格重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | FACE：基于面的自回归表示用于高保真高效网格生成 |
| 英文题名 | FACE: A Face-based Autoregressive Representation for High-Fidelity and Efficient Mesh Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.01515) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | FACE |
| Dataset | Objaverse, Toys4K, Famous, Image-to-mesh generation |

> [!tip] 效果简介
> - Objaverse (reconstruction) 上，Hausdorff Distance (HD) 0.090 vs Best baseline (EdgeRunner) around 0.111 (~ -18.9%)。
> - Toys4K (reconstruction) 上，Hausdorff Distance (HD) 0.067 vs 0.091 (EdgeRunner) (-26.4%)。
> - Famous (reconstruction) 上，Hausdorff Distance (HD) 0.077 vs Best baseline (优于所有基线)。

## 概述

### 1. 问题背景

三维网格是计算机图形学与视觉的基础表示形式，但高保真网格的生成长期受困于自回归Transformer的 $O(N^2)$ 计算瓶颈。现有自回归方法——如 **MeshGPT**（Siddiqui et al., CVPR 2024）、**MeshXL**（Chen et al., NeurIPS 2025）、**EdgeRunner**（Tang et al., arXiv 2024）——将网格展平为顶点坐标序列，每个三角形面需9个独立令牌，导致序列长度随面数线性膨胀，自注意力计算代价急剧攀升。尽管 **BPT**（Weng et al., arXiv 2024）等压缩令牌化方案试图缓解，其压缩比仍停留在0.22，高分辨率网格的效率鸿沟远未弥合。

### 2. 核心方法

**FACE** 提出“一面一令牌”（one-face-one-token）策略，从根本上重构网格的自回归生成范式。其关键设计在于：

- **令牌化层级上移**：将每个三角形面——而非其9个顶点坐标——视为单一统一令牌，通过面嵌入层（$t_{i-1} = \text{MLP}_\text{embed}(f_{i-1})$）将9维坐标向量投影为单个 $d_\text{model}$ 维令牌，序列长度骤减为原来的1/9。
- **两级自回归解码**：面级Transformer解码器（因果自注意力+交叉注意力）逐面生成全局连贯的网格拓扑，面内CausalMLP头再以轻量自回归方式解码9个量化坐标令牌，实现端到端高保真重建。
- **VecSet条件编码**：输入点云经FPS采样与交叉注意力压缩为紧凑潜在向量集 $\mathbf{C}$，为解码器提供全局形状条件（$\mathbf{H}_{l+1} = \text{CrossAttn}(\mathbf{Q}=\mathbf{H}_l', \mathbf{K}=\mathbf{C}, \mathbf{V}=\mathbf{C})$）。

### 3. 核心贡献与主要结果

FACE 在压缩效率与重建质量两个维度同时刷新最优水平：

- **压缩效率**：压缩比达到 **0.11**，仅为先前最佳方法（BPT, 0.22）的一半（Table 1），将自注意力序列长度降低一个数量级。
- **重建质量**：在 **Objaverse**、**Toys4K** 和 **Famous** 三个标准基准上均取得最低的 Hausdorff 距离（HD）和 Chamfer 距离（CD）。其中 Toys4K 上 HD 为 **0.067**，比最佳基线 EdgeRunner（0.091）低 **26%以上**（Table 2, Section 4.3）。
- **生成能力**：在图像到网格生成任务中，FACE 产生细节更丰富、与输入图像对齐更好、拓扑连通性更优的网格（Figure 5）。

消融实验进一步验证了设计的可靠性：ZYX 空间排序策略在面排序中性能最佳（HD 0.103，Table 3）；降采样点云查询优于可学习查询（Table 4）；CausalMLP 解码策略在坐标级重建上大幅领先并行预测和注意力解码（Table 5）。

### 4. 方法谱系与知识库定位

FACE 属于**自回归网格生成**这一新兴方向，与以下工作构成直接对比：

| 方法 | 核心策略 | 令牌粒度 | 压缩比 |
|------|---------|---------|--------|
| **MeshGPT** (Siddiqui et al., CVPR 2024) | 顶点序列自回归 | 每坐标一令牌 | ~1.0 |
| **MeshXL** (Chen et al., NeurIPS 2025) | 神经坐标场 | 每坐标一令牌 | ~1.0 |
| **EdgeRunner** (Tang et al., arXiv 2024) | 自回归自编码器 | 每面多令牌 | — |
| **BPT** (Weng et al., arXiv 2024) | 压缩令牌化 | 每面约2令牌 | 0.22 |
| **FACE** (本文) | **一面一令牌** | **每面1令牌** | **0.11** |

FACE 的核心洞见在于：**在面语义级别而非顶点级别进行生成**，从根本上降低序列长度，避免复杂的无损压缩方案。这一设计使其在效率上形成代际优势，同时通过面嵌入层与CausalMLP头保证了端到端的重建精度。

### 5. 局限与开放问题

- **离散表示的上限**：量化坐标的离散表示并非无限，仍然限制了可实现的细节水平上限。
- **极细结构的挑战**：依赖输入点云意味着极其精细或薄的结构（如自行车辐条）可能无法充分采样，导致在具有挑战性的区域重建不完整。
- **分辨率扩展性**：分辨率能否在不引入量化误差的情况下扩展到1024以上，仍是待探索的开放问题。

## 背景与动机

### 3D网格生成的核心挑战

3D网格是计算机图形学、游戏、影视和仿真领域的基本几何表示形式。与点云或体素相比，网格以紧凑的顶点-面拓扑结构精确描述物体表面，天然支持渲染、物理模拟和下游编辑。然而，**高质量网格的自动生成**仍然是一个公认的难题：网格不仅需要精确的几何形状，还要求拓扑正确、面片分布均匀、边缘流形连续。

近年来，自回归生成模型在语言、图像和音频领域取得了巨大成功，研究者自然将其引入3D网格生成。这类方法将网格序列化为令牌流，利用Transformer的自回归机制逐令牌预测几何结构。然而，这一范式面临一个根本性的效率瓶颈。

### 现有自回归方法的序列长度瓶颈

传统自回归网格生成方法的核心策略是**逐坐标令牌化**：将网格的每个三角形面的三个顶点坐标展平为独立的令牌。对于一个包含 $N$ 个三角形的网格，这意味着需要 $9N$ 个令牌（每个面3个顶点，每个顶点3个坐标分量）。由此带来的序列长度 $S = 9N$ 直接触发了Transformer自注意力的 $O(S^2)$ 计算复杂度瓶颈。

具体而言，当网格分辨率提升至数千面时，序列长度迅速膨胀至数万令牌，自注意力计算量呈平方级增长，严重限制了高分辨率网格的生成效率。现有工作尝试通过压缩编码缓解此问题，例如：

- **MeshGPT** (Siddiqui et al., CVPR 2024) 使用VQ-VAE对网格进行压缩，但仍保留了较长的序列表示。
- **BPT** (Weng et al., arXiv 2024) 提出了压缩令牌化方案，但压缩率仍然有限。
- **TreeMeshGPT** (Lionar et al., CVPR 2025) 采用树状序列化策略，试图从结构上优化序列组织。

这些方法虽然在一定程度上缓解了序列长度问题，但本质上仍停留在“坐标级令牌化”的范式内，**压缩效率与重建精度之间存在难以调和的权衡**——过度压缩会损害几何细节，而保留精度则意味着序列长度居高不下。

### 本文动机：“一面一令牌”策略

本文的核心洞察在于**从令牌化的粒度层面重新思考网格表示**。作者观察到，三角形面——而非顶点坐标——才是网格的语义基本单元。一个三角形面完整地定义了局部表面片元，其三个顶点坐标在几何上高度耦合，将它们拆分为独立令牌不仅增加了序列冗余，还破坏了面内坐标之间的结构关联。

基于这一洞察，FACE提出了**“一面一令牌”（one-face-one-token）策略**：将每个三角形面视为单个统一令牌，通过面嵌入层（Face Embedding）将9维坐标向量投影为单一潜在表示，从而将自注意力的序列长度**缩短为原来的1/9**。这一设计直接攻击了 $O(S^2)$ 计算瓶颈的根源，实现了**0.11的压缩率**，仅为先前最佳方法的一半（Table 1）。

同时，FACE在解码端引入**CausalMLP头**作为面内坐标级自回归解码器，在保持“一面一令牌”的宏观效率的同时，精确恢复每个面内的9个量化坐标，实现了效率与精度的统一。

## 核心创新

### 瓶颈诊断：序列长度灾难

现有自回归网格生成方法——包括 **MeshGPT** (Siddiqui et al., CVPR 2024)、**MeshXL** (Chen et al., NeurIPS 2025)、**MeshAnything** 系列 (Chen et al., arXiv 2024) 以及 **EdgeRunner** (Tang et al., arXiv 2024)——均将网格展平为长的顶点坐标序列。一个三角形面由3个顶点、每个顶点3个坐标组成，共需9个令牌来表示。这种逐坐标的令牌化策略导致Transformer自注意力的复杂度随面数 $N$ 呈 $O((9N)^2)$ 增长，严重限制了高分辨率网格的生成效率。

### 核心创新：“一面一令牌”策略

FACE 的根本性创新在于**将令牌化的粒度从顶点坐标提升到面语义级别**。具体而言，FACE 提出“一面一令牌”（one-face-one-token）策略，将每个三角形面视为单个统一令牌，通过一个面嵌入层（Face Embedding layer）将9维坐标向量 $f_{i-1}$ 投影为单一的 $d_{model}$ 维令牌：

$$t_{i-1} = \text{MLP}_{\text{embed}}(f_{i-1})$$

这一设计直接攻击了自注意力的 $O(S^2)$ 计算瓶颈——序列长度缩短为原来的 $1/9$，压缩率达到 **0.11**，仅为先前最佳方法（**BPT**, Weng et al., arXiv 2024，压缩比 0.22）的一半（Table 1）。

### 关键技术组件

**1. 面嵌入层（Face Embedding）与 CausalMLP 解码头**

FACE 在编码端通过面嵌入层实现“多对一”的令牌压缩；在解码端，则采用 **CausalMLP** 头（引用自 ）引入面内的第二层自回归——将每个潜在面令牌 $h_i$ 逐坐标解码为9个量化坐标令牌。每个坐标令牌的预测条件化于 $h_i$ 以及该面内已生成的前序坐标令牌。这种“面间自回归 + 面内自回归”的双层结构，在保持端到端训练的同时实现了高保真重建。

**2. VecSet 编码器**

FACE 采用非对称的编码器-解码器设计。编码器将输入点云压缩为紧凑的潜在向量集（VecSet），通过最远点采样（FPS）获取查询点，经交叉注意力聚合全局几何信息，再由 $L_E$ 层标准Transformer编码器细化：

$$C' = \text{CrossAttn}(Q=Q, K=K_P, V=V_P)$$
$$C = \text{TransformerEncoder}_{L_E}(C')$$

该 VecSet 作为解码器交叉注意力的键和值，为逐面生成注入全局形状条件。

**3. 空间排序策略**

FACE 采用基于最小坐标顶点的字典序 ZYX 空间排序对面进行序列化，而非传统的图遍历顺序（如DFS/BFS）。消融实验（Table 3）证实，空间排序（ZYX及ZYX-component）在重建精度上大幅领先图遍历方法，ZYX排序取得最优Hausdorff距离。

### 与基线方法的本质差异

| 维度 | 基线方法 | FACE |
|------|---------|------|
| 令牌化级别 | 逐坐标（每面9令牌） | 逐面（每面1令牌） |
| 序列压缩比 | 0.22（BPT） | **0.11** |
| 解码策略 | 单层自回归 | 双层自回归（面间Transformer + 面内CausalMLP） |
| 面排序 | 图遍历或无特定策略 | ZYX空间排序 |

这一系列设计选择共同构成了FACE的核心创新：**在面语义级别而非顶点级别进行生成，从根本上降低序列长度，避免复杂的无损压缩方案，同时利用面嵌入层和CausalMLP头实现端到端的高保真网格重建。**

## 整体框架

FACE 的整体架构是一个非对称的自回归自编码器（ARAE），其设计核心在于用**面级令牌**替代传统顶点级序列，从根本上压缩自注意力所需的序列长度。如 Figure 2 所示，pipeline 由三个关键模块串联而成：**Shape Encoder**、**Autoregressive Face Decoder** 和 **CausalMLP Head**。

![[assets/figures/papers/paper_list_l2253_https_arxiv_org_abs_2603_01515/figures/002_Figure_2.jpg]]
*Figure 2: The end-to-end pipeline of our FACE model. An encoder compresses the input point cloud into a latent VecSet. An autoregressive decoder then conditions on this VecSet, generating the mesh face-by-face. A Face Embedding layer encoder 9 tokens of each face and a CausalMLP head decodes each latent face token into 9 quantized coordinate tokens*

**输入与编码**：给定输入点云 $\mathcal{P} \in \mathbb{R}^{P \times 3}$，Shape Encoder 首先通过最远点采样（FPS）选取一组查询点 $Q$，经交叉注意力与完整点集交互，得到初始潜在表示 $C'$：

$$C' = \text{CrossAttn}(Q=Q, K=K_P, V=V_P)$$

随后，$C'$ 经 $L_E$ 层标准 Transformer 编码器细化为紧凑的潜在向量集 $C$（VecSet）：

$$C = \text{TransformerEncoder}_{L_E}(C')$$

该 VecSet 作为全局形状条件，注入后续的自回归解码过程。

**面级自回归解码**：解码器接收 VecSet $C$ 作为交叉注意力的键和值，逐面生成网格。每个三角形面 $f_i$（由 9 个坐标值组成）首先通过 Face Embedding 层投影为单一令牌：

$$t_{i-1} = \text{MLP}_{\text{embed}}(f_{i-1})$$

这一“一面一令牌”策略将自注意力的序列长度缩减为原来的 1/9，直接缓解了 $O(S^2)$ 的计算瓶颈。解码器内部，因果自注意力仅关注已生成的面令牌以捕获局部结构：

$$H_l' = \text{CausalSelfAttn}(H_l)$$

随后通过交叉注意力注入全局形状条件：

$$H_{l+1} = \text{CrossAttn}(Q=H_l', K=C, V=C)$$

**面内坐标解码**：每个潜在面令牌 $h_i$ 被送入 CausalMLP 头，在面内部引入第二层自回归——第 $j$ 个坐标令牌的预测以 $h_i$ 和该面内已预测的坐标令牌为条件，最终输出 9 个量化坐标令牌，完成从潜在表示到显式网格的重建。

**训练与损失**：整个 ARAE 端到端训练，损失函数为所有面及其 9 个坐标预测的平均交叉熵：

$$\mathcal{L} = \frac{1}{N} \sum_{i=1}^{N} \sum_{j=1}^{9} \text{CrossEntropy}(L_{i,j}, c_{i,j})$$

**图像到网格的扩展**：FACE 的模块化设计使其可自然适配条件生成任务。如 Figure 3 所示，图像到网格生成管线先用输入图像条件化一个 DiT 模型，生成潜在 VecSet，再将其馈入训练好的 Autoregressive Face Decoder，输出最终网格。这种解耦设计使得解码器无需针对不同模态重新训练。

**效率优势**：Table 1 的令牌效率对比显示，FACE 的压缩比达到 0.11，仅为先前最优方法（0.22）的一半，序列长度的大幅缩减是其在重建质量和生成效率上同时取得突破的结构性原因。

### 补充图表

![[assets/figures/papers/paper_list_l2253_https_arxiv_org_abs_2603_01515/figures/004_Figure_3.jpg]]
*Figure 3: Overview of our image-to-mesh generation pipeline. We first use the input image to condition a DiT model. The resulting latent VecSet is then fed into the Autoregressive Face Decoder to produce the final mesh*

## 核心模块与公式推导

FACE 的端到端管线（Figure 2）由三个核心模块串联构成：**形状编码器（Shape Encoder）**、**自回归面解码器（Autoregressive Face Decoder）** 和 **CausalMLP 头**。其中，面解码器内部嵌入了实现“一面一令牌”策略的面嵌入层。

### 3.1 形状编码器：从点云到潜在 VecSet

编码器的任务是将输入点云 $P \in \mathbb{R}^{M \times 3}$ 压缩为一个紧凑的潜在向量集 $C$（VecSet）。该模块采用非对称设计，由两个子步骤组成。

**步骤一：交叉注意力聚合。** 首先通过最远点采样（FPS）从 $P$ 中选取 $K$ 个查询点 $Q \in \mathbb{R}^{K \times 3}$，将其作为交叉注意力的查询，与完整点云的键 $K_P$ 和值 $V_P$ 进行交互，得到初始潜在表示 $C'$：

$$C' = \mathrm{CrossAttn}(Q=Q, K=K_P, V=V_P) \tag{1}$$

这一操作使每个查询点能够聚合来自整个点云的全局几何信息。

**步骤二：Transformer 编码器精炼。** 将 $C'$ 送入一个由 $L_E$ 层标准 Transformer 组成的编码器，通过自注意力进一步细化为最终的潜在 VecSet $C$：

$$C = \mathrm{TransformerEncoder}_{L_E}(C') \tag{2}$$

消融实验（Table 4）证实，使用降采样点云作为查询点（而非可学习查询）能显著提升重建精度，Chamfer 距离达到 0.047。

### 3.2 自回归面解码器：一面一令牌的核心实现

解码器是 FACE 方法的核心，其设计直接针对现有方法将网格展平为长顶点坐标序列所导致的 $O(S^2)$ 自注意力计算瓶颈。解码器由面嵌入层、因果自注意力层和交叉注意力层交替堆叠而成。

**面嵌入层（Face Embedding）。** 这是“一面一令牌”策略的架构实现。给定第 $i-1$ 个已生成的面 $f_{i-1}$（由 9 个量化坐标令牌组成），面嵌入层通过一个 MLP 将其投影为单一的 $d_{\text{model}}$ 维令牌 $t_{i-1}$：

$$t_{i-1} = \mathrm{MLP}_{\text{embed}}(f_{i-1}) \tag{3}$$

这一设计将自注意力序列长度缩短为原来的 $1/9$，压缩比达到 0.11（Table 1），仅为先前最优方法的一半。

**因果自注意力。** 解码器的每一层首先对历史面令牌序列执行因果自注意力，确保第 $i$ 个面的生成仅依赖于前 $i-1$ 个面：

$$H_l' = \mathrm{CausalSelfAttn}(H_l) \tag{4}$$

**交叉注意力注入全局条件。** 随后，解码器通过交叉注意力将编码器输出的潜在 VecSet $C$ 作为全局形状条件注入每一层：

$$H_{l+1} = \mathrm{CrossAttn}(Q=H_l', K=C, V=C) \tag{5}$$

这种“因果自注意力 + 交叉注意力”的交替结构，使模型既能捕获网格面的局部拓扑依赖，又能保持对全局几何形状的感知。

### 3.3 CausalMLP 头：面内坐标级自回归

解码器输出的潜在面令牌 $h_i$ 仍需被解码为具体的 9 个量化坐标令牌。FACE 采用一个轻量级的 CausalMLP 头来实现面内的第二层自回归：第 $j$ 个坐标令牌的预测同时依赖于潜在向量 $h_i$ 和该面内已预测的前 $j-1$ 个坐标令牌。消融实验（Table 5）表明，CausalMLP 在坐标解码精度上大幅领先并行预测和注意力解码方案。

### 3.4 训练目标

整个自回归自编码器（ARAE）以端到端方式训练，损失函数为所有面及其 9 个量化坐标预测值的平均交叉熵：

$$\mathcal{L} = \frac{1}{N} \sum_{i=1}^{N} \sum_{j=1}^{9} \mathrm{CrossEntropy}(L_{i,j}, c_{i,j}) \tag{6}$$

其中 $N$ 为面数，$L_{i,j}$ 为第 $i$ 个面第 $j$ 个坐标的预测 logits，$c_{i,j}$ 为对应的真实量化坐标标签。

## 实验与分析

### 核心实验设置

FACE的自回归自编码器（ARAE）采用非对称编码器-解码器设计，解码器容量显著大于编码器。编码器由8层Transformer组成，隐藏维度为768；解码器包含24层，隐藏维度为1024。潜在VecSet包含2048个令牌，瓶颈维度为64。所有网格均归一化到$[-1,1]^3$范围内，点云采样8192个点，网格面数上限为800。训练使用Muon优化器，ARAE学习率为$6 \times 10^{-4}$，DiT学习率为$1 \times 10^{-4}$。

### 令牌效率对比

Table 1展示了各方法的网格令牌压缩效率。FACE的“一面一令牌”策略将序列长度压缩至原来的1/9，压缩比达到**0.11**，仅为先前最优方法（BPT的0.22）的一半。这一结果直接验证了核心设计动机——从根本上缩短自注意力序列长度以突破$O(N^2)$计算瓶颈。

### 网格重建质量

Table 2报告了在Objaverse、Toys4K和Famous三个数据集上的定量对比。FACE在所有数据集上均取得最低的Hausdorff距离（HD）和Chamfer距离（CD）：

- **Objaverse**：HD 0.090，CD 0.041，相较于最佳基线EdgeRunner（HD约0.111）降低约18.9%。
- **Toys4K**：HD 0.067，CD 0.033，比EdgeRunner（HD 0.091）降低**26.4%**，提升幅度最为显著。
- **Famous**：HD 0.077，CD 0.049，同样优于所有对比方法。

Figure 4的定性对比进一步印证：FACE生成的网格拓扑连通性更好，细节保留更完整，而基线方法在复杂区域常出现面片断裂或缺失。

### 消融实验

#### 面排序策略（Table 3）

![[assets/figures/papers/paper_list_l2253_https_arxiv_org_abs_2603_01515/figures/009_Table_3.jpg]]
*Table 3: Ablation on mesh face ordering strategies*

在“一面一令牌”框架下，面的序列顺序直接影响自回归建模的难易程度。实验对比了图遍历排序（DFS、BFS）与空间排序（ZYX、ZYX-component）。结果显示，空间排序策略**大幅领先**图遍历方法，其中ZYX排序以HD 0.103取得最佳性能。这归因于空间排序使相邻面在序列中保持邻近，降低了自回归预测的局部几何跳变。

#### 编码器查询方式（Table 4）

![[assets/figures/papers/paper_list_l2253_https_arxiv_org_abs_2603_01515/figures/007_Table_4.jpg]]
*Table 4: Ablation on different queries of the shape encoder*

VecSet编码器采用交叉注意力将点云压缩为潜在表示，查询点的选择至关重要。实验对比了可学习查询与降采样点云查询两种方案。降采样查询的CD达到0.047，**明显优于**可学习查询。这表明直接从输入几何中采样查询点能保留更精确的空间锚定信息，避免可学习查询在训练中丢失几何先验。

#### 坐标解码策略（Table 5）

![[assets/figures/papers/paper_list_l2253_https_arxiv_org_abs_2603_01515/figures/008_Table_5.jpg]]
*Table 5: Ablation on coordinate decoding strategies*

面令牌到9个量化坐标令牌的解码是第二层自回归的关键。实验对比了三种策略：并行预测（MLP一次性输出9个坐标）、注意力解码（Transformer逐坐标生成）、CausalMLP解码。CausalMLP以CD 0.047**大幅领先**另外两种方案，验证了面内坐标间存在强条件依赖，逐坐标因果建模能有效捕获这一局部几何结构。

### 图像到网格生成

Figure 5展示了图像条件网格生成的定性结果。FACE生成的网格在细节丰富度、与输入图像的对齐度以及拓扑连通性方面均优于EdgeRunner。这得益于DiT生成的潜在VecSet保留了全局形状信息，而自回归面解码器在此基础上逐面构建高保真网格。

### 失败模式与局限

尽管FACE在主流基准上表现优异，仍存在两个主要局限：

1. **离散表示的上限**：量化坐标令牌的离散特性限制了可实现的细节水平，对于极其精细的结构（如自行车辐条），离散化误差可能导致重建不完整。
2. **点云采样的依赖**：编码器依赖输入点云，若点云在薄结构或遮挡区域采样不足，解码器缺乏足够的几何线索，导致该区域重建失败。

这两个问题指向相同的深层挑战：如何在保持序列压缩优势的同时，提升对极端几何特征的表达能力。

### 补充图表

![[assets/figures/papers/paper_list_l2253_https_arxiv_org_abs_2603_01515/figures/003_Table_1.jpg]]
*Table 1: Comparison on mesh token efficiency. Our method achieves a state-of-the-art compression ratio, representing the mesh with the shortest sequence length*

![[assets/figures/papers/paper_list_l2253_https_arxiv_org_abs_2603_01515/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparison of mesh reconstruction quality on multiple datasets*

![[assets/figures/papers/paper_list_l2253_https_arxiv_org_abs_2603_01515/figures/010_Figure_5.jpg]]
*Figure 5: Qualitative comparison of image-conditioned mesh generation*

![[assets/figures/papers/paper_list_l2253_https_arxiv_org_abs_2603_01515/figures/011_Figure_6.jpg]]
*Figure 6: Qualitative comparisons between the base and large model*

## 方法谱系与知识库定位

### 1. 自回归网格生成的方法谱系

FACE 处于“自回归网格生成”这一细分方向的核心位置，其根本贡献在于**将自回归的粒度从顶点坐标提升到面语义级别**，从而系统性地解决了此前方法的序列长度瓶颈。

此前的主流方法可大致分为两条路线：

**路线一：顶点级自回归序列建模。** 这类方法将网格展平为长序列的顶点坐标，再交由 Transformer 自回归生成。代表性工作包括：

- **MeshGPT** (Siddiqui et al., CVPR 2024)：使用 VQ-VAE 将三角面编码为离散 token，再以 GPT 风格自回归生成。由于每个面需要三个顶点共 9 个坐标 token，序列长度随面数线性膨胀，自注意力的 $O(S^2)$ 计算代价成为高分辨率网格生成的硬瓶颈。
- **MeshXL** (Chen et al., NeurIPS 2025)：将网格视为神经坐标场，同样在顶点级别进行序列化，面临类似的效率困境。
- **MeshAnything** / **MeshAnything V2** (Chen et al., arXiv 2024)：前者关注艺术家创作网格的自回归生成，后者引入邻接面 tokenization 来缓解序列长度问题，但本质上仍停留在“多 token 描述一个面”的范式内。

**路线二：压缩 tokenization 策略。** 为缓解序列膨胀，部分工作尝试在 token 层面进行压缩：

- **EdgeRunner** (Tang et al., arXiv 2024)：采用自回归自编码器架构，通过边级表示降低 token 数量，在 FACE 之前是该方向的最强基线。
- **TreeMeshGPT** (Lionar et al., CVPR 2025)：通过树结构排序面序列，利用层次化 token 组织来提升效率。
- **BPT** (Weng et al., arXiv 2024)：引入压缩 tokenization 策略，将压缩比推至 0.22，是 FACE 之前的最优值。

FACE 的“一面一令牌”（one-face-one-token）策略直接跳出了上述两条路线的思维框架：**不再试图在顶点级别做压缩，而是将整个三角形面视为不可分割的原子 token**。这一设计将序列长度缩减为原来的 1/9，压缩比达到 0.11，仅为 BPT 的一半（Table 1）。这意味着在相同计算预算下，FACE 可以处理面数 9 倍于顶点级方法的网格，从根本上拓宽了自回归网格生成的适用边界。

### 2. 关键技术差异与因果机制

FACE 相对于基线的优势并非仅来自 token 数量的减少，而是**“面级 token + 面内坐标级自回归”双层架构的系统性结果**。具体而言：

| 设计维度 | 基线做法 | FACE 做法 | 因果效应 |
|---------|---------|----------|---------|
| Token 粒度 | 每面 9 个坐标 token | 每面 1 个面 token（Face Embedding 层） | 序列长度降为 1/9，自注意力计算量降为 1/81 |
| 坐标解码 | 并行预测或注意力解码 | CausalMLP 头（面内第二层自回归） | 消融实验证实 CausalMLP 大幅领先并行预测和注意力解码（Table 5） |
| 面排序 | 图遍历顺序（DFS/BFS） | ZYX 空间排序 | 空间排序显著优于图遍历，ZYX 取得最优 Hausdorff 距离（Table 3） |
| 编码器查询 | 可学习查询向量 | 降采样点云作为查询 | 降采样查询的重建精度明显优于可学习查询（Table 4） |

这些设计选择的因果链是清晰的：**面级 token 降低了全局自注意力的序列长度 → CausalMLP 在面内以极低成本恢复坐标级精度 → ZYX 排序为自回归模型提供了更可预测的几何先验 → 降采样查询保留了输入点云的几何分布信息**。四条因果路径共同作用，使得 FACE 在 Objaverse、Toys4K 和 Famous 三个数据集上均取得最低的 Hausdorff 和 Chamfer 距离（Table 2），在 Toys4K 上的 Hausdorff 距离比最佳基线 EdgeRunner 低 26% 以上。

### 3. 适用边界与能力定位

FACE 的核心能力边界由其架构选择决定：

**适用场景：**
- **点云到网格的重建**：这是 FACE 的原生任务，VecSet 编码器天然适配非结构化点云输入。
- **图像到网格的生成**：通过将 VecSet 作为 DiT 模型的生成目标，FACE 可扩展到条件生成任务（Figure 3, Figure 5），生成细节更丰富、拓扑连通性更好的网格。
- **高面数网格的高效生成**：得益于 $O(S^2/81)$ 的自注意力计算复杂度，FACE 在处理高分辨率网格时具有显著的效率优势。

**不适用或需谨慎的场景：**
- **无点云输入的纯生成**：FACE 的编码器依赖输入点云作为条件，直接无条件生成需要额外的潜在空间建模（如 DiT），这增加了系统复杂度。
- **极端精细结构**：论文明确指出，离散表示并非无限，限制了可实现的细节水平上限。依赖输入点云意味着极其精细或薄的结构（如自行车辐条）可能无法充分采样，导致重建不完整。

### 4. 局限与开放问题

论文自身识别出两个关键局限，这些局限同时指向了未来的研究方向：

1. **离散表示的精度上限。** FACE 使用量化坐标 token，这天然限制了网格细节的精细程度。问题在于：分辨率能否在不引入量化误差的情况下扩展到 1024 以上？这需要探索更高阶的离散化策略或混合精度表示。

2. **点云采样的信息瓶颈。** FACE 的编码器依赖点云输入，当目标网格包含极其精细的结构时，点云可能无法充分采样这些区域，导致重建不完整。一个开放问题是：能否引入额外的几何先验（如边缘感知采样或自适应查询）来弥补这一信息缺口？

此外，从方法谱系的角度看，FACE 的“一面一令牌”策略与 TreeMeshGPT 的层次化树结构、EdgeRunner 的边级表示之间存在潜在的互补性——将面级 token 与层次化组织相结合，或可进一步压缩序列长度并捕获多尺度几何结构。这一方向尚未被探索。

## 原文 PDF

![[paperPDFs/CVPR_2026/FACE_A_Face_based_Autoregressive_Representation_for_High_Fidelity_and_Efficient_Mesh_Generation.pdf]]
