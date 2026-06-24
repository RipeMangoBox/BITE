---
title: Hierarchical Enhancement of Semantic Priors for Disentangled Text-Driven Motion Generation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Hierarchical_Enhancement_of_Semantic_Priors_for_Disentangled_Text_Driven_Motion_Generation.pdf
aliases:
- HESPDTDMG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
core_operator: 将潜在运动空间显式建模为时间自适应混合高斯子流形，并引入动态记忆与分层注意力实现层次化文本-运动对齐。
primary_logic: 结构化潜在建模与层次化跨模态推理是实现解耦、可解释且语义一致的文本到运动生成的关键。
claims:
- AG-VAE将潜在空间分解为多个语义子流形，显著降低重建MSE（从0.3584到0.2981，相对提升16.84%）。
- AG-VAE在潜在空间聚类质量指标上远超标准VAE（CH指数48.81 vs 11.95，DB指数5.39 vs 7.83）。
- 去除DCMM或HCA模块会显著降低R-Precision和FID，证明层次化跨模态对齐的关键作用。
- 在HumanML3D和KIT-ML上，HESP在FID、R-Precision等主要指标上达到最优或次优，同时保持更高的多样性和物理合理性。
---

# Hierarchical Enhancement of Semantic Priors for Disentangled Text-Driven Motion Generation

> [!tip] 核心洞察
> 结构化潜在建模与层次化跨模态推理是实现解耦、可解释且语义一致的文本到运动生成的关键。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向解耦文本驱动运动生成的语义先验分层增强 |
| 英文题名 | Hierarchical Enhancement of Semantic Priors for Disentangled Text-Driven Motion Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Lv_Hierarchical_Enhancement_of_Semantic_Priors_for_Disentangled_Text-Driven_Motion_Generation_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/representation_self_supervised_transfer |
| Method | HESP |
| Dataset | HumanML3D |

> [!tip] 效果简介
> - HumanML3D 上，整体文本-运动对齐（FID, R-Precision, MM-Dist, Diversity） Best or second-best scores vs SALAD, MoMask, MDM (Superior)；潜在空间 Calinski-Harabasz 指数 48.81 vs 11.95 (Standard VAE) (+36.86)。
> - HumanML3D (重建评估) 上，MSE 0.2981 vs 0.3584 (Standard VAE) (-0.0603 (16.84%))。

## 概述

文本驱动的三维人体运动生成，旨在根据自然语言描述合成逼真的动作序列，是视觉计算与具身智能交叉领域的关键问题。现有扩散模型虽在生成质量上取得显著进展，但其底层依赖**各向同性高斯先验**与**平坦跨模态监督**，导致潜在空间语义纠缠、可解释性差、可控性弱——这是制约文本-运动生成走向精细语义对齐的核心瓶颈。

针对上述问题，本文提出 **HESP**（Hierarchical Enhancement of Semantic Priors），从潜在空间结构化建模与层次化跨模态推理两个维度进行系统性重构。其核心洞察在于：**将运动潜在空间显式建模为时间自适应的高斯混合子流形，并引入动态记忆与分层注意力机制，是实现解耦、可解释且语义一致的运动生成的关键**。

方法层面，HESP 包含三个关键模块：
- **AG-VAE**（Adaptive Gaussian VAE）：以骨骼拓扑为条件，将潜在运动空间分解为多个语义子流形，形成时间自适应的高斯混合先验，取代传统 VAE 的各向同性高斯假设。
- **DCMM**（Dynamic Cross-Modal Memory）：构建可学习的跨模态记忆库，通过运动与文本的联合查询向量检索长期语义原型，实现自适应语义融合。
- **HCA**（Hierarchical Cross-Modal Attention）：在词-关节（局部）与句子-轨迹（全局）两个粒度上执行跨模态注意力，并通过可学习门控进行凸组合融合。

实验层面，在 **HumanML3D** 和 **KIT-ML** 两个标准基准上，HESP 在 FID、R-Precision 等主要指标上达到最优或次优水平，同时保持更高的运动多样性与物理合理性。具体而言：AG-VAE 将重建 MSE 从标准 VAE 的 0.3584 降至 0.2981（相对提升 16.84%），并在潜在空间聚类质量指标上取得显著优势（CH 指数 48.81 vs 11.95，DB 指数 5.39 vs 7.83）。消融实验进一步证实，移除 DCMM 或 HCA 模块会显著降低 R-Precision 并劣化 FID，验证了层次化跨模态对齐的关键作用。

