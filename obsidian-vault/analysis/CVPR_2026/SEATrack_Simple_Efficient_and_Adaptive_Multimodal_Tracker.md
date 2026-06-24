---
title: "SEATrack: Simple, Efficient, and Adaptive Multimodal Tracker"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SEATrack_Simple_Efficient_and_Adaptive_Multimodal_Tracker.pdf
project_link: null
code_link: null
aliases:
- SEATrack
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过自适应互引导（AMG）动态对齐跨模态匹配注意力图，并在对齐基础上进行高效全局关系建模（HMoE），可打破性能与效率的折衷。
primary_logic: 在跨模态融合之前进行注意力对齐，以极少的可学习参数显著提升跟踪性能，证明对齐是突破PEFT效率瓶颈的有效途径。
claims:
- 单独使用AMG-LoRA在LasHeR上获得18.3%的PR提升（仅0.14M参数），表明对齐的核心作用。
- "AMG-LoRA将跨模态注意力图的余弦相似度提升至接近1.0（LasHeR: 0.99），对称KL散度极低，定量证实对齐效果。"
- 在LasHeR的19种挑战属性上，AMG-LoRA全面优于LoRA，特别在遮挡(OV)和光照变化(FL)场景增益显著。
- LasHeR 上 PR = 71.6
---

# SEATrack: Simple, Efficient, and Adaptive Multimodal Tracker

> [!tip] 核心洞察
> 在跨模态融合之前进行注意力对齐，以极少的可学习参数显著提升跟踪性能，证明对齐是突破PEFT效率瓶颈的有效途径。

| 字段 | 内容 |
|------|------|
| 中文题名 | SEATrack：简单高效的自适应多模态跟踪器 |
| 英文题名 | SEATrack: Simple, Efficient, and Adaptive Multimodal Tracker |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.12502) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | SEATrack |
| Dataset | LasHeR, DepthTrack, VisEvent |

> [!tip] 效果简介
> - LasHeR 上，PR 71.6 vs ViPT (65.1) (+6.5)；SR 57.3 vs ViPT (52.5) (+4.8)。
> - DepthTrack 上，F-score 63.2 vs ViPT (59.4) (+3.8)。
> - VisEvent 上，PR 77.1 vs ViPT (75.8) (+1.3)。

## 概述

多模态跟踪在现实场景中面临一个核心瓶颈：**跨模态域差异导致双流PEFT跟踪器产生不一致的匹配注意力图**，阻碍有效的联合表示学习，形成性能-效率困境。现有方法或采用单流混合输入（易发生注意力偏移），或采用双流独立自注意力（注意力图不对齐），均难以在有限可训练参数下实现鲁棒的跨模态融合。

**SEATrack** 针对这一瓶颈提出了简洁而高效的解决方案。其核心洞察是：**在跨模态融合之前进行注意力对齐，能以极少的可学习参数显著提升跟踪性能**。方法上，SEATrack 以冻结的 **OSTrack**（Ye et al., ECCV 2022）为基础跟踪器，引入两个轻量级可学习组件：

- **AMG-LoRA**（自适应互引导低秩适配）：对注意力层的 Key 和 Value 投影注入 LoRA 进行域自适应，并通过自适应互引导机制动态对齐 RGB 与 X 模态的匹配注意力图。
- **HMoE**（层级混合专家）：基于层级软路由实现高效的全局跨模态关系建模，以 $O(N e h^2)$ 的复杂度替代传统注意力的 $O(N^2 D)$。

在仅 **0.6M 可训练参数**的条件下，SEATrack 在多个基准上取得领先结果：LasHeR PR 71.6%（较 ViPT 提升 +6.5%），DepthTrack F-score 63.2%（+3.8%），VisEvent PR 77.1%（+1.3%）。消融实验表明，单独使用 AMG-LoRA（仅 0.14M 参数）即可在 LasHeR 上带来 +18.3% 的 PR 提升，跨模态注意力图的余弦相似度提升至接近 1.0，定量证实了注意力对齐的核心作用。

**方法定位**：SEATrack 属于参数高效微调（PEFT）范式下的双流多模态跟踪方法，与 **ViPT**（Zhu et al., CVPR 2023）等视觉提示方法和 **SDSTrack** 等交叉注意力融合方法形成对比。其独特之处在于将跨模态对齐前置到融合之前，以极低参数代价突破 PEFT 的效率瓶颈。当前方法适用于空间对齐的多模态输入（RGB-T、RGB-D、RGB-E），向空间异构模态（如视觉-语言）的扩展仍有待探索。

## 背景与动机

### 多模态跟踪的演进与瓶颈

