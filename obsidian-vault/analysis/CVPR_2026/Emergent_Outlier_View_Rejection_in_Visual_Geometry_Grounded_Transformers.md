---
title: Emergent Outlier View Rejection in Visual Geometry Grounded Transformers
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Emergent_Outlier_View_Rejection_in_Visual_Geometry_Grounded_Transformers.pdf
project_link: https://cvlab-kaist.github.io/RobustVGGT
code_link: null
aliases:
- RRRF
- EOVRVGGT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: VGGT内部表示（注意力图和特征相似度）在深层（尤其是最后一层）自发地抑制几何不一致的干扰视图。
primary_logic: 利用VGGT最后一层的跨视图注意力或特征余弦相似度作为视图相关性分数，通过一个固定的全局阈值过滤干扰视图，无需额外训练或修改架构。
claims:
- VGGT虽然无显式离群拒绝机制，但其内部表示可固有区分干扰图像。
- 最后一层展现最强的干净/干扰视图分离，形成涌现的噪声抑制。
- 通过单次全局阈值对注意力/特征分数进行截断，即可在不微调条件下实现有效视图过滤。
- 提出的简单计分方案（RobustVGGT）使用一个共享于所有数据集的固定阈值。
---

# Emergent Outlier View Rejection in Visual Geometry Grounded Transformers

> [!tip] 核心洞察
> 利用VGGT最后一层的跨视图注意力或特征余弦相似度作为视图相关性分数，通过一个固定的全局阈值过滤干扰视图，无需额外训练或修改架构。

