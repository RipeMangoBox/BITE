---
title: "VidEoMT: Your ViT is Secretly Also a Video Segmentation Model"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VidEoMT_Your_ViT_is_Secretly_Also_a_Video_Segmentation_Model.pdf
project_link: null
code_link: https://www.tue-mps.org/videomt/
aliases:
- VVEOMT
- VidEoMT
tags:
  - CVPR_2026
  - topic/vision_multimodal_applications/segmentation
  - topic/vision_multimodal_applications
core_operator: 大规模预训练的ViT编码器（如DINOv2）内部特征已具有强大的实例判别和跨视图一致性，仅需添加轻量级的查询传播与融合机制即可在编码器内部同时完成分割与时序关联。
primary_logic: 通过将时序建模的查询直接注入ViT编码器，并利用查询融合平衡时序连续性和对新目标的适应性，可以用极简的编码器-仅架构取代庞大的解耦式分割与追踪流水线，在保持准确率的同时实现数量级的加速。
claims:
- 从CAVIS逐步移除专门组件（context-aware features、re-id layers、tracker）仅导致AP从68.9降至61.3，而推理速度从15 FPS提升至162 FPS，表明预训练ViT可以接管大部分功能。
- 在EoMT基础上添加查询传播使AP从61.3提升至63.9，且不增加计算量；进一步添加查询融合使AP恢复至68.6，速度保持在160 FPS，较CAVIS加速超过10倍。
- VidEoMT在YouTube-VIS 2019/2021/2022、OVIS、VIPSeg、VSPW共六个基准上均实现与最先进方法可比或更优的精度，同时速度提升5-10倍。
- 在编码器-解码器替代方案中，将查询融合应用于解码器得到的AP为68.0，而VidEoMT编码器-仅架构达到68.6且速度更快（160 FPS vs 34 FPS），证明编码器内部的查询融合更高效。
---

# VidEoMT: Your ViT is Secretly Also a Video Segmentation Model

> [!tip] 核心洞察
> 通过将时序建模的查询直接注入ViT编码器，并利用查询融合平衡时序连续性和对新目标的适应性，可以用极简的编码器-仅架构取代庞大的解耦式分割与追踪流水线，在保持准确率的同时实现数量级的加速。