在方法谱系上，HESP 处于**结构化潜在扩散模型**与**层次化跨模态对齐**的交汇点。相较于 **MDM**（Tevet et al., ICLR 2023）的朴素扩散框架、**MoMask**（Guo et al., CVPR 2024）的掩码生成策略以及 **SALAD**（Hong et al., CVPR 2025）的骨骼感知扩散方法，HESP 的核心区分在于：在潜在空间先验层面引入显式语义结构化，在跨模态融合层面引入记忆增强的层次化注意力，从而在生成质量与语义可控性之间取得更优平衡。

本文剩余部分组织如下：第2节回顾相关工作并给出方法总览；第3节详述 AG-VAE 的潜在结构化建模与层次化跨模态对齐机制；第4节呈现定量评估、消融实验与可视化分析；第5节讨论局限性并展望未来方向。

## 背景与动机

### 文本驱动运动生成的核心瓶颈

文本驱动的人体运动生成旨在从自然语言描述中合成逼真的三维动作序列，在动画制作、虚拟现实和人机交互等领域具有广泛的应用前景。近年来，扩散模型在该任务上取得了显著进展，代表性工作包括**MDM**（Tevet et al., ICLR 2023）、**MoMask**（Guo et al., CVPR 2024）和**SALAD**（Hong et al., CVPR 2025）等。然而，现有扩散模型普遍存在一个深层瓶颈：**潜在空间采用各向同性高斯先验，跨模态监督方式平坦**，导致潜在表示中不同语义的运动模式高度纠缠，可解释性和可控性均受到严重制约。

具体而言，标准VAE假设潜在变量服从单一的、各向同性的高斯分布，这迫使所有运动模式——无论是“行走”、“跳跃”还是“挥手”——都被压缩到同一个无结构的连续空间中。如Figure 1(a)所示，标准VAE的潜在分布呈现出高度重叠、缺乏清晰边界的特征，这使得模型难以区分不同语义的运动类型，也无法为下游的扩散生成器提供结构化的先验引导。与此同时，现有的文本-运动对齐机制多采用平坦的交叉注意力或CLIP条件注入，缺乏对词-关节（局部）和句子-轨迹（全局）等多层级语义关系的显式建模，导致生成的运动在细粒度语义对齐和物理合理性方面存在不足。

### 结构化潜在建模与层次化跨模态推理的动机

上述瓶颈的根源在于两个层面：**潜在先验的结构缺失**和**跨模态对齐的粒度不足**。从因果机制来看，若潜在空间本身不具备语义组织结构，扩散模型的去噪过程就缺乏有效的几何约束，生成的运动容易偏离文本语义；若跨模态融合仅停留在单一粒度，模型就无法同时捕捉“某个词对应哪个身体部位”的局部对齐和“整句话对应何种运动轨迹”的全局对齐。

针对这一洞察，本文提出**HESP（Hierarchical Enhancement of Semantic Priors）**框架，核心思路是：

1. **结构化潜在先验**：通过自适应高斯混合变分自编码器（AG-VAE），将潜在运动空间显式建模为多个以骨骼拓扑为条件、时间自适应的语义子流形，使不同运动模式在潜在空间中自然分离。
2. **层次化跨模态推理**：设计动态跨模态记忆模块（DCMM）和分层跨模态注意力（HCA），分别实现长期语义检索和词-关节/句子-轨迹的多层级对齐，并通过可学习门控机制自适应融合。

如Figure 1(b)所示，AG-VAE的潜在分布呈现出清晰的多模态分离结构，每个高斯分量对应一类运动动态，簇概率分布（Figure 1(c)）也验证了语义组织的有效性。这种结构化先验为扩散生成器提供了更强的归纳偏置，而层次化跨模态对齐则确保了文本语义在局部和全局两个粒度上都能准确注入运动生成过程。

## 核心创新

HESP 的核心创新在于将文本驱动的运动生成从“平坦潜在空间 + 均匀跨模态监督”的范式，升级为“结构化潜在流形 + 层次化语义推理”的双重增强框架。具体而言，HESP 在以下三个关键维度上实现了突破性的方法改进：

### 1. 潜在先验建模：从各向同性高斯到时间自适应混合高斯子流形

传统扩散模型（如 **MDM** (Tevet et al., ICLR 2023)、**MoMask** (Guo et al., CVPR 2024)）普遍采用标准 VAE 的各向同性高斯先验，导致潜在空间中不同语义的运动模式相互重叠、纠缠不清。HESP 提出的 **AG-VAE**（Adaptive Gaussian VAE）从根本上改变了这一局面——它将潜在运动空间显式建模为多个语义子流形的组合，每个子流形对应一类独特的运动动力学模式。

其核心机制是时间自适应高斯混合先验：

