---
title: "VISion On Request: Enhanced VLLM efficiency with sparse, dynamically selected, vision-language interactions"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VISion_On_Request_Enhanced_VLLM_efficiency_with_sparse_dynamically_selected_vision_language_interactions.pdf
project_link: null
code_link: null
aliases:
- VVR
- VREVESDSVLI
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 自注意力层（图像-图像交互）的执行数量与位置，即动态分配视觉计算的能力。
primary_logic: 通过将标准LVLM层解耦为高效的文本-图像交叉注意力层和少量关键位置的图像-图像自注意力层，可在不丢失视觉信息的前提下大幅降低计算开销，并借助自适应路由按样本复杂度分配计算预算，在简单和困难任务上均取得最优权衡。
claims:
- 跨模态注意力模式分析表明不同任务的图像-文本交互稀疏度差异显著，简单任务仅需少量交互，困难任务需要持续交互。
- CKA分析揭示简单任务的视觉特征在LLM中几乎不变，而困难任务的视觉特征被逐层精细化。
- 层丢弃实验证实存在两个任务簇：视觉敏感（困难）和粗粒度视觉（简单），统一视觉处理策略非最优。
- VISOR在各类基准上以更低的FLOPs超越令牌缩减方法，尤其在困难任务上优势显著。
---

# VISion On Request: Enhanced VLLM efficiency with sparse, dynamically selected, vision-language interactions

> [!tip] 核心洞察
> 通过将标准LVLM层解耦为高效的文本-图像交叉注意力层和少量关键位置的图像-图像自注意力层，可在不丢失视觉信息的前提下大幅降低计算开销，并借助自适应路由按样本复杂度分配计算预算，在简单和困难任务上均取得最优权衡。

| 字段 | 内容 |
|------|------|
| 中文题名 | VISion按需响应：通过稀疏、动态选择的视觉-语言交互增强VLLM效率 |
| 英文题名 | VISion On Request: Enhanced VLLM efficiency with sparse, dynamically selected, vision-language interactions |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.23495) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VISOR (VISion On Request) |
| Dataset | RealWorldQA, Aggregate Easy Benchmarks, Aggregate Hard Benchmarks, Vision-Language Benchmarks |

> [!tip] 效果简介
> - RealWorldQA (RWQA) 上，Accuracy 54.6 vs 54.0 (LLaVA-OV) (+0.6 (8.4× FLOPs savings))。
> - Aggregate Easy Benchmarks 上，Average Accuracy 63.6 (8.6× FLOPs reduction)。
> - Aggregate Hard Benchmarks 上，Average Accuracy 58.4 (8.6× FLOPs reduction)。

## 概要

视觉-语言大模型（VLLM）在推理时需同时处理图像和文本令牌，其标准架构的每一层都对拼接的视觉-文本序列执行全自注意力，导致计算开销随视觉令牌数量呈二次增长。现有加速方案几乎全部采用**令牌缩减（token reduction）**范式——通过剪枝或合并视觉令牌来降低序列长度，但这在需要细粒度视觉理解的任务上造成不可逆的信息瓶颈，性能显著下降。

本文的核心发现是：**不同任务对视觉-语言交互的需求存在根本性差异**。跨模态注意力模式分析（Fig. 2）揭示，简单任务（如ScienceQA）的文本-图像交互高度稀疏，模型主要依赖文本-文本注意力；而困难任务（如DocVQA）则需要在全部层中持续关注图像。CKA相似度分析（Fig. 3）进一步表明，简单任务的视觉表征在整个LLM中几乎不变（相似度>0.9），困难任务的视觉特征则被逐层精细化（相似度降至0.6）。层丢弃实验（Fig. 4）据此将数据集明确分为两个簇：**视觉敏感型（困难）**和**粗粒度视觉型（简单）**，证明统一的视觉处理策略并非最优。

基于上述洞察，论文提出**VISOR（VISion On Request）**，彻底跳出令牌缩减范式。其核心思想是**稀疏化图像与文本令牌之间的交互，而非压缩图像本身**：将标准LVLM层解耦为高效的文本-图像交叉注意力层（提供静态视觉上下文，不修改视觉令牌）和少量关键位置的全自注意力层（细化视觉表征），并通过轻量路由网络按样本复杂度动态分配计算预算。