| 字段 | 内容 |
|------|------|
| 中文题名 | VidEoMT：你的ViT其实也是一个视频分割模型 |
| 英文题名 | VidEoMT: Your ViT is Secretly Also a Video Segmentation Model |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.17807) · [Code](https://www.tue-mps.org/videomt/) |
| Topic | #topic/vision_multimodal_applications/segmentation #topic/vision_multimodal_applications |
| Method | VidEoMT (Video Encoder-only Mask Transformer) |
| Dataset | YouTube-VIS 2019 val, YouTube-VIS 2021 val, YouTube-VIS 2022 val, OVIS val |

> [!tip] 效果简介
> - YouTube-VIS 2019 val 上，AP 68.6 vs 68.9 (CAVIS) (-0.3)；FPS 160 vs 15 (CAVIS) (+145)。
> - YouTube-VIS 2021 val 上，AP 63.1 vs 64.6 (CAVIS) (-1.5)。
> - YouTube-VIS 2022 val 上，AP 42.6 vs 40.0 (CAVIS) (+2.6)。

## 概要

在线视频分割（涵盖视频实例分割VIS、视频全景分割VPS和视频语义分割VSS）的现有最先进方法，如 **CAVIS**（Lee et al., ICCV 2025）和 **DVIS++**（Zhang et al., PAMI 2025），普遍采用解耦式架构：一个负责逐帧分割的segmenter与一个专用于时序关联的tracker。这种设计依赖大量手工定制的专用组件——包括上下文感知特征（context-aware features）、重识别MLP层（re-identification layers）和独立的Transformer追踪模块——导致模型臃肿、推理效率低下，通常仅能达到约15 FPS。

本文的核心发现是：**大规模预训练的ViT编码器（如DINOv2）内部特征已天然具备强大的实例判别和跨视图一致性，仅需极轻量的时序查询机制即可在编码器内部同时完成分割与追踪。** 基于此，作者提出 **VidEoMT**（Video Encoder-only Mask Transformer），一种极简的编码器-仅架构。VidEoMT将可学习的对象查询直接注入ViT编码器的后若干层，并通过**查询传播**（将前一帧的追踪查询传递至当前帧）和**查询融合**（将传播查询与可学习查询逐元素相加，见公式 $\mathbf{Q}_{t}^{\mathcal{F}} = \mathtt{Linear} \big( \mathbf{Q}_{t-1}^{\mathcal{S}} \big) + \mathbf{Q}^{\mathrm{lrn}}$）来统一处理分割与时序关联，彻底摒弃了独立的追踪模块。

逐步消融实验（Table 1）清晰地揭示了因果链条：从CAVIS中移除segmenter替换为EoMT仅导致AP从68.9微降至68.1，而FPS从15跃升至42；进一步移除context-aware features和re-id layers后AP几乎不变（68.0），FPS升至74；即便完全移除tracker退化为逐帧分割，AP仍保持在61.3，速度飙升至162 FPS。在此基础上，添加查询传播使AP恢复至63.9且不增加任何计算开销；最终引入查询融合后，AP达到68.6，与CAVIS的68.9几乎持平，而推理速度达到160 FPS——**加速超过10倍**。

在六个主流基准上的全面验证（Tables 2–5）表明，VidEoMT在YouTube-VIS 2019/2021/2022、OVIS、VIPSeg和VSPW上均取得与最先进方法可比或更优的精度，同时速度提升5–10倍。该方法对大规模预训练具有较强依赖（使用DeiT-III等较小规模预训练时AP降至58.3），且在严重遮挡场景（如OVIS上AP为55.2 vs. CAVIS的57.3）仍存在改进空间。但其简洁的编码器-仅设计为视频分割领域提供了一条“少即是多”的新范式：预训练基础模型本身可以接管大部分曾被赋予专用模块的功能。

视频分割（video segmentation）旨在为视频的每一帧同时完成像素级目标分割与跨帧实例关联，是视频理解的核心任务之一。根据输出粒度的不同，该任务可细分为视频实例分割（VIS）、视频全景分割（VPS）和视频语义分割（VSS）。近年来，随着大规模视觉基础模型的兴起，视频分割方法在精度上取得了显著进展，但其架构设计仍面临一个根本性矛盾：**精度与效率的严重失衡**。

### 现有方法的架构瓶颈

当前最先进的在线视频分割模型普遍采用**解耦式架构**：将任务拆分为“逐帧分割”和“跨帧追踪”两个独立阶段，并分别设计专用模块。以代表性方法 **CAVIS**（Lee et al., ICCV 2025）为例，其架构包含以下核心组件：

1. **复杂的分割器（Segmenter）**：由 ViT-Adapter + Mask2Former 像素解码器 + Transformer 解码器组成，负责每帧的实例分割。
2. **专用的追踪器（Tracker）**：独立的 Transformer 模块，通过交叉注意力进行时序建模。
3. **上下文感知特征（Context-aware features）**：从分割器输出中提取的专门特征表示，用于增强时序关联。
4. **重识别层（Re-identification MLP）**：对上下文感知查询施加多层感知机以增强实例判别能力，用于对比学习。

这种“分割器 + 追踪器”的解耦范式虽然在精度上表现优异，但引入了大量任务特定的手工设计组件，导致模型架构臃肿、推理效率低下。例如，CAVIS 在 YouTube-VIS 2019 上仅能达到约 15 FPS（NVIDIA H100 GPU），远不能满足实时应用需求。类似地，**DVIS**（Zhang et al., CVPR 2023）及其后续改进 **DVIS++**（Zhang et al., PAMI 2025）、**DVIS-DAQ**（Zhou et al., ECCV 2024）均沿用了这一解耦思路，面临同样的效率瓶颈。

### 核心洞察：预训练 ViT 的未充分利用

上述方法的一个共同点是**冻结** DINOv2 等大规模预训练的 ViT 编码器，仅将其视为固定的特征提取器。然而，大规模预训练的 ViT 编码器（如 DINOv2）在自监督训练过程中已习得强大的实例判别能力和跨视图一致性——这些能力恰恰是视频分割中时序关联所需的核心要素。这意味着，预训练 ViT 内部已经潜在地具备了同时完成分割与时序关联的能力，而现有方法却忽视了这一潜力，转而依赖繁重的外部追踪模块。

### 本文动机

基于上述观察，本文提出一个根本性问题：**是否可以用极简的编码器-仅架构取代庞大的解耦式分割与追踪流水线，在保持准确率的同时实现数量级的加速？** 

为此，我们提出 **VidEoMT（Video Encoder-only Mask Transformer）**，其核心思想是：将时序建模的查询直接注入 ViT 编码器内部，通过轻量级的查询传播（Query Propagation）与查询融合（Query Fusion）机制，在编码器内部同时完成分割与时序关联，从而彻底消除对专用追踪模块的依赖。这一设计不仅大幅简化了架构，更使得推理速度提升 5–10 倍，同时保持了与最先进方法可比甚至更优的精度。

## 核心方法与创新机理

VidEoMT 的核心创新在于用一个极简的“编码器-仅”架构统一了视频分割中原本解耦的分割与时序关联，从而消除了现有方法中臃肿的专用追踪模块。其关键设计变更可归纳为以下四个 **changed slots**。

### 1. 分割器：从复杂解码器到编码器内部查询

现有最先进方法（如 **CAVIS**，Lee et al., ICCV 2025；**DVIS++**，Zhang et al., PAMI 2025）普遍采用“ViT-Adapter + Mask2Former 像素解码器 + Transformer 解码器”的复杂分割器。VidEoMT 将其替换为 **EoMT**（encoder-only mask transformer）：将可学习查询直接注入 ViT 编码器的最后 $L_2$ 层，与图像块 token 联合处理，无需任何专门的像素解码器或 Transformer 解码器即可完成分割预测（Table 1 step (1); Sec. 3.3）。

这一替换的因果效应非常显著：在 YouTube-VIS 2019 val 上，AP 仅从 68.9 微降至 68.1（−0.8），而推理速度从 15 FPS 飙升至 42 FPS，提升近 3 倍（Table 1 step (1)）。这表明大规模预训练 ViT 的内部特征已经具备了足够的实例判别能力，可以接管原本由专门分割解码器承担的功能。

### 2. 追踪器：从专用模块到编码器内部查询传播与融合

现有方法的追踪器通常由独立的 Transformer 块、上下文感知特征（context-aware features）和重识别 MLP 组成。VidEoMT 完全移除了这些专用组件，代之以在 ViT 编码器内部完成的**查询传播**与**查询融合**（Table 1 steps (2)–(6); Sec. 3.4）。

- **查询传播**：对于 $t > 0$ 的帧，不再使用可学习查询，而是将前一帧的追踪查询 $\mathbf{Q}_{t-1}^{\mathcal{S}}$ 直接作为当前帧的输入，注入 ViT 的最后 $L_2$ 层。这以零额外计算量实现了时序信息的跨帧传递。
- **查询融合**：为解决仅依赖传播查询无法检测新出现目标的问题，VidEoMT 将传播查询经线性变换后与可学习查询 $\mathbf{Q}^{\mathrm{lrn}}$ 逐元素相加，得到融合查询：

$$\mathbf{Q}_{t}^{\mathcal{F}} = \mathtt{Linear}\big(\mathbf{Q}_{t-1}^{\mathcal{S}}\big) + \mathbf{Q}^{\mathrm{lrn}}$$

该融合机制在保持时序连续性的同时，保留了对新目标的适应性。

消融实验揭示了每一步的因果贡献：移除上下文感知特征和重识别 MLP 后，AP 保持在 68.0，FPS 进一步提升至 74（Table 1 steps (2)–(3)）；进一步移除整个专用追踪器使 AP 降至 61.3，但 FPS 跃升至 162（Table 1 step (4)）；添加查询传播使 AP 恢复至 63.9（Table 1 step (5)）；最终添加查询融合使 AP 恢复至 68.6，几乎完全追平 CAVIS 的 68.9，而 FPS 保持在 160，加速超过 10 倍（Table 1 step (6)）。

### 3. 时序建模方式：从解耦到统一

现有方法采用“分割器 → 追踪器”的解耦流水线，分割和时序关联在两个独立模块中串行完成。VidEoMT 将这两者统一在 ViT 编码器内部：分割查询同时承担目标检测与时序关联的双重角色，通过查询融合在一次前向传播中完成（Fig. 2; Sec. 3.4）。

编码器-解码器替代方案的对比实验进一步验证了这一设计的关键性：将查询融合应用于 Mask2Former 解码器（而非 ViT 编码器内部）仅达到 68.0 AP，且 FPS 仅为 34；而 VidEoMT 的编码器-仅架构达到 68.6 AP 且 FPS 高达 160（Table 7）。这证明在编码器内部进行查询融合比在解码器中更高效，因为编码器中的查询可以直接利用 ViT 的全局自注意力进行深度特征交互。

### 4. 预训练微调策略：从冻结到全量微调

CAVIS 和 DVIS++ 等方法在第一阶段后冻结 DINOv2 ViT 编码器，仅训练新增的适配器和解码器。VidEoMT 则在整个训练过程中微调全部 ViT 参数（Appendix A.1）。这一策略使 ViT 能够将大规模预训练中习得的实例判别和跨视图一致性能力充分适配到视频分割任务上，是实现编码器-仅架构高性能的关键使能因素。但这也意味着 VidEoMT 对预训练规模高度依赖——当使用较小规模的预训练（如 DeiT-III）时，AP 大幅下降至 58.3（Table 8），表明该方法的能力边界受限于基础模型的预训练质量。

VidEoMT 的整体设计遵循一个核心原则：**将分割与时序关联统一在单个 ViT 编码器内部完成**，从而彻底消除现有方法中解耦的 segmenter–tracker 架构。其 pipeline 可以概括为以下流程：

1. **输入**：视频帧序列 $\nu = \{ \mathbf{I}_1, \mathbf{I}_2, \ldots, \mathbf{I}_T \}$，逐帧在线处理。
2. **特征提取与查询注入**：每帧图像被切分为 patch token，送入 DINOv2 ViT 编码器。在编码器的最后 $L_2$ 层之前，将一组对象查询（object queries）与 patch token 拼接，使查询能够直接参与 ViT 内部的交叉注意力计算，同时完成空间特征提取和实例级表示学习。
3. **时序传播**：对于 $t > 0$ 的后继帧，不再使用可学习查询，而是将前一帧输出的 track query $\mathbf{Q}_{t-1}^{\mathcal{S}}$ 作为当前帧的输入查询——这称为**查询传播（Query Propagation）**，以极低成本维持跨帧的目标身份连续性。
4. **查询融合（Query Fusion）**：为平衡时序连续性与对新出现目标的检测能力，VidEoMT 将传播查询与一组时不变的可学习查询 $\mathbf{Q}^{\mathrm{lrn}}$ 通过逐元素相加进行融合：
   $$\mathbf{Q}_{t}^{\mathcal{F}} = \mathtt{Linear}\big( \mathbf{Q}_{t-1}^{\mathcal{S}} \big) + \mathbf{Q}^{\mathrm{lrn}}$$
   融合后的查询 $\mathbf{Q}_{t}^{\mathcal{F}}$ 被送入 ViT 的最后 $L_2$ 层进行联合处理。
5. **预测头**：ViT 输出的查询表示直接送入轻量级预测头——一个线性层用于类别分类，一个三层 MLP 加点积操作用于掩码预测——生成每帧的预测集 $\mathcal{V}_t = \{ ( \mathbf{m}_{t,i}, c_{t,i} ) \}_{i=1}^{K_t}$。

**架构对比**：Figure 2 清晰展示了 VidEoMT 与以 CAVIS 为代表的现有方法的本质差异。现有方法（Figure 2 左）将 pipeline 拆分为三个独立阶段：ViT-Adapter 增强的 ViT 编码器 → Mask2Former 式分割解码器 → 专用跟踪 Transformer（含 context-aware features 和 re-identification MLP）。而 VidEoMT（Figure 2 右）将这一切压缩为单一的 ViT 编码器，仅在其中嵌入查询传播与融合机制，完全摒弃了 ViT-Adapter、像素解码器和专用跟踪模块。

**初始帧处理**：对于视频的第一帧（$t = 0$），由于没有前一帧的 track query 可供传播，VidEoMT 直接使用可学习查询 $\mathbf{Q}^{\mathrm{lrn}}$ 作为输入。这些查询在编码器内部与 patch token 交互后，输出的 track query $\mathbf{Q}_{0}^{\mathcal{S}}$ 被保存下来，用于下一帧的传播。Figure 3 详细描绘了这一机制在初始帧和后继帧中的不同数据流。

**训练目标**：整个模型端到端训练，总损失为掩码损失与分类损失的加权组合：
$$\mathcal{L}_{\mathrm{tot}} = \lambda_{\mathrm{bce}} \mathcal{L}_{\mathrm{bce}} + \lambda_{\mathrm{dice}} \mathcal{L}_{\mathrm{dice}} + \lambda_{\mathrm{ce}} \mathcal{L}_{\mathrm{ce}}$$
其中 $\lambda_{\mathrm{bce}} = 5.0$、$\lambda_{\mathrm{dice}} = 5.0$、$\lambda_{\mathrm{ce}} = 2.0$。与 CAVIS 等方法冻结 ViT 编码器的做法不同，VidEoMT 在整个训练过程中对 ViT 进行全量微调，并采用层级学习率衰减（LLRD factor = 0.6）和多项式学习率衰减（power = 0.9）。

**效率特性**：由于整个 pipeline 仅包含 ViT 编码器的前向传播和极轻量的预测头，VidEoMT 在推理时达到了极高的吞吐量。所有 FPS 测量均在相同的 NVIDIA H100 GPU 上，使用 FlashAttention v2 和 torch.compile，batch size 为 1 帧，并启用自动混合精度，确保了与基线方法的公平对比。

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2602_17807/figures/002_Figure_2.jpg]]
*Figure 2: Current State-of-the-Art Video Segmentation Methods vs. VidEoMT (Ours). We compare the architectures of current state-of-the-art video segmentation methods – using CAVIS [21] as a representative example – and our encoder-only VidEoMT method. VidEoMT streamlines the video segmentation framework, relying on the power of large-scale pre-training with vision foundation models rather than handcrafted task-specific components. TF means Transformer and CA means context-aware*

