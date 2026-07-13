---
title: "SegMoTE: Token-Level Mixture of Experts for Medical Image Segmentation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SegMoTE_Token_Level_Mixture_of_Experts_for_Medical_Image_Segmentation.pdf
project_link: null
code_link: "https://github.com/InMyDreammer/SegMoTE"
aliases:
- SegMoTE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入令牌级专家路由机制（MoTE）和渐进提示令牌化（PPT），冻结SAM编码器，仅更新轻量专家令牌，实现模态特异性自适应和高效推理。
primary_logic: 通过可学习的专家令牌集合和噪声top-k门控动态选择最适合当前模态的专家路径，结合负载平衡损失保障专家分工，在极少可训练参数（17M）和高品质小数据集（MedSeg-HQ）上显著提升跨模态分割泛化性，同时保持SAM的原始零样本能力。
claims:
- 在多个分布外数据集上，SegMoTE仅使用0.15M高质量掩码训练，性能较第二优方法提升1%-6%。
- SegMoTE的可训练参数仅17M，约为SAM的1.4%，但性能超越大规模全微调方法。
- MoTE路由的热力显示稀疏、离散的“责任区域”，验证了令牌级专家对不同模态的有效选择性。
- PPT消融表明，使用Q=2查询令牌在ISLES数据集上Dice从59.00提升至65.28（+6.28），显著降低了对人工提示的依赖。
---

# SegMoTE: Token-Level Mixture of Experts for Medical Image Segmentation

