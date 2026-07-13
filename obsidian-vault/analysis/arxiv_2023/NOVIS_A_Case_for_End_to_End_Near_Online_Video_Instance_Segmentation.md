---
title: "NOVIS: A Case for End-to-End Near-Online Video Instance Segmentation"
type: paper
paper_level: A
venue: arXiv
year: 2023
pdf_ref: paperPDFs/arxiv_2023/NOVIS_A_Case_for_End_to_End_Near_Online_Video_Instance_Segmentation.pdf
project_link: null
code_link: null
aliases:
- NOVIS
tags:
- arxiv_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/segmentation
- topic/representation_self_supervised_transfer
core_operator: 剪辑长度 (T) 与步长 (S) 的比值，以及基于重叠帧特征计算的重叠嵌入 (overlap embeddings)，在控制计算开销的同时，决定了实例跨剪辑跟踪的可靠性和掩码精度。
primary_logic: 将视频实例分割重塑为短片断上的三维时空掩码预测问题：利用体积 dice 损失处理全遮挡帧，并通过实例查询的余弦相似度匹配替代手工跟踪启发式，实现端到端的近在线处理，消除帧泛化差距，显著提升长视频上的表现。
claims:
- 近在线变体不存在训练-测试帧泛化差距，并且在较长序列上优于在线基线。
- NOVIS 在 YouTube-VIS 2019/2021 和 OVIS 基准上大幅超越所有现有方法，取得新的最佳结果。
- 用嵌入匹配替代手工启发式跟踪带来 +1.1 AP 的提升，重叠嵌入进一步贡献 +0.3 AP。
- 最优近在线配置 T=4, S=2 避免了离线及纯在线方法中出现的性能饱和。
---

# NOVIS: A Case for End-to-End Near-Online Video Instance Segmentation

> [!tip] 核心洞察
> 将视频实例分割重塑为短片断上的三维时空掩码预测问题：利用体积 dice 损失处理全遮挡帧，并通过实例查询的余弦相似度匹配替代手工跟踪启发式，实现端到端的近在线处理，消除帧泛化差距，显著提升长视频上的表现。