VidEoMT（Video Encoder-only Mask Transformer）将视频分割的时序建模与空间分割统一到一个ViT编码器中，其核心由四个模块构成：

### 1. ViT编码器（DINOv2骨干）

VidEoMT将DINOv2预训练的ViT编码器分为两个阶段：前$L_1$层仅处理图像patch tokens，后$L_2$层同时处理patch tokens和查询tokens。这种设计使编码器在提取空间特征的同时完成实例分割和时序关联，彻底消除了对专用解码器和跟踪器的依赖。在整个训练过程中，ViT编码器保持可微调状态，而非如CAVIS等方法冻结编码器。

### 2. 可学习查询（Learnable Queries）

设$\mathbf{Q}^{\mathrm{lrn}} \in \mathbb{R}^{N \times d}$为$N$个$d$维可学习查询向量，它们是时序无关的（temporally-agnostic），负责检测每帧中出现的新目标。在初始帧（$t=0$），这些查询直接与patch tokens拼接后送入后$L_2$层ViT块。

### 3. 查询传播（Query Propagation）

对于后续帧$t>0$，VidEoMT将前一帧的跟踪查询$\mathbf{Q}_{t-1}^{\mathcal{S}}$作为当前帧的输入查询，而非重新使用可学习查询。这一机制以零额外计算成本实现了跨帧的目标身份传递，使模型能够维持时序连续性。传播过程在编码器内部完成，无需独立的跟踪器模块。

