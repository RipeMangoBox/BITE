---
title: "MeshWeaver: Sparse-Voxel-Guided Surface Weaving for Autoregressive Mesh Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/arxiv_2026/MeshWeaver_Sparse_Voxel_Guided_Surface_Weaving_for_Autoregressive_Mesh_Generation.pdf
project_link: null
code_link: null
aliases:
- MeshWeaver
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过将预测单元从坐标提升到顶点，并结合稀疏体素编码器提供的多级几何特征作为顶点表示、交叉注意力引导和生成空间约束，实现紧凑标记化与几何忠实的表面编织。
primary_logic: 将网格生成重新定义为在已知几何表面上的顶点编织过程；稀疏体素编码器的层次化特征能够同时充当顶点嵌入、预测条件与表面骨架，从而在单次解码中实现由粗到精的顶点预测，并保证生成结果贴合输入表面。
claims:
- 提出顶点级标记化将压缩率提升至18%，创下自回归网格标记化的新记录。
- 移除体素特征表示(VF)和交叉注意力(CA)导致Chamfer Distance从0.116严重恶化至0.158，证明几何上下文注入对性能至关重要。
- 在点云条件生成任务中，MeshWeaver在CD、HD等指标上显著超越先前自回归方法，并获得最大的法线一致性比率(|NC|)。
- 方法可生成高达16K面的高面数网格，突破现有自回归方法的扩展限制。
---

# MeshWeaver: Sparse-Voxel-Guided Surface Weaving for Autoregressive Mesh Generation

> [!tip] 核心洞察
> 将网格生成重新定义为在已知几何表面上的顶点编织过程；稀疏体素编码器的层次化特征能够同时充当顶点嵌入、预测条件与表面骨架，从而在单次解码中实现由粗到精的顶点预测，并保证生成结果贴合输入表面。

| 字段 | 内容 |
|------|------|
| 中文题名 | MeshWeaver：稀疏体素引导的表面编织自回归网格生成 |
| 英文题名 | MeshWeaver: Sparse-Voxel-Guided Surface Weaving for Autoregressive Mesh Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2606.04688) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MeshWeaver |
| Dataset | ShapeNet（点云条件网格生成）；Thingi10K（通用网格压缩） |

> [!tip] 效果简介
> - Mesh Tokenization Efficiency 上，Compression Ratio (lower is better) 0.18 vs 0.22 (BPT) (-0.04)。

## 概要

**MeshWeaver** 是一个自回归网格生成框架，其核心思想是将网格生成重新定义为**在已知几何表面上的顶点编织过程**。与现有方法逐坐标预测 3D 点不同，MeshWeaver 将预测单元从坐标提升到顶点，实现紧凑的顶点级标记化；同时引入一个层次化稀疏体素编码器，为生成过程注入多级几何上下文。

**核心瓶颈与因果机制**：现有自回归网格生成方法（如 MeshGPT、EdgeRunner、TreeMeshGPT 等）面临两个根本性限制：（1）坐标级标记化产生超长序列，难以扩展至高面数网格；（2）缺乏局部几何引导，生成结果的几何保真度不足。MeshWeaver 通过三个互补的几何注入机制解决上述问题——稀疏体素特征作为顶点表示替代静态词汇嵌入、逐级交叉注意力引导 token 预测、以及空体素 logit 遮蔽作为生成空间约束——从而在单次解码中实现由粗到精的顶点预测，并保证生成结果贴合输入表面。

**方法定位**：MeshWeaver 属于自回归网格生成范式，但其顶点级标记化将压缩率提升至 **18%**，创下该方向的新记录（此前最优为 BPT 的 22%）。在点云条件生成任务中，该方法在 Chamfer Distance、Hausdorff Distance 等指标上显著超越先前自回归方法，并获得最大的法线一致性比率。此外，MeshWeaver 可生成高达 **16K 面**的高面数网格，突破了现有自回归方法的扩展限制。

消融实验进一步验证了因果机制的可靠性：同时移除体素特征表示和交叉注意力导致 Chamfer Distance 从 0.116 恶化至 0.158，证明几何上下文注入对高保真度重建至关重要；移除生成骨架约束也使指标轻微退化，验证了稀疏体素约束对避免预测漂移的贡献。