视觉目标跟踪是计算机视觉的核心任务之一，其目标是在视频序列中持续定位指定目标。近年来，基于Transformer的单流（one-stream）跟踪器（如**OSTrack**，Ye et al., ECCV 2022）在RGB跟踪上取得了显著成功，通过将模板与搜索区域拼接后统一进行自注意力建模，实现了高效的特征交互与目标匹配。

然而，当拓展至多模态跟踪（如RGB-T、RGB-D、RGB-E）时，这一范式面临根本性挑战。多模态输入来自不同传感器，存在显著的**跨模态域差异（domain gap）**，直接拼接会导致注意力偏移（attention shifting）——模型难以区分模态内匹配与模态间匹配，从而损害跟踪鲁棒性。

### 双流PEFT范式的效率-性能困境

为缓解域差异问题，现有工作转向**双流（two-stream）设计**：各模态独立通过共享的ViT编码器进行特征提取与模态内匹配，随后进行跨模态融合。同时，为降低全量微调（FFT，约200M可训练参数）的高昂成本，参数高效微调（PEFT）策略被引入，如**ViPT**（Zhu et al., CVPR 2023）通过视觉提示（visual prompt）适配冻结的基础跟踪器，**SDSTrack**则采用交叉注意力进行融合。

然而，这一双流PEFT范式暴露出一个关键瓶颈：**跨模态域差异导致两条分支产生不一致的匹配注意力图（attention map inconsistency）**。如Figure 1所示，当RGB分支关注目标的纹理区域时，热红外分支可能因光照变化而聚焦于完全不同的空间位置。这种注意力图的不对齐直接阻碍了后续跨模态融合的有效性——融合层面对的是两套“各说各话”的匹配信号，难以形成互补的联合表示。

更严峻的是，这一瓶颈将跟踪器推入了一个**性能-效率困境**：若采用轻量融合策略（如逐元素加法），则无法纠正注意力偏差，性能受限；若引入复杂的交叉注意力融合，虽能部分缓解对齐问题，但计算开销显著增加，违背了PEFT的效率初衷。

### 本文动机与核心思路

针对上述困境，本文提出一个根本性问题：**能否在融合之前，先让两个模态的注意力图“达成共识”？**

直觉上，如果双流分支在每一层产生的匹配注意力图是高度对齐的，那么后续的融合操作——无论简单还是复杂——都能建立在一致的匹配信号之上，从而以极小的参数代价实现高性能。这引出了本文的核心洞察：

> **在跨模态融合之前进行注意力对齐，是打破PEFT效率瓶颈的有效途径。**

基于此，本文提出**SEATrack**（Simple, Efficient, and Adaptive Multimodal Tracker），其核心设计包含两个协同组件：

1. **AMG-LoRA（Adaptive Mutual Guidance Low-Rank Adaptation）**：将低秩适配（LoRA）注入注意力投影矩阵以实现域自适应，并通过自适应互引导机制动态对齐跨模态注意力图——让RGB的匹配信息指导X模态的注意力，反之亦然。

2. **HMoE（Hierarchical Mixture of Experts）**：在对齐后的注意力图上，通过层级软路由实现高效的全局关系建模，从子令牌到令牌逐级混合跨模态信息。

这一设计将“对齐”与“融合”解耦，使得对齐成为融合的预处理步骤，从而以仅0.6M的可训练参数（约为ViPT的1/8）实现显著的性能提升。

## 核心创新

SEATrack 的核心创新围绕一个关键瓶颈展开：**跨模态域差异导致现有双流 PEFT 跟踪器产生不一致的匹配注意力图**，阻碍了有效的联合表示学习，形成了性能-效率困境。为此，SEATrack 引入了两个紧密协同的 changed slots，以极低的参数代价（总计仅 0.6M 可训练参数）打破这一折衷。

### 跨模态注意力对齐：AMG-LoRA

**基线状态**：现有双流 PEFT 方法（如 **ViPT** (Zhu et al., CVPR 2023)）对各模态独立执行自注意力，缺乏跨模态的注意力对齐机制，导致 RGB 与热红外/深度/事件模态的匹配注意力图高度不一致。

**提出方案**：AMG-LoRA（Adaptive Mutual Guidance Low-Rank Adaptation）将低秩适配与自适应互引导相结合，嵌入 ViT 编码器每 2 层，实现跨模态注意力图的动态对齐。其核心机制包含两个层面：

