---
title: Hybrid Token Compression for Vision-Language Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Hybrid_Token_Compression_for_Vision_Language_Models.pdf
project_link: null
code_link: null
aliases:
- HV
- HTCVLM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 在压缩前注入极少量（4 个）由 MGVQ 生成的离散语义锚点，恢复高层语义框架，并通过解耦注意力掩码强制信息经由混合潜在变量整合。
primary_logic: 视觉信息需在压缩前显式解耦为离散语义通道与连续细节通道，方能在单 token 表示中同时保留二者，从而突破效率-保真度权衡。
claims:
- HTC-VLM 在 7 个基准上平均性能保留率达 87.2%，显著超过领先的连续压缩基线 VoCo-LLaMA（81.0%）
- 注意力热图显示压缩后的 <voco> token 将最大注意力权重分配给离散语义 token，证实其作为可解释语义载体的作用
- 离散语义锚点（MGVQ）在消融中显著优于基于连续选择的启发式方法（随机、Top‑k 注意力、K‑Means），证明离散量化对保留高层语义的必要性
- GQA 上 Accuracy = 57.6
---

# Hybrid Token Compression for Vision-Language Models

> [!tip] 核心洞察
> 视觉信息需在压缩前显式解耦为离散语义通道与连续细节通道，方能在单 token 表示中同时保留二者，从而突破效率-保真度权衡。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向视觉-语言模型的混合 Token 压缩 |
| 英文题名 | Hybrid Token Compression for Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.08240) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | HTC-VLM |
| Dataset | GQA, VQAv2, MMBench, MME^P |

> [!tip] 效果简介
> - GQA 上，Accuracy 57.6 vs 57.4 (VoCo-LLaMA) (+0.2)。
> - VQAv2 上，Accuracy 72.4 vs 71.8 (VoCo-LLaMA) (+0.6)。
> - MMBench 上，Accuracy 60.0 vs 57.9 (VoCo-LLaMA) (+2.1)。

## 概述

视觉-语言模型（VLM）的推理效率受限于视觉 token 数量带来的二次注意力成本——典型配置下 576 个 patch token 与文本 token 的联合自注意力构成主要计算瓶颈。现有压缩策略可分为三类：**剪枝**（如 **FastV**, Chen et al., ECCV 2024; **PyramidDrop**, Xing et al., arXiv 2024）直接丢弃视觉 token，虽降低计算量却不可逆地丢失细粒度信息；**连续压缩**（如 **Q-Former**, Li et al., ICML 2023; **VoCo-LLaMA**, Ye et al., CVPR 2025）将 patch 序列压缩为少量连续潜在向量，但单 token 瓶颈无法同时编码离散语义（物体类别、空间布局）与连续视觉细节（纹理、姿态），导致语义稀释和粒度缺失；**离散量化**虽能保留高层语义，却牺牲了连续细节的保真度。

**HTC-VLM** 的核心洞察在于：视觉信息需在压缩前显式解耦为离散语义通道与连续细节通道，方能在单 token 表示中同时保留二者。该方法在压缩前注入极少量（4 个）由 MGVQ 生成的离散语义锚点，恢复高层语义框架，并通过解耦注意力掩码强制信息经由混合潜在变量整合，从而突破效率-保真度权衡。

在 7 个主流视觉理解基准（GQA、VQAv2、MMBench、MME、POPE、SEED-Bench、ScienceQA-Image）上，HTC-VLM 以 580-to-1 的极端压缩比取得 **87.2% 的平均性能保留率**，显著超过领先的连续压缩基线 VoCo-LLaMA（81.0%）。注意力热图进一步证实，压缩后的 `<voco>` token 将最大注意力权重分配给离散语义 token，表明其作为可解释语义载体的有效性。

## 背景与动机

### 视觉-语言模型的 Token 效率困境

当前主流视觉-语言模型（VLM）通常将图像编码为数百个视觉 token，再与文本 token 拼接后送入大语言模型（LLM）进行多模态理解。然而，LLM 的自注意力计算复杂度为 $\mathcal{O}((N+L)^2)$，其中 $N$ 为视觉 token 数量，$L$ 为文本 token 数量。以典型配置为例，一张图像经 CLIP ViT-L/14 编码后产生 576 个 patch token，这使得推理延迟和显存开销随视觉 token 数量平方级增长，严重制约了 VLM 在实时交互和资源受限场景下的部署。

### 现有压缩方法的局限

为缓解这一瓶颈，研究者提出了多种视觉 token 压缩策略，可大致归纳为三类：