| 字段 | 内容 |
|------|------|
| 中文题名 | 视觉几何基础Transformer中的涌现性离群视角拒绝 |
| 英文题名 | Emergent Outlier View Rejection in Visual Geometry Grounded Transformers |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.04012) · [Project](https://cvlab-kaist.github.io/RobustVGGT) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | RobustVGGT (含RobustVGGT‑A 和 RobustVGGT‑F 变体) |
| Dataset | Phototourism, ETH3D, On-the-Go |

> [!tip] 效果简介
> - Phototourism 上，ATE↓ 0.2641 (RobustVGGT‑F, Small) vs 0.3068 (VGGT, Small) (-0.0427)。
> - ETH3D 上，AbsRel↓ 0.0319 (RobustVGGT‑F, Large) vs 0.0403 (VGGT, Large) (-0.0084)。
> - On-the-Go 上，ATE↓ 0.0521 (RobustVGGT‑F, Small) vs 0.0754 (VGGT, Small) (-0.0233)。

## 概要

**问题瓶颈**：前馈3D重建模型（如VGGT，Wang et al., CVPR 2025）在真实场景中面临一个关键脆弱性——当输入的图像集合包含噪声或场景无关的干扰视图时，模型缺乏显式的离群视图剔除机制，导致重建质量严重退化。VGGT虽然能预测逐点置信度图来降权不可靠深度，但这一后验信号仅作用于点级别，无法在视图层面过滤干扰图像，使得虚假内容仍会污染恢复的几何结构。

**核心发现**：尽管VGGT未经过任何显式的离群标签或过滤目标训练，其内部表示却涌现出视图选择性——跨视图注意力图和特征相似度在深层（尤其是最后一层）自发地抑制几何不一致的干扰视图。逐层分析表明，干净视图与干扰视图之间的分离程度随网络深度增加而增强，在最终层达到峰值，形成一种涌现的噪声抑制行为。

**方法定位**：基于上述发现，RobustVGGT提出了一种无需训练、无需修改架构的视图过滤策略。该方法从VGGT最后一层的内部表示中提取两种探针信号——跨视图注意力分数（RobustVGGT-A）和特征余弦相似度分数（RobustVGGT-F）——作为视图相关性度量，并通过一个固定全局阈值进行硬过滤，仅保留几何一致的视图后重新馈入VGGT完成重建。整个过程仅需两趟前向传播，无需额外监督或微调。

**方法谱系与知识库定位**：该工作处于前馈3D重建与鲁棒性增强的交叉点。与需要优化迭代的MASt3R-SfM（Duisterhof et al., 3DV 2025）不同，RobustVGGT保持了前馈模型的推理效率；与依赖外部视觉位置识别模型预过滤的方法（如MegaLoc+VGGT, Berton & Masone, CVPR 2025；或DINOv3+VGGT, Simeoni et al., arXiv 2025）相比，RobustVGGT直接利用VGGT自身的内部表示，避免了引入额外模型和领域偏移。其核心创新在于发现并利用了大模型中涌现的内部过滤能力，而非设计新的过滤模块。

**主要结果**：在Phototourism、ETH3D和On-the-Go等多个数据集上，RobustVGGT在不同噪声水平下均一致优于未过滤的VGGT基线及其他视图选择方法。例如，在Phototourism的Small噪声设置下，RobustVGGT-F将ATE从0.3068降至0.2641；在ETH3D上，Large模型将AbsRel从0.0403降至0.0319。该方法使用一个跨数据集共享的固定阈值（注意力阈值τ=0.05，特征相似度阈值τ=0.65），展现出良好的泛化性。



### 前馈式3D重建的瓶颈：隐式假设与真实场景的错配

近年来，以 **VGGT**（Wang et al., CVPR 2025）为代表的前馈式视觉几何基础模型在3D重建领域取得了显著进展。这类模型通过Transformer架构直接从多视图图像集合中回归相机位姿与稠密深度图，无需传统的束调整（Bundle Adjustment）等迭代优化步骤，展现出极高的推理效率。然而，这一效率优势建立在一个隐含的前提之上——输入图像集合中的所有视图均来自同一场景且几何上相互一致。

真实世界的图像采集过程往往难以满足这一理想假设。无论是通过关键词检索从互联网获取的图像，还是用户随意拍摄的照片集，都不可避免地混入与目标场景无关的“干扰视图”（distractor images）。这些干扰图像可能来自完全不同的地点、拍摄对象或时间节点，在几何上与干净视图不存在任何共视关系。

### 现有机制的失效：点级置信度无法替代视图级过滤

VGGT并非完全没有噪声应对能力。如图2所示，VGGT在推理过程中会预测逐像素的置信度图，用于在深度融合阶段降低不可靠深度值的权重。然而，这一机制存在根本性的局限：**它仅在点级别（point level）运作，而非在视图级别（view level）执行过滤**。

这意味着，即使某幅干扰图像完全不包含任何有效的场景几何信息，VGGT仍会尝试为其重建点云和位姿。这些“强行重建”的虚假几何内容随后会污染整个场景的融合结果，导致重建中出现明显的噪声几何和视觉伪影（参见图1a）。简言之，点级置信度是一种“事后补救”信号，无法阻止干扰视图在管道源头就造成污染。

### 现有应对方案及其代价

针对前馈式重建中的干扰视图问题，研究者已尝试多种预处理策略：

- **视觉位置识别（VPR）预过滤**：如 **MegaLoc + VGGT**（Berton & Masone, CVPR 2025）利用VPR模型在重建前筛选视图。但VPR模型通常需要针对每个数据集独立调参，且部分方案依赖oracle信息（如已知干净图像数量），泛化能力受限。
- **全局描述子选择**：如 **DINOv3 + VGGT**（Simeoni et al., arXiv 2025）使用DINOv3的全局特征进行视图选择。类似地，**DINOv2† + VGGT**（Oquab et al., arXiv 2023）直接复用VGGT编码器中的DINOv2特征。
- **优化式重建管线**：如 **MASt3R-SfM**（Duisterhof et al., 3DV 2025）基于MASt3R编码特征构建场景图并执行优化重建，但其计算开销远高于纯前馈方案。

这些方案要么引入了额外的模型和调参负担，要么牺牲了前馈方法的速度优势。一个核心问题由此浮现：**能否在不增加外部模块、不修改架构、不进行额外训练的前提下，赋予前馈式重建模型内在的干扰视图拒绝能力？**

### 本文动机：挖掘模型内部的涌现性视图选择行为

本文的核心发现为这一问题提供了出人意料的答案。通过对VGGT内部表示的逐层分析，我们发现：**尽管VGGT从未接受过任何离群标签或噪声过滤目标的训练，其深层表示（尤其是最后一层）自发地展现出对几何不一致视图的抑制行为**。

具体而言，我们测量了VGGT所有层中干净视图与干扰视图在跨视图注意力图和特征相似度上的分离程度。如图3所示，这种分离随着网络深度的增加而持续增强，并在最后一层达到峰值——形成了一种“涌现性的噪声抑制”（emergent noise suppression）现象。图4进一步可视化了这一行为：在最后一层的注意力图和特征相似度图中，干扰视图（红色框标记）的响应被显著压低，而干净视图则保持高响应。

这一发现揭示了一个关键洞察：**VGGT已经“学会”了区分相关视图与干扰视图，只是这一能力隐藏在其内部表示中，未被显式利用。** 基于此，本文提出 **RobustVGGT**——一种完全无需训练的视图过滤策略，仅通过提取VGGT最后一层的注意力分数或特征余弦相似度作为视图相关性度量，并施加一个固定的全局阈值，即可在推理阶段有效剔除干扰视图，显著提升重建鲁棒性（如图1b所示）。



## 核心方法与创新机理

本文的核心创新在于**发现并利用前馈3D重建模型VGGT内部表示的“涌现性”离群视图抑制能力**，构建了一个完全无需训练、无需修改架构的视图过滤机制。这一机制围绕两个关键的 **changed slots** 展开：

### 1. 输入视图集的过滤式重构（Input View Set Slot）

**Baseline（VGGT）**：将所有输入图像（包括大量几何不一致的干扰视图）直接馈入VGGT的Transformer编码器-解码器流水线。模型虽然能预测逐点置信度图来降权不可靠深度，但这一后处理信号仅作用于点级别，无法在视图层面剔除干扰源，导致干扰视图的虚假内容仍会污染重建几何（见Figure 2）。

**Proposed（RobustVGGT）**：引入一个**两阶段推理范式**。第一阶段，将完整图像集馈入VGGT，提取其最后一层（ℓ⋆）的跨视图注意力图和中间密集特征；第二阶段，基于这些内部信号计算每幅图像相对于查询视图的相关性分数，通过固定全局阈值 τ^O 进行硬过滤，仅保留满足条件的视图构成干净上下文集合 ϕ(i)，再重新运行VGGT主干网络产生最终位姿和深度预测：

> *“We finally re-run the backbone on {I_j}_{j∈ϕ(i)} to obtain (P_i, D_i, X_i, C_i) using only spatially and geometrically consistent views.”*

这一改变将VGGT从“被动接受所有输入”转变为“主动选择几何一致视图”，是性能提升的核心来源。

### 2. 离群拒绝机制的从无到有（Outlier Rejection Mechanism Slot）

**Baseline（VGGT）**：**无显式视图级离群剔除机制**。VGGT的训练目标仅关注干净匹配下的几何估计，未引入任何噪声感知训练或离群标签，因此面对含干扰视图的输入时缺乏结构化的防御手段。

**Proposed（RobustVGGT）**：设计了两种基于内部表示的**无训练计分方案**，并统一通过单阈值硬过滤实现离群拒绝：

- **RobustVGGT‑A（注意力计分）**：对最后一层多头平均注意力在空间位置 (u,v) 上求均值，得到视图 i 与 j 之间的注意力分数：

$$r_{ij}^{att} = \frac{1}{HW} \sum_{u,v} A_{ij}^{(\ell^\star)}(u,v)$$

- **RobustVGGT‑F（特征相似度计分）**：对最后一层L2归一化特征图进行空间点乘，产生逐像素相关图 C_{i→j}，再对全图求空间平均，等价于平均余弦相似度：

$$r_{ij}^{feat} = \frac{1}{HW} \sum_{u,v} C_{ij}(u,v)$$

两种方案的过滤规则统一为：

$$\phi(i) = \{ j \mid j = i \text{ or } r_{ij}^O \geq \tau^O \}, \quad O \in \{att, feat\}$$

其中固定全局阈值 τ^att = 0.05，τ^feat = 0.65，**跨数据集共享，无需逐场景调参**。

### 3. 创新机制的核心洞察

上述 changed slots 的有效性根植于一个关键的**涌现行为发现**：VGGT虽然在训练阶段从未接触过离群标签或过滤目标，但其深层表示（尤其是最后一层）自发地学会了对几何不一致视图进行抑制。逐层分析（Figure 3）表明，注意力图和特征相似度在干净视图与干扰视图之间的分离程度随网络深度单调递增，在最后一层达到峰值——这是模型内部涌现出的“噪声抑制”能力。RobustVGGT的本质是将这种隐式能力**显式化、可操作化**，通过极简的阈值截断将其转化为确定性的视图过滤决策。

### 4. 方法边界与未改变部分

值得强调的是，RobustVGGT**未改变**VGGT的以下核心组件：
- Transformer编码器架构与交替注意力层的设计
- 位姿估计和深度预测的解码头
- 模型权重与训练流程

所有改进均通过**外部包装**的方式实现，这使其具有极强的即插即用特性。但同时，当前方法仅执行视图级粗粒度过滤，未涉及token/patch级别的细粒度剔除；且需要两趟前向传播（首次计分、二次重建），增加了推理开销。



RobustVGGT 的整体流程围绕一个核心发现展开：**VGGT 的前馈重建管线无需显式的离群视图剔除机制或噪声感知训练，其深层内部表示已自然具备区分干净视图与干扰视图的能力**。基于这一涌现特性，该方法设计了一个无需训练、无需修改架构的视图过滤策略，整体框架可分为四个主要模块，如 Figure 5 所示。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2512_04012/figures/005_Figure_5.jpg]]
*Figure 5: Framework overview. We compute per-view relevance from VGGT’s internal representations using two probes: (i) crossview attention from query–key projections and (ii) cosine similarity of intermediate dense features. The resulting score*