主要结果：
- 在LLaVA-OV 0.5B骨干上，VISOR以**8.4× FLOPs节省**在RealWorldQA上超越原始LLaVA-OV基线（54.6 vs. 54.0）；
- 在聚合困难基准上，VISOR在**8.6× FLOPs缩减**下保持58.4的平均准确率，显著优于令牌缩减方法在同等节省率下的表现；
- VISOR可与现有令牌缩减方法正交结合，如VISOR-TR+VisionZip实现**37× FLOPs节省**，准确率仅小幅下降；
- 方法在Qwen2-VL-2B和LLaVA-OV 1.5B等不同骨干上均验证有效，通用训练模型在所有计算预算下达到或超越独立训练模型的精度。



视觉-语言大模型（Vision-Language Large Models, VLLMs）在图像理解、文档分析、视觉问答等任务上取得了显著进展，但其推理效率受制于一个根本性的计算瓶颈：标准的Transformer层需同时处理视觉令牌与文本令牌的拼接序列，导致计算复杂度随视觉令牌数量呈二次增长。为缓解这一问题，现有方法普遍采用令牌缩减（token reduction）策略——通过剪枝、合并或渐进丢弃视觉令牌来降低序列长度。然而，这类方法在需要细粒度视觉理解的任务上暴露了关键缺陷：强制丢弃视觉令牌造成了不可逆的信息瓶颈，导致性能显著下降（Fig. 10）。

本文的核心洞察在于，不同任务的视觉-语言交互需求存在本质差异。通过跨模态注意力模式分析（Fig. 2），作者发现：对于ScienceQA等简单任务，模型仅需少量图像-文本交互即可完成任务，注意力以文本-文本交互为主导；而对于DocVQA等困难任务，模型需要在整个网络中持续关注图像信息。进一步的CKA相似度分析（Fig. 3）揭示了更深层的机制：简单任务的视觉特征在LLM各层中几乎保持不变（CKA > 0.9），而困难任务的视觉特征被逐层精细化（CKA降至0.6左右）。层丢弃实验（Fig. 4）则将任务明确划分为两个簇：视觉敏感型（困难任务，如DocVQA、ChartQA、InfoVQA）和粗粒度视觉型（简单任务，如POPE、SQA、GQA）。

上述分析揭示了一个被令牌缩减范式忽视的事实：统一地对所有任务施加相同的视觉处理策略并非最优选择。令牌缩减方法在困难任务上的性能塌缩，根源在于它们混淆了“减少视觉交互”与“丢弃视觉信息”这两个概念。VISOR的设计动机正是从这一区分出发：通过解耦视觉-语言交互层类型并动态控制其执行，在保留完整视觉信息的前提下大幅降低计算开销，从而在简单和困难任务上均取得最优的精度-效率权衡。



## 核心方法与创新机理

VISOR 的核心创新在于**彻底跳出令牌缩减范式**：现有方法（如 VisionZip、SparseVLM、PyramidDrop 等）通过丢弃或合并视觉令牌来降低计算成本，但这在需要细粒度视觉理解的任务上造成了不可逆的信息瓶颈。VISOR 转而**稀疏化视觉令牌与文本令牌之间的交互频率**，在保持完整视觉信息的前提下大幅削减计算开销。

### 关键机制解耦：从全自注意力到选择性交互

标准 LVLM 的每一层 Transformer 都对拼接后的视觉和文本令牌执行全自注意力：

$$[ \mathbf{V}^{(l)} ; \mathbf{T}^{(l)} ] = \mathrm{TL}_l ( [ \mathbf{V}^{(l-1)} ; \mathbf{T}^{(l-1)} ] )$$

该操作的计算复杂度为 $O((N_t + N_v)^2 d + (N_t + N_v) d^2)$，与视觉令牌数量 $N_v$ 呈二次关系。VISOR 将这一过程解耦为三种层类型，仅在少数关键位置执行昂贵的视觉-视觉交互：

$$( \mathbf{V}^{(l)} , \mathbf{T}^{(l)} ) = \begin{cases} \mathrm{TL}_l ( [ \mathbf{V}^{(l - 1)} ; \mathbf{T}^{(l - 1)} ] ), & \text{if } l \in \mathcal{L}_{SA} \\ ( \mathbf{V}^{(l - 1)} , \mathrm{TL}_l ( \mathbf{Z} ) ), & \text{if } l \in \mathcal{L}_{CA} \\ ( \mathbf{V}^{(l - 1)} , \mathrm{TL}_l ( \mathbf{T}^{(l - 1)} ) ), & \text{otherwise} \end{cases}$$