> [!tip] 核心洞察
> 通过可学习的专家令牌集合和噪声top-k门控动态选择最适合当前模态的专家路径，结合负载平衡损失保障专家分工，在极少可训练参数（17M）和高品质小数据集（MedSeg-HQ）上显著提升跨模态分割泛化性，同时保持SAM的原始零样本能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | SegMoTE：用于医学图像分割的令牌级专家混合网络 |
| 英文题名 | SegMoTE: Token-Level Mixture of Experts for Medical Image Segmentation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.19213) · [Code](https://github.com/InMyDreammer/SegMoTE) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SegMoTE |
| Dataset | Out-of-domain datasets, Multi-dataset (AMOS CT, AMOS MRI, BTCV, CHAOS T1, ISIC2018, SZ-CXR, ISLES, SegThor, TotalSegmentator MRI) under bounding-box |

> [!tip] 效果简介
> - Out-of-domain datasets (ISLES, SegThor, TotalSegmentator MRI) 上，Dice (%) ISLES: 77.30, SegThor Avg: 83.39, TotalSeg Avg: 71.48 vs 第二优方法（具体数值未列出） (+1%至6%)。
> - Multi-dataset (AMOS CT, AMOS MRI, BTCV, CHAOS T1, ISIC2018, SZ-CXR, ISLES, SegT... 上，Dice (%) AMOS CT 85.16, AMOS MRI 80.27, BTCV 84.51, CHAOS T1 89.00, ISIC2018 93.02, SZ-C... vs SAM, SAM2, SAM-Med2D, IMIS（具体分数未提供） (显著提升)。

## 概要

医学图像分割面临模态异质性的根本挑战：CT、MRI、X光、皮肤镜等不同成像模态在对比度、分辨率和解剖结构上差异显著，传统方法通常采用全参数微调或统一解码器处理所有模态，缺乏模态特异性的自适应机制。大规模无差别数据聚合不仅引入监督噪声，还导致负迁移，使模型在分布外场景下泛化能力严重退化。**SegMoTE** 针对这一瓶颈，提出令牌级专家混合（Mixture of Token Experts, MoTE）机制，在冻结 SAM 编码器的前提下，通过可学习的专家令牌集合和噪声 top-k 门控，动态选择最适合当前模态的专家路径，以极少可训练参数实现模态特异性自适应。

核心创新在于两点：其一，**MoTE 机制**将模态自适应的粒度下沉到令牌级别，每个令牌独立路由到最相关的专家，并通过负载平衡损失（以平方变异系数 $CV^2$ 约束）保障专家分工的均衡性；其二，**渐进提示令牌化（Progressive Prompt Tokenization, PPT）** 通过随机抽样掩码和文本提示自动生成前/背景令牌，使模型在推理阶段无需人工交互即可完成二分类分割，显著降低了对显式视觉提示的依赖。

在仅使用 0.15M 高质量掩码（MedSeg-HQ 数据集）训练的条件下，SegMoTE 仅更新约 17M 参数（约为 SAM 总参数的 1.4%），在多个分布外数据集上较第二优方法提升 1%–6% Dice 分数，同时保持了 SAM 的原始零样本能力。这一结果表明，**数据质量与模态自适应机制的结合**可以替代大规模数据堆砌，为医学图像分割的高效泛化提供了新范式。



### 医学图像分割的异构性挑战

医学图像分割面临的核心瓶颈在于成像模态的极端异构性。CT、MRI、X射线、超声、皮肤镜等不同模态在对比度、分辨率、解剖结构和病理表现上差异显著，导致单一模型难以在所有模态上保持稳定性能。传统方法通常采用**全参数微调**或**解码器部分微调**的策略，将大规模混合数据直接注入预训练模型（如SAM）进行训练。然而，这种无差别的数据聚合方式带来了两个深层问题：

1. **监督噪声与负迁移**：不同模态之间的特征分布冲突会在训练过程中引入相互矛盾的梯度信号，导致模型对某些模态过拟合而对另一些模态欠拟合。正如Figure 4所示，现有医学数据集的SAM编码器特征嵌入在降维后呈现出重叠和不平滑的过渡区域，而高质量数据集MedSeg-HQ则表现出更平滑、连续的特征分布，这暗示了数据质量与特征一致性之间的强关联。

2. **预训练能力的灾难性遗忘**：全微调会显著改变SAM原有的特征空间，破坏其在自然图像上积累的零样本泛化能力（Figure 1a）。即使参数高效的微调方法（如Adapter、LoRA）减轻了参数量负担，它们仍使用统一的输出令牌处理所有模态，缺乏对模态特异性特征的显式建模。

### 现有方法的缺口

当前医学图像分割的主流方案可归纳为三类，各自存在明显局限：

| 方法类别 | 代表工作 | 核心策略 | 关键缺陷 |
|---------|---------|---------|---------|
| **全微调SAM** | **MedSAM** (Ma et al., Nature Communications 2024) | 在百万级医学图像上全参数微调SAM | 参数量大（93M可训练参数），分布偏移导致零样本能力丧失 |
| **大规模数据微调** | **SAM-Med2D** | 在超大规模医学数据集上微调 | 数据噪声累积，跨模态泛化能力有限 |
| **密集交互标注** | **IMIS** | 依赖密集标注进行交互式分割 | 推理时需人工提示，无法实现自动化 |

这些方法的共同盲点在于：**缺乏对模态异构性的自适应机制**。它们将“更多数据”和“更多参数”视为提升性能的唯一路径，却忽视了模态间特征冲突对模型泛化的根本性制约。

### 本文的核心动机

SegMoTE的提出基于一个关键洞察：**医学图像分割的跨模态泛化不应依赖暴力数据聚合，而应通过轻量级的模态自适应路由机制，在保持预训练模型原始能力的前提下，动态激活最适合当前模态的专家路径**。

具体而言，本文试图回答以下问题：
- 能否在不修改SAM编码器、仅引入极少可训练参数（约17M，仅占SAM的1.4%）的条件下，实现多模态医学图像的自适应分割？
- 能否通过令牌级（token-level）的专家混合机制，让模型自动学习不同模态的“责任区域”，从而避免模态间的梯度冲突？
- 能否在高质量但小规模的数据集（MedSeg-HQ，仅0.15M标注）上训练，仍取得超越大规模全微调方法的分布外泛化性能？

这些问题的解答构成了SegMoTE方法设计的核心驱动力，也即本文所提出的**令牌级专家混合（MoTE）**与**渐进提示令牌化（PPT）**两大创新机制的出发点。



## 核心方法与创新机理

SegMoTE 的核心创新在于将**令牌级专家混合（Mixture of Token Experts, MoTE）** 引入 SAM 的掩码解码器，解决了医学图像分割中**异构模态缺乏自适应机制**这一关键瓶颈。与此前方法（如 MedSAM、SAM-Med2D）采用全参数微调或解码器部分微调、使用统一输出令牌处理所有模态不同，SegMoTE 冻结 SAM 编码器，仅更新轻量级的 MoTE 和渐进提示令牌化（PPT）模块，以极少的可训练参数（**17M**，仅占 SAM 总参数量的约 1.4%）实现了模态特异性自适应。

### 从统一处理到令牌级动态路由

传统方法的自适应缺陷源于其“一刀切”的设计：无论输入是 CT、MRI 还是 X 光，解码器中的令牌更新路径完全相同。这导致两个问题：其一，大规模无差别数据聚合引入的监督噪声和负迁移会损害模型在分布外场景的泛化能力；其二，全参数微调会破坏 SAM 预训练获得的通用视觉知识，造成预训练能力的退化。

SegMoTE 通过两个 **changed slots** 从根本上改变了这一范式：

**1. 自适应机制：从全参数微调到令牌级专家路由**

基线方法（如 MedSAM, Ma et al., Nature Communications 2024）对掩码解码器进行全参数微调，所有模态共享同一组输出令牌。SegMoTE 则引入一组可学习的专家令牌，并通过**噪声 top-k 门控**动态选择最适合当前输入模态的专家路径。

具体而言，对于每个令牌的隐藏状态 $\mathbf{X} \in \mathbb{R}^{B \times T \times D}$，路由门控首先计算其在所有 $E$ 个专家上的对数得分：

$$\mathrm{L} = \mathrm{XW_g} \in \mathbb{R}^{B \times T \times E}$$

为避免门控过早收敛到少数专家，MoTE 对路由权重注入高斯噪声，鼓励探索：

$$\tilde{\mathbf{L}} = \mathbf{L} + (\mathrm{softplus}(\mathbf{X}\mathbf{W}_n) + \varepsilon) \odot \mathbf{Z}, \quad \mathbf{Z} \sim \mathcal{N}(0, 1)$$

随后通过 top-k 选择激活 $k$ 个专家，计算置信度加权输出，并施加**负载平衡损失** $\mathcal{L}_{\mathrm{balance}}$ 以平方变异系数（$\mathrm{CV}^2$）约束专家重要性和负载的均衡分布：

$$\mathcal{L}_{\mathrm{balance}} = \mathrm{CV}^2\left(\{\mathrm{imp}_e\}_{e=1}^{E}\right) + \mathrm{CV}^2\left(\{\mathrm{load}_e\}_{e=1}^{E}\right)$$

这一设计的因果机制在于：**负载平衡损失保障了不同专家在训练中形成差异化分工**，而噪声门控则防止模型退化为“赢家通吃”的单一路径。消融实验证实，专家数量 $N=4$、激活数 $M=1$ 时在多模态训练中达到最佳性能（Figure 6(b)(c)），验证了适当的专家组合平衡了表达性和效率。路由热力可视化进一步显示，不同专家令牌在不同模态上形成了稀疏、离散的“责任区域”（Figure 7），直接证明了令牌级专家对模态的有效选择性。

**2. 提示方式：从人工交互到渐进提示令牌化**

SAM 及其医学变体在推理时依赖用户通过点击或边界框提供显式视觉提示，这在临床部署中构成人工负担。SegMoTE 提出的**渐进提示令牌化（PPT）** 通过随机抽样的掩码和文本提示自动生成前景/背景令牌，无需人工交互即可完成二分类分割。

PPT 的核心机制是：可学习的查询令牌 $Q$ 通过对归一化图像特征执行多头注意力，交替利用掩码提示和文本提示作为前景先验，逐步将潜在特征转化为语义对齐的特征令牌。消融实验表明，在分布外数据集 ISLES 上，使用 $Q=2$ 查询令牌时 Dice 从无 PPT 的 59.00 提升至 65.28（+6.28），显著降低了对人工提示的依赖（Table 4）。

### 创新的协同效应

MoTE 和 PPT 并非孤立运作，二者在冻结的 SAM 编码器之上形成协同：PPT 生成的语义对齐令牌进入掩码解码器后，经过自注意力和令牌-图像注意力，再由 MoTE 进行动态专家选择和令牌更新。这种设计使得模型在保持 SAM 原始零样本能力的同时，以极小的训练代价（17M 参数，0.15M 高质量掩码）在多个分布外数据集上较第二优方法提升 1%–6%（Table 1, Table 2）。



SegMoTE 在冻结的 SAM 基础架构之上，构建了一条“模态无关编码 → 语义令牌化 → 令牌级专家自适应解码”的轻量推理管线。其核心设计目标是：**在仅更新约 17M 可训练参数（约为原始 SAM 的 1.4%）的前提下，赋予模型对异构医学图像模态的自适应能力，同时保留 SAM 原有的零样本分割潜力**。整体框架如 Figure 2 所示。

![[assets/figures/papers/paper_list_l2139_https_arxiv_org_abs_2602_19213/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed SegMoTE framework. SegMoTE extends SAM by introducing a token-level expert routing mechanism to enable adaptive multimodal medical image segmentation. The frozen SAM encoder extracts modality-agnostic embedding representations, while the progressive prompt tokenization transforms latent features into semantically aligned feature tokens. These tokens interact with the decoder layers and MoTE for dynamic expert selection and adaptive token updates*

### 冻结编码器与模态无关特征提取

管线的起点是 **SAM Encoder**（冻结，不参与训练）。输入图像 $X$ 首先经过该编码器提取模态无关的视觉嵌入 $f$。冻结编码器的关键作用有二：其一，避免大规模微调导致的预训练知识灾难性遗忘与分布偏移；其二，为下游的轻量自适应模块提供一个稳定、高质量的特征基座。后续所有可学习的自适应操作均建立在这个冻结特征之上。

### 渐进提示令牌化（PPT）

编码器输出的特征图进入 **Progressive Prompt Tokenization (PPT)** 模块（Figure 3）。PPT 的设计目标是在推理阶段**完全替代人工交互**（如点击、边界框），实现自动二分类分割。其工作流程为：

1. **随机抽样掩码与文本提示**：训练时，PPT 从真实标签中随机采样前景/背景掩码区域，并结合对应的文本提示（如“foreground”/“background”），构造前景先验。
2. **可学习查询令牌 $Q$**：通过多头注意力机制，$Q$ 在归一化后的图像特征上学习前景与背景之间的关系，将潜在特征图转化为语义对齐的特征令牌。
3. **渐进式引导**：PPT 交替使用掩码提示和文本提示，逐步将提示令牌引导至前景和背景区域，最终输出与分割目标语义一致的令牌表示。

消融实验表明，PPT 对分布外数据尤为关键——在 ISLES 数据集上，引入 $Q=2$ 的查询令牌后，Dice 从 59.00 跃升至 65.28（+6.28），验证了自动提示对降低人工依赖的有效性。

### 掩码解码器与令牌级专家混合（MoTE）

PPT 输出的语义令牌进入 **Mask Decoder**，这是整个框架中唯一被解冻并参与训练的原始 SAM 组件。每个解码器层依次执行：

1. **自注意力**：在令牌之间建模全局依赖。
2. **令牌-图像交叉注意力**：将令牌与编码器的图像特征进行交互。
3. **MoTE 动态专家选择与令牌更新**：交叉注意力的输出被送入 **Mixture of Token Experts (MoTE)** 模块，这是 SegMoTE 实现模态自适应的核心。

MoTE 维护一组可学习的**专家令牌**（$N$ 个，默认 $N=4$），每个专家令牌代表一种模态特定的处理能力。其工作机制如下：

- **路由门控**：给定输入令牌 $X \in \mathbb{R}^{B \times T \times d}$，首先通过门控权重矩阵 $W_g$ 计算路由 logits：
  $$\mathrm{L} = \mathrm{X W_g} \in \mathbb{R}^{B \times T \times E}$$
- **噪声 top-k 选择**：为鼓励探索、防止过早收敛到单一专家，对 logits 注入高斯噪声后进行 top-k 选择（默认 $k=1$）：
  $$\tilde{\mathbf{L}} = \mathbf{L} + (\mathrm{softplus}(\mathbf{X}\mathbf{W}_n) + \varepsilon) \odot \mathbf{Z}, \quad \mathbf{Z} \sim \mathcal{N}(0,1)$$
- **置信度加权融合**：每个令牌的最高专家得分作为置信度 $c_{b,t}$，用于对所选专家的输出进行加权组合。
- **负载平衡损失**：为防止专家退化（所有令牌路由到同一专家），引入基于平方变异系数 $CV^2$ 的负载平衡损失：
  $$\mathcal{L}_{\mathrm{balance}} = \mathrm{CV}^2\left(\{\mathrm{imp}_e\}_{e=1}^{E}\right) + \mathrm{CV}^2\left(\{\mathrm{load}_e\}_{e=1}^{E}\right)$$
  其中 $\mathrm{imp}_e$ 为专家 $e$ 的权重和（重要性），$\mathrm{load}_e$ 为非零路由计数（负载）。

路由可视化（Figure 7）揭示了 MoTE 的关键行为：不同模态下，专家令牌呈现出**稀疏、离散的激活模式**，形成所谓的“责任区域”。这表明专家令牌确实学会了针对特定模态（如 CT、MRI、X 光）进行选择性响应，而非无差别激活。

### 端到端训练与推理

整个框架的训练损失由两部分组成：
- **分割损失**：采用 Dice Loss，衡量预测掩码与真实标签的重叠程度：
  $$L_{\mathrm{seg}}(y^E, \mathbf{y}) = 1 - \frac{2\sum_i y_i^E y_i}{\sum_i y_i^E + \sum_i y_i}$$
- **负载平衡损失** $\mathcal{L}_{\mathrm{balance}}$，通过超参数加权后与分割损失联合优化。

训练时，SAM 编码器保持冻结，仅更新 MoTE（约 10M 参数）、PPT（约 7M 参数）以及解冻的掩码解码器参数。推理时，PPT 自动生成提示令牌，MoTE 根据输入模态动态路由至最合适的专家，最终输出分割掩码，全程无需人工交互。

### 补充图表

![[assets/figures/papers/paper_list_l2139_https_arxiv_org_abs_2602_19213/figures/001_Figure_1.jpg]]
*Figure 1: SegMoTE vs. Previous Works. The heterogeneous data X is first processed by the encoder ε to extract the feature representation f . (a) Previous methods typically perform full fine-tuning of the mask decoder or parameter-efficient fine-tuning, leading to distribution shift from the pretrained model. (b) Seg-MoTE introduces a token-level mixture of experts mechanism that dynamically selects modality-adaptive expert tokens while keeping the mask decoder frozen. The process is guided by the load balancing loss*



### 3.1 整体架构与设计动机

SegMoTE 的核心设计动机源于一个瓶颈：传统方法对异构医学图像模态缺乏自适应机制，大规模无差别数据聚合会引入监督噪声和负迁移，导致模型在分布外场景的泛化能力严重退化。其因果调控旋钮是：**冻结 SAM 编码器**，仅引入并更新两个轻量级模块——**令牌级专家混合（Mixture of Token Experts, MoTE）** 和 **渐进提示令牌化（Progressive Prompt Tokenization, PPT）**——以极少的可训练参数（17M，仅占 SAM 总参数量的 1.4%）实现模态特异性自适应。

整体流程如 Figure 2 所示：冻结的 SAM 编码器提取模态无关的图像嵌入；PPT 将潜在特征转化为语义对齐的特征令牌；这些令牌进入 Mask Decoder，依次执行自注意力、令牌-图像交叉注意力，然后交由 MoTE 进行动态专家选择与令牌更新。

### 3.2 令牌级专家混合（MoTE）

MoTE 是该方法的理论核心，其目标是在令牌级别实现动态的专家选择与融合。具体而言，模型维护一组可学习的专家令牌集合，每个专家令牌对应一种模态特异性的处理能力。对于输入的每个令牌，通过一个可学习的路由门控（Router）决定其由哪些专家处理。

**路由得分计算**（Eq. 1）：给定输入令牌张量 $\mathbf{X} \in \mathbb{R}^{B \times T \times d}$（$B$ 为批量大小，$T$ 为令牌数，$d$ 为特征维度），通过门控权重矩阵 $\mathbf{W}_g$ 计算所有专家上的原始得分：

$$\mathrm{L} = \mathbf{X} \mathbf{W}_g \in \mathbb{R}^{B \times T \times E}$$

其中 $E$ 为专家总数。

**噪声 Top-k 门控**（Eq. 2）：为防止路由过早收敛到单一专家（即“赢者通吃”的退化现象），对路由得分注入可学习的高斯噪声，鼓励探索：

$$\tilde{\mathbf{L}} = \mathbf{L} + \big(\mathrm{softplus}(\mathbf{X} \mathbf{W}_n) + \varepsilon\big) \odot \mathbf{Z}, \quad \mathbf{Z} \sim \mathcal{N}(0, 1)$$

其中 $\mathbf{W}_n$ 为噪声权重，$\varepsilon$ 为小常数防止除零，$\mathbf{Z}$ 为标准高斯噪声。随后对 $\tilde{\mathbf{L}}$ 进行 Top-k 选择，仅保留得分最高的 $k$ 个专家，其余置零，经 Softmax 归一化后得到路由权重矩阵 $\mathbf{G} \in \mathbb{R}^{B \times T \times E}$。

**令牌置信度得分**（Eq. 4）：每个令牌的最高专家得分作为其置信度，用于后续的加权融合：

$$c_{b,t} = \max_{j=1,\ldots,k} \mathbf{s}_{b,t}[j]$$

其中 $\mathbf{s}_{b,t}$ 为令牌 $(b,t)$ 在 Top-k 专家上的 Softmax 得分向量。

**负载平衡损失**（Eq. 8）：为确保各专家被均衡利用，定义专家重要性 $\operatorname{imp}_e = \sum_{b,t} \mathbf{G}_{b,t,e}$（权重和）和专家负载 $\operatorname{load}_e = \sum_{b,t} \mathbf{1}(\mathbf{G}_{b,t,e} > 0)$（非零计数），通过两者的平方变异系数（$CV^2$）构建损失：

$$\mathcal{L}_{\mathrm{balance}} = CV^2\big(\{\operatorname{imp}_e\}_{e=1}^{E}\big) + CV^2\big(\{\operatorname{load}_e\}_{e=1}^{E}\big)$$

该损失促使专家分工明确，避免某些专家被过度使用而另一些被闲置。消融实验（Figure 6(b)(c)）表明，在 4 或 7 个模态上训练时，$E=4$ 专家、$k=1$ 激活的组合达到最佳性能，验证了适当的专家组合在表达性与效率之间的平衡。

### 3.3 渐进提示令牌化（PPT）

PPT 针对的是传统 SAM 依赖人工交互（点击或边界框）提供显式视觉提示的局限。其核心思想是：通过随机采样的掩码提示和文本提示，引导可学习的查询令牌 $Q$ 自动捕捉前景与背景的关系，实现无需人工干预的二分类分割。

如 Figure 3 所示，PPT 交替使用掩码提示和文本提示作为前景先验，可学习的查询 $Q$ 在归一化的图像特征上执行多头注意力，逐步将潜在特征图转化为语义对齐的特征令牌。消融实验（Table 4）提供了关键证据：在分布外数据集 ISLES 上，使用 $Q=2$ 个查询令牌时，Dice 分数从无 PPT 的 59.00 提升至 65.28（+6.28），显著降低了对人工提示的依赖。

![[assets/figures/papers/paper_list_l2139_https_arxiv_org_abs_2602_19213/figures/003_Figure_3.jpg]]
*Figure 3: Architecture of the Progressive Prompt Tokenization. By randomly selecting mask and text prompts as foreground priors, the learnable query Q captures the relationship between the foreground and background by performing attention on the normalized image features*

### 3.4 分割损失

最终分割损失采用标准的 Dice Loss（Eq. 10），衡量预测掩码 $y^E$ 与真实标签 $\mathbf{y}$ 的重叠程度：

$$L_{\mathrm{seg}}(y^E, \mathbf{y}) = 1 - \frac{2\sum_i y_i^E y_i}{\sum_i y_i^E + \sum_i y_i}$$

总训练目标为 $L = L_{\mathrm{seg}} + \lambda L_{\mathrm{balance}}$，其中 $\lambda$ 为平衡系数。



## 实验与关键发现

### 核心性能验证

SegMoTE 在分布外（out-of-domain）场景下的泛化能力是其核心优势。如 **Table 1** 所示，在仅使用 0.15M 高质量掩码训练且可训练参数仅 17M 的条件下，SegMoTE 在 ISLES、SegThor 和 TotalSegmentator MRI 三个分布外数据集上全面超越现有方法，较第二优方法提升 **1% 至 6%** 的 Dice 分数。这一结果直接验证了令牌级专家路由机制对异构模态的自适应能力——传统方法因大规模无差别数据聚合引入监督噪声，而 SegMoTE 通过冻结 SAM 编码器、仅更新轻量级专家令牌，有效规避了负迁移问题。

![[assets/figures/papers/paper_list_l2139_https_arxiv_org_abs_2602_19213/figures/008_Table_1.jpg]]
*Table 1: Performance comparison on three out-of-domain datasets. Experimental results of SegMoTE in comparison to other methods under bounding-box interactions. Best results are highlighted in red, and second best results are highlighted in blue*

在多数据集边界框交互场景下（**Table 2**），SegMoTE 同样展现出跨模态鲁棒性：在 AMOS CT（85.16）、AMOS MRI（80.27）、BTCV（84.51）、CHAOS T1（89.00）、ISIC2018（93.02）、SZ-CXR（95.04）等九个数据集上均取得显著优势。值得注意的是，当解冻原始解码器参数并与 MoTE、PPT 联合训练时，SegMoTE 在二分类分割任务上相较基线提升 **3% 至 7%**，表明令牌级专家混合机制与解码器微调之间存在正向协同效应。

![[assets/figures/papers/paper_list_l2139_https_arxiv_org_abs_2602_19213/figures/010_Table_2.jpg]]
*Table 2: Experimental results on multiple datasets under bounding-box interactions. Our method involves unfreezing the original decoder parameters and training them along with the MoTE and PPT mechanisms on the MedSeg-HQ dataset*

### 参数效率分析

**Table 3** 的模型规模对比揭示了 SegMoTE 的极致参数效率：总可训练参数仅 **17M**（MoTE 占 10M，PPT 占 7M），约为原始 SAM（1191M）的 **1.4%**，也远低于 MedSAM（93M）的全微调方案。这一轻量化设计得益于两个关键选择：冻结 SAM 编码器保留了强大的视觉先验，而可学习的专家令牌集合仅需极少量参数即可实现模态特异性适配。在保持 SAM 原始零样本能力的同时，SegMoTE 以不到 1/10 的参数量超越大规模全微调方法，证明“选择性适配”比“全盘重训”在医学多模态场景下更具性价比。

### 消融研究

#### 专家配置

专家数量 N 与激活数 M 的消融实验（**Figure 6(b)(c)**）表明，**N=4、M=1** 在多模态联合训练（4 或 7 个模态）时达到最优性能。过少的专家（N=2）不足以覆盖模态多样性，而过多的专家（N=8）则引入冗余并可能导致路由分散。M=1 的稀疏激活策略迫使每个令牌选择单一专家，强化了专家的“责任区域”分工，这与负载平衡损失的约束目标一致。

![[assets/figures/papers/paper_list_l2139_https_arxiv_org_abs_2602_19213/figures/012_Figure_6.jpg]]
*Figure 6: (a) Expert token selection statistics across datasets, the numbers above the bars in the histogram represent the sample size of the current dataset. and (b) (c) experiments with different numbers of experts and activations*

#### 渐进提示令牌化（PPT）

PPT 查询令牌数量的消融（**Table 4**）显示，在无人工交互的自动分割场景下，Q=2 或 Q=8 时 ISLES 数据集的 Dice 从无 PPT 的 **59.00 提升至 65.28（+6.28）**，域内数据亦有 1-3% 的提升。这一结果表明，PPT 通过随机采样掩码和文本提示自动生成的前景/背景令牌，能够有效替代人工点击或边界框提示，显著降低了对用户交互的依赖。但需注意，PPT 当前仅适用于前/背景区分明确的二分类分割任务，尚未扩展至多器官等多类别场景。

![[assets/figures/papers/paper_list_l2139_https_arxiv_org_abs_2602_19213/figures/013_Table_4.jpg]]
*Table 4: Ablation study on query token number. Analysis of different query token sizes (Q size) under various prompt types*

### 路由机制可视化

MoTE 路由热力图（**Figure 7**）为令牌级专家选择提供了直观解释。热力图呈现稀疏、离散的激活模式，不同专家令牌在不同模态下形成明确的“责任区域”——例如，某专家主要关注器官边界区域，另一专家则聚焦于纹理均匀的实质区域。这种稀疏性并非偶然，而是噪声 top-k 门控与负载平衡损失共同作用的结果：噪声注入鼓励探索，防止过早收敛到单一专家；负载平衡损失通过重要性（权重和）与负载（非零计数）的平方变异系数约束，保障各专家获得充分且均衡的训练信号。

![[assets/figures/papers/paper_list_l2139_https_arxiv_org_abs_2602_19213/figures/009_Figure_7.jpg]]
*Figure 7: Visualization of expert token routing across datasets in the MoTE framework. Red boxes highlight the target segmentation areas, and the green checkmark indicates the selected token*

### 失败模式与局限性

尽管 SegMoTE 在二分类分割任务上表现优异，但以下场景仍需警惕：

1. **多类别分割受限**：PPT 机制目前仅针对前/背景二分类设计，无法直接处理多器官同时分割任务。强行扩展可能导致类别间令牌干扰，需重新设计提示生成策略。
2. **3D 数据未验证**：所有实验均基于 2D 医学图像，模型在 3D 体积数据（如 CT/MRI 容积扫描）和医学视频分析中的有效性尚不明确。3D 场景下的令牌路由可能面临计算效率与内存占用的新挑战。
3. **极端罕见模态覆盖不足**：MedSeg-HQ 数据集虽质量高，但规模仅 0.15M 标注，对极端罕见模态（如特定序列的超声或核医学图像）的覆盖可能不充分，模型在这些场景下的泛化能力需进一步验证。

### 开放问题

- SegMoTE 的令牌级路由机制能否有效扩展到 3D 医学体积数据和视频分割任务？若可行，时空维度的专家令牌设计将是一个关键挑战。
- 如何将 PPT 推广到多类别分割场景，同时避免类别间令牌的相互干扰？可能的方向包括引入类别条件编码或层次化令牌结构。
- 在更大规模、更多样化的精选数据集上，模型性能是否还能持续提升？数据质量与数据量的权衡关系值得进一步探索。

### 补充图表

![[assets/figures/papers/paper_list_l2139_https_arxiv_org_abs_2602_19213/figures/011_Table_3.jpg]]
*Table 3: Comparison of SegMoTE with existing interactive segmentation benchmarks in terms of model size*

![[assets/figures/papers/paper_list_l2139_https_arxiv_org_abs_2602_19213/figures/005_Figure_5.jpg]]
*Figure 5: In-domain segmentation results across datasets. (a) and (b) show the Dice coefficient comparisons under single click and bounding box interactions, respectively. (c) illustrates the training dataset sizes used by different methods, where SegMoTE achieves performance improvement by optimizing the annotation quality of the data*



## 定位与知识库关联

### 问题定位：从统一微调到模态自适应

医学图像分割领域长期面临一个核心瓶颈：**异构模态数据缺乏自适应机制**。传统方法——无论是全参数微调（如 **MedSAM**，Ma et al., Nature Communications 2024）还是参数高效微调——通常将所有模态数据无差别地聚合训练，引入监督噪声和负迁移，导致模型在分布外（out-of-domain）场景泛化能力显著下降。SegMoTE 的切入点正是这一模态冲突问题：它不再试图用一个统一的输出令牌适配所有模态，而是通过**令牌级专家路由**为每种模态动态选择最适配的专家路径。

### 与基础模型的继承关系

SegMoTE 直接构建在 **SAM**（Kirillov et al., ICCV 2023）之上，继承了其强大的视觉编码能力和交互式分割范式。但与 MedSAM 的全微调策略或 **SAM-Med2D** 的大规模医学数据微调不同，SegMoTE 采取了更克制的路线：

- **冻结 SAM 编码器**：保留原始零样本能力，避免全微调带来的分布偏移。
- **仅更新轻量插件**：可训练参数仅 17M（MoTE 占 10M，PPT 占 7M），约为原始 SAM 总参数量的 1.4%，远小于 MedSAM（93M）和 **IMIS**（29M）等同类方法。

这种设计哲学与参数高效微调（PEFT）谱系一脉相承，但 SegMoTE 的独特贡献在于将“适配”从参数空间转移到了**路由空间**——不是让模型记住所有模态，而是让模型学会为每个输入令牌选择最合适的专家。

### 与 SAM2 的差异

**SAM2**（Ravi et al., ICLR 2025）作为 SAM 的升级版，主要面向视频分割引入了记忆机制。SegMoTE 与 SAM2 的差异在于：SAM2 关注时序一致性，而 SegMoTE 关注模态多样性。两者在问题维度上互补，SegMoTE 的 MoTE 机制理论上可与 SAM2 的记忆架构结合，但当前工作尚未探索这一方向。

### 核心创新：MoTE 与 PPT 的双轮驱动

SegMoTE 的方法创新体现在两个相互配合的模块：

**1. 令牌级专家混合（MoTE）**

MoTE 引入一组可学习的专家令牌，通过噪声 top-k 门控动态选择最适配当前输入的专家。路由器首先计算令牌在所有专家上的得分：

$$\mathrm { L } = \mathrm { X W } _ { \mathrm { g } } \in \mathbb { R } ^ { B \times T \times E }$$

然后注入高斯噪声以鼓励探索，避免过早收敛到单一专家：

$$\tilde { \mathbf { L } } = \mathbf { L } + ( \mathrm { s o f t p l u s } ( \mathbf { X } \mathbf { W } _ { n } ) + \varepsilon ) \odot \mathbf { Z } , \quad \mathbf { Z } \sim \mathcal { N } ( 0 , 1 )$$

每个令牌的置信度由其最高专家得分决定：

$$c _ { b , t } = \operatorname* { m a x } _ { j = 1 , \ldots , k } \mathbf { s } _ { b , t } [ j ]$$

为确保专家分工均衡，MoTE 采用负载平衡损失，通过重要性（权重和）和负载（非零计数）的平方变异系数约束：

$$\mathcal { L } _ { \mathrm { b a l a n c e } } = \mathrm { C V } ^ { 2 } \left( \{ \operatorname* { i m p } _ { e } \} _ { e = 1 } ^ { E } \right) + \mathrm { C V } ^ { 2 } \left( \{ \log \} _ { e = 1 } ^ { E } \right)$$

消融实验表明，专家数量 N=4、激活数 M=1 时在多模态训练中达到最佳性能，验证了适当的专家组合平衡了表达性和效率。

**2. 渐进提示令牌化（PPT）**

PPT 解决了 SAM 依赖人工交互提示的痛点。通过随机抽样的掩码和文本提示，PPT 自动生成前景/背景令牌，使模型在推理阶段无需任何人工干预即可完成二分类分割。PPT 查询令牌数量 Q=2 或 8 时，在分布外数据集 ISLES 上 Dice 从 59.00 提升至 65.28（+6.28），显著降低了对人工提示的依赖。

### 知识库定位：高质量小数据的范式转变

SegMoTE 的实验设置揭示了一个重要趋势：**数据质量优于数据规模**。模型仅在 MedSeg-HQ（0.15M 高质量掩码）上训练，却在多个分布外数据集上超越使用大规模数据训练的方法，性能提升 1%-6%。这一发现与当前“大数据驱动”的主流范式形成对比，暗示医学图像分割领域可能正在经历从“更多数据”到“更好数据”的范式转变。

MoTE 路由的热力图显示稀疏、离散的“责任区域”，验证了令牌级专家对不同模态的有效选择性——这不仅是性能提升，更是可解释性的突破：模型明确告诉我们它“看到了”什么模态特征。

### 适用边界与局限

**当前适用边界：**
- 主要针对 2D 医学图像的二分类分割任务（器官/病灶 vs 背景）
- 依赖 SAM 编码器的预训练质量，对 SAM 覆盖良好的模态效果更佳
- PPT 机制要求前/背景区分明显，适用于病灶分割、器官提取等场景

**已验证局限：**
1. **多类别分割未覆盖**：PPT 当前仅适用于二分类任务，尚未扩展至多器官等多类别分割场景。
2. **维度局限**：实验验证局限于 2D 医学图像，未探索 3D 体积数据和医学视频分析。
3. **数据规模天花板**：MedSeg-HQ 虽质量高但规模仍小（0.15M 标注），可能限制模型对极端罕见模态的覆盖。

### 开放问题

1. **3D 与视频扩展**：SegMoTE 的令牌级路由机制能否有效扩展到 3D 医学体积数据和视频分割任务？这需要重新设计令牌的时空表示和路由策略。
2. **多类别 PPT**：如何将 PPT 机制推广到多类别分割场景，避免类别间干扰？可能需要引入类别条件化的查询令牌。
3. **数据质量上限**：在更大规模、更多样化的精选数据集上，模型性能是否还能持续提升？还是说 0.15M 高质量数据已接近当前架构的表达上限？
4. **与 SAM2 融合**：MoTE 的模态自适应与 SAM2 的时序记忆是否可互补，构建统一的 3D+时序医学分割框架？



## 原文 PDF

![[paperPDFs/CVPR_2026/SegMoTE_Token_Level_Mixture_of_Experts_for_Medical_Image_Segmentation.pdf]]