### 1. VGGT 特征编码与交替注意力

输入为一组可能包含干扰图像的视图集合 $\{I_i\}$。首先将所有图像送入 VGGT 的 Transformer 编码器与交替注意力层，该骨干网络原本用于直接估计相机位姿 $P_i$ 和深度图 $D_i$。在此阶段，模型完成所有层的正向传播，并在每一层产生多尺度注意力图和中间特征图。这些内部信号是后续视图评分的基础，而非直接使用 VGGT 的原始输出。

### 2. 视图评分器：注意力探针与特征相似度探针

从 VGGT 最后一层（记作 $\ell^\star$）提取两种互补的视图相关性信号，构成两个变体：

- **RobustVGGT‑A（注意力分数）**：对最后一层的多头平均注意力图 $A_{ij}^{(\ell^\star)}$ 在空间位置 $(u, v)$ 上求均值，得到视图 $i$ 与 $j$ 之间的注意力分数：

$$r_{ij}^{att} = \frac{1}{HW} \sum_{u,v} A_{ij}^{(\ell^\star)}(u,v)$$

- **RobustVGGT‑F（特征相似度分数）**：对 L2 归一化后的中间特征图向量 $\tilde{F}_i^{(\ell^\star)}$ 和 $\tilde{F}_j^{(\ell^\star)}$ 进行点乘，生成逐像素相关图 $C_{i \to j}(u,v)$，再对整个相关图求空间平均，等价于平均余弦相似度：