其中 $\mathbf{Z} = \mathrm{CrossAttn}(\mathbf{T}^{(l-1)}, \mathbf{V}^{(l-1)})$。这一设计的三个 changed slots 构成了 VISOR 的技术支柱：

| 设计维度 | 基线方法（令牌缩减/LVLM） | VISOR 方案 | 证据锚点 |
|---------|------------------------|-----------|---------|
| **视觉-语言交互层类型** | 全自注意力（视觉与文本令牌混合处理） | 文本-图像交叉注意力 + 选择性全自注意力，解耦处理 | Eq.2, Eq.3, Fig.5 |
| **视觉令牌更新方式** | 每层都更新视觉令牌 | 仅在 $\mathcal{L}_{SA}$ 指定的自注意力层更新，其余层视觉令牌冻结 | Sec.4.2.1, Eq.2 |
| **计算预算控制** | 固定每层计算，对所有输入不加区分 | 通用模型 + 轻量策略网络根据样本复杂度动态选择 $\mathcal{L}_{SA}$ 配置 | Sec.4.2.3, Sec.4.3 |

### 交叉注意力层：高效的静态视觉上下文注入

在 $\mathcal{L}_{CA}$ 层中，视觉令牌保持冻结（$\mathbf{V}^{(l)} = \mathbf{V}^{(l-1)}$），文本令牌通过交叉注意力查询视觉特征。这一操作的计算复杂度仅为 $O(N_t N_v d)$，与视觉令牌数量呈线性关系。交叉注意力层为文本流提供了稳定的视觉上下文，但**不修改视觉表示本身**——这恰好满足了简单任务的需求：CKA 分析（Fig.3）表明，ScienceQA 等简单任务的视觉特征在 LLM 各层间高度相似（CKA > 0.9），几乎无需精化。

### 自注意力层：按需激活的视觉特征精化

对于 DocVQA、ChartQA 等困难任务，视觉特征需要逐层精化（CKA 从初始层降至约 0.6，Fig.3）。VISOR 在 $\mathcal{L}_{SA}$ 层中恢复全自注意力，使视觉令牌之间可以交互，提取更高层次的视觉特征。消融实验（Table 3）证实：仅使用交叉注意力层（8 层）即可满足粗粒度视觉任务，但困难任务需要自注意力层来细化视觉表示；自注意力层数量从 0 增加到 7 可显著提升困难任务性能，7 层自注意力已接近全模型表现。

### 自适应路由：按样本复杂度分配计算

层丢弃实验（Fig.4）揭示了两个任务簇的存在——视觉敏感型（困难）和粗粒度视觉型（简单），表明统一的视觉处理策略并非最优。VISOR 引入一个轻量策略网络（Routing MLP），根据输入样本的复杂度动态决定执行哪些自注意力层。通用训练模型在所有计算预算下均达到或超越独立训练模型的精度（Table 4），并具备自适应推理能力。路由策略离线训练泛化良好，即使排除部分训练集数据，性能未明显下降（Table 8）。

### 与令牌缩减的协同

VISOR 的稀疏交互机制与令牌缩减方法正交可组合。VISOR-TR 结合 VisionZip 等令牌剪枝方法，可达到最高 37 倍 FLOP 节省，准确率仅小幅下降（Table 2, Table 3），在极端效率场景下仍保持竞争力。



VISOR 的核心设计理念是**解耦文本与视觉令牌的处理流程**，而非像主流令牌缩减方法那样直接丢弃视觉令牌。在标准的大视觉语言模型中，每一层 Transformer 都同时对拼接后的视觉令牌和文本令牌执行全自注意力操作，计算复杂度随视觉序列长度呈二次增长。VISOR 则通过将标准 LVLM 层重构为三种功能层，在几乎不损失视觉信息的前提下大幅降低计算开销。

### 架构总览

VISOR 的推理管道由以下模块串联构成（见 Figure 5）：

![[assets/figures/papers/paper_list_l807_https_arxiv_org_abs_2603_23495/figures/010_Figure_5.jpg]]
*Figure 5: Conceptual architecture of VISOR. Visual information is sparsely injected into the language stream via a few cross-attention and self-attention layers modelling text-image and image-image interactions. Cross-attention efficiently provides visual context to the text tokens without altering the visual representations. Self-attention, while more costly, refines the visual tokens, enabling subsequent crossattention layers to access higher-level visual features. This design strikes a balance between efficiency and representational power*