1. **LoRA 域自适应**：对注意力层的 Key 和 Value 投影矩阵注入低秩矩阵 $A, B$，使预训练权重适配目标模态域：
   $$\tilde{K} = \mathbf{H}_{*} W_{k} + \mathbf{H}_{*} A B$$
   其中 $\mathbf{H}_{*}$ 为输入令牌，$W_k$ 为冻结的原始 Key 投影权重。适配后的 Key $\tilde{K}$ 用于计算未归一化匹配注意力图：
   $$\mathbf{a}\tilde{\mathbf{tt}}\mathbf{n}_{*} = \frac{(\mathbf{H}_{*} W_{q}) \tilde{K}}{\sqrt{D}}$$

2. **自适应互引导**：利用可学习的缩放因子 $w_{\mathrm{X}}$ 和 $w_{\mathrm{rgb}}$，使各模态的注意力图通过对方模态的匹配信息进行动态精炼：
   $$\mathbf{attn}_{\mathrm{rgb}} = \mathbf{a}\tilde{\mathbf{tt}}\mathbf{n}_{\mathrm{rgb}} + w_{\mathrm{X}} (\mathbf{a}\tilde{\mathbf{tt}}\mathbf{n}_{\mathrm{X}} - \mathbf{a}\tilde{\mathbf{tt}}\mathbf{n}_{\mathrm{rgb}})$$
   $$\mathbf{attn}_{\mathrm{X}} = \mathbf{a}\tilde{\mathbf{tt}}\mathbf{n}_{\mathrm{X}} + w_{\mathrm{rgb}} (\mathbf{a}\tilde{\mathbf{tt}}\mathbf{n}_{\mathrm{rgb}} - \mathbf{a}\tilde{\mathbf{tt}}\mathbf{n}_{\mathrm{X}})$$
   该设计使注意力对齐强度可自适应学习，而非固定权重。

**证据强度**：消融实验（Table 2）表明，单独使用 AMG-LoRA（仅 0.14M 参数）即可在 LasHeR 上将 PR 从 51.5 提升至 69.8（+18.3%），证实对齐本身是突破 PEFT 效率瓶颈的核心因素。定量统计（Table 9）进一步显示，AMG-LoRA 将跨模态注意力图的余弦相似度提升至接近 1.0（LasHeR 上达 0.99），对称 KL 散度极低，从数值上确证了对齐效果。在 LasHeR 的 19 种挑战属性上（Figure 4），AMG-LoRA 全面优于纯 LoRA，尤其在遮挡（OV）和光照变化（FL）场景增益显著，表明对齐机制对困难场景具有更强的鲁棒性。

### 高效全局关系建模：HMoE

**基线状态**：现有双流跟踪器的跨模态融合多采用逐元素加法或局部交叉注意力，缺乏对全局上下文关系的高效建模能力。

**提出方案**：HMoE（Hierarchical Mixture of Experts）在对齐后的注意力图基础上，通过层级软路由实现从子令牌到令牌的高效全局关系建模。其核心流程为：

1. **子令牌拆分与混合**：将输入令牌沿通道维度拆分为子令牌 $\mathbf{X}_{split} = \mathcal{F}_{s}(\mathbf{X}_{in})$，通过门控矩阵 $\Phi$ 的软分配生成每位专家的头级输入：
   $$\mathbf{X}_{mix} = \mathrm{softmax}(\mathbf{X}_{split} \Phi, \mathrm{dim}=0)^{\mathrm{T}} \mathbf{X}_{split}$$

2. **令牌到专家的层级路由**：通过 patchify 操作重建令牌到专家的亲合性矩阵：
   $$\mathbf{A} = \mathrm{softmax}(\mathcal{F}_{p}(\mathbf{X}_{split} \Phi), \mathrm{dim}=1)$$
   最终基于该亲合性矩阵将专家令牌融合回原始令牌序列：
   $$\mathbf{Y}_{out} = \mathbf{A} \mathbf{Y}_{expert}$$

**证据强度**：消融实验（Table 2）表明，HMoE 单独使用可将 LasHeR PR 提升至 67.4，与 AMG-LoRA 组合后达到最优 71.6。配置消融（Table 4, Table 5）显示，每专家 2 个头、FFN 层专家数高于注意力层的配置实现了最佳性能-效率平衡。相比基于交叉注意力的融合策略，HMoE 速度提升约 35%（Introduction 中报告），在 63.5 FPS 的运行速度下保持了约 1GB 的显存占用。

### 创新协同逻辑

AMG-LoRA 与 HMoE 并非孤立模块，而是形成了“先对齐、后融合”的协同范式。AMG-LoRA 在注意力层解决跨模态匹配图不一致的问题，为 HMoE 提供对齐后的高质量输入；HMoE 在此基础上进行高效的全局关系建模。二者共同嵌入 ViT 编码器每 2 层，以总计 0.6M 的可训练参数，在 LasHeR、DepthTrack、VisEvent 等多个基准上显著超越现有 PEFT 方法（Table 1），证明了“注意力对齐是突破 PEFT 效率瓶颈的有效途径”这一核心洞察。