$$p(z_t | S, T) = \sum_{k=1}^K \pi_k(t, S) \mathcal{N}(z_t | \mu_k(S), \Sigma_k(S, T))$$

该先验以骨骼拓扑 $S$ 和时间位置 $T$ 为条件，使混合权重 $\pi_k(t, S)$ 能够随时间动态调整，从而在序列的不同时间步自动切换至最匹配的语义子流形。这一设计的直接效果是：潜在空间从无序的重叠分布（Figure 1a）转变为清晰分离的多模态结构（Figure 1b），簇概率分布呈现出明确的语义归属（Figure 1c）。

定量证据表明，AG-VAE 在 HumanML3D 上的重建 MSE 从标准 VAE 的 0.3584 降至 0.2981，相对提升 **16.84%**（Figure 3）；潜在空间的 Calinski-Harabasz 指数从 11.95 跃升至 **48.81**，Davies-Bouldin 指数从 7.83 降至 5.39（Table 2），证实了结构化潜在建模在提升重建精度和语义可分离性方面的决定性作用。

### 2. 跨模态对齐方式：从平坦注意力到动态记忆增强的层次化推理

现有方法通常采用平坦的交叉注意力或 CLIP 条件注入来实现文本与运动的对齐，这忽略了语言描述中存在的天然层次结构——词对应局部关节、句子对应全局轨迹。HESP 通过 **DCMM**（Dynamic Cross-Modal Memory）与 **HCA**（Hierarchical Cross-Modal Attention）两个模块实现了层次化跨模态推理。

**DCMM** 维护一个可学习的跨模态记忆库 $\mathcal{M}$，存储原型化的文本-运动对。在生成过程中，它通过由运动潜在向量均值与词嵌入均值拼接而成的查询向量 $q = \varphi_q([\mathrm{mean}_t(z_t), \mathrm{mean}_w(c_w)])$ 进行检索，获取长期语义先验，从而克服了标准注意力机制在长序列中语义漂移的问题。

**HCA** 则进一步将跨模态注意力分解为两个层级：

$$\mathcal{A}_{\mathrm{local}} = \mathrm{softmax}\left(\frac{\mathcal{Q}_{\mathrm{motion}} K_{\mathrm{word}}^{\top}}{\sqrt{d}}\right) \mathcal{V}_{\mathrm{word}},\quad \mathcal{A}_{\mathrm{global}} = \mathrm{softmax}\left(\frac{\mathcal{Q}_{\mathrm{motion}} K_{\mathrm{sent}}^{\top}}{\sqrt{d}}\right) \mathcal{V}_{\mathrm{sent}}$$

并通过可学习门控 $\lambda$ 进行融合：$\mathbf{h}_t = \lambda \mathcal{A}_{\mathrm{local}} + (1-\lambda) \mathcal{A}_{\mathrm{global}}$。这种设计使得模型能够同时捕捉词-关节的细粒度对应和句子-轨迹的粗粒度语义一致性。

消融实验（Table 4）为这一创新的必要性提供了有力证据：移除 DCMM 导致 R-Precision Top-3 从 0.871 降至 0.847，FID 显著上升；移除 HCA 则使 R-Precision Top-3 降至 0.839。这表明层次化跨模态对齐的两个组件各自贡献独立且不可替代。

### 3. 文本-运动语义融合：从简单拼接/单层注意力到自适应门控融合

在将文本语义注入运动生成的过程中，HESP 摒弃了简单的特征拼接或单层注意力，转而采用可学习的自适应门控融合机制。增强后的上下文表示通过 sigmoid 门控将运动摘要 $m_b$ 与词嵌入 $c_{eg_{b,\ell}}$ 进行凸组合：

$$c_{b,\ell}^{\mathrm{enh}} = \mathrm{LayerNorm}\big(g_{b,\ell} \odot m_{b} + (1 - g_{b,\ell}) \odot c_{eg_{b,\ell}}\big)$$

这一设计使模型能够根据当前生成状态动态调节文本语义与运动先验的混合比例，而非机械地使用固定权重。与 **SALAD** (Hong et al., CVPR 2025) 等基线相比，HESP 在 HumanML3D 和 KIT-ML 两个数据集上均取得了最优或次优的 FID 与 R-Precision（Table 1），同时保持了更高的运动多样性和物理合理性（User Study）。

### 创新总结

HESP 的三项核心创新构成了一个因果链条：**AG-VAE 将潜在空间结构化**，为语义解耦提供了几何基础；**DCMM + HCA 实现了层次化跨模态推理**，确保文本语义在多粒度上与运动对齐；**自适应门控融合**则使语义注入过程具备动态调节能力。三者协同作用，使得 HESP 在文本-运动对齐精度、生成质量和潜在空间可解释性上全面超越现有基线。