1. **视觉编码器**（如 SigLIP-400M）：将输入图像编码为一组视觉令牌序列 $\mathbf{V}^{(0)}$。
2. **连接器**（2 层 MLP）：将视觉编码器输出投影到 LLM 的隐空间维度。
3. **条件位置嵌入**：通过 1D 深度可分离卷积（核大小 7，填充 3）为视觉令牌注入空间位置信息。
4. **LLM 骨干**（如 Qwen2）：大部分层仅处理文本令牌，仅在选定的少数层中注入视觉交互。

LLM 内部的每一层根据其所属的功能集合执行不同的操作（见 Eq. 3）：

- **自注意力层（$\mathcal{L}_{SA}$）**：对视觉令牌和文本令牌执行全自注意力，负责**细化视觉表示**。这是计算开销最大的层类型，但 VISOR 只将其放置在少量关键位置。
- **交叉注意力层（$\mathcal{L}_{CA}$）**：文本令牌通过交叉注意力查询静态的视觉特征，但**视觉令牌本身不被修改**（见 Eq. 2）。这为文本流提供了高效的视觉上下文注入，计算复杂度仅为 $O(N_t N_v d)$，与视觉令牌数量呈线性关系。
- **纯文本层（其余层）**：仅对文本令牌执行自注意力，视觉令牌完全冻结传递。

### 数据流与动态路由

在推理时，视觉令牌 $\mathbf{V}$ 仅在 $\mathcal{L}_{SA}$ 层被更新，在其余层保持冻结。文本令牌 $\mathbf{T}$ 则在每一层都被更新，但在 $\mathcal{L}_{CA}$ 层额外获得来自视觉令牌的交叉注意力信息。这种设计使得：

- **粗粒度视觉任务**（如 ScienceQA、POPE）仅需交叉注意力层即可维持高性能，因为其视觉特征在整个 LLM 中几乎不变（CKA > 0.9，见 Figure 3）。
- **细粒度视觉任务**（如 DocVQA、ChartQA）则需要自注意力层来逐步精化视觉表示，以支持后续交叉注意力层提取更高层次的视觉特征。

为了在推理时自适应地分配计算预算，VISOR 引入了一个轻量级**策略网络（Routing MLP）**。该网络以视觉令牌的全局池化特征为输入，输出一个离散的层配置选择（即决定哪些层属于 $\mathcal{L}_{SA}$），从而根据样本复杂度动态调整视觉-语言交互的稀疏程度。策略网络通过离线伪标签训练，泛化性实验表明即使排除部分训练集数据，性能也未明显下降（Table 8）。

### 与令牌缩减的协同

VISOR 的稀疏交互机制与令牌缩减方法是**正交且可叠加**的。VISOR-TR 变体将 VISOR 与 VisionZip 等令牌剪枝方法结合，在交叉注意力层之前进一步压缩视觉令牌数量，可实现高达 37 倍的 FLOPs 节省，同时准确率仅小幅下降（Table 2, Table 3）。这验证了“减少交互频率”与“压缩令牌数量”两条效率优化路径的互补性。



### 标准LVLM层的计算瓶颈

标准LVLM将视觉令牌 $\mathbf{V}^{(l-1)}$ 与文本令牌 $\mathbf{T}^{(l-1)}$ 拼接后送入Transformer层进行全自注意力计算：

$$[ \mathbf{V}^{(l)} ; \mathbf{T}^{(l)} ] = \mathrm{TL}_l ( [ \mathbf{V}^{(l-1)} ; \mathbf{T}^{(l-1)} ] )$$

该操作的复杂度为 $O((N_t + N_v)^2 d + (N_t + N_v) d^2)$，其中 $N_v$ 为视觉令牌数，$N_t$ 为文本令牌数，$d$ 为隐藏维度。当视觉令牌数量较大时，计算开销呈二次增长，成为效率瓶颈。

### VISOR的核心解耦设计

VISOR将标准LVLM层解耦为三种层类型，通过层索引集合 $\mathcal{L}_{SA}$（自注意力层）和 $\mathcal{L}_{CA}$（交叉注意力层）控制视觉-语言交互的稀疏性。完整层更新规则为：