- **Token 剪枝**：如 **FastV**（Chen et al., ECCV 2024）在早期层丢弃低注意力 token，**PyramidDrop**（Xing et al., arXiv 2024）通过金字塔式冗余削减逐步移除视觉 token。这类方法直接丢弃 token，不可避免地损失部分视觉信息。
- **Token 合并**：如 **ToMe**（Bolya et al., arXiv 2022）通过相似度匹配合并冗余 token，但合并后的表示语义混杂，缺乏可解释的结构。
- **连续压缩**：以 **VoCo-LLaMA**（Ye et al., CVPR 2025）为代表，将 576 个 patch token 压缩为单个 `<voco>` 潜在向量。该方法在极致压缩比下取得了当前最优的性能保留率（81.0%），但其核心缺陷在于：**单 token 连续瓶颈无法同时编码离散语义（如物体类别、属性）与连续视觉细节（如纹理、姿态）**，导致语义稀释和粒度缺失。

### 核心瓶颈：语义-细节的不可分困境

上述连续压缩方法的失败根源于一个深层矛盾：视觉信息天然包含离散的语义概念和连续的视觉外观两个正交维度。将二者强行坍缩到单一连续潜在向量中，必然导致语义结构被平滑、细节被稀释。这一“语义-细节不可分困境”构成了当前视觉 token 压缩的根本瓶颈。

### 本文动机与核心思路

针对上述困境，**HTC-VLM** 提出了一种混合压缩架构，核心思路是在压缩前显式解耦视觉信息为两个并行通道：

1. **连续细节通道**：保留 ViT 的全部 576 个 patch 嵌入，承载纹理、姿态等低层细节。
2. **离散语义通道**：通过多组向量量化（MGVQ）生成极少量（仅 4 个）离散语义 token，作为高层语义锚点。

两个通道的表示通过解耦注意力掩码在压缩瓶颈（单个 `<voco>` token）中融合，形成同时保留语义框架和视觉细节的混合潜在表示。这一设计使得 HTC-VLM 在保持单 token 推理效率的前提下，将 7 个基准上的平均性能保留率从 VoCo-LLaMA 的 81.0% 提升至 87.2%，显著突破了效率-保真度权衡。

## 核心创新

### 问题瓶颈：单 token 连续压缩的语义稀释与粒度缺失

现有视觉-语言模型（VLM）的 token 压缩方法——无论是基于学习查询向量的 **Q-Former**（Li et al., ICML 2023）、平均池化的 **LLaMA-VID**（Li et al., ECCV 2024），还是当前 SOTA 的 **VoCo-LLaMA**（Ye et al., CVPR 2025）——均将 576 个连续 patch token 直接压缩为单个连续潜在向量。这一“单通道连续瓶颈”存在根本性缺陷：连续向量空间天然适合编码纹理、姿态等低层细节，却难以有效承载物体类别、空间布局等离散语义结构，导致压缩后的表示遭遇**语义稀释**（semantic dilution）和**粒度缺失**（granularity gap）。

### 核心洞察：压缩前的显式语义-细节解耦

HTC-VLM 的核心洞察在于：视觉信息必须在压缩**之前**显式解耦为离散语义通道与连续细节通道，方能在单 token 表示中同时保留二者，从而突破效率-保真度权衡。这一设计将压缩问题从“如何在连续空间中挤压信息”重新表述为“如何让离散语义锚点引导连续信息的融合”。

### 关键创新：三个 changed slots

相较于 VoCo-LLaMA 等连续压缩基线，HTC-VLM 在三个关键维度上做出了根本性改变：

**1. 视觉 token 组成：从纯连续序列到混合序列**

基线方法仅使用 576 个连续 patch token $V = \{v_i\}_{i=1}^{576}$。HTC-VLM 在压缩前**前置** 4 个由 MGVQ（Multi-Group Vector Quantization）生成的离散语义 token $v_d$，形成 580 维混合序列：

$$V_{hy} = [v_d; V] \in \mathbb{R}^{580 \times 4096}$$

这 4 个离散 token 作为“语义锚点”，在压缩前恢复了高层语义框架。消融实验表明，离散语义锚点（MGVQ）在 GQA 和 MME 上显著优于基于连续选择的启发式方法（随机选择、Top‑k 注意力、K‑Means 聚类中心），验证了**离散量化**对保留高层语义的必要性（Table 12 Top）。

**2. 注意力掩码：从标准因果掩码到解耦注意力掩码**

基线方法采用标准因果掩码或未显式限制视觉 token 间交互。HTC-VLM 引入**解耦注意力掩码** $M_{hy}$，其规则为：
- 文本 token 只能关注 `<voco>` token，禁止直接关注视觉 token；
- 视觉 token 之间禁止相互关注（防止特征过平滑）；
- `<voco>` token 可关注所有视觉 token。

这一“星形拓扑”（Star Graph）强制信息经由 `<voco>` 瓶颈整合。消融表明，星形拓扑比全图注意力（Full Graph）平均性能保留率提高 1.8%，证明其有效防止了特征过平滑（Table 12 Bottom）。

**3. 压缩瓶颈设计：从直接压缩到混合潜在表示**