## 整体框架

HESP 的整体 pipeline 围绕两条核心设计线索展开：**结构化潜在运动建模**与**层次化跨模态对齐**。图 2 给出了系统架构的全貌，左侧为 AG-VAE 构建的语义子流形潜在空间，右侧为融合 DCMM 与 HCA 的扩散生成器。

**输入与编码**。给定文本描述，HESP 使用 CLIP-ViT-B/32 作为文本主干提取词级和句子级特征。运动侧则以骨骼拓扑图 $S$ 为条件，通过骨骼-时间卷积（SkelConv + TempConv）与时空池化（STPool）将运动序列 $\mathbf{m}_{1:N}$ 编码为潜在向量 $\mathbf{z}$。

**AG-VAE：结构化潜在先验**。与传统 VAE 使用各向同性高斯先验不同，AG-VAE 将潜在运动空间显式建模为 $K$ 个语义子流形组成的时间自适应高斯混合：

$$p(z_t | S, T) = \sum_{k=1}^K \pi_k(t, S) \mathcal{N}(z_t | \mu_k(S), \Sigma_k(S, T))$$

其中混合权重 $\pi_k(t, S)$ 随时间和骨骼结构动态调整，使每个时间步的潜在表示能够根据语义在不同子流形之间软切换。这一设计从根源上缓解了标准 VAE 中潜在空间语义纠缠、簇边界模糊的问题（见图 1 对比）。

**扩散生成器：层次化跨模态融合**。扩散去噪过程并非简单地将文本条件注入，而是通过两个协同模块实现多粒度对齐：

- **DCMM（Dynamic Cross-Modal Memory）**：维护一个可学习的跨模态记忆库 $\mathcal{M}$，存储原型文本-运动对。以运动潜在均值和词嵌入均值拼接构造查询向量 $q = \varphi_q([\mathrm{mean}_t(z_t), \mathrm{mean}_w(c_w)])$，通过检索增强机制为去噪过程提供长程语义先验。

- **HCA（Hierarchical Cross-Modal Attention）**：执行两级注意力——局部词-关节注意力 $\mathcal{A}_{\mathrm{local}}$ 捕捉细粒度语义-动作对应，全局句子-轨迹注意力 $\mathcal{A}_{\mathrm{global}}$ 建模整体运动意图，最终通过可学习门控 $\lambda$ 进行凸组合融合：

$$\mathbf{h}_t = \lambda \mathcal{A}_{\mathrm{local}} + (1-\lambda) \mathcal{A}_{\mathrm{global}}$$

融合后的特征经自适应门控与运动摘要进行增强，形成最终的文本条件表示 $c_{b,\ell}^{\mathrm{enh}}$，注入扩散 U-Net 的各层。

**输出与训练**。去噪后的潜在向量经 AG-VAE 解码器重建为运动序列。整个框架以端到端方式训练，AG-VAE 的证据下界（ELBO）包含分解后的 KL 散度项，显式鼓励潜在空间的簇结构分离：

$$\mathcal{L} = \mathbb{E}_{q_\phi(\mathbf{z},k|\mathbf{x})}[\log p_\theta(\mathbf{x}|\mathbf{z},k)] - D_{\mathrm{KL}}(q_\phi(k|\mathbf{x}) \| p(k)) - \mathbb{E}_{q_\phi(k|\mathbf{x})}[D_{\mathrm{KL}}(q_\phi(\mathbf{z}|\mathbf{x},k) \| p(\mathbf{z}|k))]$$

**模块间因果关系**。AG-VAE 提供的结构化潜在空间降低了扩散模型对先验分布的建模难度，而 DCMM 与 HCA 则确保文本语义在多个粒度上精确注入去噪过程。消融实验（Table 4）证实：移除 DCMM 或 HCA 均会导致 R-Precision 和 FID 显著退化，验证了层次化跨模态对齐的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_CVPR2026_html_Lv_Hierarchical_Enhanc/figures/004_Figure_1.jpg]]
*Figure 1: Comparative analysis of latent space organization in Standard VAE versus AG-VAE. (a) Standard VAE exhibits a less structured, overlapping distribution in latent space. (b) AG-VAE demonstrates a clearly separated multimodal distribution, reflecting distinct motion dynamics. (c) The cluster probability distribution in AG-VAE shows well-defined cluster assignments, validating the semantic organization of motion patterns*

## 核心模块与公式推导