## 整体框架

SEATrack 的整体设计遵循“冻结基础跟踪器 + 可训练任务特定组件”的范式，旨在以极低的参数开销实现鲁棒的多模态跟踪。如图 Figure 2 所示，其 pipeline 由四个核心模块串联构成：**Frozen Foundation Tracker (OSTrack)**、**AMG-LoRA**、**HMoE** 和 **Prediction Head**。

![[assets/figures/papers/paper_list_l2111_https_arxiv_org_abs_2604_12502/figures/002_Figure_2.jpg]]
*Figure 2: Overall pipeline of SEATrack. Input tokens from each modality are processed by stacked shared ViT encoders for intra-modal target matching and feature extraction. To enable cross-modal interaction, the proposed AMG-LoRA and HMoE are embedded into the ViT encoder every 2 layers to perform attention alignment and information fusion, respectively. AMG-LoRA’s mutual guidance mechanism is exemplified through the “RGB refines X” pathway (Eq. 4), with the reverse direction behaving similarly*

**输入流与特征提取。** 系统接收空间对齐的 RGB 图像与 X 模态（热红外/深度/事件）图像作为输入，分别提取 128×128 的模板区域和 256×256 的搜索区域。两组模态的图像令牌独立进入**共享权重的冻结 ViT 编码器**（基于 OSTrack 的双流变体，Ye et al., ECCV 2022），进行模态内的目标匹配与特征提取。编码器的所有权重在训练和推理期间保持冻结，不参与梯度更新。

**跨模态交互的嵌入策略。** 为实现跨模态信息交互，AMG-LoRA 和 HMoE 被**每 2 层**嵌入到 ViT 编码器中。具体而言，在每一组插入点，AMG-LoRA 首先对 RGB 和 X 模态分支的注意力图进行跨模态对齐，随后 HMoE 在对齐后的特征上执行高效的全局关系建模与融合。这种“先对齐、后融合”的顺序设计是 SEATrack 突破性能-效率瓶颈的关键——对齐后的注意力图具有高度一致性，使得后续融合能够更有效地利用跨模态互补信息。

**AMG-LoRA：跨模态注意力对齐。** 该模块在冻结的注意力投影层上注入低秩适应矩阵（LoRA），对 Key 和 Value 投影进行域自适应，使其适配多模态输入。在此基础上，通过自适应互引导机制（Adaptive Mutual Guidance），利用一个模态的匹配注意力信息动态精炼另一个模态的注意力图，最终生成对齐且精炼的跨模态注意力图（详见 Eq. 3-4）。

**HMoE：层级混合专家融合。** 对齐后的 RGB 和 X 模态特征被拼接送入 HMoE 模块。HMoE 采用层级软路由策略：首先将输入令牌沿通道维度拆分为多个子令牌，通过门控矩阵生成细粒度的子令牌混合表示；随后在专家头内部进行变换，最后通过令牌到专家的亲合性矩阵将专家输出聚合回原始令牌序列（详见 Eq. 5-10）。HMoE 分别插入注意力子层之后和 FFN 子层之后，以捕获不同粒度的跨模态关系。

**预测头与输出。** 经过多层编码器处理后，融合后的搜索区域特征被送入预测头，生成目标中心得分、位置偏移和边界框尺寸。训练采用组合损失函数 $L = L_{focal} + \lambda_{iou} L_{iou} + \lambda_{L1} L_{1}$，其中 $\lambda_{iou}=2$，$\lambda_{L1}=5$（Eq. 11）。

**参数效率。** 整个 SEATrack 仅需训练约 **0.6M** 参数（AMG-LoRA 约 0.14M，HMoE 约 0.46M），相比全量微调（~200M）或其他高参数量 PEFT 方法（>5M）实现了数量级的压缩，同时在 RTX 4090 上保持 63.5 FPS 的推理速度。

## 核心模块与公式推导

SEATrack 的跨模态交互由两个即插即用的轻量模块实现：**AMG‑LoRA**（自适应互引导低秩适配）与 **HMoE**（层级混合专家），二者嵌入冻结的 ViT 编码器每 2 层，共同解决双流 PEFT 跟踪器中跨模态注意力不一致这一核心瓶颈。

### AMG‑LoRA：跨模态注意力对齐

AMG‑LoRA 将 LoRA 的域自适应能力与跨模态互引导机制结合，动态对齐 RGB 与 X 模态（热红外/深度/事件）的匹配注意力图。其操作分三步：

**1. LoRA 增强的 Key 投影（域自适应）**