| 字段 | 内容 |
|------|------|
| 中文题名 | NOVIS：端到端近在线视频实例分割 |
| 英文题名 | NOVIS: A Case for End-to-End Near-Online Video Instance Segmentation |
| 会议/期刊 | arXiv 2023 |
| Links | [paper](https://arxiv.org/abs/2308.15266) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/segmentation #topic/representation_self_supervised_transfer |
| Method | NOVIS |
| Dataset | YouTube-VIS 2019, YouTube-VIS 2021, OVIS |

> [!tip] 效果简介
> - YouTube-VIS 2019 上，AP state-of-the-art vs IDOL (previous best online method) (+4.5)。
> - YouTube-VIS 2021 上，AP state-of-the-art vs IDOL (previous best online method) (+3.7)。
> - OVIS 上，AP 32.7 (MST=720, T=4, S=2) vs VITA (previous best offline method) (+11.2)。

## 概要

视频实例分割（VIS）要求同时检测、分割并跟踪视频中的所有实例。现有方法主要分为两类：**离线方法**一次性处理整个视频，但存在训练帧数与测试帧数之间的泛化差距，在长序列上性能显著下降；**在线方法**逐帧处理，虽能处理任意长视频，却依赖手工设计的跟踪启发式（如掩码 IoU 匹配），缺乏端到端的时序一致性。

NOVIS 提出**近在线（near-online）**范式，将视频划分为固定长度的短片断（clip），在片断内直接预测三维时空掩码体积，并通过实例查询的余弦相似度匹配实现跨片断跟踪，完全消除了手工跟踪启发式。这一设计从根本上回避了离线方法的帧泛化差距，同时保留了端到端训练的优势。

核心结论：
- **近在线变体不存在训练-测试帧泛化差距**，且在长序列上优于在线基线（Figure 1b）。
- 在 YouTube-VIS 2019/2021 和 OVIS 三个主流基准上，NOVIS 以显著优势刷新最佳结果：OVIS 上领先此前最优离线方法 **VITA**（Heo et al., NeurIPS 2022）**+11.2 AP**（Table 2）。
- 用嵌入匹配替代手工启发式跟踪带来 **+1.1 AP** 的提升，重叠嵌入（overlap embeddings）进一步贡献 **+0.3 AP**（Table 3）。
- 最优近在线配置为剪辑长度 $T=4$、步长 $S=2$，有效避免了离线及纯在线方法中出现的性能饱和（Figure 3）。

方法谱系上，NOVIS 在 Mask2Former 架构基础上引入可学习的时间编码、体积 Dice 损失（处理全遮挡帧）以及重叠嵌入匹配机制，构建了首个无手工跟踪启发式的端到端近在线 VIS 系统。

视频实例分割（Video Instance Segmentation, VIS）要求在视频的每一帧中同时检测、分割并跟踪所有实例。近年来，这一任务主要沿着两条技术路线发展：**在线方法**逐帧处理视频，依赖手工设计的跟踪启发式（如掩码 IoU 与类别匹配）来关联实例；**离线方法**则将整个视频作为输入，以端到端方式联合优化分割与跟踪。

然而，这两种范式各自存在根本性缺陷。离线方法的核心瓶颈在于**训练帧数与测试帧数之间的泛化差距**（frame generalization gap）：模型通常在固定帧数（如 5 帧）的短片断上训练，但在推理时需要处理长达数百帧的视频序列。如图 1a 所示，当测试序列长度远超训练片段时，离线方法的性能会显著退化。在线方法虽能处理任意长度视频，却牺牲了端到端的时序一致性——其跟踪完全依赖手工设计的启发式规则，无法通过损失函数直接优化跨帧关联质量，导致长序列上的身份漂移和遮挡处理能力不足。

近在线（near-online）范式为打破这一僵局提供了潜在出路：将视频分割为带重叠的短片断（clip），在片断内进行端到端时空建模，再通过片断间匹配实现跨片段跟踪。然而，此前的近在线尝试仍沿用逐帧掩码预测与手工跟踪启发式的组合，未能充分释放该范式的潜力。

NOVIS 的动机正是**将视频实例分割重塑为短片断上的三维时空掩码预测问题**。核心洞察在于：若能让模型直接输出整个片断的时空掩码体积（spatio-temporal mask volume），而非逐帧独立预测，则可以通过体积损失函数（volumetric loss）统一优化检测、分割与短程跟踪；同时，用实例查询的嵌入相似度匹配替代手工跟踪启发式，实现端到端可训练的片断间关联。这一设计从根本上消除了训练-测试帧泛化差距，使模型在长视频上的表现不再受限于训练时的片段长度（图 1b）。

## 核心方法与创新机理

NOVIS 的核心创新在于将视频实例分割从“逐帧预测+手工跟踪”或“全序列离线处理”的范式，重塑为**端到端的近在线时空掩码预测**。这一转变通过三个相互耦合的 changed slots 实现，共同消除了离线方法的帧泛化差距，同时摆脱了在线方法对启发式跟踪的依赖。

### 1. 处理范式：从在线/离线到近在线滑动窗口

离线方法（如 **Mask2Former for VIS** (Cheng et al., 2021)、**SeqFormer** (Wu et al., ECCV 2022)、**IFC** (Hwang et al., NeurIPS 2021)）在训练时使用固定长度的短片断，但测试时需处理任意长度的完整视频，导致训练帧数与测试帧数之间存在**泛化差距**——模型在长序列上的性能显著下降（Figure 1a）。在线方法（如 **IDOL** (Wu et al., ECCV 2022)、**MinVIS** (Huang et al., NeurIPS 2022)）虽能处理长序列，却依赖手工设计的跟踪启发式（如掩码 IoU 匹配），缺乏端到端的时序一致性学习。

NOVIS 采用**近在线滑动窗口**策略：将视频划分为长度为 $T$、步长为 $S$ 的重叠短片断（clip），每个片断内进行时空掩码的联合预测，片断间通过可学习的嵌入匹配进行实例关联。这一设计使训练和测试的片断长度保持一致，从根本上消除了帧泛化差距（Figure 1b）。最优配置 $T=4, S=2$ 在避免离线方法性能饱和的同时，显著超越了纯在线基线。

### 2. 实例跟踪：从手工启发式到嵌入匹配

在线方法普遍采用基于掩码 IoU 和物体类别的手工跟踪启发式，这些规则不可微分，无法与分割网络联合优化。NOVIS 将其替换为**基于余弦相似度的实例查询嵌入匹配**：相邻片断的实例查询通过计算输出嵌入的余弦距离进行关联，使整个跟踪过程可端到端训练。

消融实验（Table 3）表明，仅此一项替换便带来 **+1.1 AP** 的提升。进一步地，NOVIS 引入**重叠嵌入（overlap embeddings）**：在相邻片断的重叠帧上，通过掩码交叉注意力（masked cross-attention）专门计算用于匹配的嵌入表示，限制注意力仅作用于共享帧区域。这一设计额外贡献 **+0.3 AP**，尤其改善了长片断下大轨迹变化物体的匹配鲁棒性（Figure 3）。

### 3. 时序分割：从逐帧预测到三维时空掩码体积

传统方法将视频分割视为逐帧的二维掩码预测问题，缺乏对时序维度的显式建模。NOVIS 将每个片断内的实例掩码直接预测为**时空掩码体积** $\mathbf{Y}_i \in \{0,1\}^{T \times H \times W}$：实例查询通过交叉注意力与整个三维特征体积交互，一次性输出该片断内所有帧的掩码。

这一设计带来两个关键优势：
- **体积 Dice 损失**：将 Dice 损失从逐帧计算扩展为整个片断的单一损失，强制模型学习时序一致的掩码边界。
- **全遮挡帧包含**：损失函数包含完全遮挡帧，使模型能够将遮挡预测为掩码体积中的缺失部分，并实现短时重识别——这是 MinVIS 和 VITA 等基线所不具备的能力。

### 4. 时序编码：可学习的位置信息注入

作为时序建模的基础支撑，NOVIS 在空间位置编码之外引入了**可学习的时序编码**（temporal encoding），为每个帧的特征注入时序位置信息。消融实验（Table 3）显示，仅添加时序编码即可提升 **+0.8 AP**，验证了显式时序感知对时空掩码预测的必要性。

### 创新点间的因果耦合

上述四个 changed slots 并非孤立改进，而是形成了一条清晰的因果链：近在线范式（Slot 1）提供了端到端训练的框架基础；三维掩码体积预测（Slot 3）和体积 Dice 损失使模型能够学习时空一致的表示；嵌入匹配（Slot 2）则将这些表示转化为可微分的跨片断关联，最终实现完全摆脱手工启发式的端到端视频实例分割。

NOVIS 将视频实例分割重塑为一个**近在线滑动窗口**下的端到端时空掩码预测问题。其核心设计思想是：将长视频切分为具有重叠帧的短片断（clip），在每个片断内直接预测三维时空掩码体积，并通过嵌入匹配实现跨片断的实例关联，从而完全消除手工设计的跟踪启发式。

### 输入输出与处理范式

给定一段长度为 $T$ 的输入视频 $\mathbf{X} \in \mathbb{R}^{T \times H \times W \times 3}$，NOVIS 以滑动窗口方式将其划分为若干**剪辑**（clip），每个剪辑包含固定数量的连续帧，相邻剪辑之间存在**重叠帧**（overlap）。对于每个剪辑，模型输出一组实例预测，每个实例 $i$ 包含一个时空前景-背景掩码 $\mathbf{Y}_i \in \{0,1\}^{T \times H \times W}$ 及其对应的类别标签。最终，通过跨剪辑的实例匹配，将各剪辑的预测结果拼接为完整视频的实例序列。

这种近在线范式（Figure 1b）的关键优势在于：它既不依赖离线方法所需的完整序列上下文，也不受在线方法逐帧处理的时序视野限制。实验表明，近在线变体**不存在训练-测试帧泛化差距**，在长序列上明显优于纯在线基线。

### 模块化流水线

NOVIS 的整体架构（Figure 2）由五个核心模块串联而成，形成从像素特征到实例序列的端到端流水线：

![[assets/figures/papers/paper_list_l1240_https_arxiv_org_abs_2308_15266/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our near-online NOVIS model architecture and clip processing pipeline. Given a video with length T and clips with overlap*

1. **Backbone（骨干网络）**：对剪辑内的每一帧独立提取图像特征，输出多尺度特征图。论文使用 Swin-L 作为默认骨干。

2. **Pixel Decoder（像素解码器）**：基于可变形注意力（deformable attention）对骨干特征进行多尺度融合，生成逐帧的像素级特征表示。该模块继承自 Mask2Former 的图像分割架构。

3. **Video Instance Decoder（视频实例解码器）**：这是 NOVIS 的核心创新模块。它将逐帧特征堆叠为三维时空特征体积，通过一组可学习的**实例查询**（instance queries）$\mathbf{Q} \in \mathbb{R}^{N \times C}$ 与该体积进行交叉注意力（cross-attention），直接预测每个实例的时空掩码体积和类别。解码器采用逐层掩码注意力机制：前一解码层预测的缩放二值掩码 $\dot{\mathbf{M}}_{l-1} \in \{0,1\}^{N \times T H_{l-1} W_{l-1}}$ 用于遮蔽当前层的交叉注意力区域，使查询聚焦于对应实例的空间位置。

4. **Overlap Embedding Computation（重叠嵌入计算）**：为提升跨剪辑实例匹配的鲁棒性，NOVIS 在最后一个解码层引入重叠注意力掩码：
   $$\hat{\mathbf{M}}_L(n,t,x,y) = \begin{cases} \mathbf{M}_L(n,t,x,y) & \text{if } t \in \tau \\ 0 & \text{otherwise} \end{cases}$$
   该掩码将交叉注意力限制在相邻剪辑的共享重叠帧集合 $\tau$ 上，从而计算出仅依赖重叠区域特征的嵌入向量。若某查询在重叠区域内无预测掩码（即 $\hat{\mathbf{M}}_L(n,t) = 0$ 对所有 $t$ 成立），则跳过重叠注意力计算，直接使用基于完整剪辑的输出嵌入进行匹配。

5. **Instance Matching（实例匹配）**：相邻剪辑间的实例关联通过查询嵌入的**余弦相似度**完成。具体而言，前一剪辑的输出嵌入（或重叠嵌入）与当前剪辑的嵌入进行相似度计算，相似度最高的查询对被判定为同一实例。这一设计完全替代了传统在线方法中基于掩码 IoU 和类别的手工跟踪启发式。

### 损失函数设计

NOVIS 的训练损失由两部分组成：**体积 dice 损失**（volumetric dice loss）和**逐帧掩码损失**（per-frame mask loss）。体积 dice 损失在整个剪辑上计算单一损失值，实验证明其优于逐帧 dice 损失。然而，体积掩码损失因前景-背景像素严重不平衡（尤其当目标在部分帧中被完全遮挡时）而表现不佳，因此掩码损失仍维持在逐帧层面计算。值得注意的是，多帧分割损失**包含完全遮挡帧**，这使模型能够将遮挡预测为三维掩码中的缺失部分，并实现短时重识别。

### 3.1 问题形式化与输入输出

NOVIS 将视频实例分割定义为一个三维时空掩码预测问题。给定一段包含 $T$ 帧的 RGB 视频序列：

$$\mathbf{X} \in \mathbb{R}^{T \times H \times W \times 3}$$

模型需要为序列中的每个实例 $i$ 预测一个时空前景-背景二值掩码：

$$\mathbf{Y}_i \in \{0,1\}^{T \times H \times W}$$

这一形式化将时间维度显式地纳入掩码张量，使模型能够直接建模实例在整个短片断内的存在与消失，包括全遮挡帧。

### 3.2 模型架构与处理流程

NOVIS 采用端到端的近在线滑动窗口范式，其核心架构由以下模块串联构成：

**Backbone → Pixel Decoder → Video Instance Decoder → Overlap Embedding → Instance Matching**

**Backbone** 对输入 clip 的每一帧独立提取图像特征。**Pixel Decoder** 通过可变形注意力计算多尺度逐帧特征图。这两个模块继承自 Mask2Former 的图像分割架构。

**Video Instance Decoder** 是 NOVIS 的核心创新模块。它将一组可学习的实例查询 $\mathbf{Q} \in \mathbb{R}^{N \times C}$（$N$ 为查询数量，$C$ 为特征维度）与 backbone-pixel decoder 输出的三维时空特征体进行交叉注意力计算，直接预测每个实例的时空掩码体积和类别。解码器采用逐层掩码注意力机制：第 $l$ 层的交叉注意力被上一层预测的缩放二值掩码 $\dot{\mathbf{M}}_{l-1} \in \{0,1\}^{N \times T H_{l-1} W_{l-1}}$ 所遮蔽，使查询仅关注其对应实例的前景区域。

### 3.3 损失函数设计

训练损失由两部分组成：针对每个实例的逐帧分类损失，以及掩码预测损失。掩码损失采用混合策略——**体积 dice 损失**搭配**逐帧二值交叉熵损失**，而非纯体积损失。

关键设计决策在于：体积 dice 损失对整个 clip 计算单一损失值，实验证明其优于逐帧 dice 损失；但体积化的逐像素 mask 损失会因目标在多帧被遮挡而导致严重的前景-背景像素不平衡，因此保留逐帧形式。此外，多帧分割损失显式包含全遮挡帧，使模型能够将遮挡预测为三维掩码中的缺失部分，并实现短时重识别。

### 3.4 重叠嵌入与跨剪辑匹配

近在线处理的核心挑战在于相邻 clip 之间的实例身份关联。NOVIS 完全摒弃手工设计的跟踪启发式规则，转而采用基于嵌入余弦相似度的匹配机制。

**标准输出嵌入匹配**：Video Instance Decoder 为每个实例查询输出一个嵌入向量，相邻 clip 的实例通过计算这些嵌入的余弦相似度进行匹配。

**重叠嵌入**：为进一步提升匹配鲁棒性，尤其是对运动幅度大的目标，NOVIS 在最后一个解码器层引入重叠注意力掩码：

$$\hat{\mathbf{M}}_L(n,t,x,y) = \begin{cases} \mathbf{M}_L(n,t,x,y) & \text{if } t \in \tau \\ 0 & \text{otherwise} \end{cases}$$

其中 $\tau$ 为相邻 clip 共享的重叠帧集合。该掩码将交叉注意力限制在重叠帧上，使解码器计算出的嵌入仅编码目标在重叠区域内的外观与位置信息，从而获得更稳定的跨 clip 匹配信号。

当某个查询在重叠区域内没有任何预测掩码时（如目标被完全遮挡），满足条件：

$$\hat{\mathbf{M}}_L(n,t) = 0 \quad \forall t$$

此时模型跳过重叠注意力计算，直接使用基于整个 clip 的标准输出嵌入进行匹配，避免因遮挡导致的嵌入退化。

### 3.5 时间编码

与仅使用空间位置编码的基线方法不同，NOVIS 在空间编码基础上附加**可学习的时间编码**，注入帧序信息。消融实验表明该模块贡献 +0.8 AP（Table 3），是模型感知时序结构的必要组件。

## 实验与关键发现

### 主实验结果

NOVIS 在 YouTube-VIS 2019/2021 和 OVIS 三个主流基准上均取得当时最优结果，且提升幅度显著。

在 YouTube-VIS 2019 验证集上，NOVIS 以 **+4.5 AP** 的优势超越此前最佳在线方法 **IDOL** (Wu et al., ECCV 2022)；在 YouTube-VIS 2021 上则领先 **+3.7 AP**（Table 1）。当联合 COCO 数据进行训练（CC+VIS）时，性能进一步提升，验证了近在线范式对额外图像级数据的有效利用能力。

![[assets/figures/papers/paper_list_l1240_https_arxiv_org_abs_2308_15266/figures/003_Table_1.jpg]]
*Table 1: Benchmark results on the YouTube-VIS 2019 and 2021 validation sets. We sort results by the YouTube-VIS 2019 average precision (AP) and distinguish methods between online (ON), offline (OFF) and near-online (clip length T and stride S). Additional training data by simulating clips via COCO image augmentations is denoted with CC+VIS*

在更具挑战性的 OVIS 基准上，NOVIS 的优势更为突出——以 **32.7 AP**（MST=720, T=4, S=2）超越此前最佳离线方法 **VITA** (Heo et al., NeurIPS 2022) 达 **+11.2 AP**（Table 2）。这一巨大差距源于 OVIS 数据集中普遍存在的长时遮挡与复杂运动，恰好暴露了离线方法因训练-测试帧泛化差距导致的性能退化，而 NOVIS 的近在线滑动窗口设计从根本上规避了这一问题。

![[assets/figures/papers/paper_list_l1240_https_arxiv_org_abs_2308_15266/figures/005_Table_2.jpg]]
*Table 2: Benchmark results on the OVIS validation set. We indicate the minimum size at test-time (MST) of the shortest frame edge and distinguish between online (ON), offline (OFF) and near-online (clip length T and stride S). Our model with ∗ was only evaluated but not trained on larger (720) input resolutions. With ∗∗ we denote a joint training on simulated clips from COCO. Mask2Former and Seq-Former/IFC results are from the MinVis and IDOL papers*

**推理效率方面**，NOVIS 在类似硬件条件下达到约 19.9 FPS，快于多数离线方法，同时保持了端到端可训练的优势，无需手工设计的跟踪启发式。

### 消融实验

Table 3 系统性地验证了从朴素 Mask2Former 应用到完整 NOVIS 模型各设计组件的贡献：

![[assets/figures/papers/paper_list_l1240_https_arxiv_org_abs_2308_15266/figures/006_Table_3.jpg]]
*Table 3: Ablation of our near-online NOVIS method on a OVIS training set split. We motivate several design decisions from a naive application of Mask2Former without temporal encoding (TE) to our final model evaluated with clip length T =4 and stride S=2*

| 消融组件 | AP 提升 | 关键机制 |
|---------|--------|---------|
| 时间编码 (TE) | +0.8 | 可学习的时间位置编码使实例查询能感知帧序 |
| 嵌入匹配替代启发式跟踪 | +1.1 | 余弦相似度匹配消除了手工 IoU 阈值与类别先验的脆弱性 |
| 重叠嵌入 (overlap embeddings) | +0.3 | 在共享帧上计算受限注意力的嵌入，提升长剪辑下的匹配鲁棒性 |

**时间编码**的收益表明，即使对于近在线短片段，显式注入时序信息仍对时空掩码预测至关重要。**嵌入匹配**带来的 +1.1 AP 是单组件最大增益，证实了手工跟踪启发式（基于体积 IoU 和物体类别）是此前方法的重要性能瓶颈。**重叠嵌入**的 +0.3 AP 看似温和，但在长剪辑场景（T≥6）下贡献更为显著——Figure 3 显示，无重叠嵌入时长剪辑的匹配风险急剧上升，而重叠嵌入有效缓解了这一退化。

### 剪辑长度与步长分析

Figure 3 揭示了近在线配置的核心权衡：

- **T=4, S=2** 在 YouTube-VIS 2019 和 OVIS 上均达到最优，既避免了离线方法的长序列泛化差距，又未出现纯在线方法的性能饱和。
- 当 **T > 4** 时，像素解码器难以建模大幅度的物体运动，导致逐帧掩码质量下降（Figure 4 提供独立验证：T≤6 的多帧处理优于单帧处理，但更长剪辑的边际收益递减）。
- 步长 S 控制相邻剪辑的重叠量：S 越小，重叠帧越多，匹配机会增加但计算开销上升。S=2 在精度与效率间取得平衡。

### 掩码质量分析

Figure 4 的逐帧掩码质量分析揭示了一个反直觉发现：**用多帧剪辑训练并评估的模型，其单帧掩码 AP 也优于纯单帧训练的模型**。这表明时空上下文不仅辅助跟踪，还直接提升了实例分割质量——模型学会了利用邻近帧的外观线索来改善当前帧的边界预测。然而，当 T 超过 6 时，这一增益趋于饱和甚至下降，印证了像素解码器对大幅运动的建模局限。

### 失败模式与局限

1. **长剪辑退化**：T > 4 时，像素解码器的空间注意力难以覆盖大位移物体，导致掩码精度下降。这限制了可使用的最大剪辑窗口，进而约束了模型捕获长程时序依赖的能力。
2. **长时遮挡再识别**：尽管重叠嵌入提升了匹配质量，对于超过 60 帧的完全遮挡，实例再识别仍不够稳定。当查询在重叠区域内无预测掩码时（满足 $\hat{\mathbf{M}}_L(n,t)=0\ \forall t$ 条件），模型退回使用全剪辑嵌入匹配，信息量下降。
3. **计算资源边界**：Swin-L 骨干配合 T=4 在高分辨率（MST=720）下已达到计算极限，无法直接扩展至任意长视频或更高帧率场景。
4. **训练数据依赖**：模型依赖视频级实例标注，无法直接利用大规模图像数据集预训练，需通过模拟剪辑（CC+VIS）间接利用，增加了训练管线复杂度。

### 超参数配置

Table 4 汇总了不同基准上的关键超参数差异。值得注意的是，OVIS 因序列中目标数量常超过 20 个，测试时 top-k 预测数需相应增大；学习率策略相比 Mask2Former 调整为两次下降，以适应近在线多帧训练的收敛特性。

![[assets/figures/papers/paper_list_l1240_https_arxiv_org_abs_2308_15266/figures/007_Table_4.jpg]]
*Table 4: Summary of NOVIS hyperparameters for several VIS benchmarks. In contrast to (Cheng et al., 2022), we drop the learning rate (LR) twice. The OVIS (Qi et al., 2022) benchmark contains sequences with more than 20 objects, hence we increase the number of top-k predictions at test-time*

![[assets/figures/papers/paper_list_l1240_https_arxiv_org_abs_2308_15266/figures/009_Figure_5.jpg]]
*Figure 5: Example qualitative results from the YouTube-VIS 2019/2021 validation sets. We show outputs from our NOVIS model with the top-performing Swin-L (Liu et al., 2021b) backbone for 4 frames uniformly selected over the given sequence*

## 定位与知识库关联

### 1. 与现有方法的关系

NOVIS 处于在线与离线视频实例分割（VIS）范式的交汇点，其设计直接回应了这两个方向的核心瓶颈。

**离线方法的瓶颈与突破。** 离线方法（如 **Mask2Former for VIS** (Cheng et al., 2021)、**SeqFormer** (Wu et al., ECCV 2022)、**IFC** (Hwang et al., NeurIPS 2021)）将视频视为一个整体进行时空建模，但存在训练帧数与测试帧数之间的**泛化差距**（Figure 1a）：当测试序列长度远超训练片段时，性能显著下降。NOVIS 通过近在线滑动窗口机制（clip T, stride S）将处理限制在短片断内，从根本上消除了这一差距（Figure 1b），同时保留了端到端的时序建模能力。

**在线方法的启发式替代。** 在线方法（如 **IDOL** (Wu et al., ECCV 2022)、**MinVIS** (Huang et al., NeurIPS 2022)）能够处理任意长序列，但依赖手工设计的跟踪启发式（基于掩码 IoU 和物体类别），缺乏端到端的时序一致性。NOVIS 用**嵌入匹配**（embedding matching via cosine similarity）完全替代了这些启发式，将跟踪信号纳入端到端训练（Table 3：+1.1 AP）。此外，NOVIS 引入**重叠嵌入**（overlap embeddings），仅在相邻剪辑的重叠帧上计算嵌入，进一步提升跨剪辑匹配的鲁棒性（Table 3：额外 +0.3 AP），这在长剪辑场景下尤为关键（Figure 3）。

**与离线方法的架构差异。** 与 **VITA** (Heo et al., NeurIPS 2022) 等离线方法不同，NOVIS 直接预测整个剪辑的**时空掩码体积**（spatio-temporal mask volume），而非逐帧掩码的时序对齐。其损失函数采用**体积 dice 损失**（volumetric dice loss）结合逐帧掩码损失，且显式包含全遮挡帧，使模型能够学习遮挡预测和短期重识别，而 MinVIS 和 VITA 均不包含此能力。

### 2. 适用边界与局限

尽管 NOVIS 在多个基准上取得显著提升，其设计存在明确的适用边界：

- **剪辑长度限制。** 当剪辑长度 T > 4 时，像素解码器难以建模大幅度的物体运动，导致逐帧掩码质量下降（Figure 4）。这限制了可使用的最大剪辑窗口，使模型无法充分利用更长的时序上下文。
- **长期遮挡的脆弱性。** 重叠嵌入提升了长剪辑的匹配质量，但对于超过 60 帧的长期遮挡，实例再识别仍不够稳定。当查询在重叠区域内没有预测掩码时，模型回退到使用整个剪辑的输出嵌入进行匹配，但该机制的鲁棒性有待验证。
- **计算资源约束。** 模型无法处理任意长的视频序列，目前仅支持固定短片断的近在线处理。随着输入分辨率提升（如 OVIS 上的 MST=720）和 Swin-L 骨干的使用，计算开销进一步增加。
- **训练数据依赖。** 训练依赖视频级标注，无法直接利用大规模图像数据集进行预训练，需通过模拟剪辑（如 COCO 图像增强生成伪视频）间接利用，增加了训练流程的复杂性。

### 3. 开放问题

NOVIS 的设计打开了若干值得进一步探索的方向：

1. **时序建模的改进。** 如何通过时间可变形注意力（temporal deformable attention）等机制增强长片段下的运动建模能力，缓解 T > 4 时的性能衰减？
2. **纯在线部署的可能性。** NOVIS 能否在纯在线设置中运行（即 S=1 且无未来帧依赖），同时保留其端到端训练和嵌入匹配的优势？
3. **超长视频与密集场景的扩展。** 在 30 分钟以上且目标密集的视频中，NOVIS 的效率与精度如何？重叠嵌入的计算开销是否成为瓶颈？
4. **匹配机制的进一步优化。** 重叠嵌入的设计能否与时间位置编码更深度耦合，以减少计算开销并提高对遮挡和形变的鲁棒性？
5. **跨任务泛化。** 此类近在线思想能否扩展到其他视频理解任务，如视频全景分割（video panoptic segmentation）或视频语义分割？

## 原文 PDF

![[paperPDFs/arxiv_2023/NOVIS_A_Case_for_End_to_End_Near_Online_Video_Instance_Segmentation.pdf]]