$$r_{ij}^{feat} = \frac{1}{HW} \sum_{u,v} C_{ij}(u,v)$$

这两种探针从不同角度捕捉了 VGGT 深层对视图几何一致性的隐式判断：注意力分数反映跨视图的 token 级信息交互强度，特征相似度则衡量密集特征的语义与几何对齐程度。逐层分析表明，干净视图与干扰视图之间的分数差距随网络深度增加而扩大，在最后一层达到峰值，形成涌现的噪声抑制行为。

### 3. 阈值过滤器

基于上述评分，为每幅查询图像 $I_i$ 构建过滤后的上下文视图集合：

$$\phi(i) = \{ j \mid j = i \text{ or } r_{ij}^O \geq \tau^O \}, \quad O \in \{att, feat\}$$

其中 $\tau^O$ 为全局固定阈值。对于 RobustVGGT‑A，$\tau^{att}=0.05$；对于 RobustVGGT‑F，$\tau^{feat}=0.65$。该阈值**在所有数据集上共享，无需逐场景调参**。自身视图始终保留（$j = i$），而分数低于阈值的视图被视为干扰并直接剔除。这一硬过滤机制简洁高效，仅依赖单次阈值截断即可完成视图级离群拒绝。

### 4. 重新推理

过滤完成后，仅使用保留的干净视图集合 $\{I_j\}_{j \in \phi(i)}$ **再次运行 VGGT 骨干网络**，最终输出相机位姿 $P_i$、深度图 $D_i$、3D 点云 $X_i$ 和置信度图 $C_i$。由于输入中已剔除干扰视图，重建质量得到显著提升。

### 设计特点与权衡

整个框架的核心优势在于**零训练成本与零架构修改**：所有操作均复用 VGGT 预训练权重的内部表示，无需引入额外参数、损失函数或微调步骤。代价是**需要两趟前向传播**——首次计算视图分数，第二次进行过滤后的重建，推理开销约为原始 VGGT 的两倍。此外，当前方法仅执行视图级别的粗粒度过滤，不涉及 token 或 patch 级别的细粒度剔除，在极端大规模图像集合下的扩展性仍有待验证。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2512_04012/figures/001_Figure_1.jpg]]
*Figure 1: Motivation. In practice, image sets gathered for 3D reconstruction, e.g., via keyword search, often contain distractors or entirely irrelevant photos. As illustrated in (a), leaving these images unfiltered contaminates the VGGT [56] pipeline, producing noisy geometry and visible artifacts in the final reconstruction. In contrast, our training-free approach, dubbed RobustVGGT, filters views using internal representations within VGGT [56], yielding cleaner, more stable reconstructions, as shown in (b)*



RobustVGGT 的核心思想是利用 VGGT 前馈推理过程中自然涌现的内部表示来区分几何一致的视图与干扰视图，而无需额外训练或架构修改。整个管线由四个关键模块串联构成。

---

### 1. VGGT 特征编码器与交替注意力层

该模块直接复用预训练的 **VGGT**（Wang et al., CVPR 2025）作为冻结的特征提取与跨视图关系建模骨干。VGGT 采用基于 Transformer 的编码器和交替注意力层，对输入图像集合提取多尺度特征图并建模视图间的空间对应关系，最终输出每幅图像的相机位姿 $P_i$ 和深度图 $D_i$。本方法的关键发现是：尽管 VGGT 在训练时未接触任何离群标签或过滤目标，其深层内部表示却自发地展现出视图选择性——对几何不一致的干扰视图产生显著的信号抑制。

---

### 2. 视图评分器

从 VGGT 最后一层（记为 $\ell^\star$）提取两类内部信号，分别构造两种视图相关性分数，对应 RobustVGGT‑A 与 RobustVGGT‑F 两个变体。

**注意力分数（RobustVGGT‑A）**
对最后一层中所有注意力头的平均注意力图在空间位置 $(u,v)$ 上求均值，得到视图 $i$ 与 $j$ 之间的标量注意力分数：

$$r_{ij}^{att} = \frac{1}{HW} \sum_{u,v} A_{ij}^{(\ell^\star)}(u,v) \tag{1}$$

