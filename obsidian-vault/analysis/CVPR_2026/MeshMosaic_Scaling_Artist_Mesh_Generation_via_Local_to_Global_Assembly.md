---
title: "MeshMosaic: Scaling Artist Mesh Generation via Local-to-Global Assembly"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MeshMosaic_Scaling_Artist_Mesh_Generation_via_Local_to_Global_Assembly.pdf
project_link: "https://xrvitd.github.io/MeshMosaic/index.html"
code_link: null
aliases:
- MeshMosaic
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将完整网格分解为局部面片（patch），在边界条件与全局‑局部点云特征的引导下，逐块进行独立高分辨率量化与自回归生成，再通过位移对齐组装为完整网格。
primary_logic: 将“马赛克艺术”的局部‑全局组装思想引入自回归网格生成，使每一块面片在共享边界条件和全局上下文的约束下独立生成，从而突破长序列瓶颈，实现超过100K面的高保真艺术家网格生成。
claims:
- 在ShapeNet、Thingi10K、Objaverse三个数据集上，MeshMosaic在HD、CD、NC、F1等几何指标上全面优于DeepMesh、BPT等SOTA方法。
- 在包含27位专业用户的用户调研中，MeshMosaic在整洁度、艺术性、相似度和细节恢复四项上均获得最高评分（2.78‑2.91分）。
- MeshMosaic能够生成超过100K三角形的网格，而先前方法通常仅支持~8K面。
- ShapeNet 上 CDL2 (×10³) ↓ = 0.019
---

# MeshMosaic: Scaling Artist Mesh Generation via Local-to-Global Assembly