### 网格生成的自回归范式困境

自回归生成在语言和图像领域取得了显著成功，但在三维网格生成中面临根本性挑战。网格由大量顶点坐标构成，一个包含 $N$ 个三角面的网格需要 $3N$ 个顶点，若按朴素坐标级标记化，将产生 $9\tilde{N}$ 个坐标 token 的长序列：

$$\mathcal{M} = \{ v_{1}^{x}, v_{1}^{y}, v_{1}^{z}, \ldots, v_{3N}^{x}, v_{3N}^{y}, v_{3N}^{z} \}$$

这种标记化方式导致序列长度随面数线性膨胀，使得自回归生成难以扩展至高面数网格。同时，坐标级预测缺乏对局部几何结构的感知，生成结果容易出现面片坍塌、表面不连续等几何保真度问题。

### 现有方法的两个核心缺口

**缺口一：标记化效率与扩展性瓶颈。** 现有自回归网格生成方法（如 **MeshGPT** (Siddiqui et al., CVPR 2024)、**EdgeRunner** (Tang et al., ICLR 2025)、**TreeMeshGPT** (Lionar et al., CVPR 2025)）在标记化效率上已取得进展，但压缩率仍停留在约 22%（**BPT** (Weng et al., CVPR 2025) 为当前最优），限制了网格面数的上限。**DeepMesh** (Zhao et al., arXiv 2025) 引入强化学习优化生成过程，但标记化瓶颈仍未突破。

**缺口二：几何上下文注入不足。** 现有方法多依赖静态词汇表嵌入表示顶点，或通过全局前缀/交叉注意力注入形状信息，缺乏对局部几何细节的精细引导。这导致生成结果在尖锐特征、薄壁结构等区域容易偏离输入表面，法线一致性不足。

### 核心动机：将生成重新定义为表面编织

MeshWeaver 的出发点是将网格生成从“逐坐标预测”提升为“逐顶点编织”——在已知几何表面上，自回归地预测下一个顶点，而非孤立的坐标点。这一范式转换需要解决两个关键问题：(1) 如何紧凑地表示顶点以缩短序列长度；(2) 如何将几何表面信息有效注入生成过程，使预测的顶点始终贴合目标表面。稀疏体素编码器的引入正是为了同时解决这两个问题：其层次化特征既作为顶点嵌入替代静态词汇表，又通过交叉注意力提供局部几何引导，同时以体素骨架约束生成空间，防止预测漂移。



## 核心方法与创新机理

MeshWeaver 的核心创新在于将自回归网格生成的建模单元从**坐标提升为顶点**，并引入**稀疏体素编码器**提供多层次几何上下文，从而在紧凑标记化与几何保真度两个维度上同时突破现有方法的瓶颈。具体而言，该工作通过以下四个关键设计槽位（changed slots）实现范式转变：

### 1. 预测单元：从“下一坐标”到“下一顶点”

现有自回归网格生成方法（如 **MeshGPT** (Siddiqui et al., CVPR 2024)、**EdgeRunner** (Tang et al., ICLR 2025)、**TreeMeshGPT** (Lionar et al., CVPR 2025)）将网格展平为坐标序列，逐点预测三维坐标。这导致序列长度随面数线性增长（每面9个坐标token），难以扩展至高面数网格，且缺乏对顶点整体几何结构的感知。

MeshWeaver 提出**顶点级标记化**（vertex-level tokenization），将网格划分为局部补丁（patch），每个补丁包含一个中心顶点及其顺时针环绕的周围顶点。序列建模的基本单元从单个坐标变为一个完整顶点，任务重新定义为“下一顶点预测”。这一设计将压缩率推至 **18%**，创下自回归网格标记化的新纪录（对比基线 **BPT** (Weng et al., CVPR 2025) 的22%），序列长度大幅缩短，使模型能够生成高达 **16K 面**的高面数网格（Figure 1）。

### 2. 顶点表示：从静态词表嵌入到几何感知体素特征

传统自回归方法为量化后的坐标分配静态词汇表嵌入（static vocabulary embeddings），这类嵌入与具体形状无关，无法传递局部几何信息。