其中 $A_{ij}^{(\ell^\star)}(u,v)$ 为查询视图 $i$ 对上下文视图 $j$ 在空间位置 $(u,v)$ 处的多头平均注意力值，$H \times W$ 为 token 的空间分辨率。

**特征相似度分数（RobustVGGT‑F）**
先对最后一层的密集特征图进行 $\ell_2$ 归一化，得到 $\tilde{F}_i^{(\ell^\star)}(u)$ 和 $\tilde{F}_j^{(\ell^\star)}(v)$，再通过点积构造像素级相关图：

$$C_{i \to j}(u,v) = \tilde{F}_i^{(\ell^\star)}(u) \cdot \tilde{F}_j^{(\ell^\star)}(v) \tag{2}$$

对整个 $H \times W$ 的相关图取空间平均，等价于平均余弦相似度：

$$r_{ij}^{feat} = \frac{1}{HW} \sum_{u,v} C_{ij}(u,v) \tag{3}$$

---

### 3. 阈值过滤器

基于单一全局阈值 $\tau^O$ 对视图进行硬过滤，构建干净上下文集合。对于查询视图 $I_i$，保留其自身及分数不低于阈值的视图：

$$\phi(i) = \{ j \mid j = i \text{ or } r_{ij}^O \geq \tau^O \}, \quad O \in \{att, feat\} \tag{4}$$

实验表明，注意力分数与特征相似度分数可使用**固定的全局阈值**在所有数据集上泛化：RobustVGGT‑A 的最优阈值为 $\tau^{att}=0.05$，RobustVGGT‑F 的最优阈值为 $\tau^{feat}=0.65$（见消融实验 Tab. 3）。此外，可将归一化后的两种分数加权融合为聚合分数 $r_{ij}^{agg} = \alpha \bar{r}_{ij}^{att} + (1-\alpha) \bar{r}_{ij}^{feat}$（$\alpha=0.5$），构成 RobustVGGT‑A+F 变体，进一步提升过滤成功率。

---

### 4. 重新推理

仅使用过滤后的视图集合 $\{I_j\}_{j \in \phi(i)}$ 再次运行 VGGT 骨干网络，获得最终的相机位姿 $P_i$、深度图 $D_i$、3D 点图 $X_i$ 及置信度图 $C_i$。这一“两趟前向”策略是当前方法的主要计算开销来源，但确保了过滤后的重建仅依赖几何与空间一致的视图。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2512_04012/figures/003_Figure_3.jpg]]
*Figure 3: Layer-wise analysis. We measure the gap between clean and distractor views for attention and feature similarity across VGGT’s all layers. The separation grows with depth and peaks at the final layer, indicating emergent noise suppression*



## 实验与关键发现

### 4.1 实验设置与评估协议

为系统验证RobustVGGT在不同噪声条件下的鲁棒性，实验在四个具有不同场景特性的公开数据集上展开：**Phototourism**（多视角旅游地标）、**On‑the‑Go**（手持拍摄序列）、**RobustNeRF**（含动态物体的室内外场景）和**ETH3D**（多视角深度估计基准）。每个评估样本的构造遵循统一协议：从同一场景随机采样 $N_c$ 张干净图像，并从不相交的其他场景均匀采样 $N_n$ 张干扰图像，构成大小为 $N_c + N_n$ 的混合输入集。噪声级别按干扰图像数量划分为三档：

- **Small**：Phototourism/On‑the‑Go/RobustNeRF 使用 $N_n = 10$，ETH3D 使用 $N_n = 5$；
- **Medium**：Phototourism/On‑the‑Go/RobustNeRF 使用 $N_n = 30$，ETH3D 使用 $N_n = 14$；
- **Large**：Phototourism/On‑the‑Go/RobustNeRF 使用 $N_n = 50$，ETH3D 使用 $N_n = 30$。

所有方法在完全相同的随机采样图像集上评估，每次采样重复10次取均值以消除随机性影响。干扰视图与干净视图来自不相交的场景，视图选择过程不使用任何场景元数据。部分基线（如 MegaLoc*）使用了每数据集独立超参调优和 oracle 信息（已知干净视图数量），这些结果以斜体或灰色标示，不作为直接对比对象。

### 4.2 相机位姿估计主结果

Table 1 报告了各方法在不同噪声水平下的相机位姿估计性能。RobustVGGT的两个变体——基于注意力的 **RobustVGGT‑A** 和基于特征相似度的 **RobustVGGT‑F**——在所有数据集和噪声级别上一致优于原始VGGT及各类外部预过滤基线。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2512_04012/figures/008_Table_1.jpg]]
*Table 1: Camera pose estimation across noise levels. * denotes per-dataset hyperparameter tuning with oracle knowledge of the number of clean images in the test set; these entries are shaded as they are not directly comparable. † uses DINOv2 features extracted from VGGT*

**关键发现：**