### 4. 查询融合（Query Fusion）

为平衡时序连续性与新目标检测能力，VidEoMT提出查询融合策略：

$$\mathbf{Q}_{t}^{\mathcal{F}} = \mathrm{Linear}\left(\mathbf{Q}_{t-1}^{\mathcal{S}}\right) + \mathbf{Q}^{\mathrm{lrn}}$$

其中$\mathrm{Linear}(\cdot)$是一个线性投影层，将前一帧的跟踪查询映射到与可学习查询相同的语义空间。两者通过逐元素相加完成融合，使当前帧的输入查询同时携带历史目标信息（来自$\mathbf{Q}_{t-1}^{\mathcal{S}}$）和新目标检测能力（来自$\mathbf{Q}^{\mathrm{lrn}}$）。融合后的查询$\mathbf{Q}_{t}^{\mathcal{F}}$与patch tokens拼接后送入后$L_2$层ViT块，输出当前帧的分割预测和跟踪查询$\mathbf{Q}_{t}^{\mathcal{S}}$。

### 5. 预测头

编码器输出的查询表示通过两个轻量级预测头生成最终结果：分类头为单层线性层，掩码头由三层MLP与编码器输出的patch特征做点积得到二值掩码。总损失函数为：

$$\mathcal{L}_{\mathrm{tot}} = \lambda_{\mathrm{bce}}\mathcal{L}_{\mathrm{bce}} + \lambda_{\mathrm{dice}}\mathcal{L}_{\mathrm{dice}} + \lambda_{\mathrm{ce}}\mathcal{L}_{\mathrm{ce}}$$