对注意力 Key 投影矩阵 $W_k$ 注入低秩适配矩阵 $A, B$，使冻结的 ViT 获得模态特定的匹配能力：

$$
\tilde{K} = \mathbf{H}_{*} W_{k} + \mathbf{H}_{*} A B \tag{1}
$$

其中 $\mathbf{H}_{*}$ 为模态 $*$ 的输入令牌，$A \in \mathbb{R}^{D \times r}$、$B \in \mathbb{R}^{r \times D}$ 为可训练的低秩矩阵（秩 $r=8$），仅适配 $W_k$ 和 $W_v$ 时对齐效果最优（Table 8）。

**2. 未归一化注意力图计算**

利用适配后的 Key 与原始 Query 投影计算模板-搜索区域间的匹配得分：

$$
\mathbf{a}\tilde{\mathbf{tt}}\mathbf{n}_{*} = \frac{(\mathbf{H}_{*} W_{q}) \tilde{K}}{\sqrt{D}} \tag{2}
$$

**3. 自适应互引导（核心创新）**

以对方模态的注意力信息为条件，通过可学习的缩放因子动态精炼各模态注意力图：

$$
\mathbf{attn}_{\mathrm{rgb}} = \mathbf{a}\tilde{\mathbf{tt}}\mathbf{n}_{\mathrm{rgb}} + w_{\mathrm{X}} (\mathbf{a}\tilde{\mathbf{tt}}\mathbf{n}_{\mathrm{X}} - \mathbf{a}\tilde{\mathbf{tt}}\mathbf{n}_{\mathrm{rgb}}) \tag{3}
$$

$$
\mathbf{attn}_{\mathrm{X}} = \mathbf{a}\tilde{\mathbf{tt}}\mathbf{n}_{\mathrm{X}} + w_{\mathrm{rgb}} (\mathbf{a}\tilde{\mathbf{tt}}\mathbf{n}_{\mathrm{rgb}} - \mathbf{a}\tilde{\mathbf{tt}}\mathbf{n}_{\mathrm{X}}) \tag{4}
$$

其中 $w_{\mathrm{X}}$、$w_{\mathrm{rgb}}$ 为逐层可学习的标量缩放因子，初始化设为 1（跨引导模式）时性能最优（Table 3）。该机制使跨模态注意力图的余弦相似度提升至接近 1.0（LasHeR 上达 0.99），对称 KL 散度极低（Table 9），定量证实了对齐效果。

![[assets/figures/papers/paper_list_l2111_https_arxiv_org_abs_2604_12502/figures/006_Table_3.jpg]]
*Table 3: Initialization Choices of AMG-LoRA’s Scaling Factor*

### HMoE：层级混合专家融合

HMoE 在注意力对齐后执行高效的全局跨模态关系建模，其层级软路由设计将计算复杂度从令牌数的平方降至线性。给定对齐后的 RGB 与 X 模态令牌拼接输入 $\mathbf{X}_{in}$，HMoE 执行以下流程：

**1. 子令牌拆分**

沿通道维度将输入令牌拆分为 $h \times e$ 个子令牌（$h=2$ 头/专家，$e=4$ 专家）：

$$
\mathbf{X}_{split} = \mathcal{F}_{s}(\mathbf{X}_{in}) \tag{5}
$$

**2. 子令牌混合**

通过门控矩阵 $\Phi$ 的 softmax 软分配，为每位专家头生成细粒度的混合输入：

$$
\mathbf{X}_{mix} = \mathrm{softmax}(\mathbf{X}_{split} \Phi, \mathrm{dim}=0)^{\mathrm{T}} \mathbf{X}_{split} \tag{6}
$$

**3. 专家处理**

各专家头独立处理混合后的子令牌（注意力层或 FFN 层），FFN 层配置更多专家数以平衡性能与效率（Table 5）。

**4. 令牌到专家亲合性重建**

通过 patchify 操作 $\mathcal{F}_{p}$ 重建令牌到专家的权重矩阵：

$$
\mathbf{A} = \mathrm{softmax}(\mathcal{F}_{p}(\mathbf{X}_{split} \Phi), \mathrm{dim}=1) \tag{9}
$$

**5. 最终输出**

基于亲合性矩阵将专家令牌融合回原始令牌序列：

$$
\mathbf{Y}_{out} = \mathbf{A} \mathbf{Y}_{expert} \tag{10}
$$

HMoE 的层级设计在注意力层与 FFN 层后分别插入，秩 $r=4$ 时取得最佳性能-效率平衡（Table 7），相比基于交叉注意力的融合策略速度提升约 35%（Section 1）。

### 训练目标

SEATrack 的总损失函数组合了 focal 分类损失与边界框回归损失：