1. **噪声水平越高，优势越显著**。在Phototourism Large设定（50张干扰图像）下，RobustVGGT‑F的ATE从VGGT的0.3068降至0.2641（↓13.9%）；在On‑the‑Go Large设定下，ATE从0.0754降至0.0521（↓30.9%）。这表明内部表示驱动的过滤机制在极端噪声场景中尤为有效。

2. **特征相似度变体（RobustVGGT‑F）整体优于注意力变体（RobustVGGT‑A）**。在Phototourism Small设定下，RobustVGGT‑F取得最低ATE（0.2641）和最低RPE_trans（0.3936）。这一趋势在多数数据集‑噪声组合中保持一致，说明深层特征的余弦相似度比跨视图注意力提供了更稳定的视图相关性信号。

3. **与外部预过滤方法的对比**。MegaLoc+VGGT和DINOv3+VGGT等基线依赖独立的视觉位置识别（VPR）或全局描述子模型进行视图预选，但它们在跨数据集泛化时往往需要针对每个数据集调整超参数。相比之下，RobustVGGT使用一个共享于所有数据集的固定阈值（$\tau^{att}=0.05$，$\tau^{feat}=0.65$），无需任何数据集特定的调优，却取得了更具竞争力的结果。DINOv2†+VGGT虽然利用了VGGT编码器内部的DINOv2特征，但其视图选择性能仍不及RobustVGGT直接使用最后一层表示的方法。

4. **ETH3D深度估计的验证**。Table 2展示了ETH3D上的多视图深度估计结果。RobustVGGT‑F（Large变体）将AbsRel从VGGT的0.0403降至0.0319（↓20.8%），进一步证实该方法对深度预测同样具有鲁棒性提升。

### 4.3 消融实验

#### 4.3.1 阈值敏感性分析

Table 3 系统考察了RobustVGGT‑A和RobustVGGT‑F在不同阈值 $\tau$ 下的性能变化。实验在Phototourism和On‑the‑Go两个数据集上进行，结果以“Phototourism / On‑the‑Go”的格式并列报告。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2512_04012/figures/015_Table_3.jpg]]
*Table 3: Ablation study on varying threshold values τ . We report the results of (a) RobustVGGT-A and (b) RobustVGGT-F on Phototourism and On-the-Go using camera pose estimation metrics. Results are formatted as Phototourism / On-the-Go*

**RobustVGGT‑A** 在 $\tau = 0.05$ 时达到最佳相机位姿估计——Phototourism上ATE为0.2702，On‑the‑Go上ATE为0.0583。阈值过低（$\tau = 0.01$）会导致部分干扰视图未被有效过滤；阈值过高（$\tau = 0.1$）则可能误删部分干净视图，两者均使性能下降。

**RobustVGGT‑F** 在 $\tau = 0.65$ 时取得最优结果——Phototourism上ATE为0.2641，On‑the‑Go上ATE为0.0521。特征相似度分数对阈值变化的敏感度低于注意力分数，在 $\tau \in [0.55, 0.75]$ 的较宽范围内均保持稳定性能，这得益于余弦相似度本身的归一化特性。

值得注意的是，上述最优阈值在所有数据集和噪声级别上保持固定，无需针对特定场景重新调优，验证了方法的强泛化能力。

#### 4.3.2 干扰视图拒斥成功率

Table 4 报告了各方法在Phototourism和On‑the‑Go上的干扰视图拒斥成功率（Success Rate），即被正确识别并剔除的干扰视图占所有干扰视图的比例。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2512_04012/figures/014_Table_4.jpg]]
*Table 4: Success rate of distractor rejection across noise levels*

RobustVGGT‑F在Phototourism Large设定下达到0.978的成功率，在On‑the‑Go Large下达到0.965，显著高于RobustVGGT‑A（分别为0.942和0.931）。这表明特征相似度分数在区分几何一致/不一致视图方面比注意力分数更为可靠。

进一步地，**RobustVGGT‑A+F**（将归一化后的注意力分数与特征相似度分数以 $\alpha=0.5$ 加权融合）将Phototourism上的成功率推高至0.978，并在多数噪声级别上略优于单一分数变体（Table 8），说明两种内部信号具有互补性。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2512_04012/figures/020_Table_8.jpg]]
*Table 8: Success rate of distractor rejection of VGGT across noise levels*

#### 4.3.3 方法对其他架构的泛化性

为验证所提过滤策略的架构无关性，实验将其应用于另一个前馈3D重建模型 **Pi3**。Table 5–7 分别报告了Pi3在相机位姿估计、多视图深度估计和干扰拒斥成功率上的结果。RobustPi3在所有指标上一致优于原始Pi3，且性能增益模式与VGGT上的观察高度一致——最后一层特征相似度分数同样展现出最强的干净/干扰分离能力。这表明“深层内部表示涌现噪声抑制”的现象并非VGGT独有，可能广泛存在于基于Transformer的前馈重建架构中。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2512_04012/figures/017_Table_5.jpg]]
*Table 5: Camera pose estimation of Pi3*