其中$\lambda_{\mathrm{bce}}=5.0$，$\lambda_{\mathrm{dice}}=5.0$，$\lambda_{\mathrm{ce}}=2.0$，分别对应二元交叉熵损失、Dice损失和交叉熵损失。

### 关键公式汇总

| 公式 | 含义 | 来源 |
|------|------|------|
| $\nu = \{\mathbf{I}_1, \mathbf{I}_2, \ldots, \mathbf{I}_T\}$ | 视频定义为$T$帧序列 | Sec. 3.1 |
| $\mathcal{V}_t = \{(\mathbf{m}_{t,i}, c_{t,i})\}_{i=1}^{K_t}$ | 第$t$帧中$K_t$个目标的二值掩码和类别标签集合 | Sec. 3.1 |
| $\mathbf{Q}_{t}^{\mathcal{T}} = \mathcal{T}(\mathbf{Q}_{t}^{\mathcal{S}}, \mathbf{Q}_{t-1}^{\mathcal{T}})$ | CAVIS中跟踪器根据当前分割查询和上一帧时序查询输出当前帧时序查询 | Eq. (1) |
| $\mathbf{Q}_{t}^{\mathcal{R}} = \mathrm{MLP}(\mathbf{Q}_{t}^{\mathcal{C}})$ | CAVIS中对上下文感知查询应用3层MLP以增强特征用于对比学习 | Eq. (2) |
| $\mathbf{Q}_{t}^{\mathcal{F}} = \mathrm{Linear}(\mathbf{Q}_{t-1}^{\mathcal{S}}) + \mathbf{Q}^{\mathrm{lrn}}$ | VidEoMT查询融合：前帧跟踪查询经线性变换后与可学习查询逐元素相加 | Eq. (3) |
| $\mathcal{L}_{\mathrm{tot}} = \lambda_{\mathrm{bce}}\mathcal{L}_{\mathrm{bce}} + \lambda_{\mathrm{dice}}\mathcal{L}_{\mathrm{dice}} + \lambda_{\mathrm{ce}}\mathcal{L}_{\mathrm{ce}}$ | 总损失为BCE、Dice和CE损失的加权和 | Eq. (4) |

### 架构对比

现有最先进在线视频分割方法（以**CAVIS**（Lee et al., ICCV 2025）为代表）采用解耦架构：segmenter（ViT-Adapter + Mask2Former像素解码器 + Transformer解码器）负责逐帧分割，tracker（包含交叉注意力、context-aware features、re-identification MLP的独立Transformer块）负责时序关联。VidEoMT将两者统一到单个ViT编码器中，仅通过查询传播和查询融合完成时序建模，架构极简（见Figure 2和Figure 3）。

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2602_17807/figures/003_Figure_3.jpg]]
*Figure 3: VidEoMT architecture. For the initial video frame at*

## 实验与关键发现

### 从CAVIS到VidEoMT的逐步解构

VidEoMT的核心主张是：大规模预训练的ViT编码器内部已经蕴含了强大的实例判别和跨视图一致性，仅需轻量级的查询传播与融合即可在编码器内部同时完成分割与时序关联，从而取代臃肿的解耦式分割-追踪流水线。这一主张最直接的证据来自Table 1中从**CAVIS**（Lee et al., ICCV 2025）到VidEoMT的逐步消融实验。

**Table 1**展示了在YouTube-VIS 2019验证集上，从CAVIS逐步移除专用模块、再扩展至VidEoMT的完整过程，每一步都记录了AP、参数量、GFLOPs和FPS的变化：