MeshWeaver 改用**多级稀疏体素特征**作为顶点表示。稀疏体素编码器将输入表面编码为 $L$ 个层级的层次化特征 $\mathcal{F} = \{ \mathbf{F}^0, \mathbf{F}^1, \ldots, \mathbf{F}^{L-1} \}$（Section 3.3）。每个顶点 $v_i$ 由其在各级体素索引对应的特征拼接而成：

$$\mathbf{e}(v_i) = \mathrm{Concat}(\mathbf{F}^0[v_i^0], \mathbf{F}^1[v_i^1], \dots, \mathbf{F}^{L-1}[v_i^{L-1}])$$

这种形状感知的嵌入使模型在解码之初即获得丰富的局部几何先验，为后续高保真度生成奠定基础。

### 3. 预测引导：从全局条件到层级化局部交叉注意力

现有方法通常通过全局形状嵌入或前缀交叉注意力注入条件信息，缺乏对局部几何细节的精细化引导。

MeshWeaver 在自回归Transformer解码器的**每一级预测头**之前，引入**层级化交叉注意力**（per-level cross-attention），使隐藏状态与对应级别的稀疏体素特征进行交互。对于 $l>0$ 的精细级别，注意力进一步限制在父体素对应的子体积内，确保模型仅在局部几何上下文中做出预测。消融实验（Table 3）表明，移除体素特征表示（VF）和交叉注意力（CA）后，Chamfer Distance 从 **0.116 恶化至 0.158**，Hausdorff Distance 从 **0.087 升至 0.138**，验证了局部几何引导对生成质量的因果性贡献。

### 4. 生成约束：从无约束采样到体素骨架锚定

基线方法在推理时进行无约束的自回归采样，预测的顶点可能漂移偏离目标表面。

MeshWeaver 利用稀疏体素编码器输出的非空体素作为**生成骨架**（generation scaffold），在每级预测时对空体素对应的logit进行掩码，强制预测顶点锚定在已知表面上。消融中移除生成骨架（w/o GS）使 CD 从 0.116 升至 0.122，HD 从 0.087 升至 0.090（Table 3），证实该约束有效抑制了预测漂移。

---

**总结**：MeshWeaver 通过上述四个槽位的协同改进，将网格生成重新定义为“在已知几何表面上的顶点编织过程”。稀疏体素编码器的层次化特征同时充当顶点嵌入、预测条件与表面骨架，使模型在单次自回归解码中实现由粗到精的顶点预测，并保证生成结果忠实贴合输入表面。这一设计从根本上解决了现有方法序列过长与几何保真度不足的双重瓶颈。



MeshWeaver 将网格生成重新定义为**在已知几何表面上的顶点编织过程**，其核心流水线由两个紧密协作的模块构成：**稀疏体素编码器**（Sparse-Voxel Encoder）与**自回归 Transformer 解码器**（Autoregressive Transformer Decoder），如图 Figure 2 所示。

![[assets/figures/papers/MeshWeaver_Sparse-Voxel-Guided_Surface_Weaving_for_Autoregressive_Mesh_Generatio_dedf0c3daf25/figures/002_Figure_2.jpg]]
*Figure 2: Left: Overall Pipeline of MeshWeaver. Given an input surface, we voxelize it and sample points to extract multi-level features with a sparse-voxel encoder. These sparse features provide geometry-aware context that (i) represent vertices, (ii) guide token predictions via cross-attention, and (iii) act as a generation scaffold. The transformer autoregressively weaves the mesh vertex by vertex in a coarse-to-fine manner, attending to voxel features for local geometric context. Right: Vertex-Level Mesh Tokenization. The mesh is traversed patch-by-patch to produce compact 2D vertex tokens, greatly shortening sequences*

**输入与编码阶段**：给定输入表面（如点云或稀疏体素），系统首先对其进行体素化并采样点，通过稀疏体素编码器提取**多级层次化体素特征** $\mathcal{F} = \{ \mathbf{F}^0, \mathbf{F}^1, \ldots, \mathbf{F}^{L-1} \}$。该编码器采用点聚合、移位窗口稀疏注意力与稀疏卷积下采样的组合架构（Figure 3 左），输出的多级特征在后续生成中扮演三重角色：(i) 作为顶点的几何感知表示；(ii) 通过交叉注意力引导 token 预测；(iii) 充当生成的结构骨架，约束顶点锚定在表面上。