HESP 的核心架构由三个紧密协作的模块构成：**AG-VAE**（自适应高斯变分自编码器）、**DCMM**（动态跨模态记忆）和 **HCA**（分层跨模态注意力）。它们共同实现了从潜在空间结构化到层次化文本-运动对齐的完整链路。

### 3.1 AG-VAE：时间自适应高斯混合先验

现有扩散模型普遍采用标准 VAE 的各向同性高斯先验，导致潜在空间中不同语义的运动模式高度重叠、难以解耦。AG-VAE 的核心创新在于将潜在运动空间显式建模为**以骨骼拓扑和时间位置为条件的高斯混合子流形**，使每个高斯分量对应一类运动动态。

**时变混合先验**的形式为：

$$p(z_t | S, T) = \sum_{k=1}^K \pi_k(t, S) \mathcal{N}(z_t | \mu_k(S), \Sigma_k(S, T))$$

其中：
- $z_t$ 为第 $t$ 帧的潜在向量；
- $S$ 为骨骼拓扑图（编码关节点之间的空间连接关系）；
- $T$ 为时间位置索引；
- $K$ 为高斯分量数目（实验中取 $K=10$）；
- $\pi_k(t, S)$ 为时变混合系数，由骨骼拓扑和时间编码动态生成，使模型能够根据运动阶段自适应切换语义子流形；
- $\mu_k(S)$ 和 $\Sigma_k(S, T)$ 分别为各分量的均值与协方差，前者仅依赖骨骼结构，后者同时受时间信息调制。

这一设计的关键机制在于：**时间依赖性通过序列级后验 $q_\phi(\mathbf{z}, k|\mathbf{x})$ 隐式捕获**，每个时间步的软分配 $k$ 允许模型在不同粒度的语义子流形之间平滑过渡，而非硬性指派到单一簇。

**训练目标**采用分解后的证据下界（ELBO）：

$$\mathcal{L} = \mathbb{E}_{q_\phi(\mathbf{z},k|\mathbf{x})}[\log p_\theta(\mathbf{x}|\mathbf{z},k)] - D_{\mathrm{KL}}(q_\phi(k|\mathbf{x}) \| p(k)) - \mathbb{E}_{q_\phi(k|\mathbf{x})}[D_{\mathrm{KL}}(q_\phi(\mathbf{z}|\mathbf{x},k) \| p(\mathbf{z}|k))]$$

其中第一项为重建损失，后两项分别惩罚**簇分配分布**与**簇内潜在分布**偏离先验的程度。这种分解式的 KL 正则化迫使不同语义的运动在潜在空间中形成清晰分离的簇结构，如 Figure 1 所示：标准 VAE 呈现重叠混乱的分布，而 AG-VAE 展现出界限分明的多模态结构。

运动编码器采用**骨骼-时间卷积**提取特征：先通过骨骼图卷积（SkelConv）捕获关节空间关系，再经时序卷积（TempConv）建模运动动态，最后通过时空池化（STPool）压缩为潜在向量。这一编码路径确保潜在表示同时保留空间结构信息与时间演化特征。

### 3.2 DCMM：动态跨模态记忆检索

传统扩散模型中的交叉注意力仅在当前时间步的文本与运动特征之间进行平坦交互，缺乏对长程语义上下文的显式建模。DCMM 引入一个**可学习的跨模态记忆库** $\mathcal{M} = \{M_p\}_{p=1}^P$，存储 $P$ 个原型文本-运动对，实现检索增强的语义融合。

**查询向量的构造**如下：

$$q = \varphi_q([\mathrm{mean}_t(z_t), \mathrm{mean}_w(c_w)])$$

其中：
- $\mathrm{mean}_t(z_t)$ 为所有时间步运动潜在向量的平均池化，提供全局运动上下文；
- $\mathrm{mean}_w(c_w)$ 为所有词嵌入的平均池化，提供全局文本语义；
- $[\cdot, \cdot]$ 表示拼接操作；
- $\varphi_q$ 为可学习的查询投影网络。

查询向量 $q$ 与记忆库中所有原型进行注意力匹配，检索出与当前文本-运动对最相关的长期语义先验。这一机制使模型能够**超越局部时间窗口的视野**，例如在生成“行走后坐下”序列时，DCMM 可检索到“坐下”相关的原型模式，辅助扩散过程在过渡阶段做出合理预测。

### 3.3 HCA：分层跨模态注意力与自适应门控融合

文本描述包含多层级语义：**词级别**（如“左手”、“向前”）对应局部关节运动，**句子级别**对应整体运动轨迹与风格。HCA 通过两阶段注意力机制分别捕获这两个层次的对齐关系：