- **Step (0)：CAVIS基线**。AP为68.9，FPS仅为15。这是当前最先进的在线视频分割模型，包含完整的segmenter（ViT-Adapter + Mask2Former解码器）和tracker（包含context-aware features、re-identification MLP和专门的跟踪Transformer）。

- **Step (1)：替换segmenter为EoMT**。将复杂的segmenter替换为仅将可学习查询注入ViT最后几层的EoMT后，AP仅下降0.8（68.1 vs 68.9），而FPS从15跃升至42，提升近3倍。这表明预训练ViT本身已经能够胜任大部分分割功能，无需额外的像素解码器和Transformer解码器。

- **Steps (2)-(3)：移除context-aware features和re-identification layers**。在EoMT基础上进一步移除CAVIS追踪器中的context-aware features和re-identification MLP，AP几乎无变化（68.0），FPS进一步提升至74。这说明这些专门为追踪设计的特征增强模块对精度贡献甚微，反而显著拖慢了推理速度。

- **Step (4)：移除整个tracker**。当完全移除独立的跟踪Transformer模块后，AP骤降至61.3，但FPS飙升至162。这一结果揭示了两个关键信息：其一，独立的tracker模块确实提供了约6.7 AP的时序关联能力；其二，即便没有tracker，纯粹的EoMT分割器仍能保留大部分精度（61.3 AP），且速度达到162 FPS，远超任何现有方法。

- **Step (5)：添加查询传播**。在EoMT基础上引入查询传播机制——即将前一帧的track queries直接作为当前帧ViT的输入——使AP从61.3恢复至63.9，且不增加任何计算量。这表明简单的查询复用即可实现有效的时序信息传递。

- **Step (6)：添加查询融合（VidEoMT）**。通过将传播查询与可学习查询进行逐元素相加（即查询融合，见公式 $\mathbf{Q}_{t}^{\mathcal{F}} = \mathtt{Linear}(\mathbf{Q}_{t-1}^{\mathcal{S}}) + \mathbf{Q}^{\mathrm{lrn}}$），AP最终恢复至68.6，几乎追平CAVIS的68.9，而FPS保持在160，较CAVIS加速超过10倍。

这一消融链条清晰地揭示了瓶颈与因果机制：**现有方法的性能瓶颈不在于精度不足，而在于过度工程化的专用模块导致的效率低下**。预训练ViT已经隐式地学会了实例判别和跨帧匹配能力，只需通过查询传播与融合将这些能力显式化，即可在编码器内部完成分割与追踪的统一建模。

### 多基准主结果：精度保持下的数量级加速

VidEoMT在六个主流视频分割基准上进行了全面评估，涵盖视频实例分割（VIS）、视频全景分割（VPS）和视频语义分割（VSS）三个子任务。

**视频实例分割（VIS）结果**（Table 2, Table 3）：

- **YouTube-VIS 2019**：VidEoMT达到68.6 AP，与CAVIS的68.9几乎持平（−0.3），但FPS为160 vs 15，加速超过10倍。与**DVIS++**（Zhang et al., PAMI 2025）的67.4 AP相比，VidEoMT在精度和速度上均占优。

- **YouTube-VIS 2021**：VidEoMT达到63.1 AP，略低于CAVIS的64.6（−1.5），但仍显著快于所有对比方法。

- **YouTube-VIS 2022**：VidEoMT达到42.6 AP，超越CAVIS的40.0（+2.6），显示出在更复杂场景下的竞争力。

- **OVIS**：VidEoMT达到55.2 AP，低于CAVIS的57.3（−2.1）。OVIS以严重遮挡和复杂运动著称，这一差距表明在极端实例判别与长时遮挡场景下，VidEoMT仍有改进空间。

**视频全景分割（VPS）结果**（Table 4）：

- **VIPSeg**：VidEoMT达到55.2 VPQ，与CAVIS的56.3接近（−1.1），但速度优势显著。这表明统一编码器架构同样适用于需要同时处理“thing”和“stuff”类别的全景分割任务。

**视频语义分割（VSS）结果**（Table 5）：

- **VSPW**：VidEoMT达到64.9 mIoU，超越**DVIS++**的62.8（+2.1），说明该方法在纯语义分割任务上也具有优势。

**速度-精度权衡**（Figure 1）：散点图直观展示了VidEoMT在不同DINOv2 ViT规模（ViT-S/B/L）下相对于CAVIS和EoMT+CAVIS组合的压倒性速度优势，同时在AP上保持高度竞争力。

### 替代方案对比：编码器-仅架构的必要性

为验证编码器-仅设计的必要性，论文进行了两组关键对比：

**EoMT搭配不同tracker vs. VidEoMT**（Table 6）：将EoMT作为segmenter分别搭配CAVIS tracker、DVIS tracker等最先进追踪器，均无法同时达到VidEoMT的精度和速度。例如EoMT + CAVIS tracker达到68.3 AP但FPS仅34，而VidEoMT在160 FPS下达到68.6 AP。这说明将追踪功能从独立模块迁移到编码器内部是效率提升的关键。