**解码与生成阶段**：自回归 Transformer 解码器以**顶点级标记化**（Vertex-Level Mesh Tokenization）产生的紧凑 2D token 序列为预测目标。与先前方法逐坐标预测不同，MeshWeaver 将网格划分为局部补丁序列 $\mathcal{M} = \{ o_{1}, v_{11}, \ldots, o_{2}, v_{21}, \ldots \}$，每个补丁包含中心顶点及其顺时针环绕的周围顶点，从而将基本建模单元从坐标提升至顶点。解码器采用**由粗到精的多级解码**策略：每个顶点 $v_i = (v_i^0, \ldots, v_i^{L-1})$ 的多级体素索引被逐层预测，预测每一级时，隐藏状态通过交叉注意力与对应级别的稀疏体素特征交互以感知局部几何，同时利用**空体素 logit 遮蔽**确保预测结果始终落在有效表面上。

**推理优化**：为提升效率，系统引入**交叉注意力 KV 缓存**机制——将稀疏体素特征提前映射为键值对并缓存，解码时仅检索子体积内的相关键值，使推理吞吐量从 26.8 tokens/s 提升至 30.7 tokens/s（约 14.5%），且不损失精度。训练阶段则通过**子体积剪枝**策略随机选取子体积及其关联顶点计算损失，大幅降低交叉注意力的计算开销。

这一设计实现了紧凑的标记化（压缩率达 18%，创下自回归网格标记化新纪录），并使得单次解码即可生成贴合输入表面的高保真网格，支持高达 16K 面的高面数网格生成，突破了现有自回归方法的扩展限制。



### 3.1 预备知识：网格标记化

传统自回归网格生成方法将网格 $\mathcal{M}$（含 $N$ 个三角面）的所有顶点坐标按 $yzx$ 顺序展平为坐标级序列：

$$\mathcal{M} = \{ v_{1}^{x}, v_{1}^{y}, v_{1}^{z}, \ldots, v_{3N}^{x}, v_{3N}^{y}, v_{3N}^{z} \}$$

该序列长度为 $9\tilde{N}$（$\tilde{N}$ 为面数），其联合概率通过自回归分解建模：

$$p(\mathcal{M}) = \prod_{t=1}^{9\tilde{N}} p(c_t \mid c_{<t})$$

**瓶颈分析**：坐标级标记化产生过长序列，难以扩展至高面数网格；同时缺乏局部几何引导，生成结果的几何保真度不足。

### 3.2 顶点级网格标记化

MeshWeaver 将基本建模单元从坐标提升至**顶点**，将生成范式从“下一坐标预测”重构为“下一顶点预测”。具体而言，网格被划分为 $P$ 个局部补丁的序列：

$$\mathcal{M} = \{ o_{1}, v_{11}, \ldots, o_{2}, v_{21}, \ldots, \ldots, o_{P}, v_{P1}, \ldots \}$$

每个补丁包含一个中心顶点 $o_i$ 及其顺时针环绕的周围顶点 $v_{ij}$。每个顶点 $v_i$ 由 $L$ 个层级的体素索引表示：

$$v_{i} = (v_{i}^{0}, \ldots, v_{i}^{L-1})$$

顶点概率通过由粗到精的条件分解建模：

$$p(\pmb{v}_{j}) = \prod_{l=0}^{\bar{L}-1} p(v_{j}^{l} \mid v_{j}^{<l})$$

最终形成二维顶点 token 序列（每个补丁以 BOS 起始，序列以 EOS 终止）：

$$\mathcal{M} = \Big\{ \begin{array}{c} \mathrm{\tiny{BOS}} \\ \vdots \\ \mathrm{\tiny{BOS}} \end{array} \Big[ \begin{array}{c} o_{1}^{0} \\ \vdots \\ o_{1}^{L-1} \end{array} \Big], \left[ \begin{array}{c} v_{11}^{0} \\ \vdots \\ v_{1-1}^{L-1} \end{array} \right], \ldots, \left[ \begin{array}{c} \mathrm{\tiny{BOS}} \\ \vdots \\ \mathrm{\tiny{BOS}} \end{array} \right], \ldots, \left[ \begin{array}{c} \mathrm{\tiny{EOS}} \\ \vdots \\ \mathrm{\tiny{EOS}} \end{array} \right] \Big\}$$