### 4.4 定性分析

Figure 6 和 Figure 7 分别展示了相机轨迹预测和多视图深度估计的定性对比。在含大量干扰图像的场景中，原始VGGT的预测轨迹出现明显漂移和断裂，深度图中混入大量伪影和错误几何结构；而RobustVGGT通过预先剔除不一致视图，恢复了平滑、一致的轨迹和干净的深度图。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2512_04012/figures/006_Figure_6.jpg]]
*Figure 6: Qualitative results of camera trajectory prediction. Best viewed when zoomed in*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2512_04012/figures/007_Figure_7.jpg]]
*Figure 7: Qualitative results of multi-view depth estimation*

Figure 12 进一步对比了VGGT与RobustVGGT在各数据集上生成的点云。未过滤的VGGT点云中包含由干扰视图引入的离群点簇和重复结构，严重污染场景几何；RobustVGGT的点云则显著更干净，仅保留几何一致的表面点，验证了视图级过滤对最终重建质量的直接改善。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2512_04012/figures/022_Figure_12.jpg]]
*Figure 12: Visualization of point maps produced by VGGT and RobustVGGT on various datasets*

### 4.5 失败模式与局限性

尽管RobustVGGT在多数场景中表现鲁棒，分析揭示了以下边界情况和局限：

1. **视图级过滤的粒度限制**。当前方法仅执行视图级别的二元过滤（保留或剔除整张图像），不进行token/patch级别的细粒度剔除。当干扰视图与干净视图在局部区域共享相似纹理时（例如同一地标的不同拍摄角度但包含大量遮挡物），视图级过滤可能无法有效区分，导致部分污染信息仍被保留。

2. **两趟前向传播的开销**。方法需要首次前向传播计算视图相关性分数，再基于过滤后的视图集进行第二次前向传播以生成最终重建。这使推理成本约为原始VGGT的两倍。对于实时或资源受限的应用场景，该开销可能构成瓶颈。

3. **超大规模图像集合的扩展性未验证**。实验中的最大输入规模为80张图像（50张干净+30张干扰，或类似组合）。在街景级视觉位置识别等涉及数百至数千张候选图像的任务中，全局成对分数计算和阈值过滤的计算复杂度将显著增长，方法的效率和有效性有待进一步验证。

4. **固定阈值的边界失效**。虽然共享阈值 $\tau^{att}=0.05$ 和 $\tau^{feat}=0.65$ 在四个测试数据集上泛化良好，但无法保证在所有可能的域偏移（如极端光照变化、非透视相机模型）下均保持最优。在分布外场景中，分数分布可能整体偏移，导致固定阈值失效。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2512_04012/figures/002_Figure_2.jpg]]
*Figure 2: Reconstruction by VGGT [56]. Although VGGT predicts per-pixel confidence maps to down-weight unreliable depths, this post-hoc signal operates only at the point level and does not filter views. Consequently, distractor images are still reconstructed, allowing spurious content to corrupt the recovered geometry*



## 定位与知识库关联

### 1. 核心基底：VGGT的前馈重建范式

RobustVGGT的方法论根基建立在**VGGT**（Wang et al., CVPR 2025）之上。VGGT是一种纯前馈的3D重建模型，通过交替注意力层直接在输入图像集合上预测相机位姿与深度图，无需显式的优化迭代过程。其关键特征在于：

- **全对全注意力机制**：VGGT的Transformer编码器在图像间执行密集的交叉注意力，隐式建模多视图几何关系。
- **逐点置信度输出**：VGGT为每个深度预测值输出置信度分数，但该信号仅作用于**点级别**的下加权，无法在**视图级别**剔除干扰图像——这是RobustVGGT要解决的核心瓶颈。

RobustVGGT不修改VGGT的架构或权重，而是将其视为一个**内部表示提取器**，从最后一层抽取注意力图和特征图作为视图相关性信号源。

### 2. 与现有离群过滤方法的对比定位

RobustVGGT在方法谱系中占据一个独特位置：**无需训练、无需架构修改、利用模型自身涌现行为的视图过滤策略**。与之形成对照的基线方法可分为以下几类：

#### 2.1 基于外部视觉地点识别（VPR）的预过滤

- **MegaLoc + VGGT**（Berton & Masone, CVPR 2025）：使用专门的VPR模型MegaLoc预先计算全局图像描述子，通过检索相似场景图像来过滤干扰视图，再将筛选后的集合送入VGGT。该方法依赖额外的VPR模型，且MegaLoc的调优需要**每个数据集独立设置超参数**，在部分实验中甚至使用了oracle信息（已知干净图像数量），因此其性能不完全可比。
- **DINOv3 + VGGT**（Simeoni et al., arXiv 2025）：采用DINOv3的全局特征进行视图选择，同样属于外部描述子预过滤路线。尽管DINOv3特征具有强语义判别力，但该方法引入了VGGT之外的独立模型，增加了系统复杂性。