$$
L = L_{focal} + \lambda_{iou} L_{iou} + \lambda_{L1} L_{1} \tag{11}
$$

其中 $\lambda_{iou}=2$、$\lambda_{L1}=5$，仅 AMG‑LoRA 和 HMoE 的 0.6M 参数参与训练，冻结的 OSTrack 基础跟踪器保持不动。

### 补充图表

![[assets/figures/papers/paper_list_l2111_https_arxiv_org_abs_2604_12502/figures/003_Figure_3.jpg]]
*Figure 3: Architecture details of HMoE configured with*

![[assets/figures/papers/paper_list_l2111_https_arxiv_org_abs_2604_12502/figures/001_Figure_1.jpg]]
*Figure 1: Previous frameworks v.s. SEATrack. (a) The previous one-stream method [55] suffers from attention shifting when performing intra-modal matching on mixed inputs. (b) Similarly, domain gaps cause attention maps’ inconsistency in the two-stream method [11]. (c) Our method is able to produce aligned and refined attention maps, which facilitate cross-modal fusion*

## 实验与分析

### 主实验结果

SEATrack在五个多模态跟踪基准上进行了全面评估，涵盖RGB-T（LasHeR、RGBT234）、RGB-D（DepthTrack、VOT-RGBD2022）和RGB-E（VisEvent）三大类任务。所有对比方法均以**OSTrack**（Ye et al., ECCV 2022）为基础跟踪器，在相同数据集划分上训练和测试，确保了公平性。

**LasHeR基准**上，SEATrack以仅0.6M可训练参数取得PR 71.6%、SR 57.3%，分别超出PEFT基线方法**ViPT**（Zhu et al., CVPR 2023）6.5和4.8个百分点（Table 1）。在RGBT234上，SEATrack的MPR达到87.8%，优于所有PEFT方法。DepthTrack的F-score为63.2%，较ViPT提升3.8%。VisEvent上PR为77.1%，同样保持领先。

参数效率方面，SEATrack的可训练参数（0.6M）仅为全量微调（FFT, ~200M）的约0.3%，也低于SDSTrack等PEFT方法（>5M），同时推理速度达到63.5 FPS（RTX 4090），显存占用约1GB。

### 组件消融实验

Table 2的组件消融揭示了AMG-LoRA与HMoE各自的核心贡献。基础冻结跟踪器在LasHeR上仅取得PR 51.5%。单独加入AMG-LoRA后，PR跃升至69.8%（+18.3%），而AMG-LoRA仅引入0.14M参数，证实了跨模态注意力对齐是突破性能瓶颈的关键。单独加入HMoE将PR提升至67.4%（+15.9%），两者组合达到最优71.6%，表明对齐与融合存在协同效应。

**AMG-LoRA的缩放因子初始化**对性能有显著影响（Table 3）。缩放因子初始化为1（即初始时完全采用跨模态引导）时性能最优，优于0初始化（无引导）和0.5初始化（折中方案），说明从训练初期就建立跨模态注意力对齐有利于模型收敛。

**HMoE的架构配置**方面，每专家2个头在子令牌维度与计算开销之间取得最佳平衡（Table 4）。专家数量上，注意力层和FFN层分别采用不同专家数可获得更好的性能-效率折衷，FFN层专家数高于注意力层时效果更优（Table 5）。

### 秩与适配权重的选择

AMG-LoRA的秩r=8、HMoE的秩r=4分别在对应组件上取得最佳结果（Table 7）。过大的秩不仅增加参数量，还导致性能下降，表明适度的低秩约束对跨模态适配具有正则化效果。

![[assets/figures/papers/paper_list_l2111_https_arxiv_org_abs_2604_12502/figures/016_Table_7.jpg]]
*Table 7: Rank Choices of AMG-LoRA and HMoE*

在注意力层中适配W_k和W_v（而非W_q, W_v）对跨模态对齐最优（Table 8）。这一发现与AMG-LoRA的设计逻辑一致：通过修改Key和Value投影实现域自适应，同时保持Query投影不变以保留基础跟踪器的匹配语义。

![[assets/figures/papers/paper_list_l2111_https_arxiv_org_abs_2604_12502/figures/014_Table_8.jpg]]
*Table 8: Types of Adaptation Weights in AMG-LoRA*

### 融合策略对比

Table 6将HMoE与交叉注意力（Cross-attn）和MCP等融合策略进行了对比。HMoE在性能和效率上均优于这些替代方案，验证了层级软路由混合机制在全局关系建模中的有效性。这得益于HMoE通过子令牌拆分和层级门控实现了细粒度的跨模态信息交换，同时避免了交叉注意力的高计算开销。

### 对齐效果的定量验证