> [!tip] 核心洞察
> 将“马赛克艺术”的局部‑全局组装思想引入自回归网格生成，使每一块面片在共享边界条件和全局上下文的约束下独立生成，从而突破长序列瓶颈，实现超过100K面的高保真艺术家网格生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | MeshMosaic：通过局部到全局组装实现艺术家网格生成规模化 |
| 英文题名 | MeshMosaic: Scaling Artist Mesh Generation via Local-to-Global Assembly |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2509.19995) · [Project](https://xrvitd.github.io/MeshMosaic/index.html) |
| Topic | #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/generative_models_diffusion/diffusion_image_video |
| Method | MeshMosaic |
| Dataset | ShapeNet, Thingi10K, Objaverse, User Study |

> [!tip] 效果简介
> - ShapeNet 上，CDL2 (×10³) ↓ 0.019 vs 0.060 (DeepMesh) (-0.041)。
> - Thingi10K 上，CDL2 (×10³) ↓ 0.052 vs 2.492 (MeshAnythingV2) (-2.440)。
> - Objaverse 上，CDL2 (×10³) ↓ 0.387 vs 1.712 (DeepMesh) (-1.325)。

## 概述

**核心问题**：当前基于Transformer的自回归网格生成方法受限于长序列建模瓶颈和统一的低分辨率量化策略，难以生成超过8K面的高保真网格，导致精细几何细节与结构化密度模式大量丢失。

**核心思想**：MeshMosaic 借鉴“马赛克艺术”的局部‑全局组装思想，将完整网格分解为多个语义面片（patch），在共享边界条件与全局‑局部点云特征的约束下，逐块进行独立高分辨率量化与自回归生成，再通过位移对齐无缝拼接为完整网格。这一策略从根本上突破了长序列瓶颈，使网格面数可扩展至100K以上。

**方法定位**：MeshMosaic 属于自回归网格生成范式，直接继承 **DeepMesh**（Zhao et al., arXiv 2025）的 Hourglass Transformer 架构与标记化方案，但在生成策略、条件输入、量化分辨率和训练分割四个关键环节进行了系统性改造。与 **MeshAnythingV2**（Chen et al., arXiv 2024）的相邻面片标记化、**BPT** 的分块面片化以及 **TreeMeshGPT** 的树状邻接建模等同期工作相比，MeshMosaic 首次将语义分割引导的局部‑全局边界条件与逐块独立量化统一到自回归框架中，实现了对全局形状一致性和局部细节保真度的兼顾。

**主要结果**：在 ShapeNet、Thingi10K 和 Objaverse 三个数据集上，MeshMosaic 在倒角距离（CD）、法向一致性（NC）、F1 分数等几何指标上全面超越 DeepMesh、BPT、MeshAnythingV2 等 SOTA 方法（例如 ShapeNet CDL2 为 0.019 vs DeepMesh 的 0.060）。在包含27位专业用户的调研中，MeshMosaic 在整洁度、艺术性、相似度和细节恢复四项主观评价上均获最高评分（2.78–2.91分），远超第二名 BPT（1.04–1.08分）。此外，MeshMosaic 能够稳定生成超过100K三角形的网格，而先前方法通常仅支持约8K面，显著提升了艺术家网格生成的规模上限与视觉质量。

## 背景与动机

### 艺术家网格生成的核心瓶颈

高质量三维内容创作在游戏、影视、虚拟现实等领域需求激增，但手工建模成本高昂。近年来，基于Transformer的自回归网格生成方法尝试直接从点云等条件输入中自动生成精细的三角网格，代表工作包括**DeepMesh**（Zhao et al., arXiv 2025）、**MeshAnythingV2**（Chen et al., arXiv 2024）等。然而，这些方法面临一个根本性瓶颈：**长序列建模困难**。

自回归Transformer将网格表示为面片（face）token序列，其序列长度与网格面数成正比。当目标网格超过约8K面时，序列长度急剧膨胀，导致两个致命问题：
1. **计算复杂度平方级增长**：自注意力机制的内存和计算开销随序列长度呈$O(n^2)$增长，使高面数网格的训练和推理变得不可行。
2. **有限量化分辨率**：完整网格被统一缩放到固定的$512^3$量化空间，面数越高，每个面的量化精度越低，精细几何细节被“平均化”丢失。

这导致现有方法生成的网格面数通常被限制在~8K左右，无法忠实地还原艺术家创作的高分辨率网格（通常超过100K面）中的结构化密度模式与锐利边缘细节。

### 现有方法的尝试与不足

为缓解长序列问题，近期工作进行了多种尝试：
- **分块策略**：**BPT**通过将网格分块并对面片进行标记化来缩短序列长度，但缺乏有效的块间一致性约束，导致拼接处出现裂缝和密度不对称。
- **树状邻接建模**：**TreeMeshGPT**尝试用树结构建模面片邻接关系，但树结构的表达能力有限，难以捕捉复杂拓扑。
- **相邻面片标记化**：**MeshAnythingV2**利用相邻面片信息辅助生成，但仍受限于整体序列长度，无法规模化到高面数网格。

这些方法的共同缺陷在于：**未能将“局部高精度生成”与“全局无缝组装”有效解耦**。它们要么牺牲局部细节换取全局序列可行性，要么在局部生成时丢失全局上下文导致拼接失败。

### 核心洞察：马赛克艺术的启示

本文的核心洞察来源于**马赛克艺术**：一幅完整的马赛克画作由大量独立的小块（tesserae）拼接而成，每块承载局部图案，但通过相邻块之间的边界对齐和全局构图约束，最终形成连贯的整体画面。

将这一思想迁移到网格生成中，MeshMosaic提出：**将完整网格分解为多个语义有意义的局部面片（patch），每块面片在共享边界条件和全局上下文的双重约束下独立进行高分辨率量化与自回归生成，再通过位移对齐组装为完整网格**。这一“局部到全局组装”策略从根本上突破了长序列瓶颈——每块面片仅需处理局部token序列（~9K长度），但通过边界条件传播和全局点云特征注入，保证了跨面片的空间一致性与全局形状保真度。

该框架的关键优势在于：
- **等效高分辨率**：每块面片独立缩放到$[0,1]$并量化到$512^3$，合并后等效分辨率远超单次全局量化。
- **规模化能力**：面片数量可随网格复杂度自适应增长（训练时通过$\mathcal{N}_{\mathrm{seg}} = \frac{\mathcal{N}_{f}}{2000} \times \lambda_{\mathrm{rand}}$动态计算），支持超过100K面的网格生成。
- **边界无缝性**：通过GRU编码的边界条件token拼接到当前面片序列前端，使自注意力机制显式感知邻接面片的几何状态，配合位移对齐消除局部量化偏差。

## 核心创新

MeshMosaic 的核心创新在于将“马赛克艺术”的局部‑全局组装思想引入自回归网格生成，从根本上突破了 Transformer 长序列瓶颈对网格面数的限制。与一次性自回归生成完整网格的基线方法（如 **DeepMesh**，Zhao et al., arXiv 2025）不同，MeshMosaic 将网格生成分解为局部面片（patch）的逐块生成与全局组装，实现了四个关键机制的变化（changed slots）。

### 1. 局部到全局的分块生成策略

传统自回归方法（如 DeepMesh）直接对完整网格进行一次性生成，其序列长度随面数线性增长，导致超过约 8K 面时生成质量急剧下降。MeshMosaic 将这一任务分解为**逐块自回归生成**过程：每个面片独立进行高分辨率量化与生成，再通过位移对齐组装为完整网格。面片按广度优先搜索（BFS）顺序生成，从空间最低点出发，确保每个面片至少与一个已生成面片相邻，从而传播边界信息。这种策略使得 MeshMosaic 能够稳定生成超过 100K 三角面的高保真网格，远超先前方法的能力边界（Figure 1）。

### 2. 边界条件与局部‑全局双重点云特征的条件输入

基线方法仅使用完整形状的点云特征作为生成条件，缺乏对相邻区域几何连续性的显式建模。MeshMosaic 引入了两个关键的条件机制：

- **边界条件**：对于每个待生成面片，从前一邻接面片中选取 512 个空间最近三角面片，经 GRU 网络编码后拼接到当前面片的 token 序列前端。这使得自注意力机制能够直接融合边界上下文，确保跨面片的几何连续性。
- **局部‑全局双重点云特征**：使用冻结的 Michelangelo 编码器分别提取当前面片点云（局部特征）和完整形状点云（全局特征），与 GRU 边界特征拼接后送入 Transformer。全局特征维持整体形状一致性，局部特征捕捉面片内的精细几何细节。

消融实验（Figure 13）验证了这些设计的必要性：移除边界条件编码导致面片接缝处出现明显裂缝和密度不对称；移除全局点云特征导致显著形变与坍塌；取消自注意力中的边界令牌拼接则引起面片重叠和自相交。

### 3. 面片独立的高分辨率量化

基线方法将整个网格统一量化到 512³ 分辨率，对于高面数网格而言，每个顶点的有效量化精度随网格规模增大而稀释。MeshMosaic 将每个面片独立缩放到 [0,1] 区间并量化到 512³ 分辨率，合并后等效分辨率远高于全局量化方案。这一设计使得每个局部面片都能充分利用量化空间，忠实还原精细几何细节。

### 4. 自适应训练分割策略

训练时，MeshMosaic 采用随机 Voronoi 分割替代固定的完整网格输入，面片数量根据面数动态计算：

$$\mathcal{N}_{\mathrm{seg}} = \frac{\mathcal{N}_{f}}{2000} \times \lambda_{\mathrm{rand}}$$

其中 $\lambda_{\mathrm{rand}} \in [0.5, 2.5]$ 为随机因子。这一策略使得每块面片经 token 化后的序列长度接近窗口大小（9K），在提升训练效率的同时增强了模型对不同分割模式的泛化能力。推理时则使用 PartField 进行语义分割，获得具有自然边界的面片，产生更干净、更连贯的网格边界。

### 创新总结

上述四个 changed slots 协同作用，形成了“边界条件约束下的局部高精度生成 + 全局上下文引导下的无缝组装”这一核心范式。其根本洞察在于：**网格生成的难点不在于整体形状的宏观结构，而在于局部几何细节的精细还原与跨区域连续性**。通过将长序列问题转化为多个短序列的并行约束生成问题，MeshMosaic 在 0.5B 参数量级下取得了超越更大规模商业模型（如 Hunyuan3D）的几何保真度和用户偏好评分。

## 整体框架

MeshMosaic 的核心思想是将一个完整的艺术家网格生成任务分解为“先分割、再逐块生成、最后粘合”的局部到全局自回归流程。该流程从根本上绕开了传统 Transformer 自回归网格生成中长序列瓶颈与有限量化分辨率之间的矛盾，使模型能够稳定地产出超过 100K 三角面的高保真网格。

### 推理流水线

推理时的完整流水线如图 5 所示，包含五个关键阶段：

1. **语义面片分割**：给定输入形状的点云，首先使用 **PartField** 对其进行语义分割，得到一组具有自然边界的局部区域（面片）。与随机分割相比，语义分割能产生更干净、更连贯的网格边界，提升最终网格的美学质量（见消融实验，Fig. 16）。
2. **面片排序**：所有面片按广度优先搜索（BFS）顺序排列，起始点为空间坐标最低的面片。这一排序策略确保每个待生成的面片至少与一个已生成的面片相邻，从而能够接收有效的边界条件信息。
3. **逐块自回归生成**：按照 BFS 顺序，对每个面片独立执行高分辨率量化与自回归生成。每个面片在生成时接收三类条件信号：来自已生成邻接面片的边界条件、当前面片的局部点云特征、以及完整形状的全局点云特征。生成器基于 Hourglass Transformer 逐 token 输出该面片的三角网格。
4. **位移对齐与粘合**：由于每个面片在生成前被独立缩放到 [0,1] 区间并量化到 512³ 分辨率，其绝对空间位置会偏离原始坐标。系统通过计算边界条件面片的位移量，对当前生成面片进行整体平移，消除局部量化带来的位置偏差，实现无缝拼接。
5. **全局组装**：将所有已生成并对齐的面片合并，得到最终的完整艺术家网格。

### 单块生成架构

单个面片的生成架构（图 7）是 MeshMosaic 的核心计算单元，其输入输出流如下：

- **输入**：
  - 当前面片的局部点云
  - 完整形状的全局点云
  - 来自已生成邻接面片的边界三角面片（选取空间最近邻的 512 个三角面片）
- **特征提取**：
  - 局部点云与全局点云分别通过冻结的 **Michelangelo** 编码器提取特征
  - 边界三角面片经 token 化后，由 **GRU** 网络编码为边界条件特征
- **特征融合**：
  - 全局特征与局部特征与 GRU 边界特征拼接
  - 边界条件 token 被拼接到当前面片 token 序列的前端，使自注意力机制能够直接融合边界上下文
- **生成**：
  - 拼接后的序列送入自回归 Hourglass Transformer，逐 token 生成当前面片的三角网格

### 训练策略

训练阶段采用与推理一致的局部到全局框架，但面片分割方式有所不同：

- **随机 Voronoi 分割**：训练时使用最远点采样加 Voronoi 分解对网格进行随机分割，而非语义分割。面片数量由自适应公式 $\mathcal{N}_{\mathrm{seg}} = \frac{\mathcal{N}_{f}}{2000} \times \lambda_{\mathrm{rand}}$ 动态确定，其中 $\lambda_{\mathrm{rand}} \in [0.5, 2.5]$ 随机采样。这使得每块面片经 token 化后的序列长度接近窗口大小（9K tokens），在提升训练效率的同时增强了数据多样性。
- **渐进式训练**：训练分阶段引入新增模块——先训练基础生成能力，再逐步接入 GRU 边界编码器和全局特征输入，两个新增模块均通过零初始化线性层连接，以保证训练稳定性。

### 与基础架构的关系

MeshMosaic 以 **DeepMesh**（Zhao et al., arXiv 2025）作为基础自回归生成架构，但对其生成策略、条件输入、量化分辨率和训练分割方式进行了四个关键槽位的改造（详见方法谱系部分）。这种改造使得模型在保持与 DeepMesh 相当的每 token 推理时间（0.024 s/token vs 0.025 s/token，Table 3）的同时，实现了从 ~8K 面到 100K+ 面的规模化跨越。

### 补充图表

![[assets/figures/papers/paper_list_l2545_https_arxiv_org_abs_2509_19995/figures/007_Figure_7.jpg]]
*Figure 7: The workflow of MeshMosaic for generating a single patch. Both global and local point cloud features are extracted by a locked Michelangelo [51] encoder. For each patch, the nearest boundary mesh is identified, tokenized, and concatenated before the target mesh token sequence. The GRU network encodes boundary tokens, which are then combined with global and local features and fed into an autoregressive hourglass transformer for mesh generation*

## 核心模块与公式推导

### 整体框架：局部到全局的自回归组装

MeshMosaic 的核心思路是将完整网格生成任务分解为**逐块生成、全局组装**的过程。推理时，首先利用 PartField 对输入形状进行语义分割，得到具有自然边界的面片（patch）；随后按广度优先搜索（BFS）顺序，从空间最低点出发逐块生成；每块面片在边界条件与全局‑局部点云特征的引导下，独立完成高分辨率量化与自回归生成，最后通过位移对齐粘合为完整网格（Figure 5、Figure 7）。

这一框架从根本上绕开了传统自回归网格生成的长序列瓶颈：每个面片的 token 序列长度可控，且每块独立缩放到 $[0,1]$ 区间并以 $512^3$ 分辨率量化，合并后等效分辨率远高于单次全局量化的 $512^3$。

### 核心模块一：语义面片分割与排序

**语义面片分割 (Semantic Patch Segmentation)**。推理时使用 PartField 对输入形状进行语义分割，将网格划分为具有自然语义边界的面片。相比随机分割，语义分割能产生更干净、更连贯的网格边界，提升美学质量（消融实验证实，见 Figure 16）。

**面片排序 (Patch Ordering)**。生成顺序按 BFS 遍历，从空间最低点面片开始。这一设计确保每个待生成面片至少与一个已生成面片相邻，从而可以从前序面片中提取边界条件信息，实现无缝衔接。

### 核心模块二：边界条件构建与注入

边界条件是 MeshMosaic 实现面片间无缝拼接的关键机制。对于当前待生成面片，从其所有已生成的相邻面片中，选取空间上最近的 **512 个三角面片**作为边界条件。这些三角面片经 tokenizer 标记化后，送入一个**门控循环单元（GRU）网络**进行编码，得到边界特征表示。

边界条件通过两种方式注入生成过程：
1. **序列拼接**：将边界条件 token 拼接到当前面片 token 序列的前端，使 Hourglass Transformer 的自注意力机制能够直接融合边界上下文；
2. **特征融合**：GRU 编码的边界特征与全局‑局部点云特征拼接后，一同送入 Transformer。

消融实验表明，移除边界条件编码（Ours w/o BD）会导致面片接缝处出现明显裂缝和密度不对称；取消自注意力中的边界令牌拼接（Ours w/o SA）则使面片出现重叠和自相交（Figure 13）。

### 核心模块三：局部‑全局特征提取

MeshMosaic 同时利用**局部点云**（当前面片对应的点云子集）和**全局点云**（完整形状点云）作为条件输入。两者均通过**冻结的 Michelangelo 编码器**提取特征，该编码器在训练过程中参数固定，仅作为特征提取器使用。

全局特征与局部特征拼接后，再与 GRU 边界特征融合，共同送入自回归 Hourglass Transformer。消融实验证实，移除全局点云特征（Ours w/o GPC）会导致显著形变与坍塌，表明全局上下文对维持整体形状至关重要（Figure 13）。

### 核心模块四：面片粘合

由于每个面片独立缩放到 $[0,1]$ 并量化，其绝对坐标与相邻面片可能存在位移偏差。MeshMosaic 通过计算边界条件面片的位置位移，对当前生成面片进行整体平移对齐，从而消除局部量化带来的位置偏差，实现无缝拼接。

### 关键公式

**自适应面片数量**。训练时，根据网格总面数 $\mathcal{N}_{f}$ 和随机因子 $\lambda_{\mathrm{rand}}$ 动态计算分割出的面片数量：

$$\mathcal{N}_{\mathrm{seg}} = \frac{\mathcal{N}_{f}}{2000} \times \lambda_{\mathrm{rand}}$$

其中 $\lambda_{\mathrm{rand}} \in [0.5, 2.5]$ 随机采样。这一设计使得每块面片经 token 化后的序列长度接近窗口大小（9K），在训练效率与多样性之间取得平衡。训练时采用随机 Voronoi 分割，推理时则替换为语义分割。

**点面比率过滤**。数据预处理阶段，计算点面比 $\Phi_{\mathbf{p/f}}$ 以过滤低质量网格：

$$\Phi_{\mathbf{p/f}} = \frac{\mathcal{N}_{p}}{\mathcal{N}_{f}}$$

过滤 $\Phi > 0.8$ 的网格，以排除过多开放边界的低质量模型（Appendix A.1）。

### 补充图表

![[assets/figures/papers/paper_list_l2545_https_arxiv_org_abs_2509_19995/figures/006_Figure_6.jpg]]
*Figure 6: 2D illustration of patches with BFS order*

![[assets/figures/papers/paper_list_l2545_https_arxiv_org_abs_2509_19995/figures/008_Figure_8.jpg]]
*Figure 8: 2D and 3D Example of our boundary condition*

![[assets/figures/papers/paper_list_l2545_https_arxiv_org_abs_2509_19995/figures/005_Figure_4.jpg]]
*Figure 4: DeepMesh Tokenizer*

## 实验与分析

### 核心定量结果

Table 1 汇总了在 ShapeNet、Thingi10K 和 Objaverse 三个数据集上的几何指标对比。MeshMosaic 在几乎所有指标上取得最优或次优，验证了局部到全局组装策略对几何保真度的显著提升。

![[assets/figures/papers/paper_list_l2545_https_arxiv_org_abs_2509_19995/figures/009_Table_1.jpg]]
*Table 1: Quantitative comparison on ShapeNet [3], Thingi10K [53] and Objaverse [11] datasets. The best scores are emphasized in bold with underlining, while the second best scores are highlighted only in bold*

- **ShapeNet**：CDL2 降至 **0.019**，而 DeepMesh 为 0.060，相对改善约 68%；F1 分数达到 0.929，NC 为 0.973，均位居榜首。
- **Thingi10K**：CDL2 仅为 **0.052**，远低于 MeshAnythingV2 的 2.492 和 BPT 的 0.117；HD 为 0.051，ECD 为 0.017，全面领先。
- **Objaverse**：CDL2 为 **0.387**，DeepMesh 为 1.712，MeshAnythingV2 为 0.693，表明在多样化开放类别上同样具备鲁棒优势。

所有对比均基于 0.5B 参数量级、100 个随机测试样本，并采用公开代码或官方模型，确保了公平性。商用强化版本 Hunyuan3D 因未开源且无法批量评估，未纳入定量对比。

### 用户调研

Table 2 报告了 27 位专业用户在整洁度（Neatness）、艺术性（Artistry）、相似度（Similarity to GT）和细节恢复（Detail Recovery）四个维度上的投票评分。MeshMosaic 在所有类别中均获最高分（2.780–2.910），远超第二名 BPT（1.040–1.084）和 DeepMesh（0.836–0.940）。这表明局部量化与语义分割引导的面片组装策略不仅提升了数值指标，更在人类感知层面产生了显著可辨识的质量优势。

![[assets/figures/papers/paper_list_l2545_https_arxiv_org_abs_2509_19995/figures/012_Table_2.jpg]]
*Table 2: User study with SOAT methods aggregated from 27 professional participants in four categories: Neatness, Artistry, Similarity to Ground Truth, and Detail Recovery. The best scores are emphasized in bold with underlining, while the second best scores are highlighted only in bold*

### 消融实验

Figure 13 系统拆解了三个关键设计的作用，每个消融变体均出现特征性退化：

![[assets/figures/papers/paper_list_l2545_https_arxiv_org_abs_2509_19995/figures/015_Figure_13.jpg]]
*Figure 13: Ablation for boundary condition and global point cloud*

- **移除全局点云特征（w/o GPC）**：在全量数据集上出现显著形变与坍塌，证实全局上下文对维持整体形状结构不可或缺。
- **移除边界条件编码（w/o BD）**：面片接缝处产生明显裂缝和密度不对称，说明 GRU 编码的 512 最近邻边界三角面片是保证跨面片连续性的核心机制。
- **取消自注意力中的边界令牌拼接（w/o SA）**：面片出现重叠和自相交，表明将边界条件令牌拼接到目标序列前端、使自注意力机制融合边界上下文，对空间一致性至关重要。

此外，Figure 16 的对比显示，推理时采用 PartField 语义分割相比随机分割能产生更干净、更连贯的网格边界，提升了美学质量。Table 3 的效率分析表明，借助 KV‑cache 加速，MeshMosaic 的平均每 token 推理时间（0.024 s）与 DeepMesh（0.025 s）几乎持平，仅在训练时因窗口化策略引入少量额外开销。

![[assets/figures/papers/paper_list_l2545_https_arxiv_org_abs_2509_19995/figures/021_Figure_16.jpg]]
*Figure 16: Comparison of random and semantic segmentation*

![[assets/figures/papers/paper_list_l2545_https_arxiv_org_abs_2509_19995/figures/020_Table_3.jpg]]
*Table 3: Comparison of runtime performance between DeepMesh and our method variants. The table reports the training time per window (9K tokens) and the inference time per token in seconds*

### 失败模式与局限性

尽管 MeshMosaic 在整体指标上表现优异，仍存在以下典型失效场景：

- **远距离对称性丢失**：边界条件主要作用于局部邻接面片，对于人形模型等具有远距离对称结构的形状，双臂等部位可能产生轻微不对称（Figure 10）。当前框架未显式建模全局对称约束。
- **高面数推理延迟**：对于超过 100K 面的复杂网格，推理时间可能长达数小时（约 0.024 s/token），难以满足工业应用的实时需求。
- **边界条件容量限制**：仅选取 512 个最近邻三角面片作为边界条件，在面片边界极长或拓扑复杂时可能不足以传递完整的几何约束信息。

![[assets/figures/papers/paper_list_l2545_https_arxiv_org_abs_2509_19995/figures/011_Figure_10.jpg]]
*Figure 10: Symmetry limitation*

这些局限性指向未来可能的改进方向：引入全局感知机制以耦合远处对称部分、探索自适应量化方案以提升边缘细节、以及通过多节点同步生成降低高面数网格的推理延迟。

### 补充图表

![[assets/figures/papers/paper_list_l2545_https_arxiv_org_abs_2509_19995/figures/002_Figure_2.jpg]]
*Figure 2: Comparison with existing state-of-the-art approaches, including both academic and commercial models. MeshMosaic achieved better quality with a smaller model size*

![[assets/figures/papers/paper_list_l2545_https_arxiv_org_abs_2509_19995/figures/017_Figure_14.jpg]]
*Figure 14: Detail recovery comparison*

## 方法谱系与知识库定位

### 1. 方法谱系：在自回归网格生成演进中的位置

MeshMosaic 直接继承并突破了 **DeepMesh**（Zhao et al., arXiv 2025）的技术框架。DeepMesh 通过强化学习与人类偏好对齐，首次实现了基于自回归 Transformer 的艺术家网格生成，但其“一次性生成完整网格”的策略面临严重的长序列瓶颈——当网格面数超过约 8K 时，Transformer 的自注意力计算开销和有限量化分辨率（统一 512³）导致精细几何细节大量丢失。MeshMosaic 将这一瓶颈识别为核心问题，并提出“局部到全局组装”范式作为因果性解决方案。

在更广泛的方法谱系中，MeshMosaic 与以下并行工作形成对比：

- **MeshAnythingV2**（Chen et al., arXiv 2024）：采用相邻面片标记化策略，试图通过局部上下文改进生成质量，但本质上仍是对完整网格进行一次性编码，未从根本上解决长序列问题。在 Thingi10K 数据集上，其 CDL₂ 指标为 2.492，而 MeshMosaic 仅为 0.052，差距达两个数量级。
- **BPT**：通过分块与面片化标记化缩短序列长度，是“分而治之”思路的早期尝试。然而，BPT 缺乏边界条件引导和全局上下文约束，导致面片间出现明显接缝和密度不对称。用户调研中 BPT 的整洁度评分仅为 1.040，MeshMosaic 则达到 2.780。
- **TreeMeshGPT**：基于树状邻接关系建模自回归生成，试图通过结构化拓扑先验提升效率，但其树状结构难以处理任意拓扑的复杂网格，适用范围受限。

MeshMosaic 的关键突破在于将“马赛克艺术”的组装思想系统化地引入自回归网格生成：每个局部面片在**边界条件**（GRU 编码的 512 个最近邻边界三角面片）、**全局点云特征**（冻结的 Michelangelo 编码器）和**局部点云特征**的三重约束下独立生成，再通过位移对齐实现无缝拼接。这一设计使量化分辨率从全局 512³ 等效提升为每块独立 512³，从而突破 8K 面的上限，实现超过 100K 三角面的高保真生成。

### 2. 适用边界与条件依赖

MeshMosaic 的性能优势依赖于若干关键条件：

1. **语义分割质量**：推理阶段的 PartField 语义分割决定了面片的自然边界。当输入形状的语义结构模糊或 PartField 分割失败时，面片边界可能穿越几何特征区域，导致接缝处出现伪影。消融实验表明，语义分割相比随机分割能产生“明显更干净、更连贯的网格边界”，但 PartField 本身在非标准形状上的泛化能力未经验证。

2. **点云密度与完整性**：局部和全局点云特征均依赖 Michelangelo 编码器。若输入点云过于稀疏或存在大面积缺失，全局上下文的约束力将显著下降。消融实验中移除全局点云特征（Ours w/o GPC）导致“显著形变与坍塌”，证实了这一依赖的敏感性。

3. **面片数量与序列长度平衡**：训练时通过自适应面片数量公式 $\mathcal{N}_{\mathrm{seg}} = \frac{\mathcal{N}_{f}}{2000} \times \lambda_{\mathrm{rand}}$（$\lambda_{\mathrm{rand}} \in [0.5, 2.5]$）确保每块面片的 token 序列长度接近 9K 的窗口大小。当面片划分过细或过粗时，训练效率与生成质量之间的平衡可能被打破。

4. **计算资源需求**：训练需在 32 块 NVIDIA H20 96GB GPU 上运行 7 天，推理时单 token 耗时约 0.024 秒。对于超过 100K 面的复杂网格，完整生成可能需要数小时，难以满足实时或交互式应用场景。

### 3. 已知局限与失效模式

1. **远处对称性耦合不足**：边界条件主要作用于局部邻接面片，对于空间上分离但语义对称的部位（如人形模型的双臂），缺乏显式的全局对称约束。论文明确指出“远处对称部位可能产生轻微不对称”（Figure 10），这是当前框架的结构性局限。

2. **推理延迟与面数线性增长**：尽管 KV-cache 使每 token 推理时间与 DeepMesh 相当（0.024 s/token vs 0.025 s/token），但总推理时间随面数线性增长。对于 100K+ 面的网格，单模型生成时间可能长达数小时，限制其在工业管线中的实用性。

3. **边界条件容量限制**：当前仅选取 512 个最近邻三角面片作为边界条件，对于拓扑复杂或边界曲率变化剧烈的区域，这一固定容量可能不足以传递充分的几何约束信息。消融实验中移除边界条件编码（Ours w/o BD）导致“面片接缝处出现明显裂缝和密度不对称”，但并未探索更大边界窗口的影响。

4. **未覆盖的失效场景**：论文未系统评估 MeshMosaic 在以下场景的表现：(a) 极端非流形网格或具有复杂内部结构的模型；(b) 输入点云存在严重噪声或离群点的情况；(c) 跨类别泛化（例如在 ShapeNet 上训练后在 Thingi10K 上零样本推理）。这些边界条件下的鲁棒性需要额外验证。

### 4. 开放问题与未来方向

1. **全局感知机制的低成本引入**：如何在不过度增加序列长度或计算开销的前提下，引入全局感知机制以加强对远处对称部分的耦合？可能的路径包括轻量级全局潜在编码、图神经网络消息传递，或显式对称先验注入。

2. **自适应量化与分辨率分配**：当前所有面片统一使用 512³ 分辨率量化，但不同区域的几何复杂度差异显著。能否设计几何复杂度驱动的可变分辨率方案，在平坦区域降低量化精度以加速生成，在细节丰富区域提升精度以保证质量？

3. **并行面片生成**：当前 BFS 顺序要求每个面片等待其邻接面片完成才能获取边界条件。是否可以通过多节点同步生成（同时生成多个非邻接面片，仅在边界处进行后验对齐）显著降低高面数网格的推理延迟？这需要解决边界一致性维护的挑战。

4. **框架迁移与泛化**：MeshMosaic 的局部-全局组装范式是否可扩展到其他需要长序列建模的 3D 任务？例如纹理生成（逐块生成 UV 贴图后拼接）、骨骼蒙皮（逐部件预测蒙皮权重后融合），或大规模场景生成（逐区域生成后对齐）。这些迁移场景中的边界条件定义和全局约束形式需要重新设计。

5. **数据质量与面片分割的联合优化**：论文使用点面比率 $\Phi_{\mathbf{p/f}} = \mathcal{N}_{p} / \mathcal{N}_{f}$ 过滤 $\Phi > 0.8$ 的低质量网格，但未探讨面片分割策略与数据质量之间的交互影响。是否存在最优的分割粒度与数据过滤阈值的联合设计方案？

6. **与商业系统的对比深度**：论文仅定性展示了与商用模型 Hunyuan3D 的视觉对比（Figure 2），未进行定量评估。随着工业界网格生成模型的快速发展，建立标准化的跨系统评测基准将成为社区的重要需求。

## 原文 PDF

![[paperPDFs/CVPR_2026/MeshMosaic_Scaling_Artist_Mesh_Generation_via_Local_to_Global_Assembly.pdf]]