**核心效果**：该设计将压缩率提升至 18%，创下自回归网格标记化的新记录（Table 1），并支持生成高达 16K 面的网格。

### 3.3 稀疏体素编码器与几何引导注入

稀疏体素编码器将输入表面编码为层次化稀疏体素特征：

$$\mathcal{F} = \{ \mathbf{F}^0, \mathbf{F}^1, \ldots, \mathbf{F}^{L-1} \}$$

其中 $\mathbf{F}^l \in \mathbb{R}^{N_l \times C_l}$ 为第 $l$ 级体素特征。这些特征以三种互补方式注入几何上下文：

**(1) 顶点表示（VF）**：每个顶点通过拼接其各级体素索引对应的特征得到形状感知嵌入，替代传统静态词汇表嵌入：

$$\mathbf{e}(v_i) = \mathrm{Concat}(\mathbf{F}^0[v_i^0], \mathbf{F}^1[v_i^1], \dots, \mathbf{F}^{L-1}[v_i^{L-1}])$$

**(2) 交叉注意力引导（CA）**：在预测每个层级 token 之前，解码器隐藏状态通过交叉注意力与对应级别的稀疏体素特征交互，感知局部几何信息；对于 $l>0$ 的层级，注意力被限制在父体素对应的子体积内。

**(3) 生成骨架约束（GS）**：通过遮蔽空体素的 logit 概率，确保每个预测顶点锚定在输入表面上，防止预测漂移。

### 3.4 训练与推理加速

**子体积剪枝**：训练时随机选取子体积及其关联顶点计算损失，大幅降低交叉注意力计算量（Figure 4）。

**交叉注意力 KV 缓存**：将稀疏体素特征提前映射为键值对并缓存，推理时仅检索子体积内的相关键值。该策略将推理吞吐量从 26.8 tokens/s 提升至 30.7 tokens/s（约 14.5%），且不损失精度。

### 消融验证

Table 3 的消融实验定量验证了各模块的因果贡献：
- 同时移除 VF 和 CA 导致 CD 从 0.116 严重恶化至 0.158，HD 从 0.087 升至 0.138，证明几何上下文注入对高保真度重建至关重要；
- 移除 GS 使 CD 升至 0.122，HD 升至 0.090，验证了稀疏体素约束对避免预测漂移的贡献。

### 补充图表

![[assets/figures/papers/MeshWeaver_Sparse-Voxel-Guided_Surface_Weaving_for_Autoregressive_Mesh_Generatio_dedf0c3daf25/figures/003_Figure_3.jpg]]
*Figure 3: Network Architectures. Left: sparse-voxel encoder. Right: autoregressive transformer*

![[assets/figures/papers/MeshWeaver_Sparse-Voxel-Guided_Surface_Weaving_for_Autoregressive_Mesh_Generatio_dedf0c3daf25/figures/004_Figure_4.jpg]]
*Figure 4: Training-time Subvolume Pruning*



## 实验与关键发现

### 网格标记化效率

MeshWeaver 的核心设计动机之一是解决现有自回归网格生成方法因坐标级标记化导致的序列过长问题。我们将预测单元从独立坐标提升为顶点，并采用多级体素索引表示，从而大幅压缩序列长度。Table 1 汇总了不同方法的网格标记化效率。MeshWeaver 取得了 **18%** 的压缩率（Compression Ratio），优于此前最优的 **BPT**（Weng et al., CVPR 2025）的 22%，创下自回归网格标记化的新纪录。这一结果验证了顶点级标记化在序列压缩上的显著优势，为后续高面数网格生成提供了可扩展的基础。

![[assets/figures/papers/MeshWeaver_Sparse-Voxel-Guided_Surface_Weaving_for_Autoregressive_Mesh_Generatio_dedf0c3daf25/figures/005_Table_1.jpg]]
*Table 1: Comparison on Mesh Tokenization Efficiency*

### 点云条件网格生成主结果