Table 9提供了AMG-LoRA对齐效果的统计证据。在LasHeR上，AMG-LoRA将跨模态注意力图的余弦相似度从LoRA的较低水平提升至0.99（接近完美对齐），对称KL散度也大幅降低。这一定量结果直接证实了AMG-LoRA的互引导机制能够有效消除跨模态域差异导致的不一致匹配注意力图。

### 挑战属性分析

在LasHeR的19种挑战属性上（Figure 4），AMG-LoRA全面优于LoRA，特别在遮挡（OV）和光照变化（FL）场景下增益最为显著。这表明注意力对齐在极端外观变化条件下尤为重要——当单一模态信息不可靠时，对齐后的跨模态注意力能够有效互补。

![[assets/figures/papers/paper_list_l2111_https_arxiv_org_abs_2604_12502/figures/008_Figure_4.jpg]]
*Figure 4: LoRA v.s. AMG-LoRA across 19 challenging attributes on LasHeR [25]*

### 效率分析

Table 10展示了不同HMoE配置下的效率数据。在默认配置（e=4, h=2）下，SEATrack保持63.5 FPS的实时推理速度。增加专家数或头数会线性增加计算开销，但性能提升趋于饱和，验证了默认配置在性能-效率边界上的最优性。

### 失败模式与局限性

尽管SEATrack在空间对齐的多模态输入上表现优异，当前方法仍存在两个主要局限：一是仅适用于RGB-T/RGB-D/RGB-E等空间对齐模态，对于空间异构模态（如视觉与语言）的对齐尚未探索；二是AMG-LoRA的互引导机制依赖简单的缩放因子调制，更复杂的门控机制或序列级自适应可能进一步提升在模态缺失等极端场景下的鲁棒性。Figure 5展示了模态缺失场景下的注意力图对比，AMG-LoRA虽较LoRA有明显改善，但仍有提升空间。

### 补充图表

![[assets/figures/papers/paper_list_l2111_https_arxiv_org_abs_2604_12502/figures/004_Table_1.jpg]]
*Table 1: Main performance comparison across RGB-T, RGB-D, and RGB-E datasets. SEATrack delivers strong overall results on five benchmarks, with outstanding parameter efficiency. L.P. denotes Learnable Parameters. * indicates reproduced results*

![[assets/figures/papers/paper_list_l2111_https_arxiv_org_abs_2604_12502/figures/005_Table_2.jpg]]
*Table 2: Component-wise Ablation Studies*