$$\mathcal{A}_{\mathrm{local}} = \mathrm{softmax}\left(\frac{\mathcal{Q}_{\mathrm{motion}} K_{\mathrm{word}}^{\top}}{\sqrt{d}}\right) \mathcal{V}_{\mathrm{word}}$$

$$\mathcal{A}_{\mathrm{global}} = \mathrm{softmax}\left(\frac{\mathcal{Q}_{\mathrm{motion}} K_{\mathrm{sent}}^{\top}}{\sqrt{d}}\right) \mathcal{V}_{\mathrm{sent}}$$

$$\mathbf{h}_t = \lambda \mathcal{A}_{\mathrm{local}} + (1-\lambda) \mathcal{A}_{\mathrm{global}}$$

其中：
- $\mathcal{Q}_{\mathrm{motion}}$ 为运动特征的查询投影；
- $K_{\mathrm{word}}$、$\mathcal{V}_{\mathrm{word}}$ 为词级键和值（来自单个词的嵌入）；
- $K_{\mathrm{sent}}$、$\mathcal{V}_{\mathrm{sent}}$ 为句子级键和值（来自全局文本编码）；
- $d$ 为注意力维度；
- $\lambda$ 为**可学习的门控参数**，通过 sigmoid 激活动态调节局部与全局注意力的融合比例。

最终，DCMM 检索到的记忆增强运动摘要 $m_b$ 与原始词嵌入 $c_{eg_{b,\ell}}$ 通过自适应门控进行凸组合：

$$c_{b,\ell}^{\mathrm{enh}} = \mathrm{LayerNorm}\big(g_{b,\ell} \odot m_{b} + (1 - g_{b,\ell}) \odot c_{eg_{b,\ell}}\big)$$

其中 $g_{b,\ell}$ 为 sigmoid 门控值，$\odot$ 表示逐元素乘法。LayerNorm 确保融合后的表示在训练中保持数值稳定。这一设计使模型能够根据具体语义需求**灵活决定记忆先验与原始文本信息的贡献比例**。

### 3.4 模块协同与因果链路

三个模块形成一条清晰的因果链：**AG-VAE** 提供结构化、语义可分的潜在空间 → **DCMM** 在扩散生成过程中检索长期跨模态先验 → **HCA** 将检索到的语义信息以分层方式注入运动特征。消融实验（Table 4）证实了这一协同关系的关键性：移除 DCMM 导致 R-Precision Top-3 从 0.871 降至 0.847，移除 HCA 进一步降至 0.839，同时 FID 显著恶化，表明层次化跨模态对齐对生成质量和解耦能力均不可或缺。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_CVPR2026_html_Lv_Hierarchical_Enhanc/figures/005_Figure_3.jpg]]
*Figure 3: Compare the mean squared error (MSE) between the standard VAE and AG-VAE in data reconstruction tasks. AG-VAE demonstrates superior reconstruction performance, with the MSE decreasing from 0.3584 for the standard VAE to 0.2981, a relative improvement of 16.84%, indicating that the improved model architecture has a significant advantage in data reconstruction*

## 实验与分析

### 1. 实验设置

HESP基于PyTorch实现，运动编码器/解码器采用Transformer架构，文本主干网络为CLIP-ViT-B/32。AG-VAE中高斯混合分量数设为K=10。所有实验均在HumanML3D和KIT-ML两个标准基准上进行评估，使用与多个基线方法相同的评估协议和文本编码器，确保比较的公平性。

### 2. 主实验结果

#### 2.1 文本-运动生成质量

Table 1展示了HESP与现有方法在HumanML3D和KIT-ML测试集上的定量对比。HESP在FID、R-Precision等核心指标上达到最优或次优水平，同时保持更高的运动多样性和物理合理性。与**SALAD**（Hong et al., CVPR 2025）、**MoMask**（Guo et al., CVPR 2024）和**MDM**（Tevet et al., ICLR 2023）等代表性方法相比，HESP在文本-运动对齐方面展现出一致性的优势。值得注意的是，这一优势独立于扩散参数化方式，验证了层次化跨模态对齐机制的通用性。

#### 2.2 潜在空间结构质量

AG-VAE对潜在运动空间的结构化建模效果在Table 2中得到量化验证。在HumanML3D测试集上，AG-VAE的Calinski-Harabasz（CH）指数达到48.81，而标准VAE仅为11.95；Davies-Bouldin（DB）指数从7.83降至5.39。CH指数越高、DB指数越低，表明潜在空间中不同语义类别的簇间分离度越好、簇内紧密度越高。这一结果直接支撑了论文的核心主张：将潜在空间显式建模为时间自适应高斯混合子流形，能有效解耦不同运动语义。