基线方法直接将连续 patch 序列压缩为单个 `<voco>` token。HTC-VLM 的 `<voco>` token 在解耦掩码指导下，同时整合离散语义锚点和连续 patch token，最终提取为混合潜在表示 $z$。注意力热图（Figure 3）证实，压缩后的 `<voco>` token 将最大注意力权重分配给离散语义 token，表明其作为**可解释语义载体**的角色。

### 方法谱系与知识库定位

HTC-VLM 在视觉压缩范式谱系中占据独特位置（Table 5）：不同于 **ToMe**（Bolya et al., arXiv 2022）的 token 合并、**FastV**（Chen et al., ECCV 2024）和 **PDrop**（Xing et al., arXiv 2024）的 token 剪枝、**SparseVLM**（Zhang et al., arXiv 2024）的视觉稀疏化，以及 VoCo-LLaMA 的纯连续压缩，HTC-VLM 首次将**离散量化**与**连续压缩**在单 token 瓶颈中融合，形成了“语义锚定 + 细节保留”的混合压缩范式。

## 整体框架

HTC-VLM 的核心设计动机源于对现有视觉 Token 压缩方法瓶颈的深入诊断：**单 Token 连续瓶颈无法同时编码离散语义（如物体类别）与连续视觉细节（如纹理、姿态），导致语义稀释和粒度缺失**。为解决这一问题，HTC-VLM 提出了一种**混合压缩架构**，在压缩前注入极少量（4 个）由 MGVQ 生成的离散语义锚点，恢复高层语义框架，并通过解耦注意力掩码强制信息经由混合潜在变量整合。

### 双通道解耦架构

HTC-VLM 的整体 pipeline 由两个并行的视觉编码通道构成，分别负责提取高层语义与低层细节：

- **连续细节通道（D）**：采用冻结的 CLIP ViT-L/14 编码器 $\mathcal{E}_v$ 和可训练的线性投影层 $\mathcal{P}_v$，将输入图像 $I$ 映射为 576 个 patch 嵌入，以保留纹理、姿态等细粒度视觉细节：
  $$V = \{ v_i \}_{i=1}^{576} = \mathcal{P}_v(\mathcal{E}_v(I)), \quad v_i \in \mathbb{R}^{4096}$$

- **离散语义通道（S）**：使用预训练的 MGVQ 量化器 $\mathcal{Q}$ 将图像量化为离散编码 $q$，再通过一个两层 MLP 投影 $\mathcal{P}_d$ 生成 4 个离散语义 token $v_d$，提供物体类别、空间布局等高层语义框架：
  $$q = \mathcal{Q}(I), \quad v_d = \mathcal{P}_d(q) = \mathrm{GELU}(W_2 \cdot \mathrm{GELU}(W_1 \cdot q))$$

### 混合序列构造与信息融合

双通道的输出通过**前置融合**策略整合为统一的混合视觉序列。具体而言，将 4 个离散语义 token $v_d$ 前置到 576 个连续 patch token $V$ 之前，形成 580 维的混合序列：
$$V_{hy} = [v_d; V] \in \mathbb{R}^{580 \times 4096}$$

这种前置策略（预融合）在消融实验中被证实优于后置或并行融合，验证了语义锚点对后续压缩过程的“提示效应”（Section 5.3.2, Table 4）。

### 解耦注意力掩码与压缩瓶颈

混合序列 $V_{hy}$ 随后进入一个配备**解耦注意力掩码 $M_{hy}$** 的 Transformer 压缩模块。该掩码实现了三种关键的信息流控制规则：

1. **文本 token 只能关注 `<voco>` token**，不能直接访问任何视觉 token；
2. **视觉 token 之间禁止相互关注**（$i \neq j$ 时掩码为 $-\infty$），防止特征过平滑；
3. **`<voco>` token 可以关注所有视觉 token**（包括离散语义 token 和连续 patch token）。

掩码的数学形式为：
$$M_{hy}(i,j) = \begin{cases} 0, & \text{if } x_i \in W \text{ and } x_j \in V_{hy} \\ -\infty, & \text{if } x_i, x_j \in V_{hy} \text{ and } i \neq j \\ 1, & \text{otherwise} \end{cases}$$

这种星形拓扑（Star Graph）的注意力结构在消融中比全图注意力（Full Graph）平均性能保留率提高 1.8%，证明其有效防止了视觉 token 间的特征过平滑（Table 12）。

在解耦掩码的指导下，一个可训练的单一 `<voco>` token 通过注意力机制整合整个 $V_{hy}$ 的信息，最终提取为压缩后的潜在表示 $z$，作为 LLM 的视觉输入。

### 端到端训练

整个 pipeline 在标准自回归语言建模目标下进行端到端训练，损失函数为：
$$\mathcal{L}_{\mathrm{HTC}} = - \mathbb{E}_{p(I,T,Y)} \left[ \sum_{i=1}^{|Y|} \log p_{\theta}(y_i \mid y_{<i}, <\mathrm{voco}>, T; M_{hy}) \right]$$

