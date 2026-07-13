---
title: "WIMFRIS: WIndow Mamba Fusion and Parameter Efficient Tuning for Referring Image Segmentation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/WIMFRIS_WIndow_Mamba_Fusion_and_Parameter_Efficient_Tuning_for_Referring_Image_Segmentation.pdf
project_link: null
code_link: https://github.com/MSH970515/WIMFRIS
openreview_forum_id: WnRzN4U8Y8
aliases:
- WIMFRIS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "提出层级Mamba融合（HMF）块，通过窗口Mamba融合器（WMF）将聚合后的多尺度视觉特征与全局文本先验进行窗口化中间融合，以缓解 SSM 的指数衰减问题，实现有效的模态融合。"
primary_logic: "先聚合多层视觉特征，再通过窗口分区限制序列长度，并在每个窗口内注入全局文本标记，使局部区域直接与全局语言上下文交互；既避免了长序列 SSM 的衰减，又增强了局部-全局上下文交互。"
claims:
- "在 RefCOCO 上，去掉 neck 模块导致性能显著下降（ETRIS 从 75.7 降至 72.2）"
- "WMF 通过非重叠窗口划分减少序列长度，有效抑制 SSM 指数衰减"
- "加入 HMF 块可在现有 PET 方法（ETRIS、DETRIS）上提升性能"
- "完整 PET 框架（MSA+EP+MTA）在仅 3.0M 可训参数下达到最优融合效果"
---

# WIMFRIS: WIndow Mamba Fusion and Parameter Efficient Tuning for Referring Image Segmentation