在点云条件网格生成这一核心任务上，我们与多个自回归网格生成基线进行了定量对比，包括 **MeshGPT**（Siddiqui et al., CVPR 2024）、**EdgeRunner**（Tang et al., ICLR 2025）、**TreeMeshGPT**（Lionar et al., CVPR 2025）、**BPT** 以及 **DeepMesh**（Zhao et al., arXiv 2025）。结果如 Table 2 所示，MeshWeaver 在 Chamfer Distance（CD）和 Hausdorff Distance（HD）两项核心几何误差指标上均取得了显著优势，同时获得了最高的法线一致性比率（|NC|）。这表明，稀疏体素编码器注入的多级几何引导不仅提升了生成网格的整体形状精度，也更好地保留了局部表面细节与法线方向的一致性。定性结果（Figure 5）进一步显示，MeshWeaver 生成的网格边缘更锐利、拓扑更规整，且在复杂几何区域（如细薄结构）的保真度明显优于基线方法。此外，得益于紧凑的顶点级标记化，MeshWeaver 可生成高达 **16K 面**的高面数网格（Figure 1），突破了现有自回归方法的扩展限制。

![[assets/figures/papers/MeshWeaver_Sparse-Voxel-Guided_Surface_Weaving_for_Autoregressive_Mesh_Generatio_dedf0c3daf25/figures/008_Figure.jpg]]

![[assets/figures/papers/MeshWeaver_Sparse-Voxel-Guided_Surface_Weaving_for_Autoregressive_Mesh_Generatio_dedf0c3daf25/figures/009_Figure.jpg]]

![[assets/figures/papers/MeshWeaver_Sparse-Voxel-Guided_Surface_Weaving_for_Autoregressive_Mesh_Generatio_dedf0c3daf25/figures/006_Table_2.jpg]]
*Table 2: Quantitative Results on Point-Cloud-Conditioned Mesh Generation*

![[assets/figures/papers/MeshWeaver_Sparse-Voxel-Guided_Surface_Weaving_for_Autoregressive_Mesh_Generatio_dedf0c3daf25/figures/001_Figure_1.jpg]]
*Figure 1: MeshWeaver generates high-quality 3D meshes autoregressively with a sparse-voxel-guided surface weaving process. By directly predicting next vertices instead of independent coordinates, it achieves a state-of-the-art mesh compression ratio of 18%, and can generate meshes with up to 16K faces*