$$( \mathbf{V}^{(l)} , \mathbf{T}^{(l)} ) = \begin{cases} \mathrm{TL}_l ( [ \mathbf{V}^{(l - 1)} ; \mathbf{T}^{(l - 1)} ] ), & \text{if } l \in \mathcal{L}_{SA} \\ ( \mathbf{V}^{(l - 1)} , \mathrm{TL}_l ( \mathbf{Z} ) ), & \text{if } l \in \mathcal{L}_{CA} \\ ( \mathbf{V}^{(l - 1)} , \mathrm{TL}_l ( \mathbf{T}^{(l - 1)} ) ), & \text{otherwise} \end{cases}$$

其中 $\mathbf{Z} = \mathrm{CrossAttn}(\mathbf{T}^{(l-1)}, \mathbf{V}^{(l-1)})$ 为交叉注意力输出。

#### 交叉注意力层（$\mathcal{L}_{CA}$）

交叉注意力层将静态视觉上下文高效注入文本流，同时冻结视觉令牌：

$$\mathbf{V}^{(l)} = \mathbf{V}^{(l-1)}, \quad \mathbf{T}^{(l)} = \begin{cases} \mathrm{TL}_l(\mathbf{CrossAttn}(\mathbf{T}^{(l-1)}, \mathbf{V}^{(l-1)})), & \text{if } l \in \mathcal{L}_{CA} \\ \mathrm{TL}_l(\mathbf{T}^{(l-1)}), & \text{otherwise} \end{cases}$$

其计算复杂度为 $O(N_t N_v d)$，与视觉令牌数呈线性关系，远低于全自注意力的二次复杂度。交叉注意力层不修改视觉令牌本身，因此后续层仍可访问原始视觉特征。

为保留视觉令牌的空间结构信息，VISOR采用条件位置嵌入（Conditional Positional Embedding），通过核大小为7、填充为3的一维深度可分离卷积实现。

#### 自注意力层（$\mathcal{L}_{SA}$）

自注意力层对视觉令牌执行全自注意力计算，用于细化视觉表示，支持层次化特征提取。虽然自注意力层计算开销较大，但仅在 $\mathcal{L}_{SA}$ 指定的少量关键层执行，使后续交叉注意力层能够访问更高层次的视觉特征。

#### 纯文本层

大多数LLM层仅处理文本令牌，完全不涉及视觉令牌，计算复杂度为 $O(N_t^2 d + N_t d^2)$。

### 动态路由策略

VISOR通过轻量策略网络（Routing MLP）实现按样本复杂度的动态计算预算分配。策略网络根据输入决定执行哪些自注意力层，使简单任务仅使用交叉注意力层即可完成（粗粒度视觉上下文），而困难任务则激活更多自注意力层以精细化视觉表示。该路由策略通过离线伪标签训练，在通用模型中同时支持多种配置，无需为不同计算预算独立训练模型。

### 与令牌缩减的结合

VISOR可与令牌缩减方法结合形成VISOR-TR。在交叉注意力层前对视觉令牌进行剪枝或打包，进一步降低 $N_v$，从而减少交叉注意力的线性开销。实验表明该组合可达到最高37倍FLOP节省（结合VisionZip），同时保持有竞争力的准确率。

### 补充图表

![[assets/figures/papers/paper_list_l807_https_arxiv_org_abs_2603_23495/figures/004_Figure_2.jpg]]
*Figure 2: Cross-modality attention patterns across layers. We plot the proportion of attention scores allocated to three interaction types: text queries attending to image tokens (Query-to-Image), answer tokens attending to image tokens (Answer-to-Image), and answer tokens attending to query tokens (Answer-to-Query). For easy tasks like SQA, interaction is sparse and dominated by text-to-text attention. For hard tasks like DocVQA, the model attends to the image across the whole network*

![[assets/figures/papers/paper_list_l807_https_arxiv_org_abs_2603_23495/figures/006_Figure_3.jpg]]
*Figure 3: Evolution of visual representations across layers, measured by pairwise CKA similarity. For easy tasks (e.g., SQA), visual features remain largely static (high similarity across layers). For harder tasks (e.g., DocVQA), features are progressively refined*

![[assets/figures/papers/paper_list_l807_https_arxiv_org_abs_2603_23495/figures/008_Figure_4.jpg]]
*Figure 4: Accuracy sensitivity by dropping all vision tokens for different subsets of LLM layers. Left: Accuracy distribution on a dataset-by-dataset basis. Certain datasets (e.g., DocVQA, ChartQA) are particularly sensitive to reduced vision-language interactions. Right: we show how the layer-drop config. & accuracy correlate among datasets. Two clusters emerge: vision-sensitive (“hard”) (e.g., InfoVQA, OCRBench, etc.) and coarse vision (“easy”) (e.g., POPE, SQA, GQA, etc.) datasets*