> [!tip] 核心洞察
> 先聚合多层视觉特征，再通过窗口分区限制序列长度，并在每个窗口内注入全局文本标记，使局部区域直接与全局语言上下文交互；既避免了长序列 SSM 的衰减，又增强了局部-全局上下文交互。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | WIMFRIS：窗口Mamba融合与参数高效微调的指代图像分割 |
| 英文题名 | WIMFRIS: WIndow Mamba Fusion and Parameter Efficient Tuning for Referring Image Segmentation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=WnRzN4U8Y8) · [GitHub](https://github.com/MSH970515/WIMFRIS) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | WIMFRIS |
| Dataset | RefCOCO |

> [!tip] 效果简介
> - RefCOCO 上，mIoU (val / testA / testB) 为 77.2 / 78.9 / 74.3 (WIMFRIS-B)，对比 74.3 / 75.8 / 70.8 (DETRIS-B)，变化 +2.9 / +3.1 / +3.5。

## 概要

指代图像分割（RIS）要求模型根据自然语言表达式在图像中精确分割出所指目标。现有参数高效微调（PET）方法主要通过逐层视觉-语言对齐来适配预训练模型，但**忽视了对中间融合 Neck 模块的设计**，导致多尺度视觉特征未能充分聚合，形成信息瓶颈。本文的核心发现是：缺少 Neck 模块会导致显著性能退化——在 RefCOCO 上，ETRIS 去掉 Neck 后 mIoU 从 75.7 降至 72.2（Table 1）。

针对这一问题，本文提出 **WIMFRIS** 框架，核心贡献包括：

1. **层级 Mamba 融合块（HMF）**：先聚合多层视觉特征形成统一的多语义表征，再通过窗口 Mamba 融合器（WMF）与全局文本先验进行中间融合，填补了现有 PET 方法的 Neck 空白。
2. **窗口 Mamba 融合器（WMF）**：将视觉特征划分为非重叠窗口以限制序列长度，并在每个窗口前附加共享的全局文本标记，有效抑制了状态空间模型（SSM）的指数衰减问题，同时实现局部区域与全局语言上下文的直接交互。
3. **参数高效微调策略**：包含 Mamba 文本适配器（MTA）、多尺度对齐器（MSA）和可学习强调参数（EP），在仅 3.0M 可训参数下实现最优融合效果。

在 RefCOCO 基准上，WIMFRIS-B 取得了 77.2/78.9/74.3（val/testA/testB）的 mIoU，较强基线 DETRIS-B 分别提升 +2.9/+3.1/+3.5。消融实验证实，4×4 窗口大小、3-5-7 多尺度核组合的 RFMixer，以及分布式适配器放置 [1,3,5,7,9,11] 均对性能有正向贡献。学习到的强调参数 α 呈下降趋势，表明模型自适应地对早期低层特征施加更强微调。

**局限性**方面，当目标物体过大跨多个窗口时，非重叠窗口划分可能导致物体碎片化；模糊指代表达式或空间上远距离的视觉上下文位于不同窗口时，模型可能分割失败。



指代图像分割（Referring Image Segmentation, RIS）要求模型根据自然语言表达式在图像中分割出对应的目标区域。该任务的核心挑战在于实现细粒度的视觉-语言跨模态对齐。近年来，基于大规模预训练视觉-语言模型（如 CLIP）的方法取得了显著进展，但全量微调这些大模型的计算开销巨大。因此，参数高效微调（Parameter-Efficient Tuning, PET）范式逐渐成为主流，其核心思路是冻结预训练骨干网络，仅训练少量插入的适配器模块。

然而，现有 PET 方法存在一个被忽视的信息瓶颈。当前方法（如 ETRIS、DETRIS）主要在视觉编码器的各层分别进行视觉特征与文本先验的对齐，即**逐层对齐**。这种设计虽然减少了可训练参数量，但缺乏一个专门用于聚合多尺度视觉特征并执行中间融合的 neck 模块。其后果是：来自不同层的多尺度语义信息未能充分汇聚，视觉与语言模态之间的交互停留在浅层、碎片化的层面，限制了分割精度。

具体而言，该瓶颈体现在两个层面。其一，**多尺度特征聚合缺失**：视觉编码器不同层包含不同粒度的语义信息——浅层保留空间细节，深层蕴含高级语义——但逐层对齐策略使得这些特征各自独立与文本交互，无法形成统一的多语义视觉表征。其二，**中间融合能力不足**：即便 DETRIS 等较强方法引入了交叉注意力 neck，其融合仍依赖于简单的逐层交叉注意力机制，未能有效解决长序列下状态空间模型（SSM）的指数衰减问题。

针对上述缺口，本文提出 WIMFRIS（WIndow Mamba Fusion and Parameter Efficient Tuning for Referring Image Segmentation）框架，其核心动机是：**通过层级 Mamba 融合（Hierarchical Mamba Fusion, HMF）块，在 PET 流程中显式引入中间融合 neck，先聚合多层视觉特征，再通过窗口化 Mamba 融合器（Window Mamba Fuser, WMF）实现高效的视觉-语言模态融合**。WMF 将聚合后的视觉特征划分为非重叠窗口，并在每个窗口序列前附加共享的全局文本标记，使得局部区域能够直接与全局语言上下文交互。这一设计同时达成两个目标：通过窗口分区限制序列长度，有效抑制 SSM 的指数衰减；通过局部-全局上下文交互，增强跨模态对齐质量。

此外，WIMFRIS 还配套设计了完整的 PET 策略，包括利用 Mamba 文本适配器（MTA）增强全局文本先验、通过多尺度对齐器（MSA）和可学习强调参数实现自适应的逐层视觉微调。这些组件共同构成一个参数高效且融合能力强大的 RIS 框架。



## 核心方法与创新机理

WIMFRIS 的核心创新围绕一个被现有参数高效微调（PET）方法普遍忽视的信息瓶颈展开：**中间融合 neck 的缺失**。现有 PET 方法（如 ETRIS、DETRIS）主要进行逐层视觉-语言对齐，但各层特征独立与文本交互，多尺度视觉信息未能充分聚合与融合。Table 1 的消融实验直接验证了这一瓶颈——去掉 neck 模块后，ETRIS 在 RefCOCO 上的性能从 75.7 显著降至 72.2（`$\Delta = -3.5$`），证明中间融合对指代图像分割至关重要。

针对此瓶颈，WIMFRIS 提出了三个相互协同的 changed slots：

### 1. 层级 Mamba 融合块（HMF）——填补 Neck 空白

HMF 块是本文最核心的架构创新。与先前方法（Figure 1a）将各层视觉特征分别与文本先验做交叉注意力不同，HMF 首先将多层 MSA 调优后的视觉特征沿通道维度拼接，经 1×1 卷积聚合为统一的多语义表示，再通过窗口 Mamba 融合器（WMF）执行一次集中的中间融合（Figure 1b）。这一“先聚合、再融合”的设计避免了逐层独立融合带来的信息碎片化。

关键证据来自 Table 1：将 HMF 块嵌入现有 PET 方法后，ETRIS 性能从 74.5 提升至 75.7（`$+1.2$`），DETRIS 从 75.8 提升至 76.4（`$+0.6$`），验证了 HMF 作为通用 neck 模块的有效性。

### 2. 窗口 Mamba 融合器（WMF）——克服 SSM 指数衰减

WMF 模块解决了将 Mamba SSM 直接应用于视觉-文本融合时的根本性挑战：**长序列导致的指数衰减**。SSM 的隐藏状态满足范数不等式 `$\| h_t \| \leq M \|\overline{\boldsymbol{B}}\| \sum_{k=1}^{t} \lambda^{t-k} \|\boldsymbol{x}_k\|$`（Appendix B.2），即过去输入对当前状态的贡献呈几何级衰减。当视觉特征序列较长时，早期 token 的信息几乎完全丢失。

WMF 通过以下机制缓解此问题（Figure 3b）：
- **非重叠窗口划分**：将聚合后的视觉特征图划分为 `$n_{win} = H \cdot W / M$` 个窗口，将序列长度从 `$HW$` 缩减至 `$M$`（窗口内 token 数），有效限制衰减范围；
- **全局文本先验注入**：将共享的文本类标记 `$f_t^{cls}$` 扩展并拼接到每个窗口序列前，使每个局部窗口直接与全局语言上下文交互。

Table 3(a) 的消融实验表明，窗口大小 4×4 在 RefCOCO 上取得最优性能（77.3/79.2/74.8），优于无窗口拼接方案（76.0/77.9/73.4），证实了窗口化设计对 SSM 融合的必要性。

### 3. 参数高效微调框架——MTA + MSA + 强调参数

完整的 PET 框架包含三个组件，仅引入 3.0M 可训参数（Table 3(b)）：

- **Mamba 文本适配器（MTA）**：利用 SSM 块增强文本 token 的全局长程依赖，输出增强的全局文本先验 `$f_t$`。公式为：下采样 → ReLU → 投影 → Conv1D → SiLU → SSM → 残差连接上采样（Section 2.2）。

- **多尺度对齐器（MSA）**：核心是 RFMixer 模块，通过多分支深度可分离带状卷积（核大小 3-5-7）捕获多尺度上下文，再与全局文本先验做交叉注意力对齐。Table 4 表明 3-5-7 核组合达到最高 IoU（77.3/79.2/74.8）。

- **可学习强调参数（EP）**：通过 sigmoid 门控 `$\alpha = \sigma_{Sigmoid}(p) = \frac{1}{1+e^{-p}} \in (0,1)$` 自适应调整各层微调强度。Figure 6 显示学习到的 `$\alpha$` 值呈一致下降趋势，表明模型自动对早期低层特征施加更强微调，对深层语义层逐渐减弱——这一涌现行为验证了设计的合理性。

Table 3(b) 的逐步消融清晰展示了各组件的累积贡献：仅 MSA 时性能为 75.1，加入 EP 后升至 76.6，再加入 MTA 后达到最优 77.3，全程可训参数仅从 2.8M 增至 3.0M。

### 局限与待解决问题

WMF 的非重叠窗口划分存在固有局限：当目标物体过大跨多个窗口时，因窗口间空间隔离导致物体碎片化（Figure 7）；当区分目标所需的视觉上下文分布在远距离不同窗口时，模型无法建立跨窗口关联。如何设计融合模块以打破窗口分隔的空间隔离，是未来工作的关键方向。此外，当前融合仅为单向（视觉-文本），双向信息流的探索可能进一步提升鲁棒性。



![[assets/figures/papers/iclr26_0012_WnRzN4U8Y8_WIMFRIS_WIndow_Mamba_Fusion_and_Parameter_Effici/figures/004_Figure_2.jpg]]
*Figure 2: (a) Overview of WIMFRIS architecture. Frozen CLIP text encoder layers and DINOv2 vision encoder layers are parameter-efficient tuned by MTA (b) to get enhanced global textual features ft, and MSA (c) with learnable emphasis parameters and RFMixer (d) to obtain fine-grained visual features fv. Subsequently, our HMF block performs powerful vision-language intermediate modality fusion*

WIMFRIS 的整体 pipeline 建立在“冻结骨干 + 参数高效微调 + 中间融合”的三段式架构上，如图 2(a) 所示。其核心设计逻辑是：现有 PET 方法主要进行逐层视觉-语言对齐，但忽视了中间融合所需的 neck 模块，导致多尺度特征未能充分聚合与融合，形成信息瓶颈。WIMFRIS 通过引入层级 Mamba 融合（HMF）块和配套的 PET 适配器，填补了这一空白。

**输入与骨干编码**：输入为图像和指代表达式文本。图像由冻结的 DINOv2 视觉编码器提取多层视觉特征，文本由冻结的 CLIP 文本编码器提取多层文本特征。两个编码器在整个训练过程中保持冻结，仅通过轻量级适配器进行参数高效微调。

**PET 适配器层**：在冻结骨干的特定层上插入两类适配器。Mamba 文本适配器（MTA）对文本特征进行 SSM 增强，利用 Mamba 块的长程依赖建模能力输出全局文本先验 $f_t$，为后续模态对齐提供强引导。多尺度对齐器（MSA）对视觉特征进行处理，其内部包含 RFMixer 模块和交叉注意力层：RFMixer 通过多分支深度可分离带状卷积（核大小 3-5-7）捕获多尺度上下文，交叉注意力层则将增强后的视觉特征与全局文本先验对齐。每个 MSA 输出由可学习的强调参数 $\alpha \in (0,1)$ 进行 sigmoid 门控加权，以自适应调整各层的微调强度——实验表明，$\alpha$ 值随层级加深呈下降趋势，说明模型倾向于对早期低层特征施加更强的微调。

**中间融合 Neck**：经过 MSA 逐层对齐后的多层视觉特征 $\{f_v^i\}$ 被送入 HMF 块。HMF 首先通过通道拼接和 $1\times1$ 卷积将多层特征聚合为统一的多语义视觉表征，然后由窗口 Mamba 融合器（WMF）执行中间融合。WMF 的核心操作是：将聚合后的视觉特征图划分为非重叠窗口（如 $4\times4$），在每个窗口序列前附加共享的全局文本类标记 $f_t^{cls}$，然后进行并行的窗口级 SSM 扫描。这一窗口化设计有效抑制了 SSM 的指数衰减问题——因为序列长度被限制在窗口内，避免了长序列中过去输入贡献的几何级衰减。扫描完成后，WMF 通过注意力门控机制重组融合输出。

**任务解码器**：HMF 输出的融合特征被送入任务解码器（沿用 DETRIS 的设计），结合对比损失、Dice 损失和逐窗口对齐损失，生成最终的分割掩码。

整个框架中，可训练参数仅约 3.0M（以 WIMFRIS-B 为例），包括 MTA、MSA（含 RFMixer 和交叉注意力）、强调参数、HMF 块以及解码器。消融实验（Table 3）证实，完整的 PET 策略（MSA + EP + MTA）在仅 3.0M 可训参数下达到最优融合效果；而去掉 neck 模块会导致性能显著下降（ETRIS 从 75.7 降至 72.2），验证了中间融合 neck 的关键作用。



### 1. Mamba 文本适配器（MTA）

MTA 的目标是利用状态空间模型（SSM）增强 CLIP 文本编码器输出的文本标记，使其具备全局长程依赖，为后续视觉-语言对齐提供更强的文本先验。其计算流程为：

$$
\begin{array} { r l } 
& { \mathbf { x } _ { t - f c } ^ { l } = \sigma _ { \mathrm { R e L U } } \big ( \mathrm { D o w n } ( \mathbf { x } _ { t } ^ { l } ) \big ) , } \\ 
& { \mathbf { x } _ { t \_ S S M } ^ { l } = \mathrm { S S M } \big ( \sigma _ { \mathrm { S i L U } } \big ( \mathrm { C o n v 1 D } ( \mathrm { P r o j } _ { \mathrm { i n } } ( \mathbf { x } _ { t \_ f c } ^ { l } ) ) \big ) \big ) , } \\ 
& { \mathbf { x } _ { t \_ r e s } ^ { l } = \sigma _ { \mathrm { S i L U } } \big ( \mathrm { P r o j } _ { \mathrm { i n } } ( \mathbf { x } _ { t \_ f c } ^ { l } ) \big ) , } \\ 
& { \mathbf { x } _ { t \_ o u t } ^ { l } = \mathrm { U p } \big ( \mathrm { P r o j } _ { \mathrm { o u t } } ( \mathbf { x } _ { t \_ S S M } ^ { l } \cdot \mathbf { x } _ { t \_ r e s } ^ { l } ) + \mathbf { x } _ { t \_ f c } ^ { l } \big ) , } 
\end{array}
$$

其中：$\mathbf{x}_t^l$ 为 CLIP 第 $l$ 层输出的文本特征；$\mathrm{Down}$ 和 $\mathrm{Up}$ 分别为下采样和上采样操作；$\sigma_{\mathrm{ReLU}}$ 和 $\sigma_{\mathrm{SiLU}}$ 为激活函数；$\mathrm{Proj_{in}}$ 和 $\mathrm{Proj_{out}}$ 为线性投影；$\mathrm{Conv1D}$ 为一维卷积；$\mathrm{SSM}$ 为 Mamba 块中的状态空间模型。残差连接 $\mathbf{x}_{t\_fc}^l$ 保证了训练稳定性。该模块以线性计算复杂度捕获全序列依赖，输出增强的全局文本特征，其中类别标记 $f_t^{cls}$ 将作为后续 WMF 模块中的共享文本先验。

### 2. 多尺度对齐器（MSA）

MSA 负责将冻结的 DINOv2 视觉编码器输出与 MTA 增强的文本先验对齐。其核心包含两个组件：RFMixer 和交叉注意力。

#### 2.1 RFMixer

RFMixer 通过多分支深度可分离带状卷积捕获多尺度视觉上下文：

$$
\begin{array} { r l } 
& { \tilde { \mathbf { x } } _ { v } ^ { i ( k ) } = \mathrm { D W C o n v } _ { c _ { k } \times 1 } \Big ( \mathrm { D W C o n v } _ { 1 \times c _ { k } } \big ( \mathbf { x } _ { v } ^ { i } \big ) \Big ) , } \\ 
& { \tilde { \mathbf { x } } _ { v } ^ { i } = \sigma _ { \mathrm { R e L U } } \Big ( \mathbf { x } _ { v } ^ { i } + \sum _ { k = 1 } ^ { 3 } \tilde { \mathbf { x } } _ { v } ^ { i ( k ) } \Big ) , } \\ 
& { \mathbf { x } _ { v \_ m i x } ^ { i } = \tilde { \mathbf { x } } _ { v } ^ { i } \odot \mathbf { x } _ { v } ^ { i } , } 
\end{array}
$$

其中 $\mathbf{x}_v^i$ 为第 $i$ 层视觉特征；$c_k$ 为第 $k$ 个分支的卷积核尺寸（默认 $c_1=3, c_2=5, c_3=7$）；$\mathrm{DWConv}$ 为深度可分离卷积；$\odot$ 为逐元素乘积。消融实验（Table 4）证实 3-5-7 多尺度核组合达到最优 IoU（RefCOCO val: 77.3）。

#### 2.2 强调参数（Emphasis Parameter）

为自适应控制各层微调强度，MSA 引入可学习的强调参数 $\alpha$：

$$
\begin{array} { l } 
{ { \displaystyle p = \mathrm { l o g i t } ( \alpha _ { 0 } ) = \mathrm { l n } \bigg ( \frac { \alpha _ { 0 } } { 1 - \alpha _ { 0 } } \bigg ) , } } \\ 
{ { \displaystyle \alpha = \sigma _ { S i g m o i d } ( p ) = \frac { 1 } { 1 + e ^ { - p } } ~ \in ~ ( 0 , 1 ) , } } \\ 
{ { \displaystyle f _ { v } ^ { i } = x _ { v } ^ { i } + \alpha \cdot \mathbf { x } _ { v . f u s e d } ^ { i } } , } 
\end{array}
$$

其中 $p$ 为可学习参数，通过 sigmoid 函数映射到 $(0,1)$ 区间。可视化结果（Figure 6）显示 $\alpha$ 值呈一致的下降趋势，表明模型学习对 DINOv2 早期低层特征施加更强的微调，而对深层高语义层施加减弱的微调。

### 3. 层级 Mamba 融合块（HMF）与窗口 Mamba 融合器（WMF）

HMF 块是 WIMFRIS 的核心创新，解决现有 PET 方法缺乏有效中间融合 neck 的瓶颈。其工作流程为：首先聚合 MSA 调优后的多层视觉特征，然后通过 WMF 模块与全局文本先验进行窗口化融合。

#### 3.1 WMF 窗口化 SSM 扫描

WMF 将聚合后的视觉特征图划分为 $n_{win} = H \cdot W / M$ 个非重叠窗口（$M$ 为窗口尺寸），并在每个窗口序列前附加共享的全局文本类别标记 $f_t^{cls}$：

$$
\begin{array} { r l } 
& { { x _ { j } } = \left[ \underline { { { f _ { t } ^ { c l s } } } } ^ { \prime } , \ { f _ { v } ^ { w i n } } [ j ] \right] , \ j = 1 , \ldots , { n _ { w i n } } , } \\ 
& { { X } = \{ x _ { j } \} _ { j = 1 } ^ { { n _ { w i n } } } \in \mathbb { R } ^ { { n _ { w i n } } \times ( M + 1 ) \times C } , } \\ 
& { { Y } = \mathrm { S S M } _ { j } ( X ) \in \mathbb { R } ^ { { n _ { w i n } } \times ( M + 1 ) \times C } , } 
\end{array}
$$

其中 $f_v^{win}[j]$ 为第 $j$ 个窗口内的视觉特征；$\underline{f_t^{cls}}'$ 为扩展后的文本标记。每个窗口独立执行并行 SSM 扫描，输出经注意力门控重组为完整特征图。

**设计动机**：SSM 存在指数衰减问题，其隐藏状态范数满足：

$$
\| h _ { t } \| \leq M \| \overline { { \boldsymbol B } } \| \sum _ { k = 1 } ^ { t } \lambda ^ { t - k } \| \boldsymbol x _ { k } \|
$$

过去输入 $\boldsymbol{x}_k$ 对当前状态 $h_t$ 的贡献随距离 $t-k$ 呈几何级衰减。WMF 通过窗口分区将序列长度从 $HW$ 缩减至 $M$，有效抑制了长序列下的信息衰减。消融实验（Table 3a）表明窗口尺寸 $4 \times 4$ 在 RefCOCO 上取得最优性能（val: 77.3），优于无窗口拼接方案（val: 76.0）。

### 4. 损失函数

训练使用三项损失的加权组合：

- **文本-像素对比损失**，正样本对优化余弦相似度，负样本对优化不相似度：

$$
\mathcal { L } _ { \mathrm { c o n } } ^ { i } ( Z _ { t } , Z _ { c } ^ { i } ) = \left\{ \begin{array} { l l } 
{ - \log \bigl ( \sigma ( Z _ { t } \cdot Z _ { c } ^ { i } ) \bigr ) , } & { i \in \mathcal { P } , } \\ 
{ - \log \bigl ( 1 - \sigma ( Z _ { t } \cdot Z _ { c } ^ { i } ) \bigr ) , } & { i \in \mathcal { N } , } 
\end{array} \right.
$$

- **Dice 损失**，优化掩码重叠度：

$$
\mathrm { D i c e } ( \mathbf { p } , \mathbf { g } ) = \frac { 2 \sum _ { i = 1 } ^ { M } p _ { i } ^ { ( b ) } g _ { i } ^ { ( b ) } } { \sum _ { i = 1 } ^ { M } p _ { i } ^ { ( b ) } + \sum _ { i = 1 } ^ { M } g _ { i } ^ { ( b ) } + \varepsilon }
$$

- **对齐损失**，逐窗口二值交叉熵强化窗口内文本-像素对齐：

$$
\mathcal { L } _ { \mathrm { a l i g n } } = \frac { 1 } { B n _ { \mathrm { w i n } } } \sum _ { b = 1 } ^ { B } \mathrm { B C E } \big ( \ell ^ { ( b ) } , m ^ { ( b ) } \big )
$$

损失权重设置为 $\lambda_{con}=0.5$，$\lambda_{dice}=0.3$，$\lambda_{align}=0.2$。



## 实验与关键发现

### 核心瓶颈验证：Neck 模块的必要性

Table 1 的消融实验直接验证了本文的核心论断——中间融合 Neck 模块构成现有 PET 方法的信息瓶颈。移除 Neck 模块后，ETRIS 在 RefCOCO 上的 mIoU 从 74.5 骤降至 72.2（val），DETRIS 则从 75.8 降至 73.4，降幅分别达 2.3 和 2.4 个百分点。这一结果确证了仅做逐层视觉-语言对齐而缺乏中间多尺度聚合融合，会导致模态信息无法充分交互。

![[assets/figures/papers/iclr26_0012_WnRzN4U8Y8_WIMFRIS_WIndow_Mamba_Fusion_and_Parameter_Effici/figures/001_Table_1.jpg]]
*Table 1: Analysis of neck module functioning. Omission of the neck module results in significant performance degradation, highlighting its critical role in performing intermediate fusion. Incorporating our HMF-block into existing PET-based approaches further improves their performance. Furthermore, our WIMFRIS utilizing proposed HMF-block and PET framework achieves state-ofthe-art performance*

将本文提出的 HMF 块插入现有 PET 方法后，ETRIS+HMF 达到 74.5（+2.3），DETRIS+HMF 达到 76.4（+0.6），表明 HMF 块作为即插即用的 Neck 模块具有跨方法的泛化增益能力。完整的 WIMFRIS 框架（含 MSA+EP+MTA 适配器与 HMF 块）在仅 3.0M 可训参数下达到 77.2/78.9/74.3（RefCOCO val/testA/testB），验证了"聚合-窗口化融合"路线的有效性。

### 与 SOTA 方法的全面对比

Table 2 展示了 WIMFRIS 在 RefCOCO、RefCOCO+ 和 G-Ref 三个标准基准上与现有方法的系统对比。WIMFRIS-B（DINOv2-B/14 骨干）在 RefCOCO 上达到 77.2/78.9/74.3，相较最强 PET 基线 DETRIS-B 的 74.3/75.8/70.8，分别提升 +2.9/+3.1/+3.5 个点；在 RefCOCO+ 和 G-Ref 上也持续领先。WIMFRIS-L（DINOv2-L/14）进一步提升至平均 73.4 mIoU，在混合 RefCOCO 数据训练设置下（WIMFRIS-L*）平均 mIoU 达 78.2，超越所有对比方法。

![[assets/figures/papers/iclr26_0012_WnRzN4U8Y8_WIMFRIS_WIndow_Mamba_Fusion_and_Parameter_Effici/figures/006_Table_2.jpg]]
*Table 2: Comparison of State-of-the-art RIS methods and the PET RIS methods on RefCOCO, RefCOCO+ and G-Ref datasets without using extra data and Mixed RefCOCO dataset, evaluated using the mIoU metric. Models marked with * are trained on the mixed RefCOCO, RefCOCO+ and G-Ref data. The best results are written in bold*

值得注意的是，WIMFRIS 在仅微调 3.0M 参数的条件下，超越了多数全量微调方法，验证了"冻结骨干 + 参数高效适配器 + 中间融合 Neck"技术路线的竞争力。

### 窗口化融合的关键消融

**窗口大小**（Table 3a）：WMF 模块的窗口大小对性能有显著影响。直接拼接多模态 token 而不做窗口划分（†标记）仅得 76.0/77.9/73.4，而 4×4 窗口达到最优的 77.3/79.2/74.8。窗口过小（2×2）或过大（8×8、16×16）均导致性能下降。这一趋势与 SSM 的指数衰减特性一致：窗口过大时序列过长，衰减效应削弱远端信息；窗口过小时局部上下文不足。4×4 窗口在序列长度与局部感受野间取得最优平衡。

![[assets/figures/papers/iclr26_0012_WnRzN4U8Y8_WIMFRIS_WIndow_Mamba_Fusion_and_Parameter_Effici/figures/007_Table_3.jpg]]
*Table 3: Ablation studies on the window size of the WMF module and the PET strategy components. (a) Window size. † denotes that we simply concatenated the multi-modal tokens without window partitioning. The second smallest window size of 4 × 4 yields the best performance*

**PET 策略组件**（Table 3b）：从基础适配器逐步叠加 MSA、EP 和 MTA，性能从 76.0 逐步提升至 77.3，可训参数仅从 2.0M 增至 3.0M。其中 MSA 贡献最大（+0.8），EP 和 MTA 各带来约 0.2-0.3 的增益，表明多尺度视觉对齐是核心驱动力，而强调参数和 Mamba 文本适配器提供互补的精细化改进。

**RFMixer 卷积核**（Table 4）：多尺度核组合 3-5-7 以 3.04M 参数达到最优 77.3/79.2/74.8，优于单一尺度核（如 3-3-3 的 76.4/78.5/73.9）和其他组合。这验证了多分支带状卷积捕捉不同感受野上下文对视觉特征增强的必要性。

![[assets/figures/papers/iclr26_0012_WnRzN4U8Y8_WIMFRIS_WIndow_Mamba_Fusion_and_Parameter_Effici/figures/010_Table_4.jpg]]
*Table 4: Ablation study on the kernel sizes of the convolutional branches in the RFMixer. Using kernel sizes of 3 , 5 , and 7 in the RFMixer branches yields the best performance*

**适配器放置策略**（Table 5）：默认的分布式放置 [1,3,5,7,9,11] 显著优于集中式方案（早期 [0-5] 76.4、中期 [3-8] 76.6、后期 [6-11] 76.2），表明在整个骨干网络的浅层和深层均匀注入语言引导，比仅在某一段集中对齐更有效。

![[assets/figures/papers/iclr26_0012_WnRzN4U8Y8_WIMFRIS_WIndow_Mamba_Fusion_and_Parameter_Effici/figures/030_Table_5.jpg]]
*Table 5: Ablation study on the Impact of PET adapter placement strategies. Default [1, 3, 5, 7, 9, 11] configuration yields the best performance. Note that the layer number is zero-indexed*

### 强调参数的学习动态

Figure 6 可视化了可学习强调参数 α 在各数据集上的收敛趋势。α 值呈现一致的下降趋势：浅层（layer 1-5）α 值较高（0.6-0.8），深层（layer 9-11）降至 0.2-0.4。这表明模型自主学习到：DINOv2 的早期低层特征需要更强的微调以适配指代分割任务，而高层语义特征已具备较好的泛化性，只需轻微调整。这一发现为 PET 适配器的非均匀设计提供了经验依据。

### 定性分析与典型失败模式

Figure 4 展示了 WIMFRIS 与 DETRIS 在五个挑战性场景下的定性对比。WIMFRIS 在开放词汇表达（如"the rightmost zebra"）和精细边界分割上表现更优，生成的掩码更贴合物体轮廓且误分割区域更少。

Figure 7 揭示了三个典型失败模式，与 limitations 分析一致：

1. **大物体碎片化**：当目标物体跨越多个非重叠窗口时，各窗口独立对齐全局文本先验，缺乏窗口间协调，导致掩码出现断裂或孔洞。
2. **模糊指代歧义**：当指代表达式缺乏明确空间线索（如"the thing next to the man"）时，每个窗口独立判断文本-视觉对齐，可能产生多区域错误响应。
3. **远距离上下文缺失**：区分目标所需的视觉线索位于不同窗口时，窗口间的空间隔离使模型无法建立跨窗口依赖，导致错误分割。

这些失败模式直接指向 WMF 窗口设计的固有权衡：窗口划分有效抑制了 SSM 指数衰减，但引入了窗口间空间隔离。如何设计跨窗口交互机制以保持线性复杂度优势，是后续研究的关键开放问题。



## 定位与知识库关联

### 在 RIS 方法谱系中的位置

WIMFRIS 属于**参数高效微调（PET）范式下的指代图像分割（RIS）方法**。与需要全量微调视觉骨干的传统 RIS 方法（如 LAVT、CRIS、ReLA）不同，WIMFRIS 冻结 CLIP 文本编码器与 DINOv2 视觉编码器，仅训练轻量适配器与中间融合模块，将可训参数量压缩至约 3.0M。这一设计使其在 RefCOCO 等标准基准上以极低参数代价超越了多数全量微调方法（Table 2），同时显著优于同期 PET 方法。

**与基线方法的本质差异**：

- **ETRIS**：作为早期 PET 方法，仅在 DINOv2 各层独立进行视觉-语言对齐，缺乏中间融合 neck。Table 1 表明，去除 neck 模块后 ETRIS 性能从 75.7 骤降至 72.2（RefCOCO val），验证了逐层对齐的信息瓶颈。
- **DETRIS**：引入交叉注意力 neck 和适配器，是 WIMFRIS 的主要对比基准。然而 DETRIS 的 neck 仍以逐层交叉注意力为核心，未对多尺度特征进行聚合。WIMFRIS 的 HMF 块先聚合三层视觉特征为统一多语义表示，再通过 WMF 执行窗口化中间融合，在 RefCOCO 上实现 +2.9/+3.1/+3.5（val/testA/testB）的 mIoU 提升（Table 2）。

**核心方法贡献的因果链条**：

1. **瓶颈识别**：现有 PET 方法忽视 neck 模块的中间融合能力，多尺度特征无法充分聚合。
2. **控制变量**：HMF 块 + WMF 模块，通过窗口分区抑制 SSM 的指数衰减（见公式 $\| h_t \| \leq M \|\overline{\boldsymbol{B}}\| \sum_{k=1}^t \lambda^{t-k} \|\boldsymbol{x}_k\|$），使局部视觉区域直接与全局文本先验交互。
3. **关键证据**：Table 1 中，将 HMF 块插入 ETRIS（+1.7 mIoU）和 DETRIS（+0.6 mIoU）均获得一致提升；Table 3(a) 中窗口大小 4×4 优于无窗口拼接（† 行），验证了窗口化设计的有效性。

### 适用边界与条件

**有效场景**：
- 冻结 DINOv2/CLIP 骨干的 PET 设置，可训参数 ≤ 3.0M。
- 指代表达式具有明确语义，目标物体尺寸适中（不跨多个窗口）。
- 数据集为 RefCOCO、RefCOCO+、G-Ref 等标准 RIS 基准。

**关键设计依赖**：
- WMF 的非重叠窗口划分假设目标物体可被单个窗口覆盖。窗口大小 4×4 在 RefCOCO 上最优（Table 3a），但该超参数可能与图像分辨率和物体尺度分布相关。
- 强调参数 α 的学习曲线（Figure 6）显示一致的下降趋势，表明低层特征需要更强微调。这一规律依赖于 DINOv2 的特征层次结构，迁移到其他视觉骨干时需重新验证。
- RFMixer 的多尺度核组合 3-5-7 在消融中取得最优（Table 4），但该配置可能对特定的感受野需求敏感。

### 已知局限与失败模式

根据 Figure 7 和论文分析，WIMFRIS 存在三类典型失败模式：

1. **大物体碎片化**：当目标物体过大、跨越多个非重叠窗口时，WMF 的窗口间空间隔离导致各窗口独立生成局部响应，无法合并为统一掩码。这是窗口分区设计的固有代价。
2. **模糊指代下的错误对齐**：当指代表达式缺乏明确上下文时，每个窗口独立对齐全局文本先验，缺少窗口间一致性约束，可能导致多个窗口同时错误激活或漏激活。
3. **远距离上下文割裂**：当区分目标所需的视觉线索（如“穿红衣服的人旁边的狗”）在空间上相距较远且落入不同窗口时，WMF 无法建模跨窗口的空间关系，导致分割失败。

此外，当前融合架构是**单向的（视觉 ← 文本）**，未探索视觉到文本的反向信息流。这是方法层面的结构性限制，而非实现细节。

### 开放问题与后续方向

1. **跨窗口空间建模**：如何打破 WMF 的非重叠窗口隔离，使大物体和远距离视觉上下文得到统一理解？可能的路径包括窗口间注意力、重叠窗口划分或层次化窗口设计。
2. **双向多模态融合**：在保持参数高效的前提下实现视觉 → 文本的信息流，可能增强模型对模糊指代和歧义表达的鲁棒性。
3. **任务泛化性**：HMF 块和 PET 策略能否推广到其他密集预测任务（如指代视频分割、视觉定位）？论文明确将此列为未验证的开放问题。
4. **零样本 RIS 适配**：当前框架依赖有监督微调，如何适配到零样本指代图像分割这一更具挑战性的前沿任务，尚未被探索。



## 原文 PDF

![[paperPDFs/ICLR_2026/WIMFRIS_WIndow_Mamba_Fusion_and_Parameter_Efficient_Tuning_for_Referring_Image_Segmentation.pdf]]