![[assets/figures/papers/paper_list_l2111_https_arxiv_org_abs_2604_12502/figures/015_Table_9.jpg]]
*Table 9: Statistical results of alignment. Cos denotes cosine similarity, and SKL denotes symmetric KL divergence (scaled by*

![[assets/figures/papers/paper_list_l2111_https_arxiv_org_abs_2604_12502/figures/007_Table_4.jpg]]
*Table 4: Different Numbers of Heads per Expert in HMoE*

![[assets/figures/papers/paper_list_l2111_https_arxiv_org_abs_2604_12502/figures/009_Table_5.jpg]]
*Table 5: Different Numbers of Experts in HMoE*

## 方法谱系与知识库定位

### 1. 在PEFT多模态跟踪谱系中的位置

SEATrack处于参数高效微调（PEFT）多模态跟踪的研究前沿，其直接对标的方法谱系可划分为三类：

**第一类：全量微调（FFT）方法。** 传统多模态跟踪器通常对基础模型进行全参数更新（约200M可训练参数），虽能获得较强性能，但训练和部署成本极高，且容易破坏预训练模型的通用表征能力。

**第二类：PEFT基线方法。** SEATrack主要与以下PEFT跟踪器构成直接竞争关系：
- **ViPT**（Zhu et al., CVPR 2023）：采用视觉提示（visual prompting）策略，在输入端添加少量可学习令牌实现模态适配，是该方向的代表性工作。
- **SDSTrack**：采用交叉注意力融合机制，在双流架构中进行跨模态信息交互。
- 上述方法均以**OSTrack**（Ye et al., ECCV 2022）作为冻结的基础跟踪器，采用ViT-Base作为骨干网络，构成公平对比的基础。

**第三类：SEATrack的差异化定位。** 与现有PEFT方法不同，SEATrack的核心创新在于**在跨模态融合之前显式进行注意力对齐**。此前的方法（无论单流还是双流）均未解决跨模态域差异导致的注意力图不一致问题——单流方法面临混合输入时的注意力偏移，双流方法则因域间隙产生不匹配的匹配注意力图（见Figure 1）。SEATrack通过AMG-LoRA在极低参数代价下（0.14M）实现了跨模态注意力的动态对齐，将这一隐性瓶颈显式建模为可优化的目标。

### 2. 核心组件的方法学定位

**AMG-LoRA：LoRA适配 + 互引导对齐。** AMG-LoRA并非简单的LoRA应用，而是将低秩适配与自适应互引导机制深度融合。其设计逻辑是：首先通过LoRA对注意力投影矩阵（$W_k$, $W_v$）进行域自适应，使得双流编码器能够生成更具模态区分度的中间表征；随后通过互引导机制（Eq. 3-4），利用一个模态的匹配信息动态精炼另一模态的注意力图。这种“先适配、后对齐”的两阶段设计，使得对齐过程能够充分利用LoRA提供的域自适应表征能力。消融实验证实，单独使用AMG-LoRA即可在LasHeR上获得18.3%的PR提升（Table 2），且将跨模态注意力图的余弦相似度提升至接近1.0（Table 9），定量验证了对齐的有效性。

**HMoE：层级混合专家融合。** HMoE的设计区别于传统的交叉注意力或逐元素融合策略。其核心机制是层级软路由：首先将输入令牌沿通道维度拆分为子令牌（Eq. 5），通过门控矩阵生成每位专家的头级输入（Eq. 6），再基于令牌到专家的亲合性矩阵（Eq. 9）将专家输出聚合回令牌序列（Eq. 10）。这种设计在保持全局关系建模能力的同时，通过子令牌粒度的混合实现了显著的效率优势——相比基于注意力的融合方法，HMoE在速度上提升约35%（见Introduction部分）。消融实验表明，每专家2个头、FFN层专家数高于注意力层的配置（Table 4-5）实现了最佳的性能-效率平衡。

### 3. 适用边界与约束条件

**模态空间对齐假设。** SEATrack的当前设计隐含假设输入模态在空间上是对齐的（如RGB-T、RGB-D、RGB-E），即不同模态的像素/令牌在空间位置上存在对应关系。这一假设使得AMG-LoRA的互引导机制能够直接操作匹配注意力图。对于空间异构模态（如视觉与语言），该对齐机制的直接迁移仍有待探索。

**PEFT范式的基础模型依赖。** SEATrack的性能高度依赖冻结基础跟踪器的质量。当前实验均基于OSTrack（ViT-Base）进行，作者明确指出了这一局限性：在更大规模基础模型（如ViT-L/H）上，SEATrack的参数效率优势能否保持仍是开放问题。

**输入依赖的对齐机制。** 当前AMG-LoRA的互引导强度由可学习的缩放因子控制，这些因子在训练后固定。作者承认，更强的门控机制或序列级自适应可能进一步提升鲁棒性，特别是在模态缺失或严重退化的场景下。Figure 5展示了AMG-LoRA在模态缺失场景下的注意力图表现，虽优于LoRA基线，但仍存在改进空间。

### 4. 局限性与开放问题

**已识别的局限性：**
1. **模态空间对齐假设**：当前方法仅适用于空间对齐的多模态输入，无法直接处理视觉-语言等异构模态的跟踪任务。
2. **自适应机制的可扩展性**：当前互引导依赖固定的可学习缩放因子，缺乏对序列级或实例级动态变化的细粒度适应能力。

**开放问题：**
1. **跨异构模态的对齐泛化**：如何将AMG的互引导机制扩展到空间异构模态（如视频-语言）的对齐与跟踪？这可能需要重新设计注意力图的结构化表示或引入跨模态映射模块。
2. **更大规模基础模型的效率保持**：在ViT-L/H等更大规模骨干网络上，SEATrack的0.6M参数量优势能否保持？LoRA的秩选择、HMoE的专家配置是否需要相应调整？
3. **实时部署的进一步优化**：虽然SEATrack已达到63.5 FPS（RTX 4090），但在边缘设备上的部署效率仍有待验证。HMoE的层级路由机制在资源受限环境下的计算图优化是潜在的工程挑战。

### 5. 知识库定位总结

SEATrack在多模态跟踪领域的方法学贡献可归纳为：**首次将跨模态注意力对齐显式建模为PEFT框架中的可优化目标，并以极低参数代价（0.6M）实现了性能的显著突破**。其在LasHeR上71.6%的PR、DepthTrack上63.2%的F-score，以及VisEvent上77.1%的PR（Table 1），均超越了同期PEFT方法，证明了“先对齐、后融合”这一设计哲学的有效性。该方法为PEFT多模态跟踪提供了一个新的基线范式，其核心组件（AMG-LoRA和HMoE）的模块化设计也为后续研究提供了可复用的构建块。

## 原文 PDF

![[paperPDFs/CVPR_2026/SEATrack_Simple_Efficient_and_Adaptive_Multimodal_Tracker.pdf]]