![[assets/figures/papers/MeshWeaver_Sparse-Voxel-Guided_Surface_Weaving_for_Autoregressive_Mesh_Generatio_dedf0c3daf25/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative Results on Point-Cloud Conditioned Mesh Generation*

### 稀疏体素编码器消融研究

为系统评估稀疏体素编码器所注入的三重几何引导——**体素特征表示（VF）**、**交叉注意力引导（CA）** 以及 **生成骨架约束（GS）**——我们进行了消融实验，结果如 Table 3 和 Figure 6 所示。

![[assets/figures/papers/MeshWeaver_Sparse-Voxel-Guided_Surface_Weaving_for_Autoregressive_Mesh_Generatio_dedf0c3daf25/figures/010_Figure_6.jpg]]
*Figure 6: Qualitative Ablation Studies on Sparse-Voxel Encoder. Table 3. Ablation on Sparse-Voxel Encoder*

- **移除 VF 与 CA 的影响最为严重**：当同时移除体素特征表示和交叉注意力（w/o VF&CA）时，CD 从 0.116 恶化至 0.158，HD 从 0.087 升至 0.138，|NC| 从 0.914 降至 0.865。这组消融将模型退化至仅依赖静态词汇嵌入和全局自回归预测的基线状态，证明了**形状感知的顶点表示与局部几何上下文对高保真网格重建是不可或缺的**。
- **单独移除 VF 或 CA 均导致明显性能下降**：w/o VF（CD 0.142, HD 0.122）和 w/o CA（CD 0.146, HD 0.128）均显著弱于完整模型，表明几何感知嵌入和预测阶段的局部注意力各自独立贡献于生成质量。
- **生成骨架（GS）的贡献**：在推理时禁用空体素遮蔽（w/o GS），CD 轻微上升至 0.122，HD 升至 0.090，|NC| 降至 0.909。该退化幅度虽小于移除 VF/CA，但一致地出现在所有指标上，验证了稀疏体素骨架通过约束顶点锚定于表面来**防止预测漂移**的作用。

### 交叉注意力 KV 缓存加速

为缓解多级交叉注意力带来的推理开销，我们设计了交叉注意力 KV 缓存机制：将稀疏体素特征提前映射为键值对并缓存，解码时仅检索当前子体积内的相关键值。实验表明，启用该缓存后，推理吞吐量从 **26.8 tokens/s** 提升至 **30.7 tokens/s**，加速约 **14.5%**，且不损失任何生成精度。这为高面数网格的高效推理提供了实用的工程支撑。

### 层级空间划分方案消融

Table 4 报告了不同层级空间划分方案（不同 D₁、D₂ 组合及 Transformer 深度分配）的消融结果。实验表明，合理的层级划分（平衡各层体素粒度和解码器容量）对最终性能有显著影响，过于粗糙或过于细粒度的划分均会导致 CD/HD 上升。当前采用的配置在几何精度与序列压缩效率之间取得了最优平衡。

![[assets/figures/papers/MeshWeaver_Sparse-Voxel-Guided_Surface_Weaving_for_Autoregressive_Mesh_Generatio_dedf0c3daf25/figures/011_Table_4.jpg]]
*Table 4: Ablation Study on Level Partition*

### 失败模式与局限性

尽管 MeshWeaver 在多项指标上取得了领先，我们仍观察到以下局限：
- **极端细薄结构的表面编织**：当输入点云在极窄区域（如薄片边缘）存在稀疏或噪声采样时，稀疏体素骨架可能无法提供足够精细的表面约束，导致顶点编织出现局部错位或面片自交。这一问题在 Figure 6 的部分消融样本中有所体现。
- **补丁中心顶点的压缩瓶颈**：当前顶点级标记化方案对所有顶点（包括补丁中心顶点）采用统一的多级体素索引表示。中心顶点承载了补丁遍历的拓扑骨架信息，其编码效率仍有提升空间。论文也指出，未来可为中心顶点设计独立的 token 词汇表以进一步降低压缩率。
- **跨域泛化能力待验证**：当前实验主要基于刚性物体数据集，方法在非刚性物体、动态场景或跨域数据上的泛化能力尚未评估，需进一步研究。



## 定位与知识库关联

### 1. 对自回归网格生成范式的继承与突破

MeshWeaver 建立在自回归网格生成这一新兴技术路线之上，其核心贡献在于通过**预测单元升级**与**几何上下文注入**两个维度，系统性地突破了现有方法的瓶颈。

**继承的基线框架。** 近年来，自回归网格生成方法通过将网格建模为离散 token 序列，借助 Transformer 解码器逐 token 预测，在生成质量与多样性上取得了显著进展。代表性工作包括：

- **MeshGPT**（Siddiqui et al., CVPR 2024）：首次将自回归语言模型范式引入网格生成，通过矢量量化将三角面片编码为离散 token，验证了该技术路线的可行性。
- **EdgeRunner**（Tang et al., ICLR 2025）：进一步探索了基于边的自回归遍历策略，提升了网格拓扑的连贯性。
- **TreeMeshGPT**（Lionar et al., CVPR 2025）：引入树形结构组织网格 token，改善了长序列建模的效率。
- **BPT**（Weng et al., CVPR 2025）：通过块状压缩标记化（block-wise tokenization）将压缩率提升至 22%，代表了 MeshWeaver 之前的最优标记化效率。
- **DeepMesh**（Zhao et al., arXiv 2025）：将强化学习引入自回归网格生成，探索了非监督信号下的优化路径。

**MeshWeaver 的差异化突破。** 上述方法共享一个根本性局限：**预测单元停留在坐标级**，即将网格展平为 9N 个独立坐标 token（每个三角面片 3 个顶点 × 3 个坐标分量）。这导致两个连锁瓶颈：（1）序列长度随面数线性增长，难以扩展至高面数网格；（2）坐标 token 之间缺乏显式的几何结构约束，生成结果的几何保真度受限。

MeshWeaver 通过以下四个**关键设计槽位**的系统性变更，实现了范式升级：

| 设计槽位 | 基线方案 | MeshWeaver 方案 | 核心收益 |
|---------|---------|----------------|---------|
| **预测单元** | 坐标（3D 点） | 顶点（3D 点组） | 压缩率从 22% 降至 18%，序列长度缩减约 3 倍 |
| **顶点表示** | 静态词汇表嵌入 | 多级稀疏体素特征 | 形状感知的几何嵌入，替代形状无关的静态编码 |
| **预测引导** | 全局形状嵌入（prefix/cross-attention） | 逐级交叉注意力至局部体素特征 | 细粒度局部几何上下文注入 |
| **生成约束** | 无约束采样 | 空体素 logit 遮蔽 | 强制预测顶点锚定于输入表面 |

这一设计将网格生成重新定义为**已知几何表面上的顶点编织过程**——稀疏体素编码器提供的层次化特征同时充当顶点嵌入、交叉注意力条件与表面骨架，使得 Transformer 解码器能够在单次自回归过程中实现由粗到精的顶点预测。

### 2. 与相关技术路线的边界划分

**与非自回归方法的对比。** 与基于扩散模型（如 DiffusionNet）或基于 GAN 的网格生成方法相比，MeshWeaver 保留了自回归框架的核心优势——无需迭代去噪或对抗训练，生成过程直接且可控。同时，通过稀疏体素编码器注入显式几何先验，弥补了纯自回归方法在几何一致性上的不足。

**与基于点云的重建方法。** 传统点云到网格的重建方法（如泊松重建、Marching Cubes 变体）通常依赖后处理步骤生成网格拓扑，缺乏对网格面片分布的端到端优化。MeshWeaver 在点云条件生成任务中直接输出带拓扑结构的网格，在 Chamfer Distance（CD）、Hausdorff Distance（HD）和法线一致性比率（|NC|）上均显著超越先前自回归方法，验证了端到端编织策略的优越性。

### 3. 适用边界与局限

尽管 MeshWeaver 在标记化效率和高面数生成能力上取得了突破，其方法设计仍存在明确的适用边界：

**标记化压缩的剩余空间。** 当前 18% 的压缩率虽创下新纪录，但顶点级标记化方案仍有优化余地。论文明确指出，未来可探索针对补丁中心顶点设计更高效的 token 集或编码方式，进一步缩短序列长度。

**几何上下文的依赖强度。** 消融实验（Table 3）揭示了方法对稀疏体素编码器的强依赖：同时移除体素特征表示（VF）和交叉注意力（CA）导致 CD 从 0.116 急剧恶化至 0.158，HD 从 0.087 升至 0.138。这表明 MeshWeaver 的生成质量高度依赖于输入几何信号的质量——当输入点云稀疏或噪声较大时，体素特征的有效性可能下降，进而影响编织精度。

**训练与推理的计算权衡。** 交叉注意力 KV 缓存将推理吞吐量从 26.8 tokens/s 提升至 30.7 tokens/s（约 14.5%），但训练阶段仍需通过子体积剪枝（Subvolume Pruning）策略降低交叉注意力的计算开销。这暗示了在大规模场景下的训练效率仍有优化空间。

### 4. 开放问题与潜在延伸方向

MeshWeaver 开辟了“几何引导的自回归编织”这一新范式，其核心思想——将生成过程锚定于显式几何骨架——具有广阔的延伸潜力：

1. **标记化效率的进一步突破。** 论文提出的补丁中心顶点独立编码方案能否将压缩率推至 15% 以下？这一方向可能涉及对网格拓扑结构的更深层次利用。

2. **跨域泛化能力。** 当前实验验证集中在刚性物体网格（ShapeNet 等数据集），方法在非刚性物体（如衣物、人体姿态）、动态场景或跨域数据（如 CAD 模型与自然物体扫描）上的泛化能力尚未探索。

3. **多模态与交互式扩展。** 稀疏体素引导的编织策略能否拓展至纹理生成（将颜色信息纳入顶点表示）、蒙皮网格生成（引入骨骼约束）或交互式网格编辑（用户指定局部体素约束）？这些方向可能使 MeshWeaver 从生成工具演化为通用网格操作框架。

4. **与大规模语言模型的融合。** 自回归 Transformer 解码器的架构与语言模型天然兼容，未来工作可探索将文本或图像条件融入交叉注意力机制，实现多模态条件网格生成。



## 原文 PDF

![[paperPDFs/arxiv_2026/MeshWeaver_Sparse_Voxel_Guided_Surface_Weaving_for_Autoregressive_Mesh_Generation.pdf]]