**解码器中的查询融合 vs. 编码器-仅**（Table 7）：在ViT-Adapter + Mask2Former解码器架构中应用查询融合策略（即TrackFormer或本文的查询融合），AP为68.0，FPS为34；而VidEoMT编码器-仅架构达到68.6 AP且FPS为160。这证明**在编码器内部进行查询融合比在解码器中更高效**，因为前者避免了额外的解码器计算开销，同时让ViT的自注意力机制直接参与时序建模。

### 预训练与模型规模的影响

**预训练规模的影响**（Table 8）：VidEoMT的性能高度依赖大规模预训练。使用DINOv2（大规模自监督预训练）时AP为68.6；使用DeiT-III（仅ImageNet-21k监督预训练）时AP骤降至58.3。相比之下，CAVIS在相同预训练变化下的退化幅度较小。这表明VidEoMT的极简设计将更多建模压力转移到了预训练质量上——这是一个重要的局限性：**当预训练规模不足时，VidEoMT的简化架构无法弥补特征质量的缺失**。

**模型规模的影响**（Table 9, Table B）：随着ViT规模从ViT-S增加到ViT-L，VidEoMT的AP持续提升（ViT-L达到68.6），且在所有规模下均保持远超CAVIS的FPS。值得注意的是，即使使用ViT-S，VidEoMT仍能达到远超CAVIS ViT-L的推理速度，证明了架构简化带来的效率增益是普适的。

**预训练方法的影响**（Table 8）：使用DINOv3或EVA-02等更强的预训练权重可进一步提升VidEoMT性能，但需注意RoPE（旋转位置编码）可能导致轻微减速。

### 查询传播策略的消融

附录Table A对比了多种查询传播策略：

- **无传播**（仅EoMT逐帧分割）：AP为61.3，作为基线。
- **仅传播**（无融合，直接复用前一帧查询）：AP恢复至63.9，证明时序信息传递的有效性。
- **非目标重置**（对未匹配的传播查询进行重置）：AP略降至63.5，说明简单重置不如查询融合有效。
- **TrackFormer式传播**：AP为67.7，FPS为117。
- **查询融合（VidEoMT）**：AP为68.6，FPS为160，在精度和速度上均优于TrackFormer。

查询融合的核心优势在于：可学习查询 $\mathbf{Q}^{\mathrm{lrn}}$ 为模型提供了检测新出现目标的灵活性，而线性投影后的传播查询 $\mathtt{Linear}(\mathbf{Q}_{t-1}^{\mathcal{S}})$ 保持了时序连续性。两者通过简单的逐元素相加（而非复杂的交叉注意力）实现融合，既保证了表达能力，又避免了计算开销。

### 失败模式与局限性

1. **对大规模预训练的高度依赖**：当使用DeiT-III等较小规模预训练时，VidEoMT的AP从68.6骤降至58.3。这意味着在预训练资源受限的场景下，VidEoMT的极简设计可能不适用，需要手动验证是否可通过额外的数据增强或辅助损失来缓解。

2. **严重遮挡场景的退化**：在OVIS数据集上，VidEoMT的AP（55.2）仍低于CAVIS（57.3）和**DVIS-DAQ**（Zhou et al., ECCV 2024）。OVIS以严重遮挡、目标消失-重现为特点，仅依赖前一帧查询传播可能无法有效处理长程遮挡。这指向一个开放问题：是否需要引入更长的时序窗口或记忆模块来弥补单帧传播的不足。

3. **编码器全量微调的内存开销**：VidEoMT需要在整个训练过程中微调ViT编码器，而CAVIS等方法冻结编码器。这在资源受限场景下可能带来额外的GPU内存需求，尽管推理阶段的效率优势足以弥补这一训练成本。

### 实验公平性说明

所有FPS和FLOPs测量均在相同的NVIDIA H100 GPU上，使用FlashAttention v2和torch.compile，批量大小为1帧，采用自动混合精度，保证了速度对比的公平性。主流对比方法均使用相同的DINOv2预训练ViT-L骨干，训练设置遵循CAVIS的设定，确保结果可比。FLOPs使用fvcore计算，取验证集所有图像的平均值，与FPS相互印证。

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2602_17807/figures/004_Table_1.jpg]]
*Table 1: From CAVIS to VidEoMT. Stepwise removal of CAVIS modules toward EoMT, and modifications extending it to our VidEoMT. Evaluated on YouTube-VIS 2019 val [38]*

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2602_17807/figures/006_Table_2.jpg]]
*Table 2: Online VIS on YouTube-VIS 2019 and 2021*

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2602_17807/figures/011_Table_7.jpg]]
*Table 7: Alternative approaches: Query propagation in the decoder. Comparison of ViT-Adapter + Mask2Former (M2F) equipped with TrackFormer or our query fusion strategy and the proposed VidEoMT. All methods use a ViT-L backbone with DI-NOv2 pre-training. Evaluated on YouTube-VIS 2019 val*

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2602_17807/figures/009_Table_6.jpg]]
*Table 6: Alternative approaches: EoMT as a segmenter. Comparison of EoMT equipped with state-of-the-art trackers and our proposed VidEoMT. Evaluated on YouTube-VIS 2019 val*