Figure 1的潜在分布可视化进一步印证了上述结论：标准VAE的潜在分布呈现重叠、无结构特征，而AG-VAE展现出清晰分离的多模态分布，各簇对应不同的运动动力学模式。

### 3. 重建质量分析

Figure 3对比了标准VAE与AG-VAE在运动数据重建任务上的均方误差（MSE）。AG-VAE将MSE从0.3584降至0.2981，相对提升16.84%。这一显著改善源于AG-VAE以骨骼拓扑为条件的时间自适应混合先验，使潜在表示能够更精确地捕捉运动的时空结构。

Table 3进一步对比了不同VAE模型的重建质量与参数量。AG-VAE在保持较低重建误差的同时，参数量控制合理，体现了结构化潜在建模在效率与性能之间的良好平衡。

### 4. 消融研究

Table 4的消融实验系统验证了HESP各核心组件的贡献：

- **移除DCMM模块**：R-Precision Top-3从0.871降至0.847，FID显著上升。这表明动态跨模态记忆模块对于长期语义检索和文本-运动一致性至关重要。
- **移除HCA模块**：R-Precision Top-3从0.871降至0.839，FID同样恶化。分层跨模态注意力机制通过同时捕获词-关节的局部对齐和句子-轨迹的全局对齐，是层次化语义融合的关键。
- **AG-VAE的对抗引导**：相较于标准VAE，AG-VAE通过对抗训练获得的高斯混合先验产生了更清晰的簇边界，这在Table 2的聚类指标中已得到充分验证。

消融结果一致表明：DCMM和HCA的协同作用是HESP实现层次化跨模态对齐的核心机制，任一模块的缺失都会导致文本-运动语义一致性的显著退化。

### 5. 定性分析

Figure 4展示了MDM、SALAD和HESP在相同文本提示下的生成运动定性对比。HESP生成的动作为了更精确地匹配文本描述的语义细节，尤其在涉及多部位协调和时序动态的复杂描述上表现更优。Figure 5通过t-SNE降维可视化展示了AG-VAE潜在空间中样本的聚类分布，不同颜色代表不同语义簇，进一步验证了语义子流形的清晰分离。

### 6. 局限性与失败模式

尽管HESP在主要指标上表现优异，论文仍指出以下局限：

1. **语义过渡处理**：当文本描述缺乏明确的过渡线索时，处理语义不同运动之间的突然过渡仍然具有挑战性，可能导致生成动作的不连贯。
2. **长序列生成**：生成高质量的长时间单人物动作序列仍是难点，模型在长程时序一致性上可能出现退化。
3. **熵正则化平衡**：需要进一步研究熵正则化混合先验，以在运动多样性与可控性之间取得更优平衡。
4. **多人交互**：当前方法仅支持单人物运动生成，多人动作的交互生成是未来值得探索的方向。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_CVPR2026_html_Lv_Hierarchical_Enhanc/figures/007_Table_2.jpg]]
*Table 2: Quantitative comparison of latent-space structure metrics on the HumanML3D test set. Higher Calinski-Harabasz (CH) and Cluster Separation (CS) values, and lower Davies-Bouldin (DB) index, indicate better-organized latent representations. All scores are computed under identical cluster labels produced by the AG-VAE classifier*

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_CVPR2026_html_Lv_Hierarchical_Enhanc/figures/010_Table_4.jpg]]
*Table 4: Ablation studies on the HESP*

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_CVPR2026_html_Lv_Hierarchical_Enhanc/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative Comparison Analysis of Results Generated by MDM [38], SALAD [16], and Ours*

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_CVPR2026_html_Lv_Hierarchical_Enhanc/figures/009_Table_3.jpg]]
*Table 3: Quantitative results on the quality and accuracy of reconstructed motion features of VAE models from different methods, along with the number of trainable parameters, measured on the test set of HumanML3D*

## 方法谱系与知识库定位

### 1. 瓶颈诊断与核心差异

当前文本驱动运动生成的扩散模型普遍采用**各向同性高斯先验**与**平坦的跨模态监督**，这导致潜在空间呈现语义纠缠、缺乏可解释结构，进而限制了运动生成的可控性与语义一致性。HESP 的根本突破在于将这一瓶颈显式建模为两个因果可操作的维度：（1）潜在运动空间的语义组织；（2）文本-运动对齐的层次化推理。