## 实验与关键发现

### 主要结果：精度与效率的帕累托前沿

VISOR 在 LLaVA-OV 0.5B 骨干上的核心实验结果（Table 1）表明，该方法在多个视觉-语言基准上以显著更低的计算量达到或超越了现有最优方法的精度。在仅使用交叉注意力层（无自注意力层）的配置下，VISOR 在需要粗粒度视觉上下文的任务上实现 **8.6×** 的 FLOPs 节省，同时平均精度达到 **63.6%**；对于需要细粒度视觉理解的困难任务，通过引入少量自注意力层，VISOR 在 **8.6×** FLOPs 节省下仍保持 **58.4%** 的平均精度。当与令牌缩减方法结合时（VISOR-TR），FLOPs 节省进一步提升至 **18×**，而精度仅轻微下降。

![[assets/figures/papers/paper_list_l807_https_arxiv_org_abs_2603_23495/figures/011_Table_1.jpg]]
*Table 1: Comparison with state-of-the-art methods on various vision-language benchmarks. The metric used is accuracy for all datasets, except for MME where we report a score (higher is better; MME values are divided by 20 for normalization purposes)*

逐数据集分析（Table 5）进一步揭示了 VISOR 在不同任务上的效率优势。以 RealWorldQA 为例，VISOR 以 **8.4×** 的 FLOPs 节省实现了 **54.6%** 的准确率，超越了 LLaVA-OV 基线的 **54.0%**。在需要高分辨率理解的困难任务（如 DocVQA、ChartQA）上，现有令牌缩减方法因丢弃视觉令牌而导致显著的信息损失，而 VISOR 通过保留完整视觉令牌并仅在关键层进行视觉-语言交互，避免了这一瓶颈。

![[assets/figures/papers/paper_list_l807_https_arxiv_org_abs_2603_23495/figures/016_Table_5.jpg]]
*Table 5: Per-dataset saving rates. We compare our method against state-of-the-art approaches using a shared LLaVA-OV (0.5B) backbone. For each method, the top row indicates the accuracy, while the bottom row shows the FLOPs savings relative to the baseline LLaVA-OV model. The metrics used are accuracy for most datasets, except for MME where we report a score (higher is better)*

Figure 1 从 FLOPs 减少与准确率的关系维度展示了 VISOR 的效率优势：VISOR 在困难任务上的准确率-效率曲线显著优于令牌缩减方法，说明“保留令牌、稀疏交互”的策略在信息保持上具有根本性优势。

![[assets/figures/papers/paper_list_l807_https_arxiv_org_abs_2603_23495/figures/001_Figure_1.jpg]]
*Figure 1: Efficiency comparison: FLOPs reduction vs acc. Notice that our approach is significantly more efficient while also retaining the performance on the harder datasets. See Sects. 3 and 5.1 for “easy”-“hard” definition*

### 消融研究：交叉注意力与自注意力的功能分工

**交叉注意力层的充分性边界。** Table 3 的消融实验表明，仅使用交叉注意力层（8 层 CA，0 层 SA）即可满足粗粒度视觉任务（如 ScienceQA、POPE）的需求，准确率接近全模型水平。这验证了第 3 节的分析结论：简单任务的视觉特征在 LLM 深层中几乎不变（CKA > 0.9），因此静态视觉上下文通过交叉注意力注入文本流已足够。

**自注意力层的精化作用。** 当自注意力层数量从 0 增加到 7 时，困难任务（如 DocVQA、InfoVQA）的性能显著提升，7 层 SA 配置的准确率接近全模型。这证实了困难任务需要渐进式的视觉特征精化——自注意力层通过图像-图像交互更新视觉令牌，使后续交叉注意力层能够访问更高层次的视觉特征。Figure 3 的 CKA 分析为此提供了机制层面的解释：DocVQA 的视觉特征在 LLM 各层间持续演变（CKA 从 0.9 降至 0.6），而 ScienceQA 的特征保持高度相似。

**通用训练 vs. 独立训练。** Table 4 比较了支持多配置的通用训练模型与针对每个配置独立训练的模型。结果表明，通用训练模型在所有计算预算下均达到或超越独立训练模型的精度，同时具备自适应推理能力。这得益于训练过程中多配置的联合优化带来的正则化效应。