其中 $T$ 为文本指令，$Y$ 为目标回答。训练过程中，视觉编码器 $\mathcal{E}_v$ 和 MGVQ 量化器 $\mathcal{Q}$ 保持冻结，仅训练线性投影层 $\mathcal{P}_v$、MLP 投影 $\mathcal{P}_d$、压缩 Transformer 层以及 LLM 的 LoRA 适配器。

### 与基线方法的架构对比

Figure 2 清晰地展示了 HTC-VLM 与主流压缩范式的架构差异。与 **VoCo-LLaMA**（Ye et al., CVPR 2025）将 576 个 patch token 直接压缩为单个 `<voco>` token 不同，HTC-VLM 在压缩前显式注入了离散语义信息。与 **Q-Former**（Li et al., ICML 2023）使用可学习查询向量的方式相比，HTC-VLM 的离散语义 token 来自图像内容的量化编码，而非随机初始化的向量。与平均池化方法（如 **LLaMA-VID**, Li et al., ECCV 2024）相比，HTC-VLM 保留了 token 级别的信息交互能力，同时通过解耦掩码避免了信息冗余。

![[assets/figures/papers/paper_list_l755_https_arxiv_org_abs_2512_08240/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of visual token compression strategies. (a) Pooling Method: visual embeddings are averaged or pooled before being fused with text inputs. (b) VoCo-LLaMA: compresses 576 visual tokens into a single \<voco> token. (c) HTC-VLM (ours): introduces a hybrid representation with a continuous channel (D) encoding 576 patch embeddings and a discrete channel (S) generating 4 semantic tokens via MGVQ. The hybrid sequence*

Figure 2 的对比直观地揭示了核心创新点：**视觉信息需在压缩前显式解耦为离散语义通道与连续细节通道，方能在单 token 表示中同时保留二者，从而突破效率-保真度权衡**。

### 补充图表

![[assets/figures/papers/paper_list_l755_https_arxiv_org_abs_2512_08240/figures/001_Figure_1.jpg]]
*Figure 1: Vision-token compression. (a) VoCo-LLaMA collapses 576 patches into one \<voco> token, losing semantic structure. (b) HTC-VLM adds 4 discrete semantic tokens and compresses all into one \<voco> token, preserving semantics and visual detail*

## 核心模块与公式推导

HTC-VLM 的核心设计在于将视觉信息显式解耦为**离散语义通道**与**连续细节通道**，并通过一个配备解耦注意力掩码的单 token 瓶颈实现融合压缩。以下逐一阐述关键模块及其数学形式。

### 连续细节通道

连续通道负责保留低层视觉细节 $D$（如纹理、姿态、局部结构）。该通道采用冻结的 CLIP ViT-L/14 编码器 $\mathcal{E}_v$ 与可训练的线性投影层 $\mathcal{P}_v$，将输入图像 $I$ 映射为 $N=576$ 个 patch 嵌入：

$$V = \{ v_i \}_{i=1}^{576} = \mathcal{P}_v(\mathcal{E}_v(I)), \quad v_i \in \mathbb{R}^{4096}$$

投影后的维度 4096 与 LLM 的隐空间对齐，确保细节信息可直接注入后续 Transformer 层。

### 离散语义通道

离散通道负责提取高层语义 $S$（如物体类别、空间布局），其核心是预训练的**多组向量量化器** MGVQ $\mathcal{Q}$。量化器将图像编码为离散码本索引，再经两层 MLP 投影 $\mathcal{P}_d$ 生成 $G=4$ 个离散语义嵌入：

$$q = \mathcal{Q}(I), \quad v_d = \mathcal{P}_d(q) = \mathrm{GELU}(W_2 \cdot \mathrm{GELU}(W_1 \cdot q))$$

MGVQ 的量化目标是最小化重建误差 $\mathbb{E} \|I - \mathcal{Q}^{-1}(q)\|_2^2$，从而将连续视觉信号压缩为离散符号，形成语义“锚点”。消融实验表明，码书大小 $K=16384$ 与组数 $G=8$ 在语义聚类能力与训练稳定性之间达到最优平衡（Table 8）。

### 混合序列构造与解耦注意力掩码

两个通道的输出通过**前置融合**策略构造混合序列——将离散语义嵌入置于连续 patch 嵌入之前，形成 580-token 的混合表示：

$$V_{hy} = [v_d; V] \in \mathbb{R}^{580 \times 4096}$$

这一前置设计的动机在于让离散 token 充当“语义提示”，引导后续压缩过程聚焦于高层概念（消融证实此前置比后置或并行融合更优，Table 4）。

为实现信息隔离与定向融合，HTC-VLM 引入**解耦注意力掩码** $M_{hy}$，其规则如下：

$$M_{hy}(i,j) = \begin{cases} 0, & \text{if } x_i \in W \text{ and } x_j \in V_{hy} \\ -\infty, & \text{if } x_i, x_j \in V_{hy} \text{ and } i \neq j \\ 1, & \text{otherwise} \end{cases}$$

其中 $W$ 为文本 token 集合。该掩码构建了一个**星形拓扑**：
- 文本 token 只能关注 `<voco>` token，无法直接访问任何视觉 token；
- 视觉 token 之间禁止相互关注，防止特征过平滑；
- `<voco>` token 可关注所有视觉 token（离散语义 + 连续 patch），成为唯一的信息整合枢纽。

消融显示，此星形拓扑相比全图注意力平均性能保留率提升 1.8%（Table 12 Bottom），证实了信息隔离对压缩质量的关键作用。

### 压缩瓶颈与训练目标

可训练的 `<voco>` token 在上述掩码指导下，通过注意力机制整合 $V_{hy}$ 的全部信息，最终提取为单一潜在表示 $z$ 供 LLM 使用。整个框架以标准自回归语言建模损失端到端优化：

$$\mathcal{L}_{\mathrm{HTC}} = - \mathbb{E}_{p(I,T,Y)} \left[ \sum_{i=1}^{|Y|} \log p_{\theta}(y_i \mid y_{<i}, <\mathrm{voco}>, T; M_{hy}) \right]$$

该损失在解耦掩码 $M_{hy}$ 约束下，迫使 `<voco>` token 学习同时编码离散语义与连续细节，从而突破单 token 连续瓶颈的效率-保真度权衡。

## 实验与分析

### 核心实验设计

实验在 7 个主流视觉-语言理解基准上评估 HTC-VLM：GQA、VQAv2、MMBench、MME^P、POPE、SEED-Bench 和 ScienceQA-Image。所有对比方法均将 576 个视觉 token 压缩为单一 token，训练数据、骨干架构和评估协议严格遵循 **VoCo-LLaMA**（Ye et al., CVPR 2025）的设置，确保公平性。

基线体系覆盖了当前主流的压缩范式：
- **连续压缩**：**Q-Former**（BLIP-2; Li et al., ICML 2023）通过可学习查询向量压缩视觉信息；**Avg. Pool**（LLaMA-VID; Li et al., ECCV 2024）使用平均池化；**VoCo-LLaMA** 是单 token 连续压缩的 SOTA 方法。
- **Token 剪枝/合并**：**ToMe**（Bolya et al., arXiv 2022）、**FastV**（Chen et al., ECCV 2024）、**PDrop**（Xing et al., arXiv 2024）和 **SparseVLM**（Zhang et al., arXiv 2024）通过丢弃或合并冗余 token 实现压缩。

### 主实验结果：580-to-1 压缩下的性能保留

Table 1 展示了各方法在 580-to-1 极端压缩比下的性能。HTC-VLM 在 7 个基准上的平均性能保留率达 **87.2%**，显著超过连续压缩 SOTA VoCo-LLaMA 的 81.0%，提升 **+6.2 个百分点**。具体而言：

![[assets/figures/papers/paper_list_l755_https_arxiv_org_abs_2512_08240/figures/003_Table_1.jpg]]
*Table 1: Comparison of HTC-VLM with previous vision compression approaches on common visual understanding benchmarks. All methods reduce 576 tokens to one. ”Avg.” refers to the average of per-benchmark performance retention rates, calculated as (Result - Lower Bound) / (Upper Bound - Lower Bound) for each benchmark. Our hybrid approach attains the best results*

- 在需要高层语义理解的基准上优势尤为明显：MMBench 上领先 **+2.1%**（60.0 vs. 57.9），ScienceQA-Image 上领先 **+1.4%**（67.7 vs. 66.3），POPE 幻觉检测上领先 **+1.3%**（82.8 vs. 81.5）。
- 在 VQAv2 和 GQA 等细节敏感任务上也保持正增益（+0.6% 和 +0.2%），表明混合压缩并未牺牲细节保真度。
- 相比池化方法（Avg. Pool 保留率约 75%）和 Q-Former（约 78%），HTC-VLM 的优势更为显著，验证了“离散语义锚点 + 连续细节”双通道设计的有效性。

### 不同 Token 预算下的鲁棒性

Table 2 进一步考察了在 192、128、64 token 预算下的性能。HTC-VLM 在所有预算下均保持领先：
- 在 64-token 极端设置下，HTC-VLM 仍保留原始性能的 **89.8%**，而 VoCo-LLaMA 降至约 85%。
- 随着 token 预算减少，HTC-VLM 的性能衰减曲线明显更平缓（见 Figure 4），证明离散语义锚点在极端压缩时提供了关键的“语义骨架”，防止性能崩塌。

![[assets/figures/papers/paper_list_l755_https_arxiv_org_abs_2512_08240/figures/004_Table_2.jpg]]
*Table 2: Comparison of token compression methods under varying token budgets. Vanilla, with 576 visual tokens, serves as the upper bound for each benchmark. The table reports per-benchmark results and average performance retention (%) for different token lengths (192, 128, 64), highlighting how compression affects performance across tasks*

![[assets/figures/papers/paper_list_l755_https_arxiv_org_abs_2512_08240/figures/010_Figure_4.jpg]]
*Figure 4: Performance vs. visual token budget on GQA/VQAv2. HTC-VLM maintains higher accuracy under extreme compression while matching the efficiency of single-token baselines*

### 表征探测：解耦效果的直接证据

Table 3 通过表征探测实验量化了离散、连续和混合表征的信息承载能力。实验训练线性分类器从不同表征中解码语义信息（物体类别）和细节信息（纹理/姿态）：

![[assets/figures/papers/paper_list_l755_https_arxiv_org_abs_2512_08240/figures/005_Table_3.jpg]]
*Table 3: Probing Top-1 accuracy (%) of discrete (vd), continuous (V¯ ), and hybrid*

- 纯离散表征 v_d 在语义任务上准确率最高（约 25%），但在细节任务上表现极差（< 5%），验证了其作为高层语义载体的专一性。
- 纯连续表征 V̄ 在细节任务上表现良好（约 28%），但语义解码能力弱（约 15%）。
- 压缩后的混合表征 z_voco 在两项任务上均达到最佳：细节 30.70%、语义 26.67%，证明压缩瓶颈成功融合了两类信息，而非简单丢弃某一通道。

### 注意力热图分析：可解释的语义载体

Figure 3 展示了 HTC-VLM 与 VoCo-LLaMA 中 `<voco>` token 对视觉 token 的注意力分布对比（16 个 MME 测试样本）：

![[assets/figures/papers/paper_list_l755_https_arxiv_org_abs_2512_08240/figures/006_Figure_3.jpg]]
*Figure 3: Comparison of compression strategies and their effect on visual token attention. Left: Attention heatmap of the \<voco> token in HTC-VLM over 4 discrete semantic token plus the first 12 image patch tokens for 16 test samples from the MME benchmark. Right: Attention heatmap of the \<voco> token in the original VoCo-LLaMA [46] model over the first 16 image patch tokens for the same 16 test samples*

- HTC-VLM 的 `<voco>` token 将**最大注意力权重一致地分配给 4 个离散语义 token**，而非直接关注 patch token。这表明离散语义锚点充当了“信息路由”，`<voco>` 通过语义锚点间接获取视觉信息。
- 相比之下，VoCo-LLaMA 的 `<voco>` token 注意力分散在多个 patch token 上，缺乏明确的语义聚焦，解释了其语义稀释的机制根源。

### 消融实验：关键设计选择的因果验证

Table 4 和 Table 12 系统消融了 HTC-VLM 的各核心组件：

![[assets/figures/papers/paper_list_l755_https_arxiv_org_abs_2512_08240/figures/007_Table_4.jpg]]
*Table 4: Ablation study on different configurations of HTC-VLM. Performance retention (%) is reported relative to the full model*

![[assets/figures/papers/paper_list_l755_https_arxiv_org_abs_2512_08240/figures/016_Table_12.jpg]]
*Table 12: Component Analysis on Anchors and Masking. Top: Comparison of different semantic anchor types. Discrete anchors significantly outperform continuous selection heuristics. Bottom: Comparison of masking topologies. Our disentangled Star-Graph prevents feature oversmoothing*

**1. 双通道的必要性**
- 纯连续压缩（VoCo-LLaMA 配置）保留率 81.0%。
- 纯离散压缩（仅 MGVQ token，无连续 patch）保留率骤降至约 **33.0%**，证明离散语义信息虽关键但不足以单独支撑视觉理解，必须与连续细节协同。

**2. 语义锚点类型**
- 将 MGVQ 离散锚点替换为连续选择启发式方法（随机选择、Top-k 注意力选择、K-Means 聚类中心）后，GQA 和 MME 性能均显著下降（Table 12 Top），验证了**离散量化**对保留高层语义的必要性——连续选择无法可靠捕获离散的语义类别。

**3. 融合顺序**
- 离散 token 前置（`[v_d; V]`）优于后置或并行融合，证实了语义锚点的“提示效应”：先建立高层语义框架，再填充连续细节，有利于压缩瓶颈的高效整合。

**4. 解耦注意力掩码**
- 星形拓扑（Star Graph，禁止视觉 token 间自注意）比全图注意力（Full Graph）平均保留率提高 **+1.8%**（Table 12 Bottom）。全图注意力导致视觉 token 间特征过平滑，削弱了细节保真度；星形掩码强制信息通过 `<voco>` 整合，避免了冗余交互。

**5. MGVQ 配置**
- 组数 G=8、码书大小 K=16384 在语义聚类质量和训练稳定性之间达到最佳平衡（Table 8）。进一步增大码书（K>16384）性能饱和且可能导致训练不稳定。

![[assets/figures/papers/paper_list_l755_https_arxiv_org_abs_2512_08240/figures/011_Table_8.jpg]]
*Table 8: Ablation on MGVQ codebook and group configuration. Values are placeholders; replace with your measured results. Larger codebooks improve semantic clustering but may destabilize training beyond K = 16,384*

### 推理效率

Table 7 显示，尽管 HTC-VLM 引入了额外的离散通道（4 个 token 的 MGVQ 量化 + MLP 投影），其端到端推理延迟、吞吐量和显存占用与单 token 连续压缩方法（VoCo-LLaMA）基本持平，同时精度显著更高。离散通道的计算开销（Table 11 的延迟分解）在整体推理中占比极小，因为 MGVQ 量化器轻量且与 ViT 编码器并行执行。

![[assets/figures/papers/paper_list_l755_https_arxiv_org_abs_2512_08240/figures/012_Table_7.jpg]]
*Table 7: Inference efficiency comparison on A100 80GB. HTC-VLM matches single-token efficiency while significantly outperforming continuous-only and structured pruning baselines. Values are placeholders; replace with your measured results*

### 失败模式与局限性

论文未明确报告 HTC-VLM 的失败案例或性能下限。基于其设计原理，以下潜在弱点需在实际应用中验证：
- **空间关系推理**：离散语义锚点擅长编码“什么”（物体类别），但可能难以捕获“哪里”（精确空间布局）。在需要精细空间推理的任务（如 RefCOCO 指代表达理解）上，性能是否退化需进一步评估。
- **多图像/视频扩展**：当前设计针对单图像，离散语义锚点如何跨帧对齐和传播是开放问题。
- **联合训练**：当前 MGVQ 量化器冻结，联合微调离散码书和 VLM 可能进一步提升适应性，但也可能引入训练不稳定性。

### 理论定位：压缩范式的形式化对比

Table 5 从信息保留、语义解耦等维度形式化对比了 HTC-VLM 与剪枝、连续压缩、离散量化等范式。HTC-VLM 是唯一同时满足“单 token 瓶颈效率”和“显式语义-细节解耦”的方法，其核心机制可概括为：在压缩前注入离散语义锚点，通过解耦注意力掩码强制信息经由混合瓶颈整合，从而突破传统连续压缩的语义稀释瓶颈。

![[assets/figures/papers/paper_list_l755_https_arxiv_org_abs_2512_08240/figures/008_Table_5.jpg]]
*Table 5: Formal Comparison of Visual Compression Paradigms. We contrast HTC-VLM with Pruning, Continuous Compression, and Discrete Quantization. Notation: N is the original patch count (576), M is the pruned count*

## 方法谱系与知识库定位

### 1. 视觉压缩范式的谱系位置

HTC-VLM 处于视觉-语言模型（VLM）视觉 token 压缩的关键交叉点。为理解其创新边界，需将其置于四种主流压缩范式的坐标系中（Table 5）：

| 范式 | 代表方法 | 核心机制 | 信息损失模式 |
|------|----------|----------|--------------|
| **Token 剪枝** | **FastV** (Chen et al., ECCV 2024)、**PDrop/PyramidDrop** (Xing et al., arXiv 2024)、**SparseVLM** (Zhang et al., arXiv 2024) | 按注意力或冗余度丢弃低分 token | 不可逆丢弃，可能丢失稀疏但关键的细节 |
| **Token 合并** | **ToMe** (Bolya et al., arXiv 2022) | 基于相似度合并冗余 token | 合并操作模糊 token 边界，粒度损失 |
| **连续压缩** | **Q-Former/BLIP-2** (Li et al., ICML 2023)、**Avg. Pool/LLaMA-VID** (Li et al., ECCV 2024)、**VoCo-LLaMA** (Ye et al., CVPR 2025) | 将多 token 压缩为少量连续潜在向量 | 语义稀释：离散语义被平滑为连续均值 |
| **离散量化** | 纯 MGVQ 等 | 将图像量化为离散码字 | 细节丢失：连续纹理被离散化模糊 |

HTC-VLM 的定位是**混合压缩（Hybrid Compression）**——它并非简单地在上述范式中选择其一，而是通过**双通道解耦**将连续压缩与离散量化融合在同一瓶颈中。这一设计直接回应了论文识别出的核心瓶颈：单 token 连续瓶颈无法同时编码离散语义与连续视觉细节。

### 2. 与连续压缩基线的关系：以 VoCo-LLaMA 为直接对标

VoCo-LLaMA 是 HTC-VLM 最直接的技术前身和对比对象。二者共享以下架构基因：
- 均以 LLaVA-1.5 为骨干框架；
- 均使用冻结的 CLIP ViT-L/14 编码器和可训练的线性投影层；
- 均将 576 个 patch token 压缩为单个 `<voco>` token；
- 均采用自回归语言建模损失进行训练。

**关键差异**在于压缩前的信息结构（Figure 1）：
- VoCo-LLaMA 直接将 576 个连续 patch token 压缩为单个 `<voco>`，信息在压缩过程中被强制混合为连续潜在表示，导致离散语义（如物体类别、空间关系）被稀释为统计均值。
- HTC-VLM 在压缩前注入 4 个由 MGVQ 生成的离散语义 token，形成 580-token 混合序列 `[v_d; V]`，再通过解耦注意力掩码指导 `<voco>` token 进行信息整合。这一设计使得压缩后的表示保留了可追溯的语义锚点。

从实验证据看，HTC-VLM 在 7 个基准上的平均性能保留率达 87.2%，显著超过 VoCo-LLaMA 的 81.0%（Table 1），验证了混合解耦策略的有效性。值得注意的是，实验设置严格遵循 VoCo-LLaMA 的训练数据、骨干架构和评估协议，所有基线在相同条件下复现，确保了对比的公平性（Section 5.1）。

### 3. 与离散量化方法的关系

纯离散量化方法（如直接使用 MGVQ token 替代视觉表示）虽能保留高层语义，但消融实验显示其性能骤降至约 33.0%（Table 4），证明连续细节通道对于维持整体性能不可或缺。HTC-VLM 的创新在于**不将离散量化作为替代方案，而是作为连续压缩的语义补充**——4 个离散 token 提供语义框架，576 个连续 patch token 提供细节填充，二者在解耦注意力掩码的约束下通过 `<voco>` token 融合。

### 4. 适用边界与局限

基于现有证据和论文的开放问题，HTC-VLM 的适用边界可归纳如下：

**已验证的有效范围**：
- **单图像输入**：当前设计针对单张静态图像的视觉理解任务，在 GQA、VQAv2、MMBench、MME、POPE、SEED-Bench、ScienceQA-Image 七个基准上验证有效。
- **580-to-1 极端压缩**：在将 580 个 token 压缩为 1 个的极端设置下，HTC-VLM 仍保持 87.2% 的性能保留率，且推理效率匹配单 token 基线（Table 7）。
- **CLIP ViT-L/14 编码器**：连续通道基于该特定编码器，MGVQ 的码书大小（K=16,384）和组数（G=8）经消融验证为最优配置（Table 8）。

**待验证的扩展边界**（论文明确列为开放问题）：
- **多图像/视频输入**：HTC-VLM 如何扩展到多帧或视频场景，离散语义锚点是否能在时序维度上保持一致性，尚待研究。
- **编码器泛化性**：解耦架构是否可推广到其他视觉编码器（如 ViT-G），连续通道的投影层和离散通道的 MGVQ 是否需要重新训练或适配，缺乏实验证据。
- **联合学习**：当前 MGVQ 量化器为预训练且冻结，联合学习离散语义锚点和 VLM 是否能进一步提高适应性，是开放问题。
- **空间推理下限**：在极端压缩下，是否存在某些视觉推理任务（如精细空间关系判断）的性能下限，论文未提供专项分析。

**架构层面的固有限制**：
- MGVQ 码书大小存在饱和效应：更大码书（K > 16,384）可能引发训练不稳定（Table 8），限制了语义粒度的上限。
- 离散 token 数量固定为 4，其最优性仅在当前实验设置下验证，对不同复杂度场景的自适应调整机制尚未探索。

### 5. 开放问题与后续工作方向

除上述扩展边界外，论文还提出了以下值得关注的开放问题：

1. **语义锚点的自适应选择**：当前 MGVQ 生成的 4 个离散 token 是固定数量的全局语义锚点。是否可以根据图像复杂度动态调整锚点数量，或在空间维度上分配局部语义锚点，是提升灵活性的潜在方向。

2. **解耦掩码的拓扑扩展**：消融实验证实星形图拓扑（Star Graph）优于全图拓扑（Full Graph），平均保留率提高 1.8%（Table 12 Bottom）。但更复杂的图结构（如层次化掩码、基于语义相似度的动态掩码）是否能在保持信息隔离的同时增强融合效率，值得探索。

3. **与 Token 剪枝/合并的协同**：HTC-VLM 的混合压缩策略与 FastV、ToMe 等方法并非互斥——在混合序列构造后，是否可对连续 patch 部分进行选择性剪枝以进一步降低计算开销，同时保留离散语义锚点，是实用的工程方向。

4. **理论解释的深化**：论文通过注意力热图（Figure 3）和表征探测（Table 3）提供了语义解耦的经验证据，但对解耦注意力掩码为何能防止特征过平滑、离散锚点为何能产生“提示效应”的理论机制分析尚浅，有待形式化建模。

## 原文 PDF

![[paperPDFs/CVPR_2026/Hybrid_Token_Compression_for_Vision_Language_Models.pdf]]