具体而言，HESP 将**潜在先验建模**从标准 VAE 的各向同性高斯分布替换为**时间自适应高斯混合先验**（AG-VAE），以骨骼拓扑为条件将潜在空间分解为多个语义子流形；将**跨模态对齐方式**从平坦交叉注意力或 CLIP 条件注入升级为**动态跨模态记忆（DCMM）+ 分层跨模态注意力（HCA）+ 自适应门控融合**的三级层次化架构。这一“结构化潜在建模 + 层次化跨模态推理”的组合构成了 HESP 区别于现有方法的核心因果杠杆。

### 2. 与基线工作的关系定位

HESP 在扩散生成范式上与以下代表性工作构成直接比较关系：

- **MDM**（Tevet et al., ICLR 2023）：作为运动扩散模型的奠基性工作，MDM 直接在原始运动空间进行扩散去噪，未对潜在空间进行结构化建模。HESP 在潜在空间中引入语义子流形，从根本上改变了先验分布的形式，从而在 FID 和 R-Precision 上取得显著优势。

- **MoMask**（Guo et al., CVPR 2024）：采用生成式掩码建模策略，关注运动 token 的离散化表示。HESP 与之不同，在连续潜在空间中进行结构化先验建模，并通过层次化跨模态注意力实现更细粒度的文本-运动对齐。

- **SALAD**（Hong et al., CVPR 2025）：引入骨骼感知的潜在扩散，是当前最先进的方法之一。HESP 在 SALAD 的基础上进一步推进了潜在空间的组织化程度——AG-VAE 的时间自适应混合先验相比 SALAD 的骨骼条件化策略，提供了显式的多模态簇结构与动态组分切换能力，这在潜在空间聚类指标上体现为 CH 指数从 11.95（标准 VAE）跃升至 48.81。

### 3. 适用边界与局限

尽管 HESP 在多个基准上取得了领先或次优的性能，其方法设计仍存在明确的适用边界：

- **语义突变过渡**：当文本描述缺乏显式的过渡线索时，HESP 在处理语义不同运动之间的突然切换仍然具有挑战性。AG-VAE 的时间自适应混合先验虽能捕捉帧级语义切换，但跨簇的平滑过渡机制尚未被显式建模。

- **熵正则化与多样性-可控性权衡**：论文明确指出需要进一步研究熵正则化混合先验，以平衡运动生成的多样性与可控性。当前 AG-VAE 的混合组分数量 K=10 是固定的超参数，其与运动语义粒度的最优匹配关系仍需探索。

- **长序列与多人交互**：HESP 当前聚焦于单人物中等长度运动序列的生成。生成高质量的长时序单人物动作序列，以及扩展至多人交互场景，是论文明确指出的未来方向。

### 4. 开放问题与知识库贡献

HESP 为社区贡献了以下可迁移的知识模块与开放研究问题：

**知识贡献**：
- **AG-VAE 的时间自适应混合先验**（Eq 1）：将骨骼拓扑 S 和时间位置 T 作为混合高斯先验的条件，为其他需要结构化潜在建模的时序生成任务提供了可复用的先验设计范式。
- **DCMM 的跨模态记忆检索机制**（Eq 3）：通过平均池化的运动潜在向量与词嵌入拼接形成查询向量，从可学习的记忆库中检索长期语义先验，为跨模态生成中的记忆增强方法提供了验证有效的实现方案。
- **分层跨模态注意力与自适应门控融合**（Eq 4-5）：局部词-关节注意力与全局句子-轨迹注意力的两级设计，配合可学习门控 λ 的凸组合融合，构成了层次化跨模态对齐的通用架构模式。

**开放问题**：
1. 如何利用熵正则化混合先验在运动生成中实现多样性与可控性的精细平衡？
2. 在文本缺少显式过渡线索的条件下，如何建模语义不同运动之间的平滑过渡？
3. 如何将 HESP 的层次化对齐框架扩展至长序列多人交互运动生成？

**证据强度说明**：上述局限与开放问题均直接来自论文的讨论部分，属于作者明确承认的研究边界。关于 AG-VAE 与标准 VAE 的对比证据（重建 MSE 从 0.3584 降至 0.2981，CH 指数从 11.95 升至 48.81）来自 Figure 3 和 Table 2，置信度分别为 0.98 和 0.95，属于强证据。消融实验中移除 DCMM 或 HCA 导致 R-Precision Top-3 分别从 0.871 降至 0.847 和 0.839（Table 4），置信度 0.95，进一步验证了层次化跨模态对齐的因果作用。

## 原文 PDF

![[paperPDFs/CVPR_2026/Hierarchical_Enhancement_of_Semantic_Priors_for_Disentangled_Text_Driven_Motion_Generation.pdf]]