## 定位与知识库关联

### 1. 方法沿革与基线关系

VidEoMT 的核心创新在于对视频分割中“分割器-追踪器”解耦范式的根本性重构。当前最先进的在线视频分割方法——以 **CAVIS** (Lee et al., ICCV 2025)、**DVIS** (Zhang et al., CVPR 2023)、**DVIS++** (Zhang et al., PAMI 2025) 和 **DVIS-DAQ** (Zhou et al., ECCV 2024) 为代表——普遍遵循一条固定的架构蓝图：一个复杂的 segmenter（通常包含 ViT-Adapter + Mask2Former 像素解码器 + Transformer 解码器）负责逐帧生成分割掩码，一个独立的 tracker（包含交叉注意力 Transformer 块、上下文感知特征提取和重识别 MLP）负责跨帧关联实例身份。

VidEoMT 的起点是对这一蓝图的激进简化。它首先将 segmenter 替换为 **EoMT**（encoder-only mask transformer），后者将可学习查询直接注入 ViT 编码器的最后若干层，完全抛弃了像素解码器和 Transformer 解码器。随后，它进一步移除了 tracker 中的上下文感知特征（context-aware features）和重识别层（re-identification layers），最终用一个极简的查询传播与融合机制取代了整个专用追踪模块。这一机制完全运行在 ViT 编码器内部，无需任何额外的跟踪 Transformer 块。

从方法谱系看，VidEoMT 属于 encoder-only 架构在视频理解领域的延伸。EoMT 本身是图像级 encoder-only 分割模型，VidEoMT 将其扩展至时序维度，证明了大规模预训练的 ViT 编码器内部特征已具备足够的实例判别和跨视图一致性能力，仅需轻量级的时序查询机制即可同时完成分割与关联。

### 2. 与替代方案的对比定位

VidEoMT 在实验中系统性地与两类替代方案进行了对比：

**编码器-解码器替代方案**：当将查询融合策略应用于传统的 ViT-Adapter + Mask2Former 解码器架构时，得到的 AP 为 68.0，而 VidEoMT 的编码器-仅架构达到 68.6，且速度更快（160 FPS vs 34 FPS）。这表明查询融合在编码器内部执行比在解码器中执行更高效（Table 7）。

**EoMT 搭配不同追踪器的方案**：将 EoMT 作为 segmenter 与多种最先进追踪器组合（包括 CAVIS 的追踪器），其性能均不及 VidEoMT 的一体化设计（Table 6）。这进一步验证了将时序建模内嵌于编码器的设计优势。

**查询传播策略对比**：在附录的消融中，VidEoMT 的查询融合策略优于 **TrackFormer** 的传播方式（68.6 vs 67.7 AP）且速度更快（160 vs 117 FPS），也优于无传播、仅传播、非目标重置等变体（Table A）。

### 3. 适用边界与依赖条件

VidEoMT 的性能高度依赖于大规模预训练。当使用预训练规模不足的骨干网络（如 DeiT-III）时，AP 大幅下降至 58.3（Table 8），这表明其简化架构的有效性建立在强大的预训练特征基础之上。使用更强的预训练（如 DINOv3 或 EVA-02）可进一步提升性能，但引入 RoPE 等位置编码可能导致轻微减速。

在模型规模方面，VidEoMT 表现出良好的可扩展性：随着 ViT 从 Base 扩展到 Large，性能持续提升，且速度远超同尺寸的 CAVIS（Table 9, Table B）。

### 4. 局限与开放问题

**长时遮挡与重识别**：在 OVIS 等包含严重遮挡的数据集上，VidEoMT 的 AP（55.2）仍略低于 CAVIS（57.3）和 DVIS-DAQ。仅依赖前一帧的查询传播机制在极端实例判别与长时遮挡场景下存在固有局限，可能需要引入更长的时序窗口或显式记忆模块。

**预训练依赖性**：VidEoMT 需要在整个训练过程中微调 ViT 编码器（而 CAVIS 等方法冻结编码器），这在资源受限场景下可能带来额外的内存开销。此外，其性能退化是否与特定的自监督学习目标（如 DINO 的自蒸馏）相关，而非单纯的数据规模，仍需进一步研究。

**开放问题**：
- 预训练 ViT 是否能在剧烈光照变化或多目标密集遮挡等极端场景下完全取代专用追踪模块？
- 该 encoder-only 架构是否可扩展以支持离线模式或全局时序一致性约束，从而在更复杂的视频理解任务上进一步提升精度？
- 对于通用视频分割中的不同子任务（VIS、VPS、VSS），是否需要为每个任务单独调整查询融合策略，还是统一的设计就足够？
- 仅依赖前一帧的查询传播如何有效处理物体消失后重新出现的长程关联问题？

## 原文 PDF

![[paperPDFs/CVPR_2026/VidEoMT_Your_ViT_is_Secretly_Also_a_Video_Segmentation_Model.pdf]]