#### 2.2 基于VGGT内部特征的视图选择

- **DINOv2† + VGGT**（Oquab et al., arXiv 2023）：直接复用VGGT编码器中已集成的DINOv2特征进行视图选择。此方法与RobustVGGT最为接近，因为两者都利用了VGGT内部的表示。然而，DINOv2†使用的是**编码器阶段的冻结特征**，而非VGGT交替注意力层涌现的跨视图关系信号。RobustVGGT的关键差异在于：它利用**深层交替注意力层**中自发形成的干净/干扰视图分离，这种分离是VGGT在纯几何训练目标下涌现的行为，而非来自语义预训练特征。

#### 2.3 基于场景图优化的重建

- **MASt3R-SfM**（Duisterhof et al., 3DV 2025）：基于MASt3R的编码特征构建场景图，通过全局优化进行重建。该方法属于**优化驱动**的重建范式，与VGGT的纯前馈范式存在本质差异。其场景图构建过程可能天然具有一定的离群边抑制能力，但计算代价远高于前馈方法。

### 3. 方法适用边界

RobustVGGT的有效性建立在以下前提之上：

1. **VGGT架构依赖**：当前方法专为VGGT设计，利用其交替注意力层的特定行为。能否迁移至其他前馈重建架构（如Pi3、MASt3R）尚待验证。
2. **视图级粗粒度过滤**：方法仅执行**视图级别**的二元过滤（保留或剔除整幅图像），不进行更细粒度的token/patch级别自适应剔除。这意味着部分污染的视图（如仅局部区域包含干扰物体）可能被整体保留或整体丢弃，缺乏精细控制。
3. **阈值泛化性**：RobustVGGT使用单一固定全局阈值（$\tau^{\text{att}}=0.05$，$\tau^{\text{feat}}=0.65$）在所有数据集上工作，这一特性既是优势（无需调参）也是潜在风险——在分布差异极大的图像集合上，固定阈值可能失效。
4. **场景规模上限**：实验中的干扰图像数量最多为50幅（Large噪声级别），在极端大规模图像集合（如街景级视觉地点识别场景）下的扩展性和效率尚未验证。

### 4. 局限性与开放问题

#### 4.1 已知局限

- **两趟前向传播开销**：RobustVGGT需要两次运行VGGT——首次提取内部表示并计算分数，第二次在过滤后的视图子集上执行重建。这使推理成本翻倍，虽然可通过缓存中间表示部分缓解，但尚未在方法中实现。
- **缺乏细粒度过滤**：当前方法不执行token/patch级别的剔除。干扰图像中可能包含与场景几何一致的局部区域，视图级过滤无法利用这些信息，反之干净图像中的局部噪声区域也无法被单独抑制。
- **大规模场景效率未知**：当视图数量增长至数百或数千时，全对全注意力计算的复杂度（$O(N^2)$）和两趟前传的代价可能成为瓶颈。论文未探讨分层过滤或聚类策略来应对这一场景。

#### 4.2 开放问题

1. **细粒度扩展**：能否将视图级过滤扩展为patch/token级别的自适应剔除？例如，对注意力图进行分块阈值化，选择性保留几何一致的区域而抑制局部干扰，有望进一步提升重建精度。

2. **跨架构迁移**：该方法的核心洞察——深层交替注意力层涌现噪声抑制——是否在其他前馈3D重建架构（如Pi3、MASt3R）中同样成立？若成立，能否设计一个统一的无需训练的过滤框架？

3. **推理效率优化**：能否通过一次性联合预测（同时输出分数和重建结果）或缓存首次前传的中间表示来消除第二趟前传？例如，在首次前传中直接预测视图权重，并在同一计算图中完成加权重建。

4. **超大规模扩展策略**：对于包含数百甚至数千视图的场景，如何设计分层过滤或基于聚类的渐进式筛选策略？是否可以利用注意力分数的传递性进行图传播式过滤？

5. **涌现机制的理论理解**：VGGT在纯几何监督下为何会在深层涌现噪声抑制行为？这一现象是否与Transformer架构的归纳偏置或交替注意力的特定设计有关？更深入的理论分析可能指导设计更高效的过滤策略。

### 5. 知识库定位总结

RobustVGGT在3D重建方法谱系中填补了**“利用前馈模型内部涌现行为进行无训练离群过滤”**的空白。它既不同于依赖外部VPR模型的预过滤路线（MegaLoc、DINOv3），也不同于基于优化的场景图方法（MASt3R-SfM），更区别于使用冻结编码器特征的内部特征选择（DINOv2†）。其核心贡献在于**发现并利用**了VGGT深层交替注意力层中自发形成的几何一致性感知能力，将这一涌现行为转化为实用的视图过滤机制，同时保持了零额外训练、零架构修改的简洁性。



## 原文 PDF

![[paperPDFs/CVPR_2026/Emergent_Outlier_View_Rejection_in_Visual_Geometry_Grounded_Transformers.pdf]]