**与令牌缩减的协同效应。** Table 2 和 Table 3 显示，VISOR 与令牌缩减方法的结合可进一步压缩计算。例如，VISOR-TR 结合 VisionZip 在困难任务上达到 **37×** FLOPs 节省，准确率仅小幅下降。这表明 VISOR 的稀疏交互策略与令牌缩减在效率提升上是正交且可叠加的。

### 自适应路由：按样本复杂度分配计算

VISOR 的路由策略网络（Policy Network）根据输入样本的复杂度动态选择执行哪些自注意力层。Figure 6 的性能热力图展示了不同配置在各数据集上的相对准确率，揭示了任务需求与层配置之间的对应关系。Figure 7 进一步展示了路由器为各测试数据集分配的层配置，表明路由器能够自动为简单任务分配更少的自注意力层，为困难任务分配更多自注意力层。

![[assets/figures/papers/paper_list_l807_https_arxiv_org_abs_2603_23495/figures/015_Figure_6.jpg]]
*Figure 6: Performance heatmap for different configurations across datasets. Each row represents a configuration, and each column corresponds to a dataset. The color intensity indicates the relative accuracy achieved by that configuration on the respective dataset*

Table 8 的路由泛化性实验表明，即使训练时排除部分数据集（如 AI2D、DocVQA、GQA），路由器在测试时对这些数据集的配置分配仍保持合理，性能未出现明显下降。这说明路由策略学习到的是任务复杂度的通用特征，而非对特定数据集的过拟合。

### 失败模式与局限性

尽管 VISOR 在整体上表现出色，但在极端设置下仍存在信息瓶颈风险。当结合极端令牌缩减（如将视觉令牌压缩至极低数量）时，困难任务上的性能下降仍然显著——这是因为自注意力层的视觉精化能力受限于输入令牌的信息含量。此外，通用训练模型需要在多个配置间平衡，可能无法为某一特定配置达到绝对最优精度（尽管实验表明其性能通常优于独立训练）。离线伪标签路由依赖预定义的配置集合和训练数据分布，对于分布外样本的泛化性尚待进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l807_https_arxiv_org_abs_2603_23495/figures/013_Table_3.jpg]]
*Table 3: Acc. comparison across configurations and categories*

![[assets/figures/papers/paper_list_l807_https_arxiv_org_abs_2603_23495/figures/014_Table_4.jpg]]
*Table 4: Accuracy comparison between independently trained models and a universally trained model supporting multiple configurations. Both model variants use the same fixed configuration for all samples*

![[assets/figures/papers/paper_list_l807_https_arxiv_org_abs_2603_23495/figures/012_Table_2.jpg]]
*Table 2: Accuracy comparison when combining VISOR with token reduction methods*

![[assets/figures/papers/paper_list_l807_https_arxiv_org_abs_2603_23495/figures/021_Figure_10.jpg]]
*Figure 10: Efficiency comparison - number of FLOPS vs. vision sequence length*



## 定位与知识库关联

### 与令牌缩减范式的根本分歧

现有VLLM效率优化工作主要围绕**令牌缩减**（token reduction）展开，其核心假设是视觉令牌中存在大量冗余，可通过丢弃或合并来降低计算开销。代表性方法包括：

- **训练无关剪枝**：**VisionZip** 和 **VisPruner** 基于视觉注意力分数或文本-视觉交互排名选择性地保留视觉令牌，无需额外训练即可实现令牌压缩。
- **渐进式丢弃**：**PyramidDrop** 在LLM的不同阶段逐步减少视觉令牌数量，利用浅层到深层的冗余度差异。
- **嵌套令牌层级**：**M3** 构建多粒度的令牌表示，允许在不同计算预算下灵活切换。
- **高分辨率预过滤**：**HiRED** 在视觉令牌进入LLM之前进行高分辨率令牌的预丢弃。

这些方法的共同瓶颈在于：**当任务需要细粒度视觉理解时，强制丢弃视觉令牌会形成不可逆的信息瓶颈**。从Figure 10的效率-精度权衡曲线可以清晰看出，令牌缩减方法在简单任务上表现尚可，但在DocVQA、ChartQA等困难任务上性能急剧下降。VISOR的定位正是绕开这一范式——不压缩图像本身，而是稀疏化图像与文本令牌之间的交互。

### VISOR的核心创新维度

VISOR在以下几个维度上与现有工作形成根本差异：

| 维度 | 令牌缩减范式 | VISOR范式 |
|------|-------------|-----------|
| **信息保留** | 丢弃视觉令牌，信息不可逆丢失 | 保留全部视觉令牌，仅限制交互频率 |
| **计算控制** | 通过令牌数量控制计算量 | 通过自注意力层数量控制计算量 |
| **任务适应性** | 统一处理，难以区分任务难度 | 动态路由，按需分配计算预算 |
| **与令牌缩减的兼容性** | — | 可与VisionZip等组合，进一步节省FLOPs |

### 技术谱系中的定位

从架构演进角度看，VISOR处于**稠密全注意力LVLM**与**纯令牌缩减方法**之间的新设计点。其设计灵感来自对LVLM内部表征动态的实证分析：

1. **跨模态注意力稀疏性**（Figure 2）：简单任务（如ScienceQA）中，文本查询对图像的注意力集中在少数层，而困难任务（如DocVQA）需要贯穿整个网络的持续图像交互。这一发现直接支撑了“仅少数层需要视觉交互”的设计选择。

2. **视觉特征演化差异**（Figure 3）：通过CKA相似度分析发现，简单任务的视觉特征在LLM各层间几乎不变（CKA > 0.9），而困难任务的视觉特征被逐层精细化（CKA降至0.6）。这表明**并非所有层都需要更新视觉表示**，为冻结视觉令牌提供了依据。

3. **层丢弃敏感性聚类**（Figure 4）：随机丢弃不同层组合的视觉令牌后，数据集自然分化为两个簇——视觉敏感型（DocVQA、ChartQA、InfoVQA等）和粗粒度视觉型（POPE、SQA、GQA等）。这揭示了统一视觉处理策略的次优性，为自适应路由提供了动机。

### 方法边界与适用条件

**适用场景**：
- 混合难度批处理场景，VISOR的路由机制可自动为简单样本节省计算、为困难样本保留精度
- 需要高分辨率视觉理解但计算预算受限的部署环境
- 与令牌缩减方法协同使用时可达到极致的效率-精度权衡（VISOR-TR + VisionZip可达37倍FLOPs节省）

**边界与局限**：
1. **通用模型训练的权衡**：通用训练模型需要在多个配置间平衡，可能无法为特定配置达到绝对最优精度。虽然实验表明其性能通常优于独立训练（Table 4），但在极端计算预算下，专门训练的轻量模型可能仍有微小优势。

2. **离线路由的泛化性**：当前路由策略依赖预定义的配置集合和伪标签训练，对于分布外样本的泛化性尚待验证。Table 8显示排除部分训练集数据后路由性能未明显下降，但这仍限于同分布测试。

3. **参数开销**：交叉注意力层额外增加约7.5%参数。对于0.5B规模的LLaVA-OV骨干，这一开销可接受；但对于更小的模型，参数增加的相对比例可能成为负担。

4. **视觉编码器兼容性**：方法在SigLIP-400M和FastVLM上验证（Table 11），未在更多视觉编码器（如CLIP、DINOv2变体）上测试。不同编码器的特征特性可能影响交叉注意力的有效性。

5. **极端令牌缩减的残留风险**：当VISOR与极端令牌压缩结合时，困难任务上的信息瓶颈风险依然存在。这是因为令牌缩减和交互稀疏化虽然正交，但叠加后视觉信息的有效传递通道被双重压缩。

### 开放问题与未来方向

1. **在线/强化路由**：当前离线伪标签路由能否扩展到在线或强化学习范式，以更灵活地适应未知场景和开放域输入？

2. **多帧/视频扩展**：VISOR的稀疏交互模式能否推广到视频理解任务？视频的时间冗余可能为更激进的交互稀疏化提供机会。

3. **零样本架构迁移**：在完全无需预训练数据的设置下，VISOR能否保持对全新LLM架构（如Mamba、RWKV等非Transformer骨干）的有效性？

4. **交叉注意力层下界**：消融实验（Table 3）显示8层交叉注意力足以满足粗粒度任务，但这一数量能否进一步减少？是否存在理论下界？

5. **训练数据效率**：Table 10显示使用50%训练数据时性能下降有限，但更极端的低数据场景（如10-20%）下VISOR的训练稳定性如何，尚待探索。



## 原文 PDF

![[paperPDFs/CVPR_2026/VISion_On_Request_Enhanced_VLLM_efficiency_with_sparse_dynamically_selected_vision_language_interactions.pdf]]